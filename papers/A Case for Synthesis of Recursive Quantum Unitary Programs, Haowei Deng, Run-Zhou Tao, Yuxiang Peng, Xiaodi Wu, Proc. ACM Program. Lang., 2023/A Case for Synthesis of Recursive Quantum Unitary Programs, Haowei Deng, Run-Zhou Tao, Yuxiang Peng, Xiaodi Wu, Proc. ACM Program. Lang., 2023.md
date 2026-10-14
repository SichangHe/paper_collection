                                           A Case for Synthesis of Recursive Quantum Unitary Programs
                                           HAOWEI DENG∗ , University of Maryland, College Park, USA
                                           RUNZHOU TAO∗ , Columbia University, USA
arXiv:2311.11503v2 [quant-ph] 5 Dec 2023




                                           YUXIANG PENG, University of Maryland, College Park, USA
                                           XIAODI WU, University of Maryland, College Park, USA
                                           Quantum programs are notoriously difficult to code and verify due to unintuitive quantum knowledge
                                           associated with quantum programming. Automated tools relieving the tedium and errors associated with
                                           low-level quantum details would hence be highly desirable. In this paper, we initiate the study of program
                                           synthesis for quantum unitary programs that recursively define a family of unitary circuits for different input
                                           sizes, which are widely used in existing quantum programming languages. Specifically, we present QSynth,
                                           the first quantum program synthesis framework, including a new inductive quantum programming language,
                                           its specification, a sound logic for reasoning, and an encoding of the reasoning procedure into SMT instances.
                                           By leveraging existing SMT solvers, QSynth successfully synthesizes 10 quantum unitary programs including
                                           quantum arithmetic programs, quantum eigenvalue inversion, quantum teleportation and Quantum Fourier
                                           Transformation, which can be readily transpiled to executable programs on major quantum platforms, e.g.,
                                           Q#, IBM Qiskit, and AWS Braket.
                                           CCS Concepts: • Software and its engineering → Domain specific languages; Domain specific lan-
                                           guages; • Hardware → Quantum computation.
                                           Additional Key Words and Phrases: Quantum Programs, Program Synthesis, SMT solvers
                                           ACM Reference Format:
                                           Haowei Deng, Runzhou Tao, Yuxiang Peng, and Xiaodi Wu. 2024. A Case for Synthesis of Recursive Quantum
                                           Unitary Programs. Proc. ACM Program. Lang. 8, POPL, Article 59 (January 2024), 33 pages. https://doi.org/10.
                                           1145/3632901

                                           1   INTRODUCTION
                                           Quantum programming is a key step in enabling the various application of quantum computing
                                           such as factorization, simulation of physics and optimization. However, programming quantum
                                           computers is hard due to unintuitive quantum mechanics. To help ease the programming of quantum
                                           computers, circuit synthesis techniques have been proposed to automatically generate quantum
                                           circuits [Amy et al. 2013; de Brugiere 2020; Kang and Oh 2023; Kitaev 1997; Saeedi et al. 2011;
                                           Shende et al. 2006; Younis et al. 2021].
                                              Unfortunately, these synthesis frameworks underperform when the number of qubits of the
                                           quantum circuit to synthesize is as large as 5. For example, QFAST [Younis et al. 2021], a recent
                                           quantum circuit synthesis framework, can only synthesize QFT and adder circuit up to 5 qubits. And
                                           ∗ Both authors contributed equally to the paper.


                                           Authors’ addresses: Haowei Deng, University of Maryland, College Park, College Park, MD, USA, hwdeng@umd.edu;
                                           Runzhou Tao, Columbia University, New York, NY, USA, runzhou.tao@columbia.edu; Yuxiang Peng, University of Maryland,
                                           College Park, College Park, MD, USA, ypeng15@umd.edu; Xiaodi Wu, University of Maryland, College Park, College Park,
                                           MD, USA, xwu@cs.umd.edu.

                                           Permission to make digital or hard copies of part or all of this work for personal or classroom use is granted without fee
                                           provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and
                                           the full citation on the first page. Copyrights for third-party components of this work must be honored. For all other uses,
                                           contact the owner/author(s).
                                           © 2024 Copyright held by the owner/author(s).
                                           ACM 2475-1421/2024/1-ART59
                                           https://doi.org/10.1145/3632901


                                                                             Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
59:2                                                         Haowei Deng, Runzhou Tao, Yuxiang Peng, and Xiaodi Wu


QSyn [Kang and Oh 2023], a quantum circuit synthesis method based on user-supplied components,
needs an average time of 687.5 seconds for solving 4-qubit problems and fails to synthesize a 6-qubit
circuit within one hour. These methods cannot scale with the rapid development of qubit numbers
in hardware, with more than 1000 qubits by the end of 2023 estimated by IBM [Gambetta 2022].
Moreover, synthesizing a quantum circuit will even fail at the start because it is impossible to
write the exponential-sized matrix specifying the synthesis goal. For example, QSyn requires 16
input-output state vector pairs as the specification for a 4-qubit Toffoli circuit. Additionally, the
circuit generated by the synthesizer is hard to understand by humans, which prevents potential
human customization to the circuit after synthesis.
   In this work, we propose QSynth, the first synthesis framework for inductive quantum programs.
In contrast to previous frameworks focusing on circuits, the synthesis target of QSynth is inductively-
defined families of quantum circuits without mid-circuit measurements (i.e. unitaries). QSynth can
exploit the inductive structure of quantum programs and, compared to previous circuit synthesis
methods, 1) generate quantum circuits with an arbitrary number of qubits, 2) allow user to use a
single input-output style specification for synthesis, and 3) produces more readable and structured
quantum program code that are easy to customize by human, as illustrated by Figure 1.


            Exponential-size matrix                                        Fixed-size Quantum Circuit
                       0   ⋯   1
                       ⋮   ⋱   ⋮                 Circuit Synthesis
                       1   ⋯   0

            Input-output specification                                       Quantum program
                |0⊗(#$%) ⟩ ↦                    Program Synthesis               H(0)
                 0⊗(#$%) + 1⊗(#$%)
                                                                                for i in range(n):
                                                                                    CNOT(i, i+1)



Fig. 1. Circuit synthesis vs. program synthesis. Circuit synthesis takes an exponential-sized matrix or state
vector pairs as input and generates a fixed-size circuit, while program synthesis takes in an input-output
specification and generates a program denoting a family of circuits for any input size.

   To enable the synthesis of inductive quantum programs, there are three challenges. First, the
synthesis framework requires a representation of the specification of quantum programs. Previous
methods such as quantum Hoare triple [Ying 2012], path-sum [Amy 2018], and tree automaton [Chen
et al. 2023] are all defined on fixed-dimension quantum systems and thus cannot be directly
applied. Naive extensions of these representations with a variable qubit size do not work because
symbolically representing matrices and automata is hard, limiting their usage for synthesis and
verification. We introduce a specification language in QSynth, which enables intuitive input-output
style specification for quantum programs and supports all path-sum quantum states with an
arbitrary number of qubits. We also propose the hypothesis-amplitude (ℎ − 𝛼) specification that uses
two functions to specify quantum programs. The specification written in QSynth-spec language
will be compiled into ℎ −𝛼 specification to use in the verification step, which avoids SMT-unfriendly
matrices (or graphical representations like automata).
   The second challenge is to find a subset of quantum programs that is both expressive enough
and efficient to synthesize. Previous programming languages for verifying quantum programs are
either low-level circuit languages that do not support inductive structure (e.g., SQIR [Hietala et al.
2021]) or high-level languages that do not have a detailed structure of unitaries (e.g., Quantum-
while language used in Quantum Hoare Logic [Ying 2012]). We design the Inductive-SQIR (ISQIR)
language, an extension of SQIR that supports inductively defined quantum programs. We also

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
A Case for Synthesis of Recursive Quantum Unitary Programs                                                       59:3


define a Hoare-type verification logic that verifies an ISQIR program with respect to an ℎ − 𝛼
specification.
   Finally, the synthesizer needs automated verification of inductive quantum programs. This
requires reasoning about matrices, complex numbers, and formulas with a non-fixed number of
terms, all of which have very limited support in SMT solvers. To solve this challenge, we define
parameterized path-sum amplitudes, which, together with a sparsity constraint, can be efficiently
encoded in SMT solvers. We further show that this set of expressions is expressive enough to
specify and synthesize many quantum programs.
   We evaluate QSynth on 10 inductive quantum programs including state preparation, arithmetic
and textbook quantum algorithm procedures. We showcase that QSynth can synthesize practical
quantum programs including quantum adders [Cuccaro et al. 2004; Feynman 1985], a quantum sub-
tractor, the eigenvalue inversion for HHL [Lloyd 2010] algorithm, quantum teleportation [Bennett
et al. 1993] and Quantum Fourier Transform [Coppersmith 2002]. All synthesis processes succeed
in 5 minutes, while many of the programs cannot be synthesized by previous methods when the
number of qubits is larger than 6. A further investigation of synthesized programs shows that
QSynth successfully captures the inductive structure of the targeting problem and produces better
programs than human-written programs in Qiskit.
    Contributions. Our contributions in this paper are multi-folded.
     • We propose QSynth, the first synthesis framework for inductively-defined quantum unitary
       circuit family.
     • We introduce the QSynth-spec language that enables input-output style specification for
       inductive quantum programs, and the hypothesis-amplitude (ℎ − 𝛼) specification for scalable
       verification of quantum programs.
     • We develop the syntax and the semantics of the inductive SQIR (ISQIR) language that supports
       recursively defined families of quantum unitary circuits, and a Hoare-type logic for proving
       the correctness of ISQIR program, with an ℎ − 𝛼 specification as predicates.
     • We design Parameterized path-sum amplitude (PPSA) function, which leads to the efficient
       encoding of the verification process into SMT instances.
     • We evaluate QSynth with a benchmark of 10 quantum programs, and show that QSynth is
       able to synthesize practical quantum programs.

2     QUANTUM PRELIMINARIES
In this section, we introduce the background knowledge about quantum program. We recommend
readers to refer Nielsen and Chuang [2010] for more details about quantum computing.

2.1    Quantum States
A quantum state consists of oneor more quantum bits. A quantum bit (or qubit) can be expressed
as a two dimensional vector 𝛽 such that |𝛼 | 2 + |𝛽 | 2 = 1. The 𝛼 and 𝛽 are            called amplitudes. We
                                         𝛼

frequently write this vector as 𝛼 |0⟩ + 𝛽 |1⟩ where |0⟩ = 10 and |1⟩ = 01 are basis states. A state
written |𝜙⟩ is called a ket, following Dirac’s notation. When both 𝛼 and 𝛽 are non-zero, we can
think of the qubit as being “both 0 and 1 at once,” a.k.a. a superposition. For example, √1 (|0⟩ + |1⟩) is
                                                                                                    2
an equal superposition of |0⟩ and |1⟩. A qubit is only in superposition until it is measured, at which
point the outcome will be 0 with probability |𝛼 | 2 and 1 with probability |𝛽 | 2 .
    A quantum state with 𝑛 qubits is represented as vector of length 2𝑛 . We can join multiple
qubits together by means of the tensor product (⊗) from linear algebra. For convenience, we write
|𝑥 0 ⟩ ⊗ |𝑥 1 ⟩ ⊗ · · · ⊗ |𝑥𝑚 ⟩ as |𝑥 0𝑥 1 ...𝑥𝑚 ⟩ for 𝑥𝑖 ∈ {0, 1}, 0 ≤ 𝑖 ≤ 𝑚; we may also write |𝑘⟩ where 𝑘 ∈ N
is the decimal interpretation of bits |𝑥 0𝑥 1 ...𝑥𝑚 ⟩. For example, a 2-qubit state is represented as a

                              Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
59:4                                                         Haowei Deng, Runzhou Tao, Yuxiang Peng, and Xiaodi Wu


22 = 4 length vector where each component corresponds to (the square root of) the probability of
measuring |00⟩, |01⟩, |10⟩, and |11⟩, respectively. We may also write these four kets as |0⟩, |1⟩, |2⟩, |3⟩.
Sometimes a multi-qubit state cannot be expressed as the tensor product of individual qubits; such
states are called entangled. One example is the state √1 (|00⟩ + |11⟩), known as a Bell pair.
                                                                  2

2.2    Quantum Programs
Quantum programs are composed of a series of quantum operations, each of
which acts on a subset of qubits. Quantum operations can be expressed as 1 0 0 0
matrices, and their application to a state is expressed as matrix multiplication. ©­             ª
                                                                                       0 1 0 0®®
For example,    the Hadamard operator 𝐻 on one qubit is expressed as a matrix ­      ­
√1 11 −11 . Applying 𝐻 to state |0⟩ yields state √1 |0⟩ + √1 |1⟩. 𝑛-qubit operators ­0 0 0 1®
                                                                                                ®
  2                                                2        2
are represented as 2𝑛 × 2𝑛 matrices. For example, the CNOT operator over two «0 0 1 0¬
qubits is expressed as the 22 × 22 matrix shown at the right.
    In the standard presentation, quantum programs are expressed as circuits, as shown in Fig 2(a). In
these circuits, each horizontal wire represents a qubit and boxes on these wires indicate quantum
operations, or gates. The circuit in Fig 2(a) has three qubits and three gates: the Hadamard (H) gate
and two controlled-not (CNOT) gates. The semantics of a gate is a unitary matrix. Applying a gate to
a state is tantamount to multiplying the state vector by the gate’s matrix. The matrix corresponding
to the circuit in Fig 2(a) is shown in Fig 2(c), where 𝐼 is the 2 × 2 identity matrix.


                                    |0⟩        •               H 0;
                                           𝐻
                                                               CNOT 0 1;
                                    |0⟩            •
                                                               CNOT 1 2;
                                    |0⟩
                                    (a) Quantum circuit           (b) Unitary SQIR
                                   (𝐼 ⊗ 𝐶𝑁𝑂𝑇 ) × (𝐶𝑁𝑂𝑇 ⊗ 𝐼 ) × (𝐻 ⊗ 𝐼 ⊗ 𝐼 )
                                                (c) Matrix expression

                      Fig. 2. Example quantum program: 3-qubit GHZ state preparation.



2.3    Unitary SQIR
SQIR [Hietala et al. 2021] is a simple quantum language embedded in the Coq proof assistant.
SQIR’s unitary fragment is a sub-language for expressing programs consisting of unitary gates.
   Syntax. A unitary SQIR program 𝑃 is a sequence of applications of gates 𝐺 to qubits 𝑞:
                                    𝑃 := 𝑃1 ; 𝑃2 | 𝐺 𝑞 | 𝐺 𝑞 1 𝑞 2 | 𝐺 𝑞 1 𝑞 2 𝑞 3 .
Qubits are referred to by natural numbers that index into a global register. A SQIR program is
parameterized by a unitary gate set 𝑔 (from which 𝐺 is drawn) and the size 𝑛 of the global register
(i.e., the number of available qubits). In Coq, a unitary SQIR program U hence has type ucom g n.
𝑈 has type ucom 𝑔 𝑛, where 𝑔 identifies the gate set and 𝑛 is the size of the global register.
    The Coq function ghz on the left recursively constructs a SQIR program, which prepares the
𝑛 + 1-qubit GHZ state. When 𝑛 = 0, the program applies the Hadamard gate 𝐻 to qubit 0. Otherwise,
ghz calls itself recursively with input 𝑛 − 1 and then applies CNOT to qubits 𝑞𝑛−1, 𝑞𝑛 . For example,
ghz 2 generates the circuit in Fig 2(a).


Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
A Case for Synthesis of Recursive Quantum Unitary Programs                                                          59:5



                                              [ 𝑃1 ; 𝑃2 ] 𝑑 = [ 𝑃2 ] 𝑑 × [ 𝑃1 ] 𝑑 ;
                                           𝑎𝑝𝑝𝑙𝑦𝑖 (𝐺, 𝑞 1, ..., 𝑞𝑖 , 𝑑)
                                           
                                                                             well-typed
                  [ 𝐺 𝑞 1 · · · 𝑞𝑖 ] 𝑑 =                                                   , 𝑖 = 1, 2, 3.
                                           0 𝑑                               otherwise
                                            2

Fig. 3. Semantics of unitary SQIR programs, assuming a global register of dimension 𝑑. The 𝑎𝑝𝑝𝑙𝑦𝑘 function
maps a gate name to its corresponding unitary matrix and extends the intended operation to the given
dimension by applying an identity operation on every other qubit in the system.



                                                   Semantics. The semantics of unitary SQIR is shown
Fixpoint ghz (n : nat) : ucom g ( n + 1) :=
                                                in Fig 3. A program 𝑃 is well-typed if every gate’s index
  match n with
                                                arguments are within the bounds of the global register
    | 0 ⇒ H0
                                                and no index is repeated. The program’s semantics
    | S n' ⇒ ghz n'; CNOT n' n
                                                follows from the composition of the matrices that cor-
  end.
                                                respond to each of the applications of its unitary gates.
                                               A gate application’s matrix needs to apply the identity
operation to the qubits not being operated on. This is the purpose of using 𝑎𝑝𝑝𝑙𝑦1, 𝑎𝑝𝑝𝑙𝑦2 and
𝑎𝑝𝑝𝑙𝑦3 For example, 𝑎𝑝𝑝𝑙𝑦1 (𝐺𝑢 , 𝑞 1, 𝑑) = 𝐼 2𝑞 ⊗ 𝑢 ⊗ 𝐼 2 (𝑑 −𝑞−1) where 𝑢 is the matrix interpretation of
the gate 𝐺𝑢 and 𝐼𝑘 is the 𝑘 × 𝑘 identity matrix.
   Suppose that 𝑀1 and 𝑀2 are the matrices corresponding to unitary gates 𝑃1 and 𝑃2 , which we
want to apply to a quantum state vector |𝜓 ⟩. Matrix multiplication is associative, so 𝑀2 (𝑀1 |𝜓 ⟩)
is equivalent to (𝑀2 𝑀1 )|𝜓 ⟩. Moreover, multiplying two unitary matrices yields a unitary matrix.
As such, the semantics of SQIR program 𝑃1 ; 𝑃2 is naturally described by the unitary matrix 𝑀2 𝑀1 .
Fig 2(b) shows an example unitary SQIR program for the circuit in Fig 2(a).

2.4   Path-sum Representation
Path-sum, proposed by recent works on quantum program verification [Amy 2018; Chareton et al.
2020], is a representation for describing quantum states based on Feynman’s path integral formalism
of quantum mechanics, which is widely applied to circuit simulation [Bravyi and Gosset 2016;
Koh et al. 2017] and optimization [Amy et al. 2018, 2014; Amy and Mosca 2019]. The idea of
this formalism is to describe a quantum state’s amplitude by an integral over all paths leading to
that state. In practice, a discrete sum-over-path technique rather than integral is typically used
[Amy 2018; Amy et al. 2014; Amy and Mosca 2019; Bacon et al. 2008; Bravyi and Gosset 2016;
Chareton et al. 2020; Dawson and Nielsen 2005; Koh et al. 2017; Montanaro 2017]. We can describe
a sum-over-path abstractly as a discrete set of paths 𝑇 ∈ Z𝑚  2 , together with an amplitude function
𝜓 and a state transformation 𝑓 , both depending on specific path 𝑦, to represent a unitary 𝑈 :
                                               ∑︁
                                    𝑈 : |𝑥⟩ ↦→    𝜓 (𝑥, 𝑦)|𝑓 (𝑥, 𝑦)⟩.
                                                          𝑦 ∈𝑇

All representations based on the sum-over-path in these previous works[Amy 2018; Bacon et al.
2008; Chareton et al. 2020; Dawson and Nielsen 2005; Koh et al. 2017; Montanaro 2017] share in
common that the amplitude 𝜓 (𝑥, 𝑦) of all possible paths have the same magnitude and only the
phases are different. These forms of the same magnitude but different phase are so typical in many
quantum algorithms that they can be used as a succinct representation in the verification, which
makes them useful for synthesis purposes.

                                 Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
59:6                                                                       Haowei Deng, Runzhou Tao, Yuxiang Peng, and Xiaodi Wu



             QSynth-spec            Hypothesis-
                                                                       Verifier
             specification        amplitude ℎ, 𝛼𝛼               Do we have
             (Section 4.1)         (Section 4.2)                      ISQIR Logic
                                                                       (Section 5)
                                                                                             Yes
                                                                       Efficient encoding
                                         Candidate                                            𝑆𝑆𝑐𝑐
                                                                           with PPSA
                                         program 𝑆𝑆𝑐𝑐
                                                                           (Section 6)
                             Searcher
                                                                      SMT Solver
                                                                                                          Q#
                                           No


                                                Fig. 4. QSynth Overview.

                                                         GHZ(n-1)
                                                                                            def GHZ ( N ) :
                                         |0⟩        𝐻       •                                   circuit = QuantumCircuit ( N +1)
    𝑆𝐺𝐻𝑍 := fix1 𝐼𝑑                                                                             def S ( circ , n ) :
                                         |0⟩                      •                                   if n ==0:
            const H 0                                                                                       circ . h (0)
                                         |0⟩                                                          else :
            const ID                                ..                ..                                    S ( circ , n -1)
                                                     .                     .
            const CNOT n-1 n             |0⟩                                    •                           circ . cx (n -1 , n )
                                                                                                S ( circuit , N )
                                         |0⟩                                                    return circuit
       (a) ISQIR program
                                           (b) (𝑛 + 1)-qubit GHZ circuit
                                                                                                     (c) Qiskit program

Fig. 5. (𝑛 + 1)-qubit GHZ state preparation programs in different programming languages. (a) ISQIR program
𝑆𝐺𝐻𝑍 . (b) The quantum circuit represented by 𝑆𝐺𝐻𝑍 . (c) Qiskit function compiled from 𝑆𝐺𝐻𝑍 . Statement
circ.cx in Qiskit means appending a CNOT gate to the circuit. Qiskit’s semantic requires the program always
use class QuantumCircuit(n) to initialize a circuit. So QSynth compiler will wrap program 𝑆 with an outside
function GHZ to initialize the circuit.

3      OVERVIEW
The workflow of QSynth is shown in Fig 4. First, the user writes an input-output style specification
of the program to be synthesized using the QSynth-spec language. Then, QSynth will translate the
specification into a hypothesis-amplitude (h-𝛼) pair for later verification. Meanwhile, QSynth will
invoke a syntax-guided program searcher [Gulwani et al. 2017] to generate all possible candidate
programs written in the ISQIR language within a given search space. For each candidate ISQIR
program, QSynth will use the unitary ISQIR logic to verify whether the program satisfies the (h-𝛼)
specification. The verification process will be done in an SMT solver in which all the numbers
are encoded in the form of parameterized path-sum amplitudes (PPSA). If the verification process
succeeds, a correct program is synthesized and the program can be translated by QSynth’s ISQIR
compiler into commercial quantum programming languages including Qiskit, Q# and Braket, as
shown in Figure 5. If the verification fails, the searcher will try the next candidate program.
   Next, we will walk through QSynth’s components using the synthesis of the GHZ state prepara-
tion program as an example.
  Target Program. An 𝑁 -qubit (𝑁 ∈ 𝑍 + ) Greenberger-Horne-Zeilinger state (GHZ state) is an
entangled quantum state given by
                                                     1
                                          |𝐺𝐻𝑍 ⟩𝑁 = √ (|0⟩ ⊗𝑁 + |1⟩ ⊗𝑁 ),
                                                      2

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
A Case for Synthesis of Recursive Quantum Unitary Programs                                                       59:7


which was first studied by Greenberger et al. [1989] and is widely used in quantum information,
e.g., [Hillery et al. 1999; Liao et al. 2014; Xia et al. 2006; Zhong-Xiao and Yun-Jie 2006]. Preparing
the 𝑁 -qubit GHZ state from |0⟩ ⊗𝑁 for any 𝑁 is a natural task for program synthesis.
   Namely, we hope to synthesize an ISQIR program 𝑆 such that [ {{𝑆 }}(𝑛)]] , the instantiation of 𝑆
with 𝑛 ∈ N where N denotes the natural number in the following paper, is a unitary that transfers
state |0⟩𝑛+1 to state |𝐺𝐻𝑍 ⟩𝑛+1 for any 𝑛 ≥ 0.

   Target Specification. Our first challenge is how to specify our target program, which generates
|𝐺𝐻𝑍 ⟩𝑛+1 from |0⟩𝑛+1 . The difficulty is two-folded: (1) we want a specification for any input 𝑛,
which excludes any existing specification methods for fixed dimensions (e.g., Quantum Hoare
triples); (2) the specification should be as succinct as possible. Then, a direct matrix representation
that might require 2𝑛+1 × 2𝑛+1 is less desirable.
   In QSynth, the specification is given in an input-output manner using the QSynth-spec language
in the form √ of GHZ : |0𝑛+1 ⟩ ↦→ |0𝑛+1 ⟩ ⊎ |(2𝑛+1 − 1)𝑛+1 ⟩, where |𝑎⟩ ⊎ |𝑏⟩ means the normalized sum
(|𝑎⟩ + |𝑏⟩)/ 2. Then, the input-output style specification is compiled into the following hypothesis-
amplitude (ℎ − 𝛼) specification (Definition 4.1) for later verification. An instantiation of (ℎ − 𝛼) to
the GHZ target program is given as follows:

                                                                  1
               ℎ := {(𝑛, 𝑥, 𝑦) | 𝑥 = 0},       𝛼𝐺𝐻𝑍 (𝑛, 𝑥, 𝑦) := √ 𝛿 (𝑦 = 0 ∨ 𝑦 = 2𝑛+1 − 1),                   (3.1)
                                                                   2

where the term 𝛿 (𝑏) in 𝛼𝐺𝐻𝑍 is a {0,1}-valued function that returns 1 if the Boolean expression 𝑏 is
True and 0 otherwise.
  Intuitively, the hypothesis function ℎ specifies the interesting input to the program, the desired
program’s behaviour which is specified by the amplitude function 𝛼. Precisely, given input 𝑥, the
amplitude ⟨𝑦| [ {{𝑆 }}(𝑛)]] |𝑥⟩ of basis 𝑦 on the input 𝑥 for a desired program 𝑆 is given by 𝛼 (𝑛, 𝑥, 𝑦),
where 𝑥, 𝑦 are bit strings.
  In the GHZ example, we are only interested in input |0⟩𝑛+1 , which leads to a trivial ℎ containing
only 𝑥 = 0 in (3.1). The output state, which is √1 (|0⟩𝑛+1 + |1⟩𝑛+1 ), corresponds to an amplitude
                                                         2
function 𝛼 (𝑛, 𝑥, 𝑦) with only non-zero value √1 on either 𝑦 = 0 (referring to |0⟩𝑛+1 ) or 𝑦 = 2𝑛+1 − 1
                                                     2
(referring to |1⟩𝑛+1 ), which explains (3.1).
   Our hypothesis-amplitude specification is arguably as natural as the common classical specifica-
tions that describe the desired input-output relationship, except that one could have many such
input-output pairs (i.e., superposition) with potential complex amplitudes, in the quantum setting,
which requires an explicit use of our amplitude function 𝛼 (𝑛, 𝑥, 𝑦).

   Verification of Candidate Programs. Assume the QSynth searcher has identified a candidate 𝑆𝐺𝐻𝑍 ,
same as Fig 5 (a), on the left of Fig 6. The program 𝑆𝐺𝐻𝑍 is constructed by a FIX syntax with
subprograms 𝑆 0 = H 0, 𝑆𝐿 = ID and 𝑆𝑅 = CNOT n-1 n, which is a recursive program with the
base case 𝑆𝐺𝐻𝑍 (0) := 𝑆 0 and the inductive case, 𝑆𝐺𝐻𝑍 (𝑛) := 𝑆𝐿 (𝑛); 𝑆𝐺𝐻𝑍 (𝑛 − 1); 𝑆𝑅 (𝑛). This ISQIR
program is equivalent to the recursive Qiskit program in Figure 5c. The FIX syntax, similar to the
fixpoint in Coq, enables inductive structures in ISQIR programs.
   QSynth verifier leverages the newly developed unitary ISQIR logic (Section 5.2) to verify the
goal judgement ℎ ⊲ 𝑆𝐺𝐻𝑍 ↔ 𝛼𝐺𝐻𝑍 , which basically states that candidate program 𝑆𝐺𝐻𝑍 satisfies
the (ℎ, 𝛼) specification. QSynth verifier recursively applies the logic rules to split the judgement of
ℎ, 𝛼 for larger programs into that of smaller programs. The side conditions are checked by SMT
solvers, and the ℎ, 𝛼 judgement for constant SQIR program for quantum gates that are independent
of 𝑛 are directly computed.

                              Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
59:8                                                              Haowei Deng, Runzhou Tao, Yuxiang Peng, and Xiaodi Wu


                  User’s specification                                           αI (n, x, y) = δ(x = y)
              h(n, x, y) := {(n, x, y)|x = 0}                      αH (n, x, y) = √12 · δ(x\2 = y\2) · e2πi·d(x[0]∗y[0])
       αGHZ (n, x, y) := √12 δ(y = 0 ∨ y = 2n+1 − 1)   αCN OT (n, x, y) = δ(x[n − 1 : 0] = y[n − 1 : 0] ∧ y[n] = x[n] ⊕ x[n − 1])


         Candidate Program
       SGHZ := fix1 Id S0 SL SR
                                                                h ▷ S0 ↔ αH            N3 ▷ S0 ↔ αH
                                       Verification Goal FIX    h ▷ SL ↔ αI   WEAKEN   N3 ▷ S L ↔ α I
            S0 := const H 0                                                                                              CONST
                                         h ▷ SGHZ ↔ α        N3 ▷ SR ↔ αCN OT        N3 ▷ SR ↔ αCN OT
            SL := const ID
        SR := const CNOT n-1 n
                                         FIX
                                                                      Proof based on the SMT Solver
                                                                       ∀ 0 ≤ n < 1, (h, αGHZ ) ≡n (h, αH )
                                                       ∀n ≥ 1, (h, αGHZ ) ≡n (h, αI ) ⊗ (Id ◦ pred(h, αGHZ )) ⊗ (N3 , αCN OT )



                  Fig. 6. An example of synthesizing 𝑛 + 1-qubit GHZ state preparation program.

   In the GHZ example, QSynth verifier first uses the FIX rule to split the goal judgement into two
parts. The first part is two formulas (right bottom of Fig 6) to be checked by the SMT solver, with
details elaborated on later. The second part is three judgements for 𝑆𝐿 , 𝑆𝑅 , 𝑆 0 (right hand of the
verification goal box in Fig 6). After applying the FIX rule QSynth uses the WEAKEN rule to adjust
these judgements into an appropriate format. Since 𝑆 0, 𝑆𝐿 , 𝑆𝑅 are simple programs (formally called
const SQIR programs), their corresponding hypothesis-amplitude specifications (i.e. 𝛼 𝐼 , 𝛼 𝐻 , 𝛼𝐶𝑁 𝑂𝑇
on the upper right corner of Fig 6) are predefined in QSynth and can be verified directly using
the CONST rule. 𝛼 𝐼 returns 1 if 𝑥 = 𝑦 else 0, indicating the identity matrix. 𝛼 𝐻 represents the
                                                                                   𝑥 [0]∗𝑦 [0]
matrix of the program const H 0, i.e., √1 11 −1  1   ⊗ 𝐼 𝑛 . The expression 𝑒 2𝜋𝑖 · 2
                                                   
                                                                                               in 𝛼 𝐻 returns
                                            2
                                                                               1 1 1
                                                                                          
−1 if 𝑥 [0] = 1, 𝑦 [0] = 1 and returns 1 otherwise, indicating the matrix    √              ; the expression
                                                                                2 1 −1
𝛿 (𝑥\2 = 𝑦\2), where 𝑥\2 and 𝑦\2 are integer division (e.g. 10\3 = 3), returns 1 if 𝑥, 𝑦 only have the
lowest bit difference and 0 otherwise, indicating the matrix 𝐼 𝑛 on qubits 𝑞 1, ..., 𝑞𝑛 . 𝛼𝐶𝑁 𝑂𝑇 will be
discussed later. After this verification step, the synthesis terminates and QSynth compiles 𝑆𝐺𝐻𝑍
into programs as shown in Fig 5.
   SMT solving with PPSA. We continue with the two formulas in the bottom right corner box in
Fig 6 generated by the FIX rule and aim to verify them by SMT solvers.
   The first formula indicates the base case is correct. The relation ≡𝑛 indicates the equivalence
between two hypothesis-amplitude specifications given specified 𝑛. In this GHZ example, the first
formula becomes:
                                    ∀𝑥 𝑦 ∈ N, 𝑥 = 0 → 𝛼𝐺𝐻𝑍 (0, 𝑥, 𝑦) = 𝛼 𝐻 (0, 𝑥, 𝑦).
Note that the amplitude functions 𝛼𝐺𝐻𝑍 or 𝛼 𝐻 are generally complex-valued, the automatic equiva-
lence check of which are not generally supported by any existing tool.
   Inspired by recent work on quantum program verification [Amy 2018; Chareton et al. 2020],
QSynth restricts 𝛼 into a succinct path-sum representation yet with rich enough expressiveness
(elaborated on in Section 6.1), called the parameterized path-sum amplitude (PPSA) in Definition 6.1.
In PPSA representation, the non-zero amplitudes over 𝑥, 𝑦 share the same magnitude, which depends
on 𝑛, but can have different phases. Thus, instead of representing a general amplitude function
𝛼 (𝑛, 𝑥, 𝑦), it suffices to represent 𝛼 (𝑛, 𝑥, 𝑦) by components. For instance, 𝛼 𝐻 , 𝛼𝐺𝐻𝑍 defined in Fig 6,
can be described with three components:
 • A fraction expression indicating the amplitude: √1 for both 𝛼𝐺𝐻𝑍 , 𝛼 𝐻 .
                                                                      2
 • A Boolean expression indicating the non-zero value: 𝛿 (𝑦 = 0 ∨ 𝑦 = 2𝑛+1 − 1) for 𝛼𝐺𝐻𝑍 and
   𝛿 (𝑥\2 = 𝑦\2) for 𝛼 𝐻 .

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
A Case for Synthesis of Recursive Quantum Unitary Programs                                                        59:9

                                                                             𝑥 [0]∗𝑦 [0]
 • An expression indicating the phase: 𝑒 2𝜋𝑖 ·0 for 𝛼𝐺𝐻𝑍 and 𝑒 2𝜋𝑖 · 2     for 𝛼 𝐻 , where 𝑥 [0] means
   the lowest (i.e. 0th) bit of 𝑥’s binary representation (e.g. 6[0] = (110)𝑏 = 0).
A direct substitution of 𝛼 𝐻 , 𝛼𝐺𝐻𝑍 would require QSynth, or SMT solvers, to verify
                                    1                      1                      𝑥 [0]∗𝑦 [0]
             ∀𝑥 𝑦 ∈ N, 𝑥 = 0 → √ 𝛿 (𝑦 = 0 ∨ 𝑦 = 1) = √ 𝛿 (𝑥\2 = 𝑦\2) · 𝑒 2𝜋𝑖 · 2 ,
                                     2                      2
which is infeasible. Using PPSA, one can equivalently verify the following by SMT solvers:
                                    1     1                                   𝑥 [0] ∗ 𝑦 [0]
           ∀𝑥 𝑦 ∈ N, 𝑥 = 0 → √ = √ ∧ 𝛿 (𝑦 = 0 ∨ 𝑦 = 1) = 𝛿 (𝑥\2 = 𝑦\2) ∧                    = 0.
                                     2     2                                        2
   The second formula concerns the correctness of the induction case. The function 𝑝𝑟𝑒𝑑 (ℎ, 𝛼𝐺𝐻𝑍 )
generates the hypothesis-amplitude specification for the recursive call (i.e. 𝑆𝐺𝐻𝑍 (𝑛 − 1)), and
(ℎ 1, 𝛼 1 ) ⊗ (ℎ 2, 𝛼 2 ) calculates the one when composing two ISQIR programs together, both formally
in Definition 5.4. In this example, the composition with (ℎ, 𝛼 𝐼 ) is trivial since 𝛼 𝐼 represents an
identity matrix, and the second formula becomes
                                ∀𝑛 ≥ 1, ∀𝑥 𝑦 ∈ N, (ℎ, 𝛼𝐺𝐻𝑍 ) ≡𝑛 (ℎ, 𝛼 ′ ),
                                              ∑︁
                        where 𝛼 ′ (𝑛, 𝑥, 𝑦) =    𝛼𝐺𝐻𝑍 (𝑛 − 1, 𝑥, 𝑧)𝛼𝐶𝑁 𝑂𝑇 (𝑛, 𝑧, 𝑦),                            (3.2)
                                                𝑧 ∈N
              𝛼𝐶𝑁 𝑂𝑇 (𝑛, 𝑥, 𝑦) = 𝛿 (𝑥 [𝑛 − 1 : 0] = 𝑦 [𝑛 − 1 : 0] ∧ 𝑦 [𝑛] = 𝑥 [𝑛] ⊕ 𝑥 [𝑛 − 1]).
𝛼𝐶𝑁 𝑂𝑇 is designed to represents 𝑆𝑅 : the term 𝑥 [𝑛 − 1 : 0] = 𝑦 [𝑛 − 1 : 0] indicates the identity
map |𝑞 0 ...𝑞𝑛−1 ⟩ ↦→ |𝑞 0 ...𝑞𝑛−1 ⟩; the term 𝑦 [𝑛] = 𝑥 [𝑛] ⊕ 𝑥 [𝑛 − 1] indicates the map |𝑞𝑛−1 ⟩|𝑞𝑛 ⟩ ↦→
|𝑞𝑛−1 ⟩|𝑞𝑛−1 ⊕𝑞𝑛 ⟩. Their combination indicates 𝑆𝑅 ’s map, i.e., |𝑞 0 ...𝑞𝑛−1 ⟩|𝑞𝑛 ⟩ ↦→ |𝑞 0 ...𝑞𝑛−1 ⟩|𝑞𝑛−1 ⊕𝑞𝑛 ⟩.
   There is another major challenge to verify (3.2) by SMT solvers due to the infinite summation
over 𝑧 ∈ N, which comes from the composition of two amplitude specifications (details in Section 5).
As a result, 𝛼 ′ could have an unbounded number of terms, which makes it infeasible for any SMT
solver.
   To circumvent this general difficulty, we introduce a sparsity constraint, which restricts the
number of non-zero points with any fixed 𝑥 or 𝑦 to be constant (Definition 6.2), and prove that
the composition of two amplitude functions will have finite terms if one of the composed function
is sparse. We also prove that all quantum gates applied on a constant number of qubits (e.g.
all SQIR programs) have a sparse amplitude function. We only apply this sparsity constraint to
SQIR programs predefined in QSynth, and non-sparse functions can be generated as synthesis
specifications. However, the use of the FIX statement could generate non-sparse amplitude functions.
   As a result, we only allow one use of the FIX statement in our synthesis, as otherwise we
could risk composing two non-sparse amplitude functions that would lead to an infinite sum. The
specification for the target program, however, could be non-sparse, as we won’t need to compose
the target programs with others.
   In the GHZ example, 𝛼𝐶𝑁 𝑂𝑇 is sparse and we have
                       ∀𝑛, 𝑦 ∈ N,     𝛼𝐶𝑁 𝑂𝑇 (𝑛, 𝑧, 𝑦) ≠ 0 ↔ 𝑧 = 𝑦 ⊕ (𝑦 [𝑛 − 1]«𝑛).
Here the expression 𝑦 ⊕ (𝑦 [𝑛 − 1]«𝑛) sets the (𝑛 + 1)th bit of 𝑦 (i.e. 𝑦 [𝑛]) to 𝑦 [𝑛] ⊕ 𝑦 [𝑛 − 1] and
keeps 𝑦 [𝑛 − 1 : 0] unchanged. Let 𝑧 = 𝑦 ⊕ (𝑦 [𝑛 − 1]«𝑛). With this sparsity of 𝛼𝐶𝑁 𝑂𝑇 , we can simplify
the formula (3.2) to
                   ∀𝑛 ≥ 1, ∀𝑥 𝑦 ∈ N, (ℎ, 𝛼𝐺𝐻𝑍 ) ≡𝑛 (ℎ, 𝛼 ′ ),
                                                                       1
           where 𝛼 ′ (𝑛, 𝑥, 𝑦) = 𝛼𝐺𝐻𝑍 (𝑛 − 1, 𝑥, 𝑧)𝛼𝐶𝑁 𝑂𝑇 (𝑛, 𝑧, 𝑦) = √ 𝛿 (𝑧 = 0 ∨ 𝑧 = 2𝑛 − 1).
                                                                        2

                               Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
59:10                                                             Haowei Deng, Runzhou Tao, Yuxiang Peng, and Xiaodi Wu


With the PPSA representation, it suffices to verify the following SMT instance:
                                1      1
    ∀𝑛 ≥ 1, ∀𝑥 𝑦 ∈ N, 𝑥 = 0 → √ = √ ∧ 𝛿 (𝑦 = 0 ∨ 𝑦 = 2𝑛+1 − 1) = 𝛿 (𝑧 = 0 ∨ 𝑧 = 2𝑛 − 1).
                                 2      2
   Organization. In Section 4 we describe the QSynth’s specification language and hypothesis-
amplitude specification. In Section 5 we introduce the ISQIR programming language for the inductive
quantum circuit family, and its associated Hoare-type logic, In Section 6 we introduce the PPSA
encoding. In Section 7 we discuss the implementation and the evaluation of QSynth on a benchmark
of 10 programs. In Section 8 we discuss the related work. In Section 9 we discuss the limitation of
QSynth and future work. In Section 10 we give the conclusion.

4     SPECIFICATION
In this section, we explain how specifications are provided and processed in QSynth. Users provide
the input-output specification in the QSynth-spec language (defined in Section 4.1). Then, the
specification will be compiled into a hypothesis-amplitude pair (defined in Section 4.2) as the
predicate for later verification. We describe the compilation process in Section 4.3

4.1     QSynth-spec Interface
To allow users to give the synthesis specification more intuitively, we design language QSynth-spec
shown in Fig 7. Programmers provide the synthesis specification in QSynth-spec, and QSynth will
compile it to the corresponding hypothesis-amplitude specification.


        (Spec)       S   ::=   I ↦→ O
        (Input)      I   ::=   |𝑐𝑙 ⟩ | |𝑣 [ℓ]⟩ | I1 ⊗ I2
        (Output)               |𝐸⟩ | 𝑒 𝑖 ·𝐸 · 𝑂 ′ | O1 ⊗ O2 | 𝑒 𝑖 ·𝐸1 |𝑐 1 ⟩ ⊎ 𝑒 𝑖 ·𝐸2 |𝑐 2 ⟩ | 𝑧 ∈ {0,1}𝑙 𝛿 (𝐵) · 𝑒 −2𝜋𝑖 ·𝐸 |𝑧⟩
                                                                                               Ò
                     O   ::=
        (VarExp)     𝐸   ::=   𝑐 ℓ | 𝑣 | uop 𝐸 ′ | 𝐸 1 bop 𝐸 2
        (BoolExp)    𝐵   ::=   𝐸 1 rop 𝐸 2 | 𝐵 1 ∧ 𝐵 2 | 𝐵 1 ∨ 𝐵 2
        (Length)     ℓ   ::=   𝑐 | n | uop ℓ ′ | ℓ1 bop ℓ2
        (Variable)   𝑣    ∈    Variables                                 (Constant)       𝑐    ∈    N

  Fig. 7. QSynth-spec syntax. uop and bop are common unary operators and binary operators (e.g. + - * /)
. rop are common relation operators (e.g. ==, !=, >, <). 𝛿 (𝐵) is a function that returns 1 if 𝐵 is True and returns
                               0 otherwise. ⊎ means normalized summation.

    A QSynth-spec specification is given in the form 𝐼𝑛𝑝𝑢𝑡 ↦→ 𝑂𝑢𝑡𝑝𝑢𝑡. 𝐼𝑛𝑝𝑢𝑡 indicates the input
quantum state to the desired unitary. It is a ket expression constructed by 𝑙-bit constant numbers
𝑐𝑙 , a 𝑙−bit variable 𝑣 [𝑙], or the tensor product of two quantum states. Programmers can arbitrarily
declare variables in the 𝐼𝑛𝑝𝑢𝑡. For example, consider the 𝐼𝑛𝑝𝑢𝑡 specification for a 𝑛-bit quantum
adder: |𝐴⟩|𝐵⟩|0⟩𝑛 ↦→ |𝐴⟩|𝐵⟩|𝐴 + 𝐵⟩.
                                   |0⟩|𝐴[𝑛]⟩|𝐵 [𝑛]⟩|0𝑛 ⟩ ↦→ |𝑐 0 ⟩|𝐴⟩|𝐵⟩|𝐴 + 𝐵⟩                                                    (4.1)
where 𝑐 0 is the carry bit of 𝐴 + 𝐵. We simplify |𝜙⟩ ⊗ |𝜓 ⟩ as |𝜙⟩|𝜓 ⟩ and omit the length specification
for the one-bit state |0⟩, |1⟩. This specification indicates the qubit 𝑞 0 is initialized as |0⟩ to hold the
carry bit; qubits 𝑞 1 ∼ 𝑞𝑛 and qubits 𝑞𝑛+1 ∼ 𝑞 2𝑛 store two 𝑛-bit numbers 𝐴[𝑛], 𝐵 [𝑛]; qubit 𝑞 2𝑛+1 ∼ 𝑞 3𝑛
are initialized to |0⟩𝑛 to store the sum of 𝐴[𝑛], 𝐵 [𝑛].
  𝑂𝑢𝑡𝑝𝑢𝑡 suggests the state transformed from 𝐼𝑛𝑝𝑢𝑡 by the target unitary program. 𝑂𝑢𝑡𝑝𝑢𝑡 can be
constructed by a variable expression 𝐸, a state shifted by the phase 𝑒 𝑖𝐸 , or the tensor product of two

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
A Case for Synthesis of Recursive Quantum Unitary Programs                                                      59:11


states. The variables that appear in 𝐸 are bound: they can only be a variable declared in 𝐼𝑛𝑝𝑢𝑡 or the
sum variable 𝑦 when it is in the sum scope. Output can also be constructed as the superposition state
with the same magnitude but different phase by 𝑒 𝑖 ·𝐸1 |𝑐 1 ⟩ ⊎ 𝑒 𝑖 ·𝐸2 |𝑐 2 ⟩ and 𝑧 ∈ {0,1}𝑙 𝛿 (𝐵) · 𝑒 −2𝜋𝑖 ·𝐸 |𝑧⟩.
                                                                                  Ò
For example, consider the specifications for 𝑛-qubit GHZ state program and QFT program.
                                                                              Ú                   𝑥𝑦
            GHZ𝑛 : |0𝑛 ⟩ ↦→ |0𝑛 ⟩ ⊎ |(2𝑛 − 1)𝑛 ⟩    QFT𝑛 : |𝑥 [𝑛]⟩ ↦→                    𝑒 −2𝜋𝑖 · 2𝑛          (4.2)
                                                                                    𝑦 ∈ {0,1}
                                                                                       𝑛


Programmers can omit the amplitude normalization term, which will be calculated by QSynth
during the compilation from QSynth-spec to the hypothesis-amplitude specification.

4.2   Hypothesis-amplitude Specification for Verification
A critical component of program synthesis is the ability of expressing desired properties of the
target programs, usually called specifications. The pre and post conditions of programs in typical
Hoare triples provide a natural approach to express these input-output specifications. Quantum
Hoare triples [Ying 2012] are hence a natural candidate for describing input-output specifications
for quantum programs. However, contrary to the classical setting where pre/post conditions have a
lot of flexibility in description, the conventional pre/post conditions in quantum Hoare triples are
described by quantum predicates which are Hermitian matrices of exponential dimensions in terms
of the system size. The exponential dimension of quantum predicates incurs both the scalability
issue and technical inconvenience in automating the reasoning directly based on quantum Hoare
triples.
   Moreover, for ISQIR programs, one needs to express the specifications for a family of programs
for different sizes, which is like classical program synthesis with a varying-length array of variables.
However, existing Hoare triples can only be used to provide specifications for quantum systems of
a fixed dimension.
   To that end, we develop the so-called hypothesis-amplitude specifications for quantum circuit
families, where the hypothesis component (denoted ℎ) of the specification describes a certain subset
of input states 𝑥 in the computational basis, and the amplitude component (denoted 𝛼) describes
the output state of the program on the given input 𝑥. Both ℎ, 𝛼 are functions of the index 𝑛 so that
they can describe a family of quantum circuits.

  Definition 4.1. A hypothesis-amplitude triple contains ℎ, 𝑆 and 𝛼. Here ℎ is a set of tuples
(𝑛, 𝑥, 𝑦) ∈ N3 (we abuse the notation ℎ to also represent its indicator function of type N3 → B) that
specifies the interested entries of 𝑆’ semantics, 𝑆 is a quantum circuit family parameterized with a
natural number 𝑛, and 𝛼 (𝑛, 𝑥, 𝑦) is a complex function with natural number inputs.
  A hypothesis-amplitude triple is a valid judgement, denoted ℎ ⊲ 𝑆 ↔ 𝛼, when

                      ℎ ⊲ 𝑆 ↔ 𝛼 ⇐⇒ ∀(𝑛, 𝑥, 𝑦) ∈ ℎ, ⟨𝑦| [ {{𝑆 }}(𝑛)]] |𝑥⟩ = 𝛼 (𝑛, 𝑥, 𝑦).                         (4.3)

   Following the above definition, the hypothesis ℎ is like classical pre-conditions and specifies
the set of inputs where the post-conditions are provided. For any such input 𝑥, the output state of
                                                 Í
the program 𝑆 (𝑛) is given by [ {{𝑆 }}(𝑛)]] |𝑥⟩ = 𝑦 𝛼 (𝑛, 𝑥, 𝑦)|𝑦⟩, which explains why 𝛼 is called the
amplitude. We do not always need to specify the program’s semantics for all inputs, so we use set
ℎ to filter those unnecessary information. By the linearity of unitary, the input-output specification
on a set of inputs in the computational basis can be extended to a specification in the linear space
spanned by the given input set.
   Compared with quantum Hoare triples, our hypothesis-amplitude specification provides a more
flexible and arguably more intuitive way to formalize the desired properties on the target functions.
For instance, for state preparation, our specification is almost straightforward to use and avoids

                               Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
59:12                                                        Haowei Deng, Runzhou Tao, Yuxiang Peng, and Xiaodi Wu


the extra efforts of converting specifications into exponential-size quantum predicates. 1 Moreover,
for all unitary programs, our hypothesis-amplitude specification could provide the same expressive
power as general quantum Hoare triples at the cost of using potentially complicated ℎ, 𝛼. Neverthe-
less, efficiently encoding into SMT instances are only known in restricted cases of ℎ, 𝛼 as discussed
in Section 6.

4.3     From QSynth-spec to Hypothesis-amplitude Specification
Given a QSynth-spec specification 𝐼 ↦→ 𝑂, QSynth compiles it to the hypothesis-amplitude specifi-
cation in two steps: (1) generates the corresponding hypothesis ℎ and a variable map Π based on
𝐼 , where Π maps variables claimed in 𝐼 to the qubits; (2) generates the corresponding amplitude
function 𝛼 based on 𝑂 and Π.
   Generate Π and ℎ from 𝐼 . QSynth first calculates the total number of input qubits by adding
up the length specifications of constants and variables in the input. This number depends on
the parameter 𝑛. Then, QSynth assigns indexes from low to high for each variable and constant
in 𝐼 , according to the order they appear in 𝐼 . The assignment of the variables is included in the
variable map Π. For each constant number 𝑐 represented by qubits 𝑞𝑎 ∼ 𝑞𝑏 , QSynth adds expression
𝑥 [𝑏 : 𝑎] = 𝑐 into the hypothesis ℎ. For example, consider the specification for the quantum adder
circuit 𝐼 : |0⟩|𝐴[𝑛]⟩|𝐵 [𝑛]⟩|0𝑛 ⟩, the variable map Π and the hypothesis ℎ generated by QSynth are:
             Π = {𝐴 ↦→ 𝑞 1 ∼ 𝑞𝑛 , 𝐵 ↦→ 𝑞𝑛+1 ∼ 𝑞 2𝑛 },            ℎ = {𝑥 [0] = 0, 𝑥 [3𝑛 : 2𝑛 + 1] = 0}             (4.4)
    Generate 𝛼 from 𝑂 and Π. QSynth will then compute the value 𝛼 (𝑛, 𝑥, 𝑦) from the output 𝑂 and the
variable map Π. QSynth first calculates the number of qubits. Then, it calculates the normalization
factor 𝑘 which is the total number of qubits in the summed variable plus the number of additions.
Then, QSynth evaluates the output into a basis state 𝑒𝑣𝑎𝑙 Π,𝑥,𝑦 (𝑂) by replacing input variables with
slices of 𝑥 according to Π and summed variables with corresponding        √          slices of 𝑦 together with a
phase factor 𝑒 𝑖𝜙 (𝑂,Π,𝑥,𝑦) . Finally, the value of 𝛼 (𝑛, 𝑥, 𝑦) will be 1/ 2𝑘 𝑒 𝑖𝜙 (𝑂,Π,𝑥,𝑦) ·𝛿 (𝑒𝑣𝑎𝑙 Π,𝑥,𝑦 (𝑂) = 𝑦).
If the output contains additions, there will be a basis state and a phase factor for each term and the
𝛼 value will be the sum of their 𝛼. For example, the 𝛼’s of GHZ and QFT in Equation 4.2 are
                                 1                                                         1
                                                                      𝛼𝑄𝐹𝑇 (𝑛, 𝑥, 𝑦) = √ 𝑒 2𝜋𝑖𝑥 ·𝑦/2
                                                                                                         𝑛
           𝛼𝐺𝐻𝑍 (𝑛, 𝑥, 𝑦) = √ 𝛿 (𝑦 = 0 ∨ 𝑦 = 2𝑛+1 − 1),                                                         (4.5)
                                  2                                                        2 𝑛

5     INDUCTIVE SQIR AND ITS LOGIC
QSynth’s goal is to synthesize programs with inductive structures. To that end, we extend the
existing intermediate representation SQIR [Hietala et al. 2021] into a language called Inductive
SQIR (ISQIR) that defines a family of quantum circuits inductively in Section 5.1. In Section 5.2, we
also develop a logic for reasoning about an ISQIR program with respect to an ℎ − 𝛼 specification.

5.1     Inductive SQIR (ISQIR)
We extend SQIR with an inductive structure, similar to fixpoint in Coq, to equip the language
with the ability to describe a family of quantum circuits for general input 𝑛.
    Definition 5.1 (Inductive SQIR- Syntax). An ISQIR program is defined inductively by:

                  𝑆 ::= const P | seq 𝑆 1 𝑆 2 | relabel 𝜋 𝑆 | fix𝑘 𝜋 𝑃 0 𝑃1 · · · 𝑃𝑘 −1 𝑆𝐿 𝑆𝑅 .
Here, 𝑃, 𝑃 0, ..., 𝑃𝑘 −1 are SQIR programs, 𝜋 is a series of injective natural number mappings.
1 Quantum Hoare triples, however, need a post-predicate where the target state spans the subspace with eigenvalue 1, and

the rest space has eigenvalue 0. These complication comes from the generality of quantum Hoare triple.

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
A Case for Synthesis of Recursive Quantum Unitary Programs                                                       59:13


   At a high level, any ISQIR program is a succinct way to describe a series of SQIR programs
indexed by an integer (or input size) 𝑛 = 0, 1, 2, · · · . Intuitively, const P represents a repeating
series of SQIR programs where every entry in the series is the same SQIR program 𝑃. seq 𝑆 1 𝑆 2
concatenates two series 𝑆 1 and 𝑆 2 by concatenating SQIR programs of each entry. We also use 𝑆 1 ; 𝑆 2
and seq 𝑆 1 𝑆 2 interchangeably for notation convenience. relabel 𝜋 𝑆 permutes the qubit labels for
the 𝑛th entry with permutation 𝜋 (𝑛).
   fix𝑘 is the new inductive structure introduced to ISQIR. Specifically, fix𝑘 constructs a series of
SQIR programs by recursion, with 𝑘 base cases 𝑃0, ..., 𝑃𝑘 −1 , and the recursive call for the 𝑛-th entry
is sandwiched by the 𝑛-th entries of ISQIR programs 𝑆𝐿 and 𝑆𝑅 . The choice of fix𝑘 is inspired by
commonly seen quantum programs and serves as a good syntax guide for synthesis purposes for
all the case studies in this paper.
   We formulate the semantics of ISQIR programs as functions from a natural number to a SQIR
program, i.e., N → SQIR.
  Definition 5.2 (ISQIR- Semantics). An ISQIR program represents a series of unitary SQIR pro-
grams {𝑃 0, 𝑃1, ...}. We define the IR semantics {{𝑆 }} of ISQIR program inductively by:
               {{const 𝑃 }}(𝑛) = 𝑃;         {{seq 𝑆1 𝑆2}}(𝑛) = {{𝑆1}}(𝑛); {{𝑆2}}(𝑛);
               {{relabel 𝜋 𝑆 }}(𝑛) = map_qb(𝜋 (𝑛), {{𝑆 }}(𝑛));
                                
                                 𝑃𝑛 ,
                                                                                              𝑛<𝑘
               {{fix𝑘 }}(𝑛) =
                                 {{𝑆 }}(𝑛); map_qb(𝜋 (𝑛), {{fix }}(𝑛 − 1)); {{𝑆 }}(𝑛);
                                 𝐿                             𝑘               𝑅              else
   Here ; is the sequential construct in SQIR, map_qb is a function relabeling the indices of
qubits in a SQIR program according to injective function 𝜋 (𝑛), and fix𝑘 is an abbreviation of
fix𝑘 𝜋 𝑃0 ... 𝑃𝑘 −1 𝑆𝐿 𝑆𝑅 . We use a slightly changed denotational semantics of any SQIR program 𝑃,
denoted [ 𝑃]] , which is an infinite-dimensional matrix (i.e., N2 → C), that returns entries of 𝑃’s
original semantics within 𝑃’s dimension and 0 otherwise.
  Example 5.1. As an example, recall the GHZ program written in ISQIR syntax:
                    fix1 𝐼𝑑 (const H 0) (const ID) (relabel 𝜋 (const CNOT 0 1))
where 𝐼𝑑 is an identity map, (const H 0) is a Hadamard gate on qubit 𝑞 0 which is the 𝑃0 , (const ID)
is an identity unitary (served as 𝑆𝐿 ), and 𝜋 (𝑛) = 𝜆𝑥 .𝑥 + 𝑛 − 1 for 𝑛 ≥ 1. 𝜋 (𝑛) maps the CNOT gate
(served as 𝑆𝑅 ) on qubits 𝑞 0, 𝑞 1 to a CNOT gate on qubit 𝑞𝑛−1, 𝑞𝑛 .
   For notation convenience, when relabeling a SQIR program with a map 𝜋 (i.e. relabel 𝜋 const P),
we usually omit the relabel key word. Thus, 𝑆𝑅 can also be denoted as const CNOT n-1 n.
   We also develop the following syntax for general permutation 𝜋 used in ISQIR programs that is
also part of the candidate program search space.
  Definition 5.3 (Permutation Syntax).
                            𝜋 ::= 𝐼𝑑 | 𝑤 [𝑒 1 ⇌ 𝑒 2 ] | shift 𝑒 1 𝑒 2 𝑚 | 𝜋1 · 𝜋 2
                            𝑒 ::= 𝑛 | 𝑚 | 𝑒 1 + 𝑒 2 | 𝑒 1 − 𝑒 2 | 𝑒 1 ∗ 𝑒 2     𝑚∈N
𝐼𝑑 is an identity permutation; 𝑤 [𝑒 1 ⇌ 𝑒 2 ] swaps the mapping 𝑒 1 and 𝑒 2 . shift 𝑒 1 𝑒 2 𝑚 maps any
𝑥 ∈ [𝑒 1, 𝑒 2 ) to [(𝑥 − 𝑒 1 + 𝑚) mod (𝑒 2 − 𝑒 1 )] + 𝑒 1 ).
 For example, permutation 𝑤 [1 ⇌ 𝑛] (𝑛) maps 1 to 𝑛 and maps 𝑛 to 1. Permutation (shift 2 5 1) (𝑛)
maps 4 to 2, 2 to 3, and 3 to 4.

                                Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
59:14                                                              Haowei Deng, Runzhou Tao, Yuxiang Peng, and Xiaodi Wu


5.2     Unitary ISQIR Logic
We develop unitary ISQIR logic shown in Fig 8 to reason about ISQIR program’s semantics with
respect to the hypothesis-amplitude specification (ℎ, 𝛼) with helper functions in Def 5.4. The
soundness is formally proven in Theorem 5.1, whose proof is postponed to Appendix A.1 in the
supplementary material.
   One can view (ℎ, 𝛼) as a series of incomplete matrices: only those entries in the set ℎ are known,
whose values can be looked up in 𝛼. This gives the intuition behind our rules. The Weaken rule
states that any subset of ℎ can also be observed by 𝛼. The Const rule lifts SQIR semantics to ISQIR
semantics. The Replace rule states that if the observed entries are the same for two amplitude
functions, then one can substitute the other one with hypothesis ℎ. The Relabel rule relabels the
entries of matrices for both ℎ and 𝛼. The Seq rule calculates matrix multiplication for each term in
the series.
   The Fix rule checks observed entries for terms with index 𝑖 < 𝑘 (base cases) and computes matrix
multiplication for 𝑖 ≥ 𝑘 (inductive cases).
    Definition 5.4. For a hypothesis set ℎ and an amplitude function 𝛼,
    the relabeling function and the predecessor functions of ℎ and 𝛼 are defined by
                        𝜋 ◦ (ℎ, 𝛼) := (𝜋 ◦ ℎ, 𝜋 ◦ 𝛼)               pred (ℎ, 𝛼) := (pred ℎ, pred 𝛼)
        𝜋 ◦ ℎ := {(𝑛, 𝜋 (𝑛, 𝑥), 𝜋 (𝑛, 𝑦)) | (𝑛, 𝑥, 𝑦) ∈ ℎ}            (𝜋 ◦ 𝛼) (𝑛, 𝑥, 𝑦) := 𝛼 (𝑛, 𝜋 (𝑛, 𝑥), 𝜋 (𝑛, 𝑦))
               (pred 𝛼) (𝑛, 𝑥, 𝑦) := 𝛼 (𝑛 − 1, 𝑥, 𝑦)             pred ℎ := {(𝑛 − 1, 𝑥, 𝑦) | (𝑛, 𝑥, 𝑦) ∈ ℎ}
The entries of ℎ and 𝛼 are relabeled according to a series of injective function 𝜋. Predecessor functions
move the series by one index, and are used for recursive calls in fixed-point programs.
  The composition function of ℎ and 𝛼 are defined by:
                                   n
      comp(ℎ 1, 𝛼 1, ℎ 2, 𝛼 2 ) := (𝑛, 𝑥, 𝑦) : ∀𝑧, ((𝑛, 𝑥, 𝑧) ∈ ℎ 1 ∧ (𝑛, 𝑧, 𝑦) ∈ ℎ 2 ) ∨
                                                                                                            o
                               ((𝑛, 𝑥, 𝑧) ∈ ℎ 1 ∧ 𝛼 1 (𝑛, 𝑥, 𝑧) = 0) ∨ ((𝑛, 𝑧, 𝑦) ∈ ℎ 2 ∧ 𝛼 2 (𝑛, 𝑧, 𝑦) = 0) ,
                                   ∑︁
         (𝛼 1 ∗ 𝛼 2 ) (𝑛, 𝑥, 𝑦) :=      𝛼 1 (𝑛, 𝑥, 𝑧)𝛼 2 (𝑛, 𝑧, 𝑦),
                                     𝑧 ∈N
         (ℎ 1, 𝛼 1 ) ⊗ (ℎ 2, 𝛼 2 ) := (comp(ℎ 1, 𝛼 1, ℎ 2, 𝛼 2 ), 𝛼 1 ∗ 𝛼 2 ).
    We also define several restricted equivalence relations:
             ℎ 1 ≡𝑛 ℎ 2 ⇔ (∀𝑥, ∀𝑦, (𝑛, 𝑥, 𝑦) ∈ ℎ 1 ↔ (𝑛, 𝑥, 𝑦) ∈ ℎ 2 )
             𝛼 1 ≡ℎ𝑛 𝛼 2 ⇔ ∀𝑥, ∀𝑦, (𝑛, 𝑥, 𝑦) ∈ ℎ → 𝛼 1 (𝑛, 𝑥, 𝑦) = 𝛼 2 (𝑛, 𝑥, 𝑦)
             𝛼 1 ≡ℎ 𝛼 2 ⇔ ∀𝑛, 𝛼 1 ≡ℎ𝑛 𝛼 2,              (ℎ 1, 𝛼 1 ) ≡𝑛 (ℎ 2, 𝛼 2 ) ⇔ ℎ 1 ≡𝑛 ℎ 2 ∧ 𝛼 1 ≡ℎ𝑛1 𝛼 2

    Theorem 5.1. The rules of unitary ISQIR logic in Fig 8 are sound.

6     EFFICIENT ENCODING BY PARAMETERIZED PATH-SUM AMPLITUDE
In this section we explain how to encode the hypothesis-amplitude triple introduced In Definition 4.1
and the functions and relations in Definition 5.4 into the SMT instance.

6.1     Encoding The Hypothesis-amplitude Triple
The hypothesis-amplitude triple in Definition 4.1 includes a hypothesis set ℎ and an amplitude
function 𝛼, which will be encoded separately.

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
A Case for Synthesis of Recursive Quantum Unitary Programs                                                                                 59:15


                                                                                                      3
                   ℎ ⊲ 𝑆 ↔ 𝛼,           ℎ′ ⊆ ℎ                                               𝛼 ≡N 𝜆𝑛.[[𝑃]]
                                                       Weaken                                                          Const
                         ℎ′ ⊲ 𝑆 ↔ 𝛼                                                      N3 ⊲ (const 𝑃) ↔ 𝛼

                  ℎ ⊲ 𝑆 ↔ 𝛼,           𝛼 ≡ℎ 𝛼 ′                                      ℎ ⊲𝑆 ↔𝛼              𝛼 ′ ≡𝜋 ◦ℎ 𝜋 ◦ 𝛼
                                                       Replace                                                              Relabel
                         ℎ ⊲ 𝑆 ↔ 𝛼′                                                   𝜋 ◦ ℎ ⊲ relabel 𝜋 𝑆 ↔ 𝛼 ′

                     ℎ𝑖 ⊲𝑆𝑖 ↔𝛼𝑖 ∀𝑖=1,2                                                ℎ𝐿 ⊲𝑆𝐿 ↔𝛼 𝐿 , ℎ𝑅 ⊲𝑆𝑅 ↔𝛼𝑅
                   (ℎ,𝛼 )=(ℎ 1 ,𝛼 1 ) ⊗ (ℎ 2 ,𝛼 2 )                            ∀𝑖<𝑘, ℎ𝑖 ⊲const 𝑃𝑖 ↔𝛼𝑖 , (ℎ,𝛼 )≡𝑖 (ℎ𝑖 ,𝛼𝑖 )
                                                       Seq                 ∀𝑖 ≥𝑘, (ℎ,𝛼 )≡𝑖 (ℎ𝐿 ,𝛼 𝐿 ) ⊗ (𝜋 ◦pred (ℎ,𝛼 ) ) ⊗ (ℎ𝑅 ,𝛼 𝑅 )
                    ℎ ⊲ seq 𝑆 1 𝑆 2 ↔ 𝛼                                                                                                  Fix
                                                                                    ℎ ⊲ fix𝑘 𝑃0 · · · 𝑃𝑘 −1 𝑆𝐿 𝑆𝑅 ↔ 𝛼

                                                      Fig. 8. The unitary ISQIR logic.


   Encoding the hypothesis set. The hypothesis set ℎ refers to a set of natural numbers. Intuitively,
we encode the hypothesis ℎ with a Boolean expression 𝐵 constructed by 𝑛, 𝑥, 𝑦, whose value is true
if and only if (𝑛, 𝑥, 𝑦) is inside the hypothesis set. Namely,
                                            (𝑛, 𝑥, 𝑦) ∈ ℎ ⇐⇒ 𝐵(𝑛, 𝑥, 𝑦) = True.
   Encoding the amplitude function. Encoding the complex function 𝛼 is challenging since there
is currently no automated program verification tool that supports complex numbers. We solve
this by restricting the function 𝛼 in a limited form that can be encoded into SMT instances. This
is a trade-off between the expressiveness of our specification and the feasibility of automated
verification.
  Parameterized path-sum amplitude (PPSA) function. We restrict an amplitude function 𝛼 to be a
Parameterized Path-Sum Amplitude function:
  Definition 6.1. A Parameterized Path-Sum Amplitude (PPSA) function 𝛼 𝑝 : N3 → C is defined as
                                                               𝑚
                                                          1    ∑︁
                           𝛼 𝑝 (𝑛, 𝑥, 𝑦) := √︁                       𝛿 (𝐵𝑖 (𝑛, 𝑥, 𝑦)) · 𝑒 2𝜋𝑖 ·𝑑 (𝑉𝑖 (𝑛,𝑥,𝑦) )
                                                         𝛽 (𝑛) 𝑖=0
    • 𝛽 is a natural number expression of 𝑛 and it decides the magnitude of all paths.
    • 𝑚 ∈ N is a constant number. {𝐵𝑖 }𝑚 is a group of boolean expressions constructed by (𝑛, 𝑥, 𝑦)
      and satisfies ∀𝑛 𝑥 𝑦 ∈ N, 𝑚 𝑖=0 𝛿 (𝐵𝑖 (𝑛, 𝑥, 𝑦)) ≤ 1, where 𝛿 (𝐵) : Bool → {0, 1} is a function that
                                Í
      returns 1 if 𝐵 is True and returns 0 otherwise.
    • {𝑉𝑖 }𝑚 is a group of natural number expressions constructed by (𝑛, 𝑥, 𝑦).
    • For 𝑥 ∈ N, suppose 𝑥’s binary representation is 𝑥𝑞 ...𝑥 1𝑥 0 where 𝑥𝑖 ∈ {0, 1}, we use 𝑑 (𝑥) to denote
      the fractional binary notation of 𝑥.
                                                                               𝑞
                                                                              ∑︁
                                          𝑑 (𝑥) = [0.𝑥 0𝑥 1 ...𝑥𝑞 ] 2 =             𝑥𝑖 · 2− (𝑖+1) .
                                                                              𝑖=0

   Fig. 9 shows the syntax we allow to construct the expressions 𝛽, 𝐵, 𝑉 in a PPSA function.
"𝑉1 rop 𝑉2 " is a set of common relational operators bewteen 𝑉1, 𝑉2 (e.g. = ≠ > < ≥ ≤). "uop 𝑉 "
is a set of common unary operator on 𝑉 (i.e. - ! & | ⊕). "𝑉1 bop 𝑉2 " is a set of binary operators
between 𝑉1 and 𝑉2 , including arithmetic operators (i.e. + - * \ % ) and bit-wise operators (i.e. & | ⊕ «
»). All these operators have the same meaning as they have in C language. 𝑉1 [𝑉2 ] means the 𝑉2 -th
bit of 𝑉1 ’s binary representation (in the order from low to high). 𝑣 ′ [𝑉1 : 𝑉2 ] is the natural number
represented by the binary representation truncated from high bit 𝑉𝑉′1 to low bit 𝑉𝑉′2 . For example,

                                    Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
59:16                                                                      Haowei Deng, Runzhou Tao, Yuxiang Peng, and Xiaodi Wu


                                   𝑛, 𝑥, 𝑦 : Variables ∈ N               𝑘 : Fixed number ∈ Z
          Boolean Expression 𝐵 ::=             True | False | 𝐵 1 ∧ 𝐵 2 | 𝐵 1 ∨ 𝐵 2 | ¬𝐵 ′ | 𝑉1 rop 𝑉2
                     Binary-N 𝑉 ::=            𝑥 | 𝑦 | 𝑛 | 𝑘 | 𝛿 (𝐵) | 𝑉1 [𝑉2 ] | 𝑉 ′ [𝑉1 : 𝑉2 ] | uop 𝑉 ′ | 𝑉1 bop 𝑉2
                    Magnitude 𝛽 ::=            𝑘 | 𝑛 | 𝛽 1 bop 𝛽 2 | 2𝑛

                                           Fig. 9. Syntax of the PPSA function.
let 𝑉1 = (6)10 = (110)2 , we have 𝑉1 [0] = 0, 𝑉1 [2 : 1] = (11)2 = 3. Z3 SMT solver supports all these
syntaxes.
   By restricting amplitude function 𝛼 to a PPSA function, we disassembled the complex number
function 𝛼 into the combination of several integer or boolean expressions, which allows us to
represent 𝛼 with a set of SMT expressions that enable us to encode the calculation in Definition 5.4
into the SMT solver. This will be discussed in Section 6.2.
   Our design for the PPSA function is inspired by Feynman’s sum-over-path formalism described
in Section 2.4 which has inspired many quantum state representations. However, all of these
representations can only express constant size unitary operators and fail to work for any input size.
PPSA inherits the expressibility of the existing sum-over-path representations, which can express
most famous quantum algorithms (e.g., [Amy 2018; Chareton et al. 2020]), and works for a general
input size. Hence, we believe the restriction to PPSA is mild and serves as a good balance between
expressiveness and feasibility. Some common unitary operators that can be represented by h-𝛼
triple while restricting the amplitude function to PPSA are listed in Table 1. More examples are
provided in Section 7.

                Table 1. Examples of Unitary Operators represented by the H-𝛼 Specification.

             Name                Unitary Operator                                         H-𝛼 Specification
                                                                                         ℎ = {(𝑛, 𝑥, 𝑦)|𝑥 = 0}
                          |0⟩𝑛+1 ↦→ √ 1𝑛+1
                                                  Í
          Uniform𝑛+1
                                           2          0≤𝑦<2𝑛+1 |𝑦⟩                 𝛼 (𝑛, 𝑥, 𝑦) = √ 1𝑛+1 𝛿 (𝑦 < 2𝑛+1 )
                                                                                                    2

                                                                                ℎ = {(𝑛, 𝑥, 𝑦)|𝑥 < 2𝑛+1 ∧ 𝑦 < 2𝑛+1 }
                                     |𝑞 0𝑞 1 · · · 𝑞𝑛 ⟩ ↦→
           Toffoli𝑛+1                               Î                       𝛼 (𝑛, 𝑥, 𝑦) = 𝛿 (𝑥 [𝑛 − 1 : 0] = 𝑦 [𝑛 − 1 : 0]∧
                             |𝑞 0𝑞 1 · · · (𝑞𝑛 ⊕ 𝑛−1   𝑖=0 𝑞𝑖 ))⟩                 𝑦 [𝑛] = 𝑥 [𝑛] ⊕ (&𝑥 [𝑛 − 1 : 0]))

                                                        2𝜋𝑖 ·𝑥 𝑦                     ℎ = {𝑥 < 2𝑛+1 ∧ 𝑦 < 2𝑛+1 }
                            |𝑥⟩ ↦→ √1 𝑛
                                           Í2𝑛 −1
            QFT𝑛+1                              𝑦=0 𝑒
                                                          2𝑛       |𝑦⟩        𝛼 (𝑛, 𝑥, 𝑦) = √ 1𝑛+1 · 𝑒 2𝜋𝑖 ·𝑑 ( (𝑥 ·𝑦)»(𝑛+1) )
                                       2
                                                                                               2



6.2 Encoding Reasoning Based on ISQIR Logic
To enable SMT-based automation in reasoning, one needs to encode the functions and the equiva-
lence relations of ℎ, 𝛼 defined in Definition 5.4 into SMT instances. In the cases of the relabeling
functions (𝜋 ◦ ℎ), (𝜋 ◦ 𝛼), the predecessor function pred (ℎ, 𝛼) and the composition function
comp(ℎ 1, 𝛼 1, ℎ 2, 𝛼 2 ), all used operations are supported by SMT solvers directly and the encoding is
trivial. We hence focus our discussison on the non-trivial encoding of the composition function
𝛼 1 ∗ 𝛼 2 and the equivalence relations.
   Encoding the composition function. Recall the 𝛼 1 ∗ 𝛼 2 function from Definition 5.4:
                                                    ∑︁
                           (𝛼 1 ∗ 𝛼 2 ) (𝑛, 𝑥, 𝑦) =    𝛼 1 (𝑛, 𝑥, 𝑧)𝛼 2 (𝑛, 𝑧, 𝑦).
                                                                    𝑧 ∈N


Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
A Case for Synthesis of Recursive Quantum Unitary Programs                                                     59:17


Since the summation is over 𝑧 ∈ N, by definition, the 𝛼 1 ∗ 𝛼 2 function is a composition of two
infinite-dimension unitaries, and hence cannot be calculated directly.
   All existing symbolic matrix multiplication methods can only deal with a fixed dimension or a
fixed number of terms (e.g., [Amy 2018]) and hence are not applicable in our case.
   Fortunately, we observe that in many cases, non-zero values of the function 𝛼 are sparse,
   making the composition possible. In particular, we show the possibility of computing the function
𝛼 1 ∗ 𝛼 2 when one of 𝛼 1 or 𝛼 2 is sparse. The sparsity of 𝛼 is precisely defined as
  Definition 6.2. We say a function 𝛼 : N3 → C is sparse iff: there exist two functions X, Y :
N2 → {N} and for any inputs, the sets returned by X, Y always have constant sizes (i.e., independent
of inputs 𝑛, 𝑥, 𝑦), and further satisfy
                      ∀𝑛 𝑥 𝑦 ∈ N,      𝛼 (𝑛, 𝑥, 𝑦) ≠ 0 → 𝑥 ∈ X(𝑛, 𝑦) ∧ 𝑦 ∈ Y (𝑛, 𝑥).
We denote such sparsity by 𝛼 ⊴ (X, Y).
  Intuitively, when 𝛼 ⊴ (X, Y) holds, for any given 𝑛 0, 𝑥 0 ∈ N, 𝛼 (𝑛 0, 𝑥 0, 𝑦) has non-zero values
only on a finite of 𝑦 points, the set of which is Y (𝑛 0, 𝑥 0 ). The same intuition holds for X except for
the case when 𝑛 0, 𝑦0 are given.
   Example 6.1. We show the amplitude function that can represent the ISQIR program const H 0 and
its sparsity tuple X, Y as an example.
                                                              1                       𝑥 [0]∗𝑦 [0]
               N3 ⊲ const H 0 ↔ 𝛼 𝐻 ,        𝛼 𝐻 (𝑛, 𝑥, 𝑦) = √ 𝛿 (𝑥\2 = 𝑦\2) · 𝑒 2𝜋𝑖 · 2
                                                               2
               𝛼 𝐻 ⊴ (X, Y),         X(𝑛, 𝑦) = {𝑦, 𝑦 ⊕ 1},       Y (𝑛, 𝑥) = {𝑥, 𝑥 ⊕ 1}.
The operation ⊕ is a bit-wise operation and the expression 𝑥 ⊕ 1 flips the 0th bit of 𝑥 (e.g. (101)2 ⊕ 1 =
(100)2 = 4). The expression 𝛿 (𝑥\2 = 𝑦\2) in 𝛼 𝐻 indicates that
                      ∀𝑛 𝑥 𝑦 ∈ N,      𝛼 𝐻 (𝑛, 𝑥, 𝑦) ≠ 0 → 𝑥 ∈ X(𝑛, 𝑦) ∧ 𝑦 ∈ Y (𝑛, 𝑥)
Intuitively, X, Y are constructed in this way since const H 0 only modifies the 0th qubit.
  Now we explain how to encode 𝛼 function 𝛼 1 ∗ 𝛼 2 when one of 𝛼 1, 𝛼 2 is sparse. Suppose 𝛼 2 is
sparse and we have 𝛼 2 ⊴ (X, Y), we know that 𝛼 2 (𝑛, 𝑧, 𝑦) ≠ 0 only when 𝑧 ∈ X(𝑛, 𝑦). So 𝛼 1 ∗ 𝛼 2
can be calculated by
                                     ∑︁                              ∑︁
            (𝛼 1 ∗ 𝛼 2 ) (𝑛, 𝑥, 𝑦) =    𝛼 1 (𝑛, 𝑥, 𝑧)𝛼 2 (𝑛, 𝑧, 𝑦) =    𝛼 1 (𝑛, 𝑥, 𝑧)𝛼 2 (𝑛, 𝑧, 𝑦).
                                    𝑧 ∈N                           𝑧 ∈ X (𝑛,𝑦)

The summation on the right hand has only a fixed number of terms by sparsity which allows
encoding into SMT instances. Similarly, when 𝛼 1 is sparse and 𝛼 1 ⊴ (X, Y), we have
                                    ∑︁                              ∑︁
           (𝛼 1 ∗ 𝛼 2 ) (𝑛, 𝑥, 𝑦) =    𝛼 1 (𝑛, 𝑥, 𝑧)𝛼 2 (𝑛, 𝑧, 𝑦) =    𝛼 1 (𝑛, 𝑥, 𝑧)𝛼 2 (𝑛, 𝑧, 𝑦).
                                    𝑧 ∈N                           𝑧 ∈ Y (𝑛,𝑥 )

  Moreover, sparsity of 𝛼 can be established in many cases. (Proof in Appendix A.1).
  Theorem 6.1 (𝛼-sparsity). Suppose 𝛼, 𝛼 1, 𝛼 2 are amplitude functions:
    • Let 𝑃 be a unitary SQIR program and N3 ⊲ const P ↔ 𝛼, then 𝛼 is sparse.
    • If 𝛼 is sparse and 𝜋 is a series of injective natural number mappings, then 𝜋 ◦ 𝛼 is sparse.
    • If both 𝛼 1, 𝛼 2 are sparse, so is 𝛼 1 ∗ 𝛼 2 .

                              Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
59:18                                                                 Haowei Deng, Runzhou Tao, Yuxiang Peng, and Xiaodi Wu


   The above theorem shows that the 𝛼 functions for all SQIR programs, and for relabeling a SQIR
program or composing two SQIR programs are sparse. So non-sparse 𝛼s only appear in the fixpoint
syntax. The candidate program from our searcher has at most one fixpoint due to the challenge
discussed in Section 9. So when composing two amplitude functions 𝛼 1, 𝛼 2 , there is always at least
one sparse function and our composition strategy can work.

  Encoding the equivalence relations. Given a hypothesis ℎ and two complex functions 𝛼, 𝛼 ′ , suppose
the functions 𝛼, 𝛼 ′ are in the form:
                                                           𝑚
                                                  1        ∑︁
                             𝛼 (𝑛, 𝑥, 𝑦) = √︁                    𝛿 (𝐵𝑖 (𝑛, 𝑥, 𝑦)) · 𝑒 2𝜋𝑖 ·𝑑 (𝑉𝑖 (𝑛,𝑥,𝑦) )
                                                𝛽 (𝑛) 𝑖=0
                                                           𝑚′
                            ′                   1          ∑︁                                    ′
                          𝛼 (𝑛, 𝑥, 𝑦) = √︁                       𝛿 (𝐵𝑖′ (𝑛, 𝑥, 𝑦)) · 𝑒 2𝜋𝑖 ·𝑑 (𝑉𝑖 (𝑛,𝑥,𝑦) )
                                             𝛽 ′ (𝑛)       𝑖=0



   QSynth verifier checks the equivalence 𝛼 ≡ℎ 𝛼 ′ by the checking following SMT instance and
rejects the equivalence when the SMT solver gives a negative result.

                                                                   𝑚
                                                                   ∑︁                      𝑚′
                                                                                           ∑︁
                                                       ′
         ∀𝑛 𝑥 𝑦 ∈ N, ℎ(𝑛, 𝑥, 𝑦) →𝛽 (𝑛) = 𝛽 (𝑛) ∧                          𝐵𝑖 (𝑛, 𝑥, 𝑦) =         𝐵𝑖′ (𝑛, 𝑥, 𝑦)
                                                                    𝑖=0                    𝑖=0
                                            𝑚
                                            ∑︁                                           𝑚′
                                                                                         ∑︁
                                        ∧           𝐵𝑖 (𝑛, 𝑥, 𝑦) ∗ 𝑉𝑖 (𝑛, 𝑥, 𝑦) =               𝐵𝑖′ (𝑛, 𝑥, 𝑦) ∗ 𝑉𝑖′ (𝑛, 𝑥, 𝑦).
                                            𝑖=0                                           𝑖=0

7     EXPERIMENTAL CASE STUDIES
We demonstrate six additional case studies and provide the output Qiskit programs compiled from
synthesized ISQIR programs for better illustration. Then in Section 7.7, we compare the performance
of QSynth against the previous quantum circuit synthesis frameworks, QFAST [Younis et al. 2021]
and Qsyn [Kang and Oh 2023].

7.1     Quantum Adder
   Motivation and Background. Quantum circuits for arithmetic operations are required for quantum
algorithms. One important example is the adder circuit. Feynman [1985] first proposes the quantum
full adder circuit to implement |0⟩|𝐴⟩|𝐵⟩|0⟩ ⊗𝑛 → |𝑐 0 ⟩|𝐴⟩|𝐵⟩|𝐴 + 𝐵⟩ where 𝐴, 𝐵 are 𝑛-bit natural
number. The first |0⟩ is the carry bit and it is changed to carry value |𝑐 0 ⟩ after the addition. This
design unfortunately needs 𝑛 more qubits to store the sum of 𝐴 + 𝐵. To reduce the qubit usage,
Cuccaro et al. [2004] proposed a new ripple-carry adder that
   uses 𝑛 fewer qubits than the full adder design. When given different specifications, QSynth can
synthesize both adder circuits.

   Full Adder Synthesis. We let QSynth synthesize a program 𝑆𝑎 that 𝑆𝑎 (𝑛) provides a 𝑛-qubit full
quantum adder (i.e. 𝑆𝑎 (0) is an identity unitary) with the specification in Equation 4.1. QSynth
generates a program 𝑆𝑎 as shown in Fig 10(a)(c) (i.e. Qiskit function full_adder). When 𝑛 = 0,
𝑆𝑎 does nothing since the circuit only contains the carry bit. When 𝑛 ≥ 1, 𝑆𝑎 first call 𝑆𝑎 (𝑛 − 1)
recursively to get a 𝑛 − 1-bit full adder to calculate |𝐴𝑛−1 + 𝐵𝑛−1 ⟩ and the carry bit is stored in qubit
0. Then 𝑆𝑎 uses the one-bit adder circuit 𝑆𝑅 to sum the highest bit in 𝐴𝑛 and 𝐵𝑛 .

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
 A Case for Synthesis of Recursive Quantum Unitary Programs                                                                              59:19


                                                                          def Cuccaro_adder ( N ) :
          def full_adder (N) :
                                                                              circuit = QuantumCircuit (2* N +1)
              circuit = QuantumCircuit (3 N +1)
                                                                              def S ( circ , n ) :
              def Sa ( circ , n ) :
                                                                                    if n ==0:
                    if n ==0:
                                                                                         return
                         return
                                                                                    else :
                    else :
                                                                                         # MAJ
                         Sa ( circ ,n -1)
                                                                                         circ . cx (N - n +1 ,2* N - n +1)
                         # See the circuit SR below
                                                                                         circ . cx (N - n +1 ,N - n )
                         circ . ccx (n , N +n , 2 N + n )
                                                                                         circ . ccx (N -n ,2* N - n +1 ,N - n +1)
                         circ . cx (n , N + n )
                                                                                         S ( circ ,n -1)
                         circ . ccx ( N +n , 0 , 2 N + n )
                                                                                         # UMA
                         circ . cx ( N +n , 0)
                                                                                         circ . ccx (N -n ,2* N - n +1 ,N - n +1)
                         circ . cx (n , N + n )
                                                                                         circ . cx (N - n +1 ,N - n )
                         circ . swap (0 , 2 N + n )
                                                                                         circ . cx (N -n ,2* N - n +1)
              Sa ( circuit ,N)
                                                                              S ( circuit , N )
              return circuit
                                                                              return circuit


                                     (a)
                                                                                                            (b)
                                           0 = 𝑞0                                                                                   0
                                              𝐴1       𝑀𝐴𝐽                                                           𝑈 𝑀𝐴           𝐴1
                       𝑆𝑅                      𝐵1                                                                                   𝑆1
    𝑞𝑛        •   •              •            𝐴2               𝑀𝐴𝐽                                            𝑈 𝑀𝐴                  𝐴2
 𝑞 𝑁 +𝑛       •        •     •                 𝐵2
                                                         ..                                                           ..
                                                                                                                                    𝑆2
                                                                                                        .
                                                          .
                                                                     ..
                                                                          .   𝑆𝑐 (𝑛 − 1)            ..                 .
    𝑞0                 •         ×           𝐵𝑛−1                                                                                   𝑆𝑛−1
𝑞 2𝑁 +𝑛                          ×            𝐴𝑛                                𝑀𝐴𝐽        𝑈 𝑀𝐴                                     𝐴𝑛
                                               𝐵𝑛                                                                                   𝑆𝑛
                       (c)
                                                                                                  (d)
 Fig. 10. (a)(c) Full quantum adder program 𝑆𝑎 written in Qiskit. circ.ccx(a,b,c) means appending a Toffoli
 gate that controlled by qubit 𝑞𝑎 , 𝑞𝑏 on qubit 𝑞𝑐 to the circuit circ. The circuit 𝑆𝑅 is exactly a one-bit quantum
 full adder circuit. (b)(d) Cuccaro’s quantum ripple-carry adder program written in Qiskit language.



   Cuccaro’s Adder Synthesis. To reduce the number of qubits in the circuit, we want to synthesize
 an in-place adder. The specification is given as:

                                                    |0⟩|𝐴[𝑛]⟩|𝐵 [𝑛]⟩ ↦→ |𝑐 0 ⟩|𝐴⟩|𝐴 + 𝐵⟩                                                 (7.1)

  With this specification, QSynth generates program 𝑆𝑐 shown in Fig 10(b)(d). We use Cuccaro’s
 MAJ and UMA circuit structures as predefined modules in the synthesis. QSynth flattens these two
 modules in the compilation process.

 7.2        Quantum Subtractor
 Another important quantum arithmetic operation is the quantum subtractor. A classical 𝑛-bit
 subtractor is usually implemented based on the two’s complement theory (i.e. 𝐵 − 𝐴 = 𝐵 + 𝐴¯ + 1
 where 𝐴¯ flips each bit in 𝐴), which is also used by many existing quantum libraries (e.g. QLib [Lin
 et al. 2014],QPanda [Dou et al. 2022]). However, this method requires additional ancilla qubits to
 build the "+1" operation. To reduce the qubit usage, we let QSynth synthesize a 𝑛-bit subtractor
 using the same number of qubits in the 𝑛-bit ripple adder.

     Synthesis with QSynth. We let QSynth synthesize a program with the specification below.

                                           Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
59:20                                                           Haowei Deng, Runzhou Tao, Yuxiang Peng, and Xiaodi Wu


      def RippleSubtractor ( N ) :
          circuit = QuantumCircuit (2* N +1)                     def ConditionalAdder ( N ) :
          def S( circ , n ) :                                        circ = QuantumCircuit (2* N +2)
               if (n ==0) :                                          def S ( circ , n ) :
                     circ . id (0)                                         if ( n ==0) :
               else :                                                             circ . id (0)
                     circ . x (2* N - n +1)                                else :
                     circ . cx (N - n +1 ,2* N - n +1)                            circ . ccx (0 ,N - n +2 ,2* N - n +2)
                     circ . cx (N - n +1 ,0)                                      circ . ccx (0 , N - n +2 ,N - n +1)
                     circ . ccx (0 ,2* N - n +1 ,N - n +1)                        circ . ccx (N - n +1 ,2* N - n +2 ,N - n +2)
                     S( circ ,n -1)                                               S ( circ ,n -1)
                     circ . ccx (0 ,2* N - n +1 ,N - n +1)                        circ . ccx (N - n +1 ,2* N - n +2 ,N - n +2)
                     circ . cx (N - n +1 ,0)                                      circ . ccx (0 ,N - n +2 ,N - n +1)
                     circ . cx (0 ,2* N - n +1)                                   circ . ccx (0 ,N - n +2 ,2* N - n +2)
                     circ . x (2* N - n +1)                          S ( circuit , N )
          S( circuit ,N)                                             return circuit
          return circuit

                                                                Fig. 12. 𝑁 -bit conditional adder program written
   Fig. 11. 𝑁 -bit ripple subtractor program written            in Qiskit language.
   in Qiskit language.




                                             |0⟩|𝐴[𝑛]⟩|𝐵 [𝑛]⟩ ↦→ |𝑐 0 ⟩|𝐴⟩|𝐵 − 𝐴⟩
This specification is similar to the specification for Cuccaro’s Adder (Equation 7.1) except for
changing 𝐵 + 𝐴 to 𝐵 − 𝐴. With this specification, QSynth generates the program shown in Fig 11.
This program equals to the circuit shown in Fig 13, indicating the logical expression 𝐵 − 𝐴 = 𝐵¯ + 𝐴,
which is different from the traditional subtractor implementation. This subtractor generated by
QSynth uses no ancilla qubits and saves quantum resources.

7.3      Quantum Conditional Adder
   Motivation and Background. Quantum Conditional Adder is a necessary arithmetic operation
for many known quantum algorithms, including quantum multiplier and Thapliyal et al. [2019]’s
quantum long division algorithm. A 𝑛-bit Quantum conditional adder circuit implements the
transformation |𝑐𝑡𝑟𝑙⟩|0⟩|𝐴⟩|𝐵⟩ ↦→ |𝑐𝑡𝑟𝑙⟩|𝑐𝑡𝑟𝑙 ∗ 𝑐0⟩|𝐴⟩|𝑐𝑡𝑟𝑙 ∗ 𝐴 + 𝐵⟩. It sums 𝐴𝑛 and 𝐵𝑛 when the
control qubit |𝑐𝑡𝑟𝑙⟩ is in state |1⟩ and keeps the state unchanged when |𝑐𝑡𝑟𝑙⟩ is in state |0⟩.
   One way to construct such a program is by replacing each gate in Cuccaro’s adder program (i.e.,
the program in Fig 10(b)) with its conditional version, which is also the circuit generated by Qiskit.
However, this method needs four-qubit Toffoli gates, which needs 14 CNOT gates to implement,
increasing the total count of CNOT gates in the decomposed circuit. We let QSynth synthesize a
target program using only X gate, CNOT gate, and Toffoli gate to find a better solution.
   Synthesis with QSynth. We let QSynth synthesize a program with the specification below
                                 |𝑓 [1]⟩|0⟩|𝐴[𝑛]⟩|𝐵 [𝑛]⟩ ↦→ |𝑓 ⟩|𝑓 ∗ 𝑐 0 ⟩|𝐴⟩|𝑓 ∗ 𝐴 + 𝐵⟩
The term 𝑓 ∗ 𝐴 + 𝐵 indicates qubit 𝑞 0 is the flag qubit. With this specification, QSynth generates
program 𝑆 shown in Fig 12. We compare the resource count between the conditional adder circuits
generated by QSynth and Qiskit, which is shown in Fig 14. All circuits are decomposed with
{𝑢 3, 𝐶𝑁𝑂𝑇 } gateset by Qiskit’s decomposition pass for comparison, where 𝑢 3 is a generic single-
qubit rotation gate. The conditional adder programs generated by QSynth always use fewer quantum
resources compared to the one from Qiskit.

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
A Case for Synthesis of Recursive Quantum Unitary Programs                                                      59:21


                                                                          QSynth          Qiskit
             |a1 ⟩                              |a1 ⟩          Qubit
                                                                         𝑢 3 cnot       𝑢 3 cnot
             |b1 ⟩                              |s1 ⟩
             |a2 ⟩                              |a2 ⟩             4      182    144     244    208
                          n-qubit
             |b2 ⟩        Ripple                |s2 ⟩             5      228    180     305    260
                ..        Adder            ..                     6      274    216     366    312
                 .                          .
            |an ⟩                               |an ⟩             7      320    252     427    364
            |bn ⟩                               |sn ⟩
                                                        Fig. 14. Comparison of resource count be-
                                                        tween the conditional adder circuit generated
          Fig. 13. 𝑁 -bit ripple subtractor circuit     by QSynth and Qiskit.




7.4   Eigenvalue Inversion
   Background and Motivation. Eigenvalue inversion is a necessary arithmetic step in HHL[Lloyd
2010], a quantum algorithm for linear systems of equations. Given a 𝑐-qubit eigenvalue state |𝜆⟩,
the eigenvalue inversion circuit needs to calculate |1/𝜆⟩. In practice, only the first 𝑛 decimal places
of the 1/𝜆, denoted as 𝑑𝑛 , and the remainder 𝑟 0 are kept. The precision 𝑛 depends on the accuracy
requirement of the algorithm.

  Synthesis with QSynth. We let QSynth synthesize a program that can calculate the first 𝑛 decimal
places of 1/𝜆 and keep the remainder 𝑟 0 for further use.
  Since QSynth’s specification syntax only supports binary integers, we use the fact 2𝑛 = 𝜆 ∗𝑑𝑛 +𝑟 0
where 𝑑𝑛 is the quotient we want to give the specification. The example below shows our intuition.

      Base 10:        1/7 = 0.14285714... ⇔ 106 /7 = 142857.14...                ⇔106 = 142857 ∗ 7 + 𝑟 0
      Base 2:        1/7 = 0.001001001... ⇔ 26 /7 = 001001.001...                ⇔26 = (001001)2 ∗ 7 + 𝑟 0

The specification we send to QSynth for the 𝑛-bit precision eigenvalue inversion program is

                             |0⟩|Λ[𝑐]⟩|0𝑛 ⟩|1⟩|0𝑐 −1 ⟩ ↦→ |0⟩|Λ⟩|2𝑛 %Λ⟩𝑐 |2𝑛 /Λ⟩

The specification uses Λ[𝑐] to represent the signed input 𝑐-bit eigenvalue 𝜆. It suggests qubit
𝑞𝑐+1 ∼ 𝑞 2𝑐 store the remainder (i.e. |2𝑛 %Λ⟩) and qubit 𝑞 2𝑐+1 ∼ 𝑞 2𝑐+𝑛 store the quotient (i.e. |2𝑛 /Λ⟩).
  With this specification, QSynth generates the program shown in Fig 15. Fig 16 shows the
corresponding circuit for 𝑛 = 3, 𝑐 = 3. This program is a variant of Thapliyal [Thapliyal et al. 2019]’s
general quantum division circuit. Compared to calculating |1/𝜆⟩ with Thapliyal’s division circuit,
which is constructed by 𝑚𝑎𝑥 (𝑛, 𝑐)-qubit subtractor and conditional adder, this program uses 𝑐-qubit
one. This significantly reduces the number of qubits required when 𝑛 is large.

7.5   Quantum Fourier Transform
   Motivation and Background. Quantum Fourier Transform (QFT) [Coppersmith 2002] is the classi-
cal discrete Fourier Transform applied to the vector of amplitudes of a quantum state. QFT is a part
of many quantum algorithms, notably Shor’s algorithm [Shor 1994], QPE algorithm [Kitaev 1995],
and algorithms for the hidden subgroup problem [Ettinger and Hoyer 1999]. A QFT over Z2𝑛 can

                               Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
59:22                                                                Haowei Deng, Runzhou Tao, Yuxiang Peng, and Xiaodi Wu


  def inversion (N):
    circ = QuantumCircuit ( N +2* c +1)
    def S( circ , n):                                    Λq[3:0]                                                           |Λ⟩
      if n <1:
                                                             |q4 ⟩                                                     A   |R0 ⟩
         pass
                                                                                                                 S     D
      else :                                                 |q5 ⟩                                       A       U     D   |R1 ⟩
         Append ( circ , SUB ( c ) ,0 ,1 , c + n +1)                                               S     D       B
         Append ( circ , C_ADD (c -1) ,                      |q6 ⟩                      A          U     D                 |D0 ⟩
           2* c+n ,c ,c+ n )                                                      S     D          B
                                                             |q7 ⟩       A        U     D                                  |D1 ⟩
         circ .x (2* c+n )                                           S   D        B
         circ =S( circ ,n -1)                                |q8 ⟩   U   D                                                 |D2 ⟩
      return circ                                                    B
    circ =S( circ ,N)                                        |q9 ⟩                                                         |D3 ⟩
    return circ

                                                             Fig. 16. Eigenvalue inversion circuit for 𝑛 = 3, 𝑐 = 3.
  Fig. 15. 𝑁 -bit precision eigenvalue inver-
  sion program.


be expressed as a map in two equivalent forms:
                                          2𝑛 −1                                                          𝑛−1
                                      1 ∑︁ 2𝜋𝑖𝑛·𝑥 𝑦                                                      Ì
                         QFT: |𝑥⟩ ↦→ √          𝑒 2 |𝑦⟩                   OR          QFT: |𝑥⟩ ↦→              |𝑧𝑘 ⟩         (7.2)
                                       2𝑛 𝑦=0                                                            𝑘=0
                                                                                                   𝑚
                           1                                                                       ∑︁      𝑥𝑘
                  |𝑧𝑘 ⟩ = √ (|0⟩ + 𝑒 2𝜋𝑖 · [0.𝑥𝑘 𝑥𝑘 −1 ...𝑥 0 ] |1⟩),        [0.𝑥𝑚 ...𝑥 1𝑥 0 ] =                .            (7.3)
                            2                                                                      𝑘=0
                                                                                                         2𝑚−𝑘+1


   Synthesis with QSynth. We use the specification in Equation 4.2 to synthesize a program 𝑆𝑄 that
𝑆𝑄 (𝑛) returns the 𝑛 + 1-qubit QFT circuit.
   QSynth fails to synthesize a simple fixpoint structure QFT circuit. Therefore we synthesize it
in two steps to help QSynth synthesize a nested structure circuit. First, we let the synthesizer
generate a program 𝑆𝑧 that transforms the state of qubit 𝑛 into state |𝑧𝑛 ⟩ and keep the state of
qubits 𝑞 0 ∼ 𝑞𝑛−1 unchanged. The specification is:
                                                                                      2𝜋𝑖 ·𝑋
                                 |𝑋 [𝑛 + 1]⟩ ↦→ |𝑋 0𝑋 1 ...𝑋𝑛−1 ⟩ ⊗ (|0⟩ ⊎ 𝑒 2𝑛 · |1⟩)
  With this specification, the synthesizer generates the program as shown in Fig 17. Statement
circ.cp(pi/2**n, N-n, N) in Qiskit means a controlled phase rotation gate 𝑅𝑛 2 on qubit 𝑞 𝑁
controlled by qubit 𝑞 𝑁 −𝑛 .
  Then we insert this ISQIR program 𝑆𝑧 (i.e. Qiskit program Zn) into the database so QSynth can
use it for further synthesis, which leads to the QFT program in Fig 18.

7.6 𝑛-qubit Quantum Teleportation
   Motivation and Background. Quantum teleportation[Bennett et al. 1993] is one of the most famous
quantum applications that can be implemented in the near term. It is a technique for transferring
quantum information from a sender at one location to a receiver some distance away. The sender
does not have to know the particular quantum state being transferred. Moreover, the recipient’s
location can be unknown, but to complete the quantum teleportation, classical information needs to
be sent from sender to receiver. The right-hand side circuit shows the process for sending one-qubit
state |𝜙⟩ from Alice to Bob.
                                                   !
2 Precisely, 𝑅 is a single-qubit unitary    1    0
              𝑛                                      where 𝜔𝑛 = 𝑒𝑥𝑝 (2𝜋𝑖/2𝑛 ).
                                            0   𝜔𝑛



Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
A Case for Synthesis of Recursive Quantum Unitary Programs                                                              59:23


      def Zn (N):
          circ = QuantumCircuit ( N +1)
          def S( circ , n ) :                                      |𝑥𝑛 ⟩      𝐻       𝑅2      𝑅3      ···      𝑅𝑛
               if n == 0:
                    circ . h ( N )                              |𝑥𝑛−1 ⟩                •              ···
               else :                                           |𝑥𝑛−2 ⟩                        •      ···
                    S( circ ,n -1)
                                                                        ..                            ..
                                                                         .                               .
                    circ . cp ( pi /2** n , N -n , N )
          S( circ ,N)                                              |𝑥 0 ⟩                                      •
          return circ


                        Fig. 17. Qiskit program Zn that transforms qubit 𝑞𝑛 to state |𝑧𝑛 ⟩


                                                                        def teleport ( N ) :
                                                                            circuit = QuantumCircuit (3* N )
      def QFT (N):
                                                                            def S ( circ , n ) :
          circuit = QuantumCircuit ( N +1)
                                                                                  if (n <0) :
          def S( circ , n ) :
                                                                                        return
               if n == 0:
                                                                                  else :
                    circ . h ( n )
                                                                                        circ . h ( N + n )
               else :
                                                                                        circ . cx ( N +n , 2* N + n )
                    circ . append ( Zn ( n ) )
                                                                                        circ . cx (n , N + n )
                    S( circ , n -1)
                                                                                        circ . h ( n )
          S( circuit , N )
                                                                                        S ( circ ,n -1)
          return circuit
                                                                            S ( circuit , N )
                                                                            return circuit
      Fig. 18. 𝑁 + 1-bit QFT program written in
      Qiskit language.                                                  Fig. 19. 𝑁 -qubit quantum teleportation pro-
                                                                        gram.


   Synthesis with QSynth. We let QSynth synthesize the A : ψ                                • H    •
unitary circuit part (before the measurement) of the 𝑛-
qubit quantum teleportation process. Suggest Alice wants A : 0
to send a state |𝜙𝑛 ⟩ stored in 𝑛 data qubits to Bob, and B : 0              H       •          X  Z    ψ
they each have 𝑛 more ancilla qubits which are initialized
to state |0⟩𝑛 for the teleportation process. We follow the
same measurement strategy as the one-qubit teleportation: Alice will measure |𝜙𝑛 ⟩ and Alice’s 𝑛
aniclla qubits after the unitary circuit, then Bob apply bit-wise CZ and CX gate to Bob’s 𝑛 ancilla
qubits based on the result. Assume the data qubits, Alice’s ancilla qubits and Bob’s ancilla qubits
are in state |𝑎𝑛 ⟩, |𝑏𝑛 ⟩, |𝑐𝑛 ⟩ respectively after the measurement, Bob can use bit-wise CZ and CX
gate to reproduce the state |𝜙𝑛 ⟩ if (−1) ⊕𝑎𝑛 (|𝑏𝑛 ⟩ ⊕ |𝑐𝑛 ⟩) = |𝜙𝑛 ⟩. Here |𝑏𝑛 ⟩ ⊕ |𝑐𝑛 ⟩ is bit-wise XOR
operation (e.g. |101⟩ ⊕ (|100⟩ + |110⟩) = |001⟩ + |011⟩) and ⊕𝑎𝑛 is a reduction XOR operation on
𝑎𝑛 (e.g. ⊕101 = 1 ⊕ 0 ⊕ 1 = 0). With this intuition, we let QSynth use the specification below to
synthesize the unitary circuit part of a 𝑛-qubit quantum teleportation program,
                                                Ú
                         |𝜙 [𝑛]⟩|0𝑛 ⟩|0𝑛 ⟩ ↦→         𝛿 (𝜙 = 𝑏𝑛 ⊕ 𝑐𝑛 ) · 𝑒 −𝜋𝑖 · (⊕𝑎𝑛 ) |𝑧⟩
                                                 𝑧 ∈ {0,1} 3𝑛

where 𝑎𝑛 = 𝑧 [𝑛 − 1 : 0], 𝑏𝑛 = 𝑧 [2𝑛 − 1 : 𝑛], 𝑐𝑛 = 𝑧 [3𝑛 − 1, 2𝑛]. Fig 19 shows the program generated
by QSynth.

7.7   Performance Evaluation
In this section, we compare the performance of QSynth and previous circuit synthesis methods.

                                 Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
59:24                                                        Haowei Deng, Runzhou Tao, Yuxiang Peng, and Xiaodi Wu


   Implementation. In the experiment, we use the Syntax-Guided Top-down Tree Search [Gulwani
et al. 2017] as the searcher with the following bounds on the search space: (1) when searching a
candidate program under ISQIR syntax in Definition 5.1, we set the maximum program length to
10 and enumerate the value of 𝑘 in the FIX syntax in {1, 2, 3}; (2) shorter candidate programs are
sent to the verifier first; (3) when searching a permutation 𝜋 under the syntax in Definition 5.3, we
set the maximum syntax derivation depth to 4; (4) when deriving the syntax rule 𝑒 ::= 𝑚, 𝑚 ∈ N,
we enumerate 𝑚 ∈ [0, 3]. All benchmarks in this paper can be synthesized under these bounds.
   The implementation of QSynth uses 1k lines of Python. All the experiments are run with Z3
solver version 4.8.9 and Python 3.8.
   Benchmarks. Table 2 summarizes all 10 benchmarks. They are in three categories: arithmetic
circuits, state preparation and sub-programs widely used in quantum algorithms. Many benchmarks
are collected from textbooks [Nielsen and Chuang 2010]. Arithmetic circuits are frequently used in
quantum oracle designs which is necessary for most famous quantum algorithms (e.g. Simons, Shor’s
algorithms, Grover search algorithm). State preparation is necessary for the setup of many quantum
applications (e.g. quantum teleportation). We also collect the necessary quantum sub-program used
in quantum algorithms from their paper (e.g. HHL algorithm).

                          Table 2. Summary of all benchmarks used in the evaluation.

        Benchmark Benchmark                             Description                          Gate Set
          Type      Name
                         n-GHZ                Greenberger–Horne–Zeilinger                      H,CX
           State                               state [Greenberger et al. 1989]
        Preparation
                       n-Uniform             𝑛-qubit uniform distribution state              H, X, Y, Z
                       n-full-Add                     𝑛-qubit full adder                  QFT, CX, SWAP,
                                                                                              CCX, X
                          n-Add                    𝑛-qubit in place adder                 MAJ, UMA, QFT,
        Arithmetic                                                                           CS, CZ, X
                          n-Sub                  𝑛-qubit in place subtractor              MAJ, UMA, QFT,
                                                                                             CS, CZ, X
                      Cond n-Add             𝑛-qubit conditional in place adder           Toffoli, QFT, CX,
                                                                                             CS, CZ, X
                          n-QFT           𝑛-qubit Quantum Fourier Transform               H,CS,CT, SW AP
                        Inversion       𝑛-qubit precision eigenvalue inversion for            c-adder,
        Algorithm
                                              HHL algorithm [Lloyd 2010]                    subtractor,X
         Module
                          n-Toff                   𝑛-qubit Toffoli gate                    Toffoli, CX, X
                        n-Teleport           𝑛-qubit quantum teleportation                     H, CX

  We compare the performance of QSynth against QFAST [Younis et al. 2021] and Qsyn [Kang and
Oh 2023]. For QSynth, we use input-output style specification written in QSynth-spec as input. For
the other two frameworks, we use their specification interfaces and try to synthesize circuits with
𝑛 = 3, 4, 5, 6. We use the same gate set when comparing QSynth and Qsyn in each case, while for
QFast we use its hard-coded gate set.
  We stop the synthesis and regard the synthesis as a failure if the running time is over 1 hour. All
runtimes are a median of three runs.
  Table 3 shows the running time of all the experiments. We can see that QSynth successfully
synthesizes programs in all 10 benchmarks in at most 5 minutes, while QFAST and Qsyn fail to

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
A Case for Synthesis of Recursive Quantum Unitary Programs                                                       59:25


                      Table 3. Running time of all benchmarks used in the evaluation.

                Benchmark         QSynth            QFAST time (s)                Qsyn time (s)
                  Name            time (s)      3       4     5        6      3       4      5      6
                   n-GHZ           1.793      0.122    2.48    59.1    -*   0.091    1.33   49.2    -*
                 n-Uniform         0.415      0.027    1.25    32.7    -*   0.096    1.40   39.8    -*
                n-Full-Add         288.1       617       -*      -*    -*   812.4      -*    -*     -*
                   n-Add           170.4       942     3511      -*    -*    132     2818    -*     -*
                   n-Sub           168.6       667       -*      -*    -*    287     3240    -*     -*
                Cond n-Add         185.2       851       -*      -*    -*    192     1804    -*     -*
                   n-Toff           66.7      <0.01    21.8     679    -*   <0.01    16.5   354     -*
                   n-QFT           145.49      21.4     397    3598    -*    67.2     473    -*     -*
                 Inversion          93.5      1622       -*      -*    -*    22.5     740    -*     -*
                 n-Teleport        185.1       897       -*      -*    -*    614       -*    -*     -*
               * Time out after 1 hour.


synthesize circuits for 𝑛 = 6. From the result, we can see that when the size increases, the time of
QFAST and Qsyn indeed grow exponentially, while QSynth only pays a fixed cost for all sizes.
   The synthesis time of QSynth is comparable to the time to synthesize a corresponding circuit with
size 3, with an exception of the n-Toff benchmark. We note that this is because 3-Toffoli is exactly a
single Toffoli gate and 4-Toffoli can be done using two Toffoli gates, which are straightforward
for QFAST and Qsyn to search. In contrast, QSynth’s search is longer because it needs to consider
the inductive structure and corner cases of 𝑛 = 1 and 2. Nevertheless, QSynth quickly outperforms
other frameworks on n-Toff at 𝑛 = 5.

8   RELATED WORK
   Synthesis of quantum circuits. Many methods have been proposed to synthesis quantum circuits
of a fixed size [Amy et al. 2013; de Brugiere 2020; Deng et al. 2023a; Kang and Oh 2023; Kitaev
1997; Saeedi et al. 2011; Shende et al. 2006; Xu et al. 2023; Younis et al. 2021]. These methods do not
consider the inductive structure of quantum programs and do not scale due to their exponential
blowup with the number of qubits.
   Synthesis of classical programs. The tasks of synthesizing classical programs are intensively-
studied in the recent decades [Gulwani et al. 2017; Kitzelmann 2009]. The problem definitions of
program synthesis are diverse and orienting, including syntax-guided synthesis [Alur et al. 2013,
2018; Hu and D’Antoni 2018; Jha et al. 2010], example-guided synthesis [Gulwani 2011; Gulwani
et al. 2012; Polozov and Gulwani 2015], semantics-guided synthesis [D’Antoni et al. 2021; Kim et al.
2021], and resource-guided synthesis [Hu et al. 2021; Knoth et al. 2019]. The modern approaches to
solve these problems make use of sophisticated search algorithms, such as enumerative search with
pruning [Gulwani et al. 2011; Phothilimthana et al. 2016], constraint solver like satisfiability modulo
theory (SMT) solver [Feng et al. 2017; Jha et al. 2010; Solar-Lezama 2008], and machine learning
[Liang et al. 2010; Menon et al. 2013]. We refer curious readers to surveys [Gulwani et al. 2017;
Kitzelmann 2009] for a comprehensive picture on the development of classical program synthesis
techniques. Many synthesis frameworks are developed into productive tools. For example, the
Sketch [Solar-Lezama 2008] framework completes programs with holes by specifications. Rosette
[Torlak and Bodik 2013] builds solvers into the language to automatically fill in holes when
programming. However, QSynth needs to deal with unique challenges from quantum programs.

                                Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
59:26                                                        Haowei Deng, Runzhou Tao, Yuxiang Peng, and Xiaodi Wu


   Verification of quantum programs. An important procedure in syntax-guided synthesis is to verify
any candidate program. Various logic and verification tools for quantum programs are developed in
the last decade. QWIRE [Paykin et al. 2017] embedded the formal verification of quantum programs
manually in the Coq proof assistant. QBricks [Chareton et al. 2020] do formal verification of
quantum programs semi-manually using Why3. Quantum abstract interpretation [Yu and Palsberg
2021] provides efficient tools to test the properties of quantum programs. In particular, the path-
sum representation [Amy 2018] of quantum program semantics inspired our representation. Chen
et al. [2023] uses tree automaton to verify fixed-size quantum circuits. It is hard to generalize to
general-size cases because graphical structures like automaton are hard to symbolically model in
SMT solvers.
   Quantum Hoare logic [Ying 2012] uses quantum predicates and Hoare triples to express and
derive properties of quantum programs. Its language, quantum while language does not have
the detailed structure of unitary executions. Its specifications are quantum predicate matrices.
Therefore, it cannot be applied to synthesize quantum unitary circuit families.
   The use of SMT solvers to automate the reasoning has also appeared in Giallar [Tao et al. 2022],
Quartz [Xu et al. 2022] and symQV [Bauer-Marquart et al. 2023], although they only work on
quantum circuit compilation passes, quantum circuit optimizations or fixed-size quantum circuit
verification.


9   DISCUSSION AND FUTURE WORKS
QSynth comes with several limitations. At a high level, QSynth sacrifices the expressiveness of
the specification due to the limitation in efficient SMT encodings. For example, the lack of the
equivalence verification of general complex functions forces us to consider the special form of
amplitude in Definition 6.1. The sparsity requirement of 𝛼 is another such restriction. Any relief of
such restrictions would enlarge the space of programs that can be synthesized by QSynth.
   Another limitation is that QSynth cannot directly synthesize programs involving nested fixed-
point structures. Synthesizing a program nested loop or fixed-point structure is also a challenging
problem in the classical domain. This is because the loop invariant of the program in nested loop
structures is unknown and usually non-trivial to figure out. So we make the current QSynth only
expand the FIX syntax at most once when generating the candidate program and avoid directly
sending a program in nested fixed-point structure to the QSynth verifier. A natural next step is to
include the search for the loop invariant in nested loop structures as part of QSynth, and to verify
the candidate program against both the specification and the generated loop invariant.
   Many quantum algorithms such as Bernstein-Vazirani [Bernstein and Vazirani 1997] and Deustch-
Jozsa [Deutsch and Jozsa 1992] have quantum oracle as part of the program. However, it is hard
to synthesize and verify quantum programs with oracles because it requires higher-order logic
to quantify over arbitrary oracles. It is also an interesting next step to extend QSynth to support
quantum oracles.
   The design of ISQIR inherits concrete qubit indices from SQIR. This design introduces complica-
tions in the inductive variant that have to be addressed with explicit permutations and relabelings.
We will explore the possibility of using a different representation of variables to make synthesis
less complicated in the future.
   Besides extending the expressiveness of specification and the support of more complicated
quantum programs, it is also interesting to improve the synthesis performance by integrating
classical program synthesis techniques into the quantum domain, including counterexample-guided
synthesis, and various search heuristics.


Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
A Case for Synthesis of Recursive Quantum Unitary Programs                                                             59:27


10    CONCLUSION
We present QSynth, the first quantum program synthesis framework, including a new inductive
quantum programming language, its specification, a sound logic for reasoning, and an encoding
of the reasoning procedure into SMT instances. By leveraging existing SMT solvers, QSynth
successfully synthesizes seven quantum unitary programs and QSynth can generate programs
better than the standard solutions in the quantum subtractor and quantum conditional adder cases.
These programs can be readily transpiled to executable programs on major quantum platforms,
e.g., Q#, IBM Qiskit.
   QSynth constitutes the first step toward a fully automated quantum program synthesis framework,
which can significantly ease the task of programming in dealing with the low-level details, and
hence leave the human programmers to focus on the high-level design of the system.

ACKNOWLEDGMENTS
We thank anonymous reviewers for constructive suggestions that improve the presentation of
the paper. H.D., Y.P., and X.W. was partially funded by the U.S. Department of Energy, Office of
Science, Office of Advanced Scientific Computing Research, Quantum Testbed Pathfinder Program
under Award Number DE-SC0019040, Air Force Office of Scientific Research under award number
FA9550-21-1-0209, the U.S. National Science Foundation grant CCF-1942837 (CAREER) and a Sloan
research fellowship.

DATA-AVAILABILITY STATEMENT
QSynth is available from Zenodo DOI 10.5281/zenodo.10054966 [Deng et al. 2023b] and the latest
version from Github

REFERENCES
Rajeev Alur, Rastislav Bodik, Garvit Juniwal, Milo MK Martin, Mukund Raghothaman, Sanjit A Seshia, Rishabh Singh,
   Armando Solar-Lezama, Emina Torlak, and Abhishek Udupa. 2013. Syntax-guided synthesis. IEEE. https://doi.org/10.
   1109/FMCAD.2013.6679385
Rajeev Alur, Rishabh Singh, Dana Fisman, and Armando Solar-Lezama. 2018. Search-based program synthesis. Commun.
   ACM 61, 12 (2018), 84–93. https://doi.org/10.1145/3208071
Matthew Amy. 2018. Towards large-scale functional verification of universal quantum circuits. arXiv preprint arXiv:1805.06908
   (2018). https://doi.org/10.4204/eptcs.287.1
Matthew Amy, Parsiad Azimzadeh, and Michele Mosca. 2018. On the controlled-NOT complexity of controlled-NOT–phase
   circuits. Quantum Science and Technology 4, 1 (2018), 015002. https://doi.org/10.1088/2058-9565/aad8ca
Matthew Amy, Dmitri Maslov, and Michele Mosca. 2014. Polynomial-time T-depth optimization of Clifford+ T circuits
   via matroid partitioning. IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 33, 10 (2014),
   1476–1489. https://doi.org/10.1109/TCAD.2014.2341953
Matthew Amy, Dmitri Maslov, Michele Mosca, and Martin Roetteler. 2013. A meet-in-the-middle algorithm for fast synthesis
   of depth-optimal quantum circuits. IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 32, 6
   (2013), 818–830. https://doi.org/10.1109/TCAD.2013.2244643
Matthew Amy and Michele Mosca. 2019. T-count optimization and Reed–Muller codes. IEEE Transactions on Information
   Theory 65, 8 (2019), 4771–4784. https://doi.org/10.1109/TIT.2019.2906374
Dave Bacon, Wim van Dam, and Alexander Russell. 2008. Analyzing algebraic quantum circuits using exponential sums.
   unpublished: see tinyurl. com/qpo7s2 (2008).
Fabian Bauer-Marquart, Stefan Leue, and Christian Schilling. 2023. symQV: Automated Symbolic Verification of Quantum
   Programs. In Formal Methods, Marsha Chechik, Joost-Pieter Katoen, and Martin Leucker (Eds.). Springer International
   Publishing, Cham, 181–198. https://doi.org/10.1007/978-3-031-27481-7_12
Charles H Bennett, Gilles Brassard, Claude Crépeau, Richard Jozsa, Asher Peres, and William K Wootters. 1993. Teleporting
   an unknown quantum state via dual classical and Einstein-Podolsky-Rosen channels. Physical review letters 70, 13 (1993),
   1895. https://doi.org/10.1103/PhysRevLett.70.1895
Ethan Bernstein and Umesh Vazirani. 1997. Quantum Complexity Theory. SIAM J. Comput. 26, 5 (1997), 1411–1473.
   https://doi.org/10.1137/S0097539796300921 arXiv:https://doi.org/10.1137/S0097539796300921


                                  Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
59:28                                                           Haowei Deng, Runzhou Tao, Yuxiang Peng, and Xiaodi Wu


Sergey Bravyi and David Gosset. 2016. Improved classical simulation of quantum circuits dominated by Clifford gates.
   Physical review letters 116, 25 (2016), 250501. https://doi.org/10.1103/PhysRevLett.116.250501
Christophe Chareton, Sbastien Bardin, Franccois Bobot, Valentin Perrelle, and Benoit Valiron. 2020. A Deductive Verification
   Framework for Circuit-building Quantum Programs. arXiv preprint arXiv:2003.05841 (2020). https://doi.org/10.1007/978-
   3-030-72019-3_6
Yu-Fang Chen, Kai-Min Chung, Ondrej Lengál, Jyun-Ao Lin, Wei-Lun Tsai, and Di-De Yen. 2023. An Automata-based
   Framework for Verification and Bug Hunting in Quantum Circuits. Proceedings of the ACM on Programming Languages 7,
   PLDI (2023), 1218–1243. https://doi.org/10.1145/3591270
Don Coppersmith. 2002. An approximate Fourier transform useful in quantum factoring. arXiv preprint quant-ph/0201067
   (2002).
Steven A Cuccaro, Thomas G Draper, Samuel A Kutin, and David Petrie Moulton. 2004. A new quantum ripple-carry
   addition circuit. arXiv preprint quant-ph/0410184 (2004). https://doi.org/10.48550/arXiv.quant-ph/0410184
Christopher M Dawson and Michael A Nielsen. 2005. The solovay-kitaev algorithm. arXiv preprint quant-ph/0505030 (2005).
   https://doi.org/10.26421/QIC6.1-6
Timothee Goubault de Brugiere. 2020. Methods for optimizing the synthesis of quantum circuits. Ph. D. Dissertation. Universite
   Paris-Saclay.
Haowei Deng, Yuxiang Peng, Michael Hicks, and Xiaodi Wu. 2023a. Automating NISQ Application Design with Meta
   Quantum Circuits with Constraints (MQCC). ACM Transactions on Quantum Computing 4, 3 (2023), 1–29. https:
   //doi.org/10.1145/3579369
Haowei Deng, Zhoutao Run, Yuxiang Peng, and Xiaodi Wu. 2023b. QSynth Zenodo. (2023). https://doi.org/10.5281/zenodo.
   10054966
David Deutsch and Richard Jozsa. 1992. Rapid solution of problems by quantum computation. Proceedings of the Royal Society
   of London. Series A: Mathematical and Physical Sciences 439, 1907 (1992), 553–558. https://doi.org/10.1098/rspa.1992.0167
Menghan Dou, Tianrui Zou, Yuan Fang, Jing Wang, Dongyi Zhao, Lei Yu, Boying Chen, Wenbo Guo, Ye Li, Zhaoyun Chen,
   et al. 2022. QPanda: high-performance quantum computing framework for multiple application scenarios. arXiv preprint
   arXiv:2212.14201 (2022). https://doi.org/10.48550/arXiv.2212.14201
Loris D’Antoni, Qinheping Hu, Jinwoo Kim, and Thomas Reps. 2021. Programmable program synthesis. In International
   Conference on Computer Aided Verification. Springer, 84–109. https://doi.org/10.1007/978-3-030-81685-8_4
Mark Ettinger and Peter Hoyer. 1999. A quantum observable for the graph isomorphism problem. arXiv preprint quant-
   ph/9901029 (1999). https://doi.org/10.48550/arXiv.quant-ph/9901029
Yu Feng, Ruben Martins, Yuepeng Wang, Isil Dillig, and Thomas W Reps. 2017. Component-based synthesis for complex
   APIs. In Proceedings of the 44th ACM SIGPLAN Symposium on Principles of Programming Languages. 599–612. https:
   //doi.org/10.1145/3009837.3009851
Richard P Feynman. 1985. Quantum mechanical computers. Optics news 11, 2 (1985), 11–20. https://doi.org/10.1007/
   BF01886518
Jay Gambetta. 2022. IBM Quantum Roadmap to build quantum-centric supercomputers. https://research.ibm.com/blog/ibm-
   quantum-roadmap-2025
Daniel M Greenberger, Michael A Horne, and Anton Zeilinger. 1989. Going beyond Bell’s theorem. (1989), 69–72.
   https://doi.org/10.1007/978-94-017-0849-4_10
Sumit Gulwani. 2011. Automating string processing in spreadsheets using input-output examples. ACM Sigplan Notices 46,
   1 (2011), 317–330. https://doi.org/10.1145/1926385.1926423
Sumit Gulwani, William R. Harris, and Rishabh Singh. 2012. Spreadsheet Data Manipulation Using Examples. Commun.
   ACM 55, 8 (aug 2012), 97–105. https://doi.org/10.1145/2240236.2240260
Sumit Gulwani, Vijay Anand Korthikanti, and Ashish Tiwari. 2011. Synthesizing geometry constructions. ACM SIGPLAN
   Notices 46, 6 (2011), 50–61. https://doi.org/10.1145/1993316.1993505
Sumit Gulwani, Oleksandr Polozov, and Rishabh Singh. 2017. Program Synthesis. Foundations and Trends® in Programming
   Languages 4, 1-2 (2017), 1–119. https://doi.org/10.1561/2500000010
Kesha Hietala, Robert Rand, Shih-Han Hung, Xiaodi Wu, and Michael Hicks. 2021. A Verified Optimizer for Quantum
   Circuits. Proc. ACM Program. Lang. 5, POPL, Article 37 (Jan. 2021), 29 pages. https://doi.org/10.1145/3434318
Mark Hillery, Vladimir Buzek, and André Berthiaume. 1999. Quantum secret sharing. Physical Review A 59, 3 (1999), 1829.
   https://doi.org/10.1103/PhysRevA.59.1829
Qinheping Hu, John Cyphert, Loris D’Antoni, and Thomas Reps. 2021. Synthesis with asymptotic resource bounds. In
   International Conference on Computer Aided Verification. Springer, 783–807. https://doi.org/10.1007/978-3-030-81685-8_37
Qinheping Hu and Loris D’Antoni. 2018. Syntax-guided synthesis with quantitative syntactic objectives. In International
   Conference on Computer Aided Verification. Springer, 386–403. https://doi.org/10.1007/978-3-319-96145-3_21
Susmit Jha, Sumit Gulwani, Sanjit A Seshia, and Ashish Tiwari. 2010. Oracle-guided component-based program synthesis.
   In 2010 ACM/IEEE 32nd International Conference on Software Engineering, Vol. 1. IEEE, 215–224. https://doi.org/10.1145/


Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
A Case for Synthesis of Recursive Quantum Unitary Programs                                                              59:29


   1806799.1806833
Chan Gu Kang and Hakjoo Oh. 2023. Modular Component-Based Quantum Circuit Synthesis. Proceedings of the ACM on
   Programming Languages 7, OOPSLA1 (2023), 348–375. https://doi.org/10.1145/3586039
Jinwoo Kim, Qinheping Hu, Loris D’Antoni, and Thomas Reps. 2021. Semantics-guided synthesis. Proceedings of the ACM
   on Programming Languages 5, POPL (2021), 1–32. https://doi.org/10.1145/3434311
A Yu Kitaev. 1995. Quantum measurements and the Abelian stabilizer problem. arXiv preprint quant-ph/9511026 (1995).
   https://doi.org/10.48550/arXiv.quant-ph/9511026
A Yu Kitaev. 1997. Quantum computations: algorithms and error correction. Russian Mathematical Surveys 52, 6 (1997),
   1191. https://doi.org/10.1070/RM1997v052n06ABEH002155
Emanuel Kitzelmann. 2009. Inductive programming: A survey of program synthesis techniques. In International workshop
   on approaches and applications of inductive programming. Springer, 50–73. https://doi.org/10.1007/978-3-642-11931-6_3
Tristan Knoth, Di Wang, Nadia Polikarpova, and Jan Hoffmann. 2019. Resource-guided program synthesis. In Proceedings of
   the 40th ACM SIGPLAN Conference on Programming Language Design and Implementation. 253–268. https://doi.org/10.
   1145/3314221.3314602
Dax Enshan Koh, Mark D Penney, and Robert W Spekkens. 2017. Computing quopit Clifford circuit amplitudes by the
   sum-over-paths technique. Quantum Information & Computation (2017). https://doi.org/10.26421/QIC17.13-14-1
Percy Liang, Michael I Jordan, and Dan Klein. 2010. Learning programs: A hierarchical Bayesian approach. In Proceedings of
   the 27th International Conference on Machine Learning (ICML-10). 639–646.
Ci-Hong Liao, Chun-Wei Yang, and Tzonelish Hwang. 2014. Dynamic quantum secret sharing protocol based on GHZ state.
   Quantum information processing 13, 8 (2014), 1907–1916. https://doi.org/10.1007/s11128-014-0779-x
Chia-Chun Lin, Amlan Chakrabarti, and Niraj K Jha. 2014. Qlib: Quantum module library. ACM Journal on Emerging
   Technologies in Computing Systems (JETC) 11, 1 (2014), 1–20. https://doi.org/10.1145/2629430
Seth Lloyd. 2010. Quantum algorithm for solving linear systems of equations. In APS March Meeting Abstracts, Vol. 2010.
   D4–002. https://doi.org/10.1103/PhysRevLett.103.150502
Aditya Menon, Omer Tamuz, Sumit Gulwani, Butler Lampson, and Adam Kalai. 2013. A machine learning framework for
   programming by example. In International Conference on Machine Learning. PMLR, 187–195.
Ashley Montanaro. 2017. Quantum circuits and low-degree polynomials over. Journal of Physics A: Mathematical and
   Theoretical 50, 8 (2017), 084002. https://doi.org/10.1088/1751-8121/aa565f
Michael A. Nielsen and Isaac L. Chuang. 2010. Quantum Computation and Quantum Information: 10th Anniversary Edition.
   Cambridge University Press. https://doi.org/10.1017/CBO9780511976667
Jennifer Paykin, Robert Rand, and Steve Zdancewic. 2017. QWIRE: a core language for quantum circuits. ACM SIGPLAN
   Notices 52, 1 (2017), 846–858. https://doi.org/10.1145/3009837.3009894
Phitchaya Mangpo Phothilimthana, Aditya Thakur, Rastislav Bodik, and Dinakar Dhurjati. 2016. Scaling up superoptimiza-
   tion. In Proceedings of the Twenty-First International Conference on Architectural Support for Programming Languages and
   Operating Systems. 297–310. https://doi.org/10.1145/2872362.2872387
Oleksandr Polozov and Sumit Gulwani. 2015. Flashmeta: A framework for inductive program synthesis. In Proceedings of
   the 2015 ACM SIGPLAN International Conference on Object-Oriented Programming, Systems, Languages, and Applications.
   107–126. https://doi.org/10.1145/2858965.2814310
Mehdi Saeedi, Robert Wille, and Rolf Drechsler. 2011. Synthesis of quantum circuits for linear nearest neighbor architectures.
   Quantum Information Processing 10, 3 (2011), 355–377. https://doi.org/10.1007/s11128-010-0201-2
Vivek V Shende, Stephen S Bullock, and Igor L Markov. 2006. Synthesis of quantum-logic circuits. IEEE Transactions on
   Computer-Aided Design of Integrated Circuits and Systems 25, 6 (2006), 1000–1010. https://doi.org/10.1109/TCAD.2005.
   855930
Peter W Shor. 1994. Algorithms for quantum computation: discrete logarithms and factoring. In Proceedings 35th annual
   symposium on foundations of computer science. Ieee, 124–134. https://doi.org/10.1109/SFCS.1994.365700
Armando Solar-Lezama. 2008. Program synthesis by sketching. University of California, Berkeley.
Runzhou Tao, Yunong Shi, Jianan Yao, Xupeng Li, Ali Javadi-Abhari, Andrew W Cross, Frederic T Chong, and Ronghui
   Gu. 2022. Giallar: push-button verification for the qiskit Quantum compiler. In Proceedings of the 43rd ACM SIGPLAN
   International Conference on Programming Language Design and Implementation. 641–656. https://doi.org/10.1145/3519939.
   3523431
Himanshu Thapliyal, Edgard Munoz-Coreas, TSS Varun, and Travis S Humble. 2019. Quantum circuit designs of integer
   division optimizing T-count and T-depth. IEEE transactions on emerging topics in computing 9, 2 (2019), 1045–1056.
   https://doi.org/10.1109/iNIS.2017.34
Emina Torlak and Rastislav Bodik. 2013. Growing solver-aided languages with Rosette. In Proceedings of the 2013 ACM
   international symposium on New ideas, new paradigms, and reflections on programming & software. 135–152. https:
   //doi.org/10.1145/2509578.2509586



                                  Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
59:30                                                        Haowei Deng, Runzhou Tao, Yuxiang Peng, and Xiaodi Wu


Yan Xia, Chang-Bao Fu, Shou Zhang, Suc-Kyoung Hong, Kyu-Hwang Yeon, and Chung-In Um. 2006. Quantum dialogue by
   using the GHZ state. arXiv preprint quant-ph/0601127 (2006). https://doi.org/10.48550/arXiv.quant-ph/0601127
Amanda Xu, Abtin Molavi, Lauren Pick, Swamit Tannu, and Aws Albarghouthi. 2023. Synthesizing Quantum-Circuit
   Optimizers. Proceedings of the ACM on Programming Languages 7, PLDI (2023), 835–859. https://doi.org/10.1145/3591254
Mingkuan Xu, Zikun Li, Oded Padon, Sina Lin, Jessica Pointing, Auguste Hirth, Henry Ma, Jens Palsberg, Alex Aiken, Umut A
   Acar, et al. 2022. Quartz: superoptimization of Quantum circuits. In Proceedings of the 43rd ACM SIGPLAN International
   Conference on Programming Language Design and Implementation. 625–640. https://doi.org/10.1145/3519939.3523433
Mingsheng Ying. 2012. Floyd–hoare logic for quantum programs. ACM Transactions on Programming Languages and Systems
   (TOPLAS) 33, 6 (2012), 1–49. https://doi.org/10.1145/2049706.2049708
Ed Younis, Koushik Sen, Katherine Yelick, and Costin Iancu. 2021. Qfast: Conflating search and numerical optimization for
   scalable quantum circuit synthesis. In 2021 IEEE International Conference on Quantum Computing and Engineering (QCE).
   IEEE, 232–243. https://doi.org/10.1109/QCE52317.2021.00041
Nengkun Yu and Jens Palsberg. 2021. Quantum abstract interpretation. In Proceedings of the 42nd ACM SIGPLAN International
   Conference on Programming Language Design and Implementation. 542–558. https://doi.org/10.1145/3453483.3454061
Man Zhong-Xiao and Xia Yun-Jie. 2006. Controlled bidirectional quantum direct communication by using a GHZ state.
   Chinese Physics Letters 23, 7 (2006), 1680. https://doi.org/10.1088/0256-307X/23/7/007




Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
A Case for Synthesis of Recursive Quantum Unitary Programs                                                              59:31


A     APPENDIX



A.1     Proofs
Proof of Theorem 5.1


  Proof. We verify each rule’s soundness by reasoning about the semantics of the program
constructs.

    Weaken. For (𝑛, 𝑥, 𝑦) ∈ ℎ ′ ⊂ ℎ, there is ⟨𝑦| [ {{𝑆 }}(𝑛)]] |𝑥⟩ = 𝛼 (𝑛, 𝑥, 𝑦), hence ℎ ⊲ 𝑆 ↔ 𝛼 .

  Const. For any (𝑛, 𝑥, 𝑦) ∈ N3, note {{const P}}(𝑛) = 𝑃 and 𝛼 (𝑛, 𝑥, 𝑦) = [ 𝑃]] (𝑥, 𝑦). This makes
⟨𝑦|[[ {{const P}}(𝑛)]] |𝑥⟩ = 𝛼 (𝑛, 𝑥, 𝑦), and N3 ⊲ const P ↔ 𝛼 .

   Replace. For any (𝑛, 𝑥, 𝑦) ∈ ℎ, since ⟨𝑦| [ {{𝑆 }}(𝑛)]] |𝑥⟩ = 𝛼 (𝑛, 𝑥, 𝑦) = 𝛼 ′ (𝑛, 𝑥, 𝑦), we conclude
ℎ ⊲ 𝑆 ↔ 𝛼′.

    Relabel. For any (𝑛, 𝑥, 𝑦) ∈ ℎ, there is ⟨𝑦| [ {{𝑆 }}(𝑛)]] |𝑥⟩ = 𝛼 (𝑛, 𝑥, 𝑦). Because 𝜋 (𝑛) is injec-
tive, for any (𝑛, 𝑢, 𝑣) ∈ 𝜋 ◦ ℎ, there exists 𝑥, 𝑦 such that 𝜋 (𝑛, 𝑥) = 𝑢 and 𝜋 (𝑛, 𝑦) = 𝑣. Then
⟨𝑢 |[[ {{relabel 𝜋 𝑆 }}(𝑛)]] |𝑣⟩ = ⟨𝜋 (𝑛, 𝑦)| [ {{relabel 𝜋 𝑆 }}(𝑛)]] |𝜋 (𝑛, 𝑥)⟩ = ⟨𝑦| [ {{𝑆 }}(𝑛)]] |𝑥⟩ = 𝛼𝑛, 𝑥, 𝑦 =
𝛼 ′ (𝑛, 𝑢, 𝑣).

    Seq. For any (𝑛, 𝑥, 𝑦) ∈ ℎ, note ⟨𝑦| [ {{seq 𝑆 1 𝑆 2 }}(𝑛)]] |𝑥⟩ = ⟨𝑦| [ {{𝑆 2 }}(𝑛)]] [ {{𝑆 1 }}(𝑛)]] |𝑥⟩ = 𝑧 ⟨𝑦|
                                                                                                                      Í
[ {{𝑆 2 }}(𝑛)]] |𝑧⟩⟨𝑧| [ {{𝑆 2 }}(𝑛)]] |𝑥⟩. For any 𝑧, if (𝑛, 𝑥, 𝑧) ∈ ℎ 1 ∧ 𝛼 1 (𝑛, 𝑥, 𝑧) = 0, then ⟨𝑧| [ {{𝑆 2 }}(𝑛)]] |𝑥⟩ =
𝛼 1 (𝑛, 𝑥, 𝑧) = 𝛼 1 (𝑛, 𝑥, 𝑧)𝛼 2 (𝑛, 𝑧, 𝑦). Similarly, if (𝑛, 𝑧, 𝑦) ∈ ℎ 2 ∧𝛼 2 (𝑛, 𝑧, 𝑦) = 0, it equals to 𝛼 1 (𝑛, 𝑥, 𝑧)𝛼 2 (𝑛, 𝑧, 𝑦).
If (𝑛, 𝑥, 𝑧) ∈ ℎ 1 ∧ (𝑛, 𝑧, 𝑦) ∈ ℎ 2, the term also becomes 𝛼 1 (𝑛, 𝑥, 𝑧)𝛼 2 (𝑛, 𝑧, 𝑦). Hence we have
ℎ ⊲ seq 𝑆 1 𝑆 2 ↔ 𝛼 .

   Fix. Similarly, we denote fix𝑘 𝜋 𝑃 0 · · · 𝑃𝑘 −1 𝑆𝐿 𝑆𝑅 as fix𝑘 . For any (𝑖, 𝑥, 𝑦) ∈ ℎ where 𝑖 < 𝑘,
by (ℎ𝑖 , 𝛼𝑖 ) ≡𝑖 (ℎ, 𝛼), we know (𝑖, 𝑥, 𝑦) ∈ ℎ𝑖 and 𝛼 (𝑖, 𝑥, 𝑦) = 𝛼𝑖 (𝑖, 𝑥, 𝑦). Since ℎ𝑖 ⊲ const P𝑖 ↔
𝛼𝑖 and (ℎ, 𝛼) ≡𝑖 (ℎ𝑖 , 𝛼𝑖 ), we have ⟨𝑦| [ {{fix𝑘 }}(𝑖)]] |𝑥⟩ = ⟨𝑦| [ 𝑃𝑖 ] |𝑥⟩ = 𝛼𝑖 (𝑖, 𝑥, 𝑦) = 𝛼 (𝑖, 𝑥, 𝑦). For
any (𝑖, 𝑥, 𝑦) ∈ ℎ such that 𝑖 ≥ 𝑘, note {{fix𝑘 }} = {{𝑆𝐿 }}(𝑖); map_qb(𝜋 (𝑖), {{fix𝑘 }}(𝑖 − 1)); {{𝑆𝑅 }}(𝑖).
According to the proof for Relabel and Seq, with (ℎ, 𝛼) ≡𝑖 (ℎ𝐿 , 𝛼 𝐿 ) ⊗ (𝜋 ◦ pred (ℎ, 𝛼)) ⊗ (ℎ𝑅 , 𝛼 𝑅 ),
we have ⟨𝑦| [ {{fix𝑘 }}(𝑖)]] |𝑥⟩ = 𝛼 (𝑖, 𝑥, 𝑦).                                                               □




Proof of Theorem 6.1


  Proof. We first prove that given a SQIR program 𝑃 and we have N3 ⊲ const P ↔ 𝛼, then 𝛼 is
sparse.
  Since 𝑃 is a SQIR program, 𝑃 is a sequence of applications of gates to fixed number of qubits and
we have

                                                  𝛼 (𝑛, 𝑥, 𝑦) = {{𝑃 }}𝑥 𝑦                                              (A.1)


                                  Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
59:32                                                         Haowei Deng, Runzhou Tao, Yuxiang Peng, and Xiaodi Wu


Without loss of generality, suppose {{𝑃 }} is a unitary applied to qubits 𝑞 0, 𝑞 1, ..., 𝑞𝑚 , 𝑚 ∈ N. Let
function X, Y be
                                   {𝑘 | 𝑘 < 2𝑚+1, 𝑘 ∈ N}, 𝑦 < 2𝑚+1
                                  
                                  
                      X(𝑛, 𝑦) =                                                                              (A.2)
                                   {mk(𝑦, 0, 𝑚) + 𝑘 | 𝑘 < 2𝑚+1, 𝑘 ∈ N}, otherwise
                                  
                                   {𝑘 | 𝑘 < 2𝑚+1, 𝑘 ∈ N}, 𝑥 < 2𝑚+1
                                  
                                  
                     Y (𝑛, 𝑥) =                                                                              (A.3)
                                   {mk(𝑥, 0, 𝑚) + 𝑘 | 𝑘 < 2𝑚+1, 𝑘 ∈ N}, otherwise
                                  
where mk(𝑥, 0, 𝑚) means to set from the 0th bit to the 𝑚th bits (in the order from low to high) in 𝑥
to 0 (e.g. mk((1111)2, 0, 1)) = (1100)2 = (12)10 ). It is easy to see that for arbitrary inputs, the size
of the sets returned by Y, X is always 2𝑚+1 . Now we prove that
                                  ∀𝑛, 𝑥, 𝑦 ∈ N, 𝛼 (𝑛, 𝑥, 𝑦) ≠ 0 → 𝑦 ∈ Y (𝑛, 𝑥)                               (A.4)
Formula 𝛼 (𝑛, 𝑥, 𝑦) ≠ 0 → 𝑥 ∈ X(𝑛, 𝑦) can be proved in the same way. When 𝛼 (𝑛, 𝑥, 𝑦) ≠ 0:
    • if 𝑥 < 2𝑚+1 , since {{𝑃 }} is a unitary applied to qubits 𝑞 0, 𝑞 1, ..., 𝑞𝑚 , ⟨𝑥 |{{𝑃 }}|𝑦⟩ = 0 for every
      𝑦 ≥ 2𝑚+1 . So we know that 𝑦 < 2𝑚+1 and 𝑦 ∈ Y (𝑛, 𝑥).
    • Otherwise, since {{𝑃 }} does not change the state of qubits other than qubits 𝑞 0, 𝑞 1, 𝑞 2, ..., 𝑞𝑚 ,
      we should have mk(𝑥, 0, 𝑚) = mk(𝑦, 0, 𝑚) if 𝛼 (𝑛, 𝑥, 𝑦) ≠ 0. Then we have 𝑦 ∈ Y (𝑛, 𝑥)
So we have 𝛼 ⊴ (X, Y) and we prove that 𝛼 is sparse.
  Next we prove that given a sparse amplitude function 𝛼 and an injective mapping 𝜋, function
𝜋 ◦ 𝛼 is sparse.
  Since 𝛼 is sparse, there exists functions X, Y and we have 𝛼 ⊴ (X, Y). Let functions X 𝜋 , Y 𝜋 be
                                     X 𝜋 (𝑛, 𝑦) = {𝜋 −1 (𝑘) | 𝑘 ∈ X(𝑛, 𝜋 (𝑦))}                               (A.5)
                                       𝜋              −1
                                    Y (𝑛, 𝑥) = {𝜋          (𝑘) | 𝑘 ∈ Y (𝑛, 𝜋 (𝑥))}                           (A.6)
Then we have
        (𝜋 ◦ 𝛼) (𝑛, 𝑥, 𝑦) ≠ 0 =⇒ 𝛼 (𝑛, 𝜋 (𝑥), 𝜋 (𝑦)) ≠ 0
                              =⇒ 𝜋 (𝑥) ∈ X(𝑛, 𝜋 (𝑦)) ∧ 𝜋 (𝑦) ∈ Y (𝑛, 𝜋 (𝑥))
                              =⇒ 𝑥 ∈ {𝜋 −1 (𝑘) | 𝑘 ∈ X(𝑛, 𝜋 (𝑦))} ∧ 𝑦 ∈ {𝜋 −1 (𝑘) | 𝑘 ∈ Y (𝑛, 𝜋 (𝑥)}
                              =⇒ 𝑥 ∈ X 𝜋 (𝑛, 𝑦) ∧ 𝑦 ∈ Y 𝜋 (𝑛, 𝑥)
So we have
                       ∀𝑛 𝑥 𝑦, (𝜋 ◦ 𝛼) (𝑛, 𝑥, 𝑦) ≠ 0 → 𝑦 ∈ Y 𝜋 (𝑛, 𝑥) ∧ 𝑥 ∈ X 𝜋 (𝑛, 𝑦)
So we have , 𝜋 ◦ 𝛼 ⊴ (X 𝜋 , Y 𝜋 ) and we prove that 𝜋 ◦ 𝛼 is sparse.
   Finally we prove that given two sparse amplitude function 𝛼 1, 𝛼 2 , function 𝛼 1 ∗ 𝛼 2 is sparse. Since
𝛼 1, 𝛼 2 are sparse, suppose we have 𝛼 1 ⊴ (X1, Y1 ) and 𝛼 2 ⊴ (X2, Y2 ). We also have
                                                     ∑︁
                            (𝛼 1 ∗ 𝛼 2 ) (𝑛, 𝑥, 𝑦) =     𝛼 1 (𝑛, 𝑥, 𝑧)𝛼 2 (𝑛, 𝑧, 𝑦)
                                                      𝑧 ∈ X1 (𝑛,𝑦)

Let functions X, Y be
                                       X(𝑛, 𝑦) := {X1 (𝑛, 𝑧)|𝑧 ∈ X2 (𝑛, 𝑦)}                                  (A.7)
                                       Y (𝑛, 𝑥) := {Y2 (𝑛, 𝑧)|𝑧 ∈ Y1 (𝑛, 𝑥)}                                 (A.8)

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
A Case for Synthesis of Recursive Quantum Unitary Programs                                                      59:33


Then we have
    (𝛼 1 ∗ 𝛼 2 ) (𝑛, 𝑥, 𝑦) ≠ 0 =⇒ ∃𝑧, 𝛼 1 (𝑛, 𝑥, 𝑧) ≠ 0 ∧ 𝛼 2 (𝑛, 𝑧, 𝑦) ≠ 0                                     (A.9)
                             =⇒ ∃𝑧, 𝑧 ∈ Y1 (𝑛, 𝑥) ∧ 𝑧 ∈ X2 (𝑛, 𝑦) ∧ 𝑥 ∈ X1 (𝑛, 𝑧) ∧ 𝑦 ∈ Y2 (𝑛, 𝑧)             (A.10)
                             =⇒ 𝑥 ∈ X(𝑛, 𝑦) ∧ 𝑦 ∈ Y (𝑛, 𝑥)                                                    (A.11)
  So we have
                       ∀𝑛 𝑥 𝑦, (𝛼 1 ∗ 𝛼 2 ) (𝑛, 𝑥, 𝑦) ≠ 0 → 𝑥 ∈ X(𝑛, 𝑦) ∧ 𝑦 ∈ Y (𝑛, 𝑥)                        (A.12)
So 𝛼 1 ∗ 𝛼 2 ⊴ (X, Y) and we prove that 𝛼 1 ∗ 𝛼 2 is sparse.                                                        □



Received 2023-07-11; accepted 2023-11-07




                               Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 59. Publication date: January 2024.
