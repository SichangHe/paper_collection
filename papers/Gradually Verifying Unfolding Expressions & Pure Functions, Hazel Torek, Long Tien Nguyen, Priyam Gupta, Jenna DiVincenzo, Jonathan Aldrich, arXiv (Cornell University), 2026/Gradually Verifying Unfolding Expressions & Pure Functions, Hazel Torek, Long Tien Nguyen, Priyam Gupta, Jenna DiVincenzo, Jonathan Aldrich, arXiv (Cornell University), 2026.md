                                         Gradually Verifying Unfolding Expressions & Pure Functions
                                         HAZEL TOREK, Clemson University, USA
                                         LONG TIEN NGUYEN, Carnegie Mellon University, USA
                                         PRIYAM GUPTA, ETH Zürich, Switzerland
                                         JENNA DIVINCENZO, Purdue University, USA
                                         JONATHAN ALDRICH, Carnegie Mellon University, USA
                                         Unfolding expressions, which temporarily unfold a predicate to leverage its owned fields when evaluating
                                         a heap-dependent expression, and pure functions, which are heap-dependent functions that can be used in
                                         specifications, are used in deductive program verifiers based on implicit dynamic frames, such as Gradual C0,
                                         Gobra, Nagini, and SnaKt, to increase the modularity of specifications involving ownership. In this paper, we
                                         present the formal semantics for unfolding expressions and pure functions for a static verifier using symbolic
                                         execution, extend it for a gradual verifier, and provide a proof of soundness. To support Gradual C0, our proof
                                         is in the setting of gradual verification, a deductive program verification system that combines static and
                                         dynamic verification to allow partial specifications. However, because the gradual verifier is a conservative
arXiv:2607.15383v1 [cs.PL] 16 Jul 2026




                                         extension of a static verifier, our results also apply to static verifiers that use symbolic execution, such as the
                                         Silicon symbolic execution backend for the Viper verification infrastructure used by Gobra, Nagini, and SnaKt.
                                         CCS Concepts: • Theory of computation → Logic and verification; Automated reasoning; Separation
                                         logic.
                                         Additional Key Words and Phrases: gradual verification, symbolic execution, static verification, implicit
                                         dynamic frames, soundness proof, Viper

                                         1   Introduction
                                         Implicit dynamic frames (IDF) [26] is a verification technique related to separation logic that can
                                         provide modularity benefits by separating ownership specifications from assertions about heap
                                         contents. In the context of IDF, unfolding expressions are a type of expression that temporarily
                                         unfolds a predicate instance to gain ownership of additional fields during evaluation of a heap-
                                         dependent expression. These are of the form unfolding 𝑝 (𝑒) in 𝑒 0 where 𝑝 is a predicate, 𝑒 is the
                                         list of arguments passed to the predicate, and 𝑒 0 is the expression evaluated using the permissions
                                         encapsulated in the predicate. Unfolding expressions were originally introduced as part of the
                                         Chalice verifier [15] to enable more modular expressions of ownership. Similarly, pure functions
                                         allow developers to define heap-dependent, side effect-free, recursive functions that can be used
                                         in specifications. These also increase the modularity of specifications by allowing developers to
                                         separate and reuse recurring patterns. Both of these constructs appear in Viper [17] and many
                                         Viper-based verifiers such as Gobra for Go [30], Nagini for Python [8], SnaKt for Kotlin [22],
                                         Gradual C0 for C0 [7, 10, 18]. We observe that unfolding expressions and pure functions are used
                                         repeatedly throughout the verified packages of the Go standard library [12, 14], the implementation
                                         of VerifiedSCION, a next-generation Internet architecture [21], and the verified Go implementations
                                         of the Needham-Schroeder-Lowe, Diffie-Hellman, and WireGuard protocols [2, 3], demonstrating
                                         their use in verified codebases from the real-world.
                                            Together, unfolding expressions and pure functions enable design patterns in verified code that
                                         greatly improve modularity; for instance, Gobra codebases often define predicates that encapsulate

                                         Authors’ Contact Information: Hazel Torek, Clemson University, Clemson, South Carolina, USA, ctorek@clemson.edu;
                                         Long Tien Nguyen, Carnegie Mellon University, Pittsburgh, Pennsylvania, USA, longtien@cs.cmu.edu; Priyam Gupta, ETH
                                         Zürich, Zürich, Switzerland, priyam23g@gmail.com; Jenna DiVincenzo, Purdue University, West Lafayette, Indiana, USA,
                                         jennad@purdue.edu; Jonathan Aldrich, Carnegie Mellon University, Pittsburgh, Pennsylvania, USA, jonathan.aldrich@cs.
                                         cmu.edu.
2                                                                                                                   Torek et al.


                                                            // In Gobra , requires and ensures clauses precede
     type Int struct {                                      // the function / method they are associated with
         neg bool // sign                                   requires acc ( x . Mem ())
         abs nat // absolute value                          ensures acc ( x . Mem ()) &&
     }                                                               unfolding acc ( x . Mem ()) in
                                                                           len ( x . abs ) <= 1
     pred (i * Int ) Mem () {                                              == > toInt ( res ) == x . abs . toInt ()
         acc (i) && i. abs . Mem ()                         func ( x * Int ) Uint64 () ( res uint64 ) {
     }                                                          ... // returns uint64 representation of x
                                                            }


Fig. 1. Predicate definition and usage from the implementation of multi-precision signed integers in Verified-
SCION demonstrating a common design pattern enabled by unfolding expressions and pure functions.


entire data structures, using unfolding expressions to access fields of these data structures and pure
functions to represent properties of these data structures. Figure 1 demonstrates an example of this
pattern from the implementation of multi-precision signed integers in VerifiedSCION,1 and the
implementation of lists in the verified Go standard library provides a more complex example of
this pattern.2 Without these constructs, developers would be required to specify ownership of all
fields used in the specification and method separately and define separate predicates to express the
required recursive properties, which would significantly increase the specification burden.
   Accordingly, these are important constructs in increasing the usability and expressiveness of
implicit dynamic frames-based verifiers; however, their semantics have not yet been formalized
despite existing formalizations [6, 20] and they have not yet been included in a proof of soundness
of such a verifier. To address this gap and ensure the correctness of verifiers using this feature, we
provide a formalization and proof of soundness for a generalization of static verification called
gradual verification. Gradual verification is a verification technique introduced by Bader et al.
[5] to address the high upfront cost of static verification which, inspired by gradual typing [25],
enables developers to write explicitly partial specifications using the imprecise formula, written
as ?, which acts as a placeholder wildcard during static verification. For instance, ? ∗ 𝑥 > 9 can
refer to any non-contradictory strengthening of the formula 𝑥 > 9, such 𝑥 ≥ 15. These imprecise
specifications are backed by a combination of static and dynamic checks [29]. Notably, gradual
verification is designed to maintain an important property called the gradual guarantee, an idea
adapted from gradual typing: reducing the precision of a correct specification will never cause
the verifier to report a spurious error. Gradual verification is also a conservative extension of static
verification, meaning that a static verifier and the gradual verifier extended from it will coincide on
all fully-specified programs [29, 32].
   The initial formulation by Bader et al. lacked the ability to verify programs with recursive data
structures allocated on the heap, which limited its practicality for verifying real-world programs.
Wise et al. [29] and DiVincenzo et al. [7] later extended gradual verification with these capabilities
using implicit dynamic frames [26], a variation of separation logic [23], and recursive abstract
predicates [19]. These extensions were accompanied by an implementation for the C0 subset of the
C programming language [1, 7] by extending the Silicon symbolic execution backend for Viper
[17, 24] into Gradual Viper.
   Since Gradual Viper uses symbolic execution rather than weakest liberal preconditions, Zim-
merman et al. [32] provided a full formal system corresponding to Gradual Viper, including static
1 Our example has been slightly adapted for readability. For multi-precision signed integers, the original implementation

and usage can be found in int.gobra in VerifiedSCION.
2 For lists, the predicate is defined in list_spec.gobra and used in list.go in the verified Go standard library.
Gradually Verifying Unfolding Expressions & Pure Functions                                            3


and dynamic semantics, definitions of the correspondence between static and dynamic verifier
states, and a proof of soundness. Because gradual verification is a conservative extension of its
static counterpart, this also proves the soundness of a subset of the underlying Viper features. How-
ever, this formalization lacks many other underlying Viper constructs that could improve verifier
usability; for instance, Gupta [10] introduced unfolding expressions and Mutlu [18] introduced
pure functions to Gradual Viper’s implementation, but the formalization and proof of soundness
does not yet include either of these features.
   Addressing this gap in the static and gradual verification ecosystems, this paper makes the
following contributions:
 • Design and formalization of the symbolic evaluation semantics for unfolding expressions and
   pure functions in IDF-based verifiers such as Viper.
 • Design and formalization of the static semantics, dynamic semantics, and their correspondence
   for unfolding expressions and pure functions in Gradual Viper.
 • An updated proof of soundness for Gradual Viper, based on the formal system provided by
   Zimmerman et al [32], which also applies to a subset of Viper’s features.
   With these contributions, we increase our confidence in the correctness of Viper’s implementation
and Viper-based verification tools that use these constructs, both directly and in translation.
Additionally, by expanding upon the gradual verification ecosystem rather than focusing solely on
static verification, we maintain the same correctness guarantees while inheriting a rich body of
work on both implementation and formalization for gradual verification.

2     Viper Semantics
2.1    Ownership & Predicates in Viper
In static verification of imperative programs, ownership reasoning is used to maintain invariants
regarding heap contents and aliasing. These reasoning capabilities are established with logics like
separation logic [23], which requires reasoning about heap ownership and contents simultaneously,
or implicit dynamic frames [26], which enables specifying ownership and contents separately. The
Viper verification infrastructure, built on implicit dynamic frames, enables ownership reasoning
using several different verification primitives, the most fundamental of which is the accessibility
predicate. An accessibility predicate, written acc(𝑥 .𝑓 ), specifies read and write access to field 𝑓 of
structure 𝑥.
   In verifiers based on implicit dynamic frames, a specification is framed if it only accesses heap
locations it has permission to access. To account for this requirement regardless of the owned
heap locations in a specific verification state, specifications must be self-framing, meaning they
must specify ownership of all the fields used in the formula to be well-defined. For instance, the
specification 𝑥 .𝑓 ≥ 9 is not self-framed, but the specification acc(𝑥 .𝑓 ) ∗ 𝑥 .𝑓 ≥ 9 is.
   In Viper, predicates are named, parameterized assertions that are used to encapsulate ownership
of and express properties of potentially-unbounded data structures like lists and trees. The logic
for specifying these structures is provided by recursive abstract predicates [19]. However, there are
two differing interpretations of these predicates that lead to different semantics for assertions and
different ways of specifying ownership [28]. Under the equirecursive approach, an instance of a
predicate is considered equivalent to the information contained in its body. Although this is viewed
as more intuitive, this poses a problem in implementation because recursive predicates become
unbounded. In contrast, the isorecursive approach (used in Viper [24]) views predicate instances
and the information contained therein as distinct, requiring developers to manually exchange
between these by unfolding and folding predicate instances (some verifiers such as VeriFast [11]
use the terms opening and closing a predicate, respectively). Accordingly, unfolding expressions
4                                                                                              Torek et al.


                           struct Node { int data ; struct Node * next ; };

                           /* @
                           predicate sortedList ( struct Node * x ) =
                             ( x == NULL ) ? true : (
                                acc (x - > data ) && acc (x - > next ) &&
                                sortedList (x - > next ) && (x - > next == NULL ||
                                  unfolding sortedList (x - > next ) in
                                     x - > data <= x - > next - > data )
                               );
                           @ */


                                  Fig. 2. Checking that a list is sorted [10].



temporarily unfold a predicate, using additional permissions from its body to ensure the evaluation
of the expression is framed with sufficient permissions.
   Without using unfolding expressions in combination with pure functions, specifications are
more complex and less intuitive; for instance, in Figure 2, checking whether a linked list is sorted
would require adding an additional parameter to the sortedList predicate keeping track of the
previous value. In some cases, writing the specification without unfolding expressions might even
require additional ghost code/auxiliary data to facilitate verification [10].

2.2     Representation
The static semantics are based on the Silicon backend for Viper [24]. During symbolic execution,
the symbolic state 𝜎 tracks information about the execution of the program, and is formulated as a
tuple with the following components:
    • The precise heap H represents distinct heap chunks where ownership is statically verified.
    • The symbolic store 𝛾 maps variables to symbolic values.
    • The path condition 𝑔 identifies the path through branches in the program.
    • The visited set V tracks predicates that have already been unfolded and pure functions that
      have already been evaluated during recursive evaluation of these constructs; the use of this is
      described in Section 2.3.
  The program is statically verified starting from an initial symbolic state 𝜎, which is updated
throughout the process by performing four fundamental operations:
    • Symbolically evaluating a symbolic expression 𝑒 into a symbolic value 𝑡, resulting in new state
      𝜎 ′ . This is denoted by 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′ .
    • Producing the information from formula 𝜙˜ into the symbolic heap, resulting in new state 𝜎 ′ ;
      denoted 𝜎 ⊢ 𝜙˜ ◁ 𝜎 ′ . Intuitively, this adds information to the state.
    • Consuming a formula 𝜙˜ from the symbolic state, resulting in new state 𝜎 ′ ; denoted 𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′ .
      Intuitively, this checks for and removes information in the state.
    • Symbolically executing a statement. Notation and definitions of this judgement are provided in
      the appendix since it is not directly used or extended here.

2.3     Static Semantics for Unfolding Expressions in Viper
Because unfolding expressions are a type of expression, we extend the symbolic evaluation judge-
ment, additionally relying on the consume and produce judgements. The example in figure 3
demonstrates our formalization of the purely static approach in the Silicon backend for Viper.
Gradually Verifying Unfolding Expressions & Pure Functions                                               5


                                           field val : Int

                                           predicate pos ( x : Ref ) { acc ( x . val ) * x . val > 0 }

                                          method caller ( x : Ref , ...)
                                            requires pos ( x )
                                            ensures ...
                                          {
                                              ... unfolding pos ( x ) in ( x . val < 256) ...
                                          }


                                            Fig. 3. Example of unfolding expression.


   We start with an initial symbolic state with true as the path condition and ∅ as the visited
set. Assume we have an object 𝑥 and an initial symbolic heap containing an instance of the pos
predicate applied to 𝑥. Note that the symbolic heap doesn’t directly contain a field chunk pertaining
to 𝑥 .val because it is encapsulated by the predicate pos. We use grey highlights to show the current
symbolic state at a given step and blue highlights to show the operations being performed.
𝜎1 = ⟨H1 , 𝛾, true, ∅ ⟩    H1 = { ⟨ pos, 𝑡𝑥 ⟩ } 𝛾 = [ x ↦→ 𝑡𝑥 ]

  To begin evaluation of the unfolding expression unfolding pos(𝑥) in 𝑥 .val < 256, we evaluate
the argument 𝑥 passed to the predicate. Because 𝑥 is mapped to 𝑡𝑥 in the symbolic environment,
evaluation simply looks up the underlying values and the symbolic state remains unchanged.
𝜎 1 ⊢ 𝑥 ⇓ 𝑡𝑥 ⊣ 𝜎 1

   Then, we must temporarily exchange the predicate instance pos(𝑥) for its body to temporarily
frame the inner expression 𝑥 .val < 256 with additional permissions. To do so, we first consume
the predicate instance to ensure that it holds in the current state; this removes the predicate chunk
⟨pos, 𝑡𝑥 ⟩ from the symbolic heap.
𝜎1 ⊢ pos (𝑥 ) ▷ 𝜎2
𝜎2 = ⟨H2 , 𝛾, true, ∅ ⟩    H2 = ∅ 𝛾 = [ x ↦→ 𝑡𝑥 ]

  Now, we produce the body of the predicate to obtain the permissions encapsulated within,
yielding a symbolic heap containing the field chunk ⟨val, 𝑡𝑥 , 𝑎⟩ and the path condition 𝑎 > 0
where 𝑎 is a fresh symbolic value. This also requires updating the visited set V to prevent unbounded
recursion; more discussion of the handling of recursive unfolding expressions is provided at the
end of this section.
𝜎2 ⊢ acc (𝑥 .val ) ◁ 𝜎3
𝜎3 = ⟨H3 , 𝛾, 𝑎 > 0, { pos } ⟩   H3 = { ⟨ val, 𝑡𝑥 , 𝑎⟩ } 𝛾 = [ x ↦→ 𝑡𝑥 ]

  Now, having exchanged the predicate instance for its body, we have a suitable environment for
evaluating the inner expression. Since this evaluation recurs over the operation and requires only
evaluating a variable and a literal, the state is unchanged except for having updated the visited set.
𝜎3 [ V = ∅ ] ⊢ 𝑥 .val < 256 ⇓ 𝑎 < 256 ⊣ 𝜎4
𝜎4 = ⟨H4 , 𝛾, 𝑎 > 0, ∅ ⟩   H4 = { ⟨ val, 𝑡𝑥 , 𝑎⟩ } 𝛾 = [ x ↦→ 𝑡𝑥 ]

  Now, because the predicate instance must be re-folded after the expression is evaluated, we
simply reset the symbolic heap to its initial state to receive our final state.
𝜎5 = ⟨H5 , 𝛾, 𝑎 > 0, ∅ ⟩   H5 = { ⟨ pos, 𝑡𝑥 ⟩ } 𝛾 = [ x ↦→ 𝑡𝑥 ]

  In the end, this procedure returns the expression 𝑎 < 256 from the penultimate step. This entire
process is described formally by the SEvalUnfoldingExplicit rule in Figure 4. Note that, due to
6                                                                                                                     Torek et al.


    SEvalUnfoldingExplicit
                                                𝑝 ∉ V (𝜎1 )        𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2
    𝜎2 ⊢ 𝑝 (𝑒 ) ▷ 𝜎3   𝑥 = predicate_params(𝑝 )            𝜎3 [𝛾 = 𝛾 (𝜎3 ) [𝑥 ↦→ 𝑡 ], V = V (𝜎3 ) ∪ {𝑝 } ] ⊢ predicate(𝑝 ) ◁ 𝜎4
                          𝜎4 [𝛾 = 𝛾 (𝜎3 ) ] ⊢ 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎5      𝜎6 = 𝜎5 [ V = V (𝜎1 ), H = H(𝜎2 ) ]
                                           𝜎1 ⊢ unfolding 𝑝 (𝑒 ) in 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎6
                           SEvalUnfoldingImplicit
                           𝑝 ∈ V (𝜎1 )  𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2            ⟨𝑝, 𝑡 ⟩ ∈ H(𝜎2 )      𝑡 0 = fresh
                                            𝜎 ⊢ unfolding 𝑝 (𝑒 ) in 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎2


                       Fig. 4. Symbolic evaluation rules for unfolding expressions in Viper.




the isorecursive semantics of symbolic evaluation, predicate(𝑝) refers to the body of the predicate
𝑝 obtained by unfolding once, not by the full unrolling.
   The SEvalUnfoldingImplicit rule in Figure 4 is specific to our handling of recursive unfolding
expressions. In cases where an unfolding expression is applied with a predicate that unfolds another
instance of the same predicate, following the previously described process in its entirely can result
in unbounded recursion. This is exemplified by Figure 2, where evaluating an unfolding expression
with the sorted predicate will then unfold another instance of the same predicate, and the recursion
will not terminate because evaluation will branch over both the base and recursive cases to verify
all possible paths. To address this, our approach is adapted from that of Schwerhoff for Viper [24];
using the visited set V, we track which predicates have already been unfolded. Then, if a predicate
being unfolded has already been visited, the recursion is terminated by replacing the result of the
entire expression with an uninterpreted symbolic value. Although we don’t unfold the predicate
due to the possibility of unbounded recursion, we do still check that a predicate instance is present
in the heap to ensure that this operation will succeed at run-time. This approach is theoretically
incomplete, but it is still sound and this incompleteness is rarely observed in practice since it
requires manually unfolding predicates to the depth where the recursion was cut off. Although we
have formalized this behavior using a set, it could easily be exchanged for a multiset to enable a
specified cutoff depth rather than only allowing a depth of one.

2.4    Static Semantics for Pure Functions in Viper
Our approach for the evaluation of pure functions is based on that of Smans et al. in the Smallfoot
verifier [27] for when the bodies of pure functions are visible. However, in Viper pure functions can
have both preconditions and post-conditions, whereas in Smallfoot they can only have preconditions.
This requires us to expand our approach to axiomatize not only the result of the function evaluation,
but also the post-condition. This also means that we must provide a new definition for well-
formedness rather than using the one for methods, since methods may have a formula as their
post-condition rather than an expression. Accordingly, we impose the additional constraint that
evaluation should succeed in the symbolic state obtained from producing the precondition; this
corresponds to the body being framed by the precondition, meaning the precondition contains
all permissions necessary for evaluating the body. The use of precondition will also impact our
handling of recursive pure functions, described later in this section.
   We demonstrate our formalization of the purely static approach of Smans et al. using the example
in figure 5.
Gradually Verifying Unfolding Expressions & Pure Functions                                                       7


                                            field val : Int

                                            function add ( x : Ref , y : Ref ): Int
                                              requires acc ( x . val ) * acc ( y . val )
                                              ensures ( y . val < 0) || ( result >= x . val )
                                              { x . val + y . val }

                                            method caller (...)
                                              requires ...
                                              ensures ...
                                            {
                                                ... add (x , y ) ...
                                            }


                                                   Fig. 5. Example of pure function.


   To demonstrate the use of including the post-condition in our approach, we use the post-condition
(𝑦.val ≥ 0) =⇒ (result ≥ 𝑥 .val), so that it does not directly articulate the same information
provided by the implementation. In the program, we write this as (𝑦.val < 0) ∨ (result ≥ 𝑥 .val),
using the fact that 𝑝 =⇒ 𝑞 ≡ ¬𝑝 ∨ 𝑞 since implications are not formalized in prior work.
   Then, assume we have objects 𝑥 and 𝑦 and an initial symbolic heap containing the field chunks
H(𝜎1 ) = {⟨val, 𝑡𝑥 , 𝑎⟩, ⟨val, 𝑡 𝑦 , 𝑏⟩}, meaning field val of object 𝑡𝑥 (corresponding to the symbolic
variable 𝑥) has value 𝑎 and field val of object 𝑡 𝑦 (corresponding to 𝑦) has value 𝑏. Note that, since
these objects are contained in the symbolic heap, they must not be aliases.
   Now, we demonstrate the process for symbolically evaluating these in our formalization. We
start with a symbolic state containing only the necessary heap chunks and variable mappings for
our assumptions that is otherwise empty.
𝜎1 = ⟨H1 , 𝛾, true, ∅ ⟩    H1 = { ⟨ val, 𝑡𝑥 , 𝑎⟩, ⟨ val, 𝑡 𝑦 , 𝑏 ⟩ } 𝛾 = [ x ↦→ 𝑡𝑥 , y ↦→ 𝑡 𝑦 ]

  Now, we begin with evaluation of the pure function application add(𝑥, 𝑦). First, we evaluate
each of the arguments to the function application into corresponding symbolic values. Since these
arguments are already variables in the symbolic environment, evaluation simply results in these
underlying values and the symbolic state is not changed.
𝜎 1 ⊢ 𝑥 ⇓ 𝑡𝑥 ⊣ 𝜎 1        𝜎1 ⊢ 𝑦 ⇓ 𝑡 𝑦 ⊣ 𝜎1

   Then, since pure functions can depend on values in the heap, we compute a heap snapshot to
implicitly pass as an argument to add that contains all the fields used in the function. Since the
bodies and post-conditions of pure functions must be framed by the precondition, we can generate
this snapshot using exclusively the precondition. In Smallfoot, these heap snapshots are obtained
directly by consuming the precondition. However, since the formalization from Zimmerman et
al. does not explicitly provide machinery to take heap snapshots, we introduce the notion of a
symbolic footprint of a formula 𝜙 to do so, written J𝜙K𝜎 , which recurses over the structure of a
formula to determine the heap chunks used when producing or consuming it.
Jacc (𝑥 .val ) ∗ acc (𝑦.val )K𝜎1 = Jacc (𝑥 .val )K𝜎1 ∪ Jacc (𝑦.val )K𝜎1 = { ⟨ val, 𝑡𝑥 , 𝑎⟩, ⟨ val, 𝑡 𝑦 , 𝑏 ⟩ }

  Then, to ensure the precondition holds, we consume the function’s precondition. In the result-
ing symbolic state 𝜎2 , access to both heap chunks has been removed. Because of the separating
conjunction ∗, the consume operation also ensures that the removed heap chunks aren’t aliases.
𝜎1 ⊢ acc (𝑥 .val ) ∗ acc (𝑦.val ) ▷ 𝜎2
𝜎2 = ⟨H2 , 𝛾, true, ∅ ⟩    H2 = ∅ 𝛾 = [ x ↦→ 𝑡𝑥 , y ↦→ 𝑡 𝑦 ]
8                                                                                                                                            Torek et al.


  After consuming and ensuring the precondition holds, we produce the precondition so that we
have a suitable environment for evaluating the function’s body, resulting in a symbolic heap that
again contains two heap chunks corresponding to the fields of our two objects.
𝜎2 ⊢ acc (𝑥 .val ) ∗ acc (𝑦.val ) ◁ 𝜎3
𝜎3 = ⟨H3 , 𝛾, true, ∅ ⟩    H3 = { ⟨ val, 𝑡𝑥 , 𝑎 ′ ⟩, ⟨ val, 𝑡 𝑦 , 𝑏 ′ ⟩ } 𝛾 = [ x ↦→ 𝑡𝑥 , y ↦→ 𝑡 𝑦 ]

   However, note that between H1 and H3 , 𝑎 ≠ 𝑎 ′ and 𝑏 ≠ 𝑏 ′ . Consuming and then producing the
same specification ensures that we will end up with field chunks corresponding to the same field
accesses, but it is critical to observe that these field chunks will contain distinct symbolic values,
since producing an accessibility predicate will initialize fresh symbolic values. So that the function
body is evaluated in a way that respects constraints on the original symbolic values, we must reset
these field chunks to use the correct values.
H4 = H(𝜎1 )
𝜎4 = ⟨H4 , 𝛾, true, ∅ ⟩    H4 = { ⟨ val, 𝑡𝑥 , 𝑎⟩, ⟨ val, 𝑡 𝑦 , 𝑏 ⟩ } 𝛾 = [ x ↦→ 𝑡𝑥 , y ↦→ 𝑡 𝑦 ]

  Now, we are prepared to evaluate the body of the function. Since the evaluation of the body
involves only looking up field chunks in the symbolic heap and looking up variables in the symbolic
environment, the symbolic heap, symbolic environment, and path condition remain unchanged.
However, we add the function name add to the visited set in the resulting state to track which
function bodies have been evaluated and prevent unbounded recursion.
𝜎4 [ V = { add } ] ⊢ 𝑥 .val + 𝑦.val ⇓ 𝑎 + 𝑏 ⊣ 𝜎5
𝜎5 = ⟨H5 , 𝛾, true, { add } ⟩   H5 = { ⟨ val, 𝑡𝑥 , 𝑎⟩, ⟨ val, 𝑡 𝑦 , 𝑏 ⟩ } 𝛾 = [ x ↦→ 𝑡𝑥 , y ↦→ 𝑡 𝑦 ]

   Instead of directly returning the result of evaluation, we now encode the result of evaluation
into the path condition because of the implicit dependency on the heap snapshot. Accordingly, we
generate a fresh symbolic variable add(𝑎, 𝑏, 𝑠), which represents the dependencies on the heap and
the arguments, and require in the path condition that add(𝑎, 𝑏, 𝑠) = 𝑎 + 𝑏. We additionally reset the
value of V because we only care to cut off recursive function calls, not sequential ones.
add (𝑎, 𝑏, 𝑠 ) = fresh
𝜎6 = ⟨H6 , 𝛾, add (𝑎, 𝑏, 𝑠 ) == 𝑎 + 𝑏, ∅ ⟩    H6 = { ⟨ val, 𝑡𝑥 , 𝑎⟩, ⟨ val, 𝑡 𝑦 , 𝑏 ⟩ } 𝛾 = [ x ↦→ 𝑡𝑥 , y ↦→ 𝑡 𝑦 ]

   Furthermore, the post-condition may contain further restrictions or information about the result-
ing value. However, in its current form, the post-condition is an arbitrary expression containing
field accesses and the result variable, so we must axiomatize it to include it in the post-condition.
Accordingly, we introduce a new function axiomatize𝜎 [add(𝑎, 𝑏, 𝑠)] (𝑒), which recurses over the
expression 𝑒, substituting result with the symbolic variable add(𝑎, 𝑏, 𝑠) and substituting field
accesses for their underlying symbolic values from the snapshot.
axiomatize𝜎6 [ add (𝑎, 𝑏, 𝑠 ) ] ( (𝑦.val < 0) || ( result >= 𝑥 .val ) ) = (𝑎 < 0) || ( add (𝑎, 𝑏, 𝑠 ) >= 𝑏 )

𝜎7 = ⟨H7 , 𝛾, ( add (𝑎, 𝑏, 𝑠 ) == 𝑎 + 𝑏 ) && ( (𝑎 < 0) || ( add (𝑎, 𝑏, 𝑠 ) >= 𝑏 ) ), ∅⟩       H7 = { ⟨ val, 𝑡𝑥 , 𝑎⟩, ⟨ val, 𝑡 𝑦 , 𝑏 ⟩ } 𝛾 = [ x ↦→ 𝑡𝑥 , y ↦→ 𝑡 𝑦 ]

   Finally, we return the generated symbol add(𝑎, 𝑏, 𝑠), which is constrained by the path condition.
   Formally, this process can be represented by the rules in Figure 6. Similarly to unfolding expres-
sions, pure functions are also susceptible to unbounded verification during static verification since
a recursive function evaluation will branch over both the base case and recursive case due to the
use of symbolic values rather than concrete values. To address recursive functions, we use the same
approach as Section 2.3, where SEvalPureExplicit refers to the case where the function has not
yet recursively called itself and the body is evaluated and SEvalPureImplicit refers to the case
where the function is being recursively called and the body is not evaluated to prevent unbounded
Gradually Verifying Unfolding Expressions & Pure Functions                                                                                   9


     SEvalPureExplicit
     𝑓 ∉ V (𝜎1 )       𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2     𝑥 = params( 𝑓 )            𝑠 = Jpre( 𝑓 )K𝜎2         𝜎2 [𝛾 = 𝛾 (𝜎2 ) [𝑥 ↦→ 𝑡 ] ] ⊢ pre( 𝑓 ) ▷ 𝜎3
                       𝜎3 ⊢ pre( 𝑓 ) ◁ 𝜎4     H′ = { ⟨ 𝑓 , 𝑡𝑒 , 𝑡 ′ ⟩ : ⟨ 𝑓 , 𝑡𝑒 , 𝑡 ⟩ ∈ H(𝜎4 ), ⟨ 𝑓 , 𝑡𝑒 , 𝑡 ′ ⟩ ∈ H(𝜎2 ) }
                                     𝜎4 [H = H′ , V = V (𝜎3 ) ∪ { 𝑓 } ] ⊢ body( 𝑓 ) ⇓ 𝑡 ′ ⊣ 𝜎5 R 3
                𝑓 (𝑡, 𝑠 ) = fresh     𝜎6 = 𝜎2 [𝑔 = 𝑔 (𝜎2 ) && ( 𝑓 (𝑡, 𝑠 ) == 𝑡 ′ ) && axiomatize𝜎 [ 𝑓 (𝑡, 𝑠 ) ] (post( 𝑓 ) ) ]
                                                         𝜎1 ⊢ 𝑓 (𝑒 ) ⇓ 𝑓 (𝑡, 𝑠 ) ⊣ 𝜎6
    SEvalPureImplicit
                               𝑓 ∈ V (𝜎1 )      𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2       𝑥 = params( 𝑓 )     𝑠 = Jpre( 𝑓 )K𝜎2
    𝜎2 [𝛾 = 𝛾 (𝜎2 ) [𝑥 ↦→ 𝑡 ] ] ⊢ pre( 𝑓 ) ▷ 𝜎3     𝑓 (𝑡, 𝑠 ) = fresh    𝜎4 = 𝜎2 [𝑔 = 𝑔 (𝜎2 ) && axiomatize𝜎 [ 𝑓 (𝑡, 𝑠 ) ] (post( 𝑓 ) ) ]
                                                         𝜎1 ⊢ 𝑓 (𝑒 ) ⇓ 𝑓 (𝑡, 𝑠 ) ⊣ 𝜎4


                        Fig. 6. Symbolic evaluation rules for pure function applications in Viper.




recursion. This approach is theoretically incomplete; however, we axiomatize the post-condition of
the recursive application to minimize this drawback.
   Compared to the approach detailed here, Viper’s symbolic execution engine uses a more complex
approach based on passing axioms to the underlying SMT solver to enable more complete quantifier
triggering strategies, which increases performance when functions with large bodies are called
repeatedly or when using recursive functions [24]. We instead opt for the strategy described by
Smans et al. because the Zimmerman et al. formalization does not directly interface with the
underlying SMT solver beyond implicitly assuming its soundness; since the path condition is
provided to the SMT solver during verification, we instead opt to emulate this behavior by adding
these axioms to the path condition.

3      Gradual Viper Semantics
After gradual verification was implemented for the C0 subset of the C programming language
and the underlying Gradual Viper verifier by DiVincenzo et al. [7], it was proved to be sound by
Zimmerman et al. [32]. This work differs from the previous formalizations of gradual verification
[5, 29] in that it specifically focuses on the Silicon symbolic execution backend for Viper rather
than the weakest liberal preconditions approach used in previous iterations and that the semantics
are formalized in non-deterministic inference rules rather than continuation passing-style rules.
Overall, the formalization is structured as several components: the static semantics, the dynamic
semantics, the correspondence, and the proof of soundness.
   In this section, we provide and examine the formal semantics for symbolic evaluation, run-time
evaluation, and framing alongside the definition of exact footprints for unfolding expressions.
Additionally, we describe the changes we’ve made to the definitions of correspondence between
static and dynamic states to account for the addition of unfolding expressions.

3.1 Representation
Gradual Viper enables imprecise specifications through the use of the ? operator; accordingly, we
expand our definition of formulae to include imprecise formulas, written 𝜙˜ = ?∗𝜙. In our context, this
is noteworthy because an imprecise specification represents any non-contradictory strengthening
of the precise portion, meaning that formulas like ? ∗ 𝑥 .𝑓 ≥ 2 can also be strengthened with
accessibility predicates (acc(𝑥 .𝑓 ) ∗ 𝑥 .𝑓 ≥ 2) or with arbitrary unfolding of user-defined predicates
(unfolding pred(𝑥) in 𝑥 .𝑓 >= 2 where pred(𝑥) specifies access to 𝑥 .𝑓 ) [29].
10                                                                                          Torek et al.


3.1.1 Symbolic State. Because a symbolic state can now be imprecise, the state now includes an
imprecision flag, written 𝜄, representing whether the current state is imprecise. Additionally, to
store optimistic assumptions, the symbolic state also includes a optimistic heap, written H .
 • The imprecise flag 𝜄 ∈ {⊤, ⊥} indicates whether a specification containing ? was used during
   symbolic execution and thus whether the current state can make optimistic assumptions.
 • The optimistic heap H represents field chunks and predicate chunks that may not be distinct
   where ownership is optimistically assumed. If the current state is precise, this must be empty.
 • The precise heap H, symbolic store 𝛾, path condition 𝑔, and visited set V behave as described
   previously.
   The fundamental operations describing static verification are the same; however, because Gradual
Viper also includes imprecise specifications and optimistic assumptions, these operations can now
also produce sets of run-time checks, written R. Optimistic assumptions about ownership are backed
by these runtime checks, meaning that ownership also has to be tracked dynamically rather than
only statically. This specifically poses a challenge for methods with imprecise preconditions, since
this requires taking ownership of all fields owned by the caller since any might be used by the
callee [29].
 • Symbolically evaluating a symbolic expression 𝑒 into a symbolic value 𝑡, resulting in new state
   𝜎 ′ and run-time checks R. This is denoted by 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R. The run-time checks R will
   ensure that all fields and predicate instances necessary to evaluate the expression are available.
 • Producing the information from formula 𝜙˜ into the symbolic heap, resulting in new state 𝜎 ′ ;
   denoted 𝜎 ⊢ 𝜙˜ ◁ 𝜎 ′ .
 • Consuming a specification 𝜙˜ from the symbolic state, resulting in new state 𝜎 ′ and run-time
   checks R; denoted 𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, R. The run-time checks R will ensure that the specification holds
   if optimistic assumptions are made.
 • Symbolically executing a statement (notation unnecessary since we neither extend nor rely
   upon this judgement).
  The semantics for these operations will coincide with those for Silicon for when the program
being verified is fully precise, which will result in no run-time checks; the formalization of Gradual
Viper conservatively extends these to account for cases with imprecise specifications, resulting
optimistic assumptions, and runtime checks.
3.1.2 Dynamic State. The execution semantics for Gradual C0 were derived from those of of
the original C0 language [1]. In addition to these, the Gradual C0 dynamic semantics include the
definition of the footprint of a formula, which is the set of permissions necessary to assert that
formula.
   Analogous to how the symbolic state tracks information about a symbolic execution path, we
track information about the execution of the program at run time with a heap 𝐻 , an environment
𝜌 mapping variables to values, and a permission set 𝛼 tracking the owned fields. There are three
main operations at run time that use this information.
 • Evaluating an expression 𝑒 into a concrete value 𝑡, denoted by ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑡.
                       ˜ denoted by ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙.
 • Asserting a formula 𝜙,                         ˜
 • Executing a statement (again, notation elided for simplicity).

3.2   Static Semantics for Unfolding Expressions in Gradual Viper
With the introduction of imprecise specifications, there are several cases in which the behavior of
unfolding expressions change, depending on whether the initial state is precise, whether the body
Gradually Verifying Unfolding Expressions & Pure Functions                                             11


of the predicate is precise, and whether the predicate recursively unfolds another instance of itself.
If the predicate has not recursively unfolded another instance of itself, the following cases apply.

 • If the initial state is precise, then the optimistic heap must remain empty regardless of whether
   the predicate being unfolded is precise or not. This is because, in a precise state, the optimistic
   heap must remain empty to ensure soundness, since the optimistic heap contains assumptions
   made from an imprecise state. This is represented by the SEvalUnfoldingPrecise rule in
   Figure 8.
 • If the initial state is imprecise and the predicate body is precise, the precise heap is reset as
   usual but the information from the final optimistic heap and an instance of the predicate are
   retained in the optimistic heap. The assumptions from the final optimistic heap can be retained
   since they resulted from imprecision in the initial state and not the predicate body – since the
   predicate body must be re-folded, its resulting optimistic assumptions must be discarded. The
   predicate instance is also included because it must be optimistically assumed for framing during
   run-time evaluation. This is represented by the SEvalUnfoldingImpreciseA rule.
 • If both the initial state and the predicate body are precise, then the assumptions in the final
   optimistic heap are discarded because those assumptions could have arisen as a result of the
   imprecision in the predicate rather than the imprecision in the initial state. Conservatively,
   our design assumes that these assumptions were made resulting from the imprecision in the
   predicate body and thus must be removed when the predicate is re-folded. This is represented
   by the SEvalUnfoldingImpreciseB rule.

   Although we could naively reset both the precise and optimistic heaps in any case, our design
safely decreases the run-time overhead by retaining assumptions in the optimistic heap if possible.
   Our handling of predicates that recursively unfold another instance of themselves is similar to
the approach described in Section 2.3, where the SEvalUnfoldingImplicit rule from Figure 4
applies to cut off unbounded recursion. However, in the gradual case, additional complications
arise from the possibility of an imprecise initial state, meaning that we have to account for the
following cases:

 • The predicate instance is already in either the precise or optimistic heap. In this case, the
   unfolding operation will succeed, since access to the predicate instance has been statically
   proven. This behavior is represented by the SEvalUnfoldingImplicitPrecise rule.
 • The initial state is imprecise and the predicate instance isn’t in either heap. In this case, the
   unfolding operation will succeed, since access to the predicate instance can be optimistically
   assumed by adding a matching run-time check. This behavior is represented by the SEvalUn-
   foldingImplicitImprecise rule.
 • The initial state is precise and the predicate instance isn’t in either heap. In this case, the unfold-
   ing operation will not succeed since the predicate instance isn’t available statically or through
   optimistic assumptions. This behavior is represented by the SEvalUnfoldingImplicitFailure
   rule, since returning an unsatisfiable run-time check set {⊥} corresponds to a failure of static
   verification.

  In order to avoid unbounded recursion in the rules, we don’t actually unfold the predicate
instance in any of these cases; however, soundness still requires checking whether the instance is
available. Otherwise, a recursive unfolding expression might statically verify when the predicate
being unfolded doesn’t hold statically or at run time.
  In Figure 7, we specifically examine an example with a precise initial state and an imprecise
predicate being unfolded to demonstrate our design of the unfolding expression semantics.
12                                                                                                                         Torek et al.


                                           field val : Int

                                           predicate pos ( x : Ref ) {              ?    * x . val > 0 }

                                           method caller ( x : Ref , ...)
                                             requires pos ( x )
                                             ensures ...
                                           {
                                               ... unfolding pos ( x ) in ( x . val < 256) ...
                                           }


                          Fig. 7. Example of unfolding expression with imprecise predicate.



   To demonstrate the importance of the imprecise predicate and the optimistic assumptions
it enables, we assume that we have objects 𝑡 𝑦 and 𝑡𝑧 with an initial symbolic heap H(𝜎1 ) =
{⟨pos, 𝑡𝑥 ⟩, ⟨val, 𝑡 𝑦 , 𝑏⟩}, meaning predicate pos holds with argument 𝑡𝑥 and field val of object 𝑡 𝑦
has value 𝑏. Although 𝑡 𝑦 isn’t used in the body of the predicate, we include it to highlight how the
gradual case interacts with the heap. Again, we start with a precise (represented by ⊥) symbolic
state that contains only the described heap chunk and variable mappings for our assumptions.
𝜎1 = ⟨⊥, H1 , H1 , 𝛾, true, ∅ ⟩    H1 = { ⟨ pos, 𝑡𝑥 ⟩, ⟨ val, 𝑡 𝑦 , 𝑏 ⟩ }   H1 = ∅ 𝛾 = [ x ↦→ 𝑡𝑥 , y ↦→ 𝑡 𝑦 ]

   We evaluate the predicate argument, resulting in the same symbolic state. However, as described
in Section 3.1, the form of the evaluation judgement has changed to include an additional set
of run-time checks accumulated through evaluation. In this case, the set is empty because the
evaluation only requires looking up a variable in the symbolic environment. Note that even though
we do not have a heap chunk corresponding to 𝑥 .val, we can evaluate 𝑥 itself since we are only
looking up the underlying value 𝑡𝑥 in the symbolic environment, not accessing a field of 𝑡𝑥 .
𝜎 1 ⊢ 𝑥 ⇓ 𝑡𝑥 ⊣ 𝜎 1 , ∅

   Now, we consume an instance of the predicate. Since we are currently in a precise state and
consuming a predicate instance does not interact with the imprecise body, we remain in a precise
state afterwards. Note that this also includes a set of run-time checks, which is again empty because
the predicate instance is statically proven.
𝜎1 ⊢ pos (𝑡𝑥 ) ▷ 𝜎2 , ∅
𝜎2 = ⟨⊥, H2 , H2 , 𝛾, true, ∅ ⟩    H2 = { ⟨ val, 𝑡 𝑦 , 𝑏 ⟩ }    H2 = ∅ 𝛾 = [ x ↦→ 𝑡𝑥 , y ↦→ 𝑡 𝑦 ]

  To achieve the desired unfolding, we now produce the predicate’s body so that the information
contained therein is accessible while evaluating the inner expression. We also set the visited set to
{pos} to avoid unbounded recursion if the predicate unfolds itself in its body. Because the predicate
body is imprecise, this results in an imprecise state; while evaluating the inner expression, this also
optimistically assumes access to 𝑥 .val, adding it to the optimistic heap.
𝜎2 [ V = { pos } ] ⊢ 𝑥 .val > 0 ◁ 𝜎3
𝜎3 = ⟨⊤, H3 , H3 , 𝛾, 𝑎 > 0, { pos } ⟩   H3 = { ⟨ val, 𝑡 𝑦 , 𝑏 ⟩ }    H3 = { ⟨ val, 𝑡𝑥 , 𝑎⟩ } 𝛾 = [ x ↦→ 𝑡𝑥 , y ↦→ 𝑡 𝑦 ]

  Now, we are ready to evaluate the inner expression. Again, the state remains unchanged (except
for having reset V) and there are no run-time checks because we simply look up 𝑥 .val in the
optimistic heap.
𝜎3 [ V = ∅ ] ⊢ 𝑥 .val < 256 ⇓ 𝑎 < 256 ⊣ 𝜎4 , ∅
𝜎4 = ⟨⊤, H4 , H4 , 𝛾, 𝑎 > 0, ∅ ⟩    H4 = { ⟨ val, 𝑡 𝑦 , 𝑏 ⟩ }   H4 = { ⟨ val, 𝑡𝑥 , 𝑎⟩ } 𝛾 = [ x ↦→ 𝑡𝑥 , y ↦→ 𝑡 𝑦 ]
Gradually Verifying Unfolding Expressions & Pure Functions                                                                                          13


SEvalUnfoldingPrecise
                                             ¬𝜄 (𝜎1 )       𝑝 ∉ V (𝜎1 )      𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2 , R 1
 𝜎2 ⊢ 𝑝 (𝑒 ) ▷ 𝜎3 , R 2        𝑥 = predicate_params(𝑝 )            𝜎3 [𝛾 = 𝛾 (𝜎3 ) [𝑥 ↦→ 𝑡 ], V = V (𝜎3 ) ∪ {𝑝 } ] ⊢ predicate(𝑝 ) ◁ 𝜎4
                          𝜎4 [𝛾 = 𝛾 (𝜎3 ) ] ⊢ 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎5 , R 3    𝜎6 = 𝜎5 [ V = V (𝜎1 ), H = H(𝜎2 ), H = ∅ ]
                                         𝜎1 ⊢ unfolding 𝑝 (𝑒 ) in 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎6 , R 1 ∪ R 2 ∪ R 3
 SEvalUnfoldingImpreciseA
                                                             𝜄 (𝜎1 )
 predicate(𝑝 ) is precise      𝑝 ∉ V (𝜎1 )      𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2 , R 1    𝜎2 ⊢ 𝑝 (𝑒 ) ▷ 𝜎3 , R 2      𝑥 = predicate_params(𝑝 )
         𝜎3 [𝛾 = 𝛾 (𝜎3 ) [𝑥 ↦→ 𝑡 ], V = V (𝜎3 ) ∪ {𝑝 } ] ⊢ predicate(𝑝 ) ◁ 𝜎4      𝜎4 [𝛾 = 𝛾 (𝜎3 ) ] ⊢ 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎5 , R 3
                    H ′ = H (𝜎2 ) ∪ H (𝜎5 ) ∪ { ⟨𝑝, 𝑡 ⟩ }     𝜎6 = 𝜎5 [ V = V (𝜎1 ), H = H(𝜎2 ), H = H ′ ]
                                         𝜎1 ⊢ unfolding 𝑝 (𝑒 ) in 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎6 , R 1 ∪ R 2 ∪ R 3
SEvalUnfoldingImpreciseB
                       𝜄 (𝜎1 )       predicate(𝑝 ) is imprecise     𝑝 ∉ V (𝜎1 )        𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2 , R 1
𝜎2 ⊢ 𝑝 (𝑒 ) ▷ 𝜎3 , R 2     𝑥 = predicate_params(𝑝 )         𝜎3 [𝛾 = 𝛾 (𝜎3 ) [𝑥 ↦→ 𝑡 ], V = V (𝜎3 ) ∪ {𝑝 } ] ⊢ predicate(𝑝 ) ◁ 𝜎4
            𝜎4 [𝛾 = 𝛾 (𝜎3 ) ] ⊢ 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎5 , R 3   𝜎6 = 𝜎5 [ V = V (𝜎1 ), H = H(𝜎2 ), H = H (𝜎2 ) ∪ { ⟨𝑝, 𝑡 ⟩ } ]
                                         𝜎1 ⊢ unfolding 𝑝 (𝑒 ) in 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎6 , R 1 ∪ R 2 ∪ R 3
                          SEvalUnfoldingImplicitPrecise
                          𝑝 ∈ V (𝜎1 )  𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2 , R                    ⟨𝑝, 𝑡 ⟩ ∈ H(𝜎2 ) ∪ H (𝜎2 )          𝑡 0 = fresh
                                                  𝜎1 ⊢ unfolding 𝑝 (𝑒 ) in 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎2 , R
  SEvalUnfoldingImplicitImprecise
                                  𝑝 ∈ V (𝜎1 )        𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2 , R    𝜄 (𝜎2 )
  ⟨𝑝, 𝑡 ⟩ ∉ H(𝜎2 ) ∪ H (𝜎2 ) H ′ = H (𝜎2 ) ∪ { ⟨𝑝, 𝑡 ⟩ }    R ′ = R ∪ { ⟨𝑝, 𝑡 ⟩ }                          𝜎3 = 𝜎2 [ H = H ′ ]        𝑡 0 = fresh
                                                                                                   ′
                                                 𝜎1 ⊢ unfolding 𝑝 (𝑒 ) in 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎3 , R
                SEvalUnfoldingImplicitFailure
                𝑝 ∈ V (𝜎1 )  𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2 , R                     ¬𝜄 (𝜎2 )       ⟨𝑝, 𝑡 ⟩ ∉ H(𝜎2 ) ∪ H (𝜎2 )          𝑡 0 = fresh
                                                𝜎1 ⊢ unfolding 𝑝 (𝑒 ) in 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎2 , {⊥}


                   Fig. 8. Symbolic evaluation rules for unfolding expressions in Gradual Viper.




  Because the imprecision arose as a result of unfolding an imprecise predicate, which must now
be re-folded, we must also discard the optimistic assumptions that were made while it was unfolded.
Because the initial state was precise, the optimistic heap must be emptied, and we also must reset
the precise heap so that it once again contains the predicate instance and the fields it initially held.
H5 = H1     H5 = ∅
𝜎5 = ⟨⊤, H5 , H5 , 𝛾, 𝑎 > 0, ∅ ⟩     H5 = { ⟨ pos, 𝑡𝑥 ⟩, ⟨ val, 𝑡 𝑦 , 𝑏 ⟩ }   H5 = ∅ 𝛾 = [ x ↦→ 𝑡𝑥 , y ↦→ 𝑡 𝑦 ]

   Now, we can return the expression 𝑎 < 256 from the penultimate step.



3.3    Static Semantics for Pure Functions in Gradual Viper
To demonstrate our contribution in the static setting, in Figure 9 we use an example similar to the
fully-static example used in Section 2.4, but with an imprecise precondition.
14                                                                                                                 Torek et al.


                                           field val : Int

                                           function add ( x : Ref , y : Ref ): Int
                                              requires ? * acc ( y . val )
                                              ensures ( y . val < 0) || ( result >= x . val )
                                              { x . val + y . val }

                                           method caller (...)
                                             requires ...
                                             ensures ...
                                           {
                                               ... add (x , y ) ...
                                           }


                             Fig. 9. Example of pure function with imprecise precondition.


  To demonstrate the behavior of the imprecise precondition, we assume an initial symbolic heap
H(𝜎1 ) = {⟨val, 𝑡 𝑦 , 𝑏⟩, ⟨val, 𝑡𝑧 , 𝑐⟩} as in the previous example. Although 𝑡𝑧 again isn’t used in our
code sample, we include it to highlight the intricacies of the gradual case and its interaction with
the heap. Again, we start with a precise symbolic state with the aforementioned heap and variable
mappings.
𝜎1 = ⟨⊥, H1 , H1 , 𝛾, true, ∅ ⟩   H1 = { ⟨ val, 𝑡 𝑦 , 𝑏 ⟩, ⟨ val, 𝑡𝑧 , 𝑐 ⟩ }   H1 = ∅ 𝛾 = [ x ↦→ 𝑡𝑥 , y ↦→ 𝑡 𝑦 ]

   We evaluate the function arguments, resulting in the same symbolic state. However, as described
in Section 3.1, the form of the evaluation judgement has changed to include an additional set of
run-time checks accumulated through evaluation. In this case, the sets are both empty because
evaluation only requires looking up these variables in the symbolic environment. Note that, even
though we don’t have a heap chunk corresponding to 𝑥 .val, we can evaluate 𝑥 itself since we are
only looking up the underlying value 𝑡𝑥 in the symbolic environment, not accessing a field of 𝑡𝑥 .
𝜎 1 ⊢ 𝑥 ⇓ 𝑡𝑥 ⊣ 𝜎 1 , ∅       𝜎1 ⊢ 𝑦 ⇓ 𝑡 𝑦 ⊣ 𝜎1 , ∅

  We must take a snapshot of the heap locations used during evaluation to pass as an implicit
parameter; however, since the state during evaluation is imprecise, the verifier can make optimistic
assumptions about ownership of any fields that are then checked at run-time. To account for this
possibility, the symbolic footprint of an imprecise specification captures the entire heap, including
the unused heap chunk ⟨val, 𝑡𝑧 , 𝑐⟩.
J? ∗ acc (𝑦.val )K𝜎1 = H1

   To ensure that the precondition holds in the initial state (which is still precise), we again consume
the precondition. Because an imprecise specification might represent access to any field, consuming
an imprecise formula empties both the precise and optimistic heaps and ends in an imprecise state
(reprsented by ⊤). Note that, although the consume operation generally may produce a run-time
check, the resulting run-time check set here is empty since 𝑦.val is the only field mentioned so far
and access to it is statically proven.
𝜎1 ⊢ ? ∗ acc (𝑦.val ) ▷ 𝜎2 , ∅
𝜎2 = ⟨⊤, H2 , H2 , 𝛾, true, ∅ ⟩   H2 = ∅      H2 = ∅ 𝛾 = [ x ↦→ 𝑡𝑥 , y ↦→ 𝑡 𝑦 ]

  So that we have a suitable environment to evaluate the function’s body, we must now produce
the function’s precondition. This adds a heap chunk corresponding to the accessibility predicate
acc(𝑦.val) back into the precise heap, but the resulting state is still imprecise.
𝜎2 ⊢ ? ∗ acc (𝑦.val ) ◁ 𝜎3
Gradually Verifying Unfolding Expressions & Pure Functions                                                                                                   15


𝜎3 = ⟨⊤, H3 , H3 , 𝛾, true, ∅ ⟩          H3 = { ⟨ val, 𝑡 𝑦 , 𝑏 ′ ⟩ }    H3 = ∅ 𝛾 = [ x ↦→ 𝑡𝑥 , y ↦→ 𝑡 𝑦 ]

   However, 𝑏 ≠ 𝑏 ′ because consuming and producing resulted in new symbolic values instead
of the ones used in the original symbolic state. To ensure that the final constraints in the path
condition are expressed in terms of known symbolic values, we revert these to refer to those from a
previous state. Note that, unlike the previous example, we can’t directly reset to H1 since this would
provide static access to the field chunk ⟨val, 𝑡𝑧 , 𝑐⟩, even though the initial heaps were emptied
after consuming and access to 𝑡𝑧 .val was never obtained again through the produce.
H4 = { ⟨ 𝑓 , 𝑡𝑒 , 𝑡 ′ ⟩ : ⟨ 𝑓 , 𝑡𝑒 , 𝑡 ⟩ ∈ H(𝜎3 ), ⟨ 𝑓 , 𝑡𝑒 , 𝑡 ′ ⟩ ∈ H(𝜎1 ) }
𝜎4 = ⟨⊤, H4 , H4 , 𝛾, true, ∅ ⟩          H4 = { ⟨ val, 𝑡 𝑦 , 𝑏 ⟩ }     H4 = ∅ 𝛾 = [ x ↦→ 𝑡𝑥 , y ↦→ 𝑡 𝑦 ]

  Now, we proceed to evaluation of the function body, which is where the imprecision of the
symbolic state comes into play. Since the field 𝑥 .val isn’t available in the precise heap and we are
currently in an imprecise state, the verifier creates a new heap chunk ⟨val, 𝑡𝑥 , 𝑎⟩, adds this to the
optimistic heap H5 , and assumes that ownership of the required field will hold. This also adds the
run-time check ⟨𝑡𝑥 , val⟩ to the set of run-time checks at the end, which will check ownership of
the field val of object 𝑡𝑥 at this point during execution.
𝜎4 [ V = { add } ] ⊢ 𝑥 .val + 𝑦.val ⇓ 𝑎 + 𝑏 ⊣ 𝜎5 , { ⟨𝑡𝑥 , val ⟩ }
𝜎5 = ⟨⊤, H5 , H5 , 𝛾, true, { add } ⟩          H5 = { ⟨ val, 𝑡 𝑦 , 𝑏 ⟩ }     H5 = { ⟨ val, 𝑡𝑥 , 𝑎⟩ } 𝛾 = [ x ↦→ 𝑡𝑥 , y ↦→ 𝑡 𝑦 ]    R = { ⟨𝑡𝑥 , val ⟩ }

   Then, axiomatizing the return value and post-condition is the same as in the fully-precise case.
add (𝑎, 𝑏, 𝑠 ) = fresh
axiomatize𝜎5 [ add (𝑎, 𝑏, 𝑠 ) ] ( (𝑦.val < 0) || ( result >= 𝑥 .val ) ) = (𝑏 < 0) || ( add (𝑎, 𝑏, 𝑠 ) >= 𝑎)

𝜎6 = ⟨⊤, H6 , H6 , 𝛾, ( add (𝑎, 𝑏, 𝑠 ) == 𝑎 + 𝑏 ) && ( (𝑏 < 0) || ( add (𝑎, 𝑏, 𝑠 ) >= 𝑎) ), ∅⟩             H6 = { ⟨ val, 𝑡 𝑦 , 𝑏 ⟩ }   H6 = { ⟨ val, 𝑡𝑥 , 𝑎⟩ }
𝛾 = [ x ↦→ 𝑡𝑥 , y ↦→ 𝑡 𝑦 ]     R = { ⟨𝑡𝑥 , val ⟩ }

   When evaluating a pure function with an imprecise precondition, the final symbolic state after
evaluation remains imprecise; although this breaks a previous assumption by Zimmerman et
al. [32] that evaluation will not change the precision of a state, once imprecise assumptions are
introduced to a state, it should remain imprecise. This assumption arose only because the previous
formalization didn’t address features like pure functions that rely on the evaluation judgement
while directly interacting with imprecision.
   Overall, this process is captured by the symbolic evaluation rules in Figure 11. Notably, our
handling of recursive pure functions interacts differently with imprecise preconditions or imprecise
initial states; since recursive calls to the same function aren’t evaluated directly, the post-condition
of a recursive pure function may rely on optimistic assumptions that haven’t yet been made. For
instance, let us consider the example in Figure 10. When sum is called for the second time, no
optimistic assumptions will be made since the body isn’t called and the post-condition isn’t directly
produced.


                                                  field val : Int
                                                  field next : Ref

                                                  function sum ( node : Ref ): Int
                                                      requires         ?
                                                      ensures x.val <= result
                                                      { ( node != null ) ? node . val + sum ( node . next ) : 0 }


                          Fig. 10. Example of recursive pure function with imprecise precondition.
16                                                                                                                                  Torek et al.


           SEvalFunctionExplicit
                                                    𝑓 ∉ V (𝜎1 )             𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2 , R 1
             𝑥 = func_params( 𝑓 )         𝑠 = Jfunc_pre( 𝑓 )K𝜎2                𝜎2 [𝛾 = 𝛾 (𝜎2 ) [𝑥 ↦→ 𝑡 ] ] ⊢ func_pre( 𝑓 ) ▷ 𝜎3 , R 2
                   𝜎3 ⊢ func_pre( 𝑓 ) ◁ 𝜎4            H′ = { ⟨ 𝑓 , 𝑡𝑒 , 𝑡 ′ ⟩ : ⟨𝑓 , 𝑡𝑒 , 𝑡 ⟩ ∈ H(𝜎4 ), ⟨ 𝑓 , 𝑡𝑒 , 𝑡 ′ ⟩ ∈ H(𝜎2 ) }
                                   H ′ = { ⟨ 𝑓 , 𝑡𝑒 , 𝑡 ′ ⟩ : ⟨ 𝑓 , 𝑡𝑒 , 𝑡 ⟩ ∈ H (𝜎4 ), ⟨ 𝑓 , 𝑡𝑒 , 𝑡 ′ ⟩ ∈ H (𝜎2 ) }
                 𝜎4 [H = H′ , H = H ′ , V = V (𝜎3 ) ∪ { 𝑓 } ] ⊢ func_body( 𝑓 ) ⇓ 𝑡 ′ ⊣ 𝜎5 , R 3                      𝑓 (𝑡, 𝑠 ) = fresh
            𝜎6 = 𝜎2 [𝜄 = 𝜄 (𝜎5 ), H = H (𝜎5 ), 𝑔 = 𝑔 (𝜎2 ) && ( 𝑓 (𝑡, 𝑠 ) == 𝑡 ′ ) && axiomatize𝜎 [ 𝑓 (𝑡, 𝑠 ) ] (func_post( 𝑓 ) ) ]
                                                        𝜎1 ⊢ 𝑓 (𝑒 ) ⇓ 𝑓 (𝑡, 𝑠 ) ⊣ 𝜎6 , R 1 ∪ R 2 ∪ R 3
 SEvalFunctionImplicit
  𝑓 ∈ V (𝜎1 )        𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2 , R 1      𝑥 = func_params( 𝑓 )          𝑠 = Jfunc_pre( 𝑓 )K𝜎2       𝑠 ′ = Jfunc_post( 𝑓 )K𝜎2
         H ′ = H (𝜎2 ) ∪ (𝑠 ′ \ H(𝜎2 ) )        𝜎2 [𝛾 = 𝛾 (𝜎2 ) [𝑥 ↦→ 𝑡 ] ] ⊢ func_pre( 𝑓 ) ▷ 𝜎3 , R 2      𝑓 (𝑡, 𝑠 ) = fresh
 𝜎4 = 𝜎2 [𝜄 = 𝜄 (𝜎3 ), H = H ′ , 𝑔 = 𝑔 (𝜎2 ) && axiomatize𝜎 [ 𝑓 (𝑡, 𝑠 ) ] (func_post( 𝑓 ) ) ]    R 3 = { ⟨𝑡𝑒 , 𝑓 ⟩ : ⟨ 𝑓 , 𝑡𝑒 , 𝑡 ⟩ ∈ 𝑠 ′ }
                                                        𝜎1 ⊢ 𝑓 (𝑒 ) ⇓ 𝑓 (𝑡, 𝑠 ) ⊣ 𝜎4 , R 1 ∪ R 2 ∪ R 3


                  Fig. 11. Symbolic evaluation rules for pure function applications in Gradual Viper.


   In this case, we must take the symbolic footprint of the post-condition, add any missing fields to
the optimistic heap, and add the necessary run-time checks to the final result of evaluation. When
we pass the symbolic state to the symbolic footprint, we must ensure we pass it in an imprecise
state so that any of the necessary fields can still be obtained without being statically proven. After
this step, we can axiomatize the post-condition as usual.
𝑠 ′ = Jfunc_post( sum )K𝜎 [𝜄=⊤] = J𝑥 .valK𝜎 [𝜄=⊤] = { ⟨ val, 𝑡𝑥 , 𝑎⟩ }
R ′ = { ⟨𝑡𝑒 , 𝑓 ⟩ : ⟨ 𝑓 , 𝑡𝑒 , 𝑡 ⟩ ∈ 𝑠 ′ } = { ⟨𝑡𝑥 , val ⟩ }     H ′ = H ∪ (𝑠 ′ \ H) = { ⟨ val, 𝑡𝑥 , 𝑎⟩ }

     This behavior is exhibited in the SEvalPureImplicit rule in Figure 11.

3.4     Dynamic Semantics
Because proving that static verification is sound also requires providing semantics for execution
and because our static verification scheme results in run-time checks, specifying the execution
semantics is necessary to formalizing implementation. Consequently, our extensions to the dynamic
semantics (Figures 12 and 13) govern the evaluation, the framing checks and the footprints of
unfolding expressions and pure function applications.
    The EvalUnfolding rule, which describes the runtime evaluation of an unfolding expression,
evaluates the inner expression without using the predicate instance. Because Gradual C0 uses
equirecursive semantics at run time, it is not necessary to unfold the predicate to gain ownership
of additional fields while evaluating the expression as the predicate instance will already be fully
unrolled and the fields will already be accessible.
    In addition to the evaluation rule, the dynamic semantics also include the framing rule and the
definition of the exact footprint for unfolding expressions. The framing rule, FrameUnfolding,
gives the conditions where the evaluation of an unfolding expression is well-defined; similarly
to framing rules for other types of assertions, this checks that all the requisite memory locations
are accessible. However, this also performs an additional check that the predicate assertion holds,
which poses significant challenges in proving soundness since other framing checks rely solely on
ownership. The exact footprint defines the set of memory locations accessed to assert and frame the
unfolding expression; because the assertion relies on evaluating the expression and framing relies
on the predicate assertion, the exact footprint contains both the exact footprint of the predicate
instance and the exact footprint of the inner expression.
    Similarly for pure functions, the EvalFunction rule directly evaluates the body. At run time,
it isn’t necessary to annotate the function body with the same implicit dependency on the heap.
Gradually Verifying Unfolding Expressions & Pure Functions                                                                              17


      EvalUnfolding                                      FrameUnfolding
              ⟨𝐻, 𝜌 ⟩ ⊢ 𝑒 0 ⇓ 𝑣                          ⟨𝐻, 𝛼, 𝜌 ⟩ ⊢frmI 𝑝 (𝑒 )        ⟨𝐻, 𝛼, 𝜌 ⟩ ⊨ 𝑝 (𝑒 )       ⟨𝐻, 𝛼, 𝜌 ⟩ ⊢frm 𝑒 0
      ⟨𝐻, 𝜌 ⟩ ⊢ unfolding 𝑝 (𝑒 ) in 𝑒 0 ⇓ 𝑣                               ⟨𝐻, 𝛼, 𝜌 ⟩ ⊢frm unfolding 𝑝 (𝑒 ) in 𝑒 0
                                  Tunfolding 𝑝 (𝑒 ) in 𝑒 0 U ⟨𝐻 , 𝜌⟩ = T𝑝 (𝑒 )U ⟨𝐻 , 𝜌⟩ ∪ T𝑒 0 U⟨𝐻 , 𝜌⟩


                    Fig. 12. Dynamic evaluation and framing rules for unfolding expressions


                    EvalFunction
                    𝑥 = params( 𝑓 )          ⟨𝐻, 𝜌 ⟩ ⊢ 𝑒 ⇓ 𝑣        𝜌 ′ = [𝑥 ↦→ 𝑣 ]       ⟨𝐻, 𝜌 ′ ⟩ ⊢ body( 𝑓 ) ⇓ 𝑣 ′
                                                                                 ′
                                                          ⟨𝐻, 𝜌 ⟩ ⊢ 𝑓 (𝑒 ) ⇓ 𝑣
                           FrameFunction
                           ⟨𝐻, 𝛼, 𝜌 ⟩ ⊢frmI pre( 𝑓 )          ⟨𝐻, 𝛼, 𝜌 ⟩ ⊨ pre( 𝑓 )       ⟨𝐻, 𝛼, 𝜌 ⟩ ⊢frm 𝑒
                                                          ⟨𝐻, 𝛼, 𝜌 ⟩ ⊢frm 𝑓 (𝑒 )
                                      Ø
                  T𝑓 (𝑒 )U⟨𝐻 , 𝜌⟩ =       T𝑒U ⟨𝐻 , 𝜌⟩ ∪ Tfunc_pre( 𝑓 )U ⟨𝐻 , [𝑥 ↦→𝑣 ]⟩ ∪ Tfunc_body( 𝑓 )U ⟨𝐻 , [𝑥 ↦→𝑣 ]⟩
                                             where 𝑥 = params( 𝑓 ) and ⟨𝐻, 𝜌 ⟩ ⊢ 𝑒 ⇓ 𝑣


                        Fig. 13. Dynamic evaluation and framing rules for pure functions


The framing rule for pure functions relies on the precondition holding, similarly to how unfolding
expressions rely on the predicate assertion holding, and the exact footprint for pure function
applications depends on the arguments and the precondition to represent the minimal set of
locations the function may access. However, the maximal footprint differs depending on whether
the precondition is imprecise; if the precondition is imprecise, then the maximal footprint is the
entire set of permissions since it may implicitly assume access to new fields.

3.5    Correspondence
To prove soundness, it is necessary to specify how states of the verifier correspond to states at
run time and how run-time checks behave dynamically. Mapping between verification states and
dynamic states requires mapping between symbolic and concrete values. The primary mechanism
that Zimmerman et al. [32] use to do so is corresponding valuations. This valuation is a partial
function mapping symbolic values to concrete values for a specific program trace, starting from the
valuation function defined by Khoo et al. [13]. The initial valuation function is written as 𝑉 , and the
corresponding valuation after evaluating an expression under dynamic heap 𝐻 and environment
𝜌 is written as 𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R | 𝐻, 𝜌]. This expands upon the initial valuation by mapping
additional symbolic values to concrete values based on the result of evaluation. By chaining these
together, we can obtain a valuation corresponding to a full program trace with all the resultant
mappings between symbolic and concrete values.
   For a dynamic state to model a static state 𝜎 under a certain valuation 𝑉 , the dynamic environment
𝜌 must model the symbolic store 𝛾 (𝜎) under 𝑉 and the dynamic heap 𝐻 and permission set 𝛼 must
model the precise heap H and optimistic heap H under 𝑉 . This is notated as ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎.
   To define the corresponding valuation for SEvalUnfoldingPrecise, SEvalUnfoldingImpre-
ciseA, and SEvalUnfoldingImpreciseB, we simply follow the steps in the symbolic evaluation
rule because symbolic and concrete evaluation proceed in lockstep. For SEvalUnfoldingImplic-
itImprecise, the same approach wouldn’t work; since the expression isn’t actually being evaluated
statically, we rely on the result of run time evaluation instead (see the appendix for details). The
cases for functions are similar.
18                                                                                          Torek et al.


  Additionally, our design of unfolding expressions for Gradual Viper changed the definition of
the optimistic heap so that it is able to hold both predicate instances and heap locations rather
than just heap locations. Accordingly, when formalizing these changes, it was necessary to change
the definition of correspondence between the optimistic heap and the dynamic heap to assert that
each of the predicate instances holds in the corresponding dynamic state. This fits alongside the
previous definition’s requirements that field values align with those in the dynamic heap and that
each field is included in the permission set of the dynamic state. These updated definitions are in
the appendix.

4    Soundness
To show that the verifier only accepts programs which meet their specifications, we expand upon
the proof of soundness provided by Zimmerman et al. [32], who derive and prove a formulation of
soundness from the progress-preservation formulation commonly used in type systems [31].
  In these theorems, we use the following notation:
 • A dynamic state Γ is either the abstract symbol init, the abstract symbol final, or a pair ⟨𝐻, S⟩
   of a heap 𝐻 and a stack S.
 • A verification state Σ is either the abstract symbol init, the abstract symbol final, or a triple
           ˜ containing a symbolic state, a statement to execute, and a post-condition to be proven
    ⟨𝜎, 𝑠, 𝜙⟩
   after execution.
 • The guard judgement Σ ⇀ 𝜎 ′ ⊣ R, Θ determines that run-time check set R must be satisfied at
   state 𝜎 ′ with exclusion frame Θ to continue symbolic execution.
 • The run-time assertion judgement ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R represents that each run-time check in R
   succeeds under heap 𝐻 , permission set 𝛼, and valuation 𝑉 ′ .
 • The set of permissions in heap 𝐻 necessary to satisfy symbolic permission set Θ is given by
   𝑉 LΘM𝐻 .
  The definition of progress is split into two theorems: first, dynamic execution will continue
when the run-time checks corresponding to the current path through the program are satisfied, and
second, there exists a set of run-time checks corresponding to any valid path condition. Together,
these imply that dynamic execution will only halt if a run-time check fails.
Theorem 1 (Progress, part 1). Let Γ be some dynamic state validated by Σ and valuation 𝑉 . If Σ ⇀
𝜎 ′ ⊣ R, Θ with corresponding valuation 𝑉 ′ extending 𝑉 , 𝑉 ′ (𝑔(𝜎 ′ )) = true, and ⟨𝐻, 𝛼 (Γ)⟩ ⊢𝑉 ′ R
then
                                     Π ⊢ Γ, 𝑉 ′ LΘM𝐻 (Γ) → Γ ′
for some Γ ′ .
Theorem 2 (Progress, part 2). Let Γ be some well-formed dynamic state validated by Σ and
valuation 𝑉 . Then if Γ ≠ final and ⟨𝐻 (Γ), 𝛼⟩ ⊢𝑉 ′ R,
                                            Σ ⇀ 𝜎 ′, R, Θ
for some 𝜎 ′ , R, Θ such that 𝑉 ′ (𝑔(𝜎 ′ )) = true where 𝑉 ′ is the corresponding valuation extending
𝑉 ′.
  The definition of preservation is similar to the original formulation: when there is a dynamic
execution step to be taken from a valid dynamic state, the resulting dynamic state will also be valid.
Theorem 3 (Preservation). Let ⟨𝐻, S⟩ be some dynamic state validated by Σ and valuation 𝑉
for some program Π. If Σ ⇀ 𝜎 ′ ⊣ R, Θ with 𝑉 ′ = 𝑉 [Σ ⇀ 𝜎 ′ ⊣ R, Θ | 𝐻 ], 𝑉 ′ (𝑔(𝜎 ′ )) = true,
⟨𝐻, 𝛼 (S)⟩ ⊢𝑉 ′ R, and ⟨𝐻, S⟩, 𝑉 ′ LΘM𝐻 → ⟨𝐻 ′, S ′ ⟩ then Γ ′ = ⟨𝐻 ′, S ′ ⟩ is a valid state.
Gradually Verifying Unfolding Expressions & Pure Functions                                          19


   The full proof of soundness is structured as a set of lemmas for each of the fundamental operations
in the static verifier, culminating in proofs of progress and preservation. Previously, the proof
was structured using lemmas for each of the fundamental operations, culminating in the proof of
progress and preservation. In this structure, Zimmerman et al. [33] first proved lemmas relating
to expressions and operations on them such as evaluation and framing. However, incorporating
pure functions and unfolding expressions into this framework results in a distinct issue. Previously
the syntax forms for expressions didn’t rely on formulas at all, instead exclusively using simpler
forms like field accesses, binary operations, unary operations, literals, and variables. However,
unfolding expressions are a type of expression that rely on predicates, which are formulas, and pure
functions have preconditions, which are formulas. Accordingly, expressions that perform induction
on expressions now rely on those that perform induction on formulas, which in turn rely on those
that perform induction on expressions since formulas include heap-dependent expressions. Similarly,
defining symbolic evaluation for these constructs uses the produce and consume judgements, which
are defined in terms of symbolic evaluation.
   For example, in the proof the following are written as separate theorems. In prior work, the
second of these theorems depended on the first but not vice versa. However, because of how we
mix formulas and expressions, they rely on each other.
Theorem. If ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 and 𝛼 ⊆ 𝛼 ′ , then ⟨𝐻, 𝛼 ′, 𝜌⟩ ⊢frm 𝑒.
Theorem. If ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE 𝜙˜ and 𝛼 ⊂ 𝛼 ′ , then ⟨𝐻, 𝛼 ′, 𝜌⟩ ⊢frmE 𝜙.
                                                                    ˜
  However, to demonstrate the logical soundness of our proof, we can interpret these separate but
mutually-recursive theorems as the following single theorem.
Theorem. Let 𝑥 ∈ Expr ∪ Formula
                             ˜        and 𝛼 ⊆ 𝛼 ′ . Then, if 𝑥 ∈ Expr and if ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑥, then
⟨𝐻, 𝛼 , 𝜌⟩ ⊢frm 𝑥. If 𝑥 ∈ Formula and if ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE 𝑥, then ⟨𝐻, 𝛼 ′, 𝜌⟩ ⊢frmE 𝑥.
     ′                    ˜
  Conceptually, this theorem can be proved by induction on the size of the term. Our formalization
uses this intuition but concretely realizes it via mutual induction over the previous decoupled
theorems.

5   Related Work
Gradual verification was originally inspired by gradual typing [25], where type annotations are
optional and missing annotations are backed by checks at run time. Accordingly, previous formu-
lations of gradual verification [5, 29] draw on work from gradual typing such as the Abstracting
Gradual Typing methodology from Garcia et al. [9].
   The original formulation of gradual verification did not have any support for unfolding expres-
sions; Wise et al.’s extension [29] supports unfolding formulae, which are more restricted than
unfolding expressions since they can only appear in specifications and predicate bodies. Similarly,
although Mutlu [18] designed an approach for handling pure functions in gradual verification based
on the approach in Silicon [24], this work lacks a proof of soundness. However, our design is instead
inspired by that of Smans et al. [27] for its higher level of abstraction. Gradual verification systems
without these features using weakest liberal precondition reasoning have been previously proven
sound [29] and mechanized in Rocq [5]. However, these proofs of soundness are not applicable to
Gradual Viper verifier because it is built on top of the Viper symbolic execution backend.
   We found that unfolding expressions and pure functions are used extensively in real-world code
bases verified using symbolic execution verifiers, often in conjunction – for example, in the router
for the VerifiedSCION architecture and the verified Go standard library, which are both verified
using Gobra [30]. Our work is therefore a critical building block for extending gradual verification
to support verifying realistic programs written in mainstream programming languages.
20                                                                                            Torek et al.


   Many static verifiers based on symbolic execution, such as Chalice [15], lack formal semantics
and proofs of soundness. A notable exception to this is VeriFast, which is a static verifier for C, Rust,
and Java based on symbolic execution [11]. However, VeriFast is based on separation logic rather
than implicit dynamic frames, meaning heap ownership and contents are specified simultaneously
and unfolding expressions are unnecessary. Another notable exception is Viper; Dardinier et al. [6]
proved the soundness of the Viper verification infrastructure by providing a formal framework for
proving the soundness of translational verifiers based on separation logic that can use more than one
verification backend and applying this framework to Viper. However, this only addresses a subset of
Viper’s features not including unfolding expressions or pure functions. Similarly, Parthasarathy et
al. [20] provide semantics for a subset of Viper’s features to automatically validate translations into
the Viper IVL; however, this subset again does not include unfolding expressions or pure functions
and their method focuses on the Boogie verification condition generation backend rather than the
symbolic execution backend for Viper.
   Previous work by Summers and Drossopoulou has connected equirecursive and isorecursive
interpretations of predicates in the context of implicit dynamic frames [28], but treated the di-
chotomy as a result of the difference between theory and implementation. In contrast, Wise et al.
[29] connected isorecursive and equirecursive interpretations in the context of gradual verification
because of how it combines static and dynamic verification and the connection between symbolic
and concete values.

6    Future Work
One limitation of our work is its handling of recursive pure functions and recursive unfolding
expressions, resulting in incompleteness. Formalizing the behavior of the Silicon symbolic execution
verifier, which better handles recursion for pure functions using SMT axioms to improve quantifier
triggering strategies, would result in a more complete treatment of pure functions that is closer to
the implementation.
   Several other features that are available in the Viper verification backend have not yet been
implemented or formalized for gradual verification. For example, fractional permissions have been
implemented [16] but not formalized, and quantified permissions have been neither implemented
nor formalized. Adding these features to the gradual verification ecosystem expands the range of
programs that can be verified; for example, adding quantified permissions enables verifications of
programs that use data structures such as arrays or graphs.
   Although the underlying verifications primitives from Viper are sufficiently expressive as part
of an intermediate verification language, directly exposing these primitives in the Gradual C0
front-end is not a suitable level of abstraction for realistic usable verification. To make gradual
verification more practical, we have the long-term goal of incorporating it into a verifier for a
language with a substructural type system, such as Prusti for Rust [4] or the SnaKt uniqueness type
system and verifier for Kotlin [22]. Substructural type systems such as Rust’s type system provide
information that allow the verifier to automatically generate auxiliary specifications, such as
folding and unfolding predicates, reducing the specification burden on the developer [4]. Therefore,
introducing more features from Viper to the gradual verification ecosystem ensures that we have a
sound and practical foundation with the tools needed for such an extension.
   Although the initial semantics and properties of gradual verification were mechanized in Rocq,
these are no longer applicable to Gradual C0 due to the use of symbolic execution rather than weakest
liberal preconditions. The semantics and proof of soundness for Gradual C0 have not been formalized
using a proof assistant. However, Dardinier et al. [6] provide a formal framework for proving the
soundness of translational separation logic verifiers mechanized in the Isabelle/HOL proof assistant.
Since this framework accounts for using different verification back-ends and different front-end
Gradually Verifying Unfolding Expressions & Pure Functions                                                               21


languages, this could be expanded to include gradual verification using the gradual version of the
Silicon symbolic execution backend and the gradual version of the Silver intermediate representation
language for Viper. Incorporating the formalization of gradual verification into the mechanized
proof could make it easier to expand upon the formal system for gradual verification, discover
possible errors in the proofs, and verify that the implementation corresponds to the formal system.

7   Conclusion
In this paper, we provide the formal semantics for the evaluation of unfolding expressions and
pure function applications in gradual verification by extending the formalization provided by
Zimmerman et al. [32], as well as an extension to the proof of soundness to include the semantics
for unfolding expressions and pure functions.
   By formalizing and proving the soundness of gradually-verified unfolding expressions and pure
function applications, we demonstrate the soundness of both Gradual C0 and the underlying sym-
bolic execution backend for Viper. Overall, introducing unfolding expressions and pure functions
to the gradual verification ecosystem ensures that gradual verification becomes more practical for
verifying real-world programs while still remaining sound.

Acknowledgments
We thank Conrad Zimmerman and Chanhee Cho for their valuable feedback. Additionally, we
thank Doruk Alp Mutlu and Craig Liu for their valuable contributions to the gradual verification
ecosystem.
   This work was supported by the National Security Agency under the Continuous Reasoning
with Gradual Verification grant, by the National Science Foundation under Grant No. CCF-2447499
(https://www.nsf.gov/awardsearch/show-award?AWD_ID=2447499), and by Meta through the
Research Experiences for Undergraduates in Software Engineering program at Carnegie Mellon
University. Any opinions, findings, conclusions, or recommendations are those of the authors
and do not necessarily reflect the views of the National Security Agency, the National Science
Foundation, or Meta.

References
 [1] Rob Arnold. 2010. C0, an Imperative Programming Language for Novice Computer Scientists. Master’s thesis. Department
     of Computer Science, Carnegie Mellon University. http://reports-archive.adm.cs.cmu.edu/anon/2010/CMU-CS-10-
     145.pdf
 [2] Linard Arquint, Malte Schwerhoff, Vaibhav Mehta, and Peter Müller. 2023. A Generic Methodology for the Modular
     Verification of Security Protocol Implementations. In Proceedings of the 2023 ACM SIGSAC Conference on Computer and
     Communications Security (Copenhagen, Denmark) (CCS ’23). Association for Computing Machinery, New York, NY,
     USA, 1377–1391. doi:10.1145/3576915.3623105
 [3] Linard Arquint, Felix A. Wolf, Joseph Lallemand, Ralf Sasse, Christoph Sprenger, Sven N. Wiesner, David Basin, and
     Peter Müller. 2023. Sound Verification of Security Protocols: From Design to Interoperable Implementations. In 2023
     IEEE Symposium on Security and Privacy (SP). IEEE, 1077–1093. doi:10.1109/SP46215.2023.10179325
 [4] Vytautas Astrauskas, Peter Müller, Federico Poli, and Alexander J. Summers. 2019. Leveraging Rust types for modular
     specification and verification. Proc. ACM Program. Lang. 3, OOPSLA, Article 147 (Oct. 2019), 30 pages. doi:10.1145/
     3360573
 [5] Johannes Bader, Jonathan Aldrich, and Éric Tanter. 2018. Gradual Program Verification. In Verification, Model Checking,
     and Abstract Interpretation. Springer, Los Angeles, CA, USA, 25–46. doi:10.1007/978-3-319-73721-8_2
 [6] Thibault Dardinier, Michael Sammler, Gaurav Parthasarathy, Alexander J. Summers, and Peter Müller. 2025. Formal
     Foundations for Translational Separation Logic Verifiers. Proc. ACM Program. Lang. 9, POPL, Article 20 (Jan. 2025),
     31 pages. doi:10.1145/3704856
 [7] Jenna DiVincenzo, Ian McCormack, Conrad Zimmerman, Hemant Gouni, Jacob Gorenburg, Jan-Paul Ramos-Dávila,
     Mona Zhang, Joshua Sunshine, Éric Tanter, and Jonathan Aldrich. 2025. Gradual C0: Symbolic Execution for Gradual
     Verification. ACM Trans. Program. Lang. Syst. 46, 4, Article 14 (Jan. 2025), 57 pages. doi:10.1145/3704808
22                                                                                                                Torek et al.


 [8] Marco Eilers and Peter Müller. 2018. Nagini: A Static Verifier for Python. In Computer Aided Verification, Hana Chockler
     and Georg Weissenbacher (Eds.). Springer International Publishing, Cham, 596–603.
 [9] Ronald Garcia, Alison M. Clark, and Éric Tanter. 2016. Abstracting Gradual Typing. In Proceedings of the 43rd Annual
     ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (St. Petersburg, FL, USA) (POPL ’16).
     Association for Computing Machinery, New York, NY, USA, 429–442. doi:10.1145/2837614.2837670
[10] Priyam Gupta. 2025. Increasing the Expressiveness of a Gradual Verifier. arXiv:2507.13533 [cs.PL] https://arxiv.org/
     abs/2507.13533
[11] Bart Jacobs, Jan Smans, Pieter Philippaerts, Frédéric Vogels, Willem Penninckx, and Frank Piessens. 2011. VeriFast: A
     Powerful, Sound, Predictable, Fast Verifier for C and Java. In NASA Formal Methods, Mihaela Bobaru, Klaus Havelund,
     Gerard J. Holzmann, and Rajeev Joshi (Eds.). Springer, Berlin, Heidelberg, 41–55. doi:10.1007/978-3-642-20398-5_4
[12] Adrian Jenny. 2023.        Verifying Go’s Standard Library.         Practical Work Report. ETH Zürich.              https:
     //ethz.ch/content/dam/ethz/special-interest/infk/chair-program-method/pm/documents/Education/Theses/
     Adrian_Jenny_PW_Report.pdf.
[13] Yit Phang Khoo, Bor-Yuh Evan Chang, and Jeffrey S. Foster. 2010. Mixing type checking and symbolic execution.
     SIGPLAN Not. 45, 6 (June 2010), 436–447. doi:10.1145/1809028.1806645
[14] Conradin Laux. 2025.           Verifying Parts of the Go Standard Library.              Bachelor Thesis. ETH Zürich.
     https://ethz.ch/content/dam/ethz/special-interest/infk/chair-program-method/pm/documents/Education/Theses/
     Conradin_Laux_BS_Thesis.pdf.
[15] K. Rustan M. Leino, Peter Müller, and Jan Smans. 2009. Verification of Concurrent Programs with Chalice. In
     Foundations of Security Analysis and Design V: FOSAD 2007/2008/2009 Tutorial Lectures. Springer, Berlin, Heidelberg,
     195–222. doi:10.1007/978-3-642-03829-7_7
[16] Craig Liu. 2024. Design of Fractional Permissions for a Gradual Verifier. In Companion Proceedings of the 2024 ACM
     SIGPLAN International Conference on Systems, Programming, Languages, and Applications: Software for Humanity
     (Pasadena, CA, USA) (SPLASH Companion ’24). Association for Computing Machinery, New York, NY, USA, 40–42.
     doi:10.1145/3689491.3689972
[17] Peter Müller, Malte Schwerhoff, and Alexander J. Summers. 2016. Viper: A Verification Infrastructure for Permission-
     Based Reasoning. In Proceedings of the 17th International Conference on Verification, Model Checking, and Abstract
     Interpretation - Volume 9583 (St. Petersburg, FL, USA) (VMCAI 2016). Springer, Berlin, Heidelberg, 41–62. doi:10.1007/978-
     3-662-49122-5_2
[18] Doruk Alp Mutlu. 2025. Expanding Specification Capabilities of a Gradual Verifier with Pure Functions. doi:10.48550/
     arXiv.2511.22075 arXiv:2511.22075 [cs.PL].
[19] Matthew Parkinson and Gavin Bierman. 2005. Separation logic and abstraction. SIGPLAN Not. 40, 1 (Jan. 2005),
     247–258. doi:10.1145/1047659.1040326
[20] Gaurav Parthasarathy, Thibault Dardinier, Benjamin Bonneau, Peter Müller, and Alexander J. Summers. 2024. To-
     wards Trustworthy Automated Program Verifiers: Formally Validating Translations into an Intermediate Verification
     Language. Proceedings of the ACM on Programming Languages 8, PLDI (June 2024), 1510–1534. doi:10.1145/3656438
[21] João C. Pereira, Tobias Klenze, Sofia Giampietro, Markus Limbeck, Dionysios Spiliopoulos, Felix A. Wolf, Marco Eilers,
     Christoph Sprenger, David Basin, Peter Müller, and Adrian Perrig. 2024. Protocols to Code: Formal Verification of a
     Next-Generation Internet Router. arXiv:2405.06074 [cs.CR] https://arxiv.org/abs/2405.06074
[22] Francesco Protopapa. 2024. Verifying Kotlin Code with Viper by Controlling Aliasing. Master’s Thesis. Università degli
     studi di Padova. https://thesis.unipd.it/retrieve/c1ccf1f6-8073-4b42-abb7-51af9e3518a2/thesis-pdfA.pdf.
[23] John C. Reynolds. 2002. Separation Logic: A Logic for Shared Mutable Data Structures. In Proceedings of the 17th
     Annual IEEE Symposium on Logic in Computer Science (LICS ’02). IEEE Computer Society, USA, 55–74.
[24] Malte Schwerhoff. 2016. Advancing Automated, Permission-based Program Verification Using Symbolic Execution. Ph. D.
     Dissertation. ETH Zürich.
[25] Jeremy G. Siek and Walid Taha. 2007. Gradual Typing for Objects. In ECOOP 2007 – Object-Oriented Programming.
     Springer, Berlin, Germany, 2–27. doi:10.1007/978-3-540-73589-2_2
[26] Jan Smans, Bart Jacobs, and Frank Piessens. 2009. Implicit Dynamic Frames: Combining Dynamic Frames and
     Separation Logic. In ECOOP 2009 – Object-Oriented Programming. Springer, Genova, Italy, 148–172. doi:10.1007/978-3-
     642-03013-0_8
[27] Jan Smans, Bart Jacobs, and Frank Piessens. 2010. Heap-Dependent Expressions in Separation Logic. In Formal
     Techniques for Distributed Systems, John Hatcliff and Elena Zucca (Eds.). Springer, Berlin, Heidelberg, 170–185. doi:10.
     1007/978-3-642-13464-7_14
[28] Alexander J. Summers and Sophia Drossopoulou. 2013. A Formal Semantics for Isorecursive and Equirecursive State
     Abstractions. In ECOOP 2013 – Object-Oriented Programming. Springer, Montpellier, France, 129–153. doi:10.1007/978-
     3-642-39038-8_6
Gradually Verifying Unfolding Expressions & Pure Functions                                                                 23


[29] Jenna Wise, Johannes Bader, Cameron Wong, Jonathan Aldrich, Éric Tanter, and Joshua Sunshine. 2020. Gradual
     verification of recursive heap data structures. Proc. ACM Program. Lang. 4, OOPSLA, Article 228 (Nov. 2020), 28 pages.
     doi:10.1145/3428296
[30] Felix A. Wolf, Linard Arquint, Martin Clochard, Wytse Oortwijn, João C. Pereira, and Peter Müller. 2021. Gobra:
     Modular Specification and Verification of Go Programs. In Computer Aided Verification: 33rd International Conference,
     CAV 2021, Virtual Event, July 20–23, 2021, Proceedings, Part I. Springer, Berlin, Heidelberg, 367–379. doi:10.1007/978-3-
     030-81685-8_17
[31] Andrew K. Wright and Matthias Felleisen. 1994. A Syntactic Approach to Type Soundness. Information and Computation
     115, 1 (1994), 38–94. doi:10.1006/inco.1994.1093
[32] Conrad Zimmerman, Jenna DiVincenzo, and Jonathan Aldrich. 2024. Sound Gradual Verification with Symbolic
     Execution. Proc. ACM Program. Lang. 8, POPL, Article 85 (Jan. 2024), 30 pages. doi:10.1145/3632927
[33] Conrad Zimmerman, Jenna DiVincenzo, and Jonathan Aldrich. 2024. Sound Gradual Verification with Symbolic
     Execution. Proceedings of the ACM on Programming Languages 8, POPL (Jan. 2024), 2547–2576. https://arxiv.org/abs/
     2311.07559
24                                               Torek et al.


                                    Appendices
     A    Grammar                                        25
     B    Run-time Semantics                             26
     B.1    Definitions                                  26
     B.2    Evaluation                                   27
     B.3    Formulas                                     28
     B.4    Footprints                                   28
     B.5    Framing                                      29
     B.6    Assertions                                   31
     B.7    Execution                                    32
     B.8    Reachable transitions                        33
     C    Symbolic Execution                             34
     C.1    Definitions                                  34
     C.2    Valuations                                   35
     C.3    Footprints                                   35
     C.4    Correspondence                               36
     C.5    Run-time checks                              37
     C.6    Evaluation                                   37
     C.7    Produce                                      40
     C.8    Consume                                      41
     C.9    Execute                                      42
     C.10   Verification states                          44
     C.11   Guards                                       44
     C.12   Valid states                                 46
     D    Soundness                                      46
     D.1    Cross-cutting lemmas                         46
     D.2    Evaluation                                   50
     D.3    Produce                                      60
     D.4    Consume                                      65
     D.5    Progress                                     73
     D.6    Preservation                                 78
Gradually Verifying Unfolding Expressions & Pure Functions                                        25


A   Grammar
In the following appendices, our changes from Zimmerman et al. [33] are highlighted light gray.
 program F S P F M s                             Program definition
 S           F 𝑆{T 𝑓 }                           Struct definition
 P           F 𝑝 (T x) = 𝜙˜                      Predicate definition
 F           F 𝑇 𝑔(𝑇 𝑥) Ψ 𝑒                      Pure function definition
 Ψ           F requires 𝜙˜ ensures 𝑒             Pure function contract
 M           F 𝑇 𝑚(𝑇 𝑥) Φ 𝑠                      Method definition
 Φ           F requires 𝜙˜ ensures 𝜙˜            Method contract
 T           F 𝑆 | int | bool | char Type
 s           F s; s                              Statement sequence
               | skip                            No-op
               | 𝑥 =𝑒                            Variable assignment
               | 𝑥 .𝑓 = 𝑒                        Field assignment
               | 𝑥 = alloc(𝑆)                    Allocation
               | 𝑥 = 𝑚(𝑒)                        Method invocation
               | assert 𝜙˜                       Assertion
               | if 𝑒 then 𝑠 else 𝑠              Conditional
                                      ˜
               | while 𝑒 invariant 𝜙 do 𝑠        Loop
               | fold 𝑝 (𝑒)                      Fold predicate
               | unfold 𝑝 (𝑒)                    Unfold predicate
 e           F 𝑙 | 𝑥 | 𝑒.𝑓 | 𝑒 ⊕ 𝑒               Expression
               | 𝑒 || 𝑒 | 𝑒 && 𝑒 | ! 𝑒
               | unfolding 𝑝 (𝑒) in 𝑒            Unfolding expression
               | 𝑔(𝑒)                            Pure function call
 x           F result | 𝑖𝑑                       Variable
 l           F 𝑛 | 𝑐                             Value
               | null | true | false
 𝜙 ˜         F ?∗𝜙 | 𝜙                           Gradual formula
 𝜙           F 𝜙 ∗ 𝜙 | 𝑝 (𝑒) | 𝑒                 Precise formula
               | if 𝑒 then 𝜙 else 𝜙
               | acc(𝑒.𝑓 )
    Where 𝑛 ∈ Z, 𝑐 ∈ Char, 𝑖𝑑 ∈ Identifier, 𝑓 ∈ Field, 𝑚 ∈ Method, 𝑝 ∈ Predicate, 𝑔 ∈
Function, ⊕ ∈ {+, −, <, >, ≤, ≥, =}
Definition 1. A program is well-formed if all the following requirements are satisified:
 • It is properly typed.
 • All loop invariants, method pre-conditions, function pre-conditions, and method post-conditions
   are specifications (definition 4).
 • The free variables of any method are a subset of its parameters.
 • The special variable result is not a free variable of any method.
 • No parameters appear on the left side of a variable assignment.
 • Formulas in pre-conditions only reference parameters.
 • Formulas in post-conditions only reference parameters and the special variable result.
 • If a pre-condition is imprecise, the post-condition is also imprecise.
 • Function bodies and post-conditions are framed (section B.5) by their pre-conditions and function
   post-conditions can be proven to hold for the result.
26                                                                                       Torek et al.


B     Run-time Semantics
B.1     Definitions
The rules in the following section reference an ambient program with elements denoted as follows:

 • Structs: 𝑆 ∈ Struct
 • Predicates: 𝑝 ∈ Predicate

 • Functions: 𝑔 ∈ Function

 • Methods: 𝑚 ∈ Method
 • Types: 𝑇 ∈ Type
 • Variables: 𝑥 ∈ Var
 • Field identifiers: 𝑓 ∈ Field
 • Locations (opaque values): ℓ ∈ Location
 • Literals (integers, characters, booleans, null): 𝑙 ∈ Literal
 • Values: 𝑣 ∈ Value = Location ∪ Literal
 • Gradual formulas: 𝜙˜ ∈ Formula
                            ˜
 • Precise formulas: 𝜙 ∈ Formula
 • Statements: 𝑠 ∈ Stmt
 • Heap: 𝐻 : Location × Field → Value
 • Permissions: 𝛼 ∈ P (Location × Field)
 • Environment: 𝜌 : Var ⇀ Value

     The following functions are defined to access elements in the program:

 • default : Type → Value – Gets the default value of the given type (0, null, etc.)
 • struct : Struct → Field – Gets the list of fields from the declaration of the specified struct.
 • pre : Method → Formula
                        ˜      – Gets the precondition from the declaration of the specified
   method.
 • post : Method → Formula
                        ˜      – Gets the post-condition from the declaration of the specified
   method.
 • body : Method → Stmt – Gets the body from the declaration of the specified method.
 • params : Method → Var – Gets the list of parameters from the declaration of the specified
   predicate.
 • predicate : Predicate → Formula
                             ˜          – Gets the body from the declaration of the specified
   predicate.
 • predicate_params : Predicate → Var – Gets the list of parameters from the declaration of the
   specified predicate.

 • func_pre : Function → Formula
                            ˜         – Gets the precondition from the declaration of the specified
   pure function.
 • func_post : Function → Expr – Gets the post-condition, which is an expression rather than a
   formula, from the declaration of the specified pure function.
 • func_body : Function → Expr – Gets the body from the declaration of the specified pure
   function.
 • func_params : Function𝑡𝑜Var – Gets the list of parameters from the declaration of the specified
   pure function.
Gradually Verifying Unfolding Expressions & Pure Functions                                                27


B.2    Evaluation
The relation
                                                 ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣
denotes the evaluation of an expression 𝑒 ∈ Expr to a value 𝑣 ∈ Value where 𝐻 : Value × Field →
Value represents the heap, and 𝜌 : Var ⇀ Value represents the local variable environment.

                                                 EvalLiteral

                                                 ⟨𝐻, 𝜌⟩ ⊢ 𝑙 ⇓ 𝑙

                                              EvalVar

                                               ⟨𝐻, 𝜌⟩ ⊢ 𝑥 ⇓ 𝜌 (𝑥)
                                          EvalAndA
                                             ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ false
                                          ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 && 𝑒 2 ⇓ false
                                 EvalAndB
                                  ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ true         ⟨𝐻, 𝜌⟩ ⊢ 𝑒 2 ⇓ 𝑣 2
                                             ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 && 𝑒 2 ⇓ 𝑣 2
                                          EvalOrA
                                              ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ true
                                           ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 || 𝑒 2 ⇓ true
                                 EvalOrB
                                 ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ false          ⟨𝐻, 𝜌⟩ ⊢ 𝑒 2 ⇓ 𝑣 2
                                             ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑣 2
                                   EvalOp
                                    ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ 𝑣 1       ⟨𝐻, 𝜌⟩ ⊢ 𝑒 2 ⇓ 𝑣 2
                                          ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓ 𝑣 1 ⊕ 𝑣 2
                                               EvalNeg
                                                 ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣
                                               ⟨𝐻, 𝜌⟩ ⊢ ! 𝑒 ⇓ ¬𝑣
                                            EvalField
                                                 ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ ℓ
                                            ⟨𝐻, 𝜌⟩ ⊢ 𝑒.𝑓 ⇓ 𝐻 (ℓ, 𝑓 )

                                    EvalUnfolding
                                                ⟨𝐻, 𝜌⟩ ⊢ 𝑒 0 ⇓ 𝑣
                                     ⟨𝐻, 𝜌⟩ ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓ 𝑣
          EvalFunction
          𝑥 = params(𝑓 )         ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣          𝜌 ′ = [𝑥 ↦→ 𝑣]      ⟨𝐻, 𝜌 ′ ⟩ ⊢ body(𝑓 ) ⇓ 𝑣 ′
                                              ⟨𝐻, 𝜌⟩ ⊢ 𝑓 (𝑒) ⇓ 𝑣 ′
28                                                                                                     Torek et al.


B.3     Formulas
                                                           ˜
Formula is the set of all 𝜙 elements in the grammar, while Formula is the set of all 𝜙˜ elements in
the grammar.

Definition 2. An imprecise formula 𝜙˜ is any formula in Formula
                                                        ˜       of the form ? ∗ 𝜙 where
𝜙 ∈ Formula.
  Otherwise, a formula 𝜙 is precise and 𝜙 ∈ Formula.

Definition 3. A formula 𝜙˜ is completely precise if there is no 𝐻, 𝛼, 𝜌 such that AssertImprecise
                                                      ˜
applies at some step in the derivation of ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙.
  In other words, a completely precise formula is precise and all predicate bodies referenced in its
equi-recursive unrolling are also precise.

Definition 4. A formula 𝜙˜ is a specification if either 𝜙˜ is imprecise or 𝜙˜ is precise and self-framed
(definition 7).

B.4     Footprints
Definition 5. The exact footprint of a formula 𝜙˜ ∈ Formula,     ˜         denoted T𝜙U˜ ⟨𝐻, 𝜌 ⟩ , or of an
expression 𝑒, denoted T𝑒U ⟨𝐻, 𝜌 ⟩ , is the set of permissions that must be accessed when asserting 𝜙˜ or
evaluating 𝑒.
   By lemmas 4 and 11, if 𝜙˜ is a specification, this set is the lower bound of permissions that satisfy
 ˜
𝜙.

     The calculation of exact footprints is defined as follows:

                               T𝑙U ⟨𝐻, 𝜌 ⟩ := ∅
                              T𝑥U ⟨𝐻, 𝜌 ⟩ := ∅
                            T𝑒.𝑓 U ⟨𝐻, 𝜌 ⟩ := T𝑒U ⟨𝐻, 𝜌 ⟩ ; ⟨ℓ, 𝑓 ⟩                         if ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ ℓ
                       T𝑒 1 ⊕ 𝑒 2 U ⟨𝐻, 𝜌 ⟩ := T𝑒 1 U ⟨𝐻, 𝜌 ⟩ ∪ T𝑒 2 U ⟨𝐻, 𝜌 ⟩
                      T𝑒 1 || 𝑒 2 U ⟨𝐻, 𝜌 ⟩ := T𝑒 1 U ⟨𝐻, 𝜌 ⟩                          if ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ true
                      T𝑒 1 || 𝑒 2 U ⟨𝐻, 𝜌 ⟩ := T𝑒 1 U ⟨𝐻, 𝜌 ⟩ ∪ T𝑒 2 U ⟨𝐻, 𝜌 ⟩        if ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ false
                      T𝑒 1 && 𝑒 2 U ⟨𝐻, 𝜌 ⟩ := T𝑒 1 U ⟨𝐻, 𝜌 ⟩                         if ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ false
                      T𝑒 1 && 𝑒 2 U ⟨𝐻, 𝜌 ⟩ := T𝑒 1 U ⟨𝐻, 𝜌 ⟩ ∪ T𝑒 2 U ⟨𝐻, 𝜌 ⟩         if ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ true
                            T! 𝑒U ⟨𝐻, 𝜌 ⟩ := T𝑒U ⟨𝐻, 𝜌 ⟩
                         T? ∗ 𝜙U ⟨𝐻, 𝜌 ⟩ := T𝜙U ⟨𝐻, 𝜌 ⟩
                       T𝜙 1 ∗ 𝜙 2 U ⟨𝐻, 𝜌 ⟩ := T𝜙 1 U ⟨𝐻, 𝜌 ⟩ ∪ T𝜙 2 U ⟨𝐻, 𝜌 ⟩
                          T𝑝 (𝑒)U ⟨𝐻, 𝜌 ⟩ := Tpredicate(𝑝)U ⟨𝐻, [𝑥↦→𝑣 ] ⟩ ∪      if 𝑥 = predicate_params(𝑝)
                                              Ø
                                                  T𝑒U ⟨𝐻, 𝜌 ⟩                            and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣
      Tif 𝑒 then 𝜙 1 else 𝜙 2 U ⟨𝐻, 𝜌 ⟩ := T𝑒U ⟨𝐻, 𝜌 ⟩ ∪ T𝜙 1 U ⟨𝐻, 𝜌 ⟩                if ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ true
      Tif 𝑒 then 𝜙 1 else 𝜙 2 U ⟨𝐻, 𝜌 ⟩ := T𝑒U ⟨𝐻, 𝜌 ⟩ ∪ T𝜙 2 U ⟨𝐻, 𝜌 ⟩               if ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ false
                    Tacc(𝑒.𝑓 )U ⟨𝐻, 𝜌 ⟩ := T𝑒U ⟨𝐻, 𝜌 ⟩ ; ⟨ℓ, 𝑓 ⟩                            if ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ ℓ
Gradually Verifying Unfolding Expressions & Pure Functions                                                     29




      Tunfolding 𝑝 (𝑒) in 𝑒 0 U ⟨𝐻, 𝜌 ⟩ := T𝑝 (𝑒)U ⟨𝐻, 𝜌 ⟩ ∪ T𝑒 0 U ⟨𝐻, 𝜌 ⟩
                                           Ø
                      T𝑓 (𝑒)U ⟨𝐻, 𝜌 ⟩ :=       T𝑒U ⟨𝐻, 𝜌 ⟩ ∪                         if 𝑥 = func_params(𝑓 )
                                               Tfunc_pre(𝑓 )U ⟨𝐻, [𝑥↦→𝑣 ] ⟩ ∪             and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣
                                               Tfunc_body(𝑓 )U ⟨𝐻, [𝑥↦→𝑣 ] ⟩

Definition 6. The maximal footprint of a formula, denoted ⌊𝜙⌋    ˜ ⟨𝐻, 𝛼, 𝜌 ⟩ , is the set of all permissions
      ˜
that 𝜙 may represent in the context of a heap 𝐻 , permission set 𝛼, and variable environment 𝜌.
  The footprint of a completely precise formula (definition 3) is its exact footprint, while the
footprint of a formula which is not completely precise is the current set of permissions.
                                       (
                                          ˜             ˜
                        ˜ ⟨𝐻, 𝛼, 𝜌 ⟩ := T𝜙U ⟨𝐻, 𝜌 ⟩ if 𝜙 is completely precise
                       ⌊𝜙⌋
                                        𝛼           otherwise

B.5    Framing
The relation ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 denotes that 𝑒 ∈ Expr is framed by the permissions contained in
𝛼 ∈ P (Perm).

                                                 FrameLiteral

                                                 ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑙
                                                 FrameVar

                                                 ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑥
                                 FrameField
                                  ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒         ⟨𝐻, 𝛼, 𝜌⟩ ⊨ acc(𝑒.𝑓 )
                                                ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒.𝑓
                                   FrameOp
                                    ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1        ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 2
                                              ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1 ⊕ 𝑒 2
                                  FrameOrA
                                  ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ true          ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1
                                             ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1 || 𝑒 2
                    FrameOrB
                     ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ false          ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1         ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 2
                                             ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1 || 𝑒 2
                                 FrameAndA
                                  ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ false          ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1
                                             ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1 && 𝑒 2
                     FrameAndB
                     ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ true          ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1          ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 2
                                             ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1 && 𝑒 2
                                                FrameNeg
                                                 ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒
                                                ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm ! 𝑒
30                                                                                           Torek et al.



                 FrameUnfolding
                  ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmI 𝑝 (𝑒)        ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝑝 (𝑒)       ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 0
                                ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm unfolding 𝑝 (𝑒) in 𝑒 0
               FrameFunction
                ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmI pre(𝑓 )        ⟨𝐻, 𝛼, 𝜌⟩ ⊨ pre(𝑓 )        ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒
                                           ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑓 (𝑒)

  The relation ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmI 𝜙 denotes that 𝜙 ∈ Formula is framed by the permissions in
𝛼 ∈ P (Perm) using an iso-recursive interpretation of predicates (i.e., without unrolling predicate
instances).

                                            IFrameExpression
                                             ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒
                                             ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmI 𝑒
                             IFrameConjunction
                              ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmI 𝜙 1        ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmI 𝜙 2
                                          ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmI 𝜙 1 ∗ 𝜙 2
                                           IFramePredicate
                                             ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒
                                           ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmI 𝑝 (𝑒)
                  IFrameConditionalA
                  ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ true           ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒        ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmI 𝜙 1
                                ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmI if 𝑒 then 𝜙 1 else 𝜙 2
                 IFrameConditionalB
                  ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ false          ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒        ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmI 𝜙 2
                                ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmI if 𝑒 then 𝜙 1 else 𝜙 2
                                      IFrameAcc
                                             ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒
                                      ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmI acc(𝑒.𝑓 )
   Define the relation ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE 𝜙 denotes that 𝜙 ∈ Formula is framed by the permissions
in 𝛼 ∈ P (Perm) using an equi-recursive interpretation of predicates (i.e., unrolling predicate
instances).

                                            EFrameExpression
                                             ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒
                                            ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE 𝑒
                             EFrameConjunction
                             ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE 𝜙 1         ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE 𝜙 2
                                          ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE 𝜙 1 ∗ 𝜙 2
      EFramePredicate
                                         ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒
      ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣      𝑥 = predicate_params(𝑝)       ⟨𝐻, 𝛼, [𝑥 ↦→ 𝑣]⟩ ⊢frmE predicate(𝑝)
                                           ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE 𝑝 (𝑒)
Gradually Verifying Unfolding Expressions & Pure Functions                                             31

                     EFrameConditionalA
                     ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ true           ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒        ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE 𝜙 1
                                     ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE if 𝑒 then 𝜙 1 else 𝜙 2

                    EFrameConditionalB
                    ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ false            ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒        ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE 𝜙 2
                                     ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE if 𝑒 then 𝜙 1 else 𝜙 2

                                           EFrameAcc
                                                 ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒
                                           ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE acc(𝑒.𝑓 )

Definition 7. A self-framed formula is a precise formula 𝜙 ∈ Formula such that for all 𝐻, 𝛼, 𝜌,

                                     ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙 =⇒ ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmI 𝜙 .

B.6    Assertions
The relation ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙˜ denotes the validity of 𝜙˜ ∈ Formula
                                                         ˜       for the state represented by
⟨𝐻, 𝛼, 𝜌⟩.

                                     AssertImprecise
                                      ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙          ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE 𝜙
                                                 ⟨𝐻, 𝛼, 𝜌⟩ ⊨ ? ∗ 𝜙

                                              AssertValue
                                               ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ true
                                                   ⟨𝐻, 𝛼, 𝜌⟩ ⊨ e

                                     AssertIfA
                                     ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ true          ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙 1
                                       ⟨𝐻, 𝛼, 𝜌⟩ ⊨ if 𝑒 then 𝜙 1 else 𝜙 2

                                  AssertIfB
                                     ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ false          ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙 2
                                       ⟨𝐻, 𝛼, 𝜌⟩ ⊨ if 𝑒 then 𝜙 1 else 𝜙 2

                                         AssertAcc
                                         ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ ℓ         ⟨ℓ, 𝑓 ⟩ ∈ 𝛼
                                             ⟨𝐻, 𝛼, 𝜌⟩ ⊨ acc(𝑒.𝑓 )

                 AssertConjunction
                 ⟨𝐻, 𝛼 1, 𝜌⟩ ⊨ 𝜙 1       ⟨𝐻, 𝛼 2, 𝜌⟩ ⊨ 𝜙 2        𝛼1 ∪ 𝛼2 ⊆ 𝛼      𝛼1 ∩ 𝛼2 = ∅
                                              ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙 1 ∗ 𝜙 2

         AssertPredicate
         𝑥 = predicate_params(𝑝)             ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣          ⟨𝐻, 𝛼, [𝑥 ↦→ 𝑣]⟩ ⊨ predicate(𝑝)
                                                 ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝑝 (𝑒)
32                                                                                                                   Torek et al.


B.7     Execution
Definition 8. A stack S is a list of the form
                                         ⟨𝛼𝑛 , 𝜌𝑛 , 𝑠𝑛 ⟩ · . . . · ⟨𝛼 1, 𝜌 1, 𝑠 1 ⟩ · nil
where 𝑛 ≥ 1, 𝛼𝑛 , · · · , 𝛼 1 are permission sets, 𝜌𝑛 , · · · , 𝜌 1 are variable environments, and 𝑠𝑛 , · · · , 𝑠 1
are statements.
  𝛼 (S), 𝜌 (S), and 𝑠 (S) may be used to denote the values 𝛼𝑛 , 𝜌𝑛 , and 𝑠𝑛 , respectively.
Definition 9. An exclusion frame 𝛼ˆ a set of permissions that may not be transferred to a
callee stack frame. This is necessary to ensure that the permissions represented by the imprecise
specifications of a callee cannot overlap with some predicate instance that is owned by the caller.
     Small-step execution is denoted by the judgement
                                                 ⟨𝐻, S⟩, 𝛼ˆ → ⟨𝐻 ′, S ′ ⟩
for stacks S, S ′ , heap 𝐻 , and exclusion frame 𝛼.
                                                 ˆ

                                  ExecSeq

                                  ⟨𝐻, ⟨𝛼, 𝜌, skip; 𝑠⟩ · S⟩, 𝛼ˆ → ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · S⟩
                         ExecAssign
                                        ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣             ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒
                          ⟨𝐻, ⟨𝛼, 𝜌, 𝑥 = 𝑒; 𝑠⟩ · S⟩, 𝛼ˆ → ⟨𝐻, ⟨𝛼, 𝜌 [𝑥 ↦→ 𝑣], 𝑠⟩ · S⟩
        ExecAssignField
                                                  ⟨𝐻, 𝜌⟩ ⊢ 𝑥 ⇓ ℓ
        ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣            ⟨𝐻, 𝛼, 𝜌⟩ ⊨ acc(𝑥 .𝑓 )   ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒                    𝐻 ′ = 𝐻 [⟨ℓ, 𝑓 ⟩ ↦→ 𝑣]
                             ⟨𝐻, ⟨𝛼, 𝜌, 𝑥 .𝑓 = 𝑒; 𝑠⟩ · S⟩, 𝛼ˆ → ⟨𝐻 ′, ⟨𝛼, 𝜌, 𝑠⟩ · S⟩
        ExecAlloc
        ℓ = fresh       𝑇 𝑓 = struct(𝑆)             𝐻 ′ = 𝐻 [⟨ℓ, 𝑓 ⟩ ↦→ default(𝑇 )]               𝛼 ′ = 𝛼 ∪ {⟨ℓ, 𝑓 ⟩}
                    ⟨𝐻, ⟨𝛼, 𝜌, 𝑥 = alloc(𝑆); 𝑠⟩ · S⟩, 𝛼ˆ → ⟨𝐻 ′, ⟨𝛼 ′, 𝜌 [𝑥 ↦→ ℓ], 𝑠⟩ · S⟩
     ExecCallEnter
                                       𝑥 = params(𝑚)       ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣
     ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒         𝜌 ′ = [𝑥 ↦→ 𝑣]            ˆ 𝜌 ′ ⟩ ⊨ pre(𝑚)
                                                ⟨𝐻, 𝛼 \ 𝛼,                                    𝛼 ′ = ⌊pre(𝑚)⌋ ⟨𝐻, 𝛼\𝛼,ˆ 𝜌 ′ ⟩
                                          ⟨𝐻, ⟨𝛼, 𝜌, 𝑦 = 𝑚(𝑒); 𝑠⟩ · S⟩, 𝛼ˆ
                                                        →
                         ⟨𝐻, ⟨𝛼 ′, 𝜌 ′, body(𝑚); skip⟩ · ⟨𝛼 \ 𝛼 ′, 𝜌, 𝑦 = 𝑚(𝑒); 𝑠⟩ · S⟩
        ExecCallExit
        ⟨𝐻, 𝛼 ′, 𝜌 ′ ⟩ ⊨ post(𝑚)         𝜌 ′′ = 𝜌 [𝑦 ↦→ 𝜌 ′ (result)]                𝛼 ′′ = 𝛼 ∪ ⌊post(𝑚)⌋ ⟨𝐻, 𝛼 ′ , 𝜌 ′ ⟩
                ⟨𝐻, ⟨𝛼 , 𝜌 , skip⟩ · ⟨𝛼, 𝜌, 𝑦 = 𝑚(𝑒); 𝑠⟩ · S⟩, 𝛼ˆ → ⟨𝐻, ⟨𝛼 ′′, 𝜌 ′′, 𝑠⟩ · S⟩
                         ′    ′

                             ExecAssert
                                              ⟨𝐻, 𝛼, 𝜌⟩ ⊨ ? ∗ 𝜙
                                               ˜ 𝑠⟩ · S⟩, 𝛼ˆ → ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · S⟩
                             ⟨𝐻, ⟨𝛼, 𝜌, assert 𝜙;
                 ExecIfA
                                      ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ true               ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒
                    ⟨𝐻, ⟨𝐻, 𝜌, if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠⟩ · S⟩, 𝛼ˆ → ⟨𝐻, ⟨𝐻, 𝜌, 𝑠 1 ; 𝑠⟩ · S⟩
Gradually Verifying Unfolding Expressions & Pure Functions                                                  33

                 ExecIfB
                                  ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ false            ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒
                 ⟨𝐻, ⟨𝐻, 𝜌, if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠⟩ · S⟩, 𝛼ˆ → ⟨𝐻, ⟨𝐻, 𝜌, 𝑠 2 ; 𝑠⟩ · S⟩
        ExecWhileEnter
        ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ true          ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒                ˆ 𝜌⟩ ⊨ 𝜙˜
                                                           ⟨𝐻, 𝛼 \ 𝛼,           𝛼 ′ = ⌊𝜙⌋ ˜ ⟨𝐻, 𝛼\𝛼,ˆ 𝜌 ⟩
                            ⟨𝐻, ⟨𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠 ′ ; 𝑠⟩ · S⟩, 𝛼ˆ
                                                         →
                 ⟨𝐻, ⟨𝛼 ′, 𝜌, 𝑠 ′ ; skip⟩ · ⟨𝛼 \ 𝛼 ′, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠 ′ ; 𝑠⟩ · S⟩
                ExecWhileSkip
                     ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ false   ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒                  ˆ 𝜌⟩ ⊨ 𝜙˜
                                                                    ⟨𝐻, 𝛼 \ 𝛼,
                ⟨𝐻, ⟨𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠 ′ ; 𝑠⟩ · S⟩, 𝛼ˆ → ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · S⟩
                   ExecWhileFinish
                                 ⟨𝐻, 𝛼 ′, 𝜌 ′ ⟩ ⊨ 𝜙˜ 𝛼 ′′ = 𝛼 ∪ ⌊𝜙⌋
                                                                 ˜ ⟨𝐻, 𝛼 ′ , 𝜌 ′ ⟩
                   ⟨𝐻, ⟨𝛼 ′, 𝜌 ′, skip⟩ · ⟨𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠 ′ ; 𝑠⟩ · S⟩, 𝛼ˆ
                                                     →
                            ⟨𝐻, ⟨𝛼 ′′, 𝜌 ′, while 𝑒 invariant 𝜙˜ do 𝑠 ′ ; 𝑠⟩ · S⟩
                           ExecFold

                           ⟨𝐻, ⟨𝛼, 𝜌, fold 𝑝 (𝑒); 𝑠⟩ · 𝑆⟩, 𝛼ˆ → ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · 𝑆⟩
                         ExecUnfold

                         ⟨𝐻, ⟨𝛼, 𝜌, unfold 𝑝 (𝑒); 𝑠⟩ · 𝑆⟩, 𝛼ˆ → ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · 𝑆⟩

B.8    Reachable transitions
Definition 10. An execution state Γ is either one of the abstract symbols final or init, or a pair
⟨𝐻, S⟩ of a heap 𝐻 and a stack S.
Definition 11. An execution state Γ is well-formed if Γ is either one of the abstract symbols init
or final, or of the form ⟨𝐻, ⟨𝛼𝑛 , 𝜌𝑛 , 𝑠𝑛 ⟩ · . . . · ⟨𝛼 1, 𝜌 1, 𝑠 1 ⟩ · nil⟩ and
 • 𝛼𝑖 ∩ 𝛼 𝑗 = ∅ for all 1 ≤ 𝑖 < 𝑗 ≤ 𝑛.
 • 𝑠𝑛 = 𝑠; skip for some statement 𝑠 or 𝑠𝑛 = skip.
 • For all 1 ≤ 𝑖 < 𝑛, 𝑠𝑖 = 𝑠; 𝑠 ′ ; skip or 𝑠𝑖 = 𝑠; skip for some statements 𝑠 and 𝑠 ′ where 𝑠 is of the
    form 𝑚(𝑒) for some 𝑚, 𝑒 or while 𝑒 invariant 𝜙˜ do 𝑠𝑏𝑜𝑑 𝑦 for some 𝑒, 𝜙,       ˜ 𝑠𝑏𝑜𝑑𝑦 .

   Examining the execution rules shows that well-formedness of states is preserved by the execution
rules defined above.
   A dynamic execution transition Γ → Γ ′ is reachable under a program Π, using the exclusion
       ˆ when the following judgement holds:
frame 𝛼,
                                                  Π ⊢ Γ, 𝛼ˆ → Γ ′
                                ExecInit

                                 ⟨𝑠, 𝑀, 𝑃, 𝑆⟩ ⊢ init, _ → ⟨∅, ⟨∅, ∅, 𝑠⟩ · nil⟩
                              ExecStep
                              Π ⊢ _, _ → ⟨𝐻, S⟩              ⟨𝐻, S⟩, 𝛼ˆ → ⟨𝐻 ′, S ′ ⟩
                                          Π ⊢ ⟨𝐻, S⟩, 𝛼ˆ → ⟨𝐻 ′, S ′ ⟩
                                   ExecFinal

                                    Π ⊢ ⟨_, ⟨_, _, skip⟩ · nil⟩, _ → final
34                                                                                                         Torek et al.


Definition 12. An execution state Γ is reachable from program Π if Γ = init or Π ⊢ _, _ → Γ.

C     Symbolic Execution
C.1    Definitions
Definition 13. A symbolic value 𝜈 ∈ SValue is an abstract value that represents an unknown
character, boolean, integer, or location value. We leave the concrete type of SValue undefined, but
assume that an infinite number of distinct new values can be produced by the fresh function.
Definition 14. A symbolic expression 𝑡 ∈ SExpr is a symbolic value or symbolic expressions
combined using operators. Note that the binary operators ⊕ are the same as in §A.
                     𝑡 ::= 𝜈   | 𝑙   |    !𝑡       |       𝑡 1 && 𝑡 2   |   𝑡 1 || 𝑡 2       |   𝑡1 ⊕ 𝑡2
Definition 15. A path condition 𝑔 ∈ SExpr is a symbolic expression consisting of conjuncts
added at every branch point during a particular symbolic execution path.
Definition 16. An imprecise flag 𝜄 ∈ {⊤, ⊥} is a flag that indicates whether a state is imprecise.
Definition 17. A symbolic evironment 𝛾 : Var ⇀ SExpr is a partial function mapping variable
names to symbolic expressions.
Definition 18. A field chunk ⟨𝑓 , 𝑡, 𝑡 ′ ⟩ ∈ SField denotes the mapping of the field 𝑓 of instance 𝑡
to the value 𝑡 ′ .
Definition 19. A predicate chunk ⟨𝑝, 𝑡⟩ ∈ SPredicate represents an isorecursive predicate 𝑝
with symbolically-evaluated arguments 𝑡.
Definition 20. A heap chunk ℎ ∈ SField ∪ SPredicate is either a field chunk or a predicate
chunk.
Definition 21. A precise symbolic heap (usually abbreviated as precise heap) H ∈ P (SField ∪
SPredicate) is a set of heap chunks where all heap chunks must occupy distinct heap locations at
run time.

Definition 22. An optimistic symbolic heap (usually abbreviated as optimistic heap) H ∈
P (SField ∪ SPredicate) is a set of field chunks and predicate chunks where distinct chunks may
coincide on the heap at run time (i.e. object references that are distinct symbolic expressions may
be represent the same object value at run time).
Definition 23. A visited set V ∈ P (Predicate ∪ Function) contains predicates that have
already been unfolded and pure functions that have already been evaluated during recursive
symbolic evaluation.

Definition 24. A symbolic permission 𝜃 ∈ SPerm represents a particular heap location or
predicate instance.
                                     𝜃 ::= ⟨𝑓 , 𝑡⟩ | ⟨𝑝, 𝑡⟩
A set of symbolic permissions is denoted by Θ.
Definition 25. A run-time check 𝑟 ∈ SCheck is a symbolic value that must be asserted at
run time, a symbolic permission whose access must be asserted at run time, a set of symbolic
permissions whose disjointness must be asserted at run time, or an unsatisfiable check.
                                𝑟 ::= 𝑡   |    𝜃       |      sep(Θ1, Θ2 )       |       ⊥
A set of run-time checks is denoted by R.
Gradually Verifying Unfolding Expressions & Pure Functions                                                    35


Definition 26. A symbolic state 𝜎 ∈ SState consists of an imprecise flag, a path condition, a
precise heap, an optimistic heap, a symbolic environment, and a visited set.
                                               𝜎 ::= ⟨𝜄, 𝑔, H, H, 𝛾, V⟩
𝜄 (𝜎), 𝑔(𝜎), H(𝜎), H (𝜎), 𝛾 (𝜎), and V (𝜎) each denote a reference to the respective component of 𝜎.

C.2    Valuations
In order to prove soundness with respect to the dynamic semantics, we must first define a corre-
spondence between the two representations.
Definition 27. A valuation 𝑉 : SValue ⇀ Value is a partial function mapping symbolic values
to concrete values.
  A base valuation 𝑉 : SValue ⇀ Value is implicitly extended to 𝑉 : SExpr ⇀ Value for all
possible symbolic expressions composed of literals and symbolic values in the domain of 𝑉 :
                               𝑉 (𝑙) := 𝑙
                        𝑉 (𝑡 1 + 𝑡 2 ) := 𝑉 (𝑡 1 ) + 𝑉 (𝑡 2 )
                        𝑉 (𝑡 1 - 𝑡 2 ) := 𝑉 (𝑡 1 ) − 𝑉 (𝑡 2 )
                        𝑉 (𝑡 1 * 𝑡 2 ) := 𝑉 (𝑡 1 ) · 𝑉 (𝑡 2 )
                                          𝑉 (𝑡 1 )
                        𝑉 (𝑡 1 / 𝑡 2 ) :=
                                          𝑉 (𝑡 2 )
                                          (
                                            true         if 𝑉 (𝑡 1 ) = 𝑉 (𝑡 2 )
                       𝑉 (𝑡 1 == 𝑡 2 ) :=
                                            false        otherwise
                                          (
                                            true         if 𝑉 (𝑡 1 ) = false
                             𝑉 (! 𝑡) :=
                                            false        otherwise
                                          (
                                            true         if 𝑉 (𝑡 1 ) = true or 𝑉 (𝑡 2 ) = true
                       𝑉 (𝑡 1 || 𝑡 2 ) :=
                                            false        otherwise
                                          (
                                            true         if 𝑉 (𝑡 1 ) = true and 𝑉 (𝑡 2 ) = true
                       𝑉 (𝑡 1 && 𝑡 2 ) :=
                                            false        otherwise
Definition 28. A symbolic expression 𝑡 1 implies another symbolic expression 𝑡 2 (denoted 𝑡 1 =⇒
𝑡 2 ) if, for all valuations for which 𝑉 (𝑡 1 ) and 𝑉 (𝑡 2 ) are defined, (𝑉 (𝑡 1 ) = true) =⇒ (𝑉 (𝑡 2 ) = true).

C.3    Footprints
𝑉 L𝜃 M𝐻 and 𝑉 LΘM𝐻 denote the footprint (i.e. set of permissions) necessary to satisfy the given
symbolic permission or symbolic permission set, respectively, given some heap 𝐻 .
                                 𝑉 L⟨𝑓 , 𝑡⟩M𝐻 := ⟨𝑉 (𝑡), 𝑓 ⟩
                                  𝑉 L⟨𝑝, 𝑡⟩M𝐻 := Tpredicate(𝑝)U ⟨𝐻, [𝑥↦→𝑉 (𝑡 ) ] ⟩
                                                 Ø
                                      𝑉 LΘM𝐻 :=     𝑉 L𝜃 M𝐻
                                                      𝜃 ∈Θ

                 ˜ 𝜎 represents the set of field chunks in the precise and imprecise heaps repre-
  Additionally, J𝜙K
sented by an imprecise specification. This is used when taking heap snapshots during the evaluation
36                                                                                                    Torek et al.


of pure function applications.
                            J𝑙K𝜎 = ∅
                           J𝑥K𝜎 = ∅
                         J𝑒.𝑓 K𝜎 = {⟨𝑓 , 𝑡𝑒 , 𝑡⟩}                                    where 𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ _, _
                                                                                     and 𝜎 ⊢ 𝑡𝑒 .𝑓 ⇓ 𝑡 ⊣ _, _
                   Jacc(𝑒.𝑓 )K𝜎 = {⟨𝑓 , 𝑡𝑒 , 𝑡⟩}                                     where 𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ _, _
                                                                                     and 𝜎 ⊢ 𝑡𝑒 .𝑓 ⇓ 𝑡 ⊣ _, _
                     J𝑒 1 ⊕ 𝑒 2 K𝜎 = J𝑒 1 K𝜎 ∪ J𝑒 2 K𝜎
                    J𝑒 1 || 𝑒 2 K𝜎 = J𝑒 1 K𝜎 ∪ J𝑒 2 K𝜎
                    J𝑒 1 && 𝑒 2 K𝜎 = J𝑒 1 K𝜎 ∪ J𝑒 2 K𝜎
                          J! 𝑒K𝜎 = J𝑒K𝜎
                       J? ∗ 𝜙K𝜎 = H(𝜎) ∪ H (𝜎)
                     J𝜙 1 ∗ 𝜙 2 K𝜎 = J𝜙 1 K𝜎 ∪ J𝜙 2 K𝜎
                        J𝑝 (𝑒)K𝜎 = Jpredicate(𝑝)K𝜎 [𝛾 =[𝑥↦→𝑡 ] ] ∪          where 𝑥 = predicate_params(𝑝)
                                     Ø
                                         J𝑒K𝜎 ∪ {⟨𝑝, 𝑡⟩}                                and 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ _, _
                       J𝑓 (𝑒)K𝜎 = Jfunc_pre(𝑓 )K𝜎 ∪
                                                                Ø
                                         Jfunc_body(𝑓 )K𝜎 ∪         J𝑒K𝜎
     Junfolding 𝑝 (𝑒) in 𝑒 0 K𝜎 = J𝑝 (𝑒)K𝜎 ∪ J𝑒 0 K𝜎

C.4     Correspondence
The relations ⟨𝐻, 𝛼⟩ 𝑉 H, ⟨𝐻, 𝛼⟩ 𝑉 H , 𝜌                 𝑉
                                                             𝛾, and ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 denote correspondence
between symbolic states and run-time states:
                                   def
                 ⟨𝐻, 𝛼⟩ 𝑉 H ⇐⇒ (∀ ⟨𝑓 , 𝑡, 𝑡 ′ ⟩ ∈ H : 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ )) ∧
                                         (∀ ⟨𝑓 , 𝑡, 𝑡 ′ ⟩ ∈ H : ⟨𝑉 (𝑡), 𝑓 ⟩ ∈ 𝛼) ∧
                                                                                                                (1)
                                         (∀ ⟨𝑝, 𝑡⟩ ∈ H : ⟨𝐻, 𝛼, [𝑥 ↦→ 𝑉 (𝑡)]⟩ ⊨ predicate(𝑝)) ∧
                                         (∀ ℎ 1, ℎ 2 ∈ H2 : ℎ 1 ≠ ℎ 2 =⇒ 𝑉 Lℎ 1 M𝐻 ∩ 𝑉 Lℎ 2 M𝐻 = ∅)
                                   def
                ⟨𝐻, 𝛼⟩ 𝑉 H ⇐⇒ (∀ ⟨𝑓 , 𝑡, 𝑡 ′ ⟩ ∈ H : 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ )) ∧
                                         (∀ ⟨𝑓 , 𝑡, 𝑡 ′ ⟩ ∈ H : ⟨𝑉 (𝑡), 𝑓 ⟩ ∈ 𝛼) ∧                              (2)
                                         (∀ ⟨𝑝, 𝑡⟩ ∈ H : ⟨𝐻, 𝛼, [𝑥 ↦→ 𝑉 (𝑡)]⟩ ⊨ predicate(𝑝))
                                   def
                        𝜌 𝑉 𝛾 ⇐⇒ ∀ 𝑥 ∈ dom(𝛾) : 𝜌 (𝑥) = 𝑉 (𝑡)                                                   (3)
                                   def
               ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 ⇐⇒ (⟨𝐻, 𝛼⟩ 𝑉 H(𝜎)) ∧
                                         (⟨𝐻, 𝛼⟩ 𝑉 H (𝜎)) ∧
                                                                                                                (4)
                                         (𝜌 𝑉 𝛾 (𝜎)) ∧
                                         (𝑉 (𝑔(𝜎)) = true)
Gradually Verifying Unfolding Expressions & Pure Functions                                        37


C.5    Run-time checks
The judgement ⟨𝐻, 𝛼⟩ ⊢𝑉 𝑟 denotes that a symbolic runtime check 𝑟 ∈ SCheck is satisfied at run
time by a heap 𝐻 and permission set 𝛼 through a valuation 𝑉 . Note that there is no rule for ⊥; by
design it can never be satisfied.
                                                  CheckValue
                                                  𝑉 (𝑡) = true
                                                      ⟨𝐻, 𝛼⟩ ⊢𝑉 𝑡
                                               CheckAcc
                                                 ⟨𝑉 (𝑡), 𝑓 ⟩ ∈ 𝛼
                                                ⟨𝐻, 𝛼⟩ ⊢𝑉 ⟨𝑓 , 𝑡⟩
                  CheckPred
                   𝑥 = predicate_params(𝑝)                  ⟨𝐻, 𝛼, [𝑥 ↦→ 𝑉 (𝑡)]⟩ ⊨ predicate(𝑝)
                                                ⟨𝐻, 𝛼⟩ ⊢𝑉 ⟨𝑝, 𝑡⟩
                                           CheckSep
                                            𝑉 LΘ1 M𝐻 ∩ 𝑉 LΘ2 M𝐻 = ∅
                                    ⟨𝐻, 𝛼⟩ ⊢𝑉 sep(Θ1, Θ2 )
  This judgement is naturally extended for a set of runtime checks R:
                                                      def
                                 ⟨𝐻, 𝛼⟩ ⊢𝑉 R ⇐⇒ ∀ 𝑟 ∈ R : ⟨𝐻, 𝛼⟩ ⊢𝑉 𝑟

C.6    Evaluation
The judgement
                                               𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R
denotes the evaluation of the expression 𝑒 ∈ Expr in the symbolic state 𝜎 ∈ SState. It yields the
symbolic expression 𝑡 ∈ SExpr, a new symbolic state 𝜎 ′ which must be satisfied to produce the
resulting value, and a set of run-time checks R ∈ P (SCheck).
   Note that for any given 𝜎, there may be multiple values of 𝑡, 𝜎 ′, R for which the relation is
satisfied. Therefore, the path condition of 𝜎 ′ must be satisfied before assuming that 𝑡 corresponds
to an actual value.
   Also note that unsatisfiable paths are not pruned during evaluation. These paths may be pruned
by checking the satisfiability of 𝑔(𝜎 ′ ).
   For a list of expressions 𝑒, 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R represents a sequence of judgements
                              𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, , · · · , 𝜎𝑛−1 ⊢ 𝑒𝑛 ⇓ 𝑡𝑛 ⊣ 𝜎𝑛 , R𝑛
where 𝜎0 = 𝜎, 𝑒 1, · · · , 𝑒𝑛 = 𝑒, and R = R 1 ∪ · · · ∪ R𝑛 .

                                                SEvalLiteral

                                                𝜎 ⊢ 𝑙 ⇓ 𝑙 ⊣ 𝜎, ∅
                                           SEvalVar

                                            𝜎 ⊢ 𝑥 ⇓ 𝛾 (𝜎) (𝑥) ⊣ 𝜎, ∅
                             SEvalOrA
                             𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, R          𝜎 ′′ = 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡 1 ]
                                           𝜎 ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑡 1 ⊣ 𝜎 ′′, R
38                                                                                                                 Torek et al.

                       SEvalOrB
                       𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, R 1          𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && ! 𝑡 1 ] ⊢ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′, R 2
                                            𝜎 ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′, R 1 ∪ R 2
                                SEvalAndA
                                𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, R          𝜎 ′′ = 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && ! 𝑡 1 ]
                                                   𝜎 ⊢ 𝑒 1 && 𝑒 2 ⇓ 𝑡 1 ⊣ 𝜎 ′′, R
                        SEvalAndB
                        𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, R 1          𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡 1 ] ⊢ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′, R 2
                                            𝜎 ⊢ 𝑒 1 && 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′, R 1 ∪ R 2
                                   SEvalOp
                                   𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, R 1          𝜎 ′ ⊢ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′, R 2
                                          𝜎 ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓ 𝑡 1 ⊕ 𝑡 2 ⊣ 𝜎 ′′, R 1 ∪ R 2
                                                     SEvalNeg
                                                        𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R
                                                      𝜎 ⊢ ! 𝑒 ⇓ ! 𝑡 ⊣ 𝜎 ′, R
                       SEvalField
                       𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′ , R           𝑔(𝜎 ′ ) =⇒ 𝑡𝑒 == 𝑡𝑒′           ⟨𝑓 , 𝑡𝑒′ , 𝑡⟩ ∈ H(𝜎 ′ )
                                                      𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′, R
     SEvalFieldOptimistic
                                                     𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′ , R
      𝑡𝑒′ , 𝑡 : ⟨𝑓 , 𝑡𝑒′ , 𝑡⟩ ∈ H(𝜎) ∧ 𝑔(𝜎 ′ )    =⇒ 𝑡𝑒′ == 𝑡𝑒     ⟨𝑓 , 𝑡𝑒′ , 𝑡⟩ ∈ H (𝜎)             𝑔(𝜎 ′ ) =⇒ 𝑡𝑒′ == 𝑡𝑒
                                                      𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′, R
        SEvalFieldImprecise
        𝜄 (𝜎)       𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′ , R   𝑡𝑒′ , 𝑡 : ⟨𝑓 , 𝑡𝑒′ , 𝑡⟩ ∈ H(𝜎) ∪ H (𝜎) ∧ 𝑔(𝜎 ′ ) =⇒ 𝑡𝑒′ == 𝑡𝑒
                                𝑡 = fresh    𝜎 ′′ = 𝜎 ′ [H = H (𝜎 ′ ); ⟨𝑓 , 𝑡𝑒 , 𝑡⟩]
                                                  𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′′, R; ⟨𝑡𝑒 , 𝑓 ⟩
      SEvalFieldFailure
                                                                ¬𝜄 (𝜎)
      𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′ , R          𝑡𝑒′ , 𝑡 : ⟨𝑓 , 𝑡𝑒′ , 𝑡⟩ ∈ H(𝜎) ∪ H (𝜎) ∧ 𝑔(𝜎 ′ ) =⇒ 𝑡𝑒′ == 𝑡𝑒              𝑡 = fresh
                                                                        ′
                                                     𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 , {⊥}

     SEvalUnfoldingPrecise
                 ¬𝜄 (𝜎1 )     𝑝 ∉ V (𝜎1 )        𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2, R 1     𝜎2 ⊢ 𝑝 (𝑒) ▷ 𝜎3, R 2
     𝑥 = predicate_params(𝑝)            𝜎3 [𝛾 = 𝛾 (𝜎3 ) [𝑥 ↦→ 𝑡], V = V (𝜎3 ) ∪ {𝑝}] ⊢ predicate(𝑝) ◁ 𝜎4
            𝜎4 [𝛾 = 𝛾 (𝜎3 )] ⊢ 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎5, R 3       𝜎6 = 𝜎5 [V = V (𝜎1 ), H = H(𝜎2 ), H = ∅]
                              𝜎1 ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎6, R 1 ∪ R 2 ∪ R 3
SEvalUnfoldingImpreciseA
𝜄 (𝜎1 )    predicate(𝑝) is precise      𝑝 ∉ V (𝜎1 )         𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2, R 1  𝜎2 ⊢ 𝑝 (𝑒) ▷ 𝜎3, R 2
   𝑥 = predicate_params(𝑝)        𝜎3 [𝛾 = 𝛾 (𝜎3 ) [𝑥 ↦→ 𝑡], V = V (𝜎3 ) ∪ {𝑝}] ⊢ predicate(𝑝) ◁ 𝜎4
                                  𝜎4 [𝛾 = 𝛾 (𝜎3 )] ⊢ 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎5, R 3
         H ′ = H (𝜎2 ) ∪ H (𝜎5 ) ∪ {⟨𝑝, 𝑡⟩}       𝜎6 = 𝜎5 [V = V (𝜎1 ), H = H(𝜎2 ), H = H ′ ]
                              𝜎1 ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎6, R 1 ∪ R 2 ∪ R 3
Gradually Verifying Unfolding Expressions & Pure Functions                                                          39




  SEvalUnfoldingImpreciseB
                                                       𝜄 (𝜎1 )
     predicate(𝑝) is imprecise           𝑝 ∉ V (𝜎1 )          𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2, R 1 𝜎2 ⊢ 𝑝 (𝑒) ▷ 𝜎3, R 2
  𝑥 = predicate_params(𝑝)              𝜎3 [𝛾 = 𝛾 (𝜎3 ) [𝑥 ↦→ 𝑡], V = V (𝜎3 ) ∪ {𝑝}] ⊢ predicate(𝑝) ◁ 𝜎4
  𝜎4 [𝛾 = 𝛾 (𝜎3 )] ⊢ 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎5, R 3     𝜎6 = 𝜎5 [V = V (𝜎1 ), H = H(𝜎2 ), H = H (𝜎2 ) ∪ {⟨𝑝, 𝑡⟩}]
                           𝜎1 ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎6, R 1 ∪ R 2 ∪ R 3


            SEvalUnfoldingImplicitPrecise
            𝑝 ∈ V (𝜎1 )        𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2, R         ⟨𝑝, 𝑡⟩ ∈ H(𝜎2 ) ∪ H (𝜎2 )         𝑡 0 = fresh
                                   𝜎1 ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎2, R


        SEvalUnfoldingImplicitImprecise
              𝑝 ∈ V (𝜎1 )     𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2, R     𝜄 (𝜎2 )    ⟨𝑝, 𝑡⟩ ∉ H(𝜎2 ) ∪ H (𝜎2 )
        H ′ = H (𝜎2 ) ∪ {⟨𝑝, 𝑡⟩}     R ′ = R ∪ {⟨𝑝, 𝑡⟩}      𝜎3 = 𝜎2 [H = H ′ ]     𝑡 0 = fresh
                                  𝜎1 ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎3, R ′


     SEvalUnfoldingImplicitFailure
     𝑝 ∈ V (𝜎1 )        𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2, R         ¬𝜄 (𝜎2 )      ⟨𝑝, 𝑡⟩ ∉ H(𝜎2 ) ∪ H (𝜎2 )         𝑡 0 = fresh
                                 𝜎1 ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎2, {⊥}


SEvalFunctionExplicit
                       𝑓 ∉ V (𝜎1 )      𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2, R 1            𝑥 = func_params(𝑓 )
               𝑠 = Jfunc_pre(𝑓 )K𝜎2           𝜎2 [𝛾 = 𝛾 (𝜎2 ) [𝑥 ↦→ 𝑡]] ⊢ func_pre(𝑓 ) ▷ 𝜎3, R 2
        𝜎3 ⊢ func_pre(𝑓 ) ◁ 𝜎4          H′ = {⟨𝑓 , 𝑡𝑒 , 𝑡 ′ ⟩ : ⟨𝑓 , 𝑡𝑒 , 𝑡⟩ ∈ H(𝜎4 ), ⟨𝑓 , 𝑡𝑒 , 𝑡 ′ ⟩ ∈ H(𝜎2 )}
                        H = {⟨𝑓 , 𝑡𝑒 , 𝑡 ′ ⟩ : ⟨𝑓 , 𝑡𝑒 , 𝑡⟩ ∈ H (𝜎4 ), ⟨𝑓 , 𝑡𝑒 , 𝑡 ′ ⟩ ∈ H (𝜎2 )}
                          ′

    𝜎4 [H = H , H = H ′, V = V (𝜎3 ) ∪ {𝑓 }] ⊢ func_body(𝑓 ) ⇓ 𝑡 ′ ⊣ 𝜎5, R 3
                ′
                                                                                                     𝑓 (𝑡, 𝑠) = fresh
𝜎6 = 𝜎2 [𝜄 = 𝜄 (𝜎5 ), H = H (𝜎5 ), 𝑔 = 𝑔(𝜎2 ) && (𝑓 (𝑡, 𝑠) == 𝑡 ′ ) && axiomatize𝜎 [𝑓 (𝑡, 𝑠)] (func_post(𝑓 ))]
                                   𝜎1 ⊢ 𝑓 (𝑒) ⇓ 𝑓 (𝑡, 𝑠) ⊣ 𝜎6, R 1 ∪ R 2 ∪ R 3


SEvalFunctionImplicit
                                                𝑓 ∈ V (𝜎1 )
𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2, R 1     𝑥 = func_params(𝑓 )            𝑠 = Jfunc_pre(𝑓 )K𝜎2     𝑠 ′ = Jfunc_post(𝑓 )K𝜎2
             ′              ′
          H = H (𝜎2 ) ∪ (𝑠 \ H(𝜎2 ))          𝜎2 [𝛾 = 𝛾 (𝜎2 ) [𝑥 ↦→ 𝑡]] ⊢ func_pre(𝑓 ) ▷ 𝜎3, R 2
𝑓 (𝑡, 𝑠) = fresh     𝜎4 = 𝜎2 [𝜄 = 𝜄 (𝜎3 ), H = H ′, 𝑔 = 𝑔(𝜎2 ) && axiomatize𝜎 [𝑓 (𝑡, 𝑠)] (func_post(𝑓 ))]
                                     R 3 = {⟨𝑡𝑒 , 𝑓 ⟩ : ⟨𝑓 , 𝑡𝑒 , 𝑡⟩ ∈ 𝑠 ′ }
                                   𝜎1 ⊢ 𝑓 (𝑒) ⇓ 𝑓 (𝑡, 𝑠) ⊣ 𝜎4, R 1 ∪ R 2 ∪ R 3

  The function axiomatize, used in evaluating pure function applications to convert function
postconditions into valid path conditions, is defined as follows.
40                                                                                                       Torek et al.




                axiomatize𝜎 [𝑓 (𝑡, 𝑠)] (result) = 𝑓 (𝑡, 𝑠)
                       axiomatize𝜎 [𝑓 (𝑡, 𝑠)] (𝑙) = 𝑙
                       axiomatize𝜎 [𝑓 (𝑡, 𝑠)] (𝑥) = 𝛾 (𝜎) (𝑥)
                     axiomatize𝜎 [𝑓 (𝑡, 𝑠)] (𝑒.𝑓 ) = 𝑡 where ⟨𝑓 , 𝑡𝑒 , 𝑡⟩ ∈ 𝑠 and 𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ _, _
                axiomatize𝜎 [𝑓 (𝑡, 𝑠)] (𝑒 1 ⊕ 𝑒 2 ) = axiomatize𝜎 [𝑓 (𝑡, 𝑠)] (𝑒 1 ) ⊕ axiomatize𝜎 [𝑓 (𝑡, 𝑠)] (𝑒 2 )
                axiomatize𝜎 [𝑓 (𝑡, 𝑠)] (𝑒 1 || 𝑒 2 ) = axiomatize𝜎 [𝑓 (𝑡, 𝑠)] (𝑒 1 ) || axiomatize𝜎 [𝑓 (𝑡, 𝑠)] (𝑒 2 )
                axiomatize𝜎 [𝑓 (𝑡, 𝑠)] (𝑒 1 && 𝑒 2 ) = axiomatize𝜎 [𝑓 (𝑡, 𝑠)] (𝑒 1 ) && axiomatize𝜎 [𝑓 (𝑡, 𝑠)] (𝑒 2 )
                     axiomatize𝜎 [𝑓 (𝑡, 𝑠)] (! 𝑒) = ! axiomatize𝜎 [𝑓 (𝑡, 𝑠)] (𝑒)
axiomatize𝜎 [𝑓 (𝑡, 𝑠)] (unfolding 𝑝 (𝑒) in 𝑒 0 ) = axiomatize𝜎 [𝑓 (𝑡, 𝑠)] (𝑒 0 )



C.7    Produce
The produce operation adds the information contained in a formula 𝜙˜ to the symbolic state 𝜎,
resulting in a new symbolic state 𝜎 ′ . This is denoted by the judgement
                                                    𝜎 ⊢ 𝜙 ◁ 𝜎′.


                                                SProduceImprecise
                                                𝜎 [𝜄 = ⊤] ⊢ 𝜙 ◁ 𝜎 ′
                                                  𝜎 ⊢ ? ∗ 𝜙 ◁ 𝜎′
                               SProduceExpr
                               𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _        𝜎 ′′ = 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡]
                                                    𝜎 ⊢ 𝑒 ◁ 𝜎 ′′
                             SProducePredicate
                             𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _         𝜎 ′′ = 𝜎 ′ [H = H(𝜎 ′ ); ⟨𝑝, 𝑡⟩]
                                                  𝜎 ⊢ 𝑝 (𝑒) ◁ 𝜎 ′′
                  SProduceField
                  𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′ , _       𝑡 = fresh        𝜎 ′′ = 𝜎 ′ [H = H(𝜎 ′ ); ⟨𝑓 , 𝑡𝑒 , 𝑡⟩]
                                                𝜎 ⊢ acc(𝑒.𝑓 ) ◁ 𝜎 ′′
                                         SProduceConjunction
                                         𝜎 ⊢ 𝜙1 ◁ 𝜎 ′        𝜎 ′ ⊢ 𝜙 2 ◁ 𝜎 ′′
                                                 𝜎 ⊢ 𝜙 1 ∗ 𝜙 2 ◁ 𝜎 ′′
                            SProduceIfA
                            𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _        𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡] ⊢ 𝜙 1 ◁ 𝜎 ′′
                                         𝜎 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ◁ 𝜎 ′′
                           SProduceIfB
                           𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _        𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && ! 𝑡] ⊢ 𝜙 2 ◁ 𝜎 ′′
                                         𝜎 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ◁ 𝜎 ′
Gradually Verifying Unfolding Expressions & Pure Functions                                                          41


C.8    Consume
The consume operation checks whether a formula 𝜙˜ is established by the symbolic state, collects
runtime checks that are minimally sufficient to establish 𝜙,˜ and removes permissions asserted in 𝜙˜
from the symbolic state. This is denoted by the judgement
                                       𝜎, 𝜎𝐸 ⊢ 𝜙˜ ▷ 𝜎 ′, R, Θ
where 𝜎 is the symbolic state containing the currently remaining permissions during consume,
and 𝜎𝐸 is the symbolic state containing the original permissions which may used for evaluating
expressions.

                                     SConsumeImprecision
                                               𝜎, 𝜎𝐸 [𝜄 = ⊤] ⊢ 𝜙 ▷ 𝜎 ′, R, Θ
                                     𝜎, 𝜎𝐸 ⊢ ? ∗ 𝜙 ▷ ⟨⊤, 𝑔(𝜎 ′ ), 𝛾 (𝜎 ′ ), ∅, ∅⟩, R, Θ
                                          SConsumeValue
                                           𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡 ⊣ _, R       𝑔(𝜎) =⇒ 𝑡
                                                    𝜎, 𝜎𝐸 ⊢ 𝑒 ▷ 𝜎, R, ∅
                                      SConsumeValueImprecise
                                      𝜄 (𝜎)       𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡 ⊣ _, R       𝑔(𝜎) =⇒
                                                                                Y 𝑡
                                         𝜎, 𝜎𝐸 ⊢ 𝑒 ▷ 𝜎 [𝑔 = 𝑔(𝜎) && 𝑡], R; 𝑡, ∅
                                     SConsumeValueFailure
                                     ¬𝜄 (𝜎)       𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡 ⊣ _, R        𝑔(𝜎) =⇒
                                                                                 Y 𝑡
                                                   𝜎, 𝜎𝐸 ⊢ 𝑒 ▷ 𝜎, {⊥}, ∅
                       SConsumePredicate
                       𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡 ⊣ _, R            𝑔(𝜎) =⇒ 𝑡 == 𝑡 ′ H(𝜎) = H′ ; ⟨𝑝, 𝑡 ′ ⟩
                                                                    Ø
                                 𝜎, 𝜎𝐸 ⊢ 𝑝 (𝑒) ▷ 𝜎 [H = H′, H = ∅],   R, {⟨𝑝, 𝑡⟩}
                  SConsumePredicateImprecise                               Û
                   𝜄 (𝜎)       𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡 ⊣ _, R       ⟨𝑝, 𝑡 ′ ⟩ ∈ H(𝜎) :    𝑔(𝜎) =⇒ 𝑡 == 𝑡 ′
                                                                   Ø
                              𝜎, 𝜎𝐸 ⊢ 𝑝 (𝑒) ▷ 𝜎 [𝐻 = ∅, H = ∅],       R; ⟨𝑝, 𝑡⟩, {⟨𝑝, 𝑡⟩}
                 SConsumePredicateFailure                                        Û
                  ¬𝜄 (𝜎)        𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡 ⊣ _, R          ⟨𝑝, 𝑡 ′ ⟩ ∈ H(𝜎) :       𝑔(𝜎) =⇒ 𝑡 == 𝑡 ′
                                              𝜎, 𝜎𝐸 ⊢ 𝑝 (𝑒) ▷ 𝜎, {⊥}, {⟨𝑝, 𝑡⟩}
              SConsumeAcc
                                       𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ _, R   𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒
              ⟨𝑓 , 𝑡𝑒′ , 𝑡⟩ ∈ H(𝜎)          ′
                                          H = remfp (H(𝜎), 𝜎, 𝑡𝑒 , 𝑓 ) H ′ = remf (H (𝜎), 𝜎, 𝑡𝑒 , 𝑓 )
                               𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ▷ 𝜎 [H = H′, H = H ′ ], R, {⟨𝑡𝑒 , 𝑓 ⟩}
   SConsumeAccOptimistic
                                                   𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ _, R
   𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒             ⟨𝑓 , 𝑡𝑒′ , 𝑡⟩ ∈ H(𝜎)       𝑡𝑒′ , 𝑡 : ⟨𝑓 , 𝑡𝑒 , 𝑡⟩ ∈ H(𝜎) ∧ (𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒 )
                              ′
                             H = remf (H(𝜎), 𝜎, 𝑡𝑒 , 𝑓 )       H ′ = remf (H (𝜎), 𝜎, 𝑡𝑒 , 𝑓 )
                               𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ▷ 𝜎 [H = H′, H = H ′ ], R, {⟨𝑡𝑒 , 𝑓 ⟩}
      SConsumeAccImprecise
      𝜄 (𝜎)        𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ _, R   𝑡𝑒′ , 𝑡 : ⟨𝑓 , 𝑡𝑒 , 𝑡⟩ ∈ H(𝜎) ∪ H (𝜎) ∧ (𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒 )
                           ′
                          H = remf (H(𝜎), 𝜎, 𝑡𝑒 , 𝑓 )        H ′ = remf (H (𝜎), 𝜎, 𝑡𝑒 , 𝑓 )
                           𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ▷ 𝜎 [H = H′, H = H ′ ], R; ⟨𝑡𝑒 , 𝑓 ⟩, {⟨𝑡𝑒 , 𝑓 ⟩}
42                                                                                                            Torek et al.

      SConsumeAccFailure
       ¬𝜄 (𝜎)     𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ _, R          𝑡𝑒′ , 𝑡 : ⟨𝑓 , 𝑡𝑒 , 𝑡⟩ ∈ H(𝜎) ∪ H (𝜎) ∧ (𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒 )
                                    𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ▷ 𝜎, {⊥}, {⟨𝑡𝑒 , 𝑓 ⟩}
                   SConsumeConjunction
                   𝜎, 𝜎𝐸 ⊢ 𝜙 1 ▷ 𝜎 ′, R 1, Θ1      𝜎 ′, 𝜎𝐸 [𝑔 = 𝑔(𝜎 ′ )] ⊢ 𝜙 2 ▷ 𝜎 ′′, R 2, Θ2
                                           (R 1 ∪ R 2 ) ∩ SPerm = ∅
                                   𝜎, 𝜎𝐸 ⊢ 𝜙 1 ∗ 𝜙 2 ▷ 𝜎 ′′, R 1 ∪ R 2, Θ1 ∪ Θ2
                   SConsumeConjunctionImprecise
                   𝜎, 𝜎𝐸 ⊢ 𝜙 1 ▷ 𝜎 ′, R 1, Θ1      𝜎 ′, 𝜎𝐸 [𝑔 = 𝑔(𝜎 ′ )] ⊢ 𝜙 2 ▷ 𝜎 ′′, R 2, Θ2
                                           (R 1 ∪ R 2 ) ∩ SPerm ≠ ∅
                          𝜎, 𝜎𝐸 ⊢ 𝜙 1 ∗ 𝜙 2 ▷ 𝜎 ′′, R 1 ∪ R 2 ; sep(Θ1, Θ2 ), Θ1 ∪ Θ2
           SConsumeConditionalA
            𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡 ⊣ _, R       𝑔′ = 𝑔(𝜎 ′ ) && 𝑡         𝜎 [𝑔 = 𝑔′ ], 𝜎𝐸 [𝑔 = 𝑔′ ] ⊢ 𝜙 1 ▷ 𝜎 ′, R ′, Θ
                                𝜎, 𝜎𝐸 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ▷ 𝜎 ′, R ∪ R ′, Θ
           SConsumeConditionalB
           𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡 ⊣ _, R        𝑔′ = 𝑔(𝜎 ′ ) && ! 𝑡        𝜎 [𝑔 = 𝑔′ ], 𝜎𝐸 [𝑔 = 𝑔′ ] ⊢ 𝜙 2 ▷ 𝜎 ′, R ′, Θ
                             𝜎, 𝜎𝐸 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ▷ 𝜎 ′, R ∪ R ′, Θ
     The functions remf , remfp , and alias are defined as follows:
                        remf (H, 𝜎, 𝑡, 𝑓 ) = {⟨𝑓 ′, 𝑡 ′, 𝑡 ′′ ⟩ ∈ H : ¬ alias(𝜎, 𝑡, 𝑓 , 𝑡 ′, 𝑓 ′ )}
                       remfp (H, 𝜎, 𝑡, 𝑓 ) = remf (H, 𝜎, 𝑡, 𝑓 ) ∪ {⟨𝑝, 𝑡⟩ ∈ H}
                                               (
                                      ′ ′        𝑓 = 𝑓 ′ ∧ (𝑔(𝜎) =⇒ 𝑡 == 𝑡 ′ )              ¬𝜄 (𝜎)
                     alias(𝜎, 𝑡, 𝑓 , 𝑡 , 𝑓 ) =
                                                 (𝑓 = 𝑓 ′ ) ∧ sat(𝑔(𝜎) && 𝑡 == 𝑡 ′ )        𝜄 (𝜎)

  For ease of notation, the judgement 𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, R applies the rules above, initializing additional
parameters and ignoring the parameters that are internal to consume.
                                               SConsume
                                               𝜎, 𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, R, _
                                                  𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, R

C.9     Execute
Symbolic execution is denoted by the small-step judgement
                                                 𝜎 ⊢ 𝑠 → 𝑠′ ⊣ 𝜎′.
where 𝜎 is the symbolic state prior to execution, 𝑠 is the statement to execute, 𝑠 ′ is the statement
remaining after this execution step and 𝜎 ′ is the symbolic state after the execution step.
   Note that as in §C.6 there may be multiple resulting symbolic states 𝜎 ′ for which the judgement
applies, and therefore the path condition of 𝜎 ′ must be satisfied before assuming that 𝜎 ′ corresponds
to a particular execution step.

                                              SExecSeq

                                              𝜎 ⊢ skip; 𝑠 → 𝑠 ⊣ 𝜎
                                   SExecAssign
                                   𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _         𝛾 ′ = 𝛾 (𝜎) [𝑥 ↦→ 𝑡]
                                        𝜎 ⊢ 𝑥 = 𝑒; 𝑠 → 𝑠 ⊣ 𝜎 ′ [𝛾 = 𝛾 ′ ]
Gradually Verifying Unfolding Expressions & Pure Functions                                                  43

              SExecAssignField
               𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _      𝜎 ′ ⊢ acc(𝑥 .𝑓 ) ▷ 𝜎 ′′, _      H′ = H(𝜎); ⟨𝛾 (𝜎 ′′ ) (𝑥), 𝑓 , 𝑡⟩
                                        𝜎 ⊢ 𝑥 .𝑓 = 𝑒; 𝑠 → 𝑠 ⊣ 𝜎 ′′ [H = H′ ]

                     SExecAlloc
                      𝑡 = fresh       𝑇 𝑓 = struct(𝑆)         H′ = H(𝜎); ⟨𝑓 , 𝑡, default(𝑇 )⟩
                                     𝜎 ⊢ 𝑥 = alloc(𝑆); 𝑠 → 𝑠 ⊣ 𝜎 [H = H′ ]

              SExecCall
              𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′ , _      𝑥 = params(𝑚)        𝜎 ′ [𝛾 = [𝑥 ↦→ 𝑡𝑒 ]] ⊢ pre(𝑚) ▷ 𝜎 ′, _
                      𝑡 = fresh         𝜎 [𝛾 = [𝑥 ↦→ 𝑡𝑒 , result ↦→ 𝑡]] ⊢ post(𝑚) ◁ 𝜎 ′′
                                          ′

                                  𝜎 ⊢ 𝑦 = 𝑚(𝑒); 𝑠 → 𝑠 ⊣ 𝜎 ′′ [𝛾 = 𝛾 (𝜎) [𝑦 ↦→ 𝑡]]

                                     SExecAssert
                                      𝜎 ⊢ ? ∗ 𝜙 ▷ 𝜎 ′, _       𝜎 ′ ⊢ ? ∗ 𝜙 ◁ 𝜎 ′′
                                     𝜎 ⊢ assert 𝜙; 𝑠 → 𝑠 ⊣ 𝜎 [𝑔 = 𝑔(𝜎 ′′ )]

         SExecFold
                           𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _     𝑥 = predicate_params(𝑝)
         𝜎 [𝛾 = [𝑥 ↦→ 𝑡]] ⊢ predicate(𝑝) ▷ 𝜎 ′′, _
          ′
                                                       𝜎 ′′′ = 𝜎 ′′ [𝛾 = 𝛾 (𝜎), H = H(𝜎 ′′ ); ⟨𝑝, 𝑡⟩]
                                           𝜎 ⊢ fold 𝑝 (𝑒); 𝑠 → 𝑠 ⊣ 𝜎 ′′′

   SExecUnfold
                                              𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _
     ′               ′′
   𝜎 ⊢ 𝑝 (𝑒) ▷ 𝜎 , _            𝑥 = predicate_params(𝑝)        𝜎 ′′ [𝛾 = [𝑥 ↦→ 𝑡]] ⊢ predicate(𝑝) ◁ 𝜎 ′′′
                              𝜎 ⊢ unfold 𝑝 (𝑒 1, · · · , 𝑒𝑛 ); 𝑠 → 𝑠 ⊣ 𝜎 ′′′ [𝛾 = 𝛾 (𝜎)]

                          SExecIfA
                                                  𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _
                          𝜎 ⊢ if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠 → 𝑠 1 ; 𝑠 ⊣ 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡]

                          SExecIfB
                                                  𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _
                          𝜎 ⊢ if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠 → 𝑠 2 ; 𝑠 ⊣ 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && ! 𝑡]

              SExecWhileSkip
                                                𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, _
              𝑥 = modified(𝑠)    𝜎 ′ [𝛾 = 𝛾 (𝜎 ′ ) [𝑥 ↦→ fresh]] ⊢ 𝜙˜ ◁ 𝜎 ′′  𝜎 ′′ ⊢ 𝑒 ⇓ 𝑡 ⊣ _, _
                    𝜎 ⊢ while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ → 𝑠 ′ ⊣ 𝜎 ′′ [𝑔 = 𝑔(𝜎 ′′ ) && ! 𝑡]
                                          ˜ returns the set of all permissions remaining in 𝜎 if
Definition 29. The helper function rem(𝜎, 𝜙)
 ˜
𝜙 is not completely precise:
                      
                      
                       ∅                                       if 𝜙˜ is completely precise
                      
                      
                 ˜                         ′
          rem(𝜎, 𝜙) := {⟨𝑡, 𝑓 ⟩ : ⟨𝑓 , 𝑡, 𝑡 ⟩ ∈ H(𝜎) ∪ H (𝜎)} ∪
                      
                       {⟨𝑝, 𝑡⟩ : ⟨𝑝, 𝑡⟩ ∈ H(𝜎) ∪ H (𝜎)}
                      
                                                                otherwise
                      
This is used to symbolically calculate the required exclusion frame.
44                                                                                                 Torek et al.


C.10    Verification states
Definition 30. A verification state Σ is either an abstract symbol or a triple consisting of a
symbolic state, a statement, and a post-condition.
                                Σ ::= init | final | ⟨𝜎, 𝑠, 𝜙⟩
                                                             ˜

  The reachability of verification transitions, as determined by modular verification for a given
program Π, is determined by the judgement
                                                  Π ⊢ Σ → Σ′
where Σ is the beginning verification state and Σ′ is the next verification state.

                           SVerifyInit

                           ⟨𝑠, 𝑀, 𝑃, 𝑆⟩ ⊢ init → ⟨⟨⊥, ∅, ∅, ∅, true⟩, 𝑠, true⟩
            SVerifyMethod
             𝑚∈𝑀          𝑥 = params(𝑚)            ⟨⊥, ∅, ∅, [𝑥 ↦→ fresh], true⟩ ⊢ pre(𝑚) ◁ 𝜎
                          ⟨𝑠, 𝑀, 𝑃, 𝑆⟩ ⊢ init → ⟨𝜎, body(𝑚); skip, post(𝑚)⟩
       SVerifyLoopBody
                         Π ⊢ _ → ⟨𝜎0, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′, 𝜙˜0 ⟩
       𝑥 = modified(𝑠)      ⟨⊥, 𝛾 (𝜎0 ) [𝑥 ↦→ fresh], ∅, ∅, 𝑔(𝜎0 )⟩ ⊢ 𝜙˜ ◁ 𝜎0′     𝜎0′ ⊢ 𝑒 ⇓ 𝑡 ⊣ _, R
           Π ⊢ ⟨𝜎, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′, 𝜙˜0 ⟩ → ⟨𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡], 𝑠; skip, 𝜙⟩
                                                                  0         0
                                                                                               ˜
            SVerifyLoop
                                Π ⊢ _ → ⟨𝜎, while 𝑒 invariant 𝜙˜ ′ do 𝑠; 𝑠 ′, 𝜙⟩
                                                                              ˜
            𝜎 ⊢ 𝜙˜ ′ ▷ 𝜎 ′, _       𝑥 = modified(𝑠)     𝜎 [𝛾 = 𝛾 (𝜎) [𝑥 ↦→ fresh]] ⊢ 𝜙˜ ′ ◁ 𝜎 ′′
                                                         ′

                                 Π ⊢ ⟨𝜎, while 𝑒 invariant 𝜙˜ ′ do 𝑠; 𝑠 ′, 𝜙⟩
                                                                           ˜ →
                                       ⟨𝜎 , while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′, 𝜙⟩
                                          ′′                      ′           ˜
                                    SVerifyStep
                                    Π ⊢ _ → ⟨𝜎, 𝑠, 𝜙⟩
                                                    ˜    𝜎 ⊢ 𝑠 → 𝑠′ ⊣ 𝜎′
                                         Π ⊢ ⟨𝜎, 𝑠, 𝜙⟩
                                                     ˜ → ⟨𝜎 ′, 𝑠 ′, 𝜙⟩
                                                                    ˜
                                   SVerifyFinal
                                   Π ⊢ _ → ⟨𝜎, skip, 𝜙⟩
                                                     ˜         𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, _
                                           Π ⊢ ⟨𝜎, skip, 𝜙⟩
                                                         ˜ → final

Definition 31. A verification state Σ is reachable from program Π if Σ = init or Π ⊢ _ → Σ, _, _, _.
  A verification state Σ is reachable from program Π with valuation 𝑉 if Σ is reachable from Π
and 𝑉 is defined for all symbolic values contained in Σ.

C.11    Guards
A guard judgement determines the set of runtime checks that must be satisfied at the given
verification state before taking the next execution step, and determines the exclusion frame required
to preserve the validity of heap chunks contained by the current symbolic state. This is denoted by
the judgement
                                               Σ ⇀ 𝜎 ′, R, Θ
where Σ is the current verification state, 𝜎 ′ is the intermediate state, R is the set of required checks,
and Θ is the exclusion frame (represented as a set of symbolic permissions).
Gradually Verifying Unfolding Expressions & Pure Functions                                                 45




                                      SGuardInit

                                      init ⇀ ⟨⊥, ∅, ∅, ∅, true⟩ ⊣ ∅, ∅

                                         SGuardSeq

                                                      ˜ ⇀ 𝜎 ⊣ ∅, ∅
                                         ⟨𝜎, skip; 𝑠, 𝜙⟩
                                        SGuardAssign
                                               𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎 ′, R
                                                       ˜ ⇀ 𝜎 ⊣ R, ∅
                                         ⟨𝜎, 𝑥 = 𝑒; 𝑠, 𝜙⟩
                             SGuardAssignField
                             𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎 ′, R ′       𝜎 ′ ⊢ acc(𝑥 .𝑓 ) ▷ 𝜎 ′′, R ′′
                                                    ˜ ⇀ 𝜎 ′′ ⊣ R ′ ∪ R ′′, ∅
                                   ⟨𝜎, 𝑥 .𝑓 = 𝑒; 𝑠, 𝜙⟩
                                    SGuardAlloc

                                                         ˜ ⇀ 𝜎 ⊣ ∅, ∅
                                    ⟨𝜎, 𝑥 = alloc(𝑆); 𝑠, 𝜙⟩
           SGuardCall
           𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R      𝑥 = params(𝑚)        𝜎 ′ [𝛾 = [𝑥 ↦→ 𝑡]] ⊢ pre(𝑚) ▷ 𝜎 ′′, R ′
                                     ˜ ⇀ 𝜎 ′′ [𝛾 = 𝛾 (𝜎)] ⊣ R ∪ R ′, rem(𝜎 ′′, pre(𝑚))
                    ⟨𝜎, 𝑦 = 𝑚(𝑒); 𝑠, 𝜙⟩
                                     SGuardAssert
                                             𝜎 ⊢ ? ∗ 𝜙 ▷ 𝜎 ′, R
                                                       ˜ ⇀ 𝜎 ′ ⊣ R, ∅
                                      ⟨𝜎, assert 𝜙; 𝑠, 𝜙⟩
  SGuardFold
  𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R       𝑥 = predicate_params(𝑝)         𝜎 ′ [𝛾 = [𝑥 ↦→ 𝑡]] ⊢ predicate(𝑝) ▷ 𝜎 ′′, R ′
                                                                          Ø
                                             ˜ ⇀ 𝜎 ′′ [𝛾 = 𝛾 (𝜎)] ⊣ R ′ ∪
                          ⟨𝜎, fold 𝑝 (𝑒); 𝑠, 𝜙⟩                               R, ∅
                              SGuardUnfold
                                 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R    𝜎 ′ ⊢ 𝑝 (𝑒) ▷ 𝜎 ′′, R ′
                                                                       Ø
                                                    ˜ ⇀ 𝜎 ′′ ⊣ R ′ ∪
                               ⟨𝜎, unfold 𝑝 (𝑒); 𝑠, 𝜙⟩                     R, ∅
                                SGuardIf
                                             𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎 ′, R
                                                                ˜ ⇀ 𝜎 ′ ⊣ R, ∅
                                ⟨𝜎, if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠, 𝜙⟩

          SGuardWhile
                                              𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, R ′
          𝑥 = modified(𝑠)     𝜎 ′ [𝛾 = 𝛾 (𝜎 ′ ) [𝑥 ↦→ fresh]] ⊢ 𝜙˜ ◁ 𝜎 ′′       𝜎 ′′ ⊢ 𝑒 ⇓ _ ⊣ _, R ′′
           ⟨𝜎, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′, 𝜙˜ ′ ⟩ ⇀ 𝜎 ′ [𝑔 = 𝑔(𝜎 ′′ )] ⊣ R ′ ∪ R ′′, rem(𝜎 ′, 𝜙)
                                                                                                   ˜

                                          SGuardFinish
                                                 𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, R
                                                      ˜ ⇀ 𝜎 ′ ⊣ R, ∅
                                           ⟨𝜎, skip, 𝜙⟩
46                                                                                                       Torek et al.


C.12    Valid states
Definition 32. A verification state Σ corresponds with valuation 𝑉 to an execution state Γ if Σ = Γ,
or Γ = ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · S⟩ for some 𝐻, 𝛼, 𝜌, 𝑠 and Σ = ⟨𝜎, 𝑠, _⟩ for some 𝜎, such that ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎.
Definition 33. A partial state Γ = ⟨𝐻, S⟩ is validated by a verification state Σ with valuation 𝑉 if
one of the following cases apply:
  Part 33.1. S = nil
  Part 33.2. S = ⟨𝜌, 𝛼, 𝑦 = 𝑚(𝑒 1, · · · , 𝑒𝑘 ); 𝑠⟩ · S ∗ for some 𝜌, 𝛼, 𝑦, 𝑚, 𝑘, 𝑒 1, · · · , 𝑒𝑘 , 𝑠, and S ∗ , and
there exists some Σ′ , 𝑉 ′ , 𝑥 1, · · · , 𝑥𝑘 , 𝑡 1, · · · , 𝑡𝑘 , 𝜎0, · · · , 𝜎𝑘 and 𝜎 ′ such that:
                             The partial state ⟨𝐻, S ∗ ⟩ is validated by Σ′ and 𝑉 ′,                             (5)
                       Σ is reachable from Π with valuation 𝑉 ,
                         ′                                                  ′           ′
                                                                                    𝑠 (Σ ) = 𝑠 (S),              (6)
                                           𝑥 1, · · · , 𝑥𝑘 = params(𝑚),                                          (7)
                               ′
                   𝜎0 = 𝜎 (Σ ),     𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, _,    ··· ,       𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,             (8)
                                                                                ′
                                     ∀ 1 ≤ 𝑖 ≤ 𝑘 : 𝑉 (𝛾 (Σ) (𝑥𝑖 )) = 𝑉 (𝑡𝑖 ),                                    (9)
                                           ′                           ′
                       𝜎𝑘 ⊢ pre(𝑚) ▷ 𝜎 , _,           ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 [𝛾 = 𝛾 (𝜎0 )],           and              (10)
                                                𝜙˜ (Σ) = post(𝑚)                                                (11)

  Part 33.3. S = ⟨𝜌, 𝛼, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ ⟩ · S ∗ for some 𝜌, 𝛼, 𝑒, 𝜙,
                                                                                 ˜ 𝑠, 𝑠 ′ , S ∗ , and there
exists some Σ , 𝑉 , and 𝜎 such that:
              ′  ′       ′

                             The partial state ⟨𝐻, S ∗ ⟩ is validated by Σ′ and 𝑉 ′                             (12)
                        Σ′ is reachable from Π with valuation 𝑉 ′,                  𝑠 (Σ′ ) = 𝑠 (S)             (13)
                                   𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, _,     and    ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′                                (14)
                                                      𝜙˜ (Σ) = 𝜙˜                                               (15)
Definition 34. For a program Π, a dynamic state Γ is validated by Σ and valuation 𝑉 if all the
following are true:
   Part 34.1. Σ is reachable from Π with 𝑉
   Part 34.2. Γ corresponds to Σ with 𝑉
   Part 34.3. If Γ = ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · S ∗ ⟩, then the partial state ⟨𝐻, S ∗ ⟩ is validated by Σ and 𝑉 .
Definition 35. Γ is a valid state if Γ is validated by some Σ.

D     Soundness

   In this version of the proof, we forgo the deterministic evaluation judgement used by Zimmerman
et al. [33] to more closely align with the implementation of Gradual Viper. Lemmas 1 to 27 in
our proof have the same numbering as in the proof of soundness in [33]. Lemma 28 is a modified
version of lemma 29 in [33]. Lemmas 29 and above in our proof correspond to lemmas 31 and above
in [33].
   Lemmas 1, 14, 24, 25, 26, 27, 28, 49, 50, 54 have been modified; lemmas and theorems stated
without proof have the same proof as Zimmerman et al. [33].

D.1    Cross-cutting lemmas
Lemma 1 (Relating expression framing and exact footprints). If ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 then T𝑒U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼,
and conversely, if ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 and T𝑒U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼 ′ then ⟨𝐻, 𝛼 ′, 𝜌⟩ ⊢frm 𝑒.
Gradually Verifying Unfolding Expressions & Pure Functions                                                47


  Proof. By induction on the derivation of ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒.
  Case 1. 𝑙: Then T𝑙U ⟨𝐻, 𝜌 ⟩ = ∅, thus T𝑙U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼, and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑙 by FrameLiteral.
  Case 2. 𝑣: Then T𝑣U ⟨𝐻, 𝜌 ⟩ = ∅, thus T𝑣U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼, and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑣 by FrameVar.
  Case 3. 𝑒.𝑓 :
  Suppose that T𝑒.𝑓 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼. Then by definition T𝑒U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼 and ⟨ℓ, 𝑓 ⟩ ∈ 𝛼 for some ℓ such
that ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ ℓ. By induction ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒, by AssertAcc ⟨𝐻, 𝛼, 𝜌⟩ ⊨ acc(𝑒.𝑓 ), and thus by
FrameField, ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒.𝑓 .
  Suppose that ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒.𝑓 . Then by FrameField, ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 and ⟨𝐻, 𝛼, 𝜌⟩ ⊨ acc(𝑒.𝑓 ),
thus by induction T𝑒U ⟨𝐻, 𝑒𝑛𝑣⟩ ⊆ 𝛼 and by AssertAcc, ⟨ℓ, 𝑓 ⟩ ∈ 𝛼 for some ℓ such that ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ ℓ.
Thus T𝑒.𝑓 U ⟨𝐻, 𝜌 ⟩ = T𝑒U ⟨𝐻, 𝜌 ⟩ ; ⟨ℓ, 𝑓 ⟩ ⊆ 𝛼.
  Case 4. 𝑒 1 ⊕ 𝑒 2 :
               T𝑒 1 ⊕ 𝑒 2 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼
                 ⇐⇒ T𝑒 1 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼 and T𝑒 2 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼                       by definition
                 ⇐⇒ ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1 and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 2                        by induction
                 ⇐⇒ ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1 ⊕ 𝑒 2                                          by FrameOp
  Case 5. 𝑒 1 || 𝑒 2 :
           T𝑒 1 || 𝑒 2 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼 =⇒
            either ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ true and T𝑒 1 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼                           by definition
               =⇒ ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ true and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1                            by induction
               =⇒ ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1 || 𝑒 2                                            by FrameOrA
            or ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ false and T𝑒 1 U ⟨𝐻, 𝜌 ⟩ ∪ T𝑒 2 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼             by definition
               =⇒ ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ false, ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1,
                     and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 2                                             by induction
               =⇒ ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1 || 𝑒 2                                             by FrameOrB

         ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1 || 𝑒 2 =⇒
          either ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ true and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1                              by FrameOrA
             =⇒ ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ true and T𝑒 1 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼                                by induction
             =⇒ T𝑒 1 || 𝑒 2 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼                                                 by definition
          or ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ false, ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1,
               and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 2                                                    by FrameOrB
             =⇒ ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ false and T𝑒 1 U ⟨𝐻, 𝜌 ⟩ ∪ T𝑒 2 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼              by induction
             =⇒ T𝑒 1 || 𝑒 2 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼                                                 by definition
  Case 6. 𝑒 1 && 𝑒 2 : Similar to case 5.
  Case 7. ! 𝑒:
                         T! 𝑒U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼
                          ⇐⇒ T𝑒U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼                                  by definition
                          ⇐⇒ ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒                                 by induction
                          ⇐⇒ ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm ! 𝑒                               by FrameNeg
48                                                                                                       Torek et al.


   Case 8. FrameUnfolding – Assume that ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm unfolding 𝑝 (𝑒) in 𝑒 0 . Then, by defini-
                                                               Ð
tion of IFramePredicate, ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒, so inductively T𝑒U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼. Inductively, T𝑒 0 U ⟨𝐻, 𝜌 ⟩ ⊆
𝛼. By definition,
                                                                        Ø
                   Tunfolding 𝑝 (𝑒) in 𝑒 0 U ⟨𝐻, 𝜌 ⟩ = T𝑒 0 U ⟨𝐻, 𝜌 ⟩ ∪   T𝑒U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼
.
   Assume ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑓 (𝑒) and T𝑓 (𝑒)U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼 ′ . By definition, ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmI 𝑝 (𝑒), ⟨𝐻, 𝛼, 𝜌⟩ ⊨
𝑝 (𝑒), and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 0 . By the induction hypothesis and IFramePredicate, ⟨𝐻, 𝛼 ′, 𝜌⟩ ⊢frmI 𝑝 (𝑒)
and ⟨𝐻, 𝛼 ′, 𝜌⟩ ⊢frm 𝑒 0 . Then, by definition of AssertPredicate, ⟨𝐻, 𝛼, [𝑥 ↦→ 𝑣]⟩ ⊨ predicate(𝑝)
where 𝑥 = predicate_params(𝑝) and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣. Then, by Lemma 11 and Lemma 9, ⟨𝐻, 𝛼 ′, 𝜌⟩ ⊨
𝑝 (𝑒).
   Case 9. FrameFunction – Assume ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑓 (𝑒). Then, by definition, ⟨𝐻, 𝛼, [𝑥 ↦→ 𝑣]⟩ ⊢frmI
func_pre(𝑓 ), ⟨𝐻, 𝛼, [𝑥 ↦→ 𝑣]⟩ ⊨ func_pre(𝑓 ), and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒. By Definition 1, this implies
                                                        Ð
⟨𝐻, 𝛼, [𝑥 ↦→ 𝑣]⟩ ⊢frm func_body(𝑓 ). Inductively, T𝑒U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼 and Tfunc_bodyU ⟨𝐻, [𝑥↦→𝑣 ] ⟩ .
Then, by Lemma 3, ⟨𝐻, 𝛼, [𝑥 ↦→ 𝑣]⟩ ⊢frmE func_pre(𝑓 ), so by Lemma 2, Tfunc_pre(𝑓 )U ⟨𝐻, [𝑥↦→𝑣 ] ⟩ ⊆
𝛼. Therefore,
                                                                                          Ø
       T𝑓 (𝑒)U ⟨𝐻, 𝛼 ⟩ = Tfunc_pre(𝑓 )U ⟨𝐻, [𝑥↦→𝑣 ] ⟩ ∪ Tfunc_body(𝑓 )U ⟨𝐻, [𝑥↦→𝑣 ] ⟩ ∪       T𝑒U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼 .

  Now, assume ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑓 (𝑒) and T𝑓 (𝑒)U ⟨𝐻, 𝛼 ⟩ ⊆ 𝛼 ′ . Inductively, ⟨𝐻, 𝛼 ′, 𝜌⟩ ⊢frm 𝑒 and
⟨𝐻, 𝛼 ′, 𝜌⟩ ⊢frmI func_pre(𝑓 ). Since ⟨𝐻, 𝛼, 𝜌⟩ ⊨ func_pre(𝑓 ) and Tfunc_pre(𝑓 )U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼 ′ , by
Lemma 12, ⟨𝐻, 𝛼 ′, 𝜌⟩ ⊨ func_pre(𝑓 ). Therefore, ⟨𝐻, 𝛼 ′, 𝜌⟩ ⊢frm 𝑓 (𝑒).

                                                                                                                  □
Lemma 2 (Relating formula assertion/framing and exact footprints). If ⟨𝐻, 𝛼 ′, 𝜌⟩ ⊨ 𝜙,
                                                                                    ˜ ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE
˜       ′            ˜
𝜙, and 𝛼 ⊆ 𝛼, then T𝜙U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼.
                                                                       ˜ ⟨𝐻, 𝛼 ′, 𝜌⟩ ⊨ 𝜙,
Lemma 3 (Relating iso- and equi-recursive framing). If ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmI 𝜙,              ˜ and
 ′                          ˜
𝛼 ⊆ 𝛼, then ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE 𝜙.
Lemma 4 (Relating specification assertion and exact footprints). If 𝜙˜ is a specification and
            ˜ then T𝜙U
⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙,      ˜ ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼.

Lemma 5 (Relating specification assertion and footprints). If 𝜙˜ is a specification and ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙,
                                                                                                    ˜
      ˜
then ⌊𝜙⌋ ⟨𝐻, 𝛼, 𝜌 ⟩ ⊆ 𝛼.

Lemma 6 (Relating specification exact footprints and footprints). If 𝜙˜ is a specification and
            ˜ then T𝜙U
⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙,      ˜ ⟨𝐻, 𝜌 ⟩ ⊆ ⌊𝜙⌋
                                 ˜ ⟨𝐻, 𝛼, 𝜌 ⟩ .

Lemma 7 (Monotonicity of expression framing WRT permissions). If ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 and 𝛼 ⊆ 𝛼 ′ ,
then ⟨𝐻, 𝛼 ′, 𝜌⟩ ⊢frm 𝑒.
     Proof. By Lemma 1, T𝑒U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼 ⊆ 𝛼 ′ , so again by Lemma 1, ⟨𝐻, 𝛼 ′, 𝜌⟩ ⊢frm 𝑒.                          □

Lemma 8 (Monotonicity of equi-recursive framing WRT permissions). If ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE 𝜙˜ and
𝛼 ⊆ 𝛼 ′ , then ⟨𝐻, 𝛼 ′, 𝜌⟩ ⊢frmE 𝜙.
                                 ˜

Lemma 9 (Monotonicity of assertions WRT permissions). If ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙˜ and 𝛼 ⊆ 𝛼 ′ , then
⟨𝐻, 𝛼 ′, 𝜌⟩ ⊨ 𝜙.
              ˜
Gradually Verifying Unfolding Expressions & Pure Functions                                               49


                                                                                ˜ then
Lemma 10 (Exact footprint preserves equi-recursive framing). If ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE 𝜙,
     ˜ ⟨𝐻, 𝜌 ⟩ ∩ 𝛼, 𝜌⟩ ⊢frmE 𝜙.
⟨𝐻, T𝜙U                      ˜

                                                                ˜ then ⟨𝐻, T𝜙U
Lemma 11 (Exact footprint preserves assertions). If ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙,          ˜ ⟨𝐻, 𝜌 ⟩ ∩ 𝛼, 𝜌⟩ ⊨ 𝜙.
                                                                                                ˜

                                                                                     ˜ ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼 ′ ,
Lemma 12 (Supersets of exact footprints preserve assertions). If ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙˜ and T𝜙U
          ′       ˜
then ⟨𝐻, 𝛼 , 𝜌⟩ ⊨ 𝜙.

Lemma 13 (Footprints preserve specification assertions). If 𝜙˜ is a specification and ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙,
                                                                                                  ˜
          ˜                    ˜
then ⟨𝐻, ⌊𝜙⌋ ⟨𝐻, 𝛼, 𝜌 ⟩ , 𝜌⟩ ⊨ 𝜙.

Lemma 14 (Modeling implies ownership). If ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 then

                                     ∀ ℎ ∈ H(𝜎) ∪ H (𝜎) : 𝑉 LℎM𝐻 ⊆ 𝛼 .

   Proof. Let ℎ ∈ H(𝜎) ∪ H (𝜎). Then, by definition of the symbolic and optimistic heaps, one of
the following two cases applies:
   Case 1. ℎ is a field chunk – Then, ℎ = ⟨𝑓 , 𝑡, 𝑡 ′ ⟩. By the definition of state correspondence,
⟨𝐻, 𝛼⟩ 𝑉 H(𝜎) and ⟨𝐻, 𝛼⟩ 𝑉 H (𝜎). Therefore, ⟨𝑉 (𝑡), 𝑓 ⟩ ∈ 𝛼, so 𝑉 L⟨𝑓 , 𝑡, 𝑡 ′ ⟩M𝐻 = {⟨𝑉 (𝑡), 𝑓 ⟩} ⊆
𝛼.
   Case 2. ℎ is a predicate chunk – Then, ℎ = ⟨𝑝, 𝑡⟩. Since ⟨𝐻, 𝛼⟩ 𝑉 H(𝜎) and ⟨𝐻, 𝛼⟩ 𝑉 H (𝜎)
(since the optimistic heap can now contain predicate chunks as well), ⟨𝐻, 𝛼, [𝑥 ↦→ 𝑉 (𝑡)]⟩ ⊨
predicate(𝑝) where 𝑥 = predicate_params(𝑝). Then, since predicate(𝑝) is a specification, 𝑉 L⟨𝑝, 𝑡⟩M𝐻 =
Tpredicate(𝑝)U ⟨𝐻, [𝑥↦→𝑉 (𝑡 ) ] ⟩ ⊆ 𝛼 by Lemma 4.
                                                                                                   □

Lemma 15 (Correspondence with exclusion implies disjointness). If ⟨𝐻, 𝛼 \ 𝛼 ′, 𝜌⟩ 𝑉 𝜎, then

                                        ∀ ℎ ∈ H(𝜎) : 𝑉 LℎM𝐻 ∩ 𝛼 ′ = ∅.

Lemma 16 (Disjointness implies correspondence with exclusion). If ⟨𝐻, 𝛼⟩ 𝑉 H and ∀ ℎ ∈ H :
𝑉 LℎM𝐻 ∩ 𝛼 ′ = ∅, then ⟨𝐻, 𝛼 \ 𝛼 ′ ⟩ 𝑉 H.

Lemma 17. If ⟨𝐻, 𝛼⟩ 𝑉 H and 𝛼 ⊆ 𝛼 ′ , then ⟨𝐻, 𝛼⟩ 𝑉 H.

Lemma 18. If ⟨𝐻, 𝛼⟩ 𝑉 H and 𝛼 ⊆ 𝛼 ′ , then ⟨𝐻, 𝛼⟩ 𝑉 H .

Lemma 19. If ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 and 𝛼 ⊆ 𝛼 ′ , then ⟨𝐻, 𝛼 ′, 𝜌⟩ 𝑉 𝜎.

Lemma 20 (Statement rearrangement). If 𝑠 = 𝑠 1 ; 𝑠 2 , then 𝑠 = 𝑠 1′ ; 𝑠 2′ such that 𝑠 1′ is not a sequence
statement and 𝑠 2′ = 𝑠 2 or 𝑠 2′ = 𝑠 1′′ ; 𝑠 2 where 𝑠 1 = 𝑠 1′ ; 𝑠 1′′ .

Lemma 21 (Run-time check monotonicity WRT permissions). If ⟨𝐻, 𝛼⟩ ⊢𝑉 𝑟 and 𝛼 ⊆ 𝛼 ′ , then
⟨𝐻, 𝛼 ′ ⟩ ⊢𝑉 𝑟 .

Lemma 22 (Run-time checks monotonicity WRT permissions). If ⟨𝐻, 𝛼⟩ ⊢𝑉 R and 𝛼 ⊆ 𝛼 ′ , then
⟨𝐻, 𝛼 ′ ⟩ ⊢𝑉 R.

Lemma 23 (Run-time check set implies subsets). If ⟨𝐻, 𝛼⟩ ⊢𝑉 R and R ′ ⊆ R, then ⟨𝐻, 𝛼⟩ ⊢𝑉 R ′ .
50                                                                                                    Torek et al.


D.2   Evaluation
Definition 36. For a judgement 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R, given an initial valuation 𝑉 , heap 𝐻 , and
environment 𝜌, the corresponding valuation is denoted
                                       𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R | 𝐻, 𝜌].
This valuation is defined as follows, depending on the rule that proves the derivation. Values are
referenced using the respective name from the rule definition.
   Note that the corresponding valuation always extends the initial valuation, and is defined for all
fresh symbolic values in the judgement.
 • SEvalLiteral:
                                   𝑉 [𝜎 ⊢ 𝑙 ⇓ 𝑙 ⊣ 𝜎, _ | 𝐻, 𝜌] := 𝑉
 • SEvalVar:
                                     𝑉 [𝜎 ⊢ 𝑥 ⇓ _ ⊣ 𝜎, _ | 𝐻, 𝜌] := 𝑉
 • SEvalNeg:
                    𝑉 [𝜎 ⊢ ! 𝑒 ⇓ ! 𝑡 ⊣ 𝜎 ′, R | 𝐻, 𝜌] := 𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R | 𝐻, 𝜌]
 • SEvalOrA:
                𝑉 [𝜎 ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑡 1 ⊣ 𝜎 ′′, R | 𝐻, 𝜌] := 𝑉 [𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, R | 𝐻, 𝜌]
 • SEvalOrB:
                       𝑉 [𝜎 ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′, R 1 ∪ R 2 | 𝐻, 𝜌] :=
                            𝑉 [𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, R 1 | 𝐻, 𝜌]
                                [𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && ! 𝑡 1 ] ⊢ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′, R 2 | 𝐻, 𝜌]
 • SEvalAndA:
                𝑉 [𝜎 ⊢ 𝑒 1 && 𝑒 2 ⇓ 𝑡 1 ⊣ 𝜎 ′′, R | 𝐻, 𝜌] := 𝑉 [𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, R | 𝐻, 𝜌]
 • SEvalAndB:
                        𝑉 [𝜎 ⊢ 𝑒 1 && 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′, R 1 ∪ R 2 | 𝐻, 𝜌] :=
                             𝑉 [𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, R 1 | 𝐻, 𝜌]
                                 [𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡 1 ] ⊢ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′, R 2 | 𝐻, 𝜌]
 • SEvalOp:
                           𝑉 [𝜎 ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓ 𝑡 1 ⊕ 𝑡 2 ⊣ 𝜎 ′′, R 1 ∪ R 2 | 𝐻, 𝜌] :=
                                 𝑉 [𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, R 1 | 𝐻, 𝜌]
                                    [𝜎 ′ ⊢ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′, R 2 | 𝐻, 𝜌]
 • SEvalField or SEvalFieldOptimistic:
                    𝑉 [𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′′, _ | 𝐻, 𝜌] := 𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′, R | 𝐻, 𝜌]
 • SEvalFieldImprecise:
          𝑉 [𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′′, _ | 𝐻, 𝜌] := 𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′, R | 𝐻, 𝜌] [𝑡 ↦→ 𝐻 (𝑉 (𝑡𝑒 ), 𝑓 )]
 • SEvalFieldFailure:
          𝑉 [𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′, _ | 𝐻, 𝜌] := 𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′, R | 𝐻, 𝜌] [𝑡 ↦→ 𝐻 (𝑉 (𝑡𝑒 ), 𝑓 )]
Gradually Verifying Unfolding Expressions & Pure Functions                                                  51


 • SEvalUnfoldingPrecise, SEvalUnfoldingImpreciseA, or SEvalUnfoldingImpreciseB:
                          𝑉 [𝜎1 ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓ 𝑡 ⊣ 𝜎5 [. . .], R | 𝐻, 𝜌] :=
                                 𝑉 [𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2, R 1 | 𝐻, 𝜌]
                                    [𝜎2 ⊢ 𝑝 (𝑒) ▷ 𝜎3, R 2 | 𝐻, 𝜌]
                                    [𝜎3 [. . .] ⊢ predicate(𝑝) ◁ 𝜎4 | 𝐻, 𝜌]
                                    [𝜎4 ⊢ 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎5, R 3 | 𝐻, 𝜌]
 • SEvalUnfoldingImplicitPrecise or SEvalUnfoldingImplicitImprecise:
        𝑉 [𝜎1 ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓ 𝑡 ⊣ 𝜎2, R | 𝐻, 𝜌] := 𝑉 [𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2, R | 𝐻, 𝜌] [𝑡 ↦→ 𝑣]
   where ⟨𝐻, 𝜌⟩ ⊢ 𝑒 0 ⇓ 𝑣.
 • SEvalFunctionExplicit:
          𝑉 [𝜎1 ⊢ 𝑓 (𝑒) ⇓ 𝑡 ⊣ 𝜎6, R 1 ∪ R 2 ∪ R 3 | 𝐻, 𝜌] :=
                𝑉 [𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2, R 1 | 𝐻 ]
                   [𝜎2 [𝛾 = 𝛾 (𝜎2 ) [𝑥 ↦→ 𝑡]] ⊢ pre(𝑓 ) ▷ 𝜎3, R 2 | 𝐻, 𝜌]
                   [𝜎3 ⊢ pre(𝑓 ) ◁ 𝜎4 | 𝐻, 𝜌]
                   [𝜎4 [H = H′, H = H (𝜎2 ), V = V (𝜎3 ) ∪ {𝑓 }] ⊢ body(𝑓 ) ⇓ 𝑡 ′ ⊣ 𝜎5, R 3 | 𝐻, 𝜌]
                   [𝑓 (𝑡, 𝑠) ↦→ 𝑉 (𝑡 ′ )]
 • SEvalFunctionImplicit:
          𝑉 [𝜎1 ⊢ 𝑓 (𝑒) ⇓ 𝑡 ⊣ 𝜎4, R 1 ∪ R 2 | 𝐻, 𝜌] :=
                𝑉 [𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2, R 1 | 𝐻, 𝜌]
                   [𝜎2 [𝛾 = 𝛾 (𝜎2 ) [𝑥 ↦→ 𝑡]] ⊢ pre(𝑓 ) ▷ 𝜎3, R 2 | 𝐻, 𝜌]                 [𝑓 (𝑡, 𝑠) ↦→ 𝑣]
   where ⟨𝐻, [𝑥 ↦→ 𝑉 (𝑡)]⟩ ⊢ func_body(𝑓 ) ⇓ 𝑣.

Lemma 24. If 𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎 ′, _ then 𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎).

  Proof. We proceed by induction on the derivation of 𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎 ′, _.
  Case 1. SEvalLiteral – 𝜎 ⊢ 𝑙 ⇓ _ ⊣ 𝜎, _; SEvalVar – 𝜎 ⊢ 𝑥 ⇓ _ ⊣ 𝜎, _: Trivial since 𝑔(𝜎) =⇒
𝑔(𝜎).
  Case 2. SEvalOrA – 𝜎 ⊢ 𝑒 1 ∨ 𝑒 2 ⇓ _ ⊣ 𝜎 ′′, _: By SEvalOrA 𝜎 ⊢ 𝑒 1 ⇓ _ ⊣ 𝜎 ′, _, thus by induction
𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎). Therefore 𝑔(𝜎 ′′ ) = 𝑔(𝜎 ′ ) ∧ 𝑡 1 =⇒ 𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎).
  Case 3. SEvalOrB – 𝜎 ⊢ 𝑒 1 ∨𝑒 2 ⇓ _ ⊣ 𝜎 ′′, _: By SEvalOrB 𝜎 ⊢ 𝑒 1 ⇓ _ ⊣ 𝜎 ′, _ and 𝜎 ′ ⊢ 𝑒 2 ⇓ _ ⊣ 𝜎 ′′, _,
thus by induction 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎). Therefore 𝑔(𝜎 ′′′ ) = 𝑔(𝜎 ′′ ) && ! 𝑡 1 =⇒ 𝑔(𝜎 ′′ ) =⇒
𝑔(𝜎).
  Case 4. SEvalAndA – 𝜎 ⊢ 𝑒 1 ∧ 𝑒 2 ⇓ _ ⊣ 𝜎 ′′, _: Similar to case 2.
  Case 5. SEvalAndB – 𝜎 ⊢ 𝑒 1 ∧ 𝑒 2 ⇓ _ ⊣ 𝜎 ′′, _: Similar to case 3.
  Case 6. SEvalOp – 𝜎 ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓ _ ⊣ 𝜎 ′′, _; SEvalNeg – 𝜎 ⊢ ! 𝑒 ⇓ _ ⊣ 𝜎 ′, _; SEvalField,
SEvalFieldOptimistic – 𝜎 ⊢ 𝑒.𝑓 ⇓ _ ⊣ 𝜎 ′, _; SEvalFieldImprecise – 𝜎 ⊢ 𝑒.𝑓 ⇓ _ ⊣ 𝜎 ′′, _: By
induction.

  Case 7. SEvalUnfoldingPrecise – By definition of SEvalUnfoldingPrecise, 𝑔(𝜎6 ) =⇒ 𝑔(𝜎5 )
because 𝑔(𝜎6 ) = 𝑔(𝜎5 ). Then, 𝑔(𝜎5 ) =⇒ 𝑔(𝜎4 ) by the induction hypothesis, 𝑔(𝜎4 ) =⇒ 𝑔(𝜎3 ) by
52                                                                                              Torek et al.


Lemma 31, 𝑔(𝜎3 ) =⇒ 𝑔(𝜎2 ) by Lemma 36, and 𝑔(𝜎2 ) =⇒ 𝑔(𝜎1 ) by the induction hypothesis.
Therefore, 𝑔(𝜎6 ) =⇒ 𝑔(𝜎1 ) transitively.
  Case 8. SEvalUnfoldingImpreciseA or SEvalUnfoldingImpreciseB – By definition, 𝑔(𝜎6 ) =⇒
𝑔(𝜎5 ) because 𝑔(𝜎6 ) = 𝑔(𝜎5 ). Then, 𝑔(𝜎5 ) =⇒ 𝑔(𝜎4 ) by the induction hypothesis, 𝑔(𝜎4 ) =⇒ 𝑔(𝜎3 )
by Lemma 31, 𝑔(𝜎3 ) =⇒ 𝑔(𝜎2 ) by Lemma 36, and 𝑔(𝜎2 ) =⇒ 𝑔(𝜎1 ) by the induction hypothesis.
Therefore, 𝑔(𝜎6 ) =⇒ 𝑔(𝜎1 ) transitively.
  Case 9. SEvalUnfoldingImplicitPrecise – By induction, 𝑔(𝜎1 ) =⇒ 𝑔(𝜎2 ).
  Case 10. SEvalUnfoldingImplicitImprecise – By induction and SEvalUnfoldingImplicitImprecise,
𝑔(𝜎1 ) =⇒ 𝑔(𝜎2 ) = 𝑔(𝜎3 ).
  Case 11. SEvalFunctionExplicit – Inductively, 𝑔(𝜎2 ) =⇒ 𝑔(𝜎1 ), and by definition, 𝑔(𝜎6 ) =⇒
𝑔(𝜎2 ). Transitively, 𝑔(𝜎6 ) =⇒ 𝑔(𝜎1 ) as desired.
  Case 12. SEvalFunctionImplicit – Inductively, 𝑔(𝜎2 ) =⇒ 𝑔(𝜎1 ), and by definition, 𝑔(𝜎4 ) =⇒
𝑔(𝜎2 ). Transitively, 𝑔(𝜎4 ) =⇒ 𝑔(𝜎1 ) as desired.

                                                                                                         □

Lemma 25. If 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R then H(𝜎 ′ ) = H(𝜎), and 𝛾 (𝜎 ′ ) = 𝛾 (𝜎).
  Proof. We proceed by induction on the derivation of 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R.
  Case 1. SEvalLiteral; SEvalVar; SEvalNeg; SEvalOrA; SEvalOrB; SEvalAndA; SEvalAndB; SEvalOp;
SEvalField; SEvalFieldOptimistic; SEvalFieldImprecise; SEvalFieldFailure: Trivial by induction on
𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R.

   Case 2. SEvalUnfoldingPrecise – By definition, H(𝜎6 ) = H(𝜎2 ), and by the induction hypothesis,
H(𝜎2 ) = H(𝜎1 ). By definition and the induction hypothesis, 𝛾 (𝜎6 ) = 𝛾 (𝜎5 ) = 𝛾 (𝜎3 ). By the definition
of SConsumePredicate, 𝛾 (𝜎3 ) = 𝛾 (𝜎2 ). Then, by the induction hypothesis, 𝛾 (𝜎2 ) = 𝛾 (𝜎1 ).
   Case 3. SEvalUnfoldingImpreciseA – By definition, H(𝜎6 ) = H(𝜎2 ), and by the induction hy-
pothesis, H(𝜎2 ) = H(𝜎1 ).
   By definition and the induction hypothesis, 𝛾 (𝜎6 ) = 𝛾 (𝜎5 ) = 𝛾 (𝜎3 ). By the definition of SCon-
sumePredicate, 𝛾 (𝜎3 ) = 𝛾 (𝜎2 ). Then, by the induction hypothesis, 𝛾 (𝜎2 ) = 𝛾 (𝜎1 ).
   Case 4. SEvalUnfoldingImpreciseB – By definition, H(𝜎6 ) = H(𝜎2 ), and by the induction hy-
pothesis, H(𝜎2 ) = H(𝜎1 ). By definition and the induction hypothesis, 𝛾 (𝜎6 ) = 𝛾 (𝜎5 ) = 𝛾 (𝜎3 ).
By the definition of SConsumePredicate, 𝛾 (𝜎3 ) = 𝛾 (𝜎2 ). Then, by the induction hypothesis,
𝛾 (𝜎2 ) = 𝛾 (𝜎1 ).
   Case 5. SEvalUnfoldingImplicitPrecise – Trivially, 𝛾 (𝜎) = 𝛾 (𝜎), and H(𝜎) = H(𝜎).
   Case 6. SEvalUnfoldingImplicitImprecise – Similar to SEvalUnfoldingImplicitPrecise.
   Case 7. SEvalFunctionExplicit – Inductively, H(𝜎2 ) = H(𝜎1 ) and 𝛾 (𝜎2 ) = 𝛾 (𝜎1 ). By definition,
H(𝜎6 ) = H(𝜎2 ) and 𝛾 (𝜎6 ) = 𝛾 (𝜎2 ).
   Case 8. SEvalFunctionImplicit – Inductively, H(𝜎2 ) = H(𝜎1 ) and 𝛾 (𝜎2 ) = 𝛾 (𝜎1 ). By definition,
H(𝜎4 ) = H(𝜎2 ) and 𝛾 (𝜎4 ) = 𝛾 (𝜎2 ).

                                                                                                         □

Lemma 26 (Soundness). Let 𝑉 be some initial valuation and ⟨𝐻, 𝛼, 𝜌⟩ be some well-formed
evaluation state such that ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎.
  If 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R, ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R, and 𝑉 ′ (𝑔(𝜎 ′ )) = true where 𝑉 ′ ⊇ 𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R | 𝐻, 𝜌],
then
                     ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′, ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡), and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒.
Gradually Verifying Unfolding Expressions & Pure Functions                                                        53


   Proof. By induction on 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R.
   Case 1. SEvalLiteral – 𝜎 ⊢ 𝑙 ⇓ 𝑙 ⊣ 𝜎, ∅: Then 𝑉 ′ = 𝑉 , thus ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 by assumption.
   By EvalLiteral ⟨𝐻, 𝜌⟩ ⊢ 𝑙 ⇓ 𝑙, and by definition 𝑉 ′ (𝑙) = 𝑙.
   By FrameLiteral ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑙.
   Case 2. SEvalVar – 𝜎 ⊢ 𝑥 ⇓ 𝛾 (𝜎) (𝑥) ⊣ 𝜎, ∅: Then 𝑉 ′ = 𝑉 , thus ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 by assumption.
    By EvalVar ⟨𝐻, 𝜌⟩ ⊢ 𝑥 ⇓ 𝜌 (𝑥), and 𝜌 (𝑥) = 𝑉 ′ (𝛾 (𝜎) (𝑥)) since 𝜌 𝑉 ′ 𝛾 (𝜎).
    By FrameVar ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑥.
    Case 3. SEvalOrA – 𝜎 ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑡 1 ⊣ 𝜎 ′′, R:
    By SEvalOrA 𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, R.
    Suppose ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R and 𝑉 ′ (𝑔(𝜎 ′′ )) = true. Then 𝑉 ′ (𝑔(𝜎 ′ )) = true since 𝑔(𝜎 ′′ ) = 𝑔(𝜎 ′ ) &&
𝑡 1 =⇒ 𝑔(𝜎 ′ ) by SEvalOrA. Then by induction ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ .
    Now ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′′ since 𝜎 ′′ = 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡 1 ] by SEvalOrA and 𝑉 ′ (𝑔(𝜎 ′′ )) = true by
assumption.
    By induction ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ 𝑉 ′ (𝑡 1 ). But now 𝑉 ′ (𝑡 1 ) = true since 𝑔(𝜎 ′′ ) = 𝑔(𝜎 ′ ) && 𝑡 1 =⇒ 𝑡 1 .
Thus ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ true.
    Then by EvalOrA ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 || 𝑒 2 ⇓ true and 𝑉 ′ (𝑡 1 ) = true.
    By induction ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1 . Thus ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1 || 𝑒 2 by FrameOrA since ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓
true.
    Case 4. SEvalOrB – 𝜎 ⊢ 𝑒 1 ∨ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′, R 1 ∪ R 2 :
    By SEvalOrB 𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, R 1 and 𝜎ˆ ′ ⊢ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′, R 2 , where 𝜎ˆ ′ = 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && ! 𝑡 1 ].
    Now suppose ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R 1 ∪ R 2 and 𝑉 ′ (𝑔(𝜎 ′′ )) = true. By lemma 23 ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R 1 (thus
⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R 1 ) and ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R 2 .
    Also, by lemma 24, 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎ˆ ′ ) = 𝑔(𝜎 ′ ) && ! 𝑡 1 =⇒ 𝑔(𝜎 ′ ). Therefore 𝑉 ′ (𝑔(𝜎 ′ )) =
𝑉 (𝑔(𝜎 ′ )) = true, and 𝑉 ′ (𝑔(𝜎 ′′ )) = true by assumption.
  ′

    Now by induction ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ . Also 𝑉 ′ (𝑔(𝜎ˆ ′ )) = true since 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎 ′ ). Therefore
⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎ˆ ′ . Then also by induction ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′′ .
    By induction ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ 𝑉 ′ (𝑡 1 ) and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 2 ⇓ 𝑉 ′ (𝑡 2 ). But now 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎ˆ ′ ) =
𝑔(𝜎 ′ ) && ! 𝑡 1 =⇒ ! 𝑡 1 , thus 𝑉 ′ (𝑡 1 ) = false. Therefore ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ false.
    Thus ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑉 ′ (𝑡 2 ) by EvalOrB.
    By induction ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1 and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 2 . Thus ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1 || 𝑒 2 by FrameOrB
since ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ false.
    Case 5. SEvalAndA – 𝜎 ⊢ 𝑒 1 ∧ 𝑒 2 ⇓ 𝑡 1 ⊣ 𝜎 ′′, R: Similar to case 3.
    Case 6. SEvalAndB – 𝜎 ⊢ 𝑒 1 ∧ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′, R 1 ∪ R 2 : Similar to case 4.
    Case 7. SEvalOp – 𝜎 ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓ 𝑡 1 ⊕ 𝑡 2 ⊣ 𝜎 ′′, R 1 ∪ R 2 :
    By SEvalOp 𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, R 1 and 𝜎 ′ ⊢ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′, R 2 .
    Now suppose ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R 1 ∪ R 2 and 𝑉 ′ (𝑔(𝜎 ′′ )) = true. By lemma 23 ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R 1 and
⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R 2 .
    Also, by lemma 24, 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎 ′ ). Therefore 𝑉 ′ (𝑔(𝜎 ′ )) = 𝑉 ′ (𝑔(𝜎 ′ )) = true, and 𝑉 ′ (𝑔(𝜎 ′′ )) =
true by assumption.
    Now by induction ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ , and then also by induction ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′′ .
    By induction ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ 𝑉 ′ (𝑡 1 ) and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 2 ⇓ 𝑉 ′ (𝑡 2 ). Therefore ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓
𝑉 (𝑡 1 ) ⊕ 𝑉 ′ (𝑡 2 ) and 𝑉 ′ (𝑡 1 ) ⊕ 𝑉 ′ (𝑡 2 ) = 𝑉 ′ (𝑡 1 ⊕ 𝑡 2 ).
  ′

    By induction ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1 and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 2 . Thus ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 1 ⊕ 𝑒 2 by FrameOp.
    Case 8. SEvalNeg – 𝜎 ⊢ ! 𝑒 ⇓ ! 𝑡 ⊣ 𝜎 ′, R:
    By SEvalNeg 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R.
    Suppose that ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R and 𝑉 ′ (𝑔(𝜎 ′ )) = true.
54                                                                                                        Torek et al.


    Now ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ by induction.
    Also by induction ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡). Thus ⟨𝐻, 𝜌⟩ ⊢ ! 𝑒 ⇓ ¬𝑉 ′ (𝑡) by EvalNeg and 𝑉 ′ (! 𝑡) =
¬𝑉 ′ (𝑡).
    By induction ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒, and thus ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm ! 𝑒 by FrameNeg.
    Case 9. SEvalField: 𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′, R
    By SEvalField 𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′, R.
    Suppose that ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R and 𝑉 ′ (𝑔(𝜎 ′ )) = true.
    Then ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ by induction.
    Also by induction ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡𝑒 ). By SEvalField 𝑔(𝜎 ′ ) =⇒ 𝑡𝑒 == 𝑡𝑒′ , therefore 𝑉 ′ (𝑡𝑒 ) =
𝑉 (𝑡𝑒′ ). Also by SEvalField ⟨𝑓 , 𝑡𝑒′ , 𝑡⟩ ∈ H(𝜎 ′ ). Therefore 𝑉 ′ (𝑡) = 𝐻 (𝑉 ′ (𝑡𝑒′ ), 𝑓 ) = 𝐻 (𝑉 ′ (𝑡𝑒 ), 𝑓 ) since
  ′

⟨𝐻, 𝜌, 𝛼⟩ 𝑉 ′ 𝜎 ′ .
    Thus ⟨𝐻, 𝜌⟩ ⊢ 𝑒.𝑓 ⇓ 𝐻 (𝑉 ′ (𝑡𝑒 ), 𝑓 ) by EvalField and 𝐻 (𝑉 ′ (𝑡𝑒 ), 𝑓 ) = 𝑉𝜎 ′ (𝑡).
    By induction ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒. Also, since ⟨𝑓 , 𝑡𝑒′ , 𝑡⟩ ∈ H(𝜎 ′ ) and ⟨𝐻, 𝜌, 𝛼⟩ 𝑉 ′ 𝜎 ′ , ⟨𝑉 ′ (𝑡𝑒′ ), 𝑓 ⟩ =
⟨𝑉 ′ (𝑡𝑒 ), 𝑓 ⟩ ∈ 𝛼. By AssertAcc, ⟨𝐻, 𝛼, 𝜌⟩ ⊨ acc(𝑒.𝑓 ) since ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡𝑒 ). Thus by FrameField
⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒.𝑓 .
    Case 10. SEvalFieldOptimistic – 𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′, R: Similar to case 9.
    Case 11. SEvalFieldImprecise – 𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′, R; ⟨𝑡𝑒 , 𝑓 ⟩:
    By SEvalFieldImprecise 𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′, R, 𝑡 = fresh, and 𝜎 ′′ = 𝜎 ′ [H = H (𝜎 ′ ); ⟨𝑓 , 𝑡𝑒 , 𝑡⟩].
    Suppose ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R; ⟨𝑡𝑒 , 𝑓 ⟩ and 𝑉 ′ (𝑔(𝜎 ′′ )) = true, thus ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R by lemma 23. Then
𝑉 (𝑔(𝜎 ′′ )) = 𝑉 ′ (𝑔(𝜎 ′ )) = true.
  ′

    Then by induction ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ , thus ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ .
    By lemma 23 ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ {⟨𝑡𝑒 , 𝑓 ⟩} and thus ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ ⟨𝑡𝑒 , 𝑓 ⟩. Then by CheckAcc ⟨𝑉 ′ (𝑡𝑒 ), 𝑓 ⟩ ∈ 𝛼.
    By definition 36 𝐻 (𝑉 ′ (𝑡𝑒 ), 𝑓 ) = 𝑉 ′ (𝑡), and also ⟨𝑉 ′ (𝑡𝑒 ), 𝑓 ⟩ ∈ 𝛼 and ⟨𝐻, 𝛼⟩ 𝑉 ′ H (𝜎 ′ ), thus
⟨𝐻, 𝛼⟩ 𝑉 ′ H (𝜎 ′ ); ⟨𝑓 , 𝑡𝑒 , 𝑡⟩.
  Then ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′′ since 𝜎 ′ and 𝜎 ′′ differ only in their H components and H (𝜎 ′′ ) =
H (𝜎 ′ ); ⟨𝑓 , 𝑡𝑒 , 𝑡⟩.
  By induction ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡𝑒 ). As shown before, 𝐻 (𝑉 ′ (𝑡𝑒 ), 𝑓 ) = 𝑉 ′ (𝑡). Thus by EvalField
⟨𝐻, 𝜌⟩ ⊢ 𝑒.𝑓 ⇓ 𝑉 ′ (𝑡).
  By induction ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒. Also, as shown before, ⟨𝑉 ′ (𝑡𝑒 ), 𝑓 ⟩ ∈ 𝛼. By AssertAcc, ⟨𝐻, 𝛼, 𝜌⟩ ⊨
acc(𝑒.𝑓 ) since ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡𝑒 ). Thus by FrameField ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒.𝑓 .
  Case 12. SEvalFieldFailure – 𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′, {⊥}:
  ⟨𝐻, 𝛼⟩ ⊢𝑉 {⊥} cannot hold. Since the assumptions cannot be satisfied, the statement holds
vacuously.


     Case 13. SEvalUnfoldingPrecise – 𝜎1 ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎6, R 1 ∪ R 2 ∪ R 3 :
     By the induction hypothesis, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎2 , ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡), and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 with
𝑉 ′ (𝑔(𝜎2 )) = true. Then, by Lemma 43, ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝑝 (𝑒) and ⟨𝐻, 𝛼 \ T𝑝 (𝑒)U ⟨𝐻, 𝜌 ⟩ , 𝜌⟩                    𝑉′
                                                                                                                   𝜎3
with 𝑉 ′ (𝑔(𝜎3 ))   = true. By Lemma 31, ⟨𝐻, 𝛼, 𝜌⟩        𝑉′
                                                                   𝜎4 with 𝑉 ′ (𝑔(𝜎4 ))   = true. Then, by the
induction hypothesis, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′                    ′
                                              𝜎5 with 𝑉 (𝑔(𝜎5 ))
                                                               = true. Then, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎6 since
H(𝜎6 ) ⊆ H(𝜎5 ) and H (𝜎6 ) = ∅. Similarly, 𝑔(𝜎6 ) = 𝑔(𝜎5 ) so 𝑉 ′ (𝑔(𝜎6 )) = 𝑉 ′ (𝑔(𝜎5 )) = true, as
desired. Furthermore, by EvalUnfolding, ⟨𝐻, 𝛼⟩ ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓ 𝑉 ′ (𝑡 0 ). By the induction
hypothesis, ⟨𝐻, 𝜌⟩ ⊢ 𝑒 0 ⇓ 𝑉 ′ (𝑡 0 ) and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 0 . By Lemma 43, ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝑝 (𝑒), so by
definition of FrameUnfolding, ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm unfolding 𝑝 (𝑒) in 𝑒 0 as desired.
  Case 14. SEvalUnfoldingImplicitPrecise – 𝜎1 ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎2, R:
Gradually Verifying Unfolding Expressions & Pure Functions                                                      55



    Since ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎1 , by the induction hypothesis ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎2 . By Definition 36, ⟨𝐻, 𝜌⟩ ⊢
𝑒 0 ⇓ 𝑉 ′ (𝑡), so therefore ⟨𝐻, 𝜌⟩ ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓ 𝑉 ′ (𝑡).
    Inductively, ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 0 and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmI 𝑝 (𝑒), and since ⟨𝑝, 𝑡⟩ ∈ H(𝜎2 ) ∪ H (𝜎2 ), by the
definition of heap correspondence and AssertPredicate, ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝑝 (𝑒). Therefore, ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm
unfolding 𝑝 (𝑒) in 𝑒 0 .
    Case 15. SEvalUnfoldingImplicitImprecise – 𝜎1 ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎3, R ′ :
    Similar to the case for SEvalUnfoldingImplicitPrecise. To show heap correspondence with H ′ ,
recall that ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ ⟨𝑝, 𝑡⟩, showing that the predicate assertion holds in the corresponding state.
    Case 16. SEvalUnfoldingImplicitFailure – 𝜎1 ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎2, {⊥}:
    The run-time check set {⊥} is unsatisfiable, so the conclusion holds vacuously.
    Case 17. SEvalFunctionExplicit – 𝜎1 ⊢ 𝑓 (𝑒) ⇓ 𝑡 ′ ⊣ 𝜎6, R 1 ∪ R 2 ∪ R 3 :
    By the induction hypothesis, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎2 , ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡), and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 with
𝑉 ′ (𝑔(𝜎2 )) = true. Then, by Lemma 43, ⟨𝐻, 𝛼, 𝜌⟩ ⊨ func_pre(𝑓 ) and ⟨𝐻, 𝛼\Tfunc_pre(𝑓 )U ⟨𝐻, 𝜌 ⟩ , 𝜌⟩ 𝑉 ′
𝜎3 with 𝑉 ′ (𝑔(𝜎3 )) = true. By Lemma 31, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎4 with 𝑉 ′ (𝑔(𝜎4 )) = true. Then, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′
𝜎5 by the induction hypothesis. Then, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎6 because H (𝜎6 ) = H (𝜎5 ) and H(𝜎6 ) = H(𝜎2 ).
   Since ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmI func_pre(𝑓 ) inductively and ⟨𝐻, 𝛼, 𝜌⟩ ⊨ func_pre(𝑓 )
from the consume step, ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm func_pre(𝑓 ).
   Case 18. SEvalFunctionImplicit – 𝜎1 ⊢ 𝑓 (𝑒) ⇓ 𝑡 ′ ⊣ 𝜎4, R 1 ∪ R 2 ∪ R 3 :
   Because ⟨𝐻, 𝛼⟩ ⊢𝑉 R 2 where R 2 arose as a result of consuming func_pre(𝑓 ), in the corre-
sponding state it must be the case that ⟨𝐻, 𝛼, 𝜌⟩ ⊨ func_pre(𝑓 ). Inductively, ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 and
⟨𝐻, 𝛼, 𝜌⟩ ⊢frmI func_pre(𝑓 ), so ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑓 (𝑒) by FrameFunction. By Definition 36, ⟨𝐻, 𝜌 ′ ⟩ ⊢
func_body(𝑓 ) ⇓ 𝑉 ′ (𝑡 ′ ) so by EvalFunction, ⟨𝐻, 𝜌⟩ ⊢ 𝑓 (𝑒) ⇓ 𝑉 ′ (𝑡 ′ ). Then, to show ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎4 ,
it suffices to show that ⟨𝐻, 𝛼⟩ 𝑉 ′ H (𝜎4 ) because H(𝜎4 ) = H(𝜎1 ) and 𝛾 (𝜎4 ) = 𝛾 (𝜎1 ) by Lemma 25
where ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎1 . Furthermore, since H (𝜎4 ) = H (𝜎2 ) ∪ (𝑠 ′ \ H(𝜎2 )) where ⟨𝐻, 𝛼⟩ 𝑉 H (𝜎2 ),
it suffices to show ⟨𝐻, 𝛼⟩ 𝑉 ′ 𝑠 ′ \ H(𝜎2 ). For each heap chunk in 𝑠 ′ \ H(𝜎2 ), there is a corresponding
run-time check ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ 𝑟 showing that the heap chunk holds in the corresponding state by
CheckAcc and CheckPred. Accordingly, ⟨𝐻, 𝛼⟩ ′ 𝑠 ′ \ H(𝜎2 ) as desired.
                                                     𝑉


                                                                                                                □

Lemma 27 (Progress). If 𝑉 is some initial valuation and 𝑉 (𝑔(𝜎)) = true, then for some 𝜎 ′ , 𝑡, and
R,
                           𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R and 𝑉 ′ (𝑔(𝜎 ′ )) = true
where 𝑉 ′ = 𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R | 𝐻, 𝜌] for some 𝐻 .
    Proof. By induction on 𝑒.
    Case 1. 𝑙 ∈ Literal: By SEvalLiteral 𝜎 ⊢ 𝑙 ⇓ _ ⊣ 𝜎, _. Then 𝑉 ′ (𝑔(𝜎)) = true by assumptions.
    Case 2. 𝑥 ∈ Var: By SEvalVar 𝜎 ⊢ 𝑥 ⇓ _ ⊣ 𝜎, _. Then 𝑉 ′ (𝑔(𝜎)) = true by assumptions.
    Case 3. 𝑒.𝑓 where 𝑒 ∈ Expr, 𝑓 ∈ Field: By induction, 𝑒 ⊢ 𝑡𝑒 ⇓ 𝜎 ⊣ R, and 𝑉 ′ (𝑔(𝜎 ′ )) = true
where 𝑉 ′ is the corresponding         valuation. Then one of the following must apply:
    Case 3(a). If ∃ 𝑡𝑒′ , 𝑡 : 𝑔(𝜎 ′ ) =⇒ 𝑡𝑒′ == 𝑡𝑒 ∧ ⟨𝑓 , 𝑡𝑒′ , 𝑡⟩ ∈ H(𝜎 ′ ), then SEvalField applies and thus
                                                 

𝜎 ⊢ 𝑒.𝑓 ⇓ _ ⊣ 𝜎 ′, _. Let 𝜎 ′′ = 𝜎 ′.
    Case 3(b). Otherwise,  𝑡𝑒′ , 𝑡 : 𝑔(𝜎 ′ ) =⇒ 𝑡𝑒′ ==𝑡𝑒 ∧⟨𝑓 , 𝑡𝑒′ , 𝑡⟩ ∈ H(𝜎 ′ ). Then, if ∃ 𝑡𝑒′ , 𝑡 : 𝑔(𝜎 ′ ) =⇒
                                                                                                        

𝑡𝑒′ ==𝑡𝑒 ∧ ⟨𝑓 , 𝑡𝑒′ , 𝑡⟩ ∈ H (𝜎 ′ ), SEvalFieldOptimistic applies and thus 𝜎 ⊢ 𝑒.𝑓 ⇓ _ ⊣ 𝜎 ′, _. Let 𝜎 ′′ = 𝜎 ′ .
        
56                                                                                                              Torek et al.


     Case 3(c). Otherwise,  𝑡𝑒′ , 𝑡 : 𝑔(𝜎 ′ ) =⇒ 𝑡𝑒′ == 𝑡𝑒 ∧ ⟨𝑓 , 𝑡𝑒′ , 𝑡⟩ ∈ H(𝜎 ′ ) ∪ H (𝜎 ′ ). Then if 𝜄 (𝜎 ′ ),
                                                                

SEvalFieldImprecise applies. In this case, 𝜎 ⊢ 𝑒.𝑓 ⇓ _ ⊣ 𝜎 ′′, _ where           𝑔(𝜎 ′′ ) = 𝑔(𝜎 ′ ).
     Case 3(d). Otherwise, ¬𝜄 (𝜎 ) and  𝑡𝑒 , 𝑡 : 𝑔(𝜎 ) =⇒ 𝑡𝑒 == 𝑡𝑒 ∧ ⟨𝑓 , 𝑡𝑒′ , 𝑡⟩ ∈ H(𝜎 ′ ) ∪ H (𝜎 ′ ). Thus
                                      ′        ′         ′           ′
                                                                             

SEvalFieldFailure applies and thus 𝜎 ⊢ 𝑒.𝑓 ⇓ _ ⊣ 𝜎 ′, _. Let 𝜎 ′′ = 𝜎 ′ .
     In all of these subcases, 𝜎 ⊢ 𝑒.𝑓 ⇓ _ ⊣ 𝜎 ′′, _ where 𝑔(𝜎 ′′ ) = 𝑔(𝜎 ′ ), and thus 𝑉 ′ (𝑔(𝜎 ′′ )) =
𝑉 (𝑔(𝜎 ′ )) = true. By definition 36, in all of these subcases 𝑉 [𝜎 ⊢ 𝑒.𝑓 ⇓ _ ⊣ 𝜎 ′′, _ | 𝐻 ] extends 𝑉 ′ .
   ′

     Case 4. 𝑒 1 ⊕ 𝑒 2 ; 𝑒 1, 𝑒 2 ∈ Expr: By induction 𝜎 ⊢ 𝑒 1 ⇓ _ ⊣ 𝜎 ′, _ for some 𝑒 1, 𝜎 ′ where 𝑉 ′ is
the corresponding valuation and 𝑉 ′ (𝑔(𝜎 ′ )) = true. Then by induction 𝜎 ′ ⊢ 𝑒 2 ⇓ _ ⊣ 𝜎 ′′, where
𝑉 ′′ is the corresponding valuation extending 𝑉 ′ and 𝑉 ′′ (𝑔(𝜎 ′′ )) = true. Finally, by SEvalOp
𝜎 ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓ _ ⊣ 𝜎 ′′, _. By definition 36, 𝑉 [𝜎 ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓ _ ⊣ 𝜎 ′′, _ | 𝐻 ] extends 𝑉 ′′ .
     Case 5. 𝑒 1 || 𝑒 2 ; 𝑒 1, 𝑒 2 ∈ Expr: By induction 𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, _ for some 𝑒 1, 𝑡𝑒 , 𝜎 ′ where 𝑉 ′ is the
corresponding valuation and 𝑉 ′ (𝑔(𝜎 ′ )) = true. Then one of the following cases must apply since
the program is well-typed:
     Case 5(a). 𝑉 ′ (𝑡 1 ) = true: Then by SEvalOrA, 𝜎 ⊢ 𝑒 1 ∨ 𝑒 2 ⇓ 𝑡 1 ⊣ 𝜎 ′′, _ where 𝑔(𝜎 ′′ ) = 𝑔(𝜎 ′ ) && 𝑡 1 .
Let 𝑉 ′′ be the corresponding valuation. Now 𝑉 ′′ (𝑔(𝜎 ′′ )) = 𝑉 ′′ (𝑔(𝜎 ′ )) ∧ 𝑉 ′′ (𝑡 1 ) = true, which
completes the proof.
     Case 5(b). 𝑉 ′ (𝑡 1 ) = false: Let 𝜎ˆ ′ = 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && ! 𝑡 1 ]. Then 𝑉 ′ (𝑔(𝜎ˆ ′ )) = 𝑉 ′ (𝜎 ′ ) ∧ ¬𝑉 ′ (𝑡 1 ) =
true. By induction 𝜎ˆ ′ ⊢ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′, _ for some 𝑒 2, 𝑡 2, 𝜎 ′′ where 𝑉 ′′ is the corresponding valuation
and 𝑉 ′′ (𝑔(𝜎 ′′ )) = true. Finally, by SEvalOrB, 𝜎 ⊢ 𝑒 1 || 𝑒 2 ⇓ _ ⊣ 𝜎 ′′, _. By definition 36 𝑉 [𝜎 ⊢
𝑒 1 || 𝑒 2 ⇓ _ ⊣ 𝜎 ′′, _ | 𝐻 ] extends 𝑉 ′′ .
     Case 6. 𝑒 1 && 𝑒 2 ; 𝑒 1, 𝑒 2 ∈ Expr: Similar to case 5.
     Case 7. ! 𝑒; 𝑒 ∈ Expr: By induction 𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎 ′, _ and 𝑉 ′ (𝜎 ′ ) = true where 𝑉 ′ is the
corresponding derivation. Then by SEvalNeg, 𝜎 ⊢ ! 𝑒 ⇓ _ ⊣ 𝜎 ′, _ and the corresponding valuation
extends 𝑉 ′ by definition 36.


   Case 8. unfolding 𝑝 (𝑒) in 𝑒 0 where 𝑝 ∈ Predicate and 𝑒, 𝑒 0 ∈ Expr:
   By the induction hypothesis, 𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2, R 1 with 𝑉 ′ (𝑔(𝜎2 )) = true.
   Case 8(a). 𝑝 ∈ V (𝜎1 ), ⟨𝑝, 𝑡⟩ ∈ H(𝜎2 )∪H (𝜎2 ): In this case, SEvalUnfoldingImplicitPrecise applies.
The final state is 𝜎2 so 𝑉 ′ (𝑔(𝜎2 )) = true as desired.
   Case 8(b). 𝑝 ∈ V (𝜎1 ), ⟨𝑝, 𝑡⟩ ∉ H(𝜎2 )∪H (𝜎2 ), 𝜄 (𝜎2 ): In this case, SEvalUnfoldingImplicitImprecise
applies. Since 𝑔(𝜎3 ) = 𝑔(𝜎2 ), 𝑉 ′ (𝑔(𝜎3 )) = 𝑉 ′ (𝑔(𝜎2 )) = true.
   Case 8(c). 𝑝 ∈ V (𝜎1 ), ⟨𝑝, 𝑡⟩ ∉ H(𝜎2 ) ∪H (𝜎2 ), ¬𝜄 (𝜎2 ): In this case, SEvalUnfoldingImplicitFailure
applies. The final state is 𝜎2 so 𝑉 ′ (𝑔(𝜎2 )) = true as desired.
   Case 8(d). 𝑝 ∉ V (𝜎1 ), ¬𝜄 (𝜎1 ): In this case, SEvalUnfoldingPrecise applies, so by Lemma 45,
𝜎2 ⊢ 𝑝 (𝑒) ▷ 𝜎3, R 2 with 𝑉 ′ (𝑔(𝜎3 )) = true. Since ⟨𝑝, 𝑡⟩ holds in 𝜎2 due to the consume operation, in
the corresponding state the predicate assertion must hold, so by Lemma 32, 𝜎3 ⊢ predicate(𝑝) ◁ 𝜎4
with 𝑉 ′ (𝑔(𝜎4 )). By the induction hypothesis, 𝜎4 ⊢ 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎5, R 3 with 𝑉 ′ (𝑔(𝜎5 ) − true. Then,
since 𝑔(𝜎5 ) = 𝑔(𝜎6 ), 𝑉 ′ (𝑔(𝜎6 )) = 𝑉 ′ (𝑔(𝜎5 )) = true.
   Case 8(e). 𝑝 ∉ V (𝜎1 ), 𝜄 (𝜎1 ): In this case, SEvalUnfoldingImpreciseA or SEvalUnfoldingImpreciseB.
This case is similar to the previous case, except for the information that remains in the optimistic
heap at the end.
   Case 9. 𝑓 (𝑒) where 𝑓 ∈ Function and 𝑒 ∈ Expr: By the induction hypothesis, 𝜎1 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎2, R 1
with 𝑉2 (𝑔(𝜎2 )) = true. Then, by Lemma 45, 𝜎2 [𝛾 = 𝛾 (𝜎2 ) [𝑥 ↦→ 𝑡]] ⊢ func_pre(𝑓 ) ▷ 𝜎3, _ where
𝑉3 (𝑔(𝜎3 )) = true.
   Case 9(a). 𝑓 ∉ V (𝜎1 ): Because the precondition holds due to the consume operation, in the
corresponding state the dynamic assertion must hold, so by Lemma 32, 𝜎3 ⊢ predicate(𝑝) ◁ 𝜎4 with
Gradually Verifying Unfolding Expressions & Pure Functions                                                           57


𝑉 ′ (𝑔(𝜎4 )). By induction, 𝜎4 [H = H′, H = H ′, V = V (𝜎3 ) ∪ {𝑓 }] ⊢ func_body(𝑓 ) ⇓ 𝑡 ′ ⊣ 𝜎5, _ with
𝑉5 (𝑔(𝜎5 )). By definition, 𝑔(𝜎5 ) =⇒ 𝑔(𝜎6 ) so 𝑉5 (𝑔(𝜎6 )) = true.
    Case 9(b). 𝑓 ∈ V (𝜎1 ): By definition, 𝑔(𝜎3 ) =⇒ 𝑔(𝜎4 ) so 𝑉3 (𝑔(𝜎4 )) = true.


                                                                                                                     □


Lemma 28 (Correspondence). Let 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _ with corresponding valuation 𝑉 ′ . If ⟨𝐻, 𝛼, 𝜌⟩ 𝑉
𝜎 such that T𝑒U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼 and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣 then
                                           ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′     𝑣 = 𝑉 ′ (𝑡)
     Proof. By induction on 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _:
     Case 1. SEvalLiteral – 𝜎 ⊢ 𝑙 ⇓ 𝑙 ⊣ 𝜎, _:
     Then 𝑉 ′ = 𝑉 , so trivially ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ . In addition ⟨𝐻, 𝜌⟩ ⊢ 𝑙 ⇓ 𝑙 and by definition 𝑉 (𝑙) =
   ′
𝑉 (𝑙) = 𝑙.
     Case 2. SEvalVar – 𝜎 ⊢ 𝑥 ⇓ 𝛾 (𝜎) (𝑥) ⊣ 𝜎, _:
     Then 𝑉 ′ = 𝑉 , so trivially ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ . Therefore 𝜌 𝑉 ′ 𝛾 (𝜎), and so 𝜌 (𝑥) = 𝑉 ′ (𝛾 (𝜎) (𝑥)).
Then since ⟨𝐻, 𝛼⟩ ⊢ 𝑥 ⇓ 𝜌 (𝑥), ⟨𝐻, 𝛼⟩ ⊢ 𝑥 ⇓ 𝑉 ′ (𝛾 (𝜎) (𝑥)).
     Case 3. SEvalOrA – 𝜎 ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑡 1 ⊣ 𝜎 ′′, _:
     By SEvalOrA, 𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, _, and the corresponding valuation for this case is 𝑉 ′ = 𝑉 [𝜎 ⊢
𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, _ | 𝐻 ]. Since ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎, by lemma 27, 𝑉 ′ (𝑔(𝜎 ′′ )) = true and 𝑉 ′ (𝑔(𝜎 ′ ) = true.
Then, since 𝑔(𝜎 ′′ ) = 𝑔(𝜎 ′ ) && 𝑡 1 , 𝑉 ′ (𝑡 1 ) = true.
     Now since ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑣, either EvalOrA or EvalOrB must apply. In either case, ⟨𝐻, 𝜌⟩ ⊢
𝑒 1 ⇓ 𝑣 1 for some 𝑣 1 . Since T𝑒 1 || 𝑒 2 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼, by definition 5, T𝑒 1 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼. Then by induction
⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ 𝑉 ′ (𝑡 1 ).
    Since 𝜎 ′′ and 𝜎 ′ differ only in their 𝑔 components, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′′ as 𝑉 ′ (𝑔(𝜎 ′ )) = true. In
addition, since 𝑉 ′ (𝑡 1 ) = true, ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ true, which means EvalOrA must apply. Then
⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 || 𝑒 2 ⇓ true, which is 𝑉 ′ (𝑡 1 ).
    Case 4. SEvalOrB – 𝜎 ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′, _:
    By SEvalOrB, 𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, _. Let 𝑉 ′ = 𝑉 [𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, _ | 𝐻 ]. Let 𝜎ˆ = 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) &&! 𝑡 1 ].
Also by SEvalOrB, 𝜎ˆ ⊢ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′, _ and the corresponding valuation for this case is 𝑉 ′′ = 𝑉 ′ [𝜎ˆ ⊢
𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′, _ | 𝐻 ].
    Since ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎, by lemma 27, 𝑉 ′ (𝑔(𝜎 ′ )) = true and 𝑉 ′′ (𝑔(𝜎 ′′ )) = true. Then by lemma 24,
𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎)    ˆ = 𝑔(𝜎 ′ ) && ! 𝑡 1 . Since corresponding valuations must extend, 𝑉 ′′ (𝑡 1 ) = 𝑉 ′ (𝑡 1 ) =
false.
    Now since ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑣, either EvalOrA or EvalOrB must apply. In either case, ⟨𝐻, 𝜌⟩ ⊢
𝑒 1 ⇓ 𝑣 1 for some 𝑣 1 . Since T𝑒 1 || 𝑒 2 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼, by definition 5, T𝑒 1 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼. Then by induction
⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ 𝑉 ′ (𝑡 1 ).
   By lemma 27 𝑉 ′ (𝑔(𝜎 ′ )) = true. Then 𝜎ˆ and 𝜎 ′ differ only in their 𝑔 components, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎.    ˆ
In addition, since 𝑉 ′ (𝑡 1 ) = false, ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ false, which means that EvalOrB must apply.
Therefore, ⟨𝐻, 𝜌⟩ ⊢ 𝑒 2 ⇓ 𝑣 2 for some 𝑣 2 . In addition, by definition 5 and since T𝑒 1 || 𝑒 2 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼,
T𝑒 2 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼. Then by induction, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′′ 𝜎 ′′ and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 2 ⇓ 𝑉 ′′ (𝑡 2 ). By EvalOrB,
⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑣 2 , and 𝑣 2 = 𝑉 ′′ (𝑡 2 ).
   Case 5. SEvalAndA – 𝜎 ⊢ 𝑒 1 && 𝑒 2 ⇓ 𝑡 1 ⊣ 𝜎 ′′, _:
58                                                                                                         Torek et al.


    By SEvalAndA, 𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, _, and the corresponding valuation for this case is 𝑉 ′ = 𝑉 [𝜎 ⊢
𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, _ | 𝐻 ]. Since ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎, by lemma 27 𝑉 ′ (𝑔(𝜎 ′′ )) = true and 𝑉 ′ (𝑔(𝜎 ′ )) = true.
Then, since 𝑔(𝜎 ′′ ) = 𝑔(𝜎 ′ ) && ! 𝑡 1 , 𝑉 ′ (𝑡 1 ) = false.
    Now since ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 && 𝑒 2 ⇓ 𝑣, either EvalAndA or EvalAndB must apply. In either case,
⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ 𝑣 1 for some 𝑣 1 . Since T𝑒 1 && 𝑒 2 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼, by definition 5, T𝑒 1 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼. Then by
induction ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ 𝑉 ′ (𝑡 1 ).
   Since 𝜎 ′′ and 𝜎 ′ differ only in their 𝑔 components, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′′ as 𝑉 ′ (𝑔(𝜎 ′ )) = true. In
addition, since 𝑉 ′ (𝑡 1 ) = false, ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ false, which means EvalAndA must apply. Then
⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 && 𝑒 2 ⇓ false, which is 𝑉 ′ (𝑡 1 ).
   Case 6. SEvalAndB – 𝜎 ⊢ 𝑒 1 && 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′, _:
   By SEvalAndB 𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, _. Let 𝑉 ′ = 𝑉 [𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, _ | 𝐻 ]. Let 𝜎ˆ = 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡 1 ].
Also by SEvalAndB, 𝜎ˆ ⊢ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′, _ and the corresponding valuation for this case is 𝑉 ′′ =
𝑉 ′ [𝜎ˆ ⊢ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′, _ | 𝐻 ].
   Since ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎, by lemma 27, 𝑉 ′ (𝑔(𝜎 ′ )) = true = 𝑉 ′′ (𝑔(𝜎 ′ )) and 𝑉 ′′ (𝑔(𝜎 ′′ )) = true.
Then by lemma 24, 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎ˆ′ ) = 𝑔(𝜎 ′ ) && 𝑡 1 . Since corresponding valuations must extend,
𝑉 ′′ (𝑡 1 ) = 𝑉 ′ (𝑡 1 ) = true.
   Now since ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 && 𝑒 2 ⇓ 𝑣, either EvalAndA or EvalAndB must apply. In either case,
⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ 𝑣 1 for some 𝑣 1 . Since T𝑒 1 && 𝑒 2 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼, by definition 5, T𝑒 1 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼. Then by
induction ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ 𝑉 ′ (𝑡 1 ).
    By lemma 27 𝑉 ′ (𝑔(𝜎 ′ )) = true. Then since 𝜎ˆ and 𝜎 ′ differ only in their 𝑔 components, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′
 ˆ In addition, since 𝑉 ′ (𝑡 1 ) = true, ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ true, which means that EvalAndB must apply.
𝜎.
Therefore, ⟨𝐻, 𝜌⟩ ⊢ 𝑒 2 ⇓ 𝑣 2 for some 𝑣 2 . Also since ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ true and T𝑒 1 && 𝑒 2 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼,
T𝑒 2 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼. Then by induction, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′′ 𝜎 ′′ and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 2 ⇓ 𝑉 ′′ (𝑡 2 ). By EvalAndB,
⟨𝐻, 𝛼⟩ ⊢ 𝑒 1 && 𝑒 2 ⇓ 𝑣 2 , and 𝑣 2 = 𝑉 ′′ (𝑡 2 ).
    Case 7. SEvalOp – 𝜎 ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓ 𝑡 1 ⊕ 𝑡 2 ⊣ 𝜎 ′′, _:
    By SEvalOp 𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, _. Let 𝑉 ′ = 𝑉 [𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, _ | 𝐻 ]. Also by SEvalOP,
𝜎 ⊢ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′, _. Let 𝑉 ′′ = 𝑉 ′ [𝜎 ′ ⊢ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′, _ | 𝐻 ]. Then 𝑉 ′′ is the corresponding valuation
  ′

for this case.
    Since ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓ 𝑣 for some 𝑣, by EvalOP ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ 𝑣 1 for some 𝑣 1 and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 2 ⇓ 𝑣 2
for some 𝑣 2 . In addition, since T𝑒 1 ⊕ 𝑒 2 U ⟨𝐻, 𝛼 ⟩ ⊆ 𝛼, by definition 5, T𝑒 1 U ⟨𝐻, 𝛼 ⟩ ⊆ 𝛼 and T𝑒 2 U ⟨𝐻, 𝛼 ⟩ ⊆ 𝛼.
Then by induction ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ 𝑉 ′ (𝑡 1 ). As such, by induction ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′′
𝜎 ′′ and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 2 ⇓ 𝑉 ′′ (𝑡 2 ). Since 𝑉 ′′ extends 𝑉 ′ , by EvalOP, ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓ 𝑉 ′′ (𝑡 1 ) ⊕ 𝑉 ′′ (𝑡 2 )
and 𝑉 ′′ (𝑡 1 ) ⊕ 𝑉 ′′ (𝑡 2 ) = 𝑉 ′′ (𝑡 1 ⊕ 𝑡 2 ).
    Case 8. SEvalNeg – 𝜎 ⊢ ! 𝑒 ⇓ ! 𝑡 ⊣ 𝜎 ′, _:
    By SEvalNeg 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _, and the corresponding valuation for this case is 𝑉 ′ = 𝑉 [𝜎 ⊢
𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _ | 𝐻 ]. Since ⟨𝐻, 𝜌⟩ ⊢ ! 𝑒 ⇓ 𝑣 for some 𝑣, by EvalNeg ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣 ′ for some 𝑣 ′ . In
addition, since T! 𝑒U ⟨𝐻, 𝛼 ⟩ ⊆ 𝛼, by definition 5, T𝑒U ⟨𝐻, 𝛼 ⟩ ⊆ 𝛼. Then by induction ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′
and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡). Then by EvalNeg ⟨𝐻, 𝜌⟩ ⊢ ! 𝑒 ⇓ ¬𝑉 ′ (𝑡) and ¬𝑉 ′ (𝑡) = 𝑉 ′ (! 𝑡).
    Case 9. SEvalField – 𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′, _:
    By SEvalField, 𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′, _, and the corresponding valuation for this case is 𝑉 ′ = 𝑉 [𝜎 ⊢ 𝑒 ⇓
𝑡𝑒 ⊣ 𝜎 ′, _ | 𝐻 ].
    Since T𝑒.𝑓 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼, by definition 5 T𝑒U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼. In addition, since ⟨𝐻, 𝜌⟩ ⊢ 𝑒.𝑓 ⇓ 𝑣, by
EvalField ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ ℓ for some ℓ. Then by induction ⟨𝐻, 𝛼, 𝜌⟩ ′ 𝜎 ′ , and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡𝑒 ).
                                                                                   𝑉
Then by EvalField, ⟨𝐻, 𝜌⟩ ⊢ 𝑒.𝑓 ⇓ 𝐻 (𝑉 ′ (𝑡𝑒 ), 𝑓 ).
Gradually Verifying Unfolding Expressions & Pure Functions                                                         59


    By SEvalField, 𝑔(𝜎 ′ ) =⇒ 𝑡𝑒 ==𝑡𝑒′ , therefore 𝑉 ′ (𝑡𝑒 ) = 𝑉 ′ (𝑡𝑒′ ). Also by SEvalField ⟨𝑓 , 𝑡𝑒′ , 𝑡⟩ ∈ H(𝜎 ′ ).
Therefore 𝑉 ′ (𝑡) = 𝐻 (𝑉 ′ (𝑡𝑒′ ), 𝑓 ) = 𝐻 (𝑉 ′ (𝑡𝑒 ), 𝑓 ) since ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ .
    Case 10. SEvalFieldOptimistic – 𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′, _: Similar to case 9.
    Case 11. SEvalFieldImprecise – 𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′′, _:
    By SEvalFieldImprecise, 𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′, _, 𝑡 = fresh, and 𝜎 ′′ = 𝜎 ′ [H = H (𝜎 ′ ); ⟨𝑓 , 𝑡𝑒 , 𝑡⟩]. Let
𝑉 = 𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′, _ | 𝐻 ] [𝑡 ↦→ 𝐻 (𝑉 (𝑡𝑒 ), 𝑓 )]. Then 𝑉 ′ is the corresponding valuation for this
  ′

case.
    Since T𝑒.𝑓 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼, by definition 5 T𝑒U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼. In addition, since ⟨𝐻, 𝜌⟩ ⊢ 𝑒.𝑓 ⇓ 𝑣, by
EvalField ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ ℓ for some ℓ. Then, by induction ⟨𝐻, 𝛼, 𝜌⟩ ′ 𝜎 ′ and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡𝑒 )
                                                                                 𝑉
(so ℓ = 𝑉 ′ (𝑡𝑒 )). In addition, 𝑉 ′ (𝑡) = 𝐻 (𝑉 ′ (𝑡𝑒 ), 𝑓 ) by definition of 𝑉 ′ . Then by EvalField ⟨𝐻, 𝜌⟩ ⊢
𝑒.𝑓 ⇓ 𝐻 (ℓ, 𝑓 ), and 𝑉 ′ (𝑡) = 𝐻 (ℓ, 𝑓 ).
    Since T𝑒.𝑓 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼, by definition 5 ⟨ℓ, 𝑓 ⟩ = ⟨𝑉 ′ (𝑡𝑒 ), 𝑓 ⟩ ⊆ 𝛼. Then since ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ ,
⟨𝐻, 𝛼⟩ 𝑉 ′ H (𝜎 ′ ). Therefore, ⟨𝐻, 𝛼⟩ 𝑉 ′ H (𝜎 ′ ); ⟨𝑓 , 𝑡𝑒 , 𝑡⟩.
  Then ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′′ since 𝜎 ′ and 𝜎 ′′ differ only in their H components and H (𝜎 ′′ ) =
H (𝜎 ′ ); ⟨𝑓 , 𝑡𝑒 , 𝑡⟩.
  Case 12. SEvalFieldFailure – 𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′, _:
  By SEvalFieldFailure, 𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′, _ and 𝑡 = fresh. Let 𝑉 ′ = 𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′, _]. Then the
corresponding valuation for this case is 𝑉 ′′ = 𝑉 ′ [𝑡 ↦→ 𝐻 (𝑉 (𝑡𝑒 ), 𝑓 )].
  Since T𝑒.𝑓 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼, by definition 5 T𝑒U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼. In addition, since ⟨𝐻, 𝜌⟩ ⊢ 𝑒.𝑓 ⇓ 𝑣, by
EvalField ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ ℓ for some ℓ. Then, by induction ⟨𝐻, 𝛼, 𝜌⟩ ′ 𝜎 ′ and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡𝑒 )
                                                                            𝑉
(meaning ℓ = 𝑉 ′ (𝑡𝑒 )). Since 𝑉 ′′ extends 𝑉 ′ , ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′′ 𝜎 ′ and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′′ (𝑡𝑒 ).
   Then by EvalField, ⟨𝐻, 𝜌⟩ ⊢ 𝑒.𝑓 ⇓ 𝐻 (𝑉 ′′ (𝑡𝑒 ), 𝑓 ). Since 𝑉 ′′ extends 𝑉 ′ which extends 𝑉 , 𝑉 ′′ (𝑡) =
𝑉 (𝑡) = 𝐻 (𝑉 (𝑡𝑒 ), 𝑓 ).
   Case 13. SEvalUnfoldingPrecise – 𝜎1 ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎6, _:
   Inductively, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎2 . Since consuming 𝑝 (𝑒) only removes from the precise and optimistic
heaps, H(𝜎3 ) ⊆ H(𝜎2 ) and H (𝜎3 ) ⊆ H (𝜎2 ). Therefore, using the definition of state correspondence,
⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎3 . Then, since ⟨𝐻, 𝛼, [𝑥 ↦→ 𝑉 (𝑡)]⟩ ⊨ predicate(𝑝) in the run-time semantics due
to the previous state correspondence which uses equirecursive semantics, all obtained predicate
chunks and field chunks must hold after unfolding the predicate once, meaning ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎4 .
Then, by induction, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎5 . Since ⟨𝐻, 𝜌⟩ ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓ 𝑣, by EvalUnfolding
⟨𝐻, 𝜌⟩ ⊢ 𝑒 0 ⇓ 𝑣. Inductively, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎5 and ⟨𝐻, 𝜌⟩ ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓ 𝑉 ′ (𝑡 0 ).
    Case 14. SEvalUnfoldingImpreciseA and SEvalUnfoldingImpreciseB – 𝜎1 ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓
𝑡 0 ⊣ 𝜎6, _:
    Both of these cases are similar to the one for SEvalUnfoldingPrecise, since all that changes is
the information retained in the optimistic heap at the end of evaluation.
    Case 15. SEvalUnfoldingImplicitPrecise – 𝜎1 ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎2, _:
    By the induction hypothesis, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎2 and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 0 ⇓ 𝑣 0 where 𝑣 0 = 𝑉 ′ (𝑡 0 ). Therefore,
by EvalUnfolding, ⟨𝐻, 𝜌⟩ ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓ 𝑣 0 .
    Case 16. SEvalUnfoldingImplicitImprecise – 𝜎1 ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎3, _:
    Similar to the case for SEvalUnfoldingImplicitPrecise.
    Case 17. SEvalUnfoldingImplicitFailure – 𝜎1 ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓ 𝑡 0 ⊣ 𝜎2, _:
    Similar to the case for SEvalUnfoldingImplicitPrecise.
    Case 18. SEvalFunctionExplicit – 𝜎1 ⊢ 𝑓 (𝑒) ⇓ 𝑡 ′ ⊣ 𝜎6, _:
60                                                                                                    Torek et al.



  Inductively, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎2 . Since consuming func_pre(𝑓 ) only removes from the precise and
optimistic heaps, H(𝜎3 ) ⊆ H(𝜎2 ) and H (𝜎3 ) ⊆ H (𝜎2 ). Therefore, using the definition of state
correspondence, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎3 . Since producing directly after consuming results in precise and
optimistic heaps that are subsets of their counterparts from 𝜎1 , again ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎4 . Inductively,
⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎5 . Since H (𝜎6 ) = H (𝜎5 ) and H(𝜎6 ) = H(𝜎2 ), ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎6 as desired.
  Case 19. SEvalFunctionImplicit – 𝜎1 ⊢ 𝑓 (𝑒) ⇓ 𝑡 ′ ⊣ 𝜎5, _:
  Inductively, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎2 . Then, since 𝜎4 = 𝜎2 [𝜄 = 𝜄 (𝜎3 ), H = H ′, 𝑔 = 𝑔(𝜎2 ) && . . .], it suffices
to show ⟨𝐻, 𝛼⟩ 𝑉 ′ H ′ . If func_pre(𝑓 ) is precise, then 𝑠 ′ \ H(𝜎2 ) = ∅ because all heap chunks
used in the body are optimistically proven, meaning that they already exist in the initial heap and
⟨𝐻, 𝛼⟩ 𝑉 ′ ∅ trivially. Otherwise, since T𝑓 (𝑒)U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼 by Definition 5, ⟨𝛼, 𝜌, 𝜎 ′ ⟩ 𝑉 ′ 𝐻 where
H (𝜎 ′ ) ⊇ H ′ . Therefore, ⟨𝐻, 𝛼⟩ 𝑉 ′ H ′ .
   Since ⟨𝐻, 𝜌⟩ ⊢ 𝑓 (𝑒) ⇓ 𝑣 ′ where ⟨𝐻, 𝜌 ′ ⟩ ⊢ func_body(𝑓 ) ⇓ 𝑣 ′ , then by induction 𝑣 ′ = 𝑉 (𝑡 ′ ) =
𝑉 (𝑓 (𝑡, 𝑠)).
                                                                                                       □

D.3   Produce
Definition 37. For a judgement 𝜎 ⊢ 𝜙˜ ◁ 𝜎 ′ , given an initial valuation 𝑉 and heap 𝐻 , the corre-
sponding valuation is denoted
                                       𝑉 [𝜎 ⊢ 𝜙˜ ◁ 𝜎 ′ | 𝐻, 𝜌].
This valuation is defined as follows, depending on the rule that proves the derivation. Values are
referenced using the respective name from the rule definition.
   Note that the corresponding valuation always extends the initial valuation and is defined for all
fresh symbolic values in the judgement.
 • SProduceImprecise:
                        𝑉 [𝜎 ⊢ ? ∗ 𝜙 ◁ 𝜎 ′ | 𝐻, 𝜌] := 𝑉 [𝜎 [𝜄 = ⊤] ⊢ 𝜙 ◁ 𝜎 ′ | 𝐻, 𝜌]
 • SProduceExpr:
                           𝑉 [𝜎 ⊢ 𝑒 ◁ 𝜎 ′′ | 𝐻, 𝜌] := 𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _ | 𝐻, 𝜌]
 • SProducePredicate:
                         𝑉 [𝜎 ⊢ 𝑝 (𝑒) ◁ 𝜎 ′′ | 𝐻, 𝜌] := 𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _ | 𝐻, 𝜌]
 • SProduceField:
                        𝑉 [𝜎 ⊢ acc(𝑒.𝑓 ) ◁ 𝜎 ′′ | 𝐻, 𝜌] := 𝑉 ′ [𝑡 ↦→ 𝐻 (𝑉 ′ (𝑡𝑒 ), 𝑓 )]
   where 𝑉 ′ = 𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′, _ | 𝐻, 𝜌].
 • SProduceConjunction:
              𝑉 [𝜎 ⊢ 𝜙 1 ∗ 𝜙 2 ◁ 𝜎 ′′ | 𝐻, 𝜌] := 𝑉 [𝜎 ⊢ 𝜙 1 ◁ 𝜎 ′ | 𝐻, 𝜌] [𝜎 ′ ⊢ 𝜙 2 ◁ 𝜎 ′′ | 𝐻, 𝜌]
 • SProduceIfA:
                  𝑉 [𝜎 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ◁ 𝜎 ′′ | 𝐻, 𝜌] :=
                     𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎, _ | 𝐻, 𝜌] [𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡] ⊢ 𝜙 1 ◁ 𝜎 ′′ | 𝐻, 𝜌]
 • SProduceIfB:
                 𝑉 [𝜎 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ◁ 𝜎 ′′ | 𝐻, 𝜌] :=
                    𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _ | 𝐻, 𝜌] [𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && ! 𝑡] ⊢ 𝜙 2 ◁ 𝜎 ′′ | 𝐻, 𝜌]
Gradually Verifying Unfolding Expressions & Pure Functions                                               61


Lemma 29. If 𝜎 ⊢ 𝜙 ◁ 𝜎 ′ , then 𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎).
  Proof. By induction on 𝜎 ⊢ 𝜙 ◁ 𝜎 ′ :
  Case 1. SProduceImprecise – 𝜎 ⊢ ? ∗ 𝜙 ◁ 𝜎 ′ :
  By SProduceImprecise 𝜎 [𝜄 = ⊤] ⊢ 𝜙 ◁ 𝜎 ′ , thus by induction 𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎).
  Case 2. SProduceExpr – 𝜎 ⊢ 𝑒 ◁ 𝜎 ′′ :
  By SProduceExpr 𝜎 ′′ = 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) &&𝑡], where 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _. Trivially 𝑔(𝜎 ′ ) &&𝑡 =⇒ 𝑔(𝜎 ′ )
and by lemma 24 𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎).
  Case 3. SProducePredicate – 𝜎 ⊢ 𝑝 (𝑒) ◁ 𝜎 ′′ :
  By SProducePredicate 𝜎 ′′ = 𝜎 ′ [H = · · · ] where 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _ , so 𝑔(𝜎 ′′ ) = 𝑔(𝜎 ′ ). Then by
lemma 24 𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎).
  Case 4. SProduceField – 𝜎 ⊢ acc(𝑒.𝑓 ) ◁ 𝜎 ′ : Similar to case 3.
  Case 5. SProduceConjunction – 𝜎 ⊢ 𝜙 1 ∗ 𝜙 2 ◁ 𝜎 ′′ :
  By SProduceConjunction 𝜎 ⊢ 𝜙 1 ◁ 𝜎 ′ and 𝜎 ′ ⊢ 𝜙 2 ◁ 𝜎 ′′ . By induction 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎 ′ ) and
𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎), therefore 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎).
  Case 6. SProduceIfA – 𝜎 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ◁ 𝜎 ′′ :
  By SProduceIfA 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡] ⊢ 𝜙 1 ◁ 𝜎 ′′ where 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _ thus by induction
𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎 ′ ) && 𝑡 =⇒ 𝑔(𝜎 ′ ). Then by lemma 24 𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎).
  Case 7. SProduceIfB – 𝜎 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ◁ 𝜎 ′′ : Similar to case 6.
                                                                                                       □
Lemma 30. If 𝜎 ⊢ 𝜙˜ ◁ 𝜎 ′ then 𝛾 (𝜎 ′ ) = 𝛾 (𝜎).
  Proof. Trivial by induction on 𝜎 ⊢ 𝜙˜ ◁ 𝜎 ′ and by using lemma 25.                                     □

Lemma 31. Suppose ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 where ⟨𝐻, 𝛼 \ T𝜙U     ˜ ⟨𝐻, 𝜌 ⟩ ⟩   H(𝜎).
                                                                  𝑉
  If 𝜎 ⊢ 𝜙 ◁ 𝜎 , ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙, and 𝑉 (𝑔(𝜎 )) = true where 𝑉 = 𝑉 [𝜎 ⊢ 𝜙˜ ◁ 𝜎 ′ | 𝐻, 𝜌], then
          ˜   ′              ˜       ′    ′                     ′


                                                ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′

  Proof. By induction on 𝜎 ⊢ 𝜙˜ ◁ 𝜎 ′ :
  Case 1. SProduceImprecise – 𝜎 ⊢ ? ∗ 𝜙 ◁ 𝜎 ′ :
  By SProduceImprecise 𝜎 [𝜄 = ⊤] ⊢ 𝜙 ◁ 𝜎 ′ . Let 𝑉 ′ be the corresponding valuation, thus 𝑉 ′ is the
corresponding valuation for this case.
  Then, since ⟨𝐻, 𝛼, 𝜌⟩ ⊨ ? ∗ 𝜙, by AssertImprecise ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙. Also, T? ∗ 𝜙U ⟨𝐻, 𝜌 ⟩ = T𝜙U ⟨𝐻, 𝜌 ⟩ .
Therefore ⟨𝐻, 𝛼 \ T𝜙U ⟨𝐻, 𝜌 ⟩ ⟩ 𝑉 H(𝜎), and furthermore ⟨𝐻, 𝛼 \ T𝜙U ⟨𝐻, 𝜌 ⟩ ⟩ 𝑉 H(𝜎 [𝜄 = ⊤]).
  Therefore ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ by induction.
  Case 2. SProduceExpr – 𝜎 ⊢ 𝑒 ◁ 𝜎 ′′ :
  By SProduceExpr 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _. Let 𝑉 ′ be the corresponding valuation, therefore 𝑉 ′ is the
corresponding valuation for this case.
  Since ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜌, by AssertValue ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ true. Since ⟨𝐻, 𝛼 \ T𝑒U ⟨𝐻, 𝜌 ⟩ ⟩ 𝑉 H(𝜎) and
⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 clearly T𝑒U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼. Then by lemma 28, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ .
  Let 𝜎 ′′ = 𝜎 ′ [𝑔(𝜎 ′ ) && 𝑡]. Then, since 𝜎 ′ and 𝜎 differ only in their 𝑔 components ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′′
since 𝑉 ′ (𝑔(𝜎 ′ )) = true as ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ .
   Case 3. SProducePredicate – 𝜎 ⊢ 𝑝 (𝑒) ◁ 𝜎 ′ :
   By SProducePredicate, for each 𝑒, 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _ for some 𝑡𝑖 . Let 𝑉 ′ be the corresponding
valuation for this case, thus 𝑉 ′ extends the corresponding valuation corresponding for each 𝜎 ⊢
𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _.
62                                                                                                  Torek et al.


  By assumptions, ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝑝 (𝑒). Then by AssertPredicate, for each 𝑒, ⟨𝐻, 𝛼⟩ ⊢ 𝑒 ⇓ 𝑣. Since
⟨𝐻, 𝛼 \ T𝑝 (𝑒)U ⟨𝐻, 𝜌 ⟩ ⟩ 𝑉 H(𝜎) and ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 clearly T𝑝 (𝑒U ⟨𝐻, 𝛼 ⟩ ⊆ 𝛼. Then T𝑒U ⟨𝐻, 𝛼 ⟩ ⊆ 𝛼 by
definition 5. Then by lemma 28, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡) for all 𝑒. In addition, since
H(𝜎 ′ ) = H(𝜎) by lemma 25, ⟨𝐻, 𝛼 \ T𝑝 (𝑒)U ⟨𝐻, 𝜌 ⟩ ⟩ 𝑉 ′ H(𝜎 ′ ).
  By SProducePredicate 𝜎 ′′ = 𝜎 ′ [H = H(𝜎 ′ ); ⟨𝑝, 𝑡⟩]. Since 𝜎 ′ and 𝜎 ′′ differ only in their H
components, proving that (1) holds for H(𝜎 ′′ ) is sufficient to prove that ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′′ . Then
                       T𝑝 (𝑒)U ⟨𝐻, 𝜌 ⟩ ⊇ Tpredicate(𝑝)U ⟨𝐻, 𝑥↦→𝑉 ′ (𝑡 ) ⟩ = 𝑉 ′ L⟨𝑝, 𝑡⟩M𝐻 ,

where 𝑥 = predicate_params(𝑝) thus ⟨𝐻, 𝛼 \ 𝑉 L⟨𝑝, 𝑡⟩M𝐻 ⟩ 𝑉 ′ H(𝜎 ′ ) by lemma 19. Now by lemma
15 and since 𝑉 ′ extends 𝑉 ,
                                 ∀ ℎ ∈ H(𝜎 ′ ) : 𝑉 ′ LℎM𝐻 ∩ 𝑉 ′ L⟨𝑝, 𝑡⟩M𝐻 = ∅.
Since ⟨𝑝, 𝑡⟩ is the only addition to H(𝜎 ′′ ) relative to H(𝜎 ′ ) and 𝑉 ′ extends 𝑉 ,
                       ∀ ℎ 1, ℎ 2 ∈ H(𝜎 ′′ ) : ℎ 1 ≠ ℎ 2 =⇒ 𝑉 ′ Lℎ 1 M𝐻 ∩ 𝑉 ′ Lℎ 2 M𝐻 = ∅.
Also by AssertPredicate ⟨𝐻, 𝛼, [𝑥 ↦→ 𝑉 ′ (𝑡)]⟩ ⊨ predicate(𝑝). Therefore, since ⟨𝑝, 𝑡⟩ is the only
addition to H(𝜎 ′′ ) relative to H(𝜎 ′ ) and 𝑉 ′ extends 𝑉 ,
                        ∀ ⟨𝑝, 𝑡⟩ ∈ H(𝜎 ′′ ) : ⟨𝐻, 𝛼, [𝑥 ↦→ 𝑉 ′ (𝑡)]⟩ ⊨ predicate(𝑝).
Therefore all requirements for (1) are satisfied, and therefore ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′′ .
   Case 4. SProduceField – 𝜎 ⊢ acc(𝑒.𝑓 ) ◁ 𝜎 ′′ :
   By SProduceField 𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′, _ for some 𝑡𝑒 . Let 𝑉𝑒 be the corresponding valuation, and let
𝑉 ′ be the corresponding valuation for this case, thus 𝑉 ′ extends 𝑉𝑒 .
   Also by SProduceField 𝜎 ′′ = 𝜎 ′ [H = H(𝜎 ′ ); ⟨𝑓 , 𝑡𝑒 , 𝑡⟩] where 𝑡 = fresh. By definition 𝑉 ′ (𝑡) =
𝐻 (𝑉𝑒 (𝑡𝑒 ), 𝑓 ).
   By assumptions ⟨𝐻, 𝛼, 𝜌⟩ ⊨ acc(𝑒.𝑓 ), thus by AssertAcc ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣𝑒 for some 𝑣𝑒 such that
⟨𝑣𝑒 , 𝑓 ⟩ ∈ 𝛼. Then since ⟨𝐻, 𝛼 \ Tacc(𝑒.𝑓 )U ⟨𝐻, 𝛼 ⟩ ⟩ 𝑉 H𝜎 and ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎, Tacc(𝑒.𝑓 )U ⟨𝐻, 𝛼 ⟩ ⊆ 𝛼.
Then T𝑒U ⟨𝐻, 𝛼 ⟩ ⊆ 𝛼 by definition 5. Then by lemma 28, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 ′ and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉𝑒 (𝑡𝑒 ).
                                                                               𝑒
In addition, ⟨𝑉 ′ (𝑡𝑒 ), 𝑓 ⟩ ∈ 𝛼 as 𝑉 ′ extends 𝑉𝑒 . Also by lemma 25, H(𝜎 ′ ) = H(𝜎), so ⟨𝐻, 𝛼 \
Tacc(𝑒.𝑓 )U ⟨𝐻, 𝛼 ⟩ ⟩ 𝑉 H(𝜎 ′ ).
                       𝑒
   Since 𝜎 ′ and 𝜎 ′′ differ only in their H components, proving that (1) holds for H(𝜎 ′′ ) is sufficient
to prove that ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′′ .
   As shown before, 𝑉 ′ (𝑡) = 𝐻 (𝑉 ′ (𝑡𝑒 ), 𝑓 ). Therefore, since ⟨𝑓 , 𝑡𝑒 , 𝑡⟩ is the only addition to H(𝜎 ′′ )
relative to H(𝜎 ′ ) and 𝑉 ′ extends 𝑉𝑒 ,
                             ∀ ⟨𝑓 , 𝑡, 𝑡 ′ ⟩ ∈ H(𝜎 ′′ ) : 𝐻 (𝑉 ′ (𝑡), 𝑓 ) = 𝑉 ′ (𝑡 ′ ) and
                                   ∀ ⟨𝑓 , 𝑡, 𝑡 ′ ⟩ ∈ H(𝜎 ′′ ) : ⟨𝑉 ′ (𝑡), 𝑓 ⟩ ∈ 𝛼
Since ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡𝑒 ) as shown before,
                           Tacc(𝑒.𝑓 )U ⟨𝐻, 𝜌 ⟩ ⊇ {⟨𝑉 ′ (𝑡𝑒 ), 𝑓 ⟩} = 𝑉 L(𝑡𝑒 .𝑓 ; 𝑡)M𝐻 .
Therefore ⟨𝐻, 𝛼 \ 𝑉 ′ L(𝑡 .𝑓 ; 𝑡 ′ )M𝐻 ⟩ 𝑉 H(𝜎 ′ ) by lemma 19. Now by lemma 15, and since 𝑉 ′ extends
                                          𝑒
𝑉𝑒 ,
                                 ∀ ℎ ∈ H(𝜎 ′′ ) : 𝑉 ′ LℎM𝐻 ∩ 𝑉 ′ L⟨𝑓 , 𝑡𝑒 , 𝑡⟩M𝐻 = ∅.
Finally, since ⟨𝑓 , 𝑡𝑒 , 𝑡⟩ is the only addition to H(𝜎 ′′ ) relative to H(𝜎 ′ ) and 𝑉 ′ extends 𝑉𝑒 ,
                      ∀ ℎ 1, ℎ 2 ∈ H(𝜎 ′′ ) 2 : ℎ 1 ≠ ℎ 2 =⇒ 𝑉 ′ Lℎ 1 M𝐻 ∩ 𝑉 ′ Lℎ 2 M𝐻 = ∅.
Gradually Verifying Unfolding Expressions & Pure Functions                                                    63


Therefore all requirements for (1) are satisfied and therefore ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′′ .
   Case 5. SProduceConjunction – 𝜎 ⊢ 𝜙 1 ∗ 𝜙 2 ◁ 𝜎 ′′ :
   By SProduceConjunction 𝜎 ⊢ 𝜙 1 ◁ 𝜎 ′ and 𝜎 ′ ⊢ 𝜙 2 ◁ 𝜎 ′′ . Let 𝑉1 and 𝑉2 be the respective corre-
sponding valuations, extending 𝑉 and 𝑉1 , respectively. Then 𝑉2 is the corresponding valuation for
this case.
   Since ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙 1 ∗ 𝜙 2 , by AssertConjunction ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙 1 and ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙 2 where
T𝜙 1 U ⟨𝐻, 𝜌 ⟩ ∩ T𝜙 2 U ⟨𝐻, 𝜌 ⟩ = ∅. Also, T𝜙 1 ∗ 𝜙 2 U ⟨𝐻, 𝜌 ⟩ = T𝜙 1 U ⟨𝐻, 𝜌 ⟩ ∪ T𝜙 2 U ⟨𝐻, 𝜌 ⟩ .
   Let 𝛼 ′ = 𝛼 \ T𝜙 2 U ⟨𝐻, 𝜌 ⟩ . Then ⟨𝐻, 𝛼 ′, 𝜌⟩ ⊨ 𝜙 1 by lemma 12 since T𝜙 1 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼 ′ . Also, ⟨𝐻, 𝛼 ′ \
T𝜙 1 U ⟨𝐻, 𝜌 ⟩ ⟩ 𝑉 H(𝜎) since 𝛼 ′ \ T𝜙 1 U ⟨𝐻, 𝜌 ⟩ = 𝛼 \ T𝜙 1 ∗ 𝜙 2 U ⟨𝐻, 𝜌 ⟩ . Finally, by lemma 29, 𝑔(𝜎 ′′ ) =⇒
𝑔(𝜎 ′ ), and therefore 𝑉2 (𝑔(𝜎 ′ )) = 𝑉1 (𝑔(𝜎 ′ )) = true.
   Now ⟨𝐻, 𝛼 ′, 𝜌⟩ 𝑉 𝜎 ′ by induction. Therefore, ⟨𝐻, 𝛼 ′ ⟩ 𝑉 H(𝜎 ′ ). Also, ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙 2 by lemma
                       1                                           1
12 since T𝜙 2 U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼. Finally, 𝑉2 (𝑔(𝜎 ′′ )) = true by assumption, therefore ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 ′′ by
                                                                                                      2
induction.
   Case 6. SProduceIfA – 𝜎 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ◁ 𝜎 ′′ :
   By SProduceIfA 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _ and 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) &&𝑡] ⊢ 𝜙 1 ◁ 𝜎 ′′ . Let 𝑉1 and 𝑉 ′ be the respective
corresponding valuations extending 𝑉 and 𝑉1 , respectively. Then 𝑉 ′ is the corresponding valuation
in this case.
   By lemma 29, 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎 ′ ) && 𝑡. By assumptions 𝑉 ′ (𝑔(𝜎 ′′ )) = true, thus 𝑉 ′ (𝑔(𝜎 ′ ) && 𝑡) =
𝑉1 (𝑔(𝜎 ′ ) && 𝑡) = true. In addition, 𝑉1 (𝑔(𝜎 ′ )) = true by lemma 27. Therefore, 𝑉1 (𝑡) = true.
   Since ⟨𝐻, 𝛼, 𝜌⟩ ⊨ if 𝑒 then 𝜙 1 else 𝜙 2 , ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣 for some 𝑣 by AssertIfA or AssertIfB. As
⟨𝐻, 𝛼\Tif 𝑒 then 𝜙 1 else 𝜙 2 U ⟨𝐻, 𝛼 ⟩ ⟩ 𝑉 H(𝜎) and ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎, then Tif 𝑒 then 𝜙 1 else 𝜙 2 U ⟨𝐻, 𝛼 ⟩ ⊆
𝛼. Thus, T𝑒U ⟨𝐻, 𝛼 ⟩ ⊆ 𝛼 by definition 5. Then by lemma 28, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 ′ and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉1 (𝑡).
                                                                       1
Therefore 𝑣 = 𝑉1 (𝑡) = true.
   Then, by lemma 25 H(𝜎 ′ ) = H(𝜎), so
                             ⟨𝐻, 𝛼 \ Tif 𝑒 then 𝜙 1 else 𝜙 2 U ⟨𝐻, 𝛼 ⟩ ⟩ 𝑉 H(𝜎 ′ ).
                                                                          1

Then T𝜙 1 U ⟨𝐻, 𝜌 ⟩ ⊆ Tif 𝑒 then 𝜙 1 else 𝜙 2 U ⟨𝐻, 𝜌 ⟩ by definition 5. Therefore, since 𝑉1 (𝑔(𝜎 ′ ) && 𝑡) =
true,
                             ⟨𝐻, 𝛼 \ T𝜙 1 U ⟨𝐻, 𝜌 ⟩ ⟩ 𝑉 H(𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡]).
                                                       1

Also, ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙 1 by AssertIfA since ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ true and ⟨𝐻, 𝛼, 𝜌⟩ ⊨ if 𝑒 then 𝜙 1 else 𝜙 2 .
Finally, 𝑉 ′ (𝑔(𝜎 ′′ )) = true by assumption.
  Thus ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′′ by induction.
  Case 7. SProduceIfB – 𝜎 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ◁ 𝜎 ′′ : Similar to case 6.
                                                                                               □
Lemma 32 (Progress). If 𝑉 (𝑔(𝜎)) = true, ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙,      ˜ and ⟨𝐻, 𝛼, 𝜌⟩
                                                                             𝑉
                                                                               𝜎, then 𝜎 ⊢ 𝜙˜ ◁ 𝜎 ′ for
some 𝜎 ′ where 𝑉 ′ (𝑔(𝜎 ′ )) = true and 𝑉 ′ = 𝑉 [𝜎 ⊢ 𝜙˜ ◁ 𝜎 ′ | 𝐻, 𝜌].
  Proof. Let 𝛼 ′ = 𝛼 ∪T𝜙U   ˜ ⟨𝐻, 𝜌 ⟩ . Then by lemma 19 ⟨𝐻, 𝛼 ′, 𝜌⟩
                                                                     𝑉
                                                                       𝜎 and by lemma 12 ⟨𝐻, 𝛼 ′, 𝜌⟩ ⊨ 𝜙.
                                                                                                       ˜
Then suppose 𝑉 (𝑔(𝜎)) = true and complete the proof by induction on the syntax forms of 𝜙:         ˜
  Case 1. ? ∗ 𝜙 – 𝜙 ∈ Formula:
  Let 𝜎ˆ = 𝜎 [𝜄 = ⊤]. Then 𝑉 (𝑔(𝜎))       ˆ = 𝑉 (𝑔(𝜎)) = true. Also, since ⟨𝐻, 𝛼, 𝜌⟩ ⊨ ? ∗ 𝜙, by
AssertImprecise ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙. Thus by induction 𝜎ˆ ⊢ 𝜙 ◁ 𝜎 ′ for some 𝜎 ′ where 𝑉 ′ (𝑔(𝜎 ′ )) = true.
Then 𝜎 ⊢ ? ∗ 𝜙 ◁ 𝜎 ′ by SProduceImprecise, and 𝑉 ′ (𝑔(𝜎 ′ )) = true.
  Case 2. 𝜙 1 ∗ 𝜙 2 – 𝜙 1, 𝜙 2 ∈ Formula:
  Since ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙 1 ∗ 𝜙 2 , ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙 1 and ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙 2 by AssertConjunction and lemma 9.
64                                                                                                  Torek et al.


    By induction 𝜎 ⊢ 𝜙 1 ◁ 𝜎 ′ , with corresponding valuation 𝑉 ′ where 𝑉 ′ (𝑔(𝜎 ′ )) = true. Then by
induction 𝜎 ′ ⊢ 𝜙 2 ◁ 𝜎 ′′ , with corresponding valuation 𝑉 ′′ , for some 𝜎 ′′ where 𝑉 ′′ (𝑔(𝜎 ′′ )) = true.
By SProduceConjunction, 𝜎 ⊢ 𝜙 1 ∗ 𝜙 2 ◁ 𝜎 ′′ , and 𝑉 ′′ (𝑔(𝜎 ′′ )) = true.
    Case 3. 𝑝 (𝑒) – 𝑝 ∈ Predicate, 𝑒 ∈ Expr:
    By lemma 27, 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _ for some 𝑡 ∈ SExpr and 𝜎 ′ where 𝑉 ′ (𝑔(𝜎 ′ )) = true, and 𝑉 ′ is the
corresponding valuation extending 𝑉 . Let 𝜎 ′′ = 𝜎 ′ [H = H(𝜎 ′ ); ⟨𝑝, 𝑡⟩], then by SProducePredicate,
𝜎 ⊢ 𝑝 (𝑒) ◁ 𝜎 ′′ . Since 𝜎 ′′ and 𝜎 ′ differ only in their H components, 𝑉 ′ (𝑔(𝜎 ′′ )) = 𝑉 ′ (𝑔(𝜎 ′ )) = true.
    Case 4. 𝑒 ∈ Expr:
    By lemma 27, 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _ for some 𝑡 ∈ SExpr. Let 𝑉 ′ be the corresponding valuation and
𝜎 = 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡].
  ′′

    Since ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝑒, ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ true by AssertValue. Then, since ⟨𝐻, 𝛼 ′, 𝜌⟩ 𝑉 𝜎, and
T𝑒U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼 ′ , by lemma 28 ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡). Then 𝑉 ′ (𝑡) = true and 𝑉 ′ (𝑔(𝜎 ′ )) = true. Finally,
𝑉 ′ (𝜎 ′′ ) = 𝑉 ′ (𝜎 ′ ) ∧ 𝑉 ′ (𝑡) = 𝑉 (𝜎 ′ ) ∧ true = true.
    Case 5. if 𝑒 then 𝜙 1 else 𝜙 2 – 𝑒 ∈ Expr, 𝜙 1, 𝜙 2 ∈ Formula:
    By lemma 27, 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _ for some 𝑡 ∈ SExpr and 𝜎 ′ . Let 𝑉1 be the valuation corresponding
to this derivation. In addition, 𝑉1 (𝑔(𝜎 ′ )) = true.
    Then one of the following rules must apply to derive ⟨𝐻, 𝛼, 𝜌⟩ ⊨ if 𝑒 then 𝜙 1 else 𝜙 2 :
    Case 5(a). AssertIfA:
    Then ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ true. Since ⟨𝐻, 𝛼 ′, 𝜌⟩ 𝑉 𝜎 and T𝑒U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼 ′ , by lemma 28 ⟨𝐻, 𝛼 ′, 𝜌⟩ 𝑉 𝜎 ′
                                                                                                           1
and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉1 (𝑡). Therefore, 𝑉1 (𝑡) = true and 𝑉1 (𝑔(𝜎 ′ )) = true.
    Therefore 𝑉1 (𝑔(𝜎 ′ ) && 𝑡) = true. Also, ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙 1 by AssertIfA, and so by lemma 9
⟨𝐻, 𝛼 ′, 𝜌⟩ ⊨ 𝜙 1 .
    Then, since ⟨𝐻, 𝛼 ′, 𝜌⟩ 𝑉 𝜎 ′ , by induction 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡] ⊢ 𝜙 1 ◁ 𝜎 ′′ for some 𝜎 ′′ with
                                     1
corresponding valuation 𝑉 ′ extending 𝑉1 , where 𝑉 ′ (𝑔(𝜎 ′′ )) = true.
    Now by SProduceIfA, 𝜎 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ◁ 𝜎 ′′ . By definition 𝑉 ′ is the corresponding
valuation extending 𝑉 , and as shown before, 𝑉 ′ (𝑔(𝜎 ′′ )) = true.
    Case 5(b). AssertIfB:
    Then ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ false. Since ⟨𝐻, 𝛼 ′, 𝜌⟩ 𝑉 𝜎 and T𝑒U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼 ′ , by lemma 28 ⟨𝐻, 𝛼 ′, 𝜌⟩ 𝑉 𝜎 ′
                                                                                                           1
and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉1 (𝑡). Therefore 𝑉1 (𝑡) = false and 𝑉1 (𝑔(𝜎 ′ )) = true.
    Therefore 𝑉1 (𝑔(𝜎) && ! 𝑡) = true. Also, ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙 2 by AssertIfB, and so by lemma 9
⟨𝐻, 𝛼 ′, 𝜌⟩ ⊨ 𝜙 1 .
    Then, since ⟨𝐻, 𝛼 ′, 𝜌⟩ 𝑉 𝜎 ′ , by induction 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && ! 𝑡] ⊢ 𝜙 1 ◁ 𝜎 ′′ for some 𝜎 ′′ with
                                     1
corresponding valuation 𝑉 ′ extending 𝑉1 , where 𝑉 ′ (𝑔(𝜎 ′′ )) = true.
    Now by SProduceIfB, 𝜎 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ◁ 𝜎 ′ . By definition 𝑉 ′ is the corresponding
valuation extending 𝑉 , and as shown before, 𝑉 ′ (𝑔(𝜎 ′ )) = true.
    Case 6. acc(𝑒.𝑓 ) where 𝑒 ∈ Expr, 𝑓 ∈ Field
    By lemma 27, 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _ for some 𝑡 and 𝑉 ′ (𝑔(𝜎 ′ )) = true, where 𝑉1 is the corresponding
valuation extending 𝑉 .
    Let 𝜎 ′′ = 𝜎 ′ [H = H(𝜎 ′ ); ⟨𝑓 , 𝑡, fresh⟩]. Then, by SProduceField, 𝜎 ⊢ acc(𝑒.𝑓 ) ◁ 𝜎 ′′ with
corresponding valuation 𝑉 ′ extending 𝑉1 . Since 𝜎 ′′ and 𝜎 ′ differ only in their H component,
𝑉 ′ (𝑔(𝜎 ′′ )) = 𝑉 ′ (𝑔(𝜎 ′ )) = true.
                                                                                                             □
Gradually Verifying Unfolding Expressions & Pure Functions                                        65


D.4    Consume
Definition 38. For a judgement 𝜎, 𝜎𝐸 ⊢ 𝜙˜ ▷ 𝜎 ′, R, Θ, given an initial valuation 𝑉 , heap 𝐻 , and
environment 𝜌, the corresponding valuation is denoted
                              𝑉 [𝜎, 𝜎𝐸 ⊢ 𝜙˜ ▷ 𝜎 ′, R, Θ | 𝐻, 𝜌].
This valuation is defined as follows, depending on the rule that proves the derivation. Values are
referenced using the respective name from the rule definition.
   Note that the corresponding valuation always extends the initial valuation and is defined for all
fresh symbolic values in the judgement.
 • SConsumeImprecision:
                       𝑉 [𝜎, 𝜎𝐸 ⊢ ? ∗ 𝜙 ▷ ⟨⊤, 𝑔(𝜎 ′ ), 𝛾 (𝜎 ′ ), ∅, ∅⟩, R, Θ | 𝐻, 𝜌] :=
                          𝑉 [𝜎, 𝜎𝐸 ⊢ 𝜙 ▷ 𝜎 ′, R, Θ | 𝐻, 𝜌]
 • SConsumeValue:
                      𝑉 [𝜎, 𝜎𝐸 ⊢ 𝑒 ▷ 𝜎, R, ∅ | 𝐻, 𝜌] := 𝑉 [𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡 ⊣ _, R | 𝐻, 𝜌]
 • SConsumeValueImprecise:
            𝑉 [𝜎, 𝜎𝐸 ⊢ 𝑒 ▷ 𝜎 [𝑔 = 𝑔(𝜎) && 𝑡], R; 𝑡, ∅ | 𝐻, 𝜌] := 𝑉 [𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡 ⊣ _, R | 𝐻, 𝜌]
 • SConsumeValueFailure:
                     𝑉 [𝜎, 𝜎𝐸 ⊢ 𝑒 ▷ 𝜎, {⊥}, ∅ | 𝐻, 𝜌] := 𝑉 [𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡 ⊣ _, R | 𝐻, 𝜌]
 • SConsumePredicate:
           𝑉 [𝜎, 𝜎𝐸 ⊢ 𝑝 (𝑒) ▷ 𝜎 [H = H′, H = ∅], _, _ | 𝐻, 𝜌] := 𝑉 [𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡 ⊣ _, R | 𝐻, 𝜌]
 • SConsumePredicateImprecise:
            𝑉 [𝜎, 𝜎𝐸 ⊢ 𝑝 (𝑒) ▷ 𝜎 [𝐻 = ∅, H = ∅], _, _ | 𝐻, 𝜌] := 𝑉 [𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡 ⊣ _, R | 𝐻, 𝜌]
 • SConsumePredicateFailure:
                   𝑉 [𝜎, 𝜎𝐸 ⊢ 𝑝 (𝑒) ▷ 𝜎, {⊥}, _ | 𝐻, 𝜌] := 𝑉 [𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡 ⊣ _, R | 𝐻, 𝜌]
 • SConsumeAcc, SConsumeAccOptimistic, SConsumeAccImprecise,
   SConsumeAccFailure:
                       𝑉 [𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ▷ 𝜎 [H = H′, H = H ′ ], _, _ | 𝐻, 𝜌] :=
                          𝑉 [𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ _, R | 𝐻, 𝜌]
 • SConsumeConjunction:
                            𝑉 [𝜎, 𝜎𝐸 ⊢ 𝜙 1 ∗ 𝜙 2 ▷ 𝜎 ′′, _, _ | 𝐻, 𝜌] :=
                               𝑉 [𝜎, 𝜎𝐸 ⊢ 𝜙 1 ▷ 𝜎 ′, R 1, Θ1 | 𝐻, 𝜌]
                                  [𝜎 ′, 𝜎𝐸 [𝑔 = 𝑔(𝜎 ′ )] ⊢ 𝜙 2 ▷ 𝜎 ′′, R 2, Θ2 | 𝐻, 𝜌]
 • SConsumeConditionalA:
                       𝑉 [𝜎, 𝜎𝐸 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ▷ 𝜎 ′, R ∪ R ′, _ | 𝐻, 𝜌] :=
                          𝑉 [𝜎 [𝑔 = 𝑔′ ], 𝜎𝐸 [𝑔 = 𝑔′ ] ⊢ 𝜙 1 ▷ 𝜎 ′, R ′, Θ | 𝐻, 𝜌]
 • SConsumeConditionalB:
                       𝑉 [𝜎, 𝜎𝐸 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ▷ 𝜎 ′, R ∪ R ′, _ | 𝐻, 𝜌] :=
                          𝑉 [𝜎 [𝑔 = 𝑔′ ], 𝜎𝐸 [𝑔 = 𝑔′ ] ⊢ 𝜙 2 ▷ 𝜎 ′, R ′, Θ | 𝐻, 𝜌]
66                                                                                                  Torek et al.


Definition 39. For a judgement 𝜎 ⊢ 𝜙˜ ▷𝜎 ′, R, given an initial valuation 𝑉 , heap 𝐻 , and environment
𝜌, the corresponding valuation is denoted
                                    𝑉 [𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, R | 𝐻, 𝜌].
     The is defined by
                         𝑉 [𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, R | 𝐻, 𝜌] := 𝑉 [𝜎, 𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, R, _ | 𝐻, 𝜌]
where 𝜎, 𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, R, _ is the judgement used when applying SConsume to derive 𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, R.
Lemma 33 (Consume results in more specific path condition (long form)). If 𝜎, 𝜎𝐸 ⊢ 𝜙˜ ▷ 𝜎 ′, _, _,
then 𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎).
Lemma 34 (Consume results in more specific path condition (short form)). If 𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, _, then
𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎).
Lemma 35 (Soundness of remf for precise heaps and imprecise states). If ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 and 𝜄 (𝜎)
then ⟨𝐻, 𝛼 \ {(𝑉 (𝑡), 𝑓 )}⟩ 𝑉 remf (H(𝜎), 𝜎, 𝑡, 𝑓 ) for any 𝑡, 𝑓 .

Lemma 36. If 𝜎, 𝜎𝐸 ⊢ 𝜙˜ ▷ 𝜎 ′, R, Θ then 𝛾 (𝜎 ′ ) = 𝛾 (𝜎).
Lemma 37. If 𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, R then 𝛾 (𝜎 ′ ) = 𝛾 (𝜎).
Lemma 38 (Soundness of remfp for precise heaps). If ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 and ⟨𝑓 , 𝑡, _⟩ ∈ H(𝜎), then
⟨𝐻, 𝛼 \ {⟨𝑉 (𝑡), 𝑓 ⟩}⟩ 𝑉 remfp (H(𝜎), 𝜎, 𝑡, 𝑓 ) for any 𝑡, 𝑓 .

Lemma 39 (Soundness of remf for optimistic heaps). If 𝜎 is well-formed and ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 then
⟨𝐻, 𝛼 \ {⟨𝑉 (𝑡), 𝑓 ⟩}⟩ 𝑉 remf (H (𝜎), 𝜎, 𝑡, 𝑓 ) for any 𝑡, 𝑓 .

     Proof. If ¬𝜄 (𝜎), then H (𝜎) = ∅ because 𝜎 is well-formed, so trivially ⟨∅, H (𝜎)⟩ 𝑉 𝐻 . Then,
by definition, remf (H (𝜎), 𝜎, 𝑡, 𝑓 ) ⊆ H (𝜎) = ∅, so ⟨∅, remf (H (𝜎), 𝜎, 𝑡, 𝑓 )⟩         𝑉
                                                                                              𝐻 . Then, since
∅ ⊆ 𝛼 \ {⟨𝑉 (𝑡), 𝑓 ⟩}, ⟨𝛼 \ {⟨𝑉 (𝑡), 𝑓 ⟩}, remf (H (𝜎), 𝜎, 𝑡, 𝑓 )⟩ 𝑉 𝐻 by Lemma 18.
   If 𝜄 (𝜎) then H (𝜎) may be non-empty. Let H ′ = remf (H (𝜎), 𝜎, 𝑡, 𝑓 ) and let 𝛼 ′ = 𝛼 \ {⟨𝑉 (𝑡), 𝑓 ⟩}.
Then, by definition of remf , H ′ ⊆ H (𝜎), so ⟨𝛼, H ′ ⟩ 𝑉 𝐻 . Then, by the definition of optimistic
heap correspondence, 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ ) for all ⟨𝑓 , 𝑡, 𝑡 ′ ⟩ ∈ H ′ . Using this and the fact that H ′
contains no predicate chunks to the definition of remf , it suffices to show that ⟨𝑉 (𝑠), 𝑔⟩ ∈ 𝛼 ′ for
⟨𝑔, 𝑠, 𝑠 ′ ⟩ ∈ H ′ . By definition of remf ,

               ¬ alias(𝜎, 𝑡, 𝑓 , 𝑠, 𝑔) =⇒ (𝑓 ≠ 𝑔) ∨ ¬ sat(𝑔(𝜎) && [𝑡 == 𝑠])
                                      =⇒ (𝑓 ≠ 𝑔) ∨ (𝑉 (𝑔(𝜎) && 𝑡 == 𝑡 ′ ) = false)
                                      =⇒ (𝑓 ≠ 𝑔) ∨ (𝑉 (𝑔(𝜎)) = false) ∨ (𝑉 (𝑡) ≠ 𝑉 (𝑠))
                                      =⇒ (𝑓 ≠ 𝑔) ∨ (𝑉 (𝑡) ≠ 𝑉 (𝑠))
                                      =⇒ ⟨𝑉 (𝑡), 𝑓 ⟩ ≠ ⟨𝑉 (𝑠), 𝑔⟩.
  Furthermore, ⟨𝑉 (𝑠), 𝑔⟩ ∈ 𝛼 because ⟨𝛼, H ′ ⟩ 𝑉 𝐻 , so ⟨𝑉 (𝑠), 𝑔⟩ ∈ 𝛼 ′ and ⟨𝛼 ′, H ′ ⟩ 𝑉 𝐻 as
desired.                                                                                      □
Lemma 40 (Soundness of Θ calculation). If 𝜙 is a precise formula, ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ 𝑉 𝜎𝐸 , 𝜎, 𝜎𝐸 ⊢ 𝜙 ▷ 𝜎 ′,
R, Θ with corresponding valuation 𝑉 ′ , 𝑉 ′ (𝑔(𝜎 ′ )) = true, and ⟨𝐻, 𝛼 ′, 𝜌⟩ ⊨ 𝜙 where 𝛼 ′ ⊆ 𝛼 𝐸 , then
⟨𝐻, 𝑉 ′ LΘM𝐻 , 𝜌⟩ ⊨ 𝜙 and 𝑉 LΘM𝐻 ⊆ 𝛼 ′ .
Gradually Verifying Unfolding Expressions & Pure Functions                                                     67


   Proof. By induction on 𝜎, 𝜎𝐸 ⊢ 𝜙 ▷ 𝜎 ′, R, Θ:
   Case 1. SConsumeImprecision – 𝜎, 𝜎𝐸 ⊢ ? ∗ 𝜙 ▷ ⟨⊤, 𝑔(𝜎 ′ ), 𝛾 (𝜎 ′ ), ∅, ∅⟩, R, Θ: ? ∗ 𝜙 is not precise,
therefore this rule cannot apply.
   Case 2. SConsumeValue, SConsumeValueImprecise, SConsumeValueFailure – 𝜎, 𝜎𝐸 ⊢ 𝑒 ▷ 𝜎, _, ∅:
   Since ⟨𝐻, 𝛼 ′, 𝜌⟩ ⊨ 𝑒, ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ true by AssertValue. Therefore ⟨𝐻, 𝑉 L∅M𝐻 , 𝜌⟩ ⊨ 𝑒 by
AssertValue.
   Also, 𝑉 L∅M𝐻 = ∅ ⊆ 𝛼 ′ .
   Case 3. SConsumePredicate, SConsumePredicateImprecise, SConsumePredicateFailure – 𝜎, 𝜎𝐸 ⊢
𝑝 (𝑒) ▷ _, _, {⟨𝑝, 𝑡⟩}:
   By the respective rule, 𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡 ⊣ _, _ for some 𝑡. The corresponding valuation for this case
extends the corresponding valuation for all of these derivation.
   Since ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝑝 (𝑒), ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣 for some 𝑣 by AssertPredicate. By assumptions
⟨𝐻, 𝛼 𝐸 , 𝜌⟩ 𝑉 𝜎𝐸 . Let 𝛼ˆ𝐸 = 𝛼 𝐸 ∪ T𝑝 (𝑒)U ⟨𝐻, 𝜌 ⟩ . Then by lemma 19 ⟨𝐻, 𝛼ˆ𝐸 , 𝜌⟩ 𝑉 𝜎𝐸 . Thus by lemma
28 𝑣 = 𝑉 ′ (𝑡), i.e., ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡).
    Let 𝑥 = predicate_params(𝑝). By AssertPredicate ⟨𝐻, 𝛼 ′, [𝑥 ↦→ 𝑉 ′ (𝑡)]⟩ ⊨ predicate(𝑝). Also,
𝑉 L⟨𝑝, 𝑡⟩M𝐻 = Tpredicate(𝑝)U ⟨𝐻, [𝑥↦→𝑉 ′ (𝑡 ) ] ⟩ . Therefore ⟨𝐻, 𝑉 L⟨𝑝, 𝑡⟩∩𝛼 ′ M𝐻 , [𝑥 ↦→ 𝑉 ′ (𝑡)]⟩ ⊨ predicate(𝑝)
by lemma 11.
    But predicate(𝑝) must be a specification, thus 𝑉 L⟨𝑝, 𝑡⟩M𝐻 = Tpredicate(𝑝)U ⟨𝐻, [𝑥↦→𝑉 ′ (𝑡 ) ] ⟩ ⊆
𝑉 L⟨𝑝, 𝑡⟩M𝐻 ∩ 𝛼 ′ by lemma 4. Therefore 𝑉 L{⟨𝑝, 𝑡⟩}M𝐻 ⊆ 𝛼 ′ .
    Then ⟨𝐻, 𝑉 L{⟨𝑝, 𝑡⟩}M𝐻 , [𝑥 ↦→ 𝑉 ′ (𝑡)]⟩ ⊨ predicate(𝑝), and thus ⟨𝐻, 𝑉 L{⟨𝑝, 𝑡⟩}M𝐻 , 𝜌⟩ ⊨ 𝑝 (𝑒) by
AssertPredicate.
    Case 4. SConsumeAcc, SConsumeAccOptimistic, SConsumeAccImprecise, SConsumeAccFailure –
𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ▷ 𝜎 ′, _, {⟨𝑡𝑒 , 𝑓 ⟩}:
    By the respective rule, 𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ _, _ for some 𝑡𝑒 . The corresponding valuation for this case
extends the corresponding valuation for this derivation.
    Since ⟨𝐻, 𝛼, 𝜌⟩ ⊨ acc(𝑒.𝑓 ), ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣 for some 𝑣 by AssertAcc. Let
𝛼ˆ𝐸 = 𝛼 𝐸 ∪ Tacc(𝑒.𝑓 )U ⟨𝐻, 𝜌 ⟩ . Then by lemma 19 ⟨𝐻, 𝛼ˆ𝐸 , 𝜌⟩ 𝑉 𝜎𝐸 . Thus by lemma 28 𝑣 = 𝑉 ′ (𝑡𝑒 ), i.e.
⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡𝑒 ).
    By AssertAcc ⟨𝑉 ′ (𝑡𝑒 ), 𝑓 ⟩ ∈ 𝛼 ′ . Also, {⟨𝑉 ′ (𝑡𝑒 ), 𝑓 ⟩} = 𝑉 ′ L{⟨𝑡𝑒 , 𝑓 ⟩}M𝐻 , therefore 𝑉 ′ L{⟨𝑡𝑒 , 𝑓 ⟩}M𝐻 ⊆
𝛼 and also ⟨𝐻, 𝑉 ′ L{⟨𝑡𝑒 , 𝑓 ⟩}M𝐻 , 𝜌⟩ ⊨ acc(𝑒.𝑓 ) by AssertAcc.
  ′

    Case 5. SConsumeConjunction, SConsumeConjunctionImprecise – 𝜎, 𝜎𝐸 ⊢ 𝜙 1 ∗𝜙 2 ▷𝜎 ′′, _, Θ1 ∪Θ2 :
    By the respective rule, 𝜎, 𝜎𝐸 ⊢ 𝜙 1 ▷ 𝜎 ′, _, Θ1 and 𝜎 ′, 𝜎𝐸 [𝑔 = 𝑔(𝜎 ′ )] ⊢ 𝜙 2 ▷ 𝜎 ′′, _, Θ2 . Let 𝑉 ′ be
the corresponding valuation for this case, thus 𝑉 ′ extends the corresponding valuations for these
judgements.
    By assumptions, 𝑉 ′ (𝑔(𝜎 ′′ )) = true and 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎 ′ ) by 33. Therefore ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ 𝑉 ′
𝜎𝐸 [𝑔 = 𝑔(𝜎 ′ )].
    Then ⟨𝐻, 𝛼 1, 𝜌⟩ ⊨ 𝜙 1 and ⟨𝐻, 𝛼 2, 𝜌⟩ ⊨ 𝜙 2 where 𝛼 1 ∪𝛼 2 ⊆ 𝛼 ′ and 𝛼 1 ∩𝛼 2 = ∅ by AssertConjunction,
since ⟨𝐻, 𝛼 ′, 𝜌⟩ ⊨ 𝜙 1 ∗ 𝜙 2 . Then by induction ⟨𝐻, 𝑉 ′ LΘ1 M𝐻 , 𝜌⟩ ⊨ 𝜙 1 , ⟨𝐻, 𝑉 ′ LΘ2 M𝐻 , 𝜌⟩ ⊨ 𝜙 2 ,
𝑉 ′ LΘ1 M𝐻 ⊆ 𝛼 1 , and 𝑉 ′ LΘ2 M𝐻 ⊆ 𝛼 1 .
    Now 𝑉 ′ LΘ1 M𝐻 ∩ 𝑉 ′ LΘ2 M𝐻 = ∅ and 𝑉 ′ LΘ1 M𝐻 ∪ 𝑉 ′ LΘ2 M𝐻 = 𝑉 ′ LΘ1 ∪ Θ2 M𝐻 ⊆ 𝛼 ′ . Therefore
⟨𝐻, 𝑉 ′ LΘ1 ∪ Θ2 M𝐻 , 𝜌⟩ ⊨ 𝜙 1 ∗ 𝜙 2 by AssertConjunction.
    Case 6. SConsumeConditionalA – 𝜎, 𝜎𝐸 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ▷ 𝜎 ′, R ∪ R ′, Θ:
    By SConsumeConditionalA 𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡 ⊣ _, _ for some 𝑡. Let 𝑉1 be the corresponding valuation.
    Also, 𝜎 [𝑔 = 𝑔′ ], 𝜎𝐸 [𝑔 = 𝑔′ ] ⊢ 𝜙 1 ▷ 𝜎 ′, _, Θ where 𝑔′ = 𝑔(𝜎) && 𝑡. Let 𝑉 ′ be the corresponding
valuation for this case, which extends the corresponding valuation for this judgement and 𝑉1 .
68                                                                                                Torek et al.


    Since ⟨𝐻, 𝛼 ′, 𝜌⟩ ⊨ if 𝑒 then 𝜙 1 else 𝜙 2 , by AssertIfA ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣 for some 𝑣. Let 𝛼ˆ𝐸 =
𝛼 𝐸 ∪ T𝑒U ⟨𝐻, 𝜌 ⟩ . Then by lemma 19 ⟨𝐻, 𝛼ˆ𝐸 , 𝜌⟩ 𝑉 𝜎𝐸 . Thus, by lemma 28 𝑣 = 𝑉1 (𝑡). Also, since
𝑉 ′ (𝑔(𝜎 ′ )) = true and 𝑔(𝜎 ′ ) =⇒ 𝑔′ = 𝑔(𝜎) && 𝑡 by lemma 33, 𝑉1 (𝑡) = true. Therefore ⟨𝐻, 𝜌⟩ ⊢
𝑒 ⇓ true.
    In addition, 𝜎𝐸 [𝑔 = 𝑔′ ] and 𝜎𝐸 differ only in their 𝑔 component, so ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ 𝑉 𝜎𝐸 [𝑔 = 𝑔′ ].
                                                                                        1
Also by AssertIfA ⟨𝐻, 𝛼 ′, 𝜌⟩ ⊨ 𝜙 1 . Therefore by induction ⟨𝐻, 𝑉 LΘM𝐻 , 𝜌⟩ ⊨ 𝜙 1 and 𝑉 LΘM𝐻 ⊆ 𝛼 ′ .
    Finally, ⟨𝐻, 𝑉 LΘM𝐻 , 𝜌⟩ ⊨ if 𝑒 then 𝜙 1 else 𝜙 2 by AssertIfA.
    Case 7. SConsumeConditionalB – 𝜎, 𝜎𝐸 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ▷ 𝜎 ′, R ∪ R ′, Θ: Similar to case
6.
                                                                                                     □
Lemma 41 (Soundness of consume for precise formulas). Let 𝜙 be some precise formula, 𝑉 be
some initial valuation, 𝐻 be some heap, 𝜌 be some environment, 𝛼 𝐸 and 𝛼 be sets of permissions
such that 𝛼 ⊆ 𝛼 𝐸 , and 𝜎 and 𝜎𝐸 be well-formed symbolic states such that ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 and
⟨𝐻, 𝛼 𝐸 , 𝜌⟩ 𝑉 𝜎𝐸 .
  Then, if 𝜎, 𝜎𝐸 ⊢ 𝜙 ▷ 𝜎 ′, R, Θ with corresponding valuation 𝑉 ′ , ⟨𝐻, 𝛼 𝐸 ⟩ ⊢𝑉 ′ R, and 𝑉 ′ (𝑔(𝜎 ′ )) =
true, then
                ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊨ 𝜙,     ⟨𝐻, 𝛼 \ 𝑉 LΘM𝐻 , 𝜌⟩ 𝑉 ′ 𝜎 ′,   and ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊢frmI 𝜙 .          (16)
     Furthermore, if the above conditions hold and R ∩ SPerm = ∅, then
                                                ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙 .                                          (17)
    Proof. Suppose that 𝜎, 𝜎𝐸       ⊢ 𝜙 ▷ 𝜎 ′, R, Θ with corresponding valuation 𝑉 ′ , ⟨𝐻, 𝛼
                                                                                           𝐸 ⟩ ⊢𝑉 ′ R, and
𝑉 ′ (𝑔(𝜎 ′ )) = true. Complete the proof by induction on 𝜎, 𝜎𝐸 ⊢ 𝜙 ▷ R, Θ, :
    Case 1. SConsumeImprecision – 𝜎, 𝜎𝐸 ⊢ ? ∗ 𝜙 ▷ ⟨⊤, 𝑔(𝜎 ′ ), 𝛾 (𝜎 ′ ), ∅, ∅⟩, R, Θ: Since ? ∗ 𝜙 is
imprecise, this rule cannot apply.
    Case 2. SConsumeValue – 𝜎, 𝜎𝐸 ⊢ 𝑒 ▷ 𝜎, R, ∅:
    By SConsumeValue 𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎𝐸′ , R for some 𝜎𝐸′ . Let 𝑉 ′ be the corresponding valuation, with
initial valuation 𝑉 . Then 𝑉 ′ is the corresponding valuation for this case.
    By lemma 27, 𝑉 (𝑔(𝜎𝐸′ )) = true. Then, since ⟨𝐻, 𝛼 𝐸 ⟩ ⊢𝑉 ′ R, by lemma 26 ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡).
Also by SConsumeValue 𝑔(𝜎) =⇒ 𝑡. Therefore 𝑉 ′ (𝑡) = true, and therefore ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ true.
Thus ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊨ 𝑒 by AssertValue.
   𝑉 L∅M𝐻 = ∅, therefore ⟨𝐻, 𝛼 \ 𝑉 L∅M𝐻 , 𝜌⟩ 𝑉 ′ 𝜎 since 𝑉 ′ extends 𝑉 .
    Finally, ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊢frm 𝑒 by lemma 26. Therefore ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊢frmI 𝑒 by IFrameExpression, which
completes the proof of (16).
    As shown before, ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ true, thus ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝑒 by AssertValue, which proves (17).
    Case 3. SConsumeValueImprecise – 𝜎, 𝜎𝐸 ⊢ 𝑒 ▷ 𝜎 [𝑔 = 𝑔(𝜎) && 𝑡], R; 𝑡, ∅:
    By SConsumeValueImprecise 𝜎𝐸 ⊢ 𝑒 ⇓ 𝜎𝐸′ ⊣ 𝑡, R for some 𝜎𝐸′ . Let 𝑉 ′ be the valuation correspond-
ing to this derivation, with initial valuation 𝑉 . Then 𝑉 ′ is the valuation corresponding to this
case.
    Let 𝜎 ′ = 𝜎 [𝑔 = 𝑔(𝜎) && 𝑡].
    By assumptions, ⟨𝐻, 𝛼 𝐸 ⟩ ⊢𝑉 ′ {𝑡 } by lemma 23. Thus 𝑉 ′ (𝑡) = true by CheckValue. Also
𝑉 (𝑔(𝜎𝐸′ )) = true by lemma 27. Then, ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡) by lemma 26; therefore ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ true.
  ′

Thus, by AssertValue, ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊨ 𝑒.
   𝑉 L∅M𝐻 = ∅, therefore ⟨𝐻, 𝛼 \ 𝑉 L∅M𝐻 , 𝜌⟩ 𝑉 ′ 𝜎 since 𝑉 ′ extends 𝑉 .
    Furthermore, since 𝑉 ′ (𝑡) = true, 𝑉 ′ (𝑔(𝜎 ′ )) = 𝑉 (𝑔(𝜎)) && 𝑉 ′ (𝑡) = true. Since 𝜎 ′ and 𝜎 differ
only in their 𝑔 components, ⟨𝐻, 𝛼 \ 𝑉 L∅M𝐻 , 𝜌⟩ 𝑉 ′ 𝜎 ′ .
Gradually Verifying Unfolding Expressions & Pure Functions                                                          69


  Finally, ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊢frm 𝑒 by lemma 26. Therefore ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊢frmI 𝑒 by IFrameExpression.
  Case 4. SConsumeValueFailure – 𝜎, 𝜎𝐸 ⊢ 𝑒 ▷ 𝜎, {⊥}, ∅:
   ⟨𝐻, 𝛼 𝐸 ⟩ ⊢𝑉 ′ R ∪ {⊥} is a contradiction, thus the lemma vacuously holds.
  Case 5. SConsumePredicate – 𝜎, 𝜎𝐸 ⊢ 𝑝 (𝑒) ▷ 𝜎 ′, R, {⟨𝑝, 𝑡⟩}:
                                                       Ð
  By SConsumePredicate, for each 𝑒, 𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎𝐸′ , R for some 𝜎𝐸′ , 𝑡, and R. Let 𝑉 ′ be corre-
sponding valuation for this case, thus 𝑉 ′ extends the respective individual corresponding valuations
and for each R, ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R by lemma 23. In addition, by lemma 27 𝑉 ′ (𝑔(𝜎𝐸′ )) = true.
  Therefore, for each 𝑒 and corresponding 𝑡, ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡) by lemma 26. By SConsumePredicate,
for each 𝑡, 𝑔(𝜎) =⇒ 𝑡 == 𝑡 ′ for some 𝑡 ′ , thus 𝑉 ′ (𝑡) = 𝑉 ′ (𝑡 ′ ) since 𝑉 ′ (𝑔(𝜎)) = true. Therefore
⟨𝐻, 𝜌⟩ ⊢ 𝑒𝑖 ⇓ 𝑉 ′ (𝑡𝑖′ ).
  By SConsumePredicate ⟨𝑝, 𝑡 ′ ⟩ ∈ H(𝜎). Since ⟨𝐻, 𝛼⟩ 𝑉 𝜎, ⟨𝐻, 𝛼, [𝑥 ↦→ 𝑉 ′ (𝑡 ′ )]⟩ ⊨ predicate(𝑝)
where 𝑥 = predicate_params(𝑝). Thus by AssertPredicate ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝑝 (𝑒), which proves (17).
Also, ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊨ 𝑝 (𝑒) by lemma 9.
  Let 𝛼 ′ = 𝑉 L⟨𝑝, 𝑡⟩M𝐻 , therefore 𝛼 ′ = Tpredicate(𝑝)U ⟨𝐻, [𝑥↦→𝑉 ′ (𝑡 ) ] ⟩ = Tpredicate(𝑝)U ⟨𝐻, [𝑥↦→𝑉 ′ (𝑡 ′ ) ] ⟩ .
   By SConsumePredicate 𝜎 ′ = 𝜎 [H = H′, H = ∅] where H = H′ ; ⟨𝑝, 𝑡⟩. Thus ⟨𝐻, 𝛼⟩ 𝑉 ′ H(𝜎 ′ )
since H(𝜎 ′ ) ⊂ H(𝜎).
   Then 𝑉 ′ LℎM𝐻 ∩ 𝛼 ′ = ∅ for all ℎ ∈ H(𝜎 ′ ) since ⟨𝐻, 𝛼⟩ 𝑉 ′ H(𝜎), ⟨𝑝, 𝑡⟩ ∈ H(𝜎), and ⟨𝑝, 𝑡⟩ ∉ H(𝜎 ′ ).
Therefore, by lemma 16, ⟨𝐻, 𝛼 \ 𝛼 ′ ⟩ 𝑉 ′ H(𝜎 ′ ).
  Also, since H (𝜎 ′ ) = ∅, ⟨𝐻, 𝛼 \ 𝛼 ′ ⟩ 𝑉 ′ H (𝜎 ′ ).
   Therefore ⟨𝐻, 𝛼 \ 𝛼 ′, 𝜌⟩ 𝑉 ′ 𝜎 ′ since 𝜎 ′ and 𝜎 differ only in their H and H components.
    By lemmas 23 ⟨𝐻, 𝛼 𝐸 ⟩ ⊢𝑉 ′ R for each R, thus ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊢frm 𝑒 for each 𝑒 by lemma 26, thus
⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊢frmI 𝑝 (𝑒) by IFramePredicate. Thus (16) holds.
    Case 6. SConsumePredicateImprecise – 𝜎, 𝜎𝐸 ⊢ 𝑝 (𝑒) ▷ 𝜎 ′, R; ⟨𝑝, 𝑡⟩, {⟨𝑝, 𝑡⟩}:
                                                                  Ð
    By SConsumePredicateImprecise, for each 𝑒, 𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎𝐸′ , R for some 𝜎𝐸′ , 𝑡, and R. Let 𝑉 ′ be
corresponding valuation for this case, thus 𝑉 ′ extends the respective individual corresponding
valuations and for each R, ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R by lemma 23. In addition, 𝑉 ′ (𝑔(𝜎𝐸′ )) = true by lemma 27.
   Therefore, for each 𝑒 and corresponding 𝑡, ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡) by lemma 26. By
SConsumePredicateImprecise, for each 𝑡, 𝑔(𝜎) =⇒ 𝑡 == 𝑡 ′ for some 𝑡 ′ , thus 𝑉 ′ (𝑡) = 𝑉 ′ (𝑡 ′ ) since
𝑉 ′ (𝑔(𝜎)) = true. Therefore ⟨𝐻, 𝜌⟩ ⊢ 𝑒𝑖 ⇓ 𝑉 ′ (𝑡𝑖′ ).
   Also, ⟨𝐻, 𝛼 𝐸 ⟩ ⊢𝑉 ′ {⟨𝑝, 𝑡⟩} by assumptions and lemma 23. Thus ⟨𝐻, 𝛼 𝐸 , [𝑥 ↦→ 𝑉 ′ (𝑡)]⟩ ⊨ predicate(𝑝)
by CheckPred. Therefore ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊨ 𝑝 (𝑒) by AssertPredicate.
    By SConsumePredicateImprecise 𝜎 ′ = 𝜎 [H = ∅, H = ∅], thus ⟨𝐻, 𝛼 \ 𝑉 ′ L{⟨𝑝, 𝑡⟩}M𝐻 ⟩ 𝑉 ′ H(𝜎 ′ )
and ⟨𝐻, 𝛼 \ 𝑉 ′ L{⟨𝑝, 𝑡⟩}M𝐻 ⟩ 𝑉 ′ H (𝜎 ′ ). Therefore ⟨𝐻, 𝛼 \ 𝑉 L{⟨𝑝, 𝑡⟩}M𝐻 , 𝜌⟩ 𝑉 ′ 𝜎 ′ since 𝜎 ′ and 𝜎
differ only in their H and H components.
   For each 𝑒, ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊢frm 𝑒 by lemma 26. Therefore ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊢frmI 𝑝 (𝑒) by IFramePredicate,
which completes the proof of (16).
   Also, ⟨𝑝, 𝑡⟩ ∈ SPerm is in the resulting set of checks, which contradicts the premises of (17).
Therefore it is vacuously true.
   Case 7. SConsumePredicateFailure – 𝜎, 𝜎𝐸 ⊢ 𝑝 (𝑒) ▷ 𝜎, {⊥}, {⟨𝑝, 𝑡⟩}:
   ⟨𝐻, 𝛼 𝐸 ⟩ ⊢𝑉 ′ {⊥} is a contradiction, thus the lemma vacuously holds.
   Case 8. SConsumeAcc – 𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ▷ 𝜎 [H = H′, H = H ′ ], R, {⟨𝑡𝑒 , 𝑓 ⟩}:
   By SConsumeAcc 𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎𝐸′ , R. Let 𝑉 ′ be the corresponding valuation, thus 𝑉 ′ is the
corresponding valuation for this case.
   By lemma 27, 𝑉 ′ (𝑔(𝜎𝐸′ )) = true. Thus ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡𝑒 ) by lemma 26. Also 𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒
by SConsumeAcc, thus 𝑉 ′ (𝑡𝑒′ ) = 𝑉 ′ (𝑡𝑒 ) since 𝑉 ′ (𝑔(𝜎)) = true. Therefore, ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡𝑒′ ).
70                                                                                                         Torek et al.


  Since ⟨𝑓 , 𝑡𝑒′ , 𝑡⟩ ∈ H(𝜎) by SConsumeAcc and ⟨𝐻, 𝛼⟩ 𝑉 H(𝜎), ⟨𝑉 ′ (𝑡𝑒′ ), 𝑓 ⟩ ∈ 𝛼. Thus ⟨𝐻, 𝛼, 𝜌⟩ ⊨
acc(𝑒.𝑓 ) by AssertAcc, which proves (17). Therefore ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊨ acc(𝑒.𝑓 ) by lemma 9 since
𝛼 ⊆ 𝛼𝐸 .
  Let H′ = remfp (H(𝜎), 𝜎, 𝑡𝑒 , 𝑓 ). Therefore ⟨𝐻, 𝛼 \ {⟨𝑉 ′ (𝑡𝑒 ), 𝑓 ⟩}⟩ 𝑉 ′ H′ by lemma 38. Also,
{⟨𝑉 ′ (𝑡𝑒′ ), 𝑓 ⟩} = {⟨𝑉 ′ (𝑡𝑒 ), 𝑓 ⟩} = 𝑉 ′ L{⟨𝑡𝑒 , 𝑓 ⟩}M𝐻 . Thus ⟨𝐻, 𝛼 \ 𝑉 ′ L{⟨𝑡𝑒 , 𝑓 ⟩}M𝐻 ⟩ 𝑉 ′ H′ .
   Likewise, let H ′ = remf (H (𝜎), 𝜎, 𝑡𝑒 , 𝑓 ). Then similarly ⟨𝐻, 𝛼 \ 𝑉 L{⟨𝑡𝑒 , 𝑓 ⟩}M𝐻 ⟩ 𝑉 ′ H ′ by lemma
39.
   By SConsumeAcc, 𝜎 ′ = 𝜎 [H = H′, H = H ′ ]. Now, since 𝜎 and 𝜎 ′ differ only in their H and H
components, using the properties of H′ and H ′ shown above, ⟨𝐻, 𝛼 \ 𝑉 L{⟨𝑡𝑒 , 𝑓 ⟩}M𝐻 , 𝜌⟩ 𝑉 ′ 𝜎 ′ .
   Finally, ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊢frm 𝑒 by lemma 26. Therefore ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊢frmI acc(𝑒.𝑓 ) by IFrameAcc, which
completes the proof of (16).
   Case 9. SConsumeAccOptimistic – 𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ▷ 𝜎 ′, R, {⟨𝑡𝑒 , 𝑓 ⟩}: Similar to case 8, except
to show that ⟨𝐻, 𝛼 \ {⟨𝑉 ′ (𝑡𝑒′ ), 𝑓 ⟩}⟩ 𝑉 H′ .
   Since ⟨𝑓 , 𝑡𝑒′ , 𝑡⟩ ∈ H (𝜎), H (𝜎) ≠ ∅. Therefore, since 𝜎 is well-formed, 𝜄 (𝜎) = ⊤. Let H′ =
remf (H(𝜎), 𝜎, 𝑡𝑒′ , 𝑓 ). Therefore ⟨𝐻, 𝛼 \ {⟨𝑉 ′ (𝑡𝑒′ ), 𝑓 ⟩}⟩ 𝑉 H′ by lemma 35.
   Continue as in case 8.
   Case 10. SConsumeAccImprecise – 𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ▷ 𝜎 ′, R; ⟨𝑡𝑒 , 𝑓 ⟩, {⟨𝑡𝑒 , 𝑓 ⟩}:
   By SConsumeAcc 𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎𝐸′ , R. Let 𝑉 ′ be the corresponding valuation, thus 𝑉 ′ is the
corresponding valuation for this case.
   Then ⟨𝐻, 𝛼 𝐸 ⟩ ⊢𝑉 ′ R by assumptions and lemma 23. In addition, 𝑉 ′ (𝑔(𝜎𝐸′ )) = true by lemma 27.
Thus ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡𝑒 ) by lemma 26.
   Also, ⟨𝐻, 𝛼 𝐸 ⟩ ⊢𝑉 ′ ⟨𝑡𝑒 , 𝑓 ⟩ by assumptions and lemma 23. Then ⟨𝑉 ′ (𝑡𝑒 ), 𝑓 ⟩ ∈ 𝛼 𝐸 by CheckAcc.
Therefore ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊨ acc(𝑒.𝑓 ) by AssertAcc.
   Let H′ = remf (H(𝜎), 𝜎, 𝑡𝑒 , 𝑓 ). By SConsumeAccImprecise 𝜄 (𝜎). Thus ⟨𝐻, 𝛼 \ {⟨𝑉 ′ (𝑡𝑒 ), 𝑓 ⟩}⟩ 𝑉 ′ H′
by lemma 35. Also, {⟨𝑉 ′ (𝑡𝑒 ), 𝑓 ⟩} = 𝑉 ′ L{⟨𝑡𝑒 , 𝑓 ⟩}M𝐻 . Thus ⟨𝐻, 𝛼 \ 𝑉 ′ L{⟨𝑡𝑒 , 𝑓 ⟩}M𝐻 ⟩ 𝑉 ′ H′ .
   Likewise, let H ′ = remf (H (𝜎), 𝜎, 𝑡𝑒 , 𝑓 ). Then ⟨𝐻, 𝛼 \ 𝑉 L⟨𝑡𝑒 , 𝑓 ⟩M𝐻 ⟩ 𝑉 ′ H ′ by lemma 39.
   By SConsumeAcc, 𝜎 ′ = 𝜎 [H = H′, H = H ′ ]. Now, since 𝜎 and 𝜎 ′ differ only in their H and H
components, using the properties of H′ and H ′ shown above, ⟨𝐻, 𝛼 \ 𝑉 L{⟨𝑡𝑒 , 𝑓 ⟩}M𝐻 , 𝜌⟩ 𝑉 ′ 𝜎 ′ .
   By lemma 26 ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊢frm 𝑒, therefore ⟨𝐻, 𝛼 𝐸 , acc(𝑒.𝑓 )⟩ ⊢frmI by IFrameAcc. Thus (16) holds.
   Also, ⟨𝑡𝑒 , 𝑓 ⟩ ∈ SPerm is in the resulting set of checks, which contradicts the premises of (17),
therefore it vacuously holds.
   Case 11. SConsumeAccFailure – 𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ▷ 𝜎, {⊥}, {⟨𝑡𝑒 , 𝑓 ⟩}:
   ⟨𝐻, 𝛼 𝐸 ⟩ ⊢𝑉 ′ {⊥} is a contradiction, thus the lemma vacuously holds.
   Case 12. SConsumeConjunction – 𝜎, 𝜎𝐸 ⊢ 𝜙 1 ∗ 𝜙 2 ▷ 𝜎 ′′, R 1 ∪ R 2, Θ1 ∪ Θ2 :
   By SConsumeConjunction 𝜎, 𝜎𝐸 ⊢ 𝜙 1 ▷ 𝜎 ′, R 1, Θ1 and 𝜎 ′, 𝜎𝐸 [𝑔 = 𝑔(𝜎 ′ )] ⊢ 𝜙 2 ▷ 𝜎 ′′, R 2, Θ2 . Let
𝑉1 and 𝑉 ′ be the respective corresponding valuations, with initial valuations 𝑉 and 𝑉1 , respectively.
Then 𝑉 ′ is the corresponding valuation for this case.
   By lemma 33, 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎 ′ ). Thus 𝑉 ′ (𝑔(𝜎 ′ )) = 𝑉1 (𝑔(𝜎 ′ )) = true. Also, ⟨𝐻, 𝛼 𝐸 ⟩ ⊢𝑉1 R 1 by
lemma 23, since 𝑉 ′ extends 𝑉1 .
   By SConsumeConjunction (R 1 ∪ R 2 ) ∩ SPerm = ∅, thus R 1 ∩ SPerm = ∅.
   Let 𝛼 1 = 𝑉 LΘ1 M𝐻 . By induction, using (17), ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙 1 . Thus ⟨𝐻, 𝛼 1, 𝜌⟩ ⊨ 𝜙 1 and 𝛼 1 ⊆ 𝛼 by
lemma 40.
   Also ⟨𝐻, 𝛼 \ 𝛼 1, 𝜌⟩ 𝑉 𝜎 ′ by induction, ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ 𝑉 𝜎𝐸 [𝑔 = 𝑔(𝜎 ′ )] since 𝑉1 extends 𝑉 and
                            1                                 1
𝑉1 (𝑔(𝜎 ′ )) = true, and ⟨𝐻, 𝛼 𝐸 ⟩ ⊢𝑉 R 2 by lemma 23. Finally, by assumptions 𝑉 ′ (𝑔(𝜎 ′′ )) = true, and
(𝛼 \ 𝛼 1 ) ⊆ 𝛼 ⊆ 𝛼 𝐸 . Thus by induction ⟨𝐻, (𝛼 \ 𝛼 1 ) \ 𝑉 LΘ2 M𝐻 , 𝜌⟩ 𝑉 ′ 𝜎 ′′ .
Gradually Verifying Unfolding Expressions & Pure Functions                                                71


 Also by induction, using (17), ⟨𝐻, 𝛼 \ 𝛼 1, 𝜌⟩ ⊨ 𝜙 2 .
  Now (𝛼\𝛼 1 ) ⊆ 𝛼, 𝛼 1 ⊆ 𝛼, and (𝛼\𝛼 1 )∩𝛼 1 = ∅. Therefore ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙 1 ∗𝜙 2 by AssertConjunction,
which proves (17). Then by lemma 9 ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊨ 𝜙 1 ∗ 𝜙 2 .
 As shown before, ⟨𝐻, (𝛼 \ 𝛼 1 ) \ 𝑉 LΘ2 M𝐻 , 𝜌⟩ 𝑉 ′ 𝜎 ′′ , and (𝛼 \ 𝛼 1 ) \ 𝑉 LΘ2 M𝐻 = 𝛼 \ (𝑉 LΘ1 M𝐻 ∪
𝑉 LΘ2 M𝐻 ) = 𝛼 \ 𝑉 LΘ1 ∪ Θ2 M𝐻 , therefore ⟨𝐻, 𝛼 \ 𝑉 LΘ1 ∪ Θ2 M𝐻 , 𝜌⟩ 𝑉 ′ 𝜎 ′′ .
   By induction ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊢frmI 𝜙 1 and ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊢frmI 𝜙 2 . Therefore ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊢frmI 𝜙 1 ∗ 𝜙 2 by
IFrameConjunction, which completes the proof of (16).
   Case 13. SConsumeConjunctionImprecise – 𝜎, 𝜎𝐸 ⊢ 𝜙 1 ∗ 𝜙 2 ▷ 𝜎 ′′, R 1 ∪ R 2 ; sep(Θ1, Θ2 ), Θ1 ∪ Θ2 :
   Similar to case 12, except when showing that ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊨ 𝜙 1 ∗ 𝜙 2 and when proving (17):
   By induction ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊨ 𝜙 1 and ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊨ 𝜙 2 . Thus by lemma 40 ⟨𝐻, 𝑉 ′ LΘ1 M𝐻 , 𝜌⟩ ⊨ 𝜙 1 ,
⟨𝐻, 𝑉 ′ LΘ2 M𝐻 , 𝜌⟩ ⊨ 𝜙 2 , and 𝑉 ′ LΘ1 M𝐻 ∪ 𝑉 ′ LΘ2 M𝐻 ⊆ 𝛼 𝐸 .
   By assumptions ⟨𝐻, 𝛼 𝐸 ⟩ ⊢𝑉 ′ sep(Θ1, Θ2 ). Then by CheckSep 𝑉 ′ LΘ1 M𝐻 ∩ 𝑉 ′ LΘ2 M𝐻 = ∅. Therefore
⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊨ 𝜙 1 ∗ 𝜙 2 by AssertConjunction.
   By SConsumeConjunctionImprecise (R 1 ∪ R 2 ) ∩ SPerm ≠ ∅. Therefore the premises of (17) do
not hold, therefore it is vacuously true.
   Case 14. SConsumeConditionalA – 𝜎, 𝜎𝐸 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ▷ 𝜎 ′, R ∪ R ′, Θ:
   By SConsumeConditionalA, 𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎𝐸′ , R and 𝜎 [𝑔 = 𝑔′ ], 𝜎𝐸 [𝑔 = 𝑔′ ] ⊢ 𝜙 1 ▷ 𝜎 ′, R ′, Θ where
𝑔 = 𝑔(𝜎) && 𝑡. Let 𝑉1 and 𝑉 ′ be the respective corresponding valuations, with initial valuations 𝑉
 ′

and 𝑉1 , respectively. Then 𝑉 ′ is the corresponding valuation for this case.
   By lemma 33 𝑔(𝜎 ′ ) =⇒ 𝑔′ = 𝑔(𝜎) && 𝑡, thus 𝑉 ′ (𝑔(𝜎) && 𝑡) = 𝑉1 (𝑔(𝜎) && 𝑡) = true. Therefore
⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 [𝑔 = 𝑔(𝜎) && 𝑡] and ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎𝐸 [𝑔 = 𝑔(𝜎) && 𝑡].
             1                                         1
   By assumptions and lemma 23 ⟨𝐻, 𝛼 𝐸 ⟩ ⊢𝑉1 R. In addition, by lemma 27 𝑉1 (𝑔(𝜎𝐸′ )) = true. Thus
⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉1 (𝑡) by lemma 26. Furthermore, 𝑉1 (𝑡) = true since 𝑔(𝜎) && 𝑡 =⇒ 𝑡, thus ⟨𝐻, 𝜌⟩ ⊢
𝑒 ⇓ true. Finally, ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊨ 𝜙 1 by induction. Therefore ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊨ if 𝑒 then 𝜙 1 else 𝜙 2 by
AssertIfA.
   Also by induction ⟨𝐻, 𝛼 \ 𝑉 ′ LΘM𝐻 , 𝜌⟩ 𝑉 ′ 𝜎 ′ .
   Finally, ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊢frm 𝜙 1 by induction, and ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊢frm 𝑒 by lemma 26. As shown before,
⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ true. Therefore ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊢frm if 𝑒 then 𝜙 1 else 𝜙 2 by FrameIfA, which completes
the proof of (16).
   Now suppose that (R ∪ R ′ ) ∩ SPerm = ∅, thus R ′ ∩ SPerm = ∅. Then by induction ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙,
and as before ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ true, therefore ⟨𝐻, 𝛼, 𝜌⟩ ⊨ if 𝑒 then 𝜙 1 else 𝜙 2 by AssertIfA, which
completes the proof of (17).
   Case 15. SConsumeConditionalB – 𝜎, 𝜎𝐸 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ▷ 𝜎 ′, R ∪ R ′, Θ: Similar to case
14.
                                                                                                            □

Lemma 42 (Soundness of consume (long form)). Let 𝜙˜ be some specification, 𝜎 and 𝜎𝐸 some
well-formed symbolic states such that 𝑔(𝜎) =⇒ 𝑔(𝜎𝐸 ), and ⟨𝐻, 𝛼, 𝜌⟩ some evaluation state such
that ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 and ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎𝐸 .
  If 𝜎, 𝜎𝐸 ⊢ 𝜙˜ ▷ 𝜎 ′, R, Θ with corresponding valuation 𝑉 ′ , ⟨𝐻, 𝛼 𝐸 ⟩ ⊢𝑉 ′ R, and 𝑉 ′ (𝑔(𝜎 ′ )) = true,
then
                                                         ˜ ⟨𝐻, 𝜌 ⟩ , 𝜌⟩ ′ 𝜎 ′ .
                          ⟨𝐻, 𝛼 𝐸 , 𝜌⟩ ⊨ 𝜙˜ and ⟨𝐻, 𝛼 \ T𝜙U                 𝑉

Lemma 43 (Soundness of consume (short form)). Let 𝜙˜ be some specification, 𝜎 be some well-
formed symbolic state, ⟨𝐻, 𝛼, 𝜌⟩ some evaluation state, and 𝑉 be some valuation such that
⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎.
72                                                                                                   Torek et al.


     If 𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, R with corresponding valuation 𝑉 ′ , ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R, and 𝑉 ′ (𝑔(𝜎 ′ )) = true then

                           ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙˜    and             ˜ ⟨𝐻, 𝜌 ⟩ , 𝜌⟩ ′ 𝜎 ′ .
                                                    ⟨𝐻, 𝛼 \ T𝜙U            𝑉

Lemma 44 (Progress of consume (long form)). For any heap 𝐻 , 𝜎, 𝜎𝐸 , 𝜙,     ˜ and valuation 𝑉 , if
𝑉 (𝑔(𝜎𝐸 )) = true then 𝜎, 𝜎𝐸 ⊢ 𝜙 ▷ 𝜎 , _, _ for some 𝜎 such that 𝑉 (𝑔(𝜎 )) = true where 𝑉 ′ is the
                                ˜   ′                 ′           ′    ′

corresponding valuation.

   Proof. By induction on the syntax forms of 𝜙:
   Case 1. 𝑒 ∈ Expr: By lemma 27, 𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡 ⊣ _, _ for some 𝑡. Then one of the following cases
applies to yield 𝜎, 𝜎𝐸 ⊢ 𝑒 ▷ 𝜎, _, _:
   Case 1(a). 𝑔(𝜎) =⇒ 𝑡: Then SConsumeValue applies.
   Case 1(b). 𝜄 (𝜎) and 𝑔(𝜎) =⇒      Y 𝑡: Then SConsumeValueImprecise applies.
   Case 1(c). ¬𝜄 (𝜎) and 𝑔(𝜎) =⇒       Y 𝑡: Then SConsumeValueFailure applies.
   Case 2. 𝑝 (𝑒) – 𝑝 ∈ Predicate, 𝑒 ∈ Expr:
   By lemma 27, for each 𝑒, 𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡 ⊣ _, _ for some 𝑡. Then one of the following cases applies to
yield 𝜎, 𝜎𝐸 ⊢ 𝑝 (𝑒) ▷ 𝜎 ′, _, _ where 𝑔(𝜎 ′ ) = 𝑔(𝜎):
   Case 2(a). 𝑝 (𝑡 ′ ) ∈ H(𝜎) and 𝑔(𝜎) =⇒ 𝑡 == 𝑡 ′ for some 𝑡 ′ : Then SConsumePredicate applies.
   Case 2(b). 𝜄 (𝜎) and  ⟨𝑝, 𝑡 ′ ⟩ ∈ H(𝜎) : 𝑔(𝜎) =⇒ 𝑡 == 𝑡 ′ : Then SConsumePredicateImprecise
                                                   Ó
applies.
   Case 2(c). ¬𝜄 (𝜎) and  ⟨𝑝, 𝑡 ′ ⟩ ∈ H(𝜎) : 𝑔(𝜎) =⇒ 𝑡 == 𝑡 ′ : Then SConsumePredicateFailure
                                                    Ó
applies.
   Case 3. acc(𝑒.𝑓 ) – 𝑒 ∈ Expr, 𝑓 ∈ Field:
   By lemma 27, 𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ _, _ for some 𝑡𝑒 . Note that remf and remfp are defined for all inputs.
Then one of the following cases applies to yield 𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ▷ 𝜎 ′, _, _ where 𝑔(𝜎 ′ ) = 𝑔(𝜎 ′ ):
   Case 3(a). ⟨𝑓 , 𝑡𝑒′ , 𝑡⟩ ∈ H(𝜎) and 𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒 for some 𝑡𝑒′ and 𝑡: Then SConsumeAcc applies.
   Case 3(b).  𝑡𝑒′ , 𝑡 : ⟨𝑓 , 𝑡𝑒 , 𝑡⟩ ∈ H(𝜎) ∧ (𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒 ) and ⟨𝑓 , 𝑡𝑒′ , 𝑡⟩ ∈ H(𝜎) for some 𝑡𝑒′ and 𝑡
where 𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒 : Then
SConsumeAccOptimistic applies.
   Case 3(c).  𝑡𝑒′ , 𝑡 : ⟨𝑓 , 𝑡𝑒 , 𝑡⟩ ∈ H(𝜎) ∪ H (𝜎) ∧ (𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒 ) and 𝜄 (𝜎): Then
SConsumeAccImprecise applies.
   Case 3(d).  𝑡𝑒′ , 𝑡 : ⟨𝑓 , 𝑡𝑒 , 𝑡⟩ ∈ H(𝜎) ∪ H (𝜎) ∧ (𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒 ) and ¬𝜄 (𝜎): Then
SConsumeAccFailure applies.
   Case 4. 𝜙 1 ∗ 𝜙 2 – 𝜙 1, 𝜙 2 ∈ Formula
   By induction, 𝜎, 𝜎𝐸 ⊢ 𝜙 1 ▷ 𝜎 ′, _, _ for some 𝜎 ′ such that 𝑉 ′ (𝑔(𝜎 ′ )) = true where 𝑉 ′ is the
corresponding valuation.
   Then also by induction, 𝜎 ′, 𝜎𝐸 [𝑔 = 𝑔(𝜎 ′ )] ⊢ 𝜙 2 ▷ 𝜎 ′′, _, _ for some 𝜎 ′′ such that 𝑉 ′′ (𝑔(𝜎 ′′ )) =
true where 𝑉 ′′ is the corresponding valuation, with initial valuation 𝑉 ′ . Then one of the following
cases applies to yield 𝜎, 𝜎𝐸 ⊢ 𝜙 1 ∗ 𝜙 2 ▷ 𝜎 ′′, _, _:
   Case 4(a). (R 1 ∪ R 2 ) ∩ SPerm ≠ ∅: Then SConsumeConjunctionImprecise applies.
   Case 4(b). (R 1 ∪ R 2 ) ∩ SPerm = ∅: Then SConsumeConjunction applies.
   Case 5. if 𝑒 then 𝜙 1 else 𝜙 2 – 𝑒 ∈ Expr, 𝜙 1, 𝜙 2 ∈ Formula:
   By lemma 27, 𝜎𝐸 ⊢ 𝑒 ⇓ 𝑡 ⊣ _, _ for some 𝑡. Let 𝑉 ′ be the valuation corresponding to this derivation.
Then since this is a well-typed program, one of the following cases must apply:
   Case 5(a). 𝑉 ′ (𝑡) = true: Let 𝑔′ = 𝑔(𝜎)&&𝑡. Then 𝑉 (𝑔′ ) = true and by induction, 𝜎 [𝑔 = 𝑔′ ], 𝜎𝐸 [𝑔 =
𝑔 ] ⊢ 𝜙 1 ▷ 𝜎 ′, _, _ for some 𝜎 ′ where 𝑉 ′′ (𝑔(𝜎 ′ )) = true for the corresponding derivation 𝑉 ′′ with
 ′

initial valuation 𝑉 ′ . Then by SConsumeConditionalA, 𝜎, 𝜎𝐸 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ▷ 𝜎 ′, _, _, and
𝑉 ′′ is the corresponding valuation for this derivation with initial valuation 𝑉 .
Gradually Verifying Unfolding Expressions & Pure Functions                                           73


   Case 5(b). 𝑉 ′ (𝑡) = false: Let 𝑔′ = 𝑔(𝜎) && ! 𝑡. Then 𝑉 (𝑔′ ) = true and by induction, 𝜎 [𝑔 =
𝑔′ ], 𝜎        ′          ′                 ′       ′′    ′
       𝐸 [𝑔 = 𝑔 ] ⊢ 𝜙 2 ▷𝜎 , _, _ for some 𝜎 where 𝑉 (𝑔(𝜎 )) = true for the corresponding derivation
𝑉 with initial valuation 𝑉 . Then by SConsumeConditionalB, 𝜎, 𝜎𝐸 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ▷ 𝜎 ′,
  ′′                            ′

_, _, and 𝑉 ′′ is the corresponding valuation for this derivation with initial valuation 𝑉 .
                                                                                                   □

Lemma 45 (Progress of consume (short form)). For any heap 𝐻 , 𝜎, 𝜙,   ˜ and valuation 𝑉 , if 𝑉 (𝑔(𝜎)) =
true then 𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, _ for some 𝜎 ′ such that 𝑉 ′ (𝑔(𝜎 ′ )) = true where 𝑉 ′ is the corresponding
valuation.

D.5       Progress
Definition 40. For a derivations Σ ⇀ 𝜎 ⊣ R, Θ, given an initial valuation 𝑉 , heap 𝐻 , and
environment 𝜌 the corresponding valuation is denoted as
                                          𝑉 [Σ ⇀ 𝜎 ⊣ R, Θ | 𝐻, 𝜌].
This function is defined as follows, depending on the rule that proves the derivation. Values are
referenced using the respective name from the rule definition.
 • SGuardInit:
                             𝑉 [init ⇀ ⟨⊥, ∅, ∅, ∅, true⟩ ⊣ ∅, ∅ | 𝐻, 𝜌] := 𝑉
 • SGuardSeq:
                                                ˜ ⇀ 𝜎 ⊣ ∅, ∅ | 𝐻, 𝜌] := 𝑉
                                𝑉 [⟨𝜎, skip; 𝑠, 𝜙⟩
 • SGuardAssign:
                                  ˜ ⇀ 𝜎 ⊣ R, ∅ | 𝐻, 𝜌] := 𝑉 [𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎 ′, R | 𝐻, 𝜌]
                 𝑉 [⟨𝜎, 𝑥 = 𝑒; 𝑠, 𝜙⟩
 • SGuardAssignField:
                                         ˜ ⇀ 𝜎 ′′ ⊣ R ′ ∪ R ′′, ∅ | 𝐻, 𝜌] :=
                     𝑉 [⟨𝜎, 𝑥 .𝑓 = 𝑒; 𝑠, 𝜙⟩
                       𝑉 [𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎 ′, R ′ | 𝐻, 𝜌] [𝜎 ′ ⊢ acc(𝑥 .𝑓 ) ▷ 𝜎 ′′, R ′′ | 𝐻, 𝜌]
 • SGuardAlloc:
                                                   ˜ ⇀ 𝜎 ⊣ ∅, ∅ | 𝐻, 𝜌] := 𝑉
                           𝑉 [⟨𝜎, 𝑥 = alloc(𝑆); 𝑠, 𝜙⟩
 • SGuardCall:
                                 ˜ ⇀ 𝜎 ′′ [𝛾 = 𝛾 (𝜎)] ⊣ R ∪ R ′, rem(𝜎 ′′, pre(𝑚)) | 𝐻, 𝜌] :=
             𝑉 [⟨𝜎, 𝑦 = 𝑚(𝑒); 𝑠, 𝜙⟩
               𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R | 𝐻, 𝜌] [𝜎 ′ [𝛾 = [𝑥 ↦→ 𝑡]] ⊢ pre(𝑚) ▷ 𝜎 ′′, R ′ | 𝐻, 𝜌]
 • SGuardAssert:
                                   ˜ ⇀ 𝜎 ′ ⊣ R, ∅ | 𝐻 ] := 𝑉 [𝜎 ⊢ ? ∗ 𝜙 ▷ 𝜎 ′, R | 𝐻, 𝜌]
               𝑉 [⟨𝜎, assert 𝜙; 𝑠, 𝜙⟩
 • SGuardFold:
                                  ˜ ⇀ 𝜎 ′′ [𝛾 = 𝛾 (𝜎)] ⊣ _, ∅ | 𝐻, 𝜌] :=
            𝑉 [⟨𝜎, fold 𝑝 (𝑒); 𝑠, 𝜙⟩
              𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R | 𝐻, 𝜌] [𝜎 ′ [𝛾 = [𝑥 ↦→ 𝑡]] ⊢ predicate(𝑝) ▷ 𝜎 ′′, R ′ | 𝐻, 𝜌]
 • SGuardUnfold:
                                                                     Ø
                                               ˜ ⇀ 𝜎 ′′ ⊣ R ′ ∪
                       𝑉 [⟨𝜎, unfold 𝑝 (𝑒); 𝑠, 𝜙⟩                        R, ∅ | 𝐻, 𝜌] :=
                          𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R | 𝐻, 𝜌] [𝜎 ⊢ 𝑝 (𝑒) ▷ 𝜎 , R ′ | 𝐻, 𝜌]
                                                             ′           ′′
74                                                                                                 Torek et al.


 • SGuardIf:
                                                          ˜ ⇀ 𝜎 ′ ⊣ R, ∅ | 𝐻, 𝜌] :=
                       𝑉 [⟨𝜎, if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠, 𝜙⟩
                          𝑉 [𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎 ′, R | 𝐻, 𝜌]
 • SGuardWhile:
            𝑉 [⟨𝜎, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′, 𝜙˜ ′ ⟩ ⇀ 𝜎 ′ [𝑔 = 𝑔(𝜎 ′′ )] ⊣ _, _ | 𝐻, 𝜌] :=
               𝑉0 [𝑡 ↦→ 𝑉0 (𝛾 (𝜎 ′ ) (𝑥))] [𝜎 ′ [𝛾 = 𝛾 (𝜎 ′ ) [𝑥 ↦→ 𝑡]] ⊢ 𝜙˜ ◁ 𝜎 ′′ | 𝐻, 𝜌]

   where 𝑉0 = 𝑉 [𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, R ′ | 𝐻, 𝜌].
 • SGuardFinish:
                𝑉 [⟨𝜎, skip, 𝜙⟩ ˜ ⇀ 𝜎 ′ ⊣ R, ∅ | 𝐻, 𝜌] := 𝑉 [𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, R | 𝐻, 𝜌]

Lemma 46. If ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙˜ and ⟨𝐻, 𝛼 \ T𝜙U
                                         ˜ ⟨𝐻, 𝛼 ⟩ , 𝜌⟩
                                                        𝑉
                                                          𝜎, then ⟨𝐻, 𝛼 \ 𝑉 ′ Lrem(𝜎 ′, 𝜙˜ ′ )M𝐻 , 𝜌⟩ ⊨ 𝜙.
                                                                                                        ˜

Theorem 1 (Progress, part 1). Let Γ be some dynamic state validated by Σ and valuation 𝑉 . If Σ ⇀
𝜎 ′ ⊣ R, Θ with corresponding valuation 𝑉 ′ extending 𝑉 , 𝑉 ′ (𝑔(𝜎 ′ )) = true, and ⟨𝐻, 𝛼 (Γ)⟩ ⊢𝑉 ′ R
then
                                     Π ⊢ Γ, 𝑉 ′ LΘM𝐻 (Γ) → Γ ′
for some Γ ′ .
   In other words, if the dynamic state satisfies the matching symbolic checks, then dynamic
execution can proceed.
    Proof. We proceed by cases on Σ ⇀ 𝜎 ′ ⊣ R, Θ.
    Case 1. SGuardInit: Result is trival by ExecInit.
    Case 2. SGuardSeq: Then Γ = ⟨𝐻, ⟨𝛼, 𝜌, skip; 𝑠⟩ · S ′ ⟩ for some 𝐻, 𝛼, 𝜌, 𝑠, S ′ , thus
⟨𝐻, ⟨𝛼, 𝜌, skip; 𝑠⟩ · S ′ ⟩, 𝑉 ′ L∅M𝐻 → ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · S ′ ⟩ by ExecSeq, and the result is immediate
from ExecStep.
    Case 3. SGuardAssign: Then Γ = ⟨𝐻, ⟨𝛼, 𝜌, 𝑥 = 𝑒; 𝑠⟩ · S ′ ⟩ for some 𝐻, 𝛼, 𝜌, S ′ .
    By SGuardAssign 𝜎 (Σ) ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R for some 𝑡, 𝜎 ′, R. Also, 𝑉 ′ = 𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R | 𝐻 ].
Since Γ corresponds to Σ, by definition 32 ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 (Σ). By assumptions ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R, and
𝑉 ′ (𝑔(𝜎 ′ )) = true. Then ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡) and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 by lemma 26.
   Therefore ⟨𝐻, ⟨𝛼, 𝜌, 𝑥 = 𝑒; 𝑠⟩ · S ′ ⟩, 𝑉 ′ L∅M𝐻 → ⟨𝐻, ⟨𝛼, 𝜌 [𝑥 ↦→ 𝑉 ′ (𝑡)], 𝑠⟩ · S ′ ⟩ by ExecAssign,
and the result is immediate from ExecStep.
    Case 4. SGuardAssignField: Then Γ = ⟨𝐻, ⟨𝛼, 𝜌, 𝑥 .𝑓 = 𝑒; 𝑠⟩ · S ′ ⟩ for some 𝐻, 𝛼, 𝜌, 𝑥, 𝑓 , 𝑒, 𝑠, S ′ .
    By SGuardAssignField 𝜎 (Σ) ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R 1 for some 𝑡, 𝜎 ′, R 1 , and 𝜎 ′ ⊢ acc(𝑥 .𝑓 ) ▷ 𝜎 ′′, R 2 for
some 𝜎 ′′, R 2 . Also, 𝑉 ′ = 𝑉 [𝜎 (Σ) ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R 1 | 𝐻 ] [𝜎 ′ ⊢ acc(𝑥 .𝑓 ) ▷ 𝜎 ′′, R 2 | 𝐻 ].
    Since Γ corresponds to Σ, by definition 32 ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 (Σ). By assumptions ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R 1 ∪ R 2 ,
thus ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R 1 and ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R 2 by lemma 23, and 𝑉 ′ (𝑔(𝜎 ′′ )) = true, thus 𝑉 ′ (𝑔(𝜎 ′ )) = true
by lemma 34.
    Now ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡) and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 by lemma 26. Let ℓ = 𝜌 (𝑥), then ⟨𝐻, 𝜌⟩ ⊢ 𝑥 ⇓ 𝜌 (𝑥)
by EvalVar. Finally, ⟨𝐻, 𝛼, 𝜌⟩ ⊨ acc(𝑥 .𝑓 ) by lemma 43.
    Let 𝐻 ′ = 𝐻 [⟨ℓ, 𝑓 ⟩ ↦→ 𝑉 ′ (𝑡)]. Then ⟨𝐻, ⟨𝛼, 𝜌, 𝑥 .𝑓 = 𝑒; 𝑠⟩ · S ′ ⟩, 𝑉 ′ L∅M𝐻 → ⟨𝐻 ′, ⟨𝛼, 𝜌, 𝑠⟩ · S ′ ⟩
by ExecAssignField, and the result is immediate from ExecStep.
    Case 5. SGuardAlloc: Then Γ = ⟨𝐻, ⟨𝛼, 𝜌, 𝑥 = alloc(𝑆); 𝑠⟩ · S ′ ⟩ for some 𝐻, 𝛼, 𝜌, 𝑥, 𝑆, 𝑠, S ′ .
    Let ℓ = fresh, 𝑇 𝑓 = struct(𝑆), and 𝐻 ′ = 𝐻 [(ℓ, 𝑓 ) ↦→ default(𝑇 )]. Then
⟨𝐻, ⟨𝛼, 𝜌, 𝑥 = alloc(𝑆); 𝑠⟩ · S ′ ⟩, 𝑉 ′ L∅M𝐻 → ⟨𝐻 ′, ⟨𝛼, 𝜌, 𝑠⟩ · S ′ ⟩ by ExecAlloc, and the result is
immediate from ExecStep.
Gradually Verifying Unfolding Expressions & Pure Functions                                              75


   Case 6. SGuardCall: Then Γ = ⟨𝐻, ⟨𝛼, 𝜌, 𝑦 = 𝑚(𝑒); 𝑠⟩⟩ · S for some 𝐻, 𝛼, 𝜌, 𝑦, 𝑚, 𝑒, 𝑠, S. Let
𝑥 = params(𝑚).
   By SGuardCall 𝜎 (Σ) ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R for some 𝑡, 𝜎 ′, R, and 𝜎 ′ [𝛾 = [𝑥 ↦→ 𝑡]] ⊢ pre(𝑚) ▷ 𝜎 ′′, R ′
for some 𝜎 ′′, R ′ .
  Also, by definition 𝑉 ′ = 𝑉 [𝜎 (Σ) ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R | 𝐻 ] [𝜎 ′ [𝛾 = 𝑥 ↦→ 𝑡] ⊢ pre(𝑚) ▷ 𝜎 ′′, R ′ | 𝐻 ].
   Since Γ corresponds to Σ, by definition 32 ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 (Σ). By assumptions, 𝑉 ′ (𝑔(𝜎 ′′ )) = true
thus 𝑉 ′ (𝑔(𝜎 ′ )) = true by lemma 34, and ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R ∪ R ′ , thus ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R and ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R ′
by lemma 23.
  Then ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡), ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒, and ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ by lemma 26.
  Let 𝛾 ′ = [𝑥 ↦→ 𝑡] and 𝜌 ′ = [𝑥 ↦→ 𝑉 ′ (𝑡)]. Since ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ and 𝜌 ′ 𝑉 ′ 𝛾 ′ by construction,
⟨𝐻, 𝛼, 𝜌 ′ ⟩ 𝑉 ′ 𝜎 ′ [𝛾 = 𝛾 ′ ].
  Let 𝛼𝑉 = 𝑉 ′ Lrem(𝜎 ′, pre(𝑚))M𝐻 and 𝛼 𝐸 = Tpre(𝑚)U ⟨𝐻, 𝜌 ⟩ .
  As noted before, 𝜎 ′ [𝛾 = 𝛾 ′ ] ⊢ pre(𝑚) ▷ 𝜎 ′′, R ′ by SExecCall. Also, 𝑉 ′ (𝑔(𝜎 ′′ )) = true and
⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R ′ . Therefore ⟨𝐻, 𝛼 \ 𝛼 𝐸 , 𝜌 ′ ⟩ 𝑉 ′ 𝜎 ′ and ⟨𝐻, 𝛼, 𝜌⟩ ⊨ pre(𝑚) by lemma 43.
  Then ⟨𝐻, 𝛼 \ 𝛼𝑉 , 𝜌⟩ ⊨ pre(𝑚) by lemma 46.
  Let 𝛼 ′ = ⌊pre(𝑚)⌋ ⟨𝐻, 𝛼\𝛼𝑉 , 𝜌 ′ ⟩ . Then ⟨𝐻, ⟨𝛼, 𝜌, 𝑦=𝑚(𝑒); 𝑠⟩·S⟩, 𝛼𝑉 → ⟨𝐻, ⟨𝛼 ′, 𝜌 ′, body(𝑚); skip⟩·
⟨𝛼 \ 𝛼 ′, 𝜌, 𝑦 = 𝑚(𝑒); 𝑠⟩ · S⟩ by ExecCallEnter, and the result is immediate from ExecStep.
  Case 7. SGuardAssert: Then Γ = ⟨𝐻, ⟨𝛼, 𝜌, assert 𝜙; 𝑠⟩ · S⟩ for some 𝐻, 𝛼, 𝜌, 𝜙, 𝑠, S.
  By SGuardAssert 𝜎 (Σ) ⊢ ? ∗ 𝜙 ▷ 𝜎 ′, R, also 𝑉 ′ = 𝑉 [𝜎 (Σ) ⊢ ? ∗ 𝜙 ▷ 𝜎 ′, R | 𝐻 ].
  Since Γ corresponds to Σ, by definition 32 ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 (Σ). Also by assumptions, ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R,
and 𝑉 ′ (𝑔(𝜎 ′ )) = true. Thus ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙 by lemma 43 since ? ∗ 𝜙 is a specification.
  Therefore ⟨𝐻, ⟨𝛼, 𝜌, assert 𝜙; 𝑠⟩ · S⟩, 𝑉 ′ L∅M𝐻 → ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · S⟩ by ExecAssert, and the
result is immediate from ExecStep.
  Case 8. SGuardFold: Then 𝑠 (Σ) = 𝑠 (Γ) = fold 𝑝 (𝑒) for some 𝑝, 𝑒. Thus ExecFold trivially applies,
and the result is immediate from ExecStep.
  Case 9. SGuardUnfold: Then 𝑠 (Σ) = 𝑠 (Γ) = unfold 𝑝 (𝑒) for some 𝑝, 𝑒. Thus ExecUnfold trivially
applies, and the result is immediate from ExecStep.
  Case 10. SGuardIf: Then 𝑠 (Σ) = 𝑠 (Γ) = if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠 for some 𝑒, 𝑠 1, 𝑠 2 , and thus
Γ = ⟨𝐻, ⟨𝛼, 𝜌, if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠⟩ · S⟩ for some 𝐻, 𝛼, 𝜌, S.
  By SGuardIf 𝜎 (Σ) ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R for some 𝑡, 𝜎 ′, R, and also 𝑉 ′ = 𝑉 [𝜎 (Σ) ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R | 𝐻 ].
  Now by assumptions 𝑉 ′ (𝑔(𝜎 ′ )) = true and ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R. Then ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡) and
⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 by lemma 26.
  Now, since we assume a well-typed program, 𝑉 ′ (𝑡) = true or false. Then either ExecIfA or
ExecIfB applies, and the result is immediate from ExecStep.
  Case 11. SGuardWhile: Then 𝑠 (Σ) = 𝑠 (Γ) = while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ for some 𝑒, 𝜙,         ˜ 𝑠, 𝑠 ′ ,
and thus Γ = ⟨𝐻, ⟨𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ⟩ · S⟩ for some 𝐻 , 𝛼, 𝜌, S.
                                                             ′

  Let 𝑥 = modified(𝑠). By SGuardWhile 𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, R ′ , 𝜎 ′ [𝛾 = 𝛾 (𝜎 ′ ) [𝑥 ↦→ fresh]] ⊢ 𝜙˜ ◁ 𝜎 ′′ ,
and 𝜎 ′′ ⊢ 𝑒 ⇓ 𝑡 ⊣ _, R ′′ . Then by definition 40 𝑉 ′ extends the corresponding valuation for these
judgements.
  By assumptions 𝑉 ′ (𝑔(𝜎 ′′ )) = true, thus 𝑉 ′ (𝑔(𝜎 ′ )) = true by lemma 29.
  Also by assumptions ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R ′ ∪ R ′′ , thus ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R ′ and ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R ′′ by lemma 23.
  Therefore ⟨𝐻, 𝛼 \ T𝜙U    ˜ ⟨𝐻, 𝛼 ⟩ , 𝜌⟩ ′ 𝜎 ′ and ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙˜ by lemma 43.
                                          𝑉
  Let 𝛼ˆ = 𝑉 ′ Lrem(𝜎 ′, 𝜙)M
                           ˜ 𝐻 . Then by lemma 46 ⟨𝐻, 𝛼 \ 𝛼,            ˜
                                                                ˆ 𝜌⟩ ⊨ 𝜙.
76                                                                                                          Torek et al.


  Let 𝑡 be the list of fresh values used in 𝜎 ′ [𝛾 = 𝛾 (𝜎 ′ ) [𝑥 ↦→ fresh]] ⊢ 𝜙˜ ◁ 𝜎 ′′ when applying
SGuardWhile. Let 𝛾 ′ = 𝛾 (𝜎 ′ ) [𝑥 ↦→ 𝑡]. Then by definition 40, and since 𝜌 ′ 𝛾 (𝜎 ′ ), for each pair of
                                                                                     𝑉
𝑥 and 𝑡, 𝑉 ′ (𝛾 ′ (𝑥)) = 𝑉 ′ (𝑡) = 𝑉 ′ (𝛾 (𝜎 ′ ) (𝑥)) = 𝜌 (𝑥).
  Therefore 𝜌 𝑉 ′ 𝛾 ′ , and thus ⟨𝐻, 𝛼 \ T𝜙U        ˜ ⟨𝐻, 𝛼 ⟩ , 𝜌⟩ ′ 𝜎 ′ [𝛾 = 𝛾 ′ ].
                                                                  𝑉
  Now by lemma 31 ⟨𝐻, 𝛼, 𝜙⟩        ˜ ′ 𝜎 ′′ .
                                       𝑉
     Also, as noted before, ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R ′′ . In addition, since 𝑉 ′ (𝑔(𝜎 ′′ )) = true, by lemma 27 𝜎 ′′ ⊢
𝑒 ⇓ 𝑡 ⊣ 𝜎 ′′′, R ′′ where 𝑉 ′ (𝑔(𝜎 ′′′ )) = true. Therefore ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡) by lemma 26.
     Let 𝛼 ′ = T𝜌U ⟨𝐻, 𝛼\𝛼ˆ ⟩ .
     Now, since we assume the program to be properly typed, one of the following subcases apply:
     Case 11(a). 𝑉 ′ (𝑡) = true: Then by ExecWhileSkip ⟨𝐻, ⟨𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ ⟩ ·
S⟩, 𝛼ˆ → ⟨𝐻, ⟨𝛼 ′, 𝜌, 𝑠; skip⟩ · ⟨𝛼 \ 𝛼 ′, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ ⟩ · S⟩ and the result is
immediate from ExecStep.
     Case 11(b). 𝑉 ′ (𝑡) = false: Then by ExecWhileSkip ⟨Π, 𝐻 ⟩, ⟨𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ ⟩·
S → ⟨𝛼,   ˆ 𝐻 ⟩⟨𝛼, 𝜌, 𝑠⟩ · S and the result is immediate from ExecStep.
     Case 12. SGuardFinish: Then 𝑠 (Σ) = 𝑠 (Γ) = skip and thus Γ = ⟨𝐻, ⟨𝛼, 𝜌, skip⟩ · S⟩ for some
𝐻, 𝛼, 𝜌, S.
     By SGuardFinish 𝜎 (Σ) ⊢ 𝜙˜ (Σ) ▷ 𝜎 ′, R, and 𝑉 ′ = 𝑉 [𝜎 (Σ) ⊢ 𝜙˜ (Σ) ▷ 𝜎 ′, R | 𝐻 ]. By assumptions,
𝑉 (𝑔(𝜎 ′ )) = true and ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R. Therefore ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙˜ (Σ).
   ′

     Since Γ is a valid state, the partial state ⟨𝐻, S⟩ must be validated by Σ and 𝑉 , thus one of the
following subcases must apply:
     Case 12(a). S = nil – then Γ = ⟨𝐻, ⟨𝛼, 𝜌, skip⟩ · nil⟩. Then ExecFinal trivially applies to yield
the result.
     Case 12(b). S = ⟨𝛼 0, 𝜌 0, 𝑚(𝑒); 𝑠 0 ⟩ · S ′ for some 𝛼 0, 𝜌 0, 𝑚, 𝑒, 𝑠 0, S ′ and 𝜙˜ (Σ) = post(𝑚).
     Since 𝜙˜ (Σ) = post(𝑚), ⟨𝐻, 𝛼, 𝜌⟩ ⊨ post(𝑚). Then ExecCallExit applies, and the result is imme-
diate from ExecStep.
     Case 12(c). S = ⟨𝛼 0, 𝜌 0, while 𝑒 invariant 𝜙˜ do 𝑠 0 ; 𝑠 0′ ⟩ · S ′ for some 𝛼 0, 𝜌 0, 𝑒, 𝜙, ˜ 𝑠 0, 𝑠 ′ , S ′ and
                                                                                                            0
𝜙˜ (Σ) = 𝜙. ˜
     Since 𝜙˜ (Σ) = post(𝑚), ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙.   ˜ Then ExecWhileFinish applies, and the result is immediate
from ExecStep.
                                                                                                                       □

Theorem 2 (Progress, part 2). Let Γ be some well-formed dynamic state validated by Σ and
valuation 𝑉 . Then if Γ ≠ final and ⟨𝐻 (Γ), 𝛼⟩ ⊢𝑉 ′ R,

                                                    Σ ⇀ 𝜎 ′, R, Θ

for some 𝜎 ′ , R, Θ such that 𝑉 ′ (𝑔(𝜎 ′ )) = true where 𝑉 ′ is the corresponding valuation extending
𝑉 ′.
   In other words, there is always some matching guard that computes the necessary checks.

   Proof. First, if Γ = init, then SGuardInit applies to yield the desired result.
   Otherwise, Γ = ⟨𝐻, S⟩ for some non-empty stack. Therefore Σ = ⟨𝜎, 𝑠, 𝜙⟩       ˜ for some 𝜎, 𝑠, and 𝜙˜
such that ⟨𝐻, 𝛼 (Γ), 𝜌 (Γ)⟩ 𝑉 𝜎 and 𝑠 = 𝑠 (Γ).
   Then one of the following cases apply since S is a well-formed stack:
   Case 1. 𝑠 = skip: By lemma 45 𝜎 ⊢ 𝜙˜ ▷𝜎 ′, R for some 𝜎 ′ , R such that 𝑉 ′ (𝑔(𝜎 ′ )) = true where 𝑉 ′
is the corresponding valuation. Then by SGuardFinish Σ ⇀ 𝜎 ′ ⊣ R, ∅ and 𝑉 ′ is the corresponding
valuation for this judgement.
Gradually Verifying Unfolding Expressions & Pure Functions                                                  77


    Case 2. 𝑠 = 𝑠 ′ ; 𝑠 ′′ for some 𝑠 ′ , 𝑠 ′′ : We complete the proof by proving the following statement by
induction on the syntax form of 𝑠 ′ :
    If 𝑠 = 𝑠 ′ ; 𝑠 ′′ then Σ ⇀ 𝜎 ′, R, Θ for some 𝜎 ′ , R, Θ such that 𝑉 ′ (𝑔(𝜎 ′ )) = true where 𝑉 ′ is the
corresponding valuation extending 𝑉 ′ .
    Case 2(a). 𝑠 ′ = 𝑠 1 ; 𝑠 2 : By lemma 20, 𝑠 ′ = 𝑠 1′ ; 𝑠 2′ where 𝑠 1′ is not a sequence statement. Then
𝑠; 𝑠 ′ = 𝑠 1′ ; 𝑠 2′ ; 𝑠 ′ .
    Then the inductive hypothesis applies, which completes the proof.
    Case 2(b). 𝑠 ′ = skip: Then Σ ⇀ 𝜎 ⊣ ∅, ∅ by SGuardSeq.
    Case 2(c). 𝑠 ′ = 𝑥 =𝑒: By lemma 27, 𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎 ′, R for some 𝜎 ′ and R such that 𝑉1 (𝑔(𝜎 ′ )) = true
for the corresponding valuation 𝑉1 .
    Then Σ ⇀ 𝜎 ′ ⊣ R, ∅ by SGuardAssign. By definition the corresponding valuation extends 𝑉1 ,
thus 𝑉 ′ (𝑔(𝜎 ′ )) = true.
    Case 2(d). 𝑥 .𝑓 = 𝑒:
    By lemma 27 𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎 ′, R ′ for some 𝜎 ′ and R ′ such that 𝑉1 (𝑔(𝜎 ′ )) = true where 𝑉1 is the
corresponding valuation extending 𝑉 .
    By lemma 45 𝜎 ′ ⊢ acc(𝑥 .𝑓 ) ▷ 𝜎 ′′, R ′′ for some 𝜎 ′′ and R ′′ such that 𝑉2 (𝑔(𝜎 ′′ )) = true for
corresponding valuation 𝑉2 , with initial valuation 𝑉1 .
    Then Σ ⇀ 𝜎 ′′ ⊣ R ′ ∪ R ′′, ∅ by SGuardAssignField. By definition the corresponding valuation
𝑉 extends 𝑉2 , therefore 𝑉 ′ (𝑔(𝜎 ′′ )) = true.
  ′

    Case 2(e). 𝑥 = alloc(𝑆):
    Then Σ ⇀ 𝜎 ⊣ ∅, ∅ by SGuardAlloc.
    Case 2(f). 𝑦 = 𝑚(𝑒 1, · · · , 𝑒𝑛 ):
    Let 𝜎0 = 𝜎 and 𝑉0 = 𝑉 , then for each 𝑒𝑖 , 𝜎𝑖 −1 ⊢ 𝑒 ⇓ 𝑡𝑖 ⊣ 𝜎𝑖 , _ for some 𝜎𝑖 such that 𝑉𝑖 (𝑔(𝜎𝑖 )) = true
for corresponding valuation 𝑉𝑖 , with initial valuation 𝑉𝑖 −1 , by lemma 27.
    Let 𝑥 1, · · · , 𝑥𝑛 = params(𝑚). By lemma 45, 𝜎𝑛 [𝛾 = [𝑥𝑖 ↦→ 𝑡𝑖 ]] ⊢ pre(𝑚) ▷ 𝜎 ′, _ for some 𝜎 ′ such
that 𝑉 ′ (𝑔(𝜎 ′ )) = true for corresponding valuation 𝑉 ′ , with initial valuation 𝑉𝑛 .
    Then Σ ⇀ 𝜎 ′ [𝛾 = 𝛾 (𝜎)] ⊣ R 1 ∪ · · · ∪ R𝑛 ∪ R ′, rem(𝜎 ′′, pre(𝑚)) by SGuardCall and 𝑉 ′ is the
corresponding valuation
    Case 2(g). assert 𝜙:     ˜
    By lemma 45 𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, R for some 𝜎 ′ and R where 𝑉 ′ (𝜎 ′ ) = true for the corresponding
valuation 𝑉 ′ .
    Then by SGuardAssert Σ ⇀ 𝜎 ′ ⊣ R, ∅ and 𝑉 ′ is the corresponding valuation.
    Case 2(h). if 𝑒 then 𝑠 1 else 𝑠 2 :
    By lemma 27 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R for some 𝑡, 𝜎 ′ such that 𝑉 ′ (𝑔(𝜎 ′ )) = true where 𝑉 ′ is the
corresponding valuation.
    Then Σ ⇀ 𝜎 ′ ⊣ R, ∅ by SGuardIf and 𝑉 ′ is the corresponding valuation.
    Case 2(i). while 𝑒 invariant 𝜙˜ do 𝑠 for some 𝑒, 𝜙,        ˜ 𝑠:
    By lemma 45 𝜎 ⊢ 𝜙 ▷ 𝜎 , R for some 𝜎 and R ′ such that 𝑉1 (𝑔(𝜎 ′ )) = true where 𝑉 ′ is the
                              ˜    ′    ′              ′

corresponding valuation.
    Let 𝑥 = modified(𝑠) and 𝜎 ′′ = 𝜎 ′ [𝛾 = 𝛾 (𝜎 ′ ) [𝑥 ↦→ fresh]].
    Let 𝑉2 = 𝑉1 [𝑡 ↦→ 𝑉1 (𝛾 (𝜎 ′ ) (𝑥))]. Then 𝑉2 (𝑔(𝜎 ′′ )) = 𝑉1 (𝑔(𝜎 ′ )) = true.
    Then by lemma 32 𝜎 ′′ ⊢ 𝜙˜ ◁ 𝜎 ′′′ for some 𝜎 ′′′ such that 𝑉3 (𝑔(𝜎 ′′′ )) = true where 𝑉3 is the
corresponding valuation extending 𝑉2 .
    By lemma 27 𝜎 ′′′ ⊢ 𝑒 ⇓ 𝑡 ⊣ _, _ for some 𝑡. Let 𝑉 ′ be the corresponding valuation extending 𝑉3 ,
thus 𝑉 ′ (𝑔(𝜎 ′′′ )) = 𝑉3 (𝑔(𝜎 ′′′ )) = true.
    Then Σ ⇀ 𝜎 ′ [𝑔 = 𝑔(𝜎 ′′′ )] ⊣ R ′ ∪ R ′′, rem(𝜎 ′, 𝜙)  ˜ by SGuardWhile and 𝑉 ′ is the corresponding
valuation.
78                                                                                                       Torek et al.


    Case 2(j). fold 𝑝 (𝑒 1, · · · , 𝑒𝑛 ):
    Let 𝜎0 = 𝜎 and 𝑉0 = 𝑉 . For each 𝑒𝑖 , 𝜎𝑖 −1 ⊢ 𝑒 ⇓ 𝑡𝑖 ⊣ 𝜎𝑖 , R𝑖 by lemma 27 for some 𝜎𝑖 and R𝑖 such
that 𝑉𝑖 (𝑔(𝜎𝑖 )) = true where 𝑉𝑖 is the corresponding valuation.
    Let 𝑥 1, · · · , 𝑥𝑛 = predicate_params(𝑝). By lemma 45 𝜎𝑛 [𝛾 = [𝑥𝑖 ↦→ 𝑡𝑛 ]] ⊢ predicate(𝑝) ▷ 𝜎 ′, R ′
for some 𝜎 ′ and R ′ such that 𝑉 ′ (𝑔(𝜎 ′ )) = true where 𝑉 ′ is the corresponding valuation extending
𝑉𝑛 .
    Then Σ ⇀ 𝜎 ′ [𝛾 = 𝛾 (𝜎)] ⊣ R 1 ∪ · · · ∪ R𝑛 ∪ R ′, ∅ by SGuardFold and 𝑉 ′ is the corresponding
valuation.
    Case 2(k). unfold 𝑝 (𝑒 1, · · · , 𝑒𝑛 ):
    Let 𝜎0 = 𝜎 and 𝑉0 = 𝑉 . For each 𝑒𝑖 , 𝜎𝑖 −1 ⊢ 𝑒 ⇓ 𝑡𝑖 ⊣ 𝜎𝑖 , R𝑖 by lemma 27 for some 𝜎𝑖 and R𝑖 such
that 𝑉𝑖 (𝑔(𝜎𝑖 )) = true where 𝑉𝑖 is the corresponding valuation.
    By lemma 45 𝜎𝑛 ⊢ 𝑝 (𝑒 1, · · · , 𝑒𝑛 ) ▷ 𝜎 ′, R ′ for some 𝜎 ′ and R ′ such that 𝑉 ′ (𝑔(𝜎 ′ )) = true where
  ′
𝑉 is the corresponding valuation extending 𝑉𝑛 .
    Then Σ ⇀ 𝜎 ′ ⊣ R 1 ∪ · · · ∪ R𝑛 ∪ R ′, ∅ by SGuardUnfold and 𝑉 ′ is the corresponding valuation.
                                                                                                            □

D.6    Preservation
Lemma 47. Suppose Γ = ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · S⟩ and Γ ′ = ⟨𝐻, ⟨𝛼 ′, 𝜌, 𝑠 ′ ⟩ · S⟩.
  If Γ is validated by Σ and 𝑉 , Π ⊢ _, Γ → Γ ′ with valuation 𝑉 ′ , and Π ⊢ Σ → Σ′ for some Σ′ such
that Σ′ corresponds to Γ ′ , 𝜙˜ (Σ′ ) = 𝜙˜ (Σ), and dom(𝛾 (Σ′ )) ⊇ dom(𝛾 (Σ)), then Γ ′ is a valid state.
Lemma 48. If ⟨𝐻, 𝛼 \ 𝑉 L⟨𝑡, 𝑓 , 𝑡 ′ ⟩M𝐻 , 𝜌⟩        𝑉
                                                        𝜎, ⟨𝑉 (𝑡), 𝑓 ⟩ ∈ 𝛼, and 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ ), then
⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 [H = H(𝜎); ⟨𝑡, 𝑓 , 𝑡 ′ ⟩].
Lemma 49. If ∀ ⟨ℓ, 𝑓 ⟩ ∈ T𝑒U ⟨𝐻, 𝛼 ⟩ : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣 then ⟨𝐻 ′, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣.
   Proof. By induction on the derivation of ⟨𝐻 ′, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣.
   Case 1. EvalLiteral – ⟨𝐻, 𝜌⟩ ⊢ 𝑙 ⇓ 𝑙: ⟨𝐻 ′, 𝜌⟩ ⊢ 𝑙 ⇓ 𝑙 by EvalLiteral.
   Case 2. EvalVar – ⟨𝐻, 𝜌⟩ ⊢ 𝑥 ⇓ 𝜌 (𝑥): ⟨𝐻 ′, 𝜌⟩ ⊢ 𝑥 ⇓ 𝜌 (𝑥) by EvalVar.
   Case 3. EvalAndA – ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 && 𝑒 2 ⇓ false:
   By inversion of EvalAndA ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ false. Then T𝑒 1 && 𝑒 2 U ⟨𝐻, 𝜌 ⟩ = T𝑒 1 U ⟨𝐻, 𝜌 ⟩ by definition.
Thus ∀ ⟨ℓ, 𝑓 ⟩ ∈ T𝑒 1 U ⟨𝐻, 𝛼 ⟩ : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ), and therefore ⟨𝐻 ′, 𝜌⟩ ⊢ 𝑒 1 ⇓ false by induction.
   Case 4. EvalAndB – ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 && 𝑒 2 ⇓ 𝑣 2 :
   By inversion of EvalAndB ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ true and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 2 ⇓ 𝑣 2 . Now T𝑒 1 && 𝑒 2 U ⟨𝐻, 𝜌 ⟩ =
T𝑒 1 U ⟨𝐻, 𝜌 ⟩ ∪ T𝑒 2 U ⟨𝐻, 𝜌 ⟩ .
   Thus ∀ ⟨ℓ, 𝑓 ⟩ ∈ T𝑒 1 U ⟨𝐻, 𝛼 ⟩ : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) since T𝑒 1 U ⟨𝐻, 𝜌 ⟩ ⊆ T𝑒 1 && 𝑒 2 U ⟨𝐻, 𝜌 ⟩ . Therefore
⟨𝐻 ′, 𝜌⟩ ⊢ 𝑒 1 ⇓ true by induction. Similarly, ⟨𝐻 ′, 𝜌⟩ ⊢ 𝑒 2 ⇓ 𝑣 2 .
   Therefore ⟨𝐻 ′, 𝜌⟩ ⊢ 𝑒 1 && 𝑒 2 ⇓ 𝑣 2 by EvalAndB.
   Case 5. EvalOrA – ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 || 𝑒 2 ⇓ true: Similar to case 3.
   Case 6. EvalOrB – ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑣 2 : Similar to case 4.
   Case 7. EvalOp – ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓ 𝑣 1 ⊕ 𝑣 2 :
   By inversion of EvalOp ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ 𝑣 1 and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 2 ⇓ 𝑣 2 . Now T𝑒 1 ⊕ 𝑒 2 U ⟨𝐻, 𝜌 ⟩ = T𝑒 1 U ⟨𝐻, 𝜌 ⟩ ∪
T𝑒 2 U ⟨𝐻, 𝜌 ⟩ .
   Thus ∀ ⟨ℓ, 𝑓 ⟩ ∈ T𝑒 1 U ⟨𝐻, 𝛼 ⟩ : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) since T𝑒 1 U ⟨𝐻, 𝜌 ⟩ ⊆ T𝑒 1 && 𝑒 2 U ⟨𝐻, 𝜌 ⟩ . Therefore
⟨𝐻 ′, 𝜌⟩ ⊢ 𝑒 1 ⇓ 𝑣 1 by induction. Similarly, ⟨𝐻 ′, 𝜌⟩ ⊢ 𝑒 2 ⇓ 𝑣 2 .
   Therefore ⟨𝐻 ′, 𝜌⟩ ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓ 𝑒 1 ⊕ 𝑒 2 by EvalOp.
   Case 8. EvalNeg – ⟨𝐻, 𝜌⟩ ⊢ ¬𝑣 ⇓:
   By inversion of EvalNeg ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣. Also, T! 𝑒U ⟨𝐻, 𝜌 ⟩ = T𝑒U ⟨𝐻, 𝜌 ⟩ by definition, thus ∀ ⟨ℓ, 𝑓 ⟩ ∈
T𝑒U ⟨𝐻, 𝛼 ⟩ : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ). Therefore ⟨𝐻 ′, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣 by induction.
Gradually Verifying Unfolding Expressions & Pure Functions                                                     79


  Therefore ⟨𝐻 ′, 𝜌⟩ ⊢ ! 𝑒 ⇓ ¬𝑣 by EvalNeg.
   Case 9. EvalField – ⟨𝐻, 𝜌⟩ ⊢ 𝑒.𝑓 ⇓ 𝐻 (ℓ, 𝑓 ):
   By inversion of EvalField ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ ℓ. Then T𝑒.𝑓 U ⟨𝐻, 𝜌 ⟩ = T𝑒U ⟨𝐻, 𝜌 ⟩ ; ⟨ℓ, 𝑓 ⟩.
  Thus ∀ ⟨ℓ, 𝑓 ⟩ ∈ T𝑒U ⟨𝐻, 𝛼 ⟩ : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) since T𝑒U ⟨𝐻, 𝜌 ⟩ ⊆ T𝑒.𝑓 U ⟨𝐻, 𝜌 ⟩ . Therefore ⟨𝐻 ′, 𝜌⟩ ⊢
𝑒 ⇓ ℓ by induction.
   Now ⟨𝐻 ′, 𝜌⟩ ⊢ 𝑒.𝑓 ⇓ 𝐻 ′ (ℓ, 𝑓 ). Also, since ⟨ℓ, 𝑓 ⟩ ∈ T𝑒.𝑓 U ⟨𝐻, 𝜌 ⟩ , 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ). Therefore
⟨𝐻 ′, 𝜌⟩ ⊢ 𝑒.𝑓 ⇓ 𝐻 (ℓ, 𝑓 ).

   Case 10. EvalUnfolding – By the induction hypothesis, ⟨𝐻 ′, 𝜌⟩ ⊢ 𝑒 0 ⇓ 𝑣, so by EvalUnfolding,
⟨𝐻 ′, 𝜌⟩ ⊢ unfolding 𝑝 (𝑒) in 𝑒 0 ⇓ 𝑣 as desired.
   Case 11. EvalFunction – By the induction hypothesis, ⟨𝐻 ′, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣 and ⟨𝐻 ′, 𝜌 ′ ⟩ ⊢ func_body(𝑓 ) ⇓
𝑣 , so by definition, ⟨𝐻 ′, 𝜌⟩ ⊢ 𝑓 (𝑒) ⇓ 𝑣 ′ .
 ′



                                                                                                                □

Lemma 50. If ∀ ⟨ℓ, 𝑓 ⟩ ∈ T𝑒U ⟨𝐻, 𝜌 ⟩ : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 then ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊢frm 𝑒.

    Proof. By induction on the derivation of ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊢frm 𝑒.
    Case 1. EFrameExpression – ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE 𝑒:
    By inversion of EFrameExpression ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒 and then ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊢frm 𝑒 by assumptions
and lemma 50. Therefore ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE 𝑒 by EFrameExpression.
    Case 2. EFrameConjunction – ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE 𝜙 1 ∗ 𝜙 2 :
    By inversion of EFrameConjunction ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE 𝜙 1 and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE 𝜙 2 . Also, T𝜙 1 ∗
𝜙 2 U ⟨𝐻, 𝜌 ⟩ = T𝜙 1 U ⟨𝐻, 𝜌 ⟩ ∪ T𝜙 2 U ⟨𝐻, 𝜌 ⟩ by definition.
    Now ∀ ⟨ℓ, 𝑓 ⟩ ∈ T𝜙 1 U ⟨𝐻, 𝜌 ⟩ : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) since T𝜙 1 U ⟨𝐻, 𝛼 ⟩ ⊆ T𝜙U
                                                                                     ˜ ⟨𝐻, 𝛼 ⟩ . Therefore
    ′                                                       ′
⟨𝐻 , 𝛼, 𝜌⟩ ⊢frmE 𝜙 1 by induction. Similarly, ⟨𝐻 , 𝛼, 𝜌⟩ ⊢frmE 𝜙 2 .
    Therefore ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊢frmE 𝜙 1 ∗ 𝜙 2 by EFrameConjunction.
    Case 3. EFramePredicate – ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE 𝑝 (𝑒):
    By inversion of EFramePredicate ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒, ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣, and ⟨𝐻, 𝛼, [𝑥 ↦→ 𝑣]⟩ ⊢frmE
predicate(𝑝), where 𝑥 = predicate_params(𝑝).
                                                               Ð
    Now T𝑝 (𝑒)U ⟨𝐻, 𝜌 ⟩ = Tpredicate(𝑝)U ⟨𝐻, [𝑥↦→𝑣 ] ⟩ ∪ T𝑒U ⟨𝐻, 𝜌 ⟩ .
    Then, for each 𝑒 and corresponding 𝑥, ∀ ⟨ℓ, 𝑓 ⟩ ∈ T𝑒U ⟨𝐻, 𝜌 ⟩ : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) since T𝑒U ⟨𝐻, 𝜌 ⟩ ⊆
T𝑝 (𝑒)U ⟨𝐻, 𝜌 ⟩ . Therefore ⟨𝐻 ′, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣 by lemma 49 and ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊢frm 𝑒 by 50.
    Also, ∀ ⟨ℓ, 𝑓 ⟩ ∈ Tpredicate(𝑝)U ⟨𝐻, [𝑥↦→𝑣 ] ⟩ : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ), thus by induction
⟨𝐻 ′, 𝛼, [𝑥 ↦→ 𝑣]⟩ ⊢frmE predicate(𝑝).
    Therefore ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊢frmE 𝑝 (𝑒) by EFramePredicate.
    Case 4. EFrameConditionalA – ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE if 𝑒 then 𝜙 1 else 𝜙 2 :
    By inversion of EFrameConditionalA ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ true, ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒, and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE 𝜙 1 .
    Now Tif 𝑒 then 𝜙 1 else 𝜙 2 U ⟨𝐻, 𝜌 ⟩ = T𝑒U ⟨𝐻, 𝜌 ⟩ ∪ T𝜙 1 U ⟨𝐻, 𝜌 ⟩ .
    Then ∀ ⟨ℓ, 𝑓 ⟩ ∈ T𝑒U ⟨𝐻, 𝜌 ⟩ : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) since T𝑒U ⟨𝐻, 𝜌 ⟩ ⊆ Tif 𝑒 then 𝜙 1 else 𝜙 2 U ⟨𝐻, 𝜌 ⟩ .
Therefore ⟨𝐻 ′, 𝜌⟩ ⊢ 𝑒 ⇓ true by lemma 49 and ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊢frm 𝑒 by lemma 50.
    Also, Then ∀ ⟨ℓ, 𝑓 ⟩ ∈ T𝜙 1 U ⟨𝐻, 𝜌 ⟩ : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) since
T𝜙 1 U ⟨𝐻, 𝜌 ⟩ ⊆ Tif 𝑒 then 𝜙 1 else 𝜙 2 U ⟨𝐻, 𝜌 ⟩ . Therefore ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊢frmE 𝜙 1 by induction.
    Therefore ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊢frmE if 𝑒 then 𝜙 1 else 𝜙 2 by EFrameConditionalA.
    Case 5. EFrameConditionalB – ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE if 𝑒 then 𝜙 1 else 𝜙 2 : Similar to case 4.
    Case 6. EFrameAcc – ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmE acc(𝑒.𝑓 ):
    By inversion of EFrameAcc ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒.
80                                                                                                    Torek et al.


  Also, T𝑒U ⟨𝐻, 𝜌 ⟩ ⊆ Tacc(𝑒.𝑓 )U ⟨𝐻, 𝜌 ⟩ by definition, thus ∀ ⟨ℓ, 𝑓 ⟩ ∈ T𝑒U ⟨𝐻, 𝜌 ⟩ : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ).
Therefore ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊢frm 𝑒 by lemma 50.
  Thus ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊢frmE acc(𝑒.𝑓 ) by EFrameAcc.

     Case 7. FrameUnfolding – By definition, ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmI 𝑝 (𝑒), ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝑝 (𝑒), and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm
𝑒 0 . By the induction hypothesis, ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊢frm 𝑒 0 . By IFramePredicate, ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒, so by
the induction hypothesis, ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊢frm 𝑒 and hence ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊢frmI 𝑝 (𝑒). By AssertPredicate,
⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣 and ⟨𝐻, 𝛼, [𝑥 ↦→ 𝑣]⟩ ⊨ predicate(𝑝) where 𝑥 = predicate_params(𝑝). By Lemma 50,
⟨𝐻 ′, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣. Then, since 𝑝 is a predicate, its body must be a specification so one of the following
cases applies.
     Case 7(a). predicate(𝑝) is precise and self-framing – by Lemma 52, ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊨ predicate(𝑝).
     Case 7(b). predicate(𝑝) = ? ∗ 𝜙 – By AssertImprecise, ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙 and ⟨𝐻, 𝛼, [𝑥 ↦→ 𝑣]⟩ ⊢frmE 𝜙.
By Lemma 52, ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊨ 𝜙, and by Lemma 51, ⟨𝐻 ′, 𝛼, [𝑥 ↦→ 𝑣]⟩ ⊢frmE 𝜙. By AssertImprecise,
⟨𝐻 ′, 𝛼, 𝜌⟩ ⊨ predicate(𝑝).
     In either case, ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊨ 𝑝 (𝑒) by AssertPredicate, so ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊢frm unfolding 𝑝 (𝑒) in 𝑒 0 as
desired.
     Case 8. FrameFunction – By definition, ⟨𝐻, 𝛼, 𝜌⟩ ⊢frmI func_pre(𝑓 ), ⟨𝐻, 𝛼, 𝜌⟩ ⊨ func_pre(𝑓 ),
and ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒. By the induction hypothesis, ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊢frm 𝑒 and ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊢frmI func_pre(𝑓 ).
By Lemma 52, ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊨ func_pre(𝑓 ), so ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊢frm 𝑓 (𝑒).

                                                                                                                 □
                          ˜ ⟨𝐻, 𝛼 ⟩
Lemma 51. If ∀ ⟨ℓ, 𝑓 ⟩ ∈ T𝜙U             : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) and ⟨𝐻, 𝛼, 𝜌⟩ ⊢
                                                                            frmE       𝜙˜ then ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊢
                                                                                                       frmE
˜
𝜙.
                                             ˜ ⟨𝐻, 𝜌 ⟩ : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) then ⟨𝐻 ′, 𝛼, 𝜌⟩ ⊨ 𝜙.
Lemma 52. If ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙˜ and ∀ ⟨ℓ, 𝑓 ⟩ ∈ T𝜙U                                                     ˜

Lemma 53. If ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙˜ for some specification 𝜙˜ and ∀ ⟨ℓ, 𝑓 ⟩ ∈ 𝛼 : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) then
⟨𝐻 ′, 𝛼, 𝜌⟩ ⊨ 𝜙.
              ˜

Lemma 54. If ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 and ∀ ⟨ℓ, 𝑓 ⟩ ∈ 𝛼 : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) then ⟨𝐻 ′, 𝛼, 𝜌⟩ 𝑉 𝜎.
     Proof. From the assumptions, clearly 𝜌 𝑉 𝛾 (𝜎). It suffices to show that ⟨𝐻 ′, 𝛼⟩ 𝑉 H(𝜎) and
⟨𝐻 ′, 𝛼⟩ 𝑉 H (𝜎).
     Let H = H(𝜎). From assumptions, clearly ⟨𝐻, 𝛼⟩ 𝑉 H. Therefore
                                   ∀ ⟨𝑓 , 𝑡, 𝑡 ′ ⟩ ∈ H : 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ )                              (18)
                                                  ′
                                       ∀ ⟨𝑓 , 𝑡, 𝑡 ⟩ ∈ H : ⟨𝑉 (𝑡), 𝑓 ⟩ ∈ 𝛼                                     (19)
                            ∀ ⟨𝑝, 𝑡⟩ ∈ H : ⟨𝐻, 𝛼, [𝑥 ↦→ 𝑉 (𝑡)]⟩ ⊨ predicate(𝑝)                                 (20)
                            ∀ ℎ 1, ℎ 2 ∈ H2 : ℎ 1 ≠ ℎ 2 =⇒ 𝑉 Lℎ 1 M𝐻 ∩ 𝑉 Lℎ 2 M𝐻 = ∅                           (21)
     Let ⟨𝑓 , 𝑡, 𝑡 ′ ⟩ be an arbitrary field value in H. Then by (18) 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ ). Also, by (19)
⟨𝑉 (𝑡), 𝑓 ⟩ ∈ 𝛼, thus by our initial assumptions 𝐻 ′ (𝑉 (𝑡), 𝑓 ) = 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ ). Therefore
                                   ∀ ⟨𝑓 , 𝑡, 𝑡 ′ ⟩ ∈ H : 𝐻 ′ (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ ).                           (22)
  let ⟨𝑝, 𝑡⟩ be an arbitrary predicate instance in H. Then by (20) ⟨𝐻, 𝛼, [𝑥 ↦→ 𝑉 (𝑡)]⟩ ⊨ predicate(𝑝).
Since predicate(𝑝) is a specification, and ∀ ⟨ℓ, 𝑓 ⟩ ∈ 𝛼 : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ), then
⟨𝐻 ′, 𝛼, [𝑥 ↦→ 𝑉 ′ (𝑡)]⟩ ⊨ predicate(𝑝) by lemma 53. Therefore
                           ∀ ⟨𝑝, 𝑡⟩ ∈ H : ⟨𝐻 ′, 𝛼, [𝑥 ↦→ 𝑉 ′ (𝑡)]⟩ ⊨ predicate(𝑝).                             (23)
Gradually Verifying Unfolding Expressions & Pure Functions                                             81


  Therefore by (22), (19), (23), and (21), ⟨𝐻 ′, 𝛼⟩ 𝑉 H.

  Let H = H (𝜎) and let ⟨𝑓 , 𝑡, 𝑡 ′ ⟩ ∈ H be an arbitrary field chunk. Then, 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ ) and
⟨𝑉 (𝑡), 𝑓 ⟩ ∈ 𝛼 by definition of heap correspondence. By the assumptions, 𝐻 ′ (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡), so

                                  ∀⟨𝑓 , 𝑡, 𝑡 ′ ⟩ ∈ H : 𝐻 ′ (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ ),
                                     ∀⟨𝑓 , 𝑡, 𝑡 ′ ⟩ ∈ H : ⟨𝑉 (𝑡), 𝑓 ⟩ ∈ 𝛼 .
  Then, let ⟨𝑝, 𝑡⟩ be an arbitrary predicate chunk in H . Then, by definition of heap correspondence,
⟨𝐻, 𝛼, [𝑥 ↦→ 𝑉 ′ (𝑡)]⟩ ⊨ predicate(𝑝). Then, since predicate(𝑝) is a specification and 𝐻 ′ coincides
with 𝐻 , ⟨𝐻 ′, 𝛼, [𝑥 ↦→ 𝑉 ′ (𝑡)]⟩ ⊨ predicate(𝑝) by Lemma 55.

                                                                                                       □
Lemma 55. If ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · S⟩ is a well-formed state, the partial state ⟨𝐻, S⟩ is validated by
Σ and 𝑉 , and 𝐻 ′ = 𝐻 [⟨ℓ, 𝑓 ⟩ ↦→ 𝑣] for some ℓ, 𝑓 , and 𝑣 such that ⟨ℓ, 𝑓 ⟩ ∈ 𝛼 or ℓ is a fresh value
unused in S, then the partial state ⟨𝐻 ′, S⟩ is validated by Σ and 𝑉 .
                                          ˜ 𝐻 ⊆ 𝛼.
Lemma 56. If ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 then 𝑉 Lrem(𝜎, 𝜙)M
                                                         ˜ 𝐻 and 𝛼 ′ = ⌊𝜙⌋
Lemma 57. Let 𝜙˜ be some specification, 𝛼ˆ = 𝑉 Lrem(𝜎, 𝜙)M                ˜ ⟨𝐻, 𝛼\𝛼,ˆ 𝜌 ⟩ .
              ˜ ⟨𝐻, 𝜌 ⟩ , 𝜌⟩
  If ⟨𝐻, 𝛼 \ T𝜙U               𝜎 and ⟨𝐻, 𝛼 \ 𝛼,
                                             ˆ 𝜌⟩ ⊨ 𝜙,              ′
                                                    ˜ then ⟨𝐻, 𝛼 \ 𝛼 , 𝜌⟩     𝜎.
                             𝑉                                             𝑉
Lemma 58. Let ⟨𝐻, S⟩ be some dynamic state validated by Σ and valuation 𝑉 for some program
Π. If Σ ⇀ 𝜎 ′ ⊣ R, Θ with 𝑉 ′ = 𝑉 [Σ ⇀ 𝜎 ′ ⊣ R, Θ | 𝐻 ], 𝑉 ′ (𝑔(𝜎 ′ )) = true, ⟨𝐻, 𝛼 (S)⟩ ⊢𝑉 ′ R, and
⟨𝐻, S⟩, 𝑉 ′ LΘM𝐻 → ⟨𝐻 ′, S ′ ⟩ then Γ ′ = ⟨𝐻 ′, S ′ ⟩ is a valid state.
   Note: This is a simplification of theorem 3, restricted to the particular case of a normal program
step (in contrast to a step from init or to final).
  Proof. We proceed by cases on ⟨𝐻, S⟩, 𝑉 ′ LΘM𝐻 → ⟨𝐻 ′, S ′ ⟩.
  Case 1. ExecSeq: We have
                    ⟨𝐻, ⟨𝛼, 𝜌, skip; 𝑠⟩ · S ∗ ⟩, 𝑉 ′ LΘM𝐻 → ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · S ∗ ⟩.
  Since the initial state is validated by Σ and 𝑉 , Σ = ⟨𝜎, skip; 𝑠, 𝜙⟩     ˜ for some 𝜎, 𝜙,
                                                                                          ˜ where
⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎.
   Now 𝜎 (Σ) ⊢ skip; 𝑠 → 𝑠 ⊣ 𝜎 by SExecSeq. Therefore Π ⊢ Σ → Σ′ by SVerifyStep where
Σ = ⟨𝜎, 𝑠, 𝜙⟩.
 ′          ˜
   Now, by lemma 47, it suffices to show that Σ′ corresponds to ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · S ∗ ⟩ (with valuation
𝑉 ).
   Since 𝜎 (Σ′ ) = 𝜎, we have ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎 (Σ′ ), and 𝑠 (Σ′ ) = 𝑠 by definition. Therefore Σ′ corre-
sponds to ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · S ∗ ⟩, which completes the proof.
   Case 2. ExecAssign: We have
                   ⟨𝐻, ⟨𝛼, 𝜌, 𝑥 = 𝑒; 𝑠⟩ · S ∗ ⟩, 𝑉 ′ LΘM𝐻 → ⟨𝐻, ⟨𝛼, 𝜌 [𝑥 ↦→ 𝑣], 𝑠⟩ · S ∗ ⟩
                                            where     ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣
  Since the initial state is validated by Σ, Σ = ⟨𝜎, 𝑥 = 𝑒; 𝑠, 𝜙⟩
                                                               ˜ for some 𝜎, 𝜙˜ where ⟨𝐻, 𝛼, 𝜌⟩
                                                                                                𝑉
                                                                                                  𝜎.
  The only guard that applies is SGuardAssign, so we have, for some 𝜎 ′, 𝑡:
                                                    ˜ ⇀ 𝜎 ⊣ R, Θ
                                      ⟨𝜎, 𝑥 = 𝑒; 𝑠, 𝜙⟩
                     where 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R       and (by assumptions) ⟨𝐻, 𝜌⟩ ⊢𝑉 ′ R.
82                                                                                                               Torek et al.


where 𝑉 ′ is the corresponding valuation, extending 𝑉 .
  Let 𝜎 ′′ = 𝜎 [𝛾 = 𝛾 (𝜎) [𝑥 ↦→ 𝑡]], then 𝜎 ⊢ 𝑥 = 𝑒; 𝑠 → 𝑠 ⊣ 𝜎 ′′ by SExecAssign.
  Let Σ′ = ⟨𝜎 ′′, 𝑠, 𝜙⟩.
                     ˜ Then Π ⊢ Σ → Σ′ by SVerifyStep, thus Σ′ is reachable from Π.
 We want to show that ⟨𝐻, ⟨𝛼, 𝜌 [𝑥 ↦→ 𝑣], 𝑠⟩ · S ∗ ⟩ is validated by Σ′ with valuation 𝑉 ′ .
  Part 34.1: As shown above, Σ′ is reachable from Π with valuation 𝑉 ′ .
  Part 34.2: By lemma 26 ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡), therefore 𝑉 ′ (𝑡) = 𝑣. Also, 𝜌 𝑉 𝛾 (𝜎), thus 𝜌 [𝑥 ↦→
𝑣] 𝑉 ′ 𝛾 (𝜎) [𝑥 ↦→ 𝑉 ′ (𝑡)]. Rewriting using definitions, we get 𝜌 [𝑥 ↦→ 𝑣] 𝑉 ′ 𝛾 (𝜎 ′′ ).
     Also by lemma 26, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ . Thus, since 𝛾 is the only component changed from 𝜎 ′ to 𝜎 ′′
and 𝜌 [𝑥 ↦→ 𝑣] 𝑉 ′ 𝛾 (𝜎 ′′ ), ⟨𝐻, 𝛼, 𝜌 [𝑥 ↦→ 𝑣]⟩ 𝑉 ′ 𝜎 ′′ .
  Also, by definition Σ′ = ⟨𝜎 ′′, 𝑠, 𝜙⟩.˜
  Therefore Σ corresponds to ⟨𝐻, ⟨𝛼, 𝜌 [𝑥 ↦→ 𝑣], 𝑠⟩ · S ∗ ⟩.
                 ′

  Part 34.3: Since the initial state is validated by Σ and 𝑉 , the partial state ⟨𝐻, S ∗ ⟩ is validated by
Σ and valuation 𝑉 . Therefore one of 33.1, 33.2, 33.3 applies. We want to show that the partial state
⟨𝐻, S ∗ ⟩ is validated by Σ′ and valuation 𝑉 ′ .
 • Case 33.1: Then S ∗ = nil and trivially ⟨𝐻, nil⟩ is validated by Σ′ and valuation 𝑉 ′ .
 • Case 33.2: Then S ∗ = ⟨𝜌 0, 𝛼 0, 𝑦 = 𝑚(𝑒 1, · · · , 𝑒𝑘 ); 𝑠 0 ⟩ · S0 for some 𝜌 0 , 𝛼 0 , 𝑦, 𝑚, 𝑘, 𝑒 1, · · · , 𝑒𝑘 , 𝑠 0 ,
   S0 . Also, there is some Σ0 , 𝑉0 , 𝑥 1, · · · , 𝑥𝑘 , 𝑡 1, · · · , 𝑡𝑘 and 𝜎0, · · · , 𝜎𝑘 , 𝜎 ′ such that

                             The partial state ⟨𝐻, S0 ⟩ is validated by Σ0 and 𝑉0,
                         Σ0 is reachable from Π with valuation 𝑉0,               𝑠 (Σ0 ) = 𝑠 (S ∗ )
                                              𝑥 1, · · · , 𝑥𝑘 = params(𝑚),
                    𝜎0 = 𝜎 (Σ0 ),     𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, _,      ··· ,   𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,
                        𝜎𝑘 ⊢ pre(𝑚) ▷ 𝜎 ′, _,         ⟨𝐻, 𝛼 0, 𝜌 0 ⟩ 𝑉 𝜎 ′ [𝛾 = 𝛾 (𝜎0 )],      and
                                                                       0

                                        ∀ 1 ≤ 𝑖 ≤ 𝑘 : 𝑉 (𝛾 (Σ)(𝑥𝑖 )) = 𝑉0 (𝑡𝑖 ),
                                                 𝜙˜ (Σ) = post(𝑚).

     We want to show that the partial state ⟨𝐻, ⟨𝜌 0, 𝛼 0, 𝑦 = 𝑚(𝑒 1, · · · , 𝑒𝑘 ); 𝑠⟩ · S0 ⟩ is validated by Σ′
     and valuation 𝑉 ′ . Immediately from above we can conclude that

                             The partial state ⟨𝐻, S0 ⟩ is validated by Σ0 and 𝑉0,
                         Σ0 is reachable from Π with valuation 𝑉0,               𝑠 (Σ0 ) = 𝑠 (S ∗ )
                                              𝑥 1, · · · , 𝑥𝑘 = params(𝑚),
                𝜎0 = 𝜎 (Σ0 ),     𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, _,     ··· ,    𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,       and
                            𝜎𝑘 ⊢ pre(𝑚) ▷ 𝜎 ′, _,         ⟨𝐻, 𝛼 0, 𝜌 0 ⟩ 𝑉 𝜎 ′ [𝛾 = 𝛾 (𝜎0 )].
                                                                           0


      Also, the frame ⟨𝛼, 𝜌, 𝑥 = 𝑒; 𝑠⟩ must be executing the body of 𝑚, since it is in the stack
      immediately above the frame that contains 𝑦 = 𝑚(𝑒 1, · · · , 𝑒𝑘 ). Therefore, since 𝑥 1, · · · , 𝑥𝑘 are all
      parameters of 𝑚, 𝑦 must be distinct from all of 𝑥 1, · · · , 𝑥𝑘 , since we do not allow assignment to
      parameters in a well-formed program. Thus

                  ∀1 ≤ 𝑖 ≤ 𝑘 : 𝑉 ′ (𝛾 (Σ′ ) (𝑥𝑖 )) = 𝑉 ′ ((𝛾 (𝜎) [𝑥 ↦→ 𝑡]) (𝑥𝑖 )) = 𝑉 ′ (𝛾 (𝜎) (𝑥𝑖 ))
                                                     = 𝑉 ′ (𝛾 (Σ)(𝑥𝑖 )) = 𝑉 (𝛾 (Σ) (𝑥𝑖 ))
                                                     = 𝑉0 (𝑡𝑖 ).
Gradually Verifying Unfolding Expressions & Pure Functions                                                              83


    Finally, 𝜙˜ (Σ′ ) = 𝜙˜ (Σ) by definition, thus
                                             𝜙˜ (Σ′ ) = 𝜙˜ (Σ) = post(𝑚).
   Therefore the partial state ⟨𝐻, S ∗ ⟩ is validated by Σ′ and 𝑉 ′ in this case.
 • Case 33.3: Then S ∗ = ⟨𝜌 0, 𝛼 0, while 𝑒 0 invariant 𝜙˜0 do 𝑠 0 ; 𝑠 0′ ⟩ · S0 for some 𝜌 0 , 𝛼 0 , 𝑒, 𝜙˜0 , 𝑠 0 , 𝑠 0′ ,
   S0 , and there exists some Σ0 , 𝑉0 , and 𝜎0′ such that:
                             The partial state ⟨𝐻, S0 ⟩ is validated by Σ0 and 𝑉0
                         Σ0 is reachable from Π with valuation 𝑉0                      𝑠 (Σ0 ) = 𝑠 (S ∗ )
                                  𝜎0 ⊢ 𝜙˜0 ▷ 𝜎0′ , _,      ⟨𝐻, 𝛼 0, 𝜌 0 ⟩ 𝑉 𝜎0′              and
                                                                             0

                                                        𝜙˜ (Σ) = 𝜙˜0 .
    Now, by definition of Σ′′ , 𝜙˜ (Σ′ ) = 𝜙˜ (Σ) = 𝜙˜0 . Therefore, using the other assumptions given
    above, the partial state ⟨𝐻, S ∗ ⟩ is validated by Σ′ and 𝑉 ′ in this case.
   Therefore definition part 34.3 is satisfied.
   Therefore all parts of definition 34 are satisfied. Thus ⟨𝐻, ⟨𝛼, 𝜌 [𝑥 ↦→ 𝑣], 𝑠⟩ · S ∗ ⟩ is validated by
Σ with valuation 𝑉 ′ .
 ′

   Case 3. ExecAssignField:
   We have
                    ⟨𝐻, ⟨𝛼, 𝜌, 𝑥 .𝑓 = 𝑒; 𝑠⟩ · S ∗ ⟩, 𝑉 ′ LΘM𝐻 → ⟨𝐻 ′, ⟨𝛼, 𝜌, 𝑠⟩ · S ∗ ⟩                               (24)
                    where      ⟨𝐻, 𝜌⟩ ⊢ 𝑥 ⇓ ℓ,       ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣,             ⟨𝐻, 𝛼, 𝜌⟩ ⊨ acc(𝑥 .𝑓 ),              (25)
                                                                   ′
                               ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒,        and 𝐻 = 𝐻 [⟨ℓ, 𝑓 ⟩ ↦→ 𝑣].                                     (26)

Since the initial state is validated by Σ, Σ = ⟨𝜎, 𝑥 .𝑓 = 𝑒; 𝑠, 𝜙⟩
                                                                ˜ for some 𝜎, 𝜙˜ where ⟨𝐻, 𝛼, 𝜌⟩
                                                                                                 𝑉
                                                                                                   𝜎.
  The only guard rule that applies is SGuardAssign, so we have
                                     ˜ ⇀ 𝜎 ⊣ R ′ ∪ R ′′, ∅
                    ⟨𝜎, 𝑥 .𝑓 = 𝑒; 𝑠, 𝜙⟩                                                                               (27)
                    where 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R ′,           𝜎 ′ ⊢ acc(𝑥 .𝑓 ) ▷ 𝜎 ′′, R ′′                               (28)
                                                                       ′    ′′           ′         ′′
                    and (by assumptions)          ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R ∪ R ,                  𝑉 (𝑔(𝜎 )) = true               (29)
  Furthermore, since 𝑔(𝜎 ′′ ) =⇒ 𝜎 ′ by lemma 34, and by lemma 23,
                       𝑉 ′ (𝑔(𝜎 ′ )) = true,      ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R ′,         and         ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R ′′ .
  Now, by SExecAssignField,
                   𝜎 ⊢ 𝑥 .𝑓 = 𝑒; 𝑠 → 𝑠 ⊣ 𝜎 ′′′        where 𝜎 ′′′ = 𝜎 ′′ [H = H′ ],                     and
                                                                       ′          ′′           ′′
                                                                   H = H(𝜎 ); ⟨𝛾 (𝜎 ) (𝑥), 𝑓 , 𝑡⟩.
    Let Σ′ = ⟨𝜎 ′′′, 𝑠, 𝜙⟩.
                        ˜ We want to show that ⟨𝐻 ′, ⟨𝛼, 𝜌, 𝑠⟩ · S ∗ ⟩ is validated by Σ′ and 𝑉 ′ .
    Part 34.1: By SVerifyStep, Π ⊢ Σ → Σ′ . Therefore Σ′ is reachable from program Π with valuation
  ′
𝑉 .
    Part 34.2: We want to show that Σ′ corresponds to ⟨𝐻 ′, ⟨𝛼, 𝜌, 𝑠⟩ · S ∗ ⟩. Since Σ′ = ⟨𝜎 ′′′, 𝑠, _⟩ by
construction, it suffices to show that ⟨𝐻 ′, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′′′ .
  By lemma 26, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ . By lemma 43, ⟨𝐻, 𝛼 \ Tacc(𝑥 .𝑓 )U ⟨𝐻, 𝜌 ⟩ , 𝜌⟩ 𝑉 ′ 𝜎 ′′ .
  Since 𝜌 𝑉 𝛾 (𝜎), 𝜌 (𝑥) = 𝑉 (𝛾 (𝜎) (𝑥)) = 𝑉 ′ (𝛾 (𝜎) (𝑥)). Also, ⟨𝐻, 𝜌⟩ ⊢ 𝑥 ⇓ 𝜌 (𝑥) by EvalVar and
⟨𝐻, 𝜌⟩ ⊢ 𝑥 ⇓ ℓ by (25), thus
                                     𝑉 ′ (𝛾 (𝜎) (𝑥)) = 𝜌 (𝑥) = ℓ.
84                                                                                                         Torek et al.


Also, 𝛾 (𝜎 ′′ ) = 𝛾 (𝜎) by lemmas 25 and 37. Thus ⟨𝐻, 𝜌⟩ ⊢ 𝑥 ⇓ 𝑉 ′ (𝛾 (𝜎 ′′ ) (𝑥)). Therefore
Tacc(𝑥 .𝑓 )U ⟨𝐻, 𝜌 ⟩ = {⟨ℓ, 𝑓 ⟩} = {⟨𝑉 ′ (𝛾 (𝜎 ′′ ) (𝑥)), 𝑓 ⟩} = 𝑉 ′ L⟨𝛾 (𝜎 ′′ ) (𝑥), 𝑓 , 𝑡 ′ ⟩M𝐻 . Now,

                                 ⟨𝐻, 𝛼 \ 𝑉 ′ L⟨𝛾 (𝜎 ′′ ) (𝑥), 𝑓 , 𝑡 ′ ⟩M𝐻 , 𝜌⟩ 𝑉 ′ 𝜎 ′′ .
  Also, 𝑣 = 𝑉 ′ (𝑡) by lemma 26, thus 𝐻 ′ (𝑉 ′ (𝛾 (𝜎 ′′ ) (𝑥)), 𝑓 ) = 𝐻 ′ (ℓ, 𝑓 ) = 𝑣 = 𝑉 ′ (𝑡). Now by lemma
48,
                                         ⟨𝐻 ′, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′′′
which is sufficient to show that Σ′ corresponds to ⟨𝐻 ′, ⟨𝛼, 𝜌, 𝑠⟩ · S ∗ ⟩.
  Part 34.3:
  By (25) ⟨𝐻, 𝛼, 𝜌⟩ ⊨ acc(𝑥 .𝑓 ). This assertion must be given by AssertAcc, therefore ⟨ℓ, 𝑓 ⟩ ∈ 𝛼.
  Now we show by induction that all partial states are validated, in other words we want to show
that the partial state ⟨𝐻 ′, S ∗ ⟩ is validated by Σ′ . By assumptions, ⟨𝐻, S ∗ ⟩ is validated by Σ with
valuation 𝑉 . Also, by lemma 55, ⟨𝐻 ′, S ∗ ⟩ is validated by Σ with 𝑉 .
  Thus, one of the following cases apply:
 • Case 33.1: Then S ∗ = nil, and trivially ⟨𝐻 ′, nil⟩ is validated by Σ′ and 𝑉 .
 • Case 33.2: Then S ∗ = ⟨𝜌, 𝛼, 𝑦 = 𝑚(𝑒 1, · · · , 𝑒𝑘 ); 𝑠⟩ · S0 for some 𝜌, 𝛼, 𝑦, 𝑚, 𝑒 1, · · · , 𝑒𝑘 , and there
   exists some Σ0 , 𝑉0 , 𝑥 1, · · · , 𝑥𝑘 , 𝑡 1, · · · , 𝑡𝑘 , 𝜎0, · · · , 𝜎𝑘 , and 𝜎0′ such that:
                            The partial state ⟨𝐻 ′, S0 ⟩ is validated by Σ0 and 𝑉0,
                        Σ0 is reachable from Π with valuation 𝑉0,               𝑠 (Σ0 ) = 𝑠 (S ∗ )
                                            𝑥 1, · · · , 𝑥𝑘 = params(𝑚),
                    𝜎0 = 𝜎 (Σ0 ),    𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, _,     ··· ,     𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,
                                      ∀ 1 ≤ 𝑖 ≤ 𝑘 : 𝑉 (𝛾 (Σ)(𝑥𝑖 )) = 𝑉0 (𝑡𝑖 ),
                             𝜎𝑘 [𝛾 = [𝑥 1 ↦→ 𝑡 1, · · · , 𝑥𝑘 ↦→ 𝑡𝑘 ]] ⊢ pre(𝑚) ▷ 𝜎0′ , _,
                                      ⟨𝐻 ′, 𝛼, 𝜌⟩ 𝑉 𝜎0′ [𝛾 = 𝛾 (𝜎0 )],         and
                                                      0

                                                 𝜙˜ (Σ) = post(𝑚).
     We want to show that the partial state ⟨𝐻 ′, ⟨𝜌, 𝛼, 𝑦 = 𝑚(𝑒 1, · · · , 𝑒𝑘 ); 𝑠⟩ · S0 ⟩ is validated by Σ′ .
     From above,
                            The partial state ⟨𝐻 ′, S0 ⟩ is validated by Σ0 and 𝑉0,
                        Σ0 is reachable from Π with valuation 𝑉0,               𝑠 (Σ0 ) = 𝑠 (S ∗ )
                                            𝑥 1, · · · , 𝑥𝑘 = params(𝑚),
                    𝜎0 = 𝜎 (Σ0 ),    𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, _,     ··· ,     𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,
                         𝜎𝑘 [𝛾 = [𝑥 1 ↦→ 𝑡 1, · · · , 𝑥𝑘 ↦→ 𝑡𝑘 ]] ⊢ pre(𝑚) ▷ 𝜎0′ , _,       and
                                          ⟨𝐻 ′, 𝛼, 𝜌⟩ 𝑉 𝜎0′ [𝛾 = 𝛾 (𝜎0 )].
                                                          0

     𝛾 (Σ′ ) = 𝛾 (𝜎 ′′′ ) = 𝛾 (𝜎 ′′ ) by definition. Also, 𝛾 (𝜎 ′′ ) = 𝛾 (𝜎 ′ ) = 𝛾 (𝜎 ′ ) by lemmas 25 and 37. Also,
     𝑉 ′ extends 𝑉 . Thus
                            ∀ 1 ≤ 𝑖 ≤ 𝑘 : 𝑉 ′ (𝛾 (Σ′ ) (𝑥𝑖 )) = 𝑉 (𝛾 (Σ) (𝑥𝑖 )) = 𝑉0 (𝑡𝑖 ).
     Also, by definition
                                            𝜙˜ (Σ′ ) = 𝜙˜ (Σ) = post(𝑚).
     Therefore the partial state ⟨𝐻 ′, S ∗ ⟩ is validated by Σ′ .
Gradually Verifying Unfolding Expressions & Pure Functions                                                              85


 • Case 33.3: Then S ∗ = ⟨𝜌, 𝛼, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ ⟩ · S0 for some 𝜌, 𝛼, 𝑒, 𝜙,
                                                                                        ˜ 𝑠, 𝑠 ′ , and S0 ,
   and there exists some Σ0 , 𝑉0 , and 𝜎0 such that:
                                        ′

                               The partial state ⟨𝐻 ′, S0 ⟩ is validated by Σ and 𝑉
                          Σ0 is reachable from Π with valuation 𝑉0                      𝑠 (Σ0 ) = 𝑠 (S ∗ )
                                    𝜎 (Σ0 ) ⊢ 𝜙˜ ▷ 𝜎0′ , _,       and      ⟨𝐻 ′, 𝛼, 𝜌⟩ 𝑉 𝜎0′
                                                                                            0

                                                            𝜙˜ (Σ) = 𝜙˜
                                                         ˜ Therefore the partial state ⟨𝐻 ′, S ∗ ⟩ is
   Now, 𝜙˜ (Σ′ ) = 𝜙˜ (Σ) by definition, thus 𝜙˜ (Σ′ ) = 𝜙.
   validated by Σ .
                  ′

Now we have shown that Σ′ corresponds to the resulting state, and therefore 𝛾 ′ is validated by Σ′ .
  Case 4. ExecAlloc: We have
              ⟨𝐻, ⟨𝛼, 𝜌, 𝑥 = alloc(𝑆); 𝑠⟩ · S ∗ ⟩, 𝑉 ′ LΘM𝐻 → ⟨𝐻 ′, ⟨𝛼 ′, 𝜌 [𝑥 ↦→ ℓ], 𝑠⟩ · S ∗ ⟩
              where 𝑇 𝑓 = struct(𝑆),                 ℓ = fresh,        𝐻 ′ = 𝐻 [⟨ℓ, 𝑓 ⟩ ↦→ default(𝑇 )],
                          𝛼 ′ = 𝛼 ∪ {⟨ℓ, 𝑓 ⟩}
     Since the initial state is validated by Σ, Σ = ⟨𝜎, 𝑥 = alloc; 𝑠, 𝜙⟩
                                                                      ˜ for some 𝜎, 𝜙˜ where ⟨𝐻, 𝛼, 𝜌⟩
                                                                                                       𝑉
𝜎.
     By SExecAlloc
                𝜎 ⊢ 𝑥 = alloc(𝑆); 𝑠 → 𝑠 ⊣ 𝜎 ′, where H(𝜎 ′ ) = H(𝜎); ⟨𝑡, 𝑓 , default(𝑇 )⟩,
                                                                       𝛾 (𝜎 ′ ) = 𝛾 (𝜎) [𝑥 ↦→ 𝑡],         and
                                                                       𝑡 = fresh .
Let Σ′ = ⟨𝜎 ′, 𝑠, 𝜙⟩,
                  ˜ and 𝑉 ′ = 𝑉 [𝑡 ↦→ ℓ]. We want to show that ⟨𝐻 ′, ⟨𝛼 ′, 𝜌 [𝑥 ↦→ ℓ], 𝑠⟩ · S ∗ ⟩ is
validated by Σ′ with 𝑉 .
   Part 34.1: By SVerifyStep, Π ⊢ Σ → Σ′ , and all fresh values added to Σ′ are defined in 𝑉 ′ .
Therefore, Σ′ is reachable from Π with valuation 𝑉 ′ .
   Part 34.2: We want to show that Σ′ corresponds to 𝐻 ′ ⟨𝛼 ′, 𝜌 [𝑥 ↦→ ℓ], 𝑠⟩ · S ∗ . By definition 𝑠 (Σ′ ) =
𝑠 and 𝜎 (Σ′ ) = 𝜎 ′ , thus it suffices to show ⟨𝐻 ′, 𝛼 ′, 𝜌 [𝑥 ↦→ ℓ]⟩ 𝑉 ′ 𝜎 ′ .
     By assumptions, 𝜌 𝑉 𝛾 (𝜎). Also,
                 𝑉 ′ (𝛾 (𝜎 ′ ) (𝑥)) = 𝑉 ′ ((𝛾 (𝜎) [𝑥 ↦→ 𝑡]) (𝑥)) = 𝑉 ′ (𝑡) = ℓ = (𝜌 [𝑥 ↦→ ℓ]) (𝑥).
Therefore
                                               𝜌 [𝑥 ↦→ ℓ] 𝑉 ′ 𝛾 (𝜎) [𝑥 ↦→ 𝑡].
  By assumptions, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎. Since 𝑉 ⊆ 𝑉 ′ , ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎. Since ℓ is a fresh value, ℓ ∉ 𝛼.
Thus
                              ∀ ⟨ℓ, 𝑓 ⟩ ∈ 𝛼 : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ).
Thus by lemma 48, ⟨𝐻 ′, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎. Also, since 𝛼 ⊆ 𝛼 ′ , by lemma 19 ⟨𝐻 ′, 𝛼 ′, 𝜌⟩ 𝑉 ′ 𝜎.
    Let ⟨𝑓 ′, 𝑡 ′, 𝑡 ′′ ⟩ ∈ H(𝜎 ′ ). If ⟨𝑓 ′, 𝑡 ′, 𝑡 ′′ ⟩ ∈ H(𝜎), then since ⟨𝐻 ′, 𝛼 ′, 𝜌⟩ 𝑉 ′ 𝜎, 𝐻 ′ (𝑉 ′ (𝑡 ′ ), 𝑓 ′ ) =
𝑉 ′ (𝑡 ′′ ) and ⟨𝑉 ′ (𝑡 ′ ), 𝑓 ′ ⟩ ∈ 𝛼 ′ .
    Otherwise, 𝑡 ′ = 𝑡 and 𝑓 ′ = 𝑓 for some 𝑇 𝑓 ∈ struct(𝑆), and thus 𝑡 ′′ = default(𝑇 ). Now
𝐻 (𝑉 ′ (𝑡 ′ ), 𝑓 ′ ) = 𝐻 ′ (𝑉 ′ (𝑡), 𝑓 ) = 𝐻 ′ (ℓ, 𝑓 ) = default(𝑇 ) = 𝑡 ′′ .
    Therefore
                  ∀ ⟨𝑓 ′, 𝑡 ′, 𝑡 ′′ ⟩ ∈ H(𝜎 ′ ) : 𝐻 ′ (𝑉 ′ (𝑡 ′ ), 𝑓 ′ ) = 𝑉 ′ (𝑡 ′′ ) and ⟨𝑉 ′ (𝑡 ′ ), 𝑓 ′ ⟩ ∈ 𝛼 ′ .
86                                                                                                              Torek et al.


     Also, since ⟨𝐻 ′, 𝛼 ′, 𝜌⟩ 𝑉 ′ 𝜎 and ∀ ⟨𝑝, 𝑡⟩ ∈ H(𝜎 ′ ) : ⟨𝑝, 𝑡⟩ ∈ H(𝜎),

                           ∀ ⟨𝑝, 𝑡⟩ ∈ H(𝜎 ′ ) : ⟨𝐻 ′, 𝛼 ′, [𝑥 ↦→ 𝑉 (𝑡)]⟩ ⊨ predicate(𝑝)

where 𝑥 = predicate_params(𝑝).
   Let ℎ 1, ℎ 2 ∈ H(𝜎 ′ ) and suppose ℎ 1 ≠ ℎ 2 . If ℎ 1 ∈ H(𝜎) and ℎ 2 ∈ H(𝜎), then in this case
𝑉 Lℎ 1 M𝐻 ′ ∩ 𝑉 ′ Lℎ 2 M𝐻 ′ = ∅ since ⟨𝐻 ′, 𝛼 ′, 𝜌⟩ 𝑉 ′ 𝜎.
 ′

   Otherwise, WLOG ℎ 1 = ⟨𝑡, 𝑓1, default(𝑇1 )⟩ for some 𝑇1 𝑓1 ∈ struct(𝑆). Thus

                𝑉 ′ Lℎ 1 M𝐻 ′ = 𝑉 ′ L⟨𝑡, 𝑓1, default(𝑇1 )⟩M𝐻 ′                 ℎ 1 = ⟨𝑡, 𝑓1, default(𝑇1 )⟩
                                   ′
                            = {⟨𝑉 (𝑡), 𝑓1 ⟩}                                                         defn.
                            = {⟨ℓ, 𝑓1 ⟩}                                                         defn. 𝑉 ′

If ℎ 2 ∈ H(𝜎), then

                          𝑉 ′ Lℎ 2 M𝐻 ′ = 𝑉 Lℎ 2 M𝐻                           𝑉 ⊆ 𝑉 ′, 𝐻 ⊆ 𝐻 ′
                                       ⊆𝛼                                            Lemma 14

Now ⟨ℓ, 𝑓1 ⟩ ∉ 𝛼 since ℓ is a fresh value. Therefore 𝑉 ′ Lℎ 1 M𝐻 ′ ∩ 𝑉 ′ Lℎ 2 M𝐻 ′ = ∅ in this case.
  Otherwise, ℎ 2 = ⟨𝑡, 𝑓2, default(𝑇2 )⟩ for some 𝑇2 𝑓2 ∈ struct(𝑆). Then 𝑓1 ≠ 𝑓2 since ℎ 1 ≠ ℎ 2 .
Therefore

              𝑉 ′ Lℎ 1 M𝐻 ′ ∩ 𝑉 ′ Lℎ 2 M𝐻 ′ = 𝑉 ′ L⟨𝑡, 𝑓1, default(𝑇1 )⟩M𝐻 ′ ∩ 𝑉 ′ L⟨𝑡, 𝑓2, default(𝑇2 )⟩M𝐻 ′
                                        = {⟨𝑉 ′ (𝑡), 𝑓1 ⟩} ∩ {⟨𝑉 ′ (𝑡), 𝑓2 ⟩}
                                        =∅

     Therefore,
                                  ∀ ℎ 1, ℎ 2 ∈ H(𝜎 ′ ) : 𝑉 ′ Lℎ 1 M𝐻 ′ ∩ 𝑉 ′ Lℎ 2 M𝐻 ′ = ∅.

     Now, since we have shown all requirements, we can conclude that

                                                  ⟨𝐻 ′, 𝛼 ′ ⟩ 𝑉 ′ H(𝜎 ′ ).

     Finally, since H is the only component that differs between 𝜎 ′ and 𝜎, ⟨𝐻 ′, 𝛼 ′, 𝜌⟩ 𝑉 ′ 𝜎, 𝜌 [𝑥 ↦→
ℓ] 𝑉 ′ 𝛾 (𝜎) [𝑥 ↦→ 𝑡], and ⟨𝐻 ′, 𝛼 ′ ⟩ 𝑉 ′ H(𝜎 ′ ),

                                  ⟨𝐻 ′, 𝛼 ′, 𝜌 [𝑥 ↦→ ℓ]⟩ 𝑉 ′ 𝜎 ′ [𝛾 = 𝛾 (𝜎) [𝑥 ↦→ 𝑡]]

which is what we wanted to show.
   Part 34.3: First, we show that the partial state ⟨𝐻, S ∗ ⟩ is validated by Σ′ and 𝑉 ′ .
   Since the initial state is validated by Σ and 𝑉 , the partial state ⟨𝐻, S ∗ ⟩ is validated by Σ and
valuation 𝑉 . Therefore one of 33.1, 33.2, 33.3 applies. We want to show that the partial state ⟨𝐻, S ∗ ⟩
is validated by Σ′ and valuation 𝑉 ′ .
 • Case 33.1: Then S ∗ = nil and trivially ⟨𝐻, nil⟩ is validated by Σ′ and valuation 𝑉 ′ .
Gradually Verifying Unfolding Expressions & Pure Functions                                                                87


 • Case 33.2: Then S ∗ = ⟨𝜌 0, 𝛼 0, 𝑦 = 𝑚(𝑒 1, · · · , 𝑒𝑘 ); 𝑠 0 ⟩ · S0 for some 𝜌 0 , 𝛼 0 , 𝑦, 𝑚, 𝑘, 𝑒 1, · · · , 𝑒𝑘 , 𝑠 0 ,
   S0 . Also, there is some Σ0 , 𝑉0 , 𝑥 1, · · · , 𝑥𝑘 , 𝑡 1, · · · , 𝑡𝑘 and 𝜎0, · · · , 𝜎𝑘 , 𝜎 ′ such that
                             The partial state ⟨𝐻, S0 ⟩ is validated by Σ0 and 𝑉0,
                         Σ0 is reachable from Π with valuation 𝑉0,                 𝑠 (Σ0 ) = 𝑠 (S ∗ )
                                                 𝑥 1, · · · , 𝑥𝑘 = params(𝑚),
                    𝜎0 = 𝜎 (Σ0 ),     𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, _,       ··· ,     𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,
                                             ′                                ′
                        𝜎𝑘 ⊢ pre(𝑚) ▷ 𝜎 , _,           ⟨𝐻, 𝛼 0, 𝜌 0 ⟩ 𝑉 𝜎 [𝛾 = 𝛾 (𝜎0 )],        and
                                                                          0

                                        ∀ 1 ≤ 𝑖 ≤ 𝑘 : 𝑉 (𝛾 (Σ)(𝑥𝑖 )) = 𝑉0 (𝑡𝑖 ),
                                                 𝜙˜ (Σ) = post(𝑚).
   We want to show that the partial state ⟨𝐻, ⟨𝜌 0, 𝛼 0, 𝑦 = 𝑚(𝑒 1, · · · , 𝑒𝑘 ); 𝑠⟩ · S0 ⟩ is validated by Σ′
   and valuation 𝑉 ′ . Immediately from above we can conclude that
                             The partial state ⟨𝐻, S0 ⟩ is validated by Σ0 and 𝑉0,
                         Σ0 is reachable from Π with valuation 𝑉0,                 𝑠 (Σ0 ) = 𝑠 (S ∗ )
                                                 𝑥 1, · · · , 𝑥𝑘 = params(𝑚),
                𝜎0 = 𝜎 (Σ0 ),     𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, _,       ··· ,     𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,     and
                            𝜎𝑘 ⊢ pre(𝑚) ▷ 𝜎 ′, _,           ⟨𝐻, 𝛼 0, 𝜌 0 ⟩ 𝑉 𝜎 ′ [𝛾 = 𝛾 (𝜎0 )].
                                                                              0

    Also, the frame ⟨𝛼, 𝜌, 𝑥 = alloc(𝑆); 𝑠⟩ must be executing the body of 𝑚, since it is in the stack
    immediately above the frame that contains 𝑦 = 𝑚(𝑒 1, · · · , 𝑒𝑘 ). Therefore, since 𝑥 1, · · · , 𝑥𝑘 are all
    parameters of 𝑚, 𝑦 must be distinct from all of 𝑥 1, · · · , 𝑥𝑘 , since we do not allow assignment to
    parameters in a well-formed program. Thus
                  ∀1 ≤ 𝑖 ≤ 𝑘 : 𝑉 ′ (𝛾 (Σ′ ) (𝑥𝑖 )) = 𝑉 ′ ((𝛾 (𝜎) [𝑥 ↦→ 𝑡]) (𝑥𝑖 )) = 𝑉 ′ (𝛾 (𝜎) (𝑥𝑖 ))
                                                      = 𝑉 ′ (𝛾 (Σ)(𝑥𝑖 )) = 𝑉 (𝛾 (Σ) (𝑥𝑖 ))
                                                      = 𝑉0 (𝑡𝑖 ).
    Finally, 𝜙˜ (Σ′ ) = 𝜙˜ (Σ) by definition, thus
                                          𝜙˜ (Σ′ ) = 𝜙˜ (Σ) = post(𝑚).
   Therefore the partial state ⟨𝐻, S ∗ ⟩ is validated by Σ′ and 𝑉 ′ in this case.
 • Case 33.3: Then S ∗ = ⟨𝜌 0, 𝛼 0, while 𝑒 0 invariant 𝜙˜0 do 𝑠 0 ; 𝑠 0′ ⟩ · S0 for some 𝜌 0 , 𝛼 0 , 𝑒, 𝜙˜0 , 𝑠 0 , 𝑠 0′ ,
   S0 , and there exists some Σ0 , 𝑉0 , and 𝜎0′ such that:
                              The partial state ⟨𝐻, S0 ⟩ is validated by Σ0 and 𝑉0
                         Σ0 is reachable from Π with valuation 𝑉0,                 𝑠 (Σ0 ) = 𝑠 (S ∗ )
                                   𝜎0 ⊢ 𝜙˜0 ▷ 𝜎0′ , _,      ⟨𝐻, 𝛼 0, 𝜌 0 ⟩ 𝑉 𝜎0′     and
                                                                              0

                                                         𝜙˜ (Σ) = 𝜙˜0 .
   Now, by definition of Σ′′ , 𝜙˜ (Σ′ ) = 𝜙˜ (Σ) = 𝜙˜0 . Therefore, using the other assumptions given
   above, the partial state ⟨𝐻, S ∗ ⟩ is validated by Σ′ and 𝑉 ′ in this case.
  Therefore the partial state ⟨𝐻, S ∗ ⟩ is validated by Σ′ and 𝑉 ′ .
  Now, by lemma 55, the partial state ⟨𝐻 ′, S ∗ ⟩ is validated by Σ′ and 𝑉 ′ , which is what we need to
show for this part.
  Therefore ⟨𝐻 ′, ⟨𝛼 ′, 𝜌 [𝑥 ↦→ ℓ], 𝑠⟩ · S ∗ ⟩ is validated by Σ′ with 𝑉 , which completes the proof.
88                                                                                                           Torek et al.


     Case 5. ExecCallEnter: We have
                      ⟨𝐻, ⟨𝛼, 𝜌, 𝑦 = 𝑚(𝑒); 𝑠⟩ · S ∗ ⟩, 𝑉 ′ LΘM𝐻 →
                         ⟨𝐻, ⟨𝛼 ′, 𝜌 ′, body(𝑚); skip⟩ · ⟨𝛼 \ 𝛼 ′, 𝜌, 𝑦 = 𝑚(𝑒); 𝑠⟩ · S ∗ ⟩
                      where 𝑥 = params(𝑚),              ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑣,     ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒,
                              ′                                 ′
                            𝜌 = [𝑥 ↦→ 𝑣],        ⟨𝐻, 𝛼 \ 𝛼,
                                                         ˆ 𝜌 ⟩ ⊨ pre(𝑚),
                                   ′
                            𝛼ˆ = 𝑉 LΘM𝐻 ,      and 𝛼 ′ = ⌊pre(𝑚)⌋ ⟨𝐻, 𝛼\𝛼,ˆ 𝜌 ′ ⟩ .
  By assumptions, the initial state is validated by some Σ and valuation 𝑉 , thus Σ = ⟨𝜎, 𝑦 =
         ˜ for some 𝜎, 𝜙˜ where ⟨𝐻, 𝛼, 𝜌⟩ ′ 𝜎.
𝑚(𝑒); 𝑠, 𝜙⟩                                𝑉
  The only guard rule that applies is SGuardCall, so we have
                         𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R,      𝜎 ′ [𝛾 = [𝑥 ↦→ 𝑡]] ⊢ pre(𝑚) ▷ 𝜎 ′′, R ′,
                    Θ = rem(𝜎 ′′, pre(𝑚)),        and by assumptions,          ⟨𝐻, 𝛼⟩ ⊢𝑉 R ∪ R ′
  For some 𝑘, let 𝑥 1, · · · , 𝑥𝑘 = 𝑥, 𝑒 1, · · · , 𝑒𝑘 = 𝑒, 𝑣 1, · · · , 𝑣𝑘 = 𝑣, and 𝑡 1 = fresh, · · · , 𝑡𝑘 = fresh.
  Also, let 𝜎0 = ⟨⊥, ∅, ∅, [𝑥 1 ↦→ 𝑡 1, · · · , 𝑥𝑘 ↦→ 𝑡𝑘 ], true⟩, and let 𝑉0 = [𝑡 1 ↦→ 𝑣 1, · · · , 𝑡𝑘 ↦→ 𝑣𝑘 ].
Then ⟨𝐻, 𝛼 ′, 𝜌 ′ ⟩ 𝑉 𝜎0 .
                       0
  Tpre(𝑚)U ⟨𝐻, 𝜌 ′ ⟩ ⊆ 𝛼 ′ : If pre(𝑚) is completely precise, then 𝛼 ′ = ⌊pre(𝑚)⌋ ⟨𝐻, 𝛼\𝛼,ˆ 𝜌 ′ ⟩ =
Tpre(𝑚)U ⟨𝐻, 𝜌 ′ ⟩ . Otherwise, 𝛼 ′ = ⌊pre(𝑚)⌋ ⟨𝐻, 𝛼\𝛼,ˆ 𝜌 ′ ⟩ = 𝛼 \ 𝛼,      ˆ but also Tpre(𝑚)U ⟨𝐻, 𝜌 ′ ⟩ ⊆ 𝛼 ′ = 𝛼 \ 𝛼ˆ
by lemma 4 since ⟨𝐻, 𝛼 \ 𝛼,     ˆ 𝜌 ′ ⟩ ⊨ pre(𝑚).
  Now ⟨𝐻, 𝛼 ′, 𝜌 ′ ⟩ ⊨ pre(𝑚) by lemma 12, since ⟨𝐻, 𝛼 \ 𝛼,                ˆ 𝜌 ′ ⟩ ⊨ pre(𝑚).
  Now ⟨𝐻, 𝛼 , 𝜌 ⟩ ⊨ pre(𝑚), ⟨𝐻, 𝛼 , 𝜌 ⟩ 𝑉 𝜎0 . Thus by lemma 32, for some 𝜎0′ ,
              ′      ′                     ′     ′
                                                    0

               𝜎0 ⊢ pre(𝑚) ◁ 𝜎0′ and 𝑉0′ (𝑔(𝜎0 ))         where 𝑉0′ = 𝑉0 [𝜎0 ⊢ pre(𝑚) ◁ 𝜎0′ | 𝐻 ].
     Let Σ′0 = ⟨𝜎0′ , body(𝑚); skip, post(𝑚)⟩. We want to show that
                    Γ ′ = ⟨𝐻, ⟨𝛼 ′, 𝜌 ′, body(𝑚); skip⟩ · ⟨𝛼 \ 𝛼 ′, 𝜌, 𝑦 = 𝑚(𝑒); 𝑠⟩ · S ∗ ⟩
is validated by Σ′0 with 𝑉0′ .
   Part 34.1: By SVerifyMethod, Π ⊢ init → Σ′0 . Therefore Σ′0 is reachable from Π with valuation 𝑉0′ .
   Part 34.2: We want to show that Γ ′ corresponds to Σ′0 .
   By definition 𝑠 (Σ′0 ) = body(𝑚); skip = 𝑠 (Γ ′ ). Therefore, since 𝜎 (Σ′0 ) = 𝜎0′ , it suffices to show
⟨𝐻, 𝛼 ′, 𝜌 ′ ⟩ 𝑉 ′ 𝜎0′ .
                0
     Since H(𝜎0 ) = H (𝜎0 ) = ∅, ⟨𝐻, 𝛼 ′ \ Tpre(𝑚)U ⟨𝐻, 𝜌 ′ ⟩ ⟩ 𝑉 H(𝜎0 ) and ⟨𝐻, 𝛼 ′ \ Tpre(𝑚)U ⟨𝐻, 𝜌 ′ ⟩ ⟩ 𝑉
                                                                        0                                              0
H (𝜎0 ). Also, for each 1 ≤ 𝑖 ≤ 𝑘, 𝑉0 (𝛾 (𝜎0 ) (𝑥𝑖 )) = 𝑣𝑖 = 𝜌 ′ (𝑥𝑖 ), thus 𝜌 ′ 𝑉 𝛾 (𝜎0 ). Finally, 𝑉0 (𝑔(𝜎0 )) =
                                                                                      0
𝑉0 (true) = true. Therefore ⟨𝐻, 𝛼 ′ \ Tpre(𝑚)U ⟨𝐻, 𝜌 ′ ⟩ , 𝜌 ′ ⟩ 𝑉 𝜎0 .
                                                                  0
   Also, as shown before, ⟨𝐻, 𝛼 ′, 𝜌 ′ ⟩ ⊨ pre(𝑚). Therefore, by lemma 31,
                                                 ⟨𝐻, 𝛼 ′, 𝜌 ′ ⟩ 𝑉 ′ 𝜎0′ .
                                                                    0

     Part 34.3: We want to show that the partial state ⟨𝐻, ⟨𝛼 \ 𝛼 ′, 𝜌, 𝑦 = 𝑚(𝑒); 𝑠⟩ · S ∗ ⟩ is validated by
Σ′0 with 𝑉0′ , thus it suffices to show that case 33.2 is satisfied.
   Since ⟨𝛼, 𝜌, 𝑦 = 𝑚(𝑒); 𝑠⟩ · S ∗ was validated by Σ and 𝑉 , the partial state ⟨𝐻, S ∗ ⟩ is validated by
Σ and 𝑉 .
  Also, by assumptions, Σ is reachable from Π with valuation 𝑉 and 𝑠 (Σ) = 𝑦 = 𝑚(𝑒); 𝑠 as shown
before.
  Furthermore, by assumptions, 𝑥 1, · · · , 𝑥𝑘 = 𝑥 = params(𝑚)
Gradually Verifying Unfolding Expressions & Pure Functions                                                                    89


  Now let 𝜎0 = 𝜎 = 𝜎 (Σ), then 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R, which was shown before, represents the series of
judgements
                             𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, R 1,            ···   𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , S𝑘
where 𝜎𝑘    = 𝜎 ′ . Also, as shown before,
                             𝜎𝑘 [𝛾 = [𝑥 1 ↦→ 𝑡 1, · · · , 𝑥𝑘 ↦→ 𝑡𝑘 ]] ⊢ pre(𝑚) ▷ 𝜎 ′′, R ′ .
Note that by definition 40 𝑉 ′ = 𝑉 [Σ ⇀ 𝜎 ′ ⊣ R, Θ | 𝐻 ] is the valuation corresponding to the series
of judgements above, extending 𝑉 .
   By lemmas 24 and 34, 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎𝑘 ) =⇒ · · · =⇒ 𝑔(𝜎1 ). Thus, since 𝑉 ′ (𝑔(𝜎 ′′ )) = true by
assumption,
                              𝑉 ′ (𝑔(𝜎 ′′ )) = 𝑉 ′ (𝑔(𝜎𝑘 )) = · · · = 𝑉 ′ (𝑔(𝜎1 )) = true.
Therefore, by lemmas 26 and 43,

          ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎1,        ··· ,      ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎𝑘 ,              ⟨𝐻, 𝛼 \ Tpre(𝑚)U ⟨𝐻, 𝜌 ′ ⟩ , 𝜌 ′ ⟩ 𝑉 ′ 𝜎 ′′,

Furthermore, since 𝛼ˆ = 𝑉 ′ LΘM𝐻 = 𝑉 ′ Lrem(𝜎 ′′, pre(𝑚))M𝐻 and ⟨𝐻, 𝛼 \ 𝛼,
                                                                        ˆ 𝜌 ′ ⟩ ⊨ pre(𝑚), we can
apply lemma 57 to get
                                           ⟨𝐻, 𝛼 \ 𝛼 ′, 𝜌 ′ ⟩ 𝑉 ′ 𝜎 ′′ [𝛾 = 𝛾 (𝜎0 )].

Since 𝜌 𝑉 𝛾 (𝜎0 ) (by assumptions and since 𝜎0 = 𝜎),

                                           ⟨𝐻, 𝛼 \ 𝛼 ′, 𝜌⟩ 𝑉 ′ 𝜎 ′′ [𝛾 = 𝛾 (𝜎0 )].

   For each 1 ≤ 𝑖 ≤ 𝑘, ⟨𝐻, 𝜌⟩ ⊢ 𝑒𝑖 ⇓ 𝑉 ′ (𝑡𝑖 ) by lemma 26, and ⟨𝐻, 𝜌⟩ ⊢ 𝑒𝑖 ⇓ 𝑣𝑖 as shown before, thus
𝑉 ′ (𝑡𝑖 ) = 𝑣𝑖 . Thus
                 ∀ 1 ≤ 𝑖 ≤ 𝑘 : 𝑉0′ (𝛾 (Σ′0 ) (𝑥𝑖 )) = 𝑉0′ (𝛾 (𝜎0′ ) (𝑥𝑖 ))                               by defn.
                                                       = 𝑉0′ (𝛾 (𝜎0 ) (𝑥𝑖 ))                          Lemma 37
                                                       = 𝑉0 (𝛾 (𝜎0 ) (𝑥𝑖 ))                              𝑉 ⊆ 𝑉′
                                                       = 𝑣𝑖                                               by def.
                                                              ′
                                                       = 𝑉 (𝑡𝑖 ).                                 shown above

  Finally, by definition 𝜙˜ (Σ) = post(𝑚).
  Therefore the partial state ⟨𝐻, ⟨𝛼 ′, 𝜌 ′, body(𝑚); skip⟩ · ⟨𝛼 \ 𝛼 ′, 𝜌, 𝑦 =𝑚(𝑒); 𝑠⟩ · S ∗ ⟩ is validated
by Σ′0 with 𝑉0′ .
  Therefore Γ ′ is validated by Σ′0 with 𝑉0′ .
  Case 6. ExecCallExit: We have
             ⟨𝐻, ⟨𝛼, 𝜌, skip⟩ · ⟨𝛼 ′, 𝜌 ′, 𝑦 = 𝑚(𝑒); 𝑠⟩ · S⟩, 𝑉 ′ LΘM𝐻 → ⟨𝐻, ⟨𝛼 ′′, 𝜌 ′′, 𝑠⟩ · S ∗ ⟩                         (30)
                                                                         ′′       ′
                          where ⟨𝐻, 𝛼, 𝜌⟩ ⊨ post(𝑚),                    𝜌 = 𝜌 [𝑦 ↦→ 𝜌 (result)],                             (31)
                                                  ′′      ′
                                           and 𝛼 = 𝛼 ∪ ⌊post(𝑚)⌋ ⟨𝐻, 𝛼, 𝜌 ⟩ .                                                (32)

   By assumptions, the initial state is validated by some Σ and valuation 𝑉 , thus Σ = ⟨𝜎, skip, 𝜙⟩      ˜
             ˜
for some 𝜎, 𝜙 where ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎.
   Also, by 34.3, the partial state ⟨𝐻, ⟨𝛼 ′, 𝜌 ′, 𝑦 =𝑚(𝑒); 𝑠⟩ ·S⟩ is validated by Σ and 𝑉 . Thus 33.2 must
apply, and thus there is some Σ′ reachable from Π and valuation 𝑉 such that Σ′ = ⟨𝜎0, 𝑦=𝑚(𝑒); 𝑠, 𝜙˜ ′ ⟩
90                                                                                                                         Torek et al.


for some 𝜎0, 𝜙˜ ′ . Also, we can let 𝑒 1, · · · , 𝑒𝑘 = 𝑒 and then there are sequences 𝜎1, · · · , 𝜎𝑘 , 𝑥 1, · · · , 𝑥𝑘 ,
and 𝑡 1, · · · , 𝑡𝑘 where
                 𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, _,           ··· ,    𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,                       by (8)                (33)
                                                               ′
                 𝜎𝑘 [𝛾 = [𝑥𝑖 ↦→ 𝑡𝑖 ]] ⊢ pre(𝑚) ▷ 𝜎 , _,                                                                           (34)
                                      ′   ′         ′
                 and       ⟨𝐻, 𝛼 , 𝜌 ⟩ 𝑉 ′ 𝜎 [𝛾 = 𝛾 (𝜎0 )]                                                 by (10)                (35)
where 𝑉 ′ is a valuation corresponding to this series of judgements.
  Let
             𝑡 = fresh,        𝑉ˆ ′ = 𝑉 ′ [𝑡 ↦→ 𝜌 (result)],              𝜌ˆ = [𝑥 1 ↦→ 𝜌 (𝑥 1 ), · · · , 𝑥𝑘 ↦→ 𝜌 (𝑥𝑘 )],
                                      and 𝛾ˆ = [𝑥 1 ↦→ 𝑡 1, · · · , 𝑥𝑘 ↦→ 𝑡𝑘 , result ↦→ 𝑡]
  We have ⟨𝐻, 𝛼, 𝜌⟩ ⊨ post(𝑚) by (31). Since 𝜌ˆ is simply the restriction of 𝜌 to params(𝑚) and
result, and post(𝑚) may only reference variables in params(𝑚) as well as result, ⟨𝐻, 𝛼, 𝜌⟩           ˆ ⊨
post(𝑚) and Tpost(𝑚)U ⟨𝐻, 𝜌ˆ ⟩ = Tpost(𝑚)U ⟨𝐻, 𝜌 ⟩ .
  By lemma 4 Tpost(𝑚)U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼. Recall that 𝛼 ′′ = 𝛼 ∪ ⌊post(𝑚)⌋ ⟨𝐻, 𝛼, 𝜌 ⟩ . If post(𝑚) is com-
pletely precise, then ⌊post(𝑚)⌋ ⟨𝐻, 𝛼, 𝜌 ⟩ = Tpost(𝑚)U ⟨𝐻, 𝜌 ⟩ . Otherwise, ⌊post(𝑚)⌋ ⟨𝐻, 𝛼, 𝜌 ⟩ = 𝛼, but
Tpost(𝑚)U ⟨𝐻, 𝜌 ⟩ ⊆ 𝛼 as shown before. In both cases, Tpost(𝑚)U ⟨𝐻, 𝜌 ⟩ = Tpost(𝑚)U ⟨𝐻, 𝜌ˆ ⟩ ⊆ 𝛼 ′′ .
  Therefore by lemma 12
                                         ⟨𝐻, 𝛼 ′′, 𝜌⟩
                                                   ˆ ⊨ post(𝑚).                                       (36)
     Note that, for all 1 ≤ 𝑖 ≤ 𝑘,
             𝑉ˆ ′ (𝑡𝑖 ) = 𝑉 ′ (𝑡𝑖 )                                                                    by definition
                       = 𝑉 (𝛾 (Σ) (𝑥𝑖 ))                                                                        by (9)
                       = 𝜌 (𝑥𝑖 )                           since 𝜌 𝑉 𝛾 (Σ), since initial valid by Σ and 𝑉
                       = 𝜌ˆ (𝑥𝑖 )                                                                      by definition

Thus 𝜌ˆ ˆ ′ 𝛾 ′ . Also, ⟨𝐻, 𝛼 ′, 𝜌 ′ ⟩ 𝑉 ′ 𝜎 ′ [𝛾 = 𝛾 (𝜎0 )] by (35). Therefore ⟨𝐻, 𝛼 ′, 𝜌⟩
                                                                                         ˆ ˆ ′ 𝜎 ′ [𝛾 = 𝛾].
                                                                                                        ˆ
          𝑉                                                                                 𝑉
                 ′′    ′
Finally, since 𝛼 ⊆ 𝛼 , by lemma 19,

                                                    ⟨𝐻, 𝛼 ′′, 𝜌⟩
                                                              ˆ           𝜎 ′ [𝛾 = 𝛾].
                                                                                   ˆ                                              (37)
                                                                   𝑉ˆ ′

     Now, by lemma 32, (36), and (37),
                             𝜎 ′ [𝛾 = 𝛾]
                                      ˆ ⊢ post(𝑚) ◁ 𝜎 ′′,                 and 𝑉 ′′ (𝑔(𝜎 ′′′ )) = true                             (38)
where 𝑉 ′′ is the corresponding valuation extending 𝑉ˆ ′ .
  Let 𝜎 ′′′ = 𝜎 ′′ [𝛾 = 𝛾 (𝜎0 ) [𝑦 ↦→ 𝑡]].
  Now (33), (34), and (38), and the definition of 𝜎 ′′′ satisfy the antecedent for SExecCall, therefore
                                              𝜎0 ⊢ 𝑦 = 𝑚(𝑒 1, · · · , 𝑒𝑘 ); 𝑠 → 𝑠 ⊣ 𝜎 ′′′ .
Let Σ′′ = ⟨𝜎 ′′′, 𝑠, 𝜙˜ ′ ⟩, now by SVerifyStep
                                                           Π ⊢ Σ′ → Σ′′ .
     We want to show that ⟨𝐻, ⟨𝛼 ′′, 𝜌 ′′, 𝑠⟩ · S ∗ ⟩ is validated by Σ′′ .
     Part 34.1: Since Π ⊢ Σ′ → Σ′′ , Σ′′ is reachable from Π. Let its corresponding valuation be 𝑉 ′′′ .
     Part 34.2: By definition, 𝑠 (Σ′′ ) = 𝑠.
Gradually Verifying Unfolding Expressions & Pure Functions                                                                                 91


    By (35) ⟨𝐻, 𝛼 ′, 𝜌 ′ ⟩ 𝑉 ′ 𝜎 ′ [𝛾 = 𝛾 (𝜎0 )]. Since the initial state must be well-formed, 𝛼 and 𝛼 ′ are dis-
joint, and as shown before, Tpost(𝑚)U ⟨𝐻, 𝜌 ⟩ = Tpost(𝑚)U ⟨𝐻, 𝜌ˆ ⟩ ⊆ 𝛼, therefore 𝛼 ′ \Tpost(𝑚)U ⟨𝐻, 𝜌ˆ ⟩ =
𝛼 ′ . Also, 𝑉ˆ ′ ⊆ 𝑉 ′ . Thus

                                    ⟨𝐻, 𝛼 ′ \ Tpost(𝑚)U ⟨𝐻, 𝜌ˆ ⟩ , 𝜌 ′ ⟩                 𝜎 ′ [𝛾 = 𝛾 (𝜎0 )].
                                                                                𝑉ˆ ′


   Also, as shown before, 𝜌ˆ                    ˆ therefore
                                                𝛾,
                                         𝑉ˆ ′


                                        ⟨𝐻, 𝛼 ′ \ Tpost(𝑚)U ⟨𝐻, 𝜌ˆ ⟩ , 𝜌⟩
                                                                       ˆ                      𝜎 ′ [𝛾 = 𝛾].
                                                                                                       ˆ
                                                                                   𝑉ˆ ′


   Then, since 𝛼 ′ ⊆ 𝛼 ′′ , 𝛼 ′ \ Tpost(𝑚)U ⟨𝐻, 𝜌ˆ ⟩ ⊆ 𝛼 ′′ \ Tpost(𝑚)U ⟨𝐻, 𝜌ˆ ⟩ , and thus by lemma 19

                                       ⟨𝐻, 𝛼 ′′ \ Tpost(𝑚)U ⟨𝐻, 𝜌ˆ ⟩ , 𝜌⟩
                                                                       ˆ                          𝜎 ′ [𝛾 = 𝛾].
                                                                                                           ˆ
                                                                                       𝑉ˆ ′


  Now, since it was shown in (36) that ⟨𝐻, 𝛼 ′′, 𝜌⟩
                                                 ˆ ⊨ post(𝑚) and in (38) that 𝑉 ′′ (𝑔(𝜎 ′′ )) = true,
by lemma 31

                                                         ⟨𝐻, 𝛼 ′′, 𝜌⟩
                                                                   ˆ 𝑉 ′′ 𝜎 ′′ .

   Now by (35) 𝜌 ′ 𝑉 ′ 𝛾 (𝜎0 ), then since 𝑉 ′ ⊆ 𝑉 ′′ , 𝜌 ′ 𝑉 ′′ 𝛾 (𝜎0 ). Now, since 𝛾 (𝜎 ′′′ ) = 𝛾 (𝜎0 ) [𝑦 ↦→ 𝑡],
to show 𝜌 ′′ 𝑉 ′′ 𝛾 (𝜎 ′′′ ) it suffices to show that 𝑉 ′′ (𝛾 (𝜎 ′′′ ) (𝑦)) = 𝜌 ′′ (𝑦).
   But now 𝑉 ′′ (𝛾 (𝜎 ′′′ ) (𝑦)) = 𝑉 ′′ (𝑡) = 𝑉ˆ ′ (𝑡) = 𝜌 (result) = 𝜌 ′′ (𝑦), which is what we needed to
show. Therefore, since 𝛾 is the only component changed between 𝜎 ′′ and 𝜎 ′′′ ,

                                                        ⟨𝐻, 𝛼 ′′, 𝜌 ′′ ⟩ 𝑉 ′′ 𝜎 ′′′ .

  Therefore, since 𝜎 (Σ′′ ) = 𝜎 ′′′ , we have shown that Σ′′ corresponds to ⟨𝐻, ⟨𝛼 ′′, 𝜌 ′′, 𝑠⟩ · S ∗ ⟩ with
valuation 𝑉 ′′ .
  Part 34.3: We need to show that the partial state ⟨𝐻, S ∗ ⟩ is validated by Σ′′ and 𝑉 ′′ . We already
have that ⟨𝐻, S ∗ ⟩ is validated by Σ′ and 𝑉 ′ . Thus one of 33.1, 33.2, or 33.3 must apply.
  If 33.1 applies: Then S ∗ = nil, thus trivially the partial state ⟨𝐻, S ∗ ⟩ is validated by Σ′′ and 𝑉 ′′ .
  If 33.2 applies: Then S ∗ = ⟨𝛼 0, 𝜌 0, 𝑦 ′ =𝑚 ′ (𝑒 1′ , · · · , 𝑒𝑘′ ′ ); 𝑠 ′ ⟩ ·S0∗ for some 𝑘 ′, 𝑦 ′, 𝑚 ′, 𝑒 1′ , · · · , 𝑒𝑘′ ′ , 𝑠 ′, S0∗ .
Also, there exists some Σ′0, 𝑉0′, 𝑥 1′ , · · · , 𝑥𝑘′ ′ , 𝑡 1′ , · · · , 𝑡𝑘′ ′ , 𝜎0, · · · , 𝜎𝑘 ′ , 𝜎 ′ such that

                                  The partial state ⟨𝐻, S0∗ ⟩ is validated by Σ′0 and 𝑉0′,
                            Σ′0 is reachable from Π with valuation 𝑉0′,                               𝑠 (Σ′0 ) = 𝑠 (S ∗ ),
                                                    𝑥 1′ , · · · , 𝑥𝑘′ ′ = params(𝑚),
                      𝜎0 = 𝜎 (Σ′0 ),       𝜎0 ⊢ 𝑒 1′ ⇓ 𝑡 1′ ⊣ 𝜎1, _,      ··· ,          𝜎𝑘 ′ −1 ⊢ 𝑒𝑘′ ′ ⇓ 𝑡𝑘′ ′ ⊣ 𝜎𝑘 ′ , _,
                               𝜎𝑘 ′ ⊢ pre(𝑚 ′ ) ▷ 𝜎 ′, _,          ⟨𝐻, 𝛼 0, 𝜌 0 ⟩ 𝑉 ′ 𝜎 ′ [𝛾 = 𝛾 (𝜎0 )],
                                                                                              0

                                       ∀ 1 ≤ 𝑖 ≤ 𝑘 ′ : 𝑉 ′ (𝛾 (Σ′ ) (𝑥𝑖 )) = 𝑉0′ (𝑡𝑖′ ),                  and
                                                      𝜙˜ (Σ′ ) = post(𝑚 ′ ).
92                                                                                                                Torek et al.


  We want to show that the partial state ⟨𝐻, S ∗ ⟩ is validated by Σ′′ and 𝑉 ′′ . Immediately from
above,
                              The partial state ⟨𝐻, S0∗ ⟩ is validated by Σ′0 and 𝑉0′,
                         Σ′0 is reachable from Π with valuation 𝑉0′,                 𝑠 (Σ′0 ) = 𝑠 (S ∗ ),
                                               𝑥 1′ , · · · , 𝑥𝑘′ ′ = params(𝑚),
                   𝜎0 = 𝜎 (Σ′0 ),     𝜎0 ⊢ 𝑒 1′ ⇓ 𝑡 1′ ⊣ 𝜎1, _,    ··· ,    𝜎𝑘 ′ −1 ⊢ 𝑒𝑘′ ′ ⇓ 𝑡𝑘′ ′ ⊣ 𝜎𝑘 ′ , _,
                            𝜎𝑘 ′ ⊢ pre(𝑚 ′ ) ▷ 𝜎 ′, _,      ⟨𝐻, 𝛼 0, 𝜌 0 ⟩ 𝑉 ′ 𝜎 ′ [𝛾 = 𝛾 (𝜎0 )].
                                                                              0

Also, the frame ⟨𝛼 ′, 𝜌 ′, 𝑦 = 𝑚(𝑒 1, · · · , 𝑒𝑘 ); 𝑠⟩ must be executing the body of 𝑚 ′ , since it is in the
stack immediately above the frame that contains 𝑦 ′ = 𝑚 ′ (𝑒 1′ , · · · , 𝑒𝑘′ ′ ). Therefore, since 𝑥 1′ , · · · , 𝑥𝑘 ′
are all parameters of 𝑚 ′ , 𝑦 must be distinct from all of 𝑥 1′ , · · · , 𝑥𝑘′ ′ , since we do not allow assignment
to parameters in a well-formed program. Thus
                 ∀1 ≤ 𝑖 ≤ 𝑘 ′ : 𝑉 ′′ (𝛾 (Σ′′ ) (𝑥𝑖 )) = 𝑉 ′′ (𝛾 (Σ′ ) (𝑥𝑖 )) = 𝑉 ′ (𝛾 (Σ′ ) (𝑥𝑖 )) = 𝑉0′ (𝑡𝑖 ).

     Finally, 𝜙˜ (Σ′′ ) = 𝜙˜ (Σ′ ) by definition, thus

                                              𝜙˜ (Σ′′ ) = 𝜙˜ (Σ′ ) = post(𝑚 ′ ).
     Therefore the partial state ⟨𝐻, S ∗ ⟩ is validated by Σ′′ and 𝑉 ′′ in this case.
     If 33.3 applies: Then S ∗ = ⟨𝜌 0, 𝛼 0, while 𝑒 invariant 𝜙˜0 do 𝑠 0 ; 𝑠 0′ ⟩ · S0∗ for some 𝜌 0 , 𝛼 0 , 𝑒, 𝜙˜0 , 𝑠 0 ,
𝑠 0 , S0∗ , and there exists some Σ′0 , 𝑉0′ , and 𝜎0′ such that:
  ′


                              The partial state ⟨𝐻, S0∗ ⟩ is validated by Σ′0 and 𝑉0′
                         Σ′0 is reachable from Π with valuation 𝑉0′,                 𝑠 (Σ′0 ) = 𝑠 (S ∗ ),
                                    𝜎0 ⊢ 𝜙˜0 ▷ 𝜎0′ , _,     ⟨𝐻, 𝛼 0, 𝜌 0 ⟩ 𝑉 ′ 𝜎0′      and
                                                                             0

                                                        𝜙˜ (Σ′ ) = 𝜙˜0 .

  Now, by definition of Σ′′ , 𝜙˜ (Σ′′ ) = 𝜙˜ (Σ′ ) = 𝜙˜0 . Therefore, using the other assumptions given
above, the partial state ⟨𝐻, S ∗ ⟩ is validated by Σ′′ and 𝑉 ′′ in this case.
  Therefore definition part 34.3 is satisfied.
  Therefore all parts of definition 34 are satisfied. Thus ⟨𝐻, ⟨𝛼 ′′, 𝜌 ′′, 𝑠⟩ · S ∗ ⟩ is validated by Σ′′ , as
we wanted to show.
  Case 7. ExecAssert: We have
                        ⟨𝐻, ⟨𝛼, 𝜌, assert 𝜙; 𝑠⟩ · S ∗ ⟩, 𝑉 ′ LΘM𝐻 → ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · S ∗ ⟩
                                              where       ⟨𝐻, 𝛼, 𝜌⟩ ⊨ ? ∗ 𝜙 .

     Since the initial state is validated by Σ, Σ = ⟨𝜎, assert 𝜙; 𝑠, 𝜙⟩
                                                                     ˜ for some 𝜎, 𝜙˜ where ⟨𝐻, 𝛼, 𝜌⟩
                                                                                                      𝑉
𝜎.
     The only guard rule that applies is SGuardAssert, so we have, for some 𝜎 ′ ,
                                                    𝜎 ⊢ ? ∗ 𝜙 ▷ 𝜎 ′, R
                        and by assumptions 𝑉 ′ (𝑔(𝜎 ′ )) = true              and       ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R.
Also, by definition 𝑉 ′ = 𝑉 [𝜎 ⊢ ? ∗ 𝜙 ▷ 𝜎 ′, R | 𝐻 ].
  Thus by lemma 43 ⟨𝐻, 𝛼 \ T? ∗ 𝜙U ⟨𝐻, 𝜌 ⟩ , 𝜌⟩ 𝑉 ′ 𝜎 ′ .
Gradually Verifying Unfolding Expressions & Pure Functions                                               93


  Thus by lemma 19, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ . Also, as noted before, ⟨𝐻, 𝛼, 𝜌⟩ ⊨ ? ∗𝜙. Therefore, by lemma
31, for some 𝜎 ′′ ,
                         𝜎 ′ ⊢ ? ∗ 𝜙 ◁ 𝜎 ′′ and 𝑉 ′′ (𝑔(𝜎 ′′ )) = true.
  Now, by SExecAssert, 𝜎 ⊢ assert 𝜙; 𝑠 → 𝑠 ⊣ 𝜎 [𝑔 = 𝑔(𝜎 ′′ )].
  Let Σ′ = ⟨𝜎 [𝑔 = 𝑔(𝜎 ′′ )], 𝑠, 𝜙⟩.
                                 ˜ We want to show that ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · S ∗ ⟩ is validated by Σ′ and
 ′′
𝑉 .
  By SVerifyStep, Σ′ is reachable from Π with valuation 𝑉 ′′ .
  By assumptions, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎, and 𝑉 ′′ (𝑔(𝜎 ′′ )) = true, thus ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′′ 𝜎 [𝑔 = 𝑔(𝜎 ′′ )].
Also, by definition, Σ′ = ⟨𝜎 [𝑔 = 𝑔(𝜎 ′′ )], 𝑠, 𝜙⟩.
                                                ˜ Therefore Σ′ corresponds to ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · S ∗ ⟩ with
            ′′
valuation 𝑉 .
  Finally, by definition 𝛾 (Σ′ ) = 𝛾 (Σ) and 𝜙˜ (Σ′ ) = 𝜙˜ = 𝜙˜ (Σ).
  Therefore ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · S ∗ ⟩ is a valid state by lemma 47.
  Case 8. ExecIfA: We have
             ⟨𝐻, ⟨𝛼, 𝜌, if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠⟩ · S ∗ ⟩, 𝑉 ′ LΘM𝐻 → ⟨𝐻, ⟨𝛼, 𝜌, 𝑠 1 ; 𝑠⟩ · S ∗ ⟩
                           where       ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ true     and      ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒

  Since the initial state is validated by Σ, Σ = ⟨𝜎, if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠, 𝜙⟩
                                                                                 ˜ for some 𝜎, 𝜙˜ where
⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎.
  The only guard rule that applies is SGuardIf, so we have, for some 𝜎 ′ ,
                                               𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R
                     and by assumptions 𝑉 ′ (𝑔(𝜎 ′ )) = true           and    ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R
where 𝑉 ′ = 𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R | 𝐻 ].
  Now by SExecIfA,
                        𝜎 ⊢ if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠 → 𝑠 1 ; 𝑠 ⊣ 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡].
   Let Σ′ = ⟨𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) &&𝑡], 𝑠 1 ; 𝑠, 𝜙⟩.
                                             ˜ Then by SVerifyStep, Σ′ is reachable from Π with valuation
𝑉 ′.
   Now ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡) and ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ true, thus 𝑉 ′ (𝑡) = true. Also, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ , thus
𝑉 ′ (𝑔(𝜎 ′ )) = true, and then 𝑉 ′ (𝑔(𝜎 ′ ) && 𝑡) = 𝑉 ′ (𝑔(𝜎 ′ )) ∧ 𝑉 ′ (𝑡) = true. Therefore ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′
𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡].
    Also, by definition, Σ′ = ⟨𝜎 [𝑔 = 𝑔(𝜎 ′ ) && 𝑡], 𝑠 1 ; 𝑠, 𝜙⟩.
                                                              ˜ Therefore Σ′ corresponds to
                        ∗
⟨𝐻, ⟨𝛼, 𝜌, 𝑠 1 ; 𝑠⟩ · S ⟩ with valuation 𝑉 .    ′′

    Finally, 𝛾 (Σ′ ) = 𝛾 (𝜎 ′ ) = 𝛾 (𝜎) = 𝛾 (Σ) by lemma 25 and 𝜙˜ (Σ′ ) = 𝜙˜ = 𝜙˜ (Σ) by definition.
    Therefore 𝐻 ⟨𝛼, 𝜌, 𝑠 1 ; 𝑠⟩ · S ∗ is a valid state by lemma 47.
    Case 9. ExecIfB: Similar to case 8, but using SExecIfB.
    Case 10. ExecWhileEnter: We have
                 ⟨𝐻, ⟨𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ ⟩ · S ∗ ⟩ →
                 ⟨𝐻, ⟨𝛼 ′, 𝜌, 𝑠; skip⟩ · ⟨𝛼 \ 𝛼 ′, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ ⟩ · S ∗ ⟩
               where ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ true, ⟨𝐻, 𝛼 \ 𝛼,             ˜
                                                       ˆ 𝜌⟩ ⊨ 𝜙,
                       𝛼ˆ = 𝑉 LΘM𝐻 ,     and 𝛼 ′ = ⌊𝜙⌋
                                                    ˜ ⟨𝐻, 𝛼\𝛼,ˆ 𝜌 ⟩

  Since the initial state is validated by Σ, Σ = ⟨𝜎, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′, 𝜙˜0 ⟩ for some 𝜎, 𝜙˜
where ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎.
94                                                                                                                Torek et al.


     The only guard rule that applies is SGuardWhile, so we have, for some 𝜎 ′ , 𝜎 ′′ , 𝑘, 𝑥 1, · · · , 𝑥𝑘 ,
𝑡 1, · · · , 𝑡𝑘 , and 𝑡,
                𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, R ′,       𝑥 1, · · · , 𝑥𝑘 = modified(𝑠), 𝑡 1 = fresh, · · · , 𝑡𝑘 = fresh,                 (39)
                              𝜎 [𝛾 = 𝛾 (𝜎 ) [𝑥 1 ↦→ 𝑡 1, · · · , 𝑥𝑘 ↦→ 𝑡𝑘 ]] ⊢ 𝜙˜ ◁ 𝜎 ′′,
                                ′              ′
                                                                                                                         (40)
                                         ′′
                                        𝜎 ⊢𝑒 ⇓𝑡 ⊣𝜎 , R ,  ′′′   ′′
                                                                         Θ = rem(𝜎 , 𝜙),
                                                                                     ˜  ′
                                                                                                                         (41)
                                                   ′       ′′                                       ′       ′′
                  and by assumptions 𝑉 (𝑔(𝜎 )) = true                             and   ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R ∪ R                (42)
where 𝑉 ′ is the corresponding valuation for these judgements (see definition 40).
  By lemma 23
                              ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R ′ and ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R ′′ .                                                     (43)
     Let 𝑡 1′ = fresh, · · · , 𝑡𝑘′ = fresh and 𝜎0 = ⟨⊥, ∅, ∅, 𝛾 (𝜎) [𝑥 1 ↦→ 𝑡 1′ , · · · , 𝑥𝑘 ↦→ 𝑡𝑘′ ], 𝑔(𝜎)⟩.
     Let 𝑉0 = 𝑉 ′ [𝑡 1′ ↦→ 𝜌 (𝑥 1 ), · · · , 𝑡𝑘′ ↦→ 𝜌 (𝑥𝑘 )]. Now, for any 𝑥 ∈ dom(𝛾 (𝜎0 )), if 𝑥 = 𝑥𝑖 for some
𝑖, then 𝑉0 (𝛾 (𝑥)) = 𝑉0 (𝛾 (𝜎0 ) (𝑥𝑖 )) = 𝑉0 (𝑡𝑖 ) = 𝜌 (𝑥𝑖 ) = 𝜌 (𝑥). Otherwise, 𝑥 ∈ dom(𝛾 (𝜎)) and thus
𝑉0 (𝛾 (𝜎) (𝑥)) = 𝑉 (𝛾 (𝜎) (𝑥)) = 𝜌 (𝑥) since 𝜌 𝑉 𝛾 (𝜎). Therefore 𝜌 𝑉 𝛾 (𝜎0 ).
                                                                           0
    Also, since H(𝜎0 ) = H (𝜎0 ) = ∅, ⟨𝐻, 𝛼 ′ \ T𝜙U ˜ ⟨𝐻, 𝜌 ⟩ ⟩   H(𝜎0 ) and ⟨𝐻, 𝛼 ′ \ T𝜙U
                                                                             𝑉0
                                                                                        ˜ ⟨𝐻, 𝜌 ⟩ ⟩ H (𝜎0 ).     𝑉0
Finally, 𝑉0 (𝑔(𝜎0 )) = 𝑉 (𝑔(𝜎)) = true since ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎.
  Therefore
                                     ⟨𝐻, 𝛼 ′ \ T𝜙U
                                                ˜ ⟨𝐻, 𝜌 ⟩ , 𝜌⟩
                                                               𝑉
                                                                 𝜎0
                                                                                   0

and then also ⟨𝐻, 𝛼 ′, 𝜌⟩     𝑉0
                                     𝜎0 by lemma 19.
  Furthermore, by assumptions, ⟨𝐻, 𝛼 \ 𝛼,     ˜ thus ⟨𝐻, 𝛼 ′, 𝜌⟩ ⊨ 𝜙˜ by lemma 13, since 𝛼 ′ =
                                       ˆ 𝜌⟩ ⊨ 𝜙,
 ˜
⌊𝜙⌋ ⟨𝐻, 𝛼\𝛼,ˆ 𝜌 ⟩ .
  Therefore, by lemma 32
                                        𝜎0 ⊢ 𝜙˜ ◁ 𝜎0′      and 𝑉0′ (𝑔(𝜎0′ )) = true
where 𝑉0′ = 𝑉0 [𝜎0 ⊢ 𝜙˜ ◁ 𝜎0′ | 𝐻, 𝜌]. Also, by lemma 31,
                                                       ⟨𝐻, 𝛼 ′, 𝜌⟩ 𝑉 ′ 𝜎0′ .
                                                                         0

     Now by lemma 27,
                                                       𝜎0′ ⊢ 𝑒 ⇓ 𝑡 0 ⊣ _, _
and let 𝑉0′′ = 𝑉0′ [𝜎0′ ⊢ 𝑒 ⇓ 𝑡 0 ⊣ _, _ | 𝐻, 𝜌].
  Let Σ0 = ⟨𝜎0′ [𝑔 = 𝑔(𝜎0′ ) && 𝑡 0 ], 𝑠 ′ ; skip, 𝜙⟩.
                                                   ˜
  We want to show that
               Γ ′ = ⟨𝐻, ⟨𝛼 ′, 𝜌, 𝑠; skip⟩ · ⟨𝛼 \ 𝛼 ′, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ ⟩ · S ∗ ⟩
is validated by Σ0 and 𝑉0′′ .
   Part 34.1: By SVerifyLoopBody Π ⊢ Σ → Σ0 . Therefore Σ0 is reachable from Π with valuation 𝑉0′′ .
   Part 34.2: By lemma 19 ⟨𝐻, 𝛼 ′ ∪ T𝑒U ⟨𝐻, 𝜌 ⟩ , 𝜌⟩ 𝑉 ′ 𝜎0′ . Then since ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ true, by lemma
                                                                     0
28 𝑉0′′ (𝑡 0 ) = true. Therefore 𝑉0′′ (𝑔(𝜎0′ ) && 𝑡 0 ) = 𝑉 ′ (𝑔(𝜎0′ )) ∧ 𝑉 ′ (𝑡 0′ ) = true. Thus, since we have
already shown ⟨𝐻, 𝛼 ′, 𝜌⟩ 𝑉 ′ 𝜎0′ ,
                                    0


                                          ⟨𝐻, 𝛼 ′, 𝜌⟩ 𝑉 ′′ 𝜎0′ [𝑔 = 𝑔(𝜎0′ ) && 𝑡 0 ].
                                                           0

     Also, 𝑠 (Σ0 ) = 𝑠; skip by definition. Therefore Γ ′ corresponds to Σ0 with 𝑉0′′ .
Gradually Verifying Unfolding Expressions & Pure Functions                                                               95


   Part 34.3: We want to show that the partial state
                          Γ ∗ = ⟨𝐻, ⟨𝛼 \ 𝛼 ′, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ ⟩ · S ∗ ⟩
is validated by Σ0 and 𝑉0′′ .
   By assumptions, ⟨𝐻, ⟨𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ ⟩ · S ∗ ⟩ was validated by Σ and 𝑉 .
Therefore the partial state ⟨𝐻, S ∗ ⟩ was validated by Σ and 𝑉 , Σ is reachable from Π with 𝑉 ,
𝑠 (Σ) = while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ , and ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 𝜎.
                                                                         ˜ ⟨𝐻, 𝜌 ⟩ , 𝜌⟩ ′ 𝜎 ′ .
   By (39) 𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, R and by (43) ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R. Therefore ⟨𝐻, 𝛼 \ T𝜙U                             𝑉
  Furthermore, since 𝛼ˆ = 𝑉 ′ LΘM𝐻 = 𝑉 ′ Lrem(𝜎 ′, 𝜙)M
                                                   ˜ 𝐻 , 𝛼 ′ = ⌊𝜙⌋
                                                                 ˜ ⟨𝐻, 𝛼\𝛼,ˆ 𝜌 ⟩ , and ⟨𝐻, 𝛼 \ 𝛼,     ˜ we
                                                                                               ˆ 𝜌⟩ ⊨ 𝜙,
can apply lemma 57 to get
                                       ⟨𝐻, 𝛼 \ 𝛼 ′, 𝜌⟩ 𝑉 ′ 𝜎 ′ .
   Finally, 𝜙˜ (Σ0 ) = 𝜙˜ by definition.
   Therefore Γ ∗ is validated by Σ0 and 𝑉0′′ since we have satisfied all requirements of case 33.3.
   Therefore Γ ′ is validated by Σ0 and 𝑉0′′ , which completes the proof.
   Case 11. ExecWhileSkip: We have
                ⟨𝐻, ⟨𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ ⟩ · S ∗ ⟩, 𝛼ˆ → ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · S ∗ ⟩
                  where 𝛼ˆ = 𝑉 ′ LΘM𝐻 ,          ⟨𝐻, 𝜌⟩ ⊢ 𝑒 ⇓ false,           ⟨𝐻, 𝛼, 𝜌⟩ ⊢frm 𝑒,      and
                                                           ˆ 𝜌⟩ ⊨ 𝜙˜
                                                   ⟨𝐻, 𝛼 \ 𝛼,
     Since the initial state is validated by Σ, Σ = ⟨𝜎, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′, 𝜙˜ ′ ⟩ for some 𝜎,
𝜙˜ ′ where ⟨𝐻, 𝛼, 𝜌⟩        𝑉
                               𝜎.
     The only guard rule that applies is SGuardWhile, so we have, for some 𝜎 ′ , 𝜎 ′′ , 𝑘, 𝑥 1, · · · , 𝑥𝑘 ,
𝑡 1, · · · , 𝑡𝑘 , and 𝑡,
                    𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, R ′, 𝑥 1, · · · , 𝑥𝑘 = modified(𝑠), 𝑡 1 = fresh, · · · , 𝑡𝑘 = fresh, (44)
                                𝜎 ′ [𝛾 = 𝛾 (𝜎 ′ ) [𝑥 1 ↦→ 𝑡 1, · · · , 𝑥𝑘 ↦→ 𝑡𝑘 ]] ⊢ 𝜙˜ ◁ 𝜎 ′′,                        (45)
                                      𝜎 ′′ ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′′′, R ′′, Θ = rem(𝜎 ′, 𝜙),     ˜                               (46)
                                                 ′      ′′                                        ′    ′′
                  and by assumptions 𝑉 (𝑔(𝜎 )) = true                        and   ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R ∪ R                   (47)
where 𝑉 ′ is the corresponding valuation for these judgements (see definition 40).
   Let Σ′ = ⟨𝜎 ′′ [𝑔 = 𝑔(𝜎 ′′ ) && ! 𝑡], 𝑠 ′, 𝜙˜ ′ ⟩.
   By SExecWhileSkip
                     𝜎 ⊢ while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ → 𝑠 ′ ⊣ 𝜎 ′′ [𝑔 = 𝑔(𝜎 ′′ ) && ! 𝑡].
Therefore by SVerifyStep Π ⊢ Σ → Σ′ . Thus Σ′ is reachable from Π with valuation 𝑉 ′ .
  By lemma 23
                              ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R ′ and ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R ′′ .                   (48)
                           ′′             ′           ′      ′
  By lemmas 34 and 29, 𝑔(𝜎 ) =⇒ 𝑔(𝜎 ). Therefore 𝑉 (𝑔(𝜎 )) = true. Now, by lemma 43,
                                                     ˜ ⟨𝐻, 𝛼 ⟩ , 𝜌⟩ ′ 𝜎 ′ .
                                            ⟨𝐻, 𝛼 \ T𝜙U            𝑉

   By definition 40, for all 1 ≤ 𝑖 ≤ 𝑘, 𝑉 ′ (𝑡𝑖 ) = 𝑉 (𝛾 (𝜎) (𝑥𝑖 )). By assumptions, 𝜌                      𝑉
                                                                                                                𝛾 (𝜎), thus
𝑉 (𝛾 (𝜎) (𝑥𝑖 )) = 𝜌 (𝑥𝑖 ). Also, as shown above, 𝜌 𝑉 ′           𝛾 (𝜎 ′ ).
    Let 𝛾 ′ = 𝛾 (𝜎 ′ ) [𝑥 1 ↦→ 𝑡 1, · · · , 𝑥𝑘 ↦→ 𝑡𝑘 ]. Now, for any 𝑥 ∈ dom(𝛾 ′ ), if 𝑥 = 𝑥𝑖 for some 𝑖 then
𝑉 (𝛾 ′ (𝑥)) = 𝑉 ′ (𝑡𝑖 ) = 𝜌 (𝑥𝑖 ). Otherwise, 𝑥 ∈ dom(𝛾 (𝜎 ′ )) and thus 𝑉 ′ (𝛾 ′ (𝑥)) = 𝑉 ′ (𝛾 (𝜎 ′ ) (𝑥)) = 𝜌 (𝑥).
  ′

Therefore 𝜌 𝑉 ′ 𝛾 ′ .
96                                                                                                                     Torek et al.


                        ˜ ⟨𝐻, 𝛼 ⟩ , 𝜌⟩ ′ 𝜎 ′ [𝛾 = 𝛾 ′ ]. Using the definition of 𝛾 ′ and (45), 𝜎 ′ [𝛾 = 𝛾 ′ ] ⊢
     Therefore ⟨𝐻, 𝛼 \ T𝜙U            𝑉
𝜙˜ ◁ 𝜎 ′′ , and by (47), 𝑉 ′ (𝑔(𝜎 ′′ )) = true.
   In addition, as shown before, ⟨𝐻, 𝛼 \ 𝛼,            ˜ thus by lemma 9 ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝜙.
                                                ˆ 𝜌⟩ ⊨ 𝜙,                            ˜
   Now by lemma 31, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′′ .
   In addition, by lemma 19, ⟨𝐻, 𝛼 ∪ T𝑒U ⟨𝐻, 𝜌 ⟩ , 𝜌⟩ 𝑉 ′ 𝜎 ′′ . Then, since 𝜎 ′′ ⊢ 𝑒 ⇓ 𝑡 ⊣ _, _ and ⟨𝐻, 𝜌⟩ ⊢
𝑒 ⇓ false, by lemma 28 𝑉 ′ (𝑡) = false. Therefore 𝑉 ′ (𝑔(𝜎 ′′ ) && ! 𝑡) = 𝑉 ′ (𝑔(𝜎 ′′ )) ∧ ¬𝑉 ′ (𝑡) = true.
Therefore
                                ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′′ [𝑔 = 𝑔(𝜎 ′′ ) && ! 𝑡].
  Now, by definition, 𝑠 (Σ′ ) = 𝑠 ′ . Therefore ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · S ∗ ⟩ corresponds to Σ′ with valuation 𝑉 ′ .
  By definition 𝜙˜ (Σ′ ) = 𝜙˜ ′ = 𝜙˜ (Σ). Also, 𝛾 (Σ′ ) = 𝛾 (𝜎 ′′ ) = 𝛾 (𝜎 ′ ) [𝑥 1 ↦→ 𝑡 1, · · · , 𝑥𝑘 ↦→ 𝑡𝑘 ] by lemma
30 and 𝛾 (𝜎 ′ ) = 𝛾 (𝜎) = 𝛾 (Σ) by lemma 37. Therefore dom(𝛾 (Σ′ )) ⊇ dom(𝛾 (Σ)).
  Thus by lemma 47 ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · S ∗ ⟩ is a valid state.
  Case 12. ExecWhileFinish: We have
                   ⟨𝐻, ⟨𝛼 ′, 𝜌 ′, skip⟩ · ⟨𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ ⟩ · S ∗ ⟩ →
                      ⟨𝐻, ⟨𝛼 ′′, 𝜌 ′, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ ⟩ · S ∗ ⟩
                    where ⟨𝐻, 𝛼 ′, 𝜌 ′ ⟩ ⊨ 𝜙˜ and 𝛼 ′′ = 𝛼 ∪ ⌊𝜙⌋  ˜ ⟨𝐻, 𝛼 ′ , 𝜌 ′ ⟩ .

   By assumptions, the initial state is validated by some Σ and valuation 𝑉 ′ , thus Σ′ = ⟨𝜎 ′, skip, 𝜙˜ ′ ⟩
for some 𝜎 ′ , 𝜙˜ where ⟨𝐻, 𝛼 ′, 𝜌 ′ ⟩ 𝑉 𝜎 ′ .
   Also, by 34.3, the partial state ⟨𝐻, ⟨𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ ⟩ · S ∗ ⟩ is validated by Σ′
and 𝑉 ′ . Thus 33.3 must apply, and thus there is some Σ0 , 𝑉0 , 𝜎0 , 𝜎0′ , 𝜙˜0 such that
                                  Σ0 = ⟨𝜎0, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′, 𝜙˜0 ⟩
                                    Σ0 is reachable from Π with valuation 𝑉0
                                  𝜎0 ⊢ 𝜙˜ ▷ 𝜎0′ , _,    ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎0′ ,      𝜙˜ ′ = 𝜙,
                                                                                         ˜
                                                                        0

                                        and 𝑉0′ = 𝑉0 [𝜎 ⊢ 𝜙˜ ▷ 𝜎 ′, _ | 𝐻 ].
  We have ⟨𝐻, 𝛼 ′, 𝜌 ′ ⟩ ⊨ 𝜙,                     ˜ ⟨𝐻, 𝛼 ′ , 𝜌 ′ ⟩ , 𝜌 ′ ⟩ ⊨ 𝜙,
                           ˜ thus by lemma 13⟨𝐻, ⌊𝜙⌋                          ˜ and then by lemma 9
     ′′  ′    ˜
⟨𝐻, 𝛼 , 𝜌 ⟩ ⊨ 𝜙.
  Also by lemma 19 ⟨𝐻, 𝛼 ′′, 𝜌⟩ 𝑉 ′ 𝜎0′ .
                                           0
   For some 𝑘, let 𝑥 1, · · · , 𝑥𝑘 be the list of variables in modified(𝑠). Let 𝑡 1 = fresh, · · · , 𝑡𝑘 = fresh, let
𝛾ˆ = 𝛾 (𝜎0 ) [𝑥 1 ↦→ 𝑡 1, · · · , 𝑥𝑘 ↦→ 𝑡𝑘 ], and let 𝑉ˆ0′ = 𝑉0′ [𝑡 1 ↦→ 𝜌 ′ (𝑥 1 ), · · · , 𝑡𝑘 ↦→ 𝜌 ′ (𝑥𝑘 )].
   𝜌 ′ is contained in the stack frame executing the loop body, which is 𝑠, thus for all 𝑥 ∈ dom(𝜌 ′ ),
either 𝜌 (𝑥) = 𝜌 ′ (𝑥) or 𝑥 ∈ modified(𝑚).
   Also, since 𝜌 𝑉 ′ 𝛾 (𝜎0′ ) and 𝛾 (𝜎0′ ) = 𝛾 (𝜎0 ) by lemma 37, 𝜌 𝑉 𝛾 (𝜎0 ).
                       0                                                           0

   Now, for any 𝑥 ∈ dom(𝛾),         ˆ if 𝑥 = 𝑥𝑖 for some 𝑖, then 𝑉ˆ0′ (𝛾ˆ (𝑥)) = 𝑉ˆ0′ (𝛾ˆ (𝑥𝑖 )) = 𝜌 ′ (𝑥𝑖 ) = 𝜌 ′ (𝑥). Oth-
erwise, 𝑥 ∉ modified(𝑠), thus 𝜌 ′ (𝑥) = 𝜌 (𝑥), and 𝑥 ∈ dom(𝛾 (𝜎0 )). Thus 𝑉ˆ ′ (𝛾ˆ (𝑥)) = 𝑉0 (𝛾 (𝜎0 ) (𝑥)) =
                                                                                                 0
𝜌 (𝑥) = 𝜌 ′ (𝑥𝑖 ) since 𝜌 𝑉 𝛾 (𝜎0 ). Therefore 𝜌 ′               ˆ Thus ⟨𝐻, 𝛼 ′′, 𝜌 ′ ⟩
                                                                 𝛾.                                  𝜎0′ [𝛾 = 𝛾 ′ ].
                              0                           𝑉ˆ0′                            𝑉ˆ0′
   Therefore by lemma 32 𝜎0′ [𝛾 = 𝛾 ′ ] ⊢ 𝜙˜ ◁ 𝜎0′′ for some 𝜎0′′ such that 𝑉0′′ (𝑔(𝜎0′′ )) = true where
𝑉0′′ = 𝑉ˆ0′ [𝜎0′ ⊢ 𝜙˜ ◁ 𝜎0′′ | 𝐻 ].
   Let Σ′0 = ⟨𝜎0′′, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′, 𝜙˜0 ⟩. We want to show that
                           Γ ′ = ⟨𝐻, ⟨𝛼 ′′, 𝜌 ′, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ ⟩ · S ∗ ⟩
Gradually Verifying Unfolding Expressions & Pure Functions                                                                 97


is validated by Σ′0 and 𝑉0′′ .
    Part 34.1: By SVerifyLoop, and since Σ0 is reachable from Π, Π ⊢ Σ0 → Σ′0 . Therefore Σ′0 is
reachable from Π with valuation 𝑉0′′ .
    Part 34.2: Since ⟨𝐻, 𝛼 ′, 𝜌 ′ ⟩ ⊨ 𝜙,             ˜ ⟨𝐻, 𝜌 ′ ⟩ ⊆ 𝛼 ′ . Also, since the stack is well-formed,
                                       ˜ by lemma 4 T𝜙U
  ′                                   ˜
𝛼 and 𝛼 are disjoint, thus 𝛼 \ T𝜙U ⟨𝐻, 𝜌 ′ ⟩ = 𝛼. Therefore ⟨𝐻, 𝛼 \ T𝜙U    ˜ ⟨𝐻, 𝜌 ′ ⟩ , 𝜌⟩ ′ 𝜎 ′ , and now since
                                                                                           𝑉   0
                                                                                                               0
𝛼 ⊆ 𝛼 ′′ , by lemma 19, and since 𝜌 ′                𝛾 ′,
                                              𝑉ˆ0′


                                      ⟨𝐻, 𝛼 ′′ \ T𝜙U
                                                  ˜ ⟨𝐻, 𝜌 ′ ⟩ , 𝜌 ′ ⟩               𝜎0′ [𝛾 = 𝛾 ′ ].
                                                                             𝑉ˆ0′


   Now, by lemma 31,

                                                     ⟨𝐻, 𝛼 ′′, 𝜌 ′ ⟩ 𝑉 ′′ 𝜎0′′ .
                                                                         0


   Also, 𝑠 (Σ′0 ) = 𝑠 (Γ ′ ) by construction. Therefore Γ ′ corresponds to Σ′0 .
   Part 34.3: We need to show that the partial state ⟨𝐻, S ∗ ⟩ is validated by Σ′0 and 𝑉0′′ . We already
have that ⟨𝐻, S ∗ ⟩ is validated by Σ0 and 𝑉0 . Thus one of 33.1, 33.2, or 33.3 must apply.
   If 33.1 applies: Then S ∗ = nil, thus trivially the partial state ⟨𝐻, S ∗ ⟩ is validated by Σ′0 and 𝑉0′′ .
   If 33.2 applies: Then S ∗ = ⟨𝛼 ∗, 𝜌 ∗, 𝑦 = 𝑚(𝑒 1, · · · , 𝑒𝑘 ); 𝑠 ∗ ⟩ · S1∗ for some 𝛼 ∗ , 𝜌 ∗ , 𝑘, 𝑦, 𝑚, 𝑒 1, · · · , 𝑒𝑘 ,
𝑠 , S1∗ . Also, there exists some Σ∗ , 𝑉 ∗ , 𝑥 1, · · · , 𝑥𝑘 , 𝑡 1, · · · , 𝑡𝑘 , 𝜎0, · · · , 𝜎𝑘 , 𝜎 ′ such that
 ∗



                             The partial state ⟨𝐻, S1∗ ⟩ is validated by Σ∗ and 𝑉 ∗,
                        Σ∗ is reachable from Π with valuation 𝑉 ∗,                           𝑠 (Σ∗ ) = 𝑠 (S ∗ ),
                                               𝑥 1, · · · , 𝑥𝑘 = params(𝑚),
                                ∗
                     𝜎0 = 𝜎 (Σ ),      𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, _,           ··· ,        𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,
                                                     ′
                            𝜎𝑘 ⊢ pre(𝑚) ▷ 𝜎 , _,             ⟨𝐻, 𝛼 , 𝜌 ⟩ 𝑉 ∗ 𝜎 ′ [𝛾 = 𝛾 (𝜎0 )],
                                                                     ∗        ∗

                                    ∀ 1 ≤ 𝑖 ≤ 𝑘 : 𝑉0 (𝛾 (Σ0 ) (𝑥𝑖 )) = 𝑉 ∗ (𝑡𝑖 ),               and
                                                  𝜙˜ (Σ0 ) = post(𝑚).

  We want to show that the partial state ⟨𝐻, S ∗ ⟩ is validated by Σ′′ and 𝑉 ′′ . Immediately from
above,

                             The partial state ⟨𝐻, S1∗ ⟩ is validated by Σ∗ and 𝑉 ∗,
                        Σ∗ is reachable from Π with valuation 𝑉 ∗,                           𝑠 (Σ∗ ) = 𝑠 (S ∗ ),
                                               𝑥 1, · · · , 𝑥𝑘 = params(𝑚),
                                ∗
                     𝜎0 = 𝜎 (Σ ),      𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, _,           ··· ,        𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,
                                                     ′
                            𝜎𝑘 ⊢ pre(𝑚) ▷ 𝜎 , _,             ⟨𝐻, 𝛼 , 𝜌 ⟩ 𝑉 ∗ 𝜎 ′ [𝛾 = 𝛾 (𝜎0 )].
                                                                     ∗        ∗



Also, the frame ⟨𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ ⟩ must be executing the body of 𝑚, since
it is in the stack immediately above the frame that contains 𝑦 = 𝑚(𝑒 1, · · · , 𝑒𝑘 ). Therefore, since
𝑥 1, · · · , 𝑥𝑘 are all parameters of 𝑚, modified(𝑠) cannot contain any of 𝑥 1, · · · , 𝑥𝑘 , since we do not
98                                                                                                                Torek et al.


allow assignment to parameters in a well-formed program. Thus

                ∀1 ≤ 𝑖 ≤ 𝑘 : 𝑉0′′ (𝛾 (Σ′0 ) (𝑥𝑖 )) = 𝑉0′′ (𝛾 (𝜎0′′ )(𝑥𝑖 ))                            defn. Σ′0
                                                   = 𝑉0′′ (𝛾ˆ (𝑥𝑖 ))                               Lemma 30
                                                   = 𝑉0′′ (𝛾 (𝜎0′ ) (𝑥𝑖 ))                 𝑥𝑖 ∉ modified(𝑠)
                                                   = 𝑉0′′ (𝛾 (𝜎0 ) (𝑥𝑖 ))                          Lemma 37
                                                   = 𝑉0 (𝛾 (𝜎0 ) (𝑥𝑖 ))                              𝑉0 ⊆ 𝑉0′′
                                                   = 𝑉 ∗ (𝑡𝑖 )                                  prev. assump.

     Finally, 𝜙˜ (Σ′0 ) = 𝜙˜ (Σ0 ) by definition, thus

                                              𝜙˜ (Σ′0 ) = 𝜙˜ (Σ0 ) = post(𝑚).

   Therefore the partial state ⟨𝐻, S ∗ ⟩ is validated by Σ′0 and 𝑉0′′ in this case.
   If 33.3 applies: Then S ∗ = ⟨𝜌 ∗, 𝛼 ∗, while 𝑒 ∗ invariant 𝜙˜∗ do 𝑠 ∗ ; 𝑠 ∗′ ⟩ · S1∗ for some 𝜌 ∗ , 𝛼 ∗ , 𝑒 ∗ , 𝜙˜∗ ,
𝑠 , 𝑠 ∗′ , S1∗ , and there exists some Σ∗ , 𝑉 ∗ , and 𝜎 ′ such that:
 ∗


                              The partial state ⟨𝐻, S1∗ ⟩ is validated by Σ∗ and 𝑉 ∗
                         Σ∗ is reachable from Π with valuation 𝑉 ∗                  𝑠 (Σ∗ ) = 𝑠 (S ∗ ),
                                 𝜎 (Σ∗ ) ⊢ 𝜙˜∗ ▷ 𝜎 ′, _,         ⟨𝐻, 𝛼 ∗, 𝜌 ∗ ⟩ 𝑉 ∗ 𝜎 ′   and
                                                             ∗         ˜∗
                                                       𝜙˜ (Σ ) = 𝜙 .

   Now, by definition of Σ′0 , 𝜙˜ (Σ′0 ) = 𝜙˜ (Σ0 ) = 𝜙˜∗ . Therefore, using the other assumptions given
above, the partial state ⟨𝐻, S ∗ ⟩ is validated by Σ′0 and 𝑉0′′ in this case.
   Therefore definition part 34.3 is satisfied.
   Therefore all parts of definition 34 are satisfied. Thus Γ ′ is validated by Σ′0 and 𝑉0′′ , as we wanted
to show.
   Case 13. ExecFold: We have

                        ⟨𝐻, ⟨𝛼, 𝜌, fold 𝑝 (𝑒); 𝑠⟩ · S ∗ ⟩, 𝑉 ′ LΘM𝐻 → ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · S ∗ ⟩

  By assumptions, the initial state is validated by some Σ and valuation 𝑉 ′ , thus
Σ = ⟨𝜎, fold 𝑝 (𝑒); 𝑠, 𝜙⟩
                       ˜ for some 𝜎, 𝜙˜ where ⟨𝐻, 𝛼, 𝜌⟩
                                                         𝑉
                                                            𝜎.
  The only guard that applies is SGuardFold, thus we have

                                 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R,       𝑥 = predicate_params(𝑝),
                                   𝜎 [𝛾 = [𝑥𝑖 ↦→ 𝑡𝑖 ]] ⊢ predicate(𝑝) ▷ 𝜎 ′′, R ′,
                                     ′

                   and by assumptions           ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R ∪ R ′           and 𝑉 ′ (𝑔(𝜎 ′′ )) = true

where 𝑉 ′ is the valuation corresponding to this series of judgements, extending 𝑉 (see definition
40).
  Let 𝑒 1, · · · , 𝑒𝑛 = 𝑒, 𝑡 1, · · · , 𝑡𝑛 = 𝑡, and R 1, · · · , R𝑛 = R. Let 𝜎0 , then for some 𝜎1, · · · , 𝜎𝑛 we have

                                𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, R 1, · · · , 𝜎𝑛−1 ⊢ 𝑒𝑛 ⇓ 𝑡𝑛 ⊣ 𝜎𝑛 , R𝑛

where 𝜎𝑛 = 𝜎 ′ . By lemmas 24 and 34 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎𝑛 ) =⇒ · · · =⇒ 𝑔(𝜎1 ). Therefore
𝑉 ′ (𝑔(𝜎 ′′ )) = 𝑉 ′ (𝑔(𝜎𝑛 )) = · · · = 𝑉 ′ (𝑔(𝜎1 )) = true. Also, by lemma 23 we have ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R𝑖 for
Gradually Verifying Unfolding Expressions & Pure Functions                                                99


all 1 ≤ 𝑖 ≤ 𝑛. Thus, by lemma 26
                           ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ 𝑉 ′ (𝑡 1 ),       ··· ,      ⟨𝐻, 𝜌⟩ ⊢ 𝑒𝑛 ⇓ 𝑉 ′ (𝑡𝑛 )
                            and    ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎1,           ··· ,      ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎𝑛 .

Therefore ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ .
   Let 𝛾 ′ = [𝑥 ↦→ 𝑡] and 𝜌 ′ = [𝑥 ↦→ 𝑉 ′ (𝑡)]. Then, by construction, 𝜌 ′ 𝑉 ′ 𝛾 ′ . Therefore ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′
𝜎 ′ [𝛾 = 𝛾 ′ ].
  From above we have 𝜎 ′ [𝛾 = 𝛾 ′ ] ⊢ predicate(𝑝) ▷ 𝜎 ′′, R ′ and ⟨𝛼, 𝜌⟩ ⊢𝐻 R ′′ by lemma 23. Thus,
by lemma 43 ⟨𝐻, 𝛼 \ Tpredicate(𝑝)U ⟨𝐻, 𝜌 ′ ⟩ , 𝜌 ′ ⟩ 𝑉 ′ 𝜎 ′′ and thus

                           ⟨𝐻, 𝛼 \ Tpredicate(𝑝)U ⟨𝐻, 𝜌 ′ ⟩ , 𝜌⟩ 𝑉 ′ 𝜎 ′′ [𝛾 = 𝛾 (𝜎)].
   Let H′ = H(𝜎 ′′ ); ⟨𝑝, 𝑡⟩. Expanding definitions,
                                    𝑉 ′ L⟨𝑝, 𝑡⟩M𝐻 = Tpredicate(𝑝)U ⟨𝐻, 𝜌 ′ ⟩ .
Now ⟨𝐻, 𝛼 \ 𝑉 ′ L⟨𝑝, 𝑡⟩M𝐻 , 𝜌⟩ 𝑉 ′ 𝜎 ′′ [𝛾 = 𝛾 (𝜎)], thus
                        ∀ ℎ 1, ℎ 2 ∈ H(𝜎 ′′ ) : ℎ 1 ≠ ℎ 2 =⇒ 𝑉 ′ Lℎ 1 M𝐻 ∩ 𝑉 ′ Lℎ 2 M𝐻 = ∅
and by lemma 16,
                          ∀ ℎ ∈ H(𝜎 ′′ ) : 𝑉 ′ LℎM𝐻 ∩ 𝑉 ′ L⟨𝑝, 𝑡⟩M𝐻 = ∅.
From these we can deduce that
                          ∀ ℎ 1, ℎ 2 ∈ H′ : ℎ 1 ≠ ℎ 2 =⇒ 𝑉 ′ Lℎ 1 M𝐻 ∩ 𝑉 ′ Lℎ 2 M𝐻 = ∅.
   Also, from lemma 43, ⟨𝐻, 𝛼, [𝑥 ↦→ 𝑉 ′ (𝑡)]⟩ ⊨ predicate(𝑝) since 𝜌 ′ = [𝑥 ↦→ 𝑉 ′ (𝑡)].
   Since ⟨𝐻, 𝛼 \ 𝑉 ′ L⟨𝑝, 𝑡⟩M𝐻 , 𝜌⟩ 𝑉 ′ 𝜎 ′′ [𝛾 = 𝛾 (𝜎)],

                         ∀ ⟨𝑝, 𝑡⟩ ∈ H(𝜎 ′′ ) : ⟨𝐻, 𝛼, [𝑥 ↦→ 𝑉 ′ (𝑡)]⟩ ⊨ predicate(𝑝).
From these we can deduce that
                           ∀ ⟨𝑝, 𝑡⟩ ∈ H′ : ⟨𝐻, 𝛼, [𝑥 ↦→ 𝑉 ′ (𝑡)]⟩ ⊨ predicate(𝑝).
   Since field values are unchanged between H(𝜎 ′′ ) and H′ ,
                                   ∀ ⟨𝑓 , 𝑡, 𝑡 ′ ⟩ ∈ H′ : ⟨𝑉 (𝑡), 𝑓 ⟩ ∈ 𝛼         and
                                   ∀ ⟨𝑓 , 𝑡, 𝑡 ⟩ ∈ H : 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ ).
                                              ′         ′


   Therefore ⟨𝐻, 𝛼⟩ 𝑉 ′ H′ , and thus

                                    ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′′ [𝛾 = 𝛾 (𝜎), H = H′ ].

   Let Σ′ = ⟨𝜎 ′′ [𝛾 = 𝛾 (𝜎), H = H′ ], 𝑠, 𝜙⟩.
                                             ˜ By SExecFold 𝜎 ⊢ fold 𝑝 (𝑒); 𝑠 → 𝑠 ⊣ 𝜎 (Σ′ ) (after
expanding definitions). Therefore Π ⊢ Σ → Σ′ by SVerifyStep. Therefore Σ′ is reachable from Π
with valuation 𝑉 ′ .
   Also, as shown before, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 (Σ′ ), and by definition 𝑠 (Σ′ ) = 𝑠. Therefore Σ′ corresponds
to ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · S ∗ ⟩.
   By definition 𝛾 (Σ′ ) = 𝛾 (𝜎) = 𝛾 (Σ) and 𝜙˜ (Σ′ ) = 𝜙˜ = 𝜙˜ (Σ). Therefore by lemma 47 ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ ·
  ∗
S ⟩ is a valid state.
   Case 14. ExecUnfold: We have
                    ⟨𝐻, ⟨𝛼, 𝜌, unfold 𝑝 (𝑒); 𝑠⟩ · S ∗ ⟩, 𝑉 ′ LΘM𝐻 → ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ · S ∗ ⟩
100                                                                                                           Torek et al.


  By assumptions, the initial state is validated by some Σ and valuation 𝑉 ′ , thus
Σ = ⟨𝜎, unfold 𝑝 (𝑒); 𝑠, 𝜙⟩
                         ˜ for some 𝜎, 𝜙˜ where ⟨𝐻, 𝛼, 𝜌⟩
                                                            𝑉
                                                              𝜎.
  The only guard that applies is SGuardUnfold, thus we have The only guard that applies is
SGuardFold, thus we have
                                     𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R,   𝜎 ′ ⊢ 𝑝 (𝑒) ▷ 𝜎 ′′, R ′,
                                                               Ø
                  and by assumptions         ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R ′ ∪      R and 𝑉 ′ (𝑔(𝜎 ′′ )) = true

     Let 𝑒 1, · · · , 𝑒𝑛 = 𝑒, 𝑡 1, · · · , 𝑡𝑛 = 𝑡, and R 1, · · · , R𝑛 = R. Let 𝜎0 , then for some 𝜎1, · · · , 𝜎𝑛 we have
                                𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, R 1, · · · , 𝜎𝑛−1 ⊢ 𝑒𝑛 ⇓ 𝑡𝑛 ⊣ 𝜎𝑛 , R𝑛
where 𝜎𝑛 = 𝜎 ′ . By lemmas 24 and 34 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎𝑛 ) =⇒ · · · =⇒ 𝑔(𝜎1 ). Therefore
𝑉 ′ (𝑔(𝜎 ′′ )) = 𝑉 ′ (𝑔(𝜎𝑛 )) = · · · = 𝑉 ′ (𝑔(𝜎1 )) = true. Also, by lemma 23 we have ⟨𝐻, 𝛼⟩ ⊢𝑉 ′ R𝑖 for
all 1 ≤ 𝑖 ≤ 𝑛. Thus, by lemma 26
                              ⟨𝐻, 𝜌⟩ ⊢ 𝑒 1 ⇓ 𝑉 ′ (𝑡 1 ),   ··· ,       ⟨𝐻, 𝜌⟩ ⊢ 𝑒𝑛 ⇓ 𝑉 ′ (𝑡𝑛 )
                               and     ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎1,       ··· ,      ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎𝑛 .

Therefore ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′ 𝜎 ′ .
  Thus by lemma 43
                            ⟨𝐻, 𝜌, 𝛼⟩ ⊨ 𝑝 (𝑒)      and     ⟨𝐻, 𝛼 \ T𝑝 (𝑒)U ⟨𝐻, 𝜌 ⟩ , .⟩ 𝑉 ′ 𝜎 ′

     Let 𝑥 = predicate_params(𝑝), 𝛾 ′ = [𝑥 ↦→ 𝑡], and 𝜌 ′ = [𝑥 ↦→ 𝑉 ′ (𝑡)]. Then, by construction,
𝜌′    𝑉′
         𝛾 ′ . Therefore ⟨𝐻, 𝛼 \ T𝑝 (𝑒)U ⟨𝐻, 𝜌 ⟩ , 𝜌 ′ ⟩ 𝑉 ′ 𝜎 ′ [𝛾 = 𝛾 ′ ].
                                                                             Ð
     Now, by definition, T𝑝 (𝑒)U ⟨𝐻, 𝜌 ⟩ = Tpredicate(𝑝)U ⟨𝐻, 𝜌 ′ ⟩ ∪ T𝑒U ⟨𝐻, 𝜌 ⟩ .
     Therefore Tpredicate(𝑝)U ⟨𝐻, 𝜌 ′ ⟩ ⊆ 𝛼 \ T𝑝 (𝑒)U ⟨𝐻, 𝜌 ⟩ , thus by lemma 19,
                                ⟨𝐻, 𝛼 \ Tpredicate(𝑝)U ⟨𝐻, 𝜌 ′ ⟩ , 𝜌 ′ ⟩ 𝑉 ′ 𝜎 ′ [𝛾 = 𝛾 ′ ]

and ⟨𝜎 ′ [𝛾 = 𝛾 ′ ], 𝐻, 𝛼⟩ 𝑉 ′ 𝜎𝜌 ′ .
  Since ⟨𝐻, 𝛼, 𝜌⟩ ⊨ 𝑝 (𝑒), by AssertPredicate ⟨𝐻, 𝛼, 𝜌 ′ ⟩ ⊨ predicate(𝑝).
  Therefore by lemma 32
                         𝜎 ′ [𝛾 = 𝛾 ′ ] ⊢ predicate(𝑝) ◁ 𝜎 ′′      and 𝑉 ′′ (𝑔(𝜎 ′′ )) = true
where 𝑉 ′′ = 𝑉 ′ [𝜎 ′ [𝛾 = 𝛾 ′ ] ⊢ predicate(𝑝) ◁ 𝜎 ′′ | 𝐻 ]. Also, by lemma 31 ⟨𝐻, 𝛼, 𝜌 ′ ⟩ 𝑉 ′′ 𝜎 ′′ , and
thus
                                       ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′′ 𝜎 ′′ [𝛾 = 𝛾 (𝜎)].
  Now, by SExecUnfold, 𝜎 ⊢ unfold 𝑝 (𝑒); 𝑠 → 𝑠 ⊣ 𝜎 ′′ [𝛾 = 𝛾 (𝜎)].
  Let Σ′ = ⟨𝜎 ′′ [𝛾 = 𝛾 (𝜎)], 𝑠, 𝜙⟩.
                                 ˜ By SVerifyStep Π ⊢ Σ → Σ′ . Therefore Σ′ is reachable from Π
with valuation 𝑉 .′′

  Also, as shown before, ⟨𝐻, 𝛼, 𝜌⟩ 𝑉 ′′ 𝜎 (Σ′ ). Furthermore, 𝑠 (Σ′ ) = 𝑠 by definition. Thus ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩·
S ⟩ corresponds to Σ′ with valuation 𝑉 ′′ .
 ∗

  By definition 𝛾 (Σ′ ) = 𝛾 (𝜎) = 𝛾 (Σ) and 𝜙˜ (Σ′ ) = 𝜙˜ = 𝜙˜ (Σ). Therefore, by lemma 47 ⟨𝐻, ⟨𝛼, 𝜌, 𝑠⟩ ·
 ∗
S ⟩ is a valid state.
                                                                                                        □
Theorem 3 (Preservation). Let Γ be some dynamic state validated by the Σ and valuation 𝑉 for
some program Π. If Σ ⇀ 𝜎 ′ ⊣ R, Θ with corresponding valuation 𝑉 extending 𝑉 ′ , 𝑉 ′ (𝑔(𝜎 ′ )) = true,
⟨𝐻, 𝛼 (Γ)⟩ ⊢𝑉 ′ R, and Π ⊢ 𝑉 ′ LΘM𝐻 (Γ) , Γ → Γ ′ then Γ ′ is a valid state.
Gradually Verifying Unfolding Expressions & Pure Functions                                                        101


  In other words, if the dynamic state satisfies the matching symbolic checks, and dynamic
execution procedes, then the resulting state is valid.
   Proof. We proceed by cases on the judgement Π ⊢ 𝑉 ′ LΘM𝐻 (Γ) , Γ → Γ ′ .
   Case 1. ExecInit: Then Γ = init and Γ ′ = ⟨∅, ⟨∅, ∅, 𝑠 (Π)⟩ · nil⟩. Since Γ is validated by Σ, then
Σ = init.
   Let Σ′ = ⟨⟨⊥, ∅, ∅, ∅, true⟩, 𝑠 (Π), true⟩. Then by SVerifyInit Π ⊢ init → Σ′ .
   Since Γ ′ has a stack with a sole stack frame, and clearly Σ′ is reachable from Π, in order to
show that Γ ′ is validated by Σ′ it suffices to show that Γ ′ corresponds to Σ′ . In turn, since clearly
𝑠 (Γ ′ ) = 𝑠 (Σ′ ), it suffices to show that ⟨𝐻 (Γ ′ ), 𝛼 (Γ ′ ), 𝜌 (Γ ′ )⟩ 𝑉 𝜎 (Σ′ ). Since all the requisite sets or
values are trivial, this is immediate from the definition.
   Case 2. ExecFinal: Then Γ ′ = final and Γ = ⟨𝐻, ⟨𝛼, 𝜌, skip⟩ · nil⟩. Since Γ is validated by Σ,
𝑠 (Γ) = 𝑠 (Σ) = skip. By lemma 45, 𝜎 (Σ) ⊢ 𝜙˜ (Σ) ▷ 𝜎 ′, _ for some 𝜎 ′ . Thus Π ⊢ Σ → final by
SVerifyFinal.
   Case 3. ExecStep: Then Γ = ⟨𝐻, S⟩ and Γ ′ = ⟨𝐻 ′, S ′ ⟩ for some 𝐻, S, 𝐻 ′, S ′ where
⟨𝐻, S⟩, 𝑉 ′ LΘM𝐻 → ⟨𝐻 ′, S ′ ⟩. Therefore Γ ′ is a valid state by lemma 58.
                                                                                                                    □

Received 9 July 2026
