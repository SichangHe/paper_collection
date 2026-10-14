                                        An Efficient Cyclic Entailment Procedure in a Fragment
                                                           of Separation Logic

                                                                    Quang Loc Le1 and Xuan-Bach D. Le2
                                                1
                                                  Department of Computer Science, University College London, United Kingdom
arXiv:2210.00616v1 [cs.LO] 2 Oct 2022




                                           2
                                               School of Computing and Information Systems, the University of Melbourne, Australia



                                                 Abstract. An efficient entailment proof system is essential to compositional ver-
                                                 ification using separation logic. Unfortunately, existing decision procedures are
                                                 either inexpressive or inefficient. For example, Smallfoot is an efficient procedure
                                                 but only works with hardwired lists and trees. Other procedures that can support
                                                 general inductive predicates run exponentially in time as their proof search re-
                                                 quires back-tracking to deal with disjunction in the consequent.
                                                 In this paper, we present a decision procedure that can derive cyclic entailment
                                                 proofs for general inductive predicates in polynomial time. Our procedure is ef-
                                                 ficient and does not require back-tracking; it uses normalisation rules that help
                                                 avoid the introduction of disjunction in the consequent. Moreover, our decidable
                                                 fragment is sufficiently expressive: It is based on compositional predicates and
                                                 can capture a wide range of data structures, including sorted and nested list seg-
                                                 ments, skip lists with fast forward pointers, and binary search trees. We have
                                                 implemented the proposal in a prototype tool and evaluated it over challenging
                                                 problems taken from a recent separation logic competition. The experimental re-
                                                 sults confirm the efficiency of the proposed system.


                                        Keywords: Cyclic Proofs, Entailment Procedure, Separation Logic.


                                        1 Introduction
                                        Separation logic [20,35] has been very successful in automatically reasoning about pro-
                                        grams that manipulate pointer structures. Separation logic empowers reusability and
                                        scalability through compositional reasoning [6,7]. Moreover, a compositional verifica-
                                        tion system relies on a bi-abduction procedure which is essentially based on the entail-
                                        ment proof system. Entailment is defined as: Given an antecedent A and a consequent
                                        C where A and C are formulas in separation logic, entailment problem is the act of
                                        checking whether A |= C is valid. Thus, an efficient decision procedure for entailments
                                        is the vital ingredient of an automatic verification system in separation logic.
                                             To enhance the expressiveness of the assertion language, for example, to specify un-
                                        bounded heaps and interesting pure properties (e.g., sortedness, parent pointers), sep-
                                        aration logic is typically combined with user-defined inductive predicates [9,29,33].
                                        In this setting, one key challenge of an entailment procedure is the ability to support
                                        induction reasoning over the combination of heaps and data content. The problem of
                                        induction is very difficult, especially for an automated inductive theorem prover, where
                                        the induction rules are not explicitly stated. In fact, this problem is undecidable [1].
    Developing a sound and complete entailment procedure that could be used for com-
positional reasoning is not trivial. While it is unknown how model-based systems e.g.,
[14,15,17,18,22,23], could support compositional reasoning, there was evidence that
proof-based decision procedures, e.g., Smallfoot [2] and its variant [12], and Cycomp
[40], can be extended to solve the bi-abduction problem, which enables compostional
reasoning and scalability [7,25]. In fact, Smallfoot was the center of the biabductive pro-
cedure deployed in Infer [7], which achieved great impact in both academia and industry
[13]. Furthermore, Smallfoot is very efficient due to its use of “exclude-the-middle” rule
in which it can avoid the proof search over the disjunction in the consequent. However,
Smallfoot works for hardwired lists and binary trees only. In contrast, Cycomp, a recent
complete entailment procedure, is a cyclic proof system without “exclude-the-middle“,
can support general inductive predicates, but has double exponential time complexity
due to the proof search (and back-tracking) in the consequent.
    In this paper, we introduce a cyclic proof system with an “exclude-the-middle”-
styled decision procedure for decidable yet expressive inductive predicates. Especially,
we show that our procedure runs in polynomial time when the maximum number of
fields of data structures is bounded by a constant. The decidable fragment, called SHLIDe,
contains inductive definitions of compositional predicates and pure properties. These
predicates can capture nested list segments, skip lists and trees. The pure properties of
small models can model a wide range of common data structures e.g., a list with fast for-
ward pointers, a nested list being sorted, a tree being a binary search tree [22,30]. This
fragment is much more expressive than Smallfoot’s fragment and is non-overlapping
with Cycomp’s one [40]: there exist some entailments which our system can handle but
Cyccomp could not, and vice versa.
    Our procedure is a variant of the cyclic proof system, which was first introduced
by Brotherston [3,5] and has become one of the main solutions to induction reasoning.
Intuitively, a cyclic proof is naturally represented as a tree of statements (entailments in
this paper): the leaves are either axioms or nodes which are linked back to inner nodes,
the root of the tree is the theorem to be proven, and nodes are connected to one or more
children by locally sound proof rules. Alternatively, a cyclic proof can be viewed as a
tree possibly containing some backlinks (a.k.a. cycles, e.g., “C, if B, if C”) such that the
proof satisfies some global soundness condition. This condition ensures that the proof
can be viewed as a proof of infinite descent. Particularly, for a cyclic entailment proof
with inductive definitions, if every cycle contains an unfolding of some inductive pred-
icate, then that predicate is infinitely often reduced into a strictly “smaller” predicate;
this is impossible as the semantics of inductive definitions only allows finite steps of
unfolding. Hence, that proof path with the cycle can be disregarded.
    The proposed system advances Brotherston’s system in three ways. First, the pro-
posed proof search algorithm is specialized to SHLIDe in which it includes “exclude-
the-middle“ rules and excludes any back-tracking. The existing proof procedures typi-
cally search for a proof (and back-track) over disjunctive cases generated from unfold-
ing inductive predicates in the RHS of an entailment. To avoid such costly searches,
we propose a “exclude-the-middle“-styled normalized rules in which unfolding of in-
ductive predicates in the RHS always produces one disjunct. Therefore, our system is
much more efficient than existing systems. Second, while a standard Brotherston sys-

                                             2
tem is incomplete, our proof search is complete in SHLIDe: If it is stuck (i.e., it can not
apply any inference rules) then the root entailment is invalid.
    Lastly, while the global soundness in [5] must be checked globally and explicitly,
every backlink generated in SHLIDe is sound by design. We note that Cycomp, in-
troduced in [40], was the first work to show completeness of a cyclic proof system.
However, in contrast to ours, it did not discuss the global soundness condition, which is
the key idea attributing to the soundness of cyclic proofs.

Contributions Our primary contributions are summarized as follows.
 – We present a novel decision procedure, called S2SLin , for the entailment problem in
   separation logic with inductive definitions of compositional predicates.
 – We provide a complexity analysis of the procedure.
 – We have implemented the proposal in a prototype tool, called S2SLin , and tested it
   with the SL-COMP 2022 benchmarks [36,37]. The experimental results show that
   S2SLin is effective and efficient when compared with the state-of-the-art solvers.

Organization The remainder of the paper is organised as follows. Sect. 2 describes
syntax of formulas in fragment SHLIDe. Sect. 3 presents the basics of an “exclude-the-
middle” proof system and cyclic proofs. Sect. 4 elaborates the result, the novel cyclic
proof system including an illustrative example. Sect. 5 discusses the soundness and
completeness. Sect. 6 presents the implementation and evaluation. Sect. 7 discusses
related work. Finally, Sect. 8 concludes the work. All proofs are available in Appendix.

2 Decidable Fragment SHLIDe
Subsection 2.1 presents syntax of separation logic formulae and recursive definitions of
linear predicates and local properties. Subsection 2.2 shows semantics.

2.1 Separation Logic Formulas
Concrete heap models assume a fixed finite collection Node, a fixed finite collection
Fields, a set Loc of locations (heap addresses), a set of non-addressable values Val, with
the requirement that Val∩Loc=∅ (i.e., no pointer arithmetic). null is a special element
of Val. Z denotes the set of integers (Z⊆Val) and k denotes integer numbers. Var an
infinite set of variables, v̄ a sequence of variables.

Syntax Disjunctive formula Φ, symbolic heaps ∆, spatial formula κ, pure formula π,
pointer (dis)equality φ, and (in)equality formula α are as follows.
        Φ ::= ∆ | Φ ∨ Φ       ∆ ::= κ∧π | ∃v. κ∧π          φ ::= v=v | v=null
        κ ::= emp | x7→c(f :v, .., f :v) | P(v̄) | κ∗κ     α ::= a=a | a≤a
        π ::= true | α | φ | ¬π | ∃v. π | π∧π              a ::= k | v
where v∈Var, c∈Node and f ∈Fields. Note that we often discard field names f of points-
to predicates x7→c(f :v, .., f :v) and use the short form as x7→c(v̄). v1 6=v2 is the short
form of ¬(v1 =v2 ). E denotes for either a variable or null. ∆[E/v] denotes the formula
obtained from ∆ by substituting v by E. A symbolic heap is referred as a base, denoted
as ∆b , if it does not contain any occurrence of inductive predicates.

                                            3
Inductive Definitions We write P to denote a set of n defined predicates P={P1 , ..., Pn }
in our system. Each inductive predicate has following types of parameters: a pair of root
and segment defining segment-based linked points-to heaps, reference parameters (e.g.,
parent pointers, fast-forwarding pointers), transitivity parameters (e.g., singly-linked
lists where every heap cell contains the same value a) and pairs of ordering parameters
(e.g., trees being binary search trees). An inductive predicate is defined as

pred P(r,F ,B̄,u,sc,tg) ≡ emp∧r=F ∧sc=tg
     ∨ ∃Xtl , Z̄, sc′ .r7→c(Xtl ,p̄,u,sc′ ) ∗ κ′ ∗ P(Xtl ,F ,B̄,u,sc′ ,tg) ∧ r6=F ∧ sc ⋄ sc′

where r is the root, F the segment, B̄ the borders, u the parameter for a transitivity
property, sc and tg source and target, respectively, parameters of an order property,
r7→c(Xtl ,p̄,u,sc′ ) ∗ κ′ the matrix of the heaps, and ⋄ ∈ {=, ≥, ≤}. (The extension for
multiple local properties is straightforward.) Moreover, this definition is constrained by
the following three conditions on heap connectivity, establishment, and termination.
Condition C1. In the recursive rule, p̄ = {null}∪Z̄. This condition implies that If
two variables points to the same heap, their content must be the same. For instance, the
following definition of singly-linked lists of even length does not satisfy this condition.

  pred ell(r,F ) ≡ emp∧r=F ∨ ∃x1 ,X.r7→c1 (x1 )∗x1 7→c1 (X)∗ell(X,F )∧r6=F
as n3 and X are not field variables of the node pointed-to by r.
Condition C2. The matrix heap defines nested and connected list segments as:

                                κ′ :=Q(Z,Ū ) | κ′ ∗κ′ | emp

where Z∈p̄ and (Ū \ p̄) ∩ Z = ∅. This condition ensures connectivity (i.e. all allocated
heaps are connected to the root) and establishment (i.e. every existential quantifier either
is allocated or equals to a parameter).
Condition C3. There is no mutual recursion. We define an order ≺P on inductive pred-
icates as: P ≺P Q if at least one occurrence of predicate Q appears in the definition of P
and Q is called a direct sub-term of P. We use ≺∗P to denote the transitive closure of ≺P .
     Several definition examples are shown as follows.

pred ll(r,F ) ≡ emp∧r=F ∨ ∃Xtl .r7→c1 (Xtl )∗ll(Xtl , F )∧r6=F
pred nll(r,F ,B) ≡ emp∧r=F
  ∨ ∃Xtl ,Z.r7→c3 (Xtl ,Z)∗ll(Z, B)∗nll(Xtl ,F ,B)∧r6=F
pred skl1(r,F ) ≡ emp∧r=F ∨ ∃Xtl .r7→c4 (Xtl ,null,null)∗skl1(Xtl , F )∧r6=F
pred skl2(r,F ) ≡ emp∧r=F
  ∨ ∃Xtl , Z1 .r7→c4 (Z1 ,Xtl ,null)∗skl1(Z1 ,Xtl )∗skl2(Xtl , F )∧r6=F
pred skl3(r,F ) ≡ emp∧r=F
  ∨ ∃Xtl ,Z1 ,Z2 .r7→c4 (Z1 ,Z2 ,Xtl )∗skl1(Z1 ,Z2 )∗skl2(Z2 ,Xtl )∗skl3(Xtl ,F )∧r6=F
pred tree(r,B) ≡ emp∧r=B
   ∨ ∃rl , rr .r7→ct (rl ,rr )∗tree(rl ,B)∗tree(rr ,B) ∧ r6=B

ll defines singly-linked lists, nll defines lists of acyclic lists, slk1, slk2 and slk3
define skip-lists. Finally, tree defines binary trees. We extend predicate ll with transi-

                                             4
tivity and order parameters to obtain predicate lla and lls, respectively, as follows.
    pred lla(r,F ,a) ≡ emp∧r=F ∨ ∃Xtl .r7→c2 (Xtl ,a) ∗ lla(Xtl ,F ,a)∧r6=F
    pred lls(r,F ,mi,ma) ≡ emp∧r=F ∧ma=mi
      ∨ ∃Xtl ,mi1 .r7→c4 (Xtl ,mi1 ) ∗ lls(Xtl ,F ,mi1 ,ma)∧r6=F ∧ mi≤mi1

Unfolding Given pred P(t̄) ≡ Φ and a formula P(v̄)∗∆, then unfolding P(v̄) means
replacing P(v̄) by Φ[v̄/t̄]. We annotate a number, called unfolding number, for each oc-
currence of inductive predicates. Suppose ∃w̄.r7→c(p̄) ∗ Q1 (v̄1 )∗...∗Qm (v̄m ) ∗ P(v̄0 )∧π
be the recursive rule, then in the unfolded formula, if P(v̄0 [v̄/t̄])k1 and Qi (...)k2 are di-
rect sub-terms of P(v̄)k like above, then k1 =k+1 and k2 = 0. When it is unambiguous,
we discard the annotation of the unfolding number for simplicity.

2.2 Semantics
The program state is interpreted by a pair (s,h) where s∈Stacks, h∈Heaps and stack
Stacks and heap Heaps are defined as:
                         def
                 Heaps = Loc⇀f in (Node → (Fields → Val ∪ Loc)m )
                         def
                 Stacks = Var → Val ∪ Loc
Note that we assume that every data structure contains at most m fields. Given a formula
Φ, its semantics is given by a relation: s,h |= Φ in which the stack s and the heap h
satisfy the constraint Φ. The semantics is shown below
 s, h |= emp            iff dom(h)=∅
 s, h |= v7→c(fi : vi ) iff dom(h)={s(v)}, h(s(v))=g, g(c, fi )=s(vi )
 s, h |= P (v̄)         iff (h, s(v̄1 ), .., s(v̄k )) ∈ JP K
 s, h |= κ1 ∗ κ2        iff ∃h1 , h2 s.t h1 #h2 , h=h1 ·h2 , , s, h1 |= κ1 and s, h2 |= κ2
 s, h |= true           iff always
 s, h |= κ∧π            iff s, h |= κ and s |= π
 s, h |= ∃v.∆           iff ∃α.s[v7→α], h |= ∆
 s, h |= Φ1 ∨ Φ2        iff s, h |= Φ1 or s, h |= Φ2
dom(g) is the domain of g, h1 #h2 denotes disjoint heaps h1 and h2 i.e., dom(h1 )∩dom(h2 )=∅,
and h1 ·h2 denotes the union of two disjoint heaps. If s is a stack, v∈Var, and α∈Val∪Loc,
we write s[v7→α] = s if v∈dom(s), otherwise s[v7→α] = s∪{(v, α)}. Semantics of
non-heap (pure) formulas is omitted for simplicity. The interpretation of an inductive
predicate P(t̄) is based on the least fixed point semantics JP K.
   Entailment ∆ |= ∆′ holds iff for all s and h, if s, h |= ∆ then s, h |= ∆′ .

3 Entailment Problem & Overview
Throughout this work, we consider the following problem.
   PROBLEM: QF ENT−SLLIN .
   INPUT:    ∆a ≡ κa ∧πa and ∆c ≡ κc ∧πc where FV(∆c ) ⊆ FV(∆a ) ∪ {null}.
   QUESTION: Does ∆a |= ∆c hold?

                                              5
   An entailment, denoted as e, is syntactically formalized as: ∆a ⊢ ∆c where ∆a and
∆c are quantifier-free formulas whose syntax are defined in the preceding section.
   In Sect. 3.1, we present the basis of an exclude-the-middle proof system and our
approach to QF ENT−SLLIN . In Sect. 3.2, we describe the foundation of cyclic proofs.


3.1 Exclude-the-middle proof system

Given a goal ∆a ⊢ ∆c , an entailment proof system might derive entailments with dis-
junction in the right-hand side (RHS). Such an entailment can be obtained by a proof
rule that replaces an inductive predicate by its definition rules. Authors of Smallfoot
[2] introduced a normal form and proof rules to prevent such entailments when the
predicate are lists or trees. Basically, Smallfoot considers the following two scenarios.

 – Case 1 (Exclude-the-middle and Frame): The inductive predicate matches with a
   points-to predicate in the left hand side (LHS). For instance, the entailment is of the
   form e1 : x7→c(z) ∗ ∆ ⊢ ll(x, y) ∗ ∆′ , where ll is singly-linked lists and ll(x, y)
   matches with x7→c(z) as they have the same root x. To discharge e1 , a typical proof
   system might search for a proof through two definition rules of predicate ll (i.e., by
   unfolding ll(x, y) into two disjuncts): One includes the base case with x = y and
   another contains the recursive case with x 6= y. Smallfoot prevents such unfolding
   by excluding the middle in the LHS: It reduces the entaiment into two premises:
   x7→c(z) ∗ ∆ ∧ x = y ⊢ ll(x, y) ∗ ∆′ and x7→c(z) ∗ ∆ ∧ x 6= y ⊢ ll(x, y) ∗ ∆′ .
   The first one considers the base case of the list (that is, ll(x, x)) and is equivalent
   to x7→c(z) ∗ ∆ ∧ x = y ⊢ ∆′ . And the second premise checks the inductive case of
   the list and is equivalent to ∆ ∧ x 6= y ⊢ ll(x, z) ∗ ∆′ .
 – Case 2 (Induction proving via hard-wired Lemma). The inductive predicate matches
   other inductive predicates in the LHS. For example, the entailment is of the form
   e2 : ll(x, z) ∗ ∆ ⊢ ll(x, null) ∗ ∆′ . Smallfoot handle e2 by using a proof
   rule as the consequence of applying the following hard-wired lemma ll(x, z) ∗
   ll(z, null) |= ll(x, null) and reduces the entailment to ∆ ⊢ ll(z, null) ∗ ∆′ .

In doing so, Smallfoot does not introduce a disjunction in the RHS. However, as it uses
specific lemmas in the induction reasoning, it only works for the hardwired lists.
    In this paper, we propose S2SLin as an exclude-the-middle’s system for user-defined
predicates, those in SHLIDe. In stead of using hardwired lemmas, we apply cyclic proofs
for induction reasoning. For instance, to discharge the entailment e2 above, S2SLin first
unfolds ll(x, z) in the LHS and obtains two premises:

 – e21 : (emp ∧ x = z) ∗ ∆ ⊢ ll(x, null) ∗ ∆′ ; and
 – e22 : (x7→c(y) ∗ ll(y, z) ∧ x 6= z) ∗ ∆ ⊢ ll(x, null) ∗ ∆′

While it reduces e21 to ∆[z/x] ⊢ ll(z, null) ∗ ∆′ [z/x], for e22 , it further applies the
frame rule as in Case 1 above and obtains ll(y, z) ∗ ∆ ∧ x 6= z ⊢ ll(y, null) ∗ ∆′ .
Then, it makes a backlink between the latter and e2 and closes this path. By doing so,
it does not introduce disjunctions in the RHS and can handle user-defined predicates.

                                           6
3.2 Cyclic proofs
Central to our work is a procedure that construct a cyclic proof for an entailment. Given
an entailment ∆ ⊢ ∆′ , if our system can derive a cyclic proof, then ∆ |= ∆′ holds. If,
instead, it is stuck without a proof, then ∆ |= ∆′ is not valid.
    The procedure includes proof rules, each of which is of the form:
                                        e1 ... en
                                 PR0        e        cond
where entailment e (called the conclusion) is reduced to entailments e1 , ..,en (called
the premises) through inference rule PR0 given that the side condition cond holds.
    A cyclic proof is a proof tree Ti which is a tuple (V, E, C) where
 – V is a finite set of nodes representing entailments derived during the proof search;
 – A directed edges (e, PR, e′ ) ∈ E (where e′ is a child of e) means that the premise
   e′ is derived from the conclusion e via inference rule PR. For instance, suppose
   that the rule PR0 above has been applied, then the following n edges are generated:
   (e, PR0 , e1 ), .., (e, PR0 , en );
 – and C is a partial relation which captures back-links in the proof tree. If C(ec →eb , σ)
   holds, then eb is linked back to its ancestor ec through the substitution σ (where eb
   is referred as a bud and ec is referred as a companion). In particular, ec is of the
   form: ∆ ⊢ ∆′ and eb is of the form: ∆1 ∧π ⊢ ∆′1 where ∆ ≡ ∆1 σ and ∆′ ≡ ∆′1 σ.
A leaf node is marked as closed if it is evaluated as valid (i.e. the node is applied with an
axiom) or invalid (i.e. no rule can apply), or it is linked back. Otherwise, it is marked as
open. A proof tree is invalid if it contains at least one invalid leaf node. It is a pre-proof
if all its leaf nodes are either valid or linked back. A pre-proof is a cyclic proof if a
global soundness condition is imposed in the tree. Intuitively, this soundness condition
requires that for every C(ec →eb , σ), there exist inductive predicates P(t¯1 ) in ec and
Q(t¯2 ) in eb such that Q(t¯2 ) is a subterm of P(t¯1 ).
Definition 1 (Trace) Let Ti be a pre-proof of ∆a ⊢ ∆c and (∆ai ⊢ ∆ci )i≥0 be a path
of Ti . A trace following (∆ai ⊢∆ci )i≥0 is a sequence (αi )i≥0 such that each αi (for all
i≥0) is a subformula of ∆ai containing predicate P(t̄)u , and either:
 – αi+1 is the subformula occurrence in ∆ai+1 corresponding to αi in ∆ai .
 – or ∆ai ⊢ ∆ci is the conclusion of a left-unfolding rule, αi ≡ P(t̄)u is unfolded, and
   αi+1 is a subformula in ∆ai+1 and is the definition rule of P(x̄)u [t̄/x̄]. In this case,
   i is said to be a progressing point of the trace.
Definition 2 (Cyclic proof) A pre-proof Ti of ∆a ⊢ ∆c is a cyclic proof if, for every
infinite path (∆ai ⊢∆ci )i≥0 of Ti , there is a tail of the path p=(∆ai ⊢ ∆ci )i≥n such
that there is a trace following p which has infinitely progressing points.
    Suppose that all proof rules are (locally) sound (i.e., if the premises are valid then
the conclusion is valid), the following Theorem shows the global soundness.
Theorem 3.1 (Soundness [5]). If there is a cyclic proof of ∆a ⊢ ∆c , then ∆a |= ∆c .
The proof is by contraction and can be found in [5]. Intuitively, if we can derive a cyclic
proof for ∆a ⊢ ∆c and ∆a 6|= ∆c , then the inductive predicate at the progress points can
be unfolded infinite often. This contradicts with the least semantics of the predicate.

                                              7
4 Cyclic Entailment Procedure
In this section, we present our main proposal, the entailment procedure ω-ENT with the
proposed inference rules (subsection 4.1), and an illustrative example in subsection 4.2.

4.1 Proof Search
The proof search algorithm ω-
ENT is presented in Fig. 1. ω- ω−ENT
ENT takes e0 as input, pro- input: e0                        output: valid or invalid
duces cyclic proofs and based 1: i←0; Ti ←e0 ;
on that decides whether the in- 2: while true do
put is valid or invalid. Ini- 3: (res, ei , P Ri )←is closed(Ti);
tially, for every P(v̄)k ∈ e0 , k 4: if res=valid then return valid;
is reset to 0 and T0 only has e0 5: if res=invalid then return invalid;
as an open leaf, the root. The 6: if link backe(Ti , ei ) = false then
overall idea of ω-ENT is to itera- 7:          Ti+1 ← apply(Ti , ei , P Ri );
tively reduce T0 into a sequence 8: i←i+1;
of cyclic proof trees Ti , i ≥ 9: end
0. On line 3, through procedure
is closed(Ti ), ω-ENT chooses
                                       Fig. 1: Proof tree construction procedure
an open leaf node ei and a proof
rule P Ri to apply. If is closed(Ti ) returns valid (that is, every leaf is applied to an
axiom rule or involved in a backlink), ω-ENT returns valid on line 4. If it returns
invalid, then ω-ENT returns invalid (one line 5). Otherwise, it tries to link ei back to
an internal node (on line 6). If this attempt fails, it applies the rule (line 7).
     Note that for each leaf, is closed attempts rules in the following order: normaliza-
tion rules, axiom rules, and reduction rules. A rule P Ri is chosen if its conclusion can
be unified with the leaf, through some substitution σ. Then, on line 7, for each premise
of P Ri , procedure apply creates a new open node and connects the node to ei via a
new edge. If P Ri is an axiom, procedure apply marks ei as closed and returns.

Procedure is closed(Ti ) This procedure examines the following three cases.
 1. First, if all leaf nodes are marked closed and none of them is invalid then is closed
    returns valid.
 2. Secondly, is closed returns invalid if there exists an open leaf node ei : ∆ ⊢ ∆′
    in NF such that one of the four following conditions holds:
    (a) ei could not be applied by any inference rule.
    (b) there exists a predicate op1 (E) ∈ ∆ such that op2 (E) ∈      / ∆′ and one of the
         following conditions holds:
           – either P(E ′ ,E,...) or E ′ 7→c(E,..) are in both sides
           – both P(E ′ ,E,...) 6∈ ∆ and E ′ 7→c(E,..) 6∈ ∆
    (c) there exists a predicate op1 (E)∈∆′ such that G(op1 (E))∈∆ and op2 (E)∈∆.         /
    (d) there exist x7→c1 (v̄1 ) ∈ ∆, x7→c2 (v̄2 ) ∈ ∆′ such that c1 6≡ c2 or v̄1 6≡v̄2 .
 3. Lastly, there exists an open leaf node ei that could be applied by an inference rule
    (e.g. P Ri ), is closed returns the triple (unknown, ei , P Ri ).
   In the rest, we discuss the proof rules and the auxiliary procedures in detail.

                                            8
                                        ∆∧E1 =E2 ⊢ ∆′
            ∆[E/x] ⊢ ∆′ [E/x]
  Subst                                 ∆∧E1 6=E2 ⊢ ∆′               E1 =E2 , E1 6=E2 6∈π &
              ∆∧x=E ⊢ ∆′          ExM
                                                                 FV(E1 , E2 ) ⊆ (FV(∆)∪FV(∆′ ))S
                                                ∆ ⊢ ∆′

                      ∆ ⊢ ∆′                         (κ∧π)[tg/sc] ⊢ ∆′ [tg/sc]
               =L                       LBase
                    ∆∧E=E ⊢ ∆′                      P(E,E,B̄,u,sc,tg)∗κ∧π ⊢ ∆′
                         op(E)∗κ∧π∧G(op(E))∧E6=null ⊢ ∆′
                6=null                                                  E6=null∈π
                                                                               /
                             op(E)∗κ∧π∧G(op(E)) ⊢ ∆′
         op1 (E1 )∗op2 (E2 )∗κ∧π∧E1 6=E2 ⊢ ∆′
   6=∗                                               E1 6=E2 6∈π and G(op1 (E1 )), G(op2 (E2 )) ∈ π
             op1 (E1 )∗op2 (E2 )∗κ∧π ⊢ ∆′

                                Fig. 2: Normalization rules

Normalization An entailment is in the normal form (NF) if its LHS is in NF. We write
op(E) to denote for either E7→c(v̄) or P(E,F ,B̄,v̄). Furthermore, the guard G(op(E))
                           def                             def
is defined by: G(E7→c(v̄)) = true and G(P(E,F ,B̄,v̄)) = E6=F .

Definition 3 (Normal Form) A formula κ∧φ∧a is in normal form if:

          1. op(E) ∈ κ implies G(op(E)) ∈ φ                            4. E1 =E2 6∈ φ
          2. op(E) ∈ κ implies E6=null ∈ φ                             5. E6=E 6∈ φ
          3. op1 (E1 ) ∗ op2 (E2 ) ∈ κ implies E1 6=E2 ∈ φ             6. a is satisfiable

If ∆ is in NF and for any s, h |= ∆, then dom(h) is uniquely defined by s.
    The normalisation rules are presented in Fig. 2. Basically, ω-ENT applies these rules
to a leaf exhaustively and transforms it into NF before other. Given an inductive predi-
cate P(E, F, ...), rule ExM excludes the middle by doing case analysis for the predicate
between base-case (i.e., E=F ) and recursive-case (i.e., E6=F ). The normalization rule
6=null follows the following facts: E7→c( ) ⇒ E6=null and P(E,F , )∧E6=F ⇒
 E6=null. Similarly, rule 6=∗ follows the following facts: x7→ ∗P(y,F , )∧y6=F ⇒
x6=y, x7→ ∗y7→ ⇒ x6=y, and Pi (x,F1 , )∗Pj (y,F2 , )∧x6=F1 ∧y6=F2 ⇒ x6=y.

Axiom and Reduction Axiom rules include Emp, Inconsistency and Id presented in
Fig. 3. If each of these rules is applied into a leaf node, the node is evaluated as valid
and marked as closed. The remaining ones in Fig. 3 are reduction rules.
    To simplify the presentation, the unfoldings in rules Frame, RInd, and LInd are ap-
plied with the following definition of inductive predicates:
P(x,F ,B̄,u,sc,tg) ≡ emp∧x=F ∧sc=tg
  ∨ ∃X,sc′ ,d1 ,d2 .x7→c(X,d1 ,d2 ,u,sc)∗Q1 (d1 ,B)∗Q2 (d2 ,X)∗P(X,F ,B̄,u,sc′ ,tg)∧π0

where B∈B̄, the matrix κ′ contains two nested predicates Q1 and Q2 , and the heap
cell c ∈ Node is defined as data c{c next; c1 down1 ; c2 down2 ; τs scdata; τu udata}
where c1 , c2 ∈Node, down1 , down2 fields are for the nested predicates in the matrix

                                                9
       Id                   Emp                             Inconsistency              π |= false
             ∆∧π⊢∆                   emp∧π ⊢ emp∧true                        κ∧π ⊢ ∆

          ∆ ⊢ ∆′                           ∆∧π ⊢ ∆′                               ∆ ⊢ ∆′ ∧ tg=sc
=R                           Hypothesis                   π |= π ′   RBase
       ∆ ⊢ ∆′ ∧E=E                        ∆∧π ⊢ ∆′ ∧π ′                       ∆ ⊢ P(E,E,B̄,u,sc,tg)∗∆′
       κ1 ∧π ⊢ κ2      κ∧π ⊢ κ′ ∧π ′      roots(κ1 ) ∩ roots(κ) = ∅ & FV(κ2 )⊆FV(κ1 ∧π)∪{null}
∗
            κ1 ∗κ∧π ⊢ κ2 ∗κ′ ∧ π ′                      & FV(κ′ )⊆FV(κ∧π)∪{null}
                  Q1 (E1 ,B)0 ∗Q2 (E2 ,X)0 ∗P(X,F ,B̄,u,sc′ ,tg)k ∗∆1 ∧x6=F3 ∧π0
                      ⊢ Q(x,F3 ,B̄,u,sc,tg2 )∗κ2 ∧π2
       Frame                                                                           x7→c( )6∈κ2
                 P(x,F ,B̄,u,sc,tg)k ∗∆1 ∧x6=F3 ⊢ x7→c(X,E1 ,E2 ,u,sc′ )∗κ2 ∧π2
            x7→c(X,E1 ,E2 ,u,sc′ )∗κ1 ∧π1 ∧x6=F
              ⊢ x7→c(X,E1 ,E2 ,u,sc′ )∗Q1 (E1 ,B)∗Q2 (E2 ,X)∗P(X,F ,B̄,u,sc′ ,tg)∗κ2 ∧π2 ∧π0
RInd                                                                                                 †
                    x7→c(X,E1 ,E2 ,u,sc′ )∗κ1 ∧π1 ∧x6=F ⊢ P(x,F ,B̄,u,sc,tg)∗κ2 ∧π2
            x7→c(X,E1 ,E2 ,u,sc′ )∗Q1 (E1 ,B)0 ∗Q2 (E2 ,X)0 ∗P(X,F ,B̄,u,sc′ ,tg)k+1 ∗∆1 ∧x6=F3 ∧π0
               ⊢ Q(x,F3 ,B̄,u,sc,tg2 )∗κ2 ∧π2
LInd                                                                                                     ♯
                         P(x,F ,B̄,u,sc,tg)k ∗∆1 ∧x6=F3 ⊢ Q(x,F3 ,B̄,u,sc,tg2 )∗κ2 ∧π2

Fig. 3: Reduction rules (where ♯: P(x,F ,B̄,u,sc,tg)6∈κ2 , †: x7→c(X,E1 ,E2 ,u,sc′ )6∈κ2 )



heaps, udata field is for the transitivity data, and scdata field are for ordering data. The
formalism of these rules for general form of the matrix heaps κ′ is presented in App. A.
     =R and Hypothesis eliminate pure constraints in the RHS. In rule ∗, roots(κ) is
defined inductively as: roots(emp)≡{}, roots(r7→ )≡{r}, roots(P (r, F, ..))≡{r}
and roots(κ1 ∗κ2 ) ≡ roots(κ1 ) ∪ roots(κ2 ). This rule is applied in three ways.
First, it is applied into an entailment which is of the form κ∧π ⊢ κ∧π ′ . It matches
and discards the identified heap predicates between the two sides so as to generate a
premise with empty heaps. As a result, this premise may be applied with the axiom
rule EMP. Secondly, it is applied into an entailment whose LHS is a base formula e.g.,
x1 7→c1 (v̄1 )∗...∗xn 7→cn (v̄n )∧π ⊢ κ′ ∧π ′ . For each points-to predicate xi 7→ci (v̄i )∈κ′ ,
ω-ENT searches for one points-to predicate xj 7→cj (v̄j ) in the LHS such that xj 7→cj (v̄j ) ≡
xi 7→ci (v̄i ). Likewise, for each occurrence of inductive predicates P(r,F ,B̄,u,sc,tg) in
the RHS, ω-ENT searches for a points-to predicate r7→ in the LHS such that rule
RInd could be applied. If any of these searches fails, ω-ENT decides the conclusion as
invalid. Lastly, it is applied into an entailment that is of the form ∆1 ∗ ∆ ⊢ ∆2 ∗ ∆′
where either ∆1 ⊢ ∆2 or ∆ ⊢ ∆′ could be linked back into an internal node.
    Rule LInd unfolds the inductive predicates in the LHS. We notice that every LHS
of entailments in this rule also captures the unfolding numbers for subterm relationship
and generates the progressing point in the cyclic proofs afterward. These numbers are
essential for our system to construct cyclic proofs. This rule is applied in a depth-first
manner i.e., if there are more than one occurrences of inductive predicates in the LHS
that could be applied by this rule, the one with the greatest unfolding number is chosen.

                                                   10
We emphasize that the last five rules still work well when the predicate in the RHS
contains only a subset of the local properties wrt. the predicate in the LHS.

Back-Link Generation Procedure link backe generates a back-link as follows. In a pre-
proof, given a path containing a back-link, say e1 , e2 , .., em where e1 is a companion
and em a bud, then e1 is in NF and of the following form:

 – e1 ≡P(x,F ,B̄,u,sc,tg)k ∗κ∧π∧x6=F ∧x6=null ⊢ Q(x,F2 ,B̄,u,sc,tg2 )∗κ′ ∧π ′ .
 – e2 is obtained from applying LInd into e1 . e2 is of the form:

         x7→c(X, p̄, ,u,sc)∗κ′ ∗P(X,F ,B̄,u,sc′ ,tg)k+1 ∗κ∧π∧x6=F ∧x6=null∧π1
           ⊢ Q(x,F2 ,B̄,u,sc,tg2 )∗κ′ ∧π ′

   We remark that sc ⋄ sc′ ∈ π1 and if k ≥ 1 then sci ⋄ sc ∈ π
 – e3 , .., em−4 are obtained from applications of normalization rules in order to nor-
   malize the LHS of e2 due to the presence of κ′ . We note that as the roots of induc-
   tive predicates in κ′ are fresh variables, the applications of the normalization rules
   above do not affect the RHS of e2 . That means RHS of e3 , .., em−4 are the same
   with the RHS of e2 . As a result, em−4 is of the form:

      x7→c(X, p̄, ,u,sc)∗κ′′1 ∗P(X,F ,B̄,u,sc′ ,tg)k+1 ∗κ∧π∧x6=F ∧x6=null∧π1 ∧π2
        ⊢ Q(x,F2 ,B̄,u,sc,tg2 )∗κ′ ∧π ′

   where κ′′1 may be emp and π2 is a conjunction of disequalities coming from ExM.
 – em−3 is obtained from application of ExM over x and F2 and of the form:

      x7→c(X, p̄, ,u,sc)∗κ′′1 ∗P(X,F ,B̄,u,sc′ ,tg)k+1 ∗κ∧π∧x6=F ∧x6=null∧π1 ∧π2
        ∧x6=F2 ⊢ Q(x,F2 ,B̄,u,sc,tg2 )∗κ′ ∧π ′

   (For the case x=F2 , the rule ExM is kept applying until either F ≡ F2 , that is two
   sides are reaching the end of the same heap segment, or it is stuck.)
 – em−2 is obtained from application of RInd and is of the form:
      x7→c(X, p̄, ,u,sc)∗κ′′1 ∗P(X,F ,B̄,u,sc′ ,tg)k+1 ∗κ∧π∧x6=F ∧x6=null∧π1 ∧π2
        ∧x6=F2 ⊢ x7→c(X,p̄,u,sc)∗κ′′2 ∗Q(X,F2 ,B̄,u,sc′ ,tg2 )∗κ′ ∧π ′ ∧π2′
 – em−1 is obtained from application of Hypothesis to eliminate π2′ (otherwise, it is
   stuck) and is of the form:
      x7→c(X, p̄, ,u,sc)∗κ′′1 ∗P(X,F ,B̄,u,sc′ ,tg)k+1 ∗κ∧π∧x6=F ∧x6=null∧π1 ∧π2
        ∧x6=F2 ⊢ x7→c(X,p̄,u,sc)∗κ′′2 ∗Q(X,F2 ,B̄,u,sc′ ,tg2 )∗κ′ ∧π ′
 – em is obtained from application of ∗ and is of the form:
              P(X,F ,B̄,u,sc′ ,tg)k+1 ∗κ∧π∧x6=F ∧x6=null∧π1 ∧π2 ∧x6=F2
                ⊢ Q(X,F2 ,B̄,u,sc′ ,tg2 )∗κ′ ∧π ′
When k ≥ 1 it is always possible to link em back to e1 through the substitution is
σ≡[x/X, sc/sc′ ] after weakening some pure constraints in its LHS.

                                          11
                                                e0
                                             LInd
                                                e1
                                         ExM           ExM                    [x/X, mi/m′ ]
                                        e2                e3
                                Subst                6=∗+RInd
                                 e4
                        LBase
                                                                   e9
                         e5                               Hypothesis
                 RInd                                                   e10
                  e6                                                ∗          ∗
                     Hypothesis+RBase                        e11                   e12
                  e7
                 ∗
                  e8

     Fig. 4: Cyclic Proof of lls(x,null,mi, ma)0 ∧x6=null ⊢ llb(x,null,mi).

4.2 Illustrative Example
We illustrate our system through the following example:

               e0 : lls(x,null,mi,ma)0 ∧ x6=null ⊢ llb(x,null,mi)

where the sorted linked-list lls (mi is the minimum value and ma is the maximum
value) is defined in Sect. 2.1 and llb defines singly-linked lists whose values are greater
than or equal to a constant number. Particularly, predicate llb is defined as follows.

                pred llb(r,F ,b) ≡ emp∧r=F
                  ∨ ∃Xtl ,d.r7→c4 (Xtl ,d) ∗ llb(Xtl ,F ,b)∧r6=F ∧ b≤d

Since the LHS is stronger than the RHS, this entailment is valid. Our system could
generate the cyclic proof (shown in Fig. 4) to prove the validity of e0 . In the following,
we present step-by-step to show how the proof was created. Firstly, e0 , which is in NF,
is applied with rule LInd to unfold predicate lls(x,null,mi,ma)0 and obtain e1 as:

e1 : x7→c4 (X, m′ ) ∗ lls(X,null,m′ , ma)1 ∧ x6=null ∧ mi≤m′ ⊢ llb(x,null,mi)

We remark that the unfolding number of the recursive predicate lls in the LHS is
increased by 1. Next, our system normalizes e1 by applying rule ExM into X and null
to generate two children e2 and e3 as follows.

    e2 : x7→c4 (X, m′ ) ∗ lls(X,null,m′ ,ma)1 ∧ x6=null ∧ mi≤m′ ∧ X=null
           ⊢ llb(x,null,mi)
    e3 : x7→c4 (X, m′ ) ∗ lla(X,null,m′ ,ma)1 ∧ x6=null ∧ mi≤m′ ∧ X6=null
           ⊢ llb(x,null,mi)

For the left child, it applies normalization rules to obtain
    e4 (substitute X by null) and then e5 , by LBase to unfold lls(null,null,m′ ,ma)1
to the base case, as:
e4 : x7→c4 (null, m′ ) ∗ lls(null,null,m′ ,ma)1 ∧ x6=null ∧ mi≤m′ ⊢ llb(x,null,mi)
e5 : x7→c4 (null, ma) ∧ x6=null ∧ mi≤ma ⊢ llb(x,null,mi)

                                                     12
Now, e5 is in NF. S2SLin applies RInd and then RBase to llb in the RHS as:

     e6 : x7→c4 (null, ma) ∧ x6=null ∧ mi≤ma
             ⊢ x7→c4 (null, ma) ∗ llb(null,null,mi) ∧ mi≤ma
     e6′ : x7→c4 (null, ma) ∧ x6=null ∧ mi≤ma ⊢ x7→c4 (null, ma)∧mi≤ma

After that, as mi≤ma ⇒ mi≤ma, e6′ is applied with Hypothesis to obtain e7 .

           e7 : x7→c4 (null, ma) ∧ x6=null ∧ mi≤ma ⊢ x7→c4 (null, ma)

As the LHS of e7 is in NF and a base formula, it is sound and complete to apply rule ∗
to have e8 as: emp ∧ x6=null ∧ mi≤ma ⊢ emp. By Emp, e8 is decided as valid. For
the right branch of the proof, e3 is applied with rule 6=∗ and then RInd to obtain e9 :

e9 : x7→c4 (X, m′ )∗lls(X,null,m′ ,ma)1 ∧ x6=null ∧ mi≤m′ ∧ X6=null ∧ x6=X
       ⊢ x7→c4 (X, m′ )∗llb(X,null,mi)∧mi≤m′

After that, e9 is applied with Hypothesis to eliminate the pure constraint in the RHS:

e10 : x7→c4 (X, m′ )∗lls(X,null,m′ ,ma)1 ∧ x6=null ∧ mi≤m′ ∧ X6=null ∧ x6=X
        ⊢ x7→c4 (X, m′ )∗llb(X,null,mi)

e10 is then applied with ∗ to obtain e11 and e12 as follows.

e11 : x7→c4 (X, m′ ) ⊢ x7→c4 (X, m′ )
e12 : lls(X,null,m′ ,ma)1 ∧ x6=null ∧ mi≤m′ ∧ X6=null ∧ x6=X ⊢ llb(X,null,mi)

e11 is valid by Id. e12 is successfully linked back to e0 to form a pre-proof as

(lls(X,null,m′ ,ma)1 ∧X6=null)[x/X, mi/m′ ] ⊢ llb(X,null,mi)[x/X, mi/m′]

is identical to e0 . Since lls(X,null,m′ ,ma)1 in e12 is the subterm of lls(x,null,mi,ma)0
in e0 , our system decided that e0 is valid with the cyclic proof presented in Fig. 4.


5 Soundness, Completeness, and Complexity
We describe the soundness, termination, and completeness of ω-ENT. First, we need to
show the invariant about the quantifier-free entailments of our system.
Corollary 5.1. Every entailment derived from ω-ENT is quantifier-free.
   The following lemma shows the soundness of the proof rules.
Lemma 5.2 (Soundness). For each proof rule, if all premises are valid, then the con-
clusion is valid.
   As every backlink generated contains at least one pair of inductive predicate oc-
curences in a subterm relationship, the global soundness condition holds in our system.

Lemma 5.3 (Global Soundness). A pre-proof derived is indeed a cyclic proof.

                                           13
    The termination relies on the number of premises/entailments generated by rule ∗.
As the number of inductive symbols and their arities are finite, there is a finite number of
equivalent classes of these entailments in which any two entailments in the same class
are equivalent under some substitution and linked back together. Therefore, the number
of premises generated by rule ∗ is finite considering the generation of backlinks.
Lemma 5.4. ω-ENT terminates.

   In the following, we show the complexity analysis. First, we show that every occur-
rence of inductive predicates in the LHS is unfolded at most two times.
Lemma 5.5. Given any entailment P(v̄)k ∗ ∆a ⊢ ∆c , then 0 ≤ k ≤ 2.
   Let n be the maximum number of predicates (both inductive predicates and points-to
predicates) among the LHS of the input and the definitions in P, and m be the maximum
number of fields of data structures. Then, the complexity is defined as follows.

Proposition 5.6 (Complexity). QF ENT−SLLIN is O(n × 2m + n3 ).
As such, if m is bounded by a constant, the complexity becomes polynomial in time.
    Our completeness proofs are shown in two steps. First, we show the proofs for an
entailment whose LHS is a base formula. Second, we show the correctness when the
LHS contains inductive predicates. In the following, we first define the base formulas
of the LHS derived by ω-ENT from occurrences of inductive predicates. Based on that,
we define bad models to capture counter-model of invalid entailments.

Definition 4 (SHLIDe Base) Given κ, define κ as follows.
                            def
        P(E,F ,B̄,u,sc,tg) = E7→c(F ,E1 ,E2 ,u,tg) ∗ Q1 (E1 ,B)∗Q2 (E2 ,F )∧π0
                  def                      def                   def
        E7→c(v̄) = E7→c(v̄)           emp = emp           κ1 ∗κ2 = κ1 ∗κ2

The definition for general predicates with arbitrary matrix heaps is presented in App. A.
As P does not include mutual recursion (Condition C3), the definition above terminates
in a finite number of steps. In a pre-proof, these SHLIDe base formulas of the LHS of
an entailment are obtained once every inductive predicate has been unfolded once.
Lemma 5.7. If κ ∧ π is in NF then κ ∧ π is in NF, and κ ∧ π ⊢ κ is valid.

In other words, κ ∧ π is an under-approximation of κ ∧ π; invalidity of κ ∧ π ⊢ ∆′
implies invalidity of κ ∧ π ⊢ ∆′ .

Definition 5 (Bad Model) The bad model for κ ∧ φ ∧ a in NF is obtained by assigning
 – a distinct non-null value to each variable in FV(κ ∧ φ); and
 – a value to each variable in FV(a) such that a is satisfiable.

Lemma 5.8. 1. For every proof rule except rule ∗, all premises are valid only if the
    conclusion is valid.
 2. For rule ∗ where the conclusion is of the form ∆b ⊢ κ′ , all premises are valid only
    if the conclusion is valid and ∆b is in NF.

                                            14
The following lemma states the correctness of the procedure is closed for cases 2(b-d).

Lemma 5.9 (Stuck Invalidity). Given κ∧π ⊢ ∆′ in NF, it is invalid if procedure
is closed returns invalid for cases 2(b-d).

A bad model of the κ∧π is a counter-model. Cases 2b) and 2c) show that the heaps
of bad models are not connected and thus accordingly to conditions C1 and C2, any
model of the LHS could not be a model of the RHS. Case 2d) shows that heaps of
the two sides could not be matched. Now, we show the correctness of Case 2(a) of
procedure is closed and invalidity is preserved during the proof search in ω-ENT.
Proposition 5.10 (Invalidity Preservation). If ω-ENT is stuck, the input is invalid.

Theorem 5.11. QF ENT−SLLIN is decidable.


6 Implementation and Evaluation

We implement S2SLin using OCaml. This implementation is an instantiation of a general
framework for cyclic proofs. To discharge satisfiability for a separation logic formula,
we utilize the cyclic proof systems to derive bases for inductive predicates in the de-
cidable fragment shown in [24]. For those formulas beyond this fragment, we use the
solver presented in [27,29]. We also develop a built-in solver for discharging equalities.
    We evaluated S2SLin to show that i) it can discharge problems in SHLIDe effectively;
and ii) its performance is compatible to the state-of-the-art solvers.

Experiment settings We have evaluated S2SLin on entailment problems taken from SL-
COMP 2022 [36], a competition of separation logic solvers. We take the problems in
two divisions of the SL-COMP 2022, qf shls entl and qf shlid entl, and one new divi-
sion qf shlid2 entl. All these problems semantically belongs to our decidable fragment
and their syntax are written in SMT 2.6 format [37].

 – Division qf shls entl includes 296 entailment problems, 122 invalid problems and
   174 valid problems, with only singly linked lists. They were randomly generated
   by the authors in [31].
 – Division qf shlid entl contains 60 entailment problems which were mostly hand-
   crafted by the authors in [15]. They include singly-linked lists, doubly-linked lists,
   lists of singly-linked lists or skip lists. Furthermore, the system of inductive predi-
   cates must satisfy the following condition: For two different predicates P, Q in the
   system of definitions, either P ≺∗P Q or Q ≺∗P P.
 – In the third division, we introduce new benchmarks, with 27 problems, that are
   beyond the problems in the previous two divisions. In particular, in every system of
   predicate definitions, there exist two predicates P, Q such that they are semantically
   equivalent. We have submitted this division to the Github repository of SL-COMP.

    To evaluate S2SLin ’s performance, we compared it with the state-of-the-art tools
such as CyclistSL [5], Spen [15], Songbird [38], SLS [39] and Harrsh [23]. We did not
include Cycomp [40], as these benchmarks are beyond its decidable fragment. Note

                                           15
                              Table 1: Experimental results
    Tool         qf shls entl            qf shlid entl          qf shlid2 entl
           invalid valid Time invalid valid Time invalid valid Time
            (122) (174) (296)       (24)     (36)      (60) (14)     (13)     (27)
    SLS       12     174 507m42s      2       35 133m28s     0        11 97m54s
    Spen     122     174 10.78s      14       13      3.44s  8         2     1.69s
 CyclistSL    0       58 1520m5s      0       24 360m38s     0         3    240m3s
   Harrsh     39     116 425m19s     18       27 53m56s      8         7 156m45s
 Songbird     12     174 237m25s      2       35 40m38s      0        12 47m11s
   S2SLin    122     174      6.22s  24       36      0.96s  14       13     1.20s


that CyclistSL , Songbird and SLS are not complete; for non-valid problems, while
CyclistSL returns unknown, Songbird, and SLS use some heuristic to guess the out-
come. For each division, we report the number of correct outputs (invalid, valid)
and the time (in minutes and seconds) taken by each tool. Note that we use the sta-
tus (invalid, valid) annotated with each problem in the SL-COMP benchmark as the
ground truth. If an output is the same with the status, we classify it as correct; otherwise,
it is marked as incorrect. We also note that in these experiments we used the competi-
tion pre-processing tool [37] to transform the SMT 2.6 format into the corresponding
formats of the tools before running them. All experiments were performed on a machine
with Intel Core i7-6700 CPU 3.4Gh and 8GB RAM. The CPU timeout is 600 seconds.

Experiment results The experimental results are reported in Table 1. In this table, the
first column presents the names of the tools. The next three columns show the results of
the first division including the number of correct invalid outputs, the number of correct
valid outputs and the time taken (where m for minutes and s for seconds), respectively.
In the third row, the number between each pair of brackets (...) shows the number of
problems in the corresponding column. Similarly, the next two groups of six columns
describe the results of the second and third divisions, respectively.
     In general, the experimental results show that S2SLin is the one (and only one)
that could produce all the correct results. Other solvers either produced wrong re-
sults or could discharge a fraction of the experiments. Moreover, S2SLin took a short
time for the experiments (8.38 seconds compared to 15.91 seconds for Spen, 324 min-
utes for Songbird, 635 minutes for Harrsh, 739 minutes for SLS and 2120 minutes
for CyclistSL ). While SLS returned 14 false negatives, Spen reported 20 false posi-
tives. CyclistSL , Songbird and Harrsh did not produce any wrong result. Of 569 tests,
while CyclistSL could handle 85 tests (15%), Harrsh could handle 215 tests (38%) and
Songbird could decide 235 tests (41.3%). In total of 223 valid tests, while CyclistSL
could handle 85 problems (38%), Songbird could decide 222 problems (99.5%).
     Now we examine the results for each division in details. For qf shls entl, Spen re-
turned all correct, Songbird 186, Harrsh 155, and CyclistSL 58. If we set the timeout to
2400 seconds, both Songbird and Harrsh produced all the correct results. For division
qf shlid entl includes 24 invalid problems and 36 valid problems. While Songbird
produced 37 problems correctly, CyclistSL produced 24 correct results. Spen reported
27 correct results and 13 false positives (skl2−vc{01 − 04} skl3−vc01, skl3−vc{03 −

                                             16
10}). For the last division qf shlid2 entl includes 14 invalid test problems and 13 valid
test problems. While Songbird decided only 12 problems correctly, CyclistSL produced
3 correct outcomes. Spen reported 10 correct results. However, it produced 7 false pos-
itives (ls−mul−vc{01 − 03}, ls−mul−vc05, nll−mul−vc{01 − 03}).
    Since our experiments provide break-down results of the two divisions of SL-COMP
competition, we hope that they provide an initial understanding of the SL-COMP bench-
marks and tools. Consequently, this might reduce the effort to prepare experiments over
these benchmarks to evaluate new SL solvers. Finally, one might point out that S2SLin
performed well because the entailments in the experiments are within its scope. We
do not totally disagree with this argument, but would like to emphasize that tools do
not always work well on favorable benchmarks. For example, Spen introduced wrong
results on qf shlid entl, and Harrsh did not handle qf shlid entl and qf shlid2 entl well
although these problems are in their decidable fragments. We believe that engineering
design and effort play an important role along side with theory development.


7 Related Work

S2SLin is a variant of the cyclic proof systems [3,5,4,26] and [40]. Unlike existing
cyclic proof systems, the soundness of S2SLin is local, and the proof search is not back-
tracking. The work presented in [40] shows the completeness of the cyclic proof system.
Its main contribution is the introduction of rule ∗ for those entailments with disjunction
in the RHS obtained from predicate unfolding. In contrast to [40], our work includes
normalization to soundly and completely avoid disjunction in the RHS during unfold-
ing. Our work also presents how to obtain the global soundness condition for cyclic
proofs. Moreover, our decidable fragment SHLIDe is non-overlapping to the cone pred-
icates introduced in [40]. Furthermore, due to the empty heap in the base cases, the
matching rule in [40] cannot be applied to the predicates in SHLIDe.
     Our work relates to the inductive theorem provers introduced in [10], [38] and
Smallfoot [2]. While [10] is based on structural induction, [38] is based on mathemat-
ical induction. Smallfoot [2] proposed a decision procedure for a fragment with linked
lists and trees (and without arithmetic). To handle inductive entailments, this system
made use of a fixed compositional rule as consequences of induction reasoning. This
technique was further explored by the authors in [31]. Compared with Smallfoot, our
proof system replaces the compositional rule by the combination of rule LInd and the
back-link construction. In doing so, our system could support induction reasoning on a
much more expressive fragment of inductive predicates.
     Our proposal also relates to works that use lemmas as consequences of induction
reasoning [2,16,28,39]. These works in [16,25,28,39] automatically generate lemmas
for some classes of inductive predicates. S2 [25] generated lemmas to normalize (such
as split, equivalence) the shapes of the synthesized data structures. [16] proposed to gen-
erate several sets of lemmas not only for compositional predicates, but also for different
predicates (e.g., completion lemmas, stronger lemmas and static parameter contraction
lemmas). To prove an entailment, SLS [39] aims to infer general lemmas. Similarly,
S2 ENT [28] solves a more generic problem, frame inference, using cyclic proofs and
lemma synthesis. It first infers shape-based residual frame in the LHS and then synthe-

                                            17
sizes the pure constraints over the two sides. It would be a future work to integrate the
pure constraint synthesis into S2SLin to support non-local pure properties.
    S2SLin relates to model-based decision procedures that reduce the entailment prob-
lem in separation logic to a well-studied problem in other domains. For instance, in
[8,11,17] the entailment problem including singly-linked lists and their invariants is
reduced to the problem of inclusion checking in a graph theory. The authors in [18]
reduced the entailment problem to the satisfiability problem in second-order monadic
logic. This reduction could handle an expressive fragment of spatial-based predicates,
called bounded-tree width. Recently, the work presented in [23] show a model-based de-
cision procedure for a subfragment of the bounded-tree width. Furthermore, while the
work in [15,19] reduced the entailment problem to the tree automata inclusion checking
problem, [21] presented an idea to reduce the problem to the heap automata inclusion
checking problem. Moreover, while the procedure in [15] supported well compositional
predicates (single and double links), the procedure in [19] could handle predicates
satisfying local properties (e.g., trees with parent pointers). Our decidable fragment
subsumes the one described in [2,11,15] but is incompatible to the ones presented in
[8,17,18,19]. Works in [32] and [33,34] reduced the entailment problem in separation
logic into the satisfiability problem in SMT. While GRASShoper [33,34] could han-
dle transitive closure pure properties, S2SLin is capable of supporting local ones. Unlike
GRASShoper, which reduces entailment into SMT problems, S2SLin reduces an entail-
ment to admissible entailments and detects repetitions via cyclic proofs.
    Our work relates to decidable fragments and complexity results of the entailment
problem in separation logic with inductive predicates. The entailment is 2-EXPTIME
in cone predicates [40], the bounded tree width predicates and beyond [18,14], and
EXPTIME in a sub-fragment of cone predicates [19]. In the other class, entailment is
in polynomial time for singly-linked lists [11], semantically linear inductive predicates
[15], and its extensions with arithmetic [17] (but becomes EXPTIME when the lists are
extended with double links [8]). Our fragment (with nested lists, trees and arithmetic
properties) is roughly in the “middle” of the two classes above where the entailment is
EXPTIME and becomes polynomial under the upper bound restriction.


8 Conclusion

We have presented a novel decision procedure for the quantifier-free entailment prob-
lem in separation logic combining with inductive definitions of compositional predi-
cates and pure properties. Our proposal is the first complete cyclic proof system for the
problem in separation logic without back-tracking. We have implemented the proposal
in S2SLin and evaluated it over the set of nontrivial entailments taken from the SL-
COMP competition. The experimental results show that our proposal is both effective
and efficient when compared against the state-of-the-art solvers.
    For future work, we plan to combine this proposal with the cyclic frame inference
procedure presented in [28] for a bi-abductive procedure. This is a basic step to obtain
a compositional shape analysis beyond the lists and trees. Another work is to formally
prove that our system is as strong as Smallfoot in the decidable fragment with lists and
trees [2]: Given an entailment, if Smallfoot can produce a proof, so is S2SLin .

                                           18
References
 1. Timos Antonopoulos, Nikos Gorogiannis, Christoph Haase, Max Kanovich, and Joël Ouak-
    nine. Foundations for decision problems in separation logic with general inductive predi-
    cates. In Anca Muscholl, editor, Foundations of Software Science and Computation Struc-
    tures, pages 411–425, Berlin, Heidelberg, 2014. Springer Berlin Heidelberg.
 2. J. Berdine, C. Calcagno, and P. W. O’Hearn. Symbolic Execution with Separation Logic. In
    APLAS, volume 3780, pages 52–68, November 2005.
 3. J. Brotherston. Cyclic proofs for first-order logic with inductive definitions. In Proceedings
    of TABLEAUX-14, volume 3702 of LNAI, pages 78–92. Springer-Verlag, 2005.
 4. J. Brotherston, N. Gorogiannis, and R. L. Petersen. A generic cyclic theorem prover. In
    Proceedings of APLAS-10, LNCS, pages 350–367. Springer, 2012.
 5. James Brotherston, Dino Distefano, and Rasmus Lerchedahl Petersen. Automated cyclic
    entailment proofs in separation logic. In Proceedings of the 23rd International Conference on
    Automated Deduction, CADE’11, page 131–146, Berlin, Heidelberg, 2011. Springer-Verlag.
 6. Cristiano Calcagno, Dino Distefano, Jeremy Dubreil, Dominik Gabi, Pieter Hooimeijer, Mar-
    tino Luca, Peter O’Hearn, Irene Papakonstantinou, Jim Purbrick, and Dulma Rodriguez.
    Moving fast with software verification. In Klaus Havelund, Gerard Holzmann, and Ra-
    jeev Joshi, editors, NASA Formal Methods, pages 3–11, Cham, 2015. Springer International
    Publishing.
 7. Cristiano Calcagno, Dino Distefano, Peter W. O’Hearn, and Hongseok Yang. Compositional
    shape analysis by means of bi-abduction. In POPL, pages 289–300, 2009.
 8. Taolue Chen, Fu Song, and Zhilin Wu. Tractability of Separation Logic with Inductive
    Definitions: Beyond Lists. In Roland Meyer and Uwe Nestmann, editors, 28th International
    Conference on Concurrency Theory (CONCUR 2017), volume 85 of Leibniz International
    Proceedings in Informatics (LIPIcs), pages 37:1–37:17, Dagstuhl, Germany, 2017. Schloss
    Dagstuhl–Leibniz-Zentrum fuer Informatik.
 9. W.-N. Chin, C. Gherghina, R. Voicu, Q.-L. Le, F. Craciun, and S. Qin. A specialization
    calculus for pruning disjunctive predicates to support verification. In CAV. 2011.
10. Duc-Hiep Chu, Joxan Jaffar, and Minh-Thai Trinh. Automatic induction proofs of data-
    structures in imperative programs. In Proceedings of PLDI, PLDI ’15, pages 457–466, New
    York, NY, USA, 2015. ACM.
11. B. Cook, C. Haase, J. Ouaknine, M. Parkinson, and J. Worrell. Tractable reasoning in a
    fragment of separation logic. In CONCUR, volume 6901, pages 235–249. 2011.
12. Christopher Curry, Quang Loc Le, and Shengchao Qin. Bi-abductive inference for shape
    and ordering properties. In 2019 24th International Conference on Engineering of Complex
    Computer Systems (ICECCS), pages 220–225, 2019.
13. Dino Distefano, Manuel Fähndrich, Francesco Logozzo, and Peter W. O’Hearn. Scaling
    static analyses at facebook. Commun. ACM, 62(8):62–70, jul 2019.
14. Mnacho Echenim, Radu Iosif, and Nicolas Peltier. Unifying decidable entailments in separa-
    tion logic with inductive definitions. In Automated Deduction-CADE 28-28th International
    Conference on Automated Deduction, Virtual Event, July 12-15, 2021, Proceedings, pages
    183–199, 2021.
15. Constantin Enea, Ondrej Lengál, Mihaela Sighireanu, and Tomás Vojnar. Compositional
    entailment checking for a fragment of separation logic. Formal Methods in System Design,
    51(3):575–607, 2017.
16. Constantin Enea, Mihaela Sighireanu, and Zhilin Wu. On automated lemma generation for
    separation logic with inductive definitions. ATVA, 2015.
17. Xincai Gu, Taolue Chen, and Zhilin Wu. A Complete Decision Procedure for Linearly Com-
    positional Separation Logic with Data Constraints, pages 532–549. Springer International
    Publishing, Cham, 2016.


                                               19
18. R. Iosif, A. Rogalewicz, and J. Simácek. The tree width of separation logic with recursive
    definitions. In CADE, pages 21–38, 2013.
19. Radu Iosif, Adam Rogalewicz, and Tomás Vojnar. Deciding entailments in inductive sepa-
    ration logic with tree automata. ATVA, 2014.
20. S. Ishtiaq and P.W. O’Hearn. BI as an assertion language for mutable data structures. In
    ACM POPL, pages 14–26, London, January 2001.
21. Christina Jansen, Jens Katelaan, Christoph Matheja, Thomas Noll, and Florian Zuleger. Uni-
    fied Reasoning About Robustness Properties of Symbolic-Heap Separation Logic, pages 611–
    638. Springer Berlin Heidelberg, Berlin, Heidelberg, 2017.
22. Katelaan Jens, Jovanovic Dejan, and Weissenbacher Georg. A separation logic with data:
    Small models and automation. In IJCAI, 2018.
23. Jens Katelaan, Christoph Matheja, and Florian Zuleger. Effective entailment checking for
    separation logic with inductive definitions. In Tomáš Vojnar and Lijun Zhang, editors, Tools
    and Algorithms for the Construction and Analysis of Systems, pages 319–336, Cham, 2019.
    Springer International Publishing.
24. Quang Loc Le. Compositional satisfiability solving in separation logic. In Fritz Henglein,
    Sharon Shoham, and Yakir Vizel, editors, Verification, Model Checking, and Abstract Inter-
    pretation, pages 578–602, Cham, 2021. Springer International Publishing.
25. Quang Loc Le, Cristian Gherghina, Shengchao Qin, and Wei-Ngan Chin. Shape analysis via
    second-order bi-abduction. In CAV, volume 8559, pages 52–68. 2014.
26. Quang Loc Le and Mengda He. A decision procedure for string logic with quadratic equa-
    tions, regular expressions and length constraints. In Sukyoung Ryu, editor, Programming
    Languages and Systems, pages 350–372, Cham, 2018. Springer International Publishing.
27. Quang Loc Le, Jun Sun, and Wei-Ngan Chin. Satisfiability modulo heap-based programs.
    In CAV. 2016.
28. Quang Loc Le, Jun Sun, and Shengchao Qin. Frame inference for inductive entailment proofs
    in separation logic. In Dirk Beyer and Marieke Huisman, editors, Tools and Algorithms for
    the Construction and Analysis of Systems, pages 41–60, 2018.
29. Quang Loc Le, Makoto Tatsuta, Jun Sun, and Wei-Ngan Chin. A decidable fragment in
    separation logic with inductive predicates and arithmetic. In CAV, pages 495–517, 2017.
30. Scott McPeak and George C. Necula. Data structure specifications via local equality axioms.
    In Kousha Etessami and Sriram K. Rajamani, editors, Computer Aided Verification, pages
    476–490, Berlin, Heidelberg, 2005. Springer Berlin Heidelberg.
31. Juan Antonio Navarro Pérez and Andrey Rybalchenko. Separation logic + superposition
    calculus = heap theorem prover. In Proceedings of the 32nd ACM SIGPLAN Conference on
    Programming Language Design and Implementation, PLDI ’11, page 556–566, New York,
    NY, USA, 2011. Association for Computing Machinery.
32. JuanAntonio Navarro Pérez and Andrey Rybalchenko. Separation logic modulo theories. In
    APLAS, volume 8301, pages 90–106. 2013.
33. R. Piskac, T. Wies, and D. Zufferey. Automating separation logic using smt. In Natasha
    Sharygina and Helmut Veith, editors, CAV, volume 8044, pages 773–789. 2013.
34. Ruzica Piskac, Thomas Wies, and Damien Zufferey. Automating separation logic with trees
    and data. In CAV, volume 8559, pages 711–728. 2014.
35. J. Reynolds. Separation Logic: A Logic for Shared Mutable Data Structures. In IEEE LICS,
    pages 55–74, 2002.
36. Mihaela Sighireanu and Quang Loc Le. SL-COMP 2022. https://sl-comp.github.io/, 2022.
    [Online; accessed Jun-2022].
37. Mihaela Sighireanu, Juan Antonio Navarro Pérez, Andrey Rybalchenko, Nikos Gorogiannis,
    Radu Iosif, Andrew Reynolds, Cristina Serban, Jens Katelaan, Christoph Matheja, Thomas
    Noll, Florian Zuleger, Wei-Ngan Chin, Quang Loc Le, Quang-Trung Ta, Ton-Chanh Le,


                                               20
    Thanh-Toan Nguyen, Siau-Cheng Khoo, Michal Cyprian, Adam Rogalewicz, Tomás Vojnar,
    Constantin Enea, Ondrej Lengál, Chong Gao, and Zhilin Wu. SL-COMP: competition of
    solvers for separation logic. In Tools and Algorithms for the Construction and Analysis of
    Systems - 25 Years of TACAS: TOOLympics, pages 116–132, 2019.
38. Quang-Trung Ta, Ton Chanh Le, Siau-Cheng Khoo, and Wei-Ngan Chin. Automated mu-
    tual explicit induction proof in separation logic. In John Fitzgerald, Constance Heitmeyer,
    Stefania Gnesi, and Anna Philippou, editors, FM 2016: Proceedings, pages 659–676, 2016.
39. Quang-Trung Ta, Ton Chanh Le, Siau-Cheng Khoo, and Wei-Ngan Chin. Automated lemma
    synthesis in symbolic-heap separation logic. POPL, 2018.
40. Makoto Tatsuta, Koji Nakazawa, and Daisuke Kimura. Completeness of cyclic proofs for
    symbolic heaps with inductive definitions. In Anthony Widjaja Lin, editor, Programming
    Languages and Systems, pages 367–387, Cham, 2019. Springer International Publishing.




                                              21
                               σ= ◦ {v̄i /p̄i | p̄i ∈ w̄ ∧ p̄i 6=null}
         x7→c(v̄)∗κ1 ∧π1 ∧x6=F ⊢ (∃(w̄\p̄).x7→c(p̄)∗κ′ ∗P(w,F ,B̄,u,sc′ ,tg)∧π0 )σ∗κ2 ∧π2
RInd                                                                                            †
                        x7→c(v̄)∗κ1 ∧π1 ∧x6=F ⊢ P(x,F ,B̄,u,sc,tg)∗κ2 ∧π2

         (∃(w̄\p̄).x7→c(p̄)∗κ′ ∗P(w,F ,B̄,u,sc′ ,tg)k+1 ∧π0 )∗κ1 ∧π1 ∧x6=F3
              ⊢ Q(x,F3 ,B̄,u,sc,tg2 )∗κ2 ∧π2
LInd                                                                          P(x,F ,B̄,u,sc,tg)6∈κ2
         P(x,F ,B̄,u,sc,tg)k ∗κ1 ∧π1 ∧x6=F3 ⊢ Q(x,F3 ,B̄,u,sc,tg2 )∗κ2 ∧π2

                        Fig. 5: Reduction Ruleswhere †: x7→c(v̄)6∈κ2



A       Reduction Rules for Compositional Predicates in General Form

In Figure 5, we present rules RInd1 and LInd for the following definitions of composi-
tional predicates:

P(x,F ,B̄,u,sc,tg) ≡ emp∧x=F ∧sc=tg ∨ ∃w̄.x7→c(p̄)∗κ′ ∗P(w,F ,B̄,u,sc′ ,tg)∧π0 ;

where w̄ are fresh variables.
     To define SHLIDe base in a general form, we further assume every heap cells ci ∈
Node used in definitions of compositional predicates P(r,F ,B̄,u,sc,tg) are defined in
the form of data ci {ci next; ci1 down1 ; ...; cij downj ; τu udata; τs scdata} where
ci1 , .., cij ∈ Node, down1 ,..., downj fields are for the nested structures in the matrix
heaps, udata field is for the transitivity data, and scdata field are for ordering data.
Then, SHLIDe base of an occurrence of the compositional predicates is defined as:

                          def       ¯ tg,u)[v̄/d]∧π
                                               ¯ 0 [tg/scd] ∗ κ′ ([v̄/d]
                                                                      ¯ ◦ [tg/scd])
       P(E,F ,B̄,u,sc,tg) = E7→c(F ,d,


B Proof of Corollary 5.1

Proof. We need to show that the premises in rule RInd and rule LInd are quantifier-free.
The condition C1 in section 2.1 ensures that w̄ ⊆ p̄. Hence, w̄ \ p̄ ≡ ∅. Thus, the RHS
of the premise in RInd and the LHS of the premise in LInd are quantifier-free.


C       Proof of Soundness

We show the correctness of the soundness of the proof system.


C.1 Soundness of proof rules: Lemma 5.2

For each rule, we show that if all the premises hold, so is the conclusion

                                                22
Rule Subst . First, we consider the case E is a variable. Suppose ∆[v/x] ⊢ ∆′ [v/x].
That is for any s, h, if s, h |= ∆[v/x] then s, h |= ∆′ [v/x]. As x 6∈ FV(∆[v/x]), we
extend the domain of stack with x as: s′ = s[x7→s(v)]. As so, s′ , h |= ∆ ∧ v = x and
s′ , h |= ∆′ . Therefore ∆ ∧ v = x |= ∆′ holds.
      The case E is null is similar.

Rule ExM For simplicity, we assume that E1 and E2 are both variables. Suppose ∆ ∧
v1 = v2 ⊢ ∆′ and ∆ ∧ v1 6= v2 ⊢ ∆′ .
   Suppose s, h |= ∆.

 – Case 1: if s(v1 ) = s(v2 ) then s, h |= ∆∧v1 = v2 . As ∆∧v1 = v2 ⊢ ∆′ , s, h |= ∆′ .
 – Case 1: if s(v1 ) 6= s(v2 ) then s, h |= ∆∧v1 6= v2 . As ∆∧v1 6= v2 ⊢ ∆′ , s, h |= ∆′ .

Rule =L, rule =R, and rule Hypothesis Trivial.

Rule LBase and rule RBase based on the fact that given a compositional predicate
P(E,F ,B̄,u,sc,tg) where F is a dangling pointer, then P(E,E,B̄,u,sc,tg) implies the
base rule with emp heap predicate.

Rule 6=null Follows semantics of points-to predicate where null 6∈ Loc.

Rule 6=∗ Follows semantics of the spatial conjunction ∗.

Rule ∗ Suppose κ1 ∧ π |= κ2 ∧ π ′ and κ ∧ π |= κ′ ∧ π ′ .
     For any s, h1 |= κ1 ∧ π, s, h1 |= κ2 ∧ π ′ . And any s, h2 |= κ ∧ π, s, h2 |= κ′ ∧ π.
as roots(κ1 ) ∩ roots(κ) = ∅ dom(h1 ) ∩ dom(h2 ) = ∅. Hence s, h1 ḣ2 |= κ1 ∗ κ2 ∧ π
(a). Similarly, s, h1 ḣ2 |= κ2 ∗ κ′ ∧ π ′ (b).
     From (a), (b), κ1 ∗ κ2 ∧ π |= κ2 ∗ κ′ ∧ π ′ .

Rule LInd and RInd . Based on the least semantics of the inductive predicates and the
base case could not happen due to constraint x 6= F in RInd (respectively x 6= F3 in
LInd).


C.2 Global Soundness: Lemma 5.3
As our system always generates back-links with progressing points (via rule LInd), there
are infinitely progressing points in any infinite trace.
    We now show that all cycles are pairwise disjoint (such that in the path between a
companion and a bud of every back-link, no rule can ever “delete” an inductive predicate
formula on which the soundness relies). We prove by contradiction.
    In intuition, the soundness replies on a pair of inductive predicates in a sub-term
relationship. Given an inductive predicate P(E,F ,B̄,v̄) only rule ExM is able to generate
the constraint E=F such that P(E,F ,B̄,v̄) can be transformed into P(F ,F ,B̄,v̄ ′ ) via
rule Subst and finally eliminated by rule LBase. We now show that every companion
node of a back-link involving a bud that is in the branch E6=F of rule ExM is below the
node including the applications of rule ExM.

                                           23
                             ∆0

                 ∆1                       ∆♣
                                           2

                                                 ....
                                   ∆7
                                                        ∆3
                                                             ...

                                                                   ∆4
                                                             ...        ...

                                                        ∆5                    ∆♣
                                                                               6


                      Fig. 6: An Example of Non-Disjoint Back-Links.


    Assume that our system generates back-links with non-disjoint cycles. Two cycles
are non-disjoint only when their both companion nodes are above at least one branch
(applications of rule ExM). The non-disjoint cycles is similar to the one as shown in the
proof tree in Fig. 6 where there is no branch in the path between ∆2 and ∆3 . (The proof
for the case where ∆5 is linked with ∆2 and ∆6 is linked with ∆3 is similar. We discuss
this proof below.)
    We prove the contradiction by case analysis on the pair of variables E1 and E2
applied with rule ExM at node ∆4 . As ExM is applied to introduce G(op(E)) for every
op(E) in the LHS of entailments. We proceed case analysis on op(E).

 1. Case 1. op(E) ≡ E7→ and ExM at node ∆4 does case split E=null and E6=null
    to obtain two children. Assume that the left child (on the path from ∆4 to ∆5 ) is
    ∆4 ∧E=null. After substitution, LHS of this node is reduced to ∆′4 ∗ null7→
    which is equivalent to false . Thus, the back-link from ∆5 to ∆3 could not estab-
    lished.
 2. Case 2. op(E) ≡ P(E,F ,B̄,v̄) and ExM at node ∆4 does case split E=F and
    E6=F to obtain two children. Assume that the left child (on the path from ∆4
    to ∆5 ) is ∆4 ∧E=F . After substitution, LHS of this node is reduced to ∆′4 ∗
    P(F ,F ,B̄,v̄ ′ ). In turn, this entailment is applied with normalization rule LBase to
    eliminate P(F ,F ,B̄,v̄ ′ ). Next, we consider two sub-cases of the inductive predicate
    in any application of rule LInd applied into a node between ∆3 and ∆5 .
    (a) the predicate applied is P(E ′ ,F ,B̄,v̄) . We note that in the recursive rule of
         definitions of compositional predicates

        ∃X,sc′ ,d1 ,d2 .x7→c(X,d1 ,d2 ,u,sc)∗Q1 (d1 ,B)∗Q2 (d2 ,X)∗P(X,F ,B̄,u,sc′ ,tg)∧π0

        all nested predicates Q1 , Q2 are syntactically different to P . ∆5 is missing one
        occurrence of predicate P . Hence, it could not be linked back to ∆3 .
    (b) the predicate applied is Q(E ′ ,F ′ ,F ,v̄ ′ ) such that P(U ,F ,B̄,u′ ,sc′ ,tg ′ ) is a nested
        predicate in the definition of Q. However, u′ , tg ′ are fresh variables and in any

                                                 24
        back-links they are never substituted to become u and tg, respectively. Hence,
        ∆5 could not be linked back to ∆3 .
 3. Case 3. op(E) ≡ tree(E,B̄,v̄) and ExM at node ∆4 does case split E=null and
    E6=null to obtain two children. As LInd only applies for compositional predicates,
    tree(E,B̄,v̄) could not be a fresh formula. It has been normalised in ∆3 already.
    This case could not be occurred.

   The proof for the case where ∆5 is linked with ∆2 and ∆6 is linked with ∆3 is
similar. The main difference is that we need to show that predicate P(E,F ,B̄,v̄) is a
sub-formula of ∆2 in the proof of Case 2 like above. That means P(E,F ,B̄,v̄) has not
been eliminated by rule ExM in the path between ∆2 ∆3 . This is straightforward as no
branch exists in the path between ∆2 and ∆3 .


D     Proofs of Termination

D.1   Proof of Lemma 5.4

Proof. Termination of our system is based on the size of an entailment which is defined
as:

Definition 6 (Size) The size of an entailment e:κa ∧φa ∧aa ⊢ κc ∧φc ∧ac is a triple of:

 1. Np −np where Np is the maximal number of both points-to predicates and occur-
    rences of inductive predicates that the RHS of any entailments derived (by ω-ENT)
    from e may contain, and np is the total number of both points-to predicates and
    occurrences of inductive predicates in κc .
 2. Ne −ne where Ne is the maximal number of both disequalities and non-trivial
    equalities that the LHS of any entailments derived (by ω-ENT) from e may con-
    tain, and ne is the number of both disequalities and non-trial equalities in φa .
 3. the sum of the length of κa ∧φa ∧aa ⊢ κc ∧φc ∧ac , where length is defined in the
    obvious way taking all simple formulas to have length 1.
 4. Na : the number of constraints on arithmetic properties generated by the recursive
    rules of inductive definition.

    If Np and Ne are bounded, applying any rules except LInd makes progress since the
size of each premise of any rule application is lexicographically less than the size of the
conclusion. Np and Na rely on the number of applications of rule LInd. Ne depends on
the number applications of rule ExM. In turn, the application of ExM relies on the number
of spatial variables. Thus, Ne also relies on the number applications of rule LInd. To
show the termination, we show that the number applications of rule LInd is bounded. In
consequence, this bound is achieved if the number of applications of ∗ is finite. As the
number of inductive symbols as their arities are finite, rule ∗ indeed generates a finite
number of equivalent classes of entailments in which two entailments in the same class
are equivalent after some substitution. Thus, all entailments in the same class are linked
back together through a finite number of steps.

                                            25
D.2   Proof of Lemma 5.5

Suppose we have an entailment P(E,F ,B̄,v̄)k ∗ κ∧π ⊢ κ′ ∧π ′ . If π 6 |=π ′ then exhaus-
tively applying rule ExM our system decides it as invalid through the base cases like
E=F .
    If π|=π ′ , then our system applies rule Hypothesis to obtain P(E,F ,B̄,v̄)k ∗κ∧π ⊢ κ′ .
Hence, in the following proof, we only consider the later form of the entailment in con-
clusion of rule LInd.
    Without loss of generality, we assume P includes 4 predicates definitions: P1 , P2 ,
Q1 and Q2 where P1 ≺P P2 (that is the recursive branch of predicate definition P2 contains
one and only one occurrence of predicate P1 and P1 is self-recursive), Q1 ≺P Q2 (that is
the recursive branch of predicate definition Q2 contains one and only one occurrence
of predicate Q1 and Q1 is self-recursive), P1 6≺P Q1 , P1 6≺P Q2 , P2 6≺P Q1 , and P2 6≺P Q2 . For
instance, the definitions of these predicates could be as follows.

pred P1 (r,F ,u) ≡ emp∧r=F
   ∨ ∃X,sc′ .r7→c1 (X, ,u, , ) ∗ P1 (X,F ,u)∧r6=F ∧a1
pred P2 (r,F ,B1 ,u,sc,tg) ≡ emp∧r=F ∧sc=tg
   ∨ ∃X,d,u′ ,sc′ .r7→c1 (X,d,u,u′ ,sc′ )∗P1 (d,B,u′ )∗ P2 (X,F ,B1 ,u,sc′ ,tg)∧r6=F ∧a2
pred Q1 (r,F ,u) ≡ emp∧r=F
   ∨ ∃X,sc′ .r7→c2 (X, ,u, , ) ∗ Q1 (X,F ,u)∧r6=F ∧a3
pred Q2 (r,F ,B1 ,u,sc,tg) ≡ emp∧r=F ∧sc=tg
   ∨ ∃X,d,u′ ,sc′ .r7→c2 (X,d,u,u′ ,sc′ )∗Q1 (d,B,u′ )∗ Q2 (X,F ,B1 ,u,sc′ ,tg)∧r6=F ∧a4

    We notice that in the definitions of P2 and Q2 , we assume that in the recursive rule sc′
is a variable of a field of the root points-to predicate. In general, it may be a parameter
of P2 and Q2 as well.
    If the input entailment is in NF and of the form: P(x,F ,B̄,u,sc,tg)0 ∗ ∆⊢∆′ and
there does not exist an occurrence of inductive predicate Q(x,F2 ,B̄,...) ∈ ∆′ then this
entailment satisfy the case 2c in Sect. 4.1 and is classified as invalid immediately.
Thus, the Lemma holds. In the rest, to prove this Lemma, we only need to consider the
application of rule LInd where the entailment is in NF and of the form in the conclusion
of LInd as:

         e0 : P(x,F ,B,u,sc,tg)0 ∗κ∧π∧x6=F ∧x6=F2 ⊢ Q(x,F2 ,B,u,sc,tg2 )∗κ′

Furthermore, it is safe to assume that P(x,F ,B̄,u,sc,tg)0 is the only one with the
smallest unfolding number (i.e., 1) in the LHS of e0 could be applied with rule
LInd. We prove it by the structural induction on the number of occurrences of inductive
predicates in the LHS of the input entailment. We do case splits.


D.3   Case 1: P and Q have the same definition.

We consider two cases where the definition contains nested structures or not.

                                               26
Case 1.1 For the simpliest scenario, we assume both definitions of P and Q are self-
recursive and do not contain nested structures i.e., P ≡ Q ≡ P1 . Then, e0 becomes:

                e11 : P1 (x,F ,u)0 ∗κ∧π∧x6=F ∧x6=F2 ⊢ P1 (x,F2 ,u)∗κ′
After applied with rule LInd, our system generates a premise as follows.
        e11 1 : x7→c1 (X,d,u,sc′ ,uprm)∗P1 (X,F ,u)1 ∗κ∧π∧x6=F ∧x6=F2 ∧a11
                  ⊢ P1 (x,F2 ,u)∗κ′

where X, d, sc′ and uprm are two fresh variables and a11 is the arithmetical contraint
obtained by subsituting actual/formal paramters into the constrtaint a1 of the recursive
rule of the definition of P1 . Next, entailment e11 1 is normalized by applying rule 6=null
to obtain:
   e11 2 : x7→c1 (X,d,u,sc′ ,uprm)∗P1 (X,F ,u)1 ∗κ∧π∧x6=F ∧x6=F2 ∧a11 ∧x6=null
             ⊢ P1 (x,F2 ,u)∗κ′
   Now, e11 2 is applied with rule RInd to obtain:

   e11 3 : x7→c1 (X,d,u,sc′ ,uprm)∗P1 (X,F ,u)1 ∗κ∧π∧x6=F ∧x6=F2 ∧a11 ∧x6=null
           ⊢ x7→c1 (X,d,u,sc′ ,uprm)∗P1 (x,F2 ,u)∗κ′ ∧a11
We note that for completeness applications of rule ∗ are always performed after all other
rules. As so, next, Hypothesis is applied to eliminate the arithmetical constraint in the
RHS to obtain:
        e11 4 : x7→c1 (X,d,u,sc′ ,uprm)∗P1 (X,F ,u)1 ∗κ∧π∧x6=F ∧x6=F2 ∧a11
                  ⊢ x7→c1 (X,d,u,sc′ ,uprm)∗P1 (x,F2 ,u)∗κ′
Our system now applies rules ExM and 6=∗ to normalize the LHS where application of
the latter rule generates two premises.
e11 5 : x7→c1 (X,d,u,sc′ ,uprm)∗P1 (X,F ,u)1 ∗κ∧π∧x6=F ∧x6=F2 ∧a11 ∧x6=null∧X=F
          ⊢ x7→c1 (X,d,u,sc′ ,uprm)∗P1 (x,F2 ,u)∗κ′
e116 : x7→c1 (X,d,u,sc′ ,uprm)∗P1 (X,F ,u)1 ∗κ∧π∧x6=F ∧x6=F2 ∧a11 ∧x6=null∧X6=F
          ∧x6=X ⊢ x7→c1 (X,d,u,sc′ ,uprm)∗P1 (x,F2 ,u)∗κ′
 1. For the premise e11 5 , our system applies rules Subst and L = to eliminate X=F
    and obtain:
     e11 51 : x7→c1 (F ,d,u,sc′ ,uprm)∗P1 (F ,F ,u)1 ∗κ∧π∧x6=F ∧x6=F2 ∧a11 ∧x6=null
                ⊢ x7→c1 (F ,d,u,sc′ ,uprm)∗P1 (x,F2 ,u)∗κ′
    Next, rule LBase is applied to discard the inductive predicate in the LHS and obtain
    the following premise:
            e11 52 : x7→c1 (F ,d,u,sc′ ,uprm)∗κ∧π∧x6=F ∧x6=F2 ∧a11 ∧x6=null
                       ⊢ x7→c1 (X,d,u,sc′ ,uprm)∗P1 (x,F2 ,u)∗κ′
    As the number of inductive predicates in the LHS of e11 52 is reduced, by induction,
    this Lemma holds.

                                            27
 2. For the premise e11 6 , we have two cases.
    (a) If FV(π) ∩ FV(a11 ) = ∅. Our system links e11 6 back to e11 as follows. First,
        it weakens (a.k.a discards) two matched points-to predicates in the two sides
        and the following pure constraints in LHS: x6=F , a11 , x6=null, and x6=X.
        After that, it substitutes the remaining entailment with σ={x/X} to obtain the
        identical entailment with e11 . We notice that as X is a fresh variable, it does
        not apprear in κ∧π and κ′ . Then, the Lemma holds for this case.
    (b) FV(π) ∩ FV(a11 ) 6= ∅. As the substitution [sc/sc′ ] could not be applied, our
        system could not link e11 6 back to e11 . It applies the same the proof search as
        applied for e11 to unfold e11 ′6 . As this time, e11 ′6 contains respective a′11 and
        sc′′ and where a11 = a′11 [sc′ /sc′′ ]. Now, our system could link e11 ′6 back to
        e11 6 .

Case 1.2 For a more general case, we assume P ≡ Q ≡ P2 . Then, e0 becomes:

       e12 : P2 (x,F ,B,u,sc,tg)0 ∗κ∧π∧x6=F ∧x6=F2 ⊢ P2 (x,F2 ,B,u,sc,tg2 )∗κ′

The first four steps are similar to Case 1.1. After applied with rule LInd, our system
generates a premise as follows.

e12 1 : x7→c1 (X,d,u,u′ ,sc′ )∗P1 (d,B,u′ )1 ∗P2 (X,F ,B,u,sc′ ,tg)1 ∗κ∧π∧x6=F ∧x6=F2 ∧a21
          ⊢ P2 (x,F2 ,B,u,sc,tg2 )∗κ′

where a21 is obtaied by substituting actual/formal paramters into the arithmetical con-
traint a2 of the recursive rule of the definition of P2 . Next, this entailment is normalized
by applying rule 6=null to obtain:

e12 2 : x7→c1 (X,d,u,u′ ,sc′ )∗P1 (d,B,u′ )1 ∗P2 (X,F ,B,u,sc′ ,tg)1 ∗κ∧π∧x6=F ∧x6=F2 ∧a21
          ∧x6=null ⊢ P2 (x,F2 ,B,u,sc,tg2 )∗κ′

Next, e12 2 is applied with rule RInd to obtain:

e12 3 : x7→c1 (X,d,u,u′ ,sc′ )∗P1 (d,B,u′ )1 ∗P2 (X,F ,B,u,sc′ ,tg)1 ∗κ∧π∧x6=F ∧x6=F2 ∧a21
          ∧x6=null ⊢ x7→c1 (X,d,u,u′ ,sc′ )∗P1 (d,B,u′ )0 ∗P2 (X,F2 ,B,u,sc′ ,tg2 )∗κ′ ∧a21

We note that rule ∗ is always applied after all other rules. As so, next, Hypothesis is
applied to eliminate the arithmetical constraint in the RHS to obtain:

e12 4 : x7→c1 (X,d,u,u′ ,sc′ )∗P1 (d,B,u′ )1 ∗P2 (X,F ,B,u,sc′ ,tg)1 ∗κ∧π∧x6=F ∧x6=F2 ∧a21
          ∧x6=null ⊢ x7→c1 (X,d,u,u′ ,sc′ )∗P1 (d,B,u′ )0 ∗P2 (X,F2 ,B,u,sc′ ,tg2 )∗κ′

Our system now applies rules ExM and 6=∗ to normalize the LHS. Particularly, applying
rule ExM for d and B generates two premises:

e12 5 : x7→c1 (X,d,u,u′ ,sc′ )∗P1 (d,B,u′ )1 ∗P2 (X,F ,B,u,sc′ ,tg)1 ∗κ∧π∧x6=F ∧x6=F2 ∧a21
          ∧x6=null∧d=B ⊢ x7→c1 (X,d,u,u′ ,sc′ )∗P1 (d,B,u′ )0 ∗P2 (X,F2 ,B,u,sc′ ,tg2 )∗κ′
e12 6 : x7→c1 (X,d,u,u′ ,sc′ )∗P1 (d,B,u′ )1 ∗P2 (X,F ,B,u,sc′ ,tg)1 ∗κ∧π∧x6=F ∧x6=F2 ∧a21
          ∧x6=null∧d6=B ⊢ x7→c1 (X,d,u,u′ ,sc′ )∗P1 (d,B,u′ )0 ∗P2 (X,F2 ,B,u,sc′ ,tg2 )∗κ′

                                             28
 1. For the first premise e12 5 , our system first applies rules Subst to obtain and L =:

      e12 51 : x7→c1 (X,B,u,u′ ,sc′ )∗P1 (B,B,u′ )1 ∗P2 (X,F ,B,u,sc′ ,tg)1 ∗κ∧π∧x6=F ∧x6=F2 ∧a21
                 ∧x6=null ⊢ x7→c1 (X,B,u,u′ ,sc′ )∗P1 (B,B,u′ )0 ∗P2 (X,F2 ,B,u,sc′ ,tg2 )∗κ′

      After that, it applies rules LBase and RBase to eliminate inductive predicates P1 in
      the LHS and RHS, respectively. Afterward, the premise is obtained as:

        e12 53 : x7→c1 (X,B,u,u′ ,sc′ )∗P2 (X,F ,B,u,sc′ ,tg)1 ∗κ∧π∧x6=F ∧x6=F2 ∧a21
                   ∧x6=null ⊢ x7→c1 (X,B,u,u′ ,sc′ )∗P2 (X,F2 ,B,u,sc′ ,tg2 )∗κ′

    Now, it generates a back-link between e12 53 and e12 . Hence, the Lamma holds.
 2. For the second premise e12 6 , the system applies rule 6=∗ and then rule ExM to obtain
    two following premises:

         e12 7 : x7→c1 (X,d,u,u′ ,sc′ )∗P1 (d,B,u′ )1 ∗P2 (X,F ,B,u,sc′ ,tg)1 ∗κ∧π∧x6=F
                 ∧x6=F2 ∧a21 ∧x6=null∧d6=B∧x6=d∧X=F
                   ⊢ x7→c1 (X,d,u,u′ ,sc′ )∗P1 (d,B,u′ )∗P2 (X,F2 ,B,u,sc′ ,tg2 )∗κ′
         e12 8 : x7→c1 (X,d,u,u′ ,sc′ )∗P1 (d,B,u′ )1 ∗P2 (X,F ,B,u,sc′ ,tg)1 ∗κ∧π∧x6=F
                 ∧x6=F2 ∧a21 ∧x6=null∧d6=B∧x6=d∧X6=F
                   ⊢ x7→c1 (X,d,u,u′ ,sc′ )∗P1 (d,B,u′ )∗P2 (X,F2 ,B,u,sc′ ,tg2 )∗κ′

      (a) For the premise e12 7 , our system applies rules Subst and L = first and then rule
          LBase to eliminate inductive predicates P2 in the LHS. Afterward, the premise
          is obtained as:
             e12 73 : x7→c1 (F ,d,u,u′ ,sc′ )∗P1 (d,B,u′ )1 ∗κ∧π∧x6=F
                      ∧x6=F2 ∧a21 ∧x6=null∧d6=B∧x6=d
                        ⊢ x7→c1 (F ,d,u,u′ ,sc′ )∗P1 (d,B,u′ )∗P2 (F ,F2 ,B,u,sc′ ,tg2 )∗κ′

          Similarly to Case 1.1, the Lemma holds for e12 73 .
      (b) For the premise e128 , our system processes similarly to 2 in Case 1.1: the
          predicate in the LHS is unfolded at most two times. Hence, the Lemma holds.

D.4    Case 2: P and Q have different definitions and they are syntactically
       dependent.
We consider two sub-cases. In the first case, we assume P≺P Q. In the second case, we
assume Q≺P P.

Case 2.1: P≺P Q For a general case, we assume P ≡ P′1 and Q ≡ P′2 where P′1 is defined
similarly to P1 except it contains an additional local property (Otherwise, the proof for
P ≡ P1 and Q ≡ P2 is quite trivial.).

pred P′1 (r,F ,u,sc,tg) ≡ emp∧r=F ∧sc=tg
     ∨ ∃X,sc′ .r7→c1 (X, ,u, ,sc′ ) ∗ P′1 (X,F ,u,sc′ ,tg)∧r6=F ∧a1
pred P′2 (r,F ,B1 ,u,sc,tg) ≡ emp∧r=F ∧sc=tg
     ∨ ∃X,d,u′ ,sc′ .r7→c1 (X,d,u,u′ ,sc′ )∗P′1 (d,B,u′ ,sc,tg)∗ P′2 (X,F ,B1 ,u,sc′ ,tg)∧r6=F ∧a2

                                              29
Then, e0 becomes:
       e21 : P′1 (x,F ,B,u,sc,tg)0 ∗κ∧π∧x6=F ∧x6=F2 ⊢ P′2 (x,F2 ,B,u,sc,tg2 )∗κ′
After applying three rules LInd, 6=null and RInd in sequence (and similarly to Case 1.1
and Case 1.2 above), our system generates the following premise.
  e21 3 : x7→c1 (X,d,u,u′ ,sc′ )∗P′1 (X,F ,B,u,sc′ ,tg)1 ∗κ∧π∧x6=F ∧x6=F2 ∧a11
            ⊢ x7→c1 (X,d,u,u′ ,sc′ )∗P′1 (d,B,u′ ,sc,tg)∗P2 (X,F2 ,B,u,sc′ ,tg2 )∗κ′ ∧a21
where X, d, sc′ and u′ are two fresh variables. Our system applies rule ExM for d and B
to generate the following two premises.
  e214 : x7→c1 (X,d,u,u′ ,sc′ )∗P′1 (X,F ,B,u,sc′ ,tg)1 ∗κ∧π∧x6=F ∧x6=F2 ∧d=B∧a11
            ⊢ x7→c1 (X,d,u,u′ ,sc′ )∗P′1 (d,B,u′ ,sc,tg)∗P2 (X,F2 ,B,u,sc′ ,tg2 )∗κ′ ∧a21
  e21 5 : x7→c1 (X,d,u,u′ ,sc′ )∗P′1 (X,F ,B,u,sc′ ,tg)1 ∗κ∧π∧x6=F ∧x6=F2 ∧d6=B∧a11
            ⊢ x7→c1 (X,d,u,u′ ,sc′ )∗P′1 (d,B,u′ ,sc,tg)∗P2 (X,F2 ,B,u,sc′ ,tg2 )∗κ′ ∧a21
As d is a fresh variable, the predicate P′1 (d,B,u′ ,sc,tg) does not appear in the LHS
of e215 . Hence, e215 is classified as invalid and ω-ENT returns invalid. Hence, the
Lemma holds.

Case 2.2: Q≺P P For a general case, we assume P ≡ P2 and Q ≡ P1 . Then, e0 becomes:
          e22 : P2 (x,F ,B,u,sc,tg)0 ∗κ∧π∧x6=F ∧x6=F2 ⊢ P1 (x,F2 ,B,u)∗κ′
The proof for this case is similar to Case 2.1. After applying three rules LInd, 6=null
and RInd in sequence, our system generates the following premise.
e22 3 : x7→c1 (X,d,u,u′ ,sc′ )∗P1 (d,B,u′ )∗P2 (X,F ,B,u,sc′ ,tg)0 ∗κ∧π∧x6=F ∧x6=F2 ∧a21
          ⊢ x7→c1 (X,d,u,u′ ,sc′ )∗P1 (X,F2 ,B,u)∗κ′ ∧a11
where X, d, sc′ and u′ are two fresh variables. Our system applies rule ExM for d and B
to generate the following two premises.
e22 4 : x7→c1 (X,d,u,u′ ,sc′ )∗P1 (d,B,u′ )∗P2 (X,F ,B,u,sc′ ,tg)0 ∗κ∧π∧x6=F ∧x6=F2 ∧a21 ∧d=B
          ⊢ x7→c1 (X,d,u,u′ ,sc′ )∗P1 (X,F2 ,B,u)∗κ′ ∧a11
e225 : x7→c1 (X,d,u,u′ ,sc′ )∗P1 (d,B,u′ )∗P2 (X,F ,B,u,sc′ ,tg)0 ∗κ∧π∧x6=F ∧x6=F2 ∧a21 ∧d6=B
          ⊢ x7→c1 (X,d,u,u′ ,sc′ )∗P1 (X,F2 ,B,u)∗κ′ ∧a11
As d is a fresh variable, the predicate P1 (d,B,u′ ) does not appear in the RHS of e22 5 .
Hence, e22 5 is classified as invalid and ω-ENT returns invalid. Hence, the Lemma
holds.

D.5   Case 3: P and Q have different definitions and they are syntactically
      independent.
We consider three sub-cases based on the positions of inductive predicates in the de-
pendency hierarchies. In the first case, we assume P is “bigger” than Q. In the second
case, we assume P is “smaller” than Q. And in the last case, we assume P is “equal” to
Q.


                                            30
Case 3.1: We assume P ≡ P2 and Q ≡ Q1 . Then, e0 becomes:

           e31 : P2 (x,F ,B,u,sc,tg)0 ∗κ∧π∧x6=F ∧x6=F2 ⊢ Q1 (x,F2 ,B,u)∗κ′

If c1 6≡c2 , is closed returns invalid (Case 2d in Sect. 4.1). Otherwise, the proof for
this case is similar to Case 2.2.


Case 3.2: We assume P ≡ P′1 and Q ≡ Q2 . Then, e0 becomes:

       e32 : P′1 (x,F ,B,u,sc,tg)0 ∗κ∧π∧x6=F ∧x6=F2 ⊢ Q2 (x,F2 ,B,u,sc,tg2 )∗κ′

If c1 6≡c2 , the proof is straightforward. Otherwise, the proof for this case is similar to
Case 2.1.


Case 3.3: We assume P ≡ P1 and Q ≡ Q1 . Then, e0 becomes:

              e33 : P2 (x,F ,B,u)0 ∗κ∧π∧x6=F ∧x6=F2 ⊢ Q2 (x,F2 ,B,u)∗κ′

If c1 6≡c2 , the proof is straightforward. Otherwise, the proof for this case is similar to
Case 1.1.


Case 3.4: We assume P ≡ P2 and Q ≡ Q2 . Then, e0 becomes:

       e34 : P2 (x,F ,B,u,sc,tg)0 ∗κ∧π∧x6=F ∧x6=F2 ⊢ Q2 (x,F2 ,B,u,sc,tg2 )∗κ′

If c1 6≡c2 , the proof is straightforward. Otherwise, the proof for this case is similar to
Case 1.2.
                                                                                        .


E Complexity Analysis - Proposition 5.6

Suppose that n is the maximum number of predicates (both inductive predicates and
points-to predicates) among the LHS of the input entailment and those definitions in
P, and m is the maximum number of fields of data structures. Then, the complexity is
defined as follows.
    First, we analyze the number of computation when all inductive predicates in the
LHS are unfolded at most once. Let P (n, m) be the time complexity function under this
assumption. Each pair of the root and segment parameters, say r and F , of an inductive
predicate is applied with rule ExM at most one. For the first premise where r = F , after
applied with LBase the number of inductive predicates is n − 1 and its running time is
P (n − 1, m).
    For the second premise, say ec , where r 6= F , after applied with LInd, normalization
rules and RInd, it is applied with ∗ to create two premises. While one of them is linked
back to ec the second is of the form: κ′ ⊢κ′′ where κ′ (respective κ′′ ) is the matrix
heap of the unfolded predicate in the LHS (respective RHS). ExM is applied at most

                                            31
(n − 1) + (n − 2) + .. + 1 = O(n2 ) times. Moreover, as (i) all roots of inductive
predicates in a matrix heap must not be aliasing (ensured by the normalization rule ExM)
and (ii) they are must be in the fields of the root points-to predicate of the recursive
definition rule, the number of inductive predicates in both κ′ and κ′′ must be less than
m. Suppose that the running time of such an entailment of m inductive predicates of
matrix heap is q(m), then P (n, m) = P (n − 1, m) + q(m) + O(n2 ).

               P (n, m) = P (n − 1, m) + q(m) + O(n2 )
                        = P (n − 2, m) + 2q(m) + 2O(n2 )
                        = ....
                        = P (1, m) + (n − 1) × q(m) + (n − 1)O(n2 )
                        = 1 + n × q(m) + O(n3 )
(We presume that the running time of entailment without any inductive predicates is 1.)
     We remark that if a formula contains two inductive predicates which has the same
root parameters i.e., P(r,F1 ...)∗Q(r,F2 ...)∗∆, then at least one of them must be reduced
into base case with the empty heap. As m is the maximum number of fields of data
structures and the roots parameters of κ′ must be one of these variables of the fields, the
number of inductive predicates of the LHS of any entailment that is derived from κ′ ⊢κ′′ ,
is less than or equal to m. Thus, under modular substitution the number of combination
of such m inductive predicates is O(2m ).
     Therefore, P (n, m) = O(n × 2m + n3 ).
     The unfolding is depth-first and the steps for the second unfolding are similar. As
the proof is linear, then the number of computation when all inductive predicates are
unfolded at most two times is at most as 2 × P (n, m) = O(n × 2m + n3 ).


F    Completeness of proof rules - Lemma 5.8

The completeness of all rules except rule ∗ is straightforward. In the following, we
prove the completeness of rule ∗. The proof is based on the following auxiliary Lemma.

Lemma F.1. If κ ∧ φ ∧ a is in NF and x6=E6∈φ, then (κ ∧ φ)[E/x] ∧ a is in NF.

Proof. All but the fifth clause in the definition 3 are invariant under substitution. More-
over, x6=E6∈φ exclude the violation of the fifth clause under substitution as well      .

   First, we provide proofs for pure part when pure contraints in LHS does not imply
pure contraints in RHS.
Proposition F.2. If κ ∧ φ ∧ a ⊢ κm ∧ φ′ ∧ a′ is in NF and e′ : emp ∧ φ ∧ a ⊢ emp ∧ φ′ ∧ a′
is not derivable, then κ ∧ φ ∧ a ⊢ κ′ ∧ φ′ ∧ a′ is invalid.

Proof. We show that there is a model of the LHS that satisfies either ¬φ′ or ¬a′ holds.
We proceed cases for each predicate in the RHS.

 1. Case φ′ ≡ E1 =E2 . As the LHS is in NF, any bad model of κm ∧ φ ∧ a implies that
    E1 6=E2 . In other words, κm ∧ φ ∧ a implies that ¬E1 =E2 .

                                            32
 2. Case φ′ ≡ E1 6=E2 . As e′ is not derivable, then the side condition of rule Hypothesis
    does not hold. This means E1 6=E2 6∈φ.
    We note that if κm ∧φ∧a is in NF and E1 6=E2 6∈φ, then (κm ∧φ∧a)[E1 /E2 ] is also
    in NF (assuming that E1 is a variable - Lemma F.1). Then suppose s, h be a bad
    model of (κm ∧ φ ∧ a)[E1 /E2 ], then s[E1 7→s(E2 )], h is a model of (κm ∧ φ ∧ a).
    s[E1 7→s(E2 )], h implies that ¬E1 6=E2 . Therefore, (κm ∧ φ ∧ a) does not imply
    E1 6=E2 . Neither is (κm ∧ φ ∧ a).
 3. Case φ′ ≡ true . As e′ is not derivable, then the side condition of rule Hypothesis
    does not hold. We consider two cases.
    (a) a ∧ a′ is unsatisfiable. Hence, any model of a implies ¬a′ .
    (b) a ∧ a′ is satisfiable. Hence, a ∧ ¬a′ is also satisfiable and is in NF. Moreover,
         any model of a ∧ ¬a′ implies ¬a′ . As a ∧ ¬a′ is an under-approximation of a,
         from any model a ∧ ¬a′ we can construct a model satisfying a implies ¬a′ .

Therefore, any bad model of κm ∧ φ ∧ a is a counter-model.                              .

   Secondly, we prove the completeness of rule ∗ when the LHS of the conclusion in
NF is a base formula.
                             κ1 ∧π ⊢ κ2      κ∧π ⊢ κ′
                            ∗
                                     κ1 ∗κ∧π ⊢ κ2 ∗κ′
Proof. We prove that if the rule’s conclusion is derivable then the rule’s premises are
derivable.
    We prove by induction on the number n of points-to predicates in the LHS of the
conclusion.

 1. Base case: n = 0 and n = 1, the proof is trivial.
 2. Inductive case: Assume that it is true for n = k.
    Suppose κ1 ∗ κ = x1 7→c1 (v̄1 )∗...∗xk+1 7→ck+1 (v̄k+1 ) and π contains enough dis-
    equalities for NF.
    We proceed by cases on κ2 .
    (a) Case 1: κ2 is a points-to predicate. If κ2 ≡ xj 7→ ( ) where xj 6∈ {x1 , ...xk+1 }.
        Then procedure is closed has also returned invalid already and the the con-
        clusion is not derivable. Contradiction. Therefore, κ2 must be one of the points-
        to predicates in the LHS. Assume that κ2 ≡ x1 7→c1 (v̄1 ). Then, κ1 |= κ2 and
        by induction κ ∧ π ⊢ κ′ is also derivable.
    (b) Case 2: κ2 is an inductive predicate; assume κ2 ≡ P(r,F ). Similarly to the
        above case, r ∈ {x1 ; ...; xk+1 }. Otherwise, procedure is closed has returned
        invalid already. Assume r ≡ x1 . Secondly, x1 6=F ∈ π. Otherwise, ω-ENT is
        stuck (it could not apply rule RInd) and procedure is closed has also returned
        invalid already. Third, x1 7→c1 ( ) 6∈ κ′ . Otherwise, the RHS of the conclusion
        is false the conclusion is not derivable. Now, the conclusion could be applied
        with rule RInd to generate x1 7→c1 ( ) ∗ κ′′ ∗ P(F2 ,F ). Now, it comes back to
        Case 1 above.

                                                                                        .

                                            33
G Completeness of proof search - Proposition 5.10

We prove the correctness of Proposition 5.10 through two steps:

 1. proofs for the case where LHS is a base formula. Those entailments are reduced
    without LInd.
 2. proofs for the case where LHS is a general formula. Those entailments are reduced
    with LInd prior to applying other rules.

In the proofs, we make use of the following auxiliary Lemmas.

Lemma G.1. If κ ∧ π ⊢ κ′1 ∗ κ′2 in NF is derivable, then there exist κ1 , κ2 such that
κ ≡ κ1 ∗ κ2 and both κ1 ∧ π ⊢ κ′1 and κ2 ∧ π ⊢ κ′2 are derivable.

Lemma G.2. If κ1 ∗ κ2 ∧ π is in NF and κ1 ∧ π ⊢ κ′1 is valid, then κ1 ∗ κ2 ∧ π ⊢ κ′1 ∗ κ′2
is valid iff κ2 ∧ π ⊢ κ′2 is valid.

Based on the fact that heaps of a normalized base formula is precise. The proof is
straightforward based on the semantics of the separating conjunction ∗.


G.1 Base-Formula LHS

First, we show the correctness of case 2a) of procedure is closed i.e., an entailment
is stuck then it is invalid. After that, we show the invalidity is preserved through proof
search.
     As the LHS is a base formula, rule LInd (and rule LBase) is never be applied. We
prove case 2a) by induction on the number of disequalities missing from the LHS and
generated by rule ExM. First, we prove the case where the RHS is an occurrence of
compositional predicate P assuming that the points-to predidcate in the definition of P
is c.
Lemma G.3. If e0 : x7→c(F2 ,p̄,u)∗κ ∧ φ ∧ a ⊢ P(x,F ,B̄,u,sc,tg) is in NF and is stuck,
then it is invalid.

Proof. Due to the stuckness, ω-ENT could not applies rule RInd. Hence, x6=F 6∈φ. As
the the entailment is in NF, (x7→c(F2 ,p̄,u)∗κ∧φ)[F/x]∧a ⊢ P(x,F ,B̄,u,sc,tg)[F/x] is
in NF (by Lemma F.1). As all models satisfying the LHS (x7→c(F2 ,p̄,u)∗κ∧φ)[F/x]∧a
are non-empty heap and in NF, all models satisfying the RHS P(x,F ,B̄,u,sc,tg)[F/x] ≡
P(F ,F ,B̄,u,sc,tg) are empty heap, this entailment is invalid. As the substitution law is
sound and complete, e0 is invalid.                                                     .

Lemma G.4. If e0 : κ ∧ φ ∧ a ⊢ κ′ is in NF and is stuck, then it is invalid.

Proof. By induction on the number of disequalities missing from φ. We proceed by
cases.

 1. κ′ ≡ P(x,F ,B̄,u,sc,tg) ∗ κ′′ assuming that the points-to predidcate in the definition
    of P is c.

                                           34
    (a) op(x)6∈κ. This case is the case 2c) of procedure is closed. The bad model of
        the LHS is the counter-model.
    (b) op(x)∈κ. ω-ENT reduces the entailments by first applying rule ExM prior to
        applying rule LInd. We are considering the case ω-ENT could not apply rule
        LInd. We proceed cases for the LHS.
          i. κ ≡ x7→c(F2 ,v̄)∗κ0 and x6=F 6∈φ.
             If e1 : x7→c(F2 ,v̄)∗κ0 ∧ φ ∧ a∧x6=F ⊢ P(x,F ,B̄,u,sc,tg) ∗ κ′′ is stuck,
             rule LInd could not be applied. Hence, x7→c(F2 ,v̄) ∈ κ′′ . Therefore, there
             is no model that satisfies the RHS. This entailment e1 is thus invalid. As
             rule ExM is complete (Lemma 5.8), e0 is invalid.
             If e1 is deriable, following Lemma G.1, there exist κ1 , κ2 such that κ0 ≡
             κ1 ∗ κ2 and both e2 : x7→c(F2 ,v̄)∗κ1 ∧ φ ∧ a∧x6=F ⊢ P(x,F ,B̄,u,sc,tg)
             and e3 : κ2 ∧ φ ∧ a∧x6=F ⊢ κ′′ are derivable. We proceed two sub-cases:
              A. e′3 : κ2 ∧ φ ∧ a ⊢ κ′′ is stuck. Hence either op1 x ∈ κ2 or op2 (F ) ∈ κ2 .
                  This implies either opx ∗ op1 x in the LHS of e0 or opx ∗ op3 F in the
                  LHS of e0 . As e0 is in NF, either x6=x ∈ φ or x6=F ∈ φ. Both can’t
                  not happen as the first scenario contradicts with assumption that LHS
                  is in LHS and the second one contradicts with assumption x6=F 6∈φ.
              B. e′3 : κ2 ∧ φ ∧ a ⊢ κ′′ is derivable. Hence, by soundness (Lemma 5.3),
                  it is valid. (2a)
                  As e0 is stuck and e′3 is derivable, we deduce that e′2 : x7→c(F2 ,v̄)∗κ1 ∧
                  φ ∧ a ⊢ P(x,F ,B̄,u,sc,tg) is stuck (Otherwise, e0 is derivable as well,
                  contradition). By Lemma G.3, e′2 is invalid. (2b)
                  By (2a), (2b) and Lemma G.2, e0 is invalid.
         ii. κ ≡ x7→c′ (F2 ,v̄)∗κ0 , x6=F ∈ φ and c′ 6≡c. The proof is similar to Case 2d
             of procedure is closed. The bad model of the LHS is the counter-model.
 2. κ′ ≡ x7→c(v̄) ∗ κ′′ . Straightforward.
 3. κ′ ≡ emp. Straightforward.
                                                                                         .

Proposition G.5. If κ ∧ φ ∧ a ⊢ κ′ is in NF and is not derivable, then it is invalid.

Proof. In a incomplete proof, if a leaf node in NF is stuck then it is invalid (Lemma G.4
and Lemma F.2). The invalidity is preserved up to the root based on Lemma 5.8.         .


G.2 General LHS

By induction on the RHS. We proceed cases on the RHS. In the proofs, for convenient,
we write κa ∧ πa ⊢κ κc ∧ πc as a shorthand of κa ∗ κ ∧ πa ⊢ κc ∗ κ ∧ πc and and no any
matching heaps between κa and κc could be found through the application of rule ∗.

Lemma G.6. If e: κ ∧ π ⊢κm κ′ in NF where e0 : κ ∧ π ⊢ κ′ is stuck, then e0 is invalid.

Proof. We first show e0 is invalid. After that by using Lemma G.2, we could deduce the
invalidity of e. To show invalidity of e0 , we proceed cases on the possible base formula
of the LHS.

                                            35
 1. e1 : κ ∧ π ⊢ κ′ is stuck. By Proposition G.5, e1 is invalid. As κ ∧ π is an approxi-
    mation of κ ∧ π, e0 is invalid.
 2. e2 : κ ∧ π ⊢ κ′ is derivable. And κ′ ≡ op(E) ∗ κ′′ . We proceed cases on op(E).
     – op(E) ≡ Q(x,F3 ,B̄,u,sc,tg3 ). As the LHS is in NF, e2 could be reduced by
         RInd. This implies that x7→c(F ,d, ¯ tg,u)[v̄/d]∧π
                                                        ¯ 0 [tg/scd] ∈ κ and x6=F3 ∈ π.
         This implies that there are two possible sub-cases.
         (a) Sub-case 1: x7→c(F ,d, ¯ tg,u)[v̄/d]¯ ∈ κ. As x6=F3 ∈ π, e0 could be applied
             with RInd. It is impossible as it contradicts with the assumption that e0 is
             stuck.
         (b) Sub-case 2: P(x,F ,B̄,u,sc,tg) ∈ κ. As x6=F3 ∈ π, e0 could be applied
             with LInd. As x6=F3 ∈ π, e0 could be applied with LInd.
     – op(E) ≡ x7→c(next : F, v̄). Based on x7→c(next : F, v̄) ∈ κ, there are two
         cases.
         (a) x7→c(next : F, v̄) ∈ κ. This contradicts with the assumption that x7→c(next :
             F, v̄) could not be matched with any predicate in κ. This case is impossi-
             ble.
         (b) P(x,E, ..) ∈ κ. Any model satisfying the LHS when replacing P(x,E, ..)
             by three-time unfolding (with two points-to predicates e.g., x7→c(next :
             F1 , ..) ∗ F1 7→c(next : F, ..) is a counter-model.
                                                                                    .

Proposition G.7 (Incompleteness Preservation). Given an input entailment e0 : ∆ ⊢ ∆′ ,
and there is an leaf node ei : ∆l ⊢κm ∆′l in its incomplete proof tree where
 – the leaf node ei is in NF; and
 – none of application of rule FR from the root e0 to the leaf node ei ; and
 – ∆l ⊢ ∆′l is not derivable.
then e0 is invalid.

Proof. By Lemma G.6, ei is invalid. By Lemma 5.8, e0 is invalid.                    .




                                          36
