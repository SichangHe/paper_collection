                                                                                Zero-Knowledge Model Checking

                                                     Pascal Berrang                          Mirco Giacobbe                               Jacob Swales
                                                University of Birmingham                 University of Birmingham                    University of Birmingham
                                                     Zeroth Research                         Zeroth Research                       jxs1545@student.bham.ac.uk
                                                p.p.berrang@bham.ac.uk                   m.giacobbe@bham.ac.uk
                                                                                                Xiao Yang
                                                                                         University of Birmingham
                                                                                    Xi’an Jiaotong-Liverpool University
arXiv:2605.00487v2 [cs.CR] 8 Sep 2026




                                                                                          xiao.yang@xjtlu.edu.cn
                                                                  Abstract                                          Scalability has been the central focus of formal methods
                                        We introduce a technology to formally verify that a software             researchers for decades, yet the industrial adoption of model
                                        system satisfies a temporal specification of functional cor-             checking faces another pressing challenge: confidentiality.
                                        rectness, without revealing the system itself. Our method                The traditional formal verification algorithms require disclo-
                                        combines a deductive approach to model checking to ob-                   sure of the system description in order to convince an external
                                        tain a formal certificate of correctness for the system, with            verifier of the system’s compliance with its specification. In
                                        zero-knowledge proofs to convince an external verifier that              a setting where formal verification is a requirement poten-
                                        the system—kept secret—complies with its specification of                tially involving multiple organisations, jurisdictions, standard-
                                        correctness—made public. We consider proof certificates rep-             isation bodies, the obligation to disclose a system descrip-
                                        resented as ranking functions, and introduce both an explicit-           tion is likely to create tension between regulators’ or cus-
                                        state and a symbolic scheme for model checking in zero                   tomers’ need to ensure compliance with safety requirements
                                        knowledge. Our explicit-state scheme assumes systems repre-              and providers’ desire to protect their intellectual property.
                                        sented as transition graphs. We use polynomial commitments                  Zero-knowledge proofs provide a cryptographic mecha-
                                        to convince the verifier that the public proof certificates corre-       nism by which a prover can convince a verifier that a given
                                        spond to the secret transition relation. Our symbolic scheme             statement is true without revealing any information beyond
                                        assumes systems specified as linear guarded commands. We                 the validity of the statement itself. They are widely used in
                                        apply Farkas’ lemma to obtain a witness for the validity of the          areas such as blockchain systems, privacy-preserving authen-
                                        ranking function and employ sigma protocols with folding to              tication, secure electronic voting, and confidential data access
                                        efficiently convince the verifier of the witness’s existence. We         control. In the context of system verification, they offer the
                                        built a prototype to demonstrate the practical efficacy of our           opportunity to demonstrate compliance with formal specifica-
                                        two schemes on linear temporal logic verification examples.              tions while preserving confidentiality, as correctness claims
                                        Our technology enables formal verification in domains where              can be validated without disclosing system internals or pro-
                                        both the safety and the confidentiality of the system under              prietary designs. Despite their maturity and broad adoption in
                                        analysis are critical.                                                   multiple domains, the application of zero-knowledge proofs
                                                                                                                 to formal verification remains rare [49–51].
                                        1    Introduction                                                           We introduce the first approach to model checking in zero
                                                                                                                 knowledge: Zero-Knowledge Model Checking (ZKMC). Our
                                        Model checking is the problem of determining whether a soft-             method combines proof-theoretic model checking with zero-
                                        ware, hardware, or cyber-physical system satisfies a formal              knowledge proofs to construct a proof certificate that the
                                        specification of correctness. Unlike traditional testing, which          system satisfies the specification and then convince an exter-
                                        is inherently non-exhaustive, model checking provides formal             nal verifier that our public artefacts—the specification and the
                                        proof that the system behaves as intended [4, 7, 15]. It is an           proof certificate—are valid with respect to our secret artefact—
                                        established standard in electronic design automation, protocol           the system under analysis—without revealing any information
                                        verification, and control software development in domains                about the system itself.
                                        where safety and security are highly critical. Moreover, it                 We consider the model checking of reactive systems with
                                        is increasingly viewed as a promising avenue for the safety              discrete state spaces against ω-regular specifications (Sec-
                                        assurance of AI systems. Formal proofs of correctness enable             tion 3), which subsume linear temporal logic (LTL) [55]. Fol-
                                        verifiable compliance with safety standards and foster trust             lowing the automata-theoretic approach [63, 64], we reduce
                                        between technology providers, regulators, and users.                     model checking to the language emptiness of the synchronous


                                                                                                             1
composition of the system with a Büchi automaton for the                  therefore highlight a trade-off between expressivity and per-
complementary specification; a certificate of this emptiness              formance, with the explicit-state and symbolic approaches
serves as our certificate of correctness. On this premise, we             addressing different use cases.
realise ZKMC through two complementary algorithms: one                       In summary, our contribution is threefold. First, we in-
explicit-state, one symbolic.                                             troduce the first framework for model checking in zero
    Our explicit-state algorithm (Section 4) assumes systems              knowledge, combining cryptographic principles with proof
represented as finite-state transition graphs whose states are            techniques for formal verification. Second, we present two
labelled with atomic propositions, i.e., as Kripke structures.            schemes that realise this framework: an explicit-state algo-
We associate the system with a proof certificate over its state           rithm for finite-state transition graphs and a symbolic algo-
space alongside an appropriate automaton. The task is to con-             rithm for guarded command languages, whose thousands of
vince an external verifier of the validity of the proof certificate       proof obligations we fold into a single instance with a one-
without revealing the system’s initial states or its transition           shot folding scheme. Third, we implement both schemes in a
relation. Our scheme employs KZG polynomial commitments                   prototype and demonstrate the practical efficacy of our frame-
with batch evaluation to ensure that any hypothetical state or            work on LTL model checking tasks applied to standard com-
transition that would violate the publicly disclosed proof cer-           munication and coordination protocols.
tificate cannot correspond to an actual initial state or transition
of the secret system. Upon successful verification, which is              2   Zero-Knowledge Model Checking
guaranteed by the standard cryptographic properties of poly-
nomial commitments [42], the proof of correctness follows                 We address the problem of convincing an external verifier that
by contraposition. Our proof is two group elements regardless             a state transition system M satisfies a temporal specification
of state-space size; prover work is quadratic in the number of            φ, denoted M |= φ, without revealing any information about
states of the system.                                                     the initialisation or the transition structure of M .
    Our symbolic algorithm (Section 5) assumes reactive sys-                 Our framework combines three complementary technolo-
tems represented over integer variables by guarded commands               gies. First, we require a proof certificate witnessing M |= φ
with linear constraints and integer coefficients, potentially             and that can be verified in polynomial time. Second, we em-
yielding very large or infinite state spaces. We require state            ploy a commitment scheme that binds to M while keeping
propositions to be expressed as Boolean combinations of lin-              it hidden, ensuring that the system is uniquely identifiable
ear inequalities, and ranking functions as piecewise linear               through its cryptographic commitment. Third, we use a zero-
functions; from these, we derive proof obligations in a uni-              knowledge proof scheme to convince an external verifier that
form form, each with a secret component corresponding to                  (1) the proof certificate is valid and (2) it correctly corre-
the coefficients of the system. The task is to convince an                sponds to M and the specification φ, without revealing any
external verifier that every obligation holds without reveal-             information about the system M .
ing its secret component. Our scheme computes a Farkas                       A formal certification scheme is an algorithm Cert(M , φ)
witness for each obligation and employs specialised sigma                 that takes as input a secret encoding of the state transition
sub-protocols for the relevant operations over two-tier Peder-            system M and a public correctness specification φ, and re-
sen commitments [18]; it then folds all proofs into a single              turns a public certificate vφ that M satisfies φ. Crucially, we
instance, amortising the cost over the whole, possibly very               require the certification to be sound with respect to the model
large, batch of obligations. Upon successful verification, we             checking problem, in the sense that
obtain a zero-knowledge proof of correctness for the system
under analysis. Prover and verifier cost are independent of                                M ̸|= φ =⇒ Cert(M , φ) ̸⇝ vφ ,              (1)
the state-space size and polynomial in the number of guarded
                                                                          where Cert(M , φ) ⇝ vφ denotes that vφ is a valid output of
commands and automaton transitions.
                                                                          Cert(M , φ). We do not require the certification to be com-
    We developed a prototype implementation and evaluated
                                                                          plete for the model checking problem, a property that is de-
our two algorithms on a range of liveness verification tasks
                                                                          sirable but not essential to implement our framework. In-
(Section 6). Our benchmarks include a 3-way handshake pro-
                                                                          stead, we require that, given a certificate vφ , checking whether
tocol with exponential backoff, a model of DHCP, and a round-                          ?
robin scheduling algorithm. Our explicit-state algorithm can              Cert(M , φ) ⇝ vφ —that is, whether the certificate is valid—is
verify systems with up to approximately 212 states within                 decidable in polynomial time.
a 2 h time limit. Under the same time constraint, our sym-                   A cryptographic commitment to M under a security pa-
bolic algorithm handles significantly larger tasks, scaling to            rameter sp and randomness r is denoted by Com(sp, M ; r).
approximately 221 states. We emphasise that the explicit-state            To commit to M , a party samples r uniformly at random and
algorithm makes no assumptions about the structure of the                 computes the commitment cM = Com(sp, M ; r). The com-
system, whereas the symbolic algorithm requires the system                mitment can later be opened by revealing M and r; validity
                                                                                                                ?
to be expressed as linear guarded commands. These results                 is verified by checking whether cM = Com(sp, M ; r). We


                                                                      2
                                      φ                                  is false, or when M does not correspond to its commitment:
                          vφ
                 Cert                                            1
                                                                             M ̸|= φ ∨ cM ̸= Com(sp, M ; r)
                                          vφ , c M , π
   M                              P                          V                             =⇒ P [outV ⟨P (w, u), V (u)⟩ = 1] ≤ ε (3)
                 Com      cM                                     0       where outV ⟨·⟩ denotes the final output of V upon interaction
                 secret
                                                                         with P . Moreover, an honest prover can always convince
                                                                         the verifier when it possesses a valid certificate; a negative
         Figure 1: Non-Interactive ZKMC Scheme                           outcome, however, does not imply that M ̸|= φ.
                                                                         Remark 2.2 (Specification- and Certification-Induced Leak-
require the commitment scheme to satisfy the standard cryp-              age). Our framework ensures that neither the commitment cM
tographic properties of hiding and binding. Informally, hiding           nor the proof π reveals any information about M . However,
ensures that cM reveals no information about M , while bind-             selecting a secure specification φ and certificate vφ remains
ing guarantees that it is infeasible to produce a commitment             the user’s responsibility. In the extreme case where the public
cM that can be opened to a different value M ′ ̸= M , thus               specification φ or the certificate vφ uniquely determine the
preventing equivocation [43, p. 188].                                    secret system M , any party capable of verifying the proof
  A zero-knowledge proof system for model checking is there-             could, in principle, reconstruct the system regardless of the
fore a zero-knowledge proof system for the proof of knowl-               protocol’s cryptographic guarantees. Developing systematic
edge R (w, u) below, in the standard sense [10] with secret              specification and certification schemes that mitigate this risk
witness w and public statement u:                                        constitutes an open problem, beyond the scope of this work.
                 w
          z }| { z }|   u                                                   Side channels arising from the prover’s computation,
  R = PoK{(M , r); (vφ , cM ) :
                           {                                             denial-of-service attacks, or attacks that combine our protocol
                                                                         with auxiliary channels (such as the timing of certificate gen-
                          ?                              ?
            Cert(M , φ) ⇝ vφ ∧ Com(sp, M ; r) = cM }. (2)                eration, which may depend on M ) are addressed by standard
                                                                         countermeasures in the literature.
In other words, given appropriate certification and commit-
                                                                            We instantiate our framework to LTL model checking in
ment schemes, our objective is to convince an external verifier
                                                                         Section 3 and present two alternative commitment and zero-
that we know a model M and randomness r consistent with
                                                                         knowledge schemes in Sections 4 and 5.
both the public certificate vφ and the public commitment cM ,
thereby demonstrating that we possess a system M satisfying
the public specification φ.                                              3    LTL Model Checking
   As illustrated in Fig. 1, we propose a non-interactive
scheme for zero-knowledge model checking, in which the                   We instantiate our framework to model checking systems
prover computes a proof π once, and the verifier checks it               with discrete, potentially infinite state spaces against LTL,
alongside the commitment cM and the certificate vφ .                     more generally ω-regular properties [52]. We leverage ω-
   We assume a probabilistic polynomial-time adversary                   automata and proof certificates expressed as ranking functions
that may corrupt either party. The cryptographic guarantees              to design a certifier, thereby laying the foundations for our
of our framework follow the standard formulation of zero-                two alternative ZKMC algorithms in Sections 4 and 5.
knowledge proofs: completeness guarantees that an honest                    A nondeterministic state transition system M that executes
prover can always convince the verifier when the statement is            over an infinite time horizon on a discrete state space S is
true, soundness ensures that the verifier detects any attempt            defined in terms of an initial condition S0 ⊆ S and a transition
by a malicious prover to establish a false statement except              relation T ⊆ S×S. An execution of M is any infinite sequence
with negligible probability ε, and zero knowledge against an             of states (si ∈ S)i∈N such that s0 ∈ S0 and (si , si+1 ) ∈ T for all
honest-but-curious verifier with respect to the protocol tran-           i ∈ N. We verify temporal logic specifications over a finite set
script ensures that no information beyond the validity of the            of atomic propositions Π, and denote by Σ = 2Π the alphabet
statement is revealed.                                                   of all possible observations over states. For a state s, we write
                                                                         ⟨⟨s⟩⟩ ∈ Σ for the set of propositions that hold in that state.
Remark 2.1 (Soundness and Completeness). We stress that                  Each execution (si )i∈N then induces a trace defined as the
soundness and completeness for the certifier with respect to             infinite sequence (⟨⟨si ⟩⟩)i∈N , representing the corresponding
the model checking problem are distinct from those of the                observable behaviour. Finally, we define the language LM ⊆
zero-knowledge proof system with respect to the commitment               Σω of M as the set of all traces induced by its executions.
and certification itself, and must not be conflated. Under our
definitions, a malicious prover P cannot, except with negligi-           Example 3.1 (3-Way Handshake with Exponential Backoff).
ble probability ε, convince a verifier V that M |= φ when this           The 3-way handshake protocol with exponential backoff is a


                                                                     3
                         Wait                   Wait                   Wait                  Wait
                   delay = 28 − 1         delay = 28 − 1         delay = 28 − 1        delay = 28 − 1
                   done = 0               done = 1               done = 2              done = 3


                                                                                             syn




                                                                                                             sy
                                                                        syna      syn            ac
                                                                                     ack




                                                                                                                na
                                                                            ck                        k




                                                                                                                  ck
                                                Wait                                                                       ack
                                          delay = 27 − 1
                                          done = 1                                synack

             syn         Wait                                          synack                                                                           true              Wait




                                                           syn
    Closed         delay = 26 − 1                                                                                      Established
                   done = 0
                                      n
                                    sy


                                                                       syna
                                                                           ck        ack       ack
                                                                                                                                                                   Wait




                                                                                                               k
                                                                                  syn                                                                    q0                q1




                                                                                                            ac
                                                                                            syn




                                                                                                             n
                                                                                                          sy
                         Wait                   Wait                   Wait                  Wait
                   delay = 0              delay = 0              delay = 0             delay = 0
                   done = 0               done = 1               done = 2              done = 3


                                                                    Exhausted
                                                                 done = 3

                                                           (a)                                                                                                   (b)

      Figure 2: (a) 3-Way Handshake with Exponential Backoff and (b) Nondeterministic Büchi Automaton for FG Wait


mechanism for establishing a persistent connection between                                                 a transition relation δ ⊆ Q × Σ × Q, with the set of fair (or
two parties. It is implemented in numerous communication                                                   accepting) transitions F ⊆ δ. An input trace (σi )i∈N is ac-
protocols, such as TCP [57, p. 30], and provides a paradig-                                                cepted by A if and only if there exists an infinite sequence of
matic example of a model checking problem. Figure 2a il-                                                   states (qi ∈ Q)i∈N such that q0 ∈ Q0 and (qi , σi , qi+1 ) ∈ δ for
lustrates the protocol from the initiator’s perspective. The                                               all i ∈ N, and infinitely many fair transitions are visited, i.e.,
                                                                                                                                          1
initiator begins by sending a syn message and waits for the lis-                                           ∑∞i=0 1F (qi , σi , qi+1 ) = ∞ . The language LA of the automaton
tener to respond with a synack. Upon receiving this response,                                              A is the set of all traces it accepts. For every LTL formula
the connection is established, and the initiator responds with                                             φ, one can construct (using appropriate algorithms [27]) a
ack while transmitting data. The waiting time is sampled                                                   nondeterministic Büchi automaton Aφ such that LAφ = Lφ .
randomly (modelled nondeterministically), initially from the                                                  We adopt the standard automata-theoretic approach to LTL
range [0, 26 − 1]. If no synack is received, the syn message                                               model checking [64]. We first construct a nondeterministic
is retransmitted and the waiting time is resampled from a                                                  Büchi automaton A¬φ for the complementary specification
range of double size. This process is repeated for at most                                                 ¬φ, and then reduce model checking to the language empti-
three attempts in this example. In our model, the system state                                             ness problem LM ∩ LA¬φ = 0.        / Since LA¬φ = Σω \ LAφ , this is
is determined by four mutually exclusive Boolean variables                                                 equivalent to the language inclusion LM ⊆ LAφ , which in turn
Closed, Wait, Established, and Exhausted, an 8-bit un-                                                     coincides with LM ⊆ Lφ , that is, precisely the original model
signed integer delay, and a 2-bit unsigned integer done. The                                               checking question M |= φ.
variables delay and done are relevant only when the system                                                    Our goal is to convince an external verifier that M |= φ
is in state Wait.                                                                                          and, prior to executing our zero knowledge protocol, we re-
                                                                                                           quire an appropriate certificate that no trace of M is accepted
   An LTL formula φ over the atomic predicates Π extends                                                   by A¬φ . This amounts to certifying that no execution of the
propositional logic with temporal operators: the next opera-                                               synchronous composition of M and A¬φ is fair, which estab-
tor Xφ indicates that φ holds at the next step; the eventually                                             lishes that its language LM ∩ LA¬φ is empty. We define a fair
(finally) operator Fφ indicates that φ holds at some time in                                               execution of the synchronous composition of M and A¬φ as
the future; the always (globally) operator Gφ indicates that φ                                             any infinite sequence ((si , qi ) ∈ S × Q)i∈N over the composed
holds at all future times; the until operator φ1 Uφ2 indicates                                             state space such that (i) s0 ∈ S0 and q0 ∈ Q0 , (ii) (si , si+1 ) ∈ T
that φ1 holds continually until some future time where φ2                                                  and (qi , ⟨⟨si ⟩⟩, qi+1 ) ∈ δ for all i ∈ N, and (iii) fair transitions
holds [55]. We define the language Lφ ⊆ Σω of a specification                                              are visited infinitely often, i.e., ∑∞    i=0 1F (qi , ⟨⟨si ⟩⟩, qi+1 ) = ∞.
φ as the set of all traces (σi )i∈N that satisfy φ. The LTL model                                          Our objective is to show that no fair execution exists, which
checking problem M |= φ asks whether all traces of M satisfy                                               constitutes a fair termination problem [19, 34, 36, 63].
φ, which is the language inclusion problem LM ⊆ Lφ .                                                          Our certification scheme relies on a ranking function that
   We rely on the standard result that LTL is a special case of                                            assigns to each composed state an upper bound on the number
ω-regular specifications, and that every ω-regular specifica-                                              of fair transitions that can possibly occur along any execution
tion can be recognised by a nondeterministic Büchi automaton                                               starting from that state [63, Theorem 4.4].
A accepting the same language. Such an automaton is defined
by a finite set of states Q, with the initial states Q0 ⊆ Q, and                                                   1 For a set A, 1
                                                                                                                                      A denotes its indicator function.



                                                                                                    4
Theorem 3.2. Let Σ be a finite alphabet. Let M be a state                following piecewise-defined function:
transition system with state space S, initial condition S0 ⊆
S, transition relation T ⊆ S × S, and observation function                     V (· · · , q1 ) =
                                                                               
⟨⟨·⟩⟩ : S → Σ. Let A be a nondeterministic Büchi automaton                     
                                                                                 3 · 28                         if Closed
with state space Q, initial states Q0 ⊆ Q, transition relation
                                                                               
                                                                                    9           8
                                                                               2 + 1 − 2 · done + delay if Wait ∧ done ≤ 2
                                                                               
                                                                               
                                                                               
δ ⊆ Q × Σ × Q, and fair transitions F ⊆ δ. Suppose there
                                                                                  0                              if Established
exists a function V : S × Q → N ∪ {+∞} such that, for every                    
                                                                               0                                if Exhausted
s, s′ ∈ S and q, q′ ∈ Q, the following three conditions hold:
                                                                               
                                                                               
                                                                               
                                                                               
                                                                               +∞                               if Wait ∧ done = 3
                                                                                                (
         s ∈ S0 =⇒ q ∈ Q0 =⇒ V (s, q) ̸= ∞                    (4)                                 +∞ if Wait ∧ done = 3
         ′                                      ′
                                                                               V (· · · , q0 ) =
    (s, s ) ∈ T =⇒ V (s, q) ̸= ∞ ∧ (q, ⟨⟨s⟩⟩, q ) ∈ δ                                             3 · 28 otherwise
                                                              (5)
                               =⇒ V (s, q) ≥ V (s′ , q′ )
                                                         
                                                                            Overall, Corollary 3.3 forms the basis for a certification
    (s, s′ ) ∈ T =⇒ V (s, q) ̸= ∞ ∧ (q, ⟨⟨s⟩⟩, q′ ) ∈ F                  scheme for LTL model checking, in which the automaton and
                                                              (6)
                               =⇒ V (s, q) > V (s′ , q′ )                the ranking function jointly constitute the public certificate
                                                         
    |    {z      }   |            {z                  }                  vφ = (A¬φ ,V ). The existence of such a ranking function is
        secret                      public                               therefore a sufficient condition for a positive answer to the
                                                                         model checking problem. We remark that it is not a necessary
Then, LM ∩ LA = 0. / We call V a ranking function for the fair           condition in general; this affects only the completeness of our
termination of the synchronous composition of M and A .                  approach, not its soundness.
                                                                            Our framework thus requires a certifier that is checkable
                                                                         in polynomial time and admits a commitment and zero-
   Intuitively, the first condition ensures that all initial com-        knowledge proof scheme. We present two such strategies:
posed states are assigned a finite bound (base case), the second         an explicit-state approach that enumerates the state space
condition enforces monotonicity of the ranking function along            (Section 4), and a symbolic approach for transition systems
all transitions (inductive step), and the third condition guaran-        expressed as linear guarded commands (Section 5).
tees strict progress whenever a fair transition is taken, thereby
ruling out infinite fair executions (fair step).
                                                                         4     Explicit-State ZKMC
Corollary 3.3. Let M be a state transition system. Let φ be an           We assume that the state space of M is finite and that explicit
LTL formula and A¬φ be a nondeterministic Büchi automaton                enumeration is feasible, in the spirit of explicit-state model
recognising L¬φ . If there exists a ranking function for the fair        checking [40]. Our scheme proceeds in two phases. First, both
termination of the synchronous composition of M and A¬φ ,                parties enumerate all hypothetical states and transitions that
then M |= φ.                                                             can possibly violate the obligations of Section 3 using public
                                                                         information. Then, the prover convinces the verifier that none
                                                                         of the elements in these batches belong to the system without
Example 3.4 (Wait, but not Forever). An important correct-               revealing any secret information.
ness requirement for the protocol in Fig. 2a is that it must                The public information comprises the global state space S,
never get stuck when the listener is unreachable; in other               the automaton A¬φ (its states Q, initial states Q0 , transitions δ,
words, it should never wait forever. This liveness property is           and fair transitions F), and the ranking function V . The secret
naturally expressed in LTL by the formula ¬FG Wait, which                information, known only to the prover, is the system’s initial
rules out executions in which the system eventually remains              states S0 and transition relation T .
in the waiting state indefinitely. Figure 2b depicts a Büchi                Our certification scheme proceeds by proving the three
automaton for the complementary property FG Wait. The au-                proof obligations of Theorem 3.2 by contraposition. Each
tomaton has two states and three transitions in total, one of            obligation has the form of an implication with a secret premise
which is fair (the self-loop on q1 , shown with a double mark).          and a public consequent. We therefore negate the public con-
Our criteria require a ranking function V over the combined              sequent to identify batches of states that violate it, and then
state variables of the system and the automaton to take finite           prove that none of these states satisfy the secret premises
values on all reachable states. In automaton state q0 , all tran-        given by S0 and T .
sitions are permitted, and V is required to be non-increasing               Both parties enumerate the following three batches of states,
along every transition. In contrast, state q1 restricts the analy-       which are the hypothetical states and transitions violating the
sis to only the transitions in Wait and requires V to decrease           consequence of our obligations:
strictly, thereby certifying that the system can remain in Wait
only for a finite duration. A suitable ranking function is the               Binit = {s | ∃q. q ∈ Q0 ∧V (s, q) = ∞}                     (7)


                                                                     5
Prover Input: Secret polynomials pS0 , pT , randomness rS0 , rT
Common Input: Security parameter 1λ , degree bound t, certificate vφ = (A¬φ ,V )
                                                                          Setup Phase (both parties)
sp ← kzg.Setup(1λ ,t)
                                               Prover                                                                                Verifier
Compute Einit , Estep , Efair from vφ                                                 Compute Einit , Estep , Efair from vφ
cS0 ← kzg.Commit(sp, pS0 ; rS0 )                                                      receive cM = (cS0 , cT )
cT ← kzg.Commit(sp, pT ; rT )                                                         ..................................................................................
send cM = (cS0 , cT )                                                                 receive π = (πS0 , πT )
..................................................................................                                          ?
                                                                                      kzg.Verify(sp, cS0 , Einit , 0, πS0 ) = 1
πS0 ← kzg.Prove(sp, pS0 , cS0 , rS0 , Einit , 0)                                                                                  ?
πT ← kzg.Prove(sp, pT , cT , rT , Estep ∪ Efair , 0)                                  kzg.Verify(sp, cT , Estep ∪ Efair , 0, πT ) = 1
send π = (πS0 , πT )                                                                  accept


                                              Figure 3: Construction of our Explicit-State ZKMC Scheme


  Bstep = {(s, s′ ) | ∃q, q′ .V (s, q) ̸= ∞ ∧ (q, ⟨⟨s⟩⟩, q′ ) ∈ δ                      In other words, checking that a public batch B of states or
                                                                  ′   ′
                                               ∧V (s, q) < V (s , q )} (8)             transitions has empty intersection with its secret counterpart
                                                                                       is equivalent to proving that a certain polynomial p evaluates
  Bfair = {(s, s′ ) | ∃q, q′ .V (s, q) ̸= ∞ ∧ (q, ⟨⟨s⟩⟩, q′ ) ∈ F
                                                                                       to zero over the corresponding evaluation points E.
                                               ∧V (s, q) ≤ V (s′ , q′ )} (9)              From KZG, we only need the special case in which the
Our prover must then convince the verifier that                                        committed polynomial vanishes on a public evaluation set,
                                                                                       captured by the relation
   S0 ∩ Binit = 0,
                /           T ∩ Bstep = 0,
                                        /            T ∩ Bfair = 0,
                                                                 / (10)                                                                
                                                                                                                (p, r p ); (c p , E) : 
without revealing the secret S0 and T while committing to                                          Reval = PoK c p = Com(sp, p; r p )∧
                                                                                                                    ∀e ∈ E, p(e) = 0
                                                                                                                                       
them, which is a set membership task. Crucially, Binit , Bstep ,
and Bfair are fully determined by public information.                                  Our scheme uses a prover kzg.Prove(sp, p, c p , r p , E, 0) →
   Polynomial commitment schemes are a common candidate                                π that produces a proof π for Reval , and a verifier
to realise set membership tasks, and we use the KZG scheme                             kzg.Verify(sp, c p , E, 0, π) → {0, 1} that accepts if and only if
with Pedersen-style randomisation and batch evaluation [42].                           π is valid—that is, the polynomial committed in c p vanishes
We first embed states and transitions into a field, and then                           on every point of E. The batch zero-check can be viewed as a
reduce the disjointness obligations to the vanishing of two                            special case of standard KZG batch opening [42], where all
committed polynomials.                                                                 evaluation values are zero, allowing the proof to be expressed
   We associate the state space S and the transition space S × S                       solely via divisibility by the vanishing polynomial.
with two public embeddings e1 : S → F and e2 : S × S → F                                  KZG requires a trusted setup that produces a structured ref-
into an appropriate field F. Both embeddings are fixed, public,                        erence string of powers of a secret τ in the bilinear group; we
and injective, allowing both parties to independently compute                          assume this setup is executed honestly (e.g., via a multi-party
the evaluation points for Binit , Bstep and Bfair .                                    powers-of-tau ceremony) and treat the resulting common ref-
   Our prover computes two secret polynomials on F: a poly-                            erence string as part of the public parameters sp. Soundness
nomial pS0 derived from the set of initial states, and a poly-                         rests on the q-strong Diffie–Hellman assumption over bilinear
nomial pT derived from the transition relation of the system.                          groups [42].
These polynomials satisfy the following properties:                                       The KZG scheme satisfies the standard properties of com-
                                                                                       pleteness, polynomial binding, evaluation binding, and poly-
                      ∀s ∈ S : 1S0 (s) = pS0 ◦ e1 (s)                     (11)
                                                                                       nomial hiding; used as a zero-knowledge proof, the scheme
                      ′      2            ′                   ′
               ∀(s, s ) ∈ S : 1T (s, s ) = pT ◦ e2 (s, s )                (12)         additionally provides knowledge soundness and zero knowl-
                                                                                       edge in the sense of Section 2.
where, without loss of generality, we assume that the underly-                            We present our construction in Fig. 3, which directly ap-
ing field F contains the elements 0 and 1.                                             plies polynomial commitments to establish that M |= φ. It
   The prover and the verifier operate directly over the field                         implements the following proof of knowledge:
F. In particular, they construct the public encodings Einit =                                                                                                      
e1 [Binit ], Estep = e2 [Bstep ], and Efair = e2 [Bfair ], where f [A] in-                         
                                                                                                     (pS0 , pT , rS0 , rT ); (cS0 , cT , Einit , Estep , Efair ) : 
                                                                                                                                                                    
                                                                                                                    Eq. (13) ∧ Eq. (14)∧
                                                                                                                                                                   
dicates the image of a set A through f . The prover’s objective                         Re = PoK
is then to convince the verifier, without revealing the secret                                     
                                                                                                                 Com(sp, pS0 ; rS0 ) = cS0 ∧                       
                                                                                                                                                                    
                                                                                                                    Com(sp, pT ; rT ) = cT
                                                                                                                                                                   
polynomials pS0 and pT , that the following conditions hold:
                                                                                       This construction composes several zero-knowledge sub-
                    ∀e ∈ Einit : pS0 (e) = 0                              (13)
                                                                                       proofs, each executed with independent randomness, and in-
                    ∀e ∈ Estep ∪ Efair : pT (e) = 0                       (14)         herits its security properties from the polynomial commitment


                                                                                   6
scheme. Soundness follows from binding and evaluation-                       Since all variables are integer, negated non-strict inequalities
binding: a cheating prover cannot produce accepting proofs                   can be encoded as non-strict inequalities as well, by applying
unless the committed polynomials actually vanish on the eval-                an appropriate offset of 1.
uation sets, which by construction implies S0 ∩ Binit = 0/ and                 We allow ranking functions to be specified separately for
T ∩ (Bstep ∪ Bfair ) = 0.
                       / Zero knowledge follows from poly-                   each automaton state as piecewise linear functions [17,56,62]
nomial hiding and from the fact that all proof elements are                  defined over polyhedral regions:
masked by randomness. Completeness is immediate from
                                                                                                     (q)      (q)             (q)       (q)
completeness of the underlying scheme.                                                              w1 x + u1              if C1 x ≤ d1
                                                                                                    
                                                                                                       ..
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                       .
Complexity The cost of our explicit-state scheme is dom-
                                                                                                    
                                                                                                    
                                                                                                    w(q) x + u(q)
                                                                                                                              (q)
                                                                                                                            if Cm x ≤ dm
                                                                                                                                         (q)
inated by the polynomial pT , whose degree is O (|S|2 ) be-                              V (x, q) =
                                                                                                      m        m
                                                                                                                                               (18)
                                                                                                                               (q)       (q)
cause its evaluation domain ranges over all state pairs in                                          
                                                                                                    
                                                                                                    +∞                     if E1 x ≤ f1
S × S. Committing to pT and generating the batch evaluation
                                                                                                    
                                                                                                       ..
                                                                                                         .
                                                                                                    
proof therefore take time O (|S|2 ), and the total batch size
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                                               (q)       (q)
                                                                                                    
                                                                                                     +∞                     if El x ≤ fl
                                                                                                    
|Einit | + |Estep | + |Efair | grows accordingly. The certificate it-
self, however, remains succinct: the batch evaluation feature
of the KZG scheme produces a proof consisting of just two                    To ensure soundness, we require the case constraints to define
group elements, regardless of the size of the state space.                   a total function with a non-negative codomain. Accordingly,
                                                                             the verifier must check that the case constraints are (i) pair-
                                                                             wise disjoint, (ii) jointly cover the entire state space, and (iii)
5    Symbolic ZKMC                                                           ensure that the function takes non-negative values on its entire
                                                                             domain S × Q. Since the function is public, all of these checks
We allow the state space of M to be arbitrarily large, poten-                can be carried out using standard constraint-solving or SMT
tially countably infinite, and adopt a symbolic approach to                  solving techniques [8, 24, 45].
certification, in the spirit of symbolic model checking [13].                   The conditions of Theorem 3.2 give rise to proof obliga-
We require the state transition system to be expressed over in-              tions that can be expressed as Boolean combinations of linear
teger variables, via guarded commands with linear constraints.               inequalities. In particular, the initiation condition requires the
Under this setting, we present a certifier that leverages Farkas’            ranking function to be finite on all initial states; equivalently,
lemma to establish the validity of a ranking function as in                  for every initial automaton state q ∈ Q0 and every infinite case
Section 3, and a zero-knowledge proof scheme based on range                  k = 1, . . . , l, no initial state may satisfy the case constraint:
proofs and matrix multiplication proofs.
   We consider systems specified programmatically using                                                               (q)        (q)
                                                                                                A0 x ≤ b0 =⇒ Ek x ̸≤ fk                        (19)
guarded command languages [5, 48], and restrict our atten-                                      | {z }
                                                                                                  x∈S0
tion to systems over integer variables and coefficients, whose
initialisation and update commands are linear:
                                                                                The condition of the inductive step requires that finite-
    S0 = {x | A0 x ≤ b0 }                                         (15)       ness of the ranking function be preserved across transitions.
                                                                         Thus, for every guarded update i = 1, . . . , n, every automaton
               ′        x                 x                                  transition (q, σ, q′ ) ∈ δ, and every finite case j = 1, . . . , m, no
    T = {(x, x ) | A1 ′ ≤ b1 ∨ · · · ∨ An ′ ≤ bn }                (16)
                       x                  x                                  successor state may satisfy an infinite case k = 1, . . . , l:
                   |     {z }          |   {z  }
                     guarded update1            guarded updaten                             "      #    "      #
                                                                                              P(σ)        r(σ)
                                                                                  
                                                                                  x                                (q′ ) ′  (q′ )
We denote by x the variables in the current state and by x′                    Ai ′ ≤ bi =⇒    (q) x ≤     (q) =⇒ Ek x ̸≤ f k
                                                                                  x           Cj         dj
those in the next state. The initialisation is given by a single               | {z }       |        {z        }
system of linear inequalities A0 x ≤ b0 , whereas the transition                  (x,x′ )∈T          ⟨⟨x⟩⟩=σ∧V (x,q)̸=∞
relation is the union of n guarded update rules, each specified                                                                            (20)
as a system of linear inequalities Ai [x x′ ]T ≤ bi over both the                Finally, for every guarded update i = 1, . . . , n, every au-
current and the next state, for i = 1, . . . , n.                            tomaton transition (q, σ, q′ ) ∈ δ, and every pair of finite cases
   We represent automata explicitly and assume that each                      j, k = 1, . . . , m, we require the following ranking condition:
atomic predicate in Π corresponds to a linear inequality over
the state variables x. Consequently, every valuation σ ∈ Σ of                                            ⟨⟨x⟩⟩=σ∧V (x,q)̸=∞∧V (x′ ,q′ )̸=∞
atomic predicates induces a system of linear inequalities:                         (x,x′ )∈T z            }|    (σ) {
                                                                                z  }|
                                                                                       {      P(σ)  0          r
                                                                                   x           (q)         x    (q) 
                  σ = ⟨⟨x⟩⟩ ⇐⇒ P(σ) x ≤ r(σ)                      (17)          Ai ′ ≤ bi =⇒ C j    0  ′ ≤ dj 
                               |     {z    }                                       x                 (q′ )
                                                                                                               x    (q′ )
                                       atomic predicates                                        0   Ck            dk

                                                                         7
                           i 
                   (q′ )     x       (q′ )                                [0, M] represents the non-negative integers and [p − M, p − 1]
   h
                                           (q)
 =⇒ w(q)
     j         −wk             ′ ̸≤ uk − u j + 1F (q, σ, q′ ) − 1
                             x                                            represents the negatives [−M, −1], so that field arithmetic
                                                                          preserves integer semantics without wraparound on values
   |                                 {z                         }
                      V (x,q)−V (x′ ,q′ )>1F (q,σ,q′ )−1                                                     √
                                                               (21)       whose magnitudes stay below p. For our benchmarks, a
                                                                          255-bit prime with M = 232 keeps the relevant products AT     s λs
                                                                          and bT              ′ · M 2 ≈ 274 ≪ p, where n̂′ is the number of
Specifically, the term 1F (q, σ, q′ ) − 1 evaluates to −1 when                  s λs below  n̂
(q, σ, q′ ) ∈ δ\F, encoding the non-increase requirement of the           rows of As . Our certification scheme therefore computes two
general inductive step, and to 0 when (q, σ, q′ ) ∈ F, encoding           secret integer Farkas witnesses λs , µs ∈ [0, M]. Their existence
the strict decrease requirement on fair transitions.                      suffices to establish the corresponding obligation in Eq. (22)
   Overall, this construction yields l · |Q0 | obligations of the         but is not necessary: the dual system may admit only rational
form of Eq. (19), n·m·l ·|δ| obligations of the form of Eq. (20),         or out-of-bound solutions, which affects the completeness of
and n · m2 · |δ| obligations of the form of Eq. (21). For nota-           our approach but not its soundness. Accordingly, our scheme
tional convenience, we collapse [x x′ ] into a single vector y            requires the prover to demonstrate in zero knowledge that the
and observe, assuming appropriate zero padding where nec-                 secret certificates satisfy:
essary, that all obligations can be expressed in the following
                                                                                                            matrix multiplication
uniform form:                                                                                z                   }|                     {
                                                                          λs , µs ∈ [0, M] ∧ −bT λ
                                                                                               s s − h T
                                                                                                         µ
                                                                                                       p s − 1 ∈ [0, M] ∧ AT
                                                                                                                             λ s = −GT
                                                                                                                                       µs
         ∀y : As y ≤ bs =⇒ Cp y ≤ dp =⇒ Ep y ̸≤ fp             (22)       |                     {z                    } |s        {z p }
                                                                                             range proof                            equality proof
   ⇔ ¬∃y : As y ≤ bs ∧ Cp y ≤ dp ∧ Ep y ≤ fp                   (23)                                                                             (25)
           | {z }      |         {z        }
                 secret                         public
                                                                             Each obligation of the form of Eq. (25) comprises three
Equivalently, each derived obligation can be viewed as an                 classes of operations: (i) matrix–vector multiplications and ad-
unsatisfiability query of the form of Eq. (23), consisting of             ditions, (ii) range membership proofs, and (iii) equality proofs.
a public and a secret component. Our goal is therefore to                 This decomposition suggests a modular approach that favours
convince the verifier that each such query is unsatisfiable,              prover efficiency: we design a specialised zero-knowledge
without revealing the secret component.                                   sub-protocol for each class, prove each independently and
   Each obligation of the form of Eq. (23) asserts the infeasi-           then compose them into a single zero-knowledge proof.
bility of a system of linear inequalities—a universal statement              Since we operate over matrices and vectors, we need a
over all y. Rather than proving this directly, we pass to its dual        commitment scheme that exposes their row and column struc-
formulation, whose satisfiability certifies the infeasibility of          ture to the sub-protocols. We meet this requirement with the
the primal system:                                                        two-tier Pedersen vector commitment of [18], which lifts the
                                                                          standard Pedersen commitment [54] to matrices via a bilin-
                                    GT
                                     p                                    ear pairing. The standard scheme commits to a scalar v ∈ Z p
                                                                          under randomness r ∈ Z p as Com(v; r) = gv hr for public gen-
                            z }| {
  ∃λs ≥ 0, µs ≥ 0 : AT        T T
                     s λs + [Cp Ep ] µs = 0
                                                                          erators g, h ∈ G1 ; it is perfectly hiding, computationally bind-
                                    ∧ bT        T T
                                       s λs + [dp f p ] µs < 0 (24)       ing under the discrete-logarithm assumption, and additively
                                                                          homomorphic: Com(v; r) · Com(v′ ; r′ ) = Com(v + v′ ; r + r′ ).
                                              | {z }
                                                     hT
                                                      p
                                                                          The vector extension uses independent generators g1 , . . . , gn
By Farkas’ lemma, the unsatisfiability of the primal system               to commit to v ∈ Znp as Com(v; r) = hr ∏ni=1 gvi i , preserving
in Eq. (23) over the rationals is equivalent to the existence of          all three properties.
a rational solution for λs and µs [30].                                      The matrix extension, in turn, works over a bilinear group
   The remainder of this section develops our zero-knowledge              (G1 , G2 , GT ) of prime order p with pairing e : G1 × G2 →
proof scheme in two steps. We first introduce specialised sub-            GT [11, 33]. Bilinearity, e(ga , g′b ) = e(g, g′ )ab , lets us aggre-
protocols for the classes of operations that constitute each              gate column-level commitments in G1 into a single matrix-
obligation (Section 5.1). We then fold the many obligations               level commitment in GT that still binds to each column. Con-
of a verification task into a single instance, to which these             cretely, each column a j of A ∈ Zm×n p      is committed as a vector
primitives are applied only once (Section 5.2).                           commitment c j ∈ G1 , and the columns are then aggregated
                                                                          into a matrix commitment ĉA = ∏nj=1 e(c j , g′j ) ∈ GT for pub-
                                                                          lic generators g′j ∈ G2 . We can thus open at the column level
5.1    Primitives
                                                                          (via c j ) or at the matrix level (via ĉA ) without re-committing.
While Farkas’ lemma guarantees the existence of rational                     Finally, to avoid the round-trip cost of interaction, we ap-
witnesses, our cryptographic routines operate over a prime-               ply the Fiat–Shamir transform [31] in the random oracle
order field Z p . We use the standard bounded encoding of                 model: each sub-protocol derives its challenges by hashing
signed integers [21,37]: for a bound M with M 2 ≪ p, the range            the prover’s first messages with a hash function H, which the


                                                                      8
                                                          zkeq.Prove                                                                                               zkeq.Verify
Input: (sp, {(c( j) , r( j) , A( j) )}kj=1 , (x, cx , rx ))                                            Input: (sp, {(c( j) , A( j) )}kj=1 , cx , π)
                                          ( j) k
Extract bases {ĝi }li=1 , {ĝs }m
                                 s=1 , {ĥ } j=1 , ĥx from sp                                         Parse (tx , {t ( j) }kj=1 , {zi }li=1 , wx , {w( j) }kj=1 ) from π
                                                        ( j)                                                                                          ( j) k
                                 ( j)                                                                  Extract bases {ĝi }li=1 , {ĝs }m    s=1 , {ĥ } j=1 , ĥx from sp
∀ j ∈ [1, k], ∀i ∈ [1, l] : ĝi ← ∏m
                                   s=1           (ĝs )Asi
                                                                                                                                               ( j)                ( j)
                 R                          R          R                                                                                                   Asi
∀i ∈ [1, l], ri ← Z p ; ∀ j ∈ [1, k], σ( j) ← Z p ; σx ← Z p                                           ∀ j ∈ [1, k], ∀i ∈ [1, l] : ĝi ← ∏m    s=1 (ĝs )
               r
tx ← ∏li=1 ĝi i · ĥσx x                                                                              e ← H(cx ∥c(1) ∥ · · · ∥c(k) ∥tx ∥t (1) ∥ · · · ∥t (k) )
                                        ( j)              ( j)                                                                      ( j)              ( j) ?
∀ j ∈ [1, k] : t ( j) ← ∏li=1 (ĝi )ri · (ĥ( j) )σ                                                    ∀ j ∈ [1, k] : ∏li=1 (ĝi )zi · (ĥ( j) )w         = t ( j) · (c( j) )e
                                                                                                               z               ?
e ← H(cx ∥c(1) ∥ · · · ∥c(k) ∥tx ∥t (1) ∥ · · · ∥t (k) )                                               ∏li=1 ĝi i · ĥwx x   = tx · cex
∀i ∈ [1, l] : zi ← ri + e · xi                                                                         accept
wx ← σx + e · rx
∀ j ∈ [1, k] : w( j) ← σ( j) + e · r( j)                                                                                                                           zkrp.Setup
return π = (tx , {t ( j) }kj=1 , {zi }li=1 , wx , {w( j) }kj=1 )
                                                                                                       Input: (λ, (m, n)) with l = m · n
                                                                                                          R               R                     R
                                                                                                       g ← G1 , g′ ← G2 , α, β ← Z p
                                                          zkrp.Prove
                                                                                                                                           αi−1
                                 ij r      a                                                           ∀i ∈ [1, l − 1] : gi ← g
Input: (sp, A, ĉA = ∏m,n
                      i, j=1 ĝi j ĥ , rA , M)
                                      A

Treat A ∈ Zm×n
             p     as vector v = (a11 , a12 , . . . , amn ) ∈ Zlp                                      h = gβ , h′ = g′β , ĥ = e(h, g′ )
                                                                                                                                                       j−1         n(i−1)
Extract g, h, {gi }l−1            m,n
                    i=1 , {ĝi j }i, j=1 , and g = g2 from sp
                                                α                                                      ∀i ∈ [1, m], j ∈ [1, n] : ĝi j = e(gα , g′α          )
(1. Compute Pedersen commitments on v)                                                                 Bullet.sp ← Bullet.setup(λ)
                   R
∀i ∈ [1, l], ri ← Z p , ci ← gvi hri                                                                   return sp = (m, n, g, g , g , h, h , ĥ, {gi }i=1 , {ĝi j }m,n
                                                                                                                                 ′ ′α       ′        l−1
                                                                                                                                                                   i, j=1 , Bullet.sp)
(2. Prove algebraic linkage between {ci }li=1 and ĉA )
Define f (X) = ∑li=1 vi X i−1                                                                                                                                      zkrp.Verify
z ← H(ĉA ∥c1 ∥...∥cl )
rz = ∑li=1 ri zi−1                                                                                     Input: (sp, ĉA , M, π)
                i−1
c = ∏li=1 czi = g f (z) hrz ,                                                                          Parse π = ({ci }li=1 , πeq , θ, πBullet )
                                                                                                                               ′   ′α      ′
                                                                                                   i−1 Extract bases g , g , h from sp
Define q(X) = f (X)−
                  X−z
                      f (z)
                                                                                 (q(X) = ∑l−1
                                                                                          i=1 qi X    )
   R                          qi µ
                                                                                                        z ← H(ĉA ∥c1 ∥...∥cl )
                                               rA −rz +µz α −µ
µ ← Z p , πeq = ∏l−1    i=1 gi h , θ = g                  (g )                                                          i−1
                                                                                                       c = ∏li=1 czi
(3. Prove that each component vi lies within range [0, M])
                                                                                                                     ′ −1 ?
πBullet ← Bullet.Prove(sp, {vi , ci , ri }i=1 , M)   l                                                 ĉA · e(c, g )         = e(πeq , g′α g′−z ) · e(θ, h′ )
                                                                                                                                                               ?
return π = ({ci }li=1 , πeq , θ, πBullet )                                                             Bullet.Verify(sp, {ci }li=1 , M, πBullet ) = 1

                                                                                                       accept


                                                                       Figure 4: Primitives of our Symbolic ZKMC Scheme


verifier can replay locally.                                                                                  xs , ys are secret: the first corresponds to the proof obligation
                                                                                                              A⊤             ⊤
                                                                                                                s λs = −Gp µs appearing in Eq. (25), and the second arises
Matrix Multiplication and Addition Our proto-                                                                 from the commitment cγ to −h⊤          p µs required by our protocol
col requires proofs of consistency for committed                                                              construction (see Fig. 5). We batch both operations using              the
matrix products. To realise them, we adopt the zero-                                                          routine zkeq.Prove sp, {(c( j) , r( j) , A( j) )}kj=1 , (x, cx , rx ) → π,
knowledge matrix multiplication protocol of zkMatrix [18]                                                     which outputs a proof that, for each j, the commitment c( j)
and only state its interface. It provides the routine                                                         with randomness r( j) opens to A( j) x, where x itself is com-
zkmm.Prove(sp, A, B, cA , cB , rA , rB ; rAB ) → (πAB , cAB ), which                                          mitted as cx using randomness rx . The verification algorithm
outputs a commitment cAB to the product AB together with a                                                    zkeq.Verify sp, {(c( j) , A( j) )}kj=1 , cx , π accepts if and only if
proof πAB that it is consistent with the committed operands,                                                  all commitments are consistent. The scheme implements the
verified by zkmm.Verify(sp, cA , cB , cAB , πAB ) → {0, 1}. The                                               following relation:
scheme implements the following relation:
                                                                                                                                                 (x, rx , {r( j) }kj=1 );
                                                                                                                                                                                 
                                                             
                      (A ∈ Zm×l              l×n
                              p , B ∈ Z p , rA , rB , rAB );
                                                                                                                                      
                                                                                                                                                                                 
                                                                                                                                                                                  
                                                                                                                                            {A( j) }kj=1 , cx , {c( j) }kj=1 :
                    
                                                                                                                                                                               
                    
                    
                                  cA , cB , cAB :
                                                              
                                                              
                                                                                                                      Rzkeq = PoK            ( j)                   ( j)    ( j) 
     Rzkmm = PoK            cA = Com(sp, A; rA )∧                                                                                     ∀ j.c = Com(sp, A x; r )
                                                                                                                                      
                                                                                                                                                                                 
                    
                    
                            cB = Com(sp, B; rB )
                                                              
                                                              
                                                                                                                                            ∧cx = Com(sp, x; rx )
                                                             
                         ∧ cAB = Com(sp, AB; rAB )
                                                             
                                                                                                              Conceptually, zkeq encodes the public matrices A( j) into the
Additions, by contrast, require no dedicated protocol: since                                                  commitment bases and reduces the statement to a proof of
the commitment scheme is additively homomorphic, proving                                                      discrete-logarithm equality [14].
and verifying a commitment to an addition can be carried out
solely using the commitment algorithms.                                                                       Range Proof Our obligation requires positivity checks over
                                                                                                              the range [0, M], as illustrated in Eq. (25), and bound checks
Equality Proof Our protocol requires two equality proof                                                       As , bs ∈ [−M, M] on signed coefficients. We reduce the signed
operations of the form ys = Ap xs , where Ap is public and                                                    checks to non-negative ones via the offset As + M ∈ [0, 2M]


                                                                                                     9
and bs + M ∈ [0, 2M] and prove that every entry of a commit-               which establishes all N proof obligations at once:
ted matrix lies in [0, M], captured by the following relation:                                                                                    
                                                                                        
                                                                                            ({Ai , bi , λi , µi , rAi , rbi , rλi , rµi }i∈[N] ); 
                                                                                                                                                   
                            (A ∈ Zm×n                                                         ({Gi , hi , cAi , cbi , cλi , cµi }i∈[N] , M) : 
                                                                                                                                                
                                   p , rA ); cA , M :
                                                                                        
  Rzkrp = PoK
                                                                                        
                                                                                                                                                  
                                                                                                                                                   
                     cA = Com(sp, A; rA ) ∧ ∀i, j : ai j ∈ [0, M]                                   ∀i ∈ [N] : Ai λi = Gi µi ∧
                                                                                        
                                                                                                                                                  
                                                                                                                                                   
                                                                                        
                                                                                                                                                  
                                                                                                                                                   
                                                                                            , µ  ∈ [0,  M]    ∧  b      +  h   µ  −   1  ∈ [0, M]∧
                                                                                                                                                  
                                                                                         λ
                                                                                         i i                       λ
                                                                                                                   i i        i i
                                                                                                                                                   
                                                                                                                                                   
To realise this relation, we provide the routine zkrp (Fig-                  Rf = PoK           Ai ∈ [−M, M] ∧ bi ∈ [−M, M]∧
ure 4), with prover zkrp.Prove(sp, A, cA , rA , M) → π and veri-                                    Com(sp, Ai ; rAi ) = cAi ∧
                                                                                        
                                                                                                                                                  
                                                                                                                                                   
                                                                                        
                                                                                                                                                  
                                                                                                                                                   
fier zkrp.Verify(sp, cA , M, π) → {0, 1}. We construct zkrp by                                       Com(sp,        b  ; r   )  =  c     ∧
                                                                                                                                                  
                                                                                                                      i bi           bi
                                                                                        
                                                                                                                                                  
                                                                                                                                                   
                                                                                                                                                  
flattening A and committing to each entry under an individ-                                         Com(sp,            ; r   )  =   c    ∧
                                                                                                                                                  
                                                                                        
                                                                                        
                                                                                                                   λ i λi            λi
                                                                                                                                                   
                                                                                                                                                   
                                                                                                                                                   
ual Pedersen commitment ci , then discharging two sub-tasks:                                          Com(sp, µi ; rµi ) = cµi
                                                                                                                                                  
per-element range checks on the ci , and a consistency check
that ties the {ci } back to the matrix commitment ĉA . The                Each family of Eq. (26) comprises N instances of a single
per-element non-negative checks are discharged by Bullet-                  relation, and zkmm proves one instance at a time. We thus
proofs [12], a logarithmic-size zero-knowledge proof for prov-             combine the N instances into a single pair of operands, sum-
ing range membership of values committed under Pedersen                    ming individual instances under random scalars. The natural
commitments: a prover Bullet.Prove(sp, {vi , ri , ci }ki=1 , M) →          candidate weights instance i by a power rci of a challenge
π and a verifier Bullet.Verify(sp, {ci }ki=1 , M, π) → {0, 1} es-          r that the prover derives by Fiat–Shamir, as in Section 5.1,
tablish that each ci = gvi hri commits to a value vi ∈ [0, M]. It          and sums the result into A∗ = ∑i rci Ai and λ∗ = ∑i rci λi . The
remains to certify that the per-entry commitments {ci } and                product of the two is:
the matrix commitment ĉA encode the same data. We adapt
the KZG opening technique [42]: we encode the entries as the                               A∗ λ∗ = ∑ r2ci Ai λi + ∑ rci +c j Ai λ j               (27)
                                                                                                       i              i̸= j
coefficients of a polynomial f whose exponents follow the                                            |     {z    }    |       {z        }
                                                                                                     diagonal terms       cross terms
matrix layout, so that an evaluation of f at a verifier-chosen
challenge z uniquely determines the underlying matrix. The                 The diagonal terms correspond to the instances we set out to
prover then produces a randomised KZG-style opening proof                  prove, each carried by its own power r2ci . The cross terms
for f (z) together with a blinding-correction term, and a single           multiply data from different obligations and correspond to
pairing equation certifies that ĉA and {ci } are consistent with          nothing in Eq. (26), yet the prover cannot discard them, be-
this opening. The resulting protocol is complete, knowledge-               cause the verifier checks the product that it computes from
sound in the algebraic group model with a random oracle, and               the folded commitments. Folding schemes [28, 44] resolve
zero-knowledge in the random oracle model; we sketch the                   this tension by absorbing the cross terms into the statement:
argument in Section B.                                                     the prover commits to them before it learns the challenge,
                                                                           and both parties then define the folded right-hand side to
5.2    Folding                                                             include them. Since only the sum of the cross terms shar-
                                                                           ing a power of r enters the check, one commitment per dis-
The primitives of Section 5.1 produce one obligation at a                  tinct exponent suffices. Writing K = {ci + c j | i ̸= j} for the
time, and a verification task can produce thousands of them                set of cross-term exponents, the prover sends a commitment
(Table 1). Every obligation, however, has the same shape and               to CkA = ∑ci +c j =k, i̸= j Ai λ j for every k ∈ K, and both parties
differs only in its data. We exploit this uniformity and fold all          take α∗A = ∑i r2ci αi + ∑k∈K rkCkA as the folded right-hand side,
obligations of a task into a single instance, so that the prover           which by Eq. (27) equals A∗ λ∗ exactly when every instance
runs the matrix multiplication sub-protocols once instead of               holds. The three remaining families fold in the same way.
N times. We index the obligations by i ∈ [N] and abbreviate                Every step combines committed values linearly, so the ver-
Ai = AT              T            T               T
        s,i , bi = −bs,i , Gi = −Gp,i and hi = −hp,i , so that the         ifier can recompute the folded commitments itself from the
multiplicative part of Eq. (25) becomes two secret–secret and              per-obligation commitments and the 4|K| cross-term com-
two public–secret families of matrix–vector products:                      mitments (via the homomorphic properties), and folds the
                                                                           public G∗ and h∗ in plaintext. One invocation of zkmm per
      Ai λi = αi , bi λi = βi       Gi µi = αi , hi µi = γi    (26)        secret–secret family and one of zkeq for the two public–secret
      |         {z          }       |        {z           }
            secret–secret                 public–secret                    families then replace the N per-obligation invocations; Fig. 5
                                                                           shows the resulting construction, which realises Rf .
Both groups share αi , which is what ties AT               T
                                              s,i λs,i = −Gp,i µs,i           It remains to choose the exponents ci : we call their public
together. The remaining conditions λi , µi , δi ∈ [0, M] and               assignment C = {c1 , . . . , cN } the exponent schedule, and its
Ai , bi ∈ [−M, M] constrain ranges, where δi = βi + γi − 1 is              choice decides whether folding is sound at all. Committing
the second range term of Eq. (25).                                         to a cross term binds the prover to that term but does not
   Our folding protocol realises the proof of knowledge below,             constrain its contents, as nothing requires CkA to hold the sum


                                                                      10
Prover Input: Secret matrices Ai = AT                            T
                                         s,i and vectors bi = −bs,i , randomness rAi , rbi , for every obligation i ∈ [N]
Common Input: Security parameter 1λ , public matrices Gi = −GT                                  T
                                                                       p,i and vectors hi = −hp,i , upper bound M, setup sp as in Fig. 4, exponent schedule C = {c1 , . . . , cN } with 2C ∩ K = ∅,
where K = {ci + c j | i ̸= j}, offset commitments cθ , c′θ to the all-M matrix/vector (randomness 0), shifting Ai , bi into [0, 2M]
                                                  Prover                                                                                            Verifier
Compute Farkas witnesses λi , µi for all i ∈ [N]                                                            receive C0
sample rλi , rµi , rαi , rβi , rγi                                                                           .........................................................................
∀i: α ← A λ , β ← b λ , γ ← h µ                                                                             receive {(cCA , cCb , cCG , cCh )}k∈K and π
       i           i i       i       i i    i           i i                                                                                                                 k      k      k            k
∀i: commit to Ai , bi , λi , µi , αi , βi , γi                                                                                             (two-tier Pedersen, Section 5.1) r ← H(C0 ∥{c A , c b , c G , c h }k∈K )
                                                                                                                                                                                                  Ck   Ck Ck   Ck
send C0 = {(cAi , cbi , cλi , cµi , cαi , cβi , cγi )}i∈[N]                                                                                                                          ∗      c          ∗      c
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . G ← ∑i r i G
                                                                                                                                                                                               c
                                                                                                                                                                                                  i , h ← ∑i r i hi
                                                                                                                                                                                              r i
∀k ∈ K: CkA ← ∑ci +c j =k, i̸= j Ai λ j                                                                                                             (aggregated cross terms) cA∗ ← ∏i cA , and cb∗ , cλ∗ , cµ∗ likewise
                                                                                                                                                                                               i
                                                                                                                                                                            2c                k
        and Ckb ,CkG ,Ckh likewise from bi λ j , Gi µ j , hi µ j                                                                                            cα∗ ← ∏i crαi i · ∏k∈K cr A
                                                                                                                                                              A                               Ck
sample ωAk , ωbk , ωG    h
                    k , ωk ; cCX ← Commit(sp,Ck ; ωk )
                                                      X      X
                                                                                                                                                            cα∗ , cβ∗ , cγ∗ likewise from cCG , cCb , cCh
                                            k                                                                                                                 G                                            k   k       k
send {(cCA , cCb , cCG , cCh )}k∈K                                                                                                                                                                                 ?
               k         k       k    k                                                                                                                     zkmm.Verify(sp, cA∗ , cλ∗ , cα∗ , πα ) = 1
r ← H(C0 ∥{cCA , cCb , cCG , cCh }k∈K )                                                                                                                                                                    A
                         k       k    k         k                                                                                                                                                                  ?
A∗ ← ∑i rci Ai , b∗ ← ∑i rci bi                                                                                                    (fold the witnesses)
                                                                                                                                                            zkmm.Verify(sp, cb∗ , cλ∗ , cβ∗ , πβ ) = 1
                                                                                                                                                                                                                               ?
λ∗ ← ∑i rci λi , µ∗ ← ∑i rci µi                                                                                                                                                                    ∗           ∗
                                                                                                                                                            zkeq.Verify(sp, {(cα∗ , G ), (cγ∗ , h )}, cµ∗ , πη ) = 1
                                                                                                                                                                                         G
rA∗ ← ∑i rci rAi , and rb∗ , rλ∗ , rµ∗ likewise                                                                                                             ∀i: cδi ← cβi · cγi · Commit(sp, −1; 0)
α∗A ← ∑i r2ci αi + ∑k∈K rk CkA                                                                                                                (= A∗ λ∗ )                                                                   ?
                                                                                                                                                            zkrp.Verify on {cλi , cµi , cδi , cAi cθ , cbi c′θ }i∈[N] = 1
α∗G , β∗ , γ∗ likewise from CkG ,Ckb ,Ckh                                                                                      (= G∗ µ∗ , b∗ λ∗ , h∗ µ∗ )
                                                                                                                                                            accept
rα∗ ← ∑i r2ci rαi + ∑k∈K rk ωAk , and rα∗ , rβ∗ , rγ∗ likewise
   A                                                          G
(πα , ·) ← zkmm.Prove(sp, A∗ , λ∗ , cA∗ , cλ∗ , rA∗ , rλ∗ ; rα∗ )
                                                               A
(πβ , ·) ← zkmm.Prove(sp, b∗ , λ∗ , cb∗ , cλ∗ , rb∗ , rλ∗ ; rβ∗ )
πη ← zkeq.Prove(sp, {(cα∗ , rα∗ , G∗ ), (cγ∗ , rγ∗ , h∗ )}, (µ∗ , cµ∗ , rµ∗ ))
                                           G        G
πrp ← zkrp.Prove on {cλi , cµi , cδi , cAi cθ , cbi c′θ }i∈[N]                                                                                (batched)
send π = (πα , πβ , πη , πrp )



                                                                               Figure 5: Construction of our Folding ZKMC Scheme


that it should. Equation (27) can be seen as a polynomial                                                                                        Theorem 5.1 (Soundness of Folding). Let the commit-
identity in the challenge: the coefficient at X 2ci is the residual                                                                              ment scheme be binding except with probability εbind , let
Ai λi − αi of obligation i, and the coefficient at X k with k ∈ K                                                                                zkmm, zkeq and zkrp be knowledge sound with knowledge
is the residual of the corresponding aggregate. If a diagonal                                                                                    errors εzkmm , εzkeq and εzkrp , let C satisfy Eq. (28), and
exponent 2ci would coincide with a cross-term exponent, a                                                                                        let n̂′ M 2 + n̂MG M + M + 1 < p, where MG bounds the en-
dishonest prover could cancel the residual of obligation i                                                                                       tries of Gp and hp , and n̂′ , n̂ are the dimensions of λi , µi .
against the aggregate that it chose freely at the same power,                                                                                    Then, from any accepting prover, one can extract for ev-
and the identity would hold for every challenge. An admissible                                                                                   ery i ∈ [N] integer witnesses bound to the per-obligation
schedule must therefore separate the two sets of exponents:                                                                                      commitments that satisfy Eq. (25), except with probability
                                                                                                                                                 O (maxi ci /p) + εzkmm + εzkeq + εzkrp + εbind .
  2C ∩K = ∅,                         i.e.           2ci ̸= c j +ck for all i and all j ̸= k (28)
A violated obligation then leaves a non-zero polynomial                                                                                             The wraparound condition is per obligation and indepen-
of degree at most 2 maxi {ci }, which the Schwartz–Zippel                                                                                        dent of N, which enters only through the Schwartz–Zippel
lemma [61, 65] confines to a 2 maxi {ci }/p fraction of the                                                                                      term; we present the proof in Section C.
challenges. Collisions within K remain harmless, which is
what permits the aggregation above. Condition Eq. (28) states                                                                                    Complexity Folding replaces the N invocations of zkmm
precisely that C contains no three-term arithmetic progres-                                                                                      and zkeq by one each. It costs 4|K| group elements in the
sion (i.e., C is a Salem–Spencer set [9, 29, 60]) and thereby                                                                                    certificate, O (N + |K|) exponentiations for the verifier, and
excludes the obvious schedule ci = i − 1; reading the binary                                                                                     N(N − 1) pairwise products for the prover. Because |K| grows
digits of i − 1 in base 3, by contrast, yields an admissible                                                                                     faster than N, the schedule also bounds how far a single fold
schedule with |K| < 3⌈log2 N⌉ .                                                                                                                  scales, and the batch size becomes a tuning knob: folding
   Folding leaves the range conditions of Eq. (26) untouched.                                                                                    a task in batches of B obligations trades ⌈N/B⌉ invocations
A folded witness is essentially uniform in Z p and would fail                                                                                    against O (NB0.59 ) cross-term commitments.
any range check, so we state every range proof on the per-
obligation commitments, where zkrp applies unchanged and
the checks on δi aggregate across all obligations into a single
                                                                                                                                                 6           Experimental Evaluation
Bulletproof [12], with the verifier deriving the commitment                                                                                      We implemented an end-to-end prototype2 of both the explicit-
to δi homomorphically as before. Separating the two layers                                                                                       state and symbolic algorithms and use it to investigate three
also preserves the integer encoding of Section 5.1: folding
argues purely over Z p , while the lift to Z stays per obligation.                                                                                     2 https://github.com/aiverification/zkmc




                                                                                                                                        11
            Table 1: Runtime and problem size comparison (OOT: > 2 h; “-”: not run; OOM: out of memory).
                                           Explicit-State ZKMC                     Symbolic (Folding) ZKMC
                                                       Runtime             Oblig-              Runtime
   Benchmark                |S| ∑⋆ |E⋆ | Enum. Setup Prover Verifier ations Farkas Setup Prover Verifier
   exb_i1a2                25      26.7 140 ms 40 ms 20 ms 20 ms             217      3s    630 ms 1 min    10 s
   exb_i2a2                2 6     28.6 420 ms 80 ms 40 ms 20 ms             217      3s    630 ms 1 min    10 s
   exb_i4a2                27     210.6     2s    260 ms 120 ms 40 ms        217      3s    620 ms 1 min    10 s
   exb_i2a3                27.6   211.8     4s    870 ms 380 ms 60 ms        260      3s    620 ms 1 min    10 s
   exb_i8a2                28     212.6     6s    870 ms 380 ms 70 ms        217      3s    620 ms 1 min    10 s
   exb_i4a3                28.6   213.8    14 s      3s      2s   160 ms 260          3s    630 ms 1 min    10 s
   exb_i8a3                29.6   215.8    57 s     12 s     6s   590 ms 260          3s    630 ms 1 min    10 s
   exb_i64a3               212.6 221.8 65 min 10 min OOM             -       260      3s    620 ms 1 min    10 s
   exb_i128a3              213.6     -    OOT         -       -      -       260      3s    620 ms 1 min    10 s
   exb_i64a4               214       -       -        -       -      -       303      4s    620 ms 1 min    10 s
   exb_i128a4              215       -       -        -       -      -       303      4s    620 ms 1 min    10 s
   dhcp_noOFF_7_2_7        2 10.1 2 18.7  3 min     12 s     6s     4s      1649     25 s     2s    15 min 2 min
   dhcp_noOFF_100_2_10 213.5         -    OOT         -       -      -      1649     25 s     2s    15 min 2 min
   dhcp_noOFF_1000_2_10 216.8        -       -        -       -      -      1649     25 s     2s    15 min 2 min
   dhcp_7_2_7              210.3 219.2 4 min        22 s     12 s   6s      2139     33 s     3s    20 min 2 min
   dhcp_noOFF_7_3_7        211.6 221.5 22 min 1 min          46 s  30 s     2252     35 s     3s    21 min 2 min
   dhcp_7_3_7              2 11.8  2 22  31 min 3 min 1 min        38 s     2847     43 s     4s    25 min 3 min
   dhcp_100_3_10           214.2     -    OOT         -       -      -      2847     43 s     4s    25 min 3 min
   dhcp_1000_3_10          217.6     -       -        -       -      -      2847     43 s     4s    25 min 3 min
   dhcp_10000_3_10         220.9     -       -        -       -      -      2847     43 s     4s    25 min 3 min
   dhcp_15_4_10            213.1     -    OOT         -       -      -      3693     58 s     5s    32 min 3 min
   dhcp_32_5_10            214.4     -       -        -       -      -      4689 1 min        8s    41 min 4 min
   rr_2                         24.2    28.6    330 ms 30 ms 10 ms 30 ms     678    7s   710 ms                   2 min    14 s
   rr_3                         26.3    213.3     3s   140 ms 70 ms 60 ms 3791     48 s    4s                    18 min   2 min
   rr_4                         28.3    217.3    1 min   2s   730 ms 330 ms 13746 3 min   36 s                   68 min   8 min
   rr_5                         210.2   220.9   33 min 22 s    12 s    3s   38427 11 min 4 min                   OOM        -


research questions. (RQ1) Can either scheme verify realistic            implementation of KZG10: it interpolates the membership
protocols within practical time and memory budgets? (RQ2)               polynomials pS0 and pT by inverse FFT and proves each of
How do the two schemes compare in scalability on these                  them on its full evaluation set with a single batched opening,
protocols (explicit-state in terms of state-space size, symbolic        whose quotient is likewise computed via FFT. The symbolic
in terms of the number of proof obligations)? (RQ3) In which            back-end instantiates zkmm with zkMatrix [18] and zkrp
settings is each scheme preferable?                                     with a bls12-381 Bulletproofs library [53]. The prover com-
   Our main finding is that the two approaches are comple-              putes the commitments to the secret matrices AT  s and vectors
mentary. The explicit-state scheme performs well on small               −bTs  (see Eq. (24)), along with their zkrp range proofs, once
systems with negligible setup cost but degrades quadratically           per distinct matrix and reuses them across obligations; the
in |S|. By contrast, the symbolic scheme scales to systems              verifier caches correspondingly. Obligations are discharged
with up to 220.9 states and 213.7 proof obligations within a            concurrently across cores, in batches of 200 to bound the
two-hour budget, albeit with a higher constant overhead.                memory footprint. A separate folding back-end implements
                                                                        the construction of Section 5.2 and folds all obligations of a
                                                                        task in one shot (B = N). We ran our benchmarks on AWS
Setup Our front-end includes a toy certifier input lan-                 EC2 c6g.8xlarge instances (32 vCPU, 64GiB RAM, ARM
guage for guarded-command programs, Büchi automata, and                 Graviton2) running Ubuntu 26.04.
piecewise-linear ranking functions, and computes batches and
obligations, using Z3 [23] to derive the Farkas witnesses. Our
front-end is written in Python; the zero-knowledge proto-               Benchmarks We evaluate on three communication and co-
cols are written in Rust and receive their input in JSON for-           ordination protocols, each parameterised so that the state
mat. The explicit-state back-end builds on the Arkworks [6]             space and the number of obligations scale independently,


                                                                   12
which lets us stress-test the two back-ends along separate                themselves (the obligations of Theorem 3.2) contain secret
axes. The benchmark exb_i⟨d⟩a⟨a⟩, presented in Figure 2,                  components. Moreover, our approach mandates commitments
has initial delay d ∈ {1, . . . , 128} and maximum attempt                to the system as a core component, preventing a malicious
count a ∈ {2, 3, 4}; the state space grows with d · a while               prover from replacing the system under analysis, whether
the number of obligations depends only on a, and we prove                 during, before, or after the proof. Privacy-preserving verifica-
that the protocol does not wait indefinitely. The benchmark               tion has also been explored through multi-party computation,
dhcp_⟨w1 ⟩_⟨a⟩_⟨w2 ⟩ models a client requesting a network ad-             with solutions for CTL model checking and runtime verifica-
dress [26, p. 13], with wait bounds w1 and w2 and at most a at-           tion [38, 41]; to the best of our knowledge, ours is the first
tempts in its exponential-backoff loop; variants tagged noOFF             implementation using zero-knowledge proofs.
omit a non-essential intermediate state, and we prove that the               The proof rule of Theorem 3.2 builds on results on fair
client either fails or is configured correctly without waiting            termination in nondeterministic Büchi automata [36, 63]. Our
indefinitely. The benchmark rr_⟨k⟩ models a k-process round-              schemes extend to alternative proof rules: generalised Büchi
robin scheduler whose state space and number of obligations               automata [46], other temporal specifications [19, 20], and, in
both grow rapidly with k, making it the most demanding fam-               principle, probabilistic model checking [1–3, 25, 39, 47] and
ily, and we prove that the scheduler is starvation-free.                  cyber-physical systems [58, 59]; the continuous domains of
                                                                          the latter two, however, entail a generalisation of our crypto-
Metrics For each instance we report the problem size |S|,                 graphic routines and remain future work.
with the embedding size ∑⋆ |E⋆ | for the explicit-state scheme               Linear programming duality, of which Farkas’ lemma is
and the obligation count for the symbolic scheme, and four                a special case, is a standard technique in ranking-function
timings covering the pipeline end-to-end: enumeration pro-                synthesis and verification [16,56], and zero-knowledge proofs
duces the JSON input (set enumeration and embedding for                   for linear-algebraic relations are well studied [12, 18]; our
the explicit-state scheme; Farkas witness extraction via Z3 for           approach is the first to use duality as the structural backbone
the symbolic scheme), setup generates the KZG or SRS pa-                  of a zero-knowledge proof.
rameters, prover performs commitment and proof generation,                   Folding admits alternative realisations: a recursive binary-
and verifier checks the proof.                                            tree fold in the style of Nova [44] scales better with the
                                                                          number of obligations at the cost of multiple folding rounds,
Discussion Table 1 shows the results. Below 211.8 states,                 whereas a multi-instance Lagrange-basis fold as in Proto-
the explicit-state scheme is preferable: it has lower setup,              Galaxy [28] also uses a single challenge but incurs higher
prover, and verifier times (e.g., exb_i4a3: 2 s vs. 1 min for             prover overhead; we adopt the progression-free one-shot fold
the symbolic prover), and its polynomial commitment yields a              of Section 5.2 for its simplicity. The underlying relation
constant-size certificate. This regime fits early-stage protocol          (Eq. (25)) is also SNARK-friendly and could be instantiated
design and hardware controllers. For larger systems, the sym-             directly with Groth16 or PlonK [32, 35], achieving constant-
bolic scheme is the only viable option: it proves and verifies a          size proofs and efficient verification at the cost of increased
220.9 -state DHCP instance (dhcp_10000_3_10) in under half                prover overhead; our tailored sub-protocols resolve this trade-
an hour, while the explicit-state scheme times out in enumera-            off in favour of the prover. In particular, the transformation
tion alone. The two schemes also differ in what they assume:              behind zkrp, which lifts batched Bulletproofs range proofs on
the explicit-state algorithms make no assumption on the struc-            Pedersen commitments [12] to the two-tier matrix commit-
ture of the model, whereas the symbolic algorithm requires                ment, integrates readily with existing Bulletproofs implemen-
systems to be expressed as linear guarded commands. The two               tations and may be of independent interest.
schemes are therefore complementary, trading expressivity
for performance.
                                                                          8   Conclusion
7   Related Work
                                                                          We have presented the first approach to model checking in
Prior work at the intersection of zero-knowledge proofs and               zero knowledge, enabling formal verification in scenarios
automated reasoning has proposed protocols for theorem prov-              where the confidentiality of the system is crucial. Our imple-
ing with different logical backends: zkUNSAT for proposi-                 mentation of the explicit-state and symbolic schemes, with
tional unsatisfiability [51], zkSMT for first-order unsatisfiabil-        its one-shot folding of proof obligations, has demonstrated
ity in decidable theories [50], and zkPi for interactive theorem          the practical viability of our new technology. Our work raises
proving [22, 49]. None of these approaches performs model                 many scientific questions, from the security implications re-
checking: they establish the validity of public logical state-            lated to commitment before and after a model checking proof,
ments with a secret proof witness, whereas we verify a secret             to the information a public specification may reveal about a
system against a temporal specification, so that the theorems             secret system.


                                                                     13
Acknowledgments                                                      [11] Dan Boneh, Ben Lynn, and Hovav Shacham. Short
                                                                          signatures from the weil pairing. In Colin Boyd, ed-
This work was supported in part by the Amazon Research                    itor, Advances in Cryptology - ASIACRYPT 2001, 7th
Award Neural Software Verification (Fall 2024), and by the                International Conference on the Theory and Applica-
Advanced Research and Invention Agency (ARIA) under the                   tion of Cryptology and Information Security, Gold Coast,
Safeguarded AI programme.                                                 Australia, December 9-13, 2001, Proceedings, Lecture
                                                                          Notes in Computer Science, pages 514–532. Springer,
                                                                          2001. doi:10.1007/3-540-45682-1\_30.
References
                                                                     [12] Benedikt Bünz, Jonathan Bootle, Dan Boneh, Andrew
 [1] Alessandro Abate, Mirco Giacobbe, Sergey Ichtchenko,
                                                                          Poelstra, Pieter Wuille, and Greg Maxwell. Bulletproofs:
     and Diptarko Roy. Complete ω-regular supermartin-
                                                                          Short proofs for confidential transactions and more. In
     gale certificates. In LICS, volume 380 of LIPIcs, pages
                                                                          2018 IEEE symposium on security and privacy (SP),
     3:1–3:28. Schloss Dagstuhl - Leibniz-Zentrum für Infor-
                                                                          pages 315–334. IEEE, 2018.
     matik, 2026.

 [2] Alessandro Abate, Mirco Giacobbe, and Diptarko Roy.             [13] Jerry R. Burch, Edmund M. Clarke, Kenneth L. McMil-
     Stochastic omega-regular verification and control with               lan, David L. Dill, and L. J. Hwang. Symbolic model
     supermartingales. In CAV (3), Lecture Notes in Com-                  checking: 1020 states and beyond. In LICS, pages 428–
     puter Science, pages 395–419. Springer, 2024.                        439. IEEE Computer Society, 1990.

 [3] Alessandro Abate, Mirco Giacobbe, and Diptarko Roy.             [14] David Chaum and Torben Pryds Pedersen. Wallet
     Quantitative supermartingale certificates. In CAV                    databases with observers. In CRYPTO, volume 740
     (2), Lecture Notes in Computer Science, pages 3–28.                  of Lecture Notes in Computer Science, pages 89–105.
     Springer, 2025.                                                      Springer, 1992.

 [4] Rajeev Alur. Principles of cyber-physical systems. MIT          [15] Edmund M. Clarke, Orna Grumberg, Daniel Kroening,
     press, 2015.                                                         Doron A. Peled, and Helmut Veith. Model checking,
                                                                          2nd Edition. MIT Press, 2018.
 [5] Rajeev Alur and Thomas A. Henzinger. Reactive mod-
     ules. In LICS, pages 207–218. IEEE Computer Society,            [16] Michael Colón, Sriram Sankaranarayanan, and Henny
     1996.                                                                Sipma. Linear invariant generation using non-linear
                                                                          constraint solving. In Warren A. Hunt Jr. and Fabio
 [6] arkworks contributors. arkworks zkSNARK ecosystem,                   Somenzi, editors, Computer Aided Verification, 15th In-
     2022. URL: https://arkworks.rs.                                      ternational Conference, CAV 2003, Boulder, CO, USA,
 [7] Christel Baier and Joost-Pieter Katoen. Principles of                July 8-12, 2003, Proceedings, Lecture Notes in Com-
     model checking. MIT Press, 2008.                                     puter Science, pages 420–432. Springer, 2003. doi:
                                                                          10.1007/978-3-540-45069-6\_39.
 [8] Clark W. Barrett, Roberto Sebastiani, Sanjit A. Seshia,
     and Cesare Tinelli. Satisfiability modulo theories. In          [17] Michael Colón and Henny Sipma. Synthesis of linear
     Handbook of Satisfiability, volume 185 of Frontiers in               ranking functions. In TACAS, volume 2031 of Lec-
     Artificial Intelligence and Applications, pages 825–885.             ture Notes in Computer Science, pages 67–81. Springer,
     IOS Press, 2009.                                                     2001.

 [9] Felix A. Behrend. On sets of integers which contain             [18] Mingshu Cong, Tsz Hon Yuen, and Siu-Ming Yiu. zk-
     no three terms in arithmetical progression. Proceedings              matrix: Batched short proof for committed matrix multi-
     of the National Academy of Sciences, 32(12):331–332,                 plication. In AsiaCCS. ACM, 2024.
     1946.
                                                                     [19] Byron Cook, Alexey Gotsman, Andreas Podelski, An-
[10] Mihir Bellare and Oded Goldreich. On defining proofs                 drey Rybalchenko, and Moshe Y. Vardi. Proving that
     of knowledge. In Ernest F. Brickell, editor, Advances                programs eventually do something good. In POPL,
     in Cryptology - CRYPTO ’92, 12th Annual Interna-                     pages 265–276. ACM, 2007.
     tional Cryptology Conference, Santa Barbara, Califor-
     nia, USA, August 16-20, 1992, Proceedings, Lecture              [20] Byron Cook, Heidy Khlaaf, and Nir Piterman. Fairness
     Notes in Computer Science, pages 390–420. Springer,                  for infinite-state systems. In TACAS, Lecture Notes in
     1992. doi:10.1007/3-540-48071-4\_28.                                 Computer Science, pages 384–398. Springer, 2015.


                                                                14
[21] Geoffroy Couteau, Michael Klooß, Huang Lin, and                  [32] Ariel Gabizon, Zachary J. Williamson, and Oana Ciob-
     Michael Reichle. Efficient range proofs with transparent              otaru. PLONK: permutations over lagrange-bases for
     setup from bounded integer commitments. In EURO-                      oecumenical noninteractive arguments of knowledge.
     CRYPT (3), volume 12698 of Lecture Notes in Computer                  IACR Cryptol. ePrint Arch., 2019:953, 2019. URL:
     Science, pages 247–277. Springer, 2021.                               https://eprint.iacr.org/2019/953.

[22] Leonardo de Moura and Sebastian Ullrich. The Lean 4              [33] Steven D. Galbraith, Kenneth G. Paterson, and
     theorem prover and programming language. In CADE,                     Nigel P. Smart. Pairings for cryptographers. Dis-
     volume 12699 of Lecture Notes in Computer Science,                    cret. Appl. Math., 156(16):3113–3121, 2008. URL:
     pages 625–635. Springer, 2021.                                        https://doi.org/10.1016/j.dam.2007.12.010,
                                                                           doi:10.1016/J.DAM.2007.12.010.
[23] Leonardo Mendonça de Moura and Nikolaj S. Bjørner.
     Z3: an efficient SMT solver. In TACAS, volume 4963               [34] Mirco Giacobbe, Daniel Kroening, Abhinandan Pal,
     of Lecture Notes in Computer Science, pages 337–340.                  and Michael Tautschnig. Neural model checking. In
     Springer, 2008.                                                       NeurIPS, 2024.

[24] Leonardo Mendonça de Moura and Nikolaj S. Bjørner.               [35] Jens Groth. On the size of pairing-based non-interactive
     Satisfiability modulo theories: introduction and applica-             arguments. In Marc Fischlin and Jean-Sébastien Coron,
     tions. Commun. ACM, 54(9):69–77, 2011.                                editors, Advances in Cryptology - EUROCRYPT 2016
                                                                           - 35th Annual International Conference on the Theory
[25] Rayna Dimitrova, Luis María Ferrer Fioriti, Holger Her-               and Applications of Cryptographic Techniques, Vienna,
     manns, and Rupak Majumdar. Probabilistic ctl* : The                   Austria, May 8-12, 2016, Proceedings, Part II, Lecture
     deductive way. In TACAS, Lecture Notes in Computer                    Notes in Computer Science, pages 305–326. Springer,
     Science, pages 280–296. Springer, 2016.                               2016. doi:10.1007/978-3-662-49896-5\_11.

[26] Ralph Droms.      Dynamic Host Configuration                     [36] Orna Grumberg, Nissim Francez, Johann A. Makowsky,
     Protocol.   RFC 2131, March 1997.      URL:                           and Willem P. de Roever. A proof rule for fair termina-
     https://www.rfc-editor.org/info/rfc2131,                              tion of guarded commands. Inf. Control., 66(1/2):83–
     doi:10.17487/RFC2131.                                                 102, 1985.

[27] Alexandre Duret-Lutz, Etienne Renault, Maximilien                [37] Thomas Hader and Alex Ozdemir. An smt-lib theory
     Colange, Florian Renkin, Alexandre Gbaguidi Aisse,                    of finite fields. In Proceedings of the 22nd Interna-
     Philipp Schlehuber-Caissier, Thomas Medioni, Antoine                  tional Workshop on Satisfiability Modulo Theories (SMT
     Martin, Jérôme Dubois, Clément Gillard, and Henrich                   2024), Montreal, Canada, July, 22-23, 2024., volume
     Lauko. From spot 2.0 to spot 2.10: What’s new? In                     3725. CEUR Workshop Proceedings, 2024.
     CAV (2), volume 13372 of Lecture Notes in Computer               [38] Thomas A. Henzinger, Mahyar Karimi, and K. S. The-
     Science, pages 174–187. Springer, 2022.                               jaswini. Privacy-preserving runtime verification. In
[28] Liam Eagen and Ariel Gabizon. ProtoGalaxy: Efficient                  CCS, pages 2774–2787. ACM, 2025.
     ProtoStar-style folding of multiple instances. Cryp-             [39] Thomas A. Henzinger, Kaushik Mallik, Pouya Sadeghi,
     tology ePrint Archive, Paper 2023/1106, 2023. URL:                    and Dorde Zikelic. Supermartingale certificates for
     https://eprint.iacr.org/2023/1106.                                    quantitative omega-regular verification and control. In
                                                                           CAV (2), Lecture Notes in Computer Science, pages 29–
[29] Paul Erdős and Paul Turán. On some sequences of
                                                                           55. Springer, 2025.
     integers. Journal of the London Mathematical Society,
     11(4):261–264, 1936.                                             [40] Gerard J. Holzmann. Explicit-state model checking. In
                                                                           Handbook of Model Checking, pages 153–171. Springer,
[30] Julius Farkas. Theorie der einfachen ungleichungen.
                                                                           2018.
     Journal für die reine und angewandte Mathematik
     (Crelles Journal), 1902(124):1–27, 1902.                         [41] Samuel Judson, Ning Luo, Timos Antonopoulos, and
                                                                           Ruzica Piskac. Privacy preserving CTL model checking
[31] Amos Fiat and Adi Shamir. How to prove yourself: Prac-                through oblivious graph algorithms. In WPES@CCS,
     tical solutions to identification and signature problems.             pages 101–115. ACM, 2020.
     In Andrew M. Odlyzko, editor, Advances in Cryptology
     - CRYPTO ’86, Santa Barbara, California, USA, 1986,              [42] Aniket Kate, Gregory M. Zaverucha, and Ian Goldberg.
     Proceedings, Lecture Notes in Computer Science, pages                 Constant-size commitments to polynomials and their
     186–194. Springer, 1986.                                              applications. In ASIACRYPT, volume 6477 of Lecture


                                                                 15
     Notes in Computer Science, pages 177–194. Springer,                [55] Amir Pnueli. The temporal logic of programs. In FOCS,
     2010.                                                                   pages 46–57. IEEE Computer Society, 1977.

[43] Jonathan Katz and Yehuda Lindell. Introduction to                  [56] Andreas Podelski and Andrey Rybalchenko. A complete
     Modern Cryptography, Second Edition. CRC Press,                         method for the synthesis of linear ranking functions. In
     2014.                                                                   VMCAI, volume 2937 of Lecture Notes in Computer
                                                                             Science, pages 239–251. Springer, 2004.
[44] Abhiram Kothapalli, Srinath Setty, and Ioanna Tzialla.
     Nova: Recursive zero-knowledge arguments from fold-                [57] Jon Postel. Transmission Control Protocol. RFC 793,
     ing schemes. In CRYPTO, pages 359–388, 2022.                            September 1981. URL: https://www.rfc-editor.
                                                                             org/info/rfc793, doi:10.17487/RFC0793.
[45] Daniel Kroening and Ofer Strichman. Decision Proce-
     dures - An Algorithmic Point of View, Second Edition.              [58] Stephen Prajna and Ali Jadbabaie. Safety verification
     Texts in Theoretical Computer Science. An EATCS Se-                     of hybrid systems using barrier certificates. In HSCC,
     ries. Springer, 2016.                                                   Lecture Notes in Computer Science, pages 477–492.
                                                                             Springer, 2004.
[46] Orna Kupferman and Moshe Y. Vardi. From complemen-
     tation to certification. Theor. Comput. Sci., 345(1):83–           [59] Stephen Prajna, Ali Jadbabaie, and George J. Pappas.
     100, 2005.                                                              Stochastic safety verification using barrier certificates.
                                                                             In CDC, pages 929–934. IEEE, 2004.
[47] Satoshi Kura and Hiroshi Unno. A hierarchy of
     supermartingales for ω-regular verification. CoRR,                 [60] Raphaël Salem and Donald C. Spencer. On sets of
     abs/2512.00270, 2025.                                                   integers which contain no three terms in arithmetical
                                                                             progression. Proceedings of the National Academy of
[48] Leslie Lamport. Specifying concurrent program mod-
                                                                             Sciences, 28(12):561–563, 1942.
     ules. ACM Trans. Program. Lang. Syst., 5(2):190–222,
     1983.                                                              [61] Jacob T. Schwartz. Fast probabilistic algorithms for
                                                                             verification of polynomial identities. Journal of the
[49] Evan Laufer, Alex Ozdemir, and Dan Boneh. zkPi: Prov-
                                                                             ACM, 27(4):701–717, 1980.
     ing Lean theorems in zero-knowledge. In CCS, pages
     4301–4315. ACM, 2024.                                              [62] Caterina Urban, Arie Gurfinkel, and Temesghen Kahsai.
                                                                             Synthesizing ranking functions from bits and pieces.
[50] Daniel Luick, John C. Kolesar, Timos Antonopoulos,
                                                                             In TACAS, volume 9636 of Lecture Notes in Computer
     William R. Harris, James Parker, Ruzica Piskac, Eran
                                                                             Science, pages 54–70. Springer, 2016.
     Tromer, Xiao Wang, and Ning Luo. ZKSMT: A VM for
     proving SMT theorems in zero knowledge. In USENIX                  [63] Moshe Y. Vardi. Verification of concurrent programs:
     Security Symposium. USENIX Association, 2024.                           The automata-theoretic framework. Ann. Pure Appl.
                                                                             Log., 51(1-2):79–98, 1991.
[51] Ning Luo, Timos Antonopoulos, William R. Harris, Ruz-
     ica Piskac, Eran Tromer, and Xiao Wang. Proving UN-                [64] Moshe Y. Vardi and Pierre Wolper. An automata-
     SAT in zero knowledge. In CCS, pages 2203–2217.                         theoretic approach to automatic program verification
     ACM, 2022.                                                              (preliminary report). In LICS, pages 332–344. IEEE
                                                                             Computer Society, 1986.
[52] Zohar Manna and Amir Pnueli. A hierarchy of temporal
     properties. In PODC, pages 377–410. ACM, 1990.                     [65] Richard Zippel. Probabilistic algorithms for sparse poly-
                                                                             nomials. In EUROSAM, pages 216–226, 1979.
[53] numerous contributors. bls_bulletproofs, 2022.
     URL:       https://github.com/maidsafe/bls_
     bulletproofs.                                                      A     Open Science
[54] Torben P. Pedersen. Non-interactive and information-               We provide four tools and prototypes, as well as a series
     theoretic secure verifiable secret sharing. In Joan Feigen-        of benchmark data files, that enable readers to evaluate and
     baum, editor, Advances in Cryptology - CRYPTO ’91,                 reproduce the paper’s core contributions. We provide:
     11th Annual International Cryptology Conference, Santa
     Barbara, California, USA, August 11-15, 1991, Proceed-                 • encoder: A lightweight preprocessing front-end tool
     ings, Lecture Notes in Computer Science, pages 129–                      written in Python which implements a toy certifier in-
     140. Springer, 1991. doi:10.1007/3-540-46766-1\                          put language for guarded-command programs, Büchi
     _9.                                                                      automata, and piecewise-linear ranking functions, and


                                                                   16
      computes batches and obligations, using Z3 [23] to de-            ({ci }, πBullet ) to obtain per-entry openings (vi , ri ) satisfying
      rive the Farkas witnesses. This tool has built-in bench-          ci = gvi hri and 0 ≤ vi ≤ M. The extractor then recovers the
      marking capabilities to time explicit and symbolic output         matrix-level blinding factor rA . Under the AGM, the prover
      generation.                                                       outputs ĉA together with its algebraic representation over
                                                                                                                k
                                                                        the public pairing bases {e(g, g′ )α } and e(g, h′ ), and the ex-
    • zkmc-explicit: A prototype implementation of our                  tractor reads rA directly as the coefficient of e(g, h′ ) in this
      explicit approach, written in Rust, which takes output            representation. What remains is to show that ({vi }, {ri }, rA )
      from encoder as input and provides library methods to             is consistent with ĉA . Substituting the algebraic represen-
      prove and verify as per our specification. This prototype         tation of ĉA into the verification equation reduces it to the
      comes with a benchmark tool that times setup, proving,            polynomial identity f (α) − f (z) = (α − z) · q(α) at the chal-
      and verifying of a given input.                                   lenge z = H(ĉA ∥c1 ∥ · · · ∥cl ), where f is the matrix polynomial
    • zkmc-symbolic/non-folding: A prototype imple-                     defined by {vi }. Since the random oracle distributes z uni-
      mentation of our symbolic approach, written in Rust,              formly, the Schwartz–Zippel lemma implies coefficient-wise
      which takes output from encoder as input and provides             equality of the two polynomials with overwhelming proba-
      library methods to prove and verify as per our specifica-         bility. Therefore ĉA commits exactly to the matrix defined by
      tion. The prototype comes with a benchmark tool that              {vi } with blinding rA , and the extractor outputs the witness
      times setup, proving, and verifying of a given input.             ({vi }, {ri }, rA ).

    • zkmc-symbolic/folding: A prototype implementa-                    Zero Knowledge. We construct a simulator S that, given
      tion of our symbolic folding approach, written in Rust,           only ĉA , produces transcripts indistinguishable from those of
      which takes output from encoder as input and provides             an honest prover. We grant S the setup trapdoors α and β,
      library methods to prove and verify as per our specifica-         which is a standard simulation assumption. On input ĉA , the
      tion. The prototype comes with a benchmark tool that              simulator proceeds as follows:
      times setup, proving, and verifying of a given input.
                                                                            • Sample ci ∈ G1 uniformly for i = 1, . . . , l, and invoke
    • Example guarded command files: Various models that                      the Bulletproofs simulator to obtain πBullet .
      correspond to our benchmarked instances in guarded
      command form, which can be readily used with encoder                  • Compute the challenge z = H(ĉA ∥c1 ∥ · · · ∥cl ) and the
                                                                                                     i−1
      to build files which can then be used as input into                     aggregate c = ∏li=1 czi .
      our prototypes. These files consist of: a minimal
      example.gc; a simple counter from 0 to maxVal;                        • Sample πeq ∈ G1 uniformly, and define θ = ĉA ·
      our round-robin.gc example used in benchmarking;                        e(c, g′ )−1 e(πeq , (g′ )α−z )
                                                                                                           1/β
                                                                                                                 , which makes the veri-
      three of our models of exponential backoff, namely                      fication equation hold by construction.
      exp_backoff_state_opt_small.gc,
      exp_backoff_state_opt.gc, and                                         • Output π = ({ci }, πeq , θ, πBullet ).
      exp_backoff_guard_opt.gc; and our model of DHCP,
      named dhcp.gc.                                                    Each component of the simulated transcript is indistinguish-
                                                                        able from its real counterpart. The Pedersen commitments ci
We provide a singular repository consisting of all code and             are perfectly hiding, so the simulated ci have the same dis-
benchmark files, split by tool (with benchmarks and examples            tribution as the honest ones. The Bulletproofs simulator pro-
inside encoder), with full instructions on how to run any               duces range proofs computationally indistinguishable from
artifacts within their own folder structure. This repository can        real ones. Finally, (πeq , θ) is uniform among the pairs that
be found at https://github.com/aiverification/zkmc.                     satisfy the verification equation, matching the honest prover,
                                                                        who randomises πeq via the blinding scalar µ sampled in
B     Proof Sketch of zkrp                                              zkrp.Prove (Fig. 4) and absorbs the resulting offset into θ.
                                                                        Hence no probabilistic polynomial-time distinguisher sepa-
Completeness holds by construction. We argue knowledge                  rates the simulated transcript from a real one, and zkrp is zero
soundness in the algebraic group model (AGM) augmented                  knowledge in the random oracle model.
with a random oracle (ROM), and zero knowledge in the
random oracle model.                                                    C     Proof Sketch of Folding
Soundness. Given an accepting proof π, we construct an                  Completeness holds by construction. The argument for Theo-
extractor E that recovers a witness for the relation Rzkrp .            rem 5.1 separates into a field layer and an integer layer, which
The extractor first invokes the Bulletproofs extractor on               do not interact.


                                                                   17
Field Layer. The binding property of the commitment
scheme and the knowledge soundness of zkmm and zkeq
yield openings of the folded instances, which the homomor-
phic fold maps back to openings of the per-obligation commit-
ments. Section 5.2 established that under Eq. (28) no diagonal
residual shares a monomial with a freely chosen cross-term
aggregate. A prover that violates some obligation therefore
faces a non-zero polynomial of degree at most 2 maxi ci in
the challenge, which the Schwartz–Zippel lemma bounds as
above; we argue each of the four families separately and add
the bounds. Up to this term, the extracted openings satisfy
Eq. (26) over Z p for every i individually. No step here assigns
an integer meaning to a value, so the wraparound of the folded
witnesses is immaterial.

Integer Layer. The range proofs are stated on the per-
obligation commitments, so by binding they constrain the
very same openings, entry-wise: λi , µi , δi ∈ [0, M] and, after
removing the offsets, Ai , bi ∈ [−M, M]. Fix an obligation i
and evaluate both sides of Ai λi = αi = Gi µi over Z under
the canonical signed lift of Section 5.1. The two sides are
congruent modulo p and bounded in magnitude by n̂′ M 2 and
n̂MG M respectively, so their difference is smaller than p and
they are equal as integers. Applying the same argument to
δi = bi λi + hi µi − 1 ∈ [0, M] yields bT           T
                                        s,i λs,i + hp,i µs,i ≤ −1 over
Z. Together these are the conditions of Eq. (25). Both bounds
are per obligation, which is why the condition of Theorem 5.1
does not depend on N.

Zero Knowledge. Zero knowledge is inherited from the
sub-protocols. The cross-term commitments are perfectly
hiding and are the only additional message the prover sends,
and the folded instances are opened solely through zkmm,
zkeq and zkrp, each run with independent randomness.




                                                                         18
