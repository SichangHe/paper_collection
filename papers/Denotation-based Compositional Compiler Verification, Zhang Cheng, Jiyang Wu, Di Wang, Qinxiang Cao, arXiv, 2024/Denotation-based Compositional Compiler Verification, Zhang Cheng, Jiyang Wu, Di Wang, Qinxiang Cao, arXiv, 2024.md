                                         Denotation-based Compositional Compiler Verification
                                         ZHANG CHENG, Shanghai Jiao Tong University, China
                                         JIYANG WU, Shanghai Jiao Tong University, China
                                         DI WANG, Peking University, China
                                         QINXIANG CAO∗ , Shanghai Jiao Tong University, China
                                         A desired but challenging property of compiler verification is compositionality, in the sense that the compilation
                                         correctness of a program can be deduced incrementally from that of its substructures ranging from statements,
                                         functions, and modules. This article proposes a novel compiler verification framework based on denotational
arXiv:2404.17297v3 [cs.PL] 29 Mar 2026




                                         semantics for better compositionality, compared to previous approaches based on small-step operational
                                         semantics and simulation theories. Our denotational semantics is defined by semantic functions that map a
                                         syntactic component to a semantic domain composed of multiple behavioral sets, with compiler correctness
                                         established through behavior refinement between the semantic domains of the source and target programs.
                                         The main contributions of this article include proposing a denotational semantics for open modules, a novel
                                         semantic linking operator, and a refinement algebra that unifies various behavior refinements, making compiler
                                         verification structured and compositional. Furthermore, our formalization captures the full meaning of a
                                         program and bridges the gap between traditional power-domain-based denotational semantics and the practical
                                         needs of compiler verification. We apply our denotation-based framework to verify the front-end of CompCert
                                         and typical optimizations on simple prototypes of imperative languages. Our results demonstrate that the
                                         compositionality from sub-statements to statements, from functions to modules, and from modules to the
                                         whole program can be effectively achieved.
                                         CCS Concepts: • Software and its engineering → Software verification; Compilers; • Theory of compu-
                                         tation → Denotational semantics.
                                         Additional Key Words and Phrases: compiler verification, denotational semantics, compositionality, CompCert

                                         1   Introduction
                                         Research on compiler verification has a long history. The state-of-the-art achievement in this field
                                         is CompCert [Leroy and INRIA 2024]. Specifically, CompCert translates programs written in a large
                                         subset of C into optimized assembly code, going through multiple intermediate languages. For each
                                         of them, program behavior is formulated by a labeled transition system (LTS) according to the
                                         small-step operational semantics. Compiler correctness is then achieved by showing a backward
                                         simulation1 asserting that every execution step of the target program can be simulated by zero or
                                         more execution steps of the source program in a behaviorally consistent way, as shown in Fig. 1a.
                                            This article proposes a different framework for compiler verification—a denotation-based ap-
                                         proach that focuses on the overall properties of programs and enjoys better proof compositionality.
                                         ∗ Corresponding author
                                         1 In fact, CompCert verifies almost all compilation phases using forward simulation, and then derives the backward simulation

                                         by certain side conditions after vertically composing the compilation correctness of each phase.
                                         2 The relation 𝑅 can be indexed by a natural number that strictly decreases on source stuttering steps, ensuring progress.


                                         Authors’ Contact Information: Zhang Cheng, mooc3535@gmail.com, Shanghai Jiao Tong University, Shanghai, China;
                                         Jiyang Wu, wujiyang@sjtu.edu.cn, Shanghai Jiao Tong University, Shanghai, China; Di Wang, wangdi95@pku.edu.cn,
                                         Peking University, Beijing, China; Qinxiang Cao, caoqinxiang@gmail.com, Shanghai Jiao Tong University, Shanghai, China.



                                         This work is licensed under a Creative Commons Attribution 4.0 International License.
                                         © 2026 Copyright held by the owner/author(s).
                                         ACM 1558-4593/2026/3-ART5
                                         https://doi.org/10.1145/3797874


                                              ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:2                                                                                                           Z. Cheng et al.


                              ∗ ′                             J𝑐K                                     J𝑐K
            𝜎𝑠                 𝜎𝑠                     𝜎𝑠              𝜎𝑠′                     𝜎𝑠              𝜎𝑠′

           𝑅                        𝑅                =                   =                   𝑅                    𝑅

                    JT (𝑐)K                                 JT (𝑐)K                                 JT (𝑐)K
            𝜎𝑡                 𝜎𝑡′                    𝜎𝑡              𝜎𝑡′                     𝜎𝑡              𝜎𝑡′

      (a) The backward simulation2            (b) Simple behavior refinement         (c) General behavior refinement

      Fig. 1. The backward simulation of CompCert and the behavior refinement between denotations.


For example, considering type-safe and nondeterministic programs with the set of program states
state, a textbook denotational semantics [Plotkin 1983, Chapter 8] for a program statement 𝑐 can
be defined by a binary relation between lifted program states (i.e., J𝑐K ⊆ state × state⊥ 3 ), meaning
that for any (𝜎1, 𝜎2 ) ∈ J𝑐K, executing statement 𝑐 from state 𝜎1 may eventually terminate at state
𝜎2 if 𝜎2 ≠ ⊥, or otherwise (𝜎2 = ⊥) executing 𝑐 from state 𝜎1 may not terminate. Thus,
      • the sequential statement’s denotation can be defined by composition of binary relations,
        namely J𝑐 1 ; 𝑐 2 K ≜ J𝑐 1 K ◦ J𝑐 2 K; and
      • transformation correctness can be defined by set inclusion, i.e., a transformation T is sound
        iff. ∀𝑐, JT (𝑐)K ⊆ J𝑐K, which allows the transformation result T (𝑐) to have fewer possible
        behaviors than the original program, but no extra behaviors.
In this setting, if a transformation T satisfies T (𝑐 1 ; 𝑐 2 ) = (T (𝑐 1 ); T (𝑐 2 )), then its transformation
correctness is compositional in terms of the composition relation, i.e.,
                 if JT (𝑐 1 )K ⊆ J𝑐 1 K and JT (𝑐 2 )K ⊆ J𝑐 2 K, then JT (𝑐 1 )K ◦ JT (𝑐 2 )K ⊆ J𝑐 1 K ◦ J𝑐 2 K          (1)
This compositional proof style may look unrealistic for verifying real compilation passes, since it
is based on extremely simplified semantic assumptions. We fill the gap between this ideal proof
paradigm and reasonably practical compiler verification by overcoming the following difficulties:
   General refinement. In practice, JT (𝑐)K ⊆ J𝑐K is not general enough for describing all transforma-
tion correctness, especially for transformations that may alter how states are represented. In such
cases, a general behavior refinement, based on a state-matching relation 𝑅 (⊆ state𝑠 × state𝑡 ), is
required. We define JT (𝑐)K ⊑𝑅 J𝑐K as follows (we omit the subscript 𝑅 when there is no ambiguity):
               ∀𝜎𝑠 𝜎𝑡 𝜎𝑡′, (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅 ⇒ (𝜎𝑡 , 𝜎𝑡′ ) ∈ JT (𝑐)K ⇒ ∃𝜎𝑠′, (𝜎𝑠′, 𝜎𝑡′ ) ∈ 𝑅 ∧ (𝜎𝑠 , 𝜎𝑠′ ) ∈ J𝑐K            (2)
This formula is illustrated by Fig. 1c, and obviously JT (𝑐)K ⊆ J𝑐K is the special case when 𝑅 is
defined as the equal relation “=”, as illustrated in Fig. 1b. We find that such a general definition of
refinement is also compositional w.r.t. common semantic combinators like Formula (1).
   More program features. Realistic programming languages involve a richer set of features that
must be accounted for in the semantics. To this end, we use input-output event traces to express a
program’s observable behavior as in CompCert, and use separate behavior sets to handle different
styles of control flow for CompCert intermediate languages and especially to describe terminat-
ing, diverging, and aborting behaviors that traditional powerdomains [Plotkin 1976; Smyth 1978;
Winskel 1985] in domain theory are unable to capture simultaneously4 .
3 state represents state ∪ {⊥}, where ⊥ represents nontermination.
        ⊥
4 That is, semantics of recursion cannot be defined by taking a single Kleene least fixed point.



ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                             5:3


          S1. while 𝑒 do 𝑠 // Clight while loop         T2. block { // Cminor switch
          T1. block {        // Csharpminor loop              block {
                loop {                                          block {
                  block { if 𝑒 then 𝑠 else exit 1;                 switch (𝑒) {
                  } //continue of 𝑠 branches here                     N1: exit 0;
                }                                                     N2: exit 1;
              } //break of 𝑠 branches here                            default: exit 2;
          S2. switch (𝑒) { // Csharpminor switch                   }
                case N1: 𝑠 1 ;                                  }; 𝑡 1 //from 𝑠 1 with exits shifted by 2
                case N2: 𝑠 2 ;                                }; 𝑡 2 //from 𝑠 2 with exits shifted by 1
                default: 𝑠;                                 }; 𝑡 //from 𝑠 with exits unchanged
              }

Fig. 2. Clight loop S1 and Csharpminor switch S2 are respectively translated to Csharpminor loop T1 and
Cminor switch T2, where (exit 𝑛) will prematurely terminate (𝑛 + 1) layers of nested blocks. In program T2,
the exiting number in 𝑠𝑖 is properly shifted according to the level of blocks it resides in. In Cminor, unlike
Csharpminor, the branches of switch statements cannot be general statements but must be exit statements.


   Semantics of open modules and semantic linking. A practical compiler should support separate
compilation, i.e., different modules or different source code files can be compiled separately first
and linked in the end. The correctness of separate compilation is an important research problem
which a series of extensions to CompCert such as CompComp [Stewart et al. 2015], CompCertM
[Song et al. 2020], CompCertO [Koenig and Shao 2021] and recent work by Zhang et al. [2024]
tries to tackle. This article proposes a denotational semantics for open modules, defines a novel
semantic linking operator, and shows that this operator preserves the general behavior refinement,
analogous to how the composition preserves the set inclusion shown in Formula (1).
   Many compilation passes in CompCert are recursively defined transformations, such as, as
shown in Fig. 2, the transformation of while, do .. while and for loops into infinite loops with
appropriate block and exit constructs, along with statements break and continue into early
exits, and the transformation of multi-branch switch from Csharpminor into a Cminor switch
wrapped by the statements associated with the various branches in a cascade of nested Cminor
blocks. In our framework, the denotational semantics of a statement is recursively derived from
its substructures with certain semantic operators (e.g., the composition “◦”). For example, the
denotation of a sequential statement (𝑐 1 ; 𝑐 2 ) is defined by the denotations of 𝑐 1 and 𝑐 2 , and the
denotation of a loop statement is defined based on its loop body’s. When verifying the correctness
of statement transformations, we employ induction on the syntax of source program statements,
which produces proof obligations asserting that for each syntactic component, its corresponding
semantic operators preserve transformation correctness. As illustrated by (1), such obligations
should be easy to prove by the favorable algebraic properties inherent in denotational semantics.
   We have successfully applied our denotation-based verification framework to the front-end of
CompCert and typical optimizations on simple prototypes of imperative languages. When building
this framework, we discover that the following two algebraic structures are highly beneficial.
    • Denotational semantics can be modeled in an extended Kleene Algebra with Tests (KAT)
      [Kozen 1997] with operators ∪, ◦, the empty relation ∅ and the identity relation 1 satisfying
      certain axioms (further discussed in §3). Thus, the properties of programs can be carried out
      in a purely equational subsystem using the axioms of Kleene Algebras.
    • On top of extended KATs, we propose a notion of refinement algebra to unify various behavior
      refinements and make refinement proofs structured and automated. That is, automated proof

     ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:4                                                                                                   Z. Cheng et al.


                                    Toy languages                           CompCert front-end
       Languages
                       WHILE         PCALL     GOTO           CFG     Clight Csharpminor Cminor
       Section          §3.1       §4.1 ∼ §4.3  §4.4           §5         §3.2 ∼ §3.3 and §6

                        Fig. 3. Formal languages for demonstrating our methodology.


       tactics are designed to mechanically verify behavior refinement for composition statements
       (such as if-branch, loop, and sequential statements) and module-level compositionality.
   Main contribution. This article proposes a novel framework to formalize the denotational se-
mantics of first-order imperative languages, and we apply such framework to the compositional
verification of realistic compilers. Our denotation-based framework is featured with (i) precise de-
notational semantics for full open modules and realistic languages (putting denotational semantics
into practical scenarios and achieving better compositionality), (ii) a novel notion of refinement
algebra for behavior refinement abstraction and proof automation, and (iii) successful application
to the front-end of CompCert and typical optimizations on first-order imperative programs. The
refinement algebra integrates well with Kleene Algebra with Tests (KAT), and works for both the
verification of partial program compilation and module-level compositionality. All results of this
article are formalized in Rocq (formerly Coq). Compared to previous extensions of CompCert, such
as CompComp and CompCertM, our Rocq formalization is notably more lightweight in terms of
lines of code.
   Our presentation starts with smaller toy languages and later extends the ideas to the more
elaborate CompCert front-end languages. The languages used in each section are shown in Fig. 3.
   Structure of the paper. We briefly introduce CompCert and the challenges we are facing in §2. We
then use the WHILE language to illustrate the basic denotational semantics on KATs and extend it
to realistic languages in §3. We further take procedure calls into account and build the semantics of
open modules and a novel semantic linking operator via the PCALL languages in §4. We introduce
the denotation of unstructured branches using the GOTO language in §4.4 and that of control flow
graphs (CFG) with the CFG language in §5. We present the full semantics of Clight in §6.
   The highlight of this article is developing novel refinement algebras to establish behavior refine-
ment between denotations in §7, and applying our theoretical framework to verify the CompCert
front-end, a classical CFG generation, and optimizations on toy languages in §8. We further compare
our approach with typical related efforts in §9, followed by code evaluations in §10 and further
discussion in §11. Finally, we discuss related work in §12 and conclude the article in §13.

2     Background and Challenges of Compiler Verification
2.1    CompCert Verification Framework
The small-step semantics of a language L in CompCert is modeled as a tuple (I, ↩→, F ) where
I denotes the set of initial states loaded by a function Load: L → state, F denotes the set of final
states of program execution, and ↩→⊆ state × trace × state is a stepping relation. For each single
                                                  𝜏
step of execution (𝜎, 𝜏, 𝜎 ′ ) ∈↩→ (written as 𝜎 ↩→ 𝜎 ′ ), state 𝜎 transitions to state 𝜎 ′ with a finite
sequence of triggered observable events (typically, I/O and other system calls). An observable
behavior is defined as a (finite or infinite) trace of observable events occurring in a sequence of
execution steps. The CompCert compilation correctness theorem ensures that the target program
preserves the observable behavior of the source program and does not introduce any new behavior
that wasn’t present in the source program. Such compilation correctness is justified by a backward
simulation. We say a program 𝑃𝑠 is backward simulated by a program 𝑃𝑡 if given a state matching

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                                     5:5


relation 𝑅, their initial states Load (𝑃𝑠 ) and Load (𝑃𝑡 ) is related by 𝑅, and (simplified for presentation)
                                                           𝜏                                      𝜏
                 ∀𝜎𝑠 𝜎𝑡 𝜎𝑡′ 𝜏, (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅 ⇒ 𝜎𝑡 ↩→ 𝜎𝑡′ ⇒ ∃𝜎𝑠′, (𝜎𝑠′, 𝜎𝑡′ ) ∈ 𝑅 ∧ 𝜎𝑠 ↩→∗𝜎𝑠′
It reads that for every step taken by the compiled target program, there exists zero or more consistent
steps in the source program, such that the two programs remain in a related state. Despite the
general success of operational semantics in CompCert, the simulation technique and small-step
based proofs of CompCert face the following inconvenience compared to denotational semantics.

                      y = f(x)                                 print(x)         y = f(x)              print(y)
      𝜎𝑠                                     𝜎𝑠′       𝜎𝑠                 𝜎𝑠′              𝜎𝑠′′                  𝜎𝑠′′′

     𝑅                                             𝑅   𝑅            𝑅                𝑅                               𝑅

      𝜎𝑡                                     𝜎𝑡′       𝜎𝑡                 𝜎𝑡′              𝜎𝑡′′                  𝜎𝑡′′′
                      y = g(x)                                 y = g(x)         print(x)              print(y)

      (a) The backward simulation for f and g              (b) The backward simulation for whole programs

                          Fig. 4. Backward simulation diagrams used in CompCert.


  Intermediate correspondence. Consider the following transformation, where x and y are temporary
variables, f and g are pure internal functions, which return identical results for the same input and
generate no observable events, and the built-in function print outputs the value of its argument.
                            Source program 𝑆 : print(x); y = f(x); print(y);
                            Transformed to 𝑇 : y = g(x); print(x); print(y);
 Suppose that a (backward) simulation between f and g has been established in advance, where
nontrivial intermediate correspondence may be constructed by a series of proof steps. In CompCert,
however, these proof steps cannot be directly reused to establish simulation relations between the
larger programs 𝑆 and 𝑇 , since the rearrangement of print statements introduces observable events
that alter the simulation structure, as illustrated in Fig. 4. Consequently, subroutine equivalence
proofs must be revisited when establishing correspondence of larger programs. In comparison,
if using denotational semantics, the established semantic equivalence between f and g could
potentially be reused in proving the equivalence of the programs 𝑆 and 𝑇 .
  Nondeterminism correspondence. More importantly, it is hard to use CompCert’s (backward)
simulation techniques to verify transformations where (demonic) nondeterminism straddles event
synchronization and thereby impacts later observable behavior. Consider the following example:
                      Source program: choice(x = 0, x = 1); print(0); print(x);
                      Transformed to:       print(0); choice(x = 0, x = 1); print(x);

where the statement “choice” nondeterministically chooses to execute either “x = 0” or “x = 1”.
The transformation swaps the first two statements while preserving the set of possible observable
behaviors (i.e., traces 00 and 01). Intuitively, the denotational semantics of the programs before
and after the transformation are equivalent. However, establishing this equivalence is difficult
using CompCert’s current simulation theories. Because CompCert simulation theories constrain
a one-to-one match of observable events (i.e., strict event synchronization), the observable event
produced by the first step of the target program must correspond to the observable event produced
by the first two steps of the source program. At this point, the source program must first choose

     ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:6                                                                                                   Z. Cheng et al.


to execute either “x = 0” or “x = 1”, and whichever is chosen, the subsequent choice in the target
program may differ, potentially leading to inconsistent results for “print(x)” in the end.

   Program-state correspondence. CompCert models the semantics of high-level languages using
mixed program states integrating continuations (to represent control flow and nested calls) together
with the definitions of statements and functions currently under execution. As a result, establishing
correspondences between program states necessarily involves all components of these enriched
states. In comparison, the standard denotational semantics of a statement 𝑐 with procedure calls (as
presented, for example, in Winskel’s textbook [Winskel 1993]) interprets 𝑐 as a function mapping
the behaviors of callees to the overall behavior of 𝑐. This naturally leads to a formulation of
transformation correctness: a transformation T is correct if it preserves such semantic mappings.

      J𝑐K : mapping from “behaviors of source callee procedures” to “behavior of 𝑐”
      JT (𝑐)K : mapping from “behaviors of compiled callee procedures” to “behavior of T (𝑐)”
      T is correct iff for any callee behaviors 𝜒𝑠 𝜒𝑡 , if 𝜒𝑡 ⊑ 𝜒𝑠 , then JT (𝑐)K( 𝜒𝑡 ) ⊑ J𝑐K( 𝜒𝑠 )

This formalization benefits from two aspects: (i) we can simplify the definition of program states
and their correspondence, and further decompose the refinement proof into smaller and simpler
conclusions by splitting the original correspondence of CompCert into static environment corre-
spondence and dynamic memory correspondence; (ii) we can define semantic linking operators by
taking semantic fixed points, and we further find that the equivalence between semantic linking
and syntactic linking is reduced to the concise Bekić’s theorem [Bekić 1984] about fixed points.
   To sum up, the above statements demonstrate the potential benefits of denotational semantics
for composing proofs, handling nondeterministic correspondence, and lightening program-state
correspondence. Moreover, we also observe that recent research in simulation theories, such as
FreeSim [Cho et al. 2023], as well as more advanced approaches like prophecy variables [Abadi
and Lamport 1991; Lynch and Vaandrager 1995], proposes mechanisms intended to mitigate these
challenges. Some of these approaches, such as FreeSim, have been formalized and partially integrated
into existing proof frameworks, and some of them have not yet been formalized and used for realistic
compiler verification like prophecy variables. Particularly, they face their own inherent difficulties
in tackling the issues discussed above. We will examine these related works in greater detail in §12.

2.2    Denotational Semantics: Achievements and Challenges
Denotational semantics enjoys good compositionality, meaning that the semantics of a syntactic
construct can be systematically derived from the semantics of its substructures using semantic
operators. A central concern in this approach is handling loops and recursion effectively. Existing
research on deterministic programs demonstrates that the semantics of recursive constructs can be
defined on the basis of domain theory [Scott 1970; Scott and Strachey 1971] or Kleene Algebras
[Kozen 1997]. In domain theory, the semantics of programs are modeled as elements of domains
(typically CPOs), and the key tool in domain theory is the Kleene fixed-point theorem where
recursive constructs are given meaning by finding the least fixed point of a continuous function.
The concepts of CPOs, continuous functions and Kleene fixed points are outlined as follows.

   Definition 2.1 (Complete Partial Order). A Directed Complete Partial Order (DCPO) is a partially
ordered set 𝑃 such that every directed subset 𝐷 ⊆ 𝑃 has a supremum (i.e. sup 𝐷) in 𝑃. A subset 𝐷 of
𝑃 is directed if it is nonempty and for any elements 𝑥, 𝑦 ∈ 𝐷, there exists an element 𝑧 ∈ 𝐷 such
that 𝑥 ≤ 𝑧 and 𝑦 ≤ 𝑧. A DCPO with a least element ⊥ is usually called a pointed DCPO.

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                             5:7


  Definition 2.2 (Scott-Continuous Function). A function 𝑓 between two DCPOs is called Scott-
continuous if it preserves the directed suprema, i.e., for any directed subset 𝐷 of the domain,
                                                  𝑓 (sup 𝐷) = sup 𝑓 (𝐷)
  Theorem 2.3 (Kleene fixed point). Suppose (𝐴, ≤𝐴 ) is a directed-complete partial order (DCPO)
with a least element ⊥, and let 𝐹 : 𝐴 → 𝐴 be a Scott-continuous (and therefore monotone) function.
Then 𝐹 has a least fixed point 𝜇𝐹 = sup({𝐹 𝑛 (⊥) | 𝑛 ∈ N}), where sup means taking the supremum.
   Kleene algebras are algebraic structures with operators ◦, ∪, ∗ , ∅, 1 that satisfy certain axioms.
Typically, the family of binary relations with operators ∪, ◦, the empty relation ∅, the identity
relation 1 and the reflexive transitive closure ∗ constitute a Kleene Algebra, where iteration is
captured algebraically through the star operator. The following example shows the definition of
the textbook denotational semantics on a toy language, by domain theory or by Kleene Algebras.
   Example 2.4. Consider a simple deterministic and type-safe toy language whose syntactic con-
structs (extremely simplified for presentation purpose) and semantics can be defined as follows.
      𝑐 ≜ skip | 𝑐 1 ; 𝑐 2 | if 𝑏 then 𝑐 1 else 𝑐 2 | while 𝑏 do 𝑐
      JskipK ≜ 1       J𝑐 1 ; 𝑐 2 K ≜ J𝑐 1 K ◦ J𝑐 2 K   test(𝑋 ) ≜ {(𝜎, 𝜎) | 𝜎 ∈ 𝑋 }, for 𝑋 ⊆ state
      Jif 𝑏 then 𝑐 1 else 𝑐 2 K ≜ test(J𝑏K.(tts)) ◦ J𝑐 1 K ∪ test(J𝑏K.(ffs)) ◦ J𝑐 2 K
                                                                              
      Jwhile 𝑏 do 𝑐K ≜ 𝜇𝑥 .test(J𝑏K.(ffs)) ∪ test(J𝑏K.(tts)) ◦ J𝑐K ◦ 𝑥 , by domain theory
                                                  ∗
      Jwhile 𝑏 do 𝑐K ≜ test(J𝑏K.(tts)) ◦ J𝑐K ◦ test(J𝑏K.(ffs)), by Kleene Algebras
      where J𝑏K.(tts) ≜ {𝜎 | 𝜎 (𝑏) = T}, J𝑏K.(ffs) ≜ {𝜎 | 𝜎 (𝑏) = F}, 1 = {(𝜎, 𝜎) | 𝜎 ∈ state}
   Although domain theory and Kleene algebras have a long research history and a strong mathe-
matical foundation, it remains challenging to precisely characterize the full semantics of practical
programming languages, which may exhibit termination, divergence, or even abortion. We may
naively construct a domain by treating abortion as the least element in the partial order and
regarding normal termination and divergence as incomparable (i.e., without any ordering between
them). However, in a nondeterministic program, a state may nondeterministically transition to
either a terminating or a diverging state. If these outcomes are incomparable, the semantics can-
not represent their “join” (supremum) in a manner consistent with the domain’s ordering. This
inconsistency prevents the definition of a continuous function required by the Kleene fixed-point
theorem. In order to handle nondeterministic and possible nonterminating behaviors5 , computer
scientists proposed three classical power domain constructions, known as Hoare powerdomain,
Smyth powerdomain [Smyth 1978], and Plotkin powerdomain [Plotkin 1976], in the 1970s. Power
domains in our context are constructed from a flat domain (𝐷, ⩽𝐷 ), which may stand for possible
results of executions. Suppose that for any 𝑥 and 𝑦 in 𝐷,
                                              𝑥 ⩽𝐷 𝑦 ⇔ (𝑥 = ⊥ ∨ 𝑥 = 𝑦)
a power domain of 𝐷, written as M (𝐷), involves the subsets of the ground domain 𝐷 and a new
partial order ⊑, such that (M (𝐷), ⊑) forms a CPO and one can take a fixed point over it. For any 𝑋
and 𝑌 in M (𝐷), there are generally three natural ways to construct the new ordering:
                                        𝑋 ⊑0 𝑌 ⇔ ∀𝑥 ∈ 𝑋, ∃𝑦 ∈ 𝑌 , 𝑥 ⩽𝐷 𝑦
                                        𝑋 ⊑1 𝑌 ⇔ ∀𝑦 ∈ 𝑌 , ∃𝑥 ∈ 𝑋, 𝑥 ⩽𝐷 𝑦
                                        𝑋 ⊑2 𝑌 ⇔ 𝑋 ⊑0 𝑌 ∧ 𝑋 ⊑1 𝑌
5 Unless otherwise specified, nondeterminism means demonic nondeterminism.



     ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:8                                                                                                      Z. Cheng et al.


   The Hoare powerdomain. The Hoare powerdomain is established with the first ordering ⊑0
meaning that everything 𝑋 can do, 𝑌 can do better. However, this ordering is just a preorder but not
a partial order since it fails antisymmetry. The issue is solved by defining an equivalence relation ≃0
(𝑋 ≃0 𝑌 iff 𝑋 ⊑0 𝑌 and 𝑌 ⊑0 𝑋 ) and restricting that every set 𝑋 in M (𝐷) is a downset. Specifically,
                𝑋 is a downset iff 𝑋 ≃0 ↓ 𝑋, where ↓ 𝑋 ≜ {𝑥 0 ∈ 𝐷 | ∃𝑥 ∈ 𝑋, 𝑥 0 ⩽𝐷 𝑥 }
Consequently, with the Hoare powerdomain, one gets an angelic semantics for nondeterminism
since the downsets always include the least element ⊥. That means, any program that could either
terminate or diverge will have the same meaning with its terminating behavior. For instance, given
the following four programs, program 1 and 3 will have the same semantics under this power
domain (where“x = ?” in program 4 means “nondeterministically set x to any natural number”).
                 1. skip                                             4. while (y == 2 | | x > 0) do
                 2. while true do skip                                   if (y == 2) then y = 1; x = ?
                 3. choice(while true do skip, skip)                     else x = x − 1

  The Smyth powerdomain. The Smyth powerdomain is obtained with the preorder ⊑1 , which says
that everything 𝑌 can do is approximated by some behavior of 𝑋 . Since this ordering is still a
preorder but not a partial order, the Smyth powerdomain defines the preorder’s natural equivalence
≃1 (𝑋 ≃1 𝑌 iff 𝑋 ⊑1 𝑌 and 𝑌 ⊑1 𝑋 ) and constrains every element 𝑋 in M (𝐷) to be an upset, i.e.,

                 𝑋 is an upset iff 𝑋 ≃1 ↑ 𝑋, where ↑ 𝑋 ≜ {𝑥 0 ∈ 𝐷 | ∃𝑥 ∈ 𝑋, 𝑥 ⩽𝐷 𝑥 0 }
As a result, one will achieve a demonic semantics in the sense that any program that can diverge
has the semantics ↑ {⊥} = 𝐷. Thus, for instance, programs 2 and 3 will have the same semantics.
  The Plotkin powerdomain. The Plotkin powerdomain uses the well-known Egli-Milner ordering
⊑2 , with which every set 𝑋 in M (𝐷) is restricted to be equivalent with its convex closure:
                            𝑐𝑜𝑛𝑣 (𝑋 ) ≜ {𝑥 1 ∈ 𝐷 | ∃𝑥 0, 𝑥 2 ∈ 𝑋, 𝑥 0 ⩽𝐷 𝑥 1 ⩽𝐷 𝑥 2 }
By this powerdomain, all the first three programs will have different meanings as one would expect.
However, some constructs like program 4 that can produce infinitely many different results and yet
be certain to terminate, i.e., unbounded nondeterminism, are excluded (see Back [1983] for details).
  To sum up, power domains often fail to capture the full range of possible program outcomes.
Such inability is known as an intrinsic defect of domain theory.
   Park’s approach. Park [1979] proposed an alternative method to characterize the possible non-
terminating behavior of nondeterministic programs, by introducing an additional set to capture
nonterminating behaviors. However, when observable events are considered, it is still challenging
to explicitly distinguish reactive divergence and silent divergence for realistic compiler verification.
   In a word, a notable gap exists between denotational semantics and realistic programming lan-
guages. Additionally, practical programs often include structured (e.g., break, continue) and even
unstructured branches (e.g., goto), which may prematurely terminate the execution of subsequent
statements and hence disrupt the elegant property shown in Formula (1). Precisely capturing the
full meaning of realistic programs while still keeping good compositionality turns out to be a big
challenge. We show the solution of this problem in §3 and then extend it to open modules in §4.

3     Denotational Semantics of Statements (No Procedure Calls)
3.1    The Formal Framework for Defining Denotations
Our solution is to separately define different program behaviors of interest using different sets,
with each behavior set defined by corresponding semantic operators in the form of an extended

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                                                5:9


Kleene Algebra with Tests (KAT). This manipulation is somewhat similar to Park’s approach. In
comparison, we design new mechanisms to handle divergence with event traces, capture the full
meaning of realistic programs, and especially concisely formalize them in Rocq.
  Consider a type-safe toy language WHILE whose set of statements Com, ranged over by 𝑐, is
parameterized on the set of Boolean expressions Exp ranged over by 𝑏 (no side effects):
              𝑐 ≜ skip | 𝑎𝑡𝑜𝑚 | choice(𝑐 1, 𝑐 2 ) | 𝑐 1 ; 𝑐 2 | if 𝑏 then 𝑐 1 else 𝑐 2 | while 𝑏 do 𝑐
Nondeterminism can be introduced either by atomic statements (ranged over by 𝑎𝑡𝑜𝑚) like nonde-
terministic assignments or by choice statements that unpredictably choose 𝑐 1 or 𝑐 2 to execute. We
formalize the denotation of statements and Boolean expressions with the following signature.
    Record CDenote: Type := {
       nrm: state → state → Prop;                      (* nrm ⊆ state × state *)
       dvg: state → Prop                               (* dvg ⊆ state *)
    }.
    Record BDenote: Type := {
       tts: state → Prop;                              (* tts ⊆ state *)
       ffs: state → Prop                               (* ffs ⊆ state *)
    }.

Specifically, (𝜎1, 𝜎2 ) ∈ J𝑐K.( nrm) iff executing 𝑐 from initial state 𝜎1 could terminate on state 𝜎2 , and
𝜎 ∈ J𝑐K.( dvg) iff executing 𝑐 from 𝜎 could diverge. An element 𝜎 ∈ J𝑏K.(tts) iff state 𝜎 satisfies 𝑏,
and 𝜎 ∈ J𝑏K.(ffs) iff state 𝜎 does not satisfy 𝑏. We can use set operators (like union) and relation
operators (like composition) to define program semantics as follows.
      JskipK.( nrm) ≜ 1 JskipK.( dvg) ≜ ∅                        Jchoice(𝑐 1, 𝑐 2 )K.( nrm) ≜ J𝑐 1 K.( nrm) ∪ J𝑐 2 K.( nrm)
      J𝑐 1 ; 𝑐 2 K.( nrm) ≜ J𝑐 1 K.( nrm) ◦ J𝑐 2 K.( nrm)        Jchoice(𝑐 1, 𝑐 2 )K.( dvg) ≜ J𝑐 1 K.( dvg) ∪ J𝑐 2 K.( dvg)
      Jif 𝑏 then 𝑐 1 else 𝑐 2 K.( nrm) ≜ test(J𝑏K.(tts)) ◦ J𝑐 1 K.( nrm) ∪ test(J𝑏K.(ffs)) ◦ J𝑐 2 K.( nrm)
                                                                 ∗
      Jwhile 𝑏 do 𝑐K.( nrm) ≜ test(J𝑏K.(tts)) ◦ J𝑐K.( nrm) ◦ test(J𝑏K.(ffs)),
        where      test(𝑋 ) ≜ {(𝜎, 𝜎) | 𝜎 ∈ 𝑋 }, for 𝑋 ⊆ state                                  identity relation on 𝑋
                   1 ≜ {(𝜎, 𝜎) | 𝜎 ∈ state}                                                 identity relation on state
                   𝑅 ∗ ≜ 1 ∪ 𝑅 ∪ (𝑅 ◦ 𝑅) ∪ · · · ∪ 𝑅𝑛 ∪ · · ·                             reflexive transitive closure
                   𝑅 + ≜ 𝑅 ∪ (𝑅 ◦ 𝑅) ∪ · · · ∪ 𝑅𝑛 ∪ · · ·                                             transitive closure
                     ∞
                   𝑅 ≜ 𝑅 ◦𝑅 ◦𝑅 ◦···                                                infinitely iterated composition6
As is well known, the family of binary relations with operators ∪, ◦, the empty relation ∅, the
identity relation 1 and the reflexive transitive closure ∗ constitute a Kleene Algebra. Moreover, if
we overload the “◦” operator as follows,

             𝑅1 ◦ 𝑅2 ≜ {(𝜎1, 𝜎3 ) | ∃𝜎2, (𝜎1, 𝜎2 ) ∈ 𝑅1 ∧ (𝜎2, 𝜎3 ) ∈ 𝑅2 }                                   original
             𝑅 ◦ 𝑋 ≜ {𝜎1 | ∃𝜎2, (𝜎1, 𝜎2 ) ∈ 𝑅 ∧ 𝜎2 ∈ 𝑋 }                                                 overloaded
these operators form a typed Kleene Algebra [Kozen 1998] with two base types. The diverging
behavior of sequential, if, and while statements can then be formalized as follows.
                                                                        
    J𝑐 1 ; 𝑐 2 K.( dvg) ≜ J𝑐 1 K.( dvg) ∪ J𝑐 1 K.( nrm) ◦ J𝑐 2 K.( dvg)
                                                                                                        
    Jif 𝑏 then 𝑐 1 else 𝑐 2 K.( dvg) ≜ test(J𝑏K.(tts)) ◦ J𝑐 1 K.( dvg) ∪ test(J𝑏K.(ffs)) ◦ J𝑐 2 K.( dvg)
6 Formally, an element 𝜎           ∞ iff ∃𝜎 ...𝜎 ..., s.t. ∀𝑖, (𝜎 , 𝜎
                           0 ∈ 𝑅           1    𝑛                𝑖 𝑖+1 ) ∈ 𝑅, where 𝜎0 𝜎1 ...𝜎𝑛 ... is an infinite sequence of states.


     ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:10                                                                                                  Z. Cheng et al.

                                                                                                
       Jwhile 𝑏 do 𝑐K.( dvg) ≜ (test(J𝑏K.(tts)) ◦ J𝑐K.( nrm)) ∗ ◦ (test(J𝑏K.(tts)) ◦ J𝑐K.( dvg)) ∪
                                                            ∞
                               test(J𝑏K.(tts)) ◦ J𝑐K.( nrm)
The interesting case is that the while statement diverges if and only if either the loop body 𝑐
diverges after a finite number of normally executing 𝑐, or 𝑐 is executed an infinite number of times.
   The above style of modeling denotational semantics based on a typed Kleene Algebra can be
naturally scaled to realistic settings by extended denotations and redefined operators. In CompCert,
the behavior of a C program encompasses not only state transitions but also the observable events
(I/O and other system calls) triggered during execution. Therefore, we can formalize the denotation
of C-like program statements with the following signature, where trace is the set of all finite
sequences of observable events, and itrace the set of all infinite sequences of observable events.
       Record Denote: Type := {
          nrm: state → trace → state → Prop;    (* nrm ⊆ state × trace × state *)
          ...
          err: state → trace → Prop;            (* err ⊆ state × trace      *)
          fin_dvg: state → trace → Prop;        (* fin_dvg ⊆ state × trace *)
          inf_dvg: state → itrace → Prop        (* inf_dvg ⊆ state × itrace *)
       }.

Specifically, the terminating behavior here is extended to a ternary relation which additionally
records the event trace generated during execution. Diverging behavior is divided into finite and
infinite parts for distinguishing behaviors with finite events and infinite events. In addition, we use a
set err to capture the aborting behavior of programs. We then redefine operators ◦, test, and 1 (and
therefore the operator for reflexive transitive closure) as follows, where 𝑅 ⊆ state × trace × state,
𝑌 ⊆ state × ( trace ∪ itrace), “nil” is the empty sequence and “·” is the concatenation of sequences.
            1 ≜ {(𝜎, nil, 𝜎) | 𝜎 ∈ state}          test(𝑋 ) ≜ {(𝜎, nil, 𝜎) | 𝜎 ∈ 𝑋 }, for 𝑋 ⊆ state
            𝑅 ◦ 𝑌 ≜ {(𝜎1, 𝜏) | ∃𝜎2 𝜏1 𝜏2, (𝜎1, 𝜏1, 𝜎2 ) ∈ 𝑅 ∧ (𝜎2, 𝜏2 ) ∈ 𝑌 ∧ 𝜏 = 𝜏1 · 𝜏2 }
            𝑅1 ◦ 𝑅2 ≜ {(𝜎1, 𝜏, 𝜎3 ) | ∃𝜎2 𝜏1 𝜏2, (𝜎1, 𝜏1, 𝜎2 ) ∈ 𝑅1 ∧ (𝜎2, 𝜏2, 𝜎3 ) ∈ 𝑅2 ∧ 𝜏 = 𝜏1 · 𝜏2 }
   In summary, we use various behavior sets to define different behaviors of interest with typed op-
erators, thus solving the limitations of traditional powerdomains in compiler verification scenarios.
In our implementation, these sets operators are provided by a Rocq set library [Cao et al. 2023].
Besides, we address two additional challenges for practical languages: supporting various control
flow constructs (in §3.2) and defining program divergence in the presence of event traces (in §3.3).

3.2      Semantics of Control Flow Constructs
For handling different control flow statements like break and continue in Clight, or block and
exit in Csharpminor, we add corresponding fields of sets to the denotation record.
  Clight. The Clight language provides control flow constructs including break, continue, and
return statements to prematurely terminate the normal execution of statements. To capture the
behavior of these program constructs, we add the following sets to Denote.
       brk: state → trace → state → Prop;               (* brk ⊆ state × trace × state *)
       ctn: state → trace → state → Prop;               (* ctn ⊆ state × trace × state *)
       rtn: state → trace → state → val → Prop.         (* rtn ⊆ state × trace × state × val *)

These sets represent that for any element (𝜎0, 𝜏, 𝜎1 ) in J𝑠K.(brk) or J𝑠K.(ctn), the execution of Clight
statement 𝑠 from 𝜎0 could eventually reach state 𝜎1 and then exit because of a break or continue
statement, producing a sequence of observable events 𝜏. In other words, once a break or continue

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                             5:11


statement is encountered, the execution will end prematurely, and the corresponding set brk or ctn
records how it ends. Therefore, we formalize such semantics as follows (selectively listed).
                   JbreakK.(brk) ≜ 1, and other fields are assigned the empty set.
                   JcontinueK.(ctn) ≜ 1, and other fields are assigned the empty set
                                                                                   
                   J𝑠 1 ; 𝑠 2 K.(brk) ≜ J𝑠 1 K.(brk) ∪ J𝑠 1 K.(nrm) ◦ J𝑠 2 K.(brk)
                                                                                   
                   J𝑠 1 ; 𝑠 2 K.(ctn) ≜ J𝑠 1 K.(ctn) ∪ J𝑠 1 K.(nrm) ◦ J𝑠 2 K.(ctn)
The semantics of exiting by a return statement can be defined similarly since the rtn set has a
similar meaning but additionally with a return value (where val is the set of values ranging over
integers, floats, pointers, as well as an undefined value Vundef). Clight uses one special loop (loop
𝑠 1 𝑠 2 ) to encode all three kinds of C loops. Its semantics is to repeatedly and sequentially execute
statements 𝑠 1 and 𝑠 2 until a certain break or return statement, and a “continue jump” in 𝑠 1 will
branch to 𝑠 2 . Therefore, the for statement of C language for example can be defined as:
                                                                                           
                   for(𝑠 1 ; 𝑏; 𝑠 2 ) {𝑠 3 } ≜ 𝑠 1 ; loop (if 𝑏 then skip else break); 𝑠 3 𝑠 2
We then formalize the terminating behavior of Clight loops as follows, where 𝑁 1 denotes the
behavior that the loop body 𝑠 1 either ends normally or prematurely due to a continue statement in
𝑠 1 , and 𝑁 12 denotes the behavior of a “sequential” execution of loop bodies 𝑠 1 and then 𝑠 2 .
                        𝑁 1 = J𝑠 1 K.(nrm) ∪ J𝑠 1 K.(ctn)        𝑁 12 = 𝑁 1 ◦ J𝑠 2 K.(nrm)                        (3)
                                                                                                  
                        Jloop 𝑠 1 𝑠 2 K.(nrm) ≜ 𝑁 12
                                                  ∗
                                                     ◦      J𝑠 1 K.(brk) ∪ (𝑁 1 ◦ J𝑠 2 K.(brk))                   (4)
   Csharpminor. The control flow of Csharpminor is structured with the block and exit statement.
For instance, the execution of statement (block { block { 𝑢 1 ; exit(1)}; 𝑢 2 }; 𝑢 3 ) is equivalent to the
execution of (𝑢 1 ; 𝑢 3 ) since the statement exit(𝑛) prematurely terminates the execution of the (𝑛+1)
layers of nested block statements. We then use a function mapping from natural numbers to
relations to capture this behavior, so that an element (𝜎0, 𝜏, 𝜎1 ) ∈ J𝑢K.(blk)𝑛 if and only if executing
the Csharpminor statement 𝑢 from 𝜎0 could terminate at 𝜎1 , and 𝑛 records the layers of nested
blocks to exit. Thus, the denotation of Csharpminor statements J𝑢K satisfies the following equations.
            Jblock{𝑢}K.(nrm) ≜ J𝑢K.(nrm) ∪ J𝑢K.(blk)0                  Jblock{𝑢}K.(blk)𝑛 ≜ J𝑢K.(blk)𝑛+1
            Jexit(𝑛 0 )K.(blk)𝑛 ≜ 1, if 𝑛 0 = 𝑛                      Jexit(𝑛 0 )K.(blk)𝑛 ≜ ∅, if 𝑛 0 ≠ 𝑛
                                                                               
            J𝑢 1 ; 𝑢 2 K.(blk)𝑛 ≜ J𝑢 1 K.(blk)𝑛 ∪ J𝑢 1 K.(nrm) ◦ J𝑢 2 K.(blk)𝑛
The loop structure of Csharpminor is an infinite loop (Sloop 𝑢), whose behavior is to execute the
loop body 𝑢 repeatedly until a certain early exit. The semantics is defined as follows.
                   JSloop 𝑢K.(nrm) ≜ ∅            JSloop 𝑢K.(blk)𝑛 ≜ J𝑢K.(nrm)∗ ◦ J𝑢K.(blk)𝑛

3.3    Divergence with Event Trace
Handling divergence with event traces is more involved. Previous research indicates that simulations
between semantics have to address the classic stuttering problem [Leroy 2009]. Therefore, unlike
defining divergence directly using 𝑅 ∞ in simple languages, we must explicitly consider whether
the event trace in program execution is empty or not. We demand that 𝑅 ∞ is only defined if either
all traces in 𝑅 are nonempty (i.e., nonsilent), or all traces in 𝑅 are empty (i.e., silent). To this end, we
use silent operator △ and nonsilent operator ▲ to explicitly filter silent and nonsilent event traces
as follows, where 𝑅 ⊆ state × trace × state and 𝑌 ⊆ state × ( trace ∪ itrace).
                                  ▲𝑅 ≜ {(𝜎, 𝜏, 𝜎 ′ ) | (𝜎, 𝜏, 𝜎 ′ ) ∈ 𝑅 ∧ 𝜏 ≠ nil}

      ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:12                                                                                                     Z. Cheng et al.


                                  △𝑅 ≜ {(𝜎, 𝜏, 𝜎 ′ ) | (𝜎, 𝜏, 𝜎 ′ ) ∈ 𝑅 ∧ 𝜏 = nil}
                                  △𝑌 ≜ {(𝜎, 𝜏) | (𝜎, 𝜏) ∈ 𝑌 ∧ 𝜏 = nil}
Recall that J𝑠K.(fin_dvg) and J𝑠K.(inf_dvg) denote diverging behavior with finite and infinite event
traces generated by executing statement 𝑠, respectively. For Clight loops, Jloop 𝑠 1 𝑠 2 K.(fin_dvg)
indicates that after sequentially executing the loop bodies 𝑠 1 and 𝑠 2 a finite number of times, a
Clight loop could silently diverge since 𝑠 1 does, or 𝑠 2 does, or the entire loop itself silently diverges.
Similarly, the nonsilently diverging behavior (i.e, reacting behavior) Jloop 𝑠 1 𝑠 2 K.(inf_dvg) indicates
that after sequentially executing the loop bodies 𝑠 1 and 𝑠 2 a finite number of times, a Clight loop
could nonsilently diverge since 𝑠 1 does, or 𝑠 2 does, or the entire loop itself nonsilently diverges.
They are formalized as follows, where 𝑁 1 and 𝑁 12 are defined by Formula (3).
                                                                                                     
         Jloop 𝑠 1 𝑠 2 K.(fin_dvg) ≜ 𝑁 12
                                       ∗
                                          ◦ J𝑠 1 K.(fin_dvg) ∪ (𝑁 1 ◦ J𝑠 2 K.(fin_dvg)) ∪ (△𝑁 12 ) ∞
                                                         ∗                                          ∞
         Jloop 𝑠 1 𝑠 2 K.(inf_dvg) ≜ (△𝑁 12 ) ∗ ◦ ▲𝑁 12 ◦ (△𝑁 12 ) ∗ ◦ D ∪ (△𝑁 12 ) ∗ ◦ ▲𝑁 12
                                                                    
              where D = J𝑠 1 K.(inf_dvg) ∪ 𝑁 1 ◦ J𝑠 2 K.(inf_dvg)
Remark that D denotes the reacting behavior by the loop body 𝑠 1 or 𝑠 2 , and (△𝑁 12 ) ∗ ◦ ▲𝑁 12 denotes
that one observable behavior must be triggered after silently looping a finite number of times.

4      Denotational Semantics of Procedure Calls
So far, we have shown how to precisely define the denotational semantics of programs with
nondeterministic and nonterminating behaviors without considering procedure calls.
   Another challenge in applying such semantics to realistic compiler verification is how to model
the semantics of open modules and make it compositional, in the sense that the semantics of every
separately compiled module can be linked together and keep behavioral consistency with the
linked semantics of source modules. Our key idea, extended from the standard way of defining
denotational semantics for whole programs with procedure calls, is to define an open module’s
denotation under a semantic “oracle” that describes the terminating behavior of external calls. Then
when linking, the semantics is given by merging the denotation of modules and then taking fixed
points, in which external calls may now be “handled” by one of the linked modules. In this section,
we begin with a simple language for introducing the standard denotational semantics for programs
with procedure calls in §4.1, and then propose a denotational semantics for open modules and a
novel semantic linking operator in §4.2. Finally, their divergence is defined in §4.3.
   For presentation, this section ignores observable events and focuses solely on procedure calls.

4.1     Standard Denotational Semantics of Procedure Calls (Whole Program)
Consider a language, PCALL, defined as follows: a whole program in PCALL consists of a list of
procedures. Each procedure 𝑝, belonging to a set Pdef, is characterized by its procedure name 𝑖𝑑𝑝 , a
list of local variables 𝑥 1 ; ...; 𝑥𝑛 , and its procedure body 𝑐 𝑝 , which is represented as a statement.
    Statements: 𝑐 ≜ skip | 𝑎𝑡𝑜𝑚 | choice(𝑐 1, 𝑐 2 ) | 𝑐 1 ; 𝑐 2 |      Procedures: 𝑝 ≜ (𝑖𝑑𝑝 , 𝑥 1 ; . . . ; 𝑥𝑛 , 𝑐 𝑝 )
            if 𝑏 then 𝑐 1 else 𝑐 2 | while 𝑏 do 𝑐 | call 𝑖𝑑            Whole programs: 𝑃 ≜ 𝑝 1 ; . . . ; 𝑝𝑛
In this toy language, procedure calls have no arguments and no return values. Before defining its
semantics, we partition program states into local and global components: state ≜ lstate × gstate.
Let the symbol 𝑙 range over the set of local states lstate and 𝑔 over the set of global states gstate.
   The standard way [Back 1983; Park 1979] to define the denotational semantics of programs
with procedure calls is parameterizing the denotation of procedures with the behavior of invoked
procedures, and then taking the Kleene fixed point (see Thm. 2.3) on recursive domain equations.

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                             5:13


                                Init                       J𝑐 𝑝 K 𝜒 .(nrm)                       Free
                   𝑝, 𝑔0                      (𝑙 1, 𝑔1 )                     (𝑙 2, 𝑔2 )                 𝑔3

                           Fig. 5. An illustration of the semantic definition of J𝑝K 𝜒 .(nrm).


   Specifically, let ident be the set of procedure names. Consider a semantic oracle 𝜒 (⊆ ident ×
gstate × gstate) such that an element (𝑖𝑑, 𝑔0, 𝑔1 ) ∈ 𝜒 if and only if executing the procedure named 𝑖𝑑
from global state 𝑔0 could normally terminate at global state 𝑔1 . The terminating behavior of PCALL
statements is still a binary relation J𝑐K 𝜒 .(nrm) (⊆ state × state) so that an element (𝜎0, 𝜎1 ) ∈ J𝑐K 𝜒 .(nrm)
if and only if executing statement 𝑐 from state 𝜎0 could terminate at state 𝜎1 , in which the semantics
of procedure calls will be given by 𝜒, i.e.,
                              Jcall 𝑖𝑑K 𝜒 .(nrm) ≜ {((𝑙, 𝑔0 ), (𝑙, 𝑔1 )) | (𝑖𝑑, 𝑔0, 𝑔1 ) ∈ 𝜒 }
Notably, the local state remains unchanged after executing the procedure call. The semantics of
other PCALL statements can refer to the semantic definitions of WHILE statements, for example:
                                     J𝑐 1 ; 𝑐 2 K 𝜒 .(nrm) ≜ J𝑐 1 K 𝜒 .(nrm) ◦ J𝑐 2 K 𝜒 .(nrm)
We further use J𝑝K 𝜒 .(nrm) (⊆ {𝑖𝑑𝑝 } × gstate × gstate) to represent the terminating behavior of the
procedure 𝑝 such that an element (𝑖𝑑𝑝 , 𝑔0, 𝑔1 ) ∈ J𝑝K 𝜒 .(nrm) if and only if executing procedure 𝑝 at
global state 𝑔0 could eventually terminate at global state 𝑔1 . It’s easy to see J𝑝K 𝜒 .(nrm) can be derived
from the semantics of its body J𝑐 𝑝 K 𝜒 .(nrm) as illustrated in Fig. 5, and the formal definition is shown
in Formula (5), where the function Init: Pdef × gstate → state gives the initial local and global state
after allocating local variables for the execution of the procedure body 𝑐 𝑝 , and the function Free:
lstate × gstate → gstate gives the final global state after freeing local addressed variables.
                       (                                                                                 )
                                                         (𝑙 1, 𝑔1 ), (𝑙 2, 𝑔2 ) ∈ J𝑐 𝑝 K 𝜒 .(nrm) ∧
         J𝑝K 𝜒 .(nrm) ≜ (𝑖𝑑𝑝 , 𝑔0, 𝑔3 ) ∃𝑙 1 𝑙 2 𝑔1 𝑔2,                                                     (5)
                                                        (𝑙 1, 𝑔1 ) = Init (𝑝, 𝑔0 ) ∧ 𝑔3 = Free (𝑙 2, 𝑔2 )
Finally, the terminating behavior of the whole program, i.e., J𝑝 1 ; ...; 𝑝𝑛 K.( nrm), can be defined as:
                                                                                               
                      J𝑝 1 ; ...; 𝑝𝑛 K.( nrm) ≜ 𝜇 𝜒 . J𝑝 1 K 𝜒 .(nrm) ∪ · · · ∪ J𝑝𝑛 K 𝜒 .(nrm)          (6)
According to the Kleene fixed point theorem, Formula (6) means that a procedure call could
terminate if and only if there exists a natural number 𝑘 such that the procedure call terminates with
at most 𝑘 layers of nested calls. We proceed to discuss how we extend this approach to support
semantic linking of open modules in §4.2, and how we define the diverging behavior in §4.3.

4.2    Semantics of Open Modules and Semantic Linking
A more realistic program is usually composed of multiple modules (or partial programs), each
of which contains a list of procedures and is compiled individually. We find that the traditional
approach from Back [1983] (which we summarize in §4.1) can be easily extended to this setting
by parameterizing the semantics of open modules with the terminating behavior of external
procedures7 .
4.2.1 Semantics of Open Modules. Formally, we use J𝑀K 𝜒 .(nrm) (⊆ ident × gstate × gstate) to
represent the terminating behavior of an open module. It means that an element (𝑖𝑑, 𝑔0, 𝑔1 ) ∈
J𝑀K 𝜒 .(nrm) if and only if there exists a procedure named 𝑖𝑑 in module 𝑀 and its execution beginning
with global state 𝑔0 could finally terminate at global state 𝑔1 , in which the terminating behavior of
7 External procedures are those not defined in the current module.



      ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:14                                                                                                  Z. Cheng et al.


                            𝜒

                                                     cll. 𝑞   𝑞 ret.          cll. 𝑝 1   𝑝 1 ret.



                           cll. 𝑞      𝑞 ret.   cll. 𝑝 1        𝑝 1 ret.   cll. 𝑝 2        𝑝 2 ret.

                    𝑝1

                                      (a) Semantics of a single procedure 𝑝 1
                            𝜒
                                                     cll. 𝑞   𝑞 ret.          cll. 𝑝 1   𝑝 1 ret.



                           cll. 𝑞      𝑞 ret.   cll. 𝑝 1        𝑝 1 ret.   cll. 𝑝 2        𝑝 2 ret.

                    𝑝1

                                (b) Semantics of module 𝑀 containing procedure 𝑝 1

Fig. 6. Comparison between the semantics of procedures and that of modules. Here raising edges denote
procedure calls (abbr. cll.), falling edges denote procedure returns (abbr. ret.), and the dashed line represents the
behavior of external procedure 𝑞. The shaded areas show that for J𝑝 1 K 𝜒 .(nrm), the behavior of every procedure
call of 𝑝 1 is interpreted by 𝜒, while for J𝑀K 𝜒 .(nrm), only the behavior of external calls are interpreted by 𝜒.


external procedures is given by an oracle 𝜒 (⊆ ident × gstate × gstate). The terminating behavior of
an open module 𝑀 that consists of a list of procedures 𝑝 1 ; ...; 𝑝𝑛 can then be defined as:
                                                                                
         J𝑀K 𝜒 .(nrm) ≜ 𝜇 𝜒 0 . J𝑝 1 K 𝜒0 ∪𝜒 .(nrm) ∪ · · · ∪ J𝑝𝑛 K 𝜒0 ∪𝜒 .(nrm) , where 𝑀 = 𝑝 1 ; . . . ; 𝑝𝑛 (7)
It is trivial to see that the standard whole-program denotational semantics given in Formula (6) is a
special case of Formula (7). In Formula (7), the semantic oracle 𝜒 0 (⊆ ident×gstate×gstate) represents
the terminating behavior of internal procedures, and the Kleene least fixed-point operator is used to
capture arbitrary finite layers of internal calls. It is worth noting that although both the terminating
behavior of a single procedure and that of an open module are subsets of ident × gstate × gstate,
they depend on different semantic oracles. As shown in Fig. 6, the semantics of a procedure depends
on the semantics of all invoked procedures, even including recursive calls to itself. In comparison,
the semantics of an open module depends on the semantics of external procedures only.
4.2.2 Semantic Linking. Semantic linking means composing the behavior of individual modules
as a whole so that cross-module calls between module 𝑀1 and module 𝑀2 before linking become
“internal” calls after linking. That is, after semantic linking, only external calls outside module 𝑀1
and module 𝑀2 need to be interpreted by a semantic oracle. Therefore, the definition of semantic
linking is straightforward: assume that the terminating behavior of procedures outside module 𝑀1
and 𝑀2 are given by an oracle 𝜒, the terminating behavior of semantic linking is defined as:
                                                                                               
                    (J𝑀1 K ⊕ J𝑀2 K) 𝜒 .(nrm) ≜ 𝜇 𝜒 0 . J𝑀1 K 𝜒0 ∪𝜒 .(nrm) ∪ J𝑀2 K 𝜒0 ∪𝜒 .(nrm)      (8)
As we can see, similar to the semantic definition of modules, the semantic linking between two
modules is defined by merging their denotations as if all the procedures reside in one module and
then taking the fixed point. Based on these definitions, the equivalence between semantic and
syntactic linking is shown as follows, which is reduced to Bekić’s theorem [Bekić 1984]. Therefore,
proving horizontal compositionality in our framework is straightforward.
   Theorem 4.1 (Eqivalence between semantic and syntactic linking). For any modules
𝑀1 and 𝑀2 , J𝑀1 K ⊕ J𝑀2 K = J𝑀1 + 𝑀2 K, where “+” is syntactic linking, physically putting modules
together.

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                             5:15


  Theorem 4.2 (Bekić’s theorem). Given CPOs 𝐴1 and 𝐴2 , for any monotonic and continuous
functions 𝑓 : 𝐴1 × 𝐴2 → 𝐴1 and 𝑔 : 𝐴1 × 𝐴2 → 𝐴2 ,
                                                                                           
                   𝜇 (𝑥, 𝑦). 𝜇𝑥 0 .𝑓 (𝑥 0, 𝑦), 𝜇𝑦0 .𝑔(𝑥, 𝑦0 ) = 𝜇 (𝑥, 𝑦). 𝑓 (𝑥, 𝑦), 𝑔(𝑥, 𝑦)
   Note that Thm. 4.1 is not specific to PCALL. It generally holds for settings where the semantics
of open modules and their semantic linking are defined in the form of Formulae (7) and (8).

4.3     Diverging Behavior of PCALL
The diverging behavior of a procedure can be induced either by its internal statements or by
recursive procedure calls. We define the diverging behavior of a PCALL program as follows: when
defining statement denotation J𝑐K 𝜒 and procedure denotation J𝑝K 𝜒 , we only consider internal
divergence (caused by dead loops) first. Those caused by procedure calls (including dead loops
in callee procedures and infinite layers of nested calls) are captured at the moment of defining
module denotation J𝑀K 𝜒 . For this purpose, we further add the following set cll to CDenote to record
the point of procedure calls, so that an element (𝜎0, (𝑖𝑑, 𝑔)) ∈ J𝑐K 𝜒 .(cll) if and only if executing
statement 𝑐 from state 𝜎0 could reach a point of procedure call named 𝑖𝑑 at global state 𝑔.
      cll: state → query → Prop, where query ≜ ident × gstate.

The calling behavior J𝑐K 𝜒 .(cll) is also recursively defined on the syntax of statements, for example,
                                                                                                  
                      J𝑐 1 ; 𝑐 2 K 𝜒 .(cll) ≜ J𝑐 1 K 𝜒 .(cll) ∪ J𝑐 1 K 𝜒 .(nrm) ◦ J𝑐 2 K 𝜒 .(cll)
                                                                 
                      Jcall 𝑖𝑑K 𝜒 .(cll) ≜ (𝑙, 𝑔), (𝑖𝑑, 𝑔) | (𝑙, 𝑔) ∈ state

Correspondingly, the calling behavior of a procedure J𝑝K 𝜒 .(cll) is derived from that of its body, i.e.,
                                                                                                  
 J𝑝K 𝜒 .(cll) ≜ (𝑖𝑑𝑝 , 𝑔0 ), (𝑖𝑑, 𝑔2 ) | ∃𝑙 1 𝑔1, (𝑙 1, 𝑔1 ) = Init (𝑝, 𝑔0 ) ∧ (𝑙 1, 𝑔1 ), (𝑖𝑑, 𝑔2 ) ∈ J𝑐 𝑝 K 𝜒 .(cll)

4.3.1 Diverging Behavior of Open Modules. We use J𝑀K 𝜒 .(dvg) (⊆ ident × gstate) to denote the
diverging behavior of open modules. Specifically, (𝑖𝑑, 𝑔) ∈ J𝑀K 𝜒 .(dvg) if and only if there exists a
procedure named 𝑖𝑑 in module 𝑀 and its execution beginning with global state 𝑔 could diverge due
to internal statements after a finite number of procedure calls, or an infinite number of internal
procedure calls inside module 𝑀. Thus, assume that the terminating behavior of external procedures
is given by semantic oracle 𝜒, and let 𝜒ˆ = J𝑀K 𝜒 .(nrm) ∪ 𝜒 (i.e., 𝜒ˆ specifies the terminating behavior
of all procedures, including both internals and externals), J𝑀K 𝜒 .(dvg) can be defined as:
                          L𝑀M 𝜒ˆ ≜ J𝑝 1 K 𝜒ˆ ∪ · · · ∪ J𝑝𝑛 K 𝜒ˆ , where 𝑀 = 𝑝 1 ; . . . ; 𝑝𝑛
                                                                          
                          J𝑀K 𝜒 .(dvg) ≜ L𝑀M 𝜒ˆ .(cll)∗ ◦ L𝑀M 𝜒ˆ .(dvg) ∪ L𝑀M 𝜒ˆ .(cll)∞

where L𝑀M 𝜒ˆ is defined by simply merging corresponding behavior sets of procedures 𝑝 1, . . . , 𝑝𝑛 .
   We further use J𝑀K 𝜒 .(cll) (⊆ query × query) to denote the calling behavior of a module such that
an internal procedure of module 𝑀 could eventually call an external procedure after a finite number
of internal calls. Let J𝑀K 𝜒 .(dom) (⊆ ident) be the set of procedure names defined in 𝑀, and then
                        ExtnlQuery (𝑋 ) ≜ { (𝑖𝑑, 𝑔) | 𝑖𝑑 ∉ 𝑋 } , for 𝑋 ⊆ ident
                                                                                               
                        J𝑀K 𝜒 .(cll) ≜ L𝑀M 𝜒ˆ .(cll)+ ◦ test ExtnlQuery (J𝑀K 𝜒 .(dom))
4.3.2 Diverging Behavior of Semantic Linking. Based on the definitions above, semantic linking can
be easily extended to the dvg field and cll field: assume that the terminating behavior of external
procedures outside 𝑀1 and 𝑀2 is given by semantic oracle 𝜒, and let 𝜒ˆ = (J𝑀1 K ⊕ J𝑀2 K) 𝜒 .(nrm) ∪ 𝜒,

      ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:16                                                                                                             Z. Cheng et al.


(J𝑀1 K ⊕ J𝑀2 K) 𝜒 .(dvg) can be defined as follows.
                                                                         ∗                                      
       (J𝑀1 K ⊕ J𝑀2 K) 𝜒 .(dvg) ≜ J𝑀1 K 𝜒ˆ .(cll) ∪ J𝑀2 K 𝜒ˆ .(cll)           ◦ J𝑀1 K 𝜒ˆ .(dvg) ∪ J𝑀2 K 𝜒ˆ .(dvg) ∪
                                                                         ∞
                                     J𝑀1 K 𝜒ˆ .(cll) ∪ J𝑀2 K 𝜒ˆ .(cll)
                                                                         +                                               
       (J𝑀1 K ⊕ J𝑀2 K) 𝜒 .(cll) ≜ J𝑀1 K 𝜒ˆ .(cll) ∪ J𝑀2 K 𝜒ˆ .(cll)           ◦ test ExtnlQuery (J𝑀1 + 𝑀2 K 𝜒 .(dom))
   Remark. There may exist traditional approaches [Back 1983] that, for example, assume another
semantic oracle 𝜒 ′ (⊆ ident × gstate) to interpret the diverging behavior of procedure calls, so that
the diverging behavior of a module can be defined by taking appropriate fixed points of recursive
equations similar to Formula (7). However, this approach is not available for practical C modules,
since one will meet the same stuttering problem as we do in §3.3 when observable events are taken
into account. Our approach successfully solves this problem. We can similarly define J𝑀K 𝜒 .(fin_dvg)
and J𝑀K 𝜒 .(inf_dvg) for realistic C modules like how we handle Clight loops. The key point is to use
△L𝑀M 𝜒 .(cll) and ▲L𝑀M 𝜒 .(cll) in the definition so that we can distinguish the cases that zero events
happen before a call and the cases that at least one event happens before the call. We illustrate this
in §6.4, where the semantics of function calls and open modules in practical languages are defined
similarly to the semantics of PCALL procedures and PCALL modules shown in this section, and
the primary differences lie in the additional manipulation w.r.t. arguments and return values.

4.4      Semantics of Unstructured Branches
We further consider unstructured branches on top of PCALL with the following GOTO language.
𝑐 ≜ skip | 𝑎𝑡𝑜𝑚 | 𝑐 1 ; 𝑐 2 | choice(𝑐 1, 𝑐 2 ) | if 𝑏 then 𝑐 1 else 𝑐 2 | while 𝑏 do 𝑐 | call 𝑖𝑑 | 𝑗 : 𝑐 | goto 𝑗
where 𝑗 ranges over the set of labels. For handling goto statements, we add the following gto set to
CDenote, so that an element (𝜎0, ( 𝑗, 𝜎1 )) ∈ J𝑐K 𝜒 .(gto) if and only if executing statement 𝑐 from state
𝜎0 could reach a point of jumping by goto statement at state 𝜎1 for the first time.
 gto: state → trace → goto_info → Prop, where goto_info ≜ label × state, and label is the set of labels.

We additionally define the behavior of goto statements as follows, where the normal execution of
a program will be interrupted by a goto statement, so Jgoto 𝑗K 𝜒 .(nrm) is assigned the empty set.
                      Jgoto 𝑗K 𝜒 .(nrm) ≜ ∅           Jgoto 𝑗K 𝜒 .(gto) ≜ {(𝜎, ( 𝑗, 𝜎)) | 𝜎 ∈ state}
Existing semantic definition of other statements is the same as PCALL. The “goto” exiting behavior
of other statements is recursively defined similarly to the calling behavior in §4.3, for example,
                             J𝑐 1 ; 𝑐 2 K 𝜒 .(gto) ≜ J𝑐 1 K 𝜒 .(gto) ∪ J𝑐 1 K 𝜒 .(nrm) ◦ J𝑐 2 K 𝜒 .(gto)
We then use the following auxiliary relations to denote the terminating, “goto” exiting, and diverging
behavior of executing 𝑐 from given labels, respectively.
                                          T𝑐U 𝜒 .(nrm) ⊆ goto_info × state
                                          T𝑐U 𝜒 .(gto) ⊆ goto_info × goto_info
                                          T𝑐U 𝜒 .(dvg) ⊆ goto_info
They are defined by evaluating part of statement 𝑐 from a given label, such that, for example, an
element (( 𝑗, 𝜎0 ), 𝜎1 ) ∈ T𝑐U 𝜒 .(nrm) if and only if we can find a labeled position “𝑗 : ...” in 𝑐 and
executing 𝑐 from 𝑗 at state 𝜎0 could terminate at 𝜎1 . For instance, given statements 𝑠 1 and 𝑠 2 ,
                          T𝑐 1 ; 𝑗1 : 𝑐 2 U 𝜒 .(nrm) ≜ {(( 𝑗1, 𝜎0 ), 𝜎1 ) | (𝜎0, 𝜎1 ) ∈ J𝑐 2 K 𝜒 .(nrm)}

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                            5:17


Finally, the behavior of a procedure 𝑝 whose body 𝑐 supports goto constructs is extended as follows.
                 (                                                                                          )
                                                    (𝑙 1, 𝑔1 ), (𝑙 2, 𝑔2 ) ∈ J𝑐K 𝜒 .(nrm) ∪ J𝑐K 𝜒 .(gto) ◦ N
   J𝑝K 𝜒 .(nrm) ≜ (𝑖𝑑𝑝 , 𝑔0, 𝑔3 ) ∃𝑙 1 𝑔1 𝑙 2 𝑔2,
                                                    ∧ (𝑙 1, 𝑔1 ) = Init (𝑝, 𝑔0 ) ∧ 𝑔3 = Free (𝑙 2, 𝑔2 )
                                                                                                                
   J𝑝K 𝜒 .(dvg) ≜ (𝑖𝑑𝑝 , 𝑔0 ) ∃𝑙 1 𝑔1, (𝑙 1, 𝑔1 ) = Init (𝑝, 𝑔0 ) ∧ (𝑙 1, 𝑔1 ) ∈ J𝑐K 𝜒 .(dvg) ∪ J𝑐K 𝜒 .(gto) ◦ F
                                                                                             
      where N = T𝑐U 𝜒 .(gto)∗ ◦ T𝑐U 𝜒 .(nrm)            F = T𝑐U 𝜒 .(gto)∗ ◦ T𝑐U 𝜒 .(dvg) ∪ (T𝑐U 𝜒 .(gto)) ∞
Here, N denotes that executing 𝑐 from a given label could terminate normally after a finite number
of “goto” iterations, and F denotes that executing 𝑐 from a given label could diverge, either by a
certain sub-statement that could diverge after a finite number of “goto” iterations or by an infinite
number of “goto” iterations. The procedure would then terminate if its body 𝑐 normally terminate,
or the body meets a goto statement (i.e., goto 𝑗) and then execution from the given label 𝑗 would
finally terminate. The diverging behaviors are handled similarly, with additional consideration of
infinite iterations by goto. Intuitively, unstructured branchings resembles a loop with multiple
entry points, where each labeled statement acts as an entry, and each goto statement specifies
which entry to jump to. Finally, the way of defining the semantics of open modules and their
semantic linking is equally applicable to programs with goto constructs, as further illustrated in §6.

5   Denotational Semantics of Control Flow Graphs
Most compiler back-ends, including those of LLVM, GCC, and CompCert, are based on Control Flow
Graphs (CFGs). We use the following CFG language to illustrate how the semantic linking shown
in §4 can be applied to these settings. We here do not consider observable events for simplicity.
             Instructions                           𝐼 ≜ Do(𝑎𝑡𝑜𝑚, 𝑗) | Call(𝑖, 𝑗) | Cond(𝑏, 𝑗1, 𝑗2 )
             Control flow graph                    𝐺 ≜ 𝑗 ↦→ 𝐼
             Procedures                             𝑝 ≜ (𝑖 𝑝 , 𝑗entry, 𝑗exit, 𝐺)
             Modules                                𝑀 ≜ 𝑝 1 ; ...; 𝑝𝑛
A CFG is formulated as a finite mapping from labels to instructions. Each instruction carries the
labels of its possible successors. Specifically, the execution of Do(𝑎𝑡𝑜𝑚, 𝑗) involves executing the
atomic instruction 𝑎𝑡𝑜𝑚 (e.g., an assignment) and then branching to node 𝑗. The instruction Call(𝑖, 𝑗)
means invoking procedure 𝑖 and then branching to node 𝑗. Finally, the instruction Cond(𝑏, 𝑗1, 𝑗2 )
denotes a conditional branch determined by the truth value of the pure condition 𝑏, which is
assumed to have no side effects. We model the nodes of CFGs with instructions rather than basic
blocks since this simplifies semantics and reasoning over static analyses [Knoop et al. 1998].
   The set of program states is defined as state ≜ label × lstate × gstate. We again use a semantic
oracle 𝜒 (⊆ ident × gstate × gstate) to interpret the semantics of callee procedures, so as to apply
the method presented in §4 to define the semantics of open modules and semantic linking in this
context. The denotational semantics of typical instructions can then be defined as follows.
                                               ′
                                    ′
      jump( 𝑗) ≜ { ( 𝑗pc, 𝑙, 𝑔), ( 𝑗pc , 𝑙, 𝑔) | 𝑗pc = 𝑗 }, where 𝑗pc is the label of the current node.
      JDo(𝑎𝑡𝑜𝑚, 𝑗)K 𝜒 .(nrm) ≜ J𝑎𝑡𝑜𝑚K 𝜒 .(nrm) ◦ jump( 𝑗)
                                                            
      JCall(𝑖, 𝑗)K 𝜒 .(nrm) ≜ { ( 𝑗pc, 𝑙, 𝑔), ( 𝑗pc, 𝑙, 𝑔′ ) | (𝑖, 𝑔, 𝑔′ ) ∈ 𝜒 } ◦ jump( 𝑗)
      JCond(𝑏, 𝑗1, 𝑗2 )K 𝜒 .(nrm) ≜ test(J𝑏K.(tts)) ◦ jump( 𝑗1 ) ∪ test(J𝑏K.(ffs)) ◦ jump( 𝑗2 )

We next use J𝐺K 𝜒 .(nrm) to denote the general union of denotations of all nodes. Because a procedure
could normally terminate if and only if executing instructions from the entry node could finally

     ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:18                                                                                                      Z. Cheng et al.


                   Table 1. Program states and the query–reply interface for function calls.

              Component             Formal definition                        Representative element
              Program states        statec ≜ tenv × mem                         (𝑡𝑒, 𝑚) ∈ state
              C queries             cquery ≜ ident × list val × mem          (𝑖𝑑, 𝑣®, 𝑚) ∈ cquery
              C replies             creply ≜ mem × val                         (𝑚 ′, 𝑣 ′ ) ∈ creply


branch to the exit node after a finite number of branches between nodes, the terminating behavior
of procedures and open modules (i.e., J𝑝K 𝜒 .(nrm) and J𝑀K 𝜒 .(nrm)) can then be defined as follows.
                        Ð                       
         J𝐺K 𝜒 .(nrm) ≜ 𝑗 J𝐺 ( 𝑗)K 𝜒 .(nrm)
                                                                                        
         J𝑝K 𝜒 .(nrm) ≜ {(𝑖𝑝 , 𝑔, 𝑔′ ) | ∃𝑙 ′, ( 𝑗entry, 𝑙 empty, 𝑔), ( 𝑗exit, 𝑙 ′, 𝑔′ ) ∈ J𝐺K 𝜒 .(nrm)∗ }
                                                                                 
         J𝑀K 𝜒 .(nrm) ≜ 𝜇 𝜒 0 . J𝑝 1 K 𝜒0 ∪𝜒 .(nrm) ∪ · · · ∪ J𝑝𝑛 K 𝜒0 ∪𝜒 .(nrm) , where 𝑀 = 𝑝 1 ; . . . ; 𝑝𝑛
The semantics of open modules is defined the same way as that in §4.2, so is the semantic linking.
In essence, the denotational semantics of control-flow graphs (CFGs) does not fundamentally
differ from their small-step semantics, except for the treatment of procedure calls. The purpose
of presenting the semantics of CFGs in this section is to illustrate that this semantic construction
naturally scales to the CompCert back-end languages. Accordingly, the semantic linking operator
defined in §4.2 can also be applied to the CompCert back-end, in particular to its assembly languages.

6      Semantics of CompCert Front-end Languages
6.1     Languages and Semantic Domain
   Syntax of Clight. We write 𝑠 for the syntax of Clight statements, 𝐹 for Clight functions, 𝑒 for
Clight expressions, and 𝑥, 𝑦, 𝑧 for program variables. We recall the key definitions as follows, where
                                                                    −−−−→
?𝑡𝑒𝑟𝑚 denotes the optional occurrence of a syntactic term, and 𝑡𝑒𝑟𝑚𝑘 is a list of syntactic terms
with the representative element 𝑡𝑒𝑟𝑚𝑘 . The full syntax of Clight can be found in [Blazy et al. 2006].

       (Statements)        𝑠 ≜ skip | 𝑠 1 ; 𝑠 2 | if(𝑒) 𝑠 1 else 𝑠 2 | loop 𝑠 1 𝑠 2 | call ?𝑥 𝑒 1 → −
                                                                                                    𝑒2 | 𝑥 = 𝑒 |       (9)
                                                                                                           −−−−−−−→
                               break | continue | return ?𝑒 | goto 𝑗 | 𝑗 : 𝑠 | switch 𝑒 (?𝑛𝑘 , 𝑠𝑘 )
                                                                      −−−−−−−→                           −−−−−−→
                               where ?𝑡𝑒𝑟𝑚 ≜ ? | 𝑡𝑒𝑟𝑚                 (?𝑛𝑘 , 𝑠𝑘 ) ≜ LSnil | (𝑛 1, 𝑠 1 ); (?𝑛 2, 𝑠 2 )
                                −−−−−−−−−→ −−−−−−−−−→ −−−−−−−−−→
       (Functions)         𝐹 ≜ ( (𝑥𝑘 , 𝑡𝑦𝑝𝑒𝑘 ), (𝑦𝑘 , 𝑡𝑦𝑝𝑒𝑘 ), (𝑧𝑘 , 𝑡𝑦𝑝𝑒𝑘 ), 𝑠 𝐹 , 𝑟𝑒𝑡𝑢𝑟𝑛_𝑡𝑦𝑝𝑒 𝐹 )                   (10)

A Clight function is defined as a quintuple consisting, from left to right, of the parameter list, the
list of local variables, the list of temporary variables, the function body, and the return type of 𝐹 .
   CompCert memory model. CompCert models memories as a collection of disjoint blocks, each
identified by a block identifier (ranged over by 𝑏 of a countable set B). Within a block, memory
contents are addressed by an integer offset (ranged over by 𝑜 of the integer set Z), and operations
(e.g., load and store) are defined in terms of these block-offset pairs (i.e., memory locations). A
memory state (of set mem) can be simply viewed as a mapping from memory locations to program
values8 (of set val) that range over 32-bit integers, 64-bit floating-point numbers, pointers, and a
special value Vundef. This memory model is employed for all intermediate languages of CompCert.

8We refer to Leroy et al. [2012] for the detailed definition of the CompCert memory model.



ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                              5:19


   Clight semantic infrastructures. As shown in Table 1, a Clight program state is defined as a pair
consisting of a temporary environment 𝑡𝑒 and a memory state 𝑚, where a temporary environment
is a mapping from variables to its values. A C function call provides a query consisting of the
invoked function identifier 𝑖𝑑, the argument list 𝑣®, and the memory state 𝑚. After the function call,
the corresponding reply consisting of a memory state 𝑚 ′ and a return value 𝑣 ′ may be received.
  Clight statement denotations. A Clight statement denotation is defined by the following signature.
      Record Clit.Denote: Type := {
         nrm: state → trace → state → Prop;           (* nrm ⊆ state × trace × state ---------- *)
         brk: state → trace → state → Prop;           (* brk ⊆ state × trace × state ---------- *)
         ctn: state → trace → state → Prop;           (* ctn ⊆ state × trace × state ---------- *)
         rtn: state → trace → state → val → Prop;     (* rtn ⊆ state × trace × state × val ----*)
         err: state → trace → Prop;                   (* err ⊆ state × trace -------------------*)
         cll: state → trace → cquery → Prop;          (* cll ⊆ state × trace × cquery --------- *)
         gto: state → trace → (label × state) → Prop; (* gto ⊆ state × trace × (label × state) *)
         fin_dvg: state → trace → Prop;               (* fin_dvg ⊆ state × trace ---------------*)
         inf_dvg: state → itrace → Prop               (* inf_dvg ⊆ state × itrace --------------*)
      }.

CompCert classifies program behaviors into four categories: normal termination, abortion, silent
divergence, and reacting divergence. They are captured in our denotation by the sets nrm, err,
fin_dvg, and inf_dvg, respectively. Additionally, the sets brk, ctn, and rtn are introduced to account
for Clight’s structured control flow, corresponding to the break, continue, and return statements.
Furthermore, the set cll is used to conveniently capture abortion and divergence arising from
recursive calls, while the set gto is designed to capture possible unstructured branching by goto.
   Function/Open module denotations. Functions or open modules communicate with each other by
language interfaces [Koenig and Shao 2021; Zhang et al. 2024]. Formally, a language interface is
a tuple ⟨query, reply⟩, where query is a set of queries and reply is a set of replies. The signature of
function/open module denotations is parameterized by a language interface, as defined below.
      Record FDenote {query reply: Type}: Type := {
         dom: ident → Prop;                                (* dom ⊆ ident ---------------------------- *)
         nrm: query → trace → reply → Prop;                (* nrm ⊆ query × trace × reply ----------- *)
         err: query → trace → Prop;                        (* err ⊆ query × trace --------------------*)
         cll: query → trace → query → Prop;                (* cll ⊆ query × trace × query ----------- *)
         fin_dvg: query → trace → Prop;                    (* fin_dvg ⊆ query × trace ----------------*)
         inf_dvg: query → itrace → Prop                    (* inf_dvg ⊆ query × itrace ---------------*)
      }.

At the function level, the denotation ignores statement-level details (captured by the sets brk, ctn, rtn,
and gto of Clit.Denote), and instead focuses on the four resulting behaviors from a given incoming
query (i.e., termination, abortion, silent divergence, and reacting divergence), each capturing the
original observable behaviors in CompCert (by the trace or itrace field of each behavior set).

6.2     Denotational Semantics of Clight Statements
   Overview. We compositionally build the semantics of Clight statements from broken semantics,
labeled broken semantics, and finally to the intact semantics, as shown in Table 2. Broken semantics
captures the behavior of a statement 𝑠 under the convention that execution halts immediately upon
encountering a goto statement, thereby disregarding the semantics of any subsequent instruc-
tions that the goto might target. Building upon this, labeled broken semantics interprets 𝑠 from
a specified label, but still within the broken-semantics discipline. Finally, the intact semantics of

       ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:20                                                                                                    Z. Cheng et al.


                          Table 2. Three related semantic notions of Clight statements.

  Semantics                             Symbol         Denotation            Brief Description
   Broken semantics                       J𝑠KE𝜒        Clit.Denote           Halt at goto statements.
   Labeled broken semantics              T𝑠UE𝜒     label → Clit.Denote       Start from a given label.
   Intact semantics                      {{𝑠}}E𝜒       Clit.Denote           Full semantics via composition.


Clight statements is obtained by systematically composing the (labeled) broken semantics, thus
recovering the full control-flow behavior of goto statements.
   These semantics are parameterized by an environment E and a semantic oracle 𝜒 (⊆ cquery ×
trace × creply), where E is a tuple of global environment g and local environment e, and the oracle
𝜒 is used for specifying the terminating behavior of function calls from the Clight statement 𝑠.
6.2.1   Broken Semantics of Clight Statements.
   Atomic statements. The denotation of atomic statements satisfy the following equations, where
expr_eval (E, 𝜎, 𝑒) means trying to derive the value of 𝑒 under environment E and state 𝜎.
  JskipKE𝜒 .( nrm) ≜ 1    JskipKE𝜒 .( xxx) ≜ ∅, for xxx ∈ { brk, ctn, rtn, err, cll, gto, fin_dvg, inf_dvg }
                                                                                                
                                              ∃𝑣, expr_eval (E, (𝑡𝑒, 𝑚), 𝑒) = Succeed(𝑣)
         E                              ′
  J𝑥 = 𝑒K 𝜒 .( nrm) ≜ (𝑡𝑒, 𝑚), nil, (𝑡𝑒 , 𝑚)                                                              (11)
                                                  ∧ 𝑡𝑒 ′ = 𝑡𝑒 [𝑥 ↦→ 𝑣]
                           
  J𝑥 = 𝑒KE𝜒 .( err) ≜ 𝜎, nil | expr_eval (E, 𝜎, 𝑒) = Fail                                                 (12)
  J𝑥 = 𝑒KE𝜒 .( xxx) ≜ ∅, for xxx ∈ { brk, ctn, rtn, cll, gto, fin_dvg, inf_dvg }                                  (13)
  Jreturn ?𝑒KE𝜒 .( rtn) ≜ { (𝜎, nil, 𝜎, 𝑣) | expr_eval (E, 𝜎, ?𝑒) = Succeed(𝑣) }                                  (14)
  Jreturn ?𝑒KE𝜒 .( err) ≜ { (𝜎, nil) | expr_eval (E, 𝜎, ?𝑒) = Fail }                                              (15)
  Jreturn ?𝑒KE𝜒 .( xxx) ≜ ∅, for xxx ∈ { nrm, brk, ctn, cll, gto, fin_dvg, inf_dvg }                              (16)
  Clight function calls. The denotation of Clight function calls satisfies the following equations,
where query_eval (E, 𝜎, 𝑒 1, →  −
                                𝑒 2 ) means trying to derive the query of a call from 𝑒 1 and →          −
                                                                                                         𝑒 2 under
environment E and state 𝜎.
                              (                                                                                    )
             →
             −                                         ∃𝑞, query_eval (E, (𝑡𝑒, 𝑚), 𝑒 1, →   −
                                                                                            𝑒 2 ) = Succeed(𝑞)
Jcall ?𝑥 𝑒 1 𝑒 2 K 𝜒 .( nrm) ≜ ((𝑡𝑒, 𝑚), 𝜏, (𝑡𝑒 , 𝑚 ))
                  E                            ′   ′
                                                          ∧ ∃𝑣 ′, (𝑞, 𝜏, (𝑚 ′, 𝑣 ′ )) ∈ 𝜒 ∧ 𝑡𝑒 ′ = 𝑡𝑒 [?𝑥 ↦→ 𝑣 ′ ]
                              
Jcall ?𝑥 𝑒 1 →
             −
             𝑒 2 KE𝜒 .( cll) ≜ (𝜎, nil, 𝑞) | query_eval (E, 𝜎, 𝑒 1, →−
                                                                     𝑒 2 ) = Succeed(𝑞)                         (17)
             →
             −                                                 →−
Jcall ?𝑥 𝑒 1 𝑒 2 K 𝜒 .( err) ≜ (𝜎, nil) | query_eval (E, 𝜎, 𝑒 1, 𝑒 2 ) = Fail
                  E
                                                                                                                (18)
Jcall ?𝑥 𝑒 →1
             −
             𝑒 KE .( xxx) ≜ ∅, for xxx ∈ { brk, ctn, rtn, gto, fin_dvg, inf_dvg }
                2 𝜒                                                                                             (19)
  Operators for composing denotations. Before showing the semantics of composite statements, we
define the following operators for semantic composition. Specifically, for given denotations 𝐷 1
and 𝐷 2 of Clit.Denote, we use 𝐷 1 ⋓ 𝐷 2 to denote the union of them, and use 𝐷 1 # 𝐷 2 to denote the
sequential composition of them, in which the composition operator ◦ is overloaded as follows.
(𝐷 1 ⋓ 𝐷 2 ).( xxx) ≜ 𝐷 1 .( xxx) ∪ 𝐷 2 .( xxx), for xxx ∈ { nrm, brk, ctn, rtn, err, cll, gto, fin_dvg, inf_dvg }
(𝐷 1 # 𝐷 2 ).( nrm) ≜ 𝐷 1 .( nrm) ◦ 𝐷 2 .( nrm)
(𝐷 1 # 𝐷 2 ).( xxx) ≜ 𝐷 1 .( xxx) ∪ (𝐷 1 .( nrm) ◦ 𝐷 2 .( xxx)), xxx ∈ {brk, ctn, rtn, err, cll, gto, fin_dvg, inf_dvg}

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                                    5:21


     where 𝑅1 ◦ 𝑌 ≜ {(𝜎1, 𝜏) | ∃𝜎2 𝜏1 𝜏2, (𝜎1, 𝜏1, 𝜎2 ) ∈ 𝑅1 ∧ (𝜎2, 𝜏2 ) ∈ 𝑌 ∧ 𝜏 = 𝜏1 · 𝜏2 }
                  𝑅1 ◦ 𝑅2 ≜ {(𝜎1, 𝜏, 𝜎3 ) | ∃𝜎2 𝜏1 𝜏2, (𝜎1, 𝜏1, 𝜎2 ) ∈ 𝑅1 ∧ (𝜎2, 𝜏2, 𝜎3 ) ∈ 𝑅2 ∧ 𝜏 = 𝜏1 · 𝜏2 }
                  𝑅1 ◦ 𝑉 ≜ {(𝜎1, 𝜏, 𝜎3, 𝑣) | ∃𝜎2 𝜏1 𝜏2, (𝜎1, 𝜏1, 𝜎2 ) ∈ 𝑅1 ∧ (𝜎2, 𝜏2, 𝜎3, 𝑣) ∈ 𝑉 ∧ 𝜏 = 𝜏1 · 𝜏2 }

  Clight control flow. The denotations of Clight control flow statements (i.e., conditional branching,
sequential statements, break, continue, return, and Clight loops) satisfy the following equations,
where bool_eval (E, 𝜎, 𝑒) meaning trying to derive the Boolean value of the Clight expression 𝑒
under environment E and state 𝜎. We write ⇑ 𝑋 to lift a set of states 𝑋 into a binary relation with
empty trace, and ∇𝑅 to project a ternary relation 𝑅 onto a binary one by canceling its target state.

      J𝑒KE .(tss) (⊆ state) ≜ { 𝜎 | bool_eval (E, 𝜎, 𝑒) = Succeed(T) }
      J𝑒KE .(fss) (⊆ state) ≜ { 𝜎 | bool_eval (E, 𝜎, 𝑒) = Succeed(F) }
      J𝑒KE .(err) (⊆ state) ≜ { 𝜎 | bool_eval (E, 𝜎, 𝑒) = Fail }
       ⇑ 𝑋 ≜ { (𝜎, nil) | 𝜎 ∈ 𝑋 },                       for 𝑋 ⊆ state,
      ∇𝑅 ≜ { (𝜎, 𝜏) | ∃𝜎 , (𝜎, 𝜏, 𝜎 ) ∈ 𝑅}, for 𝑅 ⊆ state × trace × state.
                                    ′          ′

      J𝑠 1 ; 𝑠 2 KE𝜒 ≜ J𝑠 1 KE𝜒 # J𝑠 2 KE𝜒
      J if(𝑒) 𝑠 1 else 𝑠 2 KE𝜒 .( xxx) ≜ test(J𝑒KE .(tss)) ◦ J𝑠 1 KE𝜒 .( xxx) ∪ test(J𝑒KE .(fss)) ◦ J𝑠 2 KE𝜒 .( xxx),
                        for xxx ∈ { nrm, brk, ctn, rtn, cll, gto, fin_dvg, inf_dvg }
      J if(𝑒) 𝑠 1 else 𝑠 2 KE𝜒 .( err) ≜
                       (⇑ J𝑒KE .(err)) ∪ test(J𝑒KE .(tss)) ◦ J𝑠 1 KE𝜒 .( err) ∪ test(J𝑒KE .(fss)) ◦ J𝑠 2 KE𝜒 .( err)
      JbreakKE𝜒 .( brk) ≜ 1, and other fields are assigned the empty set.
      JcontinueKE𝜒 .( ctn) ≜ 1, and other fields are assigned the empty set.
      𝑁 1 = J𝑠 1 KE𝜒 .( nrm) ∪ J𝑠 1 KE𝜒 .( ctn)       𝑁 12 = 𝑁 1 ◦ J𝑠 2 KE𝜒 .( nrm)
                                    ∗
      Jloop 𝑠 1 𝑠 2 KE𝜒 .( nrm) ≜ 𝑁 12 ◦ (J𝑠 1 KE𝜒 .( brk) ∪ 𝑁 1 ◦ J𝑠 2 KE𝜒 .( brk))
      Jloop 𝑠 1 𝑠 2 KE𝜒 .( brk) = Jloop 𝑠 1 𝑠 2 KE𝜒 .( ctn) ≜ ∅
                                    ∗
      Jloop 𝑠 1 𝑠 2 KE𝜒 .( xxx) ≜ 𝑁 12 ◦ (J𝑠 1 KE𝜒 .( xxx) ∪ 𝑁 1 ◦ J𝑠 2 KE𝜒 .( xxx)), for xxx ∈ { rtn, cll, gto }
                                    ∗                                                                          
      Jloop 𝑠 1 𝑠 2 KE𝜒 .( err) ≜ 𝑁 12 ◦ J𝑠 1 KE𝜒 .( err) ∪ 𝑁 1 ◦ J𝑠 2 KE𝜒 .( err) ∪ 𝑁 1 ◦ (∇J𝑠 2 KE𝜒 .( ctn))
                                                                                                            
                                         ∗
      Jloop 𝑠 1 𝑠 2 KE𝜒 .( fin_dvg) ≜ 𝑁 12 ◦ J𝑠 1 K.(fin_dvg) ∪ 𝑁 1 ◦ J𝑠 2 K.(fin_dvg) ∪ (△𝑁 12 ) ∞
                                                                                                    
      Jloop 𝑠 1 𝑠 2 KE𝜒 .( inf_dvg) ≜ let D = J𝑠 1 KE𝜒 .( inf_dvg) ∪ 𝑁 1 ◦ J𝑠 2 KE𝜒 .( inf_dvg) in
                                             ((△𝑁 12 ) ∗ ◦ ▲𝑁 12 ) ∗ ◦ (△𝑁 12 ) ∗ ◦ D ∪ ((△𝑁 12 ) ∗ ◦ ▲𝑁 12 ) ∞

   Switch statement. In Clight, a switch statement evaluates a case expression 𝑒 and then selects the
                                                 −−−−−−−→
execution branch from a list of case statements (?𝑛𝑘 , 𝑠𝑘 ). Each case statement consists of an optional
case label ?𝑛𝑘 and its associated statement 𝑠𝑘 . If 𝑒 matches a case label, execution begins at that
case; if no match is found, execution starts from the first default case (denoted (?, 𝑠)); and if neither
a matching case nor a default exists, the switch terminates immediately, behaving as skip. Formally,
           −−−−−−−→
we use J (?𝑛𝑘 , 𝑠𝑘 )KE𝜒 to denote the semantics of sequentially executing the list of case statements
−−−−−−−→                                                                              −−−−−−−→
(?𝑛𝑘 , 𝑠𝑘 ) one by one, as defined by Equations (20) and (21). We further define {| (?𝑛𝑘 , 𝑠𝑘 )|}E𝜒 (𝑛) to
denote execution beginning from the case labeled 𝑛, if it exists, or from the default case otherwise.

     ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:22                                                                                                           Z. Cheng et al.




 JLSnilKE𝜒 ≜ JskipKE𝜒                                                                                                    (20)
                −−−−−−→                       −−−−−−→
 J(?𝑛 1, 𝑠 1 ); (?𝑛 2, 𝑠 2 )KE𝜒 ≜ J𝑠 1 KE𝜒 # J (?𝑛 2, 𝑠 2 )KE𝜒                                                           (21)


 {| LSnil |}E𝜒 (𝑛) ≜ JskipKE𝜒                                                                                            (22)
                −−−−−−→                  −−−−−−→
 {|(𝑛 1, 𝑠 1 ); (?𝑛 2, 𝑠 2 )|}E𝜒 (𝑛) ≜ {| (?𝑛 2, 𝑠 2 )|}E𝜒 (𝑛),         if 𝑛 ≠ 𝑛 1
                −−−−−−→                             −−−−−−→                                                              (23)
 {|(𝑛 1, 𝑠 1 ); (?𝑛 2, 𝑠 2 )|}E𝜒 (𝑛) ≜ J𝑠 1 KE𝜒 # J (?𝑛 2, 𝑠 2 )KE𝜒 ,   if 𝑛 = 𝑛 1
              −−−−−−→                             −−−−−−→                                       −−−−−−→
 {|(?, 𝑠 1 ); (?𝑛 2, 𝑠 2 )|}E𝜒 (𝑛) ≜ J𝑠 1 KE𝜒 # J (?𝑛 2, 𝑠 2 )KE𝜒 ,     if case 𝑛 not found in (?𝑛 2, 𝑠 2 )
              −−−−−−→                  −−−−−−→                                             −−−−−−→                       (24)
 {|(?, 𝑠 1 ); (?𝑛 2, 𝑠 2 )|}E𝜒 (𝑛) ≜ {| (?𝑛 2, 𝑠 2 )|}E𝜒 (𝑛),           if case 𝑛 found in (?𝑛 2, 𝑠 2 )


  ∥𝑒 ∥𝑛E .( nrm) ≜ { (𝜎, nil, 𝜎) | switch_case_eval (E, 𝜎, 𝑒) = Succeed(𝑛) }
 ∥𝑒 ∥𝑛E .( err) ≜ { (𝜎, nil) | switch_case_eval (E, 𝜎, 𝑒) = Fail }
               −−−−−−−→             Ð                     −−−−−−−→                      −−−−−−−→                    
 Jswitch 𝑒 (?𝑛𝑘 , 𝑠𝑘 )KE𝜒 .( nrm) ≜ 𝑛 ∥𝑒 ∥𝑛E .( nrm) ◦ {| (?𝑛𝑘 , 𝑠𝑘 )|}E𝜒 (𝑛).( nrm) ∪ {| (?𝑛𝑘 , 𝑠𝑘 )|}E𝜒 (𝑛).( brk)
               −−−−−−−→             Ð                    −−−−−−−→                   
 Jswitch 𝑒 (?𝑛𝑘 , 𝑠𝑘 )KE𝜒 .( err) ≜ 𝑛 ∥𝑒 ∥𝑛E .( nrm)) ◦ {| (?𝑛𝑘 , 𝑠𝑘 )|}E𝜒 (𝑛).( err) ∪ ∥𝑒 ∥𝑛E .( err)
           −−−−−−−→
 Jswitch 𝑒 (?𝑛𝑘 , 𝑠𝑘 )KE𝜒 .( brk) ≜ ∅
           −−−−−−−→                 Ð                    −−−−−−−→                   
 Jswitch 𝑒 (?𝑛𝑘 , 𝑠𝑘 )KE𝜒 .( xxx) ≜ 𝑛 ∥𝑒 ∥𝑛E .( nrm)) ◦ {| (?𝑛𝑘 , 𝑠𝑘 )|}E𝜒 (𝑛).( xxx) ,
                                               for xxx ∈ { rtn, cll, gto, fin_dvg, inf_dvg }
   Unstructured branching. The denotation of a goto statement and a labeled statement satisfy the
following equations, where Equation (25) and (26) reflect the essence of the name broken for J𝑠KE𝜒 .
          Jgoto 𝑗KE𝜒 .( gto) ≜ { (𝜎, nil, ( 𝑗, 𝜎)) | 𝜎 ∈ state }                                                         (25)
          Jgoto 𝑗KE𝜒 .( xxx) ≜ ∅, for xxx ∈ { nrm, brk, ctn, rtn, err, cll, fin_dvg, inf_dvg }                           (26)
          J𝑗 : 𝑠KE𝜒 .( xxx) ≜ J𝑠KE𝜒 .( xxx), for xxx ∈ { nrm, brk, ctn, rtn, err, cll, gto, fin_dvg, inf_dvg }           (27)
6.2.2 Labeled Broken Semantics of Clight Statements. We use T𝑠UE𝜒 ( 𝑗) to denote the semantics of
executing the statement 𝑠 from the given label 𝑗. If there is no such a labeled statement inside 𝑠,
then T𝑠UE𝜒 ( 𝑗) is assigned the empty denotation (i.e., each field of which is the empty set).
                                              
T𝑠 1 ; 𝑠 2 UE𝜒 ( 𝑗) ≜ T𝑠 1 UE𝜒 ( 𝑗) # J𝑠 2 KE𝜒 ⋓ T𝑠 2 UE𝜒 ( 𝑗)
T if(𝑒) 𝑠 1 else 𝑠 2 UE𝜒 ( 𝑗) ≜ T𝑠 1 UE𝜒 ( 𝑗) ⋓ T𝑠 2 UE𝜒 ( 𝑗)
𝑁 1𝑗 = (T𝑠 1 UE𝜒 ( 𝑗).( nrm) ∪ T𝑠 1 UE𝜒 ( 𝑗).( ctn))                𝑗
                                                                  𝑁 12 = 𝑁 1𝑗 ◦ J𝑠 2 KE𝜒 .( nrm)
Tloop 𝑠 1 𝑠 2 UE𝜒 ( 𝑗).( nrm) ≜ T𝑠 1 UE𝜒 ( 𝑗).( brk) ∪ 𝑁 1𝑗 ◦ J𝑠 2 KE𝜒 .( brk) ∪ 𝑁 12
                                                                                   𝑗
                                                                                      ◦ Jloop 𝑠 1 𝑠 2 KE𝜒 .( nrm) ∪
                                     T𝑠 2 UE𝜒 ( 𝑗).( brk) ∪ T𝑠 2 UE𝜒 ( 𝑗).( nrm) ◦ Jloop 𝑠 1 𝑠 2 KE𝜒 .( nrm)
                                                                                                                        
Tloop 𝑠 1 𝑠 2 UE𝜒 ( 𝑗).( err) ≜ T𝑠 1 UE𝜒 ( 𝑗).( err) ∪ 𝑁 1𝑗 ◦ ∇J𝑠 2 KE𝜒 .( ctn) ∪ (J𝑠 2 KE𝜒 # Jloop 𝑠 1 𝑠 2 KE𝜒 ).( err) ∪
                                                                                             
                                (∇T𝑠 2 UE𝜒 ( 𝑗).( ctn)) ∪ T𝑠 2 UE𝜒 ( 𝑗) # Jloop 𝑠 1 𝑠 2 KE𝜒 .( err)
Tloop 𝑠 1 𝑠 2 UE𝜒 ( 𝑗).( brk) = Tloop 𝑠 1 𝑠 2 UE𝜒 ( 𝑗).( ctn) ≜ ∅

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                                 5:23

                                                                                                    
Tloop 𝑠 1 𝑠 2 UE𝜒 ( 𝑗).( xxx) ≜ T𝑠 1 UE𝜒 ( 𝑗).( xxx) ∪ 𝑁 1𝑗 ◦ (J𝑠 2 KE𝜒 # Jloop 𝑠 1 𝑠 2 KE𝜒 ).( xxx) ∪
                                                                  
                                 T𝑠 2 UE𝜒 ( 𝑗) # Jloop 𝑠 1 𝑠 2 KE𝜒 .( xxx), for xxx ∈ { rtn, cll, gto, fin_dvg, inf_dvg }
TLSnilUE𝜒 ( 𝑗).( xxx) ≜ ∅, for xxx ∈ { nrm, brk, ctn, rtn, err, cll, gto, fin_dvg, inf_dvg }
              −−−−−−→                                 −−−−−−→            −−−−−−→
T(𝑛 1, 𝑠 1 ); (?𝑛 2, 𝑠 2 )UE𝜒 ( 𝑗) ≜ T𝑠 1 UE𝜒 ( 𝑗) # J (?𝑛 2, 𝑠 2 )KE𝜒 ⋓ T (?𝑛 2, 𝑠 2 )UE𝜒 ( 𝑗)
                −−−−−−−→                         −−−−−−−→                       −−−−−−−→
Tswitch 𝑒 (?𝑛𝑘 , 𝑠𝑘 )UE𝜒 ( 𝑗).( nrm) ≜ T (?𝑛𝑘 , 𝑠𝑘 )UE𝜒 ( 𝑗).( nrm) ∪ T (?𝑛𝑘 , 𝑠𝑘 )UE𝜒 ( 𝑗).( brk)
                −−−−−−−→
Tswitch 𝑒 (?𝑛𝑘 , 𝑠𝑘 )UE𝜒 ( 𝑗).( brk) ≜ ∅
                −−−−−−−→                         −−−−−−−→
Tswitch 𝑒 (?𝑛𝑘 , 𝑠𝑘 )UE𝜒 ( 𝑗).( xxx) ≜ T (?𝑛𝑘 , 𝑠𝑘 )UE𝜒 ( 𝑗).( xxx), xxx ∈ {ctn, rtn, err, cll, gto, fin_dvg, inf_dvg}
T𝑗 : 𝑠UE𝜒 ( 𝑗 ′ ) ≜ J𝑠KE𝜒        if 𝑗 ′ = 𝑗
T𝑗 : 𝑠UE𝜒 ( 𝑗 ′ ) ≜ T𝑠UE𝜒 ( 𝑗 ′ ) if 𝑗 ′ ≠ 𝑗
Otherwise (i.e., 𝑠 = skip | call ?𝑥 𝑒 1 →
                                        −
                                        𝑒 2 | 𝑥 = 𝑒 | break | continue | return ?𝑒 | goto 𝑗)
               T𝑠UE𝜒 ( 𝑗).( xxx) = ∅, for xxx ∈ { nrm, brk, ctn, rtn, err, cll, gto, fin_dvg, inf_dvg }
6.2.3 Intact semantics of Clight statements. We define the intact semantics of Clight statement
{{𝑠}}E𝜒 by composing the broken semantics J𝑠KE𝜒 and labeled broken semantics T𝑠UE𝜒 systematically.
To achieve this, we use ⟨T𝑠UE𝜒 ⟩ to denote the uncurried form of T𝑠UE𝜒 ( 𝑗), such that, for instance,

                  ⟨T𝑠UE𝜒 ⟩.( gto) ⊆ ( label × state) × trace × ( label × state)
                  T𝑠UE𝜒 ( 𝑗).( gto) ⊆ state × trace × ( label × state)
                                                                               
                  ⟨T𝑠UE𝜒 ⟩.( gto) ≜ ( 𝑗, 𝜎), 𝜏, ( 𝑗 ′, 𝜎 ′ ) | 𝜎, 𝜏, ( 𝑗 ′, 𝜎 ′ ) ∈ T𝑠UE𝜒 ( 𝑗).( gto))
The intact semantics of Clight statements are then defined by the following equations, where
labels_of (𝑠) denotes the set of statement labels that have appeared in 𝑠 in the form of “𝑗 : ...”.
                                                                                      
 {{𝑠}}E𝜒 .( xxx) ≜ J𝑠KE𝜒 .( xxx) ∪ J𝑠KE𝜒 .( gto) ◦ ⟨T𝑠UE𝜒 ⟩.( gto) ∗ ◦ ⟨T𝑠UE𝜒 ⟩.( xxx) , xxx ∈ {nrm, brk, ctn, rtn, cll}
                                                                                                                
 {{𝑠}}E𝜒 .( err) ≜ J𝑠KE𝜒 .( err) ∪ J𝑠KE𝜒 .( gto) ◦ ⟨T𝑠UE𝜒 ⟩.( gto) ∗ ◦ ⟨T𝑠UE𝜒 ⟩.( err) ∪ external_label (𝑠)
                   where external_label (𝑠) = { (( 𝑗, 𝜎), nil) | 𝑗 ∉ labels_of (𝑠) ∧ 𝜎 ∈ state }
{{𝑠}}E𝜒 .( fin_dvg) ≜
                                                                                                                
     J𝑠KE𝜒 .( fin_dvg) ∪ J𝑠KE𝜒 .( gto) ◦ ⟨T𝑠UE𝜒 ⟩.( gto) ∗ ◦       ⟨T𝑠UE𝜒 ⟩.( fin_dvg) ∪ (△⟨T𝑠UE𝜒 ⟩.( gto)) ∞
{{𝑠}}E𝜒 .( inf_dvg) ≜ let 𝐺 = ⟨T𝑠UE𝜒 ⟩.( gto) in
                                                             ∗                                                    ∞
      J𝑠KE𝜒 .( inf_dvg) ∪ J𝑠KE𝜒 .( gto) ◦       (△𝐺) ∗ ◦ ▲𝐺        ◦ (△𝐺) ∗ ◦ ⟨T𝑠UE𝜒 ⟩.( inf_dvg) ∪ (△𝐺) ∗ ◦ ▲𝐺

6.3    Denotational Semantics of Clight Functions
A Clight function 𝐹 is defined by Equation (10). We use J(𝑖𝑑 𝐹 , 𝐹 )Kg𝜒 (of FDenote) to denote the
semantics of the Clight function 𝐹 with the identifier 𝑖𝑑 𝐹 . This function-level semantics is parame-
terized by a global environment g and a semantic oracle 𝜒 (⊆ cquery × trace × creply) for specifying
the terminating behavior of the functions invoked by 𝐹 , and satisfies the following equations,
where function_entry intuitively represents the setup of a function’s internal initial state and local
environment at entry, while free_local_vars represents the release of its local resources at exit.
J(𝑖𝑑 𝐹 , 𝐹 )Kg𝜒 .( dom) ≜ { 𝑖𝑑 𝐹 } , i.e., the domain of 𝐹 is a singleton set with the unique element 𝑖𝑑 𝐹

      ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:24                                                                                                                          Z. Cheng et al.

                          
                                                         ∃e 𝜎, function_entry (g, 𝑚, 𝐹, 𝑣®) = Succeed(e, 𝜎)∧                                
                          
                                                                                                                                             
                                                                                                                                              
                          
                                                                                                                                             
                          
                                                                                                                                    rtn) ∨  
                                                                                                                                              
                                                                    ′                                   ′ ′                     E
             g                                    ′ ′
                                                               ∃𝜎     , E  =  (g,  e)  ∧    (𝜎,   𝜏,  𝜎   , 𝑣   )  ∈   {{𝑠 𝐹  }
                                                                                                                              } 𝜒 .(
J(𝑖𝑑 𝐹 , 𝐹 )K 𝜒 .( nrm) ≜ ((𝑖𝑑 𝐹 , 𝑣®, 𝑚), 𝜏, (𝑚 , 𝑣 ))
                          
                                                                         (𝜎, 𝜏, 𝜎 ) ∈ {{𝑠 𝐹 }} 𝜒 .( nrm) ∧ 𝑣 = Vundef ∧                     
                                                                                                                                             
                                                                                     ′               E                   ′               
                          
                                                                                                                                          ′ 
                                                                                                                                              
                                                                                                                                             
                                                                                                                                             
                                                                                                               ′
                                                                        free_local_vars           (g,   e,  𝜎    )  =   Succeed(𝑚           )
                          
                                                 (1)                      (g,           ®)  =  Fail     ∧        =        ;  or              
                                                                                                                                              
                                                                                                                                             
                                                      function_entry            𝑚,   𝐹, 𝑣                    𝜏        nil
                          
                                                                                                                                             
                          
                                                 (2) ∃e 𝜎, function_entry (g, 𝑚, 𝐹, 𝑣®) = Succeed(e, 𝜎) ∧                                   
                                                                                                                                              
                          
                                                                                                                                             
                                                                                                                                              
                          
                                                                                                                                             
                                                                                                                                              
                          
                                                             =    (g,     ∧   (𝜎, 𝜏)   ∈   {
                                                                                            {𝑠    }
                                                                                                  }  E
                                                                                                       .(       );   or                       
                                                                                                                                              
                                                                                                                                             
                                                            E           e)                                err
                                                                                                                                             
                                                                                               𝐹     𝜒
                          
                                                                                                                                             
                                                                                                                                              
                          
                          
                                                  (3) ∃e 𝜎, function_entry          (g,  𝑚,   𝐹, ®
                                                                                                 𝑣 )   =   Succeed(e,            𝜎)    ∧      
                                                                                                                                              
                          
                                                                                                                                             
                                                                                                                                              
                          
                          
                                                           ∃𝜎 ′
                                                                 , E  =  (g,  e)  ∧     (𝜎,  𝜏, 𝜎  ′
                                                                                                     ) ∈    {
                                                                                                            {𝑠   𝐹 }} E
                                                                                                                      𝜒 .( brk  )  ∨          
                                                                                                                                              
                                                                                                                                              
             g
J(𝑖𝑑 𝐹 , 𝐹 )K 𝜒 .( err) ≜ ((𝑖𝑑 𝐹 , 𝑣®, 𝑚), 𝜏)
                          
                                                                         (𝜎, 𝜏, 𝜎 ) ∈ {{𝑠 𝐹 }} 𝜒 .( ctn) ; or
                                                                                    ′                                                         
                                                                                                                                              
                                                                                                                                             
                                                                                                    E             
                          
                                                                                                                                             
                                                                                                                                              
                          
                                                                                                                                             
                                                                                                                                              
                          
                          
                                                  (4) ∃e 𝜎, function_entry          (g,  𝑚,   𝐹, ®
                                                                                                 𝑣 )   =   Succeed(e,            𝜎)    ∧      
                                                                                                                                              
                          
                                                                                                                                             
                                                                                                                                              
                          
                          
                                                               ′ ′                                     ′ ′
                                                                                                                                    rtn) ∨   
                                                                                                                                             
                                                                                                                               E
                                                            ∃𝜎    𝑣 ,     =  (g,       ∧   (𝜎,   𝜏,  𝜎  , 𝑣   )   ∈   {
                                                                                                                      {𝑠     }
                                                                                                                             }   .(
                                                                                                                                             
                                                                       E          e)                                      𝐹
                                                                                                                                             
                                                                                                                               𝜒
                          
                                                                     (𝜎, 𝜏, 𝜎 ) ∈ {{𝑠 𝐹 }} 𝜒 .( nrm) ∧ 𝑣 = Vundef ∧                         
                                                                                                                                             
                                                                                ′                                   ′
                                                                                                                                             
                                                                                               E                                     
                          
                                                                                                                                             
                                                                                                                                              
                                                                                                                                             
                                                                                                             ′
                                                                      free_local_vars (g, e, 𝜎 ) = Fail
                          (                                                                                                            )
                                                  ∃e 𝜎, function_entry (g, 𝑚, 𝐹, 𝑣®) = Succeed(e, 𝜎) ∧
J(𝑖𝑑 𝐹 , 𝐹 )Kg𝜒 .( cll) ≜   (𝑖𝑑 𝐹 , 𝑣®, 𝑚), 𝜏, 𝑞
                                                          E = (g, e) ∧ (𝜎, 𝜏, 𝑞) ∈ {{𝑠 𝐹 }}E𝜒 .( cll)
                          (                                                                                                            )
             g                                  ∃e 𝜎, function_entry (g, 𝑚, 𝐹, 𝑣®) = Succeed(e, 𝜎) ∧
J(𝑖𝑑 𝐹 , 𝐹 )K 𝜒 .( xxx) ≜    (𝑖𝑑 𝐹 , 𝑣®, 𝑚), 𝜏
                                                          E = (g, e) ∧ (𝜎, 𝜏) ∈ {{𝑠 𝐹 }}E𝜒 .( xxx)

where xxx ∈ { fin_dvg, inf_dvg }. It is worth noting that the aborting behavior J(𝑖𝑑 𝐹 , 𝐹 )Kg𝜒 .( err)
accounts for four possible cases: (1) abnormal initialization at function entry; (2) abnormal execution
within the function body; (3) premature exit of the function body via break or continue; (4)
abnormal deallocation of local variables at function exit. Besides, aborting and diverging behaviors
of a function do not include those of its callees. Instead, we record the function’s call behavior
explicitly, so that such cases can be handled later when defining the semantics of open modules.

6.4     Semantics of Open Modules
  Definition of open module. An open module is modeled as a collection of Clight functions, i.e.,
𝑀 ≜ (𝑖𝑑 1, 𝐹 1 ); ...; (𝑖𝑑𝑛 , 𝐹𝑛 ). Each 𝐹𝑖 may call functions internal or external to module 𝑀 (i.e., open).
  Semantic notations. We use J𝑀Kg𝜒 (of FDenote) to denote the semantics of open Clight modules,
where the parameter g denotes a global environment, and 𝜒 (⊆ cquery × trace × creply) is a semantic
oracle for specifying the terminating behavior of functions external to module 𝑀.
  Before showing the semantic equations, we overload the symbol “⋓” to denote the union of
function-level denotations, and define L𝑀Mg𝜒 to represent the combined denotation of all functions
defined in 𝑀. Formally, given function-level denotations 𝐷 1 and 𝐷 2 of FDenote, we have:
          (𝐷 1 ⋓ 𝐷 2 ).( xxx) ≜ 𝐷 1 .( xxx) ∪ 𝐷 2 .( xxx), for xxx ∈ { dom, nrm, err, cll, fin_dvg, inf_dvg }                             (28)
          L𝑀Mg𝜒 ≜ J(𝑖𝑑 1, 𝐹 1 )Kg𝜒 ⋓ · · · ⋓ J(𝑖𝑑𝑛 , 𝐹𝑛 )Kg𝜒 , where 𝑀 = (𝑖𝑑 1, 𝐹 1 ); ...; (𝑖𝑑𝑛 , 𝐹𝑛 )                                   (29)
   Semantic equations. The semantics of open Clight modules then satisfies the following equations:
       J𝑀Kg𝜒 .( dom) ≜ L𝑀Mg𝜒 .( dom)

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                             5:25


      J𝑀Kg𝜒 .( nrm) ≜ 𝜇 𝜒 0 .L𝑀Mg𝜒0 ∪𝜒 .( nrm)
      J𝑀Kg𝜒 .( err) ≜ L𝑀Mg𝜒ˆ .( cll) ∗ ◦ L𝑀Mg𝜒ˆ .( err)
      ExtnlQuery (𝑋 ) ≜ {(𝑖𝑑, 𝑣®, 𝑚) | 𝑖𝑑 ∉ 𝑋 } for 𝑋 ⊆ ident
                                                                                 
      J𝑀Kg𝜒 .( cll) ≜ L𝑀Mg𝜒ˆ .( cll) + ◦ test ExtnlQuery (L𝑀Mg𝜒 .( dom))
      J𝑀Kg𝜒 .( fin_dvg) ≜ L𝑀Mg𝜒ˆ .( cll) ∗ ◦ L𝑀Mg𝜒ˆ .( fin_dvg) ∪ (△L𝑀Mg𝜒ˆ .( cll)) ∞
                                                                 ∗
      J𝑀Kg𝜒 .( inf_dvg) ≜ (△L𝑀Mg𝜒ˆ .( cll)) ∗ ◦ ▲L𝑀Mg𝜒ˆ .( cll) ◦ (△L𝑀Mg𝜒ˆ .( cll)) ∗ ◦ L𝑀Mg𝜒ˆ .( inf_dvg) ∪
                                                                 ∞
                           (△L𝑀Mg𝜒ˆ .( cll)) ∗ ◦ ▲L𝑀Mg𝜒ˆ .( cll) , where 𝜒ˆ = J𝑀Kg𝜒 .( nrm) ∪ 𝜒
Here, the set ExtnlQuery (𝑋 ) denote the set of external queries w.r.t. the given identifier set 𝑋 , so as
to capture calls to functions outside the module. Besides, once the normal semantics J𝑀Kg𝜒 .( nrm)
is defined, we extend the oracle 𝜒 (specifying the terminating behavior of external functions) to
𝜒ˆ = J𝑀Kg𝜒 .( nrm) ∪ 𝜒 so as to cover the terminating behavior of both internal and external functions.

6.5    Semantic Linking
We use (J𝑀1 K ⊕ J𝑀2 K) g𝜒 to denote the semantic linking of two open Clight modules, where g is
the same global environment, and the semantic oracle 𝜒 (⊆ cquery × trace × creply) specifies the
terminating behavior of function calls external to modules 𝑀1 and 𝑀2 . Intuitively, semantic linking
merges the domains and behaviors of the two modules while continuing to rely on the oracle 𝜒 for
any calls external to both. The denotation of semantic linking satisfies the following equations:
 (J𝑀1 K ⊕ J𝑀2 K) g𝜒 .(dom) ≜ J𝑀1 Kg𝜒 .( dom) ∪ J𝑀2 Kg𝜒 .( dom)
                                                                                 
 (J𝑀1 K ⊕ J𝑀2 K) g𝜒 .(nrm) ≜ 𝜇 𝜒 0 . J𝑀1 Kg𝜒0 ∪𝜒 .( nrm) ∪ J𝑀2 Kg𝜒0 ∪𝜒 .( nrm)
 (J𝑀1 K ⊕ J𝑀2 K) g𝜒 .(err) ≜ (J𝑀1 K ⋓ J𝑀2 K) g𝜒˜ .(cll)∗ ◦ (J𝑀1 K ⋓ J𝑀2 K) g𝜒˜ .(err)
                                                                                                             
 (J𝑀1 K ⊕ J𝑀2 K) g𝜒 .(cll) ≜ (J𝑀1 K ⋓ J𝑀2 K) g𝜒˜ .(cll)+ ◦ test ExtnlQuery J𝑀1 Kg𝜒 .( dom) ∪ J𝑀2 Kg𝜒 .( dom)
                                                                                                   ∞
 (J𝑀1 K ⊕ J𝑀2 K) g𝜒 .(fin_dvg) ≜ (J𝑀1 K ⋓ J𝑀2 K) g𝜒˜ .(cll)∗ ◦ (J𝑀1 K ⋓ J𝑀2 K) g𝜒˜ .(fin_dvg) ∪ △𝐶
                                                  ∗                                                            ∞
 (J𝑀1 K ⊕ J𝑀2 K) g𝜒 .(inf_dvg) ≜ (△𝐶) ∗ ◦ ▲𝐶 ◦ (△𝐶) ∗ ◦ (J𝑀1 K ⋓ J𝑀2 K) g𝜒˜ .(inf_dvg) ∪ (△𝐶) ∗ ◦ ▲𝐶
                                      where 𝐶 = (J𝑀1 K ⋓ J𝑀2 K) g𝜒˜ .(cll), and 𝜒˜ = (J𝑀1 K ⊕ J𝑀2 K) g𝜒 .(nrm) ∪ 𝜒

     Theorem 6.1 (Semantic adeqacy). For any Clight modules 𝑀1 and 𝑀2 , J𝑀1 K⊕J𝑀2 K = J𝑀1 +𝑀2 K.

6.6    Csharpminor and Cminor
   Syntax of Csharpminor. Csharpminor is an untyped low-level imperative language featured with
infinite loops, control flow blocks, and premature exits from blocks, which are defined as follows.
  (Statements) 𝑢 ≜ skip | 𝑢 ; 𝑢 | if(𝑒) 𝑢 else 𝑢 | call ?𝑥 𝑒 →
                                       1   2          1
                                                                 −
                                                                 𝑒 : 𝑠𝑖𝑔 | goto 𝑗 | 𝑗 : 𝑢 | 𝑥 = 𝑒 |
                                                                 2               1   2
                                                                              −−−−−−−→
                         loop 𝑢 | block{𝑢} | exit(𝑛) | return ?𝑒 | switch 𝑏 𝑒 (?𝑛𝑘 , 𝑢𝑘 ) | ...
  (Functions)        𝐹 ≜ (→
                          𝑥− , →
                              𝑘𝑦− , →
                                  𝑘 𝑧− , 𝑢 , 𝑠𝑖𝑔)
                                       𝑘   𝐹

A Csharpminor function 𝐹 is composed of a list of parameter names →    𝑥−𝑘 , a list of temporary variables
→
−                              →
                               −
𝑥𝑘 , a list of local variables 𝑧𝑘 (whose addresses are taken in 𝐹 ), a statement 𝑢 𝐹 representing the
function body, and a signature 𝑠𝑖𝑔 specifying the types of the arguments and return value of 𝐹 .
   Syntax of Cminor. Cminor functions is defined by the parameter list →     𝑥−𝑘 , the temporary variables
→
−
𝑥 , the size of memory block for stack space 𝑠𝑡𝑎𝑐𝑘𝑠𝑖𝑧𝑒, the function body 𝑡 , and the signature of 𝐹 .
 𝑘                                                                                       𝐹


      ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:26                                                                                                   Z. Cheng et al.


                           Table 3. Semantic notation for Csharpminor and Cminor.

                 Language             Symbol    Denotation       Environment        Program state
                  Csharpminor          J𝑢KE𝜒    Cshm.Denote      E = (g, e)         𝜎 = (𝑡𝑒, 𝑚)
                  Cminor               J𝑡KE𝜒    Cmin.Denote      E = (g, 𝑠𝑝)        𝜎 = (𝑡𝑒, 𝑚)


In Cminor, Csharpminor local variables become sub-blocks of the Cminor stack memory block.

   (Statements)       𝑡 ≜ skip | 𝑡 1 ; 𝑡 2 | if(𝑒) 𝑡 1 else 𝑡 2 | call ?𝑥 𝑒 1 →
                                                                              −
                                                                              𝑒 2 : 𝑠𝑖𝑔 | goto 𝑗 | 𝑗 : 𝑡 | 𝑥 = 𝑒 |
                          loop 𝑡 | block{𝑡 } | exit(𝑛) | return ?𝑒 | switch 𝑏 𝑒 𝑡𝑎𝑏𝑙𝑒 𝑑𝑒𝑓𝑎𝑢𝑙𝑡 | ...
   (Functions)        𝐹 ≜ (→
                           𝑥− , →
                              𝑘 𝑦− , 𝑠𝑡𝑎𝑐𝑘𝑠𝑖𝑧𝑒, 𝑡 , 𝑠𝑖𝑔)
                                  𝑘              𝐹

  Semantic domain. Csharpminor and Cminor enjoy the same form of signatures for statement
denotations, since they adopt the same block-exit mechanism to model structured control flow.
       Record Cshm/Cmin.Denote: Type := {
          nrm: state → trace → state → Prop;           (* nrm ⊆ state × trace × state ---------- *)
          blk: nat → state → trace → state → Prop;     (* blk ⊆ nat × state × trace × state ----*)
          rtn: state → trace → state → val → Prop;     (* rtn ⊆ state × trace × state × val ----*)
          err: state → trace → Prop;                   (* err ⊆ state × trace -------------------*)
          cll: state → trace → cquery → Prop;          (* cll ⊆ state × trace × cquery --------- *)
          gto: state → trace → (label × state) → Prop; (* gto ⊆ state × trace × (label × state) *)
          fin_dvg: state → trace → Prop;               (* fin_dvg ⊆ state × trace ---------------*)
          inf_dvg: state → itrace → Prop               (* inf_dvg ⊆ state × itrace --------------*)
       }.

   The main difference between Cshm/Cmin.Denote and Clit.Denote lies in how they handle structured
control flow. While Clit.Denote uses brk and ctn, Cshm/Cmin.Denote instead employs blk; the meanings
of the other sets remain the same as in Clight. The semantic infrastructure (i.e., states, queries, and
replies) of Csharpminor and Cminor builds the same with that of Clight, as summarized in Table 1.
   The Cminorgen phase translates Csharpminor to Cminor, where CompCert coalesces the separate
memory blocks allocated to local variables into a single block that represents the activation record
as a whole. We write J𝑢KE𝜒 for the semantics of Csharpminor statements, where E = (g, e); and
write J𝑡KE𝜒 for that of Cminor statements, where E = (g, 𝑠𝑝) with 𝑠𝑝 denoting the stack pointer, as
shown in Table 3. Other notations (i.e., 𝜒, g, and e) carry the same meaning as in Clight.
   The function-level denotational semantics of Csharpminor and Cminor, including those for
functions, open modules, and semantic linking, are defined in the same way as in Clight.

7 Behavior Refinement
Compilation correctness is ubiquitously formulated as a behavior refinement relation, which
ensures that every behavior exhibited by the target program is one possible behavior of the source.
As previously discussed, we define the semantics of program statements, procedures, and open
modules through a series of behavior sets, using extended KATs and suitable fixed-point theorems.
The highlight of our theoretical contribution is proposing a novel algebraic structure to unify
various behavior refinements between different behavior sets. In this section, we begin with typical
examples of behavior refinement in §7.1, and then propose the novel refinement algebra in §7.2∼§7.4.
We define Kripke relations for Cminorgen in §7.5, and finally explain our design choices in §7.6

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                                   5:27


7.1     Examples of Behavior Refinement
   Example 7.1 (Behavior refinement for a simple transformation). Consider a simple transforma-
tion that converts a WHILE program 𝑐 into another WHILE program T (𝑐) with sequenced skip
statements removed. Because how states are represented before and after the transformation is
unchanged, we can use the set inclusion relation to define the behavior refinement between the
programs before and after transformation, i.e.,
                  JT (𝑐)K ⊑ J𝑐K ≜ JT (𝑐)K.( nrm) ⊆ J𝑐K.( nrm) and JT (𝑐)K.( dvg) ⊆ J𝑐K.( dvg)                         (30)
For the transformation of type-safe and nondeterministic WHILE programs, the behavior refinement
implies that compiler correctness allows the compiled program to exhibit fewer normal termination
possibilities and fewer divergence possibilities. In other words, if the target program terminates
normally, the source program must also be able to terminate normally; if the target program diverges,
the source program must have a behavior that can diverge. The transformation correctness is then
compositional in terms of sequential statements, in the sense that, for any 𝑐 1 and 𝑐 2 ,
                   if JT (𝑐 1 )K ⊑ J𝑐 1 K and JT (𝑐 2 )K ⊑ J𝑐 2 K, then JT (𝑐 1 ); T (𝑐 2 )K ⊑ J𝑐 1 ; 𝑐 2 K.          (31)
Its proof follows from the monotonicity of the composition and set union w.r.t. the set inclusion:
      JT (𝑐 1 ); T (𝑐 2 )K.(nrm) = JT (𝑐 1 )K.(nrm) ◦ JT (𝑐 2 )K.(nrm) ⊆ J𝑐 1 K.(nrm) ◦ J𝑐 2 K.(nrm) = J𝑐 1 ; 𝑐 2 K.(nrm)
                                                                                              
      JT (𝑐 1 ); T (𝑐 2 )K.(dvg) = JT (𝑐 1 )K.(dvg) ∪ JT (𝑐 1 )K.(nrm) ◦ JT (𝑐 2 )K.(dvg)
                                                                             
                                 ⊆ J𝑐 1 K.(dvg) ∪ J𝑐 1 K.(nrm) ◦ J𝑐 2 K.(dvg) = J𝑐 1 ; 𝑐 2 K.(dvg)                        □
The transformation correctness of while loops is compositional as well, in the sense that, for any 𝑐,
                         if JT (𝑐)K ⊑ J𝑐K, then Jwhile 𝑏 do T (𝑐)K ⊑ Jwhile 𝑏 do 𝑐K                                   (32)
Its proof similarly follows from the monotonicity of operators ◦, ∪, ∗ , and ∞ w.r.t. the set inclusion.
                                                              ∗
  Jwhile 𝑏 do T (𝑐)K.(nrm) = test(J𝑏K.(tts)) ◦ JT (𝑐)K.( nrm) ◦ test(J𝑏K.(ffs))
                                                           ∗
                             ⊆ test(J𝑏K.(tts)) ◦ J𝑐K.( nrm) ◦ test(J𝑏K.(ffs))
                                   = Jwhile 𝑏 do 𝑐K.(nrm)
                                                                             ∗                                        
  Jwhile 𝑏 do T (𝑐)K.(dvg) = test(J𝑏K.(tts)) ◦ JT (𝑐)K.( nrm)          ◦ test(J𝑏K.(tts)) ◦ JT (𝑐)K.( dvg)
                                                                        ∞
                                     ∪ test(J𝑏K.(tts)) ◦ JT (𝑐)K.( nrm)
                                                                 ∗                              
                                   ⊆ test(J𝑏K.(tts)) ◦ J𝑐K.( nrm) ◦ test(J𝑏K.(tts)) ◦ J𝑐K.( dvg)
                                                                    ∞
                                     ∪ test(J𝑏K.(tts)) ◦ J𝑐K.( nrm)
                                   = Jwhile 𝑏 do 𝑐K.(dvg)                                                                  □
   Example 7.2. To take abortion into account, we extend the WHILE language to WHILEE, which
is identical to WHILE except that it is not type-safe. In other words, WHILEE programs may abort
(e.g., division by zero). We then use the following signature to capture WHILEE’s program behavior:
      Record EDenote: Type := {
         nrm: state → state → Prop;               (* nrm ⊆ state × state *)
         err: state → Prop;                       (* err ⊆ state *)
         dvg: state → Prop                        (* dvg ⊆ state *)
      }.

To allow for more flexible optimization, modern compilers usually do not guarantee behavioral
consistency for programs with undefined behavior. That is, if the source program could abort, the
compiled program may either terminate normally, diverge, or abort as well. In such cases, behavior

      ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:28                                                                                                  Z. Cheng et al.


refinement JT (𝑐)K ⊑ J𝑐K (still consider the simple transformation in Example 7.1) can be redefined
as follows, where J𝑐K.(err) (⊆ state) denotes potential aborting behaviors of program 𝑐.
                                  
                                   JT (𝑐)K.(nrm) ⊆ J𝑐K.(nrm) ∪ (J𝑐K.(err) × state) and
                                  
                                  
                                  
                   JT (𝑐)K ⊑ J𝑐K ≜ JT (𝑐)K.(dvg) ⊆ J𝑐K.(dvg) ∪ J𝑐K.(err) and                                      (33)
                                  
                                  
                                   JT (𝑐)K.(err) ⊆ J𝑐K.(err)
                                  
The transformation correctness of sequential statements like Formula (31) can be proved as follows.
 JT (𝑐 1 ); T (𝑐 2 )K.(nrm) = JT (𝑐 1 )K.(nrm) ◦ JT (𝑐 2 )K.(nrm)                                                 (34)
                                                                                         
        ⊆ J𝑐 1 K.(nrm) ∪ (J𝑐 1 K.(err) × state) ◦ J𝑐 2 K.(nrm) ∪ (J𝑐 2 K.(err) × state)                           (35)
                                                                                                      
        ⊆ J𝑐 1 K.(nrm) ◦ J𝑐 2 K.(nrm) ∪ (J𝑐 1 K.(err) × state) ∪ J𝑐 1 K.(nrm) ◦ (J𝑐 2 K.(err) × state)            (36)
                                                                                           
        ⊆ J𝑐 1 K.(nrm) ◦ J𝑐 2 K.(nrm) ∪ J𝑐 1 K.(err) ∪ (J𝑐 1 K.(nrm) ◦ J𝑐 2 K.(err)) × state                      (37)
        = J𝑐 1 ; 𝑐 2 K.(nrm) ∪ (J𝑐 1 ; 𝑐 2 K.(err) × state)
                                                                                     
 JT (𝑐 1 ); T (𝑐 2 )K.(dvg) = JT (𝑐 1 )K.(dvg) ∪ JT (𝑐 1 )K.(nrm) ◦ JT (𝑐 2 )K.(dvg)                         (38)
                                                                                                         
        ⊆ J𝑐 1 K.(dvg) ∪ J𝑐 1 K.(err) ∪ J𝑐 1 K.(nrm) ∪ (J𝑐 1 K.(err) × state) ◦ J𝑐 2 K.(dvg) ∪ J𝑐 2 K.(err) (39)
                                                                                                   
        ⊆ J𝑐 1 K.(dvg) ∪ J𝑐 1 K.(nrm) ◦ J𝑐 2 K.(dvg) ∪ J𝑐 1 K.(err) ∪ (J𝑐 1 K.(nrm) ◦ J𝑐 2 K.(err))          (40)
        = J𝑐 1 ; 𝑐 2 K.(dvg) ∪ J𝑐 1 ; 𝑐 2 K.(err)
                                                                                       
 JT (𝑐 1 ); T (𝑐 2 )K.(err) = JT (𝑐 1 )K.(err) ∪ JT (𝑐 1 )K.(nrm) ◦ JT (𝑐 2 )K.(err)                              (41)
                                                                  
        ⊆ J𝑐 1 K.(err) ∪ J𝑐 1 K.(nrm) ∪ (J𝑐 1 K.(err) × state) ◦ J𝑐 2 K.(err)                                     (42)
                                                    
        ⊆ J𝑐 1 K.(err) ∪ J𝑐 1 K.(nrm) ◦ J𝑐 2 K.(err) = J𝑐 1 ; 𝑐 2 K.(err)                                           □
   Summary of existing proof system. In the preceding examples, we showed by hand how relational
Kleene algebra can be used to verify the correctness of simple program transformations. This
style of reasoning is supported by a well-developed proof system: the equational theory of Kleene
algebra with tests (KAT). Beyond such manual reasoning, a rich body of research has developed
automated proof techniques for regular expressions, relation algebra, and KAT. Classic approaches
build on the notion of derivatives [Brzozowski 1964], which enable the construction of automata
directly from algebraic expressions. This idea has been extended to mechanized proofs of regular
expression equivalence in Isabelle/HOL [Krauss and Nipkow 2012], decision procedures for (in-
)equivalence of regular expressions in Rocq [Moreira et al. 2012], Rocq tools for KAT applied
to while programs [Pous 2013], unified decision procedures for regular expression equivalence
[Nipkow and Traytel 2014], and symbolic algorithms for language equivalence and KAT [Pous
2015]. Together, these advances demonstrate the maturity of automated algebraic reasoning about
relational (in-)equations.
   Challenges for realistic compiler verification. Despite the expressiveness of relational Kleene
algebra and the maturity of its automated reasoning, directly applying these techniques to realistic
compiler verification remains challenging. Existing methods focus primarily on equational reasoning
over algebraic structures, whereas compiler correctness demands reasoning about simulation
relations between source and target programs. In other words, the correctness of a compiler often
cannot be expressed simply in terms of set inclusion between source and target denotations. Instead,
one must account for changes in state representations across abstraction layers—most notably the
transformation of memory models—so that correctness is proved not by inclusion alone but by
carefully designed state-matching relations. We illustrate this point with the following examples.

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                                   5:29


                  𝜏                              𝜏0                       𝜏                             𝜏0
         𝜎𝑠               𝜎𝑠′        𝜎𝑠                           𝜎𝑠               ∞        𝜎𝑠
              J𝑠K.(nrm)                       J𝑠K.(err)                J𝑠K.(xxx)                     J𝑠K.(err)
        𝑅                 𝑅     or        𝑅           𝜏0 ⩽𝑇 𝜏   𝑅                      or        𝑅           𝜏0 ⩽𝑇 𝜏

                  𝜏                               𝜏                       𝜏                             𝜏
         𝜎𝑡               𝜎𝑡′        𝜎𝑡                   𝜎𝑡′     𝜎𝑡               ∞        𝜎𝑡                   ∞
              J𝑡K.(nrm)                       J𝑡K.(nrm)                J𝑡K.(xxx)                     J𝑡K.(xxx)

        (a) Refinement of terminating behavior                    (b) Refinement of diverging behavior

Fig. 7. Behavior refinement of termination and divergence for CompCert, where xxx ∈ { fin_dvg, inf_dvg }.


  Before showing general definitions, we first consider the compilation correctness of Cshmgen.
   Example 7.3 (Behavior refinement for Cshmgen of CompCert). Cshmgen is mainly responsible
for translating structured C control flow into simpler primitives and erasing Clight types. In this
process, the representation of program states remains unchanged. Suppose that a Clight statement 𝑠
is transformed to Csharpminor by Cshmgen, we can then define the behavior refinement J𝑡K ­ J𝑠K:
                                                                                                       
     ∀𝜎 𝜏 𝜎 ′, (𝜎, 𝜏, 𝜎 ′ ) ∈ J𝑡K.(nrm) ⇒ (𝜎, 𝜏, 𝜎 ′ ) ∈ J𝑠K.(nrm) ∨ ∃𝜏0, (𝜎, 𝜏0 ) ∈ J𝑠K.(err) ∧ 𝜏0 ⩽𝑇 𝜏 ;
                                                                      
     ∀𝜎 𝜏, (𝜎, 𝜏) ∈ J𝑡K.(err) ⇒ ∃𝜏0, (𝜎, 𝜏0 ) ∈ J𝑠K.(err) ∧ 𝜏0 ⩽𝑇 𝜏 ;
                                                                                                     
     ∀𝜎 𝜏, (𝜎, 𝜏) ∈ J𝑡K.(fin_dvg) ⇒ (𝜎, 𝜏) ∈ J𝑠K.(fin_dvg) ∨ ∃𝜏0, (𝜎, 𝜏0 ) ∈ J𝑠K.(err) ∧ 𝜏0 ⩽𝑇 𝜏 ;
                                                                                                     
     ∀𝜎 𝜏, (𝜎, 𝜏) ∈ J𝑡K.(inf_dvg) ⇒ (𝜎, 𝜏) ∈ J𝑠K.(inf_dvg) ∨ ∃𝜏0, (𝜎, 𝜏0 ) ∈ J𝑠K.(err) ∧ 𝜏0 ⩽𝑇 𝜏 .
where 𝜏0 ⩽𝑇 𝜏 means that 𝜏0 is the prefix of 𝜏. This example illustrates the way how observable
event traces are preserved for realistic compilation, especially when undefined behaviors (UB) are
raised in the source program, which conforms to CompCert’s prefix-preserving view of UB.
  We now generalize the above definition to capture the correctness of more complex phases of
CompCert, where source and target program states may differ in representation and are related
through a state-matching relation. The following example illustrates this generalization.
  Example 7.4 (Behavior refinement for general phases of CompCert). Suppose that a compilation
phase of CompCert transforms a source statement 𝑠 into the target statement 𝑡. For a given state-
matching relation 𝑅, we define their behavior refinement, denoted by J𝑡K ­𝑅 J𝑠K, as follows:
     ∀𝜎𝑡 𝜏 𝜎𝑡′ 𝜎𝑠 , (𝜎𝑡 , 𝜏, 𝜎𝑡′ ) ∈ J𝑡K.(nrm) ⇒ (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅 ⇒
                                                                                                          
                 ∃𝜎𝑠′, (𝜎𝑠 , 𝜏, 𝜎𝑠′ ) ∈ J𝑠K.(nrm) ∧ (𝜎𝑠′, 𝜎𝑡′ ) ∈ 𝑅 ∨ ∃𝜏0, (𝜎𝑠 , 𝜏0 ) ∈ J𝑠K.(err) ∧ 𝜏0 ⩽𝑇 𝜏 ;
                                                                                                    
     ∀𝜎𝑡 𝜏 𝜎𝑠 , (𝜎𝑡 , 𝜏) ∈ J𝑡K.(err) ⇒ (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅 ⇒ ∃𝜏0, (𝜎𝑠 , 𝜏0 ) ∈ J𝑠K.(err) ∧ 𝜏0 ⩽𝑇 𝜏 ;
     ∀𝜎𝑡 𝜏 𝜎𝑠 , (𝜎𝑡 , 𝜏) ∈ J𝑡K.(fin_dvg) ⇒ (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅 ⇒
                                                                                
                (𝜎𝑠 , 𝜏) ∈ J𝑠K.(fin_dvg) ∨ ∃𝜏0, (𝜎𝑠 , 𝜏0 ) ∈ J𝑠K.(err) ∧ 𝜏0 ⩽𝑇 𝜏 ;
     ∀𝜎𝑡 𝜏 𝜎𝑠 , (𝜎𝑡 , 𝜏) ∈ J𝑡K.(inf_dvg) ⇒ (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅 ⇒
                                                                                       
                (𝜎𝑠 , 𝜏) ∈ J𝑠K.(inf_dvg) ∨ ∃𝜏0, (𝜎𝑠 , 𝜏0 ) ∈ J𝑠K.(err) ∧ 𝜏0 ⩽𝑇 𝜏
Fig. 7 illustrates behavior refinement for both terminating and diverging executions. It states that
for every terminating (resp. diverging) behavior of the target program, either there may exist
consistent terminating (resp. diverging) behavior in the source end, or the source program may
abort (denoted as ) prematurely. Once the source program may abort, the compiled target program
could do anything unpredictable. Furthermore, though not depicted in Fig. 7, the definition also
requires that if the target program may abort, then the corresponding source program may abort as

     ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:30                                                                                                     Z. Cheng et al.


well. This rules out compilers that intend to translate a safe program into one that may aborts. It is
also worth noting that refinement between behavior sets entails refinement between the triggered
observable behaviors, thereby demonstrating the same compilation correctness as in CompCert.
   Besides, the correctness of each compilation phase can be proved with different state-matching
relations and can be vertically composed to form end-to-end correctness of the whole compiler.
This is demonstrated by the following theorem, where 𝐿1, 𝐿2 and 𝐿3 are the semantics of statements.
   Theorem 7.5. For any matching relations 𝑅1 and 𝑅2 , if 𝐿3 ­𝑅2 𝐿2 and 𝐿2 ­𝑅1 𝐿1 , then 𝐿3 ­𝑅2 ◦𝑅1 𝐿1 .
   However, the behavior refinement defined in Example 7.4 is inherently limited to closed settings,
i.e., the verification of whole-program compilation, as is the case for the original CompCert9 .
   Toward verified compositional compilation (VCC). Verified compositional compilation requires
two dimensions of compositionality in open settings: (i) horizontal compositionality requires that the
compilation correctness of individual modules can be composed to obtain compilation correctness of
the linked whole program; (ii) vertical compositionality demands that correctness of each compilation
phase can be composed to yield an end-to-end correctness across the compilation chain.
   Several works stemming from CompCert have moved in this direction. Early attempts such as
CompComp [Stewart et al. 2015] and CompCertM [Song et al. 2020] extend CompCert with interac-
tion semantics [Beringer et al. 2014] and employ open simulations to prove compilation correctness
of open modules. More recent developments, notably CompCertO [Koenig and Shao 2021] and
the work of Zhang et al. [2024], introduce Kripke logical relations to express the correspondence
between open module interactions. We will return to these developments in more detail later.
   To support VCC in our denotation-based framework, we leverage the notion of Kripke relations
and the Kripke interface relations (also called simulation conventions) from CompCertO. We
formulate the denotation-based behavior refinement for open functions and modules as follows.
  Definition 7.6 (Kripke relations). Given sets 𝐴1 , 𝐴2 , and 𝑊 , a Kripke relation 𝑅 : 𝑊 → {𝑋 | 𝑋 ⊆
𝐴1 × 𝐴2 } is a family of relations indexed by the set of Kripke worlds 𝑊 , written as 𝑅 : K𝑊 (𝐴1, 𝐴2 ).
   Kripke interface relations (KIR) are used to relate the source and target language interfaces.
   Definition 7.7 (Kripke interface relations, or KIR). A Kripke interface relation between two
language interfaces ⟨query1, reply1 ⟩ and ⟨query2, reply2 ⟩ is a tuple 𝐵 = ⟨𝑊𝐵 , {𝐵 , 𝑅𝐵 , 𝑅𝐵𝑟 ⟩, where
                                                                                           𝑞

{𝐵 (⊆ 𝑊𝐵 × 𝑊𝐵 ) is an accessibility relation between worlds, and 𝑅𝐵 : K𝑊𝐵 ( query1, query2 ) and
                                                                            𝑞

𝑅𝐵𝑟 : K𝑊𝐵 ( reply1, reply2 ) are Kripke relations used for relating queries and replies, respectively.
  According to CompCertO [Koenig and Shao 2021], Kripke interface relations can be vertically com-
posed as follows: given Kripke interface relations 𝐴 = ⟨𝑊𝐴 , {𝐴 , 𝑅𝐴 , 𝑅𝐴𝑟 ⟩ and 𝐵 = ⟨𝑊𝐵 , {𝐵 , 𝑅𝐵 , 𝑅𝐵𝑟 ⟩,
                                                                   𝑞                             𝑞

𝐴•𝐵 ≜ ⟨𝑊𝐴 × 𝑊𝐵 , {𝐴𝐵 , 𝑅𝐴 • 𝑅𝐵 , 𝑅𝐴 • 𝑅𝐵 ⟩, where for any worlds 𝑤 𝐴 , 𝑤 𝐴 ∈ 𝑊𝐴 , and 𝑤 𝐵 , 𝑤 𝐵 ∈ 𝑊𝐵 ,
                          𝑞    𝑞 𝑟      𝑟                                   ′                  ′


                          (𝑤 𝐴 , 𝑤 𝐵 ) {𝐴𝐵 (𝑤 𝐴′ , 𝑤 𝐵′ ) ⇔ 𝑤 𝐴 {𝐴 𝑤 𝐴′ ∧ 𝑤 𝐵 {𝐵 𝑤 𝐵′ ;
         𝑅𝐴 • 𝑅𝐵 (𝑤 𝐴 , 𝑤 𝐵 ) ≜ 𝑅𝐴 (𝑤 𝐴 ) ◦ 𝑅𝐵 (𝑤 𝐵 ); and 𝑅𝐴𝑟 • 𝑅𝐵𝑟 (𝑤 𝐴 , 𝑤 𝐵 ) ≜ 𝑅𝐴𝑟 (𝑤 𝐴 ) ◦ 𝑅𝐵𝑟 (𝑤 𝐵 ).
           𝑞     𝑞                 𝑞            𝑞


   Example 7.8 (Behavior refinement for open functions/modules of CompCert). Suppose that a source
open module 𝑀𝑠 is transformed to a target module 𝑀𝑡 . We use semantic oracles 𝜒𝑠 (⊆ query𝑠 × trace ×
reply𝑠 ) and 𝜒𝑡 (⊆ query𝑡 × trace × reply𝑡 ) to specify the terminating behavior of invoked functions
external to the source module 𝑀𝑠 and functions external to the target module 𝑀𝑡 respectively.
Additionally, we use a semantic oracle 𝜒𝑒 (⊆ query𝑠 × trace) to specify the aborting behavior of

9 Extended by Kang et al. [2016], CompCert supports verified separate compilation by the same compiler from version 2.7.



ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                                  5:31


functions external to the source module 𝑀𝑠 . Given a KIR 𝐴 = ⟨𝑊𝐴 , {𝐴 , 𝑅𝐴 , 𝑅𝐴𝑟 ⟩ between languages
                                                                                         𝑞

interfaces ⟨query𝑠 , reply𝑠 ⟩ and ⟨query𝑡 , reply𝑡 ⟩, we define 𝜒𝑡 ­𝐴 ( 𝜒𝑠 , 𝜒𝑒 ) as follows.
                                                                                     𝑞
         𝜒𝑡 ­𝐴 ( 𝜒𝑠 , 𝜒𝑒 ) ≜ ∀𝑤 𝐴 𝑞𝑡 𝜏 𝑟𝑡 𝑞𝑠 , (𝑞𝑡 , 𝜏, 𝑟𝑡 ) ∈ 𝜒𝑡 ⇒ (𝑞𝑠 , 𝑞𝑡 ) ∈ 𝑅𝐴 (𝑤 𝐴 ) ⇒
                                                                                                           
                                     ∃𝑤 𝐴′ 𝑟𝑠 , (𝑞𝑠 , 𝜏, 𝑟𝑠 ) ∈ 𝜒𝑠 ∧ 𝑤 𝐴 {𝐴 𝑤 𝐴′ ∧ (𝑟𝑠 , 𝑟𝑡 ) ∈ 𝑅𝐴𝑟 (𝑤 𝐴′ ) ∨
                                                                       
                                     ∃𝜏0, (𝑞𝑠 , 𝜏0 ) ∈ 𝜒𝑒 ∧ 𝜏0 ⩽𝑇 𝜏 ;
Similarly, given a KIR 𝐵 = ⟨𝑊𝐵 , {𝐵 , 𝑅𝐵 , 𝑅𝐵𝑟 ⟩, we then define J𝑀𝑡 K 𝜒𝑡 ­𝐵 J𝑀𝑠 K 𝜒𝑠𝑒 as follows, where
                                              𝑞                                                𝜒

J𝑀𝑡 K 𝜒𝑡 has the denotation signature FDenote (defined in §6.1) with language interface ⟨query𝑡 , reply𝑡 ⟩,
and J𝑀𝑠 K 𝜒𝑠 has the denotation signature FDenote with language interface ⟨query𝑠 , reply𝑠 ⟩.
  J𝑀𝑡 K 𝜒𝑡 ­𝐵 J𝑀𝑠 K 𝜒𝑠𝑒 ≜ let J𝑀𝑠 K 𝜒𝑠𝑒 .( err) ≜ J𝑀𝑠 K 𝜒𝑠 .(err) ∪ (J𝑀𝑠 K 𝜒𝑠 .(cll) ◦ 𝜒𝑒 ) in
                     𝜒               𝜒

           ∀𝑤 𝐵 𝑞𝑡 𝜏 𝑟𝑡 𝑞𝑠 , (𝑞𝑡 , 𝜏, 𝑟𝑡 ) ∈ J𝑀𝑡 K 𝜒𝑡 .(nrm) ⇒ (𝑞𝑠 , 𝑞𝑡 ) ∈ 𝑅𝐵 (𝑤 𝐵 ) ⇒
                                                                               𝑞
                                                                                                                 
                              ∃𝑤 𝐵′ 𝑟𝑠 , (𝑞𝑠 , 𝜏, 𝑟𝑠 ) ∈ J𝑀𝑠 K 𝜒𝑠 .(nrm) ∧ 𝑤 𝐵 {𝐵 𝑤 𝐵′ ∧ (𝑟𝑠 , 𝑟𝑡 ) ∈ 𝑅𝐵𝑟 (𝑤 𝐵′ ) ∨
                                                                             
                              ∃𝜏0, (𝑞𝑠 , 𝜏0 ) ∈ J𝑀𝑠 K 𝜒𝑠𝑒 .(err) ∧ 𝜏0 ⩽𝑇 𝜏 ;
                                                        𝜒

           ∀𝑤 𝐵 𝑞𝑡 𝜏 𝑞𝑡′ 𝑞𝑠 , (𝑞𝑡 , 𝜏, 𝑞𝑡′ ) ∈ J𝑀𝑡 K 𝜒𝑡 .(cll) ⇒ (𝑞𝑠 , 𝑞𝑡 ) ∈ 𝑅𝐵 (𝑤 𝐵 ) ⇒
                                                                               𝑞
                                                                                                                    
                              ∃𝑤 𝐵′ 𝑞𝑠′ , (𝑞𝑠 , 𝜏, 𝑞𝑠′ ) ∈ J𝑀𝑠 K 𝜒𝑠 .(cll) ∧ 𝑤 𝐵 {𝐵 𝑤 𝐵′ ∧ (𝑞𝑠′ , 𝑞𝑡′ ) ∈ 𝑅𝐵 (𝑤 𝐵′ ) ∨
                                                                                                           𝑞
                                                                              
                              ∃𝜏0, (𝑞𝑠 , 𝜏0 ) ∈ J𝑀𝑠 K 𝜒𝑠𝑒 .(err) ∧ 𝜏0 ⩽𝑇 𝜏 ;
                                                          𝜒

           ∀𝑤 𝐵 𝑞𝑡 𝜏 𝑞𝑠 , (𝑞𝑡 , 𝜏) ∈ J𝑀𝑡 K 𝜒𝑡 .(err) ⇒ (𝑞𝑠 , 𝑞𝑡 ) ∈ 𝑅𝐵 (𝑤 𝐵 ) ⇒
                                                                       𝑞
                                                                                                        
                                                            ∃𝜏0, (𝑞𝑠 , 𝜏0 ) ∈ J𝑀𝑠 K 𝜒𝑠𝑒 .(err) ∧ 𝜏0 ⩽𝑇 𝜏 ;
                                                                                    𝜒

           ∀𝑤 𝐵 𝑞𝑡 𝜏 𝑞𝑠 , (𝑞𝑡 , 𝜏) ∈ J𝑀𝑡 K 𝜒𝑡 .(fin_dvg) ⇒ (𝑞𝑠 , 𝑞𝑡 ) ∈ 𝑅𝐵 (𝑤 𝐵 ) ⇒
                                                                           𝑞
                                                                                                       
                          (𝑞𝑠 , 𝜏) ∈ J𝑀𝑠 K 𝜒𝑠 .(fin_dvg) ∨ ∃𝜏0, (𝑞𝑠 , 𝜏0 ) ∈ J𝑀𝑠 K 𝜒𝑠𝑒 .(err) ∧ 𝜏0 ⩽𝑇 𝜏 ;
                                                                                   𝜒

           ∀𝑤 𝐵 𝑞𝑡 𝜏 𝑞𝑠 , (𝑞𝑡 , 𝜏) ∈ J𝑀𝑡 K 𝜒𝑡 .(inf_dvg) ⇒ (𝑞𝑠 , 𝑞𝑡 ) ∈ 𝑅𝐵 (𝑤 𝐵 ) ⇒
                                                                           𝑞
                                                                                                       
                          (𝑞𝑠 , 𝜏) ∈ J𝑀𝑠 K 𝜒𝑠 .(inf_dvg) ∨ ∃𝜏0, (𝑞𝑠 , 𝜏0 ) ∈ J𝑀𝑠 K 𝜒𝑠𝑒 .(err) ∧ 𝜏0 ⩽𝑇 𝜏 .
                                                                                   𝜒


Finally, for given Kripke interface relations 𝐴 and 𝐵, the behavior refinement between open modules
𝑀𝑠 and 𝑀𝑡 , denoted by J𝑀𝑡 K ­𝐴↠𝐵 J𝑀𝑠 K, is defined as follows.
                                                                                                   𝜒
                 J𝑀𝑡 K ­𝐴↠𝐵 J𝑀𝑠 K ≜ ∀𝜒𝑡 𝜒𝑠 𝜒𝑒 , 𝜒𝑡 ­𝐴 ( 𝜒𝑠 , 𝜒𝑒 ) ⇒ J𝑀𝑡 K 𝜒𝑡 ­𝐵 J𝑀𝑠 K 𝜒𝑠𝑒 .
We illustrate the above definitions (typically for terminating behaviors) in Fig. 8. This formalization
enables classical rely–guarantee reasoning [Liang et al. 2012] by the accessibility relation between
worlds. Specifically, the evolution of worlds in the callee’s behavior refinement provides the rely
condition for the caller’s behavior refinement. Conversely, assuming 𝑤 𝐴 {𝐴 𝑤 𝐴′ , the evolution of
worlds in the caller’s behavior refinement must respect the guarantee condition 𝑤 𝐵 {𝐵 𝑤 𝐵′ . When
each module is proved to satisfy its guarantee condition, and these guarantee conditions entail
their rely conditions, their compilation correctness becomes horizontally compositional.
 Theorem 7.9 (Horizontal compositionality). For any source modules 𝑀𝑠 , 𝑀𝑠′ , and target
modules 𝑀𝑡 , 𝑀𝑡′ , if J𝑀𝑡 K ­𝐴↠𝐴 J𝑀𝑠 K and J𝑀𝑡′ K ­𝐴↠𝐴 J𝑀𝑠′ K, then J𝑀𝑡 K ⊕ J𝑀𝑡′ K ­𝐴↠𝐴 J𝑀𝑠 K ⊕ J𝑀𝑠′ K.

  Theorem 7.10 (Vertical compositionality). Given KIRs 𝐴1, 𝐴2, 𝐵 1, 𝐵 2 , and modules 𝑀1, 𝑀2, 𝑀3 ,
                J𝑀3 K ­𝐴2 ⇒𝐵2 J𝑀2 K ⇒ J𝑀2 K ­𝐴1 ⇒𝐵1 J𝑀1 K ⇒ J𝑀3 K ­𝐴2 •𝐴1 ⇒𝐵2 •𝐵1 J𝑀1 K.
  Since the semantics of a function (e.g., Clight) is defined from the semantics of its function
body (i.e., a statement), the correctness of function-level transformations can be derived from

     ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:32                                                                                                               Z. Cheng et al.


                                                                                                              J𝑀𝑠 K 𝜒𝑠𝑒 .(err)
                                                                                                                    𝜒
                  𝜒𝑠                                 𝜒𝑒                     J𝑀𝑠 K 𝜒𝑠 .(nrm)
        𝑞𝑠                    𝑟𝑠            𝑞𝑠                         𝑞𝑠                     𝑟𝑠         𝑞𝑠

  𝑅𝐴 𝑤 𝐴 {𝐴 𝑤 𝐴′ 𝑅𝐴𝑟 or 𝑅𝐴 𝑤 𝐴                                       𝑅𝐵 𝑤 𝐵 {𝐵 𝑤 𝐵′ 𝑅𝐵𝑟 or 𝑅𝐵 𝑤 𝐵
   𝑞                     𝑞                                            𝑞                     𝑞


                  𝜒𝑡                                 𝜒𝑡                     J𝑀𝑡 K 𝜒𝑡 .(nrm)                   J𝑀𝑡 K 𝜒𝑡 .(nrm)
        𝑞𝑡                    𝑟𝑡            𝑞𝑡                𝑟𝑡       𝑞𝑡                     𝑟𝑡         𝑞𝑡                      𝑟𝑡
             (a) Refinement of callee’s behavior                              (b) Refinement of caller’s behavior

                             Fig. 8. Behavior refinement for CompCert open functions/modules.


the correctness of statement-level transformations. We build the behavior refinement for open
statements as follows, in a similar form to the behavior refinement for open modules.
   Example 7.11 (Behavior refinement for open statement of CompCert). A statement of an open
module 𝑀 may call functions external to 𝑀 (i.e., open). Suppose that a statement 𝑠 in a source
module 𝑀𝑠 is compiled to a statement 𝑡 in the compiled module 𝑀𝑡 . Given a Kripke relation
𝑅𝐵 : K𝑊𝐵 ( state𝑠 , state𝑡 ) between the source and target program states, and an accessibility relation
{𝐵 ⊆ 𝑊𝐵 × 𝑊𝐵 between worlds. The behavior refinement between 𝑠 and 𝑡, denoted by J𝑡K 𝜒𝑡 ­𝑅𝐵
J𝑠K 𝜒𝑠𝑒 , is defined as follows, where the semantic oracles 𝜒𝑠 , 𝜒𝑒 and 𝜒𝑡 are explained in Example 7.8.
    𝜒


 J𝑡K 𝜒𝑡 ­𝑅𝐵 J𝑠K 𝜒𝑠𝑒 ≜ let J𝑠K 𝜒𝑠𝑒 .(err) ≜ J𝑠K 𝜒𝑠 .(err) ∪ (J𝑠K 𝜒𝑠 .(cll) ◦ 𝜒𝑒 ) in
                       𝜒             𝜒

       ∀𝑤 𝐵 𝜎𝑡 𝜏 𝜎𝑡′ 𝜎𝑠 , (𝜎𝑡 , 𝜏, 𝜎𝑡′ ) ∈ J𝑡K 𝜒𝑡 .(nrm) ⇒ (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅𝐵 (𝑤 𝐵 ) ⇒
                                                                                                                 
                               ∃𝑤 𝐵′ 𝜎𝑠′, (𝜎𝑠 , 𝜏, 𝜎𝑠′ ) ∈ J𝑠K 𝜒𝑠 .(nrm) ∧ 𝑤 𝐵 {𝐵 𝑤 𝐵′ ∧ (𝜎𝑠′, 𝜎𝑡′ ) ∈ 𝑅𝐵 (𝑤 𝐵′ ) ∨
                                                                            
                               ∃𝜏0, (𝜎𝑠 , 𝜏0 ) ∈ J𝑠K 𝜒𝑠𝑒 .(err) ∧ 𝜏0 ⩽𝑇 𝜏 ;
                                                        𝜒
                                                                                                                    
       ∀𝑤 𝐵 𝜎𝑡 𝜏 𝜎𝑠 , (𝜎𝑡 , 𝜏) ∈ J𝑡K 𝜒𝑡 .(err) ⇒ (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅𝐵 (𝑤 𝐵 ) ⇒ ∃𝜏0, (𝜎𝑠 , 𝜏0 ) ∈ J𝑠K 𝜒𝑠𝑒 .(err) ∧ 𝜏0 ⩽𝑇 𝜏 ;
                                                                                                𝜒

       ∀𝑤 𝐵 𝜎𝑡 𝜏 𝜎𝑠 , (𝜎𝑡 , 𝜏) ∈ J𝑡K 𝜒𝑡 .(fin_dvg) ⇒ (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅𝐵 (𝑤 𝐵 ) ⇒
                                                                                                    
                           (𝜎𝑠 , 𝜏) ∈ J𝑠K 𝜒𝑠 .(fin_dvg) ∨ ∃𝜏0, (𝜎𝑠 , 𝜏0 ) ∈ J𝑠K 𝜒𝑠𝑒 .(err) ∧ 𝜏0 ⩽𝑇 𝜏 ;
                                                                                𝜒

       ∀𝑤 𝐵 𝜎𝑡 𝜏 𝜎𝑠 , (𝜎𝑡 , 𝜏) ∈ J𝑡K 𝜒𝑡 .(inf_dvg) ⇒ (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅𝐵 (𝑤 𝐵 ) ⇒
                                                                                                    
                           (𝜎𝑠 , 𝜏) ∈ J𝑠K 𝜒𝑠 .(inf_dvg) ∨ ∃𝜏0, (𝜎𝑠 , 𝜏0 ) ∈ J𝑠K 𝜒𝑠𝑒 .(err) ∧ 𝜏0 ⩽𝑇 𝜏 .
                                                                                𝜒


Example 7.4 is a special case of Example 7.11 if we define 𝑅𝐵 ≜ 𝜆𝑤 𝐵 .𝑅 and {𝐵 ≜ 𝑊𝐵 × 𝑊𝐵 . In our
Rocq implementation, we verify the statement transformation of the CompCert front-end with this
general behavior refinement. We show a concrete nontrivial Kripke relation for Cminorgen in §7.5.
  Example 7.12 (Behavior refinement for typical optimizations). Consider a standard constant prop-
agation optimization on the PCALL language, where the variables known to have a constant value
will be substituted with the constant. At the optimization level, the algorithm first produces static
analysis results, telling which variables hold constant values before and after every statement, and
then generates the target code by replacing the variable with its constant. For example:
       source code 𝑐: x = 1; y = x + 1
       analysis: [𝜋 0 := _ ↦→ ⊥] x =1; [𝜋 1 := x ↦→ const 1] y = x + 1 [𝜋2 := x ↦→ const 1; y ↦→ const 2]
       target code Tcp (𝑐 ): x = 1; y = 2

At the verification level, behavior refinement is based on the analysis results. We use Π to denote
the set of analysis results that map each variable to the constant value if the variable is constant,
or ⊥ if not. We use 𝑅𝜋 to denote the state-matching relation between source and target program

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                                    5:33


states. The relation 𝑅𝜋 is parameterized by the analysis result 𝜋, which requires that the value of
a variable on the source state respects its value on the analysis result 𝜋. Assume that the source
code 𝑐 is optimized to the target code Tcp (𝑐) by standard constant propagation, generating analysis
results 𝜋1 at the end of 𝑐 with initially known result10 𝜋 0 . We define JTcp (𝑐)K ­ (𝜋0,𝜋1 ) J𝑐K as follows.
            ∀𝜎𝑡 𝜎𝑡′ 𝜎𝑠 , (𝜎𝑡 , 𝜎𝑡′ ) ∈ JTcp (𝑐)K.(nrm) ⇒ (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅𝜋0 ⇒
                                                                                        
                                       ∃𝜎𝑠′, (𝜎𝑠 , 𝜎𝑠′ ) ∈ J𝑐K.(nrm) ∧ (𝜎𝑠′, 𝜎𝑡′ ) ∈ 𝑅𝜋1 ∨ 𝜎𝑠 ∈ J𝑐K.(err);
            ∀𝜎𝑡 𝜎𝑠 , 𝜎𝑡 ∈ JTcp (𝑐)K.(err) ⇒ (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅𝜋0 ⇒ 𝜎𝑠 ∈ J𝑐K.(err);
            ∀𝜎𝑡 𝜎𝑠 , 𝜎𝑡 ∈ JTcp (𝑐)K.(dvg) ⇒ (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅𝜋0 ⇒ 𝜎𝑠 ∈ J𝑐K.(dvg) ∨ 𝜎𝑠 ∈ J𝑐K.(err);
   Summary and our solution. Examples 7.4 ∼ 7.12 have shown that nontrivial state-matching
relations are required in realistic settings. To extend the verification technique of the first two
examples to such settings, we next propose the notion of Refinement Algebras (RAs). The key
idea is to employ isomorphism functions to establish a structured correspondence between the
denotational semantics of source and target programs, and then exploit the algebraic properties of
semantic operators and RAs to achieve compositionality and to enable mechanized verification.

7.2    Refinement Algebras
Our proof system is based on a notion of refinement algebras, whose definition is shown as follows.
   Definition 7.13. [Refinement algebras] A Refinement Algebra (RA) is a tuple (S, E, T , 𝛾), where
    • S, E, T are behavior sets. Specifically, the set S represents one kind of safe behaviors of a
      source program (e.g., termination), and the set T denotes the corresponding behavior set of
      the target program. The set E denotes the aborting behavior set of the source program;
    • 𝛾 : S × E → T is a monotonic function transforming source behavior sets to the target:
                ∀𝑁 1 𝑁 2 ∈ S, ∀𝐸 1 𝐸 2 ∈ E, 𝑁 1 ⊆ 𝑁 2 ⇒ 𝐸 1 ⊆ 𝐸 2 ⇒ 𝛾 (𝑁 1, 𝐸 1 ) ⊆ 𝛾 (𝑁 2, 𝐸 2 )                      (43)
  To illustrate how RAs encode various transformation correctness discussed in §7.1, we begin
with the following RA instances11 for Example 7.2, where P (𝐴) is the power set of a given set 𝐴.
  Example 7.14 (Termination instance 1). A1N ≜ (S1N, E1N, T1N, 𝛾 1N ), where for a given state set state,
E1 ≜ P ( state), S1N = T1N ≜ P ( state × state). ∀𝑁 ∈ S1N , 𝐸 ∈ E1N , 𝛾 1N (𝑁 , 𝐸) ≜ 𝑁 ∪ (𝐸 × state).
 N


  Example 7.15 (Divergence instance 1). A1D ≜ (S1D, E1D, T1D, 𝛾 1D ), where for a given state set state,
E1 = S1D = T1D ≜ P ( state). ∀𝑁 ∈ S1D , 𝐸 ∈ E1D , 𝛾 1D (𝑁 , 𝐸) ≜ 𝑁 ∪ 𝐸.
 D


   With the RA instances A1N and A1D , we can encode JT (𝑐)K ⊑ J𝑐K of Example 7.2 as follows.
                                      
                                       JT (𝑐)K.( nrm) ⊆ 𝛾 1N (J𝑐K.( nrm), J𝑐K.( err)) and
                                      
                                      
                                      
                       JT (𝑐)K ⊑ J𝑐K ≜ JT (𝑐)K.( dvg) ⊆ 𝛾 1D (J𝑐K.( dvg), J𝑐K.( err)) and                              (44)
                                      
                                      
                                       JT (𝑐)K.( err) ⊆ 𝛾 D (∅, J𝑐K.( err))
                                                          1

  Example 7.16 (Termination instance 2). A2N ≜ (S2N, E2N, T2N, 𝛾 2N ), where for a given state set state,
E2 ≜ P ( state × trace), S2N = T2N ≜ P ( state × trace × state). ∀𝑁 ∈ S2N , 𝐸 ∈ E2N ,
 N
                                                         
              𝛾 2N (𝑁 , 𝐸) ≜ (𝜎, 𝜏, 𝜎 ′ ) (𝜎, 𝜏, 𝜎 ′ ) ∈ 𝑁 ∨ (∃𝜏0, (𝜎, 𝜏0 ) ∈ 𝐸 ∧ 𝜏0 ⩽𝑇 𝜏)
10 All the variables are mapped to the unknown value ⊥ if we know nothing.
11 For clarity of presentation, we use subscripts to distinguish gamma functions from different refinement algebra instances.

In Rocq, the abstract refinement algebra (Def. 7.13) is declared as a type class, and concrete refinement algebras can be
instantiated for specific types. When applying an instance to define the refinement between behavior sets, Rocq’s type class
resolution mechanism automatically selects the appropriate instance of gamma according to the type of its arguments.


      ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:34                                                                                                  Z. Cheng et al.


   Example 7.17 (Finite diverging instance 2). A2F ≜ (S2F, E2F, T2F, 𝛾 2F ), where for a given state set
state, E2F = S2F = T2F ≜ P ( state × trace). ∀𝑁 ∈ S2F , 𝐸 ∈ E2F ,

                      𝛾 2F (𝑁 , 𝐸) ≜ { (𝜎, 𝜏) | (𝜎, 𝜏) ∈ 𝑁 ∨ (∃𝜏0, (𝜎, 𝜏0 ) ∈ 𝐸 ∧ 𝜏0 ⩽𝑇 𝜏) }
   Example 7.18 (Infinite diverging instance 2). A2I ≜ (S2I, E2I, T2I, 𝛾 2I ), where for a given state set
state, E2I = S2I = T2I ≜ P ( state × itrace). ∀𝑁 ∈ S2I , 𝐸 ∈ E2I ,

                      𝛾 2I (𝑁 , 𝐸) ≜ { (𝜎, 𝜏) | (𝜎, 𝜏) ∈ 𝑁 ∨ (∃𝜏0, (𝜎, 𝜏0 ) ∈ 𝐸 ∧ 𝜏0 ⩽𝑇 𝜏) }
   With the RA instances A2N , A2F and A2I , we can encode J𝑡K ­ J𝑠K of Example 7.3 as follows.
                      
                       J𝑡K.(nrm) ⊆ 𝛾 2N (J𝑠K.(nrm), J𝑠K.(err)) and J𝑡K.(err) ⊆ 𝛾 2F (∅, J𝑠K.(err)) and
                      
                      
                      
         J𝑡K ­ J𝑠K ≜ J𝑡K.(fin_dvg) ⊆ 𝛾 2F (J𝑠K.(fin_dvg), J𝑠K.(err)) and                                (45)
                      
                      
                       J𝑡K.(inf_dvg) ⊆ 𝛾 I (J𝑠K.(inf_dvg), J𝑠K.(err))
                                           2
   In fact, we can provide more general RA instances to encode nontrivial behavior refinement. For
instance, recall that we define the preservation of terminating behaviors in Example 7.4 as follows.
 J𝑡K.( nrm) ­𝑅 (J𝑠K.( nrm), J𝑠K.( err)) ≜ ∀𝜎𝑡 𝜏 𝜎𝑡′ 𝜎𝑠 , (𝜎𝑡 , 𝜏, 𝜎𝑡′ ) ∈ J𝑡K.(nrm) ⇒ (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅 ⇒
                                                                                                          (46)
                ∃𝜎𝑠′, (𝜎𝑠 , 𝜏, 𝜎𝑠′ ) ∈ J𝑠K.(nrm) ∧ (𝜎𝑠′, 𝜎𝑡′ ) ∈ 𝑅 ∨ ∃𝜏0, (𝜎𝑠 , 𝜏0 ) ∈ J𝑠K.(err) ∧ 𝜏0 ⩽𝑇 𝜏 ;
We aim to define a termination instance (as given by Example 7.19) of refinement algebras such that
                 J𝑡K.( nrm) ⊆ 𝛾𝑅 (J𝑠K.( nrm), J𝑠K.( err)) ⇔ J𝑡K.( nrm) ­𝑅 (J𝑠K.( nrm), J𝑠K.( err))
  Example 7.19 (Termination instance 3). S3N ≜ P ( state𝑠 × trace × state𝑠 ), E3N ≜ P ( state𝑠 × trace),
and T3N ≜ P ( state𝑡 × trace × state𝑡 ). For a given relation 𝑅 ⊆ state𝑠 × state𝑡 , ∀𝑁 ∈ S3N, ∀𝐸 ∈ E3N,
                                                                                                       
                                                           (∃𝜎𝑠′, (𝜎𝑠 , 𝜏, 𝜎𝑠′ ) ∈ 𝑁 ∧ (𝜎𝑠′, 𝜎𝑡′ ) ∈ 𝑅)
          N                     ′
        𝛾 3 (𝑁 , 𝐸) ≜ (𝜎𝑡 , 𝜏, 𝜎𝑡 ) ∀𝜎𝑠 , (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅 ⇒                                                (47)
                                                           ∨ (∃𝜏0, (𝜎𝑠 , 𝜏0 ) ∈ 𝐸 ∧ 𝜏0 ⩽𝑇 𝜏)
   Similarly, we can define RA instances for finite divergence and infinite divergence as follows.
  Example 7.20 (Finite divergence instance 3). S3F ≜ P ( state𝑠 × trace), E3F ≜ P ( state𝑠 × trace), and
T3 ≜ P ( state𝑡 × trace). For a given relation 𝑅 ⊆ state𝑠 × state𝑡 , ∀𝑁 ∈ S3F, ∀𝐸 ∈ E3F,
  F

       𝛾 3F (𝑁 , 𝐸) ≜ { (𝜎𝑡 , 𝜏) | ∀𝜎𝑠 , (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅 ⇒ (𝜎𝑠 , 𝜏) ∈ 𝑁 ∨ (∃𝜏0, (𝜎𝑠 , 𝜏0 ) ∈ 𝐸 ∧ 𝜏0 ⩽𝑇 𝜏) }        (48)
  Example 7.21 (Infinite divergence instance 3). S3I ≜ P ( state𝑠 × itrace), E3I ≜ P ( state𝑠 × trace),
and T3I ≜ P ( state𝑡 × itrace). For a given relation 𝑅 ⊆ state𝑠 × state𝑡 , ∀𝑁 ∈ S3I, ∀𝐸 ∈ E3I,
       𝛾 3I (𝑁 , 𝐸) ≜ { (𝜎𝑡 , 𝜏) | ∀𝜎𝑠 , (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅 ⇒ (𝜎𝑠 , 𝜏) ∈ 𝑁 ∨ (∃𝜏0, (𝜎𝑠 , 𝜏0 ) ∈ 𝐸 ∧ 𝜏0 ⩽𝑇 𝜏) }        (49)
  With the RA instances A3N = (S3N, E3N, T3N, 𝛾 3N ), A3F = (S3F, E3F, T3F, 𝛾 3F ), and A3I = (S3I, E3I, T3I, 𝛾 3I ),
we can encode J𝑡K ­𝑅 J𝑠K of Example 7.4 as follows, and obviously we have J𝑡K ⊑𝑅 J𝑠K ⇔ J𝑡K ­𝑅 J𝑠K.
                   
                    J𝑡K.( nrm) ⊆ 𝛾 3N (J𝑠K.( nrm), J𝑠K.( err)) and J𝑡K.( err) ⊆ 𝛾 3F (∅, J𝑠K.( err)) and
                   
                   
                   
       J𝑡K ⊑𝑅 J𝑠K ≜ J𝑡K.( fin_dvg) ⊆ 𝛾 3F (J𝑠K.( fin_dvg), J𝑠K.( err)) and                                        (50)
                   
                   
                    J𝑡K.( inf_dvg) ⊆ 𝛾 I (J𝑠K.( inf_dvg), J𝑠K.( err))
                                         3
  From these RA instances, we observe that the RA-based formulation, via the 𝛾 function, provides
an algebraic characterization of the correspondence between source and target behaviors. This for-
mulation not only offers a uniform and compositional foundation for proving compiler correctness,
but also enables the extension of algebraic verification methods from simple cases to more realistic
compilation settings. Before turning to more complex RA instances, we first proceed to introduce
enhanced RA structures to further consolidate the algebraic underpinnings of our framework.

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                                  5:35


                        𝜏1                            𝜏2                                   𝜏1 · 𝜏2
              𝜎𝑠                  𝜎𝑠′       𝜎𝑠′                  𝜎𝑠′′       𝜎𝑠                                 𝜎𝑠′′
                   J𝑠 1 K.(nrm)                   J𝑠 2 K.(nrm)                   J𝑠 1 K.(nrm) ◦ J𝑠 2 K.(nrm)
             𝑅                 𝑅        ◦     𝑅                     𝑅   ⇒   𝑅                                     𝑅
                        𝜏1                            𝜏2                                   𝜏1 · 𝜏2
              𝜎𝑡                  𝜎𝑡′       𝜎𝑡′                  𝜎𝑡′′       𝜎𝑡                                 𝜎𝑡′′
                   J𝑡 1 K.(nrm)                   J𝑡 2 K.(nrm)                   J𝑡 1 K.(nrm) ◦ J𝑡 2 K.(nrm)

              Fig. 9. The behavior refinement for CompCert is compositional w.r.t. composition.


7.3    Enhanced Refinement Algebras
Since the union and composition operators are ubiquitous in the semantic definition of composite
statements, we define the following enhanced RAs to facilitate structured compiler verification.
    Definition 7.22 (Union-preserved RAs). A refinement algebra A = (S, E, T , 𝛾) is union-preserved
iff:
                   ∀𝑁 1 𝑁 2 ∈ S, ∀𝐸 1 𝐸 2 ∈ E, 𝛾 (𝑁 1, 𝐸 1 ) ∪ 𝛾 (𝑁 2, 𝐸 2 ) ⊆ 𝛾 (𝑁 1 ∪ 𝑁 2, 𝐸 1 ∪ 𝐸 2 )              (51)
   Definition 7.23 (Concatenation-preserved RAs). Refinement algebras A1 = (S1, E1, T1, 𝛾 1 ) and
A2 = (S2, E2, T2, 𝛾 2 ) are concatenation-preserved to refinement algebra A3 = (S3, E1, T3, 𝛾 3 ) iff:
given operators ◦ : T1 × T2 → T3 , ◦ : S1 × S2 → S3 , and ◦ : S1 × E2 → E1 s.t. for any 𝑁 1, 𝑁 2, 𝐸 1, 𝐸 2 ,
                                                                                               
                         𝛾 1 (𝑁 1, 𝐸 1 ) ◦ 𝛾 2 (𝑁 2, 𝐸 2 ) ⊆ 𝛾 3 𝑁 1 ◦ 𝑁 2, 𝐸 1 ∪ (𝑁 1 ◦ 𝐸 2 )       (52)
Particularly, if RAs A and A are concatenation-preserved to A, A is self-concatenation-preserved.
Note that for a given RA (S, E, T , 𝛾), writing 𝛾 (𝑁 , 𝐸) implicitly means that 𝑁 ∈ S and 𝐸 ∈ E .
  Lemma 7.24 (Instances of enhanced refinement algebras). A𝑖N , A𝑖F , and A𝑖I (defined in §7.2)
are union-preserved refinement algebras; (ii) A𝑖N is self-concatenation-preserved; (iii) A𝑖N and A𝑖F are
concatenation-preserved to A𝑖F ; and (iv) A𝑖N and A𝑖I are concatenation-preserved to A𝑖I for 𝑖 = 1, 2, 3.
Concrete operators for these RA instances are provided in §3.1 according to the type of behavior sets.
   We first provide a brief preview of how the enhanced RA instances from Lemma 7.24 enable
a uniform refinement proof (see §8 for details). For a structural transformation of sequential
statements (as in Example 7.1), the proof proceeds as follows: the crucial step (54) ⊆ (55) follows
immediately from the concatenation-preservation property of the underlying RA instances. Fig. 9
provides a schematic illustration of this property for normally terminating behaviors in CompCert.
                       J𝑡 1 ; 𝑡 2 K.(nrm) = J𝑡 1 K.(nrm) ◦ J𝑡 2 K.(nrm)                                               (53)
                       ⊆ 𝛾𝑖N (J𝑠 1 K.(nrm), J𝑠 1 K.(err)) ◦ 𝛾𝑖N (J𝑠 2 K.(nrm), J𝑠 2 K.(err))                          (54)
                       ⊆ 𝛾𝑖N (J𝑠 1 K.(nrm) ◦ J𝑠 2 K.(nrm), J𝑠 1 K.(err) ∪ (J𝑠 1 K.(nrm) ◦ J𝑠 2 K.(err)))              (55)
                       = 𝛾𝑖N (J𝑠 1 ; 𝑠 2 K.(nrm), J𝑠 1 ; 𝑠 2 K.(err))                                                 (56)
  Since the star ∗ and infinity ∞ operators are ubiquitous in the semantic definition of loops and
recursion, we define the following enhanced RAs to facilitate structured compiler verification.
   Definition 7.25 (Star-preserved RAs). RAs A1 = (S1, E, T1, 𝛾 1 ) and A2 = (S2, E, T2, 𝛾 2 ) are star-
preserved to A2 iff: given operators ◦ : T1 × T2 → T2 , ◦ : S1 × S2 → S2 , and ◦ : S1 × E → E, and
star operators ∗ : T1 → T1 and ∗ : S1 → S1 such that for any 𝑁 1 ∈ S1 , 𝑁 2 ∈ S2 , 𝐸 1 and 𝐸 2 ∈ E,
                                                                                                   
                       (𝛾 1 (𝑁 1, 𝐸 1 )) ∗ ◦ 𝛾 2 (𝑁 2, 𝐸 2 ) ⊆ 𝛾 2 𝑁 1∗ ◦ 𝑁 2, 𝑁 1∗ ◦ (𝐸 1 ∪ 𝐸 2 )   (57)

      ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:36                                                                                                        Z. Cheng et al.


   Definition 7.26 (Infinity-preserved RAs). RAs A1 = (S1, E, T1, 𝛾 1 ) and A2 = (S2, E, T2, 𝛾 2 ) are
infinity-preserved to A2 iff: given composition operators ◦ : T1 × T2 → T2 , ◦ : S1 × S2 → S2 , and
◦ : S1 × E → E, star operators ∗ : T1 → T1 , ∗ : S1 → S1 , and infinity operators ∞ : T1 → T2 ,
∞ : S1 → S2 such that for any 𝑁 1 ∈ S1 , 𝑁 2 ∈ S2 , and 𝐸 1, 𝐸 2 ∈ E,
                                                               ∞                                               
         (𝛾 1 (𝑁 1, 𝐸 1 )) ∗ ◦ 𝛾 2 (𝑁 2, 𝐸 2 ) ∪ 𝛾 1 (𝑁 1, 𝐸 1 ) ⊆ 𝛾 2 (𝑁 1∗ ◦ 𝑁 2 ) ∪ 𝑁 1∞, 𝑁 1∗ ◦ (𝐸 1 ∪ 𝐸 2 )   (58)
  Connection to fixed points. Given sets 𝑋 and 𝑌 , the form 𝑋 ∗ ◦ 𝑌 is actually the Kleene (least) fixed
point of function 𝑓 (𝑥) = 𝑌 ∪ (𝑋 ◦ 𝑥), and (𝑋 ∗ ◦ 𝑌 ) ∪ 𝑋 ∞ is the greatest fixed point of function 𝑓 .
They are frequently used in the semantic definition of loops and recursion (as shown in §3 and §4),
so we use enhanced RAs to facilitate the compilation correctness proof of loops and recursion.
   Lemma 7.27 (Instances of star/infinity-preserved refinement algebras). (i) A𝑖N and A𝑖F
(defined in §7.2) are star-preserved to A𝑖F ; and (ii) A𝑖N and A𝑖I are infinity-preserved to A𝑖I for 𝑖 = 1, 2, 3.

7.4      Algebraic Behavior Refinement
7.4.1 RA Instances for Open Statement Transformation of CompCert. We define the following RA
instances to encode the behavior refinement for CompCert phases shown in Example 7.11.
  Theorem 7.28. Given a Kripke relation 𝑅𝐵 : K𝑊 ( state𝑠 , state𝑡 ) and a preorder {𝐵 ⊆ 𝑊 ×𝑊 . A N =
(S N, E, T N, 𝛾𝑅N𝐵 ), A F = (S F, E, T F, 𝛾𝑅F𝐵 ), and A I = (S I, E, T I, 𝛾𝑅I𝐵 ), where E ≜ P ( state𝑠 × trace),
        S N ≜ P ( state𝑠 × trace × state𝑠 )            S F ≜ P ( state𝑠 × trace)        S I ≜ P ( state𝑠 × itrace)
        T N ≜ P ( state𝑡 × trace × state𝑡 )            T F ≜ P ( state𝑡 × trace)        T I ≜ P ( state𝑡 × itrace)
                 (                                                                                                            )
                                      ∀𝜎𝑠 𝑤 𝐵 , (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅𝐵 (𝑤 𝐵 ) ⇒ ∃𝑤 𝐵′ 𝜎𝑠′, (𝜎𝑠 , 𝜏, 𝜎𝑠′ ) ∈ 𝑁 ∧ 𝑤 𝐵 {𝐵 𝑤 𝐵′ ∧
𝛾𝑅N𝐵 (𝑁 , 𝐸) ≜       (𝜎𝑡 , 𝜏, 𝜎𝑡′ )                                                                     
                                                (𝜎𝑠′, 𝜎𝑡′ ) ∈ 𝑅𝐵 (𝑤 𝐵′ ) ∨ ∃𝜏0, (𝜎𝑠 , 𝜏0 ) ∈ 𝐸 ∧ 𝜏0 ⩽𝑇 𝜏 ;
𝛾𝑅F𝐵 (𝑁 , 𝐸) ≜ { (𝜎𝑡 , 𝜏) | ∀𝜎𝑠 𝑤 𝐵 , (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅𝐵 (𝑤 𝐵 ) ⇒ (𝜎𝑠 , 𝜏) ∈ 𝑁 ∨ (∃𝜏0, (𝜎𝑠 , 𝜏0 ) ∈ 𝐸 ∧ 𝜏0 ⩽𝑇 𝜏) }
𝛾𝑅I𝐵 (𝑁 , 𝐸) ≜ { (𝜎𝑡 , 𝜏) | ∀𝜎𝑠 𝑤 𝐵 , (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅𝐵 (𝑤 𝐵 ) ⇒ (𝜎𝑠 , 𝜏) ∈ 𝑁 ∨ (∃𝜏0, (𝜎𝑠 , 𝜏0 ) ∈ 𝐸 ∧ 𝜏0 ⩽𝑇 𝜏) }
(i) A N , A F , and A I are union-preserved refinement algebras; (ii) A N is self-concatenation-preserved;
(iii) A N and A F are concatenation-preserved to A F ; (iv) A N and A I are concatenation-preserved to
A I ; (v) A N and A F are star-preserved to A F ; and (vi) A N and A I are infinity-preserved to A I .
7.4.2     RA Instances for CompCert Open Modules.
 Theorem 7.29. Given a KIR 𝐵 = ⟨𝑊𝐵 , {𝐵 , 𝑅𝐵 , 𝑅𝐵𝑟 ⟩, A N = (S N, E, T N, 𝛾𝐵N ), A C = (S C, E, T C, 𝛾𝐵C ),
                                                                 𝑞

A = (S I, E, T I, 𝛾𝐵I ), and A F = (S F, E, T F, 𝛾𝐵F ), where
 I


  E ≜ P ( query𝑠 × trace)                         S F ≜ P ( query𝑠 × trace)                T F ≜ P ( query𝑡 × trace)
  S N ≜ P ( query𝑠 × trace × reply𝑠 )             S C ≜ P ( query𝑠 × trace × query𝑠 )      S I ≜ P ( query𝑠 × itrace)
  T N ≜ P ( query𝑡 × trace × reply𝑡 )             T C ≜ P ( query𝑡 × trace × query𝑡 )      T I ≜ P ( query𝑡 × itrace)
                 (                                           𝑞                                                            )
                                   ∀𝑞𝑠 𝑤 𝐵 , (𝑞𝑠 , 𝑞𝑡 ) ∈ 𝑅𝐵 (𝑤 𝐵 ) ⇒ ∃𝑤 𝐵′ 𝑟𝑠 , (𝑞𝑠 , 𝜏, 𝑟𝑠 ) ∈ 𝑁 ∧ 𝑤 𝐵 {𝐵 𝑤 𝐵′ ∧
 𝛾𝐵N (𝑁 , 𝐸) ≜       (𝑞𝑡 , 𝜏, 𝑟𝑡 )                                                                   
                                              (𝑟𝑠 , 𝑟𝑡 ) ∈ 𝑅𝐵𝑟 (𝑤 𝐵′ ) ∨ ∃𝜏0, (𝑞𝑠 , 𝜏0 ) ∈ 𝐸 ∧ 𝜏0 ⩽𝑇 𝜏 ;
                 (                                           𝑞                                                            )
                                      ∀𝑞𝑠 𝑤 𝐵 , (𝑞𝑠 , 𝑞𝑡 ) ∈ 𝑅𝐵 (𝑤 𝐵 ) ⇒ ∃𝑤 𝐵′ 𝑞𝑠′ , (𝑞𝑠 , 𝜏, 𝑞𝑠′ ) ∈ 𝑁 ∧ 𝑤 𝐵 {𝐵 𝑤 𝐵′ ∧
 𝛾𝐵C (𝑁 , 𝐸) ≜       (𝑞𝑡 , 𝜏, 𝑞𝑡′ )                                                                      
                                                (𝑞𝑠′ , 𝑞𝑡′ ) ∈ 𝑅𝐵 (𝑤 𝐵′ ) ∨ ∃𝜏0, (𝑞𝑠 , 𝜏0 ) ∈ 𝐸 ∧ 𝜏0 ⩽𝑇 𝜏 ;
                                                                𝑞
                                                        𝑞
 𝛾𝐵F (𝑁 , 𝐸) ≜       (𝑞𝑡 , 𝜏) | ∀𝑞𝑠 𝑤 𝐵 , (𝑞𝑠 , 𝑞𝑡 ) ∈ 𝑅𝐵 (𝑤 𝐵 ) ⇒ (𝑞𝑠 , 𝜏) ∈ 𝑁 ∨ (∃𝜏0, (𝑞𝑠 , 𝜏0 ) ∈ 𝐸 ∧ 𝜏0 ⩽𝑇 𝜏)

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                                5:37

                                                        𝑞
 𝛾𝐵I (𝑁 , 𝐸) ≜       (𝑞𝑡 , 𝜏) | ∀𝑞𝑠 𝑤 𝐵 , (𝑞𝑠 , 𝑞𝑡 ) ∈ 𝑅𝐵 (𝑤 𝐵 ) ⇒ (𝑞𝑠 , 𝜏) ∈ 𝑁 ∨ (∃𝜏0, (𝑞𝑠 , 𝜏0 ) ∈ 𝐸 ∧ 𝜏0 ⩽𝑇 𝜏)

(i) A N , A C , A F , and A I are union-preserved refinement algebras; (ii) A C is self-concatenation-
preserved; (iii) A C and A N are concatenation-preserved to A N ; (iv) A C and A F are concatenation-
preserved to A F ; (v) A C and A I are concatenation-preserved to A I ; (vi) A C and A N are star-preserved
to A N ; (vii) A C and A F are star-preserved to A F ; and (viii) A C and A I are infinity-preserved to A I .

   Definition 7.30 (Behavior refinement for open statements of Cshmgen). Given natural numbers12
𝑛𝑏 , 𝑛𝑐 and the aborting behavior of external C functions 𝜒𝑒 (⊆ cquery × trace). A denotation 𝐷 2 of
Cshm.Denote is a refinement of a denotation 𝐷 1 of Clit.Denote, denoted by 𝐷 2 ⊑ (𝑅𝐵 ,𝑛𝑏 ,𝑛𝑐 ,𝜒𝑒 ) 𝐷 1 , iff:
                                                                                                         
                         𝐷 2 .( nrm)        ⊆ 𝛾𝑅N𝐵 𝐷 1 .( nrm),      𝐷 1 .( err) ∪ (𝐷 1 .( cll) ◦ 𝜒𝑒 )
                                                                                                         
                         𝐷 2 .( err)        ⊆ 𝛾𝑅F𝐵 ∅,                𝐷 1 .( err) ∪ (𝐷 1 .( cll) ◦ 𝜒𝑒 )
                                                                                                         
                         𝐷 2 .( blk)𝑛𝑏      ⊆ 𝛾𝑅N𝐵 𝐷 1 .( brk),      𝐷 1 .( err) ∪ (𝐷 1 .( cll) ◦ 𝜒𝑒 )
                                                                                                         
                         𝐷 2 .( blk)𝑛𝑐      ⊆ 𝛾𝑅N𝐵 𝐷 1 .( ctn),      𝐷 1 .( err) ∪ (𝐷 1 .( cll) ◦ 𝜒𝑒 )
                                                                                                         
                         𝐷 2 .( fin_dvg) ⊆ 𝛾𝑅F𝐵 𝐷 1 .( fin_dvg), 𝐷 1 .( err) ∪ (𝐷 1 .( cll) ◦ 𝜒𝑒 )
                                                                                                         
                         𝐷 2 .( inf_dvg) ⊆ 𝛾𝑅I𝐵 𝐷 1 .( inf_dvg), 𝐷 1 .( err) ∪ (𝐷 1 .( cll) ◦ 𝜒𝑒 )

where the gamma instances are defined in Theorem 7.28, the state-matching relation 𝑅𝐵 ≜ 𝜆𝑤 𝐵 .1,
and {𝐵 ≜ 𝑊𝐵 × 𝑊𝐵 as the representation of program states remains unchanged during Cshmgen.

   Definition 7.31 (Refinement between open function/module denotations). Let Φ1 and Φ2 be the
semantics of open functions/modules (e.g., that of Clight). The semantics Φ2 is said to be a refinement
of Φ1 , written as Φ2 ⊑𝐴↠𝐵 Φ1 , if and only if: (i) 𝐷 2 .( dom) = 𝐷 1 .( dom), and (ii) for any callee behaviors
𝜒𝑡 , 𝜒𝑠 and 𝜒𝑒 such that 𝜒𝑡 ⊆ 𝛾𝐴N ( 𝜒𝑠 , 𝜒𝑒 ), the following conditions hold, where 𝐷 1 = (Φ1 ) 𝜒𝑠 of
FDenote𝑠 , 𝐷 2 = (Φ2 ) 𝜒𝑡 of FDenote𝑡 , and the gamma instances are defined in Theorem 7.29:
                                                                                                
                       𝐷 2 .( nrm)     ⊆ 𝛾𝐵N 𝐷 1 .( nrm),     𝐷 1 .( err) ∪ (𝐷 1 .( cll) ◦ 𝜒𝑒 )
                                                                                                
                       𝐷 2 .( err)     ⊆ 𝛾𝐵F ∅,               𝐷 1 .( err) ∪ (𝐷 1 .( cll) ◦ 𝜒𝑒 )
                                                                                                
                       𝐷 2 .( cll)     ⊆ 𝛾𝐵C 𝐷 1 .( cll),     𝐷 1 .( err) ∪ (𝐷 1 .( cll) ◦ 𝜒𝑒 )
                                                                                                
                       𝐷 2 .( fin_dvg) ⊆ 𝛾𝐵F 𝐷 1 .( fin_dvg), 𝐷 1 .( err) ∪ (𝐷 1 .( cll) ◦ 𝜒𝑒 )
                                                                                                
                       𝐷 2 .( inf_dvg) ⊆ 𝛾𝐵I 𝐷 1 .( inf_dvg), 𝐷 1 .( err) ∪ (𝐷 1 .( cll) ◦ 𝜒𝑒 )

   The following theorems illustrates the soundness of the above algebraic behavior refinement in
terms of ­𝑅𝐵 defined in Example 7.11 and ­𝐴↠𝐵 defined in Example 7.8.

  Theorem 7.32 (Soundness of algebraic behavior refinement 1). For any 𝐷 1 of Clit.Denote
and 𝐷 2 of Cshm.Denote, for any nature numbers 𝑛𝑏 , 𝑛𝑐 , and for any semantic oracle 𝜒𝑒 ,

                                         if 𝐷 2 ⊑ (𝑅𝐵 ,𝑛𝑏 ,𝑛𝑐 ,𝜒𝑒 ) 𝐷 1, then 𝐷 2 ­𝑅𝐵 𝐷 1 .

  Theorem 7.33 (Soundness of algebraic behavior refinement 2). Given KIRs 𝐴 and 𝐵. For
any semantics of open functions/modules Φ1 and Φ2 , Φ2 ⊑𝐴↠𝐵 Φ1 if and only if Φ2 ­𝐴↠𝐵 Φ1 .

12 Natural numbers 𝑛 and 𝑛 are arguments of the statement transformation of Cshmgen, which are used to count the
                    𝑏     𝑐
exiting number from nested blocks (i.e., exit 𝑛𝑏 and exit 𝑛𝑐 are compiled from break and continue respectively).


     ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:38                                                                                                              Z. Cheng et al.


7.4.3 RA Instances for Typical Optimizations. We define the following RA instances to encode the
behavior refinement for standard constant propagation optimizations shown in Example 7.12.
  Theorem 7.34. Let 𝜋0 , 𝜋1 ∈ Π be analysis results. Given a relation 𝑅 : Π → P ( state𝑠 × state𝑡 ), let
A𝜋𝜋01 = (S N, E, T N, 𝛾𝜋𝜋01 ), A𝜋D 0 = (S D, E, T D, 𝛾𝜋D0 ), where
   S N ≜ P ( state𝑠 × state𝑠 )          T N ≜ P ( state𝑡 × state𝑡 )       E = S D ≜ P ( state𝑠 )         T D ≜ P ( state𝑡 )
                   
 𝛾𝜋𝜋01 (𝑁 , 𝐸) ≜       (𝜎𝑡 , 𝜎𝑡′ ) ∀𝜎𝑠 , (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅(𝜋 0 ) ⇒ (∃𝜎𝑠′, (𝜎𝑠 , 𝜎𝑠′ ) ∈ 𝑁 ∧ (𝜎𝑠′, 𝜎𝑡′ ) ∈ 𝑅(𝜋 1 )) ∨ 𝜎𝑠 ∈ 𝐸
 𝛾𝜋D0 (𝑁 , 𝐸) ≜ { 𝜎𝑡 | ∀𝜎𝑠 , (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅(𝜋 0 ) ⇒ (𝜎𝑠 ∈ 𝑁 ∨ 𝜎𝑠 ∈ 𝐸) }
(i) For any 𝜋 0 and 𝜋 1 , A𝜋𝜋01 and A𝜋D 0 are union-preserved refinement algebras; (ii) for any 𝜋0, 𝜋1, 𝜋2 ,
A𝜋𝜋01 and A𝜋𝜋12 are concatenation-preserved to A𝜋𝜋02 ; (iii) for any 𝜋0, 𝜋1 , A𝜋𝜋01 and A𝜋D 1 are concatenation-
preserved to A𝜋D 0 ; and (iv) for any 𝜋, A𝜋𝜋 and A𝜋D are star-preserved and infinity-preserved to A𝜋D .
  Similarly, given analysis results 𝜋0 and 𝜋1 , we can define JTcp (𝑐)K ⊑ (𝜋0,𝜋1 ) J𝑐K for typical opti-
mizations in Example 7.12 as follows, such that if JTcp (𝑐)K ⊑ (𝜋0,𝜋1 ) J𝑐K, then JTcp (𝑐)K ­ (𝜋0,𝜋1 ) J𝑐K.
                                                  
                                                   JTcp (𝑐)K.(nrm) ⊆ 𝛾𝜋𝜋01 (J𝑐K.(nrm), J𝑐K.(err)),
                                                  
                                                  
                                                  
                        JTcp (𝑐)K ⊑ (𝜋0,𝜋1 ) J𝑐K ≜ JTcp (𝑐)K.(err) ⊆ 𝛾𝜋D0 (∅, J𝑐K.(err)), and                               (59)
                                                  
                                                  
                                                   JT (𝑐)K.(dvg) ⊆ 𝛾 D (J𝑐K.(dvg), J𝑐K.(err))
                                                   cp                 𝜋0

7.5    Kripke Relations for Cminorgen
CompCert employs a hierarchy of memory relations—ranging from simple identity to extension
and, in the most intricate cases, memory injection. Each phase is thus verified with the weakest
relation sufficient for capturing its memory effects, which keeps proofs as lightweight as possible.
   Among phases of CompCert, Cminorgen is one of the most challenging phase: it eliminates scalar
local variables that are never addressed with the & operator from activation records and coalesces
separate memory blocks allocated to addressed local variables within a function activation into
a single block representing the activation record as a whole, thus reshaping memory layout in a
nontrivial way. In the original CompCert proof, this is justified using the memory injection relation.
In our framework, we recast this verification by exposing memory injections in a Kripke relation.
We show key definitions as follows, where the memory model of CompCert is explained in §6.1.
  Memory injection of CompCert. CompCert introduces injection functions to track the general
correspondence between memory blocks. An injection function 𝑓 : ifun (ifun ≜ B ⇀ B × Z) is a
partial function mapping source memory blocks to target locations, in the following form:
                                           𝑓 (𝑏 1 ) = ⊥    or     𝑓 (𝑏 1 ) = (𝑏 2, 𝛿).
The former means that 𝑏 1 is unmapped, and the later means that a location in 𝑏 1 is mapped to a
target location of block 𝑏 2 with 𝛿 offset increased. Given an injection function 𝑓 , we use 𝑣 1 ↦→V𝑓 𝑣 2
to assert the correspondent of program values (naturally lifted to →−
                                                                    𝑣 ↦→V →−
                                                                           𝑣 for a list of values), and
                                                                                         1   𝑓   2
use 𝑚 1 ↦→M𝑓 𝑚 2 to represent memory injections. Specifically, a pointer value Vptr (𝑏 1, 𝑜 1 ) is injected
to Vptr (𝑏 2, 𝑜 2 ) if there is a 𝛿 ∈ Z s.t. 𝑓 (𝑏 1 ) = (𝑏 2, 𝛿) and 𝑜 2 = 𝑜 1 + 𝛿; integers or floating numbers
are injected if the source value is identical to the target value; and the special value Vundef can be
injected to any values. Memory injection 𝑚 1 ↦→M𝑓 𝑚 2 holds if memory contents in 𝑚 1 are preserved
to 𝑚 2 for all injected addresses (simplified for presentation purposes), i.e.,
             for any 𝑏 1 𝑏 2 𝑜 1 𝑜 2, Vptr (𝑏 1, 𝑜 1 ) ↦→V𝑓 Vptr (𝑏 2, 𝑜 2 ) ⇒ 𝑚 1 (𝑏 1, 𝑜 1 ) ↦→V𝑓 𝑚 2 (𝑏 2, 𝑜 2 ).

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                                                   5:39


  We reuse the notion of Kripke memory relation for protection called injp [Koenig and Shao 2021;
Zhang et al. 2024] to formulate rely-guarantee reasoning [Liang et al. 2012] in our framework.
   Definition 7.35 (The Kripke memory relation injp). injp ≜ ⟨𝑊injp, {injp, 𝑅injp ⟩, where 𝑊injp ≜
ifun × mem × mem, 𝑅injp : K𝑊injp ( mem, mem) is a Kripke relation between memory states such that

                                ∀𝑓 𝑚 1 𝑚 2, (𝑚 1, 𝑚 2 ) ∈ 𝑅injp (𝑓 , 𝑚 1, 𝑚 2 ) ⇔ 𝑚 1 ↦→M𝑓 𝑚 2
and {injp (⊆ 𝑊injp × 𝑊injp ) is an accessibility relation s.t. for any worlds (𝑓 , 𝑚 1, 𝑚 2 ), (𝑓 ′, 𝑚 1′ , 𝑚 2′ ),
                                                           
                                                            (1) unmapped (𝑓 ) ⊆ unchanged_on (𝑚 1, 𝑚 1′ );
                                                           
                                                           
                                                           
                                                            (2) out_of_reach (𝑓 , 𝑚 1 ) ⊆ unchanged_on (𝑚 2, 𝑚 ′ );
                                                                                                                            2
           (𝑓 , 𝑚 1, 𝑚 2 ) {injp (𝑓 ′, 𝑚 1′ , 𝑚 2′ ) ⇔
                                                           
                                                            (3) separately_increased (𝑓 , 𝑓 ′, 𝑚 1, 𝑚 2 ); and
                                                           
                                                           
                                                            (4) mem_forward (𝑚 , 𝑚 ′ ) ∧ mem_forward (𝑚 , 𝑚 ′ ).
                                                                              1    1                        2  2

Here unchanged_on (𝑚, 𝑚 ′ ) denotes the set of memory locations where the memory contents remain
unchanged between 𝑚 and 𝑚 ′ . Clause (1) asserts that values at locations unmapped by 𝑓 remain
unchanged. Clause (2) indicates that values at locations not mapped to by 𝑓 from valid blocks of
𝑚 1 are also unchanged. Clause (3) states that 𝑓 ′ extends 𝑓 by adding mappings for new blocks
while preserving the existing mappings, and new blocks are not permitted to map into the existing
memory blocks of 𝑚 2 . Clause (4) represents side conditions that are not essential to the core idea.
   Intuitively, the relation {injp governs the evolution of worlds across internal executions and ex-
ternal calls while enforcing disciplined memory protection. Concretely, private and public memory
locations are identified by an injection 𝑓 : public locations are those related by 𝑓 , whereas private
locations are either unmapped in the source or out-of-reach in the target (having no preimage
through 𝑓 ). During world evolution, memory cells at private locations must remain unchanged,
ensuring that the environment cannot observe or modify them, while public locations are preserved
up to the injection so that loads, stores, and pointer comparisons behave consistently between the
source and target. These constraints enable injp to account for complex memory transformations,
such as allocating new stack slots for spilled register variables, reorganizing stack frames, and
extending or coalescing memory blocks across compilation phases, while preserving behavioral
consistency, as demonstrated in CompCertO [Koenig and Shao 2021; Zhang et al. 2024].
   The Kripke memory relation injp can be naturally integrated into our framework as follows.
   Definition 7.36 (The Kripke relation for Statement Transformation of Cminorgen). Given the set of
program states state𝑠 , state𝑡 (respectively for Csharpminor and Cminor), where state𝑠 = state𝑡 ≜
tenv × mem. We define the Kripke relation 𝑅𝐵 : K𝑊injp ( state𝑠 , state𝑡 ) for Cminorgen as follows, for
any (𝑓 , 𝑚 1, 𝑚 2 ) ∈ 𝑊injp , (𝑡𝑒 1, 𝑚 1 ) ∈ state𝑠 , and (𝑡𝑒 2, 𝑚 2 ) ∈ state𝑡 ,
                                        
              (𝑡𝑒 1, 𝑚 1 ), (𝑡𝑒 2, 𝑚 2 ) ∈ 𝑅𝐵 (𝑓 , 𝑚 1, 𝑚 2 ) ⇔ 𝑚 1 ↦→M𝑓 𝑚 2 ∧ ∀𝑥, 𝑡𝑒 1 (𝑥) ↦→V𝑓 𝑡𝑒 2 (𝑥)

   Definition 7.37 (The Kripke interface relation for Cminorgen). 𝐴C ≜ ⟨𝑊injp, {injp, 𝑅C , 𝑅𝑟C ⟩, where
                                                                                                                         𝑞

for any C queries 𝑞 1 = (𝑖𝑑 1, →           −
                                           𝑣 1 , 𝑚 1 ), 𝑞 2 = (𝑖𝑑 2, →−
                                                                      𝑣 2 , 𝑚 2 ), and C replies 𝑟 1 = (𝑣 1′ , 𝑚 1′ ), 𝑟 2 = (𝑣 2′ , 𝑚 2′ ),
                                                      
           (𝑖𝑑 1, →
                  −
                  𝑣 1 , 𝑚 1 ), (𝑖𝑑 2, →  −
                                         𝑣 2 , 𝑚 2 ) ∈ 𝑅C (𝑓 , 𝑚 1, 𝑚 2 ) ⇔ 𝑖𝑑 1 = 𝑖𝑑 2 ∧ →         −
                                                                                                    𝑣 1 ↦→V𝑓 →
                                                                                                             −
                                                            𝑞
                                                                                                             𝑣 2 ∧ 𝑚 1 ↦→M𝑓 𝑚 2
                                                     
                       (𝑣 1′ , 𝑚 1′ ), (𝑣 2′ , 𝑚 2′ ) ∈ 𝑅𝑟C (𝑓 ′, 𝑚 1′ , 𝑚 2′ ) ⇔ 𝑣 1′ ↦→V𝑓 ′ 𝑣 2′ ∧ 𝑚 1′ ↦→M𝑓 ′ 𝑚 2′

   Using the above Kripke relations (with 𝐴 = 𝐵 ≜ 𝐴C in Def. 7.31), we have successfully reverified
Cminorgen—one of the most intricate memory-reorganizing phases in CompCert—within our
framework, which indicates that our proof techniques are scalable to the remainder of CompCert.

      ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:40                                                                                                  Z. Cheng et al.


                           Σ𝑁                 Σ𝐸                                        𝜏
           𝜎𝑠′
                     𝜏                             𝜏0              𝜎𝑠                                    𝜎𝑠′
                                                                              𝑁𝑠 ∪ ( 𝐸e𝑠 × state𝑠 )
                                𝜎𝑠       𝜎𝑒
                     𝑁𝑠                            𝐸𝑠

          𝑅          𝛾𝑅N    𝑅        ∪        𝑅    𝛾𝑅E 𝜏0 ⩽𝑇 𝜏     𝑅                                    𝑅

                     𝜏                              𝜏                                   𝜏
           𝜎𝑡′                  𝜎𝑡       𝜎𝑡              𝜎𝑡′       𝜎𝑡                                    𝜎𝑡′
                     𝑁𝑡                            𝑁𝑡                                  𝑁𝑡
              (a) Behavior refinement of choice 1                      (b) Behavior refinement of choice 2

Fig. 10. Choice 1 separates correspondences for normal termination and abortion using distinct 𝛾-instances,
but they fail to cover full cases: 𝛾𝑅N fails for (Σ𝐸 − Σ𝑁 ) and 𝛾𝑅E fails for (Σ𝑁 − Σ𝐸 ). Choice 2 forces uniform
correspondence between the final states, even when the target terminates normally but the source aborts.


7.6      Design Choices
In this subsection, we explain why 𝛾 is designed to take two arguments rather than just one. For
illustration, recall that Example 7.4 defines the preservation of terminating behaviors as follows.
  J𝑡K.( nrm)­𝑅 (J𝑠K.( nrm), J𝑠K.( err)) ≜ ∀𝜎𝑡 𝜏 𝜎𝑡′ 𝜎𝑠 , (𝜎𝑡 , 𝜏, 𝜎𝑡′ ) ∈ J𝑡K.(nrm) ⇒ (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅 ⇒
                                                                                                          (60)
                ∃𝜎𝑠′, (𝜎𝑠 , 𝜏, 𝜎𝑠′ ) ∈ J𝑠K.(nrm) ∧ (𝜎𝑠′, 𝜎𝑡′ ) ∈ 𝑅 ∨ ∃𝜏0, (𝜎𝑠 , 𝜏0 ) ∈ J𝑠K.(err) ∧ 𝜏0 ⩽𝑇 𝜏 ;
where the termination behavior of a target program may correspond either to the terminating
behavior of the source program or to its aborting behavior, with different requirements: starting
from related initial states, the former requires the final states to be related, whereas the latter does
not. We next show that designing 𝛾-functions with a single parameter would be less flexible to
meet the two different requirements than that with two parameters by contraposition. Specifically,
suppose we intended to find instances of 𝛾 : S → T to encode Formula (60) for algebraic reasoning.
There may exist two choices, and they must satisfy the soundness conditions as follows.
                                                                                                 
   Chioce 1: 𝑁𝑡 ⊆ 𝛾𝑅N (𝑁𝑠 ) ∪ 𝛾𝑅E (𝐸𝑠 ) × state𝑡 ;       Choice 2: 𝑁𝑡 ⊆ 𝛾𝑅N 𝑁𝑠 ∪ ( 𝐸e𝑠 × state𝑠 )    (61)
                                                                   
   Soundness of chioce 1:                N           E
                                  𝑁𝑡 ⊆ 𝛾𝑅 (𝑁𝑠 ) ∪ 𝛾𝑅 (𝐸𝑠 ) × state𝑡 ⇒ 𝑁𝑡 ­𝑅 (𝑁𝑠 , 𝐸𝑠 )               (62)
                                                                
   Soundness of choice 2:         𝑁𝑡 ⊆ 𝛾𝑅N 𝑁𝑠 ∪ ( 𝐸e𝑠 × state𝑠 ) ⇒ 𝑁𝑡 ­𝑅 (𝑁𝑠 , 𝐸𝑠 )                  (63)
       where 𝐸e𝑠 ≜ { (𝜎, 𝜏) ∈ state𝑠 × trace | ∃𝜏0 𝜏1, (𝜎, 𝜏0 ) ∈ 𝐸𝑠 ∧ 𝜏 = 𝜏0 · 𝜏1 }
                 𝛾𝑅N : P ( state𝑠 × trace × state𝑠 ) → P ( state𝑡 × trace × state𝑡 )                              (64)
                 𝛾𝑅E : P ( state𝑠 × trace) → P ( state𝑡 × trace)
where in Choice 2 we employ a trace-extension operator 𝐸e𝑠 for the source aborting behavior 𝐸𝑠
such that the observable event trace of 𝐸𝑠 can be a prefix of the target terminating behavior 𝑁𝑡 . In
fact, we can define the following instances of 𝛾 that satisfy the above soundness conditions.
                    
          𝛾𝑅N (𝑁 ) ≜ (𝜎𝑡 , 𝜏, 𝜎𝑡′ ) ∀𝜎𝑠 , (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅 ⇒ (∃𝜎𝑠′, (𝜎𝑠 , 𝜏, 𝜎𝑠′ ) ∈ 𝑁 ∧ (𝜎𝑠′, 𝜎𝑡′ ) ∈ 𝑅) (65)
              𝛾𝑅E (𝐸) ≜ { (𝜎𝑡 , 𝜏) | ∀𝜎𝑠 , (𝜎𝑠 , 𝜎𝑡 ) ∈ 𝑅 ⇒ ∃𝜏0, (𝜎𝑠 , 𝜏0 ) ∈ 𝐸 ∧ 𝜏0 ⩽𝑇 𝜏 }                       (66)

   Choice 1 employs distinct instances of 𝛾 to separately capture the two correspondences between
source and target behaviors. The instance 𝛾𝑅N characterizes cases where, from any related initial
state, the source program may terminate normally with a matching final state. The instance 𝛾𝑅E char-
acterizes cases where, from any related initial state, the source program may abort. However, there
may exist related source states from which the source program does not terminate or does not abort.

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                             5:41

                                     
More specifically, we define Σ𝑁 ≜ 𝜎𝑠 ∃𝜏 𝜎𝑠′, (𝜎𝑠 , 𝜏, 𝜎𝑠′ ) ∈ 𝑁𝑠 , and Σ𝐸 ≜ { 𝜎𝑒 | ∃𝜏, (𝜎𝑒 , 𝜏) ∈ 𝐸𝑠 },
which respectively denotes the set of initial states for termination and abortion. As illustrated in
Fig. 10, those states in Σ𝑁 but not in Σ𝐸 are not properly quantified by 𝛾𝑅E , and those states in Σ𝐸 but
not in Σ𝑁 are not properly quantified by 𝛾𝑅N . Simply taking the union of 𝛾𝑅N and 𝛾𝑅E does not solve
this problem. Choice 2 avoids this issue by taking the union of 𝑁𝑠 and 𝐸e𝑠 × state𝑠 first. This enforces
a uniform treatment of normal termination and abortion, aligning both with the target’s normal
termination. As a result, whenever the source program aborts, one must provide an artificial final
source state related to the actual target final state, even though aborted executions do not yield
canonical final states. That is, for any target state there must exist a related source state, which
may not in fact exist. This additional requirement is unnatural and often infeasible under general
state-matching relations. Therefore, both choices are ill-suited for realistic compiler verification. By
contraposition, we conclude that it would be more challenging to instantiate a single-parameterized
𝛾 for algebraic compiler verification, especially when the source semantics is nondeterministic.

8     Compositional Correctness
Refinement algebras further enhance the compositionality of compiler verification. The semantic
operators in extended KATs enable the semantic composition of program substructures, while
refinement algebras support the compositionality of behavioral refinement. Their strong algebraic
properties allow us to design automated proof tactics to mechanize compiler verification. In this
section, taking the transformation of Clight statements in Cshmgen as an example, we first show
the proof style of our framework in §8.1, along with two essential automated tactics. We then
present the correctness of compilation phases in §8.2 and the module-level compositionality in §8.3.

8.1    Proof Style


           TCshmgens (𝑛𝑏 , 𝑛𝑐 , 𝑠 1 ) = Succeed(𝑢 1 ) ∧ TCshmgens (𝑛𝑏 , 𝑛𝑐 , 𝑠 2 ) = Succeed(𝑢 2 )
                                                                                                   Seq
                                TCshmgens (𝑛𝑏 , 𝑛𝑐 , 𝑠 1 ; 𝑠 2 ) = Succeed(𝑢 1 ; 𝑢 2 )
                                                  Brk                                                          Ctn
TCshmgens (𝑛𝑏 , 𝑛𝑐 , break) = Suc.(exit 𝑛𝑏 )              TCshmgens (𝑛𝑏 , 𝑛𝑐 , continue) = Suc.(exit 𝑛𝑐 )
          TCshmgens (1, 0, 𝑠 1 ) = Succeed(𝑢 1 ) ∧ TCshmgens (0, 𝑛𝑐 + 1, 𝑠 2 ) = Succeed(𝑢 2 )
                                                                                            Loop
           TCshmgens (𝑛𝑏 , 𝑛𝑐 , loop 𝑠 1 𝑠 2 ) = Succeed block{Sloop (block {𝑢 1 }; 𝑢 2 )}

    Fig. 11. Original Cshmgen rules from CompCert (selectively listed), where Suc. is short for Succeed.

   The proof style in our framework is demonstrated by the following proof sketch of Lemma
8.1, where TCshmgens denotes the statement translation of Cshmgen, with selected compilation
rules shown in Fig. 11. We next omit the 𝑅𝐵 , defined in Def. 7.30, for the behavior refinement
⊑ (𝑅𝐵 ,𝑛𝑏 ,𝑛𝑐 ,𝜒𝑒 ) .
  Lemma 8.1. For any natural numbers 𝑛𝑏 , 𝑛𝑐 , and callee function behaviors 𝜒𝑡 , 𝜒𝑠 , 𝜒𝑒 , if 𝑛𝑏 ≠ 𝑛𝑐
and 𝜒𝑡 ⊆ 𝛾𝑅N𝐵 ( 𝜒𝑠 , 𝜒𝑒 ), then for any Clight statement 𝑠 and Csharpminor statement 𝑢,
                    if TCshmgens (𝑛𝑏 , 𝑛𝑐 , 𝑠) = Succeed(𝑢), then J𝑢K 𝜒𝑡 ⊑ (𝑛𝑏 ,𝑛𝑐 ,𝜒𝑒 ) J𝑠K 𝜒𝑠 .
   Proof sketch. By induction on the statement 𝑠, we derive proof obligations asserting that for
every syntactic construct of 𝑠, if each substructure of 𝑠 satisfies the refinement relation with its
compiled counterpart, then the entire statement 𝑠 does as well. To illustrate how the refinement
algebra works in the proof, we demonstrate the core ideas behind three key proof obligations.

      ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:42                                                                                                                         Z. Cheng et al.


  Case 1: 𝑠 is a sequential statement. By induction, since TCshmgens (𝑛𝑏 , 𝑛𝑐 , 𝑠 1 ; 𝑠 2 ) = Succeed(𝑢), then
TCshmgens (𝑛𝑏 , 𝑛𝑐 , 𝑠 1 ) = Succeed(𝑢 1 ), TCshmgens (𝑛𝑏 , 𝑛𝑐 , 𝑠 2 ) = Succeed(𝑢 2 ), and 𝑢 = 𝑢 1 ; 𝑢 2 . Prove that:
   if J𝑢 1 K 𝜒𝑡 ⊑ (𝑛𝑏 ,𝑛𝑐 ,𝜒𝑒 ) J𝑠 1 K 𝜒𝑠 and J𝑢 2 K 𝜒𝑡 ⊑ (𝑛𝑏 ,𝑛𝑐 ,𝜒𝑒 ) J𝑠 2 K 𝜒𝑠 , then J𝑢 1 ; 𝑢 2 K 𝜒𝑡 ⊑ (𝑛𝑏 ,𝑛𝑐 ,𝜒𝑒 ) J𝑠 1 ; 𝑠 2 K 𝜒𝑠 . (67)
For the sake of brevity, let 𝑁𝑖 , 𝐸𝑖 and 𝐶𝑖 respectively represent J𝑠𝑖 K 𝜒𝑠 .(nrm), J𝑠𝑖 K 𝜒𝑠 .(err) and J𝑠𝑖 K 𝜒𝑠 .(cll)
for 𝑖 = 1, 2. The proofs for the refinement of terminating behaviors are shown as follows.
                             J𝑢 1 ; 𝑢 2 K 𝜒𝑡 .(nrm) = J𝑢 1 K 𝜒𝑡 .(nrm) ◦ J𝑢 2 K 𝜒𝑡 .(nrm)                                                (68)
                             ⊆ 𝛾𝑅N𝐵 (𝑁 1, 𝐸 1 ∪ 𝐶 1 ◦ 𝜒𝑒 ) ◦ 𝛾𝑅N𝐵 (𝑁 2, 𝐸 2 ∪ 𝐶 2 ◦ 𝜒𝑒 )                                                 (69)
                             ⊆ 𝛾𝑅N𝐵 (𝑁 1 ◦ 𝑁 2, (𝐸 1 ∪ 𝐶 1 ◦ 𝜒𝑒 ) ∪ 𝑁 1 ◦ (𝐸 2 ∪ 𝐶 2 ◦ 𝜒𝑒 ))                                             (70)
                             ⊆ 𝛾𝑅N𝐵 (𝑁 1 ◦ 𝑁 2, (𝐸 1 ∪ 𝑁 1 ◦ 𝐸 2 ) ∪ (𝐶 1 ∪ 𝑁 1 ◦ 𝐶 2 ) ◦ 𝜒𝑒 )                                           (71)
                             = 𝛾𝑅N𝐵 (J𝑠 1 ; 𝑠 2 K 𝜒𝑠 .(nrm), J𝑠 1 ; 𝑠 2 K 𝜒𝑠 .(err) ∪ J𝑠 1 ; 𝑠 2 K 𝜒𝑠 .(cll) ◦ 𝜒𝑒 )                      (72)
The key to the above proofs is the inclusion (69) ⊆ (70), which is directly solved by the concatenation-
preserved property of RAs. The inclusion (70) ⊆ (71) is by the axioms of Kleene Algebras; the
inclusion (68) ⊆ (69) is by hypotheses; and the equivalence in (68) and between (71) ∼ (72) holds by
definition. We see that refinement algebras reduce refinement proofs into the proof of relational
propositions in Kleene Algebras. Other cases for sequential statements can be proved similarly.
  Case 2: 𝑠 is a loop statement. By structural induction, the proof goal for the terminating case for
example is to show: if J𝑢 1 K 𝜒𝑡 ⊑ (1,0,𝜒𝑒 ) J𝑠 1 K 𝜒𝑠 and J𝑢 2 K 𝜒𝑡 ⊑ (0,𝑛𝑐 +1,𝜒𝑒 ) J𝑠 2 K 𝜒𝑠 , then
              Jblock{Sloop (block {𝑢 1 }; 𝑢 2 )}K 𝜒𝑡 .(nrm) ⊆
                                                                                                                                        (73)
                     𝛾𝑅N𝐵 Jloop 𝑠 1 𝑠 2 K 𝜒𝑠 .(nrm), Jloop 𝑠 1 𝑠 2 K 𝜒𝑠 .(err) ∪ (Jloop 𝑠 1 𝑠 2 K 𝜒𝑠 .(cll) ◦ 𝜒𝑒 )
Since the semantics of loops is defined with extended KATs operators ∗ (for the reflexive transitive
closure) and ∞ (for the infinite iterations of composition), the behavior refinement between them
can be efficiently verified using the instances of star-preserved RAs and infinity-preserved RAs.
   In our Rocq implementation, proof obligations for composition statements (e.g., case 1 and case 2)
is mechanically solved by two automated new proof tactics: gamma_simpl and solvefix. The gamma_simpl
tactic automatically reduces the behavior refinement between source and target programs to
relational propositions of extended KATs, by properties of refinement algebras. The solvefix tactic
mechanically verifies these relational propositions by properties of extended KATs. More specifically,
by unfolding the definition of the left-hand side of Formula (73), the goal is to show:
                                                                  ∗
        (J𝑢 1 K 𝜒𝑡 .(nrm) ∪ J𝑢 1 K 𝜒𝑡 .(blk)0 ) ◦ J𝑢 2 K 𝜒𝑡 .(nrm) ◦
                                                                                             
          J𝑢 1 K 𝜒𝑡 .(blk)1 ∪ ((J𝑢 1 K 𝜒𝑡 .(nrm) ∪ J𝑢 1 K 𝜒𝑡 .(blk)0 ) ◦ J𝑢 2 K 𝜒𝑡 .(blk)0 )
                     ⊆ 𝛾𝑅N𝐵 (Jloop 𝑠 1 𝑠 2 K 𝜒𝑠 .(nrm), Jloop 𝑠 1 𝑠 2 K 𝜒𝑠 .(err) ∪ (Jloop 𝑠 1 𝑠 2 K 𝜒𝑠 .(cll) ◦ 𝜒𝑒 ))
We then use the induction hypothesis to rewrite every set of the left-hand side of this goal, and
remember J𝑠𝑖 K 𝜒𝑠 .(err) ∪ (J𝑠𝑖 K 𝜒𝑠 .(cll)) ◦ 𝜒𝑒 ) as 𝐸𝑖 for brevity. The proof goal is reduced to:
                                                                                                  ∗
   (𝛾𝑅N𝐵 (J𝑠 1 K 𝜒𝑠 .(nrm), 𝐸 1 ) ∪ 𝛾𝑅N𝐵 (J𝑠 1 K 𝜒𝑠 .(ctn), 𝐸 1 )) ◦ 𝛾𝑅N𝐵 (J𝑠 2 K 𝜒𝑠 .(nrm), 𝐸 2 ) ◦
                                                                                                                                      
      𝛾𝑅N𝐵 (J𝑠 1 K 𝜒𝑠 .(brk), 𝐸 1 ) ∪ (𝛾𝑅N𝐵 (J𝑠 1 K 𝜒𝑠 .(nrm), 𝐸 1 ) ∪ 𝛾𝑅N𝐵 (J𝑠 1 K 𝜒𝑠 .(ctn), 𝐸 1 )) ◦ 𝛾𝑅N𝐵 (J𝑠 2 K 𝜒𝑠 .(brk), 𝐸 2 )
                     ⊆ 𝛾𝑅N𝐵 (Jloop 𝑠 1 𝑠 2 K 𝜒𝑠 .(nrm), Jloop 𝑠 1 𝑠 2 K 𝜒𝑠 .(err) ∪ (Jloop 𝑠 1 𝑠 2 K 𝜒𝑠 .(cll) ◦ 𝜒𝑒 ))                   (74)
By applying properties of underlying RA instances (using gamma_simpl), we reduce the proof goal to:
                                                              ∗
     (J𝑠 1 K 𝜒𝑠 .(nrm) ∪ J𝑠 1 K 𝜒𝑠 .(ctn)) ◦ J𝑠 2 K 𝜒𝑠 .(nrm) ◦
                                                                                                                       (75)
             J𝑠 1 K 𝜒𝑠 .(brk) ∪ ((J𝑠 1 K 𝜒𝑠 .(nrm) ∪ J𝑠 1 K 𝜒𝑠 .(ctn)) ◦ J𝑠 2 K 𝜒𝑠 .(brk)) ⊆ Jloop 𝑠 1 𝑠 2 K 𝜒𝑠 .(nrm);

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                                                  5:43

                                                                   ∗
        (J𝑠 1 K 𝜒𝑠 .(nrm) ∪ J𝑠 1 K 𝜒𝑠 .(ctn)) ◦ J𝑠 2 K 𝜒𝑠 .(nrm)        ◦
               𝐸 1 ∪ (𝐸 1 ∪ 𝐸 1 ) ∪ ((J𝑠 1 K 𝜒𝑠 .(nrm) ∪ J𝑠 1 K 𝜒𝑠 .(ctn)) ◦ 𝐸 2 )
                                                                                                                                    (76)
                     ∪ (𝐸 1 ∪ 𝐸 1 ) ∪ ((J𝑠 1 K 𝜒𝑠 .(nrm) ∪ J𝑠 1 K 𝜒𝑠 .(ctn)) ◦ 𝐸 2 )
                                                        ⊆ Jloop 𝑠 1 𝑠 2 K 𝜒𝑠 .(err) ∪ (Jloop 𝑠 1 𝑠 2 K 𝜒𝑠 .(cll) ◦ 𝜒𝑒 ).
Finally, by properties of extended KATs (using tactic solvefix), proof goals (75) and (76) are solved.
   Although these equations may appear lengthy, they are actually quite intuitive. For instance, the
left-hand side of Formula (75) says that after repeatedly executing 𝑠 1 and 𝑠 2 several times—where
each time either 𝑠 1 terminates normally, or 𝑠 1 exits early due to a continue and then 𝑠 2 terminates
normally—iterated execution may either break in 𝑠 1 or 𝑠 2 . This behavior is precisely the semantics of
the loop on the right-hand side. Therefore, using automated proof tactics to solve them is suitable.

                                         𝜒𝑠                                     Jcall 𝑖K 𝜒𝑠 .(nrm)
                                𝑔𝑠                𝑔𝑠′              (𝑙𝑠 , 𝑔𝑠 )                        (𝑙𝑠 , 𝑔𝑠′ )

                            𝑅𝐴                          𝑅𝐴 ⇒ 𝑅𝐵                                             𝑅𝐵

                                         𝜒𝑡                                     Jcall 𝑖K 𝜒𝑡 .(nrm)
                                𝑔𝑡                𝑔𝑡′              (𝑙𝑡 , 𝑔𝑡 )                        (𝑙𝑡 , 𝑔𝑡′ )

Fig. 12. Proofs for the refinement of procedure calls. Here, 𝑅𝐴 relates global states, and 𝑅𝐵 relates pairs of local
and global states. They satisfy that for any 𝑙𝑠 , 𝑔𝑠 , and 𝑙𝑡 , 𝑔𝑡 , if ((𝑙𝑠 , 𝑔𝑠 ), (𝑙𝑡 , 𝑔𝑡 )) ∈ 𝑅𝐵 , then (𝑔𝑠 , 𝑔𝑡 ) ∈ 𝑅𝐴 . After
procedure calls, if 𝑙𝑠 and 𝑙𝑡 is already related in 𝑅𝐵 , and for any 𝑔𝑠′ , 𝑔𝑡′ , (𝑔𝑠′ , 𝑔𝑡′ ) ∈ 𝑅𝐴 , then ((𝑙𝑠 , 𝑔𝑠′ ), (𝑙𝑡 , 𝑔𝑡′ )) ∈ 𝑅𝐵 .


   Case 3: 𝑠 is a call statement. In our framework, the behavior refinement of procedure calls before
and after the compilation depends on that of callee procedures. We use the PCALL language to
illustrate the key idea of proofs for simplicity, as shown in Fig. 12. The refinement of the caller’s
behavior is derived from the refinement of the callee’s behavior. The correspondence between local
states is preserved since they remain unchanged before and after the procedure call. The behavior
refinement between Clight function calls and the compiled Csharpminor function calls is proved in
a similar way, with additional considerations for arguments and return values.
   It’s worth noting that the behavior refinement of atomic statements has no algebraic structure
and is verified directly according to their definitions. We reuse some of CompCert original proofs
for these cases, such as those for the transformation of expressions.                              □
   Summary. In our framework, almost all the proofs (including proofs of all the theorems in §8.2
and §8.3) have the following main proof steps (as shown in the proof of Lemma 8.1):
     • By the algebraic properties of refinement algebras such as (51) ∼ (52) and (57) ∼ (58), the
       behavior refinement between substructures are composed into an overall refinement, without
       unfolding the concrete definition of 𝛾𝑅N𝐵 (except for proofs for atomic statements);
     • By the properties of extended KATs, proofs are finished in a purely relational subsystem.
These two proof steps are automated in Rocq by our new gamma_simpl tactic and solvefix tactic.
For clarity, we illustrate the corresponding Rocq proofs to the first two proof cases of Lemma 8.1
in Fig. 13, where a predicate (refines nbrk nctn dt ds Hree) means the denotation dt of Clit.Denote re-
fines the denotation ds of Cshm.Denote, namely dt ⊑ ( nbrk,nctn,Hree ) ds, corresponding to J𝑢K 𝜒𝑡 ⊑ (𝑛𝑏 ,𝑛𝑐 ,𝜒𝑒 )
J𝑠K 𝜒𝑠 defined in Def. 7.30. In other words, Fig. 13a means the proof obligation of Formula (67); and
Fig. 13b means that if J𝑢 1 K 𝜒𝑡 ⊑ (1,0,𝜒𝑒 ) J𝑠 1 K 𝜒𝑠 and J𝑢 2 K 𝜒𝑡 ⊑ (0,𝑛𝑐 +1,𝜒𝑒 ) J𝑠 2 K 𝜒𝑠 , then
                        Jblock{Sloop (block {𝑢 1 }; 𝑢 2 )}K 𝜒𝑡 ⊑ (𝑛𝑏 ,𝑛𝑐 ,𝜒𝑒 ) Jloop 𝑠 1 𝑠 2 K 𝜒𝑠 .                                  (77)

      ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:44                                                                                                  Z. Cheng et al.


   Lemma seq_sem_refines:                          Lemma loop_sem_refines:
     forall ds1 ds2 dt1 dt2 nbrk ncnt Hree           forall nbrk ncnt Hree dt1 dt2 ds1 ds2 ( NEQ: nbrk <> ncnt)
     ( EQ1: refines nbrk ncnt dt1 ds1 Hree)          ( EQ1: refines 1 0 dt1 ds1 Hree)
     ( EQ2: refines nbrk ncnt dt2 ds2 Hree),         ( EQ2: refines 0 ( S ncnt) dt2 ds2 Hree),
     refines nbrk ncnt (seq_sem dt1 dt2)             refines nbrk ncnt
              ( Clit.seq_sem ds1 ds2) Hree.             ( Sblock_sem (loop_sem (seq_sem (Sblock_sem dt1) dt2)))
   Proof.                                               ( Clit.loop_sem ds1 ds2) Hree.
     preprocess;handle_special;                    Proof.
     try_rewrite EQ1;try_rewrite EQ2;                preprocess; try_rewrite EQ1; try_rewrite EQ2;
     gamma_simpl;fold_callee Hree;                   gamma_simpl;handle_special; repeat empty_simpl;
     solvefix.                                         gamma_simpl;fold_callee Hree;solvefix.
   Qed.                                             Qed.

       (a) Lemma seq_sem_refines                                 (b) Lemma loop_sem_refines

          Fig. 13. Refinement proofs for sequential and looping cases by automated Rocq tactics.


   Three key tactics are employed in the proofs of Fig. 13: try_rewrite, gamma_simpl and solvefix. The
tactic try_rewrite reduces proof goals by rewriting with the refinement conditions, typically of the
form 𝑥 ⊆ 𝛾 (𝑦, 𝑧). The tactic gamma_simpl discharges 𝛾-instances by exploiting the algebraic properties
of the underlying RA instances. The tactic solvefix resolves KAT (in-)equations by applying the
equational laws of Kleene algebra with tests. Several auxiliary tactics are also used for supporting
purposes, such as preprocess for unfolding definitions and simplifying by definitional equalities,
empty_simpl for eliminating empty sets, and handle_special for handling special operators.

   Remark. The solvefix tactic is designed for KAT (in-)equations and can also handle simple
equations with infinity operators (i.e., those grammatically equal), which are sufficient in our
setting. More general cases with infinity operators are undecidable and must be handled manually.
Atomic statements lack algebraic structure and are therefore verified directly by their definitions.

8.2    Compilation Correctness
The CompCert front-end compiles Clight to Cminor through the Cshmgen and Cminorgen phases.
We use TCshmgenf for the transformation of Clight functions by Cshmgen, and TCmingenf for the
transformation of Csharpminor functions by Cminorgen, whose correctness is shown as follows.
8.2.1 Compilation Correctness from Clight to Cminor. We first define the identity Kripke interface
relation as: 𝐴U ≜ ⟨Unit, {U, 𝜆𝑤 .1, 𝜆𝑤 .1⟩, {U ≜ Unit × Unit, and Unit denotes a unit set. The KIR 𝐴C
is defined in Def. 7.37, and “⊑_↠_ ” is defined in Def. 7.31. We then have the following theorems.
   Theorem 8.2 (Cshmgen correctness). For any Clight function 𝐹𝑠 and Csharpminor function 𝐹𝑢 ,
                        if TCshmgenf (𝐹𝑠 ) = Succeed(𝐹𝑢 ), then J𝐹𝑢 K ⊑𝐴U ↠𝐴U J𝐹𝑠 K.
  Remark that Thm. 8.2 is deduced from the translation correctness of Clight statements (i.e.,
Lemma 8.1), and the original CompCert proof is reused for verifying the translation of initialization
when entering the function and the translation of memory releasing when leaving the function.
   Theorem 8.3 (Cminorgen correctness). For any Csharpminor function 𝐹𝑢 , Cminor function 𝐹𝑡 ,
                        if TCmingenf (𝐹𝑢 ) = Succeed(𝐹𝑡 ), then J𝐹𝑡 K ⊑𝐴C ↠𝐴C J𝐹𝑢 K.
8.2.2 Optimization Correctness. To demonstrate the applicability of our approach beyond the
CompCert front-end, we model typical back-end optimizations of CompCert (i.e., standard constant

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                               5:45


propagation and dead code elimination) on extended PCALL and CFG languages that additionally ac-
count for event traces. We refer to these as trace-enriched PCALL/CFG languages. Their denotations
have the signature FDenote, and the associated correctness theorems are given as follows.
  Theorem 8.4 (Soundness of constant propagation on PCALL). If a trace-enriched PCALL
program 𝑝 is optimized into Tcp (𝑝) by constant propagation, then JTcp (𝑝)K ⊑𝐴U ↠𝐴U J𝑝K.
  Theorem 8.5 (Soundness of dead code elimination on PCALL). If a trace-enriched PCALL
program 𝑝 is optimized into Tdce (𝑝) by dead code elimination, then JTdce (𝑝)K ⊑𝐴U ↠𝐴U J𝑝K.
   Similarly, we have optimization correctness on the trace-enriched control-flow-graph language.
  Theorem 8.6 (Correctness of constant propagation on CFGs). If a trace-enriched CFG 𝑝 is
optimized into Tcp (𝑝) by constant propagation, then JTcp (𝑝)K ⊑𝐴U ↠𝐴U J𝑝K.
  Theorem 8.7 (Correctness of dead code elimination on CFGs). If a trace-enriched CFG 𝑝 is
optimized into Tdce (𝑝) by dead code elimination, then JTdce (𝑝)K ⊑𝐴U ↠𝐴U J𝑝K.
   Additionally, we have the correctness of generating CFGs from syntax trees of PCALL as follows.
   Theorem 8.8 (Correctness of CFGs generation). If a trace-enriched CFG Tcfg (𝑝) is generated
from a trace-enriched PCALL program 𝑝, then JTcfg (𝑝)K ⊑𝐴U ↠𝐴U J𝑝K.

8.3    Compositional Correctness
Based on the definition of refinement between function denotations in Def. 7.31, we then have the
following results, where Lemma 8.9 helps derive the refinement of modules from the refinement of
functions, Thm. 8.10 is used to compose the correctness of each compilation phase, and Thm. 8.11
shows the correctness of module-level compositionality.
   Specifically, in our implementation, we follow CompCertO’s approach [Koenig and Shao 2021;
Zhang et al. 2024] to support vertical compositionality and use denotation-based semantic linking
along with fixed-point-related theorems to support horizontal compositionality.
   Lemma 8.9. For any open modules 𝑀𝑠 and 𝑀𝑡 , and for any Kripke interface relations 𝐴 and 𝐵,
                                 if L𝑀𝑡 M ⊑𝐴↠𝐵 L𝑀𝑠 M, then J𝑀𝑡 K ⊑𝐴↠𝐵 J𝑀𝑠 K.
   Theorem 8.10 (Vertical compositionality). For any modules 𝑀1 , 𝑀2 , 𝑀3 , and KIRs 𝐴1, 𝐴2, 𝐵 1, 𝐵 2 ,
             if J𝑀3 K ⊑𝐴2 ↠𝐵2 J𝑀2 K and J𝑀2 K ⊑𝐴1 ↠𝐵1 J𝑀1 K, then J𝑀3 K ⊑𝐴2 •𝐴1 ↠𝐵2 •𝐵1 J𝑀1 K.
   Theorem 8.11 (Horizontal compositionality). For any modules 𝑆 1 , 𝑆 2 , 𝑇1 and 𝑇2 , and a KIR 𝐴,
             if J𝑇1 K ⊑𝐴↠𝐴 J𝑆 1 K and J𝑇2 K ⊑𝐴↠𝐴 J𝑆 2 K, then J𝑇1 K ⊕ J𝑇2 K ⊑𝐴↠𝐴 J𝑆 1 K ⊕ J𝑆 2 K.
  The horizontal compositionality (termination case) is elegantly proved by the following lemma,
where 𝜇𝑥 .𝑓 (𝑥) can be (J𝑇1 K ⊕ J𝑇2 K) 𝜒𝑡 .( nrm), 𝜇𝑥 .𝑔(𝑥) can be (J𝑆 1 K ⊕ J𝑆 2 K) 𝜒𝑠 .( nrm), and 𝜇𝑥 .ℎ(𝑥) can be
(J𝑆 1 K ⊕ J𝑆 2 K) 𝜒𝑠𝑒 ( err) 13 . This lemma itself can be easily proved by induction. Other proof obligations
                  𝜒

can be systematically solved by the gamma_simpl and solvefix tactics akin to proofs for Formula (77).
  Lemma 8.12. Given a refinement algebra A = (S, E, T , 𝛾), with CPOs (S, ⊆), (E, ⊆), and (T , ⊆),
and Scott-continuous functions 𝑓 : T → T , 𝑔 : S → S, ℎ : E → E. We have:
                                                                                      
            ∀𝑁𝑡 ∈ T , 𝑁𝑠 ∈ S, 𝐸𝑠 ∈ E, 𝑁𝑡 ⊆ 𝛾 (𝑁𝑠 , 𝐸𝑠 ) ⇒ 𝑓 (𝑁𝑡 ) ⊆ 𝛾 (𝑔(𝑁𝑠 ), ℎ(𝐸𝑠 )) ⇒
                                                                   
                                𝜇𝑥 . 𝑓 (𝑥) ⊆ 𝛾 𝜇𝑥 . 𝑔(𝑥), 𝜇𝑥 . ℎ(𝑥) .
13 (J𝑆 K ⊕ J𝑆 K) 𝜒𝑒 (err) represents a fixed point equivalent to (J𝑆 K ⊕ J𝑆 K) (err) ∪ (J𝑆 K ⊕ J𝑆 K) (cll) ◦ 𝜒 .
      1      2 𝜒𝑠                                                   1      2 𝜒𝑠           1      2 𝜒𝑠         𝑒


      ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:46                                                                                                   Z. Cheng et al.


    Original invariant of Cminorgen (informal) includes:
    match_function            The source and target functions currently executed are related.
    match_statement           The source and target statements currently executed are related.
    match_continuation        The source and target continuations (control contexts) are related.
    value_inject              Function arguments and return values are related by the injection 𝑓 .
    match_memory              The source and target memories are related by injection (𝑚𝑠 ↦→M𝑓 𝑚𝑡 ).
    match_callstack           Each stack frame corresponds with the following relations:
      – match_tenv            Temporary environments correspond under injection (𝑡𝑒𝑠 ↦→E𝑓 𝑡𝑒𝑡 ).
       – match_env            Local environments are related, with pointers related by 𝑓 .
       – padding_freeable     Padding target memory between local variables can be safely released.
       – match_bounds         Local variable addresses lie in valid memory blocks (tracked by nextblock).


             Fig. 14. Informal description of the simulation invariant for Cminorgen in CompCert.


  By the horizontal compositionality (Thm. 8.11) and the equivalence between semantic linking
and syntactic linking (Thm. 4.1), we have the following separate compilation correctness.
  Lemma 8.13 (Compositional correctness of the CompCert front-end). For any Clight open
modules 𝑆 1, . . . , 𝑆𝑛 and Cminor open modules 𝑇1, . . . ,𝑇𝑛 , if 𝑇𝑖 is separately compiled from 𝑆𝑖 by the
CompCert front-end for each 𝑖, then J𝑇1 K ⊕ · · · ⊕ J𝑇𝑛 K ⊑𝐴C ↠𝐴C J𝑆 1 K ⊕ · · · ⊕ J𝑆𝑛 K.
   Theorem 8.14 (Final theorem). For any Clight open modules 𝑆 1, . . . , 𝑆𝑛 and Cminor open modules
𝑇1, . . . ,𝑇𝑛 , if 𝑇𝑖 is separately compiled from 𝑆𝑖 by the CompCert front-end for each 𝑖, then
                                    J𝑇1 + · · · + 𝑇𝑛 K ⊑𝐴C ↠𝐴C J𝑆 1 + · · · + 𝑆𝑛 K.
  Handling global environments. The global environment g maps functions to their definitions
and does not vary. Suppose that 𝐹 is a function of program 𝑃. For 𝐹 ’s semantics J𝐹 Kg , the global
environment g is loaded from the program 𝑃 following the original loading process of CompCert.
  When a compilation phase modifies the memory layout (e.g., Cminorgen), it is essential that
the global environment be preserved under memory injection. Given a global environment g, we
extend the Kripke relation 𝑅𝐵 with respect to g (denoted 𝑅𝐵g ) as follows: for any world (𝑓 , 𝑚 1, 𝑚 2 ),
       ∀𝑎 𝑏, (𝑎, 𝑏) ∈ 𝑅𝐵g (𝑓 , 𝑚 1, 𝑚 2 ) ⇔ (𝑎, 𝑏) ∈ 𝑅𝐵 (𝑓 , 𝑚 1, 𝑚 2 ) ∧ genv_preserved (g, 𝑓 , 𝑚 1, 𝑚 2 ).      (78)
Similarly, a Kripke interface relation 𝐵 = ⟨𝑊𝐵 , {𝐵 , 𝑅𝐵 , 𝑅𝐵 ⟩ is extended under a global environment
                                                               𝑞   𝑞

g, if the Kripke relations 𝑅𝐵 and 𝑅𝐵𝑟 are extended under g according to Formula (78). Readers may
                            𝑞

safely skip these technical details without compromising the conceptual grasp of our framework.

9      Comparison with small-step-based Compiler Verification
We compare our work with small-step-based approach in two aspects: (1) how we prove behavior
refinement of statements and procedures; and (2) how we support module-level compositionality.

9.1     Comparison in Behavior Refinement
The proof of behavior refinement relies on establishing an invariant (i.e., a matching relation)
between source and target program states, which must be preserved throughout execution. The
denotation-based approach, by focusing on overall outcomes rather than step-by-step processes,
simplifies the construction of such invariants and alleviates the concern of accounting for interme-
diate and nondeterminism correspondence. We illustrate the two points using concrete examples.

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                            5:47


   Simplification of program states and invariants. In our framework, we presented the definitions of
program states for CompCert front-end languages in Table 1, define the Cshmgen proof invariant
as the identity relation in Def. 7.30, and describe the Cminorgen invariant in §7.5. By comparison, a
front-end state in CompCert, illustrated here using Clight as a representative example, is originally
defined with the following structure, with Csharpminor and Cminor adopting a similar pattern.
    Clight.state = | ItnlState: function → statement → cont → env → tenv → mem → state
                   | Callstate: fundef → val → list val → cont → mem → state
                   | RtrnState: val → cont → mem → state.
Here, each state represents either: (i) an internal execution (ItnlState) of a function at a particular
statement with its continuation, local environment, temporary environment, and the current
memory; (ii) a function call (Callstate) with a function definition, arguments, continuation, and the
current memory; or (iii) a function return (RtrnState) with a return value, continuation, and the
memory. Consequently, establishing correspondences between source and target program states
requires reasoning about all components of these enriched states, as summarized in Fig. 14.
   In the original proofs of CompCert, all constraints over
these components have to be maintained at each proof                                   env other info.
                                                                             tenv
step, as illustrated in Fig. 16a. In comparison, the program
state in denotational semantics defined in Table 1 only           mem            stack-frame #1
needs to include the memory state and temporary envi-                            stack-frame #2
ronment (i.e., the real dynamic part that can be updated
by store operations or variable assignments), as colored       Fig. 15. A front-end state in CompCert.
by light red in Fig. 15. The local environment (i.e., the
static part that is not modified during the execution of statements) is treated as a parameter of the
semantic functions rather than as a component of the program state, and other information specific
to small-step semantics is not required in our state definition. Furthermore, simplifying the state
definition also reduces the complexity of establishing invariants. We quantify the simplification
offered by our framework by comparing the Rocq definitions of program states and invariants in
the CompCert front-end with that in our work in Table 4.
   In proofs, we derive the function transformation correctness from the statement (i.e., func-
tion body) transformation correctness, as illustrated in Fig. 16b. Our invariants for Cminorgen
(defined in §7.5) only involve the correspondence of dynamic parts (i.e., memory state and tempo-
rary environment), while the correspondence for static components (i.e., local environment and
padding_freeable), once established at function entry, is taken as a prerequisite for the refinement
proof of statement transformation, and is preserved until function exit through the accessibility
relation {injp (defined in §7.5). Thus, we lightened the proof burden of maintaining the invariant
in each proof step by decomposing the refinement proof into smaller and simpler obligations.

    Table 4. Comparison of program state and invariant definitions in CompCert and our framework.

   Definitions     Clit.state    Cshm.state      Cmin.state      Cshmgen.inv        Cminorgen.inv         Total
   CompCert            17           20              20               75                  83                237
   Our work             4            4              4                1                   39                52


  Elimination of intermediate correspondence. CompCert uses forward simulation to verify each
compilation phase. This works well when each step of the source program indeed corresponds to
multiple steps in the target program. However, the correspondence between the source program and
the target program can sometimes be many-to-one instead of one-to-many. In this case, verifying

     ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:48                                                                                                                      Z. Cheng et al.


            𝜎𝑠           𝜎𝑠′            𝜎𝑠′′        𝜎𝑠′′′                                     J𝐹𝑠 K 𝜒𝑠 .(nrm)
                                                                           𝑞𝑠                                                   𝑟𝑠
                                                                                              J𝑠K 𝜒𝑠 .(nrm)
                                                                                (𝑡𝑒𝑠 , 𝑚𝑠 )                     (𝑡𝑒𝑠′ , 𝑚𝑠′ )
        𝑅                      𝑅               𝑅        𝑅         𝑅𝐵
                                                                       𝑞
                                                                                      𝑅𝐵                         𝑅𝐵                  𝑅𝐵𝑟
                                                                                              J𝑡K 𝜒𝑡 .(nrm)
                                                                                (𝑡𝑒𝑡 , 𝑚𝑡 )                     (𝑡𝑒𝑡′ , 𝑚𝑡′ )
                                                                                              J𝐹𝑡 K 𝜒𝑡 .(nrm)
            𝜎𝑡           𝜎𝑡′            𝜎𝑡′′        𝜎𝑡′′′                  𝑞𝑡                                                   𝑟𝑡
                 (a) Small-step-based proof style                               (b) Denotation-based proof style

 Fig. 16. Comparison between small-step-based approach and denotation-based approach in Cminorgen.

the forward simulation requires additional proof steps for the construction of the intermediate
state correspondence. In more complex compilation phases, no matter whether using forward or
backward simulation, additional intermediate correspondences must be constructed. For instance,
CompCertM [Song et al. 2020] requires mixed simulation to verify compilation correctness due
to its modifications of interaction semantics. In comparison, the denotation-based approach can
simplify such verification process by focusing on the overall execution of programs.


                                                                                                                         𝜒𝑠         J𝑀𝑠 K 𝜒𝑠
       𝑝1                                                      𝑝1
                                                                                                                                𝐼

                                                                                                                         ⊑



                                                                                                                                       ⊑
                 𝐺   𝑅    𝐺             𝑅          𝐺
                                                                                                                         𝜒𝑡         J𝑀𝑡 K 𝜒𝑡
   T (𝑝 1 )                                                 T (𝑝 1 )

       (a) Refinement in small-step semantics                     (b) Refinement in denotational semantics

Fig. 17. Comparison between the refinement process for small-step semantics and that for denotational
semantics. In Fig. 17a, 𝑅 and 𝐺 respectively represent rely and guarantee conditions, vertical curved arrows
denote the matching relation between the source and the target program states held throughout the execution,
and vertical shaded arrows in Fig. 17b denote the refinement between function denotations.

   We use the following examples (previously presented in §2.1) to demonstrate that handling
intermediate correspondence and nondeterminism is straightforward in our framework.
                      Source program 𝑆 : print(x); y = f(x); print(y);
                                   Transformed to 𝑇 : y = g(x); print(x); print(y);
                         Source program 𝑆 ′ : choice(x = 0, x = 1); print(0); print(x);
                         Transformed to 𝑇 ′ : print(0); choice(x = 0, x = 1); print(x);
Assume that they are type-safe programs. The following semantics is derived by definitions, where
Jprint(x)K ≜ { (𝜎, 𝜏, 𝜎) | 𝜏 = 𝜎 ( x) }, and 𝜎 ( x) means the value of a temporary variable x on state 𝜎.
                      
              J𝑆K = (𝜎, 𝜏, 𝜎 ′ ) (𝜎, nil, 𝜎 ′ ) ∈ J𝑓 K ∧ 𝜏 = OUT (𝜎 ( x)) ::OUT (𝜎 ′ ( y)) ::nil
                       
              J𝑇 K = (𝜎, 𝜏, 𝜎 ′ ) (𝜎, nil, 𝜎 ′ ) ∈ J𝑔K ∧ 𝜏 = OUT (𝜎 ( x)) ::OUT (𝜎 ′ ( y)) ::nil

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                                 5:49

                                                                                                                
         J𝑆 ′ K =       (𝜎, 𝜏, 𝜎 ′ ) 𝜏 = OUT ( 0) ::OUT (𝜎 ′ ( x)) ::nil ∧ 𝜎 ′ = 𝜎 [𝑥 ↦→ 0] ∨ 𝜎 ′ = 𝜎 [𝑥 ↦→ 1]
                                                                                                                
         J𝑇 ′ K =       (𝜎, 𝜏, 𝜎 ′ ) 𝜏 = OUT ( 0) ::OUT (𝜎 ′ ( x)) ::nil ∧ 𝜎 ′ = 𝜎 [𝑥 ↦→ 0] ∨ 𝜎 ′ = 𝜎 [𝑥 ↦→ 1]

As a result, we can straightforwardly conclude that J𝑆 ′ K = J𝑇 ′ K and if J𝑔K ⊑ J𝑓 K, then J𝑇 K ⊑ J𝑆K.

9.2    Comparison in Supporting Verified Compositional Compilation
Verified compositional compilers have been an important research topic for a long time, as evidenced
by extensive research efforts such as Beringer et al. [2014], Ramananandro et al. [2015], Stewart
et al. [2015], Song et al. [2020], Koenig and Shao [2021], and Zhang et al. [2024].
   The common style of developing compositional semantics for supporting module-level composi-
tionality is based on small-step semantics (including Beringer et al. [2014], Stewart et al. [2015], Song
et al. [2020], Koenig and Shao [2021], and Zhang et al. [2024]), in which the description of behavior
refinement must introduce extra mechanisms to capture inter-module function calls. Because C
functions in a module can both be called by other modules and call other modules, a C module’s
compilation correctness described by small-step semantics, as shown in Fig. 17a, looks like:
      • If an incoming call in the target language corresponds to a call in the source language (i.e., the
        arguments and programs states match with each other), then the first outgoing calls would
        match; and further, if the returned value and program states of these two first outgoing calls
        match with each other, then the second outgoing calls would match, etc. until the original
        incoming calls return.
      • For horizontal compositionality, the compilation correctness of internal C functions relies
        on external calls satisfying certain well-behavedness conditions (known as rely-conditions;
        e.g., external calls do not modify the private memory of callers). In turn, the execution of
        internal C functions itself guarantees some well-behavedness conditions (known as guarantee-
        conditions, e.g., they do not modify the private memory of their calling environments).
   In comparison, the definition of our behavior refinement is much different. Since the semantics
of open modules is modeled as a function from callee’s denotation to caller’s denotation, i.e., the
behavior of every external call is interpreted by semantic oracle 𝜒𝑠 (for the source module) and 𝜒𝑡
(for the target module), our compilation correctness is described as follows (shown in Fig. 17b): if the
behavior of external source functions is refined by the behavior of external target functions, then
the denotation of source module is refined by the denotation of the compiled target module. The
refinement of semantic oracles (i.e., callee’s behavior) provides rely conditions for the refinement
of caller’s behavior, and the refinement of caller’s behavior itself satisfies guarantee conditions.
   Ramananandro et al. [2015] develop a compositional semantics on top of small-step semantics
by modeling the behavior of external calls as special events. Such a special event records the
procedure name and the memory state before and after the external call. When composing the
behavior of multiple procedures, one has to interpret these special traces, in which when an
external procedure is called, instead of asking an oracle to obtain its semantics, the special event
trace of the invoked procedure is used to interpret it, and so on. For example, consider two
procedures 𝑝 and 𝑞 that form two separate modules and do not use any memory state for simplicity.
If the behavior of 𝑝 is sequentially calling 𝑞 three times, and the behavior of 𝑞 is sequentially
outputting zero for two times, then their semantics can be J𝑝K = Extcall(𝑞)::Extcall(𝑞)::Extcall(𝑞)::nil
and J𝑞K = OUT(0)::OUT(0)::nil, where Extcall(𝑞) is a special event and OUT(0) is the original event of
CompCert. After the semantic linking, the behavior of 𝑝 would be outputting zero for six times, i.e.,
OUT(0)::OUT(0)::OUT(0)::OUT(0)::OUT(0)::OUT(0)::nil. That is, they compose semantics by replacing special
events (based on the small-step semantics of CompCert), which can be viewed as progressing
incrementally over the program’s execution time. The key to proving behavior refinement for

      ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:50                                                                                                                  Z. Cheng et al.


them is to establish the correspondence between events step by step. Therefore, their main proof
structure is similar to that of small-step semantics. In comparison, our refinement proofs are built
upon RA instances and are achieved in a more compositional way.

9.3         Comparison in vertical compositionality

       𝑞1       𝑞1       𝑞 1′       𝑞 1′       𝑟 1′       𝑟 1′       𝑟1     𝑟1    𝜒1         𝜒1        J𝑀1 K 𝜒1        J𝑀1 K 𝜒1
                                                                                                   𝐼




                                                                                             ⊑




                                                                                                          ⊑
                     𝐼                                           𝐼
            𝑖   𝑞2       𝑞 2′   𝐼          𝐼          𝐼   𝑟 2′       𝑟2 𝐼              𝐼     𝜒2        J𝑀2 K 𝜒2   𝐼




                                                                                  ⊑




                                                                                                                          ⊑
                     𝐼                                           𝐼                                 𝐼




                                                                                             ⊑




                                                                                                          ⊑
       𝑞3       𝑞3       𝑞 3′       𝑞 3′       𝑟 3′       𝑟 3′       𝑟3     𝑟3    𝜒3         𝜒3        J𝑀3 K 𝜒3        J𝑀3 K 𝜒3

       (a) Vertical composition in small-step semantics                          (b) Vertical composition in our framework

Fig. 18. Comparison between vertical composition of open simulations and vertical composition of behavior
refinement in our framework, where 𝑞𝑖 and 𝑟𝑖 represents the query and the reply of a function call in module
𝑀𝑖 . The solid arrow → and dashed arrow d respectively mean internal steps and external steps.

    Consider three modules 𝑀1 , 𝑀2 , and 𝑀3 such that 𝑀1 is compiled into 𝑀2 , and 𝑀2 is further
compiled into 𝑀3 by two sequential compilation phases. The vertical compositionality is to show
if J𝑀3 K ⊑ J𝑀2 K and J𝑀2 K ⊑ J𝑀1 K, then J𝑀3 K ⊑ J𝑀1 K. We compare the vertical composition of
behavior refinement in our framework with the vertical composition of open simulations between
interactive semantics in Fig. 18, where dashed fat arrows mean direct deduction by assumptions
we know, and solid fat arrows mean that one needs to split the direct correspondence or merge
the correspondence of two compilation phases (usually quite nontrivial). As shown in Fig. 18a, the
vertical composition of open simulations typically proceeds as follows:
     • Split the initial correspondence of incoming queries. The direct correspondence between incom-
       ing calls with initial queries 𝑞 1 and 𝑞 3 is decomposed. That means, there exists an incoming
       query 𝑞 2 such that 𝑞 3 corresponds to 𝑞 2 , and 𝑞 2 corresponds to 𝑞 1 .
     • Merge correspondences of outgoing queries. After zero or more internal steps, an outgoing call
       may occur. By assumption, outgoing queries (𝑞𝑖′ for module 𝑀𝑖 ) are separately related, which
       are then merged into a direct correspondence between 𝑞 1′ and 𝑞 3′ .
     • Split the correspondence of outgoing replies. Following the outgoing calls with related queries
       𝑞 1′ and 𝑞 3′ , their corresponding replies 𝑟 1′ and 𝑟 3′ are assumed to be directly related. This
       correspondence is decomposed again for further deduction of internal steps.
     • Merge correspondences of incoming replies. After zero or more internal steps, the replies of
       initial incoming queries are separately related by assumptions. Finally, by merging relations
       of each phase, a direct correspondence between incoming replies 𝑟 1 and 𝑟 3 is established.
In comparison, the vertical composition in our framework, as shown in Fig. 18b, goes through
two steps: (i) decomposing the refinement of callee’s behaviors between module 𝑀1 and 𝑀3 ; and
(ii) merging the refinements of caller’s behaviors between 𝑀1 and 𝑀2 , and between 𝑀2 and 𝑀3 .
In other words, our framework approaches vertical composition from the perspectives of overall
behaviors of the callee and the caller functions, whereas the small-step-based approach through
the lens of the program’s interactive process. The connection between these two perspectives lies
in that the first and last solid fat arrow in Fig. 18a corresponds to the last fat arrow in Fig. 18b, and
the second and third solid fat arrow in Fig.18a corresponds to the first fat arrow in Fig. 18b.
    Though the above process of vertical composition seems intuitive, constructing interpolating
program states to transitively connect evolving source and target states across external calls of open

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                                               5:51


modules turns out to be a big challenge, as evidenced by a series of efforts [Hur et al. 2012; Neis
et al. 2015; Patterson and Ahmed 2019; Song et al. 2020; Zhang et al. 2024]. Zhang et al. [2024] make
a comprehensive conclusion of challenges and approaches to verified compositional compilers,
as shown in Fig. 19. Generally, an ideal VCC framework expects to find a refinement relation
“⊑” satisfying the following properties, where 𝐿 (with subscripts) denotes the semantics of open
modules.
         Vertical compositionality:                        𝐿3 ⊑ 𝐿2 ⇒ 𝐿2 ⊑ 𝐿1 ⇒ 𝐿3 ⊑ 𝐿1                                             (79)
         Horizontal compositionality:                      𝐿2 ⊑ 𝐿1 ⇒ 𝐿2′ ⊑ 𝐿1′ ⇒ 𝐿2 ⊕ 𝐿2′ ⊑ 𝐿1 ⊕ 𝐿1′                               (80)
         Adequacy w.r.t. semantics:                        J𝑀1 + 𝑀2 K ⊑ J𝑀1 K ⊕ J𝑀2 K                                              (81)
The final goal of VCC is to prove that, for example, if a C module a.c is compiled to assembly
code a.s going through a.c → a.i1 → a.i2 → a.s, and an environment module is separately
compiled by a different compiler (typically, an assembly library b.s without any compilation), then
Ja.s + b.sK ⊑ Ja.cK ⊕ 𝐿𝑏 , where 𝐿𝑏 is the top-level semantic specification of b.s. The proof of this
goal usually proceeds as follows.
   (i) Show individual phases correctness, i.e., Ja.sK ⊑ Ja.i2K, Ja.i2K ⊑ Ja.i1K and Ja.i1K ⊑ Ja.cK.
   (ii) Show end-to-end correctness by vertical compositionality, i.e., Ja.sK ⊑ Ja.cK and Jb.sK ⊑ 𝐿𝑏 .
   (iii) Show that Ja.sK ⊕ Jb.sK ⊑ Ja.cK ⊕ 𝐿𝑏 holds by horizontal compositionality.
   (iv) Show that Ja.s + b.sK ⊑ Ja.cK ⊕ 𝐿𝑏 holds by adequacy (81) and vertical compositionality.
In practice, each compilation phase may use different refinement relations, since intermediate
representations (or IRs) may have different ways of interaction with environment (so called language
interface). CompComp uses a unified refinement relation for different compilation phases, which is
both vertically and horizontally compositional but heavyweight and limited to interaction with
C-like calling conventions. Thus CompComp does not support adequacy w.r.t. assembly semantics.
CompCertM proposes a RUSC (Refinement Under Self-relation Context) theory featured with a
fixed collection of refinement relations {⊑1, ..., ⊑𝑛 } and a uniform refinement ⊑ R , so that individual
compilation phases can be verified with one of {⊑1, ..., ⊑𝑛 }. The RUSC theory guarantees that
given semantics of open modules 𝐿1 and 𝐿2 , if 𝐿2 ⊑𝑖 𝐿1 , then 𝐿2 ⊑ R 𝐿1 for 1 ≤ 𝑖 ≤ 𝑛, where ⊑ R is
both vertically and horizontally compositional. CompCertO introduces a naive product operator
for concatenation of refinements, i.e., 𝐿3 ⊑2 · ⊑1 𝐿1 iff there exists some 𝐿2 such that 𝐿3 ⊑2 𝐿2
and 𝐿2 ⊑1 𝐿1 . Thus, vertical composition in CompCertO is trivial. However, as pointed out by


           Ja.cK     ⊕      𝐿𝑏              Ja.cK      ⊕     𝐿𝑏                 Ja.cK     ⊕      𝐿𝑏
            ⊑C




                                                                                 ⊑1
                                             ⊑1




                                                                                                ⊑3 · ⊑2 · ⊑1


                                                                                                               ⊑4 · ⊑3 · ⊑2 · ⊑1




          Ja.i1 K                          Ja.i1 K                             Ja.i1 K
                            ⊑C




                                                            ⊑4
            ⊑C




                                                                                 ⊑2
                                             ⊑2




                                                                     ⊑R




          Ja.i2 K                          Ja.i2 K                             Ja.i2 K
            ⊑C




                                                                                 ⊑3
                                             ⊑3




           Ja.sK    ⊕      Jb.sK            Ja.sK      ⊕   Jb.sK                Ja.sK     ⊕    Jb.sK
                    ̸⊑ C




                                                                                         ⊑4
                                                     ⊑5




               Ja.s + b.sK                      Ja.s + b.sK                         Ja.s + b.sK

             (a) CompComp                        (b) CompCertM                       (c) CompCertO

Fig. 19. Refinements in existing VCC methods. Adapted from Zhang et al. [2024]. © 2024 the owner/author(s).
Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Changes: replaced ­ with ⊑.


     ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:52                                                                                                  Z. Cheng et al.


Zhang et al., horizontal composition in CompCertO would expose the intermediate semantics of the
compilation chain, in the sense that (see Fig. 19c) for horizontal composition with the compilation
correctness of a.c, namely Ja.sK ⊑3 · ⊑2 · ⊑1 Ja.cK, one has to show the environment module
satisfying the same chain of refinement concatenation, i.e., Jb.sK ⊑3 · ⊑2 · ⊑1 𝐿𝑏 . Zhang et al.
address this problem by introducing a direct refinement of open modules (denoted as ⊑ac ). They
show that the concatenation of refinements in CompCertO can be further refined to the direct
refinement between C and assembly. For example, if Ja.sK ⊑3 · ⊑2 · ⊑1 Ja.cK and ⊑3 · ⊑2 · ⊑1 ≼ ⊑ac ,
then Ja.sK ⊑ac Ja.cK. In this perspective, the concatenation of refinements for CompComp and
CompCertO can be refined to themselves, i.e., ⊑ C · ⊑ C ≼ ⊑ C and ⊑ R · ⊑ R ≼ ⊑ R , while Zhang et
al. achieve this with less restrictions by discovering a uniform and compositional Kripke relation
for describing the evolution of memory injections across external calls (shown in Def. 7.35 and
used in our Cminorgen proof). In our setting, given KIRs 𝐴1, 𝐴2 and 𝐵 1, 𝐵 2 , ⊑𝐴1 ↠𝐵2 · ⊑𝐴2 ↠𝐵2 means
⊑𝐴2 •𝐴1 ↠𝐵2 •𝐵1 (see Def. 7.7). That is, the vertical compositionality shown in Example 7.8 follows the
same approach of CompCertO and can achieve direct refinement following Zhang et al’s approach.

10     Evaluation

                       Table 5. Significant lines of our code relative to CompCert v3.11.

                   Portion                                       Specs.             Proofs
                   Front-end languages:                         old new           old    new
                   Clight.v (§3)                                489   432          14      194
                   Csharpminor.v (§3)                           345   305           0       97
                   Cminor.v                                     748   239         217      184
                   Front-end compilation phases:
                   Cshmgenproof.v                               550      453     1217      1322
                   Cminorgenproof.v                             753      679     1149      1634
                   Compositionality:
                   Semantic linking (§4, Thm. 4.1)                       261                561
                   Refinement algebras (§7)                              362                475
                   Automated proof tactics (§8.1)                       1583               1511
                   Horizontal composition. (§8.3)                        103                392
                   Vertical composition. (§8.3)                           91                146
                   Demos on toy languages:
                   Const. prop. on PCALL (Thm. 8.4)                     650               1173
                   Const. prop. on CFG (Thm. 8.6)                       196                967
                   DCE on PCALL (Thm. 8.5)                              188                519
                   DCE on CFG (Thm. 8.7)                                 86                456
                   CFG generation (Thm. 8.8)                           1031               1988
                   Total                                      2885     6659     2597     11619

   The significant lines of our Rocq development relative to CompCert v3.11 is shown in Table 5.
Our verification for the CompCert front-end is 5,539 lines in total (i.e., the front-end languages
and compilation phases portion in Table 5, including specifications and proofs), which increases
only 57 lines relative to the CompCert v3.11’s 5,482 lines. The decrease in specification size is
due to the reuse of common semantic operators (e.g., union and composition of denotations) in
different languages, as well as the simplification of program states and their invariants mentioned
in §9.1. The increase in proof size is because we add deterministic proofs for the two phases, so as to

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                                  5:53


            Table 6. Comparison with existing compositional compilers derived from CompCert.

     Portion                                  CompComp          CompCertM          CompCertO14          Our work
     Based CompCert version                      v2.1              v3.5               v3.10              v3.11
     Front-end languages                         7042              2670               1634                1451
     Front-end compilation phases               11071              4306               3625                4088
     Horizontal & Vertical compos.              15489              7656                948                 732
     Total                                      33602             14632               6207               6271

apply the forward simulation proof of atomic statements in CompCert to our backward refinement.
Furthermore, the use of multiple behavior sets in semantic definition results in repeated proofs for
atomic statements, indicating potential room for further code reduction. In the compositionality
portion, our novel semantic linking operator takes 261 lines. The equivalence between semantic and
syntactic linking (i.e., Thm. 4.1) takes 561 lines. We provide a full range of RA instances (including
all the examples in §7.1∼§7.4), taking 362 lines for definitions and 475 lines for axiom proofs. Our
new proof tactic gamma_simpl and solvefix take 1,583 lines for definitions and 1,511 lines for proofs.
Finally, our demos on the verification of a typical CFG generation and optimizations (i.e., the demo
portion in Table 7) on toy languages take totally 2,151 lines for definitions and 5,103 lines for proofs.
   We compare our development with typical compositional compilers in Table 6. For the imple-
mentation of the CompCert front-end (i.e., the rows of front-end languages and compilation phases
in Table 6), our approach does not significantly increase the code size, and yet significantly reduces
the required code for supporting horizontal and vertical compositionality. As is well-known, the
structured simulation approach employed by CompComp [Stewart et al. 2015] extensively increases
proof effort. CompCertM [Song et al. 2020] supports compositional verification based on the RUSC
theory, whose developments totally take about 7.6K code lines. CompCertO [Koenig and Shao 2021]
requires 948 lines for the horizontal and vertical composition of two simulations. Our compositional
verification is as lightweight as CompCertO, but differently, our entire framework is directly based
on backward refinement to provide better support for nondeterminism.

                      Table 7. Increased significant lines of code for support new features.

    Feature                Portion                         Before support        After support        Increased by
                           Const. Prop. on PCALL                1596                 1823              227 (14.2%)
                           Const. Prop. on CFG                  970                  1163              193 (19.9%)
    Procedure calls        DCE on PCALL                         606                   707              101 (16.7%)
                           DCE on CFG                           450                   542               92 (20.4%)
                           CFG generation                       2607                 3019              412 (15.8%)
                           Front-end languages                  1250                 1451              201 (16.1%)
    Uncond. branch
                           Front-end phases                     3623                 4088              465 (12.8%)

  We demonstrate the lightweight extensibility of our framework by presenting the incremental
code required to support two new features that were not accommodated in our earlier development.
The first one is the support of procedure calls in toy languages. Adding the support of procedure
calls to the WHILE and earlier CFG languages totally requires an additional 1,025 lines of code
for definitions and proofs of the constant propagation and dead code elimination optimizations
14 Our statistics focuses on the latest version of CompCertO extended by Zhang et al. for supporting direct refinement.



     ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:54                                                                                                  Z. Cheng et al.


(corresponding to the first five portions in Table 7). The second feature is unconditional branching
introduced in §4.4. We now support this feature in the CompCert front-end (i.e., the last two
portions in Table 7), with an increase of 201 lines for the CompCert front-end languages (i.e., Clight,
Csharpminor and Cminor), and 465 additional lines for proofs of the Cshmgen and Cminorgen.

11     Discussion
   Denotational semantics versus small-step semantics. There is no definitive consensus on whether
denotational semantics or small-step operational semantics should serve as the gold standard for
semantic characterization, as both are employed in different contexts. Denotational semantics
inherently supports compositionality and is often most convenient when expressed via least fixed
points (e.g., in the semantics of open modules in §4). By contrast, small-step semantics is frequently
preferred for low-level languages such as assembly. As shown in §8.2 and §8.3, our results are stated
in terms of denotations and the algebraic notion of behavior refinement presented in §7.4. We further
proved the soundness of the algebraic behavior refinement with respect to CompCert-style behavior
refinement in Thm. 7.32 and Thm. 7.33. Consequently, relating our denotation-based refinement
results back to the original CompCert presentation reduces to establishing an equivalence theorem
between our denotational semantics and CompCert’s standard small-step semantics for Clight. To
illustrate this connection, we provide a supplementary mechanized proof of equivalence between
denotational and small-step semantics for extended WHILE and CFG languages with I/O events
considered. The proof relies on structural induction (on the syntax of the program) or rule induction
(on the state transitions of small-step semantics). However, this proof does not yet cover three
features of Clight—namely, procedure calls, unconditional branching (e.g., goto), and structured
control flow (e.g., break and continue). Extending the equivalence proof to these remaining
constructs is orthogonal to the refinement results developed in this article and is left to future work.
   Denotational semantics versus big-step semantics. Big-step operational semantics, widely used in
compiler correctness and type-safety proofs, describes how a program evaluates in terms of compu-
tations that directly map initial states to final results. For example, the CakeML compiler [Kumar
et al. 2014] employs a functional big-step semantics, where divergence is treated using a step-
indexed construction rather than a coinductive relation. Furthermore, coinductive approaches to
big-step semantics have been investigated, such as the work of Ancona et al. [2020], which extends
standard big-step semantics with inference systems and corules to capture infinite computations.
More recently, Charguéraud et al. [2023] proposed omni-big-step semantics, which defines a single
execution step from an initial state to a set of potential outcomes, demonstrating its applicability
to compiler correctness, type-safety for lambda calculi, and reasoning about partial correctness.
Nevertheless, despite these developments, big-step semantics and denotational semantics remain
fundamentally distinct, particularly in their treatment of loops and recursive constructs. Big-step
semantics captures the execution of such constructs through operational rules that describe how
results are produced, while denotational semantics provides a mathematical interpretation based
on abstract structures such as least or greatest fixed points. Furthermore, divergence in big-step
semantics is typically modeled using a coinductive relation, while denotational semantics naturally
captures nontermination by the use of least or greatest fixed points in suitable semantic domains.
   Semantics in UTP. Unifying theories of programming (UTP) [He and Hoare 1998; Woodcock and
Cavalcanti 2004] serves as a framework for unifying different programming theories and models,
primarily based on denotational semantics. To be brief, the semantics of recursion in UTP is handled
using Tarski’s fixed-point theory, leveraging the mathematical framework of complete lattices. In
this context, divergence is often represented as the bottom element (⊥) of the lattice, signifying a
program that fails to produce a meaningful or valid output. However, using the semantic framework

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                            5:55


of UTP to uniformly characterize the various program behaviors required for compiler verification
faces a key challenge: it is difficult to establish an appropriate ordering on a complete lattice. If
we consider the simple subset relation on sets, neither the least fixed point nor the greatest fixed
point can correctly capture divergence with event traces. For instance, the silent divergence of
program “while true do skip” should be characterized using the greatest fixed point, and its reactive
(or nonsilent) divergence should be captured using the least fixed point. Conversely, the silent
divergence of program “while true do print(0)” should be described by the least fixed point, while
its reactive divergence should rely on the greatest fixed point. This demonstrates that a conventional
ordering cannot meet the requirements. Resolving this issue might necessitate constructing a highly
counterintuitive ordering. In our framework, all definitions remain intuitive and straightforward,
since we describe these behaviors by different behavior sets with relevant semantic operators.
   Refinement calculus and Event-B. The refinement calculus [Back and von Wright 1998; Morgan
1988; Morris 1987] is a formal framework that focuses on transforming high-level specifications
into concrete implementations (e.g., specific data structures or algorithms), through a series of
mathematically verified refinement steps. Specifically, specifications in the refinement calculus
are written as abstract programs, usually in the form of specification statements. Each refinement
step would transform a certain component of the abstract program to a more concrete one by
applying one of the refinement laws (i.e., inference rules for valid refinements). Event-B [Abrial
2010] closely mirrors the conceptual framework of refinement calculus and extends related concepts
to state-based systems and events. Our framework shares a common trait with these pioneering
efforts: both of us can derive the refinement of composite structures through the refinement of their
substructures. In comparison, the refinement algebras in our framework are used to algebraically
and uniformly build behavior refinement between the source and target program behaviors and to
enable mechanized verification, while refinement calculus and Event-B focus on stepwise refinement
of statements so as to bridge the gap between specifications and their implementations.
   More compilation optimizations. Beyond presented optimizations, our denotation-based frame-
work can be useful for a wide range of other optimizations, including tail recursion optimizations,
inlining optimizations, context-sensitive optimization, and specification-based optimizations.
   Specifically, tail recursion optimizations convert recursive procedure calls into iterative constructs
(e.g., a while loop). Since the semantics of both recursive procedures and loops are defined by taking
fixed points, proving semantic equivalence before and after the optimization is straightforward. For
instance, the procedure “src() { if 𝑏 then 𝑐; src() else skip }” can be optimized to “tgt() { while
𝑏 do 𝑐 }” for given Boolean expression 𝑏 and statement 𝑐 in which no more recursive calls appear.
Their denotational semantics15 , respectively shown in Formulae (82) and (83), are intuitively the
two forms of loop’s semantics, as illustrated by Example 2.4. We believe that more general cases
can be proved similarly.
                                                                                            
      𝜇 𝜒 .JsrcK 𝜒 .(nrm) = 𝜇 𝜒 . test(J𝑏K.( ffs)) ◦ 1 ∪ test(J𝑏K.( tts)) ◦ J𝑐K 𝜒 .(nrm) ◦ 𝜒          (82)
                                                                                   ∗
      𝜇 𝜒 .JtgtK 𝜒 .(nrm) = Jwhile b do cK.(nrm) = test(J𝑏K.( tts)) ◦ J𝑐K 𝜒 .(nrm) ◦ test(J𝑏K.( ffs)) (83)
   Inlining optimizations within a module replace procedure calls with the body of the callee
procedures at the call sites. Before inlining, the denotations of all procedures in the module are
first combined and then their semantics is derived by taking fixed points. After inlining, the
denotations of callee procedures somehow are directly substituted into the call sites within the
caller procedures, and then the semantics of caller procedures is derived by taking fixed points. In
15We here consider a module with the single procedure foo for presentation purpose, and omit details about procedure

names, arguments, and local variables in the semantic definition since they will not affect the final result.


     ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:56                                                                                                  Z. Cheng et al.


       Before optimization                                   After optimization
       callee(bool b) { if b then 𝑐 1 else 𝑐 2 }             callee_tt() { 𝑐 1 }    callee_ff() { 𝑐 2 }
       caller_src() { callee(true); callee(false) }          caller_tgt() { callee_tt(); callee_ff() }

                         Fig. 20. A simple example of context-sensitive optimizations.


a procedural perspective, proving the correctness of inlining optimizations is conceptually similar
to demonstrating the equivalence between semantic linking and syntactic linking.
   Context-sensitive optimizations mean that realistic compilers can make use of information from
context-sensitive analyses, as demonstrated by Lattner et al. [2007], Li et al. [2013], and Poesia and
Pereira [2020], so that a callee procedure can be optimized with the information that all calls to the
callee satisfy certain properties. Typically, compilers can create multiple versions of a procedure
optimized for different contexts (i.e., procedure cloning). Consider the example in Fig. 20, where
callee is specialized according to the caller’s context. Verifying such an optimization in our frame-
work can be reduced to first show the refinement of callee procedures under assumed conditions
and then to show the refinement between caller procedures that guarantee the assumptions.
   Specification-based optimizations leverage the specification of invoked procedures to optimize
the caller procedure. For example, consider a procedure: foo() { 𝑐 1 ; x = callee(x); 𝑐 2 }. If the
specification of callee guarantees that it does not modify the variable x and always returns a
value identical to its input, the assignment x = callee(x) can then be safely eliminated. Moreover,
the information from the callee’s specification can also enhance optimizations such as constant
propagation and dead code elimination (DCE). In our framework, the refinement processes for the
caller and callee procedures are explicitly decoupled. This separation simplifies the implementation
of specification-based optimizations, as it isolates the properties of the callee while preserving the
modularity and correctness of the overall refinement.
   In summary, these optimizations, particularly those involving procedure calls, are not as intu-
itively understood using small-step semantics. In contrast, they are much more straightforward
when analyzed through the lens of denotational semantics. The latter provides a high-level, mathe-
matical representation of program behavior, making it easier to reason about the transformations
and their correctness, especially for higher-level constructs like procedure calls.
   Liveness preservation. Safety properties guarantee that “nothing bad will happen” during program
execution, such as preventing invalid states. Liveness properties, on the other hand, ensure that
“something good eventually happens”, asserting that every execution will lead to a desirable outcome
within a program. Although our refinement method primarily focuses on safety, it is important to
clarify that this does not inherently preclude the verification of liveness preservation. In fact, our
approach is capable of reasoning about liveness preservation if augmented with additional proof
strategies or invariants tailored to liveness verification. For instance, Barthe et al. [2020] develop a
Constant-Time Secure (CTS) preserving compiler based on CompCert. The CTS property can be
summarized as follows: given a safety program 𝑃, if 𝑃 is executed from any two “indistinguishable”
initial states, then both of the two executions will produce the same leakage information (both
executions terminate with the same leakage information, or they both diverge with the same
leakage information), where leakage information includes the truth values of conditions, memory
access addresses, and the addresses of invoked functions. Their approach relies on small-step
semantics and CT-simulation [Barthe et al. 2018b]—a three-dimensional extension of CompCert’s
flat simulation, forming a “cube diagram”. We can also address the CTS preservation problem by
enriching the event trace of each behavior set in our semantics with leakage information, defining
the CTS property using denotational semantics, and showing the CTS preservation compositionally.

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                            5:57


   Our limitation. Currently, our framework supports semantic linking for heterogeneous languages,
provided they share the same memory model or employ memory models that can be mutually
transformed. Moreover, we have not yet addressed concurrent settings or higher-order features (i.e.,
features of higher-order languages). We are particularly interested in exploring how our approach
can be extended to these domains. Furthermore, unlike interaction trees or small-step semantics,
our semantics is not directly executable. Nevertheless, we have established formal equivalence with
small-step operational semantics for simple imperative languages as mentioned above. We believe
that extending the equivalence proof to realistic languages presents no fundamental difficulty.

12   Related Work
   Denotational semantics. In traditional denotational semantics, two fixed-point theorems are
ubiquitous: the Kleene fixed point theorem (for Scott-continuous operators on CPOs) and the
Knaster-Tarski fixed point theorem (for monotone operators on complete lattices). Researchers
have long tended to commit to one of these frameworks when handling recursion, e.g., Kleene’s
theorem in domain theory [Scott 1970; Scott and Strachey 1971], and Knaster-Tarski’s theorem
in lattice-based frameworks such as UTP [He and Hoare 1998; Woodcock and Cavalcanti 2004].
This commitment entails adopting a single global order over the semantic domain, endowed
with (global) properties such as continuity or completeness. However, a tension has long been
observed: “trivial” domains that easily satisfy these properties often cannot express important
program features, whereas richer domains make the required global completeness or continuity
difficult to establish. This tension has motivated increasingly elaborate fixed-point theories. The
phenomenon is particularly evident in the evolution of CSP’s denotational semantics [Roscoe 2010]
(following Hoare and subsequent work): from the trace model, to the (stable) failures model, to the
failures-divergences model [Brookes et al. 1984], and eventually to more expressive extensions (e.g.,
incorporating infinite traces [Roscoe 2004]). Rather than binding ourselves to a single fixed-point
method or a uniform global order, we advocate a staged (componentwise) approach to applying
fixed-point theorems: equip each semantic component with its natural (simple) order, and apply
the most suitable fixed-point principle per component. This staged and componentwise strategy
sidesteps contrived global structures while preserving clarity, proof simplicity, and applicability.
   More specifically, the foundational work of Scott [1970] and Scott and Strachey [1971] in domain
theory provides a mathematical framework for the denotational semantics of deterministic programs.
Following their work, later efforts [Apt and Plotkin 1981; Back 1983; Broy et al. 1978; Park 1979]
attempt to extend the framework for supporting nondeterministic programs, especially programs
that can produce an infinite number of different results and yet be certain to terminate. Among them,
Back [1983] describes a path semantics for nondeterministic assignment statements indicated by
semantic models described for CSP programs [Francez et al. 1979] and data flow programs [Kosinki
1978] based on paths. The relational style of defining denotations in this article is inspired from the
relational semantics of Park [1979], which originally aims to address unbounded nondeterminism
in the fair scheduling problem of concurrency. See our comparison with this work in §2.2 and §3.1.
   Besides, Kahn [1974] describes a class of asynchronous deterministic parallel programs, now
known as Kahn networks. These networks are represented as systems of recursive equations based
on stream transformations. Each process in the network consumes input streams and produces
output streams. Kahn also provides a denotational semantics for these networks by leveraging
complete partial orders (CPOs), which focuses on stream-based communication between parallel
processes. Paulin-Mohring [2009] presents a formalization of denotational semantics for Kahn
networks in the Rocq proof assistant. The formalization includes definitions of processes, channels,
and their compositions. In addition, denotational semantics has been employed to construct semantic
models for probabilistic programming languages, as illustrated in works such as Barthe et al. [2018a],

     ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:58                                                                                                  Z. Cheng et al.


Wang et al. [2019a], and [Vákár et al. 2019]. Among these works, Barthe et al. [2018a] adopt the
traditional semantics of probabilistic distributions to develop an assertion-based program logic for
reasoning about probabilistic programs. Wang et al. [2019a] tackle the interplay of nondeterminism
and probability through domain theory. Vákár et al. [2019] support higher-order functions by
employing quasi-Borel spaces (QBS) and omega-complete quasi-Borel spaces (𝜔QBS).
   Compiler verification with interaction trees. The Vellvm project [Xia et al. 2020; Zakowski et al.
2021] uses Interaction Trees (ITrees) [Xia et al. 2020] to model the semantics of LLVM IRs and to
verify compiler transformations. Specifically, interaction trees provide a denotational approach for
modeling recursive, effectful computations that can interact with their environment. Much different
from the textbook denotational semantics and the relational denotational semantics used in this
article, interaction trees are executable via code extraction, making them suitable for debugging,
testing, and implementing software artifacts. To this end, the ITree-based denotational semantics is
also used by Song et al. [2023] for building executable module semantics in Conditional Contextual
Refinement (CCR), and Frumin et al. [2024] further scales the semantics for higher-order languages.
   In comparison, a principal advantage of our approach is the smooth proofs for horizontal
compositionality and for semantic adequacy (i.e., the equivalence between syntactic and semantic
linking for open modules shown in Thm. 4.1). The key observation is that the adequacy proofs
reduce directly to the Bekić theorem [Bekić 1984]. ITree-based frameworks model function calls and
semantic composition via event handlers. To the best of our knowledge, within these frameworks
the equivalence between syntactic and semantic linking for open modules has not been fully
established, nor is it clear how such an equivalence could be derived from the Bekić theorem.
   Moreover, ITrees use Tau to hide internal computation steps (i.e., steps with no observable events).
Establishing refinement (e.g., strong bisimulation) between two ITrees may require additional treat-
ment of Tau steps—that is, any finite number of Tau can be removed when determining equivalence.
In comparison, our refinement directly relates the target event trace with strictly equal (or prefixing
when the source aborts) source event trace. This is possible because our semantics distinguishes
finite and infinite event traces via the behavior sets fin_dvg and inf_dvg straightforwardly.
    Advanced simulation techniques beyond CompCert. In CompCert’s backward simulation, the
central proof obligation is that: under a given relation 𝑅, for any pair of related states (𝜎𝑡 , 𝜎𝑠 ) ∈ 𝑅, if
the target can take a step 𝜎𝑡 → 𝜎𝑡′ , then the source can simulate this behavior by taking zero or more
steps 𝜎𝑠 →∗ 𝜎𝑠′ so that (𝜎𝑡′, 𝜎𝑠′ ) ∈ 𝑅 and the same observable events are emitted. A broad class of
more advanced techniques relaxes this obligation by allowing the post-step states to be related by a
weaker relation 𝑅 ′ , i.e., (𝜎𝑡′, 𝜎𝑠′ ) ∈ 𝑅 ′ with 𝑅 ′ not necessarily equal to 𝑅 (e.g., [Pous 2016]). To ensure
soundness, such approaches tend to impose additional recovery simulation rules (for example, that
𝑅 be re-established at designated synchronization points). As one of the state-of-the-art efforts,
FreeSim [Cho et al. 2023] introduces progress indices into the matching relation and provides new
simulation rules for flexible simulation proofs. While the emphasis of FreeSim is put on extending
stuttering simulations [Namjoshi 1997] to ensure soundness with only asynchronous progress
(i.e., a simulation proof step that allows one side of the simulation to stay in place (stutter) while
the other side to step forward) required, using progress indices also allows intermediate proof
steps to proceed under weaker relations while ensuring that stronger invariants are recovered
when required. Consequently, in small-step semantics based settings, FreeSim can reduce the
CompCert-style burden of preserving a single global matching relation by every step, thereby
easing proofs involving intermediate correspondence. This is illustrated in Fig. 21: transforming
“print(x); y = f(x); print(y);” into “y = f(x); print(x); print(y);” is justified when f(x) is a pure,
deterministic computation that produces no observable behavior. For the example in Fig. 4, the
flexibility of Freesim can make the proofs that the fragment code g simulates f and the proofs that

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                                        5:59


           print(x)         y = f(x)          print(y)                print(x)         y = f(x)          print(y)
     𝜎𝑠               𝜎𝑠′              𝜎𝑠′′              𝜎𝑠′′′   𝜎𝑠              𝜎𝑠′              𝜎𝑠′′              𝜎𝑠′′′

    𝑅           𝑅                𝑅                           𝑅   𝑅         𝑅′               𝑅′       𝑅                  𝑅

     𝜎𝑡               𝜎𝑡′              𝜎𝑡′′              𝜎𝑡′′′   𝜎𝑡              𝜎𝑡′              𝜎𝑡′′              𝜎𝑡′′′
           y = f(x)         print(x)          print(y)                y = f(x)         print(x)          print(y)

  (a) An instance of CompCert backward simulation (b) An instance of advanced simulation diagrams

          Fig. 21. Comparison between CompCert’s simulation with advanced simulation techniques.


the larger program 𝑇 simulates 𝑆 simpler and easier to carry out respectively. However, it remains
unclear how to modularly reuse the former proofs for the latter (w.r.t. proofs based on small-step
semantics). In comparison, our denotation-based approach addressed such issues illustrated in §9.1.
   Regarding nondeterminism correspondence, FreeSim comfortably handles scenarios where nonde-
terministic choices occur entirely before or entirely after an event-synchronization step. However,
when demonic choices occur on opposite sides of such a step (i.e., step-event in FreeSim) and
influence subsequent observable events, a small-step semantics based proof in FreeSim generally
fails: the later demonic step may not match a value chosen earlier on the other side. Still consider:
                 Source program :             [𝜎𝑠 ] choice(x = 0, x = 1); print(0); [𝜎𝑠′ ] print(x);
                 Transformed to :             [𝜎𝑡 ] print(0); [𝜎𝑡′ ] choice(x = 0, x = 1); print(x);
At the first event synchronization on print(0), the proof obligation becomes to relate the post-event
states (𝜎𝑠′, 𝜎𝑡′ ) under some derived relation 𝑅 ′ . From there, the target would perform its internal
demonic step choice, and the proof must succeed for all outcomes 𝑥𝑡 ∈ {0, 1}. If 𝑥𝑡 ≠ 𝑥𝑠 (where
𝑥𝑠 was chosen earlier by the source), the subsequent visible actions print(x) do not match, so the
required second event synchronization cannot be discharged and the simulation gets stuck.
   Early research [Abadi and Lamport 1991; Lynch and Vaandrager 1995] proposes the use of
prophecy variables to enhance small-step semantics based simulations for handling such general
nondeterminism correspondence. They leverage prophecy variables to anticipate and reconcile
nondeterministic choices between the source and target programs, ensuring that simulation aligns
with their observable event traces. However, these approaches are often challenging to implement
in practice [Lamport and Merz 2022]. As far as we know, they have not yet been formalized and used
for realistic compiler verification. CompCert achieves a balance between theoretical complexity
and practical applicability by eliminating nondeterminism from the outset.
   Besides, both relational denotational semantics and big-step operational semantics exhibit equal
advantages when dealing with such a specific problem of nondeterminism; see §9.1 for our solution.
   Choice Trees (CTrees). CTrees [Chappe et al. 2025, 2023] extend ITrees with two forms of internal
choice to facilitate the reasoning about nondeterminism: stepping choice, which materializes as
Tau-steps in the induced labeled transition system (LTS), and delayed choice, which is structural and
does not create LTS transitions. This extension enables CTrees to address the above problem: when
a choice is modeled as delayed, CTrees’ equational laws (congruent for composition) allow that
choice to commute with the next observable event, aligning programs where one makes the choice
before the event and the other after. In comparison, we model the whole event traces of a program
in behavior sets (simpler than a tree structure), and hence the correspondence is immediate.
   Compositional compiler verification. Many existing works have extended the small-step semantics
of CompCert for supporting cross-module semantic linking. Among them, Ramananandro et al.

     ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:60                                                                                                  Z. Cheng et al.


[2015] model the behavior of an external call as a special event recording the function name and
memory states before and after the external call so as to signal state transitions made by the
environment and then “big-step” the small-step semantics to obtain the compositional semantics
for semantic linking. Beringer et al. [2014] propose a novel interaction model, called core semantics
(also known as interaction semantics), that describes the communication between a local thread
with its environment, which is widely used by later efforts such as CompComp [Stewart et al.
2015], CompCertM [Song et al. 2020] and CASCompCert [Jiang et al. 2019]. Specifically, with the
interaction semantics, CompComp proves a general correctness result for semantic linking where
programs can be written with heterogeneous languages such as C and assembly code. However, to
achieve horizontal (module-level) and vertical compositionality, it introduces complicated structured
simulations which require a large number of changes to the original proofs of CompCert.
   Compared to CompComp, SepCompCert [Kang et al. 2016] greatly reduces the complexity of
proofs by limiting all source modules to be compiled by the same compiler. Furthermore, both Com-
pCertM [Song et al. 2020] and CompCertO [Koenig and Shao 2021] have developed a lightweight
verification technique for supporting semantic linking of heterogeneous languages. CompCertM
proposes a RUSC (Refinement Under Self-related Contexts) theory for composing two open simula-
tions together, while CompCertO characterizes compiled program components directly in terms of
their interaction with each other and achieves compositionality through a careful and compositional
treatment of calling conventions. Recently, Zhang et al. [2024] have proposed a fully composable
and adequate approach to verified compilation with direct refinements between open modules based
on CompCertO. We believe that their approach to handling calling conventions of heterogeneous
languages can be applied to our framework. Patterson and Ahmed [2019] make a comprehensive
survey of compositional compiler correctness. They take existing compiler correctness theorems as
a spectrum which ranges from CompCert, SepCompCert, CompCertX [Gu et al. 2015; Wang et al.
2019b], and CompComp up to compilers verified with multi-language techniques.
  Other verified compiler or compilation passes. CertiCoq [Paraskevopoulou et al. 2021] and CakeML
[Kumar et al. 2014] are typical verified functional language compilers based on operational se-
mantics. We believe that our method can also be extended to support typed lambda calculus and
the verification of functional language compilation. Besides, the CompCert back-end is mostly
implemented in control flow graphs. If procedure calls are not considered, there is no big difference
between denotational semantics and small-step semantics in the back-end. However, we still believe
that the proposed semantics using semantic oracle to interpret the behavior of callee functions is
beneficial for verifying these back-end passes and then achieving module-level compositionality.
We are interested in these topics and leave them as future work.
  Discussion on program verification. The small-step semantics of Clight is also used in static
analyzers like Verasco [Jourdan 2016] and program logics like VST-Floyd [Cao et al. 2018]. The
soundness proof of VST is connected to the proof of CompCert, ensuring that the correctness
properties proved for Clight programs are preserved through compilation down to the target
machine code. We believe that for sequential programs, rebuilding Hoare-like logics on denotational
semantics should be simple. For concurrent programs, more trace-related elements need to be
incorporated into the semantics so as to provide semantic basis for related program logics.

13 Conclusion
We have proposed a denotation-based framework for compositional compiler verification. In this
framework, we have scaled relational denotational semantics to realistic settings that capture
diverse program features, and we have defined a novel semantic linking operator based on fixed-
point theorems, reducing its equivalence with syntactic linking to concise fixed-point properties.

ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                            5:61


In particular, we propose the notion of refinement algebras to define the refinement relations of
interest and to facilitate the automation of the required proofs, and support verified compositional
compilation in a language-independent way. We have applied this denotational semantics to the
front-end languages of CompCert, reproved the correctness of compilation from Clight to Cminor,
and demonstrated that the denotation-based approach is suitable for verifying typical optimizations.

Acknowledgments
We are grateful to Andrew W. Appel, Naijun Zhan, Zhenjiang Hu, Zhong Shao, Yuxi Fu, Yuxin
Deng, Yuting Wang, and Huan Long for insightful suggestions and helpful discussions. We also
thank Ximeng Li, Shuling Wang, and Yiyuan Cao for careful feedback. We thank the editors and
the anonymous TOPLAS referees for their thoughtful and constructive comments. This work was
supported by the National Natural Science Foundation of China (Grant No. 62472274, 61902240).




     ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:62                                                                                                           Z. Cheng et al.


References
Martín Abadi and Leslie Lamport. 1991. The Existence of Refinement Mappings. Theor. Comput. Sci. 82, 2 (1991), 253–284.
   doi:10.1016/0304-3975(91)90224-P
Jean-Raymond Abrial. 2010. Modeling in Event-B - System and Software Engineering. Cambridge University Press. doi:10.
   1017/CBO9781139195881
Davide Ancona, Francesco Dagnino, Jurriaan Rot, and Elena Zucca. 2020. A big step from finite to infinite computations.
   Sci. Comput. Program. 197 (2020), 102492. doi:10.1016/J.SCICO.2020.102492
Krzysztof R Apt and Gordon D Plotkin. 1981. A Cook’s tour of countable nondeterminism. In International Colloquium on
   Automata, Languages, and Programming. Springer, 479–494.
Ralph-Johan Back. 1983. A Continuous Semantics for Unbounded Nondeterminism. Theor. Comput. Sci. 23 (1983), 187–210.
   doi:10.1016/0304-3975(83)90055-5
Ralph-Johan Back and Joakim von Wright. 1998. Refinement Calculus - A Systematic Introduction. Springer. doi:10.1007/978-
   1-4612-1674-2
Gilles Barthe, Sandrine Blazy, Benjamin Grégoire, Rémi Hutin, Vincent Laporte, David Pichardie, and Alix Trieu. 2020.
   Formal verification of a constant-time preserving C compiler. Proc. ACM Program. Lang. 4, POPL (2020), 7:1–7:30.
   doi:10.1145/3371075
Gilles Barthe, Thomas Espitau, Marco Gaboardi, Benjamin Grégoire, Justin Hsu, and Pierre-Yves Strub. 2018a. An Assertion-
   Based Program Logic for Probabilistic Programs. In Programming Languages and Systems - 27th European Symposium on
   Programming, ESOP 2018, Held as Part of the European Joint Conferences on Theory and Practice of Software, ETAPS 2018,
   Thessaloniki, Greece, April 14-20, 2018, Proceedings (Lecture Notes in Computer Science, Vol. 10801), Amal Ahmed (Ed.).
   Springer, 117–144. doi:10.1007/978-3-319-89884-1_5
Gilles Barthe, Benjamin Grégoire, and Vincent Laporte. 2018b. Secure Compilation of Side-Channel Countermeasures: The
   Case of Cryptographic "Constant-Time". In 31st IEEE Computer Security Foundations Symposium, CSF 2018, Oxford, United
   Kingdom, July 9-12, 2018. IEEE Computer Society, 328–343. doi:10.1109/CSF.2018.00031
Hans Bekić. 1984. Definable Operation in General Algebras, and the Theory of Automata and Flowcharts. In Programming
   Languages and Their Definition - Hans Bekic (1936-1982) (Lecture Notes in Computer Science, Vol. 177), Cliff B. Jones (Ed.).
   Springer, 30–55. doi:10.1007/BFB0048939
Lennart Beringer, Gordon Stewart, Robert Dockins, and Andrew W. Appel. 2014. Verified Compilation for Shared-Memory
   C. In Programming Languages and Systems - 23rd European Symposium on Programming, ESOP 2014, Held as Part of the
   European Joint Conferences on Theory and Practice of Software, ETAPS 2014, Grenoble, France, April 5-13, 2014, Proceedings
   (Lecture Notes in Computer Science, Vol. 8410), Zhong Shao (Ed.). Springer, 107–127. doi:10.1007/978-3-642-54833-8_7
Sandrine Blazy, Zaynah Dargaye, and Xavier Leroy. 2006. Formal Verification of a C Compiler Front-End. In FM 2006: Formal
   Methods, 14th International Symposium on Formal Methods, Hamilton, Canada, August 21-27, 2006, Proceedings (Lecture
   Notes in Computer Science, Vol. 4085), Jayadev Misra, Tobias Nipkow, and Emil Sekerinski (Eds.). Springer, 460–475.
   doi:10.1007/11813040_31
Stephen D. Brookes, C. A. R. Hoare, and A. W. Roscoe. 1984. A Theory of Communicating Sequential Processes. J. ACM 31,
   3 (1984), 560–599. doi:10.1145/828.833
Manfred Broy, Rupert Gnatz, and Martin Wirsing. 1978. Semantics of Nondeterministic and Noncontinuous Constructs. In
   Program Construction, International Summer School, July 26 - August 6, 1978, Marktoberdorf, Germany (Lecture Notes in
   Computer Science, Vol. 69), Friedrich L. Bauer and Manfred Broy (Eds.). Springer, 553–592. doi:10.1007/BFb0014683
Janusz A. Brzozowski. 1964. Derivatives of Regular Expressions. J. ACM 11, 4 (1964), 481–494. doi:10.1145/321239.321249
Qinxiang Cao, Lennart Beringer, Samuel Gruetter, Josiah Dodds, and Andrew W. Appel. 2018. VST-Floyd: A Separation
   Logic Tool to Verify Correctness of C Programs. J. Autom. Reason. 61, 1-4 (2018), 367–422. doi:10.1007/S10817-018-9457-5
Qinxiang Cao, Xiwei Wu, and Yalun Liang. 2023. A Coq Library of Sets for Teaching Denotational Semantics. In Proceedings
   12th International Workshop on Theorem proving components for Educational software, ThEdu@CADE 2023, Rome, Italy, 5th
   July 2023 (EPTCS, Vol. 400), Julien Narboux, Walther Neuper, and Pedro Quaresma (Eds.). 79–95. doi:10.4204/EPTCS.400.6
Nicolas Chappe, Paul He, Ludovic Henrio, Eleftherios Ioannidis, Yannick Zakowski, and Steve Zdancewic. 2025. Choice
   trees: Representing and reasoning about nondeterministic, recursive, and impure programs in Rocq. J. Funct. Program.
   35 (2025). doi:10.1017/S0956796825100105
Nicolas Chappe, Paul He, Ludovic Henrio, Yannick Zakowski, and Steve Zdancewic. 2023. Choice Trees: Representing
   Nondeterministic, Recursive, and Impure Programs in Coq. Proc. ACM Program. Lang. 7, POPL (2023), 1770–1800.
   doi:10.1145/3571254
Arthur Charguéraud, Adam Chlipala, Andres Erbsen, and Samuel Gruetter. 2023. Omnisemantics: Smooth Handling of
   Nondeterminism. ACM Trans. Program. Lang. Syst. 45, 1 (2023), 5:1–5:43. doi:10.1145/3579834
Minki Cho, Youngju Song, Dongjae Lee, Lennard Gäher, and Derek Dreyer. 2023. Stuttering for Free. Proc. ACM Program.
   Lang. 7, OOPSLA2 (2023), 1677–1704. doi:10.1145/3622857



ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                                       5:63


Nissim Francez, C. A. R. Hoare, Daniel J. Lehmann, and Willem P. de Roever. 1979. Semantics of Nondeterminism,
    Concurrency, and Communication. J. Comput. Syst. Sci. 19, 3 (1979), 290–308. doi:10.1016/0022-0000(79)90006-0
Dan Frumin, Amin Timany, and Lars Birkedal. 2024. Modular Denotational Semantics for Effects with Guarded Interaction
    Trees. Proc. ACM Program. Lang. 8, POPL (2024), 332–361. doi:10.1145/3632854
Ronghui Gu, Jérémie Koenig, Tahina Ramananandro, Zhong Shao, Xiongnan (Newman) Wu, Shu-Chun Weng, Haozhong
    Zhang, and Yu Guo. 2015. Deep Specifications and Certified Abstraction Layers. In Proceedings of the 42nd Annual ACM
    SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2015, Mumbai, India, January 15-17, 2015,
    Sriram K. Rajamani and David Walker (Eds.). ACM, 595–608. doi:10.1145/2676726.2676975
Jifeng He and C. A. R. Hoare. 1998. Unifying theories of programming. In Participants Copies for Relational Methods in Logic,
    Algebra and Computer Science, 4th International Seminar RelMiCS, Warsaw, Poland, September 14-20, 1998, Ewa Orlowska
    and Andrzej Szalas (Eds.). 97–99.
Chung-Kil Hur, Georg Neis, Derek Dreyer, and Viktor Vafeiadis. 2012. The transitive composability of relation transition
    systems. MPI-SWS, Tech. Rep. MPI-SWS-2012-002 (2012).
Hanru Jiang, Hongjin Liang, Siyang Xiao, Junpeng Zha, and Xinyu Feng. 2019. Towards certified separate compilation
    for concurrent programs. In Proceedings of the 40th ACM SIGPLAN Conference on Programming Language Design and
    Implementation, PLDI 2019, Phoenix, AZ, USA, June 22-26, 2019, Kathryn S. McKinley and Kathleen Fisher (Eds.). ACM,
    111–125. doi:10.1145/3314221.3314595
Jacques-Henri Jourdan. 2016. Verasco: a Formally Verified C Static Analyzer. (Verasco: un analyseur statique pour C formellement
    vérifié). Ph. D. Dissertation. Paris Diderot University, France. https://tel.archives-ouvertes.fr/tel-01327023
Gilles Kahn. 1974. The Semantics of a Simple Language for Parallel Programming. In Information Processing, Proceedings of
    the 6th IFIP Congress 1974, Stockholm, Sweden, August 5-10, 1974, Jack L. Rosenfeld (Ed.). North-Holland, 471–475.
Jeehoon Kang, Yoonseung Kim, Chung-Kil Hur, Derek Dreyer, and Viktor Vafeiadis. 2016. Lightweight verification of
    separate compilation. In Proceedings of the 43rd Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming
    Languages, POPL 2016, St. Petersburg, FL, USA, January 20 - 22, 2016, Rastislav Bodík and Rupak Majumdar (Eds.). ACM,
    178–190. doi:10.1145/2837614.2837642
Jens Knoop, Dirk Koschützki, and Bernhard Steffen. 1998. Basic-Block Graphs: Living Dinosaurs?. In Compiler Construction,
    7th International Conference, CC’98, Held as Part of the European Joint Conferences on the Theory and Practice of Software,
    ETAPS’98, Lisbon, Portugal, March 28 - April 4, 1998, Proceedings (Lecture Notes in Computer Science, Vol. 1383), Kai
    Koskimies (Ed.). Springer, 65–79. doi:10.1007/BFB0026423
Jérémie Koenig and Zhong Shao. 2021. CompCertO: compiling certified open C components. In PLDI ’21: 42nd ACM SIGPLAN
    International Conference on Programming Language Design and Implementation, Virtual Event, Canada, June 20-25, 2021,
    Stephen N. Freund and Eran Yahav (Eds.). ACM, 1095–1109. doi:10.1145/3453483.3454097
Paul R. Kosinki. 1978. A Straightforward Denotational Semantics for Non-Determinant Data Flow Programs. In Conference
    Record of the Fifth Annual ACM Symposium on Principles of Programming Languages, Tucson, Arizona, USA, January 1978,
    Alfred V. Aho, Stephen N. Zilles, and Thomas G. Szymanski (Eds.). ACM Press, 214–221. doi:10.1145/512760.512783
Dexter Kozen. 1997. Kleene Algebra with Tests. ACM Trans. Program. Lang. Syst. 19, 3 (1997), 427–443. doi:10.1145/256167.
    256195
Dexter Kozen. 1998. Typed kleene algebra. Technical Report. Cornell University.
Alexander Krauss and Tobias Nipkow. 2012. Proof Pearl: Regular Expression Equivalence and Relation Algebra. J. Autom.
    Reason. 49, 1 (2012), 95–106. doi:10.1007/S10817-011-9223-4
Ramana Kumar, Magnus O. Myreen, Michael Norrish, and Scott Owens. 2014. CakeML: a verified implementation of ML. In
    The 41st Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL ’14, San Diego, CA,
    USA, January 20-21, 2014, Suresh Jagannathan and Peter Sewell (Eds.). ACM, 179–192. doi:10.1145/2535838.2535841
Leslie Lamport and Stephan Merz. 2022. Prophecy Made Simple. ACM Trans. Program. Lang. Syst. 44, 2 (2022), 6:1–6:27.
    doi:10.1145/3492545
Chris Lattner, Andrew Lenharth, and Vikram S. Adve. 2007. Making context-sensitive points-to analysis with heap cloning
    practical for the real world. In Proceedings of the ACM SIGPLAN 2007 Conference on Programming Language Design and
    Implementation, San Diego, California, USA, June 10-13, 2007, Jeanne Ferrante and Kathryn S. McKinley (Eds.). ACM,
    278–289. doi:10.1145/1250734.1250766
Xavier Leroy. 2009. A Formally Verified Compiler Back-end. J. Autom. Reason. 43, 4 (2009), 363–446. doi:10.1007/s10817-
    009-9155-4
Xavier Leroy, Andrew W. Appel, Sandrine Blazy, and Gordon Stewart. 2012. The CompCert Memory Model, Version 2.
    Research report RR-7987. INRIA. http://hal.inria.fr/hal-00703441
Xavier Leroy and INRIA. 2024. The CompCert Verified Compiler. https://compcert.org/. Accessed: 2024-10-24.
Lian Li, Cristina Cifuentes, and Nathan Keynes. 2013. Precise and scalable context-sensitive pointer analysis via value flow
    graph. In International Symposium on Memory Management, ISMM 2013, Seattle, WA, USA, June 20, 2013, Perry Cheng
    and Erez Petrank (Eds.). ACM, 85–96. doi:10.1145/2491894.2466483


     ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
5:64                                                                                                           Z. Cheng et al.


Hongjin Liang, Xinyu Feng, and Ming Fu. 2012. A rely-guarantee-based simulation for verifying concurrent program
   transformations. In Proceedings of the 39th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages,
   POPL 2012, Philadelphia, Pennsylvania, USA, January 22-28, 2012, John Field and Michael Hicks (Eds.). ACM, 455–468.
   doi:10.1145/2103656.2103711
Nancy A. Lynch and Frits W. Vaandrager. 1995. Forward and Backward Simulations: I. Untimed Systems. Inf. Comput. 121, 2
   (1995), 214–233. doi:10.1006/INCO.1995.1134
Nelma Moreira, David Pereira, and Simão Melo de Sousa. 2012. Deciding Regular Expressions (In-)Equivalence in Coq.
   In Relational and Algebraic Methods in Computer Science - 13th International Conference, RAMiCS 2012, Cambridge, UK,
   September 17-20, 2012. Proceedings (Lecture Notes in Computer Science, Vol. 7560), Wolfram Kahl and Timothy G. Griffin
   (Eds.). Springer, 98–113. doi:10.1007/978-3-642-33314-9_7
Carroll Morgan. 1988. The Specification Statement. ACM Trans. Program. Lang. Syst. 10, 3 (1988), 403–419. doi:10.1145/
   44501.44503
Joseph M. Morris. 1987. A Theoretical Basis for Stepwise Refinement and the Programming Calculus. Sci. Comput. Program.
   9, 3 (1987), 287–306. doi:10.1016/0167-6423(87)90011-6
Kedar S. Namjoshi. 1997. A Simple Characterization of Stuttering Bisimulation. In Foundations of Software Technology
   and Theoretical Computer Science, 17th Conference, Kharagpur, India, December 18-20, 1997, Proceedings (Lecture Notes in
   Computer Science, Vol. 1346), S. Ramesh and G. Sivakumar (Eds.). Springer, 284–296. doi:10.1007/BFB0058037
Georg Neis, Chung-Kil Hur, Jan-Oliver Kaiser, Craig McLaughlin, Derek Dreyer, and Viktor Vafeiadis. 2015. Pilsner: a
   compositionally verified compiler for a higher-order imperative language. In Proceedings of the 20th ACM SIGPLAN
   International Conference on Functional Programming, ICFP 2015, Vancouver, BC, Canada, September 1-3, 2015, Kathleen
   Fisher and John H. Reppy (Eds.). ACM, 166–178. doi:10.1145/2784731.2784764
Tobias Nipkow and Dmitriy Traytel. 2014. Unified Decision Procedures for Regular Expression Equivalence. In Interactive
   Theorem Proving - 5th International Conference, ITP 2014, Held as Part of the Vienna Summer of Logic, VSL 2014, Vienna,
   Austria, July 14-17, 2014. Proceedings (Lecture Notes in Computer Science, Vol. 8558), Gerwin Klein and Ruben Gamboa
   (Eds.). Springer, 450–466. doi:10.1007/978-3-319-08970-6_29
Zoe Paraskevopoulou, John M. Li, and Andrew W. Appel. 2021. Compositional optimizations for CertiCoq. Proc. ACM
   Program. Lang. 5, ICFP (2021), 1–30. doi:10.1145/3473591
David Michael Ritchie Park. 1979. On the Semantics of Fair Parallelism. In Abstract Software Specifications, 1979 Copenhagen
   Winter School, January 22 - February 2, 1979, Proceedings (Lecture Notes in Computer Science, Vol. 86), Dines Bjørner (Ed.).
   Springer, 504–526. doi:10.1007/3-540-10007-5_47
Daniel Patterson and Amal Ahmed. 2019. The next 700 compiler correctness theorems (functional pearl). Proc. ACM Program.
   Lang. 3, ICFP (2019), 85:1–85:29. doi:10.1145/3341689
Christine Paulin-Mohring. 2009. A constructive denotational semantics for Kahn networks in Coq. Y. Bertot, G. Huet, J.-J.
   Lévy, and G. Plotkin, editors, From Semantics to Computer Science: Essays in Honour of Gilles Kahn (2009), 383–413.
Gordon Plotkin. 1983. Domains. University of Edinburgh (1983).
Gordon D. Plotkin. 1976. A Powerdomain Construction. SIAM J. Comput. 5, 3 (1976), 452–487. doi:10.1137/0205035
Gabriel Poesia and Fernando Magno Quintão Pereira. 2020. Dynamic dispatch of context-sensitive optimizations. Proc.
   ACM Program. Lang. 4, OOPSLA (2020), 167:1–167:28. doi:10.1145/3428235
Damien Pous. 2013. Kleene Algebra with Tests and Coq Tools for while Programs. In Interactive Theorem Proving - 4th
   International Conference, ITP 2013, Rennes, France, July 22-26, 2013. Proceedings (Lecture Notes in Computer Science,
   Vol. 7998), Sandrine Blazy, Christine Paulin-Mohring, and David Pichardie (Eds.). Springer, 180–196. doi:10.1007/978-3-
   642-39634-2_15
Damien Pous. 2015. Symbolic Algorithms for Language Equivalence and Kleene Algebra with Tests. In Proceedings of the
   42nd Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2015, Mumbai, India,
   January 15-17, 2015, Sriram K. Rajamani and David Walker (Eds.). ACM, 357–368. doi:10.1145/2676726.2677007
Damien Pous. 2016. Coinduction All the Way Up. In Proceedings of the 31st Annual ACM/IEEE Symposium on Logic in
   Computer Science, LICS ’16, New York, NY, USA, July 5-8, 2016, Martin Grohe, Eric Koskinen, and Natarajan Shankar (Eds.).
   ACM, 307–316. doi:10.1145/2933575.2934564
Tahina Ramananandro, Zhong Shao, Shu-Chun Weng, Jérémie Koenig, and Yuchen Fu. 2015. A Compositional Semantics for
   Verified Separate Compilation and Linking. In Proceedings of the 2015 Conference on Certified Programs and Proofs, CPP
   2015, Mumbai, India, January 15-17, 2015, Xavier Leroy and Alwen Tiu (Eds.). ACM, 3–14. doi:10.1145/2676724.2693167
A. W. Roscoe. 2004. Seeing Beyond Divergence. In Communicating Sequential Processes: The First 25 Years, Symposium on
   the Occasion of 25 Years of CSP, London, UK, July 7-8, 2004, Revised Invited Papers (Lecture Notes in Computer Science,
   Vol. 3525), Ali E. Abdallah, Cliff B. Jones, and Jeff W. Sanders (Eds.). Springer, 15–35. doi:10.1007/11423348_2
A. W. Roscoe. 2010. Understanding Concurrent Systems. Springer. doi:10.1007/978-1-84882-258-0
Dana Scott. 1970. Outline of a mathematical theory of computation. Oxford University Computing Laboratory, Programming
   Research Group Oxford.


ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
Denotation-based Compositional Compiler Verification                                                                        5:65


Dana S Scott and Christopher Strachey. 1971. Toward a mathematical semantics for computer languages. Vol. 1. Oxford
   University Computing Laboratory, Programming Research Group Oxford.
Michael B. Smyth. 1978. Power Domains. J. Comput. Syst. Sci. 16, 1 (1978), 23–36. doi:10.1016/0022-0000(78)90048-X
Youngju Song, Minki Cho, Dongjoo Kim, Yonghyun Kim, Jeehoon Kang, and Chung-Kil Hur. 2020. CompCertM: CompCert
   with C-assembly linking and lightweight modular verification. Proc. ACM Program. Lang. 4, POPL (2020), 23:1–23:31.
   doi:10.1145/3371091
Youngju Song, Minki Cho, Dongjae Lee, Chung-Kil Hur, Michael Sammler, and Derek Dreyer. 2023. Conditional Contextual
   Refinement. Proc. ACM Program. Lang. 7, POPL (2023), 1121–1151. doi:10.1145/3571232
Gordon Stewart, Lennart Beringer, Santiago Cuellar, and Andrew W. Appel. 2015. Compositional CompCert. In Proceedings
   of the 42nd Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2015, Mumbai,
   India, January 15-17, 2015, Sriram K. Rajamani and David Walker (Eds.). ACM, 275–287. doi:10.1145/2676726.2676985
Matthijs Vákár, Ohad Kammar, and Sam Staton. 2019. A domain theory for statistical probabilistic programming. Proc. ACM
   Program. Lang. 3, POPL (2019), 36:1–36:29. doi:10.1145/3290349
Di Wang, Jan Hoffmann, and Thomas W. Reps. 2019a. A Denotational Semantics for Low-Level Probabilistic Programs
   with Nondeterminism. In Proceedings of the Thirty-Fifth Conference on the Mathematical Foundations of Programming
   Semantics, MFPS 2019, London, UK, June 4-7, 2019 (Electronic Notes in Theoretical Computer Science, Vol. 347), Barbara
   König (Ed.). Elsevier, 303–324. doi:10.1016/J.ENTCS.2019.09.016
Yuting Wang, Pierre Wilke, and Zhong Shao. 2019b. An abstract stack based approach to verified compositional compilation
   to machine code. Proc. ACM Program. Lang. 3, POPL (2019), 62:1–62:30. doi:10.1145/3290375
Glynn Winskel. 1985. On Powerdomains and Modality. Theor. Comput. Sci. 36 (1985), 127–137. doi:10.1016/0304-3975(85)
   90037-4
Glynn Winskel. 1993. The formal semantics of programming languages - an introduction. MIT Press.
Jim Woodcock and Ana Cavalcanti. 2004. A Tutorial Introduction to Designs in Unifying Theories of Programming. In
   Integrated Formal Methods, 4th International Conference, IFM 2004, Canterbury, UK, April 4-7, 2004, Proceedings (Lecture Notes
   in Computer Science, Vol. 2999), Eerke A. Boiten, John Derrick, and Graeme Smith (Eds.). Springer, 40–66. doi:10.1007/978-
   3-540-24756-2_4
Li-yao Xia, Yannick Zakowski, Paul He, Chung-Kil Hur, Gregory Malecha, Benjamin C. Pierce, and Steve Zdancewic.
   2020. Interaction trees: representing recursive and impure programs in Coq. Proc. ACM Program. Lang. 4, POPL (2020),
   51:1–51:32. doi:10.1145/3371119
Yannick Zakowski, Calvin Beck, Irene Yoon, Ilia Zaichuk, Vadim Zaliva, and Steve Zdancewic. 2021. Modular, compositional,
   and executable formal semantics for LLVM IR. Proc. ACM Program. Lang. 5, ICFP (2021), 1–30. doi:10.1145/3473572
Ling Zhang, Yuting Wang, Jinhua Wu, Jérémie Koenig, and Zhong Shao. 2024. Fully Composable and Adequate Verified
   Compilation with Direct Refinements between Open Modules. Proc. ACM Program. Lang. 8, POPL (2024), 2160–2190.
   doi:10.1145/3632914

Received 05 December 2024; revised 27 October 2025; accepted 23 January 2026




     ACM Transactions on Programming Languages and Systems, Vol. 48, No. 1, Article 5. Publication date: March 2026.
