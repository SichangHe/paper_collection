                                                                                                                                                                   1

                                         Software Model-Checking as Cyclic-Proof Search

                                         TAKESHI TSUKADA, Chiba University, Japan
                                         HIROSHI UNNO, University of Tsukuba, Japan and RIKEN AIP, Japan
arXiv:2111.05617v1 [cs.PL] 10 Nov 2021




                                         This paper shows that a variety of software model-checking algorithms can be seen as proof-search strategies
                                         for a non-standard proof system, known as a cyclic proof system. Our use of the cyclic proof system as a
                                         logical foundation of software model checking enables us to compare different algorithms, to reconstruct
                                         well-known algorithms from a few simple principles, and to obtain soundness proofs of algorithms for free.
                                         Among others, we show the significance of a heuristics based on a notion that we call maximal conservativity;
                                         this explains the cores of important algorithms such as property-directed reachability (PDR) and reveals a
                                         surprising connection to an efficient solver of games over infinite graphs that was not regarded as a kind of
                                         PDR.

                                         1   INTRODUCTION
                                         Software model-checkers [Beyer et al. 2018; Jhala and Majumdar 2009] are tools for verifying systems
                                         described by programs. They have been successfully applied to industrial software systems, in
                                         particular OS device drivers [Ball et al. 2004; Ball and Rajamani 2002; Khoroshilov et al. 2010].
                                         To address the so-called “state explosion problem” in model checking real-world programs, the
                                         past decades have witnessed a significant development of state-space abstraction and refinement
                                         techniques including predicate abstraction [Ball et al. 2001; Graf and Saïdi 1997], CounterExample-
                                         Guided Abstraction Refinement (CEGAR) [Clarke et al. 2003], lazy abstraction [Beyer and Wendler
                                         2012; Henzinger et al. 2004, 2002; McMillan 2006], and Property Directed Reachability (PDR) [Beyer
                                         and Dangl 2020; Birgmeier et al. 2014; Bradley 2011; Cimatti and Griggio 2012; Cimatti et al. 2014;
                                         Een et al. 2011; Hoder and Bjørner 2012; Komuravelli et al. 2014, 2013; Vizel and Gurfinkel 2014].
                                            Software model-checkers can be classified by their target programming language and target
                                         properties. This paper mainly focuses on the safety verification problem for while languages.
                                            The safety of a given program can be witnessed by an over-approximation of reachable states
                                         that does not intersect with the set of bad states. Such a desirable over-approximation can be
                                         characterized by the following three conditions: (1) it contains all initial states, (2) it is closed
                                         under the transition relation, and (3) it does not contain any bad state. Once a candidate of an
                                         approximation is given, it is relatively easy to check whether it satisfies the above conditions.
                                         Hence the most challenging part of the software model-checking is to find an appropriate over-
                                         approximation.
                                            A modern software model checker guesses a candidate of over-approximation and iteratively
                                         refines it until a desirable one is found. Many papers were devoted to provide efficient procedures,
                                         including the above mentioned techniques for abstraction and refinement, to find an appropri-
                                         ate over-approximation, which vary in the structure of candidates and the candidate update
                                         method [Ball et al. 2001; Birgmeier et al. 2014; Cimatti and Griggio 2012; Cimatti et al. 2014;
                                         Henzinger et al. 2004, 2002; Hoder and Bjørner 2012; Komuravelli et al. 2014, 2013; McMillan 2006].
                                            This paper aims to provide a unified account for a variety of approaches to software model-
                                         checking in terms of logic, or more precisely, proof search. Since the notion of reachable states is
                                         an inductive notion, we need a proof system with (co-)induction.

                                         Authors’ addresses: Takeshi Tsukada, Chiba University, Japan, tsukada@math.s.chiba-u.ac.jp; Hiroshi Unno, University of
                                         Tsukuba, Japan , RIKEN AIP, Japan, uhiro@cs.tsukuba.ac.jp.

                                         2018. 2475-1421/2018/1-ART1 $15.00
                                         https://doi.org/


                                                                          Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:2                                                                                 Takeshi Tsukada and Hiroshi Unno




Fig. 1. Correspondence between an intermediate state of McMillan’s Impact and an intermediate state of
cyclic-proof search. Figures (a-c) originate from [McMillan 2006]. (a) An example of a program. (b) The control
flow graph of (a). The assertion is that 𝐿 = 0 at location 2. (c) An intermediate state of Impact. Nodes with
the dotted line are needed to be expanded to confirm the safety. (d) An intermediate state of cyclic-proof
search. The sequents with ? mark are open, which are not yet proved. For each location 𝑖, 𝜈𝑃𝑖 is the formula
corresponding to it; a sequent 𝜑 ⊢ 𝜈𝑃𝑖 corresponds to the node in (c) of location 𝑖 labeled with the formula 𝜑.


   A famous proof rules for reasoning about (co-)induction are based on pre- and/or post-fixed points
(see, e.g., [Martin-Löf 1971]). However, they are not appropriate for the purpose of interpreting
various abstraction and refinement techniques as proof-search strategies, because these proof
rules are applicable only after appropriate pre- or post-fixed-points are found. Therefore the main
process of software model-checking, trial-and-error search of appropriate over-approximation, has
no logical interpretation.
   We show that well-known procedures can naturally be seen as proof-search strategies of a non-
standard proof system, known as a cyclic proof system [Brotherston and Simpson 2011; Sprenger
and Dam 2003]. Figure 1 illustrates a correspondence between McMillan’s lazy abstraction with
interpolants [McMillan 2006] and cyclic proof search. We do not explain the details here, which are
the topic of Section 4, but we believe that the correspondence should be intuitively understandable.
   Although the connection is somewhat expected, establishing a precise connection is not trivial.
This is because the most natural logical expression of the software model-checking, based on least
fixed-point, does not fit to practical algorithms (see Section 5). Our key observation to establish a
tight connection between cyclic proof search and software model-checking is that we use the dual
notion, safe states.
   Our framework covers other important procedures including variants of PDR [Cimatti and Griggio
2012; Hoder and Bjørner 2012], where we identify the significance of an underlying principle we
call maximal conservativity of refinement. It turns out that the principle has also been adopted
implicitly by highly efficient refinement algorithms, partially witnessing the usefulness of the
principle in practice: one based on Craig interpolation [Craig 1957] for a variant of PDR [Vizel and
Gurfinkel 2014] and one based on quantified satisfaction [Farzan and Kincaid 2016] for a solver of
games over infinite graphs [Farzan and Kincaid 2017]. To the best of our knowledge, we are the
first to apply the maximal conservativity, as one of the fundamental principles of software model
checking, to formalize and compare variants of PDR and McMillan’s lazy abstraction within a
unified framework. This allowed us to construct a counterexample for the refutational completeness
of existing PDR variants [Hoder and Bjørner 2012; Komuravelli et al. 2014, 2016] and to obtain the
first PDR variant with refutational completeness.
   The logical foundation of software model checking based on cyclic proof search has the following
advantages.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Software Model-Checking as Cyclic-Proof Search                                                                     1:3


      • It allows us to compare different approaches to software model checking. Different approaches
        are different proof-search strategies for the same goal sequent in the same proof system. It is
        even possible to compare a software model-checking algorithm with algorithms for other
        problems. As an example, we show that PDR shares the same heuristics based on the principle
        of maximal conservativity as the solver for infinite games [Farzan and Kincaid 2017].
      • It allows us to reconstruct well-known algorithms from a few simple principles. This is
        because a proof system is demanding: use of a proof rule requires us to ensure side conditions.
        For example, an internal state of PDR is a sequence of formulas that satisfies certain conditions;
        these conditions indeed coincide with the side conditions of proof rules.
      • We obtain soundness of model-checking algorithms for free. It is just a consequence of
        soundness of the proof system.
Note that the logical foundation goes beyond related ones [Bjørner et al. 2015; Flanagan 2004;
Podelski and Rybalchenko 2007] based on constraint logic programming (CLP): they use CLP to
capture mainly the process of modeling verification problems, while we use a cyclic-proof system
to capture both processes of modeling and solving verification problems; we expect that the logical
foundation based on cyclic proofs would also be convenient for developing new algorithms and
heuristics. We shall briefly discuss some possible directions, though the detailed studies are left for
future work. Furthermore, we expect that the logical foundation paves the way for transferring
abstraction and refinement techniques studied in the software model checking community to cyclic
proof-search, in particular, for finding necessary cut-formulas, which is considered essential for the
success of proof-search because cyclic proof systems usually do not admit cut-elimination [Kimura
et al. 2020; Masuoka and Tatsuta 2021].

   Organization of this paper. The rest of the paper is organized as follows. Section 2 briefly reviews
software model checking and two approaches: one is based on an over-approximation of reachable
states and the other is based on a cyclic proof system. Section 3.1 discusses what is an appropriate
goal sequent to establish the connection between cyclic proof search and software model-checking.
Sections 3.2–6 exemplify the generality of the logical foundation based on cyclic proofs, by pre-
senting proof-search strategies corresponding to well-known software model-checking techniques:
symbolic execution, bounded model checking, predicate abstraction, lazy abstraction, and PDR. We
discuss related work in Section 8 and conclude the paper with final remarks in Section 9.

2     BACKGROUND
2.1    Definition of Software Model-Checking
Recall that we have focused on verification of safety properties of while programs. A program
induces a transition system with finite control states and infinite data, and we are interested in
whether a bad state is reachable. For simplicity, we assume that the target program has exactly one
control state. It is not difficult to apply the ideas of the paper to programs with multiple but finite
control states, by introducing an auxiliary variable representing the program counter.
   A transition system consists of a domain D of infinite data and a subset1 𝜄 ⊆ D of initial states
and a transition relation 𝜏 ⊆ D × D; an assertion is given as a subset 𝛼 ⊆ D. A typical example of
D is Z𝑘 where 𝑘 is the number of variables in the program.
   A state 𝑥 ∈ D is reachable if there is a finite sequence 𝑥 0, 𝑥 1, . . . , 𝑥𝑛 (𝑛 ≥ 0) such that 𝜄 (𝑥 0 ) ∧
Ó𝑛
  𝑖=1 𝜏 (𝑥𝑖−1, 𝑥𝑖 ) ∧ 𝑥𝑛 = 𝑥 holds. The safety verification problem asks whether, given a while program
and an assertion, there is a reachable state that violates the assertion.

1 We shall identify a subset 𝐴 ⊆ 𝑋 with a predicate over 𝑋 given by 𝐴(𝑥) ⇔ (𝑥 ∈ 𝐴).



                                Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:4                                                                                       Takeshi Tsukada and Hiroshi Unno


2.2     Approach Based on Over-approximation of Reachable States
Unfortunately the set 𝑅 of reachable states is hard to compute, and modern model-checkers avoid
the exact computation of 𝑅 by using an equational characterization of 𝑅. The set 𝑅 of reachable
states satisfies the following condition:
                                       𝜄 (𝑦) ∨ (∃𝑥 .𝑅(𝑥) ∧ 𝜏 (𝑥, 𝑦)) ⇔ 𝑅(𝑦).                                                (1)
Actually this condition characterizes the set of reachable states: it is the least solution of Equation 1.
Defining a notion as the least solution of an equation in a certain class is called an inductive
definition. So 𝑅 is an inductively defined predicate.
   Thanks to the inductive definition of reachable states by Equation 1, it suffices to find any
solution 𝑅 of Equation 1, which is not necessarily least, such that 𝑅(𝑥) ⇒ 𝛼 (𝑥). If any solution 𝑅
of Equation 1 satisfies 𝑅(𝑥) ⇒ 𝛼 (𝑥), then obviously so does the least solution of Equation 1.
   The condition can be further relaxed. It is well-known that the least solution of Equation 1
coincides with the least solution of
                                        𝜄 (𝑦) ∨ (∃𝑥 .𝑅(𝑥) ∧ 𝜏 (𝑥, 𝑦)) ⇒ 𝑅(𝑦).                                               (2)
Theoretically the least solution can be computed by iteratively applying the predicate transformer
F [𝜑] (𝑦) := 𝜄 (𝑦) ∨ (∃𝑥 .𝜑 (𝑥) ∧ 𝜏 (𝑥, 𝑦)) to the empty set.

2.3     Approach Based on a Proof System for Inductive Predicates
The previous subsection reduces the safety verification problem to the entailment problem 𝑅(𝑥) ⇒
𝛼 (𝑥), where 𝑅 is an inductively defined predicate. Hence a proof system for inductively defined
predicates would serve as a basis for software model-checking.
   Let us first fix notations. Assume an equation 𝑃 (𝑥) ⇔ 𝛿 [𝑃] (𝑥), where 𝑃 occurs only positively
in 𝛿 [𝑃] (i.e. every occurrence of 𝑃 is under an even number of negation operators). Here 𝛿 is an
unary predicate that defines 𝑃, which itself may depend on 𝑃; this dependency is written explicitly
as 𝛿 [𝑃]. We write the least solution of this equation as (𝜇𝑃) (𝑥),2 where 𝜇 is the standard symbol
for the least fixed-points.
   This paper focuses on a cyclic proof system [Brotherston and Simpson 2011; Sprenger and Dam
2003]. It is an extension of the sequent calculus for the first-order classical logic, with two additional
mechanisms to deal with inductively defined predicates. The first one is the additional proof rules
for inductively defined predicates:
                         𝛿 [(𝜇𝑃)] (𝑥) ⊢ 𝜑 (𝑥)                         𝜑 (𝑥) ⊢ 𝛿 [(𝜇𝑃)] (𝑥)
                                              (𝜇-L)                                        (𝜇-R)
                           (𝜇𝑃) (𝑥) ⊢ 𝜑 (𝑥)                             𝜑 (𝑥) ⊢ (𝜇𝑃) (𝑥)
These rules just expand the definition of the predicate 𝜇𝑃. For example, for the reachability predicate
𝜇𝑅 defined by Equation 1, we have
                                   𝜄 (𝑥) ∨ (∃𝑦.(𝜇𝑅) (𝑦) ∧ 𝜏 (𝑦, 𝑥)) ⊢ 𝜑 (𝑥)
                                                                            (𝜇-L).
                                              (𝜇𝑅) (𝑥) ⊢ 𝜑 (𝑥)
A characteristic feature of the cyclic proof system is that a proof is not a tree but can have cycles;
instead of proving the sequent of a leaf node, one can make a link to its ancestor with the same
sequent.
  A pre-proof is a proof-like tree whose leaves are either instances of the axiom rule or equipped
with links to their ancestors. Figure 2 shows two examples of pre-proofs. Intuitively a link corre-
sponds to a use of induction; for example, the proof of Figure 2(a) says that “we prove the sequent
2 To simplify the notation, the defining equation is implicit. By explicitly writing the defining equation, 𝜇𝑃 can be written as

𝜇𝑃 .𝜆𝑥 .𝛿 [𝑃 ] (𝑥).


Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Software Model-Checking as Cyclic-Proof Search                                                                     1:5




Fig. 2. Pre-proofs and the global trace condition. The preproof (a) satisfies the global trace condition, but the
preproof (b) does not. So (a) is a cyclic proof but (b) is not. The inductive predicate 𝑅 is defined by Equation 1.




(𝜇𝑅) (𝑥) ⊢ 𝜑 (𝑥) at the second line from the bottom by induction on 𝑥" and that “the leaf node
(𝜇𝑅) (𝑦) ⊢ 𝜑 (𝑥) follows from the induction hypothesis.”
   Not all pre-proofs are valid; for example, the proof in Figure 2(b) has an invalid conclusion.
Intuitively the invalidity is caused by a wrong use of the induction hypothesis. Recall that the
induction hypothesis is applicable to only smaller elements, i.e. when proving 𝑃 (𝑡), the induction
hypothesis tells us 𝑃 (𝑢) for 𝑢 < 𝑡 but not for 𝑢 ≥ 𝑡. So if one applies the induction hypothesis to an
element not smaller than 𝑡, it is a wrong proof. Figure 2(b) makes this kind of mistake.
   A pre-proof is valid if it uses the “induction hypotheses” appropriately. The appropriateness
in the context of cyclic proof systems is called the global trace condition. Because its definition is
rather complicated (see [Brotherston and Simpson 2011]), we do not formally define the global
trace condition. For pre-proofs appearing in this paper, the following condition is equivalent to the
global trace condition:
       If there is a link from a leaf 𝑙 to its ancestor 𝑛, (𝜇-L) rule is used in the path from 𝑛 to 𝑙.
Figure 2(a) satisfies the global trace condition in the above sense, but Figure 2(b) does not. A proof
is a pre-proof that satisfies the global trace condition.

  Example 2.1. Suppose that 𝜑 is a solution of Equation 1 such that 𝜑 (𝑥) ⇒ 𝛼 (𝑥). Then the cyclic
proof of Figure 2(a) shows the sequent corresponding to the safety of the program.              □

2.4 Goal-oriented proof search
This paper studies a connection between software model-checking and the proof-search problem
for a cyclic proof system, which asks to construct a proof of a given sequent. Proof search strategies
of this paper are goal-oriented, i.e. a proof is constructed in a bottom-up manner. So an intermediate
state is a proof-like structure in which some leaves are not yet proved. We call such an unproved
leaf sequent an open sequent and a proof-like structure with open leaves a partial proof.
   We fix a signature and a theory and assume that 𝜄, 𝜏 and 𝛼 are formulas of the signature. We
assume an external solver of the theory. We use |= instead of ⊢ for the provability of a sequent
handled by the external solver. For example, if a proof rule contains ∃𝑥 .𝜄 (𝑥) ∧ 𝜏 (𝑥, 𝑦) |= 𝛼 (𝑦) as a
premise, its validity should be checked by the external solver; our proof search strategies do not
give any details of how to prove or disprove such sequents. We assume that a partial proof has no
open sequent of the form 𝜑 |= 𝜓 .
   A partial proof is valid if all |=-sequents in it are valid. We sometimes think of an invalid partial
proof, which contains a false |=-sequent. A partial proof is either valid or invalid.

                                Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:6                                                                                 Takeshi Tsukada and Hiroshi Unno


3     BASIC NOTIONS OF SOFTWARE MODEL-CHECKING
3.1    The Goal Sequent
As the first step to establish a connection between software model-checking and cyclic-proof search,
this section describes the goal sequent corresponding to software model-checking. It might seem
natural to use the sequent
                                                                                  
                   (𝜇𝑅) (𝑦) ⊢ 𝛼 (𝑦)     where 𝑅(𝑦) ⇔ 𝜄 (𝑦) ∨ (∃𝑥 .𝑅(𝑥) ∧ 𝜏 (𝑥, 𝑦)) ,
which directly expresses that all reachable states satisfy the assertion 𝛼. Unfortunately proof search
for this sequent does not precisely correspond to existing procedures.
   The key observation of this paper is that we should employ another logically-equivalent sequent,
which uses the dual notion. We explain the dual notion from the view point of program verification,
introducing the notion of safe states. We also briefly explain a proof system that handles co-
inductively defined predicates, the duals of inductively defined ones.
  Safe states. From the view point of program verification, the dual formalization can be obtained
by using the notion of safe states. A state is safe if the execution from the state will never reach a
bad state. The safety verification problem can be alternatively formalized as the problem asking
whether all initial states are safe.
  Let us formally define safe states. A state 𝑥 is unsafe if there exists a sequence 𝑥 0, . . . , 𝑥𝑛 (𝑛 ≥ 0)
                    Ó
such that 𝑥 = 𝑥 0 ∧ 𝑛𝑖=1 𝜏 (𝑥𝑖−1, 𝑥𝑖 ) ∧ ¬𝛼 (𝑥𝑛 ). A state is safe if it is not unsafe. The set 𝑆 of safe states
has an equational characterization similar to the set of reachable states: it is the greatest solution of
                                    𝛼 (𝑥) ∧ (∀𝑦.𝜏 (𝑥, 𝑦) ⇒ 𝑆 (𝑦)) ⇔ 𝑆 (𝑥).                                       (3)
This kind of definition, specifying something as the greatest solution of an equation, is called
coinductive definition, which is the dual of inductive definition. We write 𝜈𝑃 for the greatest solution
(provided that the equation for 𝑃 is understood). Following this notation, the set of safe states is 𝜈𝑆.
   Now the safety verification is reduced to the validity of the following sequent:
                                                                                     
                 𝜄 (𝑥) ⊢ (𝜈𝑆) (𝑥)     where 𝑆 (𝑥) ⇔ 𝛼 (𝑥) ∧ (∀𝑦.𝜏 (𝑥, 𝑦) ⇒ 𝑆 (𝑦)) .
This paper shows a tight connection between software model-checkers and cyclic-proof search for
the above sequent.
  Cyclic proofs for coinductively defined predicates. The idea of cyclic proof systems is applicable to
coinductively defined predicates. The proof system has the following rules:
                       𝛿 [(𝜈𝑃)] (𝑥) ⊢ 𝜑 (𝑥)                      𝜑 (𝑥) ⊢ 𝛿 [(𝜈𝑃)] (𝑥)
                                            (𝜈-L)                                     (𝜈-R)
                         (𝜈𝑃) (𝑥) ⊢ 𝜑 (𝑥)                          𝜑 (𝑥) ⊢ (𝜈𝑃) (𝑥)
where 𝑃 (𝑥) ⇔ 𝛿 [𝑃] (𝑥) is the defining equation for 𝑃. A proof is a preproof that satisfies the
following condition:
       If there is a link from a leaf 𝑙 to its ancestor 𝑛, (𝜈-R) rule is used in the path from 𝑛 to 𝑙.

3.2    Symbolic Execution
The (𝜈-R) rule with some postprocessing corresponds to the symbolic execution of the one-step
transition. This observation, which can be easily shown, is quite important because it is why
software model-checking processes coincide with proof-search strategies of 𝜄 (𝑥) ⊢ (𝜈𝑃) (𝑥). It
also tells us why (𝜇𝑃) (𝑥) ⊢ 𝛼 (𝑥), which seems a more natural expression of the model-checking
problem, does not suit for the purpose.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Software Model-Checking as Cyclic-Proof Search                                                                     1:7


   Definition 3.1 (Symbolic execution). Let 𝜑 (𝑥) be a formula denoting a set of states. Then the set
of states after the transition 𝜏 from 𝜑 can be represented by 𝜑 ′ (𝑦) := ∃𝑥 .𝜑 (𝑥) ∧ 𝜏 (𝑥, 𝑦), and we
write 𝜑 ⇝ 𝜑 ′. This transition on formulas is called symbolic execution.                            □
    Let us examine the connection between symbolic execution and (𝜈-R) rule. We discuss a proof-
search strategy for sequents of the form 𝜑 (𝑥) ⊢ (𝜈𝑃) (𝑥), which slightly generalize the goal sequent
𝜄 (𝑥) ⊢ (𝜈𝑃) (𝑥).
    Applying the (𝜈-R) rule to the sequent 𝜑 (𝑥) ⊢ (𝜈𝑃) (𝑥), we obtain
                                                           
                            𝜑 (𝑥) ⊢ ∀𝑦.𝜏 (𝑥, 𝑦) ⇒ (𝜈𝑃) (𝑦) ∧ 𝛼 (𝑥)
                                                                     (𝜈-R).
                                       𝜑 (𝑥) ⊢ (𝜈𝑃) (𝑥)
Notice that the new open sequent, which is the premise of the above partial proof, has a shape
much different from the goal sequent. For the purpose of proof search, it is convenient to restrict
the shape of open sequents. We introduce the first proof-search principle of this paper.
Principle 1. Try to fit the shape of open sequents into the form 𝜑 (𝑥) ⊢ (𝜈𝑃) (𝑥).
   We see that this principle leads to a proof strategy that corresponds to symbolic execution.
Following Principle 1, we try to simplify the open sequent 𝜑 (𝑥) ⊢ ∀𝑦.𝜏 (𝑥, 𝑦) ⇒ (𝜈𝑃) (𝑦) ∧ 𝛼 (𝑥) of
the above partial proof. Fortunately its validity is equivalent to the validity of two simple sequents
as the following partial proof shows:
                         ..
                          .
      𝜑 (𝑥), 𝜏 (𝑥, 𝑦) ⊢ ∃𝑥 .𝜑 (𝑥) ∧ 𝜏 (𝑥, 𝑦)      ∃𝑥 .𝜑 (𝑥) ∧ 𝜏 (𝑥, 𝑦) ⊢ (𝜈𝑃) (𝑦)
                                                                                   (Cut)
                               𝜑 (𝑥), 𝜏 (𝑥, 𝑦) ⊢ (𝜈𝑃) (𝑦)
                              𝜑 (𝑥) ⊢ 𝜏 (𝑥, 𝑦) ⇒ (𝜈𝑃) (𝑦)
                            𝜑 (𝑥) ⊢ ∀𝑦.𝜏 (𝑥, 𝑦) ⇒ (𝜈𝑃) (𝑦)                                  𝜑 (𝑥) |= 𝛼 (𝑥)
                                                                                 
                                               𝜑 (𝑥) ⊢ ∀𝑦.𝜏 (𝑥, 𝑦) ⇒ (𝜈𝑃) (𝑦) ∧ 𝛼 (𝑥)
                                                                                         (𝜈-R)
                                                            𝜑 (𝑥) ⊢ (𝜈𝑃) (𝑥)
(where the proof of 𝜑 (𝑥), 𝜏 (𝑥, 𝑦) ⊢ ∃𝑥 .𝜑 (𝑥) ∧ 𝜏 (𝑥, 𝑦) is omitted). One of the leaves is an open
sequent of the required form, and the other is fixed-point free and passed to an external solver. So
this partial proof meets the criterion of Principle 1.
   The above argument shows that the rule
                           ∃𝑥 .𝜑 (𝑥) ∧ 𝜏 (𝑥, 𝑦) ⊢ (𝜈𝑃) (𝑦)    𝜑 (𝑥) |= 𝛼 (𝑥)
                                                                             (SE)
                                             𝜑 (𝑥) ⊢ (𝜈𝑃) (𝑥)
is a derived rule. We call it the (precise) symbolic execution rule (SE). Since we are interested in
proof-search strategies, this rule should be read bottom-up: In order to prove the satefy of 𝜑, it
suffices to (1) check if 𝜑 does not violate the assertion, (2) do the symbolic execution 𝜑 ⇝ 𝜑 ′, and
(3) show the safety of 𝜑 ′ by proving the sequent 𝜑 ′ (𝑥) ⊢ (𝜈𝑃) (𝑥).

3.3    Bounded Model-Checking
The bounded model-checking problem [Biere et al. 1999] asks, given a bound 𝑘 and an initial state
𝜑 0 , whether a bad state is reachable from a state satisfying 𝜑 0 by transitions of steps ≤ 𝑘. More
formally, it checks if 𝜑 0 ⇝ 𝜑 1 ⇝ · · · ⇝ 𝜑𝑘 implies 𝜑𝑖 (𝑥) |= 𝛼 (𝑥) for every 𝑖 = 0, . . . , 𝑘. If it
is the case, we say 𝜑 0 is safe within 𝑘 steps. The bounded model-checking problem is important
because it is decidable in certain settings, and software model-checkers often have subprocedures
corresponding to bounded model-checking.

                                Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:8                                                                                 Takeshi Tsukada and Hiroshi Unno


             𝜑𝑘+1 (𝑥) ⊢ (𝜈𝑃) (𝑥)          𝜑𝑘 (𝑥) |= 𝛼 (𝑥)
                                                           (SE)
                        𝜑𝑘 (𝑥) ⊢ (𝜈𝑃) (𝑥)
                                 ..
                                  ..
                        𝜑 2 (𝑥) ⊢ (𝜈𝑃) (𝑥)          𝜑 1 (𝑥) |= 𝛼 (𝑥)
                                                                      (SE)
                                     𝜑 1 (𝑥) ⊢ (𝜈𝑃) (𝑥)                           𝜑 0 (𝑥) |= 𝛼 (𝑥)
                                                                                                     (SE)
                                                          𝜑 0 (𝑥) ⊢ (𝜈𝑃) (𝑥)
Fig. 3. A partial proof corresponding to bounded model-checking. Here 𝜑 0 ⇝ 𝜑 1 ⇝ · · · ⇝ 𝜑𝑘 ⇝ 𝜑𝑘+1 . The
partial proof is valid if 𝜑𝑖 (𝑥) |= 𝛼 (𝑥) for every 𝑖 = 0, . . . , 𝑘.




    In terms of cyclic-proof search, bounded model-checking is to construct a valid partial proof
consisting only of (SE). By iteratively applying (SE), we obtain a (valid or invalid) partial proof in
Figure 3. Here 𝜑 0 ⇝ 𝜑 1 ⇝ · · · ⇝ 𝜑𝑘 ⇝ 𝜑𝑘+1 . This is a valid partial proof if 𝜑𝑖 (𝑥) |= 𝛼 (𝑥) for every
𝑖 = 0, . . . , 𝑘. Therefore bounded model-checking with bound 𝑘 is equivalent to the problem asking
if the 𝑘 consecutive applications of (SE) to the corresponding sequent is a valid partial proof.

   Proposition 3.2. The 𝑘 consecutive applications of (SE) to 𝜑 (𝑥) ⊢ (𝜈𝑋 ) (𝑥) is a valid partial proof
if and only if 𝜑 is safe within 𝑘 steps.                                                              □

    Forward Criterion and States of Distance 𝑘. Sometimes postprocessing the result of bounded
model-checking gives a proof of unbounded safety. We call the criterion in [Sheeran et al. 2000]
based on a notion of distance (called forward diameter in [Sheeran et al. 2000]) forward criterion.
    Let us fix the set 𝜄 of initial states. A reachable state 𝑥 is of distance 𝑘 if there exists a sequence
                                                                        Ó
𝑥 0, . . . , 𝑥𝑘 witnessing the reachability of 𝑥 from 𝜄 (i.e. 𝜄 (𝑥 0 ) ∧ 𝑘𝑖=1 𝜏 (𝑥𝑖−1, 𝑥𝑖 ) ∧ (𝑥𝑘 = 𝑥)) and there
is no shorter witness. If 𝜄 = 𝜑 0 ⇝ 𝜑 1 ⇝ · · · ⇝ 𝜑𝑘 , then the set of states of distance 𝑘 is represented
                 Ó
by 𝜑𝑘 (𝑥) ∧ 𝑘−1    𝑖=0 ¬𝜑𝑖 (𝑥). The forward criterion says that a program is safe if the program is safe
with bound 𝑘 and the set of states of distance 𝑘 + 1 is empty.
    The set of distance-𝑘 states naturally appears in cyclic proof search. Recall that, in a cyclic
proof system, a leaf sequent can be proved by putting a link to its ancestor labeled by the same
judgement. For example, a proof of the open sequent 𝜑𝑘+1 (𝑥) ⊢ (𝜈𝑃) (𝑥) in Figure 3 is able to use
the assumptions 𝜑𝑖 (𝑥) ⊢ (𝜈𝑃) (𝑥) (0 ≤ 𝑖 < 𝑘 + 1). The set of distance-𝑘 states naturally arises when
we try to exploit the assumptions to the full.
    The idea is to split 𝜑𝑘+1 (𝑥) into 𝜑𝑖 (𝑥)Ô (0 ≤ 𝑖 < 𝑘 + 1) and the remainder, say 𝜓Ô           (𝑥). Assume a
formula 𝜓 such that 𝜑𝑘+1 (𝑥) |= 𝜓 (𝑥) ∨ 0≤𝑖<𝑘+1 𝜑𝑖 (𝑥). Let us write Ψ(𝑥) for 𝜓 (𝑥) ∨ 0≤𝑖<𝑘+1 𝜑𝑖 (𝑥).
The open sequent in the partial proof in Figure 3 can be expanded as

                        𝜓 (𝑥) ⊢ (𝜈𝑃) (𝑥)        𝜑 0 (𝑥) ⊢ (𝜈𝑃) (𝑥) . . . 𝜑𝑘 (𝑥) ⊢ (𝜈𝑃) (𝑥)
                                                                                           (∨-L) × (𝑘 + 1)
  𝜑𝑘+1 (𝑥) |= Ψ(𝑥)                                 Ψ(𝑥) ⊢ (𝜈𝑃) (𝑥)
                                                                    (Cut),
                         𝜑𝑘+1 (𝑥) ⊢ (𝜈𝑃) (𝑥)

which has 𝑘 + 1 open sequents. All but one open sequent can be immediately proved by links to
ancestors; the only remaining open sequent is 𝜓 (𝑥) ⊢ (𝜈𝑃) (𝑥). Since 𝜓 appears in a contra-variant
position, a stronger 𝜓 is more desirable.
                                       The strongest 𝜓 that satisfies the requirement is given by
                      Ó
𝜓 (𝑥) ⇔ 𝜑𝑘+1 (𝑥) ∧ 0≤𝑖<𝑘+1 ¬𝜑𝑖 (𝑥) . This is exactly the set of distance-(𝑘 + 1) states. In particular,
if the forward criterion holds, one can choose 𝜓 (𝑥) as ⊥. In this case, the remaining open sequent

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Software Model-Checking as Cyclic-Proof Search                                                                              1:9


                Impact                                                        Cyclic proof
                program unwinding                                             partial proof
                    safe, well-labeled —                                           valid —
                    safe, well-labeled, complete —                                 cyclic proof
                covering relation                                             collection of links
                Expand procedure                                              application of (SE+Cut)
                                     Table 1. An Impact-Cyclic-proof dictionary.


is ⊥ ⊢ (𝜈𝑃) (𝑥), which is trivially provable independent of 𝑃; hence we complete the proof of
𝜑 0 (𝑥) ⊢ (𝜈𝑃) (𝑥).3

3.4    Predicate Abstraction
As shown in the previous section, (Cut) plays an important role in the construction of a cyclic
proof. Let us introduce the derived rule
              𝜓 (𝑥) ⊢ (𝜈𝑃) (𝑥)           ∃𝑦.𝜑 (𝑦) ∧ 𝜏 (𝑦, 𝑥) |= 𝜓 (𝑥)           𝜑 (𝑥) |= 𝛼 (𝑥)
                                                                                                  (SE+Cut),
                                            𝜑 (𝑥) ⊢ (𝜈𝑃) (𝑥)
which can be proved by
              ∃𝑥 .𝜑 (𝑥) ∧ 𝜏 (𝑥, 𝑦) |= 𝜓 (𝑦)     𝜓 (𝑥) ⊢ (𝜈𝑃) (𝑥)
                                                                  (Cut)
                        ∃𝑥 .𝜑 (𝑥) ∧ 𝜏 (𝑥, 𝑦) ⊢ (𝜈𝑃) (𝑦)                                 𝜑 (𝑥) |= 𝛼 (𝑥)
                                                                                                          (SE).
                                                  𝜑 (𝑥) ⊢ (𝜈𝑃) (𝑥)
We call 𝜓 in (SE+Cut) the cut formula.
   The choice of the cut formula is quite important. If it is too strong, it is not an invariant; if it is
too weak, the sequent 𝜓 (𝑥) ⊢ (𝜈𝑃) (𝑥) becomes invalid.
   Predicate abstraction [Ball et al. 2001; Graf and Saïdi 1997] is a heuristic for the choice of the cut
formula. The idea is to further restrict the shape of open sequents: an open sequent must be of the
form 𝜗 (𝑥) ⊢ (𝜈𝑃) (𝑥) where 𝜗 comes from a finite set of predicates, say Ξ. Suppose that Ξ is closed
under conjunction. In order to avoid making the open sequent invalid, the best choice of the cut
formula is the strongest formula in Ξ.
   This idea leads to the following principle.
Principle 2. Use (SE+Cut). Choose the strongest formula 𝜓 ∈ Ξ satisfying ∃𝑥 .𝜑 (𝑥) ∧ 𝜏 (𝑥, 𝑦) |=
𝜓 (𝑦) as the cut formula.
   The proof-search procedure following Principles 1 and 2 terminates. Since Ξ is finite, the length
of the path in a partial proof is bounded by the number of candidate formulas; if it exceeds, then a
sequent appears twice in the path and thus putting a link completes the proof.

4     LAZY ABSTRACTION WITH INTERPOLANTS: IMPACT
This section explains another proof-search strategy that corresponds to the software model-checker
Impact developed by McMillan [McMillan 2006]. For readers familiar with Impact, Table 1 gives
a dictionary of terminologies of Impact [McMillan 2006] and cyclic-proof search and Figure 4
illustrates the correspondence between internal states of Impact (called program unwinding) and
partial proofs.
3 Actually what we obtained is a pre-proof, i.e. a proof-like structure with cycles, and we should check the global trace

condition to conclude that it is a proof. To see that the pre-proof satisfies the global trace condition, recall that (SE) is a
derived rule using (𝜈-R) rule.


                                   Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:10                                                                                Takeshi Tsukada and Hiroshi Unno


                                                  𝜑𝑛 (𝑥) |= 𝛼 (𝑥)
       𝜑𝑛+1 (𝑥) ⊢ (𝜈𝑃) (𝑥)      ∃𝑥 .𝜑𝑛 (𝑥) ∧ 𝜏 (𝑥, 𝑦) |= 𝜑𝑛+1 (𝑦)
                 𝜑𝑛 (𝑥) ⊢ (𝜈𝑃) (𝑥)
                          ..
                           ..                              𝜑 1 (𝑥) |= 𝛼 (𝑥)
                 𝜑 2 (𝑥) ⊢ (𝜈𝑃) (𝑥)         ∃𝑥 .𝜑 1 (𝑥) ∧ 𝜏 (𝑥, 𝑦) |= 𝜑 2 (𝑦)                  𝜄 (𝑥) |= 𝛼 (𝑥)
                                     𝜑 1 (𝑥) ⊢ (𝜈𝑃) (𝑥)                         ∃𝑥 .𝜄 (𝑥) ∧ 𝜏 (𝑥, 𝑦) |= 𝜑 1 (𝑦)
                                                                  𝜄 (𝑥) ⊢ (𝜈𝑃) (𝑥)

Fig. 4. A partial proof (above) and the corresponding internal state of Impact (below). All rules used in the
partial proof are (SE+Cut).


   A significant difference from the previously discussed proof-search strategies is that Impact
does not hesitate to generate an invalid sequent. The difference allows us to simplify the strategy
of the cut-formula choice. Recall that the only requirement for the cut formula 𝜓 in (SE+Cut) rule
is ∃𝑥 .𝜑 (𝑥) ∧ 𝜏 (𝑥, 𝑦) ⊢ 𝜓 (𝑦), and no upper bound is given. Impact tentatively chooses ⊤ as the cut
formula.
Principle 3. Use (SE+Cut). Tentatively choose ⊤ as the cut formula.
   Of course, ⊤ is usually too weak and the open sequent ⊤ ⊢ (𝜈𝑃) (𝑥) is often invalid. The invalidity
of the sequent is revealed by applying (SE+Cut) again:
           ⊤ ⊢ (𝜈𝑃) (𝑥) ∃𝑥 .⊤ ∧ 𝜏 (𝑥, 𝑦) |= ⊤ ⊤ |= 𝛼 (𝑥)
                          ⊤ ⊢ (𝜈𝑃) (𝑥)                     ∃𝑥 .𝜄 (𝑥) ∧ 𝜏 (𝑥, 𝑦) |= ⊤ 𝜄 (𝑥) |= 𝛼 (𝑥)
                                                     𝜄 (𝑥) ⊢ (𝜈𝑃) (𝑥)
This partial proof is invalid as ⊤ |= 𝛼 (𝑥) does not hold (otherwise the verification problem is trivial).
Impact tries to fix an invalid partial proof by strengthening the cut formulas, following the next
principle.4
Principle 4. When the partial proof is found to be invalid, replace each cut formula 𝜑𝑖 (𝑥) with
𝜑𝑖 (𝑥) ∧ 𝑄𝑖 (𝑥), where 𝑄𝑖 is a fresh predicate variable, and solve the constraints on 𝑄𝑖 .
   If the current partial proof is that in Figure 4, cut-formulas 𝜑 1, . . . , 𝜑𝑛 must be strengthened if
𝜑𝑛 (𝑥) ⊭ 𝛼 (𝑥). For simplicity, we assume 𝜑𝑖 (𝑥) |= 𝛼 (𝑥) for 𝑖 < 𝑛. We replace 𝜑𝑖 (𝑥) in the partial
proof with 𝜑𝑖 (𝑥) ∧ 𝑄𝑖 (𝑥) (1 ≤ 𝑖 ≤ 𝑛), where 𝑄 1, . . . , 𝑄𝑛 are distinct predicate variables. The side
conditions 𝜑𝑖 (𝑥) |= 𝛼 (𝑥) and ∃𝑥 .𝜑𝑖 (𝑥)∧𝜏 (𝑥, 𝑦) |= 𝜑𝑖+1 (𝑥) are transformed into 𝜑𝑖 (𝑥)∧𝑄𝑖 (𝑥) |= 𝛼 (𝑥)
and ∃𝑥 .𝜑𝑖 (𝑥) ∧ 𝑄𝑖 (𝑥) ∧ 𝜏 (𝑥, 𝑦) |= 𝜑𝑖+1 (𝑦) ∧ 𝑄𝑖+1 (𝑦). Slightly simplifying the constraints by using
∃𝑥 .𝜑𝑖 (𝑥) ∧ 𝜏 (𝑥, 𝑦) |= 𝜑𝑖+1 (𝑦) (𝑖 = 0, . . . , 𝑛) and 𝜑𝑖 (𝑥) |= 𝛼 (𝑥) (𝑖 = 0, . . . , 𝑛 − 1), we obtain the
following constraint set:
                             𝜄 (𝑥 0 ) ∧ 𝜏 (𝑥 0, 𝑥 1 ) ⇒ 𝑄 1 (𝑥 1 ),
                                                    
              𝑄𝑖 (𝑥𝑖 ) ∧ 𝜑𝑖 (𝑥𝑖 ) ∧ 𝜏 (𝑥𝑖 , 𝑥𝑖+1 ) ⇒ 𝑄𝑖+1 (𝑥𝑖+1 ),                       𝑖 = 1, . . . , 𝑛 − 1
                             𝑄𝑛 (𝑥𝑛 ) ∧ 𝜑𝑛 (𝑥𝑛 ) ⇒ 𝛼 (𝑥𝑛 ).
If a solution (𝜓𝑖 )𝑖=1,...,𝑛 for (𝑄𝑖 )𝑖 is given, we can fix the partial proof by replacing 𝜑𝑖 with 𝜑𝑖 ∧ 𝜓𝑖 .
A solution of the constraints is known as an interpolant.
4 Here we note some differences between Impact and the proof-search strategy following Principle 4. See Remark 1.



Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Software Model-Checking as Cyclic-Proof Search                                                                   1:11


   Definition 4.1. Given a sequence 𝜗® = 𝜗 1𝜗 2 . . . 𝜗𝑛+1 of formulas, its interpolant is a sequence
 ®
𝜓 = 𝜓 0𝜓 1 . . . 𝜓𝑛+1 of formulas that satisfies the following conditions: (1) 𝜓 0 = ⊤ and 𝜓𝑛+1 = ⊥, (2)
|= 𝜓𝑖−1 ∧ 𝜗𝑖 ⇒ 𝜓𝑖 for every 1 ≤ 𝑖 ≤ 𝑛, and (3) fv(𝜓𝑖 ) ⊆ fv(𝜗 1, . . . , 𝜗𝑖 ) ∩ fv(𝜗𝑖+1, . . . , 𝜗𝑛+1 ) for every
1 ≤ 𝑖 ≤ 𝑛.                                                                                                      □
   A solution of the above constraint is an interpolant of 𝜗® where 𝜗 1 := 𝜄 (𝑥 0 ) ∧ 𝜏 (𝑥 0, 𝑥 1 ), 𝜗𝑖+1 :=
𝜑𝑖 (𝑥𝑖 ) ∧ 𝜏 (𝑥𝑖 , 𝑥𝑖+1 ) for 𝑖 = 1, . . . , 𝑛 − 1, and 𝜗𝑛+1 = 𝜑𝑛 (𝑥𝑛 ) ∧ ¬𝛼 (𝑥𝑛 ).
   The termination condition of Impact is also closely related to cyclic proofs. Impact terminates if
𝜑𝑖 (𝑥) |= 𝜑 𝑗 (𝑥) for some 𝑖 > 𝑗. Then replacing the partial proof above 𝜑𝑖 (𝑥) ⊢ (𝜈𝑃) (𝑥) with
                                𝜑𝑖 (𝑥) |= 𝜑 𝑗 (𝑥)    𝜑 𝑗 (𝑥) ⊢ (𝜈𝑃) (𝑥)
                                                                        (Cut)
                                           𝜑𝑖 (𝑥) ⊢ (𝜈𝑃) (𝑥)
and making a link from 𝜑 𝑗 (𝑥) ⊢ (𝜈𝑃) (𝑥) to the ancestor yields a cyclic proof.
  In summary, Impact can be seen as a cyclic-proof search strategy following Principles 1, 3 and 4.
Remark 1. We discuss differences between Impact and the proof-search strategy following Princi-
ples 1, 3 and 4. First the proof-search strategy does not cover an important heuristic, known as
forced covering, which tries to refine predicates so that one can make a cycle from a certain node to
another; this feature can be understood as an additional proof-search rule. Second Impact computes
an interpolant of a sequence slightly different from 𝜗: ® the sequence 𝜗® contains the information of
the current cut-formulas 𝜑𝑖 . Theoretically, the difference does not affect the refinement process
(modulo logical equivalence), since the interpolants are conjoined with the current cut-formulas. In
practice, however, [Vizel and Gurfinkel 2014] claims that the use of the current cut-formulas is
one of the keys to achieve their incremental interpolation-based model checking, which indeed
shows an improvement over previous methods based on interpolation a la Impact. Third the actual
implementation of Impact uses a special kind of interpolant, which follows Principle 5 below as
well.5                                                                                              □
Remark 2. One may notice that the combination of Principles 1, 2 and 4 (instead of 1, 3 and 4) would
also be possible. The resulting cyclic-proof search strategy corresponds to the lazy abstraction in
the style of Blast [Henzinger et al. 2004, 2002].                                                 □

5   DUAL SEQUENT AND DUAL IMPACT
So far, we have discussed a relationship between cyclic-proof search for 𝜄 (𝑥) ⊢ (𝜈𝑃) (𝑥) and software
model-checking algorithms. As we emphasized in Section 3.1, the identification of the goal sequent
𝜄 (𝑥) ⊢ (𝜈𝑃) (𝑥) corresponding to software model-checking is an important contribution of this
paper, and once the goal sequent is appropriately set, the contents of Sections 3 and 4 are natural
and expected, which one might find relatively straightforward.
    This section briefly discusses proof-search for (𝜇𝑅) (𝑥) ⊢ 𝛼 (𝑥) (where 𝑅 is defined by Equation 1)
from the view point of software model-checking, and shows how the choice of the goal sequent
affects the whole picture.
    We derive the counterparts of (SE) and (SE+Cut), called (BackSE) and (BackSE+Cut). We have
                               𝜄 (𝑥) ∨ (∃𝑦.(𝜇𝑅) (𝑦) ∧ 𝜏 (𝑦, 𝑥)) ⊢ 𝜑 (𝑥)
                                                                        (𝜇-L)
                                          (𝜇𝑅) (𝑥) ⊢ 𝜑 (𝑥)
of which left-hand-side of ⊢ in the premise is a complicated formula containing a least fixed-point.
Following the dual of Principle 1, moving logical connectives to the right-hand-side, we obtain the
5 Personal communication.



                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:12                                                                                  Takeshi Tsukada and Hiroshi Unno


following derived rule:

                        (𝜇𝑅) (𝑥) ⊢ ∀𝑦.𝜏 (𝑥, 𝑦) ⇒ 𝜓 (𝑦)            𝜄 (𝑥) |= 𝜓 (𝑥)
                                                                                    (BackSE).
                                        (𝜇𝑅) (𝑥) ⊢ 𝜓 (𝑥)

The formula ∀𝑦.𝜏 (𝑥, 𝑦) ⇒ 𝜓 (𝑦) has a clear computational interpretation: it is the weakest precon-
dition of 𝜓 with respect to 𝜏. This is the dual of the strongest postcondition, which coincides with
the symbolic execution.
   The duality becomes clearer in (BackSE+Cut)

           (𝜇𝑅) (𝑥) ⊢ 𝜑 (𝑥)        𝜑 (𝑥) |= ∀𝑦.𝜏 (𝑥, 𝑦) ⇒ 𝜓 (𝑦)          𝜄 (𝑥) |= 𝜓 (𝑥)
                                                                                           (BackSE+Cut)
                                       (𝜇𝑅) (𝑥) ⊢ 𝜓 (𝑥)

which can be proved by

          (𝜇𝑅) (𝑥) ⊢ 𝜑 (𝑥)     𝜑 (𝑥) |= ∀𝑦.𝜏 (𝑥, 𝑦) ⇒ 𝜓 (𝑦)
                                                             (Cut)
                   (𝜇𝑅) (𝑥) ⊢ ∀𝑦.𝜏 (𝑥, 𝑦) ⇒ 𝜓 (𝑦)                                  𝜄 (𝑥) |= 𝜓 (𝑥)
                                                                                                    (BackSE).
                                            (𝜇𝑅) (𝑥) ⊢ 𝜓 (𝑥)

Since 𝜑 (𝑥) |= ∀𝑦.𝜏 (𝑥, 𝑦) ⇒ 𝜓 (𝑦) is equivalent to ∃𝑥 .𝜑 (𝑥) ∧ 𝜏 (𝑥, 𝑦) |= 𝜓 (𝑦), (BackSE+Cut)
computes an over-approximation of the symbolic execution as in (SE+Cut). The only difference is
the direction; in a partial proof for (𝜇𝑅) (𝑥) ⊢ 𝜓 (𝑥), an execution starts from a leaf and ends at the
root, which should be understood as an assertion.
   So model-checking algorithms corresponding to proof-search for (𝜇𝑅) (𝑥) ⊢ 𝜓 (𝑥) can be under-
stood as procedures checking the backward (un)reachability. Here is a twist: the natural logical
expression (𝜇𝑅) (𝑥) ⊢ 𝜓 (𝑥) of the model-checking problem corresponds to the execution of pro-
grams in the unnatural direction. We think that this twist might be a reason why the connection
between cyclic proofs and software model-checking hashad not yet been formally revealed despite
that it is natural and expected.

6      MAXIMAL CONSERVATIVITY AND PROPERTY-DIRECTED REACHABILITY
Sections 4 reviewed McMillan’s approach based on interpolants [McMillan 2006], as well as its
variants, from the view point of cyclic proof search. His algorithm tentatively uses ⊤ as the cut-
formula at the beginning and improves it using interpolants. The efficiency of the algorithm heavily
relies on the quality of interpolants.
   This section introduces a heuristic, or a criterion, that determines what is a “better” interpolation.
The criterion is conservativity: it prefers an interpolation that introduces smaller changes to the
current partial proof. We study a variant of McMillan’s algorithm that uses a maximally conservative
interpolation instead of arbitrary ones and discuss its connection to the approach to software model-
checking called property directed reachability (or PDR) [Cimatti and Griggio 2012; Hoder and Bjørner
2012].

6.1     Maximal conservativity
We introduce the key notion, maximal conservativity, to the heuristic studied in this section.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Software Model-Checking as Cyclic-Proof Search                                                                   1:13


  Let us first recall McMillan’s algorithm [McMillan 2006], regarded as a goal-oriented proof search.
The refinement process takes an invalid partial proof
                                         𝜑𝑛 (𝑥) |= 𝛼 (𝑥)
        ⊤ ⊢ (𝜈𝑃) (𝑥)      ∃𝑥 .𝜑𝑛 (𝑥) ∧ 𝜏 (𝑥, 𝑦) |= ⊤
             𝜑𝑛 (𝑥) ⊢ (𝜈𝑃) (𝑥)
                      ..
                       ..                            𝜑 1 (𝑥) |= 𝛼 (𝑥)
             𝜑 2 (𝑥) ⊢ (𝜈𝑃) (𝑥)       ∃𝑥 .𝜑 1 (𝑥) ∧ 𝜏 (𝑥, 𝑦) |= 𝜑 2 (𝑦)                  𝜄 (𝑥) |= 𝛼 (𝑥)
                                𝜑 1 (𝑥) ⊢ (𝜈𝑃) (𝑥)                        ∃𝑥 .𝜄 (𝑥) ∧ 𝜏 (𝑥, 𝑦) |= 𝜑 1 (𝑦)
                                                            𝜄 (𝑥) ⊢ (𝜈𝑃) (𝑥)
in which all judgements except for 𝜑𝑛 (𝑥) |= 𝛼 (𝑥) are valid. It returns a valid proof of 𝜄 (𝑥) ⊢ (𝜈𝑃) (𝑥)
obtained by replacing each 𝜑𝑖 with a stronger predicate 𝜑𝑖′.
   We represent the above partial proof as a sequence 𝜑 0, 𝜑 1, . . . , 𝜑𝑛 of formulas (where 𝜑 0 = 𝜄).
Then an input to the refinement process can be represented as a sequence 𝜑 0, . . . , 𝜑𝑛 of formulas
that satisfies
         𝜑0 = 𝜄      and       𝜑𝑖 (𝑥) |= 𝛼 (𝑥) and 𝜑𝑖 (𝑥) ∧ 𝜏 (𝑥, 𝑦) |= 𝜑𝑖+1 (𝑦) for 𝑖 = 0, . . . , 𝑛 − 1        (4)
(recall that all judgements in the input partial proof are valid except for 𝜑𝑛 (𝑥) |= 𝛼 (𝑥)). The
refinement process tries to construct a sequence 𝜑 0′ , . . . , 𝜑𝑛′ such that
                        
                        
                         𝜑 0′ = 𝜄
                        𝜑 ′ (𝑥) |= 𝜑𝑖 (𝑥)
                        
                                                             for every 𝑖 = 0, . . . , 𝑛
                        
                        
                            𝑖
                             ′                   ′
                                                                                                                 (5)
                          𝜑 𝑖 (𝑥) ∧ 𝜏 (𝑥, 𝑦) |= 𝜑𝑖+1 (𝑦)     for every 𝑖 = 0, . . . , 𝑛 − 1
                        
                        
                        
                        𝜑 ′ (𝑥) |= 𝛼 (𝑥).
                        
                         𝑛
We call a sequence that satisfies Equation 5 a refinement of 𝜑 0, . . . , 𝜑𝑛 .
   In McMillan’s approach [McMillan 2006], we let 𝜑𝑖′ (𝑥) ≡ 𝜑𝑖 (𝑥) ∧ 𝑄𝑖 (𝑥) (𝑖 = 0, . . . , 𝑛), where 𝑄𝑖
is a fresh predicate variable, and solve the constraints
 { (𝜑𝑖 (𝑥) ∧𝑄𝑖 (𝑥)) ∧𝜏 (𝑥, 𝑦) ⇒ 𝑄𝑖+1 (𝑦) | 𝑖 = 0, . . . , 𝑛 − 1 } ∪ { 𝑄 0 = ⊤, 𝜑𝑛 (𝑥) ∧𝑄𝑛 (𝑥) ⇒ 𝛼 (𝑥) } (6)
using an interpolating theorem prover, finding a suitable assignment for (𝑄𝑖 )0≤𝑖 ≤𝑛 . The constraint
solving of (6) is a kind of interpolation problem, known as sequential interpolation [Henzinger et al.
2004; McMillan 2006], we call a solution (𝑄𝑖 )0≤𝑖 ≤𝑛 an interpolant. Observe that this refinement
process may change any formula in the current partial proof.
   The heuristic studied in this section tries to minimize the changes. That means, it prefers an
interpolant (𝑄𝑖 )0≤𝑖 ≤𝑛 of (6) such that 𝑄𝑖 = ⊤ for more indices 𝑖. It is not difficult to see that, if
𝑄 0, . . . , 𝑄𝑛 is an interpolant and 𝑄𝑘 = ⊤, then ⊤, . . . , ⊤, 𝑄𝑘+1, . . . , 𝑄𝑛 is also an interpolant. Hence
the heuristic chooses an interpolant ⊤, . . . , ⊤, 𝑄𝑘 , 𝑄𝑘+1, . . . , 𝑄𝑛 such that no interpolant of the form
                   ′ , . . . , 𝑄 ′ exists, and we call such an interpolant a maximally conservative interpolant.
⊤, . . . , ⊤, ⊤, 𝑄𝑘+1           𝑛
The corresponding maximally conservative refinement 𝜑 0′ , . . . , 𝜑𝑛′ , which is defined by 𝜑𝑖′ = 𝜑𝑖 ∧ 𝑄𝑖
(0 ≤ 𝑖 ≤ 𝑛), satisfies 𝜑𝑖′ = 𝜑𝑖 as much as possible.
   Definition 6.1 (Maximally conservative refinement). Let 𝜑 0, . . . , 𝜑𝑛 be a sequential representation
of a partial proof that satisfies (4). Its refinement is a valid partial proof represented as 𝜑 0′ , . . . , 𝜑𝑛′
that satisfies the constraints in (5). It is 𝑘-conservative if 𝜑 𝑗′ = 𝜑 𝑗 for every 𝑗 ≤ 𝑘. It is maximally
conservative if it is 𝑘-conservative and no (𝑘 + 1)-conservative refinement exists.                           □
  The heuristic based on maximal conservativity introduces the following principle.

                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:14                                                                                Takeshi Tsukada and Hiroshi Unno


Algorithm 1 Naïve algorithm to compute a maximally conservative refinement
Input: Predicates 𝜄 (𝑥), 𝜏 (𝑥, 𝑦), 𝛼 (𝑥) defining linear CHCs
Input: A partial proof 𝜑 0, . . . , 𝜑𝑛 satisfying (4)
Output: A maximally conservative refinement 𝜑 0′ , . . . , 𝜑𝑛′                         ⊲ NaïveMCR may fail
  1: function NaïveMCR(𝜄, 𝜏, 𝛼; 𝜑 0, . . . , 𝜑𝑛 )
  2:    C := { (𝜑𝑖 (𝑥) ∧ 𝑄𝑖 (𝑥)) ∧ 𝜏 (𝑥, 𝑦) ⇒ 𝑄𝑖+1 (𝑦) | 𝑖 = 0, . . . , 𝑛 − 1 } ∪ { 𝜑𝑛 (𝑥) ∧ 𝑄𝑛 (𝑥) ⇒ 𝛼 (𝑥) }
  3:    𝑗 := 𝑛
  4:    while 𝑗 ≥ 0 do
  5:         if C ∪ {⊤ ⇒ 𝑄𝑖 (𝑥) | 𝑖 = 0, . . . , 𝑗 } has a solution then
  6:             let 𝑄 0, . . . , 𝑄𝑛 be a solution
  7:             return (𝜑𝑖 ∧ 𝑄𝑖 )𝑖=0,...,𝑛
  8:         end if
  9:         𝑗 := 𝑗 − 1
 10:    end while
 11:    fail
 12: end function


Principle 5. Use a maximally-conservative-interpolation theorem prover as the backend solver.6
   We define lazy abstraction with maximally conservative interpolants, or Impact/mc, as a variant
of McMillan’s algorithm in which the interpolating theorem prover always chooses a maximally
conservative one. So Impact/mc is an algorithm following Principles 1, 3, 4 and 5. Since Principle 5
does not specify an algorithm that computes a maximally conservative interpolant, the behavior of
Impact/mc depends on the backend maximally-conservative-interpolation theorem prover.
   The rest of this section develops algorithms for maximally conservative interpolation and
compares Impact/mc with other software model-checking algorithms. For technical convenience,
we shall focus on maximally conservative refinement instead of interpolation in the sequel.
Remark 3. The idea of maximally conservative refinement or interpolant can be found in the
literature, e.g. in [Cimatti and Griggio 2012] and [Vizel and Gurfinkel 2014]. We shall compare their
work with this paper in Remark 5, after establishing a connection between maximal conservativity
and PDR.                                                                                           □

6.2    A Naïve algorithm for maximally conservative refinement
A maximally conservative refinement is computable if binary interpolants (and thus sequential
interpolants) are computable. Here we give a naïve algorithm in order to prove the computability;
more sophisticated algorithms shall be introduced in the following subsections.
   Algorithm 1 is a naïve algorithm that constructs a maximally conservative refinement. The
naïve algorithm tries to construct a 𝑘-conservative refinement for 𝑘 = 𝑛, 𝑛 − 1, 𝑛 − 2, . . . , 0 until it
finds a refinement. A 𝑘-conservative refinement can be computed using a sequential interpolation
algorithm: letting 𝜑𝑖′ (𝑥) = 𝜑𝑖 (𝑥) ∧ 𝑄𝑖 (𝑥), where 𝑄𝑖 is a fresh predicate variable, it suffices to solve
the constraints (6) with ⊤ ⇒ 𝑄𝑖 (𝑥) for every 𝑖 ≤ 𝑘.

6.3    Inductive characterization of maximally conservative refinement
We show that a subproof of a maximally conservative refinement must be maximally conservative
as well in a certain sense, and this property gives us an inductive characterization of maximally
conservative refinements. After giving an inductive characterization of maximally conservative
6 The actual implementation of Impact follows this principle, as we mentioned in Remark 1.



Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Software Model-Checking as Cyclic-Proof Search                                                                               1:15


refinements, we develop an algorithm inspired by the characterization. We say that 𝜑 0′ , . . . , 𝜑𝑛′ is a
maximally conservative refinement of 𝜑 0, . . . , 𝜑𝑛 satisfying 𝜓 (𝑥) if it is a maximally conservative re-
finement with respect to the constraint system7 𝑆 ′ = {𝜄 (𝑥) ⇒ 𝑃 (𝑥), 𝑃 (𝑥) ∧𝜏 (𝑥, 𝑦) ⇒ 𝑃 (𝑦), 𝑃 (𝑥) ⇒
𝜓 (𝑥)}, in which the assertion 𝛼 is replaced with 𝜓 .
  Lemma 6.2. Let (𝜑𝑖 )0≤𝑖 ≤𝑛 be a partial proof satisfying (4). For every partial proof (𝜓 0, . . . ,𝜓𝑛−1 ),
the following conditions are equivalent:
   (i) There exists 𝜓𝑛 such that (𝜓 0, . . . ,𝜓𝑛−1,𝜓𝑛 ) is a refinement of (𝜑 0, . . . , 𝜑𝑛 ) satisfying 𝛼.
  (ii) (𝜓 0, . . . ,𝜓𝑛−1 ) is a refinement of (𝜑 0, . . . , 𝜑𝑛−1 ) satisfying ¬∃𝑦.𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦).
   Proof. Assume (1). Then 𝜓𝑛−1 (𝑥)∧𝜏 (𝑥, 𝑦) |= 𝜓𝑛 (𝑥) and 𝜓𝑛 (𝑥) |= 𝛼 (𝑥). Hence 𝜓𝑛−1 (𝑥)∧𝜏 (𝑥, 𝑦) |=
𝛼 (𝑦), which implies 𝜓𝑛−1 (𝑥) |= ¬∃𝑦.𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦).
   Assume (2). Then 𝜓𝑛−1 (𝑥) |= ¬∃𝑦.𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦), which implies 𝜓𝑛−1 (𝑥) ∧ 𝜏 (𝑥, 𝑦) |= 𝛼 (𝑦). Since
𝜓𝑛−1 (𝑥) |= 𝜑𝑛−1 (𝑥) and 𝜑𝑛−1 (𝑥) ∧ 𝜏 (𝑥, 𝑦) |= 𝜑𝑛 (𝑦) by the assumption (4), 𝜓𝑛−1 (𝑥) ∧ 𝜏 (𝑥, 𝑦) |= 𝜑𝑛 (𝑦)
as well. Letting 𝜓𝑛 (𝑥) be an interpolant of 𝜓𝑛−1 (𝑥) ∧ 𝜏 (𝑥, 𝑦) and 𝛼 (𝑦) ∧ 𝜑𝑛 (𝑦), the partial proof
(𝜓 0, . . . ,𝜓𝑛−1,𝜓𝑛 ) is a refinement of (𝜑 0, . . . , 𝜑𝑛 ) satisfying 𝛼.                                □
   Theorem 6.3. Let (𝜑𝑖 )0≤𝑖 ≤𝑛 be a partial proof satisfying (4). Suppose that (𝜑𝑖′)0≤𝑖 ≤𝑛 is a refinement
of (𝜑𝑖 )0≤𝑖 ≤𝑛 satisfying 𝛼. It is maximally conservative if and only if the following conditions hold:
   (a) If 𝜑𝑛 (𝑥) |= 𝛼 (𝑥), then (𝜑 0′ , . . . , 𝜑𝑛′ ) = (𝜑 0, . . . , 𝜑𝑛 ).
   (b) If 𝜑𝑛 (𝑥) ̸ |= 𝛼 (𝑥), then (𝜑 0′ , . . . , 𝜑𝑛−1
                                                   ′ ) is a maximally conservative refinement of (𝜑 , . . . , 𝜑
                                                                                                   0            𝑛−1 )
       satisfying ¬∃𝑦.𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦).
   Proof. The first case is trivial. Assume that 𝜑𝑛 (𝑥) ̸ |= 𝛼 (𝑥). Then there is no 𝑛-conservative
refinement. So it suffices to show that the following conditions are equivalent for every 𝑘 < 𝑛:
    • (𝜑𝑖 )0≤𝑖 ≤𝑛 has a 𝑘-conservative refinement satisfying 𝛼.
    • (𝜑𝑖 )0≤𝑖 ≤𝑛−1 has a 𝑘-conservative refinement satisfying ¬∃𝑦.𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦).
This equivalence is a consequence of Lemma 6.2.                                                   □
   IndMCR (Algorithm 2) is an algorithm based on the characterization in Theorem 6.3. The func-
tion interpolation(𝜓 (𝑥,® 𝑦),
                           ® 𝜗 (𝑦,
                                ® 𝑧®)) nondeterministically returns a formula from {𝛾 (𝑦)    ® | 𝜓 (𝑥,
                                                                                                     ® 𝑦)
                                                                                                        ® |=
𝛾 and 𝛾 (𝑦)
          ® |= 𝜗 (𝑦,
                  ® 𝑧®)}, provided that 𝜓 (𝑥,
                                            ® 𝑦)® |= 𝜗 (𝑦,
                                                         ® 𝑧®). Line 3 corresponds to the case (a), whereas
lines 4, 5 and 7 correspond to the case (b). Hence the correctness of IndMCR is a direct consequence
of Theorem 6.3. The termination can be shown by induction on 𝑛, since it has no loop and a
recursive call takes the subproof (𝜑 0, . . . , 𝜑𝑛−1 ) as its argument; note that 𝜑 0 = 𝜄 and thus, if 𝑛 = 0,
exactly one of the conditions in lines 2 and 3 is true. In summary, we have the following theorem.
  Theorem 6.4. IndMCR always terminates. The set of possible return values of IndMCR coincides
with the set of maximally conservative refinements.                                         □

6.4    Approximating quantified-formulas by quantifier-free formulas
IndMCR given in the previous subsection is defined by a simple induction on the structure of the
partial proof. However it is not practical since it uses quantified formulas, which are hard to reason
about. This section introduces an algorithm that does not pass a quantified formula as an argument.
  Our goal is to remove the quantifier of ∃𝑦.𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦) in IndMCR. We appeal to the logical
equivalence                                                Ü
                        ∃𝑦.𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦)       ⇔          (𝜏 (𝑥, 𝑐) ∧ ¬𝛼 (𝑐))                   (7)
                                                                          𝑐
7 The class of constraint systems of this form is called linear CHCs (see e.g., [Bjørner et al. 2015] for the definition).



                                    Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:16                                                                                Takeshi Tsukada and Hiroshi Unno


Algorithm 2 Maximally conservative refinement, defined inductively
Input: Predicates 𝜄 (𝑥), 𝜏 (𝑥, 𝑦), 𝛼 (𝑥) defining linear CHCs
Input: A partial proof 𝜑 0, . . . , 𝜑𝑛 satisfying (4)
Output: A maximally conservative refinement 𝜑 0′ , . . . , 𝜑𝑛′                               ⊲ IndMCR may fail
 1: function IndMCR(𝜄, 𝜏, 𝛼; 𝜑 0, . . . , 𝜑𝑛 )
 2:    if |= ∃𝑥 .𝜄 (𝑥) ∧ ¬𝛼 (𝑥) then fail
 3:    if 𝜑𝑛 (𝑥) |= 𝛼 (𝑥) then return (𝜑 0, . . . , 𝜑𝑛 )
 4:    𝛾 (𝑥) := ∃𝑦.𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦)
 5:    (𝜑 0, . . . , 𝜑𝑛−1 ) := IndMCR(𝜄, 𝜏, ¬𝛾; 𝜑 0, . . . , 𝜑𝑛−1 )
 6:                                                             ⊲ ∃𝑥 .𝜑𝑛−1(𝑥) ∧ 𝜏 (𝑥, 𝑦) |= 𝜑𝑛 (𝑦) ∧ 𝛼 (𝑦) holds
 7:    𝜑𝑛 (𝑦) := interpolation 𝜑𝑛−1 (𝑥) ∧ 𝜏 (𝑥, 𝑦), 𝜑𝑛 (𝑦) ∧ 𝛼 (𝑦)                           ⊲ Nondeterministic
 8:    return (𝜑 0, . . . , 𝜑𝑛 )
 9: end function


Algorithm 3 PDR defined by structural induction on partial proofs
Input: Predicates 𝜄 (𝑥), 𝜏 (𝑥, 𝑦), 𝛼 (𝑥) defining linear CHCs
Input: A partial proof 𝜑 0, . . . , 𝜑𝑛 satisfying (4)
Output: A maximally conservative refinement 𝜑 0′ , . . . , 𝜑𝑛′                     ⊲ IndPDR may fail or diverge
  1: function IndPDR(𝜄, 𝜏, 𝛼; 𝜑 0, . . . , 𝜑𝑛 )
  2:    if |= ∃𝑥 .𝜄 (𝑥) ∧ ¬𝛼 (𝑥) then fail
  3:    if 𝜑𝑛 (𝑥) |= 𝛼 (𝑥) then return (𝜑 0, . . . , 𝜑𝑛 )
  4:    while |= ∃𝑥 .∃𝑦.𝜑𝑛−1 (𝑥) ∧ 𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦) do
  5:         let 𝑀 be an assignment such that 𝑀 |= 𝜑𝑛−1 (𝑥) ∧ 𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦)
  6:        𝛾 (𝑥) := 𝜏 (𝑥, 𝑀 (𝑦)) ∧ ¬𝛼 (𝑀 (𝑦))
  7:         (𝜑 0, . . . , 𝜑𝑛−1 ) := IndPDR(𝜄, 𝜏, ¬𝛾; 𝜑 0, . . . , 𝜑𝑛−1 )
  8:    end while
  9:                                                               ⊲ ∃𝑥 .𝜑𝑛−1(𝑥) ∧ 𝜏 (𝑥, 𝑦) |= 𝜑𝑛 (𝑦) ∧ 𝛼 (𝑦) holds
 10:    𝜑𝑛 (𝑦) := interpolation 𝜑𝑛−1 (𝑥) ∧ 𝜏 (𝑥, 𝑦), 𝜑𝑛 (𝑦) ∧ 𝛼 (𝑦)                             ⊲ Nondeterministic
 11:    return (𝜑 0, . . . , 𝜑𝑛 )
 12: end function



where the right-hand-side is the infinite disjunction indexed by concrete values 𝑐. This equivalence
allows us to decompose a single complicated (i.e. quantified) formula into infinitely-many simple
(i.e. quantifier-free) formulas. We reduce the computation of a maximally conservative refinement
satisfying ¬(∃𝑦.𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦)) to iterative computation of maximally conservative refinements
satisfying ¬(𝜏 (𝑥, 𝑐𝑖 ) ∧ ¬𝛼 (𝑐𝑖 )) for 𝑖 = 1, 2, 3, . . ., where {𝑐 1, 𝑐 2, . . . } is an enumeration of values.
    IndPDR (Algorithm 3) is an algorithm based on this idea. As its name suggests, it is closely related
to a family of algorithms known as property-directed reachability. We shall discuss the connection
in the next subsection.
    The loop at lines 4–8 is the computation of a maximally conservative refinement satisfying
¬∃𝑦.𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦). If the algorithm actually computed maximally conservative refinement satis-
fying 𝜏 (𝑥, 𝑐) ∧ ¬𝛼 (𝑐) for all 𝑐, it would never terminate. So IndPDR computes it only for relevant
values. Line 5 chooses a value 𝑀 (𝑦) and line 7 computes a maximally conservative refinement
satisfying ¬(𝜏 (𝑥, 𝑐) ∧ ¬𝛼 (𝑐)) where 𝑐 = 𝑀 (𝑦). Note that this is an over-approximation:
                                 ¬∃𝑦.𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦) |= ¬(𝜏 (𝑥, 𝑐) ∧ ¬𝛼 (𝑐)).

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Software Model-Checking as Cyclic-Proof Search                                                                                               1:17


If the loop terminates, then |= ¬∃𝑥 .∃𝑦.𝜑𝑛−1 (𝑥) ∧ 𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦), which implies 𝜑𝑛−1 (𝑥) |=
¬∃𝑦.𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦) as expected.
   We prove the correctness.
   Lemma 6.5. Let (𝜑𝑖 )0≤𝑖 ≤𝑛 be a partial proof and let 𝛼 1, 𝛼 2 be formulas such that 𝛼 2 (𝑥) |= 𝛼 1 (𝑥). Sup-
pose that (𝜑𝑖′)0≤𝑖 ≤𝑛 is a maximally conservative refinement of (𝜑𝑖 )𝑖 satisfying 𝛼 1 and that (𝜑𝑖′′)0≤𝑖 ≤𝑛
is a maximally conservative refinement of (𝜑𝑖′)0≤𝑖 ≤𝑛 satisfying 𝛼 2 . Then (𝜑𝑖′′)𝑖 is a maximally conser-
vative refinement of (𝜑𝑖 )𝑖 satisfying 𝛼 2 .
   Proof. Assume a 𝑘-conservative refinement (𝜓𝑖 )0≤𝑖 ≤𝑛 of (𝜑𝑖 )𝑖 satisfying 𝛼 2 . It suffices to show
that (𝜑𝑖′′)𝑖 is also 𝑘-conservative. Since 𝛼 2 (𝑥) |= 𝛼 1 (𝑥), the partial proof (𝜓𝑖 )𝑖 is also a refinement of
(𝜑𝑖 )𝑖 satisfying 𝛼 1 . Since (𝜑𝑖′)𝑖 is maximally conservative, it is 𝑘-conservative. Then (𝜓𝑖 ∧ 𝜑𝑖′)0≤𝑖 ≤𝑛
is a 𝑘-conservative refinement of (𝜑𝑖′)𝑖 satisfying 𝛼 1 . By the maximal conservativity of (𝜑𝑖′′)𝑖 , it is
𝑘-conservative as well.                                                                                      □
   Lemma 6.6. If IndPDR terminates, it returns a maximally conservative refinement.
   Proof. Let (𝜓𝑖 )0≤𝑖 ≤𝑛 be the initial value of (𝜑𝑖 )0≤𝑖 ≤𝑛 and (𝜓𝑖′)0≤𝑖 ≤𝑛 be the value of (𝜑𝑖 )𝑖 at the end
of the loop (or, equivalently, line 9). It suffices to show that (𝜓𝑖′)0≤𝑖 ≤𝑛−1 is a maximally conservative
refinement of (𝜓𝑖 )0≤𝑖 ≤𝑛−1 satisfying ¬∃𝑦.𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦). Clearly 𝜓𝑛−1   ′ (𝑥) |= ¬∃𝑦.𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦)

since the condition in line 4 is false for the values at line 9. The maximal conservativity can be
proved by induction on the number of iterations using Lemma 6.5 since ¬∃𝑦.𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦) |=
¬(𝜏 (𝑥, 𝑐) ∧ ¬𝛼 (𝑐)) for every 𝑐.                                                                             □
   Other properties of IndPDR shall be discussed below.

6.5    PDR vs. IndPDR as a transition system
Property-directed reachability (or PDR) refers to the IC3 algorithm [Bradley 2011; Een et al. 2011]
and its derivatives [Beyer and Dangl 2020; Birgmeier et al. 2014; Cimatti and Griggio 2012; Cimatti
et al. 2014; Hoder and Bjørner 2012; Komuravelli et al. 2014, 2013]. This section compares PDR and
Impact/mc, in particular Impact/mc with IndPDR. Since PDR is formalized as an abstract transition
system in [Hoder and Bjørner 2012], we give a transition system corresponding to Impact/mc and
compare it with the transition system in [Hoder and Bjørner 2012].
   IndPDR as a transition system. An abstract transition system for IndPDR can be derived by the
following argument. The starting point is operational semantics of the program IndPDR. Since
IndPDR is a recursive program, a configuration in the operational semantics consists of the current
assignment to variables and the call-stacks. So a configuration can be written as
   (𝛼 ′; 𝜑 0, . . . , 𝜑𝑘−1 )■(𝑀 𝑘 , 𝛼 𝑘 ; 𝜑 0𝑘 , . . . , 𝜑𝑘𝑘 ) (𝑀 𝑘+1, 𝛼 𝑘+1 ; 𝜑 0𝑘+1, . . . , 𝜑𝑘+1
                                                                                                𝑘+1
                                                                                                    ) . . . (𝑀 𝑛 , 𝛼 𝑛 ; 𝜑 0𝑛 , . . . , 𝜑𝑛𝑛 ),
where the left-hand-side of ■ is the current variable assignment and the right-hand-side is the call-
stack. An abstract transition system can be obtained by using this representation of the call-stack.
                                                                                     ℓ in the frame (𝑀 ℓ , 𝛼 ℓ ; 𝜑 ℓ , . . . , 𝜑 ℓ )
   This representation, however, has redundancy. First forgetting 𝜑 0ℓ , . . . , 𝜑 ℓ−1                             0            ℓ
does not cause any problem, since they shall be overwritten when the control will come back
to the frame. Second 𝛼 ℓ is redundant: 𝛼 𝑛 = 𝛼 and 𝛼 ℓ (𝑥) = (𝜏 (𝑥, 𝑀 ℓ+1 (𝑦)) ∧ ¬𝛼 ℓ+1 (𝑀 ℓ+1 (𝑦))) for
ℓ = 𝑛 − 1, . . . , 𝑘. Third 𝛼 ′ = (𝜏 (𝑥, 𝑀 𝑘 (𝑦)) ∧ ¬𝛼 𝑘 (𝑀 𝑘 (𝑦))). Fourth 𝑀 ℓ (𝑥) is not used. So we obtain a
compact representation:
                                      (𝑀 𝑘 (𝑦) . . . 𝑀 𝑛 (𝑦) ∥ 𝜑 0 . . . 𝜑𝑘−1𝜑𝑘𝑘 𝜑𝑘+1
                                                                                  𝑘+1
                                                                                      . . . 𝜑𝑛𝑛 ).
Figure 5 defines the abstract transition system corresponding to IndPDR, which is the operational
semantics of IndPDR with the above representation of configurations.

                                       Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:18                                                                                     Takeshi Tsukada and Hiroshi Unno


                                          |= 𝜑𝑛 (𝑐) ∧ ¬𝛼 (𝑐)
                                                                           (Candidate)
                                (𝜖 ∥ 𝜑 0 . . . 𝜑𝑛 ) −→ (𝑐 ∥ 𝜑 0 . . . 𝜑𝑛 )

                                 |= ¬𝜄 (𝑐𝑘 )         |= 𝜑𝑘−1 (𝑐 ′) ∧ 𝜏 (𝑐 ′, 𝑐𝑘 )
                                                                                          (Decide)
                        (𝑐𝑘 . . . 𝑐𝑛 ∥ 𝜑 0 . . . 𝜑𝑛 ) −→ (𝑐 ′𝑐𝑘 . . . 𝑐𝑛 ∥ 𝜑 0 . . . 𝜑𝑛 )

                         𝜑𝑘−1 (𝑥) ∧ 𝜏 (𝑥, 𝑦) |= 𝜓 (𝑦)           𝜓 (𝑥) |= 𝑥 ≠ 𝑐𝑘
                                                                                                   (Conflict)
         (𝑐𝑘 . . . 𝑐𝑛 ∥ 𝜑 0 . . . 𝜑𝑛 ) −→ (𝑐𝑘+1 . . . 𝑐𝑛 ∥ 𝜑 0 . . . 𝜑𝑘−1 (𝜑𝑘 ∧ 𝜓 )𝜑𝑘+1 . . . 𝜑𝑛 )
                                       Fig. 5. The transition rules for IndPDR.


   The above argument shows the following proposition.
  Proposition 6.7. IndPDR(𝜄, 𝜏, 𝛼; 𝜑 0, . . . , 𝜑𝑛 ) may return (𝜑 0′ , . . . , 𝜑𝑛′ ) if and only if (𝜖 ∥ 𝜑 0, . . . , 𝜑𝑛 ) −→∗
(𝜖 ∥ 𝜑 0′ , . . . , 𝜑𝑛′ ) with 𝜑𝑛′ (𝑥) |= 𝛼 (𝑥).                                                                         □
  Before comparing the transition system with PDR, we prove a part of the correctness of IndPDR
using the transition system.
   Lemma 6.8. If (𝜑𝑖′)0≤𝑖 ≤𝑛 is a maximally conservative refinement of (𝜑𝑖 )0≤𝑖 ≤𝑛 , then
                                        (𝜖 ∥ 𝜑 0 . . . 𝜑𝑛 ) −→∗ (𝜖 ∥ 𝜑 0′ . . . 𝜑𝑛′ ).
  Proof. Assume that (𝜑𝑖′)0≤𝑖 ≤𝑛 is a maximally conservative refinement of (𝜑𝑖 )0≤𝑖 ≤𝑛 satisfying 𝛼.
Let 𝑘 be the natural number such that 𝜑𝑘′ = 𝜑𝑘 but 𝜑𝑘+1
                                                    ′   ≠ 𝜑𝑘+1 . For 𝑖 = 𝑘 + 2, . . . , 𝑛, we define 𝜓𝑖 by
                                        𝜑𝑘+1 ⇝ 𝜓𝑘+2 ⇝ 𝜓𝑘+3 ⇝ · · · ⇝ 𝜓𝑛
where ⇝ is the precise symbolic computation. Then (𝜑 0, . . . , 𝜑𝑘+1,𝜓𝑘+2, . . . ,𝜓𝑛 ) satisfies the require-
ments for refinement except for 𝜓𝑛 (𝑥) |= 𝛼 (𝑥). By the maximal conservativity of (𝜑𝑖′)𝑖 , we know
that (𝜑 0, . . . , 𝜑𝑘+1,𝜓𝑘+2, . . . ,𝜓𝑛 ) is not a refinement satisfying 𝛼, and thus |= 𝜓𝑛 (𝑐𝑛 ) ∧ ¬𝛼 (𝑐𝑛 ) for
some 𝑐𝑛 . Hence we have a sequence (𝑐𝑘+1, . . . , 𝑐𝑛 ) of values such that |= 𝜑𝑘+1 (𝑐𝑘+1 ) and |= 𝜏 (𝑐𝑖 , 𝑐𝑖+1 )
for every 𝑖 = 𝑘 + 1, . . . , 𝑛 − 1. So we have the following transition sequence:
        (𝜖 ∥ 𝜑 0 . . . 𝜑𝑛 ) −→∗ (𝑐𝑘+1 . . . 𝑐𝑛 ∥ 𝜑 0 . . . 𝜑𝑛 ) −→ (𝑐𝑘+2 . . . 𝑐𝑛 ∥ 𝜑 0 . . . 𝜑𝑘 𝜑𝑘+1
                                                                                                  ′
                                                                                                      𝜑𝑘+2 . . . 𝜑𝑛 )
                                          ′    ′                                         ′    ′
        −→ (𝑐𝑘+3 . . . 𝑐𝑛 ∥ 𝜑 0 . . . 𝜑𝑘 𝜑𝑘+1 𝜑𝑘+2 𝜑𝑘+3 . . . 𝜑𝑛 ) −→ (𝜖 ∥ 𝜑 0 . . . 𝜑𝑘 𝜑𝑘+1 𝜑𝑘+2 · · · 𝜑𝑛′ ).
                                                                                                                        □
  Corollary 6.9. The set of possible return values of IndPDR coincides with the set of all maximally
conservative refinements.
   Definition of PDR. We review PDR following Hoder and Bjørner [Hoder and Bjørner 2012]. Here
we introduce a simplified version, which we call simplified PDR (sPDR); see Remark 4 for the
differences. A configuration is of the form (𝑐𝑘 . . . 𝑐𝑛 ∥ 𝐹 0 𝐹 1 . . . 𝐹𝑛 ), consisting of two sequences of
(candidate) counterexamples 𝑐𝑖 ∈ S and frames 𝐹𝑖 ,8 which are formulas denoting unary predicates.
We call 𝑐𝑖 (resp. 𝐹𝑖 ) the counterexample (resp. the frame) at level 𝑖. Note that counterexamples are
associated to only higher levels and that the counterexample sequence can be empty 𝜖. Intuitively
a frame 𝐹𝑖 at level 𝑖 denotes an over-approximation of states of distance ≤ 𝑖 and 𝑐𝑖 together with
                                                                                    Ó
𝑐𝑖+1 . . . 𝑐𝑛 is a witness of unsafety of 𝐹𝑖 with bound (𝑛 − 𝑖), i.e. 𝐹𝑖 (𝑐𝑖 ) and 𝑛−1 𝑗=𝑖 𝜏 (𝑐 𝑗 , 𝑐 𝑗+1 ) ∧ ¬𝛼 (𝑐 𝑛 ).
Formally each configuration (𝑐𝑘 . . . 𝑐𝑛 ∥ 𝐹 0 . . . 𝐹𝑛 ) must satisfy (a) 𝐹 0 = 𝜄, (b) 𝐹𝑖 (𝑥) ∨ F (𝐹𝑖 ) (𝑥) |=
8 We do not use metavariables 𝜑 and 𝜓 for frames, because a frame does not precisely correspond to a cut-formula. See a

discussion below.


Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Software Model-Checking as Cyclic-Proof Search                                                                        1:19


                                        |= 𝐹𝑛 (𝑐) ∧ ¬𝛼 (𝑐)
                                                                         (Candidate/sPDR)
                           (𝜖 ∥ 𝐹 0 . . . 𝐹𝑛 ) −→pdr (𝑐 ∥ 𝐹 0 . . . 𝐹𝑛 )

                                       |= 𝐹𝑘−1 (𝑐 ′) ∧ 𝜏 (𝑐 ′, 𝑐𝑘 )
                                                                                        (Decide/sPDR)
                   (𝑐𝑘 . . . 𝑐𝑛 ∥ 𝐹 0 . . . 𝐹𝑛 ) −→pdr (𝑐 ′𝑐𝑘 . . . 𝑐𝑛 ∥ 𝐹 0 . . . 𝐹𝑛 )
                                      
𝜄 (𝑦) ∨ ∃𝑥 .𝐹𝑘−1 (𝑥) ∧ 𝜏 (𝑥, 𝑦)) |= 𝜓 (𝑦)              𝐹𝑘−1 (𝑥) |= 𝜓 (𝑥)            𝜓 (𝑥) |= 𝑥 ≠ 𝑐𝑘
                                                                                                    (Conflict/sPDR)
    (𝑐𝑘 . . . 𝑐𝑛 ∥ 𝐹 0 . . . 𝐹𝑛 ) −→pdr (𝑐𝑘+1 . . . 𝑐𝑛 ∥ 𝐹 0 . . . 𝐹𝑘−1 (𝐹𝑘 ∧ 𝜓 )𝐹𝑘+1 . . . 𝐹𝑛 )
Fig. 6. A simplified version of the transition rules for PDR in [Hoder and Bjørner 2012]; see Remark 4 for
the differences. We omit (Unfold), (Initialize), (Valid) and (Model), as these rules are not a part of the
refinement/interpolation process. These rules corresponds the content described in Definition 6.10.


𝐹𝑖+1 (𝑥) forÓevery 0 ≤ 𝑖 ≤ 𝑛,9 (c) 𝐹𝑖 (𝑥) |= 𝛼 (𝑥) for every 0 ≤ 𝑖 < 𝑛, (d) |= 𝐹𝑖 (𝑐𝑖 ) for every 𝑘 ≤ 𝑖 ≤ 𝑛,
and (e) |= 𝑛−1𝑖=𝑘 𝜏 (𝑐 𝑖 , 𝑐 𝑖+1 ) ∧ ¬𝛼 (𝑐 𝑛 ).
   The transition rules are given in Figure 6. The rule (Unfold) is applicable when 𝐹 0 = 𝜄 has been
confirmed safe with bound 𝑛. This rule starts to check if 𝜄 is safe with bound (𝑛 + 1), by extending
the frame by ⊤. (Candidate) is applicable when a state 𝑐𝑛 satisfying 𝐹𝑛 violates the assertion 𝛼
and starts to check if the bad state 𝑐𝑛 is 𝑛-step reachable from 𝜄. The candidate counterexample is
propagated backward by (Decide) rule. If (Decide) is not applicable, the candidate is spurious, i.e. it
was introduced by the approximation at this level. Then (Conflict) refines the approximation,
strengthening 𝐹𝑘 so that it does not contain the spurious counterexample 𝑐𝑘 (i.e. 𝜓 (𝑥) |= 𝑥 ≠ 𝑐𝑘 ).
   Definition 6.10 (Simplified PDR). The algorithm sPDR is defined as follows. It starts from the
initial configuration (𝜖 ∥ 𝜄). The algorithm iteratively rewrites the configuration. If it reaches
(𝜖 ∥ 𝐹 0 . . . 𝐹𝑛 ) with 𝐹 ℓ (𝑥) |= 𝐹 ℓ−1 (𝑥) for some ℓ, then the program is safe and an invariant is 𝐹 ℓ . If it
reaches (𝑐 0 . . . 𝑐𝑛 ∥ 𝐹 0 . . . 𝐹𝑛 ) with a counterexample at level 0, the program is unsafe. If it reaches
(𝜖 ∥ 𝐹 0 . . . 𝐹𝑛 ) with 𝐹𝑛 (𝑥) |= 𝛼, then it moves to 𝜖 ∥ 𝐹 0 . . . 𝐹𝑛 ⊤).                                     □
   sPDR vs. Impact/mc with IndPDR. sPDR in Figure 6 is essentially the same as Impact/mc with
IndPDR. Consider the relation ≈ between configurations of IndPDR and of sPDR defined by
                                                                               Ô
 (𝑐𝑘 . . . 𝑐𝑛 ∥ 𝜑 0 . . . 𝜑𝑛 ) ≈ (𝑐𝑘 . . . 𝑐𝑛 ∥ 𝐹 0 . . . 𝐹𝑛 ) iff |= 𝐹 𝑗 (𝑥) ⇔ 0≤𝑖 ≤ 𝑗 𝜑𝑖 (𝑥) for every 0 ≤ 𝑗 ≤ 𝑛
This relation ≈ is a bisimilation.
   Theorem 6.11. Suppose that (®𝑐 ∥ 𝜑)
                                    ® ≈ (® 𝑐 ∥ 𝐹®). If (®
                                                        𝑐 ∥ 𝜑)
                                                            ® −→ (®                   𝑐 ∥ 𝐹®) −→pdr
                                                                   𝑐 ′ ∥ 𝜑® ′), then (®
 𝑐 ′ ∥ 𝐹®′) and (®
(®                              𝑐 ′, ∥ 𝐹®′) for some (®
                 𝑐 ′ ∥ 𝜑® ′) ≈ (®                     𝑐 ′ ∥ 𝐹®′). Conversely, if (®
                                                                                  𝑐 ∥ 𝐹®) −→
                                                                                       𝑐 ′ ∥ 𝐹®′), then
                                                                                  pdr (®
(®
 𝑐 ∥ 𝜑)
     ® −→ (®′    ′
           𝑐 ∥ 𝜑® ) and (®′    ′     𝑐 ∥ 𝐹® ) for some (®
                         𝑐 ∥ 𝜑® ) ≈ (®′    ′              ′    ′
                                                         𝑐 ∥ 𝜑® ).
   Proof. This is intuitively clear as each rule has a counterpart, but we need some care to establish
the precise correspondence.
   (Candidate/sPDR) can be simulated by (Candidate). To see this, we have to check     Ô       that |=
𝐹𝑛 (𝑐) ∧ ¬𝛼 (𝑐) implies |= 𝜑𝑛 (𝑐) ∧ ¬𝛼 (𝑐). This follows from the assumption 𝐹𝑛 (𝑥) ⇔ 0≤𝑖 ≤𝑛 𝜑𝑖 (𝑥)
and 𝜑𝑖 (𝑥) |= 𝛼 (𝑥) for 𝑖 < 𝑛. The conserve is trivial because 𝜑𝑛 (𝑥) |= 𝐹𝑛 (𝑥).
   The correspondence of (Decide/sPDR) and (Decide) can be show similarly.
   It is easy to see that (Conflict) with interpolation 𝜓 coincides with (Conflict/sPDR) with the
same interpolation 𝜓 .                                                                               □

9 F is the predicate transformer given by F (𝐹 ) (𝑦) := 𝜄 (𝑦) ∨ ( ∃𝑥 .𝐹 (𝑥) ∧ 𝜏 (𝑥, 𝑦)).



                                    Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:20                                                                                  Takeshi Tsukada and Hiroshi Unno


Remark 4. sPDR defined by Figure 6 differs from that by Hoder and Bjørner [Hoder and Bjørner
2012], which has an additional rule (Induction/PDR) and a slightly weaker condition for the
interpolants as in (Conflict/PDR) below:
                                                                      
                      𝜄 (𝑦) ∨ ∃𝑥 .(𝐹 ℓ−1 (𝑥) ∧ 𝜓 (𝑥)) ∧ 𝜏 (𝑥, 𝑦)) |= 𝜓 (𝑦)
                                                                                                    (Induction/PDR)
     (𝑐𝑘 . . . 𝑐𝑛 ∥ 𝐹 0 . . . 𝐹𝑛 ) −→pdr (𝑐𝑘 . . . 𝑐𝑛 ∥ (𝐹 0 ∧ 𝜓 ) . . . (𝐹 ℓ ∧ 𝜓 )𝐹 ℓ+1 . . . 𝐹𝑛 )
                                                    
                𝜄 (𝑦) ∨ ∃𝑥 .𝐹𝑘−1 (𝑥) ∧ 𝜏 (𝑥, 𝑦)) |= 𝜓 (𝑦)             𝜓 (𝑥) |= 𝑥 ≠ 𝑐𝑘
                                                                                                      (Conflict/PDR)
    (𝑐𝑘 . . . 𝑐𝑛 ∥ 𝐹 0 . . . 𝐹𝑛 ) −→pdr (𝑐𝑘+1 . . . 𝑐𝑛 ∥ (𝐹 0 ∧ 𝜓 ) . . . (𝐹𝑘 ∧ 𝜓 )𝐹𝑘+1 . . . 𝐹𝑛 )
Notice that, in order to keep the monotonicity 𝐹𝑖 (𝑥) |= 𝐹𝑖+1 (𝑥), we have to conjoin 𝜓 to 𝐹 𝑗
(0 ≤ 𝑗 < 𝑘) as well. This version of PDR coincides with an extension of IndPDR by the following
rule corresponding to (Induction/PDR):
      𝜄 (𝑦) |= 𝜓 (𝑦)         ∃𝑥 .(𝜑𝑖 (𝑥) ∧ 𝜓 (𝑥)) ∧ 𝜏 (𝑥, 𝑦) |= 𝜓 (𝑦) for 𝑖 = 0, 1, . . . , ℓ − 1
                                                                                                     (Induction)
         (𝑐𝑘 . . . 𝑐𝑛 ∥ 𝜑 0 . . . 𝜑𝑛 ) −→ (𝑐𝑘 . . . 𝑐𝑛 ∥ (𝜑 0 ∧ 𝜓 ) . . . (𝜑 ℓ ∧ 𝜓 )𝜑 ℓ+1 . . . 𝜑𝑛 )
See Appendix B for the details.                                                                                         □
Remark 5. A similarity between PDR and McMillan’s lazy abstraction with interpolants was already
recognized as in [Cimatti and Griggio 2012; Een et al. 2011]. They pointed out that a multi-step
transition (𝜖 ∥ 𝜑 0 . . . 𝜑𝑛−1 ⊤) −→∗ (𝜖 ∥ 𝜑 0′ . . . 𝜑𝑛−1
                                                       ′ 𝜑 ′ ) (with 𝜑 ′ (𝑥) |= 𝛼 (𝑥)) is indeed a calculation
                                                           𝑛          𝑛
of an interpolant. Hence PDR “can be seen as an instance of the lazy abstraction with interpolants
algorithm of [McMillan 2006], in which however interpolants are constructed in a very different
way” [Cimatti and Griggio 2012]. Here we further investigate the connection, giving a complete
characterization of interpolants given by PDR (Theorem 6.11). To the best of our knowledge, this is
the first declarative characterization of interpolants computed by PDR.
   The maximal conservativity heuristic and a naïve algorithm for computing a maximally con-
servative interpolant (Algorithm 1) can be found in [Vizel and Gurfinkel 2014] (called min-suffix
heuristic), which aims to combine the interpolation-based approach and PDR. This paper differs
from the work in the following points. First this paper formally proves that Impact with the
maximal conservativity heuristic is essentially the same as PDR, whereas [Vizel and Gurfinkel
2014] regards it as a heuristic for interpolation-based model-checkers and does not establish its
formal connection to PDR. Second, this paper also analyzes other algorithms from the view point
of maximal conservativity (see Section 7).                                                                   □

6.6    Application: Making PDR refutationally complete by model-based projection
In contrast to the naïve algorithm NaïveMCR (Algorithm 1), which always terminates, IndPDR
(Algorithm 3) may diverge. Therefore Impact/mc with IndPDR does not have refutational com-
pleteness because, even if an input program (or an input linear CHC system) has an error path of
length 𝑛, the backend solver IndPDR may diverge during the construction of a proof of the safety
of the program within (𝑛 − 1) steps.
   This subsection develops a variant of PDR with refutational completeness, in order to demonstrate
the usefulness of our logical analysis of PDR. To the best of our knowledge, the algorithm developed
here is the first PDR for software model-checking with refutational completeness.10
   IndPDR may diverge because the loop starting from line 4 in Algorithm 3 may continue indefi-
nitely. Let
                     BadReachable𝑛 := { 𝑐 | |= ∃𝑥 .𝜑𝑛−1 (𝑥) ∧ 𝜏 (𝑥, 𝑐) ∧ ¬𝛼 (𝑐) }
10 An expert of software model-checking may point out that RecMC [Komuravelli et al. 2014, 2016], the algorithm of Spacer,

is a variant of PDR with refutational completeness. Although a proof sketch of refutational completeness of RecMC is given
in [Komuravelli et al. 2016], we found a counterexample, which shall be discussed at the end of this subsection.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Software Model-Checking as Cyclic-Proof Search                                                                   1:21


be the set of bad states that is reachable from 𝜑𝑛−1 in one step. In each loop, IndPDR chooses a state
𝑀 (𝑦) = 𝑐 ∈ BadRechable𝑛 and tries to refine the immediate subproof 𝜑 0, . . . , 𝜑𝑛−1 to ensure that 𝑐
is in fact unreachable. BadReachable𝑛 decreases in each iteration, and the loop terminates when
BadReachable𝑛 becomes empty. In the worst case, each loop removes only one element, namely the
chosen element 𝑐, from BadReachable𝑛 . Hence, if BadReachable𝑛 is infinite, infinite iteration of the
loop may be required to make BadReachable𝑛 empty. This divergent behavior has been observed in
[Komuravelli et al. 2014] for a variant of PDR known as GPDR [Hoder and Bjørner 2012].
   From a logical point of view, this phenomenon can be explained as follows. Recall that the aim
of IndPDR is to remove the quantification from ∃𝑦.𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦) in IndMCR (Algorithm 2). The
idea is to replace the variable 𝑦 with a concrete value, and the point is the logical equivalence
                                                          Ü                      
                        ∃𝑦.𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦)      ⇔            𝜏 (𝑥, 𝑐) ∧ ¬𝛼 (𝑐)                   (8)
                                                                  𝑐

where the right-hand-side is the infinite disjunction. This allows us to decompose a quantified
formula ∃𝑦.𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦) into an infinite collection of quantifier-free formulas 𝜏 (𝑥, 𝑐) ∧ ¬𝛼 (𝑐).
So the essence of IndPDR is a decomposition of a single hard query into infinitely many tractable
queries, and the infinity causes divergence in the worst case.
  Model-based projection [Komuravelli et al. 2014] was introduced to overcome the problem.
  Definition 6.12 (Model-based projection [Komuravelli et al. 2014]). Let 𝜑 (𝑥,
                                                                             ® 𝑦)
                                                                                ® be a quantifier-free
formula. A function MBP (𝜑, {𝑦},  ® −) from models 𝑀 of 𝜑 (i.e. assignments for 𝑥® and 𝑦® such that
𝑀 |= 𝜑) to quantifier-free formulas 𝜓𝑀 = MBP (𝜑, {𝑦},   ® 𝑀) with fv(𝜓𝑀 ) ⊆ {𝑥®} is a model-based
projection for 𝜑 with respect to 𝑦® if it satisfies
                               Ü
              ∃®𝑦.𝜑 (𝑥,
                     ® 𝑦)
                        ® ⇔          𝜓𝑀 (𝑥)®        and 𝑀 |= 𝜓𝑀 (𝑥)
                                                                 ® for every model 𝑀                (9)
                                𝑀 |=𝜑

and furthermore the image {𝜓𝑀 | 𝑀 |= 𝜑 } is finite. We assume that a model-based projection exists
for every pair of 𝜑 and 𝑦® in the constraint language.                                          □
   The condition (9) is an abstraction of the property of the mapping Subst (𝜑 (𝑥,   ® 𝑦),
                                                                                        ® {𝑦},
                                                                                            ® 𝑀) :=
𝜑 (𝑥,
   ® 𝑀 (𝑦)),
         ® so model-based projection is a generalization of the decomponition
                                                                      Ô             in Equation    8. A
significant difference is the finiteness of the image: the disjunction 𝑀 |=𝜑 𝜓𝑀 (𝑥)
                                                                                 ® is actually a finite
disjunction.
   By using our inductive description of PDR, it is surprisingly easy to incorporate model-based
projection into IndPDR: we simply replace the substitution 𝜏 (𝑥, 𝑀 (𝑦)) ∧ ¬𝛼 (𝑀 (𝑦)) of the value
𝑀 (𝑦) for 𝑦 (line 6 in Algorithm 3) with model-based projection MBP (𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦), {𝑦}, 𝑀). The
resulting algorithm, which we call IndPDR/mbp, is shown in Algorithm 4.
  Theorem 6.13. IndPDR/mbp always terminates.
  Proof. We prove the claim by induction on 𝑛. If 𝑛 = 0, then 𝜑 0 = 𝜑𝑛 = 𝜄 by (4). Since
                ¬(∃𝑥 .𝜄 (𝑥) ∧ ¬𝛼 (𝑥))      iff ∀𝑥 .𝜄 (𝑥) ⇒ 𝛼 (𝑥)        iff ∀𝑥 .𝜑𝑛 (𝑥) ⇒ 𝛼 (𝑥),
RecPDR-MBP fails in line 2 or returns a value in line 3.
   Assume that 𝑛 > 0. By the induction hypothesis, the recursive call in line 7 terminates. It suffices
to show the termination of the loop starting from line 4.
   Assume for contradiction that the loop continues indefinitely. For each 𝑖 = 1, 2, . . ., let 𝑀𝑖 and 𝛾𝑖
be 𝑀 and 𝛼 ′ in the 𝑖-th loop and 𝜓𝑖 be 𝜑𝑛−1 at the end of the 𝑖-th loop. By construction, we have
                          𝑀𝑖 |= 𝜓𝑖−1 (𝑥) ∧ 𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑥)          and 𝑀𝑖 |= 𝛾𝑖 (𝑥)

                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:22                                                                                Takeshi Tsukada and Hiroshi Unno


Algorithm 4 Inductive PDR with model-based projection
Input: Predicates 𝜄 (𝑥), 𝜏 (𝑥, 𝑦), 𝛼 (𝑥) defining linear CHCs
Input: A valid partial proof 𝜑 0, . . . , 𝜑𝑛 satisfying (4)
Output: Maximally conservative refinement 𝜑 0′ , . . . , 𝜑𝑛′                        ⊲ RecPDR-MBP may fail
  1: function IndPDR/mbp(𝜄, 𝜏, 𝛼; 𝜑 0, . . . , 𝜑𝑛 )
  2:    if |= ∃𝑥 .𝜄 (𝑥) ∧ ¬𝛼 (𝑥) then fail
  3:    if 𝜑𝑛 (𝑥) |= 𝛼 (𝑥) then return (𝜑 0, . . . , 𝜑𝑛 )
  4:    while |= ∃𝑥 .∃𝑦.𝜑𝑛−1 (𝑥) ∧ 𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦) do
  5:         let 𝑀 be an assignment such that 𝑀 |= 𝜑𝑛−1 (𝑥) ∧ 𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦)
  6:        𝛾 (𝑥) := MBP (𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦), {𝑦}, 𝑀)
  7:         (𝜑 0, . . . , 𝜑𝑛−1 ) := IndPDR/mbp(𝜄, 𝜏, ¬𝛾; 𝜑 0, . . . , 𝜑𝑛−1 )
  8:    end while
  9:                                                         ⊲ ∃𝑥 .𝜑𝑛−1(𝑥) ∧ 𝜏 (𝑥, 𝑦) |= 𝜑𝑛 (𝑦) ∧ 𝛼 (𝑦) holds
 10:    𝜑𝑛 (𝑦) := interpolation 𝜑𝑛−1 (𝑥) ∧ 𝜏 (𝑥, 𝑦), 𝜑𝑛 (𝑦) ∧ 𝛼 (𝑦)                       ⊲ Nondeterministic
 11:    return 𝜑®
 12: end function



                                                                         (Candidate/mbp)
                            (𝜖 ∥ 𝜑 0 . . . 𝜑𝑛 ) −→ (𝛼 ∥ 𝜑 0 . . . 𝜑𝑛 )

                   |= ¬∃𝑥 .𝜄 (𝑥) ∧ 𝛾𝑘 (𝑥) 𝑀 |= 𝜑𝑘−1 (𝑥) ∧ 𝜏 (𝑥, 𝑦) ∧ 𝛾𝑘 (𝑦)
                            𝛾𝑘−1 (𝑥) = MBP (𝜏 (𝑥, 𝑦) ∧ 𝛾𝑘 (𝑦), {𝑦}, 𝑀)
                                                                                       (Decide/mbp)
                    (𝛾𝑘 . . . 𝛾𝑛 ∥ 𝜑 0 . . . 𝜑𝑛 ) −→ (𝛾𝑘−1𝛾𝑘 . . . 𝛾𝑛 ∥ 𝜑 0 . . . 𝜑𝑛 )

                       𝜑𝑘−1 (𝑥) ∧ 𝜏 (𝑥, 𝑦) |= 𝜓 (𝑦)         𝜓 (𝑥) |= ¬𝛾𝑘 (𝑥)
                                                                                                 (Conflict/mbp)
       (𝛾𝑘 . . . 𝛾𝑛 ∥ 𝜑 0 . . . 𝜑𝑛 ) −→ (𝛾𝑘+1 . . . 𝛾𝑛 ∥ 𝜑 0 . . . 𝜑𝑘−1 (𝜑𝑘 ∧ 𝜓 )𝜑𝑘+1 . . . 𝜑𝑛 )
                        Fig. 7. The transition rules for PDR with model-based projection.


for each 𝑖 = 1, 2, . . .. By the definition of refinement,
                                   𝜓𝑖 (𝑥) |= ¬𝛾𝑖 (𝑥)      and 𝜓𝑖 (𝑥) |= 𝜓𝑖−1 (𝑥)
                                                                                                      
where 𝜓 0 is 𝜑𝑛−1 before the loop. Suppose 𝑖 < 𝑗. Since 𝑀 𝑗 |= 𝜓 𝑗−1 (𝑥) and ∀𝑘. 𝜓𝑘 (𝑥) |= 𝜓𝑘−1 (𝑥) , we
have 𝑀 𝑗 |= 𝜓𝑖 (𝑥). Hence 𝑀 𝑗 |= ¬𝛾𝑖 (𝑥) since𝜓𝑖 (𝑥) |= ¬𝛾𝑖 (𝑥). As 𝑀𝑖 |= 𝛾𝑖 (𝑥), we have 𝛾𝑖 (𝑥) ≠ 𝛾 𝑗 (𝑥) if
𝑖 < 𝑗. This contradicts the finiteness assumption of MBP since 𝛾𝑖 (𝑥) = MBP (𝜏 (𝑥, 𝑦)∧¬𝛼 (𝑦), {𝑦}, 𝑀𝑖 )
and the formula 𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦) is a constant in the loop.                                               □

    It is not difficult to give an abstract transition system corresponding to IndPDR/mbp (Algorithm 4).
It is shown in Figure 7.
Subtlety of model-based projection. Algorithms using MBP should be carefully designed. For example,
let IndPDR/mbp’ be the algorithm obtained by replacing line 6 of IndPDR/mbp with
                            𝛾 (𝑥) := MBP (𝜑𝑛−1 (𝑥) ∧ 𝜏 (𝑥, 𝑦) ∧ ¬𝛼 (𝑦), {𝑦}, 𝑀).
This small change breaks the termination property of the algorithm. This is because 𝜑𝑘−1 (𝑥) is
changed in each iteration of the loop; hence a different iteration calculates model-based projection
of different formulas. In this case, the finiteness property of model-based projection does not help,
since the finiteness is ensured only if model-based projection is applied to a single formula.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Software Model-Checking as Cyclic-Proof Search                                                                      1:23


   We give a small toy example to prove that IndPDR/mbp’ may diverge. Let us consider the
following unsatisfiable linear CHC system
           𝑆 = { 𝑥 = 0 ⇒ 𝑃 (𝑥), 𝑃 (𝑥) ∧ (𝑦 = 𝑥 + 1 ∨ 𝑦 = 1 − 2𝑥) ⇒ 𝑃 (𝑦), 𝑃 (𝑥) ⇒ 𝑥 ≤ 2 },
so 𝜄 (𝑥) = (𝑥 = 0), 𝜏 (𝑥, 𝑦) = (𝑦 = 𝑥 + 1 ∨𝑦 = 1 − 2𝑥) and 𝛼 (𝑥) = (𝑥 ≤ 2). Let 𝜑 0 = 𝜄, 𝜑 1 (𝑥) = (𝑥 ≤ 1)
and 𝜑 2 (𝑥) = ⊤. Then (𝜑 0, 𝜑 1, 𝜑 2 ) has a refinement, e.g. (𝑥 = 0, 𝑥 = 1, 𝑥 ≤ 2). Let MBP be an arbitrary
model-based projection method. We define MBP ′ by
                                (
        ′                         𝑥 =𝑚                        if 𝑀 (𝑥) = 𝑚 = max{𝑛 < 0 | |= ∃𝑦.𝜓 (𝑛, 𝑦)}
 MBP (𝜓 (𝑥, 𝑦), {𝑦}, 𝑀) :=
                                  MBP (𝜓 (𝑥, 𝑦), {𝑦}, 𝑀) otherwise.

We also assume that
                                     interpolation(𝜓 (𝑥, 𝑦), 𝜗 (𝑦)) := 𝜗 (𝑦).
Then IndPDR/mbp′ (𝜄, 𝜏, 𝛼; 𝜑 0, 𝜑 1, 𝜑 2 ) diverges, provided that the model 𝑀𝑖 in the 𝑖-th iteration,
𝑖 = 1, 2, . . ., of the loop is (𝑀𝑖 (𝑥), 𝑀𝑖 (𝑦)) = (−𝑖, 1 + 2𝑖). Then 𝜑 1 at the end of 𝑖-th iteration is
(𝑥 ≤ 1 ∧ 𝑥 ≠ −1 ∧ · · · ∧ 𝑥 ≠ −𝑖), and the loop never terminates.
   RecMC [Komuravelli et al. 2014, 2016], which is the algorithm used in the state-of-the-art
software model-checker Spacer, has the same problem as IndPDR/mbp’. It applies model-based
projection to a formula containing the current over- and/or under-approximations, which vary over
time; see (Query) rule in [Komuravelli et al. 2016, Fig. 7] (where the existential quantifier in the
definition of 𝜓 shall be replaced with mobel-based projection in a later section). This observation
applies to other formalizations of Spacer, e.g. [Komuravelli et al. 2015] (that actually behaves
slightly differently).
   We give a concrete counterexample. Let 𝑆 ′ be a non-linear CHC system, given by
    { 𝜄 (𝑥) ⇒ 𝑄 (0, 𝑥),   ⊤ ⇒ 𝑄 (1, 𝑥),       𝑄 (0, 𝑥) ∧ 𝑄 (1, 𝑥) ∧ 𝜏 (𝑥, 𝑦) ⇒ 𝑄 (0, 𝑦),        𝑄 (0, 𝑥) ⇒ 𝛼 (𝑥) }.
Since 𝑄 (1, 𝑥) = ⊤, one can remove 𝑄 (1, 𝑥) from 𝑆 ′ by substituting ⊤ for it. The resulting constraint
set is essentially the same as 𝑆, obtained by replacing 𝑃 (𝑥) in 𝑆 with 𝑄 (0, 𝑥). A badly-behaved
model-based projection MBP ′′ is similar to MBP ′: it basically behaves as MBP but returns 𝑥 = 𝑚 if
𝑀 (𝑥) = 𝑚 is either the maximum or minimum in {𝑛 < 0 | |= ∃𝑦.𝜓 (𝑛, 𝑦)}.
  This divergent behavior is notable because a journal paper [Komuravelli et al. 2016] proves that
RecMC always terminates without assuming any assumptions on the model-based projection pro-
cess and the interpolating theorem prover. This shows the nontriviality and subtlety of termination
proofs of algorithms with model-based projection.

7     MAXIMAL CONSERVATIVITY FOR INFINITE GAME SOLVING
The characterization of PDR by maximal conservativity reveals an unexpected connection between
PDR and an efficient procedure for game solving [Farzan and Kincaid 2017].
   Farzan and Kincaid [Farzan and Kincaid 2017] proposed a procedure for game solving over
infinite graphs of which rules are defined by linear arithmetic. Assume that a state is represented
by a tuple 𝑠® = (𝑠 1, . . . , 𝑠𝑛 ) of data of the logic, as well as actions 𝑎®0 and 𝑎®1 of Players 0 and 1,
respectively. Players alternatively choose actions, starting from Player 0. The transition of the game
is a partial function represented by 𝜏: 𝜏 (®   𝑠 , 𝑎®0, 𝑎®1, 𝑡®) is true if and only if 𝑡® is the state after playing 𝑎®0
and then 𝑎®1 . Player 0 wins the game if the game does not get stuck. We are interested in whether
Player 0 wins the game.
   Their approach is fairly naturally understood as a cyclic proof search, although their paper [Farzan
and Kincaid 2017] does not mention the connection. The winning region of Player 0 is characterized

                                 Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:24                                                                                    Takeshi Tsukada and Hiroshi Unno


by the greatest solution of
                                  𝑊 (®
                                     𝑠 ) ⇔ ∃®     𝑎 1 .∃𝑡®.𝜏 (®
                                            𝑎 0 .∀®           𝑠 , 𝑎®0, 𝑎®1, 𝑡®) ∧ 𝑊 (𝑡®).                             (10)
The definition says that 𝑠® is winning for Player 0 if there exists an appropriate action 𝑎®0 of Player
0 such that, for every action 𝑎®1 of Player 1, the next state 𝑡® exists and it is a winning position of
Player 0. So the game solving is reduced to the validity of 𝜄 (®          𝑠 ) ⊢ (𝜈𝑊 ) (® 𝑠 ).
   Their procedure can be described as a proof search strategy for sequents of the form 𝜑 (®                            𝑠) ⊢
(𝜈𝑊 ) (® 𝑠 ). Application of (𝜈-R) yields a partial proof with an open sequent 𝜑 (®             𝑠 ) ⊢ 𝛿 [𝜈𝑊 ] (®
                                                                                                               𝑠 ), where
𝛿 is the right-hand-side of Equation 10. A significant difference from software model-checking is
found here: since 𝛿 contains quantifiers, it is not easy to transform this sequent into 𝜓 (𝑡®) ⊢ (𝜈𝑊 ) (𝑡®).
Their idea is to use a proof of a fixed-point-free sequent 𝜑 (®        𝑠 ) ⊢ 𝛿 [⊤] (®𝑠 ), from which one can easily
obtain a partial proof by replacing ⊤ with (𝜈𝑊 ). To (dis)prove the sequent 𝜑 (®                     𝑠 ) ⊢ 𝛿 [⊤] (®
                                                                                                                  𝑠 ), they
used an external solver, which itself is developed in the first half of their paper [Farzan and Kincaid
2017] using [Farzan and Kincaid 2016].
   What is notable is a way to fix the partial proof when 𝜑 (®                 𝑠 ) ⊢ 𝛿 [⊤] (® 𝑠 ) is false. Recall that
𝜑 (®
   𝑠 ) ⊢ (𝜈𝑊 ) (® 𝑠 ) is an open sequent of the current partial proof, which is a leaf. Their procedure
tries to fix the partial proof, by refining a subtree containing this open sequent. Their procedure
first seeks the nearest ancestor of the open sequent 𝜑 (®            𝑠 ) ⊢ (𝜈𝑊 ) (® 𝑠 ) that uses (𝜈-R) rule in the
current partial proof. Let 𝜑 ′ (®   𝑠 ′) ⊢ 𝛿 [𝜈𝑊 ] (®
                                                    𝑠 ′) be its premise. Then the procedure check the validity
of 𝜑 ′ (®
        𝑠 ′) ⊢ 𝛿 [𝛿 [⊤]] (®𝑠 ′), the two-folded expansion of 𝜈𝑊 . If the sequent is valid, it replaces the
subtree above the ancestor by using the proof; if the sequent is invalid, it seeks the next ancestor
and tries to fix the subtree above it. This is the maximally conservative policy, and their procedure
for game solving belongs to the PDR family in this sense.
   We conclude with two consequences. First the notion of maximal conservativity is a useful
characterization of PDR that significantly extends the scope of PDR. Second the maximal conser-
vativity would be useful for implementing an efficient prover: at least, it works well for sequents
corresponding to game solving to some extent, as confirmed by the experiments in [Farzan and
Kincaid 2017].

8      RELATED WORK
We have demonstrated that not only well-known software model checking algorithms, including
symbolic execution, bounded model checking [Biere et al. 1999], predicate abstraction [Ball et al.
2001], lazy abstraction [Henzinger et al. 2004, 2002; McMillan 2006], and PDR [Cimatti and Griggio
2012; Hoder and Bjørner 2012], but also an efficient game solving algorithm [Farzan and Kincaid
2017] can be seen as cyclic-proof search. This section discusses other related proof search and
software model-checking algorithms.

8.1     Proof search in cyclic and Martin-Löf-style proof systems
Proof search in cyclic [Brotherston and Simpson 2011; Sprenger and Dam 2003] and Martin-Löf-
style [Martin-Löf 1971] proof systems finds wide applications in safety/liveness program verification
and entailment checking in first-order and separation logics with inductive predicates.
   Program verification. Brotherston et al. [Brotherston et al. 2008, 2012; Tellez and Brotherston
2020] gave cyclic proof systems for Hoare logic (with the separation logic as the underlying assertion
language). They mentioned a certain part of a proof search corresponds to symbolic execution.
However, they did not establish a connection to modern software model-checkers, of which the
main challenge is to find an invariant. Unno et al. [2017] presented an inductive proof system
tailored to CHC solving and applied it to relational verification. The search algorithms presented in

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Software Model-Checking as Cyclic-Proof Search                                                                   1:25


these studies correspond to bounded model-checking with covering, and the cut-rules (i.e., (Cons)
rule in [Tellez and Brotherston 2020] and (Apply⊥)/(ApplyP) rules in [Unno et al. 2017]) are used
only when one needs to check whether an open leaf node is covered. Researchers have extended
SMT solvers to efficiently handle recursive functions and applied them to verification of programs
that manipulate structured data [Qiu et al. 2013; Reynolds and Kuncak 2015; Suter et al. 2010, 2011].
These work however neither show a connection to modern software model checker nor discuss
heuristics to find a good cut-formula using software model checking techniques.

   Entailment checking. Many papers are devoted to give (efficient) automated theorem provers
for entailment problems with inductive predicates [Brotherston 2005; Brotherston et al. 2011;
Chin et al. 2012; Chu et al. 2015; Iosif et al. 2013; Ta et al. 2016, 2017] (in particular, of separation
logic) and to find decidable fragments of the entailment problems [Berdine et al. 2004; Le et al.
2017]. However, to our knowledge, there is no work that shows connection to modern software
model checker. An interesting question is whether these developments and ideas are applicable
to software model-checking. For example, global trace condition for cyclic proofs gives us a more
flexible covering criterion than the naïve one used in most software model-checkers. Also, lemma
discovery techniques developed for entailment checking [Enea et al. 2015; Ta et al. 2016, 2017] or
general purpose inductive theorem proving [Bundy 2001] can be useful in software model checking.
Conversely, it is interesting to investigate if Craig interpolation and other heuristics for finding
a good cut-formula that have been studied in the software model checking community can be
effectively applied as lemma discovery heuristics to inductive theorem proving.

8.2 Software model checking
   Unified framework. Beyer et al. have been developing a configurable software model checker
CPAchecker [Beyer et al. 2007, 2008; Beyer and Keremoglu 2011], which implements various
software model checking algorithms [Beyer and Dangl 2020; Beyer et al. 2018; Beyer and Wendler
2012] in a unified framework in a configurable manner. Though our logical foundation also provides
a unified framework, the level of abstraction is significantly different: we reconstruct well-known
algorithms from a few simple and declarative principles, whereas CPAchecker achieves the recon-
struction via modular design and implementation of software model checking components.

   Constraint logic programming. Constraint logic programming (CLP) has been used as a log-
ical foundation of software model checking [Bjørner et al. 2015; Flanagan 2004; Podelski and
Rybalchenko 2007]. They use CLP to model the target specification as well as the concrete or
abstract execution semantics of the target program and then invoke a CLP solver to perform an
actual proof-search such as symbolic execution, predicate abstraction, and abstraction refinement.
By contrast, the logical foundation proposed in this paper aims at analyzing and comparing existing
and unseen software model checking algorithms as different proof-search strategies in the same
cyclic proof system. In other words, we provide a logical foundation for not only modeling but also
solving safety verification problems.

   Interpolating theorem provers. We presented declarative characterizations of interpolation-based
frame refinement, where we regarded interpolating theorem provers as a black box. Their internal
states and syntactic features (e.g., size and shape) of their outputs cannot be captured by the current
cyclic-proof framework. We plan to investigate the following research questions: Is it possible to
see the internal states as partial proofs? Is it possible to give a declarative characterization for
practically “good” interpolants: those returned by PDR and beautiful interpolants [Albarghouthi
and McMillan 2013].

                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:26                                                                                  Takeshi Tsukada and Hiroshi Unno


   Other approaches to invariant synthesis. Other approaches include constraint-based one [Colón
et al. 2003; Sankaranarayanan et al. 2004] that uses ∃∀-formula solvers and CEGIS [Solar-Lezama
et al. 2006] that uses inductive synthesizers [Garg et al. 2016; Sharma et al. 2013]. The cyclic-proof
framework needs further extensions to capture their internal states: for instance, for the latter we
need to annotate each judgement in a partial proof with examples that are iteratively collected by
the CEGIS procedure.

9      CONCLUSION AND FUTURE WORK
This paper establishes a tight connection between software model-checkers and cyclic-proof
search strategies. It is worth emphasizing that our connection relates internal states of modern,
sophisticated software model-checkers and partial proofs in the cyclic proof system. The logical
viewpoint is useful for understanding model-checking procedures. A rich structure of (or strong
constraints on) partial proofs allows us to reconstruct important model-checking procedures from
a few simple principles: for example, PDR is a proof seach strategy following Principles 1, 3, 4 and
5. Furthermore the logical characterization of PDR significantly extends the scope of application,
as discussed in section 7.
   The most important future work is an empirical study. An interesting question is about the
efficiency of an alternative implementation of PDR, in which maximally conservative interpolants
are computed in a different way. If it is comparable to the original PDR, the development of an
efficient maximally-conservatively interpolating theorem prover would be of practical interest.
   Future work in another direction is a study of model-checking procedures that are not covered
by this paper, such as GPDR [Hoder and Bjørner 2012] and Spacer [Komuravelli et al. 2014] for
safety verification of programs with first-order functions. This class of the verification problem is
out of the scope of our framework: although it has an inductive characterization, it does not have
the dual, coinductive characterization.
   We are also interested in the development of new model-checkers using logical ideas. For example,
the safety verification of programs with functions has an inductive characterization (𝜇𝑅) (𝑥) ⊢ 𝛼 (𝑥),
whereas it has no coinductive characterisation. The logical analysis of the paper suggests that
backward execution looks more natural (cf. Section 5), but empirical evaluation of this suggestion
is left for future work.

ACKNOWLEDGMENTS
This work was supported by JST ERATO HASUO Metamathematics for Systems Design Project
(No. JPMJER1603) and JSPS KAKENHI Grant Numbers JP20H05703, JP19K22842, JP20H04162,
JP17H01720, and JP19H04084.

REFERENCES
Aws Albarghouthi and Kenneth L. McMillan. 2013. Beautiful Interpolants, Vol. 8044. 313–329.
Thomas Ball, Byron Cook, Vladimir Levin, and Sriram K. Rajamani. 2004. SLAM and Static Driver Verifier: Technology
   Transfer of Formal Methods inside Microsoft. In Integrated Formal Methods. 1–20.
Thomas Ball, Rupak Majumdar, Todd Millstein, and Sriram K. Rajamani. 2001. Automatic predicate abstraction of C programs.
   203–213.
Thomas Ball and Sriram K. Rajamani. 2002. The SLAM project: debugging system software via static analysis. 1–3.
Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. 2004. A Decidable Fragment of Separation Logic, Vol. 3328. 97–109.
Dirk Beyer and Matthias Dangl. 2020. Software Verification with PDR: An Implementation of the State of the Art. 3–21.
Dirk Beyer, Matthias Dangl, and Philipp Wendler. 2018. A Unifying View on SMT-Based Software Verification. 60, 3 (2018),
   299—-335.
Dirk Beyer, Thomas A. Henzinger, and Grégory Théoduloz. 2007. Configurable Software Verification: Concretizing the
   Convergence of Model Checking and Program Analysis. 504–518.
D. Beyer, T. A. Henzinger, and G. Theoduloz. 2008. Program Analysis with Dynamic Precision Adjustment. 29–38.


Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Software Model-Checking as Cyclic-Proof Search                                                                             1:27


Dirk Beyer and M. Erkan Keremoglu. 2011. CPAchecker: A Tool for Configurable Software Verification. 184–190.
D. Beyer and P. Wendler. 2012. Algorithms for software model checking: Predicate abstraction vs. Impact. 106–113.
Armin Biere, Alessandro Cimatti, Edmund Clarke, and Yunshan Zhu. 1999. Symbolic Model Checking without BDDs.
    193–207.
Johannes Birgmeier, Aaron R. Bradley, and Georg Weissenbacher. 2014. Counterexample to Induction-Guided Abstraction-
    Refinement (CTIGAR). 831–848.
Nikolaj Bjørner, Arie Gurfinkel, Kenneth L. McMillan, and Andrey Rybalchenko. 2015. Horn Clause Solvers for Program
    Verification. In Fields of Logic and Computation II: Essays Dedicated to Yuri Gurevich on the Occasion of His 75th Birthday,
    Vol. 9300. 24–51.
Aaron R. Bradley. 2011. SAT-based Model Checking Without Unrolling, Vol. 6538. 70–87.
James Brotherston. 2005. Cyclic Proofs for First-Order Logic with Inductive Definitions. In TABLEAUX ’05, Vol. 3702. 78–92.
James Brotherston, Richard Bornat, and Cristiano Calcagno. 2008. Cyclic Proofs of Program Termination in Separation
    Logic. 101–112.
James Brotherston, Dino Distefano, and Rasmus Lerchedahl Petersen. 2011. Automated Cyclic Entailment Proofs in
    Separation Logic. 131–146.
James Brotherston, Nikos Gorogiannis, and Rasmus L. Petersen. 2012. A Generic Cyclic Theorem Prover. 350–367.
J. Brotherston and A. Simpson. 2011. Sequent calculi for induction and infinite descent. Journal of Logic and Computation
    21, 6 (2011), 1177–1216.
Alan Bundy. 2001. The Automation of Proof by Mathematical Induction. In Handbook of Automated Reasoning, Vol. I.
    845–911.
Wei-Ngan Chin, Cristina David, Huu Hai Nguyen, and Shengchao Qin. 2012. Automated Verification of Shape, Size and Bag
    Properties via User-Defined Predicates in Separation Logic. Sci. Comput. Program. 77, 9 (2012), 1006–1036.
Duc-Hiep Chu, Joxan Jaffar, and Minh-Thai Trinh. 2015. Automatic Induction Proofs of Data-structures in Imperative
    Programs. 457–466.
Alessandro Cimatti and Alberto Griggio. 2012. Software Model Checking via IC3. 277–293.
Alessandro Cimatti, Alberto Griggio, Sergio Mover, and Stefano Tonetta. 2014. IC3 Modulo Theories via Implicit Predicate
    Abstraction. 46–61.
Edmund M. Clarke, Orna Grumberg, Somesh Jha, Yuan Lu, and Helmut Veith. 2003. Counterexample-guided abstraction
    refinement for symbolic model checking. 50, 5 (2003), 752–794.
Michael A. Colón, Sriram Sankaranarayanan, and Henny B. Sipma. 2003. Linear Invariant Generation Using Non-linear
    Constraint Solving, Vol. 2725. 420–432.
William Craig. 1957. Three Uses of the Herbrand-Gentzen Theorem in Relating Model Theory and Proof Theory. 22 (1957),
    269–285.
Niklas Een, Alan Mishchenko, and Robert Brayton. 2011. Efficient Implementation of Property Directed Reachability.
    125–134.
Constantin Enea, Mihaela Sighireanu, and Zhilin Wu. 2015. On Automated Lemma Generation for Separation Logic with
    Inductive Definitions. 80–96.
Azadeh Farzan and Zachary Kincaid. 2016. Linear Arithmetic Satisfiability via Strategy Improvement. AAAI Press, 735–743.
Azadeh Farzan and Zachary Kincaid. 2017. Strategy Synthesis for Linear Arithmetic Games. 2, POPL, Article 61 (Dec. 2017),
    30 pages.
Cormac Flanagan. 2004. Automatic software model checking via constraint logic. Science of Computer Programming 50, 1
    (2004), 253–270.
Pranav Garg, Daniel Neider, P. Madhusudan, and Dan Roth. 2016. Learning Invariants Using Decision Trees and Implication
    Counterexamples. 499–512.
Susanne Graf and Hassen Saïdi. 1997. Construction of Abstract State Graphs with PVS, Vol. 1254. 72–83.
Thomas A. Henzinger, Ranjit Jhala, Rupak Majumdar, and Kenneth L. McMillan. 2004. Abstractions from proofs. 232–244.
Thomas A. Henzinger, Ranjit Jhala, Rupak Majumdar, and Grégoire Sutre. 2002. Lazy abstraction. 58–70.
Kryštof Hoder and Nikolaj Bjørner. 2012. Generalized Property Directed Reachability. 157–171.
Radu Iosif, Adam Rogalewicz, and Jiri Simacek. 2013. The Tree Width of Separation Logic with Recursive Definitions. 21–38.
Ranjit Jhala and Rupak Majumdar. 2009. Software Model Checking. ACM Comput. Surv. 41, 4, Article 21 (Oct. 2009), 54 pages.
Alexey Khoroshilov, Vadim Mutilin, Alexander Petrenko, and Vladimir Zakharov. 2010. Establishing Linux Driver Verification
    Process. In Perspectives of Systems Informatics. 165–176.
Daisuke Kimura, Koji Nakazawa, Tachio Terauchi, and Hiroshi Unno. 2020. Failure of Cut-Elimination in Cyclic Proofs of
    Separation Logic. Computer Software 37, 1 (2020), 1_39–1_52.
Anvesh Komuravelli, Nikolaj Bjørner, Arie Gurfinkel, and Kenneth L. McMillan. 2015. Compositional Verification of
    Procedural Programs Using Horn Clauses over Integers and Arrays. FMCAD Inc, 89–96.



                                   Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:28                                                                                    Takeshi Tsukada and Hiroshi Unno


Anvesh Komuravelli, Arie Gurfinkel, and Sagar Chaki. 2014. SMT-Based Model Checking for Recursive Programs, Vol. 8559.
   17–34.
Anvesh Komuravelli, Arie Gurfinkel, and Sagar Chaki. 2016. SMT-Based Model Checking for Recursive Programs. 48, 3
   (June 2016), 175–205.
Anvesh Komuravelli, Arie Gurfinkel, Sagar Chaki, and Edmund M. Clarke. 2013. Automatic Abstraction in SMT-Based
   Unbounded Software Model Checking. 846–862.
Quang Loc Le, Makoto Tatsuta, Jun Sun, and Wei-Ngan Chin. 2017. A Decidable Fragment in Separation Logic with Inductive
   Predicates and Arithmetic. 495–517.
Per Martin-Löf. 1971. Hauptsatz for the Intuitionistic Theory of Iterated Inductive Definitions. In Proceedings of the Second
   Scandinavian Logic Symposium. Studies in Logic and the Foundations of Mathematics, Vol. 63. 179 – 216.
Yukihiro Masuoka and Makoto Tatsuta. 2021. Counterexample to cut-elimination in cyclic proof system for first-order logic
   with inductive definitions. CoRR abs/2106.11798 (2021). arXiv:2106.11798
Kenneth L. McMillan. 2006. Lazy Abstraction with Interpolants, Vol. 4144. 123–136.
Andreas Podelski and Andrey Rybalchenko. 2007. ARMC: The Logical Choice for Software Model Checking with Abstraction
   Refinement. In Practical Aspects of Declarative Languages. 245–259.
Xiaokang Qiu, Pranav Garg, Andrei Ştefănescu, and Parthasarathy Madhusudan. 2013. Natural Proofs for Structure, Data,
   and Separation. 231–242.
Andrew Reynolds and Viktor Kuncak. 2015. Induction for SMT Solvers, Vol. 8931. 80–98.
Sriram Sankaranarayanan, Henny B. Sipma, and Zohar Manna. 2004. Non-linear loop invariant generation using Gröbner
   bases. 318–329.
Rahul Sharma, Saurabh Gupta, Bharath Hariharan, Alex Aiken, and Aditya V. Nori. 2013. Verification as Learning Geometric
   Concepts. 388–411.
Mary Sheeran, Satnam Singh, and Gunnar Stålmarck. 2000. Checking Safety Properties Using Induction and a SAT-Solver.
   127–144.
Armando Solar-Lezama, Liviu Tancau, Rastislav Bodik, Sanjit Seshia, and Vijay Saraswat. 2006. Combinatorial Sketching
   for Finite Programs. In ASPLOS XII (San Jose, California, USA). 404–415.
Christoph Sprenger and Mads Dam. 2003. On the Structure of Inductive Reasoning: Circular and Tree-Shaped Proofs in the
   𝜇Calculus. 425–440.
Philippe Suter, Mirco Dotta, and Viktor Kuncak. 2010. Decision procedures for algebraic data types with abstractions.
   199–210.
Philippe Suter, Ali Sinan Köksal, and Viktor Kuncak. 2011. Satisfiability modulo recursive programs, Vol. 6887. 298–315.
Quang-Trung Ta, Ton Chanh Le, Siau-Cheng Khoo, and Wei-Ngan Chin. 2016. Automated Mutual Explicit Induction Proof
   in Separation Logic. 659–676.
Quang-Trung Ta, Ton Chanh Le, Siau-Cheng Khoo, and Wei-Ngan Chin. 2017. Automated Lemma Synthesis in Symbolic-
   Heap Separation Logic. 2, POPL, Article 9 (Dec. 2017), 29 pages.
Gadi Tellez and James Brotherston. 2020. Automatically Verifying Temporal Properties of Pointer Programs with Cyclic
   Proof. 64, 3 (2020), 555–578.
Hiroshi Unno, Sho Torii, and Hiroki Sakamoto. 2017. Automating Induction for Solving Horn Clauses. 571–591.
Yakir Vizel and Arie Gurfinkel. 2014. Interpolating Property Directed Reachability. 260–276.




Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Software Model-Checking as Cyclic-Proof Search                                                                          1:29


A     CYCLIC PROOF SYSTEM
This section gives the cyclic proof systems used in this paper, of which details are omitted. complete
list of rules of the cyclic proof system used in this paper. The description of this section is condensed;
see also [Brotherston et al. 2011] for the basic ideas of cyclic proof systems.
   A first-order signature is a pair of sets of function symbols and predicate symbols. Each symbol
is associated with a natural number, called its arity.11 Assume a first-order signature, fixed in the
sequel.

A.1    Formulas and judgements
For each natural number 𝑘, we assume a (finite or infinite) set V𝑘 of predicate variables of arity 𝑘.
We assume V𝑘 ∩ Vℓ = ∅ if 𝑘 ≠ ℓ.
  The syntax of terms is standard:
                                                      𝑡 ::= 𝑥 | 𝑓 (𝑡 1, . . . , 𝑡𝑘 )
where 𝑥 is a (term or object) variable and 𝑓 is an arity-𝑘 function symbol in the signature. The
syntax of formulas is also standard:
                 𝜑,𝜓 ::= 𝑝 (𝑡 1, . . . , 𝑡𝑘 ) | 𝑡 = 𝑡 ′ | 𝑃 (𝑡 1, . . . , 𝑡𝑛 ) | ¬𝜑 | 𝜑 ∧ 𝜓 | 𝜑 ∨ 𝜓 | ∀𝑥 .𝜑 | ∃𝑥 .𝜑
where 𝑝 is an arity-𝑘 predicate symbol in the signature, 𝑃 is an arity-𝑘 predicate variable and
𝑡 1, . . . , 𝑡𝑘 are terms.
     Each predicate variable 𝑃 ∈ V𝑘 is associated with its defining equation:
                                          𝑃 (𝑥 1, . . . , 𝑥𝑘 )    ⇔       𝛿𝑃 (𝑥 1, . . . , 𝑥𝑘 ).
Note that 𝛿𝑃 (𝑥 1, . . . , 𝑥𝑘 ) may contain 𝑃 and/or other predicate variables; every occurrence of a
predicate variable in 𝛿𝑃 must be positive (i.e. every occurrence of a predicate variable is under
an even number of negation operators). The meaning of this equation depends on the setting;
Section A.3 regards 𝑃 as the least fixed-point of the equation and Section A.4 as the greatest
fixed-point.12 We write 𝛿𝑃 [𝜓 ] for the formula obtained by replacing 𝑃 in 𝛿𝑃 with 𝜓 .
   We define a judgement Γ ⊢ Δ as a pair of finite sequences of formulas.
   A substitution 𝜃 is a list [𝑡 1 /𝑥 1, . . . , 𝑡𝑘 /𝑥𝑘 ] of pairs of terms and variables such that 𝑥 1, . . . , 𝑥𝑘 are
pairwise distinct. We write 𝜑𝜃 for the formula obtained by replacing 𝑥𝑖 in 𝜑 with 𝑡𝑖 (for each 𝑖).
A substitution is also applicable to sequences of formulas: if Γ = 𝜑 1, . . . , 𝜑 ℓ , then Γ𝜃 is defined as
𝜑 1𝜃, . . . , 𝜑 ℓ 𝜃 .

A.2    Standard rules for predicate logic
Figure 8 is the list of rules for the sequent calculus for predicate logic (except for the structural
rules, which we omit here). The rules (∀-R) and (∃-L) have the standard side condition: the variable
𝑥 has no free occurrence in Γ nor Δ.

A.3    Cyclic proof system for least fixed-points
This subsection describes the cyclic proof system for the predicate logic with least fixed-points.
Hence 𝑃 is regarded as the least solution of 𝑃 (𝑥 1, . . . , 𝑥𝑘 ) ⇔ 𝛿𝑃 (𝑥 1, . . . , 𝑥𝑘 ). To emphasise this
interpretation, we write 𝑃 (𝑡 1, . . . , 𝑡𝑛 ) as (𝜇𝑃) (𝑡 1, . . . , 𝑡𝑛 ).
   Figure 9 is the list of rules for the sequent calculus for the predicate logic with least fixed-points.
11 So only single-sorted signatures are considered here.
12 Note that 𝛿
             𝑃 may contain a predicate variable other than 𝑃 . So the meaning of all predicate variables are defined by
mutual recursion, as a solution of the large system of equations.


                                      Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:30                                                                                   Takeshi Tsukada and Hiroshi Unno



                                                                           Γ, 𝜑 ⊢ Δ         Γ,𝜓 ⊢ Δ
                                                                                                             (∨-L)
                                                                                 Γ, 𝜑 ∨ 𝜓 ⊢ Δ
                                                       (Ax)
                          Γ, 𝜑 ⊢ Δ, 𝜑                                               Γ ⊢ Δ, 𝜑,𝜓
                                                                                                             (∨-R)
                   Γ ⊢ Δ, 𝜑          Γ, 𝜑 ⊢ Δ                                    Γ ⊢ Δ, 𝜑 ∨ 𝜓
                                                      (Cut)
                              Γ⊢Δ                                                    Γ ⊢ Δ, 𝜑
                                                                                                             (¬-L)
                              Γ⊢Δ                                                   Γ, ¬𝜑 ⊢ Δ
                                                     (Subst)
                            Γ𝜃 ⊢ Δ𝜃                                                  Γ, 𝜑 ⊢ Δ
                                                                                                             (¬-R)
                              Γ⊢Δ                                                   Γ ⊢ Δ, ¬𝜑
                                                       (⊤-L)
                            Γ, ⊤ ⊢ Δ                                         Γ[𝑥/𝑦] ⊢ Δ[𝑥/𝑦]
                                                                                                             (=-L)
                                                                                 Γ, 𝑥 = 𝑦 ⊢ Δ
                                                      (⊤-R)
                            Γ ⊢ Δ, ⊤
                                                                                                             (=-R)
                                                                                 Γ ⊢ Δ, 𝑡 = 𝑡
                                                       (⊥-L)
                            Γ, ⊥ ⊢ Δ                                            Γ, 𝜑 [𝑡/𝑥] ⊢ Δ
                                                                                                             (∀-L)
                              Γ⊢Δ                                                Γ, ∀𝑥 .𝜑 ⊢ Δ
                                                      (⊥-R)
                            Γ ⊢ Δ, ⊥                                                 Γ ⊢ Δ, 𝜑
                                                                                                             (∀-R)
                          Γ, 𝜑,𝜓 ⊢ Δ                                             Γ ⊢ Δ, ∀𝑥 .𝜑
                                                       (∧-L)
                         Γ, 𝜑 ∧ 𝜓 ⊢ Δ                                                Γ, 𝜑 ⊢ Δ
                                                                                                             (∃-L)
                   Γ ⊢ Δ, 𝜑          Γ ⊢ Δ,𝜓                                     Γ, ∃𝑥 .𝜑 ⊢ Δ
                                                       (∧-R)
                         Γ ⊢ Δ, 𝜑 ∧ 𝜓                                           Γ ⊢ Δ, 𝜑 [𝑡/𝑥]
                                                                                                             (∃-R)
                                                                                 Γ ⊢ Δ, ∃𝑥 .𝜑

                        Fig. 8. Standard rules of the sequent calculus for predicate logic


                 Γ, 𝛿𝑃 [𝜇𝑃] (𝑡 1, . . . , 𝑡𝑘 ) ⊢ Δ                       Γ ⊢ Δ, 𝛿𝑃 [𝜇𝑃] (𝑡 1, . . . , 𝑡𝑘 )
                                                       (𝜇-L)                                                 (𝜇-R)
                   Γ, (𝜇𝑃) (𝑡 1, . . . , 𝑡𝑘 ) ⊢ Δ                         Γ ⊢ Δ, (𝜇𝑃) (𝑡 1, . . . , 𝑡𝑘 )

                                         Fig. 9. The rules for least fixed-points


    We consider derivations which may be partial in the sense that leaves are not necessarily axioms
(i.e. those provable by rules with no premise). We call a non-axiom leaf an open leaf (or a bud node).
A companion of an open leaf 𝑙 is an internal node 𝑛 in the derivation such that 𝑙 and 𝑛 are labelled
by the same sequent.
    A pre-proof is a (possibly partial) derivation with a function that assigns a companion for each
open leaf. Hence it is a directed and pointed graph (instead of a tree) such that
      • each node is labelled by a sequent, and

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Software Model-Checking as Cyclic-Proof Search                                                                           1:31



                 Γ, 𝛿𝑃 [𝜈𝑃] (𝑡 1, . . . , 𝑡𝑘 ) ⊢ Δ                           Γ ⊢ Δ, 𝛿𝑃 [𝜈𝑃] (𝑡 1, . . . , 𝑡𝑘 )
                                                           (𝜈-L)                                                 (𝜈-R)
                   Γ, (𝜈𝑃) (𝑡 1, . . . , 𝑡𝑘 ) ⊢ Δ                             Γ ⊢ Δ, (𝜈𝑃) (𝑡 1, . . . , 𝑡𝑘 )

                                      Fig. 10. The rules for greatest fixed-points



      • if 𝑛 1, . . . , 𝑛𝑘 is the set of nodes immediately reachable from 𝑛, there is a proof rule whose
        conclusion is (the label of) 𝑛 and whose premises are (the labels of) 𝑛 1, . . . , 𝑛𝑘 .
Here a graph is pointed if it is equipped with a chosen node that we call the initial node.
   As we have seen, a pre-proof is not necessarily valid. We introduce a correctness criterion, called
the global trace condition. We need some auxiliary notions.
   An infinite path 𝜋 = 𝑛 0𝑛 1𝑛 2 . . . of a pre-proof is an infinite path of the corresponding graph
(starting from the initial node 𝑛 0 ): the first node 𝑛 0 is the conclusion of the derivation and 𝑛𝑖+1 is a
premise of 𝑛𝑖 . An infinite trace of an infinite path 𝜋 = 𝑛 0𝑛 1 . . . is an infinite sequence 𝜑 0𝜑 1 . . . of
(occurrences of) formulas in the derivation that satisfies the following conditions:
      • 𝜑𝑖 appears in the sequent of 𝑛𝑖 .
      • 𝜑𝑖+𝑖 is an occurrence of a formula in the premise 𝑛𝑖+1 of 𝑛𝑖 , an occurrence which corresponds
        to 𝜑𝑖 in 𝑛𝑖 .
        – If 𝜑𝑖 is the principal occurrence and the rule concluding 𝑛𝑖 is not (∧-L) nor (∨-R), then 𝜑𝑖+1
          is the unique formula outside of Γ, Δ. For example, if 𝑛 = (Γ,𝜓 1 ∨ 𝜓 2 ⊢ Δ), 𝜑𝑖 = 𝜓 1 ∨ 𝜓 2 , the
          rule is
                                                    Γ,𝜓 1 ⊢ Δ       Γ,𝜓 2 ⊢ Δ
                                                                              ,
                                                         Γ,𝜓 1 ∨ 𝜓 2 ⊢ Δ
          and 𝑛𝑖+1 is the left premise, then 𝜑𝑖+1 = 𝜓 1 . The rules (∧-L) nor (∨-R) are exceptional: these
          rules has two formulas outside of Γ, Δ and 𝜑𝑖+1 is one of them.
        – If 𝜑𝑖 is not principal, i.e. it is in Γ or Δ, then 𝜑𝑖+1 is the same formula in Γ or Δ.
Given a trace 𝜑 0, 𝜑 1, . . ., the 𝑖-th occurrence 𝜑𝑖 is a progressing point if 𝜑𝑖 is the principal occurrence
of (𝜇-L) rule. A trace is infinitely progressing if it has infinitely many progressing points.
   A pre-proof is a proof if every infinite path has an infinitely progressing trace.

A.4     Cyclic proof system for greatest fixed-points
The cyclic proof system for the predicate logic with greatest fixed-points is essentially the same as
that for least fixed-points. Semantically, the difference is that 𝑃 is regarded as the greatest solution
of 𝑃 (𝑥 1, . . . , 𝑥𝑘 ) ⇔ 𝛿𝑃 (𝑥 1, . . . , 𝑥𝑘 ) (so 𝑃 (𝑡 1, . . . , 𝑡𝑛 ) is written as (𝜈𝑃) (𝑡 1, . . . , 𝑡𝑛 )).
   The proof rules for greatest fixed-points, which are the same as those for least fixed-points, are
given in Figure 10. The notions of pre-proofs, paths and traces are the same as in the proof system
for least fixed-points. The difference is that (𝜈-R) is progressive whereas (𝜈-L) is not. Hence the
global trance condition requires that each infinite path has an infinite trace that appears at the
principal position of (𝜈-R) rule infinitely many times.

Remark 6. This paper does not deal with formulas which contains both least and greatest fixed-
points. The idea of cyclic proofs is applicable to logics with both least and greatest fixed-points, but
we do not give a detail of cyclic proof systems for such logics because they need more complicated
global trace conditions.                                                                              □

                                  Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:32                                                                                    Takeshi Tsukada and Hiroshi Unno


B      SIMULATING PDR IN [Hoder and Bjørner 2012]
Recall PDR and an extension of IndPDR discussed in Remark 4. Let ∼ be a relation between
configurations defined by

    (𝑐𝑘 . . . 𝑐𝑛 ∥ 𝜑 0 . . . 𝜑𝑛 ) ∼ (𝑐𝑘 . . . 𝑐𝑛 ∥ 𝐹 0 . . . 𝐹𝑛 ) if and only if        for every 0 ≤ 𝑗 ≤ 𝑛,
               Ô                                                   Ô
                 0≤𝑖 ≤ 𝑗 𝜑𝑖 (𝑥) |= 𝐹 𝑗 (𝑥) and (𝐹 𝑗 (𝑥) ∧ ¬ 0≤𝑖 ≤ 𝑗 𝜑𝑖 (𝑥))           is safe within (𝑛 − 𝑗) steps.

We show that the relation ∼ is a weak bisimulation.

    Theorem B.1. Suppose that (®         𝑐 ∥ 𝜑)
                                              ® ∼ (® 𝑐 ∥ 𝐹®). If (®𝑐 ∥ 𝜑)® −→ (®                     𝑐 ∥ 𝐹®) −→∗pdr
                                                                                  𝑐 ′ ∥ 𝜑® ′), then (®
 𝑐 ′ ∥ 𝐹®′) and (®
(®                              𝑐 ′, ∥ 𝐹®′) for some (®
                 𝑐 ′ ∥ 𝜑® ′) ∼ (®                      𝑐 ′ ∥ 𝐹®′). Conversely, if (®𝑐 ∥ 𝐹®) −→pdr (®  𝑐 ′ ∥ 𝐹®′), then
(®
 𝑐 ∥ 𝜑)
      ® −→ (® ∗   ′     ′
                𝑐 ∥ 𝜑® ) and (®     ′     ′
                                  𝑐 ∥ 𝜑® ) ∼ (®   ′   ®′
                                                 𝑐 ∥ 𝐹 ) for some (®   ′    ′
                                                                     𝑐 ∥ 𝜑® ).

   Proof. This is intuitively clear as each rule has a counterpart, but we need some care to establish
                                             𝑐 ∥ 𝐹®) −→∗pdr (®𝑐 ∥ 𝐹®′) with 𝐹 𝑗′ (𝑥) ⇔ 0≤𝑖 ≤ 𝑗 𝜑𝑖 (𝑥) for
                                                                                         Ô
the precise correspondence. Note that (®
every 0 ≤ 𝑗 ≤ 𝑛 by iteratively applying (Induction/pdr) for ℓ = 1, 2, . . . , 𝑛. This is useful when
simulating −→ by −→pdr .
   Correspondence of (Induction/PDR) and (Induction) is easy.
   (Candidate/PDR) can be simulated by (Candidate). To see this, we have toÔ         check that |= 𝐹𝑛 (𝑐) ∧
¬𝛼 (𝑐) implies |= 𝜑𝑛 (𝑐) ∧ ¬𝛼 (𝑐). This follows from the assumption 𝐹𝑛 (𝑥) ∧ ( 0≤𝑖 ≤𝑛 𝜑𝑖 (𝑥)) is safe
                                Ô
within 0 steps, i.e. 𝐹𝑛 (𝑥) ∧ ( 0≤𝑖 ≤𝑛 𝜑𝑖 (𝑥)) |= 𝛼 (𝑥). The converse is trivial because 𝜑𝑛 (𝑥) |= 𝐹𝑛 (𝑥).
   The correspondence of (Decide/PDR) and (Decide) can be show similarly.
   (Conflict) can be simulated by (Conflict/PDR) and (Induction/PDR).             Ô By using (Induc-
tion/PDR), we can assume without loss of generality that 𝐹 𝑗′ (𝑥) ⇔ 0≤𝑖 ≤ 𝑗 𝜑𝑖 (𝑥) for every
0 ≤ 𝑗 ≤ 𝑛. Suppose 𝜑𝑘−1 (𝑥) ∧ 𝜏 (𝑥, 𝑦) |= 𝜓 (𝑦) and 𝜓 (𝑥) |= 𝑥 ≠ 𝑐𝑘 . Let 𝜓 ′ (𝑥) = 𝐹𝑘−1 (𝑥) ∨𝜓 (𝑥). Then
(Conflict/PDR) with the interpolation 𝜓 ′ gives a desired transition.
   (Conflict/PDR)
                      can be simulated by (Conflict) and (Induction). Assume 𝜄 (𝑦) ∨ ∃𝑥 .𝐹𝑘−1 (𝑥) ∧
𝜏 (𝑥, 𝑦) |= 𝜓 (𝑦). By 𝜑𝑖 (𝑥) |= 𝐹𝑘−1 (𝑥) for every 𝑖 ≤ 𝑘 − 1, we have 𝜄 (𝑦) |= 𝜓 (𝑦) and ∃𝑥 .𝜑𝑖 (𝑥) ∧
𝜏 (𝑥, 𝑦) |= 𝜓 (𝑦) for every 𝑖 ≤ 𝑘 − 1. By (Conflict) and (Induction),

           (𝑐𝑘 . . . 𝑐𝑛 ∥ 𝜑 0 . . . 𝜑𝑛 )    −→          (𝑐𝑘+1 . . . 𝑐𝑛 ∥ 𝜑 0 . . . 𝜑𝑘−1 (𝜑𝑘 ∧ 𝜓 )𝜑𝑘+1 . . . 𝜑𝑛 )
                                            −→          (𝑐𝑘+1 . . . 𝑐𝑛 ∥ (𝜑 0 ∧ 𝜓 ) . . . (𝜑𝑘 ∧ 𝜓 )𝜑𝑘+1 . . . 𝜑𝑛 )

and this is the required transition.                                                                                  □

C      DIVERGING BEHAVIOUR OF RECMC
We shows that RecMC [Komuravelli et al. 2014, 2016] is possibly diverging even for bounded depth.

  CHC. For ease of explanation, we use a CHC system that slightly differs from that in the main
text. The CHC system has multiple predicate variables 𝑃, 𝑄 and 𝑅; if you would like to have a
counterexample with a single predicate variable (in order to fit a formalisation of, for example,
[Komuravelli et al. 2015]), you can replace 𝑃 (𝑥), 𝑄 (𝑥) and 𝑅(𝑥) with 𝑆 (0, 𝑥), 𝑆 (1, 𝑥) and 𝑆 (2, 𝑥),
respectively, for a fresh predicate variable 𝑆.
  The non-linear CHC system is given by

                  { 𝑥 = 0 ⇒ 𝑃 (𝑥),         ⊤ ⇒ 𝑄 (𝑥),      𝑃 (𝑥) ∧ 𝑄 (𝑥) ⇒ 𝑅(𝑥),          𝑅(𝑥) ⇒ ⊥ }.

This is unsatisfiable, since 𝑃 (0), 𝑄 (0) and 𝑅(0) must be true, contradicting 𝑅(𝑥) ⇒ ⊥.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Software Model-Checking as Cyclic-Proof Search                                                                          1:33


 For an arbitrary model-based projection MBP, we define a badly-behaved model-based projection
MBP ′ by
                        
                        
                         𝑥 =𝑚                                      if 𝑀 (𝑥) = 𝑚 = max{𝑛 > 0 | |= ∃®
                                                                                                   𝑦.𝜓 (𝑛, 𝑦)}
        ′
                        
                        
 MBP (𝜓 (𝑥, 𝑦),
            ® {𝑦},
                ® 𝑀) := 𝑥 = 𝑚                                       if 𝑀 (𝑥) = 𝑚 = min{𝑛 > 0 | |= ∃®
                                                                                                   𝑦.𝜓 (𝑛, 𝑦)}
                        
                         MBP (𝜓 (𝑥, 𝑦), {𝑦}, 𝑀)
                        
                                                                    otherwise.
                        
This satisfies the requirements for model-based projection: note that the cardinality of the image of
MBP ′ (𝜓 (𝑥, 𝑦),
             ® {𝑦},
                 ® (−)) is that of MBP plus 2 and thus finite.
  We also assume that
                               interpolation(𝜓 (𝑥, 𝑦), 𝜗 (𝑦)) := 𝜗 (𝑦).                          (11)
   Divergence of RecMC. The behaviour of RecMC, specialised to the above setting, can be explained
as follows.
   We run the procedure to check the safety of the CHC with depth 2. RecMC in maintains
                                                                                            both
                                                                                      𝜑
over- and under-approximations for each predicate for each depth. We write 𝐴𝑖 =           to mean
                                                                                      𝜓
that the under- and over-approximations of predicate 𝐴 at level 𝑖 are 𝜑 and 𝜓 , respectively. The
expressions 𝐴𝑖 and 𝐴𝑖 indicate 𝜑 and 𝜓 , respectively.
   Consider the following situation:
                                                                           
                       ⊤                           ⊤                         ⊥
                𝑃1 =                       𝑄1 =                      𝑅1 =
                       ⊥                           ⊥                         ⊥
                                                                           
                       ⊤                           ⊤                         ⊤
                𝑃2 =                       𝑄2 =                      𝑅2 =         .
                       ⊥                           ⊥                         ⊥
We would like to construct a refinement such that 𝑅 2 (𝑥) ⇒ ⊥; this is impossible and 𝑥 = 0 is the
unique counterexample.
  RecMC maintains a set of queries, which are constraints that the process tries to make true. In
the current situation, it starts from the singleton {𝑅2 (𝑥) |= ⊥}.13
  The behaviour of RecMC can be understood as rewriting of approximations and queries. We
do not give the complete description of the rules, but readers familiar with RecMC should easily
understand which rule is rule at each step.
  RecMC first checks if 𝑅2 (𝑥) |= ⊥ by changing only 𝑅2 . It is impossible because
                                              𝑃1 (𝑥) ∧ 𝑄 1 (𝑥) ⇒ 𝑅2 (𝑥)
should hold, which requires ⊤ ∧ ⊤ ⇒ 𝑅2 (𝑥). The impossibility can be witnessed by the model
𝑀 (𝑥) = 1, which satisfies the left-hand-side (i.e. 𝑀 |= ⊤) and thus 𝑅2 (𝑥) but violates the requirement
(i.e. 𝑀 ̸ |= ⊥).
    So one needs to strengthen 𝑃1 and/or 𝑄 1 . For example, it may try to strengthen 𝑄 1 . In this case,
RecMC issues a new query 𝑄 1 (𝑥) |= 𝜓 1 (𝑥), where 𝜓 1 (𝑥) is obtained by the model-based projection:
                                             MBP ′ (𝑃 1 (𝑥) ∧ ¬⊥, {}, 𝑀).
By definition of MBP ′, we have 𝜓 1 (𝑥) = (𝑥 = 1). The new queries requires that 𝑄 1 (𝑥) does not
intersect with (𝑥 = 1), i.e. 𝑄 1 (𝑥) |= 𝑥 ≠ 1.
13 The representation of queries differs from that in [Komuravelli et al. 2016]. We describe a query by the condition

   ® |= 𝜑 (𝑥)
𝐴(𝑥)        ® that a predicate should satisfy, but [Komuravelli et al. 2016] represent it as a pair (𝐴(𝑥),
                                                                                                       ® ¬𝜑 (𝑥))
                                                                                                               ® expressing
that 𝐴 should not intersect with ¬𝜑 (i.e. |= ¬∃𝑥® .𝐴(𝑥)
                                                     ® ∧ ¬𝜑 (𝑥)).
                                                             ® The difference is not essential, as it is trivial to move from
one to the other by negating the formula.


                                  Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:34                                                                                                Takeshi Tsukada and Hiroshi Unno


  This requirement cannot be fulfilled because of ⊤ ⇒ 𝑄 (𝑥). This impossibility is recorded by
updating the underappoximation 𝑄 1 of 𝑄 1 , i.e. ⊤ ̸ |= 𝜓 1 (𝑥); it has the unique counter-model 𝑀 such
that 𝑀 (𝑥) = 1. Update of underapproximation also uses by model-based projection:
                                                 MBP ′ (⊤ ∧ ¬𝜓 1, {}, 𝑀),
which must be (𝑥 = 1) (since ⊤ ∧ ¬𝜓 1 denotes the singleton set {1}). Now
                                                     
                                                 ⊤
                                        𝑄1 =            .
                                               𝑥 =1
We remove the query 𝑄 1 (𝑥) |= 𝑥 ≠ 1, since it has been made clear that it cannot be fulfilled.
  We need to reconsider the query 𝑅2 (𝑥) |= ⊥. A model 𝑀 with 𝑥 = 1 is still a counterexample.
As the attempt to strengthen 𝑄 1 failed, we try to strengthen 𝑃 1 . In this case, RecMC issues a new
query 𝑄 1 (𝑥) |= 𝜗 1 (𝑥), where 𝜗 1 (𝑥) is obtained by the model-based projection:14
                                             MBP ′ (𝑄 1 (𝑥) ∧ ¬⊥, {}, 𝑀).
Since 𝑄 1 (𝑥) ∧¬⊥ is equivalent to 𝑥 = 1, we have 𝜗 1 (𝑥) = (𝑥 = 1). The new query is 𝑃1 (𝑥) |= ¬𝜗 1 (𝑥),
i.e. 𝑃 1 (𝑥) |= 𝑥 ≠ 1.
   One can strengthen 𝑃1 (𝑥) to meet the requirement (since 𝑥 = 0 ⇒ 𝑃1 (𝑥) is the unique constraint
for 𝑃1 ). Then RecMC strengthens 𝑃1 (𝑥) by conjoining an interpolation
                                                interpolation(⊥, 𝑥 ≠ 1).
Our interpolating theorem prover returns 𝑥 ≠ 1 as the interpolation (recall the assumption (11)).
The current approximations are
                                                                            
                    𝑥 ≠1                          ⊤                           ⊥
             𝑃1 =                       𝑄1 =                          𝑅1 =
                      ⊥                         𝑥 =1                          ⊥
                                                                            
                    ⊤                           ⊤                             ⊤
             𝑃2 =                       𝑄2 =                          𝑅2 =         .
                    ⊥                           ⊥                             ⊥

  As a result of the update of 𝑃1 (𝑥), we can update the over-approximation of 𝑅2 by an argument
similar to the case of 𝑃1 :
                                                                          
                     𝑥 ≠1                          ⊤                        ⊥
             𝑃1 =                         𝑄1 =                       𝑅1 =
                       ⊥                         𝑥 =1                       ⊥
                                                                              
                     ⊤                           ⊤                          𝑥 ≠1
             𝑃2 =                         𝑄2 =                       𝑅2 =            .
                     ⊥                           ⊥                            ⊥

However 𝑅2 (𝑥) still has infinite counterexamples to 𝑅2 (𝑥) |= ⊥.
  We can do the same for the model 𝑀 (𝑥) = 2. The new query 𝑄 1 (𝑥) |= 𝜓 2 (𝑥) is obtained by
model-based projection:
                                𝜓 2 (𝑥) = MBP ′ (𝑃1 (𝑥) ∧ ¬⊥, {}, 𝑀).
14 Here we use the underapproximation of 𝑄 to generate the query. The general rule is that, from a pair of a constraint

                                             𝐴1 (𝑥 1 ) ∧ · · · ∧ 𝐴𝑛 (𝑥 𝑛 ) ⇒ 𝐵 (𝑦)
a query 𝐵 ℓ (𝑦) |= 𝜑 (𝑦), a new query for 𝐴 𝑗 is obtained by model-based projection of
                               1                         𝑗 −1
                          𝐴ℓ −1 (𝑥 1 ) ∧ · · · ∧ 𝐴ℓ −1          ∧ 𝐴ℓ −1 𝑗 +1 ∧ · · · ∧ 𝐴ℓ −1 𝑛 (𝑥 𝑛 ) ∧ ¬𝜑 (𝑦).




Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Software Model-Checking as Cyclic-Proof Search                                                                   1:35


Since 2 is the minimum positive value satisfying 𝑃1 (𝑥) ∧ ¬⊥, we have 𝜓 2 (𝑥) = (𝑥 = 2) by the
definition of MBP ′. So model-based projection MBP ′ dose not generalise the counterexample in
this case. The new query leads to an update of 𝑄 1 , resulting in
                                                                           
                   𝑥 ≠1                             ⊤                        ⊥
            𝑃1 =                    𝑄1 =                            𝑅1 =
                     ⊥                      𝑥 = 1∨𝑥 = 2                      ⊥
                                                                             
                   ⊤                        ⊤                               𝑥 ≠1
            𝑃2 =                    𝑄2 =                            𝑅2 =            .
                   ⊥                        ⊥                                  ⊥
  We can then issue a new query 𝑃1 (𝑥) |= ¬𝜗 2 (𝑥) to 𝑃1 , where
                                   𝜗 2 (𝑥) = MBP ′ (𝑄 1 (𝑥) ∧ ¬⊥, {}, 𝑀)
with 𝑀 (𝑥) = 2. Note that 𝑄 1 (𝑥) ∧ ¬⊥ is equivalent to 1 ≤ 𝑥 ≤ 2. Since 2 is the maximum positive
integer satisfying 𝑄 1 (𝑥) ∧ ¬⊥, MBP ′ does not generalise the model 𝑀 (𝑥) = 2 even in this case. So
𝜗 2 (𝑥) = (𝑥 = 2). This query causes update of the over-approximation of 𝑃1 , and then 𝑅2 :
                                                                           
               𝑥 ≠ 1∧𝑥 ≠ 2                          ⊤                       ⊥
        𝑃1 =                          𝑄1 =                          𝑅1 =
                     ⊥                        𝑥 = 1∨𝑥 = 2                   ⊥
                                                                                       
               ⊤                              ⊤                             𝑥 ≠ 1∧𝑥 ≠ 2
        𝑃2 =                          𝑄2 =                          𝑅2 =                      .
               ⊥                              ⊥                                    ⊥
  The same argument for the counterexample 𝑀 (𝑥) = 3, we reaches
                                                                    
       𝑥 ≠ 1∧𝑥 ≠ 2∧𝑥 ≠ 3                       ⊤                      ⊥
𝑃1 =                           𝑄1 =                            𝑅1 =
               ⊥                      𝑥 = 1∨𝑥 = 2∨𝑥 = 3               ⊥
                                                                                   
       ⊤                              ⊤                               𝑥 ≠ 1∧𝑥 ≠ 2∧𝑥 ≠ 3
𝑃2 =                           𝑄2 =                            𝑅2 =
       ⊥                              ⊥                                       ⊥
and this process can continue indefinitely.




                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
