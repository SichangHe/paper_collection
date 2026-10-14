                                                                   Toward Automatic Verification of Quantum Programs


                                                                                              Mingsheng Ying
                                                            Centre for Quantum Software and Information, University of Technology Sydney, Australia
                                                      State Key Laboratory of Computer Science, Institute of Software, Chinese Academy of Sciences, China
                                                                  Department of Computer Science and Technology, Tsinghua University, China
                                                                          Email: Mingsheng.Ying@uts.edu.au; Yuan.Feng@uts.edu.au
arXiv:1807.11610v1 [quant-ph] 31 Jul 2018




                                               Abstract—This paper summarises the results obtained by            of quantum states, obtained by introducing the axioms
                                            the author and his collaborators in a program logic approach         for unitary transformations and quantum measurements.
                                            to the verification of quantum programs, including quantum           Roughly speaking, the assertions (preconditions and
                                            Hoare logic, invariant generation and termination analysis for
                                            quantum programs. It also introduces the notion of proof             postconditions) in this logic are properties of the real
                                            outline and several auxiliary rules for more conveniently            and imaginary components of the amplitudes.
                                            reasoning about quantum programs. Some problems for future         • Baltag and Smets [BS06] chose to develop a quantum
                                            research are proposed at the end of the paper.                       generalisation of Propositional Dynamic Logic (PDL),
                                                                                                                 which is an extension of Hoare logic for verification of
                                                                 I. I NTRODUCTION                                classical programs. The approach of [BS06] is different
                                                                                                                 from [BJ04], [CMS06], and it can be essentially seen
                                               Programming is error-prone. Programming a quantum                 as a reinterpretation of the language of PDL where a
                                            computer and designing quantum communication protocols               quantum action is interpreted as a (classical) relation
                                            are even worse due to the weird nature of quantum systems            between quantum states and models the input-output
                                            [Yin16]. Therefore, verification techniques and automatic            relation of a quantum program. In particular, by intro-
                                            tools for quantum programs and quantum protocols will be             ducing some axioms to handle separation and locality,
                                            indispensable whence commercial quantum computers and                their proof system can be used to reason about the
                                            quantum communication systems are available. In the last 10          behaviours (e.g. entanglement) of compound quantum
                                            years, various verification techniques for classical programs        systems.
                                            have been extended to deal with quantum programs; in par-          • Kakutani [Ka09] proposed a quantum extension of
                                            ticular, several quantum program logics have been proposed:          Den Hartog and De Vink’s probabilistic Hoare logic
                                              • Brunet and Jorrand [BJ04] proposed to apply Birkhoff-            [KV02]. The quantum programming language used in
                                                von Neumann quantum logic in reasoning about quan-               [Ka09] is Selinger’s QPL [Sel04] without recursive
                                                tum programs. In the Birkhoff-von Neumann logic,                 calls but with while loops. The assertions in this
                                                closed subspaces of the state Hilbert space of a                 logic are probabilistic predicates (or assertions) used
                                                quantum system are used to represent the properties              in [KV02] but, of course, re-interpreted in the setting
                                                of the system, and logical connectives ¬ (negation),             of quantum computation (e.g. the probability that qubit
                                                ∧ (and), ∨ (or) are interpreted as the operations:               variable q returns to 0 upon the measurement in the
                                                ortho-complement, meet and join, respectively, in the            computational basis is 41 ).
                                                orthomodular lattice of all closed subspaces of the            • Some useful proof rules for reasoning about quantum
                                                Hilbert space. The idea of [BJ04] is to add quantum              programs were introduced by Feng et al. [FDJY07].
                                                operations (e.g. unitary transformations and quantum             The programming language employed in [FDJY07] is
                                                measurements) into the language of quantum logic so              a natural quantum extension of the while-language.
                                                that it can be employed to describe and reason about             For simplicity of presentation, only purely quantum
                                                the dynamics (evolution) of a quantum system (e.g. a             programs without classical variables were considered
                                                quantum program).                                                there. The assertions in these proof rules are physical
                                              • Chadha, Mateus and Sernadas [CMS06] presented one                observables (mathematically modelled by Hermitian
                                                of the first attempts to develop a Hoare-like logic for          operators), or quantum predicates as called in [DP06].
                                                quantum programs. The quantum programs considered                Furthermore, a Hoare-like logic for both partial and
                                                in [CMS06] can have both classical and quantum                   total correctness of quantum programs with (relative)
                                                variables (memories). But only bounded iterations are            completeness was established in [Yin11].
                                                allowed in these quantum programs. The logic given
                                                in [CMS06] is an extension of exogenous quantum              The mathematic foundations, the programming languages
                                                logic [MS06], which has terms representing amplitudes        and the expressivity of the assertions of the quantum pro-
gram logics presented in [CMS06], [Ka09], [Yin11] are                   II. H OARE L OGIC FOR Q UANTUM P ROGRAMS
carefully compared in a recent survey [Rand17].
                                                                    Hoare logic is a cornerstone in verification of classical
   Except program logics, model-checking techniques have          programs. As mentioned in Section I, several attempts
also been developed for verification of quantum communi-          [BJ04], [CMS06], [BS06], [FDJY07], [Ka09], [Yin11] have
cation protocols and quantum programs. For example, Gay,          been made to build a Hoare-like logic for quantum programs.
Papanikolaou and Nagarajan [GPN08] developed a model-             In this section, we focus on the one presented in [Yin11]
checker for verifying properties of the quantum systems           because it is the only quantum Hoare logic with (relative)
that can be modelled in the stabiliser formalism. Feng et         completeness in the existing literature.
al. [FYY13] presented an algorithm for model-checking
quantum systems described as super-operator valued Markov         A. Syntax and Semantics
chains, and the algorithm was implemented by Feng et al. in
[FHTZ15]. The problem of checking linear-time properties            Let us first briefly recall the syntax of a quantum extension
of quantum systems was studied in [YLYF14], where linear-         of the while-language. It is assumed that the reader is
time properties are defined to be infinite sequences of sets      familiar with the basic notions of quantum computing. (A
of atomic propositions modelled as closed subspaces of            reader not familiar with them can have a quick look at
the state Hilbert spaces, as in the Birkhoff-von Neumann          Section 2 of [Yin11] or Section 1.1 of [YYW17]; for more
quantum logic.                                                    details, we refer to [NC00] or [Yin16].) We assume a
                                                                  countably infinite set Var of quantum variables. For each
  The main purpose of this paper is to summarise the results
                                                                  q ∈ Var, we write Hq for its state Hilbert space.
obtained by the author and his collaborators in a program
                                                                    Definition 2.1 (Syntax [Yin11], [Yin16]): The quantum
logic approach to the verification of quantum programs. The
                                                                  while-programs are defined by the grammar:
paper is an extension of an invited talk at SETTA’2016
[Yin16a], but the results presented in Sections IV and V                 P ::= skip | P1 ; P2 | q := |0i | q := U [q]        (1)
as well as the examples given in Section III are new and
                                                                                    | if (m · M [q] = m → Pm ) fi           (2)
have not been published elsewhere.
                                                                                      | while M [q] = 1 do P od              (3)
   The paper is organised as follows: The syntax and seman-
tics of a quantum extension of the while-language is defined         The command “q := |0i” is an initialisation that sets
and a logic of Hoare-style for reasoning about quantum            quantum variable q to a basis state |0i. The statement
programs is presented in Section II. As is well-known,            “q := U [q]” means that unitary transformation U is per-
correctness specification of classical programs can be very       formed on quantum register q, leaving the states of the
tricky. Indeed, correctness specification of quantum pro-         variables not in q unchanged. The construct “if · · · fi” is
grams can be even much trickier. In Section III, we present       a quantum generalisation of case or switch statement. In
several simple examples through which the reader can better       executing it, measurement M = {Mm } is performed on q,
understand the difference between classical and quantum           and then a subprogram Pm is selected to be executed next
correctness specifications. The notion of proof outline is        according to the outcomes m of measurement. The statement
introduced and a strong soundness theorem is proved for           “while · · · od” is a quantum generalisation of while-loop.
quantum programs in Section IV. Several auxiliary axioms          The measurement in it has only two possible outcomes 0, 1.
and inference rules are given in Section V, which can help        If the outcome 0 is observed, then the program terminates,
to simplify verifications of quantum programs. Some basic         and if the outcome 1 occurs, the program executes the loop
ideas for mechanising quantum program verification based          body P and continues the loop.
on the quantum Hoare logic are described in Section VI.              To further illustrate these program constructs, let us see
The algorithms for generating invariants and termination          two simple examples, both of which are quantum generali-
analysis of quantum programs are summarised in Sections           sations of certain probabilistic programs. The first is taken
VII and VIII, respectively. Some topics for future studies        from [YYW17], and it is the quantum version of the example
are pointed out in the concluding section. For convenience        of three dials in [KMMM10].
of the reader, several basic properties of operators in Hilbert
                                                                     Example 2.1 (Three Quantum Dials): Consider a slot
spaces needed in this paper are listed in Appendix A. Several
                                                                  machine that has three dials d1 , d2 , d3 and two suits ♥ and
simple quantum relations (i.e. quantum predicates in a tensor
                                                                  ♦. It spins the dials independently so that they come to rest
product of state Hilbert spaces) were employed in Section
                                                                  on each of the suits with equal probability. This machine
III, a brief discussion on composition of quantum relations
                                                                  can be modelled as a probabilistic program:
that can be used to generate more sophisticated quantum
relations from these simple ones is given in Appendix A.            flip ≡ (d1 := ♥ ⊕ 21 d1 := ♦); (d2 := ♥ ⊕ 12 d2 := ♦);
For readability, the proofs of the results in Sections IV and
V are deferred to Appendix A.                                                                        (d3 := ♥ ⊕ 12 d3 := ♦)
where P1 ⊕p P2 stands for a probabilistic choice which                (Sk) hskip, ρi → h↓, ρi
chooses to execute P with probability p and to execute Q
                                                                      (In) hq := |0i, ρi → h↓, ρq0 i
with probability 1 − p.
  We can define a quantum variant of flip as follows:                 (UT) hq := U [q], ρi → h↓, U ρU † i
                                                                                hP1 , ρi → hP1′ , ρ′ i
                 qflip ≡ H[d1 ]; H[d2 ]; H[d3 ]                       (SC)
                                                                            hP1 ; P2 , ρi → hP1′ ; P2 , ρ′ i
                                                                                                                          †
                                                                      (IF) hif (m · M [q] = m → Pm ) fi, ρi → hPm , Mm ρMm i
where H is the Hadamard gate in the 2-dimensional Hilbert
space H2 with {|♥i, |♦i} as an orthonormal basis. The                 (L0)    hwhile M [q] = 1 do P od, ρi → h↓, M0 ρM0† i
program qflip also spins the dials, but does it in a quantum          (L1)    hwhile M [q] = 1 do P od, ρi →
way modelled by the Hadamard “coin-tossing” operator H.
                                                                                        hP ; while M [q] = 1 do P od, M1 ρM1† i
   It is worth pointing out an interesting difference between
the probabilistic and quantum setting: spinning the dials             Figure 1. Transition Rules for Quantum while-Programs.            In (IN),
with equal probability can be implemented in many different           ρq0 = P|0iq h0|ρ|0iq h0| + |0iq h1|ρ|1iq h0| if type(q) = Bool and
                                                                        q      ∞
ways in the quantum world; e.g. a quantum gate different              ρ0 =     n=−∞ |0iq hn|ρ|niq h0| if type(q) = Int. In (SC), we make
                                                                      the convention ↓; P2 = P2 . In (IF), m ranges over every possible outcome
from the Hadamard gate.                                               of measurement M = {Mm }.
   The second example is a quantum generalisation of ran-
dom walk that every one working on probabilistic algorithms
or programming must be familiar with. Here is a simplified            This walk can be written as the quantum while-loop:
version (taken from [YYFD13]) of the one-dimensional
                                                                      QW ≡ c := |Li; p := |0i;while M [p] = no do c := H[c];
quantum walks defined in [ABNVW01].
   Example 2.2 (Quantum Walk): Let Hc be the 2-                                               c, p := S[c, p] od
dimensional Hilbert space with orthonormal basis states |Li              It is worth noticing an essential difference between the
and |Ri, indicating directions Left and Right, respectively.          quantum walk and a classical random walk: the coin (or
It is the state space of a quantum coin. Let Hp be the                direction) variable c can be in a superposition of |Li and |Ri
n-dimensional Hilbert space with orthonormal basis states             like |+i = √12 (|Li + |Ri), and thus the walker is moving
|0i, |1i, ..., |n − 1i, where vector |ii denotes position i           left and right “simultaneously”; for example,
for each 0 ≤ i < n. The state space of the walk is
                                                                            1                     1
H = Hc ⊗ Hp . The initial state is |Li|0i. Each step of the                √ (|Li + |Ri)|ii → √ (|Li|i ⊖ 1i + |Ri|i ⊕ 1i).
walk consists of:                                                            2                     2
  1) Measure the position of the system to see whether it is          This means that if the walker is currently at position i, then
     1. If the outcome is “yes”, then the walk terminates,            after one step she/he will be at both position i ⊖ 1 and i ⊕ 1.
     otherwise, it continues. The measurement is mathe-                  Similar to the case of classical while-programs, the op-
     matically modelled by M = {Myes , Mno }, where                   erational semantics of quantum programs can be defined
                                                                      as a transition relation between configurations. For each
                                                                      quantum program P , we write var (P ) for the set of quantum
                                               X
         Myes = |1ih1|, Mno = Ip − Myes =         |iihi|
                                                      i6=1
                                                                      variables occurring in P . Let
                                                                                                     O
     and Ip is the identity operator in the position space                                 HP =             Hq
                                                                                                       q∈var (P )
     Hp ;
  2) The Hadamard “coin-tossing” operator H is applied                be the state Hilbert space of P . A partial density operator
     in the coin space Hc ;                                           is defined as a positive operator ρ with trace tr (ρ) ≤ 1. We
  3) The shift operator S defined by                                  write D(HP ) for the set of partial density operators in HP .
                                                                      A configuration is a pair hP, ρi, where P is a program or
          S|L, ii = |L, i ⊖ 1i,      S|R, ii = |R, i ⊕ 1i             the termination symbol ↓, and ρ ∈ D(HP ) denotes the state
                                                                      of quantum variables.
      for i = 0, 1, ..., n − 1 is performed on the space H.              Definition 2.2 (Operational Semantics [Yin11], [Yin16]):
      Intuitively, the system walks one step left or right            The operational semantics of quantum programs is defined
      according to the direction state. Here, ⊕ and ⊖ stand           by the transition rules in Figure 1.
      for addition and subtraction modulo n, respectively.               It is worth pointing out that the transition rules (In), (UT),
      The operator S can be equivalently written as                   (IF), (L0) and (L1) are decreed by the basic postulates
           n−1                           n−1                          of quantum mechanics. A major difference between the
                                                                      operational semantics of classical and quantum programs
           X                             X
      S=         |LihL| ⊗ |i ⊖ 1ihi| +         |RihR| ⊗ |i ⊕ 1ihi|.
           i=0                           i=0                          should be noticed. During the execution of a classical case
statement or a while-loop, checking its guard does not            for the Werner state, a typical entangled state of three qubits,
change the state of program variables. In contrast, checking      then
the guard of a quantum case statement or a quantum loop                              1
requires to perform a measurement on (the system denoted          JqflipK(|W i) = √ (3|♥, ♥, ♥i + |♥, ♥, ♦i + |♥, ♦, ♥i
                                                                                   2 6
by) the program variables, which, again decreed by a basic
                                                                                         − |♥, ♦, ♦i + |♦, ♥, ♥i − |♦, ♥, ♦i
postulate of quantum mechanics, changes the state of these
variables. From the operational semantics, we see that the                               − |♦, ♦, ♥i − 3|♦, ♦, ♦i).
control flow of a quantum program is determined by the               (Note that Definitions 2.2 and 2.3 are given in a more
outcomes of the quantum measurements occurring in the             general way; i.e. in terms of density operators. Here, for sim-
case statements or loops. Note that the outcomes of quantum       plicity, a pure state |ψi is identified with the corresponding
measurements are classical information, so the control flows      density operator ρ = |ψihψ|.)
of quantum programs considered in this paper are classical.          The Löwner order between operators in the state Hilbert
Quantum programs with quantum control flows were studied          space HP of a quantum program is defined as follows:
in [vT04], [AG05], [Zu05], [BP15], [SVV18] and Chapters
6 and 7 of [Yin16].                                                        A ⊑ B if B − A is a positive operator.
   Definition 2.3 (Denotational Semantics [Yin11], [Yin16]):      This order can be naturally lifted to an order between
For any program P , its semantic function is the mapping:         quantum operations (or super-operators). It can be shown
                                                                  that the set D(HP ) of partial density operators in HP with
          JP K : D(HP ) → D(HP )
                    X                                             the Löwner order ⊑ is a complete partial order (CPO), and
          JP K(ρ) =     {|ρ′ : hP, ρi →∗ h↓, ρ′ i|}               all quantum operations in HP form a CPO too. Then a
                                                                  fixed point characterisation for the denotational semantics
for every ρ ∈ D(HP ), where →∗ is the reflexive and               of quantum while-loops can be derived (see Proposition
transitive closure of →, and {| · |} denotes a multi-set.         5.1(6) and Corollary 5.1 in [Yin11], or Proposition 3.3.2
   The defining equation of JP K(ρ) deserves an explanation.      and Corollary 3.3.1 in [Yin16]).
It is clear from rules (IF), (L0) and (L1) that transition
relation → is usually not deterministic; that is, {|ρ′ :          B. Partial Correctness and Total Correctness
hP, ρi →∗ h↓, ρ′ i|} may have more than one element. This            Now we review the notions of partial and total cor-
is different from the case of classical while-programs. The       rectness for quantum programs. Recall from [MM05] that
summation in the right-hand side of the equation comes from       probabilistic predicates (or assertions, e.g. preconditions and
the essential linearity of quantum mechanics. It is proved        postconditions) are defined to be bounded real-valued func-
that JP K(·) is a quantum operation (or a super-operator) (for    tions interpreted as the expectations of random variables.
the definition of quantum operation, see [NC00], Chapter 8        As introduced in [DP06], a quantum predicate in a Hilbert
or [Yin16], Chapter 2).                                           space H is an observable (a Hermitian operator) A in H
   To illustrate the above two definitions, let reconsider the    with 0 ⊑ A ⊑ I, where 0 and I are the zero operator
three quantum dials in Example 2.1.                               and the identity operator in H, respectively, and ⊑ stands
   Example 2.3 (Semantics of Three Quantum Dials): — A            for the Löwner order. In the quantum foundations literature,
Continuation of Example 2.1. A state of probabilistic pro-        a quantum predicate is called an effect (see, for example,
gram flip is a configuration of the slot machine, i.e. a          [Kr83]).
mapping from dials to suits. The semantics of flip is a              Definition 2.4 (Correctness Formula [Yin11], [Yin16]):
function that maps each initial state to a uniform distribution   A correctness formula (or a Hoare triple) is a statement of
of states in which every configurations has probability 18 .      the form
   In contrast, the state Hilbert space of quantum program                                  {A}P {B}
qflip is then H2⊗3 . For instance, if we write:
                                                                  where P is a quantum program, and both A, B are quantum
           1                            1                         predicates in HP , called the precondition and postcondition,
    |+i = √ (|♥i + |♦i),          |−i = √ (|♥i − |♦i)             respectively.
            2                            2
                                                                     The appearance of a quantum Hoare triple is exactly the
for the equal superpositions of |♥i and |♦i, then:                same as that of its classical counterpart. But in a classical
                                                                  Hoare triple, precondition A and postcondition B stands for
               JqflipK(|+, −, +i) = |♥, ♦, ♥i;                    (first-order) logical formulas, and in a quantum Hoare triple,
                                                                  A and B are two operators that are interpreted as observables
if we write:                                                      in physics.
              1                                                      Definition 2.5 (Correctness [Yin11], [Yin16]): — Partial
      |W i = √ (|♥, ♥, ♦i + |♥, ♦, ♥i + |♦, ♥, ♥i)
               3                                                  and Total.
  1) The correctness formula {A}P {B} is true in the sense           (Ax.Sk) {A}Skip{A}
     of total correctness, written |=tot {A}P {B}, if for all
                                                                     (Ax.In.B) {|0iq h0|A|0iq h0| + |1iq h0|A|0iq h1|}q := |0i{A}
     input states ρ ∈ D(HP ) we have:                                          ( ∞                       )
                                                                                  X
                      tr(Aρ) ≤ tr(BJP K(ρ)).                (4)      (Ax.In.I)          |niq h0|A|0iq hn| q := |0i{A}
                                                                                       n=−∞
  2) The correctness formula {A}P {B} is true in the sense           (Ax.UT) {U † AU }q := U [q] {A}
     of partial correctness, written |=par {A}P {B}, if for                 {A}P1 {B}      {B}P2 {C}
     all input states ρ ∈ D(HP ) we have:                            (R.SC)
                                                                                  {A}P1 ; P2 {C}
        tr(Aρ) ≤ tr(BJP K(ρ)) + [tr(ρ) − tr(JP K(ρ))]. (5)                                {Am }Pm {B} for all m
                                                                     (R.IF) nP                o
                                                                                    †
   A key to understanding the above definition is the ob-                      m Mm Am Mm if (m · M [q] = m → Pm ) fi{B}
                                                                                               n                o
servation that tr (Aρ) is the expected (average) value of                              {B}P M0† AM0 + M1† BM1
observable A when the system is in state ρ. The following            (R.LP)
lemma shows that the defining inequalities (4) and (5) for                  {M0† AM0 + M1† BM1 }while M [q] = 1 do P od{A}
total and partial correctness can be restated in a form of                  A ⊑ A′ {A′ }P {B ′ } B ′ ⊑ B
                                                                     (R.Or)
Löwner order, which is often easier to manipulate because                              {A}P {B}
the universal quantifier over density operator ρ is eliminated.
   Let us consider the three quantum dials in Examples 2.1           Figure 2. Proof System qPD for Quantum while-Programs.   In (Ax.In.B),
                                                                     type(q) = Boolean. In (Ax.In.I), type(q) = Int.
and 2.3 once again to illustrate the notion of correctness
introduced in the above definition.
   Example 2.4 (Correctness of Three Quantum Dials):                               • {Q}S{M0†P M0 + M1† QM1 }
We write:                                                                          • for any ǫ > 0, tǫ is a (M1† QM1 , ǫ)−ranking
                    1                                                                      function of loop while M [q] = 1 do S od
           |GHZ i = √ (|♥, ♥, ♥i + |♦, ♦, ♦i)                        (R.LT)
                     2
                                                                                 {M0† P M0 + M1† QM1 }while M [q] = 1 do S od{P }
for the GHZ (Greenberger-Horne-Zeilinger) state, another
typical entangled state of three qubits,                                   Figure 3.   Proof System qTD for Quantum while-Programs.

        1
|Φi =     (|♥, ♥, ♥i + |♥, ♦, ♦i + |♦, ♥, ♦i + |♦, ♦, ♥i),
        2                                                                  where I is the identity operator in HP , and JP K∗
                                                                           stands for the dual of super-operator JP K (see Defi-
and |Ψi = |♥, ♥, ♥i. Then A = |ΦihΦ|, B = |ΨihΨ| and
                                                                           nition A.1 in Appendix A).
C = |GHZ ihGHZ | are all quantum predicates. It is easy to
                                                                          Proof: Immediate from Lemma 4.1.2 in [Yin16] and
check that
                                                                     Lemma A.2 in Appendix A.
                                           1                           The above lemma will be extensively used in the proofs
    |=tot {A}qflip{C},              |=tot { B}qflip{C}.
                                           4                         of the results in Section V.
This means that if the input is state |Φi, then program qflip        C. Quantum Hoare Logic
will certainly output the GHZ state; and if the input is state
                                                                        A Hoare-like logic for quantum programs is established
|Ψi, it will output a state |Γi that is similar to the GHZ state
                                                                     in [Yin11]. It consists of:
in the sense:
                                                                        • A proof system qPD for partial correctness: The axioms
                                                               1          and inference rules of qPD are presented in Figure 2.
Pr(|Γi and the GHZ state cannot be discriminated) ≥              .
                                                               4        • A proof system qTD for total correctness: qTD is

   Note that partial and total correctness are the same for               obtained from qPD by replacing rule (R.LP) with the
qflip because it does not contain any loop.                               rule (R.LT) given in Figure 3. The notion of ranking
   The quantum predicates A, B, C in the above example are                function used in rule (R.LT) is defined in the following:
very simple and defined by a particular input/output state.               Definition 2.6 ([Yin11], [Yin16]): Let A be a quantum
More examples of correctness specifications will be given                 predicate in Hvar (P )∪q and real number ǫ > 0. A
in Section III.                                                           function
   Lemma 2.1: 1) |=tot {A}P {B} if and only if A ⊑                             t : D(Hvar (P )∪q ) → N (nonnegative integers)
      JP K∗ (B).
   2) |=par {A}P {B} if and only if:                                      is called a (A, ǫ)-ranking function of quantum loop
                                                                          “while M [q] = 1 do P od” if it satisfies the following
                  A ⊑ JP K∗ (B) + (I − JP K∗ (I))                         two conditions: for all ρ ∈ D(Hvar (P )∪q ),
                       
      1) t JSK M1 ρM1†       ≤ t(ρ); and                        for any unitary operator U in Hq . The precondition in (6)
                                                                and the postcondition in (7) express equalities “q = U † |ψi”,
                                         
      2) tr(P ρ) ≥ ǫ implies t JSK M1 ρM1†    < t(ρ).
                                                                “q = U |ψi”, respectively. More generally, for any closed
  It is interesting to carefully compare the Hoare rule for     subspace X of Hq , Membership “q ∈ X” can be expressed
partial correctness of classical loops:                         as quantum predicate PX (the projection onto X) and we
                    {ϕ ∧ b}P {ϕ}                                have:
             {ϕ}while b do P od{ϕ ∧ ¬b}                                       |=tot {PU † (X) } q := U [q] {PX },           (8)
and its variant for total correctness with the corresponding                  |=tot {PX } q := U [q] {PU(X) }               (9)
rules (R.LP) and (R.LT) for quantum loops, respectively.
At the first glance, the rules for classical loops and those    The precondition in (8) and the postcondition in (9) express
for quantum loops are very different. But actually there is     memberships “q ∈ U † (X)”, “q ∈ U (X)”, respectively.
a certain similarity between them: in the rules for classical   B. Quantum Relations
loops, ϕ∧b (resp. ϕ∧¬b) can be thought of as the restriction
                                                                   A quantum predicate about multiple quantum systems
of ϕ under b (resp. ¬b). If we set:
                                                                q1 , ..., qn ; i.e. an observable (between the zero and identity
                D = M0† AM0 + M1† BM1 ,                         operators) in the tensor product:
                                                                                           n
then B can be seen as the restriction of D under M1 and A                                  O
                                                                                                 Hqi ,
the restriction of D under M0 , and M0 can be considered                                   i=1
as the negation of M1 . Furthermore, as we will see at the
end of Section VII, rules (R.LP) and (R.LT) can also be         can be understood as a quantum relation among q1 , ..., qn .
                                                                In particular, a quantum predicate A in H1 ⊗ H2 can be
understood in the context of inductive assertion.
                                                                seen as a quantum (binary) relation between H1 and H2 .
  The soundness and (relative) completeness of both proof
                                                                The following are two examples showing some quantum
system qPD and qTD were proved in [Yin11], [Yin16].
                                                                relations used in preconditions and postconditions. A further
  Theorem 2.1 (Completeness [Yin11], [Yin16]): For any
                                                                discussion about quantum relation is given in Appendix A.
quantum while-program P , and for any quantum predicates
                                                                   Example 3.2: An equality like x = y between two vari-
A, B,
                                                                ables x, y also often appears in precondition or postcondition
           |=par {A}P {B} ⇔ ⊢qPD {A}P {B},                      of a classical program correctness formula, e.g.
           |=tot {A}P {B} ⇔ ⊢qTD {A}P {B}.                            |=tot {x = y} x := x + 1; y := y + 1 {x = y}
      III. E XAMPLES OF Q UANTUM C ORRECTNESS                     1) Let p, q be two quantum variables with the same
                    S PECIFICATION                                   state Hilbert space H. Then equality “p = q” can be
   In this section, let us see several simple examples, which        expressed as the symmetrisation operator:
shows some interesting and tricky differences between spec-                                  1
ifying correctness of classical programs and that of quantum                          S+ = (I + SWAP)
                                                                                             2
programs.
                                                                     where I is the identity operator in H⊗H, and operator
A. Unary Quantum Predicates                                          SWAP in H ⊗ H is defined by
   A quantum predicate about a single quantum system q; i.e.                           SWAP|ϕ, ψi = |ψ, ϕi
an observable (between the zero and identity operators) in
state Hilbert space Hq can be understood as a unary quantum           for all |ϕi, |ψi ∈ H, together with linearity. It is easy
predicate.                                                            to see that SWAP · S+ = S+ · SWAP = SWAP · S+ ·
   Example 3.1: An equality like x = c with x being a                 SWAP = S+ . Furthermore, for any unitary operator
variable and c a constant often appears in precondition or            U in H, it holds that:
postcondition of a classical program correctness formula,                     |=tot {S+ } p := U [p]; q := U [q] {S+ }
e.g.
               |=tot {x = 1}x := x + 1{x = 2}                         It is interesting to note that a similar conclusion holds
                                                                      for the anti-symmetrisation operator:
Let q be a quantum variable and |ψi a given (constant) state                                   1
in Hq . Then equality “q = |ψi” can be expressed as quantum                              S− = (I − SWAP)
                                                                                               2
predicate A = |ψihψ| in Hq , and we have:
                                                                      that is, we have SWAP · S− = S− · SWAP = −S− ,
            |=tot {U † |ψihψ|U } q := U [q] {A},          (6)         SWAP · S− · SWAP = S− and
                                              †
            |=tot {A} q := U [q] {U |ψihψ|U }             (7)                 |=tot {S− } p := U [p]; q := U [q] {S− }
  2) Equality “x = y” can also be expressed in a different     where |ϕi, |ψi ∈ H, and I is the identity operator in H,
     way; that is, as the operator                             then it holds that
                                                                |=tot {|ϕihϕ| ⊗ |ψihψ| ⊗ I}R, X := SWAP[R, X];
                          =B = |ΨihΨ|
                                                                      Y, Y := SWAP[X, Y ]; Y, R := SWAP[Y, R] (11)
     in H ⊗ H, where d = dim H and |Ψi = √1d i |iii is
                                                 P
                                                                      {|ψihψ| ⊗ |ϕihϕ| ⊗ I}
     the maximally entangled state defined by an orthonor-
     mal basis B = {|ii} of H. This equality =B has            Intuitively, the precondition and postcondition of (11) means
     an intuitive explanation. The Hilbert-Schmidt inner       “X = |ϕi and Y = |ψi”, “X = |ψi and Y = |ϕi”,
     product of two operators A, B in H:                       respectively. Here, auxiliary variables |ϕi, |ψi are employed.
                                                                  All of the examples given in the previous subsection and
                      hA|Bi = tr A† B
                                        
                                                               this subsection can be proved using axiom (Ax.UT) and rule
                                                               (R.SC) in Figure 2. A more interesting example using rule
     is often used to measure the similarity between A         (R.IF) will be presented in Section IV.
     and B. For two (mixed) states ρ, σ in H, it follows
     immediately from equation (9.73) in [NC00] that           C. Logical Connectives
                                                                  Logical connectives are widely used in specifying (the
        hρ|σi = d · hΨ|ρ ⊗ σ|Ψi = d · tr (=B (ρ ⊗ σ)) .        preconditions and postconditions of) classical programs.
                                                               Here, we show that several quantum counterparts of them
     The quantity tr (=B (ρ ⊗ σ)) can be interpreted as the
                                                               can be used in specifying correctness of quantum programs.
     degree that ρ, σ satisfies relation =B . Obviously, we
                                                               However, it is not the case that every logical connective has
     have:
                                                               an appropriate quantum counterpart.
           |=tot {=U † (B) } p := U [p]; q := U [q] {=B }         Example 3.4: The predicate “True” and “False” are de-
                                                               scribed by the identity and zero operators I and 0, respec-
           |=tot {=B } p := U [p]; q := U [q] {=U(B) }         tively, in the state Hilbert space HP of the program P under
                                                               consideration.
     where =U(B) , =U † (B) are the equalities defined by         • |=par {I}P {B} means that for any density operator ρ,
     orthonormal  bases U (B) = {U |ii} and U † (B) =
                                                                                  tr (BJP K(ρ)) = tr (JP K(ρ));
      †
      U |ii , respectively.
  Example 3.3: Consider the following correctness formula          that is, the probability that postcondition B is satisfied
for classical programs:                                            by the output is equal to the probability that the
                                                                   program terminates.
    |=tot {X = x ∧ Y = y} R := X; X := Y ; Y := R
                                                                 • |=par {A}P {I} always holds, because A ⊑ I implies
                          {X = y ∧ Y = x}                          that for any partial density operator ρ,
It means that after executing the program, the values of             tr (Aρ) ≤ tr (ρ) = tr(JP K(ρ)) + [tr(ρ) − tr (JP K(ρ))].
variables X and Y are exchanged. To properly specify the
precondition and postcondition, auxiliary (ghost) variables      •   |=tot {I}P {B} means that for any density operator ρ,
x, y are introduced. In quantum computing, statements R :=                             tr (BJP K(ρ)) = 1.
X, X := Y and Y := R cannot be directly realised as
prohibited by the no-cloning theorem [WZ82]. But we can            Since B ⊑ I, we have tr (BJP K(ρ)) ≤ tr(JP K(ρ))
consider the following modification: let X, Y, R be three          and thus tr (JP K(ρ)) = 1; that is, program P always
quantum variables with the same state Hilbert space H. Then        terminates, and output JP K(ρ) satisfies postcondition
we have:                                                           B.
                                                                 • |=tot {A}P {I} means that for any density operator,
|=tot {A}R, X := SWAP[R, X]; Y, Y := SWAP[X, Y ];                  tr(Aρ) ≤ tr(JP K(ρ)); intuitively, if precondition A is
      Y, R := SWAP[Y, R] {(SWAP ⊗ I)A(SWAP ⊗ I)}                   satisfied by input ρ to P , then P terminates.
                                             (10)                Example 3.5: 1) Negation in classical logic has a
for any quantum predicate A in H ⊗ H ⊗ H, where the first,          quantum counterpart: for each quantum predicate in
second and third H are the state Hilbert spaces of X, Y, R          Hilbert space H, I − A can be used as the negation
respectively, and I is the identity operator in H. Note that        of A. In fact, for any density operator ρ in H,
we do not use any auxiliary (ghost) variable in correctness                        tr[(I − A)ρ] = 1 − tr (Aρ).
formula (10). In particular, if
                                                                 2) Conjunction in classical logic does not always have
                A = |ϕihϕ| ⊗ |ψihψ| ⊗ I,                            an appropriate quantum counterpart; some difficulties
      caused by this fact in reasoning about quantum pro-        A proof outline for the correctness of QTEL is also presented
      grams were discussed in [YCFD07]. But if A1 and A2         in Figure 5.
      are quantum predicates in H1 , H2 , respectively, then        We can define the notion of subprogram of a quantum
      A1 ⊗ A2 can be used as the conjunction (in H1 ⊗ H2 )       program in a familiar way; namely by induction on the
      of A1 and A2 because for any density operator ρ1 in        length of the program. Then a special form of proof outline
      H1 and ρ2 in H2 , it holds that                            is defined in the following:
                                                                    Definition 4.2: A proof outline {A}P ∗ {B} of P is called
        tr ((A1 ⊗ A2 )(ρ1 ⊗ ρ2 )) = tr (A1 ρ1 ) · tr (A2 ρ2 );
                                                                 standard if every subprogram Q of P is proceeded by exactly
     for example, see equation (11).                             one quantum predicate, denoted pre(Q), in P ∗ .
  3) For a family {Ai }of quantum predicates in the same            The next proposition shows that standard proof outlines
     Hilbert space H, and a probability distribution   {pi },    are indeed sufficient for reasoning about correctness of
                                                                 quantum programs.
                                              P
     we often use the convex combination i pi Ai as a
     connective; for example, see rules (R.CC) and (R.Inv)          Proposition 4.1: 1) If {A}P ∗ {B} is a proof out-
     in Figure 7.                                                       line for partial correctness (respectively, total cor-
                                           †                            rectness), then ⊢qPD {A}P {B} (respectively, ⊢qTD
                                   P
  4) In a sense, quantum predicate m Mm      Am Mm in rule
     (R.IF) in Figure 2 can be understood as the disjunction            {A}P {B}).
     of (the conjunction of) “the outcome of measurement            2) If ⊢qPD {A}P {B} (respectively, ⊢qTD {A}P {B}),
     M is m” and quantum predicate Am .                                 then there is a standard proof outline {A}P ∗ {B} for
                                                                        partial correctness (respectively, total correctness).
                  IV. P ROOF O UTLINES                                 Proof: Induction on the lengths of proof and
   The notion of proof outline can be introduced to structure    formation.
a correctness proof of a classical while-program, according         As in classical programming, another usage of proof
to the structure of the program itself, so that the proof        outline is that it enables us to establish a strong soundness
is easier to follow (see [ABO09], Section 3.4). It is also       of quantum Hoare logic. To this end, we need the following:
a basis for defining non-interference in reasoning about            Definition 4.3: Let P be a quantum while-program and
parallel programs with shared variables. In this section, we     T a subprogram of P . Then at (T, P ) is inductively defined
generalise this notion to the quantum case.                      as follows:
   Definition 4.1: Let S be a quantum while-programs.               1) If T ≡ P , then at (T, P ) ≡ P ;
   1) A proof outline for partial correctness of S is a             2) If P ≡ P1 ; P2 , then at (T, P ) ≡ at (T, P1 ); P2 when
       formula {A}P ∗ {B} formed by the formation axioms                T is a subprogram of P1 , and at (T, P ) ≡ at (T, P2 )
       and rules in Figure 4, where P ∗ results from P by               when T is a subprogram of P2 ;
       interspersing quantum predicates.                            3) If P ≡ if (m · M [q] = m → Pm ) fi, then for each
   2) A proof outline for total correctness of S is defined             m, whenever T is a subprogram of Pm , at (T, P ) ≡
       by introducing ranking function into rule (R.LP’) (see           at (T, Pm );
       Definition 2.6 and rule (R.LT)).                             4) If P ≡ while M [q] = 1 do P ′ od and T is a
   Let us consider a simple example to illustrate the above             subprogram of P ′ , then at (T, P ) ≡ at (T, P ′ ); P .
definition.                                                         Intuitively, at (T, P ) denotes the remainder of P to be
   Example 4.1 (Teleportation [BBCJPW92]): Quantum               executed when the control is at subprogram T .
teleportation is a protocol that can send quantum states            Definitions 4.1 to 4.3 are straightforward generalisations
only using a classical communication channel. Suppose that       of the corresponding concepts for classical programs (see
Alice possesses two qubits p, q and Bob possesses qubit r,       for example [ABO09], Section 3.4). However, the strong
and there is entanglement, i.e. the EPR (Einstein-Podolsky-      soundness (Theorem 3.3 in [ABO09]) cannot be straight-
Rosen) pair:                                                     forwardly generalised to the quantum case. To present the
                          1                                      strong soundness for quantum programs, we also need to
                 |β00 i = √ (|00i + |11i),                       extend the transition relation between configurations given in
                           2
                                                                 Definition 2.2 to a transition relation between configuration
between q and r. Then Alice can send a quantum state             ensembles. We define a configuration ensemble as a multi-
|ψi = α|0i + β|1i to Bob, i.e. from p to r, by two-              set {|hPi , ρi i|} of configurations with
bit classical communication (for detailed description, see                                X
[NC00], Section 1.3.7). This protocol can be written as                                       tr (ρi ) ≤ 1.
quantum program QTEL in Figure 5. The correctness of                                     i
QTEL can be described as the Hoare triple:
                                                                 For simplicity, we identify a singleton {|hP, ρi|} with the
  {|ψip hψ| ⊗ |β00 iq,r hβ00 |} QTEL {Ip ⊗ Iq ⊗ |ψir hψ|} .      configuration hP, ρi.
            (Ax.Sk′ ) {A}Skip{A}
            (Ax.In.B′ ) {|0iq h0|A|0iq h0| + |1iq h0|A|0iq h1|}q := |0i{A}
                        ( ∞                        )
                           X
                    ′
            (Ax.In.I )           |niq h0|A|0iq hn| q := |0i{A}
                              n=−∞
            (Ax.UT′ )     {U † AU }q := U [q] {A}
                         {A}P1∗ {B}      {B}P2∗ {C}
            (R.SC′ )
                            {A}P1 ; {B}P2∗ {C}
                                   ∗
                                                   ∗
                                            {Ami }Pm   {B} (i = 1, ..., k)
            (R.IF′ )           nP                   oi
                                   k     †                                          ∗
                                   i=1 Mmi Ami Mmi      if M [q] = m1 → {Am1 } Pm     1

                                                                 ..................

                                                                                 ∗
                                                           M [q] = mk → {Amk } Pm k
                                                     fi {B}
                                                           n                o
                                                   {B}P ∗ M0† AM0 + M1† BM1
            (R.LP′ )                                                      n                 o
                           {M0† AM0 + M1† BM1 } while M [q] = 1 do {B} P ∗ M0† AM0 + M1† BM1 od {A}
                         A ⊑ A′ {A′ }P ∗ {B ′ } B ′ ⊑ B
            (R.Or′ )
                               {A}{A′ }P {B ′ }{B}
                          {A}P ∗ {B}
            (R.Del)
                          {A}P ∗∗ {B}

Figure 4. Formation Axioms and Rules for Partial Correctness of Quantum while-Programs. In (R.IF’), {m1 , ..., mk } is the set of all possible outcomes
of measurement M . In (R.Del), S ∗∗ is obtained by deleting some quantum predicates from S ∗ .



              {|ψip hψ| ⊗ |β00 iq,r hβ00 |}
               ⊑ {|β00 ip,q hβ00 | ⊗ |ψir hψ| + |β10 ip,q hβ10 | ⊗ |ψ1 ir hψ1 |
                                                           + |β01 ip,q hβ01 | ⊗ |ψ2 ir hψ2 | + |β11 ip,q hβ11 | ⊗ |ψ3 ir hψ3 |}
 QTEL ≡ p, q := CNOT[p, q];
        {|+ip h+| ⊗ |0iq h0| ⊗ |ψir hψ| + |−ip h−| ⊗ |0iq h0| ⊗ |ψ1 ir hψ1 |
                                                                  + |+ip h+| ⊗ |1iq h1| ⊗ |ψ2 ir hψ2 | + |−ip h−| ⊗ |1iq h1| ⊗ |ψ3 ir hψ3 |}
              p := H[p];
              {|0ip h0| ⊗ |0iq h0| ⊗ |ψir hψ| + |1ip h1| ⊗ |0iq h0| ⊗ |ψ1 ir hψ1 |
                                                          + |0ip h0| ⊗ |1iq h1| ⊗ |ψ2 ir hψ2 | + |1ip h1| ⊗ |1iq h1| ⊗ |ψ3 ir hψ3 |}
              if M [q] = 0 → {|0ip h0| ⊗ Iq ⊗ |ψir hψ| + |1ip h1| ⊗ Iq ⊗ |ψ1 ir hψ1 |} skip
                           1 → {|0ip h0| ⊗ Iq ⊗ |ψ2 ir hψ2 | + |1ip h1| ⊗ Iq ⊗ |ψ3 ir hψ3 |} r := X[r]
              fi;
               {|0ip h0| ⊗ Iq ⊗ |ψir hψ| + |1ip h1| ⊗ Iq ⊗ |ψ1 ir hψ1 |}
              if M [p] = 0 → {Ip ⊗ Iq ⊗ |ψir hψ|} skip
                            1 → {Ip ⊗ Iq ⊗ |ψ1 ir hψ1 |} r := Z[r]
              fi {Ip ⊗ Iq ⊗ |ψir hψ|}

Figure 5. Quantum Teleportation Program and Correctness Proof Outline.      (1) Quantum states: |ψ1 i = α|0i − β|1i, |ψ2 i = β|0i + α|1i,
|ψ3 i = −β|0i + α|1i. (2) Entangled states: |β01 = √1 (|01i + |10i, |β10 = √1 (|00i − |11i, |β01 = √1 (|01i − |10i. (3) Measurement in the
                                                     2                       2                        2
computational basis: M = {M0 , M1 }, where M0 = |0ih0|, M1 = |1ih1|.
   Definition 4.4: The transition relation between configura-          It is interesting to compare our auxiliary axioms and rules
tion ensembles is of the form:                                      for quantum programs with those for classical programs:
                                                                       • The appearance of axiom (Ax.Inv) is the same as axiom
                 {|hPi , ρi i|} → {|hQj , σj i|}             (12)
                                                                          (INVARIANCE) in Section 3.8 of [ABO09].
and defined by rules (Sk), (In), (UT), (SC) in Figure 1                • Obviously, rule (R.SO) is quantum generalisations of
together with the rules presented in Figure 6.                            rule (SUBSTITUTION) in [ABO09], with the substi-
   Now we are ready to present the strong soundness of the                tution z := t being replaced by an arbitrary super-
quantum Hoare logic.                                                      operator E.
   Theorem 4.1 (Strong Soundness): Let {A}P ∗ {B} be a                 • It is easy to see that rules (R.CC) and (R.Inv) are
standard proof outline for partial correctness. If                        generalisations of rules (CONJUNCTION) and (IN-
                                                                          VARIANCE), respectively, in [ABO09], with logical
                    hP, ρi →∗ {|hPi , ρi i|},                             conjunction being replaced by a probabilistic (convex)
then:                                                                     combination.
                                                                       • It is more interesting to note that rule (R.TI) is a
  1) for each i, Pi ≡ at (Ti , P ) for some subprogram Ti of              quantum generalisation of two rules (DISJUNCTION)
      P or Pi ≡P ↓; and                                                   and (∃-INTRODUCTION) in [ABO09], where partial
  2) tr (Aρ) ≤ i tr (Bi ρi ), where                                       trace is considered as a quantum counterpart of logical
                                                                          disjunction and existence quantifier.
                   (
                     B             if Pi ≡ ↓,
             Bi =                                                      The following theorem establishes soundness of the aux-
                     pre (Ti ) if Pi ≡ at (Ti , P ) .
                                                                    iliary axioms and rules in Figure 7.
     Proof: See Appendix A.                                            Theorem 5.1: 1) The axiom (Ax.Inv) is sound for par-
  A difference between the above theorem and the strong                     tial correctness.
soundness for classical while-programs (see [ABO09], The-              2) The rules (R.TI), (R.CC), (R.Inv), (R.SO) and (R.Lim)
orem 3.3) should be noticed. The summation in the right-                    are sound both for partial and total correctness.
hand side of the inequality in clause 2 of the above theorem              Proof: See Appendix B
indicates that we have to consider all the reached programs            Before concluding this section, let us see a simple exam-
Pi collectively in the quantum case. The reason behind it is        ple to show how the auxiliary axioms and rules can be used
that certain nondeterminism is introduced in the operational        to derive some new properties of a quantum program.
semantics of case statements and while-loops in quantum                Example 5.1: Let q be a qubit variable. Then by (Ax.UT)
computation.                                                        in Figure 3 we obtain:

           V. AUXILIARY A XIOMS AND RULES                                          {|−ih−|} q := H[q] {|1ih1|}               (13)
   Several auxiliary axioms and rules introduced in [Gor75],        where H is the Hadamard gate and |−i =         √1 (|0i − |1i).
                                                                                                                     2
[Har79] (see also [ABO09], Section 3.8) are very useful             The rule (R.SO) in Figure 7 is especially useful for reason-
for simplifying the presentation of correctness proofs of           ing about quantum computation with noise. The amplitude
classical programs. In this section, we generalise some of          damping channel is an important type of quantum noise
them into the quantum case. For this purpose, we first              where energy is lost from a quantum system with a certain
introduce several notations. Let X ⊆ Y ⊆ Var, and let               probability γ. It can be modelled by quantum operation:
A be an operator in
                              O                                                      E(ρ) = E0 ρE0 + E1 ρE1
                       HX =       Hq .
                                                                    for any density operator ρ, where
                                q∈X
                                                                                                            √ 
                                                                                  1 √ 0                      1  γ
Then operator:                                                           E0 =                   ,     E1 =         .
                                                                                  0    1−γ                   0 0
                    cl Y (A) = A ⊗ IHY \X                           Then applying (R.SO) to (13) yields:
                                                                                     √
is called the cylindric extension of A in HY . If X, Y ⊆ Var
                                                                                                                          
                                                                       1+γ             1−γ                      1−γ
and X ∩ Y = ∅. Then partial trace tr Y is a mapping from                    |0ih0| −        (|0ih1| + |1ih0|) +     |1ih1|
                                                                        2               2                         2
operators in HX∪Y to operators in HX defined by
                                                                              q := H[q] {γ|0ih0| + (1 − γ)|1ih1|} .
         tr Y (|ϕihψ| ⊗ |ϕ′ ihψ ′ |) = hψ ′ |ϕ′ i · |ϕihψ|          VI. M ECHANISING Q UANTUM P ROGRAM V ERIFICATION
                                    ′     ′
for every |ϕi, |ψi in HX and |ϕ i, |ψ i in HY .                       Proving correctness of classical programs using Hoare
  Now we can present the auxiliary axioms and rules for             logic is very fiddly and tedious. As we saw from the example
quantum programs in Figure 7.                                       given in Figure 5, it is even worse to prove correctness of
             (IF′ )                                                    †
                      hif (m · M [q] = m → Pm ) fi, ρi → {|hPm , Mm ρMm i|}
             (L′ )hwhile M [q] = 1 do P od, ρi → {|h↓, M0 ρM0† i, hP ; while M [q] = 1 do P od, M1 ρM1† i|}
                   hP, ρi ∈ A hP, ρi → B
             (MS)
                   A → (A \ {|hP, ρi|}) ∪ B

                 Figure 6.   Extended Transition Rules for Quantum while-Programs.    In (MU), A, B are configuration ensembles.




                                 (Ax.Inv)   {A} P {A}
                                            {A}P {B}
                                 (R.TI)
                                         {tr W A} P {B}
                                           {Ai } P {Bi } (i = 1, ..., m)
                                 (R.CC)
                                          { m
                                            P                 Pm
                                               i=1 pi Ai } P { i=1 pi Bi }
                                                   {A}P {B}
                                 (R.Inv)
                                          {pA + qC}P {pB + qC}
                                                {A}P {B}
                                 (R.SO)
                                          {E ∗ (A)} P {E ∗ (B)}
                                           limn→∞ An = A {An } P {Bn }                    limn→∞ Bn = B
                                 (R.Lim)
                                                                  {A}P {B}

Figure 7. Auxiliary Axioms and Rules. In (Ax.Inv), var (P ) ∩ V = ∅ and A = cl V ∪var (P ) (B) for some V ⊆ Var and for some quantum predicate
B in HV . In (R.TI),PV, W ⊆ Var , V ∩ W = ∅, A, B are quantum predicates in HV ∪W and HV , respectively, and var (P ) ⊆ V. In (R.CC), pi ≥ 0
(i = 1, ..., m) and m  i=1 pj ≤ 1. In (R.Inv), p, q ≥ 0, p + q ≤ 1, and C is a quantum predicate in HV for some V ⊆ Var with V ∩ var (P ) = ∅. In
(R.SO), E is a quantum operation (or super-operator) in HV for some V ⊆ Var with V ∩ var (P ) = ∅. In (R.Lim), {An } and {Bn } are increasing and
decreasing, respectively sequences with respect to the Löwner order.



quantum programs because a huge amount of vector and                       estimation, which is a key in Shor’s factoring algorithm.
matrix calculations is involved. Thus, automatic tools will                We can expect that more automatic tools for verification
be very helpful.                                                           of quantum programs and quantum cryptographic protocols
  Similar to the case of classical programs, a verifier can                will be built after quantum computers be commercialised.
prove the correctness:
                                                                                     VII. I NVARIANTS OF Q UANTUM P ROGRAMS
            ⊢par {A}P {B} (or ⊢tot {A}P {B})                                  It has been well-understood since the very beginning that
of a quantum program P in the following three steps:                       invariant generation is crucial for automatic verification of
   • Annotating the program: insert quantum predicates at                  programs, and the problem of invariant generation has been
      the intermediate points (in a way similar to a proof                 intensively studied for classical programs. At this moment,
      outline described in Section IV). Intuitively, an inserted           invariants are provided by humans to the theorem prover
      statement is intended to hold when the control reaches               for quantum programs developed in [LLW16] rather than
      the corresponding point.                                             generated by the system itself. But the issue of generating
   • Generating verification conditions (VCs): a set of math-              quantum invariants was recently considered in [YYW17]. In
      ematical statements, usually of the form Ai ⊑ Bi (see                this section, we briefly review the main results in [YYW17].
      Lemma 2.1), is generated from the annotated program,                    We first observed that the control flow of a quantum
      where Ai , Bi are matrices, and ⊑ stands for the Löwner              program can be represented by a super-operator-valued
      order. It is required that if all the generated VCs are              transition system (SVTS):
      true, then ⊢par {A}P {B} (or ⊢tot {A}P {B}).                            Definition 7.1 (Super-Operator-Valued Transition Systems [YYW17]):
   • Proving VCs: prove that matrix Bi − Ai is positive                    An SVTS is a 5-tuple:
      semi-definite for each VC Ai ⊑ Bi .                                                         S = hH, L, l0 , T , Θi,
   Recently, a theorem prover was built by Liu, Li, Wang et
al. in [LLW16] for the quantum Hoare logic based on the                    where:
proof assistant Isabelle/HOL. It has been used to verify sev-                1) H is a Hilbert space;
eral quantum programs, including Grover search and phase                     2) L is a finite set of locations;
  3) l0 ∈ L is the initial location;                                •  Algorithmic analysis of termination for quantum pro-
  4) Θ is a quantum predicate in H denoting the initial                grams was first considered in [YF10] where the Jor-
     condition; and                                                    dan decomposition of complex matrices was employed
  5) T is a set of transitions. Each transition τ ∈ T is               as the main tool. In [YYFD13], the author and his
                         E
     written as τ = l → l′ with l, l′ ∈ L and E being a                collaborators introduced quantum Markov chains as
     super-operator in H. For each l ∈ L, it is required that          a semantic model of quantum programs. Then in a
                         X           E
                                                                       series of their papers [YFYY13], [YY12], [LYY14],
                   El =      {|E : l → l′ ∈ T |}                       termination of quantum programs was reduced to the
                                                                       reachability problem of quantum Markov chains, which
         is trace-preserving, i.e. tr (El (ρ)) = tr(ρ) for all ρ.
                                                                       is in turn tackled by developing a theory of quantum
   Now we assume that the control flow SVTS of quantum                 graphs (see [Yin16], Section 5.2). Indeed, this line of
program P is SP with state Hilbert space HP (see [YYW17]               research also paves a way to model-checking quantum
for detailed construction of SP ). A set Π of paths in HP is           systems.
said to be prime if for each                                         • The notion of ranking function was defined in [Yin11]
                              E     En−1                               in order to present the proof rule (R.LT) for to-
                     π = l1 →1 ... → ln ∈ Π,                           tal correctness of quantum loops. It was recalled as
its proper initial segments                                            Definition 2.6 in this paper. In the last few years,
                                                                       (super)martingales have been employed as a powerful
                           E1    Ek−1
                        l1 → ... → lk ∈    /Π                          mathematical tools for termination analysis of proba-
                                                                       bilistic programs [CS13], [FH15], [CFNH16]. Recently,
for all k < n. We write         P Eπ for the composition of            a notion of quantum (super)martingales was introduced
E1 , ..., En−1 and EΠ =           {|Eπ : π ∈ Π|}. Then we can          in [LY18] as a generalisation of Definition 2.6 and used
define invariants for quantum programs:                                to characterise the termination of quantum programs.
   Definition 7.2 (Invariants of Quantum Programs [YYW17]):            The synthesis problem of (super)martingales for quan-
Let SP = hHP , L, l0 , T , Θi be the control flow SVTS of              tum programs was also investigated there. The basic
quantum program P and l ∈ L. An invariant at location                  idea is that the fundamental Gleason theorem [Gle57]
l ∈ L is a quantum predicate O in HP satisfying the                    in quantum foundations can be used to determine the
condition: for any density operator ρ and prime set Π of               template of ranking functions, and then the synthesis
paths from l0 to l, we have:                                           problem of quantum (super)martingales with certain
             tr(Θρ) ≤ 1 − tr (EΠ (ρ)) + tr (OEΠ (ρ)) .                 templates can also be reduced to an SDP problem. It
                                                                       seems that a further development of this line of research
   It was shown in [YYW17] that invariants can be used to              requires us to systematically establish a mathematical
establish partial correctness of quantum programs. We can              theory of quantum (super)martingales first.
also introduce the notion of inductive assertion for quantum         The termination of the quantum walk in Example 2.2
programs. It is not easy to identify the invariant in the proof   was analysed by both of the above approaches [YYFD13],
rules (R.LP) and (R.LT) for quantum loops, at least not           [LY18], and the second approach was also used in [LY18]
as explicit as in the Hoare rule for classical loops. Exam-       to analyse the termination of quantum Bernoulli factory, a
ple 4.1 in [YYW17] indicates that the quantum predicate           quantum algorithm for random number generation [DJR15].
M0† AM0 + M1† BM1 in rules (R.LP) and (R.LT) can be
viewed as an inductive assertion (invariant). Furthermore,                              IX. C ONCLUSION
by generalising the constraint-based technique of Colón et           We conclude this paper by pointing out several problems
al. [CSS03], [SSM04], it was demonstrated in [YYW17] that         for future research:
invariant generation for quantum programs can be reduced to          • Combining Classical Computation and Quantum Com-
an SDP (Semidefinite Programming) problem. In particular,              putation: We have been focusing on pure quantum
the method proposed in [YYW17] was actually applied to                 programs without classical computation. This allows
generate the invariants of the quantum walk in Example 2.2             us to have a clean theory of quantum programming.
and quantum Metropolis sampling [TOVPV11].                             But almost all existing quantum algorithms involves
                                                                       both quantum and classical computation, and the state-
        VIII. T ERMINATIONS A NALYSIS OF Q UANTUM                      of-art quantum programming languages like Quipper
                            P ROGRAMS                                  [GLR13], LIQUi|> [WS14], Q# [SGT18], Scaffold
   As is well-known, termination analysis is a key step                [JPK15] and QWire [PRZ17] include both classical
in proving total correctness of programs. Termination of               and quantum variables. So, it is desirable to gener-
quantum programs has been researched along the following               alise the verification techniques discussed in this paper
two lines:                                                             to quantum programs involving classical computation.
    Indeed, a kind of correctness formulas (Hoare triples)                                 R EFERENCES
    involving both classical and quantum variables were          [AG05] T. Altenkirch and J. Grattage, A functional quantum
    already introduced in [YF11], but a Hoare-like logic for            programming language, In: Proceedings of the 20th IEEE
    programs with both classical and quantum variables is               Symposium on Logic in Computer Science (LICS), 2005,
    still to be developed.                                              249-258.
  • Parallel and Distributed Quantum Programs: Dis-
                                                                 [ABNVW01] A. Ambainis, E. Bach, A. Nayak, A. Vishwanath
    tributed quantum computing has been studied for 20                 and J. Watrous, One-dimensional quantum walks, In:
    years since [Gro97] and [CB97], including finding                  Proceedings of the 33rd ACM Symposium on Theory of
    quantum algorithms for solving paradigmatic prob-                  Computing (STOC), 2001, pp. 37-49.
    lems from classical distributed computing [TKM05],           [ABO09] K. R. Apt, F. S. de Boer and E. -R. Olderog, Verifica-
    experiments toward physical implementation of dis-                   tion of Sequential and Concurrent Programs, Springer,
    tributed quantum computing [SMB06] and architecture                  London 2009.
    of distributed quantum hardware systems [MMN08].
                                                                 [AGN14] E. Ardeshir-Larijani, S. J. Gay and R. Nagarajan, Veri-
    In particular, since practical quantum computers with               fication of concurrent quantum protocols by equivalence
    large qubit capacity are still out of the current technol-          checking, Proc. of the 20th International Conference on
    ogy’s reach, it is an attractive idea to use the physical           Tools and Algorithms for the Construction and Analysis
    resources of two or more small-capacity quantum com-                of Systems (TACAS), 2014, pp. 500-514.
    puters to realise a large-capacity quantum computing
                                                                 [BP15]    C. Bǎdescu and P. Panangaden, Quantum alternation:
    system. So, another interesting problem is how the                     prospects and problems, in: Proc. of the 12th Interna-
    program logic and related techniques considered in this                tional Workshop on Quantum Physics and Logic (QPL),
    paper can be extended for reasoning about parallel                     2015, pp. 33-42.
    and distributed quantum programs. The notion of proof
                                                                 [BS06]    A. Baltag and S. Smets, LQP: the dynamic logic of quan-
    outline for quantum programs introduced in Section IV                  tum information, Mathematical Structures in Computer
    should be helpful in dealing with the (non)interference                Science, 16(2006)491-525.
    of the variables shared by component quantum pro-
    grams.                                                       [BFG14] G. Barthe, C. Fournet, B. Grégoire, P. -Y. Strub, N.
                                                                         Swamy and S. Zanella Béguelin, Probabilistic relational
  • Verification of Quantum Cryptographic Protocols: Over
                                                                         verification for cryptographic implementations, In: Proc.
    the last 10 years, quantum communication has blos-                   of the 41st Annual ACM Symposium on Principles of
    somed into a viable commercial technology. But verify-               Programming Languages (POPL), 2014, pp. 193-206.
    ing correctness and security of quantum communication
                                                                 [BKO13] G. Barthe, B. Köpf, F. Olmedo and Z. Zanella Béguelin,
    protocols is a notoriously difficult problem. Process                Probabilistic relational reasoning for differential privacy,
    algebra approach has been introduced for verification                ACM Transactions on Programming Languages and Sys-
    of quantum cryptographic protocols [AGN14], [FY15],                  tems 35(2013) Art. No. 9.
    [KKK16]. On the other hand, a (probabilistic) rela-
                                                                 [BBCJPW92] C. H. Bennett, G. Brassard, C. Crepeau, R. Jozsa,
    tional Hoare logic (pRHL) and a machine-checked                     A. Peres and W. K. Wootters, Teleporting an unknown
    framework for reasoning about security and privacy in               quantum state via dual classical and Einstein-Podolsky-
    classical computing and communicating systems were                  Rosen channels, Physical Review Letters, 70(1993) 1895-
    established by Barthe, Fournet, Köpf et al. [BFG14],                1899.
    [BKO13]. The success of this line of research suggests       [BJ04]    O. Brunet and P. Jorrand, Dynamic quantum logic for
    us to develop verification techniques for quantum cryp-                quantum programs, International Journal of Quantum
    tographic protocols by extending our quantum Hoare                     Information, 2(2004)45-54.
    logic. Indeed, the first attempt to develop a quantum
                                                                 [CMS06] R. Chadha, P. Mateus and A. Sernadas, Reasoning
    relational Hoare logic (qRHL) was already made by
                                                                         about imperative quantum programs, Electronic Notes in
    Unruh in [Unruh18], where a tool for the verification                Theoretical Computer Science, 158(2006)19-39.
    based on qRHL was implemented and successfully used
    to the security proof of several quantum cryptographic       [CS13]    A. Chakarov and S. Sankaranarayanan, Probabilistic pro-
    protocols.                                                             gram analysis with martingales, In: Proc. of the 25th
                                                                           International Conference on Computer Aided Verification
                                                                           (CAV), 2013, Springer LNCS 8044, 511-526.
  Acknowledgment: The author likes to thank Professors
Martin Fränzle, Deepak Kapur and Naijun Zhan for inviting        [CFNH16] K. Chatterjee, H. F. Fu, P. Novotný and R. Hashem-
me to give a talk at SETTA’2016. This work was partly                   inezhad, Algorithmic analysis of qualitative and quanti-
                                                                        tative termination problems for affine probabilistic pro-
supported by the Australian Research Council (Grant No:                 grams, In: Proc. of the 43rd Annual ACM Symposium
DP160101652) and the Key Research Program of Frontier                   on Principles of Programming Languages (POPL), 2016,
Sciences, Chinese Academy of Sciences.                                  327-342.
[CB97]   R. Cleve and H. Buhrman, Substituting quantum entan-        [Har79] D. Harel, First-Order Dynamic Logic, LNCS 68,
         glement for communication, Physical Review A 56(1997)               Springer, 1979.
         1201-1204.
                                                                     [KV02] J. Den Hartog and E. P. de Vink, Verifying probabilistic
[CSS03] M. A. Colón, S. Sankaranarayanan and H. B. Sipma,                   programs using a Hoare like logic, International Journal
        Linear invariant generation using non-linear constraint             of Foundations of Computer Science 13(2002)315-340.
        solving, In: Proc. of the 15th International Conference
        on Computer Aided Verification (CAV), 2003, Springer         [Kle99] T. Leymann, Hoare logic and auxiliary variables, Formal
        LNCS, pp. 420-433.                                                   Aspect of Computing 11(1999)541-566.

[DJR15] H. Dale, D. Jennings and T. Rudolph, Provable quantum        [KMMM10] J. -P. Katoen, A. McIver, L. Meinicke and C. C.
        advantage in randomness processing, Nature Communi-                Morgan, Linear-invariant generation for probabilistic pro-
        cations 6(2015), art. no. 8203.                                    grams - Automated support for proof-based methods, in:
                                                                           Proc. 17th International Symposium on Static Analysis
[DP06]   E. D’Hondt and P. Panangaden, Quantum weakest pre-                (SAS), 2010, Springer LNCS 6337, pp. 390-406.
         conditions, Mathematical Structures in Computer Sci-
                                                                     [KKK16] T. Kubota, Y. Kakutani, G. Kato, Y. Kawano and H.
         ence, 16(2006)429-451.
                                                                            Sakurada, Semi-automated verification of security proofs
                                                                            of quantum cryptographic protocols, Journal of Symbolic
[FDJY07] Y. Feng, R. Y. Duan, Z. F. Ji and M. S. Ying, Proof rules
                                                                            Computation 73(2016) 192-220.
        for the correctness of quantum programs, Theoretical
        Computer Science 386 (2007)151-166.                          [JPK15] A. JavadiAbhari, S. Patil, D. Kudrow, J. Heckey, A.
                                                                             Lvov, F. T. Chong and M. Martonosi, ScaffCC: Scalable
[FHTZ15] Y. Feng, E. M. Hahn, A. Turrini and L. J. Zhang,                    compilation and analysis of quantum programs, Parallel
        QPMC: a model checker for quantum programs and pro-                  Computing 45(2015) 2-17.
        tocols, Proceedings of the 20th International Symposium
        on Formal Methods (FM), 2015, Springer LNCS 9109,            [Ka09]   Y. Kakutani, A logic for formal verification of quantum
        pp. 265-272.                                                          programs, in: Proceedings of the 13th Asian Computing
                                                                              Science Conference (ASIAN 2009), Springer LNCS 5913,
[FY15]   Y. Feng and M. S. Ying, Toward automatic verification                pp. 79-93.
         of quantum cryptographic protocols, Proc. of the 26th
         International Conference on Concurrency Theory (CON-        [Kr83]   K. Kraus, States, Effects, and Operations: Fundamental
         CUR), 2015, pp. 441-455.                                             Notions of Quantum Theory, Springer, 1983.

[FYY13] Y. Feng, N. K. Yu and M. S. Ying, Model checking             [LY18]   Y. J. Li and M. S. Ying, Algorithmic analysis of ter-
        quantum Markov chains, Journal of Computer and Sys-                   mination problems for quantum programs, In: Proc.
        tem Sciences, 79(2013)1181-1198.                                      of the 45th Annual ACM Symposium on Principles of
                                                                              Programming Languages (POPL), 2018, pp. 35.1-29.
[FH15]   L. M. F. Fioriti and H. Hermanns, Probabilistic termina-
         tion: soundness, completeness, and compositionality. In:    [LYY14] Y. J. Li, N. K. Yu and M. S. Ying, Termination of
         Proc. of the 42nd Annual ACM Symposium on Principles                nondeterministic quantum programs, Acta Informatica
         of Programming Languages (POPL), 2015, 489-501.                     51(2014) 1-24.

[GPN08] S. J. Gay, N. Papanikolaou and R. Nagarajan, QMC:            [LLW16] T. Liu, Y. J. Li, S. L. Wang et al., A theorem
        a model checker for quantum systems. Proceedings of                  prover for quantum Hoare logic and its applications,
        the 20th International Conference on Computer Aided                  arXiv:1601.03835.
        Verification (CAV), 2008, Springer LNCS 5123, pp. 543-
                                                                     [MS06] P. Mateus and A. Sernadas, Weakly complete axiomati-
        547.
                                                                            zation of exogenous quantum propositional logic, Infor-
[Gle57] A. M. Gleason, Measures on the closed subspaces of a                mation and ComputationVolume 204(2006)771-794.
        Hilbert space, Journal of Mathematics and Mechanics          [MMN08] R. van Meter, W.J. Munro, K. Nemoto and K.M.
        6(1957)885-893.                                                     Itoh, Arithmetic on a distributed-memory quantum mul-
                                                                            ticomputer, ACM Journal on Emerging Technologies in
[Gor75] G. A. Gorelick, A complete axiomatic system for proving             Computing Systems 3(2008) Art. No. 17.
        assertions about recursive and non-recursive programs,
        Technical Report, Department of Computer Science, Uni-       [MM05] A. McIver and C. Morgan, Abstraction, Refinement and
        versity of Toronto, 1975.                                           Proof for Probabilistic Systems, Springer, 2005.
[GLR13] A. Green, P. L. Lumsdaine, N. J. Ross, P. Selinger and       [NC00]   M. A. Nielsen and I. L. Chuang, Quantum Computation
        B. Valiron, Quipper: A scalable quantum programming                   and Quantum Information, Cambridge University Press,
        language, In: Proceedings of the 34th ACM Conference                  2000.
        on Programming Language Design and Implementation
        (PLDI), 2013, pp. 333?342.                                   [PRZ17] J. Paykin, R. Rand and S. Zdancewic, QWIRE: a core
                                                                             language for quantum circuits, In: Proc. of the 44th
[Gro97] L.K. Grover, Quantum telecomputation, arXiv:quant-                   Annual ACM Symposium on Principles of Programming
        ph/9704012, 1997.                                                    Languages (POPL), 2017, pp. 846-858.
[Rand17] R. Rand, Verification Logics for Quantum Programs,          [YF10]   M. S. Ying and Y. Feng, Quantum loop programs, Acta
         http://www.cis.upenn.edu/∼rrand/wpe.pdf                              Informatica 47 (2010), 221-250.

[SVV18] A. Sabry, B. Valiron, J. K. Vizzotto, From symmetric         [YF11]   M. S. Ying and Y. Feng, A flow-chart language for
        pattern-matching to quantum control, in: Proc. of the 21st            quantum programming, IEEE Transactions on Software
        International Conference on Foundations of Software                   Engineering 37 (2011) 466-485.
        Science and Computation Structures (FoSSaCS), 2018,
        pp. 348-364.                                                 [YLYF14] M. S. Ying, Y. J. Li, N. K. Yu and Y. Feng, Model-
                                                                             checking linear-time properties of quantum systems,
[SSM04] S. Sankaranarayanan, H. B. Sipma and Z. Manna, Non-                  ACM Transactions on Computational Logic, 15(2014),
        linear loop invariant generation using Gröbner bases,                art. no. 22.
        In: Proc. of the 31st ACM Symposium on Principles of
        Programming Languages (POPL), 2004, pp. 318-329.             [YYW17] M. S. Ying, S. G. Ying and X. D. Wu, Invariants of
                                                                            quantum programs: characterisations and generation, In:
[Sel04]   P. Selinger, Towards a quantum programming language,              Proc. of the 44th Annual ACM Symposium on Principles
          Mathematical Structures in Computer Science 14, (2004)            of Programming Languages (POPL), 2017, pp. 818-832.
          527-586.
                                                                     [YYFD13] M. S. Ying, N. K. Yu, Y. Feng and R. Y. Duan,
[SMB06] A. Serafini, S. Mancinians and S. Bose, Distributed                 Verification of quantum programs, Science of Computer
        quantum computation via optical fibers, Physical Review             Programming, 78(2013)1679-1700.
        Letters 96(2006) Art. No. 010503.
                                                                     [YFYY13] S. G. Ying, Y. Feng, N. K. Yu and M. S. Ying, Reacha-
[SGT18] K. Svore, A. Geller, M. Troyer, J. Azariah, C. Granade,             bility analysis of quantum Markov chains, In: Proc. of the
        B. Heim, V. Kliuchnikov, M. Mykhailova, A. Paz and                  24th International Conference on Concurrency Theory
        M. Roetteler, Q#: Enabling scalable quantum computing               (CONCUR), 2013, pp. 334-348.
        and development with a high-level DSL, In: Proceedings
        of the Real World Domain Specific Languages Workshop         [YY12] N. K. Yu and M. S. Ying, Reachability and termination
        2018, art. no. 8.                                                   analysis of concurrent quantum programs, In: Proc. of the
                                                                            23th International Conference on Concurrency Theory
[TKM05] S. Tani, H. Kobayashi and K. Matsumoto, Exact quan-                 (CONCUR), 2012, pp. 69-83.
       tum algorithms for the leader election problem, ACM
       Transactions on Computation Theory 4(2012) Art. No.           [Zu05]   P. Zuliani, Compiling quantum programs, Acta Informat-
       1.                                                                     ica, 41(2005)435-474.
[TOVPV11] K. Temme, T. J. Osborne, K. G. Vollbrecht, D. Poulin,                                A PPENDIX
       and F. Verstraete. Quantum Metropolis sampling. Nature,
       471(2011) 87-90.                                                 For convenience of the reader, we first review some basic
                                                                     properties of operators and super-operators needed in the
[Unruh18] D. Unruh, Quantum relational             Hoare    logic,   proofs presented in Appendix A. The following lemma gives
         https://arxiv.org/pdf/1802.03188.pdf.                       a characterisation of the Löwner order in terms of trace.
[vT04]    A. van Tonder, A lambda calculus for quantum computa-         Lemma A.1: Let A, B be observables (i.e. Hermitian op-
          tion, SIAM Journal on Computing, 33(2004)1109-1135.        erators) in Hilbert space H. Then A ⊑ B if and only if
                                                                     tr (Aρ) ≤ tr (Bρ) for all density operators in H.
[WS14] D. Wecker and K. M. Svore, LIQUi|>: A software design            The notion of dual super-operator is introduced in the next
       architecture and domain-specific language for quantum
       computing, arXiv:1402.4467, 2014.                             definition. It will be extensively used in Appendix A.
                                                                        Definition A.1: Let E be a quantum operation (i.e. super-
                                                                          P in Hilbert space H with the Kraus representation
                                                                     operator)
[WZ82] W. K. Wootters and W. H. Zurek, A single quantum
       cannot be cloned, Nature, 299(1982) 802-803.                  E = i Ei ◦ Ei† . Then its (Schrödinger-Heisenberg) dual is
[Yin11] M. S. Ying, Floyd-Hoare logic for quantum programs,
                                                                     the super-operator E ∗ defined by
        ACM Transactions on Programming Languages and Sys-
                                                                                                    X †
                                                                                          E ∗ (A) =     Ei AEi
        tems 39 (2011), art. no. 19.
                                                                                                      i
[Yin16] M. S. Ying, Foundations of Quantum Programs, Morgan-         for any observable A in H.
        Kaufmann, 2016.                                                The next lemma presents a characterisation of duality
[Yin16a] M. S. Ying, Toward automatic verification of quantum        between super-operators in terms of trace.
         programs (extended abstract), In: Proc. of the 2nd Inter-     Lemma A.2: For any quantum operation E, observable A
         national Symposium on Dependable Software Engineer-         and density operator ρ in H, we have:
         ing: Theories, Tools, and Applications (SETTA), 2016.
                                                                                       tr (AE(ρ)) = tr (E ∗ (A)ρ).
[YCFD07] M. S. Ying, J. X. Chen, Y. Feng and R. Y. Duan,
       Commutativity of quantum weakest preconditions, Infor-        In particular, tr(E(ρ)) = tr (E ∗ (I)ρ), where I is the identity
       mation Processing Letters 104 (2007) 152-158.                 operator in H.
   Positivity of operators and the Löwner order between          We proceed by induction on the length n of computation.
operators in a tensor product of Hilbert spaces are considered      Induction Basis: For n = 0, {|hPi , ρi i|} is a singleton
in the following:                                                {|hP1 , ρ1 i|} with P1 ≡ P and ρ1 ≡ ρ. Then we can choose
   Lemma A.3: 1) If A1 , A2 are positive operators in H1         T1 ≡ P and it holds that P1 ≡ at (T1 , P ). Note that in
       and H2 , respectively, then A1 ⊗ A2 is a positive         the proof outline {A}P ∗ {B}, we have A ⊑ pre(P ) = B1 .
       operator in H1 ⊗ H2 .                                     Thus,
   2) For any operators A1 , B1 in H1 and A2 , B2 in H2 ,
                                                                                                     X
                                                                               tr(Aρ) ≤ tr(B1 ρ1 ) =   tr(Bi ρi ).
       A1 ⊑ B1 and A2 ⊑ B2 implies A1 ⊗ A2 ⊑ B1 ⊗ B2 .                                                           i
   The proofs of all of the above lemmas can be found in
                                                                   Induction Step: Now we assume that
any standard textbook on the theory of operators in Hilbert
spaces.                                                          hP, ρi →n−1 {|hPi , ρi i|} → {|hPi , ρi i|i 6= i0 |}∪{|hQj , σj i|}
   In Section III, we already saw some simple quantum
relations (i.e. quantum predicates in the tensor product of      where
more than one state Hilbert spaces) in specifying correctness                        hPi0 , ρi0 i → {|hQj , σj i|}
of quantum programs. The notion of composition of classical      is derived by one of the rules used in defining transition
relations is well-defined and widely used to construct com-      relation (12). Then we need to consider the following cases:
plicated relations from simple ones. However, it is highly
nontrivial to find an appropriate definition of the notion of      ◮ Case 1. The last step uses rule (IF′ ). Then Pi0 can be
composition of quantum relations. Here, we give several          written in the following form:
tentative definitions:                                                     Pi0 ≡ if (m · M [q] = m → Rm ) fi,
   Definition A.2: Let A be a quantum relation between H1
and H2 (i.e. an observable in H1 ⊗ H2 between the zero           and for each j, Qj ≡ Rm ≡ at (Rm , P ) and σj =
                                                                            †
and identity operators) and B a quantum relation between         Mm ρi0 Mm    for some m. On the other hand, a segment of the
H2 and H3 . We define three kinds of their compositions:         proof outline {A}P ∗ {B} must be derived by the following
   1) Circle composition:                                        inference:
                                                                                           ∗
                                                                                    {Am }Rm  {C} for every m
                              1 X
                   A ◦B B =          hii|A ⊗ B|iii
                                                                 nP                  o
                                                                          †                                            ∗ ) fi{C}
                              d2 i                                    m Mm Am Mm       if (m · M [q] = m → {Am } Rm

     where and in the sequel d2 = dim H2 and B = {|ii}           and
     is an orthonormal basis of H2 .                                                        X
                                                                                                  †
                                                                  Bi0 = pre (Pi0 ) ⊑             Mm Am Mm ,           Am = pre (Rm ) .
  2) Bullet composition:                                                                    m
                  A •B B = hΨ|A ⊗ B|Ψi                           Therefore,
                                                                                                                              !
     where |ΨiB = √1d
                         P
                          i |iii is the (unnormalised) max-
                                                                                                     X
                                                                                                             †
                       2
     imal entanglement defined by an orthonormal basis                     tr (Bi0 ρi0 ) ≤ tr               Mm Am Mm ρi0
                                                                                                      m
     B = {|ii} of H2 .                                                                           X
                                                                                                         †
                                                                                                                             
  3) Diamond composition:                                                                    =       tr Mm Am Mm ρi0
                                                                                                 m
                 A ⋄v B = tr H⊗2 [Sv (A ⊗ B)Sv ]                                                 X
                                                                                                                   †
                                                                                                                             
                                2                                                            =       tr Am Mm ρi0 Mm
       where v ∈ {+, −}, S± are the symmetrisation and                                           m
                                                                                                 X
       anti-symmetrisation operators (see Example 3.2), and                                  =       tr (pre (Qj ) σj ) .
       tr H⊗2 stands for tracing out the middle two H2 ’s in                                     j
           2
       H1 ⊗ H2 ⊗ H2 ⊗ H3 .                                       By the induction hypothesis, we obtain:
   The algebraic structure of quantum relations equipped                         X
with the above composition operations and corresponding               tr (Aρ) ≤     tr (Bi ρi ) + tr (Bi0 ρi0 )
transitive closures is a very interesting topic for future                          i6=i0
                                                                                    X                       X
research.                                                                       ≤           tr (Bi ρi ) +        tr (pre (Qj ) σj ) .
   In this section, we provide the proofs of theorems omitted                       i6=i0                    j
in the main part of this paper.
                                                                 So, the conclusion is true in this case.
A. Proof of Theorem 4.1                                             ◮ Case 2. The last step uses rule (L′ ). Then Pi0 must be
  To prove the strong soundness, suppose that                    in the following form:
                   hP, ρi →n {|hPi , ρi i|}.                                  Pi0 ≡ while M [q] = 1 do R od
and                                                                  in HV , respectively. Similarly, we have tr W (JP K∗ (I)) =
           {|hQj , σj i|} = {|hQ0 , σ0 i, hQ1 , σ1 i|}               JP K∗ (IV ). Therefore, it follows that

with Q0 ≡ skip, σ0 = M0 ρi0 M0† , Q1 ≡ R; Pi0 and σ1 =                   tr W A ⊑ tr W JP K∗ (B ⊗ IW ) + tr W (I − JP K∗ (I))
M1 ρi0 M1† . A segment of {A}P ∗ {B} must be derived by                         = JP K∗ (B) + (IV − JP K∗ (IV ))
the inference in Figure 8 and Bi0 ⊑ M0 CM0† + M1 DM1† .
Then Q0 ≡ at (skip, P ), pre(Q0 ) = C, Q1 ≡ at(R, P ) and            and |=par {tr W A} P {B}.
pre(Q1 ) = D. It follows that                                          3. We prove the soundness of (R.CC) for partial correct-
                      h                   i                        ness. If for every i = 1, ..., m, |=par {Ai }P {Bi }, then by
    tr (Bi0 ρi0 ) ≤ tr M0 CM0† + M1 DM1† ρi0                         Lemma 2.1 we have:
                                                 
                  = tr M0 CM0† ρi0 + tr M1 DM1† ρi0                                 Ai ⊑ JP K∗ (Bi ) + [I − JP K∗ (I)] .
                                                 
                  = tr CM0† ρi0 M0 + tr DM1† ρi0 M1                  Consequently, it holds that
                                                                           m                m
                = tr (pre(Q0 )σ0 ) + tr (pre(Q1 )σ1 ) .                    X                X
                                                                                  pi Ai ⊑         pj (JP K∗ (Aj ) + [I − JP K∗ (I)])
Furthermore, by the induction hypothesis, we have:                          i=1             i=1
                                                                                                     m
                                                                                                                    !
                X                                                                                    X
      tr (Aρ) ≤     tr (Bi ρi ) + tr (Bi0 ρi0 )                                        = JP K∗             p i Bi       + [I − JP K∗ (I)]
                  i6=i0                                                                              i=1
                  X                       X
              ≤           tr (Bi ρi ) +       tr (pre (Qj ) σj ) .   because JP K∗ (·) is linear, and I − JP K∗ (I) is positive. Thus,
                  i6=i0                   j                          we have:
                                                                                         (m          ) (m              )
Thus, the conclusion is true in this case.                                                  X              X
                                                                                 |=par         pi Ai P           p i Bi .
  ◮ Case 3. The last step uses rule (Sk), (In) or (UT).
                                                                                             i=1                    i=1
Similar but easier.
                                                                        4. We prove the soundness of (R.Inv) for partial cor-
B. Proof of Theorem 5.1                                              rectness. From |=par {A}P {B}, i.e. A ⊑ JP K∗ (B) +
  We only prove the theorem for partial correctness; the             (I − JP K∗ (I)), we derive that
case of total correctness is simpler.
                                                                          pA + qC ⊑ pJP K∗ (B) + p (I − JP K∗ (I))
  1. We first prove that rule (Ax.Inv) is sound for partial
correctness. Since var (P ) ∩ V = ∅, JP K can be seen as a                        = (pJP K∗ (B) + qC) + p (I − JP K∗ (I))
super-operator E in HV c . Then when considering JP K as a                            ⊑ (pJP K∗ (B) + qC) + (I − JP K∗ (I))
super-operator in H, we have:                                                         = JP K∗ (pB + qC) + (I − JP K∗ (I))
      JP K∗ (A) + [I − JP K∗ (I)]                                    because p ≤ 1 and V ∩ var (P ) = ∅ implies JP K∗ (C) = C.
             = B ⊗ E ∗ (IV c ) + [I − IV ⊗ E ∗ (IV c )]              Therefore, we have |=par {pA + qC}P {pB + qC}.
            = B ⊗ E ∗ (IV c ) + IV ⊗ [IV c − E ∗ (IV c )]               5. We prove that rule (R.SO) is sound for partial correct-
            ⊒ B ⊗ E ∗ (IV c ) + B ⊗ [IV c − E ∗ (IV c )]             ness. Suppose that |=par {A}P {B}, i.e. A ⊑ JP K∗ (B) +
                                                                     (I − JP K∗ (I)). Note that E is a super-operator in HV
            = B ⊗ IV c = A
                                                                     and V ∩ var (P ) = ∅. Then E ∗ and JP K∗ commutes, i.e.
because B ⊑ IV c and E ∗ (IV c ) ⊑ IV c , where I stands for         E ∗ ◦ JP K∗ = JP K∗ ◦ E ∗ . Moreover, it holds that E ∗ (I) ⊑ I
the identity operator in H.                                          and thus
  2. Now we prove the soundness of rule (R.TI) for partial                        (I − JP K∗ ) (E ∗ (I)) ⊑ (I − JP K∗ ) (I)
correctness. Assume that |=par {A}P {B}. Then it holds
that                                                                 where I is the identity super-operator. Therefore, we obtain:
           A ⊑ JP K∗ (B ⊗ IW ) + (I − JP K∗ (I))                          E ∗ (A) ⊑ E ∗ [JP K∗ (B) + (I − JP K∗ (I))]
where I is the identity operator in HV ∪W . Note that                              = E ∗ (JP K∗ (B)) + [E ∗ (I) − E ∗ (JP K∗ (I))]
var (P ) ⊆ V . Then we have:                                                       = JP K∗ (E ∗ (B)) + (I − JP K∗ ) (E ∗ (I))
             tr W (JP K∗ (B ⊗ IW )) = JP K∗ (B)                                    ⊑ JP K∗ (E ∗ (B)) + (I − JP K∗ ) (I)
                                                                                   = JP K∗ (E ∗ (B)) + (I − JP K∗ (I))
where the occurrences of JP K in the left-hand side and right-
hand side are seen as a super-operator in HV ∪W and one              and |=par {E ∗ (A)}P {E ∗ (B)}.
                                                   {D}R∗ {M0 CM0† + M1 DM1† }
                                   {M0 CM0† + M1 DM1† } while M [q] = 0 do {C} skip {C}
                                                                             = 1 do R∗ {M0 CM0† + M1 DM1† } od {C}


                                                   Figure 8.   Proof of Theorem 4.1



   6. Finally, we prove the soundness of (R.Lim) for partial
correctness. The existence of limn→∞ An and limn→∞ Bn
is guaranteed by Lemma 4.1.3 in [Yin16]. Assume that |=par
{An }P {Bn }. Then
             An ⊑ JP K∗ (Bn ) + [I − JP K∗ (I)]
and the continuity of super-operator JP K∗ yields:
    A = lim An ⊑ lim (JP K∗ (Bn ) + [I − JP K∗ (I)])
         n→∞         n→∞
                  = JP K∗ ( lim Bn ) + [I − JP K∗ (I)]
                             n→∞
                  = JP K (B) + [I − JP K∗ (I)] .
                         ∗


Thus, |=par {A}P {B}.
