                                           QbC: Quantum Correctness by Construction
                                           ANURUDH PEDURI, Ruhr University Bochum, Germany
                                           INA SCHAEFER, Karlsruhe Institute of Technology, Germany
arXiv:2307.15641v3 [quant-ph] 6 May 2025




                                           MICHAEL WALTER, Ruhr University Bochum, Germany
                                           Thanks to the rapid progress and growing complexity of quantum algorithms, correctness of quantum programs
                                           has become a major concern. Pioneering research over the past years has proposed various approaches to
                                           formally verify quantum programs using proof systems such as quantum Hoare logic. All these prior approaches
                                           are post-hoc: one first implements a program and only then verifies its correctness. Here we propose Quantum
                                           Correctness by Construction (QbC): an approach to constructing quantum programs from their specification in
                                           a way that ensures correctness. We use pre- and postconditions to specify program properties, and propose
                                           sound and complete refinement rules for constructing programs in a quantum while language from their
                                           specification. We validate QbC by constructing quantum programs for idiomatic problems and patterns. We
                                           find that the approach naturally suggests how to derive program details, highlighting key design choices
                                           along the way. As such, we believe that QbC can play a role in supporting the design and taxonomization of
                                           quantum algorithms and software.
                                           CCS Concepts: • Theory of computation → Logic and verification; Hoare logic; Quantum computation
                                           theory.
                                           Additional Key Words and Phrases: quantum Hoare logic, correctness by construction, quantum while language
                                           ACM Reference Format:
                                           Anurudh Peduri, Ina Schaefer, and Michael Walter. 2025. QbC: Quantum Correctness by Construction. Proc.
                                           ACM Program. Lang. 9, OOPSLA1, Article 99 (April 2025), 43 pages. https://doi.org/10.1145/3720433

                                           1   Introduction
                                           The field of quantum computing has seen tremendous progress. There are a variety of quantum
                                           algorithms for a broad range of computational problems, including for combinatorial search and
                                           optimization [4, 6, 16, 30], factoring and other algebraic problems [66], and linear algebra [19, 26,
                                           31, 73] – supported by algorithmic frameworks such as quantum walks [20] and the quantum
                                           singular value transform [26, 43], as well as by novel quantum data structures [27, 81]. Montanaro
                                           [44] provides an overview of various quantum algorithms. To support these developments and
                                           the construction of larger quantum programs, Selinger [64] first proposed a design for a quantum
                                           programming language. Since then, there have been numerous quantum programming languages
                                           at various levels of abstraction (see, e.g., [3, 12, 28, 69, 71, 74] and references therein).
                                              Correctness of algorithms has always been a major concern in computing, with intensive work
                                           on program analysis, testing and verification of programs and software in past decades. For classical
                                           computing, Hoare [33] introduced a formal system, in which for a program 𝑆, one specifies its
                                           properties by using a precondition 𝑃 and a postcondition 𝑄, resulting in a Hoare triple denoted
                                           Authors’ Contact Information: Anurudh Peduri, anurudh.peduri@rub.de, Chair for Quantum Information, Faculty of
                                           Computer Science, Ruhr University Bochum, Bochum, Germany; Ina Schaefer, ina.schaefer@kit.edu, Chair of Testing,
                                           Validation and Analysis of Software-Intensive Systems (TVA), Institute for Information Security and Dependability (KASTEL),
                                           Karlsruhe Institute of Technology, Karlsruhe, Germany; Michael Walter, michael.walter@rub.de, Chair for Quantum
                                           Information, Faculty of Computer Science, Ruhr University Bochum, Bochum, Germany.



                                           This work is licensed under a Creative Commons Attribution 4.0 International License.
                                           © 2025 Copyright held by the owner/author(s).
                                           ACM 2475-1421/2025/4-ART99
                                           https://doi.org/10.1145/3720433


                                                                          Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
99:2                                                                  Anurudh Peduri, Ina Schaefer, and Michael Walter


as {𝑃 }𝑆 {𝑄 }. A Hoare triple is said to be correct if running the program 𝑆 starting in any state
satisfying 𝑃 results in a state that satisfies 𝑄. Hoare logic has been extended to probabilistic
programs [46, 46], where the properties are probabilistic, and correctness is defined in terms of
their expectations. A survey of the successes of Hoare logic can be found in [7]. Another approach
to verifying programs is using Incorrectness Logic [49], which attempts to find bugs in programs by
finding counterexamples. Quantum computing poses unique challenges for formal verification that
are not encountered in classical computing due to the nature of its computational model. Pioneering
research over the past years has uncovered how to adapt the above-mentioned approaches to the
quantum setting, e.g., quantum Hoare logic [18, 34, 63, 80] and quantum incorrectness logic [78].
   Still, all prior approaches to verifying quantum programs are post-hoc: they take the completed
program as a starting point and establish whether the program meets the specification. If post-hoc
verification fails, there is often no indication of what needs to be fixed in the program. Especially
in the quantum setting, predicates specifying program properties are represented by large matrices,
which makes it difficult to reason about, locate, and fix issues with quantum programs with a
post-hoc approach. In contrast, Correctness-by-Construction (CbC) [23, 38, 45] is a programming
methodology to incrementally build correct programs based on a specification. For classical com-
puting, CbC provides a method where one starts with a concise specification, and then uses a
small set of refinement rules to incrementally construct the program in such a way that at the end
of the construction process, the program provably satisfies the specification, i.e., it is correct by
construction. This approach can help build well-structured and concise programs and draw insights
from the corresponding specification, supporting algorithm designers in developing intuition and
allowing them to focus on central design aspects of the constructed algorithms. Runge et al. [62]
provide a detailed comparison between CbC and post-hoc verification techniques. To the best of
our knowledge, the Correctness-by-Construction approach has not been applied to construct and
verify quantum programs before our work.

1.1    Our Contributions
In this work, we propose Quantum Correctness by Construction (QbC), an approach to constructing
quantum programs from their specification in a way that ensures correctness. To this end, we
consider a simple quantum programming language, the quantum while language, and extend it with
a new construct called a hole, which represents a yet-to-be-constructed program. Holes take the
form {𝑃 }□{𝑄 } , where 𝑃 and 𝑄 represent the pre- and postconditions that should be satisfied by
the program, as in quantum Hoare logic [80]. For example, the specification for the paradigmatic
problem of searching a “database” 𝑓 : {0, 1}𝑛 → {0, 1} with success probability 𝑝, as famously solved
by Grover’s algorithm [30], can be succinctly expressed as
                                                    Í
                                          {𝑝𝐼 }□{     𝑥 s.t. 𝑓 (𝑥 )=1 |𝑥⟩⟨𝑥 |} .

This states that measuring the program’s output results in a solution to the search problem, i.e., an 𝑥
such that 𝑓 (𝑥) = 1, with probability at least 𝑝. Indeed, the precondition 𝑝𝐼 accepts any state with
probability 𝑝, and the postcondition, which then must hold with at least this probability, accepts
only states that on measuring give an 𝑥 such that 𝑓 (𝑥) = 1. We discuss this example in Section 4.
   For the above language, we then provide refinement rules, which allow filling in holes in quantum
programs in such a way that correctness is preserved. There are two widely used notions of
correctness for Hoare triples, partial and total correctness, which differ in how they treat non-
termination. We provide refinement rules for both notions. These rules take the following form:

                        {𝑃 }□{𝑄 } ↩→ 𝑆              if certain conditions 𝐶 1, 𝐶 2, . . . hold

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
QbC: Quantum Correctness by Construction                                                                        99:3


To apply such a rule, one first checks that the conditions 𝐶 1, 𝐶 2, . . . are satisfied and then replaces the
left-hand side hole with the right-hand side program 𝑆 (which may itself contain other holes). For
example, we can always apply the sequence rule, {𝑃 }□{𝑄 } ↩→ {𝑃 }□{𝑅}; {𝑅}□{𝑄 } ; intuitively,
this rule states that in order to construct a program that takes precondition 𝑃 to postcondition 𝑄, it
suffices to construct a program that takes the precondition to some intermediate condition 𝑅, and
another one that takes this intermediate condition to the postcondition. Starting from an initial
specification {𝑃 }□{𝑄 } , one iteratively applies refinement rules until one arrives at a program
𝑆 final that contains no more holes. We prove a soundness theorem that states that any program
obtained by this process of refinement is guaranteed to satisfy the initial specification, that is, the
quantum Hoare triple {𝑃 }𝑆 final {𝑄 } is valid and the program is correct by construction. Here, we
use the notion of quantum Hoare triple introduced by Ying [80]. We also prove completeness: any
program that satisfies a specification can be obtained by process of refinement. We note that the
completeness above is relative to the theory of complex numbers, as defined in Ref. [80], which is
also assumed in all prior works. Because of the unintuitive nature of quantum logic, these results
are more challenging to establish than in the classical case. For example, quantum predicates cannot
be interpreted as (deterministic or probabilistic) functions of some program state; observing or
“measuring” predicates is not a passive operation, but will in general change the program’s state;
and there is in general no canonical choice of predicates in refinement rules. All these can be traced
back to the noncommutative nature of quantum information.
    Finally, we validate our approach by constructing quantum programs for quantum teleportation
and quantum search (Section 4). In each case, we start from their intuitive specification and use one
key algorithmic idea or refinement step at a time. We find that the refinement rules not only guide
the construction of the desired programs, but that the QbC approach also reveals design choices
that can be made along the way. For example, when constructing a program for the quantum
search problem, we show how one can naturally arrive at both a naive algorithm that proceeds by
random sampling, as well as Grover’s celebrated search algorithm that offers a quantum speedup.
To summarize, in this work, we:

   (1) Introduce a Quantum Correctness by Construction (QbC) approach for quantum programs.
       In QbC, quantum programs are constructed starting from specifications by successively
       applying refinement rules.
   (2) In doing so, provide a formalization based on quantum while programs with holes, which
       specify pre- and postconditions of subprograms that still need to be constructed.
   (3) Prove our refinement systems sound and complete: Any program constructed from an
       initial specification by using the refinement rules must satisfy the specification, and for any
       program satisfying a specification, there exists a sequence of refinements to obtain it from
       the specification.
   (4) Validate QbC by constructing quantum programs for idiomatic problems, starting from their
       specification. Our findings suggest that QbC can play a role in supporting the design and
       taxonomization of quantum algorithms and software.

1.2   Related Work
   Correctness-by-Construction for Classical Programs. The CbC approach to programming was
initially introduced by Back et al. [9], Dijkstra [23], Morgan [45] and Gries [29] and later extended
by Kourie and Watson [38], see also the relation algebra of programming [13]. There has since been
extensive work on tools and theory for CbC [14, 15, 37, 58–61]. Other similar approaches include
the B method [1, 2, 17], syntax-guided synthesis [68], and type systems [21].

                            Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
99:4                                                                Anurudh Peduri, Ina Schaefer, and Michael Walter


   Probabilistic Verification. Various classical program logics have been extended to probabilistic
programs: Hoare logic [22], weakest precondition reasoning [46, 50], separation logic [11], relational
logic [8, 10], and dynamic logic for forward reasoning [53]. We refer to Kaminski et al. [35] and
references therein for recent work on proving termination and bounding expected runtimes. Syntax-
guided synthesis techniques have also been extended to probabilistic programs [5].
   Quantum Verification. The majority of work in quantum verification has focused on post-hoc
approaches. The first approach on Hoare logic for quantum programs was introduced by [18,
34], and was extended to support reasoning about unbounded quantum loops with (relative)
completeness [80] and to include classical variables [24]. Zhou et al. [82] provided a rigorous
implementation of quantum Hoare logic in Coq with a range of applications. Zhou et al. [83]
focused on projections as predicates and proposed a notion of robust Hoare triples, which allow pre-
and postconditions to be approximately satisfied. Rand [55] surveys recent advances in Hoare-style
verification logics for quantum programs. Zuliani [84] illustrates a refinement based approach,
but gives no complete system of refinement rules. Neri et al. [47] contributes an extension of
laws of classical program algebra to quantum programming. Other related quantum verification
efforts include incorrectness logic [78], circuit verification [39, 54, 56], quantum relational Hoare
logic [40, 72], and equational reasoning in Dirac notation [77].
   Recent Developments. Shortly after our work had appeared as a preprint, Feng et al. [25] reported
on independent work on a refinement system that is similar to ours but differs in two key respects.
First, their work considers only projective predicates, whereas our formalism allows for arbitrary
predicates. Therefore our formalism captures a larger class of interesting properties, in particular
success probabilities of algorithms, which are important in most quantum algorithms (see Section 4
and Section 4.4). Second, while their refinement system only ensures partial correctness, we also
provide a refinement system that ensures total correctness. The latter gives stronger guarantees and
in particular enables reasoning about termination, which is impossible otherwise. Feng et al. [25]
also provide a Python-based proof-of-concept implementation of their calculus. A recent work [65]
has similarly proposed a web-based proof-of-concept implementation of QbC.
   Organization of the Paper. In Section 2, we review the basic quantum formalism that is used in
the paper. We introduce the quantum while language, a simple quantum programming language
with control-flow and loops, as well as quantum Hoare logic, which defines notions of correctness
of quantum programs in terms of pre- and postconditions. In Section 3, we introduce Quantum
Correctness by Construction (QbC). We first define an extension of the quantum while language,
called programs with holes, which allows specifying subprograms that still need to be constructed.
Then we define refinement rules that can be used to construct quantum programs from given
specifications, and we prove soundness and completeness of these rules. In Section 4, we use QbC
to naturally construct several quantum programs starting from their specification. We conclude
in Section 5. Appendices A to C contain technical proofs for results announced in the main text.
Appendix D continues the discussion of a running example in the text.

2      Preliminaries
In this section, after setting our notation and conventions (Section 2.1), we give a brief introduction
to the formalism of quantum computing (Section 2.2). Then we describe the syntax and semantics of
a simple quantum programming language (Section 2.3) and recall quantum Hoare logic (Section 2.4).

2.1     Notation and Conventions
We take N to be the set of natural numbers including zero. In this work, a Hilbert space H is a

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
QbC: Quantum Correctness by Construction                                                                       99:5


finite-dimensional complex vector space with inner product. Throughout the paper we use Dirac
notation: we write |𝜓 ⟩ ∈ H for vectors, ⟨𝜙 | for covectors, and ⟨𝜙 |𝜓 ⟩ for the inner product. Here, 𝜓
is an arbitrary label. In general, 𝑀 † denotes the adjoint of a linear operator 𝑀. The identity operator
                                                                       Í
on a Hilbert space H is denoted by 𝐼 H and can be written as 𝐼 H = 𝑥 ∈Σ |𝑥⟩⟨𝑥 | for any (orthonormal)
basis {|𝑥⟩}𝑥 ∈Σ of H , where Σ is an index set. We write 𝐼 when the Í    Hilbert space is clear from the
context. The trace of an operator 𝑀 can be computed as tr 𝑀 = 𝑥 ∈Σ ⟨𝑥 |𝑀 |𝑥⟩ for any basis as
above. For example, a quantum bit or qubit corresponds to the 2-dimensional Hilbert space H = C2 ,
with standard basis {|0⟩ , |1⟩} labeled by Σ = {0, 1}. The identity operator is 𝐼 = |0⟩⟨0| + |1⟩⟨1|. An
example of an operator on C2 is the Pauli 𝑋 matrix, defined as 𝑋 = |0⟩⟨1| + |1⟩⟨0|. It satisfies 𝑋 † = 𝑋
and tr 𝑋 = 0. We require two more concepts from linear algebra. An operator 𝑀 on H is Hermitian
if ⟨𝜓 |𝑀 |𝜓 ⟩ ∈ R for all vectors |𝜓 ⟩ ∈ H , and positive semidefinite (PSD) if ⟨𝜓 |𝑀 |𝜓 ⟩ ≥ 0 for all
vectors |𝜓 ⟩ ∈ H . Equivalently, 𝑀 can be diagonalized by a unitary matrix and has real resp.
nonnegative eigenvalues. Given two operators 𝐴 and 𝐵 on H , we write 𝐴 ⪯ 𝐵 if and only if 𝐵 − 𝐴
is PSD; this defines the Löwner order. For example, we can write 𝑀 ≥ 0 to state that 𝑀 is PSD.

2.2   Quantum Computing
We now recall the basic formalism of quantum computing. We refer to the excellent textbooks Nielsen
and Chuang [48], Wilde [76], Yanofsky and Mannucci [79] for more comprehensive introductions.
   Variables. A quantum variable 𝑞 is modeled by a Hilbert space H𝑞 = CΣ𝑞 for some finite index
set Σ𝑞 . This means that H𝑞 is a vector space equipped with an inner product and an orthonormal
standard basis (or computational basis) {|𝑥⟩}𝑥 ∈Σ𝑞 , labeled by the elements 𝑥 ∈ Σ𝑞 . When Σ𝑞 = {0, 1},
then H𝑞 = C2 and 𝑞 is called a quantum bit or qubit, with standard basis {|0⟩ , |1⟩}, Ëas above. If 𝒒 is
a collection of quantum variables, then the corresponding Hilbert space is H𝒒 = 𝑞 ∈𝒒 H𝑞  CΣ𝒒 ,
where the Cartesian product Σ𝒒 = 𝑞 ∈𝒒 Σ𝑞 labels the standard (product) basis of the quantum
                                     Î
variables 𝒒. We assume that there is a finite set of quantum variables, denoted by qVars. Then the
overall Hilbert space is
                                                                  CΣ𝑞 = CΣ,
                                            Ì               Ì
                          H = HqVars =              H𝑞 
                                             𝑞 ∈qVars         𝑞 ∈qVars

where Σ = ΣqVars = 𝑞 ∈qVars Σ𝑞 labels the standard basis of the all quantum variables. It is well
                   Î
understood how to extend the above to infinite-dimensional Hilbert spaces and an infinite number
of quantum variables, but we will not need this here.
   States. The state of all the quantum variables is described by a positive semidefinite (PSD) operator
on H with trace equal to 1, often called a density operator. We denote the set of all such operators
by D (H ). A state is called pure if it is given by a rank-one projection, i.e., if 𝜌 = |Ψ⟩⟨Ψ| for some
unit vector |Ψ⟩ ∈ H . For simplicity one often also refers to |Ψ⟩ as the (pure) state. States that are
not pure are called mixed. More generally, we consider partial states, also called subnormalized
states, which are PSD operators of trace at most one, denoted by D ≤1 (H ). Partial states are akin to
sub-probability measures in probabilistic computing. They are useful for reasoning about programs
that may terminate with probability less than one. For example, the computational basis states of a
qubit are |0⟩⟨0| and |1⟩⟨1|, which are both pure states, and the partial state 𝜌 = 0.8 |0⟩⟨0| describes the
output of a program terminating in state |0⟩⟨0| with probability 0.8 (and not terminating otherwise).
   Operations. There are two basic kinds of operations. The first is to apply a unitary. An operator 𝑈
is called a unitary if 𝑈 𝑈 † = 𝑈 †𝑈 = 𝐼 . If we apply a unitary 𝑈 on H to a (partial) state 𝜌, the result
is 𝑈 𝜌𝑈 † , which is again a (partial) state. For example, the Hadamard matrix 𝐻 = √1 11 −1      1
                                                                                                    
                                                                                                      is a
                                                                                                    2
one-qubit unitary, and on applying it to the input state |0⟩⟨0|, we get |+⟩⟨+|, where |+⟩ = √1 (|0⟩+|1⟩).
                                                                                                        2

                           Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
99:6                                                                Anurudh Peduri, Ina Schaefer, and Michael Walter


   The second operation is to measure the quantum state. A measurement (also called a positive
operator-valued measure or POVM) is given by a family of positive semidefinite operators 𝑴 =
{𝑀𝜔 }𝜔 ∈Ω , labeled by some finite index set Ω, such that 𝜔 ∈Ω 𝑀𝜔 = 𝐼 . If one measures a (partial)
                                                               Í
state 𝜌 then the probability
                     √      √ of seeing outcome 𝜔 ∈ Ω is 𝑞𝜔 = tr(𝜌𝑀𝜔 ), in which case the state
changes to 𝜌√𝜔 = 𝑀𝜔 𝜌 𝑀𝜔 /𝑞𝜔 . Note that any PSD operator            √ 𝑀 has a unique PSD square root,
denoted  by      𝑀. If 𝑀 is a   projection, meaning    𝑀 2 = 𝑀, then 𝑀 = 𝑀. We abbreviate M (𝜌) =
√      √                                                                                        𝜔
  𝑀𝜔 𝜌 𝑀𝜔 . Note that this is a partial state, with trace equal to the probability 𝑞𝜔 of outcome 𝜔.
   When Ω = {0, 1}, there are only two possible outcomes, and this is called a binary measurement.
Any binary measurement {𝐵 0, 𝐵 1 } can be obtained by picking a positive semidefinite    √ operator
                                                                                                 √ 𝐵
with 𝐵 ⪯ 𝐼 and  √ √setting  𝐵 0  = 𝐼 − 𝐵 and 𝐵 1 =  𝐵. As  above, we abbreviate B0 (𝜌) =  𝐼 − 𝐵𝜌   𝐼 −𝐵
and B1 (𝜌) √ = 𝐵𝜌 𝐵. For example,√for a qubit, 𝐵 = |1⟩⟨1| defines the standard basis measurement,
with 𝐵 0 = 𝐵 0 = |0⟩⟨0| and 𝐵 1 = 𝐵 1 = |1⟩⟨1|. For succinctness, we will often refer to 𝐵 rather
than {𝐵 0, 𝐵 1 } as a binary measurement. For example, if we apply the binary standard basis mea-
surement to a qubit in the |+⟩⟨+| state, then B0 (|+⟩⟨+|) = 12 |0⟩⟨0| and B1 (|+⟩⟨+|) = 12 |1⟩⟨1|. Thus
each outcome 𝜔 ∈ {0, 1} occurs with probability half and the state after the measurement is |𝜔⟩⟨𝜔 |.
   We can also apply any of the above operations to a subset 𝒒 ⊆ qVars of the quantum variables.
To this end, let us, for an arbitrary operator 𝐴 on H𝒒 , define the operator 𝐴𝒒 = 𝐴 ⊗ 𝐼 on H , where
the tensor product is with respect to the decomposition H = H𝒒 ⊗ H𝒒𝑐 and 𝒒𝑐 = qVars \ 𝒒 denotes
the remaining quantum variables. In prior work, this has been called cylindrical extension [82].
Then, if 𝑈 is a unitary on H𝒒 , we can apply it to the quantum variables 𝒒 by taking 𝑈 𝒒 in the
above prescription. Similarly, if {𝑀𝜔 }𝜔 ∈Ω is a measurement on H𝒒 , we take {𝑀𝜔,𝒒 } in the above
                                                   √︁       √︁
prescription; we also abbreviate M𝜔,𝒒 (𝜌) = 𝑀𝜔,𝒒 𝜌 𝑀𝜔,𝒒 .

2.3    Quantum While Language
In this paper, we consider a quantum while language [24, 80, 82]. We first introduce its syntax
and then discuss its denotational semantics. The language supports initializing quantum variables,
applying unitary operations, and classical control flow based on quantum measurement outcomes.
We first describe the language’s syntax.
   Definition 2.1 (Syntax). Quantum while programs are given by the following grammar:
          𝑆 ::= skip | 𝒒 := |0⟩ | 𝒒 := 𝑈 (𝒒) | 𝑆 1 ; 𝑆 2 | repeat 𝑁 do 𝑆 end
                 | case meas 𝒒 with {𝜔 1 : 𝑀𝜔 1 , 𝜔 2 : 𝑀𝜔 2 , . . .} of 𝜔 1 : 𝑆𝜔 1 , 𝜔 2 : 𝑆𝜔 2 , . . . end
                 | while meas 𝒒 with 𝐵 do 𝑆 end
where 𝑆, 𝑆 1, 𝑆 2, 𝑆𝜔 1 , 𝑆𝜔 2 , . . . denote programs in the language; 𝒒 denotes a set of quantum variables;
𝑈 is a unitary operator on H𝒒 ; 𝑁 is a natural number; {𝑀𝜔 }𝜔 ∈Ω is a measurement on H𝒒 with
outcomes in some set Ω = {𝜔 1, 𝜔 2, . . .}; 𝐵 is an operator defining a binary measurement {𝐼 − 𝐵, 𝐵}.
  The first five instructions are self-explanatory: skip is a no-op; 𝒒 := |0⟩ initializes the set of
variables 𝒒; 𝒒 := 𝑈 (𝒒) applies a unitary 𝑈 to the set of variables 𝒒; 𝑆 1 ; 𝑆 2 sequentially composes
the two programs, running 𝑆 1 followed by 𝑆 2 ; and repeat 𝑁 do 𝑆 end runs the program 𝑆 𝑁
times. The case statement is used for control flow: it measures the set of variables 𝒒 with the
measurement 𝑴, and on seeing outcome 𝜔 runs the program 𝑆𝜔 . The while statement measures
the set of variables 𝒒 with a binary measurement 𝐵 and, if it succeeds (i.e. has outcome 1), runs
the loop body 𝑆 and repeats. Thus, both case and while are classical control flow based on the
outcome of a quantum measurement.
   Remark 2.2. We comment on an aspect that is well-understood but usually left implicit. In the
instruction 𝒒 := 𝑈 (𝒒) , the unitary 𝑈 will often be restricted to an arbitrary fixed subset of allowed

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
QbC: Quantum Correctness by Construction                                                                       99:7


“gates” (typical choices are few-qubit unitaries or the Clifford+T gate set). The same applies to
measurement operators 𝑀𝜔 (typical choices are standard basis measurements or arbitrary 1-qubit
measurements). The results of our paper, just like those of prior works, do not depend on this
choice (Theorems 3.6 to 3.9), and all our examples use efficiently implementable unitaries.
  We also introduce some syntactic sugar for convenience. First, we define an if statement as a
shorthand for a case statement with a binary measurement:
                              if meas 𝒒 with 𝐵 then 𝑆 1 else 𝑆 0 end ≡
                       case meas 𝒒 with {1 : 𝐵, 0 : 𝐼 − 𝐵} of 1 : 𝑆 1 , 0 : 𝑆 0 end
We allow leaving out the else branch, in which case we take 𝑆 0 = skip . Lastly, we allow leaving out
the measurement in if, case, and while, in which case we default to standard basis measurements:
       if meas 𝑞 then 𝑆 1 else 𝑆 0 end ≡ if meas 𝑞 with |1⟩⟨1| then 𝑆 1 else 𝑆 0 end
               case meas 𝒒 of . . . end ≡ case meas 𝒒 with {𝑥 : |𝑥⟩⟨𝑥 |}𝑥 ∈Σ𝒒 of . . . end
               while meas 𝑞 do 𝑆 end ≡ while meas 𝑞 with |1⟩⟨1| do 𝑆 end
   Example 2.3 (Quantum coin toss until zero). As a gentle introduction to the quantum while
language, we consider the following program, which exercises several language features:
               𝐴toss-until-zero = 𝑞 := |0⟩ ; 𝑞 := 𝐻 (𝑞); while meas 𝑞 do 𝑞 := 𝐻 (𝑞) end
It first initializes a qubit in the |0⟩ state, and then repeatedly applies the Hadamard gate and
measures in the standard basis, until the outcome “0” is seen. We revisit this example later from the
perspectives of denotational semantics and quantum Hoare logic.
  Semantics. Any program 𝑆 defines a function that maps the state of the quantum variables
before execution to the corresponding (partial) state after program execution. This is called the
denotational semantics of 𝑆 and is defined formally in the following.
  Definition 2.4 (Denotational semantics). For any program 𝑆, its denotational semantics is the map
                                      ⟦𝑆⟧ : D ≤1 (H ) → D ≤1 (H ),
which is defined recursively in the following way:
  (1) ⟦ skip ⟧(𝜌) = 𝜌
                       Í
  (2) ⟦ 𝒒 := |0⟩ ⟧(𝜌) = 𝒙 ∈Σ𝒒 |0⟩⟨𝒙 | 𝒒 𝜌 |𝒙⟩⟨0| 𝒒
  (3) ⟦ 𝒒 := 𝑈 (𝒒) ⟧(𝜌) = 𝑈 𝒒 𝜌𝑈 𝒒†
  (4) ⟦ 𝑆 1 ; 𝑆 2 ⟧(𝜌) = ⟦𝑆 2 ⟧(⟦𝑆 1 ⟧(𝜌))
  (5) ⟦ repeat 𝑁 do 𝑆 end ⟧(𝜌) = ⟦𝑆⟧𝑁 (𝜌)
                                                                 Í
  (6) ⟦ case meas 𝒒 with 𝑴 of . . . , 𝜔 : 𝑆𝜔 , . . . end ⟧(𝜌) = 𝜔 ∈Ω ⟦𝑆𝜔 ⟧(M𝜔,𝒒 (𝜌))
                                                    Í∞                    𝑘 
  (7) ⟦ while meas 𝒒 with 𝐵 do 𝑆 end ⟧(𝜌) = 𝑘=0           B0,𝒒 ◦ ⟦𝑆⟧ ◦ B1,𝒒 (𝜌)

   We explain the semantics above using the definitions from Section 2.2. Statements (1)-(5) are
self-explanatory. The case statement (6) measures a set of variables 𝒒 with the measurement 𝑴,
and on seeing outcome 𝜔 executes program 𝑆𝜔 . The while statement (7) runs a loop with body 𝑆,
guarded by the condition that measuring 𝒒 with the binary measurement 𝐵 gives outcome 1. The
                                                                   Í
semantics for while is well-defined because the partial states 𝜎𝑛 = 𝑛𝑘=0 B0,𝒒 ◦ (⟦𝑆⟧ ◦ B1,𝒒 )𝑘 (𝜌)
form an increasing sequence (𝜎𝑛 ⪯ 𝜎𝑛+1 for all 𝑛) that is bounded from above. Note that 𝜎𝑛

                           Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
99:8                                                                 Anurudh Peduri, Ina Schaefer, and Michael Walter


represents the partial state corresponding to termination within at most 𝑛 iterations of the loop.
Loops 𝑆 = while meas 𝒒 with 𝐵 do 𝐶 end satisfy the following natural recurrence:
                                        ⟦𝑆⟧ = B0,𝒒 + ⟦𝑆⟧ ◦ ⟦𝐶⟧ ◦ B1,𝒒                                           (2.1)
The denotational semantics of a program, ⟦𝑆⟧, is a so-called superoperator because it is a linear
function mapping operators on one Hilbert space to operators on another. To be meaningful, this
superoperator should map partial quantum states to partial quantum states, even when applied to
a subset of the quantum variables. Formally, this means that ⟦𝑆⟧ should be completely positive and
trace non-increasing. Recall that a superoperator E is called completely positive if for every additional
Hilbert space H ′ the superoperator E ⊗IH ′ maps PSD operators to PSD operators, with IH ′ denoting
the identity superoperator on H ′ , and it is called trace non-increasing if tr E (𝑀) ≤ tr 𝑀 for every 𝑀
(it is called trace preserving if equality holds for all 𝑀). Conversely, these two conditions guarantee
that a superoperator can be physically realized.
    One can note that ⟦𝑆⟧ is completely positive and trace non-increasing for any program 𝑆.
Moreover, for any state 𝜌 ∈ D (H ), the quantity tr(⟦𝑆⟧(𝜌)) ∈ [0, 1] can be interpreted as the
probability of termination of the program 𝑆 when started in the initial state 𝜌. In particular, the
program 𝑆 terminates almost surely (that is, with probability one) when started in state 𝜌 if, and
only if, tr(⟦𝑆⟧(𝜌)) = 1. Thus the program terminates on any input state if ⟦𝑆⟧ is trace preserving
(we also say that 𝑆 is trace preserving). We note that (1)-(3) are always trace preserving, (4)-(6) are
trace preserving if all the subprograms (𝑆 1 , 𝑆 2 , 𝑆, 𝑆𝜔 for 𝜔 ∈ Ω) are trace preserving, and (7) is trace
preserving if the subprogram 𝑆 is trace preserving and the loop terminates with probability one.
  Example 2.5 (Semantics of quantum coin toss until zero). We can use Definition 2.4 to compute the
semantics for the quantum coin oss until zero program in Example 2.3. For any state 𝜌 ∈ D (H ),
       ⟦𝐴toss-until-zero ⟧(𝜌) = ⟦ 𝑞 := |0⟩ ; 𝑞 := 𝐻 (𝑞); while meas 𝑞 do 𝑞 := 𝐻 (𝑞) end ⟧(𝜌)
                                                                                                               
                           = ⟦ while meas 𝑞 do 𝑞 := 𝐻 (𝑞) end ⟧ ⟦ 𝑞 := 𝐻 (𝑞) ⟧(⟦ 𝑞 := |0⟩ ⟧(𝜌))
                                                                                       
                           = ⟦ while meas 𝑞 do 𝑞 := 𝐻 (𝑞) end ⟧ ⟦ 𝑞 := 𝐻 (𝑞) ⟧(|0⟩⟨0|)
                           = ⟦ while meas 𝑞 do 𝑞 := 𝐻 (𝑞) end ⟧(|+⟩⟨+|).
using (4), (2), and (3). By (7), the semantics of the loop is for a general state 𝜎 ∈ D ≤1 (H ) given by
                                                          ∞ 
                                                         ∑︁                               
          ⟦ while meas 𝑞 do 𝑞 := 𝐻 (𝑞) end ⟧(𝜎) =             B0 ◦ (⟦ 𝑞 := 𝐻 (𝑞) ⟧ ◦ B1 )𝑘 (𝜎),
                                                               𝑘=0
where B 𝑗 (𝜌) = | 𝑗⟩⟨𝑗 |𝜌 | 𝑗⟩⟨𝑗 | = ⟨𝑗 |𝜌 | 𝑗⟩ | 𝑗⟩⟨𝑗 |. Now, for any state 𝜎 ∈ D ≤1 (H ), we have
                                  (⟦ 𝑞 := 𝐻 (𝑞) ⟧ ◦ B1 ) (𝜎) = ⟨1|𝜎 |1⟩ |−⟩⟨−| ,
and therefore for any 𝑘 ≥ 1, (⟦ 𝑞 := 𝐻 (𝑞) ⟧ ◦ B1 )𝑘 (|+⟩⟨+|) = 21𝑘 |−⟩⟨−|. Thus we find that
                                                                          ∞              
                                                                         ∑︁      1
        ⟦ while meas 𝑞 do 𝑞 := 𝐻 (𝑞) end ⟧(|+⟩⟨+|) = B0 (|+⟩⟨+|) +           B0 𝑘 |−⟩⟨−|
                                                                         𝑘=1
                                                                                 2
                                                                                 ∞
                                                                     1          ∑︁ 1
                                                                 =     |0⟩⟨0| +        |0⟩⟨0| = |0⟩⟨0| ,
                                                                     2            2𝑘+1
                                                                                𝑘=1
and hence the semantics of the coin toss until zero program is, for any initial state 𝜌 ∈ D (H ),
given by
                                  ⟦𝐴toss-until-zero ⟧(𝜌) = |0⟩⟨0|                            (2.2)
We see that no matter what state we start in, the program always terminates in the pure state |0⟩.

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
QbC: Quantum Correctness by Construction                                                                        99:9


2.4   Quantum Hoare Logic
Hoare logic is a formal system to state and prove correctness of programs. For a program 𝑆, one
specifies a precondition 𝑃 and postcondition 𝑄 to form a Hoare triple {𝑃 }𝑆 {𝑄 }. Such a Hoare triple
is said to hold if, for any state that satisfies 𝑃, running the program on it results in a state that
satisfies 𝑄. Here 𝑃 and 𝑄 are predicates over the state of the program variables. In this section, we
present the formalism for quantum Hoare logic from [80].
   Predicates. Predicates are properties of the state of the system that can hold to some degree.
Recall that any PSD operator 𝑃 ⪯ 𝐼 defines a binary measurement {𝐵 0, 𝐵 1 } by setting 𝐵 0 = 𝐼 − 𝑃
and 𝐵 1 = 𝑃. We may think of 𝑃 as defining a predicate: As in probabilistic Hoare logic [46], instead
of assigning a definite truth value to a given predicate and state, we rather assign an expectation or
degree to which the predicate holds in the given state – namely the probability of getting outcome 1
if one were to apply the binary measurement defined by 𝑃. For any state 𝜌, this probability is given
by tr(𝑃 𝜌), as explained earlier. We thus arrive at the following definition.
   Definition 2.6 (Predicates and expectation). A predicate is a positive semidefinite operator 𝑃 such
that 𝑃 ⪯ 𝐼 , and the set of all such predicates is denoted P≤1 (H ). The expectation of the predicate 𝑃
in a (partial) state 𝜌 ∈ D ≤1 (H ) is defined as
                                           E𝜌 (𝑃) = tr(𝑃 𝜌) ∈ [0, 1].
We say that 𝑃 implies 𝑄 for two predicates 𝑃, 𝑄 iff E𝜌 (𝑃) ≤ E𝜌 (𝑄) for all states 𝜌 ∈ D (H ). This is
equivalent to 𝑃 ⪯ 𝑄 in the Löwner order, but is in the context of predicates often denoted 𝑃 ⇒ 𝑄.
   Just like in classical Hoare logic one can also transform predicates with respect to a program 𝑆. To
this end, we use the adjoint ⟦𝑆⟧† of the denotational semantics superoperator ⟦𝑆⟧ (see Definition 2.4
and the discussion below it). For any superoperator E, the adjoint E † satisfies the defining property
that tr(𝐴 E (𝐵)) = tr(E † (𝐴) 𝐵) for all operators 𝐴, 𝐵. We note that E is completely positive iff
this is the case for its adjoint; it is trace preserving iff its adjoint is unital, that is, E † (𝐼 ) = 𝐼 , and
trace non-increasing if the adjoint is sub-unital, that is, E † (𝐼 ) ⪯ 𝐼 . While ⟦𝑆⟧ transforms states, its
adjoint ⟦𝑆⟧† naturally acts on predicates, and we have the following useful duality:
                                                                   
                                        E⟦𝑆⟧(𝜌 ) (𝑃) = E𝜌 ⟦𝑆⟧† (𝑃) .
for any program 𝑆 and for any (partial) state 𝜌 ∈ D ≤1 (H ) and predicate 𝑃 ∈ P≤1 (H ).
  Quantum Hoare Triples. A quantum Hoare triple is denoted by
                                                   {𝑃 }𝑆 {𝑄 }
and consists of a program 𝑆, precondition 𝑃, and postcondition 𝑄, where 𝑃, 𝑄 are predicates as
defined above. Similar to probabilistic Hoare logic, we have notions of correctness of a Hoare triple.
  We start with total correctness. It states that the postcondition holds to a degree no less than the
precondition:
   Definition 2.7 (Total correctness). For a program 𝑆 and predicates 𝑃, 𝑄, the Hoare triple {𝑃 }𝑆 {𝑄 }
is said to be totally correct if for all partial states 𝜌 ∈ D ≤1 (H ),
                                            E𝜌 (𝑃) ≤ E⟦𝑆⟧(𝜌 ) (𝑄).
We denote total correctness by |=tot {𝑃 }𝑆 {𝑄 }. Mathematically, this is equivalent to 𝑃 ⇒ ⟦𝑆⟧† (𝑄),
or 𝑃 ⪯ ⟦𝑆⟧† (𝑄).
 Next, we define partial correctness. Here the degree to which the postcondition holds only
matters insofar as the program terminates.

                            Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
99:10                                                                  Anurudh Peduri, Ina Schaefer, and Michael Walter


   Definition 2.8 (Partial correctness). For a program 𝑆 and predicates 𝑃, 𝑄, the Hoare triple {𝑃 }𝑆 {𝑄 }
is said to be partially correct if for all partial states 𝜌 ∈ D ≤1 (H ),
                                E𝜌 (𝑃) ≤ E⟦𝑆⟧(𝜌 ) (𝑄) + [tr(𝜌) − tr(⟦𝑆⟧(𝜌))].                                     (2.3)
This condition can be equivalently stated as
                                          E𝜌 (𝐼 − 𝑃) ≥ E⟦𝑆⟧(𝜌 ) (𝐼 − 𝑄).                                          (2.4)
We denote partial correctness by |=par        {𝑃 }𝑆 {𝑄 }. Mathematically, this is equivalent to ⟦𝑆⟧† (𝐼 −𝑄) ⇒
𝐼 − 𝑃, or 𝐼 − 𝑃 ⪰ ⟦𝑆⟧† (𝐼 − 𝑄).
   As explained below Definition 2.4, the term [tr(𝜌) − tr(⟦𝑆⟧(𝜌))] in Eq. (2.3) is the probability of
non-termination of the program 𝑆 when started in an initial state 𝜌. It is always non-negative (as ⟦𝑆⟧
is trace non-increasing). Intuitively, Eq. (2.3) states that the degree to which the postcondition holds
is at least the degree to which the precondition holds, minus the probability of non-termination. The
equivalent Eq. (2.4) says that the probability that the program terminates and the postcondition
does not hold is at most the probability that the precondition does not hold. Total implies partial
correctness.
   For later use, we observe that |=tot {𝐼 }𝑆 {𝑄 } means that, for any initial state, the program
terminates almost surely in a state satisfying the postcondition, while |=par {𝐼 }𝑆 {𝑄 } means that
the postcondition holds whenever the program terminates. In particular, |=tot {𝐼 }𝑆 {𝐼 } states that 𝑆
terminates almost surely on any initial state, while |=par {𝐼 }𝑆 {𝐼 } holds trivially for any program.
  Example 2.9 (Hoare logic specification for quantum coin toss until zero). We now discuss a natural
quantum Hoare triple for our running example (Example 2.3). One way to specify the behavior of
the program 𝐴toss-until-zero is by the Hoare triple
                                             {𝐼 }𝐴toss-until-zero {|0⟩⟨0|}.
As discussed, this states that, for any input state, the program terminates in the final state |0⟩. We
can verify explicitly that this Hoare triple program is totally correct. Indeed, we saw in Eq. (2.2) of
Example 2.5 that ⟦𝐴toss-until-zero ⟧(𝜌) = |0⟩⟨0| for every state 𝜌 ∈ D (H ), and hence
                        E⟦𝐴toss-until-zero ⟧(𝜌 ) (|0⟩⟨0|) = E |0⟩⟨0| (|0⟩⟨0|) = 1 = tr 𝜌 = E𝜌 (𝐼 )
for any state 𝜌 ∈ D (H ). This confirms that the triple is totally correct. There are also much simpler
programs that meet this same specification, e.g. 𝑞 := |0⟩ . See also the discussion in Appendix D.
    Projections as Predicates. When the precondition in a Hoare triple is a projection, 𝑃 2 = 𝑃, we
only need to verify correctness for pure states 𝜌 = |𝜓 ⟩⟨𝜓 | that exactly satisfy the precondition,
meaning E𝜌 (𝑃) = 1 or equivalently 𝑃 |𝜓 ⟩ = |𝜓 ⟩ [83, Theorem 3.2]. In particular, we can specify the
behavior of the program when run with some initial pure state |Ψ⟩ by using the precondition 𝑃 =
|Ψ⟩⟨Ψ|: A Hoare triple {|Ψ⟩⟨Ψ|}𝑆 {𝑄 } is totally correct iff E⟦𝑆⟧( |Ψ⟩⟨Ψ| ) (𝑄) = 1, and partially correct
iff E⟦𝑆⟧( |Ψ⟩⟨Ψ| ) (𝑄) = E⟦𝑆⟧( |Ψ⟩⟨Ψ| ) (𝐼 ). Thus:
   Lemma 2.10. Let 𝑃 be a projection and 𝑄 an arbitrary predicate. Then, 𝑃 ⇒ 𝑄 holds if, and only if,
⟨𝜓 |𝑄 |𝜓 ⟩ = 1 for every unit vector |𝜓 ⟩ such that 𝑃 |𝜓 ⟩ = |𝜓 ⟩.
    More generally, the precondition 𝑃 = |𝜓 ⟩⟨𝜓 | 𝒒 ⊗ 𝐼 𝒒𝑐 can be used to specify the behavior on
input states where the quantum variables 𝒒 are in some pure state |𝜓 ⟩ ∈ H𝒒 . The situation
simplifies further if the postcondition is also given by a pure state, say 𝑄 = |Φ⟩⟨Φ|. Indeed, the
Hoare triple {|Ψ⟩⟨Ψ|}𝑆 {|Φ⟩⟨Φ|} is totally correct iff ⟦𝑆⟧(|Ψ⟩⟨Ψ|) = |Φ⟩⟨Φ|, and partially correct
iff ⟦𝑆⟧(|Ψ⟩⟨Ψ|) = 𝑝 |Φ⟩⟨Φ| for some arbitrary probability of termination 𝑝 ∈ [0, 1]. In other words,
total (or partial) correctness of the above Hoare triple means that running the program 𝑆 on state |Ψ⟩

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
QbC: Quantum Correctness by Construction                                                                       99:11


results in state |Φ⟩ (if the program terminates). We use the above observations later when specifying
teleportation and search in Section 4. We caution that we cannot specify program behavior on
mixed initial states 𝜌 by taking 𝑃 = 𝜌. Since any mixed state can be purified, this does not impose a
real restriction.

2.5    Multiple Specifications
We often want to specify that a single program satisfies several Hoare triples at once. We give three
motivating examples:
  (1) To prove a Hoare triple {𝑃 } repeat 𝑁 do 𝑆 end {𝑄 } correct, it suffices to prove that the loop
                           
      body satisfies 𝑅 𝑗 𝑆 𝑅 𝑗+1 for all 𝑗 ∈ {0, . . . , 𝑁 − 1}, for predicates 𝑅0, . . . , 𝑅𝑁 with 𝑃 ⇒ 𝑅0
      and 𝑅𝑁 ⇒ 𝑄.
  (2) To assert that a program 𝑆 terminates on any input, we can always add the Hoare triple {𝐼 }𝑆 {𝐼 }
      on top of any other Hoare triple that we also want to hold (as discussed earlier).
  (3) A program 𝑆 that creates a qubit that, when measured, gives 𝑥 ∈ {0, 1} with 50% probability
      each, can be specified by two Hoare triples {𝐼 /2}𝑆 {|𝑥⟩⟨𝑥 |} for 𝑥 ∈ {0, 1} (see Section 4.1).
At other times, we may also want to allow the program 𝑆 itself to depend on some parameter. For
example, the search algorithms of Section 4.3 will necessarily have to depend explicitly on the
database that is being queried. We will thus consider Hoare triples
                                                 {𝑃𝜆 }𝑆𝜆 {𝑄 𝜆 },
where the pre- and postconditions as well as the program are parameterized by 𝜆 in some index
set Λ. Such a Hoare triple is (totally or partially) correct if it is correct for every definite value of 𝜆. If
the program 𝑆𝜆 does not depend on 𝜆, we have a single program that satisfies multiple specifications,
while if it depends on (part of) 𝜆, then we have a family of programs. To stick with the literature,
we will think of 𝜆 as a formal (or meta) parameter that is implicitly quantified over universally, but
one could instead also adjust the definition of predicates to be functions Λ → P≤1 (H ) (and extend
the notions of expectation, implication, and so forth in a straightforward way).
   The following notation will be useful: if 𝜆 ranges over a finite set of options {𝜆1, . . . , 𝜆𝑘 }, then
we will also write
                                                                    
                                  𝑃𝜆1 , . . . , 𝑃𝜆𝑘 𝑆𝜆1 , . . . , 𝑆𝜆𝑘 𝑄 𝜆1 , . . . , 𝑄 𝜆𝑘
instead of {𝑃𝜆 }𝑆𝜆 {𝑄 𝜆 }. If the precondition, the postcondition, or the program do not depend on 𝜆,
we will write the corresponding term only once. For instance, the third motivating example above
could alternatively be written as {𝐼 /2}𝑆 {|0⟩⟨0| , |1⟩⟨1|}.

3     Correctness by Construction for Quantum Programs
In the Correctness-by-Construction (CbC) approach, one starts with a specification and successively
refines it to construct a program that is guaranteed to satisfy the initial specification. Prior work on
CbC defined refinement rules in terms of Hoare triples: one could replace an “abstract” program 𝑆
in a Hoare triple {𝑃 }𝑆 {𝑄 } (where 𝑃, 𝑄 are some predicates) by some concrete program 𝑆 ′ provided
certain side conditions were satisfied, which often involved the validity of other Hoare triples for
subprograms that have to be constructed beforehand.
   Here, we extend the quantum while language by a new construct {𝑃 }□{𝑄 }, called a hole, which
represents a yet-to-be-constructed subprogram that carries a precondition 𝑃 and a postcondition 𝑄
(Section 3.1). This notion of programs with holes is similar in spirit to abstract execution [70],
where one is interested in executing and analyzing programs containing “abstract statements”, and
also the concept of typed holes in programming [32, 51, 67]. For both partial and total correctness,
we then proceed to provide refinement rules (Section 3.2) that can be used to construct correct

                            Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
99:12                                                               Anurudh Peduri, Ina Schaefer, and Michael Walter


programs by replacing holes with concrete programs. Next, we prove that our refinement rules are
sound: any program 𝑆 constructed from a specification {𝑃 }□{𝑄 } must satisfy that specification,
meaning that the Hoare triple {𝑃 }𝑆 {𝑄 } is correct (Section 3.3). Finally, we show that our refinement
rules are complete: any program 𝑆 satisfying a Hoare triple {𝑃 }𝑆 {𝑄 } can be constructed from the
specification {𝑃 }□{𝑄 } (Section 3.4).

3.1     Quantum While Language with Holes
To support QbC specifications, we first extend our quantum while language in Definition 2.1 with
a new construct: holes. A hole is a yet-to-be-constructed program tagged with a precondition and a
postcondition, such that the corresponding Hoare triple should be satisfied once the hole is filled
by a program. We define the syntax of the extended language below.
   Definition 3.1 (Syntax). Programs in the quantum while language with holes are given by the
following grammar:
          𝑆 ::= skip | 𝒒 := |0⟩ | 𝒒 := 𝑈 (𝒒) | 𝑆 1 ; 𝑆 2 | repeat 𝑁 do 𝑆 end
                 | case meas 𝒒 with {𝜔 1 : 𝑀𝜔 1 , 𝜔 2 : 𝑀𝜔 2 , . . .} of 𝜔 1 : 𝑆𝜔 1 , 𝜔 2 : 𝑆𝜔 2 , . . . end
                 | while meas 𝒒 with 𝐵 do 𝑆 end | {𝑃 }□{𝑄 }.

The new construct {𝑃 }□{𝑄 } is called a hole with precondition 𝑃 and a postcondition 𝑄, which
are arbitrary predicates. Apart from this, the above grammar is identical to the quantum while
language (Definition 2.1). A program that may contain holes is called an abstract program, and one
that does not contain any holes is called a concrete program. In other words, concrete programs are
simply programs in the quantum while language.
   In the following we will also be interested in holes that satisfy multiple pre- and postcon-
ditions, which can be formalized just as discussed for Hoare triples (Section 2.5). We will de-
note these as {𝑃𝜆 }□{𝑄 𝜆 } , where 𝜆 is some formal parameter, or use short-hand notation such
as {𝑃, 𝑃 ′ }□{𝑄, 𝑄 ′ } . See, e.g., (HP.split) and (H.repeat) below, and Remark 3.3 for further discussion.

3.2     Refinement Rules
Refinement is the process of replacing holes in abstract programs with other (abstract or concrete)
programs. To this end, we define refinement relations on abstract programs, and we use these
iteratively to construct concrete programs from specifications given by a single hole {𝑃 }□{𝑄 } .
We first define refinement rules that ensure partial correctness:
  Definition 3.2 (Refinement for partial correctness). We define a relation ↩→par , called refinement for
partial correctness on programs with holes (Definition 3.1) as follows: For any two predicates 𝑃 and 𝑄,
  (H.skip) {𝑃 }□{𝑄 } ↩→par skip , if 𝑃 ⇒ 𝑄.
                                             Í
   (H.init) {𝑃 }□{𝑄 } ↩→par 𝒒 := |0⟩ , if 𝑃 ⇒ 𝒙 ∈Σ𝒒 |𝒙⟩⟨0| 𝒒 𝑄 |0⟩⟨𝒙 | 𝒒 .
  (H.unit) {𝑃 }□{𝑄 } ↩→par 𝒒 := 𝑈 (𝒒) , if 𝑃 ⇒ 𝑈 𝒒†𝑄𝑈 𝒒 .
   (H.seq) {𝑃 }□{𝑄 } ↩→par {𝑃 }□{𝑅}; {𝑅}□{𝑄 } for any predicate 𝑅.
 (HP.split) {𝑃 }□{𝑄 } ↩→par {𝑃𝛾 }□{𝑄𝛾 } for any two families of predicates 𝑃𝛾 , 𝑄𝛾 for 𝛾 in some
            index set Γ, such that 𝑃 ⇒ 𝛾 𝑝𝛾 𝑃𝛾 and 𝛾 𝑝𝛾 𝑄𝛾 ⇒ 𝑄 for a probability distribution 𝑝𝛾 .
                                            Í           Í

(H.repeat) {𝑃 }□{𝑄 } ↩→par repeat 𝑁 do {𝑅 𝑗 }□{𝑅 𝑗+1 } end , where 𝑗 ∈ {0, . . . , 𝑁 − 1}, for any
            predicates 𝑅0, 𝑅1, . . . , 𝑅𝑁 such that 𝑃 ⇒ 𝑅0 and 𝑅𝑁 ⇒ 𝑄.
  (H.case) {𝑃 }□{𝑄 } ↩→par case meas 𝒒 with 𝑴 of {𝜔 : {𝑃𝜔 }□{𝑄 }}𝜔 ∈Ω end
            for any family of predicates 𝑃𝜔 for 𝜔 ∈ Ω such that 𝑃 ⇒ 𝜔 ∈Ω M𝜔 (𝑃𝜔 ).
                                                                       Í


Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
 QbC: Quantum Correctness by Construction                                                                         99:13


(HP.while) {𝑃 }□{𝑄 } ↩→par while meas 𝒒 with 𝐵 do {𝑅}□{B0,𝒒 (𝑄) + B1,𝒒 (𝑅)} end ,
           for any predicate 𝑅 such that 𝑃 ⇒ B0,𝒒 (𝑄) + B1,𝒒 (𝑅).
We also have rules for composite statements:
  (C.seqL) 𝑆 1′ ; 𝑆 2 ↩→par 𝑆 1 ; 𝑆 2 , if 𝑆 1′ ↩→par 𝑆 1 .
  (C.seqR) 𝑆 1 ; 𝑆 2′ ↩→par 𝑆 1 ; 𝑆 2 , if 𝑆 2′ ↩→par 𝑆 2 .
(C.repeat) repeat 𝑁 do 𝑆 ′ end ↩→par repeat 𝑁 do 𝑆 end , if 𝑆 ′ ↩→par 𝑆.
  (C.case) case meas 𝒒 with 𝑴 of 𝜔 : 𝑆𝜔′ , . . . end ↩→par
            case meas 𝒒 with 𝑴 of 𝜔 : 𝑆𝜔 , . . . end ,
           if 𝑆𝜔′ ↩→par 𝑆𝜔 for one 𝜔 ∈ Ω (and the rest unchanged).
 (C.while) while meas 𝒒 with 𝐵 do 𝑆 ′ end ↩→par while meas 𝒒 with 𝐵 do 𝑆 end ,
           if 𝑆 ′ ↩→par 𝑆.
 For any two programs 𝑆, 𝑆 ′ , we say 𝑆 ′ refines in one step to 𝑆 ensuring partial correctness if 𝑆 ′ ↩→par 𝑆.
 More generally, for any 𝑘 ≥ 0 we define 𝑆 ′ ↩→𝑘par 𝑆 if 𝑆 ′ refines to 𝑆 in 𝑘 such steps. We say 𝑆 ′
 refines to 𝑆 ensuring partial correctness if 𝑆 can be obtained from 𝑆 ′ by applying any number of
                                                                          Ð∞
 refinement steps and denote this by 𝑆 ′ ↩→∗par 𝑆. Clearly, ↩→∗par = 𝑘=0         ↩→𝑘par is the reflexive and
 transitive closure of the relation ↩→par .
   In Definition 3.2, the rules labeled (H.∗) and (HP.∗) are used to refine a single hole to another
program (H stands for hole). The rules labeled (C.∗) are used to refine holes in composite programs
(C stands for composite). See Section 4.1 and Appendix D for pedagogical expositions on applying
refinements to construct quantum coin-tossing programs. The first three rules refine to concrete
program statements: (H.skip) refines to a skip statement, (H.init) refines to an initialization 𝒒 := |0⟩,
and (H.unit) refines to a unitary application 𝒒 := 𝑈 (𝒒). To refine a hole to a sequence of two
holes, we can use the (H.seq) rule with any arbitrary intermediate condition 𝑅. To motivate
(HP.split), observe that if a program satisfies two Hoare triples {𝑃 }𝑆 {𝑄 } and {𝑃 ′ }𝑆 {𝑄 ′ }, then it
also satisfies any combination {𝑝𝑃 + (1 − 𝑝)𝑄 }𝑆 {𝑝𝑄 + (1 − 𝑝)𝑄 ′ } for 𝑝 ∈ [0, 1]. So to ensure the
latter it suffices to construct a program that satisfies the former. Note that in stating this rule we
use the syntax for multiple specifications discussed below Definition 3.1. In (HP.split) we also
allow for weakening preconditions and strengthening postconditions; we isolate this in (H.sw)
below for convenience. To refine a hole to a repeat statement using (H.repeat), we must find a
family of predicates 𝑅0, 𝑅1, . . . , 𝑅𝑁 , such that 𝑅𝑛 holds after running the loop body 0 ≤ 𝑛 ≤ 𝑁
times, with 𝑅0 implied by the precondition and 𝑅𝑁 implying the postcondition. The body of the
repeat statement is {𝑅 𝑗 }□{𝑅 𝑗+1 } where 𝑗 ∈ {0, . . . , 𝑁 − 1} is a formal parameter, meaning that
the yet-to-be-constructed program must satisfy these specification for all such 𝑗. To refine a hole
to a case statement using (H.case), we must find a family of predicates 𝑃𝜔 for each measurement
outcome 𝜔 such that if 𝑃 holds before the measurement then 𝑃𝜔 holds after measurement upon
seeing outcome 𝜔. Finally, to refine a hole to a while statement using (HP.while), we need to find
an “invariant” 𝑅 for the loop body. If the measurement succeeds after the execution of the loop
body, then 𝑅 must hold; otherwise 𝑄 must hold. Finally, the composite rules allow refining any
hole in a composite program using any of the rules above.
   Remark 3.3 (Multiple specifications and formal parameters). As mentioned, some refinement rules
 can introduce holes with multiple specifications. For example, (H.repeat) introduces a hole with
 pre- and postcondition labeled by an index 𝑗 ∈ {0, . . . , 𝑁 − 1}, and (HP.split) introduces a new
 parameter 𝛾 in some arbitrary index set Γ. We can model this formally by implicitly extending the
 index set Λ of Section 2.5 to include this new parameter. Later refinements may depend on this

                               Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
 99:14                                                               Anurudh Peduri, Ina Schaefer, and Michael Walter


 parameter. For example, if we refine a hole produced by (H.repeat) with the (H.seq) rule, then the
 intermediate predicates 𝑅 may also depend on 𝑗. See Section 4 for many examples.
   We can also apply these rules to the syntactic sugar introduced in Section 2.3 and deduce some
 other rules for convenience. For example, since an if statement is shorthand for a case statement,
 we also have
 (H.ifElse) {𝑃 }□{𝑄 } ↩→par if meas 𝒒 with 𝐵 then {𝑅1 }□{𝑄 } else {𝑅0 }□{𝑄 } end ,
        for any predicates 𝑅0, 𝑅1 s.th. 𝑃 ⇒ B0,𝒒 (𝑅0 ) + B1,𝒒 (𝑅1 ).
 We can also introducing an if statement without an else branch:
 (H.if) {𝑃 }□{𝑄 } ↩→∗par if meas 𝒒 with 𝐵 then {𝑅}□{𝑄 } end ,
        for any predicate 𝑅 such that 𝑃 ⇒ B0,𝒒 (𝑄) + B1,𝒒 (𝑅).
 This follows from (H.ifElse) by further refining the second hole using (H.skip).
   Finally, we have the following rule that shows that we may always construct a program that has
 a weaker precondition and a stronger postcondition:
 (H.sw) {𝑃 }□{𝑄 } ↩→par {𝑃 ′ }□{𝑄 ′ } for any predicates 𝑃 ′, 𝑄 ′ such that 𝑃 ⇒ 𝑃 ′ and 𝑄 ′ ⇒ 𝑄.
 This is a special case of (HP.split) where we take the two families to consist of a single predicate 𝑃 ′
 and 𝑄 ′ , respectively.
   Remark 3.4 (Challenges of quantum verification). The quantum setting poses some interesting
 new challenges. For example, in a (H.case) rule for classical programs, one can always choose the
 predicates as 𝑃𝜔 = 𝑃 ∧ (𝑞 = 𝜔). In the quantum setting, there is generally no canonical choice of
 the predicates 𝑃𝜔 . We leave the problem of finding suitable heuristics to future work.
    We also define refinement rules that ensure total correctness:
    Definition 3.5 (Refinement for total correctness). We define a relation ↩→tot , called refinement for
 total correctness on programs with holes, by using all the rules from Definition 3.2 that are labeled
 (H.∗) or (C.∗), by replacing each ↩→par with ↩→tot , but replacing (HP.while) and (HP.split) by the
 following rules respectively:
(HT.while) {𝑃 }□{𝑄 } ↩→tot while meas 𝒒 with 𝐵 do {𝑅𝑛+1 }□{B0,𝒒 (𝑄) + B1,𝒒 (𝑅𝑛 )} end ,
             for any binary measurement 𝐵 and sequence of predicates {𝑅𝑛 }𝑛∈N that is weakly
             increasing in the sense that 𝑅𝑛 ⇒ 𝑅𝑛+1 for all 𝑛 ∈ N, such that 𝑅0 = 0 and the limit
             𝑅 := lim𝑛→∞ 𝑅𝑛 satisfies 𝑃 ⇒ B0,𝒒 (𝑄) + B1,𝒒 (𝑅).
 (HT.split) {𝑃 }□{𝑄 } ↩→tot {𝑃𝛾 }□{𝑄𝛾 } for any two families of predicates 𝑃𝛾 , 𝑄𝛾 for 𝛾 in some
             index set Γ, such that 𝑃 ⇒ 𝛾 𝑝𝛾 𝑃𝛾 and 𝛾 𝑝𝛾 𝑄𝛾 ⇒ 𝑄 for some 𝑝𝛾 ≥ 0.
                                          Í                Í

 For any two programs 𝑆, 𝑆 ′ , we say that 𝑆 ′ refines in one step to 𝑆 ensuring total correctness if 𝑆 ′ ↩→tot 𝑆.
 More generally, for any 𝑘 ≥ 0, we define 𝑆 ′ ↩→𝑘tot 𝑆 if 𝑆 ′ refines to 𝑆 in 𝑘 such steps. We say that 𝑆 ′
 refines to 𝑆 ensuring total correctness if 𝑆 can be obtained from 𝑆 ′ by applying any number of
                                                                                            Ð∞
 refinement steps and denote this by 𝑆 ′ ↩→∗tot 𝑆. Similarly as above, ↩→∗tot = 𝑘=0                ↩→𝑘tot is the
 reflexive and transitive closure of the relation ↩→tot .
    The new (HT.while) rule can be used to construct while loops that are totally correct. To under-
 stand it intuitively, note that the subprogram obtained by unrolling the loop body 𝑛 times (ignoring
 the initial measurement) satisfies the specification {𝑅𝑛 }□{B0 (𝑄)} , This can be interpreted as
 follows: if we start inside the loop and 𝑅𝑛 holds (with some probability), then the loop terminates
 within 𝑛 iterations in a state that satisfies 𝑄 (with at least that probability). We remark that the
 limit 𝑅 (which is easily seen to always exist) precisely satisfies the requirements on the “loop
 invariant” of the (HP.while) rule. See Section 4 for examples and Section 1.2 for related work on
 proving termination of probabilistic programs using loop invariant predicates.

 Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
QbC: Quantum Correctness by Construction                                                                      99:15


  The (HT.split) rule is more general than (HP.split) as it allows arbitrary non-negative 𝑝𝜔 that
need not add up to one.

3.3    Soundness of Refinement
We now show that the sets of rules given above are sound, meaning that each ensures the correctness
of constructed programs, in the following sense: if one starts with a specification, that is, a single
hole {𝑃 }□{𝑄 } , and repeatedly refines to construct a concrete program 𝑆 (i.e., a program without
holes), then the constructed program satisfies the initial specification, meaning that Hoare triple
{𝑃 }𝑆 {𝑄 } is correct. This holds for both partial and total correctness:
  Theorem 3.6 (Soundness of refinement for partial correctness). For any two predicates 𝑃, 𝑄
and any concrete program 𝑆, if {𝑃 }□{𝑄 } ↩→∗par 𝑆, then |=par {𝑃 }𝑆 {𝑄 }.

  Theorem 3.7 (Soundness of refinement for total correctness). For any two predicates 𝑃, 𝑄
and any concrete program 𝑆, if {𝑃 }□{𝑄 } ↩→∗tot 𝑆 then |=tot {𝑃 }𝑆 {𝑄 }.
  Theorems 3.6 and 3.7 are proved by induction over the length of the refinement chain, with the
(HP.while) and (HT.while) rules being most delicate. The detailed proofs can be found in Appendix A.

3.4    Completeness of Refinement
We now show that the refinement rules given above are complete, meaning that they allow us
to construct any correct program, in the following sense: if one has a concrete program 𝑆 (i.e., a
program without holes) such that the Hoare triple {𝑃 }𝑆 {𝑄 } is correct, then the program can be
constructed from {𝑃 }□{𝑄 } by applying a finite number of refinements. Formally, we have the
following results:
   Theorem 3.8 (Completeness of refinement for partial correctness). For any two predicates
𝑃, 𝑄 and any concrete program 𝑆, if |=par {𝑃 }𝑆 {𝑄 } then {𝑃 }□{𝑄 } ↩→∗par 𝑆.

  Theorem 3.9 (Completeness of refinement for total correctness). For any two predi-
cates 𝑃, 𝑄 and any concrete program 𝑆, if |=tot {𝑃 }𝑆 {𝑄 } then {𝑃 }□{𝑄 } ↩→∗tot 𝑆.
  Theorems 3.8 and 3.9 can be proved by induction on the structure of the program, with the while
construct requiring a careful analysis. The detailed proofs can be found in Appendix B.

4     Examples
In this section, we demonstrate how to use the QbC approach to construct quantum programs from
their specification. We first discuss a pedagogical example of a fair quantum coin. We then construct
a quantum teleportation protocol (Section 4.2) and two quantum search algorithms (Section 4.3).
We then describe new refinement rules to boost the success probability of quantum algorithms
(Section 4.4). This illustrates how QbC can be usefully extended by higher-level algorithmic patterns
and construction principles. Particularly for the more complicated algorithms, we find that the QbC
approach allows naturally discovering program detail on the fly, without explicitly using a priori
knowledge of the final algorithms. It also suggests key design decisions that give rise to different
quantum programs satisfying the same specification. Additionally, in Appendix D we discuss how
the running example from Section 2 can be constructed from a structured specification.

4.1    Fair Quantum Coin
A fair quantum coin is a program that prepares a quantum bit in a state that, when measured, gives
rise to either outcome with 50% probability. There are√infinitely many such states, but two natural
ones are the Hadamard basis states |±⟩ = (|0⟩ ± |1⟩)/ 2. We use a single qubit quantum variable 𝑞.

                           Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
99:16                                                                   Anurudh Peduri, Ina Schaefer, and Michael Walter


  Specification. To specify that each outcome occurs with 50% probability, we can use the following
program with a single hole:
                                     𝑆 fair-coin = {𝐼 /2}□{|𝑥⟩⟨𝑥 |} ,
where 𝑥 ∈ {0, 1} is a formal parameter (see Section 2.5). Indeed, suppose we manage to refine the
above into a program 𝑆 ′ without holes which does not explicitly use the parameter 𝑥. Then our
soundness result (Theorem 3.7) guarantees that the Hoare triple
                                                  {𝐼 /2}𝑆 ′ {|𝑥⟩⟨𝑥 |}
is valid for every 𝑥 ∈ {0, 1}, meaning that if we run the program (on an arbitrary state) and measure
the qubit, we obtain either outcome 𝑥 ∈ {0, 1} with probability at least, and hence equal to 12 .
   Construction. The well-known idea is that the Hadamard gate
                                                       
                                              1 1 1
                                       𝐻=√                                                     (4.1)
                                               2 1 −1
maps the standard basis to the Hadamard basis, which allows us to realize the coin toss. To confirm
this, we consider the following sequence of refinements:
                                  𝑆 fair-coin ↩→tot {𝐼 /2}□{𝑅}; {𝑅}□{|𝑥⟩⟨𝑥 |}                                  (H.seq)
                                            ↩→tot 𝑞 := |0⟩ ; {𝑅}□{|𝑥⟩⟨𝑥 |}                                     (H.init)
                                            ↩→tot 𝑞 := |0⟩ ; 𝑞 := 𝐻 (𝑞)                                       (H.unit)
The first refinement is always valid, but how should we pick the predicate 𝑅 so that the subsequent
                                                                       Í
refinements can be applied? To apply (H.init), we need that 𝐼 /2 ⇒ 𝑦 ∈ {0,1} |𝑦⟩⟨0| 𝑅 |0⟩⟨𝑦|, meaning
that ⟨0|𝑅|0⟩ ≥ 12 for 𝑥 ∈ {0, 1}. To apply (H.unit), we should choose 𝑅 such that 𝑅 ⇒ 𝐻 |𝑥⟩⟨𝑥 | 𝐻 .
Since the latter is a pure state, this suggests 𝑅 = 𝐻 |𝑥⟩⟨𝑥 | 𝐻 (which is also the weakest precondition
for the Hadamard subprogram and postcondition), and for this choice we have that ⟨0|𝑅|0⟩ =
|⟨0|𝐻 |𝑥⟩| 2 = 12 . Thus the above refinements are valid and we have constructed a program that
implements the fair coin toss specification correctly, by construction.
                                      𝑆 fair-coin ↩→∗tot 𝑞 := |0⟩ ; 𝑞 := 𝐻 (𝑞) ,

4.2     Quantum Teleportation
Imagine two parties, Alice and Bob, who share a maximally entangled state, say qubits 𝑎, 𝑏 in state
                                              1
                                     |𝜙 + ⟩ = √ (|00⟩ + |11⟩).                                 (4.2)
                                               2
Alice has another qubit 𝑞 in an unknown quantum state, and wants to transfer its state to Bob’s
qubit 𝑏, by sending only classical information but utilizing the maximally entangled state as a
resource. Furthermore, if 𝑞 was correlated or entangled with other quantum variables, then after
teleportation the same should be true for 𝑏. This is called quantum teleportation and is a basic
building block for quantum communication (see, e.g., Nielsen and Chuang [48]).
   Specification. To specify teleportation, consider an arbitrary quantum state 𝜌 between Alice’s and
some arbitrary other quantum variable 𝑟 , which does not participate in the protocol (in quantum
information, 𝑟 is called a reference system). After teleportation, we want the state of Bob’s qubit 𝑏
and 𝑟 to be in the same state. Without loss of generality, we can take 𝜌 to be a maximally entangled
state, 𝜌 = |𝜙 + ⟩⟨𝜙 + | (that is, it suffices to realize “entanglement swapping”). Indeed, a basic principle
of quantum information theory asserts that if two quantum programs (completely positive maps)
have the same behavior when applied to one half of a maximally entangled state, then they must

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
QbC: Quantum Correctness by Construction                                                                           99:17


have the same behavior on all states [48, 76]. Recall from Lemma 2.10 that we can assert that
quantum variables are in a given pure state by using its projection as the predicate. This translates
to the following initial specification:
                           𝑆 teleport = {|𝜙 + ⟩⟨𝜙 + |𝑞𝑟 ⊗ |𝜙 + ⟩⟨𝜙 + |𝑎𝑏 }□{|𝜙 + ⟩⟨𝜙 + |𝑏𝑟 }                      (4.3)
   Now, an arbitrary program that meets the above specification will not be a teleportation protocol,
since in teleportation we want to constrain all quantum operations to Alice and Bob’s variables,
while only allowing them to communicate classical bits from Alice to Bob. This disallows, e.g.,
simply swapping qubits 𝑞 and 𝑏 by applying a quantum gate. We can implement this latter constraint
by the following sequence of refinements to obtain a program with two holes, where the first hole
will be further refined by a program acting only on Alice’s qubits 𝑞 and 𝑎, and the second hole by a
program acting only on Bob’s qubit 𝑏:
                  𝑆 teleport ↩→tot {|𝜙 + ⟩⟨𝜙 + |𝑞𝑟 ⊗ |𝜙 + ⟩⟨𝜙 + |𝑎𝑏 }□{𝑃 }; {𝑃 }□{|𝜙 + ⟩⟨𝜙 + |𝑏𝑟 }             (H.seq)
                           {|𝜙 + ⟩⟨𝜙 + |𝑞𝑟 ⊗ |𝜙 + ⟩⟨𝜙 + |𝑎𝑏 }□{𝑃 };
                   ↩→tot                                                                        ,             (H.case)
                           case meas 𝑞, 𝑎 of (𝑥, 𝑦) : {𝑄 (𝑥, 𝑦)}□{|𝜙 + ⟩⟨𝜙 + |𝑏𝑟 } end
where 𝑥, 𝑦 ∈ {0, 1} for arbitrary predicates 𝑄 (𝑥, 𝑦). We can ensure that (H.case) is valid by taking
                                    ∑︁
                               𝑃 :=     |𝑥𝑦⟩⟨𝑥𝑦|𝑞𝑎 𝑄 (𝑥, 𝑦) |𝑥𝑦⟩⟨𝑥𝑦|𝑞𝑎 .                         (4.4)
                                           𝑥,𝑦
                                       ′
We have arrived at the specification 𝑆 teleport which refines Eq. (4.3),

                                 {|𝜙 + ⟩⟨𝜙 + |𝑞𝑟 ⊗ |𝜙 + ⟩⟨𝜙 + |𝑎𝑏 }□{𝑃 };
                                 |                 {z                 }
                   ′                              𝑆 Alice
                 𝑆 teleport =
                                 case meas 𝑞, 𝑎 of (𝑥, 𝑦) : {𝑄 (𝑥, 𝑦)}□{|𝜙 + ⟩⟨𝜙 + |𝑏𝑟 } end
                                                            |         {z              }
                                                                            𝑆 Bob,𝑥,𝑦

which consists of three steps:
  (1) Alice first applies some quantum program 𝑆 Alice (which will be constructed to only act on
      her qubits).
  (2) Alice measures her qubits 𝑞, 𝑎 in the standard basis (without loss of generality) and obtains
      as outcomes two classical bits 𝑥, 𝑦, which we imagine she communicates to Bob.
  (3) Bob applies another quantum program 𝑆 Bob,𝑥,𝑦 (which will be constructed to only act on his
      qubit) that is allowed to explicitly depend on the outcomes 𝑥 and 𝑦.
This precisely captures the structure as well as functionality of a quantum teleportation protocol.
  Construction. Before starting the construction we first simplify the precondition 𝑄 (𝑥, 𝑦) of Bob’s
program. As the latter is run straight after Alice’s measurements, which yielded outcomes 𝑥, 𝑦, we
know that Alice’s qubits must be in state |𝑥, 𝑦⟩. This motivates and in fact implies that we may take
                                         𝑄 (𝑥, 𝑦) = |𝑥𝑦⟩⟨𝑥𝑦|𝑞𝑎 ⊗ 𝑅𝑏𝑟 (𝑥, 𝑦)                                       (4.5)
for certain predicates 𝑅𝑏𝑟 (𝑥, 𝑦) on qubits 𝑏, 𝑟 that still need to be determined.
   To construct Alice and Bob’s programs, we make the straightforward guess that each applies
some unitary, which in Bob’s case may depend on the measurement outcomes 𝑥, 𝑦. Thus we refine
          𝑆 Alice ↩→tot 𝑞, 𝑎 := 𝑉 (𝑞, 𝑎)           and        𝑆 Bob,𝑥,𝑦 ↩→tot 𝑏 := 𝑈 (𝑥, 𝑦) (𝑏) ,             (H.unit)

                                Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
99:18                                                                    Anurudh Peduri, Ina Schaefer, and Michael Walter


where 𝑉 is a two-qubit unitary and the 𝑈 (𝑥, 𝑦) are one-qubit unitaries that we still need to construct.
The second refinement is valid assuming 𝑈𝑏 (𝑥, 𝑦)𝑄 (𝑥, 𝑦)𝑈𝑏† (𝑥, 𝑦) ⇒ |𝜙 + ⟩⟨𝜙 + |𝑏𝑟 , which by Eq. (4.5)
we can satisfy by picking
                                    𝑅𝑏𝑟 (𝑥, 𝑦) = 𝑈𝑏† (𝑥, 𝑦) |𝜙 + ⟩⟨𝜙 + |𝑏𝑟 𝑈𝑏 (𝑥, 𝑦).
By Eq. (4.4), this in turn implies that
                              ∑︁
                           𝑃=      |𝑥𝑦⟩⟨𝑥𝑦|𝑞𝑎 ⊗ 𝑈𝑏† (𝑥, 𝑦) |𝜙 + ⟩⟨𝜙 + |𝑏𝑟 𝑈𝑏 (𝑥, 𝑦).                                (4.6)
                                    𝑥,𝑦

                                                                         †
The first refinement is valid if 𝑉𝑞𝑎 (|𝜙 + ⟩⟨𝜙 + |𝑞𝑟 ⊗ |𝜙 + ⟩⟨𝜙 + |𝑎𝑏 )𝑉𝑞𝑎 ⇒ 𝑃. As the left-hand side is a pure
state, Lemma 2.10 shows that this condition is equivalent to
                                                     ∑︁
                +     +     †        +        +                            +                 +     + 2
         1 = ⟨𝜙𝑞𝑟 ⊗ 𝜙𝑎𝑏  |𝑉𝑞𝑎 𝑃𝑉𝑞𝑎 |𝜙𝑞𝑟 ⊗ 𝜙𝑎𝑏    ⟩=      |⟨𝑥𝑞 ⊗ 𝑦𝑎 ⊗ 𝜙𝑏𝑟     |𝑈𝑏 (𝑥, 𝑦)𝑉𝑞𝑎 |𝜙𝑞𝑟 ⊗ 𝜙𝑎𝑏 ⟩|
                                                           𝑥,𝑦
                                                           ∑︁
                                                                              +             𝑇    +     + 2
                                                       =         |⟨𝑥𝑞 ⊗ 𝑦𝑎 ⊗ 𝜙𝑏𝑟 |𝑈𝑏 (𝑥, 𝑦)𝑉𝑟𝑏 |𝜙𝑞𝑟 ⊗ 𝜙𝑎𝑏 ⟩|
                                                           𝑥,𝑦
                                                           1 ∑︁ +
                                                       =                       𝑇
                                                                |⟨𝜙 |𝑈𝑏 (𝑥, 𝑦)𝑉𝑟𝑏 |𝑥𝑟 ⊗ 𝑦𝑏 ⟩| 2,                    (4.7)
                                                           4 𝑥,𝑦 𝑏𝑟

where we first used Eq. (4.6) and then the identity 𝑉𝑞𝑎 |𝜙𝑞𝑟  + ⊗ 𝜙 + ⟩ = 𝑉 𝑇 |𝜙 + ⊗ 𝜙 + ⟩, known as the
                                                                      𝑎𝑏     𝑟𝑏 𝑞𝑟      𝑎𝑏
“transpose trick”, which allows moving an arbitrary operator acting on qubits 𝑞, 𝑎 to the other side of
the maximally entangled states, that is, to act on qubits 𝑟, 𝑏, if we replace the operator by its transpose
(in the computational basis). This well-known identity    √ is easily verified by direct calculation.
                                                                                                  √    The
                                              + ⟩ = |𝑥 ⟩ / 2 and similarly ⟨𝑦 | |𝜙 + ⟩ = |𝑥 ⟩ / 2. Since
final step follows by observing that ⟨𝑥𝑞 | |𝜙𝑞𝑟       𝑟                          𝑎   𝑎𝑏      𝑏
all of the summands in Eq. (4.7) are at most one, they must all be equal to one. In other words,
                                           𝑇
                                          𝑉𝑟𝑏 |𝑥𝑦⟩𝑟𝑏       and 𝑈𝑏† (𝑥, 𝑦) |𝜙𝑏𝑟
                                                                            +
                                                                               ⟩
must be the same states for all 𝑥, 𝑦 ∈ {0, 1} (up to irrelevant overall phases). Note that the left-hand
side states make up an orthonormal basis, while the right-hand states are all maximally entangled
(since they obtained by applying a unitary to one of the qubits of |𝜙 + ⟩). It follows that we should
       𝑇 to be a unitary that maps the standard basis to a basis of maximally entangled states. And
pick 𝑉𝑟𝑏
this is also sufficient since any two maximally entangled states differ by a unitary on either of
the qubits. As is well known, the Bell basis consists of maximally entangled states and it can be
prepared by the unitary 𝑉𝑟𝑏 𝑇 = CNOT 𝐻 . Thus we take
                                       𝑟𝑏 𝑏

                                                𝑉 = (𝐻 ⊗ 𝐼 )CNOT.
Finally, we note that the Bell states can be obtained from the standard maximally entangled state
    𝑇 |𝑦𝑥⟩       𝑦 𝑥    +
as 𝑉𝑟𝑏     𝑟𝑏 = 𝑍𝑏 𝑋𝑏 |𝜙 ⟩𝑟𝑏 , where 𝑋 and 𝑍 denote the Pauli 𝑋 and 𝑍 matrices. Thus Bob’s unitaries
should be
                                          𝑈 (𝑥, 𝑦) = 𝑋 𝑥 𝑍 𝑦 .
Altogether, we have constructed the following program, which is nothing but the standard protocol
for quantum teleportation:

  ′
                    𝑞, 𝑎 := (𝐻 ⊗ 𝐼 )CNOT(𝑞, 𝑎);
𝑆 teleport ↩→∗tot
                    case meas (𝑞, 𝑎) of 00 : 𝑏 := 𝐼 (𝑏); 01 : 𝑏 := 𝑍 (𝑏); 10 : 𝑏 := 𝑋 (𝑏); 11 : 𝑏 := 𝑋𝑍 (𝑏) end
As it was obtained by refinement, it satisfies the specification by construction.

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
QbC: Quantum Correctness by Construction                                                                      99:19


4.3   Quantum Search
We consider the following search problem [30, 48]. Given query access to a Boolean function or
“database” 𝑓 : {0, 1}𝑛 → {0, 1}, we wish to find a bitstring 𝑥 ∈ {0, 1}𝑛 such that 𝑓 (𝑥) = 1. Such an 𝑥
is often called a “solution” or “marked element”. In the quantum setting, we are given query access
to 𝑓 via the following standard quantum oracle unitary, O𝑓 |𝑥⟩ 𝒒 |𝑦⟩𝑎 = |𝑥⟩ 𝒒 |𝑦 ⊕ 𝑓 (𝑥)⟩𝑎 , or by the
following phase oracle unitary
                                           𝑃 𝑓 |𝑥⟩ 𝒒 = (−1) 𝑓 (𝑥 ) |𝑥⟩ 𝒒 ,                                   (4.8)
which can be obtained from the former in a straightforward fashion. Here, 𝒒 is a quantum variable
consisting of 𝑛 qubits. Let us define 𝑁 = 2𝑛 as the size of the search space, and 𝑇 = |{𝑥 : 𝑓 (𝑥) = 1}|
as the number of solutions. In the example constructions below, we will assume knowledge of this
number of solutions. In the following, we will first present a specification of the search problem,
and then construct two different programs that satisfy the specification by construction: a simple
algorithm based on random sampling and Grover’s celebrated quantum search algorithm [30].
  Specification. The search problem can be specified as follows:
                                                   Í
                             𝑆 search (𝑝) = {𝑝𝐼 }□{ 𝑥:𝑓 (𝑥 )=1 |𝑥⟩⟨𝑥 | 𝒒 } ,
It states that if we measure the state after program execution, we obtain a solution 𝑥 with probability
at least 𝑝. Thus, 𝑝 is the probability of success of the search algorithm. In our constructions below,
we treat 𝑝 as a parameter that will naturally be selected during the refinement process. Note that
whatever the value of 𝑝, such an algorithm (if it terminates) can always be amplified or “boosted”
to any desired success probability by repeating it sufficiently often until it finds a solution. We
discuss this in Section 4.4 below and propose refinement rules to automate this reasoning.
  Construction I: Random Sampling. One can solve the search problem by sampling 𝑥 ∈ {0, 1}𝑛
uniformly at random. Clearly, this succeeds with probability 𝑇 /𝑁 . One wayÍto achieve this by
a quantum program is by preparing the uniform superposition |𝑈 ⟩ = √1 𝑥 ∈ {0,1}𝑛 |𝑥⟩, since
                                                                                   𝑁
measuring this state in the standard basis will yield a uniformly random 𝑥 ∈ {0, 1}𝑛 . We can
confirm that this construction works with the aforementioned success probability, by refining the
specification into a program that prepares the state |𝑈 ⟩. This can be done by first initializing all
qubits in the zero state and then applying Hadamard gates 𝐻 (Eq. (4.1)) to all of the qubits:
                                                            Í
                        𝑆 search (𝑝) ↩→tot {𝑝𝐼 }□{𝑅}; {𝑅}□{ 𝑥:𝑓 (𝑥 )=1 |𝑥⟩⟨𝑥 | 𝒒 }           (H.seq)
                                                           Í
                                     ↩→tot 𝒒 := |0⟩ ; {𝑅}□{ 𝑥:𝑓 (𝑥 )=1 |𝑥⟩⟨𝑥 | 𝒒 }           (H.init)
                                ↩→tot 𝒒 := |0⟩ ; 𝒒 := 𝐻 ⊗𝑛 (𝒒)                                (H.unit)
                                      Í
To apply (H.init), we need that 𝑝𝐼 ⇒ 𝑥 |𝑥⟩⟨0| 𝒒 𝑅 |0⟩⟨𝑥 | 𝒒 , that is, 𝑝 ≤ ⟨0|𝑅|0⟩. To apply (H.unit),
we can choose
                                          © ∑︁
                                 𝑅 = 𝐻 ⊗𝑛 ­           |𝑥⟩⟨𝑥 | 𝒒 ®𝐻 ⊗𝑛 .
                                                                ª

                                          «𝑥:𝑓 (𝑥 )=1           ¬
Thus the above refinements are valid if
                                                 ∑︁                      𝑇
                           𝑝 ≤ ⟨0|𝑅|0⟩ = ⟨𝑈 |            |𝑥⟩⟨𝑥 | 𝒒 |𝑈 ⟩ = .
                                                                         𝑁
                                                      𝑥:𝑓 (𝑥 )=1

Thus we should pick 𝑝 := 𝑇 /𝑁 to maximize the success probability. Altogether, we have constructed
a search algorithm that succeeds with probability 𝑝 = 𝑇 /𝑁 . As mentioned earlier and will be
discussed in detail in Section 4.4, by repeating the above 𝑂 (𝑁 /𝑇 ) times until we find a solution,

                           Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
99:20                                                                    Anurudh Peduri, Ina Schaefer, and Michael Walter


we can obtain a program that solves the search problem with any desired constant probability of
success (say, 𝑝 = 2/3) at a cost of 𝑂 (𝑁 /𝑇 ) queries.
   Construction II: Grover Search. Grover [30] proposed a quantum algorithm for the search problem
which gives a quadratic speedup over random sampling. In the following, we will re-construct this
algorithm by making natural choices using one key idea at a time.
   Step 1. The first observation is that while the uniform superposition |𝑈 ⟩ over all bitstrings is
easy to prepare, what we are really after is the uniform superposition of all solutions, that is, the
                        Í
“good” state |𝐺⟩ = √1 𝑥 s.t. 𝑓 (𝑥 )=1 |𝑥⟩. Indeed, measuring |𝐺⟩ will yield a solution with probability
                      𝑇
one. We can formalize this idea by strengthening the postcondition of the specification:
                            𝑆 search (𝑝) ↩→tot {𝑝𝐼 }□{|𝐺⟩⟨𝐺 |} =: 𝑆 good (𝑝),                     (H.sw)
                                                       Í
We may apply (H.sw) since the condition |𝐺⟩⟨𝐺 | ⇒ 𝑥 s.t. 𝑓 (𝑥 )=1 |𝑥⟩⟨𝑥 | is satisfied. Indeed, the good
state |𝐺⟩ is clearly contained in the span of the basis states |𝑥⟩ corresponding to solutions 𝑥.
   Step 2. The uniform state |𝑈 ⟩ (which is easy to prepare, but not very useful) and the good state |𝐺⟩
(which solves the problem, but is a priori unclear how to prepare) span a two-dimensional subspace
of the exponentially large Hilbert space. The key idea (which has no classical counterpart) then is
to try to rotate the state |𝑈 ⟩ onto |𝐺⟩ in this two-dimensional subspace.
   To realize this idea, we first define an orthonormal basis of the two-dimensionalÍ         subspace by
picking |𝐺⟩ and a vector orthogonal to it, namely the “bad state” |𝐵⟩ = √ 1           𝑥 s.t. 𝑓 (𝑥 )=0 |𝑥⟩. At
                                                                               𝑁 −𝑇
any stage of the program, we would like the state of 𝒒 to be of the form
                                               |𝜃 ⟩ = cos 𝜃 |𝐵⟩ + sin 𝜃 |𝐺⟩
for some angle 𝜃 , which will serve as a loop variant
                                                   √︁ in the following. The plan is now to prepare
the
√︁   uniform  state, which
                     √︁     has   angle 𝜐 = arcsin   𝑇 /𝑁 ∈ [0, 𝜋/2] as it can be written as |𝑈 ⟩ =
   (𝑁 − 𝑇 )/𝑁 |𝐵⟩ + 𝑇 /𝑁 |𝐺⟩, and then rotate it repeatedly by some angle 𝛿 > 0 towards the good
state |𝐺⟩, which is at angle 𝜋2 . We can formalize this by the following refinements:
        𝑆 good (𝑝) ↩→tot {𝑝𝐼 }□{|𝜃 0 ⟩⟨𝜃 0 |}; {|𝜃 0 ⟩⟨𝜃 0 |}□{| 𝜋2 ⟩⟨ 𝜋2 |}                                    (H.seq)
                   ↩→tot {𝑝𝐼 }□{|𝜃 0 ⟩⟨𝜃 0 |}; repeat 𝑟 do {|𝜃 𝑗 ⟩⟨𝜃 𝑗 |}□{|𝜃 𝑗+1 ⟩⟨𝜃 𝑗+1 |} end             (H.repeat)
                         |     {z          }               |              {z              }
                                    𝑆 init                                     𝑆 rotate (𝛿 )

To apply (H.repeat), we choose 𝜃 𝑟 = 𝜋2 and 𝜃 𝑗+1 = 𝜃 𝑗 + 𝛿 for some arbitary rotation angle 𝛿 and
number of rotations 𝑟 that we will determine later. Hence 𝜃 0 = 𝜋2 − 𝑟𝛿.
   We first construct the 𝑆 init program. Following the plan, we prepare the uniform superposi-
tion |𝑈 ⟩ = |𝜐⟩, which we already know how to do from above:
                                        𝑆 init ↩→tot {𝑝𝐼 }□{𝑅}; {𝑅}□{|𝜃 0 ⟩⟨𝜃 0 |}                              (H.seq)
                                             ↩→tot 𝒒 := |0⟩ ; {𝑅}□{|𝜃 0 ⟩⟨𝜃 0 |}                                (H.init)
                                             ↩→tot 𝒒 := |0⟩ ; 𝒒 := 𝐻 ⊗𝑛 (𝒒)                                    (H.unit)
Since the postcondition is different from the above, we also need to choose 𝑅 differently, but we can
follow the same reasoning. In order to apply (H.init), we need that 𝑝 ≤ ⟨0|𝑅|0⟩, and to apply (H.unit)
we can choose 𝑅 = 𝐻 ⊗𝑛 |𝜃 0 ⟩⟨𝜃 0 | 𝐻 ⊗𝑛 . Together, we find that the maximum success probability for
which the above refinements are valid is given by
                                                                            𝜋         
                   𝑝 := ⟨0|𝑅|0⟩ = |⟨0|𝐻 ⊗𝑛 |𝜃 0 ⟩| 2 = |⟨𝜐 |𝜃 0 ⟩| 2 = cos2    − 𝑟𝛿 − 𝜐 .
                                                                             2

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
QbC: Quantum Correctness by Construction                                                                      99:21


To maximize this probability, we should further choose 𝑟 such that the right-hand side is maximized.
We will pick 𝑟 such that the angle in the cosine is closest to 0:
                                                𝜋
                                                    −𝜐
                                                        
                                           𝑟 := 2         ,                                    (4.9)
                                                    𝛿
where [·] rounds to the nearest integer. Clearly, 𝑝 ≥ cos2 (𝛿/2).
  Step 3. We still need to construct the program 𝑆 rotate (𝛿) for some rotation angle 𝛿. To this end,
we first observe that it suffices to construct a program that satisfies the stronger specification:
                                   ′
                                 𝑆 rotate (𝛿) = {|𝜃 ⟩⟨𝜃 |}□{|𝜃 + 𝛿⟩⟨𝜃 + 𝛿 |}.
Indeed, programs satisfying this specification rotate all states |𝜃 ⟩ in the two-dimensional subspace
by 𝛿, as opposed just the states |𝜃 𝑗 ⟩ for 𝑗 ∈ {0, 1, . . . , 𝑁 − 1}.
   How can we obtain such a rotation? Observe that the quantum phase oracle 𝑃 𝑓 in Eq. (4.8) is
a reflection about the vector |𝐵⟩, as it maps 𝑃 𝑓 |𝜃 ⟩ = |−𝜃 ⟩. Now, we know that two reflections
make a rotation. For our second reflection we simply pick some known state (independent of the
instance of the search problem) to reflect about. A natural choice is |𝑈 ⟩, since the corresponding
reflection 2 |𝑈 ⟩⟨𝑈 | −𝐼 can be efficiently implemented using 𝑂 (𝑛) gates. Thus we introduce these two
reflections in sequence and determine the rotation angle from the conditions of the refinements:
                   ′
                 𝑆 rotate (𝛿) ↩→tot {|𝜃 ⟩⟨𝜃 |}□{|−𝜃 ⟩⟨−𝜃 |}; {|−𝜃 ⟩⟨−𝜃 |}□{|𝜃 + 𝛿⟩⟨𝜃 + 𝛿 |}               (H.seq)
                            ↩→tot 𝒒 := 𝑃 𝑓 (𝒒); {|−𝜃 ⟩⟨−𝜃 |}□{|𝜃 + 𝛿⟩⟨𝜃 + 𝛿 |}                           (H.unit)
                            ↩→tot 𝒒 := 𝑃 𝑓 (𝒒); 𝒒 := (2 |𝑈 ⟩⟨𝑈 | − 𝐼 ) (𝒒)                               (H.unit)
The first application of (H.unit) is correct by our choice of intermediate condition, but for the
second one we need that
                       (2 |𝑈 ⟩⟨𝑈 | − 𝐼 ) |−𝜃 ⟩⟨−𝜃 | (2 |𝑈 ⟩⟨𝑈 | − 𝐼 ) ⇒ |𝜃 + 𝛿⟩⟨𝜃 + 𝛿 | .
Since |𝑈 ⟩ is at angle 𝜐, reflecting about it sends |−𝜃 ⟩ = |𝜐 − (𝜃 + 𝜐)⟩ to |𝜐 + (𝜃 + 𝜐)⟩ = |𝜃 + 2𝜐⟩.
Thus the above√︁refinements are valid if we choose 𝛿 = 2𝜐 as the rotation angle, where we recall
that 𝜐 = arcsin 𝑇 /𝑁 . If we plug this back into Eq. (4.9) we find that the number of rotations is
                              𝜋      "                      #      √︂ !
                                2 −𝜐             𝜋          1           𝑁
                         𝑟=            =           √︁     −     =𝑂          .
                                 2𝜐       4 arcsin 𝑇 /𝑁 2               𝑇
Moreover, the success probability can be lower bounded as
                               𝑝 ≥ cos2 (𝛿/2) = 1 − sin2 (𝜐) = 1 − 𝑇 /𝑁 .
Thus we obtain the following quantum program:
                                               𝒒 := |0⟩ ; 𝒒 := 𝐻 ⊗𝑛 (𝒒);
                                                                          
                                                            𝜋√         1
                                  𝑇            repeat                 − 2 do
                     𝑆 search 1 −     ↩→∗tot             4 arcsin   𝑇 /𝑁
                                  𝑁
                                                 𝒒 := 𝑃 𝑓 (𝒒); 𝒒 := (2 |𝑈 ⟩⟨𝑈 | − 𝐼 ) (𝒒)
                                               end
As we have constructed it by refining the initial specification for the search problem,√︁it satisfies the
specification by construction. It succeeds with probability 𝑝 ≥ 1 − 𝑇 /𝑁 and uses 𝑂 ( 𝑁 /𝑇 ) queries
to the quantum oracle. This is in fact Grover’s algorithm [30].

                           Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
99:22                                                               Anurudh Peduri, Ina Schaefer, and Michael Walter


4.4     Boosting Success Probabilities
In this section, we derive two refinement rules that formalize useful and widely used patterns (see,
e.g., [41, 52]). To motivate it, recall that in the preceding example, we constructed two quantum pro-
grams that succeed with some probability. We modeled this by a specification of the form {𝜀𝐼 }□{𝑄 }
for some 𝜀 > 0 (we now write 𝜀 rather than 𝑝 because the discussion that follows is most relevant
when 𝜀 is a small probability). Indeed, a Hoare triple {𝜀𝐼 }𝑆 {𝑄 } is totally correct if the program 𝑆
terminates and the postcondition 𝑄 holds with probability at least 𝜀. We can amplify or “boost” the
success probability of such a program 𝑆 arbitrarily by simply repeating it until the postcondition
holds, provided (i) the program 𝑆 terminates almost surely (so that we keep repeating) and (ii) the
postcondition is given by a projection (so that measuring it does not impact its expectation). To
incorporate the termination requirement we can consider the multiple specification {𝜀𝐼, 𝐼 }□{𝑄, 𝐼 } .
   We first give a rule that reduces the construction of a program that succeeds with some probabil-
ity 𝑝 ∈ (0, 1) to the construction of a program that succeeds with some smaller probability 𝜀 ∈ (0, 𝑝):
                                           repeat ⌈log1−𝜀 (1 − 𝑝)⌉ do
(H.boostRep) {𝑝𝐼, 𝐼 }□{𝑄 𝒒 , 𝐼 } ↩→∗tot         if meas 𝒒 with 𝑄 ⊥ then {𝜀𝑄 𝒒⊥, 𝑄 𝒒⊥ }□{𝑄 𝒒 , 𝐼 } end ,
                                       end
      for any projection 𝑄 and any 𝜀 ∈ (0, 𝑝), where 𝑄 ⊥ = 𝐼 − 𝑄
Second, we give a rule to reduce the construction of programs that succeed with probability one to
ones that succeed with some finite probability 𝜀 ∈ (0, 1), by repeating the program until it succeeds:
(H.boostWhile) {𝐼 }□{𝑄 𝒒 } ↩→∗tot while meas 𝒒 with 𝑄 ⊥ do {𝜀𝑄 𝒒⊥, 𝑄 𝒒⊥ }□{𝑄 𝒒 , 𝐼 } end ,
        for any projection 𝑄 and any 𝜀 ∈ (0, 1), where 𝑄 ⊥ = 𝐼 − 𝑄

   Theorem 4.1 (Boosting success probability). The relations (H.boostRep), (H.boostWhile) hold.
   The proof can be found in Appendix C. We emphasize that both rules are totally correct.

4.5     Quantum Fourier Transform
The Quantum Fourier Transform (QFT) is widely used in many algorithms, such as Shor’s factoring
algorithm [66] and quantum phase estimation [36]. For 𝑛 qubits, it computes the following unitary:
                                              1         ∑︁            𝑥𝑦
                                  QFT𝑛 = √                           𝜔𝑛 |𝑥⟩⟨𝑦|
                                              2𝑛 𝑥,𝑦 ∈ {0,...,2𝑛 −1}
                        
where 𝜔𝑛 = exp 2𝜋𝑖   2𝑛 . Here, theÍ
                                   𝑛-bit numbers 𝑥, 𝑦 are identified with big-endian bitstrings, that is,
|𝑥⟩ = |𝑥 1 ⟩⊗. . .⊗|𝑥𝑛 ⟩ where 𝑥 = 𝑛𝑗=1 𝑥 𝑗 2𝑛− 𝑗 . The key observation is that 𝜔𝑘2 = 𝜔𝑘 −1 , which naturally
motivates a recursive approach. Therefore, we will attempt to construct a program implementing
QFT𝑛 using a program for QFT𝑛−1 , and so. In this section only, we will use the shorthand notation
|Ψ⟩ to represent the predicate |Ψ⟩⟨Ψ|, which is a projection for any unit vector |Ψ⟩.
  Specification. As in the teleportation example (Section 4.2), we can fully specify the QFT by
considering its action on half of a maximally entangled input state. To allow us to recurse on the
number of qubits, we will define a specification for QFT𝑘 for each 𝑘 from 1 to 𝑛. To this end let 𝑆𝑘
denote the specification for applying QFT𝑘 on the first 𝑘 qubits of an 𝑛-qubit quantum variable 𝒒:
                            𝑆𝑘 = {|Φ𝑛+ ⟩ 𝒓,𝒒 }□{(QFT𝑘 )𝑞1,...,𝑞𝑘 |Φ𝑛+ ⟩ 𝒓,𝒒 } ,
                                          Í2𝑛 −1
where |Φ𝑛+ ⟩ 𝒓,𝒒 =        +                                            +
                   Ë𝑛
                                       √1
                    𝑗=1 |𝜙 ⟩𝑟 𝑗 ,𝑞 𝑗 = 2𝑛   𝑥=0 |𝑥⟩ 𝒓 |𝑥⟩ 𝒒 (with |𝜙 ⟩ as in Eq. (4.2)) is a maximally
entangled state between 𝒒 and an additional 𝑛-qubit variable 𝒓 that will not be used in the program.

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
QbC: Quantum Correctness by Construction                                                                                     99:23


Any program obtained by refining 𝑆𝑘 implements the QFT on the first 𝑘 qubits of 𝒒 while acting
trivially on the rest. In particular, 𝑆𝑛 specifies the 𝑛-qubit QFT.
   Construction. We will show that a quantum program for 𝑆𝑛 can be constructed recursively, starting
with 𝑆 1 and subsequently constructing a program for 𝑆𝑘 from one for 𝑆𝑘 −1 for any 𝑘 = 2, . . . , 𝑛.
                                                               Í
   Base Case (𝑘 = 1). As 𝜔 1 = −1, we can see that QFT1 = √1 𝑥,𝑦 ∈ {0,1} (−1)𝑥 𝑦 |𝑥⟩⟨𝑦| = 𝐻 straight
                                                             2
from the definition, i.e., the 1-qubit QFT is the Hadamard gate. Therefore, we can refine:
                                                    𝑆 1 ↩→tot 𝑞 1 := 𝐻 (𝑞 1 )                                          (H.unit)
                                                                                      
We can apply (H.unit) because 𝐻𝑞†1 (QFT1 )𝑞1 |Φ𝑛+ ⟩⟨Φ𝑛+ | 𝒓,𝒒 (QFT1 )𝑞†1 𝐻𝑞1 = |Φ𝑛+ ⟩⟨Φ𝑛+ | 𝒓,𝒒 holds.

  General Case (𝑘 > 1). We refine 𝑆𝑘 by using (H.seq) into a sequence of two holes, with intermediate
condition being the postcondition of 𝑆𝑘 −1 . Then the first hole in the sequence matches 𝑆𝑘 −1 :

                    𝑆𝑘 ↩→tot 𝑆𝑘 −1 ; {(QFT𝑘 −1 )𝑞1,...,𝑞𝑘 −1 |Φ𝑛+ ⟩ 𝒓,𝒒 }□{(QFT𝑘 )𝑞1,...,𝑞𝑘 |Φ𝑛+ ⟩ 𝒓,𝒒 }                   (H.seq)

The specification 𝑆𝑘 −1 can be refined recursively, but we still need to refine the right-hand side hole.
Let us denote the states defining the pre- and postcondition by |Ψ𝑘 −1 ⟩ := (QFT𝑘 −1 )𝑞1,...,𝑞𝑘 −1 |Φ𝑛+ ⟩ 𝒓,𝒒
and |Ψ𝑘 ⟩ := (QFT𝑘 )𝑞1,...,𝑞𝑘 |Φ𝑛+ ⟩ 𝒓,𝒒 , respectively. Because the program should only act on the first 𝑘
qubits, we expand these accordingly:
                                  −1 −1
                                2𝑘∑︁
                    © 1                    ∑︁
                                                    𝑥˜ 𝑦˜
         |Ψ𝑘 −1 ⟩ = ­       √                      𝜔𝑘 −1 |𝑥⟩                       ˜ 𝑞1,...,𝑞𝑘 −1 |𝑥𝑘 ⟩𝑞𝑘 ® ⊗ |Ψrest ⟩ ,
                                                          ˜ 𝑟 1,...,𝑟𝑘 −1 |𝑥𝑘 ⟩𝑟𝑘 |𝑦⟩
                                                                                                          ª
                      2𝑘 −1 2 𝑥,˜ 𝑦=0
                                   ˜    𝑥𝑘 ∈ {0,1}
                    «                                                                                     ¬
                           𝑘
                          2∑︁−1
                    ©1            𝑥𝑦
           |Ψ𝑘 ⟩ = ­ 𝑘          𝜔𝑘 |𝑥⟩𝑟 1,...,𝑟𝑘 |𝑦⟩𝑞1,...,𝑞𝑘 ® ⊗ |Ψrest ⟩ ,
                                                              ª
                      2
                    « 𝑥,𝑦=0                                   ¬
where |Ψrest ⟩ is the (unchanged) state on the last 𝑛 − 𝑘 qubits of 𝒓, 𝒒. To compare the state |Ψ𝑘 ⟩
with |Ψ𝑘 −1 ⟩, let us write 𝑥 = 2𝑥˜ + 𝑥𝑘 . Then we can also simplify
                                              𝑥𝑦          2𝑥˜ 𝑦   𝑥 𝑦     𝑥˜ 𝑦   𝑦𝑥
                                            𝜔𝑘 = 𝜔𝑘 𝜔𝑘 𝑘 = 𝜔𝑘 −1𝜔𝑘 𝑘 .
             𝑘 −1
Now as 𝜔𝑘2 −1 = 1, the most significant bit of 𝑦 does not affect the first part of the above term.
Therefore, it is natural to write the index 𝑦 as 𝑦 = 𝑦1 2𝑘 −1 + 𝑦,
                                                                ˜ so that we can further simplify
                                             𝑥˜ 𝑦    𝑦𝑥           𝑥˜ 𝑦˜          ˜
                                                                                 𝑦𝑥
                                           𝜔𝑘 −1𝜔𝑘 𝑘 = 𝜔𝑘 −1 (−1) 𝑦1𝑥𝑘 𝜔𝑘 𝑘 .
Altogether we find that the postcondition is described by the state
                 2𝑘 −1 −1
             © 1 ∑︁            ∑︁
                                          𝑥˜ 𝑦˜            ˜
                                                          𝑦𝑥
     |Ψ𝑘 ⟩ = ­ 𝑘                         𝜔𝑘 −1 (−1) 𝑦1𝑥𝑘 𝜔𝑘 𝑘 |𝑥⟩                               ˜ 𝑞2,...,𝑞𝑘 ® ⊗ |Ψrest ⟩ .
                                                               ˜ 𝑟 1,...,𝑟𝑘 −1 |𝑥𝑘 ⟩𝑟𝑘 |𝑦1 ⟩𝑞1 |𝑦⟩
                                                                                                            ª
               2 𝑥,˜ 𝑦=0
                     ˜    𝑥𝑘 ,𝑦1 ∈ {0,1}
             «                                                                                              ¬
The state |Ψ𝑘 ⟩ looks quite similar to |Ψ𝑘 −1 ⟩ but there are some key differences. For one, the index 𝑦˜
refers qubits 𝑞 2, . . . , 𝑞𝑘 rather than 𝑞 1, . . . , 𝑞𝑘 −1 and hence 𝑞 1 plays a distinguished role rather
than 𝑞𝑘 . Thus a natural first step is to move the 𝑘-th qubit to the front by applying a suitable
sequence of swaps. That is, we use (H.seq) and (H.unit) to refine
  {|Ψ𝑘 −1 ⟩}□{Ψ𝑘 } ↩→∗tot 𝑞𝑘 , 𝑞𝑘 −1 := SWAP(𝑞𝑘 , 𝑞𝑘 −1 ); . . . ; 𝑞 2, 𝑞 1 := SWAP(𝑞 2, 𝑞 1 ); {|Ψ′ ⟩}□{|Ψ𝑘 ⟩} ,

                                 Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
99:24                                                                     Anurudh Peduri, Ina Schaefer, and Michael Walter


which is allowed if we pick the intermediate condition given by the state
                              2𝑘∑︁−1 −1
                ′ © 1                      ∑︁       𝑥˜ 𝑦˜
           |Ψ ⟩ = ­       √                        𝜔𝑘 −1 |𝑥⟩                               ˜ 𝑞2,...,𝑞𝑘 ® ⊗ |Ψrest ⟩ .
                                                          ˜ 𝑟 1,...,𝑟𝑘 −1 |𝑥𝑘 ⟩𝑟𝑘 |𝑥𝑘 ⟩𝑞1 |𝑦⟩
                                                                                                       ª
                    2𝑘 −1   2 𝑥,˜ 𝑦=0
                  «                ˜    𝑥𝑘 ∈ {0,1}                                                     ¬
                                                                                                                            ˜
                                                                                                                            𝑦𝑥
Now the qubits are in the right place but we see that in |Ψ𝑘 ⟩ there is an additional relative phase 𝜔𝑘 𝑘 .
            ˜
            𝑦𝑥          𝑦
                        𝑘 −1 𝑦           𝑦
Because 𝜔𝑘 𝑘 = (𝜔𝑘 𝑘 𝜔𝑘 −1   . . . 𝜔 2 2 )𝑥𝑘 we are led to refining the second hole by a series of phase
gates, one on each qubit 𝑞 2, . . . , 𝑞𝑘 , and each controlled by the value 𝑥𝑘 that is stored in qubit 𝑞 1 :
      {|Ψ′ ⟩}□{|Ψ𝑘 ⟩} ↩→∗tot 𝑞 1, 𝑞 2 := CRz2 (𝑞 1, 𝑞 2 ); . . . ; 𝑞 1, 𝑞𝑘 := CRz𝑘 (𝑞 1, 𝑞𝑘 ); {|Ψ′′ ⟩}□{|Ψ𝑘 ⟩}
                     
where Rz𝑘 = 10 𝜔0𝑘 and CRz𝑘 denotes the corresponding controlled gate. The above refinement is
valid if pick the intermediate condition given by the state
                            2𝑘∑︁−1 −1
           ′′   © 1                      ∑︁       𝑥˜ 𝑦˜ ˜
                                                        𝑦𝑥
        |Ψ ⟩ = ­        √                        𝜔𝑘 −1𝜔𝑘 𝑘 |𝑥⟩                               ˜ 𝑞2,...,𝑞𝑘 ® ⊗ |Ψrest ⟩
                                                            ˜ 𝑟 1,...,𝑟𝑘 −1 |𝑥𝑘 ⟩𝑟𝑘 |𝑥𝑘 ⟩𝑞1 |𝑦⟩
                                                                                                         ª
                  2𝑘 −1   2 𝑥,˜ 𝑦=0
                «                ˜    𝑥𝑘 ∈ {0,1}                                                         ¬
This is almost identical toÍ|Ψ𝑘 ⟩, except that 𝑞 1 is in a basis state rather than a suitable superposition.
As we have 𝐻 |𝑥𝑘 ⟩ = √1 𝑦1 (−1)𝑥𝑘 𝑦1 |𝑦1 ⟩ by definition, this is easily fixed by a Hadamard gate:
                            2

                                        {|Ψ′′ ⟩}□{|Ψ𝑘 ⟩} ↩→tot 𝑞 1 := 𝐻 (𝑞 1 ) .                                        (H.unit)
This concludes the construction of the quantum Fourier transform.

5   Conclusion and Outlook
In this work, we proposed Quantum Correctness by Construction (QbC), an approach for construct-
ing quantum programs that are guaranteed to be correct by construction. To this end, we extended
a quantum while language with a construct called holes, which represent yet-to-be-constructed
subprograms that carry a precondition and a postcondition. We presented refinement rules that
iteratively refine such quantum programs and proved that these rules are sound and complete:
every program is guaranteed to satisfy the specification it was constructed from, and every correct
program can always be constructed from the specification. Finally, we demonstrated the QbC
approach by constructing quantum programs for some idiomatic problems, starting from their
natural specification. We found that in these examples, QbC naturally suggested how to derive
program details and highlighted key design choices that had to be made along the way. We take
these findings to suggest that QbC could play a meaningful role in supporting the design of quantum
algorithms, their taxonomization, and the construction and verification of larger quantum software.
We now describe some promising directions for future research to further pave the way in this
direction and conclude with a perspective on the role of automation in algorithm development.
   Future Directions: Theory. A natural and interesting direction would be to extend the QbC
methodology to other settings and non-functional properties, such as by building on the expected-
runtime calculus introduced by Liu et al. [42] to construct programs that are efficient by construction.
Another direction would be to extend the QbC approach to other quantum programming languages.
While the quantum while language used in our paper is well-understood to provide a clean theoretical
model, it is often cumbersome to express complex quantum programs in it. It would therefore be
desirable to extend QbC to a more expressive language, which might include both classical and
quantum variables [24], oracles and subroutines, quantum data structures, and so forth. It would
also be highly interesting to identify further refinement rules that encode high-level reasoning
and design patterns that are commonly used in quantum algorithms, and extend the language
to natively support these operations. For example, quantum amplitude amplification [16], which

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
QbC: Quantum Correctness by Construction                                                                      99:25


generalizes Grover’s algorithm to offer a quantum speedup for boosting the success probability
of a subroutine that improves over naive repetition (cf. Sections 4.3 and 4.4) and is widely used.
It would also be interesting to devise hybrid approaches that combine both post-hoc (Hoare or
weakest-precondition logic) and by-construction (QbC) reasoning, which can be useful particularly
when constructing larger and more complex programs [75].
   Future Directions: Implementation and Mechanization. Our framework and results are agnostic
to the choice of assertion language, in the interest of generality. But committing to a concrete
assertion language is an important choice for implementations. From our examples and refinement
rules, we find that it is convenient to consider projections scaled by scalar values and finite linear
combinations thereof, expressed in Dirac notation. For instance, a web-based prototype proposed
recently uses a simple assertion language based on Dirac notation for a fixed number of qubits [65].
The conditions of refinement are checked using a decision procedure on finite-sized complex
matrices to verify the Löwner order. To further mechanize QbC and in particular to handle general
programs when the number of qubits is not fixed, we believe a natural and ambitious future work
would be to integrate QbC with a proof assistant such as Coq or Lean to handle proof obligations of
side conditions. Notable prior work includes CoqQ [82] and QWIRE [57], which formalize reasoning
about quantum programs in CoQ, and the recent decision procedure for Dirac notation [77].
   Outlook: Algorithm Development. Our view is that algorithm design is a creative process that
often requires insights that are difficult to obtain purely by automation. We believe that a by-
construction approach can help algorithm designers focus on this creative aspect, one key insight
at a time, to develop algorithms that are ensured to be formally correct, without being bogged
down by small details, as the framework guides the refinement and gives a principled way to
generate side-conditions that need to be checked per refinement step. Several well-known quantum
algorithms have been post-hoc verified using the quantum Hoare logic proof system. It is also
possible to construct these same programs using QbC, at roughly the same complexity. Compared
with post-hoc verification, this can provide additional benefits: one does not have to decide on all
program details a priori, but can do so during the refinement process. This can lead to different
choices, resulting in different programs and trade-offs. We showcased this in the search example
where we derived two programs from the same specification, by making a different choice at a
key step. Similar examples are known in the classical CbC literature. This may also open up the
possibility of discovering alternate and cleaner implementations to existing algorithms. However,
we emphasize that we do not see by-construction and post-hoc approaches as mutually exclusive,
but rather as complementing each other with each having its role. The most natural approach may
well be a hybrid approach, as we propose to explore in future work above.

6   Data-Availability Statement
This paper proposes the theoretical foundations for a correctness-by-construction approach for
quantum programs. We do not provide an artifact, but note that [65] gives a web-based prototype.

Acknowledgments
We thank Gilles Barthe and Bruce Watson for fruitful discussions on the subject of this work,
 and the anonymous referees for valuable feedback on earlier versions of this manuscript. All
 authors acknowledge support by the BMBF (QuBRA, 13N16135 & 13N16303; QuSol, 13N17173
 & 13N17170). IS also acknowledges support by the BMWK (ProvideQ, 01MQ22006F). MW also
 acknowledges support by the European Union (ERC, SYMOPTIC, 101040907), by the Deutsche
 Forschungsgemeinschaft (DFG, German Research Foundation) under Germany’s Excellence Strategy
- EXC 2092 CASA - 390781972, and by the Dutch Research Council (NWO grant OCENW.KLEIN.267).

                           Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
99:26                                                                    Anurudh Peduri, Ina Schaefer, and Michael Walter


References
 [1] J.-R. Abrial. 1996. The B-Book: Assigning Programs to Meanings. Cambridge University Press, USA.
 [2] Jean-Raymond Abrial. 2010. Modeling in Event-B: System and Software Engineering (1st ed.). Cambridge University
     Press, USA.
 [3] T. Altenkirch and J. Grattage. 2005. A functional quantum programming language. In 20th Annual IEEE Symposium on
     Logic in Computer Science (LICS’ 05). IEEE, New York, NY, USA, 249–258. doi:10.1109/LICS.2005.1
 [4] Andris Ambainis. 2004. Quantum search algorithms. ACM SIGACT News 35, 2 (2004), 22–35.
 [5] Roman Andriushchenko, Milan Češka, Sebastian Junges, Joost-Pieter Katoen, and Šimon Stupinský. 2021. PAYNT: A
     Tool for Inductive Synthesis of Probabilistic Programs. In Computer Aided Verification: 33rd International Conference, CAV
     2021, Virtual Event, July 20-23, 2021, Proceedings, Part I. Springer-Verlag, Berlin, Heidelberg, 856–869. doi:10.1007/978-
     3-030-81685-8_40
 [6] Simon Apers, Stacey Jeffery, Galina Pass, and Michael Walter. 2023. (No) Quantum Space-Time Tradeoff for USTCON.
     In 31st Annual European Symposium on Algorithms (ESA 2023) (Leibniz International Proceedings in Informatics (LIPIcs),
     Vol. 274), Inge Li Gørtz, Martin Farach-Colton, Simon J. Puglisi, and Grzegorz Herman (Eds.). Schloss Dagstuhl –
     Leibniz-Zentrum für Informatik, Dagstuhl, Germany, 10:1–10:17. doi:10.4230/LIPIcs.ESA.2023.10
 [7] Krzysztof R. Apt and Ernst-Rüdiger Olderog. 2019. Fifty years of Hoare’s logic. Formal Aspects of Computing 31, 6
     (Dec. 2019), 751–807. doi:10.1007/s00165-019-00501-3
 [8] Martin Avanzini, Gilles Barthe, Davide Davoli, and Benjamin Grégoire. 2025. A Quantitative Probabilistic Relational
     Hoare Logic. Proc. ACM Program. Lang. 9, POPL, Article 40 (Jan. 2025), 29 pages. doi:10.1145/3704876
 [9] Ralph-Johan J. Back, Abo Akademi, J. Von Wright, F. B. Schneider, and D. Gries. 1998. Refinement Calculus: A Systematic
     Introduction (1st ed.). Springer-Verlag, Berlin, Heidelberg.
[10] Gilles Barthe, Benjamin Grégoire, and Santiago Zanella Béguelin. 2009. Formal certification of code-based cryptographic
     proofs. In Proceedings of the 36th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages
     (Savannah, GA, USA) (POPL ’09). Association for Computing Machinery, New York, NY, USA, 90–101. doi:10.1145/
     1480881.1480894
[11] Kevin Batz, Benjamin Lucien Kaminski, Joost-Pieter Katoen, Christoph Matheja, and Thomas Noll. 2019. Quantitative
     Separation Logic: A Logic for Reasoning about Probabilistic Pointer Programs. Proc. ACM Program. Lang. 3, POPL,
     Article 34 (jan 2019), 29 pages. doi:10.1145/3290347
[12] Benjamin Bichsel, Maximilian Baader, Timon Gehr, and Martin Vechev. 2020. Silq: A High-Level Quantum Language
     with Safe Uncomputation and Intuitive Semantics. In Proceedings of the 41st ACM SIGPLAN Conference on Programming
     Language Design and Implementation (London, UK) (PLDI 2020). Association for Computing Machinery, New York, NY,
     USA, 286–300. doi:10.1145/3385412.3386007
[13] Richard Bird and Oege de Moor. 1997. Algebra of programming. Prentice-Hall, Inc., USA.
[14] Tabea Bordis, Loek Cleophas, Alexander Kittelmann, Tobias Runge, Ina Schaefer, and Bruce W. Watson. 2022. Re-
     CorC-ing KeY: Correct-by-Construction Software Development Based on KeY. In The Logic of Software. A Tasting
     Menu of Formal Methods (Lecture Notes in Computer Science (including subseries Lecture Notes in Artificial Intelligence
     and Lecture Notes in Bioinformatics)), Wolfgang Ahrendt, Bernhard Beckert, Richard Bubel, and Einar Broch Johnsen
     (Eds.). Springer, Germany, 80–104. doi:10.1007/978-3-031-08166-8_5 Publisher Copyright: © 2022, Springer Nature
     Switzerland AG..
[15] Tabea Bordis, Tobias Runge, Alexander Kittelmann, and Ina Schaefer. 2023. Correctness-by-Construction: An Overview
     of the CorC Ecosystem. Ada Lett. 42, 2 (apr 2023), 75–78. doi:10.1145/3591335.3591343
[16] Gilles Brassard, Peter Hoyer, Michele Mosca, and Alain Tapp. 2002. Quantum amplitude amplification and estimation.
     Contemp. Math. 305 (2002), 53–74.
[17] Dominique Cansell and Dominique Mery. 2003. Foundations of the B Method. Computers and Informatics 22 (01 2003),
     31 p.
[18] R. Chadha, P. Mateus, and A. Sernadas. 2006. Reasoning About Imperative Quantum Programs. Electron. Notes Theor.
     Comput. Sci. 158 (may 2006), 19–39. doi:10.1016/j.entcs.2006.04.003
[19] Shantanav Chakraborty, Aditya Morolia, and Anurudh Peduri. 2023. Quantum Regularized Least Squares. Quantum 7
     (April 2023), 988. doi:10.22331/q-2023-04-27-988
[20] Andrew M. Childs, Richard Cleve, Enrico Deotto, Edward Farhi, Sam Gutmann, and Daniel A. Spielman. 2003. Expo-
     nential Algorithmic Speedup by a Quantum Walk. In Proceedings of the Thirty-Fifth Annual ACM Symposium on Theory
     of Computing (San Diego, CA, USA) (STOC ’03). Association for Computing Machinery, New York, NY, USA, 59–68.
     doi:10.1145/780542.780552
[21] Adam Chlipala. 2013. Certified programming with dependent types. MIT Press, London, England.
[22] J. I. den Hartog. 1999. Verifying Probabilistic Programs Using a Hoare like Logic. In Advances in Computing Science —
     ASIAN’99, P. S. Thiagarajan and Roland Yap (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 113–125.
[23] Edsger Wybe Dijkstra. 1997. A Discipline of Programming (1st ed.). Prentice Hall PTR, USA.


Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
QbC: Quantum Correctness by Construction                                                                               99:27


[24] Yuan Feng and Mingsheng Ying. 2021. Quantum Hoare logic with classical variables. ACM Transactions on Quantum
     Computing 2, 4 (2021), 1–43.
[25] Yuan Feng, Li Zhou, and Yingte Xu. 2023. Refinement calculus of quantum programs with projective assertions.
     arXiv:2311.14215 [cs.LO]
[26] András Gilyén, Yuan Su, Guang Hao Low, and Nathan Wiebe. 2019. Quantum Singular Value Transformation and
     beyond: Exponential Improvements for Quantum Matrix Arithmetics. In Proceedings of the 51st Annual ACM SIGACT
     Symposium on Theory of Computing (Phoenix, AZ, USA) (STOC 2019). Association for Computing Machinery, New
     York, NY, USA, 193–204. doi:10.1145/3313276.3316366
[27] Vittorio Giovannetti, Seth Lloyd, and Lorenzo Maccone. 2008. Quantum Random Access Memory. Phys. Rev. Lett. 100
     (Apr 2008), 160501. Issue 16. doi:10.1103/PhysRevLett.100.160501
[28] Alexander S. Green, Peter LeFanu Lumsdaine, Neil J. Ross, Peter Selinger, and Benoît Valiron. 2013. Quipper: A Scalable
     Quantum Programming Language. In Proceedings of the 34th ACM SIGPLAN Conference on Programming Language
     Design and Implementation (Seattle, Washington, USA) (PLDI ’13). Association for Computing Machinery, New York,
     NY, USA, 333–342. doi:10.1145/2491956.2462177
[29] David Gries. 1981. The Science of Programming. Springer New York, New York, NY. doi:10.1007/978-1-4612-5983-1
[30] Lov K. Grover. 1996. A Fast Quantum Mechanical Algorithm for Database Search. In Proceedings of the Twenty-Eighth
     Annual ACM Symposium on Theory of Computing (Philadelphia, Pennsylvania, USA) (STOC ’96). Association for
     Computing Machinery, New York, NY, USA, 212–219. doi:10.1145/237814.237866
[31] Aram W. Harrow, Avinatan Hassidim, and Seth Lloyd. 2009. Quantum Algorithm for Linear Systems of Equations.
     Phys. Rev. Lett. 103 (Oct 2009), 150502. Issue 15. doi:10.1103/PhysRevLett.103.150502
[32] HaskellWiki. 2014. GHC/Typed holes — HaskellWiki. https://wiki.haskell.org/index.php?title=GHC/Typed_holes&
     oldid=58717 [Online; accessed 25-January-2024].
[33] C. A. R. Hoare. 1969. An Axiomatic Basis for Computer Programming. Commun. ACM 12, 10 (oct 1969), 576–580.
     doi:10.1145/363235.363259
[34] Yoshihiko Kakutani. 2009. A Logic for Formal Verification of Quantum Programs. In Advances in Computer Science -
     ASIAN 2009. Information Security and Privacy, Anupam Datta (Ed.). Springer Berlin Heidelberg, Berlin, Heidelberg,
     79–93.
[35] Benjamin Lucien Kaminski, Joost-Pieter Katoen, Christoph Matheja, and Federico Olmedo. 2016. Weakest precondition
     reasoning for expected run–times of probabilistic programs. In Programming Languages and Systems: 25th European
     Symposium on Programming, ESOP 2016, Held as Part of the European Joint Conferences on Theory and Practice of
     Software, ETAPS 2016, Eindhoven, The Netherlands, April 2–8, 2016, Proceedings 25, Peter Thiemann (Ed.). Springer,
     Springer Berlin Heidelberg, Berlin, Heidelberg, 364–389.
[36] A. Yu. Kitaev. 1995. Quantum measurements and the Abelian Stabilizer Problem. arXiv:quant-ph/9511026 [quant-ph]
     https://arxiv.org/abs/quant-ph/9511026
[37] Alexander Knüppel, Tobias Runge, and Ina Schaefer. 2020. Scaling Correctness-by-Construction. In Leveraging
     Applications of Formal Methods, Verification and Validation: Verification Principles: 9th International Symposium on
     Leveraging Applications of Formal Methods, ISoLA 2020, Rhodes, Greece, October 20-30, 2020, Proceedings, Part I (Rhodes,
     Greece). Springer-Verlag, Berlin, Heidelberg, 187–207. doi:10.1007/978-3-030-61362-4_10
[38] Derrick G. Kourie and Bruce W. Watson. 2012. The Correctness-by-Construction Approach to Programming. Springer,
     Berlin, Heidelberg. doi:10.1007/978-3-642-27919-5
[39] Adrian Lehmann, Ben Caldwell, and Robert Rand. 2022. VyZX : A Vision for Verifying the ZX Calculus.
     arXiv:2205.05781 [quant-ph] https://arxiv.org/abs/2205.05781
[40] Yangjia Li and Dominique Unruh. 2021. Quantum Relational Hoare Logic with Expectations. In 48th International
     Colloquium on Automata, Languages, and Programming (ICALP 2021) (Leibniz International Proceedings in Informatics
     (LIPIcs), Vol. 198), Nikhil Bansal, Emanuela Merelli, and James Worrell (Eds.). Schloss Dagstuhl – Leibniz-Zentrum für
     Informatik, Dagstuhl, Germany, 136:1–136:20. doi:10.4230/LIPIcs.ICALP.2021.136
[41] Yuan Liang Lim, Almut Beige, and Leong Chuan Kwek. 2005. Repeat-Until-Success Linear Optics Distributed Quantum
     Computing. Phys. Rev. Lett. 95 (Jul 2005), 030505. Issue 3. doi:10.1103/PhysRevLett.95.030505
[42] Junyi Liu, Li Zhou, Gilles Barthe, and Mingsheng Ying. 2022. Quantum Weakest Preconditions for Reasoning about
     Expected Runtimes of Quantum Programs. In Proceedings of the 37th Annual ACM/IEEE Symposium on Logic in
     Computer Science (Haifa, Israel) (LICS ’22). Association for Computing Machinery, New York, NY, USA, Article 4,
     13 pages. doi:10.1145/3531130.3533327
[43] John M. Martyn, Zane M. Rossi, Andrew K. Tan, and Isaac L. Chuang. 2021. Grand Unification of Quantum Algorithms.
     PRX Quantum 2 (Dec 2021), 040203. Issue 4. doi:10.1103/PRXQuantum.2.040203
[44] Ashley Montanaro. 2016. Quantum algorithms: an overview. npj Quantum Information 2, 1 (Jan. 2016), 1–8. doi:10.
     1038/npjqi.2015.23 Number: 1 Publisher: Nature Publishing Group.



                                Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
99:28                                                                    Anurudh Peduri, Ina Schaefer, and Michael Walter


[45] Carroll Morgan. 1988. The specification statement. ACM Transactions on Programming Languages and Systems (TOPLAS)
     10, 3 (1988), 403–419.
[46] Carroll Morgan and Annabelle McIver. 1999. pGCL: Formal reasoning for random algorithms. South African Computer
     Journal, 14–27.
[47] Ana Neri, Rui Soares Barbosa, and José N Oliveira. 2021. Compiling quantamorphisms for the IBM Q Experience. IEEE
     Transactions on Software Engineering 48, 11 (2021), 4339–4356.
[48] Michael A Nielsen and Isaac L Chuang. 2010. Quantum Computation and Quantum Information. Cambridge University
     Press, Cambridge. doi:10.1017/CBO9780511976667
[49] Peter W. O’Hearn. 2019. Incorrectness Logic. Proc. ACM Program. Lang. 4, POPL, Article 10 (dec 2019), 32 pages.
     doi:10.1145/3371078
[50] Federico Olmedo, Benjamin Lucien Kaminski, Joost-Pieter Katoen, and Christoph Matheja. 2016. Reasoning about
     Recursive Probabilistic Programs. In Proceedings of the 31st Annual ACM/IEEE Symposium on Logic in Computer Science
     (New York, NY, USA) (LICS ’16). Association for Computing Machinery, New York, NY, USA, 672–681. doi:10.1145/
     2933575.2935317
[51] Cyrus Omar, Ian Voysey, Ravi Chugh, and Matthew A. Hammer. 2019. Live functional programming with typed holes.
     Proc. ACM Program. Lang. 3, POPL, Article 14 (jan 2019), 32 pages. doi:10.1145/3290327
[52] Adam Paetznick and Krysta M. Svore. 2014. Repeat-until-success: non-deterministic decomposition of single-qubit
     unitaries. Quantum Info. Comput. 14, 15-16 (nov 2014), 1277–1301.
[53] Raúl Pardo, Einar Broch Johnsen, Ina Schaefer, and Andrzej Wąsowski. 2022. A Specification Logic for Programs in the
     Probabilistic Guarded Command Language. In Theoretical Aspects of Computing – ICTAC 2022, Helmut Seidl, Zhiming
     Liu, and Corina S. Pasareanu (Eds.). Springer International Publishing, Cham, 369–387.
[54] Jennifer Paykin, Robert Rand, and Steve Zdancewic. 2017. QWIRE: A Core Language for Quantum Circuits. In
     Proceedings of the 44th ACM SIGPLAN Symposium on Principles of Programming Languages (Paris, France) (POPL ’17).
     Association for Computing Machinery, New York, NY, USA, 846–858. doi:10.1145/3009837.3009894
[55] Robert Rand. 2019. Verification Logics for Quantum Programs. arXiv:1904.04304 [cs.LO]
[56] Robert Rand, Jennifer Paykin, Dong-Ho Lee, and Steve Zdancewic. 2019. ReQWIRE: Reasoning about Reversible
     Quantum Circuits. Electronic Proceedings in Theoretical Computer Science 287 (jan 2019), 299–312. doi:10.4204/eptcs.
     287.17
[57] Robert Rand, Jennifer Paykin, and Steve Zdancewic. 2018. QWIRE Practice: Formal Verification of Quantum Circuits
     in Coq. Electronic Proceedings in Theoretical Computer Science 266 (feb 2018), 119–132. doi:10.4204/eptcs.266.8
[58] Tobias Runge, Tabea Bordis, Alex Potanin, Thomas Thüm, and Ina Schaefer. 2023. Flexible Correct-by-Construction
     Programming. Logical Methods in Computer Science Volume 19, Issue 2 (June 2023). doi:10.46298/lmcs-19(2:16)2023
[59] Tobias Runge, Alexander Knüppel, Thomas Thüm, and Ina Schaefer. 2020. Lattice-Based Information Flow Control-by-
     Construction for Security-by-Design. In Proceedings of the 8th International Conference on Formal Methods in Software
     Engineering (Seoul, Republic of Korea) (FormaliSE ’20). Association for Computing Machinery, New York, NY, USA,
     44–54. doi:10.1145/3372020.3391565
[60] Tobias Runge, Alex Potanin, Thomas Thüm, and Ina Schaefer. 2022. Traits: Correctness-by-Construction For Free. In
     Formal Techniques for Distributed Objects, Components, and Systems: 42nd IFIP WG 6.1 International Conference, FORTE
     2022, Held as Part of the 17th International Federated Conference on Distributed Computing Techniques, DisCoTec 2022,
     Lucca, Italy, June 13-17, 2022, Proceedings (Lucca, Italy). Springer-Verlag, Berlin, Heidelberg, 131–150. doi:10.1007/978-
     3-031-08679-3_9
[61] Tobias Runge, Ina Schaefer, Loek Cleophas, Thomas Thüm, Derrick Kourie, and Bruce W. Watson. 2019. Tool Support
     for Correctness-by-Construction. In Fundamental Approaches to Software Engineering, Reiner Hähnle and Wil van der
     Aalst (Eds.). Springer International Publishing, Cham, 25–42.
[62] Tobias Runge, Thomas Thüm, Loek Cleophas, Ina Schaefer, and Bruce W. Watson. 2020. Comparing Correctness-
     by-Construction with Post-Hoc Verification—A Qualitative User Study. In Formal Methods. FM 2019 International
     Workshops, Emil Sekerinski, Nelma Moreira, José N. Oliveira, Daniel Ratiu, Riccardo Guidotti, Marie Farrell, Matt
     Luckcuck, Diego Marmsoler, José Campos, Troy Astarte, Laure Gonnord, Antonio Cerone, Luis Couto, Brijesh Dongol,
     Martin Kutrib, Pedro Monteiro, and David Delmas (Eds.). Springer International Publishing, Cham, 388–405.
[63] Jeff W Sanders and Paolo Zuliani. 2000. Quantum programming. In International Conference on Mathematics of Program
     Construction. Springer, 80–99.
[64] Peter Selinger. 2004. Towards a quantum programming language. Mathematical Structures in Computer Science 14, 4
     (2004), 527–586. doi:10.1017/S0960129504004256
[65] Niklas Seng. 2024. Quantum Correctness By Construction On The Web. Bachelor’s thesis. Karlsruhe Institute of
     Technology. See http://qbc.kastel.kit.edu and also http://qbc.kastel.kit.edu/tutorial.
[66] P.W. Shor. 1994. Algorithms for quantum computation: discrete logarithms and factoring. In Proceedings 35th Annual
     Symposium on Foundations of Computer Science. 124–134. doi:10.1109/SFCS.1994.365700


Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
QbC: Quantum Correctness by Construction                                                                              99:29


[67] Jeremy Siek and Walid Taha. 2006. Gradual typing for functional languages. Scheme and Functional Programming.
[68] Armando Solar-Lezama. 2009. The sketching approach to program synthesis. In Asian Symposium on Programming
     Languages and Systems. Springer, 4–13.
[69] Damian S. Steiger, Thomas Häner, and Matthias Troyer. 2018. ProjectQ: an open source software framework for
     quantum computing. Quantum 2 (Jan. 2018), 49. doi:10.22331/q-2018-01-31-49
[70] Dominic Steinhöfel and Reiner Hähnle. 2019. Abstract Execution. In Formal Methods – The Next 30 Years, Maurice H.
     ter Beek, Annabelle McIver, and José N. Oliveira (Eds.). Springer International Publishing, Cham, 319–336.
[71] Krysta Svore, Alan Geller, Matthias Troyer, John Azariah, Christopher Granade, Bettina Heim, Vadym Kliuchnikov,
     Mariia Mykhailova, Andres Paz, and Martin Roetteler. 2018. Q#: Enabling Scalable Quantum Computing and De-
     velopment with a High-Level DSL. In Proceedings of the Real World Domain Specific Languages Workshop 2018
     (Vienna, Austria) (RWDSL2018). Association for Computing Machinery, New York, NY, USA, Article 7, 10 pages.
     doi:10.1145/3183895.3183901
[72] Dominique Unruh. 2019. Quantum relational Hoare logic. Proceedings of the ACM on Programming Languages 3, POPL
     (Jan. 2019), 1–31. doi:10.1145/3290346
[73] Joran van Apeldoorn, Sander Gribling, Yinan Li, Harold Nieuwboer, Michael Walter, and Ronald de Wolf. 2021. Quantum
     Algorithms for Matrix Scaling and Matrix Balancing. In 48th International Colloquium on Automata, Languages, and
     Programming (ICALP 2021) (Leibniz International Proceedings in Informatics (LIPIcs), Vol. 198), Nikhil Bansal, Emanuela
     Merelli, and James Worrell (Eds.). Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl, Germany, 110:1–110:17.
     doi:10.4230/LIPIcs.ICALP.2021.110
[74] Finn Voichick, Liyi Li, Robert Rand, and Michael Hicks. 2023. Qunity: A Unified Language for Quantum and Classical
     Computing. Proc. ACM Program. Lang. 7, POPL, Article 32 (jan 2023), 31 pages. doi:10.1145/3571225
[75] Bruce W. Watson, Derrick G. Kourie, Ina Schaefer, and Loek Cleophas. 2016. Correctness-by-Construction and Post-hoc
     Verification: A Marriage of Convenience?. In Leveraging Applications of Formal Methods, Verification and Validation:
     Foundational Techniques, Tiziana Margaria and Bernhard Steffen (Eds.). Springer International Publishing, Cham,
     730–748.
[76] Mark M Wilde. 2013. Quantum information theory. Cambridge University Press, Cambridge. doi:10.1017/
     CBO9781139525343
[77] Yingte Xu, Gilles Barthe, and Li Zhou. 2025. Automating Equational Proofs in Dirac Notation. Proc. ACM Program.
     Lang. 9, POPL, Article 42 (Jan. 2025), 33 pages. doi:10.1145/3704878
[78] Peng Yan, Hanru Jiang, and Nengkun Yu. 2022. On Incorrectness Logic for Quantum Programs. Proc. ACM Program.
     Lang. 6, OOPSLA1, Article 72 (apr 2022), 28 pages. doi:10.1145/3527316
[79] N.S. Yanofsky and M.A. Mannucci. 2008. Quantum Computing for Computer Scientists. Cambridge University Press.
     doi:10.1017/CBO9780511813887
[80] Mingsheng Ying. 2012. Floyd–Hoare Logic for Quantum Programs. ACM Trans. Program. Lang. Syst. 33, 6, Article 19
     (2012), 49 pages. doi:10.1145/2049706.2049708
[81] Charles Yuan and Michael Carbin. 2022. Tower: Data Structures in Quantum Superposition. Proc. ACM Program. Lang.
     6, OOPSLA2, Article 134 (oct 2022), 30 pages. doi:10.1145/3563297
[82] Li Zhou, Gilles Barthe, Pierre-Yves Strub, Junyi Liu, and Mingsheng Ying. 2023. CoqQ: Foundational Verification of
     Quantum Programs. Proc. ACM Program. Lang. 7, POPL, Article 29 (jan 2023), 33 pages. doi:10.1145/3571222
[83] Li Zhou, Nengkun Yu, and Mingsheng Ying. 2019. An Applied Quantum Hoare Logic. In Proceedings of the 40th
     ACM SIGPLAN Conference on Programming Language Design and Implementation (Phoenix, AZ, USA) (PLDI 2019).
     Association for Computing Machinery, New York, NY, USA, 1149–1162. doi:10.1145/3314221.3314584
[84] Paolo Zuliani. 2007. A Formal Derivation of Grover’s Quantum Search Algorithm. In First Joint IEEE/IFIP Symposium
     on Theoretical Aspects of Software Engineering (TASE ’07). 67–74. doi:10.1109/TASE.2007.3

Received 2024-10-15; accepted 2025-02-18




                                Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
99:30                                                               Anurudh Peduri, Ina Schaefer, and Michael Walter


Appendix
The supplementary material below contains the proofs for our results for both partial and total
correctness, and a pedagogical example on constructing correct quantum programs using QbC.

A       Soundness of Refinement
In this appendix we present the proofs of Theorem 3.6 and Theorem 3.7. Before giving the proof, we
first analyze the notion of how a program with multiple holes can be filled. Consider the following
intermediate program obtained by refinining to a sequence:
                                     {𝑃 }□{𝑄 } ↩→tot {𝑃 }□{𝑅}; {𝑅}□{𝑄 }                                    (H.seq)
The only way to refine this program is by picking a hole and refining it individually. The same is
true more generally for any composite program (sequence, repeat, case, while): if one refines
such a program, then the resulting program has the same outer structure; only its subprograms get
refined. We prove this in the following lemma.
  Lemma A.1 (Refining programs containing holes). For the relation ↩→ being either ↩→par or
↩→tot , we have the following for every 𝑘 ∈ N:
    (1) If 𝑆 1′ ; 𝑆 2′ ↩→𝑘 𝑆, then there exist programs 𝑆 1 and 𝑆 2 , and integers 𝑘 1, 𝑘 2 ∈ N such that
         𝑆 = 𝑆 1 ; 𝑆 2 and 𝑆 1′ ↩→𝑘1 𝑆 1 and 𝑆 2′ ↩→𝑘2 𝑆 2 and 𝑘 1 + 𝑘 2 = 𝑘.
                         ′
    (2) If repeat 𝑁 do 𝑆 body                                                           ′
                              end ↩→𝑘 𝑆, then there exists a program 𝑆 body such that 𝑆 body ↩→𝑘 𝑆 body
         and 𝑆 = repeat 𝑁 do 𝑆 body end .
    (3) If case meas 𝒒 with 𝑴 of {𝜔 : 𝑆𝜔′ }𝜔 ∈Ω end ↩→𝑘par 𝑆
        then there exist programs 𝑆𝜔 and integers 𝑘𝜔 ∈ N for all 𝜔 ∈ Ω such that
        𝑆 = case meas 𝒒 with 𝑴 of {𝜔 : 𝑆𝜔 }𝜔 ∈Ω end , and 𝑆𝜔′ ↩→𝑘𝜔 𝑆𝜔 for each 𝜔 ∈ Ω, and
        Í
          𝜔 𝑘𝜔 = 𝑘.
                                      ′
    (4) If while meas 𝒒 with 𝐵 do 𝑆 body   end ↩→𝑘 𝑆 then there exists a program 𝑆 body such that
                                                     ′
         𝑆 = while meas 𝒒 with 𝐵 do 𝑆 body end and 𝑆 body ↩→𝑘 𝑆 body .

    Proof. (1) We first prove the claim for 𝑘 = 1. If 𝑆 1′ ; 𝑆 2′ ↩→ 𝑆, then we could only have applied
one of (C.seqL) or (C.seqR) and therefore 𝑆 must be some sequence statement of the form 𝑆 1 ; 𝑆 2 .
If we use (C.seqL) then we have 𝑆 1′ ↩→ 𝑆 1 and 𝑆 2′ = 𝑆 2 , and similarly for (C.seqR). Since, in both
cases, 𝑆 is again a sequence statement, we can apply the preceding observation inductively to prove
the claim for arbitrary 𝑘.
   Similarly, for (2) we can only refine by using (C.repeat), for (3) only using (C.case), and for (4)
only using (C.while). All these rules preserve the root program structure and only refine the body
of the program, hence proving the lemma.                                                              □
    We can now proceed to prove our soundness theorem for refinement for partial correctness:
  Theorem 3.6 (Soundness of refinement for partial correctness). For any two predicates 𝑃, 𝑄
and any concrete program 𝑆, if {𝑃 }□{𝑄 } ↩→∗par 𝑆, then |=par {𝑃 }𝑆 {𝑄 }.
   Proof of Theorem 3.6. We prove this by induction over the length of the refinement chain.
That is, we prove by induction for every 𝑘 ≥ 1, if {𝑃 }□{𝑄 } ↩→𝑘par 𝑆 and 𝑆 has no holes, then
|=par {𝑃 }𝑆 {𝑄 }.
   Base case (𝑘 = 1): We have {𝑃 }□{𝑄 } ↩→par 𝑆. Since 𝑆 has no holes, the refinement can only
be due to one of the rules (H.skip), (H.init) or (H.unit). We analyze these three cases separately:

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
QbC: Quantum Correctness by Construction                                                                      99:31


  (H.skip) 𝑆 = skip and 𝑃 ⇒ 𝑄: The semantics of the former is ⟦𝑆⟧(𝜌) = ⟦ skip ⟧(𝜌) = 𝜌 and
the latter means that tr(𝑃 𝜌) ≤ tr(𝑄𝜌) for all states 𝜌. Therefore, we have for all states 𝜌 that
                      E𝜌 (𝑃) = tr(𝑃 𝜌) ≤ tr(𝑄𝜌) = tr(𝑄 ⟦𝑆⟧(𝜌)) = E⟦𝑆⟧(𝜌 ) (𝑄).
This proves |=tot {𝑃 } skip {𝑄 } and therefore also |=par {𝑃 } skip {𝑄 }.
                                   Í
  (H.init) 𝑆 = 𝒒 := |0⟩ and 𝑃 ⇒ 𝒙 ∈Σ𝒒 |𝒙⟩⟨0| 𝒒 𝑄 |0⟩⟨𝒙 | 𝒒 : From the latter, we have for all states 𝜌:

                                              ©© ∑︁
                       E𝜌 (𝑃) = tr(𝑃 𝜌) ≤ tr ­­       |𝒙⟩⟨0| 𝒒 𝑄 |0⟩⟨𝒙 | 𝒒 ®𝜌 ®
                                                                            ª ª

                                              ««𝒙 ∈Σ𝒒                       ¬ ¬
                                                ∑︁
                                        = tr ­       𝑄 |0⟩⟨𝒙 | 𝒒 𝜌 |𝒙⟩⟨0| 𝒒 ®
                                             ©                              ª

                                             «𝒙 ∈Σ𝒒                       ¬
                                           = tr 𝑄 ⟦ 𝒒 := |0⟩ ⟧(𝜌) = E⟦𝑆⟧(𝜌 ) (𝑄).

This proves |=tot {𝑃 } 𝑞 := |0⟩ {𝑄 } and therefore also |=par {𝑃 } 𝑞 := |0⟩ {𝑄 }.
   (H.unit) 𝑆 = 𝒒 := 𝑈 (𝒒) and 𝑃 ⇒ 𝑈 †𝑄𝑈 : The latter condition means that tr(𝑃 𝜌) ≤ tr(𝑈 †𝑄𝑈 𝜌)
for all states 𝜌, and therefore
                      E𝜌 (𝑃) = tr(𝑃 𝜌) ≤ tr((𝑈 †𝑄𝑈 )𝜌)
                                           = tr(𝑄 (𝑈 𝜌𝑈 † ))
                                           = tr(𝑄 ⟦ 𝒒 := 𝑈 (𝒒) ⟧(𝜌)) = E⟦𝑆⟧(𝜌 ) (𝑄).
This proves |=tot {𝑃 } 𝒒 := 𝑈 (𝒒) {𝑄 } and therefore also |=par {𝑃 } 𝒒 := 𝑈 (𝒒) {𝑄 }.
We have thus established the base case, namely that if {𝑃 }□{𝑄 } ↩→1par 𝑆 then |=par {𝑃 }𝑆 {𝑄 }.
   Induction Step (𝑘 > 1): Using the induction hypothesis, we assume that all refinements of length
at most 𝑘 − 1 are partially correct. We now prove that any program that refines in 𝑘 steps must
also be partially correct. Now, {𝑃 }□{𝑄 } ↩→𝑘par 𝑆 means that there exists a program 𝑆 ′ such that
 {𝑃 }□{𝑄 } ↩→par 𝑆 ′ ↩→𝑘par−1 𝑆. Since 𝑆 ′ must have holes, the refinement {𝑃 }□{𝑄 } ↩→           ′
                                                                                            par 𝑆 can
only be due to one of the following rules:
   (H.seq) 𝑆 ′ = {𝑃 }□{𝑅}; {𝑅}□{𝑄 } : As 𝑆 ′ ↩→𝑘par
                                                 −1 𝑆, Lemma A.1 states that there are programs 𝑆 , 𝑆
                                                                                                    1 2
and integers 𝑘 1, 𝑘 2 such that 𝑆 = 𝑆 1 ; 𝑆 2 and {𝑃 }□{𝑅} ↩→𝑘par    1
                                                                         𝑆 1 and {𝑅}□{𝑄 } ↩→𝑘par 2
                                                                                                     𝑆2
(where 𝑘 1 + 𝑘 2 = 𝑘 − 1). From the induction hypothesis we have that |=par {𝑃 }𝑆 1 {𝑅} and |=par
{𝑅}𝑆 2 {𝑄 }. Therefore, for any partial state 𝜌,
                     E𝜌 (𝑃) − tr(𝜌) = tr(𝑃 𝜌) − tr(𝜌)
                                     ≤ tr(𝑅 ⟦𝑆 1 ⟧(𝜌)) − tr(⟦𝑆 1 ⟧(𝜌))
                                     ≤ tr(𝑄 ⟦𝑆 2 ⟧(⟦𝑆 1 ⟧(𝜌))) − tr(⟦𝑆 2 ⟧(⟦𝑆 1 ⟧(𝜌)))
                                     = tr(𝑄 ⟦ 𝑆 1 ; 𝑆 2 ⟧(𝜌)) − tr(⟦ 𝑆 1 ; 𝑆 2 ⟧(𝜌))
                                     = E⟦𝑆⟧(𝜌 ) (𝑄) − tr(⟦𝑆⟧(𝜌)).
Therefore, |=par {𝑃 }𝑆 {𝑄 }.
  (HP.split) 𝑆 ′ = {𝑃𝛾 }□{𝑄𝛾 } and 𝑃 ⇒ 𝛾 𝑝𝛾 𝑃𝛾 and 𝛾 𝑝𝛾 𝑄𝛾 ⇒ 𝑄 for a probability distribution 𝑝𝛾 :
                                      Í           Í
                                                Í           Í
Recall that the two implications mean that 𝑃 ⪯ 𝛾 𝑝𝛾 𝑃𝛾 and 𝛾 𝑝𝛾 𝑄𝛾 ⪯ 𝑄. From the induction
                               
hypothesis we have |=par 𝑃𝛾 𝑆 𝑄𝛾 for all 𝛾. Therefore, for any partial state 𝜌,
                        E𝜌 (𝑃) − tr(𝜌) = tr(𝑃 𝜌) − tr(𝜌)

                           Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
99:32                                                                 Anurudh Peduri, Ina Schaefer, and Michael Walter

                                                   ∑︁                         
                                               ≤        𝑝𝛾 tr(𝑃𝛾 𝜌) − tr(𝜌)
                                                    𝛾
                                                   ∑︁                                      
                                               ≤        𝑝𝛾 tr(𝑄𝛾 ⟦𝑆⟧(𝜌)) − tr(⟦𝑆⟧(𝜌))
                                                    𝛾
                                                                              !
                                                                      ∑︁
                                               ≤ tr(𝑄⟦𝑆⟧(𝜌)) −             𝑝𝛾 tr(⟦𝑆⟧(𝜌))
                                                                      𝛾
                                             = E⟦𝑆⟧(𝜌 ) (𝑄) − tr(⟦𝑆⟧(𝜌)).
Therefore, |=par {𝑃 }𝑆 {𝑄 }.
   (H.repeat) 𝑆 ′ = repeat 𝑁 do {𝑅 𝑗 }□{𝑅 𝑗+1 } end , with 𝑗 ∈ {0, . . . , 𝑁 − 1} a formal parameter,
𝑃 ⇒ 𝑅0 , and 𝑅𝑁 ⇒ 𝑄: As 𝑆 ′ ↩→𝑘par       −1 𝑆, Lemma A.1 states that 𝑆 = repeat 𝑁 do 𝐶 end for some
                                                −1 𝐶. By the induction hypothesis, |=
                                                                                              
program 𝐶 satisfying {𝑅 𝑗 }□{𝑅 𝑗+1 } ↩→𝑘par                                           par 𝑅 𝑗 𝐶 𝑅 𝑗+1 . It
follows that for all 𝑗 ∈ {0, . . . , 𝑁 − 1} and any partial state 𝜎 𝑗 , we have
                            tr(𝑅 𝑗 𝜎 𝑗 ) − tr 𝜎 𝑗 ≤ tr(𝑅 𝑗+1 ⟦𝐶⟧(𝜎 𝑗 )) − tr(⟦𝐶⟧(𝜎 𝑗 )).
Choosing 𝜎 𝑗 = ⟦𝐶⟧ 𝑗 (𝜌), for some arbitrary partial state 𝜌, the above inequality becomes
                 tr(𝑅 𝑗 ⟦𝐶⟧ 𝑗 (𝜌)) − tr(⟦𝐶⟧ 𝑗 (𝜌)) ≤ tr(𝑅 𝑗+1 ⟦𝐶⟧ 𝑗+1 (𝜌)) − tr(⟦𝐶⟧ 𝑗+1 (𝜌))
and chaining the above inequalities for 𝑗 ∈ {0, . . . , 𝑁 − 1} gives us
                            E𝜌 (𝑅0 ) − tr(𝜌) = tr(𝑅0 𝜌) − tr(𝜌)
                                                   ≤ tr(𝑅𝑁 ⟦𝐶⟧𝑁 (𝜌)) − tr(⟦𝐶⟧𝑁 (𝜌))
                                                   = E⟦𝑆⟧(𝜌 ) (𝑅𝑁 ) − tr(⟦𝑆⟧(𝜌)),
where we used that ⟦𝑆⟧ = ⟦𝐶⟧𝑁 . This shows that |=par {𝑅0 }𝑆 {𝑅𝑁 }. Since 𝑃 ⇒ 𝑅0 and 𝑅𝑁 ⇒ 𝑄,
|=par {𝑃 }𝑆 {𝑄 } follows just like in the preceding case.
   (H.case) 𝑆 ′ = case meas 𝒒 with 𝑴 of {𝜔 : {𝑃𝜔 }□{𝑄 }}𝜔 ∈Ω end and 𝑃 ⇒ 𝜔 ∈Ω M𝜔 (𝑃𝜔 ):
                                                                                 Í
According to Lemma A.1, there exist programs 𝑆𝜔 and numbers 𝑘𝜔 for every 𝜔 ∈ Ω, such
that 𝑆 = case meas 𝒒 with 𝑴 of {𝜔 : 𝑆𝜔 }𝜔 ∈Ω end and {𝑃𝜔 }□{𝑄 } ↩→𝑘par
                                                                                  Í
                                                                          𝜔
                                                                            𝑆𝜔 and 𝜔 𝑘𝜔 = 𝑘 − 1.
From the induction hypothesis we have that |=par {𝑃𝜔 }𝑆𝜔 {𝑄 } for every 𝜔 ∈ Ω. Therefore, for any
partial state 𝜎 and any 𝜔 ∈ Ω,
                             tr(𝑃𝜔 𝜎) − tr(𝜎) ≤ tr(𝑄 ⟦𝑆𝜔 ⟧(𝜎)) − tr(⟦𝑆𝜔 ⟧(𝜎))
So for every partial state 𝜌, we have
                    E𝜌 (𝑃) − tr(𝜌) = tr(𝑃 𝜌) − tr(𝜌)
                                                                ! !
                                                 ∑︁
                                      ≤ tr              M𝜔 (𝑃𝜔 ) 𝜌 − tr(𝜌)
                                                 𝜔 ∈Ω
                                          ∑︁
                                      =          tr (𝑃𝜔 M𝜔 (𝜌)) − tr(M𝜔 (𝜌))
                                          𝜔 ∈Ω
                                          ∑︁
                                      ≤          tr (𝑄 ⟦𝑆𝜔 ⟧(M𝜔 (𝜌))) − tr(⟦𝑆𝜔 ⟧(M𝜔 (𝜌)))
                                          𝜔 ∈Ω
                                      = tr(𝑄 ⟦𝑆⟧(𝜌)) − tr(⟦𝑆⟧(𝜌))
                                      = E⟦𝑆⟧(𝜌 ) (𝑄) − tr(⟦𝑆⟧(𝜌)).
Therefore, |=par {𝑃 }𝑆 {𝑄 }.

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
QbC: Quantum Correctness by Construction                                                                      99:33


  (HP.while) 𝑆 ′ = while meas 𝒒 with 𝐵 do {𝑅}□{B0,𝒒 (𝑄) + B1,𝒒 (𝑅)} end and
𝑃 ⇒ B0,𝒒 (𝑄) + B1,𝒒 (𝑅): As 𝑆 ′ ↩→𝑘par
                                    −1 𝑆, by Lemma A.1 we must have


                                  𝑆 = while meas 𝒒 with 𝐵 do 𝐶 end
for some program 𝐶 such that {𝑅}□{B0,𝒒 (𝑄) + B1,𝒒 (𝑅)} ↩→𝑘par−1 𝐶. From the induction hypothesis
                        
we have that |=par {𝑅}𝐶 B0,𝒒 (𝑄) + B1,𝒒 (𝑅) , meaning that for every partial state 𝜎 we have
                                                                
                 tr(𝑅𝜎) − tr(𝜎) ≤ tr B0,𝒒 (𝑄) + B1,𝒒 (𝑅) ⟦𝐶⟧(𝜎) − tr(⟦𝐶⟧(𝜎)),
or equivalently, after some algebraic manipulations,
                     
                   tr (𝐼 − 𝑄) B0,𝒒 (⟦𝐶⟧(𝜎)) ≤ tr{(𝐼 − 𝑅) (𝜎 − B1,𝒒 (⟦𝐶⟧(𝜎)))}.                               (A.1)
Recalling the semantics of while applied to an arbitrary (partial) state 𝜌, we have
                             ∞                     
                            ∑︁                                          𝑘 
                   ⟦𝑆⟧(𝜌) =     𝜌𝑘 , where 𝜌𝑘 = B0,𝒒 ◦ ⟦𝐶⟧ ◦ B1,𝒒 (𝜌).
                                   𝑘=0

For each 𝑘 ≥ 0, define 𝜎𝑘 = (B1,𝒒 ◦ (⟦𝐶⟧ ◦ B1,𝒒 )𝑘 ) (𝜌), and therefore 𝜌𝑘+1 = B0,𝒒 (⟦𝐶⟧(𝜎𝑘 )).
Applying Eq. (A.1) to 𝜎 = 𝜎𝑘 , we get
                                 tr{(𝐼 − 𝑄) 𝜌𝑘+1 } ≤ tr{(𝐼 − 𝑅) (𝜎𝑘 − 𝜎𝑘+1 )}.
Summing the above over 𝑘 ∈ {0, . . . , 𝑛 − 1}, for some arbitrary 𝑛, and adding tr{(𝐼 − 𝑄) 𝜌 0 }, we get
             (          𝑛
                            )
                      ∑︁
           tr (𝐼 − 𝑄)     𝜌𝑘 ≤ tr{(𝐼 − 𝑄) 𝜌 0 } + tr{(𝐼 − 𝑅) (𝜎0 − 𝜎𝑛 )}
                           𝑘=0
                                             
                                         = tr (𝐼 − 𝑄) B0,𝒒 (𝜌) + tr{(𝐼 − 𝑅) (B1,𝒒 (𝜌) − 𝜎𝑛 )}
                                                                        
                                         = tr(𝜌) − tr B0,𝒒 (𝑄) + B1,𝒒 (𝑅) 𝜌 − tr{(𝐼 − 𝑅)𝜎𝑛 }
                                                                        
                                         ≤ tr(𝜌) − tr B0,𝒒 (𝑄) + B1,𝒒 (𝑅) 𝜌
                                         ≤ tr(𝜌) − tr{𝑃 𝜌 } = E𝜌 (𝐼 − 𝑃),
using 𝑃 ⇒ B0,𝒒 (𝑄) + B1,𝒒 (𝑅) in the last inequality. Taking the limit 𝑛 → ∞, we obtain that
                                           E⟦𝑆⟧(𝜌 ) (𝐼 − 𝑄) ≤ E𝜌 (𝐼 − 𝑃)
which means that |=par {𝑃 }𝑆 {𝑄 }.
 This concludes the proof of the induction step and hence the proof of the theorem.                              □
   We now prove soundness of refinement for total correctness. Its proof is very similar to the one
of Theorem 3.6.
  Theorem 3.7 (Soundness of refinement for total correctness). For any two predicates 𝑃, 𝑄
and any concrete program 𝑆, if {𝑃 }□{𝑄 } ↩→∗tot 𝑆 then |=tot {𝑃 }𝑆 {𝑄 }.
    Proof. We prove by induction for 𝑘 ≥ 1 that if {𝑃 }□{𝑄 } ↩→𝑘tot 𝑆 and 𝑆 is a concrete program
(i.e., has no holes) then |=tot {𝑃 }𝑆 {𝑄 }.
    Base case (𝑘 = 1): We have {𝑃 }□{𝑄 } ↩→tot 𝑆. Since 𝑆 has no holes, the refinement can only be
due to one of the rules (H.skip), (H.init) or (H.unit). In the proof of Theorem 3.6 we already saw
that these rules are totally correct. This concludes the base case.
    Induction Step (𝑘 > 1): Using the induction hypothesis, we assume that all refinements of length
at most 𝑘 − 1 are totally correct. We now prove that any program that refines in 𝑘 steps must
also be totally correct. Now, {𝑃 }□{𝑄 } ↩→𝑘tot 𝑆 means that there exists a program 𝑆 ′ such that

                           Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
99:34                                                               Anurudh Peduri, Ina Schaefer, and Michael Walter


 {𝑃 }□{𝑄 } ↩→tot 𝑆 ′ ↩→𝑘tot−1 𝑆. Since 𝑆 ′ must have holes, the refinement {𝑃 }□{𝑄 } ↩→tot 𝑆 ′ can only
be due to one of the following rules:
   (H.seq) 𝑆 ′ = {𝑃 }□{𝑅}; {𝑅}□{𝑄 } : As 𝑆 ′ ↩→𝑘tot−1 𝑆, Lemma A.1 states that there are programs 𝑆 1, 𝑆 2
and integers 𝑘 1, 𝑘 2 such that 𝑆 = 𝑆 1 ; 𝑆 2 and {𝑃 }□{𝑅} ↩→𝑘tot1 𝑆 1 and {𝑅}□{𝑄 } ↩→𝑘tot2 𝑆 2
(where 𝑘 1 +𝑘 2 = 𝑘−1). From the induction hypothesis we have that |=tot {𝑃 }𝑆 1 {𝑅} and |=tot {𝑅}𝑆 2 {𝑄 }.
Therefore, for any partial state 𝜌,
                                   E𝜌 (𝑃) = tr(𝑃 𝜌) ≤ tr(𝑅 ⟦𝑆 1 ⟧(𝜌))
                                                       ≤ tr(𝑄 ⟦𝑆 2 ⟧(⟦𝑆 1 ⟧(𝜌)))
                                                       = tr(𝑄 ⟦ 𝑆 1 ; 𝑆 2 ⟧(𝜌))
                                                       = E⟦𝑆⟧(𝜌 ) (𝑄).
Therefore, |=tot {𝑃 }𝑆 {𝑄 }.
   (HT.split) 𝑆 ′ = {𝑃𝛾 }□{𝑄𝛾 } and 𝑃 ⇒ 𝛾 𝑝𝛾 𝑃𝛾 and 𝛾 𝑝𝛾 𝑄𝛾 ⇒ 𝑄: Recall the latter mean
                                           Í         Í
          Í             Í                                                        
that 𝑃 ⪯ 𝛾 𝑝𝛾 𝑃𝛾 and 𝛾 𝑝𝛾 𝑄𝛾 ⪯ 𝑄. From the induction hypothesis we have |=tot 𝑃𝛾 𝑆 𝑄𝛾 for
all 𝛾. Therefore, for any partial state 𝜌,
                                     E𝜌 (𝑃) = tr(𝑃 𝜌)
                                              ∑︁
                                            ≤     𝑝𝛾 tr(𝑃𝛾 𝜌)
                                                 𝛾
                                                 ∑︁
                                             ≤        𝑝𝛾 tr(𝑄𝛾 ⟦𝑆⟧(𝜌))
                                                 𝛾
                                             ≤ tr(𝑄⟦𝑆⟧(𝜌)) = E⟦𝑆⟧(𝜌 ) (𝑄).
Therefore, |=tot {𝑃 }𝑆 {𝑄 }.
   (H.repeat) 𝑆 ′ = repeat 𝑁 do {𝑅 𝑗 }□{𝑅 𝑗+1 } end , with 𝑗 ∈ {0, . . . , 𝑁 − 1} a formal parameter,
𝑃 ⇒ 𝑅0 , and 𝑅𝑁 ⇒ 𝑄: As 𝑆 ′ ↩→𝑘tot−1 𝑆, Lemma A.1 states that 𝑆 = repeat 𝑁 do 𝐶 end for some
program 𝐶 satisfying {𝑅 𝑗 }□{𝑅 𝑗+1 } ↩→𝑘tot−1 𝐶. By the induction hypothesis, |=tot 𝑅 𝑗 𝐶 𝑅 𝑗+1 . It
                                                                                           

follows that for all 𝑗 ∈ {0, . . . , 𝑁 − 1} and any partial state 𝜎 𝑗 , we have
                                         tr(𝑅 𝑗 𝜎 𝑗 ) ≤ tr(𝑅 𝑗+1 ⟦𝐶⟧(𝜎 𝑗 )).

Choosing 𝜎 𝑗 = ⟦𝐶⟧ 𝑗 (𝜌), for some arbitrary partial state 𝜌, the above inequality becomes

                                    tr(𝑅 𝑗 ⟦𝐶⟧ 𝑗 (𝜌)) ≤ tr(𝑅 𝑗+1 ⟦𝐶⟧ 𝑗+1 (𝜌)),
and chaining the above inequalities for 𝑗 ∈ {0, . . . , 𝑁 − 1} gives us
                          E𝜌 (𝑅0 ) = tr(𝑅0 𝜌) ≤ tr(𝑅𝑁 ⟦𝐶⟧𝑁 (𝜌)) = E⟦𝑆⟧(𝜌 ) (𝑅𝑁 ),

where we used that ⟦𝑆⟧ = ⟦𝐶⟧𝑁 . This shows that |=tot {𝑅0 }𝑆 {𝑅𝑁 }. Since 𝑃 ⇒ 𝑅0 and 𝑅𝑁 ⇒ 𝑄,
it follows that |=tot {𝑃 }𝑆 {𝑄 } just like in the preceding case.
    (H.case) 𝑆 ′ = case meas 𝒒 with 𝑴 of {𝜔 : {𝑃𝜔 }□{𝑄 }}𝜔 ∈Ω end and 𝑃 ⇒ 𝜔 ∈Ω M𝜔 (𝑃𝜔 ):
                                                                                 Í
According to Lemma A.1, there exist programs 𝑆𝜔 and numbers 𝑘𝜔 for every 𝜔 ∈ Ω, such
that 𝑆 = case meas 𝒒 with 𝑴 of {𝜔 : 𝑆𝜔 }𝜔 ∈Ω end and {𝑃𝜔 }□{𝑄 } ↩→𝑘tot𝜔 𝑆𝜔 and 𝜔 𝑘𝜔 = 𝑘 − 1.
                                                                                  Í
From the induction hypothesis we have that |=tot {𝑃𝜔 }𝑆𝜔 {𝑄 } for every 𝜔 ∈ Ω. Therefore, for any
partial state 𝜎 and any 𝜔 ∈ Ω,
                                           tr(𝑃𝜔 𝜎) ≤ tr(𝑄 ⟦𝑆𝜔 ⟧(𝜎))

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
QbC: Quantum Correctness by Construction                                                                        99:35


So for every partial state 𝜌 we have
                                                                               ! !
                                                              ∑︁
                             E𝜌 (𝑃) = tr(𝑃 𝜌) ≤ tr                   M𝜔 (𝑃𝜔 ) 𝜌
                                                              𝜔 ∈Ω
                                                       ∑︁
                                                   =          tr (𝑃𝜔 M𝜔 (𝜌))
                                                       𝜔 ∈Ω
                                                       ∑︁
                                                   ≤          tr (𝑄 ⟦𝑆𝜔 ⟧(M𝜔 (𝜌))))
                                                       𝜔 ∈Ω
                                                   = tr(𝑄 ⟦𝑆⟧(𝜌)) = E⟦𝑆⟧(𝜌 ) (𝑄).
Therefore, |=tot {𝑃 }𝑆 {𝑄 }.
   (HT.while) 𝑆 ′ = while meas 𝒒 with 𝐵 do {𝑅𝑛+1 }□{B0,𝒒 (𝑄) + B1,𝒒 (𝑅𝑛 )} end , with 𝑛 ∈ N a
formal parameter, 𝐵 a binary measurement, and {𝑅𝑛 }𝑛∈N sequence of predicates such that 𝑅0 = 0,
𝑅𝑛 ⇒ 𝑅𝑛+1 for all 𝑛 ∈ N, and the limit 𝑅 := lim𝑛→∞ 𝑅𝑛 satisfies 𝑃 ⇒ B0,𝒒 (𝑄) + B1,𝒒 (𝑅): By
Lemma A.1, because 𝑆 ′ ↩→𝑘tot−1 𝑆, we must have 𝑆 = while meas 𝒒 with 𝐵 do 𝐶 end for some
                                                            𝑘 −1
program 𝐶 satisfying {𝑅𝑛+1 }□{B0,𝒒 (𝑄) + B1,𝒒 (𝑅𝑛 )} ↩→tot 𝐶. By the induction hypothesis we
have |=tot {𝑅𝑛+1 }𝐶 B0,𝒒 (𝑄) + B1,𝒒 (𝑅𝑛 ) for all 𝑛 ∈ N. This means that for every partial state 𝜎 and
every 𝑛 ∈ N, it holds that
                                                                 
                     tr(𝑅𝑛+1𝜎) ≤ tr B0,𝒒 (𝑄) + B1,𝒒 (𝑅𝑛 ) ⟦𝐶⟧(𝜎)
                                                                            
                               = tr 𝑄 B0,𝒒 ◦ ⟦𝐶⟧ (𝜎) + tr 𝑅𝑛 B1,𝒒 ◦ ⟦𝐶⟧ (𝜎)
By repeatedly applying this inequality for 𝑅𝑛 , 𝑅𝑛−1, . . . , 𝑅1 and using that 𝑅0 = 0, we get
                      𝑛    
                     ∑︁                             𝑘                           
       tr(𝑅𝑛+1𝜎) ≤      tr 𝑄 B0,𝒒 ◦ ⟦𝐶⟧ ◦ B1,𝒒 ◦ ⟦𝐶⟧ (𝜎) + tr 𝑅0 (B1,𝒒 ◦ ⟦𝐶⟧)𝑛 (𝜎)
                     𝑘=0
                              𝑛 
                                                                           !
                             ∑︁                             𝑘 
                  = tr 𝑄            B0,𝒒 ◦ ⟦𝐶⟧ ◦ B1,𝒒              (⟦𝐶⟧(𝜎)) .
                             𝑘=0

Therefore at the limit 𝑛 → ∞ we obtain, using the semantics of the while loop,
                           tr(𝑅𝜎) = lim tr(𝑅𝑛+1𝜎)
                                      𝑛→∞
                                              ∞ 
                                                                                             !
                                             ∑︁                            𝑘 
                                    ≤ tr 𝑄          B0,𝒒 ◦ ⟦𝐶⟧ ◦ B1,𝒒             (⟦𝐶⟧(𝜎))
                                             𝑘=0
                                    = tr(𝑄 ⟦𝑆⟧(⟦𝐶⟧(𝜎))).
Using the assumption that 𝑃 ⇒ B0,𝒒 (𝑄) + B1,𝒒 (𝑅) and the recurrence relation in Eq. (2.1), it follows
that for every partial state 𝜌 we have
                                                                   
                   E𝜌 (𝑃) = tr(𝑃 𝜌) ≤ tr 𝑄 B0,𝒒 (𝜌) + tr 𝑅 B1,𝒒 (𝜌)
                                                                            
                                    ≤ tr 𝑄 B0,𝒒 (𝜌) + tr 𝑄 ⟦𝑆⟧ ⟦𝐶⟧ B1,𝒒 (𝜌)
                                                                       
                                    = tr 𝑄 B0,𝒒 + ⟦𝑆⟧ ◦ ⟦𝐶⟧ ◦ B1,𝒒 (𝜌)
                                         = tr(𝑄 ⟦𝑆⟧(𝜌)) = E⟦𝑆⟧(𝜌 ) (𝑄).
Therefore, |=tot {𝑃 }𝑆 {𝑄 }.
  This concludes the proof of the induction step and hence the proof of the theorem.                               □

                             Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
99:36                                                               Anurudh Peduri, Ina Schaefer, and Michael Walter


B       Completeness of Refinement
In this appendix we present the proofs of Theorem 3.8 and Theorem 3.9.
   Theorem 3.8 (Completeness of refinement for partial correctness). For any two predicates
𝑃, 𝑄 and any concrete program 𝑆, if |=par {𝑃 }𝑆 {𝑄 } then {𝑃 }□{𝑄 } ↩→∗par 𝑆.
  Proof. We prove this by induction on the structure of the concrete program 𝑆. Throughout we
use that |=par {𝑃 }𝑆 {𝑄 } is equivalent to 𝐼 − 𝑃 ⪰ ⟦𝑆⟧† (𝐼 − 𝑄).
  Base cases: There are three types of programs without subprograms to consider:
  𝑆 = skip : By assumption, we have |=par {𝑃 } skip {𝑄 }, which is equivalent to 𝑃 ⇒ 𝑄. Thus we
can use the refinement rule (H.skip) to obtain {𝑃 }□{𝑄 } ↩→par 𝑆, proving this case.
  𝑆 = 𝒒 := |0⟩ : By assumption, we have |=par {𝑃 } 𝒒 := |0⟩ {𝑄 } which is equivalent to
                              ∑︁                                   ∑︁
                   𝐼 −𝑃 ⪰         |𝒙⟩⟨0| 𝒒 (𝐼 − 𝑄) |0⟩⟨𝒙 | 𝒒 = 𝐼 −    |𝒙⟩⟨0| 𝒒 𝑄 |0⟩⟨𝒙 | 𝒒
                               𝒙 ∈Σ𝒒                                   𝒙 ∈Σ𝒒
                    Í
and hence 𝑃 ⇒ 𝒙 ∈Σ𝒒 |𝒙⟩⟨0| 𝒒 𝑄 |0⟩⟨𝒙 | 𝒒 . Thus we can use the refinement rule (H.init) to obtain
 {𝑃 }□{𝑄 } ↩→par 𝑆, proving this case.
   𝑆 = 𝒒 := 𝑈 (𝒒) : By assumption, we have |=par {𝑃 } 𝒒 := 𝑈 (𝒒) {𝑄 }, which is equivalent to
                                       𝐼 − 𝑃 ⪰ 𝑈 𝒒† (𝐼 − 𝑄)𝑈 𝒒 = 𝐼 − 𝑈 𝒒†𝑄𝑈 𝒒
and hence 𝑃 ⇒ 𝑈 𝒒†𝑄𝑈 𝒒 . Thus can use the refinement rule (H.unit) to obtain {𝑃 }□{𝑄 } ↩→par 𝑆,
proving this case.
   Induction step: We now consider a concrete program 𝑆 with subprograms. We assume that |=par
{𝑃 }𝑆 {𝑄 } and we must prove that {𝑃 }□{𝑄 } ↩→∗par 𝑆. By the induction hypothesis, we know that
for every syntactic subprogram 𝑆 ′ of 𝑆 (which is necessarily concrete as well), and for arbitrary
predicates 𝑃 ′ and 𝑄 ′ , it holds that |=par {𝑃 ′ }𝑆 ′ {𝑄 ′ } implies {𝑃 ′ }□{𝑄 ′ } ↩→∗par 𝑆 ′ . There are four
cases to consider for 𝑆:
   𝑆 = 𝑆 1 ; 𝑆 2 : By assumption, we have |=par {𝑃 }𝑆 1 ; 𝑆 2 {𝑄 }, which means 𝐼 − 𝑃 ⪰ ⟦𝑆 1 ⟧† (⟦𝑆 2 ⟧† (𝐼 −
𝑄)). If we choose 𝑅 = 𝐼 − ⟦𝑆 2 ⟧† (𝐼 − 𝑄), then it follows that 𝐼 − 𝑃 ⪰ ⟦𝑆 1 ⟧† (𝐼 − 𝑅), as well as, of
course, 𝐼 − 𝑅 = ⟦𝑆 2 ⟧† (𝐼 − 𝑄), which mean that |=par {𝑃 }𝑆 1 {𝑅} and |=par {𝑅}𝑆 2 {𝑄 }, respectively.
Since 𝑆 is a concrete program, so are 𝑆 1 and 𝑆 2 . Hence we can see from the induction hypothesis
that {𝑃 }□{𝑅} ↩→∗par 𝑆 1 and {𝑅}□{𝑄 } ↩→∗par 𝑆 2 . We can thus construct 𝑆 by first using (H.seq)
with the intermediate condition 𝑅 to obtain {𝑃 }□{𝑄 } ↩→par {𝑃 }□{𝑅}; {𝑅}□{𝑄 } and then using
(C.seqL) and (C.seqR), proving this case.
   𝑆 = repeat 𝑁 do 𝑆 ′ end : By assumption, we have |=par {𝑃 } repeat 𝑁 do 𝑆 ′ end {𝑄 }, which
means 𝐼 − 𝑃 ⪰ (⟦𝑆 ′ ⟧† ) 𝑁 (𝐼 − 𝑄). Let us choose 𝑅 𝑗 = 𝐼 − (⟦𝑆 ′ ⟧† ) 𝑁 − 𝑗 (𝐼 − 𝑄) for 𝑗 ∈ {0, . . . , 𝑁 }.
                                                        ′ †
On the one′ hand, this ensures that 𝐼 − 𝑅 𝑗 = ⟦𝑆 ⟧ (𝐼 − 𝑅 𝑗+1      ) for every 𝑗 ∈ {0, . . . , 𝑁 − 1}, that is,
|=par 𝑅 𝑗 𝑆 𝑅 𝑗+1 . Since 𝑆 is a concrete program, so is 𝑆 ′ , hence we can see from the induction
hypothesis that {𝑅 𝑗 }□{𝑅 𝑗+1 } ↩→∗par 𝑆 ′ . On the other hand, it also holds that 𝑃 ⇒ 𝑅0 and 𝑅𝑁 = 𝑄.
We can thus construct 𝑆 by first using (H.repeat) with the family {𝑅 𝑗 } to obtain {𝑃 }□{𝑄 } ↩→par
 repeat 𝑁 do {𝑅 𝑗 }□{𝑅 𝑗+1 } end and then using (C.repeat), proving this case.
   𝑆 = case meas 𝒒 with {𝜔 1 : 𝑀𝜔 1 , 𝜔 2 : 𝑀𝜔 2 , . . .} of 𝜔 1 : 𝑆𝜔 1 , 𝜔 2 : 𝑆𝜔 2 , . . . end , where
{𝑀𝜔 }𝜔 ∈Ω is a measurement on H𝑞 with outcomes in Ω = {𝜔 1, 𝜔 2, . . . }: By assumption, we have
|=par {𝑃 }𝑆 {𝑄 }, which means
                                ∑︁                                 ∑︁                             
      𝐼 − 𝑃 ⪰ ⟦𝑆⟧† (𝐼 − 𝑄) =        M𝜔 ⟦𝑆𝜔 ⟧† (𝐼 − 𝑄) = 𝐼 −               M𝜔 𝐼 − ⟦𝑆𝜔 ⟧† (𝐼 − 𝑄) .          (B.1)
                                  𝜔 ∈Ω                                  𝜔 ∈Ω


Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
QbC: Quantum Correctness by Construction                                                                       99:37


Let us choose 𝑃𝜔 = 𝐼 − ⟦𝑆𝜔 ⟧† (𝐼 −𝑄) for 𝜔 ∈ Ω. On the one hand, this ensures that |=par {𝑃𝜔 }𝑆𝜔 {𝑄 },
hence we can see from the induction hypothesis that {𝑃𝜔 }□{𝑄 } ↩→∗par 𝑆𝜔 for every 𝜔 ∈ Ω. On
                                                   Í
the other hand, by Eq. (B.1) it also holds that 𝑃 ⇒ 𝜔 ∈Ω M𝜔 (𝑃𝜔 ). We can thus construct 𝑆 by first
using (H.case) to obtain {𝑃 }□{𝑄 } ↩→par case meas 𝒒 with 𝑴 of {𝜔 : {𝑃𝜔 }□{𝑄 }}𝜔 ∈Ω end and
then using (C.case) for each 𝜔 ∈ Ω, proving this case.
  𝑆 = while meas 𝒒 with 𝐵 do 𝐶 end : By assumption, we have |=par {𝑃 }𝑆 {𝑄 }, which means
that 𝐼 − 𝑃 ⪰ ⟦𝑆⟧† (𝐼 − 𝑄), or
                                           𝑃 ⇒ 𝐼 − ⟦𝑆⟧† (𝐼 − 𝑄).                                              (B.2)
Let us choose 𝑅 = 𝐼 − ⟦𝐶⟧† (⟦𝑆⟧† (𝐼 − 𝑄)). Then we have from the recurrence in Eq. (2.1) that
      ⟦𝑆⟧† (𝐼 − 𝑄) = B0,𝒒 (𝐼 − 𝑄) + B1,𝒒 (⟦𝐶⟧† (⟦𝑆⟧† (𝐼 − 𝑄))) = 𝐼 − (B0,𝒒 (𝑄) + B1,𝒒 (𝑅)).                   (B.3)
On the one hand, it follows that
                   𝐼 − 𝑅 = ⟦𝐶⟧† (⟦𝑆⟧† (𝐼 − 𝑄)) = ⟦𝐶⟧† (𝐼 − (B0,𝒒 (𝑄) + B1,𝒒 (𝑅)))
Thus, |=par {𝑅}𝐶 B0,𝒒 (𝑄) + B1,𝒒 (𝑅) , so we find {𝑅}□{B0,𝒒 (𝑄) + B1,𝒒 (𝑅)} ↩→∗par 𝐶 from the
                  

induction hypothesis. On the other hand, we have from Eqs. (B.2) and (B.3) that 𝑃 ⇒ B0,𝒒 (𝑄) +
B1,𝒒 (𝑅). We can thus construct 𝑆 by first using the refinement rule (HP.while) with the above
𝑅, to obtain {𝑃 }□{𝑄 } ↩→par while meas 𝐵 with 𝒒 do {𝑅}□{B0,𝒒 (𝑄) + B1,𝒒 (𝑅)} end , and then
(C.while), proving this case.
   This concludes the structural induction and hence the proof of the theorem.               □
  We now present the proof of completeness of refinement for total correctness. The proof is very
similar to the one of Theorem 3.8.
  Theorem 3.9 (Completeness of refinement for total correctness). For any two predi-
cates 𝑃, 𝑄 and any concrete program 𝑆, if |=tot {𝑃 }𝑆 {𝑄 } then {𝑃 }□{𝑄 } ↩→∗tot 𝑆.
  Proof. We prove this by induction on the structure of the concrete program 𝑆, similar to the
proof of Theorem 3.8. Throughout we use that |=tot {𝑃 }𝑆 {𝑄 } is equivalent to 𝑃 ⪯ ⟦𝑆⟧† (𝑄).
  Base cases: There are three types of programs without subprograms to consider:
  𝑆 = skip : By assumption, we have |=tot {𝑃 } skip {𝑄 }, which is equivalent to 𝑃 ⇒ 𝑄. Thus we
can use the refinement rule (H.skip) to obtain {𝑃 }□{𝑄 } ↩→tot 𝑆, proving this case.
  𝑆 = 𝒒 := |0⟩ : By assumption, we have |=tot {𝑃 } 𝒒 := |0⟩ {𝑄 } which is equivalent to
                                         ∑︁
                                    𝑃 ⪯      |𝒙⟩⟨0| 𝒒 𝑄 |0⟩⟨𝒙 | 𝒒 .
                                             𝒙 ∈Σ𝒒

Thus we can use the refinement rule (H.init) to obtain {𝑃 }□{𝑄 } ↩→tot 𝑆, proving this case.
  𝑆 = 𝒒 := 𝑈 (𝒒) : By assumption, we have |=tot {𝑃 } 𝒒 := 𝑈 (𝒒) {𝑄 }, which is equivalent to
                                                𝑃 ⪯ 𝑈 𝒒†𝑄𝑈 𝒒 .
Thus can use the refinement rule (H.unit) to obtain {𝑃 }□{𝑄 } ↩→tot 𝑆, proving this case.
  Induction step: We now consider a concrete program 𝑆 with subprograms. We assume that |=tot
{𝑃 }𝑆 {𝑄 } and we must prove that {𝑃 }□{𝑄 } ↩→∗tot 𝑆. By the induction hypothesis, we know that
for every syntactic subprogram 𝑆 ′ of 𝑆 (which is necessarily concrete as well), and for arbitrary
predicates 𝑃 ′ and 𝑄 ′ , it holds that |=tot {𝑃 ′ }𝑆 ′ {𝑄 ′ } implies {𝑃 ′ }□{𝑄 ′ } ↩→∗tot 𝑆 ′ . There are four
cases to consider for 𝑆:
  𝑆 = 𝑆 1 ; 𝑆 2 : By assumption, we have |=tot {𝑃 }𝑆 1 ; 𝑆 2 {𝑄 }, which means 𝑃 ⪯ ⟦𝑆 1 ⟧† (⟦𝑆 2 ⟧† (𝑄)). If
we choose 𝑅 = ⟦𝑆 2 ⟧† (𝑄), then it follows that 𝑃 ⪯ ⟦𝑆 1 ⟧† (𝑅), as well as, of course, 𝑅 ⪯ ⟦𝑆 2 ⟧† (𝑄),

                            Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
99:38                                                                Anurudh Peduri, Ina Schaefer, and Michael Walter


which mean that |=tot {𝑃 }𝑆 1 {𝑅} and |=tot {𝑅}𝑆 2 {𝑄 }, respectively. Since 𝑆 is a concrete program,
so are 𝑆 1 and 𝑆 2 . Hence we can see from the induction hypothesis that {𝑃 }□{𝑅} ↩→∗tot 𝑆 1 and
 {𝑅}□{𝑄 } ↩→∗tot 𝑆 2 . We can thus construct 𝑆 by first using (H.seq) with the intermediate condition 𝑅
to obtain {𝑃 }□{𝑄 } ↩→tot {𝑃 }□{𝑅}; {𝑅}□{𝑄 } and then using (C.seqL) and (C.seqR), proving this
case.
     𝑆 = repeat 𝑁 do 𝑆 ′ end : By assumption, we have |=tot {𝑃 } repeat 𝑁 do 𝑆 ′ end {𝑄 }, which
means 𝑃 ⪯ (⟦𝑆 ′ ⟧† ) 𝑁 (𝑄). Let us choose 𝑅 𝑗 = (⟦𝑆 ′ ⟧† ) 𝑁 − 𝑗 (𝑄) for 𝑗 ∈ {0, . . . , 𝑁 }.On the one hand,
this ensures that 𝑅 𝑗 = ⟦𝑆 ′ ⟧† (𝑅 𝑗+1 ) for every 𝑗 ∈ {0, . . . , 𝑁 −1}, that is, |=tot 𝑅 𝑗 𝑆 ′ 𝑅 𝑗+1 . Since 𝑆 is a
concrete program, so is 𝑆 ′ , hence we can see from the induction hypothesis that {𝑅 𝑗 }□{𝑅 𝑗+1 } ↩→∗tot
𝑆 ′ . On the other hand, it also holds that 𝑃 ⇒ 𝑅0 and 𝑅𝑁 = 𝑄. We can thus construct 𝑆 by first
using (H.repeat) with the family {𝑅 𝑗 } to obtain {𝑃 }□{𝑄 } ↩→tot repeat 𝑁 do {𝑅 𝑗 }□{𝑅 𝑗+1 } end
and then using (C.repeat), proving this case.
     𝑆 = case meas 𝒒 with {𝜔 1 : 𝑀𝜔 1 , 𝜔 2 : 𝑀𝜔 2 , . . .} of 𝜔 1 : 𝑆𝜔 1 , 𝜔 2 : 𝑆𝜔 2 , . . . end , where
{𝑀𝜔 }𝜔 ∈Ω is a measurement on H𝑞 with outcomes in Ω = {𝜔 1, 𝜔 2, . . . }: By assumption, we have
|=tot {𝑃 }𝑆 {𝑄 }, which means
                                                       ∑︁                      
                                    𝑃 ⪯ ⟦𝑆⟧† (𝑄) =          M𝜔 ⟦𝑆𝜔 ⟧† (𝑄)                                      (B.4)
                                                        𝜔 ∈Ω

Let us choose 𝑃𝜔 = ⟦𝑆𝜔 ⟧† (𝑄) for 𝜔 ∈ Ω. On the one hand, this ensures that |=tot {𝑃𝜔 }𝑆𝜔 {𝑄 },
hence we can see from the induction hypothesis Í   that {𝑃𝜔 }□{𝑄 } ↩→∗tot 𝑆𝜔 for every 𝜔 ∈ Ω. On
the other hand, by Eq. (B.4) it also holds that 𝑃 ⇒ 𝜔 ∈Ω M𝜔 (𝑃𝜔 ). We can thus construct 𝑆 by first
using (H.case) to obtain {𝑃 }□{𝑄 } ↩→tot case meas 𝒒 with 𝑴 of {𝜔 : {𝑃𝜔 }□{𝑄 }}𝜔 ∈Ω end and
then using (C.case) for each 𝜔 ∈ Ω, proving this case.
  𝑆 = while meas 𝒒 with 𝐵 do 𝐶 end : By assumption, we have |=tot {𝑃 }𝑆 {𝑄 }, which means
that 𝑃 ⇒ ⟦𝑆⟧† (𝑄). Recall that the semantics of the loop is given by
                                                      𝑛
                                                     ∑︁
                     ⟦𝑆⟧ = lim S𝑛 , where S𝑛 =           B0,𝒒 ◦ (⟦𝐶⟧ ◦ B1,𝒒 )𝑘 .             (B.5)
                                𝑛→∞
                                                               𝑘=0

Let us choose 𝑅0 := 0 and 𝑅𝑛+1 :=             ⟦𝐶⟧† (S𝑛† (𝑄)) for all 𝑛      ∈ N. On the one hand, using the
relation S𝑛 = B0,𝒒 + S𝑛−1 ◦ ⟦𝐶⟧ ◦ B1,𝒒 , we get
                           𝑅𝑛+1 = ⟦𝐶⟧† (S𝑛† (𝑄))
                                                                        
                                                                †
                                = ⟦𝐶⟧† B0,𝒒 (𝑄) + B1,𝒒 (⟦𝐶⟧† (S𝑛−1 (𝑄)))
                                = ⟦𝐶⟧† B0,𝒒 (𝑄) + B1,𝒒 (𝑅𝑛 ) ,
                                                            
                                                                      
and this also holds for 𝑛 = 0 if we set S−1 = 0. Thus, |=tot {𝑅𝑛+1 }𝐶 B0,𝒒 (𝑄) + B1,𝒒 (𝑅𝑛 ) , so we
find {𝑅𝑛+1 }□{B0,𝒒 (𝑄) + B1,𝒒 (𝑅𝑛 )} ↩→∗tot 𝐶 from the induction hypothesis. On the other hand, it
is clear from its definition and Eq. (B.5) that the sequence {𝑅𝑛 }𝑛∈N is weakly increasing (that is,
𝑅𝑛 ⇒ 𝑅𝑛+1 for all 𝑛 ∈ N). Moreover, using the recurrence in Eq. (2.1) (which is of course simply
the limit of the relation used above), the limit 𝑅 = lim𝑛→∞ 𝑅𝑛 = ⟦𝐶⟧† (⟦𝑆⟧† (𝑄)) of the sequence
satisfies
                                                          
               𝑃 ⪯ ⟦𝑆⟧† (𝑄) = B0,𝒒 + B1,𝒒 ◦ ⟦𝐶⟧† ◦ ⟦𝑆⟧† (𝑄) = B0,𝒒 (𝑄) + B1,𝒒 (𝑅).
Thus, 𝑃 ⇒ B0,𝒒 (𝑄) + B1,𝒒 (𝑅). We can thus construct 𝑆 by first using the refinement rule (HT.while)
with the above family {𝑅𝑛 }, to obtain
           {𝑃 }□{𝑄 } ↩→tot while meas 𝒒 with 𝐵 do {𝑅𝑛+1 }□{B0,𝒒 (𝑄) + B1,𝒒 (𝑅𝑛 )} end ,

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
QbC: Quantum Correctness by Construction                                                                       99:39


and then (C.while), proving this case.
  This concludes the structural induction and hence the proof of the theorem.                                     □

C    Example: Boosting Success Probability
In this appendix we prove Theorem 4.1.
    Theorem 4.1 (Boosting success probability). The relations (H.boostRep), (H.boostWhile) hold.
   Proof. (H.boostRep) We show that it holds by successively refining the left-hand side into the
right-hand side. To this end we first refine as follows,
               {𝑝𝐼, 𝐼 }□{𝑄 𝒒 , 𝐼 } ↩→tot repeat 𝑁 do {𝑅 𝑗 , 𝐼 }□{𝑅 𝑗+1, 𝐼 } end ,                      (H.repeat)
                                                     |         {z        }
                                                                       𝑆 body

where we choose 𝑁 = ⌈log1−𝜀 (1 − 𝑝)⌉ and
                                 𝑅 𝑗 = (1 − 𝜀) 𝑁 − 𝑗 𝑄 𝒒 + 1 − (1 − 𝜀) 𝑁 − 𝑗 𝐼
                                                                            

for 𝑗 ∈ {0, . . . , 𝑁 }. The application of (H.repeat) is valid since 𝑅𝑁 = 𝑄 𝒒 , while 𝑝𝐼 ⇒ 𝑅0 holds
because 𝑝 ≤ 1 − (1 − 𝜀) 𝑁 by our choice of 𝑁 . Next, since we only want to apply the subroutine if
the postcondition does not already hold, we refine the loop body by measuring the postcondition:
                𝑆 body ↩→tot if meas 𝒒 with 𝐼 − 𝑄 then {𝑃 𝑗 , 𝐼 − 𝑄 𝒒 }□{𝑅 𝑗+1, 𝐼 } end                      (H.if)
                                                       |           {z            }
                                                                                𝑆 then

which is valid if we take
                        𝑃 𝑗 = (𝐼 − 𝑄 𝒒 )𝑅 𝑗 (𝐼 − 𝑄 𝒒 ) = 1 − (1 − 𝜀) 𝑁 − 𝑗 (𝐼 − 𝑄 𝒒 ).
                                                                          

We can obtain the desired program by splitting up this specification in the following way:
                           𝑆 then ↩→tot {𝜀 (𝐼 − 𝑄 𝒒 ), 𝐼 − 𝑄 𝒒 , 𝐼 − 𝑄 𝒒 }□{𝑄 𝒒 , 𝐼, 𝐼 }                (HP.split)
                                      = {𝜀 (𝐼 − 𝑄 𝒒 ), 𝐼 − 𝑄 𝒒 }□{𝑄 𝒒 , 𝐼 }
Indeed, this refinement can be applied since
                     𝑃 𝑗 = 1 − (1 − 𝜀) 𝑁 − 𝑗 (𝐼 − 𝑄 𝒒 )
                                             

                         = 1 − (1 − 𝜀) 𝑁 − 𝑗 −1 (1 − 𝜀) (𝐼 − 𝑄 𝒒 )
                                                       

                           = (1 − 𝜀) 𝑁 − 𝑗 −1𝜀 (𝐼 − 𝑄 𝒒 ) + 1 − (1 − 𝜀) 𝑁 − 𝑗 −1 (𝐼 − 𝑄 𝒒 ),
                                                                                

while
                     𝑅 𝑗+1 = (1 − 𝜀) 𝑁 − 𝑗 −1𝑄 𝒒 + 1 − (1 − 𝜀) 𝑁 − 𝑗 −1 𝐼 .
                                                                       

so (HP.split) can be applied with probabilities (1 − 𝜀) 𝑁 − 𝑗 −1 and 1 − (1 − 𝜀) 𝑁 − 𝑗 −1 .
  (H.boostWhile) We can apply the rule (HT.while) with the binary measurement 𝐵 = 𝐼 − 𝑄 and
the sequence {𝑅𝑛 }𝑛∈N defined by
                                                                   
                                    𝑅𝑛 = (1 − (1 − 𝜀)𝑛 ) 𝐼 − 𝑄 𝒒
for all 𝑛 ∈ N, to obtain
                                                 while meas 𝒒 with 𝐼 − 𝑄 do
                                                     {𝑅𝑛+1 }□{𝑄 𝒒 + 𝑅𝑛 }
                            {𝐼 }□{𝑄 𝒒 } ↩→tot        |       {z       }                    .           (HT.while)
                                                              𝑆 body

                                                  end

                            Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
99:40                                                                  Anurudh Peduri, Ina Schaefer, and Michael Walter


To see that the application of (HT.while) is valid, we observe that 𝑅0 = 0, 𝑅𝑛 ⇒ 𝑅𝑛+1 for all 𝑛 ∈ N,
and the limit 𝑅 = lim𝑛→∞ 𝑅𝑛 = 𝐼 − 𝑄 𝒒 satisfies 𝐼 ⇒ B0,𝒒 (𝑄 𝒒 ) + B1,𝒒 (𝑅) = 𝑄 𝒒 + (𝐼 − 𝑄 𝒒 ) = 𝐼 , where
we used that 𝑄 𝒒 and 𝐼 − 𝑄 𝒒 are projections. To see that it yields the desired specification on the
loop body, note that B0,𝒒 (𝑄 𝒒 ) + B1,𝒒 (𝑅𝑛 ) = 𝑄 𝒒 + 𝑅𝑛 .
  Now observe that we can rewrite the pre- and postcondition of the loop body in the following
way:
                                                                                             
               𝑅𝑛+1 = 1 − (1 − 𝜀)𝑛+1 𝐼 − 𝑄 𝒒 = (1 − 𝜀)𝑛 𝜀 𝐼 − 𝑄 𝒒 + (1 − (1 − 𝜀)𝑛 ) 𝐼 − 𝑄 𝒒 ,
                                                
       𝑄 𝒒 + 𝑅𝑛 = 𝑄 𝒒 + (1 − (1 − 𝜀)𝑛 ) 𝐼 − 𝑄 𝒒 = (1 − 𝜀)𝑛 𝑄 𝒒 + (1 − (1 − 𝜀)𝑛 )𝐼 .
Thus we see that we can refine the loop body using (HT.split), with weights {(1 − 𝜀)𝑛 , (1 − (1 − 𝜀)𝑛 )},
to obtain the desired result:
                                  𝑆 body ↩→tot {𝜀 (𝐼 − 𝑄 𝒒 ), 𝐼 − 𝑄 𝒒 }□{𝑄 𝒒 , 𝐼 }                         (HT.split)
This concludes the proof of the theorem.
                                                                                                                     □

D       Example: Quantum Coin Toss until Zero
In this section we continue the discussion of our running example from Section 2. To keep the
discussion self-contained, we first restate the program as well as its semantics and specification, as
given in Examples 2.3, 2.5 and 2.9. Then we show how QbC can be used to construct programs that
meet this specification.
  Program. Consider the following algorithm: Initialize a qubit in the |0⟩ state. Repeatedly apply
the Hadamard gate and measure in the standard basis until the outcome “0” is seen. This can be
realized by the following program in the quantum while language (Definition 2.1):
                                                         𝑞 := |0⟩ ;
                                                         𝑞 := 𝐻 (𝑞);
                                      𝐴toss-until-zero = while meas 𝑞 do                                         (D.1)
                                                          𝑞 := 𝐻 (𝑞)
                                                          end

  Semantics. We can use Definition 2.4 to compute the semantics for the above program (Eq. (D.1)).
For any state 𝜌 ∈ D (H ),
    ⟦𝐴toss-until-zero ⟧(𝜌) = ⟦ 𝑞 := |0⟩ ; 𝑞 := 𝐻 (𝑞); while meas 𝑞 do 𝑞 := 𝐻 (𝑞) end ⟧(𝜌)
                                                                                                                 
                           = ⟦ while meas 𝑞 do 𝑞 := 𝐻 (𝑞) end ⟧ ⟦ 𝑞 := 𝐻 (𝑞) ⟧(⟦ 𝑞 := |0⟩ ⟧(𝜌))
                                                                                       
                           = ⟦ while meas 𝑞 do 𝑞 := 𝐻 (𝑞) end ⟧ ⟦ 𝑞 := 𝐻 (𝑞) ⟧(|0⟩⟨0|)
                           = ⟦ while meas 𝑞 do 𝑞 := 𝐻 (𝑞) end ⟧(|+⟩⟨+|).
The semantics of the loop is for a general state 𝜎 ∈ D ≤1 (H ) given by
                                                                 ∞ 
                                                                ∑︁                                 
            ⟦ while meas 𝑞 do 𝑞 := 𝐻 (𝑞) end ⟧(𝜎) =                    B0 ◦ (⟦ 𝑞 := 𝐻 (𝑞) ⟧ ◦ B1 )𝑘 (𝜎),
                                                                𝑘=0

where B 𝑗 (𝜌) = | 𝑗⟩⟨𝑗 |𝜌 | 𝑗⟩⟨𝑗 |. Now, for any state 𝜎 ∈ D ≤1 (H ), we have
                                  (⟦ 𝑞 := 𝐻 (𝑞) ⟧ ◦ B1 ) (𝜎) = ⟨1|𝜎 |1⟩ |−⟩⟨−| ,

Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
QbC: Quantum Correctness by Construction                                                                       99:41


and therefore for any 𝑘 ≥ 1, (⟦ 𝑞 := 𝐻 (𝑞) ⟧ ◦ B1 )𝑘 (|+⟩⟨+|) = 21𝑘 |−⟩⟨−|. Altogether, we find that
                                                                                        ∞            
                                                                            1          ∑︁
          ⟦ while meas 𝑞 do 𝑞 := 𝐻 (𝑞) end ⟧(|+⟩⟨+|) = B0 (|+⟩⟨+|) +     B0 𝑘 |−⟩⟨−|
                                                                     𝑘=1
                                                                            2
                                                                                   ∞
                                                                      1          ∑︁ 1
                                                                  =     |0⟩⟨0| +        |0⟩⟨0|
                                                                      2            2𝑘+1
                                                                                  𝑘=1
                                                                  = |0⟩⟨0| .

Therefore the semantics of the coin toss until zero program (D.1) is given by

                                         ⟦𝐴toss-until-zero (𝜌)⟧ = |0⟩⟨0|                                      (D.2)

for any initial state 𝜌 ∈ D (H ). We see that no matter what state we start in, the program always
terminates in the pure state |0⟩.

  Hoare Logic Specification. We now discuss a natural quantum Hoare triple (Section 2.4) and its
correctness for our example. One way to specify the behavior of the program 𝐴toss-until-zero is by
the Hoare triple
                                           {𝐼 }𝐴toss-until-zero {|0⟩⟨0|}.                                     (D.3)
As discussed, this states that the program terminates in the final state |0⟩. We can verify explicitly
that this Hoare triple program is totally correct. Indeed, we saw in Eq. (D.2) that ⟦𝐴toss-until-zero ⟧(𝜌) =
|0⟩⟨0| for every state 𝜌 ∈ D (H ), and hence

                      E⟦𝐴toss-until-zero ⟧(𝜌 ) (|0⟩⟨0|) = E |0⟩⟨0| (|0⟩⟨0|) = 1 = tr 𝜌 = E𝜌 (𝐼 )

for every state 𝜌 ∈ D (H ). This confirms the triple is totally correct.

   Applying Refinement Rules. We now illustrate how to apply refinement rules (Definition 3.5).
Consider the following abstract program, which consists of a single hole, with pre- and postcondition
as in the Hoare triple in Eq. (D.3) for the quantum coin toss until zero program:

                                        𝑆 toss-until-zero = {𝐼 }□{|0⟩⟨0|}                                     (D.4)

One possible refinement is:

                                   {𝐼 }□{|0⟩⟨0|} ↩→tot 𝑞 := |0⟩                                   (H.init)
                                                              Í
The above refinement rule can be applied as the condition 𝐼 ⇒ 𝑥 ∈ {0,1} |𝑥⟩⟨0| |0⟩⟨0| |0⟩⟨𝑥 | is satisfied,
because the RHS equals 𝐼 .
  However, this is not the only program one can construct satisfying it. Instead, we can also use
the sequence rule (H.seq):

                                {𝐼 }□{|0⟩⟨0|} ↩→tot {𝐼 }□{𝐼 }; {𝐼 }□{|0⟩⟨0|}                               (H.seq)

Now the program at hand is a sequence of two holes. We can now refine the second hole as follows:

                             {𝐼 }□{𝐼 }; {𝐼 }□{|0⟩⟨0|} ↩→tot {𝐼 }□{𝐼 }; 𝑞 := |0⟩                            (H.init)

We can achieve this by using (C.seqR), as we already know that {𝐼 }□{|0⟩⟨0|} ↩→tot 𝑞 := |0⟩ . One
can now continue and fill in the remaining hole arbitrarily.

                            Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
99:42                                                                Anurudh Peduri, Ina Schaefer, and Michael Walter


   Structured Specification. On its own, Eq. (D.4) is not a very interesting specification, as much
simpler programs than our original program (D.1) also satisfy it, e.g., 𝑞 := |0⟩ . However, we can
refine the initial specification to arrive at a more structured one that naturally leads to our original
program:

                          𝑆 toss-until-zero = {𝐼 }□{|0⟩⟨0|}
                                          ↩→tot {𝐼 }□{|+⟩⟨+|}; {|+⟩⟨+|}□{|0⟩⟨0|}                            (H.seq)
                                                   {𝐼 }□{|+⟩⟨+|};
                                                   while meas 𝑞 do
                                          ↩→tot           1             1                               (HT.while)
                                                    {𝐼 − 𝑛 |−⟩⟨−|}□{𝐼 − 𝑛 |1⟩⟨1|}
                                                         2             2
                                                   end
                                                   {𝐼 }□{|+⟩⟨+|};
                                                   while meas 𝑞 do
                                          ↩→tot                                                          (HT.split)
                                                      {|+⟩⟨+| , |−⟩⟨−|}□{|0⟩⟨0| , |1⟩⟨1|}
                                                    end

In the second step, we applied the rule (HT.while) with the weakly increasing sequence defined
by 𝑅0 = 0 and 𝑅𝑛+1 = 𝐼 − 21𝑛 |−⟩⟨−|, with limit 𝑅 = lim𝑛→∞ 𝑅𝑛 = 𝐼 . This is allowed, since |+⟩⟨+| ⇒
B0 (|0⟩⟨0|) + B1 (𝐼 ) = 𝐼 , and it gives rise to desired loop body since B0 (|0⟩⟨0|) + B1 (𝑅𝑛 ) = 𝐼 −
 1
2𝑛 |1⟩⟨1| for all 𝑛 ∈ N; B denotes the standard basis measurement of qubit 𝑞. In the third step, we
applied (HT.split) with weights {1, 1 − 21𝑛 }. Thus we have arrived at the following more structured
specification, which refines Eq. (D.4):

                                                  {𝐼 }□{|+⟩⟨+|};
                                                  | {z }
                                                        𝑆 init
                                                  while meas 𝑞 do
                              ′
                            𝑆 toss-until-zero =
                                                    {|+⟩⟨+| , |−⟩⟨−|}□{|0⟩⟨0| , |1⟩⟨1|}
                                                    |               {z               }
                                                                    𝑆 body

                                                  end

  Construction. We now construct a program from this specification by refining the two remaining
           ′
holes in 𝑆 toss-until-zero :

                                𝑆 init = ↩→tot {𝐼 }□{|0⟩⟨0|}; {|0⟩⟨0|}□{|+⟩⟨+|}                             (H.seq)
                                        ↩→tot 𝑞 := |0⟩ ; {|0⟩⟨0|}□{|+⟩⟨+|}                                  (H.init)
                                        ↩→tot 𝑞 := |0⟩ ; 𝑞 := 𝐻 (𝑞)                                        (H.unit)

and

                                             𝑆 body =↩→tot 𝑞 := 𝐻 (𝑞)                                      (H.unit)


Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
QbC: Quantum Correctness by Construction                                                                         99:43


It is easy to see that the conditions required for these refinements are satisfied. Putting it all together,
we have re-constructed the program (D.1) from a specification:
                                                                  𝑞 := |0⟩ ;
                                                                  𝑞 := 𝐻 (𝑞);
              𝑆 toss-until-zero ↩→∗tot 𝑆 toss-until-zero
                                         ′
                                                         ↩→∗tot   while meas 𝑞 do = 𝐴toss-until-zero
                                                                   𝑞 := 𝐻 (𝑞)
                                                                  end




                              Proc. ACM Program. Lang., Vol. 9, No. OOPSLA1, Article 99. Publication date: April 2025.
