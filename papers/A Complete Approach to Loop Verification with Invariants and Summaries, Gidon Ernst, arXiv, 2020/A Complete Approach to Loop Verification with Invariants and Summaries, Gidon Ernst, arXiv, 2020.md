                                                A Complete Approach to Loop Verification
                                                    with Invariants and Summaries ?

                                                                               Gidon Ernst

                                                                    LMU Munich, gidon.ernst@lmu.de
arXiv:2010.05812v3 [cs.LO] 12 Oct 2021




                                                 Abstract. Invariants are the predominant approach to verify the cor-
                                                 rectness of loops. As an alternative, loop contracts, which make explicit
                                                 the premise and conclusion of the underlying induction proof, can some-
                                                 times capture correctness conditions more naturally. But despite this
                                                 advantage, the second approach receives little attention overall, and the
                                                 goal of this paper is to lift it out of its niche. We give the first compre-
                                                 hensive exposition of the theory of loop contracts, including a charac-
                                                 terization of its completeness. We show concrete examples on standard
                                                 algorithms that showcase their relative merits. Moreover, we demonstrate
                                                 a novel constructive translation between the two approaches, which de-
                                                 couples the chosen specification approach from the verification backend.
                                                 Keywords: Program Verification, Loops, Invariants, Contracts


                                         1     Introduction
                                         Loop invariants [34] are the standard approach to verify programs with loops.
                                         The technique is practically successful for both specifying and verifying loops in
                                         automated tools. The corresponding proof obligations propagate invariants for-
                                         wards over a single arbitrary iteration, and soundness is justified by the induction
                                         principle of the least fixpoint of the loop.
                                             The alternative approach is to specify loops in terms of a contract consisting
                                         of a precondition and a relational postconditon (called “summary” here), as ad-
                                         vocated e.g. by Hehner [29, 30]. Contracts have two important features: 1) they
                                         tend to resemble the overall program specification more closely when compared
                                         to their plain invariant counterparts, and 2) they can dually express proof argu-
                                         ments that propagate backwards from the result. Essentially, loops are treated
                                         analogously to tail-recursive procedures, but without the need for an explicit
                                         syntactic translation. The benefits of such flexible proof schemas for loops are
                                         widely acknowledged, e.g. [9, 14, 57], notably in Separation Logic, where tracking
                                         the frame is problematic with just invariants [11, 20, 41, 61].
                                             Surprisingly, while contracts have been described in the literature and im-
                                         plemented in tools such as VeriFast [55], the theoretical connection between
                                         invariants, loop pre- and postconditions, as well as completeness of the contract
                                         approach appear to be unresolved. Moreover, examples tend to be given in the
                                         context of Separation Logic but not for standard verification problems.
                                         ?
                                             This article extends a conference version at VMCAI’22 with an evaluation (Sec. 8).
Contribution and Outline: In this paper, we provide a deep investigation
of loop contacts in comparison to invariants, from a theoretical and from an
empirical point of view, leading to the following technical results:
 – We formulate contract-based verification (Sec. 4) to clearly exhibit the coinci-
   dence of invariants and loop preconditions, and the dual nature of invariants
   and loop summaries. Thereby we generalize Hoare’s approach [34]; as well
   as Hehner and Gravel’s technique for for-loops [30] to all while-loops.
 – Just as variants capture the delta between partial and total correctness,
   loop preconditions correspond to absence of runtime errors in the loop body,
   leading to yet a weaker correctness criterion for which loop summaries alone
   give a complete verification method (Thm. 4).
 – We provide constructive translations between plain invariants and loop con-
   tracts (Props. 1 and 2 in Sec. 5), which explains their parity and moreover
   provides key guidelines for building and integrating tools.
 – We reify Tuerk’s approach [61] as a syntactic proof rule (Sec. 6) that that
   lends itself directly for implementation in typical verification tools, by lever-
   aging specification statements [49].
The key take-away is that contracts offer a particular and useful way to think
about the correctness of loops, that is conceptually different from invariants, but
at the same time, the technical requirements for supporting this approach turn
out to be superficial, and tool support is straight-forward.
    As a consequence, we are at liberty to choose the approach that fits a particu-
lar problem most. But what does that mean in practice? What are the advantages
and disadvantages of contracts in comparison to invariants?
 – We specify the correctness of a number of well-known algorithms with con-
   tracts (Sec. 7), characterize when and why loop summaries may carry the
   bulk of the proof, and also give insights into their limitations.
We show that loop contracts may resemble the respective correctness require-
ments more closely and require minor generalizations only, when compared to
their invariant counterparts. Loop summaries are suitable for those properties,
which naturally propagate backwards and are thus misaligned with the forward
computation of a loop. On the other hand, they tend to require additional frame
conditions to preserve modifications of data structures across iterations.
   Finally, we are interested in proof automation:
 – We evaluate whether state-of-the-art Horn clause solvers [6, 25, 36] are ef-
   fective not only in instatiating invariants but also loop contracts (Sec. 8) in
   a side-by-side comparison on SV-COMP benchmarks [3].
Primary goal of this evaluation test whether the completeness result carries
practical significance. The results, while promising, may reflect a bias towards
invariants in existing tools: Performance of Eldarica 2.0.4 and Z3 4.8.9 with
contracts is within 90% resp. 70% of that with invariants.
Proofs: A mechanization in Isabelle/HOL [53] of the theory presented in
Sects. 4 and 5 is available at https://zenodo.org/record/5509953.


                                         2
int max(int a[], int n)                  invariant (Filliâtre & Marché)
    requires 0 < n                       •0≤l≤r<n
    ensures   a[res] = max (a[0..n])     • ∀ k. 0 ≤ k < l ∨ r < k < n
{                                                =⇒ a[k] ≤ max (a[l], a[r])
    int l = 0;
                                         invariant (Ernst, Schellhorn, Tofan)
    int r = n-1;
    while(l != r)                        ∃ k. 0 ≤ l ≤ k ≤ r < n ∧ a[k] = max (a[0..n])
      if(a[l] <= a[r]) l = l+1;          contract
      else               r = r-1;        precondition:    0≤l≤r<n
    return l;                                                0
                                         summary:         a[l ] = max (a[l..r + 1])
}                                        (primed variables refer to loop exit)

Fig. 1: Finding the maximum element in an array by elimination. Algorithm
(left) and different correctness arguments (right), which are all sufficient alone.


2     Motivation and Overview
In this section we exemplify proofs using invariants and proofs using loop con-
tracts. The running example is Challenge 1 from VerifyThis 2011 [10]: finding the
maximum in an array by elimination, as shown in Fig. 1. The program maintains
a subrange a[l..r + 1] wrt. two indices l and r of candidates for the maximum
in in array a of length n. In each iteration, the smaller of the two candidates is
eliminated from the subrange, either by incrementing l or by decrementing r.
Correctness of the algorithm depends on the fact that the maximum remains in
that range. The specification, annotated at the top left expresses that the return
value, denoted res, is equal to the result given by logic function max , where
a[0..n] denotes the non-empty sequence of array elements at indices 0, . . . , n − 1.
Specification. At the top-right of Fig. 1, two example invariants are shown.
The one used by the Why 3 team in [10] imposes an ordering on the index
variables (first •) and expresses that both the left part and the right part of the
array contains elements that have been rightfully excluded, i.e., one of the two
boundary values is greater than all of these (second •). The invariant discovered
by the KIV team expresses that there remains some index k within the range
that is maximum of the whole array, implying that this range remains non-empty
for the maximum to be well-defined. In both cases, the program’s postcondition
follows from the invariant when the loop guard becomes false, i.e, when l = r.
    We can alternatively specify the loop using a contract, which consists of a
loop precondition, later called a “safe” invariant (cf. Def. 4), whose role is to guar-
antee that the loop executes without error, and a summary, which establishes
functional correctness. The latter is a relation between current unprimed values
and primed final values of the program variables. From whichever intermediate
indices l and r we jump into the execution of the loop, the element at the final
index l0 will be maximal for that subrange. The specification of the program is
implied for l0 = res wrt. initial values l = 0 and r = n −1. The loop precondition
is about the ordering of indices to keep track that the range remains nonempty.


                                          3
 P (s0 ) =⇒ I(s0 )           I(si ) ∧ t(si )   =⇒ I(si+1 )          I(sn ) ∧ ¬t(sn ) =⇒ Q(sn )
                                           body
         s0                         si                 si+1                        sn

 Fig. 2: Forward propagation of invariant I. Blue: assumptions, red: to prove.


     Note that first, the contract reflects the intuition behind the algorithm more
naturally: It computes a final index l0 that points to the maximum. Moreover,
this summary occurs almost verbatim in the annotation of procedure max, albeit
with the fixed bounds 0 and n that have to be generalized (such generalization
is, of course, unavoidable). In Sec. 5 we show a third possibility to state an
invariant, motivated by and constructed from this summary.
Proofs. Schematically, we can describe the execution of the loop, using logical
variables li and ri indexed by the i-th iteration, for i = 0, . . . , n, where l0 = 0,
r0 = n − 1, and ln = rn . We denote by I(li , ri ) the instantiation of (either of
the) invariants with l, r 7→ li , ri . Similarly, R(li , ri , ln , rn ) is the instantiation of
the summary, with l, r 7→ li , ri and l0 , r0 7→ ln , rn (note that r0 does not occur).
Hence, I describes all states encountered loop head, including when the loop
is entered first and right when the loop exits. R describes the relation between
these states at loop head and the final states at loop exit.
     The proof that an invariant I is correct considers the usual three conditions,
visualized in Fig. 2. I(l0 , r0 ) holds initially, I(li , ri ) =⇒ I(li+1 , ri+1 ) propagates
forwards through iterations for each i, and I(ln , rn ) =⇒ Q(ln , rn ) finally estab-
lishes the postcondition Q of max. With some knowledge about function max , it
is easy to check that both invariants shown in Fig. 1 satisfy these conditions.
     Dually, the proof that R is indeed a correct summary also considers three
conditions, as visualized in Fig. 3: We need to check that R(ln , rn ) holds finally,
i.e., the poscondition adequately summarizes the computation of a loop that
terminates immediately, R(li+1 , ri+1 , ln , rn ) =⇒ R(li , ri , ln , rn ) for all i ensures
that an additional leading iteration is covered, too. As a result, the entire com-
putation of the loop is summarized by R, from which we need to establish the
postcondition of max by R(l0 , r0 , ln , rn ) =⇒ Q(ln , rn ).
     We briefly sketch the critical step of backwards propagation for the R shown
in Fig. 1, in the case that a[l] <= a[r] evaluates to true in the i-th iteration.
Specifically, given that li+1 = li + 1 and ri+1 = ri , from
              R(li+1 , ri+1 , ln , rn )    ≡      a[ln ] = max (a[li+1 ..ri+1 + 1])         (1)
we propagate R from state i + 1 back to state i, where
                   R(li , ri , ln , rn )   ≡      a[ln ] = max (a[li ..ri + 1]).            (2)
Using equality max (a[li ..ri + 1]) = max (a[li ], max (a[li + 1..ri+1 + 1])) and sub-
stituting variables, it remains to be proven that a[ln ] = max (a[li ], a[ln ]), i.e.,
a[li ] ≤ a[ln ], which follows by transitivity from the if condition a[li ] ≤ a[ri ] and
a[ri ] ≤ a[ln ] as a consequence of (1). We remark that these reasoning steps are
easy for automatic provers when provided with the obvious properties of max .


                                                   4
                                                                            ¬t(sn ) =⇒ R(sn , sn )
                                             body
        s0                       si                      si+1                        sn

                                                         assume R(si+1 , sn ) ∧ t(si )

                                                        prove R(si , sn )

                  finally prove P (s0 ) ∧ R(s0 , sn ) =⇒ Q(sn )

Fig. 3: Backward propagation conditions for a loop postcondition R with respect
to an iteration of the loop. Whe overall conclusion is marked green.


3     Preliminaries

We consider imperative commands C, defined over a semantic domain of states S,
as relations C ⊆ S × Ŝ with Ŝ = S ] { } ] {s↓ | s ∈ S}, where signifies a
runtime error (e.g. failed assertion, division by zero, out of bounds array access),
and s↓ signifies early exit of a loop via a break command in state s. By notational
convention ŝ ∈ Ŝ, whereas s ∈ S strictly. Nontermination, which is orthogonal
to this paper, is reflected by the absence of successor states as usual. We use
suggestive naming, e.g. state s0 ∈ S is used for the initial state of some execution,
s, s0 , s00 are intermediate states, and sn typically refers to a final state of the loop.

Definition 1 (Validity of Hoare-Triples). A command C ⊆ S × Ŝ is par-
tially correct wrt. a precondition P ⊆ S and a postcondition Q ⊆ S, if the Hoare
triple { P } C { Q } is valid, written |= { P } C { Q }, and defined as usual

         |= { P } C { Q }      iff         ∀ s, ŝ0 . P (s) ∧ C(s, ŝ0 ) =⇒ ŝ0 ∈ S ∧ Q(ŝ0 )

Given a starting state s with P (s), the possible final states ŝ0 after executing com-
mand C satisfy two constraints: They must be regular states ŝ0 ∈ S, ruling out
runtime errors in the loop body, and they must satisfy the postcondition Q(ŝ0 ) of
the triple. Analogously to splitting total correctness into termination and partial
correctness, we separate these aspects of safe execution and correctly establishing
the postcondition into two semantic judgements:

Definition 2 (Safety and Correctness of Hoare-Triples).

             { P } C is safe         iff     ∀ s, ŝ0 . P (s) ∧ C(s, ŝ0 ) =⇒ ŝ0 ∈ S                (3)
                                                    0                       0    0               0
    { P } C { Q } is correct         iff     ∀ s, ŝ . P (s) ∧ C(s, ŝ ) ∧ ŝ ∈ S =⇒ Q(ŝ )          (4)

which clearly satisfy this correspondence:

         |= { P } C { Q }      iff          { P } C is safe and { P } C { Q } is correct             (5)


                                                         5
Definition 3 (Semantics of Loops). Semantically, a loop W (t, B) ⊆ S × Ŝ
with test t ∈ S and body B ⊆ S × Ŝ is defined as the least fixpoint of
                                            ¬t(s) =⇒ W (t, B)(s, s)
                                  t(s) ∧ B(s, ) =⇒ W (t, B)(s, )
                                  t(s) ∧ B(s, s0↓ ) =⇒ W (t, B)(s, s0 )
              t(s) ∧ B(s, s0 ) ∧ W (t, B)(s0 , ŝ00 ) =⇒ W (t, B)(s, ŝ00 )
The first condition terminates the loop, the second condition propagates errors
in the body, the third condition propagates early loop exit, and the last condition
unrolls the loop once if the first iteration results in a regular state s0 ∈ S.
    In the following we are concerned in verifying correctness of a loop W (t, B)
wrt. pre-states P and post-states Q, as expressed by |= { P } W (t, B) { Q }, re-
spectively its constitutents of “safe” and “correct” execution via (5).


4   Verification of Loops with Invariants and Contracts
This section succinctly states the approach to the verification with invariants
and loop contracts, and we prove soundness and completeness theorems. The re-
sults have been mechanized in Isabelle/HOL [53]. The presentation here is based
on systems of cyclic Horn clauses [6]. Subsequently, we mark those conditions
dealing with runtime errors by (†), and those dealing with breaks by (‡).
Definition 4 (Loop Invariants, Floyd [22], Hoare [34]). Predicate I ⊆ S
is an inductive invariant of loop W (t, B) wrt. pre-state described by P ⊆ S, if
                                 P (s0 ) =⇒ I(s0 )
                I(s) ∧ t(s) ∧ B(s, s0 ) =⇒ I(s0 )       (when s0 ∈ S)
An inductive invariant I is safe wrt. executions of the loop body B, if
                          I(s) ∧ t(s) ∧ B(s, ) =⇒ false                         (†)
An inductive invariant I is correct wrt. a post-states Q ⊆ S, if
                                 I(sn ) ∧ ¬t(sn ) =⇒ Q(sn )
                        I(s) ∧ t(s) ∧ B(s, sn↓ ) =⇒ Q(sn )                      (‡)
The first condition establishes I initially, the second propagates I over a single
iteration of the body otherwise. The third condition (†) prevents errors in the
body. The last two lines ensure Q upon regular termination of the loop, as well
as directly after a break. Note, Q(s) does not necessarily imply ¬t(s), i.e., we
cannot take the negative loop test for granted if there are non-local exits of the
loop by break.
    Relational invariants J ⊆ S ×S are sometimes convenient [50], where J(s0 , s)
additionally tracks the state s0 when the loop was entered first, which can of
course be encoded with auxiliary variables as I(s) := ∃ s0 . P (s0 ) ∧ J(s0 , s).


                                           6
   It is clear that we have chosen the notions of safe and correct invariants to
mirror precisely the semantic counterparts of safe and correct loops, respectively:

Theorem 1 (Soundness of Loop Invariants). For a loop W (t, B),
 – given a safe invariant I wrt. P then { P } W (t, B) is safe, and
 – given a correct invariant I wrt. P and Q then { P } W (t, B) { Q } is correct
Proof. We prove I(s) ∧ W (t, B)(s, ŝ0 ) =⇒ ŝ0 ∈ S ∧ Q(ŝ0 ) (first claim), resp.
I(s) ∧ W (t, B)(s, ŝ0 ) ∧ ŝ0 ∈ S =⇒ Q(ŝ0 ) (second claim), each by induction over
the least fixpoint of Def. 3 using the relevant conditions from Def. 4.           
Theorem 2 (Completeness of Loop Invariants). For a loop W (t, B),
 – if { P } W (t, B) is safe then there exists a corresponding safe invariant I
 – if { P } W (t, B) { Q } is correct, there is a corresponding correct invariant I
 – if |= { P } W (t, B) { Q }, there is an invariant I that is safe and correct
Proof. Inductive invariant λ s. ∃ s0 . P (s0 ) ∧ I ∗ (s0 , s) proves all three claims,
where I ∗ ⊆ S × S is the strongest relation that characterizes regularly terminat-
ing loop iterations, defined as the least fixpoint of:
                                              ¬t(s) =⇒ I ∗ (s, s)
                     t(s) ∧ B(s, s0 ) ∧ I ∗ (s0 , s00 ) =⇒ I ∗ (s, s00 )
We omit some technical lemmas that connect I ∗ with W (t, B).                       
    The result states that all critical pieces of information (e.g. outcome of loop
test t) and key reasoning features from the underlying induction proof are re-
flected somehow in the constraints of Def. 4. Of course, reasoning about I ∗ is by
no means easier than a proof using the semantic definition and the challenge in
practice is to find closed-form solutions in a given background theory.
Definition 5 (Loop Contract). A (correct) loop contract I, R consists of a
loop precondition I that is a safe invariant, and a correct summary R (cf. below).
   The precondition of a loop contract, as discussed previously, is just a safe
invariant (cf. Def. 4). The summary component of a contract is a relation R ⊆
S × S that characterizes remaining iterations, such that R(s, sn ) holds between
any intermediate state s at loop head and final state sn at loop exit.
Definition 6 (Loop Summary). Relation R ⊆ S × S is a summary of a loop
W (t, B) wrt. precondition P ⊆ S, if
                                            ¬t(sn ) =⇒ R(sn , sn )
                     t(s) ∧ B(s, s ) ∧ R(s0 , sn ) =⇒ R(s, sn )
                                    0


                                t(s) ∧ B(s, sn↓ ) =⇒ R(s, sn )                    (‡)
A summary R is called correct for a postcondition Q ⊆ S, if
                           P (s0 ) ∧ R(s0 , sn ) =⇒ Q(sn )


                                             7
The first line establishes that R holds reflexively at a regular loop exit, as the
dual of the initialization condition of invariants. The second line lifts R of from
remaining iterations until termination of the loop to a summary that accounts
for an additional leading iteration, whereas the third line (‡) establishes that R
summarizes the last partial execution of the loop body upon a break.
    The last line applies the relation R to the original pre-state s0 that satisfies P
to establish Q. Assumption P (s0 ) is the counterpart to the negated loop test
¬t(sn ) in the exit condition of Def. 4. If the loop body B does not contain breaks
at all—which can be checked syntactically— we may enrich R(s, sn ) with ¬t(sn )
for free, effectively adding it as an assumption in line three.
    There is no safe counterpart for summaries, because they wrap up a loop
execution after the fact when it would be too late to catch runtime errors.
    Loop contracts implicitly translate a loop into a tail-recursive procedure. The
summary, taking the role of its postcondition, can then be interpreted as a rela-
tion between the parameters of the procedure and its return value. This provides
an intuitive justification why non-relational of summaries are not adequate.1

Theorem 3 (Soundness of Summaries). Given a correct summary R of loop
W (t, B) that satisfies Def. 6 wrt. P and Q, then { P } W (t, B) { Q } is correct.

Proof. We prove W (t, B)(s, ŝ0 ) ∧ ŝ0 ∈ S =⇒ R(s, ŝ0 ) by induction over the least
fixpoint from Def. 3, the claim follows.                                           

   Of course, it is possible to strengthen the conditions of Def. 6 by known
inductive invariants, occurring as additional assumptions. While this is rather
convenient in practice, it is not necessary in theory:

Theorem 4 (Completeness of Loop Summaries). For a loop W (t, B), if
{ P } W (t, B) { Q } is correct, then there exists a corresponding loop summary R.

Proof. We take R∗ ⊆ S × S, defined as least fixpoint of

                                              ¬t(s) =⇒ R∗ (s, s)
                      t(s) ∧ B(s, s0↓ ) ∧ R∗ (s0 , s) =⇒ R∗ (s0 , s0 )
                      t(s) ∧ B(s, s0 ) ∧ R∗ (s0 , s00 ) =⇒ R∗ (s, s00 )

This R∗ is the strongest relation that characterizes terminating loop iterations,
possibly ending with a break command (in contrast to I ∗ of Thm. 2). We rely
on the presence of P (s0 ) in the third condition of Def. 6: R∗ (s0 , sn ) implies
W (t, B)(s0 , sn ), which proves Q(sn ) via validity of the Hoare triple.       

Corollary 1 (Adequacy of Loop Contracts). |= { P } W (t, B) { Q } if and
only if there exists a corresponding loop contract I, R wrt. P and Q.
1
    Dually to invariants, non-relational version of summary R would quantify over final
    states as ∀ s0 . ¬t(s0 ) =⇒ R(s, s0 ), but that condition is too strong at loop exit.


                                              8
5    Translating between the Approaches

Having soundness and completeness of both approaches from Sec. 4 we now
characterize their relationship.

Corollary 2. For a given loop W (t, B) there exists a safe and correct invari-
ant I that satisfies Def. 4 wrt. P and Q, if and only if there exists a correct
contract J, R such that J is a safe invariant and R satisfies Def. 6.

Proof. In both directions, we have that |= { P } W (t, B) { Q } by Thms. 1 and 3,
respectively, the claim then follows by Thms. 2 and 4.                         

    This corollary is of course not surprising, but the proof via the completeness
theorems and the underlying constructions I ∗ and R∗ is unsatisfactory. A direct
translation that avoids these artifacts is clearly more useful, by constructing I
from J and R, and vice-versa, R from I and Q, as shown with Props. 1 and 2.
Not only does this give a direct and obvious proof of Cor. 2, it also tells us how
to integrate tools for the respective approaches as discussed subsequently.

Proposition 1 (Invariants from Contracts). Given a contract J, R that
satisfies Def. 6, then I is a safe and correct invariant that satisfies Def. 4, where:
                                                                           
          I(s) := ∃ s0 . P (s0 ) ∧ J(s) ∧ ∀ sn . R(s, sn ) =⇒ R(s0 , sn )          (6)

The first conjunct keeps track of the initial state s0 that satisfies P , which is
needed to make use of the last property of R in Def. 6. The second conjunct
tracks the safe invariant J, whereas the third conjunct predicts that the loop
summary wrt. the remaining iterations between current state s and an arbitrary
final state sn can be lifted to a summary of the whole execution beginning at s0 .

Proof. We prove conditions of Def. 4 for the lifted invariant (6). The interest-
ing part is the choice of sn in (6), which is immediate for the loop exit cases
with ¬t(sn ) resp. sn↓ . Otherwise, sn is the same for both instances of I when
propagating it over the iteration of the body.                                

    Prop. 1 has immediate application in verification tools: Contracts can be
supported straight-forward in as a front-end feature of a deductive verifier like
Dafny [45] that takes specifications from the user. The only necessary extensions
are adding contract annotations to loops and expressing relational predicates,
e.g., with the widely-used old keyword or special naming conventions as in Veri-
Fast [55]. The analogue of (6) appears to be useful in Separation Logic [56], too.
It has has been noted in a similar form in [60] as an encoding of Tuerk’s ap-
proach [61], but it is presented less precisely wrt. the states involved (cf. Sec. 9).
   Conversely to Prop. 1, a tool with first-class support for contracts can be
turned into a purely invariant-based verifier. The gap between the conditions of
Def. 4 and Def. 6 wrt. condition Q can be closed by canonical summaries:


                                          9
Proposition 2 (Contracts from Invariants). If I is a safe and correct in-
variant then I, R is a correct contract, where

  R(s, sn ) := I(s) =⇒ ¬t(sn ) ∧ I(sn ) for loops without break            (7)
  R(s, sn ) := I(s) =⇒ Q(sn )           for all loops, possibly with break (‡)

Intuitively, these summaries characterize that if we jump into the loop with a
state s that satisfies the invariant I(s), then the remaining iterations will estab-
lish precisely what can be derived from Def. 4 for the final state sn , respectively.
Proof. We prove the conditions of Def. 6 for this R from Def. 4 for I. Premise
I(s) is needed for the respective exit properties of I to demonstrate R(sn , sn )
when the loop terminates in s = sn . Negative polarity of I(s) turns the known
forward propagation of I into the required backward propagation of R.         
    While technically correct, the constructions (6) and (7) produce rather large
and unwieldy formulas. One might furthermore worry that the introduction of
the universal quantifiers into invariant (6) hampers proof automation when R
is a complex formula, indeed, Dafny would typically fails to infer appropriate
triggers for it. There is a class of properties where the overhead of the respective
translation disappears completely. This is the case when we are interested in
tracking a function f (x) over state variables x (or analogously a predicate p(x)).


Proposition 3 (Functional Invariants and Summaries). For a loop W (t, B)
with precondition P and program variables x, y:

 – ∃ x0 . P (x0 ) ∧ f (x) = f (x0 ) is an invariant iff f (x0 ) = f (x) is a summary
 – y 0 = f (x) is a summary implies that f (x) = f (x0 ) is an invariant

merely by simplifying the result of the respective translations (6) and (7).                  
Note, the two cases coincide when f (x0 ) = y 0 for all final x0 , y 0 with ¬t(x0 , y 0 , . . .).
Example: Recall the specification of the loop in max from Fig. 1 using loop
precondition 0 ≤ l ≤ r < n and summary a[l0 ] = max (a[l..r + 1]). Given
that finally l = r, the invariant constructed via Prop. 1 simplifies to:

         invariant         0 ≤ l ≤ r < n ∧ max (a[l..r + 1]) = max (a[0..n])                 (8)

In Sec. 7 we will see that this simplification applies fairly often in practice and
can uncover invariants that are notably different from the textbook solutions,
yet conceptually simple and insightful in some sense. Simplifying the translation
in the converse direction can work nicely, too. Recovering reasonable summaries
from the invariants from Sec. 2, however, is challenging. We do not necessarily
expect the reader to follow all the details, but for completeness of discussion we
do include an example for the invariant of the KIV team.
Example: The KIV invariant has the form I(s) ≡ ∃ k. J(k, s) where J consists
of two conjuncts, 0 ≤ l ≤ k ≤ r < n and a[k] = max (a[0..n]). We now construct


                                               10
a summary following (7) (first variant), by simplification steps as well as some
heuristic weakening to obtain the original summary shown in Sec. 2 as (9) below.
   Critically, we choose the same k for both occurrences of I in (7), i.e., yielding
J(k, s) =⇒ ¬t(sn ) ∧ J(k, sn ) abstractly, which makes explicit the functional
dependency for a[k] for that k. This roughly corresponds to the intuition that
such a fixed index k can be determined (deterministically) upfront. Moreover,
we make use of the following fact

       lemma 0 ≤ l ≤ k ≤ r < n =⇒ max (a[0..n]) = max (a[l..r + 1])

to generalize all occurrences of max (a[0..n]), and we note that the loop terminates
with l0 = k = r’, such that ¬t(sn ) ∧ I(sn ) simplifies to

             summary 0 ≤ l0 = r0 < n ∧ a[l0 ] = max (a[l..r + 1])               (9)


6   Loop Contracts in Hoare Logic

In this section we present a Hoare logic proof rule for the verification of loops
with contracts that lends itself to a straight-forward implementation. The ap-
proach works analogously with strongest postcondition and weakest precondition
predicate transformers, as explained in Alexandru’s thesis [2]. The idea mirrors
that of Tuerk [61], however, he uses a shallow embedding of formulas, programs,
and Hoare triples in the higher-order logic of the HOL system. The inductive
case for one iteration of the body B with test t is expressed in [61] as
                                      
    ∀ x, C. ∀ y. { P (y) } C { Q(y) } =⇒ { t(x) ∧ P (x) } B; C { Q(x) }      (10)

where the premise of the implication amounts to the inductive hypothesis for
the remaining loop iterations, abstracted here by arbitrary the command C. The
primary question is how to represent the inductive hypothesis in (10) without es-
caping to the meta-level with Hoare triples as first-class objects. The key insight
is that specification statements (Morgan [49]) lead to an elegant formulation as
rule LoopContract below.
    To this end, we make the distinction between syntax and semantics more
precise: Predicates P, Q, I, R are represented as formulas here, where a relational
summaries R may refer to primed variables as in Sec. 2. By P [x 7→ y] we denote
the parallel renaming of variables x to y in P , where by convention we overline
vectors of variables x. Derivability of Hoare triples is written ` { P } C { Q }. We
omit treatment of break for simplicity, see e.g. [37].
    A specification statement x : [P, Q] has a precondition P , a set of variables x
that are nondeterministically modified, and a relational postcondition Q that
constrains the transition. The proof rule for the specification introduces new
logical variables that capture the pre-state, and removes the primes in Q:
                                   x0 fresh
                                                             Spec
                   ` { P } x : [P, Q] { Q[x, x0 7→ x0 , x] }


                                        11
   The proof rule to verify a loop while t do B with test t and body B using
a contract I, R is show below. The variables x = mod(B) are those modified by
body B, and x0 , xi , xn are fresh logical variables capturing intermediate states.

                    ` { P } x : [I, R] { Q }
       ` { I ∧ ¬t ∧ x = xn } skip { R[x, x0 7→ xn , x] }
     ` { I ∧ t ∧ x = xi } B; x : [I, R] { R[x, x0 7→ xi , x] }
                                                                 LoopContract
                  ` { P } while t do B { Q }

The first premise abstracts the computation of the entire loop in terms of its
contract I, R using a specification statement. From rule Spec, proof obligations
akin to those in Def. 6 are immediate via an application of the consequence
rule. The second premise terminates the loop when ¬t, the variables xn cap-
ture this final state. We encode the corresponding proof obligation as a Hoare
triple with command skip,2 which is equivalent to I ∧ ¬t =⇒ R[x, x0 7→ x, x],
mirroring the exit condition from Def. 6. The third premise, in contrast to (10),
embeds the inductive hypothesis directly into the program as specification state-
ment x : [I, R] that summarizes the remaining iterations after executing B once.
Variables xi capture the state right before B is executed for later reference in
the postcondition, whereas the reference to the intermediate state i + 1 after B,
needed for R in x : [I, R], is handled implictly via rule Spec. Thus, rule Loop-
Contract nicely retains the syntax-oriented, compositional nature of Hoare’s
approach.


7   Specification of Examples and Comparison

In this section we specify some verification challenges using invariants and con-
tracts. The examples are chosen not for their difficulty, but because they high-
light specific aspects, advantages, and limitations of the respective approaches.
    Throughout, we employ the old keyword in loop preconditions resp. invari-
ants to refer back to the state before the loop. Variables in procedure annotations
always refer back to the initial values of the parameters and res denotes the re-
sult value returned by the procedure. Moreover, we factor out the part of the
verification that is common to both approaches, in terms of a loop precondition
that one should understand as part of the invariant as well as the loop contract.
Finally, for those algorithms that do not contain break, we implicitly assume
that the negated loop test is made part of the summary (cf. Def. 6 and Prop. 2).
Fast Exponentiation. The fast exponentiation algorithm computes xn by
traversing over the binary representation of the exponent n. The program3 tracks
a multiplier 2p for each binary digit that is applied to the intermediate result r
2
  Tuerk [61] remarks that, more generally, the inductive hypothesis may encompass a
  subsequent program fragment C right after the loop, i.e., while t do B; C, and this
  (concrete) C would then replace skip in the second premise, with x = mod(B, C).
3
  Presentation adapted from http://toccata.lri.fr/gallery/power.en.html


                                          12
only if a binary digit is set to one, where residual exponent e continuously shifts
right such that the lowest significant binary digit of e always corresponds to p.
   int fastexp(int x, int n)
     requires 0 ≤ n
     ensures res = xn
   {                                            precondition (both)
       int r = 1, p = x, e = n;                 0≤e
       while(e > 0) {
                                                invariant
         if(e%2 == 1)
                                                r · pe = xn
           r = r * p;
         p = p * p;                             summary
         e = e / 2;                             r0 = r · pe
       }
       return r;
   }

    Both the invariant as well as the summary require the same kind of gener-
alization, to account for the the intermediate result in variable r. This example
admits a functional characterization according to Prop. 3. The route from the
summary to the invariant is straight-forward, the converse can be best under-
stood by noting that the initial values of r, p, e denoted r0 , p0 , e0 as in Sec. 2,
coincide with 1, x, and n, such that the invariant can be written as r · pe = r0 · pe00 .
Linear Search. Linear search, as shown below, traverses an array a of length n
from front to back using index i to find an element x. To avoid using return
inside the loop (which we have not formalized in Sec. 4) we maintain a variable r
that becomes true once the element is found, in which case we break out of the
loop. Remember that in this case we establish the postcondition of the procedure
directly, such that ¬r is a valid invariant.
   bool lsearch(int x, int a[], int n)
     requires 0 ≤ n                                 precondition (both)
     ensures res ⇐⇒ x ∈ a[0..n]                     0 ≤ i ≤ n ∧ ¬r
   {
     int i = 0; bool r = false;
                                                    invariant
       while(i < n) {                               x∈/ a[0..i]
         if(x == a[i])                              summary
           { r = true; break; }
                                                    r0 ⇔ x ∈ a[i..n]
         i++;
       }                                            invariant via Prop. 1
       return r;                                    x ∈ a[i..n] ⇔ x ∈ a[0..n]
   }

    The common condition is about the range of the index variable i and the
fact that the loop head is encountered only with when r is false. The invariant
states, as expected, that the element has not been found yet in the initial range
up to and not including i. The loop postcondition states that the final value

                                           13
of r, denoted r0 , will indicate whether the element is found in the remaining
range between i and n. It is quite similar to the procedure contract of lsearch,
requiring only the generalization of the lower bound. Moreover, given ¬r, if we
write the invariant equivalently as r ⇔ x ∈ a[0..i], then the respective approaches
become entirely symmetric. The loop invariant lifted from the postcondition via
Prop. 1 gives a nice alternative characterization of the work that remains to be
done (searching from i) in relation to the overall work to be achieved.
Binary Search. In contrast to linear search, binary search tracks two indices,
somewhat similarly to maximum by elimination from Sec. 2. The code is shown
below, using lower index l and upper index u (both inclusive).
     bool bsearch(int x, int a[], int n)
       requires 0 ≤ n ∧ sorted (a)
       ensures res ⇐⇒ x ∈ a[0..n]               precondition (both)
     {                                          0 ≤ i ≤ n ∧ ¬r
         int l = 0, u = n-1;
         bool r = false;
                                                invariant
         while(i < n) {                         x∈/ a[0..l] ∧ x ∈
                                                                / a[u + 1..n]
           int m = (l+u) / 2;                   summary
          if (x > a[m])      { l = m+1; }
                                                r0 ⇔ x ∈ a[l..u + 1]
          else if (x < a[m]) { u = m-1; }
          else       { r = true; break; }       invariant via Prop. 1
         }                                      x ∈ a[l..u + 1] ⇔ x ∈ a[0..n]
         return r;
     }

    The invariant for binary search now excludes two sub-ranges of the array,
whereas the summary incorporates only the minor additional generalization for
the upper bound from n to u + 1. Like in max from Sec. 2 but unlike with linear
search, the array is divided into three logical parts, of which the shown invariant
considers two, whereas summaries can zoom into the single remaining part. This
effect has been noted by Furia and Meyer [24, Sec. 2.3] where it is addressed by
a heuristic called “uncoupling” that splits up ranges as needed. With respect to
binary search and similarly maximum by elimination from Sec. 2, approaching
the problem via contracts leads to a nice invariant via Prop. 1 that avoids such
uncoupling.
Phone Number Comparison. Summaries can mediate between a forward
computation, which is effectively a “left-fold”, and a correctness condition that
is a “right-fold” (cf. [40]). This case occurs e.g. when the logical specification
uses an intermediate abstraction step to algebraic lists or sequences, over which
functions and predicates are typically specified by structural recursion.
    Consider the comparison of phone numbers4 by ignoring non-digit characters.
As an example, the phone numbers (0) 12/345 and 01-2345 should be regarded
the same, whereas 1-23-45 is different because of the missing leading 0.
4
    Example communicated by Rustan Leino, who based his verification on Eq. (11)..


                                         14
   bool compare(int a[], int m, int b[], int n)
     ensures res ⇐⇒ filter (isdigit, a[0..m]) = filter (isdigit, b[0..n])
   {
     bool r = false;
     int i = 0, j = 0;
       while(true) {
         if(i == m && j == n)                    { r = true; break; }
         else if(i < m && !isdigit(a[i])         { i++; }
         else if(j < n && !isdigit(b[j])         { j++; }
         else if(i < m && j < n && a[i] == b[j]) { i++; j++; }
         else                                             { r = false; break; }
       }
       return r;
   }

    The algorithm keeps two indices, i and j, into arrays a and b that store the
characters of the respective numbers, of lengths m and n. The algorithm consists
of a loop that increments i and j according to several cases until the numbers
are fully compared (first if) or a mismatch is detected (last else). If a[i] is not a
digit then i moves forwards, similarly j for b[j], and both jointly move forward
over two equal digits. The result of the comparison is returned via variable r as
previously.
    A nice specification of this algorithm is in terms of algebraic lists, constructed
from nil and cons, where a[i..j] denotes cons(a[i], cons(. . . , cons(a[j − 1], nil))),
the list of the elements from index i to and including j − 1 of a. We rely on
a function filter that keeps only those elements in the list that satisfying a
predicate p. Filtering is defined by structural recursion over the algebraic list:
                    filter (p, nil) = nil
                                      (
                                       cons(x, filter (p, xs)),   if p(x)
           filter (p, cons(x, xs)) =
                                       filter (p, xs)),           otherwise.
    With these prerequisites, the specification of procedure compare states that
the boolean result indicates whether filtering for digits only produces identical
lists. An obvious candidate for the invariant follows the idea from linear search,
and generalizes the upper bounds of the ranges compared from the array length
to the respective counter variable:
   invariant (problematic) filter (isdigit, a[0..i]) = filter (isdigit, b[0..j])
While correct, the approach has the significant drawback that we need a lemma
that unfolds the recurrence of filter (p, a[0..k + 1]) at the end instead of the
front like the definition, to accommodate the index increments, which in turn
is provable by induction only after a further generalization of the lower index
from 0 to a variable. Overall, this approach is somewhat cumbersome, and can
be avoided when the solution is approached with loop contracts:
       summary r0 ⇐⇒ filter (isdigit, a[i..m]) = filter (isdigit, b[j..n])

                                            15
for which the proof is straight-forward, and from which we immediately get an
equally easy to prove invariant by Prop. 1:

         invariant         filter (isdigit, a[0..m]) = filter (isdigit, b[0..n])   (11)
                     ⇐⇒ filter (isdigit, a[i..m]) = filter (isdigit, b[j..n])

The shown mismatch between the natural direction of the loop vs. that of the
property is correlates to the insight that for some algorithms, a recursive version
is easier to verify, and some tools explicitly translate loops into recursive proce-
dures to that end [8]. Using loop contracts, one can avoid this intermediate step.
For a similar discussion in the context of separation logic we refer to [39, 61].
    We emphasize that it is not always possible to factor out specification func-
tions like filter nicely and to defer the complexity of additional lemmas to a
library, as one might be inclined to suggest. When such functions are specific to
the case study, or simply when higher order functions are not supported by the
tool, the ability to base the loop specification on right-fold loop summaries is
certainly a useful trick in the bag that deserves to be treated first class.
Array Copy. We turn to programs that manipulate arrays, which uncovers
a deficit of summaries. Recall that loop contracts reason about three states, an
initial one s0 , an intermediate one s, and a final one sn (cf. Fig. 3), whereas
invariants reason only about the first two. While it increases expressive power as
demonstrated above, it comes at a cost, too: Summarizing the remaining loop
iterations from s to the final state sn by summary R(s, sn ) does not automatically
reflect the array modifications applied to get from s0 to s. This occurs in the
program below that copies n entries from array a to b. This is an instance of the
more general problem of framing, that is long known [12] and well studied. A
comprehensive treatment is beyond the scope of this paper, but we show how it
surfaces in the example.
   void copy(int a[], int b[], int n)
     requires 0 ≤ n                                precondition (both)
     ensures b[0..n] = a[0..n]                     0≤i≤n
   {
                                                   invariant
       int i = 0;
                                                   b[0..i] = a[0..i]
       while(i < n) {
         b[i] = a[i];                              summary
         i = i+1;                                  b0 [0..i] = b[0..i]
       }                                           b0 [i..n] = a[i..n]
   }

     The expected invariant specifies that the prefix up to current index i has been
copied already. Analogously, the summary predicts that executing the remainder
of the loop will copy the suffix starting from i into the resulting array b0 (second
equation in the listing). However, that is not enough: In the back-propagation
step from i + 1 to i, from b0 [i + 1..n] = a[i + 1..n] alone we cannot conclude
b0 [i..n] = a[i..n] because the assignment to the entry b[i] in the current entry
does not appear anywhere, it is “forgotten”. The condition missing from the

                                          16
summary is that the remaining iterations do not touch the indices again that
were modified so far, i.e., that the lower range of b is unmodified.
Bubble Sort. We now turn to sorting algorithms, which are a classic example,
starting with bubble sort. It turned out to be somewhat tricky to get out of
the mindset associated with invariants, and to find a nice notation for a natural
specification. Again, framing is crucial, and we will do it explicitly, in terms of
comparing array ranges a[i..j] = b[i..j]. In similar spirit, by a[i..j]   b[i..j] we
denote that the array range a[i..j] is a permuation of b[i..j], which is equivalent
to stating that the multiset of elements on both sides are the same (a com-
mon encoding in Dafny). The code is shown below, together with a graphical
visualization.
   void bubblesort(int a[], int n)
     requires 0 ≤ n
     ensures a    old(a)
     ensures sorted (a)
   {
       for(int i = n; i > 1; i--)
         for(int j = 0; j < i-1; j++)
           if(a[j] > a[j+1])
             swap(j, j+1, a);
   }

    The algorithm gradually constructs a sorted suffix of the array, which is
shaded in grey in the figure on the right. Goal of the inner loop is to move the
largest element in the prefix up to the boundary of the sorted range, as visualized
by the arrow. The loop specifications are shown below.
    Outer Loop                               Inner Loop
   precondition (both)                        precondition (both)
   0≤i<n                                      0≤j<i≤n
   invariant                                  invariant
   a    old(a)                                a[0..i]   old(a[0..i])
   max (a[0..i]) ≤ max (a[i..n])              a[i..n] = old(a[i..n])
   sorted (a[i..n])                           0 < j =⇒ a[j] = max (a[0..j])
   summary                                     summary
   a0 [0..i]    a[0..i]                        a0 [0..j] = a[0..j]
   a0 [i..n] = a[i..n]                         a0 [j..i]   a[j..i]
   sorted (a0 [0..i])                          a0 [i..n] = a[i..n]
                                               a0 [i − 1] = max (a0 [j..i])
    In both approaches, we keep track of which parts of the array have been
permuted and which are unchanged, albeit the summary is more precise for
both loops to account for the frame problem already seen with array copy.
    The approaches for both loops are typically symmetric: as already seen with
linear search, the invariant refers to properties of the prefix whereas the summary
refers to properties of the suffix. For the inner loop it suffices to keep track


                                        17
of where we have placed the maximum of that range. For the outer loop, we
establish that a particular part is already sorted.
    Interestingly, in the contract approach it is not necessary to specify that
all elements in the prefix are smaller than those of the suffix. This information
follows from the strong framing of the outer loop, together with the summary
of the inner loop.

Summary. The examples shown in this section complement similar expositions
of verified algorithms where invariants are used, for example [23, 52] as well as
the Toccata Gallery.5 The intention was to compare utility of loop contracts. The
case is not entirely clear but it is possible to distill some insights as evidence
that sometimes loop contracts are just the right tool.
    Contracts reason about complete results of a computation, whereas invariants
reason about partial intermediate results. Sometimes, the former is easier to
describe, and moreover closer to the overall correctness property, which can
then be taken from the program’s annotation. This comment applies specifically
to those algorithms, where the work done so far affects the overall result only
in minor ways, as it is the case with the search algorithms, but not with the
ones that modify the array. We envision that there is a hidden potential to
be unlocked to discover loop specifications automatically, as it is done with
invariants in e.g. [23], and the preliminary experiment in Sec. 8 is a first step
into this direction.
    Moreover, proof arguments for summaries run counter to the computation
of the loop, implicitly turning it into a recursion. This helps to bridge the gap
when the specification is naturally expressed as a right-fold.
    Overall, expressing correctness properties as part of a summary provides an
alternative and important conceptual angle, regardless of the underlying veri-
fication method. However, with loop contracts it may be necessary to preserve
some additional information across the round-trip to the final state, as shown
with copy. In general, if correctness of the loop depends on unbounded work done
so far, the immediate constraints from executing the body once are insufficient.
Thus, loop precondition resp. the invariant remain an important conceptual in-
gredient for formal verification of loops as well.


8     Evaluation of Proof Automation

So far, we have emphasized the properties of loop specifications, how to come up
with them from the perspective of a human engineer, in the context of verification
against strong properties, where full proof automation cannot be expected.
    In this section we switch perspective and investigate how well state-of-the-
art solvers for systems of Horn clauses can be used to infer loop contracts with
pre- and postconditions. The benchmark set of the yearly CHC competition [58]
contains verification tasks that are based on invariants only, and consequentially,
5
    https://toccata.lri.fr/gallery



                                        18
one might assume that the implemented techniques are geared towards the shape
of the resulting verification conditions. On the other hand, completeness Thm. 4
of loop contracts suggests, that we can expect reasonable results. Furthermore,
the verification tasks that are currently in reach of Horn solvers focus primarily
on integer arithmetic, for which effective algorithms exist. Nevertheless, solvers
are forced to encode correctness primarily into loop postconditions instead.

Research Question: How well do existing solvers instantiate loop contracts
automatically in comparison to invariants?
    This question is relevant in so far, as any complex verification task comprises
smaller sub-problems, often numerical, that can be automated well, whereas for
other aspects, human guidance is needed. Tools like Boogie [44] already imple-
ment such features. In order to make use of loop contracts in practice, it is
therefore useful to know whether such an interplay between automation and
manual proof works in that setting, too.
    The evaluation is based on a prototype tool that translates C programs into
systems of Horn clauses like those in Sec. 4. The tool implements verification with
both invariants and contracts for a fair comparison. As benchmark, we consider
a those tasks of the SV-COMP repository which are currently supported by the
tool, and which contain tasks with loops. We emphasize that it is not a goal to
improve the overall performance over the state-of-the-art [3] across a wide range
of benchmarks, as it would require significant additional engineering effort to
support all the C features present in the SV-COMP benchmarks.

Experimental Setup. We focus on four categories from the SV-COMP bench-
mark repository, Arrays, Loops, Recursive, and ControlFlow, where 459 of a total
of 925 benchmarks are currently supported by our translator. These benchmarks
contain nondeterministic choice, as well as linear and nonlinear integer arith-
metic. Some tasks, notably those in the Arrays category, make use of arrays
but pointer aliasing is very limited. This class of tasks falls generally within
the capabilities of the solvers, albeit most are currently out of reach, e.g. com-
plex properties over arrays that require quantified invariants, or when procedure
summaries would need to be recursive.
    The verification tool used is called Korn, which is publicly available. 6 The
results presented here have been obtained mid-2020, Korn subsequently par-
ticipated in SV-COMP 2021, 7 using some additional techniques like random
fuzzing, such that those results are not directly comparable.
    We compare Z3 4.8.9 [42] and Eldarica 2.0.4 [36] as backends, the top two
performers in the CHC competition 2020 [58]. The hardware configuration is
Intel Xeon E3-1230 with 3.40 GHz and 8 cores, limited to 1 core, 15 min, and
15 GB memory per individual task. The experiments have been executed on
Ubuntu 20.04 with Java 11 (for Eldarica).

6
    https://github.com/gernst/korn
7
    https://sv-comp.sosy-lab.org/2021/results/results-verified/



                                        19
Table 1: Correct results, as found by the backend Horn solvers, with 15 min
CPU time and 15 MB memory, per category. Some official results from SV-
COMP 2020 are included for reference. # shows the number of tasks which are
supported by this evaluation vs. the total number of tasks in the category.
    Category                                   Solved Tasks (this paper)                             SV-COMP 2020
                                             Eld. 2.0.4 [36]           Z3 4.8.9 [28]
                                                                                              CPAX               UA      VeriAbs
                  #/total                    inv.    contr.            inv. contr.
    Arrays        129/436                      2             2           7             2              3            3         122
    ControlFlow    39/ 95                     36            36          31            33             37           37          31
    Loops         196/289                    117           112         105            75             83          113         162
    Recursive      95/105                     82            82          91            91             77           74          83
    Sum           459/925                    237           232         234          201              200         227         398



Results. Numeric results are shown in Table 1. For reference, we include of-
ficial results8 from SV-COMP 2020 for CPA-seq [16] (“CPAX”), Ultimate Au-
tomizer [31] (“UA”), and VeriAbs [1], for the same set of 459 tasks (cf. “#”).
    Both our backend solvers Eldarica and Z3 have trouble with the Array cat-
egory, which is difficult and subject to active research [17, 21]. VeriAbs [1] per-
forms well, because it can exploit loop parallelism. Eldarica can deal quite well
with contracts, and instantiate these even if we force the proof with these, missing
out on 5 tasks wrt. invariants only, whereas Z3 performs worse with contracts.


                            1000
                                               CPA-seq
                                               UAutomizer
                                               VeriAbs
Fig. 4: Quan-                                  Eldarica (invariants)
                                               Eldarica (contracts)
tile      plot                     100         Z3 (invariants)
                                               Z3 (contracts)
showing the
                    CPU time (s)




relative per-
formance of                         10
the three ap-
proaches, in
comparison                           1
to three top
software ver-
ifiers on the                      0.1
                                         0         50       100         150        200        250          300         350   400
same tasks.                                                            n-th fastest correct result




    Fig. 4 show a quantile plot of all correct results, which in addition to Table 1
reflects the solving times. The results for invariants are shown in red, those with
8
    https://zenodo.org/record/3630205



                                                                  20
contracts only are shown in blue. Z3 solves the majority of tasks well within a
second, requiring more than ten seconds only on the last few benchmarks. We
also see that for the configurations using contracts, if successful, Z3 still takes
longer on average. Eldarica, on the other hand, shows no such clear performance
difference between the configurations. There are a few incorrect results per ex-
perimental setup (1 for Eldarica, and 2 resp. 3 for Z3), due to limitations of the
implementation, such as assuming unbounded integers.
Discussion We can answer the research question outlined in the beginning pos-
itively: Current Horn clause solvers are in fact able to instantiate contracts, no-
tably the relational postcondition component, and their performance is roughly
comparable to verification with invariants.
    Nevertheless, it should be clear that this evaluation is not a conclusive as-
sessment of the general utility of loop contracts for proof automation. For that,
the verification tasks are not entirely suitable. In particular, integer arithmetic
can effectively be dealt with in both settings with established techniques. On
the other hand, consider the category Arrays, where we could hope that con-
tracts might be beneficial. However, thes tasks are rather tricky, and would often
require quantified invariants, for which techniques are not mature yet [7, 21]


9    Related Work

We emphasize that the approach of using contracts, see e.g. Hehner [29] for prac-
tical examples. The work closest to the theory of Sec. 4 is by Hehner and Gravel
[30], which shows an analogue of Def. 6 as Rule F in [30, Sec 10]. Their presen-
tation is closely tied to reasoning about for-loops, where starting and ending
indices are known (as symbolic expressions). In contrast, we delimit the loop in
terms of precondition P and postcondition Q, which lifts the idea to all loops in
general. Moreover, Rule F does not make explicit the relational nature of post-
conditions, whereas Rule G in [30] considers two arbitrary execution segments
of the loop, instead of a single segment known to end in a final state (cf. Figs. 2
and 3), possibly with additional limitations wrt. framing. Further work that is
based on the same idea is [9, 14]. A constructive translation like the one shown
Sec. 5 is not provided there or elsewhere as far as we know.
    Ideas to leverage the postcondition of a procedure contract to derive invari-
ants has been explored by Furia and Meyer [24]. Applying such techniques in a
setting with loop contracts is a natural step forward, but from Sec. 7 it is clear
that the necessary generalizations remain challenging. Progress in solving Horn
clauses [13, 17, 21, 25, 26, 36, 62] will tie into such work.
    Induction for the verification of loops (and also recursive procedures) occurs
in a variety of forms in practice, specifically when strong specifications are desired
and manual effort is acceptable. In the context of Separation Logic, Tuerk [61]
demonstrates verification rules with contracts, mechanized in the HOL theorem
prover, we refer back to Sec. 6 for a comparison. VeriFast offers loop specifica-
tions in terms of pre-/postconditions, with first-class support for applying the
inductive hypothesis, which was used to solve a challenge with linked trees in the


                                         21
VerifyThis competition 2012 (Jacobs et al. [41]). Tools that embed program veri-
fication into a general purpose theorem prover can make use of explicit induction,
too, as shown e.g. with KIV (for the same challenge, Ernst et al. [20]). Alterna-
tively, loops can be turned into recursive procedures to aid verification [51].
    The support for magic wands in Schwerhoff and Summers [60] resembles the
encoding of contracts as invariants via (6). Specifically, [60, Sec 7] spells this out
as pre rest ∗(post rest −∗ post all ), albeit this construction does not shed insight into
the state variables involved, lacking the analogue of sn in (6).
    A proof system based on coinduction (i.e. forward reasoning) that generalizes
loop verification to any recurring program locations is [15], a similar approach
to tackle interleavings in concurrency is [59]. Brotherston [11] takes a similar
route to construct cyclic proofs, implicitly making use of induction. All three
approaches have in common that the inductive property is constructed on the
fly instead of being expressed by a fixed predicate or formula up-front.
     Recent work on the verification of unstructured assembly programs [47] notes
that a negative loop test ¬t cannot be assumed by default in such a setting, as
it is the case with the conditions Def. 6. As discussed, our approach can include
this conclusion as part of the loop postcondition, in the absence of break.
    The tools participating in SV-COMP [3] show a strong bias towards invari-
ants. As an example, the most successful configuration of CPAchecker [5], CPA-
seq, relies on k-Induction [4, 19], which exploits correctness constraints from
inside the loop body, but disregards the constraints after a particular loop for
its verification. Likewise, Property Directed Reachability [48] reasons forward
over loops, but it is more precise wrt. different stages of a computation; Z3’s
fixpoint engine is fundamentally based on this idea [35, 43].
    Ultimate Automizer [32] abstracts traces in terms of automata, which may
contain loops. Whether there is a more fundamental connection between their
approach and loop contracts is not quite clear, and we leave this question for
future work. SeaHorn [27] is a verification platform for Horn clause based veri-
fication of C programs, using the invariant approach.
     Backwards program analysis, notably and combinations with forward analy-
sis, has been used in abstraction refinement [46, 63]. In contrast to here, the idea
is to back-propagate information about counterexamples instead of correctness
conditions to derive invariants via interpolation. Loop summarization in log-
ics for underapproximation [18, 54] similarly guarantees reachability of certain
states, the underlying “backwards variants” are incomparable to loop summaries.
   In Spark/GNATprove, loop invariants can be specified to hold anywhere in
the loop body [33], and there is an equivalent to old, referring to the state of the
loop entry. The approach is demonstrated with a verification of the prefixsum
algorithm, a tricky challenge from VerifyThis 2012 [38]. The approach bears re-
semblance to k-Induction [19], because correctness conditions are reflected inside
the loop, not in the code that follows as with contracts.

                                           22
10    Conclusion and Outlook

This paper presents a concise and accessible formulation of loop contracts, which
generalizes Hoare’s [34] proof approach for loops using invariants, and Hehner’s
refinement-based approach [30]. The presentation sheds light into fundamental
properties of loop contracts, and we prove several novel results that are not just
theoretical but offer immediate guidelines for tool construction: We characterize,
which part of the proof may be expressed using summaries, and which part must
be covered by invariants (Thm. 4). Moreover, the approaches can represent each
other, and we give constructive translations between them (Props. 1 and 2).
    We have exemplified the use of contracts versus invariants on some stan-
dard verification tasks. Both approaches have their respective advantages and
disadvantages, as summarized at the end of Sec. 7.
    A clear path to future work is to develop algorithms that synthesize loop
summaries from procedure postconditions, similarly to Furia and Meyer [24] for
invariants, but potentially exploiting their close correspondence.
    Overall, we hope that in the future, verification based on loop-contracts finds
its way into mainstream tools, and helps leverage their possibilities for those
problems where they are beneficial.
Acknowledgement. Many thanks to Toby Murray for valuable feedback. The
presentation in Sec. 6 is part of Gregor Alexandru’s bachelor thesis [2]. The treat-
ment of break and goto in with loop contracts has been explored by Johannes
Blau. We thank Rustan Leino for the phone number example.


References

 [1] Afzal, M., Chakraborty, S., Chauhan, A., Chimdyalwar, B., Darke, P.,
     Gupta, A., Kumar, S., Babu, C., Unadkat, D., Venkatesh, R.: VeriAbs:
     Verification by abstraction and test generation (competition contribution).
     In: Proc. of Tools and Algorithms for the Construction and Analysis of
     Systems (TACAS). pp. 383–387. Springer (2020)
 [2] Alexandru, G.: Specifying loops with contracts (2019), Bachelor’s Thesis,
     LMU Munich
 [3] Beyer, D.: Advances in automatic software verification: SV-COMP 2020. In:
     Proc. of Tools and Algorithms for the Construction and Analysis of Systems
     (TACAS). pp. 347–367. Springer (2020)
 [4] Beyer, D., Dangl, M., Wendler, P.: A unifying view on smt-based software
     verification. Journal of Automated Reasoning (JAR) 60(3), 299–335 (2018)
 [5] Beyer, D., Keremoglu, M.E.: CPAchecker: A tool for configurable software
     verification. In: Proc. of Computer Aided Verification (CAV). pp. 184–190.
     Springer (2011)
 [6] Bjørner, N., Gurfinkel, A., McMillan, K., Rybalchenko, A.: Horn clause
     solvers for program verification. In: Fields of Logic and Computation II,
     pp. 24–51. Springer (2015)

                                        23
 [7] Bjørner, N., McMillan, K., Rybalchenko, A.: On solving universally quan-
     tified horn clauses. In: Proc. of Static Analysis Symposium (SAS). pp.
     105–125. Springer (2013)
 [8] Blanc, R., Kuncak, V., Kneuss, E., Suter, P.: An overview of the leon veri-
     fication system: Verification by translation to recursive functions. In: Proc.
     of the 4th Workshop on Scala. pp. 1–10 (2013)
 [9] Bohórquez, J.: An elementary and unified approach to program correctness.
     Formal Aspects of Computing (FAC) 22, 611–627 (2010)
[10] Bormer, T., Brockschmidt, M., Distefano, D., Ernst, G., Filliâtre, J.C.,
     Grigore, R., Huisman, M., Klebanov, V., Marché, C., Monahan, R., et al.:
     The COST IC0701 verification competition 2011. In: Proc. of Formal Verifi-
     cation of Object-Oriented Software (FoVeOOS). LNCS, vol. 7421, pp. 3–21.
     Springer (2011)
[11] Brotherston, J.: Cyclic proofs for first-order logic with inductive definitions.
     In: Automated Reasoning with Analytic Tableaux and Related Methods.
     pp. 78–92. Springer (2005)
[12] Burstall, R.M.: Some techniques for proving correctness of programs which
     alter data structures. Machine intelligence 7(23-50), 3 (1972)
[13] Champion, A., Kobayashi, N., Sato, R.: HoIce: An ICE-based non-linear
     Horn clause solver. In: Proc. of Asian Symposium on Programming Lan-
     guages and Systems (ASPLOS). pp. 146–156. Springer (2018)
[14] Charguéraud, A.: Characteristic formulae for mechanized program verifica-
     tion. Ph.D. thesis, PhD thesis, Université Paris-Diderot (2010)
[15] Chen, X., Trinh, M.T., Rodrigues, N., Peña, L., Rosu, G.: Towards a unified
     proof framework for automated fixpoint reasoning using matching logic.
     Tech. rep. (2020)
[16] Dangl, M., Löwe, S., Wendler, P.: CPAchecker with support for recur-
     sive programs and floating-point arithmetic. In: Proc. of Tools and Algo-
     rithms for the Construction and Analysis of Systems (TACAS). pp. 423–425.
     Springer (2015)
[17] De Angelis, E., Fioravanti, F., Pettorossi, A., Proietti, M.: Verifying ar-
     ray programs by transforming verification conditions. In: Proc. of Verifica-
     tion, Model Checking, and Abstract Interpretation (VMCAI). pp. 182–202.
     Springer (2014)
[18] De Vries, E., Koutavas, V.: Reverse hoare logic. In: International Conference
     on Software Engineering and Formal Methods. pp. 155–171. Springer (2011)
[19] Donaldson, A.F., Haller, L., Kroening, D., Rümmer, P.: Software verification
     using k-Induction. In: Proc. of Static Analysis Symposium (SAS). pp. 351–
     368. Springer (2011)
[20] Ernst, G., Pfähler, J., Schellhorn, G., Haneberg, D., Reif, W.: KIV—
     Overview and VerifyThis competition. Software Tools for Technology Trans-
     fer (STTT) 17(6), 677–694 (2015)
[21] Fedyukovich, G., Prabhu, S., Madhukar, K., Gupta, A.: Quantified invari-
     ants via syntax-guided synthesis. In: Computer Aided Verification. pp.
     259–277. Springer (2019)


                                         24
[22] Floyd, R.W.: Assigning meanings to programs. In: Program Verification,
     pp. 65–81. Springer (1993)
[23] Furia, C.A., Meyer, B., Velder, S.: Loop invariants: Analysis, classification,
     and examples. ACM Computing Surveys (CSUR) 46(3), 1–51 (2014)
[24] Furia, C.A., Meyer, B.: Inferring loop invariants using postconditions. In:
     Fields of logic and computation, pp. 277–300. Springer (2010)
[25] Grebenshchikov, S., Lopes, N.P., Popeea, C., Rybalchenko, A.: Synthesizing
     software verifiers from proof rules. ACM SIGPLAN Notices 47(6), 405–416
     (2012)
[26] Gurfinkel, A., Bjørner, N.: The science, art, and magic of constrained horn
     clauses. In: Symbolic and Numeric Algorithms for Scientific Computing
     (SYNASC). pp. 6–10. IEEE (2019)
[27] Gurfinkel, A., Kahsai, T., Komuravelli, A., Navas, J.A.: The SeaHorn ver-
     ification framework. In: Proc. of Computer Aided Verification (CAV). pp.
     343–361. Springer (2015)
[28] Gurfinkel, A., Shoham, S., Meshman, Y.: Smt-based verification of param-
     eterized systems. In: Proc. of Foundations of Software Engineering (FSE).
     pp. 338–348 (2016)
[29] Hehner, E.C.: Specified blocks. In: Proc. of Verified Software: Theories,
     Tools, and Experiments (VSTTE). pp. 384–391. Springer (2005)
[30] Hehner, E.C., Gravel, A.M.: Refinement semantics and loop rules. In: Proc.
     of Formal Methods (FM). pp. 1497–1510. Springer (1999)
[31] Heizmann, M., Chen, Y.F., Dietsch, D., Greitschus, M., Hoenicke, J., Li, Y.,
     Nutz, A., Musa, B., Schilling, C., Schindler, T., et al.: Ultimate automizer
     and the search for perfect interpolants. In: Tools and Algorithms for the
     Construction and Analysis of Systems. pp. 447–451. Springer (2018)
[32] Heizmann, M., Hoenicke, J., Podelski, A.: Refinement of trace abstraction.
     In: International Static Analysis Symposium. pp. 69–85. Springer (2009)
[33] Hoang, D., Moy, Y., Wallenburg, A., Chapman, R.: Spark 2014 and gnat-
     prove. Software Tools for Technology Transfer (STTT) 17(6), 695–707
     (2015)
[34] Hoare, C.A.R.: An axiomatic basis for computer programming. Communi-
     cations of the ACM 12(10), 576–580 (1969)
[35] Hoder, K., Bjørner, N., De Moura, L.: µz–an efficient engine for fixed points
     with constraints. In: Proc. of Computer Aided Verification (CAV). pp. 457–
     462. Springer (2011)
[36] Hojjat, H., Rümmer, P.: The eldarica horn solver. In: Proc. of Formal
     Methods in Computer Aided Design (FMCAD). pp. 1–7. IEEE (2018)
[37] Huisman, M., Jacobs, B.: Java program verification via a hoare logic with
     abrupt termination. In: Proc. of Fundamental Approaches to Software En-
     gineering (FASE). pp. 284–303. Springer (2000)
[38] Huisman, M., Klebanov, V., Monahan, R.: VerifyThis verification compe-
     tition 2012: Organizers report. Tech. rep., KIT, Fakultät für Informatik
     (2013)
[39] Huisman, M., Klebanov, V., Monahan, R.: Verifythis 2012 (2015)


                                        25
[40] Hutton, G.: A tutorial on the universality and expressiveness of fold. Journal
     of Functional Programming (JAR) 9(4), 355–372 (1999)
[41] Jacobs, B., Smans, J., Piessens, F.: Solving the VerifyThis 2012 challenges
     with VeriFast. Software Tools for Technology Transfer (STTT) 17(6), 659–
     676 (2015)
[42] Komuravelli, A., Gurfinkel, A., Chaki, S.: Smt-based model checking for re-
     cursive programs. Formal Methods in System Design 48(3), 175–205 (2016)
[43] Komuravelli, A., Gurfinkel, A., Chaki, S., Clarke, E.M.: Automatic abstrac-
     tion in smt-based unbounded software model checking. In: Proc. of Com-
     puter Aided Verification (CAV). pp. 846–862. Springer (2013)
[44] Leino, K.R.M.: This is Boogie 2 (2008)
[45] Leino, K.R.M.: Dafny: An automatic program verifier for functional cor-
     rectness. In: Logic for Programming Artificial Intelligence and Reasoning.
     pp. 348–370. Springer (2010)
[46] Lin, S.W., Sun, J., Xiao, H., Liu, Y., Sanán, D., Hansen, H.: Squeezing loop
     invariants by interpolation between forward/backward predicate transform-
     ers. In: Proc. of Automated Software Engineering (ASE). pp. 793–803. IEEE
     (2017)
[47] Lundberg, D., Guanciale, R., Lindner, A., Dam, M.: Hoare-style logic for
     unstructured programs. In: Proc. of Software Engineering and Formal Meth-
     ods (SEFM). pp. 193–213. Springer (2020)
[48] McMillan, K.L.: Interpolation and sat-based model checking. In: Proc. of
     Computer Aided Verification (CAV). pp. 1–13. Springer (2003)
[49] Morgan, C.: The specification statement. ACM Transactions on Program-
     ming Languages and Systems (TOPLAS) 10(3), 403–419 (1988)
[50] Mraihi, O., Louhichi, A., Jilani, L.L., Desharnais, J., Mili, A.: Invariant
     assertions, invariant relations, and invariant functions. Science of Computer
     Programming (SCP) 78(9), 1212–1239 (2013)
[51] Myreen, M.O., Gordon, M.J.: Transforming programs into recursive func-
     tions. Electronic Notes in Theoretical Comp. Science 240, 185–200 (2009)
[52] Nipkow, T., Eberl, M., Haslbeck, M.P.: Verified textbook algorithms. In:
     Proc. of Automated Technology for Verification and Analysis (ATVA). pp.
     25–53. Springer (2020)
[53] Nipkow, T., Paulson, L.C., Wenzel, M.: Isabelle/HOL: a proof assistant for
     higher-order logic, vol. 2283. Springer Science & Business Media (2002)
[54] O’Hearn, P.W.: Incorrectness logic. Proceedings of the ACM on Program-
     ming Languages 4(POPL), 1–32 (2019)
[55] Philippaerts, P., Mühlberg, J.T., Penninckx, W., Smans, J., Jacobs, B.,
     Piessens, F.: Software verification with verifast: Industrial case studies. Sci-
     ence of Computer Programming (SCP) 82, 77–97 (2014)
[56] Reynolds, J.C.: Separation logic: A logic for shared mutable data structures.
     In: Proc. of Logic in Computer Science (LICS). pp. 55–74. IEEE (2002)
[57] Roşu, G., Lucanu, D.: Circular coinduction: A proof theoretical founda-
     tion. In: Algebra and Coalgebra in Computer Science. pp. 127–144. Springer
     (2009)


                                         26
[58] Rümmer, P.: Competition report: CHC-COMP-20.                  arXiv preprint
     arXiv:2008.02939 (2020)
[59] Schellhorn, G., Tofan, B., Ernst, G., Pfähler, J., Reif, W.: RGITL: A tempo-
     ral logic framework for compositional reasoning about interleaved programs.
     Annals of Mathematics and Artificial Intelligence 71(1-3), 131–174 (2014)
[60] Schwerhoff, M., Summers, A.J.: Lightweight suppoert for magic wands in an
     automatic verifier. In: European Conference on Object-Oriented Program-
     ming (ECOOP). vol. 37, pp. 614–638. Schloss Dagstuhl-Leibniz-Zentrum
     für Informatik (2015)
[61] Tuerk, T.: Local reasoning about while-loops. Proc. of Verified Software:
     Theory, Tools, and Experiments (VSTTE) 2010, 29 (2010)
[62] Unno, H., Torii, S., Sakamoto, H.: Automating induction for solving horn
     clauses. In: Computer Aided Verification. pp. 571–591. Springer (2017)
[63] Vizel, Y., Grumberg, O., Shoham, S.: Intertwined forward-backward reach-
     ability analysis using interpolants. In: Tools and Algorithms for the Con-
     struction and Analysis of Systems (TACAS). pp. 308–323. Springer (2013)




                                       27
