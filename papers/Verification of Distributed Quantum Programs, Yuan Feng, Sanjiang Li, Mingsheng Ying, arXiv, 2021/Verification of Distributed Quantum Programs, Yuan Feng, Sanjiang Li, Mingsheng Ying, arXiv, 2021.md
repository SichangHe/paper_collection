                                            Verification of Distributed Quantum Programs *
                                            Yuan Feng1 , Sanjiang Li1 , and Mingsheng Ying1,2,3

                                            1       Centre for Quantum Software and Information, University of Technology Sydney, Australia
                                            2       Institute of Software, Chinese Academy of Sciences, Beijing, China
                                            3       Department of Computer Science, Tsinghua University, Beijing, China


                                                     Abstract
                                            Distributed quantum systems and especially the Quantum Internet have the ever-increasing potential to
                                            fully demonstrate the power of quantum computation. This is particularly true given that developing a
                                            general-purpose quantum computer is much more difficult than connecting many small quantum devices.
                                            One major challenge of implementing distributed quantum systems is programming them and verifying
arXiv:2104.14796v1 [quant-ph] 30 Apr 2021




                                            their correctness. In this paper, we propose a CSP-like distributed programming language to facilitate the
                                            specification and verification of such systems. After presenting its operational and denotational semantics,
                                            we develop a Hoare-style logic for distributed quantum programs and establish its soundness and (relative)
                                            completeness with respect to both partial and total correctness. The effectiveness of the logic is demon-
                                            strated by its applications in verification of quantum teleportation and local implementation of non-local
                                            CNOT gates, two important algorithms widely used in distributed quantum systems.


                                                1     Introduction
                                            Quantum computers exploit quantum phenomena such as superposition and entanglement to perform
                                            computation. The past five years have seen exciting progresses in building small-scale quantum
                                            processors and the two state-of-the-arts, Google’s Sycamore and IBM Q Rochester, both have 53
                                            qubits. While these small quantum devices already demonstrate certain advantages over classical
                                            supercomputers, large scale general-purpose quantum computers are still far from reach.
                                                The Quantum Internet has been proposed as a key strategy to provide large-scale quantum
                                            computing [25, 37, 26, 10]. The idea is to connect many small quantum devices by using quantum
                                            communications and this network of quantum devices will then have the functionality of a (virtual)
                                            large-scale quantum computer. On July 3, 2020, the Department of Energy of the United States
                                            proposed a 10-year roadmap for a national Quantum Internet under the $1.2 billion National Quantum
                                            Initiative Act. Several important steps have been experimented in the past two years. In February
                                            2020, scientists from Argonne and the University of Chicago successfully entangled photons across a
                                            52-mile underground network of optical fibre. In April 2021, a team of researchers from QuTech in
                                            the Netherlands reported realisation of the first entanglement-based quantum network (connecting
                                            three quantum processors) [30].
                                                As pointed out in [26], software-defined networking (SDN) technology is particularly important
                                            for quantum networks, because under current technical conditions, quantum memories have a very
                                            short lifespan. On the other hand, programming quantum networks is much harder and more error-
                                            prone than programming classical ones due to the possible existence of entanglement between
                                            different systems and non-commutativity of quantum observables and operations.
                                                Inspired by Apt’s work [2] on distributed programming based upon Hoare’s CSP (Concurrent
                                            Sequential Processes) [21], we define in this paper a programming language for distributed quantum
                                            systems. Recall that a distributed system consists of a number of spatially separated processes
                                            that work independently using their private storage, but communicate by explicit message passing.


                                            *   This work is partially supported by the National Key R&D Program of China (Grant No: 2018YFA0306 701) and
                                                the Australian Research Council (Grant Nos: DP180100691, DP210102449).
                                                         © Yuan Feng, Sanjiang Li, and Mingsheng Ying;
                                                         licensed under Creative Commons License CC-BY
                                                                  Leibniz International Proceedings in Informatics
                                                                  Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl Publishing, Germany
2   Verification of Distributed Quantum Programs


    Our language supports both classical and quantum operations of individual processes. However,
    to make the presentation simpler, we only consider classical communication between different
    processes. Note that this is not a serious limitation, as generic quantum communication can be
    achieved by using the teleportation protocol [5] provided that entanglement is pre-shared between
    relevant parties. Furthermore, communication is achieved in a handshaking (or rendezvous) way;
    that is, the sender can deliver a message only when the receiver is ready to accept it at the same
    moment. We leave the asynchronous communication of quantum states as future work. Based on the
    notion of classical-quantum assertions defined in [16], we propose Hoare-style logic systems for both
    partial and total correctness of distributed quantum programs, and prove their soundness and (relative)
    completeness. The effectiveness of these logic systems are demonstrated through the verification of
    quantum teleportation and local implementation of non-local CNOT gates, two important algorithms
    widely used in distributed quantum systems. It is worth noting that since the language we consider
    includes probabilistic assignments, this paper actually provides a sound and relatively complete Hoare
    logic for distributed probabilistic programs as a by-product.
       Technical Contributions: While the semantics and proof systems in this paper are defined in a
    way similar to that of [16], the extension from sequential quantum programs to distributed quantum
    programs is challenging.
        Firstly, the operational semantics of quantum measurements and probabilistic assignments in [16]
    are given in a ‘nondeterministic’ way, with the probabilities of different branches being encoded
    in the quantum part of the configurations. This follows a tradition originated in [32] and adopted
    in [39, 40] that simplifies both notationally and conceptually the semantics of (deterministic) quantum
    languages, especially the description of non-termination. However, distributed quantum programs
    investigated in this paper exhibit real nondeterminism (in the transition systems for operational
    semantics) due to the possible interleaving of local actions and communication of different sequential
    processes. To distinguish these two types of nondeterminism, we model quantum measurements
    and probabilistic assignments in a (standard) probabilistic way. Accordingly, the transition relation
    between configurations has to be lifted to probability distributions of configurations.
        Secondly, despite that the entire distributed program may exhibit nondeterminism even if each
    individual process is deterministic, we show that different computations from a given configuration
    actually obtain the same classical-quantum state, thanks to the disjointness of the (classical changeable
    and quantum) variables accessible by different processes. This result clears the obstacle in defining
    the denotational semantics of distributed quantum programs and ensures that a distributed program
    can be sequentialised into a deterministic one without affecting its semantics.
        Thirdly, the proof systems presented in [16] are designed for sequential quantum programs. New
    techniques are developed in this paper in extending them to distributed programs and proving their
    soundness and relative completeness.
        Organisation of the paper: In the rest of this section, we briefly discuss some related works and
    present quantum teleportation as a motivating example. The remainder of this paper is organised as
    follows. In Sec. 2, we present the three layers of the syntax of the distributed quantum programming
    language, which is followed by its operational and denotational semantics in Sec. 3. In particular, we
    prove that distributed quantum programs are semantically deterministic in the sense that different
    computations from a given configuration always give the same classical-quantum state. We then show
    in Sec. 4 how a distributed quantum program can be sequentialised without affecting its semantics.
    Based on the notion of classical-quantum assertion, we present a Hoare-style logic in Sec. 5 for
    distributed quantum programs and establish its soundness and (relative) completeness for both partial
    and total correctness. The last section concludes this paper with an outline of future works. Due to
    space limitation, we omit all proofs as well as the verification of quantum teleportation and local
    implementation of non-local CNOT gates. Interested readers may find these details in the appendix.
Y. Feng, S. Li, and M. Ying                                                                               3


1.1     Related Works
The following three lines of previous works are closely related to this paper.
    Quantum Process Algebras: Process algebra is the mainstream approach to formally model and
reason about quantum communication systems. Since 2004, several quantum process algebras such
as QPAlg [23], CQP [17], and qCCS [13, 42, 15] have been introduced and adopted in verification
of popular quantum communication protocols such as teleportation [5] and superdense coding [6].
Following [2] (also see [1], Chapter 11), we choose to use (a subset of) a quantum extension of process
algebra CSP as our language for programming distributed quantum systems, but use a Hoare-style
logic to reason about their correctness.
    Quantum Hoare Logic: Hoare logic provides a syntax-oriented proof system to reason about
program correctness [20]. In recent years, Hoare-style logics for quantum programs have been
developed in [9, 14, 24, 39, 35, 16]. However, these logic systems are designed for the verification of
sequential quantum programs, thus are not suitable for the distributed ones considered in the current
paper. Nevertheless, our definition of semantics of distributed quantum programs is based on the key
notions such as classical-quantum states and assertions introduced in [16].
    Programming with Quantum Communication: The authors of [33] presented some interesting
ideas of specifying and analysing quantum communication in a predicative programming language.
However, the key technique for verification of quantum communication protocols developed in [33]
(and in predicative programming [19] in general) is refinement, while we use a Hoare-style logic here.


1.2     Motivating Example — Quantum Teleportation
 Quantum teleportation was proposed by Bennett et al. [5] for transmitting quantum information (e.g.
 the exact state of an atom or photon) via only classical communication but with the help of previously
 shared quantum entanglement between the sender and the receiver. It is one of the most surprising
 examples where entanglement helps to accomplish a certain task that is impossible in the classical
 world. A large number of quantum communication protocols such as quantum gate teleportation [18],
 port-based teleportation [22], quantum repeaters [7], and measurement based quantum computing [31]
 have been designed based on it, and some of them have been experimentally implemented [29].
     Let us consider the simplest case of teleporting a qubit. Assume that Alice and Bob live far apart
 and there is only a classical communication channel between them. But Alice wants to send quantum
 information, say a state |ψi , α0 |0i + α1 |1i of qubit q, to Bob. How can she do it? This seems a
 task impossible for her to accomplish because it may take infinite amount of classical information to
 describe the complex amplitudes α0 and α1 . However, if Alice and Bob share entanglement; more
 precisely, if they possess qubits q1 and q2 respectively and these two qubits are in the Bell state
 |βi , √12 (|00i + |11i) (also called EPR pair), then they can accomplish the task using the following
 protocol, called teleportation:
(1) Alice interacts qubit q in state |ψi and her half q1 of the shared EPR pair |βi by performing first
     the controlled NOT (CNOT for short) on q, q1 and then the Hadamard gate H on q, where:
        the CNOT acts as follows: if the control qubit q is in |0i then the target qubit q1 is left
        unchanged, and if q is in |1i then q1 is flipped between |0i and |1i;
        the H gate turns basis states |0i and |1i to their equal superposition |+i and |−i, where
        |±i = √12 (|0i ± |1i), respectively.
(2) Alice measures her qubits q, q1 (in the standard basis), and sends the obtained results – classical
     bits z, x through the classical channel to Bob.
(3) On his half q2 of the EPR pair, Bob performs operation X whenever the received classical
     information x = 1, and then Z whenever z = 1. Here X and Z are Pauli operations with
     X|ii = |1 − ii and Z|ii = (−1)i |ii for i = 0, 1.
4   Verification of Distributed Quantum Programs


                                                           z
                  |ψi                      H
                                                           x

                 |βi
                                                                         X         Z

       Figure 1 Quantum Teleportation. The wires from top to bottom represent qubits q, q1 , and q2 respectively.
    Furthermore, q and q1 belong to Alice while q2 belongs to Bob.


    Quantum teleportation can be visualised as the quantum circuit in Figure 1. What surprises us is that
    at the end Bob’s qubit q2 is in state |ψi. In other words, Alice sends the quantum information |ψi to
    Bob only by classical communication of two bits in step (2), even without knowing the amplitudes
    α0 and α1 of |ψi. Of course, this is achieved by consuming some entanglement (At the end of the
    protocol, qubits q1 and q2 are no longer entangled).


     2      A Language for Programming Distributed Quantum Systems
    We propose a programming language to describe distributed quantum systems. The syntax has three
    layers, introduced in the following three subsections respectively.

    2.1     Sequential quantum programs
    For the first layer, we extend the classical-quantum while language defined in [16] with alternative
    and repetitive commands [11]. We assume two basic types for classical variables: Boolean with
    the corresponding domain DBoolean , {true, false} and Integer with DInteger , Z. For
    each integer d ≥ 1, we assume a basic quantum type Qudit with domain HQudit , which is a
    d-dimensional Hilbert space with an orthonormal basis {|0i, . . . , |d − 1i}. In particular, we denote
    the quantum type for d = 2 as Qubit. Let cVar, ranged over by x, y, · · · , and qVar, ranged over by
    q, r, · · · , be countably infinite sets of classical and quantum variables, respectively. Denote by type(v)
                                                                                                     N
    the type of a (classical or quantum) variable v. For any finite subset V of qVar, let HV , q∈V Hq ,
    where Hq , Htype(q) . In this paper, when we refer to a subset of qVar, it is always assumed to be
    finite.
         With the above notions, a sequential quantum program is defined by the following syntactic rules:

         S ::= skip | abort | x := e | x :=$ g | x := meas M[q̄] | q := 0 | q̄ ∗= U | S0 ; S1 |
               if B1 → S1  . . .  Bn → Sn fi | do B1 → S1  . . .  Bn → Sn od

    where S and Si are sequential quantum programs, x a classical variable in cVar, e a classical
    expression with the same type as x, g a discrete probability distribution over Dtype(x) , Bi a Boolean-
    type expression, q a quantum variable and q̄ , q1 , . . . , qn a (ordered) tuple of distinct quantum
    variables in qVar, M a measurement and U a unitary operator on dq̄ -dimensional Hilbert space with
                                                               n
                                                               Y
                                         dq̄ , dim(Hq̄ ) =           dim(Hqi ).
                                                               i=1


    Sometimes we also use q̄ to denote the (unordered) set {q1 , q2 , . . . , qn }. Let |q̄| , n be the size of q̄.
    We write x := meas q̄ for x := meas Mcom [q̄] where Mcom , {Pk , |kihk| : 0 ≤ k < dq̄ } is
Y. Feng, S. Li, and M. Ying                                                                                5


the projective measurement according to the computational basis of Hq̄ . We always write |ki for the
                                          Pn
product state |k1 i · · · |kn i, where k = i=1 ki dqi+1 . . . dqn .
    The alternative and repetitive commands above are sometimes abbreviated as

   if ni=1 Bi → Si fi       and       do ni=1 Bi → Si od

respectively. For simplicity, we only consider deterministic sequential quantum programs in this paper.
                                                                                            V
To this end, we assume that the Bi ’s are mutually exclusive; that is, for each i, Bi → j6=i ¬Bj
                                               Wn
is a tautology. However, we do not require i=1 Bi ↔ true. Under this assumption, a guarded
command Bi → Si in if ni=1 Bi → Si fi will be chosen to execute once its guard Bi evaluates to
true. If all guards evaluate to false, the alternative command will lead to a (classical) failure state,
which is a feature introduced in [11] but does not exist in the while language of [16]. The selection
of guarded commands in do ni=1 Bi → Si od follows a similar way, with the only difference that
after termination of a selected Si the whole command is repeated. Moreover, in contrast with the
alternative command, the repetitive command properly terminates if all the guards evaluate to false.

2.2    Sequential quantum process
To describe the second syntactic layer for distributed quantum programs, we adopt a subset of Hoare’s
CSP (Communicating Sequential Processes) [21, 8], following the approach in [1]. Let chan be a set
of (classical) channel names, ranged over by c, d, . . . . An input command is of the form c?x, while
an output command is of the form c!e, where c ∈ chan is a communication channel, x ∈ cVar a
classical variable, and e an expression. Intuitively, c?x expresses the request to receive a classical
value along channel c. Upon reception this value is assigned to variable x. In contrast, c!e expresses
the request to send the value of expression e along channel c. A generalised guard is of the form
g , B; α where B is a Boolean expression, and α an input or output command. In particular, if
B ≡ true, then we denote g simply as α.
    Let α1 and α2 be two input/output (i/o) commands. They are said to match if they refer to the
same channel, one of them is an input, and the other one output with the same type. Given two
matched i/o commands α1 , c?x and α2 , c!e, the communication effect of α1 and α2 is defined to
be the program statement x := e; that is,

                             Effect(α1 , α2 ) = Effect(α2 , α1 ) , x := e.

I Definition 1. A sequential quantum process has the form:

                                S ::= S0 ; do m
                                               j=1 Bj ; αj → Sj od

where m ≥ 0, S0 , S1 , . . . , Sm are sequential quantum programs defined in the previous subsec-
tion. Again, we assume that Bj ’s are mutually exclusive. We call S0 the initialisation part, and
do m j=1 Bj ; αj → Sj od the main loop of S. If m = 0, then we let S = S0 . In this way, any
sequential quantum program is a sequential process. If S0 ≡ skip, we drop S0 from S unless m = 0.
   We have the following notations for sequential quantum process S.
   Denote by cv(S) and qv(S) the sets of classical and quantum variables appearing in S, respect-
   ively. Note that we do not distinguish between free and bound variables; that is, the classical vari-
   able appearing in an input command of S is also included in cv(S). Let var(S) , cv(S) ∪ qv(S).
   Denote by change(S) the set of classical variables that appear on the left-hand side of an
   assignment or in an input command in S. Note that the only way to retrieve information from
   a quantum system is to measure it, which may change its state. Thus qv(S) is also the set of
   changeable quantum variables in S.
   Denote by chan(S) the set of channel names appearing in S.
6   Verification of Distributed Quantum Programs


    2.3        Distributed quantum programs
    Now we are ready to define the syntax for distributed quantum programs.

    I Definition 2. A distributed quantum program is a parallel composition S ::= S1 k · · · kSn where
    n ≥ 1 and S1 , . . . , Sn are sequential quantum processes defined in the above subsection which satisfy
        Pairwise disjointness: for all 1 ≤ i 6= j ≤ n, var(Si ) ∩ (change(Sj ) ∪ qv(Sj )) = ∅;
        Point-to-point connection: for all 1 ≤ i < j < k ≤ n, chan(Si ) ∩ chan(Sj ) ∩ chan(Sk ) = ∅.
                  Sn
    Let cv(S) , i=1 cv(Si ), and change(S), qv(S), and var(S) be similarly defined.

         Essentially, the first clause requires that (1) classical variables in any process cannot be changed
    by other processes; (2) quantum variables in any process do not appear in other processes. The second
    clause in Definition 2 implies that each communication channel is shared by at most two processes.
    This constraint, together with the assumption that sequential processes are deterministic, means that
    at any moment, each process is only able to communicate with at most one other process. Note also
    that we disallow nested parallelism in distributed programs. Finally, any sequential quantum process
    is a distributed quantum program with n = 1.
         The constraints in Definition 2 look very strict at the first glance. However, using similar
    approaches presented in [3, 43], more general distributed quantum systems can be transformed into
    this special form by introducing control variables (say, stageA and stageB in the following example).

    I Example 3 (Quantum Teleportation as a Distributed Program). The quantum teleportation
    protocol presented in Sec. 1.2 can be written as a distributed program Teleport , Alice k Bob where
    Alice ,

          q, q1 ∗= CNOT; q ∗= H; zA := meas q; xA := meas q1 ; stageA := 0;
          do stageA = 0; c!xA → stageA := 1  stageA = 1; d!zA → stageA := 2 od

    and Bob ,

          stageB := 0;
          do stageB = 0; c?xB → stageB := 1; if xB = 1 → q2 ∗= X  ¬(xB = 1) → skip fi
            stageB = 1; d?zB → stageB := 2; if zB = 1 → q2 ∗= Z  ¬(zB = 1) → skip fi
          od


      3        Operational and Denotational Semantics
    We recall some basic notions from [16] to define the semantics of distributed quantum programs.

    3.1        Classical-quantum states
    Let Σ , cVar → D be the (uncountably infinite) set of classical states, where D , DBoolean ∪
    DInteger . We further require that states in Σ respect the types of classical variables; that is, σ(x) ∈
    Dtype(x) for all σ ∈ Σ and x ∈ cVar. For V ⊆ qVar, let D(HV ) be the set of partial density
    operators on HV ; that is, positive linear operators with the trace being less than or equal to 1.
    Furthermore, let 0HV ∈ D(HV ) be the zero operator on HV .

     I Definition 4. Given V ⊆ qVar, a classical-quantum state (cq-state for short) ∆ on V is a
     function in Σ → D(HV ) such that
    (1) the support of ∆, denoted d∆e, is countable. That is, ∆(σ) 6= 0HV for at most countably infinite
        many σ ∈ Σ;
Y. Feng, S. Li, and M. Ying                                                                                                                           7



   hskip, σ, ρi → hE, σ, ρi                                                                hx := e, σ, ρi → hE, σ[σ(e)/x], ρi

                                 Pdq −1
   hq := 0, σ, ρi → hE, σ,          i=0
                                           |0iq hi|ρ|iiq h0|i                              hq̄ ∗= U, σ, ρi → hE, σ, Uq̄ ρUq̄† i

                                                                                                M = {Mi : i ∈ I}, ρi = Mi ρMi† , pi = tr(ρi )
                         P                                                                                          P
   hx :=$ g, σ, ρi →         d∈Dtype(x)
                                           g(d) · hE, σ[d/x], ρi                           hx := meas M[q̄], σ, ρi → p >0 pi · hE, σ[i/x], ρi /pi i
                                                                                                                                         i
                                                                                                                     Vn
             σ |= Bi , 1 ≤ i ≤ n                                                                       σ |= i=1 ¬Bi
   hif n
        i=1 Bi → Si fi, σ, ρi → hSi , σ, ρi                                                hif n
                                                                                                i=1 Bi → Si fi, σ, ρi → hE, fail, ρi
                                                                                                               n     V
                      σ |= Bi , 1 ≤ i ≤ n                                                              σ |= i=1 ¬Bi
   hdo n                                 n
        i=1 Bi → Si od, σ, ρi → hSi ; do i=1 Bi → Si od, σ, ρi                            hdo n
                                                                                                i=1 Bi →   S i od, σ, ρi → hE, σ, ρi
                        P                                                                                        m      V
       hS0 , σ, ρi →         pi · hSi , σi , ρi i                                                        σ |= j=1 ¬Bj
                        Pi∈I                                 where E; S1 ≡ S1
   hS0 ; S1 , σ, ρi →      i∈I
                                 pi · hSi ; S1 , σi , ρi i                                 hdo m
                                                                                                j=1 Bj ; αj → Sj od, σ, ρi → hE, σ, ρi

                                                                             P
                                                             hSk , σ, ρi →     i∈I
                                                                                     pi · hSk,i , σi , ρi i, 1 ≤ k ≤ n
                              (Paral)                                                P
                                          hS1 k . . . kSk k . . . kSn , σ, ρi →          i∈I
                                                                                               pi · hS1 k . . . kSk,i k . . . kSn , σi , ρi i

                                                                                                       0
                            Sk ≡ do m
                                     j=1 Bk,j ; αk,j → Sk,j od,                    S` ≡ do m
                                                                                            j=1 B`,j ; α`,j → S`,j od, 1 ≤ k < ` ≤ n

                        σ |= Bk,j1 ∧ B`,j2 , αk,j1 and α`,j2 match, Effect(αk,j1 , α`,j2 ) ≡ x := e, 1 ≤ j1 ≤ m, 1 ≤ j2 ≤ m0
         (Comm)
                                                             hS1 k . . . kSn , σ, ρi → hS10 k . . . kSn0 , σ[σ(e)/x], ρi
                                                 where Sk0 , Sk,j1 ; Sk , S`0 , S`,j2 ; S` , and Si0 , Si for i 6= k, `


    Table 1 Operational semantics for distributed quantum programs, where σ is a proper classical state; i.e.,
σ 6≡ fail.


                 P
(2) tr(∆) ,             σ∈d∆e tr[∆(σ)] ≤ 1.

    Denote by qv(∆) the set V of quantum variables in ∆ defined in Definition 4. Sometimes it is
                                                          L
convenient to denote a cq-state ∆ by the explicit form i∈I hσi , ρi i where d∆e = {σi : i ∈ I} and
∆(σi ) = ρi for each i ∈ I. When ∆ is a simple function such that d∆e = {σ} for some σ and
∆(σ) = ρ, we denote ∆ simply by hσ, ρi. Let {∆i : i ∈ I} be a countable set of cq-states over
                         P                                                   P
V such that for any σ, i∈I ∆i (σ) = ρσ for some ρσ ∈ D(HV ) and i∈I tr(∆i ) ≤ 1. Then the
                                P
summation of them, denoted i∈I ∆i , is a cq-state ∆ over V such that for any σ ∈ Σ, ∆(σ) = ρσ .
                    S                                                        P
Obviously, d∆e = i∈I d∆i e. It is worth noting the difference between i∈I hσi , ρi i, the summation
                                 L
of some (simple) cq-states, and i∈I hσi , ρi i, the explicit form of a single one: in the latter σi ’s must
be distinct while in the former they may not.
                                                                                            S
    Let SV be the set of all cq-states over V , and S the set of all cq-states; that is, S , V ⊆qVar SV .
We extend the Löwner order vV for D(HV ) pointwisely to S by letting ∆ v ∆0 iff qv(∆) = qv(∆0 )
and for all σ ∈ Σ, ∆(σ) vqv(∆) ∆0 (σ). Then SV is a pointed ω-CPO under v, with the least element
being the constant 0HV function, denoted ⊥V . Furthermore, S as a whole is an ω-CPO under v.
When ∆ v ∆0 , there exists a unique ∆00 ∈ Sqv(∆) , denoted ∆0 − ∆, such that ∆00 + ∆ = ∆0 . For
                                            P                           P
any real numbers λi , i ∈ I, if both ∆+ , λi >0 λi ∆i and ∆− , λi <0 (−λi )∆i are well-defined
                                       P
and ∆− v ∆+ , then the linear-sum i∈I λi ∆i is defined to be ∆+ − ∆− . In the rest of this paper,
                    P
whenever we write i∈I λi ∆i we always assume that it is well-defined. Finally, let E be a completely
positive and trace-nonincreasing super-operator from L(HV ) to L(HW ). We extend it to SV in a
pointwise way: E(∆)(σ) = E(∆(σ)) for all σ.

3.2      Operational Semantics
Let Prog be the set of all distributed quantum programs. A configuration is a triple hS, σ, ρi where
S ∈ Prog ∪ {E} with E being a special symbol to denote termination, σ ∈ Σ ∪ {fail} with fail
8   Verification of Distributed Quantum Programs


    being another special symbol to denote the failure state, and ρ ∈ D(HV ) for some V subsuming
    qv(S) with tr(ρ) = 1. We always identify Ek . . . kE with E. The operational semantics of programs
    in Prog is defined as the smallest transition relation → given in Table 1.
    I Remark. The transition rules presented in Table 1 for sequential quantum programs follows the
    same spirit as in [16], except for the newly introduced alternative and repetitive commands whose
    semantics definitions are also standard [11]. The rules (Paral) and (Comm) are similar to their analogy
    for classical non-probabilistic programs [1].
        It is worth noting that the transitions for quantum measurements and probabilistic assignments
    in [16] are given in a ‘non-deterministic’ way, with the probabilities of different branches being
    encoded in the quantum part of the configurations (by allowing partial density operators instead of
    density operators in configurations). Note that it is only a matter of notational convenience to represent
    probabilistic choices with non-determinism. However, distributed quantum programs investigated
    in this paper exhibit real non-determinism due to the possible interleaving of local actions and
    communication of different sequential processes. To distinguish these two types of non-determinism,
    we decide to model quantum measurements and probabilistic assignments in a (standard) probabilistic
    way.                                                                                                    J
       The following lemma, which can be easily proved by inspecting the transition rules in Table 1,
    shows that → is indeed a relation from configurations to probability distributions of configurations.
                                                                 P                            P
    I Lemma 5. Let hS, σ, ρi be a configuration and hS, σ, ρi → i∈I pi ·hSi , σi , ρi i. Then i∈I pi =
    1.

        The next lemma extends the Change and Access lemma for classical programs by considering the
    effects of transitions on quantum states.

     I Lemma 6 (Change and Access). Let hS, σ, ρi → µ. Then there exist a set {Si : i ∈ I} of
     distributed programs with v(Si ) ⊆ v(S) for v ∈ {change, qv, cv}, a set {fi : i ∈ I} of functions
     over Σ, and a set {Ei : i ∈ I} of super-operators acting on Hqv(S) such that
    (1) for each i, fi does not change the value of variables outside change(S). That is, for all τ ∈ Σ,
         fi (τ )|V = τ |V where V , cVar\change(S);
    (2) for each i, fi depends only on cv(S). That is, fi (σ)|cv(S) = fi (τ )|cv(S) whenever σ|cv(S) =
         τ |cv(S) ;
         P
    (3)      i∈IPEi is trace-nonincreasing;
    (4) µ = i∈I,pi >0 pi · hSi , fi (σ), Ei (ρ)/pi i where pi = tr(Ei (ρ));
    (5) for any σ 0 which agrees with σ on cv(S), i.e. σ 0 |cv(S) = σ|cv(S) , and ρ0 ∈ D(HV ) with
         V ⊇ qv(S),
                               X
              hS, σ 0 , ρ0 i →       p0i · hSi , fi (σ 0 ), Ei (ρ0 )/p0i i                           (1)
                           i∈I,p0i >0


        where p0i = tr(Ei (ρ0 )).

        A configuration is called a terminal if it has no successor distributions. Because of the communic-
    ation constraints, distributed programs can also end up with a deadlock configuration, in which not all
    the processes terminate properly (become E), and none of them has led to a failure (the classical state
    becomes fail). In other words, hS, σ, ρi is a terminal iff S ≡ E, σ ≡ fail, or it is a deadlock. For a
                      P
    distribution µ = i∈I pi · hSi , σi , ρi i of configurations, we denote by
                                                      X
                                        ∆µ ,                     hσi , pi ρi i
                                               i∈I,Si ≡E,σi 6≡fail
Y. Feng, S. Li, and M. Ying                                                                                 9


the cq-state obtained by restricting µ on the properly terminated configurations. Let Prµ (E) , tr(∆µ )
be the probability of µ having properly terminated.
    The transition relation → defined above can be further extended to distributions of configurations
                                P
by letting µ → ν where µ = i∈I pi · ci if (1) for each i, ci → νi for some νi whenever ci is not a
                                                P
terminal; otherwise, let νi , ci , and (2) ν = i∈I pi · νi . It is easy to check that such a ν is a valid
distribution over configurations. Let →k be the k-fold composition of →, and →∗ , k≥0 →k the
                                                                                          S

reflexive and transitive closure of →.
    Let S ∈ Prog, and hσ, ρi ∈ SV with V ⊇ qv(S) and tr(ρ) = 1. A computation of S starting
in hσ, ρi is an infinite sequence π , {µi : i ≥ 0} of distributions over configurations where
µ0 = hS, σ, ρi and for each i ≥ 0, µi → µi+1 .
I Lemma 7. Let π , {µi : i ≥ 0} be a computation starting in hσ, ρi. Then ∆µ0 v ∆µ1 v . . ..
    With Lemma 7, we can define for any computation π , {µi : i ≥ 0} the cq-state computed by π
         W
as ∆π , i≥0 ∆µi , the least upper bound of ∆µi according to v.
I Example 8 (Operational Semantics of Quantum Teleportation). Let σ be a classical state
and |ψi a pure state in H2 . Then one of the computations, denoted π, of Teleport starting in
hσ, |ψiq hψ| ⊗ |βiq1 ,q2 hβ|i is shown as follows:
             hTeleport, σ, [|ψ, βi]i
               X 1
      →5               · doa kdob , σ[i/xA , j/zA , 0/stageA , 0/stageB , [|j, i, X i Z j ψi]
             i,j=0,1
                     4
               X 1
       →               · hstageA := 1; doa kstageB := 1; if xB = 1 → q2 ∗= X  ¬(xB = 1) →
             i,j=0,1
                     4

                        skip; dob , σ[i/xA , j/zA , 0/stageA , 0/stageB , i/xB ], [|j, i, X i Z j ψi]
               X 1
      →4               · doa kdob , σ[i/xA , j/zA , 1/stageA , 1/stageB , i/xB ], [|j, i, Z j ψi]
             i,j=0,1
                     4
               X 1
      →5               · hdoa kdob , σ[i/xA , j/zA , 2/stageA , 2/stageB , i/xB , j/zB ], [|j, i, ψi]i
             i,j=0,1
                     4
                    X 1
      →2     µ,             · hE, σ[i/xA , j/zA , 2/stageA , 2/stageB , i/xB , j/zB ], [|j, i, ψi]i
                  i,j=0,1
                          4
       →     µ → ···
where doa and dob are the do-loops of Alice and Bob, respectively. For pure state |φi, we denote by
[|φi] its corresponding density operator |φihφ|. Thus
                    X                                                        1
                                                                                          
            ∆π =          σ[i/xA , j/zA , 2/stageA , 2/stageB , i/xB , j/zB ], [|j, i, ψi] .
                  i,j=0,1
                                                                              4

    Note that although each component process of a distributed program is deterministic, the whole
program can still exhibit nondeterminism. This is due to the interleaving nature of local actions of
individual processes and communication between disjoint pairs of processes; see Rules (Paral) and
(Comm) in Table 1. However, the following theorem shows that these different computations actually
compute the same cq-state.
I Theorem 9 (Determinism). Let S ∈ Prog be a distributed quantum program, and hσ, ρi ∈ SV
with V ⊇ qv(S) and tr(ρ) = 1. Then the set
                           {∆π : π is a computation of S starting in hσ, ρi}
has exactly one element.
10   Verification of Distributed Quantum Programs


     3.3       Denotational Semantics
     With Theorem 9, the denotational semantics of distributed quantum programs can be defined using
                                       S
     the operational one. Let S⊇qv(S) , V ⊇qv(S) SV .

      I Definition 10. Let S ∈ Prog. The denotational semantics of S is a mapping [[S ]] : S⊇qv(S) →
      S⊇qv(S) such that
     (1) for any hσ, ρi ∈ SV with V ⊇ qv(S) and tr(ρ) = 1,

                 [[S ]](σ, ρ) , the unique element in {∆π : π is a computation of S starting in hσ, ρi};
                           L
     (2) for any ∆ =           i∈I hσi , ρi i (thus tr(ρi ) > 0 for any i ∈ I),
                                                                                                
                                                         X                               ρi
                                           [[S ]](∆) ,         tr(ρi ) · [[S ]] σi ,                 .
                                                                                       tr(ρi )
                                                         i∈I


        To simplify notation, we always write (σ, ρ) for (hσ, ρi) when hσ, ρi appears as a parameter of
     some function. The next lemma guarantees the well-definedness of Definition 10.

      I Lemma 11. Let S ∈ Prog and ∆ ∈ SV with V ⊇ qv(S). Then
     (1) [[S ]](∆) has countable support, and tr([[S ]](∆)) ≤ tr(∆). Hence [[S ]](∆) ∈ SV as well;
                                     P                                P
     (2) for any λi ∈ R, [[S ]](∆) = i λi · [[S ]](∆i ) whenever ∆ = i λi · ∆i .


       4       Transformation to sequential quantum programs

     Throughout this section, we consider a distributed quantum program S , S1 k · · · kSn where for each
     i,

           Si , Si,0 ; do m
                           j=1 Bi,j ; αi,j → Si,j od.
                             i




     The transformation of S into a sequential one follows the standard approach for classical (non-
     probabilistic) programs [1].
         Let Γ , {(i, j, k, `) : αi,j and αk,` match, and i < k}. That is, Γ collects all the pairs of
     generalised guards in the component processes which are able to communicate. The sequentialisation
     of S is defined as

           T (S) , S1,0 ; . . . ; Sn,0 ;
                     do (i,j,k,`)∈Γ Bi,j ∧ Bk,` ∧ Bi → Effect(αi,j , αk,` ); Si,j ; Sk,`
                     od
                   V
     where Bi , (t,j,k,`)∈Γ,t<i ¬(Bt,j ∧ Bk,` ). When Γ is empty, we simply drop the do loop in the
     definition.
         Note that we introduce an additional condition Bi here to guarantee that the resultant quantum
     program is deterministic (so that it can be described in the language presented in Sec. 2.1). This is
     unnecessary for classical programs in [1], since verification of nondeterministic classical programs
     has been well investigated. However, from Theorem 9 the nondeterministic choices in S do not really
     matter in computing the final cq-state. Therefore, introducing the additional condition Bi does not put
     any restriction on the expressiveness of the sequentialised program T (S); this will be more rigorously
     shown with Theorem 12 below.
 Y. Feng, S. Li, and M. Ying                                                                                       11


    It is obvious that S and T (S) are not semantically equivalent: at least they have different
 conditions for termination. To see this, let
               ^ mi
               n ^                                ^                               ^
  TERM ,                  ¬Bi,j ,   BLOCK ,                 ¬(Bi,j ∧Bk,` ) =                 ¬(Bi,j ∧Bk,` ∧Bi ).
               i=1 j=1                        (i,j,k,`)∈Γ                      (i,j,k,`)∈Γ


Then S terminates iff TERM holds while T (S) terminates iff BLOCK holds. Note that TERM →
BLOCK but generally the reverse direction is not true.
   The following theorem shows that S and T (S) are indeed equivalent conditioning on TERM .

 I Theorem 12. For any cq-state ∆ ∈ SV with V ⊇ qv(S), [[S ]](∆) = [[T (S)]](∆)|TERM , the
 restriction of [[T (S)]](∆) on the set of classical states σ with σ |= TERM .

 I Example 13 (Sequentialisation of Teleportation). The sequentialisation of T eleport, denoted
 T (Teleport), is as follows:

      q, q1 ∗= CNOT; q ∗= H; zA := meas q; xA := meas q1 ;
      stageA := 0; stageB := 0;
      do stageA = 0 ∧ stageB = 0 → xB := xA ;
                stageA := 1; stageB := 1; if xB = 1 → q2 ∗= X  ¬(xB = 1) → skip fi
        stageA = 1 ∧ stageB = 1 → zB := zA ;
                stageA := 2; stageB := 2; if zB = 1 → q2 ∗= Z  ¬(zB = 1) → skip fi
      od

 It is easy to see that

      [[T eleport]](∆) = [[T (T eleport)]](∆)|stageA 6∈{0,1}∧stageB 6∈{0,1} .


  5        Verification of distributed quantum programs
The basic notion for verification of distributed quantum programs is classical-quantum assertion
from [16].

 5.1       Classical-quantum assertions
 Recall that assertions for classical program states are usually represented as first order logic formulas
 over cVar. For any classical assertion p, denote by [[p]] , {σ ∈ Σ : σ |= p} the set of classical states
 that satisfy p. Two assertions p and p0 are equivalent, written p ≡ p0 , iff [[p]] = [[p0 ]]. Let P(HV ) be
 the set of Hermitian operators on H whose eigenvalues lie between 0 and 1.

 I Definition 14. Given V ⊆ qVar, a classical-quantum assertion (cq-assertion for short) Θ over
 V is a function in Σ → P(HV ) such that
(1) the image set Θ(Σ) of Θ is countable;
(2) for each M ∈ Θ(Σ), the preimage Θ−1 (M ) is definable by a classical assertion p in the sense
     that [[p]] = Θ−1 (M ).
                                                                               L
     Denote by qv(Θ) the set V of quantum variables in Θ. We write i∈I hpi , Mi i instead of
                                                                                     −1
 L
         [[ ]]
    i∈I h pi , Mi i for a cq-assertion Θ whenever Θ(Σ) = {Mi : i ∈ I} and Θ             (Mi ) = [[pi ]] for
 each i ∈ I. Note that this representation is not unique: the representative assertion pi can be replaced
 by p0i whenever pi ≡ p0i . Furthermore, the summand with zero operator 0HV is always omitted. In
12   Verification of Distributed Quantum Programs


     particular, when Θ(Σ) = {0H , M } or {M } for some M 6= 0HV , we simply denote Θ by hp, M i for
     some p with Θ−1 (M ) = [[p]].
          Let AV be the set of all cq-assertions over V , and A the set of all cq-assertions. Again, we extend
     the Löwner order vV for L(HV ) pointwisely to A by letting Θ v Θ0 iff qv(Θ) = qv(Θ0 ) and for all
     σ ∈ Σ, Θ(σ) vqv(Θ) Θ0 (σ). It is easy to see that AV is also a pointed ω-CPO under v, with the least
     element being ⊥V . Furthermore, it has the largest element >V , htrue, IHV i. When Θ v Θ0 , we
     denote by Θ0 − Θ the unique Θ00 ∈ Aqv(Θ) such that Θ00 + Θ = Θ0 . With these notions, summation
     and linear-sum of cq-assertions can be defined similarly as for cq-states. Let V1 , V2 be two subsets
     of qVar, and Θi ∈ AVi , i = 1, 2. We say Θ1 . Θ2 whenever Θ1 ⊗ IHV2 \V1 v IHV1 \V2 ⊗ Θ2 .
     Obviously, when restricted on some given set of quantum variables, . coincides with v.
                                                              P                               P
          Given a classical assertion p, we denote by p ./ i hpi , Mi i the cq-assertion i hp ./ pi , Mi i
     (if it is valid) where ./ can be any logic connective such as ∧, ∨, ⇒, ⇔, etc. Let F be a completely
     positive and sub-unital linear map from P(HV ) to P(HW ). We extend it to AV in a pointwise
     way. In particular, when qv(Θ) ∩ W = ∅, Θ ⊗ IHW is a cq-assertion which maps any σ ∈ Σ to
     Θ(σ) ⊗ IHW .

     I Definition 15. Given a cq-state ∆ and a cq-assertion Θ with qv(∆) ⊇ qv(Θ), the expectation of
     ∆ satisfying Θ is defined to be
                            X                                     X
         Exp(∆ |= Θ) ,             tr [(Θ(σ) ⊗ IHV ) · ∆(σ)] =           tr [Θ(σ) · trHV (∆(σ))]
                           σ∈d∆e                                 σ∈d∆e


     where V = qv(∆)\qv(Θ) and the dot · denotes matrix multiplication.


     5.2    Correctness formula
     As usual, program correctness is expressed by correctness formulas with the form {Θ} S {Ψ}
     where S is a distribute quantum program, and Θ and Ψ are both cq-assertions. We do not put any
     requirement on the quantum variables which Θ and Ψ are acting on. In fact, the sets qv(S), qv(Θ),
     and qv(Ψ) can be all different.

     I Definition 16. Let S ∈ Prog, and Θ and Ψ be cq-assertions.
     (1) We say the correctness formula {Θ} S {Ψ} is true in the sense of total correctness, written
         |=tot {Θ} S {Ψ}, if for any V ⊇ qv(S, Θ, Ψ) and ∆ ∈ SV ,

                                       Exp(∆ |= Θ) ≤ Exp([[S ]](∆) |= Ψ).

     (2) We say the correctness formula {Θ} S {Ψ} is true in the sense of partial correctness, written
         |=par {Θ} S {Ψ}, if for any V ⊇ qv(S, Θ, Ψ) and ∆ ∈ SV ,

                          Exp(∆ |= Θ) ≤ Exp([[S ]](∆) |= Ψ) + tr(∆) − tr([[S ]](∆)).

     I Example 17. The correctness of quantum teleportation can be stated as follows: for any |ψi ∈ H2 ,

         |=tot {|ψiq ⊗ |βiq1 ,q2 } Teleport {|ψiq2 } ,

     which claims that the (arbitrary) quantum state of qubit q is successfully transmitted to qubit q2
     by Teleport. Note that the postcondition |ψiq2 does not refer to q and q1 , meaning that the post-
     measurement state of these quantum systems is irrelevant.
Y. Feng, S. Li, and M. Ying                                                                                                                 13



   (Skip)                       {Θ} skip {Θ}                         (Abort)                     {>V } abort {⊥V }
                                                                                                                    
                                                                                         X                          
   (Assn)                    {Θ[e/x]} x := e {Θ}                     (Rassn)                         g(d) · Θ[d/x]       x :=$ g{Θ}
                                                                                                                    
                                                                                        d∈Dtype(x)


                                   q ∈ qv(Θ)                                                           q̄ ⊆ qv(Θ)
   (Init)                                                            (Unit)
                                                                                                 Uq̄† ΘUq̄ q̄ ∗= U {Θ}
                  nP                          o                                              
                    dq −1
                       i=0
                              |iiq h0|Θ|0iq hi|   q := 0 {Θ}

                       q̄ ⊆ qv(Θ), M = {Mi : i ∈ I}                                       {Θ} S0 {Θ0 } , {Θ0 } S1 {Ψ}
   (Meas)                                                            (Seq)
                       Mi† Θ[i/x]Mi x := meas M[q̄] {Θ}
              P
                                                                                               {Θ} S0 ; S1 {Ψ}
                   i∈I

                    {Bi ∧ Θ} Si {Ψ} , ∀i ∈ {1, . . . , n}                           {Bi ∧ Θ} Si {Θ} , ∀i ∈ {1, . . . , n}
   (Alt)                                                             (Rep)                                     Vn
                       {Θ} if n
                                                                                                        
                               i=1 Bi → Si fi {Ψ}                                {Θ} do n
                                                                                         i=1 Bi → Si od   Θ ∧ i=1 ¬Bi
                     Θ . Θ0 , {Θ0 } S {Ψ0 } , Ψ0 . Ψ
   (Imp)
                               {Θ} S {Ψ}
             {Θ} S1,0 ; . . . ; Sn,0 {Ψ} , {Bi,j ∧ Bk,` ∧ Ψ} Effect(αi,j , αk,` ); Si,j ; Sk,` {Ψ} , ∀(i, j, k, `) ∈ Γ
   (Dist)
                                                {Θ} S1 k . . . kSn {Ψ ∧ TERM }

                                           where Γ and TERM are defined as in Sec. 4.



    Table 2 Proof system for partial correctness.



5.3         Proof systems
The core of Hoare logic is a proof system consisting of axioms and proof rules which enable syntax-
oriented and modular reasoning of program correctness. In this section, we propose a Hoare logic for
distributed quantum programs.
    Partial correctness. We propose in Table 2 a proof system for partial correctness of distributed
quantum programs, which is a natural extension of the quantum Hoare logic introduced in [16] for
deterministic while programs. We write `par {Θ} S {Ψ} if the correctness formula {Θ} S {Ψ}
can be derived from the system.
I Theorem 18. The proof system in Table 2 is both sound and (relatively) complete with respect to
the partial correctness of distributed quantum programs.
    Total correctness. Ranking functions play a central role in proving total correctness of while
loop programs. Recall that in the classical case, a ranking function maps each reachable state in the
loop body to an element of a well-founded ordered set (say, the set N of nonnegative integers), such
that the value decreases strictly after each iteration of the loop. Our proof rules for total correctness of
repetitive commands and distributed quantum programs also heavily relies on the notion of ranking
assertions.
I Definition 19. Let Θ ∈ AV . A decreasing sequence (w.r.t. v) of cq-assertions {Θk : k ≥ 0} in
AV with Θ v Θ0 and k Θk = ⊥V are Θ-ranking assertions for do ni=1 Bi → Si od if for any
                      V
                                   Sn
k ≥ 0, 1 ≤ i ≤ n, and ∆ ∈ SW , W , i=1 qv(Si ) ∪ V ,
    Exp([[Si ]](∆|Bi ) |= Θk ) ≤ Exp(∆ |= Θk+1 ).                                                                                     (2)
They are said to be Θ-ranking assertions for S1 k . . . kSn if, for any k ≥ 0, (i, j, t, `) ∈ Γ, and
               Sn
∆ ∈ SW , W , i=1 qv(Si ) ∪ V , we have
           t,`
    Exp([[Si,j ]](∆|Bi,j ∧Bt,` ) |= Θk ) ≤ Exp(∆ |= Θk+1 )
       t,`
where Si,j , Effect(αi,j , αt,` ); Si,j ; St,` .
14   Verification of Distributed Quantum Programs


      (Abort-T)                                    {⊥V } abort {⊥V }
                                       Wn
                                 Θ.      i=1
                                               Bi , {Bi ∧ Θ} Si {Ψ} , ∀i ∈ {1, . . . , n}
      (Alt-T)
                                               {Θ} if n i=1 Bi → Si fi {Ψ}


                                  {Bi ∧ Θ} Si {Θ} , ∀i ∈ {1, . . . , n}
                                  Θ-ranking assertions exist for do ni=1 Bi → Si od
      (Rep-T)                                                            Vn
                                    {Θ} do n
                                            i=1 Bi → Si od           Θ∧     i=1
                                                                                  ¬Bi

                       {Θ} S1,0 ; . . . ; Sn,0 {Ψ}, and Ψ-ranking assertions exist for S1 k . . . kSn
                       {Bi,j ∧ Bk,` ∧ Ψ} Effect(αi,j , αk,` ); Si,j ; Sk,` {Ψ} , ∀(i, j, k, `) ∈ Γ
                       Ψ ∧ BLOCK . TERM
      (Dist-T)
                                              {Θ} S1 k . . . kSn {Ψ ∧ TERM }

                                      where Γ and TERM are defined as in Sec. 4.


          Table 3 Some proof rules for total correctness.




         The proof system for total correctness is then defined as for partial correctness, except that the
     rules (Abort), (Alt), (Rep), and (Dist) are replaced by their corresponding total correctness version
     shown in Table 3. We write `tot {Θ} S {Ψ} if the correctness formula {Θ} S {Ψ} can be derived
     using this proof system.


     I Theorem 20. The proof system for total correctness is both sound and (relatively) complete with
     respect to the total correctness of distributed quantum programs.



      6       Conclusion and future works

     In this paper, we propose a distributed programming language for the purpose of formal description
     and verification of distributed quantum systems. A Hoare-style logic, which turns out to be sound and
     (relatively) complete for both partial and total correctness, is introduced to help analysis of quantum
     programs written in this language. Effectiveness of the logic is demonstrated by its application
     in verification of quantum teleportation and local implementation of non-local CNOT gates, two
     important protocols widely used in distributed quantum systems.
         The distributed language investigated in this paper only allows local quantum operations and
     classical communication (LOCC). Although LOCC is a widely used quantum communication model,
     there are also important quantum communication protocols, such as Quantum Key Distribution [4]
     and Quantum Leader Election [34], which do require transmission of quantum states. It is well known
     that this kind of quantum communication can be achieved by employing the teleportation protocol
     (provided that enough entanglement is pre-shared between relevant parties), and thus in principle
     these protocols can be verified using the logic presented in this paper, but their verification in this way
     will be clumsy and inconvenient. Therefore, it is desirable to extend our language to include quantum
     communication in future works. To this end, we have to trace the ownership of each quantum system
     so that the no-cloning property [38] of quantum information is not violated. We expect that the
     verification of such distributed quantum programs will be much more challenging.
Y. Feng, S. Li, and M. Ying                                                                                15


     References
 1   Krzysztof Apt, Frank S De Boer, and Ernst-Rüdiger Olderog. Verification of sequential and con-
     current programs. Springer Science & Business Media, 2010.
 2   Krzysztof R. Apt. Correctness proofs of distributed termination algorithms. ACM Trans. Program.
     Lang. Syst., 8(3):388–405, 1986.
 3   Krzysztof R Apt, Luc Bougé, and Ph Clermont. Two normal form theorems for CSP programs.
     Information Processing Letters, 26(4):165–171, 1987.
 4   Charles H Bennett and Gilles Brassard. Quantum cryptography: Public key distribution and coin
     tossing. In Proceedings of the International Conference on Computers, Systems and Signal Pro-
     cessing, 1984.
 5   Charles H Bennett, Gilles Brassard, Claude Crépeau, Richard Jozsa, Asher Peres, and William K
     Wootters. Teleporting an unknown quantum state via dual classical and Einstein-Podolsky-Rosen
     channels. Physical Review Letters, 70(13):1895, 1993.
 6   Charles H Bennett and Stephen J Wiesner. Communication via one-and two-particle operators on
     Einstein-Podolsky-Rosen states. Physical Review Letters, 69(20):2881, 1992.
 7   H-J Briegel, Wolfgang Dür, Juan I Cirac, and Peter Zoller. Quantum repeaters: the role of imperfect
     local operations in quantum communication. Physical Review Letters, 81(26):5932, 1998.
 8   Stephen D Brookes, Charles AR Hoare, and Andrew W Roscoe. A theory of communicating
     sequential processes. Journal of the ACM (JACM), 31(3):560–599, 1984.
 9   Rohit Chadha, Paulo Mateus, and Amílcar Sernadas. Reasoning about imperative quantum pro-
     grams. Electronic Notes in Theoretical Computer Science, 158:19–39, 2006.
10   Daniele Cuomo, Marcello Caleffi, and Angela Sara Cacciapuoti. Towards a distributed quantum
     computing ecosystem. IET Quantum Communication, 1(1):3–8, 2020.
11   Edsger Wybe Dijkstra. A Discipline of Programming. Prentice-Hall Englewood Cliffs, 1976.
12   Jens Eisert, Kurt Jacobs, Polykarpos Papadopoulos, and Martin B Plenio. Optimal local implement-
     ation of nonlocal quantum gates. Physical Review A, 62(5):052317, 2000.
13   Yuan Feng, Runyao Duan, Zhengfeng Ji, and Mingsheng Ying. Probabilistic bisimulations for
     quantum processes. Information and Computation, 205(11):1608–1639, 2007.
14   Yuan Feng, Runyao Duan, Zhengfeng Ji, and Mingsheng Ying. Proof rules for the correctness of
     quantum programs. Theoretical Computer Science, 386(1-2):151–166, 2007.
15   Yuan Feng, Runyao Duan, and Mingsheng Ying. Bisimulation for quantum processes. ACM Trans.
     Program. Lang. Syst., 34(4):17:1–17:43, 2012.
16   Yuan Feng and Mingsheng Ying. Quantum Hoare logic with classical variables. ACM Transactions
     on Quantum Computing, to appear, 2021.
17   Simon J. Gay and Rajagopal Nagarajan. Communicating quantum processes. In Jens Palsberg and
     Martín Abadi, editors, Proceedings of the 32nd ACM SIGPLAN-SIGACT Symposium on Principles
     of Programming Languages, POPL 2005, Long Beach, California, USA, January 12-14, 2005,
     pages 145–157. ACM, 2005.
18   Daniel Gottesman and Isaac L Chuang. Demonstrating the viability of universal quantum compu-
     tation using teleportation and single-qubit operations. Nature, 402(6760):390–393, 1999.
19   Eric CR Hehner. A Practical Theory of Programming. Springer Science & Business Media, 2012.
20   Charles Antony Richard Hoare. An axiomatic basis for computer programming. Communications
     of the ACM, 12(10):576–580, 1969.
21   Charles Antony Richard Hoare. Communicating sequential processes. Communications of the
     ACM, 21(8):666–677, 1978.
22   Satoshi Ishizaka and Tohya Hiroshima. Asymptotic teleportation scheme as a universal program-
     mable quantum processor. Physical Review Letters, 101(24):240501, 2008.
23   Philippe Jorrand and Marie Lalire. Toward a quantum process algebra. In Stamatis Vassiliadis,
     Jean-Luc Gaudiot, and Vincenzo Piuri, editors, Proceedings of the First Conference on Computing
     Frontiers, 2004, Ischia, Italy, April 14-16, 2004, pages 111–119. ACM, 2004.
16   Verification of Distributed Quantum Programs


     24   Yoshihiko Kakutani. A Logic for Formal Verification of Quantum Programs. Lecture Notes in
          Computer Science, pages 79–93, 2009.
     25   H. J. Kimble. The quantum internet. Nature, 453(7198):1023–1030, 2008.
     26   Wojciech Kozlowski and Stephanie Wehner. Towards large-scale quantum networks. In Proceed-
          ings of the Sixth Annual ACM International Conference on Nanoscale Computing and Communic-
          ation, NANOCOM 2019, Dublin, Ireland, September 25-27, 2019, pages 3:1–3:7. ACM, 2019.
     27   Karl Kraus, Arno Böhm, John D Dollard, and WH Wootters. States, effects, and operations: funda-
          mental notions of quantum theory. Lecture Notes in Physics, 190, 1983.
     28   Michael A Nielsen and Isaac Chuang. Quantum Computation and Quantum Information. Cam-
          bridge University Press, 2002.
     29   Stefano Pirandola, Jens Eisert, Christian Weedbrook, Akira Furusawa, and Samuel L Braunstein.
          Advances in quantum teleportation. Nature Photonics, 9(10):641–652, 2015.
     30   M. Pompili, S. L. N. Hermans, S. Baier, H. K. C. Beukers, P. C. Humphreys, R. N. Schouten,
          R. F. L. Vermeulen, M. J. Tiggelman, L. dos Santos Martins, B. Dirkse, S. Wehner, and R. Hanson.
          Realization of a multinode quantum network of remote solid-state qubits. Science, 372(6539):259–
          264, 2021.
     31   Robert Raussendorf and Hans J Briegel. A one-way quantum computer. Physical Review Letters,
          86(22):5188, 2001.
     32   Peter Selinger. Towards a quantum programming language. Mathematical Structures in Computer
          Science, 14(4):527–586, 2004.
     33   Anya Tafliovich and Eric CR Hehner. Programming with quantum communication. Electronic
          Notes in Theoretical Computer Science, 253(3):99–118, 2009.
     34   Seiichiro Tani, Hirotada Kobayashi, and Keiji Matsumoto. Exact quantum algorithms for the leader
          election problem. In Annual Symposium on Theoretical Aspects of Computer Science, pages 581–
          592. Springer, 2005.
     35   Dominique Unruh. Quantum hoare logic with ghost variables. In 2019 34th Annual ACM/IEEE
          Symposium on Logic in Computer Science (LICS), pages 1–13. IEEE, 2019.
     36   John Von Neumann. Mathematical Foundations of Quantum Mechanics. Princeton University
          Press, Princeton, NJ, 1955.
     37   Stephanie Wehner, David Elkouss, and Ronald Hanson. Quantum internet: A vision for the road
          ahead. Science, 362(6412), 2018.
     38   William K Wootters and Wojciech H Zurek. A single quantum cannot be cloned. Nature,
          299(5886):802–803, 1982.
     39   Mingsheng Ying. Floyd–Hoare logic for quantum programs. ACM Transactions on Programming
          Languages and Systems (TOPLAS), 33(6):1–49, 2012.
     40   Mingsheng Ying. Foundations of Quantum Programming. Morgan Kaufmann, 2016.
     41   Mingsheng Ying. Toward automatic verification of quantum programs. Formal Aspects of Comput-
          ing, 31(1):3–25, 2019.
     42   Mingsheng Ying, Yuan Feng, Runyao Duan, and Zhengfeng Ji. An algebra of quantum processes.
          ACM Transactions on Computational Logic (TOCL), 10(3):1–36, 2009.
     43   Dieter Zoebel. Normalform-Transformationen für CSP-Programme. Informatik (Berlin, West),
          3(2):64–76, 1988.
Y. Feng, S. Li, and M. Ying                                                                                  17


 A      Preliminaries

This section is devoted to fixing some notations from linear algebra and quantum mechanics that will
be used in this paper. For a thorough introduction of relevant backgrounds, we refer to [28, Chapter
2].


A.1     Basic linear algebra
Let H be a Hilbert space. In the finite-dimensional case which we are concerned with here, it is
merely a complex linear space equipped with an inner product. Consequently, it is isomorphic to Cd
where d = dim(H), the dimension of H. Following the tradition in quantum computing, vectors in
H are denoted in the Dirac form |ψi. The inner product of |ψi and |φi is written hψ|φi, and they are
orthogonal if hψ|φi = 0. The outer product of them, denoted |ψihφ|, is a rank-one       plinear operator
which maps any |ψ 0 i in H to hφ|ψ 0 i|ψi. The length of |ψi is defined to be k|ψik , hψ|ψi and it is
called normalised if k|ψik = 1. A set of vectors B , {|ii : i ∈ I} in H is orthonormal if each |ii
is normalised and every two of them are orthogonal. Furthermore, if they span the whole space H;
that is, any vector in H can be written as a linear combination of vectors in B, then B is called an
orthonormal basis of H.
    Let L(H) be the set of linear operators on H, and 0H and IH the zero and identity operators
                                                                                P
respectively. Let A ∈ L(H). The trace of A is defined to be tr(A) , i∈I hi|A|ii for some (or,
equivalently, any) orthonormal basis {|ii : i ∈ I} of H. The adjoint of A, denoted A† , is the unique
linear operator in L(H) such that hψ|A|φi = hφ|A† |ψi∗ for all |ψi, |φi ∈ H. Here for a complex
number z, z ∗ denotes its conjugate. Operator A is said to be normal if A† A = AA† , hermitian if
A† = A, unitary if A† A = IH , and positive if for all |ψi ∈ H, hψ|A|ψi ≥ 0. Obviously, hermitian
operators are normal, and both unitary operators and positive ones are hermitian. Any normal operator
                                                             P
A can be written into a spectral decomposition form A = i∈I λi |iihi| where {|ii : i ∈ I} constitute
some orthonormal basis of H. Furthermore, if A is hermitian, then all λi ’s are real; if A is unitary,
then all λi ’s have unit length; if A is positive, then all λi ’s are non-negative. The Löwner (partial)
order vH on the set of hermitian operators on H is defined by letting A vH B iff B − A is positive.
    Let H1 and H2 be two finite dimensional Hilbert spaces, and H1 ⊗ H2 their tensor product. Let
Ai ∈ L(Hi ). The tensor product of A1 and A2 , denoted A1 ⊗ A2 is a linear operator in L(H1 ⊗ H2 )
such that (A1 ⊗ A2 )|(ψ1 i ⊗ |ψ2 )i = (A1 |ψ1 i) ⊗ (A2 |ψ2 i) for all |ψi i ∈ Hi . To simplify notations,
we often write |ψ1 i|ψ2 i for |ψ1 i ⊗ |ψ2 i. Given H1 and H2 , the partial trace with respect to H2 ,
denoted trH2 , is a linear mapping from L(H1 ⊗ H2 ) to L(H1 ) such that for any |ψi i, |φi i ∈ Hi ,
i = 1, 2,
                            trH2 (|ψ1 ihφ1 | ⊗ |φ1 ihφ2 |) = hφ2 |φ1 i|ψ1 ihφ1 |.

The definition is extended to L(H1 ⊗ H2 ) by linearity.
     A linear operator E from L(H1 ) to L(H2 ) is called a super-operator. It is said to be (1) positive
if it maps positive operators to positive operators; (2) completely positive if all the cylinder extension
IH ⊗ E is positive for all finite dimensional Hilbert space H, where IH is the identity super-
operator on L(H); (3) trace-preserving (resp. trace-nonincreasing) if tr(E(A)) = tr(A) (resp.
tr(E(A)) ≤ tr(A) for any positive operator A ∈ L(H1 ); (4) unital (resp. sub-unital) if E(IH1 ) = IH2
(resp. E(IH1 ) vH2 IH2 ). From Kraus representation theorem [27], a super-operator E from L(H1 )
to L(H2 ) is completely positive iff there is some set of linear operators, called Kraus operators,
{Ei : i ∈ I} from H1 to H2 such that E(A) = i∈I Ei AEi† for all A ∈ L(H1 ). It is easy to
                                                       P

check that the trace and partial trace operations defined above are both completely positive and trace-
preserving super-operators. Given a completely positive super-operator E from L(H1 ) to L(H2 ) with
Kraus operators {Ei : i ∈ I}, the adjoint of E, denoted E † , is a completely positive super-operator
18   Verification of Distributed Quantum Programs


     from L(H2 ) back to L(H1 ) with Kraus operators {Ei† : i ∈ I}. Then we have (E † )† = E, and E is
     trace-preserving (resp. trace-nonincreasing) iff E † is unital (resp. sub-unital). Furthermore, for any
     A ∈ L(H1 ) and B ∈ L(H2 ), tr(E(A) · B) = tr(A · E † (B)).

     A.2    Basic quantum mechanics
     According to von Neumann’s formalism of quantum mechanics [36], any quantum system with
     finite degrees of freedom is associated with a finite-dimensional Hilbert space H called its state
     space. When dim(H) = 2, we call such a system a qubit, the analogy of bit in classical computing.
     A pure state of the system is described by a normalised vector in H. When the system is in one
     of an ensemble of states {|ψi i : i ∈ I} with respective probabilities pi , we say it is in a mixed
                                                   P
     state, represented by the density operator i∈I pi |ψi ihψi | on H. Obviously, a density operator is
     positive and has trace 1. Conversely, by spectral decomposition, any positive operator with unit trace
     corresponds to some (not necessarily unique) mixed state.
         The state space of a composite system (for example, a quantum system consisting of multiple
     qubits) is the tensor product of the state spaces of its components. For a mixed state ρ in H1 ⊗ H2 ,
     partial traces of ρ have explicit physical meanings: the density operators trH1 (ρ) and trH2 (ρ) are
     exactly the reduced quantum states of ρ on the second and the first component systems, respectively.
     Note that in general, the state of a composite system cannot be decomposed into tensor product of
     the reduced states on its component systems. A well-known example is the 2-qubit state |Ψi =
     √1 (|00i + |11i). This kind of state is called entangled state, and usually is the key to many quantum
       2
     information processing tasks such as teleportation [5] and superdense coding [6].
         The evolution of a closed quantum system is described by a unitary operator on its state space: if
     the states of the system at times t1 and t2 are ρ1 and ρ2 , respectively, then ρ2 = U ρ1 U † for some
     unitary operator U which depends only on t1 and t2 . In contrast, the general dynamics which can
     occur in a physical system is described by a completely positive and trace-preserving super-operator
     on its state space. Note that the unitary transformation EU (ρ) , U ρU † is such a super-operator.
         A quantum measurement M is described by a collection {Mi : i ∈ I} of linear operators on H,
     where I is the set of measurement outcomes. It is required that the measurement operators satisfy
     the completeness equation i∈I Mi† Mi = IH . If the system is in state ρ, then the probability that
                                  P

     measurement result i occurs is given by pi = tr(Mi† Mi ρ), and the state of the post-measurement
     system is ρi = Mi ρMi† /pi whenever pi > 0. Note that the super-operator

                                                                   Mi ρMi†
                                                   X           X
                                       EM : ρ 7→       pi ρi =
                                                  i∈I         i∈I

     which maps the initial state to the final (mixed) one when the measurement outcome is ignored is
     completely positive and trace-preserving. A particular case of measurement is projective measurement
     which is usually represented by a hermitian operator M in L(H) called observable. Let
                  X
        M=                mPm
               m∈spec(M )

     where spec(M ) is the set of eigenvalues of M , and Pm the projection onto the eigenspace associated
     with m. Obviously, the projectors {Pm : m ∈ spec(M )} form a quantum measurement.
         In this paper, we are especially concerned with the set
        P(H) , {M ∈ L(H) : 0H v M v IH }
     of observables whose eigenvalues lie between 0 and 1, where v is the Löwner order on L(H).
     Furthermore, following Selinger’s convention [32], we regard the set of partial density operators
        D(H) , {ρ ∈ L(H) : 0H v ρ, tr(ρ) ≤ 1}
Y. Feng, S. Li, and M. Ying                                                                               19


as (unnormalised) quantum states. Intuitively, the partial density operator ρ means that the legitimate
quantum state ρ/tr(ρ) is reached with probability tr(ρ). As a matter of fact, we note that D(H) ⊆
P(H).


  B     Some useful lemmas

We first recall some basic properties of cq-states and cq-assertions from [16].

 I Lemma 21 (Lemma 3.9, [16]). For any cq-state ∆ ∈ SV , cq-assertion Θ ∈ AW with W ⊆ V ,
 and classical assertion p,
(1) Exp(∆ |= Θ) ∈ [0, 1];
(2) Exp(⊥V |= Θ) = Exp(∆ |= ⊥W ) = 0, Exp(∆ |= >W ) = tr(∆);
                       P                       P
(3) Exp(∆ |= Θ) = i λi Exp(∆ |= Θi ) if Θ = i λi Θi ;
                       P                       P
(4) Exp(∆ |= Θ) = i λi Exp(∆i |= Θ) if ∆ = i λi ∆i ;
(5) Exp(∆|p |= Θ) = Exp(∆ |= p ∧ Θ);
(6) Exp(∆ |= F(Ψ)) = Exp(F † (∆) |= Ψ) for any Ψ ∈ AW 0 and any completely positive and
    sub-unital super-operator F from HW 0 to HW .

 I Lemma 22 (Lemma 3.10, [16]).
(1) For any cq-states ∆ and ∆0 in SV ,
      if ∆ v ∆0 , then Exp(∆ |= Θ) ≤ Exp(∆0 |= Θ) for all Θ ∈ AW with W ⊆ V ;
      conversely, if Exp(∆ |= Θ) ≤ Exp(∆0 |= Θ) for all Θ ∈ AV , then ∆ v ∆0 .
(2) For any cq-assertions Θ and Θ0 with W = qv(Θ) ∪ qv(Θ0 ),
      if Θ . Θ0 , then Exp(∆ |= Θ) ≤ Exp(∆ |= Θ0 ) for all ∆ ∈ SV with W ⊆ V ;
      conversely, if Exp(∆ |= Θ) ≤ Exp(∆ |= Θ0 ) for all ∆ ∈ SW , then Θ . Θ0 .

 I Lemma 23 (Lemma 3.11, [16]). For any cq-states ∆, ∆n ∈ SV and cq-assertions Θ, Θn ∈ AW
 with W ⊆ V , n = 1, 2, · · · ,
        W
(1) Exp( n≥0 ∆n |= Θ) = supn≥0 Exp(∆n |= Θ) for increasing sequence {∆n }n ;
        V
(2) Exp( n≥0 ∆n |= Θ) = inf n≥0 Exp(∆n |= Θ) for decreasing sequence {∆n }n ;
              W
(3) Exp(∆ |= n≥0 Θn ) = supn≥0 Exp(∆ |= Θn ) for increasing sequence {Θn }n ;
              V
(4) Exp(∆ |= n≥0 Θn ) = inf n≥0 Exp(∆ |= Θn ) for decreasing sequence {Θn }n .

    The following lemma presents the explicit form for denotational semantics of various constructs
for sequential programs, which extends [16, Lemma 4.6].

 I Lemma 24. For any cq-states hσ, ρi and ∆ in SV where V contains all quantum variables of the
 corresponding program,
(1) [[skip]](∆) = ∆, [[abort]](∆) = ⊥V ;
(2) [[x := e]](σ, ρ) = hσ[σ(e)/x], ρi;
                         P
(3) [[x :=$ g ]](σ, ρ) = d∈Dtype(x) hσ[d/x], g(d) · ρi;
(4) [[x := meas M[q̄]]](σ, ρ) = i∈I hσ[i/x], Mi ρMi† i where Mi ’s are applied on q̄, and M =
                                       P

    {Mi : i ∈ I};
                             Pdq −1
(5) [[q := 0]](σ, ρ) = hσ, i=0        |0iq hi|ρ|iiq h0|ii;
(6) [[q̄ ∗= U ]](σ, ρ) = hσ, Uq̄ ρUq̄† i.
(7) [[S0 ; S1 ]](∆) = [[S1 ]]([[S0 ]](∆));
                                      Pn
(8) [[if ni=1 Bi → Si fi]](∆) = i=1 [[Si ]](∆|Bi );
20    Verification of Distributed Quantum Programs


     (9) [[do ni=1 Bi → Si od]](∆) =              [[S k ]](∆), where S , do ni=1 Bi → Si od, S 0 , abort,
                                           W
                                               k
         and for any k ≥ 0,

              S k+1 , if ni=1 Bi → Si ; S k  B0 → skip fi.
                     Vn                                  Pn
           Here B0 , i=1 ¬Bi . Thus [[S ]](∆) = ∆|B0 + i=1 [[S ]]([[Si ]](∆|Bi )).

      Proof. Similar to that of [16, Lemma 4.6].                                                             J

       C      Omitted proofs
      Proof of Lemma 6. Induction on the structure of S.                                                     J

      Proof of Lemma 7. This can be easily seen from the fact that the only successor configuration of a
      terminal one under → is itself.                                                                 J

      C.1     Proof of Theorem 9
     To prove Theorem 9, we first introduce some notions. Note that from Table 1, any transition
     hS, σ, ρi → µ of a distributed program S must be obtained by using (Paral) or (Comm). To make it
                                                                                 k
      clear which processes are involved in the transition, we write hS, σ, ρi → µ if it is caused by a local
                                                            (k,`)
      action of process Sk . Similarly, we write hS, σ, ρi → µ if it is caused by a communication between
      processes Sk and S` with k < `. Let T , [n] ∪ {(k, `) ∈ [n]2 : k < `}, where [n] , {1, . . . , n}, be
      the set of possible transition labels.

      I Definition 25. Let π = {µi : i ≥ 0} be a computation of hS, σ, ρi. The (infinite) derivative tree
      T induced by π is defined as follows: for all i ≥ 0,
     (1) nodes at the i-th level of T are support configurations of µi . In particular, the root node of T is
         hS, σ, ρi;
                                                                                  A
     (2) for any i-th level node c (thus c ∈ dµi e) which is not a terminal, if c → ν, A ∈ T , is the transition
         from c which contributes to the evolvement from µi to µi+1 , then there is an edge in T from c
         to each support configuration of ν. Furthermore, these edges are labelled by action A and their
         corresponding probabilities in ν;
     (3) for any terminal configuration c at the i-th level, note that c also appears at the i + 1-th level.
         Then there is an edge in T from the i-th level c to the i + 1-th level c. Furthermore, this edge is
         labelled by a special symbol ∗ and probability 1.
      Note that from a derivative tree T , we can easily recover the computation {µi : i ≥ 0} as follows: for
      each i ≥ 0, let Ni be the set of nodes at the i-th level of T . Then
                X
         µi =        pc · c
                c∈Ni

     where pc is the product of all the probabilities along the path from the root to c.

      I Definition 26. Let π be a computation of hS, σ, ρi, and T its derivative tree.
     (1) A run r = {ci : i ≥ 0} of π is a path of T starting from the root node (thus c0 = hS, σ, ρi).
     (2) The history of a run r = {ci : i ≥ 0} is a sequence {(Ei , Ai ) ∈ 2T × (T ∪ {∗}) : i ≥ 0} such
         that Ei is the set of transition labels that are enabled in ci , while Ai is the label on the edge
         (ci , ci+1 ) in T . Note that Ai ∈ Ei whenever Ei 6= ∅.

         Fix arbitrarily a linear order v over T . For example, we may let A v B if (1) A ∈ [n] and
      B ∈ [n]2 , or (2) A < B when both A and B are in [n], or (3) i < j when A = (i, k) and B = (j, `).
 Y. Feng, S. Li, and M. Ying                                                                                        21


 I Definition 27. A run is good if its history {(Ei , Ai ) : i ≥ 0} satisfies the following condition:

     ∀i ≥ 0 : (Ei 6= ∅ → Ai = min Ei )

where min Ei is the minimum element in Ei according to the linear order v. A computation π is
good if all of its runs are good.
    We are now ready to prove the main theorem of this section, which says that all computations
 from a given input computes the same cq-state.

 Proof of Theorem 9. Note that from any configuration hS, σ, ρi, there exists a unique good com-
 putation. The main idea of the proof is that we can always transform the derivative tree T of any
 computation into that of the good one starting from the same configuration, using some ‘commut-
 ativity’ properties of transitions from different processes. Furthermore, this transformation does not
 change the computed cq-state.
                                                                          A
     Let π = {µi : i ≥ 0} be a computation with µ0 = hS, σ, ρi → µ1 , and T its derivative tree.
 Suppose the good computation from hS, σ, ρi would choose B, B 6= A, as the first action. We show
 in the following how to transform π into another (not necessarily good) computation π 0 with the first
 action being B, and they compute the same cq-state. To simplify the presentation, we assume B = k
 for some k ∈ [n] (the case when B ∈ [n]2 is similar).
     First, we prove that the B-transition must appear along every terminating run of π. To see this,
 suppose on the contrary there is a successful run r in which no B-transition is executed. Note that
 any transition which does not involve k cannot change the value of variables in cv(Sk ), and since
 Sk is deterministic, at most one of the actions in T which involve k is enabled at any moment.
 Consequently, B will be continuously enabled along r, which is a contradiction since the quantum
 program in the last configuration of r must be E.
     Now for any terminating run r = {ci : i ≥ 0} of π (thus c0 = hS, σ, ρi) with history {(Ei , Ai ) :
 i ≥ 0}, let ciB , hRiB , σiB , ρiB i be the first configuration in which B is executed; that is, AiB = B,
 and Ai 6= B for all i < iB . From transition rule (Paral) in Table 1 and Lemma 6, let
               B
                  X
     hS, σ, ρi →      pj · hRj , fj (σ), Ej (ρ)/pj i                                                   (3)
                   j∈J

where Rj = S1 k . . . kSk,j k . . . kSn for some Sk,j , fj only depends on cv(Sk ) but does not change
the variables outside change(Sk ), Ej is a super-operator acting on Hqv(Sk ) , and pj = tr(Ej (ρ)). Then
from the fact that along the path c0 , c1 , . . . , ciB , no action involving k is performed, the transition
that happens at ciB in the computation π has the form
                       B
                         X
    hRiB , σiB , ρiB i →     piB ,j · hRiB ,j , fj (σiB ), Ej (ρiB )/piB ,j i                            (4)
                             j∈J

 where RiB ,j = S1iB k . . . kSk,j k . . . kSniB whenever RiB = S1iB k . . . kSk k . . . kSniB , and piB ,j =
 tr(Ej (ρiB )).
     For any j ∈ J, we are going to construct from T a derivative tree Tj where the first execution of
 the B-transition along any terminating run of T is replaced by the corresponding j-th child in the
 B-transition; that is, ciB is replaced by hRiB ,j , fj (σiB ), Ej (ρiB )/piB ,j i. To be more specific, Tj is
 constructed as follows.
(1) Let the root of Tj be hRj , fj (σ), Ej (ρ)/pj i.
(2) To unfold Tj from the root, we follow precisely the transitions taken by T along each run r until
     the configuration ciB is reached. For such a finite path c0 , c1 , . . . , ciB in T , it is easy to see that
     the corresponding path in Tj is c00 , c01 , . . . , c0iB , where

         c0i , hS1i k . . . kSk,j k . . . kSni , fj (σi ), Ej (ρi )/tr(Ej (ρi ))i
22    Verification of Distributed Quantum Programs


         whenever

              ci = hS1i k . . . kSk k . . . kSni , σi , ρi i.

         Here in each ci the k-th process must be Sk since along the path c0 , c1 , . . . , ciB in T , no B-
         transition is executed. In particular, c0iB is precisely the j-th support configuration of the right-hand
         side distribution in Eq. (4). Furthermore, it is easy to check that each pair of the corresponding
         edges in T and Tj along each run up to the respective ciB are labelled with the same probability.
     (3) The subtree of Tj rooted at c0iB is the same as the subtree of T rooted at c0iB (from the above
         clause, c0iB indeed appears in T as a child node of ciB ).
         Finally, let T 0 be a derivative tree where the root is hS, σ, ρi, the action executed by the root is
     given in Eq. (3), and for each j ∈ J, Tj is the subtree starting from hRj , fj (σ), Ej (ρ)/pj i. Note also
     that the above procedure transforms non-terminating runs to non-terminating runs. Thus obviously,
     the induced computation π 0 = {µ0i : i ≥ 0} computes the same cq-state as π.
         Repeat the above procedure, we will eventually transform any computation to the good one
     without changing the cq-state computed. That concludes the proof of the theorem.                        J

      C.2     Proof of Lemma 11
      Clause (2) is easy. For (1), let ∆ = hσ, ρi with tr(ρ) = 1, and π , {µi : i ≥ 0} a computation of S
      starting in ∆. We prove by induction on i that ∆µi has countable support and tr(∆µi ) ≤ tr(ρ). Thus
      the result holds for simple cq-states. The general case follows easily.

      C.3     Proof of Theorem 12
     We first show a close relationship between the good transitions of S and the transitions of T (S).

      I Lemma 28. For any configuration hS, σ, ρi where S is a distributed quantum program,
                                         P
     (1) if the transition hS, σ, ρi →      i∈I p i · hSi , σi , ρi i appears in the derivative tree of a good
                                                P
         computation, then hT (S), σ, ρi →          i∈I pi · hT (Si ), σi , ρi i is the (unique) transition from
         hT (S), σ, ρi;
     (2) conversely, if hT (S), σ, ρi → i∈I pi · hSi0 , σi , ρi i then either hS, σ, ρi → i∈I pi · hSi , σi , ρi i
                                       P                                                    P

         appears in the derivative tree of a good computation and Si0 = T (Si ), or hS, σ, ρi is a deadlock.
         In the latter case, σ |= BLOCK ∧ ¬TERM .

     Proof. Easy from the definitions of T (S), which is a deterministic quantum program, and the good
     computation of S. Furthermore, if hS, σ, ρi is a deadlock, then the classical state σ must satisfy
     BLOCK ∧ ¬TERM .                                                                                 J

     With this lemma, Theorem 12 can be proved as follows.

     Proof of Theorem 12. We need only prove the theorem for the case when ∆ = hσ, ρi with
     tr(ρ) = 1. Let π , {µi : i ≥ 0} and π 0 , {µ0i : i ≥ 0} be the computation of T (S) and the good
     computation of S, both starting in hσ, ρi, respectively. We are going to show that for any i ≥ 0,
     ∆µi = ∆µ0i |TERM . Then the theorem follows by taking the least upper bounds of both sides.
         From Lemma 28, the derivative tree of π has the same structure (including the probability weights
     along the edges) with that of π 0 , except for deadlock configurations. However, Lemma 28 also says
     that classical states in these deadlock configurations must satisfy BLOCK ∧ ¬TERM , and thus
     they will be excluded in computing ∆µ0i |TERM . Note further that TERM is satisfied by all the
     successfully terminating configurations in µi ; that is, ∆µi = ∆µi |TERM . Thus ∆µi = ∆µ0i |TERM
     as desired.                                                                                        J
Y. Feng, S. Li, and M. Ying                                                                                     23



   xp.skip.Θ = Θ                               wlp.abort.Θ = >V                       wp.abort.Θ = ⊥V
                                                                          P
   xp.(x := e).Θ = Θ[e/x]                      xp.(x :=$ g).Θ =               d∈Dtype(x)
                                                                                           g(d) · Θ[d/x]
                                                                         Pdq −1
   xp.(q̄ ∗= U ).Θ = Uq̄† ΘUq̄                 xp.(q := 0).Θ =             i=0
                                                                                  |iiq h0|Θ|0iq hi|

                                                                                                 Mi† Θ[i/x]Mi
                                                                                      P
   xp.(S0 ; S1 ).Θ = xp.S0 .(xp.S1 .Θ)         xp.(x := meas M[q̄]).Θ =                    i∈I
                                               Pn                                Vn
           wlp.(if n
                    i=1 Bi → Si fi).Θ =              i=1
                                                           Bi ∧ wlp.Si .Θ +         i=1
                                                                                           ¬Bi
                                                           Pn
                   wp.(if n
                           i=1 Bi → Si fi).Θ =               i=1
                                                                   Bi ∧ wp.Si .Θ

   wlp.(do n
                                          V
            i=1 Bi → Si od).Θ =               k≥0
                                                    Θk , where Θ0 , >V , and for any k ≥ 0,
                             Pn                                 Vn
                   Θk+1 ,        i=1
                                       Bi ∧ wlp.Si .Θk +           i=1
                                                                         ¬Bi ∧ Θ.

    wp.(do n
                                         W
            i=1 Bi → Si od).Θ =              k≥0
                                                    Θk , where Θ0 , ⊥V , and for any k ≥ 0,
                             Pn                                 Vn
                    Θk+1 ,       i=1
                                       Bi ∧ wp.Si .Θk +            i=1
                                                                         ¬Bi ∧ Θ.

  Table 4 Weakest (liberal) precondition semantics for sequential programs, where xp ∈ {wp, wlp} and
V = qv(Θ).



C.4    Proof of Theorems 18 and 20
The basic idea of proving the soundness and completeness of our proof systems is to employ weakest
(liberal) preconditions. To this end, we extend the weakest (liberal) precondition semantics presented
in [16] to sequential programs defined in Sec. 2.1. Note that we do not have to extend it further
to distributed programs, thanks to the sequentialisation theorem (Theorem 12). Let A⊇qv(S) ,
S
   V ⊇qv(S) AV .

I Definition 29. Let S be a sequential quantum program. The weakest precondition semantics
wp.S and weakest liberal precondition semantics wlp.S of S are both mappings

                                          A⊇qv(S) → A⊇qv(S)

defined inductively in Table 4. To simplify notation, we use xp to denote both wp and wlp whenever
it is applicable for both of them.

    The following lemma shows a duality relation between the denotational and weakest (liberal)
precondition semantics of sequential programs, which extends [16, Lemma 4.14].

 I Lemma 30. Let S be a sequential quantum program, ∆ a cq-state, and Θ a cq-assertion with
 qv(∆) ⊇ qv(Θ) ⊇ qv(S). Then
(1) qv(wp.S.Θ) = qv(wlp.S.Θ) = qv(Θ);
(2) Exp(∆ |= wp.S.Θ) = Exp([[S ]](∆) |= Θ);
(3) Exp(∆ |= wlp.S.Θ) = Exp([[S ]](∆) |= Θ) + tr(∆) − tr([[S ]](∆)).

Proof. We prove this lemma by induction on the structure of S. The basis cases are easy from the
definition. We only show the following cases for clause (3) as examples. Let V , qv(Θ).
24   Verification of Distributed Quantum Programs


        Let S , if ni=1 Bi → Si fi. Note that Bi ’s are mutually exclusive. Then
                                                 n                      n
                                                                               !
                                                X                      ^
            Exp(∆ |= wlp.S.Θ) = Exp ∆ |=             Bi ∧ wlp.Si .Θ +     ¬Bi
                                                        i=1                    i=1
                                         n                                                      n
                                                                                                           !
                                         X                                                      X
                                     =         Exp(∆|Bi |= wlp.Si .Θ) + Exp ∆ |= >V −                 Bi
                                         i=1                                                    i=1
                                         Xn
                                     =         [Exp ([[Si ]](∆|Bi ) |= Θ) + tr(∆|Bi ) − tr([[Si ]](∆|Bi ))]
                                         i=1
                                                          n
                                                          X
                                           + tr(∆) −            tr(∆|Bi )
                                                          i=1

                                     = Exp([[S ]](∆) |= Θ) + tr(∆) − tr([[S ]](∆)).

        Here the second equality follows from Lemma 21, the third one from the inductive hypothesis,
        and the last one from Lemma 24.
        Let S , do ni=1 Bi → Si od and Θk , k ≥ 0, be defined as in Table 4 for the wlp semantics of
        do ni=1 Bi → Si od. First, we show by induction that for any k ≥ 0 and ∆0 ∈ SV ,

            Exp(∆0 |= Θk ) = Exp([[S k ]](∆0 ) |= Θ) + tr(∆0 ) − tr([[S k ]](∆0 ))                             (5)

        where S k is defined as in Lemma 24. The case of k = 0 follows from the definition. Let
            Vn
        B , i=1 ¬Bi . We further calculate from Lemmas 21 and 24 that

            Exp(∆0 |= Θk+1 )
                        Xn
            = Exp(∆0 |=      Bi ∧ wlp.Si .Θk ) + Exp(∆0 |= B ∧ Θ)
                               i=1
                n
                X
            =         Exp(∆0 |Bi |= wlp.Si .Θk ) + Exp(∆0 |B |= Θ)
                i=1
                n
                X
            =         [Exp ([[Si ]](∆0 |Bi ) |= Θk ) + tr(∆0 |Bi ) − tr([[Si ]](∆0 |Bi ))] + Exp(∆0 |B |= Θ)
                i=1
              n
              X
                 Exp([[S k ]]([[Si ]](∆0 |Bi )) |= Θ) + tr([[Si ]](∆0 |Bi )) − tr([[S k ]]([[Si ]](∆0 |Bi )))
                                                                                                            
            =
                i=1
                      n
                      X
                  +         [tr(∆0 |Bi ) − tr([[Si ]](∆0 |Bi ))] + Exp(∆0 |B |= Θ)
                      i=1

            = Exp([[S k+1 ]](∆0 ) |= Θ) + tr(∆0 ) − tr([[S k+1 ]](∆0 )),

        where the fourth equality follows from the induction hypothesis, and the last one from the fact that
        [[S k+1 ]](∆0 ) = ni=1 [[S k ]]([[Si ]](∆0 |Bi )) + ∆0 |B and tr(∆0 ) = ni=1 tr(∆0 |Bi ) + tr(∆0 |B ).
                         P                                                     P

        With Eq. (5), we have from Lemma 23 that
                                                 ^
          Exp(∆ |= wlp.S.Θ) = Exp(∆ |=                Θk ) = Exp([[S ]](∆) |= Θ) + tr(∆) − tr([[S ]](∆)).
                                                    k≥0

                                                                                                                 J

        The following two lemmas, which extend Lemmas 4.16 and 4.17 in [16], respectively, can be
     similarly shown for our sequential programs. The proofs are omitted here.
Y. Feng, S. Li, and M. Ying                                                                        25


 I Lemma 31. Let S be a sequential program, ∆ a cq-state, and Θ a cq-assertion with qv(∆) ⊇
 qv(Θ) ⊇ qv(S). Let xp ∈ {wp, wlp}. Then
(1) wp.S.Θ + wlp.S.(>qv(Θ) − Θ) = >qv(Θ) ;
(2) the function xp.S is monotonic; that is, for all Θ1 v Θ2 , xp.S.Θ1 v xp.S.Θ2 ;
(3) the function wp.S is linear; that is, for all Θ1 , Θ2 ∈ AV ,

          wp.S.(λ1 Θ1 + λ2 Θ2 ) = λ1 wp.S.Θ1 + λ2 wp.S.Θ2 ;

(4) the function wlp.S is affine-linear; that is, for all Θ1 , Θ2 ∈ AV and λ1 + λ2 = 1,

          wlp.S.(λ1 Θ1 + λ2 Θ2 ) = λ1 wlp.S.Θ1 + λ2 wlp.S.Θ2 .

(5) if W ∩ qv(Θ) ⊆ V ⊆ qv(Θ), (V ∪ W ) ∩ qv(S) = ∅, and FV →W is a completely positive and
    sub-unital super-operator, then

                                 FV →W (wp.S.Θ) = wp.S.(FV →W (Θ))

    and
                                 FV →W (wlp.S.Θ) v wlp.S.(FV →W (Θ)).
    The equality holds for wlp as well if FV →W is unital;

I Lemma 32. Let S be a sequential program, and Θ and Ψ are cq-assertions. Then

     |=tot {Θ} S {Ψ}       iff   Θ . wp.S.(Ψ ⊗ Iqv(S)\qv(Ψ) )
    |=par {Θ} S {Ψ}        iff   Θ . wlp.S.(Ψ ⊗ Iqv(S)\qv(Ψ) ).

In particular, if qv(Θ) = qv(Ψ) ⊇ qv(S), then

     |=tot {Θ} S {Ψ}       iff   Θ v wp.S.Ψ
    |=par {Θ} S {Ψ}        iff   Θ v wlp.S.Ψ.

   The next lemma shows a closed relationship between the correctness of a distributed quantum
program S and its sequentialisation T (S).

I Lemma 33. For any distributed program S and a cq-assertions Θ and Ψ,

     |=tot {Θ} S {Ψ ∧ TERM } iff         |=tot {Θ} T (S) {Ψ ∧ TERM }
    |=par {Θ} S {Ψ ∧ TERM } iff          |=par {Θ} T (S) {Ψ ∧ TERM + ¬TERM ∧ BLOCK } .

Proof. The first equivalence is direct from Theorem 12. For the second one, let Ψ0 , Ψ ∧ TERM +
¬TERM ∧ BLOCK . It suffices to prove for any ∆ ∈ SV with V ⊇ qv(Ψ, Θ, S),

   Exp([[T (S)]](∆) |= Ψ0 ) − tr([[T (S)]](∆)) = Exp([[S ]](∆) |= Ψ ∧ TERM ) − tr([[S ]](∆)) (6)

Note that all support configurations in [[T (S)]](∆) satisfy BLOCK . Thus

    [[T (S)]](∆) = [[S ]](∆) + [[T (S)]](∆)|¬TERM∧BLOCK

from Theorem 12, and

    tr([[T (S)]](∆)) = tr([[S ]](∆)) + Exp ([[T (S)]](∆) |= ¬TERM ∧ BLOCK ) .

Then Eq. (6) follows easily from the first equivalence.                                       J
26   Verification of Distributed Quantum Programs


         We are now ready to prove the soundness and completeness of our proof systems.

      Proof of Theorem 18. Soundness: We need only to show that each rule in Table 2 is valid in the
      sense of partial correctness. The proof is divided into two steps:
     (1) We first prove by structural induction that the proof rules are sound for sequential programs
         (thus the rule (Dist) is no applicable). We take (Rep) as an example; the others are simpler. Let
         S , do ni=1 Bi → Si od, and |=par {Bi ∧ Θ} Si {Θ} for all 1 ≤ i ≤ n. Without loss of
         generality, we assume qv(S) ⊆ qv(Θ). Then Bi ∧ Θ v wlp.Si .Θ from Lemma 32. We now
         prove by induction on k that Θ v Θk for any k ≥ 0, where Θk is defined as in Table 4 for the
                                                                          Vn
         wlp semantics of do ni=1 Bi → Si od when the postcondition is i=1 ¬Bi ∧ Θ. The case when
         k = 0 is trivial. Then we calculate
                         n
                         X                             n
                                                       ^
             Θk+1 =            Bi ∧ wlp.Si .Θk +            ¬Bi ∧ Θ
                         i=1                          i=1
                         Xn                           n
                                                      ^
                    w          Bi ∧ wlp.Si .Θ +             ¬Bi ∧ Θ
                         i=1                          i=1
                         Xn               n
                                          ^
                    w          Bi ∧ Θ +         ¬Bi ∧ Θ = Θ,
                         i=1              i=1

         where the first inequality follows from the induction hypothesis and Lemma 31. Thus
                                                   n
                                                               !
                                                   ^
                              n
            Θ v wlp.(do i=1 Bi → Si od).              ¬Bi ∧ Θ ,
                                                             i=1

         and so
                                                        ( n                  )
                                                         ^
             |=par {Θ} do ni=1 Bi → Si od                         ¬Bi ∧ Θ
                                                             i=1

         by Lemma 32.
     (2) For generic distributed program, the only relevant rules are (Imp) and (Dist). The former is direct
         from Lemma 32. For (Dist), let S , S1 k . . . kSn and T (S) be its sequentialisation defined in
         Sec. 4. Suppose |=par {Θ} S1,0 ; . . . ; Sn,0 {Ψ}, and for all (i, j, k, `) ∈ Γ,

             |=par {Bi,j ∧ Bk,` ∧ Ψ} Effect(αi,j , αk,` ); Si,j ; Sk,` {Ψ} .

         Note that T (S) is sequential. First, by the soundness of (Imp) for sequential programs, we have

             |=par {Bi,j ∧ Bk,` ∧ Bi ∧ Ψ} Effect(αi,j , αk,` ); Si,j ; Sk,` {Ψ} .

         Then |=par {Θ} T (S) {Ψ ∧ BLOCK } by using the soundness of (Seq) and (Rep) for sequential
         programs. Note that Ψ ∧ BLOCK v Ψ0 where Ψ0 is defined in Lemma 33. Thus from (Imp) and
         Lemma 33 we have |=par {Θ} S {Ψ ∧ TERM }.
         Completeness: The proof for completeness is also divided into two steps:
     (1) We first prove by induction on the structure of S that for any Θ and sequential program S with
         qv(S) ⊆ qv(Θ), `par {wlp.S.Θ} S {Θ} . We take the case for loops as an example. Let
         S , do ni=1 Bi → Si od and Ψ , wlp.S.Θ. By induction, we have `par {wlp.Si .Ψ} Si {Ψ}
         for any 1 ≤ i ≤ n. Note that
                   n
                   X                            n
                                                ^
             Ψ=          Bi ∧ wlp.Si .Ψ +             ¬Bi ∧ Θ.
                   i=1                          i=1
Y. Feng, S. Li, and M. Ying                                                                              27


    Thus Bi ∧ Ψ = Bi ∧ wlp.Si .Ψ v wlp.Si .Ψ and so `par {Bi ∧ Ψ} Si {Ψ} by the (Imp) rule.
                                                                         Vn
    Now using (Rep) we have `par {Ψ} do ni=1 Bi → Si od { i=1 ¬Bi ∧ Ψ} and the result
                                Vn                  Vn
    follows from the fact that i=1 ¬Bi ∧ Ψ = i=1 ¬Bi ∧ Θ v Θ.
(2) Let S , S1 k . . . kSn and T (S) its sequentialisation defined in Sec. 4. Suppose |=par {Θ} S {Ψ}.
    Note that for any ∆ ∈ SV with V ⊇ qv(Ψ, Θ, S), all support configurations in [[S ]](∆)
    satisfy TERM . Thus |=par {Θ} S {Ψ ∧ TERM }. Then from Lemma 33, we have |=par
    {Θ} T (S) {Θ0 } where Θ0 , Ψ ∧ TERM + ¬TERM ∧ BLOCK , and thus Θ . wlp.T (S).Θ0 .
    Let Ψ0 , wlp.do.Θ0 where do is the do-loop in T (S). As T (S) is sequential, we have from the
    above clause that

        `par {Ψ0 } do {Θ0 }          and         `par {wlp.S0 .Ψ0 } S0 {Ψ0 }

    where S0 , S1,0 ; . . . ; Sn,0 . Note that
               X                                 k,`
       Ψ0 =              Bi,j ∧ Bk,` ∧ Bi ∧ wlp.Si,j .Ψ0 + BLOCK ∧ Θ0
              (i,j,k,`)∈Γ

           k,`
    where Si,j , Effect(αi,j , αk,` ); Si,j ; Sk,` . Thus
                                                   k,`            k,`
        Bi,j ∧ Bk,` ∧ Ψ0 = Bi,j ∧ Bk,` ∧ Bi ∧ wlp.Si,j .Ψ0 v wlp.Si,j .Ψ0 ,

    and so
                                  k,`
        `par {Bi,j ∧ Bk,` ∧ Ψ0 } Si,j {Ψ0 } .

    by (Imp) and the completeness result for sequential quantum programs. Note that wlp.S0 .Ψ0 =
    wlp.T (S).Θ0 . Applying (Dist) and (Imp), we derive `par {Θ} S {Ψ0 ∧ TERM }, and the result
    follows from the fact that Ψ0 ∧ TERM = Θ0 ∧ TERM = Ψ ∧ TERM v Ψ.
                                                                                               J

    The proof for total correctness is more involved.

 Proof of Theorem 20. Soundness: Similar to the partial correctness case, the proof is divided
 into two steps:
(1) We first prove by structural induction that the proof rules in Table 2 with the corresponding
     rules replaced by those in Table 3 are sound for sequential programs (thus the rule (Dist-T) is
     no applicable), in the sense of total correctness. Again, we take (Rep-T) as an example. Let
     S , do ni=1 Bi → Si od, |=tot {Bi ∧ Θ} Si {Θ} for all 1 ≤ i ≤ n, and {Ψk : k ≥ 0} be a
     sequence of Θ-ranking assertions for S. Without loss of generality, we assume qv(S) ⊆ qv(Θ).
     We now prove by induction on k that Θ v Θk + Ψk for any k ≥ 0, where Θk is defined as in
                                                                                    Vn
     Table 4 for the wp semantics of do ni=1 Bi → Si od when the postcondition is i=1 ¬Bi ∧ Θ.
     The case when k = 0 is from the fact that Θ v Ψ0 . Then from the inductive hypothesis and
     Lemmas 31 and 32,

        Bi ∧ Θ v wp.Si .Θ v wp.Si .Θk + wp.Si .Ψk ,

    and so
                            n
                            X                         n
                                                      ^                 n
                                                                        X
        Θk+1 + Ψk+1 w             Bi ∧ wp.Si .Θk +          ¬Bi ∧ Θ +         Bi ∧ wp.Si .Ψk
                            i=1                       i=1               i=1
                            Xn               n
                                             ^
                        w         Bi ∧ Θ +         ¬Bi ∧ Θ = Θ,
                            i=1              i=1
28   Verification of Distributed Quantum Programs


         where the first inequality follows from the definition of ranking assertions and the fact that Bi ’s
         are mutually exclusive, and the second one from the induction hypothesis. Thus
                                                   n
                                                               !
                                                  ^
             Θ v wp.(do ni=1 Bi → Si od).           ¬Bi ∧ Θ
                                                        i=1
                          V
         by noting that       k Ψk = ⊥V , and so
                                                      ( n               )
                                                       ^
             |=tot {Θ} do ni=1 Bi → Si od                    ¬Bi ∧ Θ
                                                        i=1

         as desired.
     (2) For generic distributed programs, again we only consider (Dist). The proof is similar to the case
         for partial correctness, by noting the following two facts: for any distributed program S and
         cq-assertion Ψ,
            ranking assertions for S are also ranking assertions for the do-loop of T (S);
            from the assumption Ψ ∧ BLOCK . TERM we have Ψ ∧ BLOCK = Ψ ∧ TERM .
         Completeness: The proof for completeness is also divided into two steps:
     (1) We first prove by induction on the structure of S that for any Θ and sequential program S with
         qv(S) ⊆ qv(Θ), `tot {wp.S.Θ} S {Θ} . Again, we take the case for loops as an example. Let
         S , do ni=1 Bi → Si od and Ψ , wp.S.Θ. By induction, we have `tot {wp.Si .Ψ} Si {Ψ}
         for any 1 ≤ i ≤ n. Note that
                  n
                  X                            n
                                               ^
             Ψ=         Bi ∧ wp.Si .Ψ +             ¬Bi ∧ Θ.
                  i=1                         i=1

         Thus Bi ∧ Ψ = Bi ∧ wp.Si .Ψ v wp.Si .Ψ and so `tot {Bi ∧ Ψ} Si {Ψ} by the (Imp) rule.
                                               Pn
         Let Θ0 , wp.S.>qv(Θ) and Θk+1 , i=1 Bi ∧ wp.Si .Θk . We are going to show that {Θk :
         k ≥ 0} are Ψ-ranking assertions for S. First, note that
                          n
                          X                            n
                                                       ^                           n
                                                                                   X
                  Θ1 =          Bi ∧ wp.Si .Θ0 v             ¬Bi ∧ >qv(Θ) +              Bi ∧ wp.Si .Θ0 = Θ0 .
                          i=1                          i=1                         i=1

         So {Θk : k ≥ 0} is decreasing by easy induction, using Lemma 31(2). Next, as Θ v >qv(Θ) , we
         have Ψ v Θ0 .
                               V
         Finally, we prove that k Θk = ⊥qv(Θ) . We show by induction on k that for any k ≥ 0 and
         ∆ ∈ Sqv(Θ,S) ,
             Exp(∆ |= Θk ) = tr([[S ]](∆)) − tr([[S k ]](∆)).                                                    (7)
         The case when k = 0 is direct from Lemmas 21 and 30. We further calculate that
                                              n
                                                               !
                                             X
            Exp(∆ |= Θk+1 ) = Exp ∆ |=          Bi ∧ wp.Si .Θk
                                                      i=1
                                       n
                                       X
                                   =         Exp(∆|Bi |= wp.Si .Θk )
                                       i=1
                                       Xn
                                   =         Exp([[Si ]](∆|Bi ) |= Θk )
                                       i=1
                                       Xn                                   n
                                                                            X
                                   =         tr([[S ]]([[Si ]](∆|Bi ))) −         tr([[S k ]]([[Si ]](∆|Bi )))
                                       i=1                                  i=1

                                   = tr([[S ]](∆)) − tr([[S k+1 ]](∆)).
Y. Feng, S. Li, and M. Ying                                                                                                              29



                           {Bi ∧ Θ} Si {Θ} , {Bi ∧ p ∧ t = z} Si {t < z} , ∀i ∈ {1, . . . , n}, p → t ≥ 0
   (C-Rep-T)                                                             Vn
                                         {Θ} do n  i=1 Bi → Si od    Θ ∧ i=1 ¬Bi

                                                                                       L                              W
                    where type(z) = type(t) = Integer, z 6∈ cv(p, Bi , t, Si ), Θ =        i∈I
                                                                                                 hpi , Mi i and p ,       i∈I
                                                                                                                                pi .

                           {Θ} S1,0 ; . . . ; Sn,0 {Ψ} , p → t ≥ 0, p ∧ BLOCK → TERM
                           {Bi,j ∧ Bk,` ∧ p ∧ t = z} Effect(αi,j , αk,` ); Si,j ; Sk,` {t < z} , ∀(i, j, k, `) ∈ Γ
                           {Bi,j ∧ Bk,` ∧ Ψ} Effect(αi,j , αk,` ); Si,j ; Sk,` {Ψ} , ∀(i, j, k, `) ∈ Γ
   (C-Dist-T)
                                                    {Θ} S1 k . . . kSn {Ψ ∧ TERM }

                     where Γ, TERM , and BLOCK are defined as in Sec. 4,
                                                                                        L                              W
                     type(z) = type(t) = Integer, z 6∈ cv(p, t, S1 k . . . kSn ), Ψ =      i∈I
                                                                                                 hpi , Mi i, and p ,       i∈I
                                                                                                                                  pi .


      Table 5 Auxiliary rules.



    Here the second last equality is from induction hypothesis, and the last one from Lemma 24. Note
    that the second term of the r.h.s of Eq.(7) converges to the first one when k goes to infinity. Thus
                                       V
    limk Exp(∆ |= Θk ) = 0, and so k Θk = ⊥qv(Θ) from the arbitrariness of ∆.
                                                                         Vn
    Now using (Rep-T) we have `tot {Ψ} do ni=1 Bi → Si od { i=1 ¬Bi ∧ Ψ} and the result
                               Vn                 Vn
    follows from the fact that i=1 ¬Bi ∧ Ψ = i=1 ¬Bi ∧ Θ v Θ.
(2) The case for generic distributed programs S is similar to that for partial correctness. The
    construction of ranking assertions for the do-loop of T (S), which also work for S, follows the
    same approach in the above clause.
                                                                                                      J


  D       Auxiliary Rules
We have provided sound and relatively complete proof systems for both partial and total correctness of
distributed quantum programs. Thus in principle, these proof rules are sufficient for proving desired
properties as long as they can be described faithfully with Hoare triple formulas. However, in practice,
using these rules directly might be complicated. To simplify reasoning, we introduce two auxiliary
proof rules in Table 5 for the special case when a classical ranking function can be found to guarantee
the (finite) termination of repetitive sequential (C-Rep-T) or distributed (C-Dist-T) quantum programs.
More auxiliary proof rules (for deterministic quantum programs) can be found in [16, 41]. For the
sake of convenience, we write hp, |ψii for hp, |ψihψ|i, and p for p ∧ >V for some appropriate V .

I Theorem 34. The auxiliary rules presented in Table 5 are sound with respect to total correctness.

Proof. First note that for any i, |=tot {Bi ∧ p ∧ t = z} Si {t < z} implies for any σ |= Bi ∧p∧t =
z and ρ, and any σ 0 in the support of [[Si ]](σ, ρ), we have σ 0 |= t < z. Then an argument similar to that
for classical programs leads to the conclusion that all computations from hdo ni=1 Bi → Si od, σ, ρi
terminates within σ(t) steps, provided σ |= p. That proves (C-Rep-T). The case for (C-Dist-T) is
similar.                                                                                                  J

  E       Case studies
To illustrate the effectiveness of the proof systems as well as the auxiliary rules presented in this
paper, we employ them to verify the quantum teleportation protocol. A protocol to locally implement
30   Verification of Distributed Quantum Programs


     nonlocal gates is also investigated.

     E.1     Verification of quantum teleportation
     I Example 35 (Correctness of Quantum Teleportation). The correctness of quantum teleporta-
     tion can be stated as follows: for any |ψi ∈ H2 ,

         `tot {|ψiq ⊗ |βiq1 ,q2 } Teleport {|ψiq2 }                                                    (8)

         The main technique of proving Eq. (8) is to employ rule (C-Dist-T). Let t , 2 − stageA and
              1 X
         Ψ,             stageA = stageB = 0 ∧ xA = i ∧ zA = j, |j, iiq,q1 ⊗ X i Z j |ψiq2
              4 i,j=0,1

                        + stageA = stageB = 1 ∧ xA = i ∧ zA = j, |j, iiq,q1 ⊗ Z j |ψiq2
                        + hstageA = stageB = 2 ∧ xA = i ∧ zA = j, |j, iiq,q1 ⊗ |ψiq2 i) .

      The proof consists of three parts.
     (1) We show that Ψ is a global invariant for the distributed programs Teleport. To this end, consider
         the first branch of the do-loop in T (Telepor) presented in Example 13:

             {stageA = stageB = 0 ∧ Ψ}
                                                                    
             1 X                                                    
                         xA = i ∧ zA = j, |j, iiq,q1 ⊗ X i Z j |ψiq2                                  (Imp)
             4                                                      
                 i,j=0,1

             xB := xA ;
                                                                                     
             1 X                                                                     
                               xA = i ∧ zA = j ∧ xB = k, |j, iiq,q1 ⊗ X k Z j |ψiq2                   (Assn)
             4                                                                       
                   i,j,k=0,1

             stageA := 1;
                                                                                           
             1 X                                                                           
                          stageA = 1 ∧ xA = i ∧ zA = j ∧ xB = k, |j, iiq,q1 ⊗ X k Z j |ψiq2           (Assn)
             4                                                                             
                   i,j,k=0,1

             stageB := 1;
                                       
             X                         
                    (xB = k) ∧ Xqk2 (Ψ)                                                               (Assn)
                                       
                k=0,1

             if xB = 1 → q2 ∗= X  ¬(xB = 1) → skip fi
             {Ψ}                                                                                       (Alt)

         where X is the Pauli-X super-operator. Similarly, for the second branch, we can prove that

             {stageA = stageB = 1 ∧ Ψ}
             zB := zA ; stageA := 2; stageB := 2; if zB = 1 → q2 ∗= Z  ¬(zB = 1) → skip fi
             {Ψ} .

     (2) We show that t is a classical ranking function for the distributed program Teleport. Note that
                   V
         BLOCK ≡ k=0,1 ¬ (stageA = stageB = k),
                                         ^                       ^
                           TERM ≡            ¬ (stageA = k) ∧         ¬ (stageB = k)
                                           k=0,1                   k=0,1
Y. Feng, S. Li, and M. Ying                                                                               31

                                      W2
    and the classical part of Ψ is p , k=0 (stageA = stageB = k). Then it is easy to check that
    p → t ≥ 0 and p ∧ BLOCK → TERM . Furthermore, from

         {stageA = stageB = 0 ∧ p ∧ 2 − stageA = z}
         {1 < z}                                                                           (Imp)
        xB := xA ;
         {1 < z}                                                                          (Assn)
        stageA := 1;
         {2 − stageA < z}                                                                 (Assn)
        stageB := 1; if xB = 1 → q2 ∗= X  ¬(xB = 1) → skip fi
         {2 − stageA < z}                                                            (Assn, Alt)

    and similarly for the second branch of the do-loop, the integer expression t is indeed a classical
    ranking function for Teleport.
(3) We show that the sequential part of T (Teleport) establishes Ψ from the precondition |ψiq ⊗
    |βiq1 ,q2 . Let |ψi = x|0i + y|1i for some x, y ∈ C. Then

         {|ψiq ⊗ |βiq1 ,q2 }
        q, q1 ∗= CNOT;
                                                                     
            1
           √ (x|0iq (|00i + 11i)q1 ,q2 + y|1iq (|10i + 01i)q1 ,q2 )                              (Unit)
              2
        q ∗= H;
                                                                                    
           1
              (x(|0i + |1i)q (|00i + 11i)q1 ,q2 + y(|0i − |1i)q (|10i + 01i)q1 ,q2 )             (Unit)
           2
                                                                                            
         X 1                                     1   X                                      
                     |j, iiq,q1 ⊗ X i Z j |ψiq2 ≡           true, |j, iiq,q1 ⊗ X i Z j |ψiq2      (Imp)
        
           i,j=0,1
                   2                              4 i,j=0,1                                  

        zA := meas q; xA := meas q1 ;
                                                               
        1 X                                                    
                    xA = i ∧ zA = j, |j, iiq,q1 ⊗ X i Z j |ψiq2                                  (Meas)
        4                                                      
            i,j=0,1

        stageA := 0; stageB := 0;
        {Ψ}                                                                                      (Assn)

    With the three parts shown above, we have from (C-Dist-T) that

    `tot {|ψiq ⊗ |βiq1 ,q2 } Teleport {Ψ ∧ TERM } .

Then the desired result in Eq. (8) is obtained by noting that
                    1 X
   Ψ ∧ TERM ≡                 hstageA = stageB = 2 ∧ xA = i ∧ zA = j, |j, iiq,q1 ⊗ |ψiq2 i ,
                    4 i,j=0,1

which is upper bounded above by |ψiq2 according to the order ..

E.2     Local implementation of nonlocal quantum gates
In distributed quantum computing, one of the key tasks is to implement quantum gates between qubits
that are located in different quantum computers. To illustrate the basic idea, we recall the protocol
32   Verification of Distributed Quantum Programs


                   |ψi                                                            Z
                                                            x


                  |βi
                                                            z
                                           H

                   |φi                                                X

          Figure 2 Local implementation of remote CNOT gate. The wires from top to bottom represent qubits q, q1 ,
     q2 , and r respectively. Furthermore, q and q1 belong to Alice while q2 and r belong to Bob.


     proposed in [12] which implements a nonlocal CNOT gate between two parties, say Alice and Bob,
     by employing only local quantum operations and classical communication, again with the help of a
     pre-shared entangled state. The protocol is depicted as in Fig. 2 and can be written as a distributed
     program RCNOT , Alice k Bob where Alice ,

         q, q1 ∗= CNOT; xA := meas q1 ; stageA := 0;
         do stageA = 0; c!xA → stageA := 1
           stageA = 1; d?zA → stageA := 2; if zA = 1 → q ∗= Z  ¬(zA = 1) → skip fi
         od

     and Bob ,

         q2 , r ∗= CNOT; q2 ∗= H; zB := meas q2 ; stageB := 0;
         do stageB = 0; c?xB → stageB := 1; if xB = 1 → r ∗= X  ¬(xB = 1) → skip fi
           stageB = 1; d!zB → stageB := 2
         od

     The correctness of RCNOT is stated as follows: for any αij ∈ C with i,j=0,1 |αij |2 = 1,
                                                                            P

                                                                                 
              X                                         X                        
        `tot          αij |i, jiq,r ⊗ |βiq1 ,q2 RCNOT             αij |i, j ⊕ iiq,r                           (9)
                                                                                 
                i,j=0,1                                          i,j=0,1

      where ⊕ denotes the addition modulo 2. Again, the fact that the postcondition does not refer to q1
      and q2 means that the post-measurement state of these quantum systems is irrelevant.
         Similar to that of Teleport, to prove the correctness of RCNOT it suffices to show:
     (1) the cq-assertion
                   1 X
             Ψ,                stageA = stageB = 0 ∧ xA = i ∧ zB = j, |i, jiq1 ,q2 ⊗ Xri Zqj |ϕiq,r
                   4 i,j=0,1

                          + stageA = stageB = 1 ∧ xA = i ∧ zB = j, |i, jiq1 ,q2 ⊗ Zqj |ϕiq,r
                         + hstageA = stageB = 2 ∧ xA = i ∧ zB = j, |i, jiq1 ,q2 ⊗ |ϕiq,r i) .
                      P
         where |ϕi , k,`=0,1 αk` |k, `i, serves as a global invariant for RCNOT ;
     (2) the expression t , 2 − stageA is a classical ranking function; and
     (3) the sequential part of RCNOT establishes Ψ from the precondition |ϕiq,r ⊗ |βiq1 ,q2 .
      We omit the details here.
