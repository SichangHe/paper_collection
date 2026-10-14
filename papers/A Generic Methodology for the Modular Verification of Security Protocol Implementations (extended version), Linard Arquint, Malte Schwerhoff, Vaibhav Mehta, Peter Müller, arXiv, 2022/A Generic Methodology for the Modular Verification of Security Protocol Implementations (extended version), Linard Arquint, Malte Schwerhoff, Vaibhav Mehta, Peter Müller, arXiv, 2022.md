                                                              A Generic Methodology for the
                                                 Modular Verification of Security Protocol Implementations
                                                                    (extended version)
                                                                           Linard Arquint                                                                   Malte Schwerhoff
                                                               Department of Computer Science                                                        Department of Computer Science
                                                                  ETH Zurich, Switzerland                                                               ETH Zurich, Switzerland

                                                                          Vaibhav Mehta∗                                                                        Peter Müller
                                                                          Cornell University                                                        Department of Computer Science
arXiv:2212.02626v2 [cs.CR] 10 Sep 2023




                                                                           Ithaca, NY, USA                                                             ETH Zurich, Switzerland
                                         ABSTRACT                                                                                       obvious that formal proofs are necessary for verifying that crypto-
                                         Security protocols are essential building blocks of modern IT sys-                             graphic protocols actually provide the desired properties.
                                         tems. Subtle flaws in their design or implementation may compro-                                   The vast majority of existing work on automated protocol ver-
                                         mise the security of entire systems. It is, thus, important to prove the                       ification targets protocol models, i.e., abstract descriptions of the
                                         absence of such flaws through formal verification. Much existing                               cryptographic operations and message exchanges that constitute
                                         work focuses on the verification of protocol models, which is not suf-                         a protocol. The verification of protocol models is useful to show
                                         ficient to show that their implementations are actually secure. Veri-                          the security of the protocol design, but does not guarantee that
                                         fication techniques for protocol implementations (e.g., via code gen-                          concrete protocol implementations are also secure. Common pro-
                                         eration or model extraction) typically impose severe restrictions on                           gramming errors (e.g., missing bounds checks in the Heartbleed
                                         the used programming language and code design, which may lead to                               bug [5]) or incorrect implementations of the design (e.g., acciden-
                                         sub-optimal implementations. In this paper, we present a method-                               tally omitted protocol steps in the Matrix SDK [6]) may render the
                                         ology for the modular verification of strong security properties                               implementation insecure even if the protocol design is secure.
                                         directly on the level of the protocol implementations. Our method-                                 Verifying protocol implementations is substantially more com-
                                         ology leverages state-of-the-art verification logics and tools to sup-                         plex than verifying models. Targeting realistic implementations
                                         port a wide range of implementations and programming languages.                                requires reasoning, for instance, about mutable data structures,
                                         We demonstrate its effectiveness by verifying memory safety and                                intricate control-flow (e.g., dynamic dispatch), concurrency, and
                                         security of Go implementations of the Needham-Schroeder-Lowe,                                  performance-optimized code. Moreover, implementations are sig-
                                         Diffie-Hellman key exchange, and WireGuard protocols, including                                nificantly larger than abstract models, and change more frequently,
                                         forward secrecy and injective agreement for WireGuard. We also                                 which requires modular verification techniques to decompose the
                                         show that our methodology is agnostic to a particular language or                              verification task and reduce the re-verification effort when code
                                         program verifier with a prototype implementation for C.                                        evolves. Modular reasoning is more difficult than the non-modular
                                                                                                                                        analyses typically used to verify protocol models.
                                         CCS CONCEPTS                                                                                       One approach at obtaining verified protocol implementations
                                                                                                                                        is to generate an executable implementation automatically from a
                                         • Security and privacy → Logic and verification.
                                                                                                                                        verified model (e.g., [7–11]). For instance, Bhargavan et al.’s DY*
                                         KEYWORDS                                                                                       framework [9–11] generates OCaml or C code from a functional
                                                                                                                                        implementation in F* [12]. The generated code is secure by construc-
                                         Protocol implementation verification, Symbolic security, Separation                            tion (provided the code generator is correct). However, changing the
                                         logic, Automated verification, Injective agreement, Forward secrecy.                           code manually (e.g., to optimize performance) forfeits any security
                                                                                                                                        guarantees. To achieve modular verification, DY* relies on a specific
                                         1     INTRODUCTION                                                                             coding discipline (at most one protocol step per F* function), which
                                         Cryptographic protocols, such as TLS, WireGuard [1], and Sig-                                  must be enforced manually, and is in general not adhered to by
                                         nal [2], are the cornerstones of today’s global communication net-                             existing implementations. A violation of this discipline unwittingly
                                         works because they ensure crucial security properties, such as                                 restricts the capabilities of the attacker and, thus, may cause DY*
                                         participant authentication and data privacy. With Lowe’s famous                                to miss attacks.
                                         attack on the Needham-Schroeder protocol [3, 4], it has become                                     An alternative approach is to verify security properties for a
                                         ∗ The work was performed during a fellowship at ETH Zurich.                                    protocol model that is extracted automatically from an implemen-
                                                                                                                                        tation (e.g., [13–17]). However, automatic model extraction often
                                         CCS ’23, November 26–30, 2023, Copenhagen, Denmark
                                         © 2023 Copyright held by the owner/author(s). Publication rights licensed to ACM.
                                                                                                                                        requires that implementations follow restrictive coding disciplines.
                                         This is the author’s version of the work. It is posted here for your personal use. Not         Similar restrictions apply to approaches based on executable models
                                         for redistribution. The definitive Version of Record was published in Proceedings of the       (e.g., [18,19]), i.e., models written in specific subsets of programming
                                         2023 ACM SIGSAC Conference on Computer and Communications Security (CCS ’23),
                                         November 26–30, 2023, Copenhagen, Denmark, https://doi.org/10.1145/3576915.3623105.            languages that facilitate reasoning, but typically do not provide the
                                                                                                                                        low-level features required for optimized implementations.
                                                                                                                                    1
CCS ’23, November 26–30, 2023, Copenhagen, Denmark                                          Linard Arquint, Malte Schwerhoff, Vaibhav Mehta, and Peter Müller


    Instead of automatically generating an implementation or ex-                       Go implementations of three protocols: Needham-Schroeder-
tracting a model, Arquint et al. [20] prove refinement between an ex-                  Lowe (NSL) [3,4], signed Diffie-Hellman (DH) [30], and Wire-
isting verified model and a corresponding existing implementation.                     Guard [1]. We show that our approach supports different
Their approach supports realistic implementations, but requires                        programming languages and verifiers by additionally imple-
expertise in and relies on the soundness of two tools (a model and                     menting a prototype of the reusable library for C and the
a program verifier). Moreover, formal models may not always exist,                     VeriFast verifier [21], and using it to verify a C implementa-
or may not be in sync with an evolving implementation.                                 tion of NSL. The implementations of our reusable verification
This work. We present a methodology for the verification of                            library and the case studies are open-source [31].
strong security properties (e.g., injective agreement, forward se-                 (5) We prove soundness of our approach, in particular, that the
crecy) directly on the level of the protocol implementations. Our                      global trace correctly reflects all relevant protocol steps and,
methodology leverages established program verification techniques                      thus, any security property proved for the trace indeed holds
that are supported by a wide range of existing automated1 tools                        for the protocol implementation.
(e.g., [21–25]), which makes it readily applicable. It is based on sep-        We build on and substantially extend two lines of prior work: Our
aration logic [26, 27], a program logic that supports the language             use of a global trace and security labels to prove secrecy is inspired
features used to write efficient implementations, such as mutable              by Bhargavan et al. [9], but our approach achieves modularity with-
heap data structures and concurrency. As a result, our method-                 out relying on a coding discipline (cf. earlier discussion of DY*),
ology applies to realistic implementations written in mainstream               and thus handles existing protocol implementations soundly. Our
programming languages such as C, Go, JavaScript, and Rust. Verifi-             encoding of the global trace as a concurrent data structure is in-
cation in our methodology is modular, that is, one can verify each             spired by Dupressoir et al. [32]. Their work depends on specific
method (or protocol participant) in isolation. Modularity is crucial           features of the used programming language (e.g., C’s volatile fields)
for scalability, to reduce the re-verification effort when the code            and verifier (VCC [33]), while we present a separation-logic-based
evolves, and to provide strong guarantees for libraries.                       methodology applicable across different programming languages
   As is common in protocol verification, we explicitly model the              and verifiers, as demonstrated by our case studies. The use of sep-
global trace of a protocol execution, which allows us to express               aration logic allows us to verify concurrent, heap-manipulating
security properties in ways familiar to security experts. This trace           programs and prove security properties that so far were out of
is expressed and manipulated via ghost code [28], that is, program             reach for invariant-based approaches.
code that is used for verification purposes, but erased by the com-            Outline. Sec. 2 introduces background on trace-based verification
piler before the program is executed. The ghost code required to               and our attacker model. In Sec. 3, we explain how we encode the
manipulate the global protocol trace is encapsulated in the I/O and            global trace and how we relate it formally to the local state of each
crypto libraries used by an implementation to ensure, e.g., that each          participant. In Sec. 4, we show how to prove important security
sent message is correctly reflected on the trace.                              properties based on a suitable trace invariant, and how we use sepa-
   Using ghost code allows us to cleanly separate the global trace,            ration logic’s linear resources to prove injective agreement. In Sec. 5,
which is necessary to prove protocol-wide properties, from the                 we introduce our reusable verification library, which implements
data structures maintained locally by each participant. We treat               our methodology, and substantially reduces the verification effort
each participant instance of a protocol (including a Dolev-Yao at-             per protocol. Sec. 6 describes our case studies. We explain the trust
tacker [29]) as a concurrent thread, and the global trace as shared            assumptions underlying our methodology and sketch its soundness
state among these threads. This approach allows us to reason about             proof in Sec. 7, discuss related work in Sec. 8, and conclude in Sec. 9.
unboundedly many participant instances and to leverage existing
verification techniques and tools for shared-data concurrency.                 2    TRACE-BASED VERIFICATION
Contributions. We make the following contributions:                            A protocol’s security depends on the interplay of the protocol par-
   (1) We present a modular verification methodology for protocol              ticipants in the presence of an attacker. A standard technique to
       implementations, based on global traces and concurrent sep-             verify security is to record all relevant actions of the participants
       aration logic, that applies to a wide range of programming              and the attacker on a global trace and to formulate the intended
       languages, protocol implementations, and verification tools.            security properties as properties of this trace. Verification then
   (2) We show how to use separation logic’s linear resources to               amounts to proving that all possible traces of a protocol satisfy the
       modularly prove injective agreement, i.e., the absence of               intended properties. In this section, we give a high-level overview
       replay attacks. To the best of our knowledge, we present the            of this approach; we provide the details in the later sections.
       first invariant-based verification technique for this property.         Attacker. We consider a Dolev-Yao attacker that has full control
   (3) We developed a reusable Go library that facilitates main-               over the network and performs symbolic cryptographic operations.
       taining the global trace; protocol-independent properties are           These operations are modeled as functions over symbolic values,
       verified once and for all for this library and can, thus, be            so-called terms, and encode the perfect cryptography assumption,
       reused for different protocol implementations.                          e.g., that decryption succeeds if and only if it uses the correct key.
   (4) We demonstrate the practicality of our approach by using the               An attacker can apply these functions to all terms in its knowl-
       Gobra verifier [22] to verify memory safety and security of             edge, which initially consists of all publicly-known terms, including
                                                                               string and integer constants. An attacker obtains additional knowl-
1 The proof search is automatic but relies on user-provided annotations.       edge by reading messages on the network. Furthermore, an attacker
                                                                           2
A Generic Methodology for the Modular Verification of Security Protocol Implementations (extended version)                  CCS ’23, November 26–30, 2023, Copenhagen, Denmark


                                                              Γ ⊢ [𝑃1 ] 𝐶 1 [𝑄 1 ]          Γ ⊢ [𝑃 2 ] 𝐶 2 [𝑄 2 ]                  Γ ⊢ [𝑃 ∗ 𝐼𝑟 ] 𝐶 [𝑄 ∗ 𝐼𝑟 ]
                                          (Write)                                                                   (Par)                                          (With)
 Γ ⊢ [𝑝 ↦→ _] *𝑝 := 𝑒 [𝑝 ↦→ 𝑒]                                    Γ ⊢ [𝑃 1 ∗ 𝑃2 ] 𝐶 1 || 𝐶 2 [𝑄 1 ∗ 𝑄 2 ]                     Γ, 𝑟 : 𝐼𝑟 ⊢ [𝑃] with (𝑟 ) {𝐶} [𝑄]

Figure 1: Selected separation logic proof rules: heap writes (cf. Sec. 3.1) along with parallel composition and lock-protected
critical sections (cf. Sec. 3.3). Side-conditions are omitted for simplicity.

may corrupt participants, which adds all terms in the state of the cor-                           we show how to verify concrete protocol implementations by relat-
rupted participant to the attacker knowledge. We model two kinds                                  ing the global trace of the protocol to the local state and operations
of corruption: Corrupting a participant leaks its long-term state,                                of each protocol participant. This verification is modular and can
which is common to all instances of this participant, such as long-                               be automated using existing verification tools.
term secret keys. Corrupting a participant session additionally leaks
short-term state, e.g., ephemeral secret keys, or exchanged nonces2 .
Trace entries. The global trace is a sequence of events. Each event                               3.1      Safety Verification
corresponds to a high-level operation performed by a participant                                  To support realistic, efficient, and existing protocol implementa-
or the attacker. It has a name and takes event-specific arguments.                                tions, our verification technique needs to handle programming
E.g., event CreateNonce(n) records that nonce n was created. This                                 concepts such as mutable heap structures and concurrency. To this
event is protocol-independent; we also support protocol-specific                                  end, we employ separation logic [26, 27], the de-facto standard
events to keep track of the progress within a protocol execution                                  for the modular verification of imperative code. Separation logic
and to express specific security properties. E.g., a protocol-specific                            is supported by existing verifiers for many languages, including
event may express which nonces or keys a participant uses to                                      VeriFast [21] for C, Prusti [25] for Rust, and Gobra [22] for Go. All
communicate with a peer (cf. Sec. 4).                                                             of them can be used in combination with our methodology.
   We use seven protocol-independent events: (1) A create nonce                                      In separation logic, each heap location is conceptually owned
event records that a fresh nonce has been generated. (2) A send                                   by a single function execution (similar to Rust). Attempting to
message event records that a message has been sent on the network.                                access a location without owning it results in a verification failure.
Both events may originate from a participant or the attacker. The                                 Ownership prevents data races in concurrent programs (since at
remaining five protocol-independent events model the capabilities                                 most one function may access a location at any point in time) and
of the attacker. (3) The (unique) root event is the first event on                                facilitates reasoning about side effects (as long as one function owns
every trace and contains the initial attacker knowledge. (4) An                                   a location, no other function can possibly modify it).
extend attacker knowledge event models that the attacker learns                                      In specifications, the points-to assertion 𝑝 ↦→ 𝑒 expresses owner-
additional terms, e.g., by applying a cryptographic operation to a                                ship, i.e., that the current function has an exclusive permission to
term already in the attacker knowledge. Corruption is represented                                 access location 𝑝 and that 𝑝 has value 𝑒 (we write _ if the value is ir-
by (5) a participant corruption or (6) a session corruption event. In                             relevant). For instance, the proof rule for heap updates (rule Write
both cases, we use extend-events (4) to add the newly-learned terms                               in Fig. 1) enforces via its precondition that the current function exe-
(from the corrupted state) to the attacker knowledge. At any point                                cution may update 𝑝 only if it holds the corresponding permission.
during a protocol run, the total attacker knowledge is therefore                                     Permissions are initially obtained when allocating a heap loca-
determined by the union of the root event (3), the send-events (2),                               tion, and are transferred between function executions upon call and
and the extend-events (4). Finally, (7) a drop message event records                              return according to the callee function’s specification. Permissions
that the attacker dropped a message from the network.                                             may also be transferred between threads, see Sec. 3.3.
Trace invariant. To reason modularly about the (unbounded) set                                       Verifying a protocol implementation in separation logic ensures
of all possible traces, we introduce a trace invariant, a property that                           that it is memory safe (e.g., does not cause null-pointer dereferences
must hold for every prefix of each trace produced by a protocol.                                  or buffer overflows), does not abort (e.g., due to division by zero),
Verification then consists of two main steps: first, proving that                                 and does not exhibit data races. Where needed for our safety or
each action of a participant or the attacker (according to the above                              security proof, we also verify functional correctness properties. We
attacker model) maintains the trace invariant and, second, showing                                omit the details of safety proofs here because they are routine work
that the trace invariant implies the intended security properties.                                in and orthogonal to the focus of this paper.
   An important component of a trace invariant are message in-
variants, which characterize the content of a message. For instance,
a message invariant might express that a message parameter is a                                   3.2      Relating Bytes with Terms
nonce (as opposed to an arbitrary term).
                                                                                                  Our global trace includes symbolic terms, such as keys, nonces, and
                                                                                                  messages. In concrete implementations, these terms are typically
3     LOCAL REASONING
                                                                                                  represented by (mutable) byte arrays. In order to relate the two, we
In the previous section, we have summarized how we can prove                                      use a concretization function 𝛾, which maps a term to its byte repre-
security properties based on a global trace of events. In this section,                           sentation. We use this function in specifications; in particular, we
2 Session corruption affects the entire short-term state of a participant instance, which
                                                                                                  have annotated library functions, e.g., for cryptographic operations,
might participate in multiple protocol sessions; a more fine-grained treatment of                 to relate the term representations of their inputs and outputs. E.g.,
individual sessions is possible, but omitted for simplicity.                                      a hash function that maps the byte array xa (representing, e.g., a
                                                                                              3
CCS ’23, November 26–30, 2023, Copenhagen, Denmark                                         Linard Arquint, Malte Schwerhoff, Vaibhav Mehta, and Peter Müller


                  M1.    𝐴 → 𝐵 : {⟨1, na, 𝐴⟩}pkB                              for all possible interactions between the participant instances and
                  M2.    𝐵 → 𝐴 : {⟨2, na, nb, 𝐵⟩}pkA                          the attacker. Moreover, since separation logic is modular, it verifies
                                                                              the implementation of each participant in isolation, independent
                  M3.    𝐴 → 𝐵 : {⟨3, nb⟩}pkB                                 of the other threads potentially running in the system (assuming
                                                                              only that their implementations are also verified). Consequently,
Figure 2: The NSL public key protocol, where na and nb are                    the verified properties hold for an arbitrary, unbounded number of
nonces, whose generation is omitted. {𝑚}pk and ⟨· · · ⟩ denote                participant instances.
public key encryption of plain text 𝑚 under the public key pk                     Separation logic achieves thread-modular reasoning by ensuring
and tupling, respectively. Creation and distribution of the                   that different threads operate on disjoint memory, which prevents
participants’ authentic keys is not part of the protocol.                     data races and eliminates interference between threads (see below
                                                                              for shared state). The proof rule for parallel composition (Par in
message) to the byte array ra (representing, e.g., a number) is spec-         Fig. 1) illustrates this approach. The threads 𝐶 1 and 𝐶 2 can be
ified by relating the corresponding terms: ∃𝑥, 𝑟 . xa = 𝛾 (𝑥) ∧ ra =          verified independently. They operate on the heap locations for
𝛾 (𝑟 ) ∧ 𝑟 = ℎ(𝑥), where ℎ is the symbolic hash operation on terms.           which they obtain permissions via their preconditions 𝑃1 and 𝑃2 ,
    Parsing a received message often requires showing that the                resp. Separation logic’s separating conjunction ∗ in the precondition
parsed byte array 𝑏 corresponds to a given term 𝑡: 𝑏 = 𝛾 (𝑡). Proving         of the parallel composition expresses that the permissions in 𝑃 1 and
this property generally requires that each byte array corresponds to          𝑃2 are disjoint. Note that we show the rule for a structured parallel
a unique term. However, this requirement is typically not satisfied           composition statement for simplicity; our technique also supports
in realistic implementations where, e.g., a byte array of length four         dynamic thread creation.
could store an integer or an ASCII-encoded string, which have dif-                Each thread needs to manipulate its own local data structures
ferent term representations. A possible solution [9, 34] is to enforce        and the global trace data structure that is shared among all threads.
a unique byte-level representation for every term (for instance,              To support mutable shared state, we can use any of the established
by preceding it with a tag). However, this is not possible when               verification techniques for concurrency reasoning. For concreteness,
targeting existing implementations with fixed message formats.                we use a global lock, which is associated with a lock invariant that
    Therefore, we adopt a less restrictive solution here. We use the          needs to be established when the lock is first created. This invariant
pattern requirement from Arquint et al. [20], which allows multiple           may then be assumed whenever the lock is acquired and must be
terms to have the same byte-level representation in general, but              proved to hold upon release. Proof rule With in Fig. 1 illustrates
requires a unique representation for the terms corresponding to pro-          this reasoning for a critical section 𝐶 that is protected by the lock 𝑟 .
tocol messages. This requirement allows a participant to uniquely             𝐼𝑟 is the invariant associated with lock 𝑟 , as specified by 𝑟 : 𝐼𝑟
determine the term for a parsed message. It ensures that the con-             in the proof context. Conceptually, a lock owns the permissions
cretization function 𝛾 is injective on the byte arrays received as            expressed in 𝐼𝑟 and temporarily lends these permissions to a thread
messages. The pattern requirement is satisfied by many protocols              on entering the critical section.
because they include message tags to distinguish the kinds of mes-                Since the global trace exists only for the purpose of verification,
sages, which in turn determines the unique relationship between a             we model it as ghost state and all operations on it as ghost opera-
byte array and a term. At the same time, it allows clashes among              tions; both are erased during compilation. Consequently, the lock
the representations of other terms, such as integers and strings.             protecting this ghost data structure can also be erased. Reasoning
    We illustrate the approach using the NSL public key protocol [3]          about ghost locks is completely analogous to standard locks (and
in Fig. 2. After receiving message M1, Bob parses it as an encrypted          supported by separation logic program verifiers). However, since a
triple. The specification of the parse operation ensures ∃na. 𝛾 (𝑚) =         ghost lock is erased during compilation, it does not ensure mutual
𝛾 ({1, na, 𝐴}pkB ). Since {1, na, 𝐴}pkB is a protocol message, we can         exclusion. Therefore, any non-ghost operation performed between
apply the pattern requirement to derive the required information              an acquire and a release must be atomic to ensure that erasing
about 𝑚: ∃na. 𝑚 = {1, na, 𝐴}pkB .                                             the ghost lock does not create thread interleavings that were not
                                                                              considered during verification.
3.3    Global Trace Encoding                                                      The trace data structure provides two operations: appending
As explained in Sec. 2, we use a global trace of events, verify in-           an event, and reading the current state of the global trace. Fig. 3
variants over this trace, and finally prove that the invariants imply         illustrates how participants and the attacker interact with the global
the intended security properties. For this approach to be sound,              trace. The lock invariant for the global trace is the trace invariant.
the global trace has to include all relevant events performed by the          By formulating this invariant in separation logic, it can express
protocol participants and the attacker, which we ensure as follows.           ownership of heap locations and other resources, which allows
   We model each participant instance potentially participating in            us to prove security properties that are out of reach for existing
a protocol session, and the attacker, as a thread in a concurrent sys-        invariant-based related work, as we will see in Sec. 4.1.
tem. Each thread maintain its own (mutable) local state, which may                Participants must record all protocol-relevant operations on the
contain short-term, session-specific data and long-term data that is          global trace. That is, to perform an operation such as sending a
shared by all instances of the participant. Multiple instances of the         message or creating a nonce, they must (1) acquire the ghost lock,
same protocol role are modeled as threads that execute the same               (2) perform the operation, (3) append the corresponding event to
code. Soundness of separation logic ensures that any verified prop-           the trace, and (4) release the ghost lock (and at this point prove
erty holds for all possible interleavings between the threads, that is,       that the trace invariant is preserved). For each relevant operation,
                                                                          4
                                                                                                                          final
                                                                                                                          version

A Generic Methodology for the Modular Verification of Security Protocol Implementations (extended version)         CCS ’23, November 26–30, 2023, Copenhagen, Denmark


                            </>                                                 </>
  Snap.         local
                        Alice1                                             Bob
                                                                                           words, the invariant may state only those properties that are valid
                 inv                 I/O                          I/O
                                                                                           under our attacker model, a property we call attacker completeness
                                                          </>                              (sometimes referred to as attacker typability).
                                                                         local inv
                            </>
                                            Network API                                       Participant and session corruption are two of the possible at-
  Snap.         local                I/O
                 inv    Alice2                                            Snap.            tacker operations in step 2 above. In both cases, step 3 adds all
                                                                                           symbolic terms possibly present in the participant’s (long-term or
                                                    I/O         append                     short-term) state to the attacker knowledge, and step 4 checks that
                           append
                                                                                           the invariant about the attacker knowledge is maintained.
       prefix                                Attacker                      prefix

                                                                                           3.4    Local Snapshots
                                                    append
                                                                                           To prove that a protocol-relevant operation preserves the trace in-
                                                                             ...           variant, we frequently need to relate the arguments of the operation
                        Global Trace ∈ Trace Inv                                           to earlier events on the trace. For example, when sending the first
                                                                                           message of the NSL protocol (Fig. 2), Alice has to show that the
                                      ⟹




                                                                                           message invariant holds. The message invariant specifies that na is
                                     Security Properties                                   a nonce, i.e., requires a prior CreateNonce(na) event on the trace.
                                                                                               Discharging such proof obligations requires that participants
Figure 3: An overview of the main components of a proto-                                   retain information about their prior operations on the global trace.
col execution in our methodology. The blue boxes are com-                                  Since the global trace is a shared data structure that may grow
ponents of the protocol implementation; green boxes de-                                    between any two accesses, participants may soundly hold on to
note ghost structures that are used for verification. Blue and                             those facts that are stable under extensions of the trace. For instance,
green arrows denote actual and ghost method calls, resp. The                               if a CreateNonce(na) is present on the trace at some program point,
red dashed arrows denote invariants relating different data                                it will also be present in all future versions of the trace.
structures. Participants and the attacker send and receive                                     We represent the stable information of a participant by main-
messages by interacting with the network. The attacker can                                 taining in each participant a local snapshot (i.e., a local copy) of the
perform additional I/O operations such as instructing the                                  global trace (see Fig. 3). Since the global trace may evolve by actions
network to drop or modify messages. All protocol-relevant                                  of other participants and the attacker, the local snapshot of a partici-
operations (including I/O operations) are recorded on a global                             pant is generally a prefix of the global trace. Whenever a participant
trace. We verify (global) security properties by proving modu-                             performs a protocol-relevant operation, we update its local snap-
larly that each protocol implementation (e.g., two and one im-                             shot to the current global trace. The trace invariant ensures that the
plementations of Alice’s and Bob’s role, resp.) and the at-                                local snapshots of all participants are prefixes of the global trace,
tacker maintain a trace invariant, and that the trace invariant                            and that these updates are the only modifications of local snapshots.
implies the security properties. We enable the verification                                    With this design, local snapshots need to be owned by the par-
of participants by relating participant-local state with the                               ticipants (to ensure their values are retained across operations of
trace via local ghost state that contains a participant’s local                            other threads), and they must also be owned by the ghost lock (to
snapshot, i.e., its last observed version of the trace.                                    allow the lock invariant to relate the local snapshots to the global
                                                                                           trace). To express this notion of shared ownership, we use fractional
we provide a library wrapper (see Sec. 5 for details) that performs                        permissions [35], which are supported by many separation logics.
these four steps3 . Preconditions on the library functions ensure                          Conceptually, fractional permissions allow one to split a permis-
that the performed operation indeed preserves the trace invariant.                         sion into several fractions; a non-zero fraction permits read access,
Since the trace invariant (and, hence, the preconditions) contain                          whereas the full permission is required for write access. Separating
protocol-specific properties, our library is parametric in the invari-                     conjunction adds the fractions in both conjuncts and yields false if
ant (cf. Sec. 5). To ensure that all relevant operations are recorded                      the sum for any location exceeds a full permission.
on the trace, it then suffices to perform a simple syntactic check                             We split the permission to a local snapshot into two halves: One
that relevant operations are performed only via the wrapper library.                       half is part of the trace invariant and lets it express properties of the
   The attacker is handled similarly. We model it as code that (1) ac-                     local snapshot. The other half remains with the corresponding par-
quires the ghost lock, (2) determines which operations the attacker                        ticipant and enables the participant to retain information about the
could potentially perform based on its current attacker knowledge                          global trace. After acquiring the ghost lock, a participant temporar-
(which is recorded on the trace), (3) non-deterministically chooses                        ily obtains exclusive permission to its local snapshot by adding the
any of these operations and appends the corresponding event to the                         half it holds with the half from the trace invariant (through the
trace, and (4) releases the ghost lock (and at this point proves that                      precondition 𝑃 ∗ 𝐼𝑟 in rule With in Fig. 1) and can, thus, update the
the trace invariant is preserved). Verifying this code ensures that all                    local snapshot.
possible attacker operations preserve the trace invariant. In other                            By letting each participant retain a non-zero permission to its
                                                                                           snapshot, we can rule out interference from other threads and,
3 To avoid any runtime overhead, calls to this wrapper library could be inlined (and       thus, use standard sequential reasoning to relate the content of the
ghost code is erased in any case).                                                         local snapshot to the concrete data structures maintained by the
                                                                                       5
    CCS ’23, November 26–30, 2023, Copenhagen, Denmark                                               Linard Arquint, Malte Schwerhoff, Vaibhav Mehta, and Peter Müller


1       na /*@ , naT @ */ := CreateNonce ( /* @ s @ */ )                          1     let commit = FinishA (A ,B , na , nb ) in
2       // @ assert s. NonceOccurs ( naT )                                        2     t . Occurs ( commit ) =⇒
                                                                                  3     let prefix , i = t . GetPrefix ( commit ) in
                                                                                  4     ( prefix . Occurs ( Respond (A ,B , na , nb ) ) &&
    Figure 4: Excerpt from a NSL implementation for Alice creat-                  5         !( ∃ A ′ ,B ′ , nb ′ ,i ′ . i != i ′ &&
    ing a nonce and demonstrating how to relate local state with                  6            t . OccursAt ( FinishA ( A ′ ,B ′ ,na , nb ′ ) ,i ′ ) )
                                                                                  7     ) || prefix . IsCorrupted ({ A , B })
    the global trace. //@ and /*@ ... @*/ mark ghost code that is
    used for verification only. We omit the nonce’s secrecy label
    (Sec. 4.2) for simplicity.                                                        Figure 5: Non-injective (white background) and injective (all
                                                                                      lines) agreement from Alice’s perspective with Bob on the
                                                                                      nonces na and nb. t.Occurs(e) yields whether event e occurs
    participant (via local invariants) and to prove the presence of an                on trace t; t.GetPrefix(e) returns t’s prefix up to and includ-
    event on the snapshot. The example in Fig. 4 illustrates that. Line 1             ing the most recent occurrence of e, and the index of that oc-
    invokes the library function CreateNonce. Its regular result na is                currence (i.e., the length of prefix minus 1). t.OccursAt(e,i)
    the generated nonce; the additional ghost result naT is the corre-                expresses that event e occurs at index i on trace t.
    sponding term. CreateNonce takes the caller’s local snapshot s as
    ghost argument, which allows the function to update the snapshot
                                                                                  1     match ev {
    and to express in its postcondition the existence of the create-nonce         2       case FinishA (A , B , na , nb ) :
    event on the updated local snapshot. This postcondition allows the            3         UniWit ( FinishA , na ) &&
    caller to prove the assertion in line 2, without having to consider           4         ( prefix . Occurs ( Respond (A , B , na , nb ) ) ||
                                                                                  5            prefix . IsCorrupted ({ A , B }) )
    any interleaving operations by other participants or the attacker.            6       ...
                                                                                  7     }
    4     PROVING SECURITY PROPERTIES
    In this section, we show how to define a trace invariant that lets                Figure 6: A simplified fragment of the trace invariant for
    us verify two important security properties, authentication and                   NSL-specific events. This invariant is universally quantified
    secrecy. Authentication means that two protocol participants are                  over the events ev occurring on the trace; prefix is the trace
    indeed communicating with each other and (depending on the                        prefix up to event ev. The invariant expresses that when-
    particular authentication property) agree on some common values.                  ever a FinishA event occurs on the trace, a Respond event with
    Secrecy holds if confidential data remains unknown to the attacker.               matching arguments must previously occur, unless one of
    While we focus here on the proof techniques for these two standard                the participants has been corrupted. The highlighted line in-
    properties, our methodology is also applicable to more complex                    cludes a separation logic resource to express that the FinishA
    properties such as forward secrecy, as demonstrated in Sec. 6.3.                  event is unique w.r.t. to the nonce na, which allows us to
                                                                                      prove injective agreement. The conjunction && is interpreted
                                                                                      as separation logic’s separating conjunction *.
    4.1     Authentication
    To prove authentication, we use protocol-specific events to record
    additional information beyond the exchanged messages, so that                     trace (line 2) then either a Respond event with matching arguments
    authentication properties can be expressed in a familiar way: as                  occurs earlier on the trace (line 4) or one of the participants has
    correspondence between these events. In this subsection, we show                  been corrupted before an agreement was reached (line 7).
    how to use trace invariants expressed in separation logic to prove                   To prove agreement for NSL, we include the NSL-specific prop-
    two strong and common authentication properties: non-injective                    erty from Fig. 6 (ignore line 3 for now) into the trace invariant. It
    and injective agreement.                                                          states that for every FinishA event, a corresponding Respond event
       We illustrate our methodology using the NSL example from Fig. 2.               occurred prior on the trace, or one of the participants has been
    We prove authentication using four protocol-specific events: Before               corrupted. Maintaining this invariant requires us to show the oc-
    sending the first message, Alice creates event Initiate(Alice, Bob, na)           currence of a suitable Respond event (or of corruption) when Alice
    to record that she wants to communicate with Bob, and use the                     creates the FinishA event.
    nonce na in the current protocol session. After receiving the first                  We discharge this proof obligation by extending the trace in-
    and before sending the second message, Bob in turn creates event                  variant with a message invariant for NSL’s second message, which
    Respond (Alice, Bob, na, nb), indicating the communication partners               requires that the Respond event occurs on the trace or the message
    and used nonces. Finally, the events FinishA and FinishB, with the                comes from the attacker. Hence, an implementation for Bob has to
    same parameters as Respond, indicate successful completion of the                 create a Respond event before sending the second message. When
    protocol (i.e., runtime checks such as nonce comparisons succeeded)               Alice receives the message, she may assume its message invariant
    for Alice and Bob, resp. We focus on Alice’s perspective in the                   (as part of the trace invariant). Since her local snapshot gets updated
    following. We prove authentication for Bob’s perspective in Sec. 6.3,             upon the receive-operation, the received message is recorded on the
    where we also discuss authentication properties for WireGuard.                    local snapshot and the message invariant becomes part of Alice’s
    Non-injective Agreement. The fact that Alice agrees with Bob                      stable knowledge. So when Alice adds the FinishA event to the trace,
    on the nonces na and nb, known as non-injective agreement [36], is                she knows that either the Respond event occurs on the trace, or the
    specified in Fig. 5 (ignore the conjunct highlighted in blue for now).            second NSL message comes from the attacker. In the latter case,
    This trace-based property states that if a FinishA event occurs on the            Alice can derive that corruption must have occurred because the
                                                                              6
A Generic Methodology for the Modular Verification of Security Protocol Implementations (extended version)       CCS ’23, November 26–30, 2023, Copenhagen, Denmark


attacker was able to construct a message containing the nonce na,                        linearity of the resource, any attempt to append another FinishA
which is accessible only to Alice and Bob (unless corrupted).                            event with na would fail to verify because the required witness
   Once we established the trace invariant, it remains to show                           cannot be provided a second time, which would be necessary to
that for all traces, the invariant from Fig. 6 implies non-injective                     preserve the trace invariant.
agreement (Fig. 5). This proof is a standard entailment check, which                        Consequently, the invariant from Fig. 6 implies that the FinishA
is performed automatically by program verifiers.                                         event with na is unique, which allows a standard separation logic
                                                                                         verifier to prove the highlighted conjunct in the definition of injec-
Injective Agreement. The stronger property injective agreement                           tive agreement (Fig. 5).
holds only for implementations that detect if the attacker replays                          Our discussion shows how the combination of a global trace and
messages from other protocol sessions. If successful, such a replay                      local snapshots allows us to prove authentication modularly, and
attack could trick participants into reusing outdated nonces (in gen-                    how we can leverage the expressive power of separation logic to
eral, key material), thereby weakening security. Proving injective                       specify a trace invariant that lets us prove injective agreement.
agreement modularly is challenging; to the best of our knowledge,
we present here the first invariant-based verification technique for                     4.2     Secrecy
injective agreement in protocol implementations (see also Sec. 8).
                                                                                         Secrecy of a term s, e.g., a key or a nonce, states that the attacker
    The highlighted conjunct in Fig. 5 strengthens non-injective to
                                                                                         does not learn this term except when corrupting one of the protocol
injective agreement by mandating that there is no second FinishA
                                                                                         participants that know the term. We can express secrecy as a prop-
event on the trace with the same nonce na. The uniqueness of the
                                                                                         erty of the global trace because we can extract both the attacker
event/nonce-pair enforces a one-to-one correspondence between
                                                                                         knowledge and corruption events from the trace.
Respond and FinishA events and, thus, excludes replay attacks.
                                                                                            Instead of directly reasoning about the concrete attacker knowl-
    To prove injective agreement, we strengthen our trace invariant
                                                                                         edge, we follow Bhargavan et al. [9, 37] by over-approximating the
to imply this property. We could in principle include a conjunct
                                                                                         concrete attacker knowledge to classes of terms that the attacker
that specifies uniqueness by quantifying over the indexes into the
                                                                                         (possibly) knows. This over-approximation enables modular rea-
trace. However, such an invariant would be difficult to maintain
                                                                                         soning about secrecy: we impose proof obligations that prevent
modularly. The necessary proof obligation for adding a FinishA
                                                                                         secrets from being leaked to the attacker by checking for every
event would require that no such event with the same first nonce
                                                                                         send operation that the sent message belongs to a class already
already exists on the trace. However, each participant has only
                                                                                         known to the attacker. For instance, if a participant tried to send
partial information about the trace stored in its local snapshot. So
                                                                                         a (unencrypted) secret term over the network, the send operation
even if we proved the absence of an event on the local snapshot,
                                                                                         would be rejected by the verifier. Consequently, sending a message
we could not conclude its absence on the trace, such that the proof
                                                                                         does not change the over-approximated attacker knowledge. This
obligation cannot be discharged.
                                                                                         knowledge is extended only when the attacker corrupts a partici-
    To obtain a modular verification technique for injective agree-
                                                                                         pant or session. In this case, we add the class of terms readable by
ment, we leverage separation logic’s permissions to encode arbi-
                                                                                         the corrupted participant or session to the knowledge.
trary linear resources (non-duplicable facts). Due to the meaning of
                                                                                            We classify terms based on their allowed recipients by assigning
separating conjunction, 𝑝 ↦→ _ ★ 𝑝 ↦→ _ is equivalent to false (be-
                                                                                         them a secrecy label. Secrecy labels range from public (i.e., everyone
cause the permissions of the two conjuncts are not disjoint). That
                                                                                         including the attacker) over a set of participants to a set of particular
is, the points-to assertion 𝑝 ↦→ _ is a non-duplicable (i.e., unique)
                                                                                         protocol sessions. The latter is useful to classify ephemeral private
resource. We can use this fact to model the uniqueness of an event
                                                                                         keys, e.g., in our WireGuard case study, because only a participant
by representing the event as a separation logic permission. We use
                                                                                         running a particular protocol session is allowed to read these keys.
this mechanism as follows.
                                                                                            By proactively enforcing secrecy labels, we ensure that the (con-
    Conceptually, we tie event uniqueness to nonces because nonces
                                                                                         crete) attacker knowledge may contain only public terms and terms
are, by assumption of perfect cryptography, unique. When a protocol-
                                                                                         whose secrecy label contains a participant or protocol session that
specific event is declared, it can be specified as unique w.r.t. a spe-
                                                                                         is allowed to read the term and that has been corrupted in the past.
cific nonce parameter. E.g., in NSL, event FinishA is unique w.r.t. its
                                                                                         We prove this property once and for all as part of our reusable
third parameter na. Subsequently, when a nonce is generated via
                                                                                         verification library (cf. Sec. 5).
a call to our verification library, a program annotation states for
which events this nonce will be used (e.g., FinishA). The library call
returns not only the fresh nonce (na), but also a linear resource for                    5     REUSABLE VERIFICATION LIBRARY
each indicated event type (technical details follow in Sec. 5).                          We implement our methodology as a reusable verification library,
    This resource—called an event’s uniqueness witness—then needs                        which significantly reduces the verification effort per protocol: the
to be given up when the corresponding event is appended to the                           library encapsulates the global trace and provides a convenient API
trace. That is, ownership of the resource is transferred from the par-                   for common network and cryptographic operations that automates
ticipant to the ghost lock by conjoining the resource to the trace in-                   trace updates. In addition, the library provides various lemmas, such
variant. E.g., for NSL, Alice obtains the witness UniWit (FinishA, na)                   as attacker completeness (Sec. 2), which are proved once and hold
when creating nonce na. This witness is transferred to the trace                         for all protocols. To enable verification of a wide range of protocols,
invariant when she appends the event FinishA(_, _, na, _) to the                         the global trace is parametric in the events it records, and the trace
trace, as expressed by the highlighted conjunct in Fig. 6. Due to the                    invariant is parametric to account for protocol-specific properties.
                                                                                    7
CCS ’23, November 26–30, 2023, Copenhagen, Denmark                                                Linard Arquint, Malte Schwerhoff, Vaibhav Mehta, and Peter Müller


                          NSL                                                           The library also provides a convenient API for common network
                                                                                     I/O and cryptographic operations: each function performs the cor-
                              Alice          Bob                                     responding concrete operation (e.g., sending a message or creating
                                                                                     a nonce) and also adds the corresponding event to the trace. Suit-
                                                                                     able preconditions ensure that the operation preserves the trace
              RVL                                                                    invariant; they lead to proof obligations for clients using the API.
                                                                                     Clients typically discharge these with the help of stable knowledge
                       I/O                Crypto                                     about the trace, which is recorded in their local snapshots.




                                                     Lemmas, incl. Att. Compl.
                                                                                        In terms of cryptographic operations, our library currently offers
                 CDS
                                                                                     asymmetric encryption, authenticated encryption with associated
                              Invariant                                              data (AEAD), signatures, and modular exponentiation, but can eas-
                                                                                     ily be extended by additional cryptographic operations. As a refer-
                     Trace            Snapshots                                      ence, adding the latter two features and proving the corresponding
                                                                                     lemmas took about two person days.
                     Events            Terms                                            Note that almost the entire library consists of ghost code that
                                                                                     is used for verification, but will be erased by the compiler. The
                                                                                     only non-ghost operations are the calls to the underlying I/O and
Figure 7: Structure of our reusable verification library (RVL).                      crypto libraries. This has two important consequences. First, these
The library provides implementations for the abstractions                            calls can be inlined in the participant implementation, such that
used in our methodology: terms, events, the global trace, and                        the entire library can be removed from the executable program and
local snapshots. Both the trace and all local snapshots are gov-                     does not cause any runtime overhead. Second, existing protocol
erned by the trace invariant. The trace is encapsulated inside                       implementations do not have to be modified to use the library. The
a concurrent data structure (CDS) that permits shared access.                        library provides a convenient way to systematically annotate an
The APIs for I/O and cryptographic operations apply these                            implementation with ghost code and proof obligations, but other
operations and also register the corresponding events on the                         forms of annotations are also possible.
trace. The RVL also provides several lemmas that have been
proved for all protocols, e.g., attacker completeness. Many
components of the library are parametric to accommodate                              Parametricity. As we discussed earlier, some events and aspects of
protocol-specific events and invariants (and the correspond-                         the trace invariant (and consequently the preconditions of the I/O
ing preconditions for the I/O and crypto API). We indicate                           and crypto API) are protocol-specific. To capture them, we designed
parametric components using a tab symbol near the top of                             our library to be parametric, such that clients using the library can
the box. The parameters are supplied for a concrete protocol                         instantiate it for a given protocol.
(here, NSL), as indicated by the tab at the bottom of the box.                           Despite being parametric, our library nonetheless provides lem-
                                                                                     mas that are proven once and for all protocols, in particular, attacker
                                                                                     completeness (Sec. 2) and the secrecy lemma (Sec. 4.2). Attacker com-
                                                                                     pleteness can be proved once and for all because the library is not
   To demonstrate that our methodology is widely applicable, we                      parametric in the kinds of term abstractions it provides. Secrecy
developed a library for the Go verifier Gobra [22], and one for the C                directly follows from the protocol-independent parts of the trace
verifier VeriFast [21]. Both library implementations are available in                invariant, which enforce for all protocols that implementations do
our open-source artifact [31]. In this section, we give an overview                  not leak secrets to the attacker, i.e., messages have to be public.
of the library and highlight some of its technical solutions.                        The library provides also several utility lemmas (e.g., that event
                                                                                     existence is a stable trace property) that can be used when verifying
5.1    Overview                                                                      a participant implementation.
In the following, we describe the library’s structure and compo-                         Fig. 8 shows a small excerpt of our trace invariant. The parameter
nents, explain how the library can be instantiated for different                     P provides protocol-specific events and invariants. Besides various
protocols, and provide data on its size and verification time.                       properties of the entire trace (not shown in the figure), the trace
                                                                                     invariant also includes event-specific invariants. We show here
Components. Fig. 7 illustrates the structure of our library (lower                   the invariants for Send events and protocol-specific events. A Send
box) and a protocol implementation that uses it (upper box). The                     event requires the message invariant, which itself can be param-
library provides the abstractions introduced in Sec. 3: terms and                    eterized by library clients. We prove that the generic part of the
events abstract over concrete data structures (e.g., byte arrays) and                message invariant is weak enough to be preserved by the attacker;
participant operations, respectively. Events are recorded on the                     it states, in particular, that the terms occurring in the message do
global trace, whose content is constrained by the trace invariant.                   not leak secrets. The protocol-specific part of the message invariant
The concurrent data structure (CDS) fully encapsulates the trace, to                 may constrain only encrypted data and must allow the possibility
govern shared access and maintain the invariant. Local snapshots                     that the encrypted data was fabricated by the attacker out of terms
are prefixes of the global trace, which also satisfy the trace invariant,            in the attacker knowledge. This ensures that it is maintained by
but are owned locally by the protocol participants.                                  all attacker actions. For a protocol-specific event, the invariant is
                                                                                 8
     A Generic Methodology for the Modular Verification of Security Protocol Implementations (extended version)      CCS ’23, November 26–30, 2023, Copenhagen, Denmark


 1     pred TraceInv [P ]( t : Trace ) {                                                      amount of ghost code. It verifies in 1 second (VeriFast is usually
 2       foreach e: Entry of t :
 3         let pre = ... in // trace prefix up to e
                                                                                              faster than Gobra, but provides less automation). We have measured
 4         match e {                                                                          the verification times by averaging over 30 runs on a 2020 Apple
 5           case Send ( msg ) :                                                              Mac mini with M1 processor and macOS Ventura 13.0.1. Since the
 6             MsgInv [P ]( msg , pre )
 7           case PEvent ( pe ) :                                                             library is verified once for all protocols, this effort does not have to
 8             P :: PEventInv ( pe , pre )                                                    be repeated when verifying a concrete protocol implementation.
 9           ...
10         }
11     }                                                                                      5.2     Technical Solutions
                                                                                              In the following, we summarize the features of a verification tech-
     Figure 8: Excerpt of the parametric trace invariant, defined                             nique and tool required to implement the main abstractions (e.g.,
     via pattern matching over individual trace entries. All cases                            terms, events, global traces) provided by our library.
     may refer to earlier events on the trace via the prefix param-                           Custom Mathematical Theories. Verification techniques fre-
     eter pre. The case for a Send event enforces the message in-                             quently represent information as values of mathematical theories,
     variant, which is partly defined by the library, but itself para-                        such as sets, tuples, sequences, etc. In contrast to the corresponding
     metric. A PEvent represents any protocol-specific event pe.                              data types of a programming language, these values are immutable
     The corresponding case of the trace invariant comes entirely                             and their operations have a direct representation in the verification
     from the protocol parameter P.                                                           logic, which simplifies reasoning.
                                                                                                 We use mathematical theories to represent the abstractions we
               Library          LOC      LOS     Verification time [s]                        use in specifications and ghost code: events, the global trace, secrecy
               Go/Gobra          83     6,932            126.1                                labels, and terms with equational theories. Conceptually, events
               C/VeriFast       343     3,837             0.8                                 form an algebraic data type (ADT), as does the global trace (a func-
                                                                                              tional list). Labels and terms are also algebraic structures, but with
     Figure 9: Lines of code (LOC) and lines of specification (LOS)                           additional properties (e.g., labels have a commutative join operator).
     (incl. ghost code) for the library code, together with the aver-                            The Gobra implementation of the library represents all these
     age verification times in Gobra and VeriFast.                                            structures as uninterpreted functions with appropriate axioms (anal-
                                                                                              ogous to how custom theories are encoded to SMT solvers). E.g., for
     supplied entirely by the parameter P. In the following, we explain                       the ADT of events, we define axioms that ADT constructors are in-
     how this parameter is represented in our library implementations.                        jective in their arguments, and that different constructors produce
        In the Go implementation of the library, we achieve parametric-                       different events. For terms, we define additional axioms to encode
                                                                                                                                             𝑦       𝑥
     ity by using Go interfaces. In particular, the generic protocol interface                cryptographic equational theories, e.g., 𝑔𝑥 = 𝑔 𝑦 , where 𝑔𝑥 de-
     declares mathematical functions (e.g., isUnique to indicate that an                      notes Diffie-Hellman exponentiation with generator 𝑔. VeriFast
     event is unique), separation logic predicates (e.g., protocol-specific                   supports ADTs natively, which we use to represent events and the
     event invariants), and lemmas. Clients may then supply different                         global trace. For labels and terms, we again use uninterpreted func-
     implementations of this interface with different definitions for these                   tions and axioms (“auto-lemmas”) to express equational theories.
     functions, predicates, and lemmas. Gobra checks via suitable proof                       Linear Resources. Our novel support for proving injective agree-
     obligations that any concrete implementation satisfies key proper-                       ment (cf. Sec. 4) requires reasoning about the uniqueness of certain
     ties specified in the interface (e.g., that protocol-specific invariants                 protocol-specific events. For this purpose, we introduce (ghost)
     provide uniqueness witness resources for unique events). These                           memory locations and use separation logic’s (exclusive) permis-
     properties can thus soundly be assumed while verifying the para-                         sions to these locations as linear resources. Separation logic pred-
     metric library. Analogously, parametricity w.r.t. events is enabled                      icates [38] allow us to construct linear resources with arbitrary
     by declaring an Event interface that protocol-specific events extend.                    parameters by mapping the parameter tuples injectively to a heap
        In VeriFast, we use its generic types (e.g., for events), abstract                    location. We use such predicates to represent the uniqueness wit-
     mathematical functions (e.g., isUnique), and abstract lemmas (e.g.,                      nesses from Sec. 4.
     that the event invariant is stable) to achieve parametricity and verify                  Concurrency Reasoning. As discussed in Sec. 3.3, we model the
     the library once for all protocols. When verifying implementations                       global trace as a concurrent data structure. Our approach is com-
     of a particular protocol, these abstract functions and lemmas are                        patible with any verification technique that is able to reason about
     concretized by providing function and lemma definitions via an                           shared accesses to such a data structure and to maintain an invari-
     automated syntactic transformation. We prove that these definitions                      ant over it. Moreover, to encode local snapshots (cf. Sec. 3.4), we
     are not present while verifying the library, that is, we indeed verify                   require support for reasoning about properties that are stable under
     the parametric version of the library, not a concrete instantiation.                     concurrency, which are offered by separation logic verifiers.
     Statistics. Fig. 9 shows the size and verification time for the two                         We model the global trace as a data structure that is protected
     verified implementations of our library. As explained above, the                         by a ghost lock. Neither Gobra nor VeriFast support ghost locks
     library consists mostly of ghost code; only around 1% is executable                      directly, but both offer standard locks. Reasoning about ghost locks
     code. All methods and lemmas together are verified in ca. 2 minutes.                     and standard locks is almost identical, with one exception: Any
     The library for VeriFast is currently less complete than the one for                     non-ghost operations performed between acquiring and releasing
     Gobra, and lacks several useful lemmas, which explains the smaller                       a ghost lock must be atomic (because the lock will be erased by the
                                                                                         9
     CCS ’23, November 26–30, 2023, Copenhagen, Denmark                                          Linard Arquint, Malte Schwerhoff, Vaibhav Mehta, and Peter Müller


1        struct Alice {                                                                             M1.    𝐴 → 𝐵 : 𝑔𝑥
2          SkA : byte []
3          PkB : byte []                                                                            M2.    𝐵 → 𝐴 : {|⟨0, 𝐵, 𝐴, 𝑔𝑥 , 𝑔 𝑦 ⟩|}skB
4          Na : byte []
5          Nb : byte []                                                                             M3.    𝐴 → 𝐵 : {|⟨1, 𝐴, 𝐵, 𝑔 𝑦 , 𝑔𝑥 ⟩|}skA
6          /* @ Step : uint @ */
7          ...
8        }                                                                          Figure 11: The signed DH key exchange protocol, where 𝑔𝑥
 9
                                                                                    and 𝑔 𝑦 are DH public keys and {|𝑚|}sk denotes cryptographi-
10       /* @ pred LocalInvariant ( a : Alice ) {                                   cally signing a payload 𝑚 with a secret key 𝑠𝑘.
11          ∃ naT , nbT .
12          ... && // memory omitted
13          (a. Step == 2 == >
14             UniWit ( FinishA , naT ) ) &&
15          (a. Step >= 2 == >
16             𝛾 ( naT ) == a. Na &&
17             a. Snap () . NonceOccurs ( naT ) ) &&
18          (a. Step >= 3 == >
19             𝛾 ( nbT ) == a. Nb &&                                                track of via the Step field. E.g., Alice is in Step 2 after creating the
20             a. Snap () . Occurs ( FinishI (A , B , naT , nbT ) ) )
21       } @ */                                                                     nonce naT and sending the first message. In this case, the invari-
                                                                                    ant includes the uniqueness witness (line 14), which allows Alice
     Figure 10: The struct used for Alice’s local state in the Go im-               to create the FinishI event in a later protocol step. The invariant
     plementation of NSL, and an excerpt from the local invariant                   relates the concrete nonce field Na to its term representation naT
     that relates this state to Alice’s local snapshot and, thereby,                using the concretization function 𝛾 (line 16). This term is used in
     to the global trace. The Step field is a ghost field that is used              the events on the global trace. In particular, the CreateNonce event
     to track Alice’s progress in the protocol.                                     for naT must occur on Alice’s local snapshot a.Snap() (line 17)
                                                                                    and, thus, on the global trace. Once Alice’s protocol run has reached
                                                                                    the final Step 3, it adds the FinishI event to the trace. The invari-
     compiler, so it does not actually provide mutual exclusion). This              ant reflects this by stating that the event is on the local snapshot
     property is satisfied in our library.                                          (line 20). Knowledge about FinishI ’s existence on the trace entails
                                                                                    (via the trace invariant) properties about the Respond event cre-
     6     CASE STUDIES                                                             ated by Bob (recall Fig. 6). This knowledge, together with FinishI ’s
     We applied our methodology to Go implementations of the NSL                    uniqueness witness (now stored in the trace invariant), allows us
     public key protocol, signed Diffie-Hellman (DH) key exchange, and              to prove injective agreement with Bob as explained in Sec. 4.1.
     the WireGuard VPN protocol, and prove strong security properties.                  We prove for all participant implementations that they achieve
     We also verified a C implementation of NSL, and obtained the same              (at the end of a protocol execution) injective agreement on, and
     security properties as for the Go implementation. Our case stud-               secrecy for, both nonces na and nb. Additionally, we verify initial-
     ies (included in our artifact [31]) thus demonstrate the portability           ization code that creates an empty trace, generates public/private
     of our methodology across different protocols, programming lan-                key pairs for the participants, and spawns two participant instances
     guages, and verifiers, and its scalability to realistic, interoperable         as Go routines (similar to threads) to demonstrate that key distribu-
     implementations. In this section, we first summarize each of the               tion (although not part of the protocol) can be modeled using our
     case studies and then discuss our experiences.                                 methodology.

     6.1      Needham-Schroeder-Lowe
     We used Gobra to verify a Go implementation of the initiator and re-           6.2    Signed Diffie-Hellman
     sponder roles for the NSL protocol (cf. Fig. 2), and likewise VeriFast         In the signed DH key exchange (cf. Fig. 11), Alice and Bob each
     for a C implementation thereof. We implemented the core of the                 generate a DH secret key 𝑥 and 𝑦, respectively. By transmitting the
     protocol as one method per participant; we also verified an alterna-           corresponding (signed) DH public keys 𝑔𝑥 and 𝑔 𝑦 , they agree on
                                                                                                       𝑦
     tive Go implementation of the initiator that contains one method               the shared key 𝑔𝑥 after a successful protocol run.
     per message to demonstrate that verification is not sensitive to the              We prove secrecy for, and injective agreement on, the shared key.
     code structure. Both protocol roles store their program state locally          The proof is similar to the proof for NSL, which allowed us to reuse
     and use an invariant to relate the local state via the term abstraction        substantial parts. One noticable difference is that proving that both
     to their local snapshot and, thereby, to the global trace.                     participants derive the same shared key requires the equational
        Fig. 10 illustrates the interplay between the local state and the           theory for Diffie-Hellman exponentiation. Our reusable verifica-
     local snapshot for the initiator, Alice. Alice manages her program             tion library provides such custom theories, as discussed in Sec. 5.2.
     state in a struct Alice. The local invariant in lines 10–21 relates            Another difference is that the nonces 𝑥 and 𝑦 are not directly part
     Alice’s local state to her local snapshot (and, thus, indirectly to            of the protocol messages (in contrast to 𝑛𝑎 and 𝑛𝑏 in NSL), but are
     the global trace). This invariant expresses ownership of the heap              existentially quantified in the message invariants. A participant
     locations for the struct fields, which is omitted in the figure. More          instance can determine the values of these existentially-quantified
     importantly, it specifies properties about the struct fields depending         variables after receiving a protocol message, by connecting the
     on Alice’s progress within the protocol execution, which we keep               message invariant to its own Diffie-Hellman secret key.
                                                                               10
A Generic Methodology for the Modular Verification of Security Protocol Implementations (extended version)          CCS ’23, November 26–30, 2023, Copenhagen, Denmark


6.3     WireGuard                                                                       1     ! t . AttackerKnows ( s ) ||
                                                                                        2         t . GetHs ( ASess , PSess ) . IsCorrupted ({ A,   P }) ||
As our main case study, we have picked the WireGuard VPN proto-
                                                                                        3         t . IsSessionCorrupted ({ ASess , PSess })
col as a real-world protocol achieving even stronger security prop-
erties than NSL. WireGuard is a modern, open-source, and cross-
                                                                                            Figure 12: Strong (without highlighted part) and weak for-
platform VPN that uses state-of-the-art cryptography and is part
                                                                                            ward secrecy (entire property) for a session key s on trace t.
of the Linux kernel. The WireGuard protocol, which performs an
                                                                                            A and P identify the actor and peer that derive the key
authenticated key exchange, has been analyzed rigorously [39, 40].
                                                                                            in their protocol sessions ASess and PSess, respectively.
It consists of a handshake and transport phase. During the hand-
                                                                                            t.GetHs(ASess, PSess) returns a prefix of t up to and in-
shake phase, the protocol participants agree on two session keys kIR
                                                                                            cluding the corresponding handshake’s completion from the
and kRI , one per direction, that are used to symmetrically encrypt
                                                                                            actor’s perspective. The key is protected against (future) par-
VPN packets in the transport phase.
                                                                                            ticipant corruption after the handshake’s completion.
Implementation. We used the existing Go implementation from
Arquint et al. [41], whose memory safety proof we reused. Thanks                            Security Properties. Since the session keys are based on ephemeral
to our reusable verification library’s parametric design, instantiat-                       as well as long-term key material that is contributed by both pro-
ing our library with the concrete networking library used by the                            tocol participants, WireGuard achieves strong security properties.
WireGuard implementation was straightforward and only required                              In particular, we prove forward secrecy and injective agreement,
annotating cryptographic functions with suitable postconditions.                            both with actor key compromise (AKC) security. While WireGuard
   Arquint et al.’s implementation is a subset of WireGuard’s official                      optionally incorporates a pre-shared symmetric key into the hand-
Go implementation. It omits advanced VPN features such as DDoS                              shake to increase security, we prove all security properties in this
protection, session key renewal, and support for multiple concur-                           section without considering this pre-shared key, i.e., we treat the
rent VPN connections. Moreover, their implementation reduces                                pre-shared key as a term known to the attacker. In the following,
concurrency (which we partly re-introduced, as we discuss below),                           we call the initiator actor and the responder peer when proving
and replaces a message buffer pool by single-use buffers. Our tech-                         a property from the initiator’s perspective, and vice versa for the
nique could handle the removed features with additional effort that                         responder’s perspective.
is mostly orthogonal to our methodology. For instance, the imple-                               Forward secrecy protects sessions against future corruption of
mentation of DDoS protection collects metrics (which does not                               the long-term secret keys. I.e., an attacker cannot compute the
pose a challenge for program verification) and uses a slightly dif-                         session keys of an already established session after learning the
ferent handshake (whose verification is analogous to the standard                           long-term secret keys. However, sessions that get established after
handshake; the differences are not relevant for authenticity and                            corrupting the long-term secret keys are not protected because
secrecy). Supporting multiple VPN connections requires slightly                             the attacker can impersonate participants by knowing their se-
more complex data structures, as do buffer pools, which can easily                          cret keys. The literature distinguishes between weak and strong
be handled in separation logic. Despite these simplifications, the                          forward secrecy. We were able to reuse formalizations from exist-
implementation is interoperable with other WireGuard implemen-                              ing work [11, 42, 43], which are phrased as trace-based security
tations and supports tunneling IP packets via the established VPN                           properties and, thus, directly supported by our methodology.
connection to and from the operating system. Since each IP packet                               Weak forward secrecy for a session key s (cf. entire Fig. 12) holds
is encrypted using a distinct counter value, a new handshake must                           if at any point in time, one of the following three properties hold:
be performed before the counter reaches its upper limit, which is                           (1) The attacker does not know s (line 1), (2) the actor or its peer
not yet implemented. Instead, the implementation stops forwarding                           has been corrupted before completing the handshake (line 2), or
IP packets at that point.                                                                   (3) the actor’s or peer’s session has been corrupted (line 3). In the
   Our case study goes substantially beyond of Arquint et al.’s,                            last case, the attacker gets to read the long-term and short-term
which focuses on connecting Tamarin to code-level verification,                             state of the corrupted participant, that is, the long-term secret key
and proves weak forward secrecy and non-injective agreement in                              and also the session keys if the session is established. Hence, the
the presence of long-term key corruption. We additionally con-                              attacker either directly obtains the session keys if the session is
sider session corruption, i.e., the possibility for an attacker to ob-                      already established or otherwise uses the long-term secret key to
tain ephemeral key material, and prove strong forward secrecy                               impersonate the actor or its peer while establishing a session in the
and injective agreement with actor key compromise (AKC) security.                           future. The session keys of all other sessions remain secret.
Furthermore, we have re-introduced (from the official WireGuard                                 Compared to weak forward secrecy, session keys satisfying
implementation) and verified the ability to send and receive trans-                         strong forward secrecy are additionally protected against corrupting
port messages in the initiator concurrently. This change increases                          the actor, i.e., the highlighted actor is removed from line 2 in Fig. 12.
TCP throughput compared to Arquint et al.’s implementation by a                             In particular, having access to the actor’s long-term secret key does
factor of 180, which illustrates how important such code optimiza-                          not allow the attacker to obtain the established session keys. This
tions are for real-world protocol implementations. The initiator                            resilience has been formalized as actor key compromise (AKC) by
verified in our work reaches 72% of the official implementation’s                           Basin et al. [44], generalizing the more widely known notion of key
throughput; the additional concurrency needed to close the remain-                          compromise impersonation (KCI).
ing performance gap, requires standard concurrency reasoning in                                 From the initiator’s perspective, WireGuard guarantees strong
separation logic, which is supported by our methodology.                                    forward secrecy for the two session keys once the handshake has
                                                                                   11
    CCS ’23, November 26–30, 2023, Copenhagen, Denmark                                            Linard Arquint, Malte Schwerhoff, Vaibhav Mehta, and Peter Müller


1     let commit = Commit (A ,P , ASess , PSess , m ) in                                    Case Studies        LOC      LOS     Verification time [s]
2     let running = Running (A ,P , ASess , PSess , m ) in                                  Go/Gobra
3     t. Occurs ( commit ) =⇒
4     let prefix , i = t . GetPrefix ( commit ) in                                            NSL               197      924              97.6
5     ( prefix . Occurs ( running ) &&                                                        Signed DH         225      888              119.0
6        !( ∃ A ′ ,P ′ , ASess ′ , PSess ′ ,i ′ . i != i ′ &&                                 WireGuard         557     5,815             268.1
7           t. OccursAt ( Commit ( A ′ ,P ′ , ASess ′ , PSess ′ ,m ) ,i ′ ) )
8     ) || prefix . IsCorrupted ({ P })                                                     C/VeriFast
9        || prefix . IsSessionCorrupted ({ ASess })                                           NSL               300     1,014               5.0

    Figure 13: Injective agreement with AKC security on a term m                     Figure 14: Lines of code (LOC) and lines of specification (LOS)
    from the actor A’s perspective with a peer P. The highlighted                    (incl. ghost code) for our case studies, together with the aver-
    conjunct indicates the Commit event’s uniqueness require-                        age verification times in Gobra and VeriFast. We performed
    ment for the given m.                                                            the measurements in the same way as in Fig. 9.



                                                                                        Overall, the annotation overhead for Gobra ranges between 3.9
    been completed. In contrast, the responder guarantees only weak                  and 10.4 LOS per line of code, and is in the typical range for mod-
    forward secrecy by the end of the handshake, but achieves strong                 ular program verification. For example, Wolf et al. [22] report a
    forward secrecy after receiving the first transport message. We                  ratio of 2.7 for a small example using concurrency in Gobra. VST-
    verified strong forward secrecy at the appropriate points in the                 Floyd [45], a separation logic-based verifier based on Coq, reports
    protocol for both roles.                                                         an average ratio of 13.9 for small C programs. Both works verify
       The responder’s forward secrecy guarantee is strengthened by                  only memory safety and functional properties, but do not include
    receiving and successfully processing the first transport message                any (arguably much more complex) security properties, whereas
    because this message acts as a key confirmation. I.e., the responder             our numbers include safety and security. As another data point,
    checks that it derived the same session key kIR as the initiator,                Arquint et al. [20] prove security properties for WireGuard in Go-
    which allows the responder to detect AKC attacks. Based on strong                bra with a ratio of 6.5, in addition to a Tamarin model of 350 lines
    forward secrecy for the session keys, we further prove that the VPN              and a Tamarin oracle implemented in Python, which ensures that
    payloads are treated with the same level of secrecy. This induces                Tamarin’s proof search terminates. Counting the Tamarin model
    proof obligations that a participant sends VPN payloads to the                   and oracle as specification, the overall ratio is 7.1 (and requires the
    network in a way that they can be read only by participants allowed              use of three different languages).
    to read the session keys (e.g., by encrypting the VPN payloads with                 The main challenge in our case studies was finding a sufficiently
    one of the session keys).                                                        strong trace invariant to prove the presented security properties.
       Confirming the session keys not only enables strong forward                   For WireGuard, we had to find suitable message invariants such
    secrecy for the session keys but also provides additional authenti-              that the secrecy labels for the derived session keys kIR and kRI are
    cation guarantees: Injective agreement with AKC security (cf. Fig. 13)           sufficiently strong to prove weak and strong forward secrecy. These
    states that (1) an actor A agrees with a peer P on a term m with                 secrecy labels are related to the message invariants because the
    a one-to-one correspondence between the Commit and Running                       session keys are derived by an eightfold application of key deriva-
    events unless (2) the actor’s session or (3) the peer’s (short-term or           tion functions (KDFs) that factors in long-term and ephemeral, i.e.,
    long-term) state has been corrupted. In particular, corrupting the               session-specific, Diffie-Hellman key material that is either locally
    actor is not sufficient to satisfy this property. In contrast, the NSL           generated or received from the peer. Thus, each KDF application
    protocol only satisfies injective agreement without AKC security                 results in a new key with a secrecy label that depends on the secrecy
    (as presented in Sec. 4.1) from the initiator’s perspective because              labels of the input key material. To keep the annotations related to
    having access to the initiator’s secret key enables the attacker to              the secrecy labels in the implementation to a minimum, we have
    decrypt the second message, obtain the nonces na and nb, and                     implemented a lemma for each KDF application that proves the
    construct a modified second message containing na and nb′ with                   result’s secrecy label.
    nb ≠ nb′ . Thus, there is no correspondence between Commit and                      Moreover, the invariant for protocol-specific events has to be
    Running events in the case of actor key compromise because the                   strong enough to prove injective agreement with AKC resilience.
    initiator and responder do not agree on the nonces.                              Our reusable verification library enables strengthening the proven
                                                                                     authentication property from non-injective to injective by adding
                                                                                     the uniqueness witness for each protocol-specific event. This al-
    6.4    Discussion                                                                lowed us to focus on finding a suitable invariant for non-injective
    For each case study, Fig. 14 reports the size of the implementation              agreement with AKC resilience first, and then strengthen the au-
    and its specification, along with the verification time. We exclude              thentication property, which required less than 40 additional LOS.
    the alternative NSL initiator implementation in Go, and the reusable                After completing the proofs for sequential code, we re-introduced
    verification library (recall Fig. 9). However, the specifications do             concurrency to the initiator’s transport phase (recall Sec. 6.3), which
    include the (ghost) code instantiating our reusable verification li-             entailed only minimal proof changes and was done in an afternoon.
    brary: it amounts to 374, 370, and 1,077 LOS in Gobra for NSL, DH,               This demonstrates that our separation-logic-based methodology en-
    and WireGuard, respectively, and 391 LOS in VeriFast for NSL.                    ables security proofs that are robust w.r.t. nontrivial code changes.
                                                                                12
A Generic Methodology for the Modular Verification of Security Protocol Implementations (extended version)      CCS ’23, November 26–30, 2023, Copenhagen, Denmark


7    TRUST ASSUMPTIONS AND SOUNDNESS                                                     to a standard separation logic is straightforward, based on the en-
Our methodology allows us to prove strong security properties for                        coding discussed throughout the paper (using the heap to store the
implementations of security protocols. Like with all verification                        thread-local state, a ghost lock to synchronize access, and a lock
techniques, these proofs rely on several assumptions about the                           invariant to constrain the trace and all local snapshots).
implementation and the execution environment.
   We rely on the soundness of the used program verifier. Since our
                                                                                         8    RELATED WORK
methodology is compatible with standard separation logic verifiers,
we can mitigate this assumption by using a mature tool.                                  Much prior work on the verification of cryptographic protocols ex-
   As is standard for symbolic cryptography, we assume perfect                           ists, and surveys [47–49] provide an extensive overview of the field.
cryptographic operations (e.g., absence of hash collisions, or that                      We focus on modular verification of symbolic security properties, and
ciphertexts do not leak any information). We also do not verify that                     discuss the most closely related work first: techniques for verifying
the implementations of the cryptographic primitives are function-                        security of realistic protocol implementations.
ally correct; while this is orthogonal to our work, our methodology                         Dupressoir et al. [32] use VCC [33] to verify memory safety, non-
could be combined with verified libraries like EverCrypt [46].                           injective agreement, and (via an external argument in Coq) weak
   Furthermore, we assume that all output operations, i.e., sending                      secrecy, of two protocols implemented in C: RPC and Otway-Rees.
messages, are reflected on the global trace by corresponding events,                     To our knowledge, they are the first to encode a global protocol trace
which is the case when using the I/O operations provided by our                          (“log”) as a concurrent data structure. We generalize this idea to sep-
verification library. However, if an implementation uses, e.g., inline                   aration logic to make it much more widely applicable, because their
assembly or third-party libraries to send messages to the network,                       encoding relies on C’s volatile fields and a VCC-specific program
the global trace has to reflect these messages nonetheless. Omitting                     logic, neither of which are (widely) available in other languages and
any other event does not affect soundness, only completeness.                            verifiers. Moreover, since their logic (unlike separation logic) does
   Lastly, we assume that the protocol terms corresponding to the                        not provide linear resources, proving injective agreement would
byte arrays in a participant’s initial state, and those obtained from                    require a nontrivial extension of their work. Their set-based trace
operations outside of our library (e.g., read from a config file), are                   encoding prevents proving, e.g., forward secrecy (which we do);
readable at least by that participant according to the terms’ secrecy                    they account for principal corruption, but not session corruption
labels (recall Sec. 4.2). Otherwise, it would not be sufficient to model                 (we account for both). Polikarpova et al. [50] extend this work by
corruption of a participant by adding the class of terms readable by                     incorporating stepwise refinement to formally connect a model to
that participant to the attacker knowledge; the attacker could learn                     an existing implementation, all encoded in VCC. This refinement
even more. For all terms a participant can obtain by interacting with                    decomposes the verification into smaller steps, but incurs additional
our verification library (e.g., receiving messages, generating nonces,                   overhead. Moreover, they remove the need for external arguments
applying encryption), we prove in our library (via corresponding                         when proving weak secrecy. They verify the latter, and a variant of
lemmas) that a participant can read these terms (and thus the terms                      authentication, for a small stateful subset of TPM 2.0.
leak as expected to the attacker in case of corruption).                                    Vanspauwen et al. [51], like us, use a separation-logic-based
   We sketch soundness of our methodology in App. A by show-                             verifier (VeriFast [21]), but they do not model a global trace. Conse-
ing that the global trace reflects all relevant protocol steps and,                      quently, properties that are commonly expressed over a trace poten-
thus, any security property proved for the trace indeed holds for                        tially need to be assembled from individual assertions. They propose
the protocol implementation. For this purpose, we define a core                          an extended symbolic model that strengthens attackers by permit-
programming language covering all protocol-relevant operations                           ting byte-wise manipulations, such as splitting and reconcatenating
(e.g., network I/O, cryptographic primitives), and those relevant for                    byte sequences, in addition to the usual symbolic manipulations.
modeling an attacker (e.g., corruption). The language’s operational                      Our attacker operates on terms (standard for symbolic cryptogra-
semantics supports thread-local state and explicitly maintains a                         phy) but we could adapt their extension. They specify PolarSSL’s
shared global trace. The thread-local state models the state of each                     API using this extended model, and then verify secrecy and non-
participant and is manipulated via assignments in the participants’                      injective agreement of an NSL-implementation (and a few less com-
implementations. In contrast, the global trace is maintained au-                         plex protocols). Unlike us, they do not consider session corruption.
tomatically by our semantics and extended whenever a relevant                               Arquint et al. [20] suggest a two-step approach: First, a proto-
protocol operation is executed. We then define a Hoare logic to                          col model is verified via Tamarin [52]. If successful, a separation
enable modularly verifying each participant implementation. The                          logic predicate (one per participant) with I/O specifications [53]
logic natively supports our methodology’s local snapshots and the                        is generated, specifying which I/O operations preserve the secu-
global trace. We prove that this logic is sound w.r.t. the operational                   rity properties of the model. Second, existing implementations of
semantics using a standard rule induction. Thereby, we obtain the                        the protocol can be verified against these predicates; if successful,
guarantee that locally-verified participants, if composed with the                       the implementation is guaranteed to satisfy the model’s proper-
attacker to a concurrent system, maintain the global trace invariant                     ties. This two-step workflow achieves tool reuse—Tamarin, and
in all possible interleavings. As one would expect, obtaining this                       suitable separation logic verifiers—but requires expertise in two
global guarantee turned out to be the most challenging step in the                       different fields of formal reasoning, and the existence of a Tamarin
soundness proof. Formally connecting our dedicated Hoare logic                           protocol model. Moreover, limitations of Tamarin (e.g., difficulties
                                                                                         when verifying protocols with loops), and of the I/O specifications
                                                                                         (unclear how to generate specifications suitable for a concurrent
                                                                                   13
CCS ’23, November 26–30, 2023, Copenhagen, Denmark                                            Linard Arquint, Malte Schwerhoff, Vaibhav Mehta, and Peter Müller


implementation) may prevent verifying corresponding implemen-                  However, due to probabilistic reasoning, verifying computational
tations. Similar limitations apply to Sprenger et al.’s work [34],             security is generally more challenging than reasoning about sym-
which connects protocol models verified in Isabelle/HOL [54] via               bolic terms, and we are not aware of tools for modularly verifying
I/O specifications to separation logic verifiers.                              computational security properties of existing implementations. Re-
   Bhargavan et al. [9] suggest DY*: a framework for verifying pro-            cently, the first separation logics for probabilistic reasoning have
tocols implemented in F* [12], a functional language that enables              been proposed [64–66], but we are not aware of automated verifiers
type-system-based proofs, e.g., using monadic effects and refine-              for such logics.
ment types. DY* introduces the idea of a parametric library for
reducing the per-protocol proof effort; an idea we adopted. DY*’s              9    CONCLUSIONS
type system is tailored to F*, whereas our methodology supports a
                                                                               We presented a methodology for the modular verification of secu-
wide range of languages and tools. Moreover, by building on sepa-
                                                                               rity protocol implementations. It enables proving strong security
ration logic, we are able to prove stronger properties, in particular,
                                                                               properties for realistic protocol implementations in the presence of
injective agreement. Our methodology can be applied directly to
                                                                               a network-controlling attacker. By employing separation logic, we
existing implementations, as we demonstrate in the WireGuard
                                                                               support efficient implementations using heap data structures, side
case study. In contrast, DY* supports code generation, but addition-
                                                                               effects, concurrency, etc. Encapsulating the global trace in a concur-
ally requires a hand-written (and partly protocol-specific) runtime
                                                                               rent ghost data structure and our use of invariants over local snap-
wrapper [10]. Included in DY*’s case study is the first automated
                                                                               shots allow our methodology to support arbitrary code structures
verification of Signal [2] that proves forward and post-compromise
                                                                               and data representations, which is crucial for targeting existing im-
security over an unbounded number of protocol messages. Our
                                                                               plementations. Separation logic also allows us to specify resources
main case study is WireGuard, for which we prove, also for an
                                                                               in the trace invariant to express uniqueness of protocol-specific
unbounded number of messages, forward secrecy and injective
                                                                               events, which is key to modularly proving injective agreement.
agreement with AKC resilience. Soundness of DY*’s global protocol
                                                                                  We have instantiated our methodology for Go and C and two
trace depends on a specific coding discipline (one method per pro-
                                                                               corresponding verifiers. Our case studies on NSL, signed DH, and
tocol step) that is not automatically enforced. If missed, the attacker
                                                                               WireGuard demonstrate that our methodology handles existing and
is accidentally restricted, and security properties can be proven
                                                                               interoperable implementations of protocols with strong security
incorrectly.
                                                                               properties, such as forward secrecy and injective agreement.
   An earlier line of work (e.g., [37, 55, 56]) verifies security of
                                                                                  For future work, we plan to integrate our methodology with
functional programs written in F# using the F7 type checker [55],
                                                                               formally-verified cryptographic libraries to further reduce our trust
but does not integrate equational theories, and has limited support
                                                                               assumptions. It would also be interesting to advance towards the
for mutable state. Moreover, this work does not model the global
                                                                               computational model of cryptography by combining our work with
protocol traces and, thus, states security properties only implicitly.
                                                                               probabilistic separation logic.
   Küsters et al. [57] share our goal of reusing existing program
analyzers and suggest an approach that enables non-interference
checkers to establish computational indistinguishability results for           ACKNOWLEDGMENTS
sequential programs. To account for closed-system assumptions                  We thank the Werner Siemens-Stiftung (WSS) for their generous
(typically made by such checkers) in the presence of an attacker-              support of this project. We are grateful to Ralf Sasse for the helpful
controlled environment, they restrict interaction with the latter to           discussions and feedback on an earlier draft of this paper; Thibault
static, exception-free methods, and primitive (i.e., value) types. How         Dardinier, for his suggestions for the soundness proof; Hugo Quein-
to extend their approach to trace-based properties and concurrent              nec, for his critical questions; and the anonymous reviewers for
programs remains unclear.                                                      their helpful feedback that helped us sharpen our contributions.
   Several security property verifiers exist that (unlike us) do not
reuse existing program analyzers, e.g., Csur [58] and ASPIER [59]              REFERENCES
(for C), and JavaSec [60] (for Java). However, to reduce develop-               [1] J. A. Donenfeld, “WireGuard: Next generation kernel network tunnel,” in NDSS.
ment costs, such domain-specific tools typically only implement                     The Internet Society, 2017.
                                                                                [2] M. Marlinspike and T. Perrin. The X3DH key agreement protocol (revision 1).
semantics of a restricted language subset and, e.g., assume crucial                 [Online]. Available: https://www.signal.org/docs/specifications/x3dh/
properties such as memory safety (which may render implementa-                  [3] G. Lowe, “Breaking and fixing the Needham-Schroeder public-key protocol using
tions insecure, e.g., due to buffer overflows).                                     FDR,” in TACAS, ser. LNCS, vol. 1055. Springer, 1996, pp. 147–166.
                                                                                [4] R. M. Needham and M. D. Schroeder, “Using encryption for authentication in
   Prior work [11, 39, 40, 42, 61, 62] on verifying properties of Wire-             large networks of computers,” Commun. ACM, vol. 21, no. 12, pp. 993–999, 1978.
Guard (our main case study) is concerned with verifying models of               [5] CVE, “CVE-2014-0160,” 2013. [Online]. Available: https://www.cve.org/
the protocol, not existing implementations.                                         CVERecord?id=CVE-2014-0160
                                                                                [6] ——, “CVE-2021-40823,” 2021. [Online]. Available: https://www.cve.org/
   Finally, a large body of work is concerned with mechanizing                      CVERecord?id=CVE-2021-40823
the verification of computational (rather than symbolic) properties;            [7] D. Pozza, R. Sisto, and L. Durante, “Spi2Java: Automatic cryptographic protocol
                                                                                    Java code generation from spi calculus,” in AINA. IEEE Computer Society, 2004,
see aforementioned surveys for details. This line of work estab-                    pp. 400–405.
lishes stronger guarantees by making weaker, more realistic cryp-               [8] D. Cadé and B. Blanchet, “From computationally-proved protocol specifications
tographic assumptions. For instance, Owl [63] allows one to verify                  to implementations,” in ARES. IEEE Computer Society, 2012, pp. 65–74.
                                                                                [9] K. Bhargavan, A. Bichhawat, Q. H. Do, P. Hosseyni, R. Küsters, G. Schmitz, and
computational security of protocols written in a dedicated language.                T. Würtele, “DY*: A modular symbolic verification framework for executable
Like in our work, their proofs are automated and compositional.                     cryptographic protocol code,” in EuroS&P. IEEE, 2021, pp. 523–542.
                                                                          14
A Generic Methodology for the Modular Verification of Security Protocol Implementations (extended version)                    CCS ’23, November 26–30, 2023, Copenhagen, Denmark


[10] ——, “An in-depth symbolic security analysis of the ACME standard,” in CCS.                  [39] B. Dowling and K. G. Paterson, “A cryptographic analysis of the WireGuard
     ACM, 2021, pp. 2601–2617.                                                                        protocol,” in ACNS, ser. LNCS, vol. 10892. Springer, 2018, pp. 3–21.
[11] S. Ho, J. Protzenko, A. Bichhawat, and K. Bhargavan, “Noise*: A library of verified         [40] B. Lipp, B. Blanchet, and K. Bhargavan, “A mechanised cryptographic proof of
     high-performance secure channel protocol implementations,” in S&P. IEEE,                         the WireGuard virtual private network protocol,” in EuroS&P. IEEE, 2019, pp.
     2022, pp. 107–124.                                                                               231–246.
[12] N. Swamy, C. Hritcu, C. Keller, A. Rastogi, A. Delignat-Lavaud, S. Forest, K. Bhar-         [41] L. Arquint, F. A. Wolf, J. Lallemand, R. Sasse, C. Sprenger, S. N. Wiesner,
     gavan, C. Fournet, P. Strub, M. Kohlweiss, J. K. Zinzindohoue, and S. Z. Béguelin,               D. Basin, and P. Müller, “Sound verification of security protocols: From design
     “Dependent types and multi-monadic effects in F*,” in POPL. ACM, 2016, pp.                       to interoperable implementations,” Aug. 2022, Tamarin model & verified Go
     256–270.                                                                                         implementation of the WireGuard VPN key exchange protocol. [Online].
[13] K. Bhargavan, C. Fournet, A. D. Gordon, and S. Tse, “Verified interoperable                      Available: https://doi.org/10.5281/zenodo.7409524
     implementations of security protocols,” ACM Trans. Program. Lang. Syst., vol. 31,           [42] G. Girol, L. Hirschi, R. Sasse, D. Jackson, C. Cremers, and D. A. Basin, “A spectral
     no. 1, pp. 5:1–5:61, 2008.                                                                       analysis of Noise: A comprehensive, automated, formal analysis of Diffie-Hellman
[14] N. O’Shea, “Using Elyjah to analyse Java implementations of cryptographic                        protocols,” in USENIX Security Symposium. USENIX Association, 2020, pp. 1857–
     protocols,” in FCS-ARSPA-WITS-2008, 2008.                                                        1874.
[15] M. Aizatulin, A. D. Gordon, and J. Jürjens, “Computational verification of C                [43] C. Cremers, M. Horvat, J. Hoyland, S. Scott, and T. van der Merwe, “A compre-
     protocol implementations by symbolic execution,” in CCS. ACM, 2012, pp.                          hensive symbolic analysis of TLS 1.3,” in CCS. ACM, 2017, pp. 1773–1788.
     712–723.                                                                                    [44] D. A. Basin, C. Cremers, and M. Horvat, “Actor key compromise: Consequences
[16] N. Kobeissi, K. Bhargavan, and B. Blanchet, “Automated verification for secure                   and countermeasures,” in CSF. IEEE Computer Society, 2014, pp. 244–258.
     messaging protocols and their implementations: A symbolic and computational                 [45] Q. Cao, L. Beringer, S. Gruetter, J. Dodds, and A. W. Appel, “Vst-floyd: A separation
     approach,” in EuroS&P. IEEE, 2017, pp. 435–450.                                                  logic tool to verify correctness of C programs,” J. Autom. Reason., vol. 61, no. 1-4,
[17] K. Bhargavan, B. Blanchet, and N. Kobeissi, “Verified models and reference imple-                pp. 367–422, 2018.
     mentations for the TLS 1.3 standard candidate,” in S&P. IEEE Computer Society,              [46] J. Protzenko, B. Parno, A. Fromherz, C. Hawblitzel, M. Polubelova, K. Bhar-
     2017, pp. 483–502.                                                                               gavan, B. Beurdouche, J. Choi, A. Delignat-Lavaud, C. Fournet, N. Kulatova,
[18] R. Sisto, P. B. Copet, M. Avalle, and A. Pironti, “Formally sound implementations                T. Ramananandro, A. Rastogi, N. Swamy, C. M. Wintersteiger, and S. Z. Béguelin,
     of security protocols with JavaSPI,” Formal Aspects Comput., vol. 30, no. 2, pp.                 “EverCrypt: A fast, verified, cross-platform cryptographic provider,” in S&P. IEEE,
     279–317, 2018.                                                                                   2020, pp. 983–1002.
[19] J. Protzenko, B. Beurdouche, D. Merigoux, and K. Bhargavan, “Formally verified              [47] M. Barbosa, G. Barthe, K. Bhargavan, B. Blanchet, C. Cremers, K. Liao, and
     cryptographic web applications in WebAssembly,” in S&P. IEEE, 2019, pp.                          B. Parno, “SoK: Computer-aided cryptography,” in S&P. IEEE, 2021, pp. 777–795.
     1256–1274.                                                                                  [48] M. Avalle, A. Pironti, and R. Sisto, “Formal verification of security protocol
[20] L. Arquint, F. A. Wolf, J. Lallemand, R. Sasse, C. Sprenger, S. N. Wiesner, D. A.                implementations: a survey,” Formal Aspects Comput., vol. 26, no. 1, pp. 99–123,
     Basin, and P. Müller, “Sound verification of security protocols: From design to                  2014.
     interoperable implementations,” in SP. IEEE, 2023, pp. 1077–1093.                           [49] B. Blanchet, “Security protocol verification: Symbolic and computational models,”
[21] B. Jacobs, J. Smans, P. Philippaerts, F. Vogels, W. Penninckx, and F. Piessens,                  in POST, ser. LNCS, vol. 7215. Springer, 2012, pp. 3–29.
     “VeriFast: A powerful, sound, predictable, fast verifier for C and Java,” in NASA           [50] N. Polikarpova and M. Moskal, “Verifying implementations of security protocols
     Formal Methods, ser. LNCS, vol. 6617. Springer, 2011, pp. 41–55.                                 by refinement,” in VSTTE, ser. LNCS, vol. 7152. Springer, 2012, pp. 50–65.
[22] F. A. Wolf, L. Arquint, M. Clochard, W. Oortwijn, J. C. Pereira, and P. Müller,             [51] G. Vanspauwen and B. Jacobs, “Verifying protocol implementations by augment-
     “Gobra: Modular specification and verification of Go programs,” in CAV, ser. LNCS,               ing existing cryptographic libraries with specifications,” in SEFM, ser. LNCS, vol.
     vol. 12759. Springer, 2021, pp. 367–379.                                                         9276. Springer, 2015, pp. 53–68.
[23] S. Blom and M. Huisman, “The VerCors tool for verification of concurrent pro-               [52] B. Schmidt, S. Meier, C. Cremers, and D. A. Basin, “Automated analysis of Diffie-
     grams,” in FM, ser. LNCS, vol. 8442. Springer, 2014, pp. 127–131.                                Hellman protocols and advanced security properties,” in CSF. IEEE Computer
[24] J. F. Santos, P. Maksimovic, D. Naudziuniene, T. Wood, and P. Gardner, “JaVerT:                  Society, 2012, pp. 78–94.
     JavaScript verification toolchain,” Proc. ACM Program. Lang., vol. 2, no. POPL, pp.         [53] W. Penninckx, B. Jacobs, and F. Piessens, “Sound, modular and compositional
     50:1–50:33, 2018.                                                                                verification of the input/output behavior of programs,” in ESOP, ser. LNCS, vol.
[25] V. Astrauskas, P. Müller, F. Poli, and A. J. Summers, “Leveraging Rust types for                 9032. Springer, 2015, pp. 158–182.
     modular specification and verification,” Proc. ACM Program. Lang., vol. 3, no.              [54] T. Nipkow, L. C. Paulson, and M. Wenzel, Isabelle/HOL - A Proof Assistant for
     OOPSLA, pp. 147:1–147:30, 2019.                                                                  Higher-Order Logic, ser. LNCS. Springer, 2002, vol. 2283.
[26] P. W. O’Hearn, J. C. Reynolds, and H. Yang, “Local reasoning about programs                 [55] J. Bengtson, K. Bhargavan, C. Fournet, A. D. Gordon, and S. Maffeis, “Refinement
     that alter data structures,” in CSL, ser. LNCS, vol. 2142. Springer, 2001, pp. 1–19.             types for secure implementations,” in CSF. IEEE Computer Society, 2008, pp.
[27] J. C. Reynolds, “Separation Logic: A logic for shared mutable data structures,” in               17–32.
     LICS. IEEE Computer Society, 2002, pp. 55–74.                                               [56] K. Bhargavan, C. Fournet, and N. Guts, “Typechecking higher-order security
[28] J. Filliâtre, L. Gondelman, and A. Paskevich, “The spirit of ghost code,” in CAV,                libraries,” in APLAS, ser. LNCS, vol. 6461. Springer, 2010, pp. 47–62.
     ser. LNCS, vol. 8559. Springer, 2014, pp. 1–16.                                             [57] R. Küsters, T. Truderung, and J. Graf, “A framework for the cryptographic verifi-
[29] D. Dolev and A. C. Yao, “On the security of public key protocols,” IEEE Trans. Inf.              cation of Java-like programs,” in CSF. IEEE Computer Society, 2012, pp. 198–212.
     Theory, vol. 29, no. 2, pp. 198–207, 1983.                                                  [58] J. Goubault-Larrecq and F. Parrennes, “Cryptographic protocol analysis on real C
[30] W. Diffie and M. E. Hellman, “New directions in cryptography,” IEEE Trans. Inf.                  code,” in VMCAI, ser. LNCS, vol. 3385. Springer, 2005, pp. 363–379.
     Theory, vol. 22, no. 6, pp. 644–654, 1976.                                                  [59] S. Chaki and A. Datta, “ASPIER: An automated framework for verifying security
[31] L. Arquint, M. Schwerhoff, V. Mehta, and P. Müller, “A generic methodology for                   protocol implementations,” in CSF. IEEE Computer Society, 2009, pp. 172–185.
     the modular verification of security protocol implementations,” Sep. 2023, artifact         [60] J. Jürjens, “Security analysis of crypto-based Java programs using automated
     containing the reusable verification libraries and the case studies. [Online].                   theorem provers,” in ASE. IEEE Computer Society, 2006, pp. 167–176.
     Available: https://doi.org/10.5281/zenodo.8330913                                           [61] J. A. Donenfeld and K. Milner. Formal verification of the WireGuard
[32] F. Dupressoir, A. D. Gordon, J. Jürjens, and D. A. Naumann, “Guiding a general-                  protocol. [Online]. Available: https://www.wireguard.com/papers/wireguard-
     purpose C verifier to prove cryptographic protocols,” in CSF. IEEE Computer                      formal-verification.pdf
     Society, 2011, pp. 3–17.                                                                    [62] N. Kobeissi, G. Nicolas, and K. Bhargavan, “Noise Explorer: Fully automated
[33] E. Cohen, M. Dahlweid, M. A. Hillebrand, D. Leinenbach, M. Moskal, T. Santen,                    modeling and verification for arbitrary Noise protocols,” in EuroS&P. IEEE, 2019,
     W. Schulte, and S. Tobies, “VCC: A practical system for verifying concurrent C,”                 pp. 356–370.
     in TPHOLs, ser. LNCS, vol. 5674. Springer, 2009, pp. 23–42.                                 [63] J. Gancher, S. Gibson, P. Singh, S. Dharanikota, and B. Parno, “Owl: Compositional
[34] C. Sprenger, T. Klenze, M. Eilers, F. A. Wolf, P. Müller, M. Clochard, and D. A.                 verification of security protocols via an information-flow type system,” in SP.
     Basin, “Igloo: soundly linking compositional refinement and separation logic for                 IEEE, 2023, pp. 1130–1147.
     distributed system verification,” Proc. ACM Program. Lang., vol. 4, no. OOPSLA,             [64] J. Tassarotti and R. Harper, “A Separation Logic for concurrent randomized
     pp. 152:1–152:31, 2020.                                                                          programs,” Proc. ACM Program. Lang., vol. 3, no. POPL, pp. 64:1–64:30, 2019.
[35] J. Boyland, “Checking interference with fractional permissions,” in SAS, ser. LNCS,         [65] K. Batz, B. L. Kaminski, J. Katoen, C. Matheja, and T. Noll, “Quantitative Separation
     vol. 2694. Springer, 2003, pp. 55–72.                                                            Logic: A logic for reasoning about probabilistic pointer programs,” Proc. ACM
[36] G. Lowe, “A hierarchy of authentication specification,” in CSFW. IEEE Computer                   Program. Lang., vol. 3, no. POPL, pp. 34:1–34:29, 2019.
     Society, 1997, pp. 31–44.                                                                   [66] G. Barthe, J. Hsu, and K. Liao, “A probabilistic Separation Logic,” Proc. ACM
[37] K. Bhargavan, C. Fournet, and A. D. Gordon, “Modular verification of security                    Program. Lang., vol. 4, no. POPL, pp. 55:1–55:30, 2020.
     protocol code by typing,” in POPL. ACM, 2010, pp. 445–456.                                  [67] V. Vafeiadis, “Concurrent separation logic and operational semantics,” in MFPS,
[38] M. J. Parkinson and G. M. Bierman, “Separation Logic and abstraction,” in POPL.                  ser. Electronic Notes in Theoretical Computer Science, vol. 276. Elsevier, 2011,
     ACM, 2005, pp. 247–258.                                                                          pp. 335–351.
                                                                                            15
CCS ’23, November 26–30, 2023, Copenhagen, Denmark                                         Linard Arquint, Malte Schwerhoff, Vaibhav Mehta, and Peter Müller


A     SOUNDNESS PROOF SKETCH                                                  shape for local configurations of participants and the attacker, both
Intuitively, we argue soundness of our methodology by showing                 can apply the same operational semantics rules, e.g., for sequential
that, given a distributed system of verified protocol implementa-             composition.
tions and an arbitrary attacker, the systems’ set of possible exe-               Definition 3. Programming language. We consider the follow-
cutions is a subset of the executions permitted by the verification           ing programming language, where 𝐶 ranges over commands, 𝑥 and 𝑥®
trace invariant, which in turn is a subset of the executions that             over variables and lists of variables in the set PVars, respectively, and
satisfy the desired security properties. To achieve this, we define a         𝑒 over expressions (modeled as total functions from PStates to PVals):
minimal but concurrent programming language with primitives for
security-relevant operations such as sending messages or creating              𝐶 ≜ skip | 𝐶; 𝐶 | if (𝑒) {𝐶} else {𝐶} | while (𝑒) {𝐶} |
nonces, and a corresponding operational semantics (Sec. A.1) that                   x B e | send (𝑒) | x B recv() | x B nonce() |
reflects these operations on a global (i.e. system-wide shared) trace.              x B hash(𝑒) | x B pk(𝑒) | x B enc(𝑒, 𝑒) | x, x B dec(𝑒, 𝑒) |
We then define an axiomatic semantics (Sec. A.2) parameterized                      drop(𝑒) | learn(𝑒) | x B choose() | corrupt (𝑒) |
with a trace invariant that we prove sound w.r.t. the operational
semantics. I.e., we show that the axiomatic proof rules enforce the                 fork (𝑥)
                                                                                          ® {𝐶}
trace invariant. Since the global trace maintained by the opera-                 Besides standard commands, such as sequential composition
tional semantics reflects all relevant protocol steps, and because            and assignment, the programming language provides several com-
our axiomatic semantics is proven sound, we can conclude that the             mands essential for protocol implementations: for sending and
aforementioned trace inclusion holds (Sec. A.3). In each subsection,          receiving a network message, for generating a nonce, hashing a
we additionally relate the semantics defined for the proof sketch             term, generating a public key corresponding to a given secret key
with the verification performed by an off-the-shelf separation-logic          (pk), and encrypting and decrypting a term with a key. Additionally,
verifier (such as Gobra) against our reusable verification library.           the programming language provides commands only available to
                                                                              the attacker: dropping a message from the network, adding the
A.1     Language and Operational Semantics                                    value of a local variable to the attacker knowledge (learn), non-
On a high-level, we consider a distributed system consisting of               deterministically obtaining a term from the attacker knowledge
multiple components: either instances of a protocol implementa-               (choose), and corrupting the state of specific participant (each par-
tion, i.e. participants, or the attacker. Our programming language            ticipant has a unique id/index).
does not support user-defined shared variables or a heap, and each               Finally, fork starts a new thread executing the provided com-
participant executes its commands in its own local state. However,            mand, which corresponds to spawning a new participant or the
security-relevant commands additionally mutate the global trace               attacker. The new thread operates on its own local state, which
to reflect the performed operation.                                           initially maps the variables in 𝑥® to the same values as the state in
   Consequently, our system’s configurations comprise a local con-            which the fork command is executed. This command is used to
figuration per component, and the global trace 𝜏. A local config-             bootstrap the distributed system, as discussed in Sec. A.3.
uration for a protocol participant 𝑖 is characterized by its local               The expression language comprises symbolic terms for booleans
command 𝐶𝑖 and local state 𝜎𝑖 . The local configuration for the at-           and integers, and the usual operations thereon. We assume well-
tacker is similar, but additionally contains a knowledge set 𝑘𝑎 that          typed programs, e.g., that if-conditions are of type boolean.
stores all symbolic terms that are known to the attacker.
                                                                                 Definition 4. Operational semantics Fig. 15 defines the small-
   Definition 1. Local program states. Local program states,                  step operational semantics for our programming language.
ranged over by 𝜎, are total functions from local variables (in the
set PVars) to values (in the set PVals).                                        The rules for standard commands such as sequential composition
                                                                              and conditionals, are as expected, and we will thus only discuss
                        PStates ≜ PVars → PVals                               non-standard aspects of our programming language.
   We define our programming language such that it directly works                 Global trace. Recall from Sec. 3.3 that in our verification method-
with symbolic terms instead of bytes, which avoids having to com-             ology (as implemented in Gobra), we use a concurrent ghost data
plicate the semantics to reflect the orthogonal issue of mapping              structure with ghost locks to manage the global trace. In our opera-
between the bytes and terms.                                                  tional semantics, we instead represent the trace as the dedicated
   Definition 2. System configurations. A configuration of our                element 𝜏 in the system’s state. Irregardless of the technical im-
distributed system has the shape                                              plementation we must ensure three crucial properties: (1) Each
                ⟨⟨𝐶 1, 𝜎1 ⟩, · · · , ⟨𝐶𝑛 , 𝜎𝑛 ⟩, ⟨𝐶𝑎 , 𝜎𝑎 ⟩, 𝑘𝑎 , 𝜏⟩          operation may only append a single trace events. In our methodol-
                                                                              ogy, this is checked via a suitable proof obligation upon lock release;
where ⟨𝐶𝑖 , 𝜎𝑖 ⟩ denotes the local command and local state of partic-         in our operational semantics, each rule adds at most one event. (2)
ipant 𝑖, ⟨𝐶𝑎 , 𝜎𝑎 ⟩ denotes the local command and local state of the          To ensure monotonicity, the trace may only grow. Checked upon
attacker 𝑎, 𝑘𝑎 is the attacker’s knowledge set and 𝜏 denotes the sys-         lock release in our methodology; in our operational semantics, no
tem’s global trace.                                                           rule shortens the trace. (3) Each single operation must preserve the
   Observe that the attacker’s knowledge set 𝑘𝑎 is not part of the            trace invariant. Checked upon lock release in our methodology; in
attacker’s local configuration ⟨𝐶𝑎 , 𝜎𝑎 ⟩, even though only commands          our operational semantics, this is part of the soundness theorem
executed by the attacker possibly modify 𝑘𝑎 . By using the same               (cf. Thm. 1).
                                                                         16
A Generic Methodology for the Modular Verification of Security Protocol Implementations (extended version)                         CCS ’23, November 26–30, 2023, Copenhagen, Denmark



                            ⟨𝐶𝑖 , ⟨𝜎𝑖 , 𝜏⟩⟩ → ⟨𝐶𝑖′, ⟨𝜎𝑖′, 𝜏 ′ ⟩⟩                                             ⟨𝐶𝑎 , ⟨𝜎𝑎 , 𝑘𝑎 , 𝜏⟩⟩ → ⟨𝐶𝑎′ , ⟨𝜎𝑎′ , 𝑘𝑎′ , 𝜏 ′ ⟩⟩
                                                                                           (Local)                                                                         (Attacker)
           ⟨· · · , ⟨𝐶𝑖 , 𝜎𝑖 ⟩, · · · , 𝑘𝑎 , 𝜏⟩ → ⟨· · · , ⟨𝐶𝑖′, 𝜎𝑖′ ⟩, · · · , 𝑘𝑎 , 𝜏 ′ ⟩             ⟨· · · , ⟨𝐶𝑎 , 𝜎𝑎 ⟩, 𝑘𝑎 , 𝜏⟩ → ⟨· · · , ⟨𝐶𝑎′ , 𝜎𝑎′ ⟩, 𝑘𝑎′ , 𝜏 ′ ⟩

                                                                   ⟨𝐶 1, ⟨𝜎, 𝜏⟩⟩ → ⟨𝜖, ⟨𝜎 ′, 𝜏 ′ ⟩⟩                               ⟨𝐶 1, ⟨𝜎, 𝜏⟩⟩ → ⟨𝐶 1′ , ⟨𝜎 ′, 𝜏 ′ ⟩⟩
                                                 (Skip)                                                     (Seq1)                                                             (Seq2)
            ⟨skip, ⟨𝜎, 𝜏⟩⟩ → ⟨𝜖, ⟨𝜎, 𝜏⟩⟩                        ⟨𝐶 1 ; 𝐶 2, ⟨𝜎, 𝜏⟩⟩ → ⟨𝐶 2, ⟨𝜎 ′, 𝜏 ′ ⟩⟩                    ⟨𝐶 1 ; 𝐶 2, ⟨𝜎, 𝜏⟩⟩ → ⟨𝐶 1′ ; 𝐶 2, ⟨𝜎 ′, 𝜏 ′ ⟩⟩

                                                                        (If1)𝑒 (𝜎𝑖 )=True ()                                                                         (If2)𝑒 (𝜎𝑖 )≠True ()
         ⟨if (𝑒) {𝐶 1 } else {𝐶 2 }, ⟨𝜎, 𝜏⟩⟩ → ⟨𝐶 1, ⟨𝜎, 𝜏⟩⟩                                         ⟨if (𝑒) {𝐶 1 } else {𝐶 2 }, ⟨𝜎, 𝜏⟩⟩ → ⟨𝐶 2, ⟨𝜎, 𝜏⟩⟩

                                                                                                                                                (While)
                                        ⟨while (𝑒) {𝐶}, ⟨𝜎, 𝜏⟩⟩ → ⟨if (𝑒) {𝐶; while (𝑒) {𝐶}} else {skip}, ⟨𝜎, 𝜏⟩⟩

                                                                                                                       (Assign)
                                                               ⟨x B e, ⟨𝜎, 𝜏⟩⟩ → ⟨𝜖, ⟨𝜎 [𝑥 ↦→ 𝑒 (𝜎)], 𝜏⟩⟩

                                                                                                                                              (Send)
                                            ⟨send (𝑒), ⟨𝜎, 𝜏⟩⟩ → ⟨𝜖, ⟨𝜎 [snap ↦→ 𝜏 + Send (𝑒 (𝜎))], 𝜏 + Send (𝑒 (𝜎))⟩⟩

                                                                                                                   (Recv) 𝑣 ∈msgs (𝜏 )
                                                         ⟨x B recv(), ⟨𝜎, 𝜏⟩⟩ → ⟨𝜖, ⟨𝜎 [𝑥 ↦→ 𝑣], 𝜏⟩⟩

                                                                                                                                         (NonceGen) fresh(𝑣,𝜏 )
                            ⟨x B nonce(), ⟨𝜎, 𝜏⟩⟩ → ⟨𝜖, ⟨𝜎 [𝑥 ↦→ 𝑣, snap ↦→ 𝜏 + Nonce(𝑣)], 𝜏 + Nonce(𝑣)⟩⟩

                                                                                          (Hash)                                                                               (Pk)
             ⟨x B hash(𝑒), ⟨𝜎, 𝜏⟩⟩ → ⟨𝜖, ⟨𝜎 [𝑥 ↦→ Hash(𝑒 (𝜎))], 𝜏⟩⟩                                      ⟨x B pk(𝑒), ⟨𝜎, 𝜏⟩⟩ → ⟨𝜖, ⟨𝜎 [𝑥 ↦→ Pk(𝑒 (𝜎))], 𝜏⟩⟩

                                                                                                                                          (Enc)
                                                 ⟨x B enc(𝑒 1, 𝑒 2 ), ⟨𝜎, 𝜏⟩⟩ → ⟨𝜖, ⟨𝜎 [𝑥 ↦→ Enc(𝑒 1 (𝜎), 𝑒 2 (𝜎))], 𝜏⟩⟩

                                                                                                                     (DecSucc) ∃𝑣.𝑒2 (𝜎 )=Enc (Pk (𝑒1 (𝜎 ) ),𝑣)
                            ⟨x, ok B dec(𝑒 1, 𝑒 2 ), ⟨𝜎, 𝜏⟩⟩ → ⟨𝜖, ⟨𝜎 [𝑥 ↦→ 𝑣, ok ↦→ True()], 𝜏⟩⟩

                                                                                                                 (DecFail) ∀𝑣.𝑒2 (𝜎 )≠Enc (Pk (𝑒1 (𝜎 ) ),𝑣)
                                  ⟨x, ok B dec(𝑒 1, 𝑒 2 ), ⟨𝜎, 𝜏⟩⟩ → ⟨𝜖, ⟨𝜎 [ok ↦→ False()], 𝜏⟩⟩

                                                                                                                                                 (Drop)
                                        ⟨drop(𝑒), ⟨𝜎, 𝑘, 𝜏⟩⟩ → ⟨𝜖, ⟨𝜎 [snap ↦→ 𝜏 + Drop(𝑒 (𝜎))], 𝑘, 𝜏 + Drop(𝑒 (𝜎))⟩⟩

                                                                             (Learn)                                                                                (Choose) 𝑣 ∈𝑘
              ⟨learn(𝑒), ⟨𝜎, 𝑘, 𝜏⟩⟩ → ⟨𝜖, ⟨𝜎, 𝑘 ∪ {𝑒 (𝜎)}, 𝜏⟩⟩                                ⟨x B choose(), ⟨𝜎, 𝑘, 𝜏⟩⟩ → ⟨𝜖, ⟨𝜎 [𝑥 ↦→ 𝑣], 𝑘, 𝜏⟩⟩

                                                                                                                                                                           (Corrupt)
           ⟨· · · , ⟨𝐶𝑖 , 𝜎𝑖 ⟩, · · · , ⟨corrupt (𝑖); 𝐶𝑎′ , 𝜎𝑎 ⟩, 𝑘𝑎 , 𝜏⟩ → ⟨· · · , ⟨𝐶𝑖 , 𝜎𝑖 ⟩, · · · , ⟨𝐶𝑎′ , 𝜎𝑎 ⟩, 𝑘𝑎 ∪ val(𝜎𝑖 ), 𝜏 + Corrupt (𝑖, val(𝜎𝑖 ))⟩

                                                                                                                                                                                        (Fork)
 ⟨· · · , ⟨fork (𝑥 1, · · · , 𝑥𝑛 ) {𝐶}; 𝐶 ′, 𝜎𝑖 ⟩, · · · , 𝑘𝑎 , 𝜏⟩ → ⟨· · · , ⟨𝐶 ′, 𝜎𝑖 ⟩, · · · , ⟨𝐶, [𝑥 1 ↦→ 𝜎𝑖 (𝑥 1 ), · · · , 𝑥𝑛 ↦→ 𝜎𝑖 (𝑥𝑛 ), snap ↦→ 𝜎𝑖 (snap)]⟩, 𝑘𝑎 , 𝜏⟩

Figure 15: Small-step semantics. Since expressions are functions from states to values, 𝑒 (𝜎) denotes the evaluation of expression
𝑒 in state 𝜎. 𝜎 [𝑥 1 ↦→ 𝑣 1, · · · , 𝑥𝑛 ↦→ 𝑣𝑛 ] denotes state update: a state that, for all 𝑖, 1 ≤ 𝑖 ≤ 𝑛, yields 𝑣𝑖 for 𝑥𝑖 , and the value in 𝜎 for
all other variables. Appending to a trace is denoted by +, e.g., 𝜏 + Nonce(𝑣). ⟨𝜖, ⟨𝜎, 𝜏⟩⟩ denotes a terminal state.




                                                                                              17
CCS ’23, November 26–30, 2023, Copenhagen, Denmark                                             Linard Arquint, Malte Schwerhoff, Vaibhav Mehta, and Peter Müller


   Local snapshots. Recall from cf. Sec. 3.4 that each participant has          maintained even when composing arbitrarily many verified par-
a trace snapshot, which enables participants to keep local invari-              ticipants and the attacker to a distributed system. We first present
ants of trace prefixes. To enable corresponding assertions in our               several auxiliary definitions and lemmas, and then the logic’s proof
program logic (Sec. A.2), our operational semantics provide a local             rules.
variable snap that is treated special in two ways: local states 𝜎 map
                                                                                   Definition 7. Trace prefix. We define the following predicate
snap to a sequence of trace events (not to a value in PVals), and
                                                                                over two traces expressing that 𝜏1 is a prefix of 𝜏2
program commands may not use (in particular, modify) snap (a
straightforward syntactical constraint).                                                                 prefix (𝜏1, 𝜏2 ) ≜ ∃𝑝. 𝜏1 + 𝑝 = 𝜏2

   Projecting system configurations. The Local and Attacker rule                where 𝑝 is a possibly empty sequence of trace events.
project project a system configuration down to a participant- and                  Lemma 1. Prefix reflexivity.
attacker-local configuration, respectively. Besides Corrupt and
                                                                                                                   ∀𝜏 . prefix (𝜏, 𝜏)
Fork, all other rules then operate on either a participant- or attacker-
local configuration, depending on whether a command can be exe-                    Proof sketch. Pick 𝑝 to be the empty sequence in Def. 7.                                 □
cuted by participants and the attacker, or only by the attacker.
                                                                                   Lemma 2. Prefix transitivity.
    Network messages. All operations modifying the network state,
                                                                                    ∀𝜏1, 𝜏2, 𝜏3 . prefix (𝜏1, 𝜏2 ) ∧ prefix (𝜏2, 𝜏3 ) =⇒ prefix (𝜏1, 𝜏3 )
i.e., sending and dropping a message, are recorded on the global
trace 𝜏, and we can thus compute the set of receivable messages as                 Proof sketch.
follows:                                                                                       prefix (𝜏1, 𝜏2 ) ∧ prefix (𝜏2, 𝜏3 )
   Definition 5. Messages on the network.                                                          def
                                                                                                 ⇐⇒ ∃𝑝 1, 𝑝 2 . 𝜏1 + 𝑝 1 = 𝜏2 ∧ 𝜏2 + 𝑝 2 = 𝜏3
         msgs(𝜏) ≜ {𝑚 | ∀𝑚. Send (m) ∈ 𝜏 ∧ Drop(m) ∉ 𝜏 }
                                                                                                 =⇒ ∃𝑝 1, 𝑝 2 . 𝜏1 + 𝑝 1 + 𝑝 2 = 𝜏3
   Consequently, function msgs(𝜏) occurs in rule Recv’s side-condition                             def
to constrain the set of messages to receive from Without loss of                                 ⇐⇒ prefix (𝜏1, 𝜏3 )
generality, this side-condition implies that we consider only non-              where we pick in the last step 𝑝 in Def. 7 to be 𝑝 1 + 𝑝 2 .                                □
blocking traces, i.e., where recv() is invoked when msgs(𝜏) is non-
empty.                                                                              Inspired by Vafeiadis [67], we express the semantics of judge-
                                                                                ments in our logic in terms of configuration safety, which we define
   Nonce freshness. NonceGen rule’s side condition captures our                 next. Intuitively, safe𝑛 (𝑖, 𝐶, 𝜎, 𝑄, 𝜏) expresses that it is safe to exe-
perfect cryptography assumption that generated nonces are always                cute command 𝐶, as the 𝑖th component of the distributed system,
fresh.                                                                          and for 𝑛 execution steps starting in a state 𝜎; and if the command
   Definition 6. Freshness of nonces. Since all previously gener-               is fully executed, the predicate 𝑄 holds in the resulting final state.
ated nonces have been recorded on the trace 𝜏, we can define freshness          Furthermore, if new threads have been forked as part of execut-
of a nonce 𝑣 on the global trace 𝜏 as follows:                                  ing 𝐶 then it is safe to execute these forked components, too. Since
                                                                                we are ultimately interested in the effects on the global trace 𝜏,
             fresh(𝑣, 𝜏) ≜ 𝑣 ∉ {𝑛 | ∀𝑛, 𝑙 . Nonce(n, l) ∈ 𝜏 }
                                                                                configuration safety includes trace invariant 𝜌 maintenance. A
   Corruption. The Corrupt rule expresses that the attacker knowl-              judgement |= [𝑃] 𝐶 [𝑄] then expresses that it is safe to execute
edge is extended by all terms in the state 𝜎𝑖 of the corrupted partic-          the command 𝐶 for an arbitrary number of execution steps and
ipant 𝑖. The attacker can make use of these newly learnt terms by               from any initial state satisfying the predicate 𝑃.
executing x B choose() that non-deterministically picks a term in
                                                                                   Definition 8. Configuration safety.
the attacker knowledge and assigns it to the local variable 𝑥.
   Note that the Corrupt rule requires command corrupt () to be                 safe0 (𝑖, 𝐶, 𝜎, 𝑄, 𝜏) holds always.
followed by another command, skip. Baking in sequential composi-                safe𝑛+1 (𝑖, 𝐶, 𝜎, 𝑄, 𝜏) holds if and only if
tion avoids the need for further sequential rules that only differ in            (i) 𝐶 = 𝜖 =⇒ 𝑄 (𝜎) and
the kind of configuration (system vs. local) they operate on. Rule
Fork is defined analogously.                                                     (ii) ∀𝐶,     ® 𝜎®′, 𝑘𝑎 , 𝑘𝑎′ , 𝜏 ′ . 𝑖 ≤ |𝐶®| = |𝜎® | ≤ |𝐶®′ | = |𝜎®′ | ∧
                                                                                       ® 𝐶®′, 𝜎,

   Forking. Rule Fork extends the system configuration by another                                             𝐶®𝑖 = 𝐶 ∧ 𝐶®𝑖′ ≠ 𝐶 ∧ 𝜎®𝑖 = 𝜎 ∧
local configuration with the forked command to execute and the                                                𝜌 (𝜏) ∧ prefix (snap(𝜎), 𝜏) ∧
new thread’s initial state. This new state maps the variables 𝑥 1 to                                                               −−−−−−→
                                                                                                               −−−−→
𝑥𝑛 and snap to the same value as 𝜎𝑖 , i.e., the state in which the fork                                       ⟨ ⟨𝐶, 𝜎⟩, 𝑘𝑎 , 𝜏⟩ → ⟨ ⟨𝐶 ′, 𝜎 ′ ⟩, 𝑘𝑎′ , 𝜏 ′ ⟩
command is executed, which enables, e.g., the sharing of public
                                                                                       =⇒ 𝜌 (𝜏 ′ ) ∧ prefix (𝜏, 𝜏 ′ ) ∧ prefix (snap(𝜎®𝑖′ ), 𝜏 ′ ) ∧
keys.
                                                                                             𝑘𝑎 ⊆ 𝑘𝑎′ ∧ safe𝑛 (𝑖, 𝐶®𝑖′, 𝜎®𝑖′, 𝑄, 𝜏 ′ ) ∧
A.2     Program Logic
We now present a program logic that enables local reasoning about                       © Û
                                                                                                           safe𝑛 ( 𝑗, 𝐶®′𝑗 , 𝜎®′𝑗 , True(), 𝜏 ′ ) ∧ prefix (snap(𝜎®′𝑗 ), 𝜏 ′ ) ®®
                                                                                                                                                                                ª
                                                                                        ­
each participant, while guaranteeing that the trace invariant is                        ­
                                                                                        « |𝐶® |< 𝑗 ≤ |𝐶® |
                                                                                                        ′
                                                                           18                                                                                                   ¬
A Generic Methodology for the Modular Verification of Security Protocol Implementations (extended version)         CCS ’23, November 26–30, 2023, Copenhagen, Denmark



                                                                                                    𝑃 |= 𝑃 ′    𝑄 ′ |= 𝑄     ⊢ 𝑃′ 𝐶 𝑄′
                                                                                                                                   
                                                  ⊢ [𝑃] 𝐶 1 [𝑅]        ⊢ [𝑅] 𝐶 2 [𝑄]
                                      (Skip)                                             (Seq)                                                (Cons)
                  ⊢ [𝑃] 𝑠𝑘𝑖𝑝 [𝑃]                          ⊢ [𝑃] 𝐶 1 ; 𝐶 2 [𝑄]                                    ⊢ [𝑃] 𝐶 [𝑄]

         ⊢ [𝑒 ∧ 𝑃] 𝐶 1 [𝑄]        ⊢ [¬𝑒 ∧ 𝑃] 𝐶 2 [𝑄]                           ⊢ [𝑒 ∧ 𝑃] 𝐶 [𝑃]
                                                           (If)                                              (While)                                (Assign)
              ⊢ [𝑃] if (𝑒) {𝐶 1 } else {𝐶 2 } [𝑄]                     ⊢ [𝑃] while (𝑒) {𝐶} [¬𝑒 ∧ 𝑃]                         ⊢ [𝑃 [𝑒/𝑥]] x B e [𝑃]

                                                                                                     (Send)                                      (Recv)
               ⊢ [ext (Send (𝑒), snap) ∧ ∀𝑝. 𝑃 [snap + 𝑝 + Send (𝑒)/snap]] send (𝑒) [𝑃]                           ⊢ [∀𝑥 . 𝑃] x B recv() [𝑃]

                                                                                                                              (NonceGen)
                            ⊢ [ext (Nonce(𝑥), snap) ∧ ∀𝑝, 𝑥 . 𝑃 [snap + 𝑝 + Nonce(𝑥)/snap]] x B nonce() [𝑃]

                                               (Hash)                                               (Pk)                                                          (Enc)
 ⊢ [𝑃 [Hash(𝑒)/𝑥]] x B hash(𝑒) [𝑃]                           ⊢ [𝑃 [Pk(𝑒)/𝑥]] x B pk(𝑒) [𝑃]                     ⊢ [𝑃 [Enc(𝑒 1, 𝑒 2 )/𝑥]] x B enc(𝑒 1, 𝑒 2 ) [𝑃]

                                                                                                                                   (Dec)
                               ⊢ [∀𝑥 . 𝑃 [True()/ok] [𝑒 2 /Enc(Pk(𝑒 1 ), 𝑥)] ∧ 𝑃 [False()/ok]] x, ok B dec(𝑒 1, 𝑒 2 ) [𝑃]

                                                                                                                            (Drop)
                                      ⊢ [ext (Drop(𝑒), snap) ∧ ∀𝑝. 𝑃 [snap + 𝑝 + Drop(𝑒)/snap]] drop(𝑒) [𝑃]

                                                                     (Learn)                                        (Choose)
                                          ⊢ [𝑃] learn(𝑒) [𝑃]                      ⊢ [∀𝑥 . 𝑃] x B choose() [𝑃]

                                                                                                                                      (Corrupt)
                      ⊢ [(∀𝑣. ext (Corrupt (𝑒, 𝑣), snap)) ∧ (∀𝑝, 𝑣. 𝑃 [snap + 𝑝 + Corrupt (𝑒, 𝑣)/snap])] corrupt (𝑒) [𝑃]

                                               fv(𝑅) ⊆ 𝑥® 𝑃 |= 𝑅         ⊢ [𝑅] 𝐶 [True()]         ⊢ [𝑃] 𝐶 ′ [𝑄]
                                                                                                                   (Fork)
                                                                              ® {𝐶}; 𝐶 ′ [𝑄]
                                                                  ⊢ [𝑃] fork (𝑥)

                                                                     Figure 16: The proof rules.


where |𝑉® | and 𝑉®𝑖 denote the length and element at index 𝑖 of a vector 𝑉 ,             particular trace event, must always be expressed via the local snap-
            −−−−→                                                                        shot. This ensures that pre- and postconditions are stable under
resp., and ⟨𝐶, 𝜎⟩ is syntactic sugar for ⟨𝐶®1, 𝜎®1 ⟩ · · · ⟨𝐶® ® , 𝜎® | 𝜎® | ⟩.
                                                              |𝐶 |
                                                                                         potential environment interference, which is needed to prove our
   Definition 9. Validity.                                                               proof rules sound.
      |= [𝑃] 𝐶 [𝑄] ≜ ∀𝑛, 𝑖, 𝜎, 𝜏 . 𝑃 (𝜎) =⇒ safe𝑛 (𝑖, 𝐶, 𝜎, 𝑄, 𝜏)                           Similar to the discussion of the operational semantics, we discuss
                                                                                         only non-standard proof rules. Proof rules corresponding to com-
   Executing zero steps is vacuously safe. Executing 𝑛 + 1 steps                         mands that modify the global trace, e.g., Send, enforce that the trace
is safe (𝑖) if the command is already fully executed and the pred-                       invariant is maintained under potential environment interference.
icate 𝑄 satisfied; and otherwise (𝑖𝑖) if there is a transition to 𝐶®𝑖′                   For this purpose, we define an extensibility predicate specifying
that maintains the trace invariant 𝜌, the necessary monotonicity                         that appending a trace 𝑛 event to an arbitrary extension of a trace 𝜏
properties (on snapshot, trace, and the attacker’s knowledge set),                       maintains the trace invariant.
and allows continued safe execution of all components (i.e., of com-
                                                                                            Definition 10. Extensibility. A trace 𝜏 is extensible by a trace
mands 𝐶®′ ) in the system, including newly forked ones (the last,
                                                                                         event 𝑛 if the trace invariant 𝜌 is maintained for any possible trace 𝜏 ′ ,
iterated conjunct in the definition).
                                                                                         given that 𝜏 is a prefix thereof:
   Fig. 16 shows the proof rules for our logic. Our assertion lan-
guage is a first-order logic (for brevity not a separation logic) with                           ext (𝑛, 𝜏) ≜ ∀𝜏 ′ . prefix (𝜏, 𝜏 ′ ) ∧ 𝜌 (𝜏 ′ ) =⇒ 𝜌 (𝜏 ′ + 𝑛)
the usual logical connectives and quantifiers, and access to local                          Recall from Fig. 15 that commands modifying the global trace,
program variables. Pre- and postconditions can therefore refer to                        e.g., send, also update the local snapshot to the most recent ver-
the local snapshot, but they cannot refer to the global trace. The                       sion of the trace. Analogous to the proof rule for assignments, the
latter corresponds to our methodology (recall Sec. 3.4), where pre-                      proof rules for trace-modifying command thus require that the
and postconditions also cannot directly express properties about                         syntactically substituted postcondition ∀𝑝. 𝑃 [snap + 𝑝 + 𝑛/snap]
the trace because access to it is governed by our library’s ghost lock.                  holds in the state before executing the command, where n is a trace
Instead, properties about the global trace, such as the existence of a                   event (e.g., Send (𝑒)). The quantified 𝑝 accounts for all possible trace
                                                                                    19
CCS ’23, November 26–30, 2023, Copenhagen, Denmark                                                Linard Arquint, Malte Schwerhoff, Vaibhav Mehta, and Peter Müller


extensions that could have been made by the environment since                      Proof sketch. We prove this lemma by induction on 𝑛 using
the local snapshot was last updated, and thus accounts for arbitrary            the following induction hypothesis:
interleavings of participants and the attacker.                                         IH (𝑛) ≜ ∀𝑖, 𝜎, 𝑄, 𝜏 . ext (Send (𝑒 (𝜎)), snap(𝜎)) ∧
   For the sake of presentation we have omitted additional assump-
tions that are available when discharing preconditions of snapshot-                                            (∀𝑝. 𝑄 [snap + 𝑝 + Send (𝑒)/snap] (𝜎))
updating commands: e.g., in proof rule NonceGen we may addi-                                          =⇒ safe𝑛 (𝑖, send (𝑒), 𝜎, 𝑄, 𝜏)
tionally use nonce freshness, and in proof rule Recv we may assume              In the base case (𝑛 = 0), safe0 (𝑖, send (𝑒), 𝜎, 𝑄, 𝜏) holds by defi-
that a received message was previously sent and not dropped in                  nition. For the induction step, we assume IH (𝑛) and show that
the meantime.                                                                   IH (𝑛 + 1) holds. I.e., we further assume ext (Send (𝑒 (𝜎)), snap(𝜎))
   Theorem 1. Soundness of proof rules.                                         and ∀𝑝. 𝑄 [snap + 𝑝 + Send (𝑒)/snap] (𝜎) for arbitrary 𝑖, 𝜎, 𝑄, and
                                                                                𝜏. We have to prove that safe𝑛+1 (𝑖, send (𝑒), 𝜎, 𝑄, 𝜏) holds. Case (𝑖)
                 If ⊢ [𝑃] 𝐶 [𝑄] then |= [𝑃] 𝐶 [𝑄]                               from the definition of safe holds trivially because send (𝑒) ≠ 𝜖. To
    We proof this theorem in the usual way, by structural induction             prove case (𝑖𝑖), we assume the implication’s left-hand side and show
on the shape of the proof tree given by the theorem’s left-hand side            that the right-hand side holds. In particular, we consider a transi-
of the implication. We proceed by a case distinction on the last rule           tion that executes command send (𝑒). According to the operational
applied, and may assume the theorem (i.e., our induction hypothe-               semantics, only the transition rule Local with an application of the
sis) for this rule’s premises. In our proof sketch we focus on a few            Send rule in its premise is applicable and modifies the command in
interesting cases – send, sequential composition, and fork – and                the 𝑖th component’s configuration. This allows us to conclude that
we present these cases further down, as individual lemmas. Send                 the considered transition must have the following shape:
is interesting because it illustrates a trace-updating proof rule, for                             −−−−→               −−−−−−→
                                                                                                  ⟨ ⟨𝐶, 𝜎⟩, 𝑘𝑎 , 𝜏⟩ → ⟨ ⟨𝐶 ′, 𝜎 ′ ⟩, 𝑘𝑎′ , 𝜏 ′ ⟩
which we have to show that the trace invariant is maintained. The
challenge for sequential composition is to show that our definition             where
of configuration safety allows us to prove that each transition in                              |𝐶®′ | = |𝐶®| ∧ 𝑘𝑎′ = 𝑘𝑎 ∧ 𝜏 ′ = 𝜏 + Send (𝑒 (𝜎)) ∧
the system maintains the trace invariant. The Fork proof rule is
of interest because it is the only command that extends the system                              𝐶®𝑖′ = 𝜖 ∧ 𝜎®𝑖′ = 𝜎®𝑖 [snap ↦→ 𝜏 + Send (𝑒 (𝜎))] ∧
configuration with additional components.                                                       (∀𝑗 . 𝑖 ≠ 𝑗 =⇒ 𝐶®′𝑗 = 𝐶®𝑗 ∧ 𝜎®′𝑗 = 𝜎®𝑗 )
    We begin by sketching the proofs for several auxiliary lemmas
about configuration safety that will be useful later on.                        and 𝜌 (𝜏) ∧ prefix (snap(𝜎®𝑖 ), 𝜏) holds. We have to prove that (1)
                                                                                𝜌 (𝜏 ′ ), (2) prefix (𝜏, 𝜏 ′ ), (3) prefix (snap(𝜎®𝑖′ ), 𝜏 ′ ), (4) 𝑘𝑎 ⊆ 𝑘𝑎′ , and (5)
   Lemma 3. The empty command satisfies configuration safety given
that the predicate 𝑄 holds.                                                     safe (𝑖, 𝐶®′, 𝜎®′, 𝑄, 𝜏 ′ ) hold. Note that no additional local configura-
                                                                                    𝑛       𝑖     𝑖
                                                                                tions have been added by this command because |𝐶®′ | = |𝐶®| holds.
              ∀𝑛, 𝑖, 𝜎, 𝑄, 𝜏 . 𝑄 (𝜎) =⇒ safe𝑛 (𝑖, 𝜖, 𝜎, 𝑄, 𝜏)
                                                                                (1) follows directly by definition of Def. 10. (2) holds by choosing
   Proof sketch. We show for arbitrary 𝑛, 𝑖, 𝜎, 𝜏, and assuming                 𝑝 = Send (𝑒 (𝜎)) as witness in Def. 7. (3) holds by reflexivity (cf.
𝑄 (𝜎), that safe𝑛 (𝑖, 𝜖, 𝜎, 𝑄, 𝜏) holds. Case (𝑖) from the definition of        Lemma 1). (4) holds because the attacker knowledge is unchanged.
safe holds straightforwardly. Case (𝑖𝑖) is satisfied because there is           Finally, (5) follows from Lemma 3 via the following derivation to
no transition starting in command 𝜖 and resulting in a different                obtain 𝑄 (𝜎®𝑖′ ):
command. Hence, this case vacously holds.                             □
                                                                                         ∀𝑝. 𝑄 [snap + 𝑝 + Send (𝑒)/snap] (𝜎®𝑖 )
   Lemma 4. A command 𝐶 satisfying configuration safety for 𝑛 exe-                          =⇒ 𝑄 [𝜏 + Send (𝑒)/snap] (𝜎®𝑖 )
cution steps is safe to execute for fewer execution steps.
                                                                                            ⇐⇒ 𝑄 (𝜎®𝑖 [snap ↦→ 𝜏 + Send (𝑒 (𝜎®𝑖 ))]) ⇐⇒ 𝑄 (𝜎®𝑖′ )
            ∀𝑚, 𝑛, 𝑖, 𝐶, 𝜎, 𝑄, 𝜏 . 𝑚 ≤ 𝑛 ∧ safe𝑛 (𝑖, 𝐶, 𝜎, 𝑄, 𝜏)
                                                                                where the implication is justified by the fact that prefix (snap(𝜎®𝑖 ), 𝜏)
              =⇒ safe𝑚 (𝑖, 𝐶, 𝜎, 𝑄, 𝜏)
                                                                                holds.                                                                  □
   Proof sketch. Straightforward induction on 𝑚.                      □
                                                                                Seq. In the case where the last rule applied in our proof tree is Seq,
   Next, we present soundness lemmas for the aforementioned                     we may assume the induction hypothesis for the rule’s premises,
interesting proof rules: send, sequential composition, and fork.                i.e., |= [𝑃] 𝑆 1 [𝑅] and |= [𝑅] 𝑆 2 [𝑄]. Soundness for this case, i.e.,
Send. Soundness for the proof rule Send directly follows from the               showing |= [𝑃] 𝑆 1 ; 𝑆 2 [𝑄], then follows from the following safety
following safety lemma:                                                         lemma:
   Lemma 5.                                                                        Lemma 6.
         ∀𝑛, 𝑖, 𝜎, 𝑄, 𝜏 . ext (Send (𝑒 (𝜎)), snap(𝜎)) ∧                             ∀𝑛, 𝑖, 𝑆 1, 𝑆 2, 𝜎1, 𝑅, 𝑄, 𝜏 . safe𝑛 (𝑖, 𝑆 1, 𝜎1, 𝑅, 𝜏) ∧
                       (∀𝑝. 𝑄 [snap + 𝑝 + Send (𝑒)/snap] (𝜎))                               (∀𝑚, 𝜎2, 𝜏 ′ . 𝑚 ≤ 𝑛 ∧ 𝑅(𝜎2 ) =⇒ safe𝑚 (𝑖, 𝑆 2, 𝜎2, 𝑄, 𝜏 ′ ))
           =⇒ safe𝑛 (𝑖, send (𝑒), 𝜎, 𝑄, 𝜏)                                            =⇒ safe𝑛 (𝑖, 𝑆 1 ; 𝑆 2, 𝜎1, 𝑄, 𝜏)



                                                                           20
     A Generic Methodology for the Modular Verification of Security Protocol Implementations (extended version)             CCS ’23, November 26–30, 2023, Copenhagen, Denmark


 1     func main ( num_initiators , num_responders int ) {                                            for 𝑛, we obtain safe𝑛 (𝑖, 𝑆 1′ ; 𝑆 2, 𝜎𝑖′, 𝑄, 𝜏 ′′ ). Thus, we showed
 2       ... // initialization code
 3       while ( num_initiators > 0) {
                                                                                                      safe𝑛+1 (𝑖, 𝑆 1 ; 𝑆 2, 𝜎𝑖 , 𝑄, 𝜏).
 4         fork ( initiator_args ) {                                                                                                                                       □
 5            initiator ( initiator_args )
 6         }
 7         num_initiators := num_initiators - 1
                                                                                              Fork. Soundness of the Fork proof rule follows from the following
 8       }                                                                                    safety lemma:
 9       while ( num_responders > 0) {
10         fork ( responder_args ) {                                                             Lemma 7.
11            responder ( responder_args )
12         }                                                                                    ∀𝑛, 𝑖, 𝑥,
                                                                                                       ® 𝑆 1, 𝑆 2, 𝜎1, 𝑄, 𝜏 . safe𝑛 (𝑖, 𝑆 1, 𝜎1, 𝑄, 𝜏) ∧
13         num_responders := num_responders - 1                                                                               ®
14       }                                                                                               (∀𝑗, 𝜎2 . [𝜎1 ∼ 𝜎2 ] 𝑥∪snap =⇒ safe𝑛 ( 𝑗, 𝑆 2, 𝜎2, True(), 𝜏))
15       fork () { attacker () }
16     }                                                                                          =⇒ safe𝑛 (𝑖, fork (𝑥)
                                                                                                                     ® {𝑆 2 }; 𝑆 1, 𝜎1, 𝑄, 𝜏)
                                                                                                               ®
                                                                                              where [𝜎1 ∼ 𝜎2 ] 𝑥∪snap denotes that 𝜎1 maps the variables in 𝑥® and
     Figure 17: Sketch of a program 𝐶 system bootstrapping the dis-                           variable snap to the same values as 𝜎2 does.
     tributed system by first executing sequential initialization
     code to, e.g., generate public/private keypairs and then fork-                              Proof sketch. We perform induction on 𝑛 and use the follow-
     ing several instances of an initiator and responder implemen-                            ing induction hypothesis:
     tation and the highly non-deterministic attacker implemen-                               IH (𝑛) ≜ ∀𝑖, 𝑥,
                                                                                                           ® 𝑆 1, 𝑆 2, 𝜎1, 𝑄, 𝜏, .
     tation. initiator_args and responder_args are abbreviations
                                                                                                            safe𝑛 (𝑖, 𝑆 1, 𝜎1, 𝑄, 𝜏) ∧
     for a list of arguments that are passed to the initiator and
                                                                                                                                 ®
     responder implementations, respectively. E.g., the initiator’s                                         (∀𝑗, 𝜎2 . [𝜎1 ∼ 𝜎2 ] 𝑥∪snap =⇒ safe𝑛 ( 𝑗, 𝑆 2, 𝜎2, True(), 𝜏))
     public/private keypair and the responder’s public key might                                           =⇒ safe𝑛 (𝑖, fork (𝑥)
                                                                                                                              ® {𝑆 2 }; 𝑆 1, 𝜎1, 𝑄, 𝜏)
     constitute initiator_args.
                                                                                              For 𝑛 = 0, safe0 (𝑖, fork (𝑥)
                                                                                                                         ® {𝑆 2 }; 𝑆 1, 𝜎1, 𝑄, 𝜏) holds by definition. In
        Proof sketch. We perform induction on 𝑛 using the following                           the induction step, we assume 𝐼𝐻 (𝑛) to show 𝐼𝐻 (𝑛 + 1). We assume
     induction hypothesis:                                                                    the left-hand side, i.e.,
     IH (𝑛) ≜ ∀𝑖, 𝑆 1, 𝑆 2, 𝜎1, 𝑅, 𝑄, 𝜏, .                                                        safe𝑛+1 (𝑖, 𝑆 1, 𝜎1, 𝑄, 𝜏) ∧                                                 (1)
                   safe𝑛 (𝑖, 𝑆 1, 𝜎1, 𝑅, 𝜏) ∧                                                     (∀𝑗, 𝜎2 . [𝜎1 ∼ 𝜎2 ]   ®
                                                                                                                         𝑥∪snap
                                                                                                                                   =⇒ safe𝑛+1 ( 𝑗, 𝑆 2, 𝜎2, True(), 𝜏))        (2)
                   (∀𝑚, 𝜎2, 𝜏 ′ . 𝑚 ≤ 𝑛 ∧ 𝑅(𝜎2 ) =⇒ safe𝑚 (𝑖, 𝑆 2, 𝜎2, 𝑄, 𝜏 ′ ))              and seek to show safe𝑛+1 (𝑖, fork (𝑥)     ® {𝑆 2 }; 𝑆 1, 𝜎1, 𝑄, 𝜏). Similar to
                  =⇒ safe𝑛 (𝑖, 𝑆 1 ; 𝑆 2, 𝜎1, 𝑄, 𝜏)                                           the proof of Lemma 5, the interesting case is (𝑖𝑖) in which we
     The base case (𝑛 = 0) holds by definition. In the induction step, we                     only consider the inference rule Fork. Based on the operational
     may assume IH (𝑛) to prove IH (𝑛 + 1). For arbitrary 𝑖, 𝑆 1 , 𝑆 2 , 𝜎1 ,                 semantics, we obtain
     𝑅, 𝑄, and 𝜏 we assume the left-hand side, i.e., safe𝑛+1 (𝑖, 𝑆 1, 𝜎1, 𝑅, 𝜏)                        (𝐶®𝑖′ = 𝑆 1 ) ∧ (𝜎1 = 𝜎®𝑖 = 𝜎®𝑖′ ) ∧ (|𝐶®′ | = |𝐶®| + 1) ∧
     and ∀𝑚, 𝜎2, 𝜏 ′ . 𝑚 ≤ 𝑛 + 1 ∧ 𝑅(𝜎2 ) =⇒ safe𝑚 (𝑖, 𝑆 2, 𝜎2, 𝑄, 𝜏 ′ ). It                                                h                  ®
                                                                                                                                             i 𝑥∪snap
     remains to prove that safe𝑛+1 (𝑖, 𝑆 1 ; 𝑆 2, 𝜎1, 𝑄, 𝜏) holds. The proof                           (𝐶®′ |𝐶®′ | = 𝑆 2 ) ∧ 𝜎1 ∼ 𝜎®′ |𝐶®′ |          ∧
     proceeds similarly to the proof of Lemma 5 except that in case (𝑖𝑖)
     the Local rule’s premise is fulfilled by an application of either the                                (∀𝑗 . 1 ≤ 𝑗 ≤ |𝐶®| =⇒ 𝜎®′𝑗 = 𝜎®𝑗 ) ∧
     Seq1 or Seq2 rule:                                                                                   (∀𝑗 . 1 ≤ 𝑗 ≤ |𝐶®| ∧ 𝑖 ≠ 𝑗 =⇒ 𝐶®′𝑗 = 𝐶®𝑗 )
         • Case Seq1: According to this transition’s premise, there ex-
            ists a transition ⟨𝑆 1, ⟨𝜎𝑖 , 𝜏⟩⟩ → ⟨𝜖, ⟨𝜎𝑖′, 𝜏 ′′ ⟩⟩ for some 𝜏 ′′ .             Since the attacker knowledge 𝑘𝑎 and global trace 𝜏 remain un-
            Thus, we obtain by definition of safe𝑛+1 (𝑖, 𝑆 1, 𝜎𝑖 , 𝑅, 𝜏) that                 changed by the application of this inference rule, we have to prove
            𝜌 (𝜏 ′′ ), prefix (𝜏, 𝜏 ′′ ), prefix (snap(𝜎𝑖′ ), 𝜏 ′′ ), 𝑘𝑎 ⊆ 𝑘𝑎′ , and          that (a) safe𝑛 (𝑖, 𝑆 1, 𝜎1, 𝑄, 𝜏) and (b) safe𝑛 (|𝐶®′ |, 𝑆 2, 𝜎®′ |𝐶®′ | , True(), 𝜏)
            safe𝑛 (𝑖, 𝜖, 𝜎𝑖′, 𝑅, 𝜏 ′′ ) hold. We distinguish two cases, namely                hold. (a) follows from applying Lemma 4 to safe𝑛+1 (𝑖, 𝑆 1, 𝜎1, 𝑄, 𝜏).
            𝑛 = 0 and 𝑛 > 0. In the first case, we obtain by definition                       Since (2)’s left-hand side is satisfied for 𝜎2 = 𝜎®′ |𝐶®′ | , we obtain
            safe0 (𝑖, 𝑆 2, 𝜎𝑖′, 𝑄, 𝜏 ′′ ). In the second case, we obtain by defi-             safe𝑛+1 (|𝐶®′ |, 𝑆 2, 𝜎®′ ®′ , True(), 𝜏) by instantiating the quantifier 𝑗
            nition of safe𝑛 (𝑖, 𝜖, 𝜎𝑖′, 𝑅, 𝜏 ′′ ) that 𝑅(𝜎𝑖′ ) holds. Therefore, we                                  |𝐶 |
            can instantiate 𝑚, 𝜎2 , and 𝜏 ′ with 𝑛, 𝜎𝑖′ , and 𝜏 ′′ , respectively,            with |𝐶®′ |. We also obtain (b) by applying Lemma 4.                              □
            in the quantifier above. Thus, we obtain safe𝑛 (𝑖, 𝑆 2, 𝜎𝑖′, 𝑄, 𝜏 ′′ ).
            This concludes the proof for both cases 𝑛 = 0 and 𝑛 > 0                           A.3      Trace Inclusion
            showing that safe𝑛+1 (𝑖, 𝑆 1 ; 𝑆 2, 𝜎𝑖 , 𝑄, 𝜏) holds.                             We can now show the desired trace inclusion (recall Sec. A), which
         • Case Seq2: This transition’s premise specifies that a tran-                        directly follows from Thm. 1.
            sition ⟨𝑆 1, ⟨𝜎𝑖 , 𝜏⟩⟩ → ⟨𝑆 1′ , ⟨𝜎𝑖′, 𝜏 ′′ ⟩⟩ for some 𝜏 ′′ exists. We
                                                                                                Theorem 2. If we boostrap the distributed system from a single
            apply the definition of safe𝑛+1 (𝑖, 𝑆 1, 𝜎𝑖 , 𝑅, 𝜏) to obtain 𝜌 (𝜏 ′′ ),
                                                                                              component, with no precondition, a trace invariant that holds for the
            prefix (𝜏, 𝜏 ′′ ), prefix (snap(𝜎𝑖′ ), 𝜏 ′′ ), 𝑘𝑎 ⊆ 𝑘𝑎′ , and
                                                                                              empty trace, and an initial attacker knowledge set, then the trace
            safe𝑛 (𝑖, 𝑆 1′ , 𝜎𝑖′, 𝑅, 𝜏 ′′ ). By applying the induction hypothesis

                                                                                         21
CCS ’23, November 26–30, 2023, Copenhagen, Denmark                                                         Linard Arquint, Malte Schwerhoff, Vaibhav Mehta, and Peter Müller


invariant always holds, regardless of how many transitions are per-                               In our verification case studies we prove Thm. 2 in three steps:
formed, and additional components (participants and the attacker)                             in step 1, we once-and-forall verify our reusable verification library,
are forked.                                                                                   including a most-general attacker implementation (an iterated non-
                                                                                              deterministic choice between all executable commands) against a
     ∀𝐶, 𝐶®′, 𝑄, 𝜎, 𝜎®′, 𝑘𝑎′ , 𝜏 ′ . ⊢ [True()] 𝐶 [𝑄] ∧ 𝜌 (∅) ∧
                                                                                              partially abstract (thus sufficiently general) trace invariant. I.e., the
                                                             −−−−−−→
                                    ⟨⟨𝐶, 𝜎⟩, 𝑘𝑎init , ∅⟩ →∗ ⟨ ⟨𝐶 ′, 𝜎 ′ ⟩, 𝑘𝑎′ , 𝜏 ′ ⟩        judgement ⊢ [𝑡𝑟𝑢𝑒] 𝐶𝑎 [𝑡𝑟𝑢𝑒] we obtain for the attacker holds for
                                                                                              all possible attackers and protocol-specific instantiations of this
        =⇒ 𝜌 (𝜏 ′ )
                                                                                              abstract trace invariant. In step 2, we implement each participant
where 𝑘𝑎init is the initial attacker knowledge consisting of all public                       in its own program 𝐶𝑖 ; verifying these effectively yield a judge-
terms.                                                                                        ment ⊢ [𝑃𝑖 ] 𝐶𝑖 [𝑄𝑖 ] per participant.
                                                                                                  In step 3, we combine these separate judgements for the protocol
   Proof sketch. We prove this theorem by first applying sound-
                                                                                              participants and the attacker by constructing a program 𝐶 system that
ness of our proof rules (Thm. 1) and expanding Def. 8 because all
                                                                                              first performs some sequential initialization code and then forks sev-
states 𝜎 satisfy True(). We proceed by induction over the length
                                                                                              eral instances of protocol participants and the attacker, as illustrated
of transition sequences. Since the trace invariant holds initially, is
                                                                                              in Fig. 17. By taking the number of participant instances as uncon-
maintained by each transition, and each command in every compo-
                                                                                              straint input parameters, we obtain a result for unboundedly-many
nent of the system satisfies configuration safety, we obtain 𝜌 (𝜏 ′ ) for
                                                                                              instances. Functions and non-deterministic choices are straightfor-
every trace 𝜏 ′ that is possible after executing 𝑛 transitions, where
                                                                                              ward extensions to our programming language. The initialization
𝑛 is the induction variable.                                           □
                                                                                              code’s purpose is to establish the participants’ preconditions. E.g., in
   Thm. 2 implies the following trace inclusion property where 𝜙                              our NSL case study we implement initialization code that generates
is a security property implied by the trace invariant 𝜌, i.e., 𝜌 |= 𝜙:                        public-private keypairs and passes the relevant keys to the individ-
  ∀𝐶, 𝑄. ⊢ [True()] 𝐶 [𝑄] ∧ 𝜌 (∅) =⇒ Tr (𝐶) ⊆ Tr (𝜌) ⊆ Tr (𝜙)                                 ual protocol participants. In the case of WireGuard, the correspond-
                                                                                              ing initialization code remains an assumption, which is typical for
where Tr (𝐶) denotes the set of all traces that result from executing                         security protocol verification and corresponds to assuming that
arbitrary many transitions according to the small-step operational                            there exists a mechanism to authentically distribute public keys.
semantics. Tr (𝜌) and Tr (𝜙) are the sets of traces satisfying 𝜌 and
𝜙, respectively. I.e., Tr (𝜌) = {𝜏 | ∀𝜏 . 𝜌 (𝜏)} and Tr (𝜙) analogously.




                                                                                         22
