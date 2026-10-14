                        Veriﬁed Software Units

                                  Lennart Beringer

                    Princeton University, Princeton NJ 08544, USA
                             eberinge@cs.princeton.edu


       Abstract. Modularity - the partitioning of software into units of func-
       tionality that interact with each other via interfaces - has been the main-
       stay of software development for half a century. In case of the C language,
       the main mechanism for modularity is the compilation unit / header ﬁle
       abstraction. This paper complements programmatic modularity for C
       with modularity idioms for speciﬁcation and veriﬁcation in the context
       of Veriﬁable C, an expressive separation logic for CompCert Clight. Tech-
       nical innovations include (i) abstract predicate declarations – existential
       packages that combine Parkinson & Bierman’s abstract predicates with
       their client-visible reasoning principles; (ii) residual predicates, which
       help enforcing data abstraction in callback-rich code; and (iii) an appli-
       cation to pure (Smalltalk-style) objects that connects code veriﬁcation
       to model-level reasoning about features such as subtyping, self, inheri-
       tance, and late binding. We introduce our techniques using concrete ex-
       ample modules that have all been veriﬁed using the Coq proof assistant
       and combine to fully linked veriﬁed programs using a novel, abstraction-
       respecting component composition rule for Veriﬁable C.

       Keywords: Veriﬁed Software Unit · Abstract Predicate Declaration ·
       Residual Predicate · Positive Subtyping · Veriﬁed Software Toolchain.


1    Introduction
Separation logic [61,53] constitutes a powerful framework for verifying functional
correctness of imperative programs. Foundational implementations in interactive
proof assistants such as Coq exploit the expressiveness of modern type theory
to construct semantic models that feature higher-order impredicative quantiﬁca-
tion, step-indexing, and advanced notions of ghost state [4,36]. On the basis of
proof rules that are justiﬁed w.r.t. the operational semantics of the programming
language in question, these systems perform symbolic execution and employ mul-
tiple layers of tactical or computational proof automation to assist the engineer
in the construction of concrete veriﬁcation scripts. Perhaps most importantly,
these implementations integrate software veriﬁcation and model-level validation,
by embedding assertions shallowly in the proof assistant’s ambient logic; this
permits speciﬁcations to refer to executable model programs or domain-speciﬁc
constructions that are then amenable to code-independent analysis in Coq.
    To realize the potential of separation logic, such implementations must be
provided for mainstream languages and compatible with modern software engi-
neering principles and programming styles. This paper addresses this challenge
c The Author(s) 2021
N. Yoshida (Ed.): ESOP 2021, LNCS 12648, pp. 118–147, 2021.
https://doi.org/10.1007/978-3-030-72019-3 5
                                                     Veriﬁed Software Units       119

for Veriﬁable C, the program logic of the Veriﬁed Software Toolchain (VST [4]).
We advance Veriﬁable C’s methodology as follows.

 1. We provide general infrastructure for modular veriﬁcation of modular pro-
    grams by extending Beringer and Appel’s recent theory of function speciﬁ-
    cation subsumption and intersection speciﬁcations [15] to a formal calculus
    for composing veriﬁed software units (VSUs) at their speciﬁcation interface.
    Each VSU equips a compilation unit’s header ﬁle with VST speciﬁcations of
    its API-exposed functions. Composition of VSUs matches the respective im-
    port and export interfaces, applying subsumption as necessary. Crucially, a
    compilation unit’s private functions remain hidden and only need to be spec-
    iﬁed locally. Composition is compatible with source-level linking for Comp-
    Cert Clight and supports repeated import of library modules (§3).
 2. Utilizing existential abstraction [46] and parametricity, we extend work on
    abstract predicates [56] to provide clients with speciﬁcation interfaces that
    diﬀer in the degree to which module-internal representation details are re-
    vealed. This ﬂexibility is achieved by codifying how the reasoning principles
    associated with a predicate can be selectively communicated to clients, using
    a device we call (existentially) abstract predicate declarations (APDs) (§4).
 3. To investigate speciﬁcation modularity in the presence of callbacks, we study
    variants of the subject-observer design pattern; we demonstrate that by com-
    plementing a module’s primary predicate with residual predicates, represen-
    tation hiding can be respected even at transient interaction points, where
    an invocation of a module’s operation is interrupted, the module’s invari-
    ant may be violated, and yet its internal state must remain unmodiﬁed and
    unexposed until the operation is resumed (§5).
 4. We present a novel approach to foundational reasoning about object prin-
    ciples that modularly separates C code veriﬁcation from model-level behav-
    ior. Exploiting the theory of positive subtyping [30], we cover subtyping,
    interfaces with multiple implementations, dynamic dispatch, self, and late
    binding, for a simple Smalltalk-style object model with static typing (§6).

This paper is accompanied by a development in Coq [14] that conservatively
extends VST with the VSU infrastructure and contains several case studies. In
addition to the examples detailed in the paper, the Coq code treats (i) the run-
ning example (“piles”) of Beringer and Appel’s development [15]; we retain their
ability to substitute representation-altering but speciﬁcation-preserving imple-
mentations; (ii) a variant of Barnett and Naumann’s Master-Clock example [12],
as another example of tightly coupled program units; and (iii) an implementa-
tion of the Composite design pattern, obtained by transcribing a development
from the Verifast code base [35]. In addition, a VSU interface that uniﬁes the
APIs of B+ -trees and tries was recently developed by Kravchuk-Kirilyuk [40].
    To see how APDs build on Parkinson and Bierman’s work, consider a concrete
representation predicate in the style of Reynolds [61]: list x α p speciﬁes that
address p represents a monotone list α of numbers greater than x:
          def                                 def
list x nil p = (p=null) & emp   list x (a::α) p = ∃ q. a > x & p → a, q ∗ list a α q.
120    L. Beringer

Being deﬁned in terms of →, this deﬁnition assumes a speciﬁc data layout (a two-
ﬁeld struct). Representation-speciﬁc predicates enable veriﬁcation of concrete
implementations of operations such as reverse. But a client-facing speciﬁcation
of the entire list module should only expose the predicate in its folded form –
a simple case of an abstract predicate. Indeed, while VST fully supports API
exposure of structs (incl. stack allocation), all examples in this paper employ an
essentially “dataless” programming discipline [8,60,37] in which structs are at
most exposed as forward declarations. Clearly, such programmatic encapsulation
should not be compromised through the use of concrete predicate deﬁnitions.
    To regulate whether a predicate is available in its abstract or unfolded form
at a particular program point, Parkinson and Bierman employ a notion of scope:
predicates are available in their unfolded form when in scope and are treated
symbolically elsewhere. This separation can naturally align with the partitioning
into compilation units, but is all-or-nothing. But even in the absence of speciﬁca-
tions, diﬀerent clients need diﬀerent interfaces: C developments routinely provide
multiple header ﬁles for a single code unit, diﬀering in the amount to which rep-
resentational information is exposed. Mundane examples include special-purpose
interfaces for internal performance monitoring or debugging. Extending this ob-
servation to speciﬁcations means supporting multiple public invariants. Indeed,
several levels of visibility are already conceivable for our simple list predicate:
 – no (un)folding, no exposed reasoning principles: properties that follow from
   the predicate’s deﬁnition cannot be exploited during client-side veriﬁcation;
 – no (un)folding, but reasoning principles are selectively exposed; for example,
   one may expose the model-level property that α is strictly increasing, or the
   fact that the head pointer is null exactly if α is empty;
 – the set of exposed reasoning principles includes fold/unfold lemmas (perhaps
   with the least-ﬁxed-point property inherent in the inductive deﬁnition of the
   predicate), but the internal representation of nodes is encapsulated using a
   further predicate; hence, implementations are free to select a diﬀerent struct
   layout, for example by swapping the order of ﬁelds;
 – the predicate deﬁnition is fully exposed, including the internal data layout.
APDs support such ﬂexibility by combining zero or more abstract predicate dec-
larations (no deﬁnitions, to maintain implementation-independence) with ax-
ioms that selectively expose the predicates’ reasoning principles. In parallel to
programmatic forward declarations, an APD is exported in the speciﬁcation in-
terface of an API and is substantiated – in implementation-dependent fashion
– in the VST proof of the corresponding compilation unit. This substantiation
includes the validation of the exposed axioms. When specifying the API of a
module, the engineer may not only refer to any APDs introduced by the module
in question, but may also assume APDs for data structures provided by other
modules (whose header ﬁles are typically #included in the API in question).
Matching the APD assumptions and provisions of diﬀerent modules occurs nat-
urally during the application of our component linking rule, ensuring that fully
linked programs contain no unresolved APD assumptions.
    Before going into technical details, we ﬁrst summarize key aspects of VST.
                                                     Veriﬁed Software Units      121

2   Program veriﬁcation using VST
Veriﬁcation using VST happens exclusively inside the Coq proof environment,
and operates directly on abstract syntax trees of CompCert Clight. Typically,
these ASTs result from feeding a C source ﬁle through CompCert’s frontend,
clightgen, but they may also originate from code synthesis. Either way, veriﬁca-
tion applies to the same code that is then manipulated by CompCert’s optimiza-
tion and backend phases. This eliminates the assurance gap that emerges when
a compiler’s (intermediate) representation diverges syntactically or semantically
from a veriﬁcation tool’s representation. The absence of such gaps is the gist of
VST’s machine-checked soundness proof: veriﬁed programs are safe w.r.t. the op-
erational semantics of Clight; this guarantee includes memory safety (absence of
null-pointer dereferences, out-of-bounds array accesses, use-after-frees,. . . ) but
also absence of unintended numeric overﬂows or race conditions. As Clight code
is still legal C code (although slightly simpliﬁed, and with evaluation order de-
terminized), veriﬁcation happens at a level the programmer can easily grasp.
    In contrast to other veriﬁcation tools, VST does not require source code
to be annotated with speciﬁcations. Instead, the veriﬁcation engineer writes
speciﬁcations in a separate Coq ﬁle. By not mixing speciﬁcations (let alone
aspects of proof, such as loop invariants) with source code, VST easily supports
associating multiple speciﬁcations with a function and constructing multiple
proofs for a given code/speciﬁcation pair.
    We write function speciﬁcations φ in the form {P } ; {v . Q} where v denotes
the (sometimes existentially quantiﬁed) return value and P and Q are separation
logic assertions. To shield details of its semantic model, VST exposes heap asser-
tions using the type mpred rather than as direct Coq-level predicates. On top
of mpred, assertions are essentially embedded shallowly, giving the user access
to the logical and programmatic features of Coq when deﬁning speciﬁcations.
    VST’s top-level notion asserting that a (closed) program p – which must
include main, with a standard speciﬁcation – has been veriﬁed in Coq is  p : G
(“semax prog”). Here, G – of type funspecs, i.e. associating speciﬁcations φ
to function identiﬁers f – constitutes a witnessing proof context that contains
speciﬁcations for all functions in p and must itself be justiﬁed: for each (f, φf ) ∈
G, the user must exhibit a Coq proof of G  f : φf (“semax body”), expressing
that f satisﬁes φf under hypotheses in G. VST’s step-indexed model ensures
logical consistency in case of (mutual) recursion.
    We exploit Beringer and Appel [15]’s theory of speciﬁcation subsumption
φ <: ψ which extends parameter adaptation [38,50,48] to step-indexed separa-
tion logics for C and allows a function veriﬁed w.r.t φ to be used by clients
expecting speciﬁcation ψ. This theory includes a notion of speciﬁcation inter-
section ∧ which – similar to, e.g. the also combinator of the Java Modelling
Language (JML, [19])– allows functions to have multiple speciﬁcations. Notice-
ably, subsumption and intersection are related in formally the same manner as
intersection types and subtyping are in type theory: in particular, they satisfy
                                              ψ <: φ1 ψ <: φ2
the laws φ1 ∧ φ2 <: φi (for i ∈ {1, 2}) and                     (cf. [58], page 206).
                                                ψ <: φ1 ∧ φ2
122     L. Beringer

3     VSU calculus

As described above, VST veriﬁcation amounts to exhibiting a G with  p : G. In
contrast to VST’s previous linking regime, VSU ensures existence of G during
component linking without actually constructing G, maintaining representation
hiding and non-exposure of private functions. Indeed, the modules’ speciﬁcation
interfaces (specs of imported and exported functions) suﬃce for proving that a
suitable G exists, as long as each module’s individual justiﬁcation includes the
veriﬁcation of its private functions.


3.1   Components and soundness

VSU extends CompCert’s distinction between internal functions (those equipped
locally with a function body) and external functions (functions deﬁned in other
compilation units, incl. system functions). Given a Clight compilation unit p, we
denote these (disjoint) sets by IntFuns(p) and ExtFuns(p), respectively. VSU
further distinguishes between system functions (typically provided by the OS)
and ordinary external functions: the former ones are not expected to be veriﬁed
using VST even in a fully linked program, so VSU merely records their use.
    VSU’s main judgment is SP [I] p [E], to be read as using speciﬁed imports
I and system functions S, p provides/ exports functions (with speciﬁcations) E,
using internal memory satisfying (initially) P . The entities S, I, and E are all
funspecs, while P speciﬁes the memory holding p’s global variables; P ’s formal
type is globals → mpred where globals refers to a map from global identiﬁers
to CompCert values.
    The judgment SP [I] p [E] is formally introduced as an existential abstraction
(in Coq: a Record type) over a proof context G, which is again of type funspecs:

                         SP [I] p [E] = ∃G. G SP [I] p [E].
                                      def




    The role of G is to serve as the witness justifying the speciﬁcation interface; as
such it associates speciﬁcations also to p’s private functions; existentially hiding
it shields implementation details.
    The formation of the lower-level judgment G SP [I] p [E] is subject to the
following constraints:

Deﬁnition 1. Proof context G justiﬁes a component (speciﬁcation) for Clight
compilation unit p with respect to system calls S, imports I, exports E, and
predicate P , notation G SP [I] p [E], if

1. dom I ∩ dom S = ∅ and dom I ∪ dom S ⊆ ExtFuns(p),
2. dom G = IntFuns(p) ∪ dom S, with G(i) = S(i) whenever i ∈ dom S,
3. dom E ⊆ dom G, with G(i) <: E(i) for all i ∈ dom E,
4. I ∪ G func funs p : G,
5. ∀ g, InitGPred(Vardefs(p)) g  P g
                                                       Veriﬁed Software Units     123

The ﬁrst three clauses are largely administrative; they express, respectively,
that (1) system functions and imported functions are disjoint sets of external
functions, (2) G contains speciﬁcations for exactly the system functions and the
internal functions, and (3) all exported speciﬁcations are abstractions of entries
in G, in the sense of speciﬁcation subsumption <:.
    Clause (4) constitutes the main proof obligation and refers to a slight refactor-
ing of VST’s function-veriﬁcation judgment G1 func funs : G2 (semax-func),
where funs associates CompCert function deﬁnitions with identiﬁers. The instan-
tiation I ∪ G func funs p : G hence requires that imports I suﬃce for justifying
all entries in G: each system function speciﬁcation in G must be valid, and each
speciﬁcation of an internal function must be justiﬁed by a VST proof the corre-
sponding function body in funs; calls to internal and system functions inside the
body are resolved by reference to G, and calls to external functions are resolved
by the import speciﬁcations, I.
    Finally, clause (5) requires p’s global variables to collectively satisfy P (after
initialization) but avoids referring to these variables by name.
    We point out two further aspects of Deﬁnition 1. First, we note that system
functions may be exported (we do not require dom S ∩ dom E = ∅), and that
imports and exports are distinct (dom I ∩ dom E = ∅ follows). Second, we note
that for I = ∅, clause (4) yields G func funs p : G, i.e. the heart of VST’s sound-
ness condition semax prog for programs comprised of a single compilation unit.
Hence, the goal of VSU veriﬁcation is to exhaustively apply VSU’s combination
rule (presented in the next subsection) until all imports have been resolved.
    Once a component has been veriﬁed and is exposed as SP [I] p [E], the spec-
iﬁcations of p’s private functions are hidden inside the existentially quantiﬁed
context G and hence inaccessible.


3.2   Derived rules

It is easy to derive a rule of consequence from Deﬁnition 1 that strengthens
imports and relaxes exports:

       I  <: I     SP [I] p [E]     E  E      ∀ g, P g  P  g
                                                                     VSUConseq
                             P  [I ] p [E  ]
                               S    


For imported functions, we require pointwise subsumption, by deﬁning I  <: I to
hold if dom I = dom I  and I  (i) <: I(i) for all i ∈ dom I. On the export side, we
allow hiding of entries, by deﬁning E  E  to hold if dom E  ⊆ dom E and E(i) <:
E  (i) for all i ∈ dom E  . The calculus is invariant in the speciﬁcations of system
functions, but allows weakening of the initialization predicate. The derivation
of this rule instantiates the context witnessing the concluding judgment by the
(abstract) witness obtained from unfolding the hypothetical judgment.
      VSU’s workhorse is the composition rule, VSULink, shown in Figure 1. The
side conditions treat the components symmetrically and are motivated as follows.
The rule constructs a component speciﬁcation for a linked program p that retains
the internal functions of p1 and p2 , and also any unresolved external functions, as
124       L. Beringer


 (a)                           S 1
                                P1 [I1 ] p1 [E1 ]    S 2
                                                      P2 [I2 ] p2 [E2 ]


                 ∀i ∈ IntFuns(p1 ) ∪ (ExtFuns(p1 ) \ IntFuns(p2 )), p(i) = p1 (i)
 (b)             ∀i ∈ IntFuns(p2 ) ∪ (ExtFuns(p2 ) \ IntFuns(p1 )), p(i) = p2 (i)
                                   dom p = dom p1 ∪ dom p2

        ∀i ∈ (IntFuns(p1 ) ∩ IntFuns(p2 )) ∪ (ExtFuns(p1 ) ∩ ExtFuns(p2 )), p1 (i) = p2 (i)
 (c)         ∀i ∈ IntFuns(p1 ) ∩ ExtFuns(p2 ), sig(p1 (i)) = sig(p2 (i)) ∧ i ∈ dom I2
             ∀i ∈ IntFuns(p2 ) ∩ ExtFuns(p1 ), sig(p2 (i)) = sig(p1 (i)) ∧ i ∈ dom I1

 (d)               dom S1 ∩ IntFuns(p2 ) = ∅        dom S2 ∩ IntFuns(p1 ) = ∅

              ∀i ∈ dom I2 ∩ (dom S1 ∪ IntFuns(p1 )), i ∈ dom E1 ∧ E1 (i) <: I2 (i)
 (e)
              ∀i ∈ dom I1 ∩ (dom S2 ∪ IntFuns(p2 )), i ∈ dom E2 ∧ E2 (i) <: I1 (i)

 (f )                         ∀i ∈ dom I1 ∩ dom I2 , I1 (i) = I2 (i)

 (g)            I = I1 \ (dom S2 ∪ IntFuns(p2 )) ∪ I2 \ (dom S1 ∪ IntFuns(p1 ))

 (h)       Vardefs(p1 ) ∩ Vardefs(p2 ) = ∅     Vardefs(p1 ) ∪ Vardefs(p2 ) = Vardefs(p)
                                    S
                                     P1 ∗P2 [I] p [E1  E2 ]
                                       1 S2




                Fig. 1. VSU’s rule of component composition, VSULink.



detailed in side conditions (b). Condition (c) requires functions classiﬁed identi-
cally by p1 and p2 to have identical deﬁnitions, and requires diﬀerently classiﬁed
functions to have identical type signatures and be in the import set of the com-
pilation unit not providing the implementation. Condition (d) formalizes that
system functions are not locally deﬁned in either unit. Condition (e) expresses
that a function imported by one module and programmatically provided by the
other module must be exported by the provider; this condition ensures that the
export contract cannot be bypassed. Condition (f ) expresses that functions im-
ported by both units must be imported identically - if necessary, this can be
achieved using the consequence rule. Condition (g) calculates the remaining im-
port speciﬁcations by combining the constituent imports, removing entries for
the resolved functions, and ensuring the absence of duplicates. The ﬁnal con-
dition, (h), mandates that global variables from p1 and p2 be distinct (hence
initialization predicates have disjoint footprints) and propagated to p.
    The most interesting aspect of the rule is the duplicate use of the intersection
operator, C1  C2 , for constructing the concluding speciﬁcations of exported
functions and system functions. The general deﬁnition of this operator is

                             ⎨ C1 (i) ∧ C2 (i) if i ∈ dom C1 ∩ dom C2
                             ⎧

               C1  C2 := λi. C1 (i)           if i ∈ dom C1 \ dom C2
                               C2 (i)          if i ∈ dom C2 \ dom C1
                             ⎩
                                                       Veriﬁed Software Units     125

where ∧ denotes the speciﬁcation intersection operator mentioned in Section 2.
Thus, exporting E1  E2 eﬀectively exports both E1 and E2 , and similarly for
S1  S2 . Indeed, the individual export speciﬁcations can be reestablished using
the consequence rule, as the properties of intersection speciﬁcations mentioned
in Section 2 lift to (export speciﬁcation) contexts: we have C1  C2  Ci for
                X  C1 X  C2
i ∈ {1, 2} and                      for any X.
                   X  C1  C2
     By permitting functions f that are internal to both p1 and p2 , VSU supports
diamond-shaped composition patterns in which a sub-component, e.g. a library,
is imported multiple times. Conditions (b) and (c) ensure that all copies of a
repeatedly imported function f have the same body (i.e. CompCert AST), and
that this body is retained in p. However, the library’s export speciﬁcation may
have been imported diﬀerently by the diﬀerent units, hence G1 and G2 may well
associate diﬀerent (and formally incompatible) speciﬁcations with f . As G1 and
G2 are existentially hidden, we cannot inspect these speciﬁcations: adding a side
condition to the rule that mentions the speciﬁcations G1 (f ) and G2 (f ) would
violate the abstraction principle. Nevertheless, the proof of the composition rule
still requires us to attach some speciﬁcation to the shared function, when con-
structing the witnessing context of the concluding judgment, G. Our solution is
to use intersection , i.e. to instantiate the witness G with G1  G2 in the Coq
proof of VSULink. By terminating the Coq proof script with Qed rather than
Deﬁned, this instantiation is opaque to clients: applications of VSULink during
program veriﬁcation merely see that some G exists.
     Most side conditions of the rule are computational; in our applications of the
rule in Sections 4.5 and 5, Coq’s tactical engine solves the majority of them.


4     APDs and speciﬁcation interfaces

We now turn to the organization of predicates and function speciﬁcations. Our
organization reﬂects typical realizations of abstraction principles in C, where
heap data structures are introduced using forward declarations and referred to
via pointers in header ﬁles, while the selection of a concrete representation (per-
haps using private static variables) is private to an implementation. We illus-


                                              #include ”Connection.h”
typedef struct database ∗Database;
                                              typedef struct pool ∗Pool;
typedef struct connection ∗Connection;
                                              Pool consPool (Database d);
Connection consConn (Database d);
                                              Connection getConn (Pool p);
Database newDB (int DBidentiﬁer);
                                              void freeConn (Pool p, Connection c);


    Fig. 2. Connection pools in C: Connection.h (left) and Connectionpool.h (right).


trate our approach using Parkinson and Bierman’s connection pool example [56],
126     L. Beringer

ported to C as an implementation of the APIs in Figure 2. Using forward declara-
tions, the header ﬁles reveal only minimal information about the implementation.
Connection.h allows clients to create a database entity (the parameter denotes
a unique identiﬁer; Parkinson and Bierman omit this constructor and do not
model the type database explicitly) and to create connections to a database us-
ing the constructor consConn. Connectionpool.h models a collection of (dormant)
connections associated with a database; clients construct a pool using consPool,
request connections using getConn, and return them using freeConn.


4.1   Abstract predicate declarations (APDs)

Figure 3 introduces abstract predicate declarations for the three data structures.
Each APD declares zero or more spatial predicates, i.e. mpreds relating a Comp-
Cert (pointer) value to suitable semantic information. Semantic information for
the database is a DBindex (eﬀectively a mathematical integer); connection and
pool structures maintain pointers to the database; connections have additional
internal state represented by the (abstract) type ConnTP.


Record DatabaseAPD := {                 Record ConnectionAPD := {
 DB: DBIndex → val → mpred;              ConnTP:Type;
 DB-ptrnull: ∀ db s, DB db s            Conn: (val ∗ ConnTP) → val → mpred;
    !!(is-pointer-or-null s) }.          NextConn: ConnTP → globals → mpred;
Record PoolAPD := {                      Conn-isptr: ∀ C c, Conn C c  !!(isptr c);
 CPool: val → val → mpred;               Conn-validptr: ∀ C c, Conn C c 
 CPool -ptrnull: ∀ d p, CPool d p                      valid-pointer c }.
    !!(is-pointer-or-null p) }.

  Fig. 3. APDs for the connection pool example. val is CompCert’s type of values.


    Speciﬁcally, DatabaseAPD corresponds to the Database type declaration in
Connection.h and asserts existence of a predicate DB, together with an axiom
that enables clients to store a reference to a database in their own data structure.
Operator !! injects a Coq proposition into VST’s assertion language.
    In similar style, ConnectionAPD and PoolAPD declare predicates Conn and
CPool for the struct declarations connection and pool. In contrast to Parkinson
and Bierman, we model that the connection module maintains state using the
predicate NextConn. There is no need to reveal the concrete static variable
used by our implementation though: globals denotes the collection of all such
variables in VST. We assert that the head values of Conn and CPool are provably
nonnull pointers and that a Conn’s head pointer is furthermore valid.
    All APDs are introduced as (dependent) Record types in Coq. We will con-
struct values of these types in Section 4.3, i.e. implementation-dependent con-
crete predicate deﬁnitions and lemmas validating the axioms. But ﬁrst, we use
the APD types abstractly to introduce speciﬁcations for the two modules.
                                                      Veriﬁed Software Units      127

4.2   Abstract speciﬁcation interfaces (ASIs)

Abstract speciﬁcation interfaces (ASIs) consist of VST speciﬁcations for the API-
exposed functions, parametric in all relevant APDs. In addition to the APDs
introduced above, our example uses a third APD, denoted M, that declares an
abstract predicate MemM gv and represents the malloc/free library.
    Figure 4 shows the ASI of Connection.h. We use subscripts to refer to the
APD parameters: for example, DBD i p is the mpred obtained by applying the
DB component of a database APD D to index i and pointer value p.


Function        Spec
newDB(i; gv)    {MemM gv} ; {p. DBD i p ∗ MemM gv}
consConn(d; gv) {DBD i d ∗ NextConnC c gv ∗ MemM gv} ;
                    if p = null then NextConnC c gv ∗ DBD i d ∗ MemM gv
                 p.
                    else ∃c . NextConnC c gv ∗ ConnC (d, c) p ∗ DBD i d ∗ MemM gv

Fig. 4. ASI for Connection.h, parametric in databases (D), connections (C), and mem-
ory systems (M). MemM gv represents M’s abstract predicate for a memory manager
that is accessed by malloc and free.


    A speciﬁcation F(x; gv) : {Pre} ; {v . Post} is to be understood in safety-
guaranteeing partial-correctness style, where x denotes a list of actual arguments
(of type val), gv refers to (if present) the global environment, v (again of type val)
represents the return value (if present), and other items are implicitly universally
quantiﬁed. Callers of such a function select instantiations for the universally
quantiﬁed entities (“witnesses”) and must then establish Pre.
    Thus, the speciﬁcation of newDB asserts that a new database entity satisfying
DBD i p is allocated at the return value p, for the database with index i (an input
argument). The allocation draws upon the abstract predicate MemM gv which
is “located” at some global variable that is private to the malloc/free library.
    The speciﬁcation of constructor consConn refers to MemM gv in similar fash-
ion and advances the module’s connection counter from c to some c upon success;
in contrast to Parkinson and Bierman, we also support unsuccessful requests.
    The ASI for Connectionpool.h in Figure 5 is additionally parametric in an
PoolAPD, P. Our speciﬁcations are again slightly more precise than the ones
given by Parkinson and Bierman. As a consequence, the precondition of a se-
quence such as p := consPool(s); c := getConn(s); freeConn(p, c) is DBD i d ∗
MemM gv ∗ NextConnC s gv rather then emp, hence exposing the reliance on
the memory manager etc..Preﬁxing the instruction d := newDB(i) establishes
DBD i d; we will explain how the latter two conjuncts are provided in Section 4.5.


4.3   Veriﬁcation of ASI-speciﬁed compilation units

Substantiating the ASI of a header ﬁle, means to give – for a concrete implemen-
tation – concrete deﬁnitions for the predicates in the newly introduced APDs,
128     L. Beringer

Function           Spec
consPool(d; gv)    {MemM gv} ; {p. CPoolP d p ∗ MemM gv}
getConn(p; gv)     {CPool
                     ⎧ P d p ∗ DBD i d ∗ NextConnC c gv ∗ MemM gv} ⎫
                     ⎨ CPoolP d p ∗ DBD i d ∗ MemM gv∗                       ⎬
                   ; n. if n = null then NextConnC c gv
                     ⎩                                                       ⎭
                          else ∃c c . NextConnC c gv ∗ ConnC (d, c ) n
freeConn(p, i; gv) {CPoolP d p ∗ ConnC (d, c) i ∗ MemM gv} ; {CPoolP d p ∗ MemM gv}

Fig. 5. The ASI for Connectionpool.h is parametric in a database APD (D), a con-
nection APD (C), a connection pool APD (P), and a memory manager APD (M). As
consPool takes a formal parameter d, the reader may have expected the speciﬁcation
{DBD i d ∗ MemM gv} ; {p. CPoolP d p ∗ DBD i d ∗ MemM gv} which is indeed derivable
from the one given using VST’s frame rule.


show that these deﬁnitions validate the associated axioms, and ﬁnally construct
a VSU that has the ASI’s speciﬁcations as the export interface E. All these
constructions are parametric in the APDs provided by other modules.
     We refer the reader to our source code [14] for the C implementation, the (con-
crete) predicate deﬁnitions, and the proofs of the APD-supporting axioms. In
case of Connection.c, these proofs reveal the instantiation of the APD’s ConnTP
to Coq’s type of integers, Z, corresponding to the existence of a global integer
variable in the C code that maintains a connection counter; the corresponding
   .
.→− . . predicate then furnishes the abstract predicate NextConn.
     The substantiations of a unit’s APDs are subsequently used to instantiate
its ASI and the speciﬁcations of its imported function, yielding (together with
speciﬁcations of private functions) a proof context G that the unit’s local function
bodies are then veriﬁed against. APDs provided by other compilation units are
left abstract, so expose only their axioms. Speciﬁcally, the substantiation for
Connection.c yields values c and d of types ConnectionAPD and DatabaseAPD,
respectively, the predicate N = NextConn c 0, and a VSU

                    VSUConn = ∅N [IConn ] Connection.prog [EConn ]
                                 def




where EConn is the partial specialization of the speciﬁcations in Figure 4 to C
= c and D = d, Connection.prog is CompCert’s AST for Connection.c, and
IConn contains a speciﬁcation for surelymalloc. For ConnectionPool.c, we similarly
obtain a value p of type ConnectionpoolAPD and a VSU

                  VSUPool = ∅emp [IPool ] Connectionpool .prog [EPool ],
                           def




where IPool is comprised of the (abstract) speciﬁcation of consConn and speciﬁ-
cations for free and surelymalloc, and EPool is the partial specialization of Figure 5
to P = p. Both VSUs are parametric in M, but VSUPool ’s additional parame-
ters D and C are instantiated when VSUConn and VSUPool are combined using
rule VSULink. The result, VSUCP , is still parametric in M but has resolved the
imports of consConn, leaving only imports for free and surelymalloc.
                                                        Veriﬁed Software Units     129

4.4   A VSU for a malloc-free library

A recent application of VST is Appel and Naumann’s veriﬁcation of a malloc/free
library [5]. Internally maintaining a ﬁxed number of freelists – for entities of
diﬀerent size – this library exposes four functions in its API: malloc, free, pre-ﬁll,
try-pre-ﬁll. When porting this development to the VSU framework, these give
rise to two ASIs. The ﬁrst one contains speciﬁcations for all four functions and
is suitable for resource-aware clients. It employs the APD MallocFree-R-APD:
Record MallocTokenAPD := {
 malloc-token’: share → Z → val → mpred;
 malloc-token’-valid-pointer: ∀ sh sz p, malloc-token’ sh sz p  valid-pointer p;
 malloc-token’-facts: ∀ sh sz p, malloc-token’ sh sz p  !! malloc-compatible sz p }.
Record MallocFree-R-APD :=
 { MF-Tok-R :> MallocTokenAPD; mem-mgr-R: resvec → globals → mpred }.

mem-mgr-R models the freelists as a resource vector that indicates the length
of each freelist. The predicate malloc token’ refers to the piece of memory that
is typically located at a small negative oﬀset of a malloc’ed entity and holds
administrative information of the library, but conceptually, it also constitutes
a token that enables clients to share malloc’ed entities among diﬀerent threads
without loosing the ability to safely free entities. The second ASI only exposes
malloc and free, and employs the more abstract APD
Record MallocFreeAPD :=
 { MF-Tok :> MallocTokenAPD; mem-mgr: globals → mpred }.

MF-Tok still presents a malloc token but mem-mgr now hides the existence of
freelists - indeed, constructing a MallocFreeAPD from a MallocFree-R-APD simply
quantiﬁes existentially over a resource vector. Our proofs ﬁrst refactor the prior
veriﬁcation as a VSU that exports a resource-aware ASI and then use VSUCon-
seq (and export restriction  from Section 3.2) to weaken the resulting VSU
to a VSU that only exports a resource-ignorant ASI. We denote the latter as
VSUMF ; the predicate MemM gv is now revealed to be a shorthand for mem-mgr
gv, parametric in a MallocFreeAPD M, and we use MemMF gv below to refer to
its instantiation for VSUMF .


4.5   Putting it all together

Using VSULink again, we link VSUCP with a library VSU (reducing surelymalloc
to malloc and the system function exit) and then with VSUMF , obtaining

                    VSUAppLib = SMem
                                defCore
                                        MF ∗N
                                              [ ] coreprog [ECore ].
Here, coreprog contains all code (application plus library) with the exception of
main. Note that VSUAppLib ’s set of imports is empty; SCore contains axiomatic
speciﬁcations of OS functions such as exit and mmap.
   Independent from the construction of VSUAppLib we verify main, i.e. an exem-
plary client or unit test, as a semax body statement w.r.t. a not yet instantiated
130     L. Beringer

copy of ECore . The speciﬁcation that main is veriﬁed against a <: specialization
of VST’s general main-spec but is still abstract in the APDs of the application’s
code modules – see [14] for details.
    Finally, we connect VSUAppLib with the veriﬁcation of main to obtain a proof
of VST’s semax prog statement. It is in this last proof that the satisfaction of
the abstract initialization predicates for the global variables, MemMF and N , is
established from VST’s internal initialization predicates.


5     Modular veriﬁcation of the Subject/Observer pattern

Programs in imperative or object-oriented languages often contain callbacks:
chains of function calls A.m() → B.n() → A.l() between modules A and B in
which m’s invocation of n (and hence the return of control to A in the call to
l) happens when A’s state is invalid, i.e. does not satisfy A’s invariant. Clearly,
mandating satisfaction of the invariant in l’s precondition – a typical requirement
of API-level speciﬁcations – then prevents the veriﬁcation of n.
    A typical example is the chain update → notify → get in the subject-observer
pattern, a widely used design pattern [23] that has served as a litmus test for
modular speciﬁcation of callback-rich programming in the literature. Figures 6
and 7 contain excerpts of a transcription of Parkinson’s [55] code into1 C. Each
Subject maintains a list of subscribers – a list of observers that will be notiﬁed
whenever the Subject’s state is updated and then synchronize their internal state
accordingly using get. The intended invariants express that each Subject’s ob-
servers are in sync – a property that is violated during update’s traversal of its
observer list, when not-yet-notiﬁed observers are out of sync but (precisely in
order to get back in sync) nevertheless invoke get.
    The dominant technique for dealing with such situations in SMT-based tools
employs ghost ﬁelds that track validity and unfolding of invariants and are sup-
ported by further (ghost) infrastructure that controls ownership (see e.g. [47,11]).
However, this does not necessarily achieve comprehensive representation hiding:
for example, the permission to violate Subject’s invariant in get’s precondition
propagates to the precondition of notify, allowing the latter function to access
the ﬁeld2 Subject.value. Furthermore, the invariant-regulating techniques typi-
cally require that SMT solving be carried out on a whole-program basis.
    The ﬂexibility of APDs to introduce multiple predicates enables an alter-
native in which callbacks are speciﬁed using special-purpose predicates that –
similar to typestates [62] – emphasize protocol-style behavior, do not reveal the
1
  Our implementation [14] contains two further callbacks, newObs → registr → notify
  and registr → notify → get; the former one commences in the constructor, before
  any invariant has been established.
2
  For example, one may insert abstraction-violating get/putﬁeld instructions in the
  subject-observer code at http://comcom.csail.mit.edu/e4pubs/{#}observer. This
  tool implements an advanced variant of invariance regulation using ghost instruc-
  tions, semantic collaboration [59], for Eiﬀel. Fields are not private, and the method-
  ology does not prevent representation exposure between such closely coupled classes.
                                                      Veriﬁed Software Units      131


/∗ SubjectObserver.h ∗/                       /∗ Subject-rep.h ∗/
typedef struct subject ∗Subject;              #include ”SubjectObserver.h”
typedef struct observer ∗Observer;            typedef struct node ∗Node;
                                              struct node {
/∗ Subject.h∗/                                   Observer obs;
#include ”SubjectObserver.h”                     struct node ∗ next;
Subject newSubject (void);                    };
void registr (Subject s, Observer o);         struct subject {
void update (Subject s, int n);                  Node obs;
int get (Subject s);                             unsigned value;
int freeSubject(Subject s);                   };
Observer detachﬁrst(Subject s);
                                              /∗Observer-rep.h∗/
/∗Observer.h ∗/                               #include ”SubjectObserver.h”
#include ”SubjectObserver.h”                  struct observer {
Observer newObs (Subject s);                     Subject sub;
void notify (Observer o);                        int cache;
int val (Observer o);                         };
void freeObserver (Observer o);


Fig. 6. Subject/Observer: header ﬁles. The left column shows the public APIs; Sub-
ject rep.h and Observer rep.h are private to their respective module implementations.


/∗ Subject c ∗/                                       /∗ Observer.c ∗/
#include ”surelyMalloc.h”                             #include ”surelyMalloc.h”
#include ”Observer.h”                                 #include ”Observer.h”
#include ”Subject.h”                                  #include ”Subject.h”
#include ”Subject-rep.h”                              #include ”Observer-rep.h”

int get (Subject s) { return (s→ value); };           void notify (Observer o) {
void update (Subject s, int v) {                        o → cache = get(o → sub);
  s→ value = v; Node n = s → obs;                       return; }
  while (n) { notify(n→ obs); n = n → next; } }

Fig. 7. Excerpts from Subject.c and Observer.c for the callback update → notify → get.


validity of module invariants, and maintain representational hiding by being just
as abstract as a module’s main predicate.
    Concretely, our approach employs semantic subjects that are comprised of a
list of observer references and a (current) value, while observers are represented
as a subject pointer and the cache:
Deﬁnition SubjRep:= (list val) ∗ Z.      Deﬁnition ObsRep := val ∗ Z.

Next, our APDs complement the predicates relevant for API calls by external
clients, Srep and Orep, by (residual) predicates for calling the Subject functions
registr, update, and get, and the Observer functions notify and val; we also intro-
132      L. Beringer

duce a predicate for the postcondition of get, GetPost:
Record SubjectAPD := {
 Srep, RegPre, UpdPre, GetPre, GetPost: SubjRep → val → mpred;
 SubjRegister: ∀ S s, Srep S s  RegPre S s;
 SubjUpdate: ∀ S s, Srep S s  UpdPre S s;
 SubjGetPrePost: ∀ S s, Srep S s  GetPre S s ∗ (GetPost S s -∗ Srep S s);
 GetPre-ptrnull: ∀ S s, GetPre S s  !!(is-pointer-or-null s) }
Record ObserverAPD := { Orep, NtfPre, ValPre: ObsRep → val → mpred;
 ObsNtfy: ∀ O o, Orep O o  NtfPre O o; ObsVal: ∀ O o, Orep O o  ValPre O o;
 NtfPre-isptr: ∀ O o, NtfyPre O o  !!(isptr o) }
Entailment axioms such as SubjUpdate permit external clients to invoke callback
functions directly but may be omitted for functions that should only be invoked
via callbacks. The residual predicates sanction indirect invocations via callbacks
without revealing the satisfaction status of module-internal invariants.
    Axiom SubjGetPrePost splits Srep into a token that can (only) be used to
invoke get, plus a token for reestablishing Srep from GetPost. The latter is a sep-
arating implication −∗ rather than an entailment: it represents the requirement
that an observer yields back control to its subject after completing a callback to
get – the subject had retained part of its state prior to invoking notify.
    To enforce these behaviors, we employ the speciﬁcations in Figures 8 and 9;
again, the ASIs are parametric in all APDs mentioned, notwithstanding the
mutual dependence of the modules. Using axiom SubjGetPrePost, one may show


Function     Spec
update(s, v) {UpdPreSP (l, z) s ∗ Observers NtfPreOP s vals l}
             ; {SrepSP (l, v) s ∗ Observers OrepOP s v |l| l}
get(s)       {GetPreSP S s} ; {p. !!(p = snd (S)) && GetPostSP S s}

Fig. 8. ASI of Subject (excerpt), parametric in a SubjectAPD (SP), an ObserverAPD
(OP), and a MemoryAPD (M).


that the speciﬁcations for get and notify are in subsumption relationship with
large-footprint counterparts that permit invocations by external clients:
                           {SrepSP S s} ; {p. !!(p = snd S) && SrepSP S s}
      {NtfPreOP (s, c) o ∗ SrepSP S s} ; {OrepOP (s, snd S) o ∗ SrepSP S s}
The speciﬁcation of update makes reference to an auxiliary Coq function that
represents the “big” separating conjunction ∗(v,o)∈combine(vals,l) P (s, v) o,
  Observers (P:ObsRep → val → mpred) (s:val) (vals: list Z) (l: list val): mpred.
   The substantiation of these interfaces relative to our C implementations de-
ﬁnes the main predicates as
                                               Ews
Deﬁnition Srep (l, v) s := ∃o. listrep l o ∗ s −−→STP (o, v ∗ Mtok(Ews, STP, s).
                            Ews
Deﬁnition Orep O o := o −−→OTP O ∗ Mtok(Ews, OTP, o).
                                                        Veriﬁed Software Units          133

Function            Spec
newObs(s; gv)       {RegPreSP S s ∗ MemM gv} ;
                    {p. OrepOP (s, snd S) p ∗ SrepSP (p :: fst S, snd S) s ∗ MemM gv}
notify(o)           {NtfPreOP (s, c) o ∗ GetPreSP S s} ;
                    {OrepOP (s, snd S) o ∗ GetPostSP S s}
val(o)              {ValPreOP (s, c) o} ; {c. OrepOP (s, c) o}
freeObserver(o; gv) {OrepOP O o ∗ MemM gv} ; {MemM gv}

           Fig. 9. ASI of Observer, parametric in APDs SP, OP, and M.


Here, listrep is a typical list representation predicate over Node items, modeling
the observers associated with a Subject. STP and OTP are shorthands for Clight’s
representation of the struct deﬁnitions Subject and Observer, Ews represents
an exclusive writable share in VST, and Mtok(., ., .) is a variant of predicate
malloc-token’ from Section 4.4.
   Some residual predicates are minor variants of Srep and Orep. For example,
                                                         Ews
Deﬁnition NtfyPre O o := Mtok(Ews, OTP, o) ∗ ∃v. o −−→OTP (fst O, v).
existentially abstracts over snd O but is otherwise identical to Orep. This makes
validating axiom ObsNtfy trivial. As NtfyPre does not depend on a subject’s value,
no modiﬁcation of the latter can aﬀect the former’s. Other residual predicates –
like RegPre – are even deﬁnitionally equal to the main predicates, but the APD
mechanism ensures that this fact is not exposed to clients.
    Our C implementation permits GetPre and GetPost to actually be deﬁned
identically (indeed, getters typically don’t alter data structures. . . ):
                                                Ews
  Deﬁnition GetPrePost (l, v) s := s.value −−→STP v ∗ Mtok(Ews, STP, s).
                sh                         sh
Here, the p.π −→t v is a variant of p −→t v that speciﬁes the content at p.π,
where path π is a list of ﬁeld names and array subscripts. Thus, GetPrePost only
speciﬁes the content of s.value; the remaining portion of s is exactly what is
retained when SubjGetPrePost splits oﬀ GetPre from a Subject. The motivation
for this handling is that the invariant of the loop in update (which contains the
callback to get via notify) only traverses the node list. Speciﬁcally, an invari-
ant involving the full Srep would not ensure that the spine of the list remains
unchanged, as the deﬁnition of Srep quantiﬁes existentially over the node list.
This aspect illustrates the danger of predicates that are too abstract to be useful.
    Constructing VSUs for Subject and Observer proceeds straight-forwardly;
we exercise VSU’s support for shared libraries by ﬁrst combining surelyMalloc
with each of these VSUs separately, before linking the resulting VSUs with each
other, with VSUMF , and with a main client as described in Section 4.5.

5.1   Speciﬁcation and proof reuse
To evaluate speciﬁcation modularity and proof reuse, we veriﬁed several varia-
tions of our implementation. First, to evaluate robustness under representational
change, we have Subject internally maintain a freelist of Observer nodes:
134       L. Beringer

struct subject { Node ﬂ; Node obs; unsigned value; };
The freelist is drawn upon in registr (we only invoke surely-malloc if ﬂ is null)
and replenished in detachﬁrst. Constructor newSubject creates an empty freelist,
and freeSubject frees the entire list.
    The code modiﬁcation triggers new Clight ASTs, but the majority of Coq
ﬁles can then simply be reprocessed: the model-level deﬁnitions, APDs, and
ASIs of Subject and Observer remain unchanged, and so do the ﬁles associated
with verifying Observer, linking, and main. The only modiﬁcations are in the
implementation-dependent validation of Subject, namely in the deﬁnitions of the
representation predicates and in the VST proofs of the individual functions.
    Second, we veriﬁed a variant in which notify’s invocation of get is replaced
by a function pointer. The key code modiﬁcations are
      /∗Addition in SubjectObserver.h∗/      /∗Modiﬁcation in Observer.h∗/
      typedef int (∗callback)(Subject s);    void notify (Observer o, callback f);
      /∗Modiﬁcation in Observer.c∗/
      void notify (Observer o, callback f) { o → cache = f(o → sub); return; };
   The calls to notify in update and registr obtain the additional argument &get,
and the speciﬁcation of get can be removed from the imports of the Observer
VSU. The small speciﬁcation of notify becomes
                            {NtfPre (s, c) o ∗ GetPreSP S s ∗ funcptr φget g}
           notify(o, g) :
                            ; {OrepOP (s, snd S) o ∗ GetPostSP S s}

where funcptr φ g expresses that value g is a pointer to some function satisfying
speciﬁcation φ, and φget is the entry for get from Fig. 8. notify’s large speciﬁcation
is adapted similarly. Repairing the proofs incurs changes in < 10 lines of Coq.
     A third modiﬁcation exploits VST’s support for impredicative quantiﬁcation
to abstract over GetPreSP and GetPreSP in the deﬁnition of φ, such that notify’s
speciﬁcation is eﬀectively parametric in suitable GetPre/GetPost pairs. Adapt-
ing the veriﬁcation involves step-indexed aspects of VST and hence requires a
little more work; details are included in the Coq development [14].
     Finally, we veriﬁed a variation in which observers register with two subjects,
as an example of a more complex interaction pattern. As this aﬀects model-level
functionality, modiﬁcations are not conﬁned to module-internal predicate deﬁ-
nitions but aﬀect APDs declarations and ASI deﬁnitions. However, neither the
encapsulation of representation nor the modularity of veriﬁcation were compro-
mised; supporting more than two subjects per observer would likely be similar.

5.2     Pattern-level speciﬁcation
An alternative speciﬁcation of subject-observer was proposed by Parkinson [55],
who sidesteps the conﬂict between callbacks, modularity, and abstraction. Giv-
ing up on specifying the two classes independently, this approach deﬁnes a single
abstract predicate, SubObs, that ties a subject to all its observers and yields
aggregate-level function speciﬁcations. We can recover such an aggregate inter-
face by proving that the speciﬁcations involving SubObs are abstractions (in the
                                                      Veriﬁed Software Units      135

sense of . <: .) of the exports of the SubjectObserver VSU, generically in APDs
SP and OP. Indeed, Parkinson’s formulation amounts to a two-predicate APD:
Record AggAPD :=
 { Sub: val → list val → Z → mpred; Obs: val → val → Z → mpred }.

with speciﬁcations shown in Figure 10, using the derived notions
  Deﬁnition SubObs s O v := Sub s O v ∗ ∗o∈O Obs o s v.
  Deﬁnition Obs o s := ∃v. Obs o s v. (∗ Obs is related to Obs as →      is to →. ∗)
  Deﬁnition SubObs s O := ∃v. SubObs s O v.



Function          Spec
newSubject(gv) {MemM gv} ; {s. SubObs A s nil ∗ MemM gv}
registr(s, o; gv) {SubA s O v ∗ Obs A o s ∗ MemM gv}
                  ; {SubA s (o :: O) v ∗ ObsA o s v ∗ MemM gv}
update(s, v)      {SubObs A s O} ; {SubObsA s O v}
get(s)            {SubA s O v} ; {v. SubA s O v}
newObs(s; gv) {SubObsA s O v ∗ MemM gv} ; {p. SubObsA s (p :: O) v ∗ MemM gv}
notify(o)         {SubA s O v ∗ Obs A o s} ; {SubA s O v ∗ ObsA o s v}
val(o)            {SubObsA s O v} ; {v. SubObsA s O v}

Fig. 10. Selected aggregate speciﬁcations, parametric in an AggAPD A. Except for the
occurrence of MemM gv, the speciﬁcations coincide with Parkinson [55]’s speciﬁcations.


Constructing an AggAPD A from a SP/OP pair is trivial: take Sub to be SrepSP
and Obs to be OrepOP ; proving the . <: . lemmas is then straight-forward.
    SubObs constitutes a pattern invariant, or the pattern’s primary predicate,
with residuals Sub and Obs. From the aggregate’s point of view, update → notify
→ get is not a callback but an internal nesting of invocations, so the small-
footprint speciﬁcations typically don’t pose a problem for existing methodolo-
gies; client-visible speciﬁcations with large footprints can be derived using the
frame rule. In this sense, the pattern reestablishes “sequential atomicity” of op-
erations. Exploring whether other design patterns can be similarly derived from
the ASIs of their constituent classes is a topic for future research: are typical de-
sign patterns the abstraction units at which sequential atomicity is reestablished,
callbacks at most occur in valid states, and residual predicates are avoided?
    An aggregate speciﬁcation for the function pointer implementation from Sec-
tion 5.1 can be obtained using a modiﬁed AggAPD, with residual predicates
GetPre etc.. But a better option is to remove the pattern-internal functions
notify, registr, and perhaps even get from the aggregate ASI. In fact, notify’s
new signature reveals the use of function pointers, hence even an aggregate-level
speciﬁcation would have to include funcptr φ g terms. Thus, we instead employ
the notion  from Section 3.2 to lift the VSU for SubjectObserver with function
pointers from Section 5.1 to a VSU for the aggregate but narrowed ASI and then
reverify main w.r.t the latter.
136     L. Beringer

6     Veriﬁcation of object principles

This section considers features that – together with state encapsulation and
modularity – are cornerstones of object orientation: the ability for (instances
of) multiple implementations of an interface to dynamically coexist and inter-
act, dynamic dispatch, subtyping, self, and inheritance. To maintain the dataless
discipline, we employ a uniform but simple object encoding that is typical for
industrial and open-source C developments: dynamic dispatch is implemented
using function pointers that are bundled into separate structs (method tables)
that are accessible as the ﬁrst element of the object representations. Subtyping
– providing additional methods – and representation inheritance are modeled by
extending these structs, respectively, but are orthogonal to each other, and only
the former one is exposed in APIs. In the second half of this section, we hide the
dynamic dispatch mechanism behind a wrapper interface. We specify objects by
reference to a semantic (Coq-level) object model, thus comprehensively separat-
ing object reasoning from C-level reasoning: constructors establish, and methods
maintain, abstract object predicates that clients need not (and cannot) unfold.
    We again proceed in stages, using the widely used running example of points
located on a one-dimensional axis (see e.g. [18]). Figure 11 shows a preliminary
API for basic, bumpable, and colored points, organized in a simple subtyping
relationship. We provide multiple implementations for each interface (using dif-



typedef struct point ∗Point;                 typedef struct bmethods ∗ BMethods;
struct methods {
  int (∗get) (Point);                        typedef struct cpoint ∗CPoint;
  void (∗set) (Point, int); };               struct cmethods {
typedef struct methods ∗ Methods;              int (∗get) (Point);
                                               void (∗set) (Point, int);
typedef struct bpoint ∗BPoint;                 void (∗bump) (BPoint);
struct bmethods {                              int (∗getC) (CPoint); };
  int (∗get) (Point);                        typedef struct cmethods ∗ CMethods;
  void (∗set) (Point, int);                  struct point { Methods mtable; };
  void (∗bump) (BPoint); };                  struct bpoint { BMethods mtable; };
typedef struct bmethods ∗ BMethods;          struct cpoint { CMethods mtable; };

    Fig. 11. PointInterface.h, containing three interfaces for one-dimensional points



ferent data representations), each exposing its set of constructors in a separate
header ﬁle - Figure 12 shows implementation I1. Clients select an implemen-
tation during object creation but cannot otherwise distinguish between them:
method dispatch selects the appropriate function from the method table, as in
BPoint bp = makeBPoint-I1(4); int i = ((BMethods)(bp→mtable))→get((Point)bp)).
                                                      Veriﬁed Software Units        137


struct point-I1 {          struct bpoint-I1 {          struct cpoint-I1 {
  Methods mtable;            BMethods mtable;            CMethods mtable;
  int value; };              int value; };               int value; int color; };

int get-I1 (Point p) { return (((struct point-I1 ∗)p)→ value); }
void set-I1 (Point p, int i) { ((struct point-I1 ∗)p)→ value = i; return; }
void bump-I1 (BPoint p) { ((struct bpoint-I1 ∗)p)→ value++; return; }
int getC-I1 (CPoint p) { return (((struct cpoint-I1 ∗)p)→ color); }
BPoint makeBPoint-I1 (int i) {
  struct bpoint-I1 ∗p = (struct bpoint-I1 ∗)surely-malloc(sizeof ∗p);
  BMethods m = (BMethods)surely-malloc(sizeof ∗m);
  m → get = &get-I1; m → set = &set-I1; m → bump = &bump-I1;
  p → value = i; p → mtable = m; return ((BPoint)p); }

Fig. 12. Implementation I1. Constructors makePoint-I1 and makeCPoint-I1 omitted.
A second implementation I2 employs representations point-I2 etc. and exposes con-
structors makeBPoint-I2 etc.


   The basis of object speciﬁcations is a general method table predicate:
  MTable(T, k , names, m, specs, I) =
                                     Mtok(Ews, k , m) ∗
   ∃ π.!!(readable(π)) && ∗(μ,φ)∈names×specs ∃ v.funcptr(φ I, v) ∗ m.μ →πk v.

It asserts that the struct m (of shape k ) contains at ﬁeld names names pointers
to functions satisfying specs, where I is of Coq-type Pred(T) = (T∗val) → mpred
and specs has type list (Pred(T) → funspec). A generic object layout predicate

        N T tbl (σ k : type) names specs (x : T ∗ val) : mpred =
         ∃ δ I. I x ∗ Mtok(Ews, δ, snd x) ∗
            ∃ m. (snd x).tbl →Ews
                               σ   m ∗ MTable(T, k , names, m, specs, I)

then combines a speciﬁed method table (located at ﬁeld tbl ) with the requirement
that the (memory identiﬁed by the) object pointer satisfy I. C types σ and δ
represent the object’s static and dynamic types. The joint use of I in MTable
and N ensures that an object’s methods agree with its data component on what
representation predicate should be maintained. The existential abstraction over
I ensures representation hiding: external clients merely see a invariant of (Coq)
type T . Thus, diﬀerent C implementations of an object interface may employ
diﬀerent representations but still satisfy the same external speciﬁcation.
   Speciﬁcally, we introduce Coq-level object interface types in the style of Hof-
mann and Pierce’s object model [30]:
Record PointM (X:Type):Type := { get : X → Z; set : X → Z → X; }
Record BPointM (X:Type):Type :=
  { PointM-of-BPointM :> PointM X; bump : X → X; bumpable : X → Prop; }.
Inductive Color:Type := blue | red | green.
Record CPointM (X:Type):Type :=
  { BPointM-of-CPointM :> BPointM X; getC: X → Color; color-code: Color → Z; }.
138    L. Beringer

The parameters X represent semantic object representations. On the one hand,
we may instantiate these and deﬁne Coq-level behaviors, like m1, bm1, cm1:
Record PointRep := { value : Z }.
Record CPointRep := { pointRep :> PointRep; color : Color }.
Deﬁnition m1: PointM PointRep :=
  {| get := fun s ⇒ value s; set := fun s i ⇒ {| value := i |} |}.
Deﬁnition bm1: BPointM PointRep :=
 {| PointM-of-BPointM := m1; bump := fun s ⇒ {| value := value s + 1 |};
    bumpable := fun s ⇒ min-signed ≤ value s < max-signed |}.
Deﬁnition cm1: CPointM CPointRep := {| ... (∗details omitted∗) |}

But the interface types also enable speciﬁcations for get(p) and set(p, j):
     get spec T (P : PointM T ) = λI : Pred T. {I(t, p)} ; {get T P t. I(t, p)}
     set spec T (P : PointM T ) =
                                 λI : Pred T.
          {min signed ≤ j ≤ max signed & I(t, p)} ; {I(set T P t j, p)}
Thus, each method has a Coq-level counterpart that is parametric in (semantic)
representations and behaviors. To specify the constructors, we ﬁrst deﬁne spe-
cializations of N for the three interfaces by instantiating with the appropriate
method speciﬁcations and syntactic elements:

   P T (P : PointM T ) : Pred T =
       N T mtable point methods [get; set] [get spec T P ; set spec T P ]
   B T (B : BPointM T ) : Pred T =  
       N T mtable bpoint bmethods [get; set; bump]
                                                                           .
            [get spec T B ; set spec T B ; bump spec T B ]
   C T (C : CPointM T ) : Pred T = 
       N T mtable cpoint cmethods [get; set; bump; getC]
            [get spec T C ; set spec T C ; bump spec T C ; getC spec T C ]

Here, point, bpoint, cpoint and methods, bmethods, cmethods are the structs
deﬁned in the header ﬁle (Figure 11) and mtable, get, . . . , getC are the ﬁeld
names in these structs. The exemplary spec for base point constructors is then
   makePoint(i; gv) : {min signed ≤ i ≤ max signed & MemM gv}
                      ; {p. MemM gv ∗ P T P (Init Point(i), p)}.
   Verifying I1 and I2 then yields VSUs whose export interfaces tie makePoint-I1
makePoint-I2 to the specialization of this constructor to P := m1, and similarly
for the other constructors. The resulting objects behave indistinguishably; the
existential quantiﬁcation over I in the deﬁnition of N carries over to P, B, and
C, ensuring that the representational diﬀerences between I1 and I2 are hidden
from clients: when verifying a method call, clients unroll P etc., but each time
receive a “fresh” symbolic representation predicate I.

Wrapper-based veriﬁcation The unrolling of object predicates corresponds to the
exposure of the method table in our API. Programmatically, better encapsulation
is provided by wrappers that hide the function pointer mechanism, like
int GET (Point p) { Methods m = p→ mtable; return (m→ get(p)); }
                                                     Veriﬁed Software Units     139

The header ﬁle for these wrappers resembles the API of an ADT, but merely
disguises object-orientation: we still support multiple implementations (using
the same constructors as above), and operations are still invoked using dynamic
dispatch. On the speciﬁcation side, wrappers can be modeled as an APD
Record WrapperAPD := { Wr-Pt: ∀ T, PointM T → Pred T;
 Wr-BPt: ∀ T, BPointM T → Pred T;      Wr-CPt: ∀ T, CPointM T → Pred T }.

with one constructor per interface, in resemblance to the use of class names to
index predicate families [56]. The VSU for the wrapper then encapsulates the
object predicates P etc., exporting an ASI with speciﬁcations such as

            {Wr Pt W T P (t, p)} ; {get T P t. Wr Pt W T P (t, p)} ∧
   GET(p) : {Wr BPt W T P (t, p)} ; {get T P t. Wr BPt W T P (t, p)}∧
            {Wr CPt W T P (t, p)} ; {get T P t. Wr CPt W T P (t, p)}

We can further improve client-side usability by replacing these intersection spec-
iﬁcations by a deep embedding of the three interface alternatives; this eliminates
a corresponding case distinction in client-side proofs, when symbolic execution
reaches the invocation of a wrapper function. As an example, we veriﬁed a linked
list module that permits insertion of basic, bumpable, or colored points and pro-
vides map operations that apply SET, BUMP, . . . to all elements. Each element
may internally employ I1 or I2. Of course, the precondition of mapping BUMP
requires all elements to be of dynamic type (at least) BPoint and have a bumpable
coordinate; however, this condition emerges as a constraint on semantic objects
and can be discharged without unfolding object representation predicates.

Self and late binding Veriﬁcation using the above constructions fails for methods
whose body contains virtual calls on self : the deﬁnition of N eﬀectively separates
the object’s data region from the method table upon method entry, making only
the former accessible inside the body. To overcome this limitation, we deﬁne a
variant of N using the higher-order recursive functor

   F (I X : Pred T ) : Pred T =
       λ(x : T ∗ val). ∃ δ m. I x ∗ Mtok(Ews, δ, snd x) ∗ (snd x).tbl →Ews
                                                                        σ   m
                              ∗  MTable(T, k , names, m, specs, X)

in which I is now a parameter (we eschew the parameters T, . . . , specs for read-
ability) and X plays the role of N . Recursion via X is protected by VST’s [4]
modality ; indeed, any access to a method table inside a method happens at
least one step later than the method’s own invocation. Contractiveness of F
(proven in VST) ensures the existence of a ﬁxed point F(I)
                                                              := HORec(F(I)).
Recovering the quantiﬁcation over I, we then replace N with N ∗ := ∃ I. F(I).  
With this modiﬁcation in place, one may verify virtual calls on self, like a variant
of I1 that implements bump using get and set (still w.r.t. m1, bm1, and cm1).
    An important application of self is (observably behavior-altering) method
overriding. At the semantic level, Hofmann and Pierce explicate how positive
140     L. Beringer

subtyping supports both early and late binding variants of overriding; these dif-
fer in whether the observable behavior of bump (when implemented in terms
of get and set) is aﬀected when a subclass subsequently overrides set to, say,
reset the coordinate to 0. Furthermore, method overriding may aﬀect how func-
tions deﬁned in a superclass act on subclass-introduced state components. For
example, one may impose that updating the coordinate turns a point’s color
blue. Semantically, all these variations yield novel behaviors m2, bm2, and cm2,
etc. that can be compared to the earlier behaviors using Hofmann and Pierce’s
theory. As a consequence of our two-level reasoning, and the choice to param-
eterise constructor/method speciﬁcations by behaviors, we can leverage their
techniques: implementations I3, I4. . . that realize the overriding variants can be
veriﬁed as further VSUs for our earlier export interface, by (now) specializing the
constructor speciﬁcations to m2, etc.. Afterwards, the modiﬁed behaviors prop-
agate through dynamic dispatch and wrappers as expected, permitting clients
of e.g. the list module to map bump over elements with diﬀerent behavior. Side
conditions during symbolic method calls refer exclusively to semantic objects
and behaviors, do not necessitate the unrolling of representation predicates, and
can often just be discharged using simpliﬁcation.


7     Discussion

Related and future work Certiﬁed Abstraction Layers (CAL, [24,26]) are used
in the CertiKOS project [25] to verify feature-rich operating system kernels and
hypervisors in Coq. CAL permits horizontal and vertical composition of compo-
nents, and establishes full abstraction between the imports and exports. CAL’s
methodology was recently rephrased as a synthesis from a systems-oriented DSL,
DeepSEA, to C, with a CompCert backend [64]. However, “(T)here is no use of C
pointers and no built-in support of dynamic memory allocation (every DeepSEA
object is realized as a set of static variables), so programs that need dynamic
allocation will have to implement it themselves” ([64], page 10). While this frag-
ment remarkably suﬃces for the intended application area, it is unlikely to satisfy
general-purpose programmers or compiler writers for other systems languages.
    Ironclad Apps and Ironﬂeet [29,28] are systems based on Dafny and TLA+
for verifying safety and liveness of distributed systems, and app security. By
connecting model-level, concurrency-aware reasoning, state-machine reﬁnement,
and Floyd-Hoare veriﬁcation, their approach provides abstraction-bridging func-
tionality similar to that of proof-assistant-based reasoning, trading oﬀ TCB size
and foundational integration in an logical framework against automation and
developer productivity. Ironclad Apps compile to veriﬁed assembly; Ironﬂeet
employs a formally unveriﬁed route via Dafny and the .NET compiler for C#.
    Überspark [67] is a system based on Frama-C and SMT for compositionally
verifying commodity system software written in C and assembly. Überspark’s pri-
mary applications are hypervisor components and OS kernels, but it currently
addresses only safety and security properties (memory separation, control-ﬂow
integrity, information ﬂow) rather than functional correctness. The same limita-
                                                     Veriﬁed Software Units      141

tion applies to proof-carrying code systems [49,3,6,13,27], at (virtual) machine
or assembly level. Several PCC systems proposed hierarchies of formalisms that
connect operational semantics, a general-purpose program logic, and tactical
checkers or algorithmic inference systems for higher-level type systems, abstract
interpretation, or program analyses [16,2,17,1]. VST’s tactical automation is op-
timized for symbolic execution and functional correctness, but the underlying
proof rules could equally well be used to prove soundness of static analyses or
code synthesizers; we expect our structuring principles for separate compilation
will be just as useful in these scenarios as they are for functional correctness.
    McKinna and Burstall [45] pioneered the use of existential abstraction to for-
mally tie programs to their speciﬁcations and proofs in a modern proof assistant.
VSU realizes aspects of their vision of deliverables for a mainstream language but
is at this point not endowed with similarly rigorous categorical underpinnings.
    Representation hiding in separation logic can also be obtained using hypo-
thetical frame rules [54,10], but no such rule is provided by VST at present.
Pragmatically, the two approaches appear complementary: modules that expose
interesting state (e.g. a list ADT, the point objects,...) favor existential abstrac-
tion/APDs, as clients can access associated reasoning principles on demand, at
speciﬁc program points. In contrast, modules like the resource-unaware memory
manager might beneﬁt from hypothetical framing: the predicate MemM gv car-
ries no client-relevant information but still needs to be carried around in many
function speciﬁcations in our treatment.
    VST’s speciﬁcation subsumption resembles behavioral subtyping [44,42], a
notion commonly used in veriﬁcation tools for Java-like languages for relating
speciﬁcations across a class hierarchy. Exploring the relationship between our use
of positive subtyping, other notions of subtyping and inheritance, and Liskov’s
Substitution Principle [43] constitutes future work.
    By supporting ﬁeld update, Hofmann and Pierce’s theory addresses short-
comings of purely functional object models, but its support for object aggregates
or complex ownership structures appears limited and not much studied. A two-
level encoding could likely also be developed for concurrency-inspired object
models [33,32,31], perhaps by adapting the theory of interaction trees [68,39].
However, VST’s partial-correctness interpretation of triples limits the end-to-end
usefulness of coinductive reasoning. A recent proposal for integrating statically
typed Smalltalk-inspired objects into a functional calculus is Wyvern [52].
    In the context of SMT-based veriﬁcation tools, Parkinson and Bierman [57]
highlight examples that go beyond behavioral subtyping, and Summers et al. [66]
identify a catalog of advanced uses of class invariants. We intend to apply VST
to the former soon; a better understanding of the latter could perhaps commence
by recasting Drossopoulou et al.’s general framework for object invariants [22]
in separation logic. However, some aspects of class/object invariants may not
immediately transfer from Java-like to Smalltalk-style object models.
   In Java, an object’s representation remains constant over its lifetime. By
separately quantifying over I, our pre- and postconditions may support dynamic
142     L. Beringer

representation change a la Fickle [21] (with suitable updates to the method
table), as long as both representations ﬁt into an object’s top-level struct.
    Krishnaswami et al. [41] verify subject-observer and other patterns (itera-
tors, ﬂyweight, factory) by equipping a functional language, Idealized ML, with
eﬀectful speciﬁcations based on higher-order separation logic. Their veriﬁcation
was partially formalized in a predicative Hoare Type Theory/Ynot and employs
abstract module deﬁnitions that combine code and speciﬁcation. Their use of
separating implication can likely be transferred to our setting, but their im-
plementation does not separate the functionality of subjects and observers to
same extent and thus does not raise the same speciﬁcation challenges. Consider-
ate reasoning [65], object propositions [51], and multi-object languages such as
Rumer [9] are alternatives in the design space spanned by invariant techniques,
aliasing/separation and ownership; all validate variants of Composite pattern.
    Extrapolating from our exploration of the Composite pattern, it appears
feasible to generate VST speciﬁcations, loop invariants, and APD declarations
from Verifast [34]; synthesizing full proofs will be more challenging.
    Object encodings in the Linux kernel, GTK/GObject, or the SQLite database
engine deviate from the Smalltalk tradition and expose APIs that are not fully
dataless. We suspect these systems also diﬀer from standard language-level ob-
ject disciplines in their need for deeply layered ownership control or model-level
object aggregates. Like Schreiner’s encoding [63], these systems thus provide
interesting opportunities for future case studies.

Conclusion The ability of type theory to capture modularity and abstraction is
well-established. But while, e.g. Mitchell and Plotkin’s insight has been highly
inﬂuential in the world of functional programming, it has not yet made its way
into veriﬁcation tools for mainstream languages. Taking inspiration from their
work, we introduced Veriﬁed Software Units as a general component calculus
for VST, and developed an infrastructure for separating the declarations of ab-
stract predicates from concrete predicate deﬁnitions. We showed that residual
predicates support callbacks which violate operation atomicity, as is the case
in the subject-observer pattern. Finally, we introduced a two-level approach to
specifying object principles, yielding a simple logic for Smalltalk-style objects in
C. Together, these innovations substantially advance VST’s capability to verify
modular C developments that employ diverse programming styles.

Acknowledgments: This work was funded by the National Science Foundation
under the awards 1005849 (Veriﬁed High Performance Data Structure Implemen-
tations, Beringer) and 1521602 Expedition in Computing: The Science of Deep
Speciﬁcation, Appel). The author is grateful to the members of both projects for
their feedback and greatly appreciates the reviewers’ comments and suggestions.


References
 1. Ahmed, A., Appel, A.W., Richards, C.D., Swadi, K.N., Tan, G., Wang, D.C.:
    Semantic foundations for typed assembly languages. ACM Trans. Program. Lang.
                                                     Veriﬁed Software Units      143

    Syst. 32(3), 7:1–7:67 (2010), https://doi.org/10.1145/1709093.1709094
 2. Albert, E., Puebla, G., Hermenegildo, M.V.: Abstraction-carrying code. In: Baader
    and Voronkov [7], pp. 380–397, https://doi.org/10.1007/978-3-540-32275-7 25
 3. Appel, A.W.: Foundational proof-carrying code. In: LICS’01: 16th Annual IEEE
    Symposium on Logic in Computer Science, Proceedings. pp. 247–256. IEEE Com-
    puter Society (2001), https://doi.org/10.1109/LICS.2001.932501
 4. Appel, A.W., Dockins, R., Hobor, A., Beringer, L., Dodds, J., Stewart, G., Blazy,
    S., Leroy, X.: Program Logics for Certiﬁed Compilers. Cambridge (2014)
 5. Appel, A.W., Naumann, D.A.: Veriﬁed sequential malloc/free. In: Ding, C., Maas,
    M. (eds.) ISMM’20: 2020 ACM SIGPLAN International Symposium on Memory
    Management. pp. 48–59. ACM (2020), https://doi.org/10.1145/3381898.3397211
 6. Aspinall, D., Gilmore, S., Hofmann, M., Sannella, D., Stark, I.: Mobile resource
    guarantees for smart devices. In: Barthe, G., Burdy, L., Huisman, M., Lanet,
    J., Muntean, T. (eds.) CASSIS’04: International Workshop on Construction and
    Analysis of Safe, Secure, and Interoperable Smart Devices, Revised Selected
    Papers. LNCS, vol. 3362, pp. 1–26. Springer (2004), https://doi.org/10.1007/
    978-3-540-30569-9 1
 7. Baader, F., Voronkov, A. (eds.): LPAR’04: Logic for Programming, Artiﬁcial
    Intelligence, and Reasoning, 11th International Conference, Proceedings, LNCS,
    vol. 3452. Springer (2005), https://doi.org/10.1007/b106931
 8. Balzer, R.M.: Dataless programming. In: American Federation of Information Pro-
    cessing Societies: Proceedings of the AFIPS ’67 Fall Joint Computer Conference.
    AFIPS Conference Proceedings, vol. 31, pp. 535–544. AFIPS / ACM / Thom-
    son Book Company, Washington D.C. (1967), https://doi.org/10.1145/1465611.
    1465683
 9. Balzer, S.: Rumer: A programming language and modular veriﬁcation technique
    based on relationships. Ph.D. thesis, ETH Zürich (2011)
10. Banerjee, A., Naumann, D.A.: Local reasoning for global invariants, part II: dy-
    namic boundaries. J. ACM 60(3), 19:1–19:73 (2013), http://doi.acm.org/10.1145/
    2485981
11. Barnett, M., DeLine, R., Fähndrich, M., Leino, K.R.M., Schulte, W.: Veriﬁcation
    of object-oriented programs with invariants. Journal of Object Technology 3(6),
    27–56 (2004), https://doi.org/10.5381/jot.2004.3.6.a2
12. Barnett, M., Naumann, D.A.: Friends need a bit more: Maintaining invariants over
    shared state. In: Kozen, D., Shankland, C. (eds.) Mathematics of Program Con-
    struction, 7th International Conference, MPC 2004, Proceedings. LNCS, vol. 3125,
    pp. 54–84. Springer (2004), https://doi.org/10.1007/978-3-540-27764-4 5
13. Barthe, G., Crégut, P., Grégoire, B., Jensen, T.P., Pichardie, D.: The MOBIUS
    proof carrying code infrastructure. In: de Boer, F.S., Bonsangue, M.M., Graf,
    S., de Roever, W.P. (eds.) FMCO’07: Formal Methods for Components and Ob-
    jects, 6th International Symposium, Revised Lectures. LNCS, vol. 5382, pp. 1–24.
    Springer (2007), https://doi.org/10.1007/978-3-540-92188-2 1
14. Beringer, L.: Veriﬁed Software Units – Coq development (2021), https://www.cs.
    princeton.edu/∼eberinge/VSU Esop21.tar.gz
15. Beringer, L., Appel, A.W.: Abstraction and subsumption in modular veriﬁcation of
    C programs. In: ter Beek, M.H., McIver, A., Oliveira, J.N. (eds.) Formal Methods
    - The Next 30 Years - Third World Congress, FM 2019, Proceedings. LNCS, vol.
    11800, pp. 573–590. Springer (2019), https://doi.org/10.1007/978-3-030-30942-8
    34
144     L. Beringer

16. Beringer, L., Hofmann, M., Momigliano, A., Shkaravska, O.: Automatic certiﬁ-
    cation of heap consumption. In: Baader and Voronkov [7], pp. 347–362, https:
    //doi.org/10.1007/978-3-540-32275-7 23
17. Besson, F., Jensen, T.P., Pichardie, D.: Proof-carrying code from certiﬁed ab-
    stract interpretation and ﬁxpoint compression. Theor. Comput. Sci. 364(3), 273–
    291 (2006), https://doi.org/10.1016/j.tcs.2006.08.012
18. Bruce, K.B., Cardelli, L., Pierce, B.C.: Comparing object encodings. Inf. Comput.
    155(1-2), 108–133 (1999), https://doi.org/10.1006/inco.1999.2829
19. Chalin, P., Kiniry, J.R., Leavens, G.T., Poll, E.: Beyond assertions: Advanced
    speciﬁcation and veriﬁcation with JML and ESC/Java2. In: de Boer, F.S., Bon-
    sangue, M.M., Graf, S., de Roever, W.P. (eds.) Formal Methods for Components
    and Objects, 4th International Symposium, FMCO 2005, Revised Lectures. LNCS,
    vol. 4111, pp. 342–363. Springer (2005), https://doi.org/10.1007/11804192 16
20. Clarke, D., Drossopoulou, S., Noble, J., Wrigstad, T.: Aliasing, conﬁnement, and
    ownership in object-oriented programming. In: Cebulla, M. (ed.) Object-Oriented
    Technology. ECOOP 2007 Workshop Reader, Final Reports. LNCS, vol. 4906, pp.
    40–49. Springer (2007), https://doi.org/10.1007/978-3-540-78195-0 5
21. Drossopoulou, S., Damiani, F., Dezani-Ciancaglini, M., Giannini, P.: Fickle : Dy-
    namic object re-classiﬁcation. In: Knudsen, J.L. (ed.) ECOOP 2001 - Object-
    Oriented Programming, 15th European Conference, Proceedings. LNCS, vol. 2072,
    pp. 130–149. Springer (2001), https://doi.org/10.1007/3-540-45337-7 8
22. Drossopoulou, S., Francalanza, A., Müller, P., Summers, A.J.: A uniﬁed frame-
    work for veriﬁcation techniques for object invariants. In: Vitek, J. (ed.) ECOOP
    2008 - Object-Oriented Programming, 22nd European Conference, Proceed-
    ings. LNCS, vol. 5142, pp. 412–437. Springer (2008), https://doi.org/10.1007/
    978-3-540-70592-5 18
23. Gamma, E., Helm, R., Johnson, R., Vlissides, J.: Design Patterns: Elements of
    Reusable Object-Oriented Software. Addison-Wesley Longman Publishing Co.,
    Inc., USA (1995)
24. Gu, R., Koenig, J., Ramananandro, T., Shao, Z., Wu, X.N., Weng, S., Zhang,
    H., Guo, Y.: Deep speciﬁcations and certiﬁed abstraction layers. In: Rajamani,
    S.K., Walker, D. (eds.) Proceedings of the 42nd Annual ACM SIGPLAN-SIGACT
    Symposium on Principles of Programming Languages, POPL 2015. pp. 595–608.
    ACM (2015), https://doi.org/10.1145/2676726.2676975
25. Gu, R., Shao, Z., Chen, H., Kim, J., Koenig, J., Wu, X.N., Sjöberg, V., Costanzo,
    D.: Building certiﬁed concurrent OS kernels. Commun. ACM 62(10), 89–99 (2019),
    https://doi.org/10.1145/3356903
26. Gu, R., Shao, Z., Kim, J., Wu, X.N., Koenig, J., Sjöberg, V., Chen, H., Costanzo,
    D., Ramananandro, T.: Certiﬁed concurrent abstraction layers. In: Foster, J.S.,
    Grossman, D. (eds.) Proceedings of the 39th ACM SIGPLAN Conference on Pro-
    gramming Language Design and Implementation, PLDI 2018. pp. 646–661. ACM
    (2018), https://doi.org/10.1145/3192366.3192381
27. Hamid, N.A., Shao, Z., Trifonov, V., Monnier, S., Ni, Z.: A syntactic approach to
    foundational proof-carrying code. J. Autom. Reasoning 31(3-4), 191–229 (2003),
    https://doi.org/10.1023/B:JARS.0000021012.97318.e9
28. Hawblitzel, C., Howell, J., Kapritsos, M., Lorch, J.R., Parno, B., Roberts, M.L.,
    Setty, S.T.V., Zill, B.: Ironﬂeet: proving safety and liveness of practical distributed
    systems. Commun. ACM 60(7), 83–92 (2017), https://doi.org/10.1145/3068608
29. Hawblitzel, C., Howell, J., Lorch, J.R., Narayan, A., Parno, B., Zhang, D., Zill,
    B.: Ironclad apps: End-to-end security via automated full-system veriﬁcation. In:
                                                       Veriﬁed Software Units       145

    Flinn, J., Levy, H. (eds.) 11th USENIX Symposium on Operating Systems Design
    and Implementation, OSDI ’14. pp. 165–181. USENIX Association (2014), https:
    //www.usenix.org/conference/osdi14/technical-sessions/presentation/hawblitzel
30. Hofmann, M., Pierce, B.C.: Positive subtyping. Inf. Comput. 126(1), 11–33 (1996),
    https://doi.org/10.1006/inco.1996.0031
31. Honsell, F., Lenisa, M., Redamalla, R.: Coalgebraic semantics and observational
    equivalences of an imperative class-based OO-language. Electron. Notes Theor.
    Comput. Sci. 104, 163–180 (2004), https://doi.org/10.1016/j.entcs.2004.08.024
32. Huisman, M., Jacobs, B.: Inheritance in higher order logic: Modeling and reason-
    ing. In: Theorem Proving in Higher Order Logics. LNCS, vol. 1869, pp. 301–319.
    Springer (2000)
33. Jacobs, B.: Objects and classes, co-algebraically. In: Freitag, B., Jones, C.B.,
    Lengauer, C., Schek, H. (eds.) Object Orientation with Parallelism and Persis-
    tence. pp. 83–103. Kluwer Academic Publishers (1995)
34. Jacobs, B., Smans, J., Philippaerts, P., Vogels, F., Penninckx, W., Piessens, F.:
    Verifast: A powerful, sound, predictable, fast veriﬁer for C and java. In: Bobaru,
    M.G., Havelund, K., Holzmann, G.J., Joshi, R. (eds.) NASA Formal Methods -
    Third International Symposium, NFM 2011. Proceedings. LNCS, vol. 6617, pp.
    41–55. Springer (2011), https://doi.org/10.1007/978-3-642-20398-5 4
35. Jacobs, B., Smans, J., Piessens, F.: Verifying the composite pattern using separa-
    tion logic. In: Speciﬁcation and veriﬁcation of component-based systems – Work-
    shop at ACM SIGSOFT/FSE 16 (2008), available at https://people.cs.kuleuven.
    be/∼bart.jacobs/verifast
36. Jung, R., Krebbers, R., Jourdan, J.H., Bizjak, A., Birkedal, L., Dreyer, D.: Iris
    from the ground up: A modular foundation for higher-order concurrent separation
    logic. Journal of Functional Programming 28 (2018)
37. Kay, A.C.: The early history of Smalltalk. In: Lee, J.A.N., Sammet, J.E. (eds.)
    History of Programming Languages Conference (HOPL-II), Preprints. pp. 69–95.
    ACM (1993), https://doi.org/10.1145/154766.155364
38. Kleymann, T.: Hoare logic and auxiliary variables. Formal Asp. Comput. 11(5),
    541–566 (1999), https://doi.org/10.1007/s001650050057
39. Koh, N., Li, Y., Li, Y., Xia, L., Beringer, L., Honoré, W., Mansky, W., Pierce,
    B.C., Zdancewic, S.: From C to interaction trees: specifying, verifying, and testing
    a networked server. In: Mahboubi, A., Myreen, M.O. (eds.) Proceedings of the
    8th ACM SIGPLAN International Conference on Certiﬁed Programs and Proofs,
    (CPP’19). pp. 234–248. ACM (2019), https://doi.org/10.1145/3293880.3294106
40. Kravchuk-Kirilyuk, A.Y.: The B+ -tree Index as a Veriﬁed Software Unit. Master’s
    thesis, Department of Computer Science, Princeton University (2020)
41. Krishnaswami, N.R., Aldrich, J., Birkedal, L., Svendsen, K., Buisse, A.: Design
    patterns in separation logic. In: Kennedy, A., Ahmed, A. (eds.) Proceedings of
    TLDI’09: 2009 ACM SIGPLAN International Workshop on Types in Languages
    Design and Implementation. pp. 105–116. ACM (2009), https://doi.org/10.1145/
    1481861.1481874
42. Leavens, G.T., Naumann, D.A.: Behavioral subtyping, speciﬁcation inheritance,
    and modular reasoning. ACM Trans. on Programming Languages and Systems
    37(4), 13:1–13:88 (2015), https://doi.org/10.1145/2766446
43. Liskov, B.: Keynote address - data abstraction and hierarchy. SIGPLAN Not.
    23(5), 17–34 (Jan 1987), https://doi.org/10.1145/62139.62141
44. Liskov, B., Wing, J.M.: A behavioral notion of subtyping. ACM Trans. Program.
    Lang. Syst. 16(6), 1811–1841 (1994), https://doi.org/10.1145/197320.197383
146     L. Beringer

45. McKinna, J., Burstall, R.M.: Deliverables: A categorial approach to program de-
    velopment in type theory. In: Borzyszkowski, A.M., Sokolowski, S. (eds.) Math-
    ematical Foundations of Computer Science 1993, 18th International Symposium,
    MFCS’93. Lecture Notes in Computer Science, vol. 711, pp. 32–67. Springer (1993),
    https://doi.org/10.1007/3-540-57182-5 3
46. Mitchell, J.C., Plotkin, G.D.: Abstract types have existential type. ACM Trans.
    on Programming Languages and Systems 10(3), 470–502 (Jul 1988)
47. Müller, P., Poetzsch-Heﬀter, A., Leavens, G.T.: Modular invariants for layered
    object structures. Sci. Comput. Program. 62(3), 253–286 (2006), https://doi.org/
    10.1016/j.scico.2006.03.001
48. Naumann, D.A.: Deriving sharp rules of adaptation for Hoare logics. Tech.
    Rep. 9906, Department of Computer Science, Stevens Institute of Technology
    (1999)
49. Necula, G.C.: Proof-carrying code. In: Lee, P., Henglein, F., Jones, N.D. (eds.)
    Conference Record of POPL’97: The 24th ACM SIGPLAN-SIGACT Symposium
    on Principles of Programming Languages. pp. 106–119. ACM Press (1997), https:
    //doi.org/10.1145/263699.263712
50. Nipkow, T.: Hoare logics for recursive procedures and unbounded nondeterminism.
    In: Bradﬁeld, J.C. (ed.) Computer Science Logic, 16th International Workshop,
    CSL 2002, 11th Annual Conference of the EACSL, Proceedings. Lecture Notes in
    Computer Science, vol. 2471, pp. 103–119. Springer (2002), http://dx.doi.org/10.
    1007/3-540-45793-3 8
51. Nistor, L., Aldrich, J., Balzer, S., Mehnert, H.: Object propositions. In: Jones,
    C.B., Pihlajasaari, P., Sun, J. (eds.) FM 2014: Formal Methods - 19th International
    Symposium, Singapore, May 12-16, 2014. Proceedings. LNCS, vol. 8442, pp. 497–
    513. Springer (2014), https://doi.org/10.1007/978-3-319-06410-9 34
52. Nistor, L., Kurilova, D., Balzer, S., Chung, B., Potanin, A., Aldrich, J.: Wyvern:
    A simple, typed, and pure object-oriented language. In: Proceedings of the 5th
    Workshop on MechAnisms for SPEcialization, Generalization and InHerItance.
    pp. 9–16. MASPEGHI ’13, Association for Computing Machinery, New York, NY,
    USA (2013), https://doi.org/10.1145/2489828.2489830
53. O’Hearn, P.W.: Separation logic. Commun. ACM 62(2), 86–95 (2019), https://
    doi.org/10.1145/3211968
54. O’Hearn, P.W., Yang, H., Reynolds, J.C.: Separation and information hiding. ACM
    Trans. Program. Lang. Syst. 31(3), 11:1–11:50 (2009), https://doi.org/10.1145/
    1498926.1498929
55. Parkinson, M.: Class invariants: the end of the road? (2007), contained in [20].
    Also available at https://people.dsv.su.se/˜tobias/iwaco/p3-parkinson.pdf
56. Parkinson, M.J., Bierman, G.M.: Separation logic and abstraction. In: Palsberg, J.,
    Abadi, M. (eds.) Proceedings of the 32nd ACM SIGPLAN-SIGACT Symposium
    on Principles of Programming Languages, POPL 2005. pp. 247–258. ACM (2005),
    https://doi.org/10.1145/1040305.1040326
57. Parkinson, M.J., Bierman, G.M.: Separation logic, abstraction and inheritance. In:
    Necula, G.C., Wadler, P. (eds.) Proceedings of the 35th ACM SIGPLAN-SIGACT
    Symposium on Principles of Programming Languages, POPL 2008. pp. 75–86.
    ACM (2008), https://doi.org/10.1145/1328438.1328451
58. Pierce, B.C.: Types and Programming Languages. MIT Press, Cambridge, Mass.
    (2002)
59. Polikarpova, N., Tschannen, J., Furia, C.A., Meyer, B.: Flexible invariants through
    semantic collaboration. In: Jones, C.B., Pihlajasaari, P., Sun, J. (eds.) FM 2014:
                                                         Veriﬁed Software Units       147

    Formal Methods - 19th International Symposium. LNCS, vol. 8442, pp. 514–530.
    Springer (2014), https://doi.org/10.1007/978-3-319-06410-9 35
60. Reynolds, J.C.: GEDANKEN - a simple typeless language based on the principle
    of completeness and the reference concept. Commun. ACM 13(5), 308–319 (1970),
    https://doi.org/10.1145/362349.362364
61. Reynolds, J.C.: Separation logic: A logic for shared mutable data structures. In:
    17th IEEE Symposium on Logic in Computer Science (LICS 2002), Proceedings.
    pp. 55–74. IEEE Computer Society (2002), https://doi.org/10.1109/LICS.2002.
    1029817
62. Saini, D., Sunshine, J., Aldrich, J.: A theory of typestate-oriented programming. In:
    Proceedings of the 12th Workshop on Formal Techniques for Java-Like Programs,
    FTFJP 2010, Maribor, Slovenia, June 22, 2010. pp. 9:1–9:7. ACM (2010), https:
    //doi.org/10.1145/1924520.1924529
63. Schreiner, A.T.: Objektorientierte Programmierung mit ANSI-C. Hanser (1994),
    https://www.cs.rit.edu/∼ats
64. Sjöberg, V., Sang, Y., Weng, S.c., Shao, Z.: DeepSEA: A language for certiﬁed sys-
    tem software. Proc. ACM Program. Lang. 3(OOPSLA), 136:1–136:27 (Oct 2019),
    http://doi.acm.org/10.1145/3360562
65. Summers, A.J., Drossopoulou, S.: Considerate reasoning and the composite design
    pattern. In: Barthe, G., Hermenegildo, M.V. (eds.) Veriﬁcation, Model Checking,
    and Abstract Interpretation, 11th International Conference, VMCAI 2010, Pro-
    ceedings. LNCS, vol. 5944, pp. 328–344. Springer (2010), https://doi.org/10.1007/
    978-3-642-11319-2 24
66. Summers, A.J., Drossopoulou, S., Müller, P.: The need for ﬂexible object in-
    variants. In: International Workshop on Aliasing, Conﬁnement and Ownership
    in Object-Oriented Programming (IWACO’09). ACM (2009), https://doi.org/10.
    1145/1562154.1562160
67. Vasudevan, A., Chaki, S., Maniatis, P., Jia, L., Datta, A.: überspark: Enforcing ver-
    iﬁable object abstractions for automated compositional security analysis of a hyper-
    visor. In: Holz, T., Savage, S. (eds.) 25th USENIX Security Symposium, USENIX
    Security 16. pp. 87–104. USENIX Association (2016), https://www.usenix.org/
    conference/usenixsecurity16/technical-sessions/presentation/vasudevan
68. Xia, L., Zakowski, Y., He, P., Hur, C., Malecha, G., Pierce, B.C., Zdancewic, S.:
    Interaction trees: representing recursive and impure programs in Coq. Proc. ACM
    Program. Lang. 4(POPL), 51:1–51:32 (2020), https://doi.org/10.1145/3371119

Open Access This chapter is licensed under the terms of the Creative Commons
Attribution 4.0 International License (http://creativecommons.org/licenses/by/4.0/),
which permits use, sharing, adaptation, distribution and reproduction in any medium
or format, as long as you give appropriate credit to the original author(s) and the
source, provide a link to the Creative Commons license and indicate if changes were
made.
    The images or other third party material in this chapter are included in the chapter’s
Creative Commons license, unless indicated otherwise in a credit line to the material. If
material is not included in the chapter’s Creative Commons license and your intended
use is not permitted by statutory regulation or exceeds the permitted use, you will need
to obtain permission directly from the copyright holder.
