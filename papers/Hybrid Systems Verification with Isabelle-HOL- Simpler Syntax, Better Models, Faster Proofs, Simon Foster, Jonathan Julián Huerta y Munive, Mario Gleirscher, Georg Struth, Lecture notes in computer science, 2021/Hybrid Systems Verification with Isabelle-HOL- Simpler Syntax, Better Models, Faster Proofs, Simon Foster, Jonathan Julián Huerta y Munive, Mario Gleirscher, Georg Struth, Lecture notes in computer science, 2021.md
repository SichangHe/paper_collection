                                         Hybrid Systems Verification with Isabelle/HOL:
                                          Simpler Syntax, Better Models, Faster Proofs

                                                       Simon Foster1 , Jonathan Julián Huerta y Munive2 ,
                                                             Mario Gleirscher3 , and Georg Struth4
                                                                        1
                                                                          University of York, UK
                                                                2
                                                                    University of Copenhagen, Denmark
                                                                    3
                                                                      University of Bremen, Germany
                                                                      4
                                                                        University of Sheffield, UK
arXiv:2106.05987v1 [cs.LO] 10 Jun 2021




                                               Abstract. We extend a semantic verification framework for hybrid sys-
                                               tems with the Isabelle/HOL proof assistant by an algebraic model for
                                               hybrid program stores, a shallow expression model for hybrid programs
                                               and their correctness specifications, and domain-specific deductive and
                                               calculational support. The new store model yields clean separations and
                                               dynamic local views of variables, e.g. discrete/continuous, mutable/im-
                                               mutable, program/logical, and enhanced ways of manipulating them us-
                                               ing combinators, projections and framing. This leads to more local infer-
                                               ence rules, procedures and tactics for reasoning with invariant sets, cer-
                                               tifying solutions of hybrid specifications or calculating derivatives with
                                               increased proof automation and scalability. The new expression model
                                               provides more user-friendly syntax, better control of name spaces and in-
                                               terfaces connecting the framework with real-world modelling languages.


                                         1   Introduction
                                         Deductive verification of hybrid systems with interactive proof assistants like
                                         Coq, HOL or Isabelle is currently gaining traction [1–8]. Such tools have reached
                                         a level of maturity, proof power, and mathematical library support that makes
                                         the development of formal methods fast, dependable and competitive. With
                                         Isabelle/HOL, an impressive theory stack for ordinary differential equations
                                         (ODEs) [9] has been combined with algebras of programs and concrete hy-
                                         brid program semantics into a semantic framework for reasoning about hybrid
                                         systems [4]. Its development has so far focused on mathematical groundwork,
                                         exploring Isabelle’s mathematical and theory engineering facilities, supporting
                                         verification workflows for hybrid systems, and implementing a tool prototype.
                                             Here we report on its transformation into a formal method: (1) We supply
                                         a better hybrid program store model to reason about discrete and continuous,
                                         mutable and immutable, logical and program variables more succinctly (§3). It
                                         supports local reasoning about parts of stores through projection and framing
                                         techniques, and generation of fresh variables [10]. (2) Using this model, we de-
                                         rive deductive and calculational rules for hybrid system verification, including
                                         inference rules à la differential dynamic logic (dL) [11] (§5). Rules are enhanced
2       Foster, Huerta y Munive, Gleirscher, Struth

with framing conditions for local reasoning about mutable continuous variables.
We supply a new ghost rule for invariant sets, a new frame rule à la separa-
tion logic, and more effective tactics, for instance for calculating framed Fréchet
derivatives (§6). (3) Using Isabelle’s syntax translation mechanisms we create a
simpler modelling and specification language within the shallow embedding of
our framework (§4). It is meant to be extensible to modelling languages such
as Modelica and computer algebra systems such as Mathematica. These con-
tributions are explained through examples (§7); additional ones are highlighted
throughout the article. Next we outline the main features of the framework to
contextualise these contributions and prepare for the technical sections.
    The framework [4] has been formalised as a shallow embedding using Is-
abelle’s own language and types. The benefits of shallowness are well docu-
mented [12,13]. A drawback addressed by our expression model is that syntactic
properties, for instance of mutable variables, may be hard to capture. The frame-
work has three semantic layers that can be modified compositionally: abstract
algebras of programs are used for deriving structural program transformation
laws and verification condition generation (VCG) [14] by equational reasoning.
Isabelle’s type polymorphism allows their instantiation, for example with state
transformer semantics and further with concrete semantics of hybrid program
stores—the level at which basic commands such as assignments are modelled.
The store extension to hybrid programs is obtained by a state transformer se-
mantics for basic (continuous) evolution commands. As in dL, these commands
specify ODEs (via vector fields) and guards imposing boundary conditions on
their state spaces. The associated state transformer then maps initial states
of evolutions to their guarded orbits, or more general sets of reachable states.
Hybrid stores were modelled so far [4] as real-valued functions from program
variables, using Rn with a fixed finite set of natural numbers as variable names
for technical reasons. Our new hybrid store model supports more general name
spaces, dynamic stores and other implementations via records or monads.
    Users of the framework need to specify hybrid programs and standard cor-
rectness specifications using pre/postconditions and loop invariants. Two main
workflows are then supported: (1) If ODEs have unique solutions, one can cer-
tify them or rely on automatic certifications in special cases [8, 15], then trigger
automatic VCG and discharge the remaining verification conditions (VCs) by
reasoning about solutions in state spaces. (2) More generally, one can assert
invariant sets [16] for ODEs, trigger VCG and then reason abstractly about
these invariants to discharge the VCs. So far, these two workflows have relied
on Isabelle’s internal support for equational reasoning, which seems natural for
mathematicians or engineers. Our new components make them more automatic
by reasoning locally with certification conditions, invariant assertions or deriva-
tives, and more structured by supporting data-level reasoning with invariants
using the derived dL-style inference rules, for those who prefer this approach.
Capturing fresh variables is instrumental for our new dL-inspired ghost rule; pro-
jecting on mutable variables simplifies proof obligations and localises reasoning
about such variables as does separation logic, but by different means.
                             Hybrid Systems Verification with Isabelle/HOL       3

    The general framework has been tested successfully on a large set of hybrid
verification benchmarks [17]; our new components, integrated into an accessible
simplified version of the framework, can be found online5 .


2     Semantic Preliminaries

We first recall the basics of state and predicate transformers, the semantics
of evolution commands and the set-up for our new hybrid store model [4, 18].
The semantics can be motivated using the hybrid program syntax of dL [11],
X ::= x := e | x0 = f & G |?P | X ; X | X + X | X ∗ , which, beyond
standard constructs of dynamic logic, features an evolution command x0 = f & G.
It specifies a vector field f : T → S → S with time domain T over a state space
S and a guard G : S → B, a predicate modelling boundary conditions.
State and predicate transformers. We model programs as state transform-
ers α : S → PS, arrows of the Kleisli
                                  S category of the powerset monad. (Forward)
Kleisli composition (α◦K β) x = {β y | y ∈ α x} models sequential composition,
the program skip is the monadic unit ηS x = {x}, abortSis λx. ∅, nondetermin-
istic choice ∪ on functions and finite iteration α∗ x = i∈N αi x, with powers
defined using ◦K . Tests (and assertions) are subidentities (functions P ≤ ηS ,
with ≤ extended pointwise) mapping any x ∈ S either to {x} or ∅. They are
isomorphic to sets and predicates. Deterministic functions S → S are embed-
ded into S → PS via hαi = ηS ◦ α. Backward diamond operators (disjunctive
predicate transformers with contravariant composition) are Kleisli extensions of
state transformers, forward box or wlp operators are their right adjoints on the
boolean algebra of tests: wlp α Q = {x | α x ⊆ Q} for any program α and test
Q. We often write partial correctness assertions P ⊆ wlp α Q as {P } α {Q}.
    The laws of propositional Hoare logic (ignoring assignments) are derivable
in this semantics. Nevertheless, VCG with wlp (α ◦K β) = wlp α ◦ wlp β and
wlp (if P then α else β) Q = (P ∪ wlp α Q) ∩ (P ∩ wlp β Q) is more effective, while
the standard Hoare rule can be used for loops decorated with invariants.
Continuous dynamics. The evolution of continuous systems [16] is often mod-
elled by (local) flows ϕ : T → S → S, where T ⊆ R models time and S a state
space. Flows are assumed to be C 1 -functions, and monoid actions if T = R:
ϕ(t + t0 ) = ϕ t ◦ ϕ t0 and ϕ 0 = id S . A trajectory ϕs : T → S of ϕ at s ∈ S is
then a curve ϕs t = ϕ t s, and its orbit at s ∈ S is given by state transformer
γ ϕ : S → PS, s 7→ P ϕs T , which maps any state s to the set of states on the
trajectory passing through it. Flows are typically solutions to initial value prob-
lems for systems of ODEs, which specify a vector field f : T → S → S assigning
vectors to points in space-time, and an initial value s ∈ S at t0 ∈ T . A solu-
tion is then a C 1 -function X that satisfies X 0 t = f t (X t) and X t0 = s. For f
continuous, existence of X is guaranteed by the Peano theorem. Yet f must be
Lipschitz continuous to guarantee uniqueness via the Picard-Lindelöf theorem,
5
    github.com/isabelle-utp/Hybrid-Verification, also clicking our     icons.
4       Foster, Huerta y Munive, Gleirscher, Struth

which provides intervals U s ⊆ T where solutions exist around t0 for each s ∈ S
and gives rise to flows when t0 = 0.
Semantics of evolution commands. Orbit maps γ ϕ : S → PS are state
transformers, but we generalise to include guards and to continuous vector fields.
Our state transformer for evolution commands maps each state s ∈ S to the set
of reachable states (or generalised orbit)
(x0 = f & G) s = {X t | t ∈ U s∧(∀τ ∈↓U s t. G(X τ ))∧X 0 t = f t (X t)∧X t0 = s},
where ↓U s t is the down-closure of t in U s, such that t0 ∈ U s. It constrains the
domain of existence of the solutions X. If we know the flow ϕ for f , then this
semantics reduces to (x0 = f & G) s = {ϕ t s | t ∈ U s ∧ (∀τ ∈ ↓U s t. G(ϕ τ s))}.
    This state transformer maps any s ∈ S to all reachable states along any
solution to f . Thus wlp (x0 = f & G) Q holds iff for every t ∈ U s, if G (X τ )
holds for all τ ∈ ↓U s t, then Q (X t) holds as well. Computing wlp’s within the
remits of Picard-Lindelöf is then straightforward: users only need to supply and
certify the flow ϕ within the first workflow outlined in §1.
Invariant sets. Instead of analytic solutions, one can use the generalised orbit
semantics in combination with generalised invariant sets in the second workflow.
Invariant sets [16] are preserved by the orbit map of the dynamical system.
With guards, more generally, I ⊆ S is an invariant set of (x0 = f & G) whenever
(x0 = f & G)† I ⊆ I, where (−)† indicates Kleisli extension and yields a backward
modal diamond operator. The adjunction mentioned translates this property
into I ⊆ wlp (x0 = f & G) I, the standard format for invariance reasoning with
predicate transformers [4]. Intuitively, such invariants characterise regions of
the state space that contain all orbits that respect G and have a point inside
them. It then suffices to assert suitable invariants in order to verify a correctness
specification. We discuss invariance techniques for evolution commands in §5.
Lenses. Our algebraic model for hybrid stores is based on lenses [18, 19], a
tool for manipulating program stores or state spaces, which comes in many
variants and guises [20–22], in support of algebraic reasoning about program
variables [18, 23] and local reasoning about store shapes [10].
   A lens λ : V ⇒ S is a pair (getλ : S → V, putλ : V → S → S) such that
    getλ (putλ v s) = v,     putλ v ◦ putλ v 0 = putλ v,     putλ (getλ s) s = s,
for all v ∈ V and s ∈ S. Lenses are arrows in a category, as explained in §3 below.
They admit many interpretations. Typically, S is a set of program stores. Yet V
could be a smaller or simpler set of stores, get s could forget part of s ∈ S and
put v s overwrite part of s with v ∈ V. Otherwise, V could be a value domain,
get s could look up a value v in s and put v s could update s with v.
    We use variable lenses x : V ⇒ S to model program variables x, getx s to
look up values in V in stores s and putx v s to update values in s by v. They can
be implemented differently as concrete stores [23]. A variable assignment x := e,
with expression e represented semantically as a function S → V, is then a state
transformer (x := e) = hλs. putx (e s) si, and wlp (x := e) Q = λs. Q (putx (e s) s).
This suffices for VCG for hybrid programs without evolution commands.
                                Hybrid Systems Verification with Isabelle/HOL             5

3    Hybrid Store Components
Lenses enhance our hybrid store models. They provide a unifying interface for
heterogeneous variables, allow modelling frames, i.e., sets of mutable variables,
and projecting parts of the global state to vector spaces of continuous evolutions.
These projections are based on three lens combinators: composition, sum and
quotient. This makes reasoning about hybrid stores local.
States and variables. Many modelling and programming languages support
modules with local variable and constant declarations. We have implemented an
Isabelle command that automates the creation of hybrid stores.
dataspace sys =
  constants c1 ::C1 ..cn ::Cn assumes a1 :P1 ..an :Pn variables x1 ::T1 ..xn ::Tn
It has constants ci : Ci , named constraints a1 : Pi and state variables xi : Ti .
Inside, we can create local definitions, theorems and proofs, which are hidden,
but accessible using its namespace. Internally, a locale with fixed constants and
assumptions is created. Each variable is a lens xi : Ti ⇒ S, using abstract store
S with the lens axioms as locale assumptions. We also generate independence
assumptions [18] that distinguish different variables semantically. Lenses λ, λ0 :
V ⇒ S are independent, λ ./ λ0 , if putλ u ◦ putλ0 v = putλ0 v ◦ putλ u, for all
u, v ∈ V, that is, their actions commute on all states.
Substitutions. We obtain cleaner program specifications with the notation
σ(x     e) = λs. putx (e s) (σ s). With this, we can describe assignments as se-
quences of updates: for variable lenses xi : Vi ⇒ S and “expressions” ei : S → Vi ,
[x1     e1 , x2  e2 , · · · ] = id(x1 e1 )(x2        e2 ) · · · . Implicitly, any variable y
not mentioned in such a semantic “substitution” σ : S → S is left unchanged:
y    y. We write e.g. e[v/x] = e ◦ [x       v] for the application of substitutions to
expressions. These notations unclutter program specifications significantly, e.g.
(x := e) = h[x        e]i and wlp h[x       e]i Q = Q[e/x]. Crucially, the Isabelle
simplifier can reorder and reduce substitutions to support syntactic manipu-
lation of variables during VCG [18]. We can extract assignments for x with
hσis x = getx ◦ σ, and so e.g. h[x    e1 , y     e2 ]is x reduces to e1 when x ./ y.
Vectors and matrices. The lens category admits a forward lens composition
λ1 # λ2 : S1 ⇒ S3 , for λ1 : S1 ⇒ S2 , λ2 : S2 ⇒ S3 and units 1S : S ⇒ S [18, 22].
We do not reproduce the formal definition. Intuitively, # selects a part of a larger
store shape, as we will shortly demonstrate.
    Vectors and matrices are supported by HOL-Analysis. We supply notation
[[x11,...,x1n],...,[xm1,...,xmn]] for matrices and means for accessing co-
ordinates of vectors via hybrid program variables [24]. We view vectors in Rn as
part of larger hybrid stores, hence as lenses Rn ⇒ S, and project onto coordinate
vk of any vector v in Rn using lens composition and a vector lens for vk .

Π(k : [n]) = ((λs. vec-nth s k) : An → A, (λv s. vec-upd s k v) : A → An → An ),

where [n] = {1..n}, An ∼
                       = [n] → A, and the lookup function vec-nth and update
function vec-upd come from HOL-Analysis. Then, for example, vx = Π(1) # v and
6       Foster, Huerta y Munive, Gleirscher, Struth

vy = Π(2) # v for v : R2 ⇒ S, using # to first select the variable v and then the
vector-part of the hybrid store. Obviously, Π(i) ./ Π(j) iff i 6= j.
   We can specify ODEs and flows via substitutions: [p v, v a, a 0], e.g.,
specifies a vector field for lenses p, v, a : R2 ⇒ S. Though ostensibly syntactic
objects, these substitutions are semantically functions S → S, and consequently
can be used with Isabelle’s ODE components [25, 26].
Frames. Lenses support algebraic manipulations of variable frames. A frame is
a set of variables that may be mutated by a program within a given context. We
first show how variable sets can be modelled via lens sums. Then we define a
predicate that characterises the immutable variables for programs [27]. Equipped
with this we derive a frame rule in the style of separation logic that embodies
local reasoning with framed variables.
    Variable lenses can be combined into lenses for variable sets with lens sum [18]
λ1 ⊕ λ2 : V1 × V2 ⇒ S = (λ(s1 , s2 ). (getλ1 , getλ2 ), putλ1 ◦ putλ2 ), which is defined
for λ1 : V1 ⇒ S, λ2 : V2 ⇒ S if λ1 ./ λ2 . This combines two independent lenses,
and can model composite variables, e.g. (x, y) = x⊕y, which can be decomposed
by the simplifier: [(x, y) (e1 , e2 )] = [x e1 , y e2 ]. We can also use it to specify
finite sets: {x, y, z} as x ⊕ (y ⊕ z), yet each each variable in the sum may have
a different type, e.g. {vx , p} is a valid and well-typed construction.
    Sums of lenses cannot be directly related with sets: they are only associative
and commutative up-to isomorphism of cartesian products. We thus define a lens
preorder [18], λ1  λ2 ⇔ ∃λ3 . λ1 = λ3 # λ2 that captures the part-of relation
between λ1 : V1 ⇒ S and λ2 : V2 ⇒ S, e.g. vx ≤ v and p ≤ p ⊕ v. Lens
equivalence = ∼ =  ∩  then identifies lenses that have the same shape in the
store. Then, for variable set lenses up-to ∼   =, ⊕ models ∪, ./ models ∈,     / and 
models ⊆ or ∈, which we can use to construct variable frames.
    Let A : V ⇒ S be a lens modelling a variable set. For s1 , s2 ∈ S let
s1 ≈A s2 hold if s1 = s2 up-to the values of variables in A. For α : S ⇒ PS
define α nmods A ⇔ ∀s1 ∈ S s2 ∈ α s1 ⇒ s1 ≈A s2 , i.e., the mutable vari-
ables in α are not in A. Then (x := e) nmods A whenever x ./ A and, recur-
sively, (α # β) nmods A and (if P then α else β) nmods A when α nmods A and
β nmods A. Also, A ≤ B and α nmods B implies that α nmods A.
    Similarly, we use lenses to describe when a variable does not occur freely in
an expression or predicate as A ] e ⇔ ∀v. e (putA v) = e [18]. We can now derive
a variant of separation logic’s frame rule, which epitomises local reasoning:

            α nmods A ∧ (−A) ] I ∧ {P } α {Q} ⇒ {P ∧ I} α {Q ∧ I}                    (1)

Projections. Reasoning with frames often requires localising variables to part
of the store. In particular, in §5 we partition the store into continuous and
discrete parts, and localise continuous variables to the former to describe their
derivatives. Formally, we may use a frame lens A : C ⇒ S from the global store
S onto a local store C. Local reasoning within A requires lens quotient [10], λ A,
which localises a lens λ : T ⇒ S to a lens T ⇒ C. Assuming λ  A, it obtains
λ1 : T ⇒ C such that λ = λ1 # A. For example, vx v = Π(1) with C = Rn .
                              Hybrid Systems Verification with Isabelle/HOL          7

Quotient cannot be defined by, e.g. λ # B for B : S ⇒ C, since C is smaller than
S, and so B cannot satisfy the lens axioms.


4    Shallow Expressions Component

Next we present our new expression component for Isabelle that supports seam-
less transformations between the intuitive expression syntax often used in verifi-
cation approaches and the functions S → V mimicking them in our shallow em-
bedding. Naive uses of such functions may pollute specifications with λ-binders,
e.g. requiring λs. getx s + gety s instead of x + y. Isabelle’s syntax translations
allow relating syntactic and semantic representations, and ultimately designing
interfaces to modelling languages such as Modelica and Matlab.
Syntax translation. Isabelle implements a multi-stage syntax pipeline. Uni-
code strings are parsed and transformed into “pre-terms” [28]: elements of the
ML term type containing syntactic constants. These must be mapped to pre-
viously defined semantic constants by syntax translations, before they can be
checked and certified in the Isabelle kernel. Printing reverses this pipeline, map-
ping terms to strings. The pipeline supports a host of syntactic constructions.
    We reuse this pipeline with small modifications for our bidirectional expres-
sion transformation, including pretty printing. We subject pre-terms to a lifting
process, which replaces free variables and constants, and inserts store variables
(s) and λ-binders. Its implementation uses the syntactic annotation (t)e to lift
the syntactic term t to a semantic expression in the syntax translation rules
                           (
                             λs. getx s if x is a lens
   (t)e  [(t) ]e , (x)
             e        e
                                                         (f t)e     λs. f ((t)e s),
                             λs. x       otherwise

where p       q means that pre-term p is translated to term q, and q printed as p.
Moreover, [−]e is a constant that marks lifted expressions that are embedded in
terms. The pretty printer can then recognise a lifted term and print it.
     Intuitively, (t)e is processed as follows. The syntax processor first parses a
pre-term from string t. Then our parse translation traverses its syntax tree.
Whenever it encounters a free variable x, the type system determines from the
context whether it is a lens, in which case a getx is inserted. Otherwise it is
left unchanged as a logical variable. Function applications are left unchanged by
   , except for expression constructs like e[v/x]. For program variables x and y
and logical variable z, e.g., ((x + y)2 /z)e     [λs. (getx s + gety s)2 /z]e . Once an
expression has been processed, the resulting λ-term is enclosed in [−]e .
     In assignments x := e and substitutions [x          e], e is lifted transparently
without user annotations. We can also lift correctness specifications and allow
intuitive parsing of assertions: {P } α {Q}       (P )e ≤ wlp α (Q)e .
Substitution. Though our expressions are functions, we can mimic syntactic
substitution using the rule (λs. e(s))e [v/x] = (λs. e(putx (v s) s))e . This pushes
the substitution through the expression marker, by applying an update to the
8       Foster, Huerta y Munive, Gleirscher, Struth

store. This rule preserves the lifted syntax, e.g. ((x + y)2 /c)e [2 · x/y] simplifies
to ((3 · x)2 /c)e . We can also use substitutions to determine whether a variable is
used: (x ] e) ⇔ ∀v. (e[v/x]) = e: e does not depend on x if substituting any value
v for it leaves e (§3). For example, (5)e [v/x] = (5)e , and thus x ] 5. Checking ] is
usually automatic. More generally, lenses provide enough structure for simulating
many standard syntactic manipulations semantically to support VCG.


5    Dynamical Systems Components

We extend our components for the continuous dynamics with a notion of function
framing that projects to parts of the store as outlined in §3. This supports
local reasoning where evolution commands modify only continuous variables and
leave discrete ones—outside the frame—unchanged. We also introduce framed
differentiation to calculate differential invariants equationally, and derive a ghost
rule [11] that expands ODEs with fresh variables.
Framed vector fields. We fix the continuous part C of hybrid store S with
suitable topological structure for continuous variables and vector fields (e.g. Rn )
and supply a lens λ : C ⇒ S = (putλ : C → S → S, getλ : S → C). We can
compose this data with any f : S → S—frame it with λ—to fλ : S → C → C such
that fλ s = getλ ◦f ◦(λv. putλ v s). For C ⊆ S, fλ s is thus the restriction of f to C
supplied with the full store s before restriction. For example for S = R2 ×R2 ×S 0 ,
λ : R2 × R2 ⇒ S = (p ⊕ v) frames f : S → S = [(p, v)           (v, 0)] which behaves
as the identity function on S 0 , and thus fλ s : R2 × R2 → R2 × R2 . Similarly, if
f : T → S → S is a vector field and s ∈ S, then λt. (f t)λ s : T → C → C is the
framed vector field fλ for f and s. We can supply f as a substitution λt. [x       e t]
that describes the ODEs x 0 t = e t quite naturally, after framing.
Specifying evolution commands. We have formalised the generalised orbits
in the semantics for x0 = f & G in §2 as g-orbital [4]. Here we add a framed ver-
sion, g-orbital-on λ f G U S t0 : S → P S defined as the image under (λv. putλ v s)
of g-orbital applied to fλ , (λv. G (putλ v s)), U , S, t0 , and (getλ s), where S ⊆ C
is the codomain of fλ . The application of g-orbital to fλ makes it a state trans-
former on C, while its image under (λv. putλ v s) lifts it back to S. VCG with
the first workflow and g-orbital-on then remains as outlined in §1. Users need to
supply flows and constants for Lipschitz continuity in order to obtain wlp’s as in
§2. We provide tactics that may automate this process in §6.
    With Isabelle’s syntax translations, we can specify g-orbital-on naturally as
{x01 = e1 , x02 = e2 , · · · , x0n = en | G on U S @ t0 }, where each xi is a summand
of the lens {x1 , · · · , xn }. We use this notation in all our examples of §7. Users
can thus declare the ODEs in evolution commands coordinate-wise with lifted
expressions ei ranging over S, and the other parameters G, U , S and t0 which
can be omitted. Their omission defaults them to constantly true, {t. t ≥ 0}, C
and 0 respectively. We can often collapse further to (x01 , · · · , x0n ) = (e1 , · · · , en )
and obtain the following framing result: {x 0 = e | G on U S @ t0 } nmods (−x),
as variables outside of x do not change during evolution and hence, by (1) in
                                 Hybrid Systems Verification with Isabelle/HOL          9

§3, any I specified only over discrete variables is an invariant (see (12) be-
low). We can also specify evolutions using flows with the following notation
{EVOL (x1 , · · · , xn ) = (e1 τ, · · · , en τ ) | G}, which also carries a frame.
Framed derivatives. Isabelle supports Fréchet derivatives and we are localis-
ing them by framing. These derivatives are defined for functions between normed
vector spaces or Banach spaces. Recall that, for a Fréchet differentiable function
F : C → T at s ∈ C, with C ⊆ S open and S, T Banach spaces, its derivative
D F s is a continuous linear operator in C → T [29]. If F is differentiable every-
where, D F : C → L(C, T ), where L(C, T ) is the subspace of continuous linear
operators in C → T . For finite-dimensional spaces, D F s is the Jacobian of F
at a; compositions with unit vectors yield partial derivatives and the sum over
these along the coordinates of a vector yield directional derivatives.
    Fix e : S → T with restriction e|sA : C → T = e ◦ (λv. putA v s) differentiable
everywhere, variable set lens A and function f : S → S. The Fréchet derivative
LfA (e) : S → T of e at s framed by A in direction f is then defined as

                        LfA (e) s = D e|sA (getA s) (getA (f s)).

Here, getA (f s) is a vector in C. Intuitively, in the finite dimensional case,
D e|sA (getA s) : C → S corresponds to a Jacobian and getA (f s) the vector
associated by f to s in C along which the directional derivative is taken. From the
user perspective, after framing, f supplies the vector field fA representing the
ODEs, s the values of the discrete variables, and e, the expression to differentiate.
Computing framed derivatives. We can calculate framed derivatives equa-
tionally. For lenses x : V ⇒ S, A : C ⇒ S, function f : S → S, and expressions
k, e1 , e2 : S → T , which when framed by A become everywhere differentiable,

            LfA (k) = 0                                                    if A ] k    (2)
            LfA (x) = 0                                                  if x ./ A     (3)
            LfA (x) = hf is x           if x  A and x         A is bounded linear     (4)
       f                 f           f
      LA (e1 + e2 ) = (LA (e1 )) + (LA (e2 ))                                          (5)
       LfA (e1 · e2 ) = (e1 · LfA (e2 )) + (LfA (e1 ) · e2 )                           (6)
            LfA (en ) = n · (LfA (e)) · e(n−1)                                         (7)
        LfA (ln(e)) = (LfA (e))/e                                         if e > 0     (8)

Laws (2) and (5-8) are framed analogues of known derivative rules. Laws (3)
and (4) state that the derivative of a discrete variable is zero, while that for a
continuous variable is extracted from f as explained in §3. For the latter, we need
to show that x  A and that x localised to C by A (x A) is a linear lens, that
is, getx A is a continuous linear operator, implying that the expression (x)e is
                                                                             [x   1]
Fréchet differentiable. With these laws calculations are equational Lx    (x2 ) =
     [x 1]
2·(Lx      (x))·x = 2·1·x = 2x. Observe that changing the lens changes the part of
10      Foster, Huerta y Munive, Gleirscher, Struth

S described by C and thus, the value of the framed derivative: with lens y ./ x we
     [x 1] 2          [x 1]
get Ly    (x ) = 2·(Ly      (x))·x = 2·0·x = 0. Also, changing the directionality
                         [x 2] 2            [x 2]
changes the derivative: Lx     (x ) = 2 · (Lx     (x)) · x = 2 · 2 · x = 4x.
Invariance checking. The fact that I is an invariant for vector field f , as out-
lined in §1, has so far been modelled as diff-inv. We now supply a framed variant
diff-inv-on I λ f U S t0 G, replacing g-orbital with g-orbital-on in the definition of
invariance, where again, λ : C ⇒ S projects onto C and the others parame-
ters also remain unchanged. The adjunction between backward diamonds and
wlp’s still translates differential invariance to Hoare triples as in the discussion
of invariant sets of §2:

 {I} {x 0 = e | G on U S @ t0 } {I} ⇔ diff-inv-on I x (λy. [x        e]) U S t0 G. (9)

It allows us to derive the dL-style inference rules shown below. These are all
proved as theorems using diff-inv-on, along with various rules for weakening and
strengthening to support VCG.
                                                      
                              [x e]             [x e]
                     G ⇒ Lx          e1 ∝∗ Lx         e2
                                                           ∝∈ {=, ≤, <}     (10)
                      {e1 ∝ e2 } {x 0 = e | G} {e1 ∝ e2 }
               {I1 } {x 0 = e | G} {I1 } {I2 } {x 0 = e | G ∧ I1 } {I2 }
                                                                                 (11)
                           {I1 ∧ I2 } {x 0 = e | G} {I1 ∧ I2 }
                             x ] I {P } {x 0 = e | G} {Q}
                                                                                 (12)
                             {P ∧ I} {x 0 = e | G} {Q ∧ I}
                y ./ x    y ] (G, e) {I} {(x, y)0 = (e, k · y) | G} {I}
                                                                                 (13)
                         {∃v. I[v/y]} {x 0 = e | G} {∃v. I[v/y]}

Rule (10) performs differential induction on (in)equalities [30]. There, ∝∗ is ≤
if ∝ is <, and ∝ otherwise: if the framed derivatives of two expressions satisfy
an (in)equality, then a corresponding (in)equality is an invariant. More complex
invariants (e.g. boolean combinations) reduce to these cases where computa-
tions take place [4]. If Fréchet derivatives are not defined everywhere we can still
follow the procedure for invariant reasoning in [4]. Rule (11) is differential cut,
framed but unchanged from [4] otherwise. It accumulates invariants in the guard
sequentially during VCG. Framed differential weakening is also derived as be-
fore [4], but omitted for space reasons. Rule (12) is a frame rule that discharges
invariants if they only refer to discrete variables, x ] I.
    Finally, we have also derived (13), a framed variant of the differential ghost
rule of dL [11]. In dL, it substantially expands the reasoning power with invari-
ants [31]. It is used to transform an invariant for a vector field f into an invariant
of f extended with a fresh variable y and its derivative. The extension makes the
new invariant easy to prove with rules (10), (11) and (12). Formally, rule (13)
says that I, with y abstracted, is an invariant for a system of ODEs with vari-
ables in x if it is also an invariant for the same system but with y as a fresh
                             Hybrid Systems Verification with Isabelle/HOL       11

program variable, x ⊕ y, satisfying y 0 = k · y for some constant k. Lens y must
already exists in S, but we can always expand the store with new variables [10].
We limit the derivative of y to be k · y, but we will generalise in the future.


6   Reasoning Components

We have turned the results from §4 and §5 into automated proof methods for
hybrid programs using the Eisbach tool [32]. These increase proof automation
for both our workflows relative to [4]. Our proof methods use our baseline tactic
expr-auto, which targets equalities and inequalities for shallow expressions.

hoare-wp-auto. First we supply a proof method for automatic structural VCG in
our shallow approach. To discharge partial correctness specifications {P } S {Q},
it (1) computes wlp S Q by simplification, (2) reduces substitutions and side-
conditions, (3) applies expr-auto to the resulting proof goals. Our set-up ensures
that the expression syntax is not exploded to HOL terms until step (3), which
leads to readable data-level proofs.

dInduct. To prove goals {I} {x 0 = e | G} {I}, it (1) applies Law 10 to get a
framed derivative expression, and (2) applies derivative calculation laws (Laws 2-
8), substitution laws, and basic simplification laws. This yields derivative-free
arithmetic equalities or inequalities. For cases requiring deduction, we supply
dInduct-auto, which applies expr-auto after dInduct, plus further simplification
lemmas from HOL-Analysis. Ultimately such heuristics should be augmented with
decision procedures [33–36], as oracles or verified components.
    While dInduct-auto suffices for simpler examples, differential induction must
often be combined with weakening and cut rules. This leads to another more
versatile proof method, using Isabelle’s Eisbach [32] proof method language.

dInduct-mega. The following steps are executed iteratively until all goals are
proved or no rule applies: (1) try any facts labelled with attribute facts, (2)
try differential weakening to prove the goal, (3) try differential cut (Law 11)
to split it into two differential invariants, (4) try dInduct-auto. The rules are
applied using some backtracking, so that if one fails, another one is tried. This
automatically discharges many differential invariants, as shown in §7.

local-flow. While the proof methods so far describe the second workflow using
framed versions of the inference rule of dL, the first workflow of the framework [4]
supports verification with certified solutions (flows), which can be supplied using
a CAS [37]. We have developed a proof method called local-flow for certifying that
a flow is the unique solution to an ODE. As this involves supplying a suitable
Lipschitz constant, we have written a proof method local-flow-auto that tries
several such constants, such as 0.5, 1 and 2. The Picard-Lindelöf theorem can
then be supplied to hoare-wp-auto and used to replace any ODE system within
by its local flow. This can lead to simpler VCs than differential induction.
12      Foster, Huerta y Munive, Gleirscher, Struth

7    Examples
Finally we evidence the benefits of our extensions to the framework [4] by ex-
amples. We illustrate the flexibility of our store model, the usability provided by
shallow expressions, the local reasoning provided by frames and framed deriva-
tives and the automation provided by our proof methods.
Circular pendulum. We begin with a small example explaining dInduct. Con-
sider a circular pendulum in variables x, y : R ⇒ S, and constant r : R for the
radius. We use dInduct to verify a simple invariant for its vector field.
lemma pend:"{r2 = x2 +y2 } {x’ = y, y’ = -x} {r2 = x2 +y2 }" by dInduct
First, the tactic yields Lf{x,y} (r2 ) = Lf{x,y} (x2 + y 2 ), where f = [x y, y −x]
is the vector field. It then computes 2·y·x+2·(−x)·y = 0 using differentiation and
substitution rules, which is discharged automatically by arithmetic reasoning [4].
Water tank. Next, we formalise the classic water tank example, which requires
the water level h to remain between bounds hl ≤ h ≤ hu . A controller turns a
water pump on and off to regulate h. The dataspace is described below.
dataspace water tank = constants hl ::R hu ::R co ::R ci ::R
  assumes co:"0 < co " and ci:"co < ci " variables flw::B h::R hm ::R t::R
Constants co and ci indicate rates of outflow and inflow (when the pump is on).
Variable flw is for the water pump, hm for water level measurements, and t for
time. Previously, every variable had to be a real number. Now, we provide a
clear separation between discrete and continuous variables; flw is of type B.
    With framed ODEs, we need only assign derivatives to variables h and t, and
the other variables are implicitly immutable during evolution:
abbreviation "dyn ≡ IF flw THEN {h’ = -co , t’ = 1 | t ≤ (hl -hm )/(-co )}
                   ELSE {h’ = ci -co , t’ = 1 | t ≤ (hu -h0 )/(ci -co )}"
These two ODEs model the dynamics when the inflow is on and off, respectively.
They can be written intuitively due to our expression model (§4). The frame is
inferred as {h, t}, since we only assign derivatives to them, and so hm and f lw
remain unchanged during evolution, as the following theorem confirms:
lemma nm: "dyn nmods {flw, hm }" by (simp add: closure)
lemma "{flw = F} dyn {flw = F}" by (rule nmods_invariant[OF nm], unrest)
Specifically, dyn modifies neither flw nor h, and so flw keeps its initial value F,
which is recognised as a logical variable. The latter theorem is proved using our
frame rule (1). Next, we can specify our controller:
abbreviation "ctrl ≡ (t,hm )::=(0,h); IF ¬flw ∧ hm ≤Hl +1 THEN flw::=True
  ELSE IF f lw ∧ hm ≥ hu − 1 THEN f lw ::= False ELSE skip)"
This first assigns 0 and h to t and hm , respectively, to reset the time and measure
the water level. Then, if the inflow is off and the height is getting close to the
minimum, then the inflow is enabled. Otherwise, if the level is getting near the
maximum, then it is disabled. If neither is true, then we skip.
   Using the second workflow, we use differential induction to discharge invari-
ants for the tank dynamics. We focus on the invariant when the inflow is enabled:
                             Hybrid Systems Verification with Isabelle/HOL        13

lemma "{0 ≤ t ∧ h = (ci - co )*t + hm ∧ Hl ≤ h ∧ h ≤ Hu }
       {h‘ = ci - co , t‘ = 1 | t ≤ (Hu - hm ) / (ci - co )}
       {0 ≤ t ∧ h = (ci - co )*t + hm ∧ Hl ≤ h ∧ h ≤ Hu }"
  using ci by dInduct_mega

This shows one step of the verification. We prove several invariants, using ci < co .
The key is to prove that h = (ci − co ) · t + hm , which gives the solution for h and
allows us to bound how much the water rises. dInduct-mega automates the proof
with successive differential cuts. The system proof is concluded with hoare-wp-
auto to verify the controller. The verification is automated by a high-level proof
method (dProve):
lemma tank_correct:
  "{t = 0 ∧ h = hm ∧ Hl ≤ h ∧ h ≤ Hu }
    LOOP ctrl ; dyn INV (0≤t ∧ h = ((flw*ci )-co )*t + hm ∧ Hl ≤h ∧ h≤Hu )
   {Hl ≤ h ∧ h ≤ Hu }" using ci co by dProve

We need to supply an extended invariant for both the controller and dynamics
via an annotation. Internally the proof uses the frame rule to demonstrate that
both flw and ¬flw are invariants of dyn. The earlier lemma is technically not
required, as dProve itself invokes dInduct-mega during the proof.
    We can alternatively verify the controller using the first workflow, with a
solution to the differential equations:
lemma lf:"local_flow_on [h k,t 1] (h⊕t) UNIV UNIV (λτ .[h k*τ ,t τ +t])"
  by local_flow_auto

lemma "{hm ≤h ∧ h≤hM } LOOP ctrl;dyn INV (hm ≤h∧h≤hM ) {hm ≤h ∧ h≤hM }"
  using tank_arith[OF _ co ci] by (hoare_wp_auto local_flow: lf)

We need to certify the unique (framed) solution for the water tank vector field
using local-flow-auto. The loop invariant need not refer to flw or hm , since these
are discrete. The proof uses hoare-wp-auto, which is given the local flow proof
lf, and so can internally replace the ODE with the flow.
Exponential decay. This example contrasts the use of the differential ghost
law and solutions in ODE proof. We wish to show that x > 0 is an invariant of
x0 = −x, which is not immediately obvious because the derivative is negative.
    The proof using differential ghost is as follows: x > 0 is equivalent to xy 2 = 1
for some value of y. To show that this new property is an invariant for the evo-
lution command, we use the ghost rule to expand the system of ODEs into x0 =
−x, y 0 = y/2, which retains the behaviour of x. Then, by standard reasoning [4],
xy 2 = 1 is an invariant because (xy 2 )0 = x0 y 2 + 2xyy 0 = −xy 2 + xy 2 = 0 = 10 .
The Isabelle proof requires some interaction:
lemma dG example: "{x > 0} {x’ = -x} {x > 0}"
  apply (dGhost "y" "(x ∗ yˆ2 = 1)e " "1/2", expr_auto add: exp_arith)
  apply (dInduct_auto, simp add: power2_eq_square) done

The first line applies differential ghost, with the fresh variable y, the property
xy 2 = 1, and the factor 1/2 of the ODE y 0 = y/2. This yields 0 < x ⇔ ∃v. xv 2 =
14      Foster, Huerta y Munive, Gleirscher, Struth

1, which we prove using a lemma (exp arith). The last line applies dInduct-auto
and a sledgehammer [34] supplied proof for the goal yy 6= y 2 ⇒ y = 0.
    For the first workflow, x > 0 is an invariant because the solution, x t = x0 e−t ,
is a positive exponential function for x0 > 0. The proof of invariance follows
immediately from this fact and automatically with our tactic.

lemma flow ex:"{x > 0} {x’ = -x}{x > 0}" by (hoare wp auto local flow: lf)

We again supply a certified solution using the theorem lf (omitted). Alterna-
tively, if users wish to skip the certification and write the flow directly in the
specification, this is also possible and automatic using notation introduced in§5.

lemma "{x > 0} {EVOL x = x * exp (- τ )} {x > 0}" by hoare_wp_auto


Autonomous boat. The final example [24] is a controller for an autonomous
boat using the second workflow. We model the dynamics and several controller
components, which demonstrates our flexible hybrid store model and local rea-
soning with our framework. The boat’s objective is to navigate along several
way-points, while avoiding obstacles. It is manoeuvrable in R2 and has a rotat-
able thruster generating a positive propulsive force f with maximum fmax . The
boat’s state is determined by its position p, velocity v, and acceleration a:

dataspace AMV = constants S::R fmax ::R assumes fmax:"fmax ≥ 0"
  variables p::"R vec[2]" v::"R vec[2]" a::"R vec[2]" φ::R s::R
    wps::"(R vec[2]) list" org::"(R vec[2]) set" rs::R rh::R

This complex store model consists of a combination of discrete and continuous
variables. Here, R vec[n] is a vector of dimension n. In the dataspace, we
have a variable for linear speed s, and constant S is the maximum speed. We
also model discrete variables for the way-point path (wps), the obstacle register
(org), and requested speed and heading (rs and rh).
    With the following axiom, we relate s, φ with v and constrain s.

abbreviation "ax ≡ (s *R [[sin(φ), cos(φ)]] = v ∧ 0 ≤ s ∧ s ≤ S)e "

This states that v is equal to s multiplied by the heading unit-vector using
scalar multiplication (*R ) and our vector syntax, and 0 ≤ s ≤ S. The kinematics
[p 0 , v 0 , a 0 ]T is specified below:

abbreviation "ODE ≡ { p‘ = v, v‘ = a, a‘ = 0, φ‘ = ω,
                      s‘ = if s 6= 0 then (v · a) / s else kak | @ax }"

We also specify derivatives for φ and s. The former, ω is the angular velocity,
which has the value arccos((v + a) · v/(kv + ak · kvk)) when kvk =      6 0 and 0
otherwise. The linear acceleration (s0 ) is calculated using the inner product of v
and a. If the current speed is 0, then s0 is simply kak. All other variables in the
store are implicitly outside the evolution frame:

lemma "ODE nmods {rs, rh, wps, org}" by (simp add: closure)
                              Hybrid Systems Verification with Isabelle/HOL        15

The controller for the AMV consists of three parts: Navigation for way-point
following, AP the autopilot proportional controller, and LRE the safety con-
troller. Navigation and LRE both supply requested headings and speeds to the
Autopilot, which calculates an acceleration vector for the ODE. For reasons of
space, we omit further details. We prove some differential invariants of ODE:
lemma "{s2 = v · v} ODE {s2 = v · v}" by (dWeaken, metis orient_vec_mag_n)
lemma "{a = 0 ∧ v = V} ODE {a = 0 ∧ v = V}" by (dInduct_mega)
lemma "{(a = 0 ∧ s > 0) ∧ φ = X} ODE {φ = X}" by (dInduct_mega)
The first shows that s2 is equal to the inner product of v with itself, and is charged
by differential weakening and a vector lemma. The second shows that if the ac-
celeration vector is 0, the velocity is not changing. The third shows, similarly,
that the orientation is not changing. These demonstrate our ability to form dif-
ferential invariants over vectors, as well as scalars. We also reason about vectors
algebraically without coordinate-wise decomposition. Since s and v are modified
only by the ODE, we can also show that the first invariant is also an invariant    of
each other component using our frame rule; e.g. s2 = v Autopilot s2 = v .
                                                                            
Moreover, this is also a system invariant. This kind of local reasoning makes proof
about such component-based systems tractable. We check a final ODE invariant:
lemma "{a·v≥0 ∧ (a·v)2 = (a·a)·(v·v)} ODE {a·v≥0 ∧ (a·v)2 = (a·a)·(v·v)}"
  by (dInduct_mega, metis inner_commute)

This property tells us that if v and a have the same direction, they will continue
to do so. The boat may be linearly accelerating or decelerating, but is not turn-
ing. Method dInduct-mega produces a proof obligation relating to inner product,
which is discharged with sledgehammer [34].


8    Related Work, Conclusions, and Future Work
We have transformed an Isabelle framework for the verification of hybrid systems
into a more user-friendly and effective formal method, using Isabelle’s syntax
translation mechanisms to interface with more natural modelling and specifica-
tion languages for hybrid programs. We have also shown how local reasoning
about hybrid stores can be achieved using lenses, how this leads to better and
more automatic tactics and to more accessible verification conditions.
    Deductive reasoning about hybrid systems is not new, and there is substan-
tial work supporting this activity through domain-specific decision procedures.
With PVS, a formalisation for dL-style verification by formalising semi-algebraic
sets and real analytic functions is in its early steps [38]. With Coq, the ROSCoq
framework [39] uses Coq’s CoRN library of constructive real numbers to for-
malise a Logic of Events (LoE) to reason about hybrid systems. The VeriDrone
project [1] uses the Coquelicot library for a variant of the temporal logic of ac-
tions. Both semantics are very different from our dL-inspired one. Yet we view
the framework rather as complementary to dL’s KeYmaera X tool, which brings
the benefit of certified decisions procedures for real arithmetic and a user-friendly
interface. With Isabelle, a term checker for dL has been formalised as a deep em-
bedding [40,41], but without aiming at verification components. A hybrid Hoare
16      Foster, Huerta y Munive, Gleirscher, Struth

logic [2] for verifying hybrid CSP processes [42] has been formalised as a shallow
embedding, but with a very different semantics to our own Hoare logic [6].
     Work remains to be done for transforming this framework further into an
industrial-strength formal method. This is supported by its openness and com-
positionality. Our new hybrid store and extant ODE components for Isabelle
could, for instance, be integrated into the state transformer semantics [4] with
little effort. Our new expression language could easily be replaced by Modelica
syntax. In the future, one could use Isabelle’s code generator to provide path-
ways from hybrid programs to verified controller implementations. Openness
implies in particular that anyone interested in hybrid systems verification with
Isabelle could extend, adapt and contribute to this framework. Its power is only
limited by Isabelle’s higher order logic and the mathematical and verification
components that the community provides for it.


Acknowledgements

This work is funded by UKRI-EPSRC project CyPhyAssure (grant reference
EP/S001190/1); Novo Nordisk Fonden Start Package Grant (NNF20OC0063462);
and the Assuring Autonomy International Programme (AAIP; grant CSI:Cobot),
a partnership between Lloyd’s Register Foundation and the University of York.


References

 1. Ricketts, D., Malecha, G., Alvarez, M.M., Gowda, V., Lerner, S.: Towards verifica-
    tion of hybrid systems in a foundational proof assistant. In: MEMOCODE, IEEE
    (2015) 248–257
 2. Wang, S., Zhan, N., Zou, L.: An improved HHL prover: An interactive theorem
    prover for hybrid systems. In: ICFEM. Volume 9407 of LNCS. (2015) 382–399
 3. Huerta y Munive, J.J., Struth, G.: Verifying hybrid systems with modal Kleene
    algebra. In: RAMiCS. Volume 11194 of LNCS., Springer (2018) 225–243
 4. Huerta y Munive, J.J., Struth, G.: Predicate transformer semantics for hybrid sys-
    tems: Verification components for Isabelle/HOL. arXiv:1909.05618 [cs.LO] (2019)
 5. Foster, S.: Hybrid relations in Isabelle/UTP. In: UTP. Volume 11885 of LNCS.,
    Springer (2019) 130–153
 6. Foster, S., Huerta y Munive, J.J., Struth, G.: Differential Hoare logics and re-
    finement calculi for hybrid systems with Isabelle/HOL. In: RAMiCS[postponed].
    Volume 12062 of LNCS. (2020) 169–186
 7. Huerta y Munive, J.J.: Verification components for hybrid systems. Archive of
    Formal Proofs (2019)
 8. Huerta y Munive, J.J.: Matrices for ODEs. Archive of Formal Proofs (2020)
 9. Immler, F., Traut, C.: The flow of ODEs: Formalization of variational equation
    and Poincaré map. J. Automated Reasoning 62(2) (2019) 215–236
10. Foster, S., Baxter, J.: Automated algebraic reasoning for collections and local
    variables with lenses. In: RAMiCS. Volume 12062 of LNCS., Springer (2020)
11. Platzer, A.: Logical Foundations of Cyber-Physical Systems. Springer (2018)
                               Hybrid Systems Verification with Isabelle/HOL            17

12. Boulton, R.J., Gordon, A.D., Gordon, M.J.C., Harrison, J., Herbert, J., Tassel,
    J.V.: Experience with embedding hardware description languages in HOL. In:
    IFIP Transactions. Volume A-10., North-Holland (1992) 129–156
13. Wildmoser, M., Nipkow, T.: Certifying machine code safety: Shallow versus deep
    embedding. In: TPHOLs. Volume 3223 of LNCS., Springer (2004) 305–320
14. Nipkow, T., Klein, G.: Concrete Semantics - With Isabelle/HOL. Springer (2014)
15. Huerta y Munive, J.J.: Affine systems of ODEs in Isabelle/HOL for hybrid-program
    verification. In: SEFM. Volume 12310 of LNCS., Springer (2020) 77–92
16. Teschl, G.: Ordinary Differential Equations and Dynamical Systems. AMS (2012)
17. Mitsch, S., Huerta y Munive, J.J., Jin, X., Zhan, B., Wang, S., Zhan, N.: ARCH-
    COMP20 category report: Hybrid systems theorem proving. In: ARCH20. (2019)
    141–161
18. Foster, S., Baxter, J., Cavalcanti, A., Woodcock, J., Zeyda, F.: Unifying semantic
    foundations for automated verification tools in Isabelle/UTP. Science of Computer
    Programming 197 (October 2020)
19. Foster, S., Zeyda, F.: Optics. Archive of Formal Proofs (May 2017)
20. Oles, F.: A Category-Theoretic Approach to the Semantics of Programming Lan-
    guages. PhD thesis, Syracuse University (1982)
21. Back, R., von Wright, J.: Refinement Calculus—A Systematic Introduction.
    Springer (1998)
22. Foster, J.: Bidirectional programming languages. PhD thesis, University of Penn-
    sylvania (2009)
23. Foster, S., Zeyda, F., Woodcock, J.: Unifying heterogeneous state-spaces with
    lenses. In: ICTAC. Volume 9965 of LNCS. (2016) 295–314
24. Foster, S., Gleirscher, M., Calinescu, R.: Towards deductive verification of control
    algorithms for autonomous marine vehicles. In: ICECCS, IEEE (October 2020)
25. Immler, F., Hölzl, J.: Numerical analysis of ordinary differential equations in
    Isabelle/HOL. In: ITP. Volume 7406 of LNCS., Springer (2012) 377–392
26. Hölzl, J., Immler, F., Huffman, B.: Type classes and filters for mathematical
    analysis in Isabelle/HOL. In: ITP. Volume 7998 of LNCS., Springer (2013) 279–
    294
27. Foster, S., Nemouchi, Y., Gleirscher, M., Wei, R., Kelly, T.: Integration of for-
    mal proof into unified assurance cases with Isabelle/SACM. Formal Aspects of
    Computing (2021)
28. Kuncar, O., Popescu, A.: A consistent foundation for Isabelle/HOL. J. Autom.
    Reasoning 62 (2019) 531–555
29. Cheney, E.W.: Analysis for applied mathematics. Springer (2001)
30. Platzer, A.: The structure of differential invariants and differential cut elimination.
    Logical Methods in Computer Science 8(4) (2008)
31. Platzer, A., Tan, Y.K.: Differential equation axiomatization: The impressive power
    of differential ghosts. In: LICS, ACM (2018) 819–828
32. Matichuk, D., Murray, T.C., Wenzel, M.: Eisbach: A proof method language for
    Isabelle. J. Automated Reasoning 56(3) (2016) 261–282
33. Hölzl, J.: Proving inequalities over reals with computation in Isabelle/HOL. In:
    PLMMS, ACM (2009) 38–45
34. Blanchette, J.C., Kaliszyk, C., Paulson, L.C., Urban, J.: Hammering towards QED.
    Journal of Formalized Reasoning 9(1) (2016)
35. Li, W., Passmore, G., Paulson, L.: Deciding univariate polynomial problems using
    untrusted certificates in Isabelle/HOL. J. Autom. Reasoning 62 (2019) 29–91
36. Cordwell, K., Yong, K.T., A., P.: A verified decision procedure for univariate real
    arithmetic with the BKR algorithm. In: ITP. (2021) To appear.
18      Foster, Huerta y Munive, Gleirscher, Struth

37. Hickman, T., Laursen, C.P., Foster, S.: Certifying differential equation solutions
    from computer algebra systems in Isabelle/HOL. arXiv:2102.02679 [cs.LO] (Febru-
    ary 2021)
38. Slagel, J.T., White, L., Dutle, A.: Formal verification of semi-algebraic sets and
    real analytic functions. In: CPP, ACM (2021) 278–290
39. Anand, A., Knepper, R.A.: Roscoq: Robots powered by constructive reals. In:
    ITP. Volume 9236 of LNCS., Springer (2015) 34–50
40. Bohrer, B., Rahli, V., Vukotic, I., Völp, M., Platzer, A.: Formally verified differ-
    ential dynamic logic. In: CPP, ACM (2017) 208–221
41. Platzer, A.: Differential game logic. Archive of Formal Proofs 2019 (2019)
42. Liu, J., Lv, J., Quan, Z., Zhan, N., Zhao, H., Zhou, C., Zou, L.: A calculus for
    hybrid CSP. In: APLAS. Volume 6461 of LNCS., Springer (2010) 1–15
