                                                                                                                                                                  1

                                         Statically Verified Refinements for Multiparty Protocols

                                         FANGYI ZHOU, Imperial College London, United Kingdom
arXiv:2009.06541v1 [cs.PL] 14 Sep 2020




                                         FRANCISCO FERREIRA, Imperial College London, United Kingdom
                                         RAYMOND HU, University of Hertfordshire, United Kingdom
                                         RUMYANA NEYKOVA, Brunel University London, United Kingdom
                                         NOBUKO YOSHIDA, Imperial College London, United Kingdom
                                         With distributed computing becoming ubiquitous in the modern era, safe distributed programming is an open
                                         challenge. To address this, multiparty session types (MPST) provide a typing discipline for message-passing
                                         concurrency, guaranteeing communication safety properties such as deadlock freedom.
                                            While originally MPST focus on the communication aspects, and employ a simple typing system for com-
                                         munication payloads, communication protocols in the real world usually contain constraints on the payload.
                                         We introduce reﬁned multiparty session types (RMPST), an extension of MPST, that express data dependent
                                         protocols via reﬁnement types on the data types.
                                            We provide an implementation of RMPST, in a toolchain called Session⋆ , using Scribble, a multiparty
                                         protocol description toolchain, and targeting F⋆ , a veriﬁcation-oriented functional programming language.
                                         Users can describe a protocol in Scribble and implement the endpoints in F⋆ using reﬁnement-typed APIs
                                         generated from the protocol. The F⋆ compiler can then statically verify the reﬁnements. Moreover, we use a
                                         novel approach of callback-styled API generation, providing static linearity guarantees with the inversion of
                                         control. We evaluate our approach with real world examples and show that it has little overhead compared
                                         to a naïve implementation, while guaranteeing safety properties from the underlying theory.
                                         CCS Concepts: • Theory of computation → Automated reasoning; Distributed computing models; • Soft-
                                         ware and its engineering → Source code generation;
                                         ACM Reference Format:
                                         Fangyi Zhou, Francisco Ferreira, Raymond Hu, Rumyana Neykova, and Nobuko Yoshida. 2018. Statically
                                         Veriﬁed Reﬁnements for Multiparty Protocols. Proc. ACM Program. Lang. 1, CONF, Article 1 (January 2018),
                                         37 pages.

                                         1   INTRODUCTION
                                         Distributed interactions and message passing are fundamental elements of the modern comput-
                                         ing landscape. Unfortunately, language features and support for high-level and safe programming
                                         of communication-oriented and distributed programs are much lacking, in comparison to those
                                         enjoyed for more traditional “localised” models of computation. One of the research directions to-
                                         wards addressing this challenge is concurrent behavioural types [Ancona et al. 2016; Gay and Ravara
                                         2017], which seek to extend the beneﬁts of conventional type systems, as the most successful form
                                         of lightweight formal veriﬁcation, to communication and concurrency.
                                            Multiparty session types (MPST) [Honda et al. 2008, 2016], one of the most active topics in this
                                         area, oﬀer a theoretical framework for specifying message passing protocols between multiple
                                         participants. MPST use a type system–based approach to statically verify whether a system of pro-
                                         cesses implements a given protocol safely. The type system guarantees key execution properties

                                         Authors’ addresses: Fangyi Zhou, Imperial College London, United Kingdom, fangyi.zhou15@imperial.ac.uk; Francisco
                                         Ferreira, Imperial College London, United Kingdom, f.ferreira-ruiz@imperial.ac.uk; Raymond Hu, University of Hertford-
                                         shire, United Kingdom, r.z.h.hu@herts.ac.uk; Rumyana Neykova, Brunel University London, United Kingdom, rumyana.
                                         neykova@brunel.ac.uk; Nobuko Yoshida, Imperial College London, United Kingdom, n.yoshida@imperial.ac.uk.

                                         2018. 2475-1421/2018/1-ART1 $15.00
                                         https://doi.org/


                                                                         Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:2      Fangyi Zhou, Francisco Ferreira, Raymond Hu, Rumyana Neykova, and Nobuko Yoshida

             G = A → B : Count(count : int{count ≥ 0}).
                 µt(curr :int{curr ≥ 0 ∧ curr ≤ count })hcurr := 0i.                      
                           Hello(it : int{curr < count ∧ it = count }).thcurr := curr + 1i
                 B→C
                           Finish(it : int{curr = count ∧ it = count }).end
                                                  A Global Type G
          Projection onto
          each Participant
             Local Type for A LA                Local Type for B LB               Local Type for C LC

                                        Fig. 1. Top-down View of (R)MPST

such as freedom from message reception errors or deadlocks. However, despite much recent pro-
gress, there remain large gaps between the current state of the art and (i) powerful and practical
languages and techniques available to programmers today, and (ii) more advanced type disciplines
needed to express a wider variety of constraints of interaction found in real-world protocols.
   This paper presents and combines two main developments: a theory of MPST enriched with re-
ﬁnement types [Freeman and Pfenning 1991], and a practical method, callback-based programming,
for safe session programming. The key ideas are as follows:
   Reﬁned Multiparty Session Types (RMPST). The MPST theory [Honda et al. 2008, 2016] provides
a core framework for decomposing (or projecting) a global type structure, describing the collective
behaviour of a distributed system, into a set of participant-speciﬁc local types (see Fig. 1). The local
types are then used to implement endpoints.
   Our theory of RMPST follows the same top-down methodology, but enriches MPST with fea-
tures from reﬁnement types [Freeman and Pfenning 1991], to support the elaboration of data types
in global and local types. Reﬁnement types allow reﬁnements in the form of logical predicates and
constraints to be attached to a base type. This allows to express various constraints in protocols.
   To motivate our reﬁnement type extension, we use a counting protocol shown in Fig. 1, and
leave the details to § 4. Participant A sends B a number with a Count message. In this message, the
reﬁnement type count : int{count ≥ 0} restricts the value for count to be a natural number. Then
B sends C exactly that number of Hello messages, followed by a Finish message.
   We demonstrate how reﬁnement types are used to better specify the protocol: The counting part
of the protocol is described using a recursive type with two branches, where we use reﬁnement
types to restrict the protocol ﬂow. The variable curr is a recursion variable, which remembers
the current iteration, initialised to 0, and increments on each recursion (curr := curr + 1). The
reﬁnement curr = count in the Finish branch speciﬁes that the branch may only be taken at the
last iteration; the reﬁnement it = count in both Hello and Finish branches speciﬁes a payload value
dependent on the recursion variable curr and the variable count transmitted in the ﬁrst message.
   We establish the correctness of Reﬁned MPST. In particular, we show that projection is behaviour-
preserving and that well-formed global types with reﬁnements satisfy progress, i.e. they do not
get stuck. Therefore, if the endpoints follow the behaviour prescribed by the local types, derived
(via projection) from a well-formed global type with reﬁnements, the system is deadlock-free.
   Callback-styled, Reﬁnement-typed APIs for Endpoint Implementations. One of the main
challenges in applying session types in practice is dealing with session linearity: a session channel
is used once and only once. Session typing relies on a linear treatment of communication chan-
nels, in order to track the I/O actions performed on the channel against the intended session type.
Most existing implementations adopt one of two approaches: monadic interfaces in functional

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
 Statically Verified Refinements for Multiparty Protocols                                                      1:3

 languages [Imai et al. 2020, 2019; Orchard and Yoshida 2017], or “hybrid” approaches that comple-
 ment static typing with dynamic linearity checks [Hu and Yoshida 2016; Scalas et al. 2017].
    This paper proposes a fresh look to session-based programming that does not require linearity
 checking for static safety. We promote a form of session programming where session I/O is impli-
 citly implemented by callback functions — we say “implicitly” because the user does not write any
 I/O operations themself: an input callback is written to take a received message as a parameter,
 and an output callback is written to simply return the label and value of the message to be sent.
    The callbacks are supported by a runtime, generated along with APIs in reﬁnement types ac-
 cording to the local type. The runtime performs communication and invokes user-speciﬁed call-
 back functions upon corresponding communication events. We provide a code generation tool to
 streamline the writing of callback functions for the projected local type.
    The inversion of control allows us to dispense with linearity checking, because our approach
 does not expose communication channels to the user. Our approach is a natural ﬁt to functional
 programming settings, but also directly applicable to any statically typed language. Moreover, the
 linearity guarantee is achieved statically without the use of a linear type system, a feature that is
 usually not supported by mainstream programming languages. We follow the principle of event-
 based programming via the use of callbacks, prevalent in modern days of computing.

    A Toolchain Implementation: Session⋆. To evaluate our proposal, we implement RMPST
 with a toolchain — Session⋆ , as an extension to the Scribble toolchain [Hu 2017; Scribble Authors
 2015] (http://www.scribble.org/) with F⋆ [Swamy et al. 2016] as the target endpoint language.
    Building on our callback approach, we show how to integrate RMPST with the veriﬁcation-
 oriented functional programming language F⋆ , exploiting its capabilities of reﬁnement types and
 static veriﬁcation to extend our fully static safety guarantees to data reﬁnements in sessions. Our
 experience of specifying and implementing protocols drawn from the literature and real-world ap-
 plications attests to the practicality of our approach and the value of statically veriﬁed reﬁnements.
 Our integration of RMPST and F⋆ allows developers to utilise advanced type system features to
 implement safe distributed application protocols.

    Paper Summary and Contributions.

§ 2 We present an overview of our toolchain: Session⋆ , and provide background knowledge of
    Scribble and MPST. We use a number guessing game, HigherLower , as our running example.
§ 3 We introduce Session⋆ , a toolchain for RMPST. We describe in detail how our generated APIs
    can be used to implement multiparty protocols with reﬁnements.
§ 4 We establish the metatheory of RMPST, which gives semantics of global and local types with re-
    ﬁnements. We prove trace equivalence of global and local types w.r.t. projection (Theorem 4.10),
    and show progress and type safety of well-formed global types (Theorem 4.14 and Theorem 4.15).
§ 5 We evaluate our toolchain with examples from the session type literature, and measure the
    time taken for compilation and execution. We show that our toolchain does not have a long
    compilation time, and our runtime does not incur a large overhead on execution time.

   We submitted an artifact for evaluation [Zhou et al. 2020], containing the source code of our
 toolchain Session⋆, with examples and benchmarks used in the evaluation. The artifact is available
 as a Docker image, and can be accessed on the Docker Hub. The source ﬁles are available on
 GitHub (https://github.com/sessionstar/oopsla20-artifact). We present the proof of our theorems,
 and additional technical details of the toolchain, in the appendix.

                             Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:4           Fangyi Zhou, Francisco Ferreira, Raymond Hu, Rumyana Neykova, and Nobuko Yoshida

       Scribble Protocol (§ 2.2)
                                                 Endpoint Implementation (§ 3.2)
      global protocol HigherLower
        (role A, role B, role C) {                 let callbacks = ...                           User Input
        start(n0:int) from A to B;                 let connection = ...
        ...                                        let () =
      }                                              run callbacks connection

                                                                                                 Extracted
       Projection                                   Implements                     Extracts    OCaml Program
      via Scribble                                                                   into       program.ml
                     6        7                    type state = ...
                                                   type callbacks = ...
                                     Generates
          1      2       3    4                    type conn = ...                            Internal/Generated
                                                   let run callbacks conn =
                     5                               ...


        CFSM Representation                                  F⋆ API

                                             Fig. 2. Overview of Toolchain




2 OVERVIEW OF REFINED MULTIPARTY SESSION TYPES
In this section, we give an overview of our toolchain: Session⋆ , describing its key toolchain stages.
Session⋆ extends the Scribble toolchain with reﬁnement types and uses F⋆ as a target language.
We begin with a short background on basic multiparty session types and Scribble, then demon-
strate the speciﬁcation of distributed applications with reﬁnements using the extended Scribble.

2.1      Toolchain Overview
We present an overview of our toolchain in Fig. 2, where we distinguish user provided input by
developers in solid boxes , from generated code or toolchain internals in dashed boxes .
   Development begins with specifying a protocol using an extended Scribble protocol description
language. Scribble is closely associated with the MPST theory [Hu 2017; Neykova and Yoshida
2019], and provides a user-friendly syntax for multiparty protocols. We extend the Scribble tool-
chain to support RMPST, allowing reﬁnements to be added via annotations. The extended Scribble
toolchain (as part of Session⋆ ) validates the well-formedness of the protocol, and produces a rep-
resentation in the form of a communicating ﬁnite state machine (CFSM, [Brand and Zaﬁropulo
1983]) for a given participant.
   We then use a code generator (also as part of Session⋆ ) to generate F⋆ APIs from the CFSM,
utilising a number of advanced type system features available in F⋆ (explained later in § 3.1). The
generated APIs, described in detail in § 3, consist of various type deﬁnitions, and an entry point
function taking callbacks and connections as arguments.
   In our design methodology, we separate the concern of communication and program logic. The
callbacks, corresponding to program logic, do not involve communication primitives — they are in-
voked to prompt a value to be sent, or to process a received value. Separately, developers provide a
connection that allows base types to be serialised and transmitted to other participants. Developers
implement the endpoint by providing both callbacks and connections, according to the generated
reﬁnement typed APIs. They can run the protocol by invoking the generated entry point. Finally,
the F⋆ source ﬁles can be veriﬁed using the F⋆ compiler, and extracted to an OCaml program (or
other supported targets) for eﬃcient execution.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Statically Verified Refinements for Multiparty Protocols                                                      1:5

 1    global protocol HigherLower(role A, role B, role C) {
 2      // A tells B a secret number `n0`,
 3      // and the number `t0` of attempts that C has to guess it
 4      start(n0:int) from A to B; @'0≤n0<100'
 5      limit(t0:int) from A to B; @'0<t0'
 6      do Aux(A, B, C);             @'B[n0, t0]' }
 7    aux global protocol Aux(role A, role B, role C) @'B[n:int{0≤n<100}, t:int{0<t}]' {
 8      guess(x:int)             from C to B;      @'0≤x<100'         // Next guess by C
 9      choice at B { higher() from B to C;        @'n>x ∧ t>1'       // Secret is higher
10                      higher() from B to A;
11                      do Aux(A, B, C);           @'B[n, t-1]'
12             } or { win()      from B to C;      @'n=x'              // C wins, A loses
13                      lose()   from B to A;
14             } or { lower() from B to C;         @'n<x ∧ t>1'       // Secret is lower
15                      lower() from B to A;
16                      do Aux(A, B, C);           @'B[n, t-1]'
17             } or { lose()     from B to C;      @'n,x ∧ t=1'       // A wins, C loses
18                      win()    from B to A;
19    }        }

                  Fig. 3. A Refined Scribble Global Protocol for a HigherLower Game.

2.2   Global Protocol Specification — RMPST in Extended Scribble
The workﬂow in the standard MPST theory [Honda et al. 2008], as is generally the case in dis-
tributed application development, starts from identifying the intended protocol for participant
interactions. In our toolchain, a global protocol—the description of the whole protocol between
all participants from a bird eye’s view—is speciﬁed using our RMPST extension of the Scribble
protocol description language [Hu 2017; Scribble Authors 2015]. Figure 3 gives the global protocol
for a three-party game, HigherLower , which we use as a running example.
   Basic Scribble/MPST. We ﬁrst explain basic Scribble (corresponding to the standard MPST)
without the @-annotations (annotations are extensions to the basic Scribble).
(1) The main protocol HigherLower declares three roles A, B and C, representing the runtime com-
    munication session participants. The protocol starts with A sending B a start message and a
    limit message, each carrying an int payload.
(2) The do construct speciﬁes all three roles to proceed according to the (recursive) Aux sub-protocol.
    C sends B a guess message, also carrying an int. (The aux keyword simply tells Scribble that
    a sub-protocol does not need to be veriﬁed as a top-level entry protocol.)
(3) The choice at B construct speciﬁes at this point that B should decide (make an internal choice)
    by which one of the four cases the protocol should proceed. This decision is explicitly commu-
    nicated (as an external choice) to A and C via the messages in each case. The higher and lower
    cases are the recursive cases, leading to another round of Aux (i.e. another guess by C); the
    other two cases, win and lose, end the protocol.
To sum up, A sends B two numbers, and C sends a number (at least one) to B for as long as B
replies with either higher or lower to C (and A). Next we demonstrate how we can express data
dependencies using reﬁnements with our extended Scribble.
  Extended Scribble/RMPST. As described above, a basic global protocol (equivalent to a stand-
ard MPST global type) speciﬁes the structure of participant interactions, but is not very informative

                            Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:6      Fangyi Zhou, Francisco Ferreira, Raymond Hu, Rumyana Neykova, and Nobuko Yoshida

about the behaviour of the application in the aspect of data transmitted. This limitation can be con-
trasted against standardised (but informal) speciﬁcations of real-world application protocols, e.g.
HTTP, OAuth, where a signiﬁcant part, if not the majority, of the speciﬁcation is devoted to the
data side of the protocol. It goes without saying, details missing from the speciﬁcation cannot be
veriﬁed on an implementation.
   We go through Fig. 3 again, this time including the practical extensions proposed by this pa-
per to address these limitations: RMPST enables a reﬁnement type–based treatment of protocols,
capturing and integrating both data constraints and interactions. While reﬁnement types by them-
selves can already greatly enrich the speciﬁcation of individual messages, the most valuable and
interesting aspect is the interplay between data reﬁnements and the consequent interactions (i.e.
the protocol ﬂow) in the distributed, multiparty setting. In our setup, we allow data-dependent
reﬁnements to be speciﬁed in the global protocol, we explain various ways of using them in the
running example:
• Message Values. A basic use of reﬁnements is on message values, speciﬁcally their payload
  contents. The annotation on the ﬁrst interaction (Line 4) speciﬁes that A and B not only com-
  municate an n0:int, but that 0≤n0<100 is a postcondition for the value produced by A and a
  precondition on the value received by B. Similarly, the int carried by limit must be positive.
• Local Protocol State. RMPST also supports reﬁnements on the recursions that a protocol trans-
  itions through. The B[...] annotation (Line 7) in the Aux header speciﬁes the local state known
  by B during the recursion, whenever B reaches this point in the ongoing protocol. The local state
  includes an int n such that 0≤n<100 and an int t such that 0<t. These extra variables are avail-
  able for all enactments of this subprotocol. That is, on the ﬁrst entry from HigherLower , where
  the do annotation B[n0, t0] (Line 6) speciﬁes the initial values; and from the recursive entries
  (Line 11).
  By known state, we mean that B will have access to the exact values at runtime, although stat-
  ically we can only be sure that they lie within the intervals speciﬁed in the reﬁnements. Other
  session participants can only use the type information, without knowing the value, e.g. C does
  not know the exact value of n (which is the main point of this game), but knows the range via
  the reﬁnements, and hence the endpoint may utilise this knowledge for reasoning.
• Protocol Flow. As mentioned, RMPST combines protocol speciﬁcations with reﬁnements in
  order to direct the ﬂow of the protocol — speciﬁcally at internal choices. The annotation on the
  win interaction (Line 12) from B to C speciﬁes that B can only send this message, and thus select
  this choice case, after a correct guess by C. Similarly, B can only select the other cases after an
  incorrect guess: lose (Line 17) when C is on its last attempt, or the corresponding higher (Line 9)
  or lower (Line 14) cases otherwise. We exploit the fact that a reﬁnement type can be uninhabited
  due to the impossibility to satisfy the constraint on the type, to encode protocol ﬂow conditions.
   Reﬁnements allow a basic description of an interaction structure to be elaborated into a more
expressive application speciﬁcation. Note the t>1 in the higher and lower reﬁnements are neces-
sary to ensure that the 0<t in the Aux reﬁnement is satisﬁed, given that the do annotations specify
Aux to be recursively enacted with t-1. Albeit simple, the protocol shows how we can use reﬁne-
ments in various means to express data and control ﬂow dependencies and recursive invariants in
a multiparty setup. Once the protocol is speciﬁed, our toolchain allows the reﬁnements in RMPST
to be directly mapped to data reﬁnements in F* through a callback-styled API generation.

3     IMPLEMENTING REFINED PROTOCOLS IN F⋆
In this section, we demonstrate our callback-styled, reﬁnement-typed APIs for implementing en-
dpoints in F⋆ [Swamy et al. 2016]. We introduced earlier the workﬂow of our toolchain (§ 2.1).

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Statically Verified Refinements for Multiparty Protocols                                                                1:7

In § 3.1, we summarise the key features of F⋆ utilised in our implementation. Using our running
example, we explain the generated APIs in F⋆ in § 3.2, and how to implement endpoints in § 3.3.
We outline the function we generate for executing the endpoint in § 3.4.
   Developers using Session⋆ implement the callbacks in F⋆ , to utilise the functionality of reﬁne-
ment types provided by the F⋆ type-checker. The F⋆ compiler can verify statically whether the
provided implementation by the developer satisﬁes the reﬁnements as speciﬁed in the protocol.
The veriﬁed code can be extracted via the F⋆ compiler to OCaml and executed.
   The veriﬁed implementation enjoys properties both from the MPST theory, such as session ﬁdel-
ity and deadlock freedom, but also from reﬁnement types, that the data dependencies are veriﬁed
to be correct according to the protocol. Additional details on code generation can be found in
Appendix B.

3.1    Targeting F⋆ and Implementing Endpoints
F⋆ [Swamy et al. 2016] is a veriﬁcation-oriented programming language, with a rich set of features.
Our method of API generation and example programs utilise the following F⋆ features:1
• Reﬁnement Types. A reﬁnement type has the form x:t{E}, where t is the base type, x is a
  variable that stands for values of this type, and E is a pure2 boolean expression for reﬁnement,
  possibly containing x. In short, the values of this reﬁnement type are the subset of values of t
  that make E evaluate to true, e.g. natural numbers are deﬁned as x:int{x≥0}. We use this feature
  to express data and control ﬂow constraints in protocols.
  In F⋆ , type-checking reﬁnement types are done with the assistance of the Z3 SMT solver [De Moura and Bjør
  2008]. Reﬁnements are encoded into SMT formulae and the solver decides the satisﬁability of
  SMT formulae during type-checking. This feature enables automation in reasoning and saves
  the need for manual proofs in many scenarios.
• Indexed Types. Types can take pure expressions as arguments. For example, a declaration
  type t (i:t') = ... prescribes the family of types given by applying the type constructor t
  to values of type t'. We use this feature to generate type deﬁnitions for payload items in an
  internal choice, where the reﬁnements in payload types refer to a state type.
• Dependent Functions with Eﬀects. A (dependent) function in F⋆ has a type of the form
  (x:t1 ) → E t2 , where t1 is the argument type, E describes the eﬀect of the function, and t2
  is the result type, which may also refer to the argument x.
  The default eﬀect is Tot, for pure total expressions (i.e. terminating and side-eﬀect free). At the
  other end of the spectrum is the arbitrary eﬀect ML (correspondent to all possible side eﬀects in
  an ML language), which permits state mutation, non-terminating recursion, I/O, exceptions, etc.
• The Ghost Eﬀect and the erased Type. A type can be marked erased in F⋆ , so that values
  of such types are not available for computation (after extracting into target language), but only
  for proof purposes (during type-checking). The type constructor is accompanied with the Ghost
  eﬀect to mark computationally irrelevant code, where the type system prevents the use of erased
  values in computationally relevant code, so that the values can really be safely erased. In the
  following snippet, we quickly demonstrate this feature: GTot stands for Ghost and total, and
  cannot be mixed with the default pure eﬀect (the function not_allowed does not type-check).
  We use the erased type to mark variables known to the endpoint via the protocol speciﬁcation,
  whose values are not known due to not being a party of the message interaction. For example,
  in Fig. 3, the endpoint C does not know the value of n0, but knowns its type from the protocol.

1 A comprehensive F⋆ tutorial is available at https://www.fstar-lang.org/tutorial/.
2 Pure in this context means pure terminating computation, i.e. no side-eﬀects including global state modifcations, I/O

actions or inﬁnite recursions, etc.


                                      Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:8       Fangyi Zhou, Francisco Ferreira, Raymond Hu, Rumyana Neykova, and Nobuko Yoshida

1     type t = { x1: int;                  1              (* The following access is not allowed *)
2                x2: erased int; }         2              let not_allowed (o: t) = reveal o.x2
3     (* Definition in standard library *) 3              (* Accessing at type level is allowed *)
4     val reveal: erased a → GTot a        4              val allowed: (o: t{reveal o.x2 ≥ 0}) → int
   Our generated code consists of multiple type deﬁnitions and an entry point function (as shown
in Fig. 2, F⋆ API), including:
State Types: Allowing developers to access variables known at a given CFSM state.
Callbacks: A record of functions corresponding to CFSM transitions, used to implement program
 logic of the local endpoint.
Connections: A record of functions for sending and receiving values to and from other roles in
 the global protocol, used to handle the communication aspects of the local endpoint.
Entry Point: A function taking callbacks and connections to run the local endpoint.
   To implement an endpoint, the developer needs to provide implementations for the generated
callback and connection types, using appropriate functions to handle the program logic and com-
munications. The F⋆ compiler checks whether the implemented functions type-check against the
prescribed types. If the endpoint implementation succeeds the type-checking, the developer may
choose to extract to a target language (e.g. OCaml, C) for execution.

3.2   Projection and F⋆ API Generation – Communicating Finite State Machine–based
      Callbacks for Session I/O
As in the standard MPST workﬂow, the next step (Fig. 2) is to project our reﬁned global protocol
onto each role. This decomposes the global protocol into a set of local protocols, prescribing the
view of the protocol from each role. Projection is the deﬁnitive mechanism in MPST: although
all endpoints together must comply to global protocol, projection allows each endpoint to be sep-
arately implemented and veriﬁed, a key requirement for practical distributed programming. As
we shall see, the way projection treats reﬁnements—we must consider the local knowledge of val-
ues propagated through the multiparty protocol—is crucial to verifying reﬁned implementations,
including our simple running example.
   Projection onto B. We ﬁrst look at the projection onto B: although it is the largest of the three
projections, it is unique among them because B is involved in every interaction of the protocol, and
(consequently) B has explicit knowledge of the value of every reﬁnement variable during execution.
   Formally, projection is deﬁned as a syntactic function (explained in detail later in § 4.3); it is a par-
tial function, designed conservatively to reject protocols that are not safely realisable in asynchron-
ous distributed settings. However, we show in Fig. 4a the representation of projections employed in
our toolchain based on communicating ﬁnite state machines (CFSMs) [Brand and Zaﬁropulo 1983],
where the transitions are the localised I/O actions performed by B in this protocol. Projected CFSM
actions preserve their reﬁnements: as before, an action reﬁnement serves as a precondition for an
output transition to be ﬁred, and a postcondition when an input transition is ﬁred. For example,
A?start(n 0 ){0 ≤ n 0 < 100} is an input of a start message from A, with a reﬁnement on the int
payload value. Similarly, C!higher{n > x ∧ t > 1} expresses a protocol ﬂow reﬁnement on an
output of a higher message to C. For brevity, we omit the payload data types in the CFSM edges,
as this example features only ints; we omit empty payloads “()” likewise.
   We show the local state reﬁnements as annotations on the corresponding CFSM states (shaded
in grey, with an arrow to the state).
  Reﬁned API Generation for B. CFSMs oﬀer an intuitive understanding of the semantics of end-
point projections. Building on recent work [Castro et al. 2019; Hu and Yoshida 2016; Neykova et al.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Statically Verified Refinements for Multiparty Protocols                                                        1:9

                           n{0 ≤ n < 100}, A!higher 5 C!higher{n > x ∧ t > 1}      7    A!lose
A?start(n0 ){0 ≤ n0 < 100} t {0 < t }                                    C!win{n = x}
                                          C?guess(x){0 ≤ x < 100}
      1                2              3                           4
                                                                        C!lose{n , x ∧ t = 1}
                    A?limit(t0 ){0 ≤ t0 }
                                          A!lower   6 C!lower{n < x ∧ t > 1}       8     A!win

(a) CFSM Representation of the Projection. ! stands for sending actions, and ? for receiving actions on edges.
     Generated F⋆ API                                                       type s4Cases (s:s4) =
     State Edge       Generated Callback Type                               | s4_lower of
     1     A?start    s1 → (n:int{0≤n<100}) → ML unit                         unit{s.n<s.x ∧ s.t>1}
     2     A?limit    s2 → (t:int{0<t}) → ML unit
                                                                            | s4_lose of
     3     C?guess    s3 → (x:int{0≤x}) → ML unit
                                                                              unit{s.n,s.x ∧ s.t=1}
     4     [multiple] (s:s4) → ML (s4Cases s)
     5     A!higher s5 → ML unit                                            | s4_win of unit{s.n=s.x}
     6     A!lower    s6 → ML unit                                          | s4_higher of
     7     A!lose     s7 → ML unit                                            unit{s.n>s.x ∧ s.t>1}
     8     A!win      s8 → ML unit
                                                                           (c) Generated Data Type for the
                   (b) Generated I/O Callback Types                        Output Choice
                      Fig. 4. Projection and F⋆ API Generation for B in HigherLower

2018], we use our CFSM-based representation of reﬁned projections to generate protocol- and role-
speciﬁc APIs for implementing each role in F⋆ . We highlight a novel and crucial development:
we exploit the approach of type generation to produce functional-style callback-based APIs that
internalise all of the actual communication channels and I/O actions. In short, the transitions of
the CFSM are rendered as a set of transition-speciﬁc function types to be implemented by the user
— each of these functions take and return only the user-level data related to I/O actions and the
running of the protocol. The transition function of the CFSM itself is embedded into the API by
the generation, exporting a user interface to execute the protocol by calling back the appropriate
user-supplied functions according to the current CFSM state and I/O event occurrences.
   We continue with our example, Fig. 4b lists the function types for B, detailed as follows. Note, a
characteristic of MPST-based CFSMs is that each non-terminal state is either input- or output-only.
• State Types. For each state, we generate a separate type (named by enumerating the states, by
  default). Each is deﬁned as a record containing previously known payload values and its local
  recursion variables, or unit if none, for example:
                 
      type s3 =      n0: int{0≤n0<100}; t0: int{0<t0}; n: int{0≤n<100}; t: int{0<t}
• Basic I/O Callbacks. For each input transition we generate a function type s → σ → ML unit,
  where s is the predecessor state type, and σ is the reﬁned payload type received. The return type
  is unit and the function can perform side eﬀects, i.e. the callback is able to modify global state,
  interact with the console, etc, instead of merely pure computation. If an input transition is ﬁred
  during execution, the generated runtime will invoke a user-supplied function of this type with
  the appropriately populated value of s, including any payload values received in the message
  that triggered this transition. Note, any data or protocol reﬁnements are embedded into the types
  of these ﬁelds.
  Similarly, for each transition of an output state with a single outgoing transition, we generate a
  function type s → ML τ , where τ is the reﬁned type for the output payload.
• Internal Choices. For each output state with more than 1 outgoing transition, we generate an
  additional sum type ρ with the cases of the choice, e.g. Fig. 4c. This sum type (i.e. s4Cases) is

                              Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:10     Fangyi Zhou, Francisco Ferreira, Raymond Hu, Rumyana Neykova, and Nobuko Yoshida

  indexed by the corresponding state type (i.e. s) to make any required knowledge available for
  expressing the protocol ﬂow reﬁnement of each case. Its constructors indicate the label of the
  internal choice.
  We then generate a single function type for this state, s → ML ρ: the user implementation selects
  which choice case to follow by returning a corresponding ρ value, under the constraints of
  any reﬁnements. For example, a s4_win value can only be constructed, thus this choice case
  only be selected, when s.n=s.x for the given s. The state machine is advanced according to the
  constructor of the returned value (corresponding to the label of the message), and the generated
  runtime sends the payload value to the intended recipient.
   An asynchronous output event, i.e. the trigger for the API to call back an output function, re-
quires the communication medium to be ready to accept the message (e.g. there is enough memory
in the local output buﬀer). For simplicity, in this work we consider the callbacks of an output state
to always be immediately ﬁreable. Concretely, we delegate these concerns to the underlying lib-
raries and runtime system.
   Projection and API Generation for C. The projection onto C raises an interesting question
related to the reﬁnement of multiparty protocols: how should we treat reﬁnements on variables
that the target role does not itself know? C does not know the value of the secret n (otherwise this
game would be quite boring), but it does know that this information exists in the protocol and is
subject to the speciﬁed reﬁnement. In standard MPST, it is essentially the main point of projection
that interactions not involving the target role can be simply (and safely) dropped outright; e.g. the
communication of the start message would simply not appear in the projection of C. However,
naively taking the same approach in RMPST would be inadequate: although the target role may
not know some exact value, the role may still need the associated “latent information” to fulﬁl the
desired application behaviour.
   Our framework introduces a notion of erased variables for RMPST — in short, our projection
does drop third-party interactions, but retains the latent information as reﬁnement-typed erased
variables, as illustrated by the annotation on state 1 in Fig. 5a. Thanks to the SMT-based reﬁnement
type system of F⋆ , the type-checker can still take advatange of the reﬁned types of erased vari-
ables to prove properties of the endpoint implementation; however, these variables cannot actually
be used computationally in the implementation (since their values are not known). Conveniently,
F⋆ supports erased types (described brieﬂy in § 3.1), and provides ways (i.e. Ghost eﬀects) to en-
sure that such variables are not used in the computation. We demonstrate this for our example
in the next subsection. Our approach can be considered a version of irrelevant variables from
[Abel and Scherer 2012; Pfenning 2001] for the setting of typed, distributed interactions.

3.3 F⋆ Implementation – Protocol Validation and Verification by Refinement Types
Finally, the generated APIs—embodying the reﬁned projections—are used to implement the end-
point processes. As mentioned, the user implements the program logic as callback functions of
the generated (reﬁnement) types, supplied to the entry point along with code for establishing the
communication channels between the session peers. Assuming a record callbacks containing the
required functions (static typing ensures all are covered), Fig. 6a bootstraps a C endpoint.
   The API takes care of endpoint execution by monitoring the channels, and calling the appropri-
ate callback based on the current protocol state and I/O event occurrences. For example, a minimal,
well-typed implementation of B could comprise the internal choice callback above (Fig. 6b) (im-
plementing the type in Fig. 4c), cf. state 4, and an empty function for all others (i.e. fun _ → ()).
We can highlight how protocol violations are ruled out by static reﬁnement typing, which is ulti-
mately the practical purpose of RMPST. In the above callback code, changing, say, the condition

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Statically Verified Refinements for Multiparty Protocols                                                     1:11


 n : erased int{0 ≤ n < 100}, B?higher{n > x ∧ t > 1}
 t : erased int{0 < t }                                              B?win{n = x }
                              B!guess(x){0 ≤ x < 100}
                        1                                        2
                                                               B?lose{n , x ∧ t = 1}
                              B?lower{n < x ∧ t > 1}

                              (a) CFSM Representation of the Projection
                                                         User implementation
                                                             (* Allocate a refined int reference *)
 State   Edge       Generated type                           let next: ref (x:int{0≤x<100}) = alloc 50
 1       B!guess    s1 → ML (x:int{0 ≤x<100})                fun _ → !next (*Deref next*)
 2       B?higher   s2 → unit{n>x ∧ t>1} → ML unit           fun s → next ≔ s.x + 1
         B?lower    s2 → unit{n<x ∧ t>1} → ML unit           fun s → next ≔ s.x - 1
         B?win      s2 → unit{n=x} → ML unit                 fun _ → ()
         B?lose     s2 → unit{n,x ∧ t=1} → ML unit           fun _ → ()

                                   (b) Generated I/O Callback Types
                    Fig. 5. Projection and F⋆ API Generation for C in HigherLower
 let main () =                                        (* Signature (s:s4) → ML (s4Cases s) *)
   (* connect to B via TCP *)                         fun (s:s4) →
   let server_B = connect ip_B port_B in                (* Win if guessed number is correct *)
   (* Setup connection from TCP *)                      if s.x=s.n then s4_win ()
   let conn = mk_conn server_B in                       (* Lose if running out of attempts *)
   (* Invoke the Entry Point `run` *)                   else if s.t=1 then s4_lose ()
   let () = run callbacks conn in                       (* Otherwise give hints accordingly *)
   (* Close TCP connection *)                           else if s.n>s.x then s4_higher ()
   close server_B                                       else s4_lower ()
            (a) Running the Endpoint C                    (b) Implementing the Internal Choice for B
                         Fig. 6. Selected Snippets of Endpoint Implementation
for the lose case to s.t=0 would directly violate the reﬁnement on the s4_lose constructor, cf.
Fig. 4c. Omitting the lose case altogether would break both the lower and higher cases, as the type
checker would not be able to prove s.t>1 as required by the subsequent constructors.
   Lastly, Fig. 5b implements C to guess the secret by a simple search, given we know its value is
bounded within the speciﬁed interval. We draw attention to the input callback for higher, where
we adjust the next value. Given that the value being assigned is one more than the existing value,
it might have been the case that the new value falls out of the range (in the case where next is
99), hence violating the prescribed type. However, despite that the value of n is unknown, we have
known from the reﬁnement attached to the edge that n>x holds, hence it must have been the case
that our last guess x is strictly less than the secret n, which rules out the possibility that x can be
99 (the maximal value of n). Had the reﬁnement and the erased variable not been present, the type-
checker would not be able to accept this implementation, and it demonstrates that our encoding
allows such reasoning with latent information from the protocol.
   Moreover, the type and eﬀect system of F⋆ prevents the erased variables from being used in
the callbacks. On one hand, int and erased int types are not compatible, because they are not the
same type. This prevents an irrelevant variable from being used in place of a concrete variable. On
the other hand, the function reveal converts a value of erased 'a to a value of 'a with Ghost eﬀect.
A function with Ghost eﬀect cannot be mixed with a function with ML eﬀect (as in the case of our
callbacks), so irrelevant variables cannot be used in the implementation via the reveal function.

                            Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:12     Fangyi Zhou, Francisco Ferreira, Raymond Hu, Rumyana Neykova, and Nobuko Yoshida

  Interested readers are invited to try the running example out with our accompanying artifact.
We propose a few modiﬁcations on the implementation code and the protocol, and invite the read-
ers to observe errors when implementations no longer correctly conforms to the prescribed pro-
tocol.

3.4    Executing the Communicating Finite State Machine (Generated Code)
As mentioned earlier, our API design sepearates the concern of program logic (with callbacks) and
communication (with connections). A crucial piece of the generated code involves threading the
two parts together — the execution function performs the communications actions and invokes the
appropriate callbacks for handling. In this way, we do not expose explicit communication channels,
so linearity can be achieved with ease by construction in our generated code.
   The entry point function, named run, takes callbacks and connections as arguments, and ex-
ecutes the CFSM for the speciﬁed endpoint. The signature uses the permissive ML eﬀect, since
communicating with the external world performs side eﬀects. We traverse the states (the set of
states is denoted Q) in the CFSM and generate appropriate code depending on the nature of the
state and its outgoing transitions.
   Internally, we deﬁne mutually recursive functions for each state q ∈ Q, named runq , taking the
state record nqo as argument (nqo stands for the state record for a given state q), which performs
the required actions at state q. The run state function for a state q either (1) invokes callbacks
and communication primitives, then calls the run state function for the successor state q ′ , or (2)
returns directly for termination if q is a terminal state (without outgoing transitions). The main
entry point invokes the run function for the initial state q 0 , starting the ﬁnite state machine.
   The internal run state functions are not exposed to the developer, hence it is not possible to
tamper with the internal state with usual means of programming. This allows us to guarantee
linearity of communication channels by construction. In the following text, we outline how to run
each state, depending on whether the state is a sending state or a receiving state. Note that CFSMs
constructed from local types do not have mixed states [Deniélou and Yoshida 2013, Prop. 3.1]

let rec run_q (st: stateq) =                      let rec run_q (st: stateq) =
  let choice = callbacks.stateq_send st             let label = comm.recv_string p () in
  in match choice with                              match label with
  | Choiceqli payload →                             | "li " →
    comm.send_string q "li ";                         let payload = comm.recv_S p () in
                                         Repeat
    comm.send_S q payload;                            callbacks.stateq_receive_li st payload;
                                        for i ∈ I
    let st = { · · · ; xi =payload } in               let st = { · · · ; xi =payload } in
    run_q ′ st                                        run_q ′ st

          (a) Template for Sending State q                             (b) Template for Receiving State q
                                             Fig. 7. Template for runq

   Running the CFSM at a Sending State. For a sending state q ∈ Q, the developer makes an
internal choice on how the protocol proceeds, among the possible outgoing transitions. This is
done by invoking the sending callback stateq_send with the current state record, to obtain a
choice with the associated payload. We pattern match on the constructor of the label li of the
message, and ﬁnd the corresponding successor state q ′ .
   The label li is encoded as a string and sent via the sending primitive to q. It is followed by the
payload speciﬁed in the return value of the callback, via corresponding sending primitive according
to the base type with reﬁnement erased.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Statically Verified Refinements for Multiparty Protocols                                                     1:13

    We construct a state record of nq ′ o from the existing record nqo, adding the new ﬁeld x i in
the action using the callback return value. In the case of recursive protocols, we also update the
recursion variable according to the deﬁnition in the protocol when constructing nq ′ o. Finally, we
call the run state function runq ′ to continue the CFSM, eﬀectively making the transition to state
q ′.
    Following the procedure, runq is generated as shown in Fig. 7a.

   Running the CFSM at a Receiving State. For a receiving state q ∈ Q, how the protocol pro-
ceeds is determined by an external choice, among the possible outgoint actions. To know what
choice is made by the other party, we ﬁrst receive a string and decode it into a label l, via the
receiving primitive for string.
   Subsequently, according to the label l, we can look up the label in the possible transitions, and
ﬁnd the state successor q ′ . By invoking the appropriate receiving primitive, we obtain the payload
value. We note that the receiving primitive has a return type without reﬁnements. In order to re-
attach the reﬁnements, we use the F⋆ builtin assume to reinstate the reﬁnements according to the
protocol before using the value.
   According the label l received, we can call the corresponding receiving callback with the re-
ceived value. This allows the developer to process the received value and perform any relevant
program logic. This is followed by the same procedure for constructing the state record for the
next state q ′ and invoking the run function for q ′ .
   Following the procedure, runq is generated as shown in Fig. 7b.

3.5   Summary
We demonstrated with our running example, HigherLower , how to implement a reﬁned multiparty
protocol with our toolchain Session⋆ .
   Exploiting the powerful type system of F⋆ , our approach has several key beneﬁts: First, it guar-
antees fully static session type safety in a lightweight, practical manner — the callback-style API is
portable to any statically typed language. Existing work based on code generation has considered
only hybrid approaches that supplement static typing with dynamically checked linearity of expli-
cit communication channel usages. Moreover, the separation of program logic and communication
leads to a modular implementation of protocols.
   Second, it is well suited to functional languages like F⋆ ; in particular, the data-oriented nature
of the user interface allows the reﬁnements in RMPST to be directly mapped to data reﬁnements
in F⋆ , allowing the reﬁnements constraints to be discharged at the user implementation level by
the F⋆ compiler — again, fully statically.
   Furthermore, our endpoint implementation inherits core communication safety properties such
as freedom from deadlock or communication mismatches, based on the original MPST theory. We
use the F⋆ type-checker to validate statically that an endpoint implementation is correctly typed
with respect to the prescribed type obtained via projection of the global protocol. Therefore, the
implementation beneﬁts from additional guarantees from the reﬁnement types.

4 A THEORY OF REFINED MULTIPARTY SESSION TYPES (RMPST)
In this section, we introduce reﬁned multiparty session types (RMPST for short). We give the syntax
of types in § 4.1, extending original multiparty session types (MPST) with reﬁnement types. We
describe the reﬁnement typing system that we use to type expressions in RMPST in § 4.2.
   We follow the standard MPST methodology. Global session types describe communication struc-
tures of many participants (also known as roles). Local session types, describing communication

                            Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:14     Fangyi Zhou, Francisco Ferreira, Raymond Hu, Rumyana Neykova, and Nobuko Yoshida

structures of a single participant, can be obtained via projection (explain in § 4.3). Endpoint pro-
cesses implement local types obtained from projection. We give semantics of global types and
local types in § 4.4, and show the equivalence of semantics with respect to projection. As a con-
sequence, we can compose all endpoint processes implementing local types for roles in a global
type, obtained via projection, to implement the global type correctly.

4.1    Syntax of Types
We deﬁne the syntax of reﬁned multiparty session types (reﬁned MPST) in Fig. 8. We use diﬀerent
colours for diﬀerent syntactical categories to help disambiguation, but the syntax can be under-
stood without colours. We use pink for global types, dark blue for local types, blue for expressions,
purple for base types, indigo for labels, and Teal with bold fonts for participants.

  S ::= int | bool | . . .             Base Types
                                                                   L   ::=                               Local Types
  T ::= x : S {E}                      Reﬁnement Types
                                                                         |   p&{li (x i :Ti ).Li }i ∈I   Receiving
  E ::= x | n | op1 E | E op2 E . . . Expressions
                                                                         |   p⊕{li (x i :Ti ).Li }i ∈I   Sending
  G ::=                                Global Types
                                                                         |   l(x :T ).L                  Silent Preﬁx
      | p → q {li (x i :Ti ).G i }i ∈I Message
                                                                         |   µt (x :T )hx := Ei.L        Recursion
      | µt(x :T )hx := Ei.G            Recursion
                                                                         |   thx := Ei | end             Type Var., End
      | thx := Ei | end                Type Var., End

                               Fig. 8. Syntax of Refined Multiparty Session Types

   Value Types and Expressions. We use S for base types of values, ranging over integers, booleans,
etc. Values of the base types must be able to be communicated.
   The base type S can be reﬁned by a boolean expression, acting as a predicate on the members
of the base type. A reﬁnement type is of the form (x : S {E}). A value x of the type has base type
S, and is reﬁned by a boolean expression E. The boolean expression E acts as a predicate on the
members x (possibly involving the variable x). For example, we can express natural numbers as
(x : int{x ≥ 0}). We use fv(·) to denote the free variables in reﬁnement types, expressions, etc. We
consider variable x be bound in the reﬁnement expression E, i.e. fv(x : S {E}) = fv(E) \ {x }.
   Where there is no ambiguity, we use the base type S directly as an abbreviation of a reﬁnement
type (x : S {true}), where x is a fresh variable, and true acts as a predicate that accepts all values.
  Global Session Types. Global session types (global types or protocols for short) range over G, G ′, G i , . . .
Global types give an overview of the overall communication structure. We extend the standard
global types [Deniélou and Yoshida 2013] with reﬁnement types and variable bindings in message
preﬁxes. Extensions
          n         to the
                        o syntax are shaded in the following explanations.
    p → q li ( x i : Ti ).G i i ∈I is a message from p to q, which branches into one or more continu-
ations with label li , carrying a payload variable x i with type Ti . We omit the curly braces when
there is only one branch, like p → q : l(x :T ). We highlight the diﬀerence from the standard syn-
tax, i.e. the variable binding. The payload variable x i occurs bound in the continuation global type
G i , for all i ∈ I . We sometimes omit the variable if it is not used in the continuations. The free
variables are deﬁned as:                                     Ø           Ø
                       fv(p → q {li (x i :Ti ).G i }i ∈I ) =   fv(Ti ) ∪   (fv(G i ) \ {x i })
                                                            i ∈I             i ∈I
We require that the index set I is not empty, and all labels li are distinct. To prevent duplication, we
write l(x : S {E}) instead of l(x : (x : S {E})) (the ﬁrst x occurs as a variable binding in the message,
the second x occurs as a variable representing member values in the reﬁnement types).

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Statically Verified Refinements for Multiparty Protocols                                                      1:15

   We extend the construct of recursive protocols to include a variable carrying a value in the inner
protocol. In this way, we enhance the expressiveness of the global types by allowing a recursion
variable to be maintained across iterations of global protocols.
   The recursive global type µt( x :T )h x := E i.G speciﬁes a variable x carrying type T in the
recursive type, initialised with expression E. The type variable th x := E i is annotated with an
assignment of expression E to variable x. The assignment updates the variable x in the current
recursive protocol to expression E. The free variables in recursive type is deﬁned as
                        fv(µt(x :T )hx := Ei.G) = fv(T ) ∪ fv(E) ∪ (fv(G) \ {x })
   We require that recursive types are contractive [Pierce 2002, §21], so that recursive protocols
have at least a message preﬁx, and protocols such as µt(x :T )hx := E 1 i.thx := E 2 i are not allowed.
We also require recursive types to be closed with respect to type variables, e.g. protocols such as
thx := Ei alone are not allowed.
   We write G[µt(x :T ).G/t] to substitute all occurrences of type variables with expressions thx := Ei
into µt(x :T )hx := Ei.G. We write r ∈ G to say r is a participating role in the global type G.
  Example 4.1 (Global Types). We give the following examples of global types.
  (1) G 1 = A → B : Fst (x : int).B → C : Snd(y : int{x = y}).C → D : Trd(z : int{x = z}).end.
      G 1 describes a protocol where A sends an int to B, and B relays the same int to C, similar
      for C to D. Note that we can write x = z in the reﬁnement of z, whilst x is not known to C.
                                                                           
                                              Positive(unit{x > 0}).end 
                                              
                                                                           
                                                                            
  (2) G 2 = A → B : Number (x : int).B → C Zero(unit{x = 0}).end
                                              
                                               N eдative(unit{x < 0}).end 
                                                                           
      G 2 describes a protocol where A sends an int to B, and B tells C whether the int is positive,
      zero, or negative. We omit the variable here since it is not used later in the continuation.
  (3) G 3 = µt(try : int{try ≥ 0 ∧ try ≤ 3})htry := 0i.
            A → B : Password(pwd : string).
                     
                     Correct (unit).end                 
                                                         
                     
                                                        
                                                         
            B → A Retry(unit{try < 3}).thtry := try + 1i
                     
                     Denied(unit{try = 3}).end          
                                                         
                                                        
      G 3 describes a protocol where A authenticates with B with maximum 3 tries.
   Local Session Types. Local session types (local types for short) range over L, L ′, Li , . . . Local
types give a view of the communication structure of an endpoint, usually obtained from a global
type. In addition to standard syntax, the recursive types are similarly extended as those of global
types.
   Suppose the current role is q, the local type p⊕{li (x i :Ti ).Li }i ∈I describes that the role q sends
a message to the partner role p with label li (where i is selected from an index set I ), carrying
payload variable x i with type Ti , and continues with Li . It is also said that the role q takes an
internal choice. Similarly, the local type p&{li (x i :Ti ).Li }i ∈I describes that the role q receives a
message from the partner role p. In this case, it is also said that the role q oﬀers an external choice.
We omit curly braces when there is only a single branch (as is done for global messages).
   We add a new syntax construct of l(x :T ).L for silent local types. We motivate this introduction
of the new preﬁx to represent knowledge obtained from the global protocol, but not in the form of
a message. Silent local types are useful to model variables obtained with irrelevant quantiﬁcation
[Abel and Scherer 2012; Pfenning 2001]. These variables can be used in the construction of a type,
but cannot be used in that of an expression, as we explain later in § 4.2. We show an example of a

                             Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:16      Fangyi Zhou, Francisco Ferreira, Raymond Hu, Rumyana Neykova, and Nobuko Yoshida

       [WF-Rty]                                                        [TE-Plus]
       Σ+, x : S ⊢ E : bool          [TE-Var]                                 Σ ⊢ E 1 : int       Σ ⊢ E 2 : int
                                           ω
        Σ ⊢ (x : S {E}) ty           Σ1, x :T , Σ2 ⊢ x : T             Σ ⊢ E 1 + E 2 : (v : int{v = E 1 + E 2 })
         [TE-Sub]
         Σ ⊢ E : (v : S {E 1 })      Valid(nΣo ∧ nE 1 o =⇒ nE 2 o)                  [TE-Const]

                              Σ ⊢ E : (v : S {E 2 })                                 Σ ⊢ n : (v : int{v = n})
                    Fig. 9. Selected Typing Rules for Expressions in a Local Typing Context

silent local type later in Example 4.3, after we deﬁne endpoint projection, the process of obtaining
local types from a global type.

4.2     Expressions and Typing Expressions
We use E, E ′, Ei to range over expressions. Expressions consist of variables x, constants (e.g. integer
literals n), and unary and binary operations. We use an SMT assisted reﬁnement type system for
typing expressions, in the style of [Rondon et al. 2008]. The simple syntax of expressions allows all
expressions to be encoded into SMT logic, for deciding a semantic subtyping relation of reﬁnement
types [Bierman et al. 2012].
  Typing Contexts. We deﬁne two categories of typing contexts, for use in handling global types
and local types respectively.
                          Γ ::=  | Γ, x P : T         Σ ::=  | Σ, x θ : T         θ ::= 0 | ω
 We annotate global and local typing contexts diﬀerently. For global contexts Γ, variables carry the
annotation of a set of roles P, to denote the set of roles that have the knowledge of its value.
   For local contexts Σ, variables carry the annotation of their multiplicity θ . A variable with mul-
tiplicity 0 is an irrelevantly quantiﬁed variable (irrelevant variable for short), which cannot appear
in the expression when typing (also denoted as x ÷ T in the literature [Abel and Scherer 2012;
Pfenning 2001]). Such a variable can only appear in an expression used as a predicate, when de-
ﬁning a reﬁnement type. A variable with multiplicity ω is a variable without restriction. We often
omit the multiplicity ω.
   Well-formedness. Since a reﬁnement type can contain free variables, it is necessary to deﬁne
well-formedness judgements on reﬁnement types, and henceforth on typing contexts.
   We deﬁne Σ+ to be the local typing context where all irrelevant variables x 0 become unrestricted
x , i.e. ()+ = ; (Σ, x θ :T )+ = Σ+, x ω :T .
  ω

   We show the well-formedness judgement of a reﬁnement type [WF-Rty] in Fig. 9. For a reﬁne-
ment type (x : S {E}) to be a well-formed type, the expression E must have a boolean type under
the context Σ+ , extended with variable x (representing the members of the type) with type S. The
typing context Σ+ promotes the irrelevant quantiﬁed variables into unrestricted variables, so they
can be used in the expression E inside the reﬁnement type.
   The well-formedness of a typing context is deﬁned inductively, requiring all reﬁnement types
in the context to be well-formed. We omit the judgements for brevity.
  Typing Expressions. We type expressions in local contexts, forming judgements of form
Σ ⊢ E : T , and show key typing rules in Fig. 9. We modify the typing rules in a standard reﬁnement
type system [Rondon et al. 2008; Vazou et al. 2014, 2017], adding distinction between irrelevant
and unrestricted variables.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Statically Verified Refinements for Multiparty Protocols                                                                         1:17

                    
                     Γ, x P :T            if x < Γ                                     
                                                                                         Σ, x θ :T         if x < Σ
                    
                                                                                       
                                                                                        
                                                                                       
                     Γ1 , x P :T , Γ2
                                          if Γ = Γ1 , x  :T , Γ2                       Σ1, x θ :T , Σ2
                                                                                                           if Σ = Σ1 , x 0 :T , Σ2
 Γ ∪ {x P : T } =                                                    Σ ∪ {x θ : T } =
                    
                    
                     Γ1 , x P :T , Γ2     if Γ = Γ1 , x P :T , Γ2               
                                                                                 
                                                                                  Σ1, x ω :T , Σ2          if Σ = Σ1 , x ω :T , Σ2
                    
                     undeﬁned                                                   
                                                                                  undeﬁned
                                          otherwise                                                       otherwise
                                                 Fig. 10. Typing Context Extension

  [TE-Const] gives constant values in the expression a reﬁnement type that only contains the
constant value. Similarly, [TE-Plus] gives typing derivations for the plus operator, with a corres-
ponding reﬁnement type encoding the addition.
  We draw attention to the handling of variables ([TE-Var]). An irrelevant variable in the typing
context cannot appear in an expression, i.e. there is no derivation for Σ1, x 0 :T , Σ2 ⊢ x :T . These
variables can only be used in an reﬁnement type (see [WF-Rty]).
  The key feature of the reﬁnement type system is the semantic subtyping relation decided by SMT
[Bierman et al. 2012], we describe the feature in [TE-Sub]. We use nEo to denote the encoding of
expresion E into the SMT logic. We encode a type binding x θ : (v : S {E}) in a typing context by
encoding the term E[x/v], and deﬁne the encoding of a typing context nΣo inductively.
  We deﬁne the extension of typing contexts (Γ ∪ {x P : T }; Σ ∪ {x θ : T }) in Fig. 10, used in
deﬁnitions of semantics. We say a global type G (resp. a local type L) is closed under a global
context Γ (resp. a local context Σ), if all free variables in the type are in the domain of the context.
    Remark 4.2 (Empty Type). A reﬁnement type may be empty, with no inhabited member.
    We can construct such a type under the empty context  as (x : S {false}) with any base types
S. A more speciﬁc example is a reﬁnement type for an integer that is both negative and pos-
itive (x : int{x > 0 ∧ x < 0}). Similarly, under the context x ω : int{x > 0}, the reﬁnement type
y : int{y < 0 ∧ y > x } is empty. In these cases, the typing context with the speciﬁed type becomes
inconsistent, i.e. the encoded context gives a proof of falsity.
    Moreover, an empty type can also occur without inconsistency. For instance, in a typing context
of x 0 : int, the type y : int{y > x } is empty — it is not possible to produce such a value without
referring to x (cf. [TE-Var]).

4.3   Endpoint Projection: From Global Contexts and Types to Local Contexts and Types
In the methodology of multiparty session types, developers specify a global type, and obtain local
types for the participants via endpoint projection (projection for short). In the original theory, pro-
jection is a partial function that takes a global type G and a participant p, and returns a local type
L. The resulting local type L describes a the local communication behaviour for participant p in
the global scenario. Such workﬂow has the advantage that each endpoint can obtain a local type
separately, and implement a process of the given type, hence providing modularity and scalability.
   Projection is deﬁned as a partial function, since only well-formed global types can be projected to
all participants. In particular, a partial merge operator ⊔ is used during the projection, for creating
a local type Σ ⊢ L 1 ⊔ L 2 = L merged that captures the behaviour of two local types, under context Σ.
   In RMPST, we ﬁrst deﬁne the projection of global typing contexts (Fig. 11), and then deﬁne the
projection of global types under a global typing context (Fig. 12). We use expression typing judge-
ments in the deﬁnition of projection, to type-check expressions against their prescribed types.
   Projection of Global Contexts. We deﬁne the judgement Γ ↾ p = Σ for the projection of global
typing context Γ to participant p in Fig. 11. In the global context Γ, a variable x is annotated with
the set of participants P who know the value. If the projected participant p is in the set P, [P-Var-
ω] is applied to obtain an unrestricted variable in the resulting local context; Otherwise, [P-Var-0]
is applied to obtain an irrelevant variable.

                                         Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:18      Fangyi Zhou, Francisco Ferreira, Raymond Hu, Rumyana Neykova, and Nobuko Yoshida

                                                [P-Var-ω]                                 [P-Var-0]
                          [P-Empty]                  p∈P         Γ↾p=Σ                       p<P         Γ↾p=Σ
       Γ↾p=Σ
                          ↾p=                       P
                                                Γ, x : T ↾ p = Σ, x : T    ω
                                                                                           Γ, x : T ↾ p = Σ, x 0 : T
                                                                                               P

                                   Fig. 11. Projection Rules for Global Contexts
                                                                       {p, q}
            Γ↾p=Σ             ∀i ∈ I .       Σ ⊢ Ti ty         hΓ ∪ {x i        : Ti } ≺ G i i ↾ p = hΣi ≺ Li i
 [P-Send]
                      hΓ ≺ (p → q {li (x i :Ti ).G i }i ∈I )i ↾ p = hΣ ≺ q⊕{li (x i :Ti ).Li }i ∈I i
                                                                       {p, q}
            Γ↾q=Σ             ∀i ∈ I .       Σ ⊢ Ti ty         hΓ ∪ {x i        : Ti } ≺ G i i ↾ q = hΣi ≺ Li i
 [P-Recv]
                      hΓ ≺ (p → q {li (x i :Ti ).G i }i ∈I )i ↾ q = hΣ ≺ p&{li (x i :Ti ).Li }i ∈I i
                                                                               {p, q}
            Γ↾r=Σ         r < {p, q}      ∀i ∈ I .    Σ ⊢ Ti ty     hΓ ∪ {x i           : Ti } ≺ G i i ↾ r = hΣi ≺ Li i
  [P-Phi]
                           hΓ ≺ (p → q {li (x i :Ti ).G i }i ∈I )i ↾ r = hΣ ≺ ⊔i ∈I li (x i :Ti ).Li i
                Γ↾r=Σ         r∈G        hΓ ∪ {x {r|r∈G } : T } ≺ Gi ↾ r = hΣ ′ ≺ Li            Σ ⊢ T ty    Σ ⊢ E :T
  [P-Rec-In]
                               hΓ ≺ µt(x :T )hx := Ei.G)i ↾ r = hΣ ≺ µt (x :T )hx := Ei.Li
                              Γ↾r=Σ            r<G                                                  Γ↾r=Σ
[P-Rec-Out]                                                                    [P-End]
                hΓ ≺ µt(x :T )hx := Ei.G)i ↾ r = hΣ ≺ endi                                hΓ ≺ endi ↾ r = hΣ ≺ endi
                                                          Γ ↾ r = Σ = Σ1, x :T , Σ2           Σ1, x :T , Σ2 ⊢ E :T
                                              [P-Var]
       hΓ ≺ Gi ↾ p = hΣ ≺ Li                                  hΓ ≺ thx := Eii ↾ r = hΣ ≺ thx := Eii

                                    Fig. 12. Projection Rules for Global Types

   Projection of Global Types with a Global Context. When projecting a global type G, we
include a global context Γ, forming a judgement of form hΓ ≺ Gi ↾ p = hΣ ≺ Li. Projection
rules are shown in Fig. 12. Including a typing context allows us to type-check expressions during
projection, hence ensuring that variables attached to recursive protocols are well-typed.
   If the preﬁx of G is a message from role p to role q, the projection results a local type with
a send (resp. receive) preﬁx into role p (resp. q) via [P-Send] (resp. [P-Recv]). For other roles
r, the projection results in a local type with a silent label via [P-Phi], with preﬁx l(x :T ). This
follows the concept of a coordinated distributed system, where all the processes follow a global
protocol, and base assumptions of their local actions on actions of other roles not involving them.
The projection deﬁned in the original MPST theory does not contain information for role r about
a message between p and q. We use the silent preﬁx to retain such information, especially the
reﬁnement type T of the payload. For merging two local types (as used in [P-Phi]), we use a
simple plain merge operator deﬁned as Σ ⊢ L ⊔ L = L, requiring two local types to be identical in
order to be merged.3
   If the preﬁx of G is a recursive protocol µt(x :T )hx := Ei.G, the projection preserves the recur-
sion construct if the projected role is in the inner protocol via [P-Rec-In] and that the expression
E can be typed with type T under the projected local context. Typing expressions under local
contexts ensures that no irrelevant variables x 0 are used in the expression E, as no typing deriva-
tion exists for irrelevant variables. Otherwise projection results in end via [P-Rec-Out]. If G is a
type variable thx := Ei, we similarly validate that the expression E carries the speciﬁed type in the
correspondent recursion deﬁnition, and its projection also preserves the type variable construct.
3 We build upon the standard MPST theory with plain merging. Full merge [Denielou et al. 2012], allowing certain diﬀerent

index sets to be merged, is an alternative, more permissive merge operator. Our implementation Session⋆ uses the more
permissive merge operator for better expressiveness.


Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Statically Verified Refinements for Multiparty Protocols                                                           1:19

   Example 4.3 (Projection of Global Types of Example 4.1 (1)). We draw attention to the projection
of G 1 to C, under the empty context .
       h ≺ G 1 i ↾ C = h ≺ Fst(x : int).B&Snd(y : int{x = y}).D⊕Trd(z : int{x = z}).endi
We note that the local type for C has a silent preﬁx Fst(x : int), which binds the variable x in the
continuation. The silent preﬁx adds the variable x and its type to the “local knowledge” of the
endpoint C, yet the actual value of x is unknown.
   Remark 4.4 (Empty Session Type). Global types G and local types L can be empty because one
of the value types in the protocol in an empty type (cf. Remark 4.2).
   For example, the local type A⊕Impossible(x : int{x > 0 ∧ x < 0}).end cannot be implemented,
since such an x cannot be provided.
   For the same reason, the local type Pos(x : int{x > 0}).A⊕Impossible(y : int{y > x }).end can-
not be implemented.
   Remark 4.5 (Implementable Session Types). Consider the following session type:
                                                                   
                                              Pos(unit{x > 0}).end
                     L = B&Num(x : int).B⊕                            .
                                              N eд(unit{x < 0}).end
 When the variable x has the value 0, neither of the choices Pos or N eд could be selected, as the
reﬁnements are not satisﬁed. In this case, the local type L cannot be implemented, as the internal
choice callback may not be implemented in a total way, i.e. the callback returns a choice label for
all possible inputs of integer x.4

4.4   Labelled Transition System (LTS) Semantics
We deﬁne the labelled transition system (LTS) semantics for global types and local types. We show
the trace equivalence of a global type and the collection of local types projected from the global
type, to demonstrate that projection preserves LTS semantics. The equivalence result allows us to
use the projected local types for the implementation of local roles separately. Therefore, we can
implement the endpoints in F⋆ separately, and they compose to the speciﬁed protocol.
  We also prove a type safety result that well-formed global types cannot be stuck. This, combined
with the trace equivalence result, guarantees that endpoints are free from deadlocks.
  Actions. We begin with deﬁning actions in the LTS system. We deﬁne the label in the LTS as
α ::= p → q : l(x : T ), a message from role p to q with label l carrying a value named x with
type T . We deﬁne subj(α) = {p, q} to be the subjects of the action α, namely the two roles in the
action.
   Semantics of Global Types. We deﬁne the LTS semantics of global types in Fig. 13. Diﬀerent
from the original LTS semantics in [Deniélou and Yoshida 2013], we include the context Γ in the
semantics along with the global type G. Therefore, the judgements of global LTS reduction have
               α
form hΓ ≺ Gi − → hΓ ′ ≺ G ′i.
   [G-Pfx] allows the reduction of the preﬁx action in a global type. An action, matching the
deﬁnition in set deﬁned in the preﬁx, allows the correspondent continuation to be selected. The
resulting global type is the matching continuation and the resulting context contains the variable
binding in the action.
   [G-Cnt] allows the reduction of an action that is causally independent of the preﬁx action in
a global type, here, the subjects of the action are disjoint from the preﬁx of the global type. If
4 Since we use a permissive ML eﬀect in the callback type, allowing all side eﬀects to be performed in the callback, the

callback may throw exceptions or diverge in case of unable to return a value.


                                 Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:20     Fangyi Zhou, Francisco Ferreira, Raymond Hu, Rumyana Neykova, and Nobuko Yoshida


                                                               j ∈I
            [G-Pfx]
                                                              p→q:l j (x j :T j )     {p, q}
                      hΓ ≺ p → q {li (x i :Ti ).G i }i ∈I i −−−−−−−−−−→ hΓ ∪ {x j                : Tj } ≺ G j i
                                                                                             α
                       {p, q} ∩ subj(α) =               ∀j ∈ I .hΓ ∪ {x j : Tj } ≺ G j i −
                                                                                           → hΓ ′ ≺ G j′ i
            [G-Cnt]                                              α                  
                                                                 → hΓ ′ ≺ p → q li (x i :Ti ).G i′ i ∈I i
                           hΓ ≺ p → q {li (x i :Ti ).G i }i ∈I i −
                                                                                                   α
                                                hΓ ∪ {x {r|r∈G } : T } ≺ G[µt(x :T ).G/t]i −
                                                                                           → hΓ ′ ≺ G ′i
             α                        [G-Rec]                                            α
          → hΓ ′ ≺ G ′i
  hΓ ≺ Gi −                                                                       → hΓ ′ ≺ G ′ i
                                                        hΓ ≺ µt(x :T )hx := Ei.Gi −

                                       Fig. 13. LTS Semantics for Global Types

all continuations in the global types can make the reduction of that action to the same context,
then the result context is that context and the result global type is one with continuations after
reduction. When reducing the continuations, we add the variable of the preﬁx action into the con-
text, but tagged with an empty set of known roles. This addition ensures that relevant information
obtainable from the preﬁx message is not lost when performing reduction.
   [G-Rec] allows the reduction of a recursive type by unfolding the type once.
   Example 4.6 (Global Type Reductions). We demonstrate two reduction paths for a global type
                 G = p → q : Hello(x : int{x < 0}).r → s : Hola(y : int{y > x }).end.
 Note that the two messages are not causally related (they have disjoint subjects). We have the
following two reduction paths of h ≺ Gi (omitting payload in LTS actions):
                              h ≺ Gi
            p→q:H el l o
 [G-Pfx] −−−−−−−−−→           hx {p, q} : int{x < 0} ≺ r → s : Hola(y : int{y > x }).endi
              r→s:H ol a
  [G-Pfx] −−−−−−−−→           hx {p, q} : int{x < 0}, y {r, s} : int{y > x } ≺ endi

                              h ≺ Gi
              r→s:H ol a
  [G-Cnt] −−−−−−−−→           hx  : int{x < 0}, y {r, s} : int{y > x } ≺ p → q : Hello(x : int{x < 0}).endi
            p→q:H el l o
 [G-Pfx] −−−−−−−−−→           hx {p, q} : int{x < 0}, y {r, s} : int{y > x } ≺ endi
   Semantics of Local Types. We deﬁne the LTS semantics of local types in Fig. 14. Similar to
global type LTS semantics, we include the local context Σ in the semantics. Therefore, the judge-
                                                     α
ments of local LTS reductions have form hΣ ≺ Li −   → hΣ ′ ≺ L ′ i. When deﬁning the LTS semantics,
                                            ϵ
we also use judgements of form hΣ ≺ Li →    − hΣ ′ ≺ L ′ i. It represents a silent action that can occur
                                        ϵ ∗
without an observed action. We write →  − to denote the reﬂexive transition closure of silent actions
 ϵ
−.
→
   We ﬁrst have a look at silent transitions. [E-Phi] allows the variable in a silent type to be added
into the local context in the irrelevant form. This rule allows local roles to obtain knowledge from
the messages in the global protocol without their participation.
   [E-Cnt] allows preﬁxed local type to make a silent transition, if all of its continuations are
allowed to make a silent transition to reach the same context. The rule allows a preﬁxed local
type to obtain new knowledge about irrelevant variables, if such can be obtained in all possible
continuations.
   [E-Rec] unfolds recursive local types, analogous to the unfolding of global types.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Statically Verified Refinements for Multiparty Protocols                                                                1:21

                                                                                                 ϵ
                                † ∈ {&, ⊕}         ∀j ∈ I .                                 − hΣ ′ ≺ L ′j i
                                                                  hΣ ∪ {x j0 : Tj } ≺ L j i →
                      [E-Cnt]                                       ϵ               
                                                                   − hΣ ′ ≺ q † li (x i :Ti ).Li′ i ∈I i
                                 hΣ ≺ q †{li (x i :Ti ).Li }i ∈I i →

              [E-Rec]                                   ϵ
                                                     − hΣ ∪ {x ω : T } ≺ L[µt (x :T ).L/t]i
                          hΣ ≺ µt (x :T )hx := Ei.Li →

                      ϵ                           [E-Phi]                            ϵ
                  − hΣ ′ ≺ L ′ i
          hΣ ≺ Li →                                                            − hΣ ∪ {x 0 : T } ≺ Li
                                                              hΣ ≺ l(x :T ).Li →

                                                              j∈I
              [L-Send]
                                                              p→q:l j (x j :T j )
                           hΣ ≺ q⊕{li (x i :Ti ).Li }i ∈I i −−−−−−−−−−→ hΣ ∪ {x jω : Tj } ≺ L j i
                                                              j∈I
              [L-Recv]
                                                              p→q:l j (x j :T j )
                           hΣ ≺ p&{li (x i :Ti ).Li }i ∈I i −−−−−−−−−−→ hΣ ∪ {x jω : Tj } ≺ L j i
                                                              ϵ                                       α
                                                          − hΣ ′′ ≺ L ′′ i
                                                  hΣ ≺ Li →                              hΣ ′′ ≺ L ′′ i −
                                                                                                        → hΣ ′ ≺ L ′i
              α                         [L-Eps]                                      α
             → hΣ ′ ≺ L ′ i
     hΣ ≺ Li −                                                                   → hΣ ′ ≺ L ′ i
                                                                         hΣ ≺ Li −

                                    Fig. 14. LTS Semantics for Local Types

   For concrete transitions, we have [L-Send] (resp. [L-Recv]) to reduce a local type with a sending
(resp. receiving) preﬁx, if the action label is in the set of labels in the local type. The resulting
context contains the variable in the message as a concrete variable, since the role knows the value
via communication. The resulting local type is the continuation corresponding to the action label.
   In addition, [L-Eps] permits any number of silent actions to be taken before a concrete action.
  Remark 4.7 (Reductions for Empty Session Types). We consider empty session types to be
reducible, since it is not possible to distinguish which types are inhabited. However, it does not
invalidate the safety properties of endpoints, since no such endpoints can be implemented for an
empty session type.
   Relating Semantics of Global and Local Types. We extend the LTS semantics to a collection
of local types in Deﬁnition 4.8, in order to prove that projection preserves semantics. We deﬁne
the semantics in a synchronous fashion.
   The set of local types reduces with an action α = p → q : l(x : T ), if the local type for role p
and q both reduce with that action α. All other roles in the set of the local types are permitted to
make silent actions (ϵ actions).
   Our deﬁnition deviates from the standard deﬁnition [Deniélou and Yoshida 2013, Def. 3.3] in
two ways: One is that we use a synchronous semantics, so that one action involves two reductions,
namely at the sending and receiving sides. Second is that we use contexts and silent transitions
in the LTS semantics. The original deﬁnition requires all non-action roles to be identical, whereas
we relax the requirement to allow silent transitions.
  Deﬁnition 4.8 (LTS over a collection of local types). A conﬁguration s = {hΣr ≺ L r i}r∈P is a
collection of local types and contexts, indexable via participants.
                                                                  α =p→q:l (x :T )
  Let p ∈ P and q ∈ P. We say s = {hΣr ≺ L r i}r∈P −−−−−−−−−−−→ s ′ = {hΣr′ ≺ L r′ i}r∈P if
                  α                                     α
                  → hΣp′ ≺ L ′p i and, hΣq ≺ L q i −
  (1) hΣp ≺ L p i −                                → hΣq′ ≺ L ′q i and,

                                Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:22      Fangyi Zhou, Francisco Ferreira, Raymond Hu, Rumyana Neykova, and Nobuko Yoshida

                                                    ϵ ∗
                                                 − hΣs′ ≺ L s′ i
    (2) for all s ∈ P, s , p, s , q. hΣs ≺ L s i →
  For a closed global type G under context Γ, we show that the global type makes the same trace of
reductions as the collection of local types obtained from projection. We prove it in Theorem 4.10.
  Deﬁnition 4.9 (Association of Global Types and Conﬁgurations). Let hΓ ≺ Gi be a global context.
  The collection of local contexts associated to hΓ ≺ Gi, is deﬁned as the conﬁguration
{hΓ ≺ Gi ↾ r}r∈G . We write s ⇔ hΓ ≺ Gi if a conﬁguration s is the associated to hΓ ≺ Gi.
  Theorem 4.10 (Trace Eqivalence). Let hΓ ≺ Gi be a closed global context and s ⇔ hΓ ≺ Gi
be a conﬁguration associated with the global context.
           α                               α
           → hΓ ′ ≺ G ′ i if and only if s −
   hΓ ≺ Gi −                               → s ′ , where s ′ ⇔ hΓ ′ ≺ G ′i.
  The theorem states that semantics are preserved after projection. Practically, we can implement
local processes separately, and run them in parallel with preserved semantics.
   We also show that a well-formed global type G has progress. This means that a well-formed
global type does not get stuck, which implies deadlock freedom.
  Deﬁnition 4.11 (Well-formed Global Types). A global type under typing context hΓ ≺ Gi is
well-formed, if (1) G does not contain free type variables, (2) G is contractive [Pierce 2002, §21],
and (3) for all roles in the protocol r ∈ G, the projection hΓ ≺ Gi ↾ r is deﬁned.
  We also say a global type G is well-formed, if h ≺ Gi is well-formed.
  Theorem 4.12 (Preservation of Well-formedness). If hΓ ≺ Gi is a well-formed global type
                                  α
                                  → hΓ ′ ≺ G ′i, then hΓ ′ ≺ G ′i is well-formed.
under typing context, and hΓ ≺ Gi −
  Deﬁnition 4.13 (Progress). A conﬁguration s satisﬁes progress, if either (1) For all participants
                                                                                    α
p ∈ s, Lp = end, or (2) there exists an action α and a conﬁguration s ′ such that s −
                                                                                    → s ′.
  A global type under typing context hΓ ≺ Gi satisﬁes progress, if its associated conﬁguration
s ⇔ hΓ ≺ Gi, exists and satisﬁes progress.
  We also say a global type G satisﬁes progress, if h ≺ Gi satisﬁes progress.
  Theorem 4.14 (Progress). If hΓ ≺ Gi is a well-formed global type under typing context, then
hΓ ≺ Gi satisﬁes progress.
  Theorem 4.15 (Type Safety). If G is a well-formed global type, then for any global type under
typing context hΓ ′ ≺ G ′i such that h ≺ Gi −−→ ∗ hΓ ′ ≺ G ′i, hΓ ′ ≺ G ′i satisﬁes progress.
    Proof. Direct consequence of Theorem 4.12 and Theorem 4.14.                                   

5     EVALUATION
We evaluate the expressiveness and performance of our toolchain Session⋆ . We describe the meth-
odology and setup (§ 5.1), and comment on the compilation time (§ 5.2) and the execution time
(§ 5.3). We demonstrate the expressiveness of Session⋆ (§ 5.4) by implementing examples from
the session type literature and comparing with related work. The source ﬁles of the benchmarks
used in this section are included in our artifact, along with a script to reproduce the results.

5.1    Methodology and Setup
We measure the time to generate the CFSM representation from a Scribble protocol (CFSM), and
the time to generate F⋆ code from the CFSM representation (F⋆ APIs). Since the generated APIs in
F⋆ need to be type-checked before use, we also measure the type-checking time for the generated
code (Gen. Code). Finally, we provide a simple implementation of the callbacks and measure the
type-checking time for the callbacks against the generated type (Callbacks).

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Statically Verified Refinements for Multiparty Protocols                                                     1:23

global protocol PingPongn (role A, role B) {
  choice at A { Ping(x1 :int) from A to B;              Pong(y1 :int) from B to A; @"y1 >x1 "
                Ping(x2 :int) from A to B; @"x2 >y1 "    Pong(y2 :int) from B to A; @"y2 >x2 "
                ···
                Ping(xn :int) from A to B; @"xn >yn−1 " Pong(yn :int) from B to A; @"yn >xn "
                do PingPongn (A, B); }
           or { Bye() from A to B;                               Bye() from B to A; } }

                   Fig. 15. Ping Pong Protocol (Parameterised by Protocol Length n)

   To execute the protocols, we need a network transport to connect the participants by providing
appropriate sending and receiving primitives. In our experiment setup, we use the standard lib-
rary module FStar.Tcp to establish TCP connections between participants, and provide a simple
serialisation module for base types. Due to the small size of our payloads, we set TCP_NODELAY
to avoid the delays introduced by the congestion control algorithms. Since our entry point to ex-
ecute the protocol is parameterised by the connection/transport type, the implementation may use
other connections if developers wish, e.g. an in-memory queue for local setups. We measure the
execution time of the protocol (Execution Time).
   To measure the overhead of our implementation, we compare against an implementation of
the protocol without session types or reﬁnement types, which we call bare implementation. In
this implementation, we use the same sending and receiving primitives (i.e. connection ) as in the
toolchain implementation. The bare implementation is in a series of direct calls of sending and
receiving primitives, for the same communication pattern, but without the generated APIs.
   We use a Ping Pong protocol (Fig. 15), parameterised by the protocol length, i.e. the number of
Ping Pong messages n in a protocol iteration. When the protocol length n increases, the number
of CFSM states increases linearly, which gives rise to longer generated code and larger generated
types. In each Ping Pong message, we include payload of increasing numbers, and encode the
constraints as protocol reﬁnements.
   We study its eﬀect on the compilation time (§ 5.2) and the execution time (§ 5.3). We run the
experiment on varying sizes of n, up to 25. Larger sizes of n leads to unreasonably large resource
usage during type-checking in F⋆ . Table 1 reports the results for the Ping Pong protocol in Fig. 15.
   We run the experiments under a network of latency of 0.340ms (64 bytes ping), and repeat each
experiment 30 times. Measurements are taken using a machine with Intel i7-7700K CPU (4.20 GHz,
4 cores, 8 threads), 16 GiB RAM, operating system Ubuntu 18.04, OCaml compiler version 4.08.1,
F⋆ compiler commit 8040e34a, Z3 version 4.8.5.

5.2 Compilation Time
   CFSM and F⋆ Generation Time. We measure the time taken for Scribble to generate the
CFSM from the protocol in Fig. 15, and for the code generation tool to convert the CFSM to F⋆
APIs. We observe from Table 1 that the generation time for CFSMs and F⋆ APIs is short. It takes
less than 1 second to complete the generation phase for each case.
  Type-checking Time of Generated Code and Callbacks. We measure the time taken for the
generated APIs to type-check in F⋆ . We provide a simple F⋆ implementation of the callbacks fol-
lowing the generated APIs, and measure the time taken to type-check the callbacks.
  The increase of type-checking time is non-linear with regard to the protocol length. We encode
CFSM states as records corresponding to local typing contexts. In this case, the size of local typ-
ing contexts and the number of type deﬁnitions grows linearly, giving rise to a non-linear increase.
Moreover, the entry point function is likely to cause non-linear increases in the type-checking time.

                            Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:24      Fangyi Zhou, Francisco Ferreira, Raymond Hu, Rumyana Neykova, and Nobuko Yoshida

            Protocol       Generation Time          Type Checking Time                 Execution Time
           Length (n)      CFSM F⋆ APIs             Gen. Code Callbacks             (100 000 ping-pongs)
              bare            n/a       n/a                n/a       n/a                   28.79s
               1            0.38s     0.01s              1.28s     0.34s                   28.75s
               5            0.48s     0.01s              3.81s     1.12s                   28.82s
               10           0.55s     0.01s             14.83s     1.34s                   28.84s
               15           0.61s     0.01s             42.78s     1.78s                     n/a
               20           0.69s     0.02s             98.35s     2.54s                   28.81s
               25           0.78s     0.02s           206.82s      3.87s                   28.76s
                               Table 1. Time Measurements for Ping Pong Protocol

The long type-checking time of the generated code could be avoided if the developer chooses to
trust our toolchain to always generate well-typed F⋆ code for the entry point. The entry point
would be available in an interface ﬁle (cf. OCaml .mli ﬁles), with the actual implementation in
OCaml instead of F⋆5 . There would otherwise be no changes in the development workﬂow. Al-
though neither does type-checking time of the callback implementation ﬁt a linear pattern, it
remains within reasonable time frame.

5.3 Runtime Performance (Execution Time)
We measure the execution time taken for an exchange of 100,000 ping pongs for the toolchain and
bare implementation under the experiment network. The execution time is dominated by network
communication, since there is little computation to be performed at each endpoint.
   We provide a bare implementation using a series of direct invocations of sending and receiving
primitives, in a compatible way to communicate with generated APIs. The bare implementation
does not involve a record of callbacks, which is anticipated to run faster, since the bare implement-
ation involves fewer function pointers when calling callbacks. Moreover, the bare implementation
does not construct state records, which record a backlog of the communication, as the protocol
progresses. To measure the performance impact of book-keeping of callback and state records, we
run the Ping Pong protocol from Fig. 15 for a protocol of increasing size (number of states and
generated types), i.e. for increasing values of n. All implementations, including bare are run until
100,000 ping pong messages in total are exchanged6 .
   We summarise the results in Table 1. Despite the diﬀerent protocol lengths, there are no signiﬁc-
ant changes in execution time. Since the execution is dominated by time spent on communication,
the measurements are subject to network ﬂuctuations, diﬃcult to avoid during the experiments.
We conclude that our implementation does not impose a large overhead on the execution time.

5.4    Expressiveness
We implement examples from the session type literature, and add reﬁnements to encode data
dependencies in the protocols. We measure the time taken for code generation and type-checking,
and present them in Table 2. The time taken in the toolchain for examples in the session type
literature is usually short, yet we demonstrate that we are able to implement the examples easily
with our callback style API. Moreover, the time taken is incurred at the compilation stage, hence
there is no overhead for checking reﬁnements by our runtime.
5 Deﬁning a signature in an interface ﬁle, and providing an implementation in the target language (OCaml) allows the F⋆

compiler to assume the implementation is correct. This technique is used frequently in the standard library of F⋆ . This is
not to be confused with implementing the endpoints in OCaml instead of F⋆ , as that would bypass the F⋆ type-checking.
6 For n = 1, we run 100,000 iterations of recursion; for n = 10, we run 10,000 iterations, etc. Total number of ping pong

messages exchanged by two parties remain the same.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Statically Verified Refinements for Multiparty Protocols                                                        1:25

                                                                          MP     Multiparty Protocol
     Example (Endpoint)    Gen. / TC. Time     MP     RV    IV    STP     RV     Uses Recursion Variables
     Two Buyer a (A)           0.46s / 2.33s    X     ✗     X     X†      IV     Irrelevant Variables
     Negotiation b (C)         0.46s / 1.59s    ✗     X     ✗     ✗              Implementable in STP
                                                                         STP
     Fibonacci c (A)           0.44s / 1.58s    ✗     X     ✗     ✗              X† STP requires dynamic checks
                                                                            a    [Honda et al. 2016]
     Travel Agency d (C)       0.62s / 2.36s    X     ✗     ✗     X†        b    [Demangeon and Honda 2012]
     Calculator c (C)          0.51s / 2.30s    ✗     ✗     ✗     X         c    [Hu and Yoshida 2016]
     SH e (P)                  1.16s / 4.31s    X     ✗     X     X†        d    [Hu et al. 2008]
     Online Wallet f (C)       0.62s / 2.67s    X     X     ✗     ✗         e    [Neykova et al. 2018]
                                                                            f    [Neykova et al. 2013]
     Ticket д (C)              0.45s / 1.90s    ✗     X     ✗     ✗
                                                                            д    [Bocchi et al. 2013]
     HTTP h (S)                0.55s / 1.79s    ✗     ✗     ✗     X†        h    [Fielding and Reschke 2014]
                                 Table 2. Selected Examples from Literature
   We also compare the expressiveness of our work with two most closely related works, namely
Bocchi et al. [2010] and Neykova et al. [2018], which study reﬁnements in MPST (also see § 6).
Neykova et al. [2018] (Session Type Provider, STP) implements limited version of reﬁnements in
the Scribble toolchain. Our version is strictly more expressive than STP for two reasons: (1) sup-
port for recursive variables to express invariants and (2) support for irrelevant variables. Fig. 16
illustrates those features and Table 2 identiﬁes which of the implemented examples use them.
    protocol Adder(role S, role C)                        protocol Broadcast(role A, role B, role C)
    @"S[acc:=0]" {                                        {
      Num(x:int) from C to S; @"x≥0"                        Broadcast(x:int) from A to B; @"x≥0"
      Sum(sum:int) from S to C; @"sum=acc+x"                // C does not learn y≥0 in STP
      do Adder(S, C); @"S[sum]" }                           Broadcast(y:int) from A to C; @"x=y" }
       (a) Accumulator (using Recursive Invariants)          (b) Broadcasting (using Irrelevant Variables)

         Fig. 16. Example Protocols Demonstrating Additional Expressiveness to [Neykova et al. 2018]
   In STP, when recursion occurs, all information about the variables is lost at the end of an itera-
tion, hence their tool does not support even the simple example in Fig. 16a. In contrast, our work
retains the recursion variables, which are available throughout the recursion. Additionally, the
endpoint projection in STP is more conservative with regards to reﬁnements. Whilst there must
be no variables unknown to a role in the reﬁnements attached to a message for the sending role,
there may be unknown variables to the receiving role. The part unknown to the receiving role is
discarded (hence weakening the pre-condition). In our work such information can still be retained
and used for type checking, thanks to irrelevant variables.
   In Bocchi et al. [2010], a global protocol with assertions must be well-asserted (§3.1). In particu-
lar, the history sensitivity requirement states: "A predicate guaranteed by a participant p can only
contain those interaction variables that p knows." Our theory lifts this restriction by allowing vari-
ables unknown to a sending role to be used in the global or local type, whereas such variables
cannot be used in the implementation. For example, Example 4.1 fails the well-asserted require-
ment in [Bocchi et al. 2010]. In the reﬁnement x = z for variable z (for message label Trd), the
variable x is not known to C, hence the protocol would not be well-asserted. In our setup, such
protocol is permitted, the endpoint implementation for C can provide the value y received from B
to satisfy the reﬁnement type — The SMT solver can validate the reﬁnement from the transitivity
of equality.

6     RELATED WORK
We summarise the most closely related works in the areas of reﬁnement and session types. For a
detailed survey on theory and implementations of session types, see Gay and Ravara [2017].

                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:26     Fangyi Zhou, Francisco Ferreira, Raymond Hu, Rumyana Neykova, and Nobuko Yoshida

   Reﬁnement Types for Veriﬁcation and Reasoning. Reﬁnement types were introduced to al-
low recursive data structures to be speciﬁed in more details using predicates [Freeman and Pfenning
1991]. Subsequent works on the topic [Bengtson et al. 2011; Schmid and Kuncak 2016; Vazou et al.
2014, 2017] utilise SMT solvers, such as Z3 [De Moura and Bjørner 2008], to aid the type system
to decide a semantic subtyping relation [Bierman et al. 2012] using SMT encodings. Reﬁnement
types have been applied to numerous domains, such as resource usage analysis [Handley et al.
2019; Knoth et al. 2020], secure implementations [Bengtson et al. 2011; Bhargavan et al. 2010], in-
formation control ﬂow enforcements [Polikarpova et al. 2020], and theorem proving [Vazou et al.
2017]. Our aim is to utilise reﬁnement types for the speciﬁcation and veriﬁcation of distributed
protocols, by combining reﬁnement and session types in a single practical framework.

   Implementation of Session Types. Neykova et al. [2018] provides an implementation of MPST
with assertions using Scribble and F#. Their implementation, the session type provider (STP), re-
lies on code generation of ﬂuent (class-based) APIs, initially described in [Hu and Yoshida 2016].
Each protocol state is implemented as a class, with methods corresponding to the possible trans-
itions from that state. It forces a programming style that not only relies extensively on method
chaining, but also requires dynamic checks to ensure the linearity of channel usage. Our work
diﬀers from STP in multiple ways. First, we extend the Scribble toolchain to support recursion
variables, allowing reﬁnements on recursions, hence improving expressiveness. In this way, de-
velopers can specify dependencies across recursive calls, which is not supported in STP. Second,
we depart from the class-based API generation, and generate a callback-based API. Our approach
has the advantage that the linear usage of channels is ensured by construction, saving dynamic
checks for channels. Third, we use reﬁnement types in F⋆ to verify reﬁnements statically, in con-
trast, STP performs dynamic evaluations to validate assertions in protocols. Finally, the metatheory
of session types extended with reﬁnements was not developed in their work.
   Several other MPST works follow a similar technique of class-based API generation to overcome
limitations of the type system in the target language, e.g. Castro et al. [2019] for Go, Ng et al. [2015]
for C. All of the above works, suﬀer from the same limitations – they detect linearity violations
at runtime, and oﬀer no static alternative. Indeed, to our knowledge, Imai et al. [2020] provide
the only MPST implementation which statically checks linearity violation. It relies on speciﬁc
type-level OCaml features, and a monadic programming style. Our work proposes generation of
a callback-styled API from MPST protocols. To our knowledge, it is the ﬁrst work that ensures
linear channel usage by construction. Although our target language is F*, the callback-styled API
code generation technique is applicable to any mainstream programming language.

   Dependent and Reﬁnement Session Types. Bocchi et al. [2010] propose a multiparty session
π -calculus with logical assertions. By contrast, our formulation of RMPST is based on reﬁnement
types, projection with silent preﬁxes and correspondence with CFSMs, to target practical code
generation, such as for F⋆ . They do not formulate any semantics for global types nor prove an
equivalence between reﬁned global types and projections, as in this paper. Toninho and Yoshida
[2017] extend MPST with value dependent types. Invariants on values are witnessed by proof
objects, which then may be erased at runtime. Our work uses reﬁnement types, which follows the
principle naturally, since reﬁnements that appear in types are proof-irrelevant and can be erased
safely. These works are limited to theory, whereas we provide an implementation.
   De Muijnck-Hughes et al. [2019] propose an Embedded Domain Speciﬁc Language (EDSL) ap-
proach of implementing multiparty sessions (analogous to MPST) in Idris. They use value depend-
ent types in Idris to deﬁne combinators, with options to specify data dependencies, contrary to our

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Statically Verified Refinements for Multiparty Protocols                                                     1:27

approach of code generation. However, the combinators only describe the sessions, and how to im-
plement and execute the sessions remains unanswered. Our work provides a complete toolchain
from protocol description to implementation and veriﬁcation.
   In the setting of binary session types, Das and Pfenning [2020] extend session types with arith-
metic reﬁnements, with application to work analysis for computing upper bounds of work from
a given session type. Thiemann and Vasconcelos [2019] extend binary session types with label
dependent types. In the setup of their work, speciﬁcation of arithmetic properties involves com-
plicated deﬁnitions of inductive arithmetic relations and functions. In contrast, we use SMT solvers,
which have built-in functions and relations for arithmetic. Furthermore, there is no need to con-
struct proofs manually, since SMT solvers ﬁnd the proof automatically, which enhances usability
and ergonomics. Hinrichsen et al. [2019] combine binary session types with concurrent separation
logic, allowing reasoning about mixed-paradigm concurrent programs, and planned to extend the
framework to MPST. Along similar lines, Swamy et al. [2020] provide a framework of concurrent
separation logic in F⋆ , and demonstrate its expressiveness by showing how (dependent) binary
session types can be represented in the logic and used in reasoning. Our work is based on the
theory of MPST, subsuming the binary session types. Furthermore, we implement a toolchain that
developers can use.
   Bhargavan et al. [2009] use reﬁnement types to implement a limited form of multiparty session
types. Session types are encoded in reﬁnement types via code generation. The speciﬁcation lan-
guage they use, albeit similar to MPST, has limited expressive power. Only patterns of interactions
where participants alternate between sending and receiving are permitted. Moreover, they do not
study data dependencies in protocols, hence they can neither specify, nor verify constraints on pay-
loads or recursions. We use reﬁnement types to specify constraints and dependencies in multiparty
protocols, and use the F⋆ compiler [Swamy et al. 2016] for verifying the endpoint implementations.
The veriﬁed endpoint program does not only comply to the multiparty protocol, enjoying the guar-
antees provided by the original MPST theory (deadlock freedom, session ﬁdelity), but also satisﬁes
additional guarantees provided by reﬁnement types with respect to data constraints.


7   CONCLUSIONS AND FUTURE WORK
We present a novel toolchain for implementing reﬁned multiparty session types (RMPST), which
enables developers to use Scribble, a protocol description language for multiparty session types,
and F⋆ , a state-of-the-art veriﬁcation-oriented programming language, to implement a multiparty
protocol and statically verify endpoint implementations. To the best of the authors’ knowledge,
this is the ﬁrst work on statically veriﬁed multiparty protocols with reﬁnement types. We extend
the theory of multiparty session types with data reﬁnements, and present a toolchain that enables
developers to specify multiparty protocols with data dependencies, and implement the endpoints
using generated APIs in F⋆ . We leverage the advanced typing system in F⋆ to encode local session
types for endpoints, and validate the data dependencies in the protocol statically.
    The veriﬁed endpoint program in F⋆ is extracted into OCaml, where the reﬁnements are erased
— adding no runtime overhead for reﬁnements. The callback-styled API avoids linearity checks of
channel usage by internalising communications in generated code. We evaluate our toolchain and
demonstrate that our overhead is small compared to an implementation without session types.
    Whereas reﬁnement types express the data dependencies of multiparty protocols, the availab-
ility of reﬁnement types in general purpose mainstream programming languages is limited. For
future work, we wish to study how to mix participants with reﬁned implementation and those
without, possibly using a gradual typing system [Igarashi et al. 2019; Lehmann and Tanter 2017].


                            Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:28      Fangyi Zhou, Francisco Ferreira, Raymond Hu, Rumyana Neykova, and Nobuko Yoshida

ACKNOWLEDGMENTS
We thank the OOPSLA reviewers for their comments and suggestions, and David Castro, Julia Ga-
bet and Lorenzo Gheri for proofreading. We thank Wei Jiang and Qianyi Shu for testing the arti-
fact. The work is supported by EPSRC EP/T006544/1, EP/K011715/1, EP/K034413/1, EP/L00058X/1,
EP/N027833/1, EP/N028201/1, EP/T006544/1, EP/T014709/1 and EP/V000462/1, and NCSS/EPSRC
VeTSS.


REFERENCES
Andreas Abel and Gabriel Scherer. 2012. On Irrelevance and Algorithmic Equality in Predicative Type Theory. Logical
   Methods in Computer Science Volume 8, Issue 1 (March 2012). https://doi.org/10.2168/LMCS-8(1:29)2012
Davide Ancona, Viviana Bono, Mario Bravetti, Joana Campos, Giuseppe Castagna, Pierre-Malo Deniélou, Simon J. Gay, Nils
   Gesbert, Elena Giachino, Raymond Hu, Einar Broch Johnsen, Francisco Martins, Viviana Mascardi, Fabrizio Montesi,
   Rumyana Neykova, Nicholas Ng, Luca Padovani, Vasco T. Vasconcelos, and Nobuko Yoshida. 2016. Behavioral Types in
   Programming Languages. Found. Trends Program. Lang. 3, 2–3 (July 2016), 95–230. https://doi.org/10.1561/2500000031
Jesper Bengtson, Karthikeyan Bhargavan, Cédric Fournet, Andrew D Gordon, and Sergio Maﬀeis. 2011. Reﬁnement types
   for secure implementations. ACM Transactions on Programming Languages and Systems (TOPLAS) 33, 2 (2011), 8.
Karthikeyan Bhargavan, Ricardo Corin, Pierre-Malo Deniélou, Cédric Fournet, and James J. Leifer. 2009. Cryptographic
   Protocol Synthesis and Veriﬁcation for Multiparty Sessions. In 2009 22nd IEEE Computer Security Foundations Symposium.
   124–140. https://doi.org/10.1109/CSF.2009.26
Karthikeyan Bhargavan, Cédric Fournet, and Andrew D. Gordon. 2010. Modular Veriﬁcation of Security Protocol Code by
   Typing. In Proceedings of the 37th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages
   (POPL ’10). ACM, New York, NY, USA, 445–456. https://doi.org/10.1145/1706299.1706350
Gavin M Bierman, Andrew D Gordon, Cătălin Hriţcu, and David Langworthy. 2012. Semantic subtyping with an SMT
   solver. Journal of Functional Programming 22, 1 (2012), 31–105. https://doi.org/10.1017/S0956796812000032
Laura Bocchi, Romain Demangeon, and Nobuko Yoshida. 2013. A Multiparty Multi-session Logic. In Trustworthy Global
   Computing, Catuscia Palamidessi and Mark D. Ryan (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 97–111.
Laura Bocchi, Kohei Honda, Emilio Tuosto, and Nobuko Yoshida. 2010. A Theory of Design-by-Contract for Distributed
   Multiparty Interactions. In CONCUR 2010 - Concurrency Theory, Paul Gastin and François Laroussinie (Eds.). Springer
   Berlin Heidelberg, Berlin, Heidelberg, 162–176.
Daniel Brand and Pitro Zaﬁropulo. 1983. On Communicating Finite-State Machines. J. ACM 30, 2 (April 1983), 323–342.
   https://doi.org/10.1145/322374.322380
David Castro, Raymond Hu, Sung-Shik Jongmans, Nicholas Ng, and Nobuko Yoshida. 2019. Distributed Programming Using
   Role-parametric Session Types in Go: Statically-typed Endpoint APIs for Dynamically-instantiated Communication
   Structures. Proc. ACM Program. Lang. 3, POPL, Article 29 (Jan. 2019), 30 pages. https://doi.org/10.1145/3290342
Ankush Das and Frank Pfenning. 2020. Session Types with Arithmetic Reﬁnements. In 31st International Conference
   on Concurrency Theory (CONCUR 2020) (Leibniz International Proceedings in Informatics (LIPIcs)), Igor Konnov and
   Laura Kovács (Eds.), Vol. 171. Schloss Dagstuhl–Leibniz-Zentrum für Informatik, Dagstuhl, Germany, 13:1–13:18.
   https://doi.org/10.4230/LIPIcs.CONCUR.2020.13
Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: An Eﬃcient SMT Solver. In Proceedings of the Theory and Prac-
   tice of Software, 14th International Conference on Tools and Algorithms for the Construction and Analysis of Systems
   (TACAS’08/ETAPS’08). Springer-Verlag, Berlin, Heidelberg, 337–340. http://dl.acm.org/citation.cfm?id=1792734.1792766
Jan de Muijnck-Hughes, Edwin Brady, and Wim Vanderbauwhede. 2019. Value-Dependent Session Design in a Dependently
   Typed Language. In Proceedings Programming Language Approaches to Concurrency- and Communication-cEntric Soft-
   ware, Prague, Czech Republic, 7th April 2019 (Electronic Proceedings in Theoretical Computer Science), Francisco Martins
   and Dominic Orchard (Eds.), Vol. 291. Open Publishing Association, 47–59. https://doi.org/10.4204/EPTCS.291.5
Romain Demangeon and Kohei Honda. 2012. Nested Protocols in Session Types. In CONCUR 2012 - Concurrency
   Theory - 23rd International Conference, CONCUR 2012, Newcastle upon Tyne, UK, September 4-7, 2012. Proceed-
   ings (Lecture Notes in Computer Science), Maciej Koutny and Irek Ulidowski (Eds.), Vol. 7454. Springer, 272–286.
   https://doi.org/10.1007/978-3-642-32940-1_20
Pierre-Malo Denielou, Nobuko Yoshida, Andi Bejleri, and Raymond Hu. 2012. Parameterised Multiparty Session Types.
   Logical Methods in Computer Science Volume 8, Issue 4 (Oct. 2012). https://doi.org/10.2168/LMCS-8(4:6)2012
Pierre-Malo Deniélou and Nobuko Yoshida. 2013. Multiparty Compatibility in Communicating Automata: Characterisation
   and Synthesis of Global Session Types. In 40th International Colloquium on Automata, Languages and Programming
   (LNCS), Vol. 7966. Springer, Berlin, Heidelberg, 174–186. https://doi.org/10.1007/978-3-642-39212-2_18


Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Statically Verified Refinements for Multiparty Protocols                                                               1:29

Roy T. (Ed.) Fielding and Julian F. (Ed.) Reschke. 2014. Hypertext Transfer Protocol (HTTP/1.1): Message Syntax and Routing.
   RFC 7230. RFC Editor. 1–89 pages. https://www.rfc-editor.org/info/rfc7230
Tim Freeman and Frank Pfenning. 1991. Reﬁnement Types for ML. In Proceedings of the ACM SIGPLAN 1991 Con-
   ference on Programming Language Design and Implementation (PLDI ’91). ACM, New York, NY, USA, 268–277.
   https://doi.org/10.1145/113445.113468
Simon Gay and António Ravara (Eds.). 2017.               Behavioural Types: from Theory to Tools.           River Publishers.
   https://doi.org/10.13052/rp-9788793519817
Martin A. T. Handley, Niki Vazou, and Graham Hutton. 2019. Liquidate Your Assets: Reasoning about Resource Usage in Li-
   quid Haskell. Proc. ACM Program. Lang. 4, POPL, Article Article 24 (Dec. 2019), 27 pages. https://doi.org/10.1145/3371092
Jonas Kastberg Hinrichsen, Jesper Bengtson, and Robbert Krebbers. 2019. Actris: Session-Type Based Reasoning in Separ-
   ation Logic. Proc. ACM Program. Lang. 4, POPL, Article Article 6 (Dec. 2019), 30 pages. https://doi.org/10.1145/3371074
Kohei Honda, Nobuko Yoshida, and Marco Carbone. 2008. Multiparty Asynchronous Session Types. In Proceedings of the
   35th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL ’08). ACM, New York,
   NY, USA, 273–284. https://doi.org/10.1145/1328438.1328472
Kohei Honda, Nobuko Yoshida, and Marco Carbone. 2016. Multiparty Asynchronous Session Types. J. ACM 63 (2016),
   1–67. Issue 1-9. https://doi.org/10.1145/2827695
Raymond Hu. 2017. Distributed Programming Using Java APIs Generated from Session Types. Behavioural Types: from
   Theory to Tools (2017), 287–308.
Raymond Hu and Nobuko Yoshida. 2016. Hybrid Session Veriﬁcation through Endpoint API Generation. In 19th Interna-
   tional Conference on Fundamental Approaches to Software Engineering (LNCS), Vol. 9633. Springer, Berlin, Heidelberg,
   401–418. https://doi.org/10.1007/978-3-662-49665-7_24
Raymond Hu, Nobuko Yoshida, and Kohei Honda. 2008. Session-Based Distributed Programming in Java. In ECOOP 2008
   - Object-Oriented Programming, 22nd European Conference, Paphos, Cyprus, July 7-11, 2008, Proceedings (Lecture Notes in
   Computer Science), Jan Vitek (Ed.), Vol. 5142. Springer, 516–541. https://doi.org/10.1007/978-3-540-70592-5_22
Atsushi Igarashi, Peter Thiemann, Yuya Tsuda, Vasco T. Vasconcelos, and Philip Wadler. 2019. Gradual session types.
   Journal of Functional Programming 29 (2019), e17. https://doi.org/10.1017/S0956796819000169
Keigo Imai, Rumyana Neykova, Nobuko Yoshida, and Shoji Yuen. 2020. Multiparty Session Programming with Global Pro-
   tocol Combinators. https://github.com/keigoi/ocaml-mpst (LIPIcs). Schloss Dagstuhl - Leibniz-Zentrum für Informatik.
   To appear in ECOOP’20.
Keigo Imai, Nobuko Yoshida, and Shoji Yuen. 2019. Session-ocaml: A session-based library with polarities and lenses.
   Science of Computer Programming 172 (2019), 135 – 159. https://doi.org/10.1016/j.scico.2018.08.005
Tristan Knoth, Di Wang, Adam Reynolds, Jan Hoﬀmann, and Nadia Polikarpova. 2020. Liquid Resource Types. Proc. ACM
   Program. Lang. 4, ICFP, Article 106 (Aug. 2020), 29 pages. https://doi.org/10.1145/3408988
Nico Lehmann and Éric Tanter. 2017. Gradual Reﬁnement Types. In Proceedings of the 44th ACM SIGPLAN Symposium on
   Principles of Programming Languages (POPL 2017). Association for Computing Machinery, New York, NY, USA, 775–788.
   https://doi.org/10.1145/3009837.3009856
Rumyana Neykova, Raymond Hu, Nobuko Yoshida, and Fahd Abdeljallal. 2018. A Session Type Provider: Compile-time
   API Generation of Distributed Protocols with Reﬁnements in F#. In Proceedings of the 27th International Conference on
   Compiler Construction (CC 2018). ACM, New York, NY, USA, 128–138. https://doi.org/10.1145/3178372.3179495
Rumyana Neykova and Nobuko Yoshida. 2019. Featherweight Scribble. Springer International Publishing, Cham, 236–259.
   https://doi.org/10.1007/978-3-030-21485-2_14
Rumyana Neykova, Nobuko Yoshida, and Raymond Hu. 2013. SPY: Local Veriﬁcation of Global Protocols. In Runtime
   Veriﬁcation, Axel Legay and Saddek Bensalem (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 358–363.
Nicholas Ng, Jose G.F. Coutinho, and Nobuko Yoshida. 2015. Protocols by Default: Safe MPI Code Generation based
   on Session Types. In 24th International Conference on Compiler Construction (LNCS), Vol. 9031. Springer, 212–232.
   https://doi.org/10.1007/978-3-662-46663-6_11
Dominic Orchard and Nobuko Yoshida. 2017. Session Types with Linearity in Haskell. Behavioural Types: from Theory to
   Tools (2017), 219–241.
Frank Pfenning. 2001. Intensionality, extensionality, and proof irrelevance in modal type theory. In Proceedings 16th Annual
   IEEE Symposium on Logic in Computer Science. IEEE, 221–230.
Benjamin C. Pierce. 2002. Types and Programming Languages (1st ed.). The MIT Press.
Nadia Polikarpova, Deian Stefan, Jean Yang, Shachar Itzhaky, Travis Hance, and Armando Solar-Lezama. 2020.
   Liquid Information Flow Control.           Proc. ACM Program. Lang. 4, ICFP, Article 105 (Aug. 2020), 30 pages.
   https://doi.org/10.1145/3408987
Patrick M. Rondon, Ming Kawaguchi, and Ranjit Jhala. 2008. Liquid Types. In Proceedings of the 29th ACM SIGPLAN
   Conference on Programming Language Design and Implementation (PLDI ’08). ACM, New York, NY, USA, 159–169.
   https://doi.org/10.1145/1375581.1375602


                                  Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:30      Fangyi Zhou, Francisco Ferreira, Raymond Hu, Rumyana Neykova, and Nobuko Yoshida

Alceste Scalas, Ornela Dardha, Raymond Hu, and Nobuko Yoshida. 2017. A Linear Decomposition of Multiparty Sessions
   for Safe Distributed Programming. In ECOOP. https://doi.org/10.4230/LIPIcs.ECOOP.2017.24
Georg Stefan Schmid and Viktor Kuncak. 2016. SMT-based Checking of Predicate-qualiﬁed Types for Scala. In Pro-
   ceedings of the 2016 7th ACM SIGPLAN Symposium on Scala (SCALA 2016). ACM, New York, NY, USA, 31–40.
   https://doi.org/10.1145/2998392.2998398
Scribble Authors. 2015. Scribble: Describing Multi Party Protocols. http://www.scribble.org/. Accessed on 20th April 2020.
Nikhil Swamy, Cătălin Hriţcu, Chantal Keller, Aseem Rastogi, Antoine Delignat-Lavaud, Simon Forest, Karthikeyan
   Bhargavan, Cédric Fournet, Pierre-Yves Strub, Markulf Kohlweiss, Jean-Karim Zinzindohoue, and Santiago Zanella-
   Béguelin. 2016. Dependent Types and Multi-monadic Eﬀects in F*. In Proceedings of the 43rd Annual ACM SIGPLAN-
   SIGACT Symposium on Principles of Programming Languages (POPL ’16). ACM, St. Petersburg, FL, USA, 256–270.
   https://doi.org/10.1145/2837614.2837655
Nikhil Swamy, Aseem Rastogi, Aymeric Fromherz, Denis Merigoux, Danel Ahman, and Guido Martínez. 2020. SteelCore:
   An Extensible Concurrent Separation Logic for Eﬀectful Dependently Typed Programs. Proc. ACM Program. Lang. 4,
   ICFP, Article 121 (Aug. 2020), 30 pages. https://doi.org/10.1145/3409003
Peter Thiemann and Vasco T. Vasconcelos. 2019. Label-Dependent Session Types. Proc. ACM Program. Lang., Article Article
   67 (Dec. 2019), 29 pages. https://doi.org/10.1145/3371135
Bernardo Toninho and Nobuko Yoshida. 2017. Certifying data in multiparty session types. Journal of Logical and Algebraic
   Methods in Programming 90 (2017), 61 – 83. https://doi.org/10.1016/j.jlamp.2016.11.005
Niki Vazou, Eric L. Seidel, Ranjit Jhala, Dimitrios Vytiniotis, and Simon Peyton-Jones. 2014. Reﬁnement Types for Haskell.
   In Proceedings of the 19th ACM SIGPLAN International Conference on Functional Programming (ICFP ’14). ACM, New
   York, NY, USA, 269–282. https://doi.org/10.1145/2628136.2628161
Niki Vazou, Anish Tondwalkar, Vikraman Choudhury, Ryan G. Scott, Ryan R. Newton, Philip Wadler, and Ranjit Jhala.
   2017. Reﬁnement Reﬂection: Complete Veriﬁcation with SMT. Proc. ACM Program. Lang. 2, POPL, Article 53 (Dec.
   2017), 31 pages. https://doi.org/10.1145/3158141
Fangyi Zhou, Francisco Ferreira, Raymond Hu, Rumyana Neykova, and Nobuko Yoshida. 2020. Statically Veriﬁed Reﬁne-
   ments for Multiparty Protocols. https://doi.org/10.5281/zenodo.3970760


A PROOFS FOR § 4
A.1 Auxiliary lemmas
  Lemma A.1. Given a participant p, a global typing context Γ and a local typing context Σ such that
Γ ↾ p = Σ.
  Then, the projection of global typing context Γ with x P :T to p satisﬁes that
                                                 (
                                                   Σ ∪ {x ω : T } if p ∈ P
                            Γ ∪ {x P : T } ↾ p =
                                                   Σ ∪ {x 0 : T } if p < P


   Proof. By expanding deﬁntion and case analysis.                                                                     

   Lemma A.2. Given a participant p, global typing contexts Γ1 , Γ2 , a global type G.
   If the two typing contexts have the same projection on p: Γ1 ↾ p = Γ2 ↾ p, then the projection of
global types under the two contexts are the same: hΓ1 ≺ Gi ↾ p = hΓ2 ≺ Gi ↾ p.
   Proof. By induction on the derivation of projection of global types.                                                

  Lemma A.3. Given a global typing context Γ, a set of participants P, a participant p, a variable x,
a well-formed type T and a global type G.
  If hΓ ∪ {x  : T } ≺ Gi ↾ p = hΣ ≺ Li, then hΓ ∪ {x P : T } ≺ Gi ↾ p = hΣ ≺ Li.
  Proof. By induction on derivation of projection of global types, via weakening of local typing
rules:
                       Σ1, x 0 :T , Σ2 ⊢ E :T ′ =⇒ Σ1, x ω :T , Σ2 ⊢ E :T ′
                                                                                                                       

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Statically Verified Refinements for Multiparty Protocols                                                       1:31

   Lemma A.4 (Inversion of Projection). Given a global typing context Γ, a global type G, a par-
ticipant p, a local typing context Σ, a local type L, such that hΓ ≺ Gi ↾ p = hΣ ≺ Li.
   If L is of form:
   (1) L = q⊕{li (x i :Ti ).Li }i ∈I , then G is of form p → q {li (x i :Ti ).G i }i ∈I .
   (2) L = q&{li (x i :Ti ).Li }i ∈I , then G is of form q → p {li (x i :Ti ).G i }i ∈I .
   (3) L = l(x :T ).L, then G is of form s → t {li (x i :Ti ).G i }i ∈I , where p < {s, t} and l(x :T ).L =
       ⊔i ∈I li (x i :Ti ).Li , where Li is obtained via the projection of G i .
   (4) L = µt (x :T )hx := Ei.L ′ , then G is of form µt(x :T )hx := Ei.G ′ , and p ∈ G.
  Proof. A direct consequence of projections rules hΓ ≺ Gi ↾ p — The results of projections are
not overlapping.                                                                             
  Lemma A.5 (Determinancy). Let hΓ ≺ Gi be a global type under a global typing context, and α
be a labelled action.
               α                         α
  If hΓ ≺ Gi − → hΓ1 ≺ G 1 i and hΓ ≺ Gi −
                                         → hΓ2 ≺ G 2 i, then hΓ1 ≺ G 1 i = hΓ2 ≺ G 2 i.
  Proof. By induction on global type reduction rules.                                                             

A.2   Proof of Theorem 4.10
      Let hΓ ≺ Gi be a global type under a global typing context and s ⇔ hΓ ≺ Gi be a
      conﬁguration associated with the global type and context.
              α                              α
              → hΓ ′ ≺ G ′i if and only if s −
      hΓ ≺ Gi −                              → s ′, where s ′ ⇔ hΓ ′ ≺ G ′i.
                                                                                                         α
 Proof. Soundness (⇒): By induction on the reduction rules of global types hΓ ≺ Gi −      → hΓ ′ ≺
 ′
G i.
 (1) [G-Pfx]
     For p:
     We project the global context before transition to p.
     hΓ ≺ p → q {li (x i :Ti ).G i }i ∈I i ↾ p = hΣp ≺ q⊕{li (x i :Ti ).Li }i ∈I i
                                                      {p, q}
     where Σp = Γ ↾ p and hΣi ≺ Li i = hΓ ∪ {x i             : Ti } ≺ G i i ↾ p for i ∈ I
                                                  p→q:l j (x j :T j )
      We have hΣp ≺ q⊕{li (x i :Ti ).Li }i ∈I i −−−−−−−−−−→ hΣp ∪ {x j : Tj } ≺ L j i by [L-Send].
      We project the global context after transition to p (via Lemma A.1).
              {p, q}
      hΓ ∪ {x j      : Tj } ≺ G j i ↾ p = hΣp ∪ {x j : Tj } ≺ L j i
      which is the same as the result of applying [L-Send].
      For q:
      Similar to the case of p, using [L-Recv].
      For r (r , p, r , q):
      We project the global context before transition to r.
      hΓ ≺ p → q {li (x i :Ti ).G i }i ∈I i ↾ p = hΣr ≺ ⊔i ∈I li (x i :Ti ).Li i
                                                        {p, q}
      where Σr = Γ ↾ r and hΣi ≺ Li i = hΓ ∪ {x i              : Ti } ≺ G i i ↾ r for i ∈ I
      We project the global context after transition to r (via Lemma A.1).
              {p, q}
      hΓ ∪ {x j      : Tj } ≺ G j i ↾ r = hΣr ∪ {x j0 : Tj } ≺ L j i
                                            ϵ
                                             − hΣr ∪ {x j0 : Tj } ≺ L j i by [E-Phi] and plain merging.
      We have hΣr ≺ ⊔i ∈I li (x i :Ti ).Li i →
  (2) [G-Cnt]
      By inductive hypothesis, we have
                                                      α
        ∀j ∈ I . {hΓ ∪ {x j : Tj } ≺ G j i ↾ r}r∈G j −
                                                      → {hΓ ′ ≺ G j′ i ↾ r}r∈G j
                                                                  α
        If r ∈ subj(α), then hΓ ∪ {x j : Tj } ≺ G j i ↾ r −
                                                           → hΓ ′ ≺ G j′ i ↾ r.

                              Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:32     Fangyi Zhou, Francisco Ferreira, Raymond Hu, Rumyana Neykova, and Nobuko Yoshida

                                                                    ϵ
         If r’ < subj(α), then hΓ ∪ {x j : Tj } ≺ G j i ↾ r’ → − hΓ ′ ≺ G j′ i ↾ r’.
       For p:
       We project the global context before transition to p.
       hΓ ≺ p → q {li (x i :Ti ).G i }i ∈I i ↾ p = hΣp ≺ q⊕{li (x i :Ti ).Li }ii ∈I
                                                         {p, q}
       where Σp = Γ ↾ p and hΣi ≺ Li i = hΓ ∪ {x i              : Ti } ≺ G i i ↾ p for i ∈ I
       We project the global context after transition to p.     
       hΓ ′ ≺ p → q li (x i :Ti ).G i′ i ∈I i ↾ p = hΣp ′ ≺ q⊕ li (x i :Ti ).Li′ ii ∈I
                                                            {p, q}
       where Σp ′ = Γ ′ ↾ p and hΣi′ ≺ Li′ i = hΓ ′ ∪ {x i         : Ti } ≺ G i′ i ↾ p for i ∈ I
                                                                        ϵ
       Since p < subj(α), we have hΣp ∪ {x j0 : Tj } ≺ L j i →      − hΣp ′ ≺ L ′j i = hΓ ′ ≺ G j′ i ↾ p from the
       inductive hypothesis.
                                                                    ϵ                 
       By [E-Cnt], we have hΣp ≺ q⊕{li (x i :Ti ).Li }i ∈I i →     − hΣp ′ ≺ q⊕ li (x i :Ti ).Li′ i ∈I i.
       For q, the proof is similar.
       For r, where r , p, r , q, and r < subj(α):
       We project the global context before transition to r.
       hΓ ≺ p → q {li (x i :Ti ).G i }i ∈I i ↾ r = hΣr ≺ ⊔i ∈I li (x i :Ti ).Li i
                                                         {p, q}
       where Σr = Γ ↾ r and hΣi ≺ Li i = hΓ ∪ {x i              : Ti } ≺ G i i ↾ r for i ∈ I
       We project the global context after transition to r.
       hΓ ′ ≺ p → q li (x i :Ti ).G i′ i ∈I i ↾ r = hΣr ′ ≺ ⊔i ∈I li (x i :Ti ).Li′ i
                                                            {p, q}
       where Σr ′ = Γ ′ ↾ r and hΣi′ ≺ Li′ i = hΓ ′ ∪ {x i         : Ti } ≺ G i′i ↾ r for i ∈ I
                                                                        ϵ
       Since r < subj(α), we have hΣr ∪ {x j0 : Tj } ≺ L j i →− hΣr ′ ≺ L ′j i = hΓ ′ ≺ G j′ i ↾ r from the
       inductive hypothesis.
                                                          ϵ
                                                          − hΣr ∪ {x j0 : Tj } ≺ L j i where j ∈ I
       By [E-Phi], we have hΣr ≺ ⊔i ∈I li (x i :Ti ).Li i →
                                                                    ϵ
                                                               − hΣr ′ ≺ L ′j i
       By transitivity, we have hΣr ≺ ⊔i ∈I li (x i :Ti ).Li i →
       For r, where r , p, r , q, and r ∈ subj(α):
                                                                 α
       Since r ∈ subj(α), we have hΣr ∪ {x j0 : Tj } ≺ L j i −  → hΣr ′ ≺ L ′j i = hΓ ′ ≺ G j′ i ↾ r from the
       inductive hypothesis.
                                                           ϵ
                                                          − hΣr ∪ {x j0 : Tj } ≺ L j i where j ∈ I
       By [E-Phi], we have hΣr ≺ ⊔i ∈I li (x i :Ti ).Li i →
                                                                α
                                                         → hΣr ′ ≺ L ′j i
      By [L-Eps], we have hΣr ≺ ⊔i ∈I li (x i :Ti ).Li i −
  (3) [G-Rec]
      By inductive hypothesis.

   Completeness (⇐): Fix the transition label α = p → q : l(x : T ).
                                                α
   We prove by induction on the reduction of s −→ s ′ , and consider the local types for after projec-
tion.

    • [L-Send] and [L-Recv]. This case arises from the projection of G = p → q {li (x i :Ti ).G i }i ∈I
      (Lemma A.4 case (1) and (2)).
      Let Γ ′ = Γ ∪ {x {p, q} : T }.                                               
      By projection ([P-Send], [P-Recv]), we have hΣp ≺ Lp i = q⊕ li (x i :Ti ).Lpi and
                        
      hΣq ≺ Lq i = p& li (x i :Ti ).Lqi , where Lpi is obtained by hΓ ′ ≺ G i i ↾ p, resp. for q.
                 α
               → s ′ , by inversion of [L-Send] on hΣp ≺ Lp i and [L-Recv] on hΣq ≺ Lq i, we have
       Since s −
       j ∈ I with l j = l, x j = x and Tj = T . By [L-Send] and [L-Recv], the conﬁguration s ′ has
       hΣp ∪ {x : T } ≺ Lpj i, resp. for q.
                                          l           {p, q}
       We can obtain that hΓ ≺ Gi →
                                  − hΓ ∪ {x j                  : Tj } ≺ G j i, via [G-Pfx].

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Statically Verified Refinements for Multiparty Protocols                                                       1:33

     For p and q, the association with s ′ is straight forward. We further show the association for
     r (r , p, q). By projection ([P-Phi]) and plain merging, we have hΣr ≺ Lr i = l(x :T ).Lr j ,
     where Lr j is obtained by the projection hΓ ′ ≺ G j i ↾ r.
                                     l
     [E-Phi] can occur when s →        − s ′ , and hΣr ∪ {x 0 : T } ≺ Lr j i is associated with hΓ ≺ G j i.
   • [L-Eps] ([E-Phi]) and [L-Eps] ([E-Phi]). This case arises from the projection of
     G = s → t {li (x i :Ti ).G i }i ∈I ({s, t} ∩ {p, q} = , Lemma A.4 case (3)).
     Let Γi′ = Γ ∪ {x i{s, t} : T }, Γ0i = Γ ∪ {x i : T }.
     By projection ([P-Send], [P-Recv]), we have hΣp ≺ Ls i = q⊕{li (x i :Ti ).Lsi } and hΣq ≺ Lt i =
      p&{li (x i :Ti ).Lti }, where Lsi is obtained by hΓi′ ≺ G i i ↾ s, resp. for t.
     For r , s, t, the projection gives a uniform silent preﬁx ([P-Phi]), hΣr ≺ Lr i = ⊔i ∈I li (x i :Ti ).Lri ,
     where Lri is obtained by projection hΓ ′ ≺ G i i ↾ r.
     Let the merged label be l 0 , variable be x 0 , value type be T0 and session type be Lr0 . We have
     hΣr ≺ Lr i = l 0 (x 0 :T0 ).Lr0 .
     Let Γ0 = Γ ∪ {x 0i  : T }.

     In this case, [L-Send] (resp. [L-Recv]) cannot apply directly on Lp (resp. Lq ), so the rule
     applied must be [L-Eps].
                                                                                                   α
     By inversion of [L-Eps] with [E-Phi], we have that hΣpi ∪ {x 00 : T0 } ≺ Lp i −              → hΣp ′ ≺ Lp ′ i
     (resp. q).
     Take arbitrary i ∈ I , let si be the conﬁguration associated to hΓ0 ≺ G i i.
                                                       ϵ
     We note that hΣr ≺ Lr i = l 0 (x 0 :T0 ).Lr0 →   − hΣr ∪ {x 00 : T0 } ≺ Lr0 i = hΣri ≺ Lri i ([E-Phi]).
     Despite that Lri is obtained from projection with context Γ ′, the same local type is projec-
     ted with context Γ0 (Lemma A.2). Therefore, we can apply the action α on si , and use the
     inductive hypothesis on hΓ0 ≺ G i i and si .
                                                              α
     We thus have with arbitrary i ∈ I , hΓ0 ≺ G i i −       → hΓ0i′ ≺ G i′i for some hΓ0i′ ≺ G i′i associated
     with si′ . By Lemma A.5, the hΓ0i′ ≺ G i′i are identical, we denote it hΓ0′ ≺ G ′i.
                                                     α
     We can therefore obtain that hΓ ≺ Gi −         → hΓ0′ ≺ s → t {li (x i :Ti ).G ′ }i ∈I i via [G-Cnt].
     We are now left to show the association with s ′:
     From the inductive hypothesis, we have si′ ⇔ hΓ0′ ≺ G ′i.
     For r , s, t, the association result follows from Lemma A.2 and inductive hypothesis, since
     Γi′ projects x i to an irrelevant quantiﬁed variable. For s, t, we use Lemma A.3, which weakens
     the projected x i to a concrete variable.
   • [L-Eps] ([E-Rec]) and [L-Eps] ([E-Rec]). This case arises from the projection of
     G = µt(x ′ :T ′ )hx ′ := Ei.G 1 (Lemma A.4, case (4)).
     We discuss the case where the projection uses [P-Rec-In], since [P-Rec-Out] projects to end
     with no actions to be taken.
     Let Γ ′ = Γ ∪ {x ′{r|r ∈G 1 } : T }.
     For all roles r ∈ G 1 , by projection ([P-Rec-In]), we have hΣp ≺ µt (x ′ :T ′ )hx ′ := Ei.Lr1 i,
     where where Lr1 is obtained by hΓ ′ ≺ G 1 i ↾ r.
     In this case, [L-Send] (resp. [L-Recv]) cannot apply directly on Lp (resp. Lq ), so the rule
     applied must be [L-Eps].
                                                                                                                   α
     By inversion of [L-Eps] with [E-Rec], we have that hΣp ∪ {x ′ω : T ′ } ≺ Lp1 [µt (x ′ :T ′ ).Lp1 /t]i −       →
          ′       ′
     hΣp 1 ≺ Lp 1 i.
     For other roles s , p, q, by inverting [E-Rec], we have that
                                                         α
     hΣs ∪ {x ′ω : T ′ } ≺ Ls1 [µt (x ′ :T ′ ).Ls1 /t]i −→ hΣs 1′ ≺ Ls 1′ i.
     Combining all roles, we can use the inductive hypothesis and obtain


                              Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:34      Fangyi Zhou, Francisco Ferreira, Raymond Hu, Rumyana Neykova, and Nobuko Yoshida

                                                                α
        hΓ ∪ {x ′{r|r∈G 1 } : T ′ } ≺ G 1 [µt(x ′ :T ′ ).G 1 /t]i −
                                                                  → hΓ ′ ≺ G ′i via [G-Rec], and association with
           ′    ′
        hΓ ≺ G i.
      • The rest of the cases are vacuous, since inverting the projections (Lemma A.4) of Lp and Lq
        leads to incompatible shapes of global type G.
                                                                                                               

A.3     Proof of Theorem 4.12
                                                                                                α
                                                                                  → hΓ ′ ≺
        If hΓ ≺ Gi is a well-formed global type under typing context, and hΓ ≺ Gi −
           ′         ′    ′
         G i, then hΓ ≺ G i is well-formed.

                                                                               α
                                                               → hΓ ′ ≺ Gi.
   Proof. By induction on the reduction of global type hΓ ≺ Gi −
                                                         p→q:l j (x j :T j )       {p, q}
      • [G-Pfx] hΓ ≺ p → q {li (x i :Ti ).G i }i ∈I i −−−−−−−−−−→ hΓ ∪ {x j         : Tj } ≺ G j i
        There are three cases for projection to consider: [P-Send], [P-Recv], and [P-Phi]. In all cases,
                                            {p, q}
        the premises state that hΓ ∪ {x i          : Ti } ≺ G i i ↾ p = hΣi ≺ Li i, which indicates that all
        continuations are projectable for all indices.
                                                         α               
      • [G-Cnt] hΓ ≺ p → q {li (x i :Ti ).G i }i ∈I i −  → hΓ ′ ≺ p → q li (x i :Ti ).G i′ i ∈I i
        From inductive hypothesis, we have that for all index i ∈ I , if hΓ ∪ {x j : Tj } ≺ G j i is well-
        formed, then hΓ ′ ≺ G j′ i is well-formed.
        In all three cases of projection, the premises state that Σ ⊢ Ti ty for all index i ∈ I . Therefore,
        the context hΓ ∪ {x j : Tj } ≺ G j i is also well-formed.
                                                          
        We are left to show that hΓ ′ ≺ p → q li (x i :Ti ).G i′ i ∈I i is well-formed: we invert the
        premise of projection of hΓ ≺ p → q {li (x i :Ti ).G i }i ∈I i and apply Lemma A.3.
                                                 α
      • [G-Rec] hΓ ≺ µt(x :T )hx := Ei.Gi −      → hΓ ′ ≺ G ′i
        By inductive hypothesis.
                                                                                                               

A.4     Proof of Theorem 4.14
        If hΓ ≺ Gi is a well-formed global type under context, then hΓ ≺ Gi satisﬁes progress.

   Proof. By induction on the structure of global types G. Using Theorem 4.10, we are suﬃcient
                      α
                     → hΓ ′ ≺ G ′ i, and apply the theorem for the progress of associated conﬁg-
to show that hΓ ≺ Gi −
uration.
      • G = p → q {li (x i :Ti ).G i }i ∈I .
        Since the index set I must not be empty, we can pick an index i ∈ I and apply [G-Pfx].
      • G = µt(x :T )hx := Ei.G ′
        Since recursive types must be contractive, we have that G ′ [µt(x :T ).G ′ /t] , G ′. Furthermore,
        the substituted type is closed. We can apply [G-Rec].
      • G = thx := Ei
        Vacuous, since well-formed global type cannot have free type variable.
      • G = end
        Corresponds to the case where all local types are end.
                                                                                                               

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Statically Verified Refinements for Multiparty Protocols                                                     1:35

B ADDITIONAL DETAILS ON CODE GENERATION
B.1 Communicating Finite State Machines (CFSMs) (Toolchain Internals)
Communicating Finite State Machines (CFSMs, [Brand and Zaﬁropulo 1983]) correspond to local
types projected from global types, as shown in [Deniélou and Yoshida 2013]. We deﬁne the CFSM
as a tuple (Q, q 0, δ ), where Q is set of states, q 0 ∈ Q is an initial state, and δ ⊆ Q × A × Q is a
transition relation, where A is the set of labelled actions (cf. § 4.4).
   Conversion to Communicating Finite State Machines (CFSMs). Scribble follows the pro-
jection deﬁned in § 4.3, and projects a global protocol into local types. Local types can be converted
easily into a Communicating Finite State Machine (CFSM), such that the resulting CFSM does not
have mixed state (i.e. a state does not contain a mixture of sending and receiving outgoing trans-
itions), and that the states are directed (i.e. they only contain sending or receiving actions towards
an identical participant) [Deniélou and Yoshida 2013, Def. 3.4, Prop. 3.1]. We follow the same ap-
proach to obtain a CFSM from the local types with their typing contexts. The CFSM has the same
trace of actions as the local types [Deniélou and Yoshida 2013, Prop. 3.2].
   We generate F⋆ code from the CFSM obtained from projection. We generate records for each
state to correspond to the typing context (explained in Appendix B.2.3), and functions for trans-
itions to correspond to actions (explained in Appendix B.2.1). The execution of the CFSM is detailed
in § 3.4.

B.2 Generated APIs with Refinement Types (Toolchain Output)
Our code generator takes a CFSM as an input to produce type deﬁnitions and an entry point to
execute the protocol. As previously introduced, our design separates program logic and communic-
ations, corresponding to the callbacks type (Appendix B.2.1) and connection type (Appendix B.2.2).
The generated entry point function takes callbacks and a connection, and runs the protocol, which
we detail the internals in § 3.4.
B.2.1 Callbacks. We generate function types for handling transitions in the CFSM, and collect
them into a record of callbacks. When running the CFSM for a participant, appropriate callback
will be invoked when the transition occurs. For sending transitions, the sending callback is invoked
to prompt a value to be sent. For receiving transitions, the receiving callback is invoked with the
value received, so the developer may use the value for processing.
  Generating Handlers for Receiving States. For a receiving state q ∈ Q with receiving action
p → q : l(x : T ) (assuming the current role is q), the receiving callback is a function that takes
the record nqo and the received value of type T , that returns unit (with possible side-eﬀects). The
function signature is given by
                       stateq_receive_l : (st : nqo) → nT ost → ML unit
 The constructor ML is an eﬀect speciﬁcation in F⋆ , which permits all side eﬀects in ML language
(e.g. using references, performing I/O), in contrast to a pure total function permitting no side eﬀects.
nqo is a record correspondent to the local typing context of the state, nT ost is a reﬁnement type,
but the free variables in the reﬁnement types are bound to the record st . We generate one callback
for each receiving action, so that it can be invoked upon receiving a message according to the
message label.
  Generating Handlers for Sending States. For a sending state q ∈ Q with send actions p →
 q : li (x i : Ti ) (assuming the current role is p), for some index i ∈ I , the sending callback is a
function that takes the record nqo, and returns a disjoint union of allowed messages (with possible

                            Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:36      Fangyi Zhou, Francisco Ferreira, Raymond Hu, Rumyana Neykova, and Nobuko Yoshida

side-eﬀects). The constructor of of the disjoint union determines the label of the message, and
takes the payload as its parameter. The function signature is given by
                                                           Ú
                           stateq_send : (st : nqo) → ML       li (nT i ost )
                                                                         i ∈I
 Diﬀerent from receiving callbacks, only one sending callback is generated for each sending state.
This corresponds to the nature of internal choices, that the process implementing a sending preﬁx
makes a single selection; on the contrary, the process implementing a receiving preﬁx must be
able to handle all branches.
  Remark B.1 (Handlers and LTS Transitions). If the callback returns a choice with the re-
ﬁnements satisﬁed, the CFSM is able to make a transition to the next state. When a callback is
provided, against its prescribed type, then the type of the callback type is inhabited and we can
invoke the callback to obtain the label and the value of the payload. A callback function type may
be uninhabited, for instance, when none of the choices are applicable. In this case, the endpoint
cannot be implemented (we show an example below). If the developer provides a callback, then it
must be the case that the speciﬁed type is inhabited. In this way, we ensure the protocol is able to
make progress, and is not stuck due to empty value types7 .

B.2.2 Connections. The connection type is a record type with functions for sending and receiving
base types. The primitives for communications are collected in a record with ﬁelds as follows (S
range over base types int, bool, unit, etc.):
            send_S : nPo → nSo → ML unit                            recv_S : nPo → unit → ML nSo
where nPo is a disjoint union of participants roles and nSo is the data type for S in the programming
language. The communication primitives do not use reﬁnement types in the type signature. We
can safely do so by exploiting the property that reﬁnements can be erased at runtime after static
type-checking.
B.2.3 State Records with Refinements. We generate a type nqo for each state q ∈ Q in the CFSM.
The type nqo is a record type corresponding to the local typing context in the state. For each
variable in the local typing context, we deﬁne a ﬁeld in the encoded record type, corresponding
to the reﬁnement type in the typing context. Since reﬁnement types allow dependencies in the
typing context, we exploit the feature of dependent records in F⋆ to encode the dependencies.
   We use the smallest typing context associated with the CFSM state for the generated record type.
The typing context can be computed via a graph traversal of the CFSM, accumulating variables in
the local type preﬁx along the traversal.

B.3    Verified Endpoint Implementation (User Input)
To implement an endpoint, a developer needs to provide a record of type callback, containing
individual callbacks for transitions, and a record of type connection, containing functions to send
and receive values of diﬀerent base types. The two records are passed as arguments to the entry
point function run to execute the protocol.
   The design of connection record gives freedom for the developer to implement any transport
layer satisfying ﬁrst-in-ﬁrst-out (FIFO) delivery without loss of messages. These assumptions ori-
ginate from the network assumptions in MPST. TCP connections are a good candidate to connect
the participants in the protocol, since they satisfy the assumptions.
7 Since we use a permissive M L eﬀect in the callback type, the callback may throw exceptions or diverge in case of unable

to return. Such behaviours are not in the scope of our interest when we talk about progress.


Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Statically Verified Refinements for Multiparty Protocols                                                    1:37

  To satisfy the data dependencies as speciﬁed in the protocol, the provided callbacks must match
the generated reﬁnement type. The F⋆ compiler utilises the Z3 SMT solver [De Moura and Bjørner
2008] for type-checking, saving developers the need for manual proofs of arithmetic properties.
After type-checking, the compiler can extract the F⋆ code into OCaml (or other targets), where
the reﬁnements at the type level are erased. Developers can then compile the extracted OCaml
program to execute the protocol.
  The resulting program has data dependencies veriﬁed by F⋆ using reﬁnement types. Moreover,
the MPST theory guarantees that the endpoints are free for deadlocks or communication mis-
matches, and conform to the global types.




                           Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
