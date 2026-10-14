                                              AutoTam: Specifying Secure Protocol Implementations with
                                                             Tamarin Model Generation
                                                      Johannes Wilson                                 Mikael Asplund                             Niklas Johansson
                                                    Sectra Communications                           Linköping University                       Sectra Communications
                                                      Linköping, Sweden                              Linköping, Sweden                           Linköping, Sweden
                                                     Linköping University                           mikael.asplund@liu.se                       Linköping University
                                                      Linköping, Sweden                                                                          Linköping, Sweden
                                                    johannes.wilson@liu.se                                                                  niklas.johansson@sectra.com
                                         Abstract                                                                 in 2017, for which a security proof [39] was later made using the
                                         Formal verification is a challenging but important task for ensuring     Tamarin prover.
arXiv:2606.19937v1 [cs.CR] 18 Jun 2026




                                         the security of cryptographic protocols. While modern protocol              The Dolev-Yao model, while practical for verification, relies on
                                         verification tools significantly reduce verification effort, modelling   a highly abstract protocol model. Much effort has been spent on
                                         remains challenging to practitioners without a background in for-        designing methods to bridge the gap between symbolic models and
                                         mal verification. In addition, transferring verification results to a    concrete protocol implementations, providing verification of high-
                                         concrete protocol implementation requires expert knowledge.              level protocol security properties also for implementations. Despite
                                             In this paper, we present a novel language-first method for ver-     the availability of advanced analysis tools and methods applicable to
                                         ification of trace properties using a domain-specific language for       a wide variety of protocol implementations, industrial application
                                         protocol implementations. We target the Tamarin prover for verifi-       remains low. This in part because the required verification expertise
                                         cation, and we prove that verified universal trace properties trans-     is significant. To improve adoption in industry, methods must be
                                         late back to the implementation. We additionally integrate symbolic      streamlined further in order to minimise the needed expertise.
                                         execution in order to analyse the memory safety of protocol imple-          To streamline verification and minimize effort, while retaining a
                                         mentations. We use our tool to implement and generate accurate           well-defined relationship with the formal model, a new approach
                                         models for a signed Diffie-Hellman protocol, and for the WireGuard       is needed. We propose a novel language-first approach, where the
                                         VPN protocol. Our WireGuard implementation is interoperable with         symbolic Dolev-Yao model and implementation language are tied
                                         existing implementations when using our interpreter, and achieves        together through the use of a domain-specific language. We moti-
                                         acceptable performance. We formally prove our implementations            vate this in three ways. Firstly, a language designed to align with
                                         secure using a combination of symbolic execution and verification        the abstraction level of high-level security properties ensures that
                                         of the generated Tamarin models.                                         there is a clear connection to the verified properties, creating for-
                                                                                                                  mal guarantees which are more easily understood. Secondly, an
                                         CCS Concepts                                                             appropriately designed language ensures that entire implementa-
                                                                                                                  tions can be symbolically modelled, including implementation state
                                         • Networks → Protocol testing and verification; • Security and
                                                                                                                  machines, as opposed to only verifying core segments like message
                                         privacy → Security protocols; • Software and its engineering
                                                                                                                  parsing or formatting. This limits the need for expertise during the
                                         → Domain specific languages.
                                                                                                                  implementation phase to align the code with verification. Finally, a
                                                                                                                  protocol-domain-specific language can naturally encode the sym-
                                         Keywords
                                                                                                                  bolic model, allowing automatic and sound translation to a model,
                                         Protocol Verification, Cryptographic Protocols, Symbolic Protocol        only requiring formal method expertise at the verification phase
                                         Models, Model Extraction, Software Verification                          itself.
                                                                                                                     The most similar existing approaches perform model extraction
                                         1   Introduction                                                         from a general-purpose language [3, 16, 17, 19, 21, 47]. Typically,
                                         Cryptographic protocols are vital to the security of network com-        limits on loops and recursion must be imposed to retain a tractable
                                         munication. The design of secure protocols has proven difficult,         model, and as a consequence most approaches leave some parts
                                         as demonstrated by numerous vulnerabilities discovered in both           of the protocol state machine to manual modelling assumptions.
                                         proposed and deployed protocols, such as in the original Needham-        We argue that for an implementation, it is desirable to addition-
                                         Schroeder protocol [51], prior versions of SSL/TLS [22], the EMV         ally verify the state machine, considering that historical protocol
                                         standard [10], and many others. To address these challenges, sym-        vulnerabilities such as SKIP [12] were caused by incorrectly imple-
                                         bolic protocol verification based on a Dolev-Yao model [37] was          mented state machines. ProScript explicitly disallows all forms of
                                         developed as a method to formally verify security properties of          recursion or loops [47], while for SPS, the input language implicitly
                                         protocols, proving security against strong attackers for a wide class    requires a linear protocol [3]. This limits the use of the tools to
                                         of attacks. These methods can enjoy a great deal of automation,          only verification of linear handshakes, and not repeatable message
                                         thanks to the development of several automated verification tools        steps such as transport phases, nor more complex stateful protocols.
                                         such as Tamarin [54] and ProVerif [23]. Today, the security of new       While in theory fs2pv [19] does not forbid recursion, recursion is
                                         proposed protocols is often argued using verifiable symbolic mod-        discouraged for verification reasons and none of its case studies
                                         els, as was done with the WireGuard VPN protocol [38] proposed
                                                                                                Johannes Wilson, Mikael Asplund, and Niklas Johansson


apply the tool to a non-linear protocol. Defensive JavaScript [17]        safe behaviour of our language interpreter or protocol implemen-
allows loops but faces other challenges in terms of generated model       tations, since they can both be analysed using symbolic execution
size [47]. The verification framework hax [16, 21] provides auto-         for memory safety.
matic translation from annotated Rust functions to ProVerif. In this
framework, a scenario, i.e. the initialisation of both roles, must be     1.1    Contributions
manually added to the resulting model.                                    We can summarize the contributions of our work as follows:
   In this paper, we present AutoTam, which consists of a domain-             • We describe the design of the AutoTam language, a domain-
specific language in which protocol implementations can be written,              specific language for cryptographic protocols which is fully
symbolic models for verification can be extracted, and automated                 executable by our interpreter.
testing using symbolic execution can be performed. Using our tool,            • We present our procedure for extracting Tamarin models
much of the task of producing a secure protocol implementation                   from the executable implementations, and provide a sound-
can be concentrated to writing the protocol implementation in                    ness proof of the translation.
AutoTam. The tool is not limited to linear protocols. In fact, we             • We present two case studies on using our language and tool
are able to encode arbitrary finite state machines to describe the               to implement, extract models for, and prove the security
message order. This guarantees we can also specify the unbounded                 of a signed Diffie-Hellman key exchange protocol and the
transport phases of protocols.                                                   WireGuard VPN protocol.
   Compared to existing work, our approach is novel. Protocols can            • We provide a fully integrated symbolic library for perform-
largely be defined by their protocol state-machine specifying what               ing analysis of implementations using symbolic execution,
messages to accept in each state and how to transition between                   allowing us to rule out most types of memory errors in our
states, the parsing and message serialisation for each message, and              case study protocols.
the cryptographic operations to be performed in each state. We
design our high-level domain-specific language with these compo-          2     Background
nents in mind, ensuring we can concisely encode each part in a
way that follows the imperative style code that developers are used       In this section we give a short introduction to the ideas of symbolic
to. The resulting AutoTam protocol descriptions concisely describe        protocol verification and the Tamarin prover, a cryptographic pro-
implementation behaviour with enough detail to serve as reference         tocol verifier in the symbolic model which uses heuristics to find
implementations. We implement an interpreter for executing the            proofs or counterexamples to security properties.
protocol descriptions directly to allow for interoperability testing.
For verification, we implement a process for translating a set of
                                                                          2.1    Symbolic Protocol Verification
AutoTam protocol descriptions into a Tamarin model. We have               Symbolic protocol verification follows work originally by Dolev and
spent considerable effort into designing a translation that is both       Yao [37] where cryptographic functions are represented symboli-
sound and produces readable and verifiable models.                        cally and the adversary is modelled as an active network adversary.
   We believe our tool will be useful during the development of new       In contrast to a computational model, a symbolic model does not
protocols. Once AutoTam protocol role descriptions are written,           model concrete bitstrings. Instead, messages, variables, role names
symbolic verification of security properties for confidentiality and      and keys are all represented as abstract terms, making verification
authenticity comes largely for free, as the tool produces verification-   much more amenable for automation.
ready Tamarin models. Our soundness property relates such prop-              Each protocol role will describe a series of steps, where each
erties back to the protocol descriptions. Furthermore, our tool can       step may interact with the global protocol trace. In the Dolev-Yao
provide templates for common security properties, providing a             model [37], the adversary is an active network adversary and may
way to automatically add them to the generated Tamarin model.             intercept, remove, duplicate, and construct its own messages on the
This makes it easy for users to verify common confidentiality and         network. Security properties can be formulated as trace properties
authenticity properties.                                                  on the global network trace. For example, secrecy properties can
   Our language is designed with the soundness of translation in          be expressed as claims that no possible trace exists where the ad-
mind. Our soundness property states that a trace property proven          versary will be able to directly derive a message term which was at
in the generated model translates to a proof that the property holds      some point believed to be secret. A proof of such a property must
also during execution. We provide a proof of the soundness of this        then show that no matter the order in which the protocol roles
translation under standard assumptions on cryptography accord-            perform the protocol, and no matter how the adversary modifies
ing to the Dolev-Yao [37] symbolic protocol model. Appropriately          or constructs messages, the property always holds. Such verifi-
selected security properties can rule out a large number of imple-        cation problems are known to be undecidable in the general case
mentation errors, including state-machine bugs.                           when protocol participants can generate new unique values [42, 55].
   Finally, we fully integrate with a dynamic symbolic execution          Therefore, automated provers must rely on heuristics or perform
engine in a way that allows automated analysis of implementations         bounded verification.
written in AutoTam. In our case studies, this analysis produces
complete coverage tests of the implementations when receiving             2.2    Tamarin
arbitrary network input. This way, we do not have to assume the           Tamarin is a state-of-the art symbolic protocol verification tool
                                                                          which has been used in formal verification of several important
                                                                          security protocols, such as TLS [34, 35], the EMV standard [10],
AutoTam: Specifying Secure Protocol Implementations with Tamarin Model Generation


and 5G Key-Agreement [33]. Tamarin can perform unbounded
verification, meaning properties can be verified for an arbitrary
number of protocol runs. Tamarin provides a very general way
to model stateful protocols in the form of multiset rewrite rules,
where each rewrite rule may affect the global trace and adversary
knowledge [53].
   We write a rewrite rule on the form [l]-[a]->[r], where multi-
sets l and r, containing terms known as facts, represents the pre-
and post-condition of the rule, while the multiset a contains terms
known as actions, describing events visible on the global protocol
trace. Application of a rule requires that there exists some instanti-
ation of the variables in l which matches available state facts of the
global protocol state.                                                                     Figure 1: AutoTam Architecture and Workflow.
   Cryptographic operations are modelled according to an equa-
tional theory, for example describing the relationship between en-
crypted and decrypted terms. The network channel is modelled
using special facts In and Out whose contents describe the input and
output from the network respectively. The adversary may perform
any publicly known operations such as encryption and decryp-                        Figure 1. AutoTam operates in three modes: interpreter mode, trans-
tion as described by the equational theory of the model. Tamarin                    lation mode, and symbolic execution mode. In interpreter mode,
supports types to distinguish public variables, prefixed with a $                   an AutoTam protocol role description written in the AutoTam lan-
character or within single quotes in case of a constant, and fresh                  guage is parsed and executed, while in translation mode AutoTam
variables, prefixed with a ∼ character. Public variables are known                  protocol role descriptions are translated to a Tamarin model. In
to the adversary, while fresh variables may only be generated by                    symbolic execution mode, we use the KLEE dynamic symbolic ex-
the rule Fr. Fr allows modelling uniquely generated numbers and                     ecution engine [24] to generate high-coverage test cases for the
private keys. We show an example Tamarin rule below.                                protocol implementation when executed by our interpreter.
                                                                                       An AutoTam protocol role description describes the control flow,
rule RuleName:                                                                      cryptographic operations, and network operations performed by a
    let c = <a, ~b> in                                                              role in the protocol. The protocol role description files are written
    [ In(a), Fr(~b) ]                                                               in the AutoTam language. We present the syntax and execution
    --[ ActionName(a, ~b) ]->                                                       semantics of the AutoTam language in Section 4. In interpreter
    [ StateNext(c), Out(c) ]                                                        mode, AutoTam will accept a single protocol role description file,
   The rule accepts some term a from the network and generates                      describing one of the protocol roles. During execution, AutoTam
some fresh term ∼b. A term c is defined as the concatenation of a                   will interface with the user through a message passing mechanism,
and b. The term c is stored in a produced state fact StateNext, and                 and with the network through calls to system libraries for reading
also output to the network. The rule also produces an action fact                   and writing socket file descriptors.
ActionName. An action fact is not part of the state but is rather used                 In translation mode, described in detail in Section 5, AutoTam
to track the protocol trace. The action fact ActionName associates                  may instead accept several protocol role description files that to-
an application of the rule RuleName with its terms a and b.                         gether describe all roles in the protocol. In addition, Tamarin lem-
   In Tamarin, security properties are specified as guarded first                   mas can be built using pre-defined templates for secrecy and au-
order logic formulas on action facts and timepoints. This property                  thenticity properties. The protocol role description files will then
specification language allows specifying very general authentica-                   be translated into a single Tamarin file ready for verification.
tion and secrecy properties. Such formulas are called lemmas within                    Symbolic execution mode, described in Section 6, is achieved by
Tamarin. A special type of lemma known as a restriction can en-                     compiling the AutoTam interpreter into LLVM bytecode for analy-
force protocol invariants, which may be used in order to implement                  sis using the dynamic symbolic execution engine KLEE [24]. The
equality and inequality of terms appearing in rules. We will use                    execution traces of the interpreter executing an AutoTam proto-
two special action facts, Eq and NEq, both with arity two, in order to              col role description file can then be systematically explored under
signify that two terms appearing in a rule must be equal or distinct,               simplifications of the cryptographic operations using KLEE.
respectively.
                                                                                    4   AutoTam Language
3    AutoTam Overview                                                               In this section we present the syntax and semantics of the AutoTam
AutoTam is a tool for both interpreting our own domain specific lan-                language. The AutoTam language is protocol domain specific. The
guage, the AutoTam language, and for generating Tamarin models                      language is designed to be both simple and intuitive, yet expressive
from the same language. We now proceed to present the features of                   enough to implement modern cryptographic protocols. We design
the AutoTam domain specific language and the AutoTam tool. An                       our language to support arbitrary protocol state machines while
overview of the AutoTam architecture and its workflow is shown in                   maintaining a natural translation into a symbolic model.
                                                                                                  Johannes Wilson, Mikael Asplund, and Niklas Johansson


4.1    Language Control Flow
Our language design is focused specifically to provide a natural
way to describe the state machines of protocols, since complex-
ity in protocol state machines can be a cause of implementation
errors [12].
    To ensure we can soundly extract a model from our implementa-
tion, we limit control-flow to a high-level protocol state machine
only, avoiding undecidable reachability problems when extracting
the possible input-output relations of messages. This does not in
general limit the number of protocols which are possible to imple-
ment using our language, since any intra-procedural choice can be
implemented as a choice that is part of the protocol state machine.        Figure 2: Illustration of AutoTam States and Transitions
    An AutoTam protocol role description consists of states and tran-
sitions. These states and transitions in turn contain sequences of
statements. The transitions encode the state machine of a protocol.      is the mechanism by which it is possible to specify the conditions
A state may connect with multiple outgoing and incoming transi-          under which a transition should or should not be taken.
tions. We allow the resulting protocol state machine to form cycles,         Typically, each transition would start by parsing a message re-
as this is necessary for implementing protocol transport phases.         ceived in the preceding state. If multiple messages with different
The statements of the states and transitions describe the operations     formats may be received at some point in the protocol, then each
to perform during execution. The states are further divided into         message would have its own transition, and during execution each
two parts, an output part and an input part. The general syntax is       of them would be tried. We may view the transitions as providing
shown in Listing 1. A formal description of the syntax is given in       the branching control flow of our language, but at the abstraction
Listing 7 in the Appendix.                                               level of the protocol. On the other hand, if an error is encountered
                                                                         during the execution of a state, it is unrecoverable and execution
[ StateName ] {
                                                                         will terminate.
     Output {
          [ Statements ]
                                                                             We exemplify the traces from Figure 2. With state names writ-
     }                                                                   ten as 𝐴𝑂 for output part of state A, and 𝑇𝐴𝐵 for the transition
     Input {                                                             from A to B, an example execution trace could proceed as follows:
          [ Statements ]                                                 [𝐴𝑂 , 𝐴𝐼 ,𝑇𝐴𝐵 , 𝐵𝑂 , 𝐵𝐼 ,𝑇𝐵𝐷 , 𝐷𝑂 , 𝐷 𝐼 ]. Alternatively, if an error occurs
     }                                                                   during execution of transition 𝑇𝐴𝐵 , execution may instead proceed
}                                                                        as [𝐴𝑂 , 𝐴𝐼 ,𝑇𝐴𝐵 ,𝑇𝐴𝐶 , 𝐶𝑂 , 𝐶𝐼 ,𝑇𝐶𝐷 , 𝐷𝑂 , 𝐷 𝐼 ], where 𝑇𝐴𝐵 is not fully ex-
Transition ([ FromState ] , [ ToState ]) {                               ecuted.
     [ Statements ]                                                          To retain soundness during the translation to a Tamarin model
}                                                                        which we will present in Section 5, we must impose the following
                                                                         requirements on valid AutoTam programs. These restrictions ensure
                   Listing 1: AutoTam Syntax
                                                                         that a model can fully capture the behaviours of the executable
                                                                         program and are necessary for our soundness proof in Section 5.3.
   The program may only transmit messages over the network
in the output part of a state and may only receive input in the             Reqirement 1. A transition cannot assign values to variables
input part. States must be structured so that the output part lies       which are live (in the usual meaning of variable liveness, see e.g. [2])
before the input part. Such restrictions on the placement of network     at the beginning of another transition starting from the same state,
operations ensure that each transition in the program code can be        as they may get overwritten on failure.
safely translated into a single rule which represents a given protocol
step. The procedure for translation will be described in Section 5.         Reqirement 2. The output part of a state cannot contain state-
   We illustrate how the states and transitions build up the program     ments which may encounter non-network errors, including equality
control flow in Figure 2. In the figure, the output part and input       tests, AEAD decryption MAC validation, and signature verification.
parts of states are represented by the blue left and orange right
semicircles respectively. The transitions are represented by the         4.2    Variables and Functions
white arrows. The gray boxes which cover both parts of states and        Rather than providing a set of primitive types and operations on
transitions represent a list of statements which should be executed      these types, our language operates directly on the abstraction level
for each part of the program. Such lists may be empty.                   of cryptographic operations and network operations. The only
   A failure during the execution of a transition, for example a         typing in the language exists to track the sizes of variables, so that
failure to parse a message according to a message format, will           only variables of the correct size are used in functions as part of
end the execution of the transition, returning the execution of the      ensuring memory safety at runtime.
program to before the transition. The interpreter will then attempt         All statements in the language consist of a call to some prede-
to execute any alternative transitions which are available from the      fined function. A function may assign multiple variables and take
state, following in the order that the transitions are defined. This     some other variables as parameters. All statements have the form
AutoTam: Specifying Secure Protocol Implementations with Tamarin Model Generation


v1,...,vn = FunctionName(p1,...,pm) where variables v1 - vn                         pre-defined functions, we refer to the left-hand side of Table 10 in
are assigned by the function, while p1 - pm are function parameters.                the Appendix.
   Available functions in the language describe either operations on
network I/O, cryptographic operations, message operations such as                   5     Translation to Tamarin
message concatenation or division, or user I/O operations. The func-                In Translation mode, AutoTam will take several protocol imple-
tions themselves are implemented as C functions. During execution                   mentation files written in the AutoTam language and generate a
the interpreter will first make sure that the sizes of parameters                   single complete Tamarin model which models the behaviour of all
and assigned variables are correct at runtime before calling the                    involved protocol roles and their interactions with the network.
appropriate function implementation from a lookup table. Listing 2                     In this section, we present the translation process from the Au-
shows an example code snippet with two states and a transition                      toTam language to Tamarin models, first describing the translation
between them.                                                                       of control flow in Section 5.1, and then presenting the translation
State1 {
                                                                                    of individual statements in Section 5.2. In Section 5.3 we present
    Input {                                                                         our soundness theorem and its proof.
         a = recv ( fd ,10)
    }                                                                               5.1    Translation to Rules
} Transition ( State1 , State2 ) {                                                  The execution semantics of the input language described in Sec-
    b , c = split (a , 5)                                                           tion 4 can be directly translated into the trace-based semantics of
    RequireSize (c , 5)
                                                                                    Tamarin. For each defined transition in the input language, our
} State2 {
    Output {
                                                                                    translator will output a single Tamarin rule. Translation to a rule is
         d = GenSecret (5)                                                          performed for an “extended transition”, which also includes the in-
         e = Concat (c , d )                                                        put part of the previous state and the output part of the succeeding
         send ( fd , e )                                                            state.
    }                                                                                   In the running example in Listing 2, a transition starts from
    Input {                                                                         State1, leading to State2. The translation of the transition from
         f = recv ( fd ,20)                                                         State1 to State2 will begin at the input part of State1, include all
    }                                                                               its statements, continue through all the statements in the transition,
}                                                                                   and finally conclude with the statements in the output part of
Listing 2: Running Example AutoTam Language Protocol                                State2. The resulting Tamarin rule is presented in Listing 3.
Role Description                                                                    rule Role1_State1_to_State2 :
                                                                                         let a = <b , c >
   We will use the code in Listing 2 as a running example through-                           e = <c , ∼d >
out the rest of the paper. In Listing 2, executing State1 would call                     in
the “recv” function, reading fd as a socket file descriptor, for at                      [ State1 ( fd ) , In ( a ) , Fr (∼d ) ]
most ten bytes. If completed without error, execution of State1                       - -[ A_Role1_State1_State2 (a ,b ,c ,∼d , e )] - >
would finish, and the interpreter would look for transitions starting                    [ State2 ( fd ,b ,c ,∼d , e ) , Out ( e ) ]
from State1. Assuming the transition State1 to State2 is the only
                                                                                        Listing 3: AutoTam Running Example Tamarin Output
transition, execution would continue in the transition by calling the
split function, followed by a length check. If the variables parsed                    In addition to the translated individual statements, the produced
both had the appropriate length of five bytes, the transition would                 rule includes state facts in the precondition and postcondition,
have successfully completed, transferring execution to State2. In                   and an action fact to add to the program trace, as the action facts
State2, a new random number of five bytes would be generated,                       are necessary for writing lemmas. For our running example, the
which would be concatenated with the five bytes of c parsed earlier,                generated precondition contains the state fact for State1, while
which would then be sent over the same socket. Finally, execution                   the postcondition contains the state fact for State2 in order to
of State2 concludes with waiting for the next 20 bytes from the                     maintain the execution trace semantics of the implementation.
socket.                                                                                The Tamarin state facts represent the point of execution in the
   For the implementation of the cryptographic functions, we used                   implementation right in the middle of each state, between execution
the Cryspen HACL Packages1 which builds upon the HACL [61, 66]                      of the output and input parts of each state. In Figure 2, these points
formally verified cryptographic library. The cryptographic func-                    are represented by the black vertical lines in the middle of states.
tions which we use in this paper are encryption and decryption                      In the example rule, the state fact State2 represents the point of
using the Chacha20 Poly1305 AEAD algorithm used by WireGuard,                       execution after executing the output part statements of State2 in
EC25519 Diffie-Hellman key derivation, Ed25519 signatures, and                      the implementation, but before executing any of the statements in
Blake2s hashes. Additional pre-defined functions which we provide                   the input part of State2 in Listing 2.
include message operations such as concatenation and splitting,                        As noted by Cheval et al. [29], the number of Tamarin rules in a
network I/O, and equality comparisons. For a list of all available                  model can have a significant impact on verification time, and sim-
                                                                                    ply joining together compatible rules can reduce verification time
1 https://github.com/cryspen/hacl-packages                                          considerably. In a sense, our tool naturally allows the optimisation
                                                                                                    Johannes Wilson, Mikael Asplund, and Niklas Johansson


Table 1: Example Translations. The complete translation                                                Table 2: Notation
table can be found in Appendix.
                                                                                 𝑖      Statement            𝑃      protocol role description
      Function call (AutoTam)        Translation (Tamarin)                       𝑆         State             Π      Scenarios of Descriptions
                                                                                 𝑇      Transition           𝑥          Execution State
      gx = EC25519PublicKey(x)       [SET] gx → ’g’ˆx
                                                                                 𝑝      Participant          𝑋       Global Execution State
      gxy = EC25519DH(x, gy)         [SET] gxy → gyˆx
                                                                                 𝐶       Scenario            𝑤𝑒         Execution Trace
      a = Blake2s_hash(b)            [SET] a → h(b)
                                                                                 𝑅         Rule              𝑤𝑟            Rule Trace
      x = GenSecret(SIZE)            [IN] Fr(∼x)
                                                                                 𝐹      Translation          𝜏𝑒        Traces of Scenario
      m = recv(fd, SIZE)             [IN] In(m)
                                                                                 𝑀     Rule Mapping          Ψ        Transition Sequence
      send(fd, m)                    [OUT] Out(m)
                                                                                                             𝜋          Traces of Rules
      a = concat(b, c)               [SET] a → ⟨b, c⟩
      t = timestamp()                [SET] t → $t
      RequireEq(a, b)                [ACTION] Eq(a, b)                      To ensure that unique terms have new names in the Tamarin
      RequireNEq(a, b)               [ACTION] Neq(a, b)                  model, the statements to be translated are first transformed to single
      x = Arg(SIZE)                  [IN] In(x)                          static assignment form [36]. Since there is no control flow within
      x = Arg_priv_dh(SIZE)          [IN] !DHLtk(∼x)                     each extended transition, the translation is trivial.
      x = Arg_pub_dh(SIZE)           [IN] !DHPk(x)
                                                                         5.3     Soundness of Translation
                                                                         We present a proof of the soundness of translation with respect
method described in the extended version [30]. Instead of produc-        to trace properties. The desired soundness property can be stated
ing a rule for each step of execution and then merging compatible        in terms of trace inclusion. Informally, any global trace of some
rules as far as possible while maintaining the trace semantics, our      protocol participants executing the protocol must have a corre-
language makes it natural to start with a large execution step and       sponding trace in the generated Tamarin model. Then, any proof in
only subdivide it where strictly necessary. Our own experience with      Tamarin stating that a given trace property holds for every trace in
generating a model for the WireGuard protocol seems to indicate          the model, proves that an equivalent trace property holds for any
that also the complexity of individual rules can have significant        scenario during concrete execution.
impact on verifiability, suggesting that sometimes it is favourable          The basic proof idea is to prove that a global execution trace
to divide large and complex rules into smaller parts, meaning there      of completed transitions matches a Tamarin trace where the cor-
might be a sweet spot for the ideal division of statements into rules.   responding rule for each transition is applied. We prove this by
Since our language allows the user so themselves decide where            proving that the set of transition traces is preserved when perform-
to create the divisions between states, it is possible to experiment     ing the various transformations described in Section 5.1.
with different divisions directly in the code.                               We make our proof in a symbolic model, treating program vari-
                                                                         ables as abstract terms rather than bitstrings. We assume a symbolic
5.2    Translation of Individual Statements                              adversary model, both at the level of our execution semantics and
All callable functions are implemented as both an executable im-         the semantics of the translated model. A treatment on the computa-
plementation and a Tamarin translation function. The translation         tional soundness of a symbolic model is out of scope for this work.
function defines how a statement in the AutoTam language should          The survey by Cortier et al. [32] provides an overview of works
be integrated into a Tamarin rule. Such a translation function may       on bridging the gap between symbolic and computational protocol
either syntactically replace the output variables with expressions,      models.
introduce an Out fact in the case of a send operation, introduce an          We introduce some notation as we formalise the execution se-
In fact in the case of a receive or user input function, introduce       mantics of AutoTam protocol role descriptions. We summarise
an Fr fact for a newly generated unique number, or introduce an          the main notation used in Table 2. An AutoTam protocol role de-
equality restriction action fact Eq or Neq.                              scription consists of states and transitions. A state 𝑆 consists of
   We show a list of representative translations in Table 1. A list      two sequences of statements 𝑆 = ([𝑖𝑂1, 𝑖𝑂2, ..., 𝑖𝑂𝑛 ], [𝑖 𝐼 1, 𝑖 𝐼 2, ..., 𝑖 𝐼𝑚 ]),
of additional available translations can be found in Table 10 in the     where the first sequence is the output part and the second is the in-
Appendix. The type of translation meant is indicated in brackets.        put part. A transition 𝑇𝑎𝑏 between states 𝑆𝑎 and 𝑆𝑏 consists of a pre-
[SET] type will replace occurrences of the left-hand-side variable to    ceding state, a sequence of statements, and a succeeding state 𝑇𝑎𝑏 =
the right-hand-side expression. The [ACTION] type adds an action         (𝑆𝑎 , [𝑖 1, 𝑖 2, ..., 𝑖𝑛 ], 𝑆𝑏 ). A protocol role description 𝑃 consists of a set
fact, typically used for equality restrictions. The [IN] and [OUT]       of states and a set of transitions 𝑃 = ({𝑆𝐼 , 𝑆𝑥 , 𝑆 𝑦 , 𝑆𝑧 , ...}, {𝑇𝐼𝑥 ,𝑇𝑥 𝑦 , ...}).
type adds facts to the precondition and postcondition, respectively,     We assume all our protocol role descriptions are syntactically valid
of a Tamarin rule. For example, the implementation of the function       and follow Requirement 1 and Requirement 2.
“EC25519-DH” computes the Elliptic-Curve group element from a                We introduce the notion of a participant, as an instance of an
secret x and a public key gy and stores it in variable gxy, while the    executing protocol role description, given globally unique values for
translation function syntactically replaces all occurrences of gxy       all private keys, and knowledge of public keys of other participants.
in the rule with the expression gyˆx which is Tamarin syntax for         We define a scenario 𝐶 for a set of protocol role descriptions as a
Diffie-Hellman group exponentiation.                                     group of participants, and denote the set of all scenarios for a given
AutoTam: Specifying Secure Protocol Implementations with Tamarin Model Generation


set of descriptions as Π. 𝐶 = {𝑝𝑎1 , 𝑝𝑏1 , 𝑝𝑐2, ...} ∈ Π({𝑃 1, 𝑃2, ...}), where
a participant 𝑝𝑛𝑚 is an instance of protocol role description 𝑃𝑚 . We
place no bound on the number of participants for any protocol role
description.
   An execution state 𝑥𝑎 of a participant 𝑝𝑎 is given by a statement
index 𝑝𝑐 within either a state or transition 𝐵, along with a set of
terms 𝑉 , each mapped to a variable in the protocol role description,
local to the participant: 𝑥𝑎 = (𝑝𝑐, 𝐵, 𝑉 ).
   A global execution state for a scenario is given by the collective
execution state of all participants, for example 𝑋 1 = (𝑥𝑎1 , 𝑥𝑏1 , 𝑥𝑐1 ). We             Figure 3: Transition Trace Inclusion Proof Steps.
define a global execution trace 𝑤𝑒 as a sequence of global execution
states starting from the initial state, where each next global execu-                  Lemma 3. The set of global traces for a scenario when partici-
tion state has executed one statement for one of the participants.                  pants follow a deterministic transition order is a subset of the set
We assume without loss of generality that concurrent executions                     of global traces for the same scenario when participants follow a
appear in the global trace in some arbitrary order. We denote the                   non-deterministic transition order.
set of admissible global traces for a scenario 𝐶 as 𝜏𝑒 (𝐶). We write
traces using arrow notation: 𝑤𝑒 = 𝑋 1 → 𝑋 2 → 𝑋 3 ∈ 𝜏𝑒 (𝐶).                           Proof. The addition of non-deterministic choice can only add
   We define the transition sequence as the sequence of fully com-                  additional possibilities, since the previous traces remain possible.
pleted transitions performed by a participant. We define a global                                                                                     □
transition sequence as the transition sequence of the global execu-
                                                                                        We define our translation function 𝐹 (𝑈 ) = (𝑅, 𝑀) for generat-
tion trace. We define a mapping Ψ from an execution trace to its
                                                                                    ing a Tamarin model using AutoTam as a function which takes
transition sequence, consisting of a sequence of all transitions in
                                                                                    a set of protocol role descriptions 𝑈 and outputs a set of rules
the trace which were executed completely.
                                                                                    𝑅 = {𝐾𝑠 , 𝑟 𝑎𝑏 , 𝑟 𝑎𝑏 , ...} and a mapping function 𝑀. 𝑅 contains a rule
   Before presenting our soundness theorem and its proof, we prove
                                                                                    for each transition which describes the cumulative effect of per-
lemmas with respect to the various translations made by AutoTam.
                                                                                    forming a complete extended transition, meaning a joined, output-
We first define a transition-truncated global execution trace as a
                                                                                    transition-input sequence of statements, in addition to a key-share
global execution trace with no partially completed transitions.
                                                                                    rule 𝐾𝑠 which provides unique private keys for each role. The trace
   Lemma 1. For any scenario 𝐶 and any execution trace 𝑤𝑒 ∈ 𝜏𝑒 (𝐶),                 mapping function 𝑀 maps each rule in a rule trace to its transition,
there exists a transition-truncated global execution trace 𝑤𝑒 ∗ ∈ 𝜏𝑒 (𝐶)            or skips if the rule is 𝐾𝑠 . For example, 𝑀 (𝐾𝑠 → 𝑟 𝑎𝑏 → 𝐾𝑠 → 𝑟𝑏𝑐 →
with the same global transition sequence Ψ(𝑤𝑒 ) = Ψ(𝑤𝑒 ∗).                          ...) = 𝑇𝑎𝑏 → 𝑇𝑏𝑐 → .... We write 𝜋 (𝑅) for the set of admissible rule
                                                                                    traces of 𝑅.
   Proof. We depend on Requirement 1. Assume the lemma is false.                        We now state our soundness theorem for the translation.
Then there must exist some scenario 𝐶 with a trace 𝑤𝑒 , that has                       Theorem 1. For any set of protocol role descriptions 𝑈 translated
no global trace 𝑤𝑒∗ ∈ 𝜏𝑒 (𝐶) without partially completed transitions                as 𝐹 (𝑈 ) = (𝑅, 𝑀), then for any scenario 𝐶 ∈ Π(𝑈 ) all global exe-
so that Ψ(𝑤𝑒 ) = Ψ(𝑤𝑒∗ ). There must then exist some transition 𝑇𝑥 𝑦                cution traces 𝑤𝑒 ∈ 𝜏𝑒 (𝐶) have a matching trace 𝑤𝑟 ∈ 𝜋 (𝑅) so that
performed in 𝑤𝑒 which was not possible without partial execution                    Ψ(𝑤𝑒 ) = 𝑀 (𝑤𝑟 )
of some transition 𝑇𝑥𝑧 . This implies that an executed statement in
𝑇𝑥𝑧 affected future execution of the program, or another partici-                      Proof. We illustrate the proof in Figure 3. Lemmas 1 and 2
pant. This contradicts Requirement 1, and our requirement that no                   together prove that for any execution trace 𝑤𝑒 ∈ 𝜏𝑒 (𝐶) there exists a
network-visible execution may occur during a transition.           □                global complete execution trace 𝑤𝑒# ∈ 𝜏𝑒 (𝐶) so that Ψ(𝑤𝑒 ) = Ψ(𝑤𝑒# ).
                                                                                    Lemma 3 proves that 𝑤𝑒# is a valid trace of 𝐶 even if executions
   We define a complete global execution trace as a global execution                of descriptions of 𝐶 allow nondeterministic choice of transition.
trace with no partially completed transitions or states, where all                  From our definition of 𝐹 the rules 𝑅 describe complete extended
participants complete the output part upon completing the pre-                      transitions which perform the identical effect of a transition in
ceding transition, and no input parts are completed without some                    a global complete execution trace with nondeterministic choice.
following transition being completed.                                               Thus, there is a valid trace 𝑤𝑟 ∈ 𝜋 (𝑅) with Ψ(𝑤𝑒 ) = 𝑀 (𝑤𝑟 ).
                                                                                                                                                        □
   Lemma 2. For any scenario 𝐶 and any transition-truncated global
execution traces 𝑤𝑒∗ ∈ 𝜏𝑒 (𝐶), there exists a complete global execution                Some details are omitted from our proof. We do not explicitly
trace 𝑤𝑒# ∈ 𝜏𝑒 (𝐶) with the same global transition sequence Ψ(𝑤𝑒∗ ) =               formalise how variables are mapped in rewrite rules, instead the
Ψ(𝑤𝑒# ).                                                                            proof relies on variables being mapped one-to-one, while in practice
                                                                                    the translation optimises the rewrite rules to only consider locally
   Proof. We give the full proof of Lemma 2 in Section E in the                     relevant variables. We also implicitly assume that the translation
Appendix. In short, we prove that removing input parts or adding                    table, describing the mapping of statements to a symbolic Tamarin
output parts to the execution cannot reduce the set of traces, lever-               model according to Table 10, soundly captures the behaviour of the
aging Requirement 2 to guarantee that execution of the output part                  concrete function implementations. We omit most of the details
is possible.                                                       □                about key-share of pre-distributed long-term keys, which is needed
                                                                                               Johannes Wilson, Mikael Asplund, and Niklas Johansson


for any participant to meaningfully execute the protocols, but is       in Section 4.2, we rely on the formally verified HACL library for
technically performed outside AutoTam execution. We assume the          cryptographic operations.
key-share rule 𝐾𝑠 models the key-share method. Finally, we omit the        Through this method we can systematically, and in the ideal case
description of the network adversary, as we assume the adversary        completely, explore the behaviour of our implementations when
model described in Section 2.1 across our models.                       executed using our interpreter. Since at any point the program
                                                                        would read network input we produce a new symbolic message, we
                                                                        gain complete coverage with respect to arbitrary network input.
5.4    Built-In Features
In addition to the translation described, there are several built-      7     Case Studies
in features which assist in creating Tamarin models which are           We perform two case studies. One on a signed Diffie-Hellman key-
readable and efficient. Let-bindings are automatically used in place    exchange protocol, and one on the WireGuard VPN protocol [38].
of expressions which are repeated across a generated rewrite rule,      We compare our generated WireGuard model with existing Tamarin
greatly improving readability. Lists are automatically unfolded in      models from the literature. We additionally conduct a performance
order to ensure soundness, since expressions such as ℎ(< 𝑎, <           evaluation of our WireGuard implementation. We measure through-
𝑏, 𝑐 >>) and ℎ(<< 𝑎, 𝑏 >, 𝑐 >) are treated as non-unifiable terms       put when running our implementation using our interpreter and
in Tamarin, despite both representing a hash applied to the same        compare to two existing WireGuard implementations: the official
sequence of terms 𝑎, 𝑏, 𝑐. This can be remedied by choosing to use      Linux kernel implementation and the official user-level Go imple-
either a left-associative or right-associative syntax throughout a      mentation. Our WireGuard implementation is interoperable with
model. We automatically translate all expressions of either form        both implementations, although some features are omitted from our
into fully unfolded form to improve readability, e.g. < 𝑎, 𝑏, 𝑐 >,      implementation such as DoS mitigation and timed renegotiation.
which in Tamarin is syntactic sugar for right-associative pairs.
    User provided private keys are automatically typed as private
                                                                        7.1    A Diffie-Hellman Key-exchange Protocol
terms in the generated Tamarin model. Some functions, such as
computing a timestamp, are modelled as public terms in place of         We study a Diffie-Hellman key-exchange (DH) protocol designed
timestamps. Typing of terms is automatically and soundly propa-         to establish a new ephemeral key between two endpoints which
gated across rewrite rules, by ensuring that the term has the given     have known long-term signing keys. We follow a version of DH
type in all rules which produce the incoming state fact.                similar to the one used in a case study by Arquint et al. [6]. The
    AutoTam additionally allows automatic generation of Tamarin         established keys are authenticated through a signature using the
lemmas for standard security properties such as injective agreement     long-term keys. The protocol is shown in Alice and Bob notation in
from Lowe’s hierarchy [52] and weak secrecy. The user only needs        Table 3, where roles are shown to the left, with the arrow denoting
to specify the name of the transitions which are to be used as events   the direction of the message sent going from sender to receiver.
in building the properties, and the names of agreement variables.       To the right of the colon the message fields are shown, with angle
                                                                        brackets denoting list structures, quoted characters referring to
                                                                        constants, and exponentiation representing Diffie-Hellman public
6     Symbolic Execution of Implementations                             key operations. We use curly brackets for signatures or encryption.
To gain additional confidence in the security of implementations,           The protocol has two roles, labelled A for the initiator role and
and to decreases the reliance on the security of our interpreter, we    B for the responder role. The protocol starts with an agent in the
integrate dynamic symbolic execution into AutoTam. We utilise the       initiator role sending a plaintext message containing a fix header
KLEE symbolic execution engine [24], and follow the method of           ’1’, its own unique 64-bit identifier I, the 64-bit identifier of another
Wilson and Asplund [65] for performing efficient symbolic execu-        agent R, and a new ephemeral Diffie-Hellman public key 𝑔𝑥 . A
tion of protocol implementations using KLEE. The method consists        responder which receives a valid message will compute its own
of replacing the concrete implementations of cryptographic func-        public key 𝑔 𝑦 and sign a response message with the header ’2’,
tions with symbolic function abstractions, treating network input       the identifiers, and the public keys using its own long-term key
as fully symbolic, and delaying concretization of message lengths as    ltkB. The header ’10’, the message, and the computed signature
far as possible during analysis. In addition, the common “memcmp”       is sent as a response. Finally, the Initiator will compute its own
function from the standard C library is given a special function        signed response message but with the header ’3’ in similar fashion.
abstraction. Through this method, it is possible to prove that an       Upon completion both agents may compute the same value of 𝑔𝑥 𝑦 ,
implementation does not access memory outside of the largest            completing the key-exchange.
symbolic length of buffers when executed through our interpreter,
ruling out severe memory errors. Moreover, symbolic execution           7.2    The WireGuard VPN Protocol
can be extended to support other analyses such as conformance           WireGuard is a protocol designed to provide encryption for IP pack-
tests, see e.g. [7, 28, 64].                                            ets suitable for secure VPN services, similar to IPsec or OpenVPN.
   We have implemented function abstractions for all cryptographic      The WireGuard protocol operates on top of UDP, where the IP
functions available in our language. We use function abstractions       messages to send are encrypted and appended to a short message
which return symbolic data instead of performing cryptographic          header. To establish the keys to use for encryption, a handshake
operations. This way we may still explore the behaviour assuming        is first performed. The handshake is based on the IKpsk2 protocol
any output from cryptographic functions is possible. As discussed       from the Noise framework [60]. The protocol is initiated by the
AutoTam: Specifying Secure Protocol Implementations with Tamarin Model Generation


Table 3: Diffie-Hellman Key-exchange Protocol with reveal-                          Table 5: Implementation Size of DH and WireGuard Protocols
ing signature.                                                                      and Size of Generated Tamarin Model.

               A → B: ⟨’1’, I, R, 𝑔𝑥 ⟩                                                                                   DH     WireGuard
               B → A: ⟨’10’, sign{⟨’2’, R, I, 𝑔𝑥 , 𝑔 𝑦 ⟩}𝑙𝑡𝑘𝐵 ⟩
                                                                                                   LoC Initiator          68        222
               A → B: ⟨’10’, sign{⟨’3’, I, R, 𝑔𝑥 , 𝑔 𝑦 ⟩}𝑙𝑡𝑘𝐴 ⟩
                                                                                                   LoC Responder          74        243
                                                                                                   Generated Lines       107        242
                    Table 4: WireGuard Protocol

        A → B: ⟨’1’, ’000’, SidA, 𝑔𝑥 , {𝑔𝑙𝑡𝑘𝐴 }, {𝑡𝑠}, mac1, mac2⟩                         Table 6: Verification Results for Tamarin Models
        B → A: ⟨’2’, ’000’, SidB, SidA, 𝑔 𝑦 , {_}, mac1, mac2⟩
        A ↔ B: ⟨’4’, ’000’, receiverSid, csend, {msgN}⟩                                                                            DH     WireGuard
                                                                                          Time                                 3.06s         359.62s
sender of the first message, and proceeds with a response from                            Reachability Initiator                              
the responder, after which the encrypted transport messages may                           Weak Secrecy Initiator                              
be sent, first by the initiator and then from either endpoint. The                        Injective Agreement Initiator                       
protocol is shown in simplified form in Table 4.                                          Reachability Responder                              
   We use curly brackets to denote AEAD encryption using derived                          Weak Secrecy Responder                              
keys. The encryption and decryption keys are derived in a long                            Non-Injective Agreement Resp.                       
chain of hashes, Diffie-Hellman operations, and hash-based key-                           Injective Agreement Responder                      N/A*
derivation functions (HKDF) which we omit from the notation.                              *Not applicable for the handshake phase.
To highlight the complexity of the key derivation, we note that
deriving the encryption keys and first mac in the first message from
the initiator requires thirteen separate hashing operations when                    provide a so-called sources lemma (see e.g. [31]). WireGuard being
the HKDF is expanded. The final message is the transport message                    challenging to verify is in line with other works on the verification
which encrypts an IP packet msgN, and can be repeated, increasing                   of WireGuard using Tamarin, as the more detailed verified models
the counter csend.                                                                  of the protocol have required some form of manual guidance to
                                                                                    verify efficiently, either in the form of writing sources lemmas [6],
7.3     Implementation and Verification Effort                                      writing an oracle [6, 44, 49], or providing state invariants for the key-
The sizes of our AutoTam language protocol role descriptions are                    exchange [39]. Writing the sources lemma for the generated model
shown in Table 5. The protocol role descriptions include parsing and                was not any more challenging than writing a source lemma for any
serializing behaviour for both roles. Incoming network messages                     other model. We used the interactive mode of the Tamarin prover to
are parsed and serialized using the concat and split functions for                  identify the missing partial deconstructions and their cause. After
concatenating and dividing parts of messages, respectively. Most of                 some experimentation we found it sufficient to prove that adversary
the parsing behaviour can be implemented by dividing a message                      knowledge of the terms sock, src_addr and r_sender_index was
into appropriately sized parts and comparing each part with a con-                  always preceded by the fourth action fact of the initiator role.
stant or known value. We do not implement DoS mitigation, the                          We show the verification results for the automatically generated
moving window for avoiding duplicate counter values, and concur-                    DH model and the WireGuard model with the added sources lemma
rent reading and writing of transport messages in our WireGuard                     in Table 6.
implementation.
   For both protocols, we generate a Tamarin model. The generated                   7.4     Comparing Generated and Expert Models
model includes lemmas generated for both roles in each protocol.                    We compare our generated WireGuard model to other works which
We produce lemmas for the handshake phase of both protocols,                        also use Tamarin for the verification of the WireGuard protocol.
including weak secrecy of derived keys, and authentication as injec-                While other works have performed symbolic analysis for more ad-
tive agreement on derived keys. We generate a reachability lemma                    vanced security properties such as verifying the secrecy of transport
showing that a handshake can complete for both protocols as a san-                  message payloads and anonymity, the security properties are not
ity check. This ensures that the other lemmas do not vacuously hold.                our main focus, as only basic authentication and secrecy properties
The final row of Table 5 shows the size of the generated Tamarin                    are currently supported for automatic generation by our tool. The
model. The time to generate Tamarin models including lemmas                         comparison focuses on the fidelity of models, meaning the amount
for both of our test examples is less than 1s. We verify our models                 of detail kept from the protocol role description.
using Tamarin on a 16Gb RAM Intel Xeon 3.5Ghz CPU server. The                          We show our comparison in Table 7. The columns indicate that a
model for the DH protocol verifies without any modification for all                 feature is fully modelled as authentically as possible using a check-
security properties in less than 5s using Tamarin.                                  mark, or that a feature is missing from the model using X. The
   Verification of the WireGuard protocol is more challenging. In                   Protocol column indicates whether the model follows the Wire-
order to verify the generated model, we were required to manually                   Guard message format or the Noise IKpsk2 message format. The
                                                                                                                Johannes Wilson, Mikael Asplund, and Niklas Johansson


Table 7: Level of detail in resulting Tamarin Models compared to other verified WireGuard models. We use slashes to denote
partially modelled features. Lines of code (LoC) does not count lemmas.

                         Model                      Protocol     Executable        MAC        Decryption          Transport          HKDF          LoC
             Donenfeld and Milner [39]             WireGuard           X             X          no nonce               ⧸*               X          225
                  Girol et al. [44]                  Noise             X             X             ⧸†                                  X          311
                 Arquint et al. [6]                WireGuard          ⧸**            X             X                                   X          293
               Lafourcade et al. [49]              WireGuard           X                          ⧸†                                  X          371
                     AutoTam                       WireGuard                        ⧸‡                               ⧸#                         180
             *Only the first transport message is modelled.                                   † Combined ciphertext and MAC.

             **Manually written protocol implementation.                                      # Modelled but no property verified for transport.
             ‡ Only MAC1 is modelled, as MAC2 is only used for DDoS mitigation which is not implemented.




MAC column indicates whether both MAC fields of the message                          Table 8: Results of Symbolic Execution Analysis, showing
are authentically modelled as derived from message hashes. Here                      analysis time, number of paths explored by KLEE, and the
the second MAC is used only for DoS mitigation, which we have                        number of exceptions encountered.
not implemented and which is therefore not modelled in our model.
The Decryption column indicates whether AEAD was authentically                                Implementation                  Time          # Paths      Errors
modelled with both a decryption and validation of ciphertext.
                                                                                               DH initiator                    59s             965         0
   No Tamarin model explicitly describes the steps performed by the
                                                                                              DH responder                   1min 22s         1262         0
key derivation functions as individual hash operations performed
                                                                                           WireGuard initiator                 21s             44          0
by WireGuard except for our model. While not strictly needed for
                                                                                           WireGuard responder              16min 33s         4120         0
soundness of verification, the expanded HKDF operations showcase
a level of detail in our generated model which is cumbersome to
model by hand. The Tamarin model by Donenfeld and Milner [39]
                                                                                        Our analysis rules out most types of memory errors automati-
uses static strings in place of both MAC fields, and includes the
                                                                                     cally. The analysis time and number of paths is highly dependent
first but not subsequent transport messages. Girol et al. [44] verify
                                                                                     on the parsing behaviour of each role. The initiator side of the
the Noise protocols, which includes the IKpsk2 protocol. IKpsk2
                                                                                     WireGuard protocol is the fastest to analyse, as it only parses a
follows a slightly different format which does not contain some
                                                                                     single relatively short message. Analysis of the responder size of
fields such as the MACs. The model by Arquint et al. [6] was made
                                                                                     the WireGuard protocol takes considerably longer and generates a
with the intention of generating requirements in separation logic.
                                                                                     significantly larger number of execution paths. This is because this
The reparation logic served as the specification when verifying
                                                                                     side of our implementation manages variably sized messages, in the
the WireGuard implementation. This model did not authentically
                                                                                     form of transport messages with arbitrary encrypted data. Since
model the decryption of message terms, instead using encryption
                                                                                     our implementation limits the packet size to at most 512 bytes, the
both when sending a message and when receiving a message. While
                                                                                     search space is still finite, and analysis can still exhaustively search
the verification is still sound, it does not accurately represent the
                                                                                     through every possible message length.
way an implementation would perform decryption. The most de-
tailed model of WireGuard that we are aware of is by Lafourcade                      7.6     Protocol Performance
et al. [49] who wrote their models using SAPIC+ [29], a tool which
can generate models for several different protocol verifiers includ-                 We set up an experiment to evaluate the performance of our Wire-
ing Tamarin. They analyse several scenarios for key compromise,                      Guard implementation when using our AutoTam interpreter. We
including leakage of precomputed static keys and ephemeral keys,                     evaluate the throughput when connecting our client and server
and their models include the complete transport phase. They addi-                    implementations over a 1000Mb/s ethernet connection, each imple-
tionally verify a number of different compromise scenarios, such                     mentation running on a 16Gb RAM Intel Xeon 3.5Ghz CPU server.
as static ephemeral key leakage. They used a dedicated 256 core                      We perform the experiment by measuring the time it took to receive
server for the verification of their models, where verification of all               200 million fix-size UDP messages with a size of 448 bytes in UDP
lemmas took at most 4h and 45min when using Tamarin.                                 data from the initiator to the responder, starting from the time that
                                                                                     the first message was received. Throughput was then computed as
                                                                                     number of bits received over time taken.
7.5    Symbolic Execution Analysis                                                      We show the setup of our experiments in Figure 4. When measur-
We verify the safety of the executable protocol implementations                      ing the throughput for the Linux kernel and Go implementations,
using the method of symbolic execution described in Section 6. We                    we used a UDP client and server implementation where the client
show the results of applying the method to both roles of our DH                      implementation sent UDP messages to the WireGuard routed ad-
and WireGuard implementations in Table 8. For the WireGuard                          dress as fast as possible. Since our implementation is not a full
protocol, the number of transport messages is limited to a single                    TUN device implementation, we set up the implementation to itself
message.                                                                             generate the UDP messages to transport using WireGuard, while on
AutoTam: Specifying Secure Protocol Implementations with Tamarin Model Generation




                                                                                                           No routing




                                                                                      Implementation
                                                                                                           Wireguard kernel


                                                                                                           Wireguard-go


                                                                                                           AutoTam


                                                                                                       0           200         400         600      800   1000
Figure 4: Evaluation Setups. a) Measuring throughput of                                                                       Throughput [Mbit/s]
Linux and Go implementations. b) Measuring throughput of
AutoTam implementation. c) Measuring throughput with no
WireGuard routing.                                                                  Figure 5: Measured Throughput of WireGuard Implementa-
                                                                                    tions, showing median of three experiments.

the receiver end no further routing was performed and we instead
                                                                                    trace property verification and implementations. We list the input
timed receiving the WireGuard transport message payload. Because
                                                                                    language and target language(s) of each tool in col. 3, and the
of this, the comparison is not fully fair, as there is some additional
                                                                                    verifier used for trace properties in col. 4. We compare the needed
routing necessary to read and write messages between a UDP client
                                                                                    formal expertise required for creating both the implementation
and WireGuard implementation.
                                                                                    itself in col. 5, and to perform the verification in col. 6. We believe
   The results of the performance evaluation can be found in Fig-
                                                                                    no approach can be fully automatic in performing verification,
ure 5. Our implementation performs at roughly the same through-
                                                                                    since some verification domain knowledge will be needed to at
put as the official WireGuard Go implementation when ran by our
                                                                                    least specify the properties to verify, identify protocol code sections
interpreter. Considering that we have not made any specific opti-
                                                                                    for analysis, or to guide heuristics for more challenging protocols.
mizations as part of our interpreter implementation, it seems likely
                                                                                    Depending on if the approach can account for looping protocols,
that further optimizations are possible.
                                                                                    we write Y for yes and N for no in col. 7. Finally, we list the name of
                                                                                    the largest case-study performed using the tool to our knowledge
7.7     Interoperability                                                            in col. 8.
We tested running our implementation alongside both the Wire-                           Several works [6, 8, 25, 26, 43, 62] (Type 1 in Table 9) generate an
Guard Go and Linux kernel implementation in order to ensure our                     implementation or contract from a verifiable protocol model, or a
implementation is interoperable. We ensure our implementation                       language close to the model. For this approach, the implementations
can perform both sides of the WireGuard handshake, using two                        must be made by formal verification experts knowledgeable in the
experiments. For the first scenario, we ensure that the UDP message                 modelling language.
send by the UDP client results in a completed handshake between                         A number of works including CryptoBap [1, 27, 45, 57, 58] (Type
the given WireGuard implementation and our AutoTam implemen-                        2 in Table 9) develop methods for automatic verification of existing
tation, and that the UDP message gets delivered. For the second                     protocol implementations. This is important work in order to secure
scenario, we ensure that the handshake initiated by the AutoTam                     existing protocol implementations. However, the methods provide
implementation is accepted by the given WireGuard implementa-                       little guidance for how a new implementation for a new protocol
tion.                                                                               should be written, and general static analysis methods rarely scale
                                                                                    to entire protocol implementations. In the case of CSur [45], manual
8     Related Work                                                                  annotations are also required.
Prior to our work, we are not aware of any tool which can extract                       Some works [5, 59, 63] (Type 3 in Table 9) design protocol im-
Tamarin models from executable implementations besides Crypto-                      plementations using sound refinement techniques from a verified
Bap [57]. CryptoBap uses the HolBA binary analysis platform to                      formal model proven using a theorem prover. Others, e.g. [41],
symbolically execute protocol binaries for analysis, originally to                  verify implementations directly using a theorem prover. For both
ProVerif and CryptoVerif, with recent adaptions [58] also targeting                 approaches, the verification effort is significant.
SAPIC+ which can translate to both Tamarin and DEEPSEC. Their                           Other works [11, 13, 14] (Type 4 in Table 9) encode the verifica-
goal is different from ours, as they are interested in performing                   tion condition directly as type-check conditions in a type-theoretic
thorough and deep analysis of existing implementations focusing                     language. Development in such languages requires good under-
on the protocol logic, while we are interested in verifying a com-                  standing of type theory and functional programming. While specific
plete reference implementation. Case studies reflect this, as they                  to Noise protocols, Ho et al. [46] perform both symbolic verifica-
target the most relevant segments of binaries, extracting functions                 tion and produce efficient implementations of the Noise protocols.
for handshake messages, while in contrast we analyse the entirety                   Building proofs in F* was largely a manual effort, but once written,
of protocol implementations written in the AutoTam language.                        verified implementations for all noise protocols could be generated.
   We categorise related works in Table 9. We divide related work                       Finally, several works [3, 16, 17, 19, 21, 47] (Type 5 in Table 9)
into five types, depending on the method used to connect between                    automatically translate implementations in high-level languages
                                                                                                 Johannes Wilson, Mikael Asplund, and Niklas Johansson


                         Table 9: Tools and Methods for Formal Verification of Protocol Implementations.

 Work                   Type              Source                Trace Property        Impl.      Verif.        Loops            Largest
                                          →Target               Proof Method        Expertise   Expertise                      Case-Study
 Expi2Java [8]             1            Expi→Java                  ProVerif            H
                                                                                       #            H
                                                                                                    #             Y              TLS 1.0
 Cadé et al. [25, 26]      1        CryptoVerif→OCaml             CryptoVerif          H
                                                                                       #            H
                                                                                                    #             N                SSH
 Arquint et al. [6]        1         Tamarin→Java/Go               Tamarin             H
                                                                                       #            H
                                                                                                    #             Y             WireGuard
 Owl/OwlC [43, 62]         1            Owl→Rust                     Owl               H
                                                                                       #            H
                                                                                                    #             Y             WireGuard
 CSur [45]                 2              C→SMT                  Horn clauses          H
                                                                                       #            H
                                                                                                    #             Y       Needham-Schroeder
 ASPIER [27]               2            C→COPPER                 model checker         #            #
                                                                                                    H             Y         OpenSSL core
 c2pv [1]                  2            C→ProVerif                  ProVerif           #            #
                                                                                                    H             N           minexplib
 CryptoBap [57, 58]        2          Binary→SAPIC+               SAPIC+ [29]          #            #
                                                                                                    H             Y         Whatsapp core
 VCC [41]                  3                  C                       Coq              #                          Y            Otway-Rees
 Igloo [59, 63]            3                 Any                 Isabelle / HOL        #                          Y           SCION Router
 Arquint et al. [5]        3                 Any                Separation Logic       #                          Y            WireGuard
 F7 [11, 20]               4                  F#                   Typecheck           H
                                                                                       #                          Y               TLS 1.2
 DY* [13, 14]              4                  F*                   Typecheck           H
                                                                                       #                          Y             Signal / BA
 fs2pv [18, 19]            5           F#→ProVerif                  ProVerif           #            #
                                                                                                    H             Y         WS / Otway-Rees
 DJS [17]                  5           JS→ProVerif                  ProVerif           #            #
                                                                                                    H             Y         HMAC (50 LoC)
 AnBx [56]                 5           AnBx→Java                   OFMC [9]            #            #
                                                                                                    H             N               3KP
 SPS [3]                   5         SPS→JS,ProVerif,              ProVerif,           #            #
                                                                                                    H             N             TLS 1.2
                                        ASLAN [4]                   ASLAN
 ProScript [15, 47]        5      JS→ProVerif,CryptoVerif           ProVerif           #            #
                                                                                                    H             N       Signal / TLS 1.3 core
 hax [16, 21]              5         Rust→F*,ProVerif,              ProVerif           H
                                                                                       #            H
                                                                                                    #             Y              TLS 1.3
                                        CryptoVerif
 AutoTam                5      AutoTam spec.→Tamarin          Tamarin              #               #
                                                                                                   H           Y         WireGuard
 Types: 1 - Model To Implementation; 2 - Static Analysis Extraction; 3 - Direct Verification; 4 - Verification through Type Theory;
 5 - Implementation or Specification to Model. Implementation Expertise: #Target/Source Language Only; #          HSome Formal Expertise
 Verification Expertise: H#Model Language Expertise; Manual Proof


to a verifiable model. As discussed in the introduction, many of           9       Conclusions
the existing works in this category do not cover the entire state          In this paper, we have presented AutoTam, a domain-specific lan-
machine of protocols, and in particular do not fully support looping       guage and interpreter for cryptographic protocols, our AutoTam
protocol state machines. In the case of hax [16], manual annotations       translator tool for soundly producing Tamarin models, and our
are required to select functions to extract to ProVerif, and manual        integration of symbolic execution for protocol analysis of protocols
effort is needed to write the verification scenario.                       written in AutoTam. The language is directly defined at the abstrac-
    Based on our classification, only five tools require no formal         tion level of message terms, and as a result, implementation effort
verification expertise during the implementation phase, does not           is focused on placing network operations, message parsing, and
require manual proofs, and supports looping protocol state ma-             cryptographic operations into a state machine. Our sound transla-
chines: ASPIER, CryptoBap, fs2pv, DJS, and AutoTam. Out of these,          tion enables verification of authenticity and secrecy properties at
all besides CryptoBap and AutoTam only verify small case studies           the implementation level.
to our knowledge.                                                             We produce formally verified implementations of a signed Diffie-
    In addition to the works already discussed in Subsection 7.4,          Hellman protocol and the WireGuard VPN protocol in our case-
there exists a number of works which analyse WireGuard which               studies. We generate detailed symbolic models which accurately
do not use Tamarin. A Computational proof was performed by                 capture the semantics of the executable implementations, along
Lipp et al. [50] using CryptoVerif. A manual proof of security in a        with the verification goals in the form of high-level security prop-
computational model was performed by Dowling and Paterson [40].            erties. Since we use a sound transformation which retains trace
Also, the closely related Noise protocol IKpsk2 has been analysed by       properties between a set of AutoTam protocol role descriptions
Kobeissi et al. [48] and Ho et al. [46]. For a more detailed comparison    and their generated model, our proofs of the high-level properties
of most of these works we refer to Lafourcade et al. [49].                 formally verify the security of our implementations. Through sym-
                                                                           bolic execution we automatically rule out implementation-level
                                                                           memory errors. In addition, interoperability testing ensures that
                                                                           we implement and model the desired protocol.
AutoTam: Specifying Secure Protocol Implementations with Tamarin Model Generation


Acknowledgments                                                                                Implementing tls with verified cryptographic security. In 2013 IEEE Symposium
                                                                                               on Security and Privacy (2013), pp. 445–459.
This work was partially supported by the Wallenberg AI, Autonomous                        [21] Bhargavan, K., Hansen, L. L., Kiefer, F., Schneider-Bensch, J., and Spitters,
Systems and Software Program (WASP) funded by the Knut and                                     B. Formal security and functional verification of cryptographic protocol im-
                                                                                               plementations in rust. In Proceedings of the 2025 ACM SIGSAC Conference on
Alice Wallenberg Foundation.                                                                   Computer and Communications Security (2025), pp. 2729–2743.
                                                                                          [22] Bhargavan, K., Lavaud, A. D., Fournet, C., Pironti, A., and Strub, P. Y. Triple
                                                                                               handshakes and cookie cutters: Breaking and fixing authentication over tls. In
References                                                                                     2014 IEEE Symposium on Security and Privacy (2014), pp. 98–113.
 [1] Aizatulin, M., Gordon, A. D., and Jürjens, J. Extracting and verifying crypto-       [23] Blanchet, B. Modeling and verifying security protocols with the applied pi
     graphic models from c protocol code by symbolic execution. In Proceedings of              calculus and proverif. Foundations and Trends® in Privacy and Security 1, 1-2
     the 18th ACM Conference on Computer and Communications Security (2011), CCS               (2016), 1–135.
     ’11, Association for Computing Machinery, p. 331–340.                                [24] Cadar, C., Dunbar, D., and Engler, D. Klee: Unassisted and automatic genera-
 [2] Alfred, V. A., Monica, S. L., and Jeffrey, D. U. Compilers principles, techniques         tion of high-coverage tests for complex systems programs. In Proceedings of the
     & tools. pearson Education, 2007.                                                         8th USENIX Conference on Operating Systems Design and Implementation (USA,
 [3] Almousa, O., Mödersheim, S., and Viganò, L. Alice and Bob: Reconciling Formal             2008), OSDI’08, USENIX Association, p. 209–224.
     Models and Implementation. Springer International Publishing, Cham, 2015,            [25] Cadé, D., and Blanchet, B. From computationally-proved protocol specifica-
     pp. 66–85.                                                                                tions to implementations. In 2012 Seventh International Conference on Availability,
 [4] Armando, A., Arsac, W., Avanesov, T., Barletta, M., Calvi, A., Cappai, A.,                Reliability and Security (2012), IEEE, pp. 65–74.
     Carbone, R., Chevalier, Y., Compagna, L., Cuéllar, J., et al. The avantssar          [26] Cadé, D., and Blanchet, B. Proved generation of implementations from com-
     platform for the automated validation of trust and security of service-oriented           putationally secure protocol specifications. Journal of Computer Security 23, 3
     architectures. In International Conference on Tools and Algorithms for the Con-           (2015), 331–402.
     struction and Analysis of Systems (2012), Springer, pp. 267–282.                     [27] Chaki, S., and Datta, A. Aspier: An automated framework for verifying security
 [5] Arqint, L., Schwerhoff, M., Mehta, V., and Müller, P. A generic method-                   protocol implementations. In 2009 22nd IEEE Computer Security Foundations
     ology for the modular verification of security protocol implementations. In               Symposium (2009), pp. 172–185.
     Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communica-             [28] Chau, S. Y., Yahyazadeh, M., Chowdhury, O., Kate, A., and Li, N. Analyzing
     tions Security (New York, NY, USA, 2023), CCS ’23, Association for Computing              semantic correctness with symbolic execution: A case study on pkcs#1 v1.5 sig-
     Machinery, p. 1377–1391.                                                                  nature verification. Network and Distributed Systems Security (NDSS) Symposium
 [6] Arqint, L., Wolf, F. A., Lallemand, J., Sasse, R., Sprenger, C., Wiesner,                 2019 (2019).
     S. N., Basin, D., and Müller, P. Sound verification of security protocols: From      [29] Cheval, V., Jacomme, C., Kremer, S., and Künnemann, R. SAPIC+: protocol
     design to interoperable implementations. In 2023 IEEE Symposium on Security               verifiers of the world, unite! In 31st USENIX Security Symposium (USENIX Security
     and Privacy (SP) (2023), pp. 1077–1093.                                                   22) (Boston, MA, Aug. 2022), USENIX Association, pp. 3935–3952.
 [7] Asadian, H., Fiterau-Brostean, P., Jonsson, B., and Sagonas, K. Monitor-             [30] Cheval, V., Jacomme, C., Kremer, S., and Künnemann, R. Sapic+: protocol
     based testing of network protocol implementations using symbolic execution.               verifier of the world unite!, 2022. Technical report.
     In Proceedings of the 19th International Conference on Availability, Reliability     [31] Cortier, V., Delaune, S., Dreier, J., and Klein, E. Automatic generation of
     and Security (New York, NY, USA, 2024), ARES ’24, Association for Computing               sources lemmas in tamarin: towards automatic proofs of security protocols.
     Machinery.                                                                                Journal of Computer Security 30, 4 (2022), 573–598.
 [8] Backes, M., Busenius, A., and HriŢcu, C. On the development and formalization        [32] Cortier, V., Kremer, S., and Warinschi, B. A survey of symbolic methods
     of an extensible code generator for real life security protocols. In NASA Formal          in computational analysis of cryptographic systems. Journal of Automated
     Methods (Berlin, Heidelberg, 2012), A. E. Goodloe and S. Person, Eds., Springer           Reasoning 46, 3 (2011), 225–259.
     Berlin Heidelberg, pp. 371–387.                                                      [33] Cremers, C., and Dehnel-Wild, M. Component-based formal analysis of 5g-
 [9] Basin, D., Mödersheim, S., and Vigano, L. Ofmc: A symbolic model checker                  aka: Channel assumptions and session confusion. In Network and Distributed
     for security protocols. International Journal of Information Security 4 (2005),           System Security Symposium (NDSS) (2019), Internet Society.
     181–208.                                                                             [34] Cremers, C., Horvat, M., Hoyland, J., Scott, S., and van der Merwe, T. A
[10] Basin, D., Sasse, R., and Toro-Pozo, J. The emv standard: Break, fix, verify. In          comprehensive symbolic analysis of tls 1.3. In Proceedings of the 2017 ACM
     2021 IEEE Symposium on Security and Privacy (SP) (2021), pp. 1766–1781.                   SIGSAC Conference on Computer and Communications Security (New York, NY,
[11] Bengtson, J., Bhargavan, K., Fournet, C., Gordon, A. D., and Maffeis, S.                  USA, 2017), CCS ’17, Association for Computing Machinery, p. 1773–1788.
     Refinement types for secure implementations. ACM Transactions on Programming         [35] Cremers, C., Horvat, M., Scott, S., and van der Merwe, T. Automated analysis
     Languages and Systems (TOPLAS) 33, 2 (2011), 1–45.                                        and verification of tls 1.3: 0-rtt, resumption and delayed authentication. In 2016
[12] Beurdouche, B., Bhargavan, K., Delignat-Lavaud, A., Fournet, C.,                          IEEE Symposium on Security and Privacy (SP) (2016), pp. 470–485.
     Kohlweiss, M., Pironti, A., Strub, P.-Y., and Zinzindohoue, J. K. A messy            [36] Cytron, R., Ferrante, J., Rosen, B. K., Wegman, M. N., and Zadeck, F. K. An
     state of the union: Taming the composite state machines of tls. Commun. ACM               efficient method of computing static single assignment form. In Proceedings of the
     60, 2 (jan 2017), 99–107.                                                                 16th ACM SIGPLAN-SIGACT symposium on Principles of programming languages
[13] Bhargavan, K., Bichhawat, A., Do, Q. H., Hosseyni, P., Küsters, R., Schmitz,              (1989), pp. 25–35.
     G., and Würtele, T. DY★ : A modular symbolic verification framework for              [37] Dolev, D., and Yao, A. On the security of public key protocols. IEEE Transactions
     executable cryptographic protocol code. In 2021 IEEE European Symposium on                on Information Theory 29, 2 (1983), 198–208.
     Security and Privacy (EuroS&P) (2021), pp. 523–542.                                  [38] Donenfeld, J. A. Wireguard: Next generation kernel network tunnel. In Network
[14] Bhargavan, K., Bichhawat, A., Hosseyni, P., Küsters, R., Pruiksma, K.,                    and Distributed System Security (NDSS) Symposium (2017), pp. 1–12.
     Schmitz, G., Waldmann, C., and Würtele, T. Layered symbolic security analy-          [39] Donenfeld, J. A., and Milner, K. Formal verification of the wireguard protocol.
     sis in dy*. In Computer Security – ESORICS 2023 (Cham, 2024), G. Tsudik, M. Conti,        Technical Report (2018).
     K. Liang, and G. Smaragdakis, Eds., Springer Nature Switzerland, pp. 3–21.           [40] Dowling, B., and Paterson, K. G. A cryptographic analysis of the wireguard
[15] Bhargavan, K., Blanchet, B., and Kobeissi, N. Verified models and reference               protocol. In Applied Cryptography and Network Security (Cham, 2018), B. Preneel
     implementations for the tls 1.3 standard candidate. In 2017 IEEE Symposium on             and F. Vercauteren, Eds., Springer International Publishing, pp. 3–21.
     Security and Privacy (SP) (2017), pp. 483–502.                                       [41] Dupressoir, F., Gordon, A. D., Jürjens, J., and Naumann, D. A. Guiding a
[16] Bhargavan, K., Buyse, M., Franceschino, L., Hansen, L. L., Kiefer, F.,                    general-purpose c verifier to prove cryptographic protocols. Journal of Computer
     Schneider-Bensch, J., and Spitters, B. hax: Verifying security-critical rust              Security 22, 5 (2014), 823–866.
     software using multiple provers. In International Conference on Verified Software:   [42] Durgin, N., Lincoln, P., Mitchell, J., and Scedrov, A. Multiset rewriting and
     Theories, Tools, and Experiments (2024), Springer, pp. 96–119.                            the complexity of bounded security protocols. Journal of Computer Security 12, 2
[17] Bhargavan, K., Delignat-Lavaud, A., and Maffeis, S. Defensive javascript:                 (2004), 247–311.
     Building and verifying secure web components. In International School on Foun-       [43] Gancher, J., Gibson, S., Singh, P., Dharanikota, S., and Parno, B. Owl:
     dations of Security Analysis and Design. Springer, 2012, pp. 88–123.                      Compositional verification of security protocols via an information-flow type
[18] Bhargavan, K., Fournet, C., and Gordon, A. D. Verified reference implemen-                system. In 2023 IEEE Symposium on Security and Privacy (SP) (2023), pp. 1130–
     tations of ws-security protocols. In International Workshop on Web Services and           1147.
     Formal Methods (2006), Springer, pp. 88–106.                                         [44] Girol, G., Hirschi, L., Sasse, R., Jackson, D., Cremers, C., and Basin, D. A
[19] Bhargavan, K., Fournet, C., Gordon, A. D., and Tse, S. Verified interoperable             spectral analysis of noise: A comprehensive, automated, formal analysis of Diffie-
     implementations of security protocols. ACM Transactions on Programming                    Hellman protocols. In 29th USENIX Security Symposium (USENIX Security 20)
     Languages and Systems 31, 1 (dec 2008).                                                   (Aug. 2020), USENIX Association, pp. 1857–1874.
[20] Bhargavan, K., Fournet, C., Kohlweiss, M., Pironti, A., and Strub, P.-Y.             [45] Goubault-Larrecq, J., and Parrennes, F. Cryptographic protocol analysis on
                                                                                                                Johannes Wilson, Mikael Asplund, and Niklas Johansson


     real c code. In Verification, Model Checking, and Abstract Interpretation (Berlin,   public-code/autotam. The project README explains how to build
     Heidelberg, 2005), R. Cousot, Ed., Springer Berlin Heidelberg, pp. 363–379.          AutoTam on a Linux machine. The README additionally explains
[46] Ho, S., Protzenko, J., Bichhawat, A., and Bhargavan, K. Noise: A library of
     verified high-performance secure channel protocol implementations. In 2022           how to produce each artifact presented as part of our case studies.
     IEEE Symposium on Security and Privacy (SP) (2022), pp. 107–124.                     We have confirmed our project builds on Ubuntu 22.04.4 LTS.
[47] Kobeissi, N., Bhargavan, K., and Blanchet, B. Automated verification for
     secure messaging protocols and their implementations: A symbolic and compu-
                                                                                             In the repository, we provide the artifact for the generated Tamarin
     tational approach. In 2017 IEEE European Symposium on Security and Privacy           model of the DH protocol under:
     (EuroS&P) (2017), pp. 435–450.
[48] Kobeissi, N., Nicolas, G., and Bhargavan, K. Noise explorer: Fully automated
                                                                                                examples/DH/automatic.spthy
     modeling and verification for arbitrary noise protocols. In 2019 IEEE European       The generated Tamarin model of the WireGuard protocol as origi-
     Symposium on Security and Privacy (EuroS&P) (2019), pp. 356–370.
[49] Lafourcade, P., Mahmoud, D., and Ruhault, S. A Unified Symbolic Analysis
                                                                                          nally generated can be found under:
     of WireGuard. In Network and Distributed System Security (NDSS) Symposium                  examples/Wireguard/automatic.spthy
     (San Diego (CA), United States, Feb. 2024).
[50] Lipp, B., Blanchet, B., and Bhargavan, K. A mechanised cryptographic proof of        And the model with the added source lemma can be found as:
     the wireguard virtual private network protocol. In 2019 IEEE European Symposium            examples/Wireguard/wg/auto_source.spthy
     on Security and Privacy (EuroS&P) (2019), pp. 231–246.
[51] Lowe, G. Breaking and fixing the needham-schroeder public-key protocol using         The automatically generated files can be generated by building and
     fdr. In Tools and Algorithms for the Construction and Analysis of Systems (Berlin,   running AutoTam as described in the README.
     Heidelberg, 1996), T. Margaria and B. Steffen, Eds., Springer Berlin Heidelberg,
     pp. 147–166.                                                                            In order to verify the models, a working installation of Tamarin
[52] Lowe, G. A hierarchy of authentication specifications. In Proceedings 10th           is needed. Instructions for installing Tamarin are found at https:
     Computer Security Foundations Workshop (1997), pp. 31–43.
[53] Meier, S. Advancing automated security protocol verification. PhD thesis, ETH
                                                                                          //tamarin-prover.com/install.html. We used Tamarin version 1.10.0
     Zurich, 2013.                                                                        with Maude version 3.1. Once installed, automatic verification is
[54] Meier, S., Schmidt, B., Cremers, C., and Basin, D. The tamarin prover for the        performed by running:
     symbolic analysis of security protocols. In Computer Aided Verification (2013),
     Springer Berlin Heidelberg, pp. 696–701.                                                   tamarin-prover [spthy file] --prove
[55] Mitchell, J., Scedrov, A., Durgin, N., and Lincoln, P. Undecidability of
     bounded security protocols. In Workshop on formal methods and security protocols
                                                                                          All lemmas should show as verified for both models.
     (1999).                                                                                 The timing of the Tamarin verification, and the symbolic exe-
[56] Modesti, P. Efficient java code generation of security protocols specified in        cution, were performed on an 16GB RAM Intel i7-1355U (12 core)
     anb/anbx. In Security and Trust Management (Cham, 2014), S. Mauw and C. D.
     Jensen, Eds., Springer International Publishing, pp. 204–208.                        computer.
[57] Nasrabadi, F., Künnemann, R., and Nemati, H. Cryptobap: A binary analysis               To perform the benchmarking experiments, we used two 16Gb
     platform for cryptographic protocols. In Proceedings of the 2023 ACM SIGSAC          RAM Intel Xeon 3.5Ghz CPU (4 cores) servers running Ubuntu
     Conference on Computer and Communications Security (New York, NY, USA, 2023),
     CCS ’23, Association for Computing Machinery, p. 1362–1376.                          22.04.5 LTS, which were connected directly with a 1000Mb/s ether-
[58] Nasrabadi, F., Künnemann, R., and Nemati, H. Automated side-channel anal-            net connection.
     ysis of cryptographic protocol implementations. arXiv preprint arXiv:2511.11385
     (2025).
                                                                                             For instructions on how to perform the experiments in our
[59] Pereira, J., Klenze, T., Giampietro, S., Limbeck, M., Spiliopoulos, D., Wolf,        case studies, we refer to the detailed instructions in the project
     F., Eilers, M., Sprenger, C., Basin, D., Müller, P., et al. Protocols to code:       README.md file.
     Formal verification of a secure next-generation internet router. In Proceedings
     of the 2025 ACM SIGSAC Conference on Computer and Communications Security
     (2025), pp. 1469–1483.                                                               B    Ethical Considerations
[60] Perrin, T. The noise protocol framework, 2018.
[61] Polubelova, M., Bhargavan, K., Protzenko, J., Beurdouche, B., Fromherz,              This work presents methods for creating highly secure protocol
     A., Kulatova, N., and Zanella-Béguelin, S. HACLxN: Verified generic SIMD             implementations, which is for the benefit of the entire security
     crypto (for all your favourite platforms). In Proceedings of the 2020 ACM SIGSAC     community. We do not see dangers of potential misuse of AutoTam
     Conference on Computer and Communications Security (2020), pp. 899–918.
[62] Singh, P., Gancher, J., and Parno, B. { OwlC } : Compiling security proto-           itself. A malicious actor would not benefit much from access to
     cols to verified, secure, { High-Performance } libraries. In 34th USENIX Security    AutoTam or our description of it in this paper.
     Symposium (USENIX Security 25) (2025), pp. 5071–5090.
[63] Sprenger, C., Klenze, T., Eilers, M., Wolf, F. A., Müller, P., Clochard, M.,
                                                                                             The code provided to replicate our performance benchmarks
     and Basin, D. Igloo: soundly linking compositional refinement and separation         includes a simple UDP client to send messages, which could in
     logic for distributed system verification. Proc. ACM Program. Lang. 4, OOPSLA        theory be used to attempt to overload a network. We do not believe
     (nov 2020).
[64] Vanhoef, M., and Piessens, F. Symbolic execution of security protocol imple-         that our very simple UDP client is providing anything which would
     mentations: Handling cryptographic primitives. In 12th USENIX Workshop on            not already be easily implementable with a little bit of programming
     Offensive Technologies (WOOT 18) (Baltimore, MD, Aug. 2018), USENIX Associa-         knowledge. We believe that providing the exact code used in order
     tion.
[65] Wilson, J., and Asplund, M. Analysing TLS Implementations Using Full-Message         for our results to be fully replicable is more beneficial than hiding
     Symbolic Execution. No. 15396 in Lecture Notes in Computer Science. Springer,        the implementation of our UDP client.
     2025, pp. 283–302.
[66] Zinzindohoué, J.-K., Bhargavan, K., Protzenko, J., and Beurdouche, B.
     HACL*: A verified modern cryptographic library. In Proceedings of the 2017 ACM       C    Code Examples
     SIGSAC Conference on Computer and Communications Security (2017), pp. 1789–
     1806.
                                                                                          We show our full AutoTam code for the DH example in Listing 4
                                                                                          and Listing 5. Finally, we show the generated Tamarin output for
                                                                                          the DH example in Listing 6.
A     Open Science
We provide the entire codebase of the implementation of AutoTam,                          D    Full Translation Table
including the AutoTam protocol role descriptions of our case studies.                     Table 10 shows the full translation table. The left-hand side shows
Our public repository can be found at https://gitlab.liu.se/ida-rtslab/                   available functions in the AutoTam language. The right-hand side
AutoTam: Specifying Secure Protocol Implementations with Tamarin Model Generation


shows the expression which is added to the rule when building
                                                                                    START {
the Tamarin rules for a transition. The type describes how each                         Input {
                                                                                            sock = Arg_Int ()
expression is added to the Tamarin rule. ACTION is used for equality                        I = Arg (8)
and inequality restrictions which in Tamarin are encoded using                              I_be = htobe (I)
                                                                                            sk_i = Arg_priv_sign (32)
the action facts Eq and Neq. SET describes an assignment, and                               R = Arg (8)
will use the expression to the right of the arrow in place of the                           R_be = htobe (R)
                                                                                            pk_r = Arg_pub_sign (32)
expression on the left. IN and OUT types are facts which are added                          pk_i = Arg_pub_sign (32)
to the precondition and postcondition of the rule, respectively.                            x = GenSecret (32)
                                                                                            gx = EC25519_PublicKey (x)
These include network operations which make terms visible to                            }
                                                                                    }
the network adversary through In and Out facts, fresh terms in the
form of Fr, and private and public key provisioning.                                Transition ( START , State1 )

                                                                                    State1 {
                                                                                        Output {
                                                                                             const1 = Const (1 , 1)
                                                                                             m1 = concat ( const1 , I_be )
                                                                                             m1 = concat (m1 , R_be )
                                                                                             m1 = concat (m1 , gx )
                                                                                             send ( sock , m1 )
                                                                                        }
                                                                                        Input {
                                                                                             m2 = recv ( sock , 148)
                                                                                        }
                                                                                    }

                                                                                    Transition ( State1 , DONE ) {
                                                                                        const10 = Const (1 , 10)
                                                                                        msg_type , m2_tail_1 = split (m2 , 1)
                                                                                        RequireEq ( msg_type , const10 )
                                                                                        sig_msg2 , msg2 = split ( m2_tail_1 , 64)
                                                                                        Ed25519_ValidateSig ( pk_r , msg2 , sig_msg2 )
                                                                                        const2 = Const (1 , 2)
                                                                                        msg_type_inner , msg2_tail_1 = split ( msg2 , 1)
                                                                                        RequireEq ( msg_type_inner , const2 )
                                                                                        responder_name , msg2_tail_2 = split ( msg2_tail_1 , 8)
                                                                                        RequireEq ( responder_name , R_be )
                                                                                        initiator_name , msg2_tail_3 = split ( msg2_tail_2 , 8)
                                                                                        RequireEq ( initiator_name , I_be )
                                                                                        pk_initiator , gy = split ( msg2_tail_3 , 32)
                                                                                        RequireEq ( pk_initiator , gx )
                                                                                        RequireSize (gy , 32)
                                                                                        gxy = EC25519_DH (x , gy )
                                                                                    }

                                                                                    DONE {
                                                                                        Output {
                                                                                            const3 = Const (1 , 3)
                                                                                            msg3 = concat ( const3 , I_be )
                                                                                            msg3 = concat ( msg3 , R_be )
                                                                                            msg3 = concat ( msg3 , gx )
                                                                                            msg3 = concat ( msg3 , gy )
                                                                                            sig_msg3 = Ed25519_SignMessage ( sk_i , msg3 )
                                                                                            const10 = Const (1 , 10)
                                                                                            m3 = concat ( const10 , sig_msg3 )
                                                                                            m3 = concat (m3 , msg3 )
                                                                                            send ( sock , m3 )
                                                                                            Ret ( gxy )
                                                                                            Dummy (I)
                                                                                            Dummy (R)
                                                                                            Dummy ( pk_i )
                                                                                            Dummy ( pk_r )
                                                                                        }
                                                                                    }

                                                                                                Listing 4: DH Initiator code in AutoTam
                                                                                                 Johannes Wilson, Mikael Asplund, and Niklas Johansson


                                                                     segment was partially completed in 𝑤𝑒∗ , or an input state segment
START {
    Input {                                                          was completed by a participant 𝑝 without any following transition
        sock = Arg_Int ()
        R = Arg (8)
                                                                     being performed by 𝑝 in 𝑤𝑒∗ , or an output segment wasn’t fully
        R_be = htobe (R)                                             completed after a completed transition by some participant 𝑝 in
        sk_r = Arg_priv_sign (32)
        I = Arg (8)                                                  𝑤𝑒 ∗.
        I_be = htobe (I)                                                 If an input state segment was partially completed in 𝑤𝑒∗ , or an
        pk_i = Arg_pub_sign (32)
        pk_r = Arg_pub_sign (32)                                     input state segment was completed without any following transition
        m1 = recv ( sock , 49)                                       in 𝑤𝑒∗ , then there must exist a trace 𝑤𝑒# ∈ 𝜏𝑒 (𝐶) where that input
    }
}                                                                    state segment was never performed. Executed input state segments
Transition ( START , State1 ){
                                                                     do not affect the execution of other participants since no additional
    const1 = Const (1 , 1)                                           information becomes visible to the network. Additionally, executed
    msg_type , m1_tail_1 = split (m1 , 1)                            input state segments are not visible on the completed transition
    RequireEq ( msg_type , const1 )                                  trace. Therefore, it holds that Ψ(𝑤𝑒 ) = Ψ(𝑤𝑒∗ ).
    initiator_name , m1_tail_2 = split ( m1_tail_1 , 8)
    RequireEq ( initiator_name , I_be )                                  If an output segment wasn’t fully completed after a completed
    responder_name , gx = split ( m1_tail_2 , 8)                     transition by some participant 𝑝 in 𝑤𝑒∗ , then requirement 2 rules
    RequireEq ( responder_name , R_be )
    RequireSize (gx , 32)                                            out all of the statements which impose restrictions in the sym-
}
                                                                     bolic model2 , leaving no restrictions to prevent further execution.
State1 {                                                             Therefore, the same scenario must permit a trace 𝑤𝑒# ∈ 𝜏𝑒 (𝐶) where
    Output {
         y = GenSecret (32)                                          execution continues, completing the output state segment. Any
         gy = EC25519_PublicKey (y)                                  information revealed to the network in 𝑤𝑒∗ is also revealed in 𝑤𝑒# ,
         gxy = EC25519_DH (y , gx )
         const2 = Const (1 , 2)                                      thus further execution which is possible for other participants in
         msg2 = concat ( const2 , R_be )                             𝑤𝑒∗ remains possible in 𝑤𝑒# . Additionally, executed output state seg-
         msg2 = concat ( msg2 , I_be )
         msg2 = concat ( msg2 , gx )                                 ments are not visible on the completed transition trace. Therefore,
         msg2 = concat ( msg2 , gy )
         sig_msg2 = Ed25519_SignMessage ( sk_r , msg2 )
                                                                     it holds that Ψ(𝑤𝑒 ) = Ψ(𝑤𝑒∗ ).                                     □
         const10 = Const (1 , 10)
         m2 = concat ( const10 , sig_msg2 )
         m2 = concat (m2 , msg2 )
                                                                     F     Formal Syntax Definition
         send ( sock , m2 )
    }
                                                                     A more formal definition of the AutoTam syntax is given in List-
    Input {                                                          ing 7 in Backus-Naur form. Alphanumeric strings can be used in
         m3 = recv ( sock , 148)
    }                                                                place of symbols ending in Name. Only a FunctionName which
}                                                                    appears in the left-hand side of Table 10, with the correct number
Transition ( State1 , DONE ) {                                       of parameters and output variables, will be considered valid. In
    const10 = Const (1 , 10)                                         addition, the function translation may not be of type IN if placed in
    msg_type , m3_tail_1 = split (m3 , 1)
    RequireEq ( msg_type , const10 )                                 the Output part of a State, of type OUT if placed in the Input part of
    sig_msg3 , msg3 = split ( m3_tail_1 , 64)
    Ed25519_ValidateSig ( pk_i , msg3 , sig_msg3 )
                                                                     a State, or of either type IN or OUT when placed within a Transition.
    const3 = Const (1 , 3)                                           Note that transitions themselves do not have names, while states
    msg_type_inner , msg3_tail_1 = split ( msg3 , 1)
    RequireEq ( msg_type_inner , const3 )                            and variables do.
    initiator_name , msg3_tail_2 = split ( msg3_tail_1 , 8)
    RequireEq ( initiator_name , I_be )
    responder_name , msg3_tail_3 = split ( msg3_tail_2 , 8)
    RequireEq ( responder_name , R_be )
    pk_initiator , pk_responder = split ( msg3_tail_3 , 32)
    RequireEq ( pk_initiator , gx )
    RequireEq ( pk_responder , gy )
}

DONE {
    Output {
        Ret ( gxy )
        Dummy (I)
        Dummy (R)
        Dummy ( pk_i )
        Dummy ( pk_r )
    }
}


           Listing 5: DH Responder code in AutoTam


E    Proof of Lemma 2
   Proof Lemma 2. Assume the lemma is false. Then there must
exist some scenario 𝐶 with a transition truncated global execution   2 In the symbolic model, we exclude network errors, leaving only equality tests (includ-
trace 𝑤𝑒∗ , without there being a complete global execution trace    ing ones imposed by signature verification and AEAD decryption) as the statements
𝑤𝑒# ∈ 𝜏𝑒 (𝐶) so that Ψ(𝑤𝑒 ) = Ψ(𝑤𝑒∗ ). Then either an input state    which may ”halt” execution.
AutoTam: Specifying Secure Protocol Implementations with Tamarin Model Generation


theory SignedDH
begin

builtins : signing , diffie - hellman


rule Init_Signing_LTK :
     let sign_pk = pk (∼ sign_ltk ) in
     [ Fr (∼ sign_ltk ) ]
  - -[] - >
     [ Out ( sign_pk ), ! SignLtk (∼ sign_ltk ), ! SignPk ( sign_pk ) ]

rule Leak_Signing_LTK :
    [ ! SignLtk (∼ sign_ltk ) ]
  --[ Leak ( pk (∼ sign_ltk )) ]->
    [ Out (∼ sign_ltk ) ]

rule Create_arg_priv :
     let dh_pk = 'g '^∼ dh_ltk in
     [ Fr (∼ dh_ltk ) ]
  - -[] - >
     [ Out ( dh_pk ), ! DHLtk (∼ dh_ltk ), ! DHPk ( dh_pk ) ]

rule Leak_DH_LTK :
    [ ! DHLtk (∼ dh_ltk ) ]
  --[ Leak ( 'g '^∼ dh_ltk ) ]->
    [ Out (∼ dh_ltk ) ]

rule Initiator_START_to_State1 :
    let gx = 'g '^∼x
    in
    [ In ( sock ), In (I), ! SignLtk (∼ sk_i ), In (R), ! SignPk ( pk_r ), ! SignPk ( pk_i ), Fr (∼x) ]
  --[ ]->
    [ Out (< '1 ', I , R , gx >) , InitiatorState1 ( sock , I , I , ∼sk_i , R , R , pk_r , pk_i , ∼x , gx ) ]

rule Initiator_State1_to_DONE :
    let msg3222 = <'3 ', I_be , R_be , gx , gy >
         sig_msg3 = sign ( msg3222 , ∼ sk_i )
         m32 = <'10 ', sig_msg3 , '3 ', I_be , R_be , gx , gy >
    in
    [ InitiatorState1 ( sock , I , I_be , ∼sk_i , R , R_be , pk_r , pk_i , ∼x , gx ),
         In (< msg_type , sig_msg2 , msg_type_inner , responder_name , initiator_name , pk_initiator , gy >) ]
  --[ Eq ( msg_type , '10 '),
         Eq ( verify ( sig_msg2 , < msg_type_inner , responder_name , initiator_name , pk_initiator , gy >, pk_r ), true ),
         Eq ( msg_type_inner , '2 '), Eq ( responder_name , R_be ), Eq ( initiator_name , I_be ), Eq ( pk_initiator , gx ) ]->
    [ Out ( m32 ) ]

rule Responder_START_to_State1 :
    let gy = 'g '^∼y
         gxy = gx ^∼y
    in
    [ In ( sock ), In (R), ! SignLtk (∼ sk_r ), In (I), ! SignPk ( pk_i ), ! SignPk ( pk_r ),
         In (< msg_type , initiator_name , responder_name , gx >) , Fr (∼y) ]
  --[ Eq ( msg_type , '1 '), Eq ( initiator_name , I), Eq ( responder_name , R) ]->
    [ Out (< '10 ', sign (< '2 ', R , I , gx , gy >, ∼ sk_r ), '2 ', R , I , gx , gy >) ,
         ResponderState1 (R , R , I , I , pk_i , pk_r , gy , gxy , gx ) ]

rule Responder_State1_to_DONE :
    [ ResponderState1 (R , R_be , I , I_be , pk_i , pk_r , gy , gxy , gx ),
         In (< msg_type , sig_msg3 , msg_type_inner , initiator_name , responder_name , pk_initiator , pk_responder >) ]
  --[ Eq ( msg_type , '10 '),
         Eq ( verify ( sig_msg3 , < msg_type_inner , initiator_name , responder_name , pk_initiator , pk_responder >, pk_i ), true ),
         Eq ( msg_type_inner , '3 '), Eq ( initiator_name , I_be ), Eq ( responder_name , R_be ), Eq ( pk_initiator , gx ),
         Eq ( pk_responder , gy ) ]->
    [ ]

end

Listing 6: Generated Tamarin model for DH example without Lemmas and with Actions removed except for equality restrictions.
Line breaks have been added for readability. See code repository for full example.
                                                                  Johannes Wilson, Mikael Asplund, and Niklas Johansson


                          Table 10: Full Translation Table

Function call (AutoTam language)                   Translation (Tamarin)
                                            Type      Expression
p = Chacha20_Poly1305_dec(k, n, c, d, m)   [ACTION]   Eq(aead_val(k, n, c, d, m), true)
                                             [SET]    p → aead_dec(k, n, c)
c, m = Chacha20_Poly1305_enc(k, n, p, d)      [SET]   c → aead_enc(k, n, p, d),
                                              [SET]   m → aead_mac(k, n, p, d)
gx = EC25519_PublicKey(x)                     [SET]   gx → ’g’ˆx
gxy = EC25519_DH(x, gy)                       [SET]   gxy → gyˆx
sig = Ed25519_SignMessage(sk, m)              [SET]   sig → sign(m, sk)
Ed25519_ValidateSig(pk, m, sig)            [ACTION]   Eq(verify(sig, m, pk), true)
a = Blake2s_keyhash(k, m, SIZE)               [SET]   a → keyhash(k, m)
a = Blake2s_hmac(k, m)                        [SET]   a → hmac(k, m)
x = GenSecret(SIZE)                            [IN]   Fr(∼x)
m = recv(fd, SIZE)                             [IN]   In(m)
m, addr = recvfrom(fd, SIZE)                   [IN]   In(m), In(addr)
send(fd, m)                                  [OUT]    Out(m)
sendto(fd, addr, m)                          [OUT]    Out(addr), Out(m)
a = concat(b, c)                              [SET]   a → ⟨b, c⟩
b, c = split(a, SIZE)                         [SET]   a → ⟨b, c⟩
t = timestamp()                               [SET]   t → $t
s = String(’example’)                         [SET]   s → ’example’
n = Constant(NUM, SIZE)                       [SET]   n → ’NUM’
RequireEq(a, b)                            [ACTION]   Eq(a, b)
RequireNEq(a, b)                           [ACTION]   Neq(a, b)
RequireSize(x, SIZE)                             -    -
a = size(b)                                   [SET]   a → $a
a = Pad16(b)                                  [SET]   a→b
a = htobe(b)                                  [SET]   a→b
n = Counter64()                               [SET]   n → $n
m = Increment(n)                              [SET]   m → $m
x = Arg(SIZE)                                  [IN]   In(x)
x = Arg_Int()                                  [IN]   In(x)
x = Arg_priv_dh(SIZE)                          [IN]   !DHLtk(∼x)
x = Arg_pub_dh(SIZE)                           [IN]   !DHPk(x)
x = Arg_priv_sign(SIZE)                        [IN]   !SignLtk(∼x)
x = Arg_pub_sign(SIZE)                         [IN]   !SignPk(x)
Ret(x)                                           -    -
Dummy(x)                                         -    -
AutoTam: Specifying Secure Protocol Implementations with Tamarin Model Generation


< Program > ::= < State > < Program >
              | < Transition > < Program >
              | ""

< State > ::=     < StateName > { Output { < StatementList > } Input { < StatementList > } }
            |     < StateName > { Output { < StatementList > } }
            |     < StateName > { Input { < StatementList > } }
            |     < StateName > {}

< Transition > ::= Transition ( < StateName > , < StateName >) { < StatementList > }
                 | Transition ( < StateName > , < StateName >)

< StatementList > ::= < Statement > \ n < StatementList >
                    | ""

< Statement > ::= < VariableList > = < FunctionName >( < VariableList >)
                | < VariableList > = < FunctionName >()
                                   | < FunctionName >( < VariableList >)

< VariableList > ::= < VariableName > , < VariableList >
                   | < VariableName >

                                                 Listing 7: AutoTam Syntax in Backus-Naur form
