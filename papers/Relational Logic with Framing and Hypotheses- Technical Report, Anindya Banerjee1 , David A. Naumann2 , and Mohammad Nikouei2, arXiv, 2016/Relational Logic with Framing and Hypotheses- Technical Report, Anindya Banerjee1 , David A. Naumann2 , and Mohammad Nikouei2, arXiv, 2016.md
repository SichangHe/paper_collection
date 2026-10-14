                                         Relational logic with framing and hypotheses:
                                         technical report∗
                                         Anindya Banerjee1 , David A. Naumann2 , and Mohammad Nikouei2

                                         1        IMDEA Software Institute
                                         2        Stevens Institute of Technology



                                                  Abstract
                                         Relational properties arise in many settings: relating two versions of a program that use dif-
                                         ferent data representations, noninterference properties for security, etc. The main ingredient of
                                         relational verification, relating aligned pairs of intermediate steps, has been used in numerous
arXiv:1611.08992v1 [cs.LO] 28 Nov 2016




                                         guises, but existing relational program logics are narrow in scope. This paper introduces a logic
                                         based on novel syntax that weaves together product programs to express alignment of control
                                         flow points at which relational formulas are asserted. Correctness judgments feature hypotheses
                                         with relational specifications, discharged by a rule for the linking of procedure implementations.
                                         The logic supports reasoning about program-pairs containing both similar and dissimilar control
                                         and data structures. Reasoning about dynamically allocated objects is supported by a frame rule
                                         based on frame conditions amenable to SMT provers. We prove soundness and sketch how the
                                         logic can be used for data abstraction, loop optimizations, and secure information flow.

                                         Digital Object Identifier 10.4230/LIPIcs...


                                             1     Introduction
                                         Relational properties are ubiquitous. Compiler optimizations, changes of data representation,
                                         and refactoring involve two different programs. Non-interference (secure information flow)
                                         is a non-functional property of a single program; it says the program preserves a “low
                                         indistinguishability” relation [45]. Many recent works deal with one or more of these
                                         applications, using relational logic and/or some form of product construction that reduces
                                         the problem to partial correctness, though mostly for simple imperative programs. This
                                         paper advances extant work by providing a relational logic for local reasoning about heap
                                         data structures and programs with procedures.
                                             To set the stage, first consider the two simple imperative programs:

                                          b x := 1; while y > 0 do x := x ∗ y; y := y − 1 od
                                         C=

                                         C0 =
                                            b x := 1; y := y − 1; while y ≥ 0 do x := x ∗ y + x; y := y − 1 od

                                         Both C and C 0 change x to be the factorial of the initial value of y, or to 1 if y is initially
                                         negative. For a context where y is known to be positive and its final value is not used, we
                                         could reason that they are interchangeable by showing both

                                                 C : y = z ∧ y ≥ 0 ; x = z! and            C 0 : y = z ∧ y ≥ 0 ; x = z!                        (1)


                                         ∗
                                             Banerjee was partially supported by the US National Science Foundation (NSF). Naumann and
                                             Nikouei were partially supported by NSF award 1228930. Any opinion, findings, and conclusions or
                                             recommendations expressed in the material are those of the authors and do not necessarily reflect the
                                             views of NSF.
                                                      © Anindya Banerjee, David A. Naumann, Mohammad Nikouei;
                                                      licensed under Creative Commons License CC-BY
                                                             Leibniz International Proceedings in Informatics
                                                             Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl Publishing, Germany
XX:2   Relational logic with framing and hypotheses (Technical Report)


       This is our notation for partial correctness judgments, with evident pre- and postconditions,
       for C and C 0 . It is not always easy to express and prove functional correctness, which
       motivates a less well developed approach to showing interchangeability of the examples. The
       two programs have a relational property which we write as

           (C|C 0 ) : B(y ≥ 0) ∧ y =
                                   ¨ y ≈> x =
                                            ¨ x                                                        (2)

       This relational correctness judgment says that a pair of terminating executions of C and C 0 ,
       from a pair of states which both satisfy y ≥ 0 and which agree on the value of y, yields a
       pair of final states that agree on the value of x. The relational formula x = ¨ x says that the
       value of x in the left state is the same as its value in the right state.
           Property (2) is a consequence of functional correctness (1), but there is a direct way to
       prove it. Any pair of runs, from states that agree on y, can be aligned in such a way that
       both x = ¨ x and y =¨ y + 1 hold at the aligned pairs of intermediate states. The alignment is
       almost but not quite step by step, owing to the additional assignment in C 0 . The relational
       property is more complicated than partial correctness, in that it involves pairs of runs. On
       the other hand the requisite intermediate assertions are much simpler; they do not involve !
       which is recursively defined. Prior work showed such assertions are amenable to automated
       inference (see Section 7).
           Despite the ubiquity of relational properties and recent logic-based or product-based
       approaches to reasoning with them (see Section 7), simple heap-manipulating examples like
       the following remain out of reach:

       C 00 =
            b xp := new Int(1); while y > 0 do xp.set(xp.get() ∗ y); y := y − 1 od; x := xp.get()

       This Java-like program uses get/set procedures acting on an object that stores an integer
       value, and (C|C 00 ) satisfies the same relational specification as (2). This code poses significant
       new challenges. It is not amenable to product reductions that rely on renaming of identifiers
       to encode two states as a single state: encoding of two heaps in one can be done, but at
       the cost of significant complexity [36] or exposing an underlying heap model below the level
       of abstraction of the programming language. Code like C 00 also needs to be linked with
       implementations of the procedures it calls. For reasoning about two versions of a module or
       library, relational hypotheses are needed, and calls need to be aligned to enable use of such
       hypotheses.
           Floyd [22] articulates the fundamental method of inductive assertions for partial correct-
       ness: establish that certain conditions hold at certain intermediate steps of computation,
       designating those conditions/steps by associating formulas with control flow points. For
       relational reasoning, pairs of steps need to be aligned and it is again natural to designate
       those in terms of points in control flow. Alignment of steps has appeared in many guises in
       prior work, often implicit in simulation proofs but explicit in a few works [48, 8, 28].
           First contribution: In this paper we embody the alignment principle in a formal system at
       the level of abstraction of the programming language—as Hoare logic does for the inductive
       assertion method—with sufficient generality to encompass many uses of relational properties
       for programs including procedures and dynamically allocated mutable objects. Our logic
       (Section 6) manifests the reasoning principle directly, in structured syntax. It also embodies
       other reasoning principles, such as frame rules, case analysis, and hypothetical specifications
       for procedures. The rules encompass relations between both similarly- and differently-
       structured programs, and handle partially and fully aligned iterations. This achievement
       brings together ideas from many recent works (Section 7), together with two ingredients we
       highlight as contributions in their own right.
A. Banerjee, D. A. Naumann, and M. Nikouei                                                           XX:3


    Second contribution: Our relational assertion language (Section 4) can describe agreement
between unbounded pointer structures, allowing for differences in object allocation, as is
needed to specify noninterference [4] and for simulation relations [3] in languages like Java
and ML where references are abstract. Such agreements are expressed without the need
for recursively defined predicates, and the assertion language has a direct translation to
SMT-friendly encodings of the heap. (For lack of space we do not dwell on such encodings in
this paper, which has a foundational focus, but see [41, 7].)
    Third contribution: We introduce a novel form of “biprogram” (Section 5) that makes
explicit the reasoner’s choice of alignments. A biprogram run models an aligned pair of
executions of the underlying programs. The semantics of biprograms involves a number of
subtleties: To provide a foundation for extending the logic with encapsulation (based on [5]),
we need to use small-step semantics—which makes it difficult to prove soundness of linking,
even in the unary case [5]. For this to work we need to keep the semantics deterministic and
to deal with semantics of hypotheses in judgments.
    Section 2 provides background and Section 3 is an overview of the logic using examples.
This document is the technical report to accompany a paper to appear in FSTTCS 2016.
It has appendices and also some additional notes in the main body of the paper (which
appear blue on color devices). Sections A–D develop the syntax and semantics of the logic,
Sections E–G develop examples, Section H proves a theorem that says how biprogram runs
model aligned pairs of ordinary runs, and Section I is on soundness of the logic. There is a
table of contents at the end of the document,


    2    Background: synopsis of region logic

For reasoning about the heap, separation logic is very effective, with modal operators that
implicitly describe heap regions. But for relations on unbounded heap structures at the
Java/ML level of abstraction we need explicit means to refer to heap regions, as in the
dependency logic of Amtoft et al. [2]. Our relational logic is based on an underlying unary
logic dubbed “region logic” (RL), developed in a series of papers [10, 5, 7] to which we refer
for rationale and omitted details. RL is a Hoare logic augmented with some side conditions
(first order verification conditions) which facilitate local reasoning about frame conditions [10]
in the manner of dynamic frames [27, 31]. In the logic such reasoning hinges on a frame rule.
In a verifier, framing can be done by the VC-generator, optionally guided by annotation [41].
Stateful frame conditions also support an approach to encapsulation that validates a second
order frame rule (at the cost of needing to use small-step semantics) [5]. Read effects enable
the use of pure method calls in assertions and in frame conditions [7] and are useful for
proving some equivalences, like commuting assignments, that hold in virtue of disjointness of
effects [15].
     The logic is formalized for imperative programs with first order procedures and dynamically
allocated mutable objects (records), see Fig. 1. As in Java and ML, references are distinct
from integers; they can be tested for equality but there is no pointer arithmetic. Typing of
programs is standard. In specifications we use ghost1 variables and fields of type rgn. A
region is a set of object references, which may include the improper null reference.
     A specification P ; Q [ε] is comprised of precondition P , postcondition Q, and frame


1
    We do not formalize a distinction between ghost and ordinary state.
XX:4   Relational logic with framing and hypotheses (Technical Report)


           m ∈ P rocN ame        x, y, r ∈ V arN ame      f, g ∈ F ieldN ame      K ∈ DeclaredClassN ames
           (Types)         T ::= int | bool | rgn | K
           (Program Expr.) E ::= x | c | null | E ⊕ E where c is in Z and ⊕ is in {=, +, −, ∗, ≥, ∧, ¬, . . .}
           (Region Expr.) G ::= x | ∅ | {E} | G‘f | G ⊗ G where ⊗ is in {∪, ∩, \}
           (Expressions)   F ::= E | G
           (Atomic comm.) A ::= skip | m() | x := F | x := new K | x := x.f | x.f := x
           (Commands)      C ::= A | let m = C in C | if E then C else C | while E do C | C ; C
           (Biprograms)    CC ::= (C|C) | bAc | let m = (C|C) in CC | CC ; CC
                                  | if E|E then CC else CC | while E|E • P|P do CC

          Figure 1 Programs and biprograms. Assume each class type K has a declared list of fields, f : T .
       Biprograms are explained in Section 3.


       condition ε. Frame conditions include both read and write effects:

             ε ::= rd x | rd G‘f | wr x | wr G‘f | ε, ε | (empty)

       The form rd G‘f means the program may read locations o.f where o is a reference in the
       region denoted by expression G. We write rw x to abbreviate the composite effect rd x, wr x,
       and omit repeated tags: rd x, y abbreviates rd x, rd y. Predicate formulas P include standard
       first order logic with equality, region subset (G ⊆ G), and the “points-to” relation x.f = E,
       which says x is non-null and the value of field f equals E. A correctness judgment has
       the form Φ ` C : P ; Q [ε] where the hypothesis context Φ maps procedure names to
       specifications. In C there may be environment calls to procedures bound by let inside C,
       and also context calls to procedures in Φ. The form G‘f is termed an image expression.
       For an example of image expressions, consider this command which sums the elements of a
       singly-linked null-terminated list, ignoring nodes for which a deletion flag, del, has been set.

          b s := 0; while p 6= null do if ¬p.del then s := s + p.val fi; p := p.nxt od
       C1 =

       For its specification we use ghost variable r : rgn to contain the nodes. Its being closed under
       nxt is expressed by r‘nxt ⊆ r in this specification:

             p ∈ r ∧ r‘nxt ⊆ r ; s = sum(listnd(old(p))) [rw s, p, rd r, r‘val, r‘nxt, r‘del]              (3)

       The r-value of the image expression r‘nxt is the set of values of nxt fields of the objects in r.
       In frame conditions, expressions are used for their l-values. In this case, the frame condition
       uses image expressions to say that for any object o in r, locations o.val, o.nxt, o.del may be
       read. The frame condition also says that variables s and p may be both read and written.
       Let function listnd give the mathematical list of non-deleted values.2
           Some proof rules in RL have side conditions which are first order formulas on one or
       two states. In this paper we treat these subsidiary judgments semantically. (Cognoscenti
       will have no difficulty thinking of ways to encode the subsidiary judgments as ∀-formulas
       amenable to SMT, for usual representations of program state.) One kind of side condition,
       dubbed the “frames judgment”, delimits the part of state on which a formula depends (its
       read effect). RL’s use of stateful frame conditions provides for a useful frame rule, and even
       second order frame rule [38, 5], but there is a price to be paid. Frame conditions involving
       state dependent region expressions are themselves susceptible to interference by commands.


       2
           We do not formalize old expressions in the logic, but our uses of them can be desugared using ghost
           variables.
A. Banerjee, D. A. Naumann, and M. Nikouei                                                            XX:5


That necessitates side conditions, termed “immunity” and “read-framed”, in the proof rules
for sequence and iteration [5, 7]. The frame rule allows to infer from Φ ` C : P ; Q [ε] the
conclusion Φ ` C : P ∧ R ; Q ∧ R [ε] provided that R is framed by read effects η (written
η frm R) for locations disjoint from those writable according to ε (written η ·/. ε).
    In keeping with our goal to develop a comprehensive deductive system, our unary and
relational logics include a rule for discharging hypotheses, expressed in terms of the linking
construct. Here is the special case of a single non-recursive procedure.

            m : R ; S [η] ` C : P ; Q [ε]       ` B : R ; S [η]
     Link
                      ` let m = B in C : P ; Q [ε]


 3      Overview of the relational logic
This section sketches highlights of relational reasoning about a number of illustrative examples,
introducing features of the logic incrementally. Some details are glossed over.
    We write (C|C 0 ) : Q ≈> R to express that a pair of programs C, C 0 satisfies the relational
contract with precondition Q and postcondition R, leaving aside frame conditions for now.
The judgment constrains executions of C and C 0 from pairs of states related by Q. (For
the grammar of relational formulas, see (8) in Section 4.) It says neither execution faults
(e.g., due to null dereference), and if both terminate then the final states are related by R.
Moreover no context procedure is called outside its precondition. (We call this property the
∀∀ form, for contrast with refinement properties of ∀∃ form.)
    Assume f, g are pure functions. The programs

     C0 =
        b x := f (z); y := g(z)     C00 =
                                        b y := g(z); x := f (z)

are equivalent. Focusing on relevant variables, the equivalence can be specified as

     (C0 | C00 ) : z =        ¨ x∧y =
                     ¨ z ≈> x =     ¨ y                                                        (4)

which can be proved as follows. Both C0 and C00 satisfy true ; x = f (z) ∧ y = g(z), which
directly entails that (C0 | C00 ) : Btrue ≈> B(x = f (z) ∧ y = g(z)) by an embedding rule.
The general form of embedding combines two different unary judgments, with different
specifications, using relational formulas that assert a predicate on just the left (/) or right (.)
state. So BP is short for /P ∧ .P . Since z is not written by C0 or C1 , we can introduce z =  ¨ z
                                                    0
using the relational frame rule, to obtain (C0 | C0 ) : z =
                                                          ¨ z ≈> B(x = f (z) ∧ y = g(z)) ∧ z = ¨ z.
This yields (4) using the relational rule of consequence with the two valid relational assertion
schemas u = ¨ u0 ∧ /(u = v) ∧ .(u0 = v 0 ) ⇒ v =¨ v 0 and z =
                                                            ¨ z ⇒ f (z) =
                                                                        ¨ f (z).
                                     0
    For the factorial example (C|C ) in Section 1, we would like to align the loops and use the
simple relational invariant x = ¨ x∧y = ¨ y + 1. We consider the form (C|C 0 ) as a biprogram
which can be rewritten to equivalent forms using the weaving relation which preserves the
underlying programs but aligns control points together so that relational assertions can be
used. (A minor difference from most other forms of product program is that we do not
need to rename apart the variables on the left and right.) The weaving relation is given in
Section 5. In this case we weave to the form

 (x := 1 | x := 1; y := y − 1); while y > 0 | y ≥ 0 do (x := x ∗ y | x := x ∗ y + x); by := y − 1c

This enables us to assert the relational invariant at the beginning and end of the loop bodies.
Indeed, we can also assert it just before the last assignments to y. The rule for this form of
XX:6   Relational logic with framing and hypotheses (Technical Report)


       loop requires the invariant to imply equivalence of the two loops’ guard conditions, which
       it does: x =  ¨ x∧y = ¨ y + 1 ⇒ (y > 0 =  ¨ y ≥ 0). For a biprogram of the split form (C|C 0 ),
       the primary reasoning principle is the lifting of unary judgments about C and C 0 . For an
       atomic command A, the sync notation bAc is an alternative to (A|A) that indicates its left
       and right transition are considered together. This enables the use of relational specifications
       for procedures, and a relational principle for object allocation. For an ordinary assignment,
       sync merely serves to abbreviate, as in by := y − 1c above.
           The next example involves the heap and it also involves a loop that is “dissonant” in the
       sense that we do not want to align all iterations—that is, alignment is ultimately about traces,
       not program texts. Imagine the command C1 from Section 2 is run on a list from which secret
       values have been deleted. To specify that no secrets are leaked, we use the relational judgment
       (C1 |C1 ) : listnd(p) =
                             ¨ listnd(p) ≈> s =¨ s which says: Starting from any two states containing
       the same non-deleted values, terminating computations agree on the sums. The judgment
       can be proved by showing the functional property that s ends up as sum(listnd(old(p))).
       But we can avoid reasoning about list sums and prove this relational property by aligning
       some of the loop iterations in such a way that listnd(p) =   ¨ listnd(p) ∧ s =¨ s holds at every
       aligned pair, that is, it is a relational invariant. Not every pair of loop iterations should be
       aligned: When p.del holds for the left state but not the right, a left-only iteration maintains
       the invariant, and mutatis mutandis when p.del holds only on the right. To handle such
       non-aligned iterations we use a novel syntactic annotation dubbed alignment guards. The
       idea is that the loop conditions are in agreement, and thus the iterations are synchronized,
       unless one of the alignment guards hold—and then that iteration is unsynchronized but the
       relational invariant must still be preserved. We weave (C1 |C1 ) to the form

          bs := 0c; while p 6= null | p 6= null • / (p.del) | .(p.del)                             (5)
                      do if ¬p.del | ¬p.del then bs := s + p.valc fi; bp := p.nxtc od

       with alignment guards /p.del and .p.del. The rule for the while biprogram has three premises
       for the loop body: for executions on the left (resp. right) under alignment guard /p.del
       (resp. .p.del) and for simultaneous executions when neither of the alignment guards hold.
       Each premise requires the invariant to be preserved. The loop body uses the synchronized
       conditional which requires agreement on the guard conditions; indeed, agreement does hold
       when neither of the loop alignment guards hold.
           The final example is a change of data representation. It illustrates dynamic allocation
       and frame conditions, as well as procedures and linking. A substantive example of this sort
       would be quite lengthy, so we contrive a toy example to provide hints of the issues that
       motivate various elements of our formal development. Our goal is to prove a conditional
       equivalence between these programs, whose components are defined in due course.

          C4 =
             b let push(x : int) = B in Cli      C40 =
                                                     b let push(x : int) = B 0 in Cli

       These differ only in the implementations B, B 0 of the stack interface (here stripped down to
       a single procedure), to which the client program Cli is linked. For modular reasoning, the
       unary contract for push should not expose details of the data representation. We also want to
       avoid reliance on strong functional specifications—the goal is equivalence of the two versions,
       not functional correctness of the client. The client, however, should respect encapsulation of
       the stack representation, to which end frame conditions are crucial. A simple pattern is for
       contracts to expose a ghost variable rep (of type rgn) for the set of objects considered to be
       owned by a program module. Here is the specification for push, with parts named for later
       reference. Let size and rep be spec-public, i.e., they can be used in public contracts but
A. Banerjee, D. A. Naumann, and M. Nikouei                                                        XX:7


not in client code [30].

     push(x : int) : R ; S[η] where R =
                                      b size < 100                                         (6)
                                    S=b size = old(size) + 1
                                    η=b rw rep, size, rep‘any

Variables rep and size can be read and written (keyword rw) by push. This needs to be
explicit, even though client code cannot access them, because reasoning about client code
involves them. The notation rep‘any designates all fields of objects in rep; these too may be
read and written. The specification makes clear that calls to push affect the encapsulated
state, while not exposing details. Here is one implementation of push(x).

 b top := new N ode(top, x); rep := rep ∪ {top}; size++
B=

Variable top is considered internal to the stack module, so it need not appear in the
frame condition. The alternate implementation of push replaces top by module variables
f ree : int; slots : String[ ];.

B0 =
   b if slots = null then slots := new String[100]; rep := rep ∪ {slots}; f ree := 0 fi;
     slots[f ree++] := x; size++

Unary correctness of the two versions is proved using module invariants

 b (top = null ∧ size = 0) ∨ (top ∈ rep ∧ rep‘nxt ⊆ rep ∧ size = length(list(top)))
I=

I0 =
   b (slots = null ∧ size = 0) ∨ (slots ∈ rep ∧ size = f ree)

Here list(top) is the mathematical list of values reached from top. Recall that in an assertion
the expression rep‘nxt is the image of set rep under the nxt field, i.e., the set of values of
nxt fields of objects in rep. The condition rep‘nxt ⊆ rep says that rep is closed under nxt.
This form is convenient in using ghost code to express shapes of data structures without
recourse to reachability or other inductive predicates [10, 41].
   As a specific Cli, we consider one that allocates and updates a node of the same type as
used by the list implementation; this gets assigned to a global variable p.

Cli =
    b push(1); p := new N ode(null, 2); p.val := 3; push(4)

Having completed the definitions of C4 , C40 we can ask: In what sense are C4 , C40 equivalent?
A possible specification for (C4 |C40 ) requires agreement on size and ensures agreement
on size and on p and p.val. However, the latter agreements cannot be literal equality:
following the call push(1), one implementation has allocated a N ode whereas the array
implementation has not. Depending on the allocator, different references may be assigned
to p in the two executions. The appropriate relation is “equivalence modulo renaming of
references” [2, 3, 4, 16, 17]. For region expression G and field name f , we write AG‘f for
the agreement relation that says there is a partial bijection on references between the two
states, that is total on the region G, and for which corresponding f -fields are equal. The
notation AG‘any means agreement on all fields. In the present example, the only region
expression used is the singleton region {p} containing the reference denoted by p.
    To prove a relational judgment for (C4 |C40 ) we need suitable relational judgments for
(B|B 0 ) for the implementations of push. It is standard [26] that they should preserve a
“coupling relation” that connects the two data representations and also includes the data
invariants for each representation. For the example, the connection is that the sequence of
XX:8   Relational logic with framing and hypotheses (Technical Report)


       elements reached from top, written list(top), is the same as the reversed sequence of elements
       in slots[0..f ree − 1]. Writing rev for reversal, we define the coupling and specification

             b /I ∧ .I 0 ∧ LtR
            L=                     LtR =           ¨ rev(h i if slots = null else slots[0..f ree − 1])
                                       b list(top) =

            (C4 |C40 ) : B(size = 0) ∧ L ≈> p =
                                              ¨ p ∧ size =
                                                         ¨ size ∧ A{p}‘any ∧ L                           (7)

       We now proceed to sketch a proof of (7). First, we weave (C4 |C40 ) to let push(x : int) =
       (B|B 0 ) in TCliU. Here TCliU abbreviates the fully aligned biprogram bpush(1)c; bp :=
       new N ode(null, 2)c; bp.val := 3c; bpush(4)c. This biprogram simultaneously links the proced-
       ure bodies on left and right, and aligns the client. Using bp := new N ode(null, 2)c enables
       use of a relational postcondition that says the objects are in agreement. Using bpush(4)c
       enables use of push’s relational specification.
           Like in unary RL, the proof rule for linking has two premises: one says the bodies (B|B 0 )
       satisfy their specification, the other says TCliU satisfies the overall specification under the
       hypothesis that push satisfies its spec (see rLink in Fig. 2). This hypothesis context gives
       push a relational specification, using Ax as sugar for x = ¨ x:

        b push(x) :
       Φ=                BR ∧ Asize ∧ Ax ∧ L ≈> BS ∧ Asize ∧ L [η, rw top | η, rw slots, f ree]

       Here η is the effect rw rep, size, rep‘any in the original specification (6) of push.
           The specification in Φ is not simply a relational lift of push’s public specification (6).
       Invariants I and I 0 on internal data structures should not appear in push’s API: they should
       be hidden, because the client should not touch the internal state on which they depend.
       Effects on module variables (like top) should also be hidden. This kind of reasoning is the
       gist of second order framing [38, 5]. The relational counterpart is a relational second order
       frame rule which says that any client that respects encapsulation will preserve L. Hiding is
       the topic of another paper, for which this one is laying the groundwork (see Section 8).

        4      Relational formulas
       The relational assertion language is essentially syntax for a first order structure comprised of
       the variables and heaps of two states, together with a refperm connecting the states.

                     ¨ F | AG‘f | P | /P | .P | P ∧ P | P ⇒ P | ∀x|x0 : K. P
             P ::= F =                                                                                   (8)

       A refperm is a type-respecting partial bijection from references allocated in one state to
       references allocated in the other state. For use with SMT provers, a refperm can be encoded
       by a pair of maps with universal formulas stating they are inverse [7]. The syntax for relations
       caters for dynamic allocation by providing primitives such as F =   ¨ F 0 that says the value of
                                           0
       F in the left state equals that of F in the right state, modulo the refperm. In case of integer
       expressions, this is ordinary equality. For reference expressions, it means the two values are
       related by the refperm. For region expressions, G =  ¨ G0 means the refperm forms a bijection
       between the reference set denoted by G in the left state and G0 in the right state (ignoring
       null). The agreement formula AG‘f says, of a pair of states, that the refperm is total on the
       set denoted by G in the left state, and moreover the f -field of each object in that set has the
       same value, modulo refperm, as the f -field of its corresponding object in the right state.
           For commands that allocate, the postcondition needs to allow the refperm to be extended,
       which is expressed by the modal operator  (read “later”): P holds if there is an extension
       of the refperm with zero or more pairs of references for which P holds. For example, after the
       assignment to p in the stack example, the relational rule for allocation yields postcondition
A. Banerjee, D. A. Naumann, and M. Nikouei                                                                XX:9


(p =¨ p ∧ A{p}‘any). Aside from the left and right embeddings of unary predicates (/P and
.P ), the only other constructs are the logical ones (conjunction, implication, quantification
over values).
    We use the following syntax sugars: BP =      b /P ∧ .P , AE =   b E =¨ E, A(rd G‘f, rd x) =
                                                                                               b
AG‘f ∧ Ax, etc. Note that AE is unambiguous, but we cannot use the analogous abbreviation
for region expressions: For region expressions of the image form, G‘f , the atomic formula
AG‘f already has a meaning, which is different from G‘f =     ¨ G‘f . The meaning of G‘f = ¨ G‘f
is equality, modulo refperm, of two sets: the f -fields of G-objects in the left state and in
the right state. By contrast, AG‘f means that for each non-null reference o in region G
(interpreted in the left state), with counterpart o0 according to the refperm, the f fields of o
and o0 agree.
    Let 2P = b ¬  ¬P. Validity of P ⇒ 2P is equivalent to P being monotonic, i.e., not
falsified by extension of the refperm. Validity of P ⇒ P expresses that P is refperm-
independent. Here are some valid schemas: P ⇒ P,   P ⇒ P, and (P ∧ Q) ⇒ P ∧ Q.
The converse of the latter is not valid.3 For framing, a key property is that P ∧Q ⇒ (P ∧Q)
is valid if Q is monotonic. In practice,  is only needed in postconditions, and only at the
top level. Owing to   P ⇒ P, this works fine with sequenced commands.4 Many useful
formulas are monotonic, including AG‘f and F =       ¨ F 0 , but not ¬(F =¨ F 0 ). The  operator
can also break monotonicity: (x =  ¨ x) is not monotonic. The  operator extends the refperm
but not the sets of allocated references. So this is valid: alloc =  ¨ alloc ∧ P ⇒ P, where ∧
binds more tightly than ⇒. (Because alloc =     ¨ alloc says the refperm is a total bijection on
allocated references and has no proper extensions.)

    5     Biprograms
A biprogram CC (Fig. 1) represents a pair of commands, which are given by syntactic
                                                        (−−−−         −−−−*            (−
projections defined by clauses including the following: (C|C 0 ) =
                                                                 b C, (C|C 0 ) =
                                                                               b C 0 , bAc =
                                                                                           b A,
(−−−−0−−−−−−−−−−−−−−                   (−        (−       (−−−−−−−−−0−−−−−−
if E|E then BB else CC =  b if E then BB else CC, and let m = (C|C ) in CC =         b let m =
     (−
C in CC. The weaving relation has clauses including the following.

        (A|A) ,→ bAc         (for atomic commands A)
        (C; D | C 0 ; D0 ) ,→ (C|C 0 ); (D|D0 )
        (if E then C else D | if E 0 then C 0 else D0 ) ,→ if E|E 0 then (C|C 0 ) else (D|D0 )
        (while E do C | while E 0 do C 0 ) ,→ while E|E 0 • P|P 0 do (C|C 0 )      (for any P, P 0 )

Additional clauses are needed for congruence, e.g., CC ,→ DD implies BB; CC ,→ BB; DD.
The loop weaving introduces chosen alignment guards. The full alignment of a command
C is written TCU and defined by TAU =  b bAc, TC; DU =  b TCU; TDU, Tif E then C else DU =  b
if E|E then TCU else TDU, Twhile E do CU =  b while E|E • false|false do TCU, etc. Note that
(C|C) ,→∗ TCU for any C.
    Commands are deterministic (modulo allocation), so termination-insensitive noninterfer-
ence and equivalence properties can be expressed in a simple ∀∀ form described at the start of
Section 3, rather than the ∀∃ form needed for refinement and for possibilistic noninterference


3
    For example, (x =¨ y) ∧ (x =
                                 ¨ z ∧ .(z 6= y)) is satisfiable but (x =
                                                                         ¨ y∧x=¨ z ∧ .(z 6= y)) is not.
4
    There is a convenient derived rule for sequencing of judgments like CC : P ≈> Q and DD : Q ≈> R.
    We can use rule rLater to get DD : Q ≈>   R, and thus DD : Q ≈> R by the rule of consequence,
    using   R ⇒ R. Then by the sequence rule we get CC; DD : P ≈> R.
XX:10   Relational logic with framing and hypotheses (Technical Report)


        (“for all runs . . . there exists a run . . . ”). The transition rules for biprograms must ensure
        that the behavior is compatible with the underlying unary semantics, while enforcing the
        intended alignment. That would still allow some degree of nondeterminacy in biprogram
        transitions. However, we make biprograms deterministic (modulo allocation), because it
        greatly simplifies the soundness proofs. Rather than determinize by means of a scheduling
        oracle or other artifacts that would clutter the semantics, we build determinacy into the
        transition semantics. Whereas the syntax aligns points of interest in control flow, biprogram
        traces explicitly represent aligned pairs of executions. We make the arbitrary choice of
        left-then-right semantics for the split form. In a trace of (C|C 0 ), every step taken by C is
        effectively aligned with the initial state for C 0 . This is followed by the steps of C 0 , each
        aligned with the final state of C. To illustrate the idea, here is a sketch of the trace of a split
        biprogram (center column) and its alignment with left and right unary traces.
                          hx:=0; y:=0i     h(x:=0; y:=0 | x:=0; y:=0)i      hx:=0; y:=0i
                             hy:=0i           h(y:=0 | x:=0; y:=0)i
                             hskipi            h(skip | x:=0; y:=0)i
                                                  h(skip | y:=0)i              hy:=0i
                                                      hbskipci                 hskipi

        This pattern is also typical for “high conditionals” in noninterference proofs, where different
        branches may be taken (cf. rule rIf4). Here is the sync’d version in action.
                               hx:=0; y:=0i      hbx:=0c; by:=0ci     hx:=0; y:=0i
                                  hy:=0i             hby:=0ci            hy:=0i
                                  hskipi             hbskipci            hskipi


            The relational correctness judgment has the form Φ ` CC : P ≈> Q [ε|ε0 ]. The hypothesis
        context Φ maps some procedure names to their specifications: Φ(m) may be a unary
        specification as before or else a relational one of the form R ≈> S [ε|ε0 ]. Frame conditions
        retain their meaning, separately for the left and the right side. In case ε is the same as ε0 ,
        the judgment or specification is abbreviated as P ≈> Q [ε].
            The semantics of biprograms uses small steps, which makes alignments explicit. A
        configuration is comprised of a biprogram, two states, and two environments for procedures.
        The transition relation depends on a semantic interpretation for each procedure in the
        hypothesis context Φ. Context calls, i.e., calls to procedures in the context, take a single
        step in accord with the interpretation. For the sake of determinacy, this is formalized in the
        semantics of relational correctness by quantifying over deterministic “interpretations” of the
        specifications (as in [7]), rather than a single nondeterministic transition rule (as in [5, 38]).
            An aligned conditional, if E|E 0 then CC else DD, faults from initial states that do not
        agree on the guard conditions E, E 0 . An aligned loop while E|E 0 • P|P 0 do CC executes
                                     (−
        the left part of the body, CC, if E and the left alignment guard P both hold, and mutatis
        mutandis for the right. If neither alignment guard holds, the loop faults unless the guards
        E, E 0 agree.
            The relational correctness judgment disallows faults, so correctness of a biprogram implies
        it represents the intended alignments. Note that the weaving transformations can introduce,
        but not eliminate, alignment faults.
            Let us sketch the semantic consistency theorem, which confirms that executions of
        a biprogram from a pair of states correspond to pairs of executions of the underlying
        commands, so that judgments about biprograms represent relational properties of the
        underlying commands. Suppose Φ ` (C|C 0 ) : P ≈> Q [ε|ε0 ] is valid and Φ has only
A. Banerjee, D. A. Naumann, and M. Nikouei                                                                 XX:11



                      m : R ≈> S [η] ` TCU : P ≈> Q [ε]           ` (B|B 0 ) : R ≈> S [η]
              rLink
                                    ` let m = (B|B 0 ) in TCU : P ≈> Q [ε]

           Φ ` (C|C 0 ) : P ∧ /E ∧ .E 0 ≈> Q [ε|ε0 ]        Φ ` (C|D0 ) : P ∧ /E ∧ .¬E 0 ≈> Q [ε|ε0 ]
          Φ ` (D|C 0 ) : P ∧ /¬E ∧ .E 0 ≈> Q [ε|ε0 ]        Φ ` (D|D0 ) : P ∧ /¬E ∧ .¬E 0 ≈> Q [ε|ε0 ]
rIf4
               Φ ` (if E then C else D|if E 0 then C 0 else D0 ) : P ≈> Q [ε, ftpt(E)|ε0 , ftpt(E 0 )]

                                           P⇒E= ¨ E0
                                       0    0
              Φ ` CC : P ∧ /E ∧ .E ≈> Q [ε|ε ] Φ ` DD : P ∧ /¬E ∧ .¬E 0 ≈> Q [ε|ε0 ]
        rIf
                      Φ ` if E|E 0 then CC else DD : P ≈> Q [ε, ftpt(E)|ε0 , ftpt(E 0 )]

                                              Φ ` DD : P ≈> Q [ε|ε0 ]
                                                              (− (−−                            −* −−*
                  CC ,→ DD          unaryOnly(Φ)   terminates( P , DD)               terminates( P , DD)
        rWeave
                                                Φ ` CC : P ≈> Q [ε|ε0 ]

        Figure 2 Selected relational proof rules.


unary specifications. Consider any states σ, σ 0 that are related by P (modulo some refperm).
Suppose C and C 0 , when executed from σ, σ 0 , reach final states τ, τ 0 . (In the formal semantics,
transitions are defined in terms of interpretations ϕ that satisfy the specifications Φ, so this
                    ϕ                                ϕ
is written hC, σi 7−→∗ hskip, τ i and hC 0 , σ 0 i 7−→∗ hskip, τ 0 i.) Then τ, τ 0 satisfy Q.


    6      Relational region logic
Selected proof rules appear in Fig. 2.
    For linking a procedure with its implementation, rule rLink caters for a client program
C related to itself, in such a way that its executions can be aligned to use the same pattern
of calls. The procedure implementations may differ, as in the stack example, Section 3. The
rule shown here is for the special case of a single procedure, and the judgment for (B|B 0 )
has empty hypothesis context, to disallow recursion. We see no difficulty to add mutually
recursive procedures, as done for the unary logic in [5], but have not yet included that in a
detailed soundness proof. The soundness proof is basically an induction on steps as in [5]
but with the construction of an interpretation as in the proof of the linking rule in [7]. The
general rule also provides for un-discharged hypotheses for ambient libraries used in the
client and in the procedure implementations [5].
    Rule rIf4 is the obvious rule that considers all paths for a conditional not aligned
with itself (e.g., for “high branches”), whereas rIf leverages the alignment designated
by the biprogram form. The disjunction rule—i.e., from Φ ` CC : P0 ≈> Q [ε|ε0 ] and
Φ ` CC : P1 ≈> Q [ε|ε0 ] infer Φ ` CC : P0 ∨ P1 ≈> Q [ε|ε0 ]—serves to split cases on the
initial states, allowing different weavings to be used for different circumstances, which is
why there is no notion like alignment guards for the biprogram conditional. The obvious
conjunction rule is sound.5 It is useful for deriving other rules. For example, we have this
simple axiom for allocation: ` bx := new Kc : true ≈> (x =        ¨ x) [wr x, rw alloc]. Using
conjunction, embedding, the unary rule Alloc, and framing, one can add postconditions


5
    That is, from Φ ` CC : P0 ≈> Q0 [ε|ε0 ] and Φ ` CC : P1 ≈> Q1 [ε|ε0 ] infer Φ ` CC : P0 ∧ P1 ≈>
    Q0 ∧ Q1 [ε|ε0 ]. The hypotheses and frame conditions are unchanged.
XX:12   Relational logic with framing and hypotheses (Technical Report)


        like A{x}‘f and freshness of x.
             A consequence of our design decisions is “one-sided divergence” of biprograms, which comes
        into play with weaving. For example, assuming loop diverges, (y := 0; z.f := 0 | loop; x := 0)
        assigns z.f before diverging. But it weaves to (y := 0|loop); (z.f := 0|x := 0) which never
        assigns z.f . This biprogram’s executions do not cover all executions of the underlying unary
        programs. The phenomenon becomes a problem for code that can fault (e.g., if z is null).
        Were the correctness judgments to assert termination, this shortcoming would not be an
        issue, but in this paper we choose the simplicity of partial correctness. Rule rWeave needs
        to be restricted to prevent one-sided divergence of the premise biprogram DD from states
        where CC in the conclusion terminates. For simplicity in this paper we assume given a
        termination check: terminates(P, C) means that C faults or terminates normally, from any
        initial state satisfying P , This is about unary programs, so the condition can be discharged
        by standard means.6
             The relational frame rule is a straightforward extension of the unary frame rule. From a
        judgment Φ ` CC : P ≈> Q [ε|ε0 ] it infers Φ ` CC : P ∧ R ≈> Q ∧ R [ε|ε0 ] provided that R
        is framed by read effects (on the left and right) that are disjoint from the write effects in ε|ε0 .
             To prove a judgment Φ ` while E|E 0 • P|P 0 do CC : Q ≈> Q [ε, ftpt(E)|ε0 , ftpt(E 0 )],
                                                       (−
        the rule has three main premises:7 Φ ` (CC|skip) : Q ∧ P ∧ /E ≈> Q [ε| ] for left-only
                                            −*
        execution of the body, Φ ` (skip|CC) : Q ∧ P 0 ∧ .E 0 ≈> Q [ |ε0 ] for right-only, and Φ ` CC :
        Q ∧ ¬P ∧ ¬P 0 ∧ /E ∧ .E 0 ≈> Q [ε|ε0 ] for aligned execution. A side condition requires that
        the invariant Q implies these cases are exhaustive: Q ⇒ E =       ¨ E 0 ∨ (P ∧ /E) ∨ (P 0 ∧ .E 0 ).
        Additional side conditions require the effects to be self-immune, just as in unary RL [10, 7].
        Finally, the formulas P ⇒ P and P 0 ⇒ P 0 must be valid; this says the alignment guards
        are refperm-independent, which is needed because refperms are part of the semantics of
        judgments but are not part of the semantics of biprograms.
             The above rule is compatible with weaving a loop body, as in (5). The left and right
                     (−        −*
        projections CC and CC undo the weaving and take care of unaligned iterations.
             There are many other valid and useful rules. Explicit frame conditions are convenient,
        both in tools and in a logic, in part because they compose in simple ways. This may lose
        precision, but that can be overcome using postconditions to express, e.g., that x := x
        does not observably write x. This is addressed, in unary RL, by a rule to “mask” write
        effects [10]. Similarly, the relational logic supports a rule to mask read effects. There
        is a rule of transitivity along these lines: (B|C) : P ≈> Q and (C|D) : R ≈> S infer
        (B|D) : P; R ≈> Q; S where (; ) denotes composition of relations. A special case is where
        the pre-relations (resp. post-relations) are the same, transitive, relation. The rule needs to
        take care about termination of C.

            7   Related work
        Benton [15] introduced relational Hoare logic, around the same time that Yang was developing
        relational separation logic [46]. Their works emphasize the effectiveness and flexibility of
        relational reasoning using ordinary extensional program semantics. Benton’s logic does not
        encompass the heap. Yang’s does; it features separating conjunction and a frame rule. The


        6
          One can also think about a more complicated semantics for biprograms, in which splits take steps on
          alternating sides. But this requires to augment configurations with some kind of scheduler state and
          would slightly complicate some soundness proofs, so we leave that to future work.
        7
          The syntactic footprint ftpt(E) is described in the Appendix and fully defined in [10].
A. Banerjee, D. A. Naumann, and M. Nikouei                                                            XX:13


fully nondeterministic allocator is used. Pointers are treated concretely in [46]; agreement
means identical addresses, which suffices for some low level C code. Neither work includes
procedures. Beringer [18] reduces relational verification to unary verification via specifications
and uses that technique to derive rules of a relational Hoare logic for programs including the
heap (but not procedures). Whereas the logics of Benton, Yang, and others provide only rules
for synchronized alignment of loops, Beringer derives a rule that allows for unsynchronized
(“dissonant”) iterations; our alignment guards are similar to side conditions of that rule.
RHTT [35] implements a relational program logic in dependent type theory (Coq). The work
focuses on applications to information flow. It handles dynamically allocated mutable state
and procedures, and both similar and dissimilar control structures. Like the other relational
logics it does not feature frame conditions. RHTT is the only prior relational logic to include
both the heap and procedures, and the only one to have a procedure linking rule. It is also
the only one to address any form of encapsulation; it does so using abstract predicates, as
opposed to hiding [5, 38].
    Several works investigate construction of product programs that encode nontrivial choices
of alignment [39, 43, 47, 11, 12, 13]. In particular, our weaving relation was inspired by [11, 13]
which address programs that differ in structure. In contrast to the 2-safety properties for
deterministic programs considered in this paper and most prior work, Barthe et al. [12] handle
properties of the form “for all traces . . . there exists a trace . . . ” which are harder to work
with but which encompass notions of refinement and continuity. Relational specifications
of procedures are used in a series of papers by Barthe et al. (e.g.,[14]) for computer-aided
cryptographic proofs. Sousa and Dillig [42] implement a logic that encompasses k-ary
relations, e.g., the 3-safety property that a binary method is computing a transitive relation;
their verification algorithm is based on an implicit product construction. None of these works
address the heap or the linking of procedure implementations. (Although the prototype
implementation [42] does.) Several works show that syntactic heuristics can often find good
weavings in the case of similarly-structured programs not involving the heap [28, 33, 42].
Mueller et al. [33] use a form of product program and a relational logic to prove correctness
of a static analysis for dependency, including procedures but no heap.
    Works on translation validation and conditional equivalence checking use verification
conditions (VCs) with implicit or explicit product constructions [47, 48]. Godlin and
Strichman formulate and prove soundness of rules for proving equivalence of programs with
similar control structure [23]. They use one of the rules to devise an algorithm for VCs
using uninterpreted functions to encode equivalence of called procedures, which has been
implemented in two prototype tools for equivalence checking [24]. (Pointer structures are
limited to trees, i.e., no sharing.) Hawblitzel et al. [25] and Lahiri et al. [29] use relational
procedure summaries for intra- and inter-procedural reasoning about program transformations.
The heap is modeled by maps. These and related works report good experimental results
using SMT or SAT solvers to discharge VCs. Felsing et al. [21] use Horn constraint solving
to infer coupling relations and relational procedure summaries, which works well for similarly
structured programs; they do not deal with the heap. The purpose of our logic is not to
supplant VC-based tools approaches but rather to provide a foundation for them. Our
biprograms and relational assertions are easily translated to SMT-based back ends like
Boogie and Why3.
   Amtoft et al. [2] introduce a logic for information flow in object-based programs, using
abstract locations to specify agreements in the heap. It was proposed in [8] to extend this
approach to more general relational specifications, for fine-grained declassification policies.
Banerjee et al. [9] showed how region-based reasoning including a frame rule can be encoded,
XX:14   Relational logic with framing and hypotheses (Technical Report)


        using ghost code, with standard FOL assertions instead of an ancillary notion of abstract
        region. This evolved to the logic in Section 6.
            Relational properties have been considered in the context of separation logic: [19] and [44]
        both give relational interpretations of unary separation logic that account for representation
        independence, using second order framing [19] or abstract predicates [44]. Extension of this
        work to a relational logic seems possible, but the semantics does not validate the rule of
        conjunction so it may not be a good basis for verification tools. Tools often rely heavily on
        splitting conjunctions in postconditions.
            Ahmed et al. [1] address representation independence for higher order code and code
        pointers, using a step-indexed relational model, and prove challenging instances of contextual
        equivalence. Based on that work, Dreyer et al. [20] formulate a relational modal logic for
        proving contextual equivalence for a language that has general recursive types and general
        ML-style references atop System F. The logic serves to abstract from details of semantics
        in ways likely to facilitate interactive proofs of interesting contextual equivalences, but it
        includes intensional atomic propositions about steps in the transition semantics of terms.
        Whereas contextual equivalence means equivalent in all contexts, general relational logics can
        express equivalences conditioned on the initial state. For example, the assignments x := y.f
        and z.f := w do not commute, in general, because their effects can overlap. But they do
        commute under the precondition y =     6 z. We can easily prove equivalence judgments such
        as (x := y.f ; z.f := w | z.f := w; x := y.f ) : B(y 6= z) ∧ A{y}‘f ∧ w =
                                                                                ¨ w ≈> x =¨ x ∧ A{z}‘f .
        By contrast with [1, 35], we do not rely on embedding in higher-order logic.
            Benton et al. [16] give a region-based type and effect system that supports observational
        purity and validates a number of equivalences that hold in virtue of effects alone. The authors
        note that the semantics does not validate equivalences involving representation independence.



            8    Conclusion
        We provide a general relational logic that encompasses the heap and includes procedures. It
        handles both similarly- and differently-structured programs. We use small-step semantics with
        the goal to leverage, in future work, our prior work on SMT-friendly heap encapsulation [41,
        5, 7] for representation independence, which is not addressed in prior relational logics.8
            As articulated long ago by Hoare [26] but never fully formalized in a logic of programs,
        reasoning about change of data representation is based on simulation relations on encapsulated
        state, which are necessarily preserved by client code in virtue of encapsulation. For functional
        correctness this corresponds to “hiding” of invariants on encapsulated data, i.e., not including
        the invariant in the specification used by a client. O’Hearn et al. [38] formalize this as a
        hypothetical or second order framing rule (which has been adapted to RL [5]). In ongoing
        work, the logic presented here has been extended to address encapsulation and provides
        a relational second order frame rule which embodies Reynolds’ abstraction theorem [40].
        Whereas framing of invariants relies on write effects, framing of encapsulated relations also
        relies on read effects. Our ongoing work also addresses observational purity, which is known
        to be closely related to representation independence [26, 37].
            Although we can prove equivalence for loop tiling, some array-oriented loop optimizations


        8
            With the partial exception of [1], see Section 7. Although there has been some work on observational
            equivalence for higher order programs, we are not aware of work dealing with general relational judgments
            for higher order programs.
A. Banerjee, D. A. Naumann, and M. Nikouei                                                        XX:15


seem to be out of reach of the logic as currently formulated. Loop interchange changes
matrix row to column order, reordering unboundedly many atomic assignments, as does loop
fusion/distribution. Most prior work does not handle these examples; [48] does handle them,
with a non-syntactic proof rule that involves permutations on transition steps, cf. [34].

Acknowledgments
Thanks to César Kunz, Mounir Assaf, and Andrey Chudnov for helpful suggestions and
comments on previous versions of this paper.


     References
 1   Amal Ahmed, Derek Dreyer, and Andreas Rossberg. State-dependent representation inde-
     pendence. In ACM Symposium on Principles of Programming Languages, 2009.
 2   T. Amtoft, S. Bandhakavi, and A. Banerjee. A logic for information flow in object-oriented
     programs. In ACM Symposium on Principles of Programming Languages, 2006.
 3   Anindya Banerjee and David A. Naumann. Ownership confinement ensures representation
     independence for object-oriented programs. Journal of the ACM, 52(6):894–960, 2005.
 4   Anindya Banerjee and David A. Naumann. Stack-based access control for secure informa-
     tion flow. Journal of Functional Programming, 15(2):131–177, 2005.
 5   Anindya Banerjee and David A. Naumann. Local reasoning for global invariants, part II:
     Dynamic boundaries. Journal of the ACM, 60(3):19:1–19:73, 2013.
 6   Anindya Banerjee and David A. Naumann. A logical analysis of framing for specifications
     with pure method calls. In Verified Software: Theories, Tools and Experiments, volume
     8471 of LNCS, 2014.
 7   Anindya Banerjee, David A. Naumann, and Mohammad Nikouei. A logical analysis of
     framing for specifications with pure method calls. Under review for publication. Extended
     version of [6]. http://www.cs.stevens.edu/~naumann/pub/readRL.pdf, 2015.
 8   Anindya Banerjee, David A. Naumann, and Stan Rosenberg. Expressive declassification
     policies and modular static enforcement. In IEEE Symposium on Security and Privacy,
     2008.
 9   Anindya Banerjee, David A. Naumann, and Stan Rosenberg. Regional logic for local reas-
     oning about global invariants. In European Conference on Object-Oriented Programming,
     volume 5142 of LNCS, 2008.
10   Anindya Banerjee, David A. Naumann, and Stan Rosenberg. Local reasoning for global
     invariants, part I: Region logic. Journal of the ACM, 60(3):18:1–18:56, 2013.
11   Gilles Barthe, Juan Manuel Crespo, and César Kunz. Relational verification using product
     programs. In Formal Methods, volume 6664 of LNCS, 2011.
12   Gilles Barthe, Juan Manuel Crespo, and César Kunz. Beyond 2-safety: Asymmetric product
     programs for relational program verification. In Logical Foundations of Computer Science,
     International Symposium, volume 7734 of LNCS, 2013.
13   Gilles Barthe, Juan Manuel Crespo, and César Kunz. Product programs and relational
     program logics. J. Logical and Algebraic Methods in Programming, 2016. To appear.
14   Gilles Barthe, Boris Köpf, Federico Olmedo, and Santiago Zanella Béguelin. Probabilistic
     relational reasoning for differential privacy. ACM Trans. Program. Lang. Syst., 35(3):9,
     2013.
15   Nick Benton. Simple relational correctness proofs for static analyses and program trans-
     formations. In ACM Symposium on Principles of Programming Languages, 2004.
16   Nick Benton, Martin Hofmann, and Vivek Nigam. Abstract effects and proof-relevant
     logical relations. In ACM Symposium on Principles of Programming Languages, 2014.
XX:16   Relational logic with framing and hypotheses (Technical Report)


        17   Nick Benton, Andrew Kennedy, Lennart Beringer, and Martin Hofmann. Relational se-
             mantics for effect-based program transformations with dynamic allocation. In International
             Symposium on Principles and Practice of Declarative Programming, 2007.
        18   Lennart Beringer. Relational decomposition. In Interactive Theorem Proving (ITP), volume
             6898 of LNCS, 2011.
        19   Lars Birkedal and Hongseok Yang. Relational parametricity and separation logic. Logical
             Methods in Computer Science, 4(2), 2008.
        20   Derek Dreyer, Georg Neis, Andreas Rossberg, and Lars Birkedal. A relational modal
             logic for higher-order stateful ADTs. In ACM Symposium on Principles of Programming
             Languages, 2010.
        21   Dennis Felsing, Sarah Grebing, Vladimir Klebanov, Philipp Rümmer, and Mattias Ulbrich.
             Automating regression verification. In International Conference on Automated Software
             Engineering, 2014.
        22   Robert W. Floyd. Assigning meanings to programs. In Proceedings of Symposia in Applied
             Mathematics 19, pages 19–32. American Mathematical Society, 1967.
        23   Benny Godlin and Ofer Strichman. Inference rules for proving the equivalence of recursive
             procedures. Acta Inf., 45(6):403–439, 2008.
        24   Benny Godlin and Ofer Strichman. Regression verification: proving the equivalence of
             similar programs. Softw. Test., Verif. Reliab., 23(3):241–258, 2013.
        25   Chris Hawblitzel, Ming Kawaguchi, Shuvendu K. Lahiri, and Henrique Rebêlo. Towards
             modularly comparing programs using automated theorem provers. In International Con-
             ference on Automated Deduction, 2013.
        26   C. A. R. Hoare. Proofs of correctness of data representations. Acta Informatica, 1:271–281,
             1972.
        27   Ioannis T. Kassios. The dynamic frames theory. Formal Aspects of Computing, 23(3):267–
             288, 2011.
        28   Máté Kovács, Helmut Seidl, and Bernd Finkbeiner. Relational abstract interpretation
             for the verification of 2-hypersafety properties. In ACM Conference on Computer and
             Communications Security, 2013.
        29   Shuvendu K. Lahiri, Kenneth L. McMillan, Rahul Sharma, and Chris Hawblitzel. Differen-
             tial assertion checking. In Joint Meeting of the European Software Engineering Conference
             and the ACM Symposium on the Foundations of Software Engineering, 2013.
        30   Gary T. Leavens and Peter Müller. Information hiding and visibility in interface specifica-
             tions. In International Conference on Software Engineering, 2007.
        31   K. Rustan M. Leino. Dafny: An automatic program verifier for functional correctness. In
             International Conference on Logic for Programming Artificial Intelligence and Reasoning,
             LNCS, 2010.
        32   K. Rustan M. Leino and Peter Müller. Verification of equivalent-results methods. In ESOP,
             volume 4960 of LNCS, pages 307–321, 2008.
        33   Christian Mueller, Máté Kovács, and Helmut Seidl. An analysis of universal information
             flow based on self-composition. In IEEE Computer Security Foundations Symposium, 2015.
        34   Kedar S. Namjoshi and Nimit Singhania. Loopy: Programmable and formally verified loop
             transformations. In Static Analysis Symposium, volume 9837 of LNCS, 2016.
        35   Aleksandar Nanevski, Anindya Banerjee, and Deepak Garg. Dependent type theory for
             verification of information flow and access control policies. ACM Trans. Program. Lang.
             Syst., 35(2):6, 2013.
        36   David A. Naumann. From coupling relations to mated invariants for secure information
             flow. In European Symposium on Research in Computer Security, volume 4189 of LNCS,
             2006.
A. Banerjee, D. A. Naumann, and M. Nikouei                                                        XX:17


37   David A. Naumann. Observational purity and encapsulation. Theoretical Computer Science,
     376(3):205–224, 2007.
38   Peter W. O’Hearn, Hongseok Yang, and John C. Reynolds. Separation and information
     hiding. ACM Transactions on Programming Languages and Systems, 31(3):1–50, 2009.
39   John C. Reynolds. The Craft of Programming. Prentice-Hall, 1981.
40   John C. Reynolds. Types, abstraction, and parametric polymorphism. In R.E.A. Mason,
     editor, Information Processing ’83, pages 513–523. North-Holland, 1984.
41   Stan Rosenberg, Anindya Banerjee, and David A. Naumann. Decision procedures for region
     logic. In Int’l Conf. on Verification, Model Checking, and Abstract Interpretation, 2012.
42   Marcelo Sousa and Isil Dillig. Cartesian Hoare logic for verifying k-safety properties. In
     ACM Conf. on Program. Lang. Design and Implementation, 2016.
43   Tachio Terauchi and Alex Aiken. Secure information flow as a safety problem. In Interna-
     tional Static Analysis Symposium, volume 3672 of LNCS, 2005.
44   Jacob Thamsborg, Lars Birkedal, and Hongseok Yang. Two for the price of one: Lifting
     separation logic assertions. Logical Methods in Computer Science, 8(3), 2012.
45   Dennis Volpano, Geoffrey Smith, and Cynthia Irvine. A sound type system for secure flow
     analysis. Journal of Computer Security, 4(3):167–187, 1996.
46   Hongseok Yang. Relational separation logic. Theoretical Computer Science, 375(1-3):308–
     334, 2007.
47   Anna Zaks and Amir Pnueli. CoVaC: Compiler validation by program analysis of the
     cross-product. In Formal Methods, volume 5014 of LNCS, 2008.
48   Lenore D. Zuck, Amir Pnueli, Benjamin Goldberg, Clark W. Barrett, Yi Fang, and Ying Hu.
     Translation and run-time validation of loop transformations. Formal Methods in System
     Design, 27(3):335–360, 2005.
XX:18   Relational logic with framing and hypotheses (Technical Report)


            A     Semantics of unary programs and their correctness judgments

        A typing context, Γ, maps variables to types. (Types are in Fig. 1.) A Γ-state is comprised
        of a heap and a type-respecting assignment of values to the variables in Γ, which always
        includes the special variable alloc, built into the semantics, that is not allowed to be assigned
        in code. Its value is the set of allocated references. It appears in frame conditions of code
        that allocates, a detail that is glossed over in Sec. 3. A state must be well formed in the
        sense that there are no dangling references. In particular, the value of a region expression is
        a set of allocated references, possibly also including null. We write σ(x) to look up the value
        of x in state σ, σ(o.f ) to look up field f of reference o, σ(F ) for the value of expression F ,
        and [[Γ]] for the set of Γ-states.
            The transition semantics uses configurations hC, σ, µi where µ is an environment that
        maps procedure names to commands. (The control state C encodes a stack of continuations
        as a single command, using scope endmarkers for var and let. Nothing is needed to mark
        the end of a procedure call, as procedures have neither parameters nor returns.) We work
        with typed configurations, and typed correctness judgments, but gloss over typing in this
        paper (see [5]). The transition semantics is standard, except that we aim for reasoning about
        programs under hypotheses, i.e., procedure specifications, as explained in due course.
            The heap is unbounded. The command x := new K allocates a fresh reference and maps
        it to an object of type K initialized with 0-equivalent values. In order to model real allocators,
        which may depend on state not visible at the language level, we assume an arbitrary choice
        function for fresh references, which may be, but need not be, nondeterministic.
            The semantics of formulas is standard. The points-to relation is defined by σ |= x.f = E
        iff σ(x) 6= null and σ(σ(x).f ) = σ(E). Quantifiers for reference types range over allocated
        non-null references: σ |= ∀x : K. P iff [σ+x: o] |= P for all o ∈ σ(alloc) of type K. (The
        notation indicates extending σ with x mapped to o.)
            The meaning of a correctness judgment is defined in terms of executions from initial
        configurations where the environment is empty (written _). Recall that in C there may be
        environment calls to procedures bound by let in C and there may also be context calls to
        procedures in a hypothesis context Φ. In the transition semantics, context calls take a single
        step to an outcome in accord with the specification: if the pre-state satisfies the precondition
        then the post-state satisfies the postcondition, and otherwise the outcome is fault ( ). In [5]
        and [38], this kind of semantics is defined in terms of a single transition relation for the
        procedure, which encodes under-specification by nondeterminacy. Here, a key design choice is
        to avoid nondeterminacy, to cater for simple semantics of relational properties. Following [7],
        this is achieved by semantics of correctness judgments in terms of all “interpretations” of the
        hypotheses, each interpretation being deterministic up to renaming of references. This is
        captured in the ∀∀ semantics of read effects (item (c) of Context Interpretation, below).9
            A location is a variable x or a pair o.f of a reference o and field f . Define rlocs(σ, ε), the
        locations designated in σ by read effects of ε, by rlocs(σ, ε) = {x | ε contains rd x} ∪ {o.f |
        ε contains rd G‘f with o ∈ σ(G)}. Define the wlocs(σ, ε) the same way but for write effects.
        Say τ can succeed σ, written σ ,→ τ , provided σ(alloc) ⊆ τ (alloc) and Type(o, σ) =
        Type(o, τ ) for all o ∈ σ(alloc). Define written(σ, τ ) to be {x | σ(x) 6= τ (x)} ∪ {o.f |
        σ(o.f ) 6= τ (o.f )}. Say ε allows change from σ to τ , written σ→τ |= ε, iff σ ,→ τ and


        9
            We have to deal with renaming of references in any case, even if the allocator is deterministic, to handle
            properties like noninterference for a program that allocates differently depending on secrets, or two
            versions of an algorithm using different pointer structures.
A. Banerjee, D. A. Naumann, and M. Nikouei                                                                   XX:19


written(σ, τ ) ⊆ wlocs(σ, ε).
     The semantics of read effects is more involved. Let π range over partial bijections on
Ref \{null}. Write π(p) = p0 to say that π is defined on p and has value p0 . A refperm
from σ to σ 0 is a partial bijection π such that dom (π) ⊆ σ(alloc), rng(π) ⊆ σ 0 (alloc), and
π(p) = p0 implies Type(p, σ) = Type(p0 , σ 0 ) for all proper references p, p0 . For references o, o0
          π                                                  π                                   π
define o ∼ o0 to mean o = null = o0 or π(o) = o0 . Extend ∼ to a relation on integers by i ∼ j
                                                 π
iff i = j. For reference sets X, Y , define X ∼ Y iff π(X) = Y , where π(X) is the direct
image of X. For a set W of locations, define Lagree(σ, σ 0 , π, W ) iff
                      π                                                   π
     ∀x ∈ W. σ(x) ∼ σ 0 (x) ∧ ∀(p.f ) ∈ W. p ∈ dom(π) ∧ σ(p.f ) ∼ σ 0 (π(p).f )

Say that σ and σ 0 agree on ε modulo π, written Agree(σ, σ 0 , ε, π), iff Lagree(σ, σ 0 , π, rlocs(σ, ε)).
   Note that Agree(σ, τ, rd G‘f, π) implies σ(G) ⊆ dom (π) but does not imply τ (G) ⊆ rng(π)
        π
or σ(G) ∼ τ (G).
   The next definitions are the basis for the semantics of read effects, which is a relational
property of two initial states σ, σ 0 and two final states τ, τ 0 .

Allowed dependence                                                                     σ, σ 0 ⇒τ, τ 0 |= ε

    freshRefs(σ, τ ) =
                     b τ (alloc)\σ(alloc)
                     b {p.f |p ∈ freshRefs(σ, τ ), f ∈ Fields(Type(p, τ ))}
    freshLocs(σ, τ ) =

Say ε allows dependence from τ, τ 0 to σ, σ 0 , written σ, σ 0 ⇒τ, τ 0 |= ε, iff for all π if
Agree(σ, σ 0 , ε, π) then there is ρ ⊇ π such that Lagree(τ, τ 0 , ρ, freshLocs(σ, τ ) ∪ written(σ, τ )).


    An interpretation returns a non-empty set of outcomes from each initial state (notation
Pne ).

Context interpretation                                                                         ϕ for Φ

For Φ well formed in Γ, a Φ-interpretation is a function ϕ with dom ϕ = dom Φ and for
each m : P ; Q [ε] in Φ, we have that ϕ(m) is a function [[Γ]] → Pne ([[Γ]] ∪ { }) such that
for all σ ∈ [[Γ]] we have

(a) ∈ ϕ(m)(σ) iff σ 6|= P , and also ∈ ϕ(m)(σ) implies ϕ(m)(σ) = { }.
(b) For all τ ∈ ϕ(m)(σ), if σ |= P then τ |= Q and σ→τ |= ε.
(c) For all τ, σ 0 , τ 0 , if σ |= P and σ 0 |= P and τ ∈ ϕ(m)(σ) and τ 0 ∈ ϕ(m)(σ 0 ), then
    σ, σ 0 ⇒τ, τ 0 |= ε.

    Owing to the second condition in (a), dubbed fault determinacy, we could as well
choose to treat ϕ(m) as a function with codomain Pne ([[Γ]]) ∪ { }, but the chosen formulation
slightly streamlines some definitions.
                              ϕ
    The transition relation 7−→ depends on an interpretation ϕ. Transitions act on configura-
tions where the environment µ has procedures distinct from those of ϕ. Aside from the use
of interpretations, the definition is mostly standard (and omitted). We assume Fresh is a
function such that, for any σ, Fresh(σ) a non-empty set of non-null references that are not
in σ(alloc).
                                                                                                      ϕ
Selected transition rules                                                                            7−→
XX:20   Relational logic with framing and hypotheses (Technical Report)


                µ(m) = C                                        τ ∈ ϕ(m)(σ)                        ∈ ϕ(m)(σ)
                      ϕ                                               ϕ                                     ϕ
        hm(), σ, µi 7−→ hC, σ, µi                    hm(), σ, µi 7−→ hskip, τ, µi             hm(), σ, µi 7−→

                                                 o ∈ Fresh(σ)
           Fields(K) = f : T        σ1 = “σ with o added to heap, with type K and default fields”
                                                        ϕ
                                  hx := new K, σ, µi 7−→ hskip, [σ1 | x : o], µi

                                   ϕ                                                           ϕ
        hlet m() = B in C, σ, µi 7−→ hC; elet(m) , σ, [µ+m: B]i               helet(m), σ, µi 7−→ hskip, σ, µmi



            The correctness judgment gives a modular form of partial correctness. The avoidance of
        faults says not only that there are no null dereferences but more importantly that no context
        procedure is called outside its specified precondition.
        Valid correctness judgment                                                         Φ |= C : P ; Q [ε]

        The judgment is valid iff the following conditions hold for all Φ-interpretations ϕ and all
        Γ-states σ such that σ |= P .
                                                            ϕ
        (Safety) It is not the case that hC, σ, _i 7−→∗           .
                                              ϕ
        And for every τ with hC, σ, _i 7−→∗ hskip, τ, _i we have

        (Post) τ |= Q
        (Write Effect) σ→τ |= ε
                                                          ϕ
        (Read Effect) For all σ 0 , τ 0 if hC, σ 0 , _i 7−→∗ hskip, τ 0 , _i and σ 0 |= P then σ, σ 0 ⇒τ, τ 0 |= ε


            Selected proof rules appear in Fig. 3. We proceed to some notions used in the rules,
        starting with read effects of formulas.
        Framing of formulas                                                                        P |= η frm Q

        P |= η frm Q iff for all σ, σ 0 , π, if Agree(σ, σ 0 , η, π) and σ |= P ∧ Q then σ 0 |= Q


            For atomic formulas, read effects can be computed syntactically by function ftpt. Two
        clauses of the definition [10] are ftpt(x) = rd x and ftpt(x.f = F ) = rd x, rd {x}‘f, ftpt(F ).
                                                                           π
        The basic lemma is that Agree(σ, σ 0 , ftpt(F ), π) implies σ(F ) ∼ σ 0 (F ).
            To express region disjointness we use a syntactic function ·/. defined by structural
        recursion on effects (see [10]). Please note that ·/. is not syntax in the logic; it’s a function in
        the metalanguage that is used to obtain formulas from effects. For example, r‘nxt ·/. r‘val
        is the formula true and r‘nxt ·/. s‘nxt is the formula r ∩ s ⊆ {null}. The key lemma is that
        the formula ε ·/. η holds in a state σ iff rlocs(σ, ε) ∩ wlocs(σ, η) = ∅.
            The subeffect judgment P |= ε ≤ η holds iff rlocs(σ, ε) ⊆ rlocs(σ, η) and wlocs(σ, ε) ⊆
        wlocs(σ, η) for all σ with σ |= P . The key lemma about subeffects is that if σ→τ |= ε and
        σ |= η ·/. ε and P |= ε ≤ η and σ |= P then Agree(σ, τ, η, id) where id is the identity on
        σ(alloc).
            Separator formulas are used in the notion of immunity, which amounts to framing for
        frame conditions. Expression G is P/ε-immune iff this is valid: P ⇒ ftpt(G) ·/. ε. Effect η
        is P/ε-immune iff G is P/ε-immune for every G with wr G‘f or rd G‘f in η.
            The key lemma about immunity is that if η is P/ε-immune, σ |= P , and σ→τ |= ε, then
        rlocs(σ, η) = rlocs(τ, η) and wlocs(σ, η) = wlocs(τ, η).
A. Banerjee, D. A. Naumann, and M. Nikouei                                                             XX:21



                      Φ ` C : P ; Q [ε]         P |= η frm R     P ∧ R ⇒ η ·/. ε
              Frame
                                     Φ ` C : P ∧ R ; Q ∧ R [ε]

                                                y 6≡ x
         FieldUpd
                      ` x.f := y : x 6= null ; x.f = y [wr {x}‘f, rd x, rd y]

                                 Fields(K) = f : T        default(T ) = v
       Alloc
                 ` x := new K : alloc = g ; alloc = g ∪ {x} ∧ x.f = v [wr x, rw alloc]

                                               Φ ` C1 : P ; P1 [ε1 ]
             Φ ` C2 : P1 ; Q [ε2 , rw H ‘f ]      P1 ⇒ H#g       ε2 is P/ε1 -immune      wr g 6∈ ε1
       Seq
                                   Φ ` C1 ; C2 : P ∧ g = alloc ; Q [ε1 , ε2 ]

     Figure 3 Selected unary proof rules (from [5, 7]).


    The preceding notions are concerned with protecting formulas and effects from the write
effects of a command. That is, framing and immunity are about preserving the value of an
expression or formula from one control point to a later one. To deal with read effects (and
other relations), agreements also need to be preserved. To this end we use the following
notion. An effect ε has framed reads provided that for every rd G‘f in ε, its footprint
ftpt(G) is in ε. For example, with r : rgn the effect rd r‘f does not have framed reads, but it
is a subeffect of rd r‘f, rd r which does. For ε that has framed reads, if Agree(σ, σ 0 , ε, π) then
       π
σ(G) ∼ σ 0 (G) for any rd G‘f in ε. In addition, a kind of symmetry holds: Agree(σ, σ 0 , ε, π)
implies Agree(σ 0 , σ, ε, π −1 ). This property implies what we need for preservation of effects
(see [7] for details).
    In this paper we assume without comment that all frame conditions in unary and relational
judgments have framed reads. (An alternative would be to change the semantics so that
effects are interpreted in terms of their ftpt-closure.)

 B       Relation formulas
Relational correctness judgments are typed in a context of the form Γ|Γ0 comprised of
contexts Γ and Γ0 for the left and right sides. For relation formulas, typing is reduced to
                                              (−           −
                                                           *
typing of unary formulas: Γ|Γ0 ` P iff Γ ` P and Γ0 ` P . This refers to the following.
Syntactic projections


      (−                                       −*
      /P           b P
                   =                           /P          b true
                                                           =
      (−                                       −*
      .P           b true
                   =                           .P          b P
                                                           =
      (−             (−                        −*            −
                                                             *
      P           b P
                   =                           P          b P
                                                           =
      (−−−−0                                   −−−−*0
      F =¨ F       b (F = F )
                   =                           F =¨ F      b (F 0 = F 0 )
                                                           =
      (−−−                                     −−−*
      AG‘f         b (G‘f = G‘f )
                   =                           AG‘f        b (G‘f = G‘f )
                                                           =
      (−−− 0
             −−−−−           −
                             (                 −−−−0−−−−*             −*
      ∀x|x : K. P =b ∀x : K. P                             b ∀x0 : K. P
                                               ∀x|x : K. P =


    Next are various notions used in the semantics of the program logic, starting with read
effects of formulas.
XX:22   Relational logic with framing and hypotheses (Technical Report)


        Relation formula semantics                                                             σ|σ 0 |=π P
         σ|σ 0 |=π /P      if f σ |= P
         σ|σ 0 |=π .P      if f σ 0 |= P
             0                         π
         σ|σ |=π F =  ¨ F if f σ(F ) ∼ σ 0 (F 0 )
                         0

         σ|σ |=π AG‘f if f Agree(σ, σ 0 , rd G‘f, π)
             0

         σ|σ 0 |=π P      if f ∃ρ. ρ ⊇ π and σ|σ 0 |=ρ P
         σ|σ |=π P ∧ Q if f σ|σ 0 |=π P and σ|σ 0 |=π Q
             0

         σ|σ 0 |=π P ⇒ Q if f σ|σ 0 |=π P implies σ|σ 0 |=π Q


           The framing judgment is like the unary one: P |= δ|δ 0 frm Q iff for all π, σ, σ 0 , τ, τ 0 , if
                                                                       Γ|Γ0                  Γ|Γ0
        Agree(σ, τ, δ, id) and Agree(σ 0 , τ 0 , δ 0 , id) and σ|σ 0 |=π P ∧ Q then τ |τ 0 |=π Q.

         C       Biprograms

                                                                                                  (− −*
        Biprograms: syntactic projections                                                         CC, CC
         (−−−−−−0−−−−−                     (−
         hCC, σ|σ , µ|µ0 i            = hCC, σ, µi
         (−−−−
         (C|C 0 )                     = C
         (−
         bAc                          = A
         (−−−−0−−−−−−−−−−−−−−                        (−     (−
         if E|E then BB else CC = if E then BB else CC
         (−−−−−−−   −−−−−−−−−−−                         (−
         while E|E 0 • P|P 0 do CC = while E do CC
         (−−−−−                            (− (−
         BB ; CC                      = BB ; CC
         (−−−−−−−−−0−−−−−−                               (−
         let m = (C|C ) in CC         = let m = C in CC
        We identify (skip; C) ≡ C, (C; skip) ≡ C, (skip|skip) ≡ bskipc and bskipc; CC ≡ CC. Thus,
                      (−−−−−−−−−−−−−−−
        for example, (skip|x := 0); by := 0c is y := 0.


            Typing of biprograms can be defined in terms of these meta-operators, roughly as
                            (−            −*
        Γ|Γ0 ` CC iff Γ ` CC and Γ0 ` CC. But the alignment guards P, P 0 in while should also be
        typechecked (by evident rules).
            Biprograms are given transition semantics, with configurations of the form hCC, σ|σ 0 , µ|µ0 i
        that represent an aligned pair of unary configurations. Environments are unchanged from
        unary semantics: µ and µ0 map procedure names to commands, not to biprograms. We lift
                                                      (−−−−−−−−−−−          (−
        the syntactic projections to configurations: hCC, σ|σ 0 , µ|µ0 i = hCC, σ, µi.
            We define suitable interpretations ϕ for relational specifications, used to define the
                              ϕ
        transition relation Z=⇒ for biprograms, analogous to the transition relation for unary programs.
        If Φ(m) is a relational specification, ϕ(m) maps initial state-pairs to non-empty sets of final
        pairs, or fault, in accord with the specification. The effect conditions are essentially lifted
        from the corresponding unary ones.
        Interpretation of relational specification

        An interpretation θ for R ≈> S [η|η 0 ], in context Γ|Γ0 , is a function

             θ : [[Γ]] × [[Γ0 ]] → Pne (([[Γ]] × [[Γ0 ]]) ∪ { })

        such that if (τ, τ 0 ) ∈ θ(σ, σ 0 ) then σ ,→ τ and σ 0 ,→ τ 0 . Moreover
A. Banerjee, D. A. Naumann, and M. Nikouei                                                                                   XX:23



                     hA, σ, µi 7−→ hskip, τ, νi              hA, σ 0 , µ0 i 7−→ hskip, τ 0 , ν 0 i
                                 *ϕ+                                           *ϕ+

            bSync                                        ϕ
                               hbAc, σ|σ 0 , µ|µ0 i Z=⇒ hbskipc, τ |τ 0 , ν|ν 0 i

                               hA, σ, µi 7−→                    hA, σ 0 , µ0 i 7−→
                                              *ϕ+                               *ϕ+
                                                       or
                   bSyncX                                             ϕ
                                         hbAc, σ|σ 0 , µ|µ0 i Z=⇒

                      (τ |τ 0 ) ∈ ϕ(m)(σ|σ 0 )                                                         ∈ ϕ(m)(σ|σ 0 )
 bCall                            ϕ                                               bCallX                                 ϕ
         hbm()c, σ|σ 0 , µ|µ0 i Z=⇒ hbskipc, τ |τ 0 , µ|µ0 i                                  hbm()c, σ|σ 0 , µ|µ0 i Z=⇒

                                        µ(m) = B                µ0 (m) = B 0
                  bCallE                                ϕ
                             hbm()c, σ|σ 0 , µ|µ0 i Z=⇒ h(B|B 0 ), σ|σ 0 , µ|µ0 i

                                          hC, σ, µi 7−→ hD, τ, νi
                                                        *ϕ+

                 bSplitL                                 ϕ
                            h(C|C 0 ), σ|σ 0 , µ|µ0 i Z=⇒ h(D|C 0 ), τ |σ 0 , ν|µ0 i

                                        hC 0 , σ 0 , µ0 i 7−→ hD0 , τ 0 , ν 0 i
                                                         *ϕ+

                bSplitR                                     ϕ
                           h(skip|C 0 ), σ|σ 0 , µ|µ0 i Z=⇒ h(skip|D0 ), σ|τ 0 , µ|ν 0 i

                    hC, σ, µi 7−→                                                        hC 0 , σ 0 , µ0 i 7−→
                                *ϕ+                                                                      *ϕ+

  bSplitLX                               ϕ                        bSplitRX                                       ϕ
              h(C|C 0 ), σ|σ 0 , µ|µ0 i Z=⇒                                       h(skip|C 0 ), σ|σ 0 , µ|µ0 i Z=⇒

                                      ν = [µ+m: C]              ν 0 = [µ0 +m: C 0 ]
         bLet                                                     ϕ
                hlet m = (C|C 0 ) in DD, σ|σ 0 , µ|µ0 i Z=⇒ hDD; belet(m)c, σ|σ 0 , ν|ν 0 i

                                        σ(E) = true = σ 0 (E 0 )
       bIfTT                                                           ϕ
                hif E|E 0 then CC else DD, σ|σ 0 , µ|µ0 i Z=⇒ hCC, σ|σ 0 , µ|µ0 i

                                              σ(E) 6= σ 0 (E 0 )
                   bIfX                                                              ϕ
                          hif E|E 0 then CC else DD, σ|σ 0 , µ|µ0 i Z=⇒

                                 σ(E) = false = σ 0 (E 0 )
   bIfFF                                                         ϕ
           hif E|E 0 then CC else DD, σ|σ 0 , µ|µ0 i Z=⇒ hDD, σ|σ 0 , µ|µ0 i

                                  ϕ                                                                                  ϕ
            hBB, σ|σ 0 , µ|µ0 i Z=⇒ hCC, τ |τ 0 , ν|ν 0 i                                      hBB, σ|σ 0 , µ|µ0 i Z=⇒
bSeq                              ϕ                                               bSeqX                                  ϕ
       hBB; DD, σ|σ 0 , µ|µ0 i Z=⇒ hCC; DD, τ |τ 0 , ν|ν 0 i                                hBB; DD, σ|σ 0 , µ|µ0 i Z=⇒

    Figure 4 Transition rules for biprograms, except biprogram loop (for which see Fig. 5).


(a) ∈ θ(σ, σ 0 ) iff ¬∃π. σ|σ 0 |=π R, and also                  ∈ θ(σ, σ 0 ) implies θ(σ, σ 0 ) = { }.
(b) for all σ, σ 0 and (τ, τ 0 ) in θ(σ, σ 0 ),
    (post) ∀π. (σ|σ 0 |=π R) ⇒ (τ |τ 0 |=π S)
    (write) σ→τ |= η and σ 0 →τ 0 |= η 0
    (read) For all π, σ̇, π̇, τ̇ ,
       (i) if σ|σ 0 |=π R and σ̇|σ 0 |=π̇;π R and (τ̇ , τ 0 ) ∈ θ(σ̇, σ 0 ) then σ̇, σ⇒τ̇ , τ |= η
       (ii) if σ|σ 0 |=π R and σ|σ̇ |=π;π̇ R and (τ, τ̇ ) ∈ θ(σ, σ̇) then σ 0, σ̇⇒τ 0, τ̇ |= η 0
XX:24   Relational logic with framing and hypotheses (Technical Report)



                                             σ(E) = true      σ|σ 0 |= P
                        bWhL                              (−
                                                      ϕ
                                hCC, σ|σ 0 , µ|µ0 i Z=⇒ h(BB|skip); CC, σ|σ 0 , µ|µ0 i

                                    σ|σ 0 6|= P      σ 0 (E 0 ) = true σ|σ 0 |= P 0
                       bWhR                                        −*
                                                      ϕ
                                hCC, σ|σ 0 , µ|µ0 i Z=⇒ h(skip|BB); CC, σ|σ 0 , µ|µ0 i

                                 σ|σ 0 6|= P       σ|σ 0 6|= P 0   σ(E) = true = σ 0 (E 0 )
                      bWhTT                                  ϕ
                                     hCC, σ|σ 0 , µ|µ0 i Z=⇒ hBB; CC, σ|σ 0 , µ|µ0 i

                                                  σ(E) = false = σ 0 (E 0 )
                           bWhFF                             ϕ
                                     hCC, σ|σ 0 , µ|µ0 i Z=⇒ hbskipc, σ|σ 0 , µ|µ0 i

                                        (σ(E) = true and σ 0 (E 0 ) = false and σ|σ 0 6|= P)
                                      or (σ(E) = false and σ 0 (E 0 ) = true and σ|σ 0 6|= P 0 )
                             bWhX                                             ϕ
                                                         hCC, σ|σ 0 , µ|µ0 i Z=⇒

           Figure 5 Transition rules for loops, in which we abbreviate CC ≡ while E|E 0 • P|P 0 do BB.


             As in the case of unary interpretations, the second part of (a) is dubbed fault determ-
        inacy.
             Note that the read and write effect conditions amount to their unary counterparts,
        imposed on both the left and right sides.
             Note also that (read)(i) is equivalent to: For all σ̇, τ̇ with (τ̇ , τ 0 ) ∈ θ(σ̇, σ 0 ), if there are
        π, π̇ such that σ|σ 0 |=π R and σ̇|σ 0 |=π̇;π R then σ̇, σ⇒τ̇ , τ |= η. Mutatis mutandis for (ii).
             Say ϕ is a Φ-interpretation if for each m in dom Φ with Φ(m) relational, ϕ(m) is an
        interpretation in the above sense. In case Φ(m) is unary, ϕ(m) is a context interpretation in
        the sense defined in Sec. A. The biprogram transition rules are in Figs. 4 and 5, on pages 23
        and 24. Some depend on unary transitions, for which purpose we write *ϕ+ for the restriction
        of ϕ to unary interpretations.

            [THIS SPACE INTENTIONALLY BLANK]
A. Banerjee, D. A. Naumann, and M. Nikouei                                                              XX:25


    The bIf* rules align the biprogram conditional; it faults if the same branch is not taken.
This embodies the purpose of the conditional biprogram, which is to indicate that the
guards can be proved to agree. Similarly for the loop transitions (Fig. 5). Notice that the
agreement checked by conditional/loop biprograms is agreement on boolean values. (Equality
of reference values would not make sense, and agreement modulo a refperm cannot be defined
because there are no refperms in the biprogram semantics.)
    For a given configuration, exactly one rule is applicable. For context call this fact relies
on two features of the semantics. One is that a hypothesis context maps a procedure name
to a single specification, either unary or relational. The other feature is “fault determinacy”
of interpretations, i.e., the second part of condition (a) in the definition of interpretation for
relational specifications, together with the similar condition (a) in the definition of context
interpretation for unary specifications.
    In all cases except where the active biprogram involves new or a procedure call, there is a
unique outcome. In case of context call, ϕ has either a unary or a relational interpretation,
and in either case the result may be nondeterministic; but it is determined modulo renaming
of references, owing to the read condition in the definitions of unary/relational context
interpretation. In the case of new, the transition rule will be one of bSync, bSplitL, and
bSplitR; any nondeterminacy in the the choice function for references is reflected in the
transitions.

 D      Relational proof rules

Valid relational judgment                                                     Φ ` CC : P ≈> Q [ε|ε0 ]

The judgment is valid iff the following holds for all states σ and σ 0 , Φ-interpretations ϕ, and
refperms π with σ|σ 0 |=π P:
                                                            ϕ
(Safety) It is not the case that hCC, σ|σ 0 , _ | _i Z=⇒∗        .
                                                   ϕ
And for all τ, τ 0 such that hCC, σ|σ 0 , _|_i Z=⇒∗ hbskipc, τ |τ 0 , _|_i

(Post) τ |τ 0 |=π Q
(Write Effect) σ→τ |= ε and σ 0 →τ 0 |= ε0
(Read Effect) For any ρ, σ̇, τ̇ ,
                               ϕ
   (i) if hCC, σ̇|σ 0 , _|_i Z=⇒∗ hbskipc, τ̇ |τ 0 , _|_i and σ̇|σ 0 |=(ρ;π) P then σ̇, σ⇒τ̇ , τ |= ε
                               ϕ
   (ii) if hCC, σ|σ̇, _|_i Z=⇒∗ hbskipc, τ |τ̇ , _|_i and σ|σ̇ |=(π;ρ) P then σ 0, σ̇⇒τ 0, τ̇ |= ε0


    In addition to the relational proof rules in Fig. 2, we give in Fig. 6 some additional rules
that have been proved sound.
    The rLater rule is used (with rConseq and   P ⇒ P) to derive a variation on rSeq
where the intermediate relation has  (see footnote 4).
    Rule rConseq includes a subeffect judgment P |= (ε|ε0 ) ≤ (η|η 0 ) which is a direct
generalization of subeffects in the unary logic.
    Rule rEqu uses unconditional program equivalence to rewrite the commands in a split, if
they differ only in the way their control flow is expressed, i.e., their behavior in all contexts
is the same. Commands C, C 0 are unconditionally equivalent, written C =         ∼ C 0 , iff for all
σ, τ, ϕ, D we have
                   ϕ                                    ϕ
(a) If hC, σ, µi 7−→∗ hskip, τ, µi then hC 0 , σ, µi 7−→∗ hskip, τ, µi.
                   ϕ              ϕ                        ϕ             ϕ
(b) If hC, σ, µi 7−→∗ hD, τ, νi 7−→ then hC 0 , σ, µi 7−→∗ hD0 , τ, νi 7−→            for some D0 .
XX:26   Relational logic with framing and hypotheses (Technical Report)




                                                                                    Φ ` CC : P ≈> Q [ε|ε0 ]
                                                                      rLater
           rCall     m : P ≈> Q [ε] ` bm()c : P ≈> Q [ε]                           Φ ` CC : P ≈> Q [ε|ε0 ]

                   Φ ` CC : P ≈> Q [ε|ε0 ]        P |= η|η 0 frm R      P ∧ R ⇒ /(η ·/. ε) ∧ .(η 0 ·/. ε0 )
         rFrame
                                           Φ ` CC : P ∧ R ≈> Q ∧ R [ε|ε0 ]

                              Φ ` C : P ; Q [ε]         Φ ` C 0 : P 0 ; Q0 [ε0 ]
                       rEmb
                               Φ ` (C|C 0 ) : /P ∧ .P 0 ≈> /Q ∧ .Q0 [ε|ε0 ]

                                           Φ ` CC1 : P ≈> P1 [ε1 |ε01 ]
                                                      −
                                                      (                                   −
                                                                                          *
                   Φ ` CC2 : P1 ≈> Q [ε2 |ε02 ] ε2 is P /ε1 -immune                ε02 is P /ε01 -immune
            rSeq
                                       Φ ` CC1 ; CC2 : P ≈> Q [ε1 , ε2 |ε01 , ε02 ]

                    (−                                                   −*
               Φ ` (CC|skip) : Q ∧ P ∧ /E ≈> Q [ε| ]       Φ ` (skip|CC) : Q ∧ P 0 ∧ .E 0 ≈> Q [ |ε0 ]
                                Φ ` CC : Q ∧ ¬P ∧ ¬P 0 ∧ /E ∧ .E 0 ≈> Q [ε|ε0 ]
                                                                                    (−
                 Q⇒E=   ¨ E 0 ∨ (P ∧ /E) ∨ (P 0 ∧ .E 0 )     Q ` ε|ε0 frm P    ε is P /ε-immune
                                                               −
                                                               *
                      P ⇒ P        Q ` ε|ε0 frm P 0     ε0 is P 0 /ε0 -immune   P 0 ⇒ P 0
         rWh
                         Φ ` while E|E 0 • P|P 0 do CC : Q ≈> Q [ε, ftpt(E)|ε0 , ftpt(E 0 )]

                       Φ ` (C|C 0 ) : P ≈> Q [ε|ε0 ]     C∼
                                                          =D          C0 ∼
                                                                         = D0
                rEqu                          0                  0
                                    Φ ` (D|D ) : P ≈> Q [ε|ε ]

                    Φ ` CC : P ≈> Q [ε|ε0 ]        R⇒P           Q⇒S          P |= (ε|ε0 ) ≤ (η|η 0 )
          rConseq
                                              Φ ` CC : R ≈> S [η|η 0 ]


          Figure 6 Additional relational proof rules.
A. Banerjee, D. A. Naumann, and M. Nikouei                                                     XX:27


(c) Mutatis mutandis for C 0 /C.

I Lemma 1. ∼  = is an equivalence relation and
                    ∼ while E do C; while E ∧ E0 do C od od
(a) while E do C od =
(b) while E do C od ∼
                    = if E do C fi; while E do C od
We also have C ∼   = skip; C; skip. This is an instance of reflexivity, because we identify
skip; C; skip with C.
    The weaving relation ,→ is defined inductively by axioms and congruence rules. Here
is the complete list of weaving axioms, each of which replaces a split by one of the other
biprogram forms:

      (A|A) ,→ bAc
      (C; D | C 0 ; D0 ) ,→ (C|C 0 ); (D|D0 )
      (if E then C else D | if E 0 then C 0 else D0 ) ,→ if E|E 0 then (C|C 0 ) else (D|D0 )
      (while E do C | while E 0 do C 0 ) ,→ while E|E 0 • P|P 0 do (C|C 0 )
      (let m = B in C | let m = B 0 in C 0 ) ,→ let m = (B|B 0 ) in (C|C 0 )

Here is the complete list of congruence rules. Each is formulated in terms of a single sub-
biprogram, for technical convenience. The premise in each case is BB ,→ CC; the conclusions
are
      BB; DD ,→ CC; DD
      DD; BB ,→ DD; CC
      if E|E 0 then BB else DD ,→ if E|E 0 then CC else DD
      if E|E 0 then DD else BB ,→ if E|E 0 then DD else CC
      while E|E 0 • P|P 0 do BB ,→ while E|E 0 • P|P 0 do CC
      let m = (B|B 0 ) in BB ,→ let m = (B|B 0 ) in CC

   At this point we have defined the syntax and semantics of the logic. In the following
sections we apply the logic to examples. Then Sections H and I justify the semantics and
prove the rules sound.

 E      Proof for example of “dissonant” loop
Example C1 , discussed in Secs. 2 and 3, shows the use of alignment guards to achieve
intermittent alignment of iterations. It also uses a region variable, r, to express frame
conditions for heap locations.

C1 =
   b     s := 0; while p 6= null do
                   if ¬p.del then s := s + p.val fi
                   p := p.nxt;
                 od
Let

 b rw s, rw p, rd r, rd r‘val, rd r‘nxt, rd r‘del
ε=

We want to prove the judgment

      (C1 |C1 ) : B(p ∈ r ∧ r‘nxt ⊆ r) ∧ listnd(p) =
                                                   ¨ listnd(p) ≈> s =
                                                                    ¨ s [ε]

Let
XX:28   Relational logic with framing and hypotheses (Technical Report)


         b if ¬p.del then s := s + p.val if
        B=

        D=
         b B; p := p.nxt;

        DD =
           b    while p 6= null | p 6= null · /p.del | .p.del do
                                (D|D) od

        We have (C1 |C1 ) ,→∗ bs := 0c; DD. By rule rWeave (in Fig. 2, Sec. 6), it is enough to
        prove

            bs := 0c; DD :     B(p ∈ r ∧ r‘nxt ⊆ r) ∧ listnd(p) =
                                                                ¨ listnd(p) ≈> s =
                                                                                 ¨ s [ε]

        By a unary judgment then rEmb (Fig. 2) and rConseq (Sec. D) we have

           bs := 0c : true ≈> s =
                                ¨ s [wr s]

        By rFrame and rConseq (for subeffects) we have

            bs := 0c : B(p ∈ r ∧ r‘nxt ⊆ r) ∧ listnd(p) =
                                                        ¨ listnd(p) ≈>
            B(p ∈ r ∧ r‘nxt ⊆ r) ∧ listnd(p) =
                                             ¨ listnd(p) ∧ s =
                                                             ¨ s [ε | ε]

        By rSeq, it is enough to show that

           DD : Q ≈> Q [ε | ε]

        where

         b B(p ∈ r ∧ r‘nxt ⊆ r) ∧ listnd(p) =
        Q=                                  ¨ listnd(p) ∧ s =
                                                            ¨ s

        which will serve as loop invariant in rWh. We have

           Q ⇒ (p = null =
                         ¨ p = null) ∨ /(p.del ∧ p 6= null) ∨ .(p.del ∧ p 6= null)

        The consequent follows from listnd(p) =
                                              ¨ listnd(p). It remains to prove the following three
        judgments:

                (D|skip) : Q ∧ /(p.del ∧ p 6= null) ≈> Q [ε |]                                   (9)
                (skip|D) : Q ∧ .(p.del ∧ p 6= null) ≈> Q [| ε]                                  (10)
                (D|D) : Q ∧ B(¬p.del ∧ p 6= null) ≈> Q [ε | ε]                                  (11)

        (That is, the three premises of rWh, after some simplification.) To prove these, we use
        unary judgments and then embed. Add variables t and l for use in assertions. By If we have

           B : p.del ∧ p 6= null ∧ t = s ; t = s [wr s]

        By Frame we get

            B : p.del ∧ p 6= null ∧ t = s ∧ (p ∈ r ∧ r‘nxt ⊆ r ∧ l = listnd(p))
            ; t = s ∧ (p ∈ r ∧ r‘nxt ⊆ r ∧ l = listnd(p)) [η]

        where η is ε\wr p. For p := p.nxt we use the local axiom for field read, together with Conseq
        to reason using the mathematical fact p 6= null ∧ p.del ⇒ listnd(p) = listnd(p.nxt). Then by
        Seq we get

            D : p ∈ r ∧ r‘nxt ⊆ r ∧ l = listnd(p) ∧ t = s ∧ p.del∧
            p 6= null ; p ∈ r ∧ r‘nxt ⊆ r ∧ l = listnd(p) ∧ t = s [ε]
A. Banerjee, D. A. Naumann, and M. Nikouei                                                          XX:29


On the other hand, we have

      skip : p ∈ r ∧ r‘nxt ⊆ r ∧ l = listnd(p) ∧ t = s
      ; p ∈ r ∧ r‘nxt ⊆ r ∧ l = listnd(p) ∧ t = s [ε]

Since t and l are not written, we can use rEmb, rFrame, and rConseq to get (9) and (10).
To be precise, we need the usual ∃-elimination rule (e.g., [10]), to eliminate the preconditions
t = s and l = listnd(p). For (11) one could weave (D|D) but there’s no need to. Similar
steps to the preceding ones can be used to obtain (11).
    Finally, the sequence and loop rules have immunity side conditions, variations on ε
being true/ε-immune. In brief, this condition simplifies to true because the assigned
variables s and p do not occur in region expressions in ε. In more detail, notice that the
only image expressions in ε are r‘val, r‘nxt, r‘del. Applying the ·/. operator, we find that
rd r‘val, r‘nxt, r‘del, r ·/. wr s, p trivially simplifies to true.


 F      Loop tiling example

Loop tiling is a compiler optimization that changes program structure. Here is an example
from [12].

  C2 =b x := 0; while x < N ∗ M do a[x] := f (x); x++ od
  C20 =
      b i := 0; while i < N do j := 0; while j < M do A[i, j] := f (i ∗ M + j); j ++ od; i++ od

These are not equivalent, but are equivalent modulo change of data representation. We
express this by the judgment

     (C2 |C20 ) : Btrue ≈> R(M ∗ N, N, M )                                                  (12)

R(x, i, j) =
           b ∀l, r, s. 0 ≤ l < x ∧ 0 ≤ r < i ∧ 0 ≤ s < i ∧ l = r ∗ M + s ⇒ a[l] =
                                                                                ¨ A[r, s]

To prove it, we rely on some unconditional program equivalences that change the control
structure without altering the order of atomic commands (see Lemma 1). First, rewrite C2
and C20 to

C3 =
   b     x := 0; while x < N ∗ M do
                   skip; a[x] := f (x); x++;
                   while x < M ∗ N ∧ x%M 6= 0 do
                      a[x] := f (x); x++ od;
                   skip; od

C30 =
    b    i := 0; while i < N do j := 0;
                   if j < M then A[i, j] := f (i ∗ M + j); j ++ fi
                   while j < M do A[i, j] := f (i ∗ M + j); j ++ od
                   i++ od

These rewrites change the control state without altering the trace of data states (modulo
stuttering). Formally, C2 ∼= C3 and C20 ∼  = C30 , where ∼
                                                         = means unconditional equivalence and
is defined in Sec. D. We apply the relational proof rule rEqu, that is, (C2 |C20 ) satisfies the
specification in (12) if (C3 |C30 ) does. The rewrites are chosen so that we can weave (C3 |C30 )
XX:30   Relational logic with framing and hypotheses (Technical Report)


        to the carefully aligned biprogram

              (x := 0 | i := 0);
              while x < N ∗ M | i < N do
                (skip | j := 0);                                                         
                  a[x] := f (x); x++     if j < M then A[i, j] := f (i ∗ M + j); j ++ fi
                while x > M ∗ N ∧ x%M 6= 0 | j < M do
                   (a[x] := f (x); x++ | A[i, j] := f (i ∗ M + j); j ++)
                od;
                (skip | i++)
              od

        To prove that this satisfies Btrue ≈> R(M ∗ N, N, M ), we use x =  ¨ i × M + j ∧ R(x, i, j) as
        the invariant for inner loop and x =¨ i × M ∧ R(x, i, 0) as the invariant of the outer loop.

         G       Proof for Stack example
        In this section we provide a more detailed proof of equivalence for data representation
        example. The sketch of the proof given in Section 3 glossed over dynamic allocation. To
        fully consider dynamic allocation we use rule Alloc in Fig. 3 for unary judgments and the
        axiom of allocation mentioned in Sec. 6. According to these rules we need to change η in (6)
        to the following:

              b rw rep, size, rep‘any, alloc
             η=

        and we also add  to the postcondition in (7). We will use the fact, noted in Sec. 4, that

             P ∧ Q ⇒ (P ∧ Q)          is valid (for any P and any monotonic Q)                    (13)

            Recall that Φ on page 8 gives the relational specification for push. To show (B|B 0 )
        satisfies the relational specification for push, we weave it to

                top := new N ode(top, x); if slots = null then . . . fi; 
                                                                           ;
                rep := rep ∪ {top}         slots[f ree++] := x
                                      bsize++c

        Let D and D0 name the split parts, so the woven code has the form (D|D0 ); bsize++c. By
        unary reasoning and applying rules rEmb, rFrame, and rConseq, we can show that (D|D0 )
        satisifies
              BR ∧ L ∧ A(size, x) ≈> LtR ∧ /I ∧ .I10 ∧ A(size, x)
                                                                                                    (14)
              [rw top, rep, rep‘any | rw slots, f ree, rep]

        Here I10 is a slight variant of I 0 , where the last conjunct is f ree = size + 1. By unary logic
        we get

              size++ : I ; (size = old(size) + 1) ∧ I [rw size]
              size++ : I10 ; (size = old(size) + 1) ∧ I 0 [rw size]

        An embedding rule lifts these to a relational judgment with agreements, and then rFrame
        for LtR yields

             bsize++c : LtR ∧ /I ∧ .I10
                        ≈> B(size = old(size) + 1) ∧ Asize ∧ L [rw size]
A. Banerjee, D. A. Naumann, and M. Nikouei                                                       XX:31


which by rConseq shows that bsize++c satisfies

   LtR ∧ /I ∧ .I10 ∧ Asize ≈> BS ∧ Asize ∧ L [rw size]                                   (15)

From (14) and (15) by rule rSeq we get that (D|D0 ); bsize++c satisfies the specification for
push. Hence by the weaving rule so does (B|B 0 ).
   Now we aim to prove the revised version of (7), that is,

   TCliU : B(size = 0) ∧ L ≈> (A(p, size) ∧ A{p}‘any ∧ L)

where TCliU is the fully aligned biprogram

   bpush(1)c; bp := new N ode(null, 2)c; bp.val := 3c; bpush(4)c

   The first command is a method call to push. From rule rCall and the relational
specification Φ of push, we derive

   bpush(1)c : BR ∧ Asize ∧ L ≈> (BS ∧ Asize ∧ L)
               [η, rw top | η, rw slots, f ree]

Notice that B(size = 0) ∧ L implies BR ∧ Asize ∧ L. Using rule rConseq and a little sleight
of hand we get

   bpush(1)c : B(size = 0) ∧ L ≈>                                                        (16)
               (B(size = 1 ∧ r = alloc ∧ rep ⊆ r) ∧ Asize ∧ L)
               [η, rw top | η, rw slots, f ree]

The sleight of hand is to introduce a fresh ghost variable r to snapshot alloc. (The condition
rep ⊆ r follows from r = alloc.) An entirely rigorous proof would add an assignment to r
but for clarity we will skip that.
   The second command in TCliU is allocation. Using the axiom of allocation mentioned
above, we derive

    bp := new N ode(null, 2)c : B(r = alloc) ≈>
    (B(p 6= null ∧ p ∈
                      / r) ∧ A(p, {p}‘any))
    [wr p, rw alloc]

We aim to frame rep ⊆ r over this judgment. Note that rd rep, r frames rep ⊆ r and
rd rep, r ·/. wr p, rw alloc. By rules rFrame, and rConseq using the validity (13), we get

    bp := new N ode(null, 2)c : B(r = alloc ∧ rep ⊆ r) ≈>
    (B(p 6= null ∧ p ∈
                      / r ∧ rep ⊆ r) ∧ A(p, {p}‘any))
    [wr p, rw alloc]

Using rConseq we rewrite the postcondition to get

    bp := new N ode(null, 2)c : B(r = alloc ∧ rep ⊆ r) ≈>
    (B(p 6= null ∧ p ∈
                      / rep) ∧ A(p, {p}‘any))                                            (17)
    [wr p, rw alloc]

For the third command we use the unary FieldUpd and rEmb and rConseq to get

   bp.val := 3c : B(p 6= null) ∧ A(p) ≈> A(p.val)[rd p, wr p.val]
XX:32   Relational logic with framing and hypotheses (Technical Report)


        We aim to use rFrame on this last judgment to add Ap, {p}‘nxt ∧ B(p ∈     / rep) to precondition
        and postcondition of this last judgment. Note that rd p, {p}‘nxt, rep frames A(p, {p}‘nxt) ∧
        B(p ∈
            / rep). And rd p, {p}‘nxt, rep ·/. rd p, wr p.val simplifies to true. Using these two facts
        and rule rFrame we derive

            bp.val := 3c : B(p 6= null ∧ p ∈
                                           / rep) ∧ A(p, {p}‘nxt) ≈>
            B(p ∈/ rep) ∧ A(p, {p}‘nxt, {p}‘val)
            [rd p, wr p.val]

        Now we use rule rConseq and rLater to get

            bp.val := 3c :
            (B(p 6= null ∧ p ∈
                              / rep) ∧ A(p, {p}‘nxt))                                              (18)
            ≈> (B(p ∈/ rep) ∧ A(p, {p}‘any))[rd p, rw p.val]

        The judgments (17) and (18) are now ready to be unified by rule rSeq. So, from rSeq we
        derive

            bp := new N ode(null, 2)c; bp.val := 3c : B(r = alloc ∧ rep ⊆ r)
            ≈> (B(p ∈
                     / rep) ∧ A(p, {p}‘any))[rw p, alloc]

        Actually we need to use the general form of rSeq which, like Seq, lets us remove rw p.val
        from the overall effects of this last judgment. The general form of the rSeq indicates that if
        in the first command some references are allocated and the second commands writes some
        fields of these newly allocated references then the second command’s effects should have
        writes as well as reads of these fields.
            Now we frame B(size = 1) ∧ Asize ∧ L over the last judgment.

            bp := new N ode(null, 2)c; bp.val := 3c :
            B(size = 1 ∧ r = alloc ∧ rep ⊆ r) ∧ Asize ∧ L
            ≈> (B(p ∈  / rep) ∧ A(p, {p}‘any)) ∧ B(size = 1) ∧ Asize ∧ L
            [rw p, alloc]

        Now by rConseq we get.

            bp := new N ode(null, 2)c; bp.val := 3c :
            B(size = 1 ∧ r = alloc ∧ rep ⊆ r) ∧ Asize ∧ L
            ≈> (B(p ∈  / rep) ∧ A(p, {p}‘any, size) ∧ B(size = 1) ∧ L)
            [rw p, alloc]

        Now using rLater, followed by rConseq instantiating the valid formula   P ⇒ P we get

            bp := new N ode(null, 2)c; bp.val := 3c :
            (B(size = 1 ∧ r = alloc ∧ rep ⊆ r) ∧ Asize ∧ L)
            ≈> (B(p ∈  / rep) ∧ A(p, {p}‘any, size) ∧ B(size = 1) ∧ L)
            [rw p, alloc]

        Using rSeq on (16) and the last judgment we get

            bpush(1)c; bp := new N ode(null, 2)c; bp.val := 3c :
            B(size = 0) ∧ L ≈>
            (B(size = 1 ∧ p ∈   / rep) ∧ A(p, {p}‘any, size) ∧ L)
            [η, rw top, p | η, rw slots, f ree, p]
A. Banerjee, D. A. Naumann, and M. Nikouei                                                                     XX:33


Using rConseq to remove B(p ∈
                            / rep) from postcondition, we get

      bpush(1)c; bp := new N ode(null, 2)c; bp.val := 3c :
      B(size = 0) ∧ L ≈> (B(size = 1) ∧ A(p, {p}‘any, size) ∧ L)                                     (19)
      [η, rw top, p | η, rw slots, f ree, p]

For the last command we use rCall similar to (16) to get

     bpush(4)c : BR ∧ Asize ∧ L ≈> (BS ∧ Asize ∧ L)
                 [η, rw top | η, rw slots, f ree]

We use rConseq we derive

     bpush(4)c : B(size = 1) ∧ Asize ∧ L ≈> (Asize ∧ L)
                 [η, rw top | η, rw slots, f ree]

Using rFrame and rConseq we derive

     bpush(4)c : B(size = 1) ∧ A(p, {p}‘any, size) ∧ L ≈>
                 A(p, {p}‘any, size) ∧ L[η, rw top | η, rw slots, f ree]

To add the last command to (19), we use rSeq to derive

      TCliU : B(size = 0) ∧ L ≈> A(p, {p}‘any, size) ∧ L
      [η, rw top, p | η, rw slots, f ree, p]

This finishes the proof.

 H       Semantic consistency theorem
The ultimate point of the relational logic is to prove relational properties of ordinary programs.
Theorem 2 connects biprogram semantics with unary semantics, for hypothesis contexts that
have only unary specifications. Such contexts model ambient libraries, and are meaningful
for biprograms as well as for ordinary commands. By contrast, relational hypotheses can be
introduced by rule rLink for modular relational reasoning about linked subprograms.

I Theorem 2 (semantic consistency). Suppose Φ has only unary specifications. Suppose
Φ ` (C|C 0 ) : P ≈> Q [ε|ε0 ] is valid. Consider any Φ-interpretation ϕ. Consider any σ, σ 0 , π
                                 ϕ                                     ϕ
with σ|σ 0 |=π P. If hC, σ, _i 7−→∗ hskip, τ, _i and hC 0 , σ 0 , _i 7−→∗ hskip, τ 0 , _i then τ |τ 0 |=π Q.
Furthermore, if C does not diverge from σ then both of these initial configurations are safe
(i.e., do not fault).

     To prove the theorem we use lemmas that connect biprogram and unary semantics; these
lemmas are also used in proving soundness for some of the proof rules.
     A trace is a consecutive sequence of configurations, numbered from 0. Let T be a
biprogram trace and U, V unary traces. A schedule of U, V for T is a pair l, r with
l : (dom (T )) → (dom (U )) and r : (dom (T )) → (dom (V )), each surjective and monotonic.
(For example, look at the sketches in Sec. 5, where the dashed lines indicate how indices of
the biprogram trace are mapped by l and r.) A schedule l, r is an alignment of U, V for T ,
                                           −
                                           (              −
                                                          *
written align(l, r, T, U, V ), iff Ul(i) = Ti and Vr(i) = Ti for all i in dom (T ).
     It is convenient to classify the biprogram transition rules as follows. Rules bSeq and
bSeqX simply close the transitions under command sequencing. All the other rules apply
XX:34   Relational logic with framing and hypotheses (Technical Report)


        to a non-sequence biprogram of some form; for any biprogram configuration that is not
        terminated, there is a unique one of these rules that applies. In the case of context calls, this
        is a consequence of a condition (fault determinacy) in the definition of context interpretation.
        We dub this rule determinacy. One consequence is that if a configuration can step to fault
        then that is the only possible step.
            Among these non-sequence rules, bSplitL, bSplitLX, and bWhL take left-only steps,
        leaving the right side unchanged; whereas bSplitR, bSplitRX, and bWhR take right-only
        steps. All the other rules are for both-sides steps.
        I Lemma 3 (bi-to-unary correspondence). Suppose ϕ is a Φ-interpretation, with only unary
                                                                  ϕ
        specifications. (a) For any step hBB, σ|σ 0 , µ|µ0 i Z=⇒ hCC, τ |τ 0 , ν|ν 0 i, we have either
         (−            (−           (−          ϕ   ( −
        hBB, σ, µi = hCC, τ, νi or hBB, σ, µi 7−→ hCC, τ, νi. Mutatis mutandis for the right. (b) For
                          ϕ                                     ϕ
        any trace T via Z=⇒, there are unique traces U, V via 7−→ and l, r such that align(l, r, T, U, V ).
        Proof. Part (a) is by case analysis of the biprogram transition rules. Rules bCall and
        bCallX are not relevant because they are for relational specifications and ϕ has only unary
        ones. In all other cases, it is straightforward to check that the rule corresponds to a unary
        step on one or both sides, and in case it is a step on just one side the other side remains
        unchanged.
            For part (b) the proof goes by induction on T and case analysis on the rule by which the
        last step was taken. Recall that traces are indexed from 0. The base case is T comprised
                                                      (−        −
                                                                *
        of a single configuration, T0 . Let U be T0 , V be T0 , and let both l and r be the singleton
        mapping {(0, 0)}. For the induction step, suppose T has length n + 1 and let S be the prefix
        including all but the last configuration Tn . By induction hypothesis we get l, r, U, V such
        that align(l, r, S, U, V ). There are three sub-cases, depending on whether the step from Tn−1
        to Tn is a left-only step (rule bSplitL or bWhL), or right-only, or both sides. In the case
                                    (−
        of left-only, Let U 0 be U Tn , let l0 be l ∪ {(n, len(U ))}. Then align(l0 , r, T, U 0 , V ). The other
        two sub-cases are similar.                                                                            J

           Next, we need a result going from unary to biprogram traces, which is more intricate.
        I Lemma 4 (unary-to-bi correspondence). Suppose Φ has only unary specifications, and ϕ is
                                                                                               (−
        a Φ-interpretation. Let cf g be a biprogram configuration. Let U be a trace via ϕ from cf g,
                           −*                                                            (−
        and V via ϕ from cf g. Then there is trace T via ϕ from cf g and traces W from cf g and X
             −*
        from cf g and l, r with align(l, r, T, W, X), such that either
          (a) U ≤ W and V ≤ X,
          (b) U ≤ W and W faults next and so does T ,
          (c) V ≤ X and X faults next and so does T ,
          (d) U ≤ W and W is diverging and so is T ,
          (e) V ≤ X and X is diverging and so is T , or
          (f) W ≤ U or X ≤ V and the last configuration of T (which is aligned with the last ones
           of W and X) faults due to lack of agreement for if-biprogram or while-biprogram, i.e.,
           transitions bWhX, bIfX.
        Moreover, if U, V are the projections of a biprogram trace (see Lemma 3) then case (f) does
        not occur.
        Proof. First, we define an iterative procedure in which l, r, W, X, T are treated as mutable
        variables. It maintains this invariant:
           align(l, r, T, W, X) and (U ≤ W ∨ W ≤ U ) and (V ≤ X ∨ X ≤ V )
A. Banerjee, D. A. Naumann, and M. Nikouei                                                                 XX:35


                                             (− −*
• Initialize W, X, T to the singleton traces cf g, cf g, and cf g respectively. Let l(0) = 0 and
r(0) = 0 (and otherwise l and r are undefined).
• While (U  W or V  X) and neither W , X, nor T faults next, do the following:


  (step A) Let k = len(T ) − 1, so k is the index of the last configuration of T . Note that
   l(k) and r(k) index the last configurations of U and W respectively.
  (step B) If the rule that applies to Tk is a left-only step (rule tSplitL or tWhL, since
   T does not fault next), then extend l by l(k + 1) = l(k) + 1 (noting this is less than
   len(U ) because the loop guard and invariant imply W is a strict prefix of U ) and extend
   r by r(k + 1) = r(k). If right-only, extend by r(k + 1) = r(k) + 1 and l(k + 1) = l(k).
   Otherwise, extend l(k + 1) = l(k) + 1 and r(k + 1) = r(k) + 1.
                                            ϕ
  (step C) Extend T by one step via Z=⇒. There may be nondeterministic choices to make
   on one or both sides, due to allocation and due to context calls; resolve these choices to
   match the configurations Ul(k+1) and/or Vr(k+1) . For allocation, this can be done because
                                   ϕ        ϕ
   the same allocator is used by 7−→ and Z=⇒. For context call, this can be done because
   the same interpretation is used. (Because ϕ has only unary specifications, context calls
   go by rule bSync, bSplitL, or bSplitR, not bCall.)

                                                                                  (−
To see that the invariant holds following step C, note that the invariant implies Tk = Wl(k)
     −
     *
and Tk = Xr(k) , for k = len(T ) − 1. Then by construction we get a match for the new
               (−−                   −−*
configuration: Tk+1 = Wl(k+1) and Tk+1 = Xr(k+1) .
    Now we can prove the lemma. If the loop terminates because guard condition (U 
W ∨ V  X) became false then we have (a). If it terminates because W faults next then we
have (b), using invariant (U ≤ W ∨ W ≤ U ). Similarly, we get (c) if it terminates because
X faults next. If it terminates because T faults, and case (a) does not hold, then we have (f)
owing to the invariants U ≤ W ∨ W ≤ U and V ≤ X ∨ X ≤ V . If the loop fails to terminate
we get (d) or (e). The reason is that every iteration lengthens both T and either W or X
(or both), so eventually either U ≤ W or V ≤ X. It is possible for left-only steps to diverge
while V is still a proper prefix of X, as shown in earlier examples, and then we have (d);
mutatis mutandis for (e).
    Finally, suppose U, V are the projections of a biprogram trace S (see Lemma 3). Then case
(f) cannot happen: T cannot fault until at least S ≤ T , at which point the loop terminates
and case (a) applies.                                                                      J



Proof Theorem 2.

Given terminated traces U and V of hC, σ, µi and hC 0 , σ 0 , µ0 i, we can apply Lemma 4 to
obtain a trace T of h(C|C 0 ), σ|σ 0 , µ|µ0 i for which condition (a) in the Lemma holds. By
correspondence (Lemma 3(a)), T must be terminated, so by the correctness judgment we
get Q in the final state. To prove safety, suppose hC, σ, µi can fault. Then by semantics,
h(C|C 0 ), σ|σ 0 , µ|µ0 i takes left-only steps until it reaches the fault, contrary to the assumed
correctness judgment. Suppose hC 0 , σ 0 , µ0 i can fault. By semantics, and the assumption
that C does not diverge from σ, h(C|C 0 ), σ|σ 0 , µ|µ0 i reaches h(skip|C 0 ), τ |σ 0 , µ|µ0 i for some
τ , and then proceeds with right-only steps for C 0 . So a fault of C 0 gives rise to a fault of
(C|C 0 ), contrary to the assumed correctness judgment.
XX:36   Relational logic with framing and hypotheses (Technical Report)


         I     Soundness theorem
        I Theorem 5. All the proof rules for relational correctness judgments are sound with respect
        to the semantics in Sec. D.

            The soundness proofs are straightforward for many of the rules. As noted in the body
        of the paper, the proof for rLink (Fig. 2) follows the lines of the soundness proof for the
        linking rules in [5] and [7]. It involves induction on biprogram traces, and the relational
        hypothesis can be used because the relevant context calls are aligned.

        Soundness of rule rWeave
        We prove this rule in detail. The argument may illuminate some design choices in the
        semantics of biprograms.
           We write ≡ for syntactic identity.
                                                        (− (−−      −* −−*
        I Lemma 6 (weave and project). If CC ,→ DD then CC ≡ DD and CC ≡ DD.

        Proof. By induction on the rules for ,→ (near the end of Sec. D), making straightforward
        use of the definitions of the syntactic projections.
                                                         (−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
            As an example, for the if-else axiom we have (if E then C else D | if E 0 then C 0 else D0 ) ≡
                                          (−−−−      (−−−− (−−−−−−−−−−−−−−−−−−−−−−−
        if E then C else D ≡ if E then (C|C 0 ) else (D|D0 ) ≡ if E|E 0 then (C|C 0 ) else (D|D0 ).
            As an example inductive case, for the rule from BB ,→ CC infer BB; DD ,→ CC; DD,
                 (−−−−− (− (−− (− (−− (−−−−−
        we have BB; DD ≡ BB; DD ≡ CC; DD ≡ CC; DD where the middle step is by induction
        hypothesis.                                                                                      J

        I Lemma 7 (weave and trace). Suppose Φ has only unary specifications, BB ,→ CC, and
                                                            ϕ
        ϕ is a Φ-interpretation. If hBB, σ|σ 0 , µ|µ0 i Z=⇒∗ hbskipc, τ |τ 0 , µ|µ0 i then hCC, σ|σ 0 , µ|µ0 i
                                                          ϕ
        either faults, diverges, or hCC, σ|σ 0 , µ|µ0 i Z=⇒∗ hbskipc, τ |τ 0 , µ|µ0 i (for any σ, σ 0 , τ, τ 0 , µ, µ0 ).

        Proof. Consider any trace T of BB from σ|σ 0 . Let U, V be the corresponding unary traces,
        given by Lemma 3(b). In light of Lemma 6, we can obtain a trace T̂ from hCC, σ|σ 0 , _|_i
        satisfying the conditions of Lemma 4.
            Suppose in particular that T is a trace from hBB, σ|σ 0 , µ|µ0 i that terminates in
        hbskipc, τ |τ 0 , µ|µ0 i. Conditions (d) and (e) in Lemma 4 imply that T̂ diverges; then we
        are done. Conditions (b), (c), and (f) all imply that hCC, σ|σ 0 , µ|µ0 i faults; again we are
        done. The remaining condition, (a), implies that T̂ covers all the steps of T and since T is
        terminated, so is T̂ . The align conditions of Lemmas 3 and 4 imply that the final states of
        T̂ are τ, τ 0 .                                                                             J

             Now we can prove soundness of rule rWeave.

        Proof. Suppose the premise and side conditions hold:
           Φ |= DD : P ≈> Q [ε].
           CC ,→ DD
           Φ has only unary specifications
           (−−                        (−                −−*                     −*
           DD terminates from any P -state, and DD terminates from any P -state.
        To show the conclusion Φ |= CC : P ≈> Q [ε] (as per the semantics of judgments, in Sec. D),
        consider any Φ-interpretation ϕ. Consider any π and any σ, σ 0 such that σ|σ 0 |=π P. Suppose
        CC terminates from σ|σ 0 in final states τ |τ 0 . By Lemma 7, execution of DD from σ|σ 0 either
        faults, diverges, or terminates in τ |τ 0 . It cannot fault, owing to the premise for DD. It
A. Banerjee, D. A. Naumann, and M. Nikouei                                                                          XX:37


cannot diverge: Because if the traces of DD from σ|σ 0 could be extended without bound,
                                   (−−
then by Lemma 3 either traces of DD from σ could be extended without bound, or traces
    −−*                                                                           (−
of DD from σ 0 could be—which contradicts the termination conditions, since σ |= P and
       −
       *               (− − *
σ 0 |= P (because P ⇒ P ∧ P is valid). So DD terminates in τ |τ 0 . Now conditions (Post),
(Write Effect), and (Read Effect) for CC are immediate from the premise for DD.
     It remains to show that safety for CC follows from safety for DD. This is a direct
consequence of a general property of weaving, which we state as Lemma 8.               J

I Lemma 8. Consider any CC, DD such that CC ,→ DD. Consider any interpretation ϕ
of some Φ with only unary specifications.10 For any σ, σ 0 , µ, µ0 , if hCC, σ|σ 0 , µ|µ0 i can fault
then hDD, σ|σ 0 , µ|µ0 i can fault or diverge.

Proof. By rule induction on the definition of ,→. In each case, we assume the lhs (CC)
faults and show that rhs (DD) either faults or diverges, by an analysis using the biprogram
semantics (Figs. 4 and 5).
    In reasoning about transitions that do not manipulate the environment we omit µ, µ0 .
                               ϕ        ϕ
Also, we omit ϕ from 7−→ and Z=⇒.
    The base cases are the weaving axioms.
case (A|A) ,→ bAc
    By semantics there are two ways (A|A) can fault:
       h(A|A), σ|σ 0 i Z=⇒ by transition bSplitLX, where hA, σi 7−→ .
       h(A|A), σ|σ 0 i Z=⇒ h(skip|A), σ|σ 0 i Z=⇒ by bSplitL and then bSplitRX, where
       hA, σ 0 i 7−→ .
    In either case we have hbAc, σ|σ 0 i Z=⇒ by bSyncX.
case (C; D | C 0 ; D0 ) ,→ (C|C 0 ); (D|D0 )
   There are four ways (C; D | C 0 ; D0 ) can fault:
    1. h(C; D | C 0 ; D0 ), σ|σ 0 i Z=⇒∗ h(C0 ; D | C 0 ; D0 ), τ |σ 0 i Z=⇒ for some C0 , τ such that
       hC0 , τ i 7−→ (by some number of instances of bSplitL and then bSplitLX).
    2. h(C; D | C 0 ; D0 ), σ|σ 0 i Z=⇒∗ h(D | C 0 ; D0 ), υ|σ 0 i Z=⇒∗ h(D0 | C 0 ; D0 ), τ |σ 0 i Z=⇒ where
       hD0 , τ i 7−→ (for some D0 , υ, τ , and again by bSplitL and bSplitLX).
    3. h(C; D | C 0 ; D0 ), σ|σ 0 i Z=⇒∗ h(D | C 0 ; D0 ), υ|σ 0 i Z=⇒∗ h(skip | C 0 ; D0 ), τ |σ 0 i Z=⇒∗ h(skip |
       C00 ; D0 ), τ |τ 0 i Z=⇒ where hC00 , τ 0 i 7−→ (by bSplitL, bSplitR, and bSplitRX).
    4. h(C; D | C 0 ; D0 ), σ|σ 0 i Z=⇒∗ h(D | C 0 ; D0 ), υ|σ 0 i Z=⇒∗ h(skip | C 0 ; D0 ), τ |σ 0 i Z=⇒∗ h(skip |
       D0 ), τ |υ 0 i Z=⇒∗ h(skip | D00 ), τ |τ 0 i Z=⇒ where hD00 , τ 0 i 7−→
    For each case we show that the woven biprogram (C|C 0 ); (D|D0 ) faults or diverges.
    1. h(C|C 0 ); (D|D0 ), σ|σ 0 i Z=⇒∗ h(C0 |C 0 ); (D|D0 ), τ |σ 0 i Z=⇒ by bSplitL and bSplitLX,
       because hC0 , τ i 7−→
    2. We have h(C|C 0 ); (D|D0 ), σ|σ 0 iZ=⇒∗ h(skip|C 0 ); (D|D0 ), υ|σ 0 i. From this point, C 0 could
       fault, or diverge, in which case (C|C 0 ); (D|D0 ) faults, or diverges, and we are done.
       Otherwise, execution can continue as h(skip|C 0 ); (D|D0 ), υ|σ 0 i Z=⇒∗ h(D|D0 ), υ|υ 0 i Z=⇒∗
       h(D0 |D0 ), τ |υ 0 i Z=⇒ because hD0 , τ i 7−→ .
    3. h(C|C 0 ); (D|D0 ), σ|σ 0 iZ=⇒∗ h(skip|C 0 ); (D|D0 ), υ|σ 0 iZ=⇒∗ h(skip|C00 ); (D|D0 ), υ|τ 0 i Z=⇒
    4. h(C|C 0 ); (D|D0 ), σ|σ 0 iZ=⇒∗ h(skip|C 0 ); (D|D0 ), υ|σ 0 iZ=⇒∗ h(D|D0 ), υ|υ 0 iZ=⇒∗ h(skip|D0 ), τ |υ 0 iZ=⇒∗
       h(skip|D00 ), τ |τ 0 i Z=⇒


10
     The specifications are irrelevant; all that matters is that the interpretation is unary.
XX:38   Relational logic with framing and hypotheses (Technical Report)


        case (if E then C else D | if E 0 then C 0 else D0 ) ,→ if E|E 0 then (C|C 0 ) else (D|D0 )
           If σ(E) 6= σ 0 (E 0 ) then hif E|E 0 then (C|C 0 ) else (D|D0 ), σ|σ 0 i Z=⇒ by bIfX and we are
           done. Otherwise, σ(E) = σ 0 (E 0 ), and we consider the four ways that the lhs can fault.
           1. h(if E then C else D | if E 0 then C 0 else D0 ), σ|σ 0 i Z=⇒ h(C | if E 0 then C 0 else D0 ), σ|σ 0 iZ=⇒∗
               h(C0 | if E 0 then C 0 else D0 ), τ |σ 0 i Z=⇒ by bSplitL and then bSplitLX, where
               σ(E) = true.
               Then for the rhs we have hif E|E 0 then (C|C 0 ) else (D|D0 ), σ|σ 0 i Z=⇒ h(C|C 0 ), σ|σ 0 iZ=⇒∗
               h(C0 |C 0 ), τ |σ 0 i Z=⇒
           2. h(if E then C else D | if E 0 then C 0 else D0 ), σ|σ 0 i Z=⇒ h(C | if E 0 then C 0 else D0 ), σ|σ 0 iZ=⇒∗
               h(skip | if E 0 then C 0 else D0 ), τ |σ 0 i Z=⇒ h(skip | C 0 ), τ |σ 0 i Z=⇒∗ h(skip | C00 ), τ |τ 0 i Z=⇒
               where σ(E) = true = σ 0 (E 0 ).
               Then for the rhs we have hif E|E 0 then (C|C 0 ) else (D|D0 ), σ|σ 0 i Z=⇒ h(C|C 0 ), σ|σ 0 iZ=⇒∗
               h(skip|C 0 ), τ |σ 0 i Z=⇒∗ h(skip|C00 ), τ |τ 0 i Z=⇒
           The other two cases are symmetric.
        case (let m = B in C | let m = B 0 in C 0 ) ,→ let m = (B|B 0 ) in (C|C 0 )
           Similar to the preceding cases, using that transitions taken on one side are not affected
           by the presence or absence of a binding for m on the other side.
        case (while E do C | while E 0 do C 0 ) ,→ while E|E 0 • P|P 0 do (C|C 0 )
           There are two ways the lhs can fault.
           1. h(while E do C | while E 0 do C 0 ), σ|σ 0 iZ=⇒∗ h(C; while E do C | while E 0 do C 0 ), υ|σ 0 iZ=⇒∗
               h(C0 ; while E do C | while E 0 do C 0 ), τ |σ 0 i Z=⇒ where υ is the state after the nth
               completed iteration on the left, and hC0 , τ i 7−→ .
           2. h(while E do C | while E 0 do C 0 ), σ|σ 0 i Z=⇒∗ h(skip | while E 0 do C 0 ), τ |σ 0 i Z=⇒∗ h(skip |
               C 0 ; while E 0 do C 0 ), τ |υ 0 i Z=⇒∗ h(skip | C00 ; while E 0 do C 0 ), τ |τ 0 i Z=⇒ where υ 0 is the
               state after the kth completed iteration on the right, and hC00 , τ 0 i 7−→ .
                         (−−−−              −−−−*
           Note that (C|C 0 ) is C and (C|C 0 ) is C 0 . Consider a trace from hwhile E|E 0 • P|P 0 do (C|C 0 ), σ|σ 0 i.
           If it faults due to rWhX we are done. Otherwise it can be segmented into the iterates,
           each of which begins with a step by rWhL, rWhR, or rWhTT, and accordingly executes
           (C|skip), (skip|C 0 ), or (C|C 0 ). These can be put in correspondence with some or all the
           iterates of (while E do C | while E 0 do C 0 ) so that the same states are reached.
           Whereas the lhs never executes C 0 unless and until C terminates (and does not fault),
           the rhs may do some iterations of C 0 before all iterations of C have been done. Hence, if
           some iteration of C 0 diverges, then the rhs diverges and we are done. In the absence of
           divergence, the rhs eventually reaches either the nth iteration on the left (case 1 above)
           or the kth iteration on the right (case 2 above). From that point, either steps by bSplitL
           lead to a point where we get a fault by bSplitLX (hC0 , τ i 7−→ ) or steps by bSplitR
           lead to a point where we get a fault by bSplitRX (hC00 , τ 0 i 7−→ ).

           Having dispensed with the base cases, we turn to the inductive cases which each have as
        premise that BB ,→ CC. The inductive hypothesis: for any σ, σ 0 , µ, µ0 , if hBB, σ|σ 0 , µ|µ0 i
        can fault then hCC, σ|σ 0 , µ|µ0 i can fault or diverge.
        case BB; DD ,→ CC; DD
           There are two ways the lhs can fault.
           1. BB; DD faults from σ, σ 0 because BB does.
              Then by induction hypothesis, CC (and hence CC; DD) diverges or faults.
           2. hBB; DD, σ|σ 0 i Z=⇒∗ hDD, υ|υ 0 i Z=⇒∗ hDD0 , τ |τ 0 i Z=⇒ , with hBB, σ|σ 0 i Z=⇒∗
              hbskipc, υ|υ 0 i.
A. Banerjee, D. A. Naumann, and M. Nikouei                                                                 XX:39


      Then by Lem. 7, hCC, σ|σ 0 i either faults or diverges (and then we are done) or it
       terminates in υ, υ 0 . In the latter case we have hCC; DD, σ|σ 0 i Z=⇒∗ hDD, υ|υ 0 i Z=⇒∗
       hDD0 , τ |τ 0 i Z=⇒ .
case DD; BB ,→ DD; CC
   If lhs faults in DD then so does rhs. Otherwise both lhs and rhs reach the same
   intermediate states upon termination of DD, from which BB faults. So by induction
   hypothesis, CC faults from those states.
case if E|E 0 then BB else DD ,→ if E|E 0 then CC else DD
   If σ(E) 6= σ 0 (E) then lhs and rhs both fault immediately.
   If σ(E) = f alse = σ 0 (E) then both sides take one step to the same configuration
   hDD, σ|σ 0 i so fault on lhs implies fault on rhs.
   If σ(E) = true = σ 0 (E) then fault on the lhs looks like hif E|E 0 then BB else DD, σ|σ 0 i Z=⇒
   hBB, σ|σ 0 i Z=⇒∗ so for the rhs it suffices to apply the induction hypothesis.
case if E|E 0 then DD else BB ,→ if E|E 0 then DD else CC
   Symmetric to the preceding case.
case let m = (B|B 0 ) in BB ,→ let m = (B|B 0 ) in CC
   A faulting trace for lhs has the form hlet m=(B|B 0 ) in BB, σ|σ 0 , µ|µ0 i Z=⇒ hBB, σ|σ 0 , µ̇|µ̇0 iZ=⇒∗
   hBB0 , τ |τ 0 , µ̇|µ̇0 i Z=⇒ where µ̇ is [µ+m: B] and µ̇0 is [µ0 +m: B 0 ]. By the induction
   hypothesis (which is stated for all environments), we get a fault or divergence for the rhs.
case while E|E 0 • P|P 0 do BB ,→ while E|E 0 • P|P 0 do CC
   A faulting trace T of while E|E 0 • P|P 0 do BB from σ, σ 0 can be segmented into n
                                                 (−                   −*
   completed iterates (each executing BB, (BB|skip), or (skip|BB)), followed by a partial
   iterate that faults.
   Claim: a trace of while E|E 0 • P|P 0 do CC from σ, σ 0 begins with k ≤ n completed
   iterates, ending in the same states as the corresponding iteration in T , and executing
    (−                  −*
   (CC|skip), (skip|CC), or CC, according to whether the corresponding iteration in T is left,
   right, or both. These k completed iterates are possibly followed by fault or divergence.
   Proof of claim: by induction the iterates in T . For the induction step, having the same
   states implies the rhs takes either a left-, right-, or both-iteration just as the lhs did
   (because the weaving did not change the alignment guards). If it is a one-sided iteration,
   by Lemma 6 the rhs is executing the same command, hence it faults. If it is a both-sided
   iteration, i.e., a terminated execution of BB, then Lemma 7 tells us that CC either faults,
   diverges, or terminates in the same states. The claim is proved.
                                                                                     (−
   Returning to the partial iterate of BB that faults, if it is one-sided, say BB, then by
                              (− (−
   Lemma 6 we have CC ≡ BB and hence rhs faults. If it is a both-sided iteration (i.e.,
   beginning with bWhTT), the induction hypothesis applies, to yield a fault or divergence
   of CC.
                                                                                                       J

   There is an obvious rule like rWeave but using the transitive closure ,→∗ . This is
admissible: any proof using that rule can be transformed to one making repeated use of
rWeave. Indeed, it is sound: soundness can be proved for ,→n , by induction on n, by using
the above argument for each ,→ in sequence.

Framed reads and rules rSeq and rWh
One complication in the rules for sequence and loops (rSeq and rWh) is already present in
the unary rules for sequence and loops. The issue is that, because frame conditions can be
XX:40   CONTENTS


        expressed in terms of mutable locations (often ghost variables and fields), sound sequencing
        of judgments must avoid interference with those locations—so that the interpretation of an
        effect can be preserved over a command. Soundness is achieved by the immunity conditions.
        These are already present in the unary logic [10], but use of immunity is more delicate with
        the addition of read effects in [7]. A key restriction is that specifications have framed reads
        (see Sec. A). This ensures that read effects are preserved under suitable immunity conditions.
            To state the key lemma, first we define the image of refperm π on arbitrary location set W .
        This is written π(W ) and defined for variables by x ∈ π(W ) iff x ∈ W and for heap locations
        by o.f ∈ π(W ) iff (π −1 (o)).f ∈ W . Second, we note a basic lemma: Suppose ε has framed
        reads. If Agree(σ, σ 0 , ε, π) then rlocs(σ 0 , ε) = π(rlocs(σ, ε)) and hence Agree(σ 0 , σ, ε, π −1 ).
            The key lemma is a bit technical. Keep in mind that the read effect part of a correctness
        judgment, and also the read effect condition for context interpretations, quantifies over all
        pairs of runs. In particular, for any two initial states σ, σ 0 , the conditions will be instantiated
        both with σ on the left and with σ on the right.

        I Lemma 9 (preservation of agreement). Suppose ε has framed reads. Suppose σ, σ 0 ⇒τ, τ 0 |= ε
        and σ 0 , σ⇒τ 0 , τ |= ε. Suppose Agree(σ, σ 0 , ε, π) and Agree(σ 0 , σ, ε, π −1 ). Let ρ be any refperm
        ρ ⊇ π for which Lagree(τ, τ 0 , ρ, freshLocs(σ, τ ) ∪ written(σ, τ )). Then for any set of locations
        W in σ, if Lagree(σ, σ 0 , π, W ) then Lagree(τ, τ 0 , ρ, W ).

        Existence of ρ for Lagree(τ, τ 0 , ρ, freshLocs(σ, τ )∪written(σ, τ )) is a consequence of σ, σ 0 ⇒τ, τ 0 |= ε.
        The result says that agreement on an arbitrary set W is preserved. For a proof, see [7].


        Contents
        1 Introduction                                                                                          1

        2 Background: synopsis of region logic                                                                 3

        3 Overview of the relational logic                                                                     5

        4 Relational formulas                                                                                  8

        5 Biprograms                                                                                           9

        6 Relational region logic                                                                             11

        7 Related work                                                                                        12

        8 Conclusion                                                                                          14

            References                                                                                        15

        A Semantics of unary programs and their correctness judgments                                         18

        B Relation formulas                                                                                   21

        C Biprograms                                                                                          22

        D Relational proof rules                                                                              25

        E Proof for example of “dissonant” loop                                                               27
CONTENTS                              XX:41


F Loop tiling example            29

G Proof for Stack example        30

H Semantic consistency theorem   33

I   Soundness theorem            36
