                                        Realizability in Semantics-Guided Synthesis Done Eagerly
                                        ROLAND MEYER, TU Braunschweig, Germany
arXiv:2403.05607v1 [cs.LO] 8 Mar 2024



                                        JAKOB TEPE, TU Braunschweig, Germany
                                        SEBASTIAN WOLFF, New York University, USA
                                        We present realizability and realization logic, two program logics that jointly address the problem of ﬁnding
                                        solutions in semantics-guided synthesis. What is new is that we proceed eagerly and not only analyze a
                                        single candidate program but a whole set. Realizability logic computes information about the set of candidate
                                        programs in a forward fashion. Realization logic uses this information as guidance to identify a suitable
                                        candidate in a backward fashion. Realizability logic is able to analyze a set of programs due to a new form of
                                        assertions that tracks synthesis alternatives. Realizability logic then picks alternatives to arrive at a program,
                                        and we give the guarantee that this process will not need backtracking. We show how to implement the
                                        program logics using veriﬁcation conditions, and report on experiments with a prototype in the context of
                                        safe memory reclamation for lock-free data structures.

                                        1 INTRODUCTION
                                        The syntax-guided synthesis (SyGuS) initiative [2, 3] has been instrumental in pushing the develop-
                                        ment of program synthesis technology. Key to this success has been the deﬁnition of a standardized
                                        input format that is solver independent: the format only refers to the synthesis task but does not
                                        constrain the synthesis technology. This means every SyGuS solver can, in principle, be applied
                                        to the entire SyGuS benchmark set, and the community can focus on comparing and improving
                                        the synthesis technology. A SyGuS task consists of a speciﬁcation of the desired program behavior
                                        and a grammar for the programs that may be chosen. The inherent limitation of SyGuS is that the
                                        grammar should refer to SMT expressions, expressions from logical theories that are supported by
                                        SMT solvers. SyGuS cannot handle expressions that fall outside the known logical theories, and
                                        for the expressions it can handle it assumes the standard semantics.
                                           Semantics-guided synthesis (SemGuS) [23] has recently been proposed as a successor of SyGuS
                                        that is meant to overcome the dependence on SMT expressions and describe synthesis problems
                                        in a domain-independent way. The key to domain independence is to add a third parameter to
                                        the deﬁnition of the synthesis problem, namely a deﬁnition of the program semantics. Giving the
                                        user the ability to deﬁne the program semantics dramatically increases the reach of SemGuS over
                                        SyGuS. The user can now deﬁne loop constructs and synthesize programs with complex control
                                        ﬂow. In fact, synthesizing full programs rather than logical expressions has been one of the goals
                                        behind SemGuS. It is a goal that SemGuS shares with solver-aided languages like Rosette [42] or
                                        Sketch [39]. Note, however, that Rosette and Sketch are neither solver nor domain independent.
                                        Rosette will not be able to read Sketch input and vice versa, and both can only draw conclusions
                                        about the standard semantics of the language. SemGuS allows the user to provide approximate
                                        semantics, and applications abound.
                                           Giving the user the ability to deﬁne the program semantics also dramatically increases the com-
                                        putational eﬀort of solving SemGuS tasks over SyGuS tasks. To come up with eﬃcient synthesis
                                        algorithms, it has turned out helpful to decompose the problem and develop algorithms dedicated
                                        to proving synthesis tasks unrealizable and algorithms for synthesizing solutions. For unrealizabil-
                                        ity, the state-of-the-art approach, implemented in the tool Messy [23] and its SyGuS precursors
                                        nay [19] and nope [18], is unrealizability logic [22]. Unrealizability logic tries to prove Hoare triples
                                        of the form {r }N{s}. The novelty is that N denotes a set of programs, and by proving the triple one
                                        shows that all programs in this set satisfy the pre-post speciﬁcation. The pre-post speciﬁcation is
                                        set-up in a way that validity of the triple means no program in the set can solve the SemGuS task
                                        at hand, hence the name unrealizability.

                                                                                                1
                                                               Roland Meyer, Jakob Tepe, and Sebastian Wolﬀ


   Our contribution is a new algorithm for realizability, for synthesizing solutions to SemGuS
tasks. The state-of-the-art tool for realizability, called Messy-Enum [23], implements the CEGIS
algorithm [40] algorithm for search-based synthesis [3]. Guided by knowledge about failed synthe-
sis attempts, Messy-Enum iteratively constructs candidate programs and checks every single one
of them for validity, i.e., for whether it solves the synthesis task. There is, however, an important
diﬀerence between SyGuS and SemGuS. In SyGuS, checking the validity of a candidate program
is cheap, it is an SMT query. In SemGuS, checking the validity of a candidate program is expen-
sive: Messy-Enum reduces it to a constraint Horn clause (CHC) query, and solving them may turn
out as hard as conducting a full veriﬁcation run. This is not unexpected, after all SemGuS aims to
synthesize full programs. But it means that search-based solvers have no chance to scale without
new strategies to reduce (i) the number of iterations and (ii) the cost of each iteration.
   Our algorithm reduces the number of iterations by analyzing sets of candidate programs for
validity, in an eager fashion, rather than a single one. What makes this scale is compositionality.
We construct the sets of programs bottom-up, starting from sets of commands to sets of more and
more complex programs. The key idea is to abstract the sets of programs to their input-output be-
havior. Abstracting single programs to their input-output behavior to compute over equivalence
classes is an idea that has been widely used in synthesis [1, 15, 36, 44, 46]. The novelty in our work
is eagerness: we abstract sets of programs whose input-output behavior does not match. Compo-
sitionality requires that the input-output is rich enough (i) to only reason with this abstraction,
without having to resort to the underlying programs, and (ii) to answer the realizability problem.
   We develop this idea in a new program logic [17]. Our realizability logic reasons over triples of
the form hRiP hSi, where P is a set of programs whose input-output behavior is given in the form
of a precondition R and a postcondition S. What is new is that the pre- and postcondition are not
single predicates, but sets of predicates. This reﬂects the fact that the programs in P are synthesis
alternatives. To achieve compositionality, it is important to get the notion of validity right. Given
hRiP hSi and hSiQhT i, we want to be able to conclude hRiP; QhT i, where P; Q contains all pro-
grams prog; prog′ with prog ∈ P and prog′ ∈ Q. The right choice is to reason backwards and
deﬁne validity
                  |=𝑎 hRiP hSi   by ∀s ∈ S. ∃r ∈ R. ∃prog ∈ P. |=𝑑 {r }prog{s} .
It is worth contrasting this deﬁnition with the notion of validity in the recent unrealizability
logic [22]. Their triples {r }P{s} are valid, if |=𝑑 {r }prog{s} holds for all programs prog ∈ P.
Moreover, note that r and s are single predicates, and not sets of predicates as in our case. In fact,
the paper explicitly asks for a realizability analogue of their unrealizability logic, and we named
our program logic after that proposal.
   The relation |=𝑑 {r }prog{s} is validity in classical Hoare logic. The index 𝑑 stands for demonic,
and indicates that the choice of the initial state in r as well as the choice of the execution in program
prog are made demonically, and the postcondition s has to over-approximate all the resulting states.
The index 𝑎 for validity |=𝑎 hRiP hSi in our synthesis logic stands for angelic, and indicates that the
choice of the predicate r in the precondition R as well as the choice of the program prog ∈ P are
made angelically, and the postcondition S is an under-approximation of all predicates s that can
be guaranteed. Assertions in our program logic are thus angelic choices over predicates, and these
predicates are demonic choices over states. To the best of our knowledge, there is no program logic
that would reason over such alternations in related work.
   Consider the program proof given in Figure 1. The program has two Boolean variables x and y
and two non-terminals, M that may be rewritten to x=0 or x=1 and N that may be rewritten to
y=0 or y=1. Starting from the set of all states, represented by the singleton predicate true, the two
programs represented by M give us two synthesis alternatives: we can guarantee x = 0 or we can

                                                   2
Realizability in Semantics-Guided Synthesis Done Eagerly


1 htruei                                                           1 htruei
2 M ( htrueix = 0 hx = 0i          |                               2 M (htruei x = 0 hx = 0i     |
3       htrueix = 1 hx = 1i );                                     3      htruei x = 1 hx = 1i );
4   hx = 0, x = 1i                                                 4   hx = 1i
5   N ( hx = 0, x = 1iy = 0hx = 0 ∧ y = 0, x = 1 ∧ y = 0i |        5   N (hx = 0, x = 1iy = 0hx = 1 ∧ y = 1i   |
6       hx = 0, x = 1iy = 1hx = 0 ∧ y = 1, x = 1 ∧ y = 1i );       6      hx = 1iy = 1hx = 1 ∧ y = 1i );
7   h𝑥 = 0 ∧ y = 0, . . . , x = 1 ∧ y = 1i                         7   hx = 1 ∧ y = 1i
8   assert (x = 1 ∧ y = 1)                                         8   assert (x = 1 ∧ y = 1)
9   hx = 1 ∧ y = 1, faili                                          9   hx = 1 ∧ y = 1i

 Fig. 1. Proof outline in realizability logic.                     Fig. 2. Proof outline derived from Figure 1.


guarantee x = 1. In both cases, we still do not have any knowledge about the value of y. We do
not yet make a decision, but use the two alternatives to consider the programs that can be derived
from N. This yields four synthesis alternatives, namely x=0 ∧ y=0 to x=1 ∧ y=1. Only the last of
these alternatives passes the assertion, the others lead to a failure of the execution.
   A ﬁrst point of criticism one may have about realizability logic is that the alternation between
angelic and demonic choice will explode too quickly. In the end, all we have done is to replace
the choice of a program by a powerset construction over predicates, a technique pioneered in
automata theory [37]. This merely translates a complex search into complex assertions. We argue
that, for SemGuS where validity checks are expensive, the assertions may be the right place to keep
the complexity. Formal methods has developed expressive logical languages and abstract domains
that can denote complex sets of states with very concise assertions. In our experiments, we have
worked with Cartesian abstraction [8, Chapter 9].
   A more severe point of criticism is that our realizability triples hRiP hSi drop the relationship
between the single programs prog ∈ P and the pre- and postconditions r ∈ R and s ∈ S that this
program can achieve. Hence, when we have given a proof in realizability logic, like the one in
Figure 1, all we know is that the program sketch M; N; assert(x = 1 ∧ y = 1) can be completed to
a program that passes the assertion, but we do not know the program. What we have, however, is a
proof outline in realizability logic that annotates the program with intermediary assertions. The
idea is to use this proof outline as guidance of how to instantiate the non-terminals.
   Our second contribution is realization logic, a program logic to derive rewriting steps po p∼ po′
between proof outlines in realizability logic. The guarantee given by realization logic is that valid
proof outlines are rewritten to valid proof outlines. The rewriting process will not only eliminate
alternatives from the deﬁnition of non-terminals until a program that satisﬁes the speciﬁcation
has been found. An equally important step is to eliminate predicates that will not be helpful to
satisfy the desired postcondition, or may even fail in the future. The elimination of predicates is
done backwards, starting from the postcondition, and we illustrate it on our example:
               hx = 0 ∧ y = 0, . . . , x = 1 ∧ y = 1iassert(x = 1 ∧ y = 1)hx = 1 ∧ y = 1, faili                    (1)
             p∼hx = 0 ∧ y = 0, . . . , x = 1 ∧ y = 1iassert(x = 1 ∧ y = 1)hx = 1 ∧ y = 1i                          (2)
             p∼hx = 1 ∧ y = 1iassert(x = 1 ∧ y = 1)hx = 1 ∧ y = 1i .
The ﬁrst step drops the alternative fail. As there are less synthesis options to choose from, this
weakens the postcondition and the step is thus sound by the standard rule of consequence in
Hoare logic. The second step propagates this elimination backwards by weakening the precon-
dition, which is rather uncommon in program logics. We can weaken the precondition, because
x = 1 ∧ y = 1 is suﬃcient to obtain the postcondition. For the following rewriting steps, it will be
helpful to consider Figure 2. We propagate the precondition x = 1 ∧ y = 1 to the postconditions of

                                                               3
                                                              Roland Meyer, Jakob Tepe, and Sebastian Wolﬀ


the alternatives for non-terminal N. Note that the proof outline remains valid although the alterna-
tive {x = 0, x = 1}y=0{x = 1 ∧ y = 1} is invalid. The point is that there is still the alternative y=1.
We eliminate the incorrect alternative in the next rewriting step. The backwards reasoning thus
revealed that the alternative y=0 will not help to satisfy the speciﬁcation. We then weaken the
precondition of the alternative y=1 and obtain the proof outline shown in the ﬁgure. The logic
will proceed along the same lines and identify the program x=1; y=1; assert(x = 1 ∧ y = 1) as a
solution to the synthesis task.
   Our third contribution is an algorithm to construct valid proof outlines in realizability logic. The
ambition is to avoid expensive CHC queries and get away with standard SMT queries, very much
like SyGuS. To achieve this, we are willing to rely on user guidance, namely the loop invariants
that are known to be crucial for veriﬁcation. Our algorithm is then a generalization of deductive
veriﬁcation to realizability logic. We start from a realizability triple whose program sketch comes
with invariant annotations. We show how to compute the missing intermediary assertions with
the help of strongest postconditions. From the resulting proof outline, we compute veriﬁcation
conditions: a set of constraints whose validity entails the validity of the proof outline (and the
annotations). Given that our assertions are new, we had to adapt the strongest postconditions
and the veriﬁcation conditions. The new deﬁnitions are made such that they can be handled by
standard technology: the postconditions can be computed in a symbolic way and the veriﬁcation
conditions can be discharged by an SMT solver.
   Our next contribution is to automate realization logic: we give an algorithm that rewrites proof
outlines until a solution to the synthesis problem has been found. Our algorithm is again based on
deductive veriﬁcation and solver support. The idea is to derive from the given proof outline (ordi-
nary) veriﬁcation conditions (over predicates rather than sets of predicates) whose validity proves
that a certain program is a solution to the synthesis problem. What is new is that the veriﬁcation
condition checks have to be interleaved with their construction, because they control the choice
of the program and thus the future veriﬁcation conditions. The choice of veriﬁcation conditions
is not unique but depends on the program as much as the argument why this program solves the
synthesis problem. Interestingly, we can show that there is a backtracking freedom guarantee: no
matter the choice, the synthesis is guaranteed to succeed. At a high level, this is a consequence of
the notion of validity in realzability logic.
   We implemented our algorithms for realizability and realization logic in a new tool. Given that
we have not yet developed generic assertion languages to deal with sets of sets of predicates,
our implementation is tied to one application domain: memory management in lock-free data
structures with the help of a safe memory reclamation algorithm. Due to the lock-free processing,
protecting a memory cell is not a mere call to the safe memory reclamation algorithm, but a com-
plicated sequence of calls followed by checks of global invariants that indicate whether a call has
been successful. The data structures include tricky ones like the ORVYY set and the DGLM queue,
the challenging protection is with ordered hazard pointers (the ﬁrst has priority over the second),
but we can also handle epochs. This set of case studies is interesting in several respects. It works
over an abstract data domain, namely the SMR types introduced in [27], and therefore cannot be
handled by solver-aided languages out-of-the-box (an encoding would be possible). The programs
contain unbounded loops, and therefore cannot be handled by SyGuS solvers. The places in which
to synthesize information are far apart, which means we have to capture the inﬂuence of complex
code on the to-be-synthesized information. Our approach handles all instances in a matter of sec-
onds. Moreover, we did not need any user annotations but were able to infer the required loop
invariants automatically.



                                                  4
Realizability in Semantics-Guided Synthesis Done Eagerly


   It may have become clear that we develop our algorithms in the context of an imperative pro-
gramming language that is parameterized in the data domain, the set of commands, and the se-
mantics of commands. We ﬁx the semantics of choice, sequential composition, and Kleene star. In
its original formulation, SemGuS is more liberal and would also take the operators for building
programs as a parameter. To generalize our work to that setting, the user would have to come up
with appropriate proof rules for the new operators. This is also the approach taken by unrealizabil-
ity logic [22]. We believe, however, that this should only be a second step. The parameterization
we work with is the standard assumption in program logics [5], and it has proven rich enough
to handle a large variety of benchmarks. In fact, it is rich enough to handle all examples that are
typically given to motivate SemGuS (C, Python, regular expressions, and bounded loops).
   To sum up, our contributions are the following.
     • Realizability logic (Section 3), the ﬁrst program logic to reason about realizability in Sem-
       GuS. The new idea is to have sets of predicates as assertions to represent synthesis alter-
       natives.
     • Realization logic (Section 4), the ﬁrst program logic to compute a solution to a SemGuS
       problem from a proof outline in realizability logic. The key idea of realization logic is to
       propagate failing synthesis attempts backwards, and eliminate unsuitable alternatives.
     • An algorithm to ﬁnd proofs in realizability logic (Section 5). We use deductive veriﬁcation
       and develop appropriate strongest postconditions and veriﬁcation conditions.
     • An algorithm to ﬁnd program derivations in realization logic (Section 6). Also here we rely
       on deductive veriﬁcation, and we can give a backtracking freedom guarantee.
     • We implemented our algorithms and applied them to synthesize the protection of memory
       accesses in a lock-free data structure by a safe memory reclamation algorithm (Section 8).
       The synthesis works over an abstract semantics of protection types, and the problem cannot
       be handled by state-of-the-art synthesizers.
  We start with a recapitulation of program logic, which forms the foundation of our work.

2 PRELIMINARIES
We introduce an imperative programming language that is parameterized in the data domain and
in the set of commands, and give a Hoare logic for it that will form the basis of our development.

2.1 Parameters
The development in this paper is parameterized in a triple (States, COM, È−É) which is given as part
of the synthesis task. The set States is the data domain, the set of states programs operate over.
There are no requirements, the set may be ﬁnite or inﬁnite. The set COM contains the commands
com that can be used in programs. The function È−É : COM → States → Predicates assigns to each
command a function from states to the set of predicates we deﬁne in a moment.

2.2 Programs
We use a classical while-language whose commands stem from the given set COM. Apart from that,
we have sequential composition, choice, and Kleene star:
                         prog      ::=    com | prog; prog | prog + prog | prog∗ .
We use Programs for the set of all programs. We use Execs for the set of all executions ex, programs
that neither contain choices nor loops. The function exec yields all executions that can originate
from a given program. For example, exec((com1 +com2 ); com) is the set {com1 ; com, com2 ; com}. Loops
are unrolled. Formally, we see the program as a regular expression and take the language.

                                                           5
                                                             Roland Meyer, Jakob Tepe, and Sebastian Wolﬀ


   To give the program semantics, we ﬁrst deﬁne Predicates = P (States) ∪ {fail}. Predicates are
sets of states or a distinguished element fail, and we typically use r, s, t for predicates. We have
sets of states to support non-determinism, and failure to track program crashes, due to problems
like segfaults or failing assertions. The predicates form a complete lattice with inclusion as the
ordering and fail as the top element: 𝑟 𝑑 𝑠 is deﬁned by 𝑠 = fail ∨ (𝑟 ≠ fail ∧ 𝑟 ⊆ 𝑠), and we
                                                    Ã
say that 𝑟 is more precise than 𝑠. We also write 𝑑 for the join. The index 𝑑 reminds us that the
non-determinism in programs is resolved demonically. Note that we formulated predicates in a
semantic way, there is no assertion language to denote sets of states. Nevertheless, we emphasize
that the inclusion in the formulation of 𝑟 𝑑 𝑠 corresponds to implication in logic, meaning the
deﬁnition can be implemented with solver technology right away.
   To give a semantics to executions, we ﬁrst lift the semantics
                                                         Ã         of commands from states to pred-
icates. We deﬁne ÈcomÉ(fail) = fail and ÈcomÉ(𝑟 ) = 𝑑 {ÈcomÉ(𝑠) | 𝑠 ∈ 𝑟 }, where 𝑟 ≠ fail. We
then set Èex1 ; ex2 É(𝑟 ) = Èex2 É(Èex1 É(𝑟 )). A consequence is that programs cannot recover from
failure.

2.3    Hoare Logic
We specify the correctness of programs by Hoare triples of the form {𝑟 }prog{𝑠}. The triple is valid,
if every possible execution of prog that starts in a state from 𝑟 ends in a state from 𝑠. We deﬁne
                      |=𝑑 {𝑟 }prog{𝑠}   by ∀ex ∈ exec (prog). ÈexÉ(𝑟 ) 𝑑 𝑠 .
   To derive valid triples in a compositional way, Hoare logic oﬀers proof rules similar to the
black ones in Figure 3, we just have to replace all angle brackets by set brackets, the indices 𝑎
by 𝑑, and assume 𝑅, 𝑆,𝑇 are predicates as we have deﬁned them above. Rule (COM) requires that
the postcondition over-approximates the eﬀect of the command on the precondition. Rule (SEQ)
composes programs sequentially if the intermediary assertion matches. Rule (LOOP) checks that
the predicate is invariant under the loop body. Rule (DEM) is commonly called choice and lets
the demon choose the alternative with which to continue the execution. The rule of consequence
(CSQ) lets us strengthen the precondition and weaken the postcondition. We use ⊢𝑑 {𝑟 }prog{𝑠} to
indicate that a Hoare triple can be derived with these proof rules. It is readily checked that these
rules are sound in that ⊢𝑑 {r }prog{s} implies |=𝑑 {r }prog{s}.
   One can also show that the rules are complete, |=𝑑 {r }prog{s} implies ⊢𝑑 {r }prog{s}. As we
will need it later, we explain the proof. The idea is to consider the full state space of program prog
from states in r. Now for each line of code, we collect all states from the state space that decorate
this line, and let them form a predicate. We construct a proof outline in which every line of code
carries the predicate we have just constructed as a precondition. One can now check that this proof
outline can be derived with the above rules.

3     REALIZABILITY LOGIC
We extend programs to program sketches that contain yet to be resolved non-terminals, and
present our program logic to reason about realizability.

3.1 Sketches
We extend the grammar of Programs by non-terminals N from a ﬁnite set N. The resulting sketches
are given by the grammar:
             sketch     ::=   com | sketch; sketch | sketch + sketch | sketch∗ | N .
We use Sketches for the set of all sketches. We assume each non-terminal N ∈ N comes with a
set of productions ∅ ≠ prod (N) ⊆ Sketches and usually write N ::= sketch1 | sketch2 rather

                                                  6
Realizability in Semantics-Guided Synthesis Done Eagerly


                              (SEQ)                                   (LOOP)                        (CSQ)
   (COM)                              ⊢𝑎 hRisketch1 hSi                     R = {r }                 R 𝑎 R′     S ′ 𝑎 S
     ÈcomÉ(r ) 𝑑 s                   ⊢𝑎 hSisketch2 hT i               ⊢𝑎 hRisketchhRi               ⊢𝑎 hR′ isketchhS ′ i
   ⊢𝑎 h {r } icomh {s} i      ⊢𝑎 hRisketch1 ; sketch2 hT i             ⊢𝑎 hRisketch∗ hRi              ⊢𝑎 hRisketchhSi

           (DEM)
                    R = {r }                        (ANG)                            (GATHER)
               ⊢𝑎 hRisketch1 hSi                    N ::= sketch | . . .                   ⊢𝑎 hR1 isketchhS1 i
               ⊢𝑎 hRisketch2 hSi                    ⊢𝑎 hRisketchhSi                        ⊢𝑎 hR2 isketchhS2 i
           ⊢𝑎 hRisketch1 + sketch2 hSi                 ⊢𝑎 hRiNhSi                     ⊢𝑎 hR1 ∪ R2 isketchhS1 ∪ S2 i


              Fig. 3. Rules of realizability logic. Extensions of Hoare logic are highlighted in blue.


                                                                       (SHARE)
1 htruei N ( x = 0 | x = 1); h𝑥 = 0, 𝑥 = 1i
                                                                           ⊢𝑎 h𝑇 iNh𝑈 i    ⊢𝑎 hRisketch[N/h𝑇 ih𝑈 i ] hSi
2 ( assert ( x ==0) + assert ( x ==1))
                                                                                          ⊢𝑎 hRisketchhSi
3 hfaili


              Fig. 4. Demonic choice.                                               Fig. 5. Subproof sharing.


than prod (N) = {sketch1 , sketch2 }. There may be more than two alternatives, and the sketches
may themselves contain non-terminals so that we have proper recursion. The pair (N, prod) of
non-terminals and their productions belong to the synthesis task and are given by the user.
  To lift the semantics from programs to sketches, we let the function drv determine all programs
(without non-terminals) that can be derived from a sketch by rewriting the non-terminals. For
example, with N ::= com1 | com2 we have drv(N; com) = {com1 ; com, com2 ; com}. Formally, we see
the sketch as a sentential form in a context-free grammar and take the language.

3.2 Realizability Logic
Realizability logic reasons over correctness speciﬁcation of the form hRisketchhSi. Here, R, S are
so-called selections from the set Selections = Pﬁn (Predicates). A selection is a ﬁnite set of predicates
as we have deﬁned them above. The idea is this. When we encounter a non-terminal in a sketch,
we do not yet determine how to resolve it to a program with the function drv. Instead, we collect
in a selection the predicates that these programs may justify as a postcondition. Since also the
precondition is a selection, we can not only choose the program but also the precondition to justify
the postcondition. We thus deﬁne validity of realizability triples via validity in Hoare logic:
      |=𝑎 hRisketchhSi             by        ∀s ∈ S. ∃r ∈ R. ∃prog ∈ drv(sketch). |=𝑑 {r }prog{s} .


   To derive valid realizability triples, we use the proof rules in Figure 3. We write ⊢𝑎 hRisketchhSi
if the realizability triple can be derived with the help of these rules. Rule (COM) checks whether
the eﬀect of a command com on a predicate r is captured by s. The rule allows us to derive the
realizability triple h{r }icomh{s}i in which the selections are singleton sets. The rule plays together
with (GATHER): if we can also derive h{r ′ }icomh{s′ }i for another pre- and postcondition, then we
can join the selections and obtain h{r, r ′ }icomh{s, s′ }i. Rule (GATHER) is also important to join
the pre- and postconditions for the various programs that can be derived from a non-terminal. To
obtain a realizability triple hRiNhSi, Rule (ANG) unwinds the non-terminal to a sketch sketch that
is given by a production and then proves hRisketchhSi. Note that the sketch may again contain

                                                             7
                                                               Roland Meyer, Jakob Tepe, and Sebastian Wolﬀ


N, and may contain more than one occurrence. We explain at the end of the section how to avoid
the repetition of proof trees and handle non-terminals in an eﬃcient way.
   Rule (DEM) looks like the standard rule for choice operators in Hoare logic. In realizability logic,
the precondition has to be a singleton selection, and the rule is unsound without this side con-
dition. If there were multiple predicates in R, then the synthesis from sketch1 and the synthesis
from sketch2 could use diﬀerent predicates. This would be incorrect, because the synthesis is
done at compile-time while the branch is chosen at runtime, and therefore the synthesis is not
allowed to react on the branch. To see this, consider the sketch in Figure 4 and let choice stand
for assert(x==0) + assert(x==1). Without the side condition, we could derive the realizability
triple ⊢𝑎 h𝑥 = 0, 𝑥 = 1ichoicehx = 0, x = 1i, because we could enter the left branch with the
predicate 𝑥 = 0 and the right branch with the predicate 𝑥 = 1. However, the programs we can
synthesize, namely x=0; choice and x=1; choice, have to commit to one of the assignments, and
therefore choice is doomed to fail. A similar reasoning applies for Rule (LOOP). The way to handle
multiple predicates in a precondition is to consider them one by one and join the results, again
using (GATHER).
   Rule (SEQ) reinforces the deﬁnition of validity for realizability triples. Consider |=𝑎 hRisketch1 hSi
and |=𝑎 hSisketch2 hT i. If validity was deﬁned by an existential instead of a universal quantiﬁer
over the postcondition, then it would not be sound to derive |=𝑎 hRisketch1 ; sketch2 hT i. The
point is that the existentially quantiﬁed predicate s1 ∈ S that is chosen to justify the validity of
the ﬁrst triple could diﬀer from the predicate s2 ∈ S needed for the second. There is an alternative
deﬁnition of validity that admits compositionality. We discuss it at the end of the following section
when we have developed the overall synthesis technique.
   It remains to discuss (CSQ). The rule of consequence needs an ordering on selections. We say
that selection R is more versatile than selection S, if for every predicate in S there is a more precise
predicate in R, so we deﬁne
                             R 𝑎 S       by     ∀s ∈ S. ∃r ∈ R. r 𝑑 s .
Having more predicates available makes a selection more versatile and having less predicates
makes a selection less versatile. It is also possible to have a more versatile selection with less
predicates if they are more precise. With this, ∅ is the least versatile and {∅} is the most versatile
selection.
   The rules are sound and, together with a rule for the edge case of an empty precondition that
we give in the appendix, also complete.
  Theorem 3.1 (Sound-And-Complete). ⊢𝑎 hRisketchhSi if and only if |=𝑎 hRisketchhSi .
   Proof. Soundness holds by an induction on the height of the proof tree. We argue for complete-
ness and consider |=𝑎 hRisketchhSi. By the deﬁnition of validity, this means for every predicate
s ∈ S there is a predicate r ∈ R and a program prog ∈ drv(sketch) so that |=𝑑 {r }prog{s}
holds. We invoke the completeness of Hoare logic and obtain ⊢𝑑 {r }prog{s}. The derivation can
be mimicked in realizability logic and yields ⊢𝑎 hriproghsi. Since the program has been derived
from sketch, we can also obtain ⊢𝑎 hrisketchhsi with ﬁnitely many applications of (ANG). Rule
(GATHER) allows us to join the triples hrisketchhsi and obtain the desired ⊢𝑎 hRisketchhSi. 

3.3 Discussion
  On SemGuS. The synthesis tasks we consider have the following input: the states, the commands,
and the semantics (States, COM, È−É) of the programming language, the non-terminals with their
production rules (N, prod), and the realizability triple hRisketchhSi of interest. In its original
formulation [23], SemGuS would be more liberal and allow the user to also deﬁne the operators

                                                   8
Realizability in Semantics-Guided Synthesis Done Eagerly


(their syntax and their semantics) from which programs can be built. We ﬁx those operators to
concatenation, choice, and Kleene star, instead. This allows us to work with an extension of Hoare
logic. To lift our approach to the more general setting, the user would have to specify the proof rules
that are sound for the new operators, which would be in-line with the approach in unrealizability
logic [22].
   The reader may also note that we have not made assumptions about the correctness speciﬁcation.
In synthesis, it is common to work with sets of examples. The work on unrealizability logic has
shown that such sets can be captured by so-called vector assertions [22]. Vector assertions are
predicates of a particular form, and our construction of selections readily applies to them.

  On search-based synthesis. Realizability logic is formulated such that it can be readily combined
with search-based synthesis. The point is that Rule (ANG) does not force us to consider all programs
a non-terminal can be rewritten to. Instead, we can consider a set of programs that appear most
promising, as can be judged from a probabilistic grammar [20].

   On the implementation of non-terminals. A non-terminal may occur multiple times in a proof in
realizability logic, it may even occur recursively. Rather than duplicating the subproofs for this non-
terminal, we would like to share them in the various places the non-terminal is used. This is made
possible by Rule (SHARE) given in Figure 5. If we have already derived the triple h𝑇 iNh𝑈 i, then we
can eliminate the non-terminal from a program sketch and replace it by the pair h𝑇 ih𝑈 i. The pair
stands for the fact that we can synthesize a program that transforms 𝑇 to 𝑈 . Rule (SHARE) is readily
checked to be sound. However, it is a derived rule whose application can easily be mimicked by
Rule (ANG), at the cost of blowing-up the proof. An implementation would reﬁne the rule so that
diﬀerent occurrences of the non-terminal can be replaced in diﬀerent ways. Moreover, one would
maintain a pointer to the subproof that should be inserted, to be able to derive the program with
the technique given next.

4 REALIZATION LOGIC
We deﬁne realization logic, a program logic to derive programs from sketches. The key insight
is that a proof outline in realizability logic for the sketch of interest is helpful guidance to ﬁnd a
program that solves the synthesis task. To make use of this guidance, realization logic rewrites the
given proof outline until a suitable program is found. Realization logic thus reasons over rewriting
steps of the form po p∼ po′ between proof outlines. The strategy behind the rewriting is to prop-
agate information about failed synthesis attempts backwards, and thereby iteratively eliminate
predicates from selections and productions from the deﬁnition of non-terminals.
   As we need a precise understanding of proof outlines, we give the deﬁnition:

                   po    ::=    hRicomhSi | po; po | po + po | po∗ | N(po) | (po | po) .

We write ⊢𝑎 po to indicate that the proof outline has been derived with realizability logic. The
assertions we track are the ones that have been used in the application of (SEQ), (LOOP), and (ANG).
The formal deﬁnition is in the appendix. We abuse the notation a bit and write hRipohSi to indicate
that R is the precondition and S is the postcondition of the proof outline po. This is well-deﬁned,
because ⊢𝑎 po1 + po2 implies that po1 and po2 have the same pre- and postcondition.
    The proof rules of realization logic are listed in Figure 6, we discuss them below. The rules give
the following soundness guarantee: if we start from a proof outline in realizability logic and rewrite
it to another proof outline, then also this proof outline can be derived with realizability logic.

  Theorem 4.1 (Soundness). ⊢𝑎 po and po p∼ po′ together imply ⊢𝑎 po′ .

                                                           9
                                                                                         Roland Meyer, Jakob Tepe, and Sebastian Wolﬀ


(RCOM)                                                       (RANG)                                                  (RSELECT)
 ÈcomÉ(r ) 𝑑 s        R 𝑎 {r }         S 𝑎 {s}                                po p∼ po′
         hRicomhSi p∼ h {r } icomh {s} i                      N(po1 | po | po2 ) p∼ N(po1 | po′ | po2 )              N(po1 | po | po2 ) p∼ po

          (RSEQL)                                                      (RSEQR)
                hRipo1 hSi p∼ hRw ipo′1 hSi                                          hSipo2 hT i p∼ hS w ipo′2 hT w i
           hRipo1 hSi; po2 p∼ hR   w
                                       ipo′1 hSi; po2                  hRipo1 hSi; hSipo2 hT i p∼ hRipo1 hS w i; hS w ipo′2 hT w i

                                                                                                                                  (RTRANS)
(RDEM)                                                                        (RLOOP)                                              po1 p∼ po2
 Rw = {r }        hRipo𝑖 hSi p∼ hRw ipo𝑖′ hS w i        for 𝑖 = 1, 2           h𝐼 ipoh𝐼 i p∼ h𝐼 w ipo′ h𝐼 w i      𝐼 w = {𝑖 }      po2 p∼ po3
hRipo1 hSi + hRipo2 hSi p∼ hRw ipo′1 hS w i + hRw ipo′2 hS w i                        h𝐼 ipo∗ h𝐼 i p∼ h𝐼 w ipo∗ h𝐼 w i             po1 p∼ po3

                                                        (RGATHER)
       (RCSQ)                                           R 𝑎 (R1 ∪ R2 )   S 𝑎 (S1 ∪ S2 )     sketch(po′1 ) = sketch(po′2 )
         hRipohSi p∼ hRww ipo′ hS w i                       hRipohSi p∼ hR1 ipo′1 hS1 i   hRipohSi p∼ hR2 ipo′2 hS2 i
         hRipohSi p∼ hRw ipo′ hS ww i                             hRipohSi p∼ hR1 ∪ R2 igather (po′1 , po′2 ) hS1 ∪ S2 i


                                                 Fig. 6. Rules of realization logic.



This allows us to invoke the soundness of realizability logic from Theorem 3.1 and obtain the
desired semantic guarantee for the program we have derived.
   A feature all rules share is that they are guided by the original proof outline: the selections in the
proof outline that results from rewriting are limited to the selections in the original proof outline.
To ease the notation, we use Rw to denote a selection that is known to be less versatile than R,
meaning R 𝑎 Rw holds. This may be used repeatedly, so R 𝑎 Rw 𝑎 Rww .
   The rules in Figure 6 rewrite the given proof outline in a compositional fashion. The base case
(RCOM) allows us to pick a pre- and postcondition from a selection. This is the moment we realize
that predicates from the precondition can be dropped because they are not needed to obtain the
postcondition, as shown in the introduction. We have to explicitly check the over-approximation
because realizability triples do not maintain the interplay between the predicates in the pre- and in
the postcondition. Using (RANG), we can rewrite proofs for the right-hand sides of non-terminals.
The heart of the calculus is (RSELECT), which allows us to replace non-terminals by their right-
hand sides. The Rules (RSEQL) and (RSEQR) rewrite the left resp. the right part of a sequence. In
(RSEQL), it is important that the new intermediary assertion matches the original intermediary
assertion. This does not have to be the case in (RSEQR), which uses the rule of consequence to
automatically weaken the postcondition on the left. As in realizability logic, Rule (RDEM) forces
us to commit to a predicate when reasoning about demonic choices. It also produces the same
postcondition 𝑆 w in both branches. Rule (RLOOP) for rewriting loop bodies has a similar behavior.
The rule of consequence (RCSQ) is used like in realizability logic. The same is true for (RGATHER),
which uses function gather to recursively join the intermediary assertions in the proof outlines.
The deﬁnition is in the appendix. The need for this function stems from the fact that (RDEM) can
only work with single predicates. Rule (TRANS) is the transitivity of rewriting. This rule is needed
to combine rewrites, for example when rewriting the left and the right part of a sequence.
   Realization logic always rewrites a proof outline into one that is weaker in the sense that it has
less synthesis options or, phrased diﬀerently, is closer to a program.

  Lemma 4.2. po p∼ po′ implies po 𝑝 po′ .

                                                                         10
Realizability in Semantics-Guided Synthesis Done Eagerly


The ordering po 𝑝 po′ states that po′ has less versatile assertions than po and a sketch or even
program that can be derived from the sketch in po. The deﬁnition is by induction on the structure
of proof outlines. The base case is hRicomhSi 𝑝 hRw icomhS w i. The step cases are similar to the
one for choice: po1 + po2 𝑝 po′1 + po′2 if po1 𝑝 po′1 and po2 𝑝 po′2 . Non-terminals are an
exception, where we use N(po1 | po | po2 ) 𝑝 N(po1 | po′ | po2 ) if po 𝑝 po′ . A proof outline over
a non-terminal is also stronger than a proof outline over a derivative, N(po1 | po | po2 ) 𝑝 po.
   Realization logic also has a completeness property: proof outlines can be rewritten into all
weaker proof outlines that are derivable in realizability logic.
  Theorem 4.3 (Completeness). ⊢𝑎 po and ⊢𝑎 po′ and po 𝑝 po′ together imply po p∼ po′ .
  A ﬁnal guarantee that is interesting from an algorithmic point of view is that realization logic
provably does not need backtracking: from every proof outline and for every predicate in the
postcondition, one can derive a program that satisﬁes this postcondition. By Theorem 4.1, the
guarantee continues to hold after a rewriting step (that should not remove the predicate of interest),
hence the name.
  Theorem 4.4 (Backtracking Freedom). Let ⊢𝑎 hRipohSi and s ∈ S. Then there are r and po′ so
that hRipohSi p∼ h{r }ipo′ h{s}i, r ∈ R, and sketch(po′ ) ∈ drv(sketch(po)).
   It is tempting to try to prove backtracking freedom with the help of completeness in Theorem 3.1.
To understand why this does not work, consider the valid proof outline given in Figure 7 and sup-
pose both commands have the same semantics, namely the identity function. When we want to de-
rive a program for the postcondition {x = 0}, realization logic can only propose skip1 . The notion
of validity in realizability logic, however, may justify the postcondition by |=𝑑 {x = 0}skip2 {x = 0}.
Completeness in Theorem 3.1 now shows that there is a proof outline for ⊢𝑎 hx = 0iskip2 hx = 0i.
The point is that this proof outline is not weaker than the one in Figure 7. This also means that there
is no contradiction to Theorem 4.3. In short, Theorem 3.1 reasons about sketches and Theorem 4.4
reasons about proof outlines, and the two are incomparable.
   For an example application of realization logic, we refer 1 h𝑥 = 0i
to Section 1. Eliminating the predicate fail in Equation (1) is 2 N (( h𝑥 = 0i skip 1 h𝑥 = 0i) |
an application of Rule (RCSQ). Weakening the precondition in 3              (h𝑥 = 0i skip 2 h∅i ))
Equation (2) is an application of Rule (RCOM). Resolving the non- 4 h𝑥 = 0i
terminal to the left production is an application of rule (RSELECT).
The resulting proof outline fragments are put together using                    Fig. 7. Guidance.
Rules (RSEQL), (RSEQR), and (RTRANS).
   Overall approach and the notion of validity. The overall approach to synthesizing a program from
a sketch sketch, a precondition R, and postcondition S is this. We prove the triple hRisketchhSi
in realizability logic. One may see this proof as a symbolic execution that annotates the code by
assertions in a forward fashion, starting from the precondition and ending at the postcondition.
When we have proven the triple, we in particular have a proof outline at hand. We rewrite this
proof outline to a program using the realization logic we have just developed. The rewriting pro-
ceeds backwards: starting from failures and predicates that do not guarantee the postcondition, we
eliminate predicates from selections and productions from the deﬁnition of non-terminals.
   We need the rewriting phase because realizability logic abstracts away the link between the
programs that can be synthesized from the sketch and the pre- and postconditions that these
programs can guarantee. This abstraction is precisely what makes realizability logic scale, and the
link is precisely what realization logic recovers. What makes realization logic eﬃcient is that it is
guided by the proof outline in realizability logic. Moreover, realizability logic provably does not
need backtracking (the rewriting cannot go wrong).

                                                           11
                                                                Roland Meyer, Jakob Tepe, and Sebastian Wolﬀ


  It would be possible to deﬁne the notion of validity in realizability logic diﬀerently, namely by
universally quantifying over the precondition and existentially quantifying over the postcondition.
Our synthesis approach can be adapted to this deﬁnition as follows. We imagine the proof in realiz-
ability logic as being constructed backwards, the symbolic execution starts from the postcondition
and proceeds to the precondition. Realization logic would then start from unsuitable preconditions
and proceed forwards. Our approach has the advantage that forward reasoning tends to be more
deterministic than backwards reasoning, which leads to smaller assertions in realizability logic.

5 IMPLEMENTING REALIZABILITY LOGIC
We give an algorithm that checks the validity of triples in realizability logic. The algorithm also
yields a proof outline that will be handed over to the implementation of realization logic developed
in the next section. The algorithm is a deductive veriﬁcation: we compute a set of veriﬁcation
conditions whose validity entails the validity of the given realizability triple. Importantly, although
the assertions in realizability logic are selections rather than mere predicates, the validity check can
be discharged with an oﬀ-the-shelf SMT solver. At the technical level, our contribution lies in the
deﬁnition of suitable veriﬁcation conditions. We proceed forwards, using a tailor-made strongest
post. Deductive veriﬁcation needs loop invariants, and this is no diﬀerent in our case. We assume
these invariants are given by the user. Moreover, we assume the user gives us information about
the non-terminals, either in the form of an annotated assertion transformer, or in the form of a
recursion depth to which the non-terminal should be unwound in the search for a program. Taking
these user annotations as an input is a compromise: it is a burden on the user, but it improves the
applicability of the method. Having said that, we remark that in our experiments we were able to
automatically determine the loop invariants and handle the non-terminals.

5.1 Verification Conditions and Strongest Post
In Figure 8, we deﬁne the function vc : annRealizabilityTriples → P (VerifConds) which takes
an annotated realizability triple and produces a set of veriﬁcation conditions. The annotation we
assume is an invariant 𝐼 in the case of loops sketch∗ , denoted by sketch∗ [𝐼 ], and a selection trans-
former Γ : Selections → Selections in the case of non-terminals N, written as N[Γ]. A veriﬁcation
condition is an inequality between selections from the set VerifConds = Selections × Selections.
   We rely on the correctness of the annotations. A loop invariant is sound, if |=𝑎 h{𝑖}isketchh{𝑖}i
holds for all 𝑖 ∈ 𝐼 . It is complete if |=𝑎 h{ 𝑗 }isketchh{ 𝑗 }i implies 𝑗 ∈ 𝐼 . A selection transformer is
sound, if Γ(R) = S implies |=𝑎 hRiNhSi. It is complete, if |=𝑎 hRiNhSi implies Γ(R) 𝑎 S.
   Function vc is sound: when all veriﬁcation conditions hold, then the realizability triple is valid.
Note that we do not need to assume the soundness of the annotations, but will check this as part
of the veriﬁcation conditions. For completeness, however, we need to make this assumption.
   Theorem 5.1 (VC-Sound-And-Complete). |= vc(hRisketchhSi) implies |=𝑎 hRisketchhSi. If
all annotations are complete, |=𝑎 hRisketchhSi implies |= vc(hRisketchhSi).
    The beneﬁt of using veriﬁcation conditions R 𝑎 S as the proof obligation is that they can be
discharged with oﬀ-the-shelf SMT technology. For every predicate s ∈ S, we have to go through
the predicates r ∈ R until we ﬁnd r ⊆ s. This means at most quadratically many SMT queries.
Future assertion languages for selections may suggest a diﬀerent strategy.
    Function vc makes use of the strongest post function sp which is also deﬁned in Figure 8. It takes
as input a selection and a sketch and outputs a selection, sp : (Selections × Sketches) → Selections.
The output is a selection that can be guaranteed when running the sketch on the input. Moreover,
it is the most versatile selection, if the annotations are complete. Since the result does not refer to
the veriﬁcation conditions, we have to require soundness.

                                                    12
Realizability in Semantics-Guided Synthesis Done Eagerly


                      sp(R, com) := {ÈcomÉ(r ) | r ∈ R}                               sp(R, N[Γ] ) := Γ (R)
       sp (R, sketch1 ; sketch2 ) := sp (sp (R, sketch1 ), sketch2 )          sp (R, sketch∗ [𝐼 ] ) := {𝑖 ∈ 𝐼 | R 𝑎 {𝑖 } }
                 sp(R, sketch1 + sketch2 ) := {s1 ⊔𝑑 s2 | s𝑘 ∈ sp ( {r }, sketch𝑘 ) ∧ r ∈ R ∧ 𝑘 ∈ {1, 2} }

          vc (hRicomhSi) := {sp (R, com) 𝑎 S }               vc (hRiN[Γ] hSi) := {sp(R, N[Γ] ) 𝑎 S } ∪ ca(R, N, Γ)
        vc (hRisketch1 ;sketch2 h𝑆 i) := vc (hRisketch1 hsp (R, sketch1 ) i) ∪ vc (hsp(R, sketch1 ) isketch2 hSi)
               vc (hRisketch∗ [𝐼 ] hSi) := {sp (R, sketch∗ [𝐼 ] ) 𝑎 𝑆 } ∪ ca(𝐼, sketch∗ )
       vc (hRisketch1 + sketch2 hSi) := (∪{vc (h {r } isketch𝑘 hsp ( {r }, sketch𝑘 ) i ) | r ∈ R ∧ 𝑘 ∈ {1, 2} } )∪
                                            {sp (R, sketch1 + sketch2 ) 𝑎 S }

ca(R, N, Γ) := ∪ {vc (hRiproghsp(R, prog) i ) | min 𝑗 : (∪{sp (R, prog′ ) | prog′ ∈ O(N, 𝑗 ) } ) 𝑎 Γ (R) ∧ prog ∈ O(N, 𝑗 ) }
                                    ca(𝐼, sketch∗ ) := {vc (h {𝑖 } isketchh {𝑖 } i ) | 𝑖 ∈ 𝐼 }


       Fig. 8. Definitions of strongest post, verification conditions, and check annotation functions.


  Theorem 5.2 (SP-Sound-And-Complete). If the annotations are sound, sp(R, sketch) 𝑎 S
implies |=𝑎 hRisketchhSi. If the annotations are sound and complete, |=𝑎 hRisketchhSi implies
sp(R, sketch) 𝑎 S.
    The functions vc and sp are deﬁned inductively over the structure of sketches. The novelty
is in the cases for demonic choices, non-terminals, and loops. For demonic choices, recall that
Rule (DEM) reasons over single predicates. The strongest post thus iterates through the predicates
in the given precondition. For each r ∈ R , it computes the strongest post for both branches. If we
have s1 ∈ sp({r }, sketch1 ), then we can guarantee the predicates s1 when running sketch1 on r.
The same holds for s2 ∈ sp({r }, sketch2 ). But as the branch will be chosen demonically, we can
only enforce the least upper bound of s1 and s2 . However, we are free to combine all s1 with all
s2 . This explains the deﬁnition. The veriﬁcation conditions check each branch individually, again
with a singleton precondition. Moreover, they check whether the strongest post is suﬃcient to
prove the postcondition.
    For non-terminals, the strongest post is given by the annotated transformer. The veriﬁcation
conditions check whether the strongest post entails the postcondition. Moreover, they check the
soundness of the annotation with the function ca(R, N, Γ). We elaborate on it in a moment. For
loops, we rely on an annotated invariant. The strongest post keeps only those predicates from the
invariant that follow from the precondition. The veriﬁcation conditions again check whether the
strongest post entails the postcondition. Moreover, they check whether the invariant annotation
is sound via ca(𝐼, sketch∗ ).
    Soundness of a loop invariant is easy to check. Since Rule (LOOP) can only enter a loop with a
singleton, we check each predicate in 𝐼 for being an invariant. The soundness of transformers is
more diﬃcult to check. Function ca(R, N, Γ) tries to derive a set of programs from N which justiﬁes
the postcondition Γ(R). To this end, it repeatedly invokes an oracle O which returns programs
from drv(𝑁 ). The function O(N, 𝑗 ) returns the ﬁrst 𝑗 programs the oracle produces for the non-
terminal N. If the set of programs that have been returned so far is able to produce the postcondition,
ca(R, N, Γ) collects the corresponding veriﬁcation conditions and terminates. The only guarantee
we need about the oracle is that every program will eventually be returned. If the transformer
is sound, we will eventually obtain a large enough set of programs. Otherwise, the veriﬁcation
condition generation will not terminate. A simple implementation for an oracle is to return the
programs that can be obtained by unrolling each non-terminal at most 𝑘 times, for larger and
larger 𝑘.

                                                               13
                                                                Roland Meyer, Jakob Tepe, and Sebastian Wolﬀ


5.2 Example: Checking Realizability of the Factorial Function
We illustrate the veriﬁcation condition computation on an example. Consider the sketch depicted
in Figure 9. We check whether we can derive from it a program that computes the factorial of 42:
the precondition of interest is R = {x = 42 ∧ y = 1} and the postcondition is S = {y = 42!}. The
sketch is already annotated by the results of the strongest post in grey, the loop is annotated by
the invariant 𝐼 = {y ∗ x! = 42! ∧ x ≥ 0}, and the non-terminal N::= y=y+x | y=y*x is annotated
by the transformer Γ with Γ(R) = sp(R, y=y+x) ∪ sp(R, y=y*x). We refer to the sketch as sketch,
the loop body as body, and the commands by their line number, so x-- is 17. We abbreviate the
non-terminal including Lines 6 to 14 by N.
   We explain the computation of the veriﬁcation conditions, which returns
    vc(hRisketchhSi) = {sp(𝐼, 22) 𝑎 S,                            𝐼 𝑎 𝐼 (𝐼 = sp(R, body∗ [𝐼 ])),       (3)
                            sp({𝑖}, 4;N;17) 𝑎 {𝑖},                       sp({𝑖}, 4) 𝑎 sp({𝑖}, 4),      (4)
                            sp({𝑖}, 4;N) 𝑎 sp({𝑖}, 4;N),           sp({𝑖}, 4;8) 𝑎 sp({𝑖}, 4;8),        (5)
                            sp({𝑖}, 4;12) 𝑎 sp({𝑖}, 4;12)} .                                            (6)
Executing vc(hRisketchhSi) yields two recursive calls:
     vc(hRisketchhSi) = vc(hRibody∗ [𝐼 ] hsp(R, body∗ [𝐼 ])i) ∪ vc(hsp(R, body∗ [𝐼 ])i22hSi) .
To calculate the strongest post of the loop, R and each individual element of the loop invariant have
to be compared. Since 𝐼 = {𝑖} is a singleton and R 𝑎 {𝑖}, we have that 𝐼 itself is the strongest post
of the loop. Therefore, the second recursive call boils down to checking sp(𝐼, assume x = 0) 𝑎 S,
Inequality (3)(left). Next, we invoke vc(hRibody∗ [𝐼 ] hsp(R, body∗ [𝐼 ])i). We already argued that
the strongest post of the loop is the loop invariant. Thus, 𝐼 𝑎 𝐼 is added as Inequality (3)(right).
Checking the loop invariant annotation with ca(𝐼, body∗ ) returns vc(h{𝑖}ibodyh{𝑖}i). This, in turn,
yields two calls to the veriﬁcation conditions function:
            vc(h{𝑖}ibodyh{𝑖}i) = vc(h𝑖i4;Nhsp({𝑖}, 4;N)i) ∪ vc(hsp({𝑖}, 4;N)i17h𝑖i) .
For the second recursive call, the base case of function vc(−) applies and adds sp({𝑖}, 4;N;17) 𝑎
{𝑖} to the output, Inequality (4)(left). The ﬁrst recursive call yields
        vc(h𝑖i4;Nhsp({𝑖}, 4;N)i) = vc(h𝑖i4hsp({𝑖}, 4)i) ∪ vc(hsp({𝑖}, 4)iNhsp({𝑖}, 4;N)i) .
The ﬁrst of these calls adds sp({𝑖}, 4) 𝑎 sp({𝑖}, 4), Inequality (4)(right). The second recursive call
is for the non-terminal. Inequality sp({𝑖}, 4;N) 𝑎 sp({𝑖}, 4;N) checks entailment of the postcon-
dition, Inequality (5)(left). For soundness of the annotation, ca(sp({𝑖}, 4), N, Γ) is called. For 𝑗 = 2,
the oracle proposes the programs y=y+x and y=y*x. See that by our deﬁnition of the selection
transformer Γ, the inequality sp(R, y=y+x) ∪ sp(R, y=y*x) 𝑎 Γ(R) holds. Thus, the function ca
outputs two more inequalities (after resolving the recursive calls to the base case of vc): the in-
equality sp({𝑖}, 4; 8) 𝑎 sp({𝑖}, 4; 8) considers the ﬁrst production resolving the nonterminal and
the inequality sp({𝑖}, 4; 12) 𝑎 sp({𝑖}, 4; 12) considers the second production. Both inequalities are
added to the output, Inequality (5)(right) and Inequality (6).
   All inequalities of vc(hRisketchhSi) hold and so |=𝑎 hRisketchhSi by Theorem 5.1. This means,
the non-terminal can be resolved such that the resulting program will compute the factorial of 42.
We present next an algorithm to automatically choose the correct branch.

6   IMPLEMENTING REALIZATION LOGIC
We give an algorithm to compute a program from a proof outline in realizability logic. It is a deduc-
tive veriﬁcation that collects a set of veriﬁcation conditions whose validity shows that the program
is a solution to the synthesis task. What is unconventional is that the validity has to be checked in

                                                   14
Realizability in Semantics-Guided Synthesis Done Eagerly



1 hx = 42 ∧ y = 1i                                          13           h (y/x) ∗ x! = 42! ∧ x > 0i
2 (                                                         14       )
3     hy ∗ x! = 42! ∧ x ≥ 0i                                15       h (y − x) ∗ x! = 42! ∧ x > 0,
4     assume ( x > 0);                                      16           (y/x) ∗ x! = 42! ∧ x > 0i
5     hy ∗ x! = 42! ∧ x > 0i                                17       x - -;
6     N [Γ] (                                               18       h (y − (x + 1) ) ∗ (x + 1)! = 42! ∧ x + 1 > 0,
7        hy ∗ x! = 42! ∧ x > 0i                             19           (y/(x + 1) ) ∗ (x + 1)! = 42! ∧ x + 1 > 0i
8        y = y + x;                                         20   ) ∗ [ {y ∗ x! = 42! ∧ x ≥ 0} ]
9        h (y − x) ∗ x! = 42! ∧ x > 0i                      21   hy ∗ x! = 42! ∧ x ≥ 0i
10        |                                                 22   assume ( x = 0);
11       hy ∗ x! = 42! ∧ x > 0i                             23   hy ∗ x! = 42! ∧ x = 0i
12       y = y * x;


                      Fig. 9. Proof outline of a sketch for computing the factorial function.



the course of the veriﬁcation condition computation. The reason is that the validity checks steer
the program construction, and also the veriﬁcation conditions that will be collected in the future.
Despite these dynamics, we can show that a small number of veriﬁcation condition checks will
be suﬃcient to derive the program. Moreover, the veriﬁcation conditions compare ordinary pred-
icates (rather than selections in the previous section), and therefore can be implemented as single
SMT solver queries. All this makes our algorithm eﬃcient in practice.
   Our algorithm implements the proof rules in realization logic, more precisely the non-backtracking
strategy stated in Theorem 4.4. Given a proof outline and a predicate in the postcondition, it tra-
verses the proof backwards to determine suitable preconditions and programs that justify the post-
condition. Our algorithm is thus a function of type syn : prfOutls × Predicates → Predicates ×
Programs. It is deﬁned in Figure 10 and we discuss it in a moment. An important feature of the
function is to discard predicates from selections, in which case it may return (fail, −) and an arbi-
trary program.
   The function gives strong guarantees: when we start from a sketch that has been derived in
realizability logic and a predicate in the postcondition, then the function is guaranteed not to fail
but return a precondition and a program that, together with the given postcondition, will form a
valid Hoare triple. It is also very eﬃcient: the number of veriﬁcation conditions that have to be
checked is linear, actually bounded by the size of the proof outline.

  Theorem 6.1 (syn-Sound-And-Complete). Consider ⊢𝑎 hRipohSi and s ∈ S with s ≠ fail. Then
syn(hRipohSi, s) = (r, prog) with r ∈ R, r ≠ fail, prog ∈ drv(sketch(po)), and |=𝑑 {r }prog{s}. The
number of SMT solver calls is at most |po|.

   Function syn is given in Figure 10. If several cases apply, the topmost one will be taken. This
means the invocation will always return (fail, −) on an empty precondition, and the fail predicate
in a precondition will always be skipped. When we have a command, we go through the predicates
r in the precondition until we ﬁnd one that justiﬁes the given postcondition s. Since s ∈ S and we
started from a proof outline in realizability logic, the search for r is guaranteed to be successful.
Moreover, for the guarantees given by Theorem 6.1 it does not matter which predicate r we take.
The notion of soundness in realizability logic gives the guarantee that the earlier (in the program
text) assertions can handle every r. But of course the choice has an inﬂuence on the shape of the
program.

                                                           15
                                                              Roland Meyer, Jakob Tepe, and Sebastian Wolﬀ


   For a sequential composition po1 ; po2 , we take the given predicates s, propagate it through po2
to obtain (t, prog2 ), propagate t through po1 to get (r, prog1 ), and return (r, prog1 ; prog2 ). Im-
portantly, also here we have the guarantee that both calls will be successful. When we have a
non-terminal, we consult the proof outlines for the right-hand sides. For an angelic choice among
two right-hand sides, we ﬁrst try to synthesize a program from the left proof outline, and if we fail
we know that we will be successful on the right. Whether the synthesis with the left proof outline
will succeed can be foreseen by checking if the target post condition s is in the post condition of
the left proof outline.
   The involved cases are for demonic choices and loops. These are the cases in which the program
logics had to consider single predicates. This is mimicked here, and we ﬁrst discuss the demonic
choice. We go through all predicates r in the given precondition. We try to construct proof outlines
for both branches in which r is the precondition and s is the postcondition. This is the task of the
calls outl (h{r }isketch(po1 )h{s}i) and outl (h{r }isketch(po2 )h{s}i). We argue in a moment why
these calls can actually be looked up in the given proof outline, and therefore mean no eﬀort. If
one of these calls aborts, we continue with the next r. Otherwise, we obtain the proof outlines
po′1 and po′2 . We invoke syn(po′1, s) and syn(po′2, s). They will for sure return r as it is the only
precondition, but we need the programs to be able to return (r, prog1 + prog2 ).
   For loops, we have to make an assumption on the form of the proof outline: the loop invariant
should not be lost through weakening. If assertions have to be weakened, we assume the proof
outline takes the form hRih𝐼 ipo∗ h𝐼 ihSi. Like in the previous case, we go through the predicates
𝑖 ∈ 𝐼 to ﬁnd one that is stronger than the given postcondition s. If it has been found, it remains
to synthesize the program for the loop body. We reconstruct the proof outline with 𝑖 as the pre
and postcondition, and rely on syn to determine the program. If the proof outline takes the form
hRih𝐼 ipo∗ h𝐼 ihSi, instead of returning an 𝑖 of 𝐼 , we return an r of R with r 𝑑 𝑖.
   We elaborate on why the function calls outl (h{r }isketch(po)h{s}i) mean no overhead. The point
is that the Rules (DEM) and (LOOP) can only deal with single predicates in the precondition. This
means when we constructed the proof outline of interest, we have constructed the proof outlines
that we now need as a byproduct. We just have to store them explicitly to be able to look them up
now. This explains the case of loops.
   In the case of demonic choices, the proof outline construction may abort, and we explain how to
handle this with hashing. Since Rule (DEM) requires a singleton as the precondition, we must have
done proofs of the form h{r𝑖 }isketch(po′1 ) + sketch(po′2 )hS𝑖 i. From the requirements of Rule (DEM),
we also have the proof outlines h{r𝑖 }ipo′𝑗 hS𝑖 i for 𝑗 = 1, 2. The proofs might have been gathered
to form the proof outline hRipo1 + po2 hSi. Since the predicate s is in S, there must be a selection
S𝑖 with s ∈ S𝑖 . We can reuse the corresponding proof outlines h{r𝑖 }ipo′𝑗 hS𝑖 i by weakening the
postcondition S𝑖 to the singleton {s}.

6.1   Example: Synthesizing Factorial Function
Recall the sketch sketch from last section’s example, Figure 9. In the last section, we have proven
|=𝑎 hRisketchhSi with R = {x = 42 ∧ y = 1} and S = {y = 42!}. In this example, we will
concretize the sketch to a program prog such that |=𝑑 {r }prog{s} holds. To do so, we use the
function syn. The whole proof outline is called po. We use the same abbreviations as in the last
example. Additionally, with T8 we abbreviate the full realizability triple of Line 8. That means
T8 stands for Lines 7 through 9. Other realizability triples are abbreviated similarly. The realiz-
ability triple around the nonterminal is abbreviated by TN, i.e. TN stands for Lines 5 to 16. We
abbreviate the selection of Lines 15 and 16 with 𝐴15 . Other selections are abbreviated similarly.
Let {r } = R and {s} = S. We start by calling syn(hRisketchhSi, s). More speciﬁcally, the call

                                                  16
Realizability in Semantics-Guided Synthesis Done Eagerly


             syn(h ∅ipohSi, s) := (fail, −)
     syn(h {fail } ∪ RipohSi, s) := syn(hRipohSi, s)
      syn(h {r } ∪ RicomhSi, s) := ÈcomÉ(r ) 𝑑 s ? (r, com) : syn(hRicomhSi, s)
                syn(po1 ; po2 , s) :=    let (t, prog2 ) = syn(po2 , s) and (r, prog1 ) = syn(po1 , t) in (r, prog1 ; prog2 )
                  syn(N(po), s) := syn(po, s)
              syn(po1 | po2 , s) :=      let (r, prog) ∈ syn(po1 , s) in r ≠ fail ? (r, prog) : syn(po2 , s)
syn(h {r } ∪ Ripo1 hSi + h {r } ∪ Ripo2 hSi, s) := outl (h {r } isketch(po𝑖 ) h {s} i) = abort ? syn(hRipo1 hSi + hRipo2 hSi, s) :
                          let po𝑖′ = outl (h {r } isketch(po𝑖 ) h {s} i ) and (r, prog𝑖 ) = syn(po𝑖′ , s) in (r, prog1 + prog2 )
               syn(h {𝑖 } ∪ 𝐼 ipo∗ h {𝑖 } ∪ 𝐼 i, s) := 𝑖 6 𝑑 s ? syn(h𝐼 ipo∗ h𝐼 i, s) :
                          let po′ = outl (h {𝑖 } isketch(po) h {𝑖 } i ) and (𝑖, prog) = syn(po′ , 𝑖 ) in (𝑖, prog∗ )


                                        Fig. 10. Definition of the synthesis function.


is syn(hRibody∗ h𝐼 i;T22, s). The selection 𝐼 is the singleton {𝑖}. The function invokes the call
syn(T22, s) which returns (𝑖, assume(x = 0)). Next, it invokes syn(hRibody∗ h𝐼 i, 𝑖) which, in turn,
invokes syn(h{𝑖}ibodyh{𝑖}i, 𝑖) because 𝑖 𝑑 𝑖 holds trivially. We can reuse the already done
proof h{𝑖}ibodyh{𝑖}i as po′ . The call syn(h{𝑖}ibodyh{𝑖}i, 𝑖) invokes syn(h𝐴15 ix--h{𝑖}i, 𝑖). The
call syn(h{𝐴15 [0]} ∪ {𝐴15 [1]}ix--h{𝑖}i, 𝑖) will invoke syn(h{𝐴15 [1]}ix--h{𝑖}i, 𝑖) because the re-
sult of Èx--É(𝐴15 [0]) is not more precise than 𝑖. However, the call syn(h{𝐴15 [1]}ix--h{𝑖}i, 𝑖)
returns (𝐴15 [1], x--). Here, we witness a foreshadowing on how the wrong angelic choice will
be eliminated. The eliminated predicate stems from the left production of the nonterminal which
will not be able to produce the now selected predicate 𝐴15 [1]. We continue the next recursive call
of syn(h{𝑖}ibodyh{𝑖}i, 𝑖), i.e. syn(T4;TN, 𝐴15 [1]). It invokes syn(TN, 𝐴15 [1]) This call ﬁrst checks
whether the left branch can produce the target predicate. This is not the case, so eventually (fail, −)
is returned, eliminating the left branch. The right branch is now considered, where syn(T12, 𝐴15 [1])
resolves to (𝐴5 [0], y = y*x). Therefore, the next call is syn(T4, 𝐴5 [0]) which resolves to the pair
(𝑖, assume (x>0)). Getting back to the recursive call of the loop, syn(hRibody∗ h𝐼 i, 𝑖) yields the pair
(r, (4;12;17) ∗ ) because r 𝑑 𝑖 with {r } = R. In total, we get (r, prog) = (r, (4; 12; 17) ∗; 22) as out-
put. We know that |=𝑑 {r }prog{s} holds. This means, the program indeed calculates 42 factorial.

7   APPLICATION: MEMORY MANAGEMENT IN LOCK-FREE DATA STRUCTURES
We show how to employ realizability and realization logic to automatically generate code for the
memory management in lock-free data structures. This will also be the setting for our experiments.
There are several aspects that make this setting interesting for benchmarks: the states are type
assignments and the semantics of commands is an abstract one. So SemGuS [23] is an ideal choice,
while SyGuS [2] and solver-aided languages [39, 42] need an encoding to capture the synthesis
tasks. The programs contain loops, which is diﬃcult for SyGuS solvers. Finally, there are many
synthesis options, and the right ones may be far apart. This creates a large space of potential
solutions [3] that our compositional method manages to explore in a matter of seconds.
   Safe Memory Reclamation. The asynchronous nature of lock-free data structures makes manual
memory management diﬃcult: if the threads do not synchronize, how does a thread know that it
is safe to free a memory cell, or safe to access it? The solution is to add to the data structure a safe
memory reclamation algorithm (SMR) which acts as a central instance that is informed about the
intentions of all threads. If a thread wants to access a memory cell, it asks the reclamation algorithm
to protect the cell. If it wants to free a memory cell, it asks the SMR to do so. As the reclamation

                                                                 17
                                                               Roland Meyer, Jakob Tepe, and Sebastian Wolﬀ


algorithm manages the protections, it can defer the free until it is safe. Garbage collection is an
SMR, but there are more eﬃcient solution. Epochs are a simple model [13, 16], we consider here
the hazard pointers that have been proposed for addition to the next C++ standard [31]. To be
precise, we support the elaborate version in which the ﬁrst hazard pointer is stronger than the
second.
   Reclamation algorithms tend to implement lock-free data structures. This means protection calls
are non-atomic, and may be successful or fail due to interference. The reclamation algorithm will
not be able to determine success. Instead, the thread that issued the protection call will have to
ﬁnd out by checking global invariants: if, for example, a sentinal node has not changed when
returning from the call, then the call was successful. Unfortunately, ﬁnding the right combination
of protection calls and checks has turned out error-prone.
   Meyer and Wolﬀ [26, 27] gave a type system that checks memory safety. It can be instanti-
ated to diﬀerent reclamation algorithms and applies to a variety of data structures. We report
on experiments with the queues MS and DGLM, and the sets ORVYY, Michael, VechevCAS, and
VechevDCAS. The type system is control-ﬂow sensitive, which means the typing can be writ-
ten as a proof outline in Hoare logic. A type check on a program prog is successful, if the triple
⊢𝑡 h¬failiprogh¬faili can be derived: starting from no assumptions about the protection of point-
ers, the program will not fail. This means all pointers were protected before they were derefer-
enced. Appendix B.1 provides more background on [26, 27]. An important detail is that they use
code annotations to inform the type system about protections that can otherwise otherwise only
be inferred with a shape analysis. These annotations have to be discharged separately. We omit
these checks in our experiments, and therefore our synthesis is only valid relative to the validity
of the annotations.

   Instantiation. We instantiate the parameters of our development. Meyer and Wolﬀ [26, 27] track
the protection of memory cells by assigning types from a set T to the pointers in the program
Vars. Our states, predicates, and selections are thus States = Vars → T, Predicates = P (Vars →
T) ∪ {fail}, and Selections = P (P (Vars → T) ∪ {fail}).
   Our implementation needs an assertion language to represent predicates and selections. We use
Predicates # = (Vars → T) ∪ {fail} and Selections # = P (Predicates # ). The deﬁnition of the abstract
predicates is due to [26, 27]. The ﬁrst step is to apply a Cartesian abstraction on the predicates,
which yields Vars → P (T). A Cartesian predicate {x : {t1 , t2 }} × {y : {t}} represents the concrete
predicate {x : t1 ∧ y : t, x : t2 ∧ y : t}. The second step is to exploit the fact that the types form a
lattice, and represent x : {t1 , t2 } by x : t1 ⊔ t2 . The details are in Appendix B.5.
   The commands are the usual ones in C. The semantics is from [27] and deﬁned in a way that
works with the above abstraction.

   Synthesis. Given a lock-free data structure and a reclamation algorithm, our goal is to synthe-
size in the data structure calls to the reclamation algorithm and code annotations that, together,
guarantee memory safety, more precisely, make the above type check go through.
   First, we enrich every line of code with a non-terminal from which calls to the SMR algorithm
and invariant annotations may be generated. In the case of a single hazard pointer, for example, the
                                               the non-terminal has the deﬁnition to the left. For
1 AC ::= skip ; |                              each variable v, we may issue a protection, add an an-
2 atomic { @ inv active ( v );} |
                                               notation saying that the variable has not been freed,
3 ( in : protect (v ); re : protect (v );)
                                               or simply skip the annotation. For global invariants,
we use heuristics of where to put them, which improves the scalability. The result of this phase
is a sketch sketch. Next, we try to prove ⊢𝑎 h¬failisketchh¬faili in realizability logic. We use

                                                  18
Realizability in Semantics-Guided Synthesis Done Eagerly


the algorithm from Section 5 and check the validity of the corresponding veriﬁcation conditions.
If successful, we also get a proof outline that we feed to realization logic, implemented in the syn-
thesis algorithm from Section 6. The algorithm has the guarantee to be successful, and returns a
program that corresponds to the original code with suitable annotations added. What is interest-
ing is that we can control the synthesis function to avoid reclamation calls and code annotations
whenever possible. We give details on the implementation and its behavior on experiments.

8   EVALUATION
We implemented our synthesis algorithm in a C++ program. As we do not yet have an assertion
language for selections, our implementation targets the memory reclamation problem discussed
above. It can handle diﬀerent reclamation algorithms and challenging data structures, though. We
give details on the implementation and elaborate on the performance, which was surprisingly
good.
   Implementation. The most important technique we implemented to improve the scalability is
an optimistic variant of our approach. The pessimistic variant is the one from Section 7 that ﬁrst
validates the proof outline and then derives a program. The optimistic variants derives the program
without having validated the proof outline. The point is that function syn checks the veriﬁcation
conditions it needs to construct the program anyhow, and therefore the output will be sound. The
veriﬁcation conditions for proof outlines have to compare selections, and each such comparison
may create quadratically many solver calls.
   We moreover implemented the following application domain speciﬁc heuristics. We assume
local pointers do not need to be protected. We only insert annotations @inv active(v) for sentinel
nodes. The point is that sentinel nodes will never be freed. As discussed above, this would have
to be conﬁrmed by a check that we omit. We automatically compute loop invariants from the
predicates that are available when entering a loop. There is no saturation nor widening. Still, the
approach worked for all data structures we examined. For resolving non-terminals, we prefer skip
over SMR calls and SMR calls over annotations.
   Results. We experimented with the seven lock-free data structures and two hazard pointer vari-
ants discussed in Section 7. The environment is an Apple M2 with 8GB RAM. We do not have a
solver backend but hand the bitvectors we need within our implementation. The results are given
in Table 1. In some methods we used hints that can be deduced by a lightweight shape analysis.
   The ﬁrst column shows the maximum, average, and median size of a selection. The next shows
the number of invocations of the comparison function on predicates per comparison of selection.
For example, {𝑎} 𝑎 {𝑏 1, 𝑏 2, 𝑏 3 } may yield three comparisons 𝑎 𝑑 𝑏𝑖 . This only applies to the
pessimistic approach. The next two columns display the time for the functions vc and syn in the
pessimistic approach. The last two columns are for the optimistic approach. It clearly outperforms
the pessimistic approach, but both are quite fast.
   The key insight of our experiments is that there are two classes of synthesis options. The options
that are handled well by our approach lead to similar predicates and thus small selections, or they
fail early. The options that are diﬃcult for our approach lead to new predicates that fail late. This
can be seen in the benchmarks with two hazard pointers. In the set implementations, the order
among the hazard pointers matters, and if we try to synthesize a protection with the wrong order
we fail early. For DGLM, the order does not matter and the synthesis time increases dramatically.
   Taking a step back, the experiments indicate that our realizability and realization logics should
be combined with an outer search [3]. The search would concentrate on the synthesis options that
are diﬃcult for our approach and only ﬁx them. Our approach would handle the remaining, easier
options. We see this as a promising direction for future work.

                                                           19
                                                                      Roland Meyer, Jakob Tepe, and Sebastian Wolﬀ


    Table 1. Results of experiments of the Pessimistic and Optimistic Approach conducted on an Apple M2.

                                        Max/Avg/Med       Max/Avg/Med        Pessimistic       Optimistic
                                               |R|          𝑑 per 𝑎       7 vc 7 syn       7 syn    7 vc
                                 Push     6 / 1.57 / 1     12 / 1.85 / 1   < 0.1𝑠 < 0.1𝑠     < 0.1𝑠 < 0.1𝑠
                Treiber’s [43]
                                 Pop      6 / 1.43 / 1     18 / 1.71 / 1   < 0.1𝑠 < 0.1𝑠     < 0.1𝑠 < 0.1𝑠
        HP1
                   MS [30]       EnQ      5 / 1.27 / 1     12 / 1.40 / 1   < 0.1𝑠 < 0.1𝑠     < 0.1𝑠 < 0.1𝑠
                  DGLM [9]       EnQ      17 / 1.3 / 1      64 / 1.9 / 1     0.7𝑠 < 0.1𝑠     < 0.1𝑠 < 0.1𝑠
                   MS [30]       DeQ      90 / 1.6 / 1     1K / 2.92 / 1      17𝑠     0.6𝑠     0.6𝑠 < 0.1𝑠
                  DGLM [9]       DeQ     29 / 1.74 / 1     5K / 18.9 / 1    249𝑠      6.3𝑠     5.9𝑠 < 0.1𝑠
                                 Add    158 / 3.85 / 1     276 / 3.6 / 1     1.4𝑠 < 0.1𝑠     < 0.1𝑠 < 0.1𝑠
                 ORVYY [33]
                                  Rm     32 / 1.29 / 1    276 / 1.96 / 1     0.6𝑠     0.1𝑠     0.1𝑠 < 0.1𝑠
                                 Add    127 / 3.06 / 1     5K / 13.4 / 1     3.1𝑠     2.1𝑠     2.2𝑠 < 0.1𝑠
        HP2      Michael [28]
                                  Rm    127 / 3.15 / 1     5K / 13.7 / 1     1.5𝑠     2.1𝑠     2.1𝑠 < 0.1𝑠
                                 Add      25 / 1.7 / 1     148 / 3.1 / 1     0.6𝑠 < 0.1𝑠     < 0.1𝑠 < 0.1𝑠
               VechevCAS [45]
                                  Rm      21 / 1.7 / 1     178 / 3.1 / 1     0.1𝑠 < 0.1𝑠     < 0.1𝑠 < 0.1𝑠
                                 Add     45 / 2.64 / 1    341 / 6.68 / 1     0.4𝑠 < 0.1𝑠     < 0.1𝑠 < 0.1𝑠
              VechevDCAS [45]
                                  Rm      21 / 1.7 / 1     145 / 2.9 / 1     0.1𝑠 < 0.1𝑠     < 0.1𝑠 < 0.1𝑠




9     RELATED WORK
We have already discussed the related work on SemGuS, SyGuS, and solver-aided programming in
the introduction. There is a body of work on programming models with angelic non-determinism,
dating back to Floyd [12]. The common case, however, is that the angelic choices are made at
runtime, and therefore can react to the demonic choices. These models are related to two-player
zero-sum graph games [14] typically used in reactive synthesis, as originally proposed by Church
[7] and later developed by Pnueli and Rosner [35]. In SemGuS, the angelic choices have to be made
up-front, which adds a form of imperfect information [38] that the common case does not have to
deal with. This imperfect information shines through in Rules (DEM) and (LOOP), where the angelic
player cannot react. Two works, however, are closer to our development.
   Mamouras [24] presents a Hoare logic to reason about the correctness of programs with (run-
time) angelic non-determinism. His assertions are classical predicates, which means the proof con-
struction is forced to decide on a synthesis option early on, may later fail due to incompatible
decisions, and in this case has to backtrack. To avoid precisely this backtracking, we proposed
selections as assertions in realizability logic. As a consequence, the resulting theories are largely
diﬀerent.
   Celiku and von Wright [6] consider the same class of programs as Mamouras, but try to reﬁne
angelic choices to conditionals and loops. The reﬁnement is guided by a proof outline, and may
be compared to our realization logic. An important diﬀerence is that they work with ordinary
predicates, and try to synthesize appropriate ones. We work with the new selections, instead, in
which we have gathered the relevant predicates.
   Also related is the recent [32] that uses angelic non-determinism to synthesize recursive func-
tions. During recursive calls, they select an output value for the function and later check whether
the choice can be justiﬁed. The work [21, 41] infers a program from veriﬁcation conditions that
contain unknown program parts which, in the case of [21], should be ﬁlled by library components.
The crucial diﬀerence to realization logic is that we have eagerly analyzed the program space, and
the task of syn amounts to a concretization rather than a search. We have not seen a backtracking
freedom guarantee in related work.
   The deductive approach decomposes the task of synthesizing a program into synthesis tasks for
subprograms [25]. A popular idea is to factorize the subprograms along input-output equivalence

                                                         20
Realizability in Semantics-Guided Synthesis Done Eagerly


so that the computation can proceed with equivalence classes [1, 11, 15, 34, 36, 44]. What is dif-
ferent in our work is that we try to be eager in the bottom-up construction, and consider a set of
synthesis options whose behavior does not have to match. Related to our approach are [10, 46]
that weaken the input-output equivalence by considering an abstract domain. A solution for the
abstract domain is then a restricted class of programs that can be searched more eﬃciently. Real-
izability and realization logic may prove useful for this task.
   We introduced our eager approach to reduce the number of costly veriﬁcation queries, a promi-
nent endeavor in search-based synthesis [3]. An important development is to inform the solver
about semantic properties of the program sought [4]. In the context of example-based speciﬁca-
tions, a semantic property is the invariance to perturbations of the example set, which can be
incorporated by enriching the example set.

REFERENCES
 [1] A. Albarghouthi, S. Gulwani, and Z. Kincaid. 2013. Recursive Program Synthesis. In CAV (LNCS, Vol. 8044). Springer,
     934–950.
 [2] R. Alur, R. Bodik, G. Juniwal, M. M. K. Martin, M. Raghothaman, S. A. Seshia, R. Singh, A. Solar-Lezama, E. Torlak,
     and A. Udupa. 2013. Syntax-guided synthesis. In FMCAD. IEEE, 1–8.
 [3] R. Alur, R. Singh, D. Fisman, and A. Solar-Lezama. 2018. Search-based program synthesis. CACM 61, 12 (2018), 84–93.
 [4] S. An, R. Singh, S. Misailovic, and R. Samanta. 2020. Augmented example-based synthesis using relational perturbation
     properties. PACMPL 4, POPL (2020), 56:1–56:24.
 [5] C. Calcagno, P. W. O’Hearn, and H. Yang. 2007. Local Action and Abstract Separation Logic. In LICS. IEEE, 366–378.
 [6] O. Celiku and J. von Wright. 2003. Implementing angelic nondeterminism. In Asia-Paciﬁc Software Engineering Con-
     ference. IEEE, 176–185.
 [7] A. Church. 1957. Applications of recursive arithmetic to the problem of circuit synthesis. Summaries of the Summer
     Institute of Symbolic Logic 1 (1957), 3–50.
 [8] P. Cousot. 2021. Principles of Abstract Interpretation. The MIT Press.
 [9] S. Doherty, L. Groves, V. Luchangco, and M. Moir. 2004. Formal Veriﬁcation of a Practical Lock-Free Queue Algorithm.
     In FORTE (LNCS, Vol. 3235). Springer, 97–114.
[10] D. Drachsler-Cohen, S. Shoham, and E. Yahav. 2017. Synthesis with Abstract Examples. In CAV (LNCS, Vol. 10426).
     Springer, 254–278.
[11] J. K. Feser, S. Chaudhuri, and I. Dillig. 2015. Synthesizing data structure transformations from input-output examples.
     In PLDI. ACM, 229–239.
[12] R. W. Floyd. 1967. Nondeterministic Algorithms. JACM (1967).
[13] K. Fraser. 2004. Practical lock-freedom. Ph. D. Dissertation. University of Cambridge.
[14] E. Grädel, W. Thomas, and T. Wilke (Eds.). 2002. Automata, Logics, and Inﬁnite Games: A Guide to Current Research.
     LNCS, Vol. 2500. Springer.
[15] S. Gulwani. 2011. Automating string processing in spreadsheets using input-output examples. In POPL. ACM, 317–
     330.
[16] T. L. Harris. 2001. A Pragmatic Implementation of Non-Blocking Linked-Lists. In DISC (LNCS, Vol. 2180). Springer,
     300–314.
[17] C. A. R. Hoare. 1969. An Axiomatic Basis for Computer Programming. CACM 12, 10 (1969), 576–580.
[18] Q. Hu, J. Breck, J. Cyphert, L. D’Antoni, and T. W. Reps. 2019. Proving Unrealizability for Syntax-Guided Synthesis.
     In CAV (LNCS, Vol. 11561). Springer, 335–352.
[19] Q. Hu, J. Cyphert, L. D’Antoni, and T. W. Reps. 2020. Exact and approximate methods for proving unrealizability of
     syntax-guided synthesis problems. In PLDI. ACM, 1128–1142.
[20] Q. Hu and L. D’Antoni. 2018. Syntax-Guided Synthesis with Quantitative Syntactic Objectives. In CAV (LNCS,
     Vol. 10981). Springer, 386–403.
[21] S. Jha, S. Gulwani, S. A. Seshia, and A. Tiwari. 2010. Oracle-guided component-based program synthesis. In ICSE.
     ACM, 215–224.
[22] J. Kim, L. D’Antoni, and T. Reps. 2023. Unrealizability Logic. PACMPL 7, POPL, 659–688.
[23] J. Kim, Q. Hu, L. D’Antoni, and T. Reps. 2021. Semantics-Guided Synthesis. PACMPL 5, POPL, 1–32.
[24] K. Mamouras. 2016. Synthesis of Strategies Using the Hoare Logic of Angelic and Demonic Nondeterminism. LMCS
     12, 3.
[25] Z. Manna and R. J. Waldinger. 1980. A Deductive Approach to Program Synthesis. ACM TOPLAS 2, 1 (1980), 90–121.


                                                            21
                                                                          Roland Meyer, Jakob Tepe, and Sebastian Wolﬀ


[26] R. Meyer and S. Wolﬀ. 2019. Decoupling Lock-Free Data Structures from Memory Reclamation for Static Analysis,
     In POPL. PACMPL, Article 58, 31 pages.
[27] R. Meyer and S. Wolﬀ. 2020. Pointer Life Cycle Types for Lock-Free Data Structures with Memory Reclamation, In
     POPL. PACMPL, Article 68, 36 pages.
[28] M. M. Michael. 2002. High Performance Dynamic Lock-Free Hash Tables and List-Based Sets. In SPAA. ACM, 73—-82.
[29] M. M. Michael. 2002. Safe Memory Reclamation for Dynamic Lock-Free Objects Using Atomic Reads and Writes. In
     PODC. ACM, 10 pages.
[30] M. M. Michael and M. L. Scott. 1996. Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue
     Algorithms. In PODC. ACM, 267–275.
[31] M. M. Michael, M. Wong, P. McKenney, A. Hunter, D. S. Hollman, JF Bastien, H. Boehma, D. Goldblatt, F. Birbacher,
     and M. Stearn. 2023. Hazard Pointers for C++26.
[32] A. Miltner, A. T. Nuñez, A. Brendel, S. Chaudhuri, and I. Dillig. 2022. Bottom-up Synthesis of Recursive Functional
     Programs Using Angelic Execution. PACMPL 6, Article 21 (2022), 29 pages.
[33] P. W. O’Hearn, N. Rinetzky, M. T. Vechev, E. Yahav, and G. Yorsh. 2010. Verifying Linearizability with Hindsight. In
     PODC. ACM, 85—-94.
[34] P. M. Osera and S. Zdancewic. 2015. Type-and-example-directed program synthesis. In PLDI. ACM, 619–630.
[35] A. Pnueli and R. Rosner. 1989. On the Synthesis of a Reactive Module. In POPL (Austin, Texas, USA). ACM, 179—-190.
[36] O. Polozov and S. Gulwani. 2015. FlashMeta: a framework for inductive program synthesis. In OOPSLA. ACM, 107–
     126.
[37] M. O. Rabin and D. S. Scott. 1959. Finite Automata and Their Decision Problems. IBM J. Res. Dev. 3, 2 (1959), 114–125.
[38] J. H. Reif. 1984. The complexity of two-player games of incomplete information. J. Comput. System Sci. 29, 2 (1984),
     274–301.
[39] A. Solar-Lezama. 2008. Program Synthesis by Sketching. Ph. D. Dissertation. U.C. Berkeley.
[40] A. Solar-Lezama, L. Tancau, R. Bodik, S. Seshia, and V. Saraswat. 2006. Combinatorial Sketching for Finite Programs.
     ASPLOS 41, 11 (2006), 404—-415.
[41] S. Srivastava, S. Gulwani, and J. S. Foster. 2010. From program veriﬁcation to program synthesis. In POPL. ACM,
     313–326.
[42] E. Torlak and R. Bodik. 2013. Growing Solver-Aided Languages with Rosette. In Onward! ACM, 135–152.
[43] R. K. Treiber. 1986.      Systems programming: Coping with parallelism.           Technical Report RJ 5118 (1986).
     https://dominoweb.draco.res.ibm.com/reports/rj5118.pdf
[44] A. Udupa, A. Raghavan, J. V. Deshmukh, S. Mador-Haim, M. M. K. Martin, and R. Alur. 2013. TRANSIT: specifying
     protocols with concolic snippets. In PLDI. ACM, 287–296.
[45] M. Vechev and E. Yahav. 2008. Deriving Linearizable Fine-Grained Concurrent Objects. In PLDI. ACM, 125—-135.
[46] X. Wang, I. Dillig, and R. Singh. 2018. Program Synthesis Using Abstraction Reﬁnement. PACMPL 2, POPL (2018),
     63:1–63:30.
[47] S. Wolﬀ. 2021. Verifying Non-blocking Data Structures with Manual Memory Management. Ph. D. Dissertation. TU
     Braunschweig.




                                                            22
Realizability in Semantics-Guided Synthesis Done Eagerly


A PROOFS
We present omitted proofs and details of this paper.

A.1 Proofs for Section 3
  Lemma A.1. The function ÈcomÉ is monotonic for all commands com, i.e. the following equation
holds:
                           r 𝑑 s =⇒ ÈcomÉ(r) 𝑑 ÈcomÉ(s) .
   Proof. Let r and s be elements of Predicates with r 𝑑 s.
   Case 1: ÈcomÉ(s) = fail. Then ÈcomÉ(r) 𝑑 ÈcomÉ(s).
   Case 2: ÈcomÉ(s) ≠ fail. Then, s ≠ fail and there is no 𝑝 in s with ÈcomÉ(𝑝) = fail. Because
s ≠ fail, we have r ≠ fail and r ⊆ 𝑠. Therefore, there also is no 𝑝 in r with ÈcomÉ(𝑝) = fail. Now,
let 𝑝 ′ be an element of ÈcomÉ(r). Thus, there exists a 𝑝 in r with 𝑝 ′ ∈ ÈcomÉ(𝑝). Since r ⊆ 𝑠, this
𝑝 also is in s and therefore, 𝑝 ′ also is in ÈcomÉ(s), making ÈcomÉ(r) a subset of ÈcomÉ(s). In total,
ÈcomÉ(r) 𝑑 ÈcomÉ(s) holds.                                                                        
  Lemma A.2. The relation 𝑑 is a partial order relation on Predicates. This means, the order is
reﬂexive, transitive and antisymmetric, i.e. the following equations hold:
                                 ∀ r ∈ Predicates : r 𝑑 r
                             ∀ r, s, t ∈ Predicates : r 𝑑 s ∧ s 𝑑 t =⇒ r 𝑑 t
                               ∀ r, s ∈ Predicates : r 𝑑 s ∧ s 𝑑 r =⇒ r = s
  Proof. Let r, 𝑠, 𝑡 be elements of Predicates.
  Reﬂexivity (r 𝑑 r):
  Case 1: r = fail. We get r 𝑑 r immediately. Case 2: r ≠ fail. So r is a set of states. Then, r ⊆ 𝑟
holds.
  Transitivity (r 𝑑 s ∧ s 𝑑 𝑡 =⇒ r 𝑑 𝑡):
  Case 1: t = fail. Then r 𝑑 t holds. Case 2: t ≠ fail. Then s ≠ fail and r ≠ fail. By transitivity of
the relation⊆, we get r 𝑑 t.
  Anti-symmetry (r 𝑑 s ∧ s 𝑑 r =⇒ r = s):
  If either one of r and s is fail the other one also has to be fail for both inequalities to hold. If
neither one is fail, anti-symmetry follows from the anti-symmetry of ⊆.                              
  Lemma A.3. The partial order (Predicates, 𝑑 ) is a complete lattice. That means for any subset R of
Predicates there exists a join and a meet. In fact, the join and meet can be computed by the following
equations: Let R be a subset of Predicates.
                                         (
                                           fail                , fail ∈ R
                                 ⊔(R) = Ð
                                             r ∈R r            , else
                                         (
                                           fail                 , R = {fail}
                                 ⊓(R) = Ñ
                                             r ∈ (R\{fail} ) 𝑟  , else
   Proof. Let R ⊆ Predicates
   We show that ⊔(R) is an upper bound of R: Let r be in R. Case 1: Assume fail ∈ R. Then
⊔(R) = fail. Thus, r 𝑑 ⊔(R). Case 2: Assume fail is not in R. Then ⊔(R) = r ∈R r. Thus, r ⊆ ⊔(R)
                                                                           Ð
and r 𝑑 ⊔(R).
   We show that ⊔(R) is the least upper bound of R: Let 𝑢 be an upper bound of R. Case 1: Assume
                                                                                           Ð
fail ∈ R. Then fail 𝑑 𝑢. Thus, ⊔(R) 𝑑 𝑢. Case 2:Ð Assume fail is not in R. Then ⊔(R) = r ∈R r.
Since 𝑢 is an upper bound, ∀r ∈ R : r ⊆ 𝑢. Thus, ( r ∈R r) ⊆ 𝑢. So, ⊔(R) 𝑑 𝑢.

                                                           23
                                                               Roland Meyer, Jakob Tepe, and Sebastian Wolﬀ


  We show that ⊓(R) is a lower bound of R: Let r be in R. Case 1: Assume R = {fail}. Then
r = fail = ⊓(R). Thus ⊓(R) 𝑑 r. Case 2: Assume R ≠ {fail}. If r = fail, we get ⊓(R) 𝑑 r.
Otherwise, ⊓(R) = ∩r ∈R\{fail} r. Therefore, ⊓(R) ⊆ r and thus ⊓(R) 𝑑 r.
  We show that ⊓(R) is the greatest lower bound of R: Let 𝑙 be a lower bound of R. Case 1: Assume
R = {fail}. Then ⊓(R) = fail. Thus 𝑙 𝑑 ⊓(R). Case 2: Assume R ≠ {fail}. Let r be in R \ {fail}.
Then 𝑙 ⊆ r. This holds for every r. Thus, 𝑙 ⊆ ⊓(R). Therefore, 𝑙 𝑑 ⊓(R).                       

The Missing EMPTY Rule:
For completeness, we need to add the following rule to the calculus:
                                          (EMPTY)

                                          ⊢𝑎 hRisketchh∅i
Proof of Theorem 3.1.
   We prove soundness by structural induction over the proof tree.
   Base Case: We have ⊢𝑎 h{r }icomh{s}i through the rule (COM). Thus, we have ÈcomÉ(r) 𝑑 s.
Therefore, the realizability triple |=𝑎 h{r }icomh{s}i holds.
   Induction Step: In the ﬁrst case, we have ⊢𝑎 hRisketch1 ; sketch2 hT i through the rule (SEQ).
Thus, we have the realizability triples ⊢𝑎 hRisketch1 hSi and ⊢𝑎 hSisketch2 hT i. By applying the
induction hypothesis, we get |=𝑎 hRisketch1 hSi and |=𝑎 hSisketch2 hT i. Let t be an element of T .
Then, there exists a predicate s ∈ S and a program prog2 ∈ drv(sketch2 ) with |=𝑑 {s}prog2 {t}.
And, there exists r ∈ R and prog1 ∈ drv(sketch1 ) with |=𝑑 {r }prog1 {s}. By completeness of Hoare
logic, we get ⊢𝑑 {r }prog1 {s} and ⊢𝑑 {s}prog1 {t}. Using rule (SEQ), we get ⊢𝑑 {r }prog1 ; prog2 {t}.
   In the next case we have the triple ⊢𝑎 hRisketchhSi through the rule (CSQ). Thus we have
⊢𝑎 hR′ isketchhS ′ i with R 𝑎 R′ and S ′ 𝑎 S. Through the induction hypothesis, we get |=𝑎
hR′ isketchhS ′ i. Now, let s be an element of S. Since S ′ 𝑎 S, there is an s′ in S ′ with s′ 𝑑 s. From
|=𝑎 hR′ isketchhS ′ i we know, that there is an r ′ in R′ and a program prog ∈ drv(sketch) such that
|=𝑑 {r ′ }prog{s′ } holds. Through transitivity of the relation 𝑑 , we also get that |=𝑑 {r ′ }prog{s}
holds. Due to monotonicity of executions, and since R 𝑎 R′ holds, there is an r in R for which
|=𝑑 {r }prog{s} is true. That means, |=𝑎 hRisketchhSi holds.
   In the next case, we have ⊢𝑎 hRisketch1 + sketch2 hSi through the rule (DEM). Therefore, we
know R = {r } and the realizability triples ⊢𝑎 hRisketch1 hSi and ⊢𝑎 hRisketch2 hSi hold. From
the induction hypothesis we know that |=𝑎 hRisketch1 hSi and |=𝑎 hRisketch2 hSi hold. Now, let
s be an element of S. Then, there exists prog1 ∈ drv(sketch1 ) for which |=𝑑 {r }prog1 {s} is true.
Analogously, there exists prog2 ∈ drv(sketch2 ) for which |=𝑑 {r }prog2 {s} is true. We now show
that |=𝑑 {r }prog1 + prog2 {s} is true. This directly implies that |=𝑎 hRisketch1 + sketch2 hSi holds.
Let ex be an execution of prog1 +prog2 . Thus, it is either an execution of prog1 or prog2 . W.l.o.g. let
ex be in exec(prog1 ). Since |=𝑑 {r }prog1 {s} is true, we also get that ÈexÉ(r) is more precise than s.
Therefore, the Hoare triple |=𝑑 {r }prog1 + prog2 {s} is true and thus |=𝑎 hRisketch1 + sketch2 hSi
holds.
   In the next case, we have ⊢𝑎 hRisketch∗ hRi through the rule (LOOP). Thus we know the realiz-
ability triple ⊢𝑎 hRisketchhRi holds and R = {r }. The induction hypothesis yields |=𝑎 hRisketchhRi.
From this we know that there is a prog ∈ drv(sketch) with |=𝑑 {r }prog{r }. We now show that |=𝑑
{r }prog∗ {r } is true. For this, we inductively show |=𝑑 {r }prog𝑖 {r } for every 𝑖 ∈ N. Since prog0 is
skip, |=𝑑 {r }prog0 {r } immediately follows. In the induction step, we show |=𝑑 {r }prog𝑖 ;prog{r }.
From the hypothesis, we know that |=𝑑 {r }prog𝑖 {r } and |=𝑑 {r }prog{r } hold. Referring to the
case where we have proven sequences in this proof, this implies that |=𝑑 {r }prog𝑖+1 {r } is true.
Thus, we know that |=𝑑 {r }prog∗ {r } holds. Therefore, |=𝑎 hRisketch∗ hRi is true.

                                                    24
Realizability in Semantics-Guided Synthesis Done Eagerly



Fig. 11. Definition of the Program Logic for Synthesis over proof outlines. Extensions of traditional Hoare
logic are blue.

        (PCOM)                             (PSEQ)                                             (PLOOP)
           ÈcomÉ(𝑟 ) 𝑑 𝑠                  ⊢𝑝 hRipo1 hSi         ⊢𝑝 hSipo2 hT i               ⊢𝑝 hRipohRi      R = {r }
         ⊢𝑝 h {𝑟 } icomh {𝑠 } i                 ⊢𝑝 hRipo1 hSi;hSipo2 hT i                      ⊢𝑝 hRi (hRipohRi) ∗ hRi

          (PDEM)                                                          (PCSQ)
          ⊢𝑝 hRipo1 hSi           ⊢𝑝 hRipo2 hSi       R = {𝑟 }            ⊢𝑝 h𝑅 ′ ipoh𝑆 ′ i       R 𝑎 R′     S ′ 𝑎 S
                     ⊢𝑝 hRipo1 hSi + hRipo2 hSi                                            ⊢𝑝 hRipohSi

                            (PANG)
                             ⊢𝑝 hRirhshSi         N ::= rhs | . . .                      (PEMPTY)

                                      ⊢𝑝 N(hRirhshSi)                                    ⊢𝑝 hRipoh∅i

                           (PGATHER)
                            ⊢𝑝 hR1 ipo1 hS1 i       ⊢𝑝 hR2 ipo2 hS2 i    sketch(po1 ) = sketch(po2 )
                                           ⊢𝑝 hR1 ∪ R2 igather (po1 , po2 ) hS1 ∪ S2 i




   In the next case, we have ⊢𝑎 hRiNhSi through the rule (ANG). From this, we know ⊢𝑎 hRirhshSi
holds with N::= rhs | . . . . From the induction hypothesis we get |=𝑎 hRirhshSi . Since drv(rhs)
is a subset of drv(N), we get |=𝑎 hRiNhSi immediately.
   In the last case, we have ⊢𝑎 hR1 ∪ R2 isketchhS1 ∪ S2 i through the rule (GATHER). From this, we
know ⊢𝑎 hR1 isketchhS1 i and ⊢𝑎 hR2 isketchhS2 i hold. Let s be an element of S1 ∪ S2 . W.l.o.g. let s
be an element of S1 . From the induction hypothesis we know that there is an r in R1 ⊆ R1 ∪ R2 and
a program prog ∈ drv(sketch) with |=𝑑 {r }prog{s}. Thus, we get |=𝑎 hR1 ∪ R2 isketchhS1 ∪ S2 i.
This concludes the soundness proof.
   We proceed with the proof for completeness. In the ﬁrst case, the postcondition is empty. We
have |=𝑎 hRisketchh∅i. Using the rule (EMPTY), we get ⊢𝑎 hRisketchh∅i.
   In the second case, the postcondition is not empty. We have |=𝑎 hRisketchhSi. Thus, for every
s ∈ S there is a program prog ∈ drv(sketch) and a predicate r ∈ R for which |=𝑑 {r }prog{s}.
Since Hoare logic is complete, we have ⊢𝑑 {r }prog{s}. We can mimic this proof in realizability
logic for sketch by using rule (ANG) mimicking the derivation of prog from sketch. Thus, we have
⊢𝑎 hrisketchhsi. Since S is ﬁnite, we only need to do the proof for ﬁnitely many programs. These
proofs are then combined using the rule (GATHER) multiple times to derive ⊢𝑎 hR′ isketchhSi
for the subset R′ of R containing the used predicates r of R. Then, using rule (CSQ), we get ⊢𝑎
hRisketchhSi.                                                                                       

A.2    Proofs for Section 4
To properly deﬁne the notation of a valid proof outline, we state a a proof system for that ranges
over proof outlines in Figure 11. When we write ⊢𝑝 N(po) we mean ⊢𝑝 hRiN(po)hSi where R resp.
S are the union of all pre- resp. postconditions of the subproofs in po. The function sketch extracts
the program sketch out of the proof outline:

  Definition 1. The function gather combines two proofs over the same sketch.

                                      gather : (prfOutls × prfOutls) ⇀ prfOutls

                                                                 25
                                                                    Roland Meyer, Jakob Tepe, and Sebastian Wolﬀ


              gather (hR1 icomhS1 i, hR2 icomhS2 i) = hR1 ∪ R2 icomhS1 ∪ S2 i
              gather (hR1 ip1∗ hS1 i, hR2 ip2∗ hS2 i) = hR1 ∪ R2 igather (p1, p2) ∗ hS1 ∪ S2 i
                        gather (po1 ;po2, po′1 ;po′2 ) = gather (po1, po′1 );gather (po2, po′2 )
                     gather (po1 + po2 , po′1 + po′2 ) = gather (po1, po′1 ) + gather (po2 , po′2 )
                     gather (po1 | po2, po′1 | po′2 ) = gather (po1, po′1 ) | gather (po2, po′2 )
              gather (N(po1 | po2 ), N(po′1 | po′2 )) = N(gather (po1, po′1 ) | po2 | po′2 )
In the last case, po1 and po′1 are the productions where the right hand side in both proof outlines are the
same. The proof outlines po2 and po′2 reason over diﬀerent sketches and their proof outlines therefore
cannot be combined.
   In order for the function gather (po1, po2 ) to be deﬁned, it is required that po1 and po2 are proofs
over the same sketch, i.e. sketch(po1 ) = sketch(po2 ).
  We need the following theorem:
  Theorem A.4 (Eqivalence). The following implication holds for any proof po of prfOutls and
any angels R and S:
                             ⊢𝑝 hRipohSi =⇒ ⊢𝑎 hRisketch(po)hSi .
  The following implication holds for any sketch sketch of Sketches and any angels R and S:
          ⊢𝑎 hRisketchhSi =⇒ ∃ po ∈ prfOutls : sketch(po) = sketch ∧ ⊢𝑝 hRipohSi .
Proof of Theorem A.4.
   We start with the ﬁrst implication. We show the implication by structural induction over the
proof tree.
   Base Case:: We have ⊢𝑝 h{r }icomh{s}i through (PCOM). Thus, we know ÈcomÉ(r) 𝑑 s is true.
With rule (COM) we directly get ⊢𝑎 h{r }icomh{s}i.
   Induction Step: Since all induction steps are only applying the induction hypothesis and re-
building the proof in the other proof system, we demonstrate it on one case only. We have the proof
outline ⊢𝑝 hRipo1 ;po2 hT i through (PSEQ). With the preconditions and the induction hypothesis
we get ⊢𝑎 h𝑅isketch1 h𝑆i and ⊢𝑎 h𝑆isketch2 h𝑇 i where the sketches are of the corresponding
proof. Using the rule (SEQ), we get ⊢𝑎 h𝑅isketch1 ;sketch2 h𝑇 i
   We continue with the second implication. Again, we show the implication by structural induc-
tion over the proof tree.
   Base Case:: We have ⊢𝑎 h{r }icomh{s}i through (COM). Thus, we know ÈcomÉ(r) 𝑑 s is true.
With rule (PCOM) we directly get ⊢𝑝 h{r }icomh{s}i.
   Induction Step: Since all induction steps are only applying the induction hypothesis and re-
building the proof in the other proof system, we demonstrate it on one case only. We have the
realizability triple ⊢𝑎 hRisketch1 ;sketch2 hT i through (SEQ). With the preconditions and the in-
duction hypothesis we get two proofs po1 and po2 for which the following holds: ⊢𝑝 hRipo1 hSi and
⊢𝑝 hSipo2 hT i. Furthermore, sketch(po𝑖 ) = sketch𝑖 . With rule (PSEQ) we get ⊢𝑝 h𝑅ipo1 ;po2 h𝑇 i. 
  We show several properties of a valid proof outline: When we write ⊢𝑝 po with po = po1 | . . . | po𝑛
we mean ⊢𝑝 po1 ∧ . . . ∧ ⊢𝑝 po𝑛 .
  Lemma A.5. In a sketch proof outline, all realizability triples hold, i.e. the following implications
are true:
                   ⊢𝑝 po1 ;po2 =⇒ ⊢𝑝 hRipo1 hSi∧ ⊢𝑝 hS ′ ipo2 hT i ∧ S = S ′
             ⊢𝑝 po1 + po2 =⇒ ⊢𝑝 hRipo1 hSi∧ ⊢𝑝 hR′ ipo2 hS ′ i ∧ R = R′ ∧ S = S ′

                                                       26
Realizability in Semantics-Guided Synthesis Done Eagerly


                                              ⊢𝑝 N(po) =⇒ ⊢𝑝 po
                 ⊢𝑝 hRi(h𝐼 ipoh𝐼 i) hSi =⇒ ⊢𝑝 h𝐼 ipoh𝐼 ′ i ∧ 𝐼 = 𝐼 ′ ∧ R 𝑎 𝐼 ∧ 𝐼 𝑎 S .
                                   ′   ∗


   Proof. We use structural induction to prove the implications. We proof one implication at a
time.
   For the ﬁrst one, the only rules that need to be considered are (PSEQ), (PCSQ) and (PGATHER). The
base case holds trivially. Rule (PSEQ) immediately yields the sought after result. Through transitiv-
ity of 𝑎 , (PCSQ) also yields the implication after applying the induction hypothesis. When rule
(PGATHER) is applied, the proof has the following shape:

                ⊢𝑝 hR ∪ R′ igather (po1, po′1 )hS ∪ S ′ i;hS ∪ S ′ igather (po2, po′2 )hT ∪ T ′ i
We can use the gather rule to show ⊢𝑝 gather (po𝑖 , po𝑖′ ) because the individual proofs hold accord-
ing to the induction hypothesis. That fact that the intermediary assertions match is a result of the
induction hypothesis.
   The other cases all follow the same pattern: The proofs for the rule corresponding to the program
(here (PSEQ) for a program sequence) and rule (PCSQ) hold trivially. For rule (PGATHER), the rule
itself has to be applied to the result of the induction hypothesis, as seen here.                  
Proof of Theorem 4.1.
  With the newly introduced notation, the theorem is the following:
  Theorem A.6 (Soundness). ⊢𝑝 po and po p∼ po′ together imply ⊢𝑝 po′ .
  We conduct the proof using structural induction over the proof tree in realization logic.
   Base Case: We know that ⊢𝑝 h𝑅icomh𝑆i and h𝑅icomh𝑆i p∼ h{𝑟 }icomh{𝑠}i hold. From the rule
(RCOM) of the realization logic we know that ÈcomÉ(𝑟 ) 𝑑 𝑠 is true. This directly implies that
⊢𝑝 h{𝑟 }icomh{𝑠}i holds.
   Induction Step: Consider the rule (RSELECT). The implication immediately holds because the
nested proofs are sound per Lemma A.5.
   Consider the rule (RAC). Again, since the nested proofs are sound, we get ⊢𝑝 po1 and ⊢𝑝 po and
⊢𝑝 po2 . Applying the induction hypothesis on the precondition of the rule yields the triple ⊢𝑝 po′
Applying rule (PANG) on each subproof, yields ⊢𝑝 𝑁 (po1 ) and ⊢𝑝 𝑁 (po′ ) and ⊢𝑝 𝑁 (po2 ). Applying
rule (PGATHER) multiple times yields the sought after result: ⊢𝑝 𝑁 (po1 | po′ | po2 ) .
   Consider rule (RSEQL). Since the nested proofs are sound, we get ⊢𝑝 hRipo1 hSi and also ⊢𝑝 po2 .
The induction hypothesis yields the realizability triple ⊢𝑝 hRw ipo′1 hSi. Using rule (PSEQ), we get
⊢𝑝 hRw ipo′1 hSi;po2 .
   Consider rule (RSEQR). Again, by soundness of the subproofs we get ⊢𝑝 hRipo1 hSi and also
⊢𝑝 hSipo2 hT i. Applying the induction hypothesis we get ⊢𝑝 hS w ipo′2 hT w i. Since S 𝑎 S w , the
infer rule can be applied to the ﬁrst realizability triple resulting in ⊢𝑝 hRipo1 hS w i Then applying
rule (PSEQ) yields: ⊢𝑝 hRipo1 ;po2 hT w i.
   Consider rule (RDEM). Again, through the soundness of the sub proofs (Lemma A.5), we get
⊢𝑝 hRipo1 hSi and ⊢𝑝 hRipo2 hR𝑝 i. The induction hypothesis yields ⊢𝑝 hRw ipo𝑖′ hS w i with Rw = {r }.
Applying rule (PDEM) results in
                                        ⊢𝑝 hRw ipo1 + po2 hS w i .
   Consider rule (RLOOP). Through the soundness of the sub proofs (Lemma A.5), we get the re-
alizability triple ⊢𝑝 h𝐼 ipoh𝐼 i . Applying the induction hypothesis, we get the realizability triple
⊢𝑝 h𝐼 w ipo′ h𝐼 w i with 𝐼 w = {𝑖}. Applying rule (PLOOP) yields the realizability triple
                                               ⊢𝑝 h𝐼 w ipo′∗ h𝐼 w i .

                                                           27
                                                                    Roland Meyer, Jakob Tepe, and Sebastian Wolﬀ


  Consider rule (RTRANS). The induction hypothesis yields soundness of ⊢𝑝 po2 . Applying the
induction hypothesis again yields the sought after result: ⊢𝑝 po3 .
  Consider rule (RCSQ). The induction hypothesis yields ⊢𝑝 hRww ipo′ hS w i. Using rule (PCSQ), we
get ⊢𝑝 hRw ipo′ hS ww i.
  Lastly, consider rule (RGATHER). Applying the induction hypothesis yields ⊢𝑝 hR1 ipo′1 hS1 i and
⊢𝑝 hR2 ipo′2 hS2 i with sketch(po′1 ) = sketch(po′2 ). Applying the rule (PGATHER), we get
                                ⊢𝑝 hR1 ∪ R2 igather (po′1, po′2 )hS1 ∪ S2 i
                                                                                                              
Proof of Theorem 4.3. Again, we state theorem with the new notation:
  Theorem A.7. ⊢𝑝 po and ⊢𝑝 po′ and po 𝑝 po′ together imply po p∼ po′ .
   Proof. For this proof, we conduct a structural induction over the syntactic structure of the
proof po. Then, some cases require their own additional structural induction over the proof tree
of po′ in the proof outline calculus. In the following, we also have 𝑋 𝑎 𝑋 w for any selections 𝑋
and 𝑋 w .
   Base Case: po = com. Then, po′ = com. We show hRipohSi p∼ hRw ipo′ hS w i by induction over
the proof tree of ⊢𝑝 hRw ipo′ hS w i. In the base case, we have the realizability triple ⊢𝑝 hricomhsi.
Thus, we know that ÈcomÉ(r) 𝑑 s holds. Therefore, hRicomhSi p∼ h{r }icomh{s}i holds. In the
induction step, there are two cases. Either the rule (PGATHER) was used, or the rule (PCSQ) was
used. If (PGATHER) was used, we have ⊢𝑝 hR1 ∪ R2 icomhS1 ∪ S2 i. From this, we know that ⊢𝑝
hR𝑖 icomhS𝑖 i hold. Applying the induction hypothesis yields hRicomhSi p∼ hR𝑖 icomhS𝑖 i. Using the
rule (RGA), we get hRicomhSi p∼ h ∪𝑖 R𝑖 icomh ∪𝑖 R𝑖 i. If (PCSQ) was used, we have ⊢𝑝 hRw icomhS ww i.
From the precondition, we know ⊢𝑝 hRww icomhS w i holds. Using the induction hypothesis, we get
hRicomhSi p∼ hRww icomhS w i. Applying rule (RCSQ) yields hRicomhSi p∼ hRw icomhS ww i.
   Induction Step:
   If the proof is a sequence, i.e. hRipohT i = hRipo1 hSi;hSipo2 hT i , then the other proof is
hRw ipo′ hT w i = hRw ipo′1 hS w i;hS w ipo′2 hT w i .
   Thus we know that, the realizability triples ⊢𝑝 hSipo2 hT i and ⊢𝑝 hS w ipo′2 hT w i hold. Applying
the induction hypothesis, we get po2 p∼ po′2 . Applying the rule (RSEQR) yields
                       hRipo1 hSi;hSipo2 hT i p∼ hRipo1 hS w i;hS w ipo′2 hT w i .
  Because ⊢𝑝 hRipo1 hSi holds, the realizability triple ⊢𝑝 hRipo1 hS w i also holds due to the conse-
quence rule. We also have that ⊢𝑝 hRw ipo′1 hS w i is true. Applying the induction hypothesis, we get
hRipo1 hS w i p∼ hRw ipo′1 hS w i. Using rule (RSEQL) yields
                    hRipo′1 hS w i;hS w ipo′2 hT w i p∼ hRw ipo′1 hS w i;hS w ipo′2 hT w i .
Combined with the rewrite from before and rule (RTRANS), we have
                      hRipo1 hSi;hSipo2 hT i p∼ hRw ipo′1 hS w i;hS w ipo′2 hT w i .
  In the next case, the proof is a demonic choice, i.e.
                                 hRipohSi = hRipo1 hSi + hRipo2 hSi .
Then, the other proof is
                           hRw ipo′ hS w i = hRw ipo′1 hS w i + hRw ipo′2 hS w i .
We proceed by induction over the proof tree of
                                     hRw ipo′1 hS w i + hRw ipo′2 hS w i .

                                                      28
Realizability in Semantics-Guided Synthesis Done Eagerly


If the proof was done with the rule (PDEM), it has the following shape:
                                         hRw ipo′1 hS w i + hRw ipo′2 hS w i
with Rw = {r }. With the overall induction hypothesis and because the subproofs are sound, we
know that
                   hRipo1 hSi p∼ hRw ipo′1 hS w i and hRipo2 hSi p∼ hRw ipo′2 hS w i
hold. Using the rule (RDEM), we get
                        hRipo1 hSi + hRipo2 hSi p∼ hRw ipo′1 hS w i + hRw ipo′2 hS w i .
Next, we, again, have two possibilities. The proof was conducted using (PGATHER) or (PCSQ). Start-
ing with rule (PGATHER), the proof has the following shape:
                          ⊢𝑝 hR1w ∪ R2w ipo′1 hS1w ∪ S2w i + hR1w ∪ R2w ipo′2 hS1w ∪ S2w i
From preconditions of the gather rule we get
                                       ⊢𝑝 hR1w ipo′1 hS1w i + hR1w ipo′2 hS1w i
                                      ⊢𝑝 hR2w ipo′′  w       w    ′′ w
                                                 1 hS2 i + hR2 ipo2 hS2 i
and Applying the induction hypothesis then yields
                        hRipo1 hSi + hRipo2 hSi p∼ hR𝑖w ipo′1 hS𝑖w i + hR𝑖w ipo′2 hS𝑖w i .
Similarly for po′′      ′′
                1 and po2 . Using the rule (RGATHER) we get

hRipo1 hSi + hRipo2 hSi p∼ h ∪𝑖 R𝑖w igather (po′1, po′′       w           w            ′     ′′       w
                                                     1 )h ∪𝑖 S𝑖 i + h ∪𝑖 R𝑖 igather (po1 , po1 )h ∪𝑖 S𝑖 i .

Closing with the rule (PCSQ), the proof has the following shape:
                                      hRw ipo′1 hS ww i + hRw ipo′2 hS ww i .
From the precondition of the infer rule, we have
                                      hRww ipo′1 hS w i + hRww ipo′2 hS w i .
Using the induction hypothesis, we get the following rewrite:
                      hRipo1 hSi + hRipo2 hSi p∼ hRww ipo′1 hS w i + hRww ipo′2 hS w i .
Now, the rule (RCSQ) can be applied to get the sought after result:
                      hRipo1 hSi + hRipo2 hSi p∼ hRw ipo′1 hS ww i + hRw ipo′2 hS ww i .
This concludes the proof for demonic choices.
  In the next case, the proof is a loop. This case is analogous to demonic choices.
  Finally, consider the proof is over a nonterminal. So, the ﬁrst proof is
                          ⊢𝑝 hRiN(hR1 ipo1 hS1 i | . . . | hR𝑛 ipo𝑛 hS𝑛 i | po𝑟 )hSi .
Then, the other proof can either also be a weaker proof over a nonterminal or it is only one pro-
duction of the nonterminal. We start with the ﬁrst case. The second proof is then
                           ⊢𝑝 hRw iN(hR1w ipo′1 hS1w i | . . . | hR𝑛w ipo𝑛′ hS𝑛w i)hS w i .
We know that all the subproofs hold. Applying the induction hypothesis then yields the following
rewrites for all 𝑖:
                                 hR𝑖 ipo𝑖 hS𝑖 i p∼ hR𝑖w ipo𝑖′ hS𝑖w i .

                                                           29
                                                                       Roland Meyer, Jakob Tepe, and Sebastian Wolﬀ


We apply the rule (RANG) on the rewritten part several times. Together with rule (TRANS), we
combine the rewrites and get:
  hRiN(hR1 ipo1 hS1 i | . . . | hR𝑛 ipo𝑛 hS𝑛 i | po𝑟 )hSi p∼
                                               h ∪𝑖 R𝑖w iN(hR1w ipo′1 hS1w i | . . . | hR𝑛w ipo𝑛′ hS𝑛w i)h ∪𝑖 S𝑖w i .
  Moving on to the case where one production is chosen. Without loss of generality, let this be the
ﬁrst production. The proof therefore is ⊢𝑝 hR1w ipo′1 hS1w i. Since we know that ⊢𝑝 hR1 ipo1 hS1 i holds,
we can apply the induction hypothesis and get the rewrite hR1 ipo1 hS1 i p∼ hRw ipo′1 hS1w i. Then, we
apply rule (RAC) and get the following:
  hRiN(hR1 ipo1 hS1 i | . . . | hR𝑛 ipo𝑛 hS𝑛 i)hSi p∼
                                  hR1w ∪ (∪𝑖 R𝑖 )iN(hR1w ipo′1 hS1w i | . . . | hR𝑛 ipo𝑛 hS𝑛 i)hS1w ∪ (∪𝑖 S𝑖 )i .
Furthermore, the rule (RSELECT) can be applied to get
        hR1w ∪ (∪𝑖 R𝑖 )iN(hR1w ipo′1 hS1w i | . . . | hR𝑛 ipo𝑛 hS𝑛 i)hS1w ∪ (∪𝑖 S𝑖 )i p∼ hR1w ipo′1 hS1w i .
Lastly, applying the rule (RTRANS) yields the sought after result:
                     hRiN(hR1 ipo1 hS1 i | . . . | hR𝑛 ipo𝑛 hS𝑛 i)hSi p∼ hR1w ipo′1 hS1w i .
This concludes the proof.                                                                                               
  We proof the following lemma:
  Lemma A.8. The following implication holds:
   ⊢𝑝 hRipo1 hSi + hRipo2 hSi ∧ S 𝑎 {s} =⇒ ∃ r, po′1, po′2 : r ∈ R∧ ⊢𝑝 h{r }ipo′1 h{s}i∧
                             ⊢𝑝 h{r }ipo′2 h{s}i ∧ po1 𝑝 po′1 ∧ po2 𝑝 po′2 ∧
                                              sketch(po1 ) = sketch(po′1 ) ∧ sketch(po2 ) = sketch(po′2 ) .
  Proof. We conduct the proof by induction over the proof tree of
                                         ⊢𝑝 hRipo1 hSi + hRipo2 hSi
The base case holds trivially.
   In the ﬁrst case of the induction step, the proof was done using the rule (PDEM). Then, we have
⊢𝑝 hRipo1 hSi and also ⊢𝑝 hRipo2 hSi with R = {r }. Thus, we know ⊢𝑝 h{r }ipo𝑖 hSi. Using the rule
(PCSQ) on both proofs, we get the realizability triples ⊢𝑝 h{r }ipo𝑖 h{s}i.
  We have two remaining cases, either the proof was ﬁnished using the rule (PGATHER) or rule
(PCSQ). In the ﬁrst case, we have

                               ⊢𝑝 h ∪𝑖 R𝑖 ipo1 h ∪𝑖 S𝑖 i + h ∪𝑖 R𝑖 ipo2 h ∪𝑖 S𝑖 i
Since ∪𝑖 S𝑖 𝑎 {𝑠}, one assertion S𝑖 is stronger than {s}. Without loss of generality, let this be S1 .
From the above realizability triple, we know that the realizability triple
                                       ⊢𝑝 hR1 ipo′1 hS1 i + hR1 ipo′2 hS1 i
holds. Applying the induction hypothesis, we get an r and the proofs po′′       ′′
                                                                        1 and po2 for which the
realizability triples ⊢𝑝 h{r }ipo′′
                                 1  h{s}i and ⊢𝑝 h{r }ipo′′ h{s}i hold.
                                                         2
  In the second case, we have
                                        ⊢𝑝 hRipo1 hS w i + hRipo2 hS w i
The precondition of the rule (PCSQ) requires
                                        ⊢𝑝 hRw ipo1 hSi + hRw ipo2 hSi

                                                         30
Realizability in Semantics-Guided Synthesis Done Eagerly


Applying the induction hypothesis yields an r ∈ Rw and ⊢𝑝 h{r }ipo𝑖′ h{s}i. Since R 𝑎 Rw there is
an r ′ of R with r ′ 𝑑 r. Thus we can strengthen the precondition of the realizability triples to get
⊢𝑝 h{r ′ }ipo𝑖′ h{s}i.                                                                              
  We proof the following lemma:
  Lemma A.9. The following implication holds:

   ⊢𝑝 hRi(h𝐼 ipoh𝐼 i) ∗ hSi ∧ 𝑖 ∈ 𝐼 =⇒ ∃ po′ : ⊢𝑝 h{𝑖}ipo′ h{𝑖}i∧
                                                                po 𝑝 po′ ∧ sketch(po) = sketch(po′ ) .
  Proof. The proof is analogous to one of the previous lemma.                                             
Proof of Theorem 4.4. The proof is done by an induction over the structure of the prf. Again, we
ﬁrst state the theorem using the new notation:
   Theorem A.10 (Backtracking Freedom). Let ⊢𝑝 hRipohSi and s ∈ S. Then there are r and po′
so that hRipohSi p∼ h{r }ipo′ h{s}i, r ∈ R, and sketch(po′ ) ∈ drv(sketch(po)).
  Proof. Base Case: The proof is ⊢𝑝 hRicomhSi. Applying soundness yields a predicate r with
ÈcomÉ(r) 𝑑 s and r ∈ R. Therefore, we can apply rule (RCOM) and get hRicomhSi p∼ h{r }icomh{s}i.
  Induction Step: If the proof is a sequence, we have
                                            hRipo1 hSi;hSipo2 hT i .
Then, we know that the subproofs are true so po1 and po2 hold. Applying the induction hypothesis
on the second realizability triple from above, we get an s with s ∈ S and a proof po′2 for which the
following holds:
                                     hSipo2 hT i p∼ h{s}ipo′2 h{t}i .
Next, we apply the induction hypothesis on the other sequence and get a predicate r with r ∈ R
and a proof po′1 for which the following holds:
                                        hRipo1 hSi p∼ h{r }ipo′1 h{s}i .
Applying rule (RSEQR), we get the following rewrite:
                         hRipo1 hSi;hSipo2 hT i p∼ hRipo1 h{s}i;h{s}ipo′2 h{t}i .
Then, applying rule (RSEQL), we get the following rewrite:
                     hRipo1 h{s}i;h{s}ipo′2 h{t}i p∼ h{r }ipo′1 h{s}i;h{s}ipo′2 h{t}i .
Finally, with rule (RTRANS), we get the sought after result:
                        hRipo1 hSi;hSipo2 hT i p∼ h{r }ipo′1 h{s}i;h{s}ipo′2 h{t}i .
If the proof is a demonic choice, so we have
                                           hRipo1 hSi + hRipo2 hSi ,
and a predicate s with s ∈ S. Then we can apply Lemma A.8 to get a predicate r and the proofs
⊢𝑝 h{r }ipo′1 h{s}i and ⊢𝑝 h{r }ipo′2 h{s}i with po𝑖 𝑝 po𝑖′ . . Using Theorem 4.3, the following two
rewrites are sound:
                     hRipo1 hSi p∼ h{r }ipo′1 h{s}i and hRipo2 hSi p∼ h{r }ipo′2 h{s}i .
  An application of the rule (RDEM) then yields the sought after result:
                       hRipo1 hSi + hRipo2 hSi p∼ h{r }ipo′1 h{s}i + h{r }ipo′2 h{s}i .

                                                           31
                                                                    Roland Meyer, Jakob Tepe, and Sebastian Wolﬀ


  Moving on with loops. We have the proof ⊢𝑝 hRi(h𝐼 ipoh𝐼 i) ∗ hSi and a predicate s with s ∈ S.
Since 𝐼 𝑎 S, there also is an 𝑖 of 𝐼 with 𝑖 𝑑 s. Applying Lemma A.9, we get a proof po′ for which
⊢𝑝 h{𝑖}ipo′ h{𝑖}i holds and po 𝑝 po′ . Theorem 4.3 then yields
                                        h𝐼 ipoh𝐼 i p∼ h{𝑖}ipo′ h{𝑖}i .
  Applying rule (RLOOP) yields
                           hRi(h𝐼 ipoh𝐼 i) ∗ hSi p∼ h{𝑖}i(h{𝑖}ipo′ h{𝑖}i) ∗ h{𝑖}i .
Since R 𝑎 𝐼 , we know there is an r in R for which r 𝑑# 𝑖 holds. Applying rule (RCSQ), we get the
sought after result:
                          hRi(h𝐼 ipoh𝐼 i) ∗ hSi p∼ h{𝑟 }i(h{𝑖}ipo′ h{𝑖}i) ∗ h{𝑠}i .
  In the last case, we consider proofs over nonterminals. We have a predicate s and the proof
                             ⊢𝑝 hRiN(hR1 ipo1 hS1 i | . . . | hR𝑛 ipo𝑛 hS𝑛 i)hSi
with s ∈ S. Since (S1 ∪ . . . ∪S𝑛 ) = S, there is a selection S𝑖 with s ∈ S𝑖 . Without loss of generality, let
this 𝑖 be 1. We know the realizability triple ⊢𝑝 hR1 ipo1 hS1 i holds. Using the induction hypothesis,
we get the following for an r1 of R1 :
                                     hR1 ipo1 hS1 i p∼ h{r1 }ipo′1 h{s}i .
Using the rule (RANG), we get the following rewrite:
          N(hR1 ipo1 hS1 i | . . . | hR𝑛 ipo𝑛 hS𝑛 i) p∼ N(h{r1 }ipo′1 h{s}i | . . . | hR𝑛 ipo𝑛 hS𝑛 i) .
Then, with rule (RSELECT), we get
                      N(h{r1 }ipo′1 h{s}i | . . . | hR𝑛 ipo𝑛 hS𝑛 i) p∼ h{r1 }ipo′1 h{s}i .
Finally, applying rule (RTRANS) twice, we get
                    hRiN(hR1 ipo1 hS1 i | . . . | hR𝑛 ipo𝑛 hS𝑛 i)hSi p∼ h{r1 }ipo′1 h{s}i .
Because R1 ⊆ R, we have r1 ∈ R. This concludes the proof.                                                     

A.3 Proofs for Section 5
We show the following lemma:
  Lemma A.11. The function sp is monotonic (if the speciﬁcations of the nonterminals are monotonic):
                           R 𝑎 R′ =⇒ sp(R, sketch) 𝑎 sp(R′, sketch) .
   Proof. We proof this lemma by induction over the structure of sketch.
   Base Case: We show R 𝑎 R′ implies sp(R, com) 𝑎 sp(R′ , com). Let the predicate 𝑠 be of
sp(R′, com). Then, 𝑠 = ÈcomÉ(r ′ ) for some predicate r ′ of R′ . Since we know R 𝑎 R′ , there is
a predicate r in 𝑅 with 𝑟 𝑑 r ′ . Due to the interpretation of commands being monotonic, we get
that ÈcomÉ(𝑟 ) 𝑑 ÈcomÉ(r ′ ) = 𝑠. Because ÈcomÉ(𝑟 ) is in sp(R, com), sp(R, com) 𝑎 sp(R′, com)
follows.
   Induction Step: First, we consider the case where the sketch is a sequence. We show R 𝑎
R′ implies sp(R, sketch1 ; sketch2 ) 𝑎 sp(R′, sketch1 ; sketch2 ). From the induction hypothesis,
we know that sp(R, sketch1 ) 𝑎 sp(R′, sketch1 ) holds. Applying the induction hypothesis again
yields
                  sp(sp(R, sketch1 ), sketch2 ) 𝑎 sp(sp(R′, sketch1 ), sketch2 ) .
Inserting the deﬁnition of the strongest post function, we get
                        sp(R, sketch1 ; sketch2 ) 𝑎 sp(R′, sketch1 ; sketch2 ) .

                                                       32
Realizability in Semantics-Guided Synthesis Done Eagerly


   Next, we consider the case where the sketch is a choice. We show
               R 𝑎 R′ =⇒ sp(R, sketch1 + sketch2 ) 𝑎 sp(R′, sketch1 + sketch2 ) .
Let the predicate 𝑠 𝑗 be of sp(R′ , sketch1 + sketch2 ). Thus, there is an r ′ of R′ with 𝑠 ′𝑗 = 𝑠 1′ ⊔ 𝑠 2′
and 𝑠 1′ is of sp({r ′ }, sketch1 ) and 𝑠 2′ is of sp({r ′ }, sketch2 ). Since R 𝑎 R′ , there is an r of 𝑅 with
{r } 𝑎 {r ′ }. Applying the induction hypothesis yields
         sp({r }, sketch1 ) 𝑎 sp({r ′ }, sketch1 ) and sp({r }, sketch2 ) 𝑎 sp({r ′ }, sketch2 )
Therefore, there is an 𝑠 1 ∈ sp({r }, sketch1 ) and an 𝑠 2 ∈ sp({r }, sketch2 ) with {𝑠 1 } 𝑎 {𝑠 1′ } and
{𝑠 2 } 𝑎 {𝑠 2′ }. Therefore, 𝑠 𝑗 = 𝑠 1 ⊔ 𝑠 2 𝑑 𝑠 1′ ⊔ 𝑠 2′ = 𝑠 ′𝑗 . Since 𝑠 𝑗 is of sp(R, sketch1 + sketch2 ), we
have
                        sp(R, sketch1 + sketch2 ) 𝑎 sp(R′, sketch1 + sketch2 ) .
    Next, consider the sketch is a loop. We show
                        R 𝑎 R′ =⇒ sp(R, sketch∗ [𝐼 ]) 𝑎 sp(R′, sketch∗ [𝐼 ]) .
Let 𝑖 be of sp(R′ , sketch∗ [𝐼 ]). Thus, R′ 𝑎 {𝑖}. By transitivity we have R 𝑎 {𝑖} and thus 𝑖 is also
in sp(R, sketch∗ [𝐼 ]). The inequality 𝑖 𝑑 𝑖 holds trivially.
   Lastly, consider the sketch is a nonterminal. Monotonicity follows directly from the required
monotonicity of the speciﬁcation.
   This concludes the proof.                                                                          
   We show the following lemma:
  Lemma A.12 (Soundness). For any R of Selections and any sketch sketch of Sketches, the fol-
lowing realizability triple holds (if the speciﬁcations of the nonterminals and loops are sound):
                                       ⊢𝑎 hRisketchhsp(R, sketch)i .
   Proof. We proof this lemma by induction over the structure of the sketch.
   Base Case: We show ⊢𝑎 hRicomhsp(R, com)i. For every r ∈ R we can can show Ð    the realizability
triple ⊢𝑎 h{r }icomh{ÈcomÉ(r)}i. Using the rule (GATHER) we can show ⊢𝑎 hRicomh r ∈R {ÈcomÉ(r)}i.
By deﬁnition, this is the same as ⊢𝑎 hRicomhsp(R, com)i.
   Induction Step: First, consider a sequence of sketch. We show the realizability triple
                          ⊢𝑎 hRisketch1 ;sketch2 hsp(R, sketch1 ;sketch2 )i .
Applying the induction hypothesis twice yields the realizability triples:
⊢𝑎 hRisketch1 hsp(R, sketch1 )i and ⊢𝑎 hsp(R, sketch1 )isketch2 hsp(sp(R, sketch1 ), sketch2 )i .
Using rule (SEQ), we get the realizability triple
                        ⊢𝑎 hRisketch1 ;sketch2 hsp(sp(R, sketch1 ), sketch2 )i .
This is the same as the realizability triple ⊢𝑎 hRisketch1 ;sketch2 hsp(R, sketch1 ;sketch2 )i .
  Next, consider the sketch is a choice. We show
                         ⊢𝑎 hRisketch1 + sketch2 hsp(R, sketch1 + sketch2 )i .
From the deﬁnition of the strongest post, we know that it is the following:
                                Ø
    sp(R, sketch1 + sketch2 ) =    {s1 ⊔ s2 | s1 ∈ sp({r }, sketch1 ) ∧ s2 ∈ sp({r }, sketch2 )} .
                                      r ∈R
For every r of R, we know from the induction hypothesis that ⊢𝑎 h{r }isketch1 hsp({r }, sketch1 )i
and ⊢𝑎 h{r }isketch2 hsp({r }, sketch2 )i hold. Using the rule (CSQ), we can show the realizability
triples ⊢𝑎 h{r }isketch1 h{s𝑘1 }i for any s𝑘1 of sp({r }, sketch1 ) and ⊢𝑎 h{r }isketch2 h{s𝑘2 }i for any

                                                           33
                                                                Roland Meyer, Jakob Tepe, and Sebastian Wolﬀ


s𝑘2 of sp({r }, sketch2 ). Let s 𝑗 be the join of any two s𝑘1 and s𝑘2 . Using the rule (CSQ), we can show
⊢𝑎 h{r }isketch𝑖 h{s 𝑗 }i. With the rule (DEM), we get ⊢𝑎 h{r }isketch1 + sketch2 h{s 𝑗 }i. Applying
rule (GATHER) yields
                  ⊢𝑎 h{r }isketch1 + sketch2 h{s1 ⊔ s2 | s𝑖 ∈ sp({r }, sketch𝑖 )}i .
  Applying rule (GATHER) once more yields
                                         Ø
                ⊢𝑎 hRisketch1 + sketch2 h {s1 ⊔ s2 | s𝑖 ∈ sp({r }, sketch𝑖 )}i .
                                               r ∈R
This is the same as ⊢𝑎 hRisketch1 + sketch2 hsp(R, sketch1 + sketch2 )i.
  Next, consider the sketch is a loop. Let 𝑖 be of sp(R, sketch∗ ). From soundness of the invariant
annotation, we get ⊢𝑎 h{𝑖}isketchh{𝑖}i. With rule loop, we get ⊢𝑎 h{𝑖}isketch∗ h{𝑖}i. With gather,
we get
                          ⊢𝑎 hsp(R, sketch∗ )isketch∗ hsp(R, sketch∗ )i .
With (CSQ), we get ⊢𝑎 hRisketch∗ hsp(R, sketch∗ )i.
  Finally, consider the sketch is a nonterminal. Soundness follows directly from the required
soundness of the speciﬁcation of the nonterminal.
  This concludes the proof.                                                                      
  We show the following corollary:
   Corollary 1. For any R, S of Selections and any sketch sketch of Sketches with sound annota-
tions, the following implication holds:
                            sp(R, sketch) 𝑎 S =⇒ ⊢𝑎 hRisketchhSi .
  Proof. Lemma A.12 yields ⊢𝑎 hRisketchhsp(R, sketch)i. Applying rule (CSQ) gives us the
sought after result ⊢𝑎 hRisketchhSi                                                    
Proof of Theorem 5.2.
  We have already shown soundness above. We prove completeness by an induction over the
proof tree of ⊢𝑎 hRisketchhSi.
  Base Case: We show ⊢𝑎 h{r }icomh{s}i =⇒ sp({r }, com) 𝑎 {s}. From the precondition of
rule (COM), we know ÈcomÉ(r) 𝑑 s. Therefore sp({r }, com) = {ÈcomÉ(r)} 𝑎 {s}.
  Induction Step: Consider the rule (SEQ). We show that the validity of ⊢𝑎 hRisketch1 ; sketch2 h𝑇 i
implies sp(R, sketch1 ; sketch2 ) 𝑎 𝑇 . From the preconditions we know that both ⊢𝑎 hRisketch1 hSi
and ⊢𝑎 hSisketch2 h𝑇 i hold. Applying the induction hypothesis yields sp(R, sketch1 ) 𝑎 S and
sp(S, sketch2 ) 𝑎 𝑇 . Because the strongest post function is monotonic we get the sought after
inequality sp(R, sketch1 ; sketch2 ) 𝑎 𝑇 .
  Consider the rule (DEM). We show
              ⊢𝑎 h{r }isketch1 + sketch2 hSi =⇒ sp({r }, sketch1 + sketch2 ) 𝑎 S .
From the preconditions we know that ⊢𝑎 h{r }isketch1 hSi and ⊢𝑎 h{r }isketch2 hSi hold. Applying
the induction hypothesis yields the inequalities sp({r }, sketch1 ) 𝑎 S and sp({r }, sketch2 ) 𝑎 S.
Let the predicate 𝑠 be an element of 𝑆. Because the strongest posts are more versatile than 𝑆, there
is an 𝑠𝑖 of each strongest post with 𝑠𝑖 𝑑 𝑠. Therefore, 𝑠 is an upper bound of 𝑠 1 and 𝑠 2 and thus
𝑠 1 ⊔𝑠 2 𝑑 𝑠 holds. To conclude this case, see that 𝑠 1 ⊔𝑠 2 ∈ sp({r }, sketch1 +sketch2 ), and therefore
sp({r }, sketch1 + sketch2 ) 𝑎 S holds.
    Consider the rule (ANG). Completeness follows directly from the requirement that the speciﬁca-
tion of the nonterminals is complete.

                                                      34
Realizability in Semantics-Guided Synthesis Done Eagerly


  Consider the rule (CSQ). We show
                              ⊢𝑎 hRisketchhS ′ i =⇒ sp(R, sketch) 𝑎 S ′ .
From the preconditions, we know that the realizability triple ⊢𝑎 hR′ isketchhSi holds with R 𝑎 R′
and S 𝑎 S ′ . From the induction hypothesis we know that sp(R′, sketch) 𝑎 S. The sought after re-
sult immediately follows from monotonicity and because the relation 𝑎 is transitive: sp(R, sketch) 𝑎
S′ .
    Consider the rule (LOOP). We show ⊢𝑎 h{𝑖}isketch∗ [𝐼 ] h{𝑖}i implies sp({𝑖}, sketch∗ [𝐼 ]) 𝑎 {𝑖}.
Due to the precondition of rule (LOOP) and completeness of the annotation, we have 𝑖 ∈ 𝐼 . Thus,
𝑖 ∈ sp({𝑖}, sketch∗ [𝐼 ]) and therefore the inequality trivially holds.
    Lastly, consider the rule (GATHER). We show
                      ⊢𝑎 h ∪𝑖 R𝑖 isketchh ∪𝑖 S𝑖 i =⇒ sp(∪𝑖 R𝑖 , sketch) 𝑎 (∪𝑖 S𝑖 ) .
  From the preconditions we know that ⊢𝑎 hR𝑖 isketchhS𝑖 i hold. Applying the induction hy-
pothesis yields sp(R𝑖 , sketch) 𝑎 S𝑖 . Using monotonicity of the strongest post function, we get
sp(∪𝑖 R𝑖 , sketch) 𝑎 S𝑖 for every 𝑖. Together, this means sp(∪𝑖 R𝑖 , sketch) 𝑎 (∪𝑖 S𝑖 ) This concludes
the proof.                                                                                            
Proof of Theorem 5.1.
   We prove soundness by induction over the structure of the sketch.
   Base Case: We show |= vc(hRicomhSi) =⇒ ⊢𝑎 hRicomhSi. Because the veriﬁcation conditions
hold, we know that the inequality sp(R, com) 𝑎 S is true. The realizability triple ⊢𝑎 hRicomhSi
immediately follows from Corollary 1.
   Induction Step: In the ﬁrst case, the sketch is a sequence. We know the following veriﬁcation
conditions hold: |= vc(hRisketch1 ; sketch2 hSi). Thus, we know that the veriﬁcation conditions
|= vc(hRisketch2 hsp(R, sketch1 )i) and |= vc(hsp(R, sketch1 )isketch2 hSi) also hold. Applying
the induction hypothesis yields
                ⊢𝑎 hRisketch1 hsp(R, sketch1 )i and ⊢𝑎 hsp(R, sketch1 )isketch2 hSi .
Using the rule (SEQ), we get ⊢𝑎 hRisketch1 ; sketch2 hSi.
   If the sketch is a choice, we have sp(R, sketch1 + sketch2 ) 𝑎 S and for every 𝑟 ∈ R we have
|= vc(h{r }isketch1 hsp({r }, sketch1 )i) and |= vc(h{r }isketch2 hsp({r }, sketch2 )i). Applying the
induction hypothesis yields the two realizability triples ⊢𝑎 h{r }isketch1 hsp({r }, sketch1 )i and
⊢𝑎 h{r }isketch2 hsp({r }, sketch2 )i for every 𝑟 ∈ R. Using rule (CSQ), we can show the realizabil-
ity triple ⊢𝑎 h{r }isketch1 hsp({r }, sketch1 + sketch2 )i and ⊢𝑎 h{r }isketch2 hsp({r }, sketch1 +
sketch2 )i. Using the rule (DEM), we get ⊢𝑎 h{r }isketch1 + sketch2 hsp({r }, sketch1 + sketch2 )i
for every 𝑟 ∈ R. Using the gather rule, we get ⊢𝑎 hRisketch1 + sketch2 hsp(R, sketch1 + sketch2 )i.
Applying the rule (CSQ), we get ⊢𝑎 hRisketch1 + sketch2 hSi.
   If the sketch is a loop, we have the veriﬁcation conditions |= ( 𝑖 ∈𝐼 vc(h{𝑖}ish{𝑖}i)) from the
                                                                        Ð
check annotation function and the inequality sp(R, s∗ [𝐼 ]) 𝑎 S. The induction hypothesis yields
the realizability triple ⊢𝑎 h{𝑖}ish{𝑖}i for every 𝑖 ∈ 𝐼 . Applying the rule (LOOP) yields ⊢𝑎 h{𝑖}is∗ h{𝑖}i
for every 𝑖 ∈ 𝐼 . Since sp(R, s∗ [𝐼 ]) is a subset of 𝐼 we can use multiple applications of the rule
(GATHER) to get ⊢𝑎 hsp(R, s∗ [𝐼 ])is∗ hsp(R, s∗ [𝐼 ])i. Per deﬁnition, we have R 𝑎 sp(R, s∗ [𝐼 ]). Using
the rule (CSQ), we get that ⊢𝑎 hRis∗ hSi holds.
   If the sketch is a nonterminal, we know that sp(R, N[Γ]) 𝑎 S holds and from the check annota-
tions function we know there is aÐ𝑗 with |= vc(hRiproghsp(R, prog)i) for every prog of the oracle
function O(N, 𝑗 ). Also, we have ( prog∈O(N,𝑗 ) sp(R, prog)) 𝑎 Γ(R). Using the induction hypothe-
sis and rule (ANG), we get ⊢𝑎 hRiNhsp(R, prog)i for every prog of O(N, 𝑗 ). Using the gather rule,

                                                           35
                                                                Roland Meyer, Jakob Tepe, and Sebastian Wolﬀ


we get ⊢𝑎 hRiNh prog∈O(N,𝑗 ) sp(R, prog)i. Using the rule (CSQ), we get ⊢𝑎 hRiNhΓ(R)i. Since Γ(R)
                  Ð
is equal to sp(R, N[Γ]), we can apply (CSQ) one more time to get ⊢𝑎 hRiNhSi.
   Next, we show completeness. First, see that if S 𝑎 S w and |= vc(hRisketchhSi) then we also
have |= vc(hRisketchhS w i). We proceed by induction over the structure of sketches.
   Base Case: We have sketch = com. Completeness results from completeness of sp.
   Induction Step: We have |=𝑎 hRisketch1 ; sketch2 hSi. From soundness of the strongest post
and the induction hypothesis, we get |= vc(hRisketch1 hsp(R, sketch1 )i) and we also get the veri-
ﬁcation conditions of |= vc(hsp(R, sketch1 )isketch2 hsp(R, sketch1 ; sketch2 )i). Because of com-
pleteness of the strongest post and our remark that the post condition in veriﬁcation conditions
may be weakened, we get |= vc(hsp(R, sketch1 )isketch2 hSi).
   The proof for choices directly follows from soundness and completeness of the strongest post
function. Then, only an application of the induction hypothesis is left.
   In the case of loops we can discharge the ﬁrst inequality by soundness and completeness from
strongest post. The inequalities from the check annotation function are true because the annota-
tions are sound and thus the induction hypothesis can be applied.
   The case for non-terminals is more cumbersome. The ﬁrst inequality follows from completeness
of the strongest post function. We now discuss why the inequalities in the check annotations
function hold: From |=𝑎 hRiN[Γ] hSi, we get for every s ∈ S a program prog and an r ∈ S for
which |=𝑑 {r }prog{s} holds. This implies that |=𝑎 h{r }iprogh{s}i holds. From completeness of
the strongest post, we get sp({r }, prog) 𝑎 {s}. By monotonicity of the strongest post function,
we get sp(R, prog) 𝑎 {s}. We collect the programs returned from completeness in the set P. We get
that (∪prog∈P sp(R, prog)) 𝑎 S. Since 𝑆 is ﬁnite, P is ﬁnite. Thus, there is a 𝑗 for which P ⊆ O(N, 𝑗 )
holds. With this, we also have (∪prog∈O(N,𝑗 ) sp(R, prog)) 𝑎 S. The veriﬁcation conditions on the
individual programs hold because of the soundness of the strongest post function and the induction
hypothesis.                                                                                          

A.4   Proofs for Section 6
Proof of Theorem 6.1
First, we state the theorem using the new notation:
  Theorem A.13 (syn-Sound-And-Complete). Consider ⊢𝑝 hRipohSi and s ∈ S with s ≠ fail.
Then syn(hRipohSi, s) = (r, prog) with r ∈ R, r ≠ fail, prog ∈ drv(sketch(po)), and |=𝑑 {r }prog{s}.
The number of SMT solver calls is at most |po|.
   Proof. We proof this theorem by induction over the shape of hRipohSi.
   Base Case: We have the valid realizability triple hRicomhSi. Thus, we know for every s′ ∈
S there is an r ∈ R with ÈcomÉ(r) 𝑑 s′ . Since s is of S, the call syn(hRicomhSi, s) eventually
terminates returning (r, com). The predicate r cannot be fail because s is not fail and com preserves
fail. Also com ∈ drv(com) holds trivially. Moreover, since ÈcomÉ(r) 𝑑 s, the Hoare triple |=𝑑
{r }com{s} holds. Since we only have to go through R once to ﬁnd a suitable r, the number of SMT
solver calls is at most |R| ≤ |po|.
   Induction Step: In the ﬁrst case, we have hRipo1 ; po2 hSi. Thus, the call is syn(hRipo1 ; po2 hSi, s).
Let T be the intermediary selection. Applying the induction hypothesis, the call syn(po2, s) returns
(t, prog2 ) with t ∈ T , t ≠ fail, prog2 ∈ drv(sketch(po2 )), and |=𝑑 {t}prog2 {s}. Also the number
of SMT calls is at most |po2 |. Then we call syn(po1, t) and by the induction hypothesis we get
(r, prog1 ) with r ∈ R, r ≠ fail, prog1 ∈ drv(sketch(po1 )), and |=𝑑 {r }prog1 {t}. Also the number of
SMT calls is at most |po1 |. Put together, the function returns (r, prog1 ; prog2 ). Since both Hoare
triples hold, we get |=𝑑 {r }prog1 ; prog2 {s}. Also, we have prog1 ; prog2 ∈ drv(sketch(po)). And
the number of SMT calls is at most |po1 | + |po2 | ≤ |po|.

                                                   36
Realizability in Semantics-Guided Synthesis Done Eagerly


    In the next case, we have hRiN(po)hSi. We have two sub-cases: First, po is only one proof outline
as opposed to many separated by the | symbol. Then the pre and post condition of po and N(po)
match. We directly get the sought after result by applying the induction hypothesis and seeing
that drv(sketch(po)) ⊆ drv(sketch(N(po))). In the second sub-case, we know that po = po1 | po2 .
Since S is the union of all posts of po, we know that eventually we try out a subproof with s in its
post. Then, the induction hypothesis is applied again directly yielding the required results.
    In the next case, we have hRipo1 hSi + hRipo2 hSi. Because the proof outline is valid, we know
that for every s ∈ S there is an r of R for which there is a program prog1 + prog2 for which
|=𝑑 {r }prog1 + prog2 {s} holds. This implies that |=𝑑 {r }prog𝑖 {s} must hold. This also means, the
realizability triple |=𝑎 hriprog𝑖 hsi holds which in turn implies that |=𝑎 hridrv(po𝑖 )hsi holds. By
completeness, the outlines po𝑖′ can be built when supplied with the correct r ∈ R. Then, we use the
induction hypothesis to get (r, prog𝑖 ) from the recursive calls with r ∈ {r } ⊆ R, and the Hoare
triple |=𝑑 {r }prog𝑖 {s}, and prog𝑖 ∈ drv(sketch(po𝑖′ )), and the number of SMT solver calls for each
recursion is at most |po𝑖′ |. Since sketch(po𝑖 ) = sketch(po𝑖′ ) we also have that prog1 + prog2 is of
sketch(po1 + po2 ). Because |=𝑑 {r }prog𝑖 {s}, we also have |=𝑑 {r }prog1 + prog2 {s}. When the proof
outlines po𝑖′ are properly looked up, there is no need for additional SMT calls. Thus, the SMT calls
are at most |po′1 + po′2 | ≤ |po1 + po2 |.
    In the last case consider a loop hRih𝐼 ipoh𝐼 i ∗ hSi. In the case the realizability triple of the loop
was weakened, we keep the original invariant selections. Thus R resp. S are stronger resp. weaker
than 𝐼 . We have 𝐼 𝑎 S. Therefore, there is an 𝑖 of 𝐼 with 𝑖 𝑑 s. This 𝑖 will eventually be found by
the syn function. Since the proof is sound, 𝐼 is a sound invariant for sketch(po). Thus, for every 𝑖 of 𝐼 ,
the realizability triple ⊢𝑎 h{𝑖}isketch(po)h{𝑖}i is valid. Therefore, the proof outline po′ can be con-
structed. By the induction hypothesis, syn(po′ , 𝑖) returns (𝑖, prog) with prog ∈ drv(sketch(po′ )),
and |=𝑑 {𝑖}prog{𝑖}, and the number of SMT solver calls is at most |po′ |. Because |=𝑑 {𝑖}prog{𝑖}
holds, we also have |=𝑑 {𝑖}prog∗ {𝑖}. Since R 𝑎 𝐼 there is an r of R with r 𝑑 𝑖. Since 𝑖 𝑑 s,
we can weaken to |=𝑑 {r }prog∗ {s} and return r ∈ R. Because prog ∈ drv(sketch(po′ )), we have
prog∗ ∈ drv(sketch(po′ ) ∗ ). Because sketch(po′ ) = sketch(po), we have prog∗ ∈ drv(sketch(po) ∗ ).
Because the proof outline po′ can be looked up and does not need recomputing, we need at most
|𝐼 | additional SMT calls. All in all, we have at most |po| SMT calls.                                   

A.5    Proofs for Section 7
  Definition 2. An abstract predicate is fail or maps variables to sets of states of the SMR automaton.
                                   Predicates # = (Vars → P (O)) ∪ {fail}
   To substitute the original more precise relation 𝑑 deﬁned on Predicates, we introduce a new
relation on the abstracted domain.
  Definition 3. We deﬁne a stronger relation 𝑑# on Predicates # .
                               𝑎 𝑑# 𝑏 ⇔ 𝑏 = fail ∨ ∀ 𝑣 ∈ Vars : 𝑎(𝑣) ⊆ 𝑏 (𝑣)
  Ignoring the predicate fail, this relation matches the order in Meyer and Wolﬀ’s paper.
   Definition 4. We deﬁne a predicate abstraction function to abstract the original predicate and a
predicate concretisation function to concretize abstract predicates. The predicate abstraction function
is a cartesian abstraction:
                                     𝛼𝑑 : Predicates → Predicates #
Let 𝑣 be a variable in Vars. Then, the function is deﬁned as follows:
                                  (
                                    𝛼𝑑 (𝑟 ) = fail           , 𝑟 = fail
                                    𝛼𝑑 (𝑟 ) (𝑣) = 𝑞 ∈𝑟 𝑞(𝑣) , else
                                                  Ð


                                                           37
                                                                         Roland Meyer, Jakob Tepe, and Sebastian Wolﬀ


We continue with the demon concretisation function:
                                        𝛾𝑑 : Predicates # → Predicates
                                (
                                    fail                                                 , 𝑎 = fail
                     𝛾𝑑 (𝑎) =
                                    {𝑞 ∈ States | ∀𝑣 ∈ Vars : 𝑞(𝑣) ⊆ 𝑎(𝑣)}               , else

  Lemma A.14. 𝑟 𝑑 𝑠 =⇒ 𝛼𝑑 (𝑟 ) 𝑑# 𝛼𝑑 (𝑠) .
  Proof. If the predicate 𝑠 is fail, then 𝛼𝑑 (𝑠) is also fail so the inequality holds. Otherwise, we
have
                                              Ø             Ø
                                𝑟 ⊆ 𝑠 =⇒ ( 𝑞(𝑣)) ⊆ ( 𝑞(𝑣))
                                                    𝑞 ∈𝑟              𝑞 ∈𝑠

                                             =⇒ 𝛼𝑑 (𝑟 ) 𝑑# 𝛼𝑑 (𝑠) .
Here, 𝑣 is any variable of Vars.                                                                                   
  Lemma A.15. 𝑎 𝑑# 𝑏     =⇒ 𝛾𝑑 (𝑎) 𝑑 𝛾𝑑 (𝑏) .
  Proof. If the abstract predicate 𝑏 is fail, then 𝛾𝑑 (𝑏) is also fail so the inequality holds. Otherwise,
we have
                    𝑎(𝑣) ⊆ 𝑏 (𝑣) =⇒ {𝑝 ∈ States | ∀𝑣 ′ ∈ Vars : 𝑝 (𝑣) ⊆ 𝑎(𝑣)} ⊆
                                                {𝑝 ∈ States | ∀𝑣 ′ ∈ Vars : 𝑝 (𝑣) ⊆ 𝑏 (𝑣)}
                                      =⇒ 𝛾𝑑 (𝑎) 𝑑 𝛾𝑑 (𝑏) .
Here, 𝑣 is any variable of Vars.                                                                                   
                                                                                                          #
  Lemma A.16. The pair (𝛼𝑑 , 𝛾𝑑 ) is a Galois connection between Predicates and Predicates :
                                                           𝛾𝑑
                                (Predicates, 𝑑 ) ←
                                                  −−−
                                                    −−→
                                                    𝛼−
                                                      −− (Predicates #, 𝑑# )
                                                            𝑑

This means, the following inequalities hold:
                                       ∀𝑟 ∈ Predicates : 𝑟 𝑑 𝛾𝑑 (𝛼𝑑 (𝑟 ))
                                      ∀𝑎 ∈ Predicates # : 𝛼𝑑 (𝛾𝑑 (𝑎)) 𝑑# 𝑎
   Proof. We start the proof with the ﬁrst equation. Let 𝑟 be of Predicates. If 𝑟 = fail then 𝛾𝑑 (𝛼𝑑 (𝑟 )) =
fail. Thus, the inequality 𝑟 𝑑 𝛾𝑑 (𝛼𝑑 (𝑟 )) = fail holds. If 𝑟 is not fail, then
                                                                         Ø
                      𝛾𝑑 (𝛼𝑑 (𝑟 )) = {𝑝 ∈ States | ∀𝑣 ∈ Vars : 𝑝 (𝑣) ⊆        𝑞(𝑣)} .
                                                                                  𝑞 ∈𝑟

Let the state 𝑞 be of 𝑟 . Then 𝑞 is also in 𝛾𝑑 (𝛼𝑑 (𝑟 )). Therefore 𝑟 ⊆ 𝛾𝑑 (𝛼𝑑 (𝑟 )). And that means
𝑟 𝑑 𝛾𝑑 (𝛼𝑑 (𝑟 )).
   We continue with the second equation. Let 𝑎 be of Predicates # . If 𝑎 is fail, then 𝛼𝑑 (𝛾𝑑 (𝑎)) is
trivially stronger. If 𝑎 is not fail, then we show that for any 𝑣 of Vars the inclusion 𝛼𝑑 (𝛾𝑑 (𝑎)) (𝑣) ⊆
𝑎(𝑣) holds. Let 𝑣 be of Vars. Then
                         𝛼𝑑 (𝛾𝑑 (𝑎)) (𝑣) = ∪𝑞 ∈𝛾𝑑 (𝑎) 𝑞(𝑣)
                                           = ∪𝑞 ∈ {𝑝 ∈States|∀𝑣′ ∈Vars:𝑝 (𝑣′ ) ⊆𝑎 (𝑣′ ) } 𝑞(𝑣)
                                           ⊆ 𝑎(𝑣) .
This concludes the proof.                                                                                          
  Lemma A.17. The relation 𝑑# is a partial order relation on Predicates # .

                                                           38
Realizability in Semantics-Guided Synthesis Done Eagerly


   Proof. We ﬁrst show reﬂexivity. Let 𝑎 be of Predicates # . If 𝑎 = fail, then the inequality 𝑎 𝑑# 𝑎
trivially holds. Otherwise, let 𝑣 be a variable of Vars. Then the inclusion 𝑎(𝑣) ⊆ 𝑎(𝑣) also holds.
   We continue with transitivity. Let 𝑎, 𝑏 and 𝑐 be of Predicates # . We assume that the inequalities
𝑎 𝑑# 𝑏 and 𝑏 𝑑# 𝑐 are true. If 𝑐 = fail, then the inequality 𝑎 𝑑# 𝑐 trivially holds. Otherwise, we
get that 𝑏 ≠ fail and also 𝑎 ≠ fail. Let 𝑣 be of Vars. We have 𝑎(𝑣) ⊆ 𝑏 (𝑣) and 𝑏 (𝑣) ⊆ 𝑐 (𝑣). Through
transitivity of the relation ⊆ we also get the inclusion 𝑎(𝑣) ⊆ 𝑐 (𝑣).
   Lastly, we show antisymmetry. Let 𝑎 and 𝑏 be of Predicates # . We have 𝑎 𝑑# 𝑏 and 𝑏 𝑑# 𝑎. If 𝑎 is
fail then 𝑏 must also be fail and vice versa. If neither one is fail, let 𝑣 be of Vars. We know that the
inequalities 𝑎(𝑣) ⊆ 𝑏 (𝑣) and 𝑏 (𝑣) ⊆ 𝑎(𝑣) are true and thus we have 𝑎(𝑣) = 𝑏 (𝑣) for all 𝑣 of Vars.
That means, 𝑎 and 𝑏 are equal.                                                                         
  Lemma A.18. The partial order (Predicates #, 𝑑# ) is a complete lattice. In fact, the join and meet
can be computed by the following equations: Let 𝐴 be a subset of Predicates # .
                             (
                               ⊔(𝐴) = fail                  , fail ∈ 𝐴
                               ⊔(𝐴) (𝑣) = 𝑎∈𝐴 𝑎(𝑣)
                                          Ð
                                                            , else
                             (
                               ⊓(𝑅) = fail                  , 𝑅 = {fail}
                               ⊓(𝑅) = 𝑎∈ (𝐴\{fail} ) 𝑎(𝑣) , else
                                       Ñ

   Proof. Let 𝐴 be a subset of Predicates # . Let 𝑎 be an element of 𝐴. We ﬁrst show that the join
is an upper bound 𝑎 𝑑# ⊔(𝐴). If fail ∈ 𝐴, then ⊔(𝐴) = fail so the inequality 𝑎 𝑑# ⊔(𝐴) trivially
holds. Otherwise, let 𝑣 be of Vars. The inclusion 𝑎(𝑣) ⊆ 𝑎′ ∈𝐴 𝑎 ′ (𝑣) holds trivially, since 𝑎 ∈ 𝐴.
                                                               Ð
Now, to show that the join is the least upper bound, let 𝑢 be an upper bound of 𝐴. If 𝑢 is fail the
inequality ⊔(𝐴) 𝑑# 𝑢 holds trivially. Otherwise, if 𝑢 is not fail, we know fail ∉ 𝐴. Let 𝑣 be of
Vars. For any abstract demon 𝑎 of 𝐴, 𝑎(𝑣) ⊆ 𝑢 (𝑣) must hold. Therefore the inclusion ⊔(𝐴) (𝑣) =
                                                          #
   𝑎∈𝐴 𝑎(𝑣) ⊆ 𝑢 (𝑣) holds. Thus, the inequality ⊔(𝐴) 𝑑 𝑢 is true.
Ð
   Moving on with the meet. Let 𝑎 be an element of 𝐴. We ﬁrst show that the meet is a lower
bound: ⊓(𝐴) 𝑑# 𝑎. If 𝐴 = {fail}, then 𝑎 = fail so the inequality ⊓(𝐴) Ñ𝑑# 𝑎 trivially holds.
Otherwise, let 𝑣 be of Vars. Then, by deﬁnition we know that ⊓(𝐴) (𝑣) = 𝑎′ ∈𝐴\{fail} 𝑎 ′ (𝑣). If 𝑎
is fail, the inequality trivially holds. Otherwise, ⊓(𝐴) (𝑣) ⊆ 𝑎(𝑣) is also true. Now, to show that the
meet is the greatest lower bound, let 𝑙 be a lower bound of 𝐴. If 𝑙 is fail, 𝐴 must be {fail} and thus
⊓(𝐴) = fail, so 𝑙 𝑑# ⊓(𝐴) trivially holds. Otherwise, let 𝑣 be of Vars. Then for any 𝑎 of 𝐴 that is
not fail, 𝑙 (𝑣) ⊆ 𝑎(𝑣) must hold. Thus, 𝑙 (𝑣) ⊆ 𝑎′ ∈𝐴\{fail} 𝑎 ′ (𝑣) = ⊓(𝐴) (𝑣) holds. And therefore the
                                                Ñ
inequality 𝑙 𝑑# ⊓(𝐴) is true.                                                                         
  Next, we lift the abstract predicates to abstract selections. We remind the reader, that selections
are sets of predicates, i.e. Selections = P (Predicates).
  Definition 5. An Abstract Selection is a set of abstract predicates.
                                         Selections # = P (Predicates # )
  The more versatile relation on abstract angels is the same as on Selections, except that the ele-
ments of the abstract selections are compared using the abstract more precise relation deﬁned on
abstract predicates.
  Definition 6. 𝐴 𝑎# 𝐵 ⇔ ∀𝑏 ∈ 𝐵 : ∃ 𝑎 ∈ 𝐴 : 𝑎 𝑑# 𝑏
   Definition 7. The selection abstraction function 𝛼𝑎 relates elements of Selections to their abstract
representation in Selections # .
                                   𝛼𝑎 : Selections → Selections #

                                                           39
                                                                           Roland Meyer, Jakob Tepe, and Sebastian Wolﬀ


                                           𝛼𝑎 (𝑅) = {𝛼𝑑 (𝑟 ) | 𝑟 ∈ 𝑅}
  The selection concretisation function 𝛾𝑎 relates elements of Selections # to the elements of the original
domain Selections.
                                     𝛾𝑎 : Selections # → Selections
                                          𝛾𝑎 (𝐴) = {𝛾𝑑 (𝑎) | 𝑎 ∈ 𝐴}
  Lemma A.19. 𝑅 𝑎 𝑆 =⇒ 𝛼𝑎 (𝑅) 𝑎# 𝛼𝑎 (𝑆) .
  Proof. Let 𝛼𝑑 (𝑠) be of 𝛼𝑎 (𝑆). We know there is a predicate 𝑟 in 𝑅 more precise than 𝑠. Thus,
the inequality 𝛼𝑑 (𝑟 ) 𝑑# 𝛼𝑑 (𝑠) is true. And therefore the inequality 𝛼𝑎 (𝑅) 𝑎# 𝛼𝑎 (𝑆) holds. 

  Lemma A.20. 𝐴 𝑎 𝐵 =⇒ 𝛾𝑎 (𝐴) 𝑎 𝛾𝑎 (𝐵) .
   Proof. Let the predicate 𝛾𝑑 (𝑏) be of 𝛾𝑎 (𝐵). We know there is an abstract predicate 𝑎 of 𝐴 with
𝑎 𝑑# 𝑏. Thus, 𝛾𝑑 (𝑎) is more precise than 𝛾𝑑 (𝑏). Since 𝛾𝑑 (𝑎) ∈ 𝛾𝑎 (𝐴), we know the inequality
𝛾𝑎 (𝐴) 𝑎 𝛾𝑎 (𝐵) holds.                                                                           

  Lemma A.21. The pair (𝛼𝑎 , 𝛾𝑎 ) is a Galois connection between Selections and Selections # :
                                                          𝛾𝑎
                                  (Selections, 𝑎 ) ←
                                                    −−−
                                                      − −− (Selections # , 𝑎# )
                                                       −→
                                                      𝛼−   𝑎

This means, the following inequalities hold:
                                     ∀𝑅 ∈ Selections : 𝑅 𝑎 𝛾𝑎 (𝛼𝑎 (𝑅))
                                    ∀ 𝐴 ∈ Selections # : 𝛼𝑎 (𝛾𝑎 (𝐴)) 𝑎# 𝐴
   Proof. We start the proof with the ﬁrst inequality. Let 𝑅 be of Selections. Let the predicate 𝑠
be of 𝛾𝑎 (𝛼𝑎 (𝑅)). Then 𝑠 ∈ {𝛾𝑑 (𝑎) | 𝑎 ∈ {𝛼𝑑 (𝑟 ) | 𝑟 ∈ 𝑅}}. Thus, 𝑠 ∈ {𝛾𝑑 (𝛼𝑑 (𝑟 )) | 𝑟 ∈ 𝑅}. Since
the inequality 𝑟 𝑑# 𝛾𝑑 (𝛼𝑑 (𝑟 )) is true, we get that there is an 𝑟 in 𝑅 more precise than 𝑠, thus the
inequality 𝑅 𝑎# 𝛾𝑎 (𝛼𝑎 (𝑅)) holds.
   Moving on with the second inequality, let 𝐴 be of Selections # . Let the abstract predicate 𝑎 be of
𝐴. We have 𝛼𝑎 (𝛾𝑎 (𝐴)) = {𝛼𝑑 (𝑟 ) | 𝑟 ∈ {𝛾𝑑 (𝑎) | 𝑎 ∈ 𝐴}}. Thus, 𝛼𝑑 (𝛾𝑑 (𝑎)) is in 𝛼𝑎 (𝛾𝑎 (𝐴)). Since
we know that the inequality 𝛼𝑑 (𝛾𝑑 (𝑎)) 𝑑# 𝑎 holds, we get that the inequality 𝛼𝑎 (𝛾𝑎 (𝐴)) 𝑎# 𝐴 is
true.                                                                                                 

   Lemma A.22. The pair (𝛼𝑑 , 𝛾𝑑 ) is a Galois insertion, i.e. the following equation holds for any 𝑎 of
Predicates # : 𝛼𝑑 (𝛾𝑑 (𝑎)) = 𝑎.
   The pair (𝛼𝑎 , 𝛾𝑎 ) also is a Galois insertion, i.e. the following equation holds true for any 𝐴 of
Selections # : 𝛼𝑎 (𝛾𝑎 (𝐴)) = 𝐴.
   Proof. We start with the ﬁrst equality. Since we know the inequality 𝛼𝑑 (𝛾𝑑 (𝑎)) 𝑑# 𝑎 holds, it
is suﬃcient to show that the inequality 𝑎 𝑑# 𝛼𝑑 (𝛾𝑑 (𝑎)) is true because the relation 𝑑# is antisym-
metric. So let 𝑎 be of Predicates # . If 𝑎 = fail, then 𝛼𝑑 (𝛾𝑑 (𝑎)) is also fail. If 𝑎 is not fail, then let 𝑣 be
any variable of Vars. Then
                              𝑎(𝑣) ⊆ ∪𝑝 ∈States∧𝑝 (𝑣) ⊆𝑎 (𝑣) 𝑝 (𝑣)
                                    ⊆ ∪𝑝 ∈ {𝑝 ′ ∈States|∀𝑣′ ∈Vars:𝑝 ′ (𝑣′ ) ⊆𝑎 (𝑣′ ) } 𝑝 (𝑣)
                                     = 𝛼𝑑 (𝛾𝑑 (𝑎))
The second inclusion holds true because of the abundance of available states. Therefore, the in-
equality 𝑎 𝑑# 𝛼𝑑 (𝛾𝑑 (𝑎)) holds. That means 𝑎 = 𝛼𝑑 (𝛾𝑑 (𝑎)) is true.

                                                           40
Realizability in Semantics-Guided Synthesis Done Eagerly


  Because the relation on abstract angels is not antisymmetric, we show equality directly:
                                 𝛼𝑎 (𝛾𝑎 (𝐴)) = {𝛼𝑑 (𝑟 ) | 𝑟 ∈ {𝛾𝑑 (𝑎) | 𝑎 ∈ 𝐴}}
                                             = {𝛼𝑑 (𝛾𝑑 ) | 𝑎 ∈ 𝐴}
                                             = {𝑎 | 𝑎 ∈ 𝐴}
                                             =𝐴 .
                                                                                                     

  Definition 8. Meyer and Wolﬀ also provide an interpretation of commands that either maps to
another state or to their notation of failing: ⊤.
                                      (
                              #         fail       , 𝑎 = fail ∨ ÈcomÉ𝑡 (𝑎) = ⊤
                        ÈcomÉ (𝑎) =
                                        ÈcomÉ𝑡 (𝑎) , else

  Lemma A.23. The abstract interpretation of commands ÈcomÉ# is a safe abstraction for ÈcomÉ, i.e.
the following equation holds:
                                       ÈcomÉ# (𝑎) = 𝛼𝑑 (ÈcomÉ(𝛾𝑑 (𝑎)))
   Proof. The original interpretation of com in Meyer and Wolﬀ’s work is monotonic. Thus, ÈcomÉ#
is monotonic. We show equality by showing 𝑑 in both ways. By antisymmetry, equality follows.
   We start with ÈcomÉ# (𝑎) 𝑑# 𝛼𝑑 (ÈcomÉ(𝛾𝑑 (𝑎))): If the right side is fail we are done. Otherwise,
see that 𝑎 ∈ 𝛾𝑑 (𝑎). Thus, ÈcomÉ# (𝑎) ∈ ÈcomÉ(𝛾𝑑 (𝑎)). Let 𝑣 be a variable of Vars. Then ÈcomÉ# (𝑎) (𝑣)
is a subset of 𝛼𝑑 (ÈcomÉ(𝛾𝑑 (𝑎))) (𝑣). Therefore, the inequality ÈcomÉ# (𝑎) 𝑑# 𝛼𝑑 (ÈcomÉ(𝛾𝑑 (𝑎)))
holds.
   We proceed with the other direction: Again, if the left side is fail we are done. Otherwise, see that
for all 𝑞 of 𝛾𝑑 (𝑎), 𝑞 𝑑# 𝑎 holds. Now, let 𝑏 be an element of ÈcomÉ(𝛾𝑑 (𝑎)). Then, 𝑏 𝑑# ÈcomÉ# (𝑎)
holds because the original interpretation of commands is monotonic. Thus, for any variable 𝑣 of
Vars, we have 𝑏 (𝑣) ⊆ ÈcomÉ# (𝑎) (𝑣). Therefore, 𝛼𝑑 (ÈcomÉ(𝛾𝑑 (𝑎))) (𝑣) is a subset of ÈcomÉ# (𝑎) (𝑣).
So, the inequality holds. This concludes the proof.                                                   

  Lemma A.24. The following inequality holds:
                                     𝛼𝑎 (sp(𝛾𝑎 (𝐴), com)) 𝑎# sp# (𝐴, com)
  Proof.
                            𝛼𝑎 (sp(𝛾𝑎 (𝐴), com)) = {𝛼𝑑 (ÈcomÉ(𝑟 )) | 𝑟 ∈ 𝛾𝑎 (𝐴)}
                                                   = {𝛼𝑑 (ÈcomÉ(𝛾𝑑 (𝑎))) | 𝑎 ∈ 𝐴}
                                                   = {ÈcomÉ# (𝑎) | 𝑎 ∈ 𝐴}
                                                   = sp# (𝐴, com)

The inequality holds because 𝑎# is reﬂexive.                                                        

  Lemma A.25. The following equations hold:
                                         𝛼𝑎 (𝑅 ∪ 𝑆) = 𝛼𝑎 (𝑅) ∪ 𝛼𝑎 (𝑆)

                                         𝛾𝑎 (𝐴 ∪ 𝐵) = 𝛾𝑎 (𝐴) ∪ 𝛾𝑎 (𝐵) .

                                                           41
                                                                Roland Meyer, Jakob Tepe, and Sebastian Wolﬀ


  Proof. We start with the ﬁrst equation.

                          𝛼𝑎 (𝑅 ∪ 𝑆) = {𝛼𝑑 (𝑟 ) | 𝑟 ∈ 𝑅 ∪ 𝑆 }
                                     = {𝛼𝑑 (𝑟 ) | 𝑟 ∈ 𝑅} ∪ {𝛼𝑑 (𝑠) | 𝑠 ∈ 𝑆 }∪
                                     = 𝛼𝑎 (𝑅) ∪ 𝛼𝑎 (𝑆)

The proof for the second equation is analogous.                                                           

  Lemma A.26. The following equation holds

                          sp# (𝐴, com) 𝑎# 𝐵 =⇒ sp(𝛾𝑎 (𝐴), com) 𝑎 𝛾𝑎 (𝐵)

  Proof. Because the abstract strongest post is a safe abstraction, we have

                             𝛼𝑎 (sp(𝛾𝑎 (𝐴), com)) 𝑎# sp# (𝐴, com) 𝑎# 𝐵 .

Because we have a Galois connection, the following inequality holds:

                            sp(𝛾𝑎 (𝐴), com) 𝑎 𝛾𝑎 (𝛼𝑎 (sp(𝛾𝑎 (𝐴), com))) .

Applying the monotonicity of drv we get the following two inequalities:

                                 sp(𝛾𝑎 (𝐴), com) 𝑎𝛾𝑎 (sp# (𝐴, com))
                                 sp(𝛾𝑎 (𝐴), com) 𝑎𝛾𝑎 (𝐵)

                                                                                                          

Proof of Theorem B.1
   We prove the theorem by induction over the structure of sketch.
   Base Case: If sketch = com, then we know the inequality sp# (𝐴, com) 𝑎# 𝐵 is true. This then
implies that the inequality sp(𝛾𝑎 (𝐴), com) 𝑎 𝛾𝑎 (𝐵) holds. Therefore, all veriﬁcation conditions of
vc(h𝛾𝑎 (𝐴)icomh𝛾𝑎 (𝐵)i) are valid. Thus, we can show the realizability triple ⊢𝑎 h𝛾𝑎 (𝐴)icomh𝛾𝑎 (𝐵)i.
   Induction Step: If the sketch sketch = sketch1 ; sketch2 , we know that the veriﬁcation condi-
tions of the functions vc # (h𝐴isketch1 hsp# (𝐴, sketch1 )i) and vc # (hsp# (sketch1, 𝐴)isketch2 h𝐵i)
hold. Applying the induction hypothesis, we get that ⊢𝑎 h𝛾𝑎 (𝐴)isketch1 h𝛾𝑎 (sp# (𝐴, sketch1 ))i
and ⊢𝑎 h𝛾𝑎 (sp# (𝐴, sketch1 ))isketch2 h𝛾𝑎 (𝐵)i are valid. Using rule (SEQ), we prove the realizability
triple ⊢𝑎 h𝛾𝑎 (𝐴)isketch1 ; sketch2 h𝛾𝑎 (𝐵)i.
   The other rules are also analogous to the original proof.                                          

Proof of Theorem B.2
   By completeness of Hoare logic, we get ⊢𝑑 {𝛾𝑑 (𝑎)}prog{𝛾𝑑 (𝑏)}. Since the rules are the Same as
in Meyer and Wolﬀ’s type system, we get ⊢𝑡 h𝛾𝑑 (𝑎)iprogh𝛾𝑑 (𝑏)i.                                

B DETAILS ON THE APPLICATION
B.1 Background on Safe Memory Reclamation
Our goal is to synthesize code that makes a lock-free data structure memory safe. We recall the
basics of safe memory reclamation and outline the approach from [26, 27, 47] to verify that a lock-
free data structure properly protects its memory using a safe memory reclamation algorithm. We
also demonstrate the approach on an example.

                                                  42
Realizability in Semantics-Guided Synthesis Done Eagerly


B.2 Background
When writing programs in languages such as C++, memory management is manual. This is op-
posed to other programming languages, such as Java, which provide Garbage Collection (GC) for
automatic memory management. Not having GC at hand proves challenging in implementing (and
verifying) concurrent, especially lock-free data structures due to use-after-free errors and the ABA
problem. For assistance, programmers can resort to Safe Memory Reclamation (SMR) algorithms,
e.g. Hazard Pointers (HP) [29]. Instead of freeing memory directly, these algorithms provide a re-
tire function that delays freeing memory until it is safe to do so. In order for the SMR algorithm to
know when freeing memory is allowed, the programmer has to call SMR speciﬁc functions. With
HP, the programmer has to call a protect function on a pointer they want to access. Afterwards,
however, the programmer has to check if the protection was successful. In the next chapter, we
automatically synthesize the code for such calls and checks.
   In [26, 27, 47], Meyer and Wolﬀ proposed a type-based approach to automatically verify lock-free
data structures that use SMR algorithms for memory reclamation. We base our synthesis upon their
work. The idea is to abstract away the implementation details of the SMR and verify the program
with the help of a speciﬁcation, a so-called SMR automaton. The automata consist of states, and
subsets of these states form the types, also called guarantees, in their approach. The states capture
the eﬀect that the SMR algorithm has on a pointer. Every SMR automaton comes with at least three
guarantees. The local guarantee, L, signals that the pointer is thread local. The active guarantee, A,
signals that the pointer is published and was not yet retired. The safe guarantee, S, signals that the
pointer is protected by the SMR algorithm. Additionally, SMR automata may bring SMR speciﬁc
guarantees E𝐿 .
   Pointer dereferences are only allowed when the SMR automaton for the pointer is guaranteed
to be in a state described by L, A, or S.
   The type system tracks the guarantees each pointer has. It annotates the original program com-
mands, SMR commands, and invariant annotations that may have to be added to the code. The
invariant annotations provide information about the protection status of a pointer that the type
system can rely on, e.g. that a shared pointer is not retired at a certain program location. The
invariant annotations need to be veriﬁed separately. Importanty, this can be done assuming GC.
When the type check is successful and the invariant annotations can be discharged, the program
does not unsafely dereference memory and does not suﬀer from ABAs.

B.3 Example SMR Automaton: Hazard Pointer
We demonstrate the concept of SMR automata on the SMR algorithm Hazard Pointer. In Figure 12,
the SMR automaton O for Hazard Pointers is depicted. It consists of eight states, one of them ﬁnal.
The automaton speciﬁes illegal behavior. That means, when using HP, all transitions to the ﬁnal
state will not occur. The automaton takes two parameters: 𝑧𝑝 representing the pointer whose state
is tracked, and 𝑧𝑡 representing the thread whose perspective is taken. The automaton has two extra
guarantees: Einv and Eisu . In Figure 12, all guarantees are depicted by colored zones. A pointer is
safe to access when it possesses the guarantees A, L, or S, because all transitions for command free
lead to the fail state. Therefore, when a pointer is guaranteed to be in one of the states described
by the three guarantees, it cannot be freed. Thus, a dereference would be safe. Here, guarantee S
represents the protection by the SMR algorithm. Guarantee Einv describes the states the automaton
is guaranteed to be in when thread 𝑧𝑡 invokes a protection on pointer 𝑧𝑝 . When that call returns,
the automaton is guaranteed to be in the states described by Eisu . When thread 𝑧𝑡 protects another
pointer, or unprotects pointer 𝑧𝑝 , the aforementioned guarantees are lost. The transitions for free
and retire do not depend on the executing thread and can be interferences from other threads.

                                                           43
                                                                                Roland Meyer, Jakob Tepe, and Sebastian Wolﬀ



                                  Fig. 12. SMR automaton for HP, adapted from [47].
            in:protect(𝑡, 𝑝), 𝑡 = 𝑧𝑡 ∧ 𝑝 ≠ 𝑧𝑝                          F:= free(𝑝), 𝑝 = 𝑧𝑝
            in:unprotect(𝑡), 𝑡 = 𝑧𝑡                                    R:= in:retire(𝑡, 𝑝), 𝑝 = 𝑧𝑝



                   in:protect(𝑡, 𝑝),                 re:protect(𝑡),                                               Einv
                     𝑡 = 𝑧𝑡 ∧ 𝑝 = 𝑧 𝑝                    𝑡 = 𝑧𝑡
          𝑞1                                𝑞3                           𝑞5                          𝑞6
                                                                                        R
                                                                                                                  Eisu
      F        R                        F        R                         F                 R        F
                   in:protect(𝑡, 𝑝),                 re:protect(𝑡),                                                S
                     𝑡 = 𝑧𝑡 ∧ 𝑝 = 𝑧 𝑝                    𝑡 = 𝑧𝑡                         F
          𝑞0                                𝑞2                           𝑞4                          𝑞𝑓
                                 F                            F                                                   A, L


            in:protect(𝑡, 𝑝), 𝑡 = 𝑧𝑡 ∧ 𝑝 ≠ 𝑧𝑝
            in:unprotect(𝑡), 𝑡 = 𝑧𝑡


The guarantee A is not closed under interferences. Local pointers cannot experience interference,
thus interference can be disregarded for guarantee L. When using HP, after issuing a protection,
it must be checked if the protection was successful. This is represented in the automaton by the
fact that the guarantees Eisu and S are not the same. After returning from the protection call, the
automaton could be in state 𝑞 5 where it is not safe yet. The strategy to protect a pointer therefore
is to ﬁrst call the method protect and then compare it to a pointer that possesses the guarantee
A. If both are equal, they must be in the state 𝑞 4 (𝑞 𝑓 is never reached) and thus both automatically
get the guarantee S and are thereby safe to access.

B.4       Example Type Check: Treiber’s Stack pop
                                                                   We demonstrate the type check
                                                                from [27, 47]. Figure 13 shows an
 Fig. 13. Excerpt of pop in Treiber’s stack demonstrating Meyer excerpt of the pop method from
 and Wolﬀ’s type system using Hazard Pointers (simplified).     Treiber’s stack using Hazard Point-
                                                                ers as the SMR algorithm. There are
 1 top : O, TOS : O               11     top : Eisu , TOS : A   two pointer variables: the local vari-
 2 top = TOS ;                    12     assume ( top == TOS ); able top and the shared variable TOS.
 3 top : O, TOS : O               13     (top : Eisu ∧ A,       In the beginning, both pointers pos-
 4 in : protect ( top );          14      TOS : A ∧ Eisu )      sess no guarantees. First, the cur-
 5 top : Einv , TOS : O           15     (top : Eisu ∧ A ∧ S,   rent value of the shared variable is
 6 re : protect ();               16      TOS : A ∧ Eisu ∧ S)
                                                                read into top. Afterwards a hazard
 7 top : Eisu , TOS : O           17 }
                                                                pointer protection for top is called.
 8 atomic {                       18 top : Eisu ∧ S, TOS : O
 9     top : Eisu , TOS : O       19 d = top . data ;
                                                                It is invoked in Line 4 and returns
10     @ inv active ( TOS );      20 top : Eisu ∧ S, TOS : O
                                                                in Line 6. After a protection, one has
                                                                to check if it was successful. This re-
                                                                quires two steps. First, we signal the
                                                                type system that the shared variable
 TOS is not yet retired through the invariant annotation active(TOS). Afterwards, we compare the
 previously read value stored in the variable top with the current value of TOS. If both variables
 point to the same address, we combine the information we have on each variable. Therefore, both

                                                                  44
Realizability in Semantics-Guided Synthesis Done Eagerly


pointers now have the guarantees Eisu and A and by inference also S. Leaving the atomic block,
other threads are able to interfere again, so the active guarantee is lost for top. Because the pointer
TOS is shared and other threads can manipulate it in any way, it loses all its guarantees. However,
the pointer top can now be safely dereferenced in Line 19. We use the theory presented in this
paper and leverage the type system discussed above to automatically synthesize the extra code
needed to pass the type check, i.e. Lines 4, 6, and 10.

B.5    Assertion Language
Our assertion language for predicates is Predicates # = (Vars → P (O)) ∪ {fail}, and we also call the
elements in this domain abstract predicates. We annotate our development by # to indicate that we
work with abstract predicates. Functions deﬁned on the abstract domain that are annotated with
a # symbol, e.g. vc # . As an abstraction function we have 𝛼𝑑 and 𝛼𝑎 for predicates and selections,
respectively. Abstract selections are a set of abstract predicates. Similarly, the concretisation func-
tions are called 𝛾𝑑 and 𝛾𝑎 . Since it is deterministic, the original interpretation of commands ÈcomÉ𝑡
serves as a safe abstract interpretation of ÈcomÉ when the semantics for fail are added. Thus, there
is no need to concretize to the non abstract domain. We use the abstract version of veriﬁcation
conditions to proof realizability triples:
  Theorem B.1. |= vc # (h𝐴istmth𝐵i) implies ⊢𝑎 h𝛾𝑎 (𝐴)istmt′ h𝛾𝑎 (𝐵)i .
 Proofs over programs that start and end in singletons can be replicated in the type system of
Meyer and Wolﬀ of which a successful type check is denoted by ⊢𝑡 :
  Theorem B.2. |=𝑑 {𝛾𝑑 (𝑎)}prog{𝛾𝑑 (𝑏)} implies ⊢𝑡 h𝑎iprogh𝑏i .

C EXAMPLE: POP METHOD IN TREIBER’S STACK
We demonstrate our synthesis approach on the pop method of Treiber’s Stack. First, we insert
nonterminals that can resolve to calls to the SMR algorithm and invariant annotations into the
program code. Then, using veriﬁcation conditions, it is shown that these nonterminals are suﬃ-
cient for deriving a memory safe program that passes Meyer and Wolﬀ’s type check. Afterwards,
using the synthesis function, we derive a memory safe program.
   In Figure 14, the pop method of Treiber’s stack is depicted. Therein, we already inserted the
nonterminal AC. Insertions that will resolve to skip are marked in red. Insertions that will resolve
to commands other than skip are marked in purple with the commands they will resolve to in
gray right beside them. The atomic block in Lines 9 to 15 serves as an atomicity abstraction for
assume(top = TOS). The assumption is required to check if a protection was successful. Without
diving into details, the atomicity abstraction is required in Meyer and Wolﬀ’s type system because
this assumption is at risk of a harmless ABA. A type check does not pass on a harmless ABA. (This
is a detail we left out in the overview in Appendix B.2.) The atomicity abstraction circumvents this
problem.
   In the type system, dereferences and checks for equality can only be performed on pointers
that are safe to access, i.e. pointers that possess the active, local, or safe guarantee. Since the next
pointer is never accessed or compared, it does not need any protection. We therefore omit it in the
following. As mentioned before, we assume the shared pointer TOS to always be active, therefore a
protection is not needed because having the active guarantee A is suﬃcient for safe dereferences
and comparisons. However, signaling the type system that the pointer is indeed active is still
required and is done using invariant annotations. Observe that TOS needs to be active at least in
Line 19 as it is compared to top there. The pointer top needs to be protected at multiple locations. It
is accessed and compared to another pointer in Lines 16, 19 and 28. Knowing which pointers need

                                                           45
                                                                  Roland Meyer, Jakob Tepe, and Sebastian Wolﬀ



Fig. 14. Treiber’s Stack Pop with inserted nonterminals. Red nonterminals resolve to skip. Purple nontermi-
nals resolve to the gray code beside them.

1 BEGIN LOOP {                                        19         (( assume ( CAS ( TOS , top , next ));
2 top := TOS ; AC ;                                   20             AC ;
3 (( assume ( top == NULL ); AC ;                     21             flag := true ; AC ;
4     result := EMPTY ; AC ; )                        22          )
5 +                                                   23             +
6 (                                                   24          ( flag := false ; AC ; ))
7     assume ( top != NULL ); AC ;                    25        }
8     ((                                              26        AC ;
9        atomic {                                     27        (( assume ( flag == true ); AC ;
10          AC ; p∼ @ inv active ( TOS );             28           result := top . data ; AC ;)
11          top := TOS ;                              29        +
12          AC ; p∼ in : protect ( top );             30        ( assume ( flag == false ); AC ;
13                      re : protect ();              31          skip ; AC ; ))
14          assume ( top != NULL ); AC ;              32      ))
15       }                                            33      +
16       AC ; next := top . next ; AC ;               34      ( skip ; AC ; )
17       atomic {                                     35 ))
18          AC ; p∼ @ inv active ( TOS );             36 }* END LOOP




                               Fig. 15. Insertions for HP in Treiber’s Stack.
1 AC ::= skip ;     |
2 atomic { @ inv active ( TOS );}     |
3 ( in : protect ( top ); re : protect ( top );)



to be protected, we restrict nonterminal to the deﬁnition depicted in Figure 15. (This optimization
is not required.)
   We call the resulting program sketch sketch. Using veriﬁcation conditions, the realizability
triple ⊢𝑎 h𝛾𝑑 ((TOS : O, top : O))isketchh𝛾𝑑 ((TOS : O, top : O))i is proven. In order to generate
veriﬁcation conditions, the loop of sketch needs to be annotated with a loop invariant. We choose
the invariant 𝐼 = {(TOS : O, top : O)}. In total, the veriﬁcation conditions function generates 27
unique comparisons. The result is that every comparison holds. Therefore, the above realizability
triple is true. Inserting the selections used for generating the veriﬁcation conditions into the pro-
gram yields a proof outline po with sketch(po) = sketch. Having shown that there is a way to
concretize this program sketch, we now use the synthesis algorithm to eliminate the nontermi-
nals. Thus, we call the synthesis function with the predicate (TOS : O, top : O) as the target for
condition. In Lines 10, 12 and 18 the nonterminals resolve to commands other than skip. In the
following, we discuss the invocations of the synthesis function where the nonterminal does not
resolve to skip. In Equation (7), the active invariant annotation for TOS is chosen. This insertion
can be seen in Line 10. Here, executing the active invariant annotation on the ﬁrst and second
predicate in the pre condition results in the ﬁrst and second predicate of the post condition, re-
spectively. The third predicate of the post condition can be reached from both of the predicates in
the pre condition. From the ﬁrst predicate, a protection to top needs to be issued. From the second
predicate, a skip is suﬃcient. The last predicate of the post condition is reached through executing

                                                    46
Realizability in Semantics-Guided Synthesis Done Eagerly



                                  Fig. 16. Recursive calls of decision function

         syn(h𝛾𝑎 ({(TOS : O, top : O), (TOS : O, top : Einv ∧ Eisu )})iACh𝛾𝑎 ({(TOS : A, top : O),
                     (TOS : A, top : Einv ∧ Eisu ), (TOS : O, top : Einv ∧ Eisu ), (TOS : O, top : O)})i,
                                                                                                            (7)
                                             𝛾𝑑 ((TOS : A, top : O)))
                                                      = (𝛾𝑑 ((TOS : O, top : O)), @inv active(TOS);)
          syn(h𝛾𝑎 ({(TOS : O, top : O), (TOS : A, top : A)})iACh𝛾𝑎 ({(TOS : A, top : A),
                                            (TOS : A, top : Einv ∧ Eisu ∧ A ∧ S), (TOS : A, top : O),
                                                    (TOS : O, top : O), (TOS : O, top : Einv ∧ Eisu )})i,   (8)
                                   𝛾𝑑 ((TOS : A, top : Einv ∧ Eisu ∧ A ∧ S)))
                                       = ((TOS : A, top : A), (in:protect(top); re:protect();))
         syn(h𝛾𝑎 ({(TOS : O, top : Einv ∧ Eisu ∧ S), fail})iACh𝛾𝑎 ({(TOS : A, top : Einv ∧ Eisu ∧ S),
                                                               (TOS : O, top : Einv ∧ Eisu ∧ S), fail})i,
                                                                                                            (9)
                                      𝛾𝑑 ((TOS : A, top : Einv ∧ Eisu ∧ S)))
                                             = ((TOS : O, top : Einv ∧ Eisu ∧ S), @inv active(TOS);)


skip on the ﬁrst predicate of the pre condition. Thus, the ﬁrst, third and fourth predicates of the
post condition are reachable from the target pre condition. The ﬁrst predicate of the post condition
matches. Therefore, @inv active needs to be inserted and the ﬁrst predicate of the precondition
is returned. Next, in Equation (8), the protections for top are synthesized. The result is inserted in
Line 12. There are 5 predicates in the post condition of the nonterminal. The ﬁrst two predicates
are results of executing the nonterminal on the second predicate of the precondition. The ﬁrst
predicate of the postcondition stems from calling skip or @inv active(TOS). The second predi-
cate is the result of issuing the protection for top. The third, fourth and ﬁfth predicate are results
of executing the nonterminal on the ﬁrst predicates of the pre condition. The third predicate is
the product of inserting the protection for top. The fourth predicate comes from a skip. The last
predicate is the result of calling @inv active(TOS). The second predicate of the post condition
matches target post condition. Therefore, the protections for top must be synthesized here and
the second predicate of the precondition is returned.
   Lastly, in Equation (9), the active annotation in Line 18 before the compare and swap is synthe-
sized. There are two predicates in the pre condition, one of which is fail. Executing the nonterminal
on fail leads to fail in the post condition. Using the invariant annotation on the ﬁrst predicate of
the pre condition yields the ﬁrst predicate of the post condition. Inserting skip or a protection
to top leads to the second predicate. The ﬁrst predicate of the post condition matches the target
post condition, thus @inv active(TOS) is inserted and the ﬁrst predicate from the precondition
is returned.
   We call the version of Treiber’s stack with the resolved nonterminals from Figure 14 prog. We
know that the Hoare triple |=𝑑 {𝛾𝑑 ((TOS : O, top : O))}prog{𝛾𝑑 ((TOS : O, top : O))} holds
due to Theorem 6.1. Applying Theorem B.2, we conclude that the resulting program type checks:
⊢𝑡 h(TOS : O, top : O)iprogh(TOS : O, top : O)i is true. That means, we successfully synthesized
a program prog that passes Meyer and Wolﬀ’s type check and therefore is memory safe (if the
invariant annotations can be discharged).




                                                           47
