                                                                          Programming with Permissions in Mezzo

                                                                             François Pottier                                                              Jonathan Protzenko
                                                                                  INRIA                                                                           INRIA
                                                                         francois.pottier@inria.fr                                                   jonathan.protzenko@ens-lyon.org
arXiv:1311.7242v1 [cs.PL] 28 Nov 2013




                                        Abstract                                                                                        its current state. An example is a socket that moves from state
                                        We present Mezzo, a typed programming language of ML lineage.                                   “ready”, to “connected”, then to “closed”. The “close” function,
                                        Mezzo is equipped with a novel static discipline of duplicable and                              for instance, should be invoked only if the socket is currently in
                                        affine permissions, which controls aliasing and ownership. This                                 the state “connected”, and changes its state to “closed”. Another
                                        rules out certain mistakes, including representation exposure and                               example is a collection, which must not be accessed while an
                                        data races, and enables new idioms, such as gradual initialization,                             iterator exists, but can be used again once iteration is over.
                                        memory re-use, and (type)state changes. Although the core static                                    Although state and state change play an important role in many
                                        discipline disallows sharing a mutable data structure, Mezzo offers                             programs, no mainstream programming language builds these no-
                                        several ways of working around this restriction, including a novel                              tions into its static discipline. External tools must be used, such as
                                        dynamic ownership control mechanism which we dub “adoption                                      typestate checking tools [13, 5, 6] or tools for constructing proofs
                                        and abandon”.                                                                                   of programs, based for instance on separation logic [4, 20] or on
                                                                                                                                        the Spec# methodology [3]. Instead, we explore the possibility of
                                        Categories and Subject Descriptors D.3.2 [Programming Lan-                                      reasoning about state within the type system. This has well-known
                                        guages]: Language Classifications—Multiparadigm languages                                       potential benefits. A property that is expressed as a type is checked
                                                                                                                                        early, often, and at little cost. Furthermore, we believe that, in the
                                        Keywords         static type systems; side effects; aliasing; ownership                         future, such a type system can serve as a strong foundation for per-
                                                                                                                                        forming proofs of programs.
                                        1. Introduction                                                                                     Obviously, if two “principals” separately think that “the socket s
                                                                                                                                        is currently connected”, and if one of them decides to close this
                                        Programming with mutable, heap-allocated data structures is hard.
                                                                                                                                        socket, then the other will be left with an incorrect belief about s.
                                        In many typed imperative programming languages, including Java,
                                                                                                                                        Thus, precise reasoning about state and state changes requires that
                                        C#, and ML, the type system keeps track of the structure of objects,
                                                                                                                                        information about a mutable object (or data structure) be recorded
                                        but not of how they are aliased. As a result, a programming mistake
                                                                                                                                        in at most “one place” in the type system. In Mezzo, this place
                                        can cause undesired sharing, which in turn leads to breaches of ab-
                                                                                                                                        is a permission. Permissions keep track not only of the structure
                                        straction, invariant violations, race conditions, and so on. Further-
                                                                                                                                        of data, as does a traditional type system, but also of must-alias
                                        more, the fact that sharing is uncontrolled implies that the type of
                                                                                                                                        and must-not-alias (i.e. equality and disjointness) information. Like
                                        an object must never change. This forbids certain idioms, such as
                                                                                                                                        a separation logic assertion [29], a permission has an ownership
                                        delayed initialization, and prevents the type system from keeping
                                                                                                                                        reading: to have access to a description of a part of the heap is to
                                        track of the manner in which objects change state through method
                                                                                                                                        own this part of the heap. Because “to describe is to own”, we need
                                        calls. In order to work around this limitation, programmers typi-
                                                                                                                                        not explicitly annotate types with owners, as done in Ownership
                                        cally use C# and Java’s null pointer, or ML’s option type. This im-
                                                                                                                                        Types [10] or Universe Types [14].
                                        plies that a failure to follow an intended protocol is not detected
                                                                                                                                            We do not think of the “type” of an object and of its “state” as
                                        at compile time, but leads to a runtime error. In short, there is a
                                                                                                                                        two distinct notions: a permission describes both at once. Whereas
                                        price to pay for the simplicity of traditional type systems: the bugs
                                                                                                                                        previous work on permissions [5] distinguishes between a fixed
                                        caused by undesired sharing, or by the failure to follow an object
                                                                                                                                        type structure and “permissions” that evolve with time, in Mezzo,
                                        protocol, are not statically detected.
                                                                                                                                        both “type” and “state” can change over time. This yields greater
                                            This paper presents the design of a new programming language,
                                                                                                                                        expressiveness: for instance, gradual initialization and memory re-
                                        Mezzo, which attempts to address these issues. One motivating
                                                                                                                                        use become possible. This also yields greater simplicity and con-
                                        principle behind the design of Mezzo is that one should be able
                                                                                                                                        ciseness: for instance, when we write polymorphic code that ma-
                                        to express precise assertions about the current state of an object or
                                                                                                                                        nipulates a list, a single type variable a denotes not only “what” the
                                        data structure. The type system should keep track of state changes
                                                                                                                                        list elements are (e.g., sockets) but also in what “state” they are and
                                        and forbid using an object in a manner that is inconsistent with
                                                                                                                                        to what extent we “own” them.
                                                                                                                                            The choices described above form our basic design premises.
                                        Permission to make digital or hard copies of all or part of this work for personal or           Mezzo can be viewed as an experiment, whose aim is to determine
                                        classroom use is granted without fee provided that copies are not made or distributed           to what extent these choices are viable. Beyond these decisions,
                                        for profit or commercial advantage and that copies bear this notice and the full citation
                                        on the first page. Copyrights for components of this work owned by others than the
                                                                                                                                        we strive to make the language as simple as possible. Mezzo is
                                        author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or          a high-level programming language: we equip it with first-class
                                        republish, to post on servers or to redistribute to lists, requires prior specific permission   functions, algebraic data types, and require a garbage collector. We
                                        and/or a fee. Request permissions from permissions@acm.org.                                     could have chosen classes and objects instead of (or in addition
                                        ICFP ’13, September 25–27, 2013, Boston, MA, USA.                                               to) algebraic data types; this could be a topic for future research.
                                        Copyright is held by the owner/author(s). Publication rights licensed to ACM.
                                        ACM 978-1-4503-2326-0/13/09. . . $15.00.
                                                                                                                                        We equip Mezzo with a simple distinction between duplicable
                                        http://dx.doi.org/10.1145/2500365.2500598                                                       permissions (for immutable data) and exclusive permissions (for
mutable data). Although more advanced varieties of permissions                1   data list a =
exist in the literature, including read-only views of mutable data            2      Nil | Cons { head : a ; tail : list a }
and fractional permissions [7], we wish to evaluate how far one               3
can go without these advanced notions; if desired, they could in              4   data mutable mlist a =
principle be added to Mezzo.                                                  5     MNil | MCons { head : a ; tail : list a }
    By default, Mezzo’s permission discipline imposes a restrictive           6

aliasing regime: the mutable part of the heap must form a forest.             7 val rec appendAux [ a ] (
Mezzo offers several mechanisms for evading this restriction. One,            8     consumes dst : MCons { head : a ; tail : () } ,
adoption and abandon, is new. It allows arbitrary aliasing patterns           9     consumes xs : list a ,
                                                                             10     consumes ys : list a ) : (| dst @ list a ) =
within a region of the heap and achieves soundness via dynamic               11   match xs with
checks. We describe it in detail in §7. The second mechanism is              12   | Nil ->
Boyland’s nesting [7]. It can be viewed as a form of adoption                13       dst . tail <- ys ;
and abandon that requires no runtime checks but is (for many                 14       tag of dst <- Cons
purposes) less powerful. The last mechanism is locks in the style            15   | Cons ->
of concurrent separation logic [25, 18, 19, 8].                              16       let dst ’ = MCons { head = xs . head ;
    Mezzo’s static discipline has been formally defined and me-              17                              tail = () } in
chanically proved sound1 . The formalization, which is available on-         18       dst . tail <- dst ’;
                                                                             19       tag of dst <- Cons ;
line [26], includes adoption and abandon, but does not (at present)
                                                                             20       appendAux ( dst ’ , xs . tail , ys )
cover nesting, locks, or concurrency. The statement of soundness             21   end
guarantees that “well-typed programs do not go wrong”, except                22
possibly when the dynamic check performed at “abandon” fails.                23 val append [ a ] (
In a concurrent extension of Mezzo, it would in addition guarantee           24     consumes xs : list a ,
that “well-typed programs are data-race-free”. The proof is syntac-          25     consumes ys : list a ) : list a =
tic. We extend the typing judgement to a pair of a program under             26   match xs with
execution and its heap, and establish the standard subject reduction         27   | Nil ->
and progress lemmas.                                                         28       ys
                                                                             29   | Cons ->
    A prototype type-checker has been implemented and is publicly
                                                                             30       let dst = MCons { head = xs . head ;
available [27]. Several small libraries, totaling a few thousand lines       31                            tail = () } in
of code, have been written, and are also available online [27]. They         32       appendAux ( dst , xs . tail , ys );
include immutable data structures (lists), mutable data structures           33       dst
(lists, doubly-linked lists, binary search trees, hash tables, resizable     34   end
arrays, and FIFO queues, see §7), persistent data structures imple-
mented via imperative means (suspensions, persistent arrays), and                     Figure 1. Tail-recursive concatenation of immutable lists
a few algorithms (memoization; graph search). At the time of this
writing, an interpreter is available, and a simple compiler (which
translates Mezzo down to untyped OCaml) is being developed.                       copy of xs. Our implementation, on the other hand, is written
    The paper begins with a motivating example (§2), which cannot                 in destination-passing style, and has constant space overhead.
be type-checked in ML, and which serves to informally illustrate                  Roughly speaking, the list xs is traversed and copied on the fly.
Mezzo’s permission discipline. Then, we define the syntax of types,               When the end of xs is reached, the last cell of the copy is made to
permissions, and expressions (§3) and informally explain the own-                 point to ys.
ership reading of permissions for immutable and mutable data (§4).                    The append function (Figure 1, line 23) is where concatenation
We present the typing rules (§5) and introduce a few syntactic con-               begins. If xs is empty, then the concatenation of xs and ys is
ventions that make the surface language more palatable (§6). We                   ys (line 27). Otherwise (line 29), append allocates an unfinished,
explain adoption and abandon, illustrate them with a second exam-                 mutable cell dst (line 30). This cell contains the first element of the
ple (§7), and discuss nesting and locks more briefly (§8). Finally,               final list, namely xs.head. It is in an intermediate state: it cannot be
we explain where Mezzo lies in the design space and compare it                    considered a valid list, since its tail field contains the unit value ().
with some of the previous approaches found in the literature (§9).                It is now up to appendAux to finish the work by constructing the
                                                                                  concatenation of xs.tail and ys and writing the address of that list
2. Mezzo by example                                                               into dst.tail. Once appendAux returns, dst has become a well-
                                                                                  formed list (this is indicated by the postcondition “dst @ list a”
Figure 1 presents code for the concatenation of two immutable lists.              on line 10) and is returned by append.
This example showcases several of Mezzo’s features, and allows us                     The function appendAux expects an unfinished, mutable cell dst
to explain the use of permissions. We review the code first (§2.1),               and two lists xs and ys. Its purpose is to write the concatenation of
then briefly explain how it is type-checked (§2.2 and §2.3).                      xs and ys into dst.tail, at which point dst can be considered a
                                                                                  well-formed list. If xs is Nil (line 12), the tail field of dst is made
2.1 Code                                                                          to point to ys. Then, dst, a mutable MCons cell, is “frozen” by a
Our purpose is to write code that concatenates two immutable                      tag update instruction and becomes an immutable Cons cell. (This
lists xs and ys to produce a new immutable list. The traditional,                 instruction compiles to a no-op.) If xs is a Cons cell (line 15), we
purely functional implementations of concatenation have linear                    allocate a new destination cell dst’, let dst.tail point to it, freeze
space overhead, as they implicitly or explicitly allocate a reversed              dst, and repeat the process via a tail-recursive call.
                                                                                      This example illustrates several important aspects of Mezzo.
1 The formalization concerns a slightly lower-level language, Core Mezzo.
In Core Mezzo, fields are numbered, whereas in Mezzo they are named and           Expressiveness In a traditional typed programming language,
field names can be overloaded. At present, Core Mezzo is missing some             such as Java or OCaml, list concatenation in destination-passing
of the features of Mezzo, including parameterized algebraic data types and        style is possible, but its result must be a mutable list, because an
mode constraints. We hope to add them in the future.                              immutable list cell cannot be gradually initialized.
State change The call appendAux(dst, xs, ys) changes the                          At this stage, the type-checker performs an implicit operation. It
“type” of dst from “unfinished, mutable list cell” to “well-formed,            applies the permission subsumption rule D ECOMPOSE B LOCK. This
immutable list”. This type-changing update is sound because one                causes fresh names hd and tl to be introduced for the head and
must be the “unique owner” of the mutable cell dst for this call to            tail fields of this structural permission. This yields the following
be permitted.                                                                  conjunction:
Ownership transfer In fact, the call appendAux(dst, xs, ys)                                xs @ Cons {head : (=hd); tail : (=tl)} ∗
also changes the “type” of xs and ys from “immutable list” to “un-                         hd @ a ∗ tl @ list a ∗
known”. Indeed, the postcondition of appendAux guarantees noth-                            ys @ list a
ing about xs and ys. In other words, the caller gives up the permis-           This is our first encounter of a singleton type, which we write =hd.
sion to use xs and ys as lists, and in return gains the permission to          A permission of the form x @ =y asserts that the variables x
use dst as a list. In other words, the ownership of the list elements          and y denote the same value. In particular, if they denote memory
is transferred from xs and ys to dst. This is required for sound-              locations, this means that x and y point to the same object: this is
ness. We do not know what the list elements are (they have abstract            a must-alias constraint. We write x = y for x @ =y. Similarly, in
type a). They could be mutable objects, whose “unique ownership”               the structural permission above, the fact that the head field has type
property must not be violated2 .                                               =hd means that the value of this field is hd. We write head = hd
                                                                               for head : (=hd).
2.2 Permissions
                                                                                   By the typing rules N EW and L ET, when the cell dst is allocated
Permissions do not exist at runtime: they are purely an artefact               (line 30), a permission for dst appears, namely:
of the type system. An atomic permission x @ t represents the
right to use the program variable x at type t. Two permissions P1                             dst @ MCons {head = hd; tail : ()}
and P2 can be combined to form a composite permission P1 ∗ P2 .                We now see how singleton types help reason about sharing. At this
The conjunction ∗ is separating [29] at mutable memory locations               point, we have three permissions that mention hd. We know that
and requires agreement at immutable locations (§4.1). The empty                hd is stored in the head field of xs; we know that hd is stored in
permission, a unit for conjunction, is written empty.                          the head field of dst; and we have a permission to use hd at type a.
    When execution begins, a program conceptually possesses an                 We do not need a borrowing convention [24] in order to fix which
empty permission. As execution progresses through the code, per-               of xs or dst owns hd. Instead, the system knows that the object
missions come and go. At any program point, there is a certain                 hd is accessible via two paths, namely xs.head and dst.head, and
current permission. Most of the time, the manner in which permis-              can be used under either name. This use of singleton types is taken
sions evolve and flow is implicit. It must be made explicit in a few           from Alias Types [30].
places: in particular, every function type must include explicit pre-              By the typing rules R EAD and A PPLICATION, in order to call
and postconditions.                                                            appendAux(dst, xs.tail, ys) (line 32), we need the following
    Let us continue our discussion of the concatenation example                conjunction of permissions. It is the precondition of appendAux ,
(Figure 1). We explain in an informal manner how the function                  suitably instantiated:
append is type-checked. This allows us to illustrate how permis-
sions are used and how they evolve.                                               dst @ MCons {head : a; tail : ()} ∗ tl @ list a ∗ ys @ list a
    The typing rules appear in Figure 4; a subset of the permission            Are we able to satisfy this requirement? The answer is positive.
subsumption rules appear in Figure 6. In the following, we refer to            The subsumption rules E XISTS I NTRO and D ECOMPOSE B LOCK allow
some of these rules, but defer their detailed explanation to §5.               combining the permissions MCons {head = hd; tail : ()} and
    The append function is defined at line 23. At the beginning of             hd @ a (both of which are present) to obtain the first conjunct
the function’s body, by the typing rule F UNCTION, permissions for             above. The second and third conjuncts above are present already.
the formal arguments are available. Thus, the current permission is:               By A PPLICATION, the precondition of appendAux is consumed
                        xs @ list a ∗ ys @ list a                              (taken away from the caller). After the call, the postcondition of
                                                                               appendAux is added to the current permission, which is then:
This permission represents the right to use xs and ys as lists of
elements of type a.                                                                     xs @ Cons {head = hd; tail = tl} ∗ dst @ list a
   This permission soon evolves, thanks to the match construct,                The conjunct that concerns xs is of no use, and is in fact silently
which examines the tag carried by xs. By the typing rule M ATCH,               discarded when we reach the end of the Cons branch within append.
as we learn that xs is a Nil cell, we replace our permission about             The conjunct that concerns dst is used to check that this branch
xs with a more precise one, which incorporates the knowledge that
                                                                               satisfies append’s advertised return type, namely list a. Similarly,
the tag of xs is Nil. At line 27, the current permission becomes:              in the Nil branch, the permission ys @ list a shows that a value of
                         xs @ Nil ∗ ys @ list a                                appropriate type is returned. In conclusion, append is well-typed.
xs @ Nil is a structural permission: it asserts that xs points to              2.3 To loop or to tail call?
a memory block whose tag is Nil (and which has zero fields).
Similarly, at line 29, the current permission becomes:                         In-place concatenation (that is, melding) of mutable lists can also
                                                                               be implemented by a tail-recursive function. The pattern is analo-
          xs @ Cons {head : a; tail : list a} ∗ ys @ list a                    gous to that of Figure 1, but the code is simpler, because the first
The structural permission for xs asserts that xs points to a memory            list is not copied, and “freezing” is not required.
block that carries the tag Cons and has a head field of type a and a               These algorithms are traditionally viewed as iterative and im-
tail field of type list a.                                                     plemented using a while loop. Berdine et al.’s iterative formula-
                                                                               tion of mutable list melding [4], which is proved correct in sepa-
2 We later note (§4.1) that if at a call site the variable a is instantiated   ration logic, has a complex loop invariant, involving two “list seg-
with a duplicable type, say int, then the permissions xs @ list int            ments”, and requires an inductive proof that the concatenation of
and ys @ list int are considered duplicable, so they can in fact be            two list segments is a list segment. In contrast, in the tail-recursive
duplicated prior to the call appendAux(dst, xs, ys), hence are not lost.       approach, the “loop invariant” is the type of the recursive function
(e.g., appendAux in Figure 1). This type is reasonably natural and                 κ ::=   type | term | perm | κ → κ                        kind
does not involve list segments.
    How do we get away without list segments and without induc-            T, t, P ::=                                     type or permission
tive reasoning? The trick is that, even though appendAux is tail-                          X                               variable (a, x, . . .)
recursive, which means that no code is executed after the call by                          t→t                                   function type
appendAux to itself, a reasoning step still takes place after the call.                    (~t )                                     tuple type
Immediately before the call, the current permission can be written                         A {f~ : ~t} adopts t                 structural type
as follows:                                                                                T T~                        n-ary type application
                xs @ Cons {head = hd; tail = tl} ∗                                         ∀(X : κ) T                 universal quantification
               dst @ Cons {head : a; tail = dst′ } ∗                                       ∃(X : κ) T                existential quantification
              dst′ @ MCons {head : a; tail : ()} ∗                                         =x                                   singleton type
                 tl @ list a ∗ ys @ list a                                                 (t | P )              type/permission conjunction
                                                                                           dynamic                                     (see §7)
The call “appendAux (dst’, xs.tail, ys)” consumes the last
                                                                                           x@ t                            atomic permission
three permissions and produces instead dst′ @ list a. The first two
                                                                                           empty                            empty permission
permissions are “framed out”, i.e., implicitly preserved. After the
                                                                                           P ∗P                       permission conjunction
call, we have:
                                                                                           x:t                     name introduction (see §6)
                xs @ Cons {head = hd; tail = tl} ∗                                         consumes T           consumes annotation (see §6)
               dst @ Cons {head : a; tail = dst′ } ∗
              dst′ @ list a                                                        d ::=                    algebraic data type definition
                                                                                                            ~ : ~κ) = ~b
                                                                                           mutable? data d (X
Dropping the first permission and combining the last two yields:
                                                                                            adopts t
                dst @ Cons {head : a; tail : list a}
which can be folded back to dst @ list a, so appendAux satisfies its               b ::=   A {f~ : ~t}               algebraic data type branch
postcondition. In short, the code is tail-recursive, but the manner in
which one reasons about it is recursive.                                               Figure 2. Syntax of types and permissions
    Minamide [22] proposes a notion of “data structure with a hole”,
or in other words, a segment, and applies it to the problem of con-
catenating immutable lists. Walker and Morrisett [35] offer a tail-
recursive version of mutable list concatenation in a low-level typed       e ::=                                                       expression
intermediate language, as opposed to a surface language. The man-                    x                                                     variable
ner in which they avoid reasoning about list segments is analogous                   let p = e in e                               local definition
to ours. There, because the code is formulated in continuation-                      fun [X ~ : ~κ] (x : t) : t = e        anonymous function
passing style, the reasoning step that takes place “after the recur-                 e [t : κ]                                 type instantiation
sive call” amounts to composing the current continuation with a                      ee                                    function application
coercion. Maeda et al. [21] study a slightly different approach, also                (~e )                                                    tuple
in the setting of a typed intermediate language, where separating                    A {f~ = ~e}                    data constructor application
implication offers a way of defining list segments. Our approach                     e.f                                              field access
could be adapted to an iterative setting by adopting a new proof rule                e.f ← e                                         field update
for while loops. This is noted independently by Charguéraud [9,                      match e with p    ~ → ~e                       case analysis
§3.3.2] and by Tuerk [34].                                                           tag of e ← A                                       tag update
                                                                                     give e to e                                          adoption
3. Syntax                                                                            take e from e                                        abandon
                                                                                     fail                                        dynamic failure
3.1 Types
We work with the “internal syntax” of types. The surface syntax            p ::=                                                         pattern
adds a few syntactic conventions, which we explain later on (§6).                    x                                                  variable
For the moment, the reader may ignore the two underlined con-                        (~
                                                                                      p)                                           tuple pattern
structs in Figure 2.                                                                 A {f~ = p
                                                                                             ~}                         data constructor pattern
    Types have kinds. The base kinds are type, term, and perm. The
standard types, such as function types, tuple types, etc. have kind                         Figure 3. Syntax of expressions
type. The types of kind term are program variables. If a variable x
is bound (by let, fun, or match) in the code, then x may appear
not only in the code, but also in a type: it is a type of kind term.
The types of kind perm are permissions. First-order arrow kinds           types ~t. An example, taken from §2, is MCons {head : a; tail : ()}.
are used to classify parameterized algebraic data types.                  The data constructor A must refer to a previously defined algebraic
    In Figure 2, we use the meta-variables T and X to stand for           data type, and the fields f~ must match the definition of A. The
types and variables of arbitrary kind; we use t and P to suggest          types ~t, however, need not match the types that appear in the
that a type has kind type and perm, respectively; we use a and x          definition of A. For instance, in the definition of MCons, the type of
to suggest that a variable has kind type and term, respectively.          the tail field is mlist a, not (). This implies that the above structural
We omit the definition of the kinding judgment; it appears in the         type cannot be folded to mlist a; the tail field must be updated
extended version of this paper [28].                                      first. A structural type may include a clause of the form adopts t,
    The structural type A {f~ : ~t} describes a block in the heap         whose meaning is explained later on (§7). If omitted, adopts ⊥ is
whose tag is currently A and whose fields f~ currently have the           the default.
    An example of a type application T T~ is list int. We sometimes        permission denotes shared, permanent knowledge. The permis-
refer to this as a nominal type, as opposed to a structural type.          sions that describe read-only, immutable data are duplicable: for
    The universal and existential types are in the style of System F .     instance, xs @ Cons {head = hd; tail = tl} and xs @ list int are
A (base) kind annotation is mandatory; if omitted, type is the             duplicable.
default. The bottom type ⊥ and the top type unknown can be                     A subset of the permissions are considered exclusive. An ex-
defined as ∀a.a and ∃a.a, respectively.                                    clusive permission for an object x represents the “unique owner-
    The conjunction of a type and a permission is written (t | P ).        ship” of x. In other words, such a permission grants read-write ac-
Because permissions do not exist at runtime, a value of this type          cess to the memory block at address x and guarantees that no-one
is represented at runtime as a value of type t. Such a conjunction         else has access to this block. The permissions that describe mutable
is typically used to express function pre- and postconditions. The         memory blocks are exclusive: for instance, xs @ MCons {head =
type (() | P ) is abbreviated as (| P ).                                   hd; tail = tl} is exclusive. An exclusive permission is analogous
    Algebraic data type definitions are prefixed with the keyword          to a “unique” permission in other systems [5] and to a separation
data. They are anologous to Haskell’s and OCaml’s. Each branch             logic assertion [29].
is explicitly named by a data constructor and carries a number of              By lack of space, we must unfortunately omit the definition of
named fields. If a definition begins with the keyword mutable, then        the predicates “t is duplicable” and “t is exclusive”, which are used
the tag and all fields are considered mutable, and can be modified         in the typing rules (Figure 4). They can be found in the extended
via tag update and field update instructions; otherwise, they are          version of this paper.
considered immutable. Examples appear at the top of Figure 1. Like             No permission is duplicable and exclusive. Some permissions
a structural type, an algebraic data type definition may include an        are neither duplicable nor exclusive. “xs @ list (ref int)”, which
adopts clause; if omitted, adopts ⊥ is the default.                        describes an immutable list of references to integers, illustrates this.
                                                                           It must not be duplicated: this would violate the “unique owner”
3.2 Expressions                                                            property of the list elements. It is not exclusive: the list cell at xs
Expressions (Figure 3) form a fairly standard λ-calculus with tu-          is an immutable object, and this permission does not guarantee
ples and algebraic data structures. A function definition must be          exclusive access to this cell. Another example is “x @ a”. Because
explicitly annotated with the function’s type parameters, argument         a is a type variable, one cannot assume that this permission is
type, and return type. One reason for this is that the argument and        duplicable (or exclusive)3 .
return type serve as pre- and postconditions and in general cannot             Every permission is affine. One can implicitly drop a permission
be inferred. Furthermore, we have System F -style polymorphism.            that one does not need.
Explicit type abstractions are built into function definitions. Type           The language is designed so that the type-checker (and the pro-
applications must in principle be explicit as well. The prototype          grammer!) can always tell what mode a permission P satisfies: du-
type-checker allows omitting them and performs a limited form of           plicable, exclusive, or neither (hence, affine). Modes form an upper
type inference, which is outside the scope of this paper.                  semi-lattice, whose top element is “affine”, and where “duplicable”
                                                                           and “exclusive” are incomparable. Because algebraic data types are
                                                                           recursively defined, their mode analysis requires a fixed point com-
4. Ownership, modes, and extent                                            putation, whose details we omit.
We wrote earlier (§1) that “to have a permission for x” can be                 If t and u are exclusive types, then the conjunction x @ t∗y @ u
understood informally as “to own x”. Roughly speaking, this is             implies that x and y are distinct addresses. In other words, conjunc-
true, but we must be more precise, for two reasons. First, we wish to      tion of exclusive permissions is separating. On the other hand, if t
distinguish between mutable data, on which we impose a “unique             and/or u are duplicable, x and y may be aliases. Conjunction is not
owner” policy, and immutable data, for which there is no such              in general separating. Conjunction of duplicable permissions re-
restriction. For this reason, types and permissions come in several        quires agreement between the two conjuncts. The reader is referred
flavors, which we refer to as modes (§4.1). Second, in a permission        to the draft paper that accompanies the type soundness proof [26]
of the form x @ t, the type t describes the extent to which we own x.      for a formal definition of the semantics of conjunction.
If xs is a list cell, do we own just this cell? the entire spine? the
spine and the elements? The answer is given by the type t. For             4.2 Extent
instance (§4.2), xs @ Cons {head = hd; tail = tl} represents the           Every type t has an ownership reading: that is, the permission x @ t
ownership of just the cell xs, because the singleton types =hd and         represents certain access rights about x. However, the extent of
=tl denote the ownership of an empty heap fragment. On the other           these rights (or, in separation logic terminology, their footprint)
hand, xs @ Cons {head : a; tail : list a} gives access to the entire       depends on the type t.
list spine. (Because list is an immutable algebraic data type, this            A singleton type =y, for instance, has empty extent. Indeed, the
is read-only, shared access.) It further gives access to all of the list   permission x @ =y, which we usually write x = y, asserts that x
elements, insofar as the type a allows this access. In this example,       and y are equal, but does not allow assuming that x is a pointer, let
a is a variable: one must wait until a is instantiated to determine        alone dereferencing it.
what the elements are and to what extent we own them.                          A structural type such as Cons {head = hd; tail = tl} has an
                                                                           extent of one memory block. The permission xs @ Cons {head =
4.1 Modes                                                                  hd; tail = tl} gives us (read-only, shared) access to the block at
A subset of the permissions are considered duplicable, which               address xs, and guarantees that its head and tail fields contain the
means that they can be implicitly copied (D UPLICATE, Figure 6).           values hd and tl, respectively, but (as per the semantics of singleton
Copying a permission for an object x means that x may be shared:           types) guarantees nothing about hd and tl.
it may be used via different pointers, or by different threads simul-          What is the extent of a “deep” composite type, such as the
taneously. Thus, a duplicable permission does not represent unique         structural type Cons {head : a; tail : list a} or the nominal type
ownership; instead, it denotes shared knowledge. Because the sys-          list a? What does it mean to own a list? In order to answer these
tem does not control with whom this knowledge is shared, this
knowledge must never be invalidated, lest some principals be left          3 Mezzo allows the programmer to explicitly assume that a type variable a
with an outdated version of the permission. Therefore, a duplicable        is duplicable, or exclusive. This mechanism is not treated in this paper.
questions, one must understand how a composite permission is                ership reading, a function type t1 → t2 describes not only the shape
decomposed into a conjunction of more elementary permissions.               of the function’s arguments and results, but also the side effects that
    A structural permission, such as xs @ Cons {head : a; tail :            the function may perform, as well as the transfers of ownership that
list a}, can be decomposed by introducing a fresh name for each of          occur from the caller to the callee and back.
the values stored in the fields. (See D ECOMPOSE B LOCK in Figure 6.)           N EW uses a structural type to describe the newly-allocated mem-
The result is a more verbose, but logically equivalent, permission:         ory block in an exact manner. T UPLE is analogous.
                                                                                R EAD requires a structural permission x @ A {F [f : t]}, which
∃hd, tl.(xs @ Cons {head = hd; tail = tl} ∗ hd @ a ∗ tl @ list a)           guarantees that x points to a memory block that contains a field
The meaning and extent of the original structural permission is now         named f , and allows us to dereference x.f 4 . R EAD concludes that
clearer: it grants access to the cell at xs and to the first list element   the field access expression x.f has type t, and that the structural
(to the extent dictated by the type a) and to the rest of the list.         permission x @ A {F [f : t]} is preserved. There is a catch: because
    The meaning of a nominal permission, such as xs @ list a,               the type t occurs twice in this postcondition, we must require t to
is just the disjunction of the meanings of its unfoldings, namely           be duplicable, or the rule would be unsound. Fortunately, this is not
xs @ Nil and xs @ Cons {head : a; tail : list a}.                           a problem: by using D ECOMPOSE B LOCK (Figure 6; also explained
    If a is (instantiated with) an exclusive type, then we find that        earlier, see §2.2 and §4.2), it is possible to arrange for t to be a
xs @ list a implies that the list elements are pairwise distinct, and       singleton type, which is duplicable.
grants read-only access to the list spine and exclusive access to the           Like R EAD, W RITE requires a structural permission, of the form
list elements.                                                              x1 @ A {F [f : t1 ]}. It checks that this permission is exclusive, i.e.,
                                                                            the data constructor A is associated with a mutable algebraic data
                                                                            type. This ensures that we have write access. In fact, since we have
5. Type assignment                                                          exclusive access to x1 , a strong (type-changing) update is sound.
5.1 The typing judgment                                                     The permission is changed to x1 @ A {F [f : t2 ]}, where t2 is the
The typing judgment takes the form K; P ⊢ e : t. It is induc-               type of x2 . Without loss of generality, one may let t2 be the sin-
tively defined in Figures 4 and 5. The kind environment K maps              gleton type =x2 . This allows the type-checker to record that x1 .f
variables to kinds. This judgment means that, by consuming the              and x2 are now aliases. If desired, the permissions x1 @ A {F [f =
permission P , the expression e produces a value of type t. It is           x2 ]} and x2 @ t2 can later be combined by D ECOMPOSE B LOCK to
analogous to a Hoare logic or separation logic triple, where P is           yield x1 @ A {F [f : t2 ]}. Because D ECOMPOSE B LOCK, read from
the precondition and t is the postcondition.                                right to left, involves a loss of information, it is typically applied
    The typing judgement relies on a well-kindedness judgement of           by the type-checker only “on demand”, i.e., to satisfy a function
the form K ⊢ t : κ. It ensures that types are well-kinded and that          postcondition or a type annotation.
                                                                                M ATCH is used to type-check a case analysis construct. Each
the syntactic facilities of the surface syntax (§6) are used properly.
For conciseness, in the typing rules, we omit all freshness and well-       branch is type-checked independently. We currently do not check
kindedness side conditions.                                                 that the case analysis is exhaustive, but plan to add this feature in
    The typing rules require many sub-expressions to be variables.          the future. The premise relies on a judgment of the form K; P ⊢
For instance, the rule R EAD cannot handle a field access expression        let p = x in e : t. This is not a new judgment; it is an ordinary
of the form e.f : instead, it requires x.f . This requirement is met by     typing judgement, but, for clarity, the typing rules that have a con-
first performing a monadic transformation, which introduces extra           clusion of this form are isolated in Figure 5. Although these rules
let constructs. Furthermore, the pattern matching rules (Figure 5)          may appear somewhat daunting, they are in fact quite straightfor-
cannot handle deep patterns: they require shallow patterns. Again,          ward. L ET T UPLE checks that x is a tuple, i.e., we have a permission
this requirement is met by introducing extra let constructs. We omit        of the form x @ (t1 , . . . , tn ). If that is the case, then matching x
the details of these transformations.                                       against the tuple pattern (x1 , . . . , xn ) is permitted, and gives rise
    VAR is the axiom rule. It is worth noting that, in conjunction with
                                                                            to a conjunction of permissions of the form xi @ ti . Because the
the subsumption rule E QUALITY R EFLEXIVE (Figure 6), it allows             permission for x is not lost, the types ti are duplicated, so they are
proving that x has type =x, even in the absence of any hypothesis           required to be duplicable. Again, this requirement causes no loss
about x.                                                                    of generality, since one can arrange to introduce singleton types
    L ET corresponds to the sequence rule of separation logic.
                                                                            ahead of time. L ET DATA M ATCH is analogous to L ET T UPLE, but con-
    F UNCTION states that a duplicable permission P that exists at the
                                                                            cerns a (mutable or immutable) memory block. L ET DATA M ISMATCH
function definition site is also available within the function body.        concerns the situation where the pattern, which mentions the data
Requiring P to be duplicable allows us to consider every function           constructor B, will clearly not match x, which is statically known
type duplicable. Thus, a function can be shared without restriction         to have the tag A. In that case, the branch is dead code, and is con-
and can be invoked as many times as desired, provided of course             sidered well-typed. L ET DATAU NFOLD refines a nominal permission,
that one is able to satisfy its precondition. If one wishes to write a      such as x @ list a, by replacing it with a structural one, such as
function that captures a non-duplicable permission P , and can be           x @ Cons {head : a; tail : list a}, obtained by unfolding the al-
invoked at most once, this is still possible. Indeed, a type t1 ⊸ t2        gebraic data type and specializing it with respect to the data con-
of “one-shot” functions can be defined as:                                  structor that appears in the pattern. We omit the exact definition of
                                                                            unfolding.
                 ∃(p : perm) (((t1 | p) → t2 ) | p)                             W RITE TAG type-checks a tag update instruction, which modifies
                                                                            the tag carried by a memory block. Like W RITE, it requires an
This is a conjunction of a function whose precondition is p and of          exclusive permission for this block. It further requires the new
one copy of p. Because p is abstract, it is considered affine. Hence,       tag B to carry the same number of fields as the previous tag A.
at most one call is possible, after which p is consumed and the
function becomes unusable.                                                  4 We write F [f  : t] for a sequence of field/type pairs in which the pair
    A PPLICATION corresponds to the rule for procedure calls in sep-        f : t occurs. The adopts clause, if present, is irrelevant. We overload field
aration logic. The caller gives up the permission x2 @ t2 , which           names: there could exist multiple data constructors with a field named f .
is consumed, and in return gains a permission for the result of the         There can be at most one permission of the form x @ A {F [f : t]}, though,
function call, at type t1 . In other words, because types have an own-      which allows disambiguation to take place.
                          L ET                                                             F UNCTION
VAR                       K; P ⊢ e1 : t1    K, x : term; x @ t1 ⊢ e2 : t2                     ~ : ~κ, x : term; P ∗ x @ t1 ⊢ e : t2
                                                                                           K, X                                         P is duplicable
K; x @ t ⊢ x : t
                                   K; P ⊢ let x = e1 in e2 : t2                                            ~                           ~
                                                                                            K; P ⊢ fun [X : ~κ] (x : t1 ) : t2 = e : ∀(X : ~κ) t1 → t2

I NSTANTIATION                                                                                                       N EW
K; P ⊢ e : ∀(X : κ) t1           A PPLICATION                                          T UPLE                                  A {f~} is defined
                                 K; x1 @ t2 → t1 ∗ x2 @ t2 ⊢ x1 x2 : t1                K; ~x @ ~t ⊢ (~x) : (~t )
K; P ⊢ e : [T2 /X]t1                                                                                                 K; ~x @ ~t ⊢ A {f~ = ~x} : A {f~ : ~t}

               R EAD
                       t is duplicable                               W RITE
               P is x @ A {F [f : t]} adopts u                                           A {. . .} is exclusive
                    K; P ⊢ x.f : (t | P )                             K; x1 @ A {F [f : t1 ]} adopts u ∗ x2 @ t2 ⊢ x1 .f ← x2 : (|
                                                                         x1 @ A {F [f : t2 ]} adopts u)

             M ATCH                                                           W RITE TAG
             for every i, K; P ⊢ let pi = x in ei : t                         A {. . .} is exclusive       B {f~′ } is defined #f~ = #f~′
                 K; P ⊢ match x with p ~ → ~e : t                                   K; x @ A {f~ : ~t} adopts u ⊢ tag of x ← B : (|
                                                                                         x @ B {f~′ : ~t} adopts u)

                                                                                                                                S UB
  G IVE                                        TAKE                                                                                K; P2 ⊢ e : t1
           t2 adopts t1                                       t2 adopts t1                               FAIL                   P1 ≤ P2     t1 ≤ t2
                                                                                                         K; P ⊢ fail : t
        K; x1 @ t1 ∗ x2 @ t2 ⊢                             K; x1 @ dynamic ∗ x2 @ t2 ⊢                                             K; P1 ⊢ e : t2
   give x1 to x2 : (| x2 @ t2 )                  take x1 from x2 : (| x1 @ t1 ∗ x2 @ t2 )

                                    F RAME                                                    E XISTS E LIM
                                             K; P1 ⊢ e : t                                     K, X : κ; P ⊢ e : t
                                        K; P1 ∗ P2 ⊢ e : (t | P2 )                            K; ∃(X : κ) P ⊢ e : t

                                                                Figure 4. Typing rules


            L ET T UPLE                                                  L ET D ATA M ATCH
                        (~t ) is duplicable                                                      (~t ) is duplicable
            K, ~x : term; P ∗ x @ (~t ) ∗ ~x @ ~t ⊢ e : t                  K, ~x : term; P ∗ x @ A {f~ : ~t} adopts u ∗ ~x @ ~t ⊢ e : t
             K; P ∗ x @ (~t ) ⊢ let (~x) = x in e : t                     K; P ∗ x @ A {f~ : ~t} adopts u ⊢ let A {f~ = ~x} = x in e : t

                                                                                    L ET D ATAU NFOLD
   L ET D ATA M ISMATCH                                                                    x @ A {f~ : ~t} adopts u is an unfolding of T T~
           A and B belong to a common algebraic data type                           K; P ∗ x @ A {f~ : ~t} adopts u ⊢ let A {f~ = ~x} = x in e : t
   K; P ∗ x @ A {f~ : ~t} adopts u ⊢ let B {f~′ = ~x} = x in e : t                        K; P ∗ x @ T T~ ⊢ let A {f~ = ~x} = x in e : t

                                                Figure 5. Auxiliary typing rules for pattern matching


                                                                                                  D UPLICATE
   E QUALITY R EFLEXIVE             E QUALS F OR E QUALS                                           P is duplicable          M IX S TAR
   empty ≤ (x = x)                  (y1 = y2 ) ∗ [y1 /x]P ≡ (y1 = y2 ) ∗ [y2 /x]P                                           x @ t ∗ P ≡ x @ (t | P )
                                                                                                    P ≤P ∗P

                                                         E XISTS ATOMIC                       D ECOMPOSE B LOCK
W EAKEN                E XISTS I NTRO                    x @ ∃(X : κ) t                                        y @ A {F [f : t]} adopts u
P1 ∗ P2 ≤ P2           [T /X]P ≤ ∃(X : κ) P
                                                        ≡ ∃(X : κ) (x @ t)                      ≡ ∃(x : term) (y @ A {F [f = x]} adopts u ∗ x @ t)

                                                            U NFOLD
   F OLD                                                    A {f~ : ~t} adopts u is an unfolding of T T~             DYNAMIC A PPEARS
   A {f~ : ~t} adopts u is an unfolding of T T~                       T T~ has only one branch                              t is exclusive
      x @ A {f~ : ~t} adopts u ≤ x @ T T~                      x @ T T~ ≤ x @ A {f~ : ~t} adopts u                   x @ t ≤ x @ t ∗ x @ dynamic

                                               Figure 6. Permission subsumption (not all rules shown)
(Thus, the block does not have to be enlarged or shrunk.) The                 6.1 The name introduction form
structural permission is updated in a straightforward way. The                The construct x : t allows introducing a name x for a component
types ~t of the fields do not change. The names of the fields change          of type t. This allows writing “dependent function types”, such
from f~ to f~′ , where the sequences of fields are ordered in the             as (x1 : t1 ) → (x2 : t2 ), where by convention x1 is bound
same way as in the (user-provided) definitions of A and B. It is              within t1 and t2 , while x2 is bound within t2 . This is desugared
worth noting that A and B need not belong to the same algebraic               by quantifiying x1 universally above the arrow and quantifying x2
data type: thus, a memory block can be re-used for a completely               existentially in the right-hand side of the arrow.
new purpose. Furthermore, the tag B may be associated with an                     As an example, consider the type of :=, the function that writes
immutable algebraic data type: in that case, the block is frozen,             a reference. This function expects a pair of a reference x whose
that is, becomes forever immutable. This feature is exploited in the          content has type a and of a value of type b, which it stores into x.
concatenation of immutable lists (Figure 1, line 19).                         At the end, x has become a reference whose content has type b. The
    G IVE and TAKE are explained later on (§7).                               variable x must be mentioned in the pre- and postcondition. In the
    S UB is analogous to Hoare’s rule of consequence. It relies on            internal syntax, the type of := is:
permission subsumption, P1 ≤ P2 , defined in Figure 6 and dis-
cussed further on (§5.2), and on subtyping, t1 ≤ t2 , defined as                   ∀a, b.∀(x : term) ((=x | x @ ref a), b) → (| x @ ref b)
x @ t1 ≤ x @ t2 for a fresh x.                                                Thanks to the name introduction form, instead of planning ahead
    F RAME is analogous to the frame rule of separation logic.                and quantifying x in front of the function type, one names the first
5.2 The permission subsumption judgment                                       argument “x” on the fly. Thus, in the surface syntax, one writes:

A subset5 of the subsumption rules appears in Figure 6. Since                      ∀a, b.(consumes x : ref a, consumes b) → (| x @ ref b)
x = y is sugar for x @ =y, the rule E QUALITY R EFLEXIVE can                  This is not significantly shorter, because of the consumes keyword,
be understood as a claim that x inhabits the singleton type =x.               which must be used in the surface syntax, as explained below. In
E QUALS F OR E QUALS shows how equations are exploited: if y1                 actual use, though, the comfort afforded by this feature is critical.
and y2 are known to be equal, then they are interchangeable. (We
write ≡ for subsumption in both directions.) D UPLICATE states                6.2 The consumes annotation
that a permission that is syntactically considered duplicable can
                                                                              Often, a permission is required and returned by a function, in
in fact be duplicated. M IX S TAR introduces and eliminates (t | P ).
                                                                              which case it is unpleasant to have to write this permission twice,
W EAKEN states that every permission is affine. E XISTS I NTRO intro-
                                                                              in the precondition and postcondition. Drawing inspiration from
duces an existential permission; E XISTS ATOMIC converts between
                                                                              Sing# [15], we adopt the convention that, in the surface syntax, by
an existential permission and an existential type. When read from
                                                                              default, the permission for the argument is required and returned,
left to right, D ECOMPOSE B LOCK, which was discussed earlier (§2.2,
                                                                              i.e., it is not consumed.
§4.2), introduces a fresh name x for the value stored in y.f . When
                                                                                  For instance, the type of the list length function, which in the
read from right to left, it forgets such a name. (In that case, it is typ-
                                                                              internal syntax is:
ically used in conjunction with E XISTS I NTRO.) This rule is related
to Sing#’s explicit “expose” [15]. F OLD folds an algebraic data type               ∀a.∀(x : term)(=x | x @ list a) → (int | x @ list a)
definition, turning a structural type into a nominal type. Unfold-
ing is normally performed by case analysis (see L ET DATAU NFOLD              can in the surface syntax be written in a much more pleasant form:
in Figure 5), but in the special case where an algebraic data type                                      ∀a.list a → int
has only one branch (i.e., it is a record type), it can be implicitly
unfolded by U NFOLD. DYNAMIC A PPEARS is explained later on (§7).             The type list a is mentioned once, instead of twice, and as a side
                                                                              effect, the need to name the argument x vanishes.
5.3 The Mezzo type-checker                                                        When a permission is consumed, though, we need a way of
Implementing a checker for a highly non-deterministic system such             indicating this. This is the purpose of the consumes keyword. When
as Mezzo poses technical challenges. Our type-checker greedily                a component is marked with this keyword, the permission for this
introduces fresh auxiliary names so as to “normalize” the types and           component is required and not returned. This keyword makes sense
permissions at hand. A persistent union-find data structure keeps             only in the left-hand side of an arrow.
track of the permissions of the form “x = y”. The use of flexible                 Since internal syntax and surface syntax interpret the function
variables enables a limited form of type inference. At present, the           type differently, a translation is required, regardless of whether
                                                                              consumes is used. Consider a function type of the form t → u,
implemented type-checker is not complete with respect to the type
assignment rules. This is only a brief overview: a follow-up paper            where t does not contain any name introduction forms. Let t1 stand
devoted to the implementation of Mezzo is in the works.                       for [τ /consumes τ ]t, i.e., a copy of t where the consumes keyword
                                                                              is erased. Let t2 stand for [⊤/consumes τ ]t, i.e., a copy of t where
                                                                              every component marked with this keyword is replaced with ⊤6 .
6. Surface syntax                                                             Then, the translation of this function type is (x : t1 ) → (u |
The internal syntax, which we have been using so far, can be                  x @ t2 ). The parts of the argument that are not marked as consumed
fairly verbose. To remedy this, we introduce two syntactic con-               are returned to the caller.
ventions, which rely on the name introduction construct and on                    The type of the function insert, which appears in Figure 7 and
the consumes keyword (Figure 2). Two transformations eliminate                is discussed in §7.1, states that the first argument is consumed,
these constructs, so as to obtain a type expressed in the internal            while the second argument is not. Its translation into the internal
syntax. They are formalized in the extended version of the present            syntax is as follows:
paper [28]. Here, we give only an intuition.
                                                                                    ∀(a : type) ∀(x : term)
5 The reader is referred to the extended version of this paper [28] for the         (=x | x @ (a, bag a)) → (| x @ (unknown, bag a))
full set of rules. The omitted rules include: conjunction is commutative,
associative, and has unit empty; covariance and contravariance of the type    6 Here, we write ⊤ for unknown or empty, depending on whether the
constructors; and a few more.                                                 consumes keyword is applied to a type or a permission.
 1 abstract bag a
                                                                               bitrary sharing and tree-shaped mutable data structures. However,
 2 val create : [ a ] () -> bag a
                                                                               because mutable memory blocks are controlled by exclusive per-
 3 val insert : [ a ] ( consumes a , bag a ) -> ()                             missions, it cannot describe mutable data structures with sharing.
 4 val retrieve : [ a ] bag a -> option a
                                                                               7.1 Overview
                       Figure 7. An interface for bags                         In order to illustrate this problem, let us imagine how one could
                                                                               implement a “bag” abstraction. A bag is a mutable container, which
                                                                               supports two operations: inserting a new element and retrieving an
 1   data mutable cell a =                                                     arbitrary element.
 2     Cell { elem : a ; next : dynamic }                                          We would like our implementation to offer the interface in
 3                                                                             Figure 7. There, bag is presented as an abstract type. Because
 4 data mutable bag a =                                                        it is not explicitly declared duplicable, it is regarded as affine.
 5      Empty { head , tail : () }                                             Hence, a bag “has a unique owner”, i.e., is governed by a non-
 6 | NonEmpty { head , tail : dynamic }
                                                                               duplicable permission. The function create creates a new bag,
 7 adopts cell a
 8
                                                                               whose ownership is transferred to the caller. The type of insert
 9   val create [ a ] () : bag a =                                             indicates that insert(x, b) requires the permissions “x @ t” and
10     Empty { head = (); tail = () }                                          “b @ bag t”, for some type t, and returns only the latter. Thus, the
11                                                                             caller gives up the ownership of x, which is “transferred to the bag”.
12 val insert [ a ] ( consumes x : a , b : bag a ) : () =                      Conversely, the call “let o = retrieve b in ...” produces the
13   let c = Cell { elem = x ; next = () } in                                  permission “o @ option a”, which means that the ownership of
14   c . next <- c ;                                                           the retrieved element (if there is one) is “transferred from the bag
15   give c to b ;                                                             to the caller”.
16   match b with                                                                  To implement bags, we choose a simple data structure, namely
17   | Empty ->
18         tag of b <- NonEmpty ;
                                                                               a mutable singly-linked list. One inserts elements at the tail and
19         b . head <- c ;                                                     extracts elements at the head, so this is a FIFO implementation.
20         b . tail <- c                                                       One distinguished object b, “the bag”, has pointers to the head and
21   | NonEmpty ->                                                             tail of the list, so as to allow constant-time insertion and extraction.
22         take b . tail from b ;                                              (We use “object” as a synonym for “memory block”.)
23         b . tail . next <- c ;                                                  This data structure is not tree-shaped: the last cell in the list is
24         give b . tail to b ;                                                accessible via two distinct paths. In order to type-check this code,
25         b . tail <- c                                                       we must allow the ownership hierarchy and the structure of the heap
26   end                                                                       to differ. More specifically, we would like to view the list cells as
27
28 val retrieve [ a ] ( b : bag a ) : option a =
                                                                               collectively owned by the bag b. That is, we wish to keep track of
29   match b with                                                              just one exclusive permission for the group formed by the list cells,
30   | Empty ->                                                                as opposed to one permission per cell.
31       None                                                                      We use the name b as a name for this group. When a cell c joins
32   | NonEmpty ->                                                             the group, we say that b adopts c, and when c leaves the group,
33       take b . head from b ;                                                we say that b abandons c. In other words, the bag b is an adopter,
34       let x = b . head . elem in                                            and the list cells c are its adoptees. In terms of ownership, adopter
35       if b . head == b . tail then begin                                    and adoptees form a unit: the exclusive permission that controls b
36         tag of b <- Empty ;                                                 also represents the ownership of the group, and is required by the
37         b . head <- ();
38         b . tail <- ()
                                                                               adoption and abandon operations.
39       end else begin                                                            Adoption requires and consumes an exclusive permission for
40         b . head <- b . head . next                                         the cell c that is about to be adopted: the ownership of c is trans-
41       end ;                                                                 ferred to the group. Conversely, abandon produces an exclusive per-
42       Some { value = x }                                                    mission for the cell c that is abandoned: the group relinquishes the
43   end                                                                       ownership of c.
                                                                                   Abandon must be carefully controlled. If a cell could be aban-
                 Figure 8. A FIFO implementation of bags                       doned twice, two permissions for it would appear, which would be
                                                                               unsound. Due to aliasing, though, it is difficult to statically prevent
                                                                               this problem. Instead, we decide to record at runtime which object
     6.3 Function definitions                                                  is a member of which group, and to verify at runtime that abandon
     In the internal syntax, functions take the form fun (x : t1 ) : t2 = e,   is used in a safe way.
     where one variable, namely x, is bound in e. In the surface syntax,
     instead, functions take the form fun t1 : t2 = e. The argument            7.2 Details
     type t1 is interpreted as a pattern, and the names that it introduces     Let us now explain in detail the dynamic semantics of adoption and
     are considered bound in e. An example is fun (x : int, y : int) :         abandon (what these operations do) as well as their static semantics
     int = x + y, where (x : int, y : int) is the type of the argument,        (what the type-checker requires).
     int is the type of the result, and x and y are bound in the function
     body, which is x + y.                                                     Adopter fields We maintain a pointer from every adoptee to its
                                                                               adopter. Within every object, there is a hidden “adopter” field,
                                                                               which contains a pointer to the object’s current adopter, if it has
     7. Adoption and abandon                                                   one, and null otherwise. This information is updated when an
     The permission discipline that we have presented so far has limited       object is adopted or abandoned. In terms of space, the cost of this
     expressive power. It can describe immutable data structures with ar-      design decision is one field per object.
The type dynamic The permission “c @ dynamic” guarantees                 queue, b.head, is abandoned by b. This yields a permission at type
that c is a pointer to a memory block and grants read access to          “cell a” for this cell. This permission lets us read b.head.elem
the field c.adopter. This can be used to verify the identity of c’s      and b.head.next and allows us to produce the permission “x @ a”,
adopter. In other words, “c @ dynamic” can be viewed as a permis-        where x is the value found in b.head.elem.
sion to perform a dynamic group membership test. It is a duplicable          Abandon and adoption are also used inside insert, at lines 22
permission. It appears spontaneously when c is known to be a             and 24. There, the bag b is non-empty, and the cell b.tail must
(mutable) object: this is stated by the rule DYNAMIC A PPEARS in         be updated in order to reflect the fact that it is no longer the last
Figure 6.                                                                cell in the queue. However, we cannot just go ahead and access
    In the bag implementation, shown in Figure 8, the head and tail      this cell, because the only permission that we have at this point
fields of a non-empty bag object, as well as the next field of every     for this cell is at type “dynamic”. Instead, we must take the cell
cell object, have type dynamic (lines 2 and 6). Because dynamic is       out of the group, update it, and put it back. We allow writing
duplicable, sharing is permitted: for instance, the pointers b.head      “taking b.tail from b begin ... end” as sugar for such a well-
and b.tail might happen to be equal.                                     parenthesized use of take and give.
Adopts clauses When a cell c is adopted, the exclusive per-              7.3 Discussion
mission that describes it, namely “c @ cell a”, disappears. Only
“c @ dynamic” remains. As a result, the information that c is a cell     To the best of our knowledge, adoption and abandon are new.
is lost: the type-checker can no longer tell how many fields exist       Naturally, the concept of group, or region, has received sustained
in the object c and what they contain. When the bag b later aban-        interest in the literature [11, 12, 16, 32]. Regions are usually viewed
dons c, we would like the permission “c @ cell a” to re-appear.          either as a dynamic memory management mechanism or as a purely
How can the type-checker recover this information?                       static concept. Adoption and abandon, on the other hand, offer a
    Fortunately, when b abandons c, the type-checker has access to       dynamic ownership control mechanism, which complements our
the type of b. Thus, provided the type of the adopter determines the     static permission discipline.
type of its adoptees, this problem is solved.                                Adoption and abandon are a very flexible mechanism, but also
    For an object b of type t to serve as an adopter, where t is         a dangerous one. Because abandon involves a dynamic check, it
an algebraic data type, we require that the definition of t contain      can cause the program to encounter a fatal failure at runtime. In
the clause “adopts u” and that t and u be exclusive types. This          principle, if the programmer knows what she is doing, this should
is illustrated in Figure 8, where the definition of “bag a” says         never occur. There is some danger, but that is the price to pay for a
“adopts cell a” (line 7).                                                simpler static discipline. After all, the danger is effectively less than
    Because the type of the adoptees must not be forgotten when an       in ML or Java, where a programming error that creates an undesired
algebraic data type is unfolded, structural permissions also carry       alias goes completely undetected—until the program misbehaves in
an adopts clause. In the case of bags, for instance, the permission      one way or another.
“b @ bag a” is refined by the match constructs of lines 16 and 29            One might wonder why the type dynamic is so uninformative:
into either “b @ Empty { head, tail: () } adopts cell a” or              it gives no clue as to the type of the adoptee or the identity of the
“b @ NonEmpty { head, tail: dynamic } adopts cell a”, and,               adopter. Would it be possible to parameterize it so as to carry either
conversely, either of these permissions can be folded back to            information? The short answer is negative. The type dynamic is
“b @ bag a”.                                                             duplicable, so the information that it conveys should be stable (i.e.,
    We write that “t adopts u” if either t is an algebraic data type     forever valid). However, the type of the adoptee, or the identity
whose definition contains the clause “adopts u” or t is a structural     of the adopter, may change with time, through a combination of
type that contains the clause “adopts u”.                                strong updates and give and take instructions. Thus, it would not
                                                                         make sense for dynamic to carry more information.
Adoption The syntax of adoption is “give c to b”. This in-                   That said, we believe that adoption and abandon will often
struction requires two permissions “c @ u” and “b @ t”, where            be used according to certain restricted protocols, for which more
t adopts u ( G IVE, Figure 4). At the program point that follows this    information is stable, hence can be reflected at the type level.
instruction, the permission “b @ t” remains available, but “c @ u”       For instance, in the bag implementation, a cell only ever has one
has been consumed. Fortunately, not everything about c is forgot-        adopter, namely a specific bag b. In that case, one could hope to
ten. The permission “c @ dynamic”, which is present before the           work with a parameterized type dynamic′ b, whose meaning would
adoption instruction because “c @ u” spontaneously gives rise to         be “either this object is currently not adopted, or it is adopted by b”.
“c @ dynamic”, remains present after adoption.                           Ideally, dynamic′ would be defined on top of dynamic in a library
    The runtime effect of this operation is to write the address b to    module, and its use would lessen the risk of confusion.
the field c.adopter. The exclusive permission “c @ u” guarantees
that this field exists and that its value, prior to adoption, is null.
    In the bag implementation (Figure 8), adoption is used at the        8. Other means of permitting sharing
beginning of insert (line 15), after a fresh cell c has been allocated   Adoption and abandon is not the only way of sharing mutable data.
and initialized. This allows us to maintain the (unstated) invariant     We now describe two other mechanisms, namely nesting and locks.
that every cell that is reachable from b is adopted by b.
Abandon The syntax of abandon is “take c from b”. This in-               8.1 Nesting
struction requires “b @ t” and “c @ dynamic”, where t adopts “u”,        Nesting [7] is a mechanism by which an object x adopts (so to
for some type u (TAKE, Figure 4). After this instruction, “b @ t”        speak) a permission P . It is a purely static mechanism. The act of
remains available. Furthermore, the permission “c @ u” appears.          nesting P in x has no runtime effect, but consumes P and produces
    The runtime effect of this operation is to check that the field      a witness, a permission which Boyland writes P ≺ x. Because
c.adopter contains the address b and to write null into this field,      nesting is irreversible, such a witness is duplicable.
so as to reflect the fact that b abandons c. If this check fails, the       Once P has been nested in x, whoever has exclusive owner-
execution of the program is aborted.                                     ship of x may decide to temporarily recover P . This is done via
    In the bag implementation (Figure 8), abandon is used near           two symmetric operations, say “focus” and “defocus”, which in the
the beginning of retrieve, at line 33. There, the first cell in the      presence of P ≺ x convert between x @ t and P ∗ (P −+x @ t)
(where the type t is arbitrary, but must be exclusive). The permis-        program verification, as it allows the owner to impose an object in-
sion P −+x @ t means that P has been “carved out” of x. While              variant. Permission systems [5, 7, 17] annotate pointers not with
this is the case, x @ t is temporarily lost: in order to recover it, one   owners, but with permissions. The permission carried by a pointer
must give up P . Thus, it is impossible to simultaneously carve two        tells how this pointer may be used (e.g. for reading and writing,
permissions out of x.                                                      only for reading, or not at all) and how other pointers to the same
    Nesting subsumes Fähndrich and DeLine’s adoption and focus             object (if they exist) might be used by others.
[16]. We view it as a purely static cousin of adoption and abandon.            The systems mentioned so far are refinements (restrictions) of a
Adoption is more flexible in several important ways: it allows ac-         traditional type discipline. Separation logic [29] departs from this
cessing two adoptees at the same time, and allows abandoning an            approach and obeys a principle that we dub “owner-as-asserter”.
object forever. Nesting has advantages over adoption and abandon:          (In O’Hearn’s words, “ownership is in the eye of the asserter” [25].)
it cannot fail at runtime; it has no time or space overhead; one may       Objects are described by logical assertions. To assert is to own: if
nest a permission, whereas one adopts an object; and nesting is het-       one knows that “x is a linked list”, then one may read and write the
erogeneous, i.e., an object x can nest multiple distinct permissions,      cells that form this list, and nobody else may. Whereas the pre-
whereas, in the case of adoption and abandon, all adoptees of x            viously mentioned systems combine structural descriptions (i.e.,
must have the same type.                                                   types) with owner or permission annotations, separation logic as-
    Nesting can be axiomatized in Mezzo as a trusted library, whose        sertions are at once structural descriptions and claims of ownership.
interface appears in the extended version of this paper [28]. In               Mezzo follows the “owner-as-asserter” principle. In the future,
principle, this requires extending the proof of type soundness; we         this should allow us to annotate permissions with logical assertions
have not done so. When applicable, nesting seems preferable to             and use that as a basis for the specification and proof of Mezzo
adoption; however, adoption is more widely applicable.                     programs. A tempting research direction is to translate Mezzo into
                                                                           F⋆ [31]. This purely functional programming language is equipped
8.2 Locks                                                                  with affine values, with powerful facilities for expressing program
Dynamically-allocated locks in the style of concurrent separation          specifications and proofs, and with a notion of proof erasure.
logic [25, 18, 19, 8] are another dynamic mechanism for mediating              Although our permission discipline is partly inspired by sepa-
access to a permission. A new lock, of type lock P , where P is an         ration logic [29], it is original in several ways. It presents itself as
arbitrary permission, is created via a function new. The functions         a type system, as opposed to a program logic. This makes it less
acquire and release both take the lock as an argument; acquire             expressive than a program logic, but more pervasive, in the sense
produces the permission P , which release consumes. The type               that it can (and must) be used at every stage of a program’s de-
lock P is duplicable, so an arbitrary number of threads can share          velopment, without proof obligations. It distinguishes between im-
the lock and simultaneously attempt to acquire it. Within a critical       mutable and mutable data, supports first-class functions, and takes
section, delimited by acquire and release, the “lock invariant” P          advantage of algebraic data types in novel ways.
is available, whereas, outside of it, it is not. The “invariant” P can         As far as we know, Ownership or Universe Types cannot express
in fact be broken within the critical section, provided it is restored     uniqueness or ownership transfer. Müller and Rudich [23] extend
when one reaches the end of the section.                                   Universe Types with these notions. They rely on the fact that each
    Locks introduce a form of hidden state into the language. Be-          object maintains, at runtime, a pointer to its owner. The potential
cause the permission l @ lock P is duplicable, it can be captured          analogy with our adopter fields deserves further study.
by a closure. As a result, it becomes possible for a function to per-          The use of singleton types to keep track of equations, and the
form a side effect, even though its type does not reveal this fact         idea that pointers can be copied, whereas permissions are affine,
(the pre- and postcondition are empty). Mezzo’s modest library for         are inspired by Alias Types [30]. Linear [1] and affine [33] type
memoization exploits this feature.                                         systems support strong updates and often view permissions (or
    Locks can be used to encode “weak” (duplicable) references in          “capabilities”) as ordinary values, which hopefully the compiler
the style of ML and duplicable references with affine content in the       can erase. By offering an explicit distinction between permissions
style of Alms [33], both of which support arbitrary sharing.               and values, we guarantee that permissions are erased, and we are
    Locks can be axiomatized in Mezzo as a library, whose interface        able to make the flow of permissions mostly implicit. Through
appears in the extended version of this paper [28]. Again, the proof       algebraic data types and through the type constructor (t | P ), we
of type soundness must be extended; we have begun this work. We            retain the ability to tie a permission to a value, if desired.
view locks as complementary to adoption and abandon and nesting.               Regions [30, 16, 1] have been widely used as a technical device
In a typical usage scenario, a lock protects an adopter, which in turn     that allows a type to indirectly refer to a value or set of values.
controls a group of adoptees (or of nested permissions). This allows       In Mezzo, types refer to values directly. This simplifies the meta-
a group of objects to be collectively protected by a single lock. It       theory and the programmer’s view.
should be noted that (we believe) adoption and abandon are sound               Gordon et al. [17] ensure data-race freedom in an extension
in a concurrent setting.                                                   of C#. They qualify types with permissions in the set immutable,
                                                                           isolated, writable, or readable. The first two roughly correspond
9. Related work                                                            to our immutable and mutable modes, whereas the last two have
                                                                           no Mezzo analogue. Shared (writable) references allow legacy se-
The literature offers a wealth of type systems and program logics          quential code to be considered well-typed. A salient feature is the
that are intended to help write correct programs in the presence of        absence of an alias analysis, which simplifies the system consider-
mutable, heap-allocated state. We review a few of them and contrast        ably. This comes at a cost in expressiveness: mutable global vari-
them with Mezzo.                                                           ables, as well as shared objects protected by locks, are disallowed.
    Ownership Types [10] and its descendants restrict aliasing. Ev-            Plaid [2] and Mezzo exhibit several common traits. A Plaid ob-
ery object is owned by at most one other object, and an “owner-            ject does not belong to a fixed class, but can move from one “state”
as-dominator” principle is enforced: every path from a root to an          to another: this is related to Mezzo’s tag update. Methods carry state
object x must go through x’s owner. Universe Types [14] impose             pre- and postconditions, which are enforced via permissions [5].
a slightly different principle, “owner-as-modifier”. Arbitrary paths       Plaid is more ambitious in that states are organized in an extensible
are allowed to exist in the heap, but only those that go through x’s       hierarchy, whereas algebraic data types are flat and closed.
owner can be used to modify x. This approach is meant to support
10. Conclusion and future work                                                    [15] Manuel Fähndrich, Mark Aiken, Chris Hawblitzel, Orion Hodson,
                                                                                       Galen Hunt, James R. Larus, and Steven Levi. Language support for fast and reliable me
Mezzo is a high-level functional and imperative programming lan-                       In EuroSys, pages 177–190, 2006.
guage where the traditional concept of “type” is replaced with a
more powerful concept of “permission”. Distinguishing duplica-                    [16] Manuel Fähndrich and Robert DeLine. Adoption and focus: practical linear types for im
ble, exclusive, and affine permissions allows reasoning about state                    In Programming Language Design and Implementation (PLDI),
                                                                                       pages 13–24, 2002.
changes. We strive to achieve a balance between simplicity and
expressiveness by marrying a static discipline of permissions and                 [17] Colin S. Gordon, Matthew J. Parkinson, Jared Parsons, Aleks Brom-
a novel dynamic form of adoption and abandon. By adding other                          field, and Joe Duffy. Uniqueness and reference immutability for safe parallelism.
mechanisms for controlling sharing, such as nesting and locks, we                      In Object-Oriented Programming, Systems, Languages, and Applica-
                                                                                       tions (OOPSLA), pages 21–40, 2012.
augment the expressiveness of the language and emphasize that the
permission discipline is sufficiently powerful to express these no-               [18] Alexey Gotsman, Josh Berdine, Byron Cook, Noam Rinetzky, and
tions. Mezzo is type-safe: well-typed programs cannot go wrong                         Mooly Sagiv. Local reasoning for storable locks and threads. Tech-
(but an abandon operation can fail). We have carried out a machine-                    nical Report MSR-TR-2007-39, Microsoft Research, 2007.
checked proof of type safety [26]. In the future, we would like to                [19] Aquinas Hobor, Andrew W. Appel, and Francesco Zappa Nardelli.
extend Mezzo with support for shared-memory concurrency. We                            Oracle semantics for concurrent separation logic. In European Sym-
believe that, beyond locks (§8.2), many abstractions (threads, chan-                   posium on Programming (ESOP), volume 4960 of Lecture Notes in
nels, tasks, etc.) can be axiomatized so as to guarantee that well-                    Computer Science, pages 353–367. Springer, 2008.
typed code is data-race-free.                                                     [20] Bart Jacobs and Frank Piessens. The VeriFast program verifier. Tech-
                                                                                       nical Report CW-520, Department of Computer Science, Katholieke
                                                                                       Universiteit Leuven, 2008.
References                                                                        [21] Toshiyuki Maeda, Haruki Sato, and Akinori Yonezawa. Extended alias type system usin
                                                                                     In Types in Language Design and Implementation (TLDI), 2011.
 [1] Amal Ahmed, Matthew Fluet, and Greg Morrisett. L3 : A linear language with locations.
     Fundamenta Informaticæ, 77(4):397–449, 2007.                              [22] Yasuhiko Minamide. A functional representation of data structures with a hole.
 [2] Jonathan Aldrich, Joshua Sunshine, Darpan Saini, and Zachary                    In Principles of Programming Languages (POPL), pages 75–84,
     Sparks. Typestate-oriented programming. In Companion to Object-                 1998.
     Oriented Programming, Systems, Languages, and Applications (OOP-          [23] Peter Müller and Arsenii Rudich. Ownership transfer in universe types.
     SLA), pages 1015–1022, 2009.                                                    In Object-Oriented Programming, Systems, Languages, and Applica-
                                                                                     tions (OOPSLA),
 [3] Mike Barnett, K. Rustan M. Leino, and Wolfram Schulte. The Spec# programming system:             pages 461–478, 2007.
                                                                                             An overview.
     In Construction and Analysis of Safe, Secure and Interoperable Smart      [24] Karl Naden, Robert Bocchino, Jonathan Aldrich, and Kevin Bierhoff.
     devices (CASSIS), volume 3362 of Lecture Notes in Computer Sci-                 A type system for borrowing permissions. In Principles of Program-
     ence, pages 49–69. Springer, 2004.                                              ming Languages (POPL), pages 557–570, 2012.
 [4] Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. Smallfoot: Modular [25]
                                                                                 automatic
                                                                                      Peter assertion checking
                                                                                            W. O’Hearn.         with separation
                                                                                                           Resources,           logic.
                                                                                                                      concurrency  and local reasoning. The-
     In Formal Methods for Components and Objects, volume 4111 of                     oretical Computer Science, 375(1–3):271–307, 2007.
     Lecture Notes in Computer Science, pages 115–137. Springer, 2005.
                                                                                 [26] François Pottier. Type soundness for Core Mezzo. Unpublished, Jan-
 [5] Kevin Bierhoff and Jonathan Aldrich. Modular typestate checking of aliased objects.
                                                                                      uary 2013.
     In Object-Oriented Programming, Systems, Languages, and Applica-
     tions (OOPSLA), pages 301–320, 2007.                                        [27] François  Pottier and Jonathan Protzenko. Mezzo. http://gallium.inria.fr/~prot
                                                                                      July 2013.
 [6] Kevin Bierhoff, Nels E. Beckman, and Jonathan Aldrich. Practical API protocol checking with access permissions.
     In European Conference on Object-Oriented Programming (ECOOP),              [28] François Pottier and Jonathan Protzenko. Programming with permissions in Mezzo (lon
                                                                                      Unpublished, July 2013.
     volume 5653 of Lecture Notes in Computer Science, pages 195–219.
     Springer, 2009.                                                             [29] John C. Reynolds. Separation logic: A logic for shared mutable data structures.
 [7] John Tang Boyland. Semantics of fractional permissions with nesting.             In Logic in Computer Science (LICS), pages 55–74, 2002.
     ACM Transactions on Programming Languages and Systems, 32(6),               [30] Frederick Smith, David Walker, and Greg Morrisett. Alias types.
     2010.                                                                            In European Symposium on Programming (ESOP), volume 1782 of
                                                                                      Lecture
 [8] Alexandre Buisse, Lars Birkedal, and Kristian Støvring. A step-indexed Kripke model      Notes in logic
                                                                                         of separation Computer    Science,locks.
                                                                                                             for storable    pages 366–381. Springer, 2000.
     Electronic Notes in Theoretical Computer Science, 276:121–143,           [31] Nikhil Swamy, Juan Chen, Cédric Fournet, Pierre-Yves Strub, Karthik
     2011.                                                                         Bhargavan, and Jean Yang. Secure distributed programming with value-dependent types
                                                                                   In International Conference on Functional Programming (ICFP),
 [9] Arthur Charguéraud. Characteristic Formulae for Mechanized Program Verification.
     PhD thesis, Université Paris 7, 2010.                                         pages 266–278, 2011.
                                                                                 [32]
[10] David G. Clarke, John M. Potter, and James Noble. Ownership types for flexible    Nikhil
                                                                                    alias      Swamy, Michael Hicks, Greg Morrisett, Dan Grossman, and
                                                                                          protection.
     In Object-Oriented Programming, Systems, Languages, and Applica-                  Trevor Jim. Safe manual memory management in Cyclone. Science
     tions (OOPSLA), pages 48–64, 1998.                                                of Computer Programming, 62(2):122–144, 2006.
                                                                                 [33]  Jesse A.
[11] Karl Crary, David Walker, and Greg Morrisett. Typed memory management in a calculus         Tov and Riccardo Pucella. Practical affine types. In Princi-
                                                                                             of capabilities.
     In Principles of Programming Languages (POPL), pages 262–275,                     ples of Programming Languages (POPL), pages 447–458, 2011.
     1999.                                                                     [34] Thomas Tuerk. Local reasoning about while-loops. Unpublished,
                                                                                     2010.
[12] Robert DeLine and Manuel Fähndrich. Enforcing high-level protocols in low-level software.
     In Programming Language Design and Implementation (PLDI),                 [35] David Walker and Greg Morrisett. Alias types for recursive data structures.
     pages 59–69, 2001.                                                              In Types in Compilation (TIC), volume 2071 of Lecture Notes in Com-
[13] Robert DeLine and Manuel Fähndrich. Typestates for objects. In                  puter Science, pages 177–206. Springer, 2000.
     European Conference on Object-Oriented Programming (ECOOP),
     volume 3086 of Lecture Notes in Computer Science, pages 465–490.
     Springer, 2004.
[14] Werner Dietl and Müller Peter. Universes: Lightweight ownership for JML.
     Journal of Object Technology, 4(8):5–32, 2005.
