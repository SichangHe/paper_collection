                                          Semantic Prefix Oracles for LLM Decoding: Contracts
                                                      and Differential Validation
                                                                                                Paul Kronlund-Drouault✉
                                                                                                        ENS de Lyon
                                                                                                        Lyon, France
                                                                                                    Unsuspicious Industries
                                                                                                        Paris, France
                                                                                                      Université de Lille
                                                                                                         Lille, France
                                                                                                    pkd@unsuspicious.org
arXiv:2609.35425v1 [cs.PL] 28 Sep 2026




                                         Abstract                                                                  CCS Concepts: • Theory of computation → Grammars
                                         Constrained decoding can enforce regular or context-free                  and context-free languages; • Software and its engi-
                                         output formats, but many program-generation failures are se-              neering → Formal language definitions; Software testing
                                         mantic: scope, typing, and declaration effects depend on con-             and debugging; • Computing methodologies → Natural
                                         text. We present semantic grammar specifications, a declara-              language processing.
                                         tive formalism that attaches such constraints to a context-               Keywords: constrained decoding, semantic prefix grammars,
                                         free surface and executes them during Earley descent. Our                 attribute grammars, differential testing, large language mod-
                                         implementation enforces safe pruning: it rejects only pre-                els
                                         fixes whose semantic contradictions cannot be repaired by
                                                                                                                   ACM Reference Format:
                                         any continuation. A separate, grammar-dependent, dead-end
                                                                                                                   Paul Kronlund-Drouault. 2026. Semantic Prefix Oracles for LLM
                                         freedom property guarantees the existence of a realizable                 Decoding: Contracts and Differential Validation. In Proceedings of
                                         witness for each remaining branch. We give simple sufficient              the 2nd ACM SIGPLAN International Workshop on Language Models
                                         conditions based on surface productivity, type coverage, and              and Programming Languages (LMPL ’26), October 4–9, 2026, Oakland,
                                         left-to-right constraint flow. Our finite-lambda, core ML, and            CA, USA. ACM, New York, NY, USA, 11 pages. https://doi.org/10.
                                         C-like fragments satisfy them, while the STLC instance used               1145/3843750.3843841
                                         in our experiments does not: plain STLC can violate type
                                         coverage, and we show how restricting its type universe                   1    Introduction
                                         recovers it. A tokenizer-lifting lemma carries character-level            Grammar-constrained decoding has by now entered infer-
                                         witnesses to token sequences under an explicit vocabulary-                ence infrastructure, with libraries such as Outlines [25],
                                         coverage hypothesis.                                                      DOMINO [2], and Formatron [21] which mask a model’s
                                            We validate the implementation differentially against pro-             vocabulary so that every emitted prefix extends to output
                                         duction compilers (ocamlc, cc). Across every prefix of 65                 in a regular or context-free language, giving a structural
                                         compiler-valid programs we observe zero false prunes. The                 guarantee of completability. The constraints they express are
                                         semantic oracle localizes 25/30 invalid programs mid-stream,              nonetheless weak relative to how models actually fail.
                                         against 0/30 for a syntax-only oracle, and agrees on 42/42 re-               Syntax-only constraints do not address consequential
                                         cursion probes. A twelve-model generation study, including                program-generation failures such as scope, type compatibil-
                                         a matched semantic-versus-syntactic ablation for nine mod-                ity, and declaration effects, none of which a grammar mask
                                         els, finds nonnegative observed semantic-minus-syntactic                  can express. Lifting the guarantee to semantic constraints
                                         point estimates for every model-language pair, with maxima                gives two distinct properties:
                                         of +15.2 points on STLC task correctness and +14.3 points                     1. safe pruning: no prefix with a semantically valid com-
                                         on ML validity.                                                                  pletion is rejected
                                                                                                                       2. dead-end freedom: every retained prefix still has such
                                                                                                                          a completion
                                                                                                                      The first protects the model’s valid continuations while
                                                                                                                   the second protects the decoding loop from being walked
                                         This work is licensed under a Creative Commons Attribution 4.0 Interna-   into a state where no token is admissible. They are different
                                         tional License.                                                           theorems with different hypotheses.
                                         LMPL ’26, Oakland, CA, USA
                                                                                                                      We structure this paper around the following question:
                                         © 2026 Copyright held by the owner/author(s).
                                         ACM ISBN 979-8-4007-2986-7/2026/10                                               When may a semantic prefix oracle reject an LLM
                                         https://doi.org/10.1145/3843750.3843841                                          continuation without hiding a valid program, and
LMPL ’26, October 4–9, 2026, Oakland, CA, USA                                                                  Paul Kronlund-Drouault


      how do we validate that the implementation actu-            2     The Constraint Model
      ally respects that contract?                                2.1   Grammar Specifications
   As a working example, take the finite lambda instance of       We fix an alphabet Σ and write 𝐿 ⊆ Σ∗ for a language. A
§3.2. Under its constraints, a model that has decoded let x :     prefix 𝑠 is completable for 𝐿 when 𝑠𝑠 ′ ∈ 𝐿 for some 𝑠 ′ . Prefix
Int = may still emit a digit, an open parenthesis, or any Int     parsing accepts exactly the completable prefixes of the sur-
in scope, but the token true is masked out: the annotation        face syntax. The surface parser keeps branches compatible
has fixed the demanded type and the boolean literal’s type        with the consumed input, and the semantic layer removes
is fixed too. This is where semantics is needed, since let x      branches carrying a stable contradiction. Writing 𝑅𝐺 for the
: Int = true; is a perfectly good parse in the underlying         prefixes retained by Aufbau, the guarantee proved below
context-free grammar.                                             (§2.3) is the one-sided inclusion
   Our declarative format attaches typing rules to a context-
free surface. The rules compile to a language-parametric IR             Pref (𝐿𝐺 ) ⊆ 𝑅𝐺 ,      Pref (𝐿𝐺 ) = {𝑠 | ∃𝑟 . 𝑠𝑟 ∈ 𝐿𝐺 }.
over first-order terms, pattern ascription, syntactic unifica-
tion, and finite right-bound context effects. Aufbau executes     Definition 2.1 (Semantic grammar specification). A seman-
this IR during Earley descent and rejects a path only after a     tic grammar specification (what an .auf file can represent)
stable semantic contradiction. The kernel has no built-in no-     is a tuple 𝐺 = (𝑁 ,𝑇 , 𝑃, 𝑆, Θ, T , B): nonterminals 𝑁 , termi-
tion of type, function, or arrow. Those meanings come from        nal recognizers 𝑇 , productions 𝑃, start symbol 𝑆, semantic
each grammar’s constructors and shared holes. Safe pruning        rules Θ, a partial map T : 𝑁 ⇀ Θ attaching a rule to a
is therefore a property of the oracle. Dead-end freedom is a      nonterminal, and binding identifiers B. A production for 𝑛
stronger property of particular grammars. In §2.3 we give         is a sequence 𝛼 1 [𝑏 1 ] · · · 𝛼𝑚 [𝑏𝑚 ] where each 𝛼𝑖 ∈ 𝑇 ∪ 𝑁 and
three sufficient conditions, show that the ML and C-like in-      each 𝑏𝑖 ∈ B ∪ {𝜀} names the child’s evidence for use by a
stances satisfy them, and show why the STLC instance used         rule.
in our experiments does not.                                         We reserve semantic prefix grammar for the subclass addi-
   Because a proof of the rejection rule does not rule out        tionally satisfying the three conditions of §2.3 that guarantee
implementation bugs, we also validate Aufbau differentially       witness construction. Bindings are annotations only, and do
against production compilers sharing none of our code. P7         not affect the context-free structure. Terminals are matched
then measures what the semantic layer buys over the same          through a segment interface returning a status in {Prefix,
mask with typing removed.                                         Exact, Extensible} together with a regular residual, the de-
   This paper contributes:                                        rivative of the recognizer after the consumed segment [5, 14].
                                                                  The minimal example, used throughout:
    • A semantic-prefix formalism that separates safe prun-
      ing from dead-end freedom, with a safe-pruning the-                     Id → R ([A-Za-z][A-Za-z0-9]∗ )
      orem, simple sufficient conditions for dead-end free-                Type → Id | Type ‘→’ Type | ‘(’ Type ‘)’
      dom, and a tokenizer-lifting lemma under an explicit                  Var → Id[𝑥]                               (var)
      vocabulary-coverage hypothesis (§2, §3)
                                                                           Lam → ‘𝜆’ Id[𝑎] ‘:’ Type[𝑡] ‘.’ Expr[𝑒]    (lam)
    • A language-parametric implementation (Aufbau/P7,
      with STLC, finite-lambda, core ML, C-like, and typed                 App → Expr[𝑙] Expr[𝑟 ]                      (app)
      tool-DSL instances in three surface dialects) and prefix-            Expr → Var | Lam | App
      by-prefix differential validation against ocamlc and cc:
                                                                   with one rule per annotated nonterminal, each a set of
      zero false prunes over every prefix of 65 in-fragment       ascriptions over shared holes 𝔄, 𝔅:
      valid programs, 42/42 on a recursion probe, mid-stream
      error localization at 25/30 vs. 0/30 for a syntax-only       𝑥 : 𝔄 in Γ       Γ[𝑎:𝑡] ⊢ 𝑒 : 𝔅       𝑙 : 𝔄→𝔅 𝑟 : 𝔄
                                                                              (var)                (lam)               (app)
      oracle (§3–§4.1)                                                 : 𝔄            : 𝑡 →𝔅                   : 𝔅
    • A twelve-model generation study containing a                   The app rule has no idea what a function is. Its premise
      matched semantic-versus-syntactic ablation for the          𝑙 : 𝔄 → 𝔅 is one constructor pattern: → is a constructor
      nine models that ran both arms, 3,693 graded attempts       because the grammar’s type fragment wrote it, and 𝔄, 𝔅 bind
      in total, holding parser, sampler, tokenizer bridge,        its subterms. There is no separate algebra of types, leaves
      and surface grammar fixed, with per-language va-            are regular languages, and the arrow means only what hole-
      lidity and correctness metrics reported separately,         sharing across the three rules makes it mean. The inference
      together with exploratory observations on reasoning-        notation is a front end to a small IR of term evaluation, as-
      then-constrained scheduling, rejection–uncertainty          cription, equality, context membership, scoped extension,
      association, and multi-turn tool episodes (§4.2).           and right-bound effects, and the same IR runs the ML, C,
  The artifact contains the implementation, specifications,       and tool instances with no distinguished type or function
data, and commands used for the reported measurements.            instruction.
Semantic Prefix Oracles for LLM Decoding: Contracts and Differential Validation                    LMPL ’26, October 4–9, 2026, Oakland, CA, USA


2.2   Evidence and Constraint Graphs                                          only by re-deriving the same core with different evidence.
To keep the mechanism language-parametric, semantic ev-                       Acyclicity of →0 bounds the number of rule firings attribut-
idence is represented only by terms over the grammar’s                        able to any span, so each core carries finitely many semantic
signature, with ascription for checking a term against an ex-                 refinements and context effects. Terms are finite, regular-leaf
pected pattern and first-order unification as the sole rewriting              intersection is decidable, and first-order unification termi-
mechanism [9, 18]. Context lookup, type equality, and struc-                  nates with the occurs check. Semantic pruning only removes
tural matching are all ascriptions discharged by unification.                 annotated items, so the annotated chart reaches a fixed point,
Equality 𝜏1 = 𝜏2 is 𝜏1 : 𝜏2 . Membership 𝑥 ∈ Γ is 𝑥 : 𝔄 solved                and the same procedure applied to each member of a finite
against Γ. A shape such as 𝔄 → 𝔅 is matched constructor-                      candidate set terminates.                                    □
against-constructor with each hole bound by position, with                       Zero-consumption is needed, because a unit cycle such
no decomposition step and no built-in notion of domain or                     as 𝐴 → 𝐵, 𝐵 → 𝐴 | x consumes no input while its rules
codomain.                                                                     wrap evidence on every traversal, giving one finite span un-
   Parsing a prefix yields an AST whose nodes carry, at bound                 boundedly many annotations. Productivity covers a separate
positions, evidence: a status in {Exact, Prefix, Extensible}                  failure mode, since a consuming cycle can still be unproduc-
propagated bottom-up, a type term possibly containing                         tive, as 𝑆 → x 𝑆 is. Both are decidable by least-fixed-point
holes, an exported context effect, and a binding map sending                  computation and are checked when a grammar is loaded.
each binding either to Resolved(𝜈) (the child’s evidence,                     The proposition decides whether a fixed finite continuation
once the dot has passed it) or Pending (the child is past the                 survives the semantic Earley chart. Whether an arbitrary
right frontier). A binding moves from Pending to Resolved,                    prefix has some valid suffix is a different question, and needs
never the reverse. This is the available/unavailable split                    the analysis below. Declared normalization rewrites are out-
of incremental attribute grammars [6] and the typed-hole                      side Proposition 2.2, since they need separate termination
reading of an unfilled position [13].                                         and confluence arguments.
   Rules relate evidence directly, so semantic information
                                                                              2.3   Verdicts: Safe Pruning and Dead-End Freedom
forms a graph over evidence rather than a tree. Firing a rule
emits one unification edge per premise plus a conclusion                      Definition 2.3 (Witness, denotation, verdict). A witness for
edge, and holes shared between ascriptions become equality                    a prefix 𝑠 is 𝑟 ∈ Σ∗ such that 𝑠𝑟 admits a complete parse of
edges. This is the constraint-generation reading of type infer-               the start symbol whose graph G(𝑠𝑟 ) is closed and consistent.
ence where a typing system is a set of unification constraints                The denotation D (𝑠) is the set of witnesses. The semantically
over a partial program. A vertex is frontier when it still car-               valid language 𝐿𝐺 is the set of complete inputs with an empty-
ries an incomplete-input signal (status Prefix/Extensible, or                 witness parse. The evaluator returns
a Pending binding). The graph at prefix 𝑠, written G(𝑠), is                                      
                                                                                                 
                                                                                                  Satisfied closed and consistent,
open when some edge touches a frontier vertex and closed                                         
                                                                                                 
                                                                                   eval(G(𝑠)) = Lost             stable contradiction,
when it is not open and the solver finds no contradiction. The                                   
                                                                                                  Live
                                                                                                 
parser builds and solves this graph during Earley descent                                                       otherwise.
rather than after parsing. A stable contradiction removes                     A contradiction is stable when later input cannot repair it.
that item immediately, while unresolved frontier evidence                     This includes rigid constructor clashes, regular-leaf clashes,
remains in the chart. Context effects are right-bound. Only                   occurs-check failures, and failed lookups in the fixed left
an Exact node exports a declaration into the context its right                context. Ambiguity is existential: a prefix is Lost only when
siblings see.                                                                 every compatible branch is Lost.
Proposition 2.2 (Fixed-prefix decidability). Let 𝐺 be finite                  Theorem 2.4 (Safe pruning). Aufbau never rejects a prefix
with regular terminals, and let every semantic rule compile to                that has a witness.
a finite straight-line IR program interpreted in the free first-              Proof. Every rejection is justified by a stable contradiction
order theory with the occurs check and no declared rewrites.                  on every compatible branch. Extending a branch can instan-
Compute the nullable nonterminals by least fixed point and                    tiate unresolved holes, refine regular residuals as more input
define the zero-consumption left-corner relation 𝐴 →0 𝐵: some                 is consumed, and append right-bound context effects. The
production of 𝐴 can reach an occurrence of 𝐵 after a prefix of                rejection forms above are monotone under those operations:
nullable symbols. Suppose the →0 graph restricted to nonter-                  a rigid constructor clash remains a clash, an empty regular
minals reachable from 𝑆 is acyclic, and, separately, that every               intersection cannot be restored by further refinement, an
reachable nonterminal is productive (derives some finite termi-               occurs-check failure cannot be repaired by later substitu-
nal string). Then evaluation of any finite prefix and masking                 tion, and a failed lookup in the fixed left context cannot be
over any finite candidate set are decidable.                                  repaired by declarations exported to the right. Thus a contra-
Proof (sketch). Earley parsing over a finite input has a finite               diction classified as stable persists on every extension of that
chart of item cores. Semantic elaboration can multiply items                  branch. If 𝑠 had a witness 𝑟 , the complete consistent parse
LMPL ’26, October 4–9, 2026, Oakland, CA, USA                                                               Paul Kronlund-Drouault


of 𝑠𝑟 would restrict to a compatible branch at 𝑠 that is not          The conditions are deliberately sufficient rather than a
Lost, contradicting rejection.                            □        characterization of every grammar on which Aufbau hap-
                                                                   pens to avoid dead ends. They are useful because they sep-
                                                                   arate the oracle property from the language property. Safe
   The implementation is conservative about information            pruning holds independently. Dead-end freedom follows
that is not yet fixed. In particular, prediction-time checks use   once a grammar has productive syntax, type coverage, and
only constraints already determined by the consumed prefix.        left-to-right semantic flow.
Missing information can therefore delay a rejection, but it           The examples make the boundary concrete, and the bound-
cannot create one. This matters for dead-end freedom, not          ary runs through our own instances. Our STLC instance
for safe pruning.                                                  (§3.2) does not satisfy (T): its base-type universe is unre-
   Dead-end freedom is a property of a grammar in addition         stricted, so an atomic type may have no closed inhabitant,
to the oracle. A Live prefix has not contradicted the grammar,     and the 𝜆𝑓 :𝐴→𝐵. 𝑓 ( prefix above is a prefix of that grammar.
but it may still have no completion. Plain STLC gives the          Coverage is recoverable by construction: restrict the base-
simplest example. With distinct atomic types 𝐴 and 𝐵, the          type universe to a finite set in which every base type has
prefix 𝜆𝑓 :𝐴→𝐵. 𝑓 ( demands a term of type 𝐴. If the language      a literal. The literals cover the base types, and arrow types
has no closed term of type 𝐴, the prefix is Live but has no        follow inductively, since a closed realizer 𝑒𝐵 of 𝐵 makes
witness.                                                           (𝑥:𝐴) ⇒ 𝑒𝐵 a closed realizer of 𝐴 → 𝐵. The finite-lambda
   For the typed grammars in this paper, the relevant notion       instance below uses exactly this construction. We did not
of inhabitation is simply type coverage: every type that can be    run the reported STLC experiments on that restricted in-
demanded at a reachable prefix has some finite closed term         stance. Core ML has a simpler cover because assert false
of that type. A universal inhabitant is one way to obtain          can be assigned every expression type. The C-like fragment
coverage, but it is not required. Throughout, a parser branch,     also covers every reachable expression-type demand in its
nonterminal, regular residual, or type demand is reachable         fragment: scalar types have literals, and explicit casts from
when it occurs after consuming some finite input prefix from       a scalar literal realize pointer types and the other concrete
the start symbol on a compatible branch, before that branch        expression types admitted by the grammar. The tool DSL has
becomes Lost.                                                      no comparable universal cover. With an empty context, let
                                                                   s = summarize( demands a docs value, but the grammar
Definition 2.5 (Dead-end-free grammar class). We use the           has no closed docs literal, so the prefix can remain Live
following sufficient conditions for dead-end freedom.              with no completion.
                                                                      Nothing in this argument requires the implementation to
  (P) Surface productivity. Every reachable nonterminal has        decide (P), (T), and (F) automatically. They state when the
      a finite completion, and every reachable regular resid-      stronger dead-end-free guarantee applies. The implementa-
      ual is nonempty.                                             tion itself only relies on the safe-pruning contract.
  (T) Type coverage. Every reachable type demand has a
      finite closed realizer whose construction does not in-       2.4   Worked Example
      validate the already fixed left context.
                                                                   Figure 1 illustrates the three verdicts. The complete term
  (F) Left-to-right constraint flow. A child’s semantic obliga-
                                                                   resolves 𝑥 in the fixed context and closes the graph. A pend-
      tions are determined by the parent demand, the fixed
                                                                   ing body leaves the graph open and therefore Live, without
      context, and children to its left. Later children do not
                                                                   guaranteeing a witness. The exact variable 𝑦 fails lookup
      constrain earlier ones.
                                                                   in Γ = [𝑥:int], yielding a stable contradiction that syntax
                                                                   alone cannot detect.
Theorem 2.6 (Dead-end freedom under coverage). A gram-
mar satisfying (P), (T), and (F) is dead-end free: every Live
prefix has a witness.                                              3     Aufbau, P7, and the Instances
                                                                   3.1   Architecture
Proof sketch. Complete the leftmost unfinished position re-        A language definition is lowered into Aufbau’s semantic
peatedly. Condition (P) closes purely syntactic and regular        grammar IR, productions, regular terminals, binding posi-
positions. When a typed expression is required, (F) makes          tions, compiled rule programs, context effects, with .auf as
its demanded type depend only on information already fixed         one readable front end and the API able to construct the same
to its left, and (T) supplies a finite closed term of that type.   IR directly. Aufbau executes it inside an Earley parser [7]
Repeating this process moves strictly rightward and eventu-        whose items carry the evidence and constraint graph of §2.2.
ally closes the parse. The chosen terms satisfy the demands           The entry point try_feed extends the current prefix by
under which they were inserted, so the resulting completion        a candidate string and returns the three-valued verdict. P7
is consistent.                                                □    puts this oracle in the decoding loop (Figure 2).
Semantic Prefix Oracles for LLM Decoding: Contracts and Differential Validation                                       LMPL ’26, October 4–9, 2026, Oakland, CA, USA


 𝜆𝑥:int. 𝑥     Satisfied             𝜆𝑥:int.    Live                 𝜆𝑥:int. 𝑦     Lost      by token, and composing the recognizer’s derivative across
Lam (lam) : int→int              Lam (lam) : int→ 𝔅                  Lam (lam) : int         𝑣 1, . . . , 𝑣𝑘 reaches the residual the character-level run would.
   body                                                                 body                                                                                  □
          Var (var) : int            body      body 𝑒                            Var (var)
                                               Pending
                𝑥 ↦→ int                                                          𝑦∉Γ        3.2    Language Instances
             in Γ = [𝑥:int]                                                    Γ = [𝑥:int]
                                                                                               STLC. A monomorphic simply-typed lambda calculus
                  (a)                            (b)                                (c)
                                                                                             with mandatory binder annotations, used both by the
                                                                                             oracle’s validation harnesses and as the STLC arm of the
                                                                                             generation study. Its base-type universe is unrestricted, so
Figure 1. The oracle’s evidence on three prefixes of the min-
                                                                                             this instance does not satisfy the type-coverage condition
imal grammar. Gray right-angle links show AST structure,
                                                                                             (T) of §2.3 and we make no dead-end-freedom claim for it:
colored links semantic evidence. The complete term closes
                                                                                             the 𝜆𝑓 :𝐴→𝐵. 𝑓 ( counterexample is a prefix of this grammar.
at int → int. The missing body stays Pending. The exact
                                                                                             Safe pruning applies to it exactly as to every other instance.
variable 𝑦 fails lookup in Γ = [𝑥:int], making the last prefix
Lost.                                                                                          Finite Lambda ( fun.auf). A variant of the lambda
                                                                                             calculus with modern surface syntax, let-bindings, and a
                                                          try_feed
     LLM
                         token
                                          P7                               Aufbau            base-type universe restricted to Int, Bool, and Float, each
     model                             controller                          oracle
                                                           verdict                           equipped with literals. These literals cover the base types.
                                                                                             Function types are covered inductively: if 𝑒𝐵 is a closed
    resample
                                                                                             realizer of 𝐵, then (x: A) => 𝑒𝐵 is a closed realizer of
                                                                                             𝐴 → 𝐵. Together with productive syntax and left-to-right
                     Lost                  Live               Satisfied
             exclude and resample   commit and continue    commit and finish
                                                                                             constraint flow, the instance therefore satisfies (P), (T),
                                                                                             and (F), unlike the unrestricted STLC instance used in the
                                                                                             experiments.
Figure 2. P7 constrained-decoding architecture. The
model proposes a token, P7 submits it to the Aufbau prefix                                     Core ML ( ml.auf). A monomorphic ML fragment with
oracle, and the oracle returns one of three verdicts: Lost is                                let/let rec, functions, application, integers, booleans,
excluded and resampled, Live is committed and decoding                                       comparison and arithmetic, lists (T list, cons, []),
continues, Satisfied completes the derivation.                                               if/then/else, and assert false. The concrete syntax is
                                                                                             a strict OCaml subset, so every accepted program feeds
   Two properties of the loop matter below. The mask never                                   ocamlc with no translation. This makes differential prefix
forces completion: the model’s own stop tokens stay admissi-                                 validation possible (§4.1). The axiom assert false : 𝔄 is
ble mid-derivation, so §4.2 counts abandonments rather than                                  a universal expression inhabitant, so every reachable ML
hiding them. The mask prunes rather than repairs: given a                                    expression-type demand is covered. Checking-mode let
model with no useful solution, it can turn free-form garbage                                 rec is incremental because its signature is fixed before the
into well-formed garbage that still fails grading.                                           body streams.
    Tokenizer lifting. P7 feeds Aufbau tokens, not charac-                                      A C-like fragment ( c.auf). A typed C-like fragment
ters, soÐthe guarantees above must cross that boundary. Write                                whose accepted output is graded by cc -fsyntax-only:
Σ𝐺 = 𝑅 ∈𝑇 alph(𝑅) for the union of the recognizers’ alpha-                                   declarations and assignment, typed functions and calls, if,
bets, ℓ : 𝑉 → Σ𝐺∗ for the exact spelling map on ordinary text                                while, and for, arithmetic and comparison over int, float,
tokens of the vocabulary 𝑉 (control tokens and eos follow                                    and char, pointers with address-of and dereference, and
the completion policy above), and 𝐿𝑉 = {ℓ (𝑣) | 𝑣 ∈ 𝑉 }.                                     explicit casts.
    The coverage hypothesis Σ𝐺 ⊆ 𝐿𝑉∗ gives Σ𝐺∗ ⊆ 𝐿𝑉∗ , since                                    The fragment threads each function’s declared return type
  ∗
𝐿𝑉 is closed under concatenation.                                                            through an ambient context entry and checks every return
Lemma 3.1 (Tokenizer lifting). Under exact spelling (the or-                                 against it, admitting a bare return; only in a void func-
acle consumes, byte-for-byte, the text the model conditions on)                              tion.1 We still call it C-like deliberately: it does not prove
and coverage, every character-level witness factors into a finite                            that every path through a non-void function returns, does
token sequence, and regular derivatives carry the oracle’s state                             not constrain the operand of a cast or of address-of, and
across a token ending inside a terminal recognizer. Character-                               its demanded-type universe includes void and unbounded
level witness existence therefore lifts to token-sequence reacha-
bility.                                                                                      1 The return-type check postdates the generation study of §4.2, which ran on

                                                                                             the earlier version of c.auf without it. The reported C generation numbers
Proof. Coverage factors the witness into a concatenation of                                  are therefore for that earlier grammar and rerunning them is future work.
spellings ℓ (𝑣 1 ) · · · ℓ (𝑣𝑘 ), exactly the string P7 submits token                        §4.2 repeats this caveat where the numbers appear.
LMPL ’26, October 4–9, 2026, Oakland, CA, USA                                                               Paul Kronlund-Drouault


pointer depth, so Aufbau-accepted programs are not guaran-            Being invented, it has no pretraining prior and no external
teed to be accepted, or accepted without diagnostics, by a C       compiler, so an episode is graded by the value its return eval-
compiler.                                                          uates to against the registry’s real implementations rather
   For dead-end freedom, the relevant point is narrower than       than by well-typedness. Each turn is one constrained step.
full C validity. Every reachable expression-type demand in         The binding it introduces is pushed into Γ, so turn 𝑛+1 de-
this fragment has a closed realization: scalar types have lit-     codes under the types established by turns 1..𝑛, threading
erals, while explicit casts from a scalar literal realize the      the constraint graph of §2.2 across the episode.
pointer types admitted by the grammar. Together with the              Three dialects share one type discipline: a C-like let syn-
fragment’s productive statement forms and left-to-right dec-       tax (tool.auf), S-expressions (tool_sexpr.auf), and XML
laration flow, this gives the coverage used in Theorem 2.6.        elements (tool_xml.auf). Only the surface varies, so the
The differential harness of §4.1 separately checks compati-        dialect axis separates semantic discipline from syntax priors
bility with cc.                                                    and tokenizer alignment.
   Two design points carry the semantics. A two-sort type             The dialects also show why registry reachability is
discipline keeps the concrete sort CType (scalars and point-       weaker than type coverage. With an empty context, let
ers, what a cast or declaration can spell) distinct from the       s = summarize( is Live with no completion because the
internal signature sort that types functions. The latter is un-    demanded docs argument has no literal form and no binding
reachable from concrete syntax, so no source expression can        supplies one. We therefore make no dead-end-freedom claim
demand a function-shaped type. And definition-before-use           for the tool DSLs. A 51-case harness checks the checker
holds at translation-unit granularity: a call is checked against   given a witness by injecting a binding of the demanded
a signature already exported by an earlier definition’s right-     type at each demanding argument position and confirming
bound effect, which a left-to-right oracle handles without         acceptance.
lookahead because the definition precedes the call in the
token stream.                                                      4     Empirical Findings
   Declarative boundary: self-recursion. Inference-mode            The evidence comes in two tiers with different epistemic
recursion cannot be declared in this fragment. let rec with-       status, and we keep them apart.
out an annotation was implemented and dropped after some
                                                                     Tier 1 (§4.1). tests the oracle: CPU-only, deterministic,
empirical failure evidence. The problem is that the recursive
                                                                   regenerable byte-for-byte by a reviewer with no GPU.
call races the still-streaming parameter list to resolve the
signature metavariable, and an early unification can commit          Tier 2 (§4.2). measures what the oracle buys in generation:
it to a shape the header later contradicts, producing a false      GPU runs over open models, single greedy attempts, graded
prune rather than a real error. Checking-mode recursion,           by per-language metrics that are deliberately not pooled into
whose signature is exact before the body opens, has no such        one accuracy (§4.2 defines each).
race, so the declarable fragment admits checking-mode pro-
gram recursion only and inference-mode program recursion           4.1   Differential Prefix Validation
is excluded as a restriction of the fragment. It could theoreti-
                                                                   The oracle’s verdicts are compared prefix by prefix against a
cally be implemented but would require dropping the level
                                                                   production compiler that shares none of our code: ocamlc for
of constraints which isn’t very interesting here.
                                                                   the ML instance and cc for the C instance. These are finite,
   This important limitation was found by our test system
                                                                   hand-selected test cohorts, so the results validate rather than
probing ocamlc against the oracle. Indeed, some experiments
                                                                   certify. The harness extends mechanically.
on recursion corners surfaced the discrepancy (§4.1). The in-
                                                                      Safe pruning (Theorem 2.4) applies to every instance.
strumentation that rejects the model’s tokens is what caught
                                                                   The cohorts below add finite external evidence for the ML
the grammar author. This establishes the importance of our
                                                                   and C implementations, the two instances with production-
differential certification approach for implementation cor-
                                                                   compiler comparators. Differential testing can expose
rectness.
                                                                   implementation bugs, but finite cohorts are not an exhaus-
   The agentic tool DSL dialects. The third instance exer-         tive correctness proof. Theorem 2.4 is in any case a paper
cises the semantic layer as an agent harness. Constrained          proof of the rejection discipline, and the shipped engine is
decoding is usually evaluated on single-shot synthesis, but        an optimized realization of it: these cohorts check selected
multi-turn tool use, where the typed context grows as the          end-to-end compatibility properties rather than establishing
episode runs, is the natural application for a typed oracle.       that the optimized engine computes the theorem’s verdicts
tool.auf is an invented typed pipeline language over a fixed       at every token boundary. A slow reference evaluator built
registry (search: string→docs, summarize: docs→string,             directly from the formal rules, enabling prefix-by-prefix
count: docs→int, format: int→string) with let-sequencing           correspondence testing against the shipped engine, is future
and return.                                                        work.
Semantic Prefix Oracles for LLM Decoding: Contracts and Differential Validation                              LMPL ’26, October 4–9, 2026, Oakland, CA, USA


                                                                                            • Constrained Mixed: free reasoning, then a con-
   Median validation time (ms)

                                  102       Arithmetic flat sum
                                                                                              strained emission block, the interleaved schedule of
                                            Arithmetic nested
                                            C declarations
                                                                                              CRANE [1].
                                  101       STLC application chain                          • Unconstrained Thinking: a budgeted chain-of-
                                                                                              thought phase, then a free answer [24].
                                                                                            • Syntactic Only: the same mask with the typing rules
                                  100                                                         stripped, our within-framework ablation.
                                    100                 101                     102
                                                                                          Three models did not run Syntactic Only (Qwen3.6-
                                                                                        27B, gemma-4-26b, gpt-oss-20b), so pooled comparisons
                                                     Expression size (tokens)
                                                                                        are matched over the models that ran both modes being
                                                                                        compared. Decoding is greedy at temperature 0, one at-
Figure 3. Median validation time vs. expression size on four
                                                                                        tempt, fixed seed. Intervals are Wilson 95% and measure
stress families (log–log). Growth is smooth and mildly su-
                                                                                        cohort uncertainty on hand-selected tasks, not population
perlinear (log–log slopes ≈1.1–1.4).
                                                                                        sampling.
                                                                                          Grading is per-language and deliberately heterogeneous,
                                                                                        and we do not pool it into one accuracy:
   False prunes. Over the 65 in-fragment valid programs of                                  • STLC: Aufbau supplies the decoding oracle and an
the cohort (40 ML, 25 C), the oracle was evaluated at every                                   independent handwritten validator checks the output
prefix and never reported Lost: 0/40 on ML and 0/25 on                                        type and 𝛽/𝛼-equivalence against the reference.
C, with Wilson 95% upper bounds of 8.8% and 13.3% (5.6%                                     • tool: the executed return value against the registry’s
pooled). The bound is honest about cohort size, and extension                                 real implementations. Behavioral.
is mechanical: add programs, rerun, diff every prefix.                                      • ML: an output counts as valid only when Aufbau ac-
   The recursion probe. 42 programs probing let rec corners                                   cepts the declared type and ocamlc independently ac-
agree with ocamlc in 42/42 cases (Wilson 95% CI [0.92, 1.00]).                                cepts the program, and this program has the required
The probe exists because recursion is where our fragment                                      type.
boundary was wrong once (§3.2): the harness that found the                                  • C: an output counts as valid only when Aufbau and
unsoundness now pins the repaired boundary.                                                   cc -fsyntax-only independently accept it.
   Prune lead time. On 30 invalid programs, the semantic
                                                                                           The divergence idiom that gives ML its coverage also in-
oracle reports Lost mid-stream in 25 cases (12/17 on ML,
                                                                                        habits any demanded type at grading time: of 259 passing
13/13 on C), where a syntax-only oracle catches 0 before end
                                                                                        ML records, 36 contain assert false (9 of the 52 passing
of input. In the caught cases the Lost position trails the start
                                                                                        direct-mask records). ocamlc’s independent check on the
of the compiler’s diagnostic span by 2.3 characters pooled
                                                                                        declared type is what keeps the ML criterion independent of
(2.5 on ML, 2.1 on C).
                                                                                        the oracle.
   Oracle cost. Median whole-input try_feed time on four
                                                                                           ML and C passes are therefore compiler-validated validity
synthetic stress families grows smoothly and mildly super-
                                                                                        metrics rather than behavioral task-correctness metrics, and
linearly with expression size, at log–log slopes of roughly
                                                                                        we reserve behavioral claims for STLC and tool. Each task
1.1–1.4 (Figure 3). The largest inputs, 450-token C declaration
                                                                                        is specified as a TOML file (prompt, initial prefix, reference
sequences and 65-application STLC chains, the adversarial
                                                                                        program, resolution mode).
case for chart size, stay under ∼130 ms.
   The measurement is model-free and CPU-only, on a six-                                   Per-effect decomposition. Gains are heterogeneous
core laptop CPU.                                                                        across model classes.
                                                                                           Across the nine models that ran both ablation arms, every
4.2 Constrained Generation                                                              observed semantic-minus-syntactic model–language point
   Setup. We run twelve open models with full logit access:                             estimate was nonnegative. Constraint can repair weak and
Qwen3.5 at 2B, 4B, and 9B in instruct and base variants,                                base models while taxing fluent ones: Qwen3.5-2B-Base
Qwen3.5-0.8B (instruct only), Qwen3.6-27B, Phi-4-mini,                                  rises from 0% unconstrained to 50% in mixed mode, while
gpt-oss-20b, gemma-4-26b, and Pythia-1.4B [3] as a no-                                  Qwen3.5-9B and Qwen3.6-27B both lose ground under the
instruction floor. The single-shot corpus is 52 tasks (33 STLC,                         same mask.
14 core ML, 5 C). The agentic corpus is tool episodes in three                             Mixed mode avoids the cost by confining the mask to a late
dialects. Each attempt runs in one of five decoding modes:                              emission block, tracking full chain-of-thought within a few
                                                                                        points while emitting 28–36 tokens instead of 1,100–2,000.
                                 • Unconstrained: free decoding, no mask.
                                 • Constrained Direct: the semantic mask on every to-     The semantic layer over syntax. The ablation isolates
                                   ken.                                                 what the typing rules add over a pure CFG mask, holding
LMPL ’26, October 4–9, 2026, Oakland, CA, USA                                                                                                                                       Paul Kronlund-Drouault
  semantic − syntactic (pp)
                                                                                                                                           Observable final outcomes across decoding modes
                              15                                                                                                           100

                              10
                                                                                                                                            80




                                                                                                                      Share of tasks (%)
                               5
                                                                                                                                            60
                               0
                                        a        8B
                                     thi      -0.       -2B     -4B     -9B     i-4        -B        -B        -B                           40
                                   Py                 Qw      Qw      Qw      Ph        -2B      -4B       -9B
                                            Qw                                        Qw      Qw        Qw

                                                                      STLC         ML                                                       20


Figure 4. Per-model, per-language semantic-minus-                                                                                            0
                                                                                                                                                 Uncons.      Cons.         Un. Think      Cons. Mix.
syntactic difference in percentage points. STLC and ML are
shown separately. C is omitted because every matched C                                                                                                     satisfied/pass        lost at stop
difference is zero.                                                                                                                                         live at stop        satisfied/fail


                                                                                                                    Figure 5. Observable final outcomes across 619 tasks and
parser, sampler, tokenizer bridge, and grammar fixed. This                                                          four decoding modes. Lost at stop: final verdict Lost. Live
is the generation comparison the paper is about. The largest                                                        at stop: final verdict Live without a closed derivation. Sat-
lifts by language are +15.2 points on STLC task correctness                                                         isfied/pass and /fail split closed outputs by the grader of
(Phi-4-mini) and +14.3 on ML validity (Qwen3.5-4B, Phi-                                                             §4.2. The labels are observable final states, with no inference
4-mini, Qwen3.5-9B-Base), while every matched C cell is                                                             about suffix existence, and the constrained arms carry no
exactly 0.                                                                                                          lost-at-stop mass and more live-at-stop mass.
    Aggregated within each language over the matched mod-
els, the semantic layer adds +7.1 points on ML (32.5% against                                                       4.3                    Exploratory Observations
25.4%), +2.0 on STLC (40.4% against 38.4%), and exactly 0 on
C (next paragraph). The ML figure carries the caveat that                                                           Figure 6 shows the two rejection-telemetry observations.
ML’s validity grader shares the oracle’s type system.                                                                  Rejection is associated with model uncertainty. Where
    Syntax-only constraining can itself hurt: pooled over mod-                                                      the mask rejected the model’s first choice, pre-mask entropy
els it sits below unconstrained on STLC (38.4% against 44.4%)                                                       is markedly higher than at accepted steps, at every scale of
and ML (25.4% against 30.2%), fighting the model’s prior                                                            the Qwen instruct ladder: 0.87 against 1.71 bits at 0.8B, 0.94
with no semantic information to spend. That replicates, in-                                                         against 1.67 at 2B, 0.53 against 1.06 at 4B, 0.37 against 1.28 at
side our own stack, the degradation CRANE [1] reports for                                                           9B, 0.22 against 0.81 at 27B, and 2.33 against 5.51 on gpt-oss-
constrain-from-the-first-token and the underperformance of                                                          20b (Figure 6a). This is an association in single greedy runs,
grammar-only decoding in ChopChop’s tables [12].                                                                    not a predictive evaluation, but it matches CRANE’s account
                                                                                                                    of when constraint hurts [1]: rejections concentrate at un-
   Where constraint helps, and a negative result. On the
                                                                                                                    certain steps and are rare at confident ones. Retry pressure
C-like fragment the direct mask lifts pooled validity from
                                                                                                                    broadly falls with capability on that ladder (6.1% of steps at
53% to 80% (+27 points, matched over models that ran all
                                                                                                                    0.8B, 2.1% at 27B, 13.9% on 2B-Base) but not across families,
five modes), but the syntax-only mask reaches the same 80%.
                                                                                                                    gpt-oss-20b retries 32.9%, while Pythia, the weakest model,
The ablation attributes none of the C gain to the typing rules,
                                                                                                                    retries only 6.8%, so this is not a model ranking.
and the difference is not significant. Format control alone
explains the lift, and we report that as a negative result rather                                                      How strongly does the language constrain decoding?
than crediting definition-before-use or pointer typing. These                                                       The rejection signal has a model-free counterpart: at each
C cells were produced before the return-type check of §3.2                                                          position of a valid program, how many candidate tokens does
was added to c.auf, so they describe the earlier grammar.                                                           the oracle admit?
The added check tightens the semantic arm only, and rerun-                                                             We measure the mean log2 admissible-set size over a
ning the arm is future work. The semantic layer’s language-                                                         corpus-derived token alphabet: a Hartley-style branching
level gain concentrates on ML instead (+7.1 pooled), where                                                          measure under a uniform assumption, not Shannon entropy,
inference-style typing constrains many surface choices. On                                                          conditioned on the evaluated corpus (14 ML programs, 209
STLC the direct mask is slightly negative pooled (44% to 40%)                                                       positions, 42-token alphabet, and 5 C programs, 83 posi-
while mixed mode reaches 55%: those tasks are search-heavy                                                          tions). Over the ML corpus the semantic oracle admits 16.8
rather than surface-heavy, so reasoning, not masking, binds.                                                        candidate tokens per position on average against 26.3 for
   The tool dialects are the agentic case of §4.3.                                                                  its syntactic twin, removing 9.5 candidates per position and
Semantic Prefix Oracles for LLM Decoding: Contracts and Differential Validation                                                   LMPL ’26, October 4–9, 2026, Oakland, CA, USA


                                    (a) model uncertainty: entropy where the mask fires                                                    thinking   mixed
          pre-mask entropy (bits)   6
                                               token accepted                                                             Generation cost             Task performance
                                    5
                                               token rejected (retried)
                                    4                                                                    Q3.5 0.8B
                                    3
                                                                                                          Q3.5 2B
                                    2
                                    1                                                                     Q3.5 4B
                                    0
                                                                                                          Q3.5 9B
                                            0.8B     2B         4B         9B      27B   gpt-oss
                                                                                                         Q3.6 27B

                          (b) grammar branching: tokens the oracle admits / position                   Phi-4-mini

                                                                                                       gpt-oss-20b
     C semantic
                                                                                                                     30     100   300   1,000 3,000   25      50      75   100
       C syntax
                                                                                                                     mean generated tokens                 pass rate (%)
    ML semantic

     ML syntax
                                                                                                      Figure 7. Thinking vs. mixed mode: mean generated tokens
                                        0            25               50            75         100    on a log scale (left) and descriptive task-mix pass rate (right).
                                                          share of positions (%)
                                                                                                      Each row is one model and the line connects thinking (open
                                        forced (1)      tight (2–4)        open (5–16)   wide (17+)   purple) to mixed (filled orange). Mixed greatly reduces token
                                                                                                      count for the five Qwen rows (roughly 11× to 60×), but not
Figure 6. (a) Mean pre-mask entropy at steps where the                                                for Phi-4-mini (0.73×, i.e. mixed emits more tokens) or gpt-
sampler’s first choice was accepted versus rejected (retried),                                        oss-20b (1.14×). Pass-rate changes are heterogeneous across
per model, direct-mask arm: rejection is associated with the                                          rows.
model’s uncertain steps. (b) Share of positions at which the
oracle admits one candidate token (forced), a few (tight), or
many, semantic oracle against syntactic-only (14 ML / 5 C                                             optimize grammar-aligned masking to near-zero overhead,
programs).                                                                                            and subword alignment has a clean automaton treat-
                                                                                                      ment [15]. All decide membership in a fixed context-free
                                                                                                      or regular surface language. None carries the context-
raising the share of forced positions, where exactly one can-                                         dependent state, such as scope, types, and declaration effects,
didate is legal, from 9% to 13% (Figure 6b). On C it admits                                           on which models actually fail. Our syntactic layer uses the
7.1 against 11.4. The typing layer thus closes roughly a third                                        same Earley machinery. The contribution is the semantic
of the syntactic branching without ever rejecting the next                                            layer above it and the contract analysis that survives the lift.
gold token in the valid-corpus walk, and the measurement
is model-free.                                                                                           Semantic constraints. ChopChop [12] develops the
                                                                                                      general theory of semantic pruning for LLM decoding,
   Agent episodes. Each turn decodes one registry step un-                                            casting admissibility as a realizability problem and stating
der the types established by prior turns, and episodes are                                            soundness and completeness (their §3.4) relative to prop-
graded by returned value. The comparison is unpaired (per-                                            erties of the pruner the user programs: soundness needs
cell counts of 8 to 51), so we report direction only. Con-                                            an under-approximate or consistent checker, completeness
strained Qwen3.5-4B-Base completes 57% of episodes (8/14)                                             an over-approximate and consistent one. For type safety
against 22% (4/18) unconstrained, while the fluent 4B is level                                        they show no checker can be both, so their type pruner is
(69% against 71%). Rates vary with surface form at least                                              over-approximate and consistent only to type depth three.
as much as with constraint: the fluent 4B reaches 88% on S-                                           We read their framework as the general setting our work
expressions against 50% on XML under the same typing rules.                                           instantiates.
Several off-ladder models complete no episodes in either arm,                                            We use a declarative class with a context-free surface
and a paired design with matched coverage is future work.                                             and decidable first-order semantic premises. Safe pruning
                                                                                                      follows from stable contradictions. Dead-end freedom is a
5     Related Work                                                                                    separate grammar property for which we give sufficient pro-
  Syntactic constrained decoding. Outlines compiles reg-                                              ductivity, type-coverage, and left-to-right-flow conditions
ular constraints to automata over the token vocabulary [25].                                          (Theorem 2.6). The declarative route also gives a direct vali-
PICARD prunes beam candidates by incremental pars-                                                    dation path: instances that check real languages can be tested
ing [19], SynCode [22], Formatron [21], and DOMINO [2]                                                prefix by prefix against production compilers (§4.1).
LMPL ’26, October 4–9, 2026, Oakland, CA, USA                                                                Paul Kronlund-Drouault


   Mündler et al. [11] demonstrate type-constrained decod-          recovery maximizes tolerance, pruning maximizes rejection,
ing for TypeScript with an incremental checker engineered           and both need the same incremental frontier.
for that language and evaluated at scale, a stronger per-
language result than ours on its own territory. Our ML in-          6   Discussion and Limitations
stance is a smaller monomorphic fragment, but comes from
                                                                       Formal limitations. The safe-pruning proof is a paper
a declarative definition, and the same definition language
                                                                    proof of Aufbau’s rejection discipline, not a mechanized
yields the C-like fragment and the tool DSL with no new
                                                                    proof of the code. Differential validation exercises the
pruner code. IterGen [23] backtracks over partial generations
                                                                    shipped implementation on finite cohorts, so implementa-
to enforce per-symbol constraints and Synchromesh [17] en-
                                                                    tion bugs outside those cohorts remain possible. Dead-end
forces per-domain checks. Neither analyzes the two prefix
                                                                    freedom is proved only for grammars satisfying the sufficient
contracts separately.
                                                                    conditions of §2.3. We establish those conditions directly for
   Tractable control via distillation into a tractable model [27]
                                                                    the finite-lambda, core ML, and C-like fragments. We do
enforces constraints by construction rather than by pruning,
                                                                    not claim them for the tool DSLs, nor for the experimental
a complementary route.
                                                                    STLC instance, whose unrestricted base-type universe
   Grammar formalisms. The formalism assembles classi-              defeats type coverage. The implementation does not attempt
cal parts: attribute grammars with synthesized and inherited        to infer this classification automatically. Token-sequence
attributes [8], definite-clause grammars, which showed uni-         reachability is proved under exact spelling and the stated
fication against a logic program’s terms can carry a gram-          vocabulary-coverage hypothesis. Bounded proposal search
mar’s semantics [16], and unification-based grammar gener-          additionally needs exhaustive masking, a deterministic
ally [20].                                                          fallback, or a separate sampler-fairness assumption which is
   Semantic grammar specifications restrict these ideas to          assumed. Nothing is mechanized.
first-order terms, syntactic unification, and right-bound ef-
fects so that prefix verdicts are decidable and the pruning            Empirical limitations. The language metrics are het-
contract is analyzable. Condition (F) of §2.3 is the correspond-    erogeneous: ML and C measure compiler-validated validity,
ing left-to-right restriction on a prefix parser.                   STLC and tool tasks behavior. Generation uses one greedy
                                                                    attempt per task, the validation corpora are small and hand-
   Differential testing. Validating a checker against an in-
                                                                    selected, and the token-count and tool-episode comparisons
dependent implementation is differential testing in McKee-
                                                                    are exploratory rather than causal. The C generation cells
man’s sense [10], and its randomized form found hundreds
                                                                    predate the return-type check now in c.auf (§3.2).
of bugs in production C compilers [26]. Our variant tests
prefix behavior: the compiler grades whole programs, the
oracle grades every prefix, and the harness checks the two          7   Conclusion
never disagree in the direction that matters for decoding.          A semantic prefix oracle owes the decoder two contracts,
                                                                    safe pruning and dead-end freedom. Aufbau provides safe
   Reasoning and constraints. CRANE [1] establishes that
                                                                    pruning by rejecting only stable semantic contradictions.
constrained and unconstrained decoding are usefully inter-
                                                                    Dead-end freedom is separate. We give three sufficient gram-
leaved, reasoning outside the constrained block, the answer
                                                                    mar conditions, surface productivity, type coverage, and left-
inside it, and explains why constraining from the first token
                                                                    to-right constraint flow, and show how they separate the
degrades reasoning. Our mixed mode is that architecture
                                                                    covered finite-lambda, ML, and C-like fragments from the un-
with a semantic rather than syntactic block, and the teleme-
                                                                    covered experimental STLC and tool instances. A tokenizer-
try of §4.3 agrees with its account: rejection lands on exactly
                                                                    lifting lemma carries these guarantees from characters to
the uncertain steps. SynCode [22] reports the syntactic ver-
                                                                    token sequences under an explicit vocabulary-coverage hy-
sion.
                                                                    pothesis. Differential validation against production com-
   Editors, holes, incremental typing. Typing incomplete            pilers shows zero false prunes across every prefix of 65
programs is an editor-services problem before it is a decod-        compiler-valid programs, and 25/30 invalid programs caught
ing problem. Hazel gives incomplete programs a semantics            mid-stream where a syntax-only oracle catches none. These
in which the unfilled position is a first-class typed hole [13].    are finite compatibility results for the shipped engine, not
Our Pending binding is that object read through a parser,           an exhaustive correctness proof. In generation the matched
though Live is weaker than Hazel’s typing, saying only that         ablation attributes positive observed lift to the typing rules
no stable contradiction has appeared (§2.3). Incremental at-        on ML, while every matched C difference was zero, which
tribute evaluation with available/unavailable attributes goes       format control alone can explain. The next steps are behav-
back to Demers, Reps, and Teitelbaum [6]. Merlin [4] is the         ioral ML and C grading, generation experiments on the cov-
engineering dual, recovering from broken text to keep ser-          ered finite-lambda instance, a matched mixed-mode rerun,
vices alive where we prune extensions of well-typed prefixes:       broader differential corpora, and mechanization.
Semantic Prefix Oracles for LLM Decoding: Contracts and Differential Validation                        LMPL ’26, October 4–9, 2026, Oakland, CA, USA


References                                                                         42nd International Conference on Machine Learning (Proceedings of
 [1] Debangshu Banerjee, Tarun Suresh, Shubham Ugare, Sasa Misailovic,             Machine Learning Research, Vol. 267). PMLR, 48262–48275. https:
     and Gagandeep Singh. 2025. CRANE: Reasoning with Constrained                  //proceedings.mlr.press/v267/park25l.html
     LLM Generation. In Proceedings of the 42nd International Conference on   [16] Fernando C. N. Pereira and David H. D. Warren. 1980. Definite Clause
     Machine Learning (Proceedings of Machine Learning Research, Vol. 267).        Grammars for Language Analysis—A Survey of the Formalism and a
                                                                                   Comparison with Augmented Transition Networks. Artificial Intelli-
     PMLR, 2836–2857. https://proceedings.mlr.press/v267/banerjee25a.
                                                                                   gence 13, 3 (1980), 231–278. doi:10.1016/0004-3702(80)90003-X
     html
                                                                              [17] Gabriel Poesia, Alex Polozov, Vu Le, Ashish Tiwari, Gustavo Soares,
 [2] Luca Beurer-Kellner, Marc Fischer, and Martin Vechev. 2024. Guiding
                                                                                   Christopher Meek, and Sumit Gulwani. 2022. Synchromesh: Reliable
     LLMs The Right Way: Fast, Non-Invasive Constrained Generation. In
                                                                                   Code Generation from Pre-Trained Language Models. In International
     Proceedings of the 41st International Conference on Machine Learning
                                                                                   Conference on Learning Representations. https://openreview.net/forum?
     (Proceedings of Machine Learning Research, Vol. 235). PMLR, 3658–3673.
                                                                                   id=KmtVD97J43e
     https://proceedings.mlr.press/v235/beurer-kellner24a.html
                                                                              [18] John Alan Robinson. 1965. A Machine-Oriented Logic Based on the
 [3] Stella Biderman, Hailey Schoelkopf, Quentin Gregory Anthony, Herbie
                                                                                   Resolution Principle. J. ACM 12, 1 (1965), 23–41. doi:10.1145/321250.
     Bradley, Kyle O’Brien, Eric Hallahan, Mohammad Aflah Khan, Shiv-
                                                                                   321253
     anshu Purohit, Usvsn Sai Prashanth, Edward Raff, Aviya Skowron,
                                                                              [19] Torsten Scholak, Nathan Schucher, and Dzmitry Bahdanau. 2021. PI-
     Lintang Sutawika, and Oskar Van Der Wal. 2023. Pythia: A Suite for
                                                                                   CARD: Parsing Incrementally for Constrained Auto-Regressive Decod-
     Analyzing Large Language Models Across Training and Scaling. In
                                                                                   ing from Language Models. In Proceedings of the 2021 Conference on Em-
     Proceedings of the 40th International Conference on Machine Learning
                                                                                   pirical Methods in Natural Language Processing. Association for Compu-
     (Proceedings of Machine Learning Research, Vol. 202). PMLR, 2397–2430.
                                                                                   tational Linguistics, 9895–9901. doi:10.18653/v1/2021.emnlp-main.779
     https://proceedings.mlr.press/v202/biderman23a.html
                                                                              [20] Stuart M. Shieber. 1986. An Introduction to Unification-Based Ap-
 [4] Frédéric Bour, Thomas Refis, and Gabriel Scherer. 2018. Merlin: A
                                                                                   proaches to Grammar. Number 4 in CSLI Lecture Notes. CSLI Publica-
     Language Server for OCaml (Experience Report). Proceedings of the
                                                                                   tions, Stanford, CA.
     ACM on Programming Languages 2, ICFP, Article 103 (2018), 15 pages.
                                                                              [21] Xintong Sun, Chi Wei, Minghao Tian, and Shiwen Ni. 2025. Earley-
     doi:10.1145/3236798
                                                                                   Driven Dynamic Pruning for Efficient Structured Decoding. In Pro-
 [5] Janusz A. Brzozowski. 1964. Derivatives of Regular Expressions. J.
                                                                                   ceedings of the 42nd International Conference on Machine Learning (Pro-
     ACM 11, 4 (1964), 481–494. doi:10.1145/321239.321249
                                                                                   ceedings of Machine Learning Research, Vol. 267). PMLR, 57773–57789.
 [6] Alan J. Demers, Thomas Reps, and Tim Teitelbaum. 1981. Incremen-
                                                                                   https://proceedings.mlr.press/v267/sun25v.html
     tal Evaluation for Attribute Grammars with Application to Syntax-
                                                                              [22] Shubham Ugare, Tarun Suresh, Hangoo Kang, Sasa Misailovic, and
     Directed Editors. In Proceedings of the 8th ACM SIGPLAN-SIGACT
                                                                                   Gagandeep Singh. 2025. SynCode: LLM Generation with Grammar
     Symposium on Principles of Programming Languages. ACM, 105–116.
                                                                                   Augmentation. Transactions on Machine Learning Research (2025).
     doi:10.1145/567532.567544
                                                                                   https://openreview.net/forum?id=HiUZtgAPoH
 [7] Jay Earley. 1970. An Efficient Context-Free Parsing Algorithm. Com-
                                                                              [23] Shubham Dipak Ugare, Rohan Gumaste, Tarun Suresh, Gagandeep
     mun. ACM 13, 2 (1970), 94–102. doi:10.1145/362007.362035
                                                                                   Singh, and Sasa Misailovic. 2025. IterGen: Iterative Semantic-Aware
 [8] Donald E. Knuth. 1968. Semantics of Context-Free Languages. Mathe-
                                                                                   Structured LLM Generation with Backtracking. In The Thirteenth Inter-
     matical Systems Theory 2, 2 (1968), 127–145. doi:10.1007/BF01692511
                                                                                   national Conference on Learning Representations. https://openreview.
 [9] Alberto Martelli and Ugo Montanari. 1982. An Efficient Unification
                                                                                   net/forum?id=ac93gRzxxV
     Algorithm. ACM Transactions on Programming Languages and Systems
                                                                              [24] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma,
     4, 2 (1982), 258–282. doi:10.1145/357162.357169
                                                                                   Brian Ichter, Fei Xia, Ed Chi, Quoc V. Le, and Denny Zhou.
[10] William M. McKeeman. 1998. Differential Testing for Software. Digital
                                                                                   2022. Chain-of-Thought Prompting Elicits Reasoning in Large
     Technical Journal 10, 1 (1998), 100–107.
                                                                                   Language Models. In Advances in Neural Information Process-
[11] Niels Mündler, Jingxuan He, Hao Wang, Koushik Sen, Dawn Song,
                                                                                   ing Systems, Vol. 35. Curran Associates, Inc., 24824–24837.
     and Martin Vechev. 2025. Type-Constrained Code Generation with
                                                                                   https://proceedings.neurips.cc/paper_files/paper/2022/hash/
     Language Models. Proceedings of the ACM on Programming Languages
                                                                                   9d5609613524ecf4f15af0f7b31abca4-Abstract-Conference.html
     9, PLDI (2025), 601–626. doi:10.1145/3729274
                                                                              [25] Brandon T. Willard and Rémi Louf. 2023. Efficient Guided Generation
[12] Shaan Nagy, Timothy Zhou, Nadia Polikarpova, and Loris D’Antoni.
                                                                                   for Large Language Models. arXiv:2307.09702 [cs.CL] doi:10.48550/
     2026. ChopChop: A Programmable Framework for Semantically Con-
                                                                                   arXiv.2307.09702
     straining the Output of Language Models. Proceedings of the ACM
                                                                              [26] Xuejun Yang, Yang Chen, Eric Eide, and John Regehr. 2011. Find-
     on Programming Languages 10, POPL (2026), 1905–1932. doi:10.1145/
                                                                                   ing and Understanding Bugs in C Compilers. In Proceedings of the
     3776708
                                                                                   32nd ACM SIGPLAN Conference on Programming Language Design and
[13] Cyrus Omar, Ian Voysey, Michael Hilton, Jonathan Aldrich, and
                                                                                   Implementation. ACM, 283–294. doi:10.1145/1993498.1993532
     Matthew A. Hammer. 2017. Hazelnut: A Bidirectionally Typed
                                                                              [27] Honghua Zhang, Meihua Dang, Nanyun Peng, and Guy Van
     Structure Editor Calculus. In Proceedings of the 44th ACM SIGPLAN
                                                                                   Den Broeck. 2023. Tractable Control for Autoregressive Language Gen-
     Symposium on Principles of Programming Languages. ACM, 86–99.
                                                                                   eration. In Proceedings of the 40th International Conference on Machine
     doi:10.1145/3009837.3009900
                                                                                   Learning (Proceedings of Machine Learning Research, Vol. 202). PMLR,
[14] Scott Owens, John Reppy, and Aaron Turon. 2009. Regular-Expression
                                                                                   40932–40945. https://proceedings.mlr.press/v202/zhang23g.html
     Derivatives Re-Examined. Journal of Functional Programming 19, 2
     (2009), 173–190. doi:10.1017/S0956796808007090
                                                                              Received 2026-07-10; accepted 2026-08-14
[15] Kanghee Park, Timothy Zhou, and Loris D’Antoni. 2025. Flexible
     and Efficient Grammar-Constrained Decoding. In Proceedings of the
