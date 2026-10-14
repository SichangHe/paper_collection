        Lagrangian-Based Duality for Quantified
                   SMT Algorithms

 Ivana Bocevska1(B) , Takeshi Tsukada2 , Hiroshi Unno3 , Oded Padon4 ,
                          and Sharon Shoham5
                               1
                                 TU Wien, Vienna, Austria
                              ivana.bocevska@tuwien.ac.at
                            2
                               Chiba University, Chiba, Japan
                                   t.tsukada@acm.org
                          3
                              Tohoku University, Sendai, Japan
                                 hiroshi.unno@acm.org
                    4
                      Weizmann Institute of Science, Rehovot, Israel
                               oded.padon@weizmann.ac.il
                        5
                            Tel Aviv University, Tel Aviv, Israel


       Abstract. Lagrangian-based duality, traditionally applied in optimiza-
       tion, has recently been generalized to serve as the basis for a unifying
       framework for primal-dual search algorithms in the context of program
       veriﬁcation and automated reasoning. In this paper, we analyze Quanti-
       ﬁed Satisﬁability Modulo Theories (QSMT) algorithms using this frame-
       work. Interestingly, our Lagrangian-based analysis reveals that three
       recently proposed algorithms for quantiﬁed linear real arithmetic (LRA)
       share a common structure, and that their main diﬀerences lie in the
       approach to a certain problem—model-based projection for .∃∀-formulas.
       Moreover, in the course of this Lagrangian-based analysis, we identify an
       issue with the progress property of one of the algorithms, propose a way
       to ﬁx the issue, and experimentally demonstrate that the proposed ﬁx
       improves performance.

       Keywords: Lagrangian-based duality · quantiﬁed SMT


1    Intro duction

 Lagrangian-based duality is a central concept in optimization, where a Lagrangian
 is used to derive a primal problem and a dual problem such that the optimal value
 of the primal problem is bounded by (the value of) any feasible solution of the
 dual problem. Algorithms for solving the induced problems leverage this corre-
 spondence by letting the two searches interact and guide each other.
     A similar interaction between the search for proofs and the search for refu-
 tations or counterexamples is prevalent in prominent veriﬁcation and auto-
 mated reasoning algorithms; Tsukada et al. [21] have generalized the notion
 of a Lagrangian to capture this. A Lagrangian in that context is a function
.L : X × Y → {−1, +1}, where .X denotes candidate refutations and .Y denotes

 c The Author(s) 2026
E. Darulova et al. (Eds.): CAV 2026, LNCS 16683, pp. 75–96, 2026.
https://doi.org/10.1007/978-3-032-32526-6_4
76      I. Bocevska et al.

 candidate proofs.1 The Lagrangian assigns a value .−1 or .+1 to each pair of
 a candidate refutation .x ∈ X and a candidate proof .y ∈ Y , indicating which
 of the two dominates the other (.+1 if the proof candidate is better). More-
 over, if .supy inf x L(x, y) = +1 then a proof exists; and if .inf x supy L(x, y) =
 −1 then a refutation exists. In other words, ﬁnding a refutation corresponds
 to ﬁnding a witness .x∗ ∈ X such that .supy L(x∗ , y) = −1 (showing that
.inf x supy L(x, y) = −1), which we call the primal problem. Similarly, ﬁnding
 a proof corresponds to ﬁnding a witness .y ∗ ∈ Y such that .inf x L(x, y ∗ ) = +1
 (showing that .supy inf x L(x, y) = +1), which we call the dual problem. In [21] an
 abstract primal-dual procedure is presented for solving the two problems for a
 given Lagrangian, where candidate witnesses for each problem guide the search
 for candidate witnesses for the other problem: for a pair .(α, β) ∈ X × Y of the
 current proof candidate and refutation candidate, when .L(α, β) = −1, the prover
 tries to update .β to .β so that .L(α, β ) = 1, and vice versa, when .L(α, β) = 1
 the refuter tries to update .α to .α such that .L(α , β) = −1. It is shown that
 prominent veriﬁcation procedures, such as counterexample-guided abstraction-
 reﬁnement (CEGAR) [1,9] and ICE learning [12], can be viewed as instances of
 the primal-dual procedure with suitably-deﬁned Lagrangians. The Lagrangian-
 based framework also provides a uniﬁed way to reason about progress of the
 procedures that it captures.
      In this paper we investigate algorithms for solving the Quantiﬁed Satisﬁabil-
 ity Modulo Theories (QSMT) problem from the Lagrangian-based perspective.
 QSMT is an important problem in automated reasoning, with numerous appli-
 cations in veriﬁcation and synthesis. In QSMT, the input is a closed quantiﬁed
 formula .Φ over the theory .T of some structure, e.g., Linear Integer Arithmetic
 (LIA) or Linear Real Arithmetic (LRA), and the goal is to check whether .T |= Φ
 or .T |= ¬Φ. Many algorithms have been proposed in the literature for address-
 ing QSMT. We focus on three algorithms proposed recently, namely QSAT by
 Bjørner and Janota [2], QSMA by Bonacina et al. [5] and SynSAT by Murphy
 and Kincaid [18].
      These algorithms seem very diﬀerent from each other. For example, Syn-
 SAT [18] addresses the problem as a game between an .∃ player and a .∀ player,
 and solves the problem by recursively computing a winning strategy skeleton for
 one of the players. In QSAT [2], a sequence of frames that matches the formula’s
 quantiﬁer preﬁx is constructed, and the frames are incrementally strengthened
 using model-based projection [15,16] in a manner similar to IC3/PDR [7,10].
 Similar sequences appear in QSMA [5], but it manages two sequences consisting
 of over- and under-approximations and uses an interpolating theorem prover2 in
 addition to model-based pro jection. These algorithms also diﬀer qualitatively:
 for instance, SynSAT [18] relies on stronger assumptions about the background
 theory than the others (see [11, Sect. 6]), and termination of QSMA [5] is not
 guaranteed if one uses a standard interpolating theorem prover.

 1
   The original formulation [21] allows the range of the Lagrangian to be any totally-
   ordered complete lattice, but for our discussion it suﬃces to consider .{−1, +1}.
 2
   More precisely, a model-based over-approximation procedure in their terminology.
                  Lagrangian-Based Duality for Quantiﬁed SMT Algorithms          77

     We show that despite their signiﬁcant diﬀerences, these algorithms can be
 captured by a uniﬁed Lagrangian. To that end, we ﬁrst generalize the primal-
 dual procedure from [21] to a recursive one, allowing the procedures for checking
 candidate witnesses of the primal/dual problem to themselves be instances of the
 primal-dual procedure with a diﬀerent Lagrangian. This is achieved by param-
 eterizing the Lagrangian by a formula. The primal-dual procedure for .LΦ may
 then invoke the procedure for .LΦ for some formula .Φ with fewer quantiﬁers.
     We show that the three algorithms correspond to instances of the recur-
 sive primal-dual procedure deﬁned with the same family of Lagrangians. The
 diﬀerences between the algorithms manifest themselves in the way each algo-
 rithm updates its candidate proof and refutation. In all three cases, the update
 is based on solving a problem we identify, namely model-based projection for
 formulas of the form .∃x.∀x .Φ. However, each algorithm tackles this problem
 diﬀerently: QSMA [5] removes .∀x by interpolation and .∃x by model-based pro-
 jection; SynSAT [18] employs a stronger form of model-based pro jection, known
 as model-guided term selection [11]; and QSAT [2] carefully controls the formula
.Φ so that simply ignoring .x in .Φ yields an appropriate pro jection of .∀x . Thus,

 the Lagrangian-based view of the algorithms reveals their core ideas, distilling
 their similarities and diﬀerences.
     Beyond theoretical analysis, we demonstrate the practical usefulness of the
 Lagrangian-based approach by proposing a small improvement to QSAT [2]. In
 the course of our attempt to describe QSAT in terms of a Lagrangian, we noticed
 that the algorithm admits an execution trace that is diﬃcult to capture by
 our intended Lagrangian. By analyzing this trace, we found that the algorithm
 described in [2] has a progress issue, which we also conﬁrmed experimentally. We
 propose a modiﬁcation that aligns the algorithm with our intended Lagrangian.
 We implement the modiﬁcation and evaluate it experimentally, showing that the
 modiﬁcation improves performance.

Contributions. This paper analyzes three QSMT algorithms, namely by Bjørner
and Janota [2], by Bonacina et al. [5] and by Murphy and Kincaid [18], using the
Lagrangian-based framework proposed by Tsukada et al. [21]. Our contributions
can be summarized as follows.
– Our analysis uncovers a common structure shared by the three algorithms,
  which had not been clear before. By placing three algorithms on a common
  foundation, our analysis enables direct comparison and the transfer of ideas
  between them.
– We introduce a new problem, model-based projection for .∃∀-formulas or .∃∀-
  MBP. Our general procedure shows that, given a procedure for .∃∀-MBP, one
  can obtain a procedure for quantiﬁed SMT. We also observe that the largest
  diﬀerence among the three algorithms we analyze can be understood as a
  diﬀerence in how they solve quantiﬁed model-based projection.
– Beyond theoretical analysis, we demonstrate the practical value of the La–
  grangian-based approach by proposing an improvement to an algorithm and
  evaluating it experimentally. In the course of our Lagrangian-based analysis,
78        I. Bocevska et al.

     we identiﬁed an issue with the progress property of the algorithm deﬁned in
     the paper by Bjørner and Janota [2]. We propose a remedy and experimentally
     demonstrate that it improves performance.



2      Preliminaries: Lagrangian for Verification

This section brieﬂy reviews the generalized Lagrangian-based duality introduced
in [21], which forms the foundation of this paper.
    The Lagrangian-based duality in [21] generalizes the classical notion of dual-
ity from mathematical optimization, making it applicable within the domain of
program veriﬁcation and automated reasoning.3

Definition 1 (Generalized Lagrangian). A Lagrangian is a function .L : X×
Y −→ {−1, +1} from a meet semi-lattice .(X, ) and a set .Y that is monotone
on .X.

      Intuitively, .x ∈ X represents a candidate refutation and .y ∈ Y a candidate
 proof, while the Lagrangian .L(x, y) returns which of the two is more convinc-
 ing. We are interested in the values of .inf x supy L(x, y) and .supy inf x L(x, y).
 If .inf x supy L(x, y) = −1, there exists .x∗ ∈ X such that .L(x∗ , y) = −1 for
 every .y ∈ Y . This means that .x∗ ∈ X is a genuine refutation. Similarly, if
                                                                            ∗
.supy inf x L(x, y) = +1, there exists a genuine pro of, i.e. .y                 ∈ Y such that
                  ∗                                         ∗           ∗
.∀x ∈ X.L(x, y ) = +1. The problems of ﬁnding .x and .y are the primal and

 dual problems, respectively.
      Tsukada et al. [21] proposed a general procedure to search for .x∗ and .y ∗ . The
 idea is as follows. Let .α0 ∈ X be an arbitrary element. We ﬁrst check whether
.supy L(α0 , y) = −1. If that is the case, .α0 is a solution to the primal problem
 (P) and we are done; otherwise, there exists .β0 such that .L(α0 , β0 ) = +1. This
.β0 is a candidate pro of that p erforms well at least against .α0 . Then we check

 whether .inf x L(x, β0 ) = +1, i.e. .β0 performs well against all .x ∈ X. If that is the
 case, .β0 is a solution to the dual problem (D) and we are done; otherwise, there
 exists .α1 such that .L(α1 , β0 ) = −1. The basic idea is to iterate this procedure.
      Unfortunately, this naive process does not enjoy progress. For example, after
 choosing .α0 , β0 , α1 , β1 , α2 , it may happen that .L(α2 , β0 ) = +1 and .β0 is chosen
 again as .β2 . In that case, the sequence .. . . , β0 , α1 , β1 , α2 , β0 , . . . may continue
 looping, and the computation may eﬀectively make no progress.
      The mechanism that ensures progress is the meet semi-lattice structure of .X
 and the monotonicity of .L. The idea is to update .α monotonically by taking the
 meet of the current and newly discovered candidates, instead of replacing the
 current one (see Line 13 in Algorithm 1).


 3
      The following deﬁnition is not the general one given in Tsukada et al. [21], but
     a specialized version tailored to best ﬁt the setting of this paper; see [21] for the
     general deﬁnition. Likewise, Algorithm 1 is also specialized to our setting.
                  Lagrangian-Based Duality for Quantiﬁed SMT Algorithms         79

     Then the same candidate Algorithm 1 . Primal-Dual Procedure [21]
 never appears twice. Since 1: Function PrimalDual(L)
.L(αi , βi ) = +1 and .L(αi+1 , βi ) =
                                         2: arbitrary initial refutation α ∈ X
 −1, we have .αi = αi+1 , so 3: while true do
 the sequence is strictly decreas- 4:          // refutation check + update proof
 ing .α0      α1     . . . . Hence, the 5:     if supy L(α, y ) ≤ 0 then
 elements of the .α-sequence are 6:                return (P, α)
 mutually distinct. To see .βi = 7:            take β from {y ∈ Y | L(α, y ) > 0}
 βj for .i < j, it suﬃces to show 8:
.L(αj , βj ) = +1 and .L(αj , βi ) ≤     9:    // proof check + update refutation
 L(αi+1 , βi ) = −1.                    10:    if inf x L(x, β ) ≥ 0 then
     These observations yield a 11:                return (D, β )
 procedure called the primal-dual 12:          take γ from {x ∈ X | L(x, β ) < 0}
 procedure in [21] (Algorithm 1). 13:          α←α γ
 This procedure is applicable to
 arbitrary Lagrangians, provided that the following procedures are given: (Line
 5) check whether .supy L(α, y) ≤ 0; (Line 7) construct an element of .{y ∈ Y |
 L(α, y) < 0}; (Line 10) check whether .inf x L(x, β) ≥ 0; and (Line 12) construct
 an element of .{x ∈ X | L(x, β) < 0}.
     The primal–dual procedure always enjoys progress and partial correct-
 ness [21, Theorems 2.8 and 2.9], although it does not always terminate. The
 eﬃciency of the procedure (including termination) depends heavily on how .α
 and .β are chosen in Lines 7 and 12.


3     Unified Account for Quantified SMT Solving
In this section, we introduce a general Lagrangian for solving the quantiﬁed SMT
problem we propose. We begin with a Lagrangian that is easy to understand but
ineﬃcient, and use it to give an overview of the entire procedure. In particular,
the idea of constructing a QSMT procedure by recursively invoking Algorithm
1, exploiting the inductive structure of formulas, is novel. We then present a
Lagrangian that more accurately captures the actual behavior of our method.


3.1   Definition of the Problem

Assume a theory .T with a standard model over a domain .D. Typical examples
include LIA (linear integer arithmetic), LRA (linear real arithmetic) and NRA
(non-linear real arithmetic) with domains .D = Z, R, R, respectively. We denote
by L the language over which .T is deﬁned.
    Logical formulas can be classiﬁed by the complexity of their use of quantiﬁers.
The simplest class consists of formulas with no quantiﬁers; this class is called
quantiﬁer-free and written as QF-L. The next simplest formulas are those that
contain only one kind of quantiﬁer. A formula belongs to .Σ1 (resp. .Π1 ) when
it is of the form .∃x.Φ (resp. .∀ ) for some quantiﬁer-free .Φ. Slightly abusing
terminology, we will also call a formula equivalent to a .Σ1 -formula .Σ1 . For
80      I. Bocevska et al.

 example, for a .Σ1 -formula .F = ∃x.Φ and a .Π1 -formula .G = ∀y.Ψ , the formula
.F ∧ ¬G is in .Σ1 because .F ∧ G ⇔ ∃ y.(Φ ∧ ¬Ψ ) (provided that . y is a sequence
 of pairwise distinct variables).
     An assignment .M is a ﬁnite mapping from variables to values in the domain
.D. We write .M [x     v] for the extension of .M by .x  v, i.e., .(M [x  v])(y) = v
 when .x = y and .M (y) when .y ∈ dom(M ).
     The quantiﬁed SMT or QSMT problem asks whether a given closed formula .Φ
 possibly with quantiﬁers satisﬁes .T |= Φ, or equivalently .D |= Φ for the standard
 model .D of .T . We slightly generalize QSMT for a technical convenience. The
 generalized problem takes a pair of a formula .Φ and an assignment .M for all the
 free variables of .Φ and asks whether .D, M |= Φ. We shall refer this generalized
 version as QSMT.
     The standard SMT problem, which usually takes a quantiﬁer-free formula .Φ
 and asks if it has a satisfying assignment to its free-variables, can be seen as a
 special instance of QSMT: it asks whether .D |= ∃x.Φ where . is the list of free
 variables of .Φ. We call this subproblem QF-SMT and assume a decision proce-
 dure for this subproblem. We assume that a QF-SMT solver gives an assignment
.M such that .D, M |= Φ if it exists.
     Any formula is equivalent to a formula of the form .∃x1 .∀x2 .∃x3 . . . . Qxk .Ψ ,
 where .Ψ is quantiﬁer free and .Q = ∀ (when .k is even) or .∃ (when .k is odd). For
 simplicity, we assume an input of QSMT is in this form.

Remark 1. We should note here that QSMA [5] and SynSAT [18] are not
restricted to prenex-normal form and that the latter paper emphasized this
point. Our restriction to prenex-normal form is purely for ease of exposition;
the techniques developed in this paper are applicable to general formulas.


3.2   Unified Lagrangian

Assume an input .(M, Ψ ). If .Ψ is quantiﬁer-free, we can easily decide whether
M |= Ψ by evaluating .Ψ on .M . We focus on the case where .Ψ has a quantiﬁer.
.

By our assumption, .Ψ = ∃x.Φ for some .Φ.
    We deﬁne a Lagrangian for the pair .(M, ∃x.Φ(x, y1 , . . . , yk )). A refutation is
an over-approximation .F of .Φ (i.e., .Φ =⇒ F ) that is false on .M (i.e., .M = ∃x.F ).
A proof is an appropriate instantiation for .x, i.e., a value .v ∈ D such that .M [x
v] |= Φ. In contrast to proof candidates, which have canonical representations,
we still need to consider how to represent a refutation candidate .F . Here, we
assume a class .C of “easy-to-handle” formulas, which refutation candidates .F
range over. This class .C varies across algorithms: it consists of quantiﬁer-free
formulas for Bjørner and Janota [2] and Bonacina et al. [5], and of .Σ1 -formulas
for Murphy and Kincaid [18].
    This intuition induces a Lagrangian

                 LM,∃x.Φ
                 .           :   XM,∃x.Φ × YM,∃x.Φ −→ {−1, +1},
                         Lagrangian-Based Duality for Quantiﬁed SMT Algorithms                     81

Algorithm 2 . Instantiation of Primal-Dual Procedure
 1: Function QSmt0 (M , ∃x.Φ)
 2: while true do
 3:   if M |= ∀x.¬F then
 4:       return Refutation(F )
 5:   take v such that M [x    v ] |= F
 6:
 7:   if M [x    v ] |= Φ then
 8:       return Proof(v )
 9:   take H such that Φ =⇒ H and M [x                 v] = H
10:   F ←F ∧H


where .XM,∃x.Φ := { F ∈ C | Φ =⇒ F } and .YM,∃x.Φ := D, deﬁned by

                                           −1 if M [x         v] |= ¬F ( y)
                     .LM,∃x.Φ (F, v) =
                                           +1 if M [x         v] |= F ( y) .

XM,∃x.Φ has a natural meet semi-lattice structure given by conjunction. Under
.
this Lagrangian, the prover tries to ﬁnd .v such that .M [x    v] has not been
refuted by .F , and the refuter tries to ﬁnd a ﬁner over-approximation .F of .Φ
that does not contain .M [x    v].
Lemma 1. Assume that .Φ ⇐⇒ F ∗ for some .F ∗ ∈ C. Then
               .   inf F supv LM,∃x.Φ (F, v)     =     supv inf F LM,∃x.Φ (F, v),
which is .+1 if and only if .M |= ∃x.Φ.
Proof. If .M |= ∃x.Φ, then .M [x       v] |= Φ for some .v and, since .Φ =⇒ F , we
have .inf F LM,∃x.Φ (F, v) = +1. If .M = ∃x.Φ, then .supv LM,∃x.Φ (F ∗ , v) = −1. .
     By instantiating Algorithm 1 with .LM,∃x.Φ , we obtain Algorithm 2. Here, we
 use the following facts: (1) .M |= ∀x.¬F iﬀ .supv LM,∃x.Φ (F, v) = −1, and (2) for
.v chosen as in Line 5, .M [x             v] |= Φ iﬀ .inf F LM,∃x.Φ (F, v) = +1.
     To make this procedure implementable, we need to specify several subrou-
 tines, namely, (a) check of .M |= ∀x.¬F on Line 3, (b) construction of .v such that
.M [x     v] |= F on Line 5, (c) check of .M [x                    v] |= Φ on Line 7, and (d) con-
 struction of .H ⊆ Dk+1 such that .Φ ⇒ H and .M [x                       v] = H on Line 9. Among
 these, (a) and (b) can be easily provided, given that .F ∈ C is “easy-to-handle”.
 For instance, if .C consists of quantiﬁer-free formulas, then (a) amounts to check-
 ing that .F [v1 /y1 , . . . , vk /yk ] (where .y1 , . . . , yk is the list of free variables in .∃x.Φ
 and .vi = M (yi )) is unsatisﬁable, which can be solved by a QF-SMT solver.
 Similarly, (b) asks for a concrete assignment to .x when .F [v1 /y1 , . . . , vk /yk ] is
 satisﬁable, and this can also be obtained using a QF-SMT solver.
     In contrast, (c) and (d) are diﬃcult problems. Since the formula .Φ generally
 contains quantiﬁers, (c) cannot be handled by a QF-SMT solver. Likewise, the
 problem (d) is also challenging because of quantiﬁers in .Φ. We shall discuss how
 we can overcome these problems.
82      I. Bocevska et al.

Algorithm 3 . Recursive Primal-Dual Procedure
 1: Function QSmt1 (M , ∃x.∀x .Φ)
 2: while true do
 3:   if M |= ∀x.¬F then
 4:       return Refutation(F )
 5:   take v such that M [x    v ] |= F
 6:
 7:   match QSmt1 (M [x       v ], ∃x .¬Φ) with
 8:       case Refutation(F ) :
 9:          return Proof(v )
10:       case Proof(v ) :
11:           take H such that (∀x .Φ) =⇒ H and M [x        v] = H
12:           F ←F ∧H



3.3   Recursive Pro cedure

We ﬁrst consider how to handle problem (c). In fact, there is a very simple idea
for this. We are currently trying to solve a QSMT problem .M |= ∃x.Φ, and in
the process we need to decide .M [x       v] |= Φ, which is itself another QSMT
problem. This suggests solving .M [x     v] |= Φ recursively.
    The algorithm in Algorithm 3 implements this idea. To make the recursive
calls easier to follow, we explicitly write out the ﬁrst two quantiﬁers of the
input formula. Note also that, since we assume the input formula starts with
an existential quantiﬁer, the recursive call on Line 7 is made on the negated
formula. The conditional branching on Line 7 in Algorithm 2 corresponds to the
case analysis on Line 7 in Algorithm 3: the condition is true if and only if the
recursive call returns .Refutation(F ). Currently, we only use the tags of the
return value, ignoring its content .F or .v .


3.4   Quantified Mo del-Based Pro jection

The remaining issue is (d). It is tricky, and various approaches can be considered
for this problem. Actually, our Lagrangian-based analysis of the three QSMT
algorithms [2,5,18] suggests that the main diﬀerences between them are in how
they handle (d).
    Although there are diﬀerences in how (d) is handled, the three QSMT algo-
rithms also have aspects in common. This subsection discusses these similarities.
    On Line 11 in Algorithm 3, where we address issue (d), we have access
to the information .Proof(v ) obtained from the recursive call .QSMT(M [x
v], ∃x .¬Φ) on Line 7. This means that .M [x        v][x     v ] |= ¬Φ. However, con-
structing an appropriate .H from this information alone is not straightforward.
    We therefore consider asking the recursive call to return slightly stronger
information. In the recursive call, we prove .M [x       v][x      v ] |= ¬Φ, or equiv-
alently .M [x    v] |= ∃x .¬Φ, but in many cases (slight modiﬁcations of) this
proof simultaneously establishes .M1 [x        v1 ] |= ∃x .¬Φ for other .M1 and .v1
                  Lagrangian-Based Duality for Quantiﬁed SMT Algorithms         83

 as well. Therefore, we modify the procedure so that it also returns information
 about these values. More concretely, we require the recursive call to return an
 under-approximation .G ⊆ Dk of .∃x .¬Φ, which contains .M [x        v].
     This change aﬀects two parts of the procedure. One is where we receive a
 return value .Proof(v ) from the recursive call (Line 10 in Algorithm 3), and the
 other is where the procedure itself returns a value .Proof(v) (Line 9 in Algorithm
 3). The modiﬁed procedure is presented in Algorithm 4.
     The former change is straightforward. We additionally obtain, as part of the
 return value of the recursive call, information about .G satisfying .G =⇒ ∃x .¬Φ
 and .M [x    v] |= G, so it suﬃces to take .H = ¬G (Line 12 in Algorithm 4).
     The latter is more subtle. We need an appropriate under-approximation of
.∃x.∀x .Φ, namely .G such that .G =⇒ ∃x.∀x .Φ and .M |= G. The available

 information is essentially twofold: the value .v for .x and an over-approximation
.F of .¬Φ such that .M [x      v] |= ∀x .¬F . Line 9 in Algorithm 4 expresses that
 we should construct .G from this information in some way.
     This problem is close to a well-known one, namely model-based projection (or
 MBP ) [15,16]. Let us ﬁrst brieﬂy review the standard MBP.
Definition 2 (Mo del-Based Pro jection, MBP). The model-based pro jec-
tion (or MBP) with respect to .C is the fol lowing problem:
 – Input: Lists of variables . and . , a formula .F ∈ C with free variables . y
   and a model .M |= F of .F (hence .M |= ∃y.F ( y)).
 – Output: A formula .G ∈ C with free variables . such that .M |= G( ) and
  .G( ) ⇒ (∃y.F (   y)).
An MBP procedure .P enjoys image-ﬁniteness if .{P(           y) | M |= F } is
ﬁnite. We sometimes cal l MBP in this sense .∃-MBP. We often write .P(M, ∃y.F )
for .P(      y).                                                             .


MBP is closely related to quantiﬁer elimination: quantiﬁer elimination is a ﬁnite-
image MBP (which ignores the model), and conversely, a theory that admits a
ﬁnite-image MBP also admits quantiﬁer elimination, provided that QF-SMT is
decidable for the theory. However, the eﬃciency can diﬀer dramatically, and it is
known that, for some theories, MBP can be computed signiﬁcantly faster than
quantiﬁer elimination.
   What we needed for our procedure is a quantiﬁed version of MBP.
Definition 3 (.∃∀-MBP). The .∃∀ model-based pro jection (or .∃∀-MBP) with
respect to .C is the fol lowing problem:
 – Input: Lists of variables . z, a formula .F ∈ C with free variables .  z,
   and an assignment .M on . y such that .M |= ∀z.F (       z) (hence .M |=
   ∃y.∀z.F (   z)).
 – Output: A formula .G ∈ C with free variables . such that .M |= G( ) and
  .G( ) ⇒ (∃y.∀z.F (    z)).
   A .∃∀-MBP procedure .P enjoys the image-ﬁniteness if .{P(                   z) |
M |= ∀z.F } is ﬁnite. We often write .P(M, ∃y.∀z.F ) for .P(             z).     .
84      I. Bocevska et al.

Algorithm 4 . Our QSMT Procedure (Recursive Version)
 1: Function QSmt(M , ∃x.∀x .Φ)
 2: while true do
 3:   if M |= ∀x.¬F then
 4:       return Refutation(F )
 5:   take v such that M [x       v ] |= F
 6:
 7:   match QSmt(M [x          v ], ∃x .¬Φ) with
 8:       case Refutation(F ) :
 9:          G ← Pro jection(M [x         v ], ∃x.∀x .¬F )
10:           return Proof(v , G)
11:       case Proof(v , G ) :
12:           F ← F ∧ ¬G


   If the theory .T admits quantiﬁer elimination, a ﬁnite-image .∃∀-MBP is also
possible. The substitution .G := ∀z.F (    z) (where .vi = M (yi )) is a .∃∀-MBP
procedure, which is not image ﬁnite, provided that .C is closed under .∀ and
substitution of a variable by a value.

Theorem 1. The procedure in Algorithm 4 enjoys progress. Furthermore, if we
use an image-ﬁnite .∃∀-MBP procedure, Algorithm 4 always terminates.
Proof (sketch). The progress property comes from the general result [21]. We
prove termination by induction on the number of quantiﬁers in the formula. We
prove the two claims : (1) the procedure terminates for every input .M , and (2)
the number of logical formulas that can appear in the possible return values
(i.e. .F of .Refutation(F ) and .G of .Proof(v, G)) are ﬁnite. Assume that the
claim holds for recursive calls. Then the variety of .G in .Proof(v , G ) on line 11
is ﬁnite. So, there are only ﬁnitely many possible values for .F . Since Algorithm 4
enjoys progress, it eventually terminates. The number of possible return values
of the form .Refutation(F ) is bounded by the number of values stored in .F ,
which is ﬁnite. The number of .G in possible return values (generated in line 9)
is ﬁnite, because of the ﬁniteness of the variation of .F and the image-ﬁniteness
assumption of the projection.                                                     .



3.5    Implementation Notes
Algorithm 4 does not specify the initial value of .F . While this choice does not
aﬀect the theoretical properties of the procedure, it can have a signiﬁcant impact
on eﬃciency. This subsection discusses how .F should be handled in an implemen-
tation of our procedure, and provides an implementation-friendly description.
    Regarding the initial value of .F , at the beginning, we have too little informa-
tion on the input formula, and the only reasonable choice is to take .F =
(recall that .F must be an over-approximation of the input formula). How-
ever, as the computation proceeds, it can happen that QSmt is invoked on the
same formula with diﬀerent assignments: for example, after the computation of
                    Lagrangian-Based Duality for Quantiﬁed SMT Algorithms             85

Algorithm 5 . Our QSMT Procedure (Loop Version)
 1: Function QSmtLoop(M1 , ∃x1 .∀x2 . . . . ∃xn−1 .∀xn .Φ)
 2: F1      ; F2     ; . . . ; Fn      ; Fn+1 ← Φ; Fn+2 ← ¬Φ
 3: j ← 1
 4: while true do
 5:    if Mj |= ∀xj .¬Fj then
 6:       if j = 1 then
 7:            return false
 8:       if j = 2 then
 9:            return true
10:       G ← Pro jection(Mj , ∃xj −1 .∀xj .¬Fj )
11:       Fj −2 ← Fj −2 ∧ ¬G
12:       j ←j−2
13:    else
14:       take vj such that Mj [xj         vj ] |= Fj
15:       Mj +1 ← Mj [xj          vj ]
16:       j ←j+1



.QSmt(M [x         v], ∃x .¬Φ) is ﬁnished, one may invoke .QSmt(M [x        w], ∃x .¬Φ)
 with .v = w. In such a case, the ﬁrst call has already computed an approximation
.F of .∃x .¬Φ, and discarding this information and starting the computation of
.QSmt(M [x         w], ∃x .¬Φ) again from .F =          seems ineﬃcient. Therefore, for
 a formula that has been queried before, it is natural to initialize .F to “the ﬁnal
 value of .F from the previous run” of QSmt on that formula.
      To handle such information that persists beyond a function call in a clear way,
 it is preferable to write the procedure as a single loop that explicitly manages the
 call stack, rather than as a description based on recursive calls. Transformation
 can be done mechanically.
      Algorithm 5 is the resulting loop version. The variable .Fi represents the
.F asso ciated with the formula .∃xi .∀xi+1 . . . . ∀xn .Φ (when .i is o dd) or, resp ec-
 tively, .∃xi .∀xi+1 . . . . ∃xn .¬Φ (when .i is even). Moreover, to handle the trivial
 quantiﬁer-free cases (which we omitted in Algorithm 4 for brevity), we addi-
 tionally introduce two extra .F ’s, .Fn+1 = Φ and .Fn+2 = ¬Φ. The call-stack
 information consists of pairs of an assignment .M and a formula, but we do not
 record the formula explicitly, since it is uniquely determined by the call-stack
 depth, which is denoted by .j. Lines 14 to 16 in Algorithm 5 correspond to lines 5
 to 7 in Algorithm 4. Lines 10 to 12 are more subtle. Since .Mj |= ∀xj .¬Fj , the
 recursive function call at depth .j returns .Refutation(Fj ). This is received on
 Line 8 in Algorithm 4 at call-depth .j − 1, which then computes the .∃∀-MBP
 (Line 10 in Algorithm 5). The depth .j − 1 call returns .Proof(v, G), this value is
 received on Line 11 in Algorithm 4 at call-depth .j − 2, then .F at call-depth .j − 2
 is conjoined with .¬G (Line 11 in Algorithm 5). Line 12 in Algorithm 5 updates
 the current call-depth.
86         I. Bocevska et al.

4        QSMA by Bonacina Et Al
We begin with QSMA by Bonacina et al. [5] implemented in YicesQS, an exten-
sion of Yices2. QSMA manages both over- and under-approximations of the input
formula: it uses model-based pro jection to compute an under-approximation, and
model-based over-approximation to compute an over-approximation. This section
explains QSMA as an instance of our general QSmt procedure (Algorithm 4).


4.1       Mo del-Based Over-Approximation and .∃∀-MBP

Model-based over-approximation (or MBO) [5] can be seen as the “dual” of QF-
MBP. That is, given .∃x.Φ (where .Φ is quatiﬁer-free) and an assignment .M that
does not satisfy .∃x.Φ, it computes a quantiﬁer-free over-approximation .O of .∃x.Φ
that excludes .M (i.e., .(∃x.Φ) =⇒ O and .M = O).
   From our perspective, the negated view is more natural. That is, given a
formula .∀x.Ψ and a model .M |= ∀x.Ψ , a MBO procedure computes an under-
approximation .U of .∀x.Ψ that satisﬁes .M (i.e., a formula .U with .U =⇒ (∀x.Ψ )
and .M |= U ). The formula .U is given by .¬MBO(M, ∃x.¬Ψ ). We write this
procedure .MBO † .
   A combination of MBP and MBO provides a .∃∀-MBP procedure: given a
formula .∃y.∀z.Φ and a model .M |= ∀z.Φ, we obtain an under-approximation by

    .EAMBP (M, ∃y.∀z.Φ)         :=   let U = MBO † (M, ∀z.Φ) in MBP M, ∃y.U ).

        This .EAMBP is image-ﬁnite if so are .MBP and .MBO.

Remark 2. A drawback of this approach is that it is diﬃcult to achieve the image-
ﬁniteness of .EAMBP . A ma jor approach to MBO is based on interpolation:
given a formula .∃x.Φ(x, y1 , . . . , yk ) and a model .M = ∃x.Φ with .vi = M (yi ), the
desired formula .O can be obtained as an interpolation of .Φ           (y1 = v1 ∧ · · · ∧
yn = vn ). In fact, the implementation in [5] uses an interpolating theorem prover.
However, it is rare for interpolation procedures to satisfy the image-ﬁniteness
property. An image-ﬁnite interpolation procedure for LRA can be found in [6,
Sect. 6.2].                                                                            .




4.2       QSMA and Our Pro cedure

In our understanding, QSMA in [5] can be seen as an instance of Algorithm 4. An
approximation .F is represented as a quantiﬁer-free formula, and the .∃∀-MBP
procedure is the above-deﬁned one. Bonacina et al. proved that their algorithm
is totally correct [5, Theorems 2 and 3] under the assumption of the image-
ﬁniteness of .MBP and .MBO, and this result corresponds to Theorem 1.
    To see the correspondence, it suﬃces to compare [5, Fig. 2] and Algorithm 4.
Here we focus only on the minimal information needed to decode the correspon-
dence, requiring some familiarity with QSMA [5]. In QSMA, the input formula is
represented as a tree structure called a QSMA-tree. We consider only formulas of
                         Lagrangian-Based Duality for Quantiﬁed SMT Algorithms       87

 the form .Φ = ∃x1 .∀x2 . . . . ∃xn−1 .∀xn .Ψ , and the corresponding tree has the form
.1 → 2 → · · · → n → (n + 1), consisting of .n + 1 nodes. The label of each node
.i with .i ≤ n is .[xi , ¬(i + 1).p] (and .[∅, Ψ ] for .n + 1). This means that, deﬁning

.Ψi := ∃xi .¬Ψi+1 and .Ψn+1 := Ψ yields .Ψ1 = Φ. From the formula lab els, we can
 see that every model must assign .false to propositional variables .i.p.
     The approximation F in our algorithm is stored in QSMA as the negation of
 the over-appoximation associated to the unique child .b = i + 1 of .i (that is, .¬b.U
 in their notation). So .L on line 74 corresponds to .F , and the test on line 8 is (the
 negation of) the test .M |= ∀x.¬F in our procedure. Its success in our algorithm
 corresponds to .M = nil in QSMA. In this case, QSMA computes MBO and then
 returns false. The caller is on line 20, and the condition on line 20 fails (as the
 assignment .M(b.p) to .b.p must be false). Since each node has at most one child,
 it exits the loop and returns true. The caller is on line 13, and this makes the
 test on line 13 succeed, after which it computes MBU (which is another name
 for MBP) and returns true. Overall, we see that it computes the MBP of an
 MBO and then performs two returns. This corresponds, in our procedure, to the
 ﬂow .return Refutation(F )             (G ← Projection(M [x          v], ∃x.∀x .¬F ))
 return Proof(v, G). On the other hand, when .M = nil , QSMA makes a recur-
 sive call to the child with the assignment .M , which corresponds to the recursive
 call in our procedure.
     A minor diﬀerence is whether the results of MBO are accumulated. In QSMA,
 the results of MBO are accumulated in the variable .b.O. Our procedure does
 not store them: the MBO results (arising within the .∃∀-MBP computation) are
 simply discarded.


5         SynSAT by Murphy and Kincaid

This section studies SynSAT by Murphy and Kincaid [18], which reﬁnes the
approach by Farzan and Kincaid [11]. These procedures are grounded in a game-
theoretic interpretation of formulas, but here we instead provide an explanation
that focuses on quantiﬁed model-based projection.


5.1         Mo del-Guided Term Selection and .∃∀-MBP

A key technique in SynSAT is model-guided term selection [11], which is a stronger
form of MBP.

Lemma 2 ([11, Lemma 4.4]). There exists an eﬀectively computable function
select(M, ∃y.F ) that takes a pair of a formula .F (x, y) in QF-LRA (with a speciﬁed
.
variable .y) and a model .M |= F and returns a term with free variables . such that
(1) .M |= F (x, t) for .t = select(M, ∃y.F ), and (2) .{select(M, ∃y.F ) | M |= F } is
ﬁnite.                                                                              .




    4
        In this paragraph, all line numbers refer to those in [5, Fig. 2].
88      I. Bocevska et al.

    A function satisfying these properties is called a (model-guided) term selec-
tion. An eﬃcient implementation for QF-LRA is proposed by Farzan and Kin-
caid [11].
    Term selection is stronger than MBP: an image-ﬁnite MPB is obtained by
the mapping .(M, ∃y.F (x, y))     F (x, select(M, F )). The converse is non-trivial.
Although many MBP procedures are inspired by substitution, they often use
some generalization of substitution (e.g., considering an inﬁnite value). See [11,
Sect. 6] for a more detailed discussion.
    In our setting, an important consequence of term selection is that MBP can
be performed using term substitution alone, even when the target formula may
contain quantiﬁers,.

Lemma 3. Let .F (x, y) be a formula in LRA, possibly with quantiﬁers. There
exists a ﬁnite set .{t1 , . . . , tn } of terms with free variables in . such that

                       .(∃y.F ) ⇐⇒ F (x, t1 ) ∨ · · · ∨ F (x, tn ).

Proof. We apply quantiﬁer elimination to .F , obtaining a quantiﬁer-free formula
F0 that satisﬁes .F ⇐⇒ F0 . Let .{t1 , . . . , tn } = {select(M, F0 ) | M |= F0 }.
.                                                                                  .


    The proof is constructive, but it is not eﬃcient, since it relies on quantiﬁer
elimination. A key challenge, therefore, is whether we can eﬃciently ﬁnd an
appropriate term to substitute.


5.2   SynSAT in Our Framework
 We explain how to emulate SynSAT [18] using our procedure (Algorithm 4).
 The resulting procedure is shown in Algorithm 6. A key conceptual shift can be
 seen in Lines 6 and 7. Rather than engineering the .∃∀-MBP step in Line 11, it
 carefully chooses on Lines 6 and 7 the value .v assigned to .x in the recursive call.
 This simpliﬁes the subsequent .∃∀-MBP on Line 11.
     This might be somewhat unusual in veriﬁcation and SMT, but we use .Σ1 -
 formulas to represent .F . Let us ﬁrst check which class each formula belongs
 to. By induction, we show that (i) .F and the content of .Refutation(−) are
 in .Σ1 , and (ii) the content .G of .Proof(v, G) is in .Π1 . The base case is where
 the input formula is quantiﬁer-free; although we did not spell out the details of
 the procedure in this case, it is easy to construct one that satisﬁes the required
 conditions. We show the inductive step. According to the induction hypothesis,
.G on Line 13 is .Π1 , and therefore if .F is .Σ1 , so is .F ∧ ¬G. Therefore, .F remains
.Σ1 at every p oint in the execution (provided that it is initially .Σ1 ). It follows
 that the content of .Refutation(−) returned by the procedure on Line 4 is also
.Σ1 . As for .G in .Proof(v, G), by the induction hyp othesis, .F on Line 10 is .Σ1 ,
 so .G = ∀x .¬F on Line 11 is .Π1 , and so is .G in .Proof(v, G) on Line 12.
     The advantage of performing term selection on Line 6 for .F , rather than
 performing term selection on Line 11 for .∃x.∀x .¬F when constructing .G, is
 that term selection can be carried out eﬃciently for .Σ1 -formulas.
                     Lagrangian-Based Duality for Quantiﬁed SMT Algorithms               89

Algorithm 6 . Murphy-Kincaid Algorithm [18] in Our Framework
 1: Function MK(M , ∃x.∀x .Φ)
 2: while true do
 3:   if M |= ∀x.¬F then
 4:       return Refutation(F )
 5:   take v0 such that M [x       v0 ] |= F
 6:   t ← select(M [x    v0 ], ∃x.F )
 7:   v ← [[t]]M
 8:
 9:   match MK(M [x         v ], ∃x .¬Φ) with
10:       case Refutation(F ) :
11:            G ← (∀x .¬F )[t/x]
12:            return Proof(v , G)
13:       case Proof(v , G ) :
14:            F ← F ∧ ¬G


Lemma 4. Lemma 2 can be extended to the case where .F is .Σ1 .
Proof. Suppose .F = ∃z1 . . . . ∃zn .F0 with .F0 quantiﬁer-free. We ﬁrst compute a
model .M [z1        v1 , . . . , zn   vn ] of .F0 , then compute terms .si for .zi by term
selection for .∃zi .(F0 [sn /zn ][sn−1 /zn−1 ] . . . [si+1 /zi+1 ]), and ﬁnally perform term
selection for .∃y.(F0 [sn /zn ] . . . [s1 /z1 ]). The term .t obtained in the last step can
be taken as the term selected for .∃y.F with respect to .M .                               .


     The construction of .v ensures that .(∀x .¬F )[t/x] is a suitable choice
 for .Projection(M [x          v], ∃x.∀x .¬F ). The property .(∀x .¬F )[t/x] =⇒
 (∃x.∀x .¬F ) holds for substitution in general, and .M |= (∀x .¬F )[t/x] fol-
 lows from .M |= (∀x .¬F )[t/x] ⇐⇒ M [x              [[t]]M ] |= ∀x .¬F ⇐⇒ M [x
 v] |= ∀x .¬F , of which the last condition is ensured by the construction of
.Refutation(F ) in the recursive call.
     Termination follows from the following argument. First, since .F is updated
 monotonically, the same term .t cannot appear twice. Moreover, if the set of
 possible values of .G in .Proof(v , G ) is ﬁnite, there are only ﬁnitely many pos-
 sible .F ’s (as .F is a conjunction of .¬G ’s). This implies that the set of terms .t
 obtained by term selection is also ﬁnite. This ﬁniteness together with progress
 ensures termination.
     The relationship with the original procedure in [18] is as follows. Here we
 assume familiarity with [18]. The most important point is that Algorithm 4
 maintains a .Σ1 -formula .F , whereas [18] works with strategy skeletons .S. The
 bridge between the two is the lose function in [18, Sect. 5], which constructs a
.Σ1 -formula .lose(S, Φ) from a given strategy sketelon .S and the input formula .Φ.
                                                                                    5

 The term .t in our procedure corresponds to .π in [18, Algorithm 1], obtained by
 peeling the counter-strategy .U . Substituting .t into .¬F corresponds to the con-
 struction .π · U of a skeleton. Term selection appears in the function .CCS [18,
 5
      Note that deciding .M |= Ψ in our procedure corresponds to deciding .M |= ¬Ψ in
      theirs. Consequently, our formula .F in .MK(M, Φ) (Algorithm 4) and their skeleton
     .S in .Solve(¬Φ, M, S) [18, Algorithm 1] are related by .F = lose(S, ¬Φ).
90         I. Bocevska et al.

Algorithm 7 . Modiﬁed Version of Bjørner–Janota algorithm
 1: Function mBJ(M1 , ∃x1 .∀x2 . . . . ∃xn−1 .∀xn .Φ)
 2: F1      ; F2      ; . . . ; Fn  ; Fn+1 ← Φ; Fn+2 ← ¬Φ
 3: j ← 1
 4: while true do
 5:    if ¬j +1 Φ ∧ Fj ∧ strategy(Mj −1 , j ) is unsat then
 6:        if j = 1 then
 7:            return false
 8:        if j = 2 then
 9:            return true
10:        C ← Core(¬j +1 Φ ∧ Fj , strategy(Mj −1 , j ))
11:        G ← MBP (Mj , ∃xj −1 xj +1 xj +3 . . . xN .C) // N = n or n − 1
12:        Fj −2 ← Fj −2 ∧ ¬G
13:        j ←j−2
14:    else
15:        take Mj such that Mj |= ¬j +1 Φ ∧ Fj ∧ strategy(Mj , j )
16:        j ←j+1



Algorithm 3] that is used in the construction of a counter-strategy [18, Algo-
rithm 2]. It is an inductively-deﬁned function that repeatedly applies selection
and substitution, much like in the proof of Lemma 4.


6      QSAT by Bjørner and Janota

This section analyzes QSAT proposed by Bjørner and Janota [2] within the
framework of Lagrangian duality. As suggested in the introduction, our version
of Bjørner–Janota algorithm diﬀers from the original in its properties. We ﬁrst
describe our version based on QSmtLoop (Algorithm 5), and then explain how
it diﬀers from the original algorithm presented in [2].


6.1      Bjørner–Janota Algorithm in Our Framework

 The modiﬁed version of QSAT [2] is given in Algorithm 7.6 It is obtained by
 replacing .M |= ∀xj .¬Fj with a related unsatisﬁability check (Lines 5 and 15)
 and .∃∀-MBP with .∃-MBP (Line 11). Line 10 is for eﬃciency, and replacing this
 line with .C ← strategy(Mj , j) does not aﬀect its qualitative properties.
     Before going into the details of the procedure, we describe the auxiliary
 functions .Core and .strategy. The former is the computation of unsat core:
.Core(Ψ, Clauses) is deﬁned when .Ψ ∧       Clauses is unsat, and returns a sub-
 set .Clauses ⊆ Clauses such that .Ψ ∧ Clauses is also unsat. .strategy(M, j)
 returns a formula that captures .M as precisely as possible, expressible using
 only Boolean combinations of the atomic formulas occurring in .F1 , F2 , . . . , Fn+2 .

 6
      Here .¬j+1 denotes .j + 1 repetitions of .¬. Thus, .¬j+1 Φ ⇔ Φ when .j is odd, and
        j+1
     .¬     Φ ⇔ ¬Φ when .j is even.
                       Lagrangian-Based Duality for Quantiﬁed SMT Algorithms                91

It actually imposes an additional constraint: it is forbidden to use the variables
x , xj+2 , xj+4 , . . . . The concrete deﬁnition of .strategy(M, j) is .strategy(M, j) :=
. j
  {a ∈ Aj | M |= a}, where .Aj := a, ¬a a ∈ atomic(F1 , . . . , Fn+2 ), fv(a) ∩
{xj , xj+2 , xj+4 , . . . } = ∅ .
    This restriction on the free variables in .strategy(M, j) will matter in the .∃∀-
MBP step. We consider the case where .j is odd (then .¬j+1 Φ ⇔ Φ). For an
arbitrary formula .S, unsatisﬁability of .Φ ∧ Fj ∧ S implies .Φ ∧ Fj =⇒ ¬S. What
we want to compute via .∃∀-MBP is an over-approximation of

      .(∃xj .∀xj+1 . . . . ∃xn−1 .∀xn .Φ)   ⇐⇒   (∃xj .∀xj+1 . . . . ∃xn−1 .∀xn .Φ ∧ Fj )

(the equivalence follows from the invariant .(∀xj+1 . . . . ∃xn−1 .∀xn .Φ) =⇒ Fj ).
If .S does not contain .xj , xj+2 , xj+4 , . . . , the problematic universal quantiﬁers
can be ignored, so .∃∀-MBP is reduced to MBP. Line 11 performs this reduced
MBP. The unsatisﬁability check of .¬j Φ ∧ Fj ∧ strategy(M, j) is an alternative
to .M = Ψ , which also ensures that the constraint on free variables is met when
taking .S = strategy(M, j).

6.2       Comparison with the Original Pro cedure
As we have mentioned, our procedure in Algorithm 7 diﬀers from [2, Algorithm 1]
in the original paper. Here we assume some familiarity with the original paper.
    The signiﬁcant diﬀerences are on Lines 12 and 13, which correspond to the
return operations in the recursive version (Algorithm 4).
– Whereas line 12 in Algorithm 7 always moves to the level .j − 2, the original
  algorithm may move to a lower level (smaller index). The level in the original
  algorithm is given by .j := max {i | xi ∈ fv(G)} ∩ {j − 2, j − 4, j − 6, . . . }
  instead of .j − 2.
– Whereas Algorithm 7 reuses the model .Mj−2 at the returned level, the original
  algorithm refreshes it by explicitly erasing .Mj (where .j is the level deﬁned in
  the above item). More concretely, the original procedure has a line .Mj ← nil
  in between Lines 13 and 14.
     We proved that the former leads to a non-progressive behavior, which we
 also observed experimentally. We have conﬁrmed this issue with the authors of
 the original paper [2].7 A problem occurs when .G contains a free variable .x
 with .j      . This may happen when the parities of .j and . do not match.
 Algorithm 7 does not suﬀer from this issue since this problematic case never
 happens for .j = j − 2 as .xj−1 , xj+1 , xj+3 , . . . have been eliminated by MBP
 on Line 11. One can simply ﬁx this issue by taking .j as the maximum among
.{j − 2, j − 4, j − 6, . . . } that satisﬁes .x ∈ fv(G) =⇒ j ≥ .

     For the latter, we observed a non-progressive behavior in our reimplementa-
 tion of the original procedure, which cannot be observed in our implementation
 of our modiﬁcation (Algorithm 7). However, we have not yet completed a theo-
 retical analysis of whether this latter diﬀerence aﬀects progress.
 7
      Personal communication; see the extended version [4].
92      I. Bocevska et al.

    We note that a more recent adaptation of the Bjørner–Janota algorithm for
QBF satisﬁability [13] avoids the progress issues by modiﬁcations similar to ours
(in the simpler QBF setting).




Fig. 1. Comparison of MuCyc and Z3 version 4.15.2 on the SMT-LIB2 quantiﬁed LRA
benchmark set. Blue dots in the plots indicate that the answer to a given problem is
“sat”, while red dots indicate “unsat”. The timeout is 300 s.



7    Exp erimental Evaluation
We implemented MuCyc, a quantiﬁed SMT solver based on the Lagrangian
proposed in this paper. Our tool is available at GitHub [3]. MuCyc modiﬁes
the method proposed in [2] so that the resulting solver satisﬁes the progress
property. The method in [2] also forms the basis of the QSMT solving approach
implemented in the SMT solver Z3. MuCyc supports quantiﬁed LIA, quantiﬁed
LRA, and QBF. In its default conﬁguration, MuCyc enforces the progress prop-
erty. By switching the solver conﬁguration, MuCyc can reproduce the original
behavior of [2] and therefore does not satisfy the progress property.
    We formulated the following research question: to what extent enforcing the
progress property aﬀects the performance of QSMT solving. To address this ques-
tion, we conducted a comparative evaluation using the SMT-LIB2 quantiﬁed
LRA benchmark set consisting of 2,439 instances. The experiments were per-
formed with a timeout of 300 s, comparing Z3 and two conﬁgurations of MuCyc.
All the experiments were conducted on AWS t3.2xlarge instances equipped with
an Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50 GHz and 32 GB of memory.
    The experimental results are summarized in the two scatter plots in Fig. 1.
The left scatter plot compares the performance of the two MuCyc conﬁgura-
tions, namely the conﬁguration that guarantees the progress property and the
conﬁguration that does not. The right scatter plot compares MuCyc (Progress)
with Z3. According to the authors of [2], Z3’s QSMT solving engine is not a
direct implementation of the method described in the paper; however, it has
                 Lagrangian-Based Duality for Quantiﬁed SMT Algorithms       93

been conﬁrmed that it does not satisfy the progress property. Quantitatively,
Z3 solves 754 sat instances and 1,427 unsat instances, MuCyc (Progress) solves
758 sat instances and 1,532 unsat instances, and MuCyc (Non Progress) solves
727 sat instances and 1,507 unsat instances.
    It can be observed that the MuCyc conﬁguration satisfying the progress
property signiﬁcantly outperforms the non-progress conﬁguration both in solving
speed and in the number of sat and unsat instances solved within the time limit.
Moreover, compared to Z3, MuCyc also solves a larger number of instances,
conﬁrming that designing and implementing a QSMT solving algorithm so as
to satisfy the progress property has a direct and measurable impact on solver
performance. On the other hand, there also exist instances that time out in
MuCyc but are solved by Z3, which we hypothesize to arise from diﬀerences
in the models selected for MBP. As discussed in this section, our Lagrangian
based theoretical analysis shows that an existing algorithm can be modiﬁed to
satisfy the progress property, and our experimental results conﬁrm that this
modiﬁcation has a concrete and practically signiﬁcant impact.


8   Related Work and Conclusion

The most closely related work is the Lagrangian-based framework for veriﬁ-
cation algorithms leveraging duality, introduced by Tsukada et al. [21], which
this paper builds upon. The authors presented a Lagrangian characterization of
the approach by Farzan and Kincaid [11], which is a predecessor to the algo-
rithm by Murphy and Kincaid [18]. In this paper, we address the algorithm
presented in [18] and provide a corresponding Lagrangian formulation for it,
placing it withing a uniﬁed Lagrangian-based account for QSMT solving. More
broadly, we presented a Lagrangian-based analysis of three QSMT solving algo-
rithms and showed that several recently proposed approaches can be character-
ized as instances of a recursive primal-dual procedure. Despite some diﬀerences,
these algorithms share a common underlying structure, with their primary dis-
tinction arising from how .∃∀-model-based pro jection is realized. Furthermore,
the Lagrangian framework allowed us to identify a progress issue in one of the
existing methods, as well as a proposed ﬁx. The results demonstrate that the
Lagrangian-based framework provides both a unifying theoretical foundation
and a basis for practical improvement of QSMT algorithms.
    Directions for future work include analyzing additional QSMT solving
algorithms [8,19,20] to determine whether they can also be represented as
instances of the Lagrangian-based primal-dual framework by identifying suitable
Lagrangians. Such an analysis may reveal further common structure and clar-
ify diﬀerences between the approaches, leading to more principles and eﬀective
QSMT solving techniques. Another possible direction for future work is lever-
aging the current insights to develop solving methods for quantiﬁed ﬁxpoint
logics [14,17,22] using the Lagrangian-based framework.
    An open question is whether .∃∀-MBP admits an eﬃcient procedure. We
discussed three implementation approaches for a procedure that uses .∃∀-MBP,
94      I. Bocevska et al.

but in all of them, either (i) the image-ﬁniteness property lacks, or (ii) the
arguments to .∃∀-MBP (i.e., a formula .∃x.∀x .Φ and a model .M [x        v]) are
carefully controlled so that only “easy” instances arise during the computation.
The question of whether image-ﬁnite .∃∀-MBP can be implemented eﬃciently for
general formulas and models still remains.

Acknowledgments. We would like to thank the anonymous reviewers for their helpful
comments and suggestions. We would also like to thank Taro Sekiyama for his generous
support and assistance. This study was supported by JSPS KAKENHI Grant Number
JP23K24820, JP24H00699, JP25H00446, and JP25K24739. This research was funded
in whole or in part by the Austrian Science Fund (FWF) 10.55776/DOC1345324;
the FWF SFB pro ject SpyCoDe F8504; the WWTF ICT22-007 grant ForSmart; and
the SBA Research COMET Center SBA-K1 NGC. This research is partially funded
by the Israel Science Foundation (ISF), grant no. 2117/23. The research leading to
these results has received funding from the European Research Council under the
European Union’s Horizon 2020 research and innovation programme (grant agreement
No [759102-SVIS]). This research is partially supported by Israel Science Foundation
research grant (ISF’s No. 4136/25) and the Maimonides Fund’s Future Scientists Cen-
ter, a research grant from the Center for New Scientists at the Weizmann Institute of
Science, and a grant from the Azrieli Foundation.


Data Availability Statement. The software that supports the evaluation results
reported in Sect. 7 is available at GitHub and Zenodo [3].
Disclosure of Interests. The authors have no competing interests to declare that
are relevant to the content of this article.

References
 1. Ball, T., Ma jumdar, R., Millstein, T.D., Ra jamani, S.K.: Automatic predicate
    abstraction of C programs. In: Burke, M., Soﬀa, M.L. (eds.) Proceedings of the
    2001 ACM SIGPLAN Conference on Programming Language Design and Imple-
    mentation (PLDI), Snowbird, Utah, USA, June 20-22, 2001, pp. 203–213. ACM
    (2001). https://doi.org/10.1145/378795.378846
 2. Bjørner, N.S., Janota, M.: Playing with quantiﬁed satisfaction. In: Fehnker, A.,
    McIver, A., Sutcliﬀe, G., Voronkov, A. (eds.) LPAR-20. 20th International Con-
    ferences on Logic for Programming, Artiﬁcial Intelligence and Reasoning - Short
    Presentations. EPiC Series in Computing, vol. 35, pp. 15–27. EasyChair (2015).
    https://doi.org/10.29007/vv21
 3. Bocevska, I., Tsukada, T., Unno, H., Padon, O., Shoham, S.: Lagrangian-based
    duality for quantiﬁed smt algorithms - artifact (2026). https://doi.org/10.5281/
    zenodo.19682202
 4. Bocevska, I., Tsukada, T., Unno, H., Padon, O., Shoham, S.: Lagrangian-based
    duality for quantiﬁed SMT algorithms (extended version). In: Proceedings of the
    38th International Conference on Computer Aided Veriﬁcation (CAV). Lisbon,
    Portugal (July 2026). https://hal.science/hal-05623727, hAL Id: hal-05623727
 5. Bonacina, M.P., Graham-Lengrand, S., Vauthier, C.: QSMA: A new algorithm
    for quantiﬁed satisﬁability modulo theory and assignment. In: CADE-29, pp. 78–
    95. Springer-Verlag, Berlin, Heidelberg (2023). https://doi.org/10.1007/978-3-031-
    38499-8_5
                   Lagrangian-Based Duality for Quantiﬁed SMT Algorithms             95

 6. Bonacina, M.P., Graham-Lengrand, S., Vauthier, C.: The QSMA algorithm for
    quantiﬁers in SMT. J. Autom. Reason. 69(2) (May 2025). https://doi.org/10.1007/
    s10817-025-09727-8
 7. Bradley, A.R.: SAT-based model checking without unrolling. In: Lecture Notes in
    Computer Science, pp. 70–87. Springer Berlin Heidelberg (2011). https://doi.org/
    10.1007/978-3-642-18275-4_7
 8. Chatterjee, K., Goharshady, E.K., Karrabi, M., Motwani, H.J., Seeliger, M., Žike-
    lić, u.: Quantiﬁed linear and polynomial arithmetic satisﬁability via template-based
    skolemization. In: Proceedings of the Thirty-Ninth AAAI Conference on Artiﬁcial
    Intelligence and Thirty-Seventh Conference on Innovative Applications of Artiﬁ-
    cial Intelligence and Fifteenth Symposium on Educational Advances in Artiﬁcial
    Intelligence. AAAI’25/IAAI’25/EAAI’25, AAAI Press (2025). https://doi.org/10.
    1609/aaai.v39i11.33213
 9. Clarke, E.M., Grumberg, O., Jha, S., Lu, Y., Veith, H.: Counterexample-guided
    abstraction reﬁnement. In: Emerson, E.A., Sistla, A.P. (eds.) Computer Aided
    Veriﬁcation, 12th International Conference, CAV 2000, Chicago, IL, USA, July
    15–19, 2000, Proceedings. Lecture Notes in Computer Science, vol. 1855, pp. 154–
    169. Springer (2000). https://doi.org/10.1007/10722167_15
10. Een, N., Mishchenko, A., Brayton, R.: Eﬃcient implementation of property
    directed reachability. In: Proceedings of the International Conference on Formal
    Methods in Computer-Aided Design, pp. 125–134. FMCAD ’11, FMCAD Inc,
    Austin, Texas (2011). https://dl.acm.org/doi/10.1145/3798200
11. Farzan, A., Kincaid, Z.: Linear arithmetic satisﬁability via strategy improvement.
    In: Proceedings of the Twenty-Fifth International Joint Conference on Artiﬁcial
    Intelligence, pp. 735–743. IJCAI’16, AAAI Press (2016). https://dl.acm.org/doi/
    10.5555/3060621.3060724
12. Garg, P., Löding, C., Madhusudan, P., Neider, D.: ICE: A robust framework for
    learning invariants. In: Biere, A., Bloem, R. (eds.) Computer Aided Veriﬁcation -
    26th International Conference, CAV 2014, Held as Part of the Vienna Summer of
    Logic, VSL 2014, Vienna, Austria, July 18–22, 2014. Proceedings. Lecture Notes in
    Computer Science, vol. 8559, pp. 69–87. Springer (2014). https://doi.org/10.1007/
    978-3-319-08867-9_5
13. Janota, M.: Circuit-based search space pruning in QBF. In: Beyersdorﬀ, O., Win-
    tersteiger, C.M. (eds.) Theory and Applications of Satisﬁability Testing - SAT 2018
    - 21st International Conference, SAT 2018, Held as Part of the Federated Logic
    Conference, FloC 2018, Oxford, UK, July 9–12, 2018, Proceedings. Lecture Notes
    in Computer Science, vol. 10929, pp. 187–198. Springer (2018). https://doi.org/10.
    1007/978-3-319-94144-8_12
14. Kobayashi, N., Tanahashi, K., Sato, R., Tsukada, T.: Hﬂ(z) validity checking for
    automated program veriﬁcation. Proc. ACM Program. Lang. 7(POPL) (Jan 2023).
    https://doi.org/10.1145/3571199
15. Komuravelli, A., Gurﬁnkel, A., Chaki, S.: SMT-based model checking for recursive
    programs. In: Computer Aided Veriﬁcation (CAV), pp. 17–34. Springer Interna-
    tional Publishing (2014). https://doi.org/10.1007/978-3-319-08867-9_2
16. Komuravelli, A., Gurﬁnkel, A., Chaki, S.: SMT-based model checking for recursive
    programs. Formal Methods Syst. Design 48(3), 175–205 (2016). https://doi.org/
    10.1007/s10703-016-0249-4
17. Kura, S., Unno, H., Tsukada, T.: Supermartingales for unique ﬁxed points: A uni-
    ﬁed approach to lower bound veriﬁcation (2026). https://doi.org/10.48550/arXiv.
    2504.04132
96      I. Bocevska et al.

18. Murphy, C., Kincaid, Z.: Quantiﬁed linear arithmetic satisﬁability via ﬁne-grained
    strategy improvement. In: Computer Aided Veriﬁcation: 36th International Con-
    ference, CAV 2024, Montreal, QC, Canada, July 24–27, 2024, Proceedings, Part I,
    pp. 89–109. Springer-Verlag, Berlin, Heidelberg (2024). https://doi.org/10.1007/
    978-3-031-65627-9_5
19. Reynolds, A., King, T., Kuncak, V.: An instantiation-based approach for solving
    quantiﬁed linear arithmetic. CoRR abs/1510.02642 (2015). https://doi.org/10.
    48550/arXiv.1510.02642
20. Reynolds, A., Tinelli, C., Barrett, C.: Constraint solving for ﬁnite model ﬁnding
    in SMT solvers. Theory Pract. Logic Program. 17(4), 516–558 (2017). https://doi.
    org/10.1017/S1471068417000175
21. Tsukada, T., Unno, H., Padon, O., Shoham, S.: A primal-dual perspective on pro-
    gram veriﬁcation algorithms. Proc. ACM Program. Lang. 9(POPL) (Jan 2025).
    https://doi.org/10.1145/3704904
22. Unno, H., Terauchi, T., Gu, Y., Koskinen, E.: Modular primal-dual ﬁxpoint logic
    solving for temporal veriﬁcation. Proc. ACM Program. Lang. 7(POPL) (Jan 2023).
    https://doi.org/10.1145/3571265




Op en Access This chapter is licensed under the terms of the Creative Commons
Attribution 4.0 International License (http://creativecommons.org/licenses/by/4.0/),
which permits use, sharing, adaptation, distribution and reproduction in any medium
or format, as long as you give appropriate credit to the original author(s) and the
source, provide a link to the Creative Commons license and indicate if changes were
made.
   The images or other third party material in this chapter are included in the
chapter’s Creative Commons license, unless indicated otherwise in a credit line to the
material. If material is not included in the chapter’s Creative Commons license and
your intended use is not permitted by statutory regulation or exceeds the permitted
use, you will need to obtain permission directly from the copyright holder.
