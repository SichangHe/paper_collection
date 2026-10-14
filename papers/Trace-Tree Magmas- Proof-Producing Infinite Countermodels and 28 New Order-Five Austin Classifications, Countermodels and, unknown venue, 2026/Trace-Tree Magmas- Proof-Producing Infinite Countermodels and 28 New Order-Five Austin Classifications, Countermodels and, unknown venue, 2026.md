                                              Trace-Tree Magmas: Proof-Producing Infinite
                                                          Countermodels and
                                                28 New Order-Five Austin Classifications

                                                      Jiaming Zhao1,2 , Bing Wu1 , Tong Yang2 , and Xu Miao1⋆
                                                          1
                                                              Yanbiao Lab, DataCanvas Co., Ltd., Beijing, China
                                                                    2
                                                                      Peking University, Beijing, China
arXiv:2609.05690v3 [cs.LO] 22 Sep 2026




                                                 Abstract. Finite model finders cannot witness an Austin law: an iden-
                                                 tity whose finite models are all trivial but which has a nontrivial infinite
                                                 model. We introduce rank-decreasing sparse trace-tree magmas, a finitely
                                                 presented class of total operations on a countably infinite constructor-
                                                 tree carrier. The default product pairs its arguments, while finitely many
                                                 positive Horn clauses define exceptional outputs. Our main procedure
                                                 derives candidate clauses from symbolic evaluation traces. For every re-
                                                 ported model, it proves functionality of the exceptional relation by de-
                                                 scent on constructor size, proves the source identity by exhaustive sym-
                                                 bolic case analysis, and compiles the result into a self-contained Lean 4
                                                 certificate. A least simultaneous fixed point gives the model language
                                                 an implementation-independent semantics, so bounded search may miss
                                                 models but cannot invalidate a certified result.
                                                 On ETP’s 96 order-five Austin candidates, we discover and Lean-verify
                                                 infinite countermodels for 28 identities that had no prior public classifi-
                                                 cation in our documented literature-and-artifact audit. They form four-
                                                 teen classes under opposite-magma duality and establish 28 new Austin
                                                 classifications; each class has a one-clause trace-tree representative. Sup-
                                                 plemental searches independently reconstruct four further identities in
                                                 two duality classes previously reported by ALPS, giving 32 certified can-
                                                 didates in total. We evaluate generalization separately on Canonical-
                                                 4187, the deduplicated union of Order5-130—ten known Austin laws,
                                                 the 96 candidates, and 24 identities open on both the finite and infinite
                                                 sides—and the public 4,141-row ALPS pool. A fresh trace run generates
                                                 636 certificates, all accepted by Judge v3: 36 from Order5-130 and 600
                                                 from the ALPS-only canonical remainder. In a separate same-resource
                                                 comparison at two vCPUs, 2,048 MiB, and 120 seconds per identity,
                                                 Vampire 5.0.1, E 3.5.1, and a parameter-free complete Twee 2.6.1 run
                                                 have a 94-class union on the implication-proof side. Only Twee produces
                                                 trusted counter-satisfiable outcomes: 18 canonical classes, of which in-
                                                 dependent finite-side certificates force 16 to be infinite. None of these
                                                 ATP runs emits an explicit model or a Lean certificate, and none is de-
                                                 cisive on the 28 newly classified identities. This comparison documents
                                                 a complementary capability gap. To the best of our audit, this is the

                                         ⋆
                                             Corresponding author: miaoxu@zetyun.com.
2       J. Zhao et al.

      first automated system to synthesize this trace-tree model family, gen-
      erate its well-founded inversion proofs, and emit self-contained Lean 4
      certificates.

      Keywords: automated deduction · infinite model synthesis · equational
      logic · Austin identities · Lean 4 · term rewriting


1   Introduction
A magma consists of a carrier and one binary operation. Despite this minimal
signature, its equational logic exhibits a sharp finite–infinite gap. Austin showed
that an identity may force every finite model to be trivial while still admitting a
nontrivial infinite model [1,2]. Such Austin laws are difficult for standard model
search for a structural reason: no finite multiplication table can witness the
required model.
    The Equational Theories Project (ETP) turns this classical phenomenon into
a large, formally specified classification problem [6]. Its order-five study isolated
96 identities known to have only trivial finite models but with no known infinite
model in the fixed public snapshot [10]. Proving that one of these identities
is an Austin law requires more than a satisfiability answer. One must describe
an infinite carrier and a total binary operation, prove the identity for every
valuation, and show that the carrier is nontrivial.
    This paper develops automated semantic searches that produce exactly such
objects. Their principal language consists of operations on the free constructor
algebra
                              T ::= e | k(T ) | ⟨T , T ⟩.
The default product is the ordered pair of its arguments. A finite set of univer-
sally quantified Horn rules presents exceptional products; the induced relations
are defined by a least simultaneous fixed point, without reference to the search
program. The principal algorithm extracts rule shapes from an evaluation trace
of the source law. Pair projections recover rule parameters, while constructor size
provides a well-founded measure for recursive inversion. The generated source
proof then considers every relevant way in which an earlier computation can
return either an exceptional result or the default pair. Thus the result is not a
finite approximation to a large model. It is a finite presentation of a genuinely
infinite magma.
    The second defining feature is proof production. A model is reported only
with a self-contained Lean 4 theorem that reconstructs the carrier and operation,
proves universal source validity, and refutes the target identity. The common
constructor presentation separately supplies the uniform injection n 7→ kn (e), so
every trace carrier is infinite (Lemma 3). The Python search and code generator
remain untrusted: a wrong candidate or a defective proof script is rejected by
Lean’s kernel [23,30].
    The trace procedure produced the first public nontrivial infinite models found
in our documented literature-and-artifact audit for 28 order-five identities, form-
ing 14 duality classes. The distinction from prior ATP results is concrete. All
                                                        Trace-Tree Magmas         3

28 occur among the 96 order-five candidates that the published Vampire cam-
paign left unresolved; that campaign reports no constructed infinite model for
them [10]. In our same-resource experiment, Vampire, E, and one parameter-
free complete Twee run likewise return no decisive status on any of the 28. The
later Vampire/E extraction of explicit, possibly infinite models applies to the
order-at-most-four ETP corpus rather than these identities [15]. Our supple-
mental searches also reconstruct four identities in two duality classes previously
reported by ALPS; those four are explicitly excluded from the novelty count
[31,32].
    The published ALPS experiment is separate from our same-resource runs. Its
eight-configuration ATP portfolio resolves 2.2% of the 4,141-law pool at its initial
budget, and a twentyfold budget increase adds only 0.6 percentage points. At the
largest budget it reports 110 implication proofs but only four construction-side
models, all from complete Twee; under ALPS’s fixed reasoning-model protocol,
the strongest tested model solves no construction- side instance [32]. These re-
sults expose a measured shortage of model-construction methods rather than
merely a shortage of proof-search time.
    Our novelty lies in a specific combination: a finite presentation derived from
source-law traces, a functionality proof based on rank-decreasing inversion, and
end-to-end compilation of every reported operation into a self-contained Lean 4
theorem. To the best of our literature and public-artifact audit, no prior system
searches this model family or generates certificates for it.
    The contributions are:
 1. an implementation-independent semantics for finitely presented trace-tree
    magmas, together with a trace-clause synthesis algorithm. An explicit theo-
    rem chain starts from the least relational semantics, proves the exceptional
    relation functional by constructor-size induction, and obtains a total magma
    on a countably infinite carrier;
 2. a proof-producing trace search whose depth sweep, orientation schedule,
    source generalizations, and finite resource bounds are explicit, together with
    a Lean 4 compiler producing end-to-end certificates and an explicit trust
    boundary: untrusted enumeration, proof search, and text generation cannot
    create a counted result without kernel acceptance;
 3. the first public infinite models for 28 previously unclassified order-five iden-
    tities, establishing 28 new Austin classifications in fourteen duality classes,
    together with a one-clause structural taxonomy and a fresh evaluation on
    Canonical-4187, the explicitly deduplicated union of Order5-130 and ALPS-
    4141;
 4. three supplementary searches with proof production—guarded decoding,
    strict completion, and canonical-form search—whose different model lan-
    guages and targeted regression scopes are reported separately rather than
    merged into the comparison with Vampire, E, and Twee.
   The paper emphasizes the model language, search principles, correctness,
and mathematical structure of the synthesized models. Runtime and memory
are reported only to establish feasibility.
4       J. Zhao et al.

    Section 2 fixes the equational setting and duality notation. Sections 3 and 4
define the model language and the search algorithm. Section 5 gives the sound-
ness chain and trust boundary, after which Section 6 analyzes the models found.
Section 7 reports the independent experiments and the comparison with estab-
lished ATPs.


2     Problem setting

2.1   Equational nonimplication and Austin laws

We follow the notation of the ETP report [6]. If X is an alphabet, let MX =
(MX , ⋄) denote the free magma generated by X. Thus a word in MX is either a
letter of X or a product u ⋄ v. Every map f : X → M into a magma M = (M, ⋄)
extends uniquely to a homomorphism φf : MX → M. A law is a formal equality
s ≃ t with s, t ∈ MX , and M |= s ≃ t means φf (s) = φf (t) for every f : X → M .
For laws E, F , we write E |= F when every magma satisfying E also satisfies F .
Following ETP, the order of a law is the total number of occurrences of ⋄ on its
two sides.
    ETP assigns stable names En to laws. The law E2 is x ≃ y and therefore
holds exactly in singleton magmas. A countermodel to

                                   En =⇒ E2

is consequently a nontrivial model of En. Combining such a model with an
independent result that every finite model of En is trivial proves the following
classification.

Definition 1. A law E is an Austin law if every finite magma satisfying E is
trivial and some infinite magma satisfies E.

    The certificate problem addressed here is semantic: given a source law E and
target law F , synthesize a magma A = (A, ⋄), a proof A |= E, and a valuation
refuting F . For F = E2, the last component is simply a pair of distinct carrier
elements.


2.2   Opposite-magma duality

For a magma M = (M, ⋄), let Mop = (M, ⋄op ), where a ⋄op b = b ⋄ a. Reversing
the two children at every internal word node maps a law E to its dual E ∗ , and

                         M |= E     ⇐⇒      Mop |= E ∗ .

Finiteness, infinitude, and nontriviality are preserved. We therefore analyze the
new results as 14 duality classes, although Lean checks a separate certificate for
every one of the 28 identities.
                                                                  Trace-Tree Magmas     5

3     A search language for infinite tree magmas
Three objects play different roles throughout the paper. First, search produces a
finite rule set R. Second, the rules define two relations: CR (a, b; o) says that o is
an exceptional output allowed for the input pair (a, b), while SR (a, b; o) says that
o is an admissible intermediate result. An admissible result may be either the
default pair or an exceptional output. Third, after proving that CR has at most
one output for each input pair, we define the total operation evalR . The relation
SR is deliberately multivalued and is never used as the magma operation. The
implementation name Code refers to CR ; it does not mean generated Lean source
code.

3.1   The constructor-tree carrier
Let T be the inductive set generated by a constant e, a unary constructor k, and
an ordered-pair constructor ⟨−, −⟩. Define

          |e| = 0,      |k(a)| = |a| + 1,          |⟨a, b⟩| = (|a| + 1) + (|b| + 1).

Both pair components are strictly smaller than their parent. Constructor dis-
jointness and injectivity give total structural projections that reveal the left or
right component of a pair. To make the cardinality statement explicit, fix an
injective pairing function π : N2 → N and define

        γ(e) = 0,     γ(k(a)) = 3γ(a) + 1,          γ(⟨a, b⟩) = 3π(γ(a), γ(b)) + 2.

The residue modulo three identifies the outer constructor, and injectivity of π
then proves by structural induction that γ is injective. Conversely, n 7→ kn (e)
is injective by constructor injectivity and disjointness. Hence T is countably
infinite.
    The carrier is chosen for three concrete reasons. A default pair records the two
arguments of a multiplication. Projections expose those arguments to the gener-
ated uniqueness proof. Constructor size turns an attempted cyclic tree equation
into an arithmetic contradiction.

3.2   Formal clause syntax and semantics
Let V = {v1 , . . . , vr } be clause parameters and let H = {h1 , . . . , hm } be disjoint
metavariables for intermediate results. Write P (V, H) for the free constructor
algebra generated by V ∪ H:

                  p ::= v | h | e | k(p) | ⟨p1 , p2 ⟩,       v ∈ V, h ∈ H.

A dependency-respecting trace clause is
                                m
                                ^
                     ∀V H.            S(pi , qi ; hi ) =⇒ C(pL , pR ; pO ),            (1)
                                i=1
6       J. Zhao et al.

The clause must satisfy three dependency conditions. The patterns pi , qi may
mention only V and {hj | j < i}; the third argument of the ith premise is exactly
hi ; and the head may mention all of V ∪H. A ground substitution θ : V ∪H → T
extends homomorphically to patterns. The principal trace generator uses the
distinguished source variable as pO ; the larger syntax is useful for stating the
semantic class and for the related completion procedure.
     For S ⊆ T 3 , let InstR (S) be the set of all triples (θpL , θpR , θpO ) obtained
from a clause of R and a ground substitution θ whose instantiated premises all
belong to S. Let
                          Raw = {(a, b, ⟨a, b⟩) | a, b ∈ T }.
On the complete lattice P(T 3 ) × P(T 3 ), define the monotone operator
                                                                
            ΦR (C, S) = C ∪ InstR (S), S ∪ Raw ∪C ∪ InstR (S) .                   (2)

Definition 2 (Relational semantics). For a finite dependency-respecting rule
set R, let (CR , SR ) = lfp(ΦR ). Thus CR is the ternary exceptional-output relation
generated by ground rule instances, and SR is the relation of allowed intermediate
results generated jointly by default pairs and exceptional outputs.

Proposition 1 (Least semantics). Definition 2 determines a unique least pair
of relations. It is the union of the finite iterates of ΦR from (∅, ∅), and it is
equivalent to the mutually inductive default-pair, exceptional-output, and clause-
instantiation rules used in the generated Lean certificate.

Proof. The operator in Eq. (2) is monotone. Its clauses are finitary, so the union
of the ascending ω-chain from the bottom is a fixed point. Induction on the
iteration number proves that it is contained in every pre-fixed point, hence it is
least. The same induction translates iterations to finite constructor derivations
and conversely.

    When R is fixed, we suppress its subscript on CR , SR , and evalR . The two con-
structors of the generated Lean relation are called raw and hit; mathematically
they express the following default-pair and exceptional-output rules:

               S(a, b; ⟨a, b⟩)                                  for all a, b,     (3)
                    C(a, b; o) =⇒ S(a, b; o).                                     (4)

Thus SR records admissible intermediate results rather than defining a partial
function. If CR (a, b; o) and o ̸= ⟨a, b⟩, then the same inputs have at least the two
admissible outputs o and ⟨a, b⟩. No theorem below assumes global functionality
of SR .

Definition 3 (Well-formed trace-tree presentation). A finite dependency-
respecting rule set R is semantically well formed when its least exceptional rela-
tion is output-functional:

               ∀a, b, o, o′ ∈ T .   CR (a, b; o) ∧ CR (a, b; o′ ) =⇒ o = o′ .
                                                         Trace-Tree Magmas         7

Its exceptional domain is Exc(R) = {(a, b) | ∃o CR (a, b; o)}. The adjective finitely
presented refers only to finiteness of R: Exc(R) may be infinite, or even all of
T 2 . No set-theoretic density claim is intended.

      For a well-formed R, define
                                   (
                                    o,      if CR (a, b; o) for some o,
           a ⋄R b = evalR (a, b) =                                               (5)
                                    ⟨a, b⟩, if no exceptional output exists.

Functionality makes the first branch independent of witness choice. The resulting
magma TR = (T , ⋄R ) is a trace-tree magma. Lean implements the first branch
by classical choice and proves its independence using the generated functionality
theorem.

Proposition 2 (Total tree operation). If R is well formed, Eq. (5) defines a
total magma on the countably infinite carrier T . Moreover, SR (a, b; evalR (a, b))
holds for all a, b ∈ T .

Proof. If no exceptional output exists, the second branch is unique and Eq. (3)
supplies the step. Otherwise all exceptional outputs agree; the chosen output is
therefore well defined and Eq. (4) supplies the step. Countability and infinitude
were proved above.

    The mutually inductive presentation is essential. A rule may depend on an
earlier admissible computation without deciding whether that computation was
itself default or exceptional. Soundness therefore cannot be inferred from one
preferred execution trace; it must cover both derivation forms of SR .

3.3     Projection–rank certificates
Rank belongs to the proof discipline, not to the semantic definition above. In-
tuitively, the certificate is a finite case-analysis graph: it may return to an ear-
lier proof state only after proving that an explicit constructor-size measure has
decreased. The following definition makes this condition independent of Lean
syntax. Fix a presentation R. An inversion obligation is a universally closed
schematic sequent Γ ⊢ G. Its assumptions Γ may contain constructor equal-
ities, CR - or SR -derivations, and inequalities between constructor sizes. Each
node of the certificate names one obligation. An expansion replaces that obli-
gation by finitely many successors and records a derivation showing that the
successors imply their parent. This derivation uses only the first-order theory of
free constructors and the usual order on natural numbers. Inverting a CR or SR
derivation creates one successor for each applicable constructor. Projections or
constructor clashes may close a successor immediately. When inversion exposes
an inner exceptional derivation, the expansion may refer back to an already
named obligation.
    A projection–rank certificate is a finite directed hypergraph of these nodes
and expansions with the following data:
8       J. Zhao et al.

 1. every nonrecursive expansion carries a local derivation, using only construc-
    tor inversion, injectivity, disjointness, projection along a fixed path, and valid
    arithmetic over the size equations;
 2. every leaf has a derivation of its obligation without successors; and
 3. for each recursive strongly connected component there is a fixed dimension d
    and a rank µ : Qground → Nd . Each component of µ is the size of an explicit
    constructor pattern in the state’s ground arguments, and every recursive
    edge proves µ(q ′ ) <lex µ(q).

Here Qground denotes the ground instances of the finitely many schematic obli-
gations. A recursive edge also records the substitution that maps the successor
schema to the exposed ground subobligation. Lexicographic order on Nd is well
founded, so recursive back edges unfold to a well-founded (possibly unbounded-
depth) derivation rather than a finite-depth approximation. Certificates with no
recursive edge have a vacuous rank component.
    The finite hypergraph is a metatheoretic abstraction of the generated proof,
not a separately serialized intermediate representation in the released artifact.
The released implementation realizes only the scalar fragment d = 1: every mu-
tually recursive Lean theorem uses an explicit natural-valued constructor-size
expression, such as |a| or |⟨o, a⟩|, in its termination_by clause, and emits the
corresponding strict-decrease obligation. It neither searches for nor emits lexico-
graphic tuple ranks. The Nd formulation records a sound extension of the proof
discipline; every experimental claim in this paper and every released certificate
instantiates d = 1.

Proposition 3 (Certified inversion). Every closed projection–rank certificate
proves its root sequent. In particular, a certificate rooted at

                         CR (a, b; o) ∧ CR (a, b; o′ ) =⇒ o = o′

proves that R is semantically well formed.

Proof. Within each recursive component, use well-founded induction on µ. The
recorded substitution and decrease proof make every recursive successor available
at smaller rank; each nonrecursive expansion is locally sound and each leaf is
closed. Process the acyclic component graph in reverse topological order. The
resulting root proof is uniform over all ground substitutions.

    This definition separates three notions that the implementation must not
conflate: a finite syntactic rule set, its independently defined least semantics,
and a proof that establishes the required semantic property. In the artifact that
last object is the elaborated Lean proof term; the derivation hypergraph above
is the proof-system account used for the soundness argument. Failure to syn-
thesize an accepted Lean proof yields unknown; it does not make the rule set
mathematically ill defined.
                                                           Trace-Tree Magmas      9

4     Proof-producing trace search

The principal procedure targets a law normalized to x ≃ t, where x is a variable
and t is a non-variable term of the free magma. This includes all 28 new order-
five classifications. The implementation parses t into an evaluation tree and
performs the following stages. Its search state contains only the two parsed laws,
a deterministic candidate index, and resource counters; equation numbers are
absent.


4.1   Trace-mask enumeration

Let N be the non-root internal nodes of t, ordered bottom-up. A trace mask is a
subset M ⊆ N . Nodes in M are called active; the other nodes in N are inactive.
Define a symbolic value rM (n) recursively. A leaf retains its variable. An inactive
node is represented by the free pair of its two child values. An active node n
receives a fresh symbol hn and contributes the premise

                             S(rM (nL ), rM (nR ); hn ).

At the root, the two symbolic child values become the inputs of an exceptional
clause whose output is x. Thus every mask determines one candidate of the form
Eq. (1). Masks are enumerated by increasing number of active nodes and then
deterministically by bit pattern. This favors small semantic descriptions, but
does not enter the soundness argument.
    Write IM = N \ M for all inactive nodes. A node in IM is outer-visible if it
has no active ancestor; let VM ⊆ IM be this subset. The distinction matters in
the universal proof. Nodes in VM are rewritten explicitly while evaluating the
root expression. Inactive descendants of an active node are not outer-visible, but
their values may still be needed to identify the symbolic inputs of that active
node’s S premise. The proof generator therefore reasons about every node in IM ,
not only VM .
    The released implementation exposes every finite search bound. It accepts
source terms with two through eight internal product nodes and runs the core
on both the given and opposite orientations. Within one core invocation, the
candidate index i counts masks that survive clause construction, all three proof
builders (for functionality, universal source validity, and a target witness), and
certificate compilation. The tuned schedule fixes i = 0 and instead enlarges the
symbolic tableau systematically. For each depth

                                 d = 0, 1, 2, 3, 4, 5,

it tries the given orientation and then the opposite orientation, allowing 9.5 sec-
onds for each call. Thus each call asks for the first fully supported mask at that
tableau depth; increasing d permits longer chains of nested exceptional-step in-
versions in absence-of-exception proofs. This change alters the finite enumeration
schedule, not the clause semantics or acceptance obligations.
10      J. Zhao et al.

    After the depth sweep, a second finite schedule tries at most the first four de-
terministic source generalizations in both orientations. Generalization replaces
either a proper nonempty subset of repeated occurrences or one proper com-
pound subterm by a fresh variable. The trace core runs at depth one and the
generated source proof explicitly specializes that variable back to the original
term. Each generalized call has a three-second local deadline. A single 120-second
global deadline truncates every local allowance, so late jobs may receive less time
or may not start; any call that finishes early proceeds immediately. These bounds
restrict coverage only: every returned candidate must satisfy the same function-
ality, universal-source, and target-witness proof requirements.
    For example, if the active subcomputation is (z ⋄ (x ⋄ x)) ⋄ y, the mask may
introduce
                                  S(⟨z, ⟨x, x⟩⟩, y; h)

and leave the inactive nodes as explicit free pairs. Search never specializes x, y, z
to ground trees: they remain universally quantified rule parameters.


4.2   Functionality and ranking synthesis

A candidate is discarded unless the system constructs a closed projection–rank
certificate, in the precise sense of Sec. 3.3, for output functionality. To prove
that derivations C(a, b; o) and C(a, b; o′ ) have o = o′ , the generator combines
four kinds of facts:

 1. constructor projections equate parameters visible at fixed paths;
 2. constructor injectivity propagates those equalities into trace premises;
 3. pattern-specific inversion lemmas for admissible-step premises recover equal
    clause parameters after considering the default-pair and exceptional-output
    constructors; these local lemmas do not assert global functionality of S; and
 4. strict size inequalities exclude cyclic or self-embedding matches.

    The rank analysis is performed symbolically. Pair constructors generate lin-
ear inequalities such as |a| < |⟨a, b⟩|. A rule has three distinguished values—its
two inputs and its output—and hence six ordered comparisons between dis-
tinct values. In the general trace case, the implementation begins with these
six comparisons. A comparison is retained exactly when, after splitting every
premise into its default and exceptional derivations, the current retained set
proves that comparison in every branch. Iteration to a fixed point terminates
because the candidate set is finite. The retained comparisons become invari-
ants of the mutually recursive inversion states; specialized shapes use direct
projection inequalities. Each recursive call is annotated by an explicit natural-
valued constructor-size expression, and the compiler emits the corresponding
strict-decrease obligation. Arithmetic closes only branches whose accumulated
inequalities are inconsistent. Finite testing of tree assignments is never accepted
as a substitute for functionality.
                                                         Trace-Tree Magmas      11

4.3   Universal source-proof synthesis

Even a functional operation may fail the identity away from the trace that sug-
gested it. The second filter therefore synthesizes a universal proof of the source
identity rather than replaying one preferred execution. It builds a finite symbolic
proof tree by repeatedly splitting the constructors of S and C derivations. This
proof tree is a certificate-construction device, not an additional semantic object.
For any pair of symbolic inputs, define the absence-of-exception predicate

                     NoExcR (a, b)   :⇐⇒      ¬∃o. CR (a, b; o).               (6)

A formula NoExcR (a, b) is an obligation while the generator is trying to prove
it and a theorem only after Lean has checked the generated proof. Its exact
operational consequence is evalR (a, b) = ⟨a, b⟩ by Eq. (5): no exceptional rule
applies, so the product takes the default-pair branch.
    For every inactive node n ∈ IM , with symbolic children an , bn , the source-
proof generator constructs the obligation

                                 NoExcR (an , bn ).

It proves this formula in the context of the S facts on which an , bn depend. To do
so, the generator considers both constructors of every such fact: the default-pair
case in Eq. (3) and the exceptional-output case in Eq. (4). In the latter case, it
inverts the applicable C clause, uses constructor projections and unification to
expose its parameters, and may recursively analyze another exceptional-output
premise. The proof therefore does not assume that an active node took the
default branch.
    A proof branch is discharged only by a contradiction that the compiler can
express and Lean can check:

 1. constructor projections make the required exceptional pattern impossible;
 2. constructor disjointness or injectivity yields a contradiction;
 3. unification would require a finite tree to contain itself; or
 4. accumulated rank inequalities form a strict cycle.

If a branch cannot be discharged, the current mask is rejected and enumeration
continues. For an active node, the checked predicates for its inactive descendants
identify the node’s actual child values with the symbolic inputs of its S premise;
Prop. 2 then supplies that premise for the actual product. After active subtrees
have been summarized by their fresh symbols, the predicates for the outer-visible
nodes VM rewrite the remaining products to free pairs. The root C clause finally
rewrites the whole right-hand side to x. The generated Lean proof consists of
the corresponding case splits, equalities, projection lemmas, and arithmetic ar-
guments. It covers every admissible-step case required by the trace; it is not
random testing or bounded enumeration of carrier elements.
12     J. Zhao et al.

4.4   Witness synthesis and certificate compilation

For target E2, the fixed witness is e ̸= k(e). General targets can instead be eval-
uated symbolically under a synthesized valuation. The compiler emits the tree
datatype, C and S, the functionality theorem, the total operation, the universal
source proof, and the target refutation required by the official Goal interface.
That interface has no separate infinitude field: infinitude of the emitted trace
carrier is supplied uniformly by Lemma 3. If a proof pattern is unsupported, the
compiler returns failure rather than emitting a candidate. The protocol wrapper
likewise rejects empty output and output beyond the submission-size limit. The
official Judge independently enforces its proof policy and determines semantic
acceptance in Lean.
    Internally, only equality chains use a typed intermediate representation. The
released class _v13_EqProof stores the symbolic endpoints of each chain to-
gether with its Lean text. Before composing that text, the generator checks
the endpoints of every use of reflexivity, symmetry, transitivity, congruence, or
constructor projection. An inconsistent chain is therefore rejected in Python.
Functionality inversions, symbolic source-proof branches, and target normaliza-
tion are emitted as structured Lean fragments, with separate Python checks for
unsupported constructions. The implementation does not serialize one common
proof graph for all of these tasks. Constructor case splits bind the actual fields
of the selected C or S constructor instead of asking Lean’s elaborator to infer
unnamed witnesses. Both internal representations remain untrusted: only elab-
oration and kernel checking of the complete Lean theorem turn a candidate into
evidence.
    These failure paths affect only search completeness. If a source-proof branch
remains unresolved, the current mask is rejected and the mask loop continues.
If target-witness synthesis finds no separating valuation, the current mask is
likewise rejected. After a ground target witness has been found, failure to gen-
erate a NoExcR proof for one of its default products also rejects only the current
mask, and enumeration proceeds to later masks. No such failure can accept an
unsupported model.
    Figure 1 gives the core search independently of benchmark identifiers. The
implementation receives only parsed source and target terms; equation numbers
are not part of its search state or candidate grammar.
    The algorithm maintains three acceptance obligations. First, the generated
functionality theorem proves output uniqueness of the least relation CRM by con-
structor projection and scalar size descent. Second, the source theorem resolves
every default-pair/exceptional-output case needed to interpret the law under an
arbitrary valuation. Third, the target theorem evaluates both sides under the
same explicit valuation and proves distinct constructor normal forms. The com-
piler may represent an obligation by a typed equality record or by a direct Lean
fragment, but it never infers validity from the mask or from a finite test set.
The wrapper returns a model only after assembling all three obligations into
one checkable theorem. Conversely, mask order, conservative early termination
of a core call, schedule truncation, symbolic-proof depth bounds, and budget B
                                                            Trace-Tree Magmas            13

   procedure TraceCore(x ≃ t, F, i, d, D)
   j←0
   for M ⊆ N (t) \ {root} in increasing (|M |, bits(M )), while before D, do
   (RM , IM , VM ) ← BuildTraceClause(t, M ); handle reject/abort as below
   Pfun ← EmitFunctionalityProof(RM ); handle reject/abort as below
   Psrc ← EmitSourceProof(x ≃ t, RM , IM , VM , d); if an unresolved branch re-
   mains then reject-mask
   (ν, Wtgt ) ← SynthesizeTargetWitness(F, RM ); if none then reject-mask
   Ptgt ← EmitTargetNormalization(F, RM , ν, Wtgt ); if unsupported then reject-
   mask
   L ← CompileLean(RM , Pfun , Psrc , ν, Ptgt ); handle reject/abort as below
   if j < i then j ← j + 1; continue
   return L
   return failure
   where reject-mask continues the mask loop, whereas abort-job returns failure
   from TraceCore
   procedure TraceSynth(E, F, B)
   DB ← now + B
   for each job J = (EJ , FJ , i, d, δJ , τJ ) in the fixed schedule while now < DB do
   D ← min(DB , now + δJ )
   L ← TraceCore(EJ , FJ , i, d, D); if failure then continue
   L ← τJ (L)
   if L passes the postprocessing syntax and byte-size checks then return L
   return unknown
Fig. 1. Core trace-model synthesis. Here IM is the set of inactive nodes and VM ⊆ IM
is the subset with no active ancestor. A scheduled job fixes an orientation or source
generalization, candidate rank, proof depth, local allowance δJ , and proof-preserving
conversion τJ . The released depth sweep uses rank zero. The two failure modes repro-
duce the implementation: reject mask continues enumeration, whereas abort job ends
the current core invocation. The returned Lean theorem is the certificate; finite bounds
affect completeness only.


can omit a valid presentation. Returning unknown therefore means only that no
accepted certificate was found in the explored finite search.


4.5   Supplementary proof-producing model searches

Three additional searches reuse parts of the constructor vocabulary and certifi-
cate infrastructure but enumerate different mathematical presentations. They
are not trace-mask ablations. Their role in this paper is supplementary: the
tuned trace search receives the full Canonical-4187 union, whereas guarded de-
coding, completion, and CNF are rerun on fixed historical-hit sets to check that
their optimized implementations still regenerate accepted certificates.
   Guarded decoding enumerates a fixed grammar of total decoders on e, unary
constructors, and selected pair patterns. Multiplication either invokes the de-
coder under a syntactic guard or returns a free pair. The tuned implementation
14     J. Zhao et al.

observes that its Lean proof contract forces all seven decoder choices and there-
fore tries that unique admissible program directly, in both orientations, rather
than enumerating programs that the same contract must later reject. Shallow
and depth-two tree evaluations remain search filters; the compiler proves the
resulting source identity by complete constructor cases. Thus the optimization
changes enumeration cost, not the accepted decoder semantics. Section 6.3 gives
the model for the known dual pair.
    Strict completion starts from oriented consequences of the source, using an
occurs-checked unifier and a Knuth–Bendix-style order to retain only variable-
safe, decreasing root rules. It computes critical peaks, requires joinability when
using the confluence route, proves that every rule maps normal inputs to a
normal output, and constructs a symbolic proof of the source over every possible
choice between a matching rule and the default pair. Selected variants use that
exhaustive proof directly rather than relying on confluence. Like trace search, the
resulting operation changes the default pairing only at roots matched by finitely
many rules, but completion derives its candidates from critical-pair reasoning
rather than trace masks. Direct and opposite orientations are searched explicitly.
A bounded algebraic prefix check can discard an unpromising seed, but never
serves as acceptance evidence: every emitted candidate still requires a complete
symbolic source proof and a Lean certificate. The main tuned implementation
uses a hybrid compiler for the same completed-rule semantics: it selects the
regular proof representation for small rule systems whose indexed proof graph
contains an occurs-cycle leaf, and the indexed representation otherwise. The two
supplemental completion profiles used in Section 7 change search scheduling or
proof representation only; they do not define new model semantics.

4.6   Canonical-form search
The fourth standalone program uses a narrower grammar of canonical forms. We
retain its implementation name, CNF search, where CNF abbreviates canoni-
cal normal form and is unrelated to conjunctive normal form. Candidate seeds
come from diagonal simplification, abstraction of a compound shared by the
two source sides, or direct orientation of the source. A bounded critical-pair
completion, capped at 16 rules and 16 rounds, may extend a seed; completed
systems are tried before uncompleted seeds. A rule is admissible only when its
left-hand side has a pair at the root, its variables are closed, and it decreases
the selected order. This pair-root condition is enforced at orientation, seed con-
struction, rule admission, tableau, witness, and compilation boundaries. It is a
soundness restriction: without it, the Python evaluator and Lean normal-form
carrier can disagree about where a rule may fire. A retained system must also
send normal inputs to normal outputs. Its source checker shares repeated sub-
terms in an evaluation directed acyclic graph and considers, at every product
node, each matching root rule and the default-pair case. Occurs-checked unifica-
tion detects cyclic substitutions; negative constraints record when a rule pattern
does not match; and normal-form closure is used to resolve every proof branch.
Any unresolved branch rejects the system. Target-witness search and a dedicated
                                                         Trace-Tree Magmas       15

Lean compiler then produce the candidate. For a retained rule system R, write
TNF (R) for the constructor trees containing no R-redex at any subtree; output
safety makes this carrier closed under the synthesized operation.
    Semantically, CNF search also defines a free-pair operation modified at roots
matched by finitely many rules. Algorithmically it has its own seed grammar,
completion loop, symbolic source proof, compiler, and 120-second experimental
budget. We therefore report it separately rather than folding its targeted hits
into the primary trace comparison.


5     Correctness and the Lean trust boundary
The mathematical checker embedded in the search and the final Lean checker
serve different roles. The former efficiently rejects bad candidates and constructs
proof terms; the latter is the authority for every reported model.

5.1   Soundness as a theorem chain
Fix a dependency-respecting presentation R, and interpret C and S by the least
simultaneous semantics of Definition 2. Write

               : ⇒ ∀a, b, o, o′ ∈ T .
        Fun(C) ⇐                         C(a, b; o) ∧ C(a, b; o′ ) =⇒ o = o′ .

The following statements separate semantic assumptions from the algorithm that
constructs their certificates.
Lemma 1 (Functionality from certified inversion). If a closed projection–
rank certificate has root sequent C(a, b; o) ∧ C(a, b; o′ ) ⇒ o = o′ , then Fun(C).
Proof. Apply Proposition 3 uniformly to every ground quadruple a, b, o, o′ . No-
tice that the argument proves functionality of the least exceptional relation; it
does not assume, and generally cannot prove, functionality of the multivalued
relation S.
Lemma 2 (Evaluation equations and step adequacy). Assume Fun(C).
For all a, b, o ∈ T :
1. C(a, b; o) implies eval(a, b) = o;
2. ¬∃q. C(a, b; q) implies eval(a, b) = ⟨a, b⟩; and
3. S(a, b; eval(a, b)).
Proof. In the exceptional case, functionality equates the witness selected in
Eq. (5) with o; in the nonexceptional case the second branch of that definition
applies. The exceptional-output and default-pair rules, respectively, establish the
third item.
Lemma 3 (Infinite carrier). The map n 7→ kn (e) embeds N into T . Con-
sequently every full-tree trace or guarded presentation has a countably infinite,
hence nontrivial, carrier.
16      J. Zhao et al.

Proof. Constructor injectivity and disjointness make the unary tower injective;
the encoding γ from Section 3 gives the converse countability bound.
Lemma 4 (Universal trace-proof soundness). Let a mask for the law x ≃ t
determine a well-formed rule set R, the inactive-node set IM , and the outer-
visible subset VM . Suppose the symbolic proof establishes NoExcR (an , bn ) for ev-
ery n ∈ IM under both the default-pair and exceptional-output cases of every S
premise on which an , bn depend. Then TR |= x ≃ t.
Proof. Fix an arbitrary valuation f : X → T and evaluate t from the leaves
upward. At every inactive node, its NoExcR theorem and Eq. (5) identify the
actual product with the free pair used in the symbolic trace. This has two distinct
uses. First, inactive descendants of an active node identify its actual child values
with the symbolic inputs in that node’s S premise. Lemma 2 then supplies the
premise for the active node’s actual output, whether that output is the default
pair or an exceptional value. Continuing upward establishes every active-node
premise and instantiates its fresh result symbol. Second, once active subtrees
have been summarized in this way, the NoExcR theorems for the outer-visible
nodes VM rewrite the remaining products above them to their symbolic free
pairs. The two root inputs now match the instantiated head of the generated C
clause, whose output is f (x). Lemma 2 therefore identifies the root product with
f (x). Since f was arbitrary, the law holds.
Lemma 5 (Countervaluation soundness). Let F be u ≃ v. If, under one
valuation ν, symbolic evaluation derives φν (u) = a, φν (v) = b, and a ̸= b, then
TR ̸|= F .
Proof. The two evaluation derivations interpret the same operation and valua-
tion. Substituting them into a hypothetical equality for F gives a = b, contrary
to the constructor inequality.
Lemma 6 (Soundness of scheduled transports). Every transport τJ used
by the fixed schedule preserves a certified nonimplication and the cardinality of
its carrier.
Proof. The schedule composes only four operations. Swapping the two sides of
a law uses symmetry of equality. A generalized source EJ is accompanied by an
explicit term substitution σ with σ(EJ ) = E; satisfaction of a universal identity
is closed under term substitution, so a model of EJ is a model of E. Identity
jobs require no transport. Finally, an opposite job applies the equivalence of Sec-
tion 2 simultaneously to the source and target: a model of E ∗ refuting F ∗ yields
its opposite magma, which models E and refutes F . None of these operations
changes the underlying carrier. Closure under composition proves the claim.
Theorem 1 (Soundness of a kernel-accepted trace-search output). Sup-
pose the procedure in Fig. 1 returns a Lean declaration for source x ≃ t and
target F , and the fixed official Lean environment accepts that declaration under
the stated proof policy. Then its presentation defines a countably infinite magma
satisfying x ≃ t and refuting F .
                                                        Trace-Tree Magmas        17

Proof. Kernel acceptance checks the generated functionality, source, and target
proofs rather than trusting the Python emitter. The checked functionality proof
and Lemma 1 make R well formed; Proposition 2 supplies the total operation.
Lemmas 3, 4, and 5 establish infinitude, source validity, and target failure for
the core search instance, respectively. Lemma 6 transfers these conclusions to
the source and target supplied to the outer procedure.

Corollary 1 (Kernel-accepted certificate). If the fixed official Lean envi-
ronment accepts a generated declaration of type Goal, then the submitted carrier
and operation satisfy the encoded source theorem and refute the encoded tar-
get. Combining that checked declaration with Lemma 3 for full-tree carriers, or
Proposition 4 for normal-form carriers, yields the claimed infinite countermodel.

Proof. The declaration packages the selected carrier and operation, the univer-
sal source theorem, and a target countervaluation against the official problem
interface. Lean elaboration and kernel checking reconstruct those claims. The
separate theorem about the chosen carrier supplies infinitude, which is not a
separate field of the official Goal interface.

    Each returned file contains a complete Lean instance of the relevant argu-
ment. For a trace model, the file proves C functional before defining eval by
choice. In particular, no certificate assumes that S is globally functional: its lo-
cal inversion lemmas are used only under the constructor patterns and premise
context for which they were generated. For the normal-form specialization of
Sec. 6.4, both the completion and CNF compilers prove closure of the carrier
under every possible selected rule. Their symbolic source proofs consider every
root rule and the default-pair case at each product node. They use occurs-checked
unification, record negative constraints when a rule does not match, and reject
a candidate if any proof branch remains unresolved. Source theorems in both
model families quantify over all carrier variables, and the final declaration in-
habits the official Goal type with the carrier, magma instance, source theorem,
and target refutation.

Proposition 4 (Normal-form soundness). Let R be a finite set of root rules
whose outputs are normal whenever their inputs are normal. Suppose the sym-
bolic proof resolves every default-pair and rule branch of the source, and an ex-
plicit normal valuation separates the two target terms. Then the choice operation
induced by R on TNF (R) is an infinite model of the source and a countermodel
to the target.

Proof. Closure makes the operation total on TNF (R). The symbolic proof covers
every output that the choice operation can select at each source node, so every
evaluation satisfies the source. The unary tower is normal and injective, hence the
carrier is infinite; the recorded valuation refutes the target. Both compilers check
closure, the universal source theorem, and the target refutation in Lean. The
CNF compiler also emits its tower-injectivity lemma; for completion certificates
the same carrier fact is supplied by the uniform mathematical argument above.
18      J. Zhao et al.

5.2   Trust boundary



          candidate             certificate compiler
                                                         official Goal definition
        enumeration              Lean elaboration
                                                               Lean kernel
       symbolic filters    −→        proof-term      =⇒
                                                            permitted axioms
         proof search              construction
                                                           logical trusted base
          untrusted                   untrusted
        failure can cause only unknown or rejection     acceptance yields Cor. 1

Fig. 2. Data flow and trust boundary. Search metadata and Python proof objects are
hints only; the counted result is the theorem reconstructed from the submitted source
and accepted by the official Lean environment.


    The logical trusted base is the Lean kernel together with the official Goal def-
inition and the axioms permitted by the Judge policy. The elaborator translates
source into proof terms but does not enlarge that base: the kernel checks the
resulting term and all imported Mathlib declarations. Enumeration, heuristics,
Python unification, and certificate text generation are likewise untrusted. They
may miss a model or emit a rejected file, but, relative to the official encoding and
permitted axioms, cannot make a false theorem pass kernel checking. Figure 2
also separates logical validation from experimental bookkeeping: a JSON status
or a generator’s own valid flag is never counted without the matching accepted
Judge receipt. A receipt records the pinned checking environment; the theorem’s
logical authority comes from kernel checking, not from the JSON record or its
archive hash.


6     Mathematical structure of the synthesized models

The 28 new classifications are not 28 unrelated programs. Modulo duality, all
fourteen use the full carrier T , the same free-pair default, the same constructor
size, and exactly one constructor for C. For a presentation of the form Eq. (1),
call m its trace arity and call the ordered dependency graph hj → hi whenever
hj occurs in the ith premise its trace dependency graph. Dependency-respecting
syntax makes this graph acyclic. Eleven discovered classes have trace arity one;
three have trace arity two. Table 1 gives their complete mathematical presenta-
tions.
    This yields a compact structural classification.

Proposition 5 (One-clause structure). Every new Austin model reported
here is a well-formed, finitely presented one-clause extension of the free-pair
magma, and its functionality is witnessed by a projection–rank certificate. Up
to opposite-magma duality, its complete law-specific data consist of one Horn
clause with at most two admissible-step premises.
                                                                   Trace-Tree Magmas       19

Table 1. The fourteen new duality classes as one-clause trace-tree models. Here ⟨a, b⟩
is the free pair constructor, S is the admissible-step relation, and C is the exceptional-
output relation. The listed representative uses ⋆ = eval; the other law in the first
column is modeled by the opposite magma.

 Duality class           Premises Law-specific Horn clause
 E4952 / E41252             1     S(z, y; h) ⇒ C(y, ⟨x, ⟨y, ⟨y, h⟩⟩⟩; x)
 E40914 / E4957             1     S(y, x; h) ⇒ C(⟨⟨⟨h, y⟩, z⟩, x⟩, z; x)
 E5012 / E41253             1     S(y, z; h) ⇒ C(y, ⟨x, ⟨z, ⟨z, h⟩⟩⟩; x)
 E5066 / E41239             1     S(z, y; h) ⇒ C(y, ⟨y, ⟨x, ⟨y, h⟩⟩⟩; x)
 E5141 / E40917             1     S(x, y; h) ⇒ C(y, ⟨y, ⟨z, ⟨y, h⟩⟩⟩; x)
 E5295 / E40909             1     S(x, y; h) ⇒ C(y, ⟨z, ⟨y, ⟨y, h⟩⟩⟩; x)
 E38303 / E7701             2     S(x, z; h0 ) ∧ S(y, ⟨h0 , x⟩; h1 ) ⇒ C(⟨h1 , y⟩, y; x)
 E7755 / E38249             1     S(⟨z, ⟨x, x⟩⟩, y; h) ⇒ C(y, ⟨y, h⟩; x)
 E9345 / E36713             1     S(x, y; h) ⇒ C(y, ⟨h, ⟨z, ⟨y, y⟩⟩⟩; x)
 E9384 / E36714             1     S(x, z; h) ⇒ C(y, ⟨h, ⟨y, ⟨z, z⟩⟩⟩; x)
 E9680 / E36524             2     S(z, y; h0 ) ∧ S(x, y; h1 ) ⇒ C(y, ⟨h0 , ⟨y, h1 ⟩⟩; x)
 E9667 / E36638             1     S(z, y; h) ⇒ C(y, ⟨h, ⟨x, ⟨y, y⟩⟩⟩; x)
 E35036 / E11081            2     S(y, z; h0 ) ∧ S(x, y; h1 ) ⇒ C(⟨h0 , ⟨h1 , x⟩⟩, y; x)
 E11116 / E34888            1     S(z, x; h) ⇒ C(y, ⟨⟨x, h⟩, ⟨y, y⟩⟩; x)




Proof. For each of the fourteen rows of Table 1, the archived certificate defines
precisely the displayed clause as the sole constructor of C, proves the corre-
sponding code_unique theorem, and proves the source theorem by complete
default-pair/exceptional-output case analysis. Counting the displayed premises
gives eleven rows of arity one and three rows of arity two. The certificate for
the dual law transports the operation to the opposite magma and is checked
separately.

Theorem 2 (Twenty-eight new Austin classifications). Each of the first
28 laws in Table 7 is an Austin law. They form fourteen classes under opposite-
magma duality.

Proof. The finite-model half is the published ETP classification: every finite
magma satisfying any of these 28 laws is trivial [10]. For one representative of
each row of Table 1, the archived Lean certificate checks the universal source
theorem and an explicit nontrivial valuation in the full-tree carrier. Lemma 3
proves that this carrier is infinite. The separately checked opposite construction
and the equivalence in Section 2 give the dual representative. Thus both clauses
of the Austin-law definition hold for all 28 laws.


6.1   Worked example: a one-premise trace model

Consider E7755:
                                                          
                           x ≃ y ⋄ y ⋄ ((z ⋄ (x ⋄ x)) ⋄ y) .

Its only exceptional clause is

                        S(⟨z, ⟨x, x⟩⟩, y; h) =⇒ C(y, ⟨y, h⟩; x).                           (7)
20      J. Zhao et al.

To match Lemma 4 explicitly, name the five product nodes from the leaves
upward:

      n0 = x ⋄ x,      n1 = z ⋄ n0 ,     n2 = n1 ⋄ y,     n 3 = y ⋄ n2 ,   n 4 = y ⋄ n3 .

The mask makes n2 active and uses the root n4 as the exceptional-clause head.
The nodes n0 , n1 , n3 are inactive. The generated proofs of NoExcR for n0 and n1
show that their actual values are ⟨x, x⟩ and ⟨z, ⟨x, x⟩⟩; these equalities identify
the first input of the active-node premise. Proposition 2 then supplies

                                       S(⟨z, ⟨x, x⟩⟩, y; h)

for the actual value h of n2 . The NoExcR proof for n3 , which is checked under
both possible constructors of that S premise, yields n3 = ⟨y, h⟩. Equation (7)
therefore makes the root n4 equal to x. This is precisely the two-part use of
inactive nodes in Lemma 4: n0 , n1 justify the symbolic inputs of an active node,
while the outer-visible node n3 rewrites the expression above that active node.
    Functionality is equally structural. The left projection of the exceptional
clause’s second input recovers its first input y. If two instances of Eq. (7) share
both inputs, constructor injectivity equates their trace outputs. The generated
pattern-specific S-inversion lemma then recovers the embedded x values. Any
remaining cyclic case would force a finite constructor tree to contain a strictly
larger copy of itself, and the size inequalities rule it out. The opposite operation
gives the dual model for E38249.

6.2   Two-premise models
Three exceptional classes remember two earlier evaluations rather than one. For
E38303, the clause has the sequential trace

                 S(x, z; h0 ) ∧ S(y, ⟨h0 , x⟩; h1 ) =⇒ C(⟨h1 , y⟩, y; x).

The second premise consumes the first trace output, and the root pattern recov-
ers the second. Projection and size reasoning then propagates uniqueness back
through both premises. No new carrier or semantic principle is needed.
    The newly found class E9680/E36524 instead records two independent steps:

                    S(z, y; h0 ) ∧ S(x, y; h1 ) =⇒ C(y, ⟨h0 , ⟨y, h1 ⟩⟩; x).

Thus trace arity two does not by itself imply a dependency edge: the two premises
can be evaluated independently and only meet in the exceptional root pattern.
The third arity-two class, E35036/E11081, has the same empty dependency
graph with a different root projection pattern (Table 1).

6.3   The previously classified guarded pair
The two guarded-decoding certificates, E22619/E22634, independently formalize
a pair already classified by ALPS. They use the same tree carrier but a guarded
                                                                  Trace-Tree Magmas   21

decoder δ:
                              δ(e) = e,                δ(k(a)) = a,
                          δ(⟨a, a⟩) = k(a),      δ(⟨a, ⟨a, x⟩⟩) = x,

with all other pair shapes decoded to e. For E22619, multiplication returns δ(a)
when the right input is e. When b ̸= e and a = ⟨b, b⟩, it returns e; in every other
case it returns the free pair ⟨a, b⟩. The key identity δ(y ⋄ (y ⋄ x)) = x supplies
the required cancellation. The model for E22634 uses the opposite operation.
These two certificates strengthen the formal evidence but are excluded from the
novelty count.


6.4   Normal-form models from completion and CNF search

The completion procedure and the independently extracted CNF procedure use
different candidate enumerators and Lean compilers, but their accepted models
share the following mathematical form. They synthesize finitely many root rules

                             C(ℓi , ri ; oi ),    i = 1, . . . , k,

over constructor patterns. Let NFR (t) mean that every subtree is normal and no
pair root matches a rule input. The carrier becomes

                              TNF (R) = {t ∈ T | NFR (t)}.

On normal inputs, multiplication chooses a matching root-rule output when one
exists and otherwise forms a free pair. Search proves that every possible rule
output is normal and symbolically checks the source under every matching rule
and default-pair case. Overlapping rules need not be confluent: classical choice
selects one output, while the proof covers every selectable constructor. The unary
tower remains normal and therefore proves infinitude.
    For E20034,
                          x ≃ (y ⋄ y) ⋄ ((z ⋄ (x ⋄ x)) ⋄ z),

one root rule suffices:
                              ⟨y, y⟩ ⋄ ⟨⟨z, ⟨x, x⟩⟩, z⟩ 7−→ x.

Normality forces the displayed inner products to be free pairs and the source
contracts at the root. In the clean experiment, completion and CNF each inde-
pendently generated and certified this same one-rule presentation. Across the six
further duality classes in Table 4, accepted CNF presentations use one to thir-
teen root rules; completion covers five of the six classes. CNF also reconstructs
the previously published ALPS pair E19966/E26105. These results illustrate a
complementary model language, but neither they nor the guarded pair enter
the new-classification count. Agreement on a model does not identify the two
enumeration algorithms.
22      J. Zhao et al.

7     Evaluation
The evaluation addresses four questions. First, does each generated object sur-
vive independent Lean checking? Second, what does each search contribute un-
der its stated evaluation scope? Third, does trace synthesis transfer beyond the
Austin identities on which it was developed? Fourth, what capability remains
uncovered by established equational ATPs under the same resource tier? Trace
is the only procedure evaluated on the full Canonical-4187 union and is the only
one compared with the ATPs. Guarded decoding, completion, and CNF search
are reported as targeted regressions of complementary model languages.

7.1   Two source groups and two deduplication levels
We froze two evaluation groups and their SHA-256 hashes before running the
procedures; neither contents nor hashes were changed in response to outcomes.
The first group, Order5-130, is a disjoint union of three order-five subsets:
KnownAustin-10, ten previously known Austin laws; Candidate-96, the 96 iden-
tities listed by ETP as having only trivial finite models and, in the source snap-
shot, no known infinite model; and Open-24, 24 identities for which both finite-
and infinite-model statuses were unresolved in the originating study. The sec-
ond group, ALPS-4141, is the public 4,141-row ALPS evaluation pool, span-
ning orders five through eight [31,32]. For backward compatibility, machine-
readable provenance retains the legacy tags austin96 for Candidate-96 and
generality34 for KnownAustin-10 together with Open-24. These are source
tags, not additional evaluation groups.
    Together the two groups contain 4,271 source rows: 130 in Order5-130 and
4,141 in ALPS-4141. Of the Order5 identities, 83 also occur as ALPS rows.
Retaining one record for each cross-group overlap gives Merged-4188: all 130
Order5 records and 4,058 ALPS-only records. At a second, explicitly different
level, we quotient Merged-4188 by variable renaming and exchange of the two
sides of an equality. Exactly one additional pair, internal to ALPS-4141, collapses
under this equivalence, giving Canonical-4187: 130 Order5 classes and 4,057
ALPS-only classes. Magma duality is not part of this canonicalization; we use it
only to organize mathematical discoveries.
    Unless a sentence explicitly says “source row” or “original ALPS row,” all
full-search and ATP counts below refer to Canonical-4187. The internal ALPS
duplicate belongs to a class solved by trace. Consequently, 624 accepted canonical
classes have an ALPS representative, but they project to 625 accepted rows in the
original 4,141-row file. This convention prevents counts from the two overlapping
source groups from being added as though they were disjoint.
    The tuned trace executable was run afresh on all 4,187 classes in Canonical-
4187. The other executables were rerun only on frozen historical-hit sets: two
problems for guarded decoding, 61 for completion, and 17 for sound CNF search.
These regressions test preservation of known capability and certificate valid-
ity; they are not estimates of coverage on Canonical-4187. Every profile has a
120-second internal search budget, a 125-second outer allowance, a 2,000-MiB
                                                            Trace-Tree Magmas         23

Table 2. Fresh trace result on Canonical-4187. The first three rows are the disjoint con-
stituents of Order5-130; “ALPS-only” is the residual canonical contribution of ALPS-
4141 after cross-group deduplication. The three terminal generation states are exhaus-
tive. “No candidate” and “memory limit” make no mathematical claim about the input.

             Canonical partition   Inputs Accepted No candidate Memory limit
             Candidate-96             96       28           65             3
             KnownAustin-10           10        6            4             0
             Open-24                  24        2           22             0
             Order5-130 subtotal      130      36            91            3
             ALPS-only canonical    4,057     600         3,204          253
             Canonical-4187         4,187     636         3,295          256




process-tree ceiling, and a 1,024,000-byte certificate ceiling in a two-vCPU, 2,048-
MiB sandbox. Search output is counted only when the exact Lean source emitted
for that run has an accepted Judge v3 receipt.


7.2   Independent coverage and certificate validity

Primary trace result. The tuned depth sweep generates 636 certificates, and
Judge v3 accepts all 636. Among the 3,551 unsolved problems, 3,295 terminate
without a candidate and 256 reach the process-tree memory ceiling. These are
outcomes of a bounded search, not counterevidence to the existence of a model.
The largest emitted certificate is 521,804 bytes, below the configured ceiling.
    On Candidate-96, trace generates and certifies 28 new infinite countermod-
els, or fourteen classes under duality. The other 68 problems are unresolved by
this bounded trace run: 65 terminate without a candidate and three reach the
memory ceiling. All 28 identities occur in the published 96-candidate campaign
and were left unresolved by its Vampire procedure [10]. In the released ALPS
data, 24 have null baseline resolution; E4957, E5012, E40917, and E41252 are
absent from the screened pool. The exact-law literature and artifact audit found
no earlier classification for any of the 28.
    Across Order5-130, trace accepts 36 identities. Its three constituent subsets
remain separate in Table 2: Candidate-96 contributes 28; KnownAustin-10 con-
tributes six, namely three known Austin duality classes; and Open-24 contributes
the pair E17260/E28740. The last pair now has certified infinite models but is
not called Austin until its finite side is settled. On the 4,057 ALPS-only classes,
trace accepts 600. A further 24 accepted Candidate-96 identities also occur in
ALPS-4141, so 624 accepted canonical classes have an ALPS representative. The
accepted internal ALPS duplicate makes these 624 classes correspond to 625 rows
of the original pool. This transfer result is evidence that the trace language is
not an encoding of the fourteen new classes by equation identifier.

Supplementary searches. Table 3 deliberately reports the three other search fam-
ilies on their historical-hit regressions. Guarded decoding regenerates and certi-
fies E22619/E22634. The main completion profile generates 60 of its 61 targets:
24      J. Zhao et al.

Table 3. Scope-correct accounting for the four tuned searches. Trace was run on
Canonical-4187, the canonical union of Order5-130 and ALPS-4141. The other rows
are regressions on each method’s historical hit set and therefore do not measure accu-
racy over all of Canonical-4187. “Selected coverage” uses accepted alternate completion
certificates for the four cases not accepted by the main profile.

                                                     Main   Selected Trace
     Search and evaluation scope            Tested accepted accepted overlap
     Trace depth sweep (Canonical-4187)      4,187        636       636         –
     Guarded decoder (historical hits)           2          2         2         0
     Strict completion (historical hits)        61         57        61        38
     CNF NF16 (sound historical hits)           17         17        17         8



Judge accepts 57, while three receive no terminal response before the experi-
ment’s 60-minute client cutoff. It does not generate E9001325. A generalized
schedule accepts that last problem, and an indexed certificate profile accepts the
three client-cutoff cases. These alternatives cover the same completed-rule model
language; they differ in candidate schedule and Lean proof representation. We
therefore count 61 completion problems, not 65 certificates. Sound CNF search
regenerates and certifies all 17 of its targets.
    Across the four selected accepted sets, trace, guarded decoding, completion,
and CNF cover 668 canonical classes in union. Viewed through the two source
groups, this union contains 44 Order5-130 classes and 652 classes having an
ALPS-4141 representative (653 original ALPS rows); these views overlap and
must not be added. The individual selected sets have sizes 636, 2, 61, and
17. Trace contributes 598 classes not covered by a selected supplementary set;
guarded contributes two, completion 21, and CNF seven. The intersections are 38
for trace–completion, eight for trace–CNF, and ten for completion–CNF; eight
problems lie in all three of those sets, and guarded is disjoint from them. Because
only trace was run on all of Canonical-4187, this 668-class union is coverage ac-
counting for the accepted artifacts, not a full-benchmark accuracy estimate for
the supplementary searches.
    The order-five supplemental results clarify what the other model languages
add. Guarded decoding reconstructs the ALPS pair E22619/E22634; CNF recon-
structs the ALPS pair E19966/E26105. These four identities were already classi-
fied and are excluded from the 28-new-identity count. Within the KnownAustin-
10 and Open-24 subsets of Order5-130, completion covers five of the six classes
in Table 4, while CNF covers all six. Trace covers four. The Open-24 pair
E17260/E28740 remains described only as an infinite countermodel.
    Across the public result table there are 731 certificate–profile occurrences:
728 accepted and the three completion client-cutoff records above. This total
includes alternate certificates, cross-family overlap, and twelve archived trace
certificates from an earlier preflight; it is not a solved-problem count. There are
no incorrect, malformed, or other non-timeout Lean rejections. An earlier trace
preflight solved 643 problems, but its later repeat missed twelve of them; their
                                                                  Trace-Tree Magmas          25

Table 4. Supplementary Order5-130 results on six further duality classes. The first five
rows lie in KnownAustin-10; the last lies in Open-24. Trace accepts three known Austin
classes and the class whose two statuses were open; completion covers five classes and
CNF covers all six in their targeted regressions. The last row now has a kernel-checked
infinite model, but its finite-model status remains open.

           Duality class     Prior status          Trace       Completion CNF rules
           E4916 / E41082    known Austin             –         accepted        5
           E15535 / E30591   known Austin             –             –           13
           E17522 / E28770   known Austin         accepted      accepted         2
           E20034 / E25964   known Austin         accepted      accepted         1
           E22455 / E22818   known Austin         accepted      accepted         2
           E17260 / E28740   both statuses open   accepted      accepted         2


Table 5. Same-resource ATP outcomes, with the overlapping source groups kept sep-
arate. “Proofs” are implications to E2, not models. A trusted counter-satisfiable result
is available only from complete Twee; “infinite” is then inferred from an independent
finite-side certificate, not emitted by the ATP. The four ALPS counter rows duplicate
Order5-130 rows. No ATP emitted an explicit model or a Lean-checkable certificate.

                                  Implication   Trusted     Infinite by        No
       Benchmark Tool               proofs    counter-sat. admissibility decisive result
       Order5-130 Vampire 5.0.1             0            0                  0         130
       Order5-130 E 3.5.1                   0            0                  0         130
       Order5-130 Twee complete             2           18                 16         110
       ALPS-4141 Vampire 5.0.1              28             0               0         4,113
       ALPS-4141 E 3.5.1                    54             0               0         4,087
       ALPS-4141 Twee complete              79             4               4         4,058




accepted certificates are retained as a separately labelled fluctuation archive and
are excluded from the fresh count, the primary conclusions, and Table 2.


7.3   Construction-aware ATP comparison

Our same-resource experiment. We ran Vampire 5.0.1 [20], E 3.5.1 [27], and
Twee 2.6.1 [28] independently on both frozen source groups. Every tool received
one 120-second allowance per source row in a two-vCPU, 2,048-MiB sandbox,
with a sampled 2,000-MiB aggregate process-group RSS limit. Vampire used
its CASC portfolio and E used –auto, both in the conjecture-proving direc-
tion. Twee used one parameter-free complete run, twee –tstp –formal-proof
problem.p; the last option retains proof output but does not change the search.
This is one ALPS-aligned completion configuration, not the published eight-
configuration ALPS sweep. Table 5 keeps Order5-130 and ALPS-4141 separate
because 83 Order5 rows recur in the ALPS pool. We compare the ATPs with
trace alone, the only one of our searches run on the full canonical union.
    The result types answer different questions. An implication proof estab-
lishes that the source law forces E2; it is a proof-side result, not a model. Raw
CounterSatisfiable messages from the incomplete Vampire and E proof-mode
runs are retained in the artifact as diagnostics but are not treated as scientific
26      J. Zhao et al.

verdicts. Only a clean terminating saturation from the parameter-free complete
Twee run is counted as trusted counter-satisfiable. Such a result establishes a
nontrivial model of the source law, but does not by itself identify its carrier,
prove it infinite, or provide a Lean certificate.
    After cross-source deduplication and quotienting by variable renaming and
equality symmetry, the three-tool union on Canonical-4187 contains 94 impli-
cation proofs and 18 trusted counter-satisfiable classes, with no conflict. Inde-
pendent finite-side certificates exclude nontrivial finite models for 16 of those 18
classes, so infinitude follows for them; the remaining pair, E17260/E28740, be-
longs to Open-24 and yields only nontrivial-model existence. No ATP run emits
an explicit carrier operation or a Lean-checkable model certificate. By contrast,
trace constructs and Lean-certifies explicit infinite magmas for 636 canonical
classes. Its accepted set is disjoint from the 94-class proof union and overlaps
the 18-class counter-satisfiable union on eight classes. None of the three ATP
runs is decisive on any of the 28 newly classified identities. These are bounded
observations, not impossibility results; the construction comparison concerns the
16 externally justified infinite existences, rather than the aggregate 112 proof-
and model-side statuses.

The published ALPS baseline. Xie et al.’s experiment uses a different proto-
col: an eight-configuration portfolio and a staged per-configuration sweep up
to 600 seconds [32,31]. At the 30-second rung it reports 87 new implication
proofs and four construction-side models; the later rungs add 23 implication
proofs and no models. Thus its largest-budget total is 110 proof-side results and
four model-side results, leaving 4,027 of 4,141 rows unresolved. All four models
come from twee/complete; the Vampire saturation configurations’ resolutions
are implication proofs. ALPS certifies the four model-side cases through finite
presentations and complete saturation, but does not emit an explicit carrier op-
eration as a Lean theorem. We report these published results separately and do
not pool them with our same-resource measurements. They nevertheless rein-
force the same qualitative point: the scarce outcome is a constructed model, not
a proof that an implication holds.

7.4   Feasibility, environment, and artifact
Table 6 reports the algorithmic interval from parsed input through candidate
compilation for accepted records, separate from Judge time.
   The accepted trace models are usually found early: the mean search time is
3.909 seconds, the median is 0.766 seconds, and the maximum is 118.562 sec-
onds. In contrast, the median over all 4,187 Canonical-4187 trace runs is 120.406
seconds because an unsuccessful bounded run normally consumes its allocation.
Peak RSS is sampled rather than read atomically at the enforcing boundary; a
few samples can therefore slightly exceed 2,000 MiB before termination. Judge
time and queue or transport time are recorded separately from search time.
   The experiment used at most 120 reusable sandboxes and at most 48 con-
current Judge calls. The official solver image uses Python 3.11. Receipts identify
                                                               Trace-Tree Magmas        27

Table 6. Search time and sampled peak process-tree RSS. Entries are mean / median
/ maximum; Judge time is excluded. Trace rows come from the fresh full run. Auxiliary
rows are measured only on the targeted regressions of Table 3.

 Profile / scope                         Count     Search time (s)     Peak RSS (MiB)
                                                 Mean Median    Max. Mean Median   Max.
 Trace / Candidate-96 accepted              28  1.29     0.58 10.77 112.8    66.1 823.3
 Trace / KnownAustin-10 accepted             6  0.54     0.57   0.64  64.9   66.0   68.9
 Trace / Open-24 accepted                    2  0.55     0.55   0.56  64.2   64.2   66.2
 Trace / ALPS-only accepted                600  4.08     0.79 118.56 163.6   66.1 1908.3
 Trace / Canonical-4187 accepted           636  3.91     0.77 118.56 160.2   66.1 1908.3
 Guarded / targeted accepted                 2  0.58     0.58   0.59  41.3   41.3   41.3
 Completion (main) / targeted accepted      57 13.95    13.64 43.00 122.9    75.3 1934.8
 CNF / targeted accepted                    17  1.15     1.22   1.73  22.7   23.9   24.5




Judge v3 revision 380d1b2c, Lean 4.33.1, and Mathlib revision 0df444a3. The
artifact records the full combined service name, the complete Mathlib commit,
and the proof policy.
     The release records both frozen source groups (4,271 rows), the 83 cross-
group matches defining Merged-4188, and the additional within-ALPS equiva-
lence defining Canonical-4187. It also contains exact standalone programs for
all selected profiles, per-run results, 731 receipt occurrences, 731 individual cer-
tificate files, and a SHA-256 manifest. Its verifier recomputes the fresh trace
count, supplemental selected coverage, exact intersections, certificate–receipt
pairing, source hashes, Judge revision, and privacy allowlist. A separate same-
resource ATP artifact contains the completed run records, decisive proof streams,
the Canonical-4187 view, tool commands and versions, and its own manifest;
its verifier recomputes the benchmark-separated results, the canonical 94/18
unions, and the absence of contradictory statuses. The public artifacts inten-
tionally exclude controller secrets, sandbox identifiers, private endpoints, and
the full multi-method production solver. The repository is available at https:
//github.com/YanbiaoLab/trace-tree-magmas. Each experiment README
gives a one-command offline verification path; no network access or re-execution
of the search is required for the evidence audit. Re-running the searches and
replaying Lean proofs are documented as separate reproducibility levels rather
than being conflated with hash verification.


8    Related work

Austin and Kisielewicz established and analyzed identities with no nontrivial
finite models [1,2,16,17]. The present work addresses the constructive infinite
half of that classification problem.

Automatic finite and infinite model building. Finite model finders such as Mace4
enumerate bounded domains and are powerful for ordinary equational counter-
models, but a finite table cannot witness the infinite side of an Austin law [22].
28     J. Zhao et al.

Nitpick integrates a relational model finder into Isabelle, supports rich higher-
order syntax, and obtains countermodels through finite scopes [5]. Recent Lean-
oriented counterexample generation similarly produces checked witnesses to false
statements, but does not synthesize an infinite algebra satisfying a universal
magma identity [21].
    Automated infinite-model construction itself has a substantial history. Peltier
represented infinite first-order models by tree automata and regular tree gram-
mars, later constructing non-ambiguous formulae for equational clause sets and
connecting finite and infinite model builders [24,25,26]. Model Evolution lifts
the DPLL view to first-order logic and represents candidate interpretations by
evolving contexts [4]. AGES synthesizes logical models for order-sorted first-
order theories from algebraic interpretations and has both a formal account and
a dedicated implementation [11,12]. More recently, symbolic model construction
has been developed for saturated constrained Horn clauses and for first-order
literal models [8,7], while RInGen searches quantified invariants over algebraic
data types using grammar-based symbolic representations [19]. These lines make
clear that neither automated infinite-model construction nor finite descriptions
of infinite interpretations are first introduced here.
    Elad, Padon, and Shoham provide another genuinely infinite representation:
symbolic structures for satisfiable quantified verification conditions, together
with a model-finding procedure and a decidable fragment for which the rep-
resentation is complete [9]. Trace-tree magmas have a different mathematical in-
terface. They search for one total binary operation on a free constructor algebra.
A source-law trace proposes finitely many Horn rules for exceptional outputs;
descent on constructor size proves that the resulting relation is functional; and
exhaustive case analysis over default pairs and exceptional outputs proves the
universal identity. Our search space and proof requirements are therefore spe-
cialized to equational algebra rather than being an alternative notation for those
general frameworks.

ATP saturation and extracted models. General first-order ATPs such as Vampire
establish many equational implications by refutation [20,14]. A saturated unit-
equational clause set can sometimes be read as a convergent rewrite presentation
of an explicit, possibly infinite model. Janota, Rawson, and Schulz systematize
that construction for Vampire and E and propose certified termination and con-
fluence checks [15]. Their reported study starts from successful saturations in
the order-at-most-four ETP corpus; it does not cover the order-five identities
classified here. Our procedure instead searches the constructor-tree operation
directly and emits its source proof and separating valuation in Lean.
    Against this background, our claim is specific. We introduce rank-decreasing
sparse trace-tree magmas as a model language for magma identities, an auto-
mated procedure that searches this language directly from a source identity,
and a compiler whose output is a self-contained Lean 4 proof of functionality,
universal source validity, carrier infinitude, and target failure.
    Deductive program synthesis also couples search and proof. Hozzová et al.
extend superposition with answer literals to synthesize recursion-free programs
                                                       Trace-Tree Magmas        29

from proofs of functional specifications [13]. Our target is instead a semantic
structure—a total operation on a provably infinite carrier—whose universal law
and countervaluation are Lean-certified; our grammar and obligations therefore
concern model construction rather than program extraction.
    Knuth–Bendix completion and term-rewriting theory motivate free construc-
tors, critical matches, and normal forms [18,3]. Sternagel and Winkler’s verified
certifier checks ordered-completion runs and equational satisfiability certificates
in Isabelle/HOL [29]. That work validates completion-based reasoning; our main
procedure instead synthesizes an exceptional operation from a source evaluation
trace, while the smaller completion variant emits a direct Lean model rather
than an ordered-completion run. The trace family is not merely an orientation
of the source. Its mutually inductive admissible-step relation permits earlier
exceptional evaluations, and the generator must prove the exceptional-output
relation functional.
    ETP combines large-scale automated reasoning with formal verification [6],
while ALPS explores construction-oriented mathematical reasoning [32]. To the
best of our literature and public-artifact audit, no prior work defines or searches
the trace-tree model family above, or compiles discovered members of that family
into self-contained Lean 4 model certificates. Our searches certify 32 order-five
Austin candidates in total. For 28 of them—fourteen classes modulo opposite-
magma duality—they provide the first public infinite countermodels and hence
28 new Austin classifications. The remaining four identities, forming two duality
classes previously reported by ALPS, are independent reconstructions and are
explicitly excluded from that novelty count.


9   Limitations and future work

The trace grammar and its bounded enumeration are intentionally incomplete.
It is strongest for identities orientable as a variable equal to a term and whose
evaluation closes through a small number of exceptional traces. Failure to find a
model proves nothing. In particular, this work does not classify inputs on which a
procedure finishes without a certificate or is stopped by a time or memory limit.
A generated candidate is likewise not evidence until Lean accepts its certificate.
Lean accepts every certificate in the fresh trace run and in the guarded and
CNF regressions. In the main completion regression, three generated certificates
receive no terminal response before the 60-minute client cutoff; accepted indexed
alternatives for the same three problems are supplied, but the original three files
are not counted as accepted. A further generalized schedule covers the main
profile’s one no-candidate case. We make no correctness claim for an unaccepted
file, and the artifact preserves every outcome.
     The one-clause result suggests a mathematical research program. A syntac-
tic criterion for a constructor projection that recovers the output parameter,
together with an acyclic size ranking, could replace mask enumeration by a
theorem for a class of identities. Multiple compatible Horn clauses may cover
terms with several essential branches. Richer constructors or lexicographic ranks
30      J. Zhao et al.

may expose models that the current tree size cannot certify. Finally, the infinite
models for E17260/E28740 motivate a finite-model investigation to determine
whether this pair is Austin.
    At the implementation level, a future verified compiler could reduce the
trusted engineering gap between the Python candidate and its Lean rendering.
The present design instead follows a proof-producing discipline: every output
is independently reconstructed and checked, so compiler bugs cause rejection
rather than unsound acceptance.


10    Conclusion

Trace-tree magmas provide a finite search language for genuinely infinite alge-
braic countermodels. A least relational semantics defines their meaning inde-
pendently of the implementation. For each reported model, a generated Lean
proof uses constructor projection and size descent to establish functionality of
the exceptional-output relation. Complete case analysis over default pairs and
exceptional outputs proves the source identity for every valuation, and a con-
crete countervaluation refutes the target. This theorem chain turns heuristic
search into proof-producing model synthesis without claiming that the search is
complete.
    The method establishes the first public infinite countermodels in our audit
for 28 previously unclassified order-five identities, or fourteen classes modulo du-
ality. Each new class admits a single dependency-respecting Horn clause with at
most two admissible-step premises, revealing a common mathematical structure
rather than 28 unrelated witnesses. Evaluation keeps Order5-130 and ALPS-
4141 distinct: their 4,188-record deduplicated union has 4,187 classes after one
further within-ALPS pair is identified under variable renaming and equality-side
exchange. In a fresh run on those classes, trace produces 636 certificates—36 on
Order5-130 and 600 on the ALPS-only remainder—all accepted by the official
Judge. Of these, 624 canonical classes have ALPS representatives and corre-
spond to 625 rows of the original 4,141-row ALPS pool. Targeted regressions
separately confirm accepted outputs of the guarded, completion, and CNF model
languages without folding their union into the ATP comparison. In the same-
resource experiment, every one of the 28 new cases remains without a decisive
ATP answer. The three ATPs prove implications for 94 canonical classes; only
complete Twee supplies trusted counter-satisfiable results, on 18 classes, and in-
dependent finite-side facts force infinitude for 16 of them. No ATP run produces
an explicit Lean-certified infinite model. These results locate the contribution
at the intersection of automated deduction, explicit model synthesis, and proof
production, and motivate a broader theory of which magma laws admit finite
trace-tree presentations.

Author contributions. Jiaming Zhao generalized the central concept, extracted
the mathematical structure, designed and implemented the algorithms and Lean
                                                            Trace-Tree Magmas          31

certificate generator, ran the large-scale experiments, discovered the new Austin-
law classifications, and wrote the manuscript. Bing Wu developed and main-
tained all experimental infrastructure, including the database, judge-v3-repl
distributed Lean verification service, and Alibaba Cloud Sandbox setup, and
contributed to offline exploration. Xu Miao is the corresponding author.

A     The 32 certified Austin identities
The operation is written as ∗. The first 28 rows are the new classifications.
The final two dual pairs, E19966/E26105 and E22619/E22634, are independent
formal reconstructions of earlier ALPS classifications.
Table 7. The 32 certified Austin identities, grouped by duality. The binary opera-
tion is written as ∗. The first 28 identities are new classifications established by trace
search. The final two pairs were previously classified by ALPS and are independently
reconstructed here by the supplemental searches.
    Law                Identity
    E4952              x ≃ y ∗ (x ∗ (y ∗ (y ∗ (z ∗ y))))
    E41252             x ≃ ((((y ∗ z) ∗ y) ∗ y) ∗ x) ∗ y
    E40914             x ≃ ((((y ∗ x) ∗ y) ∗ z) ∗ x) ∗ z
    E4957              x ≃ y ∗ (x ∗ (y ∗ (z ∗ (x ∗ z))))
    E5012              x ≃ y ∗ (x ∗ (z ∗ (z ∗ (y ∗ z))))
    E41253             x ≃ ((((y ∗ z) ∗ y) ∗ y) ∗ x) ∗ z
    E5066              x ≃ y ∗ (y ∗ (x ∗ (y ∗ (z ∗ y))))
    E41239             x ≃ ((((y ∗ z) ∗ y) ∗ x) ∗ y) ∗ y
    E5141              x ≃ y ∗ (y ∗ (z ∗ (y ∗ (x ∗ y))))
    E40917             x ≃ ((((y ∗ x) ∗ y) ∗ z) ∗ y) ∗ y
    E5295              x ≃ y ∗ (z ∗ (y ∗ (y ∗ (x ∗ y))))
    E40909             x ≃ ((((y ∗ x) ∗ y) ∗ y) ∗ z) ∗ y
    E38303             x ≃ ((y ∗ ((x ∗ z) ∗ x)) ∗ y) ∗ y
    E7701              x ≃ y ∗ (y ∗ ((x ∗ (z ∗ x)) ∗ y))


    Law                Identity
    E7755              x ≃ y ∗ (y ∗ ((z ∗ (x ∗ x)) ∗ y))
    E38249             x ≃ ((y ∗ ((x ∗ x) ∗ z)) ∗ y) ∗ y
    E9345              x ≃ y ∗ ((x ∗ y) ∗ (z ∗ (y ∗ y)))
    E36713             x ≃ (((y ∗ y) ∗ z) ∗ (y ∗ x)) ∗ y
    E9384              x ≃ y ∗ ((x ∗ z) ∗ (y ∗ (z ∗ z)))
    E36714             x ≃ (((y ∗ y) ∗ z) ∗ (y ∗ x)) ∗ z
    E9680              x ≃ y ∗ ((z ∗ y) ∗ (y ∗ (x ∗ y)))
    E36524             x ≃ (((y ∗ x) ∗ y) ∗ (y ∗ z)) ∗ y
    E9667              x ≃ y ∗ ((z ∗ y) ∗ (x ∗ (y ∗ y)))
    E36638             x ≃ (((y ∗ y) ∗ x) ∗ (y ∗ z)) ∗ y
    E35036             x ≃ ((y ∗ z) ∗ ((x ∗ y) ∗ x)) ∗ y
    E11081             x ≃ y ∗ ((x ∗ (y ∗ x)) ∗ (z ∗ y))
    E11116             x ≃ y ∗ ((x ∗ (z ∗ x)) ∗ (y ∗ y))
    E34888             x ≃ ((y ∗ y) ∗ ((x ∗ z) ∗ x)) ∗ y
    E19966             x ≃ (y ∗ y) ∗ ((x ∗ (x ∗ z)) ∗ z)
    E26105             x ≃ (y ∗ ((y ∗ x) ∗ x)) ∗ (z ∗ z)
    E22619             x ≃ (y ∗ (y ∗ x)) ∗ ((z ∗ z) ∗ z)
    E22634             x ≃ (y ∗ (y ∗ y)) ∗ ((x ∗ z) ∗ z)
32      J. Zhao et al.

References
 1. Austin, A.K.: A note on models of identities. Proceedings of the American Math-
    ematical Society 16, 522–523 (1965)
 2. Austin, A.K.: Finite models for laws in two variables. Proceedings of the American
    Mathematical Society 17, 1410–1412 (1966)
 3. Baader, F., Nipkow, T.: Term Rewriting and All That. Cambridge University Press
    (1998). https://doi.org/10.1017/CBO9781139172752
 4. Baumgartner, P., Tinelli, C.: The model evolution calculus as a first-order DPLL
    method. Artificial Intelligence 172(4–5), 591–632 (2008). https://doi.org/10.
    1016/j.artint.2007.09.005
 5. Blanchette, J.C., Nipkow, T.: Nitpick: A counterexample generator for higher-
    order logic based on a relational model finder. In: Interactive Theorem Proving.
    Lecture Notes in Computer Science, vol. 6172, pp. 131–146. Springer (2010). https:
    //doi.org/10.1007/978-3-642-14052-5_11
 6. Bolan, M., et al.: The equational theories project: Advancing collaborative math-
    ematical research at scale. arXiv preprint arXiv:2512.07087 (2025). https://doi.
    org/10.48550/arXiv.2512.07087
 7. Bromberger, M., Krasnopol, F., Möhle, S., Weidenbach, C.: First-order automatic
    literal model generation. In: Automated Reasoning – IJCAR 2024. Lecture Notes
    in Computer Science, vol. 14739, pp. 133–153. Springer (2024). https://doi.org/
    10.1007/978-3-031-63498-7_9
 8. Bromberger, M., Leutgeb, L., Weidenbach, C.: Symbolic model construction for
    saturated constrained Horn clauses. In: Frontiers of Combining Systems. Lecture
    Notes in Computer Science, vol. 14279, pp. 137–155. Springer (2023). https://
    doi.org/10.1007/978-3-031-43369-6_8
 9. Elad, N., Padon, O., Shoham, S.: An infinite needle in a finite haystack: Find-
    ing infinite counter-models in deductive verification. Proceedings of the ACM on
    Programming Languages 8(POPL), 970–1000 (2024). https://doi.org/10.1145/
    3632875
10. Equational Theories Project contributors: Order 5 austin laws. Equational The-
    ories Blueprint, Chapter 20 (2026), https://teorth.github.io/equational_
    theories/blueprint/order-5-austin-laws.html, snapshot accessed 1 Septem-
    ber 2026; exact hash archived with the artifact
11. Gutiérrez, R., Lucas, S.: Automatic synthesis of logical models for order-sorted
    first-order theories. Journal of Automated Reasoning 60(4), 465–501 (2018).
    https://doi.org/10.1007/s10817-017-9419-3
12. Gutiérrez, R., Lucas, S.: Automatic generation of logical models with AGES. In:
    Automated Deduction – CADE 27. Lecture Notes in Computer Science, vol. 11716,
    pp. 287–299. Springer (2019). https://doi.org/10.1007/978-3-030-29436-6_17
13. Hozzová, P., Kovács, L., Norman, C., Voronkov, A.: Program synthesis in sat-
    uration. In: Automated Deduction – CADE 29. Lecture Notes in Computer
    Science, vol. 14132, pp. 307–324. Springer (2023). https://doi.org/10.1007/
    978-3-031-38499-8_18
14. Janota, M.: Experimental results for Vampire on the equational theories
    project. arXiv preprint arXiv:2508.15856 (2025). https://doi.org/10.48550/
    arXiv.2508.15856
15. Janota, M., Rawson, M., Schulz, S.: Case study: Saturations as explicit models
    in equational theories. arXiv preprint arXiv:2602.16324 (2026). https://doi.org/
    10.48550/arXiv.2602.16324
                                                             Trace-Tree Magmas          33

16. Kisielewicz, A.: Varieties of algebras with no nontrivial finite members. In: Lattices,
    Semigroups, and Universal Algebra, pp. 129–136. Plenum Press, New York (1990).
    https://doi.org/10.1007/978-1-4899-2608-1_14
17. Kisielewicz, A.: Austin identities. Algebra Universalis 38(3), 324–328 (1997).
    https://doi.org/10.1007/s000120050057
18. Knuth, D.E., Bendix, P.B.: Simple word problems in universal algebras. In: Com-
    putational Problems in Abstract Algebra, pp. 263–297. Pergamon Press (1970).
    https://doi.org/10.1016/B978-0-08-012975-4.50028-X
19. Kostyukov, Y., Mordvinov, D., Fedyukovich, G.: Beyond the elementary represen-
    tations of program invariants over algebraic data types. In: Proceedings of the 42nd
    ACM SIGPLAN International Conference on Programming Language Design and
    Implementation. pp. 451–465. ACM (2021). https://doi.org/10.1145/3453483.
    3454055
20. Kovács, L., Voronkov, A.: First-order theorem proving and Vampire. In: Com-
    puter Aided Verification. Lecture Notes in Computer Science, vol. 8044, pp. 1–35.
    Springer (2013). https://doi.org/10.1007/978-3-642-39799-8_1
21. Li, Z., Li, Z., Yang, K., Ma, X., Su, Z.: Learning to disprove: Formal counterexample
    generation with large language models. arXiv preprint arXiv:2603.19514 (2026).
    https://doi.org/10.48550/arXiv.2603.19514
22. McCune, W.: Mace4 reference manual and guide. Tech. Rep. ANL/MCS-TM-264,
    Argonne National Laboratory (2003), https://www.cs.unm.edu/~mccune/mace4/
    mace4.pdf
23. de Moura, L., Ullrich, S.: The Lean 4 theorem prover and programming lan-
    guage. In: Automated Deduction – CADE 28. Lecture Notes in Computer
    Science, vol. 12699, pp. 625–635. Springer (2021). https://doi.org/10.1007/
    978-3-030-79876-5_37
24. Peltier, N.: Tree automata and automated model building. Fundamenta Informat-
    icae 30(1), 59–81 (1997). https://doi.org/10.3233/FI-1997-30105
25. Peltier, N.: Building infinite models for equational clause sets: Constructing non-
    ambiguous formulae. Logic Journal of the IGPL 11(1), 97–129 (2003). https:
    //doi.org/10.1093/jigpal/11.1.97
26. Peltier, N.: Automated model building: From finite to infinite models. In: Intelligent
    Computer Mathematics. Lecture Notes in Computer Science, vol. 5144, pp. 155–
    169. Springer (2008). https://doi.org/10.1007/978-3-540-85110-3_13
27. Schulz, S.: E—a brainiac theorem prover. AI Communications 15(2–3), 111–126
    (2002). https://doi.org/10.3233/EAI-2002-260
28. Smallbone, N.: Twee: An equational theorem prover. In: Automated Deduction –
    CADE 28. Lecture Notes in Computer Science, vol. 12699, pp. 602–613. Springer
    (2021). https://doi.org/10.1007/978-3-030-79876-5_35
29. Sternagel, C., Winkler, S.: Certified equational reasoning via ordered com-
    pletion. In: Automated Deduction – CADE 27. Lecture Notes in Computer
    Science, vol. 11716, pp. 508–525. Springer (2019). https://doi.org/10.1007/
    978-3-030-29436-6_30
30. The mathlib Community: The Lean mathematical library. In: Proceedings of the
    9th ACM SIGPLAN International Conference on Certified Programs and Proofs.
    pp. 367–381. ACM (2020). https://doi.org/10.1145/3372885.3373824
31. Xie, E., Ye, W., Zhang, A.: ALPS complete automated-baseline results and evalu-
    ation pool. GitHub repository data release (2026), https://github.com/EricX22/
    ALPS, gitHub commit e831af76da02; accessed 1 September 2026
34     J. Zhao et al.

32. Xie, E., Ye, W., Zhang, A.: ALPS: Measuring valid creativity in large language
    models with mathematical construction. arXiv preprint arXiv:2608.15979 (2026).
    https://doi.org/10.48550/arXiv.2608.15979
