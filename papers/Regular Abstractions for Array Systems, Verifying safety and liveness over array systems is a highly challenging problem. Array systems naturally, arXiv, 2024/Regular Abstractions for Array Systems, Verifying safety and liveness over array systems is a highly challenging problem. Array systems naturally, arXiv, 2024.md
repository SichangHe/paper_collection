                                        Regular Abstractions for Array Systems
                                        CHIH-DUO HONG∗ , National Chengchi University, Taiwan
                                        ANTHONY W. LIN, University of Kaiserslautern-Landau, Germany and MPI-SWS, Germany
arXiv:2401.02618v1 [cs.SE] 5 Jan 2024




                                        Verifying safety and liveness over array systems is a highly challenging problem. Array systems naturally
                                        capture parameterized systems such as distributed protocols with an unbounded number of processes. Such
                                        distributed protocols often exploit process IDs during their computation, resulting in array systems whose
                                        element values range over an inﬁnite domain. In this paper, we develop a novel framework for proving safety
                                        and liveness over array systems. The crux of the framework is to overapproximate an array system as a
                                        string rewriting system (i.e. over a ﬁnite alphabet) by means of a new predicate abstraction that exploits the
                                        so-called indexed predicates. This allows us to tap into powerful veriﬁcation methods for string rewriting
                                        systems that have been heavily developed in the last two decades or so (e.g. regular model checking). We
                                        demonstrate how our method yields simple, automatically veriﬁable proofs of safety and liveness properties
                                        for challenging examples, including Dijkstra’s self-stabilizing protocol and the Chang-Roberts leader election
                                        protocol.
                                        CCS Concepts: • Theory of computation → Automated reasoning; Veriﬁcation by model checking;
                                        Program veriﬁcation; Logic and veriﬁcation; Program analysis.
                                        Additional Key Words and Phrases: Array theory, Regular model checking, Inﬁnite-state model checking,
                                        Abstract interpretation, Predicate abstraction, Distributed protocol veriﬁcation
                                        ACM Reference Format:
                                        Chih-Duo Hong and Anthony W. Lin. 2024. Regular Abstractions for Array Systems. Proc. ACM Program.
                                        Lang. 8, POPL, Article 22 (January 2024), 29 pages. https://doi.org/10.1145/3632864

                                        1   INTRODUCTION
                                        Over the past few decades, extensive research eﬀorts (e.g. [Cimatti et al. 2021; Felli et al. 2021;
                                        Gurﬁnkel et al. 2016; Ma et al. 2019; Mann et al. 2022]) have been devoted to the veriﬁcation of
                                        array systems. Array systems are natural models of sequential programs manipulating linear data
                                        structures such as arrays and lists. In addition, they have also been used as convenient abstrac-
                                        tions of parameterized concurrent systems with local and shared variables (cf. [Alberti et al. 2017;
                                        Bloem et al. 2015]). Speciﬁcally, many distributed protocols require each process to maintain a nu-
                                        merical local variable as its process identiﬁer, rendering these protocols suitable to be modeled as
                                        array systems.
                                           Despite the amount of work on array systems veriﬁcation, the problem remains highly challeng-
                                        ing. Diﬃculty arises from the following two aspects, among others: (1) array elements range over
                                        an inﬁnite domain (e.g. the set of integers), and (2) many properties of interest require quantiﬁca-
                                        tion over the array elements. For instance, the property “array 𝑎 is sorted in ascending order” is
                                        ∗ Corresponding author


                                        Authors’ addresses: Chih-Duo Hong, National Chengchi University, Taipei, Taiwan, chihduo@nccu.edu.tw;
                                        Anthony W. Lin, University of Kaiserslautern-Landau, Kaiserslautern, Germany and MPI-SWS, Kaiserslautern, Ger-
                                        many, awlin@mpi-sws.org.

                                        Permission to make digital or hard copies of part or all of this work for personal or classroom use is granted without fee
                                        provided that copies are not made or distributed for proﬁt or commercial advantage and that copies bear this notice and
                                        the full citation on the ﬁrst page. Copyrights for third-party components of this work must be honored. For all other uses,
                                        contact the owner/author(s).
                                        © 2024 Copyright held by the owner/author(s).
                                        ACM 2475-1421/2024/1-ART22
                                        https://doi.org/10.1145/3632864


                                                                         Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
22:2                                                                               Chih-Duo Hong and Anthony W. Lin


expressed by a universally quantiﬁed formula stating that each element in the array 𝑎 is no smaller
than its preceding elements. For this reason, in order to verify the correctness of an array system, it
is often necessary to reason about quantiﬁed formulae, which is generally undecidable over arrays
(cf. [Bradley and Manna 1998; Kroening and Strichman 2016]).
   Owing to the undecidability of quantiﬁed array theories, existing techniques for handling array
systems employ a mixture of SMT, model checking, synthesis, and/or abstraction. Most eﬀort in
developing SMT over arrays concentrates on providing more support of universal quantiﬁcation
[Bradley et al. 2006; Cimatti et al. 2021; Ge and De Moura 2009; Habermehl et al. 2008; Mann et al.
2022]. To lift SMT over arrays to the veriﬁcation of array systems, one may exploit model checking
techniques like IC3/PDR (e.g. [Cimatti et al. 2016; Gurﬁnkel et al. 2018; Komuravelli et al. 2015]),
backward reachability (e.g. [Abdulla et al. 2009; Ranise and Ghilardi 2010]), synthesis (e.g. SyGuS
[Fedyukovich et al. 2019]), eager abstraction (e.g. [Mann et al. 2022; McMillan 2018]), interpolation
(e.g. [Ghilardi et al. 2021; Hoenicke and Schindler 2018; McMillan 2008]), or predicate abstraction
[Flanagan and Qadeer 2002; Lahiri and Bryant 2004b, 2007], among others. It should be remarked
that, besides a handful of work (e.g. [Padon et al. 2017, 2021]), most existing work on array systems
veriﬁcation concerns safety veriﬁcation, with liveness still posing a signiﬁcant challenge.

   Contributions. This paper presents a new method for reasoning about array systems. We demon-
strate its eﬃcacy for verifying safety and liveness of challenging examples from array programs
and distributed protocols, including Dijkstra’s self-stabilizing protocol and the Chang-Roberts
leader election protocol. The method has two main ingredients. Firstly, we provide a new predicate
abstraction (using indexed predicates) that overapproximates an array system as a string rewriting
system. String rewriting systems can be construed as array systems, whose array elements range
over a ﬁnite domain (a.k.a. alphabet). The second ingredient answers why we use string rewriting
systems as abstractions: this subclass of array systems has been more amenable to solutions than
the general case of arrays. In fact, several powerful veriﬁcation methods over string rewriting sys-
tems (for both safety and liveness, among others) have been developed in the last decade or so,
which include methods in the framework regular model checking [Abdulla 2012; Bouajjani et al.
2004, 2000; Lin and Rümmer 2022]. This framework relies on the decidable ﬁrst-order theory over
words with preﬁx-of-relation, regular constraints, and the equal-length predicate (a.k.a. the uni-
versal automatic structure [Benedikt et al. 2003; Blumensath and Gradel 2000]). The theory of uni-
versal automatic structure can be construed as a kind of array theory, whose elements range over
a ﬁnite domain (e.g. bitvectors). In stark contrast to decidable array theories like [Bradley et al.
2006; Habermehl et al. 2008], however, the theory has no restrictions on the use of quantiﬁers, but
restricts the manner in which the indices are related. The set of solutions deﬁnable by such for-
mulae are precisely those that are captured by synchronized automata running on tuples of words
(a.k.a. regular relations).
   We now provide some details of our method. We use a variant of First-Order Linear Temporal
Logic (FO-LTL) [Abadi 1989; Hodkinson et al. 2000] restricted to a quantiﬁed array theory, in order
to specify both an array system and properties to be veriﬁed. This formalism may also be regarded
as a variant of indexed LTL [Clarke et al. 1986; German and Sistla 1992] with atomic propositions
replaced by expressions from the array theory. Our predicate abstraction reduces this FO-LTL
model checking problem over array systems to a veriﬁcation problem over string rewriting sys-
tems that can be modeled in the framework of regular model checking. We discuss next our notion
of predicate abstraction by means of indexed predicates. Indexed predicates have been used in pre-
vious work (e.g. in [Flanagan and Qadeer 2002] for invariant generation and in [Lahiri and Bryant
2007] for abstracting into a ﬁnite system), but never in the context of computing another inﬁnite-
state system that is more amenable to analysis. To this end, the right logic instantiating the indexed

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
Regular Abstractions for Array Systems                                                                            22:3


Table 1. Comparison between our approach and the classical methods. The first column is the setting of the
classical (indexed) predicate abstraction (e.g. [Flanagan and Qadeer 2002; Jhala et al. 2018; Lahiri and Bryant
2007]). The second column provides our setting of indexed predicate abstraction (Section 4.2). The last column
is our approximation of indexed predicate abstraction using regular languages (Section 4.4), which we refer
to as regular abstraction.

                                            Predicate        Indexed Predicate        Regular
                                           Abstraction          Abstraction          Abstraction

                                            ﬁnite set of    inﬁnite set of words      ﬁnite-state
                      Abstract Set
                                             bitvectors       over bitvectors         automaton

                                           ﬁnite relation     inﬁnite relation        ﬁnite-state
                      Abstract Relation
                                          over bitvectors       over words            transducer

                                          ﬁnite Boolean         inﬁnite-state           regular
                      Abstract System
                                            program          transition system     transition system



predicates has to be devised that suits our abstraction as string rewriting systems. In our case, each
indexed predicate is an atomic formula (a.k.a. atom) with a designated variable 𝑖, e.g., 𝑎[𝑖] ≤ 𝑎[𝑛].
Given indexed predicates h𝑃1 , . . . , 𝑃𝑚 i, interpretations of an array formula 𝜙 are mapped into a
word 𝑤 over the alphabet {0, 1}𝑚 of 𝑚-bitvectors. This word 𝑤 summarizes the truth values of the
predicates over all positions in the arrays interpreting 𝜙.
   Although we have chosen to abstract away the actual array values by means of such indexed
predicates, our abstraction maintains the concrete values of array sizes and index variables in the
abstract domain. This strategy often allows us to compute a precise enough abstraction based on
a small set of predicates. Given an interpretation 𝜎 of an array formula (as numbers and arrays),
the set 𝛼 (𝜎) of abstract values corresponding to 𝜎 (as tuples of numbers and words over a ﬁnite
alphabet) is computable. We propose next to overapproximate sets and relations in the abstract
domain with regular sets and relations. We show that abstractions of quantiﬁed array formulae and
array systems can be suitably approximated using regular language as a symbolic representation.
This yields our notion of regular abstractions for array formulae and systems. Figure 1 compares
this approach with the classical predicate abstraction.
   We show that regular abstractions are suﬃciently precise for veriﬁcation purposes when the
quantiﬁed array formulae used in the FO-LTL speciﬁcations belong to the so-called Singly-Indexed
Array Logic (SIA) [Habermehl et al. 2008]. To evaluate our approach, we consider non-trivial safety
and liveness properties for several case studies, including selection and merge sort algorithms,
Dijkstra’s self-stabilizing algorithm [Dijkstra 1982], and the Chang-Roberts leader election algo-
rithm [Chang and Roberts 1979]. We report promising experimental results for these case studies
using oﬀ-the-shelf regular model checkers as backend inference engines.

2   AN ILLUSTRATIVE EXAMPLE
Dijkstra’s self-stabilizing algorithm [Dijkstra 1982] assumes a ring of 𝑛 ≥ 2 processes with iden-
tiﬁers 1, . . . , 𝑛 and 𝑛 local variables 𝑥 1, . . . , 𝑥𝑛 over {0, . . . , 𝑘 − 1}, where 𝑛 and 𝑘 are ﬁnite but
unbounded parameters satisfying 𝑛 ≤ 𝑘. For 𝑖 ∈ {1, . . . , 𝑛}, Process 𝑖 is privileged if (1) 𝑖 = 1
and 𝑥 1 = 𝑥𝑛 , or (2) 𝑖 > 1 and 𝑥𝑖 ≠ 𝑥𝑖 −1 . At each time step, a privileged process, say Process 𝑖, is
scheduled, and the corresponding variable 𝑥𝑖 is updated by setting (1) 𝑥𝑖 := 𝑥𝑖 + 1 mod 𝑘 when
𝑖 = 1, or (2) 𝑥𝑖 := 𝑥𝑖 −1 when 𝑖 > 1. Process 𝑖 thus loses its privilege after the update. Dijkstra’s
self-stabilizing algorithm can be construed as a kind of token-passing algorithm, whereby a pro-
cess holds a token if and only if it is privileged. The algorithm is self-stabilizing in the sense that
eventually the system will contain a single token forever.

                               Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
22:4                                                                                         Chih-Duo Hong and Anthony W. Lin


   Let us identify each variable 𝑥𝑖 with an array1 value 𝑎[𝑖], and deﬁne a formula
                      Priv(𝑖) := (𝑖 = 1 ∧ 𝑎[𝑖] = 𝑎[𝑛]) ∨ (𝑖 > 1 ∧ 𝑖 ≤ 𝑛 ∧ 𝑎[𝑖] ≠ 𝑎[𝑖 − 1])
indicating that Process 𝑖 is privileged. One interesting property of Dijkstra’s algorithm is that
Process 1 will be privileged inﬁnitely often, regardless of what the initial state is and how the
privileged processes are scheduled. To prove this, we may use an index variable 𝑝𝑖𝑑 to represent the
scheduled process, namely, 𝑝𝑖𝑑 = 1 means that Process 1 is scheduled. Then the property “Process
1 is privileged inﬁnitely often” can be expressed in LTL as GF Priv(1). We would like to prove that
this property holds for Dijkstra’s algorithm under the scheduling assumption G Priv(𝑝𝑖𝑑), namely,
under the assumption that the scheduler always selects a privileged process.
   Inspired by the deﬁnition of Priv(𝑖), we may abstract the local state of each Process 𝑖 using
predicates h𝑎[𝑖] = 𝑎[𝑛], 𝑎[𝑖] = 𝑎[𝑖 − 1]i. The induced abstract state space is then N × N × Σ∗ with
Σ := {00, 10, 01, 11}. Each abstract state (𝑝𝑖𝑑, 𝑛, 𝑤) comprises the valuations of 𝑝𝑖𝑑 and 𝑛, and a
word 𝑤 over the alphabet Σ. The 𝑖-th letter of 𝑤 essentially corresponds to the predicate abstraction
of 𝑎 at position 𝑖. For example, 𝑤 [2] = 01 means that 𝑎 satisﬁes ¬(𝑎[2] = 𝑎[𝑛]) ∧(𝑎[2] = 𝑎[1]). The
abstraction function 𝛼 then maps a concrete state, say 𝑠 := (1, 3, [1, 2, 1]), to a set of abstract states,
say 𝛼 (𝑠) = {(1, 3, [10, 00, 10], (1, 3, [11, 00, 10])}. Observe that we may naively overapproximate
the abstraction of (the concrete states satisfying) Priv(1) by 𝐹 := N × N × (10 + 11) · Σ∗. Here,
𝐹 is an overapproximation in the sense that 𝛼 (𝑠) * 𝐹 implies 𝑠 6 |= Priv(1), whereas 𝛼 (𝑠) ⊆ 𝐹
implies nothing. (For example, given 𝑠 := (1, 2, [1, 2]), we can deduce 𝑠 6 |= Priv(1) by observing
that 𝛼 (𝑠) = {(1, 2, [00, 10]), (1, 2, [01, 10])} * 𝐹 .) Similarly,
                                                              Ð     the abstraction of Priv(𝑝𝑖𝑑) may be
overapproximated by 𝑆 := ({1} × N × (10 + 11) ·Σ∗) ⊎ 𝑖 ≥2 {𝑖} × N × Σ𝑖 −1 · (00 + 10) ·Σ∗ . Thus,
GF Priv(1) holds for Dijkstra’s algorithm under the scheduling assumption G Priv(𝑝𝑖𝑑) if there
does not exist a maximal abstract path 𝜋 ∈ 𝑆 ∗ satisfying FG (𝑆 \ 𝐹 ), namely, 𝜋 consists of states in
𝑆 and eventually stays away from 𝐹 forever.
   In this manner, we can reduce veriﬁcation problems of an array manipulating system to those
of a string manipulating system, for which eﬀective techniques and highly optimized tools exist
(e.g. [Abdulla et al. 2012; Chen et al. 2017; Fiedor et al. 2017; Klarlund and Møller 2001; Klarlund et al.
2002; Lin and Rümmer 2016; Schuppan and Biere 2006]). Unfortunately, the approximations 𝑆 and
𝐹 given above are too rough to verify the desired property, in the sense that they will produce
spurious counterexample paths after the reduction. We shall later show that an appropriate choice
of predicates and approximations will allow us to verify this property.

3 PRELIMINARIES
Notation. We adopt the standard notation of many-sorted logic (see e.g. [van Dalen 1994]), and
consistently use V to denote a set of sorted ﬁrst-order variables. We use Σ(V) to denote the set of
sort-consistent interpretations of V. Given two interpretations 𝜎1 ∈ Σ(V1 ) and 𝜎2 ∈ Σ(V2 ) with
V1 ∩ V2 = ∅, we use 𝜎1 · 𝜎2 to denote the interpretation 𝜎 ∈ Σ(V1 ⊎ V2 ) such that 𝜎 (𝑣) = 𝜎1 (𝑣) for
𝑣 ∈ V1 and 𝜎 (𝑢) = 𝜎2 (𝑢) for 𝑢 ∈ V2 . We write 𝑣 ′ for the primed version of variable 𝑣, and deﬁne
V ′ := {𝑣 ′ : 𝑣 ∈ V}. Given 𝜎 ∈ Σ(V), we use 𝜎 ′ to denote the interpretation {𝑣 ′ ↦→ 𝜎 (𝑣) : 𝑣 ∈ V}
of V ′ . Given a formula 𝜙, we use 𝜙 [𝑡/𝑥] to denote the formula obtained by substituting 𝑡 for all free
occurrences of 𝑥 in 𝜙. Finally, for 𝜙 deﬁned over variables V, we let J𝜙K := {𝜎 ∈ Σ(V) : 𝜎 |= 𝜙 },
and write 𝜙 ≡ 𝜓 when J𝜙K = J𝜓 K.
Indexed array logic. An array theory typically combines two one-sorted theories: an index the-
ory, which is used to express relations between indices, and an element theory, which is used to
1 In this paper, array indices always start from 1. We use 𝑎[𝑖 ] to denote the 𝑖-th element of array 𝑎, and use |𝑎 | to denote

the size of 𝑎. We often use [𝑎 1 , . . . , 𝑎𝑛 ] to represent an unnamed array 𝑎 with |𝑎 | = 𝑛 and 𝑎[𝑖 ] = 𝑎𝑖 for 𝑖 ∈ {1, . . . , 𝑛}.


Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
Regular Abstractions for Array Systems                                                                             22:5


express properties of the array entries. The indexed array logic is a fragment of quantiﬁed array
theory that (i) uses Diﬀerence Arithmetic as the index theory, and (ii) allows quantiﬁcation only
over index variables. To make our expositions concrete, we shall focus on an instantiation of in-
dexed array logic that uses Diﬀerence Arithmetic as the element theory. (However, we note that
our abstraction techniques can be directly applied to any indexed array logic with a decidable
quantiﬁer-free fragment, which allows for a rich set of element theories such as Linear Integer
Arithmetic (cf. [Kroening and Strichman 2016]).)
  Throughout this paper, we shall ﬁx an indexed array logic T with syntax given by
             𝐼 ::= 𝐼 + 𝑛 | 𝑖 | 𝑛 | |𝑎|                                                   (index terms)
            𝐸 ::= 𝐸 + 𝑛 | 𝑣 | 𝑛 | 𝑎[𝐼 ]                                                  (data terms)
            𝐹 ::= 𝐼 ⊲⊳ 𝐼 | 𝐸 ⊲⊳ 𝐸 | ¬𝐹 | 𝐹 ∨ 𝐹 | 𝐹 ∧ 𝐹 | ∃𝑖. 𝐹 | ∀𝑖. 𝐹                   (formulae)
where ⊲⊳ ∈ {=, ≠, ≤, <, ≥, >}, 𝑛 is a concrete integer, 𝑣 is a data variable, 𝑖 is an index variable, 𝑎 is
an array variable, |𝑎| represents the array length of 𝑎, and 𝑎[𝐼 ] represents the array element of 𝑎
stored at position 𝐼 . A formula in form of 𝐼 ⊲⊳ 𝐼 or 𝐸 ⊲⊳ 𝐸 is called an atomic formula, or an atom for
short. We extend the logic with logical connectives such as ⇒ (implies) and ⇔ (if and only if) in
the usual way. An interpretation 𝜎 of a formula in the indexed array logic is intuitive: 𝜎 maps each
integer/index variable to an integer, and each array variable 𝑎 to a function 𝑓𝑎 : Z → Z. The notion
of satisfaction of a formula with respect to this interpretation is now standard. Although arrays are
inﬁnite, it is easy to conﬁne an array 𝑎 to a ﬁnite array by focusing on the index range {1, . . . , |𝑎|}.
For example, a formula ∀𝑖. 𝜙 (𝑖, 𝑎) can simply be rewritten to ∀𝑖. 1 ≤ 𝑖 ∧ 𝑖 ≤ |𝑎| ⇒ 𝜙 (𝑖, 𝑎).
First-order array system. A ﬁrst-order array system 𝔗 := (V, 𝜙 𝐼 , 𝜙𝑇 ) is a triple where V is a
ﬁnite set of ﬁrst-order variables, and 𝜙 𝐼 and 𝜙𝑇 are array formulae over variables V and V ⊎ V ′ ,
respectively. The variables in V are grouped into state variables and system parameters. A state
variable has either an index sort, an element sort, or an array sort. A system parameter is a special
index variable whose value is determined in an initial state and immutable during system execution.
For each array variable 𝑎 ∈ V, we identify a system parameter in V with the array size |𝑎|. This
eﬀectively stipulates that the array size is not changeable after the array is allocated.
   The semantics of an array system is determined by the array logic T and interpretations for
V. A state of an array system 𝔗 := (V, 𝜙 𝐼 , 𝜙𝑇 ) is a sort-consistent interpretation 𝑠 ∈ Σ(V) for
the variables in V. The formula 𝜙 𝐼 speciﬁes the set of initial states. The formula 𝜙𝑇 speciﬁes the
system’s evolution by relating the current variables V to their updated counterparts V ′ . A (ﬁnite
or inﬁnite) sequence 𝜋 := 𝑠 0 · · · 𝑠𝑛 of states with 𝑛 ∈ N∪ {𝜔 } is a path if 𝑠 0 |= 𝜙 𝐼 and 𝑠𝑖 −1·𝑠𝑖′ |= 𝜙𝑇 for
𝑖 ∈ {1, . . . , 𝑛}. Since system parameters are immutable, 𝜋 is a legitimate path only if 𝑠𝑖 −1 (𝑣) = 𝑠𝑖 (𝑣)
for all system parameters 𝑣 ∈ V and each 𝑖 ∈ {1, . . . , 𝑛}.
A guarded modeling language. We describe a simple guarded command language for specifying
transitions of array systems. While this language is less expressive than the full-ﬂedged array logic,
it is more concise and understandable, and is already expressive enough to capture all examples
considered in this paper. A guarded command is in form of guard ⊲ update. A command is en-
abled if its guard is satisﬁed. At each time step, the system nondeterministically selects an enabled
command and updates the current state accordingly. If no command is enabled, the system halts.
More precisely, a guarded command is in form of 𝜙 ⊲ 𝛽 1 , . . . , 𝛽𝑚 , where 𝜙 is a (possibly quantiﬁed)
array formula, and each 𝛽𝑖 is an assignment in one of the two forms:
    – 𝑥 := 𝐼 or 𝑥 := ∗, where 𝑥 is an index variable, 𝐼 is an index term, and ∗ is a special symbol;
    – 𝑎[𝐼 ] := 𝐸 or 𝑎[𝐼 ] := ∗, where 𝐼 is an index term, 𝐸 is a data term, and ∗ is a special symbol.
The assignments 𝛽 1, . . . , 𝛽𝑚 are executed in parallel. The symbol “∗” stands for a nondeterministic
value, which ranges over the index domain when the left-hand side is 𝑥, and ranges over the

                                Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
22:6                                                                               Chih-Duo Hong and Anthony W. Lin


data domain when the left-hand side is 𝑎[𝐼 ]. For simplicity, assignments to data variables are not
directly supported by our modeling language. This however is not an essential restriction, since
data variables can be formally translated to array elements stored at dedicated positions, thereby
allowing assignments as array elements.
   Example 3.1. The transitions of Dijkstra’s algorithm in the illustrative example may be given as
              𝑝𝑖𝑑 = 1 ∧ 𝑎[𝑝𝑖𝑑] = 𝑎[𝑛] ∧ 𝑎[𝑝𝑖𝑑] < 𝑘 − 1 ⊲ 𝑎[𝑝𝑖𝑑] := 𝑎[𝑝𝑖𝑑] + 1, 𝑝𝑖𝑑 := ∗
              𝑝𝑖𝑑 = 1 ∧ 𝑎[𝑝𝑖𝑑] = 𝑎[𝑛] ∧ 𝑎[𝑝𝑖𝑑] = 𝑘 − 1 ⊲ 𝑎[𝑝𝑖𝑑] := 0, 𝑝𝑖𝑑 := ∗
              𝑝𝑖𝑑 > 1 ∧ 𝑝𝑖𝑑 ≤ 𝑛 ∧ 𝑎[𝑝𝑖𝑑] ≠ 𝑎[𝑝𝑖𝑑 − 1] ⊲ 𝑎[𝑝𝑖𝑑] := 𝑎[𝑝𝑖𝑑 − 1], 𝑝𝑖𝑑 := ∗
The array system 𝔗 := (V, 𝜙 𝐼 , 𝜙𝑇 ) of Dijkstra’s algorithm is speciﬁed by
                     V := {𝑝𝑖𝑑, 𝑎, 𝑛, 𝑘}
                     𝜙 𝐼 := 2 ≤ 𝑛 ∧ 𝑛 ≤ 𝑘 ∧ (∀𝑖. 1 ≤ 𝑖 ∧ 𝑖 ≤ 𝑛 ⇒ 0 ≤ 𝑎[𝑖] ∧ 𝑎[𝑖] < 𝑘)
                    𝜙𝑇 := 𝜓 1 ∨ 𝜓 2 ∨ 𝜓 3
where 𝑝𝑖𝑑 is an index variable, 𝑎 is an array variable, 𝑛, 𝑘 are system parameters, and |𝑎| is identiﬁed
with 𝑛. The transition formula 𝜙𝑇 is deﬁned by three formulae 𝜓 1 , 𝜓 2 , and 𝜓 3 , which are in turn
derived from the three guarded commands listed above. For example, 𝜓 1 can be formally derived
from the ﬁrst command as 𝑝𝑖𝑑 = 1 ∧ 𝑎[𝑝𝑖𝑑] = 𝑎[𝑛] ∧ 𝑎[𝑝𝑖𝑑] < 𝑘 − 1 ∧ 𝑎 ′ [𝑝𝑖𝑑] = 𝑎[𝑝𝑖𝑑] + 1 ∧
1 ≤ 𝑝𝑖𝑑 ′ ∧ 𝑝𝑖𝑑 ′ ≤ 𝑛 ∧ (∀𝑖. 1 ≤ 𝑖 ∧ 𝑖 ≤ 𝑛 ∧ 𝑖 ≠ 𝑝𝑖𝑑 ⇒ 𝑎 ′ [𝑖] = 𝑎[𝑖]).                                

4 REGULAR LANGUAGES AS ABSTRACTIONS
In this section, we deﬁne a novel predicate abstraction of array formulae and array systems using
indexed predicates. Since each array will be mapped to a word (over a ﬁnite alphabet) in the ab-
straction, we shall use regular languages to represent sets of words, and use regular relations to
represent relations over words. We start by recalling a logical framework of regular relations.

4.1    A First-Order Framework of Regular Relations
Let Σ𝑚 := {0, 1}𝑚 denote the set of bitvectors of length 𝑚. For 𝑚 ≥ 1, we deﬁne a two-sorted
structure2 𝔖𝑚 := (Σ𝑚  ∗ , N, 𝑠𝑢𝑐𝑐, 𝑝𝑟𝑒𝑑, ·[·], |·|, Δ , . . . , Δ ), where Σ∗ := {𝑣 · · · 𝑣 : 𝑛 ≥ 0 and
                                                       1         𝑚          𝑚       1      𝑛
𝑣 𝑖 ∈ Σ𝑚 for each 𝑖} are words over bitvectors; 𝑠𝑢𝑐𝑐, 𝑝𝑟𝑒𝑑 : N → N are deﬁned by 𝑠𝑢𝑐𝑐 (𝑛) := 𝑛 + 1
and 𝑝𝑟𝑒𝑑 (𝑛) := max{0, 𝑛 − 1}, respectively; |·| : Σ𝑚    ∗ → N is word length (i.e. |𝑤 | is the length
               ∗
of 𝑤); ·[·] : Σ𝑚 × N → Σ𝑚 oﬀers letter-level access for words, i.e., 𝑤 [𝑖] is the 𝑖th letter of 𝑤 for
1 ≤ 𝑖 ≤ |𝑤 |; each Δ𝑘 ⊆ N × Σ𝑚 ∗ oﬀers bit-level access for words, such that (𝑖, 𝑤) ∈ Δ if and only if
                                                                                           𝑘
1 ≤ 𝑖 ≤ |𝑤 | and the 𝑘th bit of 𝑤 [𝑖] is 1. We shall use 𝑛 + 𝑘 and 𝑛 − 𝑘 as syntactic sugar for 𝑠𝑢𝑐𝑐 𝑘 (𝑛)
and 𝑝𝑟𝑒𝑑 𝑘 (𝑛), respectively.
    Given two words 𝑤 1 ∈ Σ𝑚  ∗ and 𝑤 ∈ Σ∗ , we deﬁne the convolution 𝑤 ⊙ 𝑤 of 𝑤 and 𝑤 as
                                1        2    𝑚2                                1      2     1        2
                 ∗
the word 𝑤 ∈ Σ𝑚1 +𝑚2 such that |𝑤 | = max{|𝑤 1 |, |𝑤 2 |} and
                                    
                                    𝑤 [𝑖] :: 𝑤 2 [𝑖], 1 ≤ 𝑖 ≤ min{|𝑤 1 |, |𝑤 2 |};
                                     1
                                    
                                    
                             𝑤 [𝑖] = 0𝑚1 :: 𝑤 2 [𝑖],   |𝑤 1 | < 𝑖 ≤ |𝑤 2 |;                                     (1)
                                    
                                    
                                    𝑤 1 [𝑖] :: 0𝑚2 ,  |𝑤 2 | < 𝑖 ≤ |𝑤 1 |,
                                    
where 𝑢 :: 𝑣 denotes the concatenation of the bitvectors 𝑢 and 𝑣. Intuitively, 𝑤 1 ⊙ 𝑤 2 is obtained
by juxtaposing 𝑤 1 and 𝑤 2 (in a left-aligned manner), and padding the shorter word with enough
2We   note that this structure is equally expressive in ﬁrst-order logic to the so-called universal automatic struc-
tures [Benedikt et al. 2003; Blumensath and Grädel 2004; Colcombet and Löding 2007].


Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
Regular Abstractions for Array Systems                                                                            22:7


0s. For example, for two words 01, 0001 over Σ1 , 01 ⊙ 0001 is the word (0, 0) (1, 0) (0, 0) (0, 1) over
Σ2 . We lift ⊙ to languages by deﬁning 𝐿1 ⊙ 𝐿2 := {𝑤 1 ⊙ 𝑤 2 : 𝑤 1 ∈ 𝐿1 , 𝑤 2 ∈ 𝐿2 }.
   We say that a relation is regular if its language representation is regular under unary encoding.
Formally, suppose w.l.o.g. that 𝑅 ⊆ N𝑟 × (Σ𝑚               ∗ )𝑙 . We deﬁne the language representation of 𝑅 as

L (𝑅) := {𝑤 1 ⊙ · · · ⊙ 𝑤 𝑟 +𝑙 ∈ Σ𝑟 + 𝑙 ·𝑚 : (𝑤 1, . . . , 𝑤 𝑟 +𝑙 ) ∈ 𝑅} by identifying each 𝑛 ∈ N with 1𝑛 ∈ Σ∗1 .
                                  ∗

The following result states that a relation is regular if and only if it is ﬁrst-order deﬁnable in 𝔖𝑚 ,
see e.g., [Benedikt et al. 2003; Blumensath and Grädel 2004; Colcombet and Löding 2007].
    Proposition 4.1. Given a ﬁrst-order formula 𝜙 deﬁned over 𝔖𝑚 , we can compute a ﬁnite automa-
ton recognizing L (J𝜙K). Conversely, given a ﬁnite automaton recognizing L ⊆ 𝑁 1 ⊙ · · · ⊙ 𝑁𝑟 ⊙ 𝐿1 ⊙
· · · ⊙ 𝐿𝑙 , where 𝑁𝑖 ⊆ 1∗ and 𝐿𝑖 ⊆ Σ𝑚
                                     ∗ for each 𝑖, we can compute a ﬁrst-order formula 𝜙 over 𝔖 such
                                                                                               𝑚
that L = L (J𝜙K).

4.2   Abstraction of Array Formulae
We use indexed predicates to express constraints on arrays.
  Deﬁnition 4.2 (Indexed predicate). An indexed predicate is an atom (in the indexed array logic)
containing a designated index variable i. A set of indexed predicates P := h𝑃1 , . . . , 𝑃𝑚 i is said to
be deﬁned over variables V if each predicate 𝑃𝑘 ∈ P is deﬁned over variables V ⊎ {i}.
  For convenience, we shall ﬁx a set of variables V and a set of indexed predicates P := h𝑃1 , . . . , 𝑃𝑚 i
over variables V throughout the rest of this section. For each bitvector 𝑣 := 𝑏 1 · · · 𝑏𝑚 ∈ Σ𝑚 com-
prising 𝑚 bits, we deﬁne a quantiﬁer-free array formula 𝜙 𝑣P over variables V ⊎ {i} as follows:
                                                        (
                             Û                            𝑃𝑘 ,    𝑏𝑘 = 1;
                        P
                      𝜙 𝑣 :=             ˜          ˜
                                        𝑃𝑘 , where 𝑃𝑘 =                                                 (2)
                                1≤𝑘 ≤𝑚                    ¬𝑃𝑘 , 𝑏𝑘 = 0.
Formula 𝜙 𝑣P eﬀectively regards each bit 𝑏𝑘 of the bitvector 𝑣 as the truth value of predicate 𝑃𝑘 at
the parametric position i. We furthermore use a word over bitvectors to encode the truth values
of the predicates ranging over an interval of positions: for each word 𝑤 ∈ Σ𝑚 ∗ , we deﬁne an array

formula                                   Û
                                   Φ𝑤P :=            𝜙 𝑤P[𝑖 ] [𝑖/i].                             (3)
                                                    1≤𝑖 ≤ |𝑤 |
For example, if P = h𝑥 [i] = 𝑥 [𝑛], 𝑥 [i] ≠ 𝑥 [i − 1]i and 𝑤 = [10, 01], then Φ𝑤P is 𝑥 [1] = 𝑥 [𝑛] ∧
¬(𝑥 [1] ≠ 𝑥 [0]) ∧ ¬(𝑥 [2] = 𝑥 [𝑛]) ∧ 𝑥 [2] ≠ 𝑥 [1]. By construction, for 𝜎 ∈ Σ(V), 𝜎 |= Φ𝑤P holds if
and only if for 𝑖 ∈ {1, . . . , |𝑤 |} and 𝑘 ∈ {1, . . . , 𝑚}, the truth value of 𝜎 |= 𝑃𝑘 [𝑖/i] coincides with
the 𝑘th bit of the bitvector 𝑤 [𝑖].
   Fix an array system 𝔗 := (V, 𝜙 𝐼 , 𝜙𝑇 ). Let V𝑖𝑛𝑡 denote the set of parameters and index variables
in V, and V𝑝𝑎𝑟 denote the set of parameters in V. Let 𝑟 := |V𝑖𝑛𝑡 | and 𝑚 := |P |. We shall identify
an interpretation 𝜎 ∈ Σ(V𝑖𝑛𝑡 ) with an 𝑟 -tuple (𝜎 (𝑥 1 ), . . . , 𝜎 (𝑥𝑟 )) ∈ N𝑟 where 𝑥𝑖 denotes the 𝑖th
variable in V𝑖𝑛𝑡 . We deﬁne the concrete domain of the system as Σ(V), and the abstract domain
as N𝑟 × Σ𝑚 ∗ . Each abstract state (𝑡, 𝑤) ∈ N𝑟 × Σ∗ comprises a tuple 𝑡 ∈ N𝑟 representing an
                                                             𝑚
interpretation of V𝑖𝑛𝑡 , and a word 𝑤 ∈ Σ𝑚     ∗ encoding the valuations of P at positions 1, . . . , |𝑤 |.

   Given a set 𝑆𝐶 ⊆ Σ(V) of concrete states, we deﬁne
      𝛼 P (𝑆𝐶 ) := {(𝑠𝑖𝑛𝑡 , 𝑤) ∈ N𝑟 × Σ𝑚
                                       ∗
                                         : there exists 𝑠 ∈ 𝑆𝐶 s.t. |𝑤 | = max 𝑠 (𝑥) and 𝑠 |= Φ𝑤P }.
                                                                                𝑥 ∈ V𝑝𝑎𝑟
                                                                                                 ∗
Here, 𝑠𝑖𝑛𝑡 denotes the interpretation obtained by restricting 𝑠 to V𝑖𝑛𝑡 . Given a set 𝑆𝐴 ⊆ N𝑟 × Σ𝑚
of abstract states, we deﬁne
   𝛾 P (𝑆𝐴 ) := {𝑠 ∈ Σ(V) : for all 𝑤 ∈ Σ𝑚
                                         ∗ s.t. |𝑤 | = max 𝑠 (𝑥), 𝑠 |= Φ P implies (𝑠 , 𝑤) ∈ 𝑆 }.
                                                                        𝑤            𝑖𝑛𝑡      𝐴
                                                             𝑥 ∈ V𝑝𝑎𝑟


                               Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
22:8                                                                               Chih-Duo Hong and Anthony W. Lin


Notice that 𝛼 P (𝑆𝐶 ) and 𝛾 P (𝑆𝐴 ) are computable when 𝑆𝐶 and 𝑆𝐴 are ﬁnite. To simplify the notation,
we may omit the superscript P from 𝛼 P and 𝛾 P when it is clear from the context. Also, for a
single state 𝑠, we shall write 𝛼 (𝑠) and 𝛾 (𝑠) instead of 𝛼 ({𝑠}) and 𝛾 ({𝑠}) when there is no danger
of ambiguity. Finally, for a formula 𝜙, we shall write 𝛼 (𝜙) and 𝛾 (𝜙) instead of 𝛼 (J𝜙K) and 𝛾 (J𝜙K).
  Example 4.3. Recall the illustrative example in Section 2. With indexed predicates P := h𝑎[i] =
𝑎[𝑛], 𝑎[i] = 𝑎[i − 1]i, we can deﬁne 𝛼 and 𝛾 as
 𝛼 (𝑆𝐶 ) := {(𝑝𝑖𝑑, 𝑛, 𝑤) ∈ N2 × Σ∗2 : there exists (𝑝𝑖𝑑, 𝑛, 𝑎) ∈ 𝑆𝐶 s.t. |𝑤 | = 𝑛 and (𝑝𝑖𝑑, 𝑛, 𝑎) |= Φ𝑤P };
  𝛾 (𝑆𝐴 ) := {(𝑝𝑖𝑑, 𝑛, 𝑎) ∈ N2 × Z𝜔 : for all 𝑤 ∈ Σ𝑛2 , (𝑝𝑖𝑑, 𝑛, 𝑎) |= Φ𝑤P implies (𝑝𝑖𝑑, 𝑛, 𝑤) ∈ 𝑆𝐴 }.
For instance, given a concrete state 𝑠 := (1, 3, [1, 2, 1]), we can compute 𝛼 (𝑠) = {(1, 3, [10, 00, 10]),
(1, 3, [11, 00, 10])} and 𝛾 (𝛼 (𝑠)) = {(1, 3, 𝑎) : 𝑎 ∈ Z𝜔 , 𝑎[1] = 𝑎[3] ≠ 𝑎[2]}.                           
                                                                                                  Ð
   Lemma 4.4. For a countable collection {𝑆𝑖 : 𝑖 ∈ 𝐼 } of concrete state sets, it holds that 𝛼 ( 𝑖 ∈𝐼 𝑆𝑖 ) =
Ð                     Ñ            Ñ
  𝑖 ∈𝐼 𝛼 (𝑆𝑖 ) and 𝛼 ( 𝑖 ∈𝐼 𝑆𝑖 ) ⊆  𝑖 ∈𝐼 𝛼 (𝑆𝑖 ).
                                                                                Ð
   Proof.
     Ñ        Note that 𝛼 distributes
                                 Ñ       over union byÑdeﬁnition,                             Also, note that
                                                                 Ði.e., 𝛼 (𝑆) = Ñ 𝑠 ∈𝑆 𝛼 (𝑠). Ñ
𝑠 ∈ 𝑖 ∈𝐼 𝑆𝑖 implies 𝛼 (𝑠) ⊆ 𝑖 ∈𝐼 𝛼 (𝑆𝑖 ). Thus, 𝛼 ( 𝑖 ∈𝐼 𝑆𝑖 ) = {𝛼 (𝑠) : 𝑠 ∈ 𝑖 ∈𝐼 𝑆𝑖 } ⊆ 𝑖 ∈𝐼 𝛼 (𝑆𝑖 ). 
   Lemma 4.5. For any abstract state set 𝑆𝐴 , it holds that 𝛾 (𝑆𝐴 ) = {𝑠 : 𝛼 (𝑠) ⊆ 𝑆𝐴 }.
   Proof. It suﬃces to ﬁx a concrete state 𝑠 and show that 𝑠 ∈ 𝛾 (𝑆𝐴 ) ⇐⇒ 𝛼 (𝑠) ⊆ 𝑆𝐴 . For
the “⇒” direction, assume that 𝑠 ∈ 𝛾 (𝑆𝐴 ), and let (𝑠𝑖𝑛𝑡 , 𝑤) be an abstract state in 𝛼 (𝑠). Then we
have 𝑠 |= Φ𝑤P by the deﬁnition of 𝛼, which implies that (𝑠𝑖𝑛𝑡 , 𝑤) ∈ 𝑆𝐴 by the deﬁnition of 𝛾. Since
(𝑠𝑖𝑛𝑡 , 𝑤) is arbitrary, we conclude that 𝛼 (𝑠) ⊆ 𝑆𝐴 . For the “⇐” direction, assume that 𝛼 (𝑠) ⊆ 𝑆𝐴 .
Let 𝑊𝑠 := {𝑤 ∈ Σ𝑚    ∗ : |𝑤 | = max
                                   𝑥 ∈ V𝑝𝑎𝑟 𝑠 (𝑥)}. By the deﬁnition of 𝛼, 𝑆𝐴 contains all abstract states
(𝑠𝑖𝑛𝑡 , 𝑤) such that 𝑤 ∈ 𝑊𝑠 and 𝑠 |= Φ𝑤P . However, this implies that for any 𝑤 ∈ 𝑊𝑠 , if 𝑠 |= Φ𝑤P holds,
then (𝑠𝑖𝑛𝑡 , 𝑤) ∈ 𝑆𝐴 also holds. It follows that 𝑠 ∈ 𝛾 (𝑆𝐴 ) by the deﬁnition of 𝛾.                      
  The following result is a consequence of Lemma 4.4, Lemma 4.5, and Proposition 7 of [Cousot and Cousot
1977]. We provide a proof here for the sake of completeness.
   Proposition 4.6. For any concrete state set 𝑆𝐶 and abstract state set 𝑆𝐴 , it holds that
                                        𝛼 (𝑆𝐶 ) ⊆ 𝑆𝐴 ⇐⇒ 𝑆𝐶 ⊆ 𝛾 (𝑆𝐴 ).
   Proof. For the “⇒” direction, assume that 𝛼 (𝑆𝐶 ) ⊆ 𝑆𝐴 . Since 𝛼 is monotonic, i.e., 𝐸 ⊆ 𝐹 implies
𝛼 (𝐸) ⊆ 𝛼 (𝐹 ), we have 𝛼 (𝑠) ⊆ 𝑆𝐴 for every 𝑠 ∈ 𝑆𝐶 . By Lemma 4.5, we have 𝛾 (𝑆𝐴 ) = {𝑠 : 𝛼 (𝑠) ⊆
𝑆𝐴 }. It then follows that 𝑆𝐶 ⊆ 𝛾 (𝑆𝐴 ). For the “⇐” direction, assume that 𝑆𝐶 ⊆ 𝛾 (𝑆𝐴 ). Again by
Lemma 4.5, we have 𝛾 (𝑆𝐴 ) = {𝑠 : 𝛼 (𝑠) ⊆ 𝑆𝐴 }. The assumption 𝑆𝐶 ⊆ 𝛾 (𝑆𝐴 ) thus implies that
𝛼 (𝑠) ⊆ 𝑆𝐴 for every 𝑠 ∈ 𝑆𝐶 . This in turn implies that 𝛼 (𝑆𝐶 ) ⊆ 𝑆𝐴 by Lemma 4.4.                  

4.3    Abstract Safety and Liveness Analysis
For an array system 𝔗 := (V, 𝜙 𝐼 , 𝜙𝑇 ), applying predicate abstraction for safety and liveness veriﬁ-
cation involves performing reachability analysis for the abstract system of 𝔗. In each step of the
analysis, we concretize the current set of reachable abstract states via the concretization operation
𝛾, apply the concrete next-step function
                     𝑁𝐶 (𝑆𝐶 ) := {𝑡 ∈ Σ(V) : there exists 𝑠 ∈ 𝑆𝐶 such that 𝑠 ·𝑡 ′ |= 𝜙𝑇 }                       (4)
in the concrete state space, and map the result back to the abstract state space via the abstraction
operation 𝛼. We can view this process as performing state exploration in an abstract transition
system with a set 𝛼 (𝜙 𝐼 ) of initial states and an abstract next-step function
                                            𝑁𝐴 (𝑆𝐴 ) := 𝛼 (𝑁𝐶 (𝛾 (𝑆𝐴 ))).                                       (5)

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
Regular Abstractions for Array Systems                                                                             22:9


Proposition 4.6, together with the fact that 𝛼, 𝛾, and 𝑁𝐶 are monotonic, establishes the soundness
of abstract reachability analysis using 𝑁𝐴 (cf. [Cousot and Cousot 1977]). For example, let Π(𝐼,𝑇 )
denote the set of paths starting from states in 𝐼 through transition relation 𝑇 , and let 𝑠𝑡 (𝜋) denote
the set of states in path 𝜋. Given a set 𝐼𝑛𝑖𝑡 of initial states and a set 𝐵𝑎𝑑 of bad states, one can show
(e.g. by induction on the length of a counterexample path) that the safety property
                                      ∀𝜋 ∈ Π(𝐼𝑛𝑖𝑡, 𝑁𝐶 ). 𝑠𝑡 (𝜋) ∩ 𝐵𝑎𝑑 = ∅                                          (6)
holds in the concrete domain if ∀𝜋 ∈ Π(𝛼 (𝐼𝑛𝑖𝑡), 𝑁𝐴 ). 𝑠𝑡 (𝜋) ∩ 𝛼 (𝐵𝑎𝑑) = ∅ holds in the abstract
domain. Similarly, given a set 𝐹𝑖𝑛 of ﬁnal states, the liveness property
                                      ∀𝜋 ∈ Π(𝐼𝑛𝑖𝑡, 𝑁𝐶 ). 𝑠𝑡 (𝜋) ∩ 𝐹𝑖𝑛 ≠ ∅                                          (7)
holds in the concrete domain if ∀𝜋 ∈ Π(𝛼 (𝐼𝑛𝑖𝑡), 𝑁𝐴 ). 𝑠𝑡 (𝜋) ∩ 𝛼 (𝐹𝑖𝑛 c ) c ≠ ∅ holds in the abstract
domain,where 𝑆 c denotes the complement of the concrete (resp. abstract) state set 𝑆 with respect to
the concrete (resp. abstract) state space. These facts allow us to reduce the veriﬁcation of concrete
safety/liveness properties to that of their counterparts in the abstract domain.

4.4   Approximation with Regular Languages
Since indexed array logic is undecidable, the abstraction 𝛼 (𝜙) of an indexed array formula 𝜙 is
generally not computable. Therefore, we propose to overapproximate these formulae in the ab-
stract domain using regular languages. As before, ﬁx a set V of variables and a set P of indexed
predicates over V, and let 𝑟 := |V𝑖𝑛𝑡 | and 𝑚 := |P |. Then V and P induce an abstract domain
N𝑟 × Σ𝑚 ∗ . Recall that we regard a relation 𝑅 as regular when 𝑅’s language representation L (𝑅) is

regular.
  Deﬁnition 4.7 (Regular abstraction for state formulae). Let 𝜙 be an indexed array formula over
                                                                            ∗ is a regular relation
variables V. Then a tuple (𝑅, P) is a regular abstraction of 𝜙 if 𝑅 ⊆ N𝑟 × Σ𝑚
           P
such that 𝛼 (𝜙) ⊆ 𝑅.
    For P := h𝑃1 , . . . , 𝑃𝑚 i over V, we use P ∗ P ′ := h𝑃1 , . . . , 𝑃𝑚 , 𝑃𝑚+1 , . . . , 𝑃2𝑚 i to denote the set of
predicates over V ⊎ V ′ such that for 𝑘 ∈ {1, . . . , 𝑚}, 𝑃𝑚+𝑘 is obtained from 𝑃𝑘 by replacing 𝑣 with
𝑣 ′ for each variable 𝑣 ∈ V. Recall that 𝑠·𝑡 denotes the union of interpretations 𝑠 and 𝑡 over disjoint
variables, and that 𝑢 ⊙ 𝑣 denotes the convolution of words 𝑢 and 𝑣.
   Deﬁnition 4.8 (Regular abstraction for transition formulae). Let 𝜙 be an indexed array formula
                                                                                       ∗ ) × (N𝑟 ×Σ∗ )
over variables V ⊎V ′ . Then a tuple (𝑅, P) is a regular abstraction of 𝜙 if 𝑅 ⊆ (N𝑟 ×Σ𝑚           𝑚
                                    P∗P ′
is a regular relation such that 𝛼         (𝜙) ⊆ 𝜏 (𝑅), where 𝜏 is an isomorphic mapping deﬁned by
𝜏 ((𝑠, 𝑢), (𝑡, 𝑣)) = (𝑠 ·𝑡, 𝑢 ⊙ 𝑣).
  A regular abstraction (𝑅, P) of a transition formula induces a next-step function 𝑁𝑅 , deﬁned
by 𝑁𝑅 (𝑆𝐴 ) := {𝑡 : there exists 𝑠 ∈ 𝑆𝐴 such that (𝑠, 𝑡) ∈ 𝑅}, over the abstract state sets. It can be
shown that 𝑁𝑅 provides an abstract interpretation [Cousot and Cousot 1977] of the concrete array
system.
 Theorem 4.9. Let 𝔗 := (V, 𝜙 𝐼 , 𝜙𝑇 ) be an array system and P be a set of indexed predicates over
V. If (𝑅, P) is a regular abstraction of 𝜙𝑇 , then 𝑁𝑅 provides an abstract interpretation of 𝔗.
   Proof. To show that 𝑁𝑅 is an abstract interpretation, we need to check that (1) 𝑁𝑅 is monotonic;
(2) 𝑁𝑅 is null-preserving, namely, 𝑁𝑅 (∅) = ∅; (3) 𝑁𝑅 simulates 𝑁𝐶 w.r.t. a simulation relation
deﬁned by 𝛼, namely, 𝛼 (𝑁𝐶 (𝑆𝐶 )) ⊆ 𝑁𝑅 (𝛼 (𝑆𝐶 )). The ﬁrst two conditions directly follow from the
deﬁnition of regular abstraction, so it suﬃces to check the last condition. Suppose ﬁrst that 𝑆𝐶 = ∅.

                                Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
22:10                                                                              Chih-Duo Hong and Anthony W. Lin


Since 𝑁𝐶 (∅) = 𝛼 (∅) = 𝑁𝑅 (∅) = ∅, the condition holds trivially. Now suppose that 𝑆𝐶 ≠ ∅ and
consider an arbitrary state 𝑠 ∈ 𝑆𝐶 . Observe that
                    𝛼 (𝑁𝐶 (𝑠)) = 𝛼 ({𝑡 ∈ Σ(V) : 𝑠 ·𝑡 ′ |= 𝜙𝑇 })
                                = {(𝑡𝑖𝑛𝑡 , 𝑣) : 𝑠 ·𝑡 ′ |= 𝜙𝑇 , |𝑣 | = max𝑥 ∈ V𝑝𝑎𝑟 𝑡 (𝑥), 𝑡 |= Φ𝑣P }
                                ⊆ 𝑁𝑅 ({(𝑠𝑖𝑛𝑡 , 𝑢) : |𝑢| = max𝑥 ∈ V𝑝𝑎𝑟 𝑠 (𝑥), 𝑠 |= Φ𝑢P })
                                = 𝑁𝑅 (𝛼 (𝑠)),
where the inclusion in the third line follows from the deﬁnition of regular abstraction and the
stipulation that parameters are immutable. Note that 𝑁𝐶 , 𝑁𝑅 , and 𝛼 are all distributive over union.
                                                   Ð                  Ð
Since 𝑠 is arbitrary in 𝑆𝐶 , we have 𝛼 (𝑁𝐶 (𝑆𝐶 )) = 𝑠 ∈𝑆𝐶 𝛼 (𝑁𝐶 (𝑠)) ⊆ 𝑠 ∈𝑆𝐶 𝑁𝑅 (𝛼 (𝑠)) = 𝑁𝑅 (𝛼 (𝑆𝐶 )).
                                                                                                     
   Finally, a regular abstraction can be computed by composing smaller regular abstractions. This
fact is an immediate consequence of Lemma 4.4.
   Proposition 4.10. Let 𝜙 1, . .Ð   . , 𝜙𝑛 be indexed array formulae, and (𝑅Ô𝑖 , P) be a regularÑ𝑛 abstraction
                                        𝑛                                        𝑛
of 𝜙𝑖 for 𝑖 ∈ {1, . . . , 𝑛}.
                           Ó  Then (    𝑖=1 𝑅𝑖 , P) is a regular abstraction of  𝑖=1 𝜙 𝑖 , and (  𝑖=1 𝑅𝑖 , P) is a
regular abstraction of 𝑛𝑖=1 𝜙𝑖 .

5   COMPUTATION OF REGULAR ABSTRACTIONS
We have proposed to overapproximate indexed predicate abstractions with regular abstractions.
However, it remains unclear how to ﬁnd such approximations that are suﬃciently precise for a
veriﬁcation task. In this section, we address this issue by providing an automated procedure to
compute regular abstractions for a fragment of array logic called singly indexed array formulae.
In a nutshell, give such a formula 𝜙 := 𝛿𝑥 1 · · · 𝛿𝑥𝑛 . 𝜑, we compute an overapproximation of 𝜙 by
replacing the matrix 𝜑 of 𝜙 with a quantiﬁer-free formula 𝜑˜ such that 𝜑 ⇒ 𝜑˜ is valid. We shall
choose 𝜑˜ in such a way that the resulting formula 𝛿𝑥 1 · · · 𝛿𝑥𝑛 . 𝜑,
                                                                     ˜ called an abstraction formula,
can be faithfully encoded as a ﬁrst-order formula over an automatic structure. This encoding is
equally expressive to regular languages, and can be conveniently manipulated using tools such as
Mona [Klarlund and Møller 2001; Klarlund et al. 2002] and Gaston [Fiedor et al. 2017] for abstract
analysis.

5.1 Singly Indexed Array Formulae
An atomic indexed array formula is a data expression if it contains an array variable; otherwise it
is an index expression. A singly indexed array (SIA) formula is an indexed array formula in which
every data expression contains at most one quantiﬁed index variable. The satisﬁability problem of
SIA formulae is already undecidable when the element theory is instantiated to Diﬀerence Arith-
metic [Habermehl et al. 2008, Lemma 5]. Note that an SIA formula can be syntactically rewritten
to a logically equivalent SIA formula where every data expression has exactly one quantiﬁed index
variable — hence the name “singly indexed”. For example, a data expression 𝑎[1] ≠ 𝑏 [𝑛] in an SIA
formula can be replaced with ∃𝑖. 𝑖 = 1 ∧ 𝑎[𝑖] ≠ 𝑏 [𝑛] to obtain an equivalent SIA formula. We shall
assume an SIA formula to have this form when we are computing a regular abstraction for the
formula.

5.2 A Constraint-Based Abstraction Procedure
We need a couple more deﬁnitions before we introduce our abstraction method. As before, ﬁx
a set V of variables and a set P := h𝑃1 , . . . , 𝑃𝑚 i of indexed predicates over V. A formula over
V is expressible in P if each atom of the formula is either an index expression or an expression

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
Regular Abstractions for Array Systems                                                                          22:11


of form 𝑃 [𝑡/i] or ¬𝑃 [𝑡/i], where 𝑡 is an index term and 𝑃 is a predicate in P. For a formula 𝜙
expressible in P, we shall use 𝜅 P (𝜙) to denote the formula obtained by replacing each atom 𝑃𝑘 [𝑡/i]
(resp. ¬𝑃𝑘 [𝑡/i]) in 𝜙 with 𝜓 ⇒ Δ𝑘 (𝑡, 𝑤) (resp. 𝜓 ⇒ ¬Δ𝑘 (𝑡, 𝑤)), where 𝜓 encodes the boundary
check for 𝑃𝑘 [𝑡/i]. For example, suppose that 𝜙 = ∀𝑖. 𝑎[𝑖] ≤ 𝑏 [𝑝] and that 𝑃1 = 𝑎[i] > 𝑏 [𝑝] is a
predicate in P. Then 𝜅 P (𝜙) = ∀𝑖. (1 ≤ 𝑖 ∧ 𝑖 ≤ |𝑎| ∧ 1 ≤ 𝑝 ∧ 𝑝 ≤ |𝑏 | ⇒ ¬Δ1 (𝑖, 𝑤)). Note that 𝜅 P (𝜙)
is deﬁned over structure 𝔖𝑚 and variables V𝑖𝑛𝑡 ⊎ {𝑤 }. Speciﬁcally, the free variables of 𝜅 P (𝜙)
comprise the index variables and parameters of 𝜙, as well as a fresh word variable 𝑤 over domain
Σ𝑚∗ . We may simply write 𝜅 P (𝜙) as 𝜅 (𝜙) when P is clear from the context.

   Now we are ready to describe our abstraction method. Consider a singly indexed Ô formula 𝜙 over
V. Suppose w.l.o.g. that the matrix of 𝜙 is given in disjunctive normal form 𝑗 (𝑔 𝑗 ∧ ℎ 𝑗 ), where
each 𝑔 𝑗 is a conjunction of index expressions, and each ℎ 𝑗 is a conjunction of data expressions. Our
procedure computes a regular abstraction for 𝜙 in two steps:
Step 1: Replace each ℎ 𝑗 in 𝜙 with a formula cstr(ℎ 𝑗 ), where cstr(𝜓 ) denotes the conjunction of
        disjunctive clauses deﬁned by
                                  Û
                      cstr(𝜓 ) :=   {𝐶 ⊆ 𝐴(𝜓, P) : 𝜓 ⇒ 𝐶 is valid in T } ,                     (8)

        and 𝐴(𝜓, P) := {𝑃𝑘 [𝑡/i], ¬𝑃𝑘 [𝑡/i] : 𝑃𝑘 ∈ P, and 𝑡 is an index term of 𝜓 or P}. Intuitively,
        cstr(𝜓 ) attempts to express in P the necessary conditions for a concrete state to satisfy 𝜓 .
        Note that 𝐴(𝜓, P) is ﬁnite, and hence cstr(𝜓 ) is computable by our assumption on T .
Step 2: Let 𝜙 ∗ denote the formula obtained by replacing each ℎ 𝑗 with cstr(ℎ 𝑗 ). This formula 𝜙 ∗ ,
        which we shall refer to as the abstraction formula of 𝜙, is expressible in P. We then deﬁne
        𝜙 P = 𝜙 P (𝜎, 𝑤) := 𝜅 P (𝜙 ∗ ), and use (J𝜙 P K, P) as a regular abstraction for 𝜙.
   Note that when computing cstr(𝜓 ), we can exclude a clause 𝐶 if 𝜅 P (𝐶) is valid in 𝔖𝑚 (e.g. when
{𝑓 , ¬𝑓 } ⊆ 𝐶 for some atom 𝑓 ), since such a clause imposes no restrictions on the abstract states.
Furthermore, it suﬃces to consider the minimal clauses 𝐶 satisfying 𝜓 ⇒ 𝐶. Thus, we can reduce
                                                                                           Ó
the computation of cstr(𝜓 ) to enumerating the minimal unsatisﬁable cores (MUCs) of𝜓 ∧ 𝐴(𝜓, P),
as negating such a core essentially leads to a minimal feasible clause of cstr(𝜓 ). There are rich tool
supports for MUC enumeration in the literature, see e.g. [Bendík and Černá 2020; Bendík et al.
2018; Liﬃton et al. 2016]. In practice, it is often possible to compute cstr(𝜓 ) incrementally and
obtain a precise enough abstraction without including all MUCs in the abstraction formula. We
shall discuss these optimizations in Section 8.
   Example 5.1. As an illustration, let us use our abstraction method to prove that there always
exists at least one privileged process in Dijkstra’s self-stabilizing algorithm (cf. Example 3.1). Con-
sider the singly indexed array formula
    𝜙 := ∀𝑖. (𝑖 = 1 ∧ 𝑖 < 𝑛 ∧ 𝑎[𝑖] ≠ 𝑎[𝑛]) ∨ (𝑖 > 1 ∧ 𝑖 ≤ 𝑛 ∧ 𝑎[𝑖] = 𝑎[𝑖 − 1]) ∨ (𝑖 > 𝑛 ∧ 𝑛 ≥ 2),
which expresses that no process is privileged in a system containing 𝑛 ≥ 2 processes. We shall
compute a regular abstraction of 𝜙 using indexed predicates P := h𝑎[i] = 𝑎[𝑛], 𝑎[i] = 𝑎[i − 1]i,
which comprises the atomic formulae of 𝜙. The ﬁrst step computes the abstraction formula 𝜙 ∗ as
∀𝑖. (𝑖 = 1 ∧ 𝑖 < 𝑛 ∧ cstr(𝑎[𝑖] ≠ 𝑎[𝑛])) ∨ (𝑖 > 1 ∧ 𝑖 ≤ 𝑛 ∧ cstr(𝑎[𝑖] = 𝑎[𝑖 − 1])) ∨ (𝑖 > 𝑛 ∧ 𝑛 ≥ 2).
The nontrivial minimal feasible clauses for cstr(𝑎[𝑖] ≠ 𝑎[𝑛]) are {𝑎[𝑛] = 𝑎[𝑛]}, {𝑎[𝑖] ≠ 𝑎[𝑛]}, and
{𝑎[𝑖] ≠ 𝑎[𝑖 − 1], 𝑎[𝑖 − 1] ≠ 𝑎[𝑛]}. (We call a clause 𝐶 trivial if 𝜅 (𝐶) is valid in 𝔖𝑚 .) Similarly, the
nontrivial minimal feasible clauses for cstr(𝑎[𝑖] = 𝑎[𝑖 − 1]) are {𝑎[𝑛] = 𝑎[𝑛]}, {𝑎[𝑖] = 𝑎[𝑖 − 1]},
{𝑎[𝑖] = 𝑎[𝑛], 𝑎[𝑖 − 1] ≠ 𝑎[𝑛]}, and {𝑎[𝑖] ≠ 𝑎[𝑛], 𝑎[𝑖 − 1] = 𝑎[𝑛]}. From these clauses, we then
compute a regular abstraction of 𝜙 as 𝜙 P = 𝜙 P (𝑛, 𝑤) := 𝜅 (𝜙 ∗ ) = ∀𝑖. (𝑖 = 1 ∧ 𝑖 < 𝑛 ∧ 𝜅 (cstr(𝑎[𝑖] ≠

                               Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
22:12                                                                              Chih-Duo Hong and Anthony W. Lin


𝑎[𝑛]))) ∨ (𝑖 > 1 ∧ 𝑖 ≤ 𝑛 ∧ 𝜅 (cstr(𝑎[𝑖] = 𝑎[𝑖 − 1]))) ∨ (𝑖 > 𝑛 ∧ 𝑛 ≥ 2). For example,
𝜅 (cstr(𝑎[𝑖] ≠ 𝑎[𝑛])) = 𝜅 (𝑎[𝑛] = 𝑎[𝑛] ∧ 𝑎[𝑖] ≠ 𝑎[𝑛] ∧ (𝑎[𝑖] ≠ 𝑎[𝑖 − 1] ∨ 𝑎[𝑖 − 1] ≠ 𝑎[𝑛]))
                          = (1 ≤ 𝑛 ∧ 𝑛 ≤ 𝑛 ⇒ Δ1 (𝑛, 𝑤)) ∧ (1 ≤ 𝑖 ∧ 𝑖 ≤ 𝑛 ⇒ ¬Δ1 (𝑖, 𝑤)) ∧
                             ((1 ≤ 𝑖 ∧ 𝑖 ≤ 𝑛 ⇒ ¬Δ2 (𝑖, 𝑤)) ∨ (1 ≤ 𝑖 − 1 ∧ 𝑖 − 1 ≤ 𝑛 ⇒ ¬Δ1 (𝑖 − 1, 𝑤))).
We can eﬀectively check that 𝜙 P is unsatisﬁable in 𝔖2 by Proposition 4.1. Since regular abstractions
are overapproximations, this implies that 𝜙 is unsatisﬁable in T . In this way, with the provided
indexed predicates, our tool can prove that 𝜙 is unsat in a second, while solvers like Z3 and cvc5
fail to handle the formula (i.e. both of them output “unknown” for checking satisﬁability of 𝜙.) 
   Transition formulae. Given a singly indexed transition formula 𝜙 over variables V ⊎ V ′ , we
can compute a regular abstraction for 𝜙 by ﬁrst extending the predicates P to P ⊎ P ′ , where
P ′ is obtained from P by replacing each 𝑥 ∈ V with 𝑥 ′ . We then compute an abstract tran-
sition formula 𝜙 P ((𝜎, 𝑤), (𝜎 ′, 𝑤 ′ )) analogously to how we compute an abstract state formula
𝜙 P (𝜎, 𝑤). However, if we only consider transition formulae induced by our guarded command
language, we can compute an abstract transition formula directly from a command as follows. De-
                          Ó
ﬁne copy_except(𝑥) := 𝑧 ∈ V\{𝑥 } (𝑧 ′ = 𝑧). Consider w.l.o.g. a guarded command 𝜓 ⊲ 𝛽, where 𝛽
is in form of either 𝑥 := 𝑒 or 𝑎[𝑡] := 𝑒. For 𝑥 := 𝑒, the corresponding transition formula is
                                         𝜓 ∧ copy_except(𝑥) ∧ 𝑥 ′ = 𝑒.                                          (9)
For 𝑎[𝑡] := 𝑒, the corresponding formula is
                                    𝜓 ∧ copy_except(𝑎) ∧ 𝑎 ′ = 𝑎{𝑡 ← 𝑒},                                       (10)
where 𝑎{𝑡 ← 𝑒} is a notation from the theory of extensional arrays [McCarthy 1993], denoting
the array obtained by assigning 𝑒 to 𝑎[𝑡]. (We may set 𝑒 to a fresh variable when 𝑒 is the nondeter-
ministic symbol “∗”.) Note that the abstraction formulae of (9) and (10) are computable. Indeed, for
an array formula 𝜏 and a clause 𝐶, the validity check of (𝜏 ∧ 𝑎 ′ = 𝑎{𝑡 ← 𝑒}) ⇒ 𝐶 can be compiled
into a decidable array theory supported by most SMT solvers (cf. [Kroening and Strichman 2016]).

5.3 Correctness of the Abstraction Procedure
Let 𝜙 := 𝛿𝑥 1 · · · 𝛿𝑥𝑛 . 𝜑 be a singly indexed array formula, where 𝜑 is quantiﬁer-free. Recall that,
to compute a regular abstraction of 𝜙, our procedure ﬁrst computes an abstraction formula 𝜙 ∗ =
𝛿𝑥 1 · · · 𝛿𝑥𝑛 . 𝜑˜ by replacing 𝜑 with a quantiﬁer-free formula 𝜑˜ such that (1) 𝜑˜ is in negation normal
form (NNF), (2) 𝜑˜ is expressible in P, and (3) 𝜑 ⇒ 𝜑˜ holds in T . Our procedure then outputs the
formula 𝜙 P = 𝜅 (𝜙 ∗ ), where 𝜅 (·) replaces each atom 𝑃𝑘 [𝑡/i] (resp. ¬𝑃𝑘 [𝑡/i]) in the formula with
𝜓 ⇒ Δ𝑘 (𝜎, 𝑤) (resp. 𝜓 ⇒ ¬Δ𝑘 (𝑡, 𝑤)), using 𝜓 to encode the boundary check of 𝑃𝑘 [𝑡/i]. Now we
show that this procedure is sound, that is, (J𝜙 P K, P) is indeed a regular abstraction of 𝜙.
   Lemma 5.2. Let P be a set of indexed predicates, and 𝜙 be a singly indexed array formula that
is expressible in P. If 𝜙 is satisﬁable, then 𝜅 (NNF(𝜙)) is also satisﬁable, where NNF(𝜙) denotes the
negation normal form of 𝜙.
   Proof. Fix a set of predicates P = h𝑃1 , . . . , 𝑃𝑚 i. For an SIA formula 𝜙 over V, suppose that 𝜎
is a solution of 𝜙. Then 𝜎 uniquely determines a word 𝑤 = 𝑤 (𝜎) ∈ Σ𝑚          ∗ such that 𝜎 |= Φ P and
                                                                                                      𝑤
|𝑤 | = max{𝜎 (𝑥) : 𝑥 is a parameter in V}. Particularly, for each 𝑖 ∈ {1, . . . , |𝑤 |} and 𝑘 ∈ {1, . . . , 𝑚},
𝑤 |= Δ𝑘 (𝑖, 𝑤) in 𝔖𝑚 if and only if 𝜎 |= 𝑃𝑘 [𝑖/i] in T (cf. Section 4.2). Now we argue that (𝜎𝑖𝑛𝑡 , 𝑤)
is a solution of 𝜅 (𝜙), where 𝜎𝑖𝑛𝑡 denotes the restriction of 𝜎 to index variables and parameters in
V. We shall prove this by induction on the quantiﬁer rank of 𝜙, denoted by 𝑟𝑎𝑛𝑘 (𝜙).
   For the base case, we show that 𝜎𝑖𝑛𝑡 , 𝑤 |= 𝜅 (𝜙) when 𝑟𝑎𝑛𝑘 (𝜙) = 0 (i.e. 𝜙 is quantiﬁer-free). Since
𝜙 is in NNF, we can assume w.l.o.g. that 𝜙 = 𝑔 ∧ℎ and 𝜅 (𝜙) = 𝑔 ∧𝜅 (ℎ) by writing 𝜙 in DNF. Here, 𝑔

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
Regular Abstractions for Array Systems                                                                                22:13

                                                    Ó
is a conjunction of index expressions, and ℎ = 𝑗 ℎ 𝑗 is a conjunction of data expressions. Assume
to the contrary that 𝜎 |= 𝜙 but 𝜎𝑖𝑛𝑡 , 𝑤 6 |= 𝜅 (𝜙). Since 𝜎𝑖𝑛𝑡 |= 𝑔, we have 𝜎𝑖𝑛𝑡 , 𝑤 |= ¬𝜅 (ℎ 𝑗 ) for some
𝑗 . Since ℎ 𝑗 is expressible in P, suppose w.l.o.g. that ℎ 𝑗 = 𝑃𝑘 [𝑡/i] for some 𝑃𝑘 ∈ P and index term
𝑡. Then 𝜎𝑖𝑛𝑡 , 𝑤 |= 1 ≤ 𝑡 ∧ 𝑡 ≤ |𝑤 | ∧ ¬Δ𝑘 (𝑡, 𝑤) holds by the deﬁnition of 𝜅. But this implies 𝜎 |= ¬ℎ 𝑗
(and hence 𝜎 6 |= 𝜙) by the deﬁnition of 𝑤, leading to a contradiction. It follows that 𝜎𝑖𝑛𝑡 , 𝑤 |= 𝜅 (𝜙),
i.e., the hypothesis is true when 𝑟𝑎𝑛𝑘 (𝜙) = 0.
    Now suppose that 𝑟𝑎𝑛𝑘 (𝜙) = 𝑛 +1, and that the hypothesis holds for formulae of rank equal to 𝑛.
If 𝜎 |= ∃𝑖.𝜓 , we have 𝜎 |= 𝜓 [𝑝/𝑖] for some 𝑝. Then 𝜎𝑖𝑛𝑡 , 𝑤 |= 𝜅 (𝜓 [𝑝/𝑖]) by the induction hypothesis,
which implies that 𝜎𝑖𝑛𝑡 , 𝑤 |= 𝜅 (∃𝑖.𝜓 ). Similarly, if 𝜎 |= ∀𝑖.𝜓 , we have 𝜎 |= 𝜓 [𝑝/𝑖] for all 𝑝. Then
𝜎𝑖𝑛𝑡 , 𝑤 |= 𝜅 (𝜓 [𝑝/𝑖]) for all 𝑝 by the induction hypothesis, which implies that 𝜎𝑖𝑛𝑡 , 𝑤 |= 𝜅 (∀𝑖.𝜓 ).
The statement therefore holds for formulae of all ranks by induction.                                      
   Theorem 5.3 (Correctness). Let P be a set of indexed predicates, and 𝜙 be a singly indexed array
formula. Then J𝜙 P K is regular and 𝛼 (𝜙) ⊆ J𝜙 P K. Namely, 𝜙 P yields a regular abstraction of 𝜙.
   Proof. J𝜙 P K is regular by Proposition 4.1. Since 𝛼 is monotonic and 𝜙 ⇒ 𝜙 ∗ , it suﬃces to
show that 𝛼 (𝜙 ∗ ) ⊆ J𝜙 P K. Consider an arbitrary abstract state (𝜎, 𝑤) ∈ 𝛼 (𝜙 ∗ ), with 𝜎 Ó    being an
interpretation of index variables and system parameters 𝑥 1, . . . , 𝑥𝑟 in V. Deﬁne Ψ𝜎,𝑤 := ( 𝑟𝑖=1 𝑥𝑖 =
𝜎 (𝑥𝑖 )) ∧ Φ𝑤P . Then 𝜙 ∗ ∧ Ψ𝜎,𝑤 is satisﬁable by the deﬁnition of 𝛼. Since 𝜙 ∗ ∧ Ψ𝜎,𝑤 is in NNF and
expressible in P, 𝜅 (𝜙 ∗ ∧Ψ𝜎,𝑤 ) is satisﬁable by Lemma 5.2. However, observe that (𝜎, 𝑤) is a solution
of 𝜅 (𝜙 ∗ ∧Ψ𝜎,𝑤 ) when 𝜅 (𝜙 ∗ ∧Ψ𝜎,𝑤 ) is satisﬁable, as the formula only constrains its free word variable
on the ﬁrst |𝑤 | letters. Therefore, we have (𝜎, 𝑤) ∈ J𝜅 (𝜙 ∗ ∧Ψ𝜎,𝑤 )K = J𝜅 (𝜙 ∗ )∧𝜅 (Ψ𝜎,𝑤 )K ⊆ J𝜅 (𝜙 ∗ )K =
J𝜙 P K. This allows us to conclude that 𝛼 (𝜙 ∗ ) ⊆ J𝜙 P K, and therefore 𝛼 (𝜙) ⊆ J𝜙 P K.                   

5.4   A Closure Property
Consider a ﬁnite set Φ of singly indexed array formulae. Note that we can always select a set of
indexed predicates that expresses all formulae in Φ. In such cases, if Φ is closed under Boolean
operations, then the abstractions our procedure computes for Φ are also closed under Boolean
operations, as is indicated by the following proposition.
  Proposition 5.4. For indexed predicates P and singly indexed array formulae 𝜙 and 𝜓 , it holds
that (𝜙 ∨ 𝜓 ) P ≡ 𝜙 P ∨ 𝜓 P. Furthermore, we have (𝜙 ∧ 𝜓 ) P ≡ 𝜙 P ∧ 𝜓 P and (¬𝜙) P ≡ ¬𝜙 P ∧ true P 3
when 𝜙 and 𝜓 are expressible in P.
                                                           Ô                                Ô
  Proof. Suppose w.l.o.g. that 𝜙 = 𝛿𝑥 1 · · · 𝛿𝑥 𝑝 . 𝑖 ∈𝐼 (𝑔𝑖 ∧ ℎ𝑖 ) and 𝜓 = 𝛿𝑦1 · · · 𝛿𝑦𝑞 . 𝑗 ∈ 𝐽 (𝑔 𝑗 ∧ ℎ 𝑗 ),
where (i) 𝐼 ∩ 𝐽 = ∅, and (ii) for each 𝑘 ∈ 𝐼 ⊎ 𝐽 , 𝑔𝑘 is a conjunction of index expressions, and ℎ𝑘 is a
conjunction of data expressions. Then we have
                                                           Ü
              (𝜙 ∨ 𝜓 ) P ≡ 𝛿𝑥 1 · · · 𝛿𝑥 𝑝 𝛿𝑦1 · · · 𝛿𝑦𝑞 .     𝑔𝑘 ∧ 𝜅 (cstr(ℎ𝑘 )) ≡ 𝜙 P ∨ 𝜓 P.
                                                               𝑘∈ 𝐼 ⊎ 𝐽
Furthermore, notice that
                                                        Ü      Ü
         (𝜙 ∧ 𝜓 ) P ≡ 𝛿𝑥 1 · · · 𝛿𝑥 𝑝 𝛿𝑦1 · · · 𝛿𝑦𝑞 .                     𝑔𝑖 ∧ 𝑔 𝑗 ∧ 𝜅 (cstr(ℎ𝑖 ∧ ℎ 𝑗 ))
                                                        𝑖 ∈𝐼       𝑗 ∈𝐽
                                                        Ü      Ü
          𝜙 P ∧ 𝜓 P ≡ 𝛿𝑥 1 · · · 𝛿𝑥 𝑝 𝛿𝑦1 · · · 𝛿𝑦𝑞 .                     𝑔𝑖 ∧ 𝑔 𝑗 ∧ 𝜅 (cstr(ℎ𝑖 )) ∧ 𝜅 (cstr(ℎ 𝑗 ))
                                                        𝑖 ∈𝐼       𝑗 ∈𝐽

Hence, it suﬃces to show that 𝜅 (cstr(ℎ𝑖 ∧ℎ 𝑗 )) ⇔ 𝜅 (cstr(ℎ𝑖 )) ∧𝜅 (cstr(ℎ 𝑗 )) holds in 𝔖𝑚 . For the “⇒”
direction, note that a feasible clause for cstr(ℎ𝑖 ) or cstr(ℎ 𝑗 ) is also feasible for cstr(ℎ𝑖 ∧ ℎ 𝑗 ). Thus,
a solution of 𝜅 (cstr(ℎ𝑖 ∧ ℎ 𝑗 )) is also a solution of 𝜅 (cstr(ℎ𝑖 )) ∧ 𝜙 (cstr(ℎ 𝑗 )). For the “⇐” direction,
suppose that 𝐶 is a feasible clause for cstr(ℎ𝑖 ∧ ℎ 𝑗 ), and thus 𝜅 (cstr(ℎ𝑖 ∧ ℎ 𝑗 )) ⇒ 𝜅 (𝐶) holds in 𝔖𝑚 .
3 One may regard JtrueP K as the abstract state space induced by P in our regular abstraction framework.



                                 Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
22:14                                                                              Chih-Duo Hong and Anthony W. Lin


Since ℎ𝑖 , ℎ 𝑗 are expressible in P, ¬ℎ 𝑗 ∨ 𝐶 and ¬ℎ𝑖 ∨ 𝐶 are feasible clauses for cstr(ℎ𝑖 ) and cstr(ℎ 𝑗 ),
respectively. Similarly, each atom of ℎ𝑖 and ℎ 𝑗 induces a singleton feasible clause for cstr(ℎ𝑖 ) and
cstr(ℎ 𝑗 ), respectively. Hence, 𝜅 (cstr(ℎ𝑖 ) ∧ cstr(ℎ 𝑗 )) ⇒ 𝜅 (ℎ𝑖 ∧ ℎ 𝑗 ∧ (¬ℎ𝑖 ∨ 𝐶) ∧ (¬ℎ 𝑗 ∨ 𝐶)) ⇒
𝜅 (ℎ𝑖 ∧ ℎ 𝑗 ∧ 𝐶) ⇒ 𝜅 (𝐶) holds in 𝔖𝑚 . Thus, a solution of 𝜅 (cstr(ℎ𝑖 )) ∧ 𝜅 (cstr(ℎ 𝑗 )) is also a solution
of 𝜅 (cstr(ℎ𝑖 ∧ ℎ 𝑗 )). This completes the proof for both directions, leading to (𝜙 ∧ 𝜓 ) P ≡ 𝜙 P ∧ 𝜓 P.
   Finally, note that (¬𝜙) P∧𝜙 P ≡ (¬𝜙 ∧𝜙) P ≡ false P ≡ false, and (¬𝜙) P ∨𝜙 P ≡ (¬𝜙 ∨𝜙) P ≡ true P.
This allows us to deduce that (¬𝜙) P ≡ ¬𝜙 P ∧ true P.                                                      
   Proposition 5.4 makes it possible to compute precise regular abstractions of complex formulae by
composing abstractions of simple formulae. For example, we may compute the regular abstraction
of (10) as 𝜙 P = 𝜓 P ∧ (copy_except(𝑎) ∧ 𝑎 ′ = 𝑎{𝑡 ← 𝑒}) P . The two regular abstractions on the
right-hand side can then be reused for computing abstractions of other formulae. Even if 𝜙 is not
expressible in P, we can still compute 𝜙 P using composition since regular abstractions are closed
under conjunction (Proposition 4.10), but at the price of potentially losing precision.
   We conclude this section with the following observation.
  Proposition 5.5. Let P be a set of indexed predicates, and 𝜙 be a singly indexed array formula
that is expressible in P. Then it holds that 𝛾 (𝜙 P ) = 𝛾 (𝛼 (𝜙)).
     Proof. Since 𝛼 (𝜙) ⊆ J𝜙 P K by Theorem 5.3, we have 𝛾 (𝛼 (𝜙)) ⊆ 𝛾 (𝜙 P ). Suppose to the contrary
that there exists 𝑠 ∈ 𝛾 (𝜙 P ) \ 𝛾 (𝛼 (𝜙)). Since 𝑠 ∈ 𝛾 (𝜙 P ), we have 𝛼 (𝑠) ⊆ J𝜙 P K by Proposition 4.6.
Similarly, since 𝑠 ∉ 𝛾 (𝛼 (𝜙)), we have 𝛼 (𝑠) * 𝛼 (𝜙) by Proposition 4.6. The latter fact implies that
𝑠 6 |= 𝜙, that is, 𝑠 |= ¬𝜙. Thus, 𝛼 (𝑠) ⊆ 𝛼 (¬𝜙) ⊆ J(¬𝜙) P K = Jtrue P K \ J𝜙 P K by Theorem 5.3 and
Proposition 5.4. It follows that 𝛼 (𝑠) ∩ J𝜙 P K = ∅, a contradiction. This completes the proof.         

6     VERIFICATION OF TEMPORAL ARRAY PROPERTIES
In this section, we discuss how to verify linear-time array system properties by combining our
abstraction techniques with regular model checking. We shall ﬁrst introduce the notion of tempo-
ral array properties and abstractable speciﬁcations. We then present two veriﬁcation methods for
typical safety and liveness array properties. Finally, we describe a generic technique to verify a
syntactic fragment of array properties called the index-bounded monodic properties.

6.1     Temporal Array Property
To express the temporal properties of an array system, we provide a speciﬁcation language com-
bining the indexed array logic with LTL. This can be seen as a restriction of FO-LTL [Abadi 1989;
Hodkinson et al. 2000] to the indexed array logic. For ease of exposition, we shall only consider
the “globally” and “eventually” connectives in the sequel. Our approach however can be extended
to handle other standard connectives such as “next” and “until” in a straightforward manner.
   A temporal array property is a formula 𝜙 constrained by
                            𝜙 ::= 𝜓 | ¬𝜙 | 𝜙 ∨ 𝜙 | 𝜙 ∧ 𝜙 | ∃𝑖. 𝜙 | ∀𝑖. 𝜙 | G 𝜙 | F 𝜙
where 𝜓 is an indexed array formula, 𝑖 is an index variable, and G and F are the standard “glob-
ally” and “eventually” temporal connectives, respectively, in LTL. As usual, we extend the logic
with logical operators such as ⇒ (implies) and ⇔ (if and only if). The semantics of a temporal ar-
ray property is standard (see e.g. [Hodkinson et al. 2000]). Intuitively, temporal connectives oﬀer
means of relating two states at diﬀerent time points in a path, whereas the ﬁrst-order quantiﬁers
allow one to relate diﬀerent array positions. For example, both G (∀𝑖. 1 ≤ 𝑖 ∧ 𝑖 ≤ |𝑎| ⇒ 𝑎[𝑖] = 0)
and ∀𝑖. (1 ≤ 𝑖 ∧ 𝑖 ≤ |𝑎| ⇒ G 𝑎[𝑖] = 0) assert that the array 𝑎 has only 0 as elements throughout
the path. We say that a temporal array property 𝜙 holds for an array system if the system does not
have a path that satisﬁes ¬𝜙.

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
Regular Abstractions for Array Systems                                                                          22:15


6.2   Abstraction of Array System Specifications
  Deﬁnition 6.1 (Abstractable speciﬁcation). An array formula is abstractable if it is of form ∃𝑖. 𝜙
for some (possibly quantiﬁed) SIA formula 𝜙. An array system is abstractable if it is speciﬁed with
abstractable array formulae. A temporal array property 𝜙 is abstractable if it is constrained by
                                  𝜙 ::= 𝜓 | 𝜙 ∨ 𝜙 | 𝜙 ∧ 𝜙 | ∃𝑖. 𝜙 | G 𝜙 | F 𝜙
for (possibly quantiﬁed) SIA formulae 𝜓 .
   Abstractable formulae slightly generalize SIA formulae by allowing multiple existentially in-
dexed/quantiﬁed variables. In fact, a formula is abstractable if and only if it can be transformed
into an SIA formula using Skolemization. Thus, an abstractable ﬁrst-order array system 𝔗 can be
formally transformed into a set of SIA formulae. More precisely, suppose that 𝜙 := ∃𝑖.𝜓 is an
abstractable array formula over variables V. Deﬁne an SIA formula 𝜓 ★ := 𝜓 [𝑐/𝑖] over variables
V ⊎ {𝑐 }, where 𝑐 are fresh system parameters. We can then add the new parameters 𝑐 to the vo-
cabulary of 𝔗 and substitute 𝜓 ★ for 𝜙 in the speciﬁcation. Clearly, a temporal array property holds
for 𝔗 if and only if the property holds for the Skolemized version of 𝔗.
   An abstractable temporal array property can furthermore be converted to an equisatisﬁable
temporal array property wherein all maximal non-temporal subformulae are singly indexed. The
conversion is essentially the same as Skolemization, except that here we replace an indexed vari-
able quantiﬁed inside a G operator with a fresh index variable, and replace an indexed variable that
is only quantiﬁed inside an F operator with a fresh system parameter. The maximal non-temporal
subformulae of the obtained temporal array property are all singly indexed, meaning that their se-
mantics can be overapproximated by regular abstractions. In other words, an abstractable temporal
array property can be abstracted to a propositional temporal formula with atoms being regular lan-
guages. This fact makes it possible to leverage existing veriﬁcation techniques in regular model
checking to perform abstract analysis for abstractable speciﬁcations and properties.

6.3   Safety Verification
A safety array property is a temporal array property in form of ∀𝑖. (𝜓 1 ⇒ G𝜓 2 ). Fix a safety array
property 𝜙 and an array system 𝔗 := (V, 𝜙 𝐼 , 𝜙𝑇 ). Suppose that both 𝔗 and ¬𝜙 ≡ ∃𝑖. (𝜓 1 ∧F ¬𝜓 2 ) are
abstractable. Deﬁne 𝜓 1★ := 𝜓 1 [𝑐/𝑖] and 𝜓 2★ := 𝜓 2 [𝑐/𝑖] with fresh system parameters 𝑐. Moreover,
deﬁne a transition system 𝔗★ := (V ★, 𝜙 𝐼★, 𝜙𝑇 , 𝜙 𝐵 ) with V ★ := V ⊎ {𝑐 }, 𝜙 𝐼★ := 𝜙 𝐼 ∧ 𝜓 1★, and
𝜙 𝐵 := ¬𝜓 2★. It is clear that 𝔗★ is abstractable. Given a set P of indexed predicates over V ★, we can
compute regular abstractions (𝐼, P), (𝑇 , P), and (𝐵, P) of 𝜙 𝐼★, 𝜙𝑇 , and 𝜙 𝐵 , respectively, as described
in Section 5. We then obtain a regular safety property (𝐼,𝑇 , 𝐵) that holds iﬀ 𝑇 ∗ (𝐼 ) ∩ 𝐵 = ∅, where
𝑇 ∗ denotes the transitive closure of 𝑇 . It is clear that (𝐼,𝑇 , 𝐵) holds only if 𝔗 satisﬁes the safety
array property 𝜙. With Proposition 4.1, we can summarize this result as follows.
  Theorem 6.2. Let 𝔗 be an array system, and 𝜙 be a safety array property. Suppose that 𝔗 and ¬𝜙
are abstractable. Given a set of indexed predicates, we can eﬀectively compute ﬁnite automata I, T ,
and B such that 𝜙 holds for 𝔗 if the safety property (I, T , B) holds.

6.4 Liveness Verification
A liveness array property is a temporal array property in form of ∀𝑖. (𝜓 1 ⇒ F𝜓 2 ). (We pick this
“eventuality” property for simplicity and suﬃciency for our benchmarks, although our technique
can easily be adapted to other liveness properties such as recurrence). Fix a liveness array property
𝜙 and an array transition system 𝔗 := (V, 𝜙 𝐼 , 𝜙𝑇 ). Suppose that both 𝔗 and ¬𝜙 ≡ ∃𝑖. (𝜓 1 ∧ G ¬𝜓 2 )
are abstractable. Deﬁne 𝜓 1★ := 𝜓 1 [𝑐/𝑖] and 𝜓 2★ := 𝜓 2 [𝑐/𝑖] with fresh system parameters 𝑐, and
an array transition system 𝔗★ := (V ★, 𝜙 𝐼★, 𝜙𝑇 , 𝜙 𝐹 ), where V ★ := V ⊎ {𝑐 }, 𝜙 𝐼★ := 𝜙 𝐼 ∧ 𝜓 1★, and

                               Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
22:16                                                                              Chih-Duo Hong and Anthony W. Lin


𝜙 𝐹 := 𝜓 2★. It is clear that 𝔗★ is abstractable. Given a set P of indexed predicates over V ★, we
compute regular abstractions (𝐼, P), (𝑇 , P), and (𝐸, P) for 𝜙 𝐼★, 𝜙𝑇 , and ¬𝜙 𝐹 , respectively. Now,
following the reduction described in Section 4.3, we let 𝐹 := Σ𝑚      ∗ \ 𝐸 and deﬁne a regular liveness

property (𝐼,𝑇 , 𝐹 ) that holds if and only if 𝑠𝑡 (𝜋) ∩ 𝐹 ≠ ∅ for every path 𝜋 ∈ Π(𝐼,𝑇 ). It is not hard
to see that the abstract transition system hΣ𝑚   ∗ , 𝐼,𝑇 i preserves inﬁnite counterexample paths from

𝔗. That is, if there exists an inﬁnite concrete path 𝑠 0 𝑠 1 · · · such that 𝑠 0 |= 𝜓𝐼★ and 𝑠𝑖 6 |= 𝜙 𝐹 for all
𝑖 ≥ 0, then there exists an inﬁnite abstract path 𝑡 0 𝑡 1 · · · such that 𝑡 0 ∈ 𝐼 and 𝑡𝑖 ∉ 𝐹 for all 𝑖 ≥ 0.
   We say that a transition system is ¬𝜙-progressing if every maximal system path satisfying ¬𝜙
is an inﬁnite path. Observe that when 𝔗 is ¬𝜙-progressing, (𝐼,𝑇 , 𝐹 ) holds only if 𝔗 satisﬁes the
liveness array property 𝜙. We hence have the following result.
  Theorem 6.3. Let 𝔗 be an array system, and 𝜙 be a liveness array property. Suppose that 𝔗 and
¬𝜙 are abstractable, and that 𝔗 is ¬𝜙-progressing. Then given a set of indexed predicates, we can
eﬀectively compute ﬁnite automata I, T , and F such that 𝜙 holds for 𝔗 if the liveness property
(I, T , F ) holds.
Progress verification. Theorem 6.2 and 6.3 exploit the same technique that overapproximates the
target array property with a counterpart property of the abstract system. Generally, this tech-
nique works for any temporal array property with an abstractable negated formula, as long as
a false property remains false after new transitions are introduced to the system. For a safety
property, this requirement is met automatically since extensions of a counterexample path are
still counterexample paths. For a liveness array property 𝜙, this requires the array system to be
¬𝜙-progressing, i.e., the system does not have a ﬁnite maximal counterexample path.
    We may formulate and verify the progress condition as a safety array property as follows. Given
an array system 𝔗 := (V, 𝜙 𝐼 , 𝜙𝑇 ) and a liveness array property 𝜙 := ∀𝑖. (𝜓 1 ⇒ F𝜓 2 ), we aim
to check if 𝔗 is ¬𝜙-progressing. As before, deﬁne 𝜓 1★ := 𝜓 1 [𝑐/𝑖] and 𝜓 2★ := 𝜓 2 [𝑐/𝑖] with fresh
system parameters 𝑐. We then specify an array system 𝔗 ∗ := (V ★, 𝜙 𝐼★, 𝜙𝑇★) with V ★ := V ⊎ {𝑐 },
𝜙 𝐼★ := 𝜙 𝐼 ∧ 𝜓 1★ , and 𝜙𝑇★ := 𝜙𝑇 ∧ ¬𝜓 2★ . It is easy to see that the system 𝔗 ∗ is safe w.r.t. the safety
                                 ′
array property 𝜙 ∗ := ∀𝑖. G ∃𝑖 . 𝜙𝑇★ if and only if 𝔗 is ¬𝜙-progressing. When the transition formula
𝜙𝑇 is speciﬁed with guarded commands, say with 𝑛 commands (𝐴1 ⊲ 𝐵 1 ), . . . , (𝐴𝑛 ⊲ 𝐵𝑛 ), the
safety property 𝜙 ∗ can be written as ∀𝑖. G (𝐴★       1 ∨ · · · ∨ 𝐴𝑛 ∨ 𝜓 2 ). Notably, when both 𝔗 and ¬𝜙
                                                                   ★     ★

are abstractable (which is precisely the assumption of Theorem 6.3), the induced system 𝔗 ∗ and
safety property 𝜙 ∗ are also abstractable. Consequently, the progress condition of 𝔗 with respect
to ¬𝜙 can be checked formally using the safety veriﬁcation method stated in Theorem 6.2.

6.5     Liveness Verification under Fairness Requirements
We brieﬂy discuss how to perform liveness veriﬁcation of a subclass of array systems in the pres-
ence of fairness requirements. Such requirements are essential for specifying reactive and concur-
rent process systems (cf. [Demri et al. 2016; Manna and Pnueli 2012]).
   Deﬁnition 6.4 (Index-bounded array system). An array system (V, 𝜙 𝐼 , 𝜙𝑇 ) is index-bounded if for
each index variable 𝑥 ∈ V, there exist two parameters 𝑙𝑥 , ℎ𝑥 ∈ V such that 𝑠 (𝑙𝑥 ) ≤ 𝑠 (𝑥) ≤ 𝑠 (ℎ𝑥 )
holds in any reachable state 𝑠 of the system. In other words, the valuation of 𝑥 is bounded between
𝑙𝑥 and ℎ𝑥 during system executions.
   Intuitively, index-boundedness requires the range of index variables to be ﬁnite at runtime, while
leaving the range of array elements unrestricted. This assumption is reasonable since in practice,
index variables are mostly used to access elements of a ﬁnite array. Index-boundedness can be
speciﬁed formally in the array system speciﬁcation, or checked against a given array system by
formulating the assumption as a safety array property.

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
Regular Abstractions for Array Systems                                                                          22:17


  Deﬁnition 6.5 (Fairness speciﬁcation). An (abstractable) fairness speciﬁcation is a temporal array
property 𝜆 := ∀𝑖. 𝜂 constrained by the grammar
                                         𝜂 ::= GF𝜓 | FG𝜓 | 𝜂 ∨ 𝜂 | 𝜂 ∧ 𝜂,
where 𝜓 is an abstractable indexed array formula. We say that a path 𝜋 is fair with respect to 𝜆, or
simply fair when 𝜆 is clear, if 𝜋 satisﬁes 𝜆. A temporal array property 𝜙 holds for an array system
under a fairness speciﬁcation if the system does not have a fair path satisfying ¬𝜙.
   We note that our formalism of fairness is expressive enough to capture typical fairness require-
ments for reactive and concurrent systems, including process fairness (in form of GF 𝜙), weak fair-
ness (in form of GF 𝜙∨GF𝜓 ), and strong fairness (in form of GF 𝜙∨FG𝜓 ). See e.g. [Manna and Pnueli
2012] for a detailed discussion of these fairness requirements.
   Given fairness speciﬁcation 𝜆 and indexed predicates P, we can compute a regular abstraction
(𝐸, P) overapproximating 𝜆 in the abstract domain. Namely, if there is a fair concrete path 𝑠 0 𝑠 1 · · ·
with respect to 𝜆, then there is a fair abstract path 𝑡 0 𝑡 1 · · · with respect to 𝐸, and 𝑡𝑖 ∈ 𝛼 (𝑠𝑖 ) for
each 𝑖 ≥ 0. When the abstract system is weakly ﬁnite [Esparza et al. 2012], that is, every inﬁnite
path eventually enters a cycle, checking the existence of a fair counterexample path essentially
amounts to searching for a reachable fair cycle, which can in turn be reduced to a safety veriﬁcation
problem [Daniel et al. 2016; Schuppan and Biere 2006]. Indeed, for weakly ﬁnite systems, we can
formally translate the abstract fairness condition (𝐸, P) to a formalism similar to the so-called
Büchi regular transition system (BRTS) [Abdulla et al. 2012], which generalizes the translation from
linear temporal properties to Büchi automata in ﬁnite-state model checking [Vardi and Wolper
1986]. We refer the interested reader to [Hong 2022] for the technical details of our translation
procedure.
   It is easy to see that regular abstractions of an index-bounded array system are weakly ﬁnite.
Thus, together with Theorem 6.3, we can summarize our results in this section as follows.
   Theorem 6.6. Let 𝔗 be an index-bounded array system, 𝜙 be a liveness array property, and 𝜆 be
a fairness speciﬁcation. Suppose that 𝔗 and ¬𝜙 are abstractable, and that 𝔗 is ¬𝜙-progressing. Then
we can compute ﬁnite automata I, T , and F , as well as a regular fairness requirement Λ, such that
𝜙 holds for 𝔗 under the fairness speciﬁcation Λ if the liveness property (I, T , F ) holds under the
fairness requirement Λ.

6.6   Verification of Monodic Temporal Properties
In this section, we brieﬂy discuss a generic method to verify a monodic fragment of the tempo-
ral array properties. This method directly extends the classical tableaux-theoretic approach for
LTL model checking (cf. [Clarke Jr et al. 2018]) to inﬁnite structures. Similar techniques were em-
ployed in [Abdulla et al. 2012] for verifying LTL(MSO) properties of parameterized systems, and
in [Padon et al. 2021] for verifying FO-LTL properties of ﬁrst-order transition systems. The pre-
sentation here is essentially adopted from [Padon et al. 2021].
   Consider a temporal array property 𝜙 over variables V. We may eliminate F from ¬𝜙 using
the rule F 𝜙 ≡ ¬G ¬𝜙, and assume that G is the only temporal connective contained in ¬𝜙. Let
𝑠𝑢𝑏 (¬𝜙) denote the set of subformulae of ¬𝜙. Deﬁne
                                    V¬𝜙 := V ⊎ { 𝑔𝜑 : G 𝜑 ∈ 𝑠𝑢𝑏 (¬𝜙)},
where each 𝑔𝜑 is a fresh array variable. In a nutshell, to check that an array system satisﬁes 𝜙,
we take the product of the system and a “monitor” of ¬𝜙 over the extended set of variables V¬𝜙 .
The product system will be associated with a fairness condition such that the projection of a fair
path from V¬𝜙 to V coincides with a path satisfying ¬𝜙 in the original array system. Thus, the

                               Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
22:18                                                                              Chih-Duo Hong and Anthony W. Lin


temporal property 𝜙 holds for the original system if and only if the product system has no fair
path.
   To apply the aforementioned reduction in our abstraction framework, however, the temporal
property 𝜙 needs to meet some technical conditions. We say that 𝜙 is monodic [Hodkinson et al.
2000] if every temporal subformula of 𝜙 contains at most one free variable outside V. For instance,
when V = {𝑎, 𝑘}, the property ∀𝑗 .G 𝑎[ 𝑗 ] > 𝑎[𝑘] is monodic, whilst ∃𝑖.∀𝑗 .G 𝑎[ 𝑗 ] > 𝑎[𝑖] is not. We
say that 𝜙 is index-bounded [Abdulla et al. 2016, 2012; Cimatti et al. 2022; Emerson and Namjoshi
2003] if there exists an index variable ℎ ∈ V such that each quantiﬁed variable of 𝜙 is bounded
above by ℎ. This index-boundedness restriction may be imposed syntactically, for example, by
replacing each subformula ∃𝑖.𝜓 of 𝜙 with ∃𝑖. 𝑖 ≤ ℎ ∧𝜓 , and each subformula ∀𝑖.𝜓 with ∀𝑖. 𝑖 ≤ ℎ ⇒
𝜓.
   For a monodic formula 𝜙 over V, we write 𝜙 (𝑖) to indicate that 𝑖 is the only free variable of 𝜙
outside V, if there is any. In the case that 𝜙 has no such free variable, we just set 𝑖 to be an arbi-
trary index variable outside V. We use FO[𝜙] to denote a ﬁrst-order representation of 𝜙, deﬁned
inductively as follows with 𝛿 ∈ {∃, ∀}:

                FO[𝜙] := 𝜙        (𝜙 is non-temporal)                   FO[𝛿𝑖. 𝜙] := 𝛿𝑖. FO[𝜙]
          FO[G 𝜙 (𝑖)] := 𝑔𝜙 [𝑖] ≠ 0                                 FO[𝜙 1 ∨ 𝜙 2 ] := FO[𝜙 1 ] ∨ FO[𝜙 2 ]
              FO[¬𝜙] := ¬ FO[𝜙]                                     FO[𝜙 1 ∧ 𝜙 2 ] := FO[𝜙 1 ] ∧ FO[𝜙 2 ]

Now, consider an index-bounded monodic property 𝜙 and an array system 𝔗 := (V, 𝜙 𝐼 , 𝜙𝑇 ). Deﬁne
a fair transition system 𝔗 𝑓 := (V¬𝜙 ,𝜓𝐼 ,𝜓𝑇 ) with fairness requirement 𝜆, where
                                  Û
           𝜓𝐼 := 𝜙 𝐼 ∧ FO[¬𝜙] ∧                          |𝑔𝜑 | = ℎ
                                      G𝜑 (𝑖 ) ∈𝑠𝑢𝑏 (¬𝜙 )
                          Û                                                                      
          𝜓𝑇 := 𝜙𝑇 ∧ ∀𝑖.                         𝑖 > ℎ ∨ (𝑔𝜑 [𝑖] ≠ 0 ⇔ (FO[𝜑 (𝑖)] ∧ 𝑔𝜑′ [𝑖] ≠ 0))
                            G𝜑 (𝑖 ) ∈𝑠𝑢𝑏 (¬𝜙 )
                     Û
            𝜆 := ∀𝑖.                   GF (𝑖 > ℎ ∨ 𝑔𝜑 [𝑖] ≠ 0 ∨ ¬ FO[𝜑 (𝑖)])
                          G𝜑 (𝑖 ) ∈𝑠𝑢𝑏 (¬𝜙 )

    The fair transition system 𝔗 𝑓 is constructed as the product of the original system 𝔗 and a
monitor of ¬𝜙 over the extended variables V¬𝜙 . Given a subformula G 𝜑 of ¬𝜙, the monitor updates
the array 𝑔𝜑 along a path of 𝔗 in accordance with whether or not G 𝜑 is satisﬁed by the current
path. More concretely, consider a path 𝜋 of 𝔗 and some 𝑡 ∈ N. If 𝜋 |= G 𝜑 (𝑡), then the monitor
maintains the array value 𝑔𝜑 [𝑡] along the path 𝜋 to make sure 𝜑 (𝑡) is satisﬁed at every state of the
path. Otherwise, if 𝜋 6 |= G 𝜑 (𝑡), then the monitor maintains the array value 𝑔𝜑 [𝑡] along the path 𝜋
to make sure 𝜑 (𝑡) is falsiﬁed at some state of the path. In the second case, the fairness condition 𝜆
guarantees that the event of 𝜑 (𝑡) being falsiﬁed will not be postponed forever.
    For a fair path of 𝔗 𝑓 , the projection of the path to the original variables V yields a path of the
original system 𝔗 satisfying ¬𝜙. Conversely, a path satisfying ¬𝜙 in the original system 𝔗 can be
lifted to the extended variables V¬𝜙 to obtain a fair path of 𝔗 𝑓 . As a consequence, one can verify
the temporal array property 𝜙 for 𝔗 by checking fair termination of 𝔗 𝑓 .

  Proposition 6.7 ([Abdulla et al. 2012; Padon et al. 2021]). Let 𝜙 be an index-bounded monodic
array property, 𝔗 be an array system, and 𝔗 𝑓 be the fair transition system induced by 𝔗 and 𝜙. Then
𝜙 holds for 𝔗 if and only if 𝔗 𝑓 has no fair path.

  Furthermore, when 𝔗 is ¬𝜙-progressing and the fair transition system 𝔗 𝑓 is abstractable, ter-
mination analysis of 𝔗 𝑓 is amenable to our liveness-to-safety reduction techniques in Section 6.5.
This fact, in tandem with Theorem 6.6, leads to the following result:

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
Regular Abstractions for Array Systems                                                                            22:19


  Theorem 6.8. Let 𝜙 be an index-bounded monodic array property, and 𝔗 be a ¬𝜙-progressing
index-bounded array system. If the fair transition system 𝔗 𝑓 is abstractable, then we can compute
ﬁnite automata I and T as well as a fairness requirement Λ, such that 𝜙 holds for 𝔗 if the transition
system (I, T ) always terminates under the fairness requirement Λ.

7     CASE STUDIES
We present four case studies in this section: two array programs implementing selection sort and a
simpliﬁed version of merge sort, and two distributed algorithms Dijkstra’s self-stabilizing protocol
and Chang-Roberts leader election protocol. To make our presentation succinct, we shall often omit
the index range constraint in a formula when the range is clear from the context. For example, we
shall write ∀𝑖. 𝑎[𝑖] = 0 instead of ∀𝑖. 1 ≤ 𝑖 ∧ 𝑖 ≤ |𝑎| ⇒ 𝑎[𝑖] = 0.

7.1 Selection Sort and Merge Sort
For selection sort, we consider a selection sort program as follows:
      𝑝𝑐 = 0 ⊲ 𝑙𝑜𝑤 := 1, ℎ𝑖𝑔ℎ := |𝑎|, 𝑝𝑐 := 1
      𝑝𝑐 = 1 ∧ 𝑙𝑜𝑤 ≥ ℎ𝑖𝑔ℎ ∧ 1 < ℎ𝑖𝑔ℎ ⊲ ℎ𝑖𝑔ℎ := ℎ𝑖𝑔ℎ − 1, 𝑙𝑜𝑤 := 1
      𝑝𝑐 = 1 ∧ 𝑙𝑜𝑤 < ℎ𝑖𝑔ℎ ∧ 𝑎[𝑙𝑜𝑤] ≤ 𝑎[ℎ𝑖𝑔ℎ] ⊲ 𝑙𝑜𝑤 := 𝑙𝑜𝑤 + 1
      𝑝𝑐 = 1 ∧ 𝑙𝑜𝑤 < ℎ𝑖𝑔ℎ ∧ 𝑎[𝑙𝑜𝑤] > 𝑎[ℎ𝑖𝑔ℎ] ⊲ 𝑎[ℎ𝑖𝑔ℎ] := 𝑎[𝑙𝑜𝑤], 𝑎[𝑙𝑜𝑤] := 𝑎[ℎ𝑖𝑔ℎ], 𝑙𝑜𝑤 := 𝑙𝑜𝑤 + 1

The array transition system 𝔗 := (V, 𝜙 𝐼 , 𝜙𝑇 ) induced by this program is
                   V := {𝑝𝑐, 𝑙𝑜𝑤, ℎ𝑖𝑔ℎ, 𝑎, |𝑎|},     𝜙 𝐼 := 𝑝𝑐 = 0,     𝜙𝑇 := 𝜙 1 ∨ 𝜙 2 ∨ 𝜙 3 ∨ 𝜙 4,
where 𝜙 1, 𝜙 2, 𝜙 3, 𝜙 4 are transition formulae derived from the four guarded commands. We verify
the typical correctness properties of a sorting algorithm as follows.

Property        Speciﬁcation                                                                           Explanation
𝑃1              G ∀𝑖.∀𝑗 . (𝑖 < 𝑗 ∧ ℎ𝑖𝑔ℎ < 𝑗 ⇒ 𝑎[𝑖] ≤ 𝑎[ 𝑗 ])                                           Sortedness
𝑃2              (∀𝑖. 𝑎[𝑖] = 𝑎 0 [𝑖]) ⇒ G ((∀𝑖.∃𝑗 . 𝑎[𝑖] = 𝑎 0 [ 𝑗 ]) ∧ (∀𝑖.∃𝑗 . 𝑎 0 [𝑖] = 𝑎[ 𝑗 ]))     Permutation
𝑃3              F ℎ𝑖𝑔ℎ ≤ 1                                                                             Termination

Here, 𝑃1 is a safety property stating that at any step, the array segment after the pivot position
ℎ𝑖𝑔ℎ is sorted; 𝑃2 is a safety property stating that the array produced by the program has the
same content as the input array modulo multiplicities; 𝑃3 is a liveness property stating that the
program eventually terminates. These three properties together establish the total correctness of
the program for arrays with distinct values.
  As for merge sort, we consider a nondeterministic merge sort program as follows:
    𝑝𝑐 = 0 ∧ 𝑠𝑜𝑟𝑡𝑒𝑑 (𝑙𝑜𝑤,𝑚𝑖𝑑) ∧ 𝑠𝑜𝑟𝑡𝑒𝑑 (𝑚𝑖𝑑,ℎ𝑖𝑔ℎ) ∧ ¬𝑠𝑜𝑟𝑡𝑒𝑑 (𝑙𝑜𝑤, ℎ𝑖𝑔ℎ) ∧ ℎ𝑖𝑔ℎ ≥ ℎ𝑖𝑔ℎ 1 ⊲ 𝑙𝑜𝑤 1 := 𝑙𝑜𝑤, 𝑝𝑐 := 1
    𝑝𝑐 = 1 ∧ 𝑙𝑜𝑤 1 < 𝑚𝑖𝑑 ∧ 𝑚𝑖𝑑 < ℎ𝑖𝑔ℎ ∧ 𝑎[𝑙𝑜𝑤 1 ] ≤ 𝑎[𝑚𝑖𝑑] ⊲ 𝑙𝑜𝑤 1 := 𝑙𝑜𝑤 1 + 1
    𝑝𝑐 = 1 ∧ 𝑙𝑜𝑤 1 < 𝑚𝑖𝑑 ∧ 𝑚𝑖𝑑 < ℎ𝑖𝑔ℎ ∧ 𝑎[𝑙𝑜𝑤 1 ] > 𝑎[𝑚𝑖𝑑] ⊲ 𝑎[𝑛] = 𝑎[𝑙𝑜𝑤 1 ], 𝑝𝑡𝑟 := 𝑙𝑜𝑤 1, 𝑝𝑐 := 2
    𝑝𝑐 = 1 ∧ ¬(𝑙𝑜𝑤 1 < 𝑚𝑖𝑑 ∧ 𝑚𝑖𝑑 < ℎ𝑖𝑔ℎ) ⊲ ℎ𝑖𝑔ℎ 1 := ℎ𝑖𝑔ℎ, 𝑙𝑜𝑤 := ∗, 𝑚𝑖𝑑 := ∗, ℎ𝑖𝑔ℎ := ∗, 𝑝𝑐 := 0
    𝑝𝑐 = 2 ∧ 𝑝𝑡𝑟 < 𝑚𝑖𝑑 ⊲ 𝑎[𝑝𝑡𝑟 + 1] := 𝑎[𝑛], 𝑎[𝑛] := 𝑎[𝑝𝑡𝑟 + 1], 𝑝𝑡𝑟 := 𝑝𝑡𝑟 + 1
    𝑝𝑐 = 2 ∧ 𝑝𝑡𝑟 ≥ 𝑚𝑖𝑑 ⊲ 𝑎[𝑙𝑜𝑤 1 ] := 𝑎[𝑛], 𝑚𝑖𝑑 := 𝑚𝑖𝑑 + 1, 𝑙𝑜𝑤 1 := 𝑙𝑜𝑤 1 + 1, 𝑝𝑐 := 1

Here, 𝑠𝑜𝑟𝑡𝑒𝑑 (𝑙,ℎ) := ∀𝑖. 𝑙 ≤ 𝑖 ∧ 𝑖 < ℎ − 1 ⇒ 𝑎[𝑖] ≤ 𝑎[𝑖 + 1] is an auxiliary formula expressing
that the array segment 𝑎[𝑙 . . . ℎ) is sorted. This program starts with 𝑝𝑐 = 0 and ℎ𝑖𝑔ℎ 1 = 1, and
guesses the values of 𝑙𝑜𝑤, 𝑚𝑖𝑑, and ℎ𝑖𝑔ℎ within the range {1, . . . , 𝑛}. If the program spots a merge

                                 Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
22:20                                                                              Chih-Duo Hong and Anthony W. Lin


opportunity by this guess (i.e. the guard of the ﬁrst command is satisﬁed), it proceeds to 𝑝𝑐 = 1 and
performs an in-place array merge. After the merge, the program returns to 𝑝𝑐 = 0 and guesses the
values of 𝑙𝑜𝑤, 𝑚𝑖𝑑, and ℎ𝑖𝑔ℎ again. We verify the following eventuality property of the program:
𝑃1 := F (𝑝𝑐 = 0 ∧ (¬𝑠𝑜𝑟𝑡𝑒𝑑 (𝑙𝑜𝑤,𝑚𝑖𝑑) ∨ ¬𝑠𝑜𝑟𝑡𝑒𝑑 (𝑚𝑖𝑑,ℎ𝑖𝑔ℎ) ∨ 𝑠𝑜𝑟𝑡𝑒𝑑 (𝑙𝑜𝑤, ℎ𝑖𝑔ℎ) ∨ ℎ𝑖𝑔ℎ < ℎ𝑖𝑔ℎ 1 )),
which states that the program eventually fails to pinpoint a merge opportunity at 𝑝𝑐 = 0. When
𝑃1 holds, any execution run that consistently spots a merge opportunity at 𝑝𝑐 = 0 eventually
reaches 𝑝𝑐 = 0 with no further such opportunities, at which point the array segment 𝑎[1 . . . 𝑛)
is sorted. In other words, 𝑃1 indicates that the program eventually produces a sorted array on
the “proper” execution runs, namely, the runs where the program consistently attempts to merge
partially sorted array segments.

7.2 Dijkstra’s Self-Stabilizing Algorithm
Dijkstra’s self-stabilizing algorithm [Dijkstra 1982], as introduced in Section 2, can be speciﬁed in
our modeling language as follows:
                     𝑝𝑖𝑑 = 1 ∧ 𝑎[𝑝𝑖𝑑] = 𝑎[𝑛] ∧ 𝑎[𝑝𝑖𝑑] < 𝑘 − 1 ⊲ 𝑎[𝑝𝑖𝑑] := 𝑎[𝑝𝑖𝑑] + 1, 𝑝𝑖𝑑 := ∗
                     𝑝𝑖𝑑 = 1 ∧ 𝑎[𝑝𝑖𝑑] = 𝑎[𝑛] ∧ 𝑎[𝑝𝑖𝑑] = 𝑘 − 1 ⊲ 𝑎[𝑝𝑖𝑑] := 0, 𝑝𝑖𝑑 := ∗
                     𝑝𝑖𝑑 > 1 ∧ 𝑝𝑖𝑑 ≤ 𝑛 ∧ 𝑎[𝑝𝑖𝑑] ≠ 𝑎[𝑝𝑖𝑑 − 1] ⊲ 𝑎[𝑝𝑖𝑑] := 𝑎[𝑝𝑖𝑑 − 1], 𝑝𝑖𝑑 := ∗

Here, we have identiﬁed |𝑎| with 𝑛 and used 𝑝𝑖𝑑 to denote the ID of the process to be selected by
the scheduler. For simplicity, we assume that only privileged processes can be scheduled. Dijkstra’s
algorithm is progressing under this scheduling assumption, since there always exists at least one
privileged process in the system. (Recall that we have proved this fact in Example 5.1.)
   Dijkstra’s algorithm can be initialized with arbitrarily many privileged processes. When 𝑛 ≤ 𝑘,
the system will converge to a stable state containing exactly one privileged process. For conve-
nience, deﬁne an auxiliary formula 𝑝𝑟𝑖𝑣 (𝑖) := (𝑖 = 1 ∧ 𝑎[𝑖] = 𝑎[𝑛]) ∨ (𝑖 ≠ 1 ∧ 𝑎[𝑖] ≠ 𝑎[𝑖 − 1]). We
can then express the self-stabilizing property of Dijkstra’s algorithm as
                                𝑃 := FG (∃𝑖. 𝑝𝑟𝑖𝑣 (𝑖) ∧ ∀𝑗 . 𝑗 ≠ 𝑖 ⇒ ¬𝑝𝑟𝑖𝑣 ( 𝑗 )),
meaning that the system eventually converges to exactly one privileged process and remains so
forever. To prove the self-stabilizing property 𝑃, we create subgoals 𝑃1 , . . . , 𝑃4 for the property as
listed in the following table.

 Property Speciﬁcation                                         Explanation
 𝑄1            𝑎[1] = 𝑎[𝑛] ∧ 𝑝𝑖𝑑 = 1                           Process 1 is privileged and scheduled
 𝑄2            ∀𝑖. 𝑖 ≠ 1 ⇒ 𝑎[𝑖] ≠ 𝑎[1]                         𝑥𝑖 ≠ 𝑥 1 for all 𝑖 ≠ 1
 𝑄3            ∀𝑖. 𝑖 ≠ 1 ⇒ 𝑎[𝑖] = 𝑎[𝑖 − 1]                     Process 𝑖 is unprivileged for all 𝑖 ≠ 1
 𝑄4            ∃𝑖. 𝑝𝑟𝑖𝑣 (𝑖) ∧ ∀𝑗 . 𝑗 ≠ 𝑖 ⇒ ¬𝑝𝑟𝑖𝑣 ( 𝑗 )         Exactly one process is privileged
 𝑃1            GF 𝑄 1                                          Recurrence property
 𝑃2            GF 𝑄 1 ⇒ F 𝑄 2                                  Liveness property under fairness condition
 𝑃3            𝑄 2 ⇒ F (𝑄 1 ∧ 𝑄 3 )                            Liveness property
 𝑃4            (𝑄 1 ∧ 𝑄 3 ) ⇒ G 𝑄 4                            Safety property
 𝑃             FG 𝑄 4                                          Self-stabilizing property

   Intuitively, 𝑃1 states that process 𝑝 1 is privileged and scheduled inﬁnitely often; 𝑃2 states that
if process 𝑝 1 is privileged and scheduled inﬁnitely often, then eventually variable 𝑥 1 diﬀers from
all the other variables; 𝑃3 states that if 𝑥 1 diﬀers from all the other variables at some point, then

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
Regular Abstractions for Array Systems                                                                           22:21


eventually 𝑝 1 is the only privileged process; 𝑃4 states that if 𝑝 1 is the only privileged process,
then the system has stabilized. To verify that Dijkstra’s algorithm is self-stabilizing, it suﬃces
to check the properties 𝑃1 , . . . , 𝑃4 separately, since the self-stabilizing property 𝑃 is subsumed by
𝑃1 ∧ 𝑃2 ∧ 𝑃3 ∧ 𝑃4 .

7.3   Chang-Roberts Algorithm
The Chang-Roberts algorithm [Chang and Roberts 1979] is a ring-based leader election protocol.
The algorithm assumes that each process has a unique ID, and that messages can be passed on
the ring in the clockwise direction. At ﬁrst, all processes are active. An active process becomes
passive after it emits or forwards a message. The algorithm starts when an active process turns
into an initiator and emits a message tagged with its ID to the next process. Let 𝑖𝑑𝑖 denote the ID
of Process 𝑖. When Process 𝑖 receives a message tagged with 𝑖𝑑, it reacts in three cases:
   – 𝑖𝑑 < 𝑖𝑑𝑖 : Process 𝑖 will purge the message.
   – 𝑖𝑑 > 𝑖𝑑𝑖 : Process 𝑖 will forward the message and become passive.
   – 𝑖𝑑 = 𝑖𝑑𝑖 : Process 𝑖 will announce itself as a leader.
The rationale behind the protocol is that only the message tagged with the largest ID will complete
the round trip and make its sender the leader. We specify the protocol as follows:
 𝑖𝑑 [𝑝𝑖𝑑] < 𝑚𝑠𝑔[𝑝𝑖𝑑 + 1] ∧ 𝑠𝑡 [𝑝𝑖𝑑] = 0 ⊲ 𝑠𝑡 [𝑝𝑖𝑑] := 1, 𝑝𝑖𝑑 := ∗
 𝑖𝑑 [𝑝𝑖𝑑] ≥ 𝑚𝑠𝑔[𝑝𝑖𝑑 + 1] ∧ 𝑠𝑡 [𝑝𝑖𝑑] = 0 ⊲ 𝑠𝑡 [𝑝𝑖𝑑] := 1, 𝑚𝑠𝑔[𝑝𝑖𝑑 + 1] := 𝑖𝑑 [𝑝𝑖𝑑], 𝑝𝑖𝑑 := ∗
 𝑚𝑠𝑔[𝑝𝑖𝑑] ≥ 𝑖𝑑 [𝑝𝑖𝑑] ∧ 𝑚𝑠𝑔[𝑝𝑖𝑑] < 𝑚𝑠𝑔[𝑝𝑖𝑑 + 1] ⊲ 𝑚𝑠𝑔[𝑝𝑖𝑑] := 0, 𝑠𝑡 [𝑝𝑖𝑑] := 1, 𝑝𝑖𝑑 := ∗
 𝑚𝑠𝑔[𝑝𝑖𝑑] ≥ 𝑖𝑑 [𝑝𝑖𝑑] ∧ 𝑚𝑠𝑔[𝑝𝑖𝑑] ≥ 𝑚𝑠𝑔[𝑝𝑖𝑑 + 1] ⊲ 𝑚𝑠𝑔[𝑝𝑖𝑑] := 0, 𝑠𝑡 [𝑝𝑖𝑑] := 1, 𝑚𝑠𝑔[𝑝𝑖𝑑 + 1] := 𝑚𝑠𝑔[𝑝𝑖𝑑], 𝑝𝑖𝑑 := ∗

These four commands correspond to four operations as follows: an initiator emits its ID, which
is purged by the successor process; an initiator emits its ID, which is cached by the successor;
a process forwards a message, which is purged by the successor; a process forwards a message,
which is cached by the successor. As before, we use 𝑝𝑖𝑑 to denote the ID of the scheduled process.
We use 𝑠𝑡 [𝑖] to represent the status of Process 𝑖, with 0 and 1 standing for active and passive,
respectively. We use 𝑖𝑑 [𝑖] and 𝑚𝑠𝑔[𝑖] to represent the ID and the message buﬀer, respectively, of
Process 𝑖. We stipulate that all process IDs are positive, and 𝑚𝑠𝑔[𝑖] = 0 if and only if the message
buﬀer of Process 𝑖 is empty. When a process receives multiple messages, it keeps the one attached
with the largest ID. Finally, we modify these commands to distinguish the case 𝑝𝑖𝑑 = 𝑛: for this
case, we replace 𝑝𝑖𝑑 + 1 with 1. We consider two correctness properties of the Chang-Roberts
algorithm:

             Formula           Deﬁnition                            Description
             𝑙𝑎𝑟𝑔𝑒𝑠𝑡 (𝑖)       ∀𝑗 . 𝑖𝑑 [𝑖] ≥ 𝑖𝑑 [ 𝑗 ]               Process 𝑖 has the largest ID
             𝑢𝑛𝑖𝑞𝑢𝑒 (𝑖)        ∀𝑗 . 𝑗 ≠ 𝑖 ⇒ 𝑖𝑑 [𝑖] ≠ 𝑖𝑑 [ 𝑗 ]       Process 𝑖 has a unique ID
             𝑒𝑙𝑒𝑐𝑡𝑒𝑑 (𝑖)       𝑚𝑠𝑔[𝑖] = 𝑖𝑑 [𝑖]                      Process 𝑖 is elected as a leader


              Property Speciﬁcation
              𝑃1            ∀𝑖. ¬𝑙𝑎𝑟𝑔𝑒𝑠𝑡 (𝑖) ∧ 𝑢𝑛𝑖𝑞𝑢𝑒 (𝑖) ⇒ G ¬𝑒𝑙𝑒𝑐𝑡𝑒𝑑 (𝑖)
              𝑃2            (∀𝑖. GF 𝑝𝑖𝑑 = 𝑖) ⇒ (∀𝑖. 𝑙𝑎𝑟𝑔𝑒𝑠𝑡 (𝑖) ∧ 𝑢𝑛𝑖𝑞𝑢𝑒 (𝑖) ⇒ F 𝑒𝑙𝑒𝑐𝑡𝑒𝑑 (𝑖))

Here, 𝑃1 is a safety property saying that a process not holding the largest ID is never elected as a
leader; 𝑃2 is a liveness property saying that a process holding the largest ID is eventually elected

                                Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
22:22                                                                                                Chih-Duo Hong and Anthony W. Lin


Table 2. Results of applying the 𝐿∗ learning-based model checker [Chen et al. 2017] and the SLRP
tool [Lin and Rümmer 2016] in the abstract analysis of the case studies. In the table, 𝑃0 denotes the progress
conditions, and 𝑃1, . . . , 𝑃4 are the temporal properties defined in Section 7. The table also shows the indexed
predicates we used to compute regular abstractions. Note that these predicates contain Skolem constants
produced in the formulae rewriting step of our method (see Section 6). For each property, we present the
total runtime (Total), the computation time of the initial and refined abstract systems (Model), and the time
consumed by the model checker (Solver).

                                               Safety Properties                                                        𝐿∗
            Name                                     Indexed Predicates                                       Total   Model    Solver
            s.sort 𝑃0                           𝑎[i] ≤ 𝑎[ℎ𝑖𝑔ℎ], 𝑎[i] ≤ 𝑎[𝑝]                                    0.5s    0.0s     0.4s
            s.sort 𝑃1                           𝑎[i] ≤ 𝑎[ℎ𝑖𝑔ℎ], 𝑎[i] ≤ 𝑎[𝑝]                                    3.7s    0.1s     3.4s
            s.sort 𝑃2                            𝑎[i] = 𝑎 0 [𝑝], 𝑎 0 [i] = 𝑎[𝑝]                                6.3s    0.3s     5.7s
            m.sort 𝑃0                 𝑎[i] ≥ 𝑎[𝑛], 𝑎[i] ≤ 𝑎[i + 1], 𝑎[i] ≤ 𝑎[𝑚𝑖𝑑]                              0.9s    0.1s     0.8s
            Dijk. 𝑃4                    𝑎[i] = 𝑎[i − 1], 𝑎[i] = 𝑎[𝑛], 𝑎[i] = 𝑎[1]                              1.2s    0.1s     1.0s
            C.-R. 𝑃1         𝑖𝑑 [i] = 𝑖𝑑 [𝑝], 𝑖𝑑 [i] < 𝑖𝑑 [𝑞], 𝑚𝑠𝑔[i] = 𝑖𝑑 [𝑝], 𝑚𝑠𝑔[i] < 𝑖𝑑 [𝑞]                3.3s    0.4s     2.7s
            C.-R. 𝑃0      𝑚𝑠𝑔[i] ≠ 0, 𝑠𝑡 [i] = 0, 𝑖𝑑 [i] < 𝑖𝑑 [𝑝], 𝑚𝑠𝑔[i] < 𝑖𝑑 [𝑝], 𝑚𝑠𝑔[i] = 𝑖𝑑 [𝑝]            8.4s    0.9s     7.2s

                              Liveness Properties                                              𝐿∗                             SLRP
    Name                              Indexed Predicates                            Total    Model      Solver     Total      Model      Solver
    s.sort 𝑃3                            no predicates                               0.7s     0.4s       0.2s       1.5s       0.1s       1.3s
    m.sort 𝑃1          𝑎[i] ≥ 𝑎[𝑛], 𝑎[i] ≤ 𝑎[i + 1], 𝑎[i] ≤ 𝑎[𝑚𝑖𝑑]                 5m47s     5m39s        5s        1.4s       0.1s       1.1s
    Dijk. 𝑃1             𝑎[i] = 𝑎[i − 1], 𝑎[i] = 𝑎[𝑛], 𝑎[i] = 𝑎[1]                   t.o.      –          –       12m54s        3s      12m50s
    Dijk. 𝑃3             𝑎[i] = 𝑎[i − 1], 𝑎[i] = 𝑎[𝑛], 𝑎[i] = 𝑎[1]                   t.o.      –          –       3m14s         2s       3m10s
    Dijk. 𝑃2                        𝑎[i] = 𝑧, 𝑎[i] = 𝑎[1]                          9m13s       4s       9m06s       n/a         –          –
    C.-R. 𝑃2    𝑠𝑡 [i] = 0, 𝑖𝑑 [i] < 𝑖𝑑 [𝑝], 𝑚𝑠𝑔[i] < 𝑖𝑑 [𝑝], 𝑚𝑠𝑔[i] = 𝑖𝑑 [𝑝]      3m04s      11s       2m51s       n/a         –          –


as a leader under the fairness requirement that each process is scheduled inﬁnitely often. The
validity of these properties relies on the assumption that the process IDs are unique. Thus, we
need to specify this assumption in the properties.

8     OPTIMIZATION AND EVALUATION

                𝑎 ′ = 𝑎{𝐼 ← 𝑎[𝐽 ]} 𝑎[𝐽 ] ⊲⊳ 𝑎[𝐾]              𝐼 ≠𝐾         𝑎 ′ = 𝑎{𝐽 ← 𝑒} 𝑎[𝐼 ] ⊲⊳ 𝑎[𝐾]           𝐽 ≠𝐼      𝐽 ≠𝐾
                                     ′        ′
                                    𝑎 [𝐼 ] ⊲⊳ 𝑎 [𝐾]                                         𝑎 ′ [𝐼 ] ⊲⊳ 𝑎 ′ [𝐾]

                𝑥′ = 𝐽     𝑎[𝐼 ] ⊲⊳ 𝑎[𝐾]          𝑎 ′ = 𝑎{𝐼 ← 𝑎[𝐽 ]} 𝑎[𝐽 ] ⊲⊳ 𝑛       𝑎 ′ = 𝑎{𝐽 ← 𝑒} 𝑎[𝐼 ] ⊲⊳ 𝑛             𝐼≠𝐽
                      ′         ′                             ′                                          ′
                     𝑎 [𝐼 ] ⊲⊳ 𝑎 [𝐾]                         𝑎 [𝐼 ] ⊲⊳ 𝑛                               𝑎 [𝐼 ] ⊲⊳ 𝑛

           𝑥′ = 𝐽       𝑎[𝐼 ] ⊲⊳ 𝑏 [𝐾]     𝑎 ′ = 𝑎{𝐼 ← 𝑏 [𝐽 ]} 𝑏 [𝐽 ] ⊲⊳ 𝑐 [𝐾]        𝑎 ′ = 𝑎{𝐽 ← 𝑒} 𝑎[𝐼 ] ⊲⊳ 𝑏 [𝐾]             𝐼≠𝐽
                 ′          ′                            ′         ′
                𝑎 [𝐼 ] ⊲⊳ 𝑏 [𝐾]                        𝑎 [𝐼 ] ⊲⊳ 𝑐 [𝐾]                                𝑎 ′ [𝐼 ] ⊲⊳ 𝑏 ′ [𝐾]

Fig. 1. Example constraint templates for updating and copying array contents, where ⊲⊳ ∈ {=, ≠, <, ≤, >, ≥}.
Each template consists of multiple premises and a consequence. The leftmost premise corresponds to an
update (i.e. the assignment part of a guarded command), and the rest of the premises come from the guard.
The consequence copies a predicate value from the current state to the next state. These templates exploit a
simplifying assumption that one guarded command updates precisely one index variable or array element.


   We have implemented a prototype to evaluate our approach over the case studies. The veriﬁca-
tion of an array system consists of two stages: (i) computing regular abstractions from the system
speciﬁcation, and (ii) performing abstract analysis based on these regular abstractions. When we
compute a regular abstraction as described in Section 5.2, a crucial step is to compute the constraint
cstr(𝜓 ) at (8), which could be obtained by enumerating the minimal unsatisﬁable cores (MUCs).

Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
Regular Abstractions for Array Systems                                                                          22:23


For this purpose, we ﬁrst compute MUCs for 𝜓 using the MUST tool [Bendík and Černá 2020].
Since the number of MUCs could be large, including all clauses induced by these MUCs in cstr(𝜓 )
is generally impractical. Instead, our tool computes the constraint in an incremental manner: we
sort these clauses by size, and include a clause only when the constraints generated by the smaller
clauses lead to spurious counterexample or timeout in the abstract analysis. As our experimen-
tal results have shown, most of the properties in our case studies can be veriﬁed by including a
moderate number of clauses in the state formulae abstractions.
   For transition formulae abstractions, we additionally use templates to capture constraints in-
volving array updates (Figure 1). We syntactically populate these templates with predicates and
index terms in 𝜓 and P to derive feasible clauses for cstr(𝜓 ). To illustrate, suppose that (𝑎[i] ≤
𝑎[𝑛]) ∈ P and 𝜓 := 𝑎[𝑝] ≤ 𝑎[𝑛] ∧ 𝑎 ′ = 𝑎{𝑖 ← 𝑎[𝑝]}. Then, the ﬁrst template in Figure 1 syntac-
tically derives a feasible clause {𝑖 = 𝑛, 𝑎 ′ [𝑖] ≤ 𝑎 ′ [𝑛]} for cstr(𝜓 ). (To see this, note that the ﬁrst
template is in the form of 𝐴 ∧ 𝐵 ∧ 𝐶 ⇒ 𝐷, which is equivalent to 𝐴 ∧ 𝐵 ⇒ {¬𝐶, 𝐷 }. By instan-
tiating 𝐴 to 𝑎 ′ = 𝑎{𝑖 ← 𝑎[𝑝]}, 𝐵 to 𝑎[𝑝] ≤ 𝑎[𝑛], 𝐶 to 𝑖 ≠ 𝑛, and 𝐷 to 𝑎 ′ [𝑖] ≤ 𝑎 ′ [𝑛], we obtain
the desired clause.) Although such clauses may also be produced using the incremental method
described earlier, we choose to generate them directly using templates as they are essential for
computing precise transition formulae abstractions.
   When computing an abstraction formula, we include singleton feasible clauses by default, and in-
crementally inject other nontrivial feasible clauses in the reﬁnement loop. For transition formulae,
we furthermore include clauses populated by templates. We convert the abstraction formulae of an
array system speciﬁcation into ﬁnite-state automata mechanically, leveraging Mona [Klarlund and Møller
2001] and Z3 [de Moura and Bjørner 2008]. These automata comprise an abstract regular transition
system for the concrete speciﬁcation. We then analyze this abstract system using suitable regular
model checkers in the literature. For safety properties, we perform the abstract analysis using the
safety veriﬁer by [Chen et al. 2017], which employs the 𝐿 ∗ learning algorithm to generate induc-
tive invariants. For liveness properties, we apply two independent, fully automated techniques:
one combines liveness-to-safety reduction techniques (see Section 6.5) with the safety veriﬁer by
Chen et al.; the other exploits the liveness veriﬁer SLRP [Lin and Rümmer 2016], which essentially
uses an SAT solver to synthesize well-founded relations. Note that our case studies contain two
liveness properties with fairness requirements (Dijkstra 𝑃2 and Chang-Roberts 𝑃2 ). SLRP can only
verify liveness under arbitrary schedulers and does not apply to these two properties.
   We conducted the experiments on a laptop computer with a 3.6GHz Intel i7 processor, a 16GB
memory limit, and a 20-minute timeout. Table 2 presents the results. For each of these properties,
our prototype tool can compute suﬃciently precise regular abstractions using constraints gener-
ated by no more than 10 clauses from the incremental and template-based methods. As for the
abstract analysis, the safety properties turn out to be relatively easy: all of them can be proved by
the 𝐿 ∗ safety veriﬁer in seconds. Regarding liveness properties, SLRP successfully proves all four
liveness properties not requiring fair schedulers, while the 𝐿 ∗ safety veriﬁer proves only one of
them, namely selection sort 𝑃3 , within the timeout. This property can be veriﬁed without using
any indexed predicates; the resulting abstract system thus degenerates into an integer program.
Reducing a liveness property to a safety property could be expensive: this operation accounts for
the majority of the runtime for verifying merge sort 𝑃1 , and is likely the main bottleneck in the
veriﬁcation of Dijkstra 𝑃1 and 𝑃3 by 𝐿 ∗ . Interestingly, the reduction takes a relatively short time for
Dijkstra 𝑃2 and Chang-Roberts 𝑃2 , and hence allows the safety veriﬁer to prove them in time. Since
these two properties hold only under fairness requirements, they cannot be handled by SLRP.




                               Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
22:24                                                                              Chih-Duo Hong and Anthony W. Lin


9 RELATED WORK
There is a huge body of research on the veriﬁcation of array programs and systems. In this section,
we provide some context for our work and discuss related work that has not yet been mentioned
elsewhere in the paper.
   Prior work exploiting predicate abstraction and interpolation exists in the context of verify-
ing quantiﬁed inductive invariants for array programs [Alberti et al. 2012b; Cimatti et al. 2016;
Jhala and McMillan 2007; Lahiri and Bryant 2007; McMillan 2008; Seghir et al. 2009]. Indexed pred-
icates, which are essentially predicates containing free index variables, were ﬁrst introduced by
Flanagan and Qadeer [Flanagan and Qadeer 2002] to compose universally quantiﬁed inductive
invariants. Lahiri and Bryant later extended and formalized this notion in the framework of in-
dexed predicate abstraction (IPA) [Lahiri and Bryant 2004a,b, 2007]. IPA encodes abstract state sets
as propositional formulae over Boolean variables, and universally quantiﬁes index variables in
the predicates when performing concretization. Since post-images of abstract states are generally
not computable in this setting, Lahiri and Bryant devised overapproximations of them using a
quantiﬁer instantiation heuristic, which enabled the authors to reduce abstract reachability anal-
ysis to solving quantiﬁed Boolean formulae. In comparison, our abstraction framework encodes
abstract state sets as ﬁrst-order formulae over word variables, and exploits regular languages to
overapproximate sets and relations in the abstract domain. These apparatuses allow us to rea-
son about quantiﬁed formulae and temporal properties beyond those considered by Lahiri and
Bryant. On the other hand, our abstraction function induces inﬁnite abstract systems, for which
we employ inﬁnite-state model checking techniques (i.e. regular model checking [Abdulla 2012;
Lin and Rümmer 2022]).
   For a class of array systems that are used to model multi-threaded programs, specialized predi-
cate abstraction techniques have been developed to infer universally quantiﬁed inter-thread prop-
erties. Many techniques along this line have focused on symmetric systems (i.e. the system be-
haves correctly regardless of thread arrangement [Basler et al. 2009; Donaldson et al. 2011, 2012;
Pani et al. 2023]) and monotonic systems (i.e. the system is equipped with a well-quasi-ordering
[Alberti et al. 2012a,b; Ranise and Ghilardi 2010]). Some techniques further abstract the target sys-
tem into a symmetric/monotonic system by combining predication abstraction with some form
of counter or monotonic abstraction (e.g. [Abdulla et al. 2010; Clarke et al. 2006, 2008; Ganjei et al.
2016; Kaiser et al. 2017]), thereby improving the expressiveness and eﬀectiveness of the abstraction
methods. Most of these techniques were designed for safety veriﬁcation, and it is unclear whether
they could be extended to handle liveness properties eﬀectively.
   Liveness veriﬁcation of array systems is much more diﬃcult than safety veriﬁcation, and there-
fore has relatively fewer automatic techniques and tool supports. In the context of multi-threaded
programs, thread-modular analysis [Cook et al. 2007; Ketema and Donaldson 2017; Malkis et al.
2007; Pani et al. 2021, 2023; Popeea and Rybalchenko 2012] is a popular veriﬁcation methodology.
The analysis considers each thread in isolation and overapproximates the behavior of the other
threads by assuming that their eﬀects are passive or irrelevant. Thread-modular analysis is there-
fore not suitable for verifying liveness properties that require coordination among threads. For
example, in the case of Dijkstra’s self-stabilizing algorithm, proving that Process 1 eventually up-
dates its local variable requires showing that the other processes collectively make progress on
updating their own variables. To reason about liveness properties relying on thread coordination,
Farzan et al. [Farzan et al. 2016] introduced well-founded proof spaces and quantiﬁed predicate au-
tomata (QPAs) for parameterized veriﬁcation. Like our approach, well-founded proof spaces take a
language-theoretic view of termination and reduce checking termination to showing the absence



Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
Regular Abstractions for Array Systems                                                                          22:25


of lasso-shaped counterexample paths. The veriﬁcation procedure provided by Farzan et al. ex-
plores symmetric proof spaces (i.e. proofs closed under permutation of thread identiﬁers). Also,
the procedure requires to iteratively check language inclusion of QPAs, which is itself an undecid-
able problem and yet to have an eﬀective implementation.
   Ivy [McMillan and Padon 2018, 2020] is a deductive veriﬁcation system that oﬀers an automatic
liveness-to-safety proof tactic for properties speciﬁed in LTL and a decidable fragment of pure
ﬁrst-order logic called Eﬀectively Propositional Logic (EPR). Speciﬁcally, Ivy reduces liveness to
safety for inﬁnite-state systems through dynamic abstraction [Padon et al. 2017, 2021], which is
an overapproximation of cycle detection by dynamically choosing a ﬁnite projection of an inﬁnite
path. Despite the automatic reduction to safety, the resulting safety property still needs to be
proved by the user. Moreover, Ivy does not support theory reasoning inherently, i.e., theories have
to be encoded in EPR. Notably, in Ivy’s abstraction scheme, the concrete speciﬁcation, the abstract
system, and the safety proof are all expressed in EPR. Our logical formalism is not limited to EPR
and directly supports array logic with background element theories. (Our presentation has used
the theory of Diﬀerence Arithmetic for array elements, as the theory already suﬃces to analyze
our case studies. But in principle, it is easy to adapt our techniques to other background theories
such as Linear Integer Arithmetic.)

10 CONCLUDING REMARKS
By combining indexed predicate abstraction, decision procedures, automatic structures, and regu-
lar model checking, we present a novel framework to verify linear-time properties of array systems.
Given a ﬁrst-order correctness speciﬁcation, our framework provides a systematic method to com-
pute regular overapproximations of the speciﬁcation as a string rewriting system, which allows
us to exploit a wealth of regular model checking techniques for analyzing both safety and liveness
properties. Our experimental results show that this approach is able to verify non-trivial properties
of array systems in several interesting case studies.
   There are several immediate future research directions. Firstly, existing regular model check-
ing techniques do not have good support for large alphabets. For this reason, the size of the re-
sulting regular abstraction may grow exponentially in the number of predicates, especially with
explicit representations of the letters (i.e. bitvectors). This leads to the following question: is it
possible to extend regular model checking with symbolic representations of the alphabet sym-
bols? We believe that the answer to this question is positive, given promising work in symbolic
automata learning [Argyros and D’Antoni 2018; Drews and D’Antoni 2017] and bitvector theory
SMT solving [Peled et al. 2023; Shi et al. 2021; Yao et al. 2020]. Secondly, our abstraction computa-
tion procedure currently uses simple incremental and template-based methods to search for con-
straints. We are conﬁdent that more sophisticated techniques such as the reﬁnement-based search
in IC3 [Cimatti et al. 2014; Komuravelli et al. 2015] can be integrated with our procedure for con-
straint discovery. Lastly, we have assumed in this work that appropriate indexed predicates have
been supplied. Generating nontrivial indexed predicates for array properties is very challenging.
In our case studies, we extract predicates from the atomic formulae of system and property speci-
ﬁcations. Thus far, this suﬃces for our current goal, which has been to demonstrate the expressive
power and viability of regular abstractions for array systems in interesting case studies. The next
step of our research is, therefore, to study automatic generation and reﬁnement of indexed predi-
cates.

ACKNOWLEDGMENTS
We thank the anonymous reviewers for their insightful comments and corrections. Chih-Duo
Hong is partly supported by the National Science and Technology Council, Taiwan, under grant

                               Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
22:26                                                                               Chih-Duo Hong and Anthony W. Lin


number 112-2222-E004-001-MY3. Anthony Lin is supported by European Research Council un-
der European Union’s Horizon 2020 research and innovation programme (grant agreement no
101089343).

REFERENCES
Martin Abadi. 1989. The power of temporal proofs. Theoretical Computer Science 65, 1 (1989), 35–83.
Parosh Aziz Abdulla. 2012. Regular Model Checking. International Journal on Software Tools for Technology Transfer (STTT)
   14, 2 (2012), 109–118.
Parosh Aziz Abdulla, Yu-Fang Chen, Giorgio Delzanno, Frédéric Haziza, Chih-Duo Hong, and Ahmed Rezine. 2010. Con-
   strained Monotonic Abstraction: A CEGAR for Parameterized Veriﬁcation. In International Conference on Concurrency
   Theory (CONCUR). Springer, 86–101.
Parosh Aziz Abdulla, Giorgio Delzanno, and Ahmed Rezine. 2009. Approximated Parameterized Veriﬁcation of Inﬁnite-
   State Processes with Global Conditions. Formal Methods in System Design (FMSD) 34, 2 (2009), 126–156.
Parosh Aziz Abdulla, Frédéric Haziza, and Lukáš Holík. 2016. Parameterized Veriﬁcation Through View Abstraction. In-
   ternational Journal on Software Tools for Technology Transfer (STTT) 18, 5 (2016), 495–516.
Parosh Aziz Abdulla, Bengt Jonsson, Marcus Nilsson, Julien d’Orso, and Mayank Saksena. 2012. Regular Model Checking
   for LTL(MSO). International Journal on Software Tools for Technology Transfer (STTT) 14, 2 (2012), 223–241.
Francesco Alberti, Roberto Bruttomesso, Silvio Ghilardi, Silvio Ranise, and Natasha Sharygina. 2012a. Lazy Abstrac-
   tion with Interpolants for Arrays. In International Conference on Logic Programming and Automated Reasoning (LPAR).
   Springer, 46–61.
Francesco Alberti, Roberto Bruttomesso, Silvio Ghilardi, Silvio Ranise, and Natasha Sharygina. 2012b. SAFARI: SMT-Based
   Abstraction for Arrays with Interpolants. In International Conference on Computer-Aided Veriﬁcation (CAV). Springer,
   679–685.
Francesco Alberti, Silvio Ghilardi, and Natasha Sharygina. 2017. A Framework for the Veriﬁcation of Parameterized Inﬁnite-
   State Systems. Fundamenta Informaticae 150, 1 (2017), 1–24.
George Argyros and Loris D’Antoni. 2018. The Learnability of Symbolic Automata. In International Conference on Computer
   Aided Veriﬁcation (CAV). Springer, 427–445.
Gérard Basler, Michele Mazzucchi, Thomas Wahl, and Daniel Kroening. 2009. Symbolic counter abstraction for concurrent
   software. In International Conference on Computer Aided Veriﬁcation (CAV). Springer, 64–78.
Jaroslav Bendík and Ivana Černá. 2020. MUST: minimal unsatisﬁable subsets enumeration tool. In Tools and Algorithms for
   the Construction and Analysis of Systems (TACAS). Springer, 135–152.
Jaroslav Bendík, Ivana Černá, and Nikola Beneš. 2018. Recursive online enumeration of all minimal unsatisﬁable subsets.
   In Automated Technology for Veriﬁcation and Analysis (ATVA). Springer, 143–159.
Michael Benedikt, Leonid Libkin, Thomas Schwentick, and Luc Segouﬁn. 2003. Deﬁnable Relations and First-Order Query
   Languages over Strings. Journal of the ACM (JACM) 50, 5 (2003), 694–751.
Roderick Bloem, Swen Jacobs, Ayrat Khalimov, Igor Konnov, Sasha Rubin, Helmut Veith, and Josef Widder. 2015. Decid-
   ability of Parameterized Veriﬁcation. Morgan & Claypool Publishers.
Achim Blumensath and Erich Gradel. 2000. Automatic Structures. In Symposium on Logic in Computer Science (LICS). IEEE,
   51–62.
Achim Blumensath and Erich Grädel. 2004. Finite Presentations of Inﬁnite Structures: Automata and Interpretations. Theory
   of Computing Systems (TCS) 37, 6 (2004), 641–674.
Ahmed Bouajjani, Peter Habermehl, and Tomáš Vojnar. 2004. Abstract Regular Model Checking. In International Conference
   on Computer-Aided Veriﬁcation (CAV). Springer, 372–386.
Ahmed Bouajjani, Bengt Jonsson, Marcus Nilsson, and Tayssir Touili. 2000. Regular Model Checking. In International
   Conference on Computer-Aided Veriﬁcation (CAV). Springer, 403–418.
Aaron R. Bradley and Zohar Manna. 1998. The Calculus of Computation: Decision Procedures with Applications to Veriﬁcation.
   Springer.
Aaron R. Bradley, Zohar Manna, and Henny B. Sipma. 2006. What’s Decidable about Arrays?. In International Conference
   on Veriﬁcation, Model Checking, and Abstract Interpretation (VMCAI). Springer, 427–442.
Ernest Chang and Rosemary Roberts. 1979. An Improved Algorithm for Decentralized Extrema-Finding in Circular Con-
   ﬁgurations of Processes. Communications of the ACM (CACM) 22, 5 (1979), 281–283.
Yu-Fang Chen, Chih-Duo Hong, Anthony W. Lin, and Philipp Rümmer. 2017. Learning to Prove Safety over Parameterised
   Concurrent Systems. In International Conference on Formal Methods in Computer-Aided Design (FMCAD). Springer, 76–
   83.
Alessandro Cimatti, Alberto Griggio, Sergio Mover, and Stefano Tonetta. 2014. IC3 Modulo Theories via Implicit Predicate
   Abstraction. In International Conference on Tools and Algorithms for the Construction and Analysis of Systems (TACAS).


Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
Regular Abstractions for Array Systems                                                                                22:27


   Springer, 46–61.
Alessandro Cimatti, Alberto Griggio, Sergio Mover, and Stefano Tonetta. 2016. Inﬁnite-state invariant checking with IC3
   and predicate abstraction. Formal Methods in System Design 49 (2016), 190–218.
Alessandro Cimatti, Alberto Griggio, and Gianluca Redondi. 2022. Veriﬁcation of SMT Systems with Quantiﬁers. In Inter-
   national Symposium on Automated Technology for Veriﬁcation and Analysis (ATVA). Springer, 154–170.
Alessandro Cimatti, Alberto Griggio, Gianluca Redondi, et al. 2021. Universal Invariant Checking of Parametric Systems
   with Quantiﬁer-free SMT Reasoning. In International Conference on Automated Deduction (CADE). Springer, 131–147.
Edmund Clarke, Muralidhar Talupur, and Helmut Veith. 2006. Environment Abstraction for Parameterized Veriﬁcation. In
   International Workshop on Veriﬁcation, Model Checking, and Abstract Interpretation (VMCAI). Springer, 126–141.
Edmund Clarke, Murali Talupur, and Helmut Veith. 2008. Proving Ptolemy Right: The Environment Abstraction Framework
   for Model Checking Concurrent Systems. In International Conference on Tools and Algorithms for the Construction and
   Analysis of Systems (TACAS). Springer, 33–47.
Edmund M. Clarke, Orna Grumberg, and Michael C. Browne. 1986. Reasoning about Networks with Many Identical Finite
   State Processes. In Symposium on Principles of Distributed Computing (PODC). ACM, 240–248.
Edmund M. Clarke Jr, Orna Grumberg, Daniel Kroening, Doron Peled, and Helmut Veith. 2018. Model Checking. MIT press.
Thomas Colcombet and Christof Löding. 2007. Transforming Structures by Set Interpretations. Logical Methods in Computer
   Science (LMCS) 3, 2 (2007), paper–4.
Byron Cook, Andreas Podelski, and Andrey Rybalchenko. 2007. Proving Thread Termination. In Programming Language
   Design and Implementation (PLDI). ACM, 320–330.
Patrick Cousot and Radhia Cousot. 1977. Abstract Interpretation: A Uniﬁed Lattice Model for Static Analysis of Programs
   by Construction or Approximation of Fixpoints. In Symposium on Principles of Programming Languages (POPL). ACM,
   238–252.
Jakub Daniel, Alessandro Cimatti, Alberto Griggio, Stefano Tonetta, and Sergio Mover. 2016. Inﬁnite-State Liveness-To-
   Safety via Implicit Abstraction and Well-Founded Relations. In International Conference on Computer-Aided Veriﬁcation
   (CAV). Springer, 271–291.
Leonardo Mendonça de Moura and Nikolaj Bjørner. 2008. Z3: An Eﬃcient SMT Solver. In International Conference on Tools
   and Algorithms for the Construction and Analysis of Systems (TACAS). Springer, 337–340.
Stéphane Demri, Valentin Goranko, and Martin Lange. 2016. Temporal logics in computer science: ﬁnite-state systems. Vol. 58.
   Cambridge University Press.
Edsger W. Dijkstra. 1982. Self-Stabilization in Spite of Distributed Control. In Selected Writings on Computing: A Personal
   Perspective. Springer, 41–46.
Alastair Donaldson, Alexander Kaiser, Daniel Kroening, and Thomas Wahl. 2011. Symmetry-aware predicate abstraction
   for shared-variable concurrent programs. In International Conference on Computer-Aided Veriﬁcation (CAV). Springer,
   356–371.
Alastair F. Donaldson, Alexander Kaiser, Daniel Kroening, Michael Tautschnig, and Thomas Wahl. 2012. Counterexample-
   Guided Abstraction Reﬁnement for Symmetric Concurrent Programs. Formal Methods in System Design (FMSD) 41, 1
   (2012), 25–44.
Samuel Drews and Loris D’Antoni. 2017. Learning Symbolic Automata. In Tools and Algorithms for the Construction and
   Analysis of Systems (TACAS), Vol. 10205. Springer, 173–189.
E. Allen Emerson and Kedar S. Namjoshi. 2003. On Reasoning about Rings. International Journal of Foundations of Computer
   Science 14, 04 (2003), 527–549.
Javier Esparza, Andreas Gaiser, and Stefan Kiefer. 2012. Proving termination of probabilistic programs using patterns. In
   International Conference on Computer-Aided Veriﬁcation (CAV). Springer, 123–138.
Azadeh Farzan, Zachary Kincaid, and Andreas Podelski. 2016. Proving Liveness of Parameterized Programs. In Symposium
   on Logic in Computer Science (LICS). IEEE, 1–12.
Grigory Fedyukovich, Sumanth Prabhu, Kumar Madhukar, and Aarti Gupta. 2019. Quantiﬁed Invariants via Syntax-Guided
   Synthesis. In Computer Aided Veriﬁcation (CAV). Springer, 259–277.
Paolo Felli, Alessandro Gianola, and Marco Montali. 2021. SMT-based safety checking of parameterized multi-agent systems.
   In Proceedings of the AAAI Conference on Artiﬁcial Intelligence (AAAI), Vol. 35. PKP Publishing, 6321–6330.
Tomáš Fiedor, Lukáš Holík, Petr Janků, Ondřej Lengál, and Tomáš Vojnar. 2017. Lazy Automata Techniques for WS1S. In
   International Conference on Tools and Algorithms for the Construction and Analysis of Systems (TACAS). Springer, 407–
   425.
Cormac Flanagan and Shaz Qadeer. 2002. Predicate Abstraction for Software Veriﬁcation. In Symposium on Principles of
   Programming Languages (POPL). ACM, 191–202.
Zeinab Ganjei, Ahmed Rezine, Petru Eles, and Zebo Peng. 2016. Counting dynamically synchronizing processes. Interna-
   tional Journal on Software Tools for Technology Transfer (STTT) 18 (2016), 517–534.



                                 Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
22:28                                                                                Chih-Duo Hong and Anthony W. Lin


Yeting Ge and Leonardo De Moura. 2009. Complete Instantiation for Quantiﬁed Formulas in Satisﬁability Modulo Theories.
   In International Conference on Computer Aided Veriﬁcation (CAV). Springer, 306–320.
Steven M. German and A. Prasad Sistla. 1992. Reasoning about Systems with Many Processes. Journal of the ACM (JACM)
   39, 3 (1992), 675–735.
Silvio Ghilardi, Alessandro Gianola, and Deepak Kapur. 2021. Interpolation and Amalgamation for Arrays with MaxDiﬀ.
   In International Conference on Foundations of Software Science and Computation Structures (FoSSaCS). Springer, 268–288.
Arie Gurﬁnkel, Sharon Shoham, and Yuri Meshman. 2016. SMT-Based Veriﬁcation of Parameterized Systems. In Interna-
   tional Symposium on Foundations of Software Engineering (FSE). ACM, 338–348.
Arie Gurﬁnkel, Sharon Shoham, and Yakir Vizel. 2018. Quantiﬁers on Demand. In Automated Technology for Veriﬁcation
   and Analysis (ATVA). Springer, 248–266.
Peter Habermehl, Radu Iosif, and Tomáš Vojnar. 2008. A Logic of Singly Indexed Arrays. In International Conference on
   Logic Programming and Automated Reasoning (LPAR). Springer, 558–573.
Ian Hodkinson, Frank Wolter, and Michael Zakharyaschev. 2000. Decidable Fragments of First-Order Temporal Logics. In
   Annals of Pure and Applied Logic. Elsevier, 181–185.
Jochen Hoenicke and Tanja Schindler. 2018. Eﬃcient interpolation for the theory of arrays. In International Joint Conference
   on Automated Reasoning (IJCAR). Springer, 549–565.
Chih-Duo Hong. 2022. Symbolic techniques for parameterised veriﬁcation. Ph. D. Dissertation. University of Oxford.
Ranjit Jhala and Kenneth L. McMillan. 2007. Array Abstractions from Proofs. In International Conference on Computer-Aided
   Veriﬁcation (CAV). Springer, 193–206.
Ranjit Jhala, Andreas Podelski, and Andrey Rybalchenko. 2018. Predicate Abstraction for Program Veriﬁcation: Safety and
   Termination. In Handbook of Model Checking. Springer, 447–491.
Alexander Kaiser, Daniel Kroening, and Thomas Wahl. 2017. Lost in abstraction: Monotonicity in multi-threaded programs.
   Information and Computation 252 (2017), 30–47.
Jeroen Ketema and Alastair F. Donaldson. 2017. Termination Analysis for GPU Kernels. Science of Computer Programming
   148 (2017), 107–122.
Nils Klarlund and Anders Møller. 2001. Mona Version 1.4: User Manual. BRICS, Department of Computer Science, University
   of Aarhus Denmark.
Nils Klarlund, Anders Møller, and Michael I. Schwartzbach. 2002. MONA Implementation Secrets. International Journal of
   Foundations of Computer Science 13, 04 (2002), 571–586.
Anvesh Komuravelli, Nikolaj S. Bjørner, Arie Gurﬁnkel, and Kenneth L. McMillan. 2015. Compositional Veriﬁcation of Pro-
   cedural Programs using Horn Clauses over Integers and Arrays. In Formal Methods in Computer-Aided Design (FMCAD).
   IEEE, 89–96.
Daniel Kroening and Ofer Strichman. 2016. Decision Procedures. Springer.
Shuvendu K. Lahiri and Randal E. Bryant. 2004a. Constructing Quantiﬁed Invariants via Predicate Abstraction. In Interna-
   tional Conference on Veriﬁcation, Model Checking, and Abstract Interpretation (VMCAI). Springer, 267–281.
Shuvendu K. Lahiri and Randal E. Bryant. 2004b. Indexed Predicate Discovery for Unbounded System Veriﬁcation. In
   International Conference on Computer-Aided Veriﬁcation (CAV). Springer, 135–147.
Shuvendu K. Lahiri and Randal E. Bryant. 2007. Predicate Abstraction with Indexed Predicates. ACM Transactions on
   Computational Logic (TOCL) 9, 1 (2007), 4–es.
Mark H. Liﬃton, Alessandro Previti, Ammar Malik, and Joao Marques-Silva. 2016. Fast, ﬂexible MUS enumeration. Con-
   straints 21 (2016), 223–250.
Anthony W. Lin and Philipp Rümmer. 2016. Liveness of Randomised Parameterised Systems under Arbitrary Schedulers.
   In International Conference on Computer-Aided Veriﬁcation (CAV). Springer, 112–133.
Anthony W. Lin and Philipp Rümmer. 2022. Regular model checking revisited. In Model Checking, Synthesis, and Learning:
   Essays Dedicated to Bengt Jonsson on The Occasion of His 60th Birthday. Springer, 97–114.
Haojun Ma, Aman Goel, Jean-Baptiste Jeannin, Manos Kapritsos, Baris Kasikci, and Karem A Sakallah. 2019. I4: incremen-
   tal inference of inductive invariants for veriﬁcation of distributed protocols. In The Symposium on Operating Systems
   Principles (SOSP). ACM, 370–384.
Alexander Malkis, Andreas Podelski, and Andrey Rybalchenko. 2007. Precise thread-modular veriﬁcation. In International
   Static Analysis Symposium (SAS). Springer, 218–232.
Makai Mann, Ahmed Irfan, Alberto Griggio, Oded Padon, and Clark Barrett. 2022. Counterexample-Guided Prophecy for
   Model Checking Modulo the Theory of Arrays. Logical Methods in Computer Science (LMCS) 18 (2022), 131–147.
Zohar Manna and Amir Pnueli. 2012. The Temporal Logic of Reactive and Concurrent Systems: Speciﬁcation. Springer Science
   & Business Media.
John McCarthy. 1993. Towards a mathematical science of computation. Program Veriﬁcation: Fundamental Issues in Com-
   puter Science 1, 1 (1993), 35–56.



Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
Regular Abstractions for Array Systems                                                                             22:29


Kenneth L. McMillan. 2008. Quantiﬁed Invariant Generation Using an Interpolating Saturation Prover. In International
   Conference on Tools and Algorithms for the Construction and Analysis of Systems (TACAS). Springer, 413–427.
Kenneth L. McMillan. 2018. Eager Abstraction for Symbolic Model Checking. In International Conference on Computer
   Aided Veriﬁcation (CAV). Springer, 191–208.
Kenneth L. McMillan and Oded Padon. 2018. Deductive Veriﬁcation in Decidable Fragments with Ivy. In International Static
   Analysis Symposium (SAS). Springer, 43–55.
Kenneth L. McMillan and Oded Padon. 2020. Ivy: A Multi-Modal Veriﬁcation Tool for Distributed Algorithms. In Interna-
   tional Conference on Computer Aided Veriﬁcation (CAV). Springer, 190–202.
Oded Padon, Jochen Hoenicke, Giuliano Losa, Andreas Podelski, Mooly Sagiv, and Sharon Shoham. 2017. Reducing Liveness
   to Safety in First-Order Logic. Symposium on Principles of Programming Languages (POPL) 2, POPL (2017), 1–33.
Oded Padon, Jochen Hoenicke, Kenneth L. McMillan, Andreas Podelski, Mooly Sagiv, and Sharon Shoham. 2021. Temporal
   prophecy for proving temporal properties of inﬁnite-state systems. Formal Methods in System Design (FMSD) 57 (2021),
   246–269.
Thomas Pani, Georg Weissenbacher, and Florian Zuleger. 2021. Rely-guarantee bound analysis of parameterized concurrent
   shared-memory programs: With an application to proving that non-blocking algorithms are bounded lock-free. Formal
   Methods in System Design (FMSD) 57, 2 (2021), 270–302.
Thomas Pani, Georg Weissenbacher, and Florian Zuleger. 2023. Thread-modular counter abstraction: automated safety
   and termination proofs of parameterized software by reduction to sequential program veriﬁcation. Formal Methods in
   System Design (FMSD) 60 (2023), 1–38.
Matan I Peled, Bat-Chen Rothenberg, and Shachar Itzhaky. 2023. SMT sampling via model-guided approximation. In
   International Symposium on Formal Methods (FM). Springer, 74–91.
Corneliu Popeea and Andrey Rybalchenko. 2012. Compositional Termination Proofs for Multi-Threaded Programs. In
   International Conference on Tools and Algorithms for the Construction and Analysis of Systems (TACAS). Springer, 237–
   251.
Silvio Ranise and Silvio Ghilardi. 2010. Backward Reachability of Array-Based Systems by SMT Solving: Termination and
   Invariant Synthesis. Logical Methods in Computer Science (LMCS) 6, 4 (2010), 25–44.
Viktor Schuppan and Armin Biere. 2006. Liveness Checking as Safety Checking for Inﬁnite State Spaces. Electronic Notes
   in Theoretical Computer Science (ENTCS) 149, 1 (2006), 79–96.
Mohamed Nassim Seghir, Andreas Podelski, and Thomas Wies. 2009. Abstraction Reﬁnement for Quantiﬁed Array Asser-
   tions. In Static Analysis Symposium (SAS). Springer, 3–18.
Xiaomu Shi, Yu-Fu Fu, Jiaxiang Liu, Ming-Hsien Tsai, Bow-Yaw Wang, and Bo-Yin Yang. 2021. CoqQFBV: A Scalable Certi-
   ﬁed SMT Quantiﬁer-Free Bit-Vector Solver. In International Conference on Computer Aided Veriﬁcation (CAV). Springer,
   149–171.
Dirk van Dalen. 1994. Logic and structure. Vol. 3. Springer.
Moshe Y. Vardi and Pierre Wolper. 1986. An Automata-Theoretic Approach to Automatic Program Veriﬁcation. In Sympo-
   sium on Logic in Computer Science (LICS). IEEE, 322–331.
Peisen Yao, Qingkai Shi, Heqing Huang, and Charles Zhang. 2020. Fast bit-vector satisﬁability. In International Symposium
   on Software Testing and Analysis (ISSTA). ACM, 38–50.

Received 2023-07-11; accepted 2023-11-07




                                 Proc. ACM Program. Lang., Vol. 8, No. POPL, Article 22. Publication date: January 2024.
