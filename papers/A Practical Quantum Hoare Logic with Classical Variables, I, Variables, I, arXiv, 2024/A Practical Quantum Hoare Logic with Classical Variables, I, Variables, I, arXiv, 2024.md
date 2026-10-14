                                             A Practical Quantum Hoare Logic with Classical
                                                              Variables, I
                                                                        Mingsheng Ying
                                          Centre for Quantum Software and Information, University of Technology Sydney, 15
                                                             Broadway, Ultimo, 2007, NSW, Australia
arXiv:2412.09869v4 [cs.PL] 18 Apr 2026




                                         Abstract
                                         In this paper, we present a Hoare-style logic for reasoning about quantum
                                         programs with classical variables. Our approach offers several improvements
                                         over previous work:
                                           1. Enhanced expressivity of the programming language: Our logic
                                              applies to quantum programs with classical variables that incorporate
                                              quantum arrays and parameterized quantum gates, which have not
                                              been addressed in previous research on quantum Hoare logic, either
                                              with or without classical variables.
                                           2. Intuitive correctness specifications: In our logic, preconditions and
                                              postconditions for quantum programs with classical variables are spec-
                                              ified as a pair consisting of a classical first-order logical formula and a
                                              quantum predicate formula (possibly parameterized by classical vari-
                                              ables). These specifications offer greater clarity and align more closely
                                              with the programmer’s intuitive understanding of quantum and classi-
                                              cal interactions.
                                           3. Simplified proof system: By introducing a novel idea in formulating
                                              a proof rule for reasoning about quantum measurements, along with
                                              (2), we develop a proof system for quantum programs that requires only
                                              minimal modifications to classical Hoare logic. Furthermore, this proof
                                              system can be effectively and conveniently combined with classical first-
                                              order logic to verify quantum programs with classical variables.
                                         As a result, the learning curve for quantum program verification techniques
                                         is significantly reduced for those already familiar with classical program ver-
                                         ification techniques, and existing tools for verifying classical programs can
                                         be more easily adapted for quantum program verification.
Keywords: Quantum programming, quantum variables, classical variables,
quantum arrays, parameterised quantum gates, semantics, quantum
predicates, assertion language, Hoare logic, proof system.


1. Introduction
    Hoare logic has played a foundational role in classical programming method-
ology and program verification techniques. With the advent of quantum
computing, there has been a natural desire to establish Hoare-style logic for
quantum programs [10, 53, 61, 30].
    Quantum Hoare logic and assertion logic: A program logic is usually
built upon an assertion logic, which is used to specify the pre/postconditions
of a program that describe the properties of program variables before and
after its execution. So, the first step of defining quantum Hoare logic (QHL
for short) is to choose an assertion language for describing the properties of
quantum states (i.e. the states of quantum program variables). The natural
choice for this purpose should be the standard quantum logic of Birkhoff
and von Neumann [5], in which a proposition about a quantum system is
modelled as a closed subspace of (equivalently, projection operator on) the
system’s Hilbert space. Interestingly, the earliest approaches to QHL did not
adopt it:
   • Chadha, Mateus and Sernadas [8] presented a proof system for reason-
     ing about quantum programs in which the assertion language is exoge-
     nous quantum logic [36], where a superposition of classical semantic
     models is conceived as a semantic model of quantum logic.
   • Kakutani [28] proposed an extension of Hartog’s probabilistic Hoare
     logic [24] for reasoning about quantum programs, in which probabilis-
     tic assertion logical formulas are generalised with unitary and measure-
     ment operators.
    It was first proposed by D’Hondt and Panangaden [14] to use a special
class of observables as assertions (e.g. pre/postconditions) for quantum pro-
grams, called quantum predicates. This approach enjoys an elegant physical
interpretation for Hoare triples (correctness formulas) of quantum programs.
On the other hand, it aligns with Birkhoff-von Neumann quantum logic.
The observables used in [14] are mathematically modelled as Hermitian op-
erators between the zero and identity operators. They are indeed called

                                      2
quantum effects in the quantum foundations literature, and are considered
as propositions in unsharp quantum logic [23] - an extension of Birkhoff-von
Neumann logic (note that projection operators are a special kind of quantum
effects). Afterwards, some useful proof rules for reasoning about quantum
programs were introduced by Feng et. al [18] using quantum predicates as
pre/postconditions.
    A main limitation of all proof systems for quantum programs mentioned
above is that they lack (relative) completeness. The first QHL with (relative)
completeness was established in [58] using the notion of pre/postconditions
as observables proposed in [14].
    Research on QHL and related problems has become active in the last
few years. Various variants and extensions of QHL have been proposed, in-
cluding relational QHL [52, 2, 33, 57], QHL with ghost variables [51], QHL
restricted to projective quantum predicates [71], quantum separation logic
[29, 69], local and modular reasoning [13, 46], dynamic quantum logic [48],
incorrectness logic for quantum programs [56], quantum temporal logic [67],
refinement calculus for quantum programs [39, 22], and verification of re-
cursive quantum programs [55], parallel quantum programs [66] and nonde-
terministic quantum programs [20]. Also, a series of verification tools for
quantum programs based on QHL and other logics have been implemented,
including QBricks [9], QHLProver [34], CoqQ [70], Qafny [31], verification of
Shor’s algorithm in Coq [40, 41], and implementation of dynamic quantum
logic in Maude [15] as well as tools for verification of quantum compilers, e.g.
VOQC [43, 25, 26], Giallar [49, 50, 45] and VQO [32]. For more detailed dis-
cussions about research in this area, the readers can consult surveys [10, 30]
and book [61].
    Classical variables: But the QHL in [58] also has a limitation; namely,
it is defined only for purely quantum programs without classical variables.
Theoretically, such QHL is strong enough because all classical computations
can be efficiently simulated by quantum computations. For practical appli-
cations, however, a QHL with classical variables is more convenient because
most of the known quantum algorithms involve classical computations.
    Indeed, the Hoare-style proof systems in [8, 28] and several others pro-
posed recently allows classical variables, but all of them do not have (relative)
completeness. A (relatively) complete QHL with classical variables was first
presented in [21] by generalising the techniques of [58]. The key idea of [21]
is to define a classical-quantum state (i.e. a state of a quantum program


                                       3
with classical variables; cq-state for short) as a mapping from classical states
to (mixed) quantum states. Accordingly, a classical-quantum predicate (i.e.
an assertion for a quantum program with classical variables; cq-predicate
for short) is defined as a mapping from classical states to observables. This
design decision was also adopted in [12] for developing a satisfaction-based
Hoare logic for quantum programs with classical variables, and further ex-
tended in [19] for reasoning about distributed quantum programs with clas-
sical variables.
    A benefit of the view of cq-states and cq-predicates in [21] is that the QHL
for purely quantum programs in [58] can be straightforwardly generalised to
a Hoare logic for quantum programs with classical variables [21] by a point-
wise lifting from quantum predicates to cq-predicates. However, it has a
drawback that traditional logic tools (e.g. classical first-order logic) cannot
be conveniently used to specify and reason about the classical states in a
cq-state or a cq-predicate because they appear in the domain of the cq-state
or cq-predicate (as a mapping) and often must be treated point-wise.
    Contributions of this paper: This paper aims at developing a QHL
for quantum programs with classical variables that overcomes the drawback
of [21] pointed out above, but inherits the advantages of quantum predicates
as observables in [14, 58]. To this end, we first return to the view of cq-
state as a pair (σ, ρ) of a classical state σ and a quantum state ρ adopted in
[8, 28]. But different from [8, 28] as well as [21], we define an assertion for a
quantum program with classical variables (a cq-assertion for short) as a pair
(φ, A) of a classical first-order logical formula φ and a quantum predicate
(i.e. an observable) A. It should be pointed out that the classical part σ and
φ and the quantum part ρ and A are not independent, as will be explained
shortly. Intuitively, σ and ρ are the states of classical and quantum registers,
and φ and A describes the properties of classical and quantum registers,
respectively. Obviously, this is the most nature view of cq-states and cq-
assertions.
  1. More practical proof system: Why has no QHL based on the above
     view of cq-assertions been given in the previous literature? The main
     reason seems that Hoare triples with such cq-assertions cannot prop-
     erly cope with the probability distributions arisen from quantum mea-
     surements. Indeed, exogenous quantum logic employed in [8], proba-
     bilistic assertions used in [28] and defining cq-predicates as mappings
     from classical states to quantum predicates [21] are all for handling

                                       4
   these probability distributions. In this paper, however, we find a novel
   (and simple) proof rule for reasoning about quantum measurements
   (see (Axiom-Meas) in Table 3). Incorporating it with the proof rules
   for other program constructs, we are able to build a QHL for quantum
   programs with classical variables that is much more convenient and
   easier to use in practical applications than the previous work for the
   same purpose.
2. Syntax of quantum predicates: Quantum predicates in [14, 58, 21]
   and other research along this line are defined as observables. Inherited
   from physics, an observable is modelled as a Hermitian operator on
   the Hilbert space of the system under consideration, which is essen-
   tially an semantic entity from the logical point of view. For example,
   a quantum predicate A for n qubits is a 2n × 2n matrix. Its dimension
   exponentially increases with the number n of qubits. This makes verifi-
   cation of large quantum programs based on QHL impractical because a
   huge amount of matrix calculations will be unavoidable. The author of
   [60] proposed an expansion of Birkhoff-von Neumann quantum logic as
   the assertion language of QHL for purely quantum programs, in which
   quantum predicates can be symbolically and compactly represented;
   in particular, by introducing their syntax, each quantum predicate A
   can be constructed from atomic ones using logical connectives in a
   way similar to that in classical first-order logic (also see Sections 7.5
   and 7.6 of [61]). In this paper, the syntax of quantum predicates de-
   fined in [60, 61] is tailored and further expanded for specifying and
   reasoning about quantum programs with classical variables. Thus, in
   a cq-assertion (φ, A), φ is a classical first-order logical formula, and A
   can be written as a quantum predicate formula, which is usually more
   compact and economic than a large matrix representation.
3. Stronger expressive power of programming language: The quan-
   tum programming languages on which Hoare-style proof systems with
   classical variables were established in the previous literature (e.g. [8, 28,
   21]) are relatively simple. In particular, the only connection between
   their classical and quantum parts is a command of the form x := M [q]
   in which the outcome of a measurement M performed on quantum reg-
   ister q is stored in a classical variable x. In this paper, quantum arrays
   and parameterised quantum gates are introduced into our programming
   language. Then there will be more connections from the classical part
   to the quantum part: classical terms (and thus classical variables) are

                                     5
     used as the subscripts of quantum array variables, and quantum gates
     are parameterised by classical terms. Consequently, the framework of
     our QHL must be meticulously designed to effectively accommodate
     quantum arrays and parameterised quantum gates. Fortunately, the
     cq-assertions discussed earlier provide an appropriate logical tool for
     addressing this issue.
    In summary, we expect that the above contributions can significantly
improve the applicability of QHL in the practical verification of quantum
programs with classical variables.
    Organisation of the paper: The exposition of our QHL with classi-
cal variables is divided into two parts, with this paper serving as the first
instalment. Here, we establish the framework and introduce the proof rules
of QHL, as well as demonstrate the soundness of the logic. However, we
defer the discussion of (relative) completeness and its proof to a companion
paper [62], as these topics require more extensive theoretical treatment and
analysis. This division allows readers primarily interested in the practical
applications of QHL to focus on this paper without needing to engage with
the more theoretical aspects presented in the second part.
    This paper is organised as follows. Quantum arrays are defined in Section
2. We introduce our quantum programming language with classical variables
and parameterised quantum gates in Section 3. The language of cq-assertions
and its semantics are defined in Section 4. The axioms and proof rules of
our QHL for quantum programs with classical variables are presented in
Section 5. The soundness theorem of the QHL is stated in Section 6. A
brief conclusion is drawn in Section 7. Since the main aim of this paper is to
introduce the conceptual framework of QHL, all proofs are deferred to the
Appendix.

2. Quantum Arrays and Subscripted Quantum Variables
   Quantum arrays have already been introduced in several quantum pro-
gramming languages (e.g. OpenQASM [11] and Q# [47]). In this section, we
recall from [64, 65] the formal definitions of quantum arrays and subscripted
quantum variables, which will be needed in defining our programming lan-
guage in the next section.




                                      6
2.1. Quantum types
    As a basis, let us first define the notion of quantum type. Recall that a
basic classical type T denotes an intended set of values. Similarly, a basic
quantum type H denotes an intended Hilbert space. It will be considered
as the state space of a simple quantum variable. Throughout this paper, we
adopt the following notions:
   • Tensor product types: if H1 , ..., Hn (n > 1) are basic quantum types,
     then their tensor product H1 ⊗ ... ⊗ Hn is a quantum type.

   • Higher quantum types: T1 × ... × Tn → H, where T1 , ..., Tn are basic
     classical types, and H is a basic quantum type. Mathematically, this
     type denotes the following tensor power of Hilbert space H (i.e. tensor
     product of multiple copies of H):
                                          O
                       H⊗(T1 ×...×Tn ) =          Hv1 ,...,vn            (1)
                                               v1 ∈T1 ,...,vn ∈Tn

      where Hv1 ,...,vn = H for all v1 ∈ T1 , ..., vn ∈ Tn .
     Intuitively, if we have n quantum systems q1 , ..., qn and their state spaces
are H1 , ..., Hn , respectively, then according to the basic postulates of quan-
tum mechanics, the composite system of q1 , ..., qn has H1 ⊗...⊗Hn as its state
space. If H is the state space of a quantum system q, then the Hilbert space
(1) is the state space of the composite system consisting of those quantum
systems indexed by (v1 , ..., vn ) ∈ T1 × ... × Tn , each of which has the same
state space as q. There is a notable basic difference between the product of
classical types and the tensor product of quantum types: there are not only
product states of the form |ψ1 ⟩...|ψn ⟩ = |ψ1 ⟩ ⊗ ... ⊗ |ψn ⟩ in H1 ⊗ ... ⊗ Hn with
|ψi ⟩ ∈ Hi (1 ≤ i ≤ n) but also entangled states that cannot be written as
a tensor product of respective states in Hi ’s. A similar difference between
higher classical types and quantum ones is that some states in the space
(1) are entangled between the quantum systems indexed by different tuples
(v1 , ..., vn ) ∈ T1 × ... × Tn . It should be noted that (1) may be an infinite
tensor product of Hilbert spaces [54] when one of T1 , ..., Tn is infinite (e.g.,
the type integer → H2 ). However, most applications only need finite tensor
products, as shown in the following:
Example 2.1. Let H2 be the qubit type denoting the 2-dimensional Hilbert
space. If q is a qubit array of type integer → H2 , where integer is the

                                           7
(classical) integer type, then for any two integers k ≤ l, section q[k : l]
stands for the restriction of q to the interval [k : l] = {integer i|k ≤ i ≤ l}.
                                        ⊗(l−k+1)
The state space of this section is H2            . In particular, if k = l, then
q[k : l] actually denotes single qubit q[k]. Furthermore, the GHZ (Green-
berger–Horne–Zeilinger) state
                             Nl            Nl
                               i=k |0⟩i +    i=k |1⟩i
                                       √
                                         2
is an entangled state of the qubits labelled k through l.
Example 2.2. Let us consider the data structure used in quantum Fourier
transform on n qubits. We introduce a classical bit array j of type integer →
Boolean. For any integers k, l with 1 ≤ k ≤ l ≤ n, we use 0.j[k : l] to denote
the binary representation
                                         l
                                         X
                          0.jk ...jl =         j[r] · 2k−r−1 .
                                         r=k

Then we can define quantum arrays |(j, k : l)⟩ and |QFT (j, k : l)⟩ as states
of qubits q[k : l] by induction on the length k − l of the arrays:
(
  |(j, k : l)⟩ = |j[l]⟩ if k = l,
  |(j, k : r + 1)⟩ = |(j, k : r)⟩ ⊗ |j[r + 1]⟩ for k ≤ r ≤ l − 1;
(
  |QFT (j, k : l)⟩ = √12 |0⟩ + e2πi0.j[l] |1⟩ if k = l,
                                             

  |QFT (j, k : r + 1)⟩ = |QFT (j, k : r)⟩ ⊗ √12 |0⟩ + e2πi0.j[l−r:l] |1⟩ for k ≤ r ≤ l − 1.
                                                                        


By equation (5.4) in textbook [38], the quantum Fourier transform can be
rewritten as:
                       |(j, 1 : n)⟩ 7→ |QFT (j, 1 : n)⟩.

2.2. Quantum variables
    Only simple quantum variables are allowed in previous QHL (e.g. [58,
21]). In this paper, however, we will use two sorts of quantum variables:
   • simple quantum variables, of a basic quantum type, say H;

   • array quantum variables, of a higher quantum type, say T1 × ... × Tn →
     H.

                                           8
Furthermore, we introduce:
Definition 2.1. Let q be an array quantum variable of the type T1 ×...×Tn →
H, and for each 1 ≤ i ≤ n, let si be a classical expression of type Ti . Then
q[s1 , ..., sn ] is called a subscripted quantum variable of type H.
    Intuitively, array variable q denotes a quantum system composed of sub-
systems indexed by tuples (v1 , ..., vn ) ∈ T1 × ... × Tn . Thus, whenever expres-
sion si is evaluated to a value vi ∈ Ti for each i, then q[s1 , ..., sn ] indicates
the system of index tuple (v1 , ..., vn ). For example, let q be a qubit array
of type integer × integer → H2 . Then q[2x + y, 7 − 3y] is a subscripted
qubit variable; in particular, if x = 5 and y = −1 in the current classical
state, then it stands for the qubit q[9, 10]; i.e. the qubit in the memory cell
with coordinates (9, 7). To simplify the presentation, we often treat a simple
variable q as a subscripted variable q[s1 , ..., sn ] with n = 0.
    It is usually required that quantum operations are performed on a tuple of
distinct quantum variables; for example, a controlled-NOT gate CNOT [q1 , q2 ]
is meaningful only when q1 ̸= q2 . To describe this kind of conditions, let
q = q1 [s11 , ..., s1n1 ], ..., qk [sk1 , ..., sknk ] be a sequence of simple or subscripted
quantum variables. Then we define the distinctness formula Dist(q) as the
following first-order logical formula:

             Dist(q) = (∀i, j ≤ k) [(qi = qj ) → (∃l ≤ ni ) (sil ̸= sjl )] .              (2)

Thus, for a given classical structure as an interpretation of the first-order
logic and a classical state σ in it, the satisfaction relation:

                    σ |= Dist(q1 [t11 , ..., s1n1 ], ..., qk [sk1 , ..., sknk ])

means that in the classical state σ, q1 [s11 , ..., s1n1 ], ..., qk [sk1 , ..., sknk ] denotes
k distinct quantum systems. This condition will be frequently used in this
paper.

3. A Quantum Programming Language with Classical Variables
    In this section, we define a language qWhile + for quantum programming
with classical variables. It is a further extension of the purely quantum
variant qWhile (see for example, Chapter 5 of [61]) of the classical While-
language (see for example, Chapter 3 of [1]). In particular, qWhile + allows
to use quantum arrays and parameterised quantum gates.

                                                 9
3.1. Parameterised Quantum Gates
    Various quantum gates with certain parameters are implemented in quan-
tum hardware. In addition, parameterised quantum gates and circuits are
widely used in variational quantum algorithms [7] and quantum machine
learning [4]. Consequently, almost all quantum programming languages sup-
port parameterised quantum gates. In our language qWhile + , we assume
a set U of basic parameterised quantum gate symbols. Each gate symbol
U ∈ U is equipped with:
  (i) a classical type of the form T1 × ... × Tm , called the parameter type,
      where m ≥ 0; and
 (ii) a quantum type of the form H1 ⊗ ... ⊗ Hn , where n ≥ 1 is called the
      arity of U .
In the case of m = 0, U is a non-parameterised gate symbol. If for each
k ≤ m, tk is a classical expression of type Tk , and for each i ≤ n, qi is a
simple or subscripted quantum variable with type Hi , then
                             U (t1 , ..., tm )[q1 , ..., qn ]
is called a quantum gate. Intuitively, it means that the quantum gate U with
parameters t1 , ..., tm acts on quantum variables q1 , ..., qn . The following are
two examples of parameterised basic quantum gates:
Example 3.1.       1. The rotation about x-axis is defined as
                                              cos 2θ   −i sin 2θ
                                                                
                  Rx (θ) = exp(−iXθ/2) =
                                             −i sin 2θ   cos 2θ
      where parameter θ denotes the rotation angle. Let q be a qubit variable.
      Then Rx (3θ + π2 )[q] stands for the rotation of angle 3θ + π2 about x
      applied to qubit q.
   2. The XX interaction is a two-qubit interaction defined as
                                        cos 2θ                       −i sin 2θ
                                                                              
                        θ                        cos 2θ   −i sin 2θ           
      Rxx (θ) = exp(−i X ⊗ X) =                         θ      θ
                                                                               
                        2                       −i sin 2   cos 2              
                                       −i sin 2θ                      cos 2θ
      where parameter θ is an index of entangling. Let q be a qubit array.
      Then Rxx (θ)[q[m + 3], q[2m − 7]] stands for the XX interaction between
      qubits q[m + 3] and q[2m − 7].

                                           10
3.2. Quantum Measurements
    In the language qWhile + , we also assume a set M of basic quantum
measurement symbols. Each measurement symbol M ∈ M is equipped with:
  (i) a quantum type of the form H1 ⊗ ... ⊗ Hn , where n ≥ 1 is called the
      arity of M ; and
 (ii) a classical type T , called the outcome type of M .
If for each i ≤ n, qi is a quantum variable with type Hi and x a classical
variable with type T , then we will use

                              x := M [q1 , ..., qn ]

to express the basic command that the measurement denoted by symbol M
is performed on quantum variables q1 , ..., qn , and its outcome is stored in
classical variable x.

Remark 3.1. Indeed, we can also introduce parameterized measurements.
We choose not to do it in this paper because it will make the notations too
complicated. At this moment, various quantum algorithms mainly use the
measurements in the computational basis, and parameterized measurements
are rarely employed in practical applications. But when needed in the future,
the parameterization of measurements can be handled in a way similar to the
parameterization of quantum gates defined in the above subsection.

3.3. Syntax of qWhile +
    Now we are ready to define our quantum programming language qWhile + .
Essentially, it is the classical while-language expanded by quantum gates and
quantum measurement commands introduced in the previous subsections.
The alphabet of qWhile + consists of:
  (i) the alphabet of a classical while-language (see for example Chapter 3
      of [1] and Section 3.2 of [35]);
 (ii) a countably infinite set QV of (simple and array) quantum variables
      (as described in Subsection 2.2);
(iii) a set U of basic (parameterized) quantum gate symbols (as described
      in Subsections 3.1); and
(iv) a set M of basic quantum measurement symbols (as described in Sub-
      section 3.2).


                                       11
The language qWhile + is built upon the classical while-language given in
(i). For simplicity of the presentation, we omit here the standard syntax of
classical expressions and programs; the reader can consult textbook [1, 35].
Then we can introduce:
Definition 3.1. The syntax of qWhile + is given as follows:
             P ::= skip | x := e | q := |0⟩
                   | U (t1 , ..., tm )[q1 , ..., qn ] | x := M [q1 , ..., qn ]        (3)
                   | P1 ; P2 | if b then P1 else P0 | while b do P
where x is a classical variable, e and t1 , ..., tm are classical expressions, q, q1 , ..., qn
are simple or subscripted quantum variables (see their definitions at the be-
ginning of Subsection 2.2 and in Definition 2.1), U ∈ U, M ∈ M, and b is
a classical boolean expression.
    A simpler version of the language qWhile + was already introduced in the
previous literature (see for example [63, 12, 21]), but here we add parame-
terised gate U (t1 , ..., tn ) as well as quantum array into it so that q, q1 , ..., qn in
(3) can be (subscripted) array variables. On the other hand, as mentioned in
Section 2, quantum arrays have been already introduced in previous quantum
programming languages (e.g. OpenQASM [11] and Q# [47]). Parameterised
quantum gates are also supported by previous quantum programming lan-
guages, and they are recently generalised to differential quantum program-
ming [72, 17].
    Intuitively, q := |0⟩ means that quantum variable q is initialised in a basis
state |0⟩. The quantum gate U (t1 , ..., tm )[q1 , ..., qn ] and measurement com-
mand x := M [q1 , ..., qn ] were already explained in Subsections 3.1 and 3.2,
respectively. The meanings of other commands are the same as in a classi-
cal while-language. It is worth examining the interface between the classical
and quantum parts of qWhile + . In the quantum to classical direction, the
outcome of a quantum measurement M [q1 , ..., qn ] is stored in a classical vari-
able x, which can appear in a classical expression e and thus participate in a
classical computation, or in a classical boolean expression b and thus is used
in the control of subsequent computation. In the classical to quantum direc-
tion, a classical boolean expression b may be used in determining the control
flow of quantum computation. In addition, classical variables may appear
in the subscripts of some quantum array variables in U (t1 , ..., tm )[q1 , ..., qn ]
or M [q1 , ..., qn ] (see Definition 2.1) and thus determine the locations that
quantum gate U or measurement M performs on.

                                            12
QFT [q1 , ..., qn ] ::= H[q1 ]; C(R2 )[q2 , q1 ]; C(R3 )[q3 , q1 ]; ...; C(Rn−1 )[qn−1 , q1 ]; C(Rn )[qn , q1 ];
                        H[q2 ]; C(R2 )[q3 , q2 ]; C(R3 )[q4 , q2 ]; ...; C(Rn−1 )[qn , q2 ];
                                               ..............................
                        H[qn−1 ]; C(R2 )[qn , qn−1 ];
                        H[qn ];
                        Reverse[q1 , ..., qn ]

                Table 1: A quantum circuit for quantum Fourier transform.


Example 3.2. Let us consider an efficient circuit for the quantum Fourier
transform on n qubits q1 , ..., qn presented in Figure 5.1 of textbook [38]. It can
be equivalently written as the program in Table 1, where C(Rl )[qi , qj ] stands
for the controlled-Rl with qi as its control qubit and qj as its target qubit, Rl
denotes the single qubit gate (parameterised by classical integer variable l):
                                                  
                                        1     0
                                Rl =             l
                                        0 e2πi/2

and Reverse[q1 , ..., qn ] is the quantum gate that reverses the order of qubits
q1 , ..., qn . As in Example 2.1, we introduce a qubit array q of type integer →
H2 . Then the quantum circuit in Table 1 can be defined by induction on the
number n − m of qubits:

QFT [q[1 : n]] ::= QFT ∗ [q[1 : n]]; Reverse[q[1 : n]],
QFT ∗ [q[m : n]] ::= if m = n then H[q[n]]
                              else H[Q[m]]; CR[q[m : n]]; QFT ∗ [q[m + 1 : n]],
CR[q[m : n]] ::= if m = n then skip
                            else CR[q[m : n − 1]]; C(Rn−m+1 )[qn , qm ].

   The readers can find many more quantum program examples using quan-
tum arrays in the previous literature (for example [11, 47]). Also, variational
quantum algorithms [7] and quantum machine learning algorithms [4] can
be conveniently written as quantum programs with parameterised quantum
gates as defined above.


                                               13
3.4. Semantics of qWhile +
3.4.1. Interpretation of programming language
    As pointed out at the beginning of Subsection 3.3, qWhile + is obtained
by expanding the classical while-language. Thus, the semantics of quantum
programming language qWhile + is defined in a given classical structure as the
interpretation of its classical part (i.e. the while-language) together with a
quantum structure, as described in the following definition. For simplicity of
presentation, we omit the definition of a classical structure, which is standard
(for example, see Chapter 3 of [1] and Section 3.2 of [35]).

Definition 3.2. A quantum structure consists of:
  1. each quantum (simple or array) variable is assigned a quantum type Hq .
     Thus, the Hilbert space of all quantum variables is the tensor product:
                                         O
                                 Hall =     Hq .                         (4)
                                                   q∈QV


  2. each symbol U ∈ U with parameter type T1 × ... × Tm and quantum type
     H1 ⊗ ... ⊗ Hn is interpreted as a family of unitary operators,

                             {U (v1 , ..., vm )}(v1 ,...,vm )∈T1 ×...×Tm ,

      on H1 ⊗ ... ⊗ Hn . Equivalently, parameterised gate symbol U is inter-
      preted as a mapping:

                        U : T1 × ... × Tm → U (H1 ⊗ ... ⊗ Hn ) .
                            (v1 , ..., vm ) 7→ U (v1 , ..., vm ).

      Here, U (H1 ⊗ ... ⊗ Hn ) stands for the group of unitary operators on
      H1 ⊗ ... ⊗ Hn . For simplicity of presentation, we slightly abuse the
      notation so that the interpretation of U is also written as U . Thus, U
      satisfies the unitarity:

            U (v1 , ..., vm )† U (v1 , ..., vm ) = U (v1 , ..., vm )U (v1 , ..., vm )† = I

      for any (v1 , ..., vm ) ∈ T1 × ... × Tm , where I is the identity operator, and
      †
        stands for the adjoint of an operator.



                                             14
   3. each symbol M ∈ M with quantum type H1 ⊗ ... ⊗ Hn and classical type
      T is interpreted as a quantum measurement on H1 ⊗ ... ⊗ Hn , which is
      also denoted as M for simplicity; that is,

                                    M = {Mm }m∈T ,
                                                                   †
                                                           P
      and all Mm are operators on H1 ⊗ ... ⊗ Hn such that m∈T Mm     Mm = I
      (the identity operator). Obviously, the classical type T of M denotes
      the set of possible measurement outcomes m. In this paper, we always
      assume that the classical (outcome) type T of any measurement M is
      finite.

3.4.2. Operational semantics
    Now we assume that a pair of classical structure and quantum structure
is given as an interpretation of language qWhile + . We define a classical-
quantum state (cq-state or state for short) as a pair (σ, ρ), where σ is a
classical state (i.e. a state of classical variables defined in the classical struc-
ture, as a mapping from classical variables to the domain of the classical
structure), and ρ is a partial density operator on Hall , i.e. a positive oper-
ator with trace tr (ρ) ≤ 1 (following Selinger [44]), that is used to describe
the state of quantum variables. The set of all cq-states is denoted as Ω.
Then a configuration is defined as a triple (P, σ, ρ), where P is a quantum
program written in qWhile + or termination symbol ↓, and (σ, ρ) ∈ Ω is a cq-
state. Here, ρ denotes the state of quantum variables in the sense that the
quantum variables are in a (possibly mixed) state ρ/tr (ρ) with probability
tr (ρ), and the probability tr (ρ) comes from the measurements occurring in
the previous computation. Thus, we have:

Definition 3.3. The operational semantics of qWhile + is given as the tran-
sition relation → between configurations defined by the transition rules in
Table 2.

    The operational semantics defined above is a natural quantum extension
of the operational semantics of classical while-language. It is the same as that
for quantum programs with classical variables given in [63] except that here
we need to carefully deal with quantum arrays and parameterised quantum
gates, but [63] does not. However, it is different from those defined in [12, 21]
due to the treatment of cq-states (as explained in Section 1). Some notations
used in Figure 2 are explained as follows:

                                        15
(Ski) (skip, σ, ρ) → (↓, σ, ρ)         (Ass) (x := e, σ, ρ) → (↓, σ[x := σ(e)], ρ)
(Init) If B = {|n⟩} is an orthonormal basis of Hq and |0⟩ is a basis state in B, then :
                                                             !
                                   X
          (q := |0⟩, σ, ρ) → ↓, σ,   |0⟩σ(q) ⟨n|ρ|n⟩σ(q) ⟨0|
                                            n
                           σ |= Dist(q1 [s11 , ..., s1n1 ], ..., qk [sk1 , ..., sknk ])
(Uni)                                                                                                
         (U (t1 , ..., tm )[q1 [s11 , ..., s1n1 ], ..., qk [sk1 , ..., sknk ]], σ, ρ) → ↓, σ, Uσ ρUσ†
(Meas) If measurement symbol M is interpreted as M = {Mm } (in the given
         quantum structure), then for every possible outcome m :
                              σ |= Dist(q1 [s11 , ..., s1n1 ], ..., qk [sk1 , ..., sknk ])
         (x := M [q1 [s11 , ..., s1n1 ], ..., qk [sk1 , ..., sknk ]], σ, ρ) → (↓, σ[x := m], Mm   σ ρ(M σ )† )
                                                                                                       m
                               ′   ′ ′
            (P1 , σ, ρ) → (P1 , σ , ρ )
(Seq)
        (P1 ; P2 , σ, ρ) → (P1′ ; P2 , σ ′ , ρ′ )
                            σ |= b                                                       σ |= ¬b
(Cond)
       (if b then P1 else P0 , σ, ρ) → (P1 , σ, ρ)                    (if b then P1 else P0 , σ, ρ) → (P0 , σ, ρ)
                                  σ |= b                                                     σ |= ¬b
(Loop)
        (while b do P, σ, ρ) → (P ; while b do P, σ, ρ)                       (while b do P, σ, ρ) → (↓, σ, ρ)

                                  Table 2: Transition Rules.


    • In the transition rule (Ass), σ(e) denotes the value of classical expres-
      sion e in the classical state σ (in the given classical structure), and
      σ[x := σ(e)] stands for the classical state in which the value of x is
      σ(e) but the values of other classical variables are the same as in σ.

    • In the rule (Init), if q is a simple quantum variable, then σ(q) = q, and
      if q is a subscripted quantum variable q ′ [s1 , ..., sn ], then σ(q) denotes
      the quantum system q ′ [σ(s1 ), ..., σ(sn )].

    • The distinctness formula Dist(q) in the premises of the rules (Uni) and
      (Meas) means that q is a string of distinct (simple or subscripted) quan-
      tum variables (see equation (2) for its precise definition). This condition
      is introduced to guarantee that the quantum gates and measurements
      under consideration are well-defined. For example, let q be an array of


                                                16
      qubits. Then the controlled-NOT gate CNOT [q[2k + 1], q[4k − 3]] is
      meaningful in a classical state σ if and only if σ(k) ̸= 2.

   • In the conclusion of the rules (Uni) and (Meas), it should be noted
     that in the left hand side of transition →, U ∈ U and M ∈ M are a
     gate symbol and a measurement symbol, respectively, but in the right
     hand side of →, U and M stands for the interpretation of symbols
     U and M (in the given quantum structure), respectively. Moreover,
     Uσ means the unitary operator U (σ(t1 ), ..., σ(tm )) acting on quantum
     systems qi [σ(si1 ), ..., σ(sini )] (i = 1, ..., k), and Mm
                                                               σ
                                                                 means the mea-
     surement operator Mm acting on quantum systems qi [σ(si1 ), ..., σ(sini )]
     (i = 1, ..., k).

3.4.3. Denotational semantics
    Building upon the above operational semantics, we can introduce the
denotational semantics of quantum programs with classical variables:

Definition 3.4. Let P be a quantum program, and let (σ, ρ) ∈ Ω be a cq-
state. Then with input (σ, ρ), the output of P is defined to be the multi-set
of cq-states in Ω:

                 JP K(σ, ρ) = {|(σ ′ , ρ′ )|(P, σ, ρ) →∗ (↓, σ ′ , ρ′ )|}    (5)

where →∗ stands for the reflexive and transitive closure of transition relation
→, and {| · |} denotes a multi-set.

    Therefore, the denotational semantics of a quantum program P is defined
as a mapping from cq-states Ω to multi-sets of cq-states in Ω:

                             JP K : (σ, ρ) 7→ JP K(σ, ρ).

Furthermore, for any quantum program P , and for any states (σ, ρ), (σ ′ , ρ′ ) ∈
Ω, we write:
                                   P
                            (σ, ρ) ⇒ (σ ′ , ρ′ )                              (6)
if and only if (σ ′ , ρ′ ) ∈ JP K(σ, ρ). The denotational semantics can also be
understood in a slightly different way. Let Θ be a multi-set of cq-states in
Ω. Then for each classical state σ, we define:
                                     X
                            Θ(σ) =       {|ρ | (σ, ρ) ∈ Θ|}.                (7)

                                           17
We further define the normalisation of Θ as the set

                         N (Θ) = {(σ, Θ(σ)) | Θ(σ) ̸= 0}.

Obviously, for any classical state σ, there exists at most one quantum state
ρ such that (σ, ρ) ∈ N (Θ). Now given a quantum program P , for each input
state (σ, ρ) ∈ Ω, and for each classical state σ ′ , JP K(σ, ρ)(σ ′ ) is the summation
of (partial) quantum states ρ′ such that (σ ′ , ρ′ ) is outputted by P though
different execution paths. Thus, the denotational semantics of P can be
thought of as a mapping from Ω to 2Ω :

                           JP K : (σ, ρ) 7→ N (JP K(σ, ρ)).

    The following proposition gives an explicit representation of the deno-
tational semantics of quantum programs in terms of their structures. It is
often more convenient in applications than Definition 3.4. In particular, it
will be used in the proofs of soundness and (relative) completeness of our
QHL (quantum Hoare logic).

Proposition 3.1 (Structural Representation of Denotational Semantics).
For any input state (σ, ρ) ∈ Ω, we have:
   1. JskipK(σ, ρ) = {|(σ, ρ)|}.
   2. Jx := eK(σ, ρ) = {|(σ[x := σ(e)], ρ)|}.
   3. Jq := |0⟩K(σ, ρ) = |(σ, n |0⟩σ(q) ⟨n|ρ|n⟩σ(q) ⟨0|) .
                                  P

   4.                                      (
                                              |(σ, Uσ ρUσ† )| if σ |= Dist(q)
            JU (t1 , ..., tm )[q]K(σ, ρ) =
                                            ∅                 otherwise
        where Uσ denotes quantum gate U (σ(t1 ), ..., σ(tm )) acting on σ(q).
   5.
                               (
                                                       σ †
                                                  σ
                                                           
                                    | σ[x := m], Mm ρ(Mm ) |                    if σ |= Dist(q)
        Jx := M [q]K(σ, ρ) =
                                ∅                                               otherwise

        where m ranges over all possible outcomes of the measurement M , and
          σ
        Mm  denotes measurement operator Mm acting on q.
   6.                                                           [
             JP1 ; P2 K(σ, ρ) = JP2 K (JP1 K(σ, ρ)) =                       JP2 K(σ ′ , ρ′ ).
                                                        (σ ′ ,ρ′ )∈JP1 K(σ,ρ)


                                          18
   7.                                           (
                                                 JP1 K(σ, ρ) if σ |= b,
                Jif b then P1 else P0 K(σ, ρ) =
                                                 JP0 K(σ, ρ) if σ |= ¬b.
   8.
                                                                     P       P
        Jwhile b do P K(σ, ρ) = {|(σ ′ , ρ′ )|(σ, ρ) = (σ0 , ρ0 ) ⇒ ... ⇒ (σn , ρn ) = (σ ′ , ρ′ ),
                                              n ≥ 0, σi |= b (0 ≤ i < n) and σn |= ¬b|}

                               P
        where the relation ⇒ is defined as (6).

Proof. Routine by Definitions 3.3 and 3.4.
   The next proposition indicates that the trace of the state of quantum
variables does not increase during the execution of a program.

Proposition 3.2. For any quantum program P and for any input state
(σ, ρ) ∈ Ω, we have:
                  X
                     {|tr (ρ′ )|(σ ′ , ρ′ ) ∈ JP K(σ, ρ)|} ≤ tr (ρ).

Proof. It can be easily proved by induction on the structure of P . But it also
can be derived directly from Proposition 3.1.

3.4.4. Termination of programs
    Let us define:
                                         X
             NT (P )(σ, ρ) = tr (ρ) −         {|tr (ρ′ )|(σ ′ , ρ′ ) ∈ JP K(σ, ρ)|}      (8)

Then by Proposition 3.2 we know that 0 ≤ NT (P )(σ, ρ) ≤ 1. Furthermore, it
is clear from Definition 3.4 that NT (P )(σ, ρ) is the probability that program
P starting in state (σ, ρ) does not terminate. In particular, if NT (P )(σ, ρ) =
0; that is,
                                   X
   (Termination condition)             {|tr (ρ′ )|(σ ′ , ρ′ ) ∈ JP K(σ, ρ)|} = tr (ρ),

then we say that program P starting in state (σ, ρ) almost surely terminates.




                                             19
3.4.5. Equivalence of programs
    Before concluding this section, let us introduce the notion of equivalence
between quantum programs. Two multi-sets Θ1 , Θ2 of cq-states are said to
be equivalent, written Θ1 ≈ Θ2 , if for every classical state σ, it holds that
Θ1 (σ) = Θ2 (σ) according to the defining equation (7). It is easy to see that
any multiset Θ of cq-states is equivalent to its normalisation N (Θ); that is,
Θ ≈ N (Θ) = {(σ, Θ(σ))|Θ(σ) ̸= 0}. With this notation, we have:

Definition 3.5. Two quantum programs P1 , P2 are equivalent, written P1 ≈
P2 , if for any input state (σ, ρ) ∈ Ω, it holds that JP1 K(σ, ρ) ≈ JP2 K(σ, ρ).

    It is easy to see that whenever P1 ≈ P2 , when for any state (σ, ρ), P1
starting in (σ, ρ) almost surely terminates if and only if so does P2 . Moreover,
it will be shown in Section 5 that equivalent quantum programs enjoy the
same program logical properties specified as Hoare triples (see Lemma 5.1).

4. An Assertion Language for Quantum Programs with Classical
   Variables
    In this section, we turn to define an assertion language for specifying
preconditions and postconditions of the quantum programs with classical
variables described in Section 3. In this language, as briefly discussed in
Section 1, an assertion is a pair consisting of a classical first-order logical
formula that describes the property of classical variables and a quantum
predicate formula that describes the property of quantum variables.
    Quantum predicates were first introduced in [14] as observables repre-
sented by Hermitian operators between the zero and identity operators. This
purely semantic view of quantum predicates has been adopted in the previ-
ous research on quantum Hoare logic. However, it is hard to use in practical
verification of quantum programs, in particular, when formalised in a proof
assistant (e.g. Coq, Isabelle/HOL or Lean). Our experience in classical log-
ics indicates that syntactic representations of predicates are often much more
economic, because they can be constructed from atomic propositions using
propositional connectives, and in particular, they allow symbolic reasoning.
Therefore, a syntax of quantum predicates was defined in Section 7.6 of [61].
In this section, we extend it to include quantum predicates parameterized by
classical variables needed in the next section.



                                       20
4.1. Formal Quantum States
    Let us first introduce the notion of formal quantum state that will be
used to define some atomic quantum predicates in our assertion language.

Definition 4.1. Formal quantum states are inductively defined as follows:
   1. If t is a classical expression of type T , and q is a simple or subscripted
      quantum variable of type HT = span{|v⟩ : v ∈ T } (the Hilbert space
      with {|v⟩ : v ∈ T } as its orthonormal basis), then s = |t⟩q is a formal
      quantum state, and its signature is Sig(s) = {q};
   2. If s1 , s2 are formal quantum states, then s1 ⊗ s2 (often simply written
      s1 s2 ) is a formal quantum state too, and its signature is Sig(s1 ⊗ s2 ) =
      Sig(s1 ) ∪ Sig(s2 );
   3. If s1 , s2 are formal quantum states such that Sig(s1 ) = Sig(s2 ), and
      α1 , α2 are two classical expressions of type C (complex numbers), then
      α1 s1 + α2 s2 is a formal quantum states, and its signature is Sig(α1 s1 +
      α2 s2 ) = Sig(s1 ) = Sig(s2 ); and
   4. If s is a formal quantum state and U (t)[q] is a (parameterised) quantum
      gate defined in Subsection 3.1 with q ⊆ Sig(s), then (U (t)[q])s is a
      formal quantum state, and its signature is Sig((U (t)[q])s) = Sig(s).

    Intuitively, the formula (U (t)[q])s in the clause (4) of the above definition
means that quantum gate U (t)[q] is applied to formal quantum state s.
    The formal quantum states defined above are not a novel concept. In fact,
in the quantum information literature, it is common to represent a quantum
state in a form such as
      θ                                   θ
   cos |2k + 1⟩q[m+1] |n − 5⟩q[3m−4] + sin |2k − 1⟩q[m+1] |n + 3⟩q[3m−4]      (9)
      2                                   2
where the subscripts q[m+1] and q[3m−4] stand for the (m+1)st and (3m−
4)th subsystems, respectively, of a composite quantum system. Definition 4.1
simply formalises this commonly used practice as exemplified in (9).
    Now we assume that a classical structure and a quantum structure are
given as an interpretation of our programming language qWhile + (see Sub-
section 3.4). Then we can define the semantics of formal quantum states in
this interpretation.




                                       21
Definition 4.2. Let s be a formal quantum state. For any classical state
σ, if the semantics σ(s) of s in classical state σ is well-defined, then it is a
vector in Hilbert space
                                          O
                          Hσ(Sig(s)) =           Hq
                                             q∈σ(Sig(s))


where σ(Sig(s)) = {σ(q ′ )|q ′ ∈ Sig(s)}, and σ(q ′ ) is defined as in Subsection
3.4. The vector σ(s) is inductively defined as follows:
   1. σ (|t⟩q ) = |σ(t)⟩σ(q) ∈ Hσ(q) ;
   2. σ(s1 ⊗ s2 ) = σ(s1 ) ⊗ σ(s2 ) provided σ(Sig(s1 )) ∩ σ(Sig(s2 )) = ∅;
   3. σ(α1 s1 + α2 s2 ) = σ(α1 )σ(s1 ) + σ(α2 )σ(s2 ); and
   4. if σ |= Dist(q) (see equation (2) for its definition), then:
                                          
                             σ (U (t)[q])s = U (σ(t))σ(q) σ(s)

      where U (σ(t))σ(q) stands for the unitary operator U (σ(t)) performing on
      σ(q), σ(t) = σ(t1 ), ..., σ(tm ) if t = t1 , ..., tm , and σ(q) = σ(q1 ), ..., σ(qn )
      if q = q1 , ..., qn .
    It should be noticed that σ(s) is not always well-defined because the
disjoint condition in clause (2) and the distinction condition in clause (4)
may be violated. Whence these conditions are satisfied, it is a vector in the
Hilbert space Hσ(Sig(s)) , but it may not be a quantum state. If it is further the
case that the length ∥σ(s)∥ = 1, then σ(s) is a pure quantum state, and we
say that σ(s) is well-defined. Therefore, the semantics of a formal quantum
state s can be considered as a partial function from classical states to (pure)
quantum states in Hσ(Sig(s)) :

                  JsK : σ 7→ σ(s) whenever σ(s) is well-defined.

This semantic view indicates that a formal quantum state can be seen as a
quantum state parameterised by classical variables, and it coincides with the
definition of cq-states in [21].

4.2. Syntax of Quantum Predicates
    Now let us start to consider general quantum predicates. We assume a
set P of atomic quantum predicate symbols. Each quantum predicate symbol
K ∈ P is equipped with a family of classical variables x1 , ..., xm as its formal

                                           22
parameters, and it is also equipped with a quantum type H1 ⊗...⊗Hn , where
n is called the arity of K. We often write K = K(x1 , ..., xm ) in order to show
the parameters. If for any i ≤ m, ti is a classical expression with the same
type of xi , and for each j ≤ n, qj is a simple or subscripted quantum variables
with type Hj , then
                        K(t)[q] = K(t1 , ..., tm )[q1 , ..., qn ]              (10)
is called an atomic quantum predicate, where t = t1 , ..., tm and q = q1 , ..., qn .
    In particular, for any quantum type H1 ⊗ ... ⊗ Hn , we introduce quantum
predicate symbol IH1 ⊗...⊗Hn . It will be interpreted as the identity operator on
Hilbert space H1 ⊗...⊗Hn . Indeed, it can be viewed as the quantum version of
“true” in the domain H1 ⊗...⊗Hn . For simplicity, the subscript H1 ⊗...⊗Hn of
IH1 ⊗...⊗Hn is often omitted. For each formal quantum state s, we introduce
an atomic quantum predicate [s]. Intuitively, the quantum predicate [s]
means “to be in the state s”. As we will see later, mathematically, it denotes
(the projection operator onto) the one-dimensional subspace spanned by the
state s. Several other basic quantum predicates that are useful in practically
specifying correctness of quantum programs were introduced in Section 3 of
[59]; for example, unary quantum predicates defined by a subspace and a
unitary operator, and symmetric and anti-symmetric operators as quantum
counterparts of equality and inequality. We expect that more basic quantum
predicates will be conceived in future applications of quantum Hoare logic
and other program logics for quantum programs [51, 29, 69, 56, 67, 33, 51, 2].
    Recall that in classical logics, one uses connectives to construct compound
propositions from atomic propositions. Here, we use the following connectives
for quantum predicates:
  (i) negation ¬;
 (ii) tensor product ⊗; and
(iii) a family F of Kraus operator symbols. Each Kraus operator symbol
      F ∈ F is assigned a rank k, equipped with a family of classical variables
      x1 , ..., xm as its formal parameters, and equipped with a quantum type
      of the form H1 ⊗ ... ⊗ Hn , where n is called the arity of F . We often
      write F = F (x1 , ..., xm ) to show the parameters.
      In particular, we require:
         • for each basic quantum type (i.e. Hilbert space) H and an or-
           thonormal basis B of it, a Kraus operator symbol FB ∈ F of rank
           d is designated, where d = dim H;

                                           23
        • for each (parameterized) quantum gate symbol U ∈ U with (clas-
          sical) parameter type T1 × ... × Tm , a Kraus operator symbol
          FU (x1 , ..., xm ) of rank 1 is designated, where xi is a classical vari-
          able of type Ti for 1 ≤ i ≤ m;
        • for each measurement symbol M ∈ M, a Kraus operator symbol
          FM (x) ∈ F of rank k (with a formal parameter x) is designated,
          where k is the number of possible measurement outcomes.
     If F (x1 , ..., xm ) is a Kraus operator symbol with type H1 ⊗ ... ⊗ Hn , and
     for each i ≤ n, qi is a simple or subscripted quantum variables with
     type Hi , then
                               F (t)[q] = F (t1 , ..., tm )[q1 , ..., qn ]    (11)
     is called a Kraus operator, where ti is a classical expression with the
     same type as xi for 1 ≤ i ≤ m, called the actual parameters.
   Upon the alphabet of quantum predicates described above, we can intro-
duce the syntax of quantum predicates:
Definition 4.3. Quantum predicate formulas are inductively defined as fol-
lows:
              A ::= K(t)[q] | ¬A | A1 ⊗ A2 | F (t)[q]({Ai }).
  1. An atomic quantum predicate K(t)[q] of the form given in equation (10)
     is a quantum predicate formula, and its signature is Sig(K(t)[q]) = {q} ;
  2. If A is a quantum predicate formula, then so is ¬A, and Sig(¬A) =
     Sig(A);
  3. If A1 and A2 are quantum predicate formulas, then A1 ⊗A2 is a quantum
     predicate formula, and Sig(A1 ⊗ A2 ) = Sig(A1 ) ∪ Sig(A2 );
  4. If Kraus operator symbol F has rank k, {Ai } is a family of k quantum
     predicate formulas with the same signature Sig(Ai ) = X, and q ⊆ X,
     then
                                 F (t)[q]({Ai })
     is a quantum predicate formula, and Sig(F (t)[q]({Ai }) = X. In partic-
     ular, if all Ai are the same quantum predicate formula A, then F (t)[q]({Ai })
     is abbreviated to F (t)[q](A).
    With the above syntax, one can use connectives to construct various
quantum predicate formulas from atomic quantum predicates (e.g. those [s]
defined by formal quantum states s). We will see how quantum predicate

                                       24
formulas, constructed from atomic quantum predicates with Kraus operator
symbols FB , FU and FM , can be used in formulating the axioms and proof
rules of our quantum Hoare logic with classical variables in the next section.
Furthermore, using the other connectives of quantum predicates introduced
above, various useful auxiliary proof rules can be formulated to ease the veri-
fication of quantum programs with classical variables (for example, quantum
generalisations of the rules for classical programs given in Section 3.8 of [1]
and generalisations of the rules for purely quantum programs presented in
Section 6.7 of [61] to quantum programs with classical variables).

4.3. Semantics of Quantum Predicates
    As in Subsection 3.4, we assume a classical structure and a quantum
structure as the interpretation of our language for quantum predicates. To
define the semantics of quantum predicates, however, we need extend the
quantum structure by adding the following:
  1. each quantum predicate symbol K(x1 , ..., xm ) ∈ P with type H1 ⊗
     ... ⊗ Hn is interpreted as a family of effects, i.e. Hermitian operators
     between 0 and I on H1 ⊗ ... ⊗ Hn , where 0 and I stand for the zero
     and identity operators, respectively. For simplicity of presentation, the
     interpretation of K is written as K too. So, we have:

                                 K = {K(a1 , ..., am )} ,

     where for i ≤ m, ai ranges over the values of classical variable xi ,
     and for each fixed tuple (a1 , ..., an ) of parameters, K(a1 , ..., am ) is an
     operator such that 0 ≤ K(a1 , ..., am ) ≤ I, where ≤ stands for the
     Löwner order; that is, A ≤ B if and only if B −A is a positive operator.
     Consequently, K(a1 , ..., am )† = K(a1 , ..., am ); that is, K(a1 , ..., am ) is a
     Hermitian operator and can be seen as an observable in physics. It
     should be pointed out that this interpretation of K is consistent with
     the notion of quantum predicate defined in [14] in the sense that for a
     fixed tuple (a1 , ..., am ), K(a1 , ..., am ) is exactly a quantum predicate in
     the sense of [14].
     In particular, for each formal quantum state s, the atomic quantum
     predicate [s] is interpreted as the projection operator onto the one-
     dimensional subspace spanned by quantum state σ(s), where σ(s) is the
     semantics s in σ (see Definition 4.2). For example, if formal quantum


                                         25
     state
                            θ     1              θ     1
                    s = cos |x − ⟩q[3n−2] + sin |x + ⟩q[3n−2] ,
                            2     2              2     2
     and classical state σ is given by σ(θ) = 2 , σ(x) = 12 , σ(n) = 3, then [s]
                                               π

     is interpreted as operator |+⟩⟨+| on the state space of qubit q[7], where
     |+⟩ = √12 (|0⟩ + |1⟩).
  2. each Kraus operator symbol F (x1 , ..., xm ) ∈ F with rank k and type
     H1 ⊗ ... ⊗ Hn is interpreted as a family

                                   F = {Fi (a1 , ..., am )}

     of k operators on H1 ⊗ ... ⊗ Hn , where i ranges over k indices. Fur-
     thermore, each Fi (a1 , ..., am ) is parameterised by a1 , ..., am , where for
     j ≤ m, aj ranges over the values of classical variable xj . It is required
     that for a fixed tuple (a1 , ..., am ) of parameters, {Fi (a1 , ..., am )} satisfies
     the normalization condition:
                         X
                             Fi (a1 , ..., an )Fi† (a1 , ..., an ) = I.             (12)
                            i

     In particular,
        • for an orthonormal basis B = {|n⟩}, the Kraus operator symbol
          FB is interpreted as FB = {|0⟩⟨n|}, where |0⟩ is a fixed basis state
          in B;
        • for any (parameterised) quantum gate symbol U ∈ U, if in the
          given quantum structure, U is interpreted a family {U (v1 , ..., vm )}
          of unitary operators (see Subsection
                                              3.4), then the Kraus operator
          symbol FU is interpreted as FU = U (v1 , ..., vm ) ;
                                                            †

        • for any measurement symbol M ∈ M, if in the quantum structure,
          M is interpreted as M = {Mm }, then
                                            the  Kraus operator symbol
          FM (m) is interpreted as FM (m) = Mm .
                                              †


    We should notice the dualities between basis B, unitary operator U , mea-
surement M and their corresponding Kraus operators FB , FU , FM , respec-
tively.
    Given the above classical structure and (extended) quantum structure as
the interpretation of our language for quantum predicates, we can introduce
the following:

                                          26
Definition 4.4. For each quantum predicate formula A and for a classical
state σ, the interpretation σ(A) of A in σ is inductively defined as follows:
  1. If A = K(t)[q] is an atomic quantum predicate, then:
      (a) whenever σ ̸|= Dist(q), then σ(A) is not well-defined;
      (b) whenever σ |= Dist(q), then

                                   σ(A) = K(σ(t))σ(q)                     (13)

          Note that K in the right hand side of equation (13) denotes the in-
          terpretation of atomic predicate symbol K. Furthermore, K(σ(t))σ(q)
          stands for the operator K(σ(t)) acting on the quantum systems
          σ(q).
     In particular, if A = [s] is an atomic quantum predicate defined by a
     formal quantum state s, and σ(s) = |ψ⟩ is well-defined (see Definition
     4.2), then σ(A) = |ψ⟩⟨ψ|.
  2. If A = ¬B, then:
      (a) σ(A) is not well-defined when σ(B) is not well-defined; and
      (b) σ(A) = I − σ(B) when σ(B) is well-defined. Here, I stands for
          the identity operator on Hilbert space Hσ(Sig(B)) .
  3. If A = A1 ⊗ A2 , then:
      (a) σ(A) is not well-defined when either σ(A1 ) or σ(A2 ) is not well-
          defined, or σ(Sig(A1 )) ∩ σ(Sig(A2 )) ̸= ∅; and
      (b) σ(A) = σ(A1 )⊗σ(A2 ) when both σ(A1 ) and σ(A2 ) are well-defined,
          and σ(Sig(A1 )) ∩ σ(Sig(A2 )) = ∅.
  4. If A = F (t)[q]({Bi }) and Kraus operator symbol F is interpreted as
     F = {Fi (a)}, then:
      (a) whenever σ(Bi ) is not well-defined for some i or σ ̸|= Dist(q),
          then σ(A) is not well-defined;
      (b) whenever σ(Bi ) is well-defined for every i and σ |= Dist(q), then
                              X
                      σ(A) =      Fi (σ(t))σ(q) · σ(Bi ) · Fi† (σ(t))σ(q) (14)
                               i

          where Fi (σ(t))σ(q) stands for the operator Fi (σ(t)) acting on quan-
          tum systems σ(q).

    The above definition is a parameterised extension of Definition 7.23 in
[61]. Now it is a right time to explain why we use the term “Kraus operator”.

                                     27
Equation (14) is essentially motivated by Kraus’ operator-sum representa-
tion of quantum operations (i.e. quantum channels) (see Section 8.2.3 of
[38]). Kraus operators will be used in defining proof rules (Rule-Accum1)
and (Rule-Accum2) of our logic QHL+ .
    To illustrate the concepts introduced above, let us see the following simple
example:

Example 4.1. We consider an n-dimensional Hilbert space with basis {|i⟩|i =
0, 1, ..., n − 1}. Let formal quantum state si denote the basis state |i⟩. Then:
  1. Atomic quantum predicate Ai = [si ] stands for observable (projection
     operator) |i⟩⟨i|;
  2. ¬An−1 denotes observable (projection operator) n−2
                                                        P
                                                            i=0 |i⟩⟨i|.
  3. If
     √we use Kraus operator symbol
                                P       F (x0 , ..., xn−1 ) to denote a family
        xi of real numbers with i xi ≤ 1; that is,

                         F (x0 , ..., xn−1 ) = {Fi (x0 , ..., xn−1 )}
                                 √
      with Fi (x0 , ..., xn−1 ) = xi (viewed as a 0-dimensional operator) for
      0 ≤ i ≤ nP  − 1, then F (p1 , ..., pn )({Ai }) stands for observable (positive
      operator) i pi |i⟩⟨i|.

   The following lemma shows that every quantum predicate formula indeed
represents a quantum predicate parameterised by classical variables.

Lemma 4.1. For any quantum predicate formula A and for any classical sate
σ, whenever σ(A) is well-defined, then it is an effect; that is, an observable
(i.e. a Hermitian operator) on Hσ(Sig(A)) between the zero operator and the
identity operator.

Proof. Routine by induction on the structure of A.
    Thus, the semantics of a quantum predicate formula A can be understood
as a partial function from classical states to Hermitian operator on Hσ(Sig(A)) :

               JAK : σ 7→ σ(A) whenever σ(A) is well-defined.

This understanding is consistent with the notion of cq-predicate defined in
[21].
    To conclude this subsection, we introduce the following:


                                         28
Definition 4.5. Let A, B be two quantum predicate formulas and φ a clas-
sical first-order logical formula. Then:
  1. By the entailment under condition φ:

                                           φ |= A ≤ B

     we mean that for any classical state σ, whenever σ |= φ, then either both
     σ(A) and σ(B) are not well-defined, or both of them are well-defined
     and σ(A) ≤ σ(B); that is, σ(B) − σ(A) is a positive operator.
  2. By equivalence under condition φ:

                                           φ |= A ≡ B

      we mean that φ |= A ≤ B and φ |= B ≤ A; that is, whenever σ |= φ,
      then σ(A) is well-defined if and only if so is σ(B), and in this case
      σ(A) = σ(B).
   For example, we use the same notation
                                  p ′ as in Example 4.1, andPlet Kraus
operator symbol F denote a family
                   ′
                                      pi of real numbers with i p′i ≤ 1,
then it holds that

      (∀i)(pi ≤ p′i ) |= F (p0 , ..., pn−1 )({Ai }) ≤ F (p′0 , ..., p′n−1 )({Ai }).   (15)

   Some basic properties of the entailment are given in the following:
Proposition 4.1.      1. Entailment is reflexive, anti-symmetric and transi-
     tive:
      (a) φ |= A ≤ B and φ |= B ≤ A if and only if φ |= A ≡ B;
      (b) If φ |= A ≤ B and φ |= B ≤ C, then φ |= A ≤ C.
  2. Entailment is preserved by quantum predicate connectives:
      (a) If φ |= A ≤ B, then φ |= ¬B ≤ ¬A and φ |= A ⊗ C ≤ B ⊗ C;
      (b) If φ |= Ai ≤ Bi for every i, then φ |= F (t)[q]({Ai }) ≤ F (t)[q]({Bi }).
Proof. Routine by definition.

4.4. Substitutions for Quantum Predicates
    In this subsection, we introduce the notion of substitution in a quantum
predicate formula, which is needed in formulating the axioms and proof rules
of our quantum Hoare logic in the next section. It can be defined in a manner
familiar to us from classical logic:

                                             29
Definition 4.6. Let A be a quantum predicate formula, x a classical variable
and e a classical expression. Then the substitution A[e/x] of e for x in A is
a quantum predicate formula inductively defined as follows:
  1. If A = K(t)[q], then

                               A[e/x] = K(t[e/x])[q[e/x]].                               (16)

  2. If A = ¬B, then A[e/x] = ¬(B[e/x]).
  3. If A = F (t)[q]({Bi }), then

                          A[e/x] = F (t[e/x])[q[e/x]](Bi [e/x])                          (17)

     where:
      (a) for t = t1 , ..., tm , we set t[e/x] = t1 [e/x], ..., tm [e/x]; and
      (b) for q = q1 [s11 , ..., s1n1 ], ..., qk [sk1 , ..., sknk ], we set:

             q[e/x] = q1 [s11 [e/x], ..., s1n1 [e/x]], ..., qk [sk1 [e/x], ..., sknk [e/x]].

   As in the case of classical logic, we can prove the following substitution
lemma. It will be used in proving the soundness of our quantum Hoare logic
with classical variables to be presented in the next section.

Lemma 4.2 (Substitution for Quantum Predicates). For any quantum pred-
icate formula A and classical state σ, we have:
  1. σ(A[e/x]) is well-defined if and only if so is σ[x := σ(e)](A); and
  2. if they are well-defined, then

                              σ(A[e/x]) = σ[x := σ(e)](A),

where σ[x := σ(e)] is the update of σ that agrees with σ except for x where
its value is σ(e).

Proof. For readability, we deferred the tedious proof to Appendix A.1

4.5. Classical-Quantum Assertions
    Now we are ready to define an assertion language for quantum programs
with classical variables by combining classical first-order logic and quantum
predicate formulas introduced above.


                                           30
Definition 4.7. A classical-quantum assertion (cq-assertion or simply as-
sertion for short) is a pair (φ, A), where:
  1. φ is a classical first-order logical formula; and
  2. A is a quantum predicate formula (see Definition 4.3).
    As pointed out in Section 1, these cq-assertions (φ, A) will be employed
in specifying preconditions and postconditions of quantum programs with
classical variables. Intuitively, φ describes the properties of classical vari-
ables and A describes that of quantum variables in a program. It should be
particularly noticed that φ and A are not independent of each other. In-
deed, quantum predicate A is parameterised by classical variables, as seen
in the previous subsections. Thus, classical logical formula φ puts certain
constraints on quantum predicate A.
    The entailment and equivalence relations between cq-assertions can be
defined as follows:
Definition 4.8.       1. Entailment: (φ, A) |= (ψ, B) if φ |= ψ (entailment in
     classical first-order logic) and φ |= A ≤ B (see Definition 4.5(1)).
  2. Equivalence: (φ, A) ≡ (ψ, B) if φ ≡ ψ (equivalence in classical first-
     order logic) and φ |= A ≡ B (see Definition 4.5(2)).
    The following proposition asserts that the entailment between cq-assertions
is a reflexive, anti-symmetric and transitive relation:
Proposition 4.2.       1. (φ, A) |= (ψ, B) and (ψ, B) |= (φ, A) if and only if
     (φ, A) ≡ (ψ, B);
  2. If (φ, A) |= (ψ, B) and (ψ, B) |= (χ, C), then (φ, A) |= (χ, C).
Proof. Immediate by definition.
    For applications of our quantum Hoare logic to be presented in the next
section, the entailment between cq-assertions and quantum Hoare triples
(correctness formulas) will be used together in reasoning about the correct-
ness of quantum programs. On the other hand, it is clear from Definition 4.5
that classical first-order logic is helpful in proving the entailment between
quantum predicate formulas (e.g. the entailment (15)) and thus in establish-
ing the entailment between cq-assertions, as we can see from Definition 4.8.
Therefore, we will need to exploit effective techniques and tools for verifying
the entailment between quantum predicate formulas based on classical logic
in order to implement practical tools for verification of quantum programs
with classical variables.

                                      31
5. Proof System for Quantum Programs with Classical Variables
    Building on the preparations in the previous sections, we are able to
develop a Hoare-style logic in this section for reasoning about the correctness
of quantum programs written in the programming language qWhile + .

5.1. Correctness Formulas
    As in the classical Hoare logic, we use Hoare triples to specify correctness
of quantum programs with classical variables. The cq-assertions defined in
Subsection 4.5 are employed as preconditions and postconditions to define
the correctness formulas of quantum programs. More precisely, we use a
quantum Hoare triple of the form:
                                  {φ, A} P {ψ, B}                                   (18)
as a correctness formula of a quantum program P , where φ, ψ are first-
order logical formulas, called the classical precondition and postcondition,
respectively, and A, B are quantum predicate formulas (see Definition 4.3),
called quantum precondition and postcondition, respectively. A quantum
Hoare triple of the form (18) has two different interpretations:
Definition 5.1.     1. We say that Hoare triple {φ, A} P {ψ, B} is true in
     the sense of total correctness, written
                                  |=tot {φ, A} P {ψ, B},
     if for any input (σ, ρ), whenever σ |= φ and σ(A) is well-defined, then
     it holds that
                   X
     tr (σ(A)ρ) ≤     {|tr (σ ′ (B)ρ′ ) |(σ ′ , ρ′ ) ∈ JP K(σ, ρ), σ ′ |= ψ, and σ ′ (B) is well-defined|} .
                                                                                      (19)
  2. The partial correctness:
                                  |=par {φ, A} P {ψ, B}
      is defined if inequality (19) is weakened by the following:
                     X
      tr (σ(A)ρ) ≤      {|tr (σ ′ (B)ρ′ ) |(σ ′ , ρ′ ) ∈ JP K(σ, ρ), σ ′ |= ψ, and σ ′ (B) is well-defined|}
                         + NT (P )(σ, ρ)
                                                                                    (20)
    where NT (P )(σ, ρ) stands for the probability that program P starting in
state (σ, ρ) does not terminate (see its defining equation (8)).

                                          32
    The above definition is a natural quantum generalisation of the notions
of partial and total correctness in classical Hoare logic. First, we note that
a premise of inequalities (19) and (20) is σ |= φ, which means that the ini-
tial classical state σ satisfies the precondition φ for classical variables. On
the other hand, the requirement that the final classical state σ ′ satisfies the
postcondition ψ for classical variables (i.e. σ ′ |= ψ) is imposed in the right-
hand side of inequalities (19) and (20). Furthermore, according to Definition
4.4, σ(A) denotes the observable specified by quantum predicate A in clas-
sical state σ. By the interpretation of quantum mechanics, we know that
tr (σ(A)ρ) is the expectation of observable σ(A) in quantum state ρ, which
can be understood as the degree that quantum state ρ satisfies quantum pred-
icate A in classical state σ. The same interpretation applies to tr (σ ′ (B)ρ′ ).
Therefore, inequalities (19) and (20) are essentially the quantitative versions
of the following two statements, respectively:
   • Total correctness: for any input cq-state (σ, ρ), whenever (σ, ρ) sat-
     isfies cq-assertion (φ, A), then program P terminates and its output
     (σ ′ , ρ′ ) satisfies cq-assertion (ψ, B);

   • Partial correctness: for any input cq-state (σ, ρ), whenever (σ, ρ)
     satisfies cq-assertion (φ, A), then either program P does not terminate,
     or it terminates and its output (σ ′ , ρ′ ) satisfies cq-assertion (ψ, B).

Example 5.1. Let |(j, k : l)⟩ and |QFT (j, k : l)⟩ be defined as in Example
2.2. They can be seen as formal quantum states. Thus,

                A(j, k : l) ≡ |(j, k : l)⟩q[k:l] ⟨(k, l)|,
                B(j, k : l) ≡ |QFT (j, k : l)⟩q[k:l] ⟨QFT (j, k : l)|

are two atomic quantum predicate formulas. All of these quantum states
and predicates are parameterised by classical variables j, k and l. Then the
correctness of the program QFT [q[1 : n]] in Example 3.2 can be specified by
the following Hoare triple:

             {1 ≤ n, A(j, 1 : n)} QFT [q[1 : n]] {true, B(j, 1 : n)}        (21)

for any classical bit array j.
   The following lemma asserts that both partial and total correctness are
invariant under the equivalence of quantum programs.

                                         33
Lemma 5.1. If P1 ≈ P2 (see Definition 3.5), then for any precondition
(φ, A) and postcondition (ψ, B), it holds that

             |=par {φ, A} P1 {ψ, B} iff |=par {φ, A} P2 {ψ, B},              (22)
             |=tot {φ, A} P1 {ψ, B} iff |=tot {φ, A} P2 {ψ, B}.              (23)

Proof. By definitions of program equivalence and correctness and the linear-
ity of trace (see Appendix A.2).

5.2. Proof System
    Now we can present the proof system of our quantum Hoare logic with
classical variables, denoted QHL+ . The axioms and proof rules for partial
correctness are presented in Table 3. The axioms and proof rules for total
correctness are the same except that the rule for while-loop is changed to the
rule (Rule-Loop-tot) in Table 4. We write QHL+  par and QHLtot for the groups
                                                              +

of axioms and proof rules for partial and total correctness, respectively.
    Most of the axioms and rules in our quantum Hoare logic QHL+       par and
QHL+ tot look similar to the corresponding ones  in classical Hoare logic. But
the following two ideas behind the design decision of our proof system are
worth mentioning:
   • The substitution in quantum predicate formulas defined in Subsection
     4.4 are used in formulating (Axiom-Ass) and (Axiom-Meas), and Kraus
     operators on quantum predicates introduced in Subsections 4.2 and 4.3
     are employed in formulating (Axiom-Init), (Axiom-Uni) and (Axiom-
     Meas).

   • The design idea of (Axiom-Meas) is particularly interesting. Note that
     the measurement M in the command x := M [q] yields a probability
     distribution D = {Prob[x = m]} over possible outcomes m, where
     Prob[x = m] stands for the probability that the measurement outcome
     is m. It was believed by the authors of [21, 12] that it is unavoidable to
     introduce a kind of substitution [D/x] of variable x by probability dis-
     tribution D in the precondition in order to properly formulate (Axiom-
     Meas). This will make this axiom much more complicated and harder
     to use in practical verification. In our logic QHL+ , this difficulty is cir-
     cumvented by introducing equality x = y in the postcondition, where
     y is a fresh variable standing for a possible outcome. Thus, we only
     need to use the ordinary substitution [y/x] of x by a variable y rather

                                       34
(Axiom-Ski)    {φ, A} skip {φ, A}
(Axiom-Ass)     {φ[e/x], A[e/x]} x := e {φ, A}
(Axiom-Init)    {φ, FB [q](A)} q := |0⟩ {φ, A}
                
(Axiom-Uni)       φ, FU (t)[q](A) U (t)[q] {φ, A}
                                   y∈ / free(φ) ∪ cv (A) ∪ {x}
(Axiom-Meas)
                 {φ[y/x], FM (y)[q](A[y/x])} x := M [q] {φ ∧ x = y, A}
                  {φ, A} P1 {ψ, B}            {ψ, B} P2 {θ, , C}
(Rule-Seq)
                              {φ, A} P1 ; P2 {θ, C}
                  {φ ∧ b, A} P1 {ψ, B}            {φ ∧ ¬b, A} P0 {ψ, B}
(Rule-Cond )
                         {φ, A} if b then P1 else P0 {ψ, B}
                            {φ ∧ b, A} P {φ, A}
(Rule-Loop-par )
                    {φ, A} while b do P {φ ∧ ¬b, A}
                      (φ′ , A′ ) |= (φ, A)       {φ, A} P {ψ, B}               (ψ, B) |= (ψ ′ , B ′ )
(Rule-Conseq)
                                                {φ′ , A′ } P {ψ ′ , B ′ }
                    {φ, Ai } P {ψi , B} for every i          (∀i1 , i2 ) (i1 ̸= i2 → ¬(ψi1 ∧ ψi2 ))
                  q ∩ qv (P ) = ∅        [var (t) ∪ cv (q)] ∩ change(P ) = ∅            F (t) ∝ F ′ (t)
(Rule-Accum1 )                                              W n            ′
                                   φ, F (t)[q]({Ai }) P         i=1 ψi , F (t)[q](B)
                                    {φ, Ai } P {ψ, Bi } for every i
                       q ∩ qv (P ) = ∅      [var (t) ∪ cv (q)] ∩ change(P ) = ∅
(Rule-Accum2 )                                        
                              φ, F (t)[q]({Ai }) P ψ, F (t)[q]({Bi })

Table 3: Proof System QHL+       par . In (Axiom-Init), B = {|n⟩} is an orthonormal basis
and |0⟩ is a basis state in B. In (Axiom-Meas), free(φ), cv (A) stand for the set of free
classical variables in classical first-order logical formula φ and the set of classical variables
in (the subscripts of) quantum predicate formula A, respectively. In (Rule-Accum1) and
(Rule-Accum2), qv (P ) stands for the set of quantum variables in program P , change(P )
for the set of classical variables that can be modified by program P , var (t) for the set
of (classical) variables in t, and cv (q) for the set of classical variables in the (possibly
subscripted) quantum variables.




                                               35
                                           {φ ∧ b, A} P {φ, A}
                                      {φ ∧ b ∧ t = z, I} P {t < z, I}
                                                 φ→t≥0
             (Rule-Loop-tot)
                                     {φ, A} while b do P {φ ∧ ¬b, A}

Table 4: Proof System QHL+   tot . In (Rule-Loop-tot), t is an integer expression, z is an
integer variable and z ∈
                       / free(φ) ∪ var (b) ∪ var (t) ∪ cv (P ). The symbol I stands for the
identity quantum predicate on Hqv (P ) .


      than by a probability distribution in the precondition. Of course, there
      is a price for this simplification: the probabilities of different measure-
      ment outcomes stored in variable y may need be accumulated in later
      reasoning, as discussed next.

    • Since (Axiom-Meas) is designed so that different possible outcomes
      of a measurement can be treated separately, we need a mechanism
      to accumulated them together. For this purpose, (Rule-Accum1) is
      introduced in order to merge the postconditions for classical variables
      by the logical connective of disjunction. The formula F (t) ∝ F ′ (t) in
      the premise of (Rule-Accum1) needs careful explanation. Here, F (x)
      is a Kraus operator symbol of rank, say k and F ′ (x) a Kraus operator
      symbol of rank 1, and they have the same type, say H1 ⊗...⊗Hn . Given
      a classical structure and a quantum structure. Let σ be a classical state.
      Then σ |= F (t) ∝ F ′ (t) if for any i ≤ k, we have:

                     Fi† (σ(t)) · ρ · Fi (σ(t)) ≤ F ′† (σ(t)) · ρ · F ′ (σ(t))

      for all density operators ρ on H1 ⊗ ... ⊗ Hn . A special case of (Rule-
      Accum1) is the following rule:

                             {φ, Ai } P {ψi , B} for every i 0 ≤ pi for every i
                                                                                              P
                                                                                              i pi ≤ 1
                                             (∀i1 , i2 ) (i1 ̸= i2 → ¬(ψi1 ∧ ψi2 ))
      (Rule-Convex1)                           P                   W
                                         {φ, i pi Ai } P { i ψi , maxi pi · B}

    • As a complement to (Rule-Accum1), we propose (Rule-Accum2), which
      enables the combination of different preconditions and postconditions
      for quantum variables using a Kraus operator. A special case of (Rule-
      Accum2) is the following rule, which handles convex combinations of

                                            36
      quantum predicates in the preconditions and postconditions, weighted
      according to a sub-probability distribution:

                        {φ, Ai } P {ψ, Bi } for every i 0 ≤ pi for every i
                                                                           P
                                                                            i pi ≤ 1
      (Rule-Convex2)                         P               P
                                        {φ, i pi Ai } P {ψ, i pi Bi }

    It must be pointed out that there are some fundamental differences (e.g.
nondeterminism caused by quantum measurements) between the semantics
behind QHL+ and classical Hoare logic, although their axioms and proof rules
look similar. This should already been noticed through the discussions in the
previous sections. It can be seen even more clearly through reading the proofs
of the soundness theorem in Appendix A.3 and the (relative) completeness
theorem in [62].
    A key advantage of the logic QHL+ presented above over previous ap-
proaches (e.g. [21]) is its ability to seamlessly integrate classical first-order
logic into the specification and verification of quantum programs with clas-
sical variables (see also the discussions at the end of Subsection 4.5). The
readers will recognise the value of this feature through their practical appli-
cations of QHL+ .

Example 5.2. We prove the correctness (21) of the circuit realisation of
quantum Fourier transform in the logic QHL+ . Here, we only present an
outline of the proof, and some details are given in Appendix A.4. From this
example we can see that introducing the data structure of quantum array often
enables us to verify quantum programs in a more convenient and elegant way.
   (1) We introduce atomic quantum predicate

               B ∗ (j, k : l) = |QFT ∗ (j, k : l)⟩q[k:l] ⟨QFT ∗ (j, k : l)|

where formal quantum state QFT ∗ (j, k : l) is inductively defined as follows:
(
 |QFT ∗ (j, k : l)⟩ = √12 |0⟩ + e2πi0.j[l] |1⟩ if k = l,
                                              

 QFT ∗ (j, r − 1 : l) = √12 |0⟩ + e2πi0.j[l−r:l] |1⟩ ⊗ |QFT ∗ (j, r : l) for k + 1 ≤ r ≤ l.
                                                    


Then using (Axiom-Uni) we can show that

            {true, B ∗ (j, 1 : n)} Reverse[q[1 : n]] {true, B(j, 1 : n)}        (24)

(The detailed proof of (24) is deferred to Appendix A.4).

                                           37
   (2) Let
                               1
                         |φ⟩ = √ |0⟩ + e2πi0.j[m] |1⟩).
                                2
Obviously, we have:
                                                 
           m < n, |A[m]⟩q[m] ⟨A[m]|    H[q[m]]        m < n, |φ⟩q[m] ⟨φ| .

Since A(j, m : n) = |A[m]⟩q[m] ⟨A[m]| ⊗ A(j, m + 1 : n), it holds that

  {m < n, A(j, m : n)} H[q[m]] m < n, |φ⟩q[m] ⟨φ| ⊗ A(j, m + 1 : n) . (25)
                                 

   (3) Let
                              1
                        |ψ⟩ = √ |0⟩ + e2πi0.j[m:n] |1⟩).
                               2
We can prove:
     
       m < n, |φ⟩q[m] ⟨φ| ⊗ A(j, m + 1 : n) CR[q[m : n]]
                                                                            (26)
                                m < n, |ψ⟩q[m] ⟨ψ| ⊗ A(j, m + 1 : n)

by induction on the length n−m of quantum array q[m : n] (The detailed proof
of (26) can be found in Appendix A.4). Using (Rule-Seq), a combination of
(25) and (26) yields
                                          
{m < n, A(j, m : n)} H[q[m]]; CR[q[m : n]] m < n, |ψ⟩q[m] ⟨ψ| ⊗ A(j, m + 1 : n) .
                                                                        (27)
    (4) Now we prove:

         {m ≤ n, A(j, m : n)} QFT ∗ [q[m : n]] {true, B ∗ (j, m : n)}        (28)

by induction on the length n − m of quantum array q[m : n]. First, it is
obvious by definitions of A(j, m : n) and B ∗ (j, m : n) that

{m = n, A(j, m : n)} H[q[n]] {m = n, B ∗ (j, m : n)} |= {true, B ∗ (j, m : n)} .
                                                                            (29)
For the case of m < n, by the induction hypothesis we obtain:

 {m + 1 ≤ n, A(j, m + 1 : n)} QFT ∗ [q[m + 1 : n]] {true, B ∗ (j, m + 1 : n)} .
                                                                           (30)
By the inductive definition of B ∗ (j, m : n) we have:

                B ∗ (j, m : n) = |ψ⟩q[m] ⟨ψ| ⊗ B ∗ (j, m + 1 : n).

                                       38
Consequently, it holds that
  m < n, |ψ⟩q[m] ⟨ψ| ⊗ A(j, m + 1 : n) QFT ∗ [q[m+1 : n]] {true, B ∗ (j, m : n)} .


                                                                           (31)
Then we can use (Rule-Seq) to combine (27) and (31) and thus derive:
{m < n, A(j, m : n)} H[q[m]]; CR[q[m : n]]; QFT ∗ [q[m+1 : n]] {true, B ∗ (j, m : n)}.
                                                                           (32)
Therefore, employing (Rule-Cond), we obtain:
          {m ≤ n, A(j, m : n)} QFT ∗ [q[m : n]] {true, B ∗ (j, m : n)}.      (33)
from (29), (32) and the inductive definition of QFT ∗ [q[m : n]].
    (5) Finally, using (Rule-Seq), we obtain (21) from (24) and (33). Thus,
the correctness of the circuit implementation (Table 1) of quantum Fourier
transform is verified.

6. Soundness Theorem
    In this section, we present the soundness theorem of our quantum Hoare
logic QHL+ .
Theorem 6.1 (Soundness). For any quantum program P , classical first-
order logical formulas φ, ψ, and quantum predicate formulas A, B, we have:
          ⊢QHL+par {φ, A} P {ψ, B} implies |=par {φ, A} P {ψ, B};
          ⊢QHL+tot {φ, A} P {ψ, B} implies |=tot {φ, A} P {ψ, B}.
Proof. The basic idea of the proof is the same as usual: we prove that every
axiom in QHL+ is valid, and the validity is preserved by each rule in QHL+ .
But some calculations in the proof are quite involved. So, for readability, we
defer the lengthy details of the proof into Appendix A.3.
    The above soundness theorem warrants that if the correctness of a quan-
tum program written in the programming language qWhile + can be proved in
logic QHL+ par (respectively, QHLtot ), then it is indeed partially (respectively,
                                   +

totally) correct. Conversely, we can establish a (relative) completeness of
our logic, which affirms that with a certain assumption about the expres-
sive power of the assertion language, partial (respectively, total) correctness
of quantum programs written in qWhile + can always be proved in QHL+           par
(respectively, QHL+ tot ). But the presentation  and proof of the (relative) com-
pleteness theorem require much more technical preparations and theoretical
treatments. So, we postpone them to a companion paper [62].

                                       39
7. Conclusion
    In this paper, we develop a Hoare-style logic for quantum programs with
classical variables, termed QHL+ . It incorporates the following key features:
  (i) support for quantum arrays and parameterised quantum gates, en-
      abling more versatile quantum programming; and
 (ii) a syntax for quantum predicates, allowing the construction of complex
      quantum predicate formulas from atomic predicates using logical con-
      nectives. These quantum predicate formulas can also be parameterised
      by classical variables. Consequently, preconditions and postconditions
      can be expressed as pairs consisting of a classical first-order logical
      formula (describing properties of classical variables) and a quantum
      predicate formula (describing properties of quantum variables).
The first feature enhances the convenience of quantum programming, while
the second facilitates the derivation of a simple proof system for quantum
programs through minimal modifications to classical Hoare logic. As a result,
QHL+ allows for more intuitive specification of quantum program correctness
and enables more effective verification compared to previous approaches. In
particular, classical first-order logic can be seamlessly integrated with QHL+
for verifying quantum programs with classical variables.
    To conclude this paper, we would like to point out several topics for
further research:
  1. Formalisation of the logic QHL+ for quantum programs with classical
     variables in proof assistants such as Coq, Isabelle/HOL, or Lean.
  2. Applications to the verification of quantum algorithms, QEC (quantum
     error correction) codes and quantum communication and cryptographic
     protocols, leveraging the tools developed in point (1).
  3. Extension of QHL+ to parallel and distributed quantum programs [19,
     66] as well as its applications to relational reasoning [52, 2, 33, 57], local
     reasoning [29, 69], and reasoning about incorrectness [56] of quantum
     programs.
  4. Broader applications of the quantum programming language qWhile +
     and the assertion language defined in Section 4, beyond verification.
     For instance, these could be utilised to develop more advanced tech-
     niques of abstract interpretation [68, 27, 42], refinement [39, 22] and
     symbolic execution [16, 6, 37, 3] for quantum programs.


                                       40
    Acknowledgement: The author is very grateful to the referees for their
invaluable comments and suggestions which help to improve the presentations
significantly. The author also would like to thank the members of Tsinghua’s
quantum programming group for their valuable feedback, particularly for
identifying several errors in the original version of this paper.
    After this paper was published in Information and Computation 309
(2026), Yuanjie Ren, Jinzheng Li, and Yidi Qi used their AI-agentic aut-
oformalization framework to formalize the logic QHL+ in Lean. During this
process, a gap was found in the proof of the soundness theorem (Theorem
6.1) for the case of total correctness. The author is particularly grateful to
them for bringing this gap to attention. In this revision, the gap has been
fixed.

References
 [1] K. R. Apt, F. S. de Boer and E. -R. Olderog, Verification of Sequential
     and Concurrent Programs, Springer, London 2009.

 [2] G. Barthe, J. Hsu, M. S. Ying, N. K. Yu and L. Zhou, Relational proofs
     for quantum programs, Proceedings of ACM Programming Languages
     4(2020) POPL: art. 21:1-29.

 [3] F. Bauer-Marquart, S. Leue and C. Schilling, symQV: automated sym-
     bolic verification of quantum programs, Proceedings of the 25th Inter-
     national Symposium on Formal Methods (FM), 2023, pp. 181-198.

 [4] J. Biamonte, P. Wittek, N. Pancotti, P. Rebentrost, N. Wiebe and S.
     Lloyd, Quantum machine learning, Nature 549(2017) 195-202.

 [5] G. Birkhoff and J. von Neumann, The logic of quantum mechanics,
     Annals of Mathematics, 37(1936) 823-843.

 [6] J. Carette, G. Ortiz and A. Sabry, Symbolic execution of Hadamard-
     Toffoli quantum circuits, Proceedings of the 2023 ACM International
     Workshop on Partial Evaluation and Program Manipulation (PEPM),
     pp. 14-26.

 [7] M. Cerezo, A. Arrasmith, R. Babbush, S. C. Benjamin, S. Endo, K.
     Fujii, J. R. McClean, K. Mitarai, X. Yuan, L. Cincio and P. J. Coles,

                                     41
    Variational quantum algorithms, Nature Reviews Physics 3(2021) 625-
    644.

 [8] R. Chadha, P. Mateus and A. Sernadas, Reasoning about imperative
     quantum programs, Electronic Notes in Theoretical Computer Science,
     158(2006)19-39.

 [9] C. Chareton, S. Bardin, F. Bobot, V. Perrelle and B. Valiron, An au-
     tomated deductive verification framework for circuit-building quantum
     programs, Proceedings of the 30th European Symposium on Program-
     ming (ESOP), 2021, pp. 148-177.

[10] C. Chareton, D. Lee, B. Valiron, R. Vilmart, S. Bardin and Z. W. Xu,
     Formal methods for quantum algorithms, in: Handbook of Formal Anal-
     ysis and Verification in Cryptography, CRC Press 2023, pp. 319-422.

[11] A. Cross, A. Javadi-Abhari, T. Alexander, N. De Beaudrap, L. S.
     Bishop, S. Heidel, C. A. Ryan, P. Sivarajah, J. Smolin, J. M. Gambetta
     and B. R. Johnson, OpenQASM 3: a broader and deeper quantum as-
     sembly language, ACM Transactions on Quantum Computing 3(2022)
     12:1-50.

[12] Y. X. Deng and Y. Feng, Formal semantics of a classical-quantum lan-
     guage, Theoretical Computer Science 913(2022) 73-93.

[13] Y. X. Deng, H. L. Wu and M. Xu, Local reasoning about probabilis-
     tic behaviour for classical–quantum programs, Proceedings of the 25th
     International Conference on Verification, Model Checking, and Abstract
     Interpretation (VMCAI), 2024, pp. 163-184.

[14] E. D’Hondt and P. Panangaden, Quantum weakest preconditions, Math-
     ematical Structures in Computer Science, 16(2006)429-451.

[15] C. M. Do, T. Takagi and K. Ogata, Automated quantum program veri-
     fication in probabilistic dynamic quantum logic, The 2nd International
     Workshop on Formal Analysis and Verification of Post-Quantum Cryp-
     tographic Protocols, 2023.

[16] W. Fang and M. S. Ying, Symbolic execution for quantum error correc-
     tion programs, Proceedings of ACM Programming Languages 8(2024)
     PLDI: 1040-1065.

                                    42
[17] W. Fang, M. S. Ying and X. D. Wu, Differentiable quantum program-
     ming with unbounded loops, ACM Transactions on Software Engineer-
     ing and Methodology 33(2024) 19:1-63.

[18] Y. Feng, R. Y. Duan, Z. F. Ji and M. S. Ying, Proof rules for the
     correctness of quantum programs, Theoretical Computer Science, 386
     (2007), 151-166.

[19] Y. Feng, S. J. Li and M. S. Ying, Verification of distributed quantum
     programs, ACM Transactions on Computational Logic 23(2022), art.
     19:1-40.

[20] Y. Feng and Y. T. Xu, Verification of nondeterministic quantum pro-
     grams, Proceedings of the 28th ACM International Conference on Ar-
     chitectural Support for Programming Languages and Operating Systems
     (ASPLOS), 2023, pp. 789-805.

[21] Y. Feng and M. S. Ying, Quantum Hoare logic with classical variables,
     ACM Transactions on Quantum Computing 2(2021) art. 16, pp. 1-43.

[22] Y. Feng, L. Zhou and Y. Xu, Refinement calculus of quantum programs
     with projective assertions, arXiv 2311.14215 (2023).

[23] D. J. Foulis and M. K. Bennett, Effect algebras and unsharp quantum
     logics, Foundations of Physics 24(1994) 1331-1352.

[24] J. D. Hartog and E. P. de Vink, Verifying probabilistic programs using
     a Hoare like logic, International Journal of Foundations of Computer
     Science, 13 (2003)315-340.

[25] K. Hietala, A Verified Software Toolchain for Quantum Programming,
     PhD Thesis, University of Maryland, 2022.

[26] K. Hietala, R. Rand, S. H. Hung, X. D. Wu and M. Hicks, A verified
     optimizer for quantum circuits, Proceedings of the ACM on Programming
     Languages 5(2021): POPL, art. no. 31:1-29.

[27] P. Jorrand and S. Perdrix, Abstract interpretation techniques for quan-
     tum computation, in: I. Mackie, S. Gay (Eds.), Semantic Techniques in
     Quantum Computation, Cambridge University Press, 2010, pp. 206-234.


                                    43
[28] Y. Kakutani, A logic for formal verification of quantum programs, In:
     Proceedings of the 13th Asian Computing Science Conference (ASIAN),
     Springer LNCS 5913, 2009, pp. 79-93.

[29] X. -B. Le, S. -W. Lin, J. Sun and D. Sanán, A quantum interpreta-
     tion of separating conjunction for local reasoning of quantum programs
     based on separation logic, Proceedings of ACM Programming Languages
     6(2022) POPL: 1-27.

[30] M. Lewis, S. Soudjani and P. Zuliani, Formal verification of quantum
     programs: theory, tools and challenges, ACM Transactions on Quantum
     Computing 5(2024) art. 1:1-35.

[31] L. Y. Li, M. W. Zhu, R. Cleaveland, A. Nicolellis, Y. Lee, L. Chang
     and X. D. Wu, Qafny: a quantum-program verifier, arXiv : 2211.06411
     (2022).

[32] L. Y. Li, F. Voichick, K. Hietala, Y. X. Peng, X. D. Wu and M. Hicks,
     Verified compilation of quantum oracles, Proceedings of the ACM on
     Programming Languages 6(OOPSLA2) 589-615.

[33] Y. J. Li and D. Unruh, Quantum relational Hoare logic with expecta-
     tions, ICALP 2021. art. 136: 1-20.

[34] J. Y. Liu, B. H. Zhan, S. L. Wang, S. G. Ying, T. Liu, Y. J. Li, M. S.
     Ying and N. J. Zhan, Formal verification of quantum algorithms using
     quantum Hoare logic, Proceedings of the 31st International Conference
     on Computer Aided Verification (CAV), 2019, pp. 187-207.

[35] J. Loeckx and K. Sieber, Foundations of Program Verification, John
     Wiley & Sons, Chichester 1987.

[36] P. Mateus and A. Sernadas, Weakly complete axiomatization of ex-
     ogenous quantum propositional logic, Information and Computation
     204(2006) 771-794.

[37] G. Meuli, M. Soeken, M. Roetteler and T. Häner, Enabling accuracy-
     aware Quantum compilers using symbolic resource estimation, Proceed-
     ings of the ACM on Programming Languages 4(2020) OOPSLA: 130.1-
     26.


                                    44
[38] M. A. Nielsen and I. L. Chuang, Quantum Computation and Quantum
     Information, Cambridge University Press, 2000.

[39] A. Peduri, I. Schaefer and M. Walter, QbC: quantum correctness by
     construction, arXiv :2307.15641 (2023).

[40] Y. X. Peng, Theoretical and Practical High-Assurance Software Tools
     for Quantum Applications, PhD Thesis, University of Maryland, 2024.

[41] Y. X. Peng, K. Hietala, R. Z. Tao, L. Y. Li, R. Rand, M Hicks and
     X. D. Wu, A formally certified end-to-end implementation of Shor’s
     factorization algorithm, Proceedings of the National Academy of Sciences
     120(2023) e2218775120.

[42] S. Perdrix, Quantum entanglement analysis based on abstract interpre-
     tation, in: Proceedings of the 2008 International Static Analysis Sympo-
     sium (SAS), pp. 270-282.

[43] R. Rand, Formally Verified Quantum Programming, PhD Thesis, Uni-
     versity of Pennsylvania, 2018.

[44] P. Selinger, Towards a quantum programming language, Mathematical
     Structures in Computer Science 14(2004) 527-586.

[45] Y. N. Shi, Compilation, Optimization and Verification of Near-Term
     Quantum Computing, PhD Thesis, University of Chicago, 2020.

[46] K. Singhal, R. Rand and M. Amy, Beyond separation: toward a speci-
     fication language for modular reasoning about quantum programs, Pro-
     gramming Languages for Quantum Computing (PLanQC), 2022.

[47] K. Svore, A. Geller, M. Troyer, J. Azariah, C. Granade, B. Heim, V.
     Kliuchnikov, M. Mykhailova, A. Paz and M. Roetteler, Q# enabling
     scalable quantum computing and development with a high-level domain-
     specific language, Proceedings of the Real World Domain Specific Lan-
     guages Workshop, 2018, pp. 7:1-10.

[48] T. Takagi, C. M. Do and K. Ogata, Automated quantum program veri-
     fication in dynamic quantum logic, Proceedings of the 5th International
     Workshop on Dynamic Logic, 2023, pp.68-84.


                                     45
[49] R. Z. Tao, Formal Verifcation of Quantum Software, PhD Thesis, Uni-
     versity of Columbia, 2024.
[50] R. Z. Tao, Y. N. Shi, J. Yao, X. Li, A. Javadi-Abhari, A. W. Cross,
     F. T. Chong, R. H. Gu, Giallar: push-button verification for the qiskit
     quantum compiler, Proceedings of the 43rd ACM International Confer-
     ence on Programming Language Design and Implementation, 2022, pp.
     641-656.
[51] D. Unruh, Quantum Hoare logic with ghost variables, Proceedings of
     the 34th Annual ACM/IEEE Symposium on Logic in Computer Science
     (LICS), 2019.
[52] D. Unruh, Quantum relational Hoare logic, Proceedings of ACM Pro-
     gramming Languages 3(2019) POPL: art. 33:1-31.
[53] B. Valiron, On Quantum Programming Languages, Habilitation Disser-
     tation, University of Paris - Saclay, 2024.
[54] J. von Neumann, On infinite direct products, Compositio Mathematica,
     tome 6(1939) 1-77.
[55] Z. Xu, M. S. Ying and B. Valiron, Reasoning about recursive quantum
     programs, arXiv :2107.11679 (2021).
[56] P. Yan, H. R. Jiang and N. K. Yu, On incorrectness logic for quan-
     tum programs, Proceedings of ACM Programming Languages 6(2022)
     OOPSLA: 1-28.
[57] P. Yan, H. R. Jiang and N. K. Yu, Approximate relational reasoning for
     quantum programs, Proceedings of the 36th International Conference on
     Computer Aided Verification (CAV), 2024, pp. 495-519.
[58] M. S. Ying, Floyd-Hoare logic for quantum programs, ACM Transac-
     tions on Programming Languages and Systems 33(2011) art. no: 19, pp.
     1-49.
[59] M. S. Ying, Toward automatic verification of quantum programs, Formal
     Aspects of Computing 31(2019) 3-25.
[60] M. S. Ying, Birkhoff-von Neumann quantum logic as an assertion lan-
     guage for quantum programs, arXiv 2205.01959 (2022).

                                    46
[61] M. S. Ying, Foundations of Quantum Programming (Second Edition),
     Morgan Kauffman, 2024.

[62] M. S. Ying, A practical quantum Hoare logic with classical variables, II,
     in preparation.

[63] M. S. Ying and Y. Feng, A flowchart language for quantum program-
     ming, IEEE Transactions on Software Engineering 37(2011) 466-485.

[64] M. S. Ying and Z. C. Zhang, Quantum recursive programming with
     quantum case statements, arXiv 2311.01725 (2023).

[65] M. S. Ying and Z. C. Zhang, Verification of recursively defined quantum
     circuits, arXiv 2404.05934 (2024).

[66] M. S. Ying, L. Zhou and Y. J. Li, Reasoning about parallel quantum
     programs, arXiv : 1810.11334 (2018).

[67] N. K. Yu, Quantum temporal logic and reachability problems of matrix
     semigroups, Information and Computation 300(2024) 105197.

[68] N. K. Yu, J. Palsberg, Quantum abstract interpretation, in: Proceedings
     of the 42nd ACM International Conference on Programming Language
     Design and Implementation (PLDI), 2021, pp. 542-558.

[69] L. Zhou, G. Barthe, J. Hsu, M. S. Ying and N. K. Yu, A quantum
     interpretation of bunched logic & quantum separation logic, LICS 2021:
     1-14.

[70] L. Zhou, G. Barthe, P. -Y. Strub, J. Y. Liu and M. S. Ying, CoqQ:
     foundational verification of quantum programs, Proceedings of ACM
     Programming Languages 7(2023) POPL: 833-865.

[71] L. Zhou, N. K. Yu and M. S. Ying, An applied quantum Hoare logic,
     Proceedings of the 40th ACM Conference on Programming Language
     Design and Implementation (PLDI), 2019, pp. 1149-1162.

[72] S. P. Zhu, S. -H. Hung, S. Chakrabarti and X. D. Wu, On the princi-
     ples of differentiable quantum programming languages, Proceedings of
     the 41st ACM Conference on Programming Language Design and Im-
     plementation (PLDI), 2020, pp. 272-285.


                                     47
Appendix A. Appendix: Deferred Proofs
Appendix A.1. Proof of Lemma 4.2
   We prove the substitution lemma by induction on the structure of quan-
tum predicate formula A.
   Case 1: A = K(t)[q]. Then A[e/x] = K(t[e/x])[q[e/x]]. We assume that

                    q = q1 [s11 , ..., s1n1 ], ..., qk [sk1 , ..., sknk ].

Then

σ(A[e/x]) is well-defined ⇔ σ |= Dist(q[e/x])
⇔ σ |= (∀i, j ≤ k) (qi = qj → (∃l ≤ ni ) (sil [e/x] ̸= sjl [e/x])) (by Eq.(2))
         = ((∀i, j ≤ k) (qi = qj → (∃l ≤ ni ) (sil ̸= sjl )))[e/x]
⇔ σ[x := σ(e)] |= (∀i, j ≤ k) (qi = qj → (∃l ≤ ni ) (sil ̸= sjl ))
                                 (by the substitution lemma in first-order logic)
⇔ σ[x := σ(e)] |= Dist(q)        (by Eq.(2))
⇔ σ[x := σ(e)](A) is well-defined.

    Now assume that σ(A[e/x]) is well-defined. It follows from the substitu-
tion lemma for classical expressions that

                           σ[t[e/x]] = σ[x := σ(e)](t).                       (A.1)

On the other hand, by the same lemma, it is easy to show that

                          σ(q[e/x]) = σ[x := σ(e)](q).                        (A.2)

Therefore, by Definition 4.4, we obtain:

                 σ(A[e/x]) = K(σ(t[e/x]))σ(q[e/x])
                           = K(σ[x := σ(e)](t))σ[x:=σ(e)](q)
                           = σ[x := σ(e)](A).

   Case 2: A = ¬B. Then A[e/x] = ¬(B[e/x]) and

 σ(A[e/x]) = I − σ(B[e/x])                              (by Definition 4.4)
           = I − σ[x := σ(e)](B)                (by the induction hypothesis on B)
           = σ[x := σ(e)](A).                             (by Definition 4.4)

                                             48
    Case 3: A = F (t)[q]({Bi }). Then
                          A[e/x] = F (t[e/x])[q[e/x]](Bi [e/x])
and
                X
σ(A[e/x]) =           Fi (σ(t[e/x]))σ(q[e/x]) · σ(Bi [e/x]) · Fi† (σ(t[e/x]))σ(q[e/x])
                  i
                                                                           (by Definition 4.4)
    X
=         Fi (σ[x := σ(e)](t))σ[x:=σ(e)](q) · σ[x := σ(e)](Bi ) · Fi† (σ[x := σ(e)](t))σ[x:=σ(e)](q)
      i
                                   (by Eqs.(A.1) and (A.2) and the induction hypothesis on Bi )
= σ[x := σ(e)](A).                                       (by Definition 4.4)
Appendix A.2. Proof of Lemma 5.1
   Suppose that P1 ≈ P2 . We only prove (22); (23) can be proved in a similar
way. Assume cq-state (σ, ρ) satisfies that σ |= φ and σ(A) is well-defined.
Then for each σ ′ , we set:
                          Θi (σ ′ ) = {|ρ′ | (σ ′ , ρ′ ) ∈ JPi K(σ, ρ)|}
for i = 1, 2. By the definition of P1 ≈ P2 , we have Θ1 (σ ′ ) = Θ2 (σ ′ ). Then:
                          X
NT (P1 )(σ, ρ) = tr (ρ) −     {|tr (ρ′ ) | (σ ′ , ρ′ ) ∈ JP1 K(σ, ρ)|}
                          Xn X                                                                 o
               = tr (ρ) −       |      {|tr (ρ′ ) | ρ′ ∈ Θ1 (σ ′ )|} |σ ′ is a classical state|
                          Xn X                                                                 o
               = tr (ρ) −       |      {|tr (ρ′ ) | ρ′ ∈ Θ2 (σ ′ )|} |σ ′ is a classical state|
                          X
               = tr (ρ) −     {|tr (ρ′ ) | (σ ′ , ρ′ ) ∈ JP2 K(σ, ρ)|}
                  = NT (P2 )(σ, ρ).
Furthermore, let “:WD” stand for “is well-defined”. If |=par {φ, A} P1 {ψ, B},
then:
             X
tr (σ(A)ρ) ≤     {|tr (σ ′ (B)ρ′ ) | (σ ′ , ρ′ ) ∈ JP1 K(σ, ρ), σ ′ |= ψ and σ ′ (B) : W D|}
             Xn X                                                                            o
           =       |      {|tr (σ (B)ρ ) | ρ ∈ Θ1 (σ )|} | σ |= ψ and σ (B) : W D|
                                  ′      ′       ′        ′          ′            ′

             Xn X                                                                            o
           =       |      {|tr (σ ′ (B)ρ′ ) | ρ′ ∈ Θ2 (σ ′ )|} | σ ′ |= ψ and σ ′ (B) : W D|
             X
           =    {|tr (σ ′ (B)ρ′ ) | (σ ′ , ρ′ ) ∈ JP2 K(σ, ρ), σ ′ |= ψ and σ ′ (B) : W D|}

                                               49
and |=par {φ, A} P2 {ψ, B}.
   Conversely, we can prove that |=par {φ, A} P2 {ψ, B} implies |=par {φ, A} P1 {ψ, B}.

Appendix A.3. Proof of Theorem 6.1
Appendix A.3.1. The Case of Partial Correctness
   We first prove the soundness of proof system QHL+    par . It suffices to sow
that every axiom in QHLpar is valid in the sense of partial correctness, and
                          +

the validity in the sense of partial correctness is preserved by each rule in
QHL+ par .
   (Axiom-Ass): We prove:

                       |=par {φ[e/x], A[e/x]} x := e {φ, A}.

For any input state (σ, ρ) ∈ Ω, by the transition rule (Ass), we have:

                       Jx := eK(σ, ρ) = {|(σ[x := σ(e)], ρ)|}.

If σ |= φ[e/x] and σ(A[e/x]) is well-defined, then by the substitution lemma
for classical first-order logic (Lemma 2.4 in [1]), it holds that σ[x := σ(e)] |=
φ. On the other hand, by Lemma 4.2 (the substitution lemma for quantum
predicates), we know that σ[x := σ(e)](A) is well-defined and

                            σ[x := σ(e)](A) = σ(A[e/x]).

Consequently, we have:

tr (σ(A[e/x])ρ) = tr (σ[x := σ(e)](A)ρ)
    X
 =     {|tr (σ ′ (A)ρ′ |(σ ′ , ρ′ ) ∈ Jx := eK(σ, ρ), σ ′ |= φ, and σ ′ (A) is well-defined|}.

    (Axiom-Init): We prove:

                        |=par {φ, FB [q](A)} q := |0⟩ {φ, A}.

For any input state (σ, ρ) ∈ Ω, if σ |= φ and σ (FB [q](A)) is well-defined, then
according to the interpretation of modifier FB and clause (3) in Definition
4.4, we know that σ(A) is well-defined, and
                                   X
                 σ (FB [q](A)) =       |n⟩σ(q) ⟨0|σ(A)|0⟩σ(q) ⟨n|.
                                        n


                                            50
Therefore, we have:
                          X
                                                                                      (A.3)
                                                             
tr (σ (FB [q](A)) ρ) =         tr |n⟩σ(q) ⟨0|σ(A)|0⟩σ(q) ⟨n|ρ
                           n
                          X
                                                                                      (A.4)
                                                             
                      =        tr σ(A)|0⟩σ(q) ⟨n|ρ|n⟩σ(q) ⟨0|
                           n
                                                                 !
                                      X
                      = tr     σ(A)        |0⟩σ(q) ⟨n|ρ|n⟩σ(q) ⟨0|                    (A.5)
                                       n
                          X
                      =        {|tr (σ ′ (A)ρ′ )|(σ ′ , ρ′ ) ∈ Jq := |0⟩K(σ, ρ) and σ ′ (A) is well-define|}
                                                                                         (A.6)

where (A.3) and (A.5) comes from the linearity of trace, (A.4) follows from
the equality tr (AB) = tr (BA), and (A.6) is from Proposition 3.1(2).
   (Axiom-Uni): We prove:
                           
                     |=par φ, FU (t)[q] U (t)[q] {φ, A}.

For any input state (σ, ρ) ∈ Ω, if σ |= φ and σ FU (t)[q](A) is well-defined,
                                                            

then by Definition 4.4(3), we know that σ |= Dist(q), σ(A) is well-defined,
and
                        σ FU (t)[q](A) = Uσ† σ(A)Uσ ,
                                       

where Uσ denotes the unitary operator U (σ(t)) acting on quantum systems
σ(q). On the other hand, it follows from σ |= Dist(q) and transition rule
(Uni) that
                    JU (t)[q]K(σ, ρ) = |(σ, Uσ ρUσ† )| .
                                      

Therefore, we obtain:

tr σ(FU (t)[q](A))ρ = tr (Uσ† σ(A)Uσ )ρ
                                                

 = tr σ(A)(Uσ ρUσ† )
                        
   X
 =     {|tr (σ ′ (A)ρ′ |(σ ′ , ρ′ ) ∈ JU (t)[q]K(σ, ρ), σ ′ |= φ, and σ ′ (A) is well-defined|}.

   (Axiom-Meas): For any classical variable y ∈ free(φ) ∪ free(A) ∪ {x},
we prove:

          |=par {φ[y/x], FM (y)[q](A[y/x])} x := M [q] {φ ∧ x = y, A}.


                                              51
For any input state (σ, ρ) ∈ Ω, if σ |= φ[y/x] and σ(FM (y)[q](A[y/x])) is
well-defined, then σ |= Dist(q) and σ(A[y/x]) is well-defined. By transition
rule (Meas), we have:
                                    σ    σ †
                     
Jx := M [q]K(σ, ρ) = (σ[x := m], Mm   ρ(Mm ) )|m ranges over allpossible outcomes m
                                                                          (A.7)
where Mm  σ
             means that operator Mm acting on quantum systems q.
    Now Let us set m = σ(y) ∈ T (the outcome type of measurement M ),
σ0 = σ[x := m] and ρ0 = Mm   σ
                               ρ(Mm ) . Then it follows from the assumption
                                   σ †

σ |= φ[y/x] and the substitution lemma for classical first-order logic (Lemma
2.4 in [1]) that
                           σ0 = σ[x := σ(y)] |= φ.                        (A.8)
On the other hand, we have:
                   σ0 (x) = σ[x := m](x) = m = σ(y) = σ0 (y).
Thus, σ0 |= x = y. Combining this with (A.8), we obtain σ0 |= φ ∧ x = y.
  Furthermore, we have:
                                        σ
                                           †            σ
              σ(FM (y)[q](A[y/x])) = Mσ(y)    σ(A[y/x])Mσ(y)
                                            σ †           σ
                                         =(Mm ) σ(A[y/x])Mm
                                            σ †        σ
                                         =(Mm ) σ0 (A)Mm
because it follows from the substitution lemma for quantum predicate for-
mulas (Lemma 4.2) that
            σ(A[y/x]) = σ[x := σ(y)](A) = σ[x := m](A) = σ0 (A).
In addition, from the fact that σ(A[y/x]) is well-defined and Lemma 4.2, we
can assert that σ0 (A) = σ[x := σ(y)](A) is well-defined. Therefore, we have:
                                              σ †          σ
                                                             
tr [σ(FM (y)[q](A[y/x]))ρ] = tr (Mm            ) σ0 (A)Mm       ρ
                    σ       σ †
                                 
 = tr σ0 (A) Mm ρ(Mm )
 = tr (σ0 (A)ρ0 )
    X
 =      {|tr (σ ′ (A)ρ′ )|(σ ′ , ρ′ ) ∈ Jx := M [q]K(σ, ρ), σ ′ |= φ ∧ x = y, and σ ′ (A) is well-defined|} .

   (Rule-Seq): We prove that |=par {φ, A} P1 {ψ, B} and |=par {ψ, B} P2 {θ, C}
imply
                      |=par {φ, A} P1 ; P2 {θ, C}.

                                           52
First, for any state (σ, ρ) ∈ Ω, it is easy to show from transition rule (Seq)
that
                                                 [
       JP1 ; P2 K(σ, ρ) = JP2 K (JP1 K(σ, ρ)) =        JP2 K(σ ′ , ρ′ ). (A.9)
                                                               (σ ′ ,ρ′ )∈JP1 K(σ,ρ)


Now we set:

    L1 (σ, ρ) = {|(σ ′ , ρ′ ) ∈ JP1 K(σ, ρ)|σ ′ |= ψ and σ ′ (B) is well-defined|},
    L2 (σ ′ , ρ′ ) = {|(σ ′′ , ρ′′ ) ∈ JP2 K(σ ′ , ρ′ )|σ ′′ |= θ and σ ′′ (C) is well-defined|} .

Using (A.9), we can see that
    [
           L2 (σ ′ , ρ′ ) ⊆ {|(σ ′′ , ρ′′ ) ∈ JP1 ; P2 K(σ, ρ)|σ ′′ |= θ and σ ′′ (C) is well-define|} .
(σ ′ ,ρ′ )∈L1 (σ,ρ)
                                                                                (A.10)
   By the assumptions |=par {φ, A} P1 {ψ, B} and |=par {ψ, B} P2 {θ, C},
we obtain:
   (Claim 1 ) If σ |= φ and σ(A) is well-defined, then
              X
 tr (σ(A)ρ) ≤     {|tr (σ ′ (B)ρ′ )|(σ ′ , ρ′ ) ∈ L1 (σ, ρ)|} + NT (P1 )(σ, ρ). (A.11)

     (Claim 2 ) If σ ′ |= ψ and σ(B) is well-defined, then
                      X
    tr (σ ′ (B)ρ′ ) ≤     {|tr (σ ′′ (C)ρ′′ )|(σ ′′ , ρ′′ ) ∈ L2 (σ ′ , ρ′ )|} + NT (P2 )(σ ′ , ρ′ ).
                                                                                              (A.12)
     Then by combining (A.11) and (A.12), we have: if σ |= φ and σ(A) is
well-defined, then
                  X
tr (σ(A)ρ) ≤          {|µ(σ ′ , ρ′ ) + NT (P2 )(σ ′ , ρ′ )|(σ ′ , ρ′ ) ∈ L1 (σ, ρ)|} + NT (P1 )(σ, ρ)
                  X
               =      {|µ(σ ′ , ρ′ )|(σ ′ , ρ′ ) ∈ L1 (σ, ρ)|}
                           X                                                                         
                         +           {|NT (P2 )(σ ′ , ρ′ )|(σ ′ , ρ′ ) ∈ L1 (σ, ρ)|} + NT (P1 )(σ, ρ)
                                                                                                   (A.13)

where                                  X
                      µ(σ ′ , ρ′ ) =       {|tr (σ ′′ (C)ρ′′ |(σ ′′ , ρ′′ ) ∈ L2 (σ ′ , ρ′ )|} .


                                                        53
It follows from (A.10) that
 X
     {|µ(σ ′ , ρ′ )|(σ ′ , ρ′ ) ∈ L1 (σ, ρ)|}
                                                                              
    X                                               [                         
 =        |tr (σ ′′ (C)ρ′′ |(σ ′′ , ρ′′ ) ∈                     L2 (σ ′ , ρ′ )|
                                                                              
                                            (σ ′ ,ρ′ )∈L1 (σ,ρ)
    X
 ≤      {|tr (σ ′′ (C)ρ′′ |(σ ′′ , ρ′′ ) ∈ JP1 ; P2 K(σ, ρ), σ ′′ |= θ and σ ′′ is well-define|} .
                                                                                          (A.14)
On the other hand, by the definition of nontermination probability NT (P )
and (A.9) we have:
 X
     {|NT (P2 )(σ ′ , ρ′ )|(σ ′ , ρ′ ) ∈ L1 (σ, ρ)|} + NT (P1 )(σ, ρ)
   X
 ≤      {|NT (P2 )(σ ′ , ρ′ )|(σ ′ , ρ′ ) ∈ JP1 K(σ, ρ)|} + NT (P1 )(σ, ρ)
   Xn                X                                                                   o
                ′                     ′′   ′′ ′′           ′ ′       ′ ′
 =        |tr (ρ ) −       {|tr (ρ )|(σ , ρ ) ∈ JP2 K(σ , ρ )|} |(σ , ρ ) ∈ JP1 K(σ, ρ)|
                                                        + NT (P1 )(σ, ρ)
     X
 =      {|tr (ρ′ )|(σ ′ , ρ′ ) ∈ JP1 K(σ, ρ)|}
                                                                                   
         X                                             [                           
      −          |tr (ρ′′ )|(σ ′′ , ρ′′ ) ∈                        JP2 K(σ ′ , ρ′ )| + NT (P1 )(σ, ρ)
                                                                                   
                                              (σ ′ ,ρ′ )∈JP1 K(σ,ρ)
   X
 =      {|tr (ρ′ )|(σ ′ , ρ′ ) ∈ JP1 K(σ, ρ)|}
                              X
                           −        {|tr (ρ′′ )|(σ ′′ , ρ′′ ) ∈ JP1 ; P2 K(σ, ρ)|} + NT (P1 )(σ, ρ)
   X                                                                            
                  ′       ′ ′
 =       {|tr (ρ )|(σ , ρ ) ∈ JP1 K(σ, ρ)|} + NT (P1 )(σ, ρ)
                                             X
                                         −           {|tr (ρ′′ )|(σ ′′ , ρ′′ ) ∈ JP1 ; P2 K(σ, ρ)|}
             X
 = tr (ρ) −         {|tr (ρ′′ )|(σ ′′ , ρ′′ ) ∈ JP1 ; P2 K(σ, ρ)|}
 = NT (P1 ; P2 )(σ, ρ).
                                                                                             (A.15)
Finally, plugging (A.14) and (A.15) into (A.13), we obtain:
             X
tr (σ(A)ρ) ≤     {|tr (σ ′′ (C)ρ′′ |(σ ′′ , ρ′′ ) ∈ JP1 ; P2 K(σ, ρ), σ ′′ |= θ and σ ′′ is well-defined|}
                                                        + NT (P1 ; P2 )(σ, ρ).

                                                 54
Therefore, it holds that |=par {φ, A} P1 ; P2 {θ, C}.
    (Rule-Cond): We prove that |=par {φ ∧ b, A} P1 {ψ, B} and |=par {φ ∧
¬b, A} P0 {ψ, B} imply
                    |=par {φ, A} if b then P1 else P0 {ψ, B}.
For simplicity of the presentation, let us write “if ...” for “if b then P1 else P0 ”.
Then for any input state σ, ρ) ∈ Ω, by transition rule (Cond), we obtain:
                                     (
                                      JP1 K(σ, ρ) if σ |= b,
                    Jif ...K(σ, ρ) =                                          (A.16)
                                      JP0 K(σ, ρ) if σ |= ¬b.
    Now assume that σ |= φ and σ(A) is well-defined. We consider the
following two cases:
    Case 1 . σ |= b. Then it holds that σ |= φ ∧ b. By the assumption
|=par {φ ∧ b, A} P1 {ψ, B}, we have:
              X
tr (σ(A)ρ) ≤     {|tr (σ ′ (A)ρ′ )|(σ ′ , ρ′ ) ∈ JP1 K(σ, ρ), σ ′ |= ψ and σ ′ (B) is well-defined|}
                                             + NP (P1 )(σ, ρ)
    X
≤       {|tr (σ ′ (A)ρ′ )|(σ ′ , ρ′ ) ∈ Jif ...K(σ, ρ), σ ′ |= ψ and σ ′ (B) is well-defined|}
                                             + NT (if ...)(σ, ρ).

    Case 2 . σ |= ¬b. Similarly, we can prove
             X
tr (σ(A)ρ) ≤     {|tr (σ ′ (A)ρ′ )|(σ ′ , ρ′ ) ∈ Jif ...K(σ, ρ), σ ′ |= ψ and σ ′ (B) is well-defined|}
                                             + NT (if ...)(σ, ρ).
    Finally, by combining the above two cases, we assert that
                    |=par {φ, A} if b then P1 else P0 {ψ, B}.

    (Rule-Loop-par): Let us first introduce several notations. For any n ≥
0, we set:
Pn (σ, ρ) =
 n                                                                                                      o
                                 P     P
   |(σ , ρ )|(σ, ρ) = (σ0 , ρ0 ) ⇒ ... ⇒ (σk , ρk ) = (σ , ρ ), k ≤ n, σi |= b (0 ≤ i < k) and σk |= ¬b| ,
      ′ ′                                               ′ ′


Qn (σ, ρ) =
     n                                                                                     o
                                     P     P
       |(σ , ρ )|(σ, ρ) = (σ0 , ρ0 ) ⇒ ... ⇒ (σn , ρn ) = (σ , ρ ) and σi |= b (0 ≤ i ≤ n)| .
          ′ ′                                               ′ ′



                                             55
Also, to simplify the presentation, we write “while” for “while b d P ” and
“:WD” for “is well-defined”. Then {Pn } is an increasing sequence, and Propo-
sition 3.1(8) can be rewritten as
                                                   ∞
                                                   [
                            JwhileK(σ, ρ) =              Pn (σ, ρ).                    (A.17)
                                                   n=0

    Now we assume:
                              |=par {φ ∧ b, A} P {φ, A}                                (A.18)
and prove:
                          |=par {φ, A} while {φ ∧ ¬b, A},                              (A.19)
that is, for any input state (σ, ρ) ∈ Ω, if σ |= φ and σ(A) : W D, then
              X
tr (σ(A)ρ) ≤      {|tr (σ ′ (A)ρ′ )|(σ ′ , ρ′ ) ∈ JwhileK(σ, ρ), σ ′ |= φ ∧ ¬b and σ ′ (A) : W D|}
                                                                      + NT (while)(σ, ρ)
                                                                                    (A.20)

where
                                         X
      NT (while)(σ, ρ) = tr (ρ) −             {|tr (ρ′ )|(σ ′ , ρ′ ) ∈ JwhileK(σ, ρ)|} .

In fact, whenever σ |= ¬b, then σ |= φ ∧ ¬b, (σ, ρ) ∈ P0 (σ, ρ), and
             X
tr (σ(A)ρ) ≤    {|tr (σ ′ (A)ρ′ )|(σ ′ , ρ′ ) ∈ P0 (σ, ρ), σ ′ |= φ ∧ ¬b and σ ′ (A) : W D|} .

Thus, (A.20) is correct. Otherwise, that is, σ |= b, then we prove:
  Claim: For any integer n ≥ 1, it holds that

                     tr (σ(A)ρ) ≤ Λn + ∆n + tr (ρ) − Γn − Ωn                           (A.21)

where:
           X
    Λn =       {|tr (σ ′ (A)ρ′ )|(σ ′ , ρ′ ) ∈ Pn (σ, ρ), σ ′ |= φ and σ ′ (A) : W D|} ,
           X
    ∆n =       {|tr (σ ′ (A)ρ′ )|(σ ′ , ρ′ ) ∈ Qn (σ, ρ), σ ′ |= φ and σ ′ (A) : W D|} ,
           X
    Γn =       {|tr (ρ′ )|(σ ′ , ρ′ ) ∈ Pn (σ, ρ)|} ,
           X
    Ωn =       {|tr (ρ′ )|(σ ′ , ρ′ ) ∈ Qn (σ, ρ)|} .

                                              56
   We proceed by induction on n. For the case of n = 1, note that σ |= φ∧b.
Then by the assumption (A.18) we have:
            X
tr(σ(A)ρ) ≤    {|tr (σ ′ (A)ρ′ )|(σ ′ , ρ′ ) ∈ JP K(σ, ρ), σ ′ |= φ and σ ′ (A) : W D|}
                                          + NT (P )(σ, ρ)
    X
=       {|tr (σ ′ (A)ρ′ )|(σ ′ , ρ′ ) ∈ JP K(σ, ρ), σ ′ |= φ and σ ′ (A) : W D|}
                                       X
                        + tr (ρ) −         {|tr (ρ′ )|(σ ′ , ρ′ ) ∈ JP K(σ, ρ)|}
    X
=      {|tr (σ ′ (A)ρ′ )|(σ ′ , ρ′ ) ∈ P1 (σ, ρ), σ ′ |= φ and σ ′ (A) : W D|}
        X
      +      {|tr (σ ′ (A)ρ′ )|(σ ′ , ρ′ ) ∈ Q1 (σ, ρ), σ ′ |= φ and σ ′ (A) : W D|}
                    X                                            X
       + tr (ρ) −        {|tr (ρ′ )|(σ ′ , ρ′ ) ∈ P1 (σ, ρ)|} −     {|tr (ρ′ )|(σ ′ , ρ′ ) ∈ Q1 (σ, ρ)|}
= Λ1 + ∆1 + tr (ρ) − Γ1 − Ω1
                                                                                              (A.22)

because JP K(σ, ρ) = P1 (σ, ρ) ∪ Q1 (σ, ρ) and P1 (σ, ρ) ∩ Q1 (σ, ρ) = ∅. So,
(A.21) is true for n = 1.
    Now assume (A.21) is true for n, and we prove it is also true for n + 1.
We first note that for any (σ ′ , ρ′ ) ∈ Qn (σ, ρ) with σ ′ |= φ and σ ′ (A) : W D,
it holds that σ ′ |= φ ∧ b. Then by by the assumption (A.18) we obtain:
                  X
tr (σ ′ (A)ρ′ ) ≤   {|tr (σ ′′ (A)ρ′′ )|(σ ′′ , ρ′′ ) ∈ JP K(σ ′ , ρ′ ), σ ′′ |= φ and σ ′′ (A) : W D|}
                                          + NT (P )(σ ′ , ρ′ )
    X
=       {|tr (σ ′′ (A)ρ′′ )|(σ ′′ , ρ′′ ) ∈ JP K(σ ′ , ρ′ ), σ ′′ |= φ and σ ′′ (A) : W D|}
                                          + NT (P )(σ ′ , ρ′ )                                         .
    X
=      {|tr (σ ′′ (A)ρ′′ )|(σ ′′ , ρ′′ ) ∈ P1 (σ ′ , ρ′ ), σ ′′ |= φ and σ ′′ (A) : W D|}
        X
      +      {|tr (σ ′′ (A)ρ′′ )|(σ ′′ , ρ′′ ) ∈ Q1 (σ ′ , ρ′ ), σ ′′ |= φ and σ ′′ (A) : W D|}
                                          + NT (P )(σ ′ , ρ′ )
                                                                                              (A.23)

Taking the summation over (σ ′ , ρ′ ) ∈ Qn (σ, ρ) with σ ′ |= φ and σ ′ (A) : W D,




                                                57
we obtain:
                      X
∆n ≤ λn + δn +             {|NT (P )(σ ′ , ρ′ )|(σ ′ , ρ′ ) ∈ Qn (σ, ρ), σ ′ |= φ and σ ′ (A) : W D|}
                      X
     ≤ λn + δn +           {|NT (P )(σ ′ , ρ′ )|(σ ′ , ρ′ ) ∈ Qn (σ, ρ)|}
                                                                                               (A.24)
where:
λn =
Xn X                                                                                         o
     | {|tr (σ (A)ρ )|(σ , ρ ) ∈ P1 (σ , ρ ), σ |= φ and σ (A) : W D|} |(σ , ρ ) ∈ Qn (σ, ρ)| ,
              ′′   ′′   ′′ ′′         ′ ′      ′′         ′′              ′ ′


δn =
Xn X                                                                                         o
     | {|tr (σ (A)ρ )|(σ , ρ ) ∈ Q1 (σ , ρ ), σ |= φ and σ (A) : W D|} |(σ , ρ ) ∈ Qn (σ, ρ)| .
              ′′   ′′   ′′ ′′         ′ ′      ′′         ′′              ′ ′


Plugging (A.24) into (A.21) yields:
                              X                                                
tr (σ(A)ρ) ≤ Λn + λn + δn +       {|NT (P )(σ ′ , ρ′ )|(σ ′ , ρ′ ) ∈ Qn (σ, ρ)|} + tr (ρ) − Γn − Ωn
                              X                                                           
 = (Λn + λn ) + δn + tr (ρ) +    {|NT (P )(σ ′ , ρ′ )|(σ ′ , ρ′ ) ∈ Qn (σ, ρ)|} − Γn − Ωn .
                                                                                               (A.25)
It is easy to see that
            X
Λn + λ n ≤      {|tr (σ ′ (A)ρ′ )|(σ ′ , ρ′ ) ∈ Pn+1 (σ, ρ), σ ′ |= φ and σ ′ (A) : W D|} = Λn+1
                                                                                     (A.26)
and
       X
δn =        {|tr (σ ′′ (A)ρ′′ )|(σ ′′ , ρ′′ ) ∈ Qn+1 (σ, ρ), σ ′′ |= φ and σ ′′ (A) : W D|} = ∆n+1 .
                                                                                         (A.27)
By the definition of NT (P ), we have:
 X
     {|NT (P )(σ ′ , ρ′ )|(σ ′ , ρ′ ) ∈ Qn (σ, ρ)|}
    Xn                 X                                                                              o
 =        |tr (ρ′ ) −         {|tr (ρ′′ )|(σ ′′ , ρ′′ ) ∈ JP K(σ ′ , ρ′ )|} |(σ ′ , ρ′ ) ∈ Qn (σ, ρ)|
    X
 =      {|tr (ρ′ )|(σ ′ , ρ′ ) ∈ Qn (σ, ρ)|}
                     X
                   −         {|tr (ρ′′ )|(σ ′′ , ρ′′ ) ∈ JP K(σ ′ , ρ′ ) and (σ ′ , ρ′ ) ∈ Qn (σ, ρ)|}
          X
 = Ωn −        {|tr (ρ′′ )|(σ ′′ , ρ′′ ) ∈ JP K(σ ′ , ρ′ ) and (σ ′ , ρ′ ) ∈ Qn (σ, ρ)|}


                                                  58
Moreover, we have:
 X
     {|tr (ρ′′ )|(σ ′′ , ρ′′ ) ∈ JP K(σ ′ , ρ′ ) and (σ ′ , ρ′ ) ∈ Qn (σ, ρ)|}
    X
 =      {|tr (ρ′′ )|(σ ′′ , ρ′′ ) ∈ P1 (σ ′ , ρ′ ) and (σ ′ , ρ′ ) ∈ Qn (σ, ρ)|}
                        X
                   +           {|tr (ρ′′ )|(σ ′′ , ρ′′ ) ∈ Q1 (σ ′ , ρ′ ) and (σ ′ , ρ′ ) ∈ Qn (σ, ρ)|}
    X
 =      {|tr (ρ′′ )|(σ ′′ , ρ′′ ) ∈ P1 (σ ′ , ρ′ ) and (σ ′ , ρ′ ) ∈ Qn (σ, ρ)|} + Ωn+1 .
Then it follows that
X
   {|NT (P )(σ ′ , ρ′ )|(σ ′ , ρ′ ) ∈ Qn (σ, ρ)|} − Γn − Ωn
    X                                                                     
=−         {|tr (ρ )|(σ , ρ ) ∈ P1 (σ , ρ ) and (σ , ρ ) ∈ Qn (σ, ρ)|} + Γn − Ωn+1
                  ′′     ′′ ′′            ′ ′          ′ ′


= −Γn+1 − Ωn+1 .
                                                                                                (A.28)
Combining (A.25), (A.26), (A.27) and (A.28), we obtain:
                  tr (σ(A)ρ) ≤ Λn+1 + ∆n+1 + tr (ρ) − Γn+1 − Ωn+1 .
Therefore, we see from (A.25) that (A.21) is true for n + 1. Thus, the proof
of (A.21) is completed.
    Now we prove the following two facts:
    Fact 1 : By definition, we know that σ ′ |= ¬b whenever (σ ′ , ρ′ ) ∈ Pn (σ, ρ).
Then it follows from (A.17) that
           X
 lim Λn =      {|tr (σ ′ (A)ρ′ )|(σ ′ , ρ′ ) ∈ JwhileK(σ, ρ), σ ′ |= φ ∧ ¬b and σ ′ (A) : W D|} .
n→∞
                                                                                                (A.29)

   Fact 2 : Note that σ ′ (A) ≤ I (the identity operator). Then it follows
that tr (σ ′ (A)ρ) ≤ tr (ρ). Consequently, we have:
      X                                                   X
∆n ≤        {|tr (σ ′ (A)ρ′ )|(σ ′ , ρ′ ) ∈ Qn (σ, ρ)|} ≤   {|tr (ρ′ )|(σ ′ , ρ′ ) ∈ Qn (σ, ρ)|} ≤ Ωn
and
                                     ∆n − Γn − Ωn ≤ −Γn .
Then it holds that
                                                     X
 lim (∆n − Γn − Ωn ) ≤ − lim Γn = −                       {|tr (ρ′ )|(σ ′ , ρ′ ) ∈ JwhileK(σ, ρ)|} .
n→∞                                n→∞
                                                                                                (A.30)

                                                   59
    Finally, we take the limit of n → ∞ in (A.21) and invoke (A.29) and
(A.30). Then the conclusion (A.20) is achieved, and we complete the proof
of the soundness of (Rule-Loop-par).
    (Rule-Conseq): We assume that (φ′ , A′ ) |= (φ, A), (ψ, B) |= (ψ ′ , B ′ )
and
                           |=par {φ, A} P {ψ, B}                   (A.31)
and prove
                                  |=par {φ′ , A′ } P {ψ ′ , B ′ }.                          (A.32)
For any input state (σ, ρ) ∈ Ω, if σ |= φ′ and σ(A′ ) is well-defined, then
by the assumption (φ′ , A′ ) |= (φ, A) and Definitions 4.5 and 4.8, we have
σ |= φ, σ(A) is well-defined, and σ(A′ ) ≤ σ(A). Consequently, it follows
from assumptions (A.31) and (ψ, B) |= (ψ ′ , B ′ ) that

tr (σ(A′ )ρ) ≤ tr (σ(A)ρ)
    X
 ≤     {|tr (σ ′′ (B)ρ′′ )|(σ ′′ , ρ′′ ) ∈ JP K(σ, ρ), σ ′′ |= ψ and σ ′′ (B) is well-defined|}
    X
 ≤     {|tr (σ ′′ (B ′ )ρ′′ )|(σ ′′ , ρ′′ ) ∈ JP K(σ, ρ), σ ′′ |= ψ ′ and σ ′′ (B ′ ) is well-defined|} .

Thus, (A.32) is proved.
  (Rule-Accum1): We assume that q ∩ qv (P ) = ∅ and

                            |=par {φ, Ai } P {ψi , B} for every i,                          (A.33)
                             |= (∀i1 , i2 )(i1 ̸= i2 → ¬(ψi1 ∧ ψi2 )).                      (A.34)

    Let us write “:WD” for “is well-defined”. Then for any input state (σ, ρ) ∈
Ω, whenever σ |= φ and σ(Ai ) is well-defined, then:
               X
tr (σ(Ai )ρ) ≤     {|tr (σ ′ (B)ρ′ )|(σ ′ , ρ′ ) ∈ JP K(σ, ρ), σ ′ |= ψi and σ ′ (B) : W D}
                             + NT (P )(σ, ρ).
                                                                                            (A.35)

We want to prove
                                                      (                        )
                                                       _
                                                                                            (A.36)
                        
                 |=par φ, F (t)[q]({Ai })         P           ψi , F (t)[q](B) .
                                                          i




                                                60
For any input state (σ, ρ) ∈ Ω, if σ |= φ and σ F (t)[q]({Ai }) is well-defined,
                                                                      

then for all i, σ(Ai ) is well-defined, and σ |= Dist(q). Assume that the Kraus
operator symbol F is interpreted as F = {Fi (a)}. Then we have:
                                   "                                             ! #
                                      X
                                          Fi (σ(t))σ(q) · σ(Ai ) · Fi† (σ(t))σ(q) ρ
                         
  tr σ F (t)[q]({Ai }) ρ = tr
                                                i
       X          h                                          i
   =         tr        Fi (σ(t))σ(q) · σ(Ai ) · Fi† (σ(t)σ(q) ρ
         i
       X       h                                         i
   =         tr σ(Ai ) Fi† (σ(t))σ(q) · ρ · Fi (σ(t))σ(q)
         i
       X
   ≤         Λi
         i
                                                                                   (A.37)
where:
Λi =
Xn                                                                                                          o
     |tr (σ ′ (B)ρ′ )|(σ ′ , ρ′ ) ∈ JP K σ, Fi† (σ(t))σ(q) · ρ · Fi (σ(t))σ(q) , σ ′ |= ψi and σ ′ (B) : W D|
                                                   
                  †
+ NT (P ) σ, Fi (σ(t))σ(q) · ρ · Fi (σ(t))σ(q) .
Note that the last inequality of (A.37) comes from the assumption (A.35).
   Now with the assumption that q ∩ qv (P ) = ∅ and [var (t) ∪ cv (q)] ∩
change(P ) = ∅, we can prove:
                                             
   JP K σ, Fi† (σ(t))σ(q) · ρ · Fi (σ(t))σ(q)
                n                                                                 o
            = | σ ′ , Fi† (σ(t))σ(q) · ρ′ · Fi (σ(t))σ(q) |(σ ′ , ρ′ ) ∈ JP K(σ, ρ)| .
                                                                                   (A.38)
by induction on the structure of P .
   (1) By the definition of NT (·) we obtain:
        X                                                X
            NT (P ) σ, Fi† (σ(t))σ(q) · ρ · Fi (σ(t))σ(q) =  ∆i                    (A.39)
             i                                                      i

where
                                           
 ∆i = tr Fi† (σ(t))σ(q) · ρ · Fi (σ(t))σ(q)
          Xn                                
                                               †
                                                                               o
                       ′′     ′ ′′
        −        |tr (ρ )|(σ , ρ ) ∈ JP K σ, Fi (σ(t))σ(q) · ρ · Fi (σ(t))σ(q) | .


                                                    61
Using (A.38) we have:
                                           
            †
  ∆i =tr Fi (σ(t))σ(q) · ρ · Fi (σ(t))σ(q)
         Xn  †                                                                         o
       −       |tr Fi (σ(t))σ(q) · ρ′ · Fi (σ(t))σ(q) |(σ ′ , ρ′ ) ∈ JP K (σ, ρ) |
         h                     X                                                         i
     =tr Fi† (σ(t))σ(q) · ρ −        {|ρ′ |(σ ′ , ρ′ ) ∈ JP K (σ, ρ) |} · Fi (σ(t))σ(q)
         h                                       X                                      i
     =tr Fi (σ(t))σ(q) · Fi† (σ(t)σ(q) · ρ −           {|ρ′ |(σ ′ , ρ′ ) ∈ JP K (σ, ρ) |} .
                                                                                                     (A.40)
It follows from condition (12) that
                      X
                          Fi (σ(t))σ(q) · Fi† (σ(t)σ(q) = I.
                                        i

Then plugging (A.40) into (A.39) yields:
X                                               
   NT (P ) σ, Fi† (σ(t))σ(q) · ρ · Fi (σ(t))σ(q)
  i
      X            h                                             X                                 i
=             tr       Fi (σ(t))σ(q) · Fi† (σ(t)σ(q) ·       ρ−          ′     ′   ′
                                                                      {|ρ |(σ , ρ ) ∈ JP K (σ, ρ) |}
      i
          "                                              !                                                     #
                   X                                                 X                                    
= tr                     Fi (σ(t))σ(q) · Fi† (σ(t)σ(q)       · ρ−               ′   ′ ′
                                                                             {|ρ |(σ , ρ ) ∈ JP K (σ, ρ) |}
                   i
                      X                                  
                                ′   ′   ′
= tr ρ −                    {|ρ |(σ , ρ ) ∈ JP K (σ, ρ) |}
= NT (P )(σ, ρ).
                                                                                                     (A.41)
  (2) Using (A.38) we obtain:
 △
   XX
µ=
      i
n                                                                                                          o
 |tr (σ ′ (B)ρ′′ )|(σ ′ , ρ′′ ) ∈ JP K σ, Fi† (σ(t))σ(q) · ρ · Fi (σ(t))σ(q) , σ ′ |= ψi and σ ′ (Bi ) : W D|
   XX
=
n ih                                           i                                                      o
 |tr σ ′ (B) Fi† (σ(t))σ(q) · ρ′ · Fi (σ(t))σ(q) |(σ ′ , ρ′ ) ∈ JP K(σ, ρ), σ ′ |= ψi and σ ′ (B) : W D| .
                                                                                                     (A.42)

                                                         62
Let ψ =       i ψi . Then using (A.42), the assumption (A.34), the assumptions:
          W

                                   σ |= T (t) ∝ F ′ (t),

                       σ |= (∀i1 , i2 ) (i1 ̸= i2 → ¬(ψi1 ∧ ψi2 )) ,
and the commutativity tr (AB) = tr (BA) for trace, we have:
    XX
µ≤
    i ′
 |tr σ (B) F ′† (σ(t))σ(q) · ρ′ · F ′ (σ(t))σ(q) |(σ ′ , ρ′ ) ∈ JP K(σ, ρ), σ ′ |= ψi and σ ′ (B) : W D|
                                               
   X
≤
 |tr σ (B) F ′† (σ(t))σ(q) · ρ′ · F ′ (σ(t))σ(q) |(σ ′ , ρ′ ) ∈ JP K(σ, ρ), σ ′ |= ψ and σ ′ (B) : W D|
  ′                                           
   X
=
n h                             ′†
                                               i                                                        o
 |tr F (σ(t))σ(q) · σ (B) · F (σ(t))σ(q) ρ |(σ , ρ ) ∈ JP K(σ, ρ), σ |= ψ and σ (B) : W D|
           ′            ′                         ′     ′ ′                     ′             ′

   X 
         |tr σ F ′ (t)[q](B) ρ′ |(σ ′ , ρ′ ) ∈ JP K(σ, ρ), σ ′ |= ψ and σ ′ (B) : W D| .
                             
=
                                                                                   (A.43)

    Finally, by plugging (A.41) and (A.43) into (A.37), it is derived that
                    
tr σ F (t)[q]({Ai }) ρ
   X 
        |tr σ F ′ (t)[q](B) ρ′ |(σ ′ , ρ′ ) ∈ JP K(σ, ρ), σ ′ |= ψ and σ ′ (B) : W D| + NT (P )(σ, ρ).
                            
 ≤

Thus, (A.36) is proved.
  (Rule-Accum2): Let us use the same notations as in (Rule-Accum2).
We assume that q ∩ qv (P ) = ∅ and for every i,

                               |=par {φ, Ai } P {ψ, Bi };                           (A.44)

that is, for any input state (σ, ρ) ∈ Ω, whenever σ |= φ and σ(Ai ) is well-
defined, then:
               X
tr (σ(Ai )ρ) ≤    {|tr (σ ′ (Bi )ρ′ )|(σ ′ , ρ′ ) ∈ JP K(σ, ρ), σ ′ |= ψ and σ ′ (Bi ) : W D}
                          + NT (P )(σ, ρ).
                                                                                    (A.45)


                                            63
We want to prove

                                                                                 (A.46)
                                                       
                 |=par φ, F (t)[q]({Ai })        ψ, F (t)[q]({Bi }) .
                                                    P

For any input state (σ, ρ) ∈ Ω, if σ(φ) and σ F (t)[q]({Ai }) is well-defined,
                                                                     

then for all i, σ(Ai ) is well-defined, and σ |= Dist(q). Assume that the Kraus
operator symbol F is interpreted as F = {Fi (a)}. Then by the assumption
(A.45) we can derive:
                                   "                                             ! #
                                      X
                                          Fi (σ(t))σ(q) · σ(Ai ) · Fi† (σ(t))σ(q) ρ
                         
  tr σ F (t)[q]({Ai }) ρ = tr
                                           i
       X
   ≤        Γi
        i
                                                                                      (A.47)

in a way similar to (A.37), where:
       X
Γi =
 n                                                                                                         o
  |tr (σ ′ (Bi )ρ′ )|(σ ′ , ρ′ ) ∈ JP K σ, Fi† (σ(t))σ(q) · ρ · Fi (σ(t))σ(q) , σ ′ |= ψ and σ ′ (Bi ) : W D|
                                                     
                      †
 + NT (P ) σ, Fi (σ(t))σ(q) · ρ · Fi (σ(t))σ(q) .




                                               64
 Now using (A.38) we obtain:
XX

ni                                                                                                          o
 |tr (σ ′ (Bi )ρ′′ )|(σ ′ , ρ′′ ) ∈ JP K σ, Fi† (σ(t))σ(q) · ρ · Fi (σ(t))σ(q) , σ ′ |= ψ and σ ′ (Bi ) : W D|
   XX
=
n ih                                            i                                                        o
                 †
 |tr σ (Bi ) Fi (σ(t))σ(q) · ρ · Fi (σ(t))σ(q) |(σ , ρ ) ∈ JP K(σ, ρ), σ |= ψ and σ (Bi ) : W D|
      ′                        ′                       ′ ′                    ′             ′

   X
=
(                                                                                                              )
   X h                                               i
 |    tr σ ′ (Bi ) Fi† (σ(t))σ(q) · ρ′ · Fi (σ(t))σ(q) |(σ ′ , ρ′ ) ∈ JP K(σ, ρ), σ ′ |= ψ and σ ′ (Bi ) : W D|
      i
      X
=
(                                                                                                                     )
      X        h                                          i
  |       tr        Fi (σ(t))σ(q) · σ ′ (Bi )Fi† (σ(t)σ(q) ρ′ |(σ ′ , ρ′ ) ∈ JP K(σ, ρ), σ ′ |= ψ and σ ′ (Bi ) : W D|
      i
      X
=
(     "                                           #                                                        )
       X                                      
  |tr    Fi (σ(t))σ(q) · σ ′ (Bi )Fi† (σ(t)σ(q) ρ′ |(σ ′ , ρ′ ) ∈ JP K(σ, ρ), σ ′ |= ψ and σ ′ (Bi ) : W D|
           i
      X
           |tr σ F (t)[q]({Bi }) ρ′ |(σ ′ , ρ′ ) ∈ JP K(σ, ρ), σ ′ |= ψ and σ ′ (Bi ) : W D| .
                                
=
                                                                                  (A.48)

     Finally, by plugging (A.41) and (A.48) into (A.47), it is derived that
                      X
tr σ F (t)[q]({Ai }) ρ ≤
  |tr σ F (t)[q]({Bi }) ρ′ |(σ ′ , ρ′ ) ∈ JP K(σ, ρ), σ ′ |= ψ and σ ′ (Bi ) : W D| . + NT (P )(σ, ρ).
                       


Thus, (A.46) is proved.

Appendix A.3.2. The Case of Total Correctness
    Now we turn to prove the soundness of proof system QHL+ tot . The validity
of all axioms and rules except (Rule-Loop-tot) in the sense of total correct-
ness can be proved in a way similar to (but easier than) the case of partial


                                                  65
correctness. So, we only prove the validity of (Rule-Loop-tot) here. We use
the same notation as in the validity proof of (Rule-Loop-par). Assume

                        |=tot {φ ∧ b, A} P {φ, A},                                      (A.49)
                        |=tot {φ ∧ b ∧ t = z, I} P {t < z, I},                          (A.50)
                        |= φ → t ≥ 0                                                    (A.51)

where z is an integer variable with z ∈
                                      / free(φ) ∪ var (b) ∪ var (t) ∪ cv (P ), and
I stands for the identity quantum predicate. We want to prove:

                           |=tot {φ, A} while {φ ∧ ¬b, A};                              (A.52)

that is, for any input state (σ, ρ) ∈ Ω, if σ |= φ and σ(A) is well-defined,
then
              X
tr (σ(A)ρ) ≤      {|tr (σ ′ (A)ρ′ ))|(σ ′ , ρ′ ) ∈ JwhileK(σ, ρ), σ ′ |= φ ∧ ¬b and σ ′ (A) : W D|} .
                                                                                     (A.53)
    First, by the assumption (A.49), we are able to prove the following claim
in a way similar to the proof of claim (A.21):
    Claim 1 : For any integer n ≥ 1,
              X
tr (σ(A)ρ) ≤      {|tr (σ ′ (A)ρ′ )|(σ ′ , ρ′ ) ∈ Pn (σ, ρ), σ ′ |= φ and σ ′ (A) : W D|} + ∆∗n
                                                                                     (A.54)

where:
              X
      ∆∗n =       {|tr (σ ′ (A)ρ′ )) | (σ ′ , ρ′ ) ∈ Q∗n (σ, ρ) and σ ′ (A) : W D|} ,
                                                                                      (A.55)
            n                                                                                                o
                                                P     P
Q∗n (σ, ρ) = |(σ ′ , ρ′ ) | (σ, ρ) = (σ0 , ρ0 ) ⇒ ... ⇒ (σn , ρn ) = (σ ′ , ρ′ ) and σi |= φ ∧ b (0 ≤ i ≤ n)| .
                                                                                        (A.56)

Let us take the limit of n → ∞ in the right-hand side of (A.54). Then it
follows from (A.29) that
             X
tr (σ(A)ρ) ≤    {|tr (σ ′ (A)ρ′ )|(σ ′ , ρ′ ) ∈ JwhileK(σ, ρ), σ ′ |= φ ∧ ¬b and σ ′ (A) : W D|}
                          + lim ∆∗n
                             n→∞
                                                                                        (A.57)

                                             66
Thus, it suffices to show that limn→∞ ∆∗n = 0. We do this by refutation.
Suppose that limn→∞ ∆∗n > 0. We derive a contradiction in four steps:
   Step 1 : If tr (σ(A)ρ) = 0, then (A.53) is obviously true. So, we now
assume tr (σ(A)ρ) > 0 and use the assumption (A.50) to prove the following:
                        P
   Claim 2 : If (σ, ρ) ⇒ (σ ′ , ρ′ ) and ρ′ ̸= 0, then σ ′ (t) < σ(t).
   To prove this claim, by the assumptions, we have σ |= φ ∧ b and σ(I) :
W D. We can introduce a fresh integer variable z such that
                       z∈
                        / free(φ) ∪ var (b) ∪ var (t) ∪ cv (P ),                    (A.58)
and set σ(z) = σ(t). Thus, it holds that σ |= φ∧b∧t = z. By the assumption
(A.50), we obtain:
    0 < tr (ρ) = tr (σ(I)ρ)
                 Xn                            P
                                                                               o
               ≤       |tr (σ ′ (I)ρ′ )|(σ, ρ) ⇒ (σ ′ , ρ′ ) and σ ′ |= t < z|      (A.59)
                 Xn                      P
                                                                         o
               =       |tr (ρ′ )|(σ, ρ) ⇒ (σ ′ , ρ′ ) and σ ′ |= t < z| .

For any (σ ′ , ρ′ ) in the right-hand side of (A.59), by the condition (A.58) we
know that the program P does not change the value of z, and thus σ ′ (z) =
σ(z). On the other hand, σ ′ |= t < z. Then σ ′ (t) < σ ′ (z) = σ(z) = σ(t).
Therefore, we obtain:
                    Xn                   P
                                                                      o
       tr (ρ) ≤          |tr (ρ )|(σ, ρ) ⇒ (σ , ρ ) and σ (t) < σ(t)|
                               ′             ′ ′         ′
                                                                          (A.60)

from (A.59).
   It follows from Proposition 3.2 that
                   Xn                   P
                                                      o
                       |tr (ρ′ )|(σ, ρ) ⇒ (σ ′ , ρ′ )| ≤ tr (ρ).                    (A.61)

By combining (A.60) and (A.61) we have:
Xn                       P
                                       o Xn
                                                              P
                                                                                               o
        |tr (ρ′ )|(σ, ρ) ⇒ (σ ′ , ρ′ )| ≤    |tr (ρ′ )|(σ, ρ) ⇒ (σ ′ , ρ′ ) and σ ′ (t) < σ(t)| .
                                                                                       (A.62)
                                                                                P
If Claim 2 is not true; that is, there exists (σ0 , ρ0 ) such that (σ, ρ) ⇒ (σ0′ , ρ′0 ),
                                                      ′  ′

tr (ρ′0 ) > 0 and σ0′ (t) ≥ σ(t), then it holds that
                                          Xn                  P
                                                                           o
         The right-side of (A.62) ≤         |tr (ρ′ )|(σ, ρ) ⇒ (σ ′ , ρ′ )| − tr (ρ′ )
                                    < the left-side of (A.62),

                                            67
and inequality (A.62) is violated, a contradiction. Thus, Claim 2 is proved.
   Step 2 : We construct a tree using Claim 2. The root of the tree is
labelled by (σ0 , ρ0 ) = (σ, ρ). Let

                R1 = {|(σ1 , ρ1 )|(σ1 , ρ1 ) ∈ Q∗1 (σ, ρ) and ρ1 ̸= 0|} .

    From the assumption limn→∞ ∆∗n > 0, we have:
    Claim 3 : There exists an integer n0 ≥ 0 such that ∆∗n > 0 for all n ≥ n0 .
    Then from Claim 3 and the defining equations (A.55) and (A.56) of ∆∗n
and Q∗n (σ, ρ), it is easy to see that R1 ̸= ∅. We expand the tree by letting
each (σ1 , ρ1 ) ∈ R1 with σ1 |= φ ∧ b as an immediate child of (σ0 , ρ0 ). It
follows from Claim 2 that σ1 (t) < σ0 (t).
    Next, for each newly added node (σ1 , ρ1 ), we repeat the above process and
generate its immediate childs (σ2 , ρ2 ). In this way, we expand the tree step
by step, and the tree can be constructed as desired. We need to remember
that in this tree:
  (i) for any node (σi , ρi ), it holds that σn |= φ ∧ b; and
 (ii) if (σi+1 , ρi+1 ) is a child of (σi , ρi ), then σi+1 (t) < σi (t).
   Step 3 : For any n ≥ n0 , using Claim 3 and the defining equations (A.55)
and (A.56) of ∆∗n and Q∗n (σ, ρ), we can assert that there exists (σ ′ , ρ′ ) ∈
Qn (σ, ρ) such that σ ′ |= φ, σ ′ (A) : W D and tr (σ ′ (A)ρ′ ) > 0. Consequently,
there exists an execution path:
                                        P        P
                    (σ, ρ) = (σ0 , ρ0 ) ⇒ ... ⇒ (σn , ρn ) = (σ ′ , ρ′ )       (A.63)

such that σi |= φ ∧ b (0 ≤ i ≤ n). Since tr (σ ′ (A)ρ′ ) > 0, it must hold
that ρi ̸= 0 for i = 0, 1, ..., n. By Claim 2, we have σi+1 (t) < σi (t) for
i = 0, 1, ..., n − 1. Therefore, execution path (A.63) is a path in the tree that
we constructed in Step 2.
    As a conclusion of this step, since for any n ≥ n0 , the tree contains a
path of length n + 1, it must be an infinite tree.
    Step 4 : Note that we assume that the classical (outcome) type T of any
measurement M is finite. Then from the transition rules given in Definition
3.3, we know that the tree constructed in Step 2 must be finitely branching.
On the other hand, we proved it is an infinite tree in Step 3. Thus, by König’s
lemma, the tree has an infinite path
                                 P      P             P                    P
            (σ, ρ) = (σ0 , ρ0 ) ⇒ ... ⇒ (σn , ρn ) ⇒ (σn+1 , ρn+1 ) ⇒ ....

                                            68
Consequently, by the fact (ii) at the end of Step 2, we obtain an infinite
decreasing sequence

                   σ(t) = σ0 (t) > ... > σn (t) > σn+1 (t) > ...

of integers. On the other hand, by the fact (i) at the end of Step 2, we have
σn |= φ for all n ≥ 0. Invoking the assumption (A.51), i.e. |= φ → t ≥ 0, we
then obtain σn (t) ≥ 0 for all n ≥ 0. This is a contradiction.
    Therefore, we have proved that limn→∞ ∆∗n = 0. Substituting this into
(A.57), we obtain (A.53) and the proof is completed.

Appendix A.4. Verification Example: Quantum Fourier Transform
   In this section, we provide the proof details omitted in Example 5.2.
   (1) Proof of correctness formula (24): First, we notice that
     (
       Reverse[q[1 : 1]] = I (the identity operator on) H2 ,
                                                                     (A.64)
       Reverse[q[1 : n]](|Φ⟩ ⊗ |ψ⟩) = |ψ⟩ ⊗ Reverse[q[1 : n]]|Φ⟩

                                ⊗(n−1)
for any ψ⟩ ∈ H2 and |Φ⟩ ∈ H2             , and

                     Reverse † [q[1 : n]] = Reverse[q[1 : n]].

Then we can prove

 Reverse † [q[1 : n]]|QFT (j, k : l)⟩ = |QFT ∗ (j, n − l + 1 : n − k + 1)⟩ (A.65)

by induction on l − k. Indeed, the basis case of k = l is immediate from the
first equality in (A.64). The induction step is then derived as follows. By
the induction hypothesis and the second equality in (A.64) we obtain:

  Reverse † [q[1 : n]]|QFT (j, k : l)⟩ = Reverse[[1 : n]]|QFT (j, k : l)⟩
                                                                                
                                                   1         2π0.j[l−k−1:l]
                                                                               
  = Reverse[[q[1 : n]] |QFT (j, k : l − 1)⟩ ⊗ √ |0⟩ + e                     |1⟩
                                                    2
      1
  = √ |0⟩ + e2π0.j[l−k−1:l] |1⟩ ⊗ Reverse[[q[1 : n]]|QFT (j, k : l − 1)⟩
                                  
       2
      1
  = √ |0⟩ + e2π0.j[l−k−1:l] |1⟩ ⊗ |QFT ∗ (j, n − l + 2 : n − k + 1)⟩
                                  
       2
  = |QFT ∗ (j, n − l + 1 : n − k + 1)⟩.

                                          69
Here, the fourth equality comes from the induction hypothesis for n − 1.
Therefore, it holds that

             B ∗ (j, 1 : n) = Reverse † [q[1 : n]]B(j, 1 : n)Reverse[q[1 : n]]

and thus (24) is established by (Axiom-Uni).
   (2) Proof of correctness formula (26): Let A(j, m : n) = 1 (constant)
when m > n. We want to prove:
                                                        
  m ≤ n, |φ⟩q[m] ⟨φ| ⊗ A(j, m + 1 : n) CR[q[m : n]] m ≤ n, |ψ⟩q[m] ⟨ψ| ⊗ A(j, m + 1 : n)
                                                                             (A.66)
by induction on the length n − m of the arrays. If m = n, then |φ⟩ = |ψ⟩
and it is obvious that (A.66) holds. By the induction hypothesis, we have:
 
   m ≤ n − 1, |φ⟩q[m] ⟨φ| ⊗ A(j, m + 1 : n − 1) CR[q[m : n − 1]]
                               m ≤ n − 1, |ψ ′ ⟩q[m] ⟨ψ ′ | ⊗ A(j, m + 1 : n − 1)
                              

where
                              1
                      |ψ ′ = √ (|0⟩ + e2πi0.j[m:n−1] |1⟩).
                               2
Note that q[n] ∈
               / q[m : n − 1] and

           A(j, m + 1 : n) = A(j, m + 1 : n − 1) ⊗ |j[n]⟩q[n] ⟨j[n]|.             (A.67)

Then it holds that

  m ≤ n, |φ⟩q[m] ⟨φ| ⊗ A(j, m + 1 : n) CR[q[m : n − 1]]
                                         m ≤ n, |ψ ′ ⟩q[m] ⟨ψ ′ | ⊗ A(j, m + 1 : n) .
                                       

                                                                            (A.68)

     On the other hand, by (Axiom-Uni) we have:

    m ≤ n, |ψ ′ ⟩q[m] ⟨ψ ′ | ⊗ |j[n]⟩q[n] ⟨j[n]| C(Rn−m+1 )[qn , qm ]

                                                 
                                                  m ≤ n, |ψ⟩q[m] ⟨ψ| ⊗ |j[n]⟩q[n] ⟨j[n]| .

Note that q[m] and q[n] do not occur in A(j, m + 1 : n − 1). Then by (A.67)
we obtain:
  m ≤ n, |ψ ′ ⟩q[m] ⟨ψ ′ | ⊗ A(j, m + 1 : n) C(Rn−m+1 )[qn , qm ]

                                             
                                               m ≤ n, |ψ⟩q[m] ⟨ψ| ⊗ A(j, m + 1 : n) .
                                                                            (A.69)

                                            70
Now we can use (Rule-Seq) to derive:

  m ≤ n, |φ⟩q[m] ⟨φ| ⊗ A(j, m + 1 : n) CR[q[m : n − 1]]; C(Rn−m+1 )[qn , qm ]
                                       
                                         m ≤ n, |ψ⟩q[m] ⟨ψ| ⊗ A(j, m + 1 : n) .

from (A.68) and (A.69). Thus, by the inductive definition of CR[q[m : n]],
we know that (A.66) holds.




                                     71
