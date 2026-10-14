                                                Compositional Reasoning for Side-effectful
                                                    Iterators and Iterator Adapters

                                             Aurea Bílá1[0000−1111−2222−3333] , Jonas Hansen1[1111−2222−3333−4444] , Peter
                                                          Müller1[2222−−3333−4444−5555] , and Alexander J.
                                                                  Summers2[2222−−3333−4444−5555]
arXiv:2210.09857v1 [cs.LO] 18 Oct 2022




                                                      1
                                                          Department of Computer Science, ETH Zurich, Switzerland
                                                                            2
                                                                              UBC, Canada



                                                 Abstract. Iteration is a programming operation that traditionally refers
                                                 to visiting the elements of a data structure in sequence. However, modern
                                                 programming systems such as Rust, Java, and C# generalise iteration
                                                 far beyond the traditional use case. They allow iterators to be param-
                                                 eterised with (potentially side-effectful) closures and support the com-
                                                 position of iterators to form iterator chains, where each iterator in the
                                                 chain consumes values from its predecessor and produces values for its
                                                 successor. Such generalisations pose three major challenges for modular
                                                 specification and verification of iterators and the client code using them:
                                                 (1) How can parameterised iterators be specified modularly and their
                                                 (accumulated) side effects reasoned about? (2) How can the behaviour
                                                 of an iterator chain be derived from the specifications of its component
                                                 iterators? (3) How can proofs about such iterators be automated?
                                                 We present the first methodology for the modular specification and ver-
                                                 ification of advanced iteration idioms with side-effectful computations.
                                                 It addresses the three challenges above using a combination of inductive
                                                 two-state invariants, higher-order closure contracts, and separation logic-
                                                 like ownership. We implement and our methodology in a state-of-the-art
                                                 SMT-based Rust verifier. Our evaluation shows that our methodology is
                                                 sufficiently expressive to handle advanced and idiomatic iteration idioms
                                                 and requires modest annotation overhead.

                                                 Keywords: Deductive verification · Verified software · Iterators · Rust.


                                         1     Introduction
                                         Iterators are a ubiquitous programming idiom traditionally used to abstractly
                                         and simply enumerate the elements of a collection. Verification of such simple
                                         use cases comes down to proving that an iterator yields all elements of a collec-
                                         tion in a specified linear order and showing that the used iterator does not get
                                         invalidated e.g. by concurrent modifications of the underlying collection [5].
                                             Modern programming languages such as C#, Java, Python, and Rust sup-
                                         port iteration patterns that go far beyond the traditional use case. For instance,
                                         iterators are used to perform computations over streams of values, such as com-
                                         puting a moving average; the computation itself is typically parameterisable by
2        A. Bílá et al.

custom code such as closures. In general-purpose languages, both the iterators
themselves and these closures may perform side effects, e.g. to modify the data
structure in-place or to accumulate computations based on the values seen so
far; code which uses such iterators depends on properties of this modified state.
    Moreover, it is increasingly prevalent for languages to support the composi-
tion of iterators, where an iterator processes values produced by another iterator
(rather than obtained directly from a collection data structure). We follow the
Rust terminology and call this kind of iterator an iterator adapter (adapter for
short). Iterator adapters may be composed to form iterator chains, where each
iterator in the chain consumes the values from its predecessor in the chain and
produces values for its successor; the overall chain acts as a composite iterator.
    It is common for imperative languages to provide a variety of iterator adapters,
e.g. Java’s Streams API, C#’s LINQ, Python’s iterables, and Rust’s iterator
adapters all support potentially-side-effectful variants of common functional pro-
gramming operations such as filter, fold, and map. These languages also allow
developers to implement their own custom iterators and iterator adapters.
    The following Rust example illustrates the use of iterators and adapters:
 1   let mut sum = 0;
 2   some_vector                     // start with a vector of integers
 3       .iter()                     // create an iterator over the vector
 4       .map(|x| { sum += x; sum }) // running totals of seen elements
 5       .filter(|x| x < 10)         // only keep totals smaller than 10
 6       .collect::<Vec<_>>();       // collect the results into a vector

    The function iter yields a traditional iterator for the underlying vector,
which provides the input to the iterator chain. The map adapter is parameterised
with a closure, which mutates the captured variable sum. The subsequent filter
adapter, also parameterised with a closure for the filter criterion, removes ele-
ments, and finally collect stores the produced elements in another vector.
    Such advanced iteration patterns lead to concise and readable code, but they
also pose several challenges for modular specification and verification. Modular-
ity is important to give correctness guarantees for libraries, to make verification
scale, and to reduce the effort for re-verification when parts of a codebase change.
The three main challenges are:

 1. How to specify parameterised iterators modularly. The behaviour of iterators
    such as map depends on their argument closures. Modular reasoning aims at
    verifying the iterator implementation against a specification that accounts
    for all possible closures that may be used by the client code. This requires a
    specification that is parametric in the argument closure, which is especially
    challenging for closures that have side effects such as the closure in line 4
    of our example. The specification of the iterator must be strong enough
    (1) to prove how the side effects affect the values produced by the iterator
    and (2) to determine the accumulated side effects of all calls to the iterator
    and its related closures by the time the iterator terminates. The latter is
    relevant because variables mutably captured by a closure, such as sum in the
  Compositional Reasoning for Side-effectful Iterators and Iterator Adapters     3

    motivating example, become accessible to the client code once again when
    the iterator terminates (and, by extension, the closure expires).
    In our example, assume that some_vector contains the values 6, 2, 9. map’s
    specification must be strong enough to prove (1) that the iterator produces
    the sums of the prefixes of the values it iterates over, that is, 6, 8, 17, and
    (2) that the final value of sum is 17.
 2. How to reason modularly about iterator chains. Modular verification requires
    that we can prove the behaviour of an iterator chain based on the specifica-
    tions of its component iterators. In particular, verification of a chain must
    not require re-verification of its component iterators (whose code might not
    even be available); it should not be necessary to adapt the specification of an
    iterator for each and every instantiation and composition. Instead, the spec-
    ification of an iterator must be agnostic to the source of values it consumes
    and to the downstream processing of the values it produces.
    In our example, we want to prove that the final vector contains the values
    6 and 8, without requiring the specifications of the intermediate adapters to
    either refer to the initial vector or depend on the subsequent adapters.
 3. How to automate verification of modern iterator and adapter patterns. The
    behaviour of iterator chains depends on the behaviour of their component
    iterators, which may in turn depend on their argument closures. This hints
    at the need for higher-order logics (specifications which depend on specifica-
    tions), which greatly complicate proof automation; we aim instead for proofs
    which can be automated with first-order SMT solvers.

State of the art. Prior work on iterator verification only partially addresses the
challenges outlined above. Pereira [13] defines a modular verification technique
using two predicates per iterator to specify the sequence of produced values and
a termination condition. This technique is automated using Why3 [4]. It par-
tially addresses Challenge 1 by providing abstract, implementation-independent
specifications for individual iterators. However, although higher-order iterators
are discussed, this only refers to simple iterators parameterised by side-effect-
free functions, as in a functional fold operation. Support for iterators with side
effects (for instance, to prove the final value of sum in our example) is discussed
as future work in the form of a tool which rewrites client code into equivalent
loops, leaving the appropriate specification and verification to manual proof ef-
fort. Iterator composition is not addressed.
    Verification of higher-order functions such as fold in Rust is partially ad-
dressed in existing work on closure verification [16], allowing one to reason mod-
ularly about side-effectful closures, such as the argument to map in our example.
However, this technique does not provide specification or verification support for
iterators and adapters that use closures in well-known but functionally complex
ways (e.g. as an argument to a fold).

This work. We present the first modular specification and verification tech-
nique for advanced iteration patterns that addresses the three challenges above.
4         A. Bílá et al.

To address Challenge 1, we associate iterators with four key specifications: (1) the
sequence of elements, produced, returned by the iterator so far, (2) a completed
predicate that expresses when iteration terminates, (3) a two-state postcondition
step that relates two consecutive iterator states and (4) a two-state predicate
leadsto that inductively relates any previous state of the iterator to any more
recent state. The first two points are inspired by Pereira [13], but importantly
our technique can also handle side-effectful iterators by characterising the in-
termediate states occurring during an iteration, not only the returned elements.
We employ so-called call descriptions [16] to parameterise the step and leadsto
predicates with the behaviour of closures (e.g. for the map and filter iterators
above). In order to reason about the accumulated effects of an iterator, we prove
that each call to next satisfies the transitive two-state invariant leadsto. Con-
sequently, this invariant also holds between the initial and the final state of the
entire iteration and, thus, is able to characterise its overall effects.
    We show that our newly developed methodology generalises directly to it-
erator chains (Challenge 2): the leadsto predicate of an iterator adapter may
refer to the leadsto predicate and the produced sequence of its predecessor in
an iteration chain to specify the successor’s behaviour in terms of the behaviour
of the predecessor. In particular, these specification ingredients let the successor
maintain ghost data structures that keep track of all states of the predecessor
iterator and of any argument closures that occur during the iteration. We can
then reason about side effects via invariants over these ghost structures.
    Our methodology builds exclusively on specification constructs for which au-
tomated verification techniques exist (ghost fields, invariants, and closure call
descriptions). It can, thus, be automated in SMT-based verifiers, as we demon-
strate through an extension of the Rust verifier Prusti [1] (Challenge 3).
    We present our technique in the context of Rust, whose ownership type sys-
tem complements our methodology by preventing concurrent modifications of
an iterated-over data structure, or undesirable interference between iterators.
However, our technique would apply equally to other languages if augmented
with an alternative ownership-like technique such as separation logic [14].


Contributions and outline. The main contributions of our paper are:

    – We present the first specification and verification methodology for general
      side-effectful iterators (→ Sec. 3, Sec. 4).
    – We demonstrate how to use this methodology to reason about the effects
      and resulting values of complex iterator chains (→ Sec. 5).
    – We show how to express these specifications modularly for existing iterator
      hierarchies (→ Sec. 6).
    – We implement our work in the Prusti verifier [1] and demonstrate its expres-
      siveness on several challenging examples (→ Sec. 8).

Additionally, we provide the necessary background on Rust (→ Sec. 2), explain
why our approach is sound (→ Sec. 7), and discuss related work (→ Sec. 9).
     Compositional Reasoning for Side-effectful Iterators and Iterator Adapters   5

2      Background
In this section we briefly describe Rust, focusing on its ownership type system
(→ Sec. 2.1), then we discuss the relevance of this type system to verification in
general and our methodology in particular (→ Sec. 2.2).

2.1     Rust
Rust [10] is a modern systems programming language that is rapidly gaining
popularity. Among mainstream languages, it is unique due to its ownership type
system, which eliminates certain categories of common software bugs, such as
data races, use-after-free bugs, dangling pointers, and null pointer dereferences.
    The Rust type system maintains a crucial invariant: any value is either muta-
ble or shared, but never both. To maintain this invariant, values are categorised
as: owned, mutably borrowed, or immutably borrowed. All values have a single
owner, which by default has exclusive (read/write) capabilities on the data.
Since ownership is exclusive, no other thread or function can access the owned
value without borrowing it via a reference. A value can be mutably borrowed to
create exactly one mutable reference. While the mutable reference exists, it has
the unique capability to read from and modify the borrowed value. Immutable,
or shared references, on the other hand, have a read-only capability for the bor-
rowed value. Unlike mutable references, a value can be immutably borrowed any
number of times. When all borrows expire (go out of scope) the borrowed-from
value becomes writable again. The following snippet demonstrates some of these
concepts; for a full overview of Rust we refer the reader to the Rust Book [8].
 1    struct Point { A
 2        x: i32, y: i32,
 3    }
 4    fn origin() -> Point { B
 5        Point { x: 0, y: 0 }
 6    }
 7    fn get_point_x(pt: &Point) -> &i32 { C
 8        &pt.x
 9    }
10    fn set_point_x(pt: &mut Point, x: i32) {   D

11        pt.x = x;
12    }

    The above code declares a 2D point structure A consisting of two integer
coordinates. The origin method B returns an owned Point to the caller with
both coordinates at zero (types not prefixed with an & are owned). get_point_x
 C   takes a shared reference to a point (indicated by &Point), and returns a
shared reference to its x coordinate. Finally, set_point_x D takes a mutable
reference to a point (indicated by &mut Point), and sets its x coordinate to the
given value. The following code makes use of these methods:
 1    let mut pt = origin();
 2    set_point_x(&mut pt, 5);
 3    let x = get_point_x(&pt);
6         A. Bílá et al.

 4    // set_point_x(&mut pt, 6); // not allowed!
 5    println!("x␣coordinate␣is:␣{}", *x);
 6    set_point_x(&mut pt, 7);

    The variable pt is an owned Point instance. The first call to set_point_x is
made with a mutable reference to pt. The x variable creates a shared borrow
into pt. The mutable borrow in the call to set_point_x (on line 5) is rejected by
the type system because it would create a mutable reference to a Point object
while an immutable reference to its x field still exists.
    The Rust type system supports concrete types (such as structs, enums, and
unions) and traits. Traits make it possible to define an interface shared across
many types, optionally including default implementations for its methods. Traits
are also used to declare the iterator interface in Rust, as we will see in Sec. 4.3.

2.2     Deductive verification in a Rust setting
The notion of ownership in Rust’s type system is closely connected to ownership
in separation logic (SL) [14]. Earlier work on the Prusti verifier [1] exploits this
correspondence to automatically extract memory safety proofs in SL from Rust
type and borrow information. This core proof contains all information to enable
framing, that is, proving that a given heap property is not affected by a heap
modification. As a result, user-specified functional annotations can be proved
easily by conjoining them to the assertions of the core proof. Prusti verifies the
combined program using the Viper verification framework [11].
    Our verification methodology for iterators leverages Rust’s ownership system
in two ways. First, ownership defines the heap fragment that an iterator and its
argument closures may access and modify, and prevents concurrent modifica-
tions. Second, we can focus on the essential functional properties of iterators
and rely on Rust’s type system for memory safety and framing, analogously to
Prusti. Nevertheless, we are confident that our methodology can be combined
with SL to handle languages without a built-in ownership system.

3      Methodology
In this section we introduce a general-purpose methodology for reasoning about
iterators. We describe a model of iterators (→ Sec. 3.1), introduce four pred-
icates that allow one to specify the behaviour of iterators (→ Sec. 3.2), and
present the proof obligations needed to verify that an iterator implementation
satisfies this specification (→ Sec. 3.3). We illustrate our methodology on two
examples (→ Sec. 3.4). Finally, we summarise how our methodology addresses
the challenges outlined in the introduction (→ Sec. 3.5).

3.1     Iteration model
An iterator can be queried repeatedly for values using a next method, producing
a sequence of values (v0 , v1 , . . . in the diagrams below). Calls to the next method
change the internal state of the iterator (I0 , I1 , . . . below).
         Compositional Reasoning for Side-effectful Iterators and Iterator Adapters                                       7

             Ik               Ik+1                        Ip           Ip+1                                    Ip+x
                  next                                         next            next     ...         next
Mk                                     Mk+1   Pk                                                                          Pk+1
                  vk                                           vp             vp+1            vp+x
            Fk                Fk+1
                      call                                        call               call     ...      call               mk
                                        mk
                                                          Fp                Fp+1                               Fp+x
                                                                      false            false               true
                  Map::next                                                 Filter::next


 Fig. 1. State diagrams for a call to Map::next (left) and a call to Filter::next (right).



                              I0              I1               I2
                                     next               next               next      ...
                                                   v0                 v1
                                                                                            ...

          The sequence of produced values can be finite or infinite. In the former case,
 next yields a designated value ⊥ to signal that the iteration has completed3 . We
 assume that once an iterator has completed, it will remain completed, which is
 the case in many programming languages. In Rust, this assumption corresponds
 to a so-called fused iterator (FusedIterator trait), and it is satisfied by the vast
 majority of Rust’s standard library iterators.
     Iterator adapters are iterators which use the results of a previous iterator to
 produce their values. For instance, the Map adapter applies a function f to the
 outputs v0 , v1 , . . . of the previous iterator to produce its result values m0 , m1 , . . . .
 The function f may itself be a closure with potentially mutable captured vari-
 ables, which means it has its own state (F0 , F1 , . . . ):

           I0                                 I1                                      I2
                  next                                  next                                      next        ...
                              v0                               v1
                                                                                                                    ...
          F0                                  F1                                      F2
                                     call                                  call                               ...
                                                   m0                                       m1


     The overall state of the Map adapter Mi comprises (and encapsulates) the
 state of the previous iterator Ii and that of its argument closure Fi . Map’s next
 method internally manipulates both state components as shown in Fig. 1 (left).
     Each call to Map’s next method triggers exactly one call to the predecessor’s
 next method. Other adapters have more complex behaviours. For instance, the
 Filter (Fig. 1 (right)) adapter calls its predecessor’s next method until the
 provided value satisfies the filter criterion determined by an argument closure
 (or the predecessor has completed) A specification and verification methodology
 for advanced iterators must be able to capture the evolution of such composite
 iterator states and the interactions between different iterators.
     3
         In Rust, this corresponds to an Option::None.
8       A. Bílá et al.

3.2   Specification components

Our methodology uses four specification components to specify the states of
and values returned by iterators. We introduce them here using a mathematical
notation and show a concrete syntax in Rust later, in Sec. 4.3.
    As in prior work [13], we associate each iterator with two ghost (specification-
only) functions to specify the values returned by the iterator. Function produced
yields the sequence of elements returned so far : produced(Ik ) = [v0 , v1 , . . . , vk−1 ].
Function completed yields true iff the iterator has completed. In other words, a
call to next with the initial state Ik returns ⊥ iff completed(Ik ) holds.
    The evolution of an iterator’s state across a single call to next is characterised
using the third component of our methodology: a two-state predicate step. For
a call to next with the initial iterator state Ik , the updated iterator state Ik+1
and the returned value vk , step(Ik ,Ik+1 ,vk ) must hold.
    To reason about the accumulated effects of an iterator, in general concerns
an unbounded number of next calls. This motivates our fourth key compo-
nent: we associate each iterator with a predicate leadsto that represents an
inductive, two-state invariant. This invariant relates the current iterator state
to any previous iterator state. It represents the reflexive, transitive closure
of the two-state postcondition step (which relates consecutive iterator states):
leadsto(Ik ,Il ) ⇔ (∀i · k ≤ i < l ⇒ step(Ii ,Ii+1 ,_)) for any 0 ≤ k ≤ l.

              Ik                Ik+1                           Il
      ...           next                   next    ...              next            ...
                                   vk
                                                         ...                  ...

             step(Ik ,Ik+1 ,vk )             leadsto(Ik+1 ,Il )


    When an iterator is used in a loop, we can naturally make use of leadsto in
the loop invariant: leadsto(I0 ,Ik ) must hold at every iteration, where I0 is the
state of the iterator before the loop, and Ik is the current state.


3.3   Proof obligations

To use our methodology, programmers need to define the four specification com-
ponents described in the previous subsection for each concrete iterator imple-
mentation. Our methodology then imposes the following proof obligations. First,
we check that leadsto includes the reflexive, transitive closure of step (see pre-
vious subsection). If this well-formedness check fails, the program is rejected.
Second, we check whether the definitions of the four components correctly re-
flect the behaviour of the iterator implementation. This can be done by verifying
that the implementation of the next method satisfies the following five postcon-
ditions. In these conditions, Ik , Ik+1 , and vk denote the prestate, poststate, and
result value of next, respectively. For simplicity we assume that the iterator has
no methods that modify its state, other than next.
   Compositional Reasoning for Side-effectful Iterators and Iterator Adapters      9

 – Q1 ≡ step(Ik ,Ik+1 ,vk ): step reflects the behaviour of a single call to next.
 – Q2 ≡ completed(Ik ) ⇔ vk = ⊥: completed reflects correctly whether the
   iterator returns a value.
 – Q3 ≡ completed(Ik ) ⇒ produced(Ik+1 ) = produced(Ik ): if the iterator has
   completed, the produced sequence is left unchanged.
 – Q4 ≡ ¬completed(Ik ) ⇒ produced(Ik+1 ) = produced(Ik )++[vk ]: if the iterator
   has not completed, the produced sequence is extended by the returned value.
 – Q5 ≡ completed(Ik ) ⇒ completed(Ik+1 ): iterator completion is monotonic.

    As usual, these postconditions may be assumed after each call to next, which
allows client code to reason about the results and effects of an iterator. We show
examples in the next subsection.


3.4   Examples

In this subsection, we show how to instantiate our specification components
for an iterator and an iterator adapter. In both examples, we assume that the
concrete iterator implementation maintains a ghost field p that contains the
elements produced so far; produced is then defined to simply return p. Proof
obligations Q3 and Q4 above ensure that the next method updates p correctly.
In the definitions below, we still use mathematical notation over named states
(as in our diagrams). We will define a suitable concrete specification syntax
in Sec. 4.


Counter iterator. A counter iterator that yields the numbers between 0 and
bound can be (partially) specified as follows. Here, ctr is the field of the iterator
that stores the next number to return.


   ∀0 ≤ k ≤ l ·       completed(Ck ) , Ck .ctr = Ck .bound
                   step(Ck ,Ck+1 ,vk ) , vk = Ck .ctr ∧ Ck .ctr + 1 = Ck+1 .ctr
                     leadsto(Ck ,Cl ) , Ck .ctr ≤ Cl .ctr

    The leadsto definition declares that the counter is monotonically increasing.
Thus, even across a statically unknown number of calls (e.g. across a loop),
we always know that the counter will not emit values lower than ones we have
previously observed.
    This specification omits various details about the returned values. To obtain a
more comprehensive specification, step and leadsto need to constrain produced,
for instance to express that produced[i] contains the value i. We omit the details
for simplicity, but our methodology can easily express them when desired.


Map iterator adapter. As explained, a Map iterator adapter produces a value
by calling a closure on the next value from the iterator it adapts. We specify
10       A. Bílá et al.

this as follows: (1) The Map iterator has completed iff the input iterator has
completed. (2) Each execution of next performs a step on the input iterator and
calls the map’s closure on the returned value. (3) The state of the Map iterator
evolves according to the specifications of the input iterator and the closure.
    The following definitions reflect this intuition. As before, Mi is the state of
the entire Map iterator, consisting of the state of the input iterator Ii and of the
closure Fi . Note that these states include the identities of those sub-objects; that
is, Fi includes the information of which closure to call, along with the values of
any captured variables. In the definition of step, we use a call description, which
has been proposed by Wolff et al. [16] to specify the invocation of closures.
(Fk , vk )    (Fk+1 , mk ) expresses that one call to the closure with state Fk is
made with argument vk , resulting in an updated closure state Fk+1 and return
value mk . The changes to the closure state are constrained by the closure’s
history invariant hist_inv, a two-state invariant relating any previous closure
state to any new closure state. We use this history invariant in the definition of
leadsto. We will describe call descriptions in more detail in Sec. 4.1.


      ∀0 ≤ k ≤ l ·         completed(Mk ) , completed(Ik )
                      step(Mk ,Mk+1 ,mk ) , ∃vk · step(Ik ,Ik+1 ,vk )∧
                                              ∧ (Fk , vk )   (Fk+1 , mk )
                          leadsto(Mk ,Ml ) , leadsto(Ik ,Il ) ∧ hist_inv(Fk ,Fl )

    A client that knows the concrete input iterator and closure can combine
this knowledge with this specification together with the postcondition of next to
determine the values returned by the Map iterator.


3.5     Challenges revisited

The introduction presented three main challenges for the specification and ver-
ification of advanced iterators. In this subsection we summarise how our novel
methodology addresses each of them.
    How to specify parameterised iterators modularly. We capture the result and
effects of a single call to next using the two-state step predicate. When the
iterator is parameterised with a closure (as in the Map example), we use the
call descriptions from earlier work [16] as a means of abstractly and generically
describing the results and effects of calls to the closure.
    We capture the accumulated results and effects of an iteration using the
produced sequence and the reflexive, transitive leadsto predicate. When the it-
erator state includes closures, we use two-state invariants on the closure state
(again following Wolff et al.) to express how they evolve during an iteration.
    Postconditions for the next method tie together these predicates with the
concrete implementation of the iterator. They allow clients to determine the
behaviour of a single call to next (using step) as well as of a full iteration
(using leadsto). In particular, clients, which are aware of the concrete argument
     Compositional Reasoning for Side-effectful Iterators and Iterator Adapters   11

closure passed to the iterator, can use these postconditions to determine both
the sequence of returned values and all relevant accumulated side-effects (e.g. on
closure-captured state).
    How to reason modularly about iterator chains. To handle iterator chains, the
specification of iterator adapters may refer to the step and leadsto predicates
of the previous iterator in the chain. This makes the specification of the adapter
parametric in the behaviour of the input iterator. Clients, which are aware of
the concrete iterator used as input to the adapter, know how to resolve this
parameterisation to obtain the concrete behaviour of the adapter. In particular,
neither the input iterator nor the adapter need to be re-verified when forming
an iterator chain.
    How to automate verification of modern iterator and adapter patterns? As
noted in Sec. 1, this challenge is addressed by encoding the methodology into
first-order logic components suitable for verification with SMT-based verifiers.
The four predicates defined above are encoded as uninterpreted functions, their
argument states are encoded using snapshots (explained in Sec. 4.2). A suitable
first-order encoding of call descriptions is provided in prior work [16].


4      Specifying individual iterators

In this section, we define a concrete Rust-like specification language for express-
ing the specifications required by our methodology (→ Sec. 4.1) and describe
the idea of a snapshot abstraction to express properties of the entire state of a
data structure (→ Sec. 4.2). We use the language to instantiate the methodology
introduced in Sec. 3 (→ Sec. 4.3), and finally illustrate the methodology on a
simple, unchained iterator (→ Sec. 4.4).


4.1     Specification language

Contracts are attached to methods using Rust attributes for each kind of speci-
fication, e.g. pre- and postconditions are annotated as follows:
 1    #[requires(a ==> b)]   // method precondition
 2    #[ensures(result > 0)] // method postcondition
 3    fn example(a: bool, b: bool) -> i32 { ... }

    The expressions in parentheses after the requires or ensures keyword are
side-effect-free Boolean Rust expressions, with a few (but powerful) extensions:

 – Implications, represented as antecedent ==> consequent.
 – Universal and existential quantifiers, represented as:
     • forall(|qvar_ident: QvarType| body_of_quantifier)
     • exists(|qvar_ident: QvarType| body_of_quantifier)
 – Mathematical types, particularly GhostSeq<T>, a generic type representing a
   sequence of instances of type T.
12        A. Bílá et al.

 – Logical equality, represented as lhs === rhs. This operation is distinct from
   the Rust equality lhs == rhs (note double equals in Rust) and represents a
   deep structural comparison, i.e. a comparison of all the memory reachable
   from each operand. Further discussion can be found in Sec. 4.2.
 – Call descriptions, represented as F      |args...| { pre } { post }. This ex-
   pression states that a call to the method F has happened, the assertion pre
   held in the prestate of that call, the assertion post held in the poststate, and
   the arguments of the call are bound to the names args... and the return
   value to a reserved name result in the assertions pre and post. The specific
   case of a closure call is a call to the method FnMut::call_mut, with the clo-
   sure state constrained using the pre- and poststate assertions. Similarly, the
   use of an iterator is a call to the method Iterator::next. This notation is
   based on prior work on closure verification [16].

    Ghost functions are functions used only from within specifications and are
also allowed to use the extended expression syntax:
 1    fn all_false(x: GhostSeq<bool>) -> bool {
 2        forall(|idx: usize| 0 <= idx && idx < x.len() ==> !x[idx])
 3    }



4.2     Abstract data structure states

Specifications in our methodology concern properties of the state of a data struc-
ture such as an iterator, a closure, or the values returned by an iterator. For
instance, produced needs to contain the values returned during an iteration.
Moreover, step and leadsto typically compare states of data structures, and
there are examples that need to quantify over the states of data structures, for
example, to express the effects of multiple closure calls. In all of these cases, the
meanings of our specifications need to refer to the entire current state of a data
structure in memory (such as an iterator), not just its identity.
    To enable such specifications, we introduce a canonical abstraction of each
data structure that captures its structure and values, but abstracts away concrete
addresses. We refer to the abstract value of a data structure as its snapshot.
Since data structures in (safe) Rust are always tree-shaped, a snapshot can be
represented easily as terms of a (mathematical) abstract data type. For instance,
the snapshot of a Point object (Sec. 2.1) is a mathematical tuple of two integers.
    It is common for separation logic specifications to relate the memory reach-
able from a given program expression to a user-defined abstract value using
(possibly recursive) predicate definitions [12]. Our snapshots are similar to these
abstract values, but the abstraction is derived automatically from the declara-
tions of types and fields.
    Snapshots allow our specifications to conveniently express properties of entire
states of data structures. For instance, logical equality (===) is simply a compari-
son of two snapshots. Similarly, function produced yields a snapshot that includes
the snapshots of all values returned by the iterator so far. Snapshots also allow
     Compositional Reasoning for Side-effectful Iterators and Iterator Adapters        13

cleanly integrating state-dependent properties with logical features such as quan-
tifiers and mathematical functions. For example, in Prusti [1], following Smans
et al. [15], ghost functions which operate on Rust data are transparently encoded
to mathematical functions which operate on snapshots. The same approach has
been applied to encoding quantifiers and call descriptions [16], as used in our
work (instead of quantifying over expressions in different states, one quantifies
over their snapshots as mathematical values).
     A (possibly surprising) consequence of the snapshot interpretation of our
specifications is that a ghost function can take parameters that represent multiple
versions of the same data structure, which is not directly possible in actual Rust
code. This allows us to encode two-state predicates such as step and leadsto
as standard ghost functions that take two snapshots as arguments, representing
the iterator state at different points in the program execution.
     Since snapshots are simply terms of a mathematical data type, they have
a straightforward encoding into SMT, which partly addresses the automation
challenge mentioned in the introduction. In fact, several automated program
verifiers employ similar notions of snapshots internally in their encodings, for
instance, Smallfoot [15], VeriFast [7], and Viper [11].


4.3      Defining the specification components

In Rust, iterators are types which implement the Iterator trait. This is achieved
with an explicit syntactic declaration (impl Iterator for SomeType) which also
declares the element type and provides the definition of one required method:
next. The implementation of this method can modify the current state of the
iterator and must output an Option which may contain the next element, or it
may be None to signal completion. The Iterator trait defines a large number of
other methods, such as map or filter; these all have default implementations,
which are inherited into any concrete iterator.
    Conceptually, we can represent the four key components of our iterator spec-
ifications (see Sec. 3.2) as ghost functions of the Iterator trait. Because we
provide no default implementations, every concrete iterator would then need to
provide definitions for these functions. Our implementation uses an alternative
approach that does not require any changes to functions declared in the Iterator
trait, see Sec. 6.
 1    trait Iterator {
 2        fn produced(&self) -> GhostSeq<Self::Item>;
 3        fn step(i_p: &Self, i_c: &Self, r: &Option<Self::Item>) -> bool;
 4        fn leadsto(i_p: &Self, i_c: &Self) -> bool;
 5        fn completed(&self) -> bool;
 6        // other Iterator methods
 7    }

    The produced method is a getter4 for a ghost sequence of values. The two-
state predicates step and leadsto takes references to two copies (a previous
4
     Traits in Rust cannot declare fields or properties, thus we must use a getter method.
14        A. Bílá et al.

version and a current version) of the iterator type. step additionally takes a
reference to the returned value, represented in Rust as an Option to allow for
None to signal the end of iteration. As noted in Sec. 4.2, it is possible to give
the two-state predicates step and leadsto different versions of the same instance
using snapshots. Finally, completed defines the stopping condition. Since these
methods are ghost code, we allow them to use non-executable constructs such
as quantifiers in their definitions in implementations of the Iterator trait.
    Finally, we express the proof obligations from Sec. 3 as postconditions of the
next method, which must be satisfied by each implementation of next. Here,
&result denotes a shared reference to the value returned by the method.
 1    trait Iterator {
 2     Q1 #[ensures(IteratorSpec::step(old(&self), &self, &result))]

 3     Q2 #[ensures(old(self.completed()) == (result === None))]

 4     Q3 #[ensures(old(self.completed()) ==> (

 5            self.produced() === old(self.produced())
 6        ))]
 7     Q4 #[ensures(!old(self.completed()) ==> (

 8               result === Some(self.produced().last())
 9            && self.produced().len() == old(self.produced().len()) + 1
10            && GhostSeq::prefix(old(self.produced()), self.produced())
11        ))]
12     Q5 #[ensures(old(self.completed()) ==> self.completed())]

13        fn next(&mut self) -> Option<Self::Item>;
14        // ...
15    }

    This specification uses logical equality ===, described in Sec. 4.1. Using ==
would require a PartialEq trait-bound on the iterator’s elements, restricting its
interface (not all iterators’ elements need have a Rust definition of equality).


4.4     Example

We illustrate our methodology by specifying a simple iterator returning a range
of consecutive numbers. In Rust, we can define such an iterator like this:
 1    struct Counter { A
 2        pos: i32,
 3        end: i32,
 4    }
 5    impl Counter {
 6        #[ensures(Iterator::leadsto(&result, &result))]
 7        fn new(end: i32) -> Self { ... } B
 8    }
 9    impl Iterator for Counter { C
10        type Item = i32; D
11        fn next(&mut self) -> Option<Self::Item> { E
12            if self.pos <= self.end {
13                self.pos += 1;
14                Some(self.pos - 1)
15            } else {
16                None
     Compositional Reasoning for Side-effectful Iterators and Iterator Adapters   15

17           }
18       }
19       // ...
20   }

    The code above first A defines a type which represents our iterator. Its state
contains two variables: its current position and its stopping point. B defines a
convenience constructor for the counter, which must ensure that the two-state
invariant leadsto is (reflexively) satisfied to begin with. C is the declaration
that marks Counter to be an iterator, consisting of a declaration of the type of
elements emitted by this iterator D , and an implementation of the next method
  E . The latter checks if the limit has been reached yet: if so, no more items are

emitted (as signalled by a None return value), otherwise the internal position is
updated and its old value is returned (wrapped in a Some to distinguish it from
the previous case).
    To specify this iterator, we provide definitions of the four ghost methods
declared in the Iterator trait, starting with completed:
 1       fn completed(&self) -> bool {
 2           !(self.pos <= self.end)
 3       }

    This definition is sufficient to show that a counter with a non-empty range
will return at least one value:
 1   let mut counter = Counter::new(2);
 2   assert!(counter.next().is_some());

   The two-state postcondition step defines how the state is updated. Here, i_p
and i_p refer to the iterator snapshot before and after the execution of next:
 1       fn step(i_p: &Self, i_c: &Self, r: &Option<Self::Item>) -> bool {
 2           !i_p.completed() ==> (
 3                  i_c.pos == i_p.pos + 1
 4               && *res === Some(i_p.pos) A
 5           )
 6           && i_p.end == i_c.end B
 7       }

     This definition is sufficient to prove assertions in a non-looping client:
 1   let mut counter = Counter::new(1);
 2   assert!(counter.next().unwrap() == 0);
 3   assert!(counter.next().unwrap() == 1);
 4   assert!(counter.next().is_none());

   Note that the conjunct A would follow from knowledge about the produced
sequence, and the conjuncts B are actually stating an invariant that is true
between any two states of the counter, not just consecutive ones. We can thus
simplify the definition of step and provide a definition of leadsto:
 1       fn step(i_p: &Self, i_c: &Self, r: &Option<Self::Item>) -> bool {
 2           !i_p.completed() ==> (i_c.pos == i_p.pos + 1)
 3       }
 4       fn leadsto(i_p: &Self, i_c: &Self) -> bool {
16        A. Bílá et al.

 5        C      i_p.end == i_c.end
 6        D   && i_p.pos <= i_c.pos
 7        E   && 0 <= i_c.pos && i_c.pos <= i_c.end + 1
 8        F   && i_c.produced().len() == i_c.pos as usize
 9        G   && forall(|x: i32| 0 <= x && x < i_c.pos ==>
10                i_c.produced()[x as usize] == x)
11       }

    In this definition, C end remains constant. D pos is monotonically increas-
ing, and E it remains within bounds. F the number of produced elements
is given by the difference between the current position and the lower bound.
Finally, G the value of every produced element can be defined by its position
in the sequence.
    The advantage of this more verbose definition is that Counter can be used
across unboundedly many calls, such as in a loop:
 1    let mut counter = Counter::new(90);
 2    let val_pre = counter.next().unwrap();
 3    assume!(n < 80);
 4    for i in 0..n {
 5        counter.next().unwrap();
 6    }
 7    assert!(counter.next().unwrap() > val_pre);

    At this point we have specified a simple iterator. We have used all four of
the methodology components we defined in Sec. 3. Although the approach is
relatively heavy for Counter (the definition of leadsto in particular), we will
shortly see it pays off when considering more advanced (and idiomatic) cases. A
similar specification can be used for iterating over a slice or Vec.


5      Specifying iterator chains
In this section, we gradually introduce our technical solutions to the second
challenge described in Sec. 1: modular reasoning about iterator chains. To intro-
duce iterator adapters in Rust, we specify a simple doubling iterator adapter (→
Sec. 5.1). Approaching the real Map type from the standard library, we specify an
adapter with side-effectful closures (→ Sec. 5.2). For the real Map specification,
we also need to account for transitive side effects, i.e. side effects of any nested
iterators (→ Sec. 5.3).

5.1     Simple iterator adapters
In Rust, iterator adapters are types which wrap an instance of the Iterator
trait while implementing the Iterator trait themselves. When the adapter’s next
method is invoked, it calls the previous iterator’s next method some number of
times, adapting its result. As an example, the Map adapter applies a closure to
every element produced by the previous iterator, while the Filter adapter uses
a closure as a logical predicate to decide whether each value from the previous
iterator should be returned or not.
     Compositional Reasoning for Side-effectful Iterators and Iterator Adapters    17

    The Rust standard library provides many such iterator adapters for a variety
of common use cases. The iterator chain in the code example shown in Sec. 1 is
actually composed of iterator adapters, albeit hidden behind some convenience
syntax (e.g. x.map(...) wraps the iterator x in a Map adapter).
    As stated before, our goal is to write single, generic specifications, that apply
regardless of the exact iterator that precedes the adapter in the chain or any
specific closure parameters. We first show that we can specify simple adapters
by characterising their produced sequence in terms of the produced sequence of
the previous iterator. For example, consider the following Double iterator adapter
which simply doubles the values coming from the previous iterator:
 1    struct Double<I A > {
 2        prev_iter: I, B
 3    }
 4    impl<I: Iterator<Item = i32>> Iterator for Double<I> {
 5        type Item = i32;
 6        fn next(&mut self) -> Option<Self::Item> {
 7            self.prev_iter.next().map(|v| v * 2) C
 8        }
 9    }

    This iterator adapter is able to adapt any iterator type that yields integers.
It thus has a type parameter A , which stands for the type of the previous
iterator. To be able to refer and mutate the previous iterator, the struct contains
(or owns) the previous iterator B . Finally, we implement the Iterator trait for
Double with a straightforward mapping5 of values C .
    We omit the straightforward definition of step. A possible (abridged) defini-
tion of leadsto and completed is:
 1    fn leadsto(i_p: &Self, i_c: &Self) -> bool {
 2     A     i_c.produced().len() == i_c.prev_iter.produced().len()
 3     B && forall(|idx: usize| idx < i_c.produced().len() ==>

 4            i_c.produced()[idx] == i_c.prev_iter.produced()[idx] * 2)
 5    }
 6    fn completed(&self) -> bool {
 7     C self.prev_iter.completed()

 8    }

    In the definition of leadsto, we A state that the length of the produced
sequence of the previous iterator and the adapter Double is the same, and we
  B  use a quantifier to relate each element. We also C re-use the previous
iterator’s stopping criterion. This definition is sufficient to verify properties of
the values produced when Double is used over an iterator (such as the previously
defined Counter):
 1    let counter = Counter::new(2);
 2    let mut double_iter = Double::new(counter);
 3    assert!(double_iter.next().unwrap() == 0);
 4    assert!(double_iter.next().unwrap() == 2);

5
     The map method on an Option type applies the given closure on the value contained
     in a Some, but leaves None intact.
18        A. Bílá et al.

 5    assert!(double_iter.next().unwrap() == 4);
 6    assert!(double_iter.next().is_none());

The contract of next implies that if a Some result is obtained, produced was
extended by one element. For each of the first three calls to next the verifier
thus learns about a new element of this sequence, the value of which is related
to the corresponding element of the previous iterator’s produced sequence. This
establishes a concrete relationship between the elements yielded by Counter and
those yielded by Double, sufficient to imply all asserted properties about these
resulting values.


5.2     Side-effectful closures in adapters

Although Double is indeed an iterator adapter, it is rather simple. The action it
performs is functionally a fixed one-to-one mapping of values. The Map iterator
adapter performs exactly this action, but let’s the user supply the function to
be applied. To this end, the Map type has two type parameters: one to represent
the previous iterator in the chain and one to represent the closure6 :
 1    struct Map<I, F> {
 2        prev_iter: I, // the wrapped iterator
 3        f: F,          // the closure parameter
 4    }

      When mapping values from the previous iterator, Map invokes the closure:
 1    fn next(&mut self) -> Option<Self::Item> {
 2        self.prev_iter.next().map(&mut self.f)
 3    }

    To provide a generic specification of Map, we must account for the side effects
of the closure call, even when the exact type of the closure is unknown; this
property of side effects on the closure’s mutable state cannot be captured using
the produced sequences alone. Instead, we use a call description to connect the
effect of an iteration step to the effects of a call to the closure itself:
 1    fn step(i_p: &Self, i_c: &Self, r: &Option<Self::Item>) -> bool {
 2     A !i_p.prev_iter.completed() ==>

 3         B FnMut::call_mut     |cl_self, arg|
 4             C {     i_p.f === cl_self
 5             D    && arg === i_c.prev_iter.produced().last() }
 6             E {     i_c.f === cl_self
 7             F    && r === Some(result) })
 8    }

For each step we know (if the previous iterator has not completed yet A ) that
 B there is a call to the closure, with C the original state of the closure stored

in field f of the original state of Map, and E the new state of the closure stored
in field f of the new state of Map. For the call, D the argument given to the
6
     The actual declaration has a third type parameter to represent the return type of
     the closure, omitted here for brevity.
     Compositional Reasoning for Side-effectful Iterators and Iterator Adapters          19

closure is the last element yielded by the previous iterator, and F the element
yielded by Map (r) is the result of the closure (Some(result)).
    This definition of step allows us to verify the side effects of individual calls
to next on the corresponding closure’s captured state:
 1    let counter = Counter::new(2);
 2    let mut sum = 0;
 3    let cl = #[ensures(sum == old(sum) + arg && result == arg * 2)]
 4        |arg| { sum += arg; arg * 2 };
 5    let mut map_iter = Map::new(counter, cl);
 6    assert!(map_iter.next().unwrap() == 0);
 7    assert!(map_iter.next().unwrap() == 2);
 8    assert!(sum == 1);

    The final assertion (after map_iter and cl expire) follows from the call de-
scription describing the call Map makes to the closure, which establishes the
postcondition of the concrete closure known concretely in this client code7 .

5.3      Multiple adapters
The Map specification in the previous subsection refers to the values produced by
the previous iterator, but does not account for changes to its state. To address
transitive side effects of next calls (i.e. those on closures earlier in the iterator
chain), we must directly capture information about the calls to the previous it-
erator. Our call description feature can also be used to describe this necessary
connection, this time relating each change to the current iterator to the corre-
sponding pre- and poststate of a call to next on the previous iterator, all the
while keeping the specification generic with respect to the previous iterator’s
type. The following definition of step exemplifies this powerful idiom, using two
nested call descriptions:
 1    fn step(i_p: &Self, i_c: &Self, map_res: &Option<Self::Item>) -> bool {
 2     A Iterator::next     |it_self|
 3         B { i_p.prev_iter === it_self }

 4         C { let prev_iter_res = result;

 5         D       i_c.prev_iter === it_self
 6         E    && (prev_iter_res.is_some() ==>
 7             F FnMut::call_mut     |cl_self, arg|
 8                {    i_p.f === cl_self
 9                  && Some(arg) === prev_iter_res }
10                {    i_c.f === cl_self
11                  && map_res === Some(result) } )
12         G    && prev_iter_res.is_none() ==> map_res.is_none() }
13    }

    In this version of step, we begin by A describing that a call to the previous
iterator will happen, where ( B ) the original state of the previous iterator is
stored in field prev_iter of the original state of the Map iterator, and D the
7
     We assume the closures themselves to be annotated with standard pre/postcondition
     specifications; for simple closures such as this one, the required specifications could
     be inferred by a static analysis, but this is orthogonal to our presented technique.
20       A. Bílá et al.

new state of the previous iterator is as stored in field prev_iter of the resulting
state of Map. To avoid confusion, we C used a let expression to name the
result of the previous iterator prev_iter_res ; the result returned from the Map is
map_res. E If the previous iterator returned an element, we F describe how
this relates a call to the closure, as before. G Otherwise, no element is returned
from the Map iterator either.
    The overall structure of this definition of step mirrors the Map model presented
in Fig. 1 (left): each call description corresponds to one box in the diagram, and
values from the previous iterator flow through the closure.
    With the richer specifications, we can prove facts about transitive side effects:
 1   let counter = Counter::new(2);
 2   let mut sum = 0;
 3   let cl_1 = #[ensures(sum == old(sum) + arg && result == arg + 1)]
 4       |arg| { sum += arg; arg * 2 };
 5   let map_iter_1 = Map::new(counter, cl_1);
 6   let cl_2 = #[ensures(result == arg * 2)] |arg| arg * 2;
 7   let mut map_iter_2 = Map::new(map_iter_1, cl_2);
 8   assert!(map_iter_2.next().unwrap() == 2);
 9   assert!(sum == 0);

    The final assertion requires that the knowledge about the effect of cl_1 on
its captured variable is propagated through the invocation of map_iter_1, which
happens inside map_iter_2. Note that the specification is the same for both Map
iterators, and that map_iter_2 in particular cannot even know that the previous
iterator in the chain is related to a closure.
    Finally, reasoning about unboundedly many iteration steps (e.g. when calling
next in a loop), simply requires us to suitably define leadsto for Map. To store the
intermediate states of the closures and the iterators, we add a ghost sequence
field st: GhostSeq<(F, I)> to Map, where every element is a tuple containing a
closure state and an iterator state.
 1   fn leadsto(i_p: &Self, i_c: &Self) -> bool {
 2          i_c.produced().len() == i_c.prev_iter.produced().len()
 3    A && i_p.st.is_prefix_of(i_c.st)

 4    B && i_c.st.len() == i_c.produced().len() + 1

 5    C && i_c.st.last() === (i_c.f, i_c.prev_iter)

 6       && forall(|idx: usize| idx < i_c.produced().len() ==>
 7        D I::next     |iter_self|
 8               {    i_c.st[idx].1 === iter_self }
 9               {    i_c.st[idx + 1].1 === iter_self
10                 && result === Some(i_c.prev_iter.produced()[idx])
11                 && FnMut::call_mut    |cl_self, arg|
12                        {    i_c.st[idx].0 === cl_self
13                          && arg === i_c.prev_iter.produced()[idx] }
14                        {    i_c.st[idx + 1].0 === cl_self
15                          && result === i_c.produced()[idx] }})
16   }

    In this definition of leadsto, we establish a connection between the ghost
sequence st and the concrete data stored in the Map struct. In particular, B
states there are as many intermediate states as there are yielded elements, plus
     Compositional Reasoning for Side-effectful Iterators and Iterator Adapters   21

one for the current state. C The last tuple in the st sequence corresponds to the
current data stored in Map. For each yielded element D we re-use our nested
call descriptions to establish the connection between consecutive intermediate
states. We also A state that the state sequence is expanded monotonically,
i.e. the intermediate states in any previous version of Map are a prefix of the
intermediate states of any newer version of Map.
     Equipped with such a specification, we can prove code which uses a Map
parameterised by a closure with captured state, applied to an unbounded number
of elements, such as this vector summation:
 1    #[ensures(result == GhostSeq::of_vec(&vec).sum())]
 2    fn sum_vec(vec: Vec<i32>) -> i32 {
 3        let vec_vals = GhostSeq::of_vec(&vec);
 4        // ghost state of closure
 5        let mut pos = 0usize;
 6        let mut sum = 0;
 7
 8         // summation closure
 9         let cl = #[requires(pos < vec_vals.len() && x == vec_vals[pos])]
10                  #[ensures(pos == old(pos) + 1 && ret == sum)]
11                  #[invariant(   0 <= pos && pos <= vec_vals.len()
12                              && sum == vec_vals[0..pos].sum())]
13                  |x| { sum += x; pos += 1; sum };
14
15         // iterate values of vector
16         let mut map_iter = vec.into_iter().map(cl);
17         #[invariant(pos == map.prev_iter.pos)]
18         for el in map_iter {}
19
20         sum
21    }

   In this example, leadsto is maintained for map_iter throughout the loop,
which also implies the closure history invariant. Once the loop exits, it is known
that the position of the vector iterator reached the end of the vector, and so
sum == vec_vals[0..pos].sum() collapses to sum == vec_vals.sum().


6         Out-of-band contracts
So far, we assumed that Rust traits, including those from the standard library,
can be extended with additional methods. To avoid such changes to existing code,
Spec# proposed out-of-band contracts as a mechanism to attach specifications
to libraries. In this section, we present a refined notion of out-of-band contracts
that allow one to attach contracts conditionally, depending on whether a type
implements a trait.

6.1       Specification extension traits
Instead of changing Rust’s Iterator trait, we declare the four (specification-only)
methods of our methodology in a new trait:
22        A. Bílá et al.

 1    trait IteratorSpec : Iterator { A
 2        fn produced(&self) -> GhostSeq<Self::Item B >;
 3        fn leadsto(i_p: &Self, i_c: &Self) -> bool;
 4        fn step(i_p: &Self, i_c: &Self,
 5            r: &Option<Self::Item C >) -> bool;
 6        fn completed(&self) -> bool;
 7    }

    In the above, we A declare IteratorSpec and use Iterator as its super-trait.
This means that any type that implements IteratorSpec must also implement
Iterator. Apart from declaring the same methods we have already seen be-
fore, one notable feature is B , C re-using the associated type Item from the
Iterator supertrait, such that the implementation of IteratorSpec does not need
to repeat the element type that is already declared in Iterator.
    Declaring methodology components in traits should be familiar to Rust pro-
grammers because they represent a shared behaviour. Like regular traits, any
given implementation of IteratorSpec can define these methods to specify con-
crete iterators.
    In our implementation, the method declarations in IteratorSpec are addition-
ally annotated with either #[predicate] or #[pure]. Both annotations indicate
that the given method is usable in specifications, and #[predicate] additionally
allows the use of non-executable features such as quantifiers.


6.2     Type-dependent contracts

The specification extension trait IteratorSpec allows us to remove the four func-
tion declarations from the Iterator trait, but does not provide a way to express
the postconditions of the next method (Rust does not allow a sub-trait to override
methods of a super-trait). To provide a specification for next without changing
the Iterator trait, we use an out-of-band contract for the trait, that is, a speci-
fication provided in a separate file. For example, we could (erroneously) specify
Iterator::next to always return a result:
 1    #[extern_spec] // out-of-band contract
 2    trait Iterator {
 3        #[ensures(result.is_some())]
 4        fn next(&mut self) -> Option<Self::Item>;
 5    }

   However, such an extern spec for Iterator cannot use the methods from
IteratorSpec , because not every implementation of Iterator also implements
IteratorSpec . To solve this issue, we introduce type-dependent contracts, that
is, contracts that apply only to implementations of a given trait. The following
extern spec for Iterator uses this feature to impose postconditions on next only
for implementations that also implement IteratorSpec:
 1    #[extern_spec]
 2    trait Iterator { A
 3        #[type_dependent(Self: IteratorSpec, [ B
 4         Q1 ensures(IteratorSpec::step(old(&self), &self, &result)),
     Compositional Reasoning for Side-effectful Iterators and Iterator Adapters   23

 5         Q2   ensures(old(self.completed() == (result === None))),
 6         Q3   ensures(old(self.completed()) ==> (
 7                  self.produced() === old(self.produced())
 8              )),
 9         Q4   ensures(!old(self.completed()) ==> (
10                     result === Some(self.produced().last())
11                  && self.produced().len() == old(self.produced().len()) + 1
12                  && GhostSeq::prefix(old(self.produced()), self.produced())
13              )),
14         Q5   ensures(old(self.completed()) ==> self.completed()),
15        ])]
16        fn next(&mut self) -> Option<Self::Item>;
17   }

     As before,      A  an extern spec is added to the Iterator trait. The B
type_dependent attribute introduces postconditions Q1 - Q5 only for implemen-
tations that also implement IteratorSpec . As a result, it is allowed to refer to
methods of IteratorSpec , e.g. to call self.completed().
     Note that the type-dependent contract is defined on the type being extended,
i.e. it is part of the specification of Iterator::next, not part of the specification
extension trait IteratorSpec . This decision is motivated by Rust’s coherence
rules.
     To ensure that our type-dependent contracts are sound, we require that any
type-dependent contract refines its base contract. This consists of the usual be-
havioural subtyping checks: the precondition must be weakened and the post-
condition must be strengthened.



7        Soundness

Our methodology builds on standard techniques to reason about method imple-
mentations and calls, and on call descriptions to reason about closure calls [16].
Consequently, its soundness relies on a sound verification technique for these
features. Such techniques support two-state postconditions such as our step
predicate (typically expressed via logical variables or old-expressions), which
are checked for each method implementation and assumed for each call.
    The only non-standard component of our methodology is the leadsto predi-
cate, which may be assumed between any two iterator states occurring during an
iteration. If next is the only method mutating the iterator state, this assumption
is justified by the fact that each call to next satisfies step, and leadsto includes
the reflexive, transitive closure of step. Consequently, leadsto holds between two
iterator states, no matter how many calls to next occur between those states.
    If the iterator state may be modified by methods other than next, one can
interpret leadsto as a standard two-state invariant on the iterator type. Such
an invariant must be maintained by all mutating methods, such that the above
inductive argument applies.
24      A. Bílá et al.


     Test (implementation) LoS LoC VT (s)       Test (client code) LoS LoC VT (s)
     counter                 32 30     9.53     counter           0 14        11.53
     double                  43 25     9.95     double            1   6       10.16
     filter.vpr             90* 109* 18.24*     filter.vpr      10* 27*       5.68*
     map                     67 38 42.12        map              14 22        79.78
     option_intoiter         36 19     7.41     option_intoiter   0   4        6.96
     vec_intoiter            42 13     7.05     vec_intoiter      4 19        16.48
     zip                     79 32 84.46        zip               2   6       67.12

Table 1. Evaluation. LoS and LoC represent the line of specifications and lines of code,
respectively. VT represents the verification time, measured as the wall-clock runtime
averaged over 7 runs using an Intel Core i9-10885H 2.40GHz CPU with 16 GiB of
RAM, excluding the slowest and fastest runs. Test cases ending in .vpr were encoded
manually into Viper: our methodology supports these test cases, but issues in the
underlying Prusti tool (independent from the contributions of this paper) currently
prevent our implementation from supporting the analogous examples in Rust. These
Viper encoded examples are more verbose and run through a simpler tool chain; for
these reasons we mark the data with *s in the tables here.



8    Evaluation

We implemented our technique as a prototype extension to the Prusti verifier [1].
Following the design laid out in Sec. 4.1, our iterator methodology is implemented
primarily in user-facing Rust code (which can be packaged into a standard library
of specifications) and not as an ad hoc feature of Prusti.
    To enable annotating key standard library types, we added support for declar-
ing external specifications for trait types as well as for our novel type-dependent
contracts. Most other extensions were routine; this suggests that layering our
methodology onto existing tools is fairly lightweight. Due to this lightweight in-
tegration, we don’t treat leadsto as a built-in type invariant, but rather as a
postcondition on next; intended properties such as transitivity are therefore not
checked by default (but proofs relying on them would of course fail otherwise).
    We evaluated our work on a number of challenging test cases, modelling var-
ious combinations of idiomatic iterators found in the Rust standard library, as
well as custom iterator implementations discussed in this paper. The results of
our evaluation are shown in Table 1 (in terms of lines of specification, code and
verification times). Generally, the specification overhead is heavier (roughly one-
to-one with code) for the generic library functions such as Map, but these specifi-
cations need only be written once. Importantly, for client code using these itera-
tors, the specification overhead is typically lighter. A substantial body (roughly
340 LoC) of common specifications were also necessary as our implementation
neither builds in pre-defined support for common types such as Option, or our
new GhostSeq type. These specifications need only be written once can could in
principle be added as a “standard library” of specifications. We consider the ver-
ification times using our prototype implementation to be generally reasonable,
    Compositional Reasoning for Side-effectful Iterators and Iterator Adapters            25

but with some expensive outliers; we suspect that these require some additional
effort to control quantifier instantiation in the underlying solver [2].


9     Related work

The two works most closely related to this paper (Pereira et al. [13] and Wolff
et al. [16]) were already discussed in detail in Sec. 1.
    One of the first formulations of the challenges of specifying and verifying
iterators appeared in the 2006 SAVCBS workshop [5] (although the problem
has been studied for longer), which posed the research question in the context
of Java/C# collections and iterators over such collections. Various papers were
submitted as solutions to the challenge: Jacobs [6] focuses on C# iterators, which
are suspendable functions that can “yield” values to a consumer. The iteration it-
self is characterised by invariants over the sequence of produced values, similarly
to Pereira [13]. C# iterators are analogous to Rust generators (or “coroutines”)
which can be turned into an Iterator instance8 . Although Prusti does not yet
support Rust generators, our methodology should apply to this case as well: the
state of an iterator would become the state of the generator and the leadsto
two-state type invariant would be maintained over the generator.
    Krishnaswami [9] proposed specifications for Java-like iterators in a higher-
order separation logic. The application of separation logic facilitates proofs of
memory safety, and prevents concurrent modifications of a collection while an
iterator over it exists. However, functional specifications are left as abstract
higher-order predicates, which are problematic for automation.
    Creusot [3] is another Rust verifier. Its prophetic approach to encoding Rust
references simplifies the specification of some reborrowing patterns, which means
the signature of traits such as IterMut are supported, unlike in Prusti at the time
of writing. Creusot’s public tests include functional specifications based on the
Pereira methodology (both tools are based on Why3). If the contributions of this
paper were adapted to Creusot, we believe it would be possible to specify richer
properties of side-effectful iterator chains in this tool as well, as enabled by our
novel methodology. More generally, our technique is largely agnostic as to the
underlying verifier and its handling of e.g. the program memory, provided that
our snapshot interpretation of specifications can be appropriately supported.


10      Conclusion

We have presented a novel methodology for modularly specifying and verifying
the complex iterator patterns found in modern programming languages. This
methodology is designed to be compatible with basic techniques for reasoning
8
    Since generators and asynchronous code in Rust is still unstable in general, such
    adaptation is not yet part of the standard library. It is possible with relatively little
    boilerplate code, see https://stackoverflow.com/questions/16421033.
26     A. Bílá et al.

about side-effectful programs, such as Rust’s ownership system and formal tech-
niques such as separation logic; the underlying technical requirements are com-
monly found in many deductive verifiers. We have evaluated our methodology
in Rust, which has rich iterator support in its standard library, as well as a
type system which can be used to automatically take care of these ownership
requirements. Applying our methodology in languages without such a type sys-
tem would require specifications to govern side-effects, but the adaptation of our
novel methodology would nonetheless be straightforward.
    To ensure our methodology is usable in real-world codebases and integrates
well with other verification efforts, we have prioritised modularity in our exten-
sion to the state-of-the-art Rust verifier Prusti. To this end, we have introduced
novel type-dependent contracts, which, combined with specification extension
traits, allow specifying standard-library iterators without modifying the source
code of the standard library itself.
   Compositional Reasoning for Side-effectful Iterators and Iterator Adapters        27

References
 1. Astrauskas, V., Müller, P., Poli, F., Summers, A.J.: Leveraging Rust types for
    modular specification and verification. Proc. ACM Program. Lang. 3(OOPSLA),
    147:1–147:30 (2019). https://doi.org/10.1145/3360573
 2. Becker, N., Müller, P., Summers, A.J.: The axiom profiler: Understanding and
    debugging SMT quantifier instantiations. In: Tools and Algorithms for the Con-
    struction and Analysis of Systems (TACAS). pp. 99–116. LNCS, Springer (2019)
 3. Denis, X., Jourdan, J.H., Marché, C.: Creusot: a Foundry for the Deduc-
    tive Verication of Rust Programs. In: International Conference on Formal En-
    gineering Methods (ICFEM). LNCS, Springer Verlag, Madrid, Spain (2022),
    https://hal.inria.fr/hal-03737878
 4. Filliâtre, J.C., Paskevich, A.: Why3–where programs meet provers. In: European
    Symposium on Programming (ESOP). pp. 125–128. Springer (2013)
 5. Jacobs, B., Cok, D., Weide, B., Bierhoff, K., Krishnaswami, N., et al.: Proceed-
    ings of the 2006 Conference on Specification and Verification of Component-based
    Systems (SAVCBS). ACM Digital Library (2006)
 6. Jacobs, B., Piessens, F., Schulte, W.: VC generation for functional be-
    havior and non-interference of iterators. In: Specification and Verifica-
    tion of Component-based Systems (SAVCBS). p. 67. ACM Press (2006).
    https://doi.org/10.1145/1181195.1181209
 7. Jacobs, B., Smans, J., Philippaerts, P., Vogels, F., Penninckx, W., Piessens, F.:
    Verifast: A powerful, sound, predictable, fast verifier for C and Java. In: NASA
    Formal Methods Symposium. pp. 41–55. Springer (2011)
 8. Klabnik, S., Nichols, C., contributors: The Rust Programming Language. Rust
    Community (2018), https://doc.rust-lang.org/stable/book/
 9. Krishnaswami, N.R.: Reasoning about iterators with separation logic. In: Specifi-
    cation and Verification of Component-based Systems (SAVCBS). p. 83. ACM Press
    (2006). https://doi.org/10.1145/1181195.1181213
10. Matsakis, N.D., Klock, F.S.: The Rust language. ACM SIGAda Ada Letters 34(3),
    103–104 (Nov 2014). https://doi.org/10.1145/2692956.2663188
11. Müller, P., Schwerhoff, M., Summers, A.J.: Viper: A verification infrastructure for
    permission-based reasoning. In: Verification, Model checking, and Abstract inter-
    pretation (VMCAI). pp. 41–62. Springer (2016)
12. Parkinson, M.J., Bierman, G.M.: Separation logic and abstraction. In: Palsberg,
    J., Abadi, M. (eds.) Principles of Programming Languages (POPL). pp. 247–258.
    ACM (2005)
13. Parreira Pereira, M.J.: Tools and Techniques for the Verification of
    Modular Stateful Code. Theses, Université Paris Saclay (Dec 2018),
    https://tel.archives-ouvertes.fr/tel-01980343
14. Reynolds, J.C.: Separation logic: A logic for shared mutable data structures. In:
    Logic in Computer Science (LICS). pp. 55–74. IEEE (2002)
15. Smans, J., Jacobs, B., Piessens, F.: Heap-dependent expressions in separation logic.
    In: Formal Techniques for Distributed Systems, pp. 170–185. Springer (2010)
16. Wolff, F., Bílý, A., Matheja, C., Müller, P., Summers, A.J.: Modular specification
    and verification of closures in Rust. Proceedings of the ACM on Programming
    Languages 5(OOPSLA), 1–29 (Oct 2021). https://doi.org/10.1145/3485522
