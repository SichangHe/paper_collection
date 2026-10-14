                                                Deciding Separation Logic with Pointer
                                                 Arithmetic and Inductive Definitions

                                                    Wanyun Su2 , Zhilin Wu2 , and Mihaela Sighireanu1
                                                           1
                                                            State Key Laboratory of Computer Science,
                                                   Institute of Software, Chinese Academy of Sciences, China
                                               2
arXiv:2403.01867v1 [cs.LO] 4 Mar 2024




                                                 LMF, ENS Paris-Saclay, University Paris-Saclay and CNRS, France



                                              Abstract. Pointer arithmetic is widely used in low-level programs, e.g.
                                              memory allocators. The specification of such programs usually requires
                                              using pointer arithmetic inside inductive definitions to define the com-
                                              mon data structures, e.g. heap lists in memory allocators. In this work,
                                              we investigate decision problems for SLAH, a separation logic fragment
                                              that allows pointer arithmetic inside inductive definitions, thus enabling
                                              specification of properties for programs manipulating heap lists. Pointer
                                              arithmetic inside inductive definitions is challenging for automated rea-
                                              soning. We tackle this challenge and achieve decision procedures for both
                                              satisfiability and entailment of SLAH formulas. The crux of our decision
                                              procedure for satisfiability is to compute summaries of inductive defini-
                                              tions. We show that although the summary is naturally expressed as an
                                              existentially quantified non-linear arithmetic formula, it can actually be
                                              transformed into an equivalent linear arithmetic formula. The decision
                                              procedure for entailment, on the other hand, has to match and split the
                                              spatial atoms according to the arithmetic relation between address vari-
                                              ables. We report on the implementation of these decision procedures and
                                              their good performance in solving problems issued from the verification
                                              of building block programs used in memory allocators.


                                        1   Introduction

                                        Context. Separation Logic (SL, [23,22]), an extension of Hoare logic, is a well-
                                        established formalism for the verification of heap manipulating programs. SL
                                        features a separating conjunction operator and inductive predicates, which allow
                                        to express how data structures are laid out in memory in an abstract way. Since
                                        its introduction, various verification tools based on separation logic have been
                                        developed. A notable one among them is the INFER tool [7], which was acquired
                                        by Facebook in 2013 and has been actively used in its development process [8].
                                            Decision procedures for separation logic formulas are vital for the automation
                                        of the verification process. These decision procedures mostly focused on separa-
                                        tion logic fragments called symbolic heaps (SH) [4], since they provide a good
                                        compromise between expressivity and tractability. The SH fragments comprise
                                        existentially quantified formulas that are conjunctions of atoms encoding alias-
                                        ing constraints x = y and x ̸= y between pointers x and y, points-to constraints
2      W. Su, Z. Wu and M. Sighireanu

x 7→ v expressing that at the address x is stored the value v, and predicate
atoms P (⃗x) defining unbounded memory regions of a particular structure. The
points-to and predicate atoms, also called spatial atoms, are composed using the
separating conjunction to specify the disjointness of memory blocks they specify.
    Let us briefly summarize the results on the SH fragments in the sequel. For the
SH fragment with the singly linked list-segment predicate, arguably the simplest
SH fragment, its satisfiability and entailment problems have been shown to be
in PTIME [11] and efficient solvers have been developed for it [2]. The situation
changes for more complex inductive predicates: The satisfiability problem for
the SH fragment with a class of general inductive predicates was shown to be
EXPTIME-complete [5]. On the other hand, the entailment problem for the
SH fragment with slightly less general inductive predicates was shown to be
2-EXPTIME-complete [16,12].
Motivation. Vast majority of the work on the verification of heap manipulating
programs based on SL assumes that the addresses are nominal, that is, they can
be compared with only equality or disequality, but not ordered or obtained by
arithmetic operations. However, pointer arithmetic is widely used in low-level
programs to access data inside memory blocks. Memory allocators are such low-
level programs. They assume that the memory is organized into a linked list of
memory chunks, called heap lists in this paper; pointer arithmetic is used to
jump from a memory chunk to the next one [19,24]. There have been some work
to use separation logic for the static analysis and deductive verification of these
low-level programs [9,21,10]. Moreover, researchers have also started to investi-
gate the decision procedures for separation logic fragments containing pointer
arithmetic. For instance, Array separation logic (ASL) was proposed in [6], which
includes pointer arithmetic, the constraints blk(x, y) denoting a block of memory
units from the address x to y, as well as the points-to constraints x 7→ v. It was
shown in [6] that for ASL, the satisfiability is NP-complete and the entailment is
in coNEXP resp. coNP for quantified resp. quantifier-free formulas. Furthermore,
the decidability can be preserved even if ASL is extended with the list-segment
predicate [18]. Very recently, Le identified in [20] two fragments of ASL extended
with a class of general inductive predicates for which the satisfiability (but not
entailment) problem is decidable.
    Nevertheless, none of the aforementioned work is capable of reasoning about
heap lists, or generally speaking, pointer arithmetic inside inductive definitions,
in a sound and complete way. The state-of-the-art static analysis and verification
tools, e.g. [9,10,21], resort to sound (but incomplete) heuristics or interactive
theorem provers, for reasoning about heap lists. On the other hand, the decision
procedures for ASL or its extensions, e.g. [6,18,20], are unable to tackle heap
lists. This motivates us to raise the following research question: Can decision
procedures be achieved for separation logic fragments allowing pointer arithmetic
inside inductive definitions?
Contribution. In this work, we propose decision procedures for a fragment of
separation logic called SLAH, which allows pointer arithmetic inside inductive
definitions, so that inductive predicates specifying heap lists can be defined.
Deciding Separation Logic with Pointer Arithmetic and Inductive Definitions       3

We consider both satisfiability and entailment problems and show that they
are NP-complete and coNP-complete respectively. The decision procedure for
satisfiability is obtained by computing an equi-satisfiable abstraction in Pres-
burger arithmetic, whose crux is to show that the summaries of the heap list
predicates, which are naturally formalized as existentially quantified non-linear
arithmetic formulas, can actually be transformed into Presburger arithmetic for-
mulas. The decision procedure for entailment, on the other hand, reduces the
problem to multiple instances of an ordered entailment problem, where all the
address terms of spatial atoms are ordered. The ordered entailment problem is
then decided by matching each spatial atom in the consequent to some spatial
formula obtained from the antecedent by partitioning and splitting the spatial
atoms according to the arithmetic relations between address variables. Split-
ting a spatial atom into multiple ones in the antecedent is attributed to pointer
arithmetic and unnecessary for SH fragments with nominal addresses.
    We implemented the decision procedures on top of CompSPEN solver [14].
We evaluate the performance of the new solver, called CompSPEN+ [1], on a
set of formulas originating from path conditions and verification conditions of
programs working on heap lists in memory allocators. We also randomly generate
some formulas, in order to test the scalability of CompSPEN+ further. The
experimental results show that CompSPEN+ is able to solve the satisfiability
and entailment problems for SLAH efficiently (in average, less than 1 second for
satisfiability and less than 15 seconds for entailment).
    To the best of our knowledge, this work presents the first decision proce-
dure and automated solver for decision problems in a separation logic fragment
allowing both pointer arithmetic and memory blocks inside inductive definitions.
Organization. A motivating example and an overview of the decision procedures
are provided in Section 2. The logic SLAH is defined in Section 3. Then the
decision procedures for the satisfiability and entailment problems are presented
in Sections 4 resp. 5. The implementation details and the experimental evaluation
are reported in Section 6.


2   Motivating example and overview

This section illustrates the use of the logic SLAH for the specification of programs
manipulating heap lists and gives an overview of the ingredients used by the
decision procedures we propose.
    Figure 1 presents the motivating example. The function search scans a heap
list between the addresses hbeg (included) and hend (excluded) to find a chunk
of size greater than the one given as parameter. A heap list is a block of memory
divided into chunks, such that each chunk stores its size at its start address.
For readability, we consider that the size counts the number of machine integers
(and not bytes). Scanning the list requires pointer arithmetics to compute the
start address of the next chunk. After the size, the chunk may include additional
information about the chunk in so-called chunk’s header. For readability, we
consider that the header contains only the size information. The data carried
 4         W. Su, Z. Wu and M. Sighireanu


                                          pre ≜ 0 < b < e : hls(b, e)                   (1)
1  int* hbeg; // heap start
 2 int* hend; // heap end              path4-9 ≜ 0 < b < e ∧ b = t ∧ sz0 < rsz          (2)
 3 int* search(int rsz) {
                                               ∧ sz0 = t1 − t ∧ 2 ≤ t1 − t
 4   int* t = hbeg;
 5   while (t < hend) {                        : t 7→ sz0 ∗ blk(t + 1, t1 ) ∗ hls(t1 , e)
 6     int sz = *t;                          I ≜ 0<b<e∧b≤t                              (3)
 7     if (rsz ≤ sz)
 8       return t;                             : hls(b, t; rsz − 1) ∗ hls(t, e)
 9     t = t+sz;
                                   post5-10 (I) ≜ 0 < b < e ∧ b ≤ t0 < e                (4)
10   }
11   return NULL;                              ∧ 2 ≤ sz0 < rsz ∧ t − t0 = sz0
12 }                                           : hls(b, t0 ; rsz − 1) ∗ t0 7→ sz0
                                                 ∗ blk(t0 + 1, t) ∗ hls(t, e)

      Fig. 1. Searching a chunk in a heap list and some of its specifications in SLAH

 by the chunk, called chunk’s body, starts after the chunk header and ends before
 the header of the next chunk.
     The right part of Figure 1 provides several formulas in the logic SLAH defined
 in Section 3. The formula pre specifies the precondition of search, i.e., there is a
 heap list from hbeg to hend represented by the logic variables b resp. e. The pure
 part of pre (left side of ’:’) is a linear constraint on the addresses. The spatial
 part of pre (right side of ’:’) employs the predicate hls defined inductively by
 the last two rules below and for which we define the following shorthand:
       hls(x, y) ≡ hls(x, y; ∞) i.e., no upper bound on chunks’ size, where                 (5)
     hls(x, y; v) ⇐ x = y : emp                                                             (6)
     hls(x, y; v) ⇐ ∃z · 2 ≤ z − x ≤ v : x 7→ z − x ∗ blk(x + 1, z) ∗ hls(z, y; v) (7)
 The inductive definition states that a heap list from x to y is either an empty
 heap if x and y are aliased (Eq. (6)), or a chunk starting at address x and ending
 at address z followed by a heap list from z to y. The chunk stores its size z − x
 in the header (atom x 7→ z − x). The chunk’s body is specified by a memory
 block atom, blk(x + 1, z), starting after the header and ending before the next
 chunk. The parameter v is an upper bound on the size of all chunks in the list.
     The formula path4-9 is generated by the symbolic execution of search start-
 ing from pre and executing the statements from line 4 to 9. It’s satisfiability
 means that the line 9 is reachable from a state satisfying pre.
     The decision procedure for the satisfiability of SLAH in Section 4 is based on
 the translation of a SLAH formula φ into an equi-satisfiable Presburger arith-
 metic (PA) formula φP . The delicate point with respect to the previous work,
 e.g., [18], is to compute a summary in PA for the hls atoms. The summary
 computed for the atom hls(x, y; v) when the heap it denotes is not empty is
 (v = 2 ∧ ∃k · k > 0 ∧ 2k = y − x) ∨ (2 < v ∧ 2 < y − x), i.e., either all chunks have
 size 2 and the heap-list has an even size or v and the size of the heap-list are
 strictly greater than 2. For the empty case, the summary is trivially x = y. The
Deciding Separation Logic with Pointer Arithmetic and Inductive Definitions           5

other spatial atoms a (e.g., x 7→ v and blk(x, y)) are summarized by constraints
on their start address denoted by start(a) (e.g., x) and their end address de-
noted by end(a) (e.g., x + 1 resp. y). For the points-to atom, this constraint is
true, but for the blk(x, y) atom, the constraint is x = start(a) < end(a) = y.
Therefore, the spatial part of path4-9 is translated into the PA formula pbΣ
                                                                           4-9 :


                         t + 1 < t ∧ (t = e ∨ 2 < e − t1 ) .
                         | {z }1 | 1         {z         }
                         blk(t+1,t1 )         hls(t1 ,e)


Alone, pbΣ4-9 does not capture the semantics of the separating conjunction in the
spatial part. For that, we add a set of constraints expressing the disjointness of
memory blocks occupied by the spatial atoms. For our example, these constraints
are pb∗4-9 ≜ t1 < e ≤ t ∨ t + 1 < t1 ≤ e. By conjoining the pure part of
path4-9 with formulas pbΣ 4-9 and pb4-9 , we obtain an equi-satisfiable existentially
                                    ∗

quantified PA formula whose satisfiability is a NP-complete problem.
The PA abstraction is also used to decide the validity of entailments in SLAH in
combination with a matching procedure between spatial parts. To illustrate this
decision procedure presented in Section 5, we consider the verification conditions
generated by the proof of the invariant I from Equation (3) for the search’s loop.
It states that t splits the heap list in two parts. To illustrate a non-trivial case of
the matching procedure used in the decision procedure for entailment, we con-
sider the verification condition (VC) for the inductiveness of I. The antecedent
of the VC is the formula post5-10 (I) in Figure 1, obtained by symbolically ex-
ecuting the path including the statements at lines 5–7 and 9 starting from I.
The PA abstraction of post5-10 (I) is satisfiable and entails the following ordering
constraint on the terms used by the spatial atoms: 0 < b ≤ t0 < t0 + 1 < t ≤ e.
The spatial atoms used in the antecedent and consequent are ordered using the
order given by this contraint as follows:

      antecedent: hls(b, t0 ; rsz − 1) ∗ t0 7→ sz0 ∗ blk(t0 + 1, t) ∗ hls(t, e)
      consequent:                  hls(b, t; rsz − 1)               ∗ hls(t, e)

The matching procedure starts by searching a prefix of the sequence of atoms in
the antecedent that matches the first atom in the consequent, hls(b, t; rsz − 1),
such that the start and end addresses of the sequence are respectively b and t. The
sequence found is hls(b, t0 ; rsz − 1) ∗ t0 7→ sz0 ∗ blk(t0 + 1, t) which also satisfies
the condition (encoded in PA) that it defines a contiguous memory block between
b and t. The algorithm continues by trying to prove the matching found using
a composition lemma hls(b, t0 ; rsz − 1) ∗ hls(t0 , t; rsz − 1) |= hls(b, t; rsz − 1)
and the unfolding of the atom hls(t0 , t; rsz − 1). The PA abstraction of the
antecedent is used to ensure that sz0 is the size of the heap list starting at t0 ,
i.e., sz0 = t − t0 and the constraint 2 ≤ sz0 ≤ rsz − 1 is satisfied. For this
ordering of terms (i.e., 0 < b ≤ t0 < t0 + 1 < t ≤ e), the algorithm is able to
prove the matching. Since this ordering is the only one compatible with the PA
abstraction of the antecedent, we conclude that the entailment is valid.
6         W. Su, Z. Wu and M. Sighireanu

3      SLAH, a separation logic fragment for heap-list
This section defines the syntax and the semantics of the logic SLAH, which
extends array separation logic (ASL) [6] with the hls predicate. Notice that ASL
borrows the structure of formulas from the symbolic heap fragment of SL [4] and
introduces a new spatial atom for memory blocks.

Definition 1 (SLAH Syntax). Let V denote an infinite set of address variables
ranging over N, the set of natural numbers. The syntax of terms t, pure formulas
Π, spatial formulas Σ and symbolic heaps φ is given by the following grammar:

        t ::= x | n | t + t                                                  terms
        Π ::= ⊤ | ⊥ | t = t | t ̸= t | t ≤ t | t < t | Π ∧ Π        pure formulas
        Σ ::= emp | t 7→ t | blk(t, t) | hls(t, t; t∞ ) | Σ ∗ Σ   spatial formulas
        φ ::= ∃⃗z · Π : Σ                                                 formulas

where x and ⃗z are variables resp. set of variables from V, n ∈ N, t∞ is either a
term or ∞, hls is the predicate defined inductively by the rules in Equations (6)
and (7), where v is a variable interpreted over N ∪ {∞}. An atom hls(x, y; ∞)
is also written hls(x, y); Whenever one of Π or Σ is empty, we omit the colon.
We write fv(φ) for the set of free variables occurring in φ. If φ = ∃⃗z · Π : Σ,
we write qf(φ) for Π : Σ, the quantifier-free part of φ. We define start(a) and
end(a) where a is a spatial atom as follows:
    – if a ≡ t1 7→ t2 then start(a) ≜ t1 , end(a) ≜ t1 + 1,
    – if a ≡ blk(t1 , t2 ) then start(a) ≜ t1 and end(a) ≜ t2 ,
    – if a ≡ hls(t1 , t2 ; t3 ) then start(a) ≜ t1 and end(a) ≜ t2 .

    For n, n′ ∈ N such that n ≤ n′ , we use [n, n′ ] to denote the set {n, · · · , n′ }.
Moreover, we use [n] as an abbreviation of [1, n]. We interpret the formulas in
the classic model of separation logic built from a stack s and a heap h. The
stack is a function s : V → N. It is extended to terms, s(t), to denote the
interpretation of terms in the given stack; s(t) is defined by structural induction
on terms: s(n) = n, and s(t + t′ ) = s(t) + s(t′ ). We denote s[x ← n] for a stack
defined as s except for the interpretation of x which is n. Notice that ∞ is used
only to give up the upper bound on the value of the chunk size in the definition
of hls (see Equations (6)–(5)). The heap h is a partial function N ⇀ N. We
denote by dom(h) the domain of a heap h. We use h1 ⊎ h2 to denote the disjoint
union of h1 and h2 , that is, dom(h1 ) ∩ dom(h2 ) = ∅, and for i ∈ {1, 2}, we have
(h1 ⊎ h2 )(n) = hi (n) if n ∈ dom(hi ).

Definition 2 (SLAH Semantics). The satisfaction relation s, h |= φ, where s
is a stack, h a heap, and φ a SLAH formula, is defined by:
    – s, h |= ⊤ always and never s, h |= ⊥,
    – s, h |= t1 ∼ t2 iff s(t1 ) ∼ s(t2 ), where ∼∈ {=, ̸=, ≤, <},
    – s, h |= Π1 ∧ Π2 iff s, h |= Π1 and s, h |= Π2 ,
    – s, h |= emp iff dom(h) = ∅,
Deciding Separation Logic with Pointer Arithmetic and Inductive Definitions         7

 – s, h |= t1 7→ t2 iff ∃n ∈ N s.t. s(t1 ) = n, dom(h) = {n}, and h(n) = s(t2 ),
 – s, h |= blk(t1 , t2 ) iff ∃n, n′ ∈ N s.t. s(t1 ) = n, s(t2 ) = n′ , n < n′ , and
   dom(h) = [n, n′ − 1],
 – s, h |= hls(t1 , t2 ; t3 ) iff ∃k ∈ N s.t. s, h |= hlsk (t1 , t2 ; t3 ),
 – s, h |= hls0 (t1 , t2 ; t∞ ) iff s, h |= t1 = t2 : emp,
 – s, h |= hlsℓ+1 (t1 , t2 ; t∞ ) iff s, h |= ∃z · 2 ≤ z − t1 ∧ Π ′ : t1 7→ z − t1 ∗
   blk(t1 + 1, z) ∗ hlsℓ (z, t2 ; t∞ ), where if t∞ ≡ ∞, then Π ′ ≡ ⊤, otherwise,
   Π ′ ≡ z − t1 ≤ t∞ ,
 – s, h |= Σ1 ∗ Σ2 iff ∃h1 , h2 s.t. h = h1 ⊎ h2 , s, h1 |= Σ1 and s, h2 |= Σ2 ,
 – s, h |= ∃⃗z · Π : Σ iff ∃⃗n ∈ N|⃗z| s.t. s[⃗z ← ⃗n], h |= Π and s[⃗z ← ⃗n], h |= Σ.

    We write A |= B for A and B (sub-)formula in SLAH for A entails B, i.e.,
that for any model (s, h) such that s, h |= A then s, h |= B.
    Notice that the semantics of blk(x, y) differs from the one given in [6] for
array(x, y) because we consider that the location y is the first after the last
location in the memory block, as proposed in [9]. Intuitively, an atom hls(x, y; v)
with v a variable defines a heap lists where all chunks have sizes between 2 and
the value of v. Notice that if v < 2 then the atom hls(x, y; v) has a model
iff x = y. With this semantics, the blk and hls predicates are compositional
predicates [13] and therefore they satisfy the following composition lemmas:

                           blk(x, y) ∗ blk(y, z) |= blk(x, z)                     (8)
                      hls(x, y; v) ∗ hls(y, z; v) |= hls(x, z; v)                 (9)


4     Satisfiability problem of SLAH

The satisfiability problem for an SLAH formula φ is to decide whether there is
a stack s and a heap h such that s, h |= φ. In this section, we propose a deci-
sion procedure for the satisfiability problem, thus showing that the satisfiability
problem is NP-complete.

Theorem 1. The satisfiability problem of SLAH is NP-complete.

The NP lower bound follows from that of ASL in [6]. The NP upper bound is
achieved by encoding the satisfiability problem of SLAH as that of an existentially
quantified Presburger arithmetic formula. The rest of this section is devoted to
the proof of the NP upper bound.
    Presburger arithmetic (PA) is the first-order theory with equality of the sig-
nature ⟨0, 1, +, <, (≡n )n∈N\{0} ⟩ interpreted over the domain of naturals N with
‘+’ interpreted as the addition, ‘<’ interpreted as the order relation, and ≡n
interpreted as the congruence relation modulo n.3 PA is a useful tool for show-
ing complexity classes because its satisfiability problem belongs to various com-
plexity classes depending on the number of quantifier alternations [15]. In this
3
    Although ‘<’ may be encoded using existential quantification in PA over naturals,
    we prefer to keep it in the signature of PA to obtain quantifier free formulas.
8       W. Su, Z. Wu and M. Sighireanu

paper, we consider quantifier-free PA formulas (abbreviated as QFPA) and the
Σ1 -fragment of PA (abbreviated as EPA), which contains existentially quanti-
fied Presburger arithmetic formulas. We recall that the satisfiability problem of
QFPA and EPA is NP-complete.
    We basically follow the same idea as ASL to build a QFPA abstraction of a
SLAH formula φ, denoted by Abs(φ), that encodes its satisfiability:
  – At first, points-to atoms t1 7→ t2 are transformed into blk(t1 , t1 + 1).
  – Then, the block atoms blk(t1 , t2 ) are encoded by the constraint t1 < t2 .
  – The predicate atoms hls(t1 , t2 ; t3 ), absent in ASL, are encoded by a formula
     in QFPA, t1 = t2 ∨ (t1 < t2 ∧ Abs+ (hls(t1 , t2 ; t3 ))).
  – Lastly, the separating conjunction is encoded by an QFPA formula constrain-
     ing the address terms of spatial atoms.
The Appendix A provides more details. The crux of this encoding and its orig-
inality with respect to the ones proposed for ASL in [6] is the computation
of Abs+ (hls(t1 , t2 ; t3 )), which are the least-fixed-point summaries in QFPA for
hls(t1 , t2 ; t3 ). In the sequel, we show how to compute them.
    Intuitively, the abstraction of the predicate atoms hls(t1 , t2 ; t3 ) shall sum-
marize the relation between t1 , t2 and t3 for all k ≥ 1 unfoldings of the predicate
atom. From the fact that the pure constraint in the inductive rule of hls is
2 ≤ x′ − x ≤ v, it is easy to observe that for each k ≥ 1, hlsk (t1 , t2 ; t3 ) can be
encoded by 2k ≤ t2 − t1 ≤ kt3 . It follows that hls(t1 , t2 ; t3 ) can be encoded by
∃k. k ≥ 1 ∧ 2k ≤ t2 − t1 ≤ kt3 . If t3 ≡ ∞, then ∃k. k ≥ 1 ∧ 2k ≤ t2 − t1 ≤ kt3 is
equivalent to ∃k. k ≥ 1 ∧ 2k ≤ t2 − t1 ≡ 2 ≤ t2 − t1 , thus a QFPA formula. Other-
wise, 2k ≤ t2 −t1 ≤ kt3 is a non-linear formula since kt3 is a non-linear term if t3
contains variables. The following lemma states that ∃k. k ≥ 1∧2k ≤ t2 −t1 ≤ kt3
can actually be turned into an equivalent QFPA formula.
Lemma 1 (Summary of hls atoms). Let hls(x, y; z) be an atom in SLAH
representing a non-empty heap, where x, y, z are three distinct variables in
V. We can construct in polynomial time an QFPA formula Abs+ (hls(x, y; z))
which summarizes hls(x, y; z), namely we have for every stack s, s |=
Abs+ (hls(x, y; z)) iff there exists a heap h such that s, h |= hls(x, y, z).
    Since the satisfiability problem of QFPA is NP-complete, the satisfiability
problem of SLAH is in NP. The correctness of Abs(φ) is guaranteed by the
following result.
Proposition 1. A SLAH formula φ is satisfiable iff Abs(φ) is satisfiable.
   From now on, we shall assume that Abs(φ) is a QFPA formula. This enables
using the off-the-shelf SMT solvers, e.g. Z3, to solve the satisfiability problem of
SLAH formulas.

5    Entailment problem of SLAH
We consider the following entailment problem: Given the symbolic heaps φ and
ψ in SLAH such that ψ is quantifier free and fv(ψ) ⊆ fv(φ), decide if φ |= ψ.
Notice that the existential quantifiers in φ, if there is any, can be dropped.
Deciding Separation Logic with Pointer Arithmetic and Inductive Definitions       9

    Our goal in this section is to show that the entailment problem is decidable,
as stated in the following theorem.
Theorem 2. The entailment problem of SLAH is coNP-complete.
The coNP lower bound follows from the fact that the entailment problem of
quantifier-free ASL formulas is also coNP-complete [6]. The remainder of this
section is devoted to the proof of the coNP upper bound.
    In a nutshell, we show in Section 5.1 that the entailment problem φ |= ψ can
be decomposed into a finite number of ordered entailment problems φ′ |=⪯ ψ ′
where all the terms used as start and end addresses of spatial atoms in φ′ and
ψ ′ are ordered by a preorder ⪯. Then, we propose a decision procedure to solve
ordered entailment problems. In Section 5.2, we consider the special case where
the consequent ψ ′ has a unique spatial atom; this part reveals a delicate point
which appears when the consequent and the antecedent are hls atoms because of
the constraint on the chunk sizes. The general case is dealt with in Section 5.3;
the procedure calls the special case for the first atom of the consequent with
all the compatible prefixes of the antecedent, and it does a recursive call for
the remainders of the consequent and the antecedent. Note that to find all the
compatible prefixes of the antecedent, some spatial atoms in the antecedent
might be split into several ones. We derive the coNP upper bound from the
aforementioned decision procedure as follows:
 1. The entailment problem is reduced to at most exponentially many ordered
    entailment problems since there are exponentially many total preorders.
 2. Each ordered entailment problem can be reduced further to exponentially
    many special ordered entailment problems where there is one spatial atom in
    the consequent.
 3. The original entailment problem is invalid iff there is an invalid special or-
    dered entailment problem instance.
 4. The special ordered entailment problem is in coNP.
   In the sequel, we assume that Abs(φ) is satisfiable and Abs(φ) |= Abs(ψ).
Otherwise, the entailment is trivially unsatisfiable.

5.1   Decomposition into ordered entailments
Given the entailment problem φ |= ψ, we denote by A(φ) (and A(ψ)) the set
of terms used as start and end addresses of spatial atoms in φ (resp. ψ). Recall
that a preorder ⪯ over a set A is a reflexive and transitive relation on A. The
preorder ⪯ on A is total if for every a, b ∈ A, either a ⪯ b or b ⪯ a. For a, b ∈ A,
we denote by a ≃ b the fact that a ⪯ b and b ⪯ a, and we use a ≺ b for a ⪯ b
but not b ⪯ a.
Definition 3 (Total preorder compatible with Abs(φ)). Let ⪯ be a total
preorder over A(φ)∪A(ψ). Then ⪯ is said to be compatible with φ if C⪯ ∧Abs(φ)
is satisfiable, where
                      ^                           ^
     C⪯ ≜                      t1 = t2 ∧                      t1 < t2 .  (10)
               t1 ,t2 ∈A(φ)∪A(ψ),t1 ≃t2       t1 ,t2 ∈A(φ)∪A(ψ),t1 ≺t2
10      W. Su, Z. Wu and M. Sighireanu

Example 1. Let φ ≡ blk(x1 , x2 ) ∗ hls(x2 , x3 ; y) and ψ ≡ blk(x1 , x3 ). Then
A(φ) ∪ A(ψ) = {x1 , x2 , x3 }. From Abs(φ) |= x1 < x2 ∧ x2 ≤ x3 , there are two
total preorders compatible with φ, namely, x1 ≺1 x2 ≺1 x3 and x1 ≺2 x2 ≃2 x3 .
Definition 4 (φ |=⪯ ψ). Let ⪯ be a total preorder over A(φ) ∪ A(ψ) that is
compatible with φ. Then we say φ |=⪯ ψ if C⪯ ∧ Π : Σ |= Π ′ : Σ ′ .
Lemma 2. φ |= ψ iff for every total preorder ⪯ over A(φ) ∪ A(ψ) that is
compatible with φ, we have φ |=⪯ ψ.
The proof of the above lemma is immediate. There may be exponentially many
total preorders over A(φ) ∪ A(ψ) that are compatible with φ in the worst case.
   The procedure to decide φ |=⪯ ψ is presented in the rest of this section. We
assume that φ ≡ Π : a1 ∗ · · · ∗ am and ψ ≡ Π ′ : b1 ∗ · · · ∗ bn such that

               C⪯ ∧ Abs(φ) is satisfiable and C⪯ ∧ Abs(φ) |= Abs(ψ).                        (11)

We consider that the atoms hls(t1 , t2 ; t3 ) in φ or ψ such that C⪯ |= t1 =
t2 are removed because they correspond to an empty heap. Moreover, after a
renaming, we assume that the spatial atoms are sorted in each formula, namely,
the following two PA entailments hold:
             ^                             ^
      C⪯ |=       start(ai ) < end(ai ) ∧        end(ai ) ≤ start(ai+1 ), (12)
              i∈[1,m]                             1≤i<m
               ^                                   ^
      C⪯ |=             start(bi ) < end(bi ) ∧           end(bi ) ≤ start(bi+1 ).          (13)
              i∈[1,n]                             1≤i<n

   Section 5.2 considers the special case of a consequent ψ having only one
spatial atom. Section 5.3 considers the general case.

5.2   Consequent with one spatial atom
Consider the ordered entailment φ |=⪯ ψ, where φ ≡ Π : a1 ∗· · ·∗am , ψ ≡ Π ′ : b1
and the constraints (11)–(13) are satisfied. From (11) and the definition of Abs,
we have that C⪯ ∧ Abs(φ) implies Π ′ , so we simplify this entailment to deciding:

                                C⪯ ∧ Π : a1 ∗ · · · ∗ am |=⪯ b1 ,

where, the atoms ai (i ∈ [m]) and b1 represent non-empty heaps, and the start
and end addresses of atoms ai as well as those of b1 are totally ordered by C⪯ .
    Because b1 defines a continuous memory region, the procedure checks the
following necessary condition in PA:
                                                                ^
 C⪯ |= start(a1 ) = start(b1 ) ∧ end(am ) = end(b1 ) ∧                 end(ai ) = start(ai+1 ).
                                                               1≤i<m

 Then, the procedure does a case analysis on the form of b1 . If b1 ≡ t1 7→ t2 then
φ |=⪯ ψ holds iff m = 1 and a1 = t′1 7→ t′2 . If b1 ≡ blk(t1 , t2 ) then φ |=⪯ ψ holds.
For the last case, b1 ≡ hls(t1 , t2 ; t3 ), we distinguish between m = 1 or not.
Deciding Separation Logic with Pointer Arithmetic and Inductive Definitions                  11

One atom in the antecedent: A case analysis on the form of a1 follows.
 a1 ≡ t′1 7→ t′2 Then φ |=⪯ ψ does not hold, since a nonempty heap modeling b1
has to contain at least two memory cells.
 a1 ≡ blk(t′1 , t′2 ) Then the entailment φ |=⪯ ψ does not hold because a memory
block of size t′2 − t′1 where the first memory cell stores the value 1 satisfies
blk(t′1 , t′2 ) but does not satisfy b1 ≡ hls(t1 , t2 ; t3 ) where, by the inductive rule
of hls, t1 7→ z − t1 and 2 ≤ z − t1 ≤ t3 .
 a1 ≡ hls(t′1 , t′2 ; t′3 ) Then the entailment problem seems easy to solve. One may
conjecture that C⪯ ∧Π : hls(t′1 , t′2 ; t′3 ) |= hls(t1 , t2 ; t3 ) iff C⪯ ∧Abs(φ) |= t′3 ≤ t3 ,
which is not the case as a matter of fact, as illustrated by the following example.
(Recall that, from (10) we have that C⪯ ∧ Abs(φ) |= t′1 = t1 ∧ t′2 = t2 .)
Example 2. Consider x < y ∧ y − x = 4 : hls(x, y; 3) |= hls(x, y; 2). The entail-
ment is valid, while we have 3 > 2. The reason behind this seemly counterintu-
itive fact is that when we unfold hls(x, y; 3) to meet the constraint y − x = 4, it
is impossible to have a memory chunk of size 3. (Actually every memory chunk
is of size 2 during the unfolding.)
    We are going to show how to tackle this issue in the sequel.
Definition 5 (Unfolding scheme of a predicate atom and effective up-
per bound). Let φ ≡ Π : hls(t′1 , t′2 ; t′3 ) be an SLAH formula and s : V → N
be a stack such that s |= Abs(φ) and s(t′2 ) − s(t′1 ) ≥ 2. An unfolding scheme of
                                                                                     ′
φ w.r.t. s is a sequence of numbers
                     ′        ′
                                   P (sz1 , · · · , szℓ ) such that 2 ≤ szi ≤ s(t3 ) for
every i ∈ [ℓ] and s(t2 ) = s(t1 ) + i∈[ℓ] szi . Moreover, max(sz1 , · · · , szℓ ) is called
the chunk size upper bound associated with the unfolding scheme. The effective
upper bound of φ w.r.t. s, denoted by EUBφ (s), is defined as the maximum chunk
size upper bound associated with the unfolding schemes of φ w.r.t. s.
Example 3. Let φ ≡ x < y : hls(x, y; 3) and s be a store such that s(x) = 1 and
s(y) = 7. Then there are two unfolding schemes of φ w.r.t. s, namely, (2, 2, 2)
and (3, 3), whose chunk size upper bounds are 2 and 3 respectively. Therefore,
EUBφ (s), the effective upper bound of φ w.r.t. s, is 3.
   The following lemma (proved in the appendix) states that the effective upper
bounds of chunks in heap lists atoms of φ with respect to stacks can be captured
by a QFPA formula.
Lemma 3. For an SLAH formula φ ≡ Π : hls(t′1 , t′2 ; t′3 ), a QFPA formula
ξeub,φ (z) can be constructed in linear time such that for every store s satisfying
s |= Abs(φ), we have s[z ← EUBφ (s)] |= ξeub,φ (z) and s[z ← n] ̸|= ξeub,φ (z) for
all n ̸= EUBφ (s).
    The following lemma (proof in the appendix) provides the correct test used
for the case a1 ≡ hls(t′1 , t′2 ; t′3 ).
Lemma 4. Let φ ≡ Π : hls(t′1 , t′2 ; t′3 ), ψ ≡ hls(t1 , t2 ; t3 ), and ⪯ be a total
preorder over A(φ) ∪ A(ψ) such that C⪯ |= t′1 < t′2 ∧ t′1 = t1 ∧ t′2 = t2 . Then
φ |=⪯ ψ iff C⪯ ∧ Abs(φ) |= ∀z. ξeub,φ (z) → z ≤ t3 .
12       W. Su, Z. Wu and M. Sighireanu

From Lemma 4, it follows that φ ≡ Π : hls(t′1 , t′2 ; t′3 ) |=⪯ hls(t1 , t2 ; t3 ) is invalid
iff C⪯ ∧ Abs(φ) ∧ ∃z. ξeub,φ (z) ∧ ¬z ≤ t3 is satisfiable, which is an EPA formula.
Therefore, this special case of the ordered entailment problem is in coNP.

At least two atoms in the antecedent: Recall that φ ≡ C⪯ ∧Π : a1 ∗· · ·∗am ;
a case analysis on the form of the first atom of the antecedent, a1 , follows.
 a1 ≡ blk(t′1 , t′2 ) Then φ |=⪯ hls(t1 , t2 ; t3 ) does not hold (see case m = 1).
 a1 ≡ hls(t′1 , t′2 ; t′3 ) Then φ |=⪯ hls(t1 , t2 ; t3 ) iff Abs(φ) : hls(t′1 , t′2 ; t′3 ) |=⪯
hls(t1 , t′2 ; t3 ) and Abs(φ) : a2 ∗ · · · ∗ am |=⪯ hls(t′2 , t2 ; t3 ).
 a1 ≡ t′1 7→ t′2 Then the analysis is more involved because we have to check that
t′2 is indeed the size of the first chunk in hls(t1 , t2 ; t3 ) (i.e., satisfies 2 ≤ t′2 ≤ t3 )
and the address t′1 + t′2 , the end of the chunk starting at t′1 = t1 , is the start of
a heap list in the antecedent. The last condition leads to the following cases:
   – t′1 + t′2 is the end of some aj where j ∈ [m] such that t′1 + t′2 = end(aj ) ∧
      C⪯ ∧ Abs(φ) is satisfiable. Then the following entailment shall hold:

      2 ≤ t′2 ≤ t3 ∧ t′1 + t′2 = end(aj ) ∧ Abs(φ) : aj+1 ∗ · · · ∗ am |=⪯ hls(t′1 + t′2 , t2 ; t3 ).

 – t′1 + t′2 is inside a block atom aj : where j ∈ [m] such that aj ≡ blk(t′′1 , t′′2 )
   and t′′1 < t′1 + t′2 < t′′2 ∧ Abs(φ) is satisfiable. Then φ ̸|=⪯ ψ because a block
   atom cannot match the head of a heap list in the consequent.
 – t′1 + t′2 is inside a heap-list atom aj where j ∈ [m] such that aj ≡
   hls(t′′1 , t′′2 ; t′′3 ), t′′1 < t′1 + t′2 < t′′2 ∧ Abs(φ) is satisfiable. Then the follow-
   ing ordered entailment stating that the suffix of the antecedent starting at
   t′1 + t′2 matches the tail of the consequent, shall hold:

           2 ≤ t′2 ≤ t3 ∧ t′′1 < t′1 + t′2 < t′′2 ∧ Abs(φ) :
                    hls(t′1 + t′2 , t′′2 ; t′′3 ) ∗ aj+1 ∗ · · · ∗ am |=⪯ hls(t′1 + t′2 , t2 ; t3 )

     and the following formula, expressing that t′1 + t′2 is inside a block of a
     chunk in aj , shall be unsatisfiable (since otherwise the remaining suffix of
     the antecedent will start by a block atom and cannot match a heap list):

            Abs( t′′1 ≤ x′ < t′1 + t′2 < x′′ ≤ t′′2 ∧ 2 ≤ x′′ − x′ ≤ t′′3 ∧ C⪯ ∧ Π :
                 a1 ∗ · · · ∗ aj−1 ∗ Ufldx′ ,x′′ (hls(t′′1 , t′′2 ; t′′3 )) ∗ aj+1 ∗ · · · ∗ am )

     where x′ , x′′ are two fresh variables and the formula Ufld specifies a splitting
     of aj into a heap list from t′′1 to x′ , a chunk starting at x′ and ending at x′′ ,
     and a heap list starting at x′′ :

               Ufldx′ ,x′′ (hls(t′′1 , t′′2 ; t′′3 )) ≜ hls(t′′1 , x′ ; t′′3 ) ∗ x′ 7→ x′′ − x′ ∗
                                                      blk(x′ + 1, x′′ ) ∗ hls(x′′ , t′′2 ; t′′3 ),

Notice that all j ∈ [m] shall be considered above; if one j satisfying the premises
does not lead to a valid conclusion then the entailment is not valid.
Deciding Separation Logic with Pointer Arithmetic and Inductive Definitions                   13

5.3     Consequent with more spatial atoms

Using the arguments similar to the one given for the case n = 1, we simplify
φ |=⪯ ψ with φ ≡ Π : a1 ∗ · · · ∗ am and ψ ≡ Π ′ : b1 ∗ · · · ∗ bn to:

                         C⪯ ∧ Π : a1 ∗ · · · ∗ am |=⪯ b1 ∗ · · · ∗ bn .

     For n > 1, the decision procedure tries all the possible partitions of the
sequence a1 ∗ · · · ∗ am into a prefix a1 ∗ · · · ∗ a′k to be matched by b1 and a suffix
a′′k ∗ · · · ∗ am to be matched by b2 ∗ · · · ∗ bn , where a′k and a′′k are obtained by
splitting the atom ak . The partition process depends on the relative ordering
of end(b1 ), start(ak ) and end(ak ). Formally, for every k ∈ [m], the procedure
considers all the following cases for which it generates recursive calls to check
the entailments:

    C⪯ ∧ Πk : a1 ∗ · · · ∗ a′k |=⪯ b1 and C⪯ ∧ Πk : a′′k ∗ · · · ∗ am     |=⪯ b2 ∗ · · · ∗ bn ,

where Πk , a′k , a′′k are defined as follows.
 – If end(b1 ) = end(ak ) ∧ C⪯ ∧ Abs(φ) is satisfiable, then a′k ≜ ak , a′′k ≜ emp,
   Πk ≜ end(b1 ) = end(ak ) ∧ Abs(φ).
 – If start(ak ) < end(b1 ) < end(ak ) ∧ C⪯ ∧ Abs(φ) is satisfiable, then a case
   analysis on the form of ak is done to apply the suitable composition lemma:
     • If ak = blk(t′′1 , t′′2 ), then a′k ≜ blk(t′′1 , end(b1 )), a′′k ≜ blk(end(b1 ), t′′2 ),
       and Πk ≜ t′′1 < end(b1 ) < t′′2 ∧ Abs(φ).
     • If ak = hls(t′′1 , t′′2 ; t′′3 ), then we distinguish the following cases:
         ∗ end(b1 ) starts a chunk in ak , that is, a′k ≜ hls(t′′1 , end(b1 ); t′′3 ), a′′k ≜
            hls(end(b1 ), t′′2 ; t′′3 ), and Πk ≜ t′′1 < end(b1 ) < t′′2 ∧ Abs(φ);
         ∗ end(b1 ) splits the body of a chunk in ak starting at some (fresh)
            address x; depending on the position of the chunk in the list (the first,
            the last, in the middle, or the only chunk in the heap list), we obtain
            four cases. This case splitting is due to the fact that the ordered
            entailment problems always assume non-empty hls atoms in the
            formulas. For example, if the chunk starting at x is in the middle of
            the heap list, then a′k ≜ hls(t′′1 , x; t′′3 )∗x 7→ x′ −x∗blk(x+1, end(b1 )),
            a′′k ≜ blk(end(b1 ), x′ ) ∗ hls(x′ , t′′2 ; t′′3 ), and Πk ≜ t′′1 < x < end(b1 ) <
            x′ < t′′2 ∧ Abs(φ), where both x and x′ are fresh variables.


6      Implementation and experiments

Implementation. The decision procedures presented are implemented as an ex-
tension of the CompSPEN solver [14], called CompSPEN+ , available at [1]. Let
us briefly recall some information about CompSPEN. CompSPEN is written
in C++ and includes several decision procedures for symbolic heap fragments
including (i) inductive predicates that are compositional [13] (the predicate
ls(x, y) for list segments is a simple example) and (ii) integer data constraints.
It uses SMT solvers (e.g., Z3) for solving linear integer arithmetic constraints.
14      W. Su, Z. Wu and M. Sighireanu

CompSPEN ranked third among the eleven solvers in the general podium of
the last edition of SL-COMP, the competition of separation-logic solvers [2].
    CompSPEN+ supports the new theory SLAH. Internally, CompSPEN+
parses the input file which shall include the definition of hls and the satisfi-
ability or entailment queries in the SL-COMP format [2].
 – For satisfiability queries, it constructs the EPA abstraction of the SLAH for-
    mulas as shown in Section 4, and queries an SMT solver on its satisfiability.
 – For entailment queries φ |= ψ, CompSPEN+ has to enumerate all the total
    preorders over the set of the start and end addresses of spatial atoms in φ
    and ψ, as described in Section 5. This is time-consuming and a bottleneck for
    the performance. We introduced some heuristics based on the preprocessing
    of the formula to extract preorders between addresses or to decompose the
    entailment on simpler ones (i.e., with less atoms). For instance, we check for
    every block atom b in ψ, whether there is a collection of spatial atoms, say
    ai ∗ ai+1 ∗ · · · ∗ aj with i < j, such that they are contiguous (i.e., the ending
    address of ak is the starting address of ak+1 ), start(b) = start(ai ) and
    end(b) = end(aj ). If this is the case, then we generate the entailment query
    Abs(φ) : ai ∗ ai+1 ∗ · · · ∗ aj |= b and remove all these spatial atoms from φ and
    ψ, thus reducing the original entailment query to a smaller one, for which
    the number of addresses for the total preorder enumeration is decreased.
Benchmarks. We generated 190 benchmarks, available at [3], classified into four
suites, whose sizes are given in Table 1, as follows:
 – MEM-SAT and MEM-ENT are satisfiability resp. entailment problems gen-
   erated by the verification of programs that are building blocks of heap-list
   based memory allocators, including: create a heap-list with one element,
   split a memory chunk into two consecutive memory chunks, join two mem-
   ory chunks, search a memory chunk of size bigger than a given parameter
   (our running example), or search an address inside a heap-list.
 – RANDOM-SAT and RANDOM-ENT are satisfiability resp. entailment prob-
   lems which are randomly or manually generated. Starting from the path and
   verification conditions for programs manipulating heap lists, we replace some
   hls atoms with their unfoldings in order to generate formulas with more
   spatial atoms. RANDOM-SAT includes also formulas where the atoms and
   their start and end address terms are generated randomly. In addition, we
   generate some benchmarks manually. This suite is motivated by testing the
   scalability of CompSPEN+ .

Experiments. We run CompSPEN+ over the four benchmark suites, using a
Ubuntu-16.04 64-bit lap-top with an Intel Core i5-8250U CPU and 2GB RAM.
The experimental results are summarized in Table 1. We set the timeout to 60
seconds. The statistics of average time and maximum time do not include the
time of timeout instances. To the best of our knowledge, there have not been
solvers that are capable of solving the SLAH formulas that include, points-to,
block, and hls atoms. The solver SLar [17] was designed to solve entailment
problems involving points-to, block, and ls atoms. Nevertheless, we are unable
Deciding Separation Logic with Pointer Arithmetic and Inductive Definitions     15

to find a way to access SLar, thus failing to compare with it on ASL formulas.
Moreover, the examples used by SLar, available online, are in a format that
seems nontrivial to translate into the SL-COMP format.

             Table 1. Experimental results, time measured in seconds

    Benchmark suite #instances Timeout Avg. time Min. time Max. time
       MEM-SAT             38         0         0.05       0.03        0.12
     RANDOM-SAT            50         0         0.09       0.02        0.53
        TOTAL              88         0         0.07       0.02        0.53
       MEM-ENT             43         0         3.05       0.34        9.98
    RANDOM-ENT             59         2        13.39       0.04        48.85
        TOTAL             102         2         8.94       0.04        48.85


    As expected, solving entailment instances is more expensive than solving
satisfiability instances. We recall from Section 5 that the procedure for entail-
ment queries satisfiability of several formulas. CompSPEN+ efficiently solves the
benchmark instances originated from program’s verification, namely MEM-SAT
and MEM-ENT, with the average time in 0.05 and 3.05 seconds respectively.
    Table 1 shows that some entailment instances are challenging for Comp-
SPEN+ . For instance, the maximum time in MEM-ENT suite is 9.98, and there
are 2 timeout instances in RANDOM-ENT suite (more than 2 min). By inspect-
ing these challenging instances, we found that (i) they require splitting some spa-
tial atoms (blk or hls) in the antecedent, which is potentially time-consuming,
and (ii) they correspond to valid entailment problems where CompSPEN+ has
to explore all the total preorders, which is time-consuming. We noticed that
when the entailment problem is invalid, the heuristics implemented are able to
quickly find some total preorder under which the entailment does not hold.


7   Conclusion

In this work, we investigated SLAH, a separation logic fragment that allows
pointer arithmetic inside inductive definitions so that the commonly used data
structures e.g. heap lists can be defined. We show that the satisfiability problem
of SLAH is NP-complete and the entailment problem is coNP-complete. We
implemented the decision procedures in a solver, CompSPEN+ , and use it to
efficiently solve more than hundred problems issued from verification of program
manipulating heap lists or randomly generated problems. For future work, it
is interesting to see whether the logic SLAH and its decision procedures can
be extended to specify free lists, another common data structure in memory
allocators [19] in addition to heap lists. Moreover, since bit operations are also
widely used in memory allocators, it would also be interesting to automate the
reasoning about bit operations inside inductive definitions.
16      W. Su, Z. Wu and M. Sighireanu

References
 1. The CompSpen solver, https://github.com/suwy123/compspen2
 2. SL-COMP website, https://sl-comp.github.io/
 3. benchmarks, C.: CompSpen+ benchmarks (2021), https://github.com/suwy123/
    compspen2/tree/master/samples/PAsamples
 4. Berdine, J., Calcagno, C., O’Hearn, P.W.: A decidable fragment of separation logic.
    In: FSTTCS. LNCS, vol. 3328. Springer (2005)
 5. Brotherston, J., Fuhs, C., Pérez, J.A., Gorogiannis, N.: A decision procedure for
    satisfiability in separation logic with inductive predicates. In: CSL-LICS. ACM
    (2014)
 6. Brotherston, J., Gorogiannis, N., Kanovich, M.: Biabduction (and related prob-
    lems) in array separation logic. In: CADE 26. LNCS, vol. 10395. Springer (2017)
 7. Calcagno, C., Distefano, D.: Infer: An automatic program verifier for memory safety
    of C programs. In: NFM. LNCS, vol. 6617. Springer (2011)
 8. Calcagno, C., Distefano, D., Dubreil, J., Gabi, D., Hooimeijer, P., Luca, M.,
    O’Hearn, P.W., Papakonstantinou, I., Purbrick, J., Rodriguez, D.: Moving fast
    with software verification. In: NFM. LNCS, vol. 9058. Springer (2015)
 9. Calcagno, C., Distefano, D., O’Hearn, P.W., Yang, H.: Beyond Reachability: Shape
    Abstraction in the Presence of Pointer Arithmetic. In: SAS. LNCS, vol. 4134.
    Springer (2006)
10. Chlipala, A.: Mostly-automated verification of low-level programs in computational
    separation logic. In: PLDI. ACM (2011)
11. Cook, B., Haase, C., Ouaknine, J., Parkinson, M.J., Worrell, J.: Tractable reasoning
    in a fragment of separation logic. In: CONCUR. LNCS, vol. 6901. Springer (2011)
12. Echenim, M., Iosif, R., Peltier, N.: Entailment checking in separation logic with
    inductive definitions is 2-exptime hard. In: LPAR. EPiCSC, EasyChair (2020)
13. Enea, C., Sighireanu, M., Wu, Z.: On automated lemma generation for separation
    logic with inductive definitions. In: ATVA. LNCS, vol. 9364. Springer (2015)
14. Gu, X., Chen, T., Wu, Z.: A complete decision procedure for linearly compositional
    separation logic with data constraints. In: IJCAR. LNAI, vol. 9706. Springer (2016)
15. Haase, C.: A survival guide to Presburger arithmetic. ACM SIGLOG News 5,
    67–82 (2018), https://dl.acm.org/citation.cfm?id=3242964
16. Katelaan, J., Matheja, C., Zuleger, F.: Effective entailment checking for separation
    logic with inductive definitions. In: TACAS. LNCS, vol. 11428. Springer (2019)
17. Kimura, D., Tatsuta, M.: Decision procedure for entailment of symbolic heaps with
    arrays. In: APLAS. LNCS, vol. 10695. Springer (2017)
18. Kimura, D., Tatsuta, M.: Decidability for entailments of symbolic heaps with ar-
    rays. CoRR arXiv:1802.05935v3 (2018), http://arxiv.org/abs/1802.05935
19. Knuth, D.E.: The Art of Computer Programming, Volume 1 (3rd Ed.): Fundamen-
    tal Algorithms. Addison Wesley Longman Publishing Co., Inc., USA (1997)
20. Le, Q.L.: Compositional satisfiability solving in separation logic. In: VMCAI.
    LNCS, vol. 12597. Springer (2021)
21. Marti, N., Affeldt, R., Yonezawa, A.: Formal verification of the heap manager of
    an operating system using separation logic. In: ICFEM. LNCS, Springer (2006)
22. O’Hearn, P.: Separation logic. Commun. ACM 62(2) (2019)
23. Reynolds, J.: Separation logic: A logic for shared mutable data structures. In: LICS.
    IEEE Computer Society (2002)
24. Wilson, P.R., Johnstone, M.S., Neely, M., Boles, D.: Dynamic storage allocation:
    A survey and critical review. In: IWMM. Springer (1995)
Deciding Separation Logic with Pointer Arithmetic and Inductive Definitions      17

A     QFPA abstraction for SLAH formulas

A.1   QFPA summary of hls atoms

Lemma 1. Let hls(x, y; z) be an atom in SLAH representing a non-empty
heap, where x, y, z are three distinct variables in V. Then there is an QFPA
formula, denoted by Abs+ (hls(x, y; z)), which summarizes hls(x, y; z), namely
for every stack s s |= Abs+ (hls(x, y; z)) iff there exists a heap h such that
s, h |= hls(x, y, z).

Proof. The constraint that the atom represents a non-empty heap means that
the inductive rule defining hls in Equation (7) should be applied at least once.
Notice that the semantics of this rule defines, at each inductive step, a memory
block starting at x and ending before x′ of size x′ − x. By induction on k ≥ 1,
we obtain that hlsk (x, y; z) defines a memory block of length y − x such that
2k ≤ y−x ≤ kz. Then hls(x, y; z) is summarized by the formula ∃k. k ≥ 1∧2k ≤
y − x ≤ kz, which is a non-linear arithmetic formula.
    The formula ∃k. k ≥ 1 ∧ 2k ≤ y − x ≤ kz is actually equivalent to the
disjunction of the two formulas corresponding to the following two cases:

 – If 2 = z, then Abs+ (hls(x, y; z)) has the formula ∃k. k ≥ 1 ∧ y − x = 2k,
   which is equivalent to the QFPA formula 2 ≤ y −x∧y −x ≡2 0, as a disjunct.
 – If 2 < z, then we consider the following sub-cases:
     • if k = 1 then Abs+ (hls(x, y; z)) contains the formula 2 ≤ y − x ≤ z as a
        disjunct;
     • if k ≥ 2, then we observe that the intervals [2k, kz] and [2(k +1), (k +1)z]
        overlap. Indeed,

                          kz − 2(k + 1) = k(z − 2) − 2 ≥ k − 2 ≥ 0.

       Therefore,         [2k, kz] = [4, ∞). It follows that the formula ∃k. k ≥ 2 ∧
                    S
                    k≥2
       2k ≤ y − x ≤ kz is equivalent to 4 ≤ y − x. Therefore, Abs+ (hls(x, y; z))
       contains 4 ≤ y − x as a disjunct.

To sum up, we obtain

         Abs+ (hls(x, y; z)) ≜ 2 = z ∧ ∃k. k ≥ 1 ∧ 2k = y − x
                                                                   
                                                          
                               ∨ 2<z ∧       2≤y−x≤z∨4≤y−x ,

which can be further simplified into

             Abs+ (hls(x, y; z)) ≜ 2 = z ∧ 2 ≤ y − x ∧ y − x ≡2 0
                                                                       
                                                    
                                 ∨ 2<z∧2≤y−x .

                                                                                  ⊔
                                                                                  ⊓
18     W. Su, Z. Wu and M. Sighireanu

A.2   Abs(φ): The QFPA abstraction of φ
We utilize Abs+ (hls(x, y; z)) to obtain in polynomial time an equi-satisfiable
QFPA abstraction for a symbolic heap φ, denoted by Abs(φ).
   We introduce some notations first. Given a formula φ ≡ Π : Σ, Atoms(φ)
denotes the set of spatial atoms in Σ, and PAtoms(φ) denotes the set of predicate
atoms in Σ.

Definition 6. (Presburger abstraction of SLAH formula) Let φ ≡ Π : Σ be a
SLAH formula. The abstraction of φ ≡ Π : Σ, denoted by Abs(φ) is the formula
Π ∧ ϕΣ ∧ ϕ∗ where:
            V
 – ϕΣ ≜           Abs(a) such that
          a∈Atoms(φ)

                  Abs(t1 7→ t2 ) ≜ true                                                       (14)
             Abs(blk(t1 , t2 )) ≜ t1 < t2                                                     (15)
          Abs(hls(t1 , t2 , t3 )) ≜ t1 = t2                                                   (16)
                                    ∨ (t1 < t2 ∧ Abs+ (hls(x, y; z))[t1 /x, t2 /y, t3 /z]).   (17)

 – ϕ∗ ≜ ϕ1 ∧ ϕ2 ∧ ϕ3 specifies the semantics of separating conjunction, where
                         ^
         ϕ1 ≜                            (isNonEmpai ∧ isNonEmpaj ) →                      (18)
                ai ,aj ∈PAtoms(φ),i<j      (end(aj ) ≤ start(ai ) ∨ end(ai ) ≤ start(aj ))
                         ^
         ϕ2 ≜                            (isNonEmpai ) →                                      (19)
                ai ∈PAtoms,aj ̸∈PAtoms     (end(aj ) ≤ start(ai ) ∨ end(ai ) ≤ start(aj ))
                         ^
         ϕ3 ≜                            end(aj ) ≤ start(ai ) ∨ end(ai ) ≤ start(aj )        (20)
                ai ,aj ̸∈PAtoms(φ),i<j


and for each spatial atom ai , isNonEmpai is an abbreviation of the formula
start(ai ) < end(ai ).

   For formulas φ ≡ ∃⃗z · Π : Σ, we define Abs(φ) ≜ Abs(Π : Σ) since ∃⃗z · Π : Σ
and Π : Σ are equi-satisfiable.

Proposition 1. A SLAH formula φ is satisfiable iff Abs(φ) is satisfiable.

Proof. “Only if ” direction: Suppose that φ is satisfiable.
     Then there exists a stack s and a heap h such that s, h |= φ. We show
s |= Abs(φ). The semantics of SLAH implies that at least one disjunct in Abs(a)
is true for every predicate atom a. Therefore, s |= ϕΣ . Moreover, s |= ϕ∗ , as a
result of the semantics of separating conjunction. Thus s |= Abs(φ) and Abs(φ)
is satisfiable.
“If ” direction: Suppose that Abs(φ) is satisfiable.
     Then there is an interpretation s such that s |= Abs(φ). We build a heap h
from s and φ as follows:
 – For each points-to atom t1 7→ t2 in φ, h(s(t1 )) = s(t2 ).
Deciding Separation Logic with Pointer Arithmetic and Inductive Definitions           19

 – For each block atom blk(t1 , t2 ) in φ, h(n) = 1 for each n ∈ [s(t1 ), s(t2 ) − 1].
 – For every predicate atom hls(t1 , t2 ; t3 ) in φ, we have s |=
   Abs(hls(t1 , t2 ; t3 )). Then either s(t1 ) = s(t2 ) or s(t1 ) < s(t2 ) and
   s |= Abs+ (hls(x, y; z))[t1 /x, t2 /y, t3 /z].
     • For the first case, we let h(s(t1 )) undefined.
     • For the second case, s |= (2 = t3 ∧ t1 < t2 ∧ t2 − t1 ≡ 0 mod 2) ∨ (2 <
       t3 ∧ 2 ≤ t2 − t1 ).
         ∗ If s(t3 ) = 2, then let h(s(t1 ) + 2(i − 1)) = 2 and h(s(t1 ) + 2i − 1) = 1
           for every i : 1 ≤ i ≤ s(t2 )−s(t
                                        2
                                             1)
                                                .
         ∗ If s(t3 ) > 2, then from s(t2 ) − s(t1 ) ≥ 2, we know that there is a
           sequence of numbers n1 , · ·P   · , nℓ such that 2 ≤ ni ≤ s(t3 )Pfor every
           i ∈ [ℓ] and s(t2 ) = s(t1 ) +        ni . We then let h(s(t1 ) +      nj ) =
                                          i∈[ℓ]                            j∈[i−1]
             ni for every i ∈ [ℓ], and let h(n′ ) = 1 for all the other addresses
             n′ ∈ [s(t1 ), s(t2 ) − 1].
        From the construction above, we know that the subheap of the domain
        [s(t1 ), s(t2 ) − 1] satisfies hls(t1 , t2 ; t3 ).

From the definition of h, we know that s, h |= φ. Therefore, φ is satisfiable.         ⊔
                                                                                       ⊓

Remark 1. From the definition of Abs(φ), it follows that Abs(φ) is in QFPA and
the size of Abs(φ) is polynomial in that of φ. From the fact that the satisfiability
of QFPA is in NP, we conclude that the satisfiability of SLAH is in NP.


B    Proof of Lemma 3

Lemma 3. For an SLAH formula φ ≡ Π : hls(t′1 , t′2 ; t′3 ), a QFPA formula
ξeub,φ (z) can be constructed in linear time such that for every store s satisfying
s |= Abs(φ), we have s[z ← EUBφ (s)] |= ξeub,φ (z) and s[z ← n] ̸|= ξeub,φ (z) for
all n ̸= EUBφ (s).

Proof. From the construction of Abs+ (hls(t′1 , t′2 ; t′3 )) in Section 4, we know that
for every store s, there is a heap h such that s, h |= Π : hls(t′1 , t′2; t′3 ) iff s |=
Π ∧ (t′3 = 2 ∧ 2 ≤ t′2 − t′1 ∧ t′2 − t′1 ≡2 0) ∨ (2 < t′3 ∧ 2 ≤ t′2 − t′1 ) . Then the
fact that z appears in some unfolding scheme of φ w.r.t. some store s can be
specified by the formula
              ′
               (t3 = 2 ∧ z = 2 ∧ 2 ≤ t′2 − t′1 ∧ t′2 − t′1 ≡2 0) ∨
                                                                             
         Π∧                                                                    ,
               (2 < t′3 ∧ 2 ≤ z ≤ t′3 ∧ (2 ≤ t′2 − t′1 − z ∨ t′2 − t′1 = z))

where t′2 −t′1 −z denotes the remaining size of the heap after removing a memory
chunk of size z. Therefore, we define ξeub,φ (z) as
            ′                            ′   ′     ′     ′
                                                                                     
               3 = 2 ′∧ z = 2 ∧ 2 ≤′ t2 − t1 ∧′ t2 −′ t1 ≡2 0)′ ∨ ′
               (t                                                                  
     Π ∧  2 < t3 ∧ 2 ≤ z ≤ t3 ∧ (2 ≤ t2 − t1 − z ∨ t2 − t1 = z) ∧  ,
                  ∀z ′ . z < z ′ ≤ t′3 → ¬(2 ≤ t′2 − t′1 − z ′ ∨ t′2 − t′1 = z ′ )
20      W. Su, Z. Wu and M. Sighireanu

where ∀z ′ . z < z ′ ≤ t′3 → ¬(2 ≤ t′2 − t′1 − z ′ ∨ t′2 − t′1 = z ′ ) asserts that z
is the maximum chunk size upper bound among unfolding schemes of φ. The
formula ∀z ′ . z < z ′ ≤ t′3 → ¬(2 ≤ t′2 − t′1 − z ′ ∨ t′2 − t′1 = z ′ ) is equivalent to
∀z ′ . z < z ′ ≤ t′3 → (t′2 − t′1 − z ′ ≤ 1 ∧ t′2 − t′1 ̸= z ′ ), and can be simplified into

                 z + 1 ≤ t′3 → (t′2 − t′1 ≤ z + 2 ∧ t′2 − t′1 ̸= z + 1) ∧
                 z + 2 ≤ t′3 → t′2 − t′1 ̸= z + 2,

where t′2 − t′1 ̸= z + 1 is an abbreviation of t′2 − t′1 < z + 1 ∨ z + 1 < t′2 − t′1 ,
similarly for t′2 − t′1 ̸= z + 2.
   It follows that ξeub,φ (z) can be simplified into
            ′                          ′     ′   ′    ′
                                                                          
              3 = 2 ′∧ z = 2 ∧ 2 ≤′ t2 − t1 ∧′ t2 −′ t1 ≡2 0)′ ∨ ′
              (t                                                        
            2 < t3 ∧ 2 ≤ z ≤ t3 ∧ (2 ≤ t2 − t1 − z ∨ t2 − t1 = z) ∧ 
      Π ∧   z + 1 ≤ t′3 → (t′2 − t′1 ≤ z + 2 ∧ t′2 − t′1 ̸= z + 1) ∧ ,
                                                                          

                 z + 2 ≤ t′3 → t′2 − t′1 ̸= z + 2
which is a QFPA formula.                                                                    ⊔
                                                                                            ⊓


C     Proof of Lemma 4
Lemma 4 Let φ ≡ Π : hls(t′1 , t′2 ; t′3 ), ψ ≡ hls(t1 , t2 ; t3 ), and ⪯ be a total
preorder over A(φ) ∪ A(ψ) such that C⪯ |= t′1 < t′2 ∧ t′1 = t1 ∧ t′2 = t2 . Then
φ |=⪯ ψ iff C⪯ ∧ Abs(φ) |= ∀z. ξeub,φ (z) → z ≤ t3 .

Proof. “Only if ” direction: Suppose φ |=⪯ ψ.
    At first, we observe that C⪯ ∧ Abs(φ) and φ contain the same number of
variables.
    Let s be an interpretation such that s |= C⪯ ∧ Abs(φ). From C⪯ |= t′1 <
t2 ∧ t′1 = t1 ∧ t′2 = t2 , we have s(t′1 ) < s(t′2 ), s(t′1 ) = s(t1 ), and s(t′2 ) = s(t2 ).
 ′

    At first, from s |= Abs(φ) and Lemma 3, we deduce that s[z → EUBφ (s)] |=
ξeub,φ (z). Moreover, from the definition of EUBφ (s), we know that there is an
unfolding scheme, say sz1 , · · · , szℓ , such that EUBφ (s) = max(sz1 , · · · , szℓ ). From
the definition of unfoldingP schemes, we have 2 ≤ szi ≤ s(t3 ) for every i ∈ [ℓ]
                                                                          ′

and s(t2 ) = s(t1 ) +
         ′          ′
                                szi . Therefore, there is a heap h such that s, h |= φ
                          i∈[ℓ]
and for every i ∈ [ℓ], h(s(t′1 ) +           szj ) = szi . From the assumption φ |=⪯ ψ,
                                        P
                                    j∈[i−1]
we deduce that s, h |= ψ ≡ hls(t1 , t2 ; t3 ). Then each chunk of h has to be
matched exactly to one unfolding of hls(t1 , t2 ; t3 ). Thus, 2 ≤ szi ≤ s(t3 ) for
every i ∈ [ℓ]. Therefore, EUBφ (s) = max(sz1 , · · · , szℓ ) ≤ s(t3 ). We deduce that
s[z ← EUBφ (s)] |= ξeub,φ (z) ∧ z ≤ t3 . Moreover, from Lemma 3, we know that for
all n ̸= EUBφ (s), s[z ← n] ̸|= ξeub,φ (z). Consequently, s |= ∀z. ξeub,φ (z) → z ≤ t3 .
“If ” direction: Suppose C⪯ ∧Abs(φ) |= ∀z. ξeub,φ (z) → z ≤ t3 and s, h |= C⪯ ∧Π :
hls(t′1 , t′2 ; t′3 ). We show s, h |= ψ.
     From s, h |= C⪯ ∧Π : hls(t′1 , t′2 ; t′3 ), we know that there are sz1 , · · · , szℓ such
that they are the sequence of chunk sizes in h. Therefore, (sz1 , · · · , szℓ ) is an
Deciding Separation Logic with Pointer Arithmetic and Inductive Definitions         21

unfolding scheme of φ w.r.t. s. From the definition of EUBφ (s), we have EUBφ (s)
is the maximum chunk size upper bound of the unfolding schemes of φ w.r.t. s.
Therefore, max(sz1 , · · · , szℓ ) ≤ EUBφ (s).
    From s, h |= C⪯ ∧Π : hls(t′1 , t′2 ; t′3 ), we deduce that s |= C⪯ ∧Abs(φ). Because
C⪯ ∧Abs(φ) |= ∀z. ξeub,φ (z) → z ≤ t3 , we have s |= ∀z. ξeub,φ (z) → z ≤ t3 . From
Lemma 3, we know that s[z ← EUBφ (s)] |= ξeub,φ (z). Therefore, we deduce that
s[z ← EUBφ (s)] |= z ≤ t3 , namely, EUBφ (s) ≤ s(t3 ). Then max(sz1 , · · · , szℓ ) ≤
EUBφ (s) ≤ s(t3 ). It follows that for every i ∈ [ℓ], 2 ≤ szi ≤ s(t3 ). We conclude
that s, h |= hls(t1 , t2 ; t3 ) ≡ ψ.                                                 ⊔
                                                                                     ⊓


D    Complexity of the entailment problem
Theorem 2 states that the upper bound of the entailment problem is EXP-
TIME. The lower bound is given by the complexity of the entailment problem
for quantifier free formulas in ASL, which is shown to be coNP in [6].
    Claim: The entailment problem in SLAH is in coNP.

Proof. Let fix φ |= ψ an entailment problem in SLAH.
    We build in polynomial time a PA formula χ from φ and ψ such that for any
stack s, s |= χ iff ∃h. s, h |= φ and s, h ̸|= ψ.
    We suppose that both formula φ and ψ have been transformed in normal
form as follows:
 – atoms hls(x, y; v ′ ) with Abs(φ) |= (v ′ < 2 ∨ x = y) have been removed and
   replaced by x = y                                                                      M: use ξ ?
 – atoms hls(x, y; v ′ ) with Abs(φ) |= y − x = 2 ∧ v ′ ≥ 2 have been replaced by
   ∃z. z ≤ v ′ ∧ y − x = 2 : x 7→ z ⋆ blk(x + 1, y)
 – ...                                                                                    M: TODO

The normalization can be done in a linear number of calls to the EPA procedure.
   The formula χ shall ensure that φ is satisfiable, so it contains as conjunct
Abs(φ).
   The entailment may be invalid iff one of the following holds:
 1. ψ is not satisfiable, i.e., Abs(ψ) is not satisfiable.
 2. there exists an address inside a spatial atom of φ which is not inside a spatial
    atom of ψ; we denote this formula by cov(φ, ψ);
 3. similarly, cov(ψ, φ) (the semantics is non intuitionistic),
 4. a points-to or a heap-list atom of ψ “covers” a domain of addresses which is
    inside the one of a block atom of φ; we denote this formula by nblk(φ, ψ);
 5. a points-to atom of ψ defines an address inside (strictly) a heap-list atom of
    φ; we denote this formula by npto(φ, ψ);
 6. a points-to atom x 7→ v of ψ defines the same address as the start address
    of a heap-list atom hls(x, y; v ′ ) in φ; we denote this formula by npto′ (φ, ψ);
    (this is true because we are in the normal form);
 7. a points-to atoms x 7→ v of ψ defines the same address as a points-to atom
    x 7→ v ′ of φ but v ̸= v ′ ;
                     22      W. Su, Z. Wu and M. Sighireanu

                      8. a heap-list atom hls(x, y; v ′ ) of ψ starts at an address at which is defined a
                         points-to atom x 7→ v of φ such that v > v ′ ;
                      9. a heap-list atom hls(x, y; v ′ ) of ψ “covers” the domain of addresses if an
                         atom hls(z, w; v) of φ but v ′ < v;
                     10. a heap-list atom hls(x, y; v ′ ) of ψ “covers” a domain of addresses that can
                         not be filded into a hls atom with chunks of maximal size less or equal to
M: difficult in P!       v′
