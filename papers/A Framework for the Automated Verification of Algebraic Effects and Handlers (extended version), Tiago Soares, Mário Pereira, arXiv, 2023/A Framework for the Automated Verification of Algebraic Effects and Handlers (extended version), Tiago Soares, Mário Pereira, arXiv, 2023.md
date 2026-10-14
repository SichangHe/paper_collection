                                            A Framework for the Automated Verification of
                                                   Algebraic Effects and Handlers
                                                        (extended version)?

                                                                 Tiago Soares and Mário Pereira

                                                  NOVA LINCS, Nova School of Science and Technology, Portugal
arXiv:2302.01265v3 [cs.LO] 7 Feb 2023




                                               Abstract. Algebraic effects and handlers are a powerful abstraction to
                                               build non-local control-flow mechanisms such as resumable exceptions,
                                               lightweight threads, co-routines, generators, and asynchronous I/O. All
                                               of such features have very evolved semantics, hence they pose very in-
                                               teresting challenges to deductive verification techniques. In fact, there
                                               are very few proposed techniques to deductively verify programs fea-
                                               turing these constructs, even fewer when it comes to automated proofs.
                                               In this paper, we present an extension to Cameleer, a deductive verifi-
                                               cation tool for OCaml code, that allows one to reason about algebraic
                                               effects and handlers. The proposed embeds the behavior of effects and
                                               handlers using exceptions and employs defunctionalization to deal with
                                               continuations exposed by effect handlers.

                                               Keywords: OCaml· Algebraic Effects · Automated Proofs · Deductive
                                               Verification · Cameleer· GOSPEL


                                        1     Introduction

                                        The newest release of the OCaml compiler saw the introduction of a variety of
                                        new features that make parallel and concurrent code more efficient as well as
                                        easier to write. These include, amongst other, algebraic effects and handlers [22].
                                        In short, algebraic effects are similar to exceptions: when an effect is performed,
                                        execution is halted and control is surrendered to the nearest enclosing handler.
                                        The main difference between exception and effect handlers is that the latter
                                        exposes a (delimited) continuation function that allows us to go back to the
                                        point in which the effect was performed and resume execution.
                                            This addition to an industrial strength language means there is a large in-
                                        centive for verification tools to add support for algebraic effects and handlers.
                                        Although some research has been done [5, 16] that presents reasoning rules for
                                        this kind of program, none of them explore automated proofs. Therefore, the
                                        research question we pose to ourselves is what tools and methodologies must
                                        ?
                                            This work is partly supported by the HORIZON 2020 Cameleer project
                                            (Marie Skłodowska-Curie grant agreement ID:897873) and NOVA LINCS (Ref.
                                            UIDB/04516/2020)
be developed in order to apply automated deductive proofs to OCaml programs,
featuring effects and handlers?
    To answer this question, we present a framework that can automatically ver-
ify programs that employ algebraic effects. Such a framework is implemented
as an extension to Cameleer [15], a deductive verification tool for OCaml code
whose specification is written in GOSPEL [3] (Generic OCaml SPEcification
Language) and then translated to WhyML, the specification and programming
language of the Why3 verification framework [2]. Cameleer is also the only au-
tomated deductive verification platform (we are aware of) that targets OCaml
programs, making it an ideal choice for this project.
    To achieve this goal we must be able to represent the continuation function
exposed by the handler in our proofs, which we will do using a translation of
algebraic effects into Why3 that employs defunctionalization [21], a program
transformation technique that turns higher-order programs into first-order ones.
To the best of our knowledge, the use of defunctionalization in a proof scenario
is novel.
    The contributions of this work can be summarized as follows:

1. we extend GOSPEL to accommodate the needed logical elements to specify
   the behavior of algebraic effects and handlers;
2. we develop an embedding of OCaml handlers and effects in WhyML, em-
   ploying defunctionalization;
3. we extend Cameleer to automatically translate GOSPEL annotated OCaml
   programs into this embedding, allowing us to conduct deductive verification
   inside the Why3 framework; and
4. we build a set of case studies verified using our proposed methodology.

Notation. OCaml and GOSPEL share many syntactic traits with WhyML. Since
we show examples using these three languages throughout the paper, we put a
label on the right-hand side of every listing to indicate the language in which
such piece of code is written.


2    Algebraic Effects in a Nutshell

Before presenting how we plan to specify and prove algebraic effects, let us
present a program that simulates a mutable reference, without actually using
mutable state. For such purpose, we introduce the following two distinct algebraic
effects:
    effect Get : int                                                      OCaml
    effect Set : int -> unit
The role of Get and Set effects is to implement, respectively, the usual derefer-
encing and assignment operations.
   One can read the above definitions as follows: when the Get effect is per-
formed, the nearest enclosing handler calls the corresponding continuation by


                                        2
passing as argument an int value, which stands for the current value of the ref-
erence. Conversely, the Set effect sends an int, the new value of the reference,
to the handler. The handler will simply return unit. This means any future Get
effect shall retrieve this same value.
    Using these effects, we define the following function that increments the value
of the reference by one:
    let inc () : unit =                                                    OCaml
      let current = perform Get in
      perform (Set (1 + current))
To call this function, we must define a handler that enforces the intended be-
havior. Abiding to our rule of not using mutable state, we create the following
anonymous functions to represent the program state:
    let create_env () : int -> int = match inc () with                     OCaml
      | r ->                fun _ -> r
      | effect Get k ->     fun x -> (continue k x) x
      | effect (Set n) k -> fun _ -> (continue k ()) n
Here, create_env returns another function which receives the initial value of the
reference and handles each effect accordingly. In case no effect is performed, the
handler falls into the first branch and it builds a function that always returns
the result r.
    When the Get effect is handled we return a function that calls the contin-
uation Why3k with the argument x, that is, the current value of the reference.
Important to note that when we call the continuation with the continue func-
tion, the handler remains installed, meaning it handles any remaining effects.
Such kind of handlers is know as deep handlers, whereas shallow handlers can
only handle at most one effect [7]. This also means that calling the continuation
returns another function, seeing as it is the return type of the handler. After the
call to continue, we resume the computation back to the point where the effect
is performed, inside the inc function. As such, the Set effect is performed (and
handled by the next branch of the same handler). This means continue returns
a function, which we apply to x to ensure the value of the reference remains
unchanged.
    When the Set effect is handled, it returns a function that calls the continu-
ation, which once again returns a new function. In turn, this function is applied
to n, the value sent through the effect.
    The use of Get and Set effects resemble the use of the state monad, for
instance, in the Haskell language1 . Indeed, algebraic effects have many similari-
ties with monads, in the sense that both constructions provide abstraction over
effectful computations. The upside of using effects is that performing effects is
done in direct style, much like calling a function. Whereas with monads, one
would need to encapsulate every operation inside the monad type. Moreover,
effects provide a clear abstraction barrier between the action of performing an
effect and its actual implementation [10].
1
    https://wiki.haskell.org/State_Monad


                                        3
3     Specifying and Reasoning About Effects and Handlers

Proving the correctness of an handler leads to some specification and reasoning
challenges, the greatest of which begin proving that every call to continue is
sound. For the example of the previous Section, this would mean proving that
for every Get effect the handler replies with the correct value. To do this, we
must define some logical contract that the handler must respect when calling
the continuation. Additionally, the function that performs the effect, must also
respect a set of requirements to be able to perform an effect.
    Throughout this paper, we refer to any function that calls continue as the
Server, whereas any function calling perform is designated the Client. The
rules that these two agents must ensure when performing or responding to an
effect is described by protocols [5]. Protocols consist of preconditions (the condi-
tions Client must respect when performing an effect), postconditions (the con-
ditions that Server must respect when calling the continuation) and a modifies
clause with all the variables Server is given write permissions to.


3.1   Client Specification

To present how we implemented protocols in Cameleer, we use a simple example:
we create a program where Client sends some value to Server. The Server then
takes that value and sets a global reference p to that value and returns p’s old
value. To do this, we first define the reference as well as an effect, XCHG, that
receives an integer value and returns another one. We then create a protocol
with the rules we outlined, as follows:
    let p : int ref = ref 0                                      GOSPEL + OCaml
    effect XCHG : int -> int

    (*@ protocol XCHG x :
        ensures !p = x && reply = old !p
        modifies p *)
Here, we define a GOSPEL protocol which ensures that, when Server returns
control to Client, the reference holds x, the value passed by Client, and Server
replies with p’s old value (hence, the use of the keyword reply). Additionally,
we also state that Server is allowed to modify the contents of p. This protocol
has no precondition since there is no restriction over what values Client may
send. Every protocol is named after an effect, meaning it establishes the rules
the two agents must obey when using such an effect to communicate.
    Let us now move on to specifying a Client that uses this effect. This amounts
to the following:
    let xchg (n : int) : int =                                   GOSPEL + OCaml
      perform (XCHG n)
    (*@ ensures !p = n && result = old !p
        performs XCHG *)

                                         4
The performs clause lists the effects a certain function might perform. The
postcondition of the xchg function is exactly the postcondition of the protocol,
since it simply calls perform with effect XCHG.

3.2   Server Specification
Consider the following simple OCaml handler for the XCHG effect:
    let server () =                                              GOSPEL + OCaml
      try xchg (xchg 42) with
      | effect (XCHG n) k ->
          let old_p = !p in
          p := n;
          continue k old_p
It is easy, at least informally, to observe that this handler respects the protocol
defined previously. However, in the general case, this can only be established if we
specify a condition whether the function exits through an exceptional branch or
it ends normally. We refer to this piece of specification as the handler invariant,
inspired from the fact we are dealing here with deep handlers, which provide a
form of recursive treatment of effects. For the XGHG Server, we provide the
following specification:
    try xchg (xchg 42) with ...                                  GOSPEL + OCaml
    (*@ try_ensures !p = old !p && result = 42
        returns int *)
The said invariant is provided via try_ensures, a new clause we have intro-
duced in GOSPEL for the purpose of reasoning about handlers. For the above
example, whenever the execution reaches the exceptional branch, we know the
final instruction of the handler is a call to continue. Since the handler remains
installed (again, due to it being a deep-handler), it keeps calling continue until
no more effects are performed. In practice, this means the two effects produced
by the double call to xchg are treated in this handler. After the second call
to continue, function server halts its execution normally, hence the handler
specification allows one to derive this function returns 42 and the value stored
in p is unchanged (even if this reference is written twice). Finally, the returns
keyword specifies the return type of this function...

4     Translation of Effects and Handlers into WhyML
Having presented our protocol-based approach to specify effects and handlers,
we focus now on exploiting such specification for the purpose of deductive verifi-
cation. We present in this Section a translation scheme from GOSPEL-annotated
OCaml programs, with effects and handlers, into a WhyML program. Hence, the
verification conditions generated by Why3 must ensure the original OCaml pro-
gram adheres to its specification. This mainly amounts to prove that Client and
Server respect the established protocols. To guide our presentation, we re-use
the xchg example from Sec. 3.


                                         5
4.1   Reasoning about Client

Each request Client makes, via an effect, must respect the corresponding pro-
tocol’s precondition and that Client’s postcondition holds for any reply Server
may send. In order to prove such properties, our translation pipeline introduces
the following function, which simulates performing an XCHG effect:
val perform_XCHG (x : int) : int                                             WhyML
  ensures { let reply = result in
            reply = old !p && !p = x }
  writes { p }

The specification of perform_XCHG is exactly that of the XCHG protocol. Using
this function, the Client is straightforwardly translated into WhyML, as follows:
  let xchg (n : int) : int                                                   WhyML
    ensures { !p = n && result = old !p }
  = perform_XCHG n

By using the perform_XCHG function, we can check if the request made sat-
isfies the protocol’s precondition and if the function’s postcondition holds for
any possible reply. The former is proved trivially: seeing as there is no pre-
condition, Client can always make a request. As for the latter, the protocols
imposes Server can only reply after setting the p reference to the value sent by
Client and can only return the reference’s old value. This is exactly what we
put in perform_XCHG postcondition, hence the body of xchg also adheres to its
specification.


4.2   Reasoning about Server

Using our translation approach, proving a Client is no different than proving
functions that call other functions. Proving Server, on the other hand, poses
some interesting challenges:

 – How does one translate OCaml’s effects into WhyML?
 – The Why3 xchg function does not have any kind of exceptional return, it
   merely calls a function that simulates the handler’s behavior. How do we
   embed this in Why3?
 – How does one represent continuations, as well as OCaml’s continue function,
   in Why3?
 – What kind of specification should such continuations present?

To tackle the first issue, we simply choose to represent effects as WhyML excep-
tions. More specifically, we create an exception that receives the same arguments
as the original effect. In the case of XCHG, it receives a single int value, resulting
in the following encoding:
  exception XCHG int                                                         WhyML


                                          6
Using such representation for effects, OCaml effect handlers are translated into
WhyML using exception handlers. The handler from Sec. 3.2 is translated as
follows:
  try xchg (xchg 42) with                                                WhyML
  | XCHG n ->
      let old_p = !p in
      p := n;
      continue k old_p
To make this handler effective, the xchg function must be able to, indeed, throw
an exception. Our translation scheme adds the following raises clause to the
perform_XCHG function:
  raises { XCHG }                                                        WhyML

In practice, we translate every performs clause from GOSPEL specification into
a WhyML raises clause, meaning that xchg will have this same clause.


4.3   Representing Continuations

The attentive reader might notice that the continuation k is absent from the
WhyML translation of handlers. Indeed, representing and dealing with continu-
ations in Why3 is a challenge, since the framework has very limited support for
higher-order computation.
    Continuations are, in essence, functions that can only be called using the
special continue function. Moreover, they can only be called once (if the same
continuation is called multiple times, the OCaml runtime would throw an ex-
ception). We encode continuations in WhyML encoding via the following record
type:
  type continuation ’a ’b = abstract {                                   WhyML
    mutable _valid : bool;
  }
This declaration introduces a polymorphic type of continuations, with argument
of type ’a and result of type ’b. The Boolean field _valid is used to check
whether the continuation was continued, ensuring the one-shot behavior. From
a programming perspective, type continuation behaves as an abstract data
type. One can only explore the value of _valid within specification or ghost
code.
    To use continuations as a value equipped with some logical contract, we adopt
a technique [11, 20] that allows us to represent and manipulate the specification
of continuations. This is done through the following pair of predicates:
  type state                                                             WhyML

  predicate pre (continuation ’a ’b) ’a state
  predicate post (continuation ’a ’b) ’a state state ’b


                                       7
These predicates are not given a particular definition, but are axiomatized later,
as needed. The pre predicate holds if the continuation’s precondition holds.
This predicate is applied to the continuation’s argument and a representation
of the state in which the continuation begins execution. On the other hand,
post predicate holds if the continuation’s postcondition holds. This predicate
is applied to the continuation’s argument, the initial state, the state after the
continuation executed, and finally the value returned by the continuation. The
state type is instantiated with the piece of mutable state that a particular
program manipulates. For instance, for the xchg example, state would be refined
as record type with a single mutable field _p, which represents the value stored
in reference p.
    Using this approach, we define the continue function in Why3, as follows:
  val continue (k : continuation ’a ’b) (arg : ’a) : ’b    WhyML
    requires { k._valid }
    requires { pre k arg {_p = !p} }
    ensures { post k arg (old {_p = !p}) {_p = !p} result }
    writes   { k._valid, p }
When this function is called, it will respect the contract of continuation k. Ad-
ditionally, it requires the continuation to be valid (i.e., not called yet). Once
continue returns, the continuation is invalidated, since we state in the writes
clause that the k._valid field is written, hence one can no longer suppose it is
set to true.
    This encoding of the continuation data type is in fact a form of defunction-
alization [4], where continue resembles the Why3apply function that is gen-
erated during defunctionalization. A major difference in our approach is that
we do not represent continuations as an algebraic data types. Instead, we fully
capture of such values in their specification, as we explain in what follows.

4.4   Specifying continuations
Using all these different pieces, we can now conclude our WhyML proof by
creating a value k of type continuation and specifying it using the pre and
post predicates defined previously. For the example of the XCHG handler, this is
done as follows:
  try xchg (xchg 42) with                                                 WhyML
  | XCHG n ->
      val k : continuation int int in
      assume { ... };
      let old_p = !p in
      p := n;
      continue k old_p
The WhyML val..in construction allows one to introduce local abstract values,
i.e., without imposing a particular implementation. The conditions that go in
the assume clause are essentially the specification for k. First, we state that the
continuation is valid:

                                        8
  assume { k._valid }                                                      WhyML

Next, using the pre predicate, we state that the precondition for k is the proto-
col’s postcondition. Although this might seem counterintuitive at first, the proto-
col’s postcondition is the condition that Server must respect when it surrenders
control to Client via the suspended continuation. Therefore, the Client must
ensure the protocol’s postcondition when calling the continuation. To recap, the
protocol’s postcondition is the following:
  (*@ protocol XCHG n :                                          GOSPEL + OCaml
      ensures reply = old !p && !p = n *)
We must now translate the postcondition to WhyML and encode it with the pre
predicate, as follows:
  assume { let eff_p = !p in                                               WhyML
           forall reply state.
           pre k reply state <->
           reply = eff_p && state._p = n }
Within this clause, we state that the precondition of k is that the reply must
be equal to eff_p, the value p takes when the continuation is created (in other
words, when the effect is performed). Next, using the state type, we say that
when k is called the value stored in p is equal to n, the value passed by Client.
    Finally, using the post predicate, we state that the postcondition of k is the
handler’s postcondition. This is because calling k reinstalls the handler, any call
to k terminates when it exists the handler. Once again, the postcondition of the
handler is
  try_ensures !p = old !p && result = 42                         GOSPEL + OCaml

To translate this to WhyML, we need to access the value p held before xchg
was called. To do so, we create an auxiliary variable init_p and translate the
handler’s postcondition as follows:
  let init_p = !p in                                                       WhyML
  try xchg (xchg 42) with
  | XCHG n ->
    ...
    assume { forall reply old_state state result.
              post k reply old_state state result <->
              state._p = 3 && result = init_p }
It is worth noting that we do not use the initial state in which the continuation
is called nor the reply its its postcondition. This is because these values are only
relevant for the continuation’s precondition.

The generated Verification Conditions. We take a step back and observe what
VCs Why3 generates for the resulting WhyML program, and what they mean


                                         9
     Case study                   # VCs       LOC / Spec. / Ghost Proof time
     Control inversion              15           20 / 25 / 2         0.74
     Division interpreter           19           18 / 16 / 2         0.74
     Koda-Ruskey algorithm         142           26 / 20 / 0        17.60
     References                     36           37 / 22 / 3         0.91
     Xchg                           13            13 / 7 / 0         0.64
     Shallow Handlers               13             21 / 7 / 0        0.54
     Fig. 1: Summary of the case studies verified with extended Cameleer.


from the perspective of the original OCaml program. For Client, Why3 gen-
erates one VC checking if the postcondition of the xchg function holds. See-
ing as this function has the same postcondition as the perform_XCHG function,
this is proved trivially. As for Server, we generate four VCs. First, one must
prove that the handler’s invariant holds when the function terminates through
the non-exceptional branch. Since the handler’s invariant is the same as xchg’s
postcondition, this is also proved. Next, the proof that the continuation has not
been called yet (trivially, since the continuation is created valid) and that the
continuation’s precondition is respected. Given this handler respects the proto-
col, this VC is also dispatched. Finally the proof that the handler’s invariant is
maintained when we exit through the exceptional case. Seeing as the handler’s
last instruction is calling the continuation, whose postcondition is the handler’s
invariant, this is also proved.
    We give in Appendix A a general presentation of our translation scheme from
OCaml programs with effects and handlers to WhyML. We believe this approach
is general enough, hence it could be adapted to any proof-aware language with
exceptions.


5   Evaluation
To test our approach, we specify and verify a handful of illustrative case studies.
Besides the XCHG example we have already presented in detail, we also verify the
following case studies:
 1. Turning a higher order iterator function into a generator. This process is
    commonly referred to as control inversion.
 2. A division interpreter that performs an effect in case of a division by zero.
 3. Implementing mutable state using algebraic effects and deep handlers, as
    shown in Sec. 2.
 4. The Koda-Ruskey algorithm.
 5. Implementing a deep handler using a shallow handler. Our support for shal-
    low handlers is still experimental, as we are currently a significant number
    of bureaucratic verification conditions to deal with unhandled effects.
The reported case studies are all automatically verified, using a combination of
Alt-Ergo 2.4.2, CVC4 1.8, and Z3 4.8.6 SMT solvers. Fig. 1 summarizes impor-
tant metrics about our verified case studies: the number of generated verification


                                         10
conditions for each example; the total lines of OCaml code, GOSPEL specifica-
tion, and lines of ghost (these are also included in the number of OCaml LOC),
respectively; and finally the time it takes (in seconds) to replay a proof. The
runtimes were measured by averaging over ten runs on a Lenovo Thinkpad X1
Carbon 8th Generation, running Linux Mint 20.1, OCaml 5.0.0, and Why3 1.5.1.
    All examples, including OCaml implementation, GOSPEL specification, and
Why3 proof sessions files are publicly available2 . It is worth noting that through-
out this paper we use a friendly syntax for effect and handlers, which is not
supported natively by the OCaml compiler (this was in fact the syntax proposed
in an experimental-oriented switch of the compiler). However, all of our case
studies are written using the effects and handlers library supported by OCaml
5.0.0.

A more elaborate case study. Most of the proofs enumerated, although not trivial,
are relatively small scale examples. The outlier is the Koda-Ruskey algorithm [12]
which enumerates the valid colorings of a forest of n-ary trees. The complete
OCaml implementation and GOSPEL for this algorithm is depicted in Fig. 2.
Very briefly put, the nodes of a tree can either be colored White or Black. If
a node is colored White, all of its children must be White; if it is Black, there
are no restrictions posed on the color of its children. Each time the algorithm
reaches a new coloring, an effect is performed. The global array bits is used to
represent each new coloring.
    Not only is this a very challenging proof, it is the only implementation we
are aware of for the Koda-Ruskey algorithm using algebraic effects. Although
we are not going to go over the entire specification, the key part is that the
protocol for this function is defined locally. This is because we want to state
that, whenever an effect is performed, the forest has a valid coloring. Since the
forest is passed as an argument, however, we must define the protocol within
the scope of the function to refer to its argument. Our proof, namely auxiliary
definitions and lemmas about forests and colorings, follows closely a previous
Why3 for a first-order, stack-based version of the Koda-Ruskey algorithm [6].


6     Related Work
The most common type of static verifications programmers use for their pro-
grams is type-checking. A possible way of extending a type system’s reach is
by adding an effect system [1]. In normal type systems, we generally have type
signatures such as f : α →
                         − β, where f is a function that receives an argument of
type α and returns a value of type β. When using an effect system, type signa-
tures have an additional parameter: a row ρ. A row is simply a list of signatures
indicating which effects this function performs. With this typing information,
we can determine, at compile time, if a program will perform any unhandled
effects, thereby removing yet another common source of errors. Effect systems
can be used to track not only algebraic effects, but any kind of impure behavior
2
    https://github.com/mrjazzybread/cameleer/tree/effects/tests


                                        11
  effect Yield : unit                                                OCaml

  let koda_ruskey (f : forest) =
    let rec enum_eff (f : forest) ((baton : forest list)[@ghost])
    = match f with
      | E -> perform Yield
      | N (i, l, r) ->
         if bits.(i) = White then begin
           enum_eff r baton;
           bits.(i) <- Black;
           try enum_eff l (r :: baton) with
           | Yield -> enum_eff r baton; continue k ()
         end else begin
           begin try enum_eff l (r :: baton) with
           | effect Yield -> enum_eff r baton; continue k () end;
           bits.(i) <- White;
           enum_eff r baton end
    (*@ requires valid_nums_forest f (length bits)
        requires disjoint_stack f baton
        requires any_forest f bits.elts
        ensures forall i.
                not mem_forest i f && not mem_stack i baton ->
                bits[i] = old bits[i]
        ensures inverse (Cons f baton) (old bits.elts) bits.elts
        variant f
        protocol Yield {
          requires valid_coloring f bits.elts
          requires forall i.
                    not mem_stack i baton -> bits[i] = old bits[i]
          requires unchanged baton (old bits.elts) bits.elts ||
                    inverse baton (old bits.elts) bits.elts
          ensures forall i.
                   not mem_stack i baton -> bits[i] = old bits[i]
          ensures inverse baton (old bits.elts) bits.elts
          modifies bits } *)
  in enum_eff f []
(*@ requires valid_nums_forest f (length bits)
    requires white_forest f bits.elts
    performs Yield *)



    Fig. 2: The Koda-Ruskey algorithm implementation and specification.




                                    12
such as mutable state and divergence [13]. This means we can imbue within the
typing information whether or not a function is pure.
    Although effect handlers are, still, relatively niche, there has been some work
in modelling their behavior using equational theory. The vanguard of this ap-
proach was Plotkin and Power [17] where they reason over effects as equations of
effectful computations. Some research has been done by applying this algebraic
approach to effects and handlers. For example, Plotkin and Pretnar [18,19] devel-
oped a logic where the semantics of effects was captured using this approach and
handlers were verified by determining if they satisfied a set of equalities. Addi-
tionally, some implementations have been developed that embed these reasoning
rules into Coq, an interactive theorem prover [14, 24].
    Another important line of research is reasoning about the concurrent be-
havior of effects and handlers into Separation Logic. For instance, Timany and
Birkedal [23] developed a framework for the verification of full stack continu-
ations in a language with call/cc. Additionally, Hinrichsen et al. [8] developed
an extension of Coq [9] for reasoning over programs with message passing using
protocols that define the rules that two agents must respect in their exchange.
Drawing inspiration from this research, de Vilhena and Pottier [5] developed a
simplified version of protocols for programs with algebraic effects. Their frame-
work interprets effects and effect handlers as a communication between two
agents: the one who raised the effect and its handler. To model this communi-
cation, they use protocols which describe the values that can be sent in either
direction during this communication. The logic that governs these protocols is
built on top of Iris, a higher order separation logic encoded in Coq. These pro-
tocols are, indeed, the main inspiration for the Cameleer extension we have
developed.


7   Conclusions and Future Work

We have presented an extension to the Cameleer tool to specify and reason about
algebraic effects and handlers. This lead us to introduce several extensions to the
GOSPEL itself, namely the introduction of protocols at the level of specifica-
tion, as well as the performs and try_ensures clauses. In order to explore such
specification approach, we implemented inside Cameleer a translation scheme
from OCaml into a WhyML embedding, which features exceptions and defunc-
tionalization of continuations as a means to reason about effects and handlers.
To the best of our knowledge, this extension to Cameleer is the first framework
that proposes an automated verification path to algebraic effects.
    As future work, we plan extend our tool to handle hidden state, seeing as
we can only deal with mutable state defined at the top-level. Additionally, our
tool can only prove handlers that remain installed when we call the generated
continuation: we plan to add support for handlers where the continuation may
produce an unhandled effect. Finally, our long term goal is to employ Cameleer in
the effort of verifying larger OCaml libraries that make a significant use of effects

                                         13
and handlers. A good candidate is the eio3 , a library that proposes direct-style
concurrency primitives (implemented as effects and handlers) for the OCaml
language.


References
 1. Bauer, A., Pretnar, M.: An effect system for algebraic effects and handlers. In:
    Heckel, R., Milius, S. (eds.) Algebra and Coalgebra in Computer Science. pp. 1–
    16. Springer Berlin Heidelberg, Berlin, Heidelberg (2013)
 2. Bobot, F., Filliâtre, J.C., Marché, C., Paskevich, A.: Why3: Shepherd your herd of
    provers. Boogie 2011: First International Workshop on Intermediate Verification
    Languages (05 2012)
 3. Charguéraud, A., Filliâtre, J., Lourenço, C., Pereira, M.: GOSPEL — Providing
    OCaml with a Formal Specification Language. In: Formal Methods - The Next 30
    Years - Third World Congress. Lecture Notes in Computer Science, vol. 11800, pp.
    484–501. Springer (2019), 10.1007/978-3-030-30942-8_29
 4. Danvy, O., Nielsen, L.R.: Defunctionalization at work. In: Proceedings of the 3rd
    international ACM SIGPLAN conference on Principles and practice of declar-
    ative programming, September 5-7, 2001, Florence, Italy. pp. 162–174. ACM
    (2001). https://doi.org/10.1145/773184.773202, https://doi.org/10.1145/
    773184.773202
 5. de Vilhena, P.E., Pottier, F.: A separation logic for effect handlers. Proc. ACM
    Program. Lang. 5(POPL) (jan 2021). https://doi.org/10.1145/3434314, https:
    //doi.org/10.1145/3434314
 6. Filliâtre, J., Pereira, M.: Producing all ideals of a forest, formally (verification
    pearl). In: Blazy, S., Chechik, M. (eds.) Verified Software. Theories, Tools, and
    Experiments - 8th International Conference, VSTTE 2016, Toronto, ON, Canada,
    July 17-18, 2016, Revised Selected Papers. Lecture Notes in Computer Science,
    vol. 9971, pp. 46–55 (2016). https://doi.org/10.1007/978-3-319-48869-1_4,
    https://doi.org/10.1007/978-3-319-48869-1_4
 7. Hillerström, D., Lindley, S.: Shallow effect handlers. In: Ryu, S. (ed.) Programming
    Languages and Systems. pp. 415–435. Springer International Publishing, Cham
    (2018)
 8. Hinrichsen, J.K., Bengtson, J., Krebbers, R.: Actris: Session-type based reasoning
    in separation logic. Proc. ACM Program. Lang. 4(POPL) (dec 2019). https://
    doi.org/10.1145/3371074, https://doi.org/10.1145/3371074
 9. Jung, R., Krebbers, R., Jourdan, J.H., Bizjak, A., Birkedal, L., Dreyer, D.:
    Iris From the Ground Up: A Modular Foundation For Higher-order Concurrent
    Separation Logic. Journal of Functional Programming 28(e20) (2018). https:
    //doi.org/10.1017/S0956796818000151, https://hal.archives-ouvertes.fr/
    hal-01945446
10. Kammar, O., Lindley, S., Oury, N.: Handlers in action. SIGPLAN Not. 48(9),
    145–158 (sep 2013). https://doi.org/10.1145/2544174.2500590, https://doi.
    org/10.1145/2544174.2500590
11. Kanig, J., Filliâtre, J.C.: Who: A Verifier for Effectful Higher-order Programs. In:
    ACM SIGPLAN Workshop on ML. Edinburgh, Scotland, UK (Aug 2009), http:
    //www.lri.fr/~filliatr/ftp/publis/wml09.pdf
3
    https://github.com/ocaml-multicore/eio


                                          14
12. Koda, Y., Ruskey, F.: A gray code for the ideals of a forest poset. Jour-
    nal of Algorithms 15(2), 324–340 (1993). https://doi.org/https://doi.org/
    10.1006/jagm.1993.1044, https://www.sciencedirect.com/science/article/
    pii/S0196677483710448
13. Leijen, D.: Koka: Programming with row polymorphic effect types. Electronic Pro-
    ceedings in Theoretical Computer Science 153 (06 2014). https://doi.org/10.
    4204/EPTCS.153.8
14. Letan, T., Régis-Gianas, Y., Chifflier, P., Hiet, G.: Modular Verification of Pro-
    grams with Effects and Effect Handlers in Coq. In: FM 2018 - 22nd International
    Symposium on Formal Methods. LNCS, vol. 10951, pp. 338–354. Springer, Oxford,
    United Kingdom (Jul 2018). https://doi.org/10.1007/978-3-319-95582-7_20,
    https://hal.inria.fr/hal-01799712
15. Pereira, M., Ravara, A.: Cameleer: A deductive verification tool for ocaml. In:
    Silva, A., Leino, K.R.M. (eds.) Computer Aided Verification - 33rd International
    Conference, CAV 2021, Virtual Event, July 20-23, 2021, Proceedings, Part II.
    Lecture Notes in Computer Science, vol. 12760, pp. 677–689. Springer (2021).
    https://doi.org/10.1007/978-3-030-81688-9_31, https://doi.org/10.1007/
    978-3-030-81688-9_31
16. Plotkin, G., Power, J.: Algebraic operations and generic effects. Applied Categori-
    cal Structures 11, 69–94 (02 2003). https://doi.org/10.1023/A:1023064908962
17. Plotkin, G., Power, J.: Computational effects and operations: An
    overview. Electronic Notes in Theoretical Computer Science 73, 149–163
    (2004).      https://doi.org/https://doi.org/10.1016/j.entcs.2004.08.008,
    https://www.sciencedirect.com/science/article/pii/S1571066104050893,
    proceedings of the Workshop on Domains VI
18. Plotkin, G., Pretnar, M.: A logic for algebraic effects. In: Proceedings of the 2008
    23rd Annual IEEE Symposium on Logic in Computer Science. p. 118–129. LICS
    ’08, IEEE Computer Society, USA (2008). https://doi.org/10.1109/LICS.2008.
    45, https://doi.org/10.1109/LICS.2008.45
19. Plotkin, G., Pretnar, M.: Handlers of algebraic effects. In: Castagna, G. (ed.) Pro-
    gramming Languages and Systems. pp. 80–94. Springer Berlin Heidelberg, Berlin,
    Heidelberg (2009)
20. Régis-Gianas, Y., Pottier, F.: A hoare logic for call-by-value functional pro-
    grams. In: Audebaud, P., Paulin-Mohring, C. (eds.) Mathematics of Program
    Construction, 9th International Conference, MPC 2008, Marseille, France, July
    15-18, 2008. Proceedings. Lecture Notes in Computer Science, vol. 5133, pp. 305–
    335. Springer (2008). https://doi.org/10.1007/978-3-540-70594-9_17, https:
    //doi.org/10.1007/978-3-540-70594-9_17
21. Reynolds, J.C.: Definitional interpreters for higher-order programming languages.
    In: Proceedings of the ACM Annual Conference - Volume 2. p. 717–740. ACM
    ’72, Association for Computing Machinery, New York, NY, USA (1972). https:
    //doi.org/10.1145/800194.805852, https://doi.org/10.1145/800194.805852
22. Sivaramakrishnan, K., Dolan, S., White, L., Kelly, T., Jaffer, S., Madhavapeddy,
    A.: Retrofitting effect handlers onto ocaml. In: Proceedings of the 42nd ACM
    SIGPLAN International Conference on Programming Language Design and Im-
    plementation. p. 206–221. PLDI 2021, Association for Computing Machinery, New
    York, NY, USA (2021). https://doi.org/10.1145/3453483.3454039, https://
    doi.org/10.1145/3453483.3454039
23. Timany, A., Birkedal, L.: Mechanized relational verification of concurrent programs
    with continuations. Proc. ACM Program. Lang. 3(ICFP) (jul 2019). https://doi.
    org/10.1145/3341709, https://doi.org/10.1145/3341709


                                          15
24. Xia, L.y., Zakowski, Y., He, P., Hur, C.K., Malecha, G., Pierce, B.C., Zdancewic,
    S.: Interaction trees: Representing recursive and impure programs in coq. Proc.
    ACM Program. Lang. 4(POPL) (dec 2019). https://doi.org/10.1145/3371119,
    https://doi.org/10.1145/3371119




                                         16
A     General Translation Scheme


H(e0t , E x̄, ē, Shensures ,termpost , τ , Σ, termstate ) =
  let handler () =                                                     WhyML
    ensures{Shensures1 }
    ensures{Shensures2 }
    ...
        let init_state = Sx̄ in
        try e0t with
        |...
        |En x̄ ->
             let eff_state = Sx̄ in
             val gen_k unit : continuation (π2 (Σ(En ))) τ
             ensures{valid result}
             ensures{
                  forall arg state.
                  pre result arg state <->
                  E_post arg eff_state state result
             }
             ensures{
                  let f = result in
                  forall arg irrelevant_old_state state result.
                  post f arg irrelevant_old_state state result <->
                    let state_old = init_state in
                    termpost ∧ termstate
             } in let k = gen_k () in ent
         |...
    in handler ()


                       Fig. 3: Translation rule for effect handlers.




                                               17
                           O() = true
                       O(x :: t) = state.x = state_old.x ∧ O(t)


                                Fig. 4: Unmodified State


                                 T (τ1 −
                                       → τ2 −
                                            → τ3 ) =
                                    let s = T (τ2 −
                                                  → τ3 ) in
                                    τ1 :: π1 (s), π2 (s)


                                 T (τ1 −
                                       → τ2 −
                                            → τ3 ) =
                                    (τ1 −
                                        → τ2 ) = τ1 , τ 2


                                 T (τ1 −
                                       → τ2 −
                                            → τ3 ) =
                                 T (τ ) = unit, τ


                            Fig. 5: Effect Type Translation.

D (args = x1 : τ1 , x2 : τ2 , ..., xn : τn ) τr et S̄ termpre termpost =
       let f args S̄ = et in                                               WhyML
       val gen_f () : lambda (τ1 , τ2 , ..., τn ) τr
       ensures{
         forall arg state. pre result arg state <->
           let x1 , x2 ... = arg in
           termpre
       }
       ensures{
         let f = result in
         forall arg old_state state result.
         post f arg old_state state result <->
         let x1 , x2 ... = arg in
         termpost
       } in gen_f ()



                         Fig. 6: Defunctionalization Function.


                            S(term :: xs) = h(term) ∧ S(xs)
                                      S() = true


                             Fig. 7: Combination of terms


                                              18
P(E, x̄, Σ, termpre , termpost , mod) =
      predicate pre_E (arg : π1 (Σ(E))) (state : state) =      WhyML
          let x̄ = arg in
          termpre

      predicate post_E (arg : π1 (Σ(E))) (old_state : state)
                         (state : Sτ ) (reply : π2 (Σ(E))) =
          let x̄ = arg in
          termpost


      val perform_E (arg: π1 (Σ(E))) : π2 (Σ(E))
      requires{pre_E arg Sx̄ }
      ensures{post_E arg (old Sx̄ ) Sx̄ result}
      writes{mod}



                     Fig. 8: Protocol Translation Function.




                                          19
                                                                                                 (TEffect)
            Σ ◦ ∆ ◦ ν ◦ µ ` Jeffect E : τ K              exception E a Σ[E −
                                                                           → T (τ )]

                                                                                        (TPerform)
                     Σ ◦ ∆ ◦ ν ◦ µ ` Jperform Ex̄K             perform_E x̄ a

                 S(Sprequires ) = termpre                S(Spensures ) = termpost
                                                                                                             (TProtocol)
Σ ◦ ∆ ◦ ν ◦ µ ` Jprotocol E x̄ : SpK          P(E, x̄, Σ, termpre , termpost , Spmodif ies ) a

   Σ ◦ ∆ ◦ ν ∪ x ◦ ∅ ` JeK         e t a µ0       S(S̄requires ) = pre            S(S̄ensures ) = post
                                                                                                           (TFun)
   Σ ◦ ∆ ◦ ν ◦ µ ` Jfun S̄ (x : τarg ) : τret −
                                              → eK            D (x : τarg ) τret et S̄ pre post a

                                                                                                     (TPerformsClause)
         Σ ◦ ∆ ◦ ν ◦ µ ` Jperforms EK              raises{E arg −
                                                                → E_pre arg Sx̄ } a

               ∀i Σ ◦ ∆ ◦ ν ◦ µi ` Jei K        eit a µi+1        e0 = x =⇒ x ∈ ν
                                                                                                 (TAppDefun)
            Σ ◦ ∆ ◦ ν ◦ µ0 ` Je0 e1 ... en K          apply e0 (e2 , e3 , ..., en ) a Svars

                     ∀i Σ ◦ ∆ ◦ ν ◦ µi ` Jei K           eit a µi+1         ¬x ∈ ν
                                                                                                    (TApp)
           Σ ◦ ∆ ◦ ν ◦ µ ` Jx e0 e1 ... en K            x e0t e1t . . . ent a ∆(x) ∪ µn+1

  ∀i.0 < i 5 n =⇒ Σ ◦ ∆ ◦ ν ◦ µi ` Jei K  eit a µi+1  S(Shensures ) = termpost
             Shreturns = τ   etry = try e0 with Sh effect E x̄ k −
                                                                 →e
                                                                                                             (TTry)
Σ ◦ ∆ ◦ ν ◦ ∅ ` Jetry K       H(E x̄, e, Shensures , termpost , τ, Σ, O(Svars \ µn+1 )) a µn

                                    Σ ◦ ∆ ◦ ν ◦ ∅ ` JeK   et a µ
           e 6= f un ...       x̄ 6=  =⇒ ∆0 = ∆[f −    → µ]     x̄ =  =⇒ ∆0 = ∆
                                                                                                    (TLet)
                 Σ ◦ ∆ ◦ ν ◦ ∅ ` Jlet S̄ f x̄ = eK            let S̄ f x̄ = et a ∆0

          Σ ◦ ∆ ◦ ν ◦ µ ` Je1 K        e1t a µ0         Σ ◦ ∆ ◦ ν ◦ µ0 ` Je2 K          e2t a µ00
                                                                                                     (TIf)
        Σ ◦ ∆ ◦ ν ◦ µ ` Jif a then e1 else e2 K              if a then e1t else e2t a µ00

          Σ ◦ ∆ ◦ ν ◦ µ ` Je1 K        e1t a µ0         Σ ◦ ∆ ◦ ν ◦ µ0 ` Je2 K          e2t a µ00
                                                                             00                     (TSeq)
                            Σ ◦ ∆ ◦ ν ◦ µ ` Je1 ; e2 K        e1 ; e2 a µ

                                  x̄ 6=  =⇒ µ = ∅
    Σ ◦ ∆ ◦ ν ◦ µ ` Je1 K e1t a µ0      e 6= f un ...   x̄ 6=  =⇒ ∆0 = ∆[f −
                                                                            → µ0 ]
                            0                 0       0                  00
                x̄ =  =⇒ ∆ = ∆         Σ ◦ ∆ ◦ ν ◦ µ ` Je2 K    e2t a µ
                                                                                                          (TLetIn)
        Σ ◦ ∆ ◦ ν ◦ µ ` Jlet S̄ f x̄ = e1 in e2 K            let S̄ f x̄ = e1t in e2t a µ00

            ∀i.0 5 i < n =⇒ Σ ◦ ∆ ◦ ν ◦ µi ` Jei K               eit a Σ ◦ ∆ ◦ ν ◦ µi+1
                                                                                                           (TMatch)
   Σ ◦ ∆ ◦ ν ◦ µ ` Jmatch a with p −
                                   → ei K               match a with p −
                                                                       → eit a Σ ◦ ∆ ◦ ν ◦ µn

                                                         (TModifies)
Σ ◦ ∆ ◦ ν ◦ µ ` Jmodifies s̄K         writes{s} a                            Σ ◦ ∆ ◦ ν ◦ µ ` JK           a (Tempty)

      Σ ◦ ∆ ◦ ν ◦ ∅ ` JdK        dt a Σ0 ◦ ∆0         Σ0 ◦ ∆0 ◦ ν ◦ ∅ ` JdK
                                                                         ¯             dtl a Σ00 ◦ ∆00
                                                 ¯                     00         00                     (TDecl)
                           Σ ◦ ∆ ◦ ν ◦ ∅ ` Jd :: dK       dt :: dtl a Σ ◦ ∆
                                                   20
                             Fig. 9: Inductive Translation Rules.
