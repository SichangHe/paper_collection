                                                                  Bi-Abduction for Shapes with Ordered Data 1

                                                                                   Christopher Currya,∗, Quang Loc Leb
                                         a School of Computing, Engineering and Digital Technologies, Teesside University, Middlesbrough, Tees Valley TS1 3BX, UK
                                                                      b University College London, London, Gower Street WC1E 6BT, UK




                                         Abstract
arXiv:2006.10439v1 [cs.LO] 18 Jun 2020




                                         Shape analysis is of great importance for the verification of the correctness and memory-safety of heap-
                                         manipulating programs, yet such analyses have been shown to be highly difficult problems. The integration
                                         of separation logic into shape analyses has improved the effectiveness of the techniques, but the most
                                         significant advancement in this area is bi-abductive inference. Enabled by separation logic, bi-abduction -
                                         a combination of abductive inference and frame inference - is the key enabler for compositional reasoning,
                                         helping to scale up verification significantly. Indeed, the success of bi-abduction has led to the development
                                         of Infer, the tool used daily to verify Facebook’s codebase of millions of lines of code. However, this success
                                         currently stays largely within the shape domain. To extend this impact towards the combination of shape
                                         and arithmetic domains, in this work, we present a novel one-stage bi-abductive procedure for a combination
                                         of data structures and ordering values. The procedure is designed in the spirit of the Unfold-and-Match
                                         paradigm where the inference is utilized to derive any mismatched portion. We have also implemented a
                                         prototype solver, based on the Cyclist library, and demonstrate its capabilities over a range of benchmarks
                                         from the SL-COMP competition. The experimental results show that our proposal shows promise for the
                                         specification inference in an automated verification of heap-manipulating programs.
                                         Keywords: Bi-abduction, Separation Logic, Specification Inference.



                                         1. Introduction

                                             Heap-manipulation is a powerful building block used in many real-world applications and is frequently
                                         utilised in low-level system software such as device drivers. While useful, heap manipulation can also be a
                                         dangerous technique, one in which relatively simple faults can cause significant numbers of issues, ranging
                                         from software crashes [2] to security vulnerabilities [3]. As a result, ensuring the correctness and safety of
                                         such programs is of great importance, yet such analyses have been shown to be highly difficult problems.
                                             In recent years, shape analysis has emerged as a strong candidate for accomplishing such verification
                                         tasks, and with the integration of separation logic [4, 5] into shape analysis techniques, an increasing number
                                         of advanced and usable tools are being developed for automated reasoning over dynamically allocated heap
                                         programs. The success of separation logic comes from the capabilities provided by local reasoning: a program
                                         only has an effect over the memory it accesses, it’s footprint. This local reasoning is enabled by two main
                                         constructions: the separating conjunction operator (∗) and the frame rule. While the former is used to
                                         assert the separation of parts of the heap (i.e., F ∗ G asserts that F and G hold in disjoint heap regions),
                                         the latter can be used to compose the analysis results of separate program parts, such as procedures.

                                            1 This is an extended version of an earlier short paper [1]. The additions over that work include: (1) greater context regarding

                                         the use of bi-abductive inference and an illustrative example showing how it would be applied; (2) a step-by-step illustration
                                         of our technique in use; (3) greater detail concerning each stage of the proof process; (4) an extension to the technique, adding
                                         support for both binary trees and binary search trees; (5) details of a prototype implementation of the technique and (6)
                                         experimental results from applying the prototype tool to examples taken from SL-COMP.
                                            ∗ Corresponding Author



                                                                                                         1
    One of the most promising techniques currently utilised to automate local reasoning is bi-abductive
inference [6–8]. Bi-abductive inference, or bi-abduction for short, is the combination of the abductive
inference and frame inference techniques into a singular analysis. Given two formulas in separation logic, A
and C, bi-abduction aims to identify some non-trivial terms ?M and ?F such that the entailment
                                             A ∗ [?M ] ⊢ C ∗ [?F ]
is satisfied. Bi-abduction has seen a large growth in interest in recent years due to a number of useful
properties of the technique. First, bi-abductive techniques generally have very low requirements placed
upon the end-user, with many requiring only the code of the program to be analysed. Second, bi-abduction
is a powerful enabler of compositional analysis: an analysis in which the final output is the combination
of the results of smaller analyses over components of the program, typically procedures. Compositional
analyses provide a number of significant benefits, including high scalability, parallelisation, the ability to
undertake incremental analyses and potential support for graceful failure, all highly desirable properties for
an analysis technique. More recent work has also included advances that support the use of bi-abductive
inference over near-arbitrary data structures [8], further improving the usability of the technique.
    However, while bi-abduction has proven to be a highly capable technique for use in program analysis, the
majority of existing implementations stay within the shape domain only. This restriction not only limits the
range of inputs that can be supported by the technique, but also carries the potential risk of imprecision when
used to analyse data structures that have pure constraints as a component of their design, such as binary
search trees or sorted linked lists. Currently, efforts are being made towards extending bi-abduction to the
combined domain, allowing bi-abductive techniques to operate over general pure constraints in addition to
those shape properties, with common examples of investigated pure constraints including size, ordering and
content (bag) properties. As an example, the technique outlined by Trinh et al [9] utilises an enrichment-
based approach to the identification of pure constraints, but is fully reliant upon some previous shape analysis
in order to function. This multi-phase approach is common in the literature of combined domain verification
techniques [10], and while it has been shown to be effective, the approach is apparently not very efficient.
Additionally, by separating the shape and pure domain, the accuracy of the final inferred specification would
be heavily reliant upon the accuracy and expressiveness of the shape information determined in the initial
analysis, potentially negatively affecting the quality of the overall result.
    For both effectiveness and efficiency, in this work, we present a novel one-phase bi-abduction procedure
for the combination of shape and ordering properties. In particular, we develop a set of inference rules
and a novel algorithm to search for a sequence of rule applications. Our search algorithm operates based
on the Unfold-and-Match principle as follows: firstly, it unfolds inductive predicates, as well as subtracting
heaps identified on both sides of the bi-abductive entailment. If this process cannot progress due to missing
heap components on the left-hand side (LHS), it invokes an abductive rule to infer part of the anti-frame.
Likewise, if the process cannot progress due to the extra heap components on the right-hand side (RHS), it
invokes a procedure to infer part of the frame. Our system is more expressive than the bi-abduction system
used in Infer [6] as it could deal with inductive definitions with ordering properties. Additionally, our
system is as powerful as the combination of bi-abduction for shape domains (e.g., [6, 8]) and pure inference
for ordering properties in the arithmetic domain (e.g., [9, 10]). Moreover, the proposed proof system is
proven to be sound and terminating. We also present a prototype implementation of the tool, developed
as an instantiation of the Cyclist library [11], and demonstrate its capabilities over a range of benchmarks
from the SL-COMP competition [12].

Organization. The remainder of this paper is organized as follows. Section 2 discusses related works. Section
3 shows the syntax of separation logic formulas and formalism of the bi-abductive problem. Section 4
describes our overall approach, supported with an illustrative example. Sections 5, 6, and 7 present our
main result: a bi-abduction procedure through an inference system. Next, Section 8 discusses soundness and
termination of the proposed procedure. Section 9 shows the implementation and the evaluation is discussed
in Section 10. Finally, Section 11 concludes the work.


                                                       2
2. Related Work

    There are a number of works related to our technique. For classical bi-abduction, Infer [6] remains the
most well-known and is essentially a “pure” implementation of the bi-abduction technique [6]. Extensions
have been made to the tool, but its bi-abductive capabilities remain restricted to shape properties. Other
techniques to take advantage of bi-abductive inference include the JaVerT [13] and Gillian [14] verification
and testing frameworks, which utilise shape-only bi-abduction to correct identified deficiencies in specifica-
tions during a compositional analysis of real-world programs. In addition to these, some extended versions
of the technique have also been investigated, with the second-order bi-abduction technique of Le et. al.
[8, 15] for general shape-only inductive predicates beyond list and binary trees.
    In the area of combined domain, there is a small number of relevant works. One of the earliest in this
area is the work of Trinh et. al., described in [9]. Building upon a set of shape properties obtained from some
previous shape analysis, the technique extends the shape predicates with a set of pure terms representing
properties such as size or order, alongside additional predicates representing relational information over the
structure. A forwards analysis is then undertaken to generate proof obligations for the relational predicates,
which are then finalised via a fixpoint analysis, producing a precondition ensuring memory safety and
termination. One of the most developed techniques for combined domain bi-abduction, and close to our
own work, is the work of Qin et al [16]. This technique is also based around a fixpoint analysis of the
target program, abducting necessary state components in each pass, developing stronger preconditions until
a fixpoint is reached. This stage is guided through user-defined predicates outlining the expected data
structures encountered, identifying several aspects of the pure domain in these passes. However, a secondary
bi-abductive inference is still necessary to obtain smaller components of pure information during the final
abstraction phase for each iteration, and widening operations utilised to accelerate reaching the fixpoint
may introduce soundness issues. Since it is not truly a single-stage bi-abductive method as our system is,
the performance of the tool is degraded by the two-phase analysis.
    A range of other combined domain analysis techniques exist in the literature: Thor [10] is capable
of handling pure properties alongside memory safety, able to operate over ordering, shape, size or depth
properties via an additional analysis over a ”proof program”. Chang et al [17] describe a generalised
framework for shape analysis based around forward abstract interpretation with additional support for
relations between data values. The venerable TVLA system [18] is capable of supporting a wide range of
structures and properties, including complex pure properties such as ordering, though is limited by the lack
of support for compositional reasoning. Finally, techniques based on Forest Automata are also known [19],
though few can operate in the combined domain [20].

3. Preliminaries

   In this section, we present the syntax of separation logic formulas (Subsection 3.1), their semantics
(Subsection 3.2), and the problem targeted by our technique (Subsection 3.3).

3.1. Syntax
    The language used in our work is shown in Figure 1a. Program variables are defined as italic characters,
and refer to variables originating from within the program itself. Logical variables are indicated with upper-
case letters, such as X, and refer to variables that appear in the analysis only. For readability, we often
omit record fields from the notation where unambiguous: x7→[n:y, v:z] may be shortened to x7→[y, z], as an
example. We may additionally omit the square brackets around single-field records, as in x7→y.
    Our language includes inductive definitions describing fundamental list structures: ls, representing a
simple singly-linked list, and sls, representing a sorted singly-linked list. We have also included definitions
for a binary tree tree and a binary search tree stree, an addition to our initial work [1]. The full inductive
definitions of these shape predicates may be found in Figure 1b.
    A singly-linked list ls(E1 , E2 ) consists of a series of nodes linked via a pointer, starting with E1 and
ending at E2 (non-inclusive). Each of the list predicates included in our system can be used to define a
list segment or a full null-terminated list, dependant only on the value of E2 . A sorted singly-linked list
                                                      3
                   x, y, ... ∈ V ar                                                              variables
                   f, fi , ... ∈ F ields                                                           fields
                   E ::= null | x                                                              expressions
                   V ::= i, j, ... ∈ V alues                                                      values
                   P ::= E=E | E<E                                                        simple pure formulae
                   Π ::= true | P | ¬Π | ∃v.Π | Π ∧ Π                                         pure formulae
                   ρ ::= f1 : E1 , ..., fk : Ek                                             record expressions
                   Σ ::= emp | E7→[ρ]| Σ ∗ Σ | ls(E, E) | sls(E, x, y, E)
                   ∆ ::= Π ∧ Σ                                                              qf symbolic heaps
                               →
                               −
                   H ::= ∃ X .∆                                                              symbolic heaps
                                                     (a) Grammar Definitions

                           def
 ls(E1 , E2 )              =     E1 = E2 ∧ emp ∨ ∃E ′ .E1 6= E2 ∧ E1 7→[E ′ ] ∗ ls(E ′ , E2 )
                           def
 sls(E1 , V1 , V2 , E2 )   =     E1 =E2 ∧ V1 =V2 ∧ emp ∨ ∃E ′ , V ′ .V1 ≤V ′ ∧ E1 6=E2 ∧ E1 7→[E ′ , V1 ] ∗ sls(E ′ , V ′ , V2 , E2 )
                           def
 tree(E)                   =     E = null ∧ emp ∨ E7→[l, r] ∗ tree(l) ∗ tree(r)
                           def
 stree(E, V1 , V2 )        =     E = null ∧ V1 = V2 ∧ emp
                                   ∨ ∃V3 , V4 .V3 ≤V ′ ∧ V ′ ≤V4 ∧ E7→[l, r, V ′ ] ∗ stree(l, V1 , V3 ) ∗ stree(r, V4 , V2 )
                                                     (b) Predicate Definitions

                                                   Figure 1: Language Fragment


sls(E1 , V1 , V2 , E2 ) is a sequence of singly-linked nodes, beginning with node E1 and ending at some node
E2 (non-inclusive), with all values stored in those nodes obeying an ascending order. In order to simplify
the checking of these structures, the minimum and maximum values of the list are also tracked inside the
predicate, with the minimum value being represented as V1 and the maximum V2 . Note that V2 is not the
value of node E2 ; rather, V2 would refer to the value of the final node in the list, which points to E2 . Both
tree(E) and stree(E, V1 , V2 ) describe a binary tree: a single node pointing to two known subtrees, or a null
root describing an empty tree. As with ls and sls, the primary difference between tree and stree is the
consistent ordering constraints present in stree, which ensures that all values in the left subtree of an stree
are lower than the value of the root node, and all values in the right subtree are greater than the value of the
root. Minimum and maximum values are recorded in stree predicates in a similar manner to sls predicates.

3.2. Semantics
    The semantics of this fragment are quite standard, following from the semantics of separation logic
with general inductive definitions and arithmetic presented in [21]. These semantics are given by a relation
s,h |= H that forces the stack s and heap h to satisfy the constraint H, where h ∈ Heaps, s ∈ Stacks, and
H is a formula. Stack and heap abstractions are defined as:
                                                  def
                                        Heaps      =    Values⇀f in (Fields × Values)N
                                                  def
                                        Stacks     =    Var → Values
where N is the maximum number of fields.
  The semantics of our fragment are as follows:
                 s, h |= emp            iff     dom(h)={}
                 s, h |= E7→[fi :vi ]   iff     dom(h)={s(E)}h(s(E))=( (f1 , s(E1 )), ..., (fN , s(EN )) )
                 s, h |= Σ1 ∗ Σ2        iff     ∃h1 , h2 · h1 #h2 and h=h1 ·h2 , s, h1 |= Σ1 and s, h2 |= Σ2
                 s, h |= true           iff     always
                 s, h |= Π ∧ Σ          iff     s, h |= Σ and s |= Π
                 s, h |= ∃v.∆           iff     ∃α · s[v7→α], h |= ∆
                 s, h |= H1 ∨ H2        iff     s, h |= H1 or s, h |= H2
                                                                   4
where dom(f ) is the domain of function f , h1 #h2 denotes disjoint heaps h1 and h2 i.e., dom(h1 )∩dom(h2 )=∅,
and h1 ·h2 denotes the union of two disjoint heaps. If s is a stack, v∈Var, v6∈dom(s) and α∈Values∪Loc,
we write s[v7→α] ≡ s∪{(v, α)}. Note that in a concrete memory model such as the RAM model, the field
names of points-to predicates are transformed into pointer offsets. The pair (fi , s(Ei ) (for all i ∈ {1...N })
would then be interpreted as s(E) + off fi = s(Ei ), where off fi is the corresponding offset of field fi . The
entailment H |= H ′ holds iff for all s and h, we have if s, h |= H then s, h |= H ′ . Note that we also preserve
s(null) as a special value such that it is not in any domain of heaps.

3.3. Bi-Abduction
    In this subsection, we first discuss two sub-problems: abductive inference and frame inference. Following
this, we formally define the bi-abductive problem.

Abductive Inference. Abductive inference is an analysis technique that aims to identify the “missing” por-
tions of a program state required to satisfy some entailment. Initially inspired by the work of Peirce [22],
abductive inference has seen a surge in interest over recent years, with its applications in the field of shape
analysis being the focus of this work. In general, abductive inference aims to find some anti-frame ?M such
that the entailment: A ∗ [?M ] ⊢ C is satisfied2 .
    For a given entailment, there may be many possible solutions for the anti-frame, often varying in the level
of detail outlined by a particular formula. As a result of this, abductive inference techniques often make use
of a ranking function in order to identify the best solution for a given abduction. These ranking functions
vary between implementations, but typically favour the solution with the smallest spatial footprint in order
to generate higher-quality specifications. Additional constraints are also enforced over the possible solutions:
trivial solutions such as ?M = false are prohibited in order to ensure a useful solution is identified.

Frame Inference. Frame inference can be seen as the counterpart to abductive inference. Given an entailment
A ⊢ C, frame inference aims to identify some ?F such that A ⊢ C ∗ [?F ] holds. This ?F is the frame of the
entailment, some additional fragment of the program state that is not necessary to prove the entailment.
For example, consider the entailment: x 6= y ∧ x7→3 ∗ y7→4 ⊢ x7→3 ∗ [?F ]. It can be readily seen that
this entailment can be satisfied, as x7→3 is present in both the antecedent and consequent. However, the
fragment y7→4 is not necessary to show the satisfiability of the entailment and could be removed without a
negative effect; y7→4 is the frame of this example.
    The identification of the frame of an entailment in an analysis is crucial to supporting both the use of
procedure specifications and compositional analyses. By identifying the portion of the state that will not be
modified by a given procedure, the postcondition of the invoked procedure, when extended with the frame,
will be an accurate representation of the program state upon return. This extended postcondition can be
directly adopted as the state, allowing for a simple continuation of the analysis without the need to analyse
the procedure itself, assuming the specification is known.

Bi-Abduction. We use F V (H) to denote all free variables in formula H. Throughout this work, we consider
the bi-abductive problem which is defined as:

                  PROBLEM: QF BIABD.
                  INPUT:    ∆ and ∆′ where F V (∆′ ) ⊆ F V (∆) ∪ {null}.
                  QUESTION: Does there exist ?M, ?F such that ∆ ∗ ?M |= ∆′ ∗ ?F holds?

4. Overview and Illustration

   To illustrate how bi-abduction is applied for specification inference, consider the program detailed in
Figure 2. insertSorted outlines a basic insertion procedure for sorted lists. It is designed to insert the

   2 A variation of abductive inference for classical logic is also described in the literature; it is mechanically identical, using

classical logic’s ∧ in place of separation logic’s ∗.

                                                                 5
 1   Node i n s e r t S o r t e d ( Node l , Node y ){
 2   // Inf . PRE : sls (l ,I ,J , null ) ∗ y7→ [N , K ]
 3        Node p = f i n d P o s(l , y . val );
 4        if ( p == null ) {
 5            y . next = l ;
 6            return y ;
 7        }
 8        else {
 9            y . next = p . next ;
10            p . next = y ;
11            return l ;
12        }
13   }// Inf . POST :
14   // ret = y ∧ K < I ∧ y7→ [l , K ] ∗ sls (l ,I ,J , null ) ∨
15   // ret = l ∧ p6= null ∧ A≤B ∧ B < K ∧ B≤C ∧ K≤C ∧
16   // sls (l ,I ,A , p ) ∗ p7→ [y , B ] ∗ y7→ [M , K ] ∗ sls (M ,C ,D , null )
17
18   Node f i n d P o s( Node l , int x ){
19   // S U M M A R Y ONLY
20   // Given PRE :
21   // sls (l ,i ,j , null );
22   // Given POST :
23   // ret = null∧x < i∧sls (l ,i ,j , null ) ∨
24   // A≤B ∧ B < x ∧ B≤C ∧ x≤C ∧
25   // sls (l ,i ,A , ret ) ∗ ret7→ [M , B ] ∗ sls (M ,C ,D , null )
26   }

                                         Figure 2: Sorted List Insertion



node y into the sorted list rooted at l, preserving the ordering properties of the data structure. Assuming
we are given a procedure summary (a specification using Hoare triples) of the procedure findPos, we show
how to infer the pre and post of insertSorted at lines 2 and 13.
   The inference begins with the precondition emp and proceeds to execute the code at line 3. In order to
show that the procedure does not contain a null-dereference error over pointer y, we call the bi-abductive
procedure with the following query:

                                   emp ∗ [?M ] ⊢ ∃N, K. y7→[N, K] ∗ [?F ]

The procedure identifies an anti-frame ?M ≡ y7→[N, K] and the corresponding frame ?F ≡ emp, leading us
to infer that we would execute the procedure with precondition y7→[N, K] rather than emp.
    We then proceed to the procedure call for findPos, using its summary. By means of compositional
analysis, we send the following query to the bi-abductive procedure:

                              y7→[N, K] ∗ [?M ] ⊢ ∃I, J. sls(l, I, J, null) ∗ [?F ]

which returns ?M ≡ ∃I, J. sls(l, I, J, null) and ?F ≡ y7→[N, K]. This inference identifies the fact that in
order to satisfy the precondition of findPos, l must be the head of a sorted list and y must be an assigned
node with a value field, a state that can intuitively be seen as reasonable. While the anti-frame is spatially
conjoined into the insertSorted precondition, the frame is composed with the post of findPos to constitute
the post-state of the call. We then continue the execution forward until we obtain the postconditions of the
return statements, and so the procedure.

                                                       6
4.1. Bi-Abductive Procedure
    The core of the proposed bi-abductive procedure is a search algorithm that, given some starting entail-
ment, scans through the set of proof rules for a rule that can be applied on the entailment. Once such a
rule is identified, it is applied to the entailment to obtain some new sub-goals (and possibly fragments of
the frame or anti-frame) until it can make a decision as to whether the entailment holds. All proof rules
in our system are checked and applied in a specific order, aiming to ensure the process identifies the weak-
est possible preconditions and the strongest possible postconditions, while maintaining the validity of the
solutions and forbidding trivial or false preconditions. The rules are searched in the following order:
  1. Firstly, rules in Sect. 5 are applied exhaustively to unfold all possible scenarios and normalize the
     antecedent of the input entailment.
  2. Secondly, rules in Sect. 6 are applied to match terms across the antecedent and consequent, removing
     them where possible. If heaps in the two sides are empty, the algorithm returns successfully.
  3. Lastly, it checks whether or not any rules in Sect. 7 could be applied to infer an anti-frame and frame.
     That is to identify portions of heap and pure information missing/immutable from the entailment,
     moving terms missing from the antecedent to the precondition and moving immutable terms from the
     antecedent to the postconditions. After that, it repeats the first phase.
    The normalization in the first phase is essential for the subsequent two phases. It ensures that every
spatial predicate in a normalized formula is precise; that is, given that s, h |= H and H is in normal form,
then for any spatial predicate p ∈ H, there exists one and only one sub-heap h′ ⊆ h such that s, h′ |= p.
In turn, this precision helps to guide the matching and inference rules, as given a predicate p on one side
of a normalized entailment, there exists one and only one predicate p′ on the other side such that p and
p′ are matched using the rules in the second phase. Furthermore, if we could not find such a predicate
p′ in the existing entailment, p′ is eventually missing. The inference rules in the third phase reveal the
missing predicates and then add them back to the entailment. This forms the foundation for the inference
mechanism in our work.

4.2. A Bi-Abduction Example
    We will now demonstrate our technique over an example entailment. This example, shown below, features
sorted singly linked lists, with a known root and (non-inclusive) end-point, as well as a known minimum
and maximum value. This predicate, discussed in detail in Section 3, can be seen in full in Figure 1b.

                  w7→[x, i] ∗ x7→[y, j] ∗ sls(y, k, l, z) ∗ [?M ] ⊢ sls(x, j, l, z) ∗ z7→null ∗ [?F ]      (1)

    Our technique aims to identify whether a given entailment holds, and if not, identify some values for
the symbolic heap fragments ?M and ?F . These fragments, named the anti-frame and frame respectively,
when introduced into the initial invalid entailment, will ensure that the now corrected entailment will hold
(note that we will omit these placeholders for spacing reasons in this example). In order to achieve this, our
technique first aims to convert the entailment into an appropriate normalized form. In this form, predicates
in the antecedent will have a singular configuration, ensuring there will be very little ambiguity as to the
contents of the program memory. The initial stage of this process is to identify implicit constraints and
introduce pure terms in order to ensure that those constraints are explicit in the entailment. Initially, this
will produce the entailment:

          w6=null ∧ x6=null ∧ w6=x ∧ w7→[x, i] ∗ x7→[y, j] ∗ sls(y, k, l, z) ⊢ sls(x, j, l, z) ∗ z7→null   (2)

   In this entailment, the two assigned nodes, w and x now have explicit non-null constraints, as any assigned
node cannot by definition be null. Similarly, as there are now two separate, non-null, non-empty spatial
terms, these two variables cannot be aliases, and so an inequality between the two is also introduced. These
terms ensure that certain contradictory inferences are detected, or in some cases prevented, and ensuring
that invalid branches do not progress.

                                                          7
    Following this, the next key part of this transformation is to force any shape predicates (in this case, the
sls predicate) into either the base case, indicating that the predicate is equivalent to an empty heap, or the
recursive case, ensuring that the predicate refers to at least a single assigned node in memory. In order to
achieve this, we apply a form of the excluded middle rule, identifying equalities and disequalities such that
the entailment will only permit one of the two cases of the shape predicate. This process will also create
branches in the entailment, one for each configuration of the shape predicate, allowing for the exploration
of all possible states of the data structure. For this example, the two produced branches are as follows:

       w6=null ∧ x6=null ∧ x6=w ∧ y6=z ∧ w7→[x, i] ∗ x7→[y, j] ∗ sls(y, k, l, z) ⊢ sls(x, j, l, z) ∗ z7→null   (3)

       w6=null ∧ x6=null ∧ x6=w ∧ y=z ∧ w7→[x, i] ∗ x7→[y, j] ∗ sls(y, k, l, z) ⊢ sls(x, j, l, z) ∗ z7→null    (4)
    Entailment 3 represents the case in which the sorted list is non-empty, and Entailment 4 represents the
case in which the predicate is empty. The inclusion of the equality (or inequality) between y and z ensures
that, when expanded, the predicate definition can only permit one of the cases to hold, thus eliminating
the other from that branch of the entailment. From this point, the illustration focuses on Entailment 3,
the recursive case. The technique proceeds onwards, identifying a small number of further constraints:
first, as the sls predicate is non-empty, y, the head of that list must be non-null. Secondly, as in the
earlier stages, constraints enforcing the non-aliasing of y with the other non-null variables are identified,
and finally, in order to ease further inference, the ordering constraint between the minimum and maximum
values in the predicate is also expressed as a separate constraint. Introducing these constraints into the
entailment concludes the normalisation phase, as the resulting antecedent can now only refer to a single
heap configuration. The fully normalised entailment is as follows:

    w6=null ∧ x6=null ∧ y6=null ∧ x6=w ∧ y6=w ∧ y6=x ∧ y6=z ∧ k≤l ∧ w7→[x, i] ∗ x7→[y, j] ∗ sls(y, k, l, z)
         ⊢ sls(x, j, l, z) ∗ z7→null                                                                           (5)

    Once no further normalisation can take place, the system will begin to match and subtract spatial
components of the entailment, aiming to reduce the entailment to an empty heap. Initially, the procedure
will match the node x7→[y, j] against the sls predicate in the consequent, recognising that they share a head
variable. The procedure will then implicitly unfold the predicate, match the concrete node with the freshly
concretized node in the consequent and subtract both from the entailment.

         w6=null ∧ x6=null ∧ y6=null ∧ x6=w ∧ y6=w ∧ y6=x ∧ y6=z ∧ k≤l ∧ w7→[x, i] ∗ sls(y, k, l, z)
               ⊢ j≤k ∧ sls(y, k, l, z) ∗ z7→null                                                               (6)

    The procedure would also repeat any normalisation steps at this stage, but no such steps are needed in
this example. Following this, another match is identified, recognising that there are identical spatial terms
on each side of the entailment: sls(y, k, l, z). As the predicates are identical, there is no need to unfold
either of the predicates, and so both terms are simply removed, leaving the entailment

       w6=null ∧ x6=null ∧ y6=null ∧ x6=w ∧ y6=w ∧ y6=x ∧ y6=z ∧ k≤l ∧ w7→[x, i] ⊢ j≤k ∧ z7→null               (7)

    At this stage, there are no further matches that can be made with the remaining terms, both spatial
and pure. As a result, the procedure continues on to attempting to infer some aspect of the antecedent or
consequent that would allow for the proof to continue. In this case, the only solution is to recognise that
the remaining spatial nodes are part of the frame and anti-frame. To handle this, the procedure applies
inference rules that record the relevant terms as part of either the frame or anti-frame, and removes them
from the entailment. In this manner, the remaining nodes are subtracted from the entailment, and are
tracked separately as part of either ?M or ?F . After applying these rules, only pure terms remain:

                   w6=null ∧ x6=null ∧ y6=null ∧ x6=w ∧ y6=w ∧ y6=x ∧ y6=z ∧ k≤l ⊢ j≤k                         (8)

  As there is no overlap between these pure terms, and no further refinement or subtractions can be
made, the procedure concludes that these pure terms are part of the frame and anti-frame. Applying a
                                                        8
final inference rule, all remaining pure terms are recoreded as part of the relevant inferred fragment and
subtracted from the entailment, reducing it to true ∧ emp ⊢ true ∧ emp and ending the proof of this branch.
    From here, the procedure backtracks to the second branch produced by the case-split over the predicate
and repeats this process. The proof proceeds in a highly similar manner, with one significant exception:
immediately following the branching caused by splitting the entailment, the produced equality is applied to
the whole entailment. The result:

          w6=null ∧ x6=null ∧ x6=w ∧ w7→[x, i] ∗ x7→[y, j] ∗ sls(y, k, l, y) ⊢ sls(x, j, l, y) ∗ z7→null         (9)

includes an sls predicate where both the start and end point are identical. In this case, the predicate equates
to emp, causing the procedure will subtract the predicate and introduce an equality over the values in order
to preserve that information. This eliminates both list fragments much earlier in the proof, accelerating the
eventual conclusion of the branch.
    Once all branches in the proof have been completed, the procedure collects all fragments of the anti-frame
and propagates them back to the initial entailment, and gathers the final resulting frame from each branch
in a similar way. Once substituted back into the initial entailment, we obtain the final outputs:

 z6=null ∧ j≤k ∧ w7→[x, i] ∗ x7→[y, j]7→sls(y, k, l, z) ∗ z7→null
     ⊢ w6=null ∧ x6=null ∧ y6=null ∧ x6=w ∧ y6=w ∧ y6=x ∧ y6=z ∧ k≤l ∧ w7→[x, i] ∗ sls(x, j, l, z) ∗ z7→null

 l=k ∧ y=z ∧ y6=null ∧ j≤l ∗ w7→[x, i] ∗ x7→[y, j] ∗ z7→null ∗ sls(y, k, l, z)
     ⊢ l=k ∧ y=z ∧ x6=null ∧ w6=null ∧ x6=w ∧ w7→[x, i] ∗ sls(x, j, l, z) ∗ z7→null

    In the following sections, we will go into further details as to the purpose of each stage of our procedure,
as well as the the design and utilisation of the inductive rules of those stages. For the normalisation stage,
Section 5 describes its purpose in greater detail, as well as presenting the rules employed to transform
entailments into that normalised form. For the core matching and subtraction stage, Section 6 outlines the
rules, aims and processes of that step of our procedure. Finally, Section 7 presents our inference rules, and
discusses both their use and design intentions.

5. Unfolding and Normalization

   In this section, we will discuss the design of our normal form, as well as the design and usage of the corre-
sponding normalisation rules, which are detailed in Figure 3. In the definition of our normal form, we utilise
a small number of shorthand symbols to represent a range of values: the symbol op(E) denotes one of the
separation logic expressions supported by our system, namely E7→[ρ], ls(E, F ), sls(E, V, V ′ , F ), tree(E) and
                                                                                 def                       def
stree(E, V, V ′ ). Additionally, the guard G(op(E)) is defined as G(E7→[ρ]) = true, G(ls(E, F )) = E6=F ,
                    def                    def                                  def
G(sls(E, V, V ′ , F )) = E6=F , G(tree(E)) = E 6= null, G(stree(E, V, V ′ )) = E 6= null, and describes the
condition that will enforce non-empty properties over the corresponding op. The conditions of the normal
form itself are defined as follows:
Definition 1 (Normal Form). A formula Π∧Σ is in normal form (NF for short) if:
  1. op(E) ∈ Σ implies G(op(E)) ∈ Π.
  2. op(E) ∈ Σ and G(op(E)) ∈ Π imply E6=null ∈ Π.
  3. op1 (E1 ) ∗ op2 (E2 ) ∈ Σ, G(op1 (E1 )) ∈ Π, and G(op2 (E2 )) ∈ Π imply E1 6=E2 ∈ Π.
  4. E1 =E2 6∈ Π.
  5. E6=E 6∈ Π.
  6. Π is satisfiable.
   If ∆ is in NF and for any s and h such that s, h |= ∆, dom(h) is uniquely defined by s. A bi-abductive
entailment is in NF if its antecedent is in NF.

                                                        9
                              [SUBST]                                       [LIDENT =]
                  (Π ∧ Σ)[E/x] ∗ [M ] ⊢ ∆[E/x] ∗ [F ]                    (∆) ∗ [M ] ⊢ ∆′ ∗ [F ]
             (Π ∧ x=E ∧ Σ) ∗ [M ∧ x=E] ⊢ ∆ ∗ [F ∧ x=E]                (∆ ∧ E=E) ∗ [M ] ⊢ ∆′ ∗ [F ]

                                         [EXCLUDE − MIDDLE]
                   (E1 =E2 ∧ ∆1 ) ∗ [M1 ] ⊢ ∆′ ∗ [F1 ]   (E1 6=E2 ∧ ∆2 ) ∗ [M2 ] ⊢ ∆′ ∗ [F2 ]
                                      ∆ ∗ [M1 ∧ M2 ] ⊢ ∆′ ∗ [F1 ∨ F2 ]
                               (where F V (E1 , E2 ) ⊆ (F V (∆1 )∪F V (∆2 )))
              [LS−LBASE]                                            [SLS−LBASE]
           (∆) ∗ [M ] ⊢ ∆′ ∗ [F ]                        (∆[V ′ /V ]) ∗ [M ] ⊢ ∆′ [V ′ /V ] ∗ [F ]
      (∆ ∗ ls(E, E)) ∗ [M ] ⊢ ∆′ ∗ [F ]      (∆ ∗ sls(E, V, V ′ , E)) ∗ [M ∧ V = V ′ ] ⊢ ∆′ ∗ [F ∧ V = V ′ ]
            [TREE − LBASE]                                       [STREE − LBASE]
            (∆) ∗ [M ] ⊢ ∆′ ∗ [F ]                        (∆[V ′ /V ]) ∗ [M ] ⊢ ∆′ [V ′ /V ] ∗ [F ]
     (∆ ∗ tree(null)) ∗ [M ] ⊢ ∆′ ∗ [F ]      (∆ ∗ stree(null, V, V ′ )) ∗ [M ∧ V =V ′ ] ⊢ ∆′ ∗ [F ∧ V =V ′ ]
                   [NODE−EX]                                                   [NODES−EX]
  (G(op(E)) ∧ E6=null ∧ ∆ ∗ op(E)) ∗ [M ] ⊢ ∆′ ∗ [F ]         E1 6=E2 ∧ ∆ ∗ op1 (E1 )∗op2 (E2 )) ∗ [M ] ⊢ ∆′ ∗ [F ]
       (G(op(E)) ∧ ∆ ∗ op(E)) ∗ [M ] ⊢ ∆′ ∗ [F ]                   (∆ ∗ op1 (E1 )∗op2 (E2 )) ∗ [M ] ⊢ ∆′ ∗ [F ]
                (where E6=null∈∆)
                                /                           (where E1 6=E2 6∈∆ and G(op1 (E1 )), G(op2 (E2 )) ∈ ∆)

                                  Figure 3: Normalization Rules for Bi-Abduction




    Figure 3 shows the inference rules used by our system to transform a bi-abductive entailment into it’s
NF. For the first condition of NF, we apply EXCLUDE-MIDDLE. This rule splits the case in the entailment,
identifying formulas that force a shape predicate into either its base or recursive case, due to contradicting
pure constraints. The proof then branches, one branch enforcing the base case, and one enforcing the
recursive case. For the second condition of NF, NODE-EX explicates the fact that given a heap h, for any
l ∈ dom(h), then l 6= null. For the third condition of NF, NODEs-EX explicates the semantics of the separating
conjunction ∗: given a heap h, for any l1 , l2 ∈ dom(h), then l1 6= l2 . For the fourth condition of NF, while
LIDENT= discards redundant equalities, LS-LBASE, SLS-LBASE, TREE-LBASE and STREE-LBASE concretises the
inductive predicates with its base case prior to applying any corresponding substitution. While the fifth
condition of NF could be checked syntactically, the sixth would be performed using an SMT solver such as
Z3 [23].
    Transforming the bi-abduction problem into it’s normalised form is a key stage of our technique. By
normalising the entailment, ambiguity in the entailment is eliminated and any potential contradictions are
identified. This precise representation is critical to the effectiveness of our rules.

6. Matching and Subtraction

    We will now discuss the process of matching and subtraction in our technique, alongside the rules
underpinning this design. At it’s core, this second phase of the search is aimed at identifying and resolving
equivalent and overlapping segments of the entailment, aiming to reduce both sides of the entailment to
emp. The subtraction rules, detailed in Figure 4, aim to achieve this goal in one of three ways, with each
rule grouped according to manner in which the rule operates.
    The first group consists of decision rules, EMP and IDENT and are defined as follows:

                                                    [EMP]
                               Π ∧ emp ∗ [true ∧ emp] ⊢ true ∧ emp ∗ [Π ∧ emp]

                                                       10
                  [RIDENT =]                                    [∗−INTRODUCTION]
                ∆ ∗ [M ] ⊢ ∆′ ∗ [F ]             Σ ∗ [M1 ] ⊢ Σ′ ∗ [F1 ] Π ∧ Σ1 ∗ [M2 ] ⊢ Π′ ∧ Σ2 ∗ [F2 ]
            ∆ ∗ [M ] ⊢ ∆′ ∧ E=E ∗ [F ]              Π ∧ Σ ∗ Σ1 ∗ [M1 ∗ M2 ] ⊢ Π′ ∧ Σ′ ∗ Σ2 ∗ [F1 ∗ F2 ]

         [HYPOTHESIS]
                                                       [LS−BASE]                            [TREE − BASE]
     Π ∧ Σ ∗ [M ] ⊢ Π′′ ∧ Σ′ ∗ [F ]
                                                    ∆ ∗ [M ] ⊢ ∆′ ∗ [F ]                   (∆) ∗ [M ] ⊢ ∆′ ∗ [F ]
   Π ∧ Σ ∗ [M ] ⊢ Π′ ∧ Π′′ ∧ Σ′ ∗ [F ]
           (where Π ⇒ Π′ )                     ∆ ∗ [M ] ⊢ ∆′ ∗ ls(E, E) ∗ [F ]        ∆ ∗ [M ] ⊢ ∆′ ∗ tree(null) ∗ [F ]

                     [SLS−BASE]                                                  [STREE − BASE]
                ∆ ∗ [M ] ⊢ ∆′ [V ′ /V ] ∗ [F ]                                ∆ ∗ [M ] ⊢ ∆′ [V ′ /V ] ∗ [F ]
     ∆ ∗ [M ] ⊢ ∆′ ∗ sls(E, V, V ′ , E) ∗ [F ∧ V = V ′ ]           ∆ ∗ [M ] ⊢ ∆′ ∗ stree(null, V, V ′ ) ∗ [F ∧ V =V ′ ]

                     [SLS − REC(Node)]                                               [LS − REC(Node)]
    ∆ ∗ [M ] ⊢ ∃V2 . V1 ≤V2 ∧ ∆′ ∗ sls(E2 , V2 , V3 , E3 ) ∗ [F ]              ∆ ∗ [M ] ⊢ ∆′ ∗ ls(E2 , E3 ) ∗ [F ]
    ∆ ∗ E1 7→[E2 , V1 ] ∗ [M ] ⊢ ∆′ ∗ sls(E1 , V1 , V3 , E3 ) ∗ [F ]      ∆ ∗ E1 7→[E2 ] ∗ [M ] ⊢ ∆′ ∗ ls(E1 , E3 ) ∗ [F ]
                   (where E1 7→[E2 , V1 ] 6∈ ∆′ )                                   (where E1 7→[E2 ] 6∈ ∆′ )

                              [R − EX]                          [TREE − REC(Node)]
                      ∆ ∗ [M ] ⊢ ∆′ [V ′ /V ] ∗ [F ]       ∆ ∗ [M ] ⊢ ∆′ ∗ tree(l) ∗ tree(r) ∗ [F ]
                       ∆ ∗ [M ] ⊢ ∃V. ∆′ ∗ [F ]           ∆ ∗ E7→[l, r] ∗ [M ] ⊢ ∆′ ∗ tree(E) ∗ [F ]
                       (where V ′ ∈ F V (∆))                     (where E7→[l, r] 6∈ ∆′ )
                                          [STREE − REC(Node)]
                    ∆ ∗ [M ] ⊢ V1 ≤V2 ∧ V2 ≤V3 ∧ ∆′ ∗ stree(l, V1 , V2 ) ∗ stree(r, V2 , V3 ) ∗ [F ]
                                ∆ ∗ E1 7→[l, r, V2 ] ∗ [M ] ⊢ ∆′ ∗ stree(E1 , V1 , V3 ) ∗ [F ]
                                              (where E1 7→[l, r, V2 ] 6∈ ∆′ )

                    [LS−REC]                                                      [SLS−REC]
        ∆ ∗ [M ] ⊢ ∆′ ∗ ls(E2 , E3 ) ∗ [F ]                 ∆ ∗ [M ] ⊢ ∃V2 . V ′ ≤V2 ∧ ∆′ ∗ sls(E2 , V2 , V3 , E3 ) ∗ [F ]
  ∆ ∗ ls(E1 , E2 ) ∗ [M ] ⊢ ∆′ ∗ ls(E1 , E3 ) ∗ [F ]     ∆ ∗ sls(E1 , V1 , V ′ , E2 ) ∗ [M ] ⊢ ∆′ ∗ sls(E1 , V1 , V3 , E3 ) ∗ [F ]
  (where E3 is dangling & ls(E1 , E2 ) 6∈ ∆′ )               (where E3 is dangling & sls(E1 , V1 , V ′ , E2 ) 6∈ ∆′ )

                                        Figure 4: Subtraction Rules for Bi-Abduction




                                                         [IDENT]
                                          ∆ ∗ [true ∧ emp] ⊢ ∆ ∗ [true ∧ emp]
   Both of these axioms are applied only in a situation where the search can be ended. EMP is applied
whenever the antecedent contains only pure constraints and the consequent is empty, carrying forwards
those pure terms into the frame, preserving those additional constraints for future use. IDENT is applied
only when the antecedent and the consequent are identical, matching and removing all terms, and ending
the search. As both sides are identical in this case, no additional terms are inferred, leaving the frame and
anti-frame unchanged.
   The second group describes rules that seek to reduce the size of the entailment (Definition 2, Section 8) by
subtracting matching sub-formulae from each side, and are presented in Figure 4. Two rules, RIDENT= and
HYPOTHESIS focus on removing pure formulae from the entailment via elimination of trivial and matching
expressions, respectively. While RIDENT= simply removes the trivial term, HYPOTHESIS identifies a sub-

                                                              11
formula of pure terms from the antecedent that implies a sub-formula in the consequent, removing the
sub-formula and maintaining the terms in the antecedent. *-INTRODUCTION operates in a similar manner
to HYPOTHESIS, identifying and separating out spatial terms that entail each other, directly or otherwise.
Unlike HYPOTHESIS, however, *-INTRODUCTION creates a new branch in the proof, aiming to demonstrate
the entailment holds explicitly, and allowing for indirect equivalences as a result. We also include a rule to
concretise existentially-quantified terms in the consequent, R-EX. This rule specifically replaces the existential
variable in the consequent with a free variable selected from the antecedent, with the intent of allowing for
further subtraction of terms.
    The bulk of the remaining rules in this group are specialised unfolding and subtraction rules, targeted
at specific shape predicates. BASE rules identify and eliminate shape predicates that are equivalent to emp,
preserving any additional relations enforced by the definition. Rules REC and REC (Node) aim to identify, un-
fold and subtract any overlapping spatial formulae, preserving any implicit constraints and maintaining any
unaffected fragments, where necessary. REC rules target scenarios with two overlapping spatial predicates,
and REC (Node) rules target a points-to term that overlaps with a specific shape predicate. As an example,
the rule SLS-REC would be applied to scenarios in which an SLS predicate in the antecedent is found to
have the same head pointer as an SLS predicate in the consequent, as in sls(x, i, j, y) ⊢ sls(x, i, k, z). Rules
targeting other data structures would be utilised in the same way.
    The third group consists of the two following rules:

                                            [LS − GENERALIZE]
                                   V ≤V ′ ∧ ∆ ∗ [M ] ⊢ ∆′ ∗ ls(E2 , E3 ) ∗ [F ]
                              ∆ ∗ sls(E1 , V, V ′ , E2 ) ∗ [M ] ⊢ ∆′ ∗ ls(E1 , E3 ) ∗ [F ]
                                        (where sls(E, V, V ′ , E ′ ) 6∈ ∆′ )
                                          [tree − GENERALIZE]
                                          V ≤V ′ ∧ ∆ ∗ [M ] ⊢ ∆′ ∗ [F ]
                                 ∆ ∗ stree(E, V, V ′ ) ∗ [M ] ⊢ ∆′ ∗ tree(E) ∗ [F ]
                                         (where stree(E, V, V ′ ) 6∈ ∆′ )
These two rules inductively generalize ordering constraints in the LHS such that the matching between the
two could be successful. In our system, a sorted linked list indirectly entails a basic singly-linked list between
the same points due to the fact that by our definition, all sorted lists are simple singly-linked lists at the
structural level. This fact could be easily proved by inductively unfolding both predicates and eliminating
the matching nodes. LS-GENERALIZE fires when a sorted list in the antecedent of the entailment shares a head
node with a simple singly-linked list on the consequent, and essentially abstracts the ordering information
away from the sorted list, leaving only the spatial information; a singly-linked list. TREE-GENERALIZE
operates in the same manner.
    The normalisation and subtraction rules of our system are sufficient to prove that a given valid entailment
holds. However, should an entailment be invalid, with either some aspect of the symbolic heap missing or
extra, these rules will not be enough, and our search must continue on to our inference rules.

7. Inference

    When normalisation and subtraction rules are insufficient to continue the proof search, the search aims
to find a applicable rule within our set of inference rules. The rules within this set aim to identify a relevant
fragment of the anti-frame or frame, determined by the current state of the entailment, that will satisfy
some extra or missing term that cannot be resolved by the previous rules. These identified fragments are
introduced into the relevant part of the entailment, and are matched against the existing terms, eliminating
such matches where possible. All of the identified fragments are maintained during the search, with any
fragment of the frame being propagated forwards and the fragments of the anti-frame collected and propa-
gated backwards, producing the final specification. As with the other rule groups, once an appropriate rule
match is found, the search will loop back to the beginning of the rule search; this approach ensures that the
inference rules are applied only when absolutely necessary.
                                                          12
                      [INF−PURE]                                               [INF−7→]
      (Π ∧ emp) ∗ [Π ∧ emp] ⊢ Π ∧ emp ∗ [Π ∧ emp]
                     ′             ′                                 (E0 =E1 ∧ ∆) ∗ [M ] ⊢ ∆′ ∗ [F ]
             (where Π ∧ Π′ is satisfiable.)                   ∆ ∗ E7→E0 ∗ [E0 =E1 ∧ M ] ⊢ ∆′ ∗ E7→E1 ∗ [F ]

                                                   [INF − LS]
                                                                       →
                                                                       −
                                    E 6= E1 ∧ ∆ ∗ ls(X, E1 ) ∗ [M ] ⊢ ∃ Y .∆′
                                                                   →
                                                                   −
                              ∆ ∗ ls(E, E1 ) ∗ [E 6= E1 ∧ M ] ⊢ ∃X Y .∆′ ∗ E7→[X]
                                               [INF − TREE]
                                                                       →
                                                                       −
                                 X 6= null ∧ ∆ ∗ tree(E) ∗ tree(F ) ⊢ ∃ Y ∆′
                                                                 →
                                                                 −
                             ∆ ∗ tree(X) ∗ [X 6= null ∧ M ] ⊢ ∃X Y ∆′ X7→[E, F ]
                                                      [INF − SLS]
                         E1 6= E2 ∧ V1 ≤V ′ ∧ ∆ ∗ sls(X, V ′ , V2 , E2 ) ∗ [M ] ⊢ ∆′ ∗ [F ]
                  ∆ ∗ sls(E1 , V1 , V2 , E2 ) ∗ [E1 6= E2 ∧ V1 ≤V ′ ∧ M ] ⊢ ∆′ ∗ E1 7→[X, V1 ] ∗ [F ]
                                               [INF − STREE]
                                                                                           →
                                                                                           −
                X 6= null ∧ V3 ≤V ∧ V ≤V4 ∧ ∆ ∗ stree(E, V1 , V3 ) ∗ stree(F, V4 , V2 ) ⊢ ∃ Y ∆′
                                                                            →
                                                                            −
               ∆ ∗ stree(X, V1 , V2 ) ∗ [X6=null ∧ V3 ≤V ∧ V ≤V4 ∧ M ] ⊢ ∃X Y ∆′ X7→[E, F, V ]
                   [INF−MISSING]                                                [INF−EXTRA]
      ∆ ∗ [M ] ⊢ ∆′ ∗ [F ]    ∆ ∗ Q(E, E ′ ) 0 false             ∆ ∗ [M ] ⊢ ∆′ ∗ [F ]     ∆′ ∗ Q(E, E ′ ) 0 false
        ∆ ∗ [M ∗ Q(E, E ′ )] ⊢ ∆′ ∗ Q(E, E ′ ) ∗ [F ]              ∆ ∗ Q(E, E ′ ) ∗ [M ] ⊢ ∆′ ∗ [F ∗ Q(E, E ′ )]
                (where Q(E, E ′ ) is op(E))                                (where Q(E, E ′ ) is op(E))

                                       Figure 5: Inference Rules for Combined Domain




    The proof rules for inference are shown in Figure 5. INF-PURE is the final axiom in our core system,
and is applied whenever both sides of the entailment consist of pure terms only. INF-PURE identifies that
all remaining pure terms do not have a direct or indirect match, and moves all remaining pure terms
in the antecedent into the frame, and all remaining pure terms in the consequent into the anti-frame,
ending the search. Important to note is that the side-condition of the rule implies that we will never infer
a trivial pure constraint. INF-7→ infers the unification of constraints over fields such that two points-to
predicates could be matched. This new equality is introduced into the anti-frame and antecedent, and the
now matched predicates are removed. INF-SLS and INF-LS identify overlap between an SLS or LS predicate
in the antecedent and subtract it from the entailment. The rules also infer the constraints required to allow
for this subtraction, adding any inferred terms to the anti-frame and antecedent. In the case of INF-SLS, this
may also include the ordering constraints.
    In order to maintain the validity of the sorted list predicates, both SLS-REC* and INF-SLS take additional
steps to ensure that the order of the sorted list is preserved throughout the application of the rule. In
this case, this means the identification of a suitable ordering constraint between the sorted list and other
spatial predicates. Unlike the inequality between the two end-points, however, this ordering constraint is
not abduced from the application of the rule, as it is implicit inside the sorted list predicate throughout.
Instead, the ordering constraint is simply made explicit by the application of the rule. For the INF-SLS rule,
the ordering constraint is immediately added to the known symbolic state, working under the assumption
that the logical variable X refers to a node with a value field, required for the correctness of the sls predicate
that remains. For SLS-REC*, the ordering constraint becomes an additional constraint in the consequent of
the entailment, requiring proof that the ordering relation is satisfied in order to prove the overall entailment.
The inference of these ordering constraints may be performed through INF-PURE afterwards, if needed. While

                                                            13
this may initially seem to be a useful aspect in ensuring the soundness of the SLS-REC* and SLS-* rules, this
identification of formerly implicit ordering constraints has an additional benefit. In previous works in the
area of combined domain bi-abduction, the handling of complex pure terms, such as ordering, was typically
undertaken in a secondary analysis phase. By completely integrating the pure constraints into the abduction
and entailment rules, we have developed a system in which the complex pure properties are identified during
the shape analysis, eliminating the need for a subsequent pure analysis following this initial phase.
    Finally, INF-MISSING and INF-EXTRA identify the missing symbolic heap of the antecedent and add them to
the anti-frame and frame, respectively. While this is typically necessary, bulk additions to the anti-frame may
result in the identification of overly-complex specifications, should the previous rules not be applied. The
greater precision of the earlier rules is therefore preferred. In these two rules, to avoid inference contradiction,
the satisfiability of the solution is required. The solving of this satisfiability may be implemented through
existing works like [21, 24–27].

8. Soundness and Termination
   We will now present the soundness and termination proof sketches for our system.
Theorem 1 (Soundness). Given an antecedent ∆a and a consequent ∆c , if our system returns “yes” with
an anti-frame M and a frame F , then ∆a ∗ M |= ∆c ∗ F holds.
Proof Sketch : We discuss the soundness of the main proof rules in Section 5, Section 6 and Section 7. Rules
BASE in Figure 3 are essentially unfolding rules (i.e., replace an inductive predicate by its definition) prior to
pruning the recursive case due to the contradiction of equality constraints in the LHS. NODE-EX is based on
the fact that G(op(E)) ∧ op(E) ⇒ E 6= null. NODEs-EX is based on the fact that G(op1 (E1 )) ∧ G(op2 (E2 )) ∧
op1 (E1 )∗op2 (E2 ) ⇒ E1 6= E2 . In Figure 4, rules BASE (reps. REC(NODE)) are essentially unfolding rules prior
to pruning the recursive case (resp. base case). LS-REC is based on the fact that ls(E1 , E2 ) ∗ ls(E2 , E3 ) ⇒
ls(E1 , E3 ). Similarly, SLS-REC is based on the fact that V2 ≤V3 ∧ sls(E1 , V1 , V2 , E2 ) ∗ sls(E2 , V2 , V3 , E3 ) ⇒
sls(E1 , V1 , V3 , E3 ). In Figure 5, INF-LS and INF-SLS infer the pure constraints for recursive case, unfolding
the inductive predicate in the LHS, prune the base case prior to matching and subtracting the points-to
predicates.                                                                                                           
    Termination of our system is based on the size of an entailment which is defined as:
Definition 2 (Size). The size of an entailment Πa ∧ Σa ⊢ Πc ∧ Σc is a triple of:
   1. Np −np where Np is the maximal number of both points-to predicates and inductive predicates that the
      RHS of any entailments derived from the entailment may contain, and np is the total number of both
      points-to predicates and inductive predicates in Σc .
   2. Ne −ne where Ne is the maximal number of both disequalities and non-trivial equalities that the LHS of
      any entailments derived from the entailment may contain, and ne is the number of both disequalities
      and non-trivial equalities in Πa .
   3. the sum of the length of Πa ∧ Σa ⊢ Πc ∧ Σc , where length is defined in the obvious way taking all
      simple formulas to have length 1.
Theorem 2 (Termination). Our system terminates.
Proof Sketch : Np and Ne are bound. Moreover, every rule reduces the size: each rule in Fig. 3 increases
either np or ne ; each rule in Fig. 4 reduces the length (the third component); each rule in Fig. 5 reduces
the length.                                                                                             

9. Implementation
  Our proof technique has been prototyped as an instantiation of a modified version of the Cyclist library3 .
While the library is largely intended to be used to identify Cyclic proofs of programs [11, 28, 29], the

  3 http://www.cyclist-prover.org


                                                          14
underlying representation of separation logic is quite robust and the proof-based approach used in the
library is very similar to our own.
     Our implementation is broadly-speaking a modification of one of the existing instantiations of the Cyclist
library, a separation logic entailment prover, sl prove. While the general usage and structure of our
prototype is very similar to that of the original instantiation, there were two main changes made to the
tool. Firstly, a number of modifications were introduced to enable the retrieval and validation of the frames
and anti-frames produced by the technique. The proof rules themselves were implemented as a replacement
of the rule-set utilised by the original tool. Secondly, a new proof searching algorithm was implemented
as three aforementioned phases: unfolding and normalization, matching and subtracting, and inference. In
addition to these modifications, a number of additions and changes were made to the underlying separation
logic representation. These changes were primarily focussed on the extension of the initial fragment to
include support for ordering constraints, a basic degree of support for numerical values, and a number of
critical supporting functions and behaviours that allows for such support to be effectively utilised.
     Wherever possible, these changes were performed in a manner which had little to no effect on the other
tools in the library, allowing for the other instantiations of the tool to be used without issues. While the
bulk of these changes were made in this way, either preserving older behaviour or replacing code in a way
that preserved the signatures, some changes were to distinct from the original code for this to be effectively
achieved. In these cases, new modules were created, generally similar in design and function, but distinct
due to the enhanced capabilities. As a result, the other existing instantiations of the Cyclist library should
still operate correctly.
     In order to more effectively and efficiently support an automated implementation, a small number of
conditions were applied to the implementation of the rules. First, a number of restrictions on rule applications
were introduced in order to prevent irrelevant or unhelpful applications. As an example, the existential
renaming rule R-EX can only be applied in the implementation if the identified renaming directly enables the
use of a subsequent subtraction rule, preventing spurious renaming of existential variables. Secondly, both
HYPOTHESIS and *-INTRO rules were reduced in scope to elimination of singular matching formulas. While
an unrestricted version was implemented and tested, the impact on the efficiency of the implementation was
significant, slowing many analyses down to near-unusable speeds, and in some cases exhausting all available
memory. The restricted variant currently used in our implementation avoids these issues, and while less
comprehensive, does not seem to have an impact on the results. Finally, EXCLUDE-MIDDLE was restricted
to only splitting on cases using the spatial terms within given predicate, limiting the branching only to
specific empty or non-empty cases. This restriction in particular was due to the significant performance
cost of permitting any and all case-splits to be made via EXCLUDE-MIDDLE. These restrictions help to gain
a significant improvement in efficiency over an unrestricted implementation.
     In addition to the restrictions on specific rules, a number of additional rules were implemented in order
to support the implementation. One such example is the SLS-INV rule, which makes explicit the ordering
invariant of a guarded sls predicate in order to preserve that information though subtraction operations, and
a restricted renaming rule SLS-PARAM-EQ, which identifies and equates non-spatial parameters in matching
predicates. Corresponding rules for trees are also present.
     Overall, the prototype does have a number of limitations at present, such as the very general treatment of
numerical values and a brittle approach to the implementation of rules that target specific predicates. These
issues, intended to be resolved in future refinements, do carry a slight negative impact on the effectiveness,
stability and general extensibility of the tool, though they do not impact the underlying technique. Despite
these issues, the initial results indicate that our approach shows promise in the area of combined domain
bi-abductive inference. These results are presented and discussed below.

10. Evaluation
  In order to experimentally evaluate our technique, we applied our prototype tool to a selection of bench-
marks utilised in the 2019 SL-COMP competition4 [12]. Specifically, we performed our evaluation over the

  4 Benchmarks were downloaded from competition GitHub during November 2019 [30].


                                                       15
benchmarks included in the SL-COMP divisions qf shls entl, containing entailments restricted to basic
singly-linked lists without quantifiers, and a subset of the benchmarks included in the qf shidlia entl
division, specifically those that targeted sorted list segments, also without quantifiers. The benchmarks
selected from these divisions are all the benchmarks that operate within the symbolic heap fragment cur-
rently supported by our technique, and allow us to examine the capabilities of our implementation against
a strong, standardised set of benchmarks.
    An important point is that while these examples are not strictly designed for use in the evaluation of
bi-abductive techniques, there is still a significant overlap: our tool, when applied over the invalid examples
of the set, should produce a frame and anti-frame that, if introduced, would make the example valid. As
a result, the main focus of our analysis is the invalid benchmarks, though the valid examples will still be
examined for the purposes of execution times and efficiency.
    In total, we ran our implementation over 313 example entail-
ments: all 296 basic list examples from qf shls entl (174 valid                Category Valid Invalid
and 122 invalid) and 17 sorted list examples from qf shidlia entl,                      qf shls entl
modified to use our definition of sorted lists. A more detailed break-         smallfoot       23          54
down of the number of entailments from each source can be seen                   clones        40          60
in Table 1. These benchmarks are each represented in their own                 bolognesa       57          53
dedicated file, with the entailment problem itself defined using a                  ls          6           3
variation of the SMT-LIB format, extended with support for spa-
                                                                                      qf shidlia entl
tial terms [31]. These files are arranged within relevant division di-
                                                                                sls join       17           0
rectories, alongside an auxiliary information file which summarises
properties of the corresponding example, such as the source and the          Table 1: Breakdown of list benchmarks
validity. For our experimentation, a batch file was created to pass
the filepath of each relevant example to the implementation front
end (with expected flags), which parses the SMT-LIB file and invokes the main solving process, forwarding
the cumulative output to a benchmark file.
    For each valid entailment in the set of benchmarks, our implementation identifies either an empty frame
and anti-frame or a trivial one, where the final impact of the inferred fragments is essentially negligible. For
invalid entailments, our implementation either identifies a suitable frame and anti-frame, ensuring that the
refined entailment is valid, or determines that there is is no possible solution for that particular benchmark.
    The benchmarking was performed on an Ubuntu 18.04 virtual machine with 8GB of memory, running
on an Intel i7-7700 processor. A 30s limit on execution time was enforced throughout these experiments.
    The benchmarks will be presented in three parts: first, we will present and discuss the results of applying
the implementation over examples featuring basic singly-linked lists with no ordering constraints. Subse-
quently, we will discuss the results of the sorted list benchmarks, and finally conclude with the results of
applying our technique to examples utilising trees, both simple binary trees as well as binary search trees.

10.1. Simple Singly-Linked List Benchmarks
   The majority of the examples included in the benchmarks were entailments focussed around the ma-
nipulation of simple singly-linked lists, likely due to the number and maturity of tools in this specific area.
As a result of the volume of benchmarks examined, the analysis of these results will be somewhat general,
though a small number of specific results from each category will be presented. Additional focus is placed
on the Smallfoot benchmarks due to the similarities between that tool and our own.

10.1.1. Smallfoot
    Our implementation proved to be highly effective over the Smallfoot benchmarks, typically identifying
and evaluating all found solutions in only a few ms of CPU time. Our technique was able to solve the vast
majority of the examples within this set, either confirming the validity of the entailment or identifying some
suitable frame or anti-frame to correct it. The execution times and validation percentages of a subset of the
benchmarks of this set can be seen in Table A.6.
    Many of the benchmarks in the Smallfoot set are essentially equivalences, in which the antecedent and
consequent are two descriptions of a symbolic heap. As a result, the majority of the work undertaken by the
                                                       16
                            Benchmark:                                 % of time
                                             Valid     Time (ms)
                             Smallfoot                                 validating
                               vc09            Y           5               53
                               vc21            Y           <1              29
                               vc28            Y           2               61
                               vc29            N           2               45
                               vc33            N           5               54
                               vc37            N           2                -
                               vc40            N           3               48
                               vc65            Y           2               61
                               vc70            N           9               61

                                   Table 2: Benchmarks for Smallfoot Example



tool is to show those equivalences through match-and-subtract operations, unfolding and eliminating shape
predicates from the entailment where possible. Other examples featured aliased pointer fields, requiring the
inference of an equality enforcing that alias for the entailment to be satisfied. Of note in this category is
the smallfoot-vc37 benchmark. In this example, the alias is over the pointer itself; resolving aliases such
as this is currently beyond the capacity of our implementation, and thus no solution was found for this
particular bi-abductive problem.
    Another important aspect to note is that several of the examples within this set were made trivial from
simplifications applied during the initial reading of the problem from file. Due to the chosen representation
of equalities in the Cyclist SL library, trivial equalities are naturally filtered out without any input. As a
result, a small number of the benchmarks featured either antecedents or consequents that were reduced to
emp immediately, vastly simplifying the entailment as a whole. In this case, the entailment to be solved
appears in the simplified form, such as emp ⊢ emp; while equivalent to the original input, the simplifications
applied to reach this point are not detailed in the proof, though the equivalence itself is apparent.
    However, the most relevant examples in this set are those that require bi-abduction in order to be
effectively resolved. A number of the benchmarks of the Smallfoot set feature entailments with aspects of the
symbolic heap that are missing or extra within that entailment. In these cases, our technique must identify
those fragments, and infer that they form part of the frame or anti-frame. Our technique is remarkably
effective in these cases, readily identifying fragments of the entailment that are missing or extra in the
example, and moving them to the frame or anti-frame as appropriate. There are fewer examples in which a
spatial fragment is inferred into the anti-frame than into the frame, but these benchmarks are resolved with
equal ease. A number of benchmarks and their inferred specifications can be seen in Table A.6.

10.1.2. LS
    Alongside the larger groups of entailments, there are also a small number of list-targeting examples
sourced from [32], listed under the group ls. This group of entailments features a number of list segments and
connecting points-to terms in the antecedent, and requires that the implementation identify the equivalence
of those fragments with a single, unified list over the same points defined in the consequent. In order to
resolve these entailments, the prototype must identify each overlapping fragment of the heap and subtract
it from entailment.
    Over these examples, our implementation excels, proving each of the 3 valid entailments in less than 5ms
CPU time each. Indeed, even over the initially invalid examples, our prototype is able to identify suitable
frames and anti-frames and complete the proof in typically under 10ms.

10.1.3. Clones
    We have also evaluated our implementation’s performance over the set of Clones benchmarks. This set
of examples feature entailments that include a number of unidentified aliases. In each of these cases, in


                                                      17
 Benchmark:                               % of time           Benchmark:                                % of time
                  Valid    Time (s)                                             Valid        Time (s)
   clones                                 validating           bolognesa                                validating
   03 e07           N        0.119            59                 10 e01           N           0.385         77
   03 e08           N        0.118        No solution            10 e03           Y           0.744         77
   03 e09           N        0.172            64                 10 e04           N           0.740         77
   03 e10           N        0.123            60                 10 e09           N           0.434         77
   04 e07           N        0.619            63                 12 e01           Y           1.052         81
   04 e08           N        0.636        No solution            12 e03           N           20.425        80
   04 e09           N        0.916            69                 12 e04           N           1.742         80
   04 e10           N         0.62            64                 12 e09           Y           10.458        79
   05 e07           N        2.897            67                 14 e01           Y            7.02         84
   05 e08           N         2.97        No solution            14 e03           Y           12.713        83
   05 e09           N        4.258            73                 14 e04           Y            2.4          82
   05 e10           N         2.88            67                 14 e09           Y           12.163        83
   06 e07           N        12.198           71                 16 e01           Y           13.797        86
   06 e08           N        12.382       No solution            16 e03           N           14.325        86
   06 e09           N        18.013           76                 16 e04           N           15.155        85
   06 e10           N        12.270           71                 16 e09           Y           26.303        85
                (a) Clones Benchmarks                                      (b) Bolognesa Benchmarks

                           Table 3: Selection of Benchmarks for Simple Singly-Linked Lists



order to satisfy the entailment, these aliases must be identified, and an equality representing this alias must
be introduced into the anti-frame or frame as needed.
    The benchmarks are arranged into 10 groups of similar problems, with each group featuring a different
number of terms. For the benchmarks in the earliest groups, there are only a small number of terms to
be processed, increasing as the benchmarks proceed. In each of these groups, examples 01 through 06 are
relatively trivial problems featuring empty sides of the entailment or simple equivalences, and are solved
either by simplification during the initial construction of the entailment from the benchmark file, or by early
applications of one of our axioms. The remaining examples in each group are more complex, and are thus
the only ones discussed in detail here; a selection of these benchmarks can be found in Table 3a.
    The examples within the earlier groups are solved handily by our implementation, with all examples in
groups clones-01 through clones-04 solved in less than one second of CPU time, including validation of
results. However, beyond this point the size of the entailments begin to have an increasingly large impact
on the time required to complete, with clones-05 taking over a second for many of the examples, and
dramatically increasing from there. Indeed, examples in clones-06 takes over 10 seconds to complete, and
the implementation begins to time out from clones-07 onwards.
    In each group, our implementation was able to solve and identify suitable aliases for each instance of e7,
e9 and e10 (timeouts notwithstanding). In most instances, this process was undertaken via the application
of the INF-PTO rule, identifying an alias implied by the shared root of points-to terms in the antecedent and
consequent, and applying it to the entailment as a whole. This in turn allows for the remainder of the proof
to be resolved as standard, matching and subtracting equivalent fragments. This process was accomplished
reasonably efficiently, though the impact of larger entailments on the overall performance is quite noticeable.
    Example e8 within each group is a special case. Each instance of e8 within the clones benchmarks
outlines an invalid entailment, in which the alias eventually produces a conflict between parts of the en-
tailment. While our implementation does detect this inconsistency, it does not achieve this until candidate
specifications are validated, which unfortunately results in only a minimal reduction in execution time. It
may be possible to accelerate this detection in future works, but is uninvestigated at this time.
    When looking at the breakdown in execution times, it seems that the bulk of the analysis time is spent
on the validation of the produced results, becoming increasingly costly as the number of terms and potential

                                                         18
solutions increases. Indeed, this aspect seems to be common throughout the examples tested here, and while
entailments with a small number of terms are solved almost instantly, larger entailments take dramatically
more time to complete.

10.1.4. Bolognesa
    The Bolognesa examples consist primarily of a large number of interlinking spatial fragments. In order
to prove these examples, our technique must identify equivalent fragments of the entailment, often formed
of a mix of points-to entailments and list predicates, and eliminate them, with any remaining fragments
inferred as a part of the frame or anti-frame. A selection of example benchmarks can be found in Table 3b.
    The Bolognesa examples were arranged into 20 groups of 10 examples, with each group increasing in
the number of terms and expressions included within the entailment. Much like the Clones examples, our
implementation was able to rapidly solve the majority of the smaller examples in very short periods of
time; the majority of these earlier problems were solved within only a few seconds of CPU time, validation
included. However, as in the other examples, as the number of terms increased, the overall execution times
increased dramatically. While a small number of exceptions were present within the benchmarks, the larger
entailments took significantly more time to complete as the number of terms increased, eventually beginning
to timeout regularly in the largest examples. A few exceptions to this were present, but as in clones, a
significant number of the timeouts occurred within the validation stage, with the underlying proof already
constructed. Indeed, of the 54 timeouts throughout the entire benchmark set, only 20 were due to a timeout
in the construction of the proof, with the remaining 34 taking place during the validation.
    With that said, when the implementation did complete, the results showed promise: for the majority of
the invalid examples, our implementation produced a range of potential solutions for the frame and anti-
frame, typically within a reasonable time.

    Overall, our approach is reasonably efficient and effective over the basic list examples detailed here.
Despite some issues regarding the scalability of the proof search over large entailments, the search overall
was effective, accurate, and fast in the majority of cases, producing useful and accurate specifications. In
fact, it seems that the largest factor in the execution time is the verification of the potential results. Indeed,
throughout the benchmarks, it is apparent that the majority of the execution time for a given entailment
is spent upon the validation of the results, not the construction of the underlying proof. While this is
clearly not ideal, the speed at which our technique is able to explore and identify all possible solutions
for a given entailment does indicate that our approach is effective, and that a more efficient validation
mechanism, possibly taking advantage of SMT-based solutions, may help overcome many of these issues;
this in particular is a focus for future works.

10.2. Sorted List Benchmarks
     The sls benchmarks utilised in this section were taken from the qf shidlia entl division of SL-COMP.
Unfortunately, there are only a small number of such examples within the SL-COMP benchmarks, and so
while the results here are a reasonable indicator of the effectiveness of the implementation, they likely do
not fully represent the capabilities of our technique.
     Regarding the examples themselves, each of the benchmarks examined in this section are valid entail-
ments, each aiming to demonstrate that several indirectly linked sorted lists entail a single combined sorted
list over the same range. The primary difference between each example is the amount of explicit information
regarding the values of each segment. For some of these examples, the exact bounds are known, making the
ordering between each segment trivial. However, for the majority of the examples, only a selection of the
bounds are known, requiring the identification of ordering constraints that will enforce the order between
the segments. In order to successfully solve these examples, our technique must be able to identify those
ordering constraints, and then identify that the multiple linked segments are equivalent to a single sorted
list segment between the same two points. The results for this section are detailed in Table 4.
     In summary, our technique was able to solve the sorted list examples in very short periods of time, with the
longest execution time only just exceeding half a second. For each of the cases, implicit or missing ordering

                                                       19
                              Benchmark                      Time (ms)        % Validation
                         sls join 2 known bnd                    16               47
                          sls join 2 no cond                     20               62
                               sls join 2                        20               63
                       sls join 2 unk lower bnd                  18               55
                       sls join 2 unk upper bnd                  17               56
                           sls join 3 2 cond                    119               67
                          sls join 3 no cond                     50               35
                               sls join 3                       120               67
                       sls join 3 unk lower bnd                 116               67
                       sls join 3 unk upper bnd                  71               51
                      sls join 4 1 cond unk both                298               51
                    sls join 4 1 cond unk lower bnd             217               36
                    sls join 4 1 cond unk upper bnd              78               35
                    sls join 4 2 cond unk lower bnd             339               54
                    sls join 4 2 cond unk upper bnd             445               66
                           sls join 4 3 cond                    570               70
                          sls join 4 no cond                    202               32

                                  Table 4: Benchmarks for Sorted List Entailments



constraints were identified, and as in the simple linked-list examples, each valid state of the shape predicates
are explored separately, often producing a range of valid specifications upon completion. Curiously, the
performance of the tool seems to be better over examples with fewer known boundaries, suggesting that
the more general symbolic ordering constraints are simpler to identify with our technique than ordering
constraints with known values. More investigation into this phenomenon may be undertaken at a later date.
    There are some minor issues, however. Of particular note is the presence of the trivial numerical terms
within the final outputs. Terms such as 100≤ 200 are obviously true, but appear within the final output as a
side-effect of our simplistic treatment of numerical terms. While modifying the implementation to eliminate
such terms would not be overly complex, their presence does not cause a significant negative effect, and so
has been ignored for now.
    While these examples are relatively simplistic, the ease with with our technique was able to identify the
requisite ordering constraints, either explicit or implicit, does show great promise. Though not undertaken
in this work, extending the combined-domain benchmark set to include more complex examples, including
larger numbers of terms and mixing in more standard spatial terms, such as points-to terms and simple
list predicates will give a much greater insight into the effectiveness of our technique. Additionally, a far
wider range of combined-domain benchmarks were included within the SL-COMP set, though most of them
targeted data structures or properties that are not currently supported within our technique. By extending
the fragment supported by our tool, these benchmarks may be added into our evaluation, further testing
the effectiveness of our technique. Such enhancements will be left for future works.

10.3. Binary Trees
    Unlike the other experiments performed in this evaluation, the examples used for exploring the effec-
tiveness of our technique over trees were created by-hand due to difficulties in identifying relevant examples
supported by the tool’s current implementation. These benchmarks were created in the spirit of the Small-
foot benchmarks, aiming to evaluate the implementations performance and capabilities over a range of fairly
“primitive” entailments. These entailments and their corresponding results can be seen in Table 5.
    For the majority of the examples tested here, it can be seen that the performance of the tool over the
tree-based examples is comparable in many ways to the performance over the SL-COMP examples. Over
these entailments, the tool was able to create a proof tree identifying a number of possible solutions in
very short time, typically under 100ms. However, as in the previous examples, the amount of time spent
                                                        20
       No.                             Entailment                               Time (ms)   % Validation
        1                           x7→[l, r] ⊢ tree(x)                             2           83
        2                x7→[l, r] ∗ tree(l) ∗ tree(r) ⊢ tree(x)                    9           62
        3                tree(x) ⊢ x7→[l, r] ∗ tree(l) ∗ tree(r)                    7           66
        4                      tree(x) ⊢ tree(x) ∗ tree(y)                          3           70
        5              x7→[l, r] ∗ l7→[m, n] ∗ r7→[s, t] ⊢ tree(x)                  70          98
        6               tree(x) ∗ tree(y) ⊢ x7→[i, j] ∗ y7→[k, l]                   62          76
        7                        x7→[l, r, i] ⊢ stree(x, i, j)                      7           88
        8     x7→[l, r, i] ∗ stree(l, a, h) ∗ stree(r, j, k) ⊢ stree(x, a, k)       18          56
        9     stree(x, a, k) ⊢ x7→[l, r, i] ∗ stree(l, a, h) ∗ stree(r, j, k)       16          63
       10            stree(x, a, b) ⊢ stree(x, c, d) ∗ stree(y, i, j)               4           63
       11       x7→[l, r, i] ∗ l7→[m, n, a] ∗ r7→[s, t, k] ⊢ stree(x, a, k)        196          97
       12      stree(x, i, j) ∗ stree(y, k, l) ⊢ x7→[a, b, i] ∗ y7→[c, d, k]       114          74
       13                         stree(x, i, j) ⊢ tree(x)                          2           57
       14           stree(x, i, k) ⊢ x7→[l, r, i] ∗ tree(l) ∗ tree(r)               14          69

                                       Table 5: Benchmarks for Tree Entailments



validating these examples is significantly larger than the initial identification. In particular, entailment 5
spent almost the entirety of its execution time validating the potential solutions, likely due to the inferred
anti-frame including a number of additional predicates.
    With that said, the performance over the stree entailments does continue to indicate that the core system
is very promising. The construction of the initial proof tree, including the inference of frames and anti-frames,
continues to take only a short time over these simpler entailments, and while the verification continues to
be a source of extreme inefficiency, the overall CPU time required remains quite brief. Additionally, due to
the similarities between the entailments using tree and stree predicates, it can be seen that the inclusion
of ordering constraints does not seem to introduce a large cost to performance. As in the sls examples
previously, the technique reliably identified the omitted ordering constraints necessary for the entailments
to hold, as well as identifying any spatial fragments of the frames and anti-frames, with the overall execution
time increasing by only a few ms.
    In addition to the more standard entailments, we have also included 2 special cases, aiming to examine
the performance of the tool when GENERALIZE rules are required to solve the bi-abductive problem. In each
example, the antecedent features a binary search tree, whereas the consequent describes only simple binary
trees. In order to resolve these examples, the technique must identify the relationship between the two
predicates and generalize the stree predicate to a simple tree, before continuing on to complete the proof.
As can be seen in the experimental results, the need to apply one of these rules does not have a significant
effect on the overall execution time when compared to similar entailments.

11. Conclusions and Future Work

    We have presented a novel proof system for the bi-abduction problem in separation logic for sorted
lists and binary search trees. Our system has been designed based on the Unfold-and-Match paradigm:
given an entailment, it systematically explores all candidate matching instances of the antecedent and
consequent prior to inferring any missing portion. In order to inspect the effectiveness of the system, we
have implemented the technique into a prototype tool based upon the Cyclist library [11] and tested it over
a range of benchmarks from the SL-COMP competition. While in an early stage, the system does show
promise, and further work to improve the system will likely improve it further.
    Possible future works include extending the base system to a more expressive fragment, such as the
inclusions of more general inductive definitions and additional pure properties such as size, balance and bag
or set information. Our current system is based on the decidable fragment presented in [33], and extending
it to a more expressive decidable fragment such as [34, 35] is also of interest. Other possible avenues include
                                                           21
using the system to infer error specifications via bi-abduction [36] for use in counterexample generation
[37, 38] and program repair [25]. In addition, our system may be embedded inside a program analysis tool
e.g. [6, 8, 29], allowing our system to be used for full program analysis and specification inference.

References
 [1] C. Curry, Q. L. Le, S. Qin, Bi-abductive inference for shape and ordering properties, in: 2019 24th International Conference
     on Engineering of Complex Computer Systems (ICECCS), IEEE, 2019, pp. 220–225.
 [2] H. Yang, O. Lee, J. Berdine, C. Calcagno, B. Cook, D. Distefano, P. O’Hearn, Scalable shape analysis for systems code,
     in: CAV, Springer, 2008, pp. 385–398.
 [3] L. Szekeres, M. Payer, T. Wei, D. Song, Sok: Eternal war in memory, in: 2013 IEEE Symposium on Security and Privacy,
     2013, pp. 48–62. doi:10.1109/SP.2013.13.
 [4] J. C. Reynolds, Separation logic: A logic for shared mutable data structures, in: Proceedings of the 17th Annual IEEE
     Symposium on Logic in Computer Science, IEEE, 2002, pp. 55–74.
 [5] S. S. Ishtiaq, P. W. O’Hearn, BI as an assertion language for mutable data structures, ACM SIGPLAN Notices 36 (2001)
     14–26.
 [6] C. Calcagno, D. Distefano, P. O’Hearn, H. Yang, Compositional shape analysis by means of bi-abduction, in: Proceedings
     of the 36th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, ACM, 2009, pp.
     289–300. doi:10.1145/1480881.1480917.
 [7] C. Calcagno, D. Distefano, Infer: An automatic program verifier for memory safety of c programs, in: NASA Formal
     Methods Symposium, Springer, 2011, pp. 459–465.
 [8] Q. L. Le, C. Gherghina, S. Qin, W.-N. Chin, Shape analysis via second-order bi-abduction, in: A. Biere, R. Bloem (Eds.),
     Computer Aided Verification, Springer International Publishing, Cham, 2014, pp. 52–68.
 [9] M.-T. Trinh, Q. L. Le, C. David, W.-N. Chin, Bi-abduction with pure properties for specification inference, in: Asian
     Symposium on Programming Languages and Systems, 2013, pp. 107–123.
[10] S. Magill, M.-H. Tsai, P. Lee, Y.-K. Tsay, Automatic numeric abstractions for heap-manipulating programs, in: Pro-
     ceedings of the 37th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL ’10,
     ACM, 2010, pp. 211–222. doi:10.1145/1706299.1706326 .
[11] J. Brotherston, N. Gorogiannis, R. L. Petersen, A generic cyclic theorem prover, in: Asian Symposium on Programming
     Languages and Systems, Springer, 2012, pp. 350–367.
[12] M. Sighireanu, J. A. N. Pérez, A. Rybalchenko, N. Gorogiannis, R. Iosif, A. Reynolds, C. Serban, J. Katelaan, C. Matheja,
     T. Noll, et al., Sl-comp: Competition of solvers for separation logic, in: International Conference of Tools and Algorithms
     for the Construction and Analysis of Systems, 2019, pp. 116–132. doi:10.1007/978-3-030-17502-3\textunderscore8 .
[13] J. Fragoso Santos, P. Maksimović, G. Sampaio, P. Gardner, JaVerT 2.0: Compositional symbolic execution for javascript,
     Proceedings of the ACM on Programming Languages 3 (2019). doi:10.1145/3290379.
[14] J. Fragoso Santos, P. Maksimović, S.-E. Ayoun, P. Gardner, Gillian: Compositional symbolic execution for all, 2020.
     Preprint, available at arXiv: https://arxiv.org/abs/2001.05059.
[15] Q. L. Le, J. Sun, S. Qin, Frame inference for inductive entailment proofs in separation logic, in: D. Beyer, M. Huisman
     (Eds.), Tools and Algorithms for the Construction and Analysis of Systems, Springer International Publishing, Cham,
     2018, pp. 41–60.
[16] S. Qin, G. He, W.-N. Chin, F. Craciun, M. He, Z. Ming, Automated specification inference in a combined domain via
     user-defined predicates, Science of Computer Programming (2017) 189–212.
[17] B.-Y. Chang, X. Rival, Relational inductive shape analysis, in: Proceedings of the 35th Annual ACM SIGPLAN-SIGACT
     Symposium on Principles of Programming Languages, ACM, 2008, pp. 247–260. doi:10.1145/1328438.1328469 .
[18] M. Sagiv, T. Reps, R. Wilhelm, Parametric shape analysis via 3-valued logic, ACM Transactions on Programming
     Languages and Systems 24 (2002) 217–298. doi:10.1145/514188.514190.
[19] L. Holı́k, M. Hruška, O. Lengál, A. Rogalewicz, J. Šimáček, T. Vojnar, Forester: Shape analysis using tree automata, in:
     C. Baier, C. Tinelli (Eds.), TACAS, Springer Berlin Heidelberg, 2015, pp. 432–435.
[20] P. A. Abdulla, L. Holı́k, B. Jonsson, O. Lengál, C. Q. Trinh, T. Vojnar, Verification of heap manipulating prorams with
     ordered data by extended forest automata, in: ATVA 2013, October 15-18, Hanoi, Vietnam, Springer Berlin/Heidelberg,
     2013, pp. 224–239.
[21] Q. L. Le, M. Tatsuta, J. Sun, W.-N. Chin, A decidable fragment in separation logic withinductive predicates and arithmetic,
     in: R. Majumdar, V. Kunčak (Eds.), Computer Aided Verification, Springer International Publishing, Cham, 2017, pp.
     495–517.
[22] C. S. Peirce, Collected Papers of Charles Sanders Peirce, Harvard University Press, 1965.
[23] L. de Moura, N. Bjørner, Z3: An efficient smt solver, in: C. R. Ramakrishnan, J. Rehof (Eds.), Tools and Algorithms for
     the Construction and Analysis of Systems, Springer Berlin Heidelberg, Berlin Heidelberg, 2008, pp. 337–340.
[24] Q. L. Le, J. Sun, W.-N. Chin, Satisfiability modulo heap-based programs, in: S. Chaudhuri, A. Farzan (Eds.), Computer
     Aided Verification, Springer International Publishing, Cham, 2016, pp. 382–404.
[25] L. D. X. Bach, Q. L. Le, D. Lo, C. L. Goues, Enhancing automated program repair with deductive verification, in: 2016
     IEEE International Conference on Software Maintenance and Evolution, 2016, pp. 428–432. doi:10.1109/ICSME.2016.66.
[26] X. Gu, T. Chen, Z. Wu, A complete decision procedure for linearly compositional separation logic with data constraints,
     in: N. Olivetti, A. Tiwari (Eds.), Automated Reasoning, Springer International Publishing, Cham, 2016, pp. 532–549.


                                                               22
[27] Z. Xu, T. Chen, Z. Wu, Satisfiability of compositional separation logic with tree predicates and data constraints, in:
     L. de Moura (Ed.), Automated Deduction – CADE 26, Springer International Publishing, Cham, 2017, pp. 509–527.
[28] J. Brotherston, R. Bornat, C. Calcagno, Cyclic proofs of program termination in separation logic, in: Proceedings of the
     35th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL ’08, ACM, New York,
     NY, USA, 2008, pp. 101–112. URL: http://doi.acm.org/10.1145/1328438.1328453 . doi:10.1145/1328438.1328453.
[29] J. Brotherston, N. Gorogiannis, Cyclic abduction of inductively defined safety and termination preconditions, in:
     M. Muller-Olm, H. Seidl (Eds.), Static Analysis, volume 8723 of SAS 2014, Springer International Publishing, Cham,
     2014, pp. 68–84.
[30] M. Sighireanu,         N. Gorogiannis,       R. Iosif,  SL-COMP 2019,           https://sl-comp.github.io/,  2019. URL:
     https://sl-comp.github.io/, [Online; accessed 01-Jul-2019].
[31] R. Iosif, C. Serban, A. Reynolds, M. Sighireanu, Encoding separation logic in SMT-LIB v2.5, 2018. URL:
     https://sl-comp.github.io/docs/smtlib-sl.pdf .
[32] C. Enea, O. Lengál, M. Sighireanu, T. Vojnar, Compositional entailment checking for a fragment of separation logic,
     Formal Methods in System Design 51 (2017) 575–607.
[33] J. Berdine, C. Calcagno, P. W. Ohearn, Symbolic execution with separation logic, in: Asian Symposium on Programming
     Languages and Systems, Springer, 2005, pp. 52–68.
[34] C. Enea, O. Lengál, M. Sighireanu, T. Vojnar, Compositional entailment checking for a fragment of separation logic, in:
     J. Garrigue (Ed.), Programming Languages and Systems, Springer International Publishing, Cham, 2014, pp. 314–333.
[35] C. Enea, O. Lengál, M. Sighireanu, T. Vojnar, Compositional entailment checking for a fragment of separation logic,
     Form. Methods Syst. Des. 51 (2017) 575607.
[36] Q. L. Le, A. Sharma, F. Craciun, W.-N. Chin, Towards complete specifications with an error calculus, in: G. Brat,
     N. Rungta, A. Venet (Eds.), NASA Formal Methods, Springer Berlin Heidelberg, Berlin, Heidelberg, 2013, pp. 291–306.
[37] L. H. Pham, Q. L. Le, Q.-S. Phan, J. Sun, Concolic testing heap-manipulating programs, in: Formal Methods – The Next
     30 Years, Springer International Publishing, Cham, 2019, pp. 442–461.
[38] L. H. Pham, Q. L. Le, Q.-S. Phan, J. Sun, S. Qin, Enhancing symbolic execution of heap-based programs with separa-
     tion logic for test input generation, in: Automated Technology for Verification and Analysis (ATVA), Springer International
     Publishing, Cham, 2019, pp. 209–227.




                                                              23
Appendix A. Example Inferred Specifications

   Name                                                                   Specifications
                                  ls(x1, null) ∗ ls(x2, null) ∗ [] ⊢ ∗ls(x1, null) ∗ ls(x2, null) ∗ [x16=null ∗ x26=null ∗ x16=2]
                                ls(x1, null) ∗ ls(x2, null) ∗ [x1 = null] ⊢ ∗ls(x1, null) ∗ ls(x2, null) ∗ [x1 = null ∗ x26=null]
    vc09
                                ls(x1, null) ∗ ls(x2, null) ∗ [x2 = null] ⊢ ∗ls(x1, null) ∗ ls(x2, null) ∗ [x2 = null ∗ x16=null]
                         ls(x1, null) ∗ ls(x2, null) ∗ [x1 = null ∗ x2 = null] ⊢ ∗ls(x1, null) ∗ ls(x2, null) ∗ [x1 = null ∗ x2 = null]
    vc21                                        x16=null ∗ ls(x1, null) ∗ [true ∧ emp] ⊢ ls(x1, null) ∗ [x16=null]
                          x16=null ∗ x26=null ∗ x27→null ∗ ls(x1, x2) ∗ [true ∧ emp] ⊢ ls(x1, null) ∗ [x16=null ∗ x26=null ∗ x16=x2]
    vc28
                           x16=null ∗ x26=null ∗ x27→null ∗ ls(x1, x2) ∗ [x1 = x2] ⊢ ls(x1, null) ∗ [x1 = x2 ∗ x16=null ∗ x26=null]
                                     Π ∗ x27→x1 ∗ ls(x1, x2) ∗ [x1 = x3] ⊢ x27→x3 ∗ ls(x3, x2) ∗ [Π ∗ x1 = x3 ∗ x26=x3]
    vc29
                               Π ∗ x27→x1 ∗ ls(x1, x2) ∗ [x1 = x3 ∗ x2 = x3] ⊢ x27→x3 ∗ ls(x3, x2) ∗ [x1 = x3 ∗ x2 = x3 ∗ Π]
                            Π ∗ x17→x2 ∗ x37→x1 ∗ ls(x2, x3) ∗ [x1 = x4] ⊢ x36=x4 ∗ x37→x4 ∗ ls(x4, x3) ∗ [Π ∗ x1 = x4 ∗ x26=x3]
    vc33
                      Π ∗ x17→x2 ∗ x37→x1 ∗ ls(x2, x3) ∗ [x1 = x4 ∗ x2 = x3] ⊢ x36=x4 ∗ x37→x4 ∗ ls(x4, x3) ∗ [Π ∗ x1 = x4 ∗ x2 = x3]




                                                                                                                                                               24
    vc37                                                                      INVALID
                               Π ∗ x27→x3 ∗ ls(1, null) ∗ ls(x3, null) ∗ [] ⊢ ls(x1, null) ∗ ls(x3, null) ∗ [Π ∗ x36=null ∗ x27→x3]
    vc40
                         Π ∗ x27→x3 ∗ ls(1, null) ∗ ls(x3, null) ∗ [x3 = null] ⊢ ls(x1, null) ∗ ls(x3, null) ∗ [Π ∗ x3 = null ∗ x27→x3]
                                            Π ∗ x17→x2 ∗ ls(x2, null) ∗ [true ∧ emp] ⊢ ls(x1, null) ∗ [Π ∗ x26=null]
    vc65
                                            Π ∗ x17→x2 ∗ ls(x2, null) ∗ [x2 = null] ⊢ ls(x1, null) ∗ [Π ∗ x2 = null]
              Π ∗ x17→x2 ∗ ls(x2, null) ∗ ls(x3, null) ∗ [] ⊢ x17→x2 ∗ ls(x2, null) ∗ ls(x1, x1) ∗ [Π ∗ x26=null ∗ x36=null ∗ x26=x3 ∗ ls(x3, null)]
                    Π ∗ x17→x2 ∗ ls(x2, null) ∗ ls(x3, null) ∗ [x3 = null] ⊢ x17→x2 ∗ ls(x2, null) ∗ ls(x1, x1) ∗ [Π ∗ x26=null ∗ x3 = null]
    vc70
             Π ∗ x17→x2 ∗ ls(x2, null) ∗ ls(x3, null) ∗ [x2 = null] ⊢ x17→x2 ∗ ls(x2, null) ∗ ls(x1, x1) ∗ [Π ∗ x2 = null ∗ x36=null ∗ ls(x3, null)]
             Π ∗ x17→x2 ∗ ls(x2, null) ∗ ls(x3, null) ∗ [x2 = null ∗ x3 = null] ⊢ x17→x2 ∗ ls(x2, null) ∗ ls(x1, x1) ∗ [Π ∗ x2 = null ∗ x3 = null]

                                                  Table A.6: Inferred Specifications for Smallfoot Benchmark
Blue text indicates inferred anti-frames, Red text indicates inferred frames. Π is used as a shorthand for pure constraints from the initial entailment that
                                                             are not relevant to the inference.
