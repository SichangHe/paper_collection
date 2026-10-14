                                         An Algebra of Alignment for Relational Verification
                                         (Extended Version)
arXiv:2202.04278v4 [cs.LO] 23 Mar 2023




                                         TIMOS ANTONOPOULOS, Yale University, USA
                                         ERIC KOSKINEN, TON CHANH LE, RAMANA NAGASAMUDRAM, DAVID A. NAUMANN,
                                         and MINH NGO, Stevens Institute of Technology, USA
                                         Relational veriﬁcation encompasses information ﬂow security, regression veriﬁcation, translation validation
                                         for compilers, and more. Eﬀective alignment of the programs and computations to be related facilitates use of
                                         simpler relational invariants and relational procedure specs, which in turn enables automation and modular
                                         reasoning. Alignment has been explored in terms of trace pairs, deductive rules of relational Hoare logics
                                         (RHL), and several forms of product automata. This article shows how a simple extension of Kleene Algebra
                                         with Tests (KAT), called BiKAT, subsumes prior formulations, including alignment witnesses for forall-exists
                                         properties, which brings to light new RHL-style rules for such properties. Alignments can be discovered
                                         algorithmically or devised manually but, in either case, their adequacy with respect to the original programs
                                         must be proved; an explicit algebra enables constructive proof by equational reasoning. Furthermore our
                                         approach inherits algorithmic beneﬁts from existing KAT-based techniques and tools, which are applicable
                                         to a range of semantic models.
                                         ACM Reference Format:
                                         Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh                              20
                                         Ngo. 2023. An Algebra of Alignment for Relational Veriﬁcation (Extended Version). Proc. ACM Program. Lang.
                                         7, POPL, Article 20 (January 2023), 61 pages. https://doi.org/10.1145/3571213

                                         1   INTRODUCTION
                                         A number of important program requirements are not trace properties but can be deﬁned as 2-
                                         properties. For example, secure information ﬂow says that any two executions with the same “low”
                                         (non-secret) inputs have the same low outputs. Continuity says two executions from very close
                                         inputs produce very close outputs. Pairs of executions are also the basis for relations between
                                         programs, such as extensional equivalence, reﬁnement, or simulation.
                                            One way to prove such a relational property is to prove a strong functional property of each
                                         program, and show that the relational property is a consequence. However, from early work on
                                         reﬁnement [de Roever et al. 2001; de Roever and Engelhardt 1998] through explicit studies of rela-
                                         tional program logic [Benton 2004; Francez 1983] to current work on automated relational reason-
                                         ing (e.g. see [Beckert and Ulbrich 2018]) it has been clear that one should align intermediate points
                                         in programs and their executions, in order to decompose the reasoning. In many cases it is much
                                         better to reason in terms of a well chosen alignment, which can make it possible to reason using
                                         logically simple relational invariants such as conjunctions of equalities between variables. This is
                                         especially important for automated reasoning, since restricted fragments such as linear arithmetic
                                         facilitate techniques like Horn clause solving to ﬁnd invariants. It is also important in the many
                                         Authors’ addresses: Timos Antonopoulos, Yale University, USA; Eric Koskinen; Ton Chanh Le; Ramana Nagasamudram;
                                         David A. Naumann; Minh Ngo, Stevens Institute of Technology, USA.

                                         Permission to make digital or hard copies of part or all of this work for personal or classroom use is granted without fee
                                         provided that copies are not made or distributed for proﬁt or commercial advantage and that copies bear this notice and
                                         the full citation on the ﬁrst page. Copyrights for third-party components of this work must be honored. For all other uses,
                                         contact the owner/author(s).
                                         © 2023 Copyright held by the owner/author(s).
                                         2475-1421/2023/1-ART20
                                         https://doi.org/10.1145/3571213


                                                                          Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:2     Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


situations where a functional speciﬁcation is not available. Moreover, alignment enables use of
relational speciﬁcations and summaries for procedures.
   For these reasons, alignment appears in various guises such as the same-structure (“diagonal”)
proof rules of Benton’s relational Hoare logic [Benton 2004] and program product constructions
based on syntax [Barthe et al. 2011a; Sousa and Dillig 2016] and on product automata [Barthe et al.
2013; Churchill et al. 2019]. For the moment let us use the term aligned product for such construc-
tions. The proof of a given relational property has two parts: the chosen aligned product satisﬁes
the property, and the aligned product is adequate, in the sense that it represents all computations
of the program(s) of interest. Veriﬁcation can be automated by searching for possible alignments
and checking whether they can be proved to satisfy the property, or by synthesizing an alignment
in tandem with attempting to prove the property [Antonopoulos et al. 2019; Churchill et al. 2019;
Farzan and Vandikas 2019; Shemer et al. 2019; Unno et al. 2021].
   The current state of the art oﬀers a number of variations on these ideas, in disparate formu-
lations. In this paper we introduce an algebra for alignment products which makes it possible to
account for adequacy by equational reasoning. Our algebra, called BiKAT, is a simple extension of
Kleene Algebra with Tests (KAT) [Kozen 1997], itself an algebra of programs. Our representation
of alignment products is thus immediately amenable to various program analysis tools and may
serve as a framework for procedures that search for alignments.
   In KAT, a partial correctness assertion {𝑝 }𝑐{𝑞} is expressed by an equation: 𝑝; 𝑐; ¬𝑞 = 0. Now
consider what we call the ∀∀ relational judgment, written 𝑐 |𝑐 ′ : 𝑅 ≈> 𝑆, meaning that: from a pair
of states related by 𝑅, terminated executions of 𝑐 and 𝑐 ′ respectively, end in states related by 𝑆. The
relational judgment can be expressed by the similar equation 𝑅; h𝑐 | 𝑐 ′ i; ¬𝑆 = 0, using the BiKAT
form h𝑐 | 𝑐 ′ i that represents pairs of executions. We show that rules of relational Hoare logics can
be derived in BiKAT, which applies to many semantic models, not just the speciﬁc semantic models
used in prior works such as those cited above.
   Not all relational properties have the termination-insensitive ∀∀ (2-safety) form described above.
For programs which may exhibit nondeterminacy, typical requirements involve existential quan-
tiﬁcation. For example, possibilistic noninterference says that given two low-indistinguishable
states, and a terminated execution from the ﬁrst, there is a terminated execution from the second,
with low-indistinguishable ﬁnal state [Clarkson and Schneider 2010; Sabelfeld and Myers 2003].
As we explain, attempts to formulate such properties in the algebra lead to a three-run equation
which we have found somewhat unwieldly. So, in addition we provide a usable reduction to equa-
tions on two-run alignment products.
   With this reduction in hand, we discovered that one can derive rules for reasoning about two
fundamental and ubiquitous kinds of ∀∃ properties: forward and backward simulation. We derived
inference rules for a logic of forward simulation and a logic of backward simulation. In retrospect,
these logics seem natural and it is surprising that (to our knowledge) such rules have not appeared
in the literature. As often happens, devising an algebraic description of the models of interest leads
to new insights about existing ideas, and also results far beyond the initial motivations.
   Contributions.
       • We deﬁne a novel algebra, BiKAT, that can express the alignment of programs in both rela-
         tional and trace semantic models, building in a simple way on the well understood KAT.
       • Using BiKAT, we derive rules of relational Hoare logic for ∀∀ properties, just as Kozen’s
         seminal work derives the rules for conventional Hoare logic [Kozen 2000].
       • Using BiKAT equations, we characterize the ∀∃ forward and backward simulation properties,
         and use these results to derive new proof rules for these properties. To our knowledge this
         provides the ﬁrst deductive system for backward simulation judgments.

Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                             20:3


   Outline. Sect. 2 is an overview of the problem and shows BiKAT in action. Sect. 3 brieﬂy reviews
KAT. Sect. 4 deﬁnes BiKAT and some standard models. Sect. 5 demonstrates direct use of BiKAT on
illustrative examples of relational reasoning challenges. Examples are given throughout to show
how BiKAT can express and justify alignments used in the literature on relational veriﬁcation.
Sect. 6 derives rules for the ∀∀ judgment. Sect. 7 addresses ∀∃ properties: we develop characteriza-
tions in BiKAT and use these to derive proof rules for forward and backward simulation. We also
report on explorations for ∃∀ and ∃∃ properties, and sketch a notion of TriKAT that deserves fur-
ther study. Sect. 8 discusses automation, product programs, expressiveness, and future directions,
all in the context of related work. This extended version of the paper adds an Appendix (Sect. 9) with
many proofs and examples. It also completes the proof of Theorem 7.3, strengthens that result, and
strengthens Theorems 7.8 and 7.9 accordingly.
   Accompanying this paper is a Coq formalization that includes the basic deﬁnitions and results
about BiKATs [Antonopoulos et al. 2022b].

2   EXAMPLES OF ALIGNMENT IN BIKAT
We now introduce our algebra of alignment, through a series of examples that highlight the fea-
tures of our theory. Recall that Kleene Algebra with Tests (KAT) [Kozen 1997] can be used to
represent and reason about the behavior of programs. Atomic program statements can be treated
as primitive “actions” in the KAT and conditions can be treated as primitive “tests.” For example,
consider the following program that computes factorial of n and stores it in r:
                         Code: C1: i:=n; r:=1; while i!=0 do r:=r*i; i:=i-1 od
                         KAT: 𝑘 1 : i:=n · r:=1 · ( [i≠0] · r:=r*i · i:=i-1) ∗ · ¬[i≠0]
   The above KAT expression combines primitives with sequential composition · and Kleene star-
iteration ∗. Tests are denoted with square brackets to distinguish from non-test actions (in a KAT
tests are a subset of actions). There are various semantic models of KATs, notably relational models,
where actions are state relations, and trace models where actions denote sets of traces. KAT permits
one to express properties through terms/equations that involve programs and their speciﬁcations.
For example, KAT subsumes Hoare logic: the KAT equation 𝑝 · 𝑘 1 · ¬𝑞 = 0 expresses validity of the
Hoare triple {𝑝 }C1 {𝑞}.
   Example 2.1. Dependency or non-interference. Let us now consider a basic ∀∀ property of a single
program (2-safety): whether diﬀerent output results can be observed by varying input values. A
basic pre/post 2-safety ∀∀ property, written 𝐶1 | 𝐶1 : [n =¥ n] ≈> [r =¥ r], requires that for any
two executions of 𝐶1, if they agree on the initial value of n, then they will agree on the ﬁnal value
of r, regardless of the initial values of the other variables. Here [n =¥ n] means value of n in the
left program is equal to the value of n in the right program. Our notation does not require that the
given program(s) have been modiﬁed to act on disjoint parts of a single state.
   In this paper we will describe an algebra for expressing these and other relational veriﬁcation
problems, as well as the alignments necessary for proving them. We will introduce a relational
analog of KAT called BiKAT, which allows us to, for example, express this 2-safety judgment as:
                                         [n =¥ n] · h𝑘 1 | 𝑘 1 i · ¬[r =¥ r] = 0                                   (1)
The connectives above are relational analogs of the KAT connectives: · is sequential composition,
¬ is negation, and 0 is the empty relation. A key feature of BiKAT is to be able to homomorphically
embed a unary KAT expression 𝑘 into a relational setting, that acts according to 𝑘 on one side and
acts as the identity on the other side. Embedding 𝑘 on the “left” is denoted h𝑘], on the “right”
is [𝑘i, and we write h𝑘 | 𝑘 ′ i to mean h𝑘] · [𝑘 ′ i. This embedding resembles the popular sequential
product (a.k.a. self-composition [Barthe et al. 2004]), but does not require 𝑘 and 𝑘 ′ to act on disjoint

                                Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:4   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


variables. A BiKAT is a (special kind of) KAT and, in addition to embedded unary actions/tests, can
be equipped with its own relational primitive actions and tests. The agreement [r =¥ r] above is a
primitive “bitest.” Embedding and bitests are sequentially composed together in the equation above
with · into an overall equation that characterizes validity of the relational judgment, by requiring
that post-disagreement on r is equivalent to the empty set of behaviors.
   While the above is merely a BiKAT problem statement of non-interference, the principle beneﬁts
of BiKAT arise when we begin to use our equational theory of BiKAT to derive alignments that ease
(or make tractable) the task of relational veriﬁcation. Notice that, thus far, the above embedding
would still require one to reason that 𝑘 1 computes the factorial function, which is more work
than truly necessary for non-interference. (This issue was highlighted in the seminal work that
introduced the term 2-safety [Terauchi and Aiken 2005].) We can instead exploit that the left/right
embeddings are homomorphisms, and exploit the algebra of the embedded KAT expressions, to
ﬁnd another equation that implies the above one. In Sect. 4 we will discuss the details that lead to
the following:
        [n =¥ n] · hi:=n | i:=ni · hr:=1 | r:=1i
         · (h[i!=0] · r:=r*i · i:=i-1 | [i!=0] · r:=r*i · i:=i-1i) ∗ · h[i==0] | [i==0]i · ¬[r =¥ r] = 0
This equation is derived from (1) using BiKAT laws, the fact that embedding distributes through
the KAT operators, and the fact that left and right embeddings commute: h𝑘] · [𝑘 ′ i = [𝑘 ′ i · h𝑘].
We have now aligned the programs so that their loops iterate in “lock step”. (We will see more
complicated alignments below.) For this example, this alignment is suﬃcient because, using a few
axioms that embody the semantics of primitive tests and assignments we can introduce relations
within the body of the BiKAT term, using bitests [i =¥ i], [n =¥ n], [r =¥ r] expressing agreement
on i, n, r. Overall this lets us conclude the original property without having to resort to reasoning
about the full functional behavior of the programs involved.
   Example 2.2. Aligning two diﬀerent programs. Consider the programs from Shemer et al. [2019]:
                          𝐷1 :     y:=0 · z:=2*x · ( [z>0] · z-- · y:=y+x) ∗ · [z<=0]
                          𝐷2 :     y:=0 · z:=x · ( [z>0] · z-- · y:=y+x) ∗ · [z<=0] · y:=y*2

These programs compute 2x2 , but in diﬀerent ways: 𝐷 1 iterates 2x times, each time adding x to the
result y, whereas 𝐷 2 iterates only x times, but then multiplies by 2 at the end. This example has a
ﬂavor of a compiler optimization, where a program may be transformed to save on loop iterations.
Here too we can formulate the property of equal outputs from equal inputs and, using the laws of
BiKAT to rewrite the problem into this aligned form:
                        [x =¥ x] · hy:=0 | y:=0i · hz:=2*x | z:=xi · [z =¥ 2z]
                         · ( [z =¥ 2z] [2y =¥ y] hbody · body | bodyi) ∗
                         ·[2y =¥ y] · h[z==0] | [z==0] · y:=y*2i · [x =¥ x] · ¬[x =¥ x] = 0
where body =  ˆ [z>0] z--; y:=y+x. (Throughout this paper, we often use juxtaposition or ; to mean
the · KAT operator.) This example uses an alignment where two iterations of the loop in the ﬁrst
program are related to one iteration of the second one, to preserve the relational invariant that z
in the left program is twice the value of z in the right program and that y in the right program is
twice the value of y in the left program. To prove this we introduce agreement bitests in the body
of the loop and use KAT-based inductive reasoning to show those bitests, including [x =¥ x], are
indeed invariant. With these simple relational bitests, we can prove the equivalence between 𝐷 1
and 𝐷 2 .
   Example 2.3. Mixing program algebra with alignment algebra. Now consider two programs that
iterate over C-style arrays:

Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                             20:5


𝐿1 : x := 0; while ( x < N * M ){ a [ x ] := f ( x ); x ++;}
𝐿2 : i := 0; while ( i < N ) { j := 0; while ( j < M ) { A [i , j ] := f ( i* M + j ) ; j ++; i ++;}}

   In 𝐿1 there is a one-dimensional array, a, of size N*M, while 𝐿2 uses an N-by-M two-dimensional
array A. We prove that the two programs are equivalent modulo this change in data representation.
This example is used in Barthe et al. [2013] to argue for alignment based on a control ﬂow graph
representation. A custom rewriting relation, with KAT-like rules, is used in Banerjee et al. [2016]
to handle the example using syntactic RHL rules.
   Aligning these programs is challenging because they have fundamentally diﬀerent shapes to
them (single versus nested loops). To address this example we exploit the fact that the programs
can be represented as KAT terms which themselves can be algebraically manipulated, whilst em-
bedded within the BiKAT. Our alignment (detailed in Sect. 5) ﬁrst uses unary KAT laws to trans-
form 𝐿1 so that it consists of nested loops. We then align those nested loops and introduce loop
alignment invariants including an agreement on indexing [x =¥ i × M + j] and an agreement on
array values [a[x] =¥ A[i,j]]. In this way, the laws of BiKAT (and underlying KAT laws) allow one
to use equational reasoning to simplify the task of deriving useful alignments, and then introduce
simple relational invariants that suﬃce to prove the overall property.
   Beyond the above examples, BiKAT can also be used to construct data-dependent alignment
(e.g., [Shemer et al. 2019]). A single iteration in one program may need to be aligned with a varying
number of iterations in a second program, dependent on the data. Example 6.3 will demonstrate
BiKAT’s capability to support such alignments.

   Example 2.4. Expressing ∀∃ properties. Consider programs 𝐸 1 : x:=any; y:=x and 𝐸 2 : t:=any; z:=t+1.
These simple programs choose a nondeterministic value (keyword any) and then use that value to
make an assignment. A common speciﬁcation pattern is that for any pair of pre-related states, and
every execution of 𝐸 1 , there are choices that 𝐸 2 can make to ensure that the post-states are related.
The pattern is useful for program equivalence and also for information ﬂow where it is known as
possibilistic non-interference [Clarkson and Schneider 2010]. For this example, let us use true as the
pre-relation and [y =¥ z] as the post-relation.
   In Sect. 7.5 we describe how BiKAT can be used to support ∀∃ properties such as the above. We
again use BiKAT to derive alignments but for ∀∃ we also introduce bitests that intentionally restrict
some of the behaviors of the programs. Let 𝑊 be this “witness,” consisting of the aligned programs,
along with bitest restrictions. We reduce the problem to three conditions on 𝑊 (Theorem 7.1):
(WC) The corresponding ∀∀ property holds of 𝑊 .
(WO) 𝑊 over-approximates the behavior of the left program.
(WU) 𝑊 under-approximates the behavior of the right program.
For the above example, we can align the programs in lock-step, and use the bitest [x-1 =¥ t] so that,
after the assignment t:=any, executions are then restricted to those where t is x-1. Doing so will
ensure that the post-relation [y =¥ z] holds (WC). Moreover, this bitest does not restrict the behav-
iors of the left program (WO), nor does it add behaviors on the right that are not already allowed
by the right program (WU). In Sect. 7.4 we also provide deductive rules for such ∀∃ properties.

3 PRELIMINARIES
A Kleene Algebra with Tests (KAT) [Kozen 1997; Kozen and Smith 1996] is a two-sorted structure
(A, B, +, ·, ∗, ¬, 1, 0), where B ⊆ A, such that B is closed under the operations +, ·, ¬ and these
satisfy the laws of Boolean algebra. Moreover (A, +, ·, ∗, 1, 0) is a Kleene algebra.
   We use 𝑎, 𝑏, 𝑐, . . . for elements of A (the “actions”) and 𝑝, 𝑞 . . . for elements of B (the “tests”). We
sometimes write 𝑎 · 𝑏 as 𝑎; 𝑏 or 𝑎𝑏 and let it bind tighter than +. The axioms of Kleene algebra are:

                                Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:6   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo




                  𝑎 + (𝑏 + 𝑐)      =    (𝑎 + 𝑏) + 𝑐                      1 + 𝑎 · 𝑎∗     =     𝑎∗
                         𝑎 +𝑏      =    𝑏 +𝑎                             1 + 𝑎∗ · 𝑎     =     𝑎∗
                         𝑎+0       =    𝑎                             𝑏 +𝑎 ·𝑐 ≤ 𝑐       ⇒     𝑎∗ · 𝑏 ≤ 𝑐
                         𝑎 +𝑎      =    𝑎                             𝑏 +𝑐 ·𝑎 ≤ 𝑐       ⇒     𝑏 · 𝑎∗ ≤ 𝑐
                    𝑎 · (𝑏 · 𝑐)    =    (𝑎 · 𝑏) · 𝑐
                          1·𝑎      =    𝑎
                          𝑎·1      =    𝑎
                   𝑎 · (𝑏 + 𝑐)     =    𝑎 ·𝑏 +𝑎 ·𝑐
                   (𝑎 + 𝑏) · 𝑐     =    𝑎 ·𝑐 +𝑏 ·𝑐
                          0·𝑎      =    0
                          𝑎·0      =    0

where ≤ is the partial order deﬁned by 𝑎 ≤ 𝑏 ⇔ 𝑎 + 𝑏 = 𝑏. Some useful consequences are the
sliding law 𝑎 · (𝑏 · 𝑎) ∗ = (𝑎 · 𝑏) ∗ · 𝑎 and the invariance law 𝑝 · 𝑎 ≤ 𝑝 · 𝑎 · 𝑝 ⇒ 𝑝 · 𝑎 ∗ ≤ 𝑝 · 𝑎 ∗ · 𝑝
(where 𝑝 is a test). The correctness equation 𝑝 ·𝑐 · ¬𝑞 = 0 has useful equivalent forms: 𝑝 ·𝑐 = 𝑝 ·𝑐 ·𝑞
and 𝑝 · 𝑐 ≤ 𝑝 · 𝑐 · 𝑞. Every test 𝑝 satisﬁes 𝑝 ≤ 1.
   Given some set Σ, a relational model is (A, B, +, ·, ∗, ¬, 1, 0) where A is a set of relations1 on
Σ, where 1 is the identity relation 𝑖𝑑 Σ , 0 is the empty relation, · is relational composition, ∗ is
reﬂexive-transitive closure, + is union of relations, B is a set of sub-identities, i.e., subsets of the
identity relation 1, and ¬𝑏 is the complement 1 \𝑏. Note that ≤ is set inclusion.2 Relational models
can be obtained from big-step or denotational semantics of programs, with Σ the set of states.
   A full relational model is one where A is all relations on Σ and B is all sub-identities. A full
relational model has a top element, which we call havoc and write hav. Being top means 𝑎 ≤ hav
for all 𝑎 in A.
   A trace model [Kozen 2003, 2004] (A, B, +, ·, ∗, ¬, 1, 0) is given in terms of some set of primitive
actions and some set Σ of states. An element of A is a set of traces, where a trace is a nonempty
alternating sequence of states and primitive actions, beginning and ending with a state. (The def-
initions are with respect to a given set of admissible traces, which one can consider as possible
observations for a programming language of interest. For example, if each primitive action has an
associated relation on states, then traces may be required to be consecutive with respect to those
relations.) An element of B is a set of singleton traces (essentially a set of states) and negation is de-
ﬁned as complement with respect to Σ. The + operation is union. For traces 𝑡 and 𝑢, the coalesced
catenation 𝑡 ⋄ 𝑢 is deﬁned only if the last state of 𝑡 is the ﬁrst of 𝑢, in which case the sequences
are catenated but omitting one copy of that state. Otherwise 𝑡 ⋄ 𝑢 is undeﬁned. For 𝑎 and 𝑏 in A,
the set 𝑎 · 𝑏 is deﬁned to be {𝑡 ⋄ 𝑢 | 𝑡 ∈ 𝑎 ∧ 𝑢 ∈ 𝑏 ∧ 𝑡 ⋄ 𝑢 deﬁned}. The star operation is given by
iterated catenation. A full trace model is one that contains all sets of admissible traces (so it has
a top).
   A KAT is *-continuous [Kozen 1997] provided that for all 𝑥, 𝑦, 𝑧 the supremum sup𝑛 ∈N (𝑥 ·𝑦𝑛 ·𝑧)
(with respect to ≤) exists and 𝑥 · 𝑦 ∗ · 𝑧 = sup𝑛 ∈N (𝑥 · 𝑦𝑛 · 𝑧). Here 𝑦𝑛 is the iterate deﬁned by 𝑦 0 = 1
and 𝑦𝑛+1 = 𝑦 · 𝑦𝑛 . Relational and trace models are *-continuous.



1 We always mean binary relations.
2 Also, A is closed under these operations, but need not be the full set ℘(Σ × Σ) of all relations; and B need not include all

sub-identities.


Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                                         20:7


4 BIKAT
4.1 Definitions and Basic Results
                                                                          ¥ B,
  Deﬁnition 4.1. A BiKAT over the KAT (A, B, +, ·, ∗, ¬, 1, 0) is a KAT ( A, ¥ ⊕, #, ⊛, ¬, ¥ 0)
                                                                                        ¥ 1, ¥ with
                                    ¥           ¥
KAT homomorphisms h_] : A → A and [_i : A → A, which we call the left and right embeddings,
that satisfy left-right commutativity:
                                (𝐿𝑅𝐶)           h𝑥] # [𝑦i = [𝑦i # h𝑥]         for all 𝑥, 𝑦 in A.
                                                                    ¥ are.
We call A the underlying KAT. A BiKAT is *-continuous if both A and A
   For h_] to be a KAT homomorphism means the following:
     • h𝑥] ∈ B¥ for all 𝑥 ∈ B
     • h0] = 0, h1] = 1¥ , and h¬𝑥] = ¬h𝑥] for all 𝑥 ∈ B
             ¥
     • h𝑥 + 𝑦] = h𝑥] ⊕ h𝑦], h𝑥 · 𝑦] = h𝑥] # h𝑦], and h𝑥 ∗ ] = h𝑥] ⊛ for all 𝑥, 𝑦 in A
Mutatis mutandis for [_i.
   An obvious generalization is to consider two diﬀerent underlying KATs (e.g., modeling source
and target semantics, for compiler correctness). It is also possible to generalize to 𝑘-KATs; we
return to this in Sect. 7.6. But our focus is on 2-trace properties. Specializing to 2 lets us streamline
notation and use convenient “left/right” terminology.
   Deﬁne h_ | _i by
                                                        ˆ h𝑎] # [𝑏i
                                                h𝑎 | 𝑏i =
We call this the two-argument embedding. Note that h𝑎] = h𝑎 | 1i and [𝑎i = h1 | 𝑎i because [1i = 1¥
and 1¥ is the identity element of #. Another immediate consequence is that h_ | _i is a homomor-
phism to A from the product KAT A × A, with the additional property that h0 | 𝑎i = 0 = h𝑎 | 0i for
all 𝑎 ∈ A.3 In case A is a relational model of KAT, the elements of A × A are pairs of relations on
some set Σ. By contrast, the relational BiKAT over A will comprise relations on Σ × Σ (Sect. 4.2).
   Being KAT homomorphisms, the embeddings send tests to tests. For tests 𝑝, 𝑞 in A we have
¬h𝑝 | 𝑞i = ¬(h𝑝] # [𝑞i) = h¬𝑝] ⊕ [¬𝑞i by homomorphism and de Morgan.
   We use identiﬁers 𝐴, 𝐵, 𝐶 . . . for elements of A     ¥ and 𝑃, 𝑄, 𝑅, 𝑆 . . . for bitests, i.e., elements of B.
                                                                                                               ¥
While we use fancy symbols 1,    ¥ ⊕, #, . . . in Def. 4.1 to distinguish between the BiKAT’s operations
and those of the underlying KAT, we usually use the simpler +, · or ;, ¬, etc., for both levels of a
BiKAT since the types can be inferred from context.
   The ∀∀ judgment 𝑐 | 𝑐 ′ : 𝑅 ≈> 𝑆 can be interpreted in any BiKAT, provided 𝑅 and 𝑆 are bitests
and 𝑐 and 𝑐 ′ are actions in the underlying KAT. It is like the Hoare triple equation:
                                                      𝑅; h𝑐 | 𝑐 ′ i; ¬𝑆 = 0                                                     (2)
Deﬁning the judgment this way is justiﬁed in terms of the standard models (see Sect. 4.2 and
Theorem 4.6).
   In applications of KAT, one reasons under hypotheses that specify the interpretation of primitive
tests and actions. For many applications it suﬃces to use hypotheses in the form of Hoare triples. In
applications of BiKAT we can use relational Hoare triple hypotheses to specify the interpretation
of primitive bitests, usually with respect to embedded unary actions. The key point is to leverage
the use of such hypotheses by rewriting the given veriﬁcation task into a conveniently aligned
form. This can be done in ad hoc ways but several general patterns can be identiﬁed.
3 An equivalent way to deﬁne BiKAT is to take h_ | _i as primitive and deﬁne h𝑎] = h𝑎 | 1i and [𝑎i = h1 | 𝑎i. Then we

get left-right commutativity because h𝑎]; [𝑏 i = h𝑎 | 1i; h1 | 𝑏 i = h𝑎; 1 | 1; 𝑏 i = h1; 𝑎 | 𝑏; 1i = h1 | 𝑏 i; h𝑎 | 1i = [𝑏 i; h𝑎].
For h_] and [_i deﬁned this way to be homomorphisms requires the property h0 | 𝑎i = 0 = h𝑎 | 0i since in A × A the
values (𝑎, 0), (0, 0), and (0, 𝑎) are diﬀerent in general. Since left-right commutativity is the key property we care about,
we choose a formulation that highlights it.

                                    Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:8    Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


   The following general law is useful for reasoning about two loops while 𝑒 do 𝑐 and while 𝑒 ′ do 𝑐 ′ .
They are aligned lockstep, under a common star, with a remainder to account for whichever may
iterate longer.4 Here 𝑒, 𝑒 ′ are tests in the underlying KAT.

          h(𝑒; 𝑐) ∗ | (𝑒 ′ ; 𝑐 ′ ) ∗ i; h¬𝑒 | ¬𝑒 ′ i = h𝑒; 𝑐 | 𝑒 ′ ; 𝑐 ′ i ∗ ; (h𝑒; 𝑐 | ¬𝑒 ′ i ∗ + h¬𝑒 | 𝑒 ′ ; 𝑐 ′ i ∗ ); h¬𝑒 | ¬𝑒 ′ i   (3)

This holds in any BiKAT, i.e., it follows by equational reasoning from Def. 4.1. (see appendix
of Antonopoulos et al. [2022a]). Note that h(𝑒; 𝑐) ∗ | (𝑒 ′ ; 𝑐 ′ ) ∗ i; h¬𝑒 | ¬𝑒 ′ i = h(𝑒; 𝑐) ∗ ; ¬𝑒 | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i
by LRC.
   The standard models of BiKAT have additional structure that we formalize as follows.

  Deﬁnition 4.2. A BiKAT with projections is a BiKAT together with total functions ւ : A   ¥ →A
        ¥ → A to its underlying KAT, that satisfy the following for all 𝑎 in A and 𝐴, 𝐵 in A.
and ց : A                                                                                   ¥

                 (Inversion)                  ւh𝑎] = 𝑎                                    ց[𝑎i = 𝑎
                 (Disjointness)               𝑎 ≠ 0 ⇒ ւ[𝑎i = 1¥                           𝑎 ≠ 0 ⇒ ցh𝑎] = 1¥
                 (Disjunctivity)              ւ(𝐴 ⊕ 𝐵) = ւ𝐴 + ւ𝐵                          ց(𝐴 ⊕ 𝐵) = ց𝐴 + ց𝐵

   Projections are not required to distribute over sequence or star. For most of our development,
the projections are not needed. However, they exist in the standard models and they do serve a
purpose that raises open problems discussed in Sect. 7.6.
   For BiKATs with projections, we get the following easy consequences. Only the ﬁrst condition
is expressed using projection, but all of them are proved using projection properties.

   Lemma 4.3. In any BiKAT with projections, we have
                  (Unit)              ւ1¥ = 1 = ց1¥
                  (Separation)        h𝑎] = [𝑏i ∧ (𝑎 ≠ 0 ∨ 𝑏 ≠ 0) ⇒ 𝑎 = 𝑏 = 1
                  Order Separation) h𝑎] ≥ [𝑏i ∧ 𝑎 ≠ 0 ≠ 𝑏 ⇒ 𝑎 ≥ 1 ∧ 1 ≥ 𝑏
                  (Injectivity)       h𝑎] = h𝑏] ⇒ 𝑎 = 𝑏 and same for [_i
                  (Order-Injectivity) h𝑎] ≥ h𝑏] ⇒ 𝑎 ≥ 𝑏 and same for [_i

   An attractive aspect of KAT is that implications ℎ𝑦𝑝𝑜𝑡ℎ ⇒ 𝑐 = 𝑑 are decidable provided the
hypotheses are of the form 𝑏 = 0 which includes the KAT encoding of Hoare triples. On the other
hand, implications with general commutativity hypotheses are undecidable [Kozen and Smith 1996].
One proof goes by reduction to the Post correspondence problem, and the proof idea can be adapted
to BiKAT embeddings in such a way that the commutativity conditions are expressed by LRC (see
appendix of Antonopoulos et al. [2022a]). It should be noted that the original argument is pre-
sented for ∗-continuous KATs and as such our proof is over ∗-continuous BiKATs.

   Theorem 4.4. It is undecidable whether a given identity holds in all ∗-continuous BiKATs.

   We do not need decidability in order to derive useful alignments for speciﬁc programs, and to
derive general laws like (3). Consider a given veriﬁcation problem 𝑅; h𝑐 | 𝑐 ′ i; ¬𝑆 = 0. Alignment
reasoning, using LRC and its consequences, transforms it to a problem of the form 𝑅; 𝐵; ¬𝑆 = 0
that is proved using unary and relational Hoare-triple hypotheses. For that matter, having used
BiKAT to obtain well-aligned 𝐵, veriﬁcation subtasks in 𝐵 can be solved by whatever method you
like.

4 This is the most ﬂexible loop alignment available in some systems, e.g., Cartesian Hoare logic [Sousa and Dillig 2016].



Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                                     20:9


4.2 Models of BiKAT
Elements of a relational or trace KAT can be seen as sets of observations, where an observation
may be a proper trace or just a pair (initial,ﬁnal) of states. Elements of a BiKAT are meant to be
sets of observation pairs. We will describe trace models of BiKAT this way. For relational BiKATs,
however, we use a slightly diﬀerent representation that facilitates spelling out connections with
relational Hoare logics etc.
   First, some deﬁnitions. Let 𝑅 and 𝑆 be relations on some set Σ. Deﬁne 𝑅 ⊗ 𝑆 to be the relation
on Σ × Σ such that (𝜎, 𝜎 ′) (𝑅 ⊗ 𝑆) (𝜏, 𝜏 ′ ) iﬀ 𝜎𝑅𝜏 and 𝜎 ′𝑆𝜏 ′. If 𝑅 and 𝑆 are the denotations of two
programs, 𝑅 ⊗ 𝑆 relates a pair (𝜎, 𝜎 ′ ) interpreted as initial states to a ﬁnal pair (𝜏, 𝜏 ′). (To strictly
model the idea of observation pair, one would use ((𝜎, 𝜏), (𝜎 ′, 𝜏 ′)) instead of ((𝜎, 𝜎 ′), (𝜏, 𝜏 ′)).)
   For relation 𝑅 on Σ, the relations h𝑅] and [𝑅i on Σ × Σ are deﬁned by h𝑅] = 𝑅 ⊗ 𝑖𝑑 Σ and
[𝑅i = 𝑖𝑑 Σ ⊗ 𝑅. (We write 𝑖𝑑 or 𝑖𝑑 Σ for the identity relation on Σ.) In terms of states, we have
               (𝜎, 𝜎 ′ )h𝑅] (𝜏, 𝜏 ′) ⇔ 𝜎𝑅𝜏 ∧ 𝜎 ′ = 𝜏 ′                       (𝜎, 𝜎 ′) [𝑅i(𝜏, 𝜏 ′) ⇔ 𝜎 ′𝑅𝜏 ′ ∧ 𝜎 = 𝜏
For a relation R on Σ × Σ, deﬁne relations ւR and ցR on Σ by
            𝜎 (ւR)𝜏 ⇔ ∃𝜎 ′, 𝜏 ′ . (𝜎, 𝜎 ′) R (𝜏, 𝜏 ′ )                       𝜎 ′ (ցR)𝜏 ′ ⇔ ∃𝜎, 𝜏 . (𝜎, 𝜎 ′ ) R (𝜏, 𝜏 ′ )   (4)
                                  𝑜                                   𝑜
Equivalently, ւR =    ˆ fst ; R; fst and ցR =  ˆ snd ; R; snd where fst : Σ × Σ → Σ and snd : Σ × Σ →
Σ are the projection functions, treated as relations so we can use the converse operation (written
𝑜 as in [Freyd and Scedrov 1990]) and relational composition (written ;).

   A relational BiKAT over a relational model (A, B, +, ·, ∗, ¬, 1, 0) is ( A,    ¥ B,
                                                                                    ¥ ⊕, #, ⊛, ¬, ¥ 0)
                                                                                               ¥ 1, ¥ such
that A¥ is a set of relations on Σ × Σ and the structure on A  ¥ is a relational model of KAT. Moreover,
both h𝑅] and [𝑅i are in A,  ¥ for any 𝑅 in A, and both ւR and ցR are in A, for any R in A.          ¥ Note
that a relational BiKAT is a BiKAT with projections.
   Given a relation 𝑅 on states, we sometimes write 𝑅¤ for the associated sub-identity in B,          ¥ i.e.,
         ¤ 𝜏 ′) iﬀ 𝜎𝑅𝜎 ′ ∧ 𝜏 = 𝜎 ∧ 𝜏 ′ = 𝜎 ′ . Please note that 𝑖𝑑¤Σ is diﬀerent from 1.
(𝜎, 𝜎 ′ )𝑅(𝜏,                                                                          ¥
   For an example, say a relation 𝑅 is boundedly nondeterministic if for any 𝜎 there are ﬁnitely
many 𝜏 with 𝜎𝑅𝜏. Take A to be all boundedly nondeterministic relations on Σ and A               ¥ to be all
boundedly nondeterministic relations on Σ × Σ.
   A full relational BiKAT is one where the BiKAT and its underlying KAT are full relational
models. The example of boundedly nondeterministic relations is not full; both the underlying KAT
and the BiKAT lack a top.
   For programs 𝑐, 𝑑 (interpreted as relations on Σ) and relations 𝑅, 𝑆 on Σ meant to be pre- and
post-conditions, the ∀∀ judgment 𝑐 | 𝑑 : 𝑅 ≈> 𝑆 is pictured
                                                                 𝑐 ✲
                                                        𝜎       𝜏    𝜏
                                                         ❄       ❄
                                 ∀     𝑅
                                          ❄ 𝑑
                                                       =⇒        ❄
                                                                  𝑆                           (5)
                                         𝜎′      ✲ 𝜏′           𝜏′
                          ′      ′     ′         ′  ′     ′
This is meant to say ∀𝜎, 𝜎 , 𝜏, 𝜏 . 𝜎𝑅𝜎 ∧ 𝜎𝑐𝜏 ∧ 𝜎 𝑑𝜏 ⇒ 𝜏𝑆𝜏 . By deﬁnitions we have the following.
   Lemma 4.5 (adeqacy for relational models). In a relational BiKAT, for any 𝑐, 𝑑, the BiKAT
term h𝑐 | 𝑑i denotes the set of all pairs of 𝑐, 𝑑 computations.5
  Now we can conﬁrm that deﬁning the judgment 𝑐 | 𝑑 : 𝑅 ≈> 𝑆 as the BiKAT equation (2) captures
the semantic condition of (5). Moreover, BiKAT equality preserves adequacy.
5 To be precise, the set of all ( (𝜎, 𝜎 ′ ), (𝜏, 𝜏 ′ )) where (𝜎, 𝜏) ∈ 𝑐 and (𝜎 ′ , 𝜏 ′ ) ∈ 𝑑.



                                       Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:10   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


  Theorem 4.6 (∀∀ soundness for relational models). Suppose that 𝑐, 𝑑 are elements of the
                                                                             ¤ 𝑆¤ that represent 𝑅, 𝑆
underlying KAT of a relational BiKAT, and suppose the sub-identity relations 𝑅,
are among the BiKAT’s tests. Then
  (a) The condition (5) holds iﬀ 𝑅;¤ h𝑐 | 𝑑i; ¬𝑆¤ = 0.
                    ¤            ¤
  (b) For any 𝐵, if 𝑅; h𝑐 | 𝑑i ≤ 𝑅; 𝐵 and 𝑅;¤ 𝐵; ¬𝑆¤ = 0 then (5) holds.

  Proof. For (a) the proof is by mutual implication. If (5) holds then 𝑅;            ¤ h𝑐 | 𝑑i ≤ 𝑅; ¤ h𝑐 | 𝑑i; 𝑆¤ by
deﬁnitions. And 𝑅;  ¤ h𝑐 | 𝑑i ≤ 𝑅; ¤ h𝑐 | 𝑑i; 𝑆¤ is equivalent to 𝑅;
                                                                  ¤ h𝑐 | 𝑑i; ¬𝑆¤ = 0 as a fact about KATs. For
the converse, assume 𝑅;    ¤ h𝑐 | 𝑑i ≤ 𝑅; ¤ h𝑐 | 𝑑i; 𝑆.
                                                     ¤ To show (5), for any states 𝜎, 𝜎 ′, 𝜏, 𝜏 ′ that satisfy the
antecedent in (5), by adequacy Lemma 4.5 the executions are in 𝑅;            ¤ h𝑐 | 𝑑i, so by assumption they
       ¤ h𝑐 | 𝑑i; 𝑆.
are in 𝑅;         ¤ So by deﬁnitions the post states are related by 𝑆.
  For Part (b), if 𝑅;¤ h𝑐 | 𝑑i ≤ 𝑅;¤ 𝐵 then we have that 𝑅;   ¤ 𝐵; ¬𝑆¤ ≤ 0 implies 𝑅; ¤ h𝑐 | 𝑑i; ¬𝑆¤ ≤ 0 by KAT
reasoning. This yields (5) using Part (a).                                                                         
    Part (b) of Theorem 4.6 says that adequacy of 𝐵 for proving 𝑐 | 𝑑 : 𝑅 ≈> 𝑆 is expressed by
the equation 𝑅;       ¤ h𝑐 | 𝑑i ≤ 𝑅;
                                  ¤ 𝐵 (called “𝑅-adequacy” in Nagasamudram and Naumann [2021]). An
adequacy proof can be interwoven with the correctness proof, in a form like 𝑅;                         ¤ h𝑐 | 𝑑i; ¬𝑆¤ ≤ . . . ≤
 ¤ 𝐵; ¬𝑆¤ = . . . = 0. Some of our examples have this form, using equality not ≤.
𝑅;
    A trace BiKAT over trace model (A, B, +, ·, ∗, ¬, 1, 0) is ( A,                ¥ B,
                                                                                      ¥ ⊕, #, ⊛, ¬,  ¥ 0)
                                                                                                   ¥ 1, ¥ where elements
of A ¥ are sets of pairs of traces. To deﬁne #, the coalesced catenation ⋄ is lifted to trace pairs
and used as in ordinary trace models. That is, 𝐴 # 𝐵 = {(𝑡 ⋄ 𝑢, 𝑡 ′ ⋄ 𝑢 ′ ) | (𝑡, 𝑡 ′ ) ∈ 𝐴, (𝑢, 𝑢 ′ ) ∈
𝐵, 𝑡 ⋄ 𝑢 and 𝑡 ′ ⋄ 𝑢 ′ deﬁned}. Sum and star are union and iterated #. For trace set 𝑎, the left embed-
ding h𝑎] is {(𝑡, 𝜎) | 𝑡 ∈ 𝑎 ∧𝜎 ∈ Σ}. For set 𝐴 of trace pairs, the left projection ւ𝐴 is {𝑡 | (𝑡, 𝑢) ∈ 𝐴},
i.e., ւ maps fst over 𝐴. As with relational BiKATs, we require that A                      ¥ contains all the images of
h_] and [_i on A, and A contains the images of ւ and ց on A.                        ¥
    To see why LRC holds in a trace BiKAT, let us write ⊳𝑡 for the ﬁrst state of trace 𝑡 and 𝑡 ⊲ for the
last. For trace sets 𝑐, 𝑐 ′ , and any 𝑡 ∈ 𝑐 and 𝑡 ′ ∈ 𝑐 ′ , we have (𝑡, 𝑡 ′ ) ∈ h𝑐] # [𝑐 ′ i iﬀ (𝑡, ⊳𝑡 ′ ) ∈ h𝑐] and
( ⊲𝑡, 𝑡 ′ ) ∈ [𝑐 ′ i. Note that (𝑡, ⊳𝑡 ′ ) ⋄ ( ⊲𝑡, 𝑡 ′ ) = (𝑡, 𝑡 ′ ). Similarly, we have (𝑡, 𝑡 ′ ) ∈ [𝑐 ′ i # h𝑐]. The upshot
is that h𝑐] # [𝑐 ′ i = [𝑐 ′ i # h𝑐].
    A full trace BiKAT has all trace sets (relative to the given set of admissible traces), for the
underlying KAT, and all pairs of traces for the BiKAT. Like full relational models, full trace models
have a top.
    Lemma 4.5 and Theorem 4.6 can be straightforwardly adapted to trace models.

5    USING BIKAT FOR ∀∀ RELATIONAL REASONING
Having introduced BiKAT we now demonstrate how it can be used to algebraically derive align-
ments and verify ∀∀ properties of a variety of examples that necessitate diﬀerent kinds of align-
ment.
    Simple Example. The following two programs compute the sum of integers up to some 𝑁 .
                                                                               ∗
                                  ˆ
                               𝐶1 =     i:=0; ( [ i ≤ N] ; x:=x+i; i:=i+1) ; ¬[ i ≤ N]
                                                                               ∗
                                  ˆ
                               𝐶2 =     i:=1; ( [ i ≤ N] ; x:=x+i; i:=i+1) ; ¬[ i ≤ N]

To prove the ∀∀ relational judgment 𝐶 1 | 𝐶 2 : h[N ≥ 0]] [x =¥ x] [N =¥ N] ≈> [x =¥ x] without resorting
to functional correctness, we start from h[N ≥ 0]] · [x =¥ x] · [N =¥ N] · h𝐶 1 | 𝐶 2 i · ¬[x =¥ x] = 0 and
then manipulate the sequential composition h𝐶 1 | 𝐶 2 i into an alignment, where we can directly
relate the programs’ variables during loop iterations. In this case, there is a simple alignment: 𝐶 1
does one more iteration than 𝐶 2 , so we unroll its loop once before aligning the two loop bodies in
lockstep. Then, a simple relational loop invariant, [x =¥ x] [i =¥ i], suﬃces to establish equivalence.

Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                            20:11


   Let us now see this step-by-step in the algebra of BiKAT. Unrolling 𝐶 1 ’s loop once, we have that
h𝐶 1 | 𝐶 2 i is equal to:
                                        hi:=0; (1 + 𝐶; 𝐶 ∗ ) ;¬𝑒 | i:=1;𝐶 ∗ ;¬𝑒i
where 𝐶 is the program text (𝑒 ; x:=x+i;i:=i+1) and 𝑒 is [i ≤ N]. Distributing, we get

                                      hi:=0;¬𝑒 + i:=0;𝐶 ;𝐶 ∗ ;¬𝑒 | i:=1;𝐶 ∗ ;¬𝑒i

For semantic reasons, ( i:=0;¬𝑒) is infeasible. So we can assume hypothesis ( i:=0;¬𝑒) = 0 which
lets us eliminate that term. For the other term, we calculate
                   hi:=0;𝐶 ;𝐶 ∗ ;¬𝑒 | i:=1;𝐶 ∗ ;¬𝑒i
              =    hi:=0 | i:=1i ; h𝐶] ; h𝐶 ∗ | 𝐶 ∗ i ; h¬𝑒 | ¬𝑒i        embedding homomorphic
              =    hi:=0] ; [i:=1i ; h𝐶] ; h𝐶 ∗ ] ; [𝐶 ∗ i ; h¬𝑒 | ¬𝑒i   def two-argument embedding
              =    hi:=0] ;h𝐶] ; [i:=1i ; h𝐶 ∗ ] ; [𝐶 ∗ i ; h¬𝑒 | ¬𝑒i    LRC
              =    hi:=0;𝐶 | i:=1i ; h𝐶 ∗ | 𝐶 ∗ i ; h¬𝑒 | ¬𝑒i            embedding homomorphic
Using the expansion lemma (3), h𝐶 ∗ | 𝐶 ∗ i can be rewritten into

                             (h[i ≤ N] ; x:=x+i; i:=i+1 | [i ≤ N] ; x:=x+i; i:=i+1i) ∗

(Eliding terms that cancel out once we introduce the loop invariant.) By systematically using LRC
along with the homomorphism property of embeddings, we align the loop bodies in lockstep:

                           (h[i ≤ N] | [i ≤ N]i ; hx:=x+i | x:=x+ii ; hi:=i+1 | i:=i+1i) ∗

We next add the assumption that [x =¥ x] initially, add relational loop invariant [i =¥ i] [x =¥ x], and
conclude the post-relation [x =¥ x] must hold beyond the loop.
   Double Square (Example 2.2, Sect. 2). Recall the KAT expressions of the two programs:

                                  ˆ y:=0;z:=2*x; ( [z>0];z:=z-1;y:=y+x) ∗ ;[z>0]
                             𝑘𝐷 1 =
                                  ˆ y:=0;z:=x; ( [z>0];z:=z-1;y:=y+x) ∗ ;[z>0];y:=2*y
                             𝑘𝐷 2 =
Note we are using overline as alternate notation for negation.
   In the preceding example, we did a unary unfolding of one iteration on the left, and then aligned
the loops in lockstep. For this example we choose to align two iterations on the left with one
iteration on the right. We ﬁrst use KAT laws to rewrite 𝑘𝐷 1 as:

                         𝑘𝐷 1 = y:=0;z:=2*x; ( [z>0];𝑏 ;[z>0];𝑏) ∗ ; ( [z>0];𝑏 + 1) ;[z>0]

        ˆ z:=z-1;y:=y+x. We then align the two loops and apply the expansion law (3) as follows:
where 𝑏 =

               h( [z>0];𝑏 ;[z>0];𝑏) ∗ | ( [z>0];𝑏) ∗i
          =    h[z>0];𝑏 ;[z>0];𝑏 | [z>0];𝑏i ∗ ; (h[z>0];𝑏 ;[z>0];𝑏 | [z>0]i ∗ + h[z>0] | [z>0];𝑏i ∗ )

  Now it is easier to prove the relational loop invariant I¥ =
                                                             ˆ [𝑦 =¥ 2𝑦] ; [𝑧 =¥ 2𝑧] by proving that it is
preserved across the above expansion loops. In the derivation, we break the proof into sub-proofs
over the embeddings of loop bodies:
                                                                    ¥                                   ¥
                                                                   I ; h[z>0];𝑏 ;[z>0];𝑏 | [z>0];𝑏i ;¬I = 0 ∧
                                                                  
                                                                  
  I¥ ; h( [z>0];𝑏 ;[z>0];𝑏) ∗ | ( [z>0];𝑏) ∗ i ;¬I¥ = 0 ⇐           I¥ ; h[z>0];𝑏 ;[z>0];𝑏 | [z>0]i ;¬I¥ = 0 ∧
                                                                  
                                                                   I¥ ; h[z>0] | [z>0];𝑏i ;¬I¥ = 0
                                                                  

                                 Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:12   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


   Loop Tiling (Example 2.3, Sect. 2). Here are the two programs 𝐿1 , 𝐿2 as KAT expressions:
                   ˆ x:=0; ( [x<N*M];a[x]:=f(x);x:=x+1) ∗ ;x<N*M
              𝑘 𝐿1 =
                   ˆ i:=0; ( [i<N];j:=0; ( [j<M];A[i,j]:=f(i*M+j);j:=j+1) ∗ ;[j<M];i:=i+1) ∗ ;[i<N]
              𝑘 𝐿2 =
For the alignment, we then transform these KAT expressions into two equivalent KAT expressions
which have the same structure.
               𝑘𝐿1 = x:=0; ( [x<N*M];𝑏 1 ; ( [x<N*M];[x%M!=0];𝑏 1 ) ∗ ;[x<N*M];[x%M!=0]) ∗ ;x<N*M
               𝑘𝐿2 = i:=0; ( [i<N];j:=0; ( [j<M];𝑏 2 + [j<M]) ; ( [j<M];𝑏 2 ) ∗ ;[j<M] ;i:=i+1) ∗ ;[i<N]
where 𝑏 1 =   ˆ a[x]:=f(x);x:=x+1 and 𝑏 2 =     ˆ A[i,j]:=f(i*M+j);j:=j+1. We next prove the judgment
𝑃¥; h𝑘𝐿1 | 𝑘𝐿2 i ;¬𝑄¥ = 0 with the pre-relation 𝑃¥ =       ˆ [N =¥ N] ; [M =¥ M] ;[N > 0];[M > 0] and the post-
relation 𝑄¥ = ˆ [R ( N × M, N, M)], where R (𝑥, 𝑖, 𝑗 ) is a predicate6 that says every element of the array a
up to the index 𝑥 is equal to its corresponding element of the two-dimensional array A up to the
index 𝑖, 𝑗 . To prove the above judgment, we use the relational invariant I¥ =         ˆ [i < N];[j ≤ M];[x=¥ i ×
M + j]; [R ( x, i, j)] for the inner loops and the relational invariant J     ¥ =
                                                                                ˆ [i ≤ N];[x=¥ i × M]; [R (x, i, 0)]
for the outer loops.
   Loop Summaries and Procedure Calls. KAT is a
propositional theory of imperative control struture.
                                                        arrayInsert (A , len , h ) {
In KAT-based systems, ﬁrst order state variables,          i := 0;
conditions, and assignments can be handled using           while (i < len && A [ i ] < h) i ++;
hypotheses (typically, Hoare triples) that axioma-         len := shift_array (A , i , 1) ;
tize their semantics.                                      A [i ] := h;
   Here too, the KATs embedded in a BiKAT are              while (i < len ) i ++;
parametric over alphabets of actions and tests and         return i ;
hypotheses about those tests. Consequently BiKAT }
inherently supports reasoning at coarser or ﬁner
granularies. Moreover, this parameterization allows BiKAT to be used in concert with other proce-
dures (e.g. loop summarization, procedure specs/summaries, ghost states, prophecy variables, etc.)
which could be applied beforehand and then incorporated into a BiKAT through the primitive
actions and hypothesis. For example, consider the array insertion procedure7 [Goyal et al. 2021;
Shemer et al. 2019] shown to the right that will illustrate the use of externally-provided unary pro-
cedure summaries. The goal is to prove that, arrayInsert | arrayInsert : [len =¥ len] [A =¥ A] ≈> [i =¥ i]
i.e., the noninterference property that there is no leak on h.
   Contrary to some examples above, this example does not require loop bodies to be lock-step
aligned. It does, however, require alignment between intermediate points between the loops. Specif-
ically, the programs must be aligned in three places: after both have completed their ﬁrst loop, after
both have completed the call to shift_array (incorporating that method’s post-condition), and after
both of completed their second loop. That is, the BiKAT alignment:
                [len =¥ len]; hwhile(...)i++ | while(...)i++i; [len =¥ len]; h[i<=len] | [i<=len]i;
                   hlen := shift_array(...) | len := shift_array(...)i; [len+1 =¥ len+1];
                   hwhile(i<len)i++; [i=len]]; [while(i<len)i++; [i=len]i; [i =¥ i]
We ﬁrst use the pre-relation [len =¥ len] and the postcondition of the ﬁrst loop on both the left and
right sides, aligning when both sides have completed to show that [len =¥ len] still holds, while
i ≤ len (on the left) and i′ ≤ len ′ (on the right).

6 R (𝑥, 𝑖, 𝑗 ) =
               ˆ ∀𝑙, 𝑟, 𝑐. 0 ≤ 𝑙 < 𝑥 ∧0 ≤ 𝑟 < 𝑖 ∧ (𝑟 < 𝑖 − 1 ∧0 ≤ 𝑐 < M ∨𝑟 = 𝑖 − 1 ∧0 ≤ 𝑐 < 𝑗 ) ∧𝑙 = 𝑟 × M +𝑐 ⇒ [a [𝑙 ] =A
                                                                                                                        ¥ [𝑟, 𝑐 ] ]
7 The second loop sets i to len in a way that avoids a timing channel but we are not modeling timing here.



Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                                    20:13


                                                                 𝑐 | 𝑐 ′ : 𝑃 ≈> 𝑅       𝑑 | 𝑑 ′ : 𝑅 ≈> 𝑄
                                                       dSeq
                                                                         𝑐; 𝑑 | 𝑐 ′; 𝑑 ′ : 𝑃 ≈> 𝑄

                      ¥ ′
                𝑃 ⇒ 𝑒 =𝑒      𝑐 | 𝑐 ′ : 𝑃 ∧ h𝑒] ∧ [𝑒 ′ i ≈> 𝑄        𝑑 | 𝑑 ′ : 𝑃 ∧ ¬h𝑒] ∧ ¬[𝑒 ′i ≈> 𝑄
          dIf
                              if 𝑒 then 𝑐 else 𝑑 | if 𝑒 ′ then 𝑐 ′ else 𝑑 ′ : 𝑃 ≈> 𝑄

                      ¥ ′
                𝑃 ⇒ 𝑒 =𝑒       𝑐 | 𝑐 ′ : 𝑃 ∧ h𝑒] ∧ [𝑒 ′ i ≈> 𝑃                          𝑐 | 𝑑 : 𝑃 ≈> 𝑄        𝑐 | 𝑑 : 𝑅 ≈> 𝑄
    dWh                         ′      ′                             ′          rDisj
          while 𝑒 do 𝑐 | while 𝑒 do 𝑐 : 𝑃 ≈> 𝑃 ∧ ¬h𝑒] ∧ ¬[𝑒 i                                𝑐 | 𝑑 : 𝑃 ∨ 𝑅 ≈> 𝑄

          𝑐 | skip : 𝑃 ≈> 𝑅     𝑑 | skip : 𝑅 ≈> 𝑄                                   𝑅⇒𝑃        𝑐 | 𝑑 : 𝑃 ≈> 𝑄        𝑄 ⇒𝑆
 SeqSk                                                               rConseq
                    𝑐; 𝑑 | skip : 𝑃 ≈> 𝑄                                                     𝑐 | 𝑑 : 𝑅 ≈> 𝑆

                                    Fig. 1. Selected inference rules of ∀∀ logic



   At this point we have established the alignment necessary for this example. Completing the
proof requires small semantic hypotheses (similar to those in earlier examples) and some strategy
for establishing [len =¥ len] is preserved across the procedure call to shift_array. One option is
to introduce relational hypothesis shift_array(A,i,j) | shift_array(A,i,j) : [len =¥ len] [j =¥ j] ≈>
[len =¥ len] which ensures agreement on len after the embedded procedures. Alternatively, one
could employ a unary speciﬁcations of the form {}shift_array(A,i,j){len=old(len)+j} through the
use of KAT hypotheses of the form 𝑝𝐶¬𝑞 = 0 embedded on the left and the right. These unary
post-conditions can be combined with the pre-call [len =¥ len] to add a post-call bitest [len =¥ len].
Here there are some details that would be needed (e.g. ghost variables) to support post-condition
tests that relate variables to pre-conditions. Finally, we use [len =¥ len] with the post-conditions of
the last loops that i = len on both sides to conclude that [i =¥ i].

6    RELATIONAL HOARE LOGIC IN BIKAT
In this section we show that relational Hoare logic rules can be derived in any BiKAT. Relational
logics involve two programs, thus quadruples, sometimes written {𝑃 }𝑐 ∼ 𝑐 ′ {𝑄 } for commands
𝑐, 𝑐 ′ . Benton [2004] writes 𝑐 ∼ 𝑐 ′ : 𝑃 ⇒ 𝑄. We consider inference rules for the ∀∀ judgment form
𝑐 | 𝑐 ′ : 𝑃 ≈> 𝑄 introduced in Sect. 1 and expressed in any BiKAT by the equation (2).

   Deriving Rules of RHL. A number of publications have presented variations on relational Hoare
logic. We consider a number of basic rules that can be found in Benton’s inﬂuential paper [Benton
2004] and in Francez’ less known paper [Francez 1983], and a number of subsequent works. There
is not yet a standard set of rules, in part because until recently there was no satisfactory notion
of completeness [Nagasamudram and Naumann 2021; Naumann 2020]. We consider a number of
representative rules in Fig. 1.
   In the rules we use suggestive syntax for formulas and programs, and we will not belabor the
distinction between program syntax and its standard representation in KAT. We lift boolean ex-
pression 𝑒 to a relation formula h𝑒] that says 𝑒 is true in the left state, so its representation as a
test in BiKAT will look the same.
   We will show that all the rules are sound in any BiKAT. Recall that we interpret the judgment
𝑐 | 𝑐 ′ : 𝑃 ≈> 𝑄 as the BiKAT equation 𝑃; h𝑐 | 𝑐 ′ i; ¬𝑄 = 0. In the soundness proofs we use the
equivalent form 𝑃; h𝑐 | 𝑐 ′ i ≤ 𝑃; h𝑐 | 𝑐 ′ i; 𝑄. This form is also used in Kozen’s work deriving Hoare
logic rules in KAT [Kozen 2000].

                                Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:14   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


   Several rules in Fig. 1 infer “diagonal” judgments relating two same-structured programs, e.g.,
dSeq, dIf, and dWh. The latter two cater for alignment whereby the same control path is followed,
with a requirement of agreement on conditional tests. There is a rule dIf4, named after the number
of its premises, does not require such agreement.
   Some of the rules can be derived from others. Regarding rule SeqSk, from its premises one can
use dSeq to obtain 𝑐; 𝑑 | skip; skip : 𝑃 ≈> 𝑄. But the inference rules provide no way to replace
skip; skip by the equivalent skip. One of the beneﬁts of working in KAT is free use of such equiva-
lences, including more interesting ones like loop unrolling in the Tiling example.
   Rule dIf can be derived from dIf4 using rule FalsePre and rConseq, but we prove dIf directly.
The side condition 𝑃 ⇒ 𝑒 =𝑒  ¥ ′ is most directly expressed as 𝑃 ≤ 𝑒 =𝑒
                                                                     ¥ ′ . The left-right equality 𝑒 =𝑒
                                                                                                     ¥ ′
                       ′            ′
is equivalent to h𝑒 | 𝑒 i + h¬𝑒 | ¬𝑒 i so the side condition yields
                                              𝑃; h𝑒 | ¬𝑒 ′ i = 0           𝑃; h¬𝑒 | 𝑒 ′ i = 0                                    (6)
To prove soundness of dIf we calculate:
                          𝑃; h𝑒; 𝑐 + ¬𝑒; 𝑑 | 𝑒 ′ ; 𝑐 ′ + ¬𝑒 ′ ; 𝑑 ′i
                    =     𝑃; h𝑒 | 𝑒 ′ i; h𝑐 | 𝑐 ′ i + 𝑃; h𝑒 | ¬𝑒 ′ i; h𝑐 | 𝑑 ′ i                   emb homo, distrib
                          + 𝑃; h¬𝑒 | 𝑒 ′ i; h𝑑 | 𝑐 ′ i + 𝑃; h¬𝑒 | ¬𝑒 ′ i; h𝑑 | 𝑑 ′ i
                    =     𝑃; h𝑒 | 𝑒 ′ i; h𝑐 | 𝑐 ′ i + 𝑃; h¬𝑒 | ¬𝑒 ′ i; h𝑑 | 𝑑 ′i                   using (6)
                    ≤     𝑃; h𝑒 | 𝑒 ′ i; h𝑐 | 𝑐 ′ i; 𝑄 + 𝑃; h¬𝑒 | ¬𝑒 ′ i; h𝑑 | 𝑑 ′i; 𝑄             premises of dIf
                    =     𝑃; h𝑒; 𝑐 + ¬𝑒; 𝑑 | 𝑒 ′ ; 𝑐 ′ + ¬𝑒 ′ ; 𝑑 ′i; 𝑄                            reverse steps
   To prove dWh, ﬁrst observe
    𝑃; (h𝑒; 𝑐 | ¬𝑒 ′ i ∗ + h¬𝑒 | 𝑒 ′ ; 𝑐 ′ i ∗ )
  = 𝑃; (1 + h𝑒; 𝑐 | ¬𝑒 ′ i; h𝑒; 𝑐 | ¬𝑒 ′ i ∗ ) + 𝑃; (1 + h¬𝑒 | ¬𝑒 ′ ; 𝑐 ′ i; h¬𝑒 | 𝑒 ′ ; 𝑐 ′ i ∗ )            distrib, star unfold
  = 𝑃 + 𝑃; h𝑒; 𝑐 | ¬𝑒 ′ i; h𝑒; 𝑐 | ¬𝑒 ′ i ∗ + 𝑃 + 𝑃; h¬𝑒 | ¬𝑒 ′ ; 𝑐 ′ i; h¬𝑒 | 𝑒 ′ ; 𝑐 ′ i ∗                  distrib
  = 𝑃                                                                                                         using (6)
The last step uses that embedding is homomorphic, and the side condition (6) whence 𝑃 +0+𝑃 +0 =
𝑃. Using the premise 𝑃; h𝑒 | 𝑒 ′ i; h𝑐 | 𝑐 ′ i ≤ 𝑃; h𝑒 | 𝑒 ′ i; h𝑐 | 𝑐 ′ i; 𝑃, we get the conclusion of dWh by
        𝑃; h(𝑒; 𝑐) ∗ ; ¬𝑒 | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i
  =     𝑃; h(𝑒; 𝑐) ∗ | (𝑒 ′ ; 𝑐 ′ ) ∗ i; h¬𝑒 | ¬𝑒 ′ i                                                  emb homo
  =     𝑃; h𝑒; 𝑐 | 𝑒 ′ ; 𝑐 ′ i ∗ ; (h𝑒; 𝑐 | ¬𝑒 ′ i ∗ + h¬𝑒 | 𝑒 ′ ; 𝑐 ′ i ∗ ); h¬𝑒 | ¬𝑒 ′ i             expansion (3)
  ≤     𝑃; h𝑒; 𝑐 | 𝑒 ′ ; 𝑐 ′ i ∗ ; 𝑃; (h𝑒; 𝑐 | ¬𝑒 ′ i ∗ + h¬𝑒 | 𝑒 ′ ; 𝑐 ′ i ∗ ); h¬𝑒 | ¬𝑒 ′ i          premise, invariance
  =     𝑃; h𝑒; 𝑐 | 𝑒 ′ ; 𝑐 ′ i ∗ ; 𝑃; h¬𝑒 | ¬𝑒 ′ i                                                     observation above
  =     𝑃; h𝑒; 𝑐 | 𝑒 ′ ; 𝑐 ′ i ∗ ; 𝑃; h¬𝑒 | ¬𝑒 ′ i; 𝑃                                                  tests idem, tests commute
  =     𝑃; h𝑒; 𝑐 | 𝑒 ′ ; 𝑐 ′ i ∗ ; 𝑃; (h𝑒; 𝑐 | ¬𝑒 ′ i ∗ + h¬𝑒 | 𝑒 ′ ; 𝑐 ′ i ∗ ); h¬𝑒 | ¬𝑒 ′ i; 𝑃       observation, in reverse
  ≤     𝑃; h𝑒; 𝑐 | 𝑒 ′ ; 𝑐 ′ i ∗ ; (h𝑒; 𝑐 | ¬𝑒 ′ i ∗ + h¬𝑒 | 𝑒 ′ ; 𝑐 ′ i ∗ ); h¬𝑒 | ¬𝑒 ′ i; 𝑃          𝑃 ≤ 1 since 𝑃 is a test
  =     𝑃; h(𝑒; 𝑐) ∗ ; ¬𝑒 | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i; 𝑃; h¬𝑒 | ¬𝑒 ′ i                                   reverse steps using (3)
   Theorem 6.1. The rules of Fig. 1 are sound in any BiKAT.
  To cater for reasoning about related loops where data-dependent alignment is needed, the fol-
lowing rule caWh for conditionally aligned loops has been shown sound for speciﬁc models in
prior work [Banerjee et al. 2022; Beringer 2011; Nagasamudram and Naumann 2021]. The rule fea-
tures relations 𝑄 (resp. 𝑅) as conditions under which an iteration on one side is aligned with doing
nothing on the other side.
                         𝑐 | 𝑐 ′ : 𝑃 ∧ h𝑒] ∧ [𝑒 ′ i ∧ ¬𝑄 ∧ ¬𝑅 ≈> 𝑃     𝑐 | skip : 𝑃 ∧ 𝑄 ∧ h𝑒] ≈> 𝑃
                          skip | 𝑐 ′ : 𝑃 ∧ 𝑅 ∧ [𝑒 ′ i ≈> 𝑃          ¥ ′ ∨ (𝑄 ∧ h𝑒]) ∨ (𝑅 ∧ [𝑒 ′ i)
                                                              𝑃 ⇒ 𝑒 =𝑒
               caWh
                                     while 𝑒 do 𝑐 | while 𝑒 ′ do 𝑐 ′ : 𝑃 ≈> 𝑃 ∧ ¬h𝑒] ∧ ¬[𝑒 ′ i

Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                                       20:15


The rule can be used together with the one-side rules like SeqSk. To prove caWh we use this
expansion law:
        h𝑒; 𝑐] ∗ ; h¬𝑒]; [𝑒 ′ ; 𝑐 ′ i ∗ ; [¬𝑒 ′ i   =   (𝑄; h𝑒; 𝑐] + 𝑅; [𝑒 ′ ; 𝑐 ′ i + ¬𝑄; ¬𝑅; h𝑒; 𝑐 | 𝑒 ′ ; 𝑐 ′ i
                                                                                                                              (7)
                                                             +¬𝑄; h𝑒; 𝑐 | ¬𝑒 ′ i + ¬𝑅; h¬𝑒 | 𝑒 ′ ; 𝑐 ′ i) ∗ ; h¬𝑒 | ¬𝑒 ′ i
We do not know whether (7) holds in all BiKATs, but it holds in relational BiKATs and trace BiKATs.
    Theorem 6.2. (a) Law (7) holds in any *-continuous BiKAT.
    (b) Rule caWh is sound in any BiKAT that satisﬁes (7).
    Example 6.3. Consider the following, adapted from Naumann [2020].
           𝑃1 :      y:=x; z:=24; w:=0; while y>4 do if w%2=0 then z:=z*y; y:=y-1 fi; w:=w+1 od
           𝑃2 :      y:=x; z:=16; w:=0; while y>4 do if w%3=0 then z:=z*2; y:=y-1 fi; w:=w+1 od

For x ≥ 4, 𝑃1 computes x! in z and 𝑃2 , 2x in z. We want to show that 𝑃1 majorizes 𝑃2 , i.e., 𝑃1 | 𝑃2 :
  ¥ x ′ ≈> z > z′ (using primed variables to refer to those in 𝑃2 ). Notice that both programs take
x =
gratuitous steps, making it diﬃcult to reason by a simple lockstep alignment of the two loops—
the relational loop invariant would become needlessly complicated. Veriﬁcation can be simpliﬁed
by using the following data-dependent alignment: if hw%2 ≠ 0], perform a left-only iteration; if
[w%3 ≠ 0i, perform a right-only iteration; otherwise, if hw%2 = 0 | w%3 = 0i, execute the loop bodies
jointly. Then, y =¥ y′ ∧ z > z ′ > 0 is invariant and suﬃcient to establish the postrelation. This
reasoning is done using rule caWh in Nagasamudram and Naumann [2021]. An alternative is to
reason in BiKAT with the following alignment:
         hy:=x | y:=xi; hz:=24 | z:=16i; hw:=0 | w:=0i;
           h[w%2 ≠ 0]; w:=w+1] + [[w%3 ≠ 0]; w:=w+1i                               ∗
         + h[w%2=0] | [w%3=0]i; hz:=z*y; y:=y-1; w:=w+1 | z:=z*2; y:=y-1; w:=w+1 i; ; h¬[y>4] | ¬[y>4]i.
It can be derived by starting with [x =¥ x ′ ]; h𝑃1 | 𝑃2 i, using (7) with 𝑄 := hw%2 ≠ 0] and 𝑅 := [w%2 ≠ 0i,
and then simplifying, relying on the loop invariant which cancels the ¬𝑄 and ¬𝑅 cases in (7).
   Self-Composition Rule. Researchers have repeatedly discovered that relational correctness can
be encoded in (unary) Hoare logic, essentially because a pair of states can be represented by a
single state, e.g., using renamed variables [Barthe et al. 2004; Francez 1983]. A state relation 𝑃 can
                                   ˆ and a command 𝑐 can be renamed to 𝑐ˆ acting on the alternate
be expressed by a state predicate 𝑃,
variables. Then the judgment 𝑐 | 𝑑 : 𝑃 ≈> 𝑄 is represented by the Hoare triple 𝑐; 𝑑ˆ : 𝑃ˆ ❀ 𝑄.       ˆ
(We write 𝑐 : 𝑝 ❀ 𝑞 for {𝑝 }𝑐{𝑞}.) A complete relational Hoare logic thereby comprises the single
rule, “from 𝑐; 𝑑ˆ : 𝑃ˆ ❀ 𝑄ˆ infer 𝑐 | 𝑑 : 𝑃 ≈> 𝑄”, together with a complete (unary) Hoare logic.
In terms of alignment, of course, this is the most degenerate form of reasoning. The notion of
alignment completeness explains the need for other rules, in terms of alignment of automata;
see Nagasamudram and Naumann [2021].

7    BEYOND 2-SAFETY: PROPERTIES AND LOGICS
Many relational requirements can be expressed as instances of the ∀∀ (2-safety) form depicted in
(5), or other conditions that must hold for all pairs of behaviors. Some other frameworks, such as
HyperLTL [Clarkson et al. 2014], can express properties with other patterns of quantiﬁcation. In
Sect. 7.1 we consider, two ∀∃ patterns based on pre- and post-relations the way (5) is. In Sect. 7.5 we
consider ∃∀ and ∃∃ properties, for the sake of systematic exploration. The discussion focuses on
relational models for concreteness, though the goal is model-independent algebraic formulations.

                                      Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:16   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


7.1 ∀∃ Properties
For programs that may be nondeterministic, the ∀∀ property depicted in (5) is often too strong.
A range of interesting requirements such as possibilistic noninterference and data reﬁnement are
                                                                                             ∃
expressed in a ∀∃ form. We call it forward simulation and write 𝑐 | 𝑑 : 𝑅 ≈> 𝑆 for the following.

                                             𝑐
                                      𝜎           ✲𝜏                                   𝜏
                                       ❄                                                 ❄
                         ∀        𝑅
                                    ❄
                                                               ∃                         ❄
                                                                                          𝑆              (8)
                                                                                 𝑑
                                   𝜎′                                   𝜎   ′         ✲𝜏 ′

Here 𝜎, 𝜎 ′, 𝜏, 𝜏 ′ are states and 𝑐, 𝑑, 𝑅, 𝑆 are relations, so (8) says
                                  ∀𝜎, 𝜎 ′, 𝜏 . 𝜎𝑅𝜎 ′ ∧ 𝜎𝑐𝜏 ⇒ ∃𝜏 ′ . 𝜎 ′𝑑𝜏 ′ ∧ 𝜏𝑆𝜏 ′
An equivalent “point-free” formulation, using relation algebra, is 𝑅𝑜 ; 𝑐 ⊆ 𝑑; 𝑆 𝑜 . (Recall from Sect. 4.2
that 𝑅𝑜 means the converse of 𝑅.)
  For possibilistic noninterference, 𝑐 = 𝑑 and the relations express low indistinguishability: 𝑅
expresses agreement on low inputs and 𝑆 on low outputs. In the case of data reﬁnement, 𝑅 = 𝑆
and 𝑅 captures some change of data representation.
  For program reﬁnement one sometimes needs the similar ∀∃ property called backward simu-
                              ∃
lation, written 𝑐 | 𝑑 : 𝑅 ≈> 𝑆 .

                                              𝑐
                                      𝜎            ✲𝜏                      𝜎
                                                     ❄                      ❄
                          ∀                          ❄
                                                      𝑆         ∃      𝑅
                                                                         ❄
                                                                                                         (9)
                                                                                  𝑑
                                                    𝜏′                  𝜎′                ✲ 𝜏′
This is expressed in relation algebra as 𝑐; 𝑆 ⊆ 𝑅; 𝑑, and pointwise as
                                  ∀𝜎, 𝜏, 𝜏 ′ . 𝜎𝑐𝜏 ∧ 𝜏𝑆𝜏 ′ ⇒ ∃𝜎 ′ . 𝜎𝑅𝜎 ′ ∧ 𝜎 ′𝑑𝜏 ′
   In Sect. 7.2 we give theorems that characterize the forward and backward simulation properties
in terms of existence of BiKAT witnesses. Using those theorems, we derive (Sect. 7.4) rules for
                                   ∃                 ∃
inferring judgments 𝑐 | 𝑑 : 𝑅 ≈> 𝑆 and 𝑐 | 𝑑 : 𝑅 ≈> 𝑆. In Sect. 7.6 we show how forward and
backward simulation can be expressed in closed form, by generalizing BiKAT to a kind of 3-KAT.
   As an aside, we note that the simulation properties subsume unary underapproximation. For
unary tests 𝑝, 𝑞, the incorrectness logic [O’Hearn 2019] judgment “every state in 𝑞 can be reached
                                                                                 ∃
by a terminating execution of 𝑐 from some state in 𝑝” is equivalent to [𝑐i : [𝑝i ≈> [𝑞i. The forward
approximation condition “for every state in 𝑝 there is a terminating execution of 𝑐 that ends in 𝑞”
                            ∃
is equivalent to [𝑐i : [𝑝i ≈> [𝑞i.

7.2 BiKAT Characterizations of Simulation
Alignment is well known to play a role in verifying ∀∃ properties. Example 2.4 in Sect. 2 illustrates
that one aligns the computations in a convenient way, in order to winnow out execution pairs
in which the second execution makes undesirable nondeterministic choices. Bitests can serve as
assume statements for this purpose.
  Theorem 7.1 (forward witness soundness). In a relational BiKAT over a KAT with top, we
                                  ∃
have forward simulation 𝑐 |𝑑 : 𝑅 ≈> 𝑆 if there is some BiKAT term 𝑊 , called alignment witness,

Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                                               20:17


that is f-valid, which means:
                            ¤
                     (WC) 𝑅;𝑊      ¤ ; 𝑆¤
                                ≤ 𝑅;𝑊                               (witness ∀∀ correct)
                            ¤
                     (WO) 𝑅; h𝑐] ≤ 𝑊 ; [havi                        (witness overapproximates 𝑐)
                            ¤
                     (WU) 𝑅;𝑊   ≤ hhav | 𝑑i                         (witness underapproximates 𝑑)
                                        ∃
                                                                       ¤ h𝑐] (𝜏, 𝜎 ′). By (WO) there is
   Proof. To prove 𝑐 | 𝑑 : 𝑅 ≈> 𝑆, suppose 𝜎𝑅𝜎 ′ and 𝜎𝑐𝜏. Thus (𝜎, 𝜎 ′)𝑅;
𝜏 ′ with (𝜎, 𝜎 ′)𝑊 (𝜏, 𝜏 ′) [havi(𝜏, 𝜎 ′ ). Then by (WU) we have 𝜎 ′𝑑𝜏 ′ and by (WC) we have 𝜏𝑆𝜏 ′.  

  The theorem is not simply a reduction to ∀∀-logic; it relies essentially on the use of inequalities
(WO) and (WU) that are not ∀∀ conditions of the form (5). It is no suprise that reasoning about
the existential in a ∀∃ property involves ﬁnding a witness—that is familiar in many settings. Here
a witness comprises an alignment of the programs, with embedded bitests that serve to select the
witnessing executions —and all the correctness conditions are expressed equationally!
  Theorem 7.2 (backward witness soundness). In a relational BiKAT over a KAT with top, we
               ∃
have 𝑐 | 𝑑 : 𝑅 ≈> 𝑆 if there is alignment witness 𝑊 that is b-valid, meaning:
                     (WCb) 𝑊 ; 𝑆¤ ≤ 𝑅;𝑊¤ ; 𝑆¤      (witness reverse ∀∀ correct)
                                     ¤
                     (WOb) h𝑐]; 𝑆 ≤ [havi;𝑊 (witness overapproximates 𝑐)
                     (WUb) 𝑊 ; 𝑆¤ ≤ hhav | 𝑑i      (witness underapproximates 𝑑)
                                        ∃
  Proof. To prove 𝑐 | 𝑑 : 𝑅 ≈> 𝑆, suppose 𝜎𝑐𝜏 and 𝜏𝑆𝜏 ′. By (WOb) there is 𝜎 ′ with (𝜎, 𝜎 ′ )𝑊 (𝜏, 𝜏 ′ ).
By (WUb) we have 𝜎 ′𝑑𝜏 ′. By (WCb) we have 𝜎𝑅𝜎 ′.                                                    
   Theorem 7.3 (witness completeness). In a relational BiKAT over a KAT with top, a forward
(resp. backward) simulation judgment holds if and only if it has an f-valid (resp. b-valid) alignment
witness.8
                                                                                                           ∃
    Proof. To prove completeness for forward simulation, suppose 𝑐 |𝑑 : 𝑅 ≈> 𝑆 holds. Let witness
𝑊 be 𝑅; ¤ h𝑐 | 𝑑i; 𝑆.
                    ¤ We show 𝑊 is f-valid. We have 𝑅;𝑊      ¤       ¤ ; 𝑆¤ because 𝑅;𝑊
                                                                   ≤ 𝑅;𝑊                ¤       ¤ 𝑅;
                                                                                             = 𝑅; ¤ h𝑐 | 𝑑i; 𝑆¤ =
 ¤ 𝑅;
𝑅;  ¤ h𝑐 | 𝑑i; 𝑆;
               ¤ 𝑆¤ by deﬁnition of 𝑊 and idempotence of tests. To show 𝑅;         ¤ h𝑐] ≤ 𝑊 ; [havi, consider
any 𝜎, 𝜎 ′, 𝜏, 𝜏 ′. By deﬁnitions, (𝜎, 𝜎 ′)𝑅;¤ h𝑐] (𝜏, 𝜏 ′) is equivalent to 𝜎𝑅𝜎 ′ ∧ 𝜎𝑐𝜏 ∧ 𝜏 ′ = 𝜎 ′. So by
          ∃
𝑐 |𝑑 : 𝑅 ≈> 𝑆 there is 𝜏 ′′ with 𝜎 ′𝑑𝜏 ′′ and 𝜏𝑆𝜏 ′′, whence by deﬁnition of 𝑊 we have (𝜎, 𝜎 ′)𝑊 (𝜏, 𝜏 ′′ ).
Thus (𝜎, 𝜎 ′)𝑊 ; [havi(𝜏, 𝜏 ′) by deﬁnitions. To show 𝑅;𝑊      ¤     ≤ hhav | 𝑑i, consider any 𝜎, 𝜎 ′, 𝜏, 𝜏 ′. By
                     ′ ¤
deﬁnitions, (𝜎, 𝜎 )𝑅;𝑊 (𝜏, 𝜏 ) iﬀ 𝜎𝑅𝜎 ∧𝜎𝑐𝜏∧𝜎 𝑑𝜏 ∧𝜏𝑆𝜏 . So (𝜎, 𝜎 ′ )hhav] (𝜏, 𝜎 ′ ) and (𝜏, 𝜎 ′ ) [𝑑i(𝜏, 𝜏 ′),
                               ′           ′         ′    ′      ′

hence (𝜎, 𝜎 ′ )hhav]; [𝑑i(𝜏, 𝜏 ′), i.e., (𝜎, 𝜎 ′)hhav | 𝑑i(𝜏, 𝜏 ′).
    The proof for backward simulation is similar, again using 𝑅;       ¤ h𝑐 | 𝑑i; 𝑆¤ as witness.                
                                                                              ∃                       ∃
   For clarity we deﬁned the judgment forms 𝑐 | 𝑑 : 𝑅 ≈> 𝑆 and 𝑐 | 𝑑 : 𝑅 ≈> 𝑆 for relational models,
but it is straightforward to interpret them in trace models. Essentially the horizontal arrows in
(8) and (9) are interpreted as sequences of zero or more steps. Then the soundness Theorems 7.1
8 In the published version of this paper, the theorem requires the model to be full, and the proof only shows that witnesses

exist in the model, without showing that they are expressible as BiKAT terms. (Note that the theorem implicitly assumes
the pre/post relations are expressible as bitests.) For the record here is the original proof of completeness for forward
simulation; it constructs witness elements that are in some sense minimal.
                          ∃
  Suppose 𝑐 |𝑑 : 𝑅 ≈> 𝑆 holds. Using suggestive identiﬁers for bound variables, deﬁne the predicate P (𝜎, 𝜎 ′, 𝜏) =                 ˆ
𝜎𝑅𝜎 ′ ∧ 𝜎𝑐𝜏 and the set X (𝜎, 𝜎 ′ , 𝜏) =
                                       ˆ {𝜏 ′ | 𝜎 ′𝑑𝜏 ′ ∧𝜏𝑆𝜏 ′ }. For any (𝜎, 𝜎 ′, 𝜏) that satisfy P we have X (𝜎, 𝜎 ′, 𝜏) ≠ ∅, owing
                ∃
to 𝑐 | 𝑑 : 𝑅 ≈> 𝑆. So deﬁne Y (𝜎, 𝜎 ′ , 𝜏) to be a chosen element of X (𝜎, 𝜎 ′ , 𝜏) if P (𝜎, 𝜎 ′, 𝜏), and undeﬁned otherwise.
Deﬁne 𝑊 =   ˆ { ( (𝜎, 𝜎 ′ ), (𝜏, 𝜏 ′ )) | P (𝜎, 𝜎 ′ , 𝜏) ∧ 𝜏 ′ = Y (𝜎, 𝜎 ′, 𝜏) }. By fullness, 𝑊 is in the BiKAT. We have (WC) because
𝑊 = 𝑅;𝑊 ¤     ¤ We have (WU) using the deﬁnition of 𝑊 . We have (WO) also by deﬁnitions: If (𝜎, 𝜎 ′ ) 𝑅;
            ; 𝑆.                                                                                                       ¤ h𝑐 ] (𝜏, 𝜎 ′ ) then
         ′            ′               ′                    ′        ′             ′
P (𝜎, 𝜎 , 𝜏) so let 𝜏 = Y (𝜎, 𝜎 , 𝜏); we get (𝜎, 𝜎 )𝑊 (𝜏, 𝜏 ) so (𝜎, 𝜎 )𝑊 ; [havi (𝜏, 𝜎 ).         ′



                                      Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:18   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


and 7.2 extend to trace models and we get a witness completeness theorem for full trace models,
by an argument like our proof of Theorem 7.3.
  Theorem 7.3 is about existence of a witness that satisﬁes the witness conditions in a model. Next
we consider ﬁnding witnesses for which the conditions can be proved equationally.

7.3 Examples Proving ∀∃ with Witnesses
Example 2.4 in Sect. 2 considers the programs 𝐸 1 : x:=any; y:=x and 𝐸 2 : t:=any; z:=t+1. To establish
                  ∃
𝐸 1 | 𝐸 2 : true ≈> y =¥ z we choose witness 𝑊 =ˆ hx:=any | t:=anyi; [x-1 =¥ t]; hy:=x | z:=t+1i. The bitest
[x-1 =¥ t] winnows execution pairs so choices made by 𝐸 2 match favorably the nondeterministic
assignment made by 𝐸 1 . Condition (WO) ensures that all executions of 𝐸 1 are still covered. The
three conditions are proved using axioms to express semantics of the primitives, e.g., the bitest
[x-1 =¥ t] commutes with hy:=x]. We also use a condition which expresses the left-totality of the
bitest [x-1 =¥ t] as discussed later in connection with rule enAss.
  Example 7.4 (∀∃ path alignment). When considering ∀∃ properties, sometimes the choices made
by the witness determine which paths are taken in the program, rather than merely values taken
for variables. Consider this example adapted from Beutner and Finkbeiner [2022].
a1 := any ; a2 := any ; if ( h > l ) o := l + a1 ;               // 𝑘1
                        else { x := a2 ; if ( x > l ) o := x ;   // 𝑘2
                                          else        o := l ; } // 𝑘3
                                                                                                  ∃
Here we are interested in the possibilistic non-interference property 𝐶 | 𝐶 : [l =¥ l] ≈> [o =¥ o]. This
example has multiple cases to consider depending on (i) how the inputs to an execution impact
the conditional and (ii) how those choices may diﬀer from one execution to another. Consequently,
for any path taken in the left program, our choices for the anys in the second may involve taking
diﬀerent paths than were taken in the ﬁrst program. The following is the KAT representation of
the three paths and the whole program (𝑘 = 𝑘 1 + 𝑘 2 + 𝑘 3 ):
                           𝑘1    ˆ
                                 =   a1:=any; a2:=any; [h>l]; o:=l+a1
                           𝑘2    ˆ
                                 =   a1:=any; a2:=any; [h<=l]; x:=a2; [x>l]; o:=x
                           𝑘3    ˆ
                                 =   a1:=any; a2:=any; [h<=l]; x:=a2; [x<=l]; o:=l

We will refer to the right program as 𝑘 ′ , having primed variables. We use the following witness
  𝑊      ˆ
         =   ha1:=any; a2:=any; | a1’:=any; a2’:=any;i;
             ( [h>l; h’>l’; a1’=a1]                               + [h>l; h’<=l’; a2’>l’; a2’=l+a1]
              + [h<=l; h’>l’; a2>l; a1’=a2-l’]                    + [h<=l; h’>l’; a2<=l; a1’=0]
              + [h<=l; h’<=l’; a2>l; a2’>l’; a2’=a2]              + [h<=l; h’<=l’; a2<=l; a2’<=l’]) ; h𝑐 | 𝑐 ′ i
where 𝑐 and 𝑐 ′ are the remainders of 𝑘 and 𝑘 ′ , respectively, after the nondeterministic choices. (So
𝑐 ≡ ([h>l]; o:=l+a1 + [h<=l]; x:=a2; ([x>l]; o:=x + [x<=l]; o:=l;)) .) The witness 𝑊 comprises six
cases covering all preconditions of the input l, h and l’, h’ of the two programs. The witness can
be rewritten into 𝑊 = 𝑊1 +𝑊2 + . . . +𝑊6 where each 𝑊𝑖 corresponds to a case in 𝑊 . For example,
the witness 𝑊2 corresponding to the precondition h > l ∧ h’ ≤ l’ can be simpliﬁed into
        𝑊2    ˆ
              =    ha1:=any; a2:=any; | a1’:=any; a2’:=any;i;
                   [h>l; h’<=l’; a2’>l’; a2’=l+a1]; h𝑐 | 𝑐 ′ i
              =    ha1:=any; a2:=any; | a1’:=any; a2’:=any;i;
                   [h>l; h’<=l’; a2’>l’; a2’=l+a1];
                   h[h>l]; o:=l+a1 | [h’<=l’]; x’:=a2’; ([x’>l’]; o’:=x’ + [x’<=l’]; o’:=l’;)i
              =    ha1:=any; a2:=any; | a1’:=any; a2’:=any;i;
                   [h>l; h’<=l’; a2’>l’; a2’=l+a1]; ho:=l+a1 | x’:=a2’; o’:=x’i (distrib, cancel)

Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                           20:19


In the above𝑊2 , infeasible paths in the left and right program under the precondition h > l∧h’ ≤ l’
and the chooser a2’ > l’ have been pruned out. Under this precondition, path 𝑘 1 in the left program
can be aligned with path 𝑘 2′ and path 𝑘 3′ in the right program. However, the alignment between
the left 𝑘 1 and the right 𝑘 3′ is invalid w.r.t the ∀∃ property because it requires that the left a1 must
be always 0, which is infeasible since under the ∀ quantiﬁer, we have to consider every execution
of the left program. The condition a2’ > l’ in 𝑊2 then chooses the right 𝑘 2′ to align with the left
𝑘 1 and the condition a2’ = l + a1 shows that there exists an execution under that alignment to
achieve agreement on o. With that intuition, the (WC) condition for the witness 𝑊2 , and all the
conditions of Theorem 7.1 for the witness terms, are straightforward to prove.

  Example 7.5 (Backward simulation). Consider the following, where x, t, s, and z range over the
natural numbers:
                        𝐶 1 : while x>n do x:=x-1 od; t:=any+x; z:=x+t
                        𝐶 2 : s:=any; while x>n do x:=x-1 od; z:=x+s
                                                                                                                 ∃
We want to show their possibilistic equivalence, which could be expressed as 𝐶 1 | 𝐶 2 : 𝑅 ≈> 𝑆,
where 𝑅 = ˆ x =¥ x ∧ n =¥ n and 𝑆 =
                                  ˆ z =¥ z. To prove this it would be convenient to align the two loops,
to enable use of simple relational invariants x =¥ x etc. But then the nondeterministic assignment
to t is aligned far after the assignment to s that needs to match it. There are two well known
ways to deal with such situations: introduce a prophecy variable [Abadi and Lamport 1988] or
(equivalently an auxiliary variable [Morgan 1988]) use backward simulation. We can prove the
                          ∃
following:9 𝐶 1 | 𝐶 2 : 𝑅 ≈> 𝑇 , where 𝑇 =ˆ x =¥ x ∧ n =¥ n ∧ z =¥ z ∧ t =¥ s. To prove this using the witness
technique of Theorem 7.2, we choose the witness to be:

                       ˆ [s:=anyi; h𝑋 | 𝑋 i ∗ ; h¬[x>n]]; ht:=any+x]; hz:=x+t | z:=x+si;𝑇
                     𝑊 =

where 𝑋 =ˆ [x>n]; x:=x-1 . Notice that 𝑊 ends with the postrelation 𝑇 and we do not need to intro-
duce additional bitests. The three conditions the witness must satisfy are easily proved. As usual
we rely on axioms for the semantics of primitives. Interestingly, these include ones about backward
preservation of bitests, e.g., h𝑋 | 𝑋 i; [x =¥ x] = [x =¥ x]; h𝑋 | 𝑋 i; [x =¥ x].

   Example 7.6 (Forward simulation and prophecy). As a variation on Example 7.5 we can prove
               ∃
𝐶 3 | 𝐶 2 : 𝑅 ≈> 𝑆 for a modiﬁed version of 𝐶 1 that uses variable p to “prophesize” the value for t.

                             𝐶3 :   p:=any; while x>n do x:=x-1 od; t:=p+x; z:=x+t

                         ∃
To show 𝐶 3 | 𝐶 2 : 𝑅 ≈> 𝑆 using the witness technique in Theorem 7.1, choose witness 𝑊 to be:

                     ˆ hp:=any | s:=anyi; 𝐵; h𝑋 | 𝑋 i ∗ ; h¬[x>n]]; ht:=p+x; z:=x+t | z:=x+si
                   𝑊 =

where 𝑋 =                         ˆ [p+min(x,n) =¥ 𝑠]. As in the previous forward simulation exam-
            ˆ [x>n]; x:=x-1 and 𝐵 =
ples, the witness aligns the two nondeterministic assignments together, the loops in lockstep, and
introduces a bitest 𝐵 that ﬁlters executions of 𝐶 2 to only those that ensure agreement on z upon
termination. The three witness conditions for 𝑊 are straightforward to check.
    In the next section we introduce deductive rules for forward simulation. With these, the judg-
ment about 𝐶 3 and 𝐶 2 is proved in a way that implicitly follows the alignment 𝑊 . The chooser
bitest 𝐵 is introduced as a postcondition, by a rule for aligned nondeterministic assignments, and
it is manipulated in intermediate assertions rather than being inlined like it is in 𝑊 . (See Appen-
dix 9.6.2.)

                                Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:20   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


                                                                              ∃                                 ∃
                            𝑃 ⇒ ([𝑒 ′ i ⇒ h𝑒])      𝑐 | 𝑐 ′ : 𝑃 ∧ h𝑒] ∧ [𝑒 ′ i ≈> 𝑃        𝑐 | skip : 𝑃 ∧ h𝑒] ≈> 𝑃
                  eWhL                                                        ∃
                                       while 𝑒 do 𝑐 | while 𝑒 ′ do 𝑐 ′ : 𝑃 ≈> 𝑃 ∧ ¬h𝑒] ∧ ¬[𝑒 ′ i

eHav                                 enAss                                                eDisj
                                                                                                   ∃                 ∃
             ¤ [havi
 1¥ ≤ [havi; 𝑅;                                         ¤ [𝑦 := anyi
                                       1¥ ≤ [𝑦 := anyi; 𝑅;                                𝑐 | 𝑑 : 𝑃 ≈> 𝑄    𝑐 | 𝑑 : 𝑅 ≈> 𝑄
                        ∃                                             ∃                                     ∃
hhav | havi : 𝑡𝑟𝑢𝑒 ≈> 𝑅              h𝑥 := any | 𝑦 := anyi : 𝑡𝑟𝑢𝑒 ≈> 𝑅                        𝑐 | 𝑑 : 𝑃 ∨ 𝑅 ≈> 𝑄
Fig. 2. Selected rules for ∀∃ forward simulation correctness. Please note: there are also rules eConseq, eSeq,
                                                                                      ∃
eIf, eWh, which look the same as rConseq, dSeq, dIf, dWh but using − ≈> −.


7.4     Logics of Forward and Backward Simulation
7.4.1 Forward Simulation Logic. Theorem 7.1 gives a way to prove forward simulation judgments,
by direct reasoning in a BiKAT. There are also inference rules for forward simulation. In fact several
of the inference rules for ∀∀ judgments (Fig. 1) are also sound for forward simulation. Fig. 2 gives
                       ∃
some rules for the − ≈> − judgment.
                                                          ∃
   Consider eWh, which is simply dWh but for the − ≈> − judgment. Informally, eWh is sound
because any terminating execution of the left program can be matched by one that terminates on
the right, owing to the side condition that says the loop tests agree. Rule eWhL has a similarly
simple side condition that suﬃces to ensure relative termination: in terms of alignment, if the
right loop can continue to iterate then so can the left, and their joint iterations can be aligned in
lockstep. An additional premise handles the situation where the left loop has more iterations than
the right.
   One can consider two other situations. One is where the iterations can be aligned in lockstep,
but the right loop may need more iterations. Consider this rule:
                                             𝑃 ⇒ (¬h𝑒] ∨ [𝑒 ′ i) ∧ [𝑓 ≥ 0i
                                                   ∃                                              ∃
                   skip | 𝑐 ′ : 𝑃 ∧ [𝑒 ′ ∧ 𝑓 = 𝑛i ≈> 𝑃 ∧ [𝑓 < 𝑛i      𝑐 | 𝑐 ′ : 𝑃 ∧ h𝑒] ∧ [𝑒 ′ i ≈> 𝑃
           eWhR                                                           ∃
                                while 𝑒 do 𝑐 | while 𝑒 ′ do 𝑐 ′ : 𝑃 ≈> 𝑃 ∧ ¬h𝑒] ∧ ¬[𝑒 ′ i
It uses a variant expression 𝑓 to establish termination on the right side (like in total correctness
                                                                                   ∃
Hoare logic). A related but diﬀerent idea is the general rule to infer 𝑐 |𝑐 ′ : 𝑃 ≈> 𝑅 from 𝑐 | 𝑐 ′ : 𝑃 ≈> 𝑅
                                 ′
together with termination of 𝑐 from states in the codomain of 𝑃. But KAT does not support direct
expression of termination, and we refrain from formulating the requisite notations for a BiKAT
encoding of these rules.
   The other situation for loops is where lockstep alignment is not suﬃcient. We conjecture that a
rule similar to rule caWh can be devised, but that is beyond the scope of this paper.
   To relate two nondeterministic assignments, this axiom is sound in relational and trace models:
                          𝑥−.∃⇀
                              −𝑦 .𝑅) ≈>
                                      ∃
h𝑥 := any | 𝑦 := anyi : (∀↼             𝑅. It uses suggestive informal notation for quantiﬁcation over
the left and right states. The precondition ensures that for any value assigned to 𝑥 there is some
value for 𝑦 such that 𝑅 holds. But in this paper we refrain from formalizing formulas for relations.
                                                                                          ∃
Instead we consider a rule for judgments of the form h𝑥 := any | 𝑦 := anyi : 𝑡𝑟𝑢𝑒 ≈> 𝑅. This holds
provided that, in any pair of states, for every value of 𝑥 there is some value for 𝑦 making 𝑅 true. As
a step towards an algebraic formulation for that condition, ﬁrst consider the fully nondeterministic
action hav.
9 A stronger postcondition is needed for this backwards property, for similar reasons to what happens in incorrectness

logic [O’Hearn 2019].


Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                              20:21

                               ∃
   For hhav | havi : 𝑡𝑟𝑢𝑒 ≈> 𝑅¤ to hold, 𝑅 must be a domain-total relation. In terms of relations this
can be expressed by the equation 𝑅; hav = hav but we prefer to express the condition in terms of
the bitest 𝑅¤ for 𝑅. The condition in rule eHav (Fig. 2), i.e., BiKAT equation 1¥ ≤ [havi; 𝑅; ¤ [havi,
holds (in a relational model) just if the relation 𝑅 is domain-total.
                                                                                                   ∃
   For two nondeterministic assignments to satisfy the judgment h𝑥 := any | 𝑦 := anyi : 𝑡𝑟𝑢𝑒 ≈> 𝑅,
the condition that we wrote as ∀↼     𝑥−. ∃⇀
                                           −𝑦 . 𝑅 should be valid. This is equivalent to the condition
                  ¤ [𝑦 := anyi of rule enAss. An informal reading is that for any pair of states, there
¥1 ≤ [𝑦 := anyi; 𝑅;
is some value for 𝑦 on the right that makes 𝑅 hold. (The trailing assignment to 𝑦 can restore the
initial value of 𝑦.)
  Lemma 7.7. In any BiKAT, and for any rule in Fig. 2, given an f-valid witnesses for the premises,
there is an f-valid witness for the conclusion.
   Theorem 7.8. The rules in Fig. 2 are sound in any relational BiKAT over a KAT with top.
  Proof. For each rule, if its premises are true then by Theorem 7.3 there are f-valid witnesses for
the premises. So by Lemma 7.7 we obtain an f-valid witness for the conclusion, so by Theorem 7.1
the conclusion is true.                                                                           
   We consider illustrative cases in the proof of Lemma 7.7.
  Proof of eHav. The rule has no premise judgment, only the antecedent 1¥ ≤ [havi; 𝑅;  ¤ [havi. To
prove the conclusion we take witness 𝑊 to be hhav | havi; 𝑅.  ¤ Using the BiKAT notation 1¥ for the
pre-relation 𝑡𝑟𝑢𝑒, the f-validity conditions are:
 (WC) 1¥ ; hhav | havi; 𝑅¤ ≤ 1¥ ; hhav | havi; 𝑅;
                                               ¤ 𝑅¤
 (WU) 1;  ¥ hhav | havi; 𝑅¤ ≤ hhav | havi
 (WO) 1;  ¥ hhav] ≤ hhav | havi; 𝑅; ¤ [havi
We have (WC) by idempotence of the test 𝑅,  ¤ and (WU) using 𝑅¤ ≤ 1.
                                                                  ¥ The condition (WO), expressing
                                                        ¤ 1;
existence, is proved using the antecedent condition for 𝑅. ¥ hhav] = 1;
                                                                     ¥ hhav]; 1¥ ≤ 1;               ¤ [havi =
                                                                                   ¥ hhav]; [havi; 𝑅;
              ¤ [havi. For rule enAss the proof is similar.
hhav | havi; 𝑅;
                                                            ∃                                                   ∃
  Proof of eSeq. Suppose for premise 𝑐 | 𝑐 ′ : 𝑃 ≈> 𝑅 we have witness 𝑍 and for 𝑑 | 𝑑 ′ : 𝑅 ≈> 𝑄 we
have witness 𝑊 , so the conditions are
   (WCZ) 𝑃;   ¤ 𝑍 ≤ 𝑃;
                     ¤ 𝑍 ; 𝑅¤    (WCW) 𝑅;𝑊   ¤       ¤ ; 𝑄¤
                                                   ≤ 𝑅;𝑊
              ¤                              ¤
   (WUZ) 𝑃; 𝑍 ≤ hhav | 𝑐 i (WUW) 𝑅;𝑊 ≤ hhav | 𝑑 ′i
                              ′

   (WOZ) 𝑃;   ¤ h𝑐] ≤ 𝑍 ; [havi (WOW) 𝑅;     ¤ h𝑑] ≤ 𝑊 ; [havi
                               ∃
To prove 𝑐; 𝑑 | 𝑐 ′ ; 𝑑 ′ : 𝑃 ≈> 𝑄 we use 𝑍 ;𝑊 as witness.
• (WC) To show 𝑃¤ ; 𝑍 ;𝑊 ≤ 𝑃;    ¤ 𝑍 ;𝑊 ; 𝑄¤ we have 𝑃;
                                                     ¤ 𝑍 ;𝑊 ≤ 𝑃;
                                                              ¤ 𝑍 ; 𝑅;𝑊
                                                                    ¤     ¤ 𝑍 ; 𝑅;𝑊
                                                                        ≤ 𝑃;    ¤ ; 𝑄¤ ≤ 𝑃;
                                                                                         ¤ 𝑍 ;𝑊 ; 𝑄¤
using (WCZ), (WCW), and 𝑅 ≤ 1.   ¤   ¥

                ¤ 𝑍 ;𝑊 ≤ 𝑃;
• (WU) We have 𝑃;           ¤ 𝑍 ; 𝑅;𝑊
                                  ¤   ≤ hhav | 𝑐 ′ i; hhav | 𝑑 ′i = hhav | 𝑐 ′ ; 𝑑 ′i using (WCZ), (WUZ),
(WUW), embedding homomorphic, and idempotence of hav.
• (WO)      ¤ h𝑐; 𝑑]
           𝑃;
            ¤
        = 𝑃; h𝑐]; h𝑑]                emb homo
        ≤ 𝑃;¤ 𝑍 ; [havi; h𝑑]         (WOZ)
        = 𝑃;¤ 𝑍 ; h𝑑]; [havi         (LRC)
        = 𝑃;¤ 𝑍 ; 𝑅;
                  ¤ h𝑑]; [havi       (WCZ)
            ¤
        ≤ 𝑃; 𝑍 ;𝑊 ; [havi; [havi (WOW)
        = 𝑃;¤ 𝑍 ;𝑊 ; [havi           hav idem, emb homo
        ≤ 𝑍 ;𝑊 ; [havi               𝑃 ≤ 1¥

                                   Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:22   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


                                                            ∃                                           ∃
                             𝑐 | 𝑐 ′ : 𝑃 ∧ h𝑒] ∧ [𝑒 ′ i ≈> 𝑄            𝑑 | 𝑑 ′ : 𝑃 ∧ ¬h𝑒] ∧ ¬[𝑒 ′i ≈> 𝑄
                       bIf                                                                     ∃
                                     if 𝑒 then 𝑐 else 𝑑 | if 𝑒 ′ then 𝑐 ′ else 𝑑 ′ : 𝑃 ≈> 𝑄

                                                    ∃                                                    ∃                             ∃
                      𝑐 | 𝑐 ′ : 𝑃 ∧ h𝑒] ∧ [𝑒 ′ i ≈> 𝑃                                         𝑐 | 𝑐 ′ : 𝑃 ≈> 𝑅               𝑑 | 𝑑 ′ : 𝑅 ≈> 𝑄
 bWh                                           ∃
                                                                                       bSeq                                     ∃
        while 𝑒 do 𝑐 | while 𝑒 ′ do 𝑐 ′ : 𝑃 ≈> 𝑃 ∧ ¬h𝑒] ∧ ¬[𝑒 ′ i                                    𝑐; 𝑑 | 𝑐 ′ ; 𝑑 ′ : 𝑃 ≈> 𝑄

                                                                                                                         ∃
                            ¤ [𝑦 := anyi
           1¥ ≤ [𝑦 := anyi; 𝑅;                                                             𝑅⇒𝑃          𝑐 | 𝑑 : 𝑅 ≈> 𝑆               𝑄 ⇒𝑆
 bnAss                                ∃
                                                                           bConseq                                   ∃
         h𝑥 := any | 𝑦 := anyi : 𝑅 ≈> 𝑡𝑟𝑢𝑒                                                           𝑐 | 𝑑 : 𝑃 ≈> 𝑄

                                                                ∃                      ∃
                                                    𝑐 | 𝑑 : 𝑃 ≈> 𝑄         𝑐 | 𝑑 : 𝑃 ≈> 𝑅
                                          bDisj                     ∃
                                                            𝑐 | 𝑑 : 𝑃 ≈> 𝑄 ∨ 𝑅

                          Fig. 3. Selected rules for ∀∃ backward simulation correctness.


7.4.2 Backward Simulation Logic. The backward simulation judgment has a number of inference
rules, with some interesting diﬀerences from the ∀∀ and forward simulation rules. The rules are
derivable in BiKAT.
   Hoare’s assignment axiom based on weakest precondition, using substitution in the precondi-
tion, is often called “backwards”. The relational generalization works for ∀∀ and forward simula-
tion:
                   dAss                                                         eAss
                                            𝑣 |𝑣′                                                            ′       ∃
                   𝑣 := 𝑒 | 𝑣 ′ := 𝑒 ′ : 𝑃𝑒 |𝑒 ′ ≈> 𝑃                           𝑣 := 𝑒 | 𝑣 ′ := 𝑒 ′ : 𝑃𝑒𝑣|𝑒|𝑣′ ≈> 𝑃

Variables and substitution are not part of KAT/BiKAT but the rules are sound in models. But a
judgment of this form is unsound for backward simulation, for the same reason as in incorrectness
logic [O’Hearn 2019]: with an arbitrary postcondition, there can be ﬁnal states that are not in the
image of the assignment. The unary Floyd [1967] axiom for assignment is 𝑣 := 𝑒 : 𝑞 ❀ ∃𝑢.𝑞𝑢𝑣 ∧𝑣 =
𝑒𝑢𝑣 which suggests the following:
                                                        ∃       |𝑣          ′                                    ′
                       𝑣 := 𝑒 | 𝑣 ′ := 𝑒 ′ : 𝑃 ≈> ∃𝑢, 𝑢 ′ . 𝑃𝑢𝑣 |𝑢           𝑣       ′   ′𝑣
                                                                   ′ ∧ h𝑣 = 𝑒𝑢 ] ∧ [𝑣 = 𝑒 𝑢 ′ i


Consider 𝜏, 𝜏 ′ that satisfy the postcondition and let 𝜎 be the left initial state. Let 𝑢,
                                                                                        ˆ 𝑢ˆ′ be values that
                                                                                      ′
witness the existential and observe that 𝜏 is 𝜎 with 𝑣 updated to 𝑢.      ˆ Choose 𝜎 be a state such that
𝜏 ′ is 𝜎 ′ with 𝑣 updated to 𝑢ˆ′ . Conclude 𝜎, 𝜎 ′ satisfy the precondition, and further, that executing
𝑣 ′ := 𝑒 ′ in 𝜎 ′ yields 𝜏 ′ ; hence the judgment holds.
    Unlike the simple law that can be used to express semantics of assignments in a proof of eAss
for forward simulation, a BiKAT formulation of the Floyd rule would need a more complicated
way to reason about assignment and postcondition formula. It can be done by choosing some type,
say integers, for data, and then treating the existential as an integer-indexed sum of tests, but we
leave this to the reader.
    Another resemblance to incorrectness logic is that the consequence rule is reversed from the
                                                                                      ∃
one for forward simulation and ∀∀. Suppose 𝑊 is a witness for 𝑐 | 𝑑 : 𝑃 ≈> 𝑄, and moreover
                                                              ∃
𝑃 ⇒ 𝑅 and 𝑆 ⇒ 𝑄. Then 𝑊 is also a witness for 𝑐 |𝑑 : 𝑅 ≈> 𝑆 To show (WCb) for the latter, we have
𝑊 ; 𝑆¤ ≤ 𝑊 ; 𝑄¤ ≤ 𝑃;𝑊¤ ; 𝑄¤ ≤ 𝑅;𝑊  ¤ ; 𝑄¤ (using (WCd) for 𝑊 , i.e., 𝑊 ; 𝑄 ≤ 𝑃;𝑊 ; 𝑄). And 𝑊 ; 𝑆¤ ≤ 𝑅;𝑊
                                                                                                     ¤ ; 𝑄¤
iﬀ 𝑊 ; 𝑆¤ ≤ 𝑅;𝑊
              ¤ ; 𝑆¤ using 𝑆 ⇒ 𝑄.

Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                           20:23


   The rule for sequence looks just like dSeq (and eSeq), and is proved by a calculation similar to
the one proving eSeq. For conditional and loop, the pattern of rules dIf and dWh (also eIf and
eWh) can be retained but the side conditions are not needed! The conclusion of rule bWh in Fig. 3
says that given ﬁnal states (𝜏, 𝜏 ′ ) related by 𝑃 in which the loop tests are false, and a terminating
execution from some initial 𝜎 with (𝜎, 𝜎 ′ ) related by 𝑃, there is an execution from 𝜎 ′ ending in 𝜏 ′ .
Informally, the conclusion follows because we can repeatedly invoke the premise, starting from
the last iteration, to obtain the requisite right execution. If 𝜎𝑖 is the state reached after the 𝑖th
iteration on the left, and 𝜏𝑖 the corresponding right state given by our induction hypothesis, and
there is a preceding iteration on the left from 𝜎𝑖−1, the premise yields some 𝜏𝑖−1 with a matching
right iteration, and moreover 𝑒 ′ holds in 𝜏𝑖−1 so the loop does take this iteration.
   Theorem 7.9. The rules in Fig. 3 are sound in any relational BiKAT over a KAT with top.
  The proof uses Theorem 7.3. Thorough investigation of loop rules for backward simulation is
beyond the scope of this paper.

7.5 On ∃∀ and ∃∃ Properties
We have looked at various forms of properties involving 2 executions, with pre/post-conditions
playing a diﬀerent roles. So far we have focused on some ∀∀ properties (Sect. 6), and some ∀∃ ones
(Sects. 7.1–7.4). Many of the relational properties can be expressed in these forms, but the classes
that correspond to the duals of those properties are also interesting. Consider the property

                                       𝑐 ✲
                                𝜎              𝜏                                  𝜏
                                 ❄                                                  ❄
                         ∃ 𝑅❄                     ∀                        ⇒        ❄
                                                                                     𝑆                (10)
                                 ′                         ′    𝑑 ✲ ′               ′
                               𝜎                         𝜎           𝜏            𝜏
that says ∃𝜎, 𝜎 ′, 𝜏 . 𝜎𝑅𝜎 ′ ∧𝜎𝑐𝜏 ∧∀𝜏 ′ (𝜎 ′𝑑𝜏 ′ ⇒ 𝜏𝑆𝜏 ′). This property is the dual of forward simulation
                                                                                             ∃
with a negated postcondition, or in other words (10) is equivalent to ¬(𝑐 | 𝑑 : 𝑅 ≈> ¬𝑆). Using
Theorem 7.3, to prove this property, we can check whether the following holds: for any BiKAT
term 𝑍 at least one of the conditions (WO), (WU) or (WC) fails.
   Although not many properties of the form ∃∀ naturally occur in the literature on relational
veriﬁcation, they are nonetheless important, and not only as duals of the more frequently occurring
∀∃ ones. The reason is that with the former, it suﬃces to ﬁnd one single execution of the left
program that captures the required behavior against as traces of the right one. Checking whether
such an execution or trace exists is often hard, and a proof system of ∃∀ properties will be of value.
   Arguing similarly we can use BiKAT reasoning to explore ∃∃ properties on two executions. A
prime example of such properties is “deﬁnite non-determinism”, or in other words the existence
of an input, and two executions on that input that produce diﬀerent output. Consider
                                   ∃𝜎, 𝜎 ′, 𝜏, 𝜏 ′ . 𝜎𝑅𝜎 ′ ∧ 𝜎𝑐𝜏 ∧ 𝜎 ′𝑑𝜏 ′ ∧ ¬𝜏𝑆𝜏 ′
as a general form of ∃∃ properties. This formulation is the dual of the main 2-safety property
we study in the previous sections (see Equation (5)). Non-determinism can then be expressed by
setting both programs 𝑐 and 𝑑 to be the same, and setting 𝑅 and 𝑆 to be relations expressing
agreement on all variables.

7.6 TriKAT
One might hope that the existential quantiﬁcations of (8) and (9) could be expressed algebraically
using BiKAT projection (Def. 4.2). Unfortunately, projection existentially quantiﬁes both initial and
ﬁnal state of the second execution (see (4)). So projection does not directly capture (8), where the

                                Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:24   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


second execution’s initial state is universally quantiﬁed, nor (9) where its ﬁnal state is universally
quantiﬁed. We sketch a way to use projection that merits further investigation but is not used in
the rest of the paper.
    Possibilistic noninterference can be expressed in HyperLTL, a temporal logic with explicit quan-
tiﬁers that range over the traces of a ﬁxed program [Clarkson et al. 2014]. The formula says that
for all traces 𝜋, 𝜋 ′ with initial states related by 𝑅, there is a trace 𝜋 ′′ with the same initial state as
𝜋 ′ , and 𝑅 relates the ﬁnal states of 𝜋 and 𝜋 ′′ . The reason three traces are needed is that two initial
states are universally quantiﬁed in (8).
                          ∃
    To express 𝑐 | 𝑑 : 𝑅 ≈> 𝑆 we consider three executions, using in place of (8) the following pattern.
                                           𝑐 ✲                           hav ✲
                                   𝜎               𝜏               𝜎′               𝜏
                                    ❄               ❄               ❄                ❄
                        ∀        𝑅
                                    ❄ hav
                                                     𝑖𝑑     ∃       ❄
                                                                     𝑖𝑑
                                                                                     ❄
                                                                                      𝑆
                                    ′
                                                    ❄                ′     𝑑         ′
                                  𝜎             ✲𝜏                 𝜎           ✲𝜏
We deﬁne a notion of TriKAT so these ingredients can be described in the form of the following
diagram. It depicts a relation on state triples represented by the displayed TriKAT term using
notation to be explained.
                                      𝑐 ✲
                              𝜎               𝜏
                               ❄               ❄
                            𝑅                   𝑖𝑑
                               ❄ hav           ❄        represented by TriKAT term
                               ′
                             𝜎            ✲𝜏
                                                               ¤ h𝑐 | hav | 𝑑i; h𝑖𝑑
                                                                                  ¤ 8 𝑆i                (11)
                               ❄               ❄        h𝑅¤ 8 𝑖𝑑i;                     ¤
                           𝑖𝑑                   𝑆
                               ❄      𝑑 ✲ ❄
                               ′               ′
                             𝜎               𝜏
The existential quantiﬁcation will then be expressed by projection, as we proceed to show.
    One can easily generalize BiKAT with a three-argument embedding we will write as h_ | _ | _i.
But we also need BiKAT elements to encode the relations 𝑅, 𝑆, 𝑖𝑑. So we deﬁne a two-argument
embedding h_ 8 _i with the following meaning: if 𝐴, 𝐵 are BiKAT elements, thus denoting pairs of
executions, then h𝐴 8 𝐵i denotes triples of executions, comprising pairs from 𝐴 and 𝐵 that agree
on the middle one. Speciﬁcally, for elements 𝐴 and 𝐵 of a relational BiKAT, deﬁne h𝐴 8 𝐵i to be
this relation on Σ × Σ × Σ.
                     (𝜎, 𝜎 ′, 𝜎 ′′ )h𝐴 8 𝐵i(𝜏, 𝜏 ′, 𝜏 ′′ ) =
                                                           ˆ (𝜎, 𝜎 ′)𝐴(𝜏, 𝜏 ′ ) ∧ (𝜎 ′, 𝜎 ′′ )𝐵(𝜏 ′, 𝜏 ′′ )
For the special case of BiKAT elements embedded from the underlying KAT, deﬁne the abbreviation
                                                        ˆ hh𝑎 | 𝑏i 8 h𝑏 | 𝑐ii
                                            h𝑎 | 𝑏 | 𝑐i =
Observe that (𝜎, 𝜎 ′, 𝜎 ′′ )h𝑎 | 𝑏 | 𝑐i(𝜏, 𝜏 ′, 𝜏 ′′ ) iﬀ 𝜎𝑎𝜏 ∧ 𝜎 ′𝑏𝜏 ′ ∧ 𝜎 ′′𝑐𝜏 ′′ . Now one can check that the
relation on state triples depicted by the diagram in (11) is denoted by the term on the right in (11).
   Among the available projections we need the one that projects the left two of three. This can be
considered as a projection from the “TriKAT” to the left underlying BiKAT. For any relation 𝑋 on
Σ × Σ × Σ, deﬁne the relation w𝑋 on Σ × Σ by
                           (𝜎, 𝜎 ′ )w𝑋 (𝜏, 𝜏 ′)      iﬀ    ∃𝜎 ′′, 𝜏 ′′ . (𝜎, 𝜎 ′, 𝜎 ′′ )𝑋 (𝜏, 𝜏 ′, 𝜏 ′′ )
                                                            ∃
   Lemma 7.10. In a relational model, 𝑐 | 𝑑 : 𝑅 ≈> 𝑆, i.e., (8), is equivalent to this BiKAT equation:
                                     ¤ ≤ w(h𝑅¤ 8 𝑖𝑑i;
                       ¤ h𝑐 | havi; 𝑖𝑑
                      𝑅;                            ¤ h𝑐 | hav | 𝑑i; h𝑖𝑑   ¤ 8 𝑆i)
                                                                                ¤                    (12)
               ∃
and 𝑐 | 𝑑 : 𝑅 ≈> 𝑆, i.e., (9) is equivalent to
                            ¤ h𝑐 | havi; 𝑆¤ ≤ w(h𝑖𝑑
                           𝑖𝑑;                    ¤ 8 𝑅i;                     ¤
                                                      ¤ h𝑐 | hav | 𝑑i; h𝑆¤ 8 𝑖𝑑i)                             (13)

Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                           20:25


    The proofs are by unfolding deﬁnitions. The whole story works also for trace models. We hoped
that (12) could be used directly to prove simulations, but were unsuccessful. The reader may check
that in relational or trace models of BiKAT, projection distributes only weakly over sequence, as
ւ(𝐴; 𝐵) ≤ ւ𝐴; ւ𝐵, and w(𝑋 ; 𝑌 ) ≤ w𝑋 ; w𝑌 , which is not helpful for proving equations like
(12). Nonetheless, we can use (12) and (13) to derive some rules including eDisj in Fig. 2.
    The operation h− | − | −i used above does distribute homomorphically over sequence and the
other operators. As a result, BiKAT generalizes straightforwardly to 𝑛-KAT, which encompasses
∀𝑛 properties of program 𝑛-tuples, as in Cartesian Hoare logic [Sousa and Dillig 2016]. However,
it is an open question how to axiomatize projections and the bi-to-tri embedding h− 8 −i in a way
that is useful for ∀∃, so we do not formally deﬁne TriKAT.

8 DISCUSSION
We have described BiKAT, a theory for equational reasoning about alignment for relational pro-
gram veriﬁcation. In this section we consider implications for automated reasoning, connections
with other work including product programs and deductive veriﬁcation, and problems for future
work.

8.1   Automation of Alignment
Recent years have seen advances in automation of relational veriﬁcation, as summarized in Sect. 8.3.
To our knowledge, none of these techniques algebraically derive an alignment. As we developed
the algebraic theory of BiKAT, along the way we found possible approaches for automation such as
integrating with existing automated techniques for discovering alignments or relational invariants.
We save automation for future work, but summarize some general approaches here.
   Solving BiKAT equivalence queries. A BiKAT is itself a KAT and we can, therefore exploit a wide
range of KAT-based tools such as symbolic equality reasoning [Pous 2015], Coq tactics [Braibant and Pous
2010], abstract interpretation with KAT [Antonopoulos et al. 2019], and methods for constructing
and deciding equality in concrete KATs [Greenberg et al. 2022]. Existing KAT tools do not have
a built-in way of representing our particular kinds of KATs. However, we can encode a BiKAT,
minus LRC, as a KAT through suitable variable renaming. We did this manually for a simple, con-
crete BiKAT and conﬁrmed that KMT [Greenberg et al. 2022] was able to verify some equivalence
queries. Of course we interactively use LRC to obtain the desired alignment and do not give KMT
instances of the LRC axiom, owing to undecidability.
   Constraint-based relational veriﬁcation. Unno et al. [2021] reduced 𝑘-safety and possibilisitic
non-interference to a constraint-satisfaction problem. Although these reductions are relatively
complete, the approach does not scale well, as it searches for possible alignments. One possible
path forward is to use BiKAT reasoning to algebraically derive alignments at a coarse-grained
level, and then employ a constraint-satisfaction problem to solve the ﬁne-grained subproblems.
   Semi-automation. Automated solving (e.g. via KAT tools or constraint-satisfaction) could also
be used as part of a larger semi-automated reasoning framework. Our Coq development already
provides the basic BiKAT laws/lemmas and could be extended to include forward/backward sim-
ulation rules, which would then be used interactively on given problem to derive an alignment.
Along the way, automated solvers could be integrated and used to discharge smaller semantic
queries.
   Numerous other works discuss automation of relational veriﬁcation. Pick et al. [2018] describe
a technique that aligns conditional blocks (in addition to loops) and exploits symmetries to reduce
the veriﬁcation burden. Farzan and Vandikas [2019] describe an approach to hypersafety veriﬁca-
tion of unary programs by discovering representative executions of a product program, whose cor-
rectness proofs are suﬃcient to prove the overall property. Unno et al. [2021] work with transition

                                Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:26   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


systems and use a constraint-solving approach to automatically discover a “scheduler”—a form of
alignment described as a function that directs which element of the 𝑘-tuple (product of transition
systems) should take the next step. Badihi et al. [2020] describe ARDiﬀ, using a combination of ab-
straction and reﬁnement for automatically proving program equivalence. Mordvinov and Fedyukovich
[2019] work in the context of CHCs, and infer relational invariants.

8.2     Product Programs and Expressibility
BiKAT serves as notation for alignment products which in turn represent alignments of executions.
We have already shown examples of some alignments in the literature, including the 2𝑥 2 example
of Shemer et al. [2019] (our Example 2.2) and the array insertion example of Shemer et al. (in
Sect. 5). In this section we consider what alignments can be represented in BiKAT, compared with
product programs and other representations in the literature. We also consider how adequacy is
established in various works, compared with our Theorem 4.6.
   In some works, products are literally programs (e.g., [Barthe et al. 2011a, 2004; Eilers et al. 2018]).
In others, products are represented in some form of control-ﬂow automata (e.g., [Churchill et al.
2019]) or transition system (e.g., [Shemer et al. 2019]). In all cases, products represent alignments
between corresponding points in execution pairs (or 𝑘-tuples), for reasoning based on assertions
at the aligned points.
   Representation of products as programs has the advantages (and disadvantages) of syntactic
representation. For products as programs, one approach to ensuring adequacy is developed by
Barthe et al. [2011a, 2016] who develop a ternary judgment that connects two programs to a third
that represents an aligned product of them. Assert commands are used to ensure adequacy. For
example, in the case of if-else, the guard-agreement side condition of rule dIf (in Fig. 1) can be
added to the product program as an initial assertion. If the assertion holds, the product is adequate.
For if 𝑒 then 𝑐 else 𝑑 and if 𝑒 ′ then 𝑐 ′ else 𝑑 ′, one might try to write their product as this BiKAT
         ¥ ′ ; (h𝑒]; h𝑐 | 𝑐 ′ i+¬h𝑒]; h𝑑 | 𝑑 ′ i). However, this treats the initial agreement as an assumption,
term: 𝑒 =𝑒
whereas for adequacy it must be a consequence of the precondition. KAT can be extended with
failures (FailKAT) in order to express assertions [Mamouras 2017].
   The approach of Barthe et al. has the advantage of making a close connection with Hoare logic,
but the disadvantage of lacking means to leverage left-right-commutativity as such. Banerjee et al.
[2022, 2016] handle products using custom syntax for what they call biprograms. The semantics of
their bi-if is essentially like having the guard-agreement assertion. Their bi-command form (𝑐 |𝑐 ′ )
serves as a product with no designated intermediate alignment. Relational judgments apply to
biprograms and a veriﬁcation problem is posed in the form (𝑐 |𝑐 ′ ). There is an auxiliary relation
on biprograms, called weaving, that eﬀectively performs left-right-commutings in a way that pre-
serves adequacy. Whereas Barthe et al. reduce relational veriﬁcation to unary Hoare logic, Banerjee
et al. use a custom proof system for biprograms. In both of these lines of work, adequacy is proved
as a general result about the system. By inspection of our examples and Theorems 6.1 and 6.2, one
can see that BiKAT can represent the alignments achievable in these systems, when they are ad-
equate, but (as noted above) cannot directly encode adequacy checks expressed as assertions. We
conjecture that the systems can be encoded in an extension of BiKAT based on FailKAT [Mamouras
2017]. Such an extension would also serve another purpose, namely to encode the fault-sensitive
variation of ∀∀ used in practical veriﬁcation systems and logics including Banerjee et al. [2022,
2016]; Yang [2007].
   As mentioned earlier, the tiling example is handled in Banerjee et al. [2016] using a custom
rewriting relation with KAT-like rules. The probabilistic relational Hoare logic of Barthe et al.
[2017] has a similar rule, called structural equivalence (as well as a rule for conditionally aligned

Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                            20:27


loops). The logic’s relational correctness judgment connects the related programs to a product
program that witnesses a probabilistic coupling.
   As we discuss in Sect. 5, procedure calls can be treated as primitives in BiKAT, which can
thereby express alignment of calls for use with relational specs as hypotheses. However, BiKAT
has no mean to express patterns of alignments involving nested procedure calls as in the work of
Godlin and Strichman [2008]. Nor does BiKAT provide for directly expressing alignment deﬁned
by code overlay as in the ghost monitors of Clochard et al. [2020]. However, history-sensitive align-
ment can be expressed in BiKAT and other systems using ghost code.
   Many prior works use products based on the representation of programs, and products, as transi-
tion systems. We sketch how BiKAT can express such products quite generally. A transition system
can be presented as rules of the form 𝑔 → 𝑎 where the guard 𝑔 is a state condition, and 𝑎 is an
assignment command (or basic block). So the program can be written in Dijkstra’s guarded com-
mand notation [Apt et al. 2009] as do 𝑔0 → 𝑎 0 8 𝑔1 → 𝑎 1 8 . . . od. Regardless of the form of the
commands 𝑎𝑖 , this has a simple representation in KAT, as (𝑔0 ; 𝑎 0 + 𝑔1 ; 𝑎 1 ...) ∗ ; ¬(Σ𝑖 𝑔𝑖 ). For clarity
in the following discussion we ignore the negated condition and simply write (𝑔0 ; 𝑎 0 + 𝑔1 ; 𝑎 1 ...) ∗ .
So the following BiKAT term represents a product of two transition systems.
                                    h(𝑔0 ; 𝑎 0 + 𝑔1 ; 𝑎 1 ...) ∗ | (𝑔0′ ; 𝑎 0′ + 𝑔1′ ; 𝑎 1′ ...) ∗ i
Alignment products in the literature constrain executions of the underlying programs by some
conditions 𝐿, 𝑅, 𝐽 on state-pairs, that designate whether to take a left-only step, right-only step, or
joint step. (More generally, which of 𝑘 copies, as in Shemer et al. [2019], Eilers et al. [2018].) In a
BiKAT, assuming the conditions 𝐿, 𝑅, 𝐽 are expressible as bitests, the alignment is expressible using
ﬁnite sums as
                 ((Σ𝑔,𝑎,𝑔′,𝑎′ 𝐽 ; h𝑔; 𝑎 | 𝑔 ′ ; 𝑎 ′ i) + (Σ𝑔,𝑎 𝐿; h𝑔; 𝑎 | 1i) + (Σ𝑔′,𝑎′ 𝑅; h1 | 𝑔 ′; 𝑎 ′ i)) ∗     (14)
In these sums, 𝑔, 𝑎 range over the guarded actions 𝑔 → 𝑎 of the left program and 𝑔 ′, 𝑎 ′ range over
the right.
   So much for expressing alignments. What about proving adequacy? One can formulate gen-
eral conditions under which a product is adequate. Roughly, the idea is that 𝐿 ∨ 𝑅 ∨ 𝐽 ∨ 𝑇 𝑅𝑀
must be invariant, where 𝑇 𝑅𝑀 stands for “both sides terminated”. Shemer et al. [2019] give an ad-
equacy result of this form. (Their term is “fairness”. There is no standard term; we take “adequacy”
from Nagasamudram and Naumann [2021].) Churchill et al. [2019] formulate adequacy as veriﬁ-
cation conditions involving their alignment invariants. In our setting, adequacy is proved equa-
tionally (Theorem 4.6), raising the question whether the term (14) can be derived from h(𝑔0 ; 𝑎 0 +
𝑔1 ; 𝑎 1 ...) ∗ | (𝑔0′ ; 𝑎 0′ +𝑔1′ ; 𝑎 1′ ...) ∗ i. Invariance of 𝐿 ∨ 𝑅 ∨ 𝐽 ∨𝑇 𝑅𝑀 is analogous to the side condition of
the proof rule caWh, and the equality of terms h(𝑔0 ; 𝑎 0 + 𝑔1 ; 𝑎 1 ...) ∗ | (𝑔0′ ; 𝑎 0′ + 𝑔1′ ; 𝑎 1′ ...) ∗ i and (14)
is analogous to how the expansion law (7) is used to prove caWh. We conjecture that the general
equality can be proved, in *-continuous BiKATs, just as we have done for (7).
   The 𝐿, 𝑅, 𝐽 form discussed above is very general. In implementations, the conditions 𝐿, 𝑅, 𝐽 tend
to be restricted to constraints supported by an eﬃcient solver, and the same restrictions would be
applicable in uses of BiKAT. Ignoring such restrictions, that general form seems as expressive as
BiKAT. We are not aware of patterns that can be expressed in BiKAT but not by products repre-
sented as transition systems.

8.3    Other Related Work
We have covered many of the most related works; we now mention a few others.
  In recent work D’Osualdo et al. [2022] describe a logic for hyper-triple composition (LHC) based
on weakest preconditions that can decompose a hypersafety proof along the boundary of hyper

                                 Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:28   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


tuples, oﬀering ways of combining multiple 𝑘-safety proofs with diﬀering 𝑘s. In contrast with
BiKAT, LHC is a calculus based on weakest pre-condition rather than an equational system, and
supports only ∀∀ pre/post 𝑘-safety properties. There may be a connection between LHC-style
decomposition and our proposed work on TriKAT discussed in Sect. 7.6. Both permit ways to
combine two relational proofs that share some common program terms into an overall proof by
correlating the common terms. However, we leave this investigation to future work.
   Barthe et al. [2019] discuss relational veriﬁcation in a ﬁrst order predicate logic in which pro-
gram variables are represented as functions 𝑣 (𝑖, 𝑡𝑟 ) over a time step 𝑖 and trace identiﬁed by 𝑡𝑟 .
The authors’ encoding can express highly non-local relationships between traces such as equating
the value of 𝑣 at the beginning of one trace with the value of 𝑣 at the end of another trace. This
approach does not involve deriving an alignment, but rather enables correlating of arbitrary com-
putation steps. The encoding in FO exploits quantiﬁers available in ﬁrst-order provers. Although,
in principle, the traces could be quantiﬁed existentially, the authors only discuss ∀∀ properties
non-interference and sensitivity without mention of quantiﬁer alternation over traces.
   Murray [2020] introduces a relational incorrectness logic for imperative programs, inspired by
incorrectness logic of O’Hearn [2019]. Using relational semantics, the judgment relates 𝑐 to 𝑑 for
spec 𝑅, 𝑆 iﬀ ∀𝜏, 𝜏 ′ .𝜏𝑅𝜏 ′ ⇒ ∃𝜎, 𝜎 ′ .𝜎𝑅𝜎 ′ ∧𝜎𝑐𝜏 ∧𝜎 ′𝑑𝜏 ′. So the postcondition is an underapproximation
of the reachable pairs. In a BiKAT over a KAT with havoc, this can be expressed as hhav | havi; 𝑆¤ ≤
              ¤ h𝑐 | 𝑑i, generalizing O’Hearn’s KAT formulation of incorrectness [O’Hearn 2019,
hhav | havi; 𝑅;
Sect. 5.3]. Zhang et al. [2022] investigated KATs with top for (unary) incorrectness logic.
   Although KAT equations under commutativity hypotheses are undecidable, there are recent
positive results for other classes of hypotheses [Doumane et al. 2019; Pous et al. 2021]. Synchro-
nous KAT [Wagemaker et al. 2019] has models based on strings-of-sets which can be interpreted
as multiple simultaneous actions; this could perhaps be used to model the step-by-step alignments
of Kovács et al. [2013] and Banerjee et al. [2022].
   Apropos ∀∀ properties, Terauchi and Aiken [2005] introduce the term 2-safety and describe
a type system-based alignment used for secure information ﬂow. Their rules (e.g. their Fig. 8)
can be formulated so that the alignments are expressed in BiKAT, leading to a more equational
algebraic derivation strategy of the non-interference property. Sousa and Dillig [2016] describe
Cartesian Hoare Logic for reasoning about 𝑘-safety of individual programs by alignment without
explicit representation of a product program. Eilers et al. [2018] describe a 𝑘-way lock-step product
encoding for single programs, that facilitates the use of 𝑘-safety procedure speciﬁcations.
   Apropos ∀∃ properties, Lamport and Schneider [2021] use TLA+ as a logic for deductive reason-
ing about such properties in the setting of temporal logic. Clochard et al. [2020] manually encode
alignment products as programs in the Why3 deductive veriﬁcation tool, including resolution of
nondeterminacy to prove ∀∃ properties. Barthe et al. [2013] deﬁne left products for proving for-
ward simulation, in a formulation based on control ﬂow graphs. Hawblitzel et al. [2013] use the for-
ward simulation property (calling it relative termination), in translation validation using relational
summaries and veriﬁcation conditions. Example 7.4 was drawn from Beutner and Finkbeiner [2022]
who discuss a more generalized possibilistic non-interference ∀𝑘 ∃𝑙 .
   None of the preceding works provide inference rules for ∀∃ judgments. The Iris-based rela-
tional logic [Frumin et al. 2018; Gäher et al. 2022] does so, in particular a judgment for contextual
reﬁnement, in forward simulation form. The logic has complex features catering for higher or-
der concurrent programs. Prophecy variables have been added [Frumin et al. 2020] so backward
simulation reasoning is available in some form. It is unclear whether the simple forward and back-
ward rules applicable to sequential programs can be extracted from this framework. Maillard et al.
[2020] develop a relational dependent type theory that accounts for core RHL rules encompassing


Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                           20:29


a range of computational eﬀects. It is not clear that the framework facilitates manipulation of in-
tricate data-dependent alignments together with simple ﬁrst-order relational assertions as used in
automated relational veriﬁcation.

8.4   Future Work
BiKAT provides a foundation for several interesting directions for future work in addition to ques-
tions raised in Sects. 6 and 7. As already detailed above, we are optimistic about the outlook for
automation.
   There are several open questions about completeness. We have proved soundness for a number
of forward and backward simulation rules, but have not investigated their completeness. Com-
pleteness in the sense of “true implies provable” is problematic owing to the possibility to reduce
the problem to unary Hoare logic via the self-composition rule. A more relevant notion is align-
ment completeness, which so far was formulated only for 2-safety [Nagasamudram and Naumann
2021]. One may think that BiKAT provides a notion of “regular alignment”, which could provide a
yardstick to evalute alignment completeness of other systems. However, in an applied BiKAT the
interpretation of tests, in combination with conditional alignments like Eqn. (7), expresses more
than regular patterns.
   What about completeness of the BiKAT axioms with respect to models? For KAT, Kozen and Smith
[1996] obtain completeness for relational models from a completeness result for a language model
called guarded strings. A guarded string model is given by sets of primitive actions and primitive
tests. An atom is a boolean valuation of primitive tests. The model is the trace model where Σ is
the set of atoms and all sequences are admissible. The guarded string model has a canonical inter-
pretation of its primitive tests and actions. Being a trace model, it gives rise to a trace BiKAT. One
can then interpret primitive bitests as relations on atoms. However, the trace BiKAT for guarded
strings does not determine a canonical interpretation of bitests; nor does it validate LRC. Several
problems remain open: Is BiKAT, or BiKAT with projections, complete for relational models? Is
there a class of BiKATs where the underlying KAT is a guarded string model, for which BiKAT is
complete?
   General study of algebras of programs has a long history [Hoare et al. 1987] and remains ac-
tive [Höfner et al. 2019]. Because KAT is about control structure it seems particularly suited to
describing alignment. For reasoning, however, other algebraic structures are relevant, e.g., Con-
current Kleene Algebra [Hoare et al. 2016] has an operator that can model spatial separation and
it would be interesting to explore some notion of spatial locality in connection with alignment
and BiKAT. We have highlighted the relevance of relation algebra, as also done in the Coq library
of Damien Pous for KAT [Pous [n. d.]]. Such settings may be helpful for further exploration of
∀∃ properties along the lines of TriKAT, and for relational properties of nonterminating programs
(e.g., using 𝜔-algebra [Cohen 2000]). One speciﬁc question is whether some formulation of TriKAT
can be used to obtain an algebraic proof to generalize Theorem 7.3.

ACKNOWLEDGMENTS
The authors would like to thank Anindya Banerjee, Lennart Beringer and Michael Greenberg for
helpful discussions and the anonymous reviewers for their valuable feedback.
  Authors Antonopoulos, Koskinen, Le, and Naumann were supported in part by the Oﬃce of
Naval Research under Grant No. N00014-17-1-2787. Antonopoulos, Koskinen and Le were sup-
ported in part by NSF award CCF-2106845. Antonopoulos was supported in part by NSF award
CCF-2131476. Naumann, Nagasamudram, and Ngo were supported in part by NSF award CNS-
1718713.

                                Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:30   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


REFERENCES
Martín Abadi and Leslie Lamport. 1988. The Existence of Reﬁnement Mappings. In Proceedings of LICS.
Timos Antonopoulos, Eric Koskinen, and Ton Chanh Le. 2019. Speciﬁcation and inference of trace reﬁnement relations.
   Proceedings of the ACM on Programming Languages 3, OOPSLA (2019), 1–30.
Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo. 2022a.
   An algebra of alignment for relational veriﬁcation (extended version). CoRR abs/2202.04278 (2022). arXiv:2202.04278
   https://arxiv.org/abs/2202.04278
Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo. 2022b.
   An algebra of alignment for relational veriﬁcation (artifact). https://doi.org/10.5281/zenodo.7144067
Krzysztof R. Apt, Frank S. de Boer, and Ernst-Rüdiger Olderog. 2009. Veriﬁcation of Sequential and Concurrent Programs (3
   ed.). Springer. https://doi.org/10.1007/978-1-84882-745-5
Sahar Badihi, Faridah Akinotcho, Yi Li, and Julia Rubin. 2020. ARDiﬀ: Scaling Program Equivalence Checking via Itera-
   tive Abstraction and Reﬁnement of Common Code. In Joint Meeting on European Software Engineering Conference and
   Symposium on the Foundations of Software Engineering. 13–24. https://doi.org/10.1145/3368089.3409757
Anindya Banerjee, Ramana Nagasamudram, Mohammad Nikouei, and David A. Naumann. 2022. A Relational Program
   Logic with Data Abstraction and Dynamic Framing. ACM Transactions on Programming Languages and Systems (2022).
   Accepted for publication. Available as http://arxiv.org/abs/1910.14560.
Anindya Banerjee, David A. Naumann, and Mohammad Nikouei. 2016. Relational Logic with Framing and Hypotheses. In
   36th IARCS Annual Conference on Foundations of Software Technology and Theoretical Computer Science. Long version
   at http://arxiv.org/abs/1611.08992.
Gilles Barthe, Juan Manuel Crespo, and César Kunz. 2011a. Relational Veriﬁcation Using Product Programs. In Formal
   Methods.
Gilles Barthe, Juan Manuel Crespo, and César Kunz. 2013. Beyond 2-Safety: Asymmetric Product Programs for Relational
   Program Veriﬁcation. In Logical Foundations of Computer Science (LFCS) (LNCS, Vol. 7734). 29–43.
Gilles Barthe, Juan Manuel Crespo, and César Kunz. 2016. Product Programs and Relational Program Logics. J. Logical and
   Algebraic Methods in Programming 85, 5 (2016), 847–859.
Gilles Barthe, Pedro R. D’Argenio, and Tamara Rezk. 2004. Secure Information Flow by Self-Composition. In IEEE CSFW.
   See extended version [Barthe et al. 2011b].
Gilles Barthe, Pedro R. D’Argenio, and Tamara Rezk. 2011b. Secure information ﬂow by self-composition. Math. Struct.
   Comput. Sci. 21, 6 (2011).
Gilles Barthe, Renate Eilers, Pamina Georgiou, Bernhard Gleiss, Laura Kovács, and Matteo Maﬀei. 2019. Verifying relational
   properties using trace logic. In 2019 Formal Methods in Computer Aided Design (FMCAD). 170–178.
Gilles Barthe, Benjamin Grégoire, Justin Hsu, and Pierre-Yves Strub. 2017. Coupling proofs are probabilistic product pro-
   grams. In ACM Symposium on Principles of Programming Languages. 161–174. https://doi.org/10.1145/3009837.3009896
Bernhard Beckert and Mattias Ulbrich. 2018. Trends in relational program veriﬁcation. In Principled Software Development.
   Springer, 41–58.
N. Benton. 2004. Simple Relational Correctness Proofs for Static Analyses and Program Transformations. In POPL. 14–25.
Lennart Beringer. 2011. Relational Decomposition. In Interactive Theorem Proving (ITP) (LNCS, Vol. 6898).
Raven Beutner and Bernd Finkbeiner. 2022. Software Veriﬁcation of Hyperproperties Beyond k-Safety. In Computer Aided
   Veriﬁcation. 341–362. https://doi.org/10.1007/978-3-031-13185-1_17
Lionel Blatter, Nikolai Kosmatov, and Pascale Prevosto, Virgileand Le Gall. 2022. Certiﬁed Veriﬁcation of Relational Prop-
   erties. In Integrated Formal Methods. 86–105.
Thomas Braibant and Damien Pous. 2010. An eﬃcient Coq tactic for deciding Kleene algebras. In International Conference
   on Interactive Theorem Proving. 163–178.
Berkeley R. Churchill, Oded Padon, Rahul Sharma, and Alex Aiken. 2019. Semantic program alignment for equivalence
   checking. In PLDI.
Michael R. Clarkson, Bernd Finkbeiner, Masoud Koleini, Kristopher K. Micinski, Markus N. Rabe, and César Sánchez. 2014.
   Temporal Logics for Hyperproperties. In Principles of Security and Trust (POST) (LNCS, Vol. 8414). 265–284.
Michael R. Clarkson and Fred B. Schneider. 2010. Hyperproperties. Journal of Computer Security 18, 6 (2010), 1157–1210.
Martin Clochard, Claude Marché, and Andrei Paskevich. 2020. Deductive Veriﬁcation with Ghost Monitors. Proc. ACM
   Program. Lang. 4, POPL (2020).
Ernie Cohen. 2000. Separation and Reduction. In Mathematics of Program Construction (LNCS, Vol. 1837). 45–59.
   https://doi.org/10.1007/10722010_4
Willem-Paul de Roever, Frank de Boer, Ulrich Hannemann, Jozef Hooman, Yassine Lakhnech, Mannes Poel, and Job Zwiers.
   2001. Concurrency Veriﬁcation: Introduction to Compositional and Noncompositional Methods. Cambridge University.
Willem-Paul de Roever and Kai Engelhardt. 1998. Data Reﬁnement: Model-Oriented Proof Methods and their Comparison.
   Cambridge University Press.


Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                               20:31


Amina Doumane, Denis Kuperberg, Damien Pous, and Pierre Pradic. 2019. Kleene Algebra with Hypotheses. In Foundations
   of Software Science and Computation Structures (FOSSACS) (LNCS, Vol. 11425). 207–223.
Emanuele D’Osualdo, Azadeh Farzan, and Derek Dreyer. 2022. Proving Hypersafety Compositionally. Proc. ACM Program.
   Lang. 6, OOPSLA2, Article 135 (2022), 26 pages. https://doi.org/10.1145/3563298
Marco Eilers, Peter Müller, and Samuel Hitz. 2018. Modular Product Programs. In European Symposium on Programming.
Azadeh Farzan and Anthony Vandikas. 2019. Automated hypersafety veriﬁcation. In Computer Aided Veriﬁcation. 200–218.
Robert Floyd. 1967. Assigning Meaning to Programs. In Symp. on Applied Math. 19, Math. Aspects of Comp. Sci. Amer. Math.
   Soc., 19–32.
Nissim Francez. 1983. Product Properties and Their Direct Veriﬁcation. Acta Informatica 20 (1983), 329–344.
Peter J. Freyd and Andre Scedrov. 1990. Categories, Allegories. North-Holland.
Dan Frumin, Robbert Krebbers, and Lars Birkedal. 2018. ReLoC: A Mechanised Relational Logic for Fine-Grained Concur-
   rency. In IEEE Symp. on Logic in Computer Science. 442–451.
Dan Frumin, Robbert Krebbers, and Lars Birkedal. 2020. ReLoC Reloaded: A Mechanized Relational Logic for Fine-Grained
   Concurrency and Logical Atomicity. CoRR abs/2006.13635 (2020). arXiv:2006.13635 https://arxiv.org/abs/2006.13635
Benny Godlin and Ofer Strichman. 2008. Inference rules for proving the equivalence of recursive procedures. Acta Inf. 45,
   6 (2008), 403–439.
Manish Goyal, Muqsit Azeem, Kumar Madhukar, and R. Venkatesh. 2021. Direct Construction of Program Alignment
   Automata for Equivalence Checking. https://doi.org/10.48550/ARXIV.2109.01864
Michael Greenberg, Ryan Beckett, and Eric Hayden Campbell. 2022. Kleene algebra modulo theories: a framework for
   concrete KATs. In PLDI. 594–608. https://doi.org/10.1145/3519939.3523722
Lennard Gäher, Michael Sammler, Simon Spies, Ralf Jung, Hoang-Hai Dang, Robbert Krebbers, Jeehoon Kang, and Derek
   Dreyer. 2022. Simuliris: a separation logic framework for verifying concurrent program optimizations. Proc. ACM
   Program. Lang. 6, POPL (2022).
Chris Hawblitzel, Ming Kawaguchi, Shuvendu K. Lahiri, and Henrique Rebêlo. 2013. Towards Modularly Comparing Pro-
   grams Using Automated Theorem Provers. In CADE. 282–299.
C. A. R. Hoare, I.J. Hayes, He Jifeng, C.C. Morgan, A.W. Roscoe, J.W. Sanders, I.H. Sorensen, J.M. Spivey, and B.A. Sufrin.
   1987. Laws of Programming. Commun. ACM 30 (1987), 672–686,770.
Tony Hoare, Stephan van Staden, Bernhard Möller, Georg Struth, and Huibiao Zhu. 2016. Developments in concurrent
   Kleene algebra. J. Log. Algebraic Methods Program. 85, 4 (2016), 617–636. https://doi.org/10.1016/j.jlamp.2015.09.012
Peter Höfner, Damien Pous, and Georg Struth. 2019. Relational and algebraic methods in computer science. J. Log. Algebraic
   Methods Program. 106 (2019), 198–199. https://doi.org/10.1016/j.jlamp.2019.05.005
Máté Kovács, Helmut Seidl, and Bernd Finkbeiner. 2013. Relational abstract interpretation for the veriﬁcation of 2-
   hypersafety properties. In ACM Computer and Communications Security.
Dexter Kozen. 1997. Kleene algebra with tests. ACM Transactions on Programming Languages and Systems 19, 3 (1997),
   427–443.
Dexter Kozen. 2000. On Hoare logic and Kleene algebra with tests. ACM Trans. Comput. Log. 1, 1 (2000), 60–76.
Dexter Kozen. 2003. Kleene algebra with tests and the static analysis of programs. Technical Report. Cornell University.
Dexter Kozen. 2004. Some results in dynamic model theory. Sci. Comput. Program. 51, 1-2 (2004), 3–22.
Dexter Kozen and Frederick Smith. 1996. Kleene algebra with tests: Completeness and decidability. In International Work-
   shop on Computer Science Logic. Springer, 244–259.
Leslie Lamport and Fred B. Schneider. 2021. Verifying Hyperproperties With TLA. In IEEE Computer Security Foundations
   Symposium (CSF). 1–16.
Kenji Maillard, Cătălin Hritçu, Exequiel Rivas, and Antoine Van Muylder. 2020. The Next 700 Relational Program Logics.
   Proc. ACM Program. Lang. 4, POPL (2020), 4:1–4:33.
Konstantinos Mamouras. 2017. Equational Theories of Abnormal Termination Based on Kleene Algebra. In FoSSaCS. 88–
   105.
Dmitry Mordvinov and Grigory Fedyukovich. 2019. Property Directed Inference of Relational Invariants. In Formal Methods
   in Computer Aided Design. 152–160. https://doi.org/10.23919/FMCAD.2019.8894274
Carroll Morgan. 1988. Auxiliary Variables in Data Reﬁnement. Inform. Process. Lett. 29, 6 (1988), 293–296.
Toby Murray. 2020. An Under-Approximate Relational Logic: Heralding Logics of Insecurity, Incorrect Implementation &
   More. CoRR abs/2003.04791 (2020). arXiv:2003.04791 https://arxiv.org/abs/2003.04791
Ramana Nagasamudram and David A. Naumann. 2021. Alignment Completeness for Relational Hoare Logics. In IEEE Symp.
   on Logic in Computer Science. 1–13. Extended version at https://arxiv.org/abs/2101.11730..
David A. Naumann. 2020. Thirty-Seven Years of Relational Hoare Logic: Remarks on Its Principles and History.
   In 9th International Symposium On Leveraging Applications of Formal Methods, Veriﬁcation and Validation. 93–116.
   https://doi.org/10.1007/978-3-030-61470-6_7 Extended version at https://arxiv.org/abs/2007.06421..
Peter W O’Hearn. 2019. Incorrectness logic. Proceedings of the ACM on Programming Languages 4, POPL (2019), 1–32.


                                 Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:32   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


Lauren Pick, Grigory Fedyukovich, and Aarti Gupta. 2018. Exploiting Synchrony and Symmetry in Relational Veriﬁcation.
   In Computer Aided Veriﬁcation. 164–182.
Damien Pous. [n. d.]. Relation Algebra and KAT in Coq. http://perso.ens-lyon.fr/damien.pous/ra/ Coq library, accessed
   July 2022.
Damien Pous. 2015. Symbolic algorithms for language equivalence and Kleene algebra with tests. In ACM Symposium on
   Principles of Programming Languages. 357–368.
Damien Pous, Jurriaan Rot, and Jana Wagemaker. 2021. On Tools for Completeness of Kleene Algebra with Hypotheses.
   In Relational and Algebraic Methods in Computer Science (RAMiCS) (LNCS, Vol. 13027). 378–395.
Andrei Sabelfeld and Andrew C. Myers. 2003. Language-Based Information-Flow Security. IEEE J. Selected Areas in Com-
   munications 21, 1 (Jan. 2003), 5–19.
Rahul Sharma, Eric Schkufza, Berkeley Churchill, and Alex Aiken. 2013.                  Data-Driven Equivalence Check-
   ing. In ACM Conf. on Object-Oriented Programming Languages, Systems, and Applications. 391–406.
   https://doi.org/10.1145/2509136.2509509
Ron Shemer, Arie Gurﬁnkel, Sharon Shoham, and Yakir Vizel. 2019. Property directed self composition. In International
   Conference on Computer Aided Veriﬁcation. Springer, 161–179.
Marcelo Sousa and Isil Dillig. 2016. Cartesian Hoare logic for verifying k-safety properties. In Proceedings of the 37th ACM
   SIGPLAN Conference on Programming Language Design and Implementation. 57–69.
Tachio Terauchi and Alex Aiken. 2005. Secure information ﬂow as a safety problem. In International Static Analysis Sym-
   posium. Springer, 352–367.
Hiroshi Unno, Tachio Terauchi, and Eric Koskinen. 2021. Constraint-Based Relational Veriﬁcation. In Computer Aided
   Veriﬁcation. 742–766.
Jana Wagemaker, Marcello M. Bonsangue, Tobias Kappé, Jurriaan Rot, and Alexandra Silva. 2019. Completeness and In-
   completeness of Synchronous Kleene Algebra. In Mathematics of Program Construction (LNCS, Vol. 11825). 385–413.
Hongseok Yang. 2007. Relational Separation Logic. Theo. Comp. Sci. 375 (2007).
Cheng Zhang, Arthur Azevedo de Amorim, and Marco Gaboardi. 2022. On incorrectness logic and Kleene algebra with
   top and tests. Proc. ACM Program. Lang. 6, POPL (2022), 1–30. https://doi.org/10.1145/3498690




Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                           20:33


9 APPENDIX
9.1 Some KAT Lemmas
This section proves some results that hold in any KAT, including useful consequences of commu-
tativity assumptions. We begin with a few well known and easily proved facts for which proofs
are omitted.
   Lemma 9.1 (invariance). Let 𝑝 be a test, then 𝑝; 𝑥 ≤ 𝑝; 𝑥; 𝑝 ⇒ 𝑝; 𝑥 ∗ ≤ 𝑝; 𝑥 ∗ ; 𝑝.
   Lemma 9.2 (backward invariance). Let 𝑝 be a test, then 𝑥; 𝑝 = 𝑝; 𝑥; 𝑝 ⇒ 𝑥 ∗ ; 𝑝 = 𝑝; 𝑥 ∗; 𝑝.
   Lemma 9.3. Let 𝑝 be a test, then 𝑥; 𝑝 ≤ 𝑝; 𝑥; 𝑝 ⇒ 𝑥 ∗ ; 𝑝 ≤ 𝑝; (𝑥; 𝑝) ∗; 𝑝.
   Lemma 9.4. If 𝑥; 𝑦 ≤ 𝑥; 𝑦; 𝑥 then 𝑥; 𝑦 ∗ ≤ 𝑥; (𝑦; 𝑥) ∗ .
   Kozen [Kozen 1997] uses the following in the case that 𝑤 is a test.
   Lemma 9.5. If 𝑥; 𝑤 = 𝑤; 𝑥 and 𝑤; 𝑤 = 𝑤 then 𝑥 ∗ ; 𝑤 = (𝑥; 𝑤) ∗ ; 𝑤.
   Lemma 9.6. If 1 ≤ 𝑧 and 𝑧; 𝑧 ≤ 𝑧 then 𝑥 ≤ 𝑦; 𝑧 ⇔ 𝑥; 𝑧 ≤ 𝑦; 𝑧
  KAT and Commutativity. There are several useful laws for iteration involving two terms that
commute. These hold in any KAT.
   Lemma 9.7. 𝑤; 𝑧 = 𝑧; 𝑤 ⇒ 𝑤 ∗ ; 𝑧 = 𝑧; 𝑤 ∗
   Proof by mutual inclusion. For 𝑤 ∗ ; 𝑧 ≤ 𝑧; 𝑤 ∗ we have
                        𝑤 ∗ ; 𝑧 ≤ 𝑧; 𝑤 ∗
                      ⇐ 𝑧 + 𝑤; 𝑧; 𝑤 ∗ ≤ 𝑧; 𝑤 ∗                   ind 𝑏 + 𝑎𝑥 ≤ 𝑥 ⇒ 𝑎 ∗𝑏 ≤ 𝑥
                      ⇔ 𝑧 ≤ 𝑧; 𝑤 ∗ ∧ 𝑤; 𝑧; 𝑤 ∗ ≤ 𝑧; 𝑤 ∗          join
                      ⇔ 𝑧 ≤ 𝑧; 𝑤 ∗ ∧ 𝑧; 𝑤; 𝑤 ∗ ≤ 𝑧; 𝑤 ∗          𝑤; 𝑧 = 𝑧; 𝑤
The two conjuncts hold by the star laws 1 ≤ 𝑥 ∗ and 𝑥; 𝑥 ∗ ≤ 𝑥 ∗ and monotonicity of ;. The reverse
inclusion is proved similarly, using the other induction rule 𝑏 + 𝑥𝑎 ≤ 𝑥 ⇒ 𝑏𝑎 ∗ ≤ 𝑥.
   Lemma 9.8. 𝑤; 𝑧 = 𝑧; 𝑤 ⇒ (𝑤 + 𝑧) ∗ = 𝑤 ∗ ; 𝑧 ∗ .
   Proof by mutual inclusion. One inclusion does not require the commutativity assumption:
                                  𝑤 ∗; 𝑧∗
                                ≤ (𝑤 + 𝑧) ∗ ; (𝑤 + 𝑧) ∗      𝑥 ≤ 𝑥 + 𝑦, star mono
                                = (𝑤 + 𝑧) ∗                  star law 𝑥 ∗ ; 𝑥 ∗ = 𝑥 ∗
For the reverse we have:
            (𝑤 + 𝑧) ∗ ≤ 𝑤 ∗ ; 𝑧 ∗
      ⇔ 1 + (𝑤 + 𝑧); (𝑤 + 𝑧) ∗ ≤ 𝑤 ∗ ; 𝑧 ∗                                                     star unfold
      ⇔ 1 ≤ 𝑤 ∗ ; 𝑧 ∗ ∧ (𝑤 + 𝑧); (𝑤 + 𝑧) ∗ ≤ 𝑤 ∗ ; 𝑧 ∗                                         + join
      ⇔ (𝑤 + 𝑧); (𝑤 + 𝑧) ∗ ≤ 𝑤 ∗ ; 𝑧 ∗                                                         using 1 ≤ 𝑥 ∗
      ⇐ 𝑤 + 𝑧 + 𝑤 ∗ ; 𝑧 ∗ ; (𝑤 + 𝑧) ≤ 𝑤 ∗ ; 𝑧 ∗                                                star induct
      ⇔ 𝑤 + 𝑧 + 𝑤 ∗; 𝑧∗; 𝑤 + 𝑤 ∗; 𝑧∗; 𝑧 ≤ 𝑤 ∗; 𝑧∗                                              distrib
      ⇔ 𝑤 ≤ 𝑤 ∗; 𝑧∗ ∧ 𝑧 ≤ 𝑤 ∗; 𝑧∗ ∧ 𝑤 ∗; 𝑧∗; 𝑤 ≤ 𝑤 ∗; 𝑧∗ ∧ 𝑤 ∗; 𝑧∗; 𝑧 ≤ 𝑤 ∗; 𝑧∗                + join
      ⇔ 𝑤 ≤ 𝑤 ∗ ; 𝑧 ∗ ∧ 𝑧 ≤ 𝑤 ∗ ; 𝑧 ∗ ∧ 𝑤 ∗ ; 𝑤; 𝑧 ∗ ≤ 𝑤 ∗ ; 𝑧 ∗ ∧ 𝑤 ∗ ; 𝑧 ∗ ; 𝑧 ≤ 𝑤 ∗ ; 𝑧 ∗   Lemma 9.7
The left two conjuncts follow using 𝑥 ≤ 𝑥 ∗ and 1 ≤ 𝑥 ∗ . The right two conjuncts follow using
𝑥 ∗; 𝑥 ≤ 𝑥 ∗.
   Lemma 9.9. 𝑤; 𝑧 = 𝑧; 𝑤 ⇒ 𝑤 ∗ ; 𝑧 ∗ = 𝑧 ∗ ; 𝑤 ∗

                                Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:34   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


   Proof: 𝑤 ∗ ; 𝑧 ∗ = (𝑤 + 𝑧) ∗ = (𝑧 + 𝑤) ∗ = 𝑧 ∗ ; 𝑤 ∗ using Lemma 9.8 twice.
   Lemma 9.10. 𝑤; 𝑧 = 𝑧; 𝑤 ⇒ (𝑤; 𝑧) ∗ ≤ 𝑤 ∗ ; 𝑧 ∗
   Proof:
                        (𝑤; 𝑧) ∗ ≤ 𝑤 ∗ ; 𝑧 ∗
                  ⇔     1 ≤ 𝑤 ∗ ; 𝑧 ∗ ∧ 𝑤; 𝑧; (𝑤; 𝑧) ∗ ≤ 𝑤 ∗ ; 𝑧 ∗   star unfold, + join
                  ⇔     𝑤; 𝑧; (𝑤; 𝑧) ∗ ≤ 𝑤 ∗ ; 𝑧 ∗                   using 1 ≤ 𝑥 ∗
                  ⇐     𝑤; 𝑧 + 𝑤 ∗ ; 𝑧 ∗ ; 𝑤; 𝑧 ≤ 𝑤 ∗ ; 𝑧 ∗          ind 𝑏 + 𝑥𝑎 ≤ 𝑥 ⇒ 𝑏𝑎 ∗ ≤ 𝑥
                  ⇔     𝑤 ∗ ; 𝑧 ∗ ; 𝑤; 𝑧 ≤ 𝑤 ∗ ; 𝑧 ∗                 + join, 𝑥 ≤ 𝑥 ∗
                  ⇔     𝑤 ∗ ; 𝑧 ∗ ; 𝑧; 𝑤 ≤ 𝑤 ∗ ; 𝑧 ∗                 𝑤; 𝑧 = 𝑧; 𝑤
                  ⇐     𝑤 ∗; 𝑧∗ ; 𝑤 ≤ 𝑤 ∗; 𝑧∗                        𝑥 ∗𝑥 ≤ 𝑥 ∗
                  ⇐     𝑤 ∗ ; 𝑤; 𝑧 ∗ ≤ 𝑤 ∗ ; 𝑧 ∗                     Lemma 9.7
                  ⇐     𝑤 ∗; 𝑧∗ ≤ 𝑤 ∗; 𝑧∗                            𝑥𝑥 ∗ ≤ 𝑥 ∗
As usual the hints do not mention uses of transitivity and monotonicity.
   Lemma 9.11. 𝑤; 𝑧 = 𝑧; 𝑤 ⇒ 𝑤 ∗ ; 𝑧 ∗ = (𝑤; 𝑧) ∗ ; (𝑤 ∗ + 𝑧 ∗ )
   Proof by mutual inclusion. First,
                                (𝑤; 𝑧) ∗ ; (𝑤 ∗ + 𝑧 ∗ )
                              ≤ 𝑤 ∗ ; 𝑧 ∗ ; (𝑤 ∗ + 𝑧 ∗ )    Lemma 9.10
                              ≤ 𝑤 ∗; 𝑧∗; 𝑤 ∗; 𝑧∗            𝑥 ∗ + 𝑦 ∗ ≤ 𝑥 ∗ ; 𝑦 ∗ by KAT
                              = 𝑤 ∗; 𝑤 ∗; 𝑧∗ ; 𝑧∗           Lemma 9.9
                              = 𝑤 ∗; 𝑧∗                     𝑥 ∗ ; 𝑥 ∗ = 𝑥 ∗ by KAT
For the reverse inclusion,
        𝑤 ∗ ; 𝑧 ∗ ≤ (𝑤; 𝑧) ∗ ; (𝑤 ∗ + 𝑧 ∗ )
 ⇔      (𝑤 + 𝑧) ∗ ≤ (𝑤; 𝑧) ∗ ; (𝑤 ∗ + 𝑧 ∗ )                                            Lemma 9.8
 ⇔      1 ≤ (𝑤; 𝑧) ∗ ; (𝑤 ∗ + 𝑧 ∗ ) ∧ (𝑤 + 𝑧) ∗ ; (𝑤 + 𝑧) ≤ (𝑤; 𝑧) ∗ ; (𝑤 ∗ + 𝑧 ∗ )    star expansion, + join
 ⇔      (𝑤 + 𝑧) ∗ ; (𝑤 + 𝑧) ≤ (𝑤; 𝑧) ∗ ; (𝑤 ∗ + 𝑧 ∗ )                                  using 1 ≤ 𝑥 ∗
 ⇐      𝑤 + 𝑧 + (𝑤 + 𝑧); (𝑤; 𝑧) ∗ ; (𝑤 ∗ + 𝑧 ∗ ) ≤ (𝑤; 𝑧) ∗ ; (𝑤 ∗ + 𝑧 ∗ )             ind 𝑏 + 𝑎𝑥 ≤ 𝑥 ⇒ 𝑎 ∗𝑏 ≤ 𝑥
By join property of +, the last line is equivalent to the conjunction of 𝑤 + 𝑧 ≤ (𝑤; 𝑧) ∗ ; (𝑤 ∗ + 𝑧 ∗ ),
which follows easily using 𝑥 ≤ 𝑥 ∗ , and this:
                               (𝑤 + 𝑧); (𝑤; 𝑧) ∗ ; (𝑤 ∗ + 𝑧 ∗ ) ≤ (𝑤; 𝑧) ∗ ; (𝑤 ∗ + 𝑧 ∗ )
Using distributivity on the left side, and the join property, the displayed inequality is equivalent
to the conjunction of four conditions:
𝑤; (𝑤; 𝑧) ∗ ; 𝑤 ∗ ≤ (𝑤; 𝑧) ∗ ; (𝑤 ∗ + 𝑧 ∗ ),
𝑧; (𝑤; 𝑧) ∗ ; 𝑤 ∗ ≤ (𝑤; 𝑧) ∗ ; (𝑤 ∗ + 𝑧 ∗ ),
𝑤; (𝑤; 𝑧) ∗ ; 𝑧 ∗ ≤ (𝑤; 𝑧) ∗ ; (𝑤 ∗ + 𝑧 ∗ ), and
𝑧; (𝑤; 𝑧) ∗ ; 𝑧 ∗ ≤ (𝑤; 𝑧) ∗ ; (𝑤 ∗ + 𝑧 ∗ ).
For the ﬁrst condition:
                                𝑤; (𝑤; 𝑧) ∗ ; 𝑤 ∗
                              = 𝑤; (𝑧; 𝑤) ∗ ; 𝑤 ∗           assumption 𝑤; 𝑧 = 𝑧; 𝑤
                              = (𝑤; 𝑧) ∗ ; 𝑤; 𝑤 ∗           sliding 𝑥 (𝑦𝑥) ∗ = (𝑥𝑦) ∗𝑥
                              ≤ (𝑤; 𝑧) ∗ ; 𝑤 ∗              𝑥; 𝑥 ∗ ≤ 𝑥 ∗
                              ≤ (𝑤; 𝑧) ∗ ; (𝑤 ∗ + 𝑧 ∗ )     𝑥 ≤ 𝑥 + 𝑦, mono

Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                                                  20:35


For the second condition,
                                𝑧; (𝑤; 𝑧) ∗ ; 𝑤 ∗
                          =     (𝑧; 𝑤) ∗ ; 𝑧; 𝑤 ∗                              sliding 𝑥 (𝑦𝑥) ∗ = (𝑥𝑦) ∗𝑥
                          =     (𝑧; 𝑤) ∗ ; 𝑧; (1 + 𝑤; 𝑤 ∗ )                    star unfold
                          =     (𝑧; 𝑤) ∗ ; 𝑧 + (𝑧; 𝑤) ∗ ; 𝑧; 𝑤; 𝑤 ∗            distrib
                          ≤     (𝑧; 𝑤) ∗ ; 𝑧 ∗ + (𝑧; 𝑤) ∗ ; 𝑧; 𝑤; 𝑤 ∗          𝑥 ≤ 𝑥∗
                          ≤     (𝑧; 𝑤) ∗ ; 𝑧 ∗ + (𝑧; 𝑤) ∗ ; 𝑤 ∗                𝑥 ∗; 𝑥 ≤ 𝑥 ∗
                          =     (𝑧; 𝑤) ∗ ; (𝑧 ∗ + 𝑤 ∗ )                        distrib
                          =     (𝑤; 𝑧) ∗ ; (𝑤 ∗ + 𝑧 ∗ )                        assumption 𝑤; 𝑧 = 𝑧; 𝑤
The other two conditions are symmetric with these two.
  Here’s another expansion lemma that can be used to relate two loops.
   Lemma 9.12. 𝑤; 𝑧 = 𝑧; 𝑤 ⇒ 𝑤 ∗ ; 𝑧 ∗ = (𝑤; 𝑧 + 𝑤 + 𝑧) ∗
  Proof by mutual inclusion. We have 𝑤 ∗ ; 𝑧 ∗ ≤ (𝑤; 𝑧 + 𝑤 + 𝑧) ∗ because 𝑤 ∗ ; 𝑧 ∗ = (𝑤 + 𝑧) ∗ ≤
(𝑤; 𝑧 + 𝑤 + 𝑧) ∗ by Lemma 9.8 and then (𝑦+) increasing, star mono.
  For the reverse, we have
              (𝑤; 𝑧 + 𝑤 + 𝑧) ∗ ≤ 𝑤 ∗ ; 𝑧 ∗
            ⇔ 1 + (𝑤; 𝑧 + 𝑤 + 𝑧) ∗ ; (𝑤; 𝑧 + 𝑤 + 𝑧) ≤ 𝑤 ∗ ; 𝑧 ∗                           star expansion
            ⇔ (𝑤; 𝑧 + 𝑤 + 𝑧) ∗ ; (𝑤; 𝑧 + 𝑤 + 𝑧) ≤ 𝑤 ∗ ; 𝑧 ∗                               using + join and 1 ≤ 𝑥 ∗
            ⇐ 𝑤; 𝑧 + 𝑤 + 𝑧 + (𝑤; 𝑧 + 𝑤 + 𝑧); 𝑤 ∗ ; 𝑧 ∗ ≤ 𝑤 ∗ ; 𝑧 ∗                        ind 𝑏 + 𝑎𝑥 ≤ 𝑥 ⇒ 𝑎 ∗𝑏 ≤ 𝑥
The last line can be decomposed, using join, to easy conditions 𝑤; 𝑧 ≤ 𝑤 ∗ ; 𝑧 ∗ , 𝑤 ≤ 𝑤 ∗ ; 𝑧 ∗ , and
𝑧 ≤ 𝑤 ∗ ; 𝑧 ∗ , together with this:
                                                (𝑤; 𝑧 + 𝑤 + 𝑧); 𝑤 ∗ ; 𝑧 ∗ ≤ 𝑤 ∗ ; 𝑧 ∗
which by distribution and join property is equivalent to the three conjuncts
                         𝑤; 𝑧; 𝑤 ∗ ; 𝑧 ∗ ≤ 𝑤 ∗ ; 𝑧 ∗ ∧ 𝑤; 𝑤 ∗ ; 𝑧 ∗ ≤ 𝑤 ∗ ; 𝑧 ∗ ∧ 𝑧; 𝑤 ∗ ; 𝑧 ∗ ≤ 𝑤 ∗ ; 𝑧 ∗
The ﬁrst holds because
                                          𝑤; 𝑧; 𝑤 ∗ ; 𝑧 ∗
                                        = 𝑧; 𝑤; 𝑤 ∗ ; 𝑧 ∗         assumption 𝑤; 𝑧 = 𝑧; 𝑤
                                        ≤ 𝑧; 𝑤 ∗ ; 𝑧 ∗            𝑥𝑥 ∗ ≤ 𝑥 ∗
                                        = 𝑤 ∗ ; 𝑧; 𝑧 ∗            Lemma 9.7
                                        ≤ 𝑤 ∗; 𝑧∗                 𝑥𝑥 ∗ ≤ 𝑥 ∗
The second and third are similar.

9.2 BiKAT Theorems
This section proves results that hold in any BiKAT.
   Lemma 9.13. In a BiKAT we have 𝑋 ; h𝑦] ≤ 𝑍 ; [havi iﬀ 𝑋 ; h𝑦 | havi ≤ 𝑍 ; [havi.
  Proof: By deﬁnition 𝑋 ; h𝑦 | havi = 𝑋 ; h𝑦]; [havi, and now we can apply Lemma 9.6 because
[havi is idempotent and above 1.
   Lemma 9.14. Equation (3) holds, i.e., for any 𝑐, 𝑐 ′ and tests 𝑒, 𝑒 ′ in the underlying KAT:
         h(𝑒; 𝑐) ∗ | (𝑒 ′ ; 𝑐 ′ ) ∗ i; h¬𝑒 | ¬𝑒 ′ i = h𝑒; 𝑐 | 𝑒 ′ ; 𝑐 ′ i ∗ ; (h𝑒; 𝑐 | ¬𝑒 ′ i ∗ + h¬𝑒 | 𝑒 ′ ; 𝑐 ′ i ∗ ); h¬𝑒 | ¬𝑒 ′ i

                                     Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:36   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


  Proof by mutual inclusion. For readability we omit the embedding notations, i.e., 𝑐 stands for
h𝑐], 𝑐 ′ for [𝑐 ′ i, etc. The sequence operation is written variously by juxtaposition, semicolon, and
bar |. (Bar because h𝑥 | 𝑦i is shorthand for the sequence h𝑥]; [𝑦i.)
  For 𝑅𝐻𝑆 ≤ 𝐿𝐻𝑆 we have


                             (𝑒𝑐 |𝑒 ′𝑐 ′ ) ∗ ; ((𝑒𝑐 |¬𝑒 ′ ) ∗ + (¬𝑒 |𝑒 ′𝑐 ′ ) ∗ ) (¬𝑒 |¬𝑒 ′ )
                       ≤     (𝑒𝑐) ∗ ; (𝑒 ′𝑐 ′ ) ∗ ; ((𝑒𝑐 |¬𝑒 ′ ) ∗ + (¬𝑒 |𝑒 ′𝑐 ′ ) ∗ ) (¬𝑒 |¬𝑒 ′ )     Lemma 9.11
                       ≤     (𝑒𝑐 |) ∗ ; (|𝑒 ′𝑐 ′ ) ∗ ; (¬𝑒 |¬𝑒 ′ )                                     1 below star


   For 𝐿𝐻𝑆 ≤ 𝑅𝐻𝑆 we have


                         (𝑒𝑐 |) ∗ ; (|𝑒 ′𝑐 ′ ) ∗ ; (¬𝑒 |¬𝑒 ′) ≤ (𝑒𝑐 |𝑒 ′𝑐 ′ ) ∗ ; ((𝑒𝑐 |¬𝑒 ′) ∗ + (¬𝑒 |𝑒 ′𝑐 ′ ) ∗ ); (¬𝑒 |¬𝑒 ′)
                  ⇔        using Lemma 9.8
                         ((𝑒𝑐 |) + (|𝑒 ′𝑐 ′ )) ∗ ; (¬𝑒 |¬𝑒 ′) ≤ (𝑒𝑐 |𝑒 ′𝑐 ′) ∗ ; ((𝑒𝑐 |¬𝑒 ′) ∗ + (¬𝑒 |𝑒 ′𝑐 ′ ) ∗ ); (¬𝑒 |¬𝑒 ′)
                  ⇐        by ind 𝑏 + 𝑎𝑥 ≤ 𝑥 ⇒ 𝑎 ∗𝑏 ≤ 𝑥
                         (¬𝑒 |¬𝑒 ′) + ((𝑒𝑐 |) + (|𝑒 ′𝑐 ′ )); (𝑒𝑐 |𝑒 ′𝑐 ′) ∗ ; ((𝑒𝑐 |¬𝑒 ′) ∗ + (¬𝑒 |𝑒 ′𝑐 ′) ∗ ); (¬𝑒 |¬𝑒 ′)
                         ≤ (𝑒𝑐 |𝑒 ′𝑐 ′ ) ∗ ; ((𝑒𝑐 |¬𝑒 ′) ∗ + (¬𝑒 |𝑒 ′𝑐 ′) ∗ ); (¬𝑒 |¬𝑒 ′)
                  ⇔        using distrib leftmost; + join
                         (¬𝑒 |¬𝑒 ′) ≤ (𝑒𝑐 |𝑒 ′𝑐 ′ ) ∗ ; ((𝑒𝑐 |¬𝑒 ′) ∗ + (¬𝑒 |𝑒 ′𝑐 ′ ) ∗ ); (¬𝑒 |¬𝑒 ′)
                         ∧ ((𝑒𝑐 |) + (|𝑒 ′𝑐 ′ )); (𝑒𝑐 |𝑒 ′𝑐 ′ ) ∗ ; ((𝑒𝑐 |¬𝑒 ′) ∗ + (¬𝑒 |𝑒 ′𝑐 ′ ) ∗ ); (¬𝑒 |¬𝑒 ′)
                           ≤ (𝑒𝑐 |𝑒 ′𝑐 ′) ∗ ; ((𝑒𝑐 |¬𝑒 ′) ∗ + (¬𝑒 |𝑒 ′𝑐 ′ ) ∗ ); (¬𝑒 |¬𝑒 ′)
                  ⇔        ﬁrst conjunct holds using 1 ≤ 𝑥 ∗
                         ((𝑒𝑐 |) + (|𝑒 ′𝑐 ′ )); (𝑒𝑐 |𝑒 ′𝑐 ′) ∗ ; ((𝑒𝑐 |¬𝑒 ′) ∗ + (¬𝑒 |𝑒 ′𝑐 ′ ) ∗ ); (¬𝑒 |¬𝑒 ′)
                           ≤ (𝑒𝑐 |𝑒 ′𝑐 ′) ∗ ; ((𝑒𝑐 |¬𝑒 ′) ∗ + (¬𝑒 |𝑒 ′𝑐 ′ ) ∗ ); (¬𝑒 |¬𝑒 ′)


By distributivity the last line is equivalent to these four conditions:


     (𝐴)     (𝑒𝑐 |); (𝑒𝑐 |𝑒 ′𝑐 ′ ) ∗ ; (𝑒𝑐 |¬𝑒 ′ ) ∗ ; (¬𝑒 |¬𝑒 ′ ) ≤ (𝑒𝑐 |𝑒 ′𝑐 ′ ) ∗ ; ((𝑒𝑐 |¬𝑒 ′ ) ∗ + (¬𝑒 |𝑒 ′𝑐 ′ ) ∗ ); (¬𝑒 |¬𝑒 ′ )
     (𝐵)     (|𝑒 ′𝑐 ′ ); (𝑒𝑐 |𝑒 ′𝑐 ′ ) ∗ ; (𝑒𝑐 |¬𝑒 ′ ) ∗ ; (¬𝑒 |¬𝑒 ′ ) ≤ (𝑒𝑐 |𝑒 ′𝑐 ′ ) ∗ ; ((𝑒𝑐 |¬𝑒 ′ ) ∗ + (¬𝑒 |𝑒 ′𝑐 ′ ) ∗ ); (¬𝑒 |¬𝑒 ′ )
     (𝐶)     (𝑒𝑐 |); (𝑒𝑐 |𝑒 ′𝑐 ′ ) ∗ ; (¬𝑒 |𝑒 ′𝑐 ′ ) ∗ ; (¬𝑒 |¬𝑒 ′ ) ≤ (𝑒𝑐 |𝑒 ′𝑐 ′ ) ∗ ; ((𝑒𝑐 |¬𝑒 ′ ) ∗ + (¬𝑒 |𝑒 ′𝑐 ′ ) ∗ ); (¬𝑒 |¬𝑒 ′ )
     (𝐷)     (|𝑒 ′𝑐 ′ ); (𝑒𝑐 |𝑒 ′𝑐 ′ ) ∗ ; (¬𝑒 |𝑒 ′𝑐 ′ ) ∗ ; (¬𝑒 |¬𝑒 ′ ) ≤ (𝑒𝑐 |𝑒 ′𝑐 ′ ) ∗ ; ((𝑒𝑐 |¬𝑒 ′ ) ∗ + (¬𝑒 |𝑒 ′𝑐 ′ ) ∗ ); (¬𝑒 |¬𝑒 ′ )


We prove (𝐴) and (𝐵); then (𝐶) and (𝐷) follow for reasons of symmetry.
 For (𝐴):


        (𝑒𝑐 |); (𝑒𝑐; 𝑒 ′𝑐 ′ ) ∗ ; (𝑒𝑐 |¬𝑒 ′ ) ∗ ; (¬𝑒 |¬𝑒 ′ )
 =      (𝑒𝑐 |); (𝑒 ′𝑐 ′ ; 𝑒𝑐) ∗ ; (𝑒𝑐 |¬𝑒 ′ ) ∗ ; (¬𝑒 |¬𝑒 ′ )                 LRC (and def emb)
 =      (𝑒𝑐; 𝑒 ′𝑐 ′ ) ∗ ; 𝑒𝑐; (𝑒𝑐 |¬𝑒 ′ ) ∗ ; (¬𝑒 |¬𝑒 ′ )                     star sliding
 =      (𝑒𝑐; 𝑒 ′𝑐 ′ ) ∗ ; 𝑒𝑐; (¬𝑒 ′ ; 𝑒𝑐) ∗ ; (¬𝑒 |¬𝑒 ′ )                     LRC
 =      (𝑒𝑐; 𝑒 ′𝑐 ′ ) ∗ ; ¬𝑒 ′ ; 𝑒𝑐; (¬𝑒 ′ ; 𝑒𝑐) ∗ ; (¬𝑒 |¬𝑒 ′ )              test 𝑒 ′ idem, commutes with 𝑒𝑐, Lemma 9.7
 ≤      (𝑒𝑐; 𝑒 ′𝑐 ′ ) ∗ ; (¬𝑒 ′ ; 𝑒𝑐) ∗ ; (¬𝑒 |¬𝑒 ′ )                         using 𝑥; 𝑥 ∗ ≤ 𝑥 ∗
 ≤      (𝑒𝑐; 𝑒 ′𝑐 ′ ) ∗ ; ((¬𝑒 ′ ; 𝑒𝑐) ∗ + (¬𝑒 |𝑒 ′𝑐 ′ ) ∗ ); (¬𝑒 |¬𝑒 ′ )     + mono

Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                                                  20:37


   For (B):
      (|𝑒 ′𝑐 ′); (𝑒𝑐 |𝑒 ′𝑐 ′ ) ∗ ; (𝑒𝑐 |¬𝑒 ′) ∗ ; (¬𝑒 |¬𝑒 ′)
 =    (𝑒 ′𝑐 ′; 𝑒𝑐) ∗ ; (𝑒 ′𝑐 ′ ); (𝑒𝑐 |¬𝑒 ′) ∗ ; (¬𝑒 |¬𝑒 ′)                                                      star sliding
 =    (𝑒 ′𝑐 ′𝑒𝑐) ∗ ; (𝑒 ′𝑐 ′ ); (1 + (𝑒𝑐 |¬𝑒 ′)(𝑒𝑐 |¬𝑒 ′) ∗ ); (¬𝑒 |¬𝑒 ′)                                        star expand
 =    (𝑒 ′𝑐 ′𝑒𝑐) ∗ ; (𝑒 ′𝑐 ′ ); (¬𝑒 |¬𝑒 ′) + (𝑒 ′𝑐 ′𝑒𝑐) ∗ ; (𝑒 ′𝑐 ′ ); (𝑒𝑐 |¬𝑒 ′); (𝑒𝑐 |¬𝑒 ′) ∗ ; (¬𝑒 |¬𝑒 ′)     distrib
 ≤    (𝑒 ′𝑐 ′𝑒𝑐) ∗ ; (𝑒 ′𝑐 ′ ) ∗ ; (¬𝑒 |¬𝑒 ′) + (𝑒 ′𝑐 ′𝑒𝑐) ∗ ; (𝑒 ′𝑐 ′); (𝑒𝑐 |¬𝑒 ′); (𝑒𝑐 |¬𝑒 ′) ∗ ; (¬𝑒 |¬𝑒 ′)   using 𝑥 ≤ 𝑥 ∗
 =    (𝑒 ′𝑐 ′𝑒𝑐) ∗ ; (𝑒 ′𝑐 ′ ) ∗ ; (¬𝑒 |¬𝑒 ′) + (𝑒 ′𝑐 ′𝑒𝑐) ∗ ; (𝑒 ′𝑐 ′𝑒𝑐); ¬𝑒 ′; (𝑒𝑐 |¬𝑒 ′) ∗ ; (¬𝑒 |¬𝑒 ′)       emb def, assoc
 ≤    (𝑒 ′𝑐 ′𝑒𝑐) ∗ ; (𝑒 ′𝑐 ′ ) ∗ ; (¬𝑒 |¬𝑒 ′) + (𝑒 ′𝑐 ′𝑒𝑐) ∗ ; ¬𝑒 ′; (𝑒𝑐 |¬𝑒 ′) ∗ ; (¬𝑒 |¬𝑒 ′)                   𝑥 ∗ 𝑥 ≤ 𝑥 for 𝑥 := 𝑒 ′𝑐 ′𝑒𝑐
 =    (𝑒 ′𝑐 ′𝑒𝑐) ∗ ; (𝑒 ′𝑐 ′ ) ∗ ; (¬𝑒 |¬𝑒 ′) + (𝑒 ′𝑐 ′𝑒𝑐) ∗ ; (𝑒𝑐 |¬𝑒 ′) ∗ ; ¬𝑒 ′; (¬𝑒 |¬𝑒 ′)                   sliding, ¬𝑒 ′ comm. 𝑒𝑐
 =    (𝑒 ′𝑐 ′𝑒𝑐) ∗ ; (𝑒 ′𝑐 ′ ) ∗ ; (¬𝑒 |¬𝑒 ′) + (𝑒 ′𝑐 ′𝑒𝑐) ∗ ; (𝑒𝑐 |¬𝑒 ′) ∗ ; (¬𝑒 |¬𝑒 ′)                         tests idempotent
 =    (𝑒 ′𝑐 ′𝑒𝑐) ∗ ; ((𝑒 ′𝑐 ′) ∗ ; (¬𝑒 |¬𝑒 ′) + (𝑒𝑐 |¬𝑒 ′) ∗ ; (¬𝑒 |¬𝑒 ′))                                       distrib
 =    (𝑒𝑐𝑒 ′𝑐 ′ ) ∗ ; ((𝑒 ′𝑐 ′) ∗ ; (¬𝑒 |¬𝑒 ′) + (𝑒𝑐 |¬𝑒 ′) ∗ ; (¬𝑒 |¬𝑒 ′))                                      LRC: 𝑒𝑐𝑒 ′𝑐 ′ = 𝑒 ′𝑐 ′𝑒𝑐
 =    (𝑒𝑐𝑒 ′𝑐 ′ ) ∗ ; ((𝑒𝑐 |¬𝑒 ′) ∗ ; (¬𝑒 |¬𝑒 ′) + (𝑒 ′𝑐 ′ ) ∗ ; (¬𝑒 |¬𝑒 ′))                                     + commut
 =    (𝑒𝑐𝑒 ′𝑐 ′ ) ∗ ; ((𝑒𝑐 |¬𝑒 ′) ∗ ; (¬𝑒 |¬𝑒 ′) + (𝑒 ′𝑐 ′ ) ∗ ; ¬𝑒; (¬𝑒 |¬𝑒 ′))                                 tests idempotent
 ≤    (𝑒𝑐𝑒 ′𝑐 ′ ) ∗ ; ((𝑒𝑐 |¬𝑒 ′) ∗ ; (¬𝑒 |¬𝑒 ′) + (¬𝑒 |𝑒 ′𝑐 ′) ∗ ; (¬𝑒 |¬𝑒 ′))                                  Lemma 9.5
 =    (𝑒𝑐𝑒 ′𝑐 ′ ) ∗ ; ((𝑒𝑐 |¬𝑒 ′) ∗ + (¬𝑒 |𝑒 ′𝑐 ′ ) ∗ ); (¬𝑒 |¬𝑒 ′))                                             distrib
 =    (𝑒𝑐 |𝑒 ′𝑐 ′ ) ∗ ; ((𝑒𝑐 |¬𝑒 ′) ∗ + (¬𝑒 |𝑒 ′𝑐 ′ ) ∗ ); (¬𝑒 |¬𝑒 ′))                                           def

Theorem 4.4 (restated). It is undecidable whether a given identity holds in all ∗-continuous BiKATs.
  We present the undecidability argument from [Kozen and Smith 1996] adapted for BiKATs.

   Proof. Let 𝐼 be an instance of the Post Correspondence Problem (PCP) over some alphabet
{𝑝, 𝑞}. In other words let 𝐼 be 𝑘 pairs of strings 𝑥𝑖 , 𝑦𝑖 ∈ {𝑝, 𝑞}+ . We deﬁne two BiKAT expressions 𝑆
and 𝑇 over unary primitives {𝑝, 𝑞}. (So they will appear in the forms h𝑝], h𝑞], [𝑝i and [𝑞i, noting
that for any string 𝑠 = 𝑠 1 · · · 𝑠𝑛 over {𝑝, 𝑞}, the BiKAT axioms imply h𝑠] = h𝑠 1 ]; . . . ; h𝑠𝑛 ] and
[𝑠i = [𝑠 1 i; . . . ; [𝑠𝑛 i.)
   Let 𝑆 = (h𝑥 1 | 𝑦1 i + . . . + h𝑥𝑘 | 𝑦𝑘 i) ∗ . Let 𝑇 be
                                                                                                           
    (h𝑝 | 𝑝i + h𝑞 | 𝑞i) ∗ ; (h𝑝] + h𝑞]) + + ( [𝑝i + [𝑞i) + + (h𝑝 | 𝑞i + h𝑞 | 𝑝i); (h𝑝] + h𝑞] + [𝑝i + [𝑞i) ∗ .
We will show that the equation 𝑆 ≤ 𝑇 holds in all ∗-continuous BiKATs if and only if 𝐼 has no
solution.
   Suppose ﬁrst that 𝐼 has no solution, and let 𝛼 = 𝛼 1 · · · 𝛼𝑛 be any sequence from {1, . . . , 𝑘}𝑛 ,
which by assumption it cannot be a solution. Then h𝑥𝛼 1 · · · 𝑥𝛼𝑛 | 𝑦𝛼 1 · · · 𝑦𝛼𝑛 i is equivalent to an
element of the form h𝑧 | 𝑧ih𝑝 | 𝑞i𝑤 or h𝑧 | 𝑧ih𝑞 | 𝑝i𝑤 for 𝑤 an arbitrary element, or of the form
h𝑧 | 𝑧i𝑤 for 𝑤 a non-null element of only left embedded or only right embedded symbols. There
cannot be any other elements since 𝛼 is not a solution. By the axioms for BiKATs, all such elements
can be shown to be less than or equal to 𝑇 . For any ∗-continuous BiKAT, 𝑆 is the supremum of all
such elements of the form h𝑥𝛼 1 · · · 𝑥𝛼𝑛 | 𝑦𝛼 1 · · · 𝑦𝛼𝑛 i and therefore 𝑆 ≤ 𝑇 .
   For the other direction, suppose then that 𝛼 = 𝛼 1 · · · 𝛼𝑛 is a solution of 𝐼 , meaning that 𝑥𝛼 1 · · · 𝑥𝛼𝑛 =
𝑦𝛼 1 · · · 𝑦𝛼𝑛 . Denote these strings by 𝑧. It suﬃces to show there is a ∗-continuous BiKAT for which
the equation 𝑆 ≤ 𝑇 does not hold.
   First consider the KAT 𝐾 =      ˆ (℘({𝑝, 𝑞}∗ ), {∅, {𝜖}}, ∪, ·, ∗, ¬, {𝜖}, ∅), where · is the operation of
element-wise concatenation on two sets of strings, and ∗ is the iterated application of element-
wise concatenation. We can deﬁne an interpretation 𝐼 of KAT expressions over {𝑝, 𝑞} by letting
𝐼 (𝑝) = {𝑝 } (respectively 𝐼 (𝑞) = {𝑞}). We will deﬁne a BiKAT with actions being binary relations
on the set of strings {𝑝 𝐿 , 𝑞𝐿 }∗ ∪ {𝑝 𝑅 , 𝑞𝑅 }∗ where 0, 1, dot, sum and star are interpreted in the usual
way as in relation models.
   Given any element 𝑎 of 𝐾, let h𝑎] be deﬁned as the union of all 𝑓𝐿 (𝑥) for 𝑥 ∈ 𝑎, where 𝑓𝐿 is
deﬁned inductively as follows (where 𝜖 is the empty string):

                                      Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:38   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo




     𝑓𝐿 (𝜖) =    {(𝑥, 𝑥) | 𝑥 ∈ {𝑝 𝐿 , 𝑞𝐿 }∗ ∪ {𝑝 𝑅 , 𝑞𝑅 }∗ }
 𝑓𝐿 (𝑠 · 𝑢) =    𝑓𝐿 (𝑠); {(𝑥 𝐿 , 𝑥 𝐿𝑢𝐿 ) | 𝑥 𝐿 ∈ {𝑝 𝐿 , 𝑞𝐿 }∗ } ∪ {(𝑢𝑅 𝑥 𝑅 , 𝑥 𝑅 ) | 𝑥 𝑅 ∈ {𝑝 𝑅 , 𝑞𝑅 }∗ }   for 𝑢 ∈ {𝑝, 𝑞}.
The embedding [𝑎i is deﬁned analogously, but using the helper function 𝑓𝑅 :
     𝑓𝑅 (𝜖) =    {(𝑥, 𝑥) | 𝑥 ∈ {𝑝 𝐿 , 𝑞𝐿 }∗ ∪ {𝑝 𝑅 , 𝑞𝑅 }∗ }
 𝑓𝑅 (𝑠 · 𝑢) =    𝑓𝐿 (𝑠); {(𝑥 𝑅 , 𝑥 𝑅𝑢𝑅 ) | 𝑥 𝑅 ∈ {𝑝 𝑅 , 𝑞𝑅 }∗ } ∪ {(𝑢𝐿 𝑥 𝐿 , 𝑥 𝐿 ) | 𝑥 𝐿 ∈ {𝑝 𝐿 , 𝑞𝐿 }∗ }   for 𝑢 ∈ {𝑝, 𝑞}.
As a reminder, ; above is the usual relational composition. It is straightforward to show that the
left and right embeddings as deﬁned are KAT homomorphisms.

Claim 1: For any KAT expression 𝑒 over {𝑝, 𝑞} we have:
                𝐼 (h𝑒]) =     {(𝑥 𝐿 , 𝑥 𝐿𝑦𝐿 ) | 𝑥 𝐿 ∈ {𝑝 𝐿 , 𝑞𝐿 }∗ } ∪ {(𝑦𝑅 𝑥 𝑅 , 𝑥 𝑅 ) | 𝑥 𝑅 ∈ {𝑝 𝑅 , 𝑞𝑅 }∗ }
                𝐼 ( [𝑒i) =    {(𝑥 𝑅 , 𝑥 𝑅𝑦𝑅 ) | 𝑥 𝑅 ∈ {𝑝 𝑅 , 𝑞𝑅 }∗ } ∪ {(𝑦𝐿 𝑥 𝐿 , 𝑥 𝐿 ) | 𝑥 𝐿 ∈ {𝑝 𝐿 , 𝑞𝐿 }∗ }.
where 𝑦𝐿 is the “left” version of some 𝑦 in 𝐼 (𝑒) and 𝑦𝑅 is the “right” version of some 𝑦 in 𝐼 (𝑒).

Claim 2: For any KAT expression 𝑒 over {𝑝, 𝑞} we have:
                    𝐼 (h𝑒]) ∪ 𝐼 ( [𝑒i) ⊆ ({𝑝 𝐿 , 𝑞𝐿 }∗ × {𝑝 𝐿 , 𝑞𝐿 }∗ ) ∪ ({𝑝 𝑅 , 𝑞𝑅 }∗ × {𝑝 𝑅 , 𝑞𝑅 }∗ )

   To show that the BiKAT is well-deﬁned it remains to show LRC, and in particular that h𝑤 | 𝑣i =
h𝑣 | 𝑤i, where 𝑤 and 𝑣 are arbitrary elements from the KAT 𝐾 (and we omit writing 𝐼 ). Let (𝑥 1, 𝑥 2 )
be in h𝑤 | 𝑣i and recall h𝑤 | 𝑣i = h𝑤]; [𝑣i by deﬁnition. Then there is 𝑥 such that (𝑥 1, 𝑥) ∈ h𝑤]
and (𝑥, 𝑥 2 ) ∈ [𝑣i. Then, by Claim 1 and properties of relational composition, either 𝑥 1, 𝑥 2 and
𝑥 are all “left” strings in {𝑝 𝐿 , 𝑞𝐿 }∗ , or they are all “right” strings in {𝑝 𝑅 , 𝑞𝑅 }∗ . Without loss of
generality, suppose they are both “left” strings. But then, by Claim 1, the strings have to be of the
form 𝑥 1 = 𝑎𝐿 · 𝑠𝐿 , 𝑥 = 𝑎𝐿 · 𝑠𝐿 · 𝑏 𝐿 and 𝑥 2 = 𝑠𝐿 · 𝑏 𝐿 . It remains to show that (𝑥 1, 𝑥 2 ) ∈ [𝑣i; h𝑤]. It
suﬃces to show (𝑥 1, 𝑠𝐿 ) ∈ [𝑣i and (𝑠𝐿 , 𝑥 2 ) ∈ [𝑤i, which follows from Claim 1.
   Let the BiKAT also contain the bitest 𝐸, interpreted as the identity relation on the empty string
𝜖. It can be shown that 𝐸; h𝑝 | 𝑝i = 𝐸; h𝑞 | 𝑞i = 𝐸, which implies that 𝐸; (h𝑝 | 𝑝i + h𝑞 | 𝑞i) ∗ = 𝐸,
and 𝐸; h𝑧 | 𝑧i; 𝐸 = 𝐸. Since h𝑧 | 𝑧i = h𝑥𝛼 1 · · · 𝑥𝛼𝑛 | 𝑦𝛼 1 · · · 𝑦𝛼𝑛 i ≤ 𝑆 it follows that 𝐸 ≤ 𝐸; 𝑆; 𝐸 and
therefore 𝐸; 𝑆; 𝐸 ≠ 0.
   It also follows that 𝐸; h𝑝 | 𝑞i = 𝐸; h𝑞 | 𝑝i = 0 and 𝐸; (h𝑝] + h𝑞]) + ; 𝐸 = 𝐸; ( [𝑝i + [𝑞i) + ; 𝐸 = 0.
Therefore
         𝐸;𝑇 ; 𝐸
    =    𝐸; (h𝑝 | 𝑝i + h𝑞 | 𝑞i) ∗ ; ((h𝑝] + h𝑞]) + + ([𝑝i + [𝑞i) + + (h𝑝 | 𝑞i + h𝑞 | 𝑝i); (h𝑝] + h𝑞] + [𝑝i + [𝑞i) ∗ ); 𝐸
    =    𝐸; ((h𝑝] + h𝑞]) + + ([𝑝i + [𝑞i) + + (h𝑝 | 𝑞i + h𝑞 | 𝑝i); (h𝑝] + h𝑞] + [𝑝i + h𝑞 | )i ∗ )
    =    𝐸; (h𝑝] + h𝑞]) + ; 𝐸 + 𝐸; ([𝑝i + [𝑞i) + ; 𝐸 + 𝐸; (h𝑝 | 𝑞i + h𝑞 | 𝑝i); (h𝑝] + h𝑞] + [𝑝i + [𝑞i) ∗ ; 𝐸
    =    0
Since 𝐸; 𝑆; 𝐸 ≠ 0 and 𝐸;𝑇 ; 𝐸 = 0, it cannot be the case that 𝑆 ≤ 𝑇 .                                                      

9.3 Details for Sect. 5
Following on from the discussion in Sect. 5 of Example 2.3 from Sect. 2: In Fig. 4, we show the
proof of the invariant I¥ over the BiKAT alignment of the two inner loops. After using the BiKAT
expansion law (3) to lockstep align the loop bodies and deriving sub-proofs over these alignments,
we can easily prove the validity of the sub-proofs. Similarly, we align the two outer loops and
prove their invariant J¥ .

Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                            20:39


        ¥ h([x<N*M];[x%M!=0];𝑏 1 ) ∗ ;[x<N*M];[x%M!=0] | ([j<M];𝑏 2 ) ∗ ;[j<M]i;¬ I¥ = 0
       I;
 ⇐      ¥ h[x<N*M];[x%M!=0];𝑏 1 | [j<M];𝑏 2 i ∗ ;( h[x<N*M];[x%M!=0];𝑏 1 | [j<M]i ∗ + h[x<N*M];[x%M!=0] | [j<M]; 𝑏 2 i ∗ );
       I;
            h[x<N*M];[x%M!=0] | [j<M]i;¬ I¥ = 0
       
          I; h[x<N*M];[x%M!=0];𝑏 1 | [j<M];𝑏 2 i;¬ I¥ = 0 ∧ I;
          ¥                                                  ¥ h[x<N*M];[x%M!=0];𝑏 1 | [j<M]i;¬ I¥ = 0 ∧
 ⇐        ¥ h[x<N*M];[x%M!=0] | [j<M];𝑏 2 i;¬ I¥ = 0 ∧ I;¥ h[x<N*M];[x%M!=0] | [j<M]i;¬ I¥ = 0
          I;
                               Fig. 4. BiKAT reasoning for the loop tiling example


                              𝑐 | 𝑐 ′ : 𝑃 ∧ h𝑒] ∧ [𝑒 ′ i ≈> 𝑄       𝑑 | 𝑑 ′ : 𝑃 ∧ ¬h𝑒] ∧ ¬[𝑒 ′ i ≈> 𝑄
                              𝑐 | 𝑑 ′ : 𝑃 ∧ h𝑒] ∧ ¬[𝑒 ′ i ≈> 𝑄        𝑑 | 𝑐 ′ : 𝑃 ∧ ¬h𝑒] ∧ [𝑒 ′ i ≈> 𝑄
                       dIf4
                                       if 𝑒 then 𝑐 else 𝑑 | if 𝑒 ′ then 𝑐 ′ else 𝑑 ′ : 𝑃 ≈> 𝑄

                   dSkip                                  AssSkip
                   skip | skip : 𝑃 ≈> 𝑃                  𝑣 := 𝑒 | skip : 𝑃𝑒𝑣|| ≈> 𝑃

                                 𝑐 | skip : 𝑃 ∧ h𝑒] ≈> 𝑄         𝑑 | skip : 𝑃 ∧ h¬𝑒] ≈> 𝑄
                        IfSkip
                                            if 𝑒 then 𝑐 else 𝑑 | skip : 𝑃 ≈> 𝑄

                𝑐 | skip : 𝑃 ∧ h𝑒] ≈> 𝑃                                  𝑐 | 𝑑 : 𝑃 ≈> 𝑄         𝑐 | 𝑑 : 𝑃 ≈> 𝑅
WhSk                                                             rConj
        while 𝑒 do 𝑐 | skip : 𝑃 ≈> 𝑃 ∧ h¬𝑒]                                    𝑐 | 𝑑 : 𝑃 ≈> 𝑄 ∧ 𝑅

                                     falsePre
                                     𝑐 | 𝑐 ′ : 𝐹𝑎𝑙𝑠𝑒 ≈> 𝑃

                                          Fig. 5. Some additional ∀∀ rules


9.4 Details for Sect. 6
9.4.1 Proof of Theorem 6.1. In this section we prove some of the ∀∀ RHL rules (see Fig. 1). Fig. 5
gives some additional RHL rules that are also provable in any BiKAT.

      For dSkip: the judgment skip | skip : 𝑃 ≈> 𝑃 is encoded as 𝑃; h1 | 1i = 𝑃; h1 | 1i; 𝑃 which holds
because h1 | 1i = 1¥ by the homomorphism property of the embeddings. Strictly: h1 | 1i = h1]; [1i =
1¥ ; 1¥ = 1¥ .

  For rConseq: 𝑐 | 𝑑 : 𝑃 ≈> 𝑄 is encoded as 𝑃; h𝑐 | 𝑑i ≤ 𝑃; h𝑐 | 𝑑i; 𝑄 and the implications as 𝑅 ≤ 𝑃
and 𝑄 ≤ 𝑆. These immediately yield 𝑅; h𝑐 | 𝑑i ≤ 𝑅; h𝑐 | 𝑑i; 𝑆 by transitivity.

  For rDisj: The premises 𝑐 | 𝑑 : 𝑃 ≈> 𝑄 and 𝑐 | 𝑑 : 𝑅 ≈> 𝑄 are encoded as 𝑃; h𝑐 | 𝑑i ≤ 𝑃; h𝑐 | 𝑑i; 𝑄
and 𝑅; h𝑐 | 𝑑i ≤ 𝑅; h𝑐 | 𝑑i; 𝑄. The conclusion 𝑐 | 𝑑 : 𝑃 ∨ 𝑅 ≈> 𝑄 is encoded as (𝑃 + 𝑅); h𝑐 | 𝑑i ≤
(𝑃 + 𝑅); h𝑐 | 𝑑i; 𝑄, and it is proved by
                                        (𝑃 + 𝑅); h𝑐 | 𝑑i
                                   =    𝑃; h𝑐 | 𝑑i + 𝑅; h𝑐 | 𝑑i          distrib
                                   ≤    𝑃; h𝑐 | 𝑑i; 𝑄 + 𝑅; h𝑐 | 𝑑i; 𝑄    premises
                                   =    (𝑃 + 𝑅); h𝑐 | 𝑑i; 𝑄              distrib
Note that the proof is independent of the form of h𝑐 | 𝑑i. The reasoning embodied by this rule is
sound for any BiKAT term.

                                 Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:40   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


  For rConj: The premises 𝑐 | 𝑑 : 𝑃 ≈> 𝑄 and 𝑐 | 𝑑 : 𝑃 ≈> 𝑅 are encoded as 𝑃; h𝑐 | 𝑑i ≤ 𝑃; h𝑐 | 𝑑i; 𝑄
and 𝑃; h𝑐 | 𝑑i ≤ 𝑃; h𝑐 | 𝑑i; 𝑅. The conclusion 𝑐 |𝑑 : 𝑃 ≈> 𝑄 ∧𝑅 is encoded as 𝑃; h𝑐 | 𝑑i ≤ 𝑃; h𝑐 | 𝑑i; 𝑄; 𝑅,
and it is proved by 𝑃; h𝑐 | 𝑑i ≤ 𝑃; h𝑐 | 𝑑i; 𝑅 ≤ 𝑃; h𝑐 | 𝑑i; 𝑄; 𝑅 using the second premise and then the
ﬁrst.
  As in the case of rDisj, the proof is independent of the form of h𝑐 | 𝑑i. The reasoning embodied
by this rule is sound for any BiKAT term.

   For dSeq:
                                     𝑃; h𝑐; 𝑑 | 𝑐 ′ ; 𝑑 ′i
                               =     𝑃; h𝑐 | 𝑐 ′ i; h𝑑 | 𝑑 ′ i         embed homo, i.e., LRC
                               ≤     𝑃; h𝑐 | 𝑐 ′ i; 𝑅; h𝑑 | 𝑑 ′ i      premise
                               ≤     𝑃; h𝑐 | 𝑐 ′ i; 𝑅; h𝑑 | 𝑑 ′ i; 𝑄   premise
                               ≤     𝑃; h𝑐 | 𝑐 ′ i; h𝑑 | 𝑑 ′ i; 𝑄      test 𝑅 ≤ 1
                               =     𝑃; h𝑐; 𝑑 | 𝑐 ′ ; 𝑑 ′i; 𝑄          emb homo
The premises are used in the form 𝑃; h𝑐 | 𝑐 ′ i ≤ 𝑃; h𝑐 | 𝑐 ′ i; 𝑅 and 𝑅; h𝑑 | 𝑑 ′i ≤ 𝑅; h𝑑 | 𝑑 ′i; 𝑄 and those
steps use monotonicity of sequence.

   For SeqSk, suppose 𝑃; h𝑐 | 1i ≤ 𝑃; h𝑐 | 1i; 𝑅 and 𝑅; h𝑑 | 1i ≤ 𝑅; h𝑑 | 1i; 𝑄. Then 𝑃; h𝑐; 𝑑 | 1i =
𝑃; h𝑐 | 1i; h𝑑 | 1i ≤ 𝑃; h𝑐 | 1i; 𝑅; h𝑑 | 1i ≤ 𝑃; h𝑐 | 1i; 𝑅; h𝑑 | 1i; 𝑄 ≤ 𝑃; h𝑐 | 1i; h𝑑 | 1i; 𝑄 using homo-
morphism, the premises, and test below 1.

   For WhSkip, the premise has the form 𝑃; h𝑒]; h𝑐 | 1i ≤ 𝑃; h𝑒]; h𝑐 | 1i; 𝑃 which can be rewritten
to 𝑃; h𝑒; 𝑐] ≤ 𝑃; h𝑒; 𝑐]; 𝑃. The conclusion follows by
                                   𝑃; h(𝑒; 𝑐) ∗ ; ¬𝑒 | 1i
                           =       𝑃; h𝑒; 𝑐] ∗ ; ¬h𝑒]                   emb def and homo
                           ≤       𝑃; h𝑒; 𝑐] ∗ ; 𝑃; ¬h𝑒]                premise, invariance lem
                           =       𝑃; h(𝑒; 𝑐) ∗ ; ¬𝑒 | 1i; 𝑃; ¬h𝑒]      emb def and homo
9.4.2    Proof of Theorem 6.2.
    Proof of Expansion Law (7). We prove that in any *-continuous model, the following holds, where
𝑒, 𝑒 ′ are tests in the underlying model and 𝑄, 𝑅 are bitests.
     h𝑒; 𝑐] ∗ ; h¬𝑒]; [𝑒 ′ ; 𝑐 ′ i ∗ ; [¬𝑒 ′ i = 𝑑 ∗ ; h¬𝑒 | ¬𝑒 ′ i
                                                                                                                       (15)
      where 𝑑 = 𝑄; h𝑒; 𝑐] + 𝑅; [𝑒 ′ ; 𝑐 ′ i + ¬𝑄¬𝑅; h𝑒; 𝑐 | 𝑒 ′ ; 𝑐 ′ i + ¬𝑄; h𝑒; 𝑐 | ¬𝑒 ′ i + ¬𝑅; h¬𝑒 | 𝑒 ′ ; 𝑐 ′ i
Note that (15) is the same as (7); it is re-stated here for convenience and to deﬁne abbreviation 𝑑
for the right side loop body. The proof is by mutual inclusion.
  One direction holds in any biKAT, namely 𝑑 ∗ h¬𝑒 | ¬𝑒 ′ i ≤ h𝑒𝑐] ∗ h¬𝑒] [𝑒 ′𝑐 ′ i ∗ [¬𝑒 ′ i. (We omit semi-
colon to save space.) In its proof we use that tests are below 1, and in particular the consequence
that h𝑒𝑐 | ¬𝑒 ′ i ≤ h𝑒𝑐] and h¬𝑒 | 𝑒 ′𝑐 ′ i ≤ [𝑒 ′𝑐 ′ i.
        (𝑄 h𝑒𝑐] + 𝑅 [𝑒 ′𝑐 ′ i + ¬𝑄¬𝑅h𝑒𝑐 | 𝑒 ′𝑐 ′ i + ¬𝑄 h𝑒𝑐 | ¬𝑒 ′ i + ¬𝑅h¬𝑒 | 𝑒 ′𝑐 ′ i) ∗ h¬𝑒 | ¬𝑒 ′ i
 ≤      (h𝑒𝑐] + [𝑒 ′𝑐 ′ i + h𝑒𝑐 | 𝑒 ′𝑐 ′ i + h𝑒𝑐 | ¬𝑒 ′ i + h¬𝑒 | 𝑒 ′𝑐 ′ i) ∗ h¬𝑒 | ¬𝑒 ′ i
 =      (h𝑒𝑐] + [𝑒 ′𝑐 ′ i + h𝑒𝑐 | 𝑒 ′𝑐 ′ i) ∗ h¬𝑒 | ¬𝑒 ′ i
 =      h𝑒𝑐] ∗ [𝑒 ′𝑐 ′ i ∗ h¬𝑒 | ¬𝑒 ′ i                                                                    Lemma 9.12
To prove the reverse inclusion, h𝑒𝑐] ∗ h¬𝑒] [𝑒 ′𝑐 ′ i ∗ [¬𝑒 ′ i ≤ 𝑑 ∗ h¬𝑒 | ¬𝑒 ′ i, we ﬁrst commute h¬𝑒] with
[𝑒 ′𝑐 ′ i ∗ (by LRC and Lemma 9.7), to get the equivalent inequality
                                          h𝑒𝑐] ∗ [𝑒 ′𝑐 ′ i ∗ h¬𝑒 | ¬𝑒 ′ i ≤ 𝑑 ∗ h¬𝑒 | ¬𝑒 ′ i

Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                           20:41


Now rewrite the left side using *-continuity:

                          (𝑠𝑢𝑝 : 𝑛, 𝑚 ∈ N : h𝑒𝑐] 𝑛 [𝑒 ′𝑐 ′ i𝑚 h¬𝑒 | ¬𝑒 ′ i) ≤ 𝑑 ∗ h¬𝑒 | ¬𝑒 ′ i

By the sup property this is equivalent to

                              ∀𝑛, 𝑚 ∈ N. h𝑒𝑐] 𝑛 [𝑒 ′𝑐 ′ i𝑚 h¬𝑒 | ¬𝑒 ′ i ≤ 𝑑 ∗ h¬𝑒 | ¬𝑒 ′ i

We prove this by induction on 𝑛 + 𝑚.
  For the base case, 𝑛 = 0 = 𝑚, we have h𝑒𝑐] 0 [𝑒 ′𝑐 ′ i 0 h¬𝑒 | ¬𝑒 ′ i = h¬𝑒 | ¬𝑒 ′ i ≤ 𝑑 ∗ h¬𝑒 | ¬𝑒 ′ i using
the deﬁnition of iterate 0 as 1, and 1 ≤ 𝑑 ∗ .
  For the induction step we consider separately the cases where 𝑛 or 𝑚 is zero.
Case 𝑛 > 0 and 𝑚 = 0:

      h𝑒𝑐] 𝑛 [𝑒 ′𝑐 ′ i 0 h¬𝑒 | ¬𝑒 ′ i
    = h𝑒𝑐] h𝑒𝑐] 𝑛−1 h¬𝑒 | ¬𝑒 ′ i                                         def iterate
    = 𝑄 h𝑒𝑐] h𝑒𝑐] 𝑛−1 h¬𝑒 | ¬𝑒 ′ i + 𝑄 h𝑒𝑐] h𝑒𝑐] 𝑛−1 h¬𝑒 | ¬𝑒 ′ i        KAT
    = 𝑄 h𝑒𝑐] h𝑒𝑐] 𝑛−1 h¬𝑒 | ¬𝑒 ′ i + 𝑄 h𝑒𝑐 | ¬𝑒 ′ ih𝑒𝑐] 𝑛−1 h¬𝑒 | ¬𝑒 ′ i [¬𝑒 ′ i idempotent, LRC
    ≤ 𝑄 h𝑒𝑐]𝑑 ∗ h¬𝑒 | ¬𝑒 ′ i + 𝑄 h𝑒𝑐 | ¬𝑒 ′ i𝑑 ∗ h¬𝑒 | ¬𝑒 ′ i            induction, twice
    ≤ 𝑑𝑑 ∗ h¬𝑒 | ¬𝑒 ′ i + 𝑑𝑑 ∗ h¬𝑒 | ¬𝑒 ′ i                               𝑄 h𝑒𝑐] ≤ 𝑑 and 𝑄 h𝑒𝑐 | ¬𝑒 ′ i ≤ 𝑑
       ∗             ′      ∗
    ≤ 𝑑 h¬𝑒 | ¬𝑒 i + 𝑑 h¬𝑒 | ¬𝑒 i     ′                                  𝑑𝑑 ∗ ≤ 𝑑 ∗

Case 𝑛 = 0 and 𝑚 > 0: Symmetric with the preceding case 𝑛 > 0 and 𝑚 = 0, using 𝑅 [𝑒 ′𝑐 ′ i ≤ 𝑑
      and 𝑅h¬𝑒 | 𝑒 ′𝑐 ′ i ≤ 𝑑.
Case 𝑛 > 0 and 𝑚 > 0: By distributivity and boolean algebra, we rewrite h𝑒𝑐] 𝑛 [𝑒 ′𝑐 ′ i𝑚 h¬𝑒 | ¬𝑒 ′ i to
      the sum
                                     𝑄 𝑅h𝑒𝑐] 𝑛 [𝑒 ′𝑐 ′ i𝑚 h¬𝑒 | ¬𝑒 ′ i
                                 + 𝑄𝑅h𝑒𝑐] 𝑛 [𝑒 ′𝑐 ′ i𝑚 h¬𝑒 | ¬𝑒 ′ i
                                 + 𝑄𝑅h𝑒𝑐] 𝑛 [𝑒 ′𝑐 ′ i𝑚 h¬𝑒 | ¬𝑒 ′ i
                                 + 𝑄𝑅h𝑒𝑐] 𝑛 [𝑒 ′𝑐 ′ i𝑚 h¬𝑒 | ¬𝑒 ′ i
       We show each term of the sum is below 𝑑 ∗ h¬𝑒 | ¬𝑒 ′ i.
       •
                     𝑄 𝑅h𝑒𝑐] 𝑛 [𝑒 ′𝑐 ′ i𝑚 h¬𝑒 | ¬𝑒 ′ i
                = 𝑄 𝑅h𝑒𝑐 | 𝑒 ′𝑐 ′ ih𝑒𝑐] 𝑛−1 [𝑒 ′𝑐 ′ i𝑚−1 h¬𝑒 | ¬𝑒 ′ i def iterate, LRC
                ≤ 𝑄 𝑅h𝑒𝑐 | 𝑒 ′𝑐 ′ i𝑑 ∗ h¬𝑒 | ¬𝑒 ′ i                   induction
                ≤ 𝑑𝑑 ∗ h¬𝑒 | ¬𝑒 ′ i                                   𝑄 𝑅h𝑒𝑐 | 𝑒 ′𝑐 ′ i ≤ 𝑑
                ≤ 𝑑 ∗ h¬𝑒 | ¬𝑒 ′ i                                    𝑑𝑑 ∗ ≤ 𝑑 ∗
       •
                               𝑄𝑅h𝑒𝑐] 𝑛 [𝑒 ′𝑐 ′ i𝑚 h¬𝑒 | ¬𝑒 ′ i
                          =    𝑄𝑅h𝑒𝑐] h𝑒𝑐] 𝑛−1 [𝑒 ′𝑐 ′ i𝑚 h¬𝑒 | ¬𝑒 ′ i def iterate, LRC
                          ≤    𝑄𝑅h𝑒𝑐]𝑑 ∗ h¬𝑒 | ¬𝑒 ′ i                  induction
                          ≤    𝑄 h𝑒𝑐]𝑑 ∗ h¬𝑒 | ¬𝑒 ′ i                  test 𝑅 ≤ 1
                          ≤    𝑑𝑑 ∗ h¬𝑒 | ¬𝑒 ′ i                       𝑄 h𝑒𝑐] ≤ 𝑑
                          ≤    𝑑 ∗ h¬𝑒 | ¬𝑒 ′ i                        𝑑𝑑 ∗ ≤ 𝑑 ∗

       • The argument for 𝑄𝑅h𝑒𝑐] 𝑛 [𝑒 ′𝑐 ′ i𝑚 h¬𝑒 | ¬𝑒 ′ i is symmetric with the preceding bullet, using
         that 𝑅 [𝑒 ′𝑐 ′ i ≤ 𝑑

                                Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:42   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


        •
                                 𝑄𝑅h𝑒𝑐] 𝑛 [𝑒 ′𝑐 ′ i𝑚 h¬𝑒 | ¬𝑒 ′ i
                           =     𝑄𝑅h𝑒𝑐] h𝑒𝑐] 𝑛−1 [𝑒 ′𝑐 ′ i𝑚 h¬𝑒 | ¬𝑒 ′ i def iterate, LRC
                           ≤     𝑄𝑅h𝑒𝑐]𝑑 ∗ h¬𝑒 | ¬𝑒 ′ i                  induction
                           ≤     𝑄 h𝑒𝑐]𝑑 ∗ h¬𝑒 | ¬𝑒 ′ i                  test 𝑅 ≤ 1
                           ≤     𝑑𝑑 ∗ h¬𝑒 | ¬𝑒 ′ i                       𝑄 h𝑒𝑐] ≤ 𝑑
                           ≤     𝑑 ∗ h¬𝑒 | ¬𝑒 ′ i                        𝑑𝑑 ∗ ≤ 𝑑 ∗
            For this case there is an alternate proof using using 𝑅 [𝑒 ′𝑐 ′ i ≤ 𝑑 instead of 𝑄 h𝑒𝑐] ≤ 𝑑.


   Proof of Rule caWh. By calculation, we show that caWh is sound in any BiKAT that satisﬁes
(15).
   The premises of rule caWh are:
                      𝑃; h𝑒]; [𝑒 ′ i; ¬𝑄; ¬𝑅; h𝑐 | 𝑐 ′ i      ≤   𝑃; h𝑒]; [𝑒 ′ i; ¬𝑄; ¬𝑅; h𝑐 | 𝑐 ′ i; 𝑃
                                        𝑃; 𝑄; h𝑒]; h𝑐]        ≤   𝑃; 𝑄; h𝑒]; h𝑐]; 𝑃
                                       𝑃; 𝑅; [𝑒 ′ i; [𝑐 ′ i   ≤   𝑃; 𝑅; [𝑒 ′ i; [𝑐 ′ i; 𝑃
                            ¥ ′ + 𝑄; h𝑒] + 𝑅; [𝑒 ′ i, which implies
The side condition is 𝑃 ≤ 𝑒 =𝑒
                               𝑃; ¬𝑄; h𝑒]; ¬[𝑒 ′ i = 0        and 𝑃; ¬𝑅; ¬h𝑒]; [𝑒 ′ i = 0                            (16)
Observe that the premises imply 𝑃 is preserved by the loop body:
                𝑃 (𝑄 h𝑒𝑐] + 𝑅 [𝑒 ′𝑐 ′ i + ¬𝑄¬𝑅h𝑒𝑐 | 𝑒 ′𝑐 ′ i + ¬𝑄 h𝑒𝑐 | ¬𝑒 ′ i + ¬𝑅h¬𝑒 | 𝑒 ′𝑐 ′ i)
            =      distrib
                𝑃𝑄 h𝑒𝑐] + 𝑃𝑅 [𝑒 ′𝑐 ′ i + 𝑃¬𝑄¬𝑅h𝑒𝑐 | 𝑒 ′𝑐 ′ i + 𝑃¬𝑄 h𝑒𝑐 | ¬𝑒 ′ i + 𝑃¬𝑅h¬𝑒 | 𝑒 ′𝑐 ′ i
            =      side condition (16)
                𝑃𝑄 h𝑒𝑐] + 𝑃𝑅 [𝑒 ′𝑐 ′ i + 𝑃¬𝑄¬𝑅h𝑒𝑐 | 𝑒 ′𝑐 ′ i
            ≤      premises, emb homo
                𝑃𝑄 h𝑒𝑐]𝑃 + 𝑃𝑅 [𝑒 ′𝑐 ′ i𝑃 + 𝑃¬𝑄¬𝑅h𝑒𝑐 | 𝑒 ′𝑐 ′ i𝑃
            =      side condition (16)
                𝑃𝑄 h𝑒𝑐]𝑃 + 𝑃𝑅 [𝑒 ′𝑐 ′ i𝑃 + 𝑃¬𝑄¬𝑅h𝑒𝑐 | 𝑒 ′𝑐 ′ i𝑃 + 𝑃¬𝑄 h𝑒𝑐 | ¬𝑒 ′ i𝑃 + 𝑃¬𝑅h¬𝑒 | 𝑒 ′𝑐 ′ i𝑃
            =      distrib
                𝑃 (𝑄 h𝑒𝑐] + 𝑅 [𝑒 ′𝑐 ′ i + ¬𝑄¬𝑅h𝑒𝑐 | 𝑒 ′𝑐 ′ i + ¬𝑄 h𝑒𝑐 | ¬𝑒 ′ i + ¬𝑅h¬𝑒 | 𝑒 ′𝑐 ′ i)𝑃
The conclusion of caWh follows by
        𝑃 h𝑒𝑐] ∗ h¬𝑒] [𝑒 ′𝑐 ′ i ∗ [¬𝑒 ′ i
  =        by (15)
        𝑃 (𝑄 h𝑒𝑐] + 𝑅 [𝑒 ′𝑐 ′ i + ¬𝑄¬𝑅h𝑒𝑐 | 𝑒 ′𝑐 ′ i + ¬𝑄 h𝑒𝑐 | ¬𝑒 ′ i + ¬𝑅h¬𝑒 | 𝑒 ′𝑐 ′ i) ∗ h¬𝑒 | ¬𝑒 ′ i
   ≤       invariance, observation above
        𝑃 (𝑄 h𝑒𝑐] + 𝑅 [𝑒 ′𝑐 ′ i + ¬𝑄¬𝑅h𝑒𝑐 | 𝑒 ′𝑐 ′ i + ¬𝑄 h𝑒𝑐 | ¬𝑒 ′ i + ¬𝑅h¬𝑒 | 𝑒 ′𝑐 ′ i) ∗ 𝑃 h¬𝑒 | ¬𝑒 ′ i
  =        tests idem, tests commute
        𝑃 (𝑄 h𝑒𝑐] + 𝑅 [𝑒 ′𝑐 ′ i + ¬𝑄¬𝑅h𝑒𝑐 | 𝑒 ′𝑐 ′ i + ¬𝑄 h𝑒𝑐 | ¬𝑒 ′ i + ¬𝑅h¬𝑒 | 𝑒 ′𝑐 ′ i) ∗ h¬𝑒 | ¬𝑒 ′ i𝑃 h¬𝑒 | ¬𝑒 ′ i
  =        by (15)
        𝑃 (h𝑒𝑐] ∗ h¬𝑒] [𝑒 ′𝑐 ′ i ∗ [¬𝑒 ′ i)𝑃 h¬𝑒 | ¬𝑒 ′ i

9.5     Details for Sect. 7
9.5.1    Details for Sect. 7.2.

Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                            20:43


                                         𝑅;𝑊1 ≤ 𝑅;𝑊1 ; 𝑆           𝑅;𝑊2 ≤ 𝑅;𝑊2 ; 𝑆
                               DisjWC
                                             𝑅; (𝑊1 + 𝑊2 ) ≤ 𝑅; (𝑊1 + 𝑊2 ); 𝑆

                              𝑅;𝑊1 ≤ hhav | 𝑑 1 i          𝑅;𝑊2 ≤ hhav | 𝑑 2 i
                    DisjWU
                                     𝑅; (𝑊1 + 𝑊2 ) ≤ hhav | 𝑑 1 + 𝑑 2 i

                                     𝑅; h𝑐 1 ] ≤ 𝑊1 ; [havi        𝑅; h𝑐 2 ] ≤ 𝑊2 ; [havi
                           DisjWO
                                         𝑅; h𝑐 1 + 𝑐 2 ] ≤ (𝑊1 + 𝑊2 ); [havi

                Fig. 6. Disjunction lemmas for use with forward simulation witness technique



                                                                                    ∃
   Proof of Theorem 7.3, Backward Simulation Case. Suppose 𝑐 | 𝑑 : 𝑅 ≈> 𝑆 holds. Let witness 𝑊 be
¤ h𝑐 | 𝑑i; 𝑆.
𝑅;         ¤ We show it satisﬁes the conditions to be b-valid.

    • We have (WCb) because 𝑊 ; 𝑆¤ = 𝑅;𝑊  ¤ ; 𝑆¤ by deﬁnition of 𝑊 and idempotence of the bitest 𝑅.        ¤
                                     ¤                            ′      ¤
    • To show (WOb), i.e., h𝑐]; 𝑆 ≤ [havi;𝑊 , suppose (𝜎, 𝜎 )h𝑐]; 𝑆 (𝜏, 𝜏 ). Then 𝜎𝑐𝜏 and 𝜎 = 𝜏 ′
                                                                                 ′                   ′
                                       ∃
      and 𝜏𝑆𝜏 ′. Now by 𝑐 | 𝑑 : 𝑅 ≈> 𝑆 there is 𝜎 ′′ with 𝜎 ′′𝑑𝜏 ′ and 𝜎𝑅𝜎 ′′ . So (𝜎, 𝜎 ′′ )𝑊 (𝜏, 𝜏 ′ ) and
                  ′
      thus (𝜎, 𝜎 ) [havi;𝑊 (𝜏, 𝜏 ).′

    • To show (WUb), i.e., 𝑊 ; 𝑆¤ ≤ hhav | 𝑑i, suppose (𝜎, 𝜎 ′ )𝑊 ; 𝑆¤(𝜏, 𝜏 ′ ). Then by deﬁnitions 𝜎𝑅𝜎 ′ ,
      𝜎𝑐𝜏, 𝜎 ′𝑑𝜏 ′, and 𝜏𝑆𝜏 ′. Since 𝜎hav𝜏, we have (𝜎, 𝜎 ′ )hhav | 𝑑i(𝜏, 𝜏 ′).
This concludes the proof.
   Apropos Footnote 8, if the model is full then it contains elements that satisfy the b-validity con-
ditions and are in some sense minimal (whereas the expressible witness 𝑅;            ¤ h𝑐 | 𝑑i; 𝑆¤ used above is in
                                                             ∃
some sense maximal). To elaborate, suppose 𝑐 | 𝑑 : 𝑅 ≈> 𝑆 holds. Deﬁne the predicate P (𝜎, 𝜏, 𝜏 ′) =                  ˆ
𝜎𝑐𝜏𝑆𝜏 ′ and the set X(𝜎, 𝜏, 𝜏 ′) =
                                 ˆ {𝜎 ′ | 𝜎𝑅𝜎 ′𝑑𝜏 ′ }. For any (𝜎, 𝜏, 𝜏 ′ ) that satisfy P we have X(𝜎, 𝜏, 𝜏 ′)
                                 ∃
nonempty, owing to 𝑐 |𝑑 : 𝑅 ≈> 𝑆. So deﬁne Y (𝜎, 𝜏, 𝜏 ′) to be a chosen element of X(𝜎, 𝜏, 𝜏 ′) if
P (𝜎, 𝜏, 𝜏 ′ ), and undeﬁned otherwise. Deﬁne 𝑊 =      ˆ {((𝜎, 𝜎 ′ ), (𝜏, 𝜏 ′)) | P (𝜎, 𝜏, 𝜏 ′) ∧ 𝜎 ′ = Y (𝜎, 𝜏, 𝜏 ′ )}.
By fullness, 𝑊 is in the BiKAT. For b-validity we have (WCb) because 𝑊 = 𝑅;𝑊                ¤ ; 𝑆, ¤
                                      ¤
   For (WOb), suppose (𝜎, 𝜎 )h𝑐]; 𝑆 (𝜏, 𝜏 ). Then 𝜎𝑐𝜏 and 𝜎 = 𝜏 and 𝜏𝑆𝜏 . So P (𝜎, 𝜏, 𝜏 ′) so there’s
                               ′             ′                      ′      ′          ′

𝜌 with 𝜎𝑅𝜌𝑑𝜏 ′ and (𝜎, 𝜌)𝑊 (𝜏, 𝜏 ′) Since 𝜎 ′ hav𝜌 we have (𝜎, 𝜎 ′ ) [havi(𝜏, 𝜏 ′).
   For (WUb), suppose (𝜎, 𝜎 ′ )𝑊 ; 𝑆¤ (𝜏, 𝜏 ′). So (𝜎, 𝜎 ′ )𝑊 (𝜏, 𝜏 ′) and 𝜏𝑆𝜏 ′. By deﬁnition of 𝑊 we have
𝜎𝑐𝜏𝑆𝜏 ′ and 𝜎𝑅𝜎 ′𝑑𝜏 ′. Since 𝜎hav𝜏 we have (𝜎, 𝜎 ′)hhav | 𝑑i(𝜏, 𝜏 ′).

  Disjunctive Forward Witness Soundness Rules. To support case analysis, we also have additional
forward witness soundness rules with disjunctions. Fig. 6 presents three lemmas for disjunctive
decomposition of witnesses for forward simulation.
  DisjWC holds because        𝑅; (𝑊1 + 𝑊2 )
                         = 𝑅;𝑊1 + 𝑅;𝑊2               distrib
                          ≤ 𝑅;𝑊1 ; 𝑆 + 𝑅;𝑊2 ; 𝑆 assumptions
                         = 𝑅; (𝑊1 + 𝑊2 ); 𝑆
  DisjWU holds because        𝑅; (𝑊1 + 𝑊2 )
                          = 𝑅;𝑊1 + 𝑅;𝑊2                  distrib
                          ≤ hhav | 𝑑 1 i + hhav | 𝑑 2 i assumptions
                          = hhav | 𝑑 1 + 𝑑 2 i           emb homo

                                Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:44   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


   DisjWO holds because            𝑅; h𝑐 1 + 𝑐 2 ]
                                 = 𝑅; h𝑐 1 ] + 𝑅; h𝑐 2 ]             assumption, emb homo
                                 ≤ 𝑊1 ; [havi + 𝑊2 ; [havi           assumptions
                                 = (𝑊1 + 𝑊2 ); [havi
   Proof of Example 2.4 in Sect. 2. The programs:
   ( c1 )   x := any ; y := x
   ( c2 )   t := any ; z := t + 1
                                                             ∃
Goal: forward simulation judgment 𝑐 1 | 𝑐 2 : 𝑡𝑟𝑢𝑒 ≈> 𝑦 =𝑧.
                                                         ¥
Choose as witness, 𝑊 =ˆ hx:=any | t:=anyi; [𝑥 − 1 =¥ 𝑡]; hy:=x | z:=t+1i.
To show:
(WC) 𝑊 ≤ 𝑊 ; [𝑦 =𝑧]
                 ¥
(WU) 𝑊 ≤ hhav | t:=any; z:=t+1i
(WO) hx:=any; y:=x] ≤ 𝑊 ; [havi
• (WC)         hx:=any | t:=anyi; [𝑥 − 1 =¥ 𝑡]; hy:=x | z:=t+1i
          = hx:=any | t:=anyi; [𝑥 =¥ 𝑡 + 1]; hy:=x | z:=t+1i              equiv test
          = hx:=any | t:=anyi; [𝑥 =¥ 𝑡 + 1]; hy:=x | z:=t+1i[𝑦 =¥ 𝑧]
The last step is by the assignment axiom 𝑤𝑝 (hy:=x | z:=t+1i) (𝑦 =¥ 𝑧) = (𝑥 =¥ 𝑡 + 1) in the KAT form
(𝑥 =¥ 𝑡 + 1); hy:=x | z:=t+1i = (𝑥 =¥ 𝑡 + 1); hy:=x | z:=t+1i; (𝑦 =¥ 𝑧).
• (WU)          hx:=any | t:=anyi; [𝑥 − 1 =¥ 𝑡]; hy:=x | z:=t+1i
           ≤ hx:=any | t:=anyi; hy:=x | z:=t+1i                    tests below 1
          = hx:=any; y:=x | t:=any; z:=t+1i                        emb homo
           ≤ hhav | t:=any; z:=t+1i                                hav is top, emb mono
   • (WO) We use these axioms for the primitives:
  (a) 1 ≤ [t:=anyi; [𝑥 − 1 =¥ 𝑡]; [t:=anyi (says that [𝑥 − 1 =¥ 𝑡] is left total, cf. rule enAss)
  (b) hy:=x]; [𝑥 − 1 =¥ 𝑡] = [𝑥 − 1 =¥ 𝑡]; hy:=x] (disjoint variables)
  (c) z:=t+1; hav = hav (assignments are total)
We have (WO) because
                 hx:=any; y:=x]
            =    hx:=any]; hy:=x]                                               emb homo
            ≤    hx:=any]; hy:=x]; [t:=anyi; [𝑥 − 1 =¥ 𝑡]; [t:=anyi             (a)
            =    hx:=any | t:=anyi; hy:=x]; [𝑥 − 1 =¥ 𝑡]; [t:=anyi              LRC
            =    hx:=any | t:=anyi; [𝑥 − 1 =¥ 𝑡]; hy:=x]; [t:=anyi              (b)
            ≤    hx:=any | t:=anyi; [𝑥 − 1 =¥ 𝑡]; hy:=x]; [havi                 hav top, embed mono
            =    hx:=any | t:=anyi; [𝑥 − 1 =¥ 𝑡]; hy:=x | z:=t+1i; [havi        (c)
9.5.2   Proofs for Lemma 7.7, i.e., Forward Simulation Rules in Fig. 2.
  Proof of eAss. For alignment witness take 𝑊 := h𝑣 := 𝑒 | 𝑣 ′ := 𝑒 ′ i itself. Have (WC) in accord
                                                             ′
with the ∀∀ assignment rule dAss. For (WU), we have 𝑃𝑒𝑣|𝑒|𝑣′ ; h𝑣 := 𝑒 | 𝑣 ′ := 𝑒 ′ i ≤ h𝑣 := 𝑒 | 𝑣 ′ := 𝑒 ′ i ≤
hhav | 𝑣 ′ := 𝑒 ′ i by test below 1 and hav above all. For (WO):
    ′
𝑃𝑒𝑣|𝑒|𝑣′ ; h𝑣 := 𝑒 | 1i ≤ h𝑣 := 𝑒 | 1i ≤ h𝑣 := 𝑒 | havi = h𝑣 := 𝑒 | 𝑣 ′ := 𝑒 ′ ; havi = h𝑣 := 𝑒 | 𝑣 ′ := 𝑒 ′ i; h1 | havi

using homomorphism in the last step and the law hav = 𝑣 ′ := 𝑒 ′ ; hav. This law holds in usual
operational and denotational semantics.

Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                            20:45


   Proof of enAss. Let witness 𝑊 to be h𝑥 := any | 𝑦 := anyi; 𝑅.    ¤
   • (WC) 1; ¥ h𝑥 := any | 𝑦 := anyi; 𝑅¤ ≤ 1;                        ¤ 𝑅¤ holds by idempotence of tests.
                                           ¥ h𝑥 := any | 𝑦 := anyi; 𝑅;
   • (WU) 1; ¥ h𝑥 := any | 𝑦 := anyi; 𝑅¤ ≤ hhav | 𝑦 := anyi holds by 1¥ identity, hav top, h−] monotonic,
and 𝑅¤ ≤ 1.¥
   • (WO) is 1; ¥ h𝑥 := any] ≤ h𝑥 := any | 𝑦 := anyi; 𝑅;  ¤ [havi and we have 1;    ¥ h𝑥 := any] = 1;
                                                                                                   ¥ h𝑥 :=
any]; 1¥ ≤ 1;¥ h𝑥 := any]; [𝑦 := anyi; 𝑅; ¤ [𝑦 := anyi = h𝑥 := any | 𝑦 := anyi; 𝑅;   ¤ [𝑦 := anyi ≤ h𝑥 :=
                  ¤ [havi using the antecedent of the rule in the second step.
any | 𝑦 := anyi; 𝑅;

                                                                    ∃
  Proof of eConseq. Given witness 𝑊 for 𝑐 | 𝑑 : 𝑃 ≈> 𝑄, and conditions 𝑅 ⇒ 𝑃 and 𝑄 ⇒ 𝑆,
                                               ∃
                                                                                         ¤
we have that 𝑊 is also a witness for 𝑐 |𝑑 : 𝑅 ≈> 𝑆. To show (WC) for the latter, we have 𝑅;𝑊 ≤
¤       ¤     ¤   ¤     ¤                           ¤      ¤   ¤    ¤        ¤     ¤
𝑃;𝑊 ≤ 𝑃;𝑊 ; 𝑄 ≤ 𝑃;𝑊 ; 𝑆 using (WC) for 𝑊 . And 𝑅;𝑊 ≤ 𝑃;𝑊 ; 𝑆 iﬀ 𝑅;𝑊 ≤ 𝑅;𝑊 ; 𝑆 by KAT fact
𝑝𝑥 ≤ 𝑦 ⇔ 𝑝𝑥 ≤ 𝑝𝑦 and 𝑅¤ · 𝑃¤ = 𝑅¤ from 𝑅 ⇒ 𝑃. The proofs of (WO) and (WU) are even simpler.

                                                                                                             ∃
    Proof of eIf. Assume the side condition 𝑃 ⇒ 𝑒 =𝑒      ¥ ′ and premises 𝑐 | 𝑐 ′ : 𝑃 ∧ h𝑒] ∧ [𝑒 ′ i ≈> 𝑄 and
                               ∃
𝑑 | 𝑑 ′ : 𝑃 ∧ ¬h𝑒] ∧ ¬[𝑒 ′ i ≈> 𝑄. The encoding of the conclusion is about h𝑒; 𝑐 + ¬𝑒; 𝑑 | 𝑒 ′ ; 𝑐 ′ + ¬𝑒 ′ ; 𝑑 ′i.
The side condition yields 𝑃 = 𝑃; (h𝑒 | 𝑒 ′ i + h¬𝑒 | ¬𝑒 ′ i).
    By the theorem, there is some witness 𝑍 for the ﬁrst premise and 𝑊 for the second, such that
    (WCZ) 𝑃; h𝑒 | 𝑒 ′ i; 𝑍 ≤ 𝑃; h𝑒 | 𝑒 ′ i; 𝑍 ; 𝑄
    (WUZ) 𝑃; h𝑒 | 𝑒 ′ i; 𝑍 ≤ hhav | 𝑐 ′ i
    (WOZ) 𝑃; h𝑒 | 𝑒 ′ i; h𝑐 | 1i ≤ 𝑍 ; h1 | havi
    (WCW) 𝑃; h¬𝑒 | ¬𝑒 ′ i;𝑊 ≤ 𝑃; h¬𝑒 | ¬𝑒 ′ i;𝑊 ; 𝑄
    (WUW) 𝑃; h¬𝑒 | ¬𝑒 ′ i;𝑊 ≤ hhav | 𝑑 ′ i
    (WOW) 𝑃; h¬𝑒 | ¬𝑒 ′ i; h𝑑 | 1i ≤ 𝑊 ; h1 | havi
    To show the conclusion we take as witness 𝑋 := h𝑒 | 𝑒 ′ i; 𝑍 + h¬𝑒 | ¬𝑒 ′ i;𝑊 and prove each of the
conditions.
• (WC) is 𝑃; (h𝑒 | 𝑒 ′ i; 𝑍 + h¬𝑒 | ¬𝑒 ′ i;𝑊 ) ≤ 𝑃; (h𝑒 | 𝑒 ′ i; 𝑍 + h¬𝑒 | ¬𝑒 ′ i;𝑊 ); 𝑄 and we have


              𝑃; (h𝑒 | 𝑒 ′ i; 𝑍 + h¬𝑒 | ¬𝑒 ′ i;𝑊 )
         =    𝑃; (h𝑒 | 𝑒 ′ i + h¬𝑒 | ¬𝑒 ′ i); (h𝑒 | 𝑒 ′ i; 𝑍 + h¬𝑒 | ¬𝑒 ′ i;𝑊 )   side condition
         =    𝑃; h𝑒 | 𝑒 ′ i; 𝑍 + 𝑃; h¬𝑒 | ¬𝑒 ′ i;𝑊                                distribute, cancel, absorb
         ≤    𝑃; h𝑒 | 𝑒 ′ i; 𝑍 ; 𝑄 + 𝑃; h¬𝑒 | ¬𝑒 ′ i;𝑊 ; 𝑄                        (WCZ), (WCW)
         =    𝑃; (h𝑒 | 𝑒 ′ i; 𝑍 + h¬𝑒 | ¬𝑒 ′ i;𝑊 ); 𝑄                             symmetric steps


• (WU) is 𝑃; (h𝑒 | 𝑒 ′ i; 𝑍 + h¬𝑒 | ¬𝑒 ′ i;𝑊 ) ≤ hhav | 𝑒 ′ ; 𝑐 ′ + ¬𝑒 ′ ; 𝑑 ′i and we have


             𝑃; (h𝑒 | 𝑒 ′ i; 𝑍 + h¬𝑒 | ¬𝑒 ′ i;𝑊 ) ≤ hhav | 𝑒 ′ ; 𝑐 ′ + ¬𝑒 ′ ; 𝑑 ′i
           ⇔ 𝑃; h𝑒 | 𝑒 ′ i; 𝑍 + 𝑃 h¬𝑒 | ¬𝑒 ′ i;𝑊 ≤ hhav | 𝑒 ′ ; 𝑐 ′ + ¬𝑒 ′ ; 𝑑 ′i              distrib
           ⇔ 𝑃; h𝑒 | 𝑒 ′ i; 𝑍 + 𝑃 h¬𝑒 | ¬𝑒 ′ i;𝑊 ≤ hhav | 𝑒 ′ ; 𝑐 ′ i + hhav | ¬𝑒 ′ ; 𝑑 ′ i    emb homo
           ⇐ 𝑃; h𝑒 | 𝑒 ′ i; 𝑍 ≤ hhav | 𝑒 ′ ; 𝑐 ′ i ∧ 𝑃 h¬𝑒 | ¬𝑒 ′ i;𝑊 ≤ hhav | ¬𝑒 ′ ; 𝑑 ′i     + mono


Note that (WUZ) is equivalent to 𝑃; h𝑒 | 𝑒 ′ i; 𝑍 ≤ [𝑒 ′ i; hhav | 𝑐 ′ i (by 𝑝𝑥 ≤ 𝑦 ⇔ 𝑝𝑥 ≤ 𝑝𝑦) and then
by LRC we get [𝑒 ′ i; hhav | 𝑐 ′ i = hhav | 𝑒 ′ ; 𝑐 ′ i, which yields the left conjunct above. For the right
conjunct, use (WUW) similarly.

                                 Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:46   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


• (WO) is 𝑃; h𝑒; 𝑐 + ¬𝑒; 𝑑 | 1i ≤ (h𝑒 | 𝑒 ′ i; 𝑍 + h¬𝑒 | ¬𝑒 ′ i;𝑊 ); h1 | havi and we have

   𝑃; h𝑒; 𝑐 + ¬𝑒; 𝑑 | 1i ≤ (h𝑒 | 𝑒 ′ i; 𝑍 + h¬𝑒 | ¬𝑒 ′ i;𝑊 ); h1 | havi
 ⇔ side condition
   h𝑒 | 𝑒 ′ i + h¬𝑒 | ¬𝑒 ′ i); 𝑃; h𝑒; 𝑐 + ¬𝑒; 𝑑 | 1i ≤ (h𝑒 | 𝑒 ′ i; 𝑍 + h¬𝑒 | ¬𝑒 ′ i;𝑊 ); h1 | havi
 ⇐ distrib, cancel, + mono
   h𝑒 | 𝑒 ′ i; 𝑃; h𝑒; 𝑐 | 1i ≤ h𝑒 | 𝑒 ′ i; 𝑍 ; h1 | havi ∧ h¬𝑒 | ¬𝑒 ′ i; 𝑃; h¬𝑒; 𝑑 | 1i ≤ h¬𝑒 | ¬𝑒 ′ i;𝑊 ; h1 | havi
 ⇔ test property 𝑝𝑥 ≤ 𝑦 ⇔ 𝑝𝑥 ≤ 𝑝𝑦
   h𝑒 | 𝑒 ′ i; 𝑃; h𝑒; 𝑐 | 1i ≤ 𝑍 ; h1 | havi ∧ h¬𝑒 | ¬𝑒 ′ i; 𝑃; h¬𝑒; 𝑑 | 1i ≤ 𝑊 ; h1 | havi

The latter conjuncts are equivalent to (WOZ) and (WOW), using emb homo on the left.
                                                                                              ∃
   Proof of eWh. Suppose we have 𝑃 ⇒ 𝑒 =𝑒        ¥ ′ and 𝑐 | 𝑐 ′ : 𝑃 ∧ h𝑒] ∧ [𝑒 ′ i ≈> 𝑃. Suppose we have
alignment witness 𝑊 for this judgment, thus
   (WCW) 𝑃; h𝑒 | 𝑒 ′ i;𝑊 ≤ 𝑃; h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃
   (WUW) 𝑃; h𝑒 | 𝑒 ′ i;𝑊 ≤ hhav | 𝑐 ′ i
   (WOW) 𝑃; h𝑒 | 𝑒 ′ i; h𝑐 | 1i ≤ 𝑊 ; h1 | havi
                                                        ∃
   To show while 𝑒 do 𝑐 | while 𝑒 ′ do 𝑐 ′ : 𝑃 ≈> 𝑃 ∧ ¬h𝑒] ∧ ¬[𝑒 ′ i, take as alignment witness
            ′     ∗
𝑍 := (h𝑒 | 𝑒 i;𝑊 ) ; h¬𝑒].
• (WC) is 𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; h¬𝑒] ≤ 𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; h¬𝑒]𝑃 h¬𝑒 | ¬𝑒 ′ i = 𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; h¬𝑒 | ¬𝑒 ′ i
and we have

                       𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; h¬𝑒]
                     = 𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; 𝑃; h¬𝑒]              (WCW) and invariance
                     = 𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; 𝑃; h¬𝑒 | ¬𝑒i         by side condition, 𝑃 ⇒ 𝑒 =¥ 𝑒 ′

• (WO) is 𝑃; h(𝑒; 𝑐) ∗ ; ¬𝑒] ≤ (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; h¬𝑒]; [havi. To establish this fact, we start by calculating

        𝑃; h(𝑒; 𝑐) ∗ ; ¬𝑒] ≤ (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; h¬𝑒]; hhav]
  ⇔     𝑃; h𝑒; 𝑐] ∗ ; h¬𝑒] ≤ (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; [havi; h¬𝑒]                           emb homo and LRC
  ⇐     𝑃; h𝑒; 𝑐] ∗ ≤ (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; [havi                                        monotonicity
  ⇔     𝑃; h𝑒; 𝑐] ∗ ≤ 𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; [havi                                     using 𝑎; 𝑥 ≤ 𝑦 ⇔ 𝑎; 𝑥 ≤ 𝑎; 𝑦
  ⇐     𝑃 + 𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; [havi; h𝑒; 𝑐] ≤ 𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; [havi        induction
  ⇐     𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; [havi; h𝑒; 𝑐] ≤ 𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; [havi            join, and 𝑃 ≤ RHS
  ⇔     𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; h𝑒; 𝑐 | havi ≤ 𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; [havi             rewrite LHS

Now consider the LHS. We have:

                  𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; h𝑒; 𝑐 | havi
            =     𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; 𝑃; h𝑒; 𝑐 | havi                        (WCW) and invariance
            =     𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; 𝑃; h𝑒; 𝑐 | 𝑒 ′ ; havi                  side condition, 𝑃 ⇒ 𝑒 =¥ 𝑒 ′
            =     𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; 𝑃; h𝑒 | 𝑒 ′ i; 𝑃; h𝑒; 𝑐 | 𝑒 ′ i[havi   duplicate tests, emb homo
            ≤     𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; 𝑃; h𝑒 | 𝑒 ′ i;𝑊 ; [havi                (WOW)
            ≤     𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; h𝑒 | 𝑒 ′ i;𝑊 ; [havi                   drop test 𝑃
            ≤     𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; [havi                                  using 𝑥 ∗ ; 𝑥 ≤ 𝑥 ∗

This is equal to the RHS and we are done.

Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                                       20:47


• (WU) is 𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; h¬𝑒] ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i. We show

               𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; h¬𝑒] ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i
             ⇔ using lemma 𝑝; 𝑥 = 𝑝; 𝑥; 𝑝 ⇒ 𝑝; 𝑥 ∗ = 𝑝; (𝑥; 𝑝) ∗ and (WCW)
               𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; h¬𝑒] ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i
             ⇔ sliding
               (𝑃; h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; 𝑃; h¬𝑒] ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i
             ⇔ side condition, 𝑃 ⇒ 𝑒 =¥ 𝑒 ′
               (𝑃; h𝑒 | 𝑒 ′ i;𝑊 ) ∗ ; 𝑃; h¬𝑒 | ¬𝑒 ′ i ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i
             ⇐ induction, 𝑥 ∗ ; 𝑦 ≤ 𝑧 ⇐ 𝑦 + 𝑥; 𝑧 ≤ 𝑧
               𝑃; h¬𝑒 | ¬𝑒 ′ i + 𝑃; h𝑒 | 𝑒 ′ i;𝑊 ; hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i

   Since 𝑃; h¬𝑒 | ¬𝑒 ′ i is less than the RHS, by join, it suﬃces to show:

               𝑃; h𝑒 | 𝑒 ′ i;𝑊 ; hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒i ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i
         ⇔     𝑃; h𝑒 | 𝑒 ′ i; [𝑒 ′ i;𝑊 ; hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i   dup test [𝑒 ′ i
         ⇔     [𝑒 ′ i; 𝑃; h𝑒 | 𝑒 ′ i;𝑊 ; hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i   commute tests
         ⇐     [𝑒 ′ i; hhav | 𝑐 ′ i; hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i       using (WUW)
         ⇔     hhav | 𝑒 ′ ; 𝑐 ′ i; hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i         emb homo
         ⇐     [𝑒 ′ ; 𝑐 ′ ; (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i ≤ [(𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i                             hav is top

But this follows from the fact that 𝑥; 𝑥 ∗ ≤ 𝑥 ∗ .

                                                                                                               ∃
   Proof of eWhL. Suppose we have 𝑃 ⇒ ( [𝑒 ′ i ⇒ h𝑒]), 𝑐 | 𝑐 ′ : 𝑃 ∧ h𝑒] ∧ [𝑒 ′ i ≈> 𝑃, and 𝑐 | skip :
         ∃
𝑃 ∧ h𝑒] ≈> 𝑃. From judgment for 𝑐 | 𝑐 ′ obtain alignment witness 𝐵 and from judgment for 𝑐 | skip
obtain witness 𝐿. We have,
   (WCB) 𝑃; h𝑒 | 𝑒 ′ i; 𝐵 ≤ 𝑃; h𝑒 | 𝑒 ′ i; 𝐵; 𝑃
   (WCL) 𝑃; h𝑒 | 1i; 𝐿 ≤ 𝑃; h𝑒 | 1i; 𝐿; 𝑃
   (WUB) 𝑃; h𝑒 | 𝑒 ′ i; 𝐵 ≤ hhav | 𝑐 ′ i
   (WUL) 𝑃; h𝑒 | 1i; 𝐿 ≤ hhav | 1i
   (WOB) 𝑃; h𝑒 | 𝑒 ′ i; h𝑐 | 1i ≤ 𝐵; h1 | havi
   (WOL) 𝑃; h𝑒 | 1i; h𝑐 | 1i ≤ 𝐿; h1 | havi
                                                  ∃
   To show while 𝑒 do 𝑐 | while 𝑒 ′ do 𝑐 ′ : 𝑃 ≈> 𝑃 ∧ ¬h𝑒] ∧ ¬[𝑒 ′ i we take as alignment witness
𝑊 := (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; (h𝑒 | 1i𝐿) ∗ ; h¬𝑒 | 1i.
   We have to show:
   (WC) 𝑃;𝑊 ≤ 𝑃;𝑊 ; 𝑃; h¬𝑒 | ¬𝑒 ′ i
   (WU) 𝑃;𝑊 ≤ hhav | (𝑒 ′𝑐 ′ ) ∗ ¬𝑒 ′ i
   (WO) 𝑃; h(𝑒𝑐) ∗ ¬𝑒 | 1i ≤ 𝑊 ; h1 | havi
• For (WC), we have:

                 𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; (h𝑒]; 𝐿) ∗ ; h¬𝑒]
           ≤     𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; 𝑃; (h𝑒]; 𝐿) ∗ ; h¬𝑒]                  using (WCB) and invariance
           ≤     𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; 𝑃; (h𝑒]; 𝐿) ∗ ; 𝑃; h¬𝑒]               using (WCL) and invariance
           =     𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; 𝑃; (h𝑒]; 𝐿) ∗ ; 𝑃; h¬𝑒 | ¬𝑒 ′ i       using side condition 𝑃 ⇒ 𝑒 =¥ 𝑒 ′
           ≤     𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; (h𝑒]; 𝐿) ∗ ; 𝑃; h¬𝑒 | ¬𝑒 ′ i          drop test 𝑃

                                    Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:48   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


• For (WU), we have to show 𝑃; (h𝑒 | 𝑒 ′ i𝐵) ∗ ; (h𝑒]; 𝐿) ∗ ; h¬𝑒] ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i. We calculate as
follows,



              𝑃; (h𝑒 | 𝑒 ′ i𝐵) ∗ ; (h𝑒]; 𝐿) ∗ ; h¬𝑒] ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i
        ⇐     (WCB) with Lemma 9.4
              𝑃; (h𝑒 | 𝑒 ′ i𝐵; 𝑃) ∗ ; (h𝑒]; 𝐿) ∗ ; h¬𝑒] ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i
        ⇔     sliding
              (𝑃; h𝑒 | 𝑒 ′ i𝐵; ) ∗ ; 𝑃; (h𝑒]; 𝐿) ∗ ; h¬𝑒] ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i
        ⇔     (WCL) and invariance
              (𝑃; h𝑒 | 𝑒 ′ i𝐵; ) ∗ ; 𝑃; (h𝑒]; 𝐿) ∗ ; 𝑃; h¬𝑒] ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i
        ⇔     by side condition 𝑃 ⇒ 𝑒 =¥ 𝑒 ′ , whence 𝑃 h¬𝑒] = 𝑃 h¬𝑒 | ¬𝑒 ′ i
              (𝑃; h𝑒 | 𝑒 ′ i𝐵; ) ∗ ; 𝑃; (h𝑒]; 𝐿) ∗ ; 𝑃; h¬𝑒 | ¬𝑒 ′ i ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i
        ⇐     induction, 𝑥 ∗ ; 𝑦 ≤ 𝑧 ⇐ 𝑦 + 𝑥; 𝑧 ≤ 𝑧
              𝑃 (h𝑒]; 𝐿) ∗ ; 𝑃; h¬𝑒 | ¬𝑒 ′ i + 𝑃; h𝑒 | 𝑒 ′ i; 𝐵; hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i



   By join, it suﬃces to check two conditions:



                         𝑃; (h𝑒]; 𝐿) ∗ ; 𝑃; h¬𝑒 | ¬𝑒 ′ i ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i
                  ⇐      (WCL) using Lemma 9.4
                         𝑃; (h𝑒]; 𝐿; 𝑃) ∗ ; 𝑃; h¬𝑒 | ¬𝑒 ′ i ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i
                  ⇔      sliding and test idem
                         (𝑃; h𝑒]; 𝐿; ) ∗ ; 𝑃; h¬𝑒 | ¬𝑒 ′ i ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i
                  ⇐      induction
                         𝑃; h¬𝑒 | ¬𝑒 ′ i + 𝑃; h𝑒]; 𝐿; hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i
                  ⇐      join along with 𝑃; h¬𝑒 | ¬𝑒 ′ i ≤ RHS
                         𝑃; h𝑒]; 𝐿; hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i
                  ⇐      (WUL)
                         hhav]; hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i



This follows from hav being top and reﬂexivity. For the other case, we have:



         𝑃; h𝑒 | 𝑒 ′ i; 𝐵; hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i
  ⇔      [𝑒 ′ i; 𝑃; h𝑒 | 𝑒 ′ i; 𝐵; hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i   tests idem, tests commute
  ⇐      [𝑒 ′ i; hhav | 𝑐 ′ i; hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i       (WUB)
  ⇔      hhav | 𝑒 ′ ; 𝑐 ′ i; hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i         LRC, emb homo
  ⇐      𝑒 ′ ; 𝑐 ′ ; (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ ≤ (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′



And the last fact follows from 𝑥; 𝑥 ∗ ≤ 𝑥 ∗ .


Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                               20:49


• Finally, for (WO) we have to show 𝑃; h(𝑒; 𝑐) ∗ ; ¬𝑒 | 1i ≤ (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; (h𝑒]; 𝐿) ∗ ; h¬𝑒 | havi. We
argue
        ⇔     by 𝑎; 𝑥 ≤ 𝑦 ⇔ 𝑎; 𝑥 ≤ 𝑎; 𝑦
              𝑃; h(𝑒; 𝑐) ∗ ; ¬𝑒 | 1i ≤ 𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; (h𝑒]; 𝐿) ∗ ; h¬𝑒 | havi
        ⇔     emb homo and LRC
              𝑃; h𝑒; 𝑐] ∗ ; h¬𝑒] ≤ 𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; (h𝑒]; 𝐿) ∗ ; [havi; h¬𝑒]
        ⇐     monotonicity
              𝑃; h𝑒; 𝑐] ∗ ≤ 𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; (h𝑒]; 𝐿) ∗ ; [havi
        ⇐     induction
              𝑃 + 𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; (h𝑒]; 𝐿) ∗ ; [havi; h𝑒; 𝑐] ≤ 𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; (h𝑒]; 𝐿) ∗ ; [havi
        ⇐     by join and 𝑃 ≤ RHS
              𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; (h𝑒]; 𝐿) ∗ ; [havi; h𝑒; 𝑐] ≤ 𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; (h𝑒]; 𝐿) ∗ ; [havi
        ⇔     hav idem, emb homo
              𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; (h𝑒]; 𝐿) ∗ ; [havi; h𝑒; 𝑐] ≤ 𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; (h𝑒]; 𝐿) ∗ ; [havi; [havi
        ⇔     LRC
              𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; (h𝑒]; 𝐿) ∗ ; h𝑒; 𝑐]; [havi ≤ 𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; (h𝑒]; 𝐿) ∗ ; [havi; [havi
        ⇐     monotonicity
              𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; (h𝑒]; 𝐿) ∗ ; h𝑒; 𝑐] ≤ 𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; (h𝑒]; 𝐿) ∗ ; [havi
   Now, we show
                  𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; (h𝑒]; 𝐿) ∗ ; h𝑒; 𝑐]
             ≤    𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; 𝑃; (h𝑒]; 𝐿) ∗ ; h𝑒; 𝑐]        using (WCB) and invariance
             ≤    𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; 𝑃; (h𝑒]; 𝐿) ∗ ; 𝑃; h𝑒; 𝑐]     using (WCL) and invariance
             ≤    𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; (h𝑒]; 𝐿) ∗ ; 𝑃; h𝑒; 𝑐]        dropping test 𝑃 in the middle
             =    𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; (h𝑒]; 𝐿) ∗ ; h𝑒]; 𝑃; h𝑒; 𝑐]   duplicating h𝑒] and commuting
             ≤    𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; (h𝑒]; 𝐿) ∗ ; h𝑒]; 𝐿; [havi    using (WOL)
             ≤    𝑃; (h𝑒 | 𝑒 ′ i; 𝐵) ∗ ; (h𝑒]; 𝐿) ∗ [havi              since 𝑥 ∗ ; 𝑥 ≤ 𝑥 ∗
And now we are done since this is equal to the RHS.
  Proof of eDisj. We give two proofs.
  First, here is a proof directly in terms of the TriKAT formulation (12). We use that w and se-
quence distribute over +, as does the embedding:
             h𝐴 + 𝐵 8 𝐶i = h𝐴 8 𝐶i + h𝐵 8 𝐶i                and        h𝐴 8 𝐵 + 𝐶i = h𝐴 8 𝐵i + h𝐵 8 𝐶i               (17)
These facts are easily proved for any relational model (not necessarily full). These conditions are
candidates for an axiomatization of TriKAT.
                               ∃                 ∃
  The premises are 𝑐 | 𝑑 : 𝑃 ≈> 𝑄 and 𝑐 | 𝑑 : 𝑅 ≈> 𝑄. Here are the premises expressed in the form
given by (12):
                                     ¤ ≤ w(h𝑃¤ 8 𝑖𝑑i;
                       ¤ h𝑐 | havi; 𝑖𝑑
                       𝑃;                          ¤ h𝑐 | hav | 𝑑i; h𝑖𝑑
                                                                      ¤ 8 𝑄i)
                                                                          ¤
                                     ¤ ≤ w(h𝑅¤ 8 𝑖𝑑i;
                       ¤ h𝑐 | havi; 𝑖𝑑
                       𝑅;                          ¤ h𝑐 | hav | 𝑑i; h𝑖𝑑
                                                                      ¤ 8 𝑄i)
                                                                          ¤
                                    ∃
The conclusion 𝑐 | 𝑑 : 𝑃 ∨ 𝑅 ≈> 𝑄 is expressed as
               (𝑃¤ + 𝑅);            ¤ ≤ w(h(𝑃¤ + 𝑅)
                      ¤ h𝑐 | havi; 𝑖𝑑                  ¤ h𝑐 | hav | 𝑑i; h𝑖𝑑
                                                  ¤ 8 𝑖𝑑i;                ¤ 8 𝑄i)
                                                                              ¤
By disjunctivity, LHS equals
                                                 ¤ + 𝑅;
                                   ¤ h𝑐 | havi; 𝑖𝑑
                                  𝑃;                               ¤
                                                     ¤ h𝑐 | havi; 𝑖𝑑
and by disjunctivity, including the left equation of (17), RHS equals
                       ¤ h𝑐 | hav | 𝑑i; h𝑖𝑑
            w(h𝑃¤ 8 𝑖𝑑i;                  ¤ 8 𝑄i)
                                              ¤ + w(h𝑅¤ 8 𝑖𝑑i;¤ h𝑐 | hav | 𝑑i; h𝑖𝑑
                                                                                 ¤ 8 𝑄i)
                                                                                     ¤

                                 Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:50   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


Now LHS≤RHS follows directly from the premises by monotonicity of +.
   Second, we give a proof of eDisj using witnesses. Let 𝑊 and 𝑋 be witnesses of the ﬁrst and
second premise, so we have
    (WCW) 𝑃;𝑊 ¤        ¤ ; 𝑄¤
                   ≤ 𝑃;𝑊         (WCX) 𝑅;   ¤ 𝑋 ≤ 𝑅;
                                                   ¤ 𝑋 ; 𝑄¤
    (WUW) 𝑃;𝑊 ¤    ≤ hhav | 𝑑i   (WUX) 𝑅;   ¤ 𝑋 ≤ hhav | 𝑑i
    (WOW) 𝑃;  ¤ h𝑐] ≤ 𝑊 ; [havi (WOX) 𝑅;    ¤ h𝑐] ≤ 𝑋 ; [havi
Let 𝑍 = ¤
      ˆ 𝑃;𝑊     ¤ 𝑋 . We show that 𝑍 satisﬁes the witness conditions for the conclusion.
             + 𝑅;
• (WC)
                       (𝑃¤ + 𝑅);
                             ¤ (𝑃;𝑊
                                  ¤      ¤ 𝑋)
                                       + 𝑅;
                 =     ¤        ¤ ¤      ¤  ¤
                       𝑃;𝑊 + 𝑃; 𝑅; 𝑋 + 𝑅; 𝑃;𝑊        ¤ 𝑋
                                                  + 𝑅;                       distrib, tests idem
                 ≤     ¤           ¤ ¤         ¤   ¤        ¤ 𝑋;𝑄
                       𝑃;𝑊 ; 𝑄 + 𝑃; 𝑅; 𝑋 ; 𝑄 + 𝑅; 𝑃;𝑊 ; 𝑄 + 𝑅;               (WCW) and (WCX)
                 =       ¤   ¤    ¤      ¤
                       (𝑃 + 𝑅); (𝑃;𝑊 + 𝑅; 𝑋 ); 𝑄 ¤                           distrib, tests idem

• (WU) The obligation (𝑃¤ + 𝑅);
                            ¤ (𝑃;𝑊
                                ¤    ¤ 𝑋 ) ≤ hhav | 𝑑i is equivalent, by distributivity and tests
                                   + 𝑅;
idempotent, to
                                 ¤
                                 𝑃;𝑊   ¤ 𝑅;
                                     + 𝑃; ¤ 𝑋 + 𝑅;
                                                ¤ 𝑃;𝑊
                                                   ¤    ¤ 𝑋 ≤ hhav | 𝑑i
                                                      + 𝑅;

By the join property of + this is equivalent to four inequalities, all consequences of (WUW) or
(WUX), for example 𝑃;¤ 𝑅;
                       ¤ 𝑋 ≤ 𝑅;¤ 𝑋 ≤ hhav | 𝑑i using (WUX).
• (WO) By distribution, the obligation (𝑃¤ + 𝑅);
                                             ¤ h𝑐] ≤ (𝑃;𝑊
                                                       ¤      ¤ 𝑋 ); [havi is equivalent to
                                                           + 𝑅;

                                 ¤ h𝑐] + 𝑅;
                                 𝑃;      ¤ h𝑐] ≤ 𝑃;𝑊
                                                 ¤ ; [havi + 𝑅;
                                                             ¤ 𝑋 ; [havi

which follows from (WOW) and (WOX) by monotonicity of +.

9.5.3   Proofs for Backward Simulation Rules. Fig. 3 gives some backward simulation rules.

   Sequential Composition bSeq. The rule bSeq looks the same as dSeq and eSeq except that it is
about the backwards judgment.
                                   ∃                                          ∃
   Suppose for premise 𝑐 | 𝑐 ′ : 𝑃 ≈> 𝑅 we have witness 𝑍 and for 𝑑 | 𝑑 ′ : 𝑅 ≈> 𝑄 we have witness
𝑊 , so the conditions are
   (WCbZ) 𝑍 ; 𝑅 ≤ 𝑃; 𝑍 ; 𝑅
   (WUbZ) 𝑍 ; 𝑅 ≤ hhav | 𝑐 ′ i
   (WObZ) h𝑐 | 1i; 𝑅 ≤ h1 | havi; 𝑍
   (WCbW) 𝑊 ; 𝑄 ≤ 𝑅;𝑊 ; 𝑄
   (WUbW) 𝑊 ; 𝑄 ≤ hhav | 𝑑 ′ i
   (WObW) h𝑑 | 1i; 𝑄 ≤ h1 | havi;𝑊
                                                 ∃
   To prove the conclusion 𝑐; 𝑑 | 𝑐 ′ ; 𝑑 ′ : 𝑃 ≈> 𝑄 we use 𝑍 ;𝑊 as witness, showing it satisﬁes the
three conditions.
• (WCb) To show 𝑍 ;𝑊 ; 𝑄 ≤ 𝑃; 𝑍 ;𝑊 ; 𝑄 we have 𝑍 ;𝑊 ; 𝑄 ≤ 𝑍 ; 𝑅;𝑊 ; 𝑄 ≤ 𝑃; 𝑍 ; 𝑅;𝑊 ; 𝑄 ≤
𝑃; 𝑍 ;𝑊 ; 𝑄 using (WCbZ), (WCbW), and test below 1.
• (WUb)

                 𝑍 ;𝑊 ; 𝑄 ≤ hhav | 𝑐; 𝑑 ′ i
               ⇔ 𝑍 ; 𝑅;𝑊 ; 𝑄 ≤ hhav | 𝑐; 𝑑 ′ i                  using (WCbW) in equality form
               ⇔ 𝑍 ; 𝑅;𝑊 ; 𝑄 ≤ hhav | 𝑐i; hhav | 𝑑 ′ i          hav idem, emb homo

and the last line follows from (WUbZ) and (WUbW) using monotonicity of sequence.

Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                                        20:51


• (WOb)

                        h𝑐; 𝑑 | 1i; 𝑄
                  =     h𝑐 | 1i; h𝑑 | 1i; 𝑄; 𝑄                      emb homo, test idem
                  ≤     h𝑐 | 1i; h1 | havi;𝑊 ; 𝑄                    (WObW)
                  =     h𝑐 | 1i; h1 | havi; 𝑅;𝑊 ; 𝑄                 (WCbW) as equality
                  =     h1 | havi; h𝑐 | 1i; 𝑅;𝑊 ; 𝑄                 LRC
                  ≤     h1 | havi; h1 | havi; 𝑍 ;𝑊 ; 𝑄              (WObZ)
                  ≤     h1 | havi; 𝑍 ;𝑊                             hav idem, emb homo, test below 1

                                                                                                                              ∃
  Proof of Loop Rule bWh. Suppose we have witness 𝑊 for the premise 𝑐 | 𝑐 ′ : 𝑃 ∧ h𝑒] ∧ [𝑒 ′ i ≈> 𝑃,
with

                        (𝑊 𝐶𝑏𝑊 ) 𝑊 ; 𝑃 ≤ 𝑃; h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃                   in brief: 𝑊 𝑃 ≤ 𝑃𝑒𝑒 ′𝑊 𝑃
                        (𝑊 𝑈 𝑏𝑊 ) 𝑊 ; 𝑃 ≤ hhav | 𝑐 ′ i                         in brief: 𝑊 𝑃 ≤ hhav]𝑐 ′
                        (𝑊 𝑂𝑏𝑊 ) h𝑐]; 𝑃 ≤ [havi;𝑊 ; 𝑃                          in brief: 𝑐𝑃 ≤ [havi𝑊 𝑃

   For loop witness we choose 𝑍 := (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; h¬𝑒 | ¬𝑒 ′ i.
• (WCb) for conclusion is (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; h¬𝑒 | ¬𝑒 ′ i; 𝑃 ≤ 𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; h¬𝑒 | ¬𝑒 ′ i; 𝑃. We have,

              (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; h¬𝑒 | ¬𝑒 ′ i; 𝑃 ≤ 𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; h¬𝑒 | ¬𝑒 ′ i; 𝑃
       ⇔      (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; 𝑃; h¬𝑒 | ¬𝑒 ′ i ≤ 𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; 𝑃; h¬𝑒 | ¬𝑒 ′ i         tests commute
       ⇐      (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; 𝑃 ≤ 𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; 𝑃

which holds by backwards invariance Lemma 9.3 using h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃 ≤ 𝑃; h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃 which fol-
lows from (WCbW).
• (WUb) for conclusion is (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; h¬𝑒 | ¬𝑒 ′ i; 𝑃 ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i. We have,

            (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; h¬𝑒 | ¬𝑒 ′ i; 𝑃 ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i
      ⇐     h¬𝑒 | ¬𝑒 ′ i; 𝑃 + h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃; hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i   induction

Using join, for the ﬁrst conjunct h¬𝑒 | ¬𝑒 ′ i; 𝑃 ≤ hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i holds using 1 below star and
hav is top. For the second conjunct, we have

                          h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃; hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i
                    ≤     h𝑒 | 𝑒 ′ i; hhav | 𝑐 ′ i; hhav | (𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i   using WUbW
                    =     h𝑒]; hhav]; [𝑒 ′; 𝑐 ′ i; [(𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i          LRC, hav idempotent
                    ≤     h𝑒]; hhav]; [(𝑒 ′; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i                        using 𝑥; 𝑥 ★ ≤ 𝑥 ∗
                    ≤     hhav]; [(𝑒 ′ ; 𝑐 ′ ) ∗ ; ¬𝑒 ′ i                            test below 1

• (WOb) for the conclusion is h(𝑒; 𝑐) ∗ ; ¬𝑒]; h¬𝑒 | ¬𝑒 ′ i; 𝑃 ≤ [havi; (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; h𝑒 | 𝑒 ′ i; 𝑃. We
have,

   h(𝑒; 𝑐) ∗ ; ¬𝑒]; h¬𝑒 | ¬𝑒 ′ i; 𝑃 ≤ [havi; (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; h𝑒 | 𝑒 ′ i; 𝑃
 ⇐ induction, 𝑎 ∗ ; 𝑏 ≤ 𝑥 from 𝑏 + 𝑎; 𝑥 ≤ 𝑥
   h¬𝑒 | ¬𝑒 ′ i; 𝑃 + h𝑒; 𝑐]; [havi; (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; h¬𝑒 | ¬𝑒 ′ i; 𝑃 ≤ [havi; (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; h𝑒 | 𝑒 ′ i; 𝑃

                                   Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:52    Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


Using join and the fact that tests are below 1, star is above 1, and hav top, it suﬃces to show the
second conjunct is less than or equal to the RHS.
        h𝑒; 𝑐]; [havi; (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; h¬𝑒 | ¬𝑒 ′ i; 𝑃
 =      h𝑒; 𝑐]; [havi; (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; 𝑃; h¬𝑒 | ¬𝑒 ′ i                               tests commute
 =      h𝑒; 𝑐]; [havi; 𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; 𝑃; h¬𝑒 | ¬𝑒 ′ i                            backward invariance
 =      [havi; h𝑒; 𝑐]; 𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; 𝑃; h¬𝑒 | ¬𝑒 ′ i                            LRC
 ≤      using (WObW) in equivalent form h𝑐]; 𝑃 ≤ [havi;𝑊 ; 𝑃
        [havi; h𝑒]; [havi;𝑊 ; 𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; 𝑃; h¬𝑒 | ¬𝑒 ′ i
 =      [havi; h𝑒]; [havi; 𝑃; h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; 𝑃; h¬𝑒 | ¬𝑒 ′ i      using (WCbW) as an equality
 =      [havi; 𝑃; h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; 𝑃; h¬𝑒 | ¬𝑒 ′ i                  LRC, tests and hav idem
 ≤      [havi; 𝑃; (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; 𝑃; h¬𝑒 | ¬𝑒 ′ i                                    star fold
 ≤      [havi; (h𝑒 | 𝑒 ′ i;𝑊 ; 𝑃) ∗ ; 𝑃; h¬𝑒 | ¬𝑒 ′ i                                       test below 1


  Proof of bIf. The rule is like dIf and eIf except no side condition is needed.
                                                  ∃                                     ∃
  Suppose the premises 𝑐 | 𝑐 ′ : 𝑃 ∧ h𝑒] ∧ [𝑒 ′ i ≈> 𝑄 and 𝑑 | 𝑑 ′ : 𝑃 ∧ ¬h𝑒] ∧ ¬[𝑒 ′ i ≈> 𝑄 are witnessed
by 𝑍 and 𝑊 , so we have
  (WCbZ) 𝑍 ; 𝑄 ≤ 𝑃; h𝑒 | 𝑒 ′ i; 𝑍 ; 𝑄
  (WUbZ) 𝑍 ; 𝑄 ≤ hhav | 𝑐 ′ i
  (WObZ) h𝑐]; 𝑄 ≤ [havi; 𝑍
  (WCbW) 𝑊 ; 𝑄 ≤ 𝑃; h¬𝑒 | ¬𝑒 ′ i;𝑊 ; 𝑄
  (WUbW) 𝑊 ; 𝑄 ≤ hhav | 𝑑 ′ i
  (WObW) h𝑑]; 𝑄 ≤ [havi;𝑊
  As witness we choose h𝑒 | 𝑒 ′ i; 𝑍 + h¬𝑒 | ¬𝑒 ′ i;𝑊 .
• To prove (WCb) for the conclusion:
                     (h𝑒 | 𝑒 ′ i𝑍 + h¬𝑒 | ¬𝑒 ′ i𝑊 )𝑄
                =    h𝑒 | 𝑒 ′ i𝑍𝑄 + h¬𝑒 | ¬𝑒 ′ i𝑊 𝑄           distrib
                ≤    𝑃 h𝑒 | 𝑒 ′ i𝑍𝑄 + 𝑃 h¬𝑒 | ¬𝑒 ′ i𝑊 𝑄       (WCbZ), (WCbW), tests idem, + mono
                =    𝑃 (h𝑒 | 𝑒 ′ i𝑍 + h¬𝑒 | ¬𝑒 ′ i𝑊 )𝑄        distrib
• To prove (WUb) for the conclusion:
         (h𝑒 | 𝑒 ′ i𝑍 + h¬𝑒 | ¬𝑒 ′ i𝑊 )𝑄 ≤ hhav | 𝑒 ′𝑐 ′ + ¬𝑒 ′𝑑 ′i
 ⇔       h𝑒 | 𝑒 ′ i𝑍𝑄 + h¬𝑒 | ¬𝑒 ′ i𝑊 𝑄 ≤ hhav | 𝑒 ′𝑐 ′ i + hhav | ¬𝑒 ′𝑑 ′i                             distrib, emb homo
 ⇔       h𝑒 | 𝑒 ′ i𝑍𝑄 + h¬𝑒 | ¬𝑒 ′ i𝑊 𝑄 ≤ [𝑒 ′ ihhav | 𝑐 ′ i + [¬𝑒 ′ ihhav | 𝑑 ′i                       emb homo, LRC
 ⇐       h𝑒 | 𝑒 ′ ihhav | 𝑐 ′ i + h¬𝑒 | ¬𝑒 ′ ihhav | 𝑑 ′ i ≤ [𝑒 ′ ihhav | 𝑐 ′ i + [¬𝑒 ′ ihhav | 𝑑 ′ i   using (WUbZ), (WUbW)
which holds by tests below 1 and emb homo: h𝑒 | 𝑒 ′ i ≤ [𝑒 ′ i and h¬𝑒 | ¬𝑒 ′ i ≤ h𝑒].
• To prove (WOb) for the conclusion, we use (WObZ) and (WObW) in the equivalent forms h𝑐]; 𝑄 ≤
[havi; 𝑍 ; 𝑄 and h𝑑]; 𝑄 ≤ [havi;𝑊 ; 𝑄 (by 𝑥𝑞 ≤ 𝑦 ⇔ 𝑥𝑞 ≤ 𝑦𝑞).
           h𝑒𝑐 + ¬𝑒𝑑]; 𝑄 ≤ [havi; (h𝑒 | 𝑒 ′ i; 𝑍 + h¬𝑒 | ¬𝑒 ′ i;𝑊 )
     ⇔     distrib, emb homo
           h𝑒]; h𝑐]; 𝑄 + h¬𝑒]; h𝑑]; 𝑄 ≤ [havi; 𝑃; h𝑒 | 𝑒 ′ i; 𝑍 + [havi; 𝑃; h¬𝑒 | ¬𝑒 ′ i;𝑊
     ⇐     (WObZ), (WObW)
           h𝑒]; [havi; 𝑍 ; 𝑄 + h¬𝑒]; [havi;𝑊 ; 𝑄 ≤ [havi; h𝑒 | 𝑒 ′ i; 𝑍 + [havi; h¬𝑒 | ¬𝑒 ′ i;𝑊
     ⇔     (LRC)
           [havi; h𝑒]; 𝑍 ; 𝑄 + [havi; h¬𝑒];𝑊 ; 𝑄 ≤ [havi; h𝑒 | 𝑒 ′ i; 𝑍 + [havi; h¬𝑒 | ¬𝑒 ′ i;𝑊
     ⇔     (WCbZ),(WCbW)
           [havi; h𝑒 | 𝑒 ′ i; 𝑍 ; 𝑄 + [havi; h¬𝑒 | ¬𝑒 ′ i;𝑊 ; 𝑄 ≤ [havi; h𝑒 | 𝑒 ′ i; 𝑍 + [havi; h¬𝑒 | ¬𝑒 ′ i;𝑊

Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                            20:53


The last step uses (WCbZ) and (WCbW) in equality form. It holds by test below 1.
  Proof of bDisj. This can be proved by an argument very similar to the proof of eDisj, using (13)
and the right equation of (17).
   Proof of bnAss. This works very similarly to the forward rule. Let witness 𝑊 to be 𝑅;          ¤ h𝑥 :=
any | 𝑦 := anyi and recall 𝑡𝑟𝑢𝑒 is encoded as 1. ¥
   • (WCb) 𝑅;                               ¤ 𝑅;
              ¤ h𝑥 := any | 𝑦 := anyi; 1¥ ≤ 𝑅; ¤ h𝑥 := any | 𝑦 := anyi; 1¥ holds by idempotence of tests.
              ¤
   • (WUb) 𝑅; h𝑥 := any | 𝑦 := anyi; 1 ≤ hhav | 𝑦 := anyi holds by 1¥ identity, hav top, h−] monotonic,
                                        ¥
and 𝑅¤ ≤ 1.¥
   • (WOb) is h𝑥 := any]; 1¥ ≤ [havi; 𝑅;  ¤ h𝑥 := any | 𝑦 := anyi which holds because

            h𝑥 := any]; 1¥
        =   ¥ h𝑥 := any]
            1;
        ≤                ¤ [𝑦 := anyi; h𝑥 := any]
            [𝑦 := anyi; 𝑅;                                                                 ¤ [𝑦 := anyi
                                                         using antecedent 1¥ ≤ [𝑦 := anyi; 𝑅;
        =                ¤ h𝑥 := any | 𝑦 := anyi
            [𝑦 := anyi; 𝑅;
        ≤           ¤ h𝑥 := any | 𝑦 := anyi
            [havi; 𝑅;
9.5.4   Details for Sect. 7.6.
   Proof of Lemma 7.10. Consider the inequality
                                         ¤ ≤ w(h𝑅¤ 8 𝑖𝑑i;
                           ¤ h𝑐 | havi; 𝑖𝑑
                           𝑅;                         ¤ h𝑐 | hav | 𝑑i; h𝑖𝑑
                                                                         ¤ 8 𝑆i)
                                                                             ¤

Observe that by deﬁnitions, we have (for any 𝜎, 𝜎 ′, 𝜎 ′′, 𝜏, 𝜏 ′, 𝜏 ′′ )
                                                    ¤ h𝑐 | hav | 𝑑i; h𝑖𝑑
                            (𝜎, 𝜎 ′, 𝜎 ′′ ) (h𝑅¤ 8 𝑖𝑑i;                ¤ 8 𝑆i)
                                                                           ¤ (𝜏, 𝜏 ′, 𝜏 ′′ )

iﬀ 𝜎𝑅𝜎 ′ ∧ 𝜎 ′ = 𝜎 ′′ ∧ 𝜎𝑐𝜏 ∧ 𝜎 ′′𝑑𝜏 ′′ ∧ 𝜏 = 𝜏 ′ ∧ 𝜏 ′𝑆𝜏 ′′ .
                              ¤ (𝜏, 𝜏 ′) iﬀ 𝜎𝑅𝜎 ′ ∧ 𝜎𝑐𝜏 ∧ 𝜏 = 𝜏 ′ . So the displayed inequality says
                ¤ h𝑐 | havi; 𝑖𝑑)
Also (𝜎, 𝜎 ′ ) (𝑅;
   ∀𝜎, 𝜎 ′, 𝜏, 𝜏 ′ . 𝜎𝑅𝜎 ′ ∧ 𝜎𝑐𝜏 ∧ 𝜏 = 𝜏 ′ ⇒ ∃𝜎 ′′, 𝜏 ′′ . 𝜎𝑅𝜎 ′ ∧ 𝜎 ′ = 𝜎 ′′ ∧ 𝜎𝑐𝜏 ∧ 𝜎 ′′𝑑𝜏 ′′ ∧ 𝜏 = 𝜏 ′ ∧ 𝜏 ′𝑆𝜏 ′′
By the one-point rule of predicate calculus, for 𝜏 ′, this is equivalent to
               ∀𝜎, 𝜎 ′, 𝜏 . 𝜎𝑅𝜎 ′ ∧ 𝜎𝑐𝜏 ⇒ ∃𝜎 ′′, 𝜏 ′′ . 𝜎𝑅𝜎 ′ ∧ 𝜎 ′ = 𝜎 ′′ ∧ 𝜎𝑐𝜏 ∧ 𝜎 ′′𝑑𝜏 ′′ ∧ 𝜏𝑆𝜏 ′′
Using again the one-point rule, for 𝜎 ′′ , this is equivalent to
                        ∀𝜎, 𝜎 ′, 𝜏 . 𝜎𝑅𝜎 ′ ∧ 𝜎𝑐𝜏 ⇒ ∃𝜏 ′′ . 𝜎𝑅𝜎 ′ ∧ 𝜎𝑐𝜏 ∧ 𝜎 ′𝑑𝜏 ′′ ∧ 𝜏𝑆𝜏 ′′
By predicate calculus this is equivalent to
                                 ∀𝜎, 𝜎 ′, 𝜏 . 𝜎𝑅𝜎 ′ ∧ 𝜎𝑐𝜏 ⇒ ∃𝜏 ′′ . 𝜎 ′𝑑𝜏 ′′ ∧ 𝜏𝑆𝜏 ′′
                                          ∃
which is the deﬁnition of 𝑐 | 𝑑 : 𝑅 ≈> 𝑆 (except the identiﬁer 𝜏 ′ is used in (8) rather than 𝜏 ′′ ).
  The proof that (9) is equivalent to (13) is similar.

9.6 Additional Examples for Sect. 7
This section considers additional examples for ∀∃ properties.
9.6.1 Forward Simulation Example 7.6 Using Witness Technique. Consider the following two pro-
grams, where x, t, s, and z range over natural numbers:
                               𝐶1 :    while x>n do x:=x-1 od; t:=any+x; z:=x+t
                               𝐶2 :    s:=any; while x>n do x:=x-1 od; z:=x+s


                                 Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:54   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo

                                      ∃
We want to show 𝐶 1 | 𝐶 2 : 𝑅 ≈> 𝑆, where 𝑅 =
                                            ˆ (x =¥ x ∧ n =¥ n) and 𝑆 =
                                                                      ˆ ( z =¥ z). To do so eﬀectively,
we prophesize the nondeterministic assignment to t in 𝐶 1 . Rewriting:
                             𝐶3 :     p:=any; while x>n do x:=x-1 od; t:=p+x; z:=x+t
                             𝐶 2′ :   s:=any; while x>n do x:=x-1 od; z:=x+s

                         ∃
To show 𝐶 3 | 𝐶 2′ : 𝑅 ≈> 𝑆, we use the witness technique described in Theorem 7.1. Choose witness
𝑊 to be:
                             𝑊 =ˆ hp:=any | s:=anyi; 𝐵; h𝑋 | 𝑋 i ∗ ; h¬𝑒]; h𝑞 | 𝑞 ′ i
where 𝑒 =ˆ [x>n], 𝑋 =
                    ˆ (𝑒; x:=x-1), 𝐵 =                      ˆ t:=p+x; z:=x+t, and 𝑞 ′ =
                                     ˆ [p+min(x,n) =¥ 𝑠], 𝑞 =                         ˆ z:=x+s. There
are three conditions to check.
(WC) [x =¥ x ∧ n =¥ n];𝑊 ≤ [x =¥ x ∧ n =¥ n];𝑊 ; [z =¥ z]
(WU) [x =¥ x ∧ n =¥ n];𝑊 ≤ hhav | 𝐶 2′ i
(WO) [x =¥ x ∧ n =¥ n]; h𝐶 3 ] ≤ 𝑊 ; [havi
Note that the witness does not contain [¬𝑒i. This is a minor technicality that helps shorten the
proof of (WO), allowing us to avoid steps that cancel [¬𝑒i on the right hand side. The ommision is
justiﬁed by the following observation we take as axiom: 𝑅; h¬𝑒 | ¬𝑒i = 𝑅; h¬𝑒]. To prove the above
inequalities, we rely on the following axioms:
  (a) 𝑅; 𝐵 is preserved by h𝑋 | 𝑋 i, i.e., 𝑅; 𝐵; h𝑋 | 𝑋 i = 𝑅; 𝐵; h𝑋 | 𝑋 i; 𝑅; 𝐵.
  (b) 𝑅 is preserved by h𝑋 | 𝑋 i.
  (c) 𝑅; h¬𝑒] = 𝑅; h¬𝑒 | ¬𝑒i and 𝑅; h𝑒] = 𝑅; h𝑒 | 𝑒i
  (d) 𝑅; 𝐵; h¬𝑒 | ¬𝑒i ≤ [x =¥ x]; h¬𝑒]; [p+x =¥ s].
  (e) 1 ≤ [s:=anyi; 𝐵; [s:=anyi which expresses left-totality of 𝐵.
   (f) 𝑅 is preserved by hp:=any | s:=anyi, i.e., 𝑅; hp:=any | s:=anyi = 𝑅; hp:=any | s:=anyi; 𝑅.
  (g) [x =¥ x]; [p+x =¥ s]; ht:=p+x; z:=x+t | z:=x+si ≤ ht:=p+x; z:=x+t | z:=x+si; [z =¥ z].
  (h) x:=e; hav = hav, for any assignment x:=e.
• To prove (WC) start by considering the LHS,
        𝑅; hp:=any | s:=anyi; 𝐵; h𝑋 | 𝑋 i ∗ ; h¬𝑒]; h𝑞 | 𝑞 ′ i
   = 𝑅; hp:=any | s:=anyi; 𝑅; 𝐵; h𝑋 | 𝑋 i ∗ ; h¬𝑒]; h𝑞 | 𝑞 ′ i                       using (f)
   = 𝑅; hp:=any | s:=anyi; 𝑅; 𝐵; h𝑋 | 𝑋 i ∗ ; 𝑅; 𝐵; h¬𝑒]; h𝑞 | 𝑞 ′ i                 using (a) and lemma 9.1
   = 𝑅; hp:=any | s:=anyi; 𝑅; 𝐵; h𝑋 | 𝑋 i ∗ ; 𝑅; 𝐵; h¬𝑒 | ¬𝑒i; h𝑞 | 𝑞 ′ i            using (c)
   ≤ 𝑅; hp:=any | s:=anyi; 𝑅; 𝐵; h𝑋 | 𝑋 i ∗ ; h¬𝑒]; [x =¥ x]; [p+x =¥ s]; h𝑞 | 𝑞 ′ i using (d)
   ≤ 𝑅; hp:=any | s:=anyi; 𝑅; 𝐵; h𝑋 | 𝑋 i ∗ ; h¬𝑒]; h𝑞 | 𝑞 ′ i; [z =¥ z]             using (g)
   ≤ 𝑅; hp:=any | s:=anyi; 𝐵; h𝑋 | 𝑋 i ∗ ; h¬𝑒]; h𝑞 | 𝑞 ′ i; [z =¥ z]                𝑅 below 1
   = 𝑅;𝑊 ; 𝑆
• To prove (WU) we have to show [x =¥ x ∧ n =¥ n];𝑊 ≤ hhav | 𝐶 2′ i. We start by proving a general
lemma about hav: for any 𝑐 and 𝑑,
                                           h𝑐 | 𝑑i ∗ ; hhav] ≤ [𝑑i ∗ ; hhav]
By induction and join, it suﬃces to show: hhav] ≤ [𝑑i ∗ ; hhav] and h𝑐 | 𝑑i; [𝑑i ∗ ; hhav] ≤ [𝑑i ∗ ; hhav].
The former follows from the fact that 1 ≤ 𝑥 ∗ for any 𝑥. The latter:
                             h𝑐 | 𝑑i; [𝑑i ∗ ; hhav] ≤ [𝑑i ∗ ; hhav]
                     ⇔       [𝑑i; h𝑐]; [𝑑i ∗ ; hhav] ≤ [𝑑i ∗ ; hhav]    LRC
                     ⇔       [𝑑i; [𝑑i ∗ ; h𝑐]; hhav] ≤ [𝑑i ∗ ; hhav]    by lemma 9.7
                     ⇐       [𝑑i ∗ ; h𝑐]; hhav] ≤ [𝑑i ∗ ; hhav]         emb homo, 𝑑; 𝑑 ∗ ≤ 𝑑 ∗
                     ⇐       [𝑑i ∗ ; hhav] ≤ [𝑑i ∗ ; hhav]              hav is top

Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                           20:55


and this follows from reﬂexivity. For (WU), we calculate starting from the LHS,
       𝑅; hp:=any | s:=anyi; 𝐵; h𝑋 | 𝑋 i ∗ ; h¬𝑒]; h𝑞 | 𝑞 ′ i
  =    𝑅; hp:=any | s:=anyi; 𝑅; 𝐵; h𝑋 | 𝑋 i ∗ ; 𝑅; 𝐵; h¬𝑒 | ¬𝑒i; h𝑞 | 𝑞 ′ i   using (f), (a), (c), and lemma 9.1
  ≤    hp:=any | s:=anyi; h𝑋 | 𝑋 i ∗ ; h¬𝑒 | ¬𝑒i; h𝑞 | 𝑞 ′ i                  𝑅 and 𝐵 below 1
  ≤    hhav | s:=anyi; h𝑋 | 𝑋 i ∗ ; h¬𝑒 | ¬𝑒i; hhav | 𝑞 ′ i                   hav is top
  ≤    hhav | s:=anyi; h𝑋 | 𝑋 i ∗ ; hhav]; [¬𝑒; 𝑞 ′ i                         hav is top, LRC
  ≤    hhav | s:=anyi; [𝑋 i ∗ ; hhav]; [¬𝑒; 𝑞 ′ i                             using lemma above
  =    hhav]; hhav | s:=anyi; [𝑋 i ∗ ; [¬𝑒; 𝑞 ′ i                             LRC and lemma 9.7
  =    hhav | s:=anyi; [𝑋 i ∗ ; [¬𝑒; 𝑞 ′ i                                    hav = hav; hav
  =    hhav | 𝐶 2′ i                                                          emb homo and defs
• Finally for (WO) we have to show [x =¥ x ∧ n =¥ n]; h𝐶 3 ] ≤ 𝑊 ; [havi. We ﬁrst prove the following
lemma:
                                  𝑅; h𝑋 ] ∗ ≤ 𝑅; h𝑋 | 𝑋 i ∗ ; [havi
This follows from induction and join, provided 𝑅 ≤ 𝑅; h𝑋 | 𝑋 i ∗ ; [havi and 𝑅; h𝑋 | 𝑋 i ∗ ; h𝑋 | havi ≤
𝑅; h𝑋 | 𝑋 i ∗ ; [havi. The ﬁrst inequality is immediate. For the second, we calculate,
             𝑅; h𝑋 | 𝑋 i ∗ ; h𝑋 | havi
        =    𝑅; h𝑋 | 𝑋 i ∗ ; 𝑅; h𝑋 | havi                                      using (b) and lemma 9.1
        =    𝑅; h𝑋 | 𝑋 i ∗ ; 𝑅; h[x > n]; x:=x-1 | havi                        def of 𝑋
        =    𝑅; h𝑋 | 𝑋 i ∗ ; 𝑅; h[x > n]; x:=x-1 | [x > n]; havi               using (c)
        =    𝑅; h𝑋 | 𝑋 i ∗ ; 𝑅; h[x > n]; x:=x-1 | [x > n]; x:=x-1; havi       using (h)
        =    𝑅; h𝑋 | 𝑋 i ∗ ; 𝑅; h[x > n]; x:=x-1 | [x > n]; x:=x-1i[havi       emb homo
        =    𝑅; h𝑋 | 𝑋 i ∗ ; 𝑅; h𝑋 | 𝑋 i; [havi                                def of 𝑋
        ≤    𝑅; h𝑋 | 𝑋 i ∗ ; h𝑋 | 𝑋 i; [havi                                   𝑅 below 1
        ≤    𝑅; h𝑋 | 𝑋 i ∗ ; [havi                                             since 𝑥 ∗ ; 𝑥 ≤ 𝑥 ∗ for any 𝑥
Now for (WO), we start from the LHS,
   𝑅; h𝐶 3 ]
 = 𝑅; hp:=any | 1i; h𝑋 ] ∗ ; h¬𝑒]; h𝑞]                                        unfolding 𝐶 3 and emb homo
 ≤ 𝑅; hp:=any | s:=anyi; 𝐵; [s:=anyi; h𝑋 ] ∗ ; h¬𝑒]; h𝑞]                      using (e)
 ≤ 𝑅; hp:=any | s:=anyi; 𝐵; [havi; h𝑋 ] ∗ ; h¬𝑒]; h𝑞]                         hav is top
 = 𝑅; hp:=any | s:=anyi; 𝐵; h𝑋 ] ∗ ; [havi; h¬𝑒]; h𝑞]                         using lemma 9.7
 = 𝑅; hp:=any | s:=anyi; 𝐵; 𝑅; h𝑋 ] ∗ ; [havi; h¬𝑒]; h𝑞]                      using (f) and commuting 𝑅,𝐵
 ≤ 𝑅; hp:=any | s:=anyi; 𝐵; 𝑅; h𝑋 | 𝑋 i ∗ ; [havi; [havi; h¬𝑒]; h𝑞]           using lemma above
 ≤ 𝑅; hp:=any | s:=anyi; 𝐵; 𝑅; h𝑋 | 𝑋 i ∗ ; h¬𝑒; 𝑞 | havi                     LRC, emb homo, hav; hav = hav
 = 𝑅; hp:=any | s:=anyi; 𝐵; 𝑅; h𝑋 | 𝑋 i ∗ ; h¬𝑒; 𝑞 | 𝑞 ′ ; havi               using (h) which implies 𝑞 ′ ; hav = hav
 = 𝑅; hp:=any | s:=anyi; 𝐵; 𝑅; h𝑋 | 𝑋 i ∗ ; h¬𝑒]; h𝑞 | 𝑞 ′ i; [havi           LRC, emb homo
 ≤ hp:=any | s:=anyi; 𝐵; h𝑋 | 𝑋 i ∗ ; h¬𝑒]; h𝑞 | 𝑞 ′ i; [havi                 𝑅 below 1
 = 𝑊 ; [havi
9.6.2 Forward Simulation Using Deductive Rules. Example. 7.6 describes using the witness tech-
                                                              ∃
nique from Theorem 7.1 to prove 𝐶 3 | 𝐶 2′ : x =¥ x ∧ n =¥ n ≈> z =¥ z. An alternative is to directly apply
the forward simulation proof rules described in Fig. 2. Start by deriving an alignment of 𝐶 3 and
𝐶 2′ :
      hp:=any | s:=anyi; h[x>n]; x:=x-1 | [x>n]; x:=x-1i ∗ ; h¬[x>n] | ¬[x>n]i; ht:=p+x]; hz:=x+t | z:=x+si,
and establishing the following triples:

                                Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:56   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo

                                ∃
  (1) hp:=any | s:=anyi : 𝑅 ≈> 𝐵 ∧ 𝑅, where 𝐵 =     ˆ [p+min(x,n) =¥ s] and 𝑅 =
                                                                              ˆ [x =¥ x ∧ n =¥ n].
                                                           ∃
       From enAss conclude hp:=any | s:=anyi : true ≈> 𝐵. The use of this rule requires proving 𝐵 is
       left total, which it is. Then use the fact that hp:=any | s:=anyi does not modify x or n and so
       preserves 𝑅.
                                                                      ∃
  (2) h[x>n]; x:=x-1 | [x>n]; x:=x-1i ∗ ; h¬[x>n] | ¬[x>n]i : 𝐵 ∧ 𝑅 ≈> 𝐵 ∧ 𝑅 ∧ ¬h[x>n]] ∧ ¬[[x>n]i.
       Follows from an application of eWh. We have to show:
   (2.1) 𝐵 ∧ 𝑅 ⇒ [x>n] =¥ [x>n].
         This holds because 𝑅 implies agreement on x and n.
                                                        ∃
   (2.2) hx:=x-1 | x:=x-1i : 𝐵 ∧ 𝑅 ∧ h[x>n] | [x>n]i ≈> 𝐵 ∧ 𝑅.
         This follows from eAss and eConseq. Note that 𝑅 is clearly preserved by hx:=x-1 | x:=x-1i.
         To reason that 𝐵 is preserved, we rely on the fact that under assumption h[x>n]], the bitest
          [p+min(x,n) =¥ s] is equivalent to the bitest [p+n =¥ s] which is preserved by the loop body.
                                    ∃
  (3) ht:=p+x] : p+x =¥ s ∧ x =¥ x ≈> t =¥ s ∧ x =¥ x.
       This follows from eAss and the fact that t:=p+x does not modify 𝑥.
                                           ∃
  (4) hz:=x+t | z:=x+si : t =¥ s ∧ x =¥ x ≈> z =¥ z.
       This follows from eAss and eConseq.
                                       ∃
  Finally conclude 𝐶 3 | 𝐶 2′ : 𝑅 ≈> 𝑆 by using eSeq and eConseq and the triples described above.
One key step is the use of eConseq when sequencing triples (2) and (3) above: we must show that
𝐵∧𝑅∧¬h[x>n]]∧¬[[x>n]i implies p+x =¥ s. This follows from observing that p+min(x,N) =¥ 𝑠∧¬h[x>n]]
implies p+x =¥ s.
                                                                                     ∃
9.6.3 Backward Simulation Example 7.5. We want to show 𝐶 1 | 𝐶 2 : 𝑅 ≈> 𝑆 where 𝑅 =     ˆ x =¥ x ∧ n =¥ n
      ˆ x =¥ x ∧ n =¥ n ∧ t =¥ s ∧ z =¥ z. We use the the witness technique described in Theorem 7.2.
and 𝑆 =
Take as witness:
                          ˆ [s:=anyi; h𝑋 | 𝑋 i ∗ ; h¬𝑒]; ht:=any+x]; hz:=x+t | z:=x+si; 𝑆
                        𝑊 =
where 𝑒 = ˆ [x>n], and 𝑋 =
                         ˆ 𝑒; x:=x-1. Notice that 𝑊 ends with the postrelation 𝑆. We have three
inequalities to prove,
(WCb) 𝑊 ; 𝑆 ≤ 𝑅;𝑊 ; 𝑆
(WOb) h𝐶 1 ]; 𝑆 ≤ [havi;𝑊
(WUb) 𝑊 ; 𝑆 ≤ hhav | 𝐶 2 i.
   We take the following as axioms:
  (a) hav; x:=e = hav; [x = e] for any primitive assignment x:=e where e does not depend on x,
  (b) x:=e = x:=e; [x = e] where e does not depend on x,
  (c) hav; x:=x-1 = hav, which expresses the fact that x:=x-1 is range total,
  (d) h[z = x+t]]; 𝑆 = h[z = x+t] | [z = x+s]i; 𝑆,
  (e) 𝑅 commutes with hz:=x+t | z:=x+si since 𝑅 does not depend on 𝑧,
   (f) 𝑅 commutes with ht:=any+x] since 𝑅 does not depend on 𝑡,
  (g) 𝑅 commutes with s:=any since 𝑅 does not depend on 𝑠,
  (h) hav; s:=any = hav,
   (i) 𝑅 is backwards preserved by hx:=x-1 | x:=x-1i (i.e., hx:=x-1 | x:=x-1i; 𝑅 = 𝑅; hx:=x-1 | x:=x-1i; 𝑅),
   (j) 𝑅; h𝑒] = 𝑅; h𝑒 | 𝑒i, and 𝑅; h¬𝑒] = 𝑅; h¬𝑒 | ¬𝑒i.
   We also note the following consequences of the axioms above:
  (k) hx:=x-1]; 𝑅 ≤ [havi; hx:=x-1 | x:=x-1i; 𝑅, which follows from (c).
   (l) 𝑅 is backwards preserved by h𝑋 | 𝑋 i, which follows from (i).

Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                           20:57


  (m) ht:=any+x]; hz:=x+t | z:=x+si; 𝑆 = 𝑅; ht:=any+x]; hz:=x+t | z:=x+si; 𝑆, which follows from (e), (f),
      and the fact that 𝑆 contains 𝑅.
• For (WCb), we have to show 𝑊 ; 𝑆 ≤ 𝑅;𝑊 ; 𝑆 which is:

                      [s:=anyi; h𝑋 | 𝑋 i ∗ ; h¬𝑒]; ht:=any+x]; hz:=x+t | z:=x+si; 𝑆 ≤ 𝑅;𝑊 ; 𝑆

. Consider the left hand side. We have,

             [s:=anyi; h𝑋 | 𝑋 i ∗ ; h¬𝑒]; ht:=any+x]; hz:=x+t | z:=x+si; 𝑆
         =   [s:=anyi; h𝑋 | 𝑋 i ∗ ; h¬𝑒]; 𝑅; ht:=any+x]; hz:=x+t | z:=x+si; 𝑆         using (m)
         =   [s:=anyi; h𝑋 | 𝑋 i ∗ ; 𝑅; h¬𝑒]; ht:=any+x]; hz:=x+t | z:=x+si; 𝑆         commute tests
         =   [s:=anyi; 𝑅; h𝑋 | 𝑋 i ∗ ; 𝑅; h¬𝑒]; ht:=any+x]; hz:=x+t | z:=x+si; 𝑆      using (l), lemma 9.2
         =   𝑅; [s:=anyi; h𝑋 | 𝑋 i ∗ ; 𝑅; h¬𝑒]; ht:=any+x]; hz:=x+t | z:=x+si; 𝑆      using (g)
         ≤   𝑅; [s:=anyi; h𝑋 | 𝑋 i ∗ ; h¬𝑒]; ht:=any+x]; hz:=x+t | z:=x+si; 𝑆         𝑅 below 1
         =   𝑅;𝑊 ; 𝑆                                                                  def of 𝑊

• For (WUb), we have to show 𝑊 ; 𝑆 ≤ hhav | 𝐶 2 i which is,

     [s:=anyi; h𝑋 | 𝑋 i ∗ ; h¬𝑒]; ht:=any+x]; hz:=x+t | z:=x+si; 𝑆 ≤ hhav]; [s:=anyi; [𝑋 i ∗ ; [¬𝑒i; [z:=x+si

We start by proving a lemma: h𝑋 | 𝑋 i ∗ ≤ hhav]; [𝑋 i ∗ . By (left) induction and join it suﬃces to
show, 1 ≤ hhav]; [𝑋 i ∗ and h𝑋 | 𝑋 i; hhav]; [𝑋 i ∗ ≤ hhav]; [𝑋 i ∗ . The ﬁrst inequality is immediate.
For the second, consider the left hand side. We have:

                        h𝑋 | 𝑋 i; hhav]; [𝑋 i ∗
                  =     h𝑒 | 𝑒i; hx:=x-1 | x:=x-1i; hhav]; [𝑋 i ∗    def of 𝑋
                  ≤     h𝑒 | 𝑒i; hhav | x:=x-1i; hhav]; [𝑋 i ∗       hav is top
                  ≤     [𝑒i; hhav | x:=x-1i; hhav]; [𝑋 i ∗           𝑒 below 1
                  =     hhav; hav]; [𝑒; x:=x-1i; [𝑋 i ∗              LRC, emb homo
                  =     hhav]; [𝑒; x:=x-1i; [𝑋 i ∗                   hav; hav = hav
                  ≤     hhav]; [𝑋 i ∗                                since 𝑝; 𝑝 ∗ ≤ 𝑝 ∗ for any 𝑝

Now for (WUb), we start from the left hand side and show,

       [s:=anyi; h𝑋 | 𝑋 i ∗ ; h¬𝑒]; ht:=any+x]; hz:=x+t | z:=x+si; 𝑆
 =     [s:=anyi; h𝑋 | 𝑋 i ∗ ; 𝑅; h¬𝑒] ht:=any+x]; hz:=x+t | z:=x+si; 𝑆           using (m) and commuting tests
 =     [s:=anyi; h𝑋 | 𝑋 i ∗ ; 𝑅; h¬𝑒 | ¬𝑒i; ht:=any+x]; hz:=x+t | z:=x+si; 𝑆     using (j)
 ≤     [s:=anyi; h𝑋 | 𝑋 i ∗ ; [¬𝑒i; ht:=any+x; z:=x+t | z:=x+si;                 tests below 1, LRC, emb homo
 ≤     [s:=anyi; h𝑋 | 𝑋 i ∗ ; [¬𝑒i; hhav | z:=x+si                               hav is top
 ≤     [s:=anyi; hhav]; [𝑋 i ∗ ; [¬𝑒i; hhav | z:=x+si                            using lemma above
 ≤     hhav; hav]; [s:=anyi; [𝑋 i ∗ ; [¬𝑒i; [z:=x+si                             LRC, emb homo, LRC over star
 =     hhav]; [s:=anyi; [𝑋 i ∗ ; [¬𝑒i; [z:=x+si                                  hav; hav = hav

• Finally for (WOb), we have to show h𝐶 1 ]; 𝑆 ≤ [havi;𝑊 which is,

  h𝑋 ] ∗ ; h¬𝑒]; ht:=any+x; z:=x+t]; 𝑆 ≤ [havi; [s:=anyi; h𝑋 | 𝑋 i ∗ ; h¬𝑒]; ht:=any+x]; hz:=x+t | z:=x+si; 𝑆

By (left) induction and join there are two cases to consider:
  (n) h¬𝑒]; ht:=any+x; z:=x+t]; 𝑆 ≤ [havi;𝑊 , and
  (o) h𝑋 ]; [havi;𝑊 ≤ [havi;𝑊 .

                                Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:58   Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


   For (n) we start with the right hand side:


                [havi; [s:=anyi; h𝑋 | 𝑋 i ∗ ; h¬𝑒]; ht:=any+x]; hz:=x+t | z:=x+si; 𝑆
        =       [havi; h𝑋 | 𝑋 i ∗ ; h¬𝑒]; ht:=any+x]; hz:=x+t | z:=x+si; 𝑆                using (h)
        ≥       [havi; h¬𝑒]; ht:=any+x]; hz:=x+t | z:=x+si; 𝑆                             since 1 ≤ 𝑥 ∗
        =       h¬𝑒]; ht:=any+x; z:=x+t | hav; z:=x+si; 𝑆                                 LRC, emb homo
        =       h¬𝑒]; ht:=any+x; z:=x+t | hav; [z = x+s]i; 𝑆                              using (a)
        =       h¬𝑒]; ht:=any+x; z:=x+t; [z = x+t] | hav; [z = x+s]i; 𝑆                   using (b)
        =       h¬𝑒]; ht:=any+x; z:=x+t | havi; h[z = x+t] | [z = x+s]i; 𝑆                LRC, emb homo
        ≥       h¬𝑒]; ht:=any+x; z:=x+t | havi; h[z = x+t]]; 𝑆                            using (d)
        =       h¬𝑒]; ht:=any+x | havi; hz:=x+t; [z = x+t]]; 𝑆                            LRC, emb homo
        =       h¬𝑒]; ht:=any+x | havi; hz:=x+t]; 𝑆                                       using (b) in reverse
        ≥       h¬𝑒]; ht:=any+x; z:=x+t]; 𝑆                                               hav is top, emb homo


   Now for (o), (writing 𝑞 for z:=x+t, 𝑞 ′ for z:=x+s, 𝑠 for s:=any, and 𝑡 for t:=any+x)


        h𝑋 | hav; 𝑠i; h𝑋 | 𝑋 i ∗ ; h¬𝑒; 𝑡]; h𝑞 | 𝑞 ′ i; 𝑆 ≤ [hav; 𝑠i; h𝑋 | 𝑋 i ∗ ; h¬𝑒; 𝑡]; h𝑞 | 𝑞 ′ i; 𝑆
 ⇔      h𝑋 | havi; h𝑋 | 𝑋 i ∗ ; h¬𝑒; 𝑡]; h𝑞 | 𝑞 ′ i; 𝑆 ≤ [havi; h𝑋 | 𝑋 i ∗ ; h¬𝑒; 𝑡]; h𝑞 | 𝑞 ′ i; 𝑆         using (h)
 ⇔      h𝑋 | havi; h𝑋 | 𝑋 i ∗ ; h¬𝑒]; 𝑅; h𝑡]; h𝑞 | 𝑞 ′ i; 𝑆 ≤ [havi; h𝑋 | 𝑋 i ∗ ; h¬𝑒; 𝑡]; h𝑞 | 𝑞 ′ i; 𝑆    using (m)
 ⇔      h𝑋 | havi; h𝑋 | 𝑋 i ∗ ; 𝑅; h¬𝑒; 𝑡]; h𝑞 | 𝑞 ′ i; 𝑆 ≤ [havi; h𝑋 | 𝑋 i ∗ ; h¬𝑒; 𝑡]; h𝑞 | 𝑞 ′ i; 𝑆      commute tests
 ⇐      h𝑋 | havi; h𝑋 | 𝑋 i ∗ ; 𝑅 ≤ [havi; h𝑋 | 𝑋 i ∗                                                       monotonicity


   For the left hand side, we show:


                 h𝑋 | havi; h𝑋 | 𝑋 i ∗ ; 𝑅
            =    h𝑒; x:=x-1 | havi; h𝑋 | 𝑋 i ∗ ; 𝑅                         def of 𝑋
            =    h𝑒; x:=x-1 | havi; 𝑅; h𝑋 | 𝑋 i ∗ ; 𝑅                      using (l), lemma 9.2
            =    h𝑒 | havi; hx:=x-1]; 𝑅; h𝑋 | 𝑋 i ∗ ; 𝑅                    LRC, emb homo
            ≤    h𝑒 | havi; [havi; hx:=x-1 | x:=x-1i; 𝑅; h𝑋 | 𝑋 i ∗ ; 𝑅    using (k)
            =    h𝑒 | havi; hx:=x-1 | x:=x-1i; 𝑅; h𝑋 | 𝑋 i ∗ ; 𝑅           using hav; hav = ℎ𝑎𝑣
            =    h𝑒 | havi; 𝑅; hx:=x-1 | x:=x-1i; 𝑅; h𝑋 | 𝑋 i ∗ ; 𝑅        using (i)
            =    [havi; 𝑅; h𝑒; x:=x-1 | x:=x-1i; 𝑅; h𝑋 | 𝑋 i ∗ ; 𝑅         LRC, emb homo, tests commute
            =    [havi; 𝑅; h𝑒; x:=x-1 | 𝑒; x:=x-1i; 𝑅; h𝑋 | 𝑋 i ∗ ; 𝑅      using (j), emb homo
            ≤    [havi; h𝑒; x:=x-1 | 𝑒; x:=x-1i; h𝑋 | 𝑋 i ∗                𝑅 below 1
            ≤    [havi; h𝑋 | 𝑋 i ∗                                         lemma 𝑝; 𝑝 ∗ ≤ 𝑝 ★ for any 𝑝

9.6.4 Example 7.4, ∀∃ Path Alignment. We ﬁrst prove the correctness of each witness 𝑊𝑖 under
the pre-relation 𝑅 = [l =¥ l] and the post-relation 𝑆 = [o =¥ o] then prove the correctness of the
overall witness 𝑊 under the same pre- and post-relation with the disjunction rules.
   We only show the correctness proof of 𝑊2 as an example. The correctness proofs of the other
𝑊𝑖 is similar. Recall that 𝑊2 corresponds to the precondition h > l ∧ h’ ≤ l’ with the chooser
a2’ > l’ ∧ a2’ = l + a1 on the nondeterministic value in the right program.
• (WC) 𝑅;𝑊2 ≤ 𝑅;𝑊2 ; 𝑆

Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                           20:59




                       𝑅;𝑊2
                  =    [l = l’]; ha1:=any; a2:=any | a1’:=any; a2’:=anyi;
                       [h>l; h’<=l’; a2’>l’; a2’=l+a1];
                       ho:=l+a1 | x’:=a2’; o’:=x’i
                  =    [l = l’]; ha1:=any; a2:=any | a1’:=any; a2’:=anyi;
                       [l=l’; h>l; h’<=l’; a2’>l’; a2’=l+a1];                      R is preserved
                       ho:=l+a1 | x’:=a2’; o’:=x’)i
                  ≤    [l = l’]; ha1:=any; a2:=any | a1’:=any; a2’:=anyi;
                       [l=l’; h>l; h’<=l’; a2’>l’; a2’=l+a1];
                       ho:=l+a1 | x’:=a2’; o’:=x’)i[o = o’]
                  =    𝑅;𝑊2 ; 𝑆
Using rule DisjWC in Fig. 6 we can conclude the (WC) proof for the witness 𝑊 from the (WC)
proof of each 𝑊𝑖 .
• (WU) 𝑅;𝑊2 ≤ hhav | 𝑘 2′ i


          𝑅;𝑊2
     =    [l = l’]; ha1:=any; a2:=any | a1’:=any; a2’:=anyi;
          [h>l; h’<=l’; a2’>l’; a2’=l+a1];
          ho:=l+a1 | x’:=a2’; o’:=x’i
     ≤    ha1:=any; a2:=any | a1’:=any; a2’:=anyi;                       tests below 1
          h[h>l]; o:=l+a1 | [h’<=l’; a2’>l’]; x’:=a2’; o’:=x’i
     =    ha1:=any; a2:=any; [h>l]; o:=l+a1 | a1:=any; a2:=any; [h’<=l’; a2’>l’]; x’:=a2’; o’:=x’i
     ≤    hhav | a1:=any; a2:=any; [h’<=l’]; x’:=a2’; [x’>l’]; o’:=x’i
                                                                         emb homo
     =    hhav | 𝑘 2′ i
Similarly, we have the (WU) proofs for the other witnesses
                       𝑅;𝑊1 ≤ hhav | 𝑘 1′ i     𝑅;𝑊3 ≤ hhav | 𝑘 1′ i     𝑅;𝑊4 ≤ hhav | 𝑘 1′ i
                       𝑅;𝑊5 ≤ hhav | 𝑘 2′ i     𝑅;𝑊6 ≤ hhav | 𝑘 3′ i
From the (WU) proof of each 𝑊𝑖 , applying rule DisjWU we have 𝑅; (𝑊1 +𝑊2 +𝑊3 +𝑊4 +𝑊5 +𝑊6 ) ≤
hhav | 𝑘 1′ + 𝑘 2′ + 𝑘 3′ i or equivalently 𝑅;𝑊 ≤ hhav | 𝑘 ′ i .
• (WO)
      𝑅; h𝑘 1 ] ≤ 𝑊2 ; [havi
    ⇐ h𝑘 1 ] ≤ ha1:=any; a2:=any | a1’:=any; a2’:=anyi;                                        by 𝑅 ≤ 1
                   [h>l; h’<=l’; a2’>l’; a2’=l+a1];
                  ho:=l+a1 | x’:=a2’; o’:=x’i; [havi
    ⇐ h𝑘 1 ] ≤ ha1:=any; a2:=any; [h > l]; o:=l+a1];
                   [a1’:=any; a2’:=any;i; [h’<=l’; a2’>l’; a2’=l+a1];
                   [x’:=a2’; o’:=x’i; [havi                                                    emb homo, LRC
    ⇔ h𝑘 1 ] ≤ h𝑘 1 ]; [a1’:=any; a2’:=any;i; [h’<=l’; a2’>l’; a2’=l+a1]; [havi
    ⇐ 1 ≤ [a1’:=any; a2’:=any;i; [h’<=l’; a2’>l’; a2’=l+a1]; [havi                             EnAss
Similarly, we have:
                    𝑅; h𝑘 1 ] ≤ 𝑊1 ; [havi     𝑅; h𝑘 2 ] ≤ 𝑊3 ; [havi     𝑅; h𝑘 3 ] ≤ 𝑊4 ; [havi
                    𝑅; h𝑘 2 ] ≤ 𝑊5 ; [havi     𝑅; h𝑘 3 ] ≤ 𝑊6 ; [havi

                                Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
20:60    Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo


   Applying DisjWO on those proofs, we have 𝑅; h𝑘 1 +𝑘 2 +𝑘 3 ] ≤ (𝑊1 +𝑊2 +𝑊3 +𝑊4 +𝑊5 +𝑊6 ); [havi
or equivalently 𝑅; h𝑘] ≤ 𝑊 ; [havi.

9.7     Additional Alignment Examples
This section considers additional examples from the literature, for ∀∀ properties, showing how
their alignments can be expressed in BiKAT.
  Example 9.15 (Lock-step alignment for strength reduction). Sharma et al.[Sharma et al. 2013] de-
scribe methods for inferring equivalence between loops by observing and correlating executions.
The following exampleis re-produced from their Figure 1.
      int f ( int x , int n ) { int k = 0;                    int ff ( int x , int n ){ int k = 0;
        for (i =0; i != n ; ++ i ) {                            for (i =0; i != n ; ++ i ) {
          x += k *5; k += 1;                                      x += k ; k += 5;
          if ( i >= 5) k += 3;                                    if ( i >= 5) k += 15;
        }                                                       }
        return x ; }                                            return x ; }

This strength-reduction optimization replaces multiplications with additions, improving perfor-
mance. Their algorithm discovers a relational invariant between the aligned loops that i*5 in f is
equal to i<<2+i in ff. This lock-step alignment can be expressed in BiKAT, as follows:
                [x,n,i,k =¥ x,n,i,k];
                (hi!=n | i!=ni; [5i =¥ i<<2 + i]; hf loop body | ff loop bodyi; ) ∗ ; hi=n | i=ni;
                [5i =¥ i<<2 + i]; [x =¥ x]
Here we have, using BiKAT structural rules instead of control-ﬂow graphs, algebraically derived
a proof of the ∀∀ property of the original program, with help from the Sharma et al. technique for
inferring the bitest relational loop invariant [5i =¥ i<<2 + i].
   Example 9.16 (Sequential alignment and memory actions). BiKAT is parametric on the alphabet
of actions and so it is possible to work with other actions such as memory references such as
assignment *x=v and dereference v=*x. Blatteret al.[Blatter et al. 2022] describe a certiﬁed relational
veriﬁcation approach that directly constructs veriﬁcation conditions and avoids self-composition.
They provide an example comparing two implementations of swapping values in memory:
  𝐶1 :     x3=*x1; *x1=*x2; *x2 = x3;                     𝐶2 :    *x1=*x1 + *x2; *x2 = *x1-*x2; *x1=*x1-*x2;

Above 𝐶 1 uses a temporary variable x3, whereas 𝐶 2 uses addition/subtraction. In this case a se-
quential alignment is suﬃcient, with an intermediate relation that relates *x1 on the left with *x2
on the right and vice-versa:
               [*x1,*x2 =¥ *x1,*x2 ]; h𝐶 1 ]; [*x1 =¥ *x2 ∧ *x2 =¥ *x1 ]; [𝐶 2 i; [*x1,*x2 =¥ *x1,*x2 ]
   Example 9.17 (Using relational speciﬁcations). As seen in the previous example, BiKAT permits
one to use speciﬁcations such as procedure pre/post conditions as hypotheses in the logic. The
previous example used a unary speciﬁcation via left/right embedding, but relational speciﬁcations
can also be directly via bitests and equations of the form 𝑃; h𝑚() | 𝑚()i; ¬𝑄
                                                                           ¥ = 0.
   Eilers et al. [Eilers et al. 2018] describe modular product programs (MPP) which has a method for
supporting procedure-level modularity as part of a reduction to reduce 𝑘-safety tasks to problems
for unary solvers such as Viper. A comparison of approaches is given in Section 8; in brief, while
MPP is automated and has full interprocedural support, it is limited to 𝑘-safety of single programs,
limited to lock-step alignment, and does not provide an algebraic way to justify the relationship
with the original program.

Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
An Algebra of Alignment for Relational Verification (Extended Version)                                           20:61


   By contrast, BiKAT can directly incorporate relational speciﬁcations and can express a wider
range of alignment, including the lock-step alignments used in MPPs. For example, the relational
speciﬁcation for the program in their Fig. 1 can be written in BiKAT along with calls as [person =¥
person]; his_female(person) | is_female(person)i; ¬[
                                                   ¥ res =¥ res] = 0, ¥ and the unary speciﬁcation is
written [person > 0]; is_female(person); ¬true = 0, which can be embedded on the left or on the
right. We can then give an algebraically justiﬁed BiKAT alignment for their Fig. 1 main procedure
as follows:
             (hi<people | i<peoplei
                 [i,count,people =¥ i,count,people]
                 hcurrent:=people[i] | current:=people[i]i
                 [current =¥ current] hf:=is_female(current) | f:=is_female(current)i[f =¥ f]
                 hcount := count + f | count := count + fi
                 hi := i + 1 | i := i + 1i) ⊛
             hi>=people | i>=peoplei[count =¥ count]
Above is the lock-step alignment used by MPP, except without the activation variables (see Sec-
tion 8 for a discussion on activation variables). The loops are lock-step aligned, the relational loop
invariant is used, the relational speciﬁcation of is_female is employed, and the loop invariant im-
plies the ﬁnal bitest, which entails that the property holds.

Received 2022-07-07; accepted 2022-11-07




                                Proc. ACM Program. Lang., Vol. 7, No. POPL, Article 20. Publication date: January 2023.
