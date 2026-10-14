                                                             T RANSITION -O RIENTED P ROGRAMMING :
                                                           D EVELOPING P ROVABLY C ORRECT S YSTEMS

                                                                                               A P REPRINT


                                                                                             Yepeng Ding*
                                                                                        The University of Tokyo
                                                                                  yepengding@g.ecc.u-tokyo.ac.jp
arXiv:2009.06029v3 [cs.PL] 22 Feb 2024




                                                                                               A BSTRACT
                                                   Correctness is a necessary condition for systems to be effective in meeting human demands, thus
                                                   playing a critical role in system development. However, correctness often manifests as a nebulous
                                                   concept in practice, leading to challenges in accurately creating specifications, effectively proving
                                                   correctness satisfiability, and efficiently implementing correct systems. Motivated by tackling these
                                                   challenges, this paper introduces Transition-Oriented Programming (TOP), a programming paradigm
                                                   to facilitate the development of provably correct systems by intertwining correctness specification,
                                                   verification, and implementation within a unified theoretical framework.
                                                   This paper establishes a formalized foundation for correctness with formal models and formal logics.
                                                   Based on this foundation, this paper introduces Graph Transition Systems (GTSs), a formalism
                                                   proficient in capturing stateful dynamics and structural transformations of systems. The core features
                                                   of TOP in practice are centered around GTSs, including progressive specification, modularization,
                                                   context perception, and proof automation.
                                                   These features are exemplified through practical examples programmed in Seni, a fully-fledged
                                                   TOP language. The Seni language excels at intuitively constructing GTSs and articulating tempo-
                                                   ral and functional properties. It combines bottom-up (modularization) and top-down (progressive
                                                   specification) approaches to improve development efficiency via model refinement, parameteriza-
                                                   tion, integration, and composition. Seni also incorporates context perception that introduces type
                                                   refinement and transformation prioritization to improve the precision of specifications and efficiency
                                                   of verification processes. Besides, Seni leverages bounded model checking and iterative deepening
                                                   theorem proving techniques in correctness verification to automate proofs at compile time.
                                                   Furthermore, this paper demonstrates the applicability of TOP in diverse practical scenarios. It
                                                   introduces transition-oriented development, a development process aligned with the principles of TOP
                                                   to develop provably correct distributed protocols. It also elaborates on transition-oriented security
                                                   analysis for security infrastructures against threat models, exemplified by a security framework for
                                                   self-sovereign identity systems. Additionally, this paper presents transition-oriented program analysis,
                                                   exemplified by context-sensitive concolic verification, for uncovering vulnerabilities in decentralized
                                                   applications, particularly in decentralized finance protocols. These applications underscore the
                                                   potential of TOP in addressing the real-world challenges of developing provably correct systems.
                                                   This paper concludes with a summary of its contributions, followed by a detailed discussion on
                                                   broadening the applicability of extending TOP in compiling tool development, explainable artificial
                                                   intelligence, and hardware design, alongside the future directions of TOP and the Seni language.

                                         Keywords Transition-oriented programming · Formal methods · Software engineering · Information security ·
                                         Distributed computing




                                           ∗
                                               https://yepengding.github.io/
                                               Transition-Oriented Programming                                    A P REPRINT



    1   Introduction

    Systems are developed to meet human demands. A system is a group of interconnected elements acting as a unified
    whole to satisfy its specification that formalizes human demands. Consequently, a system is effective if

           • Expressiveness its specification accurately describe a human demand, and
           • Correctness it satisfies its specification.

    However, human demands are subjective and not always precisely describable in languages that humans and machines
    can understand, making the expressiveness proof an open philosophical challenge. Nevertheless, the correctness proof
    concerning the objective satisfaction relation is an approximately solvable problem. Therefore, a system is correct if it
    satisfies its specification, regardless of whether it meets human demands or not.
    In software development, demand analysis is indispensable yet remains a formidable challenge regarding soundness and
    completeness. This difficulty stems primarily from the diverse and dynamic nature of user demands, coupled with the
    constraints of limited analysis resources Leffingwell and Widrig [2000]. Despite diligent efforts in demand analysis, the
    resultant requirement specifications, though meticulously documented and formalized, inevitably fall short of meeting
    all user demands perpetually. Consequently, the efficacy of software is inherently time-bound and user-specific, even
    when it adheres to the correctness condition.
    This paper delves into the concept of correctness within the context of computer science and engineering, while
    acknowledging the challenge of the expressiveness proof in this specific academic field. The focus is predominantly on
    programs as exemplars of computer systems, although the discourse is applicable to other system typologies. At its
    core, the paper contends that a program’s correctness is contingent upon the satisfaction of its requirement specification.
    However, this premise gives rise to two pivotal questions as follows.

        Q1 How to define languages for specification?
        Q2 How to prove correctness satisfiability?

    Q1 and Q2 are intertwined, as the selection of a specification language is crucial for proving correctness satisfiability.
    While natural languages can be used for program specification, their inherent ambiguity and lack of verifiability
    pose significant challenges. To illustrate, consider the program presented in Listing 1, which is a distilled version of
    real-world incidents, notably the 2018 BeautyChain hack. A specification about this program, stating "The execution of
    function process yields a result where x is greater than 0", may seem clear but harbors ambiguity. It could be interpreted
    in multiple ways, such as ∀t ∈ [0, 2256 ) : process(t) =⇒ x > 0, ∃t ∈ [0, 2256 ) : process(t) =⇒ x > 0, and
    ∀t ∈ [0, 28 ) : process(t) =⇒ x > 0. Each interpretation significantly alters the perceived behavior of the program,
    thereby accentuating the critical need for precise and rigorous specification languages.

                                      Listing 1: Pseudocode of a vulnerable smart contract.
1   public uint8 x := 1;
2   function process(uint256 t) −> uint8 {
3       for i in [0..t):
4            x := x + 1;
5       return x;
6   }
7
8   process(Random.UINT256)

    Moreover, the verifiability of specification languages, particularly conducive to automated verification, is paramount.
    The reliance on manual proofs for correctness satisfiability is fraught with challenges, especially when dealing with
    extensive inputs and outputs, due to the high risk of human error and the impracticality of mental computation. Taking
    the example of the simple program outlined in Listing 1, even a seemingly straightforward manual proof for the
    specification ∀t ∈ [0, 2256 ) : process(t) =⇒ x > 0 can be problematic. A plausible proof constructed on the premises
    that x = 1 + t and t ≥ 0 to deduce that x > 0, however, is flawed. For instance, when t = 28 − 1, it results in x = 0
    due to integer overflow, a typical issue overlooked in manual proofs. Besides, the variable x is publicly accessible and
    subject to modification by other functions, which adds another layer of complexity to the proof. The limitations of
    manual proofs in such scenarios underscore the necessity for automated verification. In conjunction with precise and
    verifiable specifications, automated verification has the potential to navigate through the complexities of efficiently
    constructing reliable proof.


                                                                2
                                           Transition-Oriented Programming                                    A P REPRINT



Formal languages, exemplified by representing programs as either transition systems or rewriting systems, can effectively
mitigate ambiguity and enhance verifiability. However, these models of computation are incomparable, as each of them
has unique strengths in representing different aspects of programs. Generally, program specifications can be categorized
into temporal and functional properties. Transition systems are adept at capturing stateful dynamics, representing
changes in system states with respect to time, exemplified by properties like "There exists an execution path of function
process where x ≥ 0 eventually holds", i.e., ∃3(x ≥ 0). These properties are commonly verified by model checking
Baier and Katoen [2008], Clarke Jr et al. [2018] (e.g., SPIN Holzmann [1997], NuSMV Cimatti et al. [2002], CBMC
Kroening and Tautschnig [2014]) and concolic execution Baldoni et al. [2018] (e.g., PathFinder Visser et al. [2004],
KLEE Cadar et al. [2008], PyExZ3 Irlbeck [2015]) techniques.
Conversely, rewriting systems are tailored to the representation of structural transformations with respect to rules,
suitable for specifying functional properties such as process(v+1) = process(v)+1. These properties are predominantly
verified by theorem proving Bibel [2013] (Isabelle Paulson [1994], F* Swamy et al. [2016], Lean Moura and Ullrich
[2021]) and term rewriting Baader and Nipkow [1998] techniques (AProVE Giesl et al. [2004], TNT Gupta et al. [2008],
TTT Korp et al. [2009]). The incomparable expressiveness requires considerable effort, such as selecting and mastering
appropriate languages and tools, for both specification and verification.
Therefore, an intuitive answer to Q1 and Q2 is to define a specification language that is comprehensible to humans and
processable by machines. Such a language should be precise and concise to reflect human demands, while also being
computable and verifiable to automate correctness satisfiability proving. Nevertheless, in practical scenarios, repairing
erroneous programs to preserve specific properties often involves arduous efforts and introduces new complexities
and risks. For the vulnerable smart contract presented in Listing 1, modifying the variable type of x to uint256 seems
a viable solution to the integer overflow issue and fulfilling the specification ∀t ∈ [0, 28 ) : process(t) =⇒ x ≥ 0.
However, this modification is fraught with risks and incurs significant costs. For instance, x may only be adequate for
other functions with type uint8. Besides, altering its type not only increases gas consumption but may also disrupt the
storage layout of the deployed smart contract, potentially leading to malfunctions. Consequently, our focus may shift
towards the following question.

    Q3 How to implement correct systems?

Q3 presents a harder question on account of the fact that an effective and efficient solution to Q3 implies an effective
solution to Q2. In practice, system complexity is escalating rapidly to accommodate a variety of demands, propelled by
advancements in Information and Communications Technologies (ICTs), which, in turn, catalyze significant societal
shifts, as evidenced in Industry 4.0 and Web 3.0. The increasing complexity carries the promise of enriching user
experience, streamlining functionalities, and spawning innovative solutions, thereby bolstering productivity across
various domains. Industry 4.0, characterized by the integration of cyber-physical systems Baheti and Gill [2011], Lee
[2015], the Internet of Things (IoT) Da Xu et al. [2014], Li et al. [2015], artificial intelligence Jordan and Mitchell
[2015], Mahesh [2020], and cloud computing Dillon et al. [2010], Mao et al. [2017], is transforming traditional
manufacturing processes into smart, interoperable systems. Simultaneously, Web 3.0 is reshaping the landscape of the
Internet by advocating decentralized, personalized, and intelligent systems Ding and Sato [2020a,b, 2023a] through
blockchain Wood [2014], Nakamoto [2019], Zheng et al. [2018] and extended reality Ratcliffe et al. [2021] technologies.
Therefore, for Q3, intuitively, an implementation of a correct system should not only adhere to its specified requirements
but also be cost-effective. This consideration becomes particularly crucial in large-scale and complex systems, where
the complexity of individual components and their interactions necessitates a systematic method to balance correctness
and cost. Additionally, correctness satisfiability may not be theoretically provable for implementations in cases like
those involving undecidable problems. Therefore, an implementation is provably correct if and only if its correctness
satisfiability is provable.
As illustrated in Figure 1, only a subset of human demands is specifiable by a specification language. However,
an effective response to Q1 holds the potential to expand this subset to approximate the human demands, thereby
amplifying correctness specifiability. Besides, only a subset of these specifications is technically provable. Nonetheless,
an effective and efficient solution to Q2 can streamline the establishment of correctness, thereby enhancing correctness
verifiability. Furthermore, among the specifications that are technically provable, only a subset proving to be correct is
practically implementable in a manner that produces provably correct systems. Addressing Q3 effectively and efficiently
can extend the set of provably correct systems, consequently advancing correctness implementability. This hierarchical
interplay highlights the nuanced and interconnected nature of human demands, specifications, provable specifications,
and provably correct systems.
This paper is primarily driven by the objective of addressing Q1, Q2, and Q3. It commences with a formalization of
correctness by a systematic illustration of formal models and logic. The formalization streamlines the representations


                                                            3
                                            Transition-Oriented Programming                                    A P REPRINT




        Figure 1: Inclusion of demands, specifications, provable specifications, and provably correct systems.


of transition systems and rewriting systems, along with their typical variants, thereby laying a foundation for the
subsequent discussions.
Central to this paper is the introduction of Transition-Oriented Programming (TOP), a novel programming paradigm
designed to facilitate the development of provably correct systems. The essence of TOP lies in intertwining specification,
verification, and implementation within a singular theoretical framework, which ensures that a provably correct
specification is also a provably correct implementation. The theoretical underpinnings of TOP are grounded in
the concept of Graph Transition Systems (GTSs) that are adept at capturing both stateful dynamics and structural
transformations inherent in complex systems. Additionally, TOP is distinct in its intrinsic support for correctness
verification to prove correctness satisfiability regarding the formulated GTSs associated with temporal and functional
properties. The correctness verification follows the principles of the established model-checking and theorem-proving
techniques with tailored adaptations for application to GTSs. Moreover, TOP bridges the gap between formal models
and practical implementations. Formal models are not only immediately executable but are also capable of handling
side effects with practical refinements effectively, thereby marking a stride toward applicability and usability in practice.
This paper also introduces the Seni language, a TOP language with fully-fledged TOP features. Seni is designed to
facilitate the intuitive construction of GTSs and the expressive formulation of both temporal and functional properties. A
distinctive feature of Seni is its integration of both bottom-up (modularization) and top-down (progressive specification)
approaches to optimize the specification process. Modularization is geared toward amplifying scalability and reusability
by enabling model parameterization and composition. In parallel, progressive specification is augmented by model
refinement techniques, fostering an iterative and incremental methodology for both model and property specification and
enabling verification at multiple abstract levels. Besides, Seni incorporates context perception, a feature that improves
specification precision and verification efficiency via type refinement and transformation prioritization. Furthermore,
Seni stands out by offering intrinsic support for correctness verification at compile time, leveraging fully automated
bounded model checking and iterative deepening theorem proving techniques.
Additionally, this paper discusses the applicability of TOP through three application scenarios, including transition-
oriented development of distributed protocols, transition-oriented security analysis of security infrastructures, and
transition-oriented program analysis of decentralized applications. It further envisions the potential of TOP in compiling
tool development, explainable artificial intelligence, and hardware design.




                                                             4
                                               Transition-Oriented Programming                                  A P REPRINT



2     Correctness
A system is correct if it satisfies its specification. A specification uses a language to describe a set of properties that a
system needs to hold. Intriguingly, specifications themselves can be represented through systems. Consequently, system
correctness is a type of satisfaction relation between two systems.
However, practical systems, such as computer programs, usually manifest a significant degree of complexity and
encompass numerous details that are extraneous to their correctness. In contrast, succinct and expressive specifications
are paramount for articulating the necessary system properties. This dichotomy underscores the indispensable role of
formal models and formal logic in formalizing and practicalizing correctness.
Intuitively, system correctness revolves around two fundamental operations: verification and implementation. Verifica-
tion entails the rigorous process of proving correctness satisfaction, whereas implementation refers to the development
of a system according to its specifications.
This section formalizes correctness to elucidate the essence of Q1, Q2, and Q3 as introduced in Section 1 with formal
models and formal logic as preliminaries.

2.1     Formal Model

Formal models are essential in abstracting complex systems. Given that computer programs represent computations,
models of computation serve as appropriate abstractions for these programs.
A model of computation is a formal system that specifies the mechanism of a function producing an output for an input.
Such formal systems play a pivotal role in program analysis, as they provide a foundational basis to which all computer
programs can be theoretically reduced. This section presents two representative models of computation: transition
system and rewriting system.

2.1.1    Transition System
Basic Transition System A transition system, formally defined in Definition 2.1, is a model of computation to specify
states and their dynamic transitions.
Definition 2.1 (Transition System). A Transition System (TS) is a pair
                                                           ⟨S, →⟩

        • S is a set of states, and
        • → ⊆ S × S is a transition relation.
Example 2.1 (Transition System). A transition system example is visualized in Figure 2a, where S = {s0 , s1 , s2 } and
→ = {(s0 , s1 ), (s0 , s2 )}.




              (a) Transition system example.                                  (b) Labeled transition system example.
                                         Figure 2: Examples of transition systems.

Many variants of transition systems have emerged from Definition 2.1 to accommodate a wide range of scenarios,
such as labeled transition systems in Definition 2.2, Kripke structure in Definition 2.3, and labeled Kripke structure in
Definition 2.4.
Labeled transition systems, formally defined in Definition 2.2, introduce the label set to represent elements varying with
contexts, such as inputs to consume, conditions to trigger transitions, actions performed during transitions, and effects
emitted after the transition.


                                                             5
                                              Transition-Oriented Programming                                  A P REPRINT




             (a) Kripke structure example.                                   (b) Labeled Kripke structure example.
                                        Figure 3: Examples of Kripke structures.


Definition 2.2 (Labeled Transition System). A Labeled Transition System (LTS) is a triple
                                                         ⟨S, L, →⟩

       • S is a set of states,
       • L is a set of labels, and
      • → ⊆ S × L × S is a transition relation.
Example 2.2 (Labeled Transition System). An example of a labeled transition system is depicted in Figure 2b, where
S = {s0 , s1 , s2 }, L = {l0 , l1 }, and → = {(s0 , l0 , s1 ), (s0 , l1 , s2 )}.

While LTSs focus on state changes via introducing labels over transitions, Kripke structures, formally defined in
Definition 2.3, abstract away specific transitions and focus on state properties by assigning atomic propositions to states.

Kripke Structure
Definition 2.3 (Kripke Structure). A Kripke Structure (KS) over set A of atomic propositions is a quadruple
                                                       ⟨S, 0S, →, L⟩

       • S is a set of states,
       • 0S ⊆ S is a set of initial states,
       • → ⊆ S × S is a transition relation, and
        • L : S 7→ ℘(A) is a total labeling function.
Example 2.3 (Kripke Structure). Figure 3a illustrates a Kripke structure over A = {a0 , a1 , a2 , a3 }, where S =
{s0 , s1 , s2 }, 0S = {s0 }, → = {(s0 , s1 ), (s0 , s2 )}, and L relates a set atomic propositions in curly brackets to a
corresponding state, such as L(s0 ) = {a0 , a1 }.

Combining the characteristics of LTSs and KSs, labeled Kripke structures, formally defined in Definition 2.4, have both
labels over transitions and atomic propositions assigned to states.
Definition 2.4 (Labeled Kripke Structure). A Labeled Kripke Structure (LKS) over set A of atomic propositions is a
quintuple
                                                   ⟨S, 0S, L, →, L⟩

       • S is a set of states,
       • 0S ⊆ S is a set of initial states,
       • L is a set of labels,
       • → ⊆ S × L × S is a transition relation,
       • L : S 7→ ℘(A) is a total labeling function.


                                                             6
                                             Transition-Oriented Programming                                   A P REPRINT



A LKS is terminal if it contains a terminal state, i.e., ∃s ∈ S : S(s) = ∅.
Example 2.4 (Labeled Kripke Structure). An example of a LKS over A = {a0 , a1 , a2 , a3 } is visualized in Figure 3b.
It retain the same sets S, 0S, and function L as defined in Example 2.3, while adopting the L and → from Example 2.2.
This LKS models interactive state changes governed by L in a system. When l0 is activated, the system transitions from
the initial state s0 to s1 . Similarly, the activation of l1 results in a transition from s0 to s2 .

2.1.2   Rewriting System
Basic Rewriting System An abstract rewriting system, formally defined in Definition 2.5, is a model of computation
to specify structures and their transformation rules.
Definition 2.5 (Abstract Rewriting System). An Abstract Rewriting System (ARS) is a pair
                                                          ⟨S, →⟩

        • S is a set of structures, and
        • → ⊆ S × S is a transformation relation containing a set of rules.

We can observe that Definition 2.5 of ARSs aligns with Definition 2.1 of TSs, despite differing terminologies. While
TSs emphasize specific state transitions, ARSs focus on the transformation rules governing transitions.
Example 2.5 (Abstract Rewriting System). An example of an ARS is shown in Figure 4a, where S is a set of objects
{◦, □, △} and → = {r0 , r1 }. Rule r0 transforms ◦ into □, while rule r1 transforms △ to □.




          (a) Abstract rewriting system example.                               (b) Term rewriting system example.
                                          Figure 4: Examples of rewriting systems.

Theoretically, ARS structures can represent various mathematical objects, including terms and graphs. A term rewriting
system and a graph rewriting system are defined in Definition 2.6 and Definition 2.10 respectively.
Definition 2.6 (Term Rewriting System). A Term Rewriting System (TRS) over set F of function symbols and set V
of variables, where F ∩ V = ∅, is a pair
                                                  ⟨S, →⟩

        • S ⊆ Term(F, V ) is a set of terms defined inductively:
            – V ⊆ Term(F, V ),
            – ∀f ∈ F i : f (t1 , . . . , ti ) ∈ Term(F, V ), where F i , i ∈ N is the set of i-ary function symbols, and
              t1 , . . . , ti ∈ Term(F, V ).
        • → ⊆ S × S is a transformation relation.
Example 2.6 (Term Rewriting System). Figure 2.6 depicts an example of a TRS over F = {+, 0, Su} and V = {x, y},
where S = { + (x, 0), x, +(x, Su(y)}, and → = {r0 , r1 } = {(+(x, 0), x), (+(x, Su(y)), Su(+(x, y)))}.
This TRS models the binary addition function of natural numbers. For instance, the initial term +(Su(0), Su(0)) is
utilized to compute 1 + 1, where Su(0) represents the natural number 1 by the unary successor function Su. The
computational (rewriting) process involves sequentially applying the transformation rules defined in → to the initial
term, as exemplified in the computation of 1 + 1 as follows.
                                   +(Su(0), Su(0)) −→ Su(+(Su(0), 0)) −→ Su(Su(0))
                                                     r1                   r0

The process terminates when no further rules in → can be applied to the term. In this case, the process terminates with
the term Su(Su(0)) representing the natural number 2.


                                                             7
                                              Transition-Oriented Programming                                        A P REPRINT



Graph Rewriting System Terms can be represented by node-labeled graphs defined in Definition 2.7.
Definition 2.7 (Node-Labeled Graph). A Node-Labeled Graph (NLG) over set F of function symbols and set V of
variables, where F ∩ V = ∅ is a quadruple
                                              ⟨N, 0 n, L, S⟩
         • N is a set of nodes,
         • 0 n ∈ N is the root,
         • L : N 7→ F ∪ V is a total labeling function, and
         • S : N 7→ N ∗ is a partial successor function well-defined for all n ∈ N such that L(n) ∈ F , where N ∗ is the
           Kleene closure of N .
A NLG is closed if V = ∅ or ∀n ∈ N : L(n) ∈ F . Thus, a Closed NLG (CNLG) is a quadruple
                                                          ⟨N, 0 n, L, S⟩
         • N is a set of nodes,
         • 0 n is the root,
         • L : N 7→ F is a total labeling function, and
         • S : N 7→ N ∗ is a total successor function.
A subgraph g/ 0 n′ of a NLG g rooted at 0 n′ is a NLG
                                                        ⟨N ′ , 0 n′ , L′ , S ′ ⟩
         • N ′ ⊆ N is a set of nodes reachable by paths from 0 n′ ,
         • 0 n′ is the root,
         • L : N ′ 7→ F ∪ V is a total labeling function, and
         • S : N ′ 7→ N ′∗ is a partial successor function well-defined for all n ∈ N ′ such that L(n) ∈ F .
A node n is a function node if L(n) ∈ F and a variable node if L(n) ∈ V . For any NLG g, Function(g) = {L(n) ∈
F | n ∈ N }, Variable(g) = {L(n) ∈ V | n ∈ N }.
This paper uses a simple language to describe NLGs, as detailed in Definition 2.8.
Definition 2.8 (Language for Node-Labeled Graphs). The Extended Backus-Naur Form (EBNF)2 standardized in
ISO/IEC 14977 of the language for NLGs is defined as follows.
                      NLG = ["^"], Node | Node, "⊕", NLG
                      Node = Function, "(", {Node}, ")" | ID | ID, "[", Function, "(", {Node}, ")", "]"
Here, ^ identifies a node as the root and must occur exactly once. ⊕ denotes a graph concatenation operation. Function
ranges over F , and ID ranges over a set of identifier symbols such that F ∩ID = ∅ and V ⊆ ID. Besides, for any identifier
symbol appearing in a graph, this symbol must occur exactly once in the form ID, "[", Function, "(", {Node}, ")", "]".
For brevity, a nullary (0-ary) function Function() is abbreviated as Function.
Example 2.7 (Terms as Graphs). The term +(Su(0), Su(0)) in Example 2.6 can be represented as a
NLG defined in Definition 2.7 over F and V , where N = { 0 n, n1 , n2 , n3 , n4 }, n0 = 0 n, L =
{( 0 n, +), (n1 , Su), (n2 , Su), (n3 , 0), (n4 , 0)}, and S = {( 0 n, {n1 , n2 }), (n1 , {n3 }), (n2 , {n4 })}. By Definition 2.8,
we can describe the NLG by +̂(Su(0()), Su(0())), abbreviated to +̂(Su(0), Su(0)) and visualized in Figure 5a. Notably,
this is to be distinguished from +̂(1[Su(0)], 1), as visualized in Figure 5b.
Definition 2.9 (Node-Labeled Graph Homomorphism). A node-labeled graph homomorphism g0 ; g1 from a NLG
g0 = ⟨N0 , 0 n0 , L0 , S0 ⟩ to g1 = ⟨N1 , 0 n1 , L1 , S1 ⟩ over F and V , where F ∩ V = ∅, is a function H : N0 7→ N1 , such
that H( 0 n0 ) = 0 n1 , and for all n ∈ N0 , L0 (n) ∈ F ,
         • L1 (H(n)) = L0 (n), and
   2
       https://www.iso.org/standard/26153.html


                                                                   8
                                             Transition-Oriented Programming                                          A P REPRINT




        (a) Node-labeled graph +̂(Su(0), Su(0)).                                   (b) Node-labeled graph +̂(1[Su(0)], 1).
                                       Figure 5: Examples of node-labeled graphs.


       • For each i-th element ni ≜ S0 (n)[i] in S0 (n), H(ni ) = S1 (H(n))[i], where 1 ≤ i ≤ |S0 (n)|.
Definition 2.10 (Graph Rewriting System). A Graph Rewriting System (GRS) over set F of function symbols and set
V of variables, where F ∩ V = ∅, is a pair
                                                   ⟨S, →⟩

       • S ⊆ NLG(F, V ) is a set of NLGs over F and V as per Definition 2.7, and
       • → ⊆ S × N is a transformation relation, such that ∀s ∈ S : (s, n) ∈ → =⇒ n ∈ N ∧ n ̸= 0 n, where
         s = ⟨N, 0 n, L, S⟩.

A transformation rule (s, n) ∈ → is applicable to a graph g if s/ 0 n ; g, as per Definition 2.9, with n the post-
transformation root.
Definition 2.11 (NLG Rewriting). NLGRewrite : G × G̃ × Ñ 7→ G is a rewriting function, where G, G̃ ⊆ NLG(F, V ),
∀g̃ ∈ G̃, g̃ = ⟨Ñ , L̃, 0˜n, S̃⟩ : (g̃, ñ) ∈ G̃ × Ñ =⇒ ñ ∈ Ñ ∧ ñ ̸= 0˜n, and ∀g ∈ G : ∃(g̃, ñ) ∈ G̃ × Ñ : g̃/ 0˜n ; g.
Function NLGRewrite(⟨N, L, 0 n, S⟩, ⟨Ñ , L̃, 0˜n, S̃⟩, ñ) contains three steps as follows.

      1. Construct g1 ≜ ⟨N1 , 0 n1 , L1 , S1 ⟩ by adding an isomorphic copy of Ñg̃/ñ \ Ñg̃/ 0˜n to g.

            • N1 = N ⊎ (Ñg̃/ñ \ Ñg̃/ 0˜n ),
            • 0 n1 = 0 n,
            • The labeling function
                                                              (
                                                                  L(n), n ∈ N
                                                   L1 (n) =
                                                                  L̃(n), n ∈ Ñg̃/ñ \ Ñg̃/ 0˜n

            • The successor function
                                              
                                              S(n)[i],
                                                           n∈N
                                   S1 (n)[i] = S̃(n)[i],    n, S̃(n)[i] ∈ Ñg̃/ñ \ Ñg̃/ 0˜n
                                              H(S̃(n)[i]), n ∈ Ñ
                                                                   g̃/ñ \ Ñg̃/ 0˜n , S̃(n)[i] ∈ Ñg̃/ 0˜n
                                              


      2. Construct g2 ≜ ⟨N2 , 0 n2 , L2 , S2 ⟩ by substituting all references to H( 0˜n) with references to ñ in g1 .
            • N2 = N1 ,
            •
                                                              (
                                                      0        ñ,    0
                                                                        n1 = H( 0˜n)
                                                          n2 = 0
                                                                 n1 , otherwise

            • L2 = L1 ,


                                                                  9
                                           Transition-Oriented Programming                                     A P REPRINT



            •
                                                         (
                                                          ñ,        S1 (n)[i] = H( 0˜n)
                                             S2 (n)[i] =
                                                          S1 (n)[i], otherwise

     3. Construct g3 = g2 / 0 n2 by deriving the subgraph of g2 rooted at 0 n2 , as per Definition 2.7.
Example 2.8 (Graph Rewriting System). An example of a graph rewriting system functioning the same as the TRS in
Example 2.6 is depicted in Figure 6, where S consist of two NLGs s0 = +̂(x, 0) and s1 = +̂(x, Su(y)) ⊕ Su(+(x, y)),
and → = {(s0 , n0′           1′
                 0 ), (s1 , n0 )}.




                                       Figure 6: Graph rewriting system example.

Given an initial graph g0 = +̂(Su(0), Su(0)), the rewriting process sequentially applies transformation rules to g0 if there
is a homomorphism from the NLG of a rule to g0 . The process continues until no further homomorphisms are possible.
                                                                                                     ˆ
For instance, by function NLGRewrite Definition 2.11, r1 is first applied to g0 and produces g1 = Su(+(Su(0),      0)) due
                             1
to the homomorphism s1 /n0 ; g0 as per Definition 2.9. Then applying r0 transforms g1 to g2 = Su(Su(0))  ˆ           due to
s0 /n00 ; g1 . As no more homomorphisms exist, the process terminates with g2 representing the natural number 2.
Notably, graphs of GRSs can inherently represent shared and cyclic structures, where a node may have multiple
predecessors. In contrast, TRSs, with their tree-like structures, cannot naturally represent a shared structure.

2.1.3   Incomparability
Transition systems and rewriting systems have their own advantages in abstraction. Transition systems are powerful in
expressing stateful and temporal dynamics to define how a system operates step by step, while rewriting systems excel
in expressing functional structure transformations to define what a system operates.
In Example 2.9, transition systems prove to be convenient in modeling stateful dynamics.
Example 2.9 (Variable Assignment). Value assignment is a common operation in imperative programming languages.
For an operation where a variable x is assigned the value of x + 1, a transition system offers a convenient and intuitive
representation through the transition relation x → x + 1.
In contrast, the representation of this operation in a rewriting system introduces complexity, particularly in terms of
encoding state context information to control termination. The complexity becomes increasingly notable with the
escalation in the number of variables and the application of system compositions.
However, rewriting systems are convenient in modeling functional structure transformations, as shown in Example 2.10.
Example 2.10 (Y Combinator). The Y combinator is a higher-order function to implement recursion in languages
without native support for recursive functions. In untyped lambda calculus, the Y combinator is typically represented as
λf.(λx.f (x x)) (λx.f (x x)).
While formulating a transition system to model the Y combinator in a succinct way is challenging due to its potential to
generate an infinite number of states, a TRS ⟨S, →⟩ over F = {Y } and V = {f }, as defined in Definition 2.6, can
succinctly model the Y combinator, where S = {Y (f ), f (Y (f ))}, → = {(Y (f ), f (Y (f ))}.
Therefore, transition systems are widely used in imperative programming (e.g., how a variable value changes from state
to state in Java), while rewriting systems are widely used in functional programming (e.g., what a pure function does in
Haskell).


                                                            10
                                          Transition-Oriented Programming                                   A P REPRINT



A program can be modeled in different formal models depending on contexts, as discussed in Section 2.1.3. Even with
the same formal model, a program can be modeled in different ways. Some models are concrete with many details,
while some models are rather abstract with a specific focus. For example, at the syntactic level, a program can be
modeled by a parse tree (concrete model) or an abstract syntax tree (abstract model).

2.2     Formal Logic

Formal logic is important in specifying system properties. Although formal models introduced in Section 2.1 can be
used to specify properties, formal logic is more expressive and succinct. This section presents two representative formal
logic: temporal logic and Hoare logic.

2.2.1    Temporal Logic
Temporal logic formulates temporal properties to reason about stateful dynamics regarding linear or branching time,
particularly for transition systems.

Linear-Time Logic
Definition 2.12 (Linear Temporal Logic). Linear Temporal Logic (LTL) is a linear-time temporal logic. The syntax
of LTL formulae over set A of atomic propositions is defined as
                                      ϕ ::= ⊤ | a | ϕ0 ∧ ϕ1 | ¬ϕ | ⃝ϕ | ϕ0 Uϕ1 ,
where a ∈ A.
Temporal modalities 3 and 2 are derived from U and defined as follows.
                                                      3ϕ ≜ ⊤Uϕ
                                                      2ϕ ≜ ¬3¬ϕ

Branching-Time Logic
Definition 2.13 (Computation Tree Logic). Computation Tree Logic (CTL) is a branching-time logic. The syntax of
CTL formulae over set A of atomic propositions is defined as
                                         ϕ ::= ⊤ | a | ϕ0 ∧ ϕ1 | ¬ϕ | ∃φ | ∀φ
where a ∈ A and φ is formed by
                                                    φ ::= ⃝ϕ | ϕ0 Uϕ1

Temporal modalities 3 and 2 are defined as follows.
                                                     ∃3ϕ ≜ ∃(⊤Uϕ)
                                                     ∀3ϕ ≜ ∀(⊤Uϕ)
                                                     ∃2ϕ ≜ ¬∀3¬ϕ
                                                     ∀2ϕ ≜ ¬∃3¬ϕ


The release operator R is defined as follows:
                                           ∃(ϕ0 Rϕ1 ) = ¬∀((¬ϕ0 )U(¬ϕ1 ))
                                           ∀(ϕ0 Rϕ1 ) = ¬∃((¬ϕ0 )U(¬ϕ1 ))


Definition 2.14 (Universal Fragment of Computation Tree Logic). The universal fragment of CTL (UCTL) over set
A of atomic propositions is a fragment of CTL in Definition 2.13 without existential path quantifiers. The syntax of
UCTL formulae over set A of atomic propositions is defined as
                                    ϕ ::= ⊤ | ⊥ | a | ¬a | ϕ0 ∧ ϕ1 | ϕ0 ∨ ϕ1 | ∀φ
where a ∈ A and φ is formed by
                                                φ ::= ⃝ϕ | ϕ0 Uϕ1 | ϕ0 Rϕ1


                                                           11
                                           Transition-Oriented Programming                                          A P REPRINT



 Definition 2.15 (Existential Fragment of Computation Tree Logic). The existential fragment of CTL (ECTL) over set
 A of atomic propositions is a fragment of CTL in Definition 2.13 without universal path quantifiers. The syntax of
 ECTL formulae over set A of atomic propositions is defined as
                                    ϕ ::= ⊤ | ⊥ | a | ¬a | ϕ0 ∧ ϕ1 | ϕ0 ∨ ϕ1 | ∃φ
 where a ∈ A and φ is formed by
                                             φ ::= ⃝ϕ | ϕ0 Uϕ1 | ϕ0 Rϕ1

 2.2.2    Equational Logic
 Equational logic formulates functional properties to reason about structural transformations via equations, particularly
 for rewriting systems.
 Definition 2.16 (Equational Logic). Equational logic over set F of function symbols and set V of variables is a
 fragment of first-order logic (FOL) where formulae are formed by equations between structures (e.g., Term(F, V ) in
 Definition 2.6, NLG(F, V ) in Definition 2.10). An equation is an ordered pair of structures denoted in the form of
 s0 ≈ s1 . The syllogisms are defined below.

                                           s0 ≈ s1                              s0 ≈ s1 , s1 ≈ s2
              s ≈ s Reflexivity            s1 ≈ s0    Symmetry                       s0 ≈ s2             Transitivity
                       s0 ≈ s1                                 s0 ≈ s′0 , . . . , sn ≈ s′n
               s[v := s0 ] ≈ s[v := s1 ] Leibniz          f (s0 , . . . , sn ) ≈ f (s′0 , . . . , s′n ) Congruence
 Here, s, s0 , . . . , sn ∈ Term/NLG(F, V ), f ∈ F, v ∈ V , where n ≥ 0. The notation s[v := s0 ] denotes substituting s0
 for all occurrences of v in s.

 2.3     Formal Correctness

 2.3.1    Formalization
 As presented in Section 2.1 and Section 2.2, we can use formal models to abstract programs, while using formal logic
 to formalize their properties. By default, this paper uses a model to denote an abstract representation of a program in a
 formal model and uses a property to denote a model property described in a formal logic interpretable in the context of
 the model. Formally, correctness is defined in Definition 2.17.
 Definition 2.17 (Correctness). Correctness is a satisfaction relation |= between a model M and a property ϕ.
 M is correct with respect to ϕ if and only if M |= ϕ holds true.
 Q1 illustrated in Section 1 is to formulate a satisfaction relation defined in Definition 2.17 with a formal model and a
 formal logic.

 2.3.2    Correctness Operation
 From Definition 2.17, two operations associated with correctness are derived.
 Definition 2.18 (Correctness Verification). A correctness verification, denoted as V Corr, is a partial function that
 accepts a model M and a set of properties Φ. It returns ⊤ if ∀ϕ ∈ Φ : M ⊢ ϕ, and returns ⊥ if ∃ϕ ∈ Φ : M, ϕ ⊢ ⊥
 upon termination.
 Proposition 2.1 (Correctness Verification). If there exists a correctness verification V Corr, such that V Corr(M, Φ) =
 ⊤, then M ⊢ Φ.

 Proof. From Definition 2.18, V Corr(M, Φ) = ⊤ implies ∀ϕ ∈ Φ : M ⊢ ϕ. Therefore, M ⊢ Φ.                                     ■
  Definition 2.19 (Soundness of Correctness Verification). A correctness verification is sound if M ⊢ Φ =⇒ M |= Φ.
  Definition 2.20 (Completeness of Correctness Verification). A correctness verification is complete if M |= Φ =⇒
  M ⊢ Φ.
  Definition 2.21 (Correctness Implementation). A correctness implementation, denoted as I Corr, is a partial function
  that accepts a set of properties Φ and returns a model M upon termination if there exists a correctness verification
V
  Corr, such that V Corr(M, Φ) = ⊤.
 Correspondingly, Q2 illustrated in Section 1 is to formulate a correctness verification defined in Definition 2.18 and Q3
 is to formulate a correctness implementation defined in Definition 2.21.


                                                            12
                                          Transition-Oriented Programming                                  A P REPRINT



2.3.3   Provable Correctness
Correctness verification and implementation may not exist in some cases. For instance, given that a property ϕ specifies
a model to decide whether a program with its input terminates, constructing M and proving M |= ϕ is impractical
due to the undecidability of the halting problem Cook [2023]. Consequently, in practice, the focus often shifts to the
concept of provable correctness, formally illustrated in Proposition 2.2.
Proposition 2.2 (Provable Correctness). A set Φ of properties specifying a model M is provable, if there exists a sound
and complete correctness verification V Corr, such that V Corr(M, Φ) ∈ {⊤, ⊥}.

Proof. By Definition 2.18, 2.19, and 2.20, the computation of V Corr(M, Φ) is the proof structure for Φ, if V Corr(M, Φ)
terminates.                                                                                                           ■

Different from Proposition 2.2 that requires both soundness and completeness for correctness verification, provably
correct models only require soundness, as in Proposition 2.3.
Proposition 2.3 (Provably Correct Model). M is a provably correct model with respect to a set Φ of properties, if
there exists a sound correctness verification V Corr, such that V Corr(M, Φ) = ⊤.

Proof. As per Proposition 2.1, V Corr(M, Φ) = ⊤ implies M ⊢ Φ. By Definition 2.19, if V Corr is sound, then
M ⊢ Φ =⇒ M |= Φ. Therefore, Φ holds for M, i.e., M is provably correct.                                  ■




                                                          13
                                            Transition-Oriented Programming                                   A P REPRINT



3     Transition-Oriented Programming
Transition-Oriented Programming (TOP) is a programming paradigm focusing on articulating stateful dynamics
and structural transformations of systems through formal models and logics. It leverages an expressive formal model
(graph transition system) and formal logics to resolve the ambiguities present in requirement specifications. Besides,
TOP integrates intrinsic correctness verification and bridges the gap between verified models and executables with side
effects, thus intertwining correctness specification, verification, and implementation.
TOP combines two distinct approaches, bottom-up (modularization) and top-down (progressive specification), to
facilitate correctness specification and verification through iterative and incremental processes. Besides, TOP enhances
precise specification and efficient verification via context perception, including type refinement and transformation
prioritization. Furthermore, TOP promotes automated proof techniques to streamline correctness verification, such as
bounded model checking and iterative deepening theorem proving.
This section delves into the theoretical foundations of TOP and its practical implementation, particularly through the
Seni language.

3.1     Graph Transition System

3.1.1    Model
Definition 3.1 (Typed Node-Labeled Graph). A Typed Node-Labeled Graph (TNLG) over set F of typed function
symbols and set V of typed variables, where F ∩ V = ∅, is a quadruple ⟨N, 0 n, L, S⟩ paralleling that of a NLG in
Definition 2.7 with restrictions applied to S as follows.

         • ∀n ∈ N, L(n) ∈ F 0 : |S(n)| = 0, where F 0 ⊆ F is the set of nullary (0-ary) function symbols representing
           constants of primitive types, including Boolean, Integer, Float, and Character. The node value Value(n) of n
           is a value of a primitive type.
         • ∀n ∈ N, L(n) ∈ F i , i > 0 : |S(n)| = i, where F i ⊆ F is the set of i-ary function symbols containing i typed
           parameters, such that S(n)[j], 0 < j ≤ i represents the j-th typed parameter that is a typed function symbol
           or variable.

A Closed TNLG (CTNLG) and a subgraph of a TNLG are defined the same in Definition 2.7.
Example 3.1 (Typed Node-Labeled Graph). An example of a TNLG is depicted in Figure 7, where each node is
associated with a typed function symbol, characterizing it as a CTNLG. The binary operator :: binds the function
symbol on the left side with the type on the right side. For any function symbol f ∈ F \ F 0 , its type is represented by a
sequence delineating the types of its parameters, enclosed within parentheses. For instance, node nˆ0 corresponds to a
binary function symbol M , of which the parameters are two unary function symbols, each taking an integer nullary
function symbol as the parameter.




                                      Figure 7: Typed node-labeled graph example.

Definition 3.2 (Pattern Graph). A Pattern Graph (PG) over set F of typed function symbols and set V of typed
variables, where F ∩ V = ∅, is a variant of TNLG as per Definition 3.1, defined as a quintuple
                                                     ⟨N, 0 n, L, S, E⟩

         • N, 0 n, L, S parallel that of a TNLG in Definition 3.1, and


                                                            14
                                              Transition-Oriented Programming                                   A P REPRINT



       • E : V 7→ Condition(V ) × Expression(V ) is a partial effect function that relates a condition and an expression
         to any variable v that satisfies ∃n, n′ ∈ N, 0 < i ≤ |S(n′ )| : L(n) = v ∧ n = S(n′ )[i] with the i-th parameter
         of L(n′ ) a primitive type.

For E(v) = (c, e), c is a propositional formula that applies value-level constraints to pattern matching, and e is an
expression that applies value change to v after pattern matching, constructed using constants, variables and operators. c
is a tautology if c = ⊤. e is an idempotent expression if e = v.
Example 3.2 (Pattern Graph). Figure 8 illustrates an example of a PG that removes variables with duplicated values
for garbage collection. The representation follows the conventions in Example 3.1 with additional details related to
variable nodes with primitive types by E. For a variable node associated with v and E(v) = (c, e), the former square
bracket represents c, and the latter square bracket represents e. For instance, E(x) = (⊤, x + 1) for integer variable x
related to n1 .




                                              Figure 8: Pattern graph example.

Definition 3.3 (Pattern Graph Homomorphism). A pattern graph homomorphism g0 ⇝ g1 from a PG g0 =
⟨N0 , 0 n0 , L0 , S0 , E0 ⟩ to a TNLG g1 = ⟨N1 , 0 n1 , L1 , S1 ⟩ over F and V , where F ∩ V = ∅, is a function H : N0 7→ N1 ,
such that H( 0 n0 ) = 0 n1 , and

       • for all n ∈ N0 , L0 (n) ∈ F ,
            – L1 (H(n)) = L0 (n), and
            – For each i-th element ni ≜ S0 (n)[i] in S0 (n), S1 (H(n))[i] = H(ni ), where 0 < i ≤ |S0 (n)|;
       • for all v ∈ V, E0 (v) = (c, e), if there exists n ∈ N0 , L0 (n) = v,
            – Value1 |= c, i.e., substituting all variables in c with their values from Value1 makes c hold true.
Definition 3.4 (Pattern Graph Rewriting). PGRewrite : G × G̃ × Ñ 7→ G is a rewriting function, where G ⊆
TNLG(F, ∅), G̃ ⊆ PG(F, V ), ∀g̃ ∈ G̃, g̃ = ⟨Ñ , L̃, 0˜n, S̃, Ẽ⟩ : (g̃, ñ) ∈ G̃ × Ñ =⇒ ñ ∈ Ñ ∧ ñ ̸= 0˜n, and
∀g ∈ G : ∃(g̃, ñ) ∈ G̃ × Ñ : g̃/ 0˜n ⇝ g.
Function PGRewrite follows the three steps defined in Definition 2.11 with an additional step:

      4. Construct g4 ≜ ⟨N4 , 0 n4 , L4 , S4 ⟩ by applying effects defined for all n ∈ N3 , L3 (n) = v ∈ V, E0 (v) = (c, e),
         such that Value4 (n) = Evaluate(e, Value3 ), where Evaluate(e, Value3 ) evaluates e to a value by substituting
         variables in e with their values from Value3 .
Definition 3.5 (Graph Transition System). A Graph Transition System (GTS) over set F of typed function symbols
and set V of variables, where F ∩ V = ∅, is a quintuple
                                                     ⟨P, 0P, R, ,→, 0˜g⟩

       • P is a set of places,
       • 0P ⊆ P is a set of initial places,
       • R ⊆ G̃ × Ñ is a transformation relation, where G̃ ⊆ PG(F, V ) is a set of PGs over F and V as per
         Definition 3.2, and ∀g̃ ≜ ⟨Ñ , L̃, 0˜n, S̃, Ẽ⟩ ∈ G̃ : (p, g̃, ñ, p′ ) ∈ ,→ =⇒ ñ ∈ Ñ ∧ ñ ̸= 0˜n,


                                                             15
                                                   Transition-Oriented Programming                                     A P REPRINT



        • ,→ ⊆ P × R × P is a pattern matching transition relation, and

        • 0˜g ∈ PG(F, V ) is the initial pattern.
Definition 3.6 (Labeled Kripke Structure Semantics of a Graph Transition System). Let G ≜ ⟨P, 0P, R, ,→, 0˜g⟩ be a
GTS over F and V . The corresponding LKS, denoted as LKS(G), is the tuple ⟨S, 0S, L, →, L⟩ over set P ∪ PG(F, V )
of atomic propositions,

        • S = P × TNLG(F, ∅),

        • 0S = {(p, g) | p ∈ 0P, 0˜g ⇝ g}, where ⇝ is defined in Definition 3.3,

        • L = R ⊆ G̃ × Ñ ,
        • → ⊆ S × L × S is defined by the following rule:
                                                                   g̃,ñ
                                                              (p ,−−→ p′ ) ∧ (g̃/ 0˜n ⇝ g)
                                                                 g̃,ñ
                                                        (p, g) −−→ (p′ , PGRewrite(g, g̃, ñ))
          where PGRewrite is defined in Definition 3.4, and

        • L is a labeling function such that L((p, g)) = {p} ∪ {g̃ ∈ G̃ | g̃/ 0˜n ⇝ g}.

A GTS is terminal if its LKS interpretation is terminal.

3.1.2   Property
Temporal Property
Definition 3.7 (Path). A path of a GTS interpreted over a LKS ⟨S, 0S, L, →, L⟩ according to Definition 3.6 is either

        • a finite state sequence [s0 , s1 , . . . , sn ] over S, such that s0 ∈ 0S, sn is a terminal state, and ∀0 < i ≤ n : si ∈
          S(si−1 ), or
        • an infinite state sequence [s0 , s1 , . . . ] over S, such that ∀i > 0 : si ∈ S(si−1 ).

Path(G) is the set of all paths.
Definition 3.8 (Trace). A trace of a GTS over a LKS LKS(G) ≜ ⟨S, 0S, L, →, L⟩ is defined as

        • [L(s0 ), L(s1 ), . . . , L(sn )] for a finite path [s0 , s1 , . . . , sn ], and
        • [L(s0 ), L(s1 ), . . . ] for an infinite path [s0 , s1 , . . . ].

Trace(G), the traces of G, is a set of traces defined for Path(G).
Definition 3.9 (Semantics of LTL over GTS). Given a GTS G ≜ ⟨P, 0P, R, ,→, 0˜g⟩ over F and V , and an LTL formula
ϕ formed in Definition 2.12 over P ∪ TNLG(F, V ), G |= ϕ if and only if Trace(G) ⊆ W (ϕ).
Here, W (ϕ) = {w ∈ Aω | w |= ϕ}, where A = ℘(P ∪ TNLG(F, V )), Aω is an ω-language for LKS(G). For each
word w ∈ Aω , w is an infinite sequence [A0 , A1 , . . . ]. The satisfaction relation |= ⊆ Aω × Language(LTL) is the
smallest relation defined as follows.
             w |= ⊤
             w |= a                           ⇐⇒ a ∈ A0
             w |= ϕ0 ∧ ϕ1                     ⇐⇒ w |= ϕ0 ∧ w |= ϕ1
             w |= ¬ϕ                          ⇐⇒ w ̸|= ϕ
             w |= ⃝ϕ                          ⇐⇒ w[A1 , . . . ] |= ϕ
             w |= ϕ0 ⨿ ϕ1                     ⇐⇒ (∃j ≥ 0 : w[Aj , . . . ] |= ϕ1 ) ∧ (∀0 ≤ i < j : w[Ai , . . . ] |= ϕ0 )
             w |= 3ϕ                          ⇐⇒ ∃i ≥ 0 : w[Ai , . . . ] |= ϕ
             w |= 2ϕ                          ⇐⇒ ∀i ≥ 0 : w[Ai , . . . ] |= ϕ


                                                                         16
                                             Transition-Oriented Programming                                           A P REPRINT



Definition 3.10 (Semantics of CTL over GTS). Given a GTS G over F and V , and a CTL formula ϕ formed in
Definition 2.13 over P ∪ TNLG(F, V ), G |= ϕ if and only if ∀s ∈ 0S : s |= ϕ for LKS(G) ≜ {S, 0S, L, →, L}. The
satisfaction relation |= ⊆ S × Language(CTL) is the smallest relation defined as follows.
                s |= ⊤
                s |= a                          ⇐⇒ a ∈ L(s)
                s |= ¬ϕ                         ⇐⇒ s ̸|= ϕ
                s |= ϕ0 ∧ ϕ1                    ⇐⇒ s |= ϕ0 ∧ s |= ϕ1
                s |= ∃φ                         ⇐⇒ ∃path ∈ Path(s) : path |= φ
                s |= ∀φ                         ⇐⇒ ∀path ∈ Path(s) : path |= φ
             path |= ⃝ϕ                         ⇐⇒ path[1] |= ϕ
             path |= ϕ0 ⨿ ϕ1                    ⇐⇒ ∃j ≥ 0 : path[j] |= ϕ1 ∧ (∀0 ≤ k < j : path[k] |= ϕ0 )
             path |= 3ϕ                         ⇐⇒ ∃j ≥ 0 : sj |= ϕ
             path |= 2ϕ                         ⇐⇒ ∀j ≥ 0 : sj |= ϕ

Functional Property
Definition 3.11 (Structure Path). A structure path of a GTS is a finite CTNLG sequence [g0 , g1 , . . . , gn ] over
TNLG(F, ∅), such that

      • [(p0 , g0 ), (p1 , g1 ), . . . , (pn , gn )] is a path variant of Path(G) without the constraint (p0 , g0 ) ∈ 0S , and
       • ∀0 < i ≤ n : (pi , gi ) ∈ S((pi−1 , gi−1 )).
Definition 3.12 (Instantiation of Typed Node-Labeled Graph). An instantiation of a TNLG g is a function
Instance(g, V) that takes g and a total variable evaluation function V well-defined for Variable(g) and produces
a CTNLG by assigning concrete values to all typed variables present in g according to V.
Definition 3.13 (Semantics of EL over GTS). Given a GTS G = ⟨P, 0P, R, ,→, 0˜g⟩ and an EL formula Lg ≈ Rg over
F and V , where Lg, Rg ∈ TNLG(F, V ). G |= Lg ≈ Rg if and only if

      • for any LV, there exists RV and a CTNLG g,                               such that [Instance( Lg, LV), . . . , g] and
        [Instance( Rg, RV), . . . , g] are structure paths of G, and
      • for any RV, there exists LV and a CTNLG g,                               such that [Instance( Rg, RV), . . . , g] and
        [Instance( Lg, LV), . . . , g] are structure paths of G,

where ∀v ∈ Variable( Lg) ∩ Variable( Rg) : LV(v) = RV(v).
Definition 3.14 (Symbolic Instantiation of Typed Node-Labeled Graph). A symbolic instantiation of a TNLG g is a
function Symbolic(g) that produces a CTNLG by substituting Variable(g) with nullary function symbols in g.
Definition 3.15 (Derivation Tree). A derivation tree of a TNLG g regarding a GTS ⟨P, 0P, R, ,→, 0˜g⟩ over F and V is
a tree ⟨N, 0 n, S⟩
      • N ⊆ TNLG(F, V ) is a set of nodes,
      • 0 n = Symbolic(g), 0 n ∈ N , and

      • S(n) = {PGRewrite(n, g̃, ñ) | (g̃, ñ) ∈ R, g̃/ 0˜n ⇝ n}.
Theorem 3.1 (EL Satisfiability). Lg ≈ Rg holds for G if DerivationTree( Lg) and DerivationTree( Rg) with respect to
G have at least one common node.

Proof. Let g be a common node present in both DerivationTree( Lg) and DerivationTree( Rg). According to Defini-
tion 3.15, there exist structure paths [Symbolic( Lg), . . . , Symbolic(g)] and [Symbolic( Rg), . . . , Symbolic(g)].
Correspondingly, for any LV that substitutes symbolic values in Symbolic( Lg), Symbolic(g), and shared symbolic
values of Lg and Rg, the structure paths remain unaffected. Therefore, for each such LV, there exists a corresponding
                                                                             L
Symbolic( Rg) to ensure that ∀v ∈ Variable( Lg) ∩ Variable( Rg) : RV(v) = V(v). Analogously, this relationship is
                      R                                           L
bidirectional, as each V implies the existence of a corresponding V.
By Definition 3.13, this completes the proof.                                                                                    ■


                                                                17
                                           Transition-Oriented Programming                                    A P REPRINT



3.1.3    Implementation
GTSs interact with external environments through side effects encapsulated by their transitions. A side effect refers to
any operation that alters the state of external environments, a typical example of which is performing Input/Output (I/O)
operations.
For a GTS containing a transformation relation R, each r ∈ R preserves its functional purity while encapsulating
two side effects: prior effect and later effect. A prior effect transpires before r, such as consuming a signal from the
external environment. Conversely, a later effect manifests after r, such as displaying a message on a console via a
command transmission to the external environment.
Theorem 3.2 (Provably Correct Implementation). A provably correct GTS with side effects is a provably correct
implementation with respect to a set of temporal and functional properties.

Proof. Let S denote a provably correct GTS S associated with a set Φ of temporal and functional properties. A sound
correctness verification that mechanizes S ⊢ Φ exists to ensure S |= Φ, as per Definition 3.5 and Proposition 2.3.
By Definition 2.21, the process of formulating the specification (S and Φ) is a correctness implementation. Additionally,
side effects alter the external environment but do not affect the functional purity of the transformation relation of S.
Therefore, the implementation, S with side effects, preserves Φ and is provably correct.                              ■

3.2     The Seni Language

The Seni language is a transition-oriented programming language that facilitates the development of provably correct
systems by practicalizing the TOP features elaborated upon in subsequent Section 3.3, Section 3.4, Section 3.5, and
Section 3.6.
The etymology of "Seni" is derived from the romanization of the Japanese term "遷移," meaning "transition". This
nomenclature profoundly reflects the fundamental purpose of the Seni language. Specifically, Seni effectively mech-
anizes GTSs as illustrated in Section 3.1 to capture both stateful dynamics and structural transformations that are
formulated as temporal and functional properties to be verified by its intrinsic correctness verification.

3.2.1    Core Syntax
The core syntax of the Seni language focuses on constructing a PGTS as per Definition 3.17, of which the Extended
Backus–Naur Form (EBNF) is shown in Definition 3.16.
Definition 3.16 (Core Syntax of Seni).
                           Unit = {TypeDecl}, {SysDecl}
                     TypeDecl = type, TypeID, "=", ConsDecl, {"|", ConsDecl}
                       SysDecl = [default], system, SysID, SysParam, SysBody
                      SysBody = "{", {SymDecl}, {VarStmt}, {InstStmt}, InitStmt, {RuleDecl}, "}"
                       InstStmt = InstID | as | SysIDSysArg
                      SymDecl = Symbol, "::", Type | SymVarDecl
                       VarStmt = Variable, "::", Type
                   SymVarDecl = var, Symbol, "::", Type
                       InitStmt = InitParam, "=", GraphStmt | RelationStmt
                     RuleDecl = RuleID, "=", Rule
                     PropDecl = LTLDecl | CTLDecl | ELDecl


The Seni language extends the primitive type with string, list, stack, and queue as built-in types. Particularly, the graph
type is handy for representing an inferable complicated type.

3.2.2    Execution by Rewriting
The Seni language represents TNLGs and PGs in a natural way, as shown in Example 3.3.
Example 3.3 (Garbage Collection). A Seni program implementing the garbage collection in Example 3.2 is shown in
Listing 2.


                                                            18
                                                Transition-Oriented Programming                                     A P REPRINT



                                              Listing 2: Garbage collection by Seni.
 1   default system Main {
 2
 3       init() = GarbageCollector(1, 1)
 4
 5   }
 6
 7   system GarbageCollector {
 8
 9       M :: ((Int), (Int) | (Int, Int))
10       V_a :: (Int)
11       V_b :: (Int) | (Int, Int)
12       x, y, z :: Int
13
14       init(a :: Int, b :: Int) = M(
15            V_a(a),
16            V_b(b, 1)
17       )
18
19       r = ^M(
20                  V_a(x),
21                  V_b(
22                     y[y = x],
23                     z[z = y]
24                  )
25            )
26            −>
27            ~M(
28                  V_a(x),
29                  V_b(
30                     x[x + 1]
31                  )
32            )
33
34       before r {
35           print("Collecting")
36       }
37
38       after r {
39           print("Collected")
40       }
41   }


     The default system Main initializes a GarbageCollector by assigning its arguments at line 3. Lines 9 to 11 declare three
     typed function symbols M , Va , and Vb representing a memory model with two program variables. Subsequently, line
     12 declares a typed variable used to define PGs. The code block spanning lines 14 to 17 creates the CTNLG of the
     initial state. Following this, the block from lines 19 to 32 declares the rule r by constructing a PG and identifying M̂ as
     the root and M̃ a post-transformation root by tokens ^and ~. These tokens can be omitted if the first function symbols
     are roots. For the branch rooted at M̂ , propositional formulae in square brackets are conditions to guard the execution
     of the rule. For the branch rooted at M̃ , expressions in square brackets are effects to be applied after applying the rule.
     Additionally, lines 34 to 40 define two I/O functions associated with rule r.

     The execution of Seni programs relies on a virtual machine that implements PGRewrite as defined in Definition 3.4. A
     Seni virtual machine continuously rewrites the initial CTNLG defined in a Seni program according to the defined PGs
     until no pattern rewriting rule can be applied. Meanwhile, it calls I/O functions associated with the PGs each time a PG
     is applied.

     3.2.3   Temporal Property Verification

     The Seni language offers an intuitive way to formulate temporal properties in temporal logics, including LTL (Defini-
     tion 2.12) and CTL (Definition 2.13), as shown in Example 3.4.


                                                                 19
                                                        Transition-Oriented Programming                           A P REPRINT



     Example 3.4 (Mutual Exclusion). A Seni program implementing the semaphore-based mutual exclusion is shown in
     Listing 3.

                                                      Listing 3: Mutual Exclusion by Seni.
 1   system Process with (s :: Int) {
 2
 3       var id :: String
 4       var loc :: Int
 5
 6       init(_id :: String) = (
 7            id(_id),
 8            loc(0)
 9       )
10
11       toWait = [loc = 0] −> {loc: 1}
12       enterCrit = [loc = 1 & s > 0] −> {loc: 2, s: s − 1}
13       exitCrit = [loc = 2] −> {loc: 0, s: s + 1}
14
15       expose prop crit = [loc = 2]
16
17       ltl G F crit
18   }

     Line 3 uses the keyword var to declare a unary function symbol id with a unique anonymous integer variable as the
     parameter. Notably, the rules describing PGs are simplified since there is no structure transformation. For instance, line
     11 states that the rule toWait will be applied if there is a homomorphism from loc to the CTNLG of the current state
     with the variable condition loc = 0 and the effect changing the value of the node bound to loc to 1 will be applied after
     the transition. Additionally, line 17 declares an LTL property using the proposition declared in line 15. The exposed
     proposition is also accessible by other modules.

     The verification of temporal properties is carried out by default before the execution. A Seni virtual machine embeds
     bounded model checking techniques to automate verification processes. The details will be presented in Section 3.6.1.

     3.2.4   Functional Property Verification
     Functional properties are naturally encoded in equational logic (Definition 2.16) with the Seni language, as shown in
     Example 3.5.
     Example 3.5 (Binary Addition Function). A Seni program implementing the binary addition function in Example 2.6
     is shown in Listing 4.

                                                  Listing 4: Binary addition function by Seni.
 1   type Nat = Zero | Su(Nat)
 2
 3   default system Main {
 4       init() = BinaryAddition(Su(Zero), Su(Zero))
 5   }
 6
 7   system BinaryAddition {
 8
 9       Plus :: (Nat, Nat)
10       x, y :: Nat
11
12       init(left :: Nat, right :: Nat) = Plus(left, right)
13
14       r0 = Plus(x, Zero) −> x
15       r1 = Plus(x, Su(y)) −> Su(Plus(x, y))
16
17       el Plus(Su(x), Su(Zero)) = Su(Su(x))
18
19   }



                                                                      20
                                                   Transition-Oriented Programming                                     A P REPRINT



    The keyword type in line 1 creates a user-defined recursive type Nat presenting natural numbers. The initial statement
    in line 12 creates a CTNLG in a succinct representation. Since there are only structural transformations, the rules can
    be simplified, as shown in lines 14 and 15. Additionally, line 17 declares a functional property by keyword el.

    The same as temporal properties, a Seni virtual machine verifies functional properties before the execution by automated
    theorem proving techniques that will be discussed in Section 3.6.2.

    3.3     Modularization

    Modularization is a bottom-up approach to compose a large model by a set of modules.

    3.3.1    Module
    A module is a self-contained model for scalability and reusability. It is architecturally engineered to be seamlessly
    integrated into larger, more complex models, where it interacts with other modules to implement global functionalities.
    In this manner, correctness verification and implementation of complex models are scalable by decomposing global
    correctness into manageable segments, represented by the local correctness of individual modules. This decomposition
    not only simplifies the verification and implementation process but also enhances the manageability and maintainability
    of complex models.
     Besides, a module can function as an abstract model encapsulating generalized functionalities. This abstraction enables
     the instantiation of a module into multiple concrete models, each tailored to specific requirements through the provision
     of relevant arguments. Therefore, formulating modules mitigates the need for redundant efforts in developing similar
     models from scratch, thereby enhancing reusability. As shown in Example 3.4, two Process systems encapsulating
     primary functionalities are instantiated by a higher-level system Main with different arguments. Formally, an abstract
     model is a parameterized graph transition system defined in Definition 3.17.
     Definition 3.17 (Parameterized Graph Transition System). A Parameterized Graph Transition System (PGTS)
     is a GTS Ḡ over F and V with typed parameters binding with V̄ ⊆ V , such that for all ( 0 p, 0g) ∈ 0S of LKS(Ḡ),
    0
      g ∈ TNLG(F, V̄ ).
    A PGTS is initialized if 0g is instantiated.

    Notably, the correctness of an abstract model can be verifiable through a set of correctness verification processes. These
    processes are used to rigorously verify the model against all conceivable parameter values, ensuring its correctness for
    all potential concrete models.
    However, the correctness verification is usually computationally intensive and may not terminate within a reasonable
    timeframe, especially when the parameter space is vast and multidimensional. A common strategy involves constraining
    the ranges of parameters. By limiting the scope of parameter values to a smaller manageable subset, the correctness
    verification has the potential to be efficient. This strategy reduces the computational burden by focusing on a narrowed
    yet representative concrete models to be generated.

    3.3.2    Concurrency
    Multiple modules can compose a concurrent model by asynchronous or synchronous composition.
    Definition 3.18 (Asynchronous Concurrency of Graph Transition Systems). Given two GTSs G0 ≜
    ⟨P0 , 0P0 , R0 , ,→0 , 0˜g 0 ⟩ over F0 and V0 , and G1 ≜ ⟨P1 , 0P1 , R1 , ,→1 , 0˜g 1 ⟩ over F1 and V1 , the asynchronous concur-
    rency of G0 and G1 , denoted as G0 9 G1 , is defined over F0 ∪ F1 and V0 ∪ V1 :
                                   G0 9 G1 ≜ ⟨P0 × P1 , 0P0 × 0P1 , R0 ⊎ R1 , ,→, 0˜g 0 ⊕ 0˜g 1 ⟩
    where ,→ is defined by the rules:
                                              r                                           r
                                             →0 p′0
                                         p0 ,−                                           →1 p′1
                                                                                     p1 ,−
                                               r                                           r
                                               → ⟨p′0 , p1 ⟩
                                   ⟨p0 , p1 ⟩ ,−                                           → ⟨p0 , p′1 ⟩
                                                                               ⟨p0 , p1 ⟩ ,−
    Example 3.6 (Asynchronous Concurrency). The Process module coded in Listing 3 of Example 3.4 can be composed
    as an asynchronous module, as shown in Listing 5.
                                          Listing 5: Asynchronous Concurrency by Seni.
1   default system Main {


                                                                  21
                                                         Transition-Oriented Programming                                   A P REPRINT



 2
 3         var s :: Int
 4
 5         p1 as Process("p1") with (s)
 6         p2 as Process("p2") with (s)
 7
 8         init() = async [p1, p2] {s: 1}
 9
10         ltl G (not p1.crit or not p2.crit)
11
12   }

     Line 5 instantiates a Process with a string and passes a shared TNLG into the instance. Line 8 initializes an asynchronous
     model composed of two Process instances sharing a TNLG s(1). Line 10 declares an LTL property using the exposed
     proposition crit of the Process module.
     Definition 3.19 (Synchronous Concurrency of Graph Transition Systems). Given two GTSs G0 ≜
     ⟨P0 , 0P0 , R0 , ,→0 , 0˜g 0 ⟩ over F0 and V0 , and G1 ≜ ⟨P1 , 0P1 , R1 , ,→1 , 0˜g 1 ⟩ over F1 and V1 , the synchronous con-
     currency of G0 and G1 , denoted as G0 ∥ G1 , is defined over F0 ∪ F1 and V0 ∪ V1 :
                                         G0 ∥ G1 ≜ ⟨P0 × P1 , 0P0 × 0P1 , R0 ∪ R1 , ,→, 0˜g ⊕ 0˜g ⟩     0       1
     where ,→ is defined by the rules:
              • For r ∈
                      / R0 ∩ R1 :
                                                           r                                                r
                                                          →0 p′0
                                                      p0 ,−                                              →1 p′1
                                                                                                     p1 ,−
                                                            r                                               r
                                                            → ⟨p′0 , p1 ⟩
                                                ⟨p0 , p1 ⟩ ,−                                              → ⟨p0 , p′1 ⟩
                                                                                               ⟨p0 , p1 ⟩ ,−
              • For r ∈ R0 ∩ R1 :
                                                                            r              r
                                                                          →0 p′0 ∧ p1 ,−
                                                                      p0 ,−            →1 p′1
                                                                                     r
                                                                                   → ⟨p′0 , p′1 ⟩
                                                                       ⟨p0 , p1 ⟩ ,−

     3.4     Progressive Specification

     Progressive specification is a top-down approach to refine a model through a set of iterations.

     3.4.1     Iteration
     An iteration takes a model associated with a set of properties as the input and produces a refined model with more
     details. An input model is typically an approximation that encapsulates a smaller set of functionalities than its output
     model.
     During an iteration, the initial step executes a correctness verification against the input model with respect to its
     predefined properties. This verification assesses whether the model satisfies the established provable correctness. If
     the verification returns ⊥, indicating the input model violates one of the predefined properties, the model is subjected
     to a rectification phase. This phase is dedicated to resolving any deficiencies until the model satisfies the established
     provable correctness.
     Subsequent to the correctness verification, the iteration progresses to a refinement stage. In this stage, the primary
     objective is to further align the model with the demands by making small increments for the model. This is achieved
     through a dual approach: firstly, by concretizing and establishing additional properties that better resonate with the
     intended functionalities; and secondly, by extending the structure and transitions of the model to fulfill the functionalities.
     The iteration concludes with another round of correctness verification applied to the refined model with respect to all
     specified properties.

     3.4.2     Correctness Preservation
     Each iteration benefits from the bisimulation and simulation techniques Alur et al. [1998], Păsăreanu et al. [2005],
     Baier and Katoen [2008], Ding and Sato [2022a]. These techniques enable the preservation of the established provable
     correctness without necessitating the correctness verification of old properties. This not only improves the verification
     efficiency but also ensures that the refined model maintains consistency with the input model while evolving to meet new
     requirements. Formally, bisimulation and simulation are defined in Definition 3.20 and Definition 3.21, respectively.


                                                                                22
                                                    Transition-Oriented Programming                               A P REPRINT



     Definition 3.20 (Bisimulation). Given two GTSs G0 and G1 over F and V , G0 and G1 are bisimulation-equivalent,
                                                      s
     denoted G0 ∼ G1 , if there exists a bisimulation ∼ ⊆ S0 × S1 regarding LKS(G0 ) ≜ ⟨S0 , 0S0 , L0 , →0 , L0 ⟩ and
                      0
     LKS(G1 ) ≜ ⟨S1 , S1 , L1 , →1 , L1 ⟩ such that
                                                        s                                       s
            • ∀s0 ∈ 0S0 : ∃s1 ∈ 0S1 : (s0 , s1 ) ∈ ∼ and ∀s1 ∈ 0S1 : ∃s0 ∈ 0S0 : (s0 , s1 ) ∈ ∼, and
                                   s
            • for all (s0 , s1 ) ∈ ∼,
                 – L0 (s0 ) = L1 (s1 ),
                                                                                                     s
                 – if (s0 , s′0 ) ∈ →0 , then there exists (s1 , s′1 ) ∈ →1 such that (s′0 , s′1 ) ∈ ∼, and
                                                                                                     s
                 – if (s1 , s′1 ) ∈ →1 , then there exists (s0 , s′0 ) ∈ →0 such that (s′0 , s′1 ) ∈ ∼.
     Example 3.7 (Bisimulation). The toWait rule of the Process system in Example 3.4 can be augmented by an additional
     rule toWaitLog associating with an I/O operation writing the waiting information to a file, as coded in Listing 6 and
     visualized in Figure 9.
                                        Listing 6: Bisimulating the Mutual Exclusion Program.
 1   system Process with (s :: Int) {
 2
 3       var id :: String
 4       var loc :: Int
 5
 6       init(_id :: String) = (
 7            id(_id),
 8            loc(0)
 9       )
10
11       toWait = [loc = 0] −> {loc: 1}
12       toWaitLog = [loc = 0] −> {loc: 1}
13       enterCrit = [loc = 1 & s > 0] −> {loc: 2, s: s − 1}
14       exitCrit = [loc = 2] −> {loc: 0, s: s + 1}
15
16       after toWaitLog {
17           write("system.log").append(id + "␣is␣waiting")
18       }
19
20       expose prop crit = [loc = 2]
21   }




     Figure 9: Kripke structure of bisimular GTSs. The blue transitions and states {s0 , s1 , s2 } are interpreted from the GTS
     in Example 3.4, while the orange transitions and state s3 are interpreted from its bisimular GTS in Example 3.7.

     While the introduction of the toWaitLog rule introduces an additional state into the underlying LKS, the resultant GTS is
     bisimulation-equivalent to the original one. This equivalence indicates that, despite the new state, the stateful dynamics
     of the system are fundamentally unaltered.
     Definition 3.21 (Simulation). Given two GTSs G0 and G1 over F and V , G0 simulates G1 , denoted G0 ⪰ G1 , if there
     exists a simulation ⪰s ⊆ S0 ×S1 regarding LKS(G0 ) ≜ ⟨S0 , 0S0 , L0 , →0 , L0 ⟩ and LKS(G1 ) ≜ ⟨S1 , 0S1 , L1 , →1 , L1 ⟩
     such that

            • ∀s1 ∈ 0S1 : ∃s0 ∈ 0S0 : (s0 , s1 ) ∈ ⪰s , and


                                                                  23
                                                   Transition-Oriented Programming                               A P REPRINT




                                          Listing 7: Simulating the Mutual Exclusion Program.
 1   system Process with (s :: Int) {
 2
 3       var id :: String
 4       var loc :: Int
 5
 6       init(_id :: String) = (
 7            id(_id),
 8            loc(0)
 9       )
10
11       toWait = [loc = 0] −> {loc: 1}
12       enterCrit = [loc = 1 & s > 0] −> CRIT{loc: 2, s: s − 1}
13       enterContinuousCrit = [loc = 1 & s > 0] −> CONT_CRIT{loc: 2, s: s − 1}
14       continueCrit = CONT_CRIT[loc = 2] −> {loc: 1}
15       exitCrit = CRIT[loc = 2] −> {loc: 0, s: s + 1}
16
17       after toWaitLog {
18           write("system.log").append(id + "␣is␣waiting")
19       }
20
21       expose prop crit = [loc = 2]
22   }



            • for all (s0 , s1 ) ∈ ⪰s ,
                 – L0 (s0 ) = L1 (s1 ), and
                 – if (s1 , s′1 ) ∈ →1 , then there exists (s0 , s′0 ) ∈ →0 such that (s′0 , s′1 ) ∈ ⪰s .

     G0 and G1 are simulation-equivalent, denoted as G0 ≃ G1 , if G0 ⪰ G1 and G1 ⪰ G0 .
     Example 3.8 (Simulation). An unfair Process system in Example 3.4 contains an additional rule continueCrit = [loc =
     2] -> loc: 1, which simulates a refined GTS coded in Listing 7.




     Figure 10: Kripke structure of simular GTSs. The blue transitions and states {s0 , s1 , s2 } are interpreted from the GTS
     of the unfair Process, while the orange transitions and state s3 are interpreted from its simular GTS in Example 3.8.

     Lines 12 and 13 explicitly specify the places CRIT and CONT_CRIT. This specification is instrumental in managing the
     stateful transitions with fine granularity.

     An iteration can prove to preserve the correctness of the last iteration by bisimulation and simulation.
     Theorem 3.3 (Correctness Preservation). For non-terminal G0 and G1 over F and V ,

          (a) if G0 ∼ G1 , then ∀ϕ ∈ Language(LTL) ∪ Language(CTL) : G0 |= ϕ ⇐⇒ G1 |= ϕ,
          (b) if G0 ≃ G1 , then ∀ϕ ∈ Language(LTL) ∪ Language(UCTL) ∪ Language(ECTL) : G0 |= ϕ ⇐⇒ G1 |= ϕ,
          (c) if G0 ⪰ G1 , then ∀ϕ ∈ Language(LTL) ∪ Language(UCTL) : G0 |= ϕ =⇒ G1 |= ϕ.


                                                                      24
                                                    Transition-Oriented Programming                                   A P REPRINT



     Proof Outline. The proof of (a) follows that bisimulation in Definition 3.20 is finer than CTL*, a formal logic that
     subsumes LTL and CTL, by structural induction over LTL and CTL formulae. The proofs of (b) and (c) follow similar
     induction over the structure of logic formulae.                                                                   ■

     3.5     Context Perception

     Context perception enables GTSs to behave according to contexts, which improves the efficiency of verification. A
     context contains constraint information about typed function symbols and pattern transition relations.
     Definition 3.22 (Context of Graph Transition Systems). A context of a GTS ⟨P, 0P, R, ,→, 0˜g⟩ over F and V is a pair
                                                             ⟨Refine, Prior⟩

              • Refine : F ∪ V 7→ Language(F OL) is a type refinement function that relates FOL formulae to typed function
                symbols and variables, and
              • Prior : R × R 7→ N is a transformation prioritization function such that Prior(r, r′ ) is the priority differential
                between r and r′ , i.e., r is accorded a priority that is higher by Prior(r, r′ ) units than that of r′ .

     3.5.1     Type Refinement
     Each typed function symbol and variable can have its type refined by associating it with a predicate in a context. A
     predicate is a FOL formula assumed to hold for any element of the refined type. These refinement types provide precise
     type information to reason about systems and reduce the state space of property verification.
     Example 3.9 (Type Refinement). In the mutual exclusion program described in Example 3.4, the function symbol loc is
     defined to accept an anonymous integer variable as its parameter. Notably, within the Process system, the values bound
     to loc are limited to 0, 1, 2. This observation indicates that the generic integer type originally associated with loc and its
     parameter is overly broad. To refine this, predicate {v ∈ Int | 0 ≤ v < 3} can be used to effectively narrow the range of
     permissible values. This refinement enhances the precision of the type system in the Process system. Consequently, the
     Main system is updated to reflect this type refinement, as detailed in the revised program with a context in Listing 8.
                                 Listing 8: Mutual Exclusion Program with a Type Refinement Context.
 1   context TypeRefinement for Process {
 2       refine var loc :: {v :: Int | v >= 0 and v < 3}
 3   }
 4
 5   default system Main {
 6
 7         var s :: Int
 8
 9         p1 as Process("p1") with (s) under TypeRefinement
10         p2 as Process("p2") with (s) under TypeRefinement
11
12         init() = async [p1, p2] {s: 1}
13
14         ltl G (not p1.crit or not p2.crit)
15
16   }

     Notably, the context in Listing 8 refines both the type of loc and its bound variable. The refinement can also operate
     on a function-symbol or variable level. For example, the statement refine loc :: (v :: Int | v >=0 and v < 3) identifies
     Refine(loc) = ({v ∈ Int | 0 ≤ v < 3}) within a context.

     As illustrated in Example 3.9, the integer type associated with loc and its parameter is refined in the context to explicitly
     state the expected behavior and reduce the state space of the verification of the formulated temporal properties.

     3.5.2     Transformation Prioritization
     In GTSs, when multiple patterns are concurrently matched, the selection of PGs for transformation is nondeterministic.
     Consequently, the Seni language assigns identical priority levels to all PGs by default. Nonetheless, PGs can be priori-
     tized in contexts by assigning integers to each concurrently matched rule or by formulating inequations. Example 3.10
     illustrates the method of formulating an inequation to prioritize a rule.


                                                                   25
                                                       Transition-Oriented Programming                              A P REPRINT



     Example 3.10 (Transformation Prioritization). For the bisimulation-equivalent GTS in Example 3.20, the priority of
     rules toWait and toWaitLog is assigned in a context programmed in Listing 9.

                                                Listing 9: Transformation Prioritization Context.
 1   context TransformationPrioritization for Process {
 2       prior toWait > toWaitLog
 3   }
 4
 5   default system Main {
 6
 7         var s :: Int
 8
 9         p1 as Process("p1") with (s) under TypeRefinement
10         p2 as Process("p2") with (s) under TypeRefinement
11
12         init() = async [p1, p2] {s: 1}
13
14         ltl G (not p1.crit or not p2.crit)
15
16   }

     The inequation statement in line 2 serves as a concise notation to establish that the priority of toWait supersedes that of
     toWaitLog, irrespective of the actual magnitude of their priority differential. This formulation ensures that toWait is
     consistently applied prior to toWaitLog within the specified context.

     Notably, the inequation method is particularly pertinent in scenarios where the objective is to completely eradicate
     nondeterminism, which effectively dictates a deterministic order of rule application.
     The method of integer assignment operates on a probabilistic basis, where the likelihood of a rule application is
     determined by the ratio of its assigned integer value to the aggregate sum of all assigned integers to the concurrent rules.
     This method enables a nuanced control over the rule application to preserve certain nondeterminism.
     Transformation prioritization can improve the efficiency of verification processes by directing them toward an expedient
     convergence. Besides, it facilitates fine-grained control over the execution.

     3.6     Proof Automation

     TOP promotes proof automation techniques to facilitate property verification by default. For temporal property
     verification, bounded model checking techniques are introduced. For functional property verification, automated
     theorem proving techniques are introduced.

     3.6.1     Bounded Model Checking
     Bounded Model Checking (BMC) is a model checking technique that leverages Satisfiability Modulo Theories (SMT)
     solvers to efficiently check temporal properties as illustrated in Section 3.1.2.
     BMC transforms the temporal property verification problem into a satisfiability problem, as outlined in Figure 11.
     System structures and behaviors are encoded for a fixed number of steps, and a formula encoding a temporal property is
     satisfiable if and only if a counterexample to the property being verified exists within those steps. The SMT solver is
     then used to check the satisfiability of this formula and report a counterexample if a violation is found.




                              Figure 11: Overview of the bounded model checking for temporal properties.


                                                                       26
                                          Transition-Oriented Programming                                   A P REPRINT



Compared to traditional model checking techniques that attempt to explore the entire state space and can suffer from the
state explosion problem Valmari [1996], BMC focuses on a fixed number of steps for a quicker exploration in systems
where violations manifest in the early stages of execution. However, BMC does not guarantee the absence of violations
beyond the specified bound, which necessitates careful consideration of the bound’s adequacy in practical applications.
In TOP, GTSs and temporal properties formulated in LTL and CTL are encoded into SMT programs by Algorithm 1.

Algorithm 1 Bounded Model Checking of GTSs with Temporal Properties.
Input: G, ϕ ∈ Language(LT L) ∪ Language(CT L), θ ∈ N+
Output: ⊤ or path ∈ Path(G)
 1: K ← LKS(G)                                                                                      ▷ By Definition 3.6
 2: for each k ∈ {0, . . . , θ} do
          k
 3:     fM   ← UnfoldToSMT(K, k)                                                                ▷ Unfold K for k steps
          k
 4:     fϕ ← TranslateToSMT(¬ϕ, k)                                          ▷ Translate ¬ϕ with respect to the bound k
                                   k
 5:     (sat, path) ← SMTSolver(fM   ∧ fϕk )
 6:     if sat = ⊤ then
 7:         return path
 8:     end if
 9: end for
10: return ⊤

Notably, the termination of Algorithm 1 with ⊤ implies that G |= ϕ holds within bound θ. If θ attains or exceeds the
completeness threshold Biere et al. [2009] of G regarding ϕ, then G |= ϕ can be conclusively stated.

3.6.2   Iterative Deepening Theorem Proving
Iterative Deepening Theorem Proving (IDTP) is an automated theorem proving technique that capitalizes on the
Iterative Deepening Depth-First Search (IDDFS) algorithm to efficiently verify functional properties as illustrated in
Section 3.1.2.
In accordance with the semantics of EL in Definition 3.13, IDTP concurrently applies transformation rules to TNLGs
on both sides of an EL formula to identify a shared TNLG, which establishes the logical equivalence, as outlined in
Figure 12. IDTP amalgamates the space-efficiency of Depth-First Search (DFS) with the completeness of Breadth-First
Search (BFS) to enable a gradual exploration of the search space.




              Figure 12: Overview of the iterative deepening theorem proving for functional properties.

The core of IDTP relies on an algorithm for the Depth-Limited Search (DLS) of symbolic instances, as introduced
in Algorithm 2. Based on the DLS algorithm, IDTP is illustrated in Algorithm 3. In essence, Algorithm 3 is an
implementation of Theorem 3.1.

3.6.3   External Proof Assistance
TOP is formulated to integrate a diverse array of proof techniques for verifying both temporal and functional properties.
Nonetheless, the evolution of a practical language necessitates ongoing developmental efforts to assimilate these


                                                           27
                                              Transition-Oriented Programming                                   A P REPRINT



    Algorithm 2 Depth-Limited Search of Symbolic Instances.
    Input: g ∈ TNLG(F, V ), depth d ∈ N, and set T ⊆ TNLG(F, V ) of target symbolic instances to search.
    Output: ∅ if a target instance is found, or set D of derived symbolic instances.
     1: if d = 0 ∧ g ∈ T then
     2:     return ∅
     3: end if
     4: if d > 0 then
     5:     D = Derive(g, R)                                                    ▷ Derive implements S in Definition 3.15.
     6:     for each g ′ ∈ D′ do
     7:         D′ ← DLS(g ′ , d − 1, T )
     8:         if D′ = ∅ then
     9:             return ∅
    10:         else
    11:             D ← D ∪ D′
    12:         end if
    13:     end for
    14: end if
    15: return D

    Algorithm 3 Iterative Deepening Theorem Proving of Functional Properties.
    Input: transformation relation R of a GTS, EL formula ( Lg, Rg) ∈ Language(EL), and depth bound θ ∈ N+ .
    Output: ⊤ if the EL formula holds. ⊥ otherwise.
     1: (Dl , Dr ) ← (Symbolic( Lg), Symbolic( Rg))
     2: for each d ∈ {0, . . . , θ} do
     3:     Dl′ ← DLS( Lg, d, Dr )                                               ▷ DLS is illustrated in Algorithm 2.
     4:     if Dl′ = ∅ then
     5:         return ⊤
     6:     else
     7:         Dl ← Dl ∪ Dl′
     8:     end if
     9:     Dr′ ← DLS( Rg, d, Dl )
    10:     if Dr′ = ∅ then
    11:         return ⊤
    12:     else
    13:         Dr ← Dr ∪ Dr′
    14:     end if
    15: end for
    16: return ⊥


    techniques effectively. To address this challenge, TOP is engineered to support compatibility with external proof
    assistants. The current version of Seni provides fully automated proof mechanisms as illustrated in Section 3.6.1 and
    Section 3.6.2. Consequently, external proof tools can be used when these built-in automated proofs are either ineffective
    or fail to conclude within a reasonable time.
    Consider, for example, a snippet of a Seni program in Listing 10. The coded functional property Rev(Rev l) = l asserts
    that applying the reversal function to any list twice will yield the original list. Due to the absence of mathematical
    induction capabilities in the current Seni, the automated verification process is unable to reach a conclusion promptly.
    In such cases, an external proof assistant, such as Lean Moura et al. [2015], Moura and Ullrich [2021], can be used
    with the lemma Rev(Append(l0, l1)) = Append(Rev(l1), Rev(l0)) to efficiently give the proof. Correspondingly, this
    externally verified property is marked by the admitted keyword.
                                                Listing 10: Admitted Property.
1   type IntList = Nil | Cons(Int, IntList)
2   system Main {
3
4       Append :: (IntList, IntList)
5       Rev :: (IntList)
6


                                                               28
                                                 Transition-Oriented Programming   A P REPRINT



 7       h :: Int
 8       l, l0, l1 :: IntList
 9
10       r0 = Append(Nil, l) −> l
11       r1 = Append(Cons(h, l0), l1) −> Cons(h, Append(l0, l1))
12       r2 = Rev(Nil) −> Nil
13       r3 = Rev(Cons(h, l)) −> Append(Rev(l), Cons(h, Nil))
14
15       admitted el Rev(Rev l) = l
16
17   }




                                                                   29
                                           Transition-Oriented Programming                                   A P REPRINT



4         Applicability
4.1        Transition-Oriented Development of Distributed Protocols

A distributed protocol constitutes a comprehensive set of rules agreed upon by nodes to synchronize their behaviors and
maintain state consistency. These protocols adeptly navigate various challenges endemic to distributed computing, such
as event ordering Lamport [2019a], data consistency Lamport [2019b], fault tolerance Castro and Liskov [1999], and
concurrent control Bernstein et al. [1987].
Distributed Ledger Technology (DLT) epitomizes the application of distributed protocols to build decentralized systems.
Initially conceived as the underlying protocol for Bitcoin, a decentralized payment system Nakamoto [2019], DLT
has gained widespread adoption. Its applicability extends across diverse domains, addressing critical security and
privacy concerns, such as the Internet of Things (IoT) Dai et al. [2019], data persistence Ding and Sato [2020b,a],
and security infrastructures Ding and Sato [2023a]. Among the various distributed protocols for DLT, consensus
mechanisms hold a place of central importance. They serve as the protocol enabling the nodes in a distributed system
to agree on a consistent data value, especially in the absence of central authorities. Examples of these mechanisms
include proof-based mechanisms (e.g., Proof of Work (PoW) Dwork and Naor [1992]) for permissionless DLT, Practical
Byzantine Fault Tolerance (PBFT) Castro and Liskov [1999], and Raft Ongaro and Ousterhout [2014] for permissioned
DLT.
The allure of DLT primarily stems from its distinctive features, such as immutability, robust fault tolerance, non-
repudiation, transparency, traceability, and auditability. In a world increasingly reliant on data as a crucial asset,
DLT offers enhanced protection against the vulnerabilities inherent in centralized systems by distributing control and
restoring ownership to the data proprietors. Nonetheless, the development of a reliable decentralized system that upholds
these characteristics is far from straightforward or cost-free. Even experienced architects and developers encounter
formidable challenges in this endeavor Fu et al. [2019]. A case in point is Geth, the predominant implementation of the
Ethereum Virtual Machine (EVM), which is not impervious to vulnerabilities that can induce consensus errors. Notably,
a recent vulnerability3 led to a chain split following the London hard fork, demonstrating that even minor flaws can
precipitate substantial security concerns Yang et al. [2021]. Meanwhile, these vulnerabilities are hard to identify, yet
threatening the core distributed protocols Yang et al. [2021], such as the consensus mechanism.
Current methods for verifying decentralized systems typically fall into two categories: implementation-level verification
and model-based verification. The former scrutinizes the execution details, addressing runtime errors (e.g., null pointer,
division by zero, buffer overflow), function exceptions (e.g., undefined behaviors, unexpected algorithm output), and
concurrency issues (e.g., deadlocks, race conditions). Although crucial to verify implementations and even worthwhile
analyzing bytecodes, these methods are limited in their ability to detect underlying design flaws. Nevertheless, the
implementation-level verification is a unilateral strategy and hard to unravel the design flaw. Conversely, the latter
involves verifying the extracted models from implementations to identify design faults. However, extracting abstract
models from complex implementation is nontrivial. Extracted models may be overly simplified and lack meaningful
properties, or too complicated for effective verification Valmari [1996]. Additionally, ensuring that the extracted model
aligns with the intended demands poses a significant conformance issue, where any deviation renders the verified
properties unreliable. Moreover, a standardized development process is still missing Destefanis et al. [2018], especially
regarding the development of provably correct decentralized systems.
To mitigate the aforementioned challenges effectively, Transition-Oriented Development (TOD), an iterative and
incremental development process, is introduced by leveraging TOP in the development of distributed protocols, with a
focus on decentralized systems. TOD represents a sophisticated evolution of Formalism-Driven Development (FDD), a
concept initially proposed in Ding and Sato [2022a] and further refined in Ding and Sato [2022b]. The essence of TOD
lies in its pragmatic application of TOP within the development lifecycle, guiding the process toward the generation of
precise specifications and provably correct implementations.

4.1.1       Overview
TOD is an iterative and incremental development process that promotes formal methods throughout its lifecycle. It is
devised to take advantage of TOP to eliminate design ambiguity, prove model properties, compile correctness implemen-
tation with mainstream programming languages, and ensure conformance among design, model, and implementation.
In fact, the philosophy of iterative and incremental development process has been widely practiced in agile development
Shore [2007]. Nevertheless, both iteration and increment are not formally defined in agile processes. Typically, iteration
means enhancing systems progressively, whereas increment refers to the piecewise delivery of the system. However, it
      3
          https://github.com/ethereum/go-ethereum/security/advisories/GHSA-9856-9gg9-qcmq


                                                           30
                                            Transition-Oriented Programming                                      A P REPRINT



is hard to give a well-defined explanation about what an iteration or increment produces and relations between two
iterations and relations between an iteration and an increment. In TOD, iteration and increment are defined based on
Graph Transition System (GTS) theory, including modeling, refinement, and verification. With these well-defined
theories, iterations and increments can be rigorously managed and used to produce verifiable deliveries.
In TOD, an iteration formulates a model, proves model properties, implements the model, verifies the model imple-
mentation, and integrates or delivers the milestone. An increment organizes subsystems together as a higher-level
system. Concretely, an iteration contains four stages: abstraction, verification, composition, and refinement, which
is shown in Figure 13. All stages are supported by the Seni language introduced in Section 3.2. Abstraction Stage
produces a GTS as a module. In Verification Stage, the created GTS is verified by either built-in correctness verification
mechanisms or external tools. Composition Stage integrates multiple verified modules into higher-level systems or
delivered. Refinement Stage accepts a module from the last iteration and produces a more detailed GTS while preserving
and extending properties and can also launch a new iteration.




                                Figure 13: Overview of transition-oriented development.


4.1.2   Abstraction Stage
In Abstraction Stage, the goal is to produce a GTS, a rigorous design, from the ground up. Compared to the system graph,
originally formulated in FDD, the GTS is more expressive, especially regarding its functional property specifiability.

System Graph Parameter Variables of system graphs can be represented as a structure where a unary function
symbol binds a variable in GTSs. As introduced in Example 3.4, the Seni language uses the keyword var to conveniently
declare such a structure. Besides, channels of system graphs can be established by shared variables and side effects of
GTSs, as introduced in Section 3.3.2 and Section 3.1.3.

State Declarator State declarators of system graphs enable a succinct representation of stateful dynamics because
only the most critical features of states identified by interesting state variables need to be explicitly specified, while the
evaluation of other state variables is inferred from the preceding state. For GTSs, the concept of places functions in a
similar way and is also equipped with the capability of state inference.
Lemma 4.1 (State Inference). Consider a labeled Kripke structure ⟨S, 0S, L, →, L⟩ interpreted from a GTS, as per
Definition 3.6. Let Value and Value′ be node value evaluation functions of s and s′ , where s, s′ ∈ S, (s, s′ ) ∈ →
interpreted according to a pattern graph containing an effect function E associated with variable nodes EN = {n ∈
N | L(n) ∈ Domain(E)}. The following formula holds.

                                                                Evaluate(E(L(n))e , Value) n ∈ EN
                                                            
                     ∀n ∈ Domain(Value) : Value′ (n) =
                                                                Value(n)                   n∈/ EN.

Proof. The proof follows Definition 3.4 and Definition 3.6.                                                                ■

In Example 3.4, the rule toWait of Process only identifies the change of the node value of the child of loc without
explicitly identifying the child of id. By Lemma 4.1, the interpreted LKS has the child of id remaining unchanged.


                                                             31
                                             Transition-Oriented Programming                                  A P REPRINT



4.1.3   Verification Stage
Verification Stage produces a verifiable model based on the input GTS associated with the specified admissible behaviors
as properties. The properties are formally verified by internal verification algorithms by default and can also be verified
by external verification tools.

Internal Verification Inherited from TOP, TOD intertwines correctness specification and verification. Consequently,
TOD provides internal verification mechanisms. For instance, the Seni language mechanizes a bounded model checking
and an iterative deepening theorem proving technique, as introduced in Section 3.6.
Compared to FDD that only promotes the usage of external verification tools, these internal verification mechanisms
enhance the applicability of TOD by reducing the dependence on extra tools for verification, thereby minimizing the
risk of conformance issues and the requirement of the domain knowledge of formal verification tools.

External Verification A practical TOD tool takes time to evolve into a sophisticated tool with versatile correctness
verification. To bridge the gap, TOD enables compatibility with external verification tools.
Similar to the idea proposed in FDD Ding and Sato [2022a,b], the modeling language of TOD generates verification-
oriented programs for temporal property verification, such as SMT De Moura and Bjørner [2008] programs, Promela
Holzmann [1997] programs, and NuSMV Cimatti et al. [2002] programs. As illustrated in Section 4.1.2, the Seni
language that is capable of describing GTSs is expressive enough to program system graphs. Therefore, it is trivial
to implement the generation algorithm by slightly modifying the operational semantics of the verification program
generation of FDD.
Besides, TOD supports the verification of functional properties via proof assistants, as introduced in Section 3.6.3.
These external proof tools, such as F* Swamy et al. [2016] and Lean4 Moura and Ullrich [2021], can be used when
internal verification mechanisms are either ineffective or fail to conclude within a reasonable time.

4.1.4   Composition Stage
Composition Stage serves the overall bottom-up approach that composes multiple GTSs into a higher-level GTS,
which is an incremental process. There are three types of compositions in this stage: concatenation, embedding, and
concurrency.

Concatenation The concatenation of GTSs is to merge their corresponding elements, which is detailed in Algorithm 4.
With the support of the concatenation composition, complicated business logic can be separated into smaller modules.

Algorithm 4 Concatenating G0 and G1 .
Input: Gi = ⟨Pi , 0Pi , Ri , ,→i , 0˜g i ⟩ over Fi and Vi , where i ∈ {0, 1}
Output: ⟨P, 0P, R, ,→, 0˜g⟩ or exceptions
 1: for each i, j ∈ {0, 1} do
 2:     if Fi ∪ Vj ̸= ∅ then
 3:         return exception Uncontactable
 4:     end if
 5: end for
 6: return ⟨P0 ∪ P1 , 0P0 ∪ 0P1 , R0 ∪ R1 , ,→0 ∪ ,→1 , 0˜g 0 ⊕ 0˜g 1 ⟩


Example 4.1 (Concatenation). Given three GTSs GreaterThan and LessThan in Listing 11 and Listing 12, respectively.
A concatenated GTS Inequality is in Listing 13. A higher-level GTS can instantiate a GreaterThan module by
Inequality.GreaterThan(Su(Zero), Su(Zero)).

Embedding Embedding a GTS into another GTS is commonly used to formulate nested structures, as detailed in
Algorithm 5.
Notably, the invocation relation between two GTSs is established by the embedding composition, as exemplified in
Example 4.2.
Example 4.2 (Embedding). The Process in Example 3.4 can embed the BinaryAddition in Example 3.5 together with
functional modules EqualTo, GreaterThan, and BinarySubtraction, as shown in Listing 14.


                                                               32
                                                       Transition-Oriented Programming                                A P REPRINT




                                                             Listing 11: Module for >.
 1   system GreaterThan {
 2
 3       GT :: (Nat, Nat)
 4       x, y :: Nat
 5
 6       init(left :: Nat, right :: Nat) = GT(left, right)
 7
 8       r0 = GT(Su(x), Zero) −> True
 9       r1 = GT(Zero, Su(x)) −> False
10       r2 = GT(Su(x), Su(y)) −> GT(x, y)
11
12   }




                                                             Listing 12: Module for <.
 1   system LessThan {
 2
 3       LT :: (Nat, Nat)
 4       x, y :: Nat
 5
 6       init(left :: Nat, right :: Nat) = LT(left, right)
 7
 8       r0 = LT(Su(x), Zero) −> False
 9       r1 = LT(Zero, Su(x)) −> True
10       r2 = LT(Su(x), Su(y)) −> LT(x, y)
11
12   }




                                               Listing 13: Concatenated module for inequality.
1    system Inequality {
2        GreaterThan, LessThan
3    }




                                                 Listing 14: Process with embedded modules.
 1   system Process with (s :: Nat) {
 2
 3       var id :: String
 4       var loc :: Nat
 5
 6       init(_id :: String) = (
 7            id(_id),
 8            loc(Zero)
 9       )
10
11       toWait = [EqualTo(loc, Zero)] −> {loc: Su(Zero)}
12       enterCrit = [EqualTo(loc, Su(Zero)) & GreaterThan(s, Zero)] −> {loc: Su(Su(Zero)), s: BinarySubtraction(s, Su(Zero))}
13       exitCrit = [EqualTo(loc, Su(Su(Zero)))] −> {loc: Zero, s: BinaryAddition(s, Su(Zero))}
14
15   }




                                                                        33
                                            Transition-Oriented Programming                                      A P REPRINT



Algorithm 5 Embedding G0 into a node of 1˜g of G1 .
Input: Gi = ⟨Pi , 0Pi , Ri , ,→i , 0˜g i ⟩ over Fi and Vi , where i ∈ {0, 1}, ( 1˜g, _) ∈ R1 , and θ
Output: ⟨P, 0P, R, ,→, 0˜g⟩ or exceptions
 1: for each i, j ∈ {0, 1} do
 2:     if Fi ∪ Vj ̸= ∅ then
 3:          return exception Unembeddable
 4:     end if
 5: end for
 6: K1 ← LKS(G1 )                                                                                           ▷ By Definition 3.6
 7: G ← Unfold(K1 , θ)                                              ▷ Unfold K1 for θ steps to get a set of terminal CTNLGs.
 8: if |G| = 0 then
 9:     return exception Nonterminal Embedding
10: else if |G| > 1 then
11:     return exception Nondeterministic Embedding
12: end if
13: R ← R1
14: ,→ ← ,→1
15: for each (g, n) ∈ R do
16:     if g = 1˜g then
17:          g ′ ← UpdateNode(g, G[0])                                              ▷ Update the pattern graph that embeds G0 .
18:          R ← (R \ {(g, n)}) ∪ {(g ′ , n)}
19:          for each (p, (g, n), p′ ) ∈ ,→ do
20:              ,→ ← (,→ \ {(p, (g, n), p′ )}) ∪ {(p, (g, n), p′ )}
21:          end for
22:     end if
23: end for
24: return ⟨P1 , 0P1 , R, ,→, 0˜g 1 ⟩



Concurrency Concurrency composition is introduced in Section 3.3.2, including asynchronous and synchronous
concurrency. The algorithms are trivial to implement according to Definition 3.18 and Definition 3.19.

4.1.5    Refinement Stage
Refinement Stage accepts a GTS from the last iteration and produces a more detailed GTS while preserving and
extending properties. This stage also produces executables and functions as a milestone for delivery.

Property-Preserving Refinement TOD utilizes both bisimulation and simulation techniques introduced in Section 3.4
to support the refining process. The original purposes of these techniques are generally to optimize the verification
process and improve verification efficiency by compacting a model while preserving its properties. However, Refinement
Stage inverses the original purpose to extend a small model into a big one while preserving its properties by Theorem 3.3.

Executable Generation TOD intertwines correctness specification, verification, and implementation by default.
Therefore, a GTS is executable with side effects according to Theorem 3.2, which is supported by the Seni language.
However, language consistency plays an important role in maintaining a large-scale system developed in other
programming languages, such as Java, C++, and Go. Correspondingly, generating programs from GTSs for other
programming languages can be necessary to eliminate the consistency.
It is straightforward to construct a GTS in functional programming languages, as its related definitions and theorems are
mechanizable as pure functions. Meanwhile, the impure side effects are isolated by the monad. However, mechanizing
a GTS in object-oriented programming languages can be challenging, regarding the correctness preservation and
performance. It is an open challenge for the TOD tool.

4.2     Transition-Oriented Security Analysis of Security Infrastructures

Security infrastructures, such as public key infrastructures Brands [2000], access control frameworks Ribot and
Peluso [2003], and identity management systems Recordon and Reed [2006], are integral to the security paradigm


                                                             34
                                            Transition-Oriented Programming                                    A P REPRINT



in information and communications technologies (ICTs) to ensure confidentiality, integrity, and availability of the
protected resources.
Nonetheless, implementing a trustworthy security infrastructure is challenging, especially within centralized archi-
tectural designs where a central authority governs a critical component or mechanism. In centralized architectures,
the entire infrastructure is vulnerable to security breaches if a critical component is compromised. This vulnerability
manifests as a Single Point of Failure (SPoF), where the malfunction or penetration of a critical component can lead to
the breakdown of the entire infrastructure. In response to these vulnerabilities, recent advancements in decentralized
security infrastructures have emerged, offering solutions to the limitations inherent in centralized systems. Notable
developments include decentralized access control Ding and Sato [2023a] and decentralized identity management Ding
and Sato [2022c]. These decentralized systems distribute the control and management of security mechanisms, thereby
mitigating the risks associated with SPoFs and enhancing the overall robustness of the infrastructure.
However, decentralized security architectures are not immune to threats, including unauthorized access, impersonation
attacks, Man-in-the-Middle (MitM) attacks, and Distributed Denial of Service (DDoS) attacks. Consequently, conduct-
ing a formal security analysis of these frameworks is essential for making architectural decisions. To bridge the gap in
formal security analysis of security infrastructures, Transition-Oriented Security Analysis (TOSA) is introduced to
analyze security properties against threat models, exemplified by SecureSSI Ding and Sato [2023b], a security analysis
framework for Self-Sovereign Identity (SSI) systems.
TOSA is a security analysis framework that unifies system and threat modeling through GTSs. The specified systems
and threats are composed into a concurrent system, as introduced in Section 3.3.2. Besides, TOSA promotes the
intrinsic correctness verification for specifications, thereby obviating the need for additional formal verification efforts.
Additionally, the temporal property verification via the bounded model checking technique introduced in Section 3.6.1
can report counterexamples for reproducing attack vectors. The workflow is visualized in Figure 14.




                              Figure 14: Overview of transition-oriented security analysis.

In contrast to TOD introduced in Section 4.1, TOSA aims to analyze systems rather than produce deliverable imple-
mentations. Besides, TOSA verifies security properties regarding formulated threat models, as opposed to the intrinsic
properties inherent to system designs. This focus implies that the properties addressed within TOSA invariably entail
the interaction of multiple, relatively independent GTSs.

4.3   Transition-Oriented Program Analysis

Decentralized applications (DApps) are implemented by smart contracts that are programs deployed and automatically
executed on blockchains like Ethereum Wood [2014] and Hyperledger Fabric Androulaki et al. [2018]. Decentralized
finance (DeFi), a domain-specific DApps, is an emerging paradigm in finance, decoupling financial instruments from
traditional centralized intermediaries. Over the past five years, DeFi has provided many types of financial services, such
as decentralized exchanges (DEXs) Xu et al. [2023], derivative trading Eskandari et al. [2017], and lending Bartoletti
et al. [2021]. Although the DeFi benefits are remarkable (e.g., high availability, transparency, tamper-proofing) Zheng
et al. [2018], developing secure DeFi services is still challenging Zou et al. [2019].
Table 1 presents an investigation of 80 (with damages ranging from 2,400 to 600 million dollars) real-world DeFi
incidents occurring between November 2017 and December 2022, significantly endangering market health. The
investigation further categorizes them into six types based on root causes and ordered by severity, computed by
the average loss in US dollars per incident. Notably, this investigation dismisses the incidents caused by outdated
vulnerabilities like insecure integer arithmetic Torres et al. [2018], Gao et al. [2019], Rodler et al. [2021] given that
recent smart contract compilers (e.g., Solidity v0.8+), libraries (e.g., OpenZeppelin), and virtual machines (e.g., go-


                                                            35
                                           Transition-Oriented Programming                                   A P REPRINT



                                            Table 1: Typical DeFi incidents.
 Root Cause    Description                 Total   Loss     Incident Examples (Year, Affected Value)
 BF            Business Logic Flaw          23     $1.4B    Eleven Finance (2021, $4.5M), Parity (2017, $280M)
 RE            Reentrancy                    9     $147M    Rari Capital (2022, $80M), Grim Finance (2021, $30M)
 PM            Price Oracle Manipulation    20      $92M    Lodestar Finance (2022, $4M) , Harvest Finance (2020, $33.8M)
 IV            Insufficient Validation      10      $12M    OlympusDAO (2022, $292K), Anyswap (2022, $1.4M)
 AF            Access Control Flaw          13     $14M     TempleDAO (2022, $2.3M), Reaper Farm (2022, $1.7M)
 UE            Unexpected External Call      5       $3M    Rubic (2022, $1.5M), Rabby Wallet (2022, $200K)


ethereum) will prevent these vulnerabilities. Existing methods related to smart contract security, published in top-tier
venues and journals from 2018 to 2022, have proved to be adequate for finding generic vulnerabilities with common
patterns Singh et al. [2020], Durieux et al. [2020], such as insufficient validation, arbitrary external call, and typical
reentrancy vulnerabilities based on symbolic execution Mossberg et al. [2019], Krupp and Rossow [2018], Permenev
et al. [2020], model checking Wang et al. [2019], Frank et al. [2020], semantic pattern analysis Hildenbrandt et al.
[2018], Tsankov et al. [2018], and fuzzing Jiang et al. [2018], Nguyen et al. [2020], Choi et al. [2021].
Unfortunately, the top three severe root causes responsible for the most substantial financial losses pose a formidable
challenge for existing methods. Consider business logic flaws, the most severe vulnerability type, are exploited based
on understanding the conformity issues between requirement specifications and implementations. On account of their
particularity, highly automated methods Krupp and Rossow [2018], Wang et al. [2019], Nguyen et al. [2020] are not
applicable, while other methods Tsankov et al. [2018], Mossberg et al. [2019], Choi et al. [2021] are not scalable to
these patternless vulnerabilities. Besides, vulnerabilities stemming from potential price oracle manipulations bring
attackers exceptionally profitable arbitrage opportunities with low attack costs via flash loans. However, neither methods
based on control flow Krupp and Rossow [2018], Wang et al. [2019] and semantic pattern analysis Hildenbrandt et al.
[2018], Tsankov et al. [2018] nor symbolic execution Mossberg et al. [2019], So et al. [2021] and fuzzing Jiang et al.
[2018], Nguyen et al. [2020] can efficiently find these vulnerabilities. Additionally, reentrancy variants, exemplified by
the Rari Capital hack in 2022, where no typical recursive reentry via a callback function occurred, have emerged as new
threats since this specific pattern proves challenging for existing reentrancy detectors Mossberg et al. [2019], Wang
et al. [2019], Choi et al. [2021].
Motivated by finding DeFi security issues in the early stage, Transition-Oriented Program Analysis (TOPA) is
introduced to leverage TOP in finding DeFi vulnerabilities, exemplified by Context-Sensitive Concolic Verification
(CSCV) Ding et al. [2024]. Different from TOSA discussed in Section 4.2, TOPA analyzes concrete programs rather than
abstract protocols. Besides, TOPA extends its analytical purview to encompass both security and safety considerations.
Additionally, the analysis of TOPA incorporates both temporal and functional properties.




                             Figure 15: Overview of transition-oriented program analysis.

The workflow of TOPA is illustrated in Figure 15. The initial step involves system modeling, where programs are
abstracted into formal models, and properties specifying normal operational behaviors are formulated. Concurrently,
TOPA promotes contexts, extended from the context perception feature of TOP in Section 3.5, to optimize correctness
verification. If a property violation is identified, TOPA reports the threat action path along with any malicious
assignments, thereby facilitating the identification and mitigation of potential vulnerabilities.




                                                           36
                                           Transition-Oriented Programming                                   A P REPRINT



5     Related Work
Formal methods have been advancing software engineering to enable the development of safe and secure systems. As
discussed in Section 1 and Section 2, formal methods can be roughly categorized into: formal specification, formal
verification, and formal implementation.

5.1   Formal Specification

Formal languages introduced in Section 2.1 and Section 2.2 of Section 2 are of paramount importance for formal
specification. However, there is a marked preference for formal languages that offer higher expressiveness in practice.
To illustrate, process algebras are widely employed for reasoning about concurrent systems and communication protocols.
Notable examples include Communication Sequential Processes (CSP) Hoare [1978], Calculus of Communicating
Systems (CCS) Milner [1980], Language Of Temporal Ordering Specification (LOTOS) Bolognesi and Brinksma
[1987], and π-calculus Milner et al. [1992]. Concurrently, program logics such as Hoare logic Hoare [1969], lambda
calculus Barendregt [1984], and Z notation Spivey and Abrial [1992] are instrumental in the reasoning about program
behavior and structure.
With the advancement of modern system development, there has been a notable shift towards formal languages that
align with prevalent programming paradigms, such as object-oriented and functional programming. Languages such as
Alloy Jackson [2002], Dafny Leino [2010], Lean Moura and Ullrich [2021], and F* Swamy et al. [2016] exemplify this
trend, which proves to be more comprehensible to practitioners.

5.2   Formal Verification

Formal verification tools that mechanize correctness verification defined in Definition 2.18 can be broadly classified
into two categories: model checking and theorem proving.
Model checking techniques Clarke et al. [1994], Baier and Katoen [2008], Biere et al. [2009], Clarke Jr et al. [2018],
known for their high degree of automation, are often challenged by the state explosion problem Clarke et al. [2012].
This issue arises from the exponential growth in the number of states that need to be examined as system complexity
increases. To mitigate this, symbolic model checkers like NuSMV Cimatti et al. [2002] employ binary decision
diagrams, which offer a more efficient representation of stateful dynamics. Additionally, bounded model checkers like
CBMC Kroening and Tautschnig [2014] adopt a different strategy by unrolling the transition system for a predetermined
number of steps, thereby circumventing the need to explore the entire state space.
In contrast, theorem proving techniques Gordon and Melham [1993], Fitting [2012], Bibel [2013], Loveland [2016]
boast greater generality and expressiveness but typically necessitate human intervention, commonly leveraging proof
assistants to facilitate correctness verification through human-machine collaboration. Prominent proof assistants enable
a more interactive and comprehensive way of correctness verification, including Isabelle Nipkow et al. [2002], F*
Swamy et al. [2016], and Lean4 Moura and Ullrich [2021].

5.3   Formal Implementation

Formal implementation tools serve as a conduit between formal models and executables, which mechanizes correctness
implementation defined in Definition 2.21.
Model-Driven Engineering (MDE) Kent [2002], Schmidt [2006], Da Silva [2015] prioritizes system development
through the management of formal models. In MDE, formal models transcend their traditional role as mere specifications,
becoming the fundamental basis from which executables are derived. For instance, there is a focus on the code generation
from formal models, exemplified by Executable UML Mellor and Balcer [2002] and the Eclipse Modeling Framework
Steinberg et al. [2008]. Additionally, there is a research community dedicated to improving the interoperability of formal
models through model transformation techniques, as seen in DUALLy Malavolta et al. [2009]. Complementing these
approaches, formalism-driven development, as discussed in Ding and Sato [2022a,b], introduces a verification-focused
aspect by generating verification-oriented executables.




                                                           37
                                           Transition-Oriented Programming                                    A P REPRINT



6     Conclusion

This paper systematically discussed system correctness through three aspects: specification, verification, and imple-
mentation. First, it formalized correctness with formal models and logics by unifying the representations of transition
systems and rewriting systems and their typical variants as the fundamentals for a unified theoretical framework.
Meanwhile, formal correctness elucidates the essence of Q1, Q2, and Q3 introduced in Section 1.
Second, this paper presented TOP, a programming paradigm that facilitates the development of provably correct systems.
The central tenet of TOP is to seamlessly intertwine specification, verification, and implementation within a unified
theoretical framework. This ensures that a provably correct specification is a provably correct implementation, thus
providing a theoretical solution to Q2 and Q3. The framework is centered around GTSs, a formalism capturing
both stateful dynamics and structural transformations. Besides, TOP promotes intrinsic verification support to prove
correctness satisfiability regarding the formulated GTSs and their temporal and functional properties. This verification
process is grounded in model-checking and theorem-proving methods, yet is specifically refined for GTSs. Crucially,
TOP eliminates the gap between formal models and program implementations to enable executable formal models with
side effects.
Third, this paper presented the Seni language, a TOP language with fully-fledged features. Seni supports intuitively
constructing GTSs with side effects and formulating temporal and functional properties. Besides, it combines a bottom-
up (modularization) and a top-down (progressive specification) approach to enhance specifiability and verifiability.
Modularization focuses on improving scalability and reusability by enabling model parameterization and composition,
while progressive specification enables an iterative and incremental process for model and property specifications via
model refinement techniques. Additionally, Seni introduces context perception to facilitate precise specification and
efficient verification. Furthermore, the current version of Seni also intrinsically supports correctness verification at
compile time through fully automated techniques, including bounded model checking and iterative deepening theorem
proving. Concurrently, Seni demonstrates a practical solution to Q1, Q2, and Q3.
Finally, this paper illustrated three practical scenarios with TOP. It initially delineated transition-oriented develop-
ment, a development process designed to develop provably correct distributed protocols. Subsequently, the paper
introduced transition-oriented security analysis for security infrastructures by TOP, exemplified by SecureSSI formally
assessing self-sovereign identity systems against threat models that address security concerns. Lastly, this paper pre-
sented transition-oriented program analysis through CSCV in identifying vulnerabilities of decentralized applications,
particularly targeting DeFi systems.

6.1     TOP Vision

In addition to the three application scenarios illustrated in Section 4.1, Section 4.2, and Section 4.3, TOP holds the
potential for the development, verification, and optimization of compiling tools, explainable artificial intelligence, and
hardware.

6.1.1    Compiling Tool Development

TOP provides a comprehensive and coherent method for programming language design and implementation. At the
syntactic level, TOP affords a robust formalism, enabling the precise definition of languages by facilitating the formal
specification of both sequential and functional models of computation, which is pivotal in establishing a consistent and
unambiguous language structure. Moving to the semantic level, TOP enables an effective and intuitive representation of
the operational semantics Plotkin [1981] of languages through GTSs, which offers a provable mapping between the
language semantics and their execution mechanisms. Furthermore, TOP promotes the formulation of both temporal and
functional properties that are critical in specifying the behavior of compiling tools and ensures their correctness through
formal verification.
Additionally, existing compiling tools can be encoded into GTSs associated with properties for formal analysis to
identify vulnerabilities and explore potential optimization via the proof automation techniques, including BMC and
IDTP introduced in Section 3.6.

6.1.2    Explainable Artificial Intelligence

TOP can facilitate the development of explainable AI systems. Based on formal logic, TOP enables the precise
specification of machine learning models, thereby articulating the reasoning behind their decisions. Meanwhile, the
expected model properties of training and prediction processes can be encoded into GTSs that precisely describe model


                                                            38
                                           Transition-Oriented Programming                                    A P REPRINT



behaviors. By the intrinsic verification of TOP, these properties are formally verified before the real processes to ensure
model safety in practical applications.
Besides, encoding neural networks into GTSs under TOP provides a clear window into the operations of both training
and predicting phases. This transparency is critical in understanding the relationship between input features and their
corresponding outputs, which is particularly beneficial in counterfactual explanations that illustrate how variations in
certain inputs could lead to different outcomes.
Particularly, TOP offers a structured method of unraveling the complex pattern within graph-structured data since Graph
Neural Networks (GNN)Wu et al. [2020], known for their effectiveness in handling graph data, can greatly benefit from
the logical reasoning provided by TOP.

6.1.3    Hardware Design
TOP has the potential to facilitate hardware design, especially in the context of High-Level Synthesis (HLS) Gajski
et al. [2012]. GTSs are expressive to encode circuit designs and their corresponding expected properties. A noteworthy
parallel exists between the communication protocols designed for circuits, such as handshake mechanisms Edwards et al.
[2019]. In the same manner, the modularization feature of TOP, as discussed in Section 3.3, along with the progressive
specification approach detailed in Section 3.4, endows TOP with the capability to specify large-scale circuit designs
effectively. Furthermore, the formal verification of TOP plays a crucial role in optimizing circuit designs and ensuring
their safety. Additionally, the potential of a TOP language, such as Seni introduced in Section 3.2, extends to generating
Register-Transfer Level (RTL) designs that can be subsequently synthesized to the gate level through the application of
a logic synthesis tool.

6.2     Future Direction

As a nascent programming paradigm, TOP is on a trajectory toward establishing an ecosystem that facilitates the
development of provably correct systems across diverse domains. Looking ahead, the Seni language, as a practical
embodiment of TOP, plays a pivotal role in advancing the theoretical framework that underpins TOP.
Concretely, Seni is set to augment syntactic sugar to be more expressive in modeling complex structures and behaviors.
This enhancement will include the integration of functional styles reminiscent of programming languages like Haskell,
specifically for formulating transformation relations of GTSs. Besides, Seni aims to incorporate a suite of ready-to-use
modules designed to streamline the development of real-world applications, such as network modules at the syntactic
level, operating system modules, and enhanced I/O modules.
Besides, Seni is positioned to broaden its repertoire of proof techniques and optimize compatibility with existing tools.
The roadmap includes the introduction of the mathematical induction capability, complemented by semi-automated
theorem proving techniques. The objective is to enhance Seni’s verification prowess and further refine the theoretical
framework to incorporate usable proof techniques.
Moreover, Seni is strategically set to leverage interactions with language processing methods like Large Language
Models (LLMs) Brown et al. [2020] to aid in the comprehension of model and property specifications, which is
particularly pertinent when dealing with complex models and large-size formulas. Meanwhile, introducing machine
learning approaches presents a promising avenue to assist developers who may not possess extensive mathematical
expertise. Based on these approaches, Seni aims to facilitate a more intuitive and user-friendly way of understanding
and working with the concepts of TOP and lowers the barriers to entry for developers with diverse backgrounds.
As Seni evolves, its applicability is expected to become wider. Seni will continue to be applied in the studied domains,
such as distributed protocols, security infrastructures, and decentralized applications. Simultaneously, Seni intends
to branch out into other promising fields, as outlined in Section 6.1, such as the development of compiling tools,
the exploration of explainable artificial intelligence, and advancements in hardware design. This strategic expansion
is not merely an extension of Seni’s applicability but a testament to the growing influence of TOP as a formidable
programming paradigm to develop provably correct systems.




                                                            39
                                         Transition-Oriented Programming                                  A P REPRINT



References
Dean Leffingwell and Don Widrig. Managing software requirements: a unified approach. Addison-Wesley Professional,
  2000. ISBN 0-201-61593-2.
Christel Baier and Joost-Pieter Katoen. Principles of model checking. MIT press, 2008. ISBN 0-262-30403-1.
Edmund M. Clarke Jr, Orna Grumberg, Daniel Kroening, Doron Peled, and Helmut Veith. Model checking. MIT press,
  2018. ISBN 0-262-34945-0.
Gerard J. Holzmann. The model checker SPIN. IEEE Transactions on software engineering, 23(5):279–295, 1997.
  ISBN: 0098-5589 Publisher: IEEE.
Alessandro Cimatti, Edmund Clarke, Enrico Giunchiglia, Fausto Giunchiglia, Marco Pistore, Marco Roveri, Roberto
  Sebastiani, and Armando Tacchella. Nusmv 2: An opensource tool for symbolic model checking. In International
  conference on computer aided verification, pages 359–364. Springer, 2002.
Daniel Kroening and Michael Tautschnig. CBMC–C Bounded Model Checker: (Competition Contribution). In Tools
  and Algorithms for the Construction and Analysis of Systems: 20th International Conference, TACAS 2014, Held as
  Part of the European Joint Conferences on Theory and Practice of Software, ETAPS 2014, Grenoble, France, April
  5-13, 2014. Proceedings 20, pages 389–391. Springer, 2014. ISBN 3-642-54861-X.
Roberto Baldoni, Emilio Coppa, Daniele Cono D’elia, Camil Demetrescu, and Irene Finocchi. A survey of symbolic
  execution techniques. ACM Computing Surveys (CSUR), 51(3):1–39, 2018. ISBN: 0360-0300 Publisher: ACM New
  York, NY, USA.
Willem Visser, Corina S. Pǎsǎreanu, and Sarfraz Khurshid. Test input generation with Java PathFinder. In Proceedings
 of the 2004 ACM SIGSOFT international symposium on Software testing and analysis, pages 97–107, 2004.
Cristian Cadar, Daniel Dunbar, and Dawson R. Engler. Klee: Unassisted and automatic generation of high-coverage
  tests for complex systems programs. In OSDI, volume 8, pages 209–224, 2008.
M. Irlbeck. Deconstructing dynamic symbolic execution. Dependable Software Systems Engineering, 40(2015):26,
 2015. Publisher: IOS Press.
Wolfgang Bibel. Automated theorem proving. Springer Science & Business Media, 2013. ISBN 3-322-90102-5.
Lawrence C. Paulson. Isabelle: A generic theorem prover, volume 828. Springer Science & Business Media, 1994.
  ISBN 3-540-58244-4.
Nikhil Swamy, Cătălin Hriţcu, Chantal Keller, Aseem Rastogi, Antoine Delignat-Lavaud, Simon Forest, Karthikeyan
  Bhargavan, Cédric Fournet, Pierre-Yves Strub, and Markulf Kohlweiss. Dependent types and multi-monadic effects in
  F. In Proceedings of the 43rd annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages,
  pages 256–270, 2016.
Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and programming language. In Automated
  Deduction–CADE 28: 28th International Conference on Automated Deduction, Virtual Event, July 12–15, 2021,
  Proceedings 28, pages 625–635. Springer, 2021. ISBN 3-030-79875-5.
Franz Baader and Tobias Nipkow. Term rewriting and all that. Cambridge university press, 1998. ISBN 0-521-77920-0.
Jürgen Giesl, René Thiemann, Peter Schneider-Kamp, and Stephan Falke. Automated termination proofs with AProVE.
  In Rewriting Techniques and Applications: 15th International Conference, RTA 2004, Aachen, Germany, June 3-5,
  2004. Proceedings 15, pages 210–220. Springer, 2004. ISBN 3-540-22153-0.
Ashutosh Gupta, Thomas A. Henzinger, Rupak Majumdar, Andrey Rybalchenko, and Ru-Gang Xu. Proving non-
  termination. In Proceedings of the 35th annual ACM SIGPLAN-SIGACT symposium on Principles of programming
  languages, pages 147–158, 2008.
Martin Korp, Christian Sternagel, Harald Zankl, and Aart Middeldorp. Tyrolean termination tool 2. In Rewriting
 Techniques and Applications: 20th International Conference, RTA 2009 Brasília, Brazil, June 29-July 1, 2009
 Proceedings 20, pages 295–304. Springer, 2009. ISBN 3-642-02347-9.
Radhakisan Baheti and Helen Gill. Cyber-physical systems. The impact of control technology, 12(1):161–166, 2011.
Edward A. Lee. The past, present and future of cyber-physical systems: A focus on models. Sensors, 15(3):4837–4869,
  2015. ISBN: 1424-8220 Publisher: Multidisciplinary Digital Publishing Institute.
Li Da Xu, Wu He, and Shancang Li. Internet of things in industries: A survey. IEEE Transactions on industrial
  informatics, 10(4):2233–2243, 2014. ISBN: 1551-3203 Publisher: IEEE.
Shancang Li, Li Da Xu, and Shanshan Zhao. The internet of things: a survey. Information systems frontiers, 17:
  243–259, 2015. ISBN: 1387-3326 Publisher: Springer.


                                                         40
                                         Transition-Oriented Programming                                 A P REPRINT



Michael I. Jordan and Tom M. Mitchell. Machine learning: Trends, perspectives, and prospects. Science, 349(6245):
 255–260, 2015. ISBN: 0036-8075 Publisher: American Association for the Advancement of Science.
Batta Mahesh. Machine learning algorithms-a review. International Journal of Science and Research (IJSR).[Internet],
  9(1):381–386, 2020.
Tharam Dillon, Chen Wu, and Elizabeth Chang. Cloud computing: issues and challenges. In 2010 24th IEEE
  international conference on advanced information networking and applications, pages 27–33. Ieee, 2010. ISBN
  1-4244-6696-2.
Yuyi Mao, Changsheng You, Jun Zhang, Kaibin Huang, and Khaled B. Letaief. A survey on mobile edge computing: The
  communication perspective. IEEE communications surveys & tutorials, 19(4):2322–2358, 2017. ISBN: 1553-877X
  Publisher: IEEE.
Yepeng Ding and Hiroyuki Sato. Derepo: A Distributed Privacy-Preserving Data Repository with Decentralized
  Access Control for Smart Health. In 2020 7th IEEE International Conference on Cyber Security and Cloud
  Computing (CSCloud)/2020 6th IEEE International Conference on Edge Computing and Scalable Cloud (EdgeCom),
  pages 29–35. IEEE, 2020a. ISBN 1-72816-550-4. doi:10.1109/CSCloud-EdgeCom49738.2020.00015. URL
  https://ieeexplore.ieee.org/document/9170998.
Yepeng Ding and Hiroyuki Sato. Dagbase: A Decentralized Database Platform Using DAG-Based Consensus.
  In 2020 IEEE 44th Annual Computers, Software, and Applications Conference (COMPSAC), pages 798–807,
  Madrid, Spain, 2020b. IEEE. ISBN 1-72817-303-5. doi:10.1109/COMPSAC48688.2020.0-164. URL https:
  //ieeexplore.ieee.org/document/9202805.
Yepeng Ding and Hiroyuki Sato. Bloccess: Enabling Fine-Grained Access Control Based on Blockchain. Journal of
  Network and Systems Management, 31(1):1–34, 2023a. doi:10.1007/s10922-022-09700-5. URL https://link.
  springer.com/article/10.1007/s10922-022-09700-5.
Gavin Wood. Ethereum: A secure decentralised generalised transaction ledger. Ethereum project yellow paper, 151
  (2014):1–32, 2014.
Satoshi Nakamoto. Bitcoin: A peer-to-peer electronic cash system. Technical report, Manubot, 2019.
Zibin Zheng, Shaoan Xie, Hong-Ning Dai, Xiangping Chen, and Huaimin Wang. Blockchain challenges and opportuni-
  ties: A survey. International Journal of Web and Grid Services, 14(4):352–375, 2018. ISBN: 1741-1106 Publisher:
  Inderscience Publishers (IEL).
Jack Ratcliffe, Francesco Soave, Nick Bryan-Kinns, Laurissa Tokarchuk, and Ildar Farkhatdinov. Extended reality (XR)
  remote research: a survey of drawbacks and opportunities. In Proceedings of the 2021 CHI Conference on Human
  Factors in Computing Systems, pages 1–13, 2021.
Stephen A. Cook. The complexity of theorem-proving procedures. In Logic, Automata, and Computational Complexity:
  The Works of Stephen A. Cook, pages 143–152. 2023.
Rajeev Alur, Thomas A. Henzinger, Orna Kupferman, and Moshe Y. Vardi. Alternating refinement relations. In
  CONCUR’98 Concurrency Theory: 9th International Conference Nice, France, September 8–11, 1998 Proceedings
  9, pages 163–178. Springer, 1998. ISBN 3-540-64896-8.
Corina S. Păsăreanu, Radek Pelánek, and Willem Visser. Concrete model checking with abstract matching and
  refinement. In Computer Aided Verification: 17th International Conference, CAV 2005, Edinburgh, Scotland, UK,
  July 6-10, 2005. Proceedings 17, pages 52–66. Springer, 2005. ISBN 3-540-27231-3.
Yepeng Ding and Hiroyuki Sato. Formalism-Driven Development of Decentralized Systems. In 2022 26th International
  Conference on Engineering of Complex Computer Systems (ICECCS), pages 81–90, Hiroshima, Japan, 2022a. IEEE.
  ISBN 978-1-66540-162-3. doi:10.1109/ICECCS54210.2022.00018.
Antti Valmari. The state explosion problem. In Advanced Course on Petri Nets, pages 429–528. Springer, 1996.
Armin Biere, Alessandro Cimatti, Edmund M. Clarke, Ofer Strichman, and Yunshan Zhu. Bounded model checking.
  Handbook of satisfiability, 185(99):457–481, 2009.
Leonardo de Moura, Soonho Kong, Jeremy Avigad, Floris van Doorn, and Jakob von Raumer. The Lean theorem prover
  (system description). In International Conference on Automated Deduction, pages 378–388. Springer, 2015.
Leslie Lamport. Time, clocks, and the ordering of events in a distributed system. In Concurrency: the Works of Leslie
  Lamport, pages 179–196. 2019a.
Leslie Lamport. The part-time parliament. In Concurrency: the Works of Leslie Lamport, pages 277–317. 2019b.
Miguel Castro and Barbara Liskov. Practical byzantine fault tolerance. In OsDI, volume 99, pages 173–186, 1999.
 Issue: 1999.


                                                         41
                                         Transition-Oriented Programming                                 A P REPRINT



Philip A. Bernstein, Vassos Hadzilacos, and Nathan Goodman. Concurrency control and recovery in database systems,
   volume 370. Addison-wesley Reading, 1987.
Hong-Ning Dai, Zibin Zheng, and Yan Zhang. Blockchain for Internet of Things: A survey. IEEE Internet of Things
   Journal, 6(5):8076–8094, 2019. ISBN: 2327-4662 Publisher: IEEE.
Cynthia Dwork and Moni Naor. Pricing via processing or combatting junk mail. In Annual international cryptology
   conference, pages 139–147. Springer, 1992.
Diego Ongaro and John Ousterhout. In search of an understandable consensus algorithm. In 2014 USENIX annual
   technical conference (USENIX ATC 14), pages 305–319, 2014. ISBN 1-931971-10-2.
Ying Fu, Meng Ren, Fuchen Ma, Heyuan Shi, Xin Yang, Yu Jiang, Huizhong Li, and Xiang Shi. Evmfuzzer: detect
   evm vulnerabilities via fuzz testing. In Proceedings of the 2019 27th ACM Joint Meeting on European Software
   Engineering Conference and Symposium on the Foundations of Software Engineering, pages 1110–1114, 2019.
Youngseok Yang, Taesoo Kim, and Byung-Gon Chun. Finding Consensus Bugs in Ethereum via Multi-transaction
   Differential Fuzzing. In 15th {USENIX} Symposium on Operating Systems Design and Implementation ({OSDI} 21),
   pages 349–365, 2021. ISBN 1-939133-22-X.
Giuseppe Destefanis, Michele Marchesi, Marco Ortu, Roberto Tonelli, Andrea Bracciali, and Robert Hierons. Smart
   contracts vulnerabilities: a call for blockchain software engineering? In 2018 International Workshop on Blockchain
   Oriented Software Engineering (IWBOSE), pages 19–25. IEEE, 2018. ISBN 1-5386-5986-7.
Yepeng Ding and Hiroyuki Sato. Formalism-Driven Development: Concepts, Taxonomy, and Practice. Applied
   Sciences, 12(7), 2022b. ISSN 2076-3417. doi:10.3390/app12073415. URL https://www.mdpi.com/2076-3417/
   12/7/3415.
James Shore. The Art of Agile Development: Pragmatic guide to agile software development. " O’Reilly Media, Inc.",
   2007. ISBN 0-596-55379-X.
Leonardo De Moura and Nikolaj Bjørner. Z3: An efficient SMT solver. In International conference on Tools and
   Algorithms for the Construction and Analysis of Systems, pages 337–340. Springer, 2008.
Stefan Brands. Rethinking public key infrastructures and digital certificates: building in privacy. Mit Press, 2000.
   ISBN 0-262-26166-9.
Jesse C. Ribot and Nancy Lee Peluso. A theory of access. Rural sociology, 68(2):153–181, 2003. ISBN: 0036-0112
   Publisher: Wiley Online Library.
David Recordon and Drummond Reed. OpenID 2.0: a platform for user-centric identity management. In Proceedings
   of the second ACM workshop on Digital identity management, pages 11–16, 2006.
Yepeng Ding and Hiroyuki Sato. Self-Sovereign Identity as a Service: Architecture in Practice. In 2022 IEEE 46th
   Annual Computers, Software, and Applications Conference (COMPSAC), pages 1536–1543, Los Alamitos, CA, USA,
   2022c. IEEE. ISBN 978-1-66548-810-5.
Yepeng Ding and Hiroyuki Sato. Model-Driven Security Analysis of Self-Sovereign Identity Systems. In 2023 IEEE
   International Conference on Trust, Security and Privacy in Computing and Communications (TrustCom). IEEE,
   2023b. to appear.
Elli Androulaki, Artem Barger, Vita Bortnikov, Christian Cachin, Konstantinos Christidis, Angelo De Caro, David
   Enyeart, Christopher Ferris, Gennady Laventman, and Yacov Manevich. Hyperledger fabric: a distributed operating
   system for permissioned blockchains. In Proceedings of the thirteenth EuroSys conference, pages 1–15, 2018.
Jiahua Xu, Krzysztof Paruch, Simon Cousaert, and Yebo Feng. Sok: Decentralized exchanges (dex) with automated
   market maker (amm) protocols. ACM Computing Surveys, 55(11):1–50, 2023. ISBN: 0360-0300 Publisher: ACM
   New York, NY.
Shayan Eskandari, Jeremy Clark, Vignesh Sundaresan, and Moe Adham. On the feasibility of decentralized derivatives
   markets. In Financial Cryptography and Data Security: FC 2017 International Workshops, WAHC, BITCOIN,
   VOTING, WTSC, and TA, Sliema, Malta, April 7, 2017, Revised Selected Papers 21, pages 553–567. Springer, 2017.
   ISBN 3-319-70277-7.
Massimo Bartoletti, James Hsin-yu Chiang, and Alberto Lluch Lafuente. SoK: lending pools in decentralized finance.
   In Financial Cryptography and Data Security. FC 2021 International Workshops: CoDecFin, DeFi, VOTING,
   and WTSC, Virtual Event, March 5, 2021, Revised Selected Papers 25, pages 553–578. Springer, 2021. ISBN
   3-662-63957-2.
Weiqin Zou, David Lo, Pavneet Singh Kochhar, Xuan-Bach Dinh Le, Xin Xia, Yang Feng, Zhenyu Chen, and Baowen
   Xu. Smart contract development: Challenges and opportunities. IEEE Transactions on Software Engineering, 47(10):
   2084–2106, 2019. ISBN: 0098-5589 Publisher: IEEE.


                                                         42
                                          Transition-Oriented Programming                                 A P REPRINT



Christof Ferreira Torres, Julian Schütte, and Radu State. Osiris: Hunting for integer bugs in ethereum smart contracts.
  In Proceedings of the 34th Annual Computer Security Applications Conference, pages 664–676, 2018.
Jianbo Gao, Han Liu, Chao Liu, Qingshan Li, Zhi Guan, and Zhong Chen. Easyflow: Keep ethereum away from
   overflow. In 2019 IEEE/ACM 41st International Conference on Software Engineering: Companion Proceedings
   (ICSE-Companion), pages 23–26. IEEE, 2019. ISBN 1-72811-764-X.
Michael Rodler, Wenting Li, Ghassan O. Karame, and Lucas Davi. EVMPatch: Timely and Automated Patching of
 Ethereum Smart Contracts. In USENIX Security Symposium, pages 1289–1306, 2021.
Amritraj Singh, Reza M. Parizi, Qi Zhang, Kim-Kwang Raymond Choo, and Ali Dehghantanha. Blockchain smart
 contracts formalization: Approaches and challenges to address vulnerabilities. Computers & Security, 88:101654,
 2020. ISBN: 0167-4048 Publisher: Elsevier.
Thomas Durieux, João F. Ferreira, Rui Abreu, and Pedro Cruz. Empirical review of automated analysis tools on 47,587
  ethereum smart contracts. In Proceedings of the ACM/IEEE 42nd International conference on software engineering,
  pages 530–541, 2020.
Mark Mossberg, Felipe Manzano, Eric Hennenfent, Alex Groce, Gustavo Grieco, Josselin Feist, Trent Brunson, and
 Artem Dinaburg. Manticore: A user-friendly symbolic execution framework for binaries and smart contracts. In
 2019 34th IEEE/ACM International Conference on Automated Software Engineering (ASE), pages 1186–1189. IEEE,
 2019. ISBN 1-72812-508-1.
Johannes Krupp and Christian Rossow. {teEther}: Gnawing at Ethereum to Automatically Exploit Smart Contracts. In
  27th USENIX Security Symposium (USENIX Security 18), pages 1317–1333, 2018. ISBN 1-939133-04-1.
Anton Permenev, Dimitar Dimitrov, Petar Tsankov, Dana Drachsler-Cohen, and Martin Vechev. Verx: Safety verification
  of smart contracts. In 2020 IEEE symposium on security and privacy (SP), pages 1661–1677. IEEE, 2020. ISBN
 1-72813-497-8.
Shuai Wang, Chengyu Zhang, and Zhendong Su. Detecting nondeterministic payment bugs in Ethereum smart contracts.
  Proceedings of the ACM on Programming Languages, 3(OOPSLA):1–29, 2019. ISBN: 2475-1421 Publisher: ACM
  New York, NY, USA.
Joel Frank, Cornelius Aschermann, and Thorsten Holz. {ETHBMC}: A Bounded Model Checker for Smart Contracts.
  In 29th USENIX Security Symposium (USENIX Security 20), pages 2757–2774, 2020. ISBN 1-939133-17-3.
Everett Hildenbrandt, Manasvi Saxena, Nishant Rodrigues, Xiaoran Zhu, Philip Daian, Dwight Guth, Brandon Moore,
  Daejun Park, Yi Zhang, and Andrei Stefanescu. Kevm: A complete formal semantics of the ethereum virtual
  machine. In 2018 IEEE 31st Computer Security Foundations Symposium (CSF), pages 204–217. IEEE, 2018. ISBN
  1-5386-6680-4.
Petar Tsankov, Andrei Dan, Dana Drachsler-Cohen, Arthur Gervais, Florian Buenzli, and Martin Vechev. Securify:
  Practical security analysis of smart contracts. In Proceedings of the 2018 ACM SIGSAC Conference on Computer
  and Communications Security, pages 67–82, 2018.
Bo Jiang, Ye Liu, and Wing Kwong Chan. Contractfuzzer: Fuzzing smart contracts for vulnerability detection. In 2018
  33rd IEEE/ACM International Conference on Automated Software Engineering (ASE), pages 259–269. IEEE, 2018.
  ISBN 1-4503-5937-X.
Tai D. Nguyen, Long H. Pham, Jun Sun, Yun Lin, and Quang Tran Minh. sfuzz: An efficient adaptive fuzzer for solidity
  smart contracts. In Proceedings of the ACM/IEEE 42nd International Conference on Software Engineering, pages
  778–788, 2020.
Jaeseung Choi, Doyeon Kim, Soomin Kim, Gustavo Grieco, Alex Groce, and Sang Kil Cha. SMARTIAN: Enhancing
  smart contract fuzzing with static and dynamic data-flow analyses. In 2021 36th IEEE/ACM International Conference
  on Automated Software Engineering (ASE), pages 227–239. IEEE, 2021. ISBN 1-66540-337-3.
Sunbeom So, Seongjoon Hong, and Hakjoo Oh. SmarTest: Effectively Hunting Vulnerable Transaction Sequences
  in Smart Contracts through Language Model-Guided Symbolic Execution. In USENIX Security Symposium, pages
  1361–1378, 2021.
Yepeng Ding, Arthur Gervais, Roger Wattenhofer, and Hiroyuki Sato. Hunting DeFi Vulnerabilities via Context-
  Sensitive Concolic Verification. In 2024 IEEE/ACM 46th International Conference on Software Engineering:
  Companion Proceedings (ICSE-Companion). IEEE, 2024. to appear.
Charles Antony Richard Hoare. Communicating sequential processes. Communications of the ACM, 21(8):666–677,
  1978. ISBN: 0001-0782 Publisher: ACM New York, NY, USA.
Robin Milner. A calculus of communicating systems. Springer, 1980.


                                                         43
                                        Transition-Oriented Programming                               A P REPRINT



Tommaso Bolognesi and Ed Brinksma. Introduction to the ISO specification language LOTOS. Computer Networks
   and ISDN systems, 14(1):25–59, 1987. ISBN: 0169-7552 Publisher: Elsevier.
Robin Milner, Joachim Parrow, and David Walker. A calculus of mobile processes, I. Information and computation,
   100(1):1–40, 1992. ISBN: 0890-5401 Publisher: Elsevier.
Charles Antony Richard Hoare. An axiomatic basis for computer programming. Communications of the ACM, 12(10):
   576–580, 1969. ISBN: 0001-0782 Publisher: ACM New York, NY, USA.
Hendrik P. Barendregt. The lambda calculus, volume 3. North-Holland Amsterdam, 1984.
J. Michael Spivey and Jean-Raymond Abrial. The Z notation, volume 29. Prentice Hall Hemel Hempstead, 1992.
Daniel Jackson. Alloy: a lightweight object modelling notation. ACM Transactions on software engineering and
   methodology (TOSEM), 11(2):256–290, 2002. ISBN: 1049-331X Publisher: ACM New York, NY, USA.
K. Rustan M. Leino. Dafny: An automatic program verifier for functional correctness. In International conference on
   logic for programming artificial intelligence and reasoning, pages 348–370. Springer, 2010.
Edmund M. Clarke, Orna Grumberg, and David E. Long. Model checking and abstraction. ACM transactions on
   Programming Languages and Systems (TOPLAS), 16(5):1512–1542, 1994. ISBN: 0164-0925 Publisher: ACM New
   York, NY, USA.
Edmund M. Clarke, William Klieber, Miloš Nováček, and Paolo Zuliani. Model checking and the state explosion
   problem. Tools for Practical Software Verification: LASER, International Summer School 2011, Elba Island, Italy,
   Revised Tutorial Lectures, pages 1–30, 2012. ISBN: 3642357458 Publisher: Springer.
Michael JC Gordon and Tom F. Melham. Introduction to HOL: A theorem proving environment for higher order logic.
   Cambridge University Press, 1993. ISBN 0-521-44189-7.
Melvin Fitting. First-order logic and automated theorem proving. Springer Science & Business Media, 2012. ISBN
   1-4612-2360-1.
Donald W. Loveland. Automated theorem proving: A logical basis. Elsevier, 2016. ISBN 1-4832-9677-6.
Tobias Nipkow, Lawrence C. Paulson, and Markus Wenzel. Isabelle/HOL: a proof assistant for higher-order logic,
   volume 2283. Springer Science & Business Media, 2002. ISBN 3-540-43376-7.
Stuart Kent. Model driven engineering. In International conference on integrated formal methods, pages 286–298.
   Springer, 2002.
Douglas C. Schmidt. Model-driven engineering. Computer-IEEE Computer Society-, 39(2):25, 2006. ISBN: 0018-9162
   Publisher: Citeseer.
Alberto Rodrigues Da Silva. Model-driven engineering: A survey supported by the unified conceptual model. Computer
   Languages, Systems & Structures, 43:139–155, 2015. ISBN: 1477-8424 Publisher: Elsevier.
Stephen J. Mellor and Marc J. Balcer. Executable UML: a foundation for model-driven architecture. Addison-Wesley
   Professional, 2002. ISBN 0-201-74804-5.
Dave Steinberg, Frank Budinsky, Ed Merks, and Marcelo Paternostro. EMF: eclipse modeling framework. Pearson
   Education, 2008. ISBN 0-13-270221-5.
Ivano Malavolta, Henry Muccini, Patrizio Pelliccione, and Damien Tamburri. Providing architectural languages and
   tools interoperability through model transformation technologies. IEEE Transactions on Software Engineering, 36
   (1):119–140, 2009. ISBN: 0098-5589 Publisher: IEEE.
Gordon D. Plotkin. A structural approach to operational semantics. Aarhus university, 1981.
Zonghan Wu, Shirui Pan, Fengwen Chen, Guodong Long, Chengqi Zhang, and S. Yu Philip. A comprehensive survey
   on graph neural networks. IEEE transactions on neural networks and learning systems, 32(1):4–24, 2020. ISBN:
   2162-237X Publisher: IEEE.
Daniel D. Gajski, Nikil D. Dutt, Allen CH Wu, and Steve YL Lin. High—Level Synthesis: Introduction to Chip and
   System Design. Springer Science & Business Media, 2012. ISBN 1-4615-3636-7.
Stephen A. Edwards, Richard Townsend, Martha Barker, and Martha A. Kim. Compositional dataflow circuits. ACM
   Transactions on Embedded Computing Systems (TECS), 18(1):1–27, 2019. ISBN: 1539-9087 Publisher: ACM New
   York, NY, USA.
Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D. Kaplan, Prafulla Dhariwal, Arvind Neelakantan,
   Pranav Shyam, Girish Sastry, and Amanda Askell. Language models are few-shot learners. Advances in neural
   information processing systems, 33:1877–1901, 2020.



                                                        44
