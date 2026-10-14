                                           Formal Methods in Computer-Aided Design 2025



            P OLY V ER: A Compositional Approach for
            Polyglot System Modeling and Verification
                        Pei-Wei Chen∗ , Shaokai Lin∗ , Adwait Godbole∗ , Ramneet Singh†                          ,
                             Elizabeth Polgreen‡ , Edward A. Lee∗ , Sanjit A. Seshia∗
                 ∗ University of California, Berkeley, USA, {pwchen, shaokai, adwait, eal, sseshia}@berkeley.edu
                             † Indian Institute of Technology, Delhi, India, ramneet2001@gmail.com
                                   ‡ University of Edinburgh, UK, elizabeth.polgreen@ed.ac.uk



    Abstract—Many software systems are polyglot; that is, they        that helps localize bugs specifically due to the interaction
comprise programs implemented in a combination of program-            between multiple languages in a single system. These tools and
ming languages. Program verifiers, however, tend to be cus-           techniques can help developers build safer systems, but they
tomized for individual languages. Verification by compiling to a
common encoding requires supporting full language syntax and          cannot provide the guarantees needed in safety-critical settings
semantics which is prohibitive for modern languages. We present       and other vital settings in which polyglot systems appear.
P OLY V ER, an alternative compositional approach to polyglot ver-       In this paper, we study the problem of formally verifying
ification that bootstraps off-the-shelf language-specific verifiers   polyglot systems. Just like developing polyglot systems in-
with abstraction and synthesis.                                       troduces new challenges in the development cycle, verifying
    P OLY V ER uses contracts written in an intermediate language
to abstract individual procedures in the system. Our verification     polyglot systems introduces new challenges in the verification
approach uses language-specific verifiers (e.g., for C or Rust) to    process. Over the past few decades, there has been substantial
validate these contracts and the UCLID5 model checker for com-        work on program verifiers that operate directly on individual
positionally verifying a temporal property on the overall system      programming languages. We refer to these tools as language-
using the contracts. The intermediate language sidesteps the need     specific verifiers. For example, CBMC [8] and Frama-C [9] can
for compiling implementation languages to a common encoding,
a key obstacle with polyglot verification. Finally, P OLY V ER        be used to verify C code, Kani [10] and Verus [11] for Rust,
automates the generation of contracts using synthesis oracles such    ESC/Java [12], Java PathFinder [13], and JBMC for Java [14],
as large-language-models (LLMs). Overall P OLY V ER performs          etc. However, very few approaches have been proposed for
contract synthesis and verification in a counterexample-guided        multi-language systems, so polyglot verification challenges
abstraction refinement and inductive synthesis (CEGIS-CEGAR)          remain largely unexplored.
loop to verify the system-level property. We use P OLY V ER to
verify programs in the Lingua Franca polyglot language. We are           The main existing approach for polyglot system verification
able to verify systems with C and Rust procedures, as well as C       translates all code to one common language and applies
language fragments that were unsupported in previous work.            existing reasoning engines to that common representation.
    Index Terms—Polyglot languages, formal verification, synthe-      However, this approach is challenging due to the complexity
sis, contracts, large language models.                                of handling diverse syntax and semantics across languages,
                                                                      and arguably, it loses the benefits of having highly optimized
                        I. I NTRODUCTION                              language-specific verifiers. For instance, prior work, such as
   Many modern software systems comprise code written in              Lin et al. [15], only handles very restricted C code within the
a combination of programming languages [1]. For exam-                 Lingua Franca language, highlighting the difficulties of such
ple, the Robot Operation System 2 (ROS2) [2], [3] allows              monolithic approaches. Encoding a multi-language system in a
users to specify processes that communicate with each other,          single verification model may also result in scalability issues,
called ROS nodes, where each node can be implemented                  as the generated verification problem can become prohibitively
in a different programming language. Other languages and              large. To our knowledge, no existing approach enables auto-
frameworks provide similar cross-language functionality for           mated verification of multi-language software systems through
various domains, like Lingua Franca [4] for real-time, dis-           cooperative use of language-specific verifiers.
tributed embedded systems, and Eclipse Cyclone DDS [5] and               We propose a compositional verification approach to address
gRPC [6] for distributed systems and networking. We refer to          this gap. Our approach has two key components: (a) interface
these multi-language software systems as polyglot systems.            contracts written in an intermediate contract language that
   Polyglot systems allow developers to pick and choose the           abstract individual components, and (b) a synthesizer that
best programming language for specific system components.             automatically generates and refines these contracts with the
Unfortunately, this flexibility comes at a cost, with studies         help of language-specific verifiers. The intermediate contract
indicating that the increased complexity of polyglot systems          language is much smaller than the languages of individual
can lead to an increase in bugs [1]. Recent work has addressed        components, allowing us to sidestep full language translation.
these issues through testing and other incomplete methods. For        Instead, we can use language-specific verifiers to check the
example, Yang et al. [7] develop a deep-learning-based method         contract validity by only translating the (much smaller) inter-



     https://doi.org/                                                                        This article is licensed under a Creative
                                                                                             Commons Attribution 4.0 International License
state vars (V): t, request, count: 32-bit unsigned int                             fn Waited (                                if x.type == "i32":
               wait, pass, response: bool                                            request: &mut Port, count: &mut u32) {     return CodeBlock(f"if (x + 1 < 2147483647bv32) then x + 1 else 2147483647bv32")
                                                                                     *count = count.saturating_add(1);        elif x.type == "u32":
   t := 0               true /                                                       ctx.set(request, count);                   return CodeBlock(f"if (x + 1 <_u 4294967295bv32) then x + 1 else 4294967295bv32")
 count := 0
              𝑞"         Init
                                    𝑞!     Pr
                                                 re
                                                      qu
                                                           es
                                                                                   }                                          elif ...:
                                                oc              t
                                                     es
                                                          sQ
                                                                     /                                                          ...
                                                               ue
                                                                    ry             void ProcessQuery (
                             wait /                                                  Port request, Port response) {
                          t := t + 2;                                         𝑞#     if (request->value < 3) {
                             Waited
                                                          on
                                                               se
                                                                     /
                                                                              se       lf_set(response, rand() % 2);
                                                                                                                              Fig. 2: UCLID5 translation of x.saturating_add(1) in
                                                     sp                  on          } else {
                                                re                  sp

            𝑞%
                       pass /
                                    𝑞$           oc
                                                    e     ss
                                                               Re
                                                                                       lf_set(response, true);                Rust. Notice that the translation depends on the type of x.
                    t := t + 10;            Pr                                       }
                       Passed                                                      }                                          In UCLID5 and SMT-LIB, bitvectors do not have implicit
                                                                                                                              type interpretation. Instead, they are only interpreted when
Fig. 1: An Extended State Machine (ESM) describing a sub-
                                                                                                                              specific operators are applied. For example, < (bvslt) and
way traffic control system implemented in Lingua Franca (LF).
                                                                                                                              <_u (bvult) stands for the signed and unsigned less than
a/b means that when a is present, b is run. The procedures in
                                                                                                                              comparators in UCLID (SMT-LIB), respectively.
blue and orange are Rust and C procedures respectively.
Implementations of two procedures are shown on the right.
ctx.set and lf_set are LF API calls assigning values to ports.                                                                that type) instead of wrapping around. Figure 2 shows the
                                                                                                                              corresponding UCLID5 expression of this function. Encodings
                                                                                                                              must faithfully capture all language-specific constructs which
mediate language fragment. Further, our large language model                                                                  can be large/complex for modern languages.
(LLM)-based synthesizer and language-specific verifiers elim-
                                                                                                                              Language-specific verification (LSV) tools such as CBMC
inate the burden of manually writing and refining contracts.
                                                                                                                              [8] for C, Kani [19] for Rust, and Cameleer [20] for OCaml
This enables scalable and automated verification of multi-
                                                                                                                              already perform this heavy lifting of faithfully capturing
language systems without requiring a full translation into a
                                                                                                                              language semantics. However, these tools might use different
single verification framework.
                                                                                                                              backends/proof techniques. For example, CBMC and Kani
   In summary, the novel contributions of this paper are:
                                                                                                                              perform symbolic bounded model checking, while Cameleer
• Polyglot verification problem. We formalize the polyglot                                                                    uses deductive verification. Verifying polyglot systems with
   verification problem and propose a compositional solution                                                                  LSVs requires connecting these verifiers, which is challenging
   integrating multiple language-specific verifiers.                                                                          due to these differences.
• Automated pre/post-condition contract synthesis. We
                                                                                                                              Compositional (contract-based) verification uses interface
   automate synthesis and refinement of pre/post-condition
                                                                                                                              specifications, also called contracts, to abstract individual sys-
   contracts using an intermediate language and combining
                                                                                                                              tem components. Contracts can be assume-guarantee pairs for
   counterexample-guided inductive synthesis (CEGIS) and
                                                                                                                              concurrent systems or pre/post-condition pairs for sequential
   abstraction refinement (CEGAR). Our approach uses syn-
                                                                                                                              software. Once the validity of a contract w.r.t. the system
   thesis oracles including syntax-guided synthesis (SyGuS)
                                                                                                                              component is checked using an LSV, it can be soundly used
   solvers and large language models (LLMs).
                                                                                                                              for system-level verification. Crucially, given the contract,
• Our tool. We implemented P OLY V ER on top of                                                                               system-level check becomes agnostic of techniques/backends
   UCLID5 [16], [17], supporting C and Rust via CBMC [8]                                                                      employed by the LSV. P OLY V ER uses this precise strategy
   and Kani [10]. Our implementation shows that an LLM-                                                                       of using contracts as the glue connecting language-specific
   based synthesis oracle outperforms pure symbolic synthesis                                                                 verifiers. In this sense, verification in P OLY V ER operates much
   approaches.                                                                                                                like assume-guarantee/requires-ensures reasoning [21], [22].
• Case study and evaluation. We developed a verifier for                                                                      Manually identifying valid, yet strong enough contracts, how-
   the Lingua Franca coordination language [4] and show that                                                                  ever, is challenging. E.g., ProcessQuery (Fig. 1) requires
   our approach is able to verify multi-language systems with                                                                 a non-trivial postcondition:
   reasonable synthesis time. We also introduce a new set of
   polyglot verification benchmarks and realistic applications                                                                ((request->value < 3) || response->value)
   that are only solved by our approach.                                                                                          && (request == \old(request))

                      II. M OTIVATION AND BACKGROUND                                                                          To address this, P OLY V ER performs automated contract
                                                                                                                              synthesis by using refinement-based neural (LLM-based) con-
   Consider a train management system modeled in Figure 1
                                                                                                                              tract search in combination with symbolic verification of the
as an Extended State Machine (ESM) [18], i.e., a guarded
                                                                                                                              contract. Thus, with contract synthesis, P OLY V ER bootstraps
transition system where transitions have procedures attached
                                                                                                                              existing LSVs to solve the multi-language verification prob-
to them. Our example has procedures in two languages – the
                                                                                                                              lem, at the same time avoiding the challenges of encoding the
Waited procedure in Rust and ProcessQuery in C.
                                                                                                                              entire system into a single language.
Encodings must match language semantics. Differences
in language semantics can make encoding polyglot systems                                                                                          III. P ROBLEM F ORMULATION
into a single formal model challenging. For example, the                                                                        Polyglot systems are compositions of components where
x.saturating_add(1) Rust function in Waited satu-                                                                             each component is a procedure in some language L (e.g., C,
rates addition overflows to the maximum integer value (for                                                                    Rust, Java). Such a setup is widely seen in distributed systems
where nodes execute code in a specific language and interact            is a set of procedures. Each transition ((q, q ′ ), (g, u)) ∈ T
via mechanisms like remote procedure calls (RPCs). We                   is s.t. u = {(d, d′ ) | d′ = fk ◦ · · · ◦ f1 (d)} for some
formalize such systems and define the verification problem.             fi ∈ F , where ◦ denotes procedure composition: f1 ◦ f2 (d) =
   We model polyglot systems as Extended State Machines                 JC1 KL1 (JC2 KL2 (d)).
(ESM) [23]. Informally, ESMs capture inter-procedural control
                                                                           An example of a polyglot model is shown in Figure 1,
flow as transitions between modes, where each transition
                                                                        where Q = {qi }i , I0 = (q0 , _) is the state after executing
has an associated update function representing a sequence of
                                                                        the procedures on the initial transition, T is depicted by the
procedure calls. ESMs operate on a set of typed variables V
                                                                        transitions, and F = {Init, ProcessQuery, · · · }.
shared across all procedures in the system. We refer to the
domain of (typed) variable v ∈ V as D(v) and denote the                 Remark on semantics: While procedures are deterministic in
Cartesian product of the domains of all variables as D(V ).             our formulation (terms have deterministic semantics), nonde-
D(V ) thus forms the set of assignments d to V . A predicate            terministic procedures can be introduced by changing term
is a function D(V ) → B.                                                interpretations from functions to relations. Further, side-effects
                                                                        are emulated by extending V with global variables.
Definition 1 (Extended State Machine). An Extended State                   Traces. Each execution of the model produces an infinite
Machine (ESM) is a tuple (Q, V, I0 , T ) where                          trace that is the sequence of assignments (d) to variables in V
  1) Q is a set of modes,                                               seen in the execution. A property ϕ is a set of traces, typically
  2) V is a set of typed variables,                                     in the form of a temporal logic formula. Let the set of all traces
  3) I0 ⊆ Q × D(V ) is a set of initial states,                         that can be produced by a model M be T (M). We write
  4) T ⊆ (Q×Q)×(G×U ) is a set of mode-mode transitions,                M |= ϕ if T (M) ⊆ ϕ. The polyglot verification problem aims
      each associated with a guard in G = D(V ) → B and                 to determine whether a polyglot model satisfies a property ϕ.
      an update relation in U = 2D(V )×D(V ) .
                                                                        Problem Statement 1 (Polyglot verification problem). Given
   Executions. The guard g is a predicate determining whether           a polyglot model M = (Q, V, I0 , T, F ) and a system property
a transition can occur, and the update relation u defines how           ϕ determine whether M |= ϕ. If M ̸|= ϕ, provide a
the transition affects V . At every step, the ESM in a state            counterexample trace generated by M that violates ϕ.
(q, d) takes a transition ((q, q ′ ), (g, u)) such that g(d) is true.
                                                                           Verification Challenge and Insight. Crucially, while the
The ESM then updates the state to (q ′ , d′ ) where (d, d′ ) ∈ u.
                                                                        procedure bodies (C) in M are known, capturing their inter-
While the update relation (u) in each ESM transition is kept
                                                                        pretations (JCKL ) is difficult. Naive monolithic verification of
abstract, polyglot systems specialize them to be invocations of
                                                                        M would require encoding full semantics of L (for all L) to a
procedures (possibly from different languages).
                                                                        common modeling language, e.g. SMT-LIB. This is extremely
Definition 2 (Language). A language L is a set of terms and             tedious and would require a parser/compiler infrastructure for
predicates constructed through syntactic rules over a set of            each language. Our solution is to use contracts written in
variables V . The language fixes the interpretation of each term        an intermediate language L∗ – in this way we only need to
t ∈ L and predicate p ∈ L denoted as JtKL : D(V ) → D(V )               support encodings for this (much smaller) language L∗ .
and JpKL : D(V ) → B respectively.
   We assume that the set V contains all the variables read             IV. P OLYGLOT V ERIFICATION THROUGH A C ONTRACT IL
or written by the procedures implemented in the various lan-
                                                                          We now introduce contract-based decomposition. The key
guages. Further, the interface variables shared across languages
                                                                        component is a pre-post condition contract that abstracts (over-
must have matching types, and hence we use the same D(V )
                                                                        approximates) the behavior of a procedure f .
for different languages. This interface type-consistency is en-
forced in practical polyglot frameworks such as Lingua Franca           Definition 5 (Contract). A (L-)contract for procedure (C, L)
[4] and ROS2 [2]. Unless otherwise noted, we implicitly use             is a pair (P, Q) where P, Q are predicates in L. (P, Q) is
the same variable set V for the rest of the paper.                      valid iff the Hoare-triple {P }C{Q} holds, i.e.,
   Next, we define procedures.
                                                                         ∀d, d′ ∈ D(V ).(JP KL (d) ∧ d′ = JCKL (d)) =⇒ JQKL (d′ )
Definition 3 (Procedure). A procedure f is a pair (C, L)                                                                       (1)
where C ∈ L represents the procedure body. We call such
a procedure an L-procedure. We refer to pre-state and post-                By convention, preconditions P can only refer to pre-state
state variables of a procedure as V and V ′ , respectively.             variables V , while postconditions Q can refer to both pre- and
                                                                        post-state variables V and V ′ . Equation (1) can be checked
  We assume that procedures are total and always terminate
                                                                        with a language-specific verifier for L. A valid contract can
Polyglot models, our model for polyglot systems, are ESMs
                                                                        serve as a sound system-facing abstraction of the procedure,
where update relations are procedure invocation sequences.
                                                                        as we now discuss.
Definition 4 (Polyglot Model). A polyglot model M is a                     Contract composition replaces procedures in a polyglot
tuple (Q, V, I0 , T, F ) where (Q, V, I0 , T ) is an ESM and F          system M with their contracts. Formally, for each transition
u = fk ◦ · · · ◦ f1 in M, we generate contracts (Pj , Qj ) for      synth Oracles                                                mc and verif Oracles
each Lj -procedure fj such that,                                                                                compUCLID5
                                                                                                                               if (x <_u y)
                                                                    SyGuS/SyMO                                               then a else b
                                                                                                                                              UCLID5
                                                                      Solvers       ITE(         Intermediate
         ∀d ∈ D(V ).JQj KLj (d) =⇒ JPj+1 KLj+1 (d)           (2)                     LT(x, y),    Language       compRust
                                                                                                                                  if x < y
                                                                                                                                               Kani
                                                                                                                              {a} else {b}
                                    ′
                                                                     LLM-based       a, b)           ℒ∗
Then, we define a new model M where u is replaced with               Synthesizer                                                x<y?
                                                                                                                  compC                       CBMC
                                                                                                                                 a:b
the contract-derived relation u′ = {(a, b) | JP1 (a)KL1 =⇒
JQk (b)KLk }. Since the replacement contract u′ overapproxi-        Fig. 3: An intermediate language L∗ act as glue between
mates u, we have the following theorem.                             languages. Synthesis oracles generate expressions in L∗ , which
                                                                    are translated to semantic equivalent expressions in specific
Theorem 1. If M′ |= ϕ, then M |= ϕ.                                 languages used by a model checker or verification oracles. x
   How does a contract IL help verification? A key challenge        and y are unsigned bitvectors, hence using <_u in UCLID5.
with contract-based polyglot verification is checking Equation
(2), which involves predicates in two different languages. We
are unable to use a language-specific verifier to check this. Our   common IL allows us to maintain a single interface with
solution is to write contracts in an intermediate language L∗       synthesis oracles. For instance, in the case of Syntax Guided
and bridge contracts using a semantics-preserving compilation.      Synthesis (SyGuS) [24] we require a single grammar, or in the
                                                                    case of neural search (e.g., using LLMs), we require a single
Definition 6 (Intermediate Language). An intermediate lan-          in-context example set. Like verification, this greatly reduces
guage (IL) L∗ is a language of pre/post-condition contracts,        the effort in developing synthesis oracles. Figure 3 illustrates
whose semantics is defined by the SMT-based semantics of the        how L∗ mediates contract synthesis and verification.
language L to which it is translated.
                                                                         V. A N A BSTRACTION S YNTHESIS A PPROACH FOR
  Concretely, we translate contract predicates from L∗ to each                  P OLYGLOT M ODEL V ERIFICATION
procedure language L, e.g., C, Rust, through a semantics-
preserving compilation compL :                                        We present an approach for contract synthesis (Problem 2)
                                                                    which we use as a subroutine to solve Problem 1. We provide
Assumption 1 (L∗ → L Compilation).                                  some background and then an overview in Section V-B.
              ∀C ∈ L∗ . JcompL (C)KL ≡ JCKL∗                        A. Background: CEGIS and CEGAR
   Assumption 1 allows us to compose and validate contracts            We synthesize contracts by combining Counterexample
in L∗ . When contracts are in L∗ , contract composition check       Guided Inductive Synthesis (CEGIS) [25] and Counterexample
(Equation (2)) simplifies to:                                       Guided Refinement Abstraction (CEGAR) [26].
                                                                       CEGIS uses an iterative interaction between a learner and
          ∀d ∈ D(V ).JQj KL∗ (d) =⇒ JPj+1 KL∗ (d)            (3)
                                                                    a teacher to synthesize a solution (in our case contracts)
Equation (3) can be checked by a model checker when L∗ is           satisfying a set of constraints (in our case, example traces).
translated into a modeling language like UCLID5. Validity           The learner generates a candidate solution satisfying the con-
checking (Equation (1)) of an L∗ -contract (P, Q) simply            straints, while the teacher checks whether the solution satisfies
reduces to that of an L-contract (compL (P ), compL (Q)).           the overall specification. Synthesis succeeds if the solution is
   Counterexample guided contract refinement. While The-            correct; else, the teacher provides a new counterexample.
orem 1 provides a soundness result, the converse does not hold.        CEGAR iteratively refines an abstraction (in our case
A counterexample trace found in M′ may be a spurious coun-          contracts) in the context of a property. At each step, the
terexample that cannot be produced by M. Contracts must             abstraction is checked for correctness. If verification fails, the
be strengthened to exclude this trace. However, developing          counterexample is analyzed to determine whether it is spurious
valid contracts that are strong enough to prove system-level        (due to the abstraction being too coarse). If the counterexample
properties is challenging, often involving iterative contract       is real, the system is buggy; else, the abstraction is refined.
refinement. To address this, we introduce the valid contract
synthesis problem, which aims to generate a contract that           B. Approach Overview
avoids a set of spurious traces provided as negative examples.         We illustrate our CEGIS/CEGAR-hybrid approach to the
                                                                    polyglot verification in Figure 4 and Algorithm 1. The ap-
Problem Statement 2 (Valid Contract Synthesis Problem).
                                                                    proach is parameterized by the set of synthesis oracles, ver-
Given an L-procedure f and positive, negative example sets
                                                                    ification oracles, and the intermediate contract language L∗ .
X, X ⊆ D(V ) × D(V ), synthesize a valid contract in L∗ that
                                                                    It operates by performing CEGIS (inner loop; line 5) using
includes the positive examples and excludes negative ones.
                                                                    synthesis and verification oracles to synthesize contracts for
   How does a contract IL help synthesis? Contract synthesis        each procedure, which solves Problem 2. CEGAR (outer loop)
illustrates the second benefit of the intermediate language         then uses these contracts to generate the induced abstract
L∗ . Language-specific contracts would require synthesizers         model M′ (line 6) specified entirely in L∗ by combining
tailored to the syntax and semantics of each language. A            the system model and the contracts. We then check these
     CEGAR loop                                                              C. Oracles
        CEGIS loop                                                              We assume access to synthesis and verification oracles, and
                  synth oracle                               procedure C     a model checker. Synthesis oracles accept positive, negative
                                       contract (P, Q)
                                                                             example sets X, X, and return an L∗ -contract (P, Q) that
                               invalid contract /
                                                         verif oracle        satisfies X and dissatisfies X:
                                  𝑋 ←𝑋⋃𝑥
       spurious trace 𝑋ത ← 𝑋ത ⋃ 𝑥ҧ                  all contracts valid ℳ’             synth(X, X, C ∈ L) → (P ∈ L∗ , Q ∈ L∗ )
             verif-based                fail(𝜏)
                                                                                A verification oracle call verif(P, Q, C) verifies L∗ -contract
                                                         mc oracle
         spuriousness check
         true counter example trace
                                                                pass         validity w.r.t. an L-procedure (producing a positive-example if
                                                                             invalid): The verifier is a part of our trusted computing base
           𝜏 ∈ 𝒯(ℳ) ∖ 𝜙                                  ℳ⊨𝜙                 (TCB) and is assumed to be sound and complete:
Fig. 4: Flow diagram of our approach. The process starts from                Assumption 2 (Verifier).
the synthesis oracle. Contracts are synthesized in the inner
                                                                                verif(P, Q, C) = pass ⇐⇒ {P } C {Q}
(dashed) CEGIS loop and refined in the outer CEGAR loop.
X and X denotes positive and negative example sets.                             verif(P, Q, C) = fail(x = (d, d′ )) ⇐⇒
                                                                                                 JP KL∗ (d) ∧ d′ = JCKL (d) ∧ ¬JQKL∗ (d′ )
                                                                                A model checker call mc(M′ [Pi , Qi ], ϕ) verifies the ab-
contracts against the system-level property (line 7) – if the
                                                                             stract model M′ (with contracts) w.r.t. property ϕ, and
property is proven, the system is verified (line 8); otherwise,
                                                                             produces a (negative-) counterexample trace τ if violated.
we check if the counterexample trace is spurious (line 13). If
                                                                             Examples Yf can be extracted from τ for each procedure f :
the trace is spurious, we exclude it by returning to the inner
CEGIS loop to refine contracts, else we report failure with the              Assumption 3 (Model Checker).
trace (line 20). Thus, P OLY V ER iteratively switches between
CEGIS and CEGAR to generate a counterexample or prove                            mc(M′ [Pi , Qi ], ϕ) = pass ⇐⇒ M′ |= ϕ
the property.                                                                    mc(M′ [Pi , Qi ], ϕ) = fail(τ ) ⇐⇒ τ ∈ T (M′ ) \ ϕ
                                                                                      with extract(τ ) = {Yf }f
Algorithm 1 PolyVer: CEGIS/CEGAR-hybrid approach
                                                                                We now detail contract synthesis and refinement in Sec-
Require: M = (Q, V, I0 , T, F ): a polyglot model, ϕ: a                      tions V-D and V-E respectively. Finally, we discuss correctness
    property                                                                 guarantees in Section V-F.
Ensure: res: verification result, τ : a counterexample trace
 1: for all fi ∈ F do                                                        D. Contract Synthesis via CEGIS Loop
 2:     Xi , X i ← ∅, ∅                                                         The (inner) CEGIS loop iterates to generate a valid contract
 3: end for                                                                  for procedure (C, L) ∈ F , described in Algorithm 2. In each
 4: while ⊤ do                                   ▷ CEGAR loop                iteration, given C ∈ L, and initially empty example sets X and
 5:     C ← {synthContract(fi , Xi , X i )}fi     ▷ CEGIS loop               X, synth(X, X, C) generates a contract (P, Q) in L∗ . Then,
 6:     M′ ← induce(M, C)                                                    verif checks contract validity with respect to the procedure C.
 7:     res ← mc(M′ , ϕ)                                                     If verif(P, Q, C) = pass the contract is valid; otherwise the
 8:     if res = pass then               ▷ Verification succeeds             positive example x is added to X and the loop continues until
 9:         return pass, -                                                   a valid contract is found. Under Assumption 2, this produces
10:     else if res = fail(τ ) then                                          valid contracts upon termination, thereby solving Problem 2.
11:         isSpurious ← ⊥
12:         for all fi ∈ F do                                                Example 1 (Contract synthesis). The below table illustrates
                    ′                                                        CEGIS-based contract synthesis for ProcessQuery. synth
13:              X i ← checkSpurious(τ, fi )
14:
                       ′
                 if X i ̸= ∅ then                                            synthesizes (P1 , Q1 ) which verif checks for validity returns
15:                   isSpurious ← ⊤                                         a positive example (d, d′ ). Note that the pre-state d satisfies
16:              end if                                                      P1 but the post-state d′ violates Q2 . synth then refines the
17:              Xi ← Xi ∪ Xi
                                 ′                                           contract based on (d, d′ ) and generates (P2 , Q2 ), which is
18:         end for                                                          again checked by verif. req and resp are short for request
19:         if ¬isSpurious then        ▷ Counterexample found                and response respectively.
20:              return fail, τ                                                  Oracle                            Output
21:         end if                                                               synth iter. 1     P1 : ⊤, Q1 : (resp == (req >= 3))
22:     end if                                                                   verif iter. 1   fail / (req, resp) : d = (1, ⊥), d′ = (1, ⊤)
                                                                                 synth iter. 2    P2 : ⊤, Q2 : (req < 3 || resp == ⊤)
23: end while                                                                    verif iter. 2                    pass / −
                                                                         Oracle                                      Output
Algorithm 2 synthContract(f, X, X)                                       mc in CEGAR               (· · · , d = (2, ⊤), d′ = (10, ⊤), · · · )
Require: f = (C, L): a procedure                                         verif in CEGAR       pass / (req, resp) : d = (2, ⊤), d′ = (2, ⊤)
                                                                         synth in CEGIS        P3 : ⊤, Q3 : (req < 3 || resp == ⊤)
Modify: X, X: a set of positive/negative examples                                                         && \old(req) == req
Ensure: (P, Q): a valid contract for f                                   verif in CEGIS                           pass / −
 1: while ⊤ do
 2:    (P, Q) ← synth(X, X, C)
 3:    res ← verif(P, Q, C)                                           F. Correctness Guarantee
 4:    if res = pass then                 ▷ Contract is valid            Our approach makes assumptions 1, 2, and 3. Given these
 5:        return (P, Q)                                              assumptions, we guarantee partial correctness, meaning that if
 6:    else if res = fail(x) then       ▷ Contract is invalid         P OLY V ER terminates with pass result, the system is verified,
 7:        X ← X ∪ {x}            ▷ Collect positive example          M |= ϕ (soundness), and if it terminates with a fail result,
 8:    end if                                                         the system is unsafe, M ̸|= ϕ (completeness).
 9: end while                                                            We intuit this result as follows. For soundness, notice that
                                                                      contracts used in the induced model must overapproximate
                                                                      procedure behaviors because of the verification oracle assump-
   Valid contracts are then used to construct M′ (§IV) which          tion (Assumption 2). This means that when mc reports pass,
is then checked by mc. This may either succeed or return a            there does not exist a trace that is producible by the procedures
counterexample trace, which is then checked for spuriousness.         that violates the property, since all producible behaviors have
                                                                      already been captured by the contracts. For completeness,
E. Spuriousness Check                                                 when mc reports fail with a trace, the trace must violate the
                                                                      property. This trace must also be producible by the procedures
   A counterexample trace generated by mc may be spuri-
                                                                      by the spuriousness check (§V-E).
ous, i.e., unreproducible by the procedures. We illustrate the
checking process in Algorithm 3. We first extract pre/post                             VI. P OLY V ER I MPLEMENTATION
variable assignments p = {(d, d′ )}i for each procedure call
                                                                        We implement the P OLY V ER automated approach in a tool1
in the trace (line 2). For each (d, d′ ) ∈ p, we check whether
                                                                      which builds on top of the UCLID5 verifier [16] and currently
{V = d} C {V ′ ̸= d′ } holds using verif. If it holds, the pair
                                                                      supports the C and Rust languages. The tool is modular and
cannot be produced by the procedure and is then added as
                                                                      can be extended to support other languages and verifiers. Users
a negative example to X (“spurious trace” edge in Figure 4;
                                                                      need to provide oracles that subscribe to certain interfaces,
line 5). This will be excluded during the next CEGIS loop
                                                                      which we now describe. We also illustrate oracles we have
refinement iteration. If all pre-post transitions are valid for all
                                                                      used for C and Rust. We use Boolean connectives, arithmetic
procedures, the trace is a true counterexample (“true cex trace”
                                                                      operations, and comparators for the intermediate language L∗ .
edge). Example 2 shows an example of a spuriousness check
performed on ProcessQuery against a pair of assignments.              A. Synthesis Oracle Interface
                                                                         Given a procedure C, a set of positive and negative exam-
Algorithm 3 checkSpurious(τ, f )                                      ples X, X, the synthesis oracle synth returns an L∗ -contract
Require: τ : a counterexample trace, f = (C, L): a procedure          that is consistent with the examples. Below we discuss two
Ensure: X: a set of negative examples for f                           candidate synthesis oracles and their interfaces.
 1: X ← ∅                                                                1) LLM-based Synthesizer: LLMs are a good fit for con-
 2: for all (d, d′ ) ∈ extract(τ ) do                                 tract synthesis because of their understanding and reasoning
 3:     res ← verif(V = d, V ′ ̸= d′ , C)                             abilities across multiple (common) programming languages.
 4:     if res = pass then                   ▷ τ is spurious          We developed an LLM-based synthesizer that uses chain-of-
 5:         X ← X ∪ {(d, d′ )} ▷ Collect negative example             thought prompting [27] with error and example feedback to
 6:     end if                                                        generate contracts, i.e., the LLM is asked to first summarize
 7: end for                                                           the behavior of C and then generate a contract in L∗ .
 8: return X                                                             Inspired by work by Mora et al. [28], we formulate a
                                                                      Python-based DSL that allows the LLM to construct L∗ -
                                                                      expressions in a familiar language. We note that this does
Example 2 (Spuriousness check). Continuing from Ex-                   not affect the expressivity of generated the contract expres-
ample 1, assume that a model checker (mc) checks the                  sions. However, it increases the LLM’s ability to generate
property using (P2 , Q2 ) and returns a trace containing d            syntactically correct expressions. If the expression is invalid,
and d′ . To check spuriousness, we check the Hoare-triple             we re-prompt the LLM with an error message indicating
{(req, resp) = d} ProcessQuery {(req′ , resp′ ) ̸= d′ }               incorrect syntax or inconsistent types. Provided with positive
using verif, who returns pass. The pair is thus impossible,           and negative examples, the LLM is asked to find a constraint
making the trace spurious. We then return to the CEGIS loop
and re-synthesize a contract, which is proven valid by verif.           1 Available at https://github.com/uclid-org/polyver.
    that distinguishes the two sets. Details of our prompt are                     concurrent, and distributed systems. LF programs contain con-
    provided in Appendix A.                                                        current components called reactors connected through ports
       2) SyGuS/SyMO-based Synthesizer: The second oracle                          and connections. A reactor contains reactive message handlers
    treats the problem as a Programming by Example (PBE)                           called reactions, which can be written in a target programming
    problem [29], asserting that the generated contract (P, Q)                     language, e.g., C, C++, Rust, Python, or TypeScript. A reaction
    must2 satisfy examples in X and dissatisfy those in X:                         is invoked when any of its triggers are present, and it may pro-
                                                                                   duce effects triggering downstream reactions. With multiple
             ∀(d, d′ ) ∈ X. JP KL∗ (d) =⇒ JQKL∗ (d′ )                              reaction languages, Lingua Franca verification exhibits all the
                ∧ ∀(d, d′ ) ∈ X. JP KL∗ (d) ∧ ¬JQKL∗ (d′ )                         polyglot system verification challenges discussed previously.
       We use Syntax-Guided Synthesis (SyGuS) [24] solvers to
    solve the PBE problems. A similar approach is to encode as                     A. Our Running Example as a Lingua Franca Program
    a SyGuS Modulo Oracles (SyMO) [30] problem, a variant of
    SyGuS that allows constraints to contain black-box functions.                     Figure 5 shows the full LF program for our running example
    We use SyMO solvers with language-specific verifiers as                        (Fig. 1), a subway U-turn management system (UMS). The
    black-box functions. As the solver itself forms a CEGIS loop,                  Train and UMS reactors, written in Rust and C respectively,
    we can directly solve Problem 2 in a single iteration.                         use special brackets {=...=} to enclose reaction bodies. The
                                                                                   system describes a train asking for permission to cross. The
    B. Verification Oracle Interface                                               train sends out requests to the UMS, which decides whether
      We use CBMC and Kani as verification oracles for C and                       to grant permission (ProcessQuery). If the train has previ-
    Rust, respectively. Given a procedure body C and a contract                    ously made more than three attempts, the UMS will certainly
    (P, Q), we generate CBMC and Kani queries by constructing                      grant permission; otherwise permission is granted randomly.
    {P }C{Q} using their respective APIs. Listing 1 shows an                       If granted, the train will pass, taking ten minutes; otherwise,
    example of a CBMC query. Specifically, at lines 20 and 22, we                  it waits two minutes before retrying (ProcessResponse).
    use CBMC APIs to assume and assert the PRECONDITION                            The property (ϕ) that the train passes in 12 minutes is false,
    and POSTCONDITION C macros around the function call                            since the train may take up to 16 minutes.
    at line 21. This query is then verified using CBMC. We
    apply a similar template for Rust procedures, verified with the                B. Methodology: Mapping LF Programs to Polyglot Models
    Kani model checker. CBMC and Kani can achieve unbounded
    correctness for programs with loops by using loop invariants                      LFVerifier [15] performs end-to-end LF verification by
    or loop unwinding assertions.                                                  mapping the program onto a State Space Diagram (SSD) and
1  // ... Definitions of structs and APIs ...
                                                                                   compiling it along with the reaction body (C code) into a
2  void ProcessQuery() {                                                           monolithic axiomatic model. P OLY V ER instead compiles the
 3     if (query->value < 3) {                                                     SSD into an operational polyglot model.
 4         lf_set(response, rand() % 2 == 1);
 5     } else { lf_set(response, true); }                                             An SSD is a graph where each node (state) s contains the
 6 }                                                                               current logical time, a set R of reactions to be executed, and
 7 int main() {
                                                                                   a set of pending events, and each edge represents logical time
 8     // calloc for inputs and the self struct.
 9     query = calloc(1, sizeof(UMS_query_t));                                     advancement. Figure 6 in the Appendix shows an example
10     response = calloc(1, sizeof(UMS_response_t));                               SSD generated from the LF program in Figure 5.
11     // Assume that there are no NULL pointers.
12     __CPROVER_assume(query && response);
                                                                                      LF timing semantics at each state s impose a directed-
13     // Initialize with nondeterministic values.                                 acyclic graph (DAG) over the set of reactions R, with edges
14     *query = nondet_UMS_query_t();                                              encoding execution precedence. A reaction may fire only
15     // CBMC checks pre/post-conditions.
16     __CPROVER_assume(PRECONDITION);
                                                                                   when all of its predecessors have run to completion, so
17     ProcessQuery();                                                             any topological sort of the DAG is a valid execution order.
18     assert(POSTCONDITION);                                                      Independent reactions whose predecessors have finished may
19 }
                                                                                   execute in either order, hence introducing nondeterministic
       Listing 1: CBMC query generated for ProcessQuery                            reaction interleaving. Once all reactions in R are completed,
                                                                                   the SSD state can advance to the next state.
          VII. C ASE S TUDY: LF P ROGRAM V ERIFICATION                                We encode time progression and nondeterministic reaction
                                                                                   interleaving in UCLID5 by encoding reaction DAGs and
      We demonstrate P OLY V ER’s effectiveness by developing a                    dynamically tracking their execution status. This yields a
    verifier for the Lingua Franca (LF) coordination language [4].                 nondeterministic polyglot model (Definition 4) where each
    LF is a polyglot coordination language designed for real-time,                 transition executes one reaction, as in the model in Fig-
       2 Note that unlike Assm. 2, this is not a part of the trusted base of the
                                                                                   ure 1. We integrate the P OLY V ER-based verifier into the LF
    P OLY V ER approach. In particular, the LLM-based synthesizer (Sec. VI-A1)     compiler, which generates C, Rust, and UCLID5 code and
    may not satisfy this.                                                          performs verification.
 1   // Rust reactor                                                          26   // C reactor
 2   reactor Train {                                                          27   reactor UMS {
 3     input response : bool                                                  28     input request : uint32_t
 4     output request : u32                                                   29     output response : bool
 5     state count : u32 = 0                                                  30
 6     state passed : bool = false                                            31       reaction ProcessQuery (request) -> response {=
 7     logical action wait(2 minute)                                          32         if (request->value < 3) {
 8     logical action pass(10 minute)                                         33           lf_set(response, rand() % 2);
 9                                                                            34         } else { lf_set(response, true); }
10       reaction Init (startup) -> request {=                                35       =}
11          ctx.set(request, self.count);                                     36   }
12       =}                                                                   37
13       reaction Waited (wait) -> request {=                                 38   // Property to be verified
14          self.count = self.count.saturating_add(1);                        39   @property(
15          ctx.set(request, self.count);                                     40     name="pass_within_12_seconds",
16       =}                                                                   41     spec="F[0, 12 minute](t.passed)",
17       reaction Passed (pass) {= self.passed = true; =}                     42   )
18       reaction ProcessResponse (response) -> pass, wait {=                 43   main reactor {
19          if ctx.get(response).unwrap() {                                   44     // Component instantiations
20            ctx.schedule(pass, 0);                                          45     u = new UMS()
21          } else {                                                          46     t = new Train()
22            ctx.schedule(wait, 0);                                          47     // Component interactions
23          }                                                                 48     t.request -> u.request
24       =}                                                                   49     u.response -> t.response
25   }                                                                        50   }


                                          Fig. 5: LF program for a subway control system from [31].


                  VIII. E XPERIMENTAL E VALUATION                                  TABLE I: The synthesis oracle time (SOT) is the total contract
                                                                                   synthesis time for all procedures (proc) across all CEGIS
        Our experimentation evaluates P OLY V ER on both its com-                  iterations (IS). The verification oracle time (VOT) is the total
     ponents: contract synthesis and verification using synthesized                time on verification oracles, including contract validation and
     contracts. We want to answer the following research questions:                spuriousness checks. The verification time (UT) is the total
     RQ1. How does P OLY V ER compare to prior LF verification                     time on UCLID5, called once per CEGAR iteration (AR).
     work? RQ2. Can P OLY V ER handle full-fledged LF examples?
     RQ3. Can P OLY V ER verify multi-language systems?                                                    LOC  #Iters          CPU Time (s)
        Experiment Setup. We run all experiments on a single core                      Benchmark    #proc C LF IS AR       SOT VOT UT [15]
                                                                                       ADASModel      7   16 73 7 1        220.9 3.2 21.5 24.1
     on a 3.7GHz Intel Core i9 machine with 62GB RAM. We                               AircraftDoor   3   10 38 3 1         82.1 1.2   2.0   6.1
     generate contracts using an LLM-based synthesizer (OpenAI                         Alarm          2   12 30 2 1         62.3 0.9   2.1   5.8
     o1-mini) with three parallel LLM queries per procedure, and                       CoopSchedule   2   2 37 2 1          54.5 0.8 13.4 15.5
                                                                                       Election       3   7 35 3 1         124.2 1.4 83.9 35.7
     use CBMC-6.3.1, Kani-0.56.0, and z3-4.8.7 for verification.                       Election2      2   6 31 3 2         142.8 1.5 11.7 11.4
     Parallel synthesis for multiple procedures is implemented in                      Elevator      13 53 206 13 1        413.1 33.4 664.8 106.1
     P OLY V ER but not used in the experiments. Since LF reactions                    Factorial      3   11 36 3 1        138.2 1.9 63.0 42.4
                                                                                       Fibonacci      5   14 39 5 1        167.3 2.4 390.9 264.3
     often include unmodified variables irrelevant to strong/tight                     PingPong       4   8 62 4 1         131.0 1.8   8.2 12.0
     contracts, our LLM prompt includes a single instruction em-                       Pipe           5   10 60 5 1        147.4 2.4 172.2 144.1
     phasizing the importance of identifying these variables.                          ProcessMsg     4   10 32 4 1        116.6 1.8   5.1 14.6
                                                                                       ProcessSync    1   2 18 1 1          35.2 0.4   1.7   5.0
                                                                                       Railroad      10 64 66 17 2         678.9 9.0 264.8 223.4
     A. RQ1: Comparison to prior LF verification work                                  Ring           4   7 45 4 1         105.6 1.8   6.8 16.7
        We contrast P OLY V ER with LFVerifier [15] using its pro-                     RoadsideUnit   8   26 81 8 1        259.0 3.8 25.3 44.0
                                                                                       SafeSend       4   12 53 4 1        124.3 1.8   2.3   6.9
     posed LF benchmarks.3 These are arguably toy examples due                         Subway        10 20 64 10 1         266.5 4.5 67.2 35.0
     to the limited C syntax [15] supports – only assignments,                         Thermostat     6   29 45 6 1        192.6 2.6   3.5 12.8
     conditionals (incomplete), and arithmetic and Boolean oper-                       TrafficLight   4   46 42 8 2        462.1 4.4 216.1    -
                                                                                       TrainDoor      3   7 50 3 1          74.5 1.2   2.1   5.8
     ations. They use a subset of safety MTL properties [32].                          UnsafeSend     4   12 53 4 1        122.1 1.8   2.9   6.8
     A direct comparison is not entirely fair since [15] uses a
     monolithic, axiomatic encoding specialized for LF programs,
     while P OLY V ER uses a compositional, operational encoding
                                                                                   the contracts and verifies all benchmarks automatically, while
     that is more general. Despite this, [15] is, to our knowledge,
                                                                                   [15] is unable to verify the TrafficLight example. In
     the only prior work that performs end-to-end automated LF
                                                                                   18 out of the 22 benchmarks, the contracts were synthesized
     program verification, so we compare with it.
                                                                                   correctly in a single CEGIS loop, taking 37 seconds on
        We report on benchmark details, synthesis iteration counts,
                                                                                   average. For the rest, we observe that all but one reaction
     and runtimes in Table I. P OLY V ER successfully synthesizes
                                                                                   still requires one CEGIS iteration while one (hard) reaction
       3 While these benchmarks may be present in the LLM training data, no        requires all the remainder of iterations. The hard reaction often
     contracts are available.                                                      includes complex control flow and data dependencies, which
makes it difficult even for human experts to reason about.           TABLE II: Results for full-fledged and multi-language exam-
   We record the synthesis oracle time (SOT), verification           ples. The Blink, HillClimb, and Satellite examples include real
oracle time (VOT), and verification runtime (UT). Though the         implementation C code. The rest and other 22 variants in Ta-
total runtime (SOT + VOT + UT), dominated by the contract            ble I are multi-language systems only solvable by P OLY V ER.
synthesis time, is generally slower than that of [15], we argue                          LOC        #Iters            CPU Time (s)
that this is time well spent as P OLY V ER offers a significant       Benchmark #proc C/Rust LF CEGIS CEGAR         SOT VOT UT
qualitative improvement over [15]: There is no longer a               Blink       1    123   35   1        1        31.0 0.45 1.26
                                                                      HillClimb 12      75   102 20        1        685.4 74.9 9.7
need to develop a translator from a target language to the            Satellite   6    424 166    9        2        729.0 32.2 7.0
modeling language (e.g., C to UCLID5). Since we leverage              Submit      7     43    66  7        1        276.7 4.8 9.4
robust language-specific verifiers (e.g., CBMC, Kani), we are         TrainPass   5     14    44  5        1         160 8.8 14.1
                                                                      Service     4     8      -  4        1        118.9 7.1 3.5
also able to support a much more comprehensive fragment               FFI         3     30     -  3        1        73.9 6.5 1.75
of C/Rust. For example, CBMC officially supports ANSI-C,
while [15] develops a custom C-to-UCLID5 translator for a
small C subset (which is what these benchmarks use). These           in Table II. The LLM-based synthesizer is able to reason about
benefits are highlighted in Section VIII-B and VIII-C.               Rust code and library functions in both C and Rust.
   We also experimented with SyGuS/SyMO solvers but found               Aside from LF, we can also model and verify ROS2 appli-
that these approaches required a large number of CEGAR               cations using services (the call-and-response model), shown
iterations and failed to terminate in most benchmarks. We            by the Service example. The publish-subscribe pattern can
attribute this to the solvers’ lack of access to procedure bodies,   be modeled as well. Another general class of polyglot system
relying solely on positive and negative examples for guidance.       involves inter-language function calls, e.g., Rust using C via
                                                                     FFI or Java via Java Native Interface (JNI). These systems
B. RQ2: Can P OLY V ER handle full-fledged LF examples?
                                                                     can be modeled by splitting programs into language-specific
   We now evaluate P OLY V ER on examples requiring a                segments with typed interfaces (FFI example in Table II).
broader fragment of C that [15] is unable to verify.
   We evaluate our approach on two embedded systems –                                    IX. R ELATED W ORK
a blinking LED controller and a hill-climbing robot – and               Most approaches to verifying multi-language systems rely
a satellite altitude controller [33], [34]. The LED controller       on manually translating some parts of the system until every-
tracks blinking status, while the robot checks if it is in           thing is in a common language. For instance, Cook et al. [35]
climbing mode when on a ramp. Both are resource-constrained          translate fragments of assembly code into C to verify the Xen
embedded systems. The satellite example uses a PID controller        hypervisor, and Marin et al. [36] define a small imperative
and disables motors if user input exceeds safe limits. When          language within the Maude modeling language to manually
library functions (e.g., atan) are unavailable, we overapprox-       encode LF reactions. Where it is common to combine a
imate them using nondeterministic input/output values.               fragment of one language with another, tools may automate
   The results in Table II show that our approach is able to         translation of that fragment. For example, prior work [15] on
handle language complexities and generate contracts for actual       LF verification automatically translates a fragment of C into
implementation code. In the LED and hill climbing examples,          the verification language, and tools like CBMC [8] support
the LLM-based synthesizer was able to summarize procedure            small fragments of assembly code. Another method is to
behavior while ignoring details about low-level code when            black-box unanalyzable code and infer summaries from their
they are irrelevant. In the satellite example, the LLM struggled     observed input-output behavior [37]. While similar to us, this
to synthesize a valid contract for the PID controller. However,      relies on sufficient examples and lacks the guarantees that fully
we noticed that providing a simple comment in the code that          integrating language-specific verifiers provides.
captures the logic of the controller greatly helped synthesis.          We employ compositional verification based on Hoare
The synthesized contracts can all be checked by CBMC. This           logic [38]. This is commonly applied to verification problems
highlights P OLY V ER’s potential to verify real-world systems.      that, whilst written in only one language, are too large to be
                                                                     tackled in a single verification query [39]. Previous work, e.g.,
C. RQ3: Can P OLY V ER verify multi-language systems?                [40]–[43], automates this by learning pre/post-conditions using
   We show that P OLY V ER is able to verify multi-language          abstract interpretation and CEGAR [26].
LF programs, ROS2 applications, and programs with inter-                There are also property-guided approaches to inferring
language function calls via a foreign function interface (FFI).      contracts, while we aim to discover a contract that is just good
Note that these benchmarks cannot be solved by [15] as they          enough to prove a given property. Here, previous work uses
involve multiple languages. Some results are shown in Table II.      syntactic patterns [44], Constrained Horn Clause solvers [45],
   The final set of LF benchmarks consists of the 22 examples        and even CEGIS [25], [46]. Recently, LLMs have been applied
in Section VIII-A with half of the C reactions replaced by           to learning specifications, including pre/post-conditions, for
Rust reactions, plus Submit and TrainPass (the running               code [47]. The work closest to ours uses CEGIS and LLMs to
example in Figure 5). As the performance is similar for the 22       infer post-conditions, but neither of these approaches addresses
examples, we only report results for the two new benchmarks          the challenge of multi-language verification.
   Our approach to compositional verification, relying on                         [6] K. Indrasiri and D. Kuruppu, gRPC: up and running: building cloud
learning-based synthesis oracles, implements the paradigm of                          native applications with Go and Java for Docker and Kubernetes.
                                                                                      O’Reilly Media, 2020.
“verification by reduction to synthesis” and the use of learning-                 [7] H. Yang, Y. Nong, T. Zhang, X. Luo, and H. Cai, “Learning to detect
driven synthesis advocated by [48]. Our contract learning                             and localize multilingual bugs,” Proceedings of the ACM on Software
approach is based on an integration of CEGIS and CEGAR.                               Engineering, vol. 1, no. FSE, pp. 2190–2213, 2024.
                                                                                  [8] D. Kroening, P. Schrammel, and M. Tautschnig, “CBMC: the C bounded
This integration can be considered a form of oracle-guided                            model checker,” CoRR, vol. abs/2302.02384, 2023.
synthesis/learning [30], [48], [49], where the verification or-                   [9] P. Cuoq, F. Kirchner, N. Kosmatov, V. Prevosto, J. Signoles, and
acle and model checker act as oracles guiding the synthesis                           B. Yakobowski, “Frama-c: A software analysis perspective,” in In-
                                                                                      ternational conference on software engineering and formal methods.
search. In hardware, prior work [50] uses synthesis to gener-                         Springer, 2012, pp. 233–247.
ate environment invariants for modular hardware verification.                    [10] A. VanHattum, D. Schwartz-Narbonne, N. Chong, and A. Sampson,
These invariants can be seen as pre-conditions in our context.                        “Verifying dynamic trait objects in rust,” in Proceedings of the
                                                                                      44th International Conference on Software Engineering: Software
                          X. C ONCLUSIONS                                             Engineering in Practice, ser. ICSE-SEIP ’22. New York, NY, USA:
                                                                                      Association for Computing Machinery, 2022, p. 321–330. [Online].
   We formulated the polyglot verification problem and pro-                           Available: https://doi.org/10.1145/3510457.3513031
posed P OLY V ER, a contract-based approach. This approach                       [11] A. Lattuada, T. Hance, C. Cho, M. Brun, I. Subasinghe, Y. Zhou,
bootstraps off-the-shelf language-specific verifiers to verify                        J. Howell, B. Parno, and C. Hawblitzel, “Verus: Verifying rust programs
                                                                                      using linear ghost types,” Proceedings of the ACM on Programming
polyglot systems, while side-stepping challenges involved in                          Languages, vol. 7, no. OOPSLA1, pp. 286–315, 2023.
compiling the entire system to a single homogenous encoding.                     [12] C. Flanagan, K. R. M. Leino, M. Lillibridge, G. Nelson, J. B. Saxe,
We implemented our approach in a tool that automatically                              and R. Stata, “Extended static checking for java,” in Proceedings of the
                                                                                      ACM SIGPLAN 2002 Conference on Programming language design and
iterates between CEGAR and CEGIS loops to synthesize                                  implementation (PLDI), 2002, pp. 234–245.
contracts using an LLM-based synthesizer. We demonstrate a                       [13] K. Havelund and T. Pressburger, “Model checking java programs using
significant qualitative improvement by verifying full-fledged,                        java pathfinder,” International Journal on Software Tools for Technology
                                                                                      Transfer, vol. 2, pp. 366–381, 2000.
multi-language systems that previous work could not handle.                      [14] L. Cordeiro, P. Kesseli, D. Kroening, P. Schrammel, and M. Trtik,
   There are several interesting directions for future work. One                      “Jbmc: A bounded model checking tool for verifying java bytecode,”
is to apply the P OLY V ER approach to verifying other kinds                          in International Conference on Computer Aided Verification. Springer,
                                                                                      2018, pp. 183–190.
of polyglot distributed software systems or robotics software                    [15] S. Lin, Y. A. Manerkar, M. Lohstroh, E. Polgreen, S.-J. Yu, C. Jerad,
systems. We believe our approach is also applicable in cases                          E. A. Lee, and S. A. Seshia, “Towards building verifiable cps using
where the software is not necessarily polyglot to begin with.                         lingua franca,” ACM Trans. Embed. Comput. Syst., vol. 22, no. 5s, Sep.
                                                                                      2023. [Online]. Available: https://doi.org/10.1145/3609134
For example, it would also be interesting to apply this ap-                      [16] E. Polgreen, K. Cheang, P. Gaddamadugu, A. Godbole, K. Laeufer,
proach to the problem of formally-verified translation of code                        S. Lin, Y. A. Manerkar, F. Mora, and S. A. Seshia, “UCLID5: multi-
from one language to another (e.g., from C to Rust), where the                        modal formal modeling, verification, and synthesis,” in 34th Interna-
                                                                                      tional Conference on Computer Aided Verification (CAV), ser. Lecture
translation is performed in stages, and the intermediate state                        Notes in Computer Science, vol. 13371. Springer, 2022, pp. 538–551.
of the translated code involves a mix of languages.                              [17] S. A. Seshia and P. Subramanyan, “Uclid5: Integrating modeling, verifi-
                                                                                      cation, synthesis, and learning,” in Proceedings of the 15th ACM/IEEE
                       ACKNOWLEDGEMENTS                                               International Conference on Formal Methods and Models for Codesign
                                                                                      (MEMOCODE), October 2018.
  This work was supported in part by the DARPA Provably                          [18] V. S. Alagar and K. Periyasamy, Extended Finite State Machine.
Correct Design of Adaptive Hybrid Neuro-Symbolic Cyber                                London: Springer London, 2011, pp. 105–128. [Online]. Available:
Physical Systems (ANSR) program award number FA8750-23-                               https://doi.org/10.1007/978-0-85729-277-3_7
                                                                                 [19] A. VanHattum, D. Schwartz-Narbonne, N. Chong, and A. Sampson,
C-0080; the National Science Foundation (NSF) award #CNS-                             “Verifying dynamic trait objects in rust,” in Proceedings of the
2233769 (Consistency vs. Availability in Cyber-Physical Sys-                          44th International Conference on Software Engineering: Software
tems); Nissan and Toyota under the iCyPhy Center, Intel,                              Engineering in Practice, ser. ICSE-SEIP ’22. New York, NY, USA:
                                                                                      Association for Computing Machinery, 2022, p. 321–330. [Online].
Berkeley Deep Drive, and the RDI Frontier Fellows Program.                            Available: https://doi.org/10.1145/3510457.3513031
                                                                                 [20] M. Pereira and A. Ravara, “Cameleer: A deductive verification tool for
                              R EFERENCES                                             ocaml,” in Computer Aided Verification: 33rd International Conference,
 [1] H. Yang, Y. Nong, S. Wang, and H. Cai, “Multi-language software                  CAV 2021, Virtual Event, July 20–23, 2021, Proceedings, Part II. Berlin,
     development: Issues, challenges, and solutions,” IEEE Transactions on            Heidelberg: Springer-Verlag, 2021, p. 677–689.
     Software Engineering, vol. 50, no. 3, pp. 512–533, 2024.                    [21] C. B. Jones, “Tentative steps toward a development method for inter-
 [2] M. Quigley, K. Conley, B. Gerkey, J. Faust, T. Foote, J. Leibs,                  fering programs,” ACM Transactions on Programming Languages and
     R. Wheeler, A. Y. Ng et al., “ROS: An open-source robot operating                Systems (TOPLAS), vol. 5, no. 4, pp. 596–619, 1983.
     system,” in ICRA workshop on open source software, vol. 3, no. 3.2,         [22] B. Liskov, J. Guttag et al., Abstraction and specification in program
     2009, p. 5.                                                                      development. MIT press Cambridge, 1986, vol. 180.
 [3] S. Macenski, T. Foote, B. Gerkey, C. Lalancette, and W. Woodall,            [23] E. A. Lee and S. A. Seshia, Introduction to Embedded Systems:
     “Robot operating system 2: Design, architecture, and uses in the wild,”          A Cyber-Physical Systems Approach. MIT Press, 2016. [Online].
     Science Robotics, vol. 7, no. 66, p. eabm6074, 2022. [Online]. Available:        Available: http://leeseshia.org
     https://www.science.org/doi/abs/10.1126/scirobotics.abm6074                 [24] R. Alur, R. Bodik, G. Juniwal, M. M. K. Martin, M. Raghothaman, S. A.
 [4] M. Lohstroh, C. Menard, S. Bateni, and E. A. Lee, “Toward a lingua               Seshia, R. Singh, A. Solar-Lezama, E. Torlak, and A. Udupa, “Syntax-
     franca for deterministic concurrent systems,” ACM Transactions on                guided synthesis,” in 2013 Formal Methods in Computer-Aided Design,
     Embedded Computing Systems, vol. 20, no. 4, May 2021. [Online].                  2013, pp. 1–8.
     Available: https://doi.org/10.1145/3448128                                  [25] A. Solar-Lezama, L. Tancau, R. Bodík, S. A. Seshia, and V. A. Saraswat,
 [5] Eclipse Cyclone DDS project. [Online]. Available: https://github.com/            “Combinatorial sketching for finite programs,” in ASPLOS. ACM, 2006,
     eclipse-cyclonedds/cyclonedds                                                    pp. 404–415.
[26] E. M. Clarke, O. Grumberg, S. Jha, Y. Lu, and H. Veith,                     [48] S. A. Seshia, “Combining induction, deduction, and structure for veri-
     “Counterexample-guided abstraction refinement,” in CAV, vol. 1855.               fication and synthesis,” Proceedings of the IEEE, vol. 103, no. 11, pp.
     Springer, 2000, pp. 154–169.                                                     2036–2051, 2015.
[27] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le,         [49] S. Jha and S. A. Seshia, “A theory of formal synthesis via inductive
     D. Zhou et al., “Chain-of-thought prompting elicits reasoning in large           learning,” Acta Informatica, vol. 54, no. 7, pp. 693–726, 2017.
     language models,” Advances in neural information processing systems,        [50] H. Zhang, W. Yang, G. Fedyukovich, A. Gupta, and S. Malik, “Syn-
     vol. 35, pp. 24 824–24 837, 2022.                                                thesizing environment invariants for modular hardware verification,” in
[28] F. Mora, J. Wong, H. Lepe, S. Bhatia, K. Elmaaroufi, G. Varghese,                VMCAI, vol. 11990. Springer, 2020, pp. 202–225.
     J. E. Gonzalez, E. Polgreen, and S. A. Seshia, “Synthetic programming
     elicitation for text-to-code in very low-resource programming and
     formal languages,” in The Thirty-eighth Annual Conference on Neural
     Information Processing Systems (NeurIPS), 2024. [Online]. Available:
     https://openreview.net/forum?id=kQPzFiwVIu
[29] S. Gulwani, “Programming by examples: Applications, algorithms, and
     ambiguity resolution,” in Automated Reasoning: 8th International Joint
     Conference, IJCAR 2016, Coimbra, Portugal, June 27–July 2, 2016,
     Proceedings 8. Springer, 2016, pp. 9–14.
[30] E. Polgreen, A. Reynolds, and S. A. Seshia, “Satisfiability and synthesis
     modulo oracles,” in VMCAI, vol. 13182. Springer, 2022, pp. 263–284.
[31] N. Halbwachs, F. Lagnier, and C. Ratel, “Programming and verifying
     real-time systems by means of the synchronous data-flow language
     lustre,” IEEE transactions on software engineering, vol. 18, no. 9, pp.
     785–793, 1992.
[32] J. Ouaknine and J. Worrell, “Safety metric temporal logic is fully
     decidable,” in Tools and Algorithms for the Construction and Analysis
     of Systems, H. Hermanns and J. Palsberg, Eds. Berlin, Heidelberg:
     Springer Berlin Heidelberg, 2006, pp. 411–425.
[33] J. Cardoso, C. Chanel, P. Chauvin, A. Hostallier, J. Lamaison,
     A. Mascarenas-Gonzales, E. Metral, and L. Alloza, “Lab on the real-
     time control of reaction wheel,” 2022, unpublished lab exercise for the
     course 1MAE803: Real-time Control of Aerospace Systems, M.Sc in
     Aerospace Engineering, ISAE-SUPAERO.
[34] S. Lin, E. Jellum, M. Theile, T. Tanneberger, B. Sun, C. Jerad,
     R. Xu, G. Feng, C. Menard, M. Lohstroh, J. Castrillon, S. Seshia,
     and E. Lee, “Pretvm: Predictable, efficient virtual machine for
     real-time concurrency,” 2024. [Online]. Available: https://arxiv.org/abs/
     2406.06253
[35] B. Cook, B. Döbel, D. Kroening, N. Manthey, M. Pohlack, E. Polgreen,
     M. Tautschnig, and P. Wieczorkiewicz, “Using model checking tools to
     triage the severity of security bugs in the xen hypervisor,” in FMCAD.
     IEEE, 2020, pp. 185–193.
[36] M. Marin, P. C. Ölveczky, M. Reja, M. Rukhaia, and K. Bae, Semantics
     and Formal Analysis of Lingua Franca CPS Specifications in Rewriting
     Logic. Cham: Springer Nature Switzerland, 2025, pp. 70–101.
     [Online]. Available: https://doi.org/10.1007/978-3-031-85134-6_4
[37] W. Penninckx, B. Jacobs, and F. Piessens, “Sound, modular and compo-
     sitional verification of the input/output behavior of programs,” in ESOP,
     vol. 9032. Springer, 2015, pp. 158–182.
[38] C. A. R. Hoare, “An axiomatic basis for computer programming,”
     Commun. ACM, vol. 12, no. 10, pp. 576–580, 1969.
[39] D. Beyer, M. Kettl, and T. Lemberger, “Decomposing software verifi-
     cation using distributed summary synthesis,” Proc. ACM Softw. Eng.,
     vol. 1, no. FSE, pp. 1307–1329, 2024.
[40] P. Cousot, R. Cousot, M. Fähndrich, and F. Logozzo, “Automatic
     inference of necessary preconditions,” in VMCAI, vol. 7737. Springer,
     2013, pp. 128–148.
[41] Y. Moy, “Sufficient preconditions for modular assertion checking,” in
     VMCAI, vol. 4905. Springer, 2008, pp. 188–202.
[42] M. Gordon and H. Collavizza, “Forward with hoare,” in Reflections on
     the Work of C. A. R. Hoare. Springer, 2010, pp. 101–121.
[43] M. N. Seghir and D. Kroening, “Counterexample-guided precondition
     inference,” in ESOP, vol. 7792. Springer, 2013, pp. 451–471.
[44] E. Denney and B. Fischer, “A generic annotation inference algorithm
     for the safety certification of automatically generated code,” in GPCE.
     ACM, 2006, pp. 121–130.
[45] A. Alshnakat, D. Gurov, C. Lidström, and P. Rümmer, “Constraint-
     based contract inference for deductive verification,” in 20 Years of KeY.
     Springer, 2020, vol. 12345, pp. 149–176.
[46] A. Albarghouthi, I. Dillig, and A. Gurfinkel, “Maximal specification
     synthesis,” in POPL. ACM, 2016, pp. 789–801.
[47] C. Wen, J. Cao, J. Su, Z. Xu, S. Qin, M. He, H. Li, S. Cheung, and
     C. Tian, “Enchanting program specification synthesis by large language
     models using static analysis and program verification,” in CAV (2), vol.
     14682. Springer, 2024, pp. 302–328.
                                A PPENDIX                                 32   the negative examples.
                                                                          33
                          A PPENDIX A                            Positive example 1: ...
                                                                          34

           L ARGE L ANGUAGE M ODEL (LLM) P ROMPTING              ...      35
                                                              36 Negative example 1: ...
       We use chain-of-thought prompting to produce pre/post- 37 ...
     condition contracts for procedures. The prompt is structured
                                                                                  After completing the reasoning step, the LLM is instructed
     into three stages: (1) task description and instruction, (2)
                                                                               to generate the contract in the provided Python DSL, adhering
     procedure behavior reasoning, and (3) contract generation.
                                                                               to the specified requirements. Any SUGGESTION extracted
        In the first stage, the task is introduced and the requirements
                                                                               from its earlier analysis is highlighted in the prompt to guide
     are specified. At this point, a Python-based DSL is also
                                                                               this generation. A Python template is then supplied for the
     provided so that the LLM can employ it in the later contract-
                                                                               model to complete, along with an example to serve as a
     generation stage.
                                                                               usage reference. The final pre/post-conditions are extracted by
 1 Your task is to create two Boolean expressions,                             parsing the Python code block returned in this stage.
 2 a precondition and a postcondition, for a function
 3 named ’<function_name>’. Instructions below:                            Based on your analysis, complete the two Python
                                                                           1

 4 1. Precondition should only depend on inputs.                           functions PRECONDITION and POSTCONDITION that
                                                                           2

 5 2. Postcondition can depend on inputs and outputs.                    3 returns pre/postconditions for the code.

 6 3. Express pre/post-conditions using the following                    4 Requirements:

 7    set of Python DSL.                                                 5 1. The function body should be a single return

 8                                                                       6     statement. Do not use intermediate variables.
 9 # Addition operation                                                  7 2. Link all fields of the output to the inputs

10 def Add(a, b): return a + b                                           8     if possible, even if they are not used.
11 ...                                                                   9 3. You may abstract the postcondition by ignoring
                                                                        10     details and focusing on the relationship
        Next, the LLM performs a code reasoning step. It             is 11     between the inputs and outputs.
                                                                        12 ...
     instructed to identify: (1) the assumptions the function might 13
     make prior to execution, and (2) the guarantees it provides 14 **NOTE**: <SUGGESTION> Focus on this when generating
     afterward. When refining an existing contract, the model is fur- 15 pre/postconditions.
                                                                       16
     ther asked to specify (3) additional constraints that distinguish 17 Complete the code below using the provided
     between a given set of positive and negative examples. In this 18 Python DSL and put it in a Python code block.
     refinement setting, we also prompt the LLM to explain why 19 ‘‘‘python
                                                                       20 def PRECONDITION(query):
     the previous contract was invalid and to propose corrective 21 return # TODO: Fill in using the provided DSL
     modifications. We observe that explicitly reasoning about such 22 def POSTCONDITION(query, response):
     additional constraints enables the model to refine contracts 23 return # TODO: Fill in using the provided DSL
                                                                       24 ‘‘‘
     more effectively in light of the provided examples.               25
                                                        26 Below is an example of using the DSL.
 1 Describe what the function
                                                        27 ‘‘‘python
 2 1. may assume before it is executed, and
                                                        28 def PRECONDITION(in):
 3 2. guarantees after it is executed. Also,
 4 3. think about additional constraints that would
                                                        29   return TrueExpr()
 5    satisfy (eliminate) positive (negative) examples. 30 def POSTCONDITION(in, out):
 6 Output a list of the above points and nothing else.
                                                        31   return And(
 7
                                                        32     Eq(Select(out, ’count’), Select(in, ’count’)),
 8 The function has the following inputs and outputs:
                                                        33     Eq(Select(out, ’is_present), TrueExpr()),
 9 Inputs: <inputs>; Outputs: <outputs>
                                                        34   )
                                                        35 ‘‘‘
10 Code below: <code>
11
12 Here is a cex of the following pre/postconditions:                                               A PPENDIX B
13 Precondition: <precondition>
14 Postcondition: <postcondition>                                              S TATE S PACE D IAGRAM FOR LF P ROGRAM V ERIFICATION
15 Counterexample: <cex>
16 Write an explanation of why the pre/postconditions
17 are violated in the form
18 ‘‘‘json
19 {
20   "explanation": <EXPLANATION>
21   "suggestion": <SUGGESTION>
22 }
23 ‘‘‘
24
25 Lastly, below are some input/output examples.
26 Make sure the conditions satisfy the positive
27 examples and dissatisfy the negative examples.
28 Compare the positive and negative examples and
29 deduce what makes the negative examples invalid
30 behaviors of the code.
31 List constraints that need to be added to avoid
                                                                                                                                                        S3
                                                                                                                 S2
                                                                     S1
                             S0                                                                                                                    (6 minute, 0)
                                                                                                            (4 minute, 0)
                                                                (2 minute, 0)
                            (0, 0)                                                                                                              Reactions invoked:
                                                                                                         Reactions invoked:
                                                             Reactions invoked:                                                                    t.reaction_4
                     Reactions invoked:                                                                     t.reaction_4
                                                                t.reaction_4                                                                       t.reaction_2
                        t.reaction_4          +2 minute                               +2 minute             t.reaction_2          +2 minute
                                                                t.reaction_2                                                                       u.reaction_1
                        t.reaction_1                                                                        u.reaction_1
                                                                u.reaction_1
                        u.reaction_1                                                                                                              Pending events:
                                                                                                           Pending events:
                                                               Pending events:                                                                 (t.wait, (8 minute, 0))
                       Pending events:                                                                  (t.wait, (6 minute, 0))
                                                            (t.wait, (4 minute, 0))                                                           (t.pass, (10 minute, 0))
                    (t.wait, (2 minute, 0))                                                            (t.pass, (12 minute, 0))
                                                           (t.pass, (10 minute, 0))                                                           (t.pass, (14 minute, 0))
                   (t.pass, (10 minute, 0))                                                            (t.pass, (10 minute, 0))
                                                           (t.pass, (12 minute, 0))                                                           (t.pass, (12 minute, 0))
                                                                                                       (t.pass, (14 minute, 0))
                                                                                                                                              (t.pass, (16 minute, 0))


                                                    (a) The initialization phase of SSD (including S4)
                                                                                                  S6
                                                                                            (12 minute, 0)
                                                                                         Reactions invoked:
                                                                                            t.reaction_4
                                                                                            t.reaction_3
                                                                                            t.reaction_2
                                                                                            u.reaction_1
                                                                                          Pending events:                                                  S7
                         S4
                                                                                      (t.pass, (14 minute, 0))
                                                                                                                                                (14 minute, 0)
                 (8 minute, 0)                                                        (t.wait, (14 minute, 0))
                                                                                      (t.pass, (20 minute, 0))                    +2 minute   Reactions invoked:
               Reactions invoked:
                                                                                      (t.pass, (18 minute, 0))                                   t.reaction_4
                  t.reaction_4
                                                                                      (t.pass, (16 minute, 0))                                   t.reaction_3
                  t.reaction_2
                                                                                      (t.pass, (22 minute, 0))                                   t.reaction_2
                  u.reaction_1
                                                                                       +2 minute                                                 u.reaction_1
                 Pending events:
                                                                                                  S5                                         Pending events:
             (t.pass, (10 minute, 0))
                                                                                                                                         (t.pass, (16 minute, 0))
             (t.wait, (10 minute, 0))                                                       (10 minute, 0)
                                                                                                                                         (t.wait, (16 minute, 0))
             (t.pass, (14 minute, 0)) +2 minute                                          Reactions invoked:                              (t.pass,
                                                                                                                       +2 minute -6 minute        (20 minute, 0))
             (t.pass, (16 minute, 0))                                                       t.reaction_4                                 (t.pass, (22 minute, 0))
             (t.pass, (12 minute, 0))                                                       t.reaction_3                                 (t.pass, (18 minute, 0))
             (t.pass, (18 minute, 0))                                                       t.reaction_2                                 (t.pass, (24 minute, 0))
                                                                                            u.reaction_1
                                                                                          Pending events:
                                                                                      (t.pass, (12 minute, 0))
                                                                                      (t.wait, (12 minute, 0))
                                                                                      (t.pass, (14 minute, 0))
                                                                                      (t.pass, (18 minute, 0))
                                                                                      (t.pass, (16 minute, 0))
                                                                                      (t.pass, (20 minute, 0))

                                                          (b) The periodic phase of SSD (excluding S4)
Fig. 6: The State Space Diagram (SSD) of the LF program in Figure 5. The SSD is a lasso, with an initialization phase in
Figure 6a and a periodic phase in Figure 6b.
