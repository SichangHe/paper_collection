                                         Sound State Encodings in Translational Separation Logic
                                         Verifiers (Extended Version)
                                         HONGYI LING, ETH Zurich, Switzerland
                                         THIBAULT DARDINIER, EPFL, Switzerland
                                         ELLEN ARLT, MPI-SWS, Germany
                                         PETER MÜLLER, ETH Zurich, Switzerland
                                         Automated program verifiers are often organized into a front-end, which encodes an input program into
arXiv:2603.20001v3 [cs.PL] 23 Sep 2026




                                         an intermediate verification language (IVL), and a back-end, which proves that the IVL program is correct.
                                         Soundness of such translational verifiers requires that the back-end verification is sound and that correctness
                                         of the IVL program implies correctness of the input program. Existing formalizations for translational verifiers
                                         based on separation logic target the former, but support the latter only under the strong assumption that
                                         there exists a separation logic for the input program with the same state model as the IVL. This assumption is
                                         unrealistic in practice, especially since the state model also defines the supported separation logic resources.
                                            We present the first formal framework for proving the soundness of translational separation logic verifiers
                                         with non-trivial state encodings. To be applicable to various front-ends and IVLs, our framework only assumes
                                         the existence of a homomorphic encoding relation between the front-end and IVL state models. At the core of
                                         our framework is a novel condition, backward satisfiability, which is crucial to guarantee the soundness of the
                                         front-end translation. We formalize our framework for front-end verifiers based on concurrent separation logic
                                         and separation logic IVLs, such as Raven, VeriFast, and Viper. We demonstrate its expressiveness by proving
                                         soundness for three common state encodings. Our framework and all proofs are formalized in Isabelle/HOL.
                                         CCS Concepts: • Theory of computation → Logic and verification; Automated reasoning; Separation
                                         logic; Axiomatic semantics; Program verification.
                                         Additional Key Words and Phrases: Translational Verifier, Front-End Translation, Intermediate Verification
                                         Language, Implicit Dynamic Frames, State Encoding, Backward Satisfiability

                                         1   Introduction
                                         Many modern program verification tools are translational verifiers, i.e., they split the verification into
                                         front-ends, which translate the input program with its specification into an intermediate verification
                                         language (IVL), and back-ends, which verify the resulting IVL program. This split enables the reuse
                                         of back-end verifiers across multiple front-ends, thus dramatically reducing the effort of developing
                                         verifiers. Examples of translational verifiers include Civl [25] and Dafny [28] based on the Boogie
                                         IVL [27], Gillian for C and Javascript [33] and Rust [2] based on GIL [17], Prusti [1], Nagini [14],
                                         and Gobra [58] based on Viper [34], as well as Frama-C [8] and Creusot [12] based on WhyML [15].
                                         To support heap-manipulating and concurrent programs, many existing translational verifiers and
                                         their IVLs (GIL, Raven [19], VeriFast1 [22], and Viper) are based on separation logic (SL) [42].
                                            Soundness of a translational verifier requires (1) soundness of the back-end verifier and (2) sound-
                                         ness of the front-end translation, that is, that the successful verification of the IVL program implies
                                         correctness of the input program. While several existing works target back-end soundness for
                                         various IVLs [32, 37, 38, 7, 20], the state of the art does not offer practical techniques to prove
                                         soundness of realistic front-ends based on SL.
                                         1 VeriFast does not have a human-readable IVL, but uses a uniform internal representation and back-end for multiple input

                                         languages (C, Java, Rust).

                                         Authors’ Contact Information: Hongyi Ling, ETH Zurich, Zurich, Switzerland, hongyi.ling@inf.ethz.ch; Thibault Dardinier,
                                         EPFL, Lausanne, Switzerland, thibault.dardinier@epfl.ch; Ellen Arlt, MPI-SWS, Kaiserslautern, Germany, earlt@mpi-sws.org;
                                         Peter Müller, ETH Zurich, Zurich, Switzerland, peter.mueller@inf.ethz.ch.
330:2                                                                  Hongyi Ling, Thibault Dardinier, Ellen Arlt, and Peter Müller


def main(v: Int):
   x := alloc(f)
// { true }              { 𝑥 .𝑓 ↦→ _ }
      y := v      ||      x.f := v
// { 𝑦 = 𝑣 }             { ∃𝑣 ′ . 𝑥 .𝑓 ↦→ 𝑣 ′ ∗ 𝑣 ′ = 𝑣 }
      assert y = x.f


(a) Python-like front-end program, with concurrency and lazy field creation. The comments before and
after the parallel composition represent the pre- and postconditions of the two threads, respectively. Here
𝑥 .𝑓 ↦→ _ represents the ownership of 𝑥 .𝑓 without any guarantee that the field f has been created yet, while
∃𝑣 ′ . 𝑥 .𝑓 ↦→ 𝑣 ′ represents the ownership of 𝑥 .𝑓 with the guarantee that it has been created.

method main(v: Int) {                                                   method leftThread(v, y: Int) {
   // x := alloc(f)                                                         inhale   true
   havoc x                                                                  y := v
   inhale 𝑥 .𝑓added ↦→ false                                                exhale   𝑦 =𝑣
                                                                        }
      // parallel composition
      exhale    true                                                    method rightThread(v: Int, x: Ref) {
      exhale     ∃𝑏. 𝑥 .𝑓added ↦→ 𝑏 ∗ (𝑏 ⇒ 𝑥 .𝑓IVL ↦→ _ )                   inhale    ∃𝑏. 𝑥 .𝑓added ↦→ 𝑏 ∗ (𝑏 ⇒ 𝑥 .𝑓IVL ↦→ _ )
      havoc y
      inhale 𝑦 = 𝑣                                                          // x.f := v
      inhale     ∃𝑣 ′ . 𝑥 .𝑓added ↦→ true ∗ 𝑥 .𝑓IVL ↦→ 𝑣 ′ ∗ 𝑣 ′ = 𝑣        if (¬x. 𝑓added )
                                                                                 inhale 𝑥 .𝑓IVL ↦→ _
                                                                            x. 𝑓added := true
      // assert y = x.f
                                                                            x. 𝑓IVL := v
      assert ∃𝑣 ′ . 𝑥 .𝑓IVL ↦→ 𝑣 ′ ∗ 𝑦 = 𝑣 ′
}
                                                                            exhale    ∃𝑣 ′ . 𝑥 .𝑓added ↦→ true ∗ 𝑥 .𝑓IVL ↦→ 𝑣 ′ ∗ 𝑣 ′ = 𝑣
                                                                        }


(b) Example translation of the front-end program into the Viper IVL, inspired by Nagini. The highlighted
assertions represent the translations of the corresponding pre- and postconditions from Fig. 1a.

                                            Fig. 1. An example front-end translation.


1.1     Challenge: Large Semantic Gap
The main challenge in establishing the soundness of a front-end translation into an SL-based
IVL is to bridge the large semantic gap between the semantics and proof rules of the front-end
programming language and the IVL. As an example, consider the program in Fig. 1a. This program
allocates a new object with field f, then concurrently assigns the value of the argument v to local
variable y and field x.f, before asserting that y and x.f are equal. Like in Python, the language
used here adds the field f lazily to the object when it is first written: Attempting to read a field that
has not yet been added results in a runtime error. To verify this program, a translation into the
IVL must check that all fields that are read were previously assigned, in addition to ensuring the
absence of memory errors and data races, and that the assertion at the end of method main holds.
   Concurrency. Our IVL translation, inspired by the Viper-based Python verifier Nagini [14],
is shown on Fig. 1b. Since the IVL does not support concurrency directly, we translate it using
concurrent separation logic (CSL) [36] rules: The two front-end threads with their own pre- and post-
conditions are translated into and verified as separate IVL methods leftThread and rightThread.
Sound State Encodings in Translational Separation Logic Verifiers (Extended Version)                                  330:3


                         Valid front-end    (2) Proof reconstruction   Translation correct w.r.t.
                            SL proof                                   IVL axiomatic semantics
                                                                                      (1) Equivalence of
                (3) Soundness of front-end SL
                                                                                    the two semantics [11]

 Front-end program correct                 Soundness of the front-end translation                Translation correct w.r.t.
 w.r.t. operational semantics                                                                   IVL operational semantics


Fig. 2. Decomposing the soundness proof via a front-end SL. The dashed arrow represents the goal and the
three solid arrows represent the decomposition. Existing work does the decomposition, but assumes that the
two SLs have the same state model, which is unrealistic in practice. Our work lifts this key restriction, and
enables full soundness proofs for front-ends with different state models to their IVLs.


In each of them, the translated precondition is added to the initially-empty IVL state via an inhale
(also called produce) operation, the translated thread body is executed, and the translated postcon-
dition is checked (and removed from the final state) via exhale (also called consume). In the main
method, the concurrent part is abstracted to an exhale-havoc-inhale sequence that first removes
the resources transferred to each thread via exhales, then reflects the side effects of the threads on
the local variable y by assigning a non-deterministic value (havoc), and finally adds the resources
given back by each thread via inhales.
    Lazy field creation. As our target IVL has static field declarations (but does not support lazy
field creation directly), our encoding needs to reflect for each field whether it has been added. To
this end, the encoding represents each field 𝑓 of the front-end program with two statically-declared
fields in the IVL: the field 𝑓IVL to store the value of the front-end field, and an additional boolean
field 𝑓added that indicates whether field 𝑓 has been added to the object. As shown in the example:
(1) Allocating the object 𝑥 (as in the translation of x := alloc(f)) produces the SL resource
𝑥 .𝑓added ↦→ false, which provides the permission to add the field later, but does not generate
any ownership to 𝑓IVL . (2) Assigning to 𝑥 .𝑓 (as in the translation of x.f := v in the right thread)
requires 𝑥 .𝑓added ↦→ false (if the field has not been added before) or 𝑥 .𝑓IVL ↦→ _ (if it has). In
the former case, the resource 𝑥 .𝑓IVL ↦→ _ is produced lazily. In either case, 𝑥 .𝑓IVL ↦→ 𝑣 is held
after the assignment, thereby enabling subsequent reads. (3) Reading 𝑥 .𝑓 (as in the translation of
assert y = x.f) requires 𝑥 .𝑓IVL ↦→ _, as usual.

   This example demonstrates that the gap between front-end programs and their IVL encoding
is substantial, affecting the state representation (here, an extra IVL field per front-end field), the
operational execution (e.g., concurrency in the front-end program vs. multiple sequential methods
on the IVL), and proof rules (e.g., CSL for the front-end vs. inhale and exhale primitives in the
IVL). A soundness proof for a front-end translation needs to bridge this gap to show that verification
of the IVL program implies the correctness of the front-end program.

1.2   State of the Art
As explained above, establishing the soundness of a front-end translation into an SL-based IVL, for
example for the translation depicted in Fig. 1, requires bridging the large semantic gap between
the semantics and proof rules of the front-end programming language and the IVL. Dardinier et al.
[11] show that this gap can be reduced to proving that the correctness of the IVL encoding (with
respect to an axiomatic semantics) implies the existence of a valid proof in a suitable program logic
for the front-end programming language, as depicted in Fig. 2. This decomposition leverages the
existence of sound separation logics for many advanced front-end features (e.g., different kinds of
330:4                                                         Hongyi Ling, Thibault Dardinier, Ellen Arlt, and Peter Müller


concurrency [36, 18, 13, 56, 24], initialization semantics [41], non-local control flow [26], etc.) to
prove the soundness of front-end translations. For example, Dardinier et al. show how to prove
the soundness of the concurrency translation from Fig. 1. However, their framework requires the
front-end SL and the IVL to use the same state model, which is unrealistic in practice.
   In practice, most front-ends use a state model that is vastly different from the fixed state model
of the IVL. One major discrepancy is how memory and data are represented. For example, C’s
memory regions or Java’s arrays might be encoded into an object-based memory model in an IVL,
which does not natively support a notion of consecutive addresses. Moreover, our example from
Fig. 1a encodes each Python field by a pair of fields to track which fields have been added to an
object.
   Important discrepancies also arise for the information tracked as part of the verification state,
such as the separation logic resources held in a state. For example, front-end states may include
designated resources to execute a method call [21] or perform an I/O operation [39, 45], which
need to be encoded into standard SL predicates in the IVL. Moreover, front-end and IVL may use
a different permission model. For example, Viper [34], VeriFast [22], and Raven2 [19] all build in
fractional permissions [6, 5] but have front-ends that use binary3 permissions (e.g., the encoding
of I/O tokens in VeriFast [39] or Viper [45, 40]), counting permissions [5] (e.g., in Gobra [58] and
the encoding of relaxed separation logic [56] in Viper [46, 34]), or duplicable permissions (e.g.,
duplicable invariants over immutable shared data [41]).
   Due to these discrepancies, none of these encodings can be proven sound by the existing
framework by Dardinier et al.

1.3     This Work
We develop the first formal framework for proving the soundness of front-end translations that
use different state models from their IVLs, thus lifting the key restriction of existing work and
enabling soundness proofs for practical front-end translations. To be compatible with a wide
range of front-end separation logics and IVLs, our framework simply assumes the existence of a
homomorphic encoding relation between front-end and IVL states. We identify a novel condition
on this encoding relation, which we call backward satisfiability, that is crucial to guarantee the
soundness of the front-end translation. To show the practicality of our approach, we develop a
formal framework to prove the soundness of front-end translations based on concurrent separation
logic (CSL) [36], and instantiate it with three different front-end translations inspired by existing
Viper front-ends, including the one in Fig. 1. We also show that backward satisfiability is essential
for soundness, by uncovering several subtle sources of unsoundness in state encodings that affect
existing verifiers, but have not been described before. More broadly, we show that violations of our
framework’s requirements underlie several previously-reported soundness bugs in verifiers such as
Prusti, Nagini, and VerCors [4].
   In addition to proving the soundness of existing front-ends, our framework also guides the
development of new sound front-end translations. Developing a front-end typically involves three
steps: choosing a suitable IVL, designing the state encoding relation between front-end and IVL
states, and defining the translations of front-end expressions, assertions, and statements. Our
framework’s requirements support each of these steps in two ways. First, they provide design
guidance even before any proof is attempted: because a sound design must satisfy them, they rule
out large families of unsound choices and narrow the design space. Second, they enable incremental

2 Raven employs user-definable resource algebras for its ghost resources, but still uses fractional permissions for its regular

program states.
3 That is, one either owns a full permission or no permission at all.
Sound State Encodings in Translational Separation Logic Verifiers (Extended Version)                330:5


verification: once a design decision is made, the corresponding requirement is a self-contained
proof obligation that can be discharged immediately, allowing to catch an unsound choice early
rather than after the whole translation is built.
   In summary, we make the following technical contributions:
      (1) We identify a set of sufficient conditions, including the novel backward satisfiability, that
          guarantee the soundness of state encodings (§2 and §3).
      (2) We identify several subtle sources of unsoundness in state encodings that affect existing
          verifiers, but have not been described before (§2).
      (3) We develop a formal framework for proving the soundness of front-end translations. It is
          parametric in the front-end state model, expressions, assertions, statements, and logic, as
          well as their translations into the IVL. It is applicable to the translations used in practical
          SL-verifiers for both sequential and concurrent programs (§3).
      (4) We demonstrate the expressiveness of our framework by instantiating it for three practical
          front-end translations inspired by existing verifiers (§4).
      (5) The framework including all proofs is formalized in Isabelle/HOL.
  Our framework, including all formalizations and proofs, is mechanized in Isabelle/HOL [35] and
the mechanization is publicly available [31].

2     Overview: Homomorphism, Spurious Splittability, and Backward Satisfiability
In this section, we present key properties that a front-end translation must satisfy to be sound.
We assume the existence of a state encoding relation between front-end and IVL states, which
is general enough to capture many practical front-end translations (§2.1). We explain why this
relation should be homomorphic, and show how violating this requirement can lead to unsoundness
(§2.2). We then describe the key problem of spurious splittability, where the IVL state resulting from
encoding a front-end state is split into two IVL states that have no front-end counterparts (§2.3). We
explain how spurious splittability may lead to unsoundness and introduce our solution, backward
satisfiability, to prevent this (§2.4). Finally, we show examples where spurious splittability, and the
absence of backward satisfiability, lead to unsoundness (§2.5).

2.1     State Encoding Relations
Discrepancies between front-end and IVL states can stem from many different sources: a different
heap structure (e.g., in Fig. 1), a different permission model (e.g., binary vs. fractional permissions),
or even a different representation of the same permission model (e.g., rational vs. real numbers for
fractional permissions). To abstract over these different aspects and make our approach generically
applicable to different front-ends and IVLs, our framework is parametric in the front-end and IVL
state models, and we simply assume the existence of a state encoding relation · ∼S · between them.
Intuitively, 𝜔 ∼S Ω holds when the IVL state Ω represents the front-end state 𝜔.

   Relations from encoding functions. The state encoding relation is often derived naturally
from a function J·KS that encodes a front-end separation logic state into the corresponding IVL state,
in which case 𝜔 ∼S Ω is defined as Ω = J𝜔KS . For example, J·KS could encode binary permissions
into fractional permissions by setting a permission of 1 for locations owned by the state, and 0 for
the others. In the example from Fig. 1, our function J·KS encodes states as follows: The ownership
of a non-existent field f of a created object x is encoded as the ownership of 𝑓added of x with its
value set to false; the ownership of a created field f with value 𝑣 is encoded as the ownership
of both 𝑓added and 𝑓IVL , where the former has value true and the latter stores the actual value 𝑣.
The situation is represented in black in Fig. 3: Our function J·KS encodes the front-end states into
330:6                                                      Hongyi Ling, Thibault Dardinier, Ellen Arlt, and Peter Müller


                         Front-end states                       𝜔𝐹


                                                  𝜔𝐴 ⊨ 𝐴                  𝜔



                                                                                 J·KS
                                                  ⪰
                                        Ω𝐹
                                                                J𝜔 𝐹 KS


                                                                          J𝜔KS
                                              J𝜔𝐴 KS
                                                       ⪯
                         IVL states                              Ω𝐴 ⊨ J𝐴KA


Fig. 3. An illustration of our setting (in black), the problem of spurious splittability (in red), and the backward
satisfiability solution (in blue). The black dashed arrows represent the state encoding function J·KS from
front-end states to IVL states, and the black dashed ellipse represents the image of J·KS . The red arrows
represent a possible spurious split of the IVL state J𝜔KS into Ω𝐴 (that satisfies the translated assertion
J𝐴KA ) and Ω𝐹 (the frame), that have no front-end counterparts. The blue arrows show how the backward
satisfiability of 𝐴 guarantees the existence of front-end states 𝜔𝐴 and 𝜔 𝐹 , such that 𝜔𝐴 satisfies 𝐴, J𝜔𝐴 KS is
smaller or equal to Ω𝐴 , and J𝜔 𝐹 KS is larger or equal to Ω𝐹 .


(typically) a subset of the IVL states. For example, the image of the encoding function from binary
permissions is the subset of IVL states with permissions 0 or 1.
   The need for a relation. State encoding functions are too restrictive to capture some front-end
encodings, for instance, translations that encode duplicable permissions into fractional permissions,
as no fixed positive fraction, however small, can be duplicated. However, duplicable permissions
can be interpreted in the IVL as any arbitrary positive fraction: A front-end state with a single
duplicable resource then corresponds to infinitely many IVL states, each with a different fraction.
Such encodings are easily captured by our binary relation · ∼S ·, as we will show in §4.

2.2     The Homomorphism Requirement
At the core of separation logic is the concept of separation: A state 𝜔 satisfies the assertion 𝑃 ∗ 𝑄 if
it can be split into two states 𝜔 𝑃 and 𝜔𝑄 such that 𝜔 𝑃 satisfies 𝑃, 𝜔𝑄 satisfies 𝑄, and 𝜔 = 𝜔 𝑃 ⊕ 𝜔𝑄 ,
where ⊕ is a partial commutative and associative binary operation. In particular, both front-end
and IVL states are equipped with their operator ⊕. For the translation to be meaningful, we require
the state encoding relation to be homomorphic with respect to ⊕.
   For simplicity, we describe here the homomorphism requirement for the case where · ∼S ·
is defined by an encoding function J·KS , but we adapt it later to the general case of a relation.
The encoding function J·KS is required to be homomorphic: For all front-end states 𝜔 1 and 𝜔 2 ,
J𝜔 1 ⊕ 𝜔 2 KS = J𝜔 1 KS ⊕ J𝜔 2 KS . This is necessary so that the separating conjunction (∗) in the IVL
program (e.g., when adding or removing resources via inhale or exhale) corresponds to the separating
conjunction in the front-end program (e.g., in its parallel rule).
  Unsoundness without homomorphism. To see why the homomorphism requirement is neces-
sary, consider encoding a front-end state model with counting permissions into an IVL state model
with fractional permissions. Counting permissions [5] is a permission model that allows one to
Sound State Encodings in Translational Separation Logic Verifiers (Extended Version)                     330:7


 method m(x: Ref, y: Ref, z: Ref)                           method m(x: Ref, y: Ref, z: Ref) {
                 𝜖          𝜖          𝜖
   requires x.f ↦→ _ * y.f ↦→ _ * z.f ↦→ _                                   1
                                                                             2
                                                                                       1
                                                                                       2
                                                                                                 1
                                                                                                 2
 {                                                              inhale x.f ↦→ _ * y.f ↦→ _ * z.f ↦→ _
      if (x = y ∧ x = z)                                        if (x = y ∧ x = z)
        assert false                                              assert false
 }                                                          }



Fig. 4. Encoding counting permissions 𝑘 · 𝜖 as fractions 1 − 21𝑘 is unsound. The front-end program on the left
permits the three inputs to be aliased, but the IVL program on the right does not.


subtract from a full permission an unbounded number of units. In this model, a state holds either
1 − 𝑘 · 𝜖 or 𝑘 · 𝜖 permission to a heap location (for any non-negative 𝑘), where a full permission
1 is required to write to a location, and any positive number of units 𝑘 · 𝜖 provides read access.
Counting permissions are, for instance, used in the Chalice verifier [29].
   A simple (but unsound) encoding of counting permissions into an IVL offering fractional per-
missions [6], such as VeriFast and Viper, is to encode 𝑘 · 𝜖 as the fraction 1 − 21𝑘 , and 1 − 𝑘 · 𝜖 as
the complementary fraction 21𝑘 . This encoding ensures that the sum of the fractions for 1 − 𝑘 · 𝜖
and 𝑘 · 𝜖 provides write permission and, for positive 𝑘, each fraction is positive and, thus, pro-
vides read permission. However, this encoding is not homomorphic: Let 𝜔 𝑘 be a front-end state
with 𝑘 · 𝜖 permission to some heap location x.f, and Ω𝑝 be an IVL state with a fractional per-
                                                                                      1
mission 𝑝 to the corresponding heap location. Then J𝜔 1 ⊕ 𝜔 1 KS = J𝜔 2 KS = Ω1− 22 = Ω 4 , whereas
                                                                                             3

                         1
J𝜔 1 KS ⊕ J𝜔 1 KS = Ω1− 21 ⊕ Ω1− 2 = Ω1 ≠ Ω 4 . In other words, the encoding of the sum of the front-end
                                 1           3


states 𝜔 1 ⊕ 𝜔 1 has strictly less permission than the sum of the individual encodings.
   This violation of the homomorphic requirement results in an unsound front-end translation, as
illustrated by the example in Fig. 4. The front-end program on the left might lead to an assertion
violation because the counting permissions required in the precondition do not prevent all three
inputs from being aliased, as there is no bound on the number of units for each location. In contrast,
the assertion inhaled by the IVL program (on the right) rules out the case that all three inputs are
aliased since it is not possible to own more than one full permission to each location. Therefore,
the IVL program verifies even though the input program should not.
   Note that this unsoundness is independent of the particular fraction chosen to represent one
unit, as long as this fraction is strictly positive; smaller fractions just need more aliases to exhibit
the unsoundness. Summers and Müller [46] use an alternative encoding, in which a unit is encoded
as a symbolic fraction, together with the axioms 𝑓 > 0 and ∀𝑘 ∈ N. 𝑘 · 𝑓 < 1. This representation
makes it harder for an SMT-based verifier to exploit the unsoundness, but it is still present as there
is no fraction 𝑓 that satisfies these axioms.

2.3     Spurious Splittability
As discussed in §1, front-end translations rely on SL operations to add resources to the verification
state (produce) and to remove them (consume). IVLs provide these operations (e.g., inhale and
exhale in Viper) to encode SL proof rules. For example, the front-end translation from Fig. 1 uses
these operations to model allocation and parallel composition, which are not supported by the IVL.
   In general, a front-end statement 𝐶 (e.g., x := alloc(f)) can be modeled in the IVL via the cor-
responding rule from the front-end separation logic: If the triple {𝑃 } 𝐶 {𝑄 } is valid in the front-end
separation logic, then a possible (and typical) translation for 𝐶 in the IVL is exhale P; inhale Q
(assuming that 𝐶 does not modify local variables for simplicity). Starting in the IVL state Ω,
exhale P will split Ω into Ω𝑃 ⊕ Ω𝐹 (where Ω𝑃 satisfies 𝑃) and remove Ω𝑃 . The resulting state Ω𝐹
330:8                                                   Hongyi Ling, Thibault Dardinier, Ellen Arlt, and Peter Müller


 method main() {                                         method main() {
   x := alloc(f)                                           havoc x
   fork reader(x)                                          inhale x.f ↦→ _
                                                                                  𝑝
   y := x.f                                                  exhale ∃𝑝 > 0. x.f ↦→ _
 }                                                           y := x.f
                                                         }
 method reader(x: Ref)
   requires x.f ↦→ _                                     method reader(x: Ref) {
                                                                                  𝑝
 {                                                           inhale ∃𝑝 > 0. x.f ↦→ _
   var v := x.f                                              var v := x.f
   ...                                                       ...
 }                                                       }



Fig. 5. Encoding binary permissions using fractional permissions is generally unsound. The IVL program on
the right allows reading x.f after the fork because of the use of fractional permissions, and thus is correct. In
contrast, the front-end program uses binary permissions, and thus should not be verified.




represents the frame, i.e., the resources that are unaffected by the execution of 𝐶. The inhale Q
statement will then add another state Ω𝑄 to the frame Ω𝐹 , resulting in the state Ω𝑄 ⊕ Ω𝐹 . The
state Ω𝑄 , which satisfies 𝑄, models how the statement 𝐶 modified Ω𝑃 . Intuitively, this encoding is
justified by the frame rule of the front-end separation logic, with Ω𝐹 used as frame.
   Unfortunately, this intuitive justification might not be valid, because the split Ω𝑃 ⊕ Ω𝐹 might
be spurious: As represented in Fig. 3 (in red), the IVL states Ω𝑃 and Ω𝐹 might not have front-end
counterparts, even if the initial IVL state Ω has a front-end counterpart (i.e., a front-end state 𝜔
such that Ω = J𝜔KS ). In such a case, the frame rule of the front-end separation logic cannot be
used soundly with the IVL state Ω𝐹 , as it has only been proven sound for front-end states. Such
spurious splits arise because the front-end states generally correspond to a subset of the IVL states;
in other words, there are generally infinitely many more IVL states than front-end states, and thus
infinitely many IVL states without front-end counterparts. We call IVL states that have a front-end
counterpart concrete states, and spurious those that do not.

  Unsoundness from spurious splits. As a simplified example (we show more examples below),
consider a front-end that uses binary permissions. The encoding into an IVL with fractional
permissions attempts to improve framing by determining with a simple pre-analysis whether a
method updates a heap location. If not, it encodes permission to that location as an arbitrary
positive fraction rather than full permission, such that callers can frame the value around calls.
In this setting, the front-end program on the left of Fig. 5 does not verify because there is no
permission to access x.f after the fork. However, the encoding on the right verifies because the
                            𝑝
assertion ∃𝑝 > 0. x.f ↦→ _ in the IVL program (on the right of Fig. 5) can be satisfied by any
positive fraction, enabling the read y := x.f in the main thread. This unsoundness is caused by
spurious splittability: an IVL state with full permission to x.f can be split into two states, each
with 1/2-permission (one being passed to the forked thread and the other retained to read x.f
subsequently). However, these states have no corresponding front-end states, such that the same
reasoning steps are not valid there. We show in §2.5 that similar problems arise even with an
assertion syntax suitably restricted for the front-end state model.
Sound State Encodings in Translational Separation Logic Verifiers (Extended Version)                           330:9


2.4   Backward Satisfiability
The unsoundness in the previous example comes from the fact that the encoded precondition
                 𝑝
∃𝑝 > 0. x.f ↦→ _ can be satisfied by a spurious IVL state, which results in a spurious frame. In
particular, no smaller concrete state satisfies the encoded precondition, such that any split that
enables verifying the whole IVL program is spurious.
   We prevent this source of unsoundness by requiring front-end assertions to satisfy a novel
soundness condition. Intuitively, a front-end assertion 𝐴 is backward satisfiable if for any4 IVL
state Ω𝐴 that satisfies its translation J𝐴KA , there exists a front-end state 𝜔𝐴 that satisfies 𝐴 and
whose encoding J𝜔𝐴 KS is smaller than Ω𝐴 . Intuitively, and as depicted in Fig. 3 in blue, backward
satisfiability guarantees the existence of an alternative, non-spurious split J𝜔KS = J𝜔𝐴 KS ⊕ J𝜔 𝐹 KS
for some front-end states 𝜔𝐴 (satisfying 𝐴) and 𝜔 𝐹 , such that J𝜔 𝐹 KS ⪰ Ω𝐹 . The latter ensures that
the IVL frame Ω𝐹 can be used soundly with the frame rule from the front-end SL.5
                                                                                                                 𝑝
   Importantly, backward satisfiability holds for many basic SL assertions, such as points-to x.f ↦→
𝑣 and pure assertions (i.e., without permissions). Backward satisfiability is preserved by many
important SL connectives. For example, if 𝐴 and 𝐵 are backward satisfiable, then so is 𝐴 ∗ 𝐵 (with
the straightforward definition J𝐴 ∗ 𝐵KA ≜ J𝐴KA ∗ J𝐵KA ). Unfortunately, backward satisfiability is
not preserved by all connectives, such as magic wands (separating implications), as we show next.

2.5   Unsoundness without Backward Satisfiability
In this subsection, we show two examples that violate backward satisfiability because of the magic
wand connective, and how the soundness of front-end translations can be compromised when the
backward satisfiability condition is violated. The framework presented in this paper allows one to
uncover such subtle sources of unsoundness and to prove that correct encodings are indeed sound.
  Encoding binary permissions into fractional permissions. The example in Fig. 6 encodes the
input program on the left into the identical IVL program on the right. The front-end program on
the left uses binary permissions, whereas the IVL encoding on the right uses fractional permissions.
The assertion 𝑊 is defined using a magic wand (separating implication) connective:
                                      𝑊 ≜ x.f ↦→ _ −∗ ( x.f ↦→ _ ∗ y.g ↦→ _)
 Intuitively, it expresses that one can give up the wand as well as ownership of x.f to obtain
ownership of both x.f and y.g (that is, apply modus ponens).
 method m(x: Ref, y: Ref)                                    method m(x: Ref, y: Ref) {
   requires x.f ↦→ _                                           inhale x.f ↦→ _
   ensures 𝑊 ∗ 𝑊 ∗ 𝑊                                           skip
 { skip }                                                      exhale 𝑊 ∗ 𝑊 ∗ 𝑊
                                                             }



Fig. 6. Encoding binary permissions using fractional permissions is generally unsound. The IVL program on
the right verifies because there are fractional permissions for the footprints of the three magic wands 𝑊 .
With the binary permissions used by the front-end program on the left, it is not possible to provide sufficient
permissions for all three wands.

   Magic wands themselves represent resources (the wand’s footprint) that, combined with the
left-hand side of the wand, entail the right-hand side. With binary permissions, 𝑊 ’s footprint
4 More precisely, backward satisfiability only considers IVL states Ω that are smaller than the encoding J𝜔K of some
                                                                     𝐴                                      S
front-end state 𝜔, i.e., such that J𝜔KS = Ω𝐴 ⊕ Ω𝑅 for some IVL state Ω𝑅 .
5 Throughout the paper, we assume an affine front-end SL.
330:10                                              Hongyi Ling, Thibault Dardinier, Ellen Arlt, and Peter Müller


contains either permission to x.f (so that combining it with the left-hand side yields false, thereby
trivially satisfying the right-hand side) or permission to y.g. No matter which footprint is chosen,
the postcondition represents more than full permission to a heap location and is thus unsatisfiable.
Hence, verification should fail. Nevertheless, verification of the IVL program succeeds. With
                                                                   1/3
fractional permissions, one can choose 𝑊 ’s footprint as x.f ↦→ _, such that the right-hand side is
entailed trivially. With this choice, the postcondition holds, and verification succeeds.
   This unsoundness stems from the violation of backward satisfiability by 𝑊 (despite the fact that
both sides of the magic wand are backward satisfiable): the IVL may satisfy the translation of 𝑊 in
a state Ω𝐴 with 13 permission to x.f. However, the only front-end state 𝜔𝐴 that satisfies 𝑊 has full
permission to x.f and, thus, its encoding is not smaller than or equal to Ω𝐴 .
   This example also demonstrates that a commonly-used state encoding is sound only if it is
combined with appropriate restrictions on the allowed assertions. For instance, disallowing binary
permissions inside magic wands would rule out our unsound example.
  Encoding rational permission amounts into real permission amounts. Our next example
shows that the common practice of encoding SLs with rational permission amounts into automatic
verifiers targeting real permission amounts is surprisingly unsound in the presence of the magic
wand connective. Consider the following two assertions:
                                                                            
                                                 1                         𝑣
               𝑃1 ≜ ∃𝑣. y.g ↦→ 𝑣 ∗ 0 < 𝑣 ∗ 𝑣 2 ≤    −∗ ∃𝑣. y.g ↦→ 𝑣 ∗ x.f ↦→ _
                                                 2
                                                                                      
                                                           1                         𝑣
               𝑃2 ≜ ∃𝑣. y.g ↦→ 𝑣 ∗ 0 < 𝑣 < 1 ∗ (1 − 𝑣) 2 ≥    −∗ ∃𝑣. y.g ↦→ 𝑣 ∗ x.f ↦→ _
                                                           2
  In both of them, the left-hand side of the magic wand constrains the value 𝑣, which is used as a
permission amount for x.f on the right-hand side. The predicate y.g ↦→ 𝑣 enforces the values 𝑣 on
both sides to be the same. 𝑃1 constrains 𝑣 to be in the half-open interval (0, √1 ], whereas 𝑃2 allows
                                                                                      2
values for 𝑣 in (0, 1 − √1 ]. In both wands, the left-hand side provides no permission for x.f, so in
                         2
                  𝑣
both cases, x.f ↦→ _ is part of the footprint of the wand.

 method m(x: Ref, y: Ref)                             method m(x: Ref, y: Ref) {
   requires x.f ↦→ _                                    inhale x.f ↦→ _
   ensures 𝑃 1 ∗ 𝑃 2                                    skip
 { skip }                                               exhale 𝑃 1 ∗ 𝑃 2
                                                      }



Fig. 7. Encoding rational permission amounts as real numbers is unsound. The front-end program on the left
and the IVL program on the right interpret the permission amounts in the postcondition differently, such
that the IVL program verifies successfully even though the front-end program should not.

  The front-end and IVL methods in Fig. 7 require full ownership to x.f and ensure the separating
conjunction 𝑃1 ∗ 𝑃 2 . The two methods look identical, but use rationals and reals as permission
                                                                                          𝑣
amounts, respectively. The footprints of both magic wands need to contain x.f ↦→ _ for every
value 𝑣 permitted by the left-hand side. The IVL program, which uses real numbers as permission
amounts, thus, uses √1 for 𝑃1 and 1 − √1 for 𝑃2 . In real arithmetic, these add up to a full permission,
                       2                2
which is provided by the precondition. Hence, verification of the IVL program succeeds. However,
the front-end logic, which uses rational permission amounts, cannot represent the amounts √1 and
                                                                                                          2
1 − √1 precisely and, thus, needs to conservatively over-approximate them. As a result, their sum
      2
exceeds the full permission provided in the precondition, which causes verification to fail.
Sound State Encodings in Translational Separation Logic Verifiers (Extended Version)                                      330:11


   The unsoundness in this example again stems from the violation of backward satisfiability, by
both 𝑃1 and 𝑃2 (despite the fact that all sides of the magic wands are backward satisfiable): the IVL
may satisfy 𝑃1 (resp. 𝑃2 ) in a state Ω𝐴 with √1 (resp. 1 − √1 ) permission to x.f, while the front-end
                                                2             2
must provide strictly more amount of permission for 𝜔𝐴 to satisfy 𝑃 1 (resp. 𝑃 2 ).
   This example shows that encoding rational permission amounts as reals is generally unsound.
Since it should in principle be possible to formalize fractional permissions with real numbers instead
of rational ones, we do not expect this unsoundness to compromise actual verification results.
However, the mismatch makes it impossible to prove a formal soundness result for front-ends using
this common state model encoding.
   These unsoundnesses stem from the mismatch between the front-end and IVL state models:
when the two coincide, the state encoding can be taken to be the identity, backward satisfiability
holds trivially, and all connectives (including magic wands and universal quantifications) can be
translated soundly. Conversely, for front-ends with a sufficiently expressive assertion language,
backward satisfiability is necessary: whenever an assertion’s translation violates it and the front-end
can express the corresponding upper bound and frame (as in all our examples), one can construct
an unsound method as above, in which the IVL translation verifies but the front-end program does
not.

3     A Framework for Proving Front-End Translations Sound
Our core contribution is a formal framework that allows one to prove that the state model encoding
of a front-end translation is sound. In this section, we formalize our framework: the semantic model
of the IVL (§3.1), its parameters (§3.2) and their soundness requirements (§3.3), our soundness
result (§3.4), and a generalization in which the state encoding is a relation rather than a function
(§3.5). All results are formalized in Isabelle/HOL. Although the formalization uses Viper as the IVL,
all requirements and results are independent of any specific IVL, so we present them for a general
SL-based IVL.

3.1    Preliminaries
We adopt much of our semantic model of the IVL from Dardinier et al. [11].
  IDF algebras. To make our framework widely applicable, our formalization captures both IVLs
based on standard SL (e.g., VeriFast) and IVLs based on implicit dynamic frames (IDF) [43, 44] (e.g.,
Viper). To achieve that, we formalize states as IDF algebras, a generalization of separation algebras
that also captures IDF state models:6
Definition 1 (IDF algebra). An IDF algebra is a tuple (Σ, ⊕, | · |, stable, stabilize, unit) that satisfies
a set of axioms (listed in Appendix A), where Σ is a set of states, ⊕ : Σ × Σ ⇀ Σ is a partial,
commutative, and associative addition on Σ, | · |, stabilize, and unit are endomorphisms of Σ, and
stable is a predicate on Σ.
   Intuitively, ⊕ denotes the composition of states, | · | projects a state on its largest duplicable part,
stable decides the self-containedness of a state (i.e., the state holds enough ownership to all its
fields so that none of them may be modified by the environment), stabilize projects a state on its
largest stable part, and unit denotes the unit element of ⊕.

6 Compared with the definition from Dardinier et al. [11], we make the unit function explicit and independent from stabilize

and | · |; the definition from Dardinier et al. [11] can be derived from ours by setting unit(𝑠 ) ≜ stabilize( |𝑠 | ). Our
generalization is crucial to capture front-end state models where stabilize( | · | ) does not satisfy the properties for unit(·),
e.g., the immutable heaps from §4.4, where stabilize( |ℎ | ) = ℎ but unit(ℎ) = 𝜆𝑙 . ⊥.
330:12                                                      Hongyi Ling, Thibault Dardinier, Ellen Arlt, and Peter Müller


    IDF assertions separate ownership information from value constraints. For instance, SL’s points-
to assertion x.f ↦→ v is expressed in IDF as acc(x.f) ∗ x.f = v. To ensure sound framing, IDF
requires assertions to be self-framing; that is, an assertion may constrain a heap location only
if it includes the permission to that location. Consequently, acc(x.f) ∗ x.f = v is self-framing,
but x.f = v alone is not. We defined self-framedness of assertions and other related concepts as
follows:
Definition 2. Let 𝑃 be an IDF assertion (i.e., a set of states from an IDF algebra).
    • 𝑃 is self-framing, written selfFraming(𝑃), iff ∀𝜔. 𝜔 ∈ 𝑃 ⇔ stabilize(𝜔) ∈ 𝑃.
    • A state 𝜔 frames 𝑃, written frames(𝜔, 𝑃), iff selfFraming({𝜔 } ∗ 𝑃).
    • An IDF assertion 𝐵 frames 𝑃, written frames(𝐵, 𝑃), iff ∀𝜔 ∈ 𝐵. stable(𝜔) ⇒ frames(𝜔, 𝑃).
    • 𝑃 frames an expression (i.e., a partial function from states to values) 𝑒, written frames(𝑃, 𝑒),
       iff 𝑒 (𝜔) is defined for all 𝜔 ∈ 𝑃.
    • An expression 𝑒 is stable under 𝑃, written stableUnder(𝑒, 𝑃), iff ∀𝜔 ∈ 𝑃, 𝑒 (𝜔) is defined iff
       𝑒 (stabilize(𝜔)) is defined, and 𝑒 (𝜔) = 𝑒 (stabilize(𝜔)) when they are both defined.
   IVL semantics. An IVL state consists of a store of local variables and a customized heap 𝜑 ∈ Σ
equipped with an IDF algebra structure, i.e., the set of IVL states Σ𝑉 = (Var ⇀ 𝑉 ) × Σ, where 𝑉 is
the set of values and the store Var ⇀ 𝑉 is instantiated to the agreement algebra, i.e., addition on
stores is defined only for identical stores and yields the argument store, | · |, stabilize, and unit are
instantiated to the identity function, and stable(𝑠) holds for any store 𝑠.
   We require that the IVL supports three primitive statements havoc 𝑥, inhale 𝐴, exhale 𝐴,
and sequential compositions 𝐶 1 ; 𝐶 2 and conditional statements if (𝑏) {𝐶 1 } else {𝐶 2 } in order to
translate some front-end control structures. Intuitively, havoc 𝑥 erases the value of local variable 𝑥
by overwriting it non-deterministically, inhale 𝐴 adds the resource specified by assertion 𝐴 into
the current state and assumes the value constraints in 𝐴, and exhale 𝐴 checks that 𝐴 holds in the
current state and subsequently removes the resource corresponding to 𝐴 from the current state.
   We assume an axiomatic semantics for the IVL. The axiomatic semantic judgements are of the
form Δ ⊢ [𝑃] 𝐶 [𝑄], where Δ is a type context7 , 𝑃 and 𝑄 are IVL semantic assertions (i.e., sets of IVL
states), and 𝐶 is an IVL statement. The axiomatic semantic rules of the aforementioned statements
are given in Appendix A.

3.2      Framework Parameters
To capture a wide range of front-ends, our framework offers numerous parameters that describe
the input language to the front-end as well as the translation performed by the front-end.
   Parameters describing the input language. The framework parameters for the input language
describe, for instance, the available boolean expressions, assertions, and statements. Fig. 8 provides
an overview of the parameters; in the following, we explain some of the most interesting ones;
further details are included in the appendix.
   Types and boolean expressions are fully described by the respective framework parameters
(𝑇𝐹 and 𝐵𝐸 𝐹 ). The parameter 𝐴𝐹 𝑝 for assertions describes a set of so-called input assertions; the
assertions supported by the front-end are then obtained using the following grammar, where
𝐴𝑝 ∈ 𝐴𝐹 𝑝 , 𝑏 ∈ 𝐵𝐸 𝐹 , 𝑡 ∈ 𝑇𝐹 , and 𝑃 is a designated symbol for recursive occurrences (as we explain
below):
                            𝐴 F 𝐴𝑝 | 𝑏 | 𝐴 ∗ 𝐴 | 𝐴 ∨ 𝐴 | 𝑏 ⇒ 𝐴 | ∃𝑥 : 𝑡 . 𝐴 | 𝑃 | 𝜇𝑃 . 𝐴
7We omit typing details here, but our Isabelle/HOL formalization includes them: it requires the state encoding to preserve

well-typedness and deals only with well-typed states (whose store and heap contain values of the types prescribed by Δ).
All states in §3 and §4 are implicitly assumed well-typed.
Sound State Encodings in Translational Separation Logic Verifiers (Extended Version)                                  330:13


       Framework parameter                                                  Description
                 𝑇𝐹                       Set of front-end types.
                 𝑉𝐹                       Set of front-end values.
           tp : 𝑉𝐹 → 𝑇𝐹                   Function that assigns each value 𝑣 ∈ 𝑉𝐹 a type 𝑡 ∈ 𝑇𝐹 .
                                          Set of front-end ghost heaps used for reasoning about the resources in front-end
                  𝐻𝐹
                                          states. They must be instantiated as an IDF algebra.
                𝐻𝑃                        Set of front-end program heaps.
         embed𝐻 : 𝐻𝑃 → 𝐻 𝐹                Function that embeds program heaps onto ghost heaps.
               𝐵𝐸 𝐹                       Set of front-end boolean expressions.
                                          Interpretation for each boolean expression 𝑏 ∈ 𝐵𝐸 𝐹 as a partial predicate on
 𝐼 B : 𝐵𝐸 𝐹 → (Σ𝐹 ⇀ { true, false } )
                                          front-end ghost states.
         fvB : 𝐵𝐸 𝐹 → P (Var)             (Possibly overapproximating) finite free variable set of a boolean expression.
                  𝐴𝐹 𝑝                    Set of input assertions.
                   Δ
                wf𝐴𝐹 (·)                  Well-formedness predicate on input assertions in a given type context Δ𝐹 .
          Δ                               Interpretation of each input assertion 𝐴𝑝 ∈ 𝐴𝐹 𝑝 as a set of front-end ghost
         𝐼 A 𝐹 : 𝐴𝐹 𝑝 → P (Σ𝐹 )
                                          states satisfying the assertion under type context Δ𝐹 .
         fvA : 𝐴𝐹 𝑝 → P (Var)             (Possibly overapproximating) finite free variable set of an input assertion.
                  𝐶𝐹 𝑝                    Set of primitive statements.
                   Δ
                wf𝐶𝐹 (·)                  Well-formedness predicate on primitive statements in a given type context Δ𝐹 .
                           𝑐              Operational semantic reduction rules for each primitive statement 𝑐 ∈ 𝐶 𝐹 𝑝 .
     Rules of the form 𝜎 →Δ𝐹 𝜎 ′
                                          𝜎, 𝜎 ′ ∈ Σ𝑃 are program pre- and post-states, and Δ𝐹 is a type context.
                                          CSL rules for primitive statements 𝑐 ∈ 𝐶 𝐹 𝑝 . Δ𝐹 is a front-end type context, and
  Rules of the form Δ𝐹 ⊢𝑝 {𝑃 } 𝑐 {𝑄 }
                                          𝑃 and 𝑄 are front-end semantic assertions (i.e., sets of front-end ghost states).
                                          (Possibly overapproximating) finite modified variable set of a primitive state-
         wr : 𝐶 𝐹 𝑝 → P (Var)
                                          ment.
         fvC : 𝐶 𝐹 𝑝 → P (Var)            (Possibly overapproximating) finite free variable set of a primitive statement.

                                Fig. 8. Framework parameters for the input language.


That is, separating conjunctions, disjunctions, implications, existential quantifiers, and inductive
predicates are built into the framework, because they preserve backward satisfiability (as we
present in Lemma 1) and we can thus reduce the effort of users of our framework to only proving
backward satisfiability for input assertions; all other SL connectives (e.g., magic wands) have to
be provided as input assertions. Following Dardinier et al. [10], we formalize inductive predicates
with one designated symbol 𝑃, which represents a recursive occurrence inside the least fixed-point
computation 𝜇𝑃 . 𝐴. For example, the standard linked-list inductive predicate can be expressed as8
      𝜇𝑃 . x ≠ null ⇒ ( acc(x.val) ∗ acc(x.next) ∗ (∃𝑣 : Ref. v = x.next ∗ (∃𝑥 : Ref. x = v ∗ 𝑃)))

 𝐼 AΔ𝐹 is extended to an interpretation function on all front-end assertions using the standard
interpretation for the built-in connectives and the least fixed point interpretation for inductive
predicates. fvA , the function that returns the set of free variables for assertions, and wf𝐴Δ𝐹 , the well-
formedness predicates of assertions, are extended to all front-end composite assertions accordingly.
The concrete definitions of the extensions of 𝐼 AΔ𝐹 , fvA , and wf𝐴Δ𝐹 are in Appendix A.
     Similarly, the parameter for statements 𝐶𝑝 provides a set of primitive statements, from which the
framework derives the set of statements using the following grammar, where 𝐶𝑝 ∈ 𝐶 𝐹 𝑝 , 𝑏 ∈ 𝐵𝐸 𝐹 ,
and 𝐴 is a front-end assertion:
       𝐶 F skip | 𝐶𝑝 | 𝐶; 𝐶 | if (𝑏) {𝐶} else {𝐶} | while (𝑏) inv 𝐴 {𝐶} | {𝐴} 𝐶 {𝐴} || {𝐴} 𝐶 {𝐴}

8 The standard linked-list predicate is usually defined as List(x) ≜ x ≠ null ⇒ ( acc(x.val) ∗ acc(x.next) ∗List( x.next ) ).

In our syntax, the recursive occurrence 𝑃 (which in our example represents List) does not take explicit arguments as input;
we thus use an existential quantifier to bind the heap-dependent expression x.next to the implicit argument x.
330:14                                               Hongyi Ling, Thibault Dardinier, Ellen Arlt, and Peter Müller


 Loops and parallel compositions contain assertions (invariants for loops, and pre- and postcondi-
tions for each parallel branch) for verification purposes. wf𝐶 , fvC , and wr can be extended to all
front-end statements in a straightforward way, as shown in Appendix A.
   The small-step operational semantic reduction rules and CSL rules for these control structures
are fixed to the standard ones in the framework, as shown in Appendix A. For primitive statements,
they are expressed by the framework parameters.
   To customize the state model of the input language, the framework has parameters for types
(𝑇𝐹 ), values (𝑉𝐹 ), program heaps (𝐻𝑃 ), and ghost heaps (𝐻 𝐹 ). Intuitively, program heaps abstract the
memory part of execution states and are involved in the definition of the operational semantics of the
front-end language. In contrast, ghost heaps typically include the program heaps and additional SL
resources (e.g., permission masks) for reasoning under SL. They are thus elements of an IDF algebra.
We define front-end ghost states Σ𝐹 = (Var ⇀ 𝑉𝐹 ) × 𝐻 𝐹 and program states Σ𝑃 = (Var ⇀ 𝑉𝐹 ) × 𝐻𝑃
to consist of a store of local variables and a ghost (resp. program) heap. The embedding function
embed𝐻 of heaps can then be naturally extended to an embedding embed𝑆 : Σ𝑃 → Σ𝐹 of program
states onto ghost states.

   Parameters describing the front-end translation. Our framework captures the translation
from the front-end language to the IVL by parameters J·KT , J·KV , J·KH , J·KΔ , J·KB , J·KAp , and J·KCp
for the translation of front-end types, values, ghost heaps, type contexts, boolean expressions,
input assertions, and primitive statements, respectively. The functions J·KAp and J·KCp may translate
front-end input assertions and primitive statements into composite ones in the IVL.
   The translation of types and values may in general lose information. For example, when translat-
ing the front-end type Rat of rational values into the IVL type Real of real values, the rationality of
front-end values will not be reflected in their IVL translation. As a result, witnesses for existential
quantifiers in the IVL do not necessarily witness the corresponding quantifier in the input program,
which could cause the translation to be unsound.
   To avoid this unsoundness, our framework offers another parameter typeInv that is used to
constrain the possible witnesses in the IVL-translation. For any front-end type 𝑡 ∈ 𝑇𝐹 and local
variable 𝑥 ∈ Var, typeInv(𝑡, 𝑥) yields a syntactic boolean IVL expression that evaluates to true iff
the value of variable 𝑥 in the IVL state has a corresponding front-end value of type 𝑡. For example
when JRatKT = Real, we can define typeInv( Rat, 𝑥) ≜ (∃𝑎 : Int. ∃𝑏 : Int. 𝑏 ≠ 0 ∧ 𝑥 = 𝑎/𝑏). Using
this framework parameter, we extend the translation of input assertions to all front-end assertions
and obtain the assertion translation function J·KA . The definition of J∃𝑥 : 𝑡 . 𝐴KA is as follows; that
of the other cases is straightforward and is listed in Appendix A.
                              J∃𝑥 : 𝑡 . 𝐴KA ≜ ∃𝑥 : J𝑡KT . typeInv(𝑡, 𝑥) ∗ J𝐴KA

   Our framework translates loops and parallel compositions in an overapproximating way as
verifiers like Viper do: the loop body or each thread in the parallel composition is translated
together with its annotations as a separate program; we collect these programs to form a set of
auxiliary IVL statements J𝑐Kext
                             C for the front-end statement 𝑐. If 𝑐 does not contain loops or parallel
compositions, J𝑐Kext
                   C   is empty. In the main program, each statement 𝑐 is translated to J𝑐Kmain
                                                                                            C . If 𝑐
                                        main
is a loop or parallel composition, J𝑐KC is a sequence of exhale-havoc-inhale statements which
first remove the resources specified by the annotations that are required to execute the block, then
assign fresh values to all local variables that the execution of the block might modify, and finally
add back the resources specified by the annotations that the execution of the block yields. Given
J·KCp that translates front-end primitive statements into (possibly composite) IVL statements, our
framework thus defines the translation J𝑐KC of front-end composite statement 𝑐 as a pair of an IVL
statement J𝑐Kmain
               C   and a finite set of auxiliary IVL statements J𝑐Kext
                                                                   C . We give the definition of J·KC
Sound State Encodings in Translational Separation Logic Verifiers (Extended Version)                                          330:15

                                                                                    
               Jwhile (𝑏 ) inv 𝐼 {𝑐 }KC ≜ exhale J𝐼 KA ∗ J𝑏KB ∨ ¬ J𝑏KB ; havoc wr(𝑐 ); inhale J𝐼 KA ∗ ¬ J𝑏KB ,
                                              n                                                                     o    
                                                                             main
                                                inhale J𝐼 KA ∗ J𝑏KA ; J𝑐KC        ; exhale J𝐼 KA ∗ J𝑏KB ∨ ¬ J𝑏KB ∪ J𝑐Kext
                                                                                                                        C
                                                
  J{𝑃 1 } 𝑐 1 {𝑄 1 } | | {𝑃 2 } 𝑐 2 {𝑄 2 }KC ≜ exhale J𝑃 1 ∗ 𝑃 2 KA ; havoc wr(𝑐 1 ) ∪ wr(𝑐 2 ); inhale J𝑄 1 ∗ 𝑄 2 KA ,
                                              n                                              o
                                                                       main
                                                inhale J𝑃 1 KA ; J𝑐 1 KC    ; exhale J𝑄 1 KA ∪
                                              n                                              o                      
                                                                       main
                                                inhale J𝑃 2 KA ; J𝑐 2 KC     ; exhale J𝑄 2 KA ∪ J𝑐 1 Kext       ext
                                                                                                      C ∪ J𝑐 2 KC



Fig. 9. The translation J·KC of front-end loops and parallel compositions. The full definition of J·KC is in
Appendix A. The condition J𝑏KB ∨ ¬ J𝑏KB in the translation of loops excludes states in which the evaluation of
J𝑏KB fails (e.g., due to a division by zero). Here we assume that the IVL supports (1) disjunction and negation
of pure boolean expressions, and (2) directly using pure boolean expressions as assertions. It can therefore
construct assertions including J𝑏KB ∨ ¬ J𝑏KB . havoc 𝑉 is a shorthand for havoc 𝑥 1 ; · · · ; havoc 𝑥𝑛 for the
finite set 𝑉 = {𝑥 1, . . . , 𝑥𝑛 }.


for loops and parallel compositions in Fig. 9. That for the other control structures is straightforward;
the full definition of J·KC is in Appendix A.
   Finally, the provided parameters let us extend the encoding      of front-end ghost heaps to an
encoding J·KS of front-end ghost states: J(𝑠, 𝜑)KS ≜ J𝑠KSt , J𝜑KH , where the store encoding J𝑠KSt is
defined as:                             
                                                      undefined,      𝑠 (𝑥) is undefined
                                     J𝑠KSt (𝑥) =
                                                      J𝑠 (𝑥)KV ,      otherwise

3.3    Requirements on the Framework Parameters
In this subsection, we present the requirements on the framework parameters that guarantee the
soundness of the front-end translation. Most of these requirements for the parameters from Fig. 8
as well as the translations of types and values are standard and easy to satisfy; we list them in
Appendix A.
   Req. 1 states the homomorphism property of the state encoding. We state it on the ghost heap
encoding parameter J·KH of the framework rather than the derived ghost state encoding J·KS ; the
homomorphism result of J·KS can be easily derived from that of J·KH in Req. 1. The second property
here is a sanity requirement that prevents the heap encoding from introducing garbage that has no
correspondence in the front-end; while in the diagram of Fig. 3, backward satisfiability provides
𝜔𝐴 , this property guarantees the existence of 𝜔 𝐹 and thus helps complete the desired state split in
the front-end. Moreover, we require a third property, which allows us to support IDF.
Requirement 1. The encoding of ghost heaps J·KH must satisfy the following properties:
   • J·KH preserves addition ⊕ when the sum of ghost heaps is defined in the front-end, i.e., if 𝜑 1 ⊕ 𝜑 2
      is defined, then so is J𝜑 1 KH ⊕ J𝜑 2 KH and J𝜑 1 KH ⊕ J𝜑 2 KH = J𝜑 1 ⊕ 𝜑 2 KH .
   • J·KH preserves subtraction in the following sense: if J𝜑KH = Φ1 ⊕ J𝜑 2 KH , then there exists some
      𝜑 1 such that Φ1 ⪰ J𝜑 1 KH and 𝜑 = 𝜑 1 ⊕ 𝜑 2 , where 𝑎 ⪰ 𝑏 ≜ (∃𝑟 . 𝑎 = 𝑏 ⊕ 𝑟 ).
   • J·KH preserves stability. Specifically, stabilize(J𝜑KH ) = Jstabilize(𝜑)KH for any front-end ghost
      heap 𝜑 ∈ 𝐻 𝐹 .
  With the parameters of the front-end language and the translation from §3.2, we formally define
backward satisfiability for front-end assertions in Def. 3.
Definition 3 (Backward satisfiability). A front-end assertion 𝐴 is backward satisfiable w.r.t. the
assertion translation J·KA iff: for any IVL state Ω that satisfies J𝐴KA , and that is upper-bounded by
330:16                                                      Hongyi Ling, Thibault Dardinier, Ellen Arlt, and Peter Müller


the encoding of some front-end state 𝜔𝑏 , i.e., J𝜔𝑏 KS ⪰ Ω, there exists a front-end state 𝜔 which
satisfies 𝐴 and Ω ⊕ | J𝜔𝑏 KS | ⪰ J𝜔KS 9 .
   Req. 2 formalizes that the translations of boolean expressions, assertions, and statements must
preserve the semantics in the front-end. For assertions, we require in addition monotonicity of
translated assertions, a property that is naturally satisfied in an affine logic, and that the translation
does not add new free occurrences of 𝑃. Together with backward satisfiability, it ensures that
whenever the IVL satisfies a separating conjunction, the front-end can also satisfy it by redistributing
the resources between the conjuncts. We make the requirements only for input assertions in Req. 2,
and prove Lemma 1 as part of the framework that these properties hold for all front-end assertions.
Requirement 2. The translation functions for boolean expressions, input assertions, and primitive
statements must satisfy the following properties:
     • The translation J𝑏KB of any front-end boolean expression 𝑏 ∈ 𝐵𝐸 𝐹 preserves the semantics of 𝑏,
       i.e., for any front-end state 𝜔 ∈ Σ𝐹 , 𝐼 B (𝑏) (𝜔) is defined iff J𝑏KB (J𝜔KS ) is defined, and they
       evaluate to the same truth value when both are defined.
     • The translation of input assertions J·KAp must satisfy:
          – J·KAp preserves the semantics of all well-formed input assertions (i.e., each 𝐴 such that
              wf𝐴Δ𝐹 (𝐴)) in the front-end. Concretely, for any front-end state 𝜔 and any input assertion
              𝐴, 𝜔 satisfies 𝐴 iff J𝜔KS satisfies J𝐴KAp .
          – J𝐴KAp is monotone for any input front-end assertion 𝐴. An assertion 𝑄 is monotone iff for
              any states Ω and Ω ′ , if Ω satisfies 𝑄 and Ω ′ ⪰ Ω, then Ω ′ also satisfies 𝑄.
          – J𝐴KAp of any input front-end assertion 𝐴 does not contain any free occurrence of 𝑃.
          – All well-formed input assertions are backward satisfiable w.r.t. J·KAp .
     • The translation of statements J·KCp preserves the semantics in the front-end, see formalization
       in Appendix A.
Lemma 1 (Extending requirements to all front-end assertions). If the translation J·KA is monotone,
does not add new free occurrences of 𝑃, and preserves the semantics for front-end assertions 𝐴1 and 𝐴2 ,
and these two assertions are backward satisfiable w.r.t. J·KA , then these properties are preserved by J·KA
of 𝐴1 ∗ 𝐴2 , 𝐴1 ∨ 𝐴2 , 𝐴1 ⇒ 𝐴2 (for a pure 𝐴1 ), ∃𝑥 : 𝑡 . 𝐴1 , and 𝜇𝑃 . 𝐴1 .
   As a corollary, J·KA is monotone and preserves the semantics for all well-formed front-end assertions,
and all well-formed front-end assertions are backward satisfiable w.r.t. J·KA .
  In contrast, magic wands −∗, universal quantifications ∀, and iterated separating conjunctions ⊛
do not necessarily preserve backward satisfiability of their components. For instance, assertions
𝑊 , 𝑃1 , and 𝑃2 from the two examples in §2.5 are not backward satisfiable (as explained in the
corresponding examples), even though their components are by Lemma 1. For assertions containing
these connectives, backward satisfiability needs to be proven without the help from Lemma 1.

3.4      Soundness
The conditions presented in the previous subsection are sufficient to guarantee that the front-end
translation described by a given instantiation of our framework is sound. In the following, we
summarize the soundness argument. The full proof is in our Isabelle/HOL formalization.
   One of our central lemmas shows that the state encoding preserves the validity of separating
conjunctions if the first conjunct is monotone and the second is backward satisfiable. This property
9 The stronger statement Ω ⪰ J𝜔K from Fig. 3 might not be satisfied by some front-ends (e.g., the one encoding lazy field
                                S
creation in §4.3) in the IDF algebra setting, as Ω might lose some pure information from 𝜔𝑏 which is necessary to construct
𝜔.
Sound State Encodings in Translational Separation Logic Verifiers (Extended Version)                   330:17


is essential to show that assertions retain the meaning, no matter whether they are assumed or
asserted. It is, in fact, one of the main reasons we require assertions to be backward satisfiable:

Lemma 2 (Translation of separating conjunctions). For any IVL semantic assertion 𝐴, define
btr(𝐴) ≜ {𝜔 | J𝜔KS ∈ 𝐴} as the backward translation of 𝐴, i.e., the collection of all front-end states
whose encodings satisfy 𝐴.
   For arbitrary IVL semantic assertions 𝐴 and 𝐵, btr(𝐴) ∗ btr(𝐵) ⊆ btr(𝐴 ∗ 𝐵). Furthermore, when
𝐴 is monotone, and 𝐵 is the translation of some backward satisfiable front-end assertion, the other
direction also holds, i.e., btr(𝐴 ∗ 𝐵) ⊆ btr(𝐴) ∗ btr(𝐵).

  Lemma 2 allows us to prove Lemma 3 which states that the exhale-havoc-inhale translation
pattern that appears in the translation of both loops and parallel compositions (as in Fig. 9) is sound.
The proof proceeds by applying the CSL frame rule on the CSL proof from the first property of
Lemma 3 with a carefully chosen frame assertion, followed by an application of the consequence
rule where the implications at the pre- and postconditions in the consequence rule are justified by
the two directions of implication in Lemma 2 respectively.

Lemma 3 (Soundness of the exhale-havoc-inhale translation pattern). Assume that the framework
parameters satisfy Req. 1 and Req. 2, 𝑃0 and 𝑄 0 are well-formed, and that the following properties hold:
      • Δ𝐹 ⊢CSL {𝐼 AΔ𝐹 (𝑃0 )} 𝑐 {𝐼 AΔ𝐹 (𝑄 0 )}. That is, the front-end loop or parallel composition block has
        a proof under CSL against the pre- and postconditions from the annotation of the block.
      • JΔ𝐹 KΔ ⊢ [𝑃] exhale J𝑃0 KA ; havoc wr(𝑐); inhale J𝑄 0 KA [𝑄]. That is, the main program of
        the translation of the loop or parallel composition verifies against another given pair of pre-
        and postconditions in the IVL.
      • The given IVL pre- and postconditions 𝑃 and 𝑄 are monotone.
      • All written variables of the loop or parallel composition block are declared, and thus included
        in the type context, i.e., wr(𝑐) ⊆ dom(Δ𝐹 ).
Then Δ𝐹 ⊢CSL {btr(𝑃)} 𝑐 {btr(𝑄)}. That is, the front-end CSL proof for the block can be lifted to against
the new pre- and postconditions backward translated from the IVL.

  We can then prove our central soundness result stated as Thm. 4. The proof proceeds by induction
on the structure of front-end statements, where for the loop and parallel composition cases, we can
apply Lemma 3 with the IVL assertions 𝑃 and 𝑄 in the lemma as the translation of the desired front-
end pre- and postconditions J𝑃KA and J𝑄KA and the first property derived by applying induction
hypotheses on the axiomatic semantic proofs of the auxiliary IVL statements and CSL loop rule or
parallel rule subsequently.

Theorem 4 (Soundness). Assume that the framework parameters satisfy Req. 1 and Req. 2. Let 𝑐
be a well-formed front-end composite statement w.r.t. type context Δ𝐹 , and J𝑐KC = (𝐶𝑚 , 𝐶𝑒 ) be the
translation of 𝑐. Let 𝑃 and 𝑄 be arbitrary well-formed front-end composite assertions. Assume (1)
JΔ𝐹 KΔ ⊢ [J𝑃KA ] 𝐶𝑚 [J𝑄KA ], and (2) any 𝐶 ∈ 𝐶𝑒 verifies in the IVL, i.e., there exists an IVL semantic
assertion 𝑄𝐶 such that JΔ𝐹 KΔ ⊢ [⊤] 𝐶 [𝑄𝐶 ]. Then Δ𝐹 ⊢CSL {𝐼 AΔ𝐹 (𝑃)} 𝑐 {𝐼 AΔ𝐹 (𝑄)} holds in CSL.

   This theorem guarantees that, whenever the IVL translation of a front-end program is correct
then there exists a proof in CSL for the front-end program. To further connect this result to the
operational semantics of the front-end language, we also prove the soundness of the CSL rules w.r.t.
the small-step semantics. Our proof adapts the proof from Vafeiadis [55] to our IDF setting. The
formal statement of this result is in Appendix A.
330:18                                              Hongyi Ling, Thibault Dardinier, Ellen Arlt, and Peter Müller


3.5      Generalization to State Encoding Relations
As we have seen in §2.1, some front-ends might relate a single front-end state with multiple IVL
states, as in the case of encoding duplicable permissions. To capture such encodings, we generalize
the state encoding from a function J·KS to a binary relation · ∼S · between front-end states and IVL
states and write 𝜔 ∼S Ω if IVL state Ω is one of the possible encodings of front-end state 𝜔.
   The generalized framework takes the same inputs as in Fig. 8, except that the heap encoding
function J·KH is replaced by a binary relation · ∼H · that models the encoding of front-end ghost
heaps into IVL heaps. The framework extends · ∼H · naturally to the binary relation · ∼S · between
front-end and IVL states: (𝑠, ℎ) ∼S (𝑆, 𝐻 ) ≜ (𝑆 = J𝑠KSt ∧ ℎ ∼H 𝐻 ).
   Most requirements of our framework are not affected by this generalization, but Req. 1 and Req. 2
need to be adapted:
Requirement 1′ . The binary relation · ∼H · between front-end ghost heaps and IVL heaps need to
satisfy the following properties.
      • If 𝜑 = 𝜑 1 ⊕ 𝜑 2 and 𝜑 ∼H Φ, then there exist Φ1 and Φ2 such that Φ = Φ1 ⊕ Φ2 , 𝜑 1 ∼H Φ1 , and
        𝜑 2 ∼H Φ2 .
      • If 𝜑 ∼H Φ and 𝜑 0 = 𝜑 ⊕ 𝜑 1 , then there exists Φ1 such that 𝜑 1 ∼H Φ1 , Φ ⊕ Φ1 is defined, and
        𝜑 0 ∼H (Φ ⊕ Φ1 ).
      • For every front-end ghost heap 𝜑 ∈ 𝐻 𝐹 , there exists an IVL heap Φ ∈ Σ such that 𝜑 ∼H Φ.
      • If 𝜑 ∼H Φ, then stabilize(𝜑) ∼H stabilize(Φ).
      • If stabilize(𝜑) ∼H Φ′ , then ∃Φ such that stabilize(Φ) = stabilize(Φ′ ) and 𝜑 ∼H Φ.
  Compared with Req. 1 in §3.3, the adaptation is in the following ways:
      • The first property in Req. 1 (preservation of addition) is adjusted in a straightforward way.
      • The second property in Req. 1 (preservation of subtraction) is now subsumed by a generalized
        backward satisfiability, see below.
      • The second property here excludes certain ill-formed encodings by requiring that whenever
        a heap can be extended in the front-end, the corresponding extension is possible in the IVL
        (for instance, it is not possible to encode a fractional permission in the front-end to a full
        permission in the IVL). For the case where the heap encoding is a function, this property
        follows from the addition requirement and is, thus, not explicitly required in Req. 1.
      • The third property here, intuitively, ensures that the encoding is non-degenerated.
      • The preservation of stability (i.e., the last requirement in Req. 1) is adapted to the last two
        requirements here.
   We adjust the definition of backward satisfiability to Def. 5. The definition coincides with the
intuition in Fig. 3, except that now 𝜔 𝐹 may be encoded into an even larger Ω𝐹′ rather than Ω𝐹 . This
relaxation gives more flexibility with no affection on the soundness of the framework, intuitively
because excess resources can always be discarded harmlessly in an affine SL.
Definition 5 (Generalized backward satisfiability). A front-end assertion 𝐴 has generalized back-
ward satisfiability w.r.t. the assertion translation J·KA iff: for any front-end state 𝜔 and IVL states Ω,
Ω𝐴 , and Ω𝐹 , if 𝜔 ∼S Ω, Ω = Ω𝐴 ⊕ Ω𝐹 , and Ω𝐴 satisfies J𝐴KA , then there exist front-end states 𝜔𝐴
and 𝜔 𝐹 and IVL state Ω𝐹′ such that: 𝜔 = 𝜔𝐴 ⊕ 𝜔 𝐹 , 𝜔𝐴 satisfies 𝐴, 𝜔 𝐹 ∼S Ω𝐹′ , and Ω𝐹′ ⪰ Ω𝐹 .
  With the generalized backward satisfiability notion, Req. 2 from §3.3 needs only technical
adaptations:
Requirement 2′ . The translation functions for boolean expressions, input assertions, and primitive
statements must satisfy the following properties:
Sound State Encodings in Translational Separation Logic Verifiers (Extended Version)                   330:19


      • The translation J𝑏KB of any front-end boolean expression 𝑏 ∈ 𝐵𝐸 𝐹 preserves the semantics of 𝑏,
        i.e., for any front-end state 𝜔 ∈ Σ𝐹 and IVL state Ω ∈ Σ𝑉 with 𝜔 ∼S Ω, 𝐼 B (𝑏) (𝜔) is defined
        iff J𝑏KB (Ω) is defined, and they evaluate to the same value when both are defined.
      • The translation of input assertions J·KAp must satisfy:
           – J·KAp preserves the semantics of all well-formed input assertions in the front-end. Concretely,
               for any front-end state 𝜔 and IVL state Ω with 𝜔 ∼S Ω, 𝜔 satisfies 𝐴 iff Ω satisfies J𝐴KAp .
           – J𝐴KAp is monotone for any 𝐴 ∈ 𝐴𝐹 𝑝 .
           – J𝐴KAp of any input front-end assertion 𝐴 does not contain any free occurrence of 𝑃.
           – Any well-formed 𝐴 ∈ 𝐴𝐹 𝑝 has generalized backward satisfiability w.r.t. J·KAp .
      • The translation of statements J·KCp preserves the semantics in the front-end.
    To show that our framework for state encoding relations is indeed a generalization, we instantiate
it, modeling the state encoding as a function, as stated in Thm. 6.
Theorem 6 (Generalization). Given an instantiation of the generalized framework where the state
encoding is a function, if this instantiation satisfies all requirements from §3.3 then it also satisfies the
adapted requirements of the generalized framework.
   Our main result is that any instantiation of the generalized framework that satisfies the adapted
requirements is sound. That is, Thm. 4, with the adapted requirements, also holds in the generalized
framework.
   The proof of the theorem requires several adaptations. In the generalized setting, we define the
backward translation of IVL semantic assertion 𝑃 as btr(𝑃) ≜ {𝜔 | ∃Ω ∈ 𝑃 . 𝜔 ∼S Ω}, and call 𝑃
well-formed iff btr(𝑃) = {𝜔 | ∀Ω. 𝜔 ∼S Ω ⇒ Ω ∈ 𝑃 }. The direction btr(𝐴) ∗ btr(𝐵) ⊆ btr(𝐴 ∗ 𝐵)
in Lemma 2 does not hold for general 𝐴 and 𝐵 anymore, but requires 𝐵 to be well-formed. As a
result, 𝑄 0 being well-formed is needed for Lemma 3. Despite these changes, we prove that all the
assertions supported by a front-end instantiation of our generalized framework are well-formed
as long as the instantiation satisfies all the requirements in §3.5. As a result, the new premise in
Lemma 3 is always satisfied, and we get the same soundness result as Thm. 4 in the generalized
framework.
   The generalized framework provides an expressive foundation for proving the soundness of
practical translational verifiers. In particular, it reduces the soundness proof for state encodings to
proving a small number of relatively simple requirements. We will demonstrate this expressiveness
in §4.4 by instantiating it with an encoding of duplicable permissions for immutable location.

4   Applications of the Framework
In this section, we demonstrate the applicability of our framework by formalizing three front-end
translations with different state encodings into Viper, whose state model we formally define in
§4.1. We first revisit the encoding from rational permission amount to reals (§4.2), and we show
how to extend this encoding to support a backward-satisfiable fragment of magic wands used by
Prusti [1]. We also translate a language with lazy field creation (§4.3), and show an encoding of
an immutable heap (§4.4). We describe more encodings inspired by real-world front-ends (§4.5).
Finally, we discuss previously-reported soundness bugs in existing translational verifiers whose
root causes manifest themselves as violations of our framework’s requirements (§4.6).
   In all the examples, our framework substantially simplifies the effort required for defining the
translation and proving it sound: a formalization without our framework would essentially have to
repeat the definitions and proofs of our main theorems, in addition to proving the requirements
of our framework. Our framework also makes the soundness proof easy to maintain in practice,
as it decomposes the global soundness of a front-end translation into local proof obligations:
330:20                                                   Hongyi Ling, Thibault Dardinier, Ellen Arlt, and Peter Müller


the translation of each input assertion must be backward satisfiable, and the translation of each
primitive statement must be sound. This modularity keeps the proof robust under changes: adding
a new input assertion (e.g., the sound magic wand fragment in §4.2) does not require revisiting the
overall soundness argument, only proving the corresponding requirements for that assertion.

4.1      Viper State Model
The formalization of Viper we use models the heap as a partial function from heap locations
to values and the currently-owned permissions as a partial function from heap locations to real
numbers, called permission mask. A heap ℎ with a permission mask 𝜋 forms an IDF algebra with the
following instantiations: Σ = {(ℎ, 𝜋) ∈ (𝐿 ⇀ 𝑉 ) × (𝐿 → [0, 1]) | ∀𝑙 . 𝜋 (𝑙) > 0 ⇒ ℎ(𝑙) ≠ ⊥}, where
a heap location 𝑙 ∈ 𝐿 is a pair of an address (modeled as natural number) and a field (identified
by a unique name); ⊕ adds up the permission amounts at each heap location and combines the
values in the heap when the two heaps are compatible (the sum of permissions at each heap
location does not exceed 1, and the two heaps do not have different values at any heap location), i.e.,
(ℎ 1, 𝜋1 ) ⊕ (ℎ 2, 𝜋2 ) is defined iff ∀𝑙 . 𝜋 1 (𝑙) +𝜋2 (𝑙) ≤ 1∧ (𝑙 ∈ dom(ℎ 1 ) ∩dom(ℎ 2 ) ⇒ ℎ 1 (𝑙) = ℎ 2 (𝑙)), and
equals to (ℎ 1 ∪ ℎ 2, 𝜋1 + 𝜋 2 ) when it is defined; |_| clears all the permissions, i.e., |(ℎ, 𝜋)| ≜ (ℎ, 𝜆𝑙 . 0);
stabilize erases all values for heap locations to which no permission is held, i.e., stabilize((ℎ, 𝜋)) ≜
(𝜆𝑙 . if 𝜋 (𝑙) > 0 then ℎ(𝑙) else ⊥, 𝜋); stable asserts whether every heap location storing a concrete
value has a positive permission amount, i.e., stable((ℎ, 𝜋)) ⇔ (∀𝑙 . ℎ(𝑙) ≠ ⊥ ⇒ 𝜋 (𝑙) > 0); unit
erases the whole heap with the permissions, i.e., unit((ℎ, 𝜋)) = (𝜆𝑙 . ⊥, 𝜆𝑙 . 0);
   A Viper state is thus an IVL state where the customized heap is instantiated with a heap with a
permission mask, i.e., Σ𝑉 = (Var ⇀ 𝑉 ) × Σ with Σ defined above.

4.2      Encoding Rational Permission Amounts into Real Permission Amounts
In §2.5, we showed that the common encoding of fractional permissions with rational permission
amounts into real permission amounts is generally unsound. Our example there made use of magic
wands. In this subsection, we show that such an encoding is sound for a front-end with a more
restricted assertion language.
   To focus on the essentials, we assume that the front-end language is very similar to our IVL,
Viper. Both have the same types (e.g., for booleans, integers, and references), values (e.g., null),
and expressions (except that the front-end uses rational arithmetic whereas the IVL uses reals).
Among the primitive statements, local variable assignment and field assignment are common to
front-end language and IVL; moreover, the front-end supports allocation and de-allocation, whose
translation is discussed below.
   We provide the details of the instantiation of our framework in Appendix B.1 and focus on
the most interesting aspects here. The front-end models the program heap as a partial map from
heap locations (as pairs of natural number identifiers and string-named fields, which is the same
as in Viper) to values, and uses rational permission amounts for its ghost heap, i.e., 𝐻𝑃 = {ℎ𝑝 :
𝐿 ⇀fin 𝑉𝐹 } where ⇀fin represents a finite partial mapping , and 𝐻 𝐹 = {(ℎ, 𝜋) ∈ (𝐿 ⇀ 𝑉𝐹 ) × (𝐿 →
[0, 1] ∩ Q) | ∀𝑙 . 𝜋 (𝑙) > 0 ⇒ ℎ(𝑙) ≠ ⊥}. The embedding of 𝐻𝑃 onto 𝐻 𝐹 keeps the partial heap, and
assigns full permissions to heap locations that contain values and zero permissions otherwise:
embed𝐻 (ℎ𝑝 ) = (ℎ𝑝 , 𝜆𝑙 . if ℎ𝑝 (𝑙) ≠ ⊥ then 1 else 0).
   Due to the similarity of the front-end language and IVL, the translation functions for types,
values, ghost heaps, and expressions are straightforward, except that the type Rat is translated to
Real. typeInv(𝑡, 𝑥) is thus non-trivial only for 𝑡 = Rat as typeInv( Rat, 𝑥) ≜ ∃𝑎 : Int. ∃𝑏 : Int. 𝑏 ≠
0 ∧ 𝑥 = 𝑎/𝑏.
   The input assertion acc (𝑥 .𝑓 , 𝑝) is translated unchanged to acc (𝑥 .𝑓 , 𝑝). Preservation of semantics
of the translation and monotonicity of the translated assertion are straightforward. Backward
Sound State Encodings in Translational Separation Logic Verifiers (Extended Version)                             330:21


satisfiability is also intuitive: if J𝑝KE 10 evaluates to 𝑣 under some Ω with J𝜔𝑏 KS ⪰ Ω, then it also
evaluates to 𝑣 under J𝜔𝑏 KS (adding resources cannot change a defined evaluation), and hence to
𝑣 under 𝜔𝑏 in the front-end, so 𝑣 is rational. The front-end state holding just 𝑣 permission to 𝑥 .𝑓
(and only the information needed to evaluate 𝑥 and 𝑝) is therefore the smallest state satisfying
acc (𝑥 .𝑓 , 𝑝), and its encoding is smaller than or equal to Ω.
   The translations of variable assignment and field assignment are straightforward. Allocation
and de-allocation are translated as follows:
                 J𝑥 := alloc (𝑓1, . . . , 𝑓𝑛 )KCp ≜ havoc 𝑥; inhale acc (𝑥 .𝑓1, 1) ∗ · · · ∗ acc (𝑥 .𝑓𝑛 , 1)
                              Jfree (𝑥 .𝑓 )KCp ≜ exhale acc (𝑥 .𝑓 , 1)
 Intuitively, the translation of allocation picks non-deterministically a fresh heap location identifier
(havoc 𝑥) and provides the necessary permissions for the allocated heap locations; the translation
of de-allocation removes the permission to the deleted heap location.
   We prove in Isabelle/HOL that this instantiation satisfies all requirements of our framework. This
instantiation shows that translating rational permission amounts as reals is not per se unsound. If
we had added general magic wands as input assertions to our instantiation (as in Fig. 7 in §2.5)
then the proof would have failed because Req. 2 would not hold. Nevertheless, our framework can
still support a restricted fragment of magic wands.
   A sound fragment of magic wands. In practice, the magic wands used by existing verifiers
are often far more limited. Prusti [1], for instance, uses only wands whose two sides are binary
assertions (i.e., never use fractional permissions), and that do not access rational-valued fields.
Such assertions are given by the following grammar (we further check that the fields they read do
not have the type Rat with the framework’s well-formedness predicate wf𝐴Δ𝐹 ), where 𝑒 ∈ 𝐵𝐸 𝐹 and
𝑡 ∈ 𝑇𝐹 :
                         𝐴𝑏 F acc (𝑥 .𝑓 , 1) | 𝑒 | 𝐴𝑏 ∗ 𝐴𝑏 | 𝐴𝑏 ∨ 𝐴𝑏 | 𝑒 ⇒ 𝐴𝑏 | ∃𝑥 : 𝑡 . 𝐴𝑏
  Each such assertion is translated like the corresponding case of J·KA in Appendix A; we write
J·KAb for this translation. We then add to the front-end’s input assertions all wands 𝐿 −∗ 𝑅 whose
two sides are binary assertions that do not access rational fields, with the standard interpretation
and J𝐿 −∗ 𝑅KAp ≜ J𝐿KAb −∗ J𝑅KAb . We prove in Isabelle/HOL that J𝐿 −∗ 𝑅KAp satisfies Req. 2, so this
fragment of magic wands is captured by our framework and, thus, sound.

4.3   Encoding Lazy Field Creation
In §1, we showed an encoding of a Python-like front-end language with lazy field creation into an
IVL with static field declarations. In this subsection, we define a front-end that formalizes the lazy
field creation feature, and a translation into Viper. Our framework is able to capture this translation
to prove its soundness. This instantiation shows, in particular, that our framework is able to express
translations with different heap structures (each front-end field is encoded as two IVL fields) and
custom proof rules (as we explain below).
   We assume a front-end similar to the one from §4.2. Its logic reasons about lazy field creation as
follows: It governs access to a location 𝑥 .𝑓 using the standard accessibility predicate acc (𝑥 .𝑓 , 𝑝).
We assume that the front-end can determine statically which fields are potentially added to an
object, for instance, by using a type system such as Python’s MyPy. Allocation provides permission
to all those fields and sets their value to nofield to indicate that this field has not been created
yet. Field updates require permission to access the field, as usual. The first assignment to a field
creates the field, which is reflected by replacing nofield with the assigned value. Finally, field
read requires permission and asserts that the field value is different from nofield, as attempting
10We use J·K to denote the translation of general expressions (including non-boolean ones). It is not a parameter of our
            E
framework, but framework parameters can use it (like any other mathematical function).
330:22                                                     Hongyi Ling, Thibault Dardinier, Ellen Arlt, and Peter Müller


to read a field before it has been added triggers a runtime error. Since nofield is not part of the
surface syntax, the frontend provides pure input assertion added (𝑥 .𝑓 ) and missing (𝑥 .𝑓 ) to denote
𝑥 .𝑓 ≠ nofield and 𝑥 .𝑓 = nofield, respectively.
    To reflect this logic, the front-end provides the designated value nofield and uses it in its heap
model: 𝐻𝑃 = {ℎ𝑝 : 𝐿 ⇀fin 𝑉𝐹 ∪ {nofield}} and 𝐻 𝐹 = {(ℎ, 𝜋) ∈ (𝐿 ⇀ 𝑉𝐹 ∪ {nofield}) × (𝐿 →
[0, 1] ∩ Q) | ∀𝑙 . 𝜋 (𝑙) > 0 ⇒ ℎ(𝑙) ≠ ⊥}. The evaluation of a heap access expression 𝑥 .𝑓 is defined
only if its value is different from nofield. Other than that, the evaluation of expressions is the
same as in §4.2.
    Our front-end supports the input assertions acc (𝑥 .𝑓 , 𝑝), added (𝑥 .𝑓 ), and missing (𝑥 .𝑓 ). Com-
pared with the interpretation of acc (𝑥 .𝑓 , 𝑝) in the previous subsection, the interpretation here
additionally accepts the case where the field is missing, but excludes the case where 𝑝 evaluates to
0. The interpretation of added (𝑥 .𝑓 ) and missing (𝑥 .𝑓 ) is straightforward. The concrete definition
of 𝐼 AΔ𝐹 for the three input assertions is shown in Appendix B.2.
    Local variable assignments, allocations, and de-allocations have the same form as in the previous
subsection. For simplicity, we restrict field assignments to the form 𝑥 .𝑓 := 𝑣, where 𝑣 ∈ Var is a
local variable. The CSL rules for the primitive statements are the same as before, and so are the
operational semantic reduction rules for local variable and field assignments and de-allocations.
For an allocation 𝑥 := alloc (𝑓1, . . . , 𝑓𝑛 ), the allocated locations are initialized to nofield rather
than arbitrary concrete values. The formal reduction rule is shown in Appendix B.2.
    The most interesting aspect of this front-end is its state encoding. Each front-end field 𝑓 is
encoded by two IVL fields: The boolean field 𝑓added indicates whether the field 𝑓 has been added,
whereas the field 𝑓IVL stores the translated value of the front-end heap location. That is, our encoding
reflects the cases where a field has been added or not as follows (𝑣 is different from nofield).
                              𝑝                                       𝑝                    0
                         𝑎.𝑓 ↦→ nofield for 𝑝 ∈ [0, 1]       𝑎.𝑓added ↦→ false, 𝑎.𝑓IVL ↦→ ⊥
                                  𝑝                                   𝑝                𝑝
                             𝑎.𝑓 ↦→ 𝑣 for 𝑝 ∈ [0, 1]        𝑎.𝑓added ↦→ true, 𝑎.𝑓IVL ↦→ J𝑣KV
   Expressions are translated identically, except that every field name 𝑓 in field access expressions
is replaced by 𝑓IVL . The translation of input assertions needs to reflect the above state encoding. In
particular, Jacc (𝑥 .𝑓 , 𝑝)KA denotes permission to 𝑓added and, in case the field has been added, also
permission to 𝑓IVL :
      Jacc (𝑥 .𝑓 , 𝑝)KAp ≜ J𝑝KE > 0 ∗ acc (J𝑥KE .𝑓added , J𝑝KE ) ∗ (J𝑥KE .𝑓added = true ⇒ acc (J𝑥KE .𝑓IVL, J𝑝KE ))
  Field assignments are translated as follows:
               J𝑥 .𝑓 := 𝑣KCp ≜ if (J𝑥KE .𝑓added = false) {inhale acc (J𝑥KE .𝑓IVL, 1)} else {skip};
                              J𝑥KE .𝑓added := true; J𝑥KE .𝑓IVL := 𝑣
 Intuitively, it uses the field J𝑥KE .𝑓added to check whether this assignment dynamically creates
the field. If so, it adds full permission to the field J𝑥KE .𝑓IVL , which enables future read and write
accesses. Moreover, it records in J𝑥KE .𝑓added that the field has been created (in either case, as this
is a monotonic update), and assigns the value to J𝑥KE .𝑓IVL . The translation of the other primitive
statements is straightforward; the full definition is presented in Appendix B.2.
   The front-end translation described above satisfies all requirements of our framework (for state
encoding functions) and is, thus, guaranteed to be sound.

4.4      Encoding Immutable Heaps
Our final instantiation illustrates how our framework supports duplicable resources into an IVL that
offers only (non-duplicable) fractional resources. Duplicable resources have many applications, for
instance, as permission to acquire a lock or to represent monotonic information. In this subsection,
we use access to immutable data as an example for duplicable resources.
Sound State Encodings in Translational Separation Logic Verifiers (Extended Version)                                 330:23


    To avoid the complications of initializing immutable fields, we assume a front-end here, where
immutable data is stored in a separate heap. Field accesses select the heap using different deref-
erencing operators, 𝑥 .𝑓 for the mutable heap and 𝑥 ◦ 𝑓 for the immutable heap.11 Allocation in
the mutable heap works as usual, whereas allocation in the immutable heap takes as arguments
the initial values of the fields and initializes them. Hence, regular allocation provides the usual
ownership of the allocated locations, donated again by acc (𝑥 .𝑓 , 𝑝), whereas immutable allocation
provides a duplicable resource init (𝑥 ◦ 𝑓 ), which permits read access, but not assignments.
    To reflect these ideas, our front-end is similar to the one in §4.2, but has two heaps: 𝐻𝑃 =
{(ℎ, ℎ𝑖𝑚 ) ∈ (𝐿 ⇀ 𝑉𝐹 ) × (𝐿 ⇀ 𝑉𝐹 )}, where the first component is the mutable partial heap and the
second one is the immutable heap. The ghost heap set is 𝐻 𝐹 = {(ℎ, 𝜋, ℎ𝑖𝑚 ) ∈ (𝐿 ⇀ 𝑉𝐹 ) × (𝐿 →
[0, 1] ∩ Q) × (𝐿 ⇀ 𝑉𝐹 ) | ∀𝑙 . 𝜋 (𝑙) > 0 ⇒ ℎ(𝑙) ≠ ⊥}. The embedding function embed𝐻 maps the
immutable heap ℎ𝑖𝑚 identically and the mutable heap ℎ as to a heap (ℎ, 𝜋) with rational permissions.
The resource of each heap location in the immutable heap is stable and duplicable, i.e., the immutable
heap in 𝐻 𝐹 is instantiated as an IDF algebra with the following definitions of the operations:
        • ℎ 1 ⊕ ℎ 2 is defined iff ∀𝑙 ∈ 𝐿, if both ℎ 1 (𝑙) and ℎ 2 (𝑙) are defined then ℎ 1 (𝑙) = ℎ 2 (𝑙). In this
           case, (ℎ 1 ⊕ ℎ 2 ) (𝑙) ≜ if ℎ 1 (𝑙) is defined then ℎ 1 (𝑙) else ℎ 2 (𝑙).
        • |ℎ| = stabilize(ℎ) ≜ ℎ, and stable(ℎ) holds for any ℎ.
        • unit(ℎ) ≜ emp, where emp is the empty heap 𝜆𝑙 . ⊥.
    The front-end supports the same primitive statements as in §4.2. In addition, the statement
𝑥 := immalloc (𝑓 := 𝑣) allocates and initializes an immutable location 𝑥 ◦ 𝑓 . The operational
semantic reduction rule and CSL rule for this statement are straightforward; we list them in
Appendix B.3.
    Since our IVL does not provide duplicable resources, we encode them as arbitrary positive
fractional permission amounts. As a result, the representation for a duplicable front-end resource
is not unique. Our generalized framework allows us to express such state encoding relations.
    The encoding of front-end ghost heaps is modeled as a binary relation. Both front-end heaps are
encoded into a single IVL heap. To disambiguate accesses, we use a map 𝑓ℎ that maps each front-end
field 𝑓 in the mutable heap to the IVL field ℎ𝑓 ; the map 𝑓𝑣 analogously maps each front-end field 𝑔
in the immutable heap to the IVL field 𝑣𝑔. The ranges of 𝑓ℎ and 𝑓𝑣 are disjoint. The encoding of the
mutable heap is the same as in §4.2 (except that here field names are mapped). The (allocated) heap
locations in the immutable heap are encoded to having any permission 𝑝 ∈ (0, 1); that is, the state
relation permits all such amounts 𝑝. Un-allocated locations have zero permission and no value.
    To formalize the state encoding relation, we need to divide the IVL heap into the parts corre-
sponding to the mutable and immutable front-end heaps. In those parts, we then undo the field
name mappings 𝑓ℎ and 𝑓𝑣 so that we can relate them to the front-end fields. Concretely, we define
𝐻 | 𝑓ℎ to be the IVL sub-heap constructed by taking only locations with field names in the range of
𝑓ℎ ; we construct 𝐻 | 𝑓𝑣 analogously. 𝐻 rem denotes the remaining part of 𝐻 after removing 𝐻 | 𝑓ℎ and
𝐻 | 𝑓𝑣 . Π| 𝑓ℎ , Π| 𝑓𝑣 , and Π rem are defined similarly for the permission mask Π (while “removing” means
setting the permission to each location in the corresponding part to zero). Now we can define the
state relation, by reusing the ghost heap encoding J·KH from §4.2 for the mutable heap:
              (ℎ, 𝜋, ℎ𝑖𝑚 ) ∼H (𝐻, Π) ≜ 𝐻 | 𝑓ℎ , Π| 𝑓ℎ = J(ℎ, 𝜋)KH ∧ 𝐻 rem = 𝜆𝑙 . ⊥ ∧ Π rem = 𝜆𝑙 . 0 ∧ (∀𝑙 .
                                                     

                                        (ℎ𝑖𝑚 (𝑙) = ⊥ ⇒ (𝐻 | 𝑓𝑣 (𝑙) = ⊥ ∧ Π| 𝑓𝑣 (𝑙) = 0)) ∧
                                        (ℎ𝑖𝑚 (𝑙) = 𝑣 ⇒ (𝐻 | 𝑓𝑣 (𝑙) = J𝑣KV ∧ Π| 𝑓𝑣 (𝑙) ∈ (0, 1))))
  Heap access expressions are translated accordingly: the field names for all accesses to the mutable
heap (of the form 𝑥 .𝑓 ) are translated by 𝑓ℎ , while those for the accesses to the immutable heap (of
11 Note that both heaps share the same identifiers, so a field 𝑓 may occur in both heaps, and a syntactic distinction of the

two accesses is necessary.
330:24                                                        Hongyi Ling, Thibault Dardinier, Ellen Arlt, and Peter Müller


the form 𝑥 ◦ 𝑓 ) are translated by 𝑓𝑣 . The translation for the input assertions are as follows, where
acc (𝑥 .𝑓 , _) represents ownership of an arbitrary positive fractional permission amount for 𝑥 .𝑓 .
            Jacc (𝑥 .𝑓 , 𝑝)KAp ≜ acc (J𝑥KE .𝑓ℎ (𝑓 ), J𝑝KE )           Jinit (𝑥 ◦ 𝑓 )KAp ≜ acc (J𝑥KE .𝑓𝑣 (𝑓 ), _)
   The translation of local variable assignments, allocations in the mutable heap, and de-allocations
is similar to that in §4.2; we show them in Appendix B.3. The translation of allocation in the
immutable heap assigns a fresh heap location, adds the resource corresponding to init (𝑥 ◦ 𝑓 ) to
the state, and assumes that the new location has its initial value:
                  J𝑥 := immalloc (𝑓 := 𝑣)KCp ≜ havoc 𝑥; inhale acc (𝑥 .𝑓𝑣 (𝑓 ), _) ∗ 𝑥 .𝑓𝑣 (𝑓 ) = 𝑣
   We proved in Isabelle/HOL that the instantiation of our generalized framework for immutable data
satisfies all requirements and is, thus, guaranteed to be sound. This instantiation also demonstrates
that our generalized framework is sufficiently expressive to handle complex, but common state
encodings such as translating duplicable resources to non-duplicable fractional resources.

4.5      Additional Encodings Inspired by Real-World Front-Ends
Beyond the three instantiations formalized above, we believe that our framework can capture many
other front-ends. To illustrate this point, we outline three further state encodings, inspired by
real-world front-ends, that also fit our framework:
   The Pancake verifier’s state model [60]: The front-end heap is a fixed-size array of cells, encoded
into a Viper sequence heap of references, where the cell at offset i corresponds to the heap location
heap[i] refers to. It uses the same fractional permission model as Viper.
   The block-offset memory model for C, adapted from Leroy [30]: C memory is modeled as an
unbounded but finite set of blocks, each with a unique identifier, a linear array of cells (with binary
permissions) indexed by their offset, and a fixed size. The encoding maps each cell (identified by its
block and offset) to a unique heap location storing its value in a val field, and each block to a heap
location whose size field stores the block’s size.
   The object-oriented memory model from Lööw et al. [32]: The front-end heap consists of an
unbounded but finite set of objects, each with a unique identifier, a list of cells (with binary
permissions) named by field, and a domain (the set of its field names). The encoding maps each
object to a unique heap location, each cell to the field of that location with the same name, and
stores the object’s domain in an additional field.
   In all three instantiations, the homomorphism requirement holds: Two heaps in the Pancake
state model must agree on the array size and the content of each cell, allowing the combination of
the encodings; the permissions are simply added for each cell. In the other two models, two states
with the same identifier must agree on their shared contents and have disjoint domains on the
non-duplicable contents, so their encodings combine: two C blocks must agree on their size and
two objects on their domain; blocks or objects from two states must own disjoint cells. Backward
satisfiability of the input assertions (e.g., fractional ownership of a cell, or a block’s size) is likewise
straightforward.

4.6      Identifying Unsoundness in Real-World Front-End Translations
In addition to proving existing front-ends sound, our framework captures common sources of
unsoundness in existing verifiers: the root causes of several previously-reported soundness bugs
correspond to violations of our requirements, showing that checking these requirements could
have caught them. For example, issues #1189 [47] and #1518 [48] in Prusti [1] are caused by passing
the same shared reference as two arguments to a method call, which creates two independent
fractional permissions in the IVL, whereas the front-end state model forbids such a split, which thus
violates the homomorphism requirement in Req. 1. Violations of Req. 2 underlie issue #955 [53]
Sound State Encodings in Translational Separation Logic Verifiers (Extended Version)               330:25


(an unsound quantifier-simplification rewrite) in VerCors [4], issue #1501 [49] (wrong encoding of
matches! inside assertions) in Prusti, and issue #281 [50] (unsound bool/object round-trip cast)
in Nagini [14]. Violations of requirements in Appendix A underlie further bugs: soundness of the
front-end SL rules is violated by issue #703 [52] (an unreachable send is treated as transferring
permission) in VerCors, injectivity of value translation by issue #1357 [54] (int and short are both
mapped to the same IVL type) in VerCors, and soundness of the statement translation by issue
#161 [51] (static field updates are not propagated) in Nagini.

5   Related Work
Our work was inspired by Dardinier et al. [11]’s framework for proving the soundness of SL-
based translational verifiers. However, their framework requires the front-end and the IVL to have
the same state model, which is not the case in existing translational SL-verifiers, such as Gobra,
Nagini [14], a Pancake verifier [60], Prusti, and VeriFast. In contrast, our framework supports
complex state encodings, both in terms of the representation of values and of SL resources.
   Several existing works target the soundness of front-end translations. For instance, Summers and
Müller [46] and Wolf et al. [59] sketch soundness proofs for the Viper translations of the RSL weak
memory logic [56] and the TaDA logic [9], respectively. Both involve non-standard SL resources,
for which our framework provides a formal foundation.
   Instead of translating state models to the IVL, Gillian uses an IVL and verification back-end
that are parametric in the state model. This simplifies front-end soundness proofs but requires
the back-end to be sound for all instantiations. Lööw et al. [32] present a framework for such
proofs in Rocq, which is parametric in the concrete and symbolic state models, with sufficient
conditions for a sound instantiation. However, unlike our work, it includes no statement or assertion
translations and supports neither loops nor concurrency, so it is unclear whether it can capture
realistic front-end translations. Moreover, it does not facilitate soundness proofs for IVLs that are
not parametric in the state model, such as Raven, VeriFast, and Viper.
   Front-end translations to IVLs not based on SL [57, 3, 20, 16, 37] involves generally much simpler
state encodings. In fact, the existing unsound encodings from §2.2 and §2.5 as well as our sufficient
soundness conditions are all concerned with the representation of SL resources.
   Some existing approaches target the soundness of SL-based verification back-ends. Parthasarathy
et al. [37] present a technique for automatically producing certificates for successful verification runs
in Viper. Zimmerman et al. [61] present a formalization of a variant of Viper’s symbolic execution
back-end for gradual verification. Jacobs et al. [23] formalize and prove sound a simplified version
of the symbolic execution back-end of VeriFast [22] in Rocq. These back-end soundness proofs can
be combined with our framework’s front-end proofs for an overall soundness guarantee.

6   Conclusion and Future Work
We presented the first framework, formalized in Isabelle/HOL, for proving the soundness of the
front-ends of translational separation logic verifiers with complex state encodings, which are
pervasive in existing verifiers. Our sufficient soundness conditions greatly simplify soundness
proofs and help uncover flawed encodings quickly, as we illustrate on several common encodings.
   As future work, we plan to extend the framework to support additional concurrency primitives
(e.g., threads and locks) and to apply the framework to prove soundness of existing front-ends.

Data Availability Statement
All technical results presented in this paper have been formalized and proved in Isabelle/HOL.
The formalization is publicly available in our artifact [31]. The latest version is available at https:
//doi.org/10.5281/zenodo.21509501.
330:26                                                          Hongyi Ling, Thibault Dardinier, Ellen Arlt, and Peter Müller


References
 [1] Vytautas Astrauskas, Peter Müller, Federico Poli, and Alexander J. Summers. 2019. Leveraging Rust Types for Modular
     Specification and Verification. Proc. ACM Program. Lang. 3, OOPSLA (Oct. 2019), 147:1–147:30. doi:10.1145/3360573
 [2] Sacha-Élie Ayoun, Xavier Denis, Petar Maksimović, and Philippa Gardner. 2025. A Hybrid Approach to Semi-Automated
     Rust Verification. arXiv:2403.15122 [cs] doi:10.48550/arXiv.2403.15122
 [3] Michael Backes, Catalin Hritcu, and Thorsten Tarrach. 2011. Automatically Verifying Typing Constraints for a
     Data Processing Language. In Certified Programs and Proofs (CPP), Jean-Pierre Jouannaud and Zhong Shao (Eds.).
     doi:10.1007/978-3-642-25379-9_22
 [4] Stefan Blom, Saeed Darabi, Marieke Huisman, and Wytse Oortwijn. 2017. The VerCors Tool Set: Verification of Parallel
     and Concurrent Software. In Integrated Formal Methods, Nadia Polikarpova and Steve Schneider (Eds.). Springer
     International Publishing, Cham, 102–110. doi:10.1007/978-3-319-66845-1_7
 [5] Richard Bornat, Cristiano Calcagno, Peter O’Hearn, and Matthew Parkinson. 2005. Permission Accounting in Separation
     Logic. SIGPLAN Not. 40, 1 (Jan. 2005), 259–270. doi:10.1145/1047659.1040327
 [6] John Boyland. 2003. Checking Interference with Fractional Permissions. In Static Analysis, Radhia Cousot (Ed.).
     Springer, Berlin, Heidelberg, 55–72. doi:10.1007/3-540-44898-5_4
 [7] Joshua M. Cohen and Philip Johnson-Freyd. 2024. A Formalization of Core Why3 in Coq. Proc. ACM Program. Lang. 8,
     POPL, Article 60 (jan 2024), 30 pages. doi:10.1145/3632902
 [8] Pascal Cuoq, Florent Kirchner, Nikolai Kosmatov, Virgile Prevosto, Julien Signoles, and Boris Yakobowski. 2012.
     Frama-C – A Software Analysis Perspective. In SEFM (Lecture Notes in Computer Science, Vol. 7504). Springer, 233–247.
     doi:10.1007/978-3-642-33826-7_16
 [9] Pedro da Rocha Pinto, Thomas Dinsdale-Young, and Philippa Gardner. 2014. TaDA: A Logic for Time and Data
     Abstraction. In European Conference on Object-Oriented Programming (ECOOP) (Lecture Notes in Computer Science,
     Vol. 8586), Richard E. Jones (Ed.). Springer, 207–231. doi:10.1007/978-3-662-44202-9_9
[10] Thibault Dardinier, Peter Müller, and Alexander J. Summers. 2022. Fractional Resources in Unbounded Separation
     Logic. Proc. ACM Program. Lang. 6, OOPSLA2 (Oct. 2022), 163:1066–163:1092. doi:10.1145/3563326
[11] Thibault Dardinier, Michael Sammler, Gaurav Parthasarathy, Alexander J. Summers, and Peter Müller. 2025. Formal
     Foundations for Translational Separation Logic Verifiers. Proc. ACM Program. Lang. 9, POPL (Jan. 2025), 569–599.
     doi:10.1145/3704856
[12] Xavier Denis, Jacques-Henri Jourdan, and Claude Marché. 2022. Creusot: A Foundry for the Deductive Verification of
     Rust Programs. In ICFEM (Lecture Notes in Computer Science, Vol. 13478). Springer, 90–105. doi:10.1007/978-3-031-
     17244-1_6
[13] Thomas Dinsdale-Young, Mike Dodds, Philippa Gardner, Matthew J. Parkinson, and Viktor Vafeiadis. 2010. Concurrent
     Abstract Predicates. In ECOOP 2010 – Object-Oriented Programming, Theo D’Hondt (Ed.). Springer, Berlin, Heidelberg,
     504–528. doi:10.1007/978-3-642-14107-2_24
[14] Marco Eilers and Peter Müller. 2018. Nagini: A Static Verifier for Python. In Computer Aided Verification, Hana Chockler
     and Georg Weissenbacher (Eds.). Springer International Publishing, Cham, 596–603. doi:10.1007/978-3-319-96145-3_33
[15] Jean-Christophe Filliâtre and Andrei Paskevich. 2013. Why3 - Where Programs Meet Provers. In ESOP (Lecture Notes
     in Computer Science, Vol. 7792). Springer, 125–128. doi:10.1007/978-3-642-37036-6_8
[16] Jean Fortin. 2013. BSP-Why, un outil pour la vérification déductive de programmes BSP : machine-checked semantics and
     application to distributed state-space algorithms. (BSP-Why, a tool for deductive verification of BSP programs : sémantiques
     mécanisées et application aux algorithmes d’espace d’états distribués). Ph. D. Dissertation. University of Paris-Est, France.
     https://tel.archives-ouvertes.fr/tel-00974977
[17] José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner. 2020. Gillian, part i: a multi-language
     platform for symbolic execution. In Proceedings of the 41st ACM SIGPLAN Conference on Programming Language Design
     and Implementation. 927–942. doi:10.1145/3385412.3386014
[18] Alexey Gotsman, Josh Berdine, Byron Cook, Noam Rinetzky, and Mooly Sagiv. 2007. Local reasoning for storable
     locks and threads. In Asian Symposium on Programming Languages And Systems. Springer, 19–37. doi:10.1007/978-3-
     540-76637-7_3
[19] Ekanshdeep Gupta, Nisarg Patel, and Thomas Wies. 2025. Raven: An SMT-Based Concurrency Verifier. In Computer
     Aided Verification - 37th International Conference, CAV 2025, Zagreb, Croatia, July 23-25, 2025, Proceedings, Part I
     (Lecture Notes in Computer Science, Vol. 15931), Ruzica Piskac and Zvonimir Rakamaric (Eds.). Springer, 81–106.
     doi:10.1007/978-3-031-98668-0_4
[20] Paolo Herms. 2013. Certification of a Tool Chain for Deductive Program Verification. (Certification d’une chaine de
     vérification déductive de programmes). Ph. D. Dissertation. University of Paris-Sud, Orsay, France. https://tel.archives-
     ouvertes.fr/tel-00789543
Sound State Encodings in Translational Separation Logic Verifiers (Extended Version)                                330:27


[21] Bart Jacobs, Dragan Bosnacki, and Ruurd Kuiper. 2015. Modular Termination Verification. In 29th European Conference
     on Object-Oriented Programming (ECOOP 2015) (Leibniz International Proceedings in Informatics (LIPIcs), Vol. 37),
     John Tang Boyland (Ed.). Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl, Germany, 664–688. doi:10.
     4230/LIPIcs.ECOOP.2015.664
[22] Bart Jacobs, Jan Smans, Pieter Philippaerts, Frédéric Vogels, Willem Penninckx, and Frank Piessens. 2011. VeriFast: A
     Powerful, Sound, Predictable, Fast Verifier for C and Java. In NASA Formal Methods (NFM) (Lecture Notes in Computer
     Science, Vol. 6617), Mihaela Gheorghiu Bobaru, Klaus Havelund, Gerard J. Holzmann, and Rajeev Joshi (Eds.). Springer,
     41–55. doi:10.1007/978-3-642-20398-5_4
[23] Bart Jacobs, Frédéric Vogels, and Frank Piessens. 2015. Featherweight VeriFast. Logical Methods in Computer Science
     Volume 11, Issue 3 (Sept. 2015). doi:10.2168/LMCS-11(3:19)2015
[24] Ralf Jung, David Swasey, Filip Sieczkowski, Kasper Svendsen, Aaron Turon, Lars Birkedal, and Derek Dreyer. 2015.
     Iris: Monoids and Invariants as an Orthogonal Basis for Concurrent Reasoning. In Proceedings of the 42nd Annual
     ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL ’15). Association for Computing
     Machinery, New York, NY, USA, 637–650. doi:10.1145/2676726.2676980
[25] Bernhard Kragl and Shaz Qadeer. 2021. The Civl Verifier. In #PLACEHOLDER_PARENT_METADATA_VALUE#. TU
     Wien Academic Press, 143–152. doi:10.34727/2021/isbn.978-3-85448-046-4_23
[26] Robbert Krebbers and Freek Wiedijk. 2013. Separation logic for non-local control flow and block scope variables.
     In International Conference on Foundations of Software Science and Computational Structures. Springer, 257–272.
     doi:10.1007/978-3-642-37075-5_17
[27] K. Rustan M. Leino. 2008. This Is Boogie 2. (June 2008). Available from https://www.microsoft.com/en-us/research/wp-
     content/uploads/2016/12/krml178.pdf.
[28] K. Rustan M. Leino. 2010. Dafny: An Automatic Program Verifier for Functional Correctness. In Logic for Programming,
     Artificial Intelligence, and Reasoning, Edmund M. Clarke and Andrei Voronkov (Eds.). Springer, Berlin, Heidelberg,
     348–370. doi:10.1007/978-3-642-17511-4_20
[29] K. Rustan M. Leino and Peter Müller. 2009. A Basis for Verifying Multi-threaded Programs. In Programming Languages
     and Systems, Giuseppe Castagna (Ed.). Springer, Berlin, Heidelberg, 378–393. doi:10.1007/978-3-642-00590-9_27
[30] Xavier Leroy. 2009. Formal Verification of a Realistic Compiler. Commun. ACM 52, 7 (2009), 107–115. doi:10.1145/
     1538788.1538814
[31] Hongyi Ling, Thibault Dardinier, Ellen Arlt, and Peter Müller. 2026. Sound State Encodings in Translational Separation
     Logic Verifiers (Artifact). doi:10.5281/zenodo.21509502
[32] Andreas Lööw, Seung Hoon Park, Daniele Nantes-Sobrinho, Sacha-Élie Ayoun, Opale Sjöstedt, and Philippa Gardner.
     2025. Compositional Symbolic Execution for the Next 700 Memory Models. Proceedings of the ACM on Programming
     Languages 9, OOPSLA2 (2025), 2815–2842. doi:10.1145/3763151
[33] Petar Maksimović, Sacha-Élie Ayoun, José Fragoso Santos, and Philippa Gardner. 2021. Gillian, Part II: Real-World
     Verification for JavaScript and C. In Computer Aided Verification, Alexandra Silva and K. Rustan M. Leino (Eds.).
     Springer International Publishing, Cham, 827–850. doi:10.1007/978-3-030-81688-9_38
[34] Peter Müller, Malte Schwerhoff, and Alexander J. Summers. 2016. Viper: A Verification Infrastructure for Permission-
     Based Reasoning. In Verification, Model Checking, and Abstract Interpretation, Barbara Jobstmann and K. Rustan M.
     Leino (Eds.). Springer, Berlin, Heidelberg, 41–62. doi:10.1007/978-3-662-49122-5_2
[35] Tobias Nipkow, Lawrence C. Paulson, and Markus Wenzel. 2002. Isabelle/HOL - A Proof Assistant for Higher-Order
     Logic. Lecture Notes in Computer Science, Vol. 2283. Springer. doi:10.1007/3-540-45949-9
[36] Peter W. O’Hearn. 2004. Resources, Concurrency and Local Reasoning. In CONCUR 2004 - Concurrency Theory, Philippa
     Gardner and Nobuko Yoshida (Eds.). Springer, Berlin, Heidelberg, 49–67. doi:10.1007/978-3-540-28644-8_4
[37] Gaurav Parthasarathy, Thibault Dardinier, Benjamin Bonneau, Peter Müller, and Alexander J. Summers. 2024. To-
     wards Trustworthy Automated Program Verifiers: Formally Validating Translations into an Intermediate Verification
     Language. Proc. ACM Program. Lang. 8, PLDI, Article 208 (jun 2024), 25 pages. doi:10.1145/3656438
[38] Gaurav Parthasarathy, Peter Müller, and Alexander J. Summers. 2021. Formally Validating a Practical Verification
     Condition Generator. In Computer Aided Verification (CAV) (LNCS, Vol. 12760), Alexandra Silva and K. Rustan M. Leino
     (Eds.). 704–727. doi:10.1007/978-3-030-81688-9_33
[39] Willem Penninckx, Bart Jacobs, and Frank Piessens. 2015. Sound, Modular and Compositional Verification of the In-
     put/Output Behavior of Programs. In Programming Languages and Systems, Jan Vitek (Ed.). Springer, Berlin, Heidelberg,
     158–182. doi:10.1007/978-3-662-46669-8_7
[40] João Pereira, Tobias Klenze, Sofia Giampietro, Markus Limbeck, Dionysios Spiliopoulos, Felix Wolf, Marco Eilers,
     Christoph Sprenger, David Basin, Peter Müller, and Adrian Perrig. 2025. Protocols to Code: Formal Verification
     of a Secure Next-Generation Internet Router. In Proceedings of the 2025 ACM SIGSAC Conference on Computer and
     Communications Security (New York, NY, USA, 2025-11-22) (CCS ’25). Association for Computing Machinery, 1469–1483.
     doi:10.1145/3719027.3765104
330:28                                                       Hongyi Ling, Thibault Dardinier, Ellen Arlt, and Peter Müller


[41] João C. Pereira, Isaac van Bakel, Patricia Firlejczyk, Marco Eilers, and Peter Müller. 2025. Modular Reasoning about
     Global Variables and Their Initialization. Proc. ACM Program. Lang. 9, OOPSLA2 (2025), 2310–2337. doi:10.1145/3763133
[42] J.C. Reynolds. 2002. Separation Logic: A Logic for Shared Mutable Data Structures. In Proceedings 17th Annual IEEE
     Symposium on Logic in Computer Science. 55–74. doi:10.1109/LICS.2002.1029817
[43] Jan Smans, Bart Jacobs, and Frank Piessens. 2012. Implicit Dynamic Frames. ACM Trans. Program. Lang. Syst. 34, 1
     (May 2012), 2:1–2:58. doi:10.1145/2160910.2160911
[44] Simon Spies, Niklas Mück, Haoyi Zeng, Michael Sammler, Andrea Lattuada, Peter Müller, and Derek Dreyer. 2025.
     Destabilizing Iris. Proc. ACM Program. Lang. 9, PLDI (2025), 848–873. doi:10.1145/3729284
[45] Christoph Sprenger, Tobias Klenze, Marco Eilers, Felix A. Wolf, Peter Müller, Martin Clochard, and David Basin. 2020.
     Igloo: soundly linking compositional refinement and separation logic for distributed system verification. Artifact for
     "Igloo: Soundly Linking Compositional Refinement and Separation Logic for Distributed System Verification" 4, OOPSLA
     (Nov. 2020), 152:1–152:31. doi:10.1145/3428220
[46] Alexander J. Summers and Peter Müller. 2020. Automating deductive verification for weak-memory programs
     (extended version). International Journal on Software Tools for Technology Transfer (STTT) 22, 6 (2020), 709–728.
     doi:10.1007/S10009-020-00559-Y
[47] GitHub user: Aurel300. 2022. Shared reference unsoundness (issue #1189). https://github.com/viperproject/prusti-
     dev/issues/1189.
[48] GitHub user: cliu369. 2024. Assert(false) passing with Shared References (issue #1518). https://github.com/viperproject/
     prusti-dev/issues/1518.
[49] GitHub user: fpoli. 2024. Wrong encoding of signed discriminants in pure code (issue #1501). https://github.com/
     viperproject/prusti-dev/issues/1501.
[50] GitHub user: gewlar. 2026. Unsound behavior when casting to object (issue #281). https://github.com/marcoeilers/
     nagini/issues/281.
[51] GitHub user: marcoeilers. 2024. Unsoundness relating to static fields (issue #161). https://github.com/marcoeilers/
     nagini/issues/161.
[52] GitHub user: pieter-bos. 2021. Send/Recv is unsound where guard checking is incomplete (issue #703). https:
     //github.com/utwente-fmt/vercors/issues/703.
[53] GitHub user: pieter-bos. 2023. SimplifyNestedQuantifiers makes an unsound rewrite (issue #955). https://github.com/
     utwente-fmt/vercors/issues/955.
[54] GitHub user: superaxander. 2025. Unsoundness due to violation of effective type rules (issue #1357). https://github.
     com/utwente-fmt/vercors/issues/1357.
[55] Viktor Vafeiadis. 2011. Concurrent Separation Logic and Operational Semantics. Electronic Notes in Theoretical
     Computer Science 276 (Sept. 2011), 335–351. doi:10.1016/j.entcs.2011.09.029
[56] Viktor Vafeiadis and Chinmay Narayan. 2013. Relaxed separation logic: a program logic for C11 concurrency. In Object
     Oriented Programming Systems Languages & Applications, (OOPSLA), Antony L. Hosking, Patrick Th. Eugster, and
     Cristina V. Lopes (Eds.). doi:10.1145/2509136.2509532
[57] Frédéric Vogels, Bart Jacobs, and Frank Piessens. 2009. A Machine Checked Soundness Proof for an Intermediate
     Verification Language. In Theory and Practice of Computer Science, Conference on Current Trends in Theory and
     Practice of Computer Science (SOFSEM) (Lecture Notes in Computer Science, Vol. 5404), Mogens Nielsen, Antonín
     Kucera, Peter Bro Miltersen, Catuscia Palamidessi, Petr Tuma, and Frank D. Valencia (Eds.). Springer, 570–581.
     doi:10.1007/978-3-540-95891-8_51
[58] Felix A. Wolf, Linard Arquint, Martin Clochard, Wytse Oortwijn, João C. Pereira, and Peter Müller. 2021. Gobra: Modular
     Specification and Verification of Go Programs. In Computer Aided Verification, Alexandra Silva and K. Rustan M. Leino
     (Eds.). Springer International Publishing, Cham, 367–379. doi:10.1007/978-3-030-81685-8_17
[59] Felix A. Wolf, Malte Schwerhoff, and Peter Müller. 2022. Concise outlines for a complex logic: a proof outline checker
     for TaDA. Formal Methods in System Design 61, 1 (2022), 110–136. doi:10.1007/S10703-023-00427-W
[60] Junming Zhao, Miki Tanaka, Johannes Åman Pohjola, Alessandro Legnani, Tiana Tsang Ung, H. Truong, Tsun Wang
     Sau, Thomas Sewell, Rob Sison, Hira Syeda, Magnus Myreen, Michael Norrish, and Gernot Heiser. 2025. Verifying
     Device Drivers with Pancake. arXiv:2501.08249 [cs.PL] https://arxiv.org/abs/2501.08249
[61] Conrad Zimmerman, Jenna DiVincenzo, and Jonathan Aldrich. 2024. Sound Gradual Verification with Symbolic
     Execution. Proc. ACM Program. Lang. 8, POPL (Jan. 2024), 85:2547–85:2576. doi:10.1145/3632927
Sound State Encodings in Translational Separation Logic Verifiers (Extended Version)                                           330:29


A     Full Definitions and Semantics in the Framework
The axioms for IDF algebra is listed in Fig. 10.

    𝑎 ⊕𝑏 =𝑏 ⊕𝑎              𝑎 ⊕ (𝑏 ⊕ 𝑐) = (𝑎 ⊕ 𝑏) ⊕ 𝑐               𝑐 =𝑎 ⊕𝑏 ∧𝑐 =𝑐 ⊕𝑐 ⇒ 𝑎 =𝑎 ⊕𝑎                         𝑥 = 𝑥 ⊕ |𝑥 |

|𝑥 | = |𝑥 | ⊕ |𝑥 |      𝑥 = 𝑥 ⊕ 𝑐 ⇒ |𝑥 | ⪰ 𝑐           |𝑎 ⊕ 𝑏 | = |𝑎| ⊕ |𝑏|          𝑎 = 𝑏 ⊕ 𝑥 ∧ 𝑎 = 𝑏 ⊕ 𝑦 ∧ |𝑥 | = |𝑦| ⇒ 𝑥 = 𝑦

 stable(𝜔) ⇒ 𝜔 = stabilize(𝜔)                 stable(stabilize(𝜔))              stabilize(𝑎 ⊕ 𝑏) = stabilize(𝑎) ⊕ stabilize(𝑏)

    𝑥 = stabilize(𝑥) ⊕ |𝑥 |              𝑎 = 𝑏 ⊕ unit(𝑐) ⇒ 𝑎 = 𝑏                𝑎 = 𝑎 ⊕ unit(𝑎)               |unit(𝑎)| = unit(𝑎)

                                                            stable(unit(𝑎))

    Fig. 10. Axioms for the IDF algebra (Σ, ⊕, |_|, stable, stabilize, unit). Define 𝜔 ′ ⪰ 𝜔 ≜ (∃𝑟 .𝜔 ′ = 𝜔 ⊕ 𝑟 ).

    The axiomatic semantic rules for IVL statements havoc 𝑥, inhale 𝐴, exhale 𝐴, 𝐶 1 ; 𝐶 2 , and
if (𝑏) {𝐶 1 } else {𝐶 2 } are listed in Fig. 11.

InhaleAx                                                      ExhaleAx
 selfFraming(𝑃 )        frames(𝐴, 𝑃 )                         selfFraming(𝑃 )         𝑃 ⊆ 𝑄 ∗𝐴            selfFraming(𝑄 )
     Δ ⊢ [𝑃 ] inhale 𝐴 [𝑃 ∗ 𝐴]                                                 Δ ⊢ [𝑃 ] exhale 𝐴 [𝑄 ]

     HavocAx                                                          SeqAx
     selfFraming(𝑃 )         Δ(𝑥 ) = 𝜏                                Δ ⊢ [𝑃 ] 𝐶 1 [𝑅 ]        Δ ⊢ [𝑅 ] 𝐶 2 [𝑄 ]
      Δ ⊢ [𝑃 ] havoc 𝑥 [ ∃𝑥 ∈ 𝜏 . 𝑃 ]                                           Δ ⊢ [𝑃 ] 𝐶 1 ; 𝐶 2 [𝑄 ]

                     IfAx
                      selfFraming(𝑃 )       frames(𝑃, 𝑏 )       Δ ⊢ [𝑃 ∗ 𝑏 ] 𝐶 1 [𝐵 1 ]     Δ ⊢ [𝑃 ∗ ¬𝑏 ] 𝐶 2 [𝐵 2 ]
                                            Δ ⊢ [𝑃 ] if (𝑏 ) {𝐶 1 } else {𝐶 2 } [𝐵 1 ∨ 𝐵 2 ]


                     Fig. 11. Axiomatic semantics for the IVL statements used in our framework.

   The extension of wf𝐴Δ𝐹 for front-end assertions is defined via an auxiliary function wf𝐴Δ𝐹 (𝐴)𝐵 ,
where 𝐵 is a boolean indicator of whether 𝐴 is in the scope of any 𝜇 binder. wf𝐴Δ𝐹 (𝐴)𝐵 is defined as
follows, where Δ𝐹 [𝑥 := 𝑡] represents the type context derived from Δ𝐹 by replacing the type of
local variable 𝑥 to 𝑡, and wf𝐴Δ𝐹 (𝐴) ≜ wf𝐴Δ𝐹 (𝐴)false .
                                               wf𝐴Δ𝐹 (𝐴𝑝 )𝐵 ≜ wf𝐴Δ𝐹 (𝐴𝑝 )
                                          wf𝐴Δ𝐹 (𝐴1 ∗ 𝐴2 )𝐵 ≜ wf𝐴Δ𝐹 (𝐴1 )𝐵 ∧ wf𝐴Δ𝐹 (𝐴2 )𝐵
                                         wf𝐴Δ𝐹 (𝐴1 ∨ 𝐴2 )𝐵 ≜ wf𝐴Δ𝐹 (𝐴1 )𝐵 ∧ wf𝐴 𝐴2 𝐵
                                         wf𝐴Δ𝐹 (∃𝑥 : 𝑡 . 𝐴)𝐵 ≜ wf𝐴Δ𝐹 [𝑥:=𝑡 ] (𝐴)𝐵
                                          wf𝐴Δ𝐹 (𝑏 ⇒ 𝐴)𝐵 ≜ wf𝐴Δ𝐹 (𝐴)𝐵
                                                 wf𝐴Δ𝐹 (𝑏)𝐵 ≜ true
                                                 wf𝐴Δ𝐹 (𝑃)𝐵 ≜ 𝐵
                                            wf𝐴Δ𝐹 (𝜇𝑃 . 𝐴)𝐵 ≜ wf𝐴Δ𝐹 (𝐴)true


  To define the extension of interpretation function 𝐼 AΔ𝐹 (·) and free variable function fvA for front-
end assertions, we first define auxiliary interpretation 𝐼 AΔ𝐹 (·) Γ parameterized by the interpretation
330:30                                                                 Hongyi Ling, Thibault Dardinier, Ellen Arlt, and Peter Müller


Γ for predicate symbol 𝑃 and auxiliary function fvA (·) 𝐹 parameterized by the free variable set 𝐹
of predicate symbol 𝑃 as follows, where 𝜔 [𝑣/𝑥] represents the resulting state of overwriting the
                                                          Ñ
value of local variable 𝑥 in 𝜔 to 𝑣, and LFP (𝜆𝑆. 𝑓 (𝑆)) ≜ 𝑆:𝑓 (𝑆 ) ⊆𝑆 𝑆 is the least fixed point of 𝑓
when it monotonely increases on 𝑆, which we prove is the case for 𝐼 AΔ𝐹 (·) Γ and fvA (𝐴) 𝐹 . Then
𝐼 AΔ𝐹 (𝐴) ≜ 𝐼 AΔ𝐹 (𝐴) ∅ and fvA (𝐴) ≜ fvA (𝐴) ∅ .

                 𝐼 AΔ𝐹 (𝐴1 ∗ 𝐴2 ) Γ ≜ {𝜔 | ∃𝜔 1 ∈ 𝐼 AΔ𝐹 (𝐴1 ) Γ , 𝜔 2 ∈ 𝐼 AΔ𝐹 (𝐴2 ) Γ . 𝜔 = 𝜔 1 ⊕ 𝜔 2 }
                𝐼 AΔ𝐹 (𝐴1 ∨ 𝐴2 ) Γ ≜ 𝐼 AΔ𝐹 (𝐴1 ) Γ ∪ 𝐼 AΔ𝐹 (𝐴2 ) Γ
                𝐼 AΔ𝐹 (∃𝑥 : 𝑡 . 𝐴) Γ ≜ {𝜔 | ∃𝑣. tp(𝑣) = 𝑡 ∧ 𝜔 [𝑣/𝑥] ∈ 𝐼 AΔ𝐹 [𝑥:=𝑡 ] (𝐴) Γ }
                    𝐼 AΔ𝐹 (𝑏 ⇒ 𝐴) Γ ≜ 𝜔 | 𝐼 B (𝑏) (𝜔) is defined ∧ 𝐼 B (𝑏) (𝜔) = true ⇒ 𝜔 ∈ 𝐼 AΔ𝐹 (𝐴) Γ
                                       n                                                               o


                        𝐼 AΔ𝐹 (𝑏) Γ ≜ {𝜔 | 𝐼 B (𝑏) (𝜔) = true}
                        𝐼 AΔ𝐹 (𝑃) Γ ≜ Γ
                   𝐼 AΔ𝐹 (𝜇𝑃 . 𝐴) Γ ≜ LFP 𝜆𝑆. 𝐼 AΔ𝐹 (𝐴)𝑆
                                                        

                 fvA (𝐴1 ∗ 𝐴2 ) 𝐹 ≜ fvA (𝐴1 ) 𝐹 ∪ fvA (𝐴2 ) 𝐹
                fvA (𝐴1 ∨ 𝐴2 ) 𝐹 ≜ fvA (𝐴1 ) 𝐹 ∪ fvA (𝐴2 ) 𝐹
                fvA (∃𝑥 : 𝑡 . 𝐴) 𝐹 ≜ fvA (𝐴) 𝐹 \{𝑥 }
                  fvA (𝑏 ⇒ 𝐴) 𝐹 ≜ fvB (𝑏) ∪ fvA (𝐴) 𝐹
                         fvA (𝑏) 𝐹 ≜ fvB (𝑏)
                        fvA (𝑃) 𝐹 ≜ 𝐹
                   fvA (𝜇𝑃 . 𝐴) 𝐹 ≜ LFP (𝜆𝑆. fvA (𝐴)𝑆 )


  In the Isabelle/HOL formalization, we use de Bruijn indices, and prove the following overapprox-
imation of fvA (𝜇𝑃 . 𝐴).
                                                                       Ø
                                                 fvA (𝜇𝑃 . 𝐴) ⊆                  {0, 1, . . . , 𝑥 }
                                                                    𝑥 ∈fvA (𝐴)

  The extension of wf𝐶 , fvC , and wr to all compositions of front-end statements is as follows.

                                      wf𝐶Δ𝐹 ( skip) ≜ true
                                      wf𝐶Δ𝐹 (𝑐 1 ; 𝑐 2 ) ≜ wf𝐶Δ𝐹 (𝑐 1 ) ∧ wf𝐶Δ𝐹 (𝑐 2 )
                  wf𝐶Δ𝐹 ( if (𝑏) {𝑐 1 } else {𝑐 2 }) ≜ wf𝐶Δ𝐹 (𝑐 1 ) ∧ wf𝐶Δ𝐹 (𝑐 2 )
                   wf𝐶Δ𝐹 ( while (𝑏) inv 𝐼 {𝑐}) ≜ wf𝐶Δ𝐹 (𝑐) ∧ selfFraming(𝐼 ) ∧ stableUnder(𝑏, 𝐼 ) ∧ wf𝐴Δ𝐹 (𝐼 )
         wf𝐶Δ𝐹 ({𝑃1 } 𝑐 1 {𝑄 1 } || {𝑃2 } 𝑐 2 {𝑄 2 }) ≜ wf𝐶Δ𝐹 (𝑐 1 ) ∧ wf𝐶Δ𝐹 (𝑐 2 ) ∧
                                                          selfFraming(𝑃1 ) ∧ selfFraming(𝑄 1 ) ∧
                                                          selfFraming(𝑃2 ) ∧ selfFraming(𝑄 2 ) ∧
                                                          wr(𝑐 1 ) ∩ (fvC (𝑐 2 ) ∪ fvA (𝑃2 ) ∪ fvA (𝑄 2 )) = ∅ ∧
                                                          wr(𝑐 2 ) ∩ (fvC (𝑐 1 ) ∪ fvA (𝑃1 ) ∪ fvA (𝑄 1 )) = ∅ ∧
                                                          wf𝐴Δ𝐹 (𝑃1 ) ∧ wf𝐴Δ𝐹 (𝑄 1 ) ∧ wf𝐴Δ𝐹 (𝑃2 ) ∧ wf𝐴Δ𝐹 (𝑄 2 )
                                          fvC ( skip) ≜ ∅
                                          fvC (𝑐 1 ; 𝑐 2 ) ≜ fvC (𝑐 1 ) ∪ fvC (𝑐 2 )
Sound State Encodings in Translational Separation Logic Verifiers (Extended Version)                                                              330:31


                   fvC ( if (𝑏) {𝑐 1 } else {𝑐 2 }) ≜ fvB (𝑏) ∪ fvC (𝑐 1 ) ∪ fvC (𝑐 2 )
                    fvC ( while (𝑏) inv 𝐼 {𝑐}) ≜ fvB (𝑏) ∪ fvC (𝑐)
         fvC ({𝑃1 } 𝑐 1 {𝑄 1 } || {𝑃2 } 𝑐 2 {𝑄 2 }) ≜ fvC (𝑐 1 ) ∪ fvC (𝑐 2 )
                                          wr( skip) ≜ ∅
                                          wr(𝑐 1 ; 𝑐 2 ) ≜ wr(𝑐 1 ) ∪ wr(𝑐 2 )
                    wr( if (𝑏) {𝑐 1 } else {𝑐 2 }) ≜ wr(𝑐 1 ) ∪ wr(𝑐 2 )
                     wr( while (𝑏) inv 𝐼 {𝑐}) ≜ wr(𝑐)
          wr({𝑃1 } 𝑐 1 {𝑄 1 } || {𝑃2 } 𝑐 2 {𝑄 2 }) ≜ wr(𝑐 1 ) ∪ wr(𝑐 2 )
  The small-step operational semantic reduction rules and CSL rules for all the control structures
are shown in Fig. 12 and Fig. 13, respectively.

RedPrim                                                                                                  RedSeq
        𝑐
     𝜎 →Δ𝐹 𝜎 ′                                   RedSeqSkip                                                 ⟨𝑐 1 , 𝜎 ⟩ →Δ𝐹 𝑐 1′ , 𝜎 ′
⟨𝑐, 𝜎 ⟩ →Δ𝐹 ⟨ skip, 𝜎 ′ ⟩                        ⟨ skip; 𝑐, 𝜎 ⟩ →Δ𝐹 ⟨𝑐, 𝜎 ⟩                               ⟨𝑐 1 ; 𝑐 2 , 𝜎 ⟩ →Δ𝐹 𝑐 1′ ; 𝑐 2 , 𝜎 ′

     RedIfT                                                                              RedIfF
          𝐼 B (𝑏 ) (embed𝑆 (𝜎 ) ) = true                                                      𝐼 B (𝑏 ) (embed𝑆 (𝜎 ) ) = false
     ⟨ if (𝑏 ) {𝑐 1 } else {𝑐 2 }, 𝜎 ⟩ →Δ𝐹 ⟨𝑐 1 , 𝜎 ⟩                                    ⟨ if (𝑏 ) {𝑐 1 } else {𝑐 2 }, 𝜎 ⟩ →Δ𝐹 ⟨𝑐 2 , 𝜎 ⟩

        RedLoop
        ⟨ while (𝑏 ) inv 𝐼 {𝑐 }, 𝜎 ⟩ →Δ𝐹 ⟨ if (𝑏 ) {𝑐; while (𝑏 ) inv 𝐼 {𝑐 } } else { skip }, 𝜎 ⟩

                 RedParSkip
                 ⟨ {𝑃 1 } skip {𝑄 1 } | | {𝑃 2 } skip {𝑄 2 } , 𝜎 ⟩ →Δ𝐹 ⟨ skip, 𝜎 ⟩

         RedParL
                                             ⟨𝑐 1 , 𝜎 ⟩ →Δ𝐹 𝑐 1′ , 𝜎 ′
         ⟨ {𝑃 1 } 𝑐 1 {𝑄 1 } | | {𝑃 2 } 𝑐 2 {𝑄 2 } , 𝜎 ⟩ →Δ𝐹   {𝑃 1 } 𝑐 1′ {𝑄 1 } | | {𝑃 2 } 𝑐 2 {𝑄 2 } , 𝜎 ′

                     RedParR
                                                          ⟨𝑐 2 , 𝜎 ⟩ →Δ𝐹 𝑐 2′ , 𝜎 ′
                     ⟨ {𝑃 1 } 𝑐 1 {𝑄 1 } | | {𝑃 2 } 𝑐 2 {𝑄 2 } , 𝜎 ⟩ →Δ𝐹    {𝑃 1 } 𝑐 1 {𝑄 1 } | | {𝑃 2 } 𝑐 2′ {𝑄 2 } , 𝜎 ′


Fig. 12. Small-step operational semantic reduction rules of the form ⟨𝑐, 𝜎⟩ →Δ𝐹 ⟨𝑐 ′, 𝜎 ′ ⟩ for front-end state-
ments, where 𝑐 and 𝑐 ′ are statements, 𝜎 and 𝜎 ′ are program states, Δ𝐹 is a front-end type context.

    The full definition of J·KA is shown in Fig. 14.
    The full definition of J·KC is as follows, where 𝐶𝑝 ∈ 𝐶 𝐹 𝑝 is a front-end primitive statement,
and havoc 𝑉 is a shorthand for havoc 𝑥 1 ; · · · ; havoc 𝑥𝑛 for finite set 𝑉 = {𝑥 1, . . . , 𝑥𝑛 }. Here we
assume that the IVL supports (1) disjunction and negation of pure boolean expressions, and (2)
directly using pure boolean
                              expressions as assertions. It can therefore construct assertions including
J𝐼 KA ∗ J𝑏KB ∨ ¬ J𝑏KB as in the translation of front-end loops.

                              JskipKC ≜ ( skip, ∅)
                                q y           q y           
                                  𝐶𝑝 C ≜ 𝐶𝑝 Cp , ∅
                                                                                           
                              J𝑐 1 ; 𝑐 2 KC ≜ J𝑐 1 Kmain
                                                    C    ; J𝑐 2 Kmain
                                                                 C    , J𝑐 1 Kext       ext
                                                                              C ∪ J𝑐 2 KC
                                                                                                                    
           Jif (𝑏 ) {𝑐 1 } else {𝑐 2 }KC ≜ if (J𝑏KB ) {J𝑐 1 Kmain  C     } else {J𝑐 2 Kmain
                                                                                        C     }, J𝑐 1 Kext       ext
                                                                                                       C ∪ J𝑐 2 KC
                                                                                   
            Jwhile (𝑏 ) inv 𝐼 {𝑐 }KC ≜ exhale J𝐼 KA ∗ J𝑏KB ∨ ¬ J𝑏KB ; havoc wr(𝑐 ); inhale J𝐼 KA ∗ ¬ J𝑏KB ,
330:32                                                                   Hongyi Ling, Thibault Dardinier, Ellen Arlt, and Peter Müller


 RuleSkip                                            RulePrim
    selfFraming(𝑃 )                                  selfFraming(𝑃 )           selfFraming(𝑄 )        Δ𝐹 ⊢𝑝 {𝑃 } 𝑐 {𝑄 }
 Δ𝐹 ⊢CSL {𝑃 } skip {𝑃 }                                                        Δ𝐹 ⊢CSL {𝑃 } 𝑐 {𝑄 }

                      RuleSeq
                      Δ𝐹 ⊢CSL {𝑃 } 𝑐 1 {𝑅 }           Δ𝐹 ⊢CSL {𝑅 } 𝑐 2 {𝑄 }
                                    Δ𝐹 ⊢CSL {𝑃 } 𝑐 1 ; 𝑐 2 {𝑄 }

             RuleIf
             frames(𝐴, 𝑏 )       Δ𝐹 ⊢CSL {𝐴 ∩ 𝑏 } 𝑐 1 {𝐵 1 }         Δ𝐹 ⊢CSL {𝐴 ∩ ¬𝑏 } 𝑐 2 {𝐵 2 }
                             Δ𝐹 ⊢CSL {𝐴} if (𝑏 ) {𝑐 1 } else {𝑐 2 } {𝐵 1 ∪ 𝐵 2 }

                RuleWhile
                frames(𝑃, 𝑏 )        stableUnder(𝑏, 𝑃 )           Δ𝐹 ⊢CSL {𝑃 ∩ 𝑏 } 𝑐 {𝑃 }
                             Δ𝐹 ⊢CSL {𝑃 } while (𝑏 ) inv 𝐼 {𝑐 } {𝑃 ∩ ¬𝑏 }

 RulePar
 Δ𝐹 ⊢CSL {𝑃1 } 𝑐 1 {𝑄 1 }    Δ𝐹 ⊢CSL {𝑃2 } 𝑐 2 {𝑄 2 }             fvC (𝑐 1 ) ∩ wr(𝑐 2 ) = ∅   fvC (𝑐 2 ) ∩ wr(𝑐 1 ) = ∅
    ∀𝑥 ∈ wr(𝑐 1 ). 𝑃1 and 𝑄 1 are independent of 𝑥                ∀𝑥 ∈ wr(𝑐 2 ). 𝑃2 and 𝑄 2 are independent of 𝑥
                        Δ𝐹 ⊢CSL {𝑃1 ∗ 𝑃 2 } {𝐴1 } 𝑐 1 {𝐵 1 } | | {𝐴2 } 𝑐 2 {𝐵 2 } {𝑄 1 ∗ 𝑄 2 }

           RuleFrame
           Δ𝐹 ⊢CSL {𝑃 } 𝑐 {𝑄 }        selfFraming(𝑅)            ∀𝑥 ∈ wr(𝑐 ). 𝑅 is independent of 𝑥
                                        Δ𝐹 ⊢CSL {𝑃 ∗ 𝑅 } 𝑐 {𝑄 ∗ 𝑅 }

         RuleConseq
         Δ𝐹 ⊢CSL {𝑃 } 𝑐 {𝑄 }       𝑃′ ⊆ 𝑃          𝑄 ⊆ 𝑄′         selfFraming(𝑃 ′ )         selfFraming(𝑄 ′ )
                                             Δ𝐹 ⊢CSL {𝑃 } 𝑐 {𝑄 }
                                                            ′        ′



Fig. 13. CSL rules of the form Δ𝐹 ⊢CSL {𝑃 } 𝑐 {𝑄 } for front-end statements, where Δ𝐹 is a front-end type
context, 𝑐 is a statement, 𝑃 and 𝑄 are semantic assertions (i.e., sets of front-end ghost states). The separating
conjunction 𝑃 ∗𝑄 of semantic assertions 𝑃 and 𝑄 is defined as {𝜔 | ∃𝜔 1 ∈ 𝑃, 𝜔 2 ∈ 𝑄. 𝜔 = 𝜔 1 ⊕ 𝜔 2 }. A semantic
assertion 𝑃 is independent of a local variable 𝑥 iff: ∀𝜔, 𝑣. 𝜔 ∈ 𝑃 ⇔ 𝜔 [𝑣/𝑥] ∈ 𝑃.

                   q y    q y
                    𝐴𝑝 A ≜ 𝐴𝑝 Ap                                              J𝑏KA ≜ J𝑏KB
               J𝐴1 ∗ 𝐴2 KA ≜ J𝐴1 KA ∗ J𝐴2 KA                        J𝐴1 ∨ 𝐴2 KA ≜ J𝐴1 KA ∨ J𝐴2 KA
                J𝑏 ⇒ 𝐴KA ≜ J𝑏KB ⇒ J𝐴KA                              J∃𝑥 : 𝑡 . 𝐴KA ≜ ∃𝑥 : J𝑡KT . typeInv(𝑡, 𝑥) ∗ J𝐴KA
                     J𝑃KA ≜ 𝑃                                            J𝜇𝑃 . 𝐴KA ≜ 𝜇𝑃 . J𝐴KA


  Fig. 14. Extending the input assertion translation J·KAp to a translation J·KA of all front-end assertions.

                                             n                                                                        o              
                                                                              main
                                                 inhale J𝐼 KA ∗ J𝑏KA ; J𝑐KC          ; exhale J𝐼 KA ∗ J𝑏KB ∨ ¬ J𝑏KB        ∪ J𝑐Kext
                                                                                                                                C
                                                
  J{𝑃 1 } 𝑐 1 {𝑄 1 } | | {𝑃 2 } 𝑐 2 {𝑄 2 }KC ≜ exhale J𝑃 1 ∗ 𝑃 2 KA ; havoc wr(𝑐 1 ) ∪ wr(𝑐 2 ); inhale J𝑄 1 ∗ 𝑄 2 KA ,
                                              n                                              o
                                                                       main
                                                inhale J𝑃 1 KA ; J𝑐 1 KC    ; exhale J𝑄 1 KA ∪
                                              n                                              o                      
                                                                       main
                                                inhale J𝑃 2 KA ; J𝑐 2 KC     ; exhale J𝑄 2 KA ∪ J𝑐 1 Kext       ext
                                                                                                      C ∪ J𝑐 2 KC

  The requirements for the input front-end components are listed in Req. 3.
Requirement 3. The following properties need to be satisfied by the input front-end components:
Sound State Encodings in Translational Separation Logic Verifiers (Extended Version)                        330:33


      • 𝐼 B is pure, i.e., ∀𝑏 ∈ 𝐵𝐸 𝐹 , 𝜔 ∈ Σ𝐹 , 𝐼 B (𝑏) (𝜔) is defined iff 𝐼 B (𝑏) (|𝜔 |) is defined, and
        𝐼 B (𝑏) (𝜔) = 𝐼 B (𝑏) (|𝜔 |) when they are both defined.
      • For any boolean expression 𝑏 ∈ 𝐵𝐸 𝐹 , fvB (𝑏) overapproximates the free variables of 𝑏, i.e., ∀𝑥 ∉
        fvB (𝑏), 𝑣 ∈ 𝑉𝐹 , 𝜔 ∈ Σ𝐹 , 𝐼 B (𝑏) (𝜔) is defined iff 𝐼 B (𝑏) (𝜔 [𝑣/𝑥]) is defined, and 𝐼 B (𝑏) (𝜔) =
        𝐼 B (𝑏) (𝜔 [𝑣/𝑥]) when they are both defined.
      • For any input assertion 𝐴𝑝 ∈ 𝐴𝐹 𝑝 , fvA (𝐴𝑝 ) overapproximates the free variables of 𝐴𝑝 , i.e.,
        ∀𝑥 ∉ fvA (𝐴𝑝 ), 𝜔 ∈ Σ𝐹 , 𝑣 ∈ 𝑉𝐹 , 𝜔 ∈ 𝐼 AΔ𝐹 𝐴𝑝 iff 𝜔 [𝑣/𝑥] ∈ 𝐼 AΔ𝐹 𝐴𝑝 .
                                                                                
      • The written variables of well-formed primitive statements must be declared in the type context,
        i.e., for any 𝑐 ∈ 𝐶 𝐹 𝑝 , if wf𝐶Δ𝐹 (𝑐), then wr(𝑐) ⊆ dom(Δ𝐹 ).
      • The CSL rules for any well-formed primitive statement 𝐶 are affine, i.e., if Δ𝐹 ⊢CSL {𝑃 } 𝐶 {𝑄 }
        for some semantic assertions 𝑃 and 𝑄, then Δ𝐹 ⊢CSL {monotonize(𝑃)} 𝐶 {monotonize(𝑄)}.
        Here, for any semantic assertion 𝐴, monotonize(𝐴) ≜ {𝜔 | ∃𝜔 0 . 𝜔 ⪰ 𝜔 0 ∧ 𝜔 0 ∈ 𝐴} is the
        minimal semantic assertion that is monotone (a semantic assertion 𝑃 is monotone iff ∀𝜔 ∈ 𝑃
        and 𝜔 ′ ⪰ 𝜔, 𝜔 ′ ∈ 𝑃) and that subsumes 𝐴.
      • The operational semantic reduction rules of any primitive statement 𝑐 ∈ 𝐶 𝐹 𝑝 do not modify
                                                      𝑐
        local variables outside wr(𝑐), i.e., if 𝜎 →Δ𝐹 𝜎 ′ , then ∀𝑥 ∉ wr(𝑐), 𝜎 (𝑥) = 𝜎 ′ (𝑥).
      • For any primitive statement 𝑐 ∈ 𝐶 𝐹 𝑝 , any finite number of changes outside fvC (𝑐) does not
        affect the reduction of 𝑐, i.e., if two states 𝜎1, 𝜎2 agree on a set 𝑋 whose complement is finite
                                                                                          𝑐
        and that subsumes fvC (𝑐), and they have the same program heap, and 𝜎1 →Δ𝐹 𝜎1′ , then there
                                    𝑐
        exists 𝜎2′ such that 𝜎2 →Δ𝐹 𝜎2′ , and 𝜎1′ and 𝜎2′ agree on 𝑋 and the whole program heap.
      • The operational semantic reduction of any well-formed primitive statement preserves well-
                                𝑐
        typedness, i.e., if 𝜎 →Δ𝐹 𝜎 ′ for some 𝜎 that is well-typed under Δ𝐹 , then 𝜎 ′ is also well-typed
        under Δ𝐹 .
      • The precondition of each CSL rule for well-formed primitive statements guarantees progression
        for well-typed states. Specifically, if Δ𝐹 ⊢𝑝 {𝑃 } 𝑐 {𝑄 } for some primitive statement 𝑐 ∈ 𝐶 𝐹 𝑝
        and monotone semantic assertion 𝑃 ⊆ P (Σ𝐹 ), then for any program state 𝜎𝑝 ∈ Σ𝑃 that is
        well-typed w.r.t. Δ𝐹 , if embed𝑆 (𝜎𝑝 ) = 𝜎 ⊕ 𝜎 𝑓 such that 𝜎 ∈ 𝑃 and both 𝜎 and 𝜎 𝑓 are stable,
                                                       𝑐
        then there exists 𝜎𝑝′ ∈ Σ𝑃 such that 𝜎𝑝 →Δ𝐹 𝜎𝑝′ .
      • The front-end CSL rules for well-formed primitive statements are sound w.r.t. operational
        semantics: for any well-formed primitive statement, the post-state after the reduction satisfies
        the postcondition, whenever starting from a well-typed pre-state satisfying the precondition.
        Specifically, let 𝑐 ∈ 𝐶 𝐹 𝑝 be well-formed and 𝜎𝑝 be well-typed w.r.t. Δ𝐹 . If Δ𝐹 ⊢𝑝 {𝑃 } 𝑐 {𝑄 } for
        monotone semantic assertions 𝑃 and 𝑄, embed𝑆 (𝜎𝑝 ) = 𝜎 ⊕ 𝜎 𝑓 such that 𝜎 ∈ 𝑃 and both 𝜎 and
                                    𝑐
         𝜎 𝑓 are stable, and 𝜎𝑝 →Δ𝐹 𝜎𝑝′ , then there exist 𝜎 ′ and 𝜎 𝑓′ such that 𝜎 𝑓 and 𝜎 𝑓′ agree on the
         ghost heap, 𝜎 ′ is stable, embed𝑆 (𝜎𝑝′ ) = 𝜎 ′ ⊕ 𝜎 𝑓′ , and 𝜎 ′ ∈ 𝑄.

   The requirements for the translation of front-end types and values are listed in Req. 4.

Requirement 4. For the translation of front-end types and values, J·KT , J·KV , and typeInv should
satisfy the following properties:
      • J·KT translates types correctly. Specifically, if tp(𝑣) = 𝑡 for any front-end value 𝑣 and type 𝑡,
        then J𝑣KV is of type J𝑡KT .
      • J·KV is injective. Specifically, J𝑣 1 KV = J𝑣 2 KV implies 𝑣 1 = 𝑣 2 for any front-end values 𝑣 1 and 𝑣 2 .
      • typeInv correctly reflects the bijectivity of the translation of values of all types. Specifically, if
        typeInv(𝑡, 𝑥) is undefined for front-end type 𝑡 ∈ 𝑇𝐹 for all 𝑥, then    q any
                                                                                    y value 𝑣 of type J𝑡KT in the
        IVL must correspond to some front-end value 𝑣 𝑓 of type 𝑡 (i.e., 𝑣 𝑓 V = 𝑣); if typeInv(𝑡, 𝑥) = 𝑒,
330:34                                                                    Hongyi Ling, Thibault Dardinier, Ellen Arlt, and Peter Müller


        then for any IVL stateqΩ ∈ y Σ𝑉 with Ω(𝑥) = 𝑣 for 𝑣 of type J𝑡KT , 𝑒 (Ω) = true iff there exists
        𝑣 𝑓 of type 𝑡 such that 𝑣 𝑓 V = 𝑣.
      • The expressions typeInv returns are pure and monotone. Specifically, if typeInv(𝑡, 𝑥) = 𝑒, then
        for any Ω ∈ Σ𝑉 , 𝑒 (Ω) is defined iff 𝑒 (|Ω|) is defined, and 𝑒 (Ω) = 𝑒 (|Ω|) when they are both
        defined; for any Ω, Ω ′ ∈ Σ𝑉 , if 𝑒 (Ω) is defined and Ω ′ ⪰ Ω, then 𝑒 (Ω ′ ) is also defined and
        evaluates to the same value as 𝑒 (Ω) does.
    The requirement for the translation of primitive statements J·KCp is shown as Req. 5.
Requirement 5. J·KCp is sound: it preserves the semantics of any primitive statement 𝐶. Specifically,
if JΔ𝐹 KΔ ⊢ [𝑃] J𝐶KCp [𝑄] in the IVL for monotone IVL assertions 𝑃 and 𝑄, then Δ𝐹 ⊢CSL {btr(𝑃)} 𝐶
{btr(𝑄)} in the CSL of the front-end. Here, for any IVL semantic assertion 𝐴, btr(𝐴) ≜ {𝜔 | J𝜔KS ∈ 𝐴}
is the backward translation of 𝐴, i.e., a collection of all front-end states whose encoded states satisfy 𝐴.
  We prove Thm. 7 in the framework, which states the soundness of the CSL rules in Fig. 13 w.r.t.
the small-step operational semantics in Fig. 12.
Theorem 7 (Soundness of the CSL in Fig. 13). If Δ𝐹 ⊢CSL {𝑃 } 𝐶 {𝑄 } for well-formed front-end state-
ment 𝐶 and monotone 𝑃 and 𝑄, then for any well-typed stable program state 𝜎 such that embed𝑆 (𝜎) ∈ 𝑃,
executing 𝐶 from 𝜎 never aborts, and for all 𝜎 ′ that ⟨𝐶, 𝜎⟩ →∗Δ𝐹 ⟨skip, 𝜎 ′ ⟩, we have embed𝑆 (𝜎 ′ ) ∈ 𝑄.
Here ⟨·, ·⟩ →∗· ⟨·, ·⟩ is the reflexive transitive closure of ⟨·, ·⟩ →· ⟨·, ·⟩.

B     Full Definitions and Semantics of the Instantiated Front-Ends
B.1      Encoding Rational Permission Amounts into Real Permission Amounts
The interpretation of acc (𝑥 .𝑓 , 𝑝) is defined in Fig. 15.

 AccPos
                                                  𝐼 E (𝑥 ) ( (𝑠, (ℎ, 𝜋 ) ) ) = 𝑎
 𝑎 is a heap location identifier          𝐼 E (𝑝 ) = 𝑝 𝑣 > 0         𝜋 (𝑎.𝑓 ) ≥ 𝑝 𝑣        ℎ (𝑎.𝑓 ) = 𝑣     Δ𝐹 ( 𝑓 ) = tp(𝑣)
                                                               Δ
                                             (𝑠, (ℎ, 𝜋 ) ) ∈ 𝐼 A 𝐹 ( acc (𝑥 .𝑓 , 𝑝 ) )

         AccZero
         𝐼 E (𝑥 ) ( (𝑠, (ℎ, 𝜋 ) ) ) = 𝑟   𝑟 = null or 𝑟 is a heap location identifier             𝐼 E (𝑝 ) = 0    Δ𝐹 ( 𝑓 ) is defined
                                                                       Δ
                                                     (𝑠, (ℎ, 𝜋 ) ) ∈ 𝐼 A 𝐹 ( acc (𝑥 .𝑓 , 𝑝 ) )


                   Fig. 15. The interpretation of acc (𝑥 .𝑓 , 𝑝) in the rational permissioned front-end.

   Every input assertion is well-formed in this front-end, i.e., wf𝐴Δ𝐹 (𝐴𝑝 ) ≜ true for any input
assertion 𝐴𝑝 .
   We can define syntactically the type tpΔ𝐹 (𝑒) for each expression 𝑒 by an induction on the structure
of 𝑒. The definition guarantees that: for any expression 𝑒 of type tpΔ𝐹 (𝑒) = 𝑡, if it evaluates to 𝑣 at
some well-typed state 𝜔, then 𝑣 is of type 𝑡. Using this definition, the well-formedness predicate
for primitive statements is defined as follows.

                                   wf𝐶Δ𝐹 (𝑥 := 𝑒) ≜ ∃𝑡 . Δ𝐹 (𝑥) = 𝑡 ∧ tpΔ𝐹 (𝑒) = 𝑡
                                wf𝐶Δ𝐹 (𝑥 .𝑓 := 𝑒) ≜ tpΔ𝐹 (𝑥) = Ref ∧ (∃𝑡 . Δ𝐹 (𝑓 ) = 𝑡 ∧ tpΔ𝐹 (𝑒) = 𝑡)
            wf𝐶Δ𝐹 (𝑥 := alloc (𝑓1, . . . , 𝑓𝑛 )) ≜ Δ𝐹 (𝑥) = Ref ∧ 𝑓1, . . . , 𝑓𝑛 are distinct ∧ ∀𝑖. Δ𝐹 (𝑓𝑖 ) is defined
                            wf𝐶Δ𝐹 ( free (𝑥 .𝑓 )) ≜ ⊤
Sound State Encodings in Translational Separation Logic Verifiers (Extended Version)                                                    330:35


  The operational semantic reduction rules and CSL rules for the primitive statements are listed in
Fig. 16 and Fig. 17, respectively.

  RedAssignVar                                         RedFree
      𝑒 (𝜎 ) = 𝑣                                       𝜎 (𝑥 ) = 𝑎        𝑎 is a heap location identifier          𝜎 (𝑎.𝑓 ) ≠ ⊥
      𝑥 :=𝑒                                                                      free (𝑥 .𝑓 )
  𝜎 −−−→Δ𝐹 𝜎 [𝑣/𝑥 ]                                                        𝜎 −−−−−−−→Δ𝐹 𝜎 [𝑎.𝑓 := ⊥]

     RedAssignField
     𝑥 (𝜎 ) = 𝑎  𝑎 is a heap location identifier                    𝑒 (𝜎 ) = 𝑣         tp(𝑣) = Δ𝐹 ( 𝑓 )      𝜎 (𝑎.𝑓 ) ≠ ⊥
                                                      𝑥 .𝑓 :=𝑒
                                                  𝜎 −−−−→Δ𝐹 𝜎 [𝑎.𝑓 := 𝑣 ]

                RedAlloc
                ∀𝑓 . (𝑙 .𝑓 ∉ dom(𝜎 ) )           Δ𝐹 (𝑥 ) = Ref          length( 𝑣®) = 𝑛         ∀0 < 𝑖 ≤ 𝑛. tp( 𝑣® [𝑖 ] ) = Δ𝐹 ( 𝑓𝑖 )
                                        𝑥 :=alloc (𝑓1 ,...,𝑓𝑛 )
                                     𝜎 −−−−−−−−−−−−→Δ𝐹 𝜎 [𝑙/𝑥 ] [𝑙 .𝑓1 := 𝑣® [1], . . . , 𝑙 .𝑓𝑛 := 𝑣® [𝑛] ]


Fig. 16. Operational semantic reduction rules for primitive statements of the ractional permissioned front-
end. We use 𝑒 (𝜎) to represent the evaluation of 𝑒 on program state 𝜎 (whose result is the same as
𝐼 E (𝑒) (embed𝑆 (𝜎))), 𝜎 [𝑣/𝑥] to represent the state by substituting the value of local variable 𝑥 by value
𝑣 in 𝜎, and 𝜎 [𝑎.𝑓 := ⊥] or 𝜎 [𝑎.𝑓 := 𝑣] to represent the state by erasing the value at location 𝑎.𝑓 or setting the
value to 𝑣 in 𝜎, respectively.


RuleAssignVar                                                        RuleAssignField
selfFraming(𝐴)            frames(𝐴, 𝑒 )                              selfFraming(𝐴)             𝐴 ⇒ 𝑥 .𝑓 ↦→ _        frames(𝐴, 𝑒 )
    Δ𝐹 ⊢𝑝 {𝐴} 𝑥 := 𝑒 {𝐴[𝑒/𝑥 ] }                                                   Δ𝐹 ⊢𝑝 {𝐴} 𝑥 .𝑓 := 𝑒 {𝐴[𝑥 .𝑓 := 𝑒 ] }

RuleAlloc                                                                                                   RuleFree
Δ𝐹 ⊢𝑝 {⊤} 𝑥 := alloc ( 𝑓1 , . . . , 𝑓𝑛 ) { acc (𝑥 .𝑓1 , 1) ∗ · · · ∗ acc (𝑥 .𝑓𝑛 , 1) }                      Δ𝐹 ⊢𝑝 {𝑥 .𝑓 ↦→ _} free (𝑥 .𝑓 ) {⊤}


Fig. 17. CSL rules for primitive statements of the ractional permissioned front-end. Here acc (𝑥 .𝑓 , 1) represents
the typed version of 𝑥 .𝑓 ↦→ _, i.e., while 𝑥 .𝑓 ↦→ _ asserts that the current state has full permission to the
heap location 𝑥 .𝑓 , acc (𝑥 .𝑓 , 1) further requires that the value 𝜔 (𝑥 .𝑓 ) is well-typed w.r.t. the type context Δ𝐹 .
We use 𝐴[𝑒/𝑥] for the assertion {𝜔 [𝐼 E (𝑒) (𝜔)/𝑥] | 𝜔 ∈ 𝐴}, i.e., updating the value of the local variable 𝑥 to
the evaluation of 𝑒 for every state in 𝐴, and 𝐴[𝑥 .𝑓 := 𝑒] for the assertion {𝜔 [𝑎.𝑓 := 𝑣] | 𝜔 ∈ 𝐴, 𝐼 E (𝑥) (𝜔) =
𝑎 for some heap location identifier 𝑎, 𝐼 E (𝑒) (𝜔) = 𝑣 }, i.e., updating the value of the heap location 𝑥 (𝜔).𝑓 to
𝑒 (𝜔) for every 𝜔 ∈ 𝐴 that 𝑥 and 𝑒 evaluate correctly.

   The translation of all four primitive statements are listed as follows.

                                           J𝑥 := 𝑒KCp ≜ 𝑥 := 𝑒
                                        J𝑥 .𝑓 := 𝑒KCp ≜ 𝑥 .𝑓 := 𝑒
                     J𝑥 := alloc (𝑓1, . . . , 𝑓𝑛 )KCp ≜ havoc 𝑥; inhale acc (𝑥 .𝑓1, 1) ∗ · · · ∗ acc (𝑥 .𝑓𝑛 , 1)
                                     Jfree (𝑥 .𝑓 )KCp ≜ exhale acc (𝑥 .𝑓 , 1)

   A sound fragment of magic wands. The interpretation of 𝐿 −∗ 𝑅 is defined as follows:
 𝐼 AΔ𝐹 (𝐿 −∗ 𝑅) ≜      𝜔 | ∀𝜔 𝐿 ∈ 𝐼 AΔ𝐹 (𝐿) . 𝜔 𝐿 is well-typed w.r.t. Δ𝐹 and compatible with 𝜔 ⇒ 𝜔 𝐿 ⊕ 𝜔 ∈ 𝐼 AΔ𝐹 (𝑅)
                      n                                                                                               o



  Well-formedness of 𝐿 −∗ 𝑅 is defined as wf𝐴Δ𝐹 (𝐿 −∗ 𝑅) ≜ noRatAccΔ𝐹 (𝐿) ∧ noRatAccΔ𝐹 (𝑅), where
noRatAccΔ𝐹 (𝐴𝑏 ) if and only if 𝐴𝑏 does not access rational fields. Its concrete definition is given in
330:36                                                                       Hongyi Ling, Thibault Dardinier, Ellen Arlt, and Peter Müller


Fig. 18, where noRatAcc𝐸Δ𝐹 (𝑒) of an expression 𝑒 holds if and only if the type of any field name 𝑓
in 𝑒 is not Rat in Δ𝐹 .

                               noRatAccΔ𝐹 ( acc (𝑥 .𝑓 , 1)) ≜ noRatAcc𝐸Δ𝐹 (𝑥)
                                             noRatAccΔ𝐹 (𝑒) ≜ noRatAcc𝐸Δ𝐹 (𝑒)
                                    noRatAccΔ𝐹 (𝐴1 ∗ 𝐴2 ) ≜ noRatAccΔ𝐹 (𝐴1 ) ∧ noRatAccΔ𝐹 (𝐴2 )
                                    noRatAccΔ𝐹 (𝐴1 ∨ 𝐴2 ) ≜ noRatAccΔ𝐹 (𝐴1 ) ∧ noRatAccΔ𝐹 (𝐴2 )
                                      noRatAccΔ𝐹 (𝑒 ⇒ 𝐴) ≜ noRatAcc𝐸Δ𝐹 (𝑒) ∧ noRatAccΔ𝐹 (𝐴)
                                   noRatAccΔ𝐹 (∃𝑥 : 𝑡 . 𝐴) ≜ noRatAccΔ𝐹 (𝐴)


                                                    Fig. 18. Definition of noRatAccΔ𝐹 .


B.2      Encoding Lazy Field Creation
𝐼 AΔ𝐹 for the three input assertions is shown in Fig. 19. Every input assertion is well-formed in this
front-end, i.e., wf𝐴Δ𝐹 (𝐴𝑝 ) ≜ true for any input assertion 𝐴𝑝 .

 DFCAcc
                                𝐼 E (𝑥 ) ( (𝑠, (ℎ, 𝜋 ) ) ) = 𝑎        𝑎 is a heap location identifier
 𝐼 E (𝑝 ) ( (𝑠, (ℎ, 𝜋 ) ) ) = 𝑝 𝑣 > 0         𝜋 (𝑎.𝑓 ) ≥ 𝑝 𝑣          ℎ (𝑎.𝑓 ) = nofield ∨ (ℎ (𝑎.𝑓 ) = 𝑣 ∧ Δ𝐹 ( 𝑓 ) = tp(𝑣) )
                                                          Δ
                                                      𝐼 A 𝐹 ( acc (𝑥 .𝑓 , 𝑝 ) ) = 1

          DFCAdded
          𝐼 E (𝑥 ) ( (𝑠, (ℎ, 𝜋 ) ) ) = 𝑎      𝑎 is a heap location identifier            ℎ (𝑎.𝑓 ) = 𝑣 ≠ nofield
                                                    Δ
                                                  𝐼 A 𝐹 ( added (𝑥 .𝑓 ) ) = 1

                         DFCMissing
                         𝐼 E (𝑥 ) ( (𝑠, (ℎ, 𝜋 ) ) ) = 𝑎       𝑎 is a heap location identifier         ℎ (𝑎.𝑓 ) = nofield
                                                                Δ
                                                              𝐼 A 𝐹 ( missing (𝑥 .𝑓 ) ) = 1


         Fig. 19. The assertion interpretation 𝐼 AΔ𝐹 for input assertions of the lazy field creation front-end.

   The operational semantic reduction rule for allocations is shown in Fig. 20.

                                              RedAlloc
                                                  ∀𝑓 .(𝑙, 𝑓 ) ∉ dom(𝜔 )               Δ𝐹 (𝑥 ) = Ref
                                                  𝑥 :=alloc (𝑓1 ,...,𝑓𝑛 )
                                              𝜔 −−−−−−−−−−−−→Δ𝐹 𝜔 [𝑙/𝑥 ] [𝑙 .𝑓𝑖 := nofield ]


Fig. 20. The operational semantic reduction rule for 𝑥 := alloc (𝑓1, . . . , 𝑓𝑛 ) in the lazy field creation front-end.

   The translation of input assertions is defined as follows:

         Jacc (𝑥 .𝑓 , 𝑝)KAp ≜ J𝑝KE > 0 ∗ acc (J𝑥KE .𝑓added , J𝑝KE ) ∗ (J𝑥KE .𝑓added = true ⇒ acc (J𝑥KE .𝑓IVL, J𝑝KE ))
         Jadded (𝑥 .𝑓 )KAp ≜ J𝑥KE .𝑓added = true
    Jmissing (𝑥 .𝑓 )KAp ≜ J𝑥KE .𝑓added = false
Sound State Encodings in Translational Separation Logic Verifiers (Extended Version)                                               330:37


   The translation of primitive statements is defined as follows.

                          J𝑥 := 𝑒KCp ≜ 𝑥 := J𝑒KE
      J𝑥 := alloc (𝑓1, . . . , 𝑓𝑛 )KCp ≜ havoc 𝑥; inhale Jacc (𝑥 .𝑓1, 1)KA ∗ · · · ∗ Jacc (𝑥 .𝑓𝑛 , 1)KA
                     Jfree (𝑥)𝑓 KCp ≜ exhale Jacc (𝑥 .𝑓 , 1)KA
                       J𝑥 .𝑓 := 𝑣KCp ≜ if (J𝑥KE .𝑓added = false) {inhale acc (J𝑥KE .𝑓IVL, 1)} else {skip};
                                           J𝑥KE .𝑓added := true; J𝑥KE .𝑓IVL := 𝑣

B.3    Encoding Immutable Heaps
The interpretation function 𝐼 AΔ𝐹 on input assertion init (𝑥 ◦ 𝑓 ) is shown in Fig. 21. Every input
assertion is well-formed in this front-end, i.e., wf𝐴Δ𝐹 (𝐴𝑝 ) ≜ true for any input assertion 𝐴𝑝 .

         ImInit
         𝐼 E (𝑥 ) (𝑠, (ℎ, 𝜋, ℎ𝑖𝑚 ) ) = 𝑎     𝑎 is a heap location identifier           ℎ𝑖𝑚 (𝑎 ◦ 𝑓 ) = 𝑣         tp(𝑣) = Δ𝑖𝑚
                                                                                                                         𝐹 (𝑓 )
                                                                      Δ
                                               (𝑠, (ℎ, 𝜋, ℎ𝑖𝑚 ) ) ∈ 𝐼 A 𝐹 ( init (𝑥 ◦ 𝑓 ) )


Fig. 21. The interpretation of init (𝑥 ◦ 𝑓 ) in the immutable heap front-end. We allow the regular heap and the
immutable heap to have different type contexts, and use Δ𝑖𝑚    𝐹 to denote the type context of the immutable
heap.

   The free variable set, written variable set, and well-formedness predicate for 𝑥 := immalloc (𝑓 :=
𝑣) are naturally defined as follows.

                     fvC (𝑥 := immalloc (𝑓 := 𝑣)) ≜ {𝑥, 𝑣 }
                     wr(𝑥 := immalloc (𝑓 := 𝑣)) ≜ {𝑥 }
                  wf𝐶Δ𝐹 (𝑥 := immalloc (𝑓 := 𝑣)) ≜ 𝑥 ≠ 𝑣 ∧ Δ𝐹 (𝑥) = Ref ∧ Δ𝐹 (𝑣) = Δ𝐹 (𝑓 ) ≠ ⊥
  The CSL rule and operational semantic reduction rule for 𝑥 := immalloc (𝑓 := 𝑣) are shown in
Fig. 22.

                                                                                RedInit
                                                                                ∀𝑓 . 𝜔 (𝑙 ◦ 𝑓 ) = ⊥       Δ𝐹 (𝑥 ) = Ref      𝜔 (𝑣) = 𝑣0
 RuleInit
                                                                                         𝑥 :=immalloc (𝑓 :=𝑣)
 Δ𝐹 ⊢CSL {⊤} 𝑥 := immalloc ( 𝑓 := 𝑣) {𝑥 ◦ 𝑓 = 𝑣 }                                    𝜔 −−−−−−−−−−−−−→Δ𝐹 𝜔 [𝑙/𝑥 ] [𝑙 ◦ 𝑓 := 𝑣0 ]


Fig. 22. The CSL rule and operational semantic reduction rule for the primitive statement 𝑥 := immalloc (𝑓 :=
𝑣) in the immutable heap front-end.

   The translation of primitive statements is listed as follows.

                                  J𝑥 := 𝑒KCp ≜ 𝑥 := J𝑒KE
                               J𝑥 .𝑓 := 𝑒KCp ≜ J𝑥KE .𝑓ℎ (𝑓 ) := J𝑒KE
             J𝑥 := alloc (𝑓1, . . . , 𝑓𝑛 )KCp ≜ havoc 𝑥; inhale acc (𝑥 .𝑓ℎ (𝑓1 ), 1) ∗ · · · ∗ acc (𝑥 .𝑓ℎ (𝑓𝑛 ), 1)
                            Jfree (𝑥 .𝑓 )KCp ≜ exhale acc (𝑥 .𝑓ℎ (𝑓 ), 1)
            J𝑥 := immalloc (𝑓 := 𝑣)KCp ≜ havoc 𝑥; inhale acc (𝑥 .𝑓𝑣 (𝑓 ), _) ∗ 𝑥 .𝑓𝑣 (𝑓 ) = 𝑣
