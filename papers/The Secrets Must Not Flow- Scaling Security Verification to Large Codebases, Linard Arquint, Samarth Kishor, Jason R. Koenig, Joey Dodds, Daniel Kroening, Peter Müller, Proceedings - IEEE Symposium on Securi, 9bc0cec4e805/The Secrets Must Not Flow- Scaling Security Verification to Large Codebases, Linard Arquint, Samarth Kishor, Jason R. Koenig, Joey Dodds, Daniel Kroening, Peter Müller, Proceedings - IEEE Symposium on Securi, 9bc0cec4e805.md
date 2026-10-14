                                                                          The Secrets Must Not Flow:
                                                      Scaling Security Verification to Large Codebases (extended version)

                                                                       Linard Arquint† , Samarth Kishor‡ , Jason R. Koenig‡                              ,
                                                                        Joey Dodds‡ , Daniel Kroening‡ , and Peter Müller†
                                                                           † Department of Computer Science, ETH Zurich, Switzerland
                                                                                          ‡ Amazon Web Services, USA
arXiv:2507.00595v2 [cs.CR] 18 Nov 2025




                                         Abstract—Existing program verifiers can prove advanced prop-                Verifying security properties for protocol implementa-
                                         erties about security protocol implementations, but are difficult       tions is possible as well [12], [13], [14]. For instance,
                                         to scale to large codebases because of the manual effort                Arquint et al. [13] first verify security properties for a
                                         required. We develop a novel methodology called Diodon                  Tamarin model of the protocol in the presence of a Dolev–
                                         that addresses this challenge by splitting the codebase into            Yao (DY) attacker [15] fully controlling the network. Then,
                                         the protocol implementation (the Core) and the remainder                they prove that the protocol implementation refines this
                                         (the Application). This split allows us to apply powerful semi-         model, i.e., that the model justifies every I/O operation
                                         automated verification techniques to the security-critical Core,        performed by the implementation. Refinement guarantees that
                                         while fully-automatic static analyses scale the verification to         the implementation inherits the security properties proven
                                         the entire codebase by ensuring that the Application cannot             for the model.
                                         invalidate the security properties proved for the Core. The                 Existing approaches to verifying protocol implemen-
                                         static analyses achieve that by proving I/O independence, i.e.,         tations are sound only if they are applied to the entire
                                         that the I/O operations within the Application are independent          implementation. Verifying only a subset of the codebase
                                         of the Core’s security-relevant data (such as keys), and that           is unsound, and would fail to prevent, e.g., code seemingly
                                         the Application meets the Core’s requirements. We have                  unrelated to a security protocol accidentally logging key
                                         proved Diodon sound by first showing that we can safely allow           material [16], [17]. However, the required expertise and
                                         the Application to perform I/O independent of the security              annotation overhead make it infeasible to verify entire
                                         protocol, and second that manual verification and static analyses
                                                                                                                 production codebases, which often consist of hundreds of
                                         soundly compose. We evaluate Diodon on two case studies: an
                                                                                                                 thousands of lines of code.
                                         implementation of the signed Diffie–Hellman key exchange and            This work. We present Diodon1 , a proved-sound method-
                                         a large (100k+ LoC) production Go codebase implementing                 ology that scales verification of security properties to large
                                         a key exchange protocol for which we obtained secrecy and               production codebases. Diodon works with codebases where a
                                         injective agreement guarantees by verifying a Core of about             small, syntactically-isolated component implements a security
                                         1 % of the code with the auto-active program verifier Gobra             protocol, whose security argument can be made separately
                                         in less than three person months.                                       from the rest of the code. Our methodology decomposes
                                                                                                                 the overall codebase into this protocol implementation (the
                                                                                                                 Core) and the remainder (the Application).
                                         1. Introduction                                                             This decomposition allows us to apply different verifica-
                                                                                                                 tion techniques to the two parts. We verify the Core using
                                             Security protocols such as TLS or Signal ensure security
                                                                                                                 Arquint et al.’s approach to show refinement w.r.t. a verified
                                         and privacy for browsing the web, sending private messages,
                                                                                                                 Tamarin model, which requires precise reasoning about,
                                         and using cloud services. It is, thus, crucial that these ubiq-
                                                                                                                 e.g., the payloads of I/O operations. Instead of applying the
                                         uitous and critical protocols are designed and implemented
                                                                                                                 same annotation-heavy approach to the Application, we
                                         correctly.
                                                                                                                 use automatic static analyses to ensure that security-relevant
                                             Automatic protocol verifier tools such as Tamarin [1], [2]          data of the Core (in particular, secrets such as keys) does
                                         and ProVerif [3] make it viable to formally verify protocol             not influence any I/O operation within the Application.
                                         models. Their applications to TLS [4], EMV [5], Signal [6],             If this I/O independence holds, the Application cannot
                                         and 5G [7], [8] demonstrate that they can handle realistic              perform any I/O operations that could interfere with the
                                         protocols. However, proving protocol models secure does not             protocol and invalidate its proven security. Additionally, we
                                         result in secure implementations on its own. Coding errors              use static analyses to prove that the Application satisfies the
                                         such as omitted protocol steps (as in the Matrix SDK [9]) or
                                         ignored errors (e.g., returned by a TLS library [10], [11]) may           1. Diodon is a genus of fish known for their inflation capabilities. Erecting
                                         invalidate all security properties proven for the corresponding         spines and scaling their volume by a multiple provide security, like our
                                         models.                                                                 verification methodology.



                                                                                                             1
                                                                                      ifications such as pre- and postconditions and loop invariants,
 Protocol Model                                           Role 1
                                                                                      and attempt to verify the implementation automatically using




                                   ⊑



                                                           ⊑
                                                                                      a satisfiability modulo theories (SMT) solver.
                                            Secrets                                        Auto-active verification is generally sound only if it
     I/O           I/O                                                                is applied to the entire codebase because all callers of a
                                                                   I/O
                                                                                      function must establish its precondition and all functions
                                                         I/O                          must preserve data structure invariants. To ensure that our
           I/O                               I/O
                             I/O                                         I/O          methodology is sound while avoiding this requirement for
 APPLICATION                               CORE                                       the Application, we design our methodology such that static
                                                                                      analyses automatically discharge the proof obligations on
Figure 1. The Diodon methodology. We partition the codebase (blue)
into the module implementing a protocol (Core) and the remaining
                                                                                      the Application. Nevertheless, our methodology is flexible
codebase (Application). We prove that the Core refines (trace inclusion on            enough to permit complex interactions between the Core
the right) a particular role of the verified protocol model (green) by auto-          and Application, e.g., through concurrency and callbacks.
active verification. We apply static analyses to the entire codebase to enforce       Some assumptions remain, in particular, the absence of data
that secrets (red) do not influence (red arrows) the I/O operations (gray             races and undefined behavior; we discuss those in Sec. 4.4.
circles) of the Application and to ensure that the Application cannot
invalidate the security properties proved for the Core. Consequently, Diodon               We prove Diodon sound, providing a blueprint for
guarantees that the entire codebase refines the protocol model (trace inclusion       combining the distinct formalisms of auto-active verifiers and
in the middle) and, thus, enjoys all security properties proved for that model.       static analyses. First, we prove that a DY attacker can simulate
                                                                                      all secret-independent I/O operations. Consequently, if a
assumptions made for the proof of the Core, in particular,                            Tamarin model permits every secret-dependent I/O operation
that the preconditions of Core functions hold when called                             in a codebase, then this codebase refines the model. Second,
from the Application and that the Application does not                                we show that Diodon reasons about these secret-dependent
violate any invariants of Core data structures. These checks                          I/O operations without verifying the entire codebase. I.e., we
ensure that the proofs of the Core and the Application                                construct the corresponding proof for the entire codebase by
compose soundly. Consequently, the entire codebase refines                            starting from the proof for the Core, which we obtain from
the protocol model and enjoys all security properties proved                          auto-active verification, and discharging the remaining proof
for the model. Diodon significantly reduces the proof effort                          obligations using our static analyses.
of verifying software that contains protocol implementations.                              We evaluate Diodon on two Go implementations, a
Fig. 1 illustrates our methodology.                                                   signed Diffie–Hellman (DH) key exchange and a fork of the
    We prove I/O independence for the Application by                                  Amazon Web Services (AWS) Systems Manager Agent (SSM
executing an automatic taint analysis on the entire codebase                          Agent) [19], a large (100k+ LoC) codebase. Part of the latter
to identify I/O operations that are possibly affected by                              codebase implements an experimental protocol for encrypted
secrets (also implicitly via control flow) and checking that all                      shell sessions. We prove secrecy for and injective agreement
such operations are within the Core, which shows that the                             on the session keys established by both protocols. For the
codebase’s decomposition is valid and the Core is sufficiently                        SSM Agent codebase, Diodon allowed us to limit auto-active
large. It would be too restrictive to enforce that all secrets are                    verification to only about 1% of the entire codebase, which
confined within the Core. In most implementations, secrets                            took less than three person months. This demonstrates that
exist outside the Core, e.g., the Application might have                              Diodon enables, for the first time, the verification of strong
access to secrets either via program inputs or the Core’s state                       security properties at the scale of production codebases. Our
(red area within the Application in Fig. 1). It is therefore                          static analyses and case studies are open-source [20], [21].
essential to ensure (via a whole-program analysis) that the
Application does not use these secrets to violate the security                        Contributions. We make the following contributions:
properties of the Tamarin model.                                                      ➤ We present a scalable verification methodology for imple-
    Most I/O operations within the Core correspond to a                                 mentations of security protocols within large codebases,
protocol step and are relevant for proving refinement w.r.t.                            which applies to any codebase with a clear distinction
a protocol model. In production code, however, the Core                                 between the protocol core and the rest of the code.
might also contain operations irrelevant to the protocol, such                        ➤ We identify I/O independence, enabling concise protocol
as logging a protocol step. To reduce the verification effort                           models for complex implementations.
further, we also check I/O independence within the Core                               ➤ We show how to use static analyses to automatically
to classify each I/O operation based on whether it depends                              discharge the Core’s proof obligations, enabling Diodon
on secrets occurring in a protocol run (dark red circles in                             to scale to large codebases.
Fig. 1) or not (gray circles). The former need to be considered                       ➤ We prove the soundness of I/O independence w.r.t. a DY
during the refinement proof, while the latter can safely be                             attacker, and the soundness of Diodon’s combination
ignored. This classification simplifies the refinement proof                            of auto-active verification and static analyses.
and shortens the abstract protocol model.                                             ➤ We evaluate our methodology on two case studies, an
    We prove refinement of the Core w.r.t. a protocol model                             implementation of the signed DH key exchange and an
using an auto-active program verifier [18]. These program                               AWS Systems Manager Agent fork, to demonstrate that
verifiers take as input an implementation annotated with spec-                          Diodon scales to large, production codebases.


                                                                                  2
 1     package core                                                                    1     package main
 3     type Chan struct {                                                              3     import . "core"
 4       psk []byte
 5       cb Cb                                                                      5        func main(psk []byte) {
 6     }                                                                            6          cb := func(m []byte) {fmt.Printf("%x\n", m)}
                                                                                    7          c := InitChannel(psk, cb)
 8     type Cb = func(msg []byte)                                                   8          Send(c, []byte("hello world"))
                                                                                    9          fmt.Printf("Log: message sent.\n")
10     //@ req acc(msg, 1)                                                         10          // fmt.Printf("%v\n", c)
11     //@ func CbSpec(msg []byte)                                                 11        }
13     //@ req cb != nil ==> cb implements CbSpec{}
14     //@ pres psk != nil ==> acc(psk, 1)                                                 Figure 3. Sample Application that is a client of Fig. 2. We omit parsing
15     //@ ens Inv(c)                                                                      of command line arguments for presentation purposes and, thus, assume
16     func InitChannel(psk []byte, cb Cb) (c *Chan) {                                     that psk stores the parsed pre-shared key.
17       //@ inhale AliceIOPermissions()
18       c = &Chan{append([]byte(nil), psk...), cb}                                 1        rule Alice_Send:
19       go continuousRecv(c)                                                       2            let packet = <msg, sign(msg, psk)> in
20       return c                                                                   3            [ Alice_1(rid, A, B, psk), In(msg) ]
21     }                                                                            4          --->
                                                                                    5            [ Alice_1(rid, A, B, psk), Out(packet) ]
23     //@ pres c != nil ==> Inv(c)                                                 6        rule Alice_Recv:
24     //@ pres msg != nil ==> acc(msg, 1)                                          7            let packet = <msg, sign(msg, psk)> in
25     func Send(c *Chan, msg []byte) {                                             8            [ Alice_1(rid, A, B, psk), In(packet) ]
26       if c == nil || msg == nil { return }                                       9          --->
27       fmt.Printf("Send %x\n", msg)                                              10            [ Alice_1(rid, A, B, psk), Out(msg) ]
28       packet := append(msg, HMAC(msg, c.psk)...)
29       sendToNetwork(packet)                                                             Figure 4. Tamarin model excerpt for the MAC protocol implemented in
30     }                                                                                   Fig. 2.
32     /*@ pred Inv(c *Chan) {
33       c != nil && acc(c, 1/2) &&
34       acc(c.psk, 1/2) && AliceIOPermissions() &&                                        two API functions, InitChannel and Send, which
35       (c.cb != nil ==> c.cb implements CbSpec{})
36     } @*/
                                                                                           access this struct, and a predicate Inv that represents the
                                                                                           separation logic [24] invariant used to verify the functions.
     Figure 2. Sample Core for a simple MAC communication. In Go, function                 The definition of Inv includes permissions to access the
     definitions take a list of input parameters and may have a second list for            struct fields and the pre-shared key’s bytes. Separation
     outputs. We omit the continuousRecv goroutine’s implementation that                   logic controls heap access with these permissions to reason
     invokes the c.cb closure (if non-nil) whenever a message has been received.
     We simplify the representation of I/O permissions, which describe permitted           about side effects and to prove data-race freedom, as
     protocol-relevant I/O operations, and omit proof-related statements.                  detailed in Sec. 3.2. Accessibility predicates (acc) represent
                                                                                           permissions in specifications. Their first argument indicates
                                                                                           the heap location and the second argument characterizes
     2. Running Example of Diodon                                                          the permitted access: a value of 1 provides exclusive read
                                                                                           and write access, and any value strictly between 0 and 1
         We demonstrate the core ideas of Diodon on a sample                               provides read-only access that might be shared. For instance,
     program in the Go programming language, which implements                              acc(msg,1) on line 24 passes full permission to write the
     a simple message authentication code (MAC) protocol that                              contents of msg (if it is non-nil) from a caller to function
     sends and receives signed messages using a pre-shared                                 Send, and back to the caller when the function returns. Pre-
     key. In the remainder of this section, we refers to a user                            and postconditions start with the keyword req and ens, re-
     of Diodon. First, we manually split the codebase into                                 spectively, and we use pres as syntactic sugar for properties
     Core and Application following function boundaries. We                                that are preserved, that is, act as pre- and postconditions.
     make the Core as small as possible to reduce auto-active                                  To receive incoming packets, the Core spawns a gor-
     verification efforts while making sure that the entire protocol                       outine (lightweight thread) on line 19 executing the func-
     implementation is contained therein and that we can define an                         tion continuousRecv. We omit its implementation in the
     invariant for the Core’s application programming interface                            figure for space reasons. The goroutine repeatedly calls a
     (API) with which the Application interacts.                                           blocking receive operation, checks the MAC’s validity, and on
         We model the protocol and prove security properties                               success calls the closure that is stored in the struct field cb as
     with the Tamarin protocol verifier [1], [2]. The goal is to                           a callback. If the callback is non-nil, it delivers the resulting
     prove that the entire program, i.e., the composition of the                           message to the Application.
     Core and Application, refines the Tamarin model and,                                      We verify the Core for any callback closure that satisfies
     thus, satisfies the same security properties as the protocol                          the specification CbSpec (cf. line 13 & 10–11), which
     model. We auto-actively verify the Core using Gobra [22]                              states that a caller must pass permission for modifying the
     and apply the automatic Argot [23] static analyses to the                             message to the closure when invoking it and that the closure
     entire codebase.                                                                      does not have to return any permissions. On line 18, we
     Core. The Core (Fig. 2) consists of a struct definition,                              duplicate the pre-shared key (which the Application obtains


                                                                                   3
as a program input) to keep the Core’s memory footprint                protocol-relevant I/O operations and that the chosen Core
separated from the Application. Thus, we can pass half of              is sufficiently large.
the permissions for accessing the struct fields to the goroutine
spawned on line 19 and store the remaining permissions in                   The Core may execute protocol-relevant operations not
the invariant Inv, which is then returned to the caller of             only by performing I/O operations, but also by communi-
InitChannel.                                                           cating with the Application. For example, Alice’s protocol
                                                                       step of taking an arbitrary message from the environment
Application. The Application (Fig. 3) consists of a single             (before signing and sending it), is implemented by the Core
function that creates a closure that will print any incoming           obtaining msg from the Application (line 25 in Fig. 2).
message, initializes the Core with the pre-shared key psk              Similarly, Alice may (after receiving a packet and checking
and this closure, and then sends a message by invoking the             its signature) release its payload to the environment, which
Send function of the Core. In realistic programs, the Appli-           is implemented as passing the payload to the Application
cation might have thousands of lines of code, making auto-             when invoking the closure c.cb (not shown in Fig. 2). To
active verification prohibitively expensive. Diodon allows us          handle such protocol-relevant operations uniformly, we treat
to apply automatic static analyses instead, as detailed below.         them as virtual protocol-relevant I/O operations. This allows
Protocol model. Fig. 4 excerpts our abstract protocol model            us to enforce or assume constraints on the arguments’ taint
as a multiset rewriting system in Tamarin (cf. Sec. 3.1) with          status while creating the necessary proof obligations in the
two protocol roles, Alice and Bob, each starting off with a pre-       next step of the refinement proof. Here, the fact that releasing
shared key psk. Both roles can send and receive unboundedly            the payload is permitted by the protocol model (line 10 in
many packets, each of which are the composition of a                   Fig. 4) informs the taint analysis that the callback’s argument
message plus the appropriate MAC. To make zero assumptions             may be considered as untainted, which allows printing it on
about the messages themselves, we treat them as being                  line 6 in Fig. 3.
attacker-controlled, i.e., the sending role obtains a message              Second, we prove the Core using the auto-active Gobra
from the attacker-controlled network via an In fact, as shown          verifier. This proof includes showing that the protocol model
on line 3. For this protocol model, we prove that all received         permits every protocol-relevant I/O operation, including
messages were previously sent by either Alice or Bob, unless           virtual I/O. Note that step (1) ensures that these operations
the attacker obtains the pre-shared key, which Tamarin                 must all be in the Core. We use an I/O specification for
proves automatically.                                                  each protocol role describing the permitted protocol-relevant
    In order to prove that our program is actually a refinement        I/O operations (cf. Sec. 3.3). In our example, Alice obtains
of this model and, thus, inherits all proven properties, Diodon        the permissions to perform these operations during the
combines auto-active verification and static analyses to obtain        initialization of the Core (line 17) and maintains them
provably-sound guarantees.                                             as part of the invariant (line 34), where inhale adds
Verification. Our goal is to ensure that the composition of the        the specified permissions to the current program state
Application and Core refines the abstract Tamarin model,               by assumption. When performing a protocol-relevant I/O
i.e., the program’s I/O behavior is contained in the model’s           operation, like sendToNetwork, Gobra proves that the
I/O behavior. This refinement implies that any trace-based             I/O specification permits this operation with the specific
safety property proven in Tamarin also holds for the program           arguments. Otherwise, Gobra reports a verification failure.
because the program performs the same or fewer I/O opera-                  Third, since the Gobra proof for the Core assumes that
tions than the protocol model. Diodon splits the refinement            callers respect the functions’ preconditions, Diodon restricts
proof into three steps: We prove that (1) non-protocol I/O is          the class of supported pre- and postconditions such that static
independent of protocol secrets, (2) all remaining I/O refines         analyses are able to prove that the Application satisfies them.
a protocol role, and (3) the proof steps soundly compose.              For example, the precondition of Send requires exclusive
     First, we manually identify protocol-relevant calls to            access for the argument msg; Diodon enforces this condition
I/O operations within the Core. In our example, these are              using a combination of static pointer, escape, and pass-
the sendToNetwork call and the corresponding network                   through analyses to ensure that no other goroutine accesses
receive operation. We then perform an automatic taint                  the memory pointed to by msg. Send’s other precondition
analysis on the entire codebase to prove I/O independence              requires the Core’s invariant to hold, which is established
for all other calls to I/O operations (in our example, the             by InitChannel. The Application could in principle
calls to Printf), i.e., we check that they do not use                  violate this precondition, for example, by creating a Chan
tainted data. Uncommenting line 10 in Fig. 3 would result              instance without calling InitChannel, or by invalidating
in printing all struct fields of variable c including the pre-         the invariant of a Chan instance through field updates or
shared key psk, which is the only secret. I/O independence             concurrency. We apply this combination of static analyses
would correctly fail for this modified program, resulting in an        to prevent all such cases (cf. Sec. 4.3).
error message indicating the flow of secret data to the print
statement. In general, we treat data as a secret (i.e., tainted)           Together, these three proof steps ensure that the program
if the protocol model’s attacker might not know this data.             refines the abstract Tamarin model and inherits the security
Checking I/O independence ensures that we do not miss any              properties proved for the model.


                                                                   4
3. Background                                                                 We perform modular verification, i.e., we reason about
                                                                         each function in an implementation in isolation. To do this,
   In this section, we provide the necessary background                  we equip a function with a specification that consists of
on the verification techniques that we reference in the rest             a pre- and postcondition. A function’s precondition is a
of the paper. We detail verification of abstract protocol                logical formula specifying all valid program states in which
models (Sec. 3.1), verification of implementations (Sec. 3.2),           this function can be called, and a function’s postcondition
and code-level refinement (Sec. 3.3), which transfers security           specifies properties that hold for all valid program states
properties from a protocol model to implementations.                     after executing the function’s body.
                                                                              To reason about heap-manipulating programs, we use
3.1. Protocol Model Verification                                         separation logic [24]. Separation logic allows us to express
                                                                         precisely which heap fragment f a function operates on and
                                                                         provides connectives that split and combine heap fragments,
    We model a security protocol and prove security prop-
                                                                         e.g., when calling another function that operates only on a
erties about it using Tamarin, an automated protocol model
                                                                         subfragment f ′ ⊆ f , we know that the function does not
verifier. A protocol model consists of protocol roles and a
                                                                         modify any heap location in the frame f \ f ′ .
DY attacker that are expressed as multiset rewrite rules. Each
                                                                              Separation logic associates a permission with each heap
rule has the shape L --[ A ]-> R, where L and R are                      location. A permission represents ownership of a particular
multisets of facts and A is a set of actions. The system’s               heap location and is required for each access. We use
state S is a multiset of facts, which is initially empty, and            fractional permissions [27] to distinguish between exclusive
a rule can be applied if L is (multiset) included in S, i.e.,            and shared ownership, which permits multiple threads in a
L ⊆m S. Applying a rule removes the facts in L from and                  concurrent program to simultaneously share ownership of a
adds those in R to the system state, i.e., results in a new              heap location. In specifications, we express permission to a
state S \m L ∪m R. While most facts are user-defined to                  heap location l with fraction p as acc(l,p), cf. Sec. 2.
represent the state of a protocol role, Tamarin uses certain                  The separating conjunction ∗ is akin to regular conjunc-
predefined facts. In particular, In(x) and Out(x) facts                  tion, but requires the sum of the permissions in both conjuncts.
represent receiving and sending a message x from and to the              For instance, acc(l1,1) ∗ acc(l2,1/2) specifies full
attacker-controlled network, respectively. Since Tamarin uses            and half permissions for heap locations l1 and l2, respec-
equational theories to describe otherwise uninterpreted func-            tively. Additionally, this example implicitly specifies that the
tions, such as dec(enc(p, pk (sk )), sk ) = p to describe asym-          heap locations are disjoint, i.e., l1 ̸= l2. Otherwise, if l1
metric decryption (dec) w.r.t. asymmetric encryption (enc),              and l2 were aliased, the permission amounts would add
Tamarin performs multiset inclusion modulo equational                    up to 3/2 contradicting separation logic’s invariant that at
theories. A possible sequence of rule applications forms a               most a full permission exists for a heap location. In our code
trace that consists of each rule application’s set of actions (A).       listings, we overload && to denote separating conjunction.
Tamarin symbolically explores all possible traces involving                   We use separation logic predicates [28] to abstract over
unboundedly many instances of protocol roles to prove a                  individual permissions to heap locations as demonstrated by
security property, or, if the proof fails, provides a trace of           the Core’s invariant in our running example. Conceptually,
an attack as a counterexample to the security property.                  we can treat a predicate instance such as Inv(c) in Fig. 2
    Tamarin’s symbolic DY attacker fully controls the net-               as a shorthand notation for the predicate’s body.
work and can construct new messages by applying symbolic                      A separation-logic proof guarantees safety, in part by
operations to terms it has observed. However, a symbolic                 requiring a proof that each function has sufficient permissions
attacker can neither perform arbitrary computations, nor can             for each heap access. E.g., a buffer overflow corresponds to
it exploit algorithmic weaknesses or side channels such as               accessing an array element out of bounds; this is prevented
timing. Nevertheless, verification using Tamarin guarantees              since allocating an array creates permissions only for
the absence of many relevant vulnerabilities and has proven              in-bound elements. Similarly, data races are prevented since
effective in applications to 5G [7], EMV card protocols [25],            two threads simultaneously writing the same heap location
and the Noise protocol family [26].                                      would require that each thread has write permission for this
                                                                         heap location, which is impossible as there is only a single
3.2. Code-Level Verification                                             write permission for any given heap location.
                                                                              Various separation logic-based program verifiers exist,
    We prove safety and functional properties of an implemen-            including VeriFast [29] and VST [30] for C, Gobra [22]
tation by reasoning about all possible executions statically,            for Go, Nagini [31] for Python, and Prusti [32] for Rust.
without any runtime checks. In this context, the term safety             These verifiers are auto-active, i.e., use manual annotations
expresses that an implementation neither causes runtime                  and proof automation to prove properties about programs.
exceptions nor undefined behavior. In particular, it covers
the absence of memory errors, buffer overflows, and data                 3.3. Code-Level Refinement
races. Functional properties are implementation-specific and
express the desired behavior, e.g., that a sorting algorithm’s              Arquint et al. [13] split verification of security protocol
result is a sorted permutation of the input.                             implementations into two steps: proving security properties


                                                                     5
 CORE                           Auto-Active               Protocol Model              protocol, and the Application consisting of the remaining
                                                   ⊑
                                Verification
                                                                Role 1                code. Typically, this decomposition is natural and follows
   Specification
                                                   ⊑                                  module boundaries as a protocol’s implementation is local-
                               Taint Analysis                  Attacker
 APPLICATION
                                                                                      ized. As illustrated in Fig. 5, this decomposition allows us
                                                                                      to split the proof that the entire codebase refines a protocol
                                                           APPLICATION respects
                               Static Analyses             CORE’s specification       model into three steps and uses the best-suited tool for each
                                                                                      step. We explain in Sec. 4.1 how Diodon identifies which I/O
Figure 5. Diodon proves that the entire codebase (blue) refines a protocol            operations are protocol-relevant by performing a static taint
model (green) by soundly composing auto-active verification with automatic            analysis on the entire codebase. Sec. 4.2 covers the Core’s
static analyses. We auto-actively verify the Core based on its specification          auto-active verification using Gobra proving that protocol-
to show that the protocol-relevant I/O operations refine a protocol                   relevant I/O operations refine a particular protocol role.
role (upper trace inclusion). This specification is partially generated from
the protocol model, which is omitted. The static taint analysis proves                Finally, Sec. 4.3 explains how we discharge the assumptions
that all other I/O operations within the entire codebase refine our attacker          made when auto-actively verifying the Core by performing
model (lower trace inclusion). Lastly, we discharge the Core’s assumptions            static analyses on the Application.
by applying automatic static analyses, proving that the Application
satisfies the calling restrictions expressed in the Core’s specification.
                                                                                      4.1. I/O Independence
for an abstract protocol model using Tamarin, and using an                                One of our key insights is to distinguish between I/O
auto-active program verifier to prove that an implementation                          operations that are relevant for a security protocol from
refines this model. This approach disentangles proving global                         those that are not (e.g., sending log messages to a remote
security properties from local reasoning about implementa-                            server). This distinction has two main benefits. First, protocol-
tions, while exploiting each tool’s automation.                                       irrelevant operations do not have to be reflected in the
    To connect these two steps, Tamarin automatically                                 abstract protocol model, which makes the model concise,
generates an I/O specification for each protocol role in                              more general, and easier to maintain, review, and prove secure.
a given abstract protocol model. A protocol role’s I/O                                Second, by ensuring that protocol-irrelevant I/O operations
specification describes the permitted I/O operations including                        cannot possibly invalidate the security properties proven
their sequential ordering and arguments. By verifying that                            for the protocol model, we do not have to consider them
an implementation executes at most the operations permitted                           during the laborious auto-active refinement proof and instead
by the I/O specification, we prove that all executions of this                        can check simpler properties using automatic static analyses.
implementation result in a trace of I/O operations that is                            We classify all calls to I/O operations as either protocol-
included in the set of traces considered by Tamarin when                              relevant or protocol-irrelevant. In the Core, an I/O operation
verifying the security properties. Thus, the implementation                           is protocol-irrelevant if and only if its specification requires
satisfies the same security properties as the model.                                  no I/O permissions. In contrast, all I/O operations in the
    The I/O specification is expressed in I/O separation                              Application are implicitly considered protocol-irrelevant.
logic [33], a dialect of separation logic, which is readily                               To ensure that I/O operations classified as protocol-
supported by separation logic-based verifiers. I/O separa-                            irrelevant indeed do not interfere with the protocol or
tion logic extends the use of permissions beyond guarding                             invalidate proven security properties of the protocol, we
heap accesses to guarding I/O operations by associating an                            check that they do not use any secret data (such as key
I/O permission with each I/O operation. We equip library                              material); more precisely, we check non-interference between
functions performing I/O operations with a specification that                         protocol secrets and the parameters of these I/O operations.
checks and consumes the corresponding I/O permission.                                 We call this important property of an I/O operation
    Successful code-level verification against the library                            I/O independence. It guarantees that an I/O operation
functions equipped with I/O permissions guarantees that                               cannot possibly invalidate the protocol’s proven security
an implementation performs at most the I/O operations                                 properties: any I/O operation that uses only non-secret
specified in the Tamarin model and respects their sequential                          data could also have been performed by the DY attacker
ordering. Otherwise, verification fails because a prohibited                          and, thus, was already considered by Tamarin during
I/O operation would require an unavailable I/O permission.                            the protocol verification. In other words, proving that all
                                                                                      protocol-irrelevant I/O operations satisfy I/O independence
4. Diodon                                                                             guarantees that they refine our DY attacker (cf. Sec. 5.1).
                                                                                          From a cryptographic perspective, I/O independence
    Our methodology, Diodon, proves security properties for                           allows us to reduce the security of an entire codebase to the
implementations by refinement and scales to large codebases                           security of its Core. This reduction is valid because most
by significantly reducing verification effort. Diodon enables                         of the Application can be treated as part of the attacker,
more concise protocol models than previous approaches                                 while the parts of the Application that manipulate secrets
and leverages fully automatic analyses on most of the                                 (e.g., code that loads long-term keys from disk) are shown
implementation to discharge proof obligations.                                        not to perform I/O, and thus can conceptually be considered
    We manually decompose a codebase into two syntacti-                               part of the Core, without introducing violations of the I/O
cally isolated components, the Core implementing a security                           specification of its protocol role.


                                                                                  6
    We prove I/O independence by performing an automatic              thus, refines this protocol role. This approach is inspired
static taint analysis on the entire codebase that includes            by Arquint et al. [13], but differs in three significant ways.
implicit information flows from control flow. A taint analysis            First, we do not auto-actively verify the entire codebase
checks for a set of sources and sinks whether there are any           and, instead, verify only the Core. As we will discuss
flows of information from a source to a sink. The analysis            in Sec. 4.3, we syntactically restrict the preconditions of
starts at each source, i.e., a function which produces secret         the Core functions so that we can apply automatic static
data, and explores how secret information propagates through          analyses to check that each call from the Application
the program by keeping track of program locations storing             satisfies them, which is necessary for soundness.
a tainted value, i.e., a value that is influenced by a source.            Second, our approach supports codebases that use
We disallow branching on tainted data to avoid information            multiple instances of the Core, e.g., to run multiple roles
flows via control flow.                                               of the protocol or to run the protocol multiple times. Since
    We configure the taint analysis to consider all calls to          Tamarin considers unboundedly many role instantiations,
key-generation functions within the Core and long-term                we can soundly create the required I/O permissions for
secrets that are passed as program inputs, like the pre-              executing a role instance whenever we create a new Core
shared key in our running example, as sources because the             instance. These I/O permissions are bound to an instance’s
DY attacker does not have access to them. This set of initial         unique identifier such that each Core instance has its own set
sources taints all protocol secrets including session keys.           of I/O permissions for executing the security protocol once.
E.g., if the Core implements a DH key exchange, the analysis              Third, to reflect that interactions in the model between the
correctly considers the generated secret key and the resulting        protocol and the environment may manifest as interactions
shared key tainted because the shared key is computed from            between the Core and the Application in the implementa-
the secret key and the other party’s public key. We then              tion, we treat the boundary between them as a virtual network
configure the taint analysis to treat all I/O operations in the       interface and enforce I/O permissions for the corresponding
Application as well as all protocol-irrelevant I/O operations         virtual I/O operations, as we illustrated in Sec. 2.
in the Core as sinks. We use Capslock [34] to identify
such I/O performing functions in the Go standard library.             4.3. Analyzing the Application
We consider all functions with at least one of the following
capabilities as a sink: write to the file system or network,
                                                                           We now show how to scale auto-active verification to
modify the state of the operating system (e.g., os.Setenv),
                                                                      the entire codebase. Applying auto-active verification to an
perform a system call, and execute external programs (e.g.,
                                                                      entire codebase is typically not feasible within the resource
(*os/exec.Cmd).Run).
                                                                      constraints of industrial projects. A key insight of Diodon is
    We run the taint analysis on the entire codebase. If taint
                                                                      that this is not necessary: we can use static analyses to auto-
reaches a sink, verification fails because a secret reached a
                                                                      matically discharge separation logic proof obligations arising
supposedly protocol-irrelevant I/O operation. Otherwise, we
                                                                      in the Application to obtain, together with the verified Core,
have correctly identified the protocol-relevant I/O operations
                                                                      a proof in separation logic for the entire codebase.
(and thereby confirmed that we have correctly delimited the
                                                                           The refinement proof for the Core is valid in the context
Core); it remains to reason about those I/O operations, as
                                                                      of the entire application if (1) each call to a Core function
we discuss next.
                                                                      from the Application satisfies the function precondition,
                                                                      and (2) the Application respects permissions on memory
4.2. Core Refinement                                                  accesses. Our soundness proof for Diodon (cf. Sec. 5.2)
                                                                      ensures that these proof obligations are sufficient and that our
    We auto-actively verify the entire Core, which allows us          novel combination of static analyses can soundly discharge
to state and prove (besides safety and functional correctness)        them. We illustrate these proof obligations and how we
precise constraints about protocol-relevant calls to I/O func-        discharge them by considering the exemplary Core function
tions and their arguments. We prove that the implementation           in Fig. 6, taking two integer pointers as input and returning
uses the payload for each I/O operation specified in the pro-         an integer pointer. This function maintains the Core invariant
tocol model. The corresponding verification effort is feasible        (if c is non-nil), needs full permissions for both inputs, and
since, in industrial codebases like our main case study, the          returns full permissions for the input and output parameters
Core comprises only a small fraction of the codebase.                 (if they are non-nil). Thus, we cannot allow, e.g., the
    We prove that the Core refines a protocol role by building        Application to pass two aliased arguments (cf. Sec. 3.2) to
on the approach explained in Sec. 3.3. In particular, we equip        this function or to concurrently access heap locations pointed
each protocol-relevant I/O operation with a specification             to by these arguments as this would violate the precondition,
that requires an I/O permission for executing this operation          i.e., the permissions specified therein.
with the provided arguments. Since we provide exactly the             Implicit annotations. To construct a proof for the entire
I/O permissions justified by the protocol role’s model to             codebase, we enrich the Application with a hypothetical
the Core during its initialization, successful verification           program instrumentation that connects the Application to
with Gobra implies that the Core executes at most the                 the necessary proof obligations imposed by the proof of
protocol-relevant I/O operations permitted by the model and,          the Core. These implicit annotations track the permissions


                                                                  7
                                                                                                                               
1     //@ pres c ̸= nil =⇒ inv(c)                                                 1     //@ assert ⋆l∈lhs acc(l) ⋆ ⋆i∈ihs inv(i)
2     //@ pres a0 ̸= nil =⇒ acc(a0)                                               2     //@ ihs := ihs \ {c}
      //@ pres a1 ̸= nil =⇒ acc(a1)
                                                                                                                               
3                                                                                 3     //@ assert ⋆l∈lhs acc(l) ⋆ ⋆i∈ihs inv(i) ⋆
4     //@ ens r ̸= nil =⇒ acc(r)                                                  4     //@           (c ̸= nil =⇒ inv(c))
5     func (c *Core) ApiFn(a0, a1 *int) (r *int)                                  5     //@ lhs := lhs \ {a0}                   
                                                                                  6     //@ assert ⋆l∈lhs acc(l) ⋆ ⋆i∈ihs inv(i) ⋆
    Figure 6. Example of a signature and specification of a Core API function.    7     //@           (c ̸= nil =⇒ inv(c)) ⋆
                                                                                  8     //@           (a0 ̸= nil =⇒ acc(a0))
                                                                                  9     //@ lhs := lhs \ {a1}                   
    that the Application owns by using sets of heap locations                    10     //@ assert ⋆l∈lhs acc(l) ⋆ ⋆i∈ihs inv(i) ⋆
                                                                                 11     //@           (c ̸= nil =⇒ inv(c)) ⋆
    and a program invariant specifying permissions for the heap                  12     //@           (a0 ̸= nil =⇒ acc(a0)) ⋆
    locations in these sets. More precisely, each thread has a                   13     //@           (a1 ̸= nil =⇒ acc(a1))
    set lhs (short for “local heap set”) for thread-local objects                14     r := c.ApiFn(a0, a1)                    
    such as buffers, and a set ihs (short for “invariant heap set”)              15     //@ assert ⋆l∈lhs acc(l) ⋆ ⋆i∈ihs inv(i) ⋆
                                                                                 16     //@           (c ̸= nil =⇒ inv(c)) ⋆
    for Core instances. Similarly, a global set ghs (“global heap                17     //@           (a0 ̸= nil =⇒ acc(a0)) ⋆
    set”) keeps track of objects that might be shared between                    18     //@           (a1 ̸= nil =⇒ acc(a1)) ⋆
    threads, which becomes relevant later. These sets are mutable                19     //@           (r ̸= nil =⇒ acc(r))
    and, thus, their content depends on a particular program point.              20     //@ lhs := lhs ∪ ({a0, a1, r} \ nil)
    The sets lhs and ihs allow us to state the following local                   21     //@ ihs := ihs ∪ ({c} \ nil)            
                                                                                 22     //@ assert ⋆l∈lhs acc(l) ⋆ ⋆i∈ihs inv(i)
    program invariant that must hold at every program point in
    the Application.                                                                  Figure 7. Conceptually inserted implicit annotations for a Core API call
                                                                                    r := c.ApiFn(a0, a1) in the Application. The assert statements
               Πl ≜ ⋆l∈lhs acc(l) ⋆ ⋆i∈ihs inv(i)                                     solely illustrate our deductions and, thus, can be omitted.

    Here, the iterated separating conjunction ⋆e∈s a(e) conjoins
    the assertions a(e) using separating conjunction for all                          line 5 in Fig. 7, i.e., we would obtain only acc(a0) instead
    elements e in set s. Πl states that a thread holds full                           of acc(a0) ⋆ acc(a1).
    permissions for all objects in lhs and the Core invariant                             We discharge these two proof obligations by checking the
    for all instances in ihs. In addition, these permissions are                      conditions (C6) and (C7) in Fig. 8, resp., using static analyses.
    disjoint allowing the Application to write to heap locations                      We check (C6) by using a thread escape analysis, which
    in lhs without breaking the Core invariant. When a thread                         delivers judgments local(x) for a particular program point
    obtains or gives up permissions, our implicit annotations                         expressing that ∗x is definitely not accessible by any other
    adjust lhs and ihs to maintain the program invariant.                             thread. We show in Sec. 5.2 that (C6) suffices to discharge
        Fig. 7 shows these implicit annotations for calls to                          {a0, a1} ⊆ lhs (if the arguments are non-nil) by proving
    ApiFn. To highlight that each statement in the Application                        a lemma that relates local(x) for a program point p with
    maintains the program invariant, we assert Πl on lines 1                          x ∈ lhs. We obtain (C7) by applying a pointer analysis, which
    and 22. For each permission required by the callee’s precondi-                    computes may-alias information, i.e., pts(x ) for a pointer x,
    tion, we remove the corresponding heap location from one of                       where a ∈ pts(x ) denotes that ∗x may-alias any location al-
    the sets to reflect that ownership is being passed to the callee.                 located at site a. More precisely, we check for each pair of ar-
    Assuming (for now) that the location was originally in the set,                   guments that the sets of locations they may-alias are disjoint,
    this removal extracts the corresponding permission from Πl ,                      which is sufficient as we restrict parameters to be shallow.
    as illustrated by the intermediate assert statements starting on                  Guaranteeing the Core invariant. Similarly to parameters,
    lines 3, 6, and 10 for the three arguments of the call. After                     we have to prove that c ∈ ihs holds such that removing
    the call, we conversely add those heap locations to the sets                      c from ihs on line 2 grants us the Core invariant inv(c),
    for which the callee’s postcondition provides permissions.                        if c is non-nil. In Sec. 5.2, we prove that c ∈ ihs if the
        For each permission in the precondition, if the corre-                        following premises hold. (1) The Core instance c must have
    sponding heap location was contained in one of the sets                           been returned as a result from a Core API function initially
    before the removal operation, then we have effectively proved                     establishing the Core invariant, e.g., InitChannel in
    that the precondition holds (syntactic restrictions ensure                        our running example. (2) All heap modifications in the
    that the preconditions cannot contain constraints other than                      Application must not modify the internal state of the Core
    permission requirements, see below). In the rest of this                          instance, even through an alias, since this could invalidate
    subsection, we explain how we use static analyses to check                        the Core invariant.
    this set containment. Then, we explain the proof obligations                          In a single-threaded program without callbacks from the
    for memory accesses within the Application.                                       Core to the Application, the above premises are sufficient.
    Guaranteeing permissions for parameters. For the argu-                            However, in the presence of these two features, we need to
    ments a0 and a1 (we will discuss the core instance c below),                      ensure that the Application does not call two Core functions
    we need to prove that (1) {a0, a1} ⊆ lhs holds before the                         on the same Core instance simultaneously, which would
    call to ApiFn and (2) a0 and a1 do not alias. If (2) was                          effectively duplicate permissions and, thus, make reasoning
    violated, a1 would no longer be in lhs after removing a0 on                       unsound: (3) The Application must not pass the same Core


                                                                                 8
   Condition           Details                                                     threads, this would require a significantly more sophisticated
C1 Core init           Core instances are created in a function                    static analysis that can reason about the ordering of con-
                       ensuring the invariant in its postcondition                 current executions. Condition (C5) is enforced by checking
C2 No modification     Application does not write to Core                          that the call graph does not contain Core functions invoked
                       instances’ internal state, even through an
                                                                                   transitively from Application callbacks. Allowing such calls
                       alias
C3 Core preservation Core instances are passed only to Core                        would require proving that the same instance is not used in
                       functions that preserve the invariant                       the inner call, which requires a more precise pointer analysis.
C4 Core locality       Core instances are used only in the thread                      Our explanations generalize from the exemplary Core
                       they are created in                                         function in Fig. 6 to arbitrary Core API functions as long
C5 Core callback       Core APIs are not invoked in Applica-
                       tion callbacks                                              as they satisfy the following restrictions on pre- and post-
C6 Parameter locality Parameters to Core APIs are local                            conditions. We support an arbitrary number of input and
C7 Disjoint parameters Parameters to the same Core API call do                     output parameters with arbitrary value and pointer types. Our
                       not alias one another                                       restrictions mandate that Core API functions preserve the
C8 Application access Reads and writes in the Application                          Core invariant and full permissions for each parameter of
                       occur to memory allocated in the Appli-                     pointer type, both only under the condition that the receiver
                       cation or transferred from the Core                         and parameters are non-nil. Additionally, the postcondition
Figure 8. Sufficient conditions checked by our static analyses, grouped into       specifies full permissions for each return parameter if it is
those involving Core instances, other parameters to Core functions, and            non-nil and of pointer type. These restrictions ensure that
memory accesses in the Application.                                                preconditions do not specify functional properties, such as
                                                                                   require an input array to have a certain length, which we
                                                                                   cannot check using our static analyses. As seen with our
reference to more than one thread, and (4) the Application
                                                                                   example in Fig. 6, we cannot rule out that the Application
must not call a Core function in a callback on the same
                                                                                   passes nil as an argument because there is no sound nilness
instance that is invoking the callback.
                                                                                   analysis for Go to the best of our knowledge and, thus, we
    We establish the four premises by checking the condi-
                                                                                   account for this possibility in our restrictions.
tions (C1) to (C5) in Fig. 8. Conditions (C1) and (C3) can be
enforced by checking that the Application calls only Core
functions that establish or preserve the invariant. While the                      Application memory access. Finally, we need to ensure that
postconditions provide this information for Core instances                         the Application accesses only memory to which it has per-
that are passed as arguments or results, our analyses need to                      missions. While we have already established that the Applica-
prevent a subtle loophole: We need to prevent Core functions                       tion does not write to internal state of Core instances (C2),
from allocating a Core instance without establishing its                           we need to particularly consider the case where memory is
invariant and letting the Application access it via global                         transferred after its allocation between the Core and the Ap-
variables or shared memory. We implemented a pass-through                          plication. The other case, namely the Core or Application
analysis computing passf (x, r) for a function f stating that                      allocating memory without transferring it, is straightforward.
outside of calls to f , ∗x definitely passed through return                        I.e., if Core-allocated memory is never transferred to the Ap-
parameter r. We use this pass-through analysis to ensure                           plication then the Application cannot access it. Similarly, if
that all references to Core instances in the Application are                       Application-allocated memory is not transferred to the Core
obtained exclusively through the return parameter, such that                       then the Application retains the corresponding permission.
the postcondition establishes the invariant.                                           Checking condition (C8) is sufficient. If Application-
    To establish (C2), we use a pointer analysis to ensure                         allocated memory is transferred to the Core, our syntactic
that all reads and writes in the Application never access a                        restrictions guarantee that the Core only temporarily borrows
Core instance’s internal state. In particular, we ensure that                      the corresponding permissions until the Core API call
the Application accesses only heap locations that must-not-                        returns. If the Core allocates memory and transfers it to the
alias locations reachable from ihs, i.e., internal state of Core                   Application, the Core must also transfer the corresponding
instances. Since we use a sound pointer analysis, this check                       permissions, which we enforce via our pass-through analysis
conservatively over-approximates the heap locations about                          checking that this transfer happens via a return parameter
which the Core invariant states properties. While it is possi-                     as our syntactic restrictions guarantee that the postcondition
ble to access Core memory without breaking the invariant,                          specifies permissions for this return parameter. Using (C8),
we could not treat the Core invariant as an opaque separation                      we prove that each memory access in the Application is
logic resource when analyzing the Application, which would                         to a location in either lhs or ghs (cf. Sec. 5.2). In the latter
require a static analysis capable of reasoning about fractional                    case, we need to reason about concurrent access. We assume
permissions and arbitrary functional properties.                                   that the Application is free from data races: if two accesses
    For (C4), we use the thread escape analysis to ensure                          race, then the program is invalid according to the Go
that each Core instance does not escape its thread (we show                        specification. If there are no races, then there is some total
local(c) for each call to Core instance c), guaranteeing that                      order in which the threads can atomically pull permission
each thread operates on a disjoint set of Core instances ihs.                      from ghs, perform the access, and then return permissions to
While it is possible to safely pass Core instances between                         ghs before the next thread needs to access the same location.


                                                                               9
4.4. Threat Model, Assumptions, and Limitations                             The employed static analyses assume that the entire
                                                                        codebase is free of data races and, thus, exhibits defined
    The Diodon methodology provides strong guarantees                   behavior only [37]. While we auto-actively prove race
for large codebases, namely that a codebase satisfies the               freedom for the Core, this remains an assumption for the
same trace-based safety properties as the abstract protocol             Application. Our implicit annotations clearly indicate where
model. Like other verification techniques, Diodon relies on             in the Application we rely on this assumption. Additionally,
assumptions about the codebase, execution environment, and              the static analyses do not soundly handle certain hard-to-
the employed tools.                                                     analyze features such as the unsafe package (e.g., allowing
    Diodon considers an arbitrary number of potentially                 arbitrary pointer arithmetic), cgo (i.e., the ability to invoke C
concurrent protocol sessions, allowing the DY attacker to,              functions), or reflection. We rely on the codebase not using
e.g., replay messages across sessions or apply cryptographic            them in a way that would invalidate the analysis results.
operations thereto to construct messages of unbounded size.             Diodon could be extended by additional static analyses to
As is standard for symbolic cryptography, we assume crypto-             reduce these assumptions, e.g., by performing a data race
graphic operations such as signing are perfectly secure, e.g.,          analysis and checking for uses of the unsafe and cgo
the attacker can create valid signatures only if it possesses           packages and reflection. As such, these assumptions are not
the correct signing key. The attacker can obtain such keys              an inherent limitation of Diodon itself. We report case-
only by observing or constructing them, never by guessing.              studies-related limitations of the static analyses in Sec. 6.
    Our methodology allows us to prove that each imple-
mentation individually refines a particular role of an abstract         5. Formalization and Soundness
protocol model. Since the security properties we prove about
an abstract model are typically global, they hold only if each              We provide an overview of Diodon’s soundness proof
involved implementation refines one of the protocol roles.              by highlighting its key steps and main ideas. Readers
Next, we discuss limitations of this refinement proof, grouped          interested in full details may refer directly to App. A,
by limitations of the methodology itself and limitations of             which subsumes this section. We split the soundness proof
our instantiation in Go.                                                into two parts. First, we prove that we can soundly allow
    The Diodon methodology requires a partitioning of a                 protocol-independent I/O operations in a codebase while
codebase into Core and Application, while satisfying the                assuming that we auto-actively verify an entire codebase.
syntactic restrictions for the Core API specifications. This            Second, we relax the requirement of verifying an entire
partitioning limits applicability, not soundness as the taint           codebase by showing that we can still construct a proof for
analysis checking I/O independence guides correct partition-            the entire codebase in separation logic even though only the
ing and fails otherwise. Additionally, Diodon requires the              Core is verified when certain side conditions are satisfied,
absence of undefined behavior in the codebase, which we                 most of which can be discharged by static analyses.
prove for the Core. However, this remains an assumption for
the Application, which could be mitigated by performing                 5.1. I/O Independence
an additional static analysis establishing this property. E.g.,
we could use Astrée [35] for a subset of C and C++. Finally,                As explained in Sec. 4.1, we execute a taint analysis to
we inherit the pattern requirement from Arquint et al. [13],            identify protocol-independent I/O operations in a codebase.
which allows multiple terms to have the same byte-level                 Furthermore, we assume that we have a proof that a code-
representation in general, but requires a unique representation         base c satisfies the Hoare triple [ϕ] c [true], where ϕ is
for terms corresponding to protocol messages.                           an I/O specification providing I/O permissions to execute
    Our instantiation of Diodon in Go uses several tools to             protocol-dependent I/O operations. Protocol-independent I/O
discharge proof obligations, and we rely on the soundness of            operations do not require an I/O permission and, thus,
each tool: the abstract protocol model verifier, the auto-active        the codebase c may contain arbitrarily many protocol-
program verifier, and the static analyses. The risk that any of         independent I/O operations.
these tools is unsound can be mitigated by choosing mature                  We prove in App. A.1that these independent I/O oper-
tools such as Tamarin and Gobra.                                        ations do not violate the security properties proven for the
    More specifically, the Core’s auto-active verification              abstract protocol model by showing that the DY attacker can
relies on trusted specifications for libraries, such as the I/O         simulate these I/O operations. Hence, Tamarin considers
or cryptographic libraries that, e.g., consume I/O permissions          the existence of these I/O operations when proving security
or specify the cryptographic relations between input and                properties for a protocol model. More specifically, we extend
output parameters. Diodon could be combined with verified               the soundness proof by Arquint et al. [38] by an additional
libraries like EverCrypt [36] to reduce this trust assumption.          refinement step. This step defines a more refined protocol
    Furthermore, our taint analysis relies on the correct               model by augmenting a given protocol model with rules
specification of secrets and I/O operations (we use an existing         enabling the protocol roles to perform protocol-independent
tool [34] to identify I/O operations). E.g., not treating the           I/O operations. We then prove that this refined protocol
pre-shared key in the running example as a secret would                 model refines the original protocol model by establishing a
allow us to perform I/O operations in the Application that              refinement relation that simulates protocol-independent I/O
depend on this key.                                                     operations by actions of the DY attacker.


                                                                   10
    The key insight of the I/O independence proof is that we           Programming language. We consider an imperative, con-
split the state of every protocol role instance into two parts.        current, and heap-manipulating programming language in
The first part is involved in the protocol’s execution, e.g.,          which the codebase c is written. To focus on the main ideas,
keeping track of progress therein. The second part is involved         we keep this language simple by restricting the codebase to a
only in the protocol-independent I/O operations. Our refine-           single run of a protocol role and omitting function boundaries,
ment relation leaves the former part unchanged while refining          complex control flow, and callbacks; we separately discuss
the latter to a corresponding state of the DY attacker. We             extensions lifting these restrictions at the end. Thus, we make
map a transition in the augmented protocol model executing             calls to Core functions first-class statements in our language.
a protocol-independent I/O operation to a transition of the            I.e., we consider c := CoreAlloc(ē) to correspond to
DY attacker performing the same I/O operation.                         calling the Core function allocating and initializing a new
    Therefore, we prove that the codebase c refines the                Core instance (cf. InitChannel in the running example)
abstract protocol model R even though the codebase contains            and r̄ := CoreApi_k(c, ē) to correspond to calling any
more I/O operations than specified by the model for this               other Core function (indexed by k) on a Core instance c
protocol role, the difference being all protocol-independent           with arguments ē and results r̄.
I/O operations in c. We prove (||rid c(rid )) || O ≼t R                Implicit annotations. As explained in Sec. 4.3, we con-
(simplified here, see Thm. 3), where we consider unboundedly           ceptually introduce ghost sets to track the permissions for
many instances of the codebase c, parameterized by a run               heap locations owned by the Application. We recall that
identifier rid , O denotes instances of all other verified             each thread has a set lhs for thread-local objects such as
protocol role implementations and the environment including            buffers and a set ihs for Core instances. In addition, a set ghs
the DY attacker, || represents parallel composition, and ≼t            contains heap locations that are shared between threads, and
expresses trace inclusion.                                             a flag used tracks whether the codebase has already used the
                                                                       I/O specification ϕ to create an instance of the Core and,
5.2. Combining Auto-Active Verification and Static                     thus, a run of the corresponding protocol role.
Analyses                                                                    While Fig. 7 demonstrates the implicit annotations to
                                                                       manipulate the mentioned ghost sets for a Core API call,
     In the second part of the soundness proof App. A.2, we            Fig. 9 presents the general algorithm A for inserting these
want to prove the Hoare triple [ϕ] c [true] for an entire              implicit annotations for every statement in our language.
codebase c, such that we can apply the soundness proof’s                    Writing to a heap location (∗x := e) in the case that x
first part, while auto-actively verifying only a small part of         does not point to a thread-local heap location, i.e., x ̸∈ lhs,
c, namely the Core.                                                    and our fork statement are of particular interest. For the
     At a high-level, we prove a Hoare triple for each                 former statement, the implicit annotations wrap the heap
function f in the Core using an auto-active verifier, i.e.,            access in an atomic block to synchronize this access. This
[P ] f [C], where P and Q are f ’s pre- and postconditions.            synchronization is sound as we assume that the Application
Since the Application calls multiple Core functions and                is free of data races, and, thus, a linearization of accesses to a
performs arbitrary I/O and memory operations in between, we            particular heap location exists (we assume that the underlying
have to prove that the Application establishes each invoked            memory model is sequentially-consistent, like Go’s memory
Core function’s precondition and has sufficient permissions            model). Furthermore, we not only temporarily remove x from
to execute its memory operations in order that we obtain a             ghs but also move all heap locations that are transitively
proof in concurrent separation logic [24], [39] for the entire         reachable from e from lhs to ghs because the write operation
codebase c. While not all codebases c have such a proof, we            makes these heap locations become potentially accessible to
prove its existence under certain side conditions that can be          other threads (via the heap location to which x points). Since
discharged using static analyses.                                      our fork statement (fork (x̄) {s}) passes the arguments x̄ to
     The proof sketch proceeds as follows. After presenting a          a newly forked thread executing the statement s, we similarly
simple programming language allowing us to focus on the                move all heap locations that are transitively reachable from
main ideas, we present an algorithm inserting the implicit             x̄ from lhs to ghs. The newly forked thread then starts with
annotations for every statement in our language (cf. Sec. 4.3).        its own, initially empty lhs and ihs as no thread-local heap
The implicit annotations then allow us to define a program             locations and Core instances exist yet.
invariant that each statement in our language maintains, under         Program invariant. With ghost sets and algorithm A defined,
some side conditions. By constructing derivation trees, we             we can define a program invariant that holds at every original
prove that each statement maintains the program invariant and          program point and that each statement maintains. More
make all side conditions apparent. We then prove lemmata               specifically, this program invariant is split into a thread-
showing that all these side conditions hold if our static              local (Πl ) and global (Πg ) part.
analyses succeed on the codebase c. Finally, we compose
the individual proof rules to construct a proof for the entire                    Πl ≜ (⋆l∈lhs acc(l)) ⋆ (⋆i∈ihs inv(i))
codebase c, i.e., [ϕ] c [true], and discuss extensions of our
                                                                                  Πg ≜ acc(ghs) ⋆ (⋆g∈∗ghs acc(g)) ⋆
soundness proof to support features commonly found in
programming languages.                                                                 acc(used) ⋆ (¬(∗used) =⇒ ϕ)



                                                                  11
                      A(skip) ⇝ skip
                A(x := new()) ⇝ x := new(); lhs := lhs ∪nil {x}
                                   (
                                    lhs := lhs \ {e}; x := ∗e; lhs := lhs ∪nil {e}                        if e ∈ lhs
                    A(x := ∗e) ⇝
                                    atomic {∗ghs := ∗ghs \ {e}; x := ∗e; ∗ ghs := ∗ghs ∪nil {e}} otherwise
                                   
                                   lhs := lhs \ {x}; ∗ x := e; lhs := lhs ∪nil {x}                       if x ∈ lhs
                    A(∗x := e) ⇝ atomic { ∗ ghs := ∗ghs \ {x}; lhs := lhs \ (reach(e) ∩ lhs);
                                                                                                          otherwise
                                                 ∗ x := e; ∗ ghs := ∗ghs ∪nil {x} ∪ (reach(e) ∩ lhs)}
                                   

         A(c := CoreAlloc(ē)) ⇝ atomic {∗used := true}; lhs := lhs \ ē; c := CoreAlloc(ē); lhs := lhs ∪nil ē; ihs := ihs ∪nil {c}
      A(r̄ := CoreApi_k(c, ē)) ⇝ ihs := ihs \ {c}; lhs := lhs \ ē; r̄ := CoreApi_k(c, ē); lhs := lhs ∪nil ē ∪ r̄; ihs := ihs ∪nil {c}
                     A(s1 ; s2 ) ⇝ A(s1 ); A(s2 )
               A(fork (x̄) {s}) ⇝ lhs := lhs \ (reach(x̄) ∩ lhs); ∗ ghs := ∗ghs ∪nil (reach(x̄) ∩ lhs); fork (x̄) {lhs := ∅; ihs := ∅; A(s)}
Figure 9. Algorithm A transforms a codebase by inserting ghost statements. We define this algorithm by cases, i.e., describe how A transforms each
statement s to a statement s′ , written as A(s) ⇝ s′ . reach(e) computes the set of transitively reachable heap locations from expression e. The set union
operation ignores nil, as variables might be nil, i.e., S1 ∪nil S2 ≜ (S1 ∪ S2 ) \ nil. This ensures that nil is never contained in any ghost set.


    Since Sec. 4.3 already explains Πl , we briefly explain                     return arguments r̄ of a r̄ := CoreApi_k(c, ē) statement,
Πg here. As ghs and used are shared between threads, we                         respectively, between site a and program point p on trace τ .
treat them as pointers and Πg specifies permissions for the                          More specifically, we use our static analyses to obtain the
corresponding heap locations. Furthermore, Πg specifies                         judgments for each statement in the codebase as shown in
full permissions for each heap location in ∗ghs and the I/O                     Def. 1 and prove in Lemma 10that these judgments are
specification ϕ, unless ϕ has already been used to create a                     sufficient to discharge the side conditions ω. While the
Core instance, i.e., ∗used is set to true. The last separating                  static analyses run on the original program, before applying
conjunct is sufficient for programs that create at most one                     algorithm A, the runtime (non-ghost) behavior is identical
core instance. We later discuss how this conjunct can be                        and so the judgments apply equally to the codebase after
adapted to provide a family of I/O permissions, enabling                        transformation. This proof relies on our assumptions, i.e., the
arbitrarily many Core instances.                                                Application’s data race freedom, the syntactic restrictions
                                                                                for Core functions, and the soundness of our static analyses.
Proof rules. As shown in Fig. 10, we use algorithm A and the
program invariant to define proof rules that have structurally                  Definition 1 (Static analyses for Diodon). In Diodon, we
identical conclusions, namely Πg ⊢ [Πl ] A(s) [Πl ] for                         execute the static analyses on a codebase to obtain the
each statement s. This Hoare triple expresses that executing                    following judgments for every statement s at label ℓ therein,
the statement s, transformed by algorithm A, starting in a                      denoted as j (sℓ ).
context satisfying Πg and state satisfying Πl , maintains this
context and results in a state satisfying Πl . We prove these                           j (x := ∗e) ≜ ∀a, τ. a ∈ pts(e) =⇒ am pre-ℓ
                                                                                                                              τ     (a)
rules sound in App. A.2.2by constructing a proof tree in                                j (∗x := e) ≜ ∀a, τ. a ∈ pts(x ) =⇒ am pre-ℓ
                                                                                                                               τ     (a)
concurrent separation logic [39]. Our proof relies on the side
                                                                                     j (c := CoreAlloc(ē)) ≜ disjoint as (ē) ∧ local ℓam (ē)
conditions ω (cf. Fig. 11) for statements other than sequential
composition and fork. We require that the specification                          j (r̄ := CoreApi_k(c, ē)) ≜ disjoint as (ē) ∧ local ℓam (ē)
of Core functions satisfies our syntactic restrictions as                                                              ∧ local ℓCore (c) ∧ local ℓret (r̄ )
mentioned in Sec. 4.3.
                                                                                where
Discharging side conditions. Since the side conditions ω
refer to containment of heap locations in certain ghost sets                        disjoint as (ē) ≜ ∀i, j. 0 ≤ i < j < len(ē) =⇒
and disjointness of heap locations, we prove several lemmata                                                pts(ē[i ]) ∩ pts(ē[j ]) = ∅
in App. A.2.3to bridge the gap between these side conditions
and the properties that a successful execution of our static                            local ℓam (ē) ≜ ∀e, h, τ. e ∈ set(ē) ∧
analyses provides.                                                                                                as τ (h) ∈ pts(e) =⇒
    Our pointer analysis computes judgments pts(x ) for a                                                      local post-ℓ (e) ∧ am pre-ℓ
                                                                                                                                     τ     (h)
pointer x, where a ∈ pts(x ) denotes that ∗x may-alias any
                                                                                      local ℓCore (c) ≜ ∀h, τ. as τ (h) ∈ pts(c) =⇒
location allocated at site a. Applying our escape analysis
delivers local p (x ) guaranteeing that x points at program                                                    local pre-ℓ (c) ∧ pt pre-ℓ
                                                                                                                                    Core (h, τ )
point p to a heap location that is accessible only by the                               local ℓret (r̄ ) ≜ ∀r, τ. r ∈ set(r̄) =⇒ local post-ℓ (r )
current thread and not by any other thread. Finally, our
pass-through analysis computes the judgments pt pCore (a, τ )                   pre-ℓ and post-ℓ refer to the program points immediately
and pt pret (a, τ ) denoting that a heap location allocated at                  preceding and following the statement at label ℓ, respectively.
allocation site a passed through (pt) the return argument                       as τ (h) returns heap location h’s allocation site for a partic-
of a c := CoreAlloc(ē) statement and through one of the                        ular program trace τ . am pre-ℓ
                                                                                                            τ   (a) denotes that an allocation


                                                                           12
         ω(ssimple )                             Πg ⊢ [Πl ] A(s1 ) [Πl ]     Πg ⊢ [Πl ] A(s2 ) [Πl ]                        Πg ⊢ [Πl ] A(s) [Πl ]
                               (Simple)                                                                (Seq)                                              (Fork)
Πg ⊢ [Πl ] A(ssimple ) [Πl ]                                 Πg ⊢ [Πl ] A(s1 ; s2 ) [Πl ]                            Πg ⊢ [Πl ] A(fork (x̄) {s}) [Πl ]
Figure 10. Proof rules. ssimple ranges over all simple statements; s, s1 , and s2 range over all statements. ω denotes a statement’s side conditions (cf. Fig. 11).



                         ω(x := ∗e) ≜ e ∈ lhs ∪ ∗ghs                                    [ϕ] sinit ; A(c) [true]. This Hoare triple relies on sinit that
                                                                                        initializes lhs, ihs, and ∗ghs to empty sets, as well as sets
                         ω(∗x := e) ≜ x ∈ lhs ∪ ∗ghs                                    the ghost flag ∗used to false. sinit is similar in spirit to the
        ω(c := CoreAlloc(ē)) ≜ ∗ used = false ∧                                        ghost statements that algorithm A inserts as these statements
                                (set(ē) \ nil) ⊆ lhs ∧                                 are necessary to construct a proof for the codebase c.
                                                                                        Cor. 1’s premise states that our static analyses succeed on
                                disjoint(ē)
                                                                                        the codebase c, such that we obtain j (s) for each statement s
    ω(r̄ := CoreApi_k(c, ē)) ≜ (set(ē) \ nil) ⊆ lhs ∧                                 therein, and that we prove a Hoare triple for each Core
                                disjoint(ē) ∧                                          function satisfying the syntactic restrictions.
                                (c ∈ ihs ∨ c = nil)                                         We combine the proof for the entire codebase that we
                                                                                        obtain from Cor. 1 with the result of Sec. 5.1 to obtain
Figure 11. Side conditions for our statements, which are amenable to static             Diodon’s overall soundness result. This result states that
analyses. ω evaluates to true for all statements not listed above and set(l)
returns the set of elements in list l. We implicitly refer to variables’ values,
                                                                                        successfully executing our static analyses on codebase c
e.g., v ∈ S denotes that the value of variable v is contained in set stored             and auto-actively verifying its Core suffices to prove that
in variable S as opposed to the variables’ syntactical representation.                  the traces of executing c together with other verified imple-
                                                                                        mentations and the environment are contained in the traces
                                                                                        described by the abstract protocol model.
site a is Application-managed on trace τ at the program
point pre-ℓ. An allocation site a is Application-managed if                             Theorem 2 (Overall soundness). Suppose Cor. 1’s an-
a is either within the Application or the Core passed the                               tecedent holds, and we established I/O independence. Then,
corresponding heap location as a return argument to the                                 (||rid c(rid )) || O ≼t R (simplified) holds.
Application. We decide whether a is Application-managed
by checking its location in the program text and running our                            Proof sketch. By Cor. 1 and Thm. 3(cf. Sec. 5.1).
pass-through analysis.

Proof construction. While we showed that we can compose                                 5.2.1. Limitations. Our formalization defines a simple
the proof rules in Fig. 10 and discharge their side condi-                              programming language to focus on the main ideas of our
tions ω, it remains to show that we initially establish the                             soundness proof and to show that successfully executing our
global context Πg and the local program invariant Πl , such                             static analyses discharges all side conditions. We believe
that we obtain a proof for the entire codebase c. We close                              this language covers the most critical features like heap
this gap in Cor. 1.                                                                     manipulations and concurrency as these features are relevant
                                                                                        for the results of our static analyses. In addition, we abstract
Corollary 1 (Proof construction). Successfully executing                                each function making up the Core’s API to a dedicated state-
Diodon’s static analyses on a codebase c and the Core’s                                 ment in our language, and assume that the specification of
auto-active verification combined with our assumptions allow                            each such function satisfies our syntactic restrictions Asm. 4.
us to construct a separation logic proof for c.                                         However, there is a slight risk that this language misses Go
    If ∀s, k. s ∈ c ∧ j (s) ∧                                                           features that would be a threat to soundness such as function
                                                                                       boundaries, complex control flow, and callbacks; the former
          s = c := CoreAlloc(ē) =⇒                                                     two features would be straightforward to add, and we discuss
                                                                                       in Sec. 5.2.2 how to add the latter.
              Πg ⊢ [PCoreAlloc (ē)] s [QCoreAlloc (c, ē)] ∧                               To prove a Hoare triple for the entire codebase, we
          
                                                                                        assume that the Application is free of crashes Asm. 2and
              s = r̄ := CoreApi_k(c, ē) =⇒
                                                                                       data races Asm. 3. While our soundness proof does not
              Πg ⊢ [PCoreApi_k (c, ē)] s [QCoreApi_k (c, ē, r̄)] ,                    make any statement in the case that the program crashes,
                                                                                        our compositional proof informally guarantees that the trace
then emp ⊢ [ϕ] sinit ; A(c) [true]                                                      inclusion holds for the program’s prefix up to the program
                                                                                        point at which a crash occurs, such that the crash freedom
where sinit is ghost code creating and initializing the thread-
                                                                                        assumption could be dropped, which we leave to future work.
local ghost sets lhs and ihs for the main thread, as well as
                                                                                        However, data race freedom remains an assumption; more
the global ghost set ∗ghs and the ghost flag ∗used.
                                                                                        generally, we assume the absence of undefined behavior
    We show that we obtain the desired proof for the                                    for programming languages other than Go and our formal-
entire codebase, namely that the codebase satisfies the                                 ized one. This assumption can be mitigated by performing
I/O specification ϕ expressed as the Hoare triple emp ⊢                                 additional static analyses.


                                                                                   13
5.2.2. Extensions. Having covered the main soundness result,            satisfy a particular precondition for the callback, then we can
we discuss two extensions to bridge the gap to realistic                update the ghost sets accordingly. E.g., such a precondition
applications of Diodon as used in our case studies. We first            can specify permissions for heap locations passed to the
lift the restriction of at most one Core instance to allow              callback or that the Core invariant holds.
a codebase to create unboundedly many Core instances.                       In our SSM Agent case study (Sec. 6.1), we make use
Second, we allow the Core to invoke callbacks into the                  of these proof obligations for the callback delivering in-
Application and discuss the side conditions that arise by               coming messages to the Application as we specify that
this extension.                                                         the Core transfers permission for the incoming message
Unboundedly many Core instances. So far, our global                     to the Application. Conceptually, this allows us to add
program invariant Πg contains the separating conjunct                   the corresponding heap location to lhs before executing the
                                                                        statements constituting the callback because the auto-active
              acc(used) ⋆ (¬(∗used) =⇒ ϕ).                              proof guarantees that no statement in the Core thereafter
                                                                        accesses this heap location.
As explained in App. A.1, each execution of a protocol
role is parameterized by a unique rid . I.e., ϕ and all I/O                 For our case studies, it was not necessary to transfer
permissions that ϕ internally provides are parameterized                permissions from a callback back to the Core via a callback’s
by rid and, thus, are not interchangeable but specific to a             postcondition. Extending Diodon to allow such permission
particular rid . Hence, we can change the separating conjunct           transfers would require an analysis of the callback showing
stated above to                                                         that the Application possesses these permissions while
                                                                        executing the callback and that the corresponding heap
         acc(used) ⋆ (∀rid ̸∈ ∗used =⇒ ϕ(rid ))                         locations do not get accessed by the Application after the
                                                                        callback returns.
providing a family of I/O permissions, where used points
to a ghost set containing the rid s that have already been
used. In addition, we adapt the entire program’s precondition           6. Case Studies
from ϕ to ∀rid . ϕ(rid ) and change the translation A(c :=
CoreAlloc(ē)) to, first, pick a fresh rid ′ such that rid ′ ̸∈             To demonstrate that Diodon scales to large codebases,
∗used and, second, adding rid ′ to ∗used. Picking such a                we evaluate it on the AWS Systems Manager Agent (SSM
fresh rid ′ is always possible since rid ranges over N.                 Agent) [19], a 100k+ lines of code (LoC) production Go
                                                                        codebase. Furthermore, we apply Diodon to a small imple-
Adding callbacks to the Core. So far, we have treated the
                                                                        mentation of the signed Diffie–Hellman (DH) key exchange
statements CoreAlloc(ē) and r̄ := CoreApi_k(c, ē) as
                                                                        to showcase that our methodology applies to other imple-
atomic statements in our language. These two statements are
                                                                        mentations and coding styles.
internally implemented as sequences of statements, which
we hereafter call Core statements. As these statements
constitute the Core, we auto-actively prove that a particular           6.1. AWS Systems Manager Agent
postcondition holds when control transfers back to the
Application after fully executing these statements.                         The AWS Systems Manager Agent (SSM Agent) [19]
    In the presence of callbacks, however, calling into the             provides features for configuring, updating, and managing
Core becomes non-atomic and control flow might transfer                 Amazon EC2 instances, and is widely used by AWS customers.
to the Application before reaching the post-state for which             A fork of this codebase implements a novel protocol which
we know that the postcondition holds. We can treat callbacks            enables encrypted interactive shell sessions with remote host
as temporarily pausing the execution of these auto-actively             machines, similar to the Secure Shell (SSH) protocol, without
verified Core statements to (sequentially) execute some                 needing to open inbound ports or manage SSH keys. This
statements belonging to the Application before eventually               protocol establishes these shell sessions with a handshake
resuming execution of Core statements.                                  protocol involving a signed elliptic-curve DH key exchange to
    With respect to algorithm A and the ghost sets, inter-              derive sessions keys that are subsequently used in the trans-
rupting the execution of Core statements to execute certain             port phase to encrypt the shell commands and their results.
Application statements sapp means that heap locations on                    We apply Diodon by first modeling the protocol
which the Core statements operate are missing from the ghost            in Tamarin and proving secrecy and injective agree-
sets while executing sapp as we remove them from the ghost              ment (Sec. 6.1.1). Second, we partition the codebase into
sets before executing Core statements and put them back only            the code implementing the protocol (the Core) and the re-
after the Core statements’ postcondition holds. Missing per-            maining codebase (the Application), and prove I/O indepen-
missions include both arguments ē and the Core instance c.             dence (Sec. 6.1.2). Third, we auto-actively verify the Core
Therefore, we have to make sure that sapp neither accesses              using Gobra to prove that the Core refines the SSM Agent’s
heap locations to which ē points nor invokes API calls on              role (Sec. 6.1.3). Finally, we apply the automatic static analy-
the Core instance c as the Core invariant might not hold.               ses Argot [23] to discharge the assumptions within the Ap-
    We can lift these restrictions by introducing additional            plication on which the auto-active proof relies (Sec. 6.1.4).
proof obligations for the auto-active verification. More specif-            Fig. 12 overviews each tool’s execution time, for which
ically, if we auto-actively prove that the Core statements              we use the 10 % Winsorized mean of the wall-clock runtime


                                                                   14
                             Tool        Proof Effort      Execution Time               The taint analysis succeeds for the SSM Agent codebase
 Protocol Model            Tamarin          <2 pms            3.30 min              in 29.0 s, proving that there are no taint flows.
 Core Refinement            Gobra           <3 pms            1.17 min
 I/O Independence           Argot          <0.5 pm            0.48 min
 Core Assumptions           Argot          <1.5 pms           2.12 min              6.1.3. Core Refinement. The SSM Agent contains a Go
                                                                                    package called datachannel that implements the protocol.
Figure 12. Execution time for running each tool on the SSM Agent codebase           More precisely, this package contains struct definitions that
and approximate proof effort in person-months (pms) for creating a protocol
model, adding specifications, and adapting the Argot analyses, respectively.        together store all necessary internal state. Additionally, this
                                                                                    package exposes publicly accessible functions to initialize
                                                                                    the internal state, perform a handshake, and send a payload,
across 10 verification runs, measured on a 2023 Apple                               which internally rely on several private functions. We refer
MacBook Pro with M3 Pro processor and macOS 15.6.                                   to these struct definitions and functions as the Core. For
                                                                                    backward compatibility, the Core also implements a legacy
6.1.1. Protocol Model. We model in Tamarin the security                             protocol; we assume that this legacy protocol is disabled.
protocol for establishing a remote shell session between an                         Implementation. Each Core instance corresponds to one
SSM Agent running on an EC2 instance and an AWS customer.                           run of the protocol with a particular AWS customer. During
The protocol offloads all signature operations to the AWS Key                       initialization of a new Core instance, the Core starts a new
Management Service (KMS) [40] such that neither protocol                            thread, responsible for receiving and processing incoming
role has to manage their own signing keys. We model the                             packets for this protocol run, similar to the running example.
connections to KMS as secure channels. Furthermore, the SSM                         If an incoming packet contains a transport phase payload,
Agent sends the asymmetrically-encrypted session keys to a                          this payload is delivered by a callback to the Application.
trusted third party to monitor the transmitted shell commands                       Thus, the Core uses two different threads, one for sending
should this be necessary for regulatory reasons. We provide                         messages and another one for receiving messages, which
the full description of the protocol in App. B.                                     both operate on shared state. This shared state keeps track of
    In Tamarin, we prove secrecy for the two symmetric                              the progress within the protocol and the secret data involved
session keys, i.e., the attacker does not learn these keys unless                   in the protocol, such as the elliptic-curve DH points and the
the SSM Agent’s or customer’s signing key or the monitor’s                          resulting session keys.
secret key is corrupted. Additionally, we prove that the SSM                             Since the shared state is modified during the handshake,
Agent injectively agrees with the customer, and vice versa,                         accesses must be synchronized to avoid data races. Hence,
on their identities and the session keys, unless one of the                         the Core employs Go channels, i.e., lightweight message
three aforementioned corruption cases occurs.                                       passing, to signal a transfer of the shared state’s ownership
    The abstract protocol model amounts to 319 LoC and is                           from one thread to another. During the handshake phase,
automatically verified by Tamarin 1.10.0 in 3.30 min using                          exclusive ownership is transferred such that the threads have
an auxiliary oracle consisting of 75 lines of Python code.                          synchronized write access to the shared state. Afterwards,
                                                                                    the shared state, which includes the established session
6.1.2. Proving I/O Independence. We perform a taint                                 keys, is used in a read-only way permitting both threads
analysis to prove I/O independence. We configure the taint                          to concurrently read the shared state while sending and
analysis to consider all generated elliptic-curve secret keys                       receiving transport messages.
as sources of protocol secrets. We assume that only the                             Auto-active refinement proof. We verify the Core using
Core uses the SSM Agent’s signing keys and do not treat                             Gobra, which proves that the Core refines the Tamarin
KMS responses as taint sources because KMS only sends us                            model’s SSM Agent role. This proof encompasses safety, i.e.,
signatures and never key material. As described in Sec. 4.1,                        we prove that the Core does not crash and has sufficient
we use Capslock’s capability information to automatically                           permissions for every heap access, thus, guaranteeing absence
configure the taint analysis’ sinks.                                                of data races. In particular, this forces us to reason precisely
    We annotated some branching operations, instructing the                         about the accesses to shared state that the two threads within
taint analysis to ignore that the branch condition is tainted.                      the Core perform.
We identified two classes of such branching operations.                                 Due to the intricate interplay of these threads, the result-
The first class is justified by cryptography. E.g., we allow                        ing safety proof is substantial and requires Gobra’s expres-
branching on the success of decrypting a transport message                          sivity. We isolate and axiomatize operations that Gobra does
because leakage is minimal. The second class results from                           not yet support such as simultaneously receiving on multiple
imprecisions of the taint analysis and corresponds to false                         channels and functionally reasoning about serialization and
positives, i.e., the analysis deems a branch condition tainted                      deserialization. For the purpose of the proof, we treat the
although it is not. To avoid another source of false positives,                     Core as a state machine consisting of 12 different states.
we configured the taint analysis to ignore taint escaping the                       This allows us to refer to these states in the Core’s invariant
current thread (which would otherwise always lead to errors).                       and precisely express for each state the permissions and
Such cases could be handled precisely by marking certain                            progress w.r.t. the abstract protocol model.
struct fields as potentially storing concurrently-accessed,                             Although the entire complexity of the proof is encap-
tainted data, such that the analysis can track the taint.                           sulated in the Core’s invariant, function calls to the Core


                                                                               15
must respect its state machine. To avoid exposing the state              from both Core and Application, which could be addressed
machine in these functions’ preconditions and imposing                   by adding calling context information.
additional restrictions on callers, we slightly changed the                  Some Core functions take a pointer to a logger object as a
implementation to perform a dynamic check consisting of                  parameter, which is internally thread-safe and shared between
a comparison with nil and a single integer comparison                    threads. We can safely ignore escape errors due to these
ensuring that the state machine is in a correct state; otherwise,        parameters because the Core does not access any memory
these Core functions return a descriptive error. Thus, the               of the logger object; the pointer is just used as an opaque refer-
Core functions’ specifications are similar to those of our               ence to invoke log functions that are part of the Application.
running example, i.e., mention only the invariant and specify                In summary, this case study demonstrates that Diodon
permissions for parameters without referring to the state                allows one to obtain strong security guarantees for a produc-
machine. While most parameters are of primitive type or                  tion codebase that was not designed with formal verification
shallow, there are a few non-shallow input parameters, which             in mind. The remaining limitations (manual overrides of
the Core treats as opaque. Similarly, the callback from the              false positives in the static analyses, checking condition (C5),
Core to the Application delivers a non-shallow struct for                extremely lightweight dynamic checks enforcing non-nilness
which we ensure that the Core passes permissions for all                 and correct ordering of API calls, and minor code changes)
transitively reachable heap locations to the Application.                are modest compared to the complexity of the overall
    We prove safety and refinement of the Core in 1.17 min               verification challenge and we conjecture that we can lift
for 749 lines of code requiring 3825 lines of specification              them by employing more precise static analyses.
and proof annotations; 1064 thereof are related to the I/O
specification and generated automatically by Tamarin.                    6.2. Signed Diffie–Hellman (DH) Key Exchange

6.1.4. Analyzing the Application. The auto-active proof                      We also apply our approach to a codebase employing in-
for the Core relies on callers satisfying the specified pre-             verted I/O, i.e., has a Core that only produces and consumes
conditions, which we establish using a combination of static             byte arrays corresponding to protocol messages while the
analyses. We implemented automatic checks as described                   Application performs all I/O operations. We adapted the
in Sec. 4.3 for conditions (C1)–(C4) and (C6)–(C8). Condi-               Tamarin model and Go implementation of the signed DH
tion (C5) requires a more precise call graph than is currently           key exchange from Arquint et al. [13] and extended both by a
available in our tool and is, thus, left as future work.                 transport phase that uses the established session key to send
     We implemented our analyses by forking and extending                and receive unboundedly many payloads. Tamarin verifies
the existing Argot tool. Most of our analyses are obtained               the abstract model with 177 lines of code in 3.2 s while
by interpreting the output of an existing analysis; e.g., the            Gobra verifies the Core consisting of 178 lines of code in
parameter alias check uses the off-the-shelf pointer analysis            14.2 s requiring 1726 lines of specification (LoS). Executing
to show parameters do not alias one another.                             all static analyses including the taint analysis takes 9.7 s.
     For some conditions, our static analyses were not able                  This case study clearly exhibits the concept of virtual I/O.
to validate the Application due to tool limitations. For                 The Core performs a virtual input operation for messages that
example, the escape analysis cannot reason about which                   the Application received from the network and forwarded to
fields are accessed after a struct escapes. This can cause the           the Core. Similarly, we perform a virtual output operation for
tool to raise alarms when a struct stores a Core instance in             every message that the Core produces before returning this
a field. We found it was straightforward to rewrite the Core             message to the Application. Therefore, we prove that the
and Application to eliminate these failures. For example,                Tamarin model permits sending this message and in return,
the struct leakage can be fixed by moving the relevant field             we sanitize the message from a taint analysis’ perspective
accesses before thread creation, so that the new thread has              such that the Application can send the message without
access only to the values of those fields and not the entire             causing a false-positive taint flow.
struct, and by extension the Core instance.                                  Diodon separates the justification of sending a particular
     By running our escape analysis, we observed that Core               message from the actual I/O operation. This is important for
instances escape the thread in which they are created because            tackling realistic codebases because identifying the actual
the Application creates a closure that closes over an object             send operation in a call stack is typically difficult as a message
that points to a Core instance. This capture is incidental in            passes through several functions that, e.g., add additional
that the closure does not access the captured Core instance,             protocol headers before a message is handed to the network
which we verified by manual inspection. This capture can                 interface controller.
be eliminated by rewriting the application to reference only
the state necessary in this closure, rather than the full object.        6.3. Discussion
This change would result in a more defensive implementation
by reducing the scope of possibly concurrent accesses.                       Our evaluation demonstrates that Diodon enables us to
     Our pass-through analysis is a prototype that succeeds              efficiently prove that an entire codebase refines a protocol
on our second case study. However, for the SSM Agent, we                 model and therefore is secure. To obtain the security proper-
obtain false positives due to allocations in functions called            ties as proven in Tamarin for a deployment of this protocol,


                                                                    16
we have to prove the implementations of all other protocol             OwlC [48] enables embedding a generated implementation
roles analogously against the same model using Diodon.                 into a codebase, they rely on the Rust type system to
    As shown in Fig. 12, the efforts for applying Diodon to            shield secrets from the rest of the codebase. We avoid this
the SSM Agent is manageable. Thanks to I/O independence,               restriction by checking I/O independence for the Application.
the Tamarin model is concise and can focus on the relevant             In addition, they use a Rust type to ensure that a previously
interactions between the protocol roles. In addition, I/O              established session key is used during a transport phase. In-
independence allows us to apply automatic static analyses              stead, we use the Core invariant to maintain separation logic
at the code-level to reason about all protocol-irrelevant I/O          properties between Core API calls, which is more expressive.
operations. This contrasts existing approaches that would                  An alternative approach extracts an abstract model from
auto-actively verify the entire codebase and prove that every          an implementation, e.g., [4], [6], [49], [50], [51]. However,
I/O operation is explicitly permitted by the model, which is           for this extraction to work, an implementation typically has
completely impractical for this codebase.                              to follow restrictive coding disciplines such that relevant
    To evaluate Diodon’s effectiveness at preventing security          protocol steps can be identified and extracted. To achieve
vulnerabilities, we deliberately introduce bugs in our case            isolation between a verified component and potentially
studies. E.g., our taint analysis correctly fails if the Core’s        malicious code, Kobeissi et al. [6] build on process isolation
internal state, which includes the established session keys,           provided by operating systems and, thus, require verifying
is logged after the handshake. Additionally, sending the DH            the entire critical process. We cannot adopt this approach
secret key in plaintext correctly results in Gobra failing             because it requires changing the codebase heavily to split
to prove refinement w.r.t. the abstract protocol model. The            it into several processes and results in an, for our use
tools’ execution time in the presence of these bugs remains            case, unacceptable overhead, since each process includes
comparable to that for the secure implementations.                     its copy of the Go runtime and the Go standard library.
    By applying Diodon we not only obtain security proper-             Bhargavan et al. [4] impose substantial restrictions on the API
ties for the SSM Agent codebase but we also discovered and             of verified code, e.g., disallowing state preservation between
fixed bugs along the way. Tamarin allowed us to quickly                API calls. Codebases do not normally satisfy these restrictions,
locate and fix a Mallory-in-the-middle (MITM) attack in an             including all our case studies. E.g., they use a session key
earlier and unreleased version of the protocol, which is               for sending a transport message in one API call that was
possible if the intended recipient’s identity is omitted in            established during the handshake, i.e., a previous API call.
the signatures (sig x and sig y in Fig. 36). On the code level,        Existing implementations. Dupressoir et al. [12] embed
we identified and fixed a potential data race in an earlier            a trace storing relevant protocol operations as an auxiliary
and unreleased version of the Core caused by insufficient              data structure for proof purposes into C code implementing
synchronization between the two threads that send and receive          a security protocol. This auxiliary data structure is removed
handshake messages. We uncovered this data race because                before compilation and does not incur any runtime overhead
completing the safety proof for the Core’s earlier version             while enabling reasoning about weak secrecy and non-
is not possible as an additional synchronization point is              injective agreement. Arquint et al. [14] generalize this
necessary to transfer separation logic permissions between             approach to separation logic, making it applicable to a wide
these threads. This demonstrates the power of applying                 range of programming languages and supporting stronger
formal methods because detecting this data race with testing           security properties such as forward secrecy and injective
techniques would require to precisely time the reception of            agreement. However, both approaches require a sufficiently
a handshake message such that the faulty memory access                 strong invariant over this trace to prove security properties. To
occurs and, thus, can be observed.                                     avoid such a trace invariant, Arquint et al. [13] prove security
                                                                       properties on the level of an abstract model using Tamarin’s
7. Related Work                                                        proof automation and prove that an implementation refines
                                                                       the abstract model. All three approaches require verifying
    Much prior work on verifying security protocols exists             the entire codebase using an auto-active verifier (which we
and surveys [41], [42], [43] provide an extensive overview.            do not). We build on the latter approach and, to the best
Hence, we focus on approaches for verifying security prop-             of our knowledge, are the first to relax this requirement to
erties for implementations and their applicability to large            verifying just the Core and reason about the Application
and real-world codebases. We end by comparing Diodon to                using lightweight static analyses.
approaches based on dynamic verification.                              Dynamic verification. Several approaches employ dynamic
Implementation and model generation. One approach to                   checks at runtime to allow for partially verified codebases.
obtain verified protocol implementations generates secure-by-          Agten et al. [52] target single-threaded C code and generate
construction implementations from an abstract model, e.g.,             runtime checks at the boundary between verified and unveri-
[44], [45], [46], [47], [48]. However, these implementations           fied code to test that the verified code’s specification holds.
typically show subpar performance and optimizing them by               To detect violations of properties expressed in separation
hand or integrating them into a larger codebase forfeits proven        logic such as ownership (via permissions) and aliasing, this
security properties. Thus, the abstract model has to cover             approach tracks the heap locations accessed by the verified
the entire functionality (which we do not require). While              codebase at runtime and computes cryptographic hashes


                                                                  17
thereover. It remains unclear whether these checks only at             Acknowledgments
the boundary remain sufficient when targeting concurrent
codebases or whether the runtime overhead increases further.               We thank the Werner Siemens-Stiftung (WSS) for their
To avoid tracking heap locations at runtime, Ho et al. [53]            generous support of this project, Michael Hicks, K. Rustan
copy all heap data at this boundary to rule out aliasing.              M. Leino, and Margarida Ferreira for feedback on drafts of
     Gradual verification (e.g., [54], [55]) combines auto-            this paper, Christoph Sprenger and Joseph Lallemand for
active verification with dynamic checks but aims at helping            helpful discussions, and the anonymous reviewers for their
the proof developer by allowing incomplete specifications.             insightful comments. Parts of this work were conducted by
I.e., gradual verification enables incremental verification            the first author during internships at AWS. Some authors
where each function’s specification is extended over time              are developers of Gobra or Argot, which we disclose as
to eventually obtain a fully specified and verified codebase.          potential non-financial interests.
However, as long as a codebase is not fully specified and
verified, gradual verification requires tracking heap locations        References
at runtime, which results in noticeable runtime overhead.
     SCIO⋆ [56] is an F⋆ transpiler that injects dynamic               [1]   B. Schmidt, S. Meier, C. Cremers, and D. A. Basin, “Automated
checks not only at the boundary between verified and                         analysis of Diffie–Hellman protocols and advanced security properties,”
unverified code but also at call sites of I/O operations.                    in CSF. IEEE, 2012, pp. 78–94.
While they can enforce access policies for I/O operations, it          [2]   S. Meier, B. Schmidt, C. Cremers, and D. A. Basin, “The TAMARIN
remains unclear how this approach extends to cryptographic                   prover for the symbolic analysis of security protocols,” in CAV, ser.
message payloads. To be applicable in our context, we                        LNCS, vol. 8044. Springer, 2013, pp. 696–701.
would need to dynamically check whether a message sent                 [3]   B. Blanchet, “An efficient cryptographic protocol verifier based on
by our Application is indeed protocol-irrelevant and, thus,                  Prolog rules,” in CSFW. IEEE, 2001, pp. 82–96.
does not contain any secrets from the Core—not even in                 [4]   K. Bhargavan, B. Blanchet, and N. Kobeissi, “Verified models and
encrypted form. Like our work, SecRef⋆ [57] considers the                    reference implementations for the TLS 1.3 standard candidate,” in
                                                                             S&P. IEEE, 2017, pp. 483–502.
problem of verifying only a subset of a codebase due to
the otherwise prohibitive proof effort. While they also allow          [5]   D. A. Basin, R. Sasse, and J. Toro-Pozo, “The EMV standard: Break,
                                                                             fix, verify,” in S&P. IEEE, 2021, pp. 1766–1781.
pre- and postconditions at the boundary between verified
and unverified code, they rely on dynamic checks to enforce            [6]   N. Kobeissi, K. Bhargavan, and B. Blanchet, “Automated verification
                                                                             for secure messaging protocols and their implementations: A symbolic
these conditions for heap locations accessible by unverified                 and computational approach,” in EuroS&P. IEEE, 2017, pp. 435–450.
code. For a verified component like our Core, this means
                                                                       [7]   D. A. Basin, J. Dreier, L. Hirschi, S. Radomirovic, R. Sasse, and
that they check the entire invariant at runtime for each API                 V. Stettler, “A formal analysis of 5G authentication,” in CCS. ACM,
call (which we do not), as they treat the unverified code                    2018, pp. 1383–1396.
as potentially modifying a Core instance’s entire state. By            [8]   C. Cremers and M. Dehnel-Wild, “Component-based formal analysis
targeting a single-threaded language (F⋆ ), SecRef⋆ does not                 of 5G-AKA: Channel assumptions and session confusion,” in NDSS.
have to consider concurrent memory accesses (which we do).                   The Internet Society, 2019.
     By contrast, Diodon performs only extremely lightweight           [9]   CVE, “CVE-2021-40823,” 2021. [Online]. Available: https://www.
dynamic checks enforcing non-nilness and correct ordering of                 cve.org/CVERecord?id=CVE-2021-40823
API calls, and checks all other constraints statically to avoid        [10] ——, “CVE-2022-22805,” 2022. [Online]. Available: https://www.
runtime overhead while simultaneously requiring minimal                     cve.org/CVERecord?id=CVE-2022-22805
code changes.                                                          [11] ——, “CVE-2022-22806,” 2022. [Online]. Available: https://www.
                                                                            cve.org/CVERecord?id=CVE-2022-22806
8. Conclusions                                                         [12] F. Dupressoir, A. D. Gordon, J. Jürjens, and D. A. Naumann, “Guiding
                                                                            a general-purpose C verifier to prove cryptographic protocols,” in CSF.
                                                                            IEEE, 2011, pp. 3–17.
    We present Diodon, a novel methodology to scale
verification of security protocol implementations to large             [13] L. Arquint, F. A. Wolf, J. Lallemand, R. Sasse, C. Sprenger, S. N.
                                                                            Wiesner, D. A. Basin, and P. Müller, “Sound verification of security
existing codebases by symbiotically combining powerful                      protocols: From design to interoperable implementations,” in S&P.
auto-active verification of a relatively small part of the                  IEEE, 2023, pp. 1077–1093.
codebase with static analyses that scale to the entire                 [14] L. Arquint, M. Schwerhoff, V. Mehta, and P. Müller, “A generic
codebase. Since Diodon is not inherently limited to Go,                     methodology for the modular verification of security protocol imple-
future work could apply it to codebases written in, e.g., Rust              mentations,” in CCS. ACM, 2023, pp. 1377–1391.
and C. Adapting Diodon to Rust would remove several static             [15] D. Dolev and A. C. Yao, “On the security of public key protocols,”
analyses due to the strong type system, and C has a variety                 IEEE Trans. Inf. Theory, vol. 29, no. 2, pp. 198–207, 1983.
of static analyses and auto-active verifiers that can be used.         [16] CVE, “CVE-2024-47083,” 2024. [Online]. Available: https://www.
Orthogonally, extending Diodon with further static analyses,                cve.org/CVERecord?id=CVE-2024-47083
such as for nilness, would allow us to pass more guarantees            [17] ——, “CVE-2023-6746,” 2023. [Online]. Available: https://www.cve.
from the Application to the Core. We hope our work                          org/CVERecord?id=CVE-2023-6746
spurs both practical and theoretical understanding of how to           [18] K. R. M. Leino and M. Moskal, “Usable auto-active verification,” in
soundly combine proof systems of different expressive power.                Usable Verification Workshop, 2010.



                                                                  18
[19] Amazon Web Services, Inc., “Working with SSM Agent,” 2023.                       [39] V. Vafeiadis, “Concurrent Separation Logic and operational semantics,”
     [Online]. Available: https://docs.aws.amazon.com/systems-manager/                     in MFPS, ser. Electronic Notes in Theoretical Computer Science, vol.
     latest/userguide/ssm-agent.html                                                       276. Elsevier, 2011, pp. 335–351.
[20] L. Arquint, S. Kishor, J. R. Koenig, J. Dodds, D. Kroening, and                  [40] Amazon Web Services, Inc., “AWS Key Management Service,” 2024.
     P. Müller, “The secrets must not flow: Scaling security verification                  [Online]. Available: https://aws.amazon.com/kms/
     to large codebases (artifact),” Sep. 2025. [Online]. Available:
                                                                                      [41] M. Barbosa, G. Barthe, K. Bhargavan, B. Blanchet, C. Cremers,
     https://doi.org/10.5281/zenodo.17099763
                                                                                           K. Liao, and B. Parno, “SoK: Computer-aided cryptography,” in S&P.
[21] ——. (2025, Oct.) The secrets must not flow: Scaling security                          IEEE, 2021, pp. 777–795.
     verification to large codebases. Artifact repository containing
                                                                                      [42] M. Avalle, A. Pironti, and R. Sisto, “Formal verification of security
     the protocol models, the forked SSM Agent’s codebase, a DH
                                                                                           protocol implementations: a survey,” Formal Aspects Comput., vol. 26,
     implementation codebase, and the static analysis tools. [Online].
                                                                                           no. 1, pp. 99–123, 2014.
     Available: https://github.com/viperproject/diodon-artifact
                                                                                      [43] B. Blanchet, “Security protocol verification: Symbolic and computa-
[22] F. A. Wolf, L. Arquint, M. Clochard, W. Oortwijn, J. C. Pereira,
                                                                                           tional models,” in POST, ser. LNCS, vol. 7215. Springer, 2012, pp.
     and P. Müller, “Gobra: Modular specification and verification of Go
                                                                                           3–29.
     programs,” in CAV, ser. LNCS, vol. 12759. Springer, 2021, pp.
     367–379.                                                                         [44] D. Pozza, R. Sisto, and L. Durante, “Spi2Java: Automatic crypto-
                                                                                           graphic protocol Java code generation from Spi calculus,” in AINA.
[23] AWS Labs, “Argot,” 2024. [Online]. Available: https://github.com/
                                                                                           IEEE, 2004, pp. 400–405.
     awslabs/ar-go-tools
                                                                                      [45] D. Cadé and B. Blanchet, “From computationally-proved protocol
[24] J. C. Reynolds, “Separation Logic: A logic for shared mutable data
                                                                                           specifications to implementations,” in ARES. IEEE, 2012, pp. 65–74.
     structures,” in LICS. IEEE, 2002, pp. 55–74.
                                                                                      [46] K. Bhargavan, A. Bichhawat, Q. H. Do, P. Hosseyni, R. Küsters,
[25] D. A. Basin, X. Hofmeier, R. Sasse, and J. Toro-Pozo, “Getting chip
                                                                                           G. Schmitz, and T. Würtele, “DY*: A modular symbolic verification
     card payments right,” in FM (1), ser. LNCS, vol. 14933. Springer,
                                                                                           framework for executable cryptographic protocol code,” in EuroS&P.
     2024, pp. 29–51.
                                                                                           IEEE, 2021, pp. 523–542.
[26] G. Girol, L. Hirschi, R. Sasse, D. Jackson, C. Cremers, and D. A.
                                                                                      [47] J. Gancher, S. Gibson, P. Singh, S. Dharanikota, and B. Parno, “Owl:
     Basin, “A spectral analysis of Noise: A comprehensive, automated,
                                                                                           Compositional verification of security protocols via an information-
     formal analysis of Diffie–Hellman protocols,” in USENIX Security
                                                                                           flow type system,” in S&P. IEEE, 2023, pp. 1130–1147.
     Symposium. USENIX Association, 2020, pp. 1857–1874.
                                                                                      [48] P. Singh, J. Gancher, and B. Parno, “OwlC: Compiling security
[27] J. Boyland, “Checking interference with fractional permissions,” in
                                                                                           protocols to verified, secure, high-performance libraries,” in USENIX
     SAS, ser. LNCS, vol. 2694. Springer, 2003, pp. 55–72.
                                                                                           Security Symposium. USENIX Association, 2025, pp. 5071–5090.
[28] M. J. Parkinson and G. M. Bierman, “Separation Logic and abstraction,”
                                                                                      [49] K. Bhargavan, C. Fournet, A. D. Gordon, and S. Tse, “Verified
     in POPL. ACM, 2005, pp. 247–258.
                                                                                           interoperable implementations of security protocols,” ACM Trans.
[29] B. Jacobs, J. Smans, P. Philippaerts, F. Vogels, W. Penninckx, and                    Program. Lang. Syst., vol. 31, no. 1, pp. 5:1–5:61, 2008.
     F. Piessens, “VeriFast: A powerful, sound, predictable, fast verifier
                                                                                      [50] N. O’Shea, “Using Elyjah to analyse Java implementations of crypto-
     for C and Java,” in NASA Formal Methods, ser. LNCS, vol. 6617.
                                                                                           graphic protocols,” in FCS-ARSPA-WITS-2008, 2008.
     Springer, 2011, pp. 41–55.
                                                                                      [51] M. Aizatulin, A. D. Gordon, and J. Jürjens, “Computational verification
[30] Q. Cao, L. Beringer, S. Gruetter, J. Dodds, and A. W. Appel, “VST-
                                                                                           of C protocol implementations by symbolic execution,” in CCS. ACM,
     Floyd: A Separation Logic tool to verify correctness of C programs,”
                                                                                           2012, pp. 712–723.
     J. Autom. Reason., vol. 61, no. 1-4, pp. 367–422, 2018.
                                                                                      [52] P. Agten, B. Jacobs, and F. Piessens, “Sound modular verification of
[31] M. Eilers and P. Müller, “Nagini: A static verifier for Python,” in CAV
                                                                                           C code executing in an unverified context,” in POPL. ACM, 2015,
     (1), ser. LNCS, vol. 10981. Springer, 2018, pp. 596–603.
                                                                                           pp. 581–594.
[32] V. Astrauskas, P. Müller, F. Poli, and A. J. Summers, “Leveraging
                                                                                      [53] S. Ho, J. Protzenko, A. Bichhawat, and K. Bhargavan, “Noise*: A
     Rust types for modular specification and verification,” Proc. ACM
                                                                                           library of verified high-performance secure channel protocol imple-
     Program. Lang., vol. 3, no. OOPSLA, pp. 147:1–147:30, 2019.
                                                                                           mentations,” in S&P. IEEE, 2022, pp. 107–124.
[33] W. Penninckx, B. Jacobs, and F. Piessens, “Sound, modular and
                                                                                      [54] J. Bader, J. Aldrich, and É. Tanter, “Gradual program verification,” in
     compositional verification of the input/output behavior of programs,”
                                                                                           VMCAI, ser. Lecture Notes in Computer Science, vol. 10747. Springer,
     in ESOP, ser. LNCS, vol. 9032. Springer, 2015, pp. 158–182.
                                                                                           2018, pp. 25–46.
[34] Google, “Capslock,” 2024. [Online]. Available: https://github.com/
                                                                                      [55] J. Wise, J. Bader, C. Wong, J. Aldrich, É. Tanter, and J. Sunshine,
     google/capslock
                                                                                           “Gradual verification of recursive heap data structures,” Proc. ACM
[35] AbsInt Angewandte Informatik GmbH, “Astrée static analyzer for C                      Program. Lang., vol. 4, no. OOPSLA, pp. 228:1–228:28, 2020.
     and C++,” 2025. [Online]. Available: https://www.absint.com/astree
                                                                                      [56] C. Andrici, Ş. Ciobâcă, C. Hritcu, G. Martínez, E. Rivas, É. Tanter,
[36] J. Protzenko, B. Parno, A. Fromherz, C. Hawblitzel, M. Polubelova,                    and T. Winterhalter, “Securing verified IO programs against unverified
     K. Bhargavan, B. Beurdouche, J. Choi, A. Delignat-Lavaud, C. Fournet,                 code in F*,” Proc. ACM Program. Lang., vol. 8, no. POPL, pp. 2226–
     N. Kulatova, T. Ramananandro, A. Rastogi, N. Swamy, C. M. Winter-                     2259, 2024.
     steiger, and S. Z. Béguelin, “EverCrypt: A fast, verified, cross-platform
                                                                                      [57] C. Andrici, D. Ahman, C. Hritcu, R. Icleanu, G. Martínez, E. Rivas,
     cryptographic provider,” in S&P. IEEE, 2020, pp. 983–1002.
                                                                                           and T. Winterhalter, “SecRef*: Securely sharing mutable references be-
[37] Go developers, “The Go memory model,” 2022. [Online]. Available:                      tween verified and unverified code in F*,” CoRR, vol. abs/2503.00404,
     https://go.dev/ref/mem                                                                2025.
[38] L. Arquint, F. A. Wolf, J. Lallemand, R. Sasse, C. Sprenger, S. N.               [58] C. Sprenger, T. Klenze, M. Eilers, F. A. Wolf, P. Müller, M. Clochard,
     Wiesner, D. A. Basin, and P. Müller, “Sound verification of security                  and D. A. Basin, “Igloo: Soundly linking compositional refinement
     protocols: From design to interoperable implementations (extended                     and Separation Logic for distributed system verification,” Proc. ACM
     version),” CoRR, vol. abs/2212.04171, 2022.                                           Program. Lang., vol. 4, no. OOPSLA, pp. 152:1–152:31, 2020.




                                                                                 19
Appendix A.                                                                  We assume that the program’s traces are described by the
Soundness Proof Sketch                                                  labeled transition system (LTS) semantics C , which is pro-
                                                                        vided by the operational semantics of the programming lan-
    To prove Diodon sound, we reason separately about                   guage in which c is implemented2 . α abstracts the program’s
allowing protocol-independent I/O operations in a codebase              traces, e.g., referring to specific function names, to traces of
and combining auto-active verification with static analyses.            operations that match the naming as used in ϕ and δ. δ repre-
    In App. A.1, we prove that a codebase c containing                  sents the set of traces resulting from generating fresh nonces
protocol-dependent and protocol-independent I/O operations              and using received payloads as well as public constants to con-
refines a given Tamarin model if the I/O specification ϕ,               struct and send payloads, as will be made explicit in Def. 3.
corresponding to a protocol role in this Tamarin model,                      Note that Asm. 1 expresses besides the trace inclusion
permits all protocol-dependent I/O operations in the codebase.          itself that the states of ϕ and δ are independent such that their
For this part of the soundness proof, we assume that the                parallel composition is possible. We obtain this independence
entire codebase c satisfies the Hoare triple [ϕ] c [true], where        by successfully executing our taint analysis. In particular,
protocol-independent I/O operations do not consume an I/O               our taint analysis establishes that protocol-independent I/O
permission and, thus, can be performed at arbitrary points              operations do not operate on tainted data. We configure the
within c and independently of the I/O specification ϕ. Such             taint analysis such that long-term and short-term secrets
a Hoare triple could be obtained by auto-actively verifying             known by a protocol role but not the attacker are a source
the entire codebase c, which Diodon does not require.                   of taint. Hence, these I/O operations and all steps necessary
    In App. A.2, we show that we constructively obtain the              to compute their data are either already part of δ or the
Hoare triple [ϕ] c [true] for an entire codebase c using                necessary computation steps can be replicated and added
Diodon by auto-actively verifying only parts thereof, namely            thereto, such that δ is independent of ϕ.
the Core, and executing our static analyses on c, if we                      The other direction, namely that the I/O specification ϕ
assume crash freedom and absence of undefined behavior                  is independent of from δ, holds by construction of ϕ. Since
for the parts of c that are not auto-actively verified.                 we generate ϕ by a series of transformations from a protocol
    By combining both results, we obtain that applying                  role’s abstract model and use syntactically distinct elements to
Diodon to a codebase c proves that c refines a Tamarin                  represent this protocol role’s state and express the transitions
model, despite the presence of protocol-independent I/O                 that form δ, as we shall see next, δ cannot influence ϕ.
operations, and auto-actively verifying the Core only, as long               For a set of function symbols Σ operating over terms,
as we discharge the side conditions using our static analyses.          MD denotes the set of transition rules that the attacker can
                                                                        apply. K(x) represents the fact that the attacker knows the
                                                                        term x and the fact symbols out and in represent that a
A.1. I/O Independence
                                                                        protocol participant sent and might receive a particular term,
                                                                        respectively. Therefore, MD captures all operations available
    We show that we can soundly allow protocol-independent
                                                                        to the attacker, namely receiving a sent term, sending a term,
I/O operations in a codebase by treating these I/O operations
                                                                        adding a public constant to its knowledge, generating a fresh
as a refinement of our attacker model. For this purpose,
                                                                        nonce, and applying a function f ∈ Σ.
we extend Arquint et al.’s soundness proof [38, App. E]
to accommodate such I/O operations, and we adopt their                  Definition 2 (Attacker message deduction rules). As defined
notation for legibility. More specifically, we add these I/O            in [38, Def. 9], MD Σ denotes the set of message deduction
operations to the concrete system and show that this concrete           rules representing our DY attacker for Σ:
system refines an abstract system that is composed of only                                                []
protocol roles and our attacker, which corresponds to a                                    [out(x)]      −
                                                                                                         →       [K(x)]
protocol’s Tamarin model.                                                                               [K(x)]
                                                                                             [K(x)] −−−−→ [in(x)]
    Since we permit a codebase c to perform independent                                                   []
I/O operations in addition to I/O operations permitted by an                                       []    −
                                                                                                         →       [K(x ∈ pub)]
I/O specification ϕ, we adapt the verifier assumption [38,                                                []
                                                                                  [Fr(x ∈ fresh)]        −
                                                                                                         →       [K(x)]
Asm. 1] to account for both types of I/O operations.                                                      []
                                                                             [K(x1 ), . . . , K(xk )]    −
                                                                                                         →       [K(f (x1 , . . . , xk ))]
Assumption 1 (Verifier assumption).                                                                              for f ∈ Σ with arity k
   ⊢α [ϕ] c [true] ∧ T(c, s) = true =⇒ α(C ) ≼ ϕ ||| δ.                     Similarly, we define MD ind
                                                                                                      Σ in Def. 3, which consists of
    I.e., we assume that successfully verifying a program c             the transition rules a protocol-independent component can
against an I/O specification ϕ and successfully executing the           execute. These transition rules represent sending known terms
taint analysis T with some configuration s specifying sources           to the network and receiving terms from the network, using
and sinks of tainted data implies that the program’s traces             public constants, generating nonces, and applying functions to
abstracted under a relabeling function α are included in the            learn new terms. We assume that these transition rules cover
parallel composition of the I/O specification’s traces ϕ and            all operations that a protocol-independent component might
the traces of performing independent I/O operations δ.
                                                                          2. We leave the programming language intentionally unspecified to keep
                                                                        our soundness result general.



                                                                   20
perform. In contrast to MD, MD ind   Σ operates on syntactically           Definition 5 (Re+         e+       e    +           e
                                                                                            env ). Renv = Renv ⊎ Rio where Renv is
                                                                                                                   +
different, reserved fact symbols. Avoiding these name clashes              defined as in [38, Sec. 3.2.2 (6)] and Rio consists of the
simplifies defining a simulation relation for proving Lemma 1.             following multiset transition rules.
     While ind represents knowledge of a particular term,
outind and inind represent a term sent to and received from                                            [λeoutind (rid , x)]
                                                                                                   [] −−−−−     −−−−−−→ [outind (x)]
the network, respectively. ind, outind , and inind are in the                                           [λeinind (rid , x)]
same class of fact symbols as their analogous counterparts                                [inind (x)] −−−−−−−−−−−→ []
K, out, and in, respectively. I.e., K and ind are persistent                                            [λeFr (rid , x)]
fact symbols Σper capturing the property that knowledge                             [Fr(x ∈ fresh)] −−−−ind   −−−−−−−→ []
is monotonically increasing. This means that applying a                                        +
transition rule does not consume such facts and, thus, their               Definition 6 (χS      ). We define the partial synchronization
multiplicity in the multiset comprising the state is irrelevant.           function χ : ( i,rid (Rirole (rid ) ∪ Rind (rid ))) × Re+
                                                                                        +
                                                                                                                                        env →
In contrast, out, in, outind , and inind are in the class of linear        E that synchronizes events        of   the    two systems   |||i,rid
fact symbols Σlin , meaning that applying a transition rule that            Rirole (rid ) ||| Rind (rid ) and Re+env , i.e.,
states such a fact in its premise will remove this fact from the                                 
state while such a fact occurring in the rule’s conclusion adds                                  
                                                                                                   []         if e = F s (rid , x) and
                                                                                                                  e′ = F e (rid , x)
                                                                                                 
it to the state. Additionally, outind and inind are in the class
                                                                                                 
                                                                                                 
                                                                                                 
of output and input fact symbols Σout and Σin , respectively,                    χ+ (e, e′ ) = χ(e, e′ )       if e ̸= F s (rid , x) and
                                                                                                                  e′ ̸= F e (rid , x)
as suggested by their intuitive semantics.                                                       
                                                                                                 
                                                                                                 
                                                                                                 
                                                                                                 
                                                                                                 
Definition 3 (Protocol-independent message deduction rules).                                        undefined otherwise
                                 []                                        where F ∈ {λoutind , λinind , λFrind } and the partial func-
                      [ind(x)] −
                               → [outind (x)]                              tion χ [38, App. E.5] synchronizes labels occurring in Rirole
                                 []
                     [inind (x)] −
                                 → [ind(x)]                                and Reenv and [] denotes the empty transition label.
                                 []
                              [] −
                                 → [ind(x ∈ pub)]                          Lemma 1 (Protocol-independent components refine the
                                 []                                        attacker).
              [Fr(x ∈ fresh)] −
                              → [ind(x)]                                            
                                 []                                                                                         
      [ind(x1 ), . . . , ind(xk )] −
                                   → [ind(f (x1 , . . . , xk ))]                      |||i,rid Rirole (rid ) ||| Rind (rid ) ∥χ+ Re+
                                                                                                                                  env
                                     for f ∈ Σ with arity k                                              
                                                                                 ≼ |||i,rid Rirole (rid ) ∥χ Reenv
where ind, outind , and inind are reserved fact symbols and
ind ∈ Σper , outind ∈ Σout ∩ Σlin , and inind ∈ Σin ∩ Σlin .                   Given Rind (rid ) and Re+env , Lemma 1 states that we can
    Although we present MD ind
                            Σ on the same abstraction level
                                                                           treat the system (on the first line) consisting of possibly
as the attacker deduction rules MD Σ to make them more                     unboundedly many instances of components executing a
legible, these deduction rules are not part of the multiset                protocol role and executing protocol-independent operations
rewriting (MSR) system R. Instead, we transform these rules                as a refinement of the system on the second line that does not
according to [38] and make them part of the component                      have components executing protocol-independent operations
system as described next.                                                  and uses an environment without the rules in R+    io .
    We introduce buffered versions for the outind and inind                    The following proof proceeds by setting up a simulation
facts and split the rules in MD indΣ involving I/O into two
                                                                           relation that merges the states of components executing
separate rules each, which we synchronize using transition                 protocol-independent operations with the environment and
labels. This split allows us to assign half of the rules                   renames certain fact symbols. Using this simulation relation,
to the component executing protocol-independent opera-                     we show that each transition in the concrete system can
tions Rind (rid ) and assign the remaining rules R+ io to the
                                                                           be simulated by the abstract system. While this simulation
environment forming Re+  env . We use χ +
                                          to synchronize  the              is straightforward for transitions executed by components
execution of these now separated rules.                                    that are present in both, the concrete and abstract system,
                                                                           concrete transitions corresponding to protocol-independent
Definition 4 (Rind (rid )). Rind (rid ) consists of the following          operations are more insightful as we show that the abstract
multiset transition rules.
                                                                           environment, namely our DY attacker model, can simulate
                       [λsoutind (rid , x)]                                those transitions.
     [ind(rid , x)] −−−−−       −−−−−−→ []
                        [λsinind (rid , x)]                                Proof. We denote E and E ′ the abstract and concrete
                   [] −−−−−−−−−−−→ [ind(rid , x)]                          systems, respectively, and prove this lemma by establishing
                                  []                                       refinement with a stuttering simulation relation R between
                   [] −−−−−−−−−−−→ [ind(rid , x ∈ pub)]
                        [λsFr (rid , x)]                                   states of the abstract system
                                                                                                         E and statesof the concrete
                 
                   [] −−−−ind −−−−−−−→ [ind(rid , x)]                      system E . I.e., E = |||i,rid Rirole (rid ) ∥χ Reenv and
                                                                                      ′

   ind(rid , x1 ),                []
       ...,       −−−−−−−−−−−→ [ind(rid , f (x1 , . . . , xk ))]
   ind(rid , xk )                           for f ∈ Σ with arity k

                                                                      21
                                                                                                                   F e (rid,x)
                                                    
E ′ = |||i,rid Rirole (rid ) ||| Rind (rid ) ∥χ+ Re+           env . Using                                  s′1,e −−−−−−→Re+  s′2,e
                                                                                                                          env
a stuttering simulation relation in contrast to a standard
                                                                                        and all other component states remain unchanged, i.e.,
simulation relation allows us to relate the abstract and
concrete states even if the concrete system performs                                                            s′2,i,rid = s′1,i,rid
additional transitions that do not have a corresponding                                                        s′2,j,rid ′ = s′1,j,rid ′
transition in the abstract system, i.e., the abstract system can
stutter as long as the observable behaviors of the two systems                                            s′2,ind,j,rid ′ = s′1,ind,j,rid ′
                                                         .          .
remain the same. Accordingly, we use →                  − E and → − E ′ to              for all (j, rid ′ ) ̸= (i, rid ). We now need to distinguish
denote a transition step in the abstract system E and concrete                          the cases where F = λoutind , F = λinind , and F = λFrind .
                                                                .
system E ′ , respectively. Additionally, we use →              − Rirole (rid)
        .                                                                               – F = λoutind : By definition of the transition rule F s ,
and →  − Reenv for transitions performed by the individual
                                                               .                           we have ind(rid , x) ∈ s′1,ind,i,rid and s′2,ind,i,rid =
components in the abstract system and, similarly, →           − Rirole (rid) ,
 .                     .                                                                   s′1,ind,i,rid \m {|ind(rid , x)|}. Similarly, by definition
→
− Rind (rid) and →    − Re+    for the concrete system’s components.
                           env                                                             of F e , we have s′2,e = s′1,e ∪m {|outind (x)|}. By
     The         abstract       states       are      of    the       shape
((si,rid )1≤i≤n, for each rid , se ). We use primed variables                              definition of χ+ , the transition label e is the empty
for referring to concrete states, which are of the shape                                   label []. We simulate this transition in E by stuttering,
((s′i,rid , s′ind,i,rid )1≤i≤n, for each rid , s′e ), i.e., they are                       i.e., s2 = s1 . Since r renames both facts ind(rid , x)
composed of two multisets of facts for each i, rid , and                                   and outind (x) to K(x) and (s1 , s′1 ) ∈ R, we have
one for the environment. Each multiset s′i,rid corresponds                                 K(x) ∈ s1,e . Additionally, the multiset minus and
to the state of instance rid executing the protocol role i,                                multiset union operations cancel out after applying
while s′ind,i,rid corresponds to the state of the component                                r such that s2,e = s1,e . Therefore, (s2 , s′2 ) ∈ R.
executing protocol-independent operations, which is                                     – F = λinind : This case is analogous to F = λoutind .
conceptually co-located with s′i,rid but guaranteed by our                              – F = λFrind : By definition of F s and F e , we have
taint analysis to operate on distinct state.                                                                  Fr(x ∈ fresh) ∈ s′1,e ,
     We use a stuttering simulation relation R, such that
(s, s′ ) ∈ R iff                                                                                        s′2,e = s′1,e \m {|Fr(x)|}, and
  s = ((s′i,rid )1≤i≤n, for each rid , r((∪m      ′            m ′                               s2,ind,i,rid = s′1,ind,i,rid ∪m {|ind(rid , x)|}.
                                                                                                  ′
                                           i,rid sind,i,rid ) ∪ se )),
where s′ = ((s′i,rid , s′ind,i,rid )1≤i≤n, for each rid , s′e ) and r is                  Since (s1 , s′1 ) ∈ R, we obtain Fr(x) ∈ s1,e enabling
the identity function except for the cases specified below. We                            us to apply the attacker’s message deduction rule
                                                                                                                                 []
lift r to operate on multiset of facts. This lifted version re-                           (from MD Σ ) [Fr(x ∈ fresh)] −        → [K(x)], which
moves duplicate K facts because K is a persistent fact symbol.                            results in s2,e = s1,e \ {|Fr(x)|} ∪m {|K(x)|}. Due
                                                                                                                    m

            r(ind(rid , x)) = K(x)                                                       to the renaming function r applied to s′2,ind,i,rid , we
                                      

              r(outind (x)) = K(x) for all rid , x.                                       obtain (s2 , s′2 ) ∈ R.
                                                                                                   ′
                                                                                      • e = χ(e, e ):
                                      
               r(inind (x)) = K(x)
                                                                                        We consider the following four subcases based on the
I.e., to derive se from s′ , we, first, combine all facts in the                        definition of χ:
states of protocol-independent components s′ind,i,rid with
                                                                                        – e = χ(λsF,i,rid (m̄), λeF,i,rid (m̄)) for some F , i, rid ,
s′e by applying multiset union ∪m and, second, rename and                                 m̄:
deduplicate these facts according to the renaming function r.                             By definition, neither Rind (rid ) nor R+
     It is clear that the initial states are related, i.e., (s, s′ ) ∈ R                                                                io contain
                                                                                          any transition rule with a matching transition label.
with s = ((∅, . . . , ∅), ∅) and s′ = ((∅, ∅), . . . , (∅, ∅), ∅). We
                                                                                          Hence, this transition step synchronizes a step in
now show that for all states (s1 , s′1 ) ∈ R and for all concrete
                        e                                                                 Rirole and Reenv . By definition of our composition
transition steps s′1 − →E ′ s′2 there exists an abstract transition                                                  e
     e                                                                                    operators and since s′1 − →E ′ s′2 , we have
s1 −→E s2 such that (s2 , s′2 ) ∈ R. We use the following
naming convention to refer to individual multisets within                                                      λsF,i,rid (m̄)
                                                                                                    s′1,i,rid −−−−−−−→Ri,rid (rid)            s′2,i,rid
the abstract and concrete states, respectively, for j ∈ {1, 2}:                                                                  role
                                                                                                               λeF,i,rid (m̄)
     sj = ((sj,i,rid )1≤i≤n, for each rid , sj,e )                                                      s′1,e −−−−−−−→Reenv                   s′2,e
     s′j = ((s′j,i,rid , s′j,ind,i,rid )1≤i≤n, for each rid , s′j,e )                      and
   Based on the definition of the parallel and synchronizing                                                     s′2,j,rid ′ = s′1,j,rid ′
composition, ||| and ∥χ+ , resp., we distinguish the following                                               s′2,ind,i,rid = s′1,ind,i,rid
                                            e
two cases for the transition step s′1 −    →E ′ s′2 :                                                       s′2,ind,j,rid ′ = s′1,ind,j,rid ′
                      +     s            e
  • e     =        χ (F (rid , x), F (rid , x)) for F                 ∈
    {λoutind , λinind , λFrind }:                                                          for all (j, rid ′ ) ̸= (i, rid ).
                 e
    Since s′1 − →E ′ s′2 , we have:
                               F s (rid,x)
                s′1,ind,i,rid −−−−−−→Rind (rid) s′2,ind,i,rid


                                                                                 22
   Since the renaming function r behaves like the                                Theorem 3 (Soundness). Suppose Asm. 1 holds and that
   identity function for facts occurring in the premise                          we have verified, for each role i, the Hoare triple ⊢πext
                                                                                                                                       ′

   and conclusion of rules λsF,i,rid (m̄) and λeF,i,rid (m̄),                    [ψi (rid )] ci (rid ) [true]. Then
   the same rules can be applied in the abstract
   states s1,i,rid and s1,e . I.e., we have                                                    (|||i,rid πint (Ci (rid ))) ∥χ′ E ≼t R.

                        λsF,i,rid (m̄)                                                Thm. 3 states that composing unboundedly many in-
             s1,i,rid −−−−−−−→Ri,rid (rid)
                                         role
                                                     s2,i,rid                    stances of each role’s LTS Ci (rid ) with the concrete envi-
                        λeF,i,rid (m̄)                                           ronment E refines the protocol model R. While this theorem
                 s1,e −−−−−−−→Reenv                  s2,e                        is identical to [38, Thm. 2], the proof differs since our Asm. 1
                                                                                 considers a larger set of traces per LTS Ci (rid ).
  and (s2 , s′2 ) ∈ R.
– e = χ(e′ , skip) for some e′ ∈ Rirole (rid ):                                  Proof. We decompose the proof into a similar series of
  Then, e′ = e and by definition of our composition                              trace inclusions as [38] but add an additional trace inclusion
                                 e
  operators, we obtain s′1,i,rid −
                                 →Rirole (rid) s′2,i,rid and                     to abstract the protocol-independent I/O operations to the
                                                                                 environment, which contains the DY attacker (cf. Lemma 1).
                         s′2,j,rid ′ = s′1,j,rid ′                                   The first trace inclusion is
                     s′2,ind,i,rid = s′1,ind,i,rid
                                                                                                                    
                                                                                            |||i,rid πint (Ci (rid )) ∥χ′ E
                    s′2,ind,j,rid ′ = s′1,ind,j,rid ′                                                                                         (1)
                                                                                                           ′                         ′
                               s′2,e = s′1,e                                            ≼ |||i,rid π(πext    (Ci (rid ))) ∥χ+ πext (πext (E )),

  for all (j, rid ′ ) ̸= (i, rid ). Since (s1 , s′1 ) ∈ R, we                    where we obtain the first line from the second by pushing
                                                            e                                              ′
  further have s1,i,rid = s′1,i,rid , s1,i,rid −           →Rirole (rid)         the relabeling πext ◦ πext   into the parallel composition, thus
  s2,i,rid , and, thus, s2,i,rid = s′2,i,rid . Therefore,                        changing the set of synchronization labels from χ+ to χ′ .
  (s2 , s′2 ) ∈ R.                                                                   By      combining         Asm.      1,    the   assumption
– e = χ(e′ , skip) for some e′ ∈ Rind (rid ):                                    ⊢πext
                                                                                    ′ [ψi (rid )] ci (rid ) [true], and [38, Thm. 1], we obtain


  e′ ̸= F s (rid , x) for F ∈ {λoutind , λinind , λFrind }                                   ′
                                                                                          π(πext (Ci (rid ))) ≼ Rirole (rid ) ||| Rind (rid ),   (2)
  by definition of χ+ . Therefore, e′ must be the
  transition adding a public constant or applying a                              where Rind (rid ) is a multiset rewriting (MSR) system captur-
  k-ary function f to the state of Rind (rid ). We can                           ing the execution of protocol-independent I/O operations. All
  simulate either transition in the abstract system E                            facts in this MSR system are instantiated with the thread id rid ,
  by performing the corresponding message deduction                              which helps in distinguishing the facts belonging to each Rind
  rule in MD Σ , which updates the abstract state                                instance. Additionally, (2) implicitly specifies that the MSR
  in the same way after merging the states of the                                systems Rirole (rid ) and Rind (rid ) operate independently, i.e.,
  environment and of the components performing                                   on different multisets of facts. By performing the taint analy-
  protocol-independent operations and applying the                               sis, we ensure that Rirole (rid ) does not influence Rind (rid ).
  renaming function r. Thus, (s2 , s′2 ) ∈ R.                                    Checking the opposite, i.e., that Rind (rid ) does not influence
– e = χ(skip, e′ ) for some e′ ∈ Re+          env :                              Rirole (rid ) by performing a second taint analysis is not neces-
  Then, e′ = e and, by definition of the composition op-                         sary. We explicitly track throughout code-level verification the
                                e
  erators, we obtain s′1,e −  →Re+        s′2,e , s′2,i,rid = s′1,i,rid ,        multiset of facts representing the state of Rirole (rid ), which
                                    env
            ′                 ′
  and s2,ind,i,rid = s1,ind,i,rid for all i, rid . By                            is only manipulated by internal and I/O library functions
  definition of χ+ , e cannot have the shape F e (rid , x)                       corresponding to state updates permitted by Rirole (rid ).
  for some rid , x, and F ∈ {λoutind , λinind , λFrind }, which                  Therefore, this state cannot be influenced by Rind (rid ).
  rules out the transitions in R+                            e
                                      io . Thus, e ∈ Renv . Since
                                                                                     We can leverage a general composition theorem [58,
  (s1 , s′1 ) ∈ R, we have s′1,e ⊆m s1,e . Since e’s guard                       Thm. 2.3] that implies that trace inclusion is compositional
  is stable under supermultiset, the rewrite rule e can                          for a large class of composition operators including |||
  be applied in state s1,e , i.e., s1,e −
                                                e
                                              →Reenv s2,e . As this              and ∥Λ . Applying this theorem to (2) and [38, Prop. 2]
  abstract transition only modifies the submultiset s′1,e                        establishes the trace inclusion
                                                                                                                        
  by adding or removing facts for which the renaming                                                     ′                           ′
                                                                                             |||i,rid π(πext (Ci (rid ))) ∥χ+ πext (πext (E ))
  function r behaves as the identity function and leaves                                                                                        (3)
  all other s1,i,rid and s1,e \m s′1,e unchanged, we                                     ≼ |||i,rid Rirole (rid ) ||| Rind (rid ) ∥χ+ Re+
                                                                                                                                 
                                  ′                   m ′                                                                                   env .
  obtain s2,e = r((∪m     i,rid s1,ind,i,rid ) ∪ s2,e ). Thus,
       e
  s1 −→E s2 and (s2 , s′2 ) ∈ R.                                                    Applying Lemma 1 in connection with [38, Lemma 1
                                                                                 & Lemma 2] completes the proof.




                                                                            23
A.2. Combining Auto-Active Verification and Static                               We call S; S and fork (x̄) {S} compound statements, while
Analyses                                                                         all other statements in our language are called simple. When
                                                                                 not relevant, we omit a statement’s label ℓ, which uniquely
     In this subsection, we sketch soundness of our combina-                     identifies the statement in the program text. We use these
tion of auto-active program verification and fully automatic                     labels to refer to the program points before and after each
static analyses by constructing a proof in concurrent separa-                    labeled statement. We abstractly treat c := CoreAlloc(ē)
tion logic [24], [39] for the entire codebase. More specifically,                and r̄ := CoreApi_k(c, ē) as first-class statements in
we give an invariant that is maintained by each statement in                     our language despite being implemented as sequences of
our programming language (App. A.2.1) and present proof                          statement that are considered by our static analyses and the
rules that use, besides certain side conditions, only this                       auto-active program verifier. This is possible because we
invariant in their premises and conclusions (App. A.2.2).                        can treat these statements as opaque boxes from a proof
We use Diodon’s static analyses to discharge these side                          construction point of view as we prove a Hoare triple for
conditions (App. A.2.3). Therefore, we can compose the                           each such statement using the auto-active program verifier.
proof rules to prove ⊢ [ϕ] c [true] for an I/O specification ϕ                       We assume that all memory accesses in the unverified
and an entire codebase c (App. A.2.4).                                           Application neither cause crashes nor data races such that
     To focus on the main proof insights, we deliberately                        we can reason about their effects. While we could have
keep the considered programming language simple (cf.                             avoided assuming data race freedom by defining that all heap
Def. 7) and consider the case where an execution of the                          operations in our language are atomic, we try to stay faithful
codebase c corresponds to at most one execution of a protocol                    to most programming languages, which specify data races
role, which is represented by the I/O specification ϕ. We                        to cause undefined behavior, thus, making this assumption
discuss limitations in App. A.2.5 and extensions lifting these                   necessary.
restrictions in App. A.2.6.
                                                                                 Assumption 2 (Crash freedom). We assume that all heap
Prerequisites. We consider an imperative, concurrent, and
                                                                                 accesses within the Application, x := ∗e and ∗x := e do
heap-manipulating programming language as shown in Def. 7.
                                                                                 not crash4 , i.e., the Application dereferences only pointers
For simplicity, we omit function boundaries and statements
                                                                                 to allocated heap locations as opposed to nil.
creating complex control flow. Furthermore, we assume that
programs are in static single assignment (SSA) form such that                    Assumption 3 (Data race freedom). We assume that all heap
we do not have to consider variable reassignments for the                        accesses within the Application, x := ∗e and ∗x := e, are
purpose of our proof. Besides statements to allocate, read, and                  data race free. I.e., all accesses to the heap locations to
write a heap location, we make each auto-actively verified API                   which e and x, respectively, point are linearizable and, thus,
function of the Core a dedicated statement in the language                       do not cause data races.
even though these statements are themselves implemented as
                                                                                     Note that Asm. 2 and Asm. 3 apply to heap accesses
sequences of statements, which are considered by our static
                                                                                 within the Application only, as we auto-actively prove safety
analyses. c := CoreAlloc(ē) corresponds to calling the
                                                                                 for the Core.
Core’s constructor and creating a new Core instance c. We
                                                                                     By auto-actively verifying the Core, we prove a Hoare
use r̄ := CoreApi_k(c, ē) to represent invoking the k-th
                                                                                 triple for each API function. This allows us to abstractly
API function3 on a Core instance c using input arguments ē
                                                                                 treat each API function as a statement in our language as
and return arguments r̄. s1 ; s2 denotes standard sequential
                                                                                 long as there are no callbacks; we discuss callbacks as an
composition of two statements and fork (x̄) {s} spawns a
                                                                                 extension at the end of this subsection. We syntactically
new thread executing statement s while passing variables x̄ to
                                                                                 restrict the specification of Core API functions, i.e., the
this thread. We syntactically require that the newly spawned
                                                                                 assertions occurring in the auto-actively verified Hoare triples,
thread accesses only its own local variables and variables x̄.
                                                                                 such that we can discharge the side conditions using static
Definition 7 (Basic Programming Language). We consider                           analyses and, thus, construct a proof for the entire codebase.
the following programming language, where S ranges over                          We state these restrictions immediately after introducing
labeled statements, x over variables, ℓ over statement labels,                   some notational conventions.
and e over expressions. We have the usual side effect-free
                                                                                 Definition 8 (Notation). We introduce the following notation
expressions. We use ȳ as a shorthand notation to denote lists
                                                                                 to simplify forthcoming definitions, explanations, and proofs.
of kind y.
                                                                                 accnil (x) denotes full permission for the heap location
    S ≜ Uℓ                                                                       to which x points but only if x is non-nil. Analogously,
    U ≜ skip | x := new() | x := ∗e | ∗x := e |                                  we define invnil (x) for the Core invariant. Lastly, we lift
        c := CoreAlloc(ē) | r̄ := CoreApi_k(c, ē) |                               4. We require Asm. 2 as we construct a Hoare triple for the entire
                                                                                 codebase, whose definition includes that a program does not crash. We
        S; S | fork (x̄) {S}                                                     could avoid this assumption by altering the definition of a Hoare triple
                                                                                 to guarantee the postcondition only if the program does not crash. This
  3. We assume the existence of some total order for API functions, e.g.,        alternative definition would be suitable for programming languages like Go
based on their declarations’ syntactical ordering.                               in which dereferencing nil is defined behavior and results in a crash, which
                                                                                 does not invalidate our security guarantees.



                                                                            24
permissions for a heap location to lists thereof, internally             tracking the set of heap locations that are accessible by
using the iterated separating conjunction ⋆i ranging over i.             multiple threads. The thread-local ghost variable lhs tracks
                                                                         Application-managed heap locations that are only accessible
           accnil (x) ≜ x ̸= nil =⇒ acc(x)
                                                                         by the current thread. Lastly, the thread-local variable ihs
            invnil (x) ≜ x ̸= nil =⇒ inv(x)                              tracks the Core instance if it is already allocated.
              acc(x̄) ≜ ⋆0≤i<len(x̄) acc(x̄[i])                              Relying on these ghost variables, we can define the
                                                                         program invariants Πl and Πg that specify the separation
           accnil (x̄) ≜ ⋆0≤i<len(x̄) accnil (x̄[i])                     logic permissions held by a thread at each program point,
where len(x̄) returns the length of list x̄ and x̄[i] the i-th           as shown in Def. 9, where used is a pointer to a boolean
element therein.                                                         specifying whether the I/O permissions ϕ have already been
                                                                         consumed to allocate a Core instance.
Assumption 4 (Syntactic restrictions for Core specification).
We make the following syntactical assumptions about the pre-             Definition 9 (Program invariants).
and postconditions of Core API functions, which ultimately                                                           
                                                                                   Πl ≜ ⋆l∈lhs acc(l) ⋆ ⋆i∈ihs inv(i)
enable us to apply static analyses.                                                                              
                                                                                   Πg ≜ acc(ghs) ⋆ ⋆g∈∗ghs acc(g) ⋆
            PCoreAlloc (ē)      ≜ ϕ⋆R                                                                              
                                                                                         acc(used) ⋆ ¬(∗used) =⇒ ϕ
            QCoreAlloc (c, ē)   ≜ inv(c) ⋆ R′
                                                                             Πl specifies permissions that are exclusively owned by
            PCoreApi_k (c, ē)   ≜ invnil (c) ⋆ Sk
                                                                         each thread. The first conjunct specifies (full) permissions to
            QCoreApi_k (c, ē, r̄) ≜ invnil (c) ⋆ Sk′                    every heap location in lhs, which, as we will see, holds every
where R, R′ , Sk , and Sk′ are separation logic assertions that          heap location that is accessible only by the current thread and
specify permissions for the arguments ē and, if applicable, r̄.         is unrelated to Core instances. Additionally, Πl specifies that
Preconditions are free of functional properties and specify at           the Core invariant inv(i) holds for each Core instance i.
most permissions for non-nil arguments, i.e., accnil (ē) |= R           Note that inv(i) is a separation logic predicate that specifies
and accnil (ē) |= Sk . Each postcondition needs to specify the          permissions for a subset of the transitively reachable heap
same or more permissions than the respective precondition,               locations starting from i and possibly functional properties
i.e., R′ |= R and Sk′ |= Sk . Additionally, postconditions need          about these heap locations. While the definition of inv(i)
to specify full permission to every heap location that becomes           matters for the Core’s auto-active verification, we treat
accessible to the Application and that is created within the             inv(i) for the purpose of the program invariant as an opaque
corresponding Core function or any function transitively                 separation logic resource.
called thereby. For simplicity, we disallow CoreAlloc(ē) to                 Πg specifies permissions to heap locations that are
return such heap locations other than the Core instance itself           potentially shared among multiple threads. When accessing
and, thus, permissions to such heap locations can only occur             such a heap location, a thread can temporarily acquire the
in Sk′ for the return arguments r̄. Furthermore, we restrict             corresponding permission from Πg , which is justified as
the input arguments ē and output arguments r̄ to be shallow,            long as all accesses to this location are linearizable. Since
i.e., their transitive closure of reachable heap locations is the        we assume absence of data races (cf. Asm. 3), there exists
singleton set, i.e., ∀e ∈ ē. e ̸= nil =⇒ reach(e) = {e} and             a linearization of heap accesses such that permission for
analogously for r̄. This restriction simplifies the reasoning            manipulating g, i.e., acc(g), can temporarily be obtained
about which heap locations are passed between the Core                   from Πg for the manipulation’s duration. Furthermore, Πg
and Application. However, lifting this restriction is possible           specifies the I/O permissions ϕ if they have not been
and would require that Sk and Sk′ specify the permission                 used yet to create a Core instance, in which case the
for every reachable heap location.                                       pointer used points to a heap location storing the value
                                                                         false. As mentioned, we focus in this proof on the case of
A.2.1. Program Invariant. In order to define composable                  creating at most one Core instance. However, this conjunct
proof rules for our language, we define a program invariant              can easily be adapted to provide a family of I/O permissions
that is maintained by each statement. Our invariant concep-              such that the creation of arbitrarily-many Core instances
tually partitions the heap among two dimensions, namely                  becomes possible, as we will detail in Sec. 5.2.2.
whether a heap location is accessible by multiple threads                    Since the presented program invariants rely on ghost
and whether a heap location is owned by the Application                  variables to specify permissions, we have to ensure that
as opposed to the Core. As we will formalize later, we call              these ghost variables stay in sync with a program’s execu-
a heap location h Application-managed if h is under the Ap-              tion, i.e., the effects of each statement. Hence, we present
plication’s control, which means that it is not covered by the           algorithm A in Fig. 13 that augments a program with ghost
Core invariant. Furthermore, we ensure that the Application              statements updating the ghost variables according to each
only accesses memory that is Application-managed.                        statement’s effects. These ghost statements manipulate only
    We make the heap partitioning explicit by introducing                ghost variables and aid verification without changing the
ghost variables tracking the heap locations belonging to                 input program’s runtime behavior. Thus, these ghost variables
each partition. We use a global ghost set pointed to by ghs              and ghost statements can be erased before compilation.



                                                                    25
                      A(skip) ⇝ skip
                A(x := new()) ⇝ x := new(); lhs := lhs ∪nil {x}
                                   (
                                    lhs := lhs \ {e}; x := ∗e; lhs := lhs ∪nil {e}                        if e ∈ lhs
                    A(x := ∗e) ⇝
                                    atomic {∗ghs := ∗ghs \ {e}; x := ∗e; ∗ ghs := ∗ghs ∪nil {e}} otherwise
                                   
                                   lhs := lhs \ {x}; ∗ x := e; lhs := lhs ∪nil {x}                       if x ∈ lhs
                    A(∗x := e) ⇝ atomic { ∗ ghs := ∗ghs \ {x}; lhs := lhs \ (reach(e) ∩ lhs);
                                                                                                          otherwise
                                                 ∗ x := e; ∗ ghs := ∗ghs ∪nil {x} ∪ (reach(e) ∩ lhs)}
                                   

         A(c := CoreAlloc(ē)) ⇝ atomic {∗used := true}; lhs := lhs \ ē; c := CoreAlloc(ē); lhs := lhs ∪nil ē; ihs := ihs ∪nil {c}
      A(r̄ := CoreApi_k(c, ē)) ⇝ ihs := ihs \ {c}; lhs := lhs \ ē; r̄ := CoreApi_k(c, ē); lhs := lhs ∪nil ē ∪ r̄; ihs := ihs ∪nil {c}
                     A(s1 ; s2 ) ⇝ A(s1 ); A(s2 )
               A(fork (x̄) {s}) ⇝ lhs := lhs \ (reach(x̄) ∩ lhs); ∗ ghs := ∗ghs ∪nil (reach(x̄) ∩ lhs); fork (x̄) {lhs := ∅; ihs := ∅; A(s)}
Figure 13. Algorithm A transforms a codebase by inserting ghost statements. We define this algorithm by cases, i.e., describe how A transforms each
statement s to a statement s′ , written as A(s) ⇝ s′ . reach(e) computes the set of transitively reachable heap locations from expression e. The set union
operation ignores nil, as variables might be nil, i.e., S1 ∪nil S2 ≜ (S1 ∪ S2 ) \ nil. This ensures that nil is never contained in any ghost set.


    Common to all cases of algorithm A is that for a                            A.2.2. Proof Rules. Thanks to the program invariants and
statement s, first, the current heap is partitioned into a heap H               the ghost statements that algorithm A inserts into a program,
on which s possibly operates and the remaining heap F                           we can define proof rules as shown in Fig. 14. In particular,
that s leaves untouched by removing the separation logic                        all proof rules share the same pre- and postcondition, namely
resources for H via corresponding ghost set subtractions.                       the local and global program invariants Πl and Πg , resp.,
The separation logic resources belonging to heap F remain                       which allow us to compose the proof rules to obtain a whole
in the ghost sets. Afterwards, statement s is executed that                     program proof. The proof rules’ simplicity is enabled by
changes heap H to H ′ , followed by merging the heaps H ′                       their side conditions (cf. Fig. 15) that we discharge using
and F via ghost set union operations.                                           our static analyses.
    Allocating a heap location operates on an empty heap                            Besides containment of heap locations in particular
and produces a new heap location, which is added to the set                     ghost sets, the side conditions rely on disjointness of in-
of local heap locations as there is no way any other thread                     put arguments, which we formally define next. Informally,
might already have gained access thereto. Dereferencing                         two arguments are disjoint if they point to different heap
a pointer e and reading the corresponding heap location                         locations or one of the arguments is nil.
requires a permission for the duration of this operation.
                                                                                Definition 10 (Variable value). val τ (x ) denotes the value of
Therefore, we first subtract and afterwards add this location
                                                                                variable x on trace τ . Since we assume that our programs
from the current heap by manipulating either the ghost set
                                                                                are in SSA-form, this definition is independent of a particular
of local or global heap locations depending on whether this
                                                                                program point. However, x must be declared such that
heap location is contained in lhs. In case the heap location is
                                                                                val τ (x ) is defined.
in the ghost set of global heap locations, we insert an atomic
block, which is justified by Asm. 3 stating that accesses to                    Definition 11 (Disjointness). Two pointer variables x and y
this heap location are linearizable.                                            are disjoint if their pointer value is different or nil for all
    Noteworthy are write operations to heap locations, espe-                    traces τ .
cially in the case that a heap location is accessible by other
threads as the written value becomes accessible by these                        disjoint({x, y}) ≜ ∀τ.val τ (x ) = nil ∨ val τ (x ) ̸= val τ (y)
threads. Hence, we first remove all local heap locations that                   We straightforwardly lift this definition to lists of variables z̄,
are transitively reachable from the written value and add                       where disjoint(z̄) denotes pairwise disjointness between
them afterwards to the ghost set of global heap location as                     every element in z̄.
these locations possibly escape the current thread via this
write operation. Similarly, when forking a thread, the heap                         Next, we sketch the proof rules’ soundness proof, which
locations that are reachable from the variables x̄ escape the                   relies on the side conditions ω. Afterwards, we define
current thread and, thus, the sets of local and global heap                     what properties our static analyses provide given that their
locations are updated accordingly.                                              execution succeeded and show that these properties imply the
    For CoreAlloc(ē) and r̄ := CoreApi_k(c, ē), the                           side conditions ω. We conclude by proving a corollary stating
algorithm A adds and subtracts only ē and r̄ as opposed to                     that we construct a Hoare triple for the entire codebase.
all transitively reachable heap locations. This is sufficient                   Theorem 4 (Soundness of proof rules).
because Asm. 4 restricts ē and r̄ to be shallow and, thus,
no other heap locations are reachable. However, extend-                            If Πg ⊢ [Πl ] A(s) [Πl ] , then Πg |= [Πl ] A(s) [Πl ]
ing algorithm A to support non-shallow arguments would                          Proof sketch. We perform structural induction over the input
be straightforward by adding and removing reach(ē) and                         statement s to algorithm A and construct a proof tree
reach(r̄) instead of ē and r̄ to and from lhs, respectively.



                                                                           26
         ω(ssimple )                             Πg ⊢ [Πl ] A(s1 ) [Πl ]     Πg ⊢ [Πl ] A(s2 ) [Πl ]                        Πg ⊢ [Πl ] A(s) [Πl ]
                               (Simple)                                                                (Seq)                                              (Fork)
Πg ⊢ [Πl ] A(ssimple ) [Πl ]                                 Πg ⊢ [Πl ] A(s1 ; s2 ) [Πl ]                            Πg ⊢ [Πl ] A(fork (x̄) {s}) [Πl ]
Figure 14. Proof rules. ssimple ranges over all simple statements; s, s1 , and s2 range over all statements. ω denotes a statement’s side conditions (cf. Fig. 15).



                         ω(x := ∗e) ≜ e ∈ lhs ∪ ∗ghs                                        from Πl within the proof.
                                                                                          • A(s1 ; s2 ): We apply the standard Seq rule from sep-
                         ω(∗x := e) ≜ x ∈ lhs ∪ ∗ghs                                        aration logic to combine the proof subtrees for A(s1 )
        ω(c := CoreAlloc(ē)) ≜ ∗ used = false ∧                                            and A(s2 ) that we obtain by applying our induction
                                (set(ē) \ nil) ⊆ lhs ∧                                     hypothesis.
                                                                                          • A(fork (x̄) {s}): Fig. 33 shows the proof tree that
                                disjoint(ē)
                                                                                            applies the induction hypothesis to A(s). Since the
    ω(r̄ := CoreApi_k(c, ē)) ≜ (set(ē) \ nil) ⊆ lhs ∧                                     algorithm A removes the permissions for heap locations
                                disjoint(ē) ∧                                              only in reach(x̄) ∩ lhs, the resulting side condition
                                (c ∈ ihs ∨ c = nil)                                         ((reach(x̄) ∩ lhs) ⊆ lhs) is trivial since these heap
                                                                                            locations are by definition contained in lhs.
Figure 15. Side conditions for our statements, which are amenable to static                 The main proof insight is that we ensure that the global
analyses. ω evaluates to true for all statements not listed above and set(l)                invariant covers the permissions for all heap locations
returns the set of elements in list l. We implicitly refer to variables’ values,
e.g., v ∈ S denotes that the value of variable v is contained in set stored                 that become accessible by the spawned thread and
in variable S as opposed to the variables’ syntactical representation.                      establish the local invariant for the spawned thread
                                                                                            by initializing the set of local heap locations and (local)
                                                                                            Core instances to the empty set. reach(x̄) forms an
in separation logic building up on the proof rules by
                                                                                            upper bound on the heap locations that command s
Vafeiadis [39]. We use a small caps font to denote proof
                                                                                            might access because we syntactically require that s
rules, such as Skip. All rules in this theorem’s proof are from
                                                                                            accesses only x̄ and its own local variables.
Vafeiadis [39], except Fork and Seq∗ that are straightforward
extensions from the parallel and sequential composition rules,
respectively. Side conditions arising in the proof trees are
marked in blue and form ω (cf. Fig. 15).                                                A.2.3. Static Analyses. Since our proof rules rely on the
   • A(skip): Since the algorithm A does not insert any                                 side conditions ω (cf. Fig. 15), we introduce next our static
     ghost commands and skip does not alter the program                                 analyses, cover the properties we assume they provide, and
     state, Πl is trivially maintained. The Skip rule is                                show that these properties imply ω. We end by proving a
     immediately applicable and completes the proof tree.                               corollary that we can construct a whole program proof for a
   • A(x := new()): Fig. 25 shows the proof tree that uses                              codebase given that we have auto-actively verified the Core
     Fig. 16 as a sub-proof for inserting a heap location into                          and successfully executed the static analyses.
     the ghost set of local heap locations.
                                                                                        Pointer analysis. A pointer analysis computes for each
   • A(x := ∗e): The side condition ω ensures that e ∈
                                                                                        pointer x a set of heap locations L to where x may point,
     lhs ∪ ∗ghs holds. If e ∈ lhs then Fig. 26 is a valid proof
                                                                                        which we formalize as a judgement pts(x ) = L. Each
     tree for this read operation. Otherwise, e ∈ ∗ghs holds
                                                                                        heap location in L is identified by its allocation site, which
     and Fig. 27 shows the corresponding proof tree.
                                                                                        corresponds to the label of a particular statement in the
   • A(∗x := e): For write operations, we construct a proof
                                                                                        program’s text. Note that this analysis over-approximates the
     tree similar to read operations, as explained in the case
                                                                                        set of heap locations that actually change when writing to
     above, except that we extract permissions for x instead of
                                                                                        x. The pointer analysis we are using is context insensitive,
     e from the program invariants and replace applications
                                                                                        i.e., ignores control flow and ordering of statements. Thus,
     of the Read rule by Write. We can apply these rules
                                                                                        we omit the program location at which such a judgement
     because we possess full permission (as opposed to only
                                                                                        holds as it holds for all program locations within a given
     partial permission) to the heap location (i.e., acc(x)).
                                                                                        codebase. If necessary, we could employ a context-sensitive
   • A(c := CoreAlloc(ē)): Fig. 29 shows the proof tree
                                                                                        pointer analysis to increase precision.
     extending the subproof that the auto-active program
                                                                                             To formalize what the pointer analysis computes, let
     verifier implicitly constructs (in Fig. 28) while verifying
                                                                                        us first state several definitions before stating the pointer
     the Hoare triple for CoreAlloc(ē).
   • A(r̄ := CoreApi_k(c, ē)): We construct a proof tree
                                                                                        analysis’ soundness, which we assume.
     in Fig. 31 using Fig. 30 as a subtree that is similar                              Definition 12 (Reachability). reach pτ (x) returns the set
     to the one for the Core allocation command with the                                of addresses for all heap locations that are transitively
     main difference that the precondition requires invnil (c)                          reachable from variable x at program point p on trace τ .
     instead of the I/O permissions ϕ. The side condition                               Hence, ∀x, τ, p. val τ (x ) ∈ reach pτ (x) holds for all program
     c ∈ ihs ∨ c = nil ensures that we can obtain invnil (c)                            points p after x is defined.




                                                                                   27
                                                                                                                   Assign
                                     Πg ⊢ [∀l ∈ lhs ∪nil {x}. acc(l)] lhs := lhs ∪nil {x} [∀l ∈ lhs. acc(l)]
                                                                                                                     Conseq
                                  Πg ⊢ [(∀l ∈ lhs. acc(l)) ⋆ accnil (x)] lhs := lhs ∪nil {x} [∀l ∈ lhs. acc(l)]
                                                                                                                     Frame
                                                 Πg ⊢ [Πl ⋆ accnil (x)] lhs := lhs ∪nil {x} [Πl ]
                                 Figure 16. Proof tree for lhs := lhs ∪nil {x}, where accnil (e) ≜ e ̸= nil =⇒ acc(e).



                                                                                                                            Write
                          emp ⊢ [acc(ghs) ⋆ ∗ghs = v] ∗ ghs := ∗ghs ∪nil {x} [acc(ghs) ⋆ ∗ghs = v ∪nil {x}]
                                                                                                                               Frame
                     emp ⊢ [acc(ghs) ⋆ ∗ghs = v ⋆ R] ∗ ghs := ∗ghs ∪nil {x} [acc(ghs) ⋆ ∗ghs = v ∪nil {x} ⋆ R]
                                                                                                                                       Conseq
             emp ⊢ [acc(ghs) ⋆ (∀g ∈ ∗ghs. acc(g)) ⋆ accnil (x)] ∗ ghs := ∗ghs ∪nil {x} [acc(ghs) ⋆ ∀g ∈ ∗ghs. acc(g)]
                                                                                                                                       Frame
                                            emp ⊢ [Πg ⋆ accnil (x)] ∗ ghs := ∗ghs ∪nil {x} [Πg ]


                                                          with   R ≜ ∀g ∈ (v ∪nil {x}). acc(g)

Figure 17. Proof tree for ∗ghs := ∗ghs ∪nil {x} given that Πg is already local, where v is a fresh variable and the Write rule has been naturally extended
to internally perform a heap read operation returning the value v for ∗ghs as specified in the precondition.


                                                                       ·
                                                                       · F ig. 17
                                                                       ·
                                              emp ⊢ [Πg ⋆ accnil (x)] ∗ ghs := ∗ghs ∪nil {x} [Πg ]
                                                                                                            Atom
                                                 Πg ⊢ [accnil (x)] ∗ ghs := ∗ghs ∪nil {x} [emp]
                                                    Figure 18. Proof tree for ∗ghs := ∗ghs ∪nil {x}.



                                                                                                                   Assign
                                     Πg ⊢ [∀i ∈ ihs ∪nil {c}. inv(i)] ihs := ihs ∪nil {c} [∀i ∈ ihs. inv(i)]
                                                                                                                     Conseq
                                   Πg ⊢ [(∀i ∈ ihs. inv(i)) ⋆ invnil (c)] ihs := ihs ∪nil {c} [∀i ∈ ihs. inv(i)]
                                                                                                                     Frame
                                                 Πg ⊢ [Πl ⋆ invnil (c)] ihs := ihs ∪nil {c} [Πl ]
                                 Figure 19. Proof tree for ihs := ihs ∪nil {c}, where invnil (c) ≜ c ̸= nil =⇒ inv(c).



                                                                                                                     Assign
                                               Πg ⊢ [∀l ∈ lhs \ {e}. acc(l)] lhs := lhs \ {e} [∀l ∈ lhs. acc(l)]
                                                                                                                                 Frame
                       e ∈ lhs     Πg ⊢ [(∀l ∈ lhs \ {e}. acc(l)) ⋆ acc(e)] lhs := lhs \ {e} [(∀l ∈ lhs. acc(l)) ⋆ acc(e)]
                                                                                                                                 Conseq
                                     Πg ⊢ [∀l ∈ lhs. acc(l)] lhs := lhs \ {e} [(∀l ∈ lhs. acc(l)) ⋆ acc(e)]
                                                                                                                   Frame
                                                    Πg ⊢ [Πl ] lhs := lhs \ {e} [Πl ⋆ acc(e)]
                                                   Figure 20. Proof tree for lhs := lhs \ {e} if e ∈ lhs.



                                                                                                                            Assign
                                                    Πg ⊢ [∀l ∈ lhs \ {e}. acc(l)] lhs := lhs \ {e} [∀l ∈ lhs. acc(l)]
                                                                                                                                          Frame
              e ∈ lhs ∨ e = nil       Πg ⊢ [(∀l ∈ lhs \ {e}. acc(l)) ⋆ accnil (e)] lhs := lhs \ {e} [(∀l ∈ lhs. acc(l)) ⋆ accnil (e)]
                                                                                                                                          Conseq
                                    Πg ⊢ [∀l ∈ lhs. acc(l)] lhs := lhs \ {e} [(∀l ∈ lhs. acc(l)) ⋆ accnil (e)]
                                                                                                                    Frame
                                                  Πg ⊢ [Πl ] lhs := lhs \ {e} [Πl ⋆ accnil (e)]
                                      Figure 21. Alternative proof tree for lhs := lhs \ {e} that permits e being nil.




                                                                            28
                                                                                                                              Write
                                     emp ⊢ [acc(ghs) ⋆ ∗ghs = v] ∗ ghs := ∗ghs \ {e} [acc(ghs) ⋆ ∗ghs = v \ {e}]
                                                                                                                                   Frame
                   e ∈ ∗ghs     emp ⊢ [acc(ghs) ⋆ ∗ghs = v ⋆ R] ∗ ghs := ∗ghs \ {e} [acc(ghs) ⋆ ∗ghs = v \ {e} ⋆ R]
                                                                                                                                   Conseq
                 emp ⊢ [acc(ghs) ⋆ ∀g ∈ ∗ghs. acc(g)] ∗ ghs := ∗ghs \ {e} [acc(ghs) ⋆ (∀g ∈ ∗ghs. acc(g)) ⋆ acc(e)]
                                                                                                                                   Frame
                                              emp ⊢ [Πg ] ∗ ghs := ∗ghs \ {e} [Πg ⋆ acc(e)]


                                                     with    R ≜ (∀g ∈ (v \ {e}). acc(g)) ⋆ acc(e)

                                      Figure 22. Proof tree for ∗ghs := ∗ghs \ {e} that requires Πg to be local.


                                                                                                                          Assign
                                                    Πg ⊢ [∀i ∈ ihs \ {c}. inv(l)] ihs := ihs \ {c} [∀i ∈ ihs. inv(i)]
                                                                                                                                          Frame
               c ∈ ihs ∨ c = nil    Πg ⊢ [(∀i ∈ ihs \ {c}. inv(l)) ⋆ invnil (c)] ihs := ihs \ {c} [(∀i ∈ ihs. inv(i)) ⋆ invnil (c)]
                                                                                                                                          Conseq
                                   Πg ⊢ [∀i ∈ ihs. inv(i)] ihs := ihs \ {c} [(∀i ∈ ihs. inv(i)) ⋆ invnil (c)]
                                                                                                                  Frame
                                                 Πg ⊢ [Πl ] ihs := ihs \ {c} [Πl ⋆ invnil (c)]
                                                       Figure 23. Proof tree for ihs := ihs \ {c}.


                                                                                                                      Write
                                              emp ⊢ [acc(used)] ∗ used := true [acc(used) ⋆ ∗used = true]
                                                                                                                          Frame
                             ¬(∗used)     emp ⊢ [acc(used) ⋆ ϕ] ∗ used := true [acc(used) ⋆ ∗used = true ⋆ ϕ]
                                                                                                                          Conseq
                           emp ⊢ [acc(used) ⋆ ¬(∗used) =⇒ ϕ] ∗ used := true [acc(used) ⋆ ∗used = true ⋆ ϕ]
                                                                                                                              Conseq
                       emp ⊢ [acc(used) ⋆ ¬(∗used) =⇒ ϕ] ∗ used := true [acc(used) ⋆ (¬(∗used) =⇒ ϕ) ⋆ ϕ]
                                                                                                                              Frame
                                                     emp ⊢ [Πg ] ∗ used := true [Πg ⋆ ϕ]
                                                                                                    Atom
                                                 Πg ⊢ [emp] atomic {∗used := true} [ϕ]
                                                                                                    Frame
                                                Πg ⊢ [Πl ] atomic {∗used := true} [Πl ⋆ ϕ]
                                                 Figure 24. Proof tree for atomic {∗used := true}.


                                                                                                  ·
                                                                                                  · F ig. 16
                                                                Alloc                             ·
                       Πg ⊢ [emp] x := new() [acc(x)]                      Πg ⊢ [Πl ⋆ accnil (x)] lhs := lhs ∪nil {x} [Πl ]
                                                                 Frame                                                        Conseq
                      Πg ⊢ [Πl ] x := new() [Πl ⋆ acc(x)]                    Πg ⊢ [Πl ⋆ acc(x)] lhs := lhs ∪nil {x} [Πl ]
                                                                                                                            Seq
                                              Πg ⊢ [Πl ] x := new(); lhs := lhs ∪nil {x} [Πl ]
                                                       Figure 25. Proof tree for A(x := new()).


                                                                                                                 ·
                                                                                                                 · F ig. 16
                                                                                     Read                        ·
                            ·                        Πg ⊢ [acc(e)] s2 [acc(e)]                      Πg ⊢ [Πl ⋆ accnil (e)] s3 [Πl ]
                            · F ig. 20
                            ·                                                               Frame                                     Conseq
               Πg ⊢ [Πl ] s1 [Πl ⋆ acc(e)]     Πg ⊢ [Πl ⋆ acc(e)] s2 [Πl ⋆ acc(e)]                   Πg ⊢ [Πl ⋆ acc(e)] s3 [Πl ]
                                                                                                                                   Seq∗
                                                            Πg ⊢ [Πl ] s1 ; s2 ; s3 [Πl ]


                    with    s1 ≜ lhs := lhs \ {e}                         s2 ≜ x := ∗e                        s3 ≜ lhs := lhs ∪nil {e}

Figure 26. Proof tree for A(x := ∗e) if e ∈ lhs, where Seq∗ represents repeated application of the Seq rule. We discharge the side condition from Fig. 20
as e ∈ lhs holds by definition.




                                                                              29
                                                                                                                       ·
                    e ∈ ∗ghs                                                                                           · F ig. 17
                                                                                       Read                            ·
                         ·                           emp ⊢ [acc(e)] s2 [acc(e)]                          emp ⊢ [Πg ⋆ accnil (e)] s3 [Πg ]
                         · F ig. 22
                         ·                                                                    Frame                                            F ig. 17
            emp ⊢ [Πg ] s1 [Πg ⋆ acc(e)]       emp ⊢ [Πg ⋆ acc(e)] s2 [Πg ⋆ acc(e)]                       emp ⊢ [Πg ⋆ acc(e)] s3 [Πg ]
                                                                                                                                             Seq∗
                                                          emp ⊢ [Πg ] s1 ; s2 ; s3 [Πg ]
                                                                                                     Atom
                                                   Πg ⊢ [emp] atomic {s1 ; s2 ; s3 } [emp]
                                                                                                     Frame
                                                     Πg ⊢ [Πl ] atomic {s1 ; s2 ; s3 } [Πl ]


                   with   s1 ≜ ∗ghs := ∗ghs \ {e}                         s2 ≜ x := ∗e                          s3 ≜ ∗ghs := ∗ghs ∪nil {e}

                                                      Figure 27. Proof tree for A(x := ∗e) if e ̸∈ lhs.



                                                                                ·
                                                                                · auto-active verification
                                                                                ·
                                                  Πg ⊢ [PCoreAlloc (ē)] c := CoreAlloc(ē) [QCoreAlloc (c, ē)]
                                                                                                                             Frame
                                 Asm. 4      Πg ⊢ [PCoreAlloc (ē) ⋆ F ] c := CoreAlloc(ē) [QCoreAlloc (c, ē) ⋆ F ]
                                                                                                                             Conseq
                                         Πg ⊢ [accnil (ē) ⋆ ϕ] c := CoreAlloc(ē) [accnil (ē) ⋆ inv(c)]
                                                                                                                       Frame
                                   Πg ⊢ [Πl ⋆ accnil (ē) ⋆ ϕ] c := CoreAlloc(ē) [Πl ⋆ accnil (ē) ⋆ inv(c)]
Figure 28. Proof tree for c := CoreAlloc(ē) using the subproof that we extract from the auto-active program verifier. The side condition (Asm. 4) states that
PCoreAlloc (ē) = ϕ ⋆ R and accnil (ē) |= R. We call F the permissions that are framed around, i.e., accnil (ē) = R ⋆ F . The side condition further specifies
that QCoreAlloc (c, ē) = inv(c) ⋆ R′ and R′ |= R hold, allowing us to derive R′ ⋆ F |= accnil (ē). Thus, we can apply the Conseq rule. We abuse the
notation accnil (ē) to denote the iterated separating conjunction expressing accnil (e) for each element e in ē, i.e., ∀i. 0 ≤ i < len(ē) =⇒ accnil (ē[i]),
where len(ē) and ē[i] return the length and the i-th element of the list ē, respectively.




                                   (set(ē) \ nil) ⊆ lhs ∧
                                         disjoint(ē)
                                               ·                                                             ·                              ·
             ¬(∗used)                          · F ig. 21                    Asm. 4                          · F ig. 16                     · F ig. 19
                                               ·                                                             ·                              ·
                  ·                  Πg ⊢ [Πl ] s2 [R2′ ]                       ·                   Πg ⊢ [R2′ ] s4 [Πl ]           Πg ⊢ [R4′ ] s5 [Πl ]
                  · F ig. 24                                                    · F ig. 28
                  ·                                            Frame            ·                                          Frame                          Seq
       Πg ⊢ [Πl ] s1 [Πl ⋆ ϕ]        Πg ⊢ [Πl ⋆ ϕ] s2 [R2 ]             Πg ⊢ [R2 ] s3 [R3 ]         Πg ⊢ [R3 ] s4 [R4 ]            Πg ⊢ [R4 ] s5 [Πl ]
                                                                                                                                                          Seq∗
                                                          Πg ⊢ [Πl ] s1 ; s2 ; s3 ; s4 ; s5 [Πl ]
with

    s1 ≜ atomic {∗used := true}            s2 ≜ lhs := lhs \ ē    s3 ≜ c := CoreAlloc(ē)              s4 ≜ lhs := lhs ∪nil ē       s5 ≜ ihs := ihs ∪nil {c}
   R2′ ≜ Πl ⋆ accnil (ē)                 R2 ≜ R2′ ⋆ ϕ            R3 ≜ R2′ ⋆ inv(c)                    R4 ≜ Πl ⋆ inv(c)              R4′ ≜ Πl ⋆ invnil (c)

Figure 29. Proof tree for A(c := CoreAlloc(ē)). We naturally extend Fig. 16 and Fig. 20 to adding and removing lists of heap locations to and from the
ghost set lhs, respectively. The latter requires their disjointness.



                                                                                 ·
                                                                                 · auto-active verification
                                                                                 ·
                                              Πg ⊢ [PCoreApi_k (c, ē)] r̄ := CoreApi_k(c, ē) [QCoreApi_k (c, ē, r̄)]
                                                                                                                                   Frame
                             Asm. 4      Πg ⊢ [PCoreApi_k (c, ē) ⋆ F ] r̄ := CoreApi_k(c, ē) [QCoreApi_k (c, ē, r̄) ⋆ F ]
                                                                                                                                   Conseq
                            Πg ⊢ [invnil (c) ⋆ accnil (ē)] r̄ := CoreApi_k(c, ē) [invnil (c) ⋆ accnil (ē) ⋆ accnil (r̄)]
                                                                                                                                       Frame
                     Πg ⊢ [Πl ⋆ invnil (c) ⋆ accnil (ē)] r̄ := CoreApi_k(c, ē) [Πl ⋆ invnil (c) ⋆ accnil (ē) ⋆ accnil (r̄)]
                                                     Figure 30. Proof tree for r̄ := CoreApi_k(c, ē).




                                                                               30
                                  (set(ē) \ nil) ⊆ lhs ∧
                                        disjoint(ē)
                                              ·                                                                ·
        c ∈ ihs ∨ c = nil                     · F ig. 21                      Asm. 4                           · F ig. 16
                                              ·                                                                ·
                ·                   Πg ⊢ [Πl ] s2 [R2′ ]                         ·                    Πg ⊢ [R3′ ] s4 [Πl ]                    ·
                · F ig. 23                                                       · F ig. 30                                                   · F ig. 19
                ·                                              Frame             ·                                           Frame            ·
        Πg ⊢ [Πl ] s1 [R1 ]            Πg ⊢ [R1 ] s2 [R2 ]               Πg ⊢ [R2 ] s3 [R3 ]          Πg ⊢ [R3 ] s4 [R1 ]             Πg ⊢ [R1 ] s5 [Πl ]
                                                                                                                                                            Seq∗
                                                            Πg ⊢ [Πl ] s1 ; s2 ; s3 ; s4 ; s5 [Πl ]
with

   s1 ≜ ihs := ihs \ {c}       s2 ≜ lhs := lhs \ ē      s3 ≜ r̄ := CoreApi_k(c, ē)             s4 ≜ lhs := lhs ∪nil ē ∪nil r̄        s5 ≜ ihs := ihs ∪nil {c}
   R1 ≜ Πl ⋆ invnil (c)       R2′ ≜ Πl ⋆ accnil (ē)     R2 ≜ R2′ ⋆ invnil (c)                  R3′ ≜ R2′ ⋆ accnil (r̄)                 R3 ≜ R3′ ⋆ invnil (c)

                                                 Figure 31. Proof tree for A(r̄ := CoreApi_k(c, ē)).

                                                                                                          Assign
                                                                 Πg ⊢ [emp] ihs := ∅ [ihs = ∅]
                                                                                                                Frame
                                                          Πg ⊢ [lhs = ∅] ihs := ∅ [lhs = ∅ ⋆ ihs = ∅]                                  ·
                                                                                                                                       · IH
                                               Assign                                                           Conseq                 ·
             Πg ⊢ [emp] lhs := ∅ [lhs = ∅]                         Πg ⊢ [lhs = ∅] ihs := ∅ [Πl ]                             Πg ⊢ [Πl ] A(s) [Πl ]
                                                                                                                                                     Seq∗
                                                      Πg ⊢ [emp] lhs := ∅; ihs := ∅; A(s) [Πl ]
Figure 32. Proof tree for the sequence of statements that is executed as the newly spawned thread, where s represents an arbitrary input statement and IH
denotes an application of the induction hypothesis. We omit trivial applications of the Conseq rule.

                                                   ·                                                    ·
                                                   · F ig. 18                                           · F ig. 32
                                                   ·                                                    ·
                                         Πg ⊢ [R′ ] s2 [emp]                          Πg ⊢ [emp] lhs := ∅; ihs := ∅; A(s) [Πl ]
                                                                  Conseq                                                                        Fork
                                         Πg ⊢ [R] s2 [emp]                   Πg ⊢ [emp] fork (x̄) {lhs := ∅; ihs := ∅; A(s)} [emp]
                                                                                                                                                Seq
                         ·                                Πg ⊢ [R] s2 ; fork (x̄) {lhs := ∅; ihs := ∅; A(s)} [emp]
                         · F ig. 20
                         ·                                                                                                        Frame
              Πg ⊢ [Πl ] s1 [Πl ⋆ R]                     Πg ⊢ [Πl ⋆ R] s2 ; fork (x̄) {lhs := ∅; ihs := ∅; A(s)} [Πl ]
                                                                                                                                  Seq
                                   Πg ⊢ [Πl ] s1 ; s2 ; fork (x̄) {lhs := ∅; ihs := ∅; A(s)} [Πl ]


                     with     s1 ≜ lhs := lhs \ (reach(x̄) ∩ lhs)                             s2 ≜ ∗ghs := ∗ghs ∪nil (reach(x̄) ∩ lhs)
                              R ≜ ∀l ∈ (reach(x̄) ∩ lhs). acc(l)                              R′ ≜ ∀l ∈ (reach(x̄) ∩ lhs). accnil (l)

Figure 33. Proof tree for A(fork (x̄) {s}) that assumes the existence of a Fork rule. The side conditions stemming from Fig. 18 hold trivially as
reach(x̄) ∩ lhs ⊆ lhs and since reach(x̄) returns a set of heap locations, which is by definition free of duplicates and, thus, its elements are pairwise
disjoint.


Definition 13 (Allocation site). as τ (h) returns the allocation                     disjointness.
site for a heap location h on trace τ , which is the label of
the statement that allocated this heap location.                                            ∀x, y.pts(x ) ∩ pts(y) = ∅ =⇒ disjoint({x, y})

Assumption 5 (Soundness of pointer analysis). The pointer                            Proof sketch. If x or y store the value nil, disjoint({x, y})
analysis computes for a variable x the heap locations pts(x )                        holds. Otherwise, x and y are non-nil. We apply Asm. 5 to
to which x may point on all possible traces. These heap                              our premise and obtain ∀τ. as τ (val τ (x )) ̸= as τ (val τ (y)).
locations are identified by their allocation site. We assume                         Since x and y point on all possible traces to heap locations
that the pointer analysis is sound, i.e., computes an over-                          that were allocated at different allocation sites, the heap
approximation of the heap locations to which x actually                              locations themselves must be different, i.e., val τ (x ) ̸=
points when looking at concrete traces.                                              val τ (y).

       ∀x, τ. val τ (x ) ̸= nil =⇒ as τ (val τ (x )) ∈ pts(x )                       Pass-through analysis. As hinted at by our ghost sets,
                                                                                     we distinguish two types of heap locations, namely heap
Lemma 2 (Disjointness from pointer analysis). We can                                 locations that make up Core instances and heap locations
use the pointer analysis’ may-point-to judgments to derive                           that the Application might access. Heap locations of the



                                                                                31
former type are tracked by collecting the respective Core                  Lemma 3 (Uniqueness of locality). The thread t having
instances in ihs. The latter type encompasses heap locations               access to a local heap location h is unique, i.e.,
that are either allocated within the Application by new() or
allocated within the Core and returned from a Core API call.                    ∀h, t, t′ , p.localhl pt (h) ∧ localhl pt′ (h) =⇒ t = t′ .
     To distinguish these types of heap locations, we                      Proof sketch. The lemma follows directly from Def. 16.
run a pass-through analysis that provides the judgments
pt pCore (a, τ ) and pt pret (a, τ ) denoting that a heap location         Lemma 4 (Locality is reverse monotonic). A local heap
allocated at allocation site a passed through (pt) the return              location h at program point p′ must be local at every earlier
argument c of a c := CoreAlloc(ē) statement and through                   program point p if h is accessible at p, i.e.,
one of the return arguments r̄ of a r̄ := CoreApi_k(c, ē)                                                                        ′
                                                                            ∀h, t, p, p′ .p ⪯ p′ ∧ accessible pt (h) ∧ localhl pt (h) =⇒
statement, respectively, between label a and program point p
on trace τ . I.e., we have that pt pCore (as τ (val τ (c)), τ ) and                       localhl pt (h).
∀r ∈ set(r̄). pt pret (as τ (val τ (r )), τ ) hold at the program          Proof sketch. We prove this lemma by contradiction for
point p on trace τ after executing the statement c :=                      arbitrary h, t, p, and p′ . ¬localhl pt (h) implies that h is
CoreAlloc(ē) and r̄ := CoreApi_k(c, ē), respectively.                    accessible by another thread t′ , i.e., t′ ̸= t ∧ accessible pt′ (h).
Definition 14 (Application-managed heap locations). We                     Since accessibility is monotonic,   h remains accessible by t′
                                                                               ′                      p′
call a heap location h Application-managed at program                      at p contradicting localhl t (h).
point p on trace τ if h is either allocated within the Appli-
                                                                           Lemma 5 (Locality is reverse transitive). If a local heap
cation or has been returned from a r̄ := CoreApi_k(c, ē)
                                                                           location h′ is transitively reachable from another heap
statement.
                                                                           location h then h must also be local.
       am pτ (h) ≜ is-app(as τ (h)) ∨ pt pret (as τ (h), τ )
                                                                                ∀h, h′ , t, τ, p.localhl pt (h ′ ) ∧ h′ ∈ reach pτ (h) =⇒
Escape analysis. The goal of the escape analysis is to                                           localhl pt (h)
correctly place heap locations into lhs, ∗ghs, and ihs. In
                                                                           Proof sketch. We prove this lemma by contradiction for
particular, we want to establish globally that an Application-
                                                                           arbitrary h, h′ , t, τ , and p. I.e., a thread t′ exists such that
managed heap location and a Core instance are in lhs and
                                                                           h is accessible by t′ . h′ is accessible by t′ via reachability
ihs, respectively, if they are local.
                                                                           from h, thus, contradicting localhl pt (h ′ ).
    We first define what it means for a heap location to be
local (cf. Def. 16). I.e., this definition takes all threads into          Assumption 6 (Soundness of escape analysis). We assume
account and states that a heap location h is local to a thread t           that the escape analysis is sound, i.e., reports a heap
if and only if t is the only thread that can potentially access h.         location to which variable x points as being local only
    Locality of a heap location is approximated by our escape              if the corresponding heap location is indeed local (or x is
analysis. The result of the escape analysis is formalized in               nil) for every possible trace τ , i.e.,
a judgement local p (x ) for some variable x and program
point p. The intuition is that a variable that is local points                    ∀x, τ, p.local p (x ) =⇒
to heap locations (i.e., ∗x) that are accessible only by the                               val τ (x ) = nil ∨ ∃t. localhl pt (val τ (x )).
current thread and, thus, can be modified or even referred
                                                                              Based on these definitions and the soundness of our
to only by the current thread. The escape analysis is sound
                                                                           analyses, we prove several lemmata that relate accessible
in that no heap location that is accessible by another thread
                                                                           heap locations to our ghost sets and corollaries that lift these
will ever be reported as local (cf. Asm. 6), but potentially
                                                                           properties to variables and the judgments we obtain from
imprecise in that some locations that are not accessible by
                                                                           our static analyses. We will later use these corollaries to
other threads will fail to be local.
                                                                           show that these judgments discharge our proof rules’ side
Definition 15 (Accessibility). We write accessible pt (h) to               conditions ω.
denote that heap location h is accessible by thread t at
                                                                           Lemma 6 (Inaccessability implies set absence). All heap
program point p. A thread may access such a heap location
                                                                           locations stored in the ghost sets are accessible by at least
either directly via variables or indirectly by dereferencing
                                                                           one thread.
other heap locations. We define accessibility independently of
variables and, thus, accessibility of h does not change when                 ∀h, τ, p.h ̸= nil ∧ p ∈ τ ∧ (∀t. ¬accessible pt (h)) =⇒
variables go out of scope. Instead, accessibility is monotonic                        ∀t. h ̸∈ (lhst ∪ ∗ghs ∪ ihst )p
for a thread’s execution.
                                                                           where ep denotes evaluating expression e at program point p.
Definition 16 (Locality). A heap location h is local at
program point p if it is accessible by a single thread t.                  Proof sketch. We prove this lemma by induction over pro-
                                                                           gram traces. The base case for the empty trace holds trivially
     localhl pt (h) ≜ accessible pt (h) ∧                                  as lhs and ihs for every thread t and ∗ghs are initialized to
                      (∀t′ . t′ ̸= t =⇒ ¬accessible pt′ (h))               the empty set. In the inductive step, we prove this lemma
                                                                           for an arbitrary heap location h′ , program point p′ , and
                                                                           trace τ . We assume the premise and apply the induction

                                                                      32
hypothesis for the ′immediately preceding program point p                      holds, and we apply the induction hypothesis. If
as ∀t. ¬accessible pt (h ′ ) implies ∀t. ¬accessible pt (h ′ ) due to          h′ = val τ (e), then accessible pts (h ′ ) and, thus, h′ ∈
                                                                    ′                                                                ′
monotonicity. We show that ∀t. h′ ̸∈ (lhst ∪ ∗ghs ∪ ihst )p                    (lhsts ∪ ∗ghs)p hold. Hence, A ensures ∀t′ . lhspt′ = lhspt′
                                                                                          ′
holds by analyzing the ghost operations that A inserts for                     and lhsp = lhsp . Otherwise, A neither adds nor removes
a statement s. We assume without loss of generality that                       h′ to and from any ghost set.
thread ts executes A(s), which transitions from p to p′ . We                 • s = ∗x := e: Since s does not allocate new heap
observe that every element that is added to lhsts , ∗ghs or                    locations, am pτ (h ′ ) holds. If val τ (x ) = h′ , then h′ is
ihst is either the heap location to which a variable accessible                accessible by ts , and we apply the induction hypothesis.
by ts points or a set of heap locations that are reachable from                Since A leaves h′ in the same ghost set, (4) holds.
such a variable. Since h′ by assumption is not accessible                      Otherwise, we focus on the case val τ (x ) ∈ ∗ghsp ∧
from any thread at p′ , A does not add h′ to any ghost set.                    h′ ∈ reach pτ (e) ∩ lhspts as A removes in this case h′
    The next lemmata depend on certain requirements for a                      from lhsts and for all other cases guarantees that h′
codebase, which we define next. As we will see, successfully                   remains in the same ghost set. From h′ ∈ lhspts and our
executing the static analyses implies that a codebase meets                    induction hypothesis, we get t = ts as h′ is accessible
these requirements.                                                            only by a single thread. Since accessible pts (val τ (x )) and
                                                                                                            ′
                                                                               am pτ (val τ (x )) (from rτp ) hold, we apply the induction
Lemma 7 (Locality implies set containment for Applica-                         hypothesis and obtain that another thread t′ with t′ ̸= ts
tion-managed locations). An Application-managed heap                           exists that can access val τ (x ). However, by writing e to
location h is in thread t’s lhs at program point p if h is                     val τ (x ), all from e reachable heap locations including
local, and in ∗ghs if h is accessible by multiple threads.                     h′ become accessible from t′ at p′ . Since h′ is accessible
Both cases hold if a codebase meets the requirements rτp (cf.                  at p′ from at least two different threads,′ namely ts and
Fig. 34).
                                                                               t′ , we have to show that h′ ∈ ∗ghsp and that h′ is
 ∀h, t,τ, p. (h ̸= nil ∧ p ∈ τ ∧ accessible pt (h) ∧                           removed from lhsts , which is guaranteed by A.
                                                                                                                                               ′
            am pτ (h) ∧ rτp ) =⇒                                             • s = c := CoreAlloc(ē): If ∃e. e ∈ ē ∧ val τ (e) = h ,
                                                                                                 p′           p′
       ((∀t′ . t′ = t ∨ ¬accessible pt′ (h)) ⇐⇒ h ∈ lhspt ) ∧                  we get local (e) from rτ . Thus, ts = t as only a
                                                                               single thread can access h′ . From Asm. 6 and Lemma 4,
       ((∃t′ . t′ ̸= t ∧ accessible pt′ (h)) ⇐⇒ h ∈ ∗ghsp )                    localhl pt (h ′ ) holds, and we apply the induction hypothe-
Proof sketch. We prove this lemma by induction over pro-                       sis to obtain h′ ∈ lhspt . A guarantees that h′ remains in
gram traces. The base case for the empty trace holds trivially                 lhst and that h′ is not inserted into any other ghost
as there are no allocated and, thus, accessible heap locations                 set since h′ ̸= val τ (c). Otherwise, accessible pt (h ′ )
yet. In the inductive step, we prove this lemma for an arbitrary               holds because s cannot change h′ ’s accessibility as
heap location h′ , thread t, program point p′ , and trace τ                    the arguments ē are shallow (cf. Asm. 4) and, thus,
by applying the induction hypothesis to the immediately                        s internally does not have access to h′ . We apply the
preceding program point p and showing that we obtain the                       induction hypothesis and observe that A does not change
specified set containment for p′ . I.e., we assume the premise                 set containment of h′ .
and show that                                                                • s = r̄ := CoreApi_k(c, ē): We reason similarly as in
                                   ′                      ′                    the case of CoreAlloc(ē) except that we consider a
 ((∀t′ . t′ = t ∨ ¬accessible pt ′ (h ′ )) ⇐⇒ h′ ∈ lhspt ) ∧
                               ′                           ′     (4)           third case, namely ∃r. r ∈ r̄ ∧val τ (r ) = h′ . In this case,
                                                                                                                                           ′
 ((∃t′ . t′ ̸= t ∧ accessible pt ′ (h ′ )) ⇐⇒ h′ ∈ ∗ghsp )                         ′
                                                                               rτp guarantees that h′ is local and from accessible pt (h ′ )
                                                                                                         ′
holds. We case split on statement s (before applying A) such                   follows that t = ts . h is a heap location newly allocated
that executing A(s) on thread ts transitions from p to p′ . We                 by s and A guarantees that h′ is inserted into lhst . From
first note that the restrictions r are monotonic′ when going                   Lemma 6, we get that h′ is in no other ghost set.
                                                                                                       ′
backwards on a trace, i.e., rτp follows from rτp .                           • s = fork (x̄) {s }: Let us call the newly spawned

   • s = skip: Since skip does not allocate any heap
                                                                               thread t′s with t′s ̸= ts . Since t′s can access the
      locations and leaves accessibility unchanged, we get                     variables x̄, we have ∀h. h ∈ reach pτ (x̄)                   =⇒
                                                                                            p′                   p′          ′             p
      accessible pt (h ′ ) and apply the induction hypothesis.                 accessible ts (h) ∧ accessible ts′ (h). If h ̸∈ reach τ (x̄),
      Because algorithm A leaves all ghost sets unmodified,                    then accessibility of h′ does not change by executing
      (4) holds.                                                               s, and we apply the induction hypothesis and note that
                                 ′
   • s = x := new(): If h = val τ (x ), then t = ts as                         A does not modify set containment of h′ . In particular,′
                  p′
      accessible t (h ′ ) holds and no other thread can access                 h′ is not accessible by t′s and, thus, h′ ̸∈ lhspt′s holds
      h′ yet. A adds h′ to lhst and (4) holds as h′ is in no                                                                       p
                                                                               as required by (4). Otherwise (h′ ∈ reach τ (x̄)), we
                                                                                                                    ′
      other ghost set (by Lemma 6). Otherwise, h′ is already                   have to prove that ∀t′ . h′ ̸∈ lhspt′ and h′ ∈ ∗ghsp hold.
                                                                                                                                         ′


      allocated at p, and we apply the induction hypothesis                                          p
                                                                               Since accessible ts (h ′ ) holds, we apply the induction
      to obtain (4) as A neither adds nor removes h′ to and                    hypothesis and case split on whether h′ ∈ lhspts holds.
      from any ghost set.                                                      If so, A moves h′ from lhsts to ∗ghs, which is sufficient
   • s = x := ∗e: Since s neither allocates new heap lo-
      cations nor changes accessibility of h′ , accessible pt (h ′ )


                                                                        33
                 rτp ≜ (∀s, x, e, ℓ. sℓ = ∗x := e ∧ ℓ ≺ p =⇒ am pre-ℓ
                                                                τ     (val τ (x ))) ∧
                        (∀s, c, e, ē, ℓ. sℓ = c := CoreAlloc(ē) ∧ ℓ ≺ p ∧ e ∈ set(ē) =⇒
                                val τ (e) = nil ∨ am pre-ℓ
                                                     τ     (val τ (e)) ∧ local post-ℓ (e)) ∧
                        (∀s, k, c, e, ē, r, r̄, ℓ. sℓ = r̄ := CoreApi_k(c, ē) ∧ ℓ ≺ p ∧ e ∈ set(ē) ∧ r ∈ set(r̄) =⇒
                               (val τ (e) = nil ∨ am pre-ℓ
                                                     τ     (val τ (e)) ∧ local post-ℓ (e)) ∧
                               (val τ (c) = nil ∨ ¬am pre-ℓ
                                                      τ     (val τ (c))) ∧
                               (val τ (r ) = nil ∨ local post-ℓ (r )))

Figure 34. rτp expresses requirements that all statements in a codebase before program point p on trace τ must satisfy. These requirements allow us to
relate properties of heap locations to containment in the ghost sets. In particular, heap write statements must write to Application-managed heap locations
only, arguments that are passed to the Core (i.e., ē in CoreAlloc(ē) and r̄ := CoreApi_k(c, ē) statements) must be Application-managed and local
after executing the statement unless they are nil, the Core instance c must not be Application-managed, and return arguments from the Core, i.e., r̄ in
r̄ := CoreApi_k(c, ē), must be local or nil.

                                                                                                             ′
      as ∀t′ . t′ ̸= ts =⇒ h′ ̸∈ lhspt′ holds. Otherwise,                       and show that h′ ∈ ihspt holds. We case split on statement s
                                               ′
      h′ ∈ ∗ghsp holds and A ensures h′ ∈ ∗ghsp .                               (before applying A) such that executing A(s) on thread ts
                                                                                transitions from p to p′ . We first note that the restrictions r
                                                                                are monotonic when going backwards on a trace, i.e., rτp
                                                                                                      ′
Corollary 5 (Set containment in lhs ∪ ∗ghs). A variable x                       follows from rτp .
is in a thread t’s lhst or ∗ghs at program point p if x is                         • s = skip: Since skip does not allocate Core instances
a defined variable, all heap locations x may point to are                            and leaves accessibility unchanged, we get localhl pt (h ′ )
Application-managed, and the requirements rτp hold.                                                                                                    ′
                                                                                     and apply the induction hypothesis. We get h′ ∈ ihspt
    ∀x, t,p, τ. p ∈ τ ∧ defined pt (x ) ∧ rτp ∧                                      as A leaves all ghost sets unmodified.
                                                                                                                ′
               (∀h. as τ (h) ∈ pts(x ) =⇒ am pτ (h)) =⇒                            • s = x := new(): h ̸= val τ (x ) holds because x points
                                                                                     to a newly allocated heap location that has not been
          val τ (x ) = nil ∨ val τ (x ) ∈ (lhst ∪ ghs)p
                                                                                     passed through the return argument of CoreAlloc(ē).
where defined pt (x ) expresses that x is defined at p for                           Thus, localhl pt (h ′ ) holds, and we apply the induction
thread t.                                                                            hypothesis. We observe that A leaves ihst unchanged.
                                                                                   • s = x := ∗e: Since s does not allocate Core instances,
Proof sketch. Let x, t, p, and τ be arbitrary and assume
                                                                                     pt pCore (h ′ , t) holds, and we apply the induction hypoth-
the corollary’s premise. If val τ (x ) = nil holds, then the
                                                                                     esis. The lemma holds as A does not modify ihst .
corollary holds trivially. Otherwise, x points at p to an
                                                                                   • s = ∗x := e: Identical reasoning as for reading a heap
allocated heap location, which we call h′ , that is, thus,
                                                                                     location.
accessible from thread t i.e., h′ = val τ (x ) ∧ accessible pt (h ′ ).                                                                           ′
                                                                                   • s = c := CoreAlloc(ē): If val τ (c) = h , then
From Asm. 5 we obtain as τ (h ′ ) ∈ pts(x ) and, thus, am pτ (h ′ )                           p′
holds. We apply Lemma 7 and observe that one of the                                  localhl t (h ) implies t = ts . A guarantees that h′ ∈
                                                                                                      ′
                                                                                          ′

equivalences’ left-hand sides must be satisfied. Therefore, h′                       ihspt . Otherwise, localhl pt (h ′ ) and pt pCore (h ′ , τ ) hold,
                                                                                                                                                 ′
is either in lhspt or ∗ghsp .                                                        and we apply the induction hypothesis. h′ ∈ ihspt holds
                                                                                     as A does not remove elements from ihs.
Lemma 8 (Locality implies set containment for Core in-
                                                                                   • s = r̄ := CoreApi_k(c, ē): Since s does not allocate
stances). A heap location h at program point p that cor-
                                                                                     Core instances, localhl pt (h ′ ) and pt pCore (h ′ , τ ) hold, and
responds to a Core instance returned from an earlier
                                                                                     we apply the induction hypothesis. Furthermore, A does
CoreAlloc(ē) statement is in a thread t’s ihs if h is local
                                                                                     not remove elements from ihst′ for any thread t′ .
and the restrictions rτp (Fig. 34) hold.                                                                      ′
                                                                                   • s = fork (x̄) {s }: Let us call the newly spawned
                                                                                                                                 ′
          ∀h, t, τ, p.h ̸= nil ∧ p ∈ τ ∧ localhl pt (h) ∧                            thread t′s with t′s ̸= ts . If accessible tps (h ′ ), then t = t′s
                      pt pCore (h, τ ) ∧ rτp =⇒ h ∈ ihspt                            as h′ is local. However, h′ can only be accessible to
                                                                                     t′s if h′ is reachable from x̄, which is accessible from
Proof sketch. We prove this lemma by induction over pro-                             thread ts too. I.e., accessible tps (h ′ ) holds contradicting
gram traces. The base case for the empty trace holds                                           ′

trivially as there are no allocated heap locations yet. In                           localhl pt (h ′ ). Otherwise, A initializing ihst′s to the
the inductive step, we prove this lemma for an arbitrary                             empty set does not violate the lemma as t′s cannot access
heap location h′ , thread t, program point p′ , and trace τ                          h′ . Furthermore, we apply the induction hypothesis as
by applying the induction hypothesis to the immediately                              pt pCore (h ′ , τ ) holds, and we note that A does not remove
preceding program point p and showing that we obtain the                             any element from ihst .
specified set containment for p′ . I.e., we assume the premise



                                                                           34
Corollary 6 (Escape analysis implies set containment in ihs).                   Lemma 9 (Discharging the requirements). We show that
A variable x is in a thread t’s ihst at program point p if x is                 the judgments provided by our static analyses j (sℓ ) (cf.
a defined variable, local, all heap locations x may point to                    Def. 17) for every statement s at label ℓ before program
passed through the return parameter of some CoreAlloc(ē),                      point p and our assumptions are sufficient to discharge the
and the requirements rτp hold.                                                  requirements rτp (cf. Fig. 34).
 ∀x, t,p, τ. p ∈ τ ∧ local p (x ) ∧ defined pt (x ) ∧ rτp ∧                             ∀p, τ. p ∈ τ ∧ (∀s, ℓ. ℓ ≺ p ∧ j (sℓ )) =⇒ rτp
            (∀h. as τ (h) ∈ pts(x ) =⇒ pt pCore (h, τ )) =⇒
                                                                                Proof sketch. We prove this lemma by induction over pro-
       val τ (x ) = nil ∨ val τ (x ) ∈ ihspt                                    gram traces. The base case for the empty trace holds trivially
Proof sketch. Let x, t, p, and τ be arbitrary and assume                        as there are no preceding statements sℓ . In the inductive
the corollary’s premise. If val τ (x ) = nil holds, then the                    step, we prove this lemma for an arbitrary program point p′
corollary holds trivially. Otherwise, x points at p to an                       and trace τ by applying the induction hypothesis to the
allocated heap location, which we call h′ , which is, thus,                     immediately preceding        ′
                                                                                                               program point p. ′I.e., we show that
accessible from thread t, i.e., h′ = val τ (x )∧accessible pt (h ′ ).           ∀s′ , ℓ′ . ℓ′ ≺ p′ ∧ j (s′ℓ ) and rτp imply rτp by case splitting
localhl pt (h ′ ) follows from Asm. 6. From Asm. 5 we ob-                       on statement sℓ , whose execution transitions from p to p′ .
tain as τ (h ′ ) ∈ pts(x ) and, thus, pt pCore (h ′ , τ ). Applying                      ℓ
                                                                                   • s = ∗x := e: We have to prove that am τ (val τ (x ))
                                                                                                                                         p
Lemma 8 completes the proof.                                                           holds. From j (sℓ ) and Asm. 5, we get val τ (x ) = nil ∨
     Having defined the properties that successfully executing                        am pτ (val τ (x )). x ̸= nil holds as the statement would
our static analyses provides, we present next how we apply the                         otherwise crash (cf. Asm. 2).
                                                                                         ℓ
                                                                                   • s = c := CoreAlloc(ē): We have to show for
static analyses in Diodon (Def. 17) and prove in Lemma 10
that this application discharges the side conditions ω (cf.                            an arbitrary argument e ∈ set(ē) that val τ (e) =
                                                                                                                      ′

Fig. 15).                                                                              nil∨am pτ (val τ (e))∧local p (e) holds. If val τ (e) ̸= nil,
     As shown in Def. 17, we check for every heap read                                 then we apply Asm. 5 to obtain am pτ (val τ (e)) from
operation x := ∗e that e points to Application-managed                                local ℓam (ē).
                                                                                         ℓ
heap locations, which are identified by their allocation site a.                   • s = r̄ := CoreApi_k(c, ē): We proceed identically as
Analogously, we check for heap writes ∗x := e that x                                   in the case of CoreAlloc(ē). Additionally, we have to
satisfies the same property. For every CoreAlloc(ē) and                               show val τ (c) = nil ∨ ¬am pτ (val τ (c)) and val τ (r ) =
                                                                                                       ′
r̄ := CoreApi_k(c, ē), we check that the arguments ē point                           nil ∨ local p (r ) for an arbitrary return argument r ∈ r̄,
to disjoint heap locations and that these heap locations are                           which we get from local ℓCore (c) by applying Asm. 5
local and Application-managed. Additionally, we check for                              and local ℓret (r̄ ).
r̄ := CoreApi_k(c, ē) that c points to a local Core instance,                                           p′                                       ℓ
                                                                                   • Otherwise: rτ holds because no requirements for s
i.e., a local heap location that has been returned by an earlier                       must be met.
Core allocation call, and that the outputs r̄ are local.
Definition 17 (Static analyses for Diodon). In Diodon, we                       Lemma 10 (Discharging the side conditions ω). We show
execute the static analyses on a codebase to obtain the                         that the judgments provided by our static analyses j (s) (cf.
following judgments for every statement s at label ℓ therein,                   Def. 17) for every statement s in a codebase c together
denoted as j (sℓ ).                                                             with our assumptions are sufficient to discharge the side
                   j (x := ∗e) ≜ ∀a, τ. a ∈ pts(e) =⇒                           conditions ω(s) (cf. Fig. 15).
                                           am pre-ℓ
                                              τ     (a)                                       ∀s ∈ c. (∀s′ ∈ c. j (s′ )) =⇒ ω(s)
                   j (∗x := e) ≜ ∀a, τ. a ∈ pts(x ) =⇒                          Proof sketch. We prove this lemma for an arbitrary state-
                                           am pre-ℓ
                                              τ     (a)                         ment s at label ℓ such that s ∈ c, assume ∀s′ ∈ c. j (s′ )
     j (c := CoreAlloc(ē)) ≜ disjoint as (ē) ∧ local ℓam (ē)                 and show that ω(s) holds by case splitting on statement s.
                                                                                Throughout the proof, we use program point p to refer to s’s
 j (r̄ := CoreApi_k(c, ē)) ≜ disjoint as (ē) ∧ local ℓam (ē)                 pre-state, i.e., p ≜ pre-ℓ. We obtain ∀τ. rτp from Lemma 9.
                                    ∧ local ℓCore (c) ∧ local ℓret (r̄ )           • s = x := ∗e: From Cor. 5, we get val τ (e) =

where                                                                                nil ∨ val τ (e) ∈ (lhs ∪ ghs)p . e points to an allocated
                                                                                     heap location and cannot be nil as the statement would
disjoint as (ē) ≜ ∀i, j. 0 ≤ i < j < len(ē) =⇒                                     otherwise crash (cf. Asm. 2).
                         pts(ē[i ]) ∩ pts(ē[j ]) = ∅                             • s = ∗x := e: Analogous to heap reads but for x instead

   local ℓam (ē) ≜ ∀e, h, τ. e ∈ set(ē) ∧ as τ (h) ∈ pts(e) =⇒                     of e.
                                                                                   • s = c := CoreAlloc(ē): From disjoint as (ē), we
                            local post-ℓ (e) ∧ am pre-ℓ
                                                  τ     (h)                          obtain disjoint(ē) by applying Lemma 2. local ℓam (ē)
 local ℓCore (c) ≜ ∀h, τ. as τ (h) ∈ pts(c) =⇒
                         local pre-ℓ (c) ∧ pt pre-ℓ
                                              Core (h, τ )
   local ℓret (r̄ ) ≜ ∀r, τ. r ∈ set(r̄) =⇒ local post-ℓ (r )

                                                                           35
    allows us to apply Lemma 7 providing ∀e ∈                             the ghost flag ∗used to false. sinit is similar in spirit to the
    set(ē). val τ (e) = nil∨val τ (e) ∈ lhsp . Lastly, ∗used =           ghost statements that algorithm A inserts as these statements
    false holds by our assumption that we have a single                   are necessary to construct a proof for the codebase c.
    Core allocation statement in the codebase c. We lift                  Cor. 1’s premise states that our static analyses succeed on
    this assumption in Sec. 5.2.2.                                        the codebase c, such that we obtain j (s) for each statement s
  • s = r̄ := CoreApi_k(c, ē): Likewise to the previous                  therein, and that we prove a Hoare triple for each Core
    case, we obtain disjoint(ē) and ∀e ∈ set(ē). val τ (e) =            function satisfying the syntactic restrictions.
    nil ∨ val τ (e) ∈ lhsp . Left to show is val τ (c) = nil ∨                We combine the proof for the entire codebase that we
    val τ (c) ∈ ihsp , which we obtain from local ℓCore (c) by            obtain from Cor. 7 with the result of App. A.1 to obtain
    applying Cor. 6.                                                      Diodon’s overall soundness result. This result states that
  • Otherwise: ω(s) = true and, thus, the lemma holds                     successfully executing our static analyses on codebase c
    trivially.                                                            and auto-actively verifying its Core suffices to prove that
                                                                          the traces of executing c together with other verified imple-
                                                                          mentations and the environment are contained in the traces
                                                                          described by the abstract protocol model.
A.2.4. Proof Construction. While we showed that we can
compose the proof rules in Fig. 14 and discharge their side               Theorem 8 (Overall soundness). Suppose Asm. 1 holds and
conditions ω, it remains to show that we initially establish              that we have established, for each role i, I/O independence
the global context Πg and the local program invariant Πl ,                and Cor. 7’s antecedent for a codebase ci (rid ) and I/O
such that we obtain a proof for the entire codebase c. We                 specification ψi (rid ). Then
close this gap in Cor. 7.                                                              (|||i,rid πint (Ci (rid ))) ∥χ′ E ≼t R.
Corollary 7 (Proof construction). Successfully executing                  Proof sketch. We apply Cor. 7 to obtain for each role i
Diodon’s static analyses on a codebase c and the Core’s                   emp ⊢ [ψi (rid )] sinit ; A(ci (rid )) [true]. Since we omitted
auto-active verification combined with our assumptions allow              the turnstile subscript α (cf. Asm. 1) throughout App. A.2 for
us to construct a separation logic proof for c.                           brevity and emp on the turnstile’s left-hand side is a nota-
   If ∀s, k. s ∈ c ∧ j (s) ∧                                              tional difference only (Asm. 1 could be adapted accordingly),
                                                                         we apply Thm. 3 to obtain the desired result.
         s = c := CoreAlloc(ē) =⇒
                                                         
                                                                          A.2.5. Limitations. Our formalization defines a simple
            Πg ⊢ [PCoreAlloc (ē)] s [QCoreAlloc (c, ē)] ∧
                                                                         programming language to focus on the main ideas of our
            s = r̄ := CoreApi_k(c, ē) =⇒                                 soundness proof and to show that successfully executing our
                                                                         static analyses discharges all side conditions. We believe
            Πg ⊢ [PCoreApi_k (c, ē)] s [QCoreApi_k (c, ē, r̄)] ,        this language covers the most critical features like heap
                                                                          manipulations and concurrency as these features are relevant
then emp ⊢ [ϕ] sinit ; A(c) [true]                                        for the results of our static analyses. In addition, we abstract
where sinit is ghost code creating and initializing the thread-           each function making up the Core’s API to a dedicated state-
local ghost sets lhs and ihs for the main thread, as well as              ment in our language, and assume that the specification of
the global ghost set ∗ghs and the ghost flag ∗used.                       each such function satisfies our syntactic restrictions Asm. 4.
                                                                          However, there is a slight risk that this language misses Go
Proof sketch. All our proof rules (cf. Fig. 14) have the same             features that would be a threat to soundness such as function
shape, namely Πg ⊢ [Πl ] A(s) [Πl ] for a statement s. As                 boundaries, complex control flow, and callbacks; the former
shown by Lemma 10, the judgments obtained from the static                 two features would be straightforward to add, and we discuss
analyses allow us to discharge the side conditions that are               in Sec. 5.2.2 how to add the latter.
associated with each proof rule (Fig. 15). Therefore, left to                 To prove a Hoare triple for the entire codebase, we
show is that we initially establish Πl and Πg such that we                assume that the Application is free of crashes Asm. 2and
can compose the proof rules to form a proof for an entire                 data races Asm. 3. While our soundness proof does not
codebase c. The ghost statement sinit creates and initializes             make any statement in the case that the program crashes,
the ghost sets lhs, ihs, and ∗ghs as well as the ghost flag               our compositional proof informally guarantees that the trace
∗used. Thus, we can complete the proof tree as shown in                   inclusion holds for the program’s prefix up to the program
Fig. 35. This constitutes a proof for c as neither sinit nor the          point at which a crash occurs, such that the crash freedom
statements added by A modify c’s runtime behavior.                        assumption could be dropped, which we leave to future work.
    We show that we obtain the desired proof for the                      However, data race freedom remains an assumption; more
entire codebase, namely that the codebase satisfies the                   generally, we assume the absence of undefined behavior
I/O specification ϕ expressed as the Hoare triple emp ⊢                   for programming languages other than Go and our formal-
[ϕ] sinit ; A(c) [true]. This Hoare triple relies on sinit that           ized one. This assumption can be mitigated by performing
initializes lhs, ihs, and ∗ghs to empty sets, as well as sets             additional static analyses.




                                                                     36
                                                                                              ·
                                                                                              · F ig. 14
                                                                                              ·
                                              ·                                     Πg ⊢ [Πl ] A(p) [Πl ]
                                              ·
                                              ·                                                             Conseq
                                   emp ⊢ [emp] sinit [Rg ⋆ Rl ]                    Πg ⊢ [Πl ] A(p) [true]
                                                                    Frame                                     Share
                                   emp ⊢ [ϕ] sinit [Rg ⋆ Rl ⋆ ϕ]               emp ⊢ [Πg ⋆ Πl ] A(p) [Πg ]
                                                                    Conseq                                     Conseq
                                     emp ⊢ [ϕ] sinit [Πg ⋆ Πl ]               emp ⊢ [Πg ⋆ Πl ] A(p) [true]
                                                                                                               Seq
                                                          emp ⊢ [ϕ] sinit ; A(p) [true]


                     with   Rl ≜ lhs = ∅ ⋆ ihs = ∅                        Rg ≜ acc(ghs) ⋆ ∗ghs = ∅ ⋆ acc(used) ⋆ ∗used = false

Figure 35. Proof tree showing the initial establishment of Πl and Πg for a codebase p. We assume that the ghost statement sinit initializes lhs and ihs to
the empty set, as stated in Rl , and allocates two heap locations on the ghost heap storing ∅ and false to which ghs and used point, respectively (cf. Rg ).


A.2.6. Extensions. Having covered the main soundness                              as temporarily pausing the execution of these auto-actively
result, we discuss two extensions to bridge the gap to realistic                  verified Core statements to (sequentially) execute some
applications of Diodon as used in our case studies. We first                      statements belonging to the Application before eventually
lift the restriction of at most one Core instance to allow                        resuming execution of Core statements.
a codebase to create unboundedly many Core instances.                                 With respect to algorithm A and the ghost sets, inter-
Second, we allow the Core to invoke callbacks into the                            rupting the execution of Core statements to execute certain
Application and discuss the side conditions that arise by                         Application statements sapp means that heap locations on
this extension.                                                                   which the Core statements operate are missing from the ghost
Unboundedly many Core instances. So far, our global                               sets while executing sapp as we remove them from the ghost
program invariant Πg contains the separating conjunct                             sets before executing Core statements and put them back only
                                                                                  after the Core statements’ postcondition holds. Missing per-
                acc(used) ⋆ (¬(∗used) =⇒ ϕ).                                      missions include both arguments ē and the Core instance c.
As explained in App. A.1, each execution of a protocol                            Therefore, we have to make sure that sapp neither accesses
role is parameterized by a unique rid . I.e., ϕ and all I/O                       heap locations to which ē points nor invokes API calls on
permissions that ϕ internally provides are parameterized                          the Core instance c as the Core invariant might not hold.
by rid and, thus, are not interchangeable but specific to a                           We can lift these restrictions by introducing additional
particular rid . Hence, we can change the separating conjunct                     proof obligations for the auto-active verification. More specif-
stated above to                                                                   ically, if we auto-actively prove that the Core statements
                                                                                  satisfy a particular precondition for the callback, then we can
           acc(used) ⋆ (∀rid ̸∈ ∗used =⇒ ϕ(rid ))                                 update the ghost sets accordingly. E.g., such a precondition
                                                                                  can specify permissions for heap locations passed to the
providing a family of I/O permissions, where used points
                                                                                  callback or that the Core invariant holds.
to a ghost set containing the rid s that have already been
                                                                                      In our SSM Agent case study (Sec. 6.1), we make use
used. In addition, we adapt the entire program’s precondition
                                                                                  of these proof obligations for the callback delivering in-
from ϕ to ∀rid . ϕ(rid ) and change the translation A(c :=
CoreAlloc(ē)) to, first, pick a fresh rid ′ such that rid ′ ̸∈
                                                                                  coming messages to the Application as we specify that
∗used and, second, adding rid ′ to ∗used. Picking such a
                                                                                  the Core transfers permission for the incoming message
fresh rid ′ is always possible since rid ranges over N.
                                                                                  to the Application. Conceptually, this allows us to add
                                                                                  the corresponding heap location to lhs before executing the
Adding callbacks to the Core. So far, we have treated the                         statements constituting the callback because the auto-active
statements CoreAlloc(ē) and r̄ := CoreApi_k(c, ē) as                            proof guarantees that no statement in the Core thereafter
atomic statements in our language. These two statements are                       accesses this heap location.
internally implemented as sequences of statements, which                              For our case studies, it was not necessary to transfer
we hereafter call Core statements. As these statements                            permissions from a callback back to the Core via a callback’s
constitute the Core, we auto-actively prove that a particular                     postcondition. Extending Diodon to allow such permission
postcondition holds when control transfers back to the                            transfers would require an analysis of the callback showing
Application after fully executing these statements.                               that the Application possesses these permissions while
    In the presence of callbacks, however, calling into the                       executing the callback and that the corresponding heap
Core becomes non-atomic and control flow might transfer                           locations do not get accessed by the Application after the
to the Application before reaching the post-state for which                       callback returns.
we know that the postcondition holds. We can treat callbacks




                                                                             37
  M1 .    A ⇒ S : ⟨SignReq, Id skA , g x , Id M , Id B ⟩                           which we model in Tamarin as generating a fresh term x
  M2 .    S ⇒ A : ⟨SignResp, sig x ⟩                                               and computing the corresponding public key via modular
  M3 .    A → B : ⟨SessReq, g x , sig x , Id skA , Id M ⟩                          exponentiation denoted by g x . Then, A sends message M1
  M4 .    B ⇒ S : ⟨VerReq, Id A , Id skA , g x , Id M , Id B , sig x ⟩             to instruct KMS to use a particular signing key belonging
  M5 .    S ⇒ B : ⟨VerResp⟩                                                        to A, identified by Id skA , to sign the triple ⟨g x , Id M , Id B ⟩.
                                                                                   This triple includes the monitor’s and B’s identity to prevent
  M6 .    B ⇒ S : ⟨SignReq, Id skB , g y , Id A ⟩
                                                                                   Mallory-in-the-middle (MITM) attacks. KMS checks whether
  M7 .    S ⇒ B : ⟨SignResp, sig y ⟩                                               the requested signing key actually belongs to A before creat-
  M8 .    B → A : ⟨SessResp, g y , sig y , Id skB , h(g x∗y )⟩                     ing and sending the signature in M2 back to A. This allows
  M9 .     A ⇒ S : ⟨VerReq, Id B , Id skB , g y , Id A , sig y ⟩                   A to send a session request (M3 ) to B, which includes g x ,
  M10 . S ⇒ A : ⟨VerResp⟩                                                          the signature, and the signing key’s and monitor’s identities.
  M11 . A ⇒ S : ⟨SignReq, Id skA , css , Id B ⟩                                         After receiving a session request, B first checks the
  M12 . S ⇒ A : ⟨SignResp, sig ss ⟩                                                received signature via KMS. For this purpose, B sends the
  M13 . A → M : ⟨SSKey, css , sig ss , Id A , Id skA , Id B ⟩                      signature itself and the components over which the signature
  M14 . A → B : ⟨HSDone, css , senc(⟨HSPay, z⟩, kdf1 (g x∗y ))⟩                    is computed in a signature check request (M4 ) to KMS. If
  M15 . A → B : ⟨Msg, senc(z, kdf1 (g x∗y ))⟩                                      the signature is valid, KMS replies with a signature check
  M16 . B → A : ⟨Msg, senc(z, kdf2 (g x∗y ))⟩                                      response (M5 ). Otherwise, KMS aborts the protocol, which
                                                                                   we model as not sending any response. Afterwards, B
      where      sig x ≜ sign(⟨g x , Id M , Id B ⟩, sk A )                         generates its elliptic-curve public-private key pair (g y , y)
                 sig y ≜ sign(⟨g y , Id A ⟩, sk B )                                and uses KMS to sign g y and A’s identity. B then sends a
                 css    ≜ aenc(⟨kdf1 (g x∗y ), kdf2 (g x∗y )⟩, pk M )              session response (M8 ) to A that contains B’s public curve
                 sig ss ≜ sign(⟨css , Id B ⟩, sk A )                               point, the signature, the identity of B’s signing key, and a
                                                                                   hash of the shared secret h(g x∗y ). The latter allows A to
Figure 36. Signed DH key exchange for deriving the symmetric                       detect early on if A and B computed different shared secrets,
keys kdf1 (g x∗y ) and kdf2 (g x∗y ) that are used during the transport
phase, i.e., in messages M15 and M16 . We use → and ⇒ to denote
                                                                                   e.g., due to an attempted replay attack.
communication via the untrusted network and a secure channel, respectively.             After receiving a session response, A computes the
                                                                                   shared secret and checks that it derives the same shared
                                                                                   secret’s hash value. Additionally, A checks the received
Appendix B.                                                                        signature using KMS and derives the two symmetric session
Secure Shell Session Protocol                                                      keys from the shared secret by applying two different key
                                                                                   derivation functions (KDFs) kdf1 and kdf2 . To enable a
    Fig. 36 shows the protocol for establishing interactive
                                                                                   trusted monitor M to audit the shell session, A computes css
shell sessions between an SSM Agent (A) and a customer (B).
                                                                                   by asymmetrically encrypting the two session keys using the
The protocol includes two additional roles namely KMS (S)
                                                                                   monitor’s public key pk M . Next, role A requests a signature
and an optional, trusted monitor (M) that is allowed to inspect
                                                                                   from KMS for css and B’s identity to bind these identities
the established shell sessions, e.g., for compliance reasons.
                                                                                   to the session keys. The handshake ends by sending the
    Since A and B do not personally possess their secret
                                                                                   encrypted session keys to the monitor (M13 ) and confirming
keys for creating signatures, we explicitly model the presence
                                                                                   the session keys to B (M14 ). The latter message includes
of and the interactions with KMS that remotely creates and
                                                                                   some version information, which we model as an attacker-
checks signatures. We model these interactions as happening
                                                                                   chosen payload z .
on a secure channel, indicated by ⇒, because each role
                                                                                        Message M13 enables M, a trusted third party, to monitor
instance of A and B establishes a TLS connection to KMS.
    On a high-level, this protocol performs a signed                               the transmitted shell commands should this be necessary
elliptic-curve DH key exchange establishing two symmetric                          for regulatory reasons (otherwise sending message M13
keys kdf1 (g x∗y ) and kdf2 (g x∗y ). These keys are used in                       can simply be skipped). For this purpose, role A sends the
the transport phase, i.e., M15 and M16 , to symmetrically                          asymmetrically encrypted session keys to the monitor M such
encrypt (senc) payloads for sending in a particular direc-                         that M can obtain the session keys and, thus, decrypt and
tion. In Tamarin, we model the transport phase as a non-                           audit the transport messages. Note that the monitor does not
deterministic loop that allows each role A and B to send                           need to be online during the handshake or transport phase;
and receive an unbounded number of transport messages and                          it is sufficient for the monitor to come online at a later time
interleave them arbitrarily.                                                       as an untrusted log server could store message M13 and all
    More specifically, the protocol proceeds as follows.                           messages sent during the transport phase until M becomes
Role A first generates an elliptic-curve public-private key pair,                  online and fetches these messages from the log server.




                                                                              38
