                                                         Summing Up Smart Transitions

                                             Neta Elad1 , Sophie Rain2 , Neil Immerman3 , Laura Kovács2 , and
                                                                       Mooly Sagiv1
                                                                       1
                                                                           Tel Aviv University, Israel
                                                                             2
                                                                               TU Wien, Austria
arXiv:2105.07663v1 [cs.LO] 17 May 2021




                                                                           3
                                                                             UMass Amherst, USA


                                                 Abstract. Some of the most significant high-level properties of curren-
                                                 cies are the sums of certain account balances. Properties of such sums can
                                                 ensure the integrity of currencies and transactions. For example, the sum
                                                 of balances should not be changed by a transfer operation. Currencies
                                                 manipulated by code present a verification challenge to mathematically
                                                 prove their integrity by reasoning about computer programs that operate
                                                 over them, e.g., in Solidity. The ability to reason about sums is essential:
                                                 even the simplest ERC-20 token standard of the Ethereum community
                                                 provides a way to access the total supply of balances.
                                                 Unfortunately, reasoning about code written against this interface is non-
                                                 trivial: the number of addresses is unbounded, and establishing global
                                                 invariants like the preservation of the sum of the balances by operations
                                                 like transfer requires higher-order reasoning. In particular, automated
                                                 reasoners do not provide ways to specify summations of arbitrary length.
                                                 In this paper, we present a generalization of first-order logic which can
                                                 express the unbounded sum of balances. We prove the decidablity of
                                                 one of our extensions and the undecidability of a slightly richer one.
                                                 We introduce first-order encodings to automate reasoning over software
                                                 transitions with summations. We demonstrate the applicability of our
                                                 results by using SMT solvers and first-order provers for validating the
                                                 correctness of common transitions in smart contracts.

                                                 This submission is an extended version of the CAV 2021 paper ”Summing
                                                 Up Smart Transitions”, by N. Elad, S. Rain, N. Immerman, L. Kovács
                                                 and M. Sagiv.


                                         1     Introduction
                                         A basic challenge in smart contract verification is how to express the functional
                                         correctness of transactions, such as currency minting or transferring between ac-
                                         counts. Typically, the correctness of such a transaction can be verified by proving
                                         that the transaction leaves the sum of certain account balances unchanged.
                                             Consider for example the task of minting an unbounded number of tokens
                                         in the simplified ERC-20 token standard of the Ethereum community [31], as
                                         illustrated in Figure 14 . This example deposits the minted amount (n) into the re-
                                         4
                                             The old- prefix denotes the value of a function before the mint transition, and the
                                             new- prefix denotes the value afterwards.
2       Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

a : Address
n : Nat

mint (a , n )

# Post - conditions
assert new - bal ( a ) = old - bal ( a ) + n                                    #(i)
for each Address a 0 6= a :                                                   # ( ii )
    assert new - bal ( a 0 ) = old - bal ( a 0 )
assert new -sum() = old -sum() + n                                          # ( iii )


                      Fig. 1: Minting n Tokens in ERC-20.

ceiver’s address (a) and we need to ensure that the mint operation only changed
the balance of the receiver. To do so, in addition to (i) proving that the bal-
ance of the receiver has been increased by n, we also need to verify that (ii) the
account balance of every user address a0 different than a has not been changed
during the mint operation and that (iii) the sum of all balances changed exactly
by the amount that was minted. The validity of these three requirements (i)-(iii),
formulated as the post-conditions of Figure 1, imply its functional correctness.
    Surprisingly, proving formulas similar to the post-conditions of Figure 1 is
challenging for state-of-the-art automated reasoners, such as SMT solvers [7,6,9]
and first-order provers [18,10,33]: it requires reasoning that links local changes of
the receiver (a) with a global state capturing the sum of all balances, as well as
constructing that global state as an aggregate of an unbounded but finite number
of Address balances. Moreover, our encoding of the problem uses discrete coins
that are minted and deposited, whose number is unbounded but finite as well.
    In this paper we address verification challenges of software transactions with
aggregate properties, such as preservation of sums by transitions that manipulate
low-level, individual entities. Such properties are best expressed in higher-order
logic, hindering the use of existing automated reasoners for proving them. To
overcome such a reasoning limitation, we introduce Sum Logic (SL) as a gen-
eralization of first-order logic, in particular of Presburger arithmetic. Previous
works [20,30,11] have also introduced extensions of first-order logic with ag-
gregates by counting quantifiers or generalized quantifiers. In Sum Logic (SL)
we only consider the special case of integer sums over uninterpreted functions,
allowing us to formalize SL properties with and about unbounded sums, in par-
ticular sums of account balances, without higher-order operations (Section 3).
We prove the decidability of one of our SL extensions and the undecidability of
a slightly richer one (Section 4). Given previous results [20], our undecidability
result is not surprising. In contrast, what may be unexpected is our decidability
result and the fact that we can use our first-order fragment for a convenient and
practical new way to verify the correctness of smart contracts.
    We further introduce first-order encodings which enable automated reason-
ing over software transactions with summations in SL (Section 5). Unlike [5],
where SMT-specific extensions supporting higher-order reasoning have been in-
                                            Summing Up Smart Transitions         3

troduced, the logical encodings we propose allow one to use existing reasoners
without any modification. We are not restricted to SMT reasoning, but can
also leverage generic automated reasoners, such as first-order theorem provers,
supporting first-order logic. We believe our results ease applying automated rea-
soning to smart contract verification even for non-experts.
     We demonstrate the practical applicability of our results by using SMT
solvers and first-order provers for validating the correctness of common financial
transitions appearing in smart contracts (Section 6). We refer to these transi-
tions as smart transitions. We encode SL into pure first-order logic by adding
another sort that represents the tokens of the crypto-currency themselves (which
we dub “coins”).
     Although the encodings of Section 5 do not translate to our decidable SL
fragment from Section 4, our experimental results show that automated rea-
soning engines can handle them consistently and fast. The decidability results
of Section 5 set the boundaries for what one can expect to achieve, while our
experiments from Section 5 demonstrate that the unknown middle-ground can
still be automated.
     While our work is mainly motivated by smart contract verification, our results
can be used for arbitrary software transactions implementing sum/aggregate
properties. Further, when compared to the smart contract verification frame-
work of [32], we note that we are not restricted to proving the correctness of
smart contracts as finite-state machines, but can deal with semantic properties
expressing financial transactions in smart contracts, such as currency minting/-
transfers.
     While ghost variable approaches [13] can reason about changes to the global
state (the sum), our approach allows the verifier to specify only the local changes
and automatically prove the impact on the global state.


Contributions. In summary, this paper makes the following contributions:

 – We present a generalization to Presburger arithmetic (SL, in Section 3)
   that allows expressing properties about summations. We show how we can
   formalize verification problems of smart contracts in SL.
 – We discuss the decidability problem of checking validity of SL formulas
   (Section 4): we prove that it is undecidable in the general case, but also that
   there exists a small decidable fragment.
 – We show different encodings of SL to first-order logic (Section 5). To this
   end, we consider theory-specific reasoning and variations of SL, for example
   by replacing non-negative integer reasoning with term algebra properties.
 – We evaluate our results with SMT solvers and first-order theorem provers,
   by using 31 new benchmarks encoding smart transitions and their properties
   (Section 6). Our experiments demonstrate the applicability of our results
   within automated reasoning, in a fully automated manner, without any user
   guidance.
4       Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

2    Preliminaries

We consider many-sorted first-order logic (FOL) with equality, defined in the
standard way. The equality symbol is denoted by ≈.
    We denote by STRUCT [Σ] the set of all structures for the vocabulary Σ. A
structure A ∈ STRUCT [Σ] is a pair (D, I), where for each sort s, its domain
in A is D(s), and for each symbol S, its interpretation in A is I(S). Note that
models of a formula ϕ over a vocabulary Σ are structures A ∈ STRUCT [Σ].
    A first-order theory is a set of first-order formulas closed under logical con-
sequence. We will consider, the first-order theory of the natural numbers with
addition. This is Presburger arithmetic (PA) which is of course decidable [26].
We write N to denote the set of natural numbers. We consider 0 ∈ N and
write N+ to explicitly        exclude 0 from N. The vocabulary of PA is ΣPresburger =
 0, 1, c1 , . . . , cl , +2 , with all constants 0, 1, ci of sort Nat. A structure A =
(D, I) ∈ STRUCT [ΣPresburger ] is called a Standard Model of Arithmetic when
D(Nat) = N and +2 is interpreted as the standard binary addition + function
over the naturals. The vocabulary ΣPresburger can         be extended with a total or-
                                ∗
der relation, yielding ΣPresburger       = 0, 1, +2 , ≤2 , where ≤2 is interpreted as the
binary relation ≤ in Standard Models of Arithmetic.


3    Sum Logic (SL)

We now define Sum Logic ( SL) as a generalization of Presburger arithmetic, ex-
tending Presburger arithmetic with unbounded sums. SL is motivated by appli-
cations of financial transactions over cryptocurrencies in smart contracts. Smart
contracts are decentralized computer programs executed on a blockchain-based
system, as explained in [27]. Among other tasks, they automate financial trans-
actions such as transferring and minting money. We refer to these transactions
as smart transitions. The aim of this paper and SL in particular is to express
and reason about the post-conditions of smart transitions similar to Figure 1.
     SL expresses smart transition relations among sums of accounts of various
kinds, e.g., at different banks, times, etc. Each such kind, j, is modeled by an
uninterpreted function symbol, bj , where bj (a) denotes the balance of a’s account
of kind j, and a constant symbol sj , which denotes the sum of all outputs of
bj . As such, our SL generalizes Presburger arithmetic with (i) a sort Address
corresponding to the (unbounded) set of account addresses; (ii) balance functions
bj mapping account addresses from Address to account values of sort Nat; and
(iii) sum constants sj of sort Nat capturing the total sum of all account balances
represented by bj . Formally, the vocabulary of SL is defined as follows.

Definition 1 (SL Vocabulary). Let
         l,m,d
               = a1 , . . . , al , b11 , . . . , b1m , c1 , . . . , cd , s1 , . . . , sm , 0, 1, +2 , ≤2
                                                                                                           
        Σ+,≤

be a sorted first-order vocabulary of SL over sorts {Address, Nat}, where
                                                 Summing Up Smart Transitions          5

      Function                   Encoding in SL                  Reference in ERC-20
 sum                                    s or s0                  totalSupply
 bal(a)                              b(a) or b0 (a)              balanceOf
                                   0
 mint(a, v)                       b (a) ≈ b(a) + v               transfer
 transferFrom(f, t, v) b0 (t) ≈ b(t) + v ∧ b(f ) ≈ b0 (f ) + v   transferFrom
                          Table 1: ERC-20 Token Standard

 – (Addresses) The constants a1 , . . . , al are of sort Address;
 – (Balance functions) b11 , . . . , b1m are unary function symbols from Address to
   Nat;
 – (Constants and Sums) The constants c1 , . . . , cd , s1 , . . . , sm and 0, 1 are of
   sort Nat;
 – +2 is a binary function Nat × Nat → Nat;
 – ≤2 is a binary relation over Nat × Nat.
    In what follows, when the cardinalities in an SL vocabulary are clear from
                                          l,m,d                   l,m,d
context, we simply write Σ instead of Σ+,≤       . Further, by Σ+,  ≤
                                                                        we denote the
                                                                 
sub-vocabulary where the crossed-out symbols are not available. Note that even
when addition is not available, we still allow writing numerals larger than 1.
    We restrict ourselves to universal sentences over an SL vocabulary, with
quantification only over the Address sort.
    We now extend the Tarskian semantics of first-order logic to ensure that the
sum constants of an SL vocabulary (s1 , . . . , sm ) are equal to the sum of outputs
of their associated balance functions (bj for each sj ) over the respective entire
domains of sort Address.
    Let Σ be an SL vocabulary. An SL structure A = (D, I) ∈ STRUCT [Σ]
representing a model for an SL formula ϕ is called an SL model iff
                  X
      I(sj ) =            [I(bj )] (a), for each 1 ≤ j ≤ m.           (Sum Property)
               a∈D(Address)

   We write A SL ϕ to mean that A is an SL model of ϕ. When it is clear
from context, we simply write A  ϕ.
Example 1 (Encoding ERC-20 in SL). As a use case of SL, we showcase the
encoding of the ERC-20 token standard of the Ethereum community [31] in SL.
To this end, we consider an SL vocabulary Σ l,2,d . We respectively denote the
balance functions and their associated sums as b, b0 , s, s0 in the SL structure
over Σ l,2,d . The resulting instance of SL can then be used to encode ERC-20
operations/smart transitions as SL formulas, as shown in Table 1. Using this
encoding, the post-condition of Figure 1 is expressed as the SL formula
              b0 (a) ≈ b(a) + n ∧ ∀a0 6≈ a.b0 (a0 ) ≈ b(a0 ) ∧ s0 ≈ s + n          (1)
formalizing the correctness of the smart transition of minting n tokens in Fig-
ure 1. In the applied verification examples in Section 6, rather than verifying the
low-level implementation of built-in functions such as mintn , we assume their
correctness by including suitable axioms.
6        Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

4     Decidability of SL

We consider the decidability problem of verifying formulas in SL. We show that
when there are several function symbols bj to sum over, the satisfiability prob-
lem for SL becomes undecidable5 . We first present, however, a useful decidable
fragment of SL.


4.1    A Decidable Fragment of SL

We prove decidability for a fragment of SL, which we call the (l, 1, d)-FRAG
fragment of SL (Theorem 4). For doing so, we reduce the fragment to Presburger
arithmetic, by using regular Presburger constructs to encode SL extensions, that
is the uninterpreted functions and sum constants of SL.
    The first step of our reduction proof is to consider distinct models, which are
models where the Address constants ai represent distinct elements in the domain
D(Address). While this restriction is somewhat unnatural, we show that for each
vocabulary and formula that has a model, there exists an equisatisfiable formula
over a different vocabulary that has a distinct model (Theorem 1). The crux of
our decidability proof is then proving that (l, 1, d)-FRAG has small Address
space: given a formula ϕ, if it is satisfiable, then there exists a model where
|D(Address)| ≤ κ(|ϕ|), |ϕ| is the length of ϕ, and κ(.) is some computable
function (Theorem 3)6 .
Distinct Models An SL structure A is considered distinct when the l Address
constants represent l distinct elements in D(Address). I.e.,
                               |{I(a1 ), . . . , I(al )}| = l .

Since each SL model induces an equivalence relation over the Address constants,
we consider partitions P over {a1 , . . . , al }. For each possible partition P we define
a transformation of terms and formulas TP that substitutes equivalent Address
constants with a single Address constant. The resulting formulas are defined
over a vocabulary that has |P | Address constants. We show that given an SL
formula ϕ, if ϕ has a model, we can always find a partition P such that each of
its classes corresponds to an equivalence class induced by that model.

Theorem 1 (Distinct Models). Let ϕ be an SL formula over Σ, then ϕ
has a model iff there exists a partition P of {a1 , . . . , al } such that TP (ϕ) has a
distinct model.                                                                       t
                                                                                      u

Small Address Space In order to construct a reduction to Presburger arith-
metic, we bound the size of the Address sort. For a fragment of SL to be
decidable, we therefore need a way to bound its models upfront. We formalize
this requirement as follows.
5
    Due to space restrictions, proofs of our results are given in our Appendix.
6
    The function κ(.) is defined per decidable fragment of SL, and not per formula.
                                              Summing Up Smart Transitions           7

Definition 2 (Small Address Space). Let FRAG be some fragment of SL
                       l,m,d
over vocabulary Σ = Σ+,≤     . FRAG is said to have small Address space if there
exists a computable function κΣ (.), such that for any SL formula ϕ ∈ FRAG,
ϕ has a distinct model iff ϕ has a distinct model A = (D, I) with small Address
space, where |D(Address)| ≤ κΣ (|ϕ|).
    We call κΣ (.) the bound function of FRAG; when the vocabulary is clear
from context we simply write κ(.).

   One instance of a fragment (or rather, family of fragments) that satisfies this
property is the (l, 1, d)-FRAG fragment: the simple case of a single uninter-
preted “balance” function (and its associated sum constant), further restricted
by removing the binary function + and the binary relation ≤. Therefore, we
derive the following theorem:

Theorem 2 (Small Address Space of (l, 1, d)-FRAG).
   For any l, d, it holds (l, 1, d)-FRAG, the fragment of SL formulas over the
SL vocabulary
                     l,1,d
                           = a1 , . . . , al , b1 , c1 , . . . , cd , s, 0, 1 ,
                                                                             
                    Σ+, ≤
                     
has small Address space with bound function κ(x) = l + x + 1.                   t
                                                                                u

   An attempt to trivially extend Theorem 2 for a fragment of SL with two bal-
ance functions falls apart in a few places, but most importantly when comparing
balances to the sum of a different balance function. In Section 4.2 we show that
these comparisons are essential for proving our undecidability result in SL.


Presburger Reduction For showing decidability of some FRAG fragment of
SL, we describe a Turing reduction to pure Presburger arithmetic. We introduce
a transformation τ (.) of formulas in SL into formulas in Presburger arithmetic.
It maps universal quantifiers to disjunctions, and sums to explicit addition of all
balances. In addition, we define an auxiliary formula η(ϕ), which ensures only
valid addresses are considered, and that invalid addresses have zero balances.
The formal definitions of τ (.) and η(ϕ) can be found in Appendix A.
    By relying on the properties of distinctness and small Address space we get
the following results.

Theorem 3 (Presburger Reduction). An SL formula ϕ has a distinct,
SL model with small Address space iff τ (ϕ) ∧ η(ϕ) has a Standard Model of
Arithmetic.                                                             t
                                                                        u

Theorem 4 (SL Decidability). Let FRAG be a fragment of SL that has
small Address space, as defined in Definition 2. Then, FRAG is decidable.

Proof (Theorem 4). Let ϕ be a formula in FRAG. Then ϕ has an SL model
iff for some partition P of {a1 , . . . , al }, TP (ϕ) has a distinct SL model. For any
P , the formula TP (ϕ) is in FRAG, therefore TP (ϕ) has a distinct SL model iff
it has a distinct SL model with small Address space.
8         Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

     From Theorem 3, we get that for any P , ϕP , TP (ϕ) has a distinct SL model
iff τ (ϕP ) ∧ η(ϕP ) has a Standard Model of Arithmetic. By using the PA decision
procedure as an oracle, we obtain the following decision procedure for a FRAG
formula ϕ:

    – For each possible partition P of {a1 , . . . , al }, let ϕP = TP (ϕ);
    – Using a PA decision procedure, check whether τ (ϕP ) ∧ η(ϕP ) has a model,
      for each P ;
    – If a model for some partition P was found, the formula ϕP has a distinct SL
      model, and therefore ϕ has SL model;
    – Otherwise, there is no distinct SL model for any partition P , and therefore
      there is no SL model for ϕ.

Remark 1. Our decision procedure for Theorem 4 requires Bl Presburger queries,
where Bl is Bell’s number for all possible partitions of a set of size l.

      Using Theorem 4 and Theorem 2, we then obtain the following result.
Corollary 1. (l, 1, d)-FRAG is decidable.                                                  t
                                                                                           u


4.2     SL Undecidability

We now show that simple extensions of our decidable (l, 1, d)-FRAG fragment
lose its decidability (Theorem 5). For doing so, we encode the halting problem
of a two-counter machine using SL with 3 balance functions, thereby proving
that the resulting SL fragment is undecidable.
    Consider a two-counter machine, whose transitions are encoded by the Pres-
burger formula π(c1 , c2 , p, c01 , c02 , p0 ) with 6 free variables: 2 for each of the three
registers, one of which being the program counter (pc). We assume w.l.o.g. that
all three registers are within N+ , allowing us to use addresses with a zero balance
as a special “separator”. In addition, we assume that the program counter is 1
at the start of the execution, and that there exists a single halting statement at
line H. That is, the two-counter machine halts iff the pc is equal to H.

Reduction Setting We have 4 Address elements for each time-step, 3 of them
hold one register each, and one is used to separate between each group of Address
elements (see Table 2). We have 3 uninterpreted functions from Address to
Nat (“balances”). For readability we denote these functions as c, l, g (instead of
b1 , b2 , b3 ) and their respective sums as sc , sl , sg :

 1. Function c : Cardinality function, used to force size constraints. We set its
    value for all addresses to be 1, and therefore the number of addresses is sc .
 2. Function l : Labeling function, to order the time-steps. We choose one ele-
    ment to have a maximal value of sc − 1 and ensure that l is injective. This
    means that the values of l are distinctly [0, sc − 1].
 3. Function g : General purpose function, which holds either one of the registers
    or 0 to mark the Address element as a separating one.
                                            Summing Up Smart Transitions             9


                             Address   l(Address)     c(Address)     g(Address)
                          
                                             0             1       0
                                              1             1       c1 at #0
                          
          Time-step #0
                          
                                             2             1       c2 at #0
                                a0            3             1       pc at #0 = 1
                          
                                 ..           ..            ..             ..
                                 .            .             .              .
                          
                               x1           4i             1       0
                                x2         4i + 1           1       c1 at #i
                          
           Time-step #i
                          
                               x3         4i + 2           1       c2 at #i
                                x4         4i + 3           1       pc at #i
                          
                          
                          
                               x5         4i + 4           1       0
                                x6         4i + 5           1       c1 at #(i + 1)
                          
     Time-step #(i + 1)
                          
                               x7         4i + 6           1       c2 at #(i + 1)
                                x8         4i + 7           1       pc at #(i + 1)
                          
                                  ..           ..            ..             ..
                                  .            .             .              .
                          
                                          sc − 4           1       0
                                           sc − 3           1       c1 at #n
                          
 Time-step #n = s4c − 1
                          
                                          sc − 2           1       c2 at #n
                                a1         sc − 1           1       pc at #n = H
                          

       Table 2: Transition System of a 2-Counter Machine, Array View.

Each group representing a time-step is a 4 Address element, ordered as follows:

1. First, a separating Address element x (where g(x) is 0).
2. Then, the two general-purpose counters.
3. Lastly, the program counter.

In addition we have 2 Address constants, a0 and a1 which represent the pc
value at the start and at the end of the execution. The element a1 also holds
the maximal value of l, that is, l(a1 ) + 1 ≈ sc . Further, a0 holds the fourth-
minimal value, since its the last element of the first group, and each group has
four elements.

Formalization Using a Two-Counter Machine We now formalize our re-
duction, proving undecidability of SL.
(i) We impose an injective labeling
                      ϕ1 = ∀x, y. (l(x) ≈ l(y)) → (x ≈ y)

(ii) We next formalize properties over the program counter pc. The Address
constant that represents the program counter pc value of the last time-step is
set to have the maximal labeling, that is
                               ϕ2 = ∀x.l(x) ≤ l(a1 )

Further, the Address constant that represents the pc value of the first time-step
has the fourth labeling, hence
                                ϕ3 = l(a0 ) ≈ 3
10      Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

Finally, the first and last values of the program counter are respectively 1 and
H, that is                  ϕ4 = g(a0 ) ≈ 1 ∧ g(a1 ) ≈ H
(iii) We express cardinality constraints ensuring that there are as many Address
elements as the labeling of the last Address constant (a1 ) + 1. We assert
                      ϕ5 = (sc ≈ l(a1 ) + 1) ∧ ∀x. (c(x) ≈ 1)

(iv) We encode the transitions of the two-counter machine, as follows. For every
8 Address elements, if they represent two sequential time-steps, then the formula
for the transitions of the two-counter machine is valid for the registers it holds.
As such, we have
               ϕ6 = ∀x1 , . . . , x8 . (F 1 ∧ F 2 ∧ F 3)
                       → π (g(x2 ), g(x3 ), g(x4 ), g(x6 ), g(x7 ), g(x8 ))

where the conjunction F 1 ∧ F 2 ∧ F 3 expresses that x1 , . . . , x8 are two sequential
time-steps, with F 1, F 2 and F 3 defined as below. In particular, F 1, F 2 and
F 3 formalize that x1 , . . . , x8 have sequential labeling, starting with one zero-
valued Address element (“separator”) and continuing with 3 non-zero elements,
as follows:

 – Sequential:         l(x2 ) ≈ l(x1 ) + 1 ∧ · · · ∧ l(x8 ) ≈ l(x7 ) + 1          (F1)
 – Time-steps:     g(x1 ) ≈ 0 ∧ g(x2 ) > 0 ∧ g(x3 ) > 0 ∧ g(x4 ) > 0 ,            (F2)
                   g(x5 ) ≈ 0 ∧ g(x6 ) > 0 ∧ g(x7 ) > 0 ∧ g(x8 ) > 0              (F3)

     Based on the above formalization, the formula ϕ = ϕ1 ∧ · · · ∧ ϕ6 is satisfiable
iff the two-counter machine halts within a finite amount of time-steps (and the
exact amount would be given by s4c ). Since the halting problem for two-counter
machines is undecidable, our SL, already with 3 uninterpreted functions and
their associated sums, is also undecidable.
                                                                l,m,d
Theorem 5. For any l ≥ 2, m ≥ 3 and d, any fragment of SL over Σ+,≤   is
undecidable.                                                          t
                                                                      u
Remark 2. Note that in the above formalization the only use of associated sums
comes from expressing the size of the set of Address elements. As for our un-
interpreted function c(.) we have ∀x.c(x) ≈ 1, its sum sc is thus the amount of
addresses. Hence, we can encode the halting problem for two-counter machines
in an almost identical way to the encoding presented here, using a generalization
of PA with two uninterpreted functions for l(.) and g(.), and a size operation
replacing c(.) and its associated sum.


5    SL Encodings of Smart Transitions

The definition of SL models in Sections 3 and 4 ensured that the summation
constants sj were respectively equal to the actual summation of all balances
bj (.). In this section, we address the challenge to formalize relations between sj
                                           Summing Up Smart Transitions        11

and bj (.) in a way that the resulting encodings can be expressed in the logical
frameworks of automated reasoners, in particular of SMT solvers and first-order
theorem provers.
    In what follows, we consider a single transaction or one time-step of multiple
transactions over sj , bj (.). We refer to such transitions as smart transitions.
Smart transitions are common in smart contracts, expressing for example the
minting and/or transferring of some coins, as evidenced in Figure 1 and discussed
later.
    Based on Section 3, our smart transitions are encoded in the Σ l,2,d frag-
ment of SL. Note however, that neither decidability nor undecidability of this
fragment is implied by Theorem 4, nor Theorem 5. In this section, we show
that our SL encoding of smart transitions is expressible in first-order logic. We
first introduce a sound, implicit SL encoding, by “hiding” away sum semantics
and using invariant relations over smart transitions (Section 5.1). This encoding
does not allow us to directly assert the values of any balance or sum, but we can
prove that this implicit encoding is complete, relative to a translation function
(Section 5.2).
    By further restricting our implicit SL encoding to this relative complete
setting, we consider counting properties to explicitly reason with balances and
directly express verification conditions with unbounded sums on sj and bj (.).
This is shown in Section 5.3, and we evaluate different variants of the explicit
SL encoding in Section 6, showcasing their practical use and relevance within
automated reasoning.
    To directly present our SL encodings and results in the smart contract do-
main, in what follows we rely on the notation of Table 1. As such, we respectively
denote b, b0 by old-bal, new-bal and write old-sum, new-sum for s, s0 . As al-
ready discussed in Figure 1, the prefixes old- and new- refer to the entire state
expressed in the encoding before and after the smart transition. We explicitly
indicate this state using old-world, new-world respectively. The non-prefixed
versions bal and sum are stand-ins for both the old- and new- versions — Fig-
ure 2 illustrates our setting for the smart transition of minting one coin.
    With this SL notation at hand, we are thus interested in finding first-order
formulas that verify smart transition relations between old-sum and new-sum,
given the relation between old-bal and new-bal. In this paper, we mainly focus
on the smart transitions of minting and transferring money, yet our results could
be used in the context of other financial transactions/software transitions over
unbounded sums.

Example 2. In the case of minting n coins in Figure 1, we require formulas that
(a) describe the state before the transition (the old-world, thus pre-condition),
(b) formalize the transition (the relation between old-bal and new-bal; (i)-
(ii) in Figure 1) and (c) imply the consequences for the new-world ((iii) in
Figure 1). These formulas verify that minting and depositing n coins into some
address result in an increase of the sum by n, that is new-sum = old-sum + n,
as expressed in the functional correctness formula (1) of Figure 1.
12       Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv




      Fig. 2: Implicit SL Encoding of mint1 , where Addr is short for Address.


5.1     SL Encoding using Implicit Balances and Sums
The first encoding we present is a set of first-order formulas with equality over
sorts {Coin, Address}. No additional theories are considered. The Coin sort
represents money, where one coin is one unit of money. The Address sort rep-
resents the account addresses as before. As a consequence, balance functions
and sumPconstants only exist implicitly in this encoding. As such, the property
sum = a∈Address bal(a) cannot be directly expressed in this encoding. Instead,
we formalize this property by using so-called smart invariant relations between
two predicates has-coin and active over coins c ∈ Coin and a ∈ Address, as
follows.
Definition 3 (Smart Invariants). Let has-coin ⊆ Address × Coin and con-
sider active ⊆ Coin. A smart invariant of the pair (has-coin, active) is the
conjunction of the following three formulas
1. Only active coins c can be owned by an address a:
                 ∀c : Coin. ∃a : Address. has-coin(a, c) → active(c) .       (I1)
2. Every active coin c belongs to some address a:
                 ∀c : Coin. active(c) → ∃a : Address. has-coin(a, c) .       (I2)
3. Every coin c belongs to at most one address a:
                ∀c : Coin.∀a, a0 : Address.                                  (I3)
                                                        0           0
                          (has-coin(a, c) ∧ has-coin(a , c) → a ≈ a ) .
                                            Summing Up Smart Transitions        13

We write inv(has-coin, active) to denote the smart invariant (I1)∧(I2)∧(I3)
of (has-coin, active) .

   Intuitively, our smart invariants ensure that a coin c is active iff it is owned
by precisely one address a. Our smart invariants imply the soundness of our
implicit SL encoding, as follows.

Theorem 6 (Soundness of SL Encoding). Given that sum = |active| and
for every a ∈ Address it holds bal(a)
                                   P = |{c ∈ Coin | (a, c) ∈ has-coin}|, then
inv(has-coin, active) =⇒ sum = a∈Address bal(a).                            t
                                                                            u

We say that a smart transition preserves smart invariants, when

                  inv(old-has-coin, old-active)
                       ⇐⇒ inv(new-has-coin, new-active),

    where old-has-coin, old-active and new-has-coin, new-active respec-
tively denote the functions has-coin, active in the states before and after the
smart transition. Based on the soundness of our implicit SL encoding, we for-
malize smart transitions preserving smart invariants as first-order formulas. We
only discuss smart transitions implementing minting n coins here, but other
transitions, such as transferring coins, can be handled in a similar manner. We
first focus on miniting a single coin, as follows.

Definition 4 (Transition mint1 (a, c)). Let there be c ∈ Coin, a ∈ Address.
The transition mint1 (a, c) activates coin c and deposits it into address a.
1. The coin c was inactive before and is active now:

                         ¬old-active(c) ∧ new-active(c) .                    (M1)

2. The address a owns the new coin c:

         new-has-coin(a, c) ∧ ∀a0 : Address. ¬old-has-coin(a0 , c) .         (M2)

3. Everything else stays the same:

          ∀c0 : Coin. c0 6≈ c → (new-active(c0 ) ↔ old-active(c0 )) ,        (M3)
          ∀c0 : Coin. ∀a0 : Address. (c0 6≈ c ∨ a0 6≈ a) →                   (M4)
                                  0   0                      0   0
               (new-has-coin(a , c ) ↔ old-has-coin(a , c )) .

The transition mint1 (a, c) is defined as (M1) ∧ (M2) ∧ (M3) ∧ (M4).

    By minting one coin, the balance of precisely one address, that is of the re-
ceiver’s address, increases by one, whereas all other balances remain unchanged.
Thus, the expected impact on the sum of account balances is also increased by
one, as illustrated in Figure 2. The following theorem proves that the defini-
tion of mint1 is sound. That is, mint1 affects the implicit balances and sums as
expected and hence mint1 preserves smart invariants.
14     Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

Theorem 7 (Soundness of mint1 (a, c)). Let c ∈ Coin, a ∈ Address such
that mint1 (a, c). Consider balance functions old-bal, new-bal : Address → N,
non-negative integer constants old-sum, new-sum, unary predicates old-active,
new-active ⊆ Coin and binary predicates old-has-coin, new-has-coin ⊆
Address × Coin such that

              |old-active| = old-sum , |new-active| = new-sum,

and for every address a0 , we have

            old-bal(a0 ) = |{c0 ∈ Coin | (a0 , c0 ) ∈ old-has-coin}| ,
            new-bal(a0 ) = |{c0 ∈ Coin | (a0 , c0 ) ∈ new-has-coin}| .

    Then, new-sum = old-sum + 1, new-bal(a) = old-bal(a) + 1. Moreover, for
all other addresses a0 6= a, it holds new-bal(a0 ) = old-bal(a0 ).        t
                                                                          u

Smart transitions minting an arbitrary number of n coins, as in our Figure 1, is
then realized by repeating the mint1 transition n times. Based on the soundness
of mint1 , ensuring that mint1 preserves smart invariants, we conclude by induc-
tion that n repetitions of mint1 , that is minting n coins, also preserves smart
invariants. The precise definition of mintn together with the soundness result
is stated in Appendix B.2.

5.2   Completeness Relative to a Translation Function
Smart invariants provide sufficient conditions for ensuring soundness of our SL
encodings (Theorem 6). We next show that, under additional constraints, smart
invariants are also necessary conditions, establishing thus (relative) completeness
of our encodings.
    A straightforward extension of Theorem 6 however does not hold. Namely,
only under the assumptions of Theorem 6, the following formula is not valid:
                     X
           sum =           bal(a)     ⇐⇒      inv(has-coin, active) .
                  a∈Address

    As a counterexample, assume (i) sum = |active|, (ii) for every a ∈ Address
it holds that bal(a) = |{c ∈ Coin | (a, c) ∈ has-coin}|, that is the assumptions
of Theorem 6. Further, let (iii) the smart invariants inv(has-coin, active) hold
for all but the coins c1 , c2 ∈ Coin and all but the addresses a1 , a2 ∈ Address.
We also assume that (iv) c1 is active but not owned by any address and (v) c2
is
Pactive and owned by the two distinct addresses a1 , a2 . We thus have sum =
   a∈Address bal(a), yet inv(has-coin, active) does not hold.
    To ensure completeness of our encodings, we therefore introduce a translation
function f that restricts the set F , 2Address×Coin × 2Coin of (has-coin, active)
pairs, as follows. We exclude from F those pairs (has-coin, active) that violate
smart invariants by both (i) not satisfying (I2), as (I2) ensures that there are
not too many active coins, and by (ii) not satisfying at least one of (I1) and
                                           Summing Up Smart Transitions        15

(I3), as (I1) and (I3) ensure that there are not too few active coins. The re-
quired translation function f (Appendix B.3) now assigns every pair (bal, sum)
the set of all (has-coin, active) ∈ F that satisfy sum = |active|, bal(a) =
|{c ∈ Coin | has-coin(a, c)}| for every address a and have not been excluded.

Theorem 8 (Relative Completeness of SL Encoding). Let (bal, sum) ∈
NAddress × N and let (has-coin, active) ∈ f (bal, sum) be arbitrary. Then,
                X
        sum =          bal(a)   ⇐⇒     inv (has-coin, active) .        t
                                                                       u
               a∈Address


5.3    SL Encodings using Explicit Balances and Sums
We now restrict our SL encoding from Section 5.1 to explicitly reason with
balance functions during smart transitions. We do so by expressing our transla-
tion function f from Section 5.2 in first-order logic. We now use the summation
constant sum ∈ N and the balance function bal : Address → N in our SL en-
coding. In particular, we use our smart invariants inv(has-coin, active) in
this explicit SL encoding together with two additional axioms (Ax1, Ax2), en-
suring that sum = |active| and bal(a) = |{c ∈ Coin | has-coin(a, c)}| for all
a ∈ Address.
    To formalize the additional properties, we introduce two counting mecha-
nisms in our SL encoding. The first one is a bijective function count : Coin → N+
and the second one is a function idx : Address × Coin → N+ , where idx(a, .) :
Coin → N+ is bijective for every a ∈ Address. To ensure that count and idx(a, .)
count coins, we impose the following two properties:

                   ∀c : Coin. active(c) ⇐⇒ count(c) ≤ sum ,                (Ax1)

      ∀c : Coin. ∀a : Address. has-coin(a, c) ⇐⇒ idx(a, c) ≤ bal(a) .      (Ax2)
    Figure 3 illustrates our revised SL encoding for our smart transition mint1 .
We next ensure soundness of our resulting explicit encoding for summation, as
follows.

Theorem 9 (Soundness of Explicit SL Encodings). Let there be a pair
(bal, sum) ∈ NAddress × N, a pair (has-coin, active) ∈ F, and functions count :
Coin → N+ and idx : Address × Coin → N+ .
   Given that count is bijective, idx(a, .) : Coin → N+ is bijective for every a ∈
Address, and that (Ax1), (Ax2) and inv (has-coin, active) hold, then, sum =
|active| and bal(a) = |{c ∈ CoinP: has-coin(a, c)}|, for every a ∈ Address.
   In particular, we have sum = a∈Address bal(a).                                t
                                                                                 u

    When compared to Section 5.1, our explicit SL encoding introduced above
uses our smart invariants as axioms of our encoding, together with (Ax1) and
(Ax2). In our explicit SL encoding, the post-conditions asserting functional cor-
rectness of smart transitions express thus relations among old-sum to new-sum.
For example, for mintn we are interested in ensuring
16      Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv




     Fig. 3: Explicit SL Encoding of mint1 , where Addr is short for Address.

                        mintn ⇒ new-sum = old-sum + n .                            (2)

By using two new constants old-total, new-total ∈ N, we can use sum = total
as smart invariant for mintn . As a result, the property to be ensured is then

         (old-sum = old-total ∧ new-total = old-total + n ∧ mintn )
                                                                                   (3)
         ⇒ (new-sum = new-total) .

    It is easy to see that the negations of (2) and (3) are equisatisfiable. We note
however that the additional constants old-total, new-total used in (3) lead
to unstable results within automated reasoners, as discussed in Section 6.


6    Experiments
From Theory to Practice. To make our explicit SL encodings handier for
automated reasoners, we improved the setting illustrated in Figure 3 by applying
the following restrictions without losing any generality.
(i) The predicates has-coin and active were removed from the explicit SL
encodings, by replacing them by their equivalent expressions (Ax1)-(Ax2).
(ii) The surjectivity assertions of count and idx were restricted to the relevant
intervals [1, sum], [1, bal(a)] respectively.
(iii) Compared to Figure 3, only one mutual count and one mutual idx functions
were used. We however conclude that we do not lose expressivity of our resulting
SL encoding, as shown in Appendix B.5.
(iv) When our SL encoding contains expressions such as ∀c : Coin. idx(a0 , c) ∈
[l0 , u0 ] ⇐⇒ idx(a1 , c) ∈ [l1 , u1 ], with a0 , a1 being distinct addresses such that
either ui ≤ bal(ai ) or li > bal(ai ), i ∈ {0, 1}, then it can be assumed that the
coins in those intervals are in the same order for both functions (Appendix B.6).
                                            Summing Up Smart Transitions        17




                            Fig. 4: Linked Lists in id.


    Based on the above, we derive three different explicit SL encodings to be
used in automated reasoning about smart transitions. We respectively denote
these explicit SL encodings by int, nat and id, and describe them next.
Benchmarks. In our experiments, we consider four smart transitions mint1 ,
mintn , transferFrom1 and transferFromn , respectively denoting minting and
transferring one and n coins. These transitions capture the main operations of
linear integer arithmetic. In particular, mintn implements the smart transition
of our running example from Figure 1.
    For each of the four smart transitions, we implement four SL encodings: the
implicit SL encoding uf from Section 5.1 using only uninterpreted functions
and three explicit encodings int, nat and id as variants of Section 5.3. We
also consider three additional arithmetic benchmarks using int, which are not
directly motivated by smart contracts. Together with variants of int and nat
presented in the sequel, our benchmark set contains 31 examples altogether, with
each example being formalized in the SMT-LIB input syntax [1]. In addition to
our encodings, we also proved consistency of the axioms used in our encodings.
SL Encodings and Relaxations. Our explicit SL encoding int uses linear
integer arithmetic, whereas nat and id are based on natural numbers. As nat-
urals are not a built-in theory in SMT-LIB, we assert the axioms of Presburger
arithmetic directly in the encodings of nat and id.
    In our id encodings, inductive datatypes are additionally used to order coins.
There exists one linked list of all coins for count and one for each idx(a, .),
a ∈ Address. Additionally, there exists a “null” coin, which is the first ele-
ment of every list and is not owned by any address. As shown in Figure 4, the
numbering of each coin is defined by its position in the respective list. This
way surjectivity for count and idx can respectively be asserted by the formu-
las ∃c : Coin. count(c) ≈ sum and ∀a : Address. ∃c : Coin. idx(a, c) ≈ bal(a).
However, asserting surjectivity for int and nat cannot be achieved without quan-
tifying over N+ . Such quantification would drastically effect the performance of
automated reasoners in (fragments of) first-order logics. As a remedy, within
the default encodings of int and nat, we only consider relevant instances of
surjectivity.
    Further, we consider variations of int and nat by asserting proper surjectiv-
ity to the relevant intervals of idx and count (denoted as surj ) and/or adding the
total constants mentioned in Section 5.3 (denoted as with total, no total) .
These variations of int and nat are implemented for mint1 and transferFrom1 .
Experimental Setting. We evaluated our benchmark set of 31 examples using
SMT solvers Z3 [7] and CVC4 [6], as well as the first-order theorem prover
18          Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

                     mint1                               transferFrom1
no total         Z3      CVC4 Vampire no total           Z3      CVC4 Vampire
 nat                0.02     ×    0.92 nat                    ×        × 15.35
 nat surj.            ×      ×      × nat surj.           100.03       ×    ×
 int                0.02   0.03     × int                   0.02    0.07    ×
 int surj.            ×    5.96     × int surj.             1.02       ×    ×
with total       Z3      CVC4 Vampire with total         Z3      CVC4 Vampire
 nat                0.03     ×    2.92 nat                  0.28       × 22.54
 nat surj.          0.11     ×      × nat surj.            38.24       ×    ×
 int                0.02   0.03     × int                   0.02    0.10    ×
 int surj.          3.81   5.95     × int surj.               ×     6.56    ×

Table 3: Results of mint1 and transferFrom1 using nat and int, with/without
the total Constants and with/without Surjectivity.
                                             Task
    Encoding
                      mint1    transferFrom1      mintn        transferFromn
               Z3:       0.01 Z3:        0.02 Z3:          × Z3:            ×
       uf      CVC4:     0.02 CVC4:      0.03 CVC4:        × CVC4:          ×
               Vampire: 0.18 Vampire:    0.19 Vampire: 0.35∗ Vampire:    0.44∗
               Z3:       0.02 Z3:          × Z3:           × Z3:            ×
      nat      CVC4:       × CVC4:         × CVC4:         × CVC4:          ×
               Vampire: 0.92 Vampire: 15.35 Vampire: 23.23† Vampire: 228.22†
               Z3:       0.02 Z3:        0.02 Z3:        0.03 Z3:         0.11
      int      CVC4:     0.03 CVC4:      0.07 CVC4:      0.05 CVC4:       0.35
               Vampire:    × Vampire:      × Vampire:      × Vampire:       ×
               Z3:         × Z3:           × Z3:           × Z3:            ×
       id      CVC4:       × CVC4:         × CVC4:         × CVC4:          ×
               Vampire: 7.36‡ Vampire: 17.16‡ Vampire: 23.52‡ Vampire:      ×
         Table 4: Smart Transitions using Implicit/Explicit SL Encodings.

Vampire [18]. Our experiments were run on a standard machine with an Intel
Core i5-6200U CPU (2.30GHz, 2.40GHz) and 8 GB RAM. The time is given
in seconds and we ran all experiments with a time limit of 300s. Time out is
indicated by the symbol ×. The default parameters were used for each solver,
unless stated otherwise in the corresponding tables. The precise calls of the
solvers, together with examples of the encodings, can be found in Appendix C7 .
Experimental Analysis. We first report on our experiments using different
variations of int and nat. Table 3 shows that asserting complete surjectivity for
int and nat is computationally hard and indeed significantly effects the perfor-
mance of automated reasoners. Thus, for the following experiments only relevant
instances of surjectivity, such as ∃c : Coin. count(c) = sum were asserted in int
and nat. Table 3 also illustrates the instability of using the total constant.
Some tasks seem to be easier even though their reasoning difficulty increased
strictly by adding additional constants.
    Our most important experimental findings are shown in Table 4, demonstrat-
ing that our SL encodings are suitable for automated reasoners. Thanks to our
7
     All encodings are available at github.com/SoRaTu/SmartSums.
                                           Summing Up Smart Transitions       19

                             Task
                                                                Time
               Transition                  Impact
                                                           Z3:        0.20
     new-bal(a0 ) = old-bal(a0 ) + 3
                                     new-sum = old-sum     CVC4:      1.28
     new-bal(a1 ) = old-bal(a1 ) − 3
                                                           Vampire:     ×
                                                           Z3:        0.58
     new-bal(a0 ) = old-bal(a0 ) + 4
                                     new-sum = old-sum + 2 CVC4:      7.14
     new-bal(a1 ) = old-bal(a1 ) − 2
                                                           Vampire:     ×
     new-bal(a0 ) = old-bal(a0 ) + 5                       Z3:        1.52
     new-bal(a1 ) = old-bal(a1 ) − 3 new-sum = old-sum + 1 CVC4:    155.20
     new-bal(a2 ) = old-bal(a2 ) − 1                       Vampire:     ×
       Table 5: Arithmetic Reasoning in the Explicit SL Encoding int.

explicit SL encodings, each solver can certify every smart transition in at least
one encoding. Our explicit SL encodings are more relevant than the implicit
encoding uf as we can express and compare any two non-negative integer sums,
whereas for uf handling arbitrary values n can only be done by iterating over the
mint1 (or transferFrom1 ) transition. This iteration requires inductive reason-
ing, which currently only Vampire could do [14], as indicated by the superscript
∗. Nevertheless, the transactions mint1 , transferFrom1 , which involve only one
coin in uf, require no inductive reasoning as the actual sum is not considered;
each of our solvers can certify these examples.
    We note that the tasks mintn and transferFromn from Table 4 yield a huge
search space when using their explicit SL encodings within automated reasoners.
We split these tasks into proving intermediate lemmas and proved each of these
lemmas independently, by the respective solver. In particular, we used one lemma
for mintn and four lemmas for transferFromn . In our experiments, we only
used the recent theory reasoning framework of Vampire with split queues [12]
and indicate our results in by superscript †.
    We further remark that our explicit SL encoding id using inductive datatypes
also requires inductive reasoning about smart transitions and beyond. The need
of induction explains why SMT solvers failed proving our id benchmarks, as
shown in Table 4. We note that Vampire found a proof using built-in induc-
tion [14] and theory-specific reasoning [12], as indicated by superscript ‡.
    We conclude by showing the generality of our approach beyond smart tran-
sitions.
P        It inPfact enables fully automated reasoning about any two summations
   i∈I g(i),    i∈I h(i) of non-negative integer values g(i), h(i) (i ∈ I) over a
mutual finite set I. The examples of Table 5 affirm this claim.


7   Related work

Smart Contract Safety. Formal verification of smart contracts is an emerging hot
topic because of the value of the assets stored in smart contracts, e.g. the DeFi
software [3]. Due to the nature of the blockchain, bugs in smart contracts are
irreversible and thus the demand for provably bug-free smart contracts is high.
20      Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

    The K interactive framework has been used to verify safety of a smart con-
tract, e.g. in [22]. Isabelle [21] was also shown to be useful in manual, interactive
verification of smart contracts [16]. We, however, focus on automated approaches.
   There are also efforts to perform deductive verification of smart contracts
both on the source level in languages such as Solidity [32,4,13] and Move [34],
as well as on the the Ethereum virtual machine (EVM) level [2,28]. This paper
improves the effectiveness of these approaches by developing techniques for au-
tomatically reasoning about unbounded sums. This way, we believe we support
a more semantic-based verification of smart contracts.
   Our approach differs from works using ghost variables [13], since we do not
manually update the “ghost state”. Instead, the verifier needs only to reason
about the local changes, and the aggregate state is maintained by the axioms.
That means other approaches assume (a) the local changes and (b) the impact
on ghost variables (sum), whereas we only assume (a) and automatically prove
a ⇒ b. This way, we reduce the user-guidance in providing and proving (b).
   Our work complements approaches that verify smart contracts as finite state
machines [32] and methods, like ZEUS [17], using symbolic model checking and
abstract interpretation to verify generic safety properties for smart contracts.
    The work in [29] provides an extensive evaluation of ERC-20 and ERC-721
tokens. ERC-721 extends ERC-20 with ownership functions, one of which being
“approve”. It enables transactions on another party’s behalf. This is independent
of our ability to express sums in first-order logic, as the transaction’s initiator is
irrelevant to its effect.
Reasoning about Financial Applications. Recently, the Imandra prover intro-
duced an automated reasoning framework for financial applications [23,24,25].
Similarly to our approach, these works use SMT procedures to verify and/or gen-
erate counter-examples to safety properties of low- and high-level algorithms. In
particular, results of [23,24,25] include examples of verifying ranking orders in
matching logics of exchanges, proving high-level properties such as transitivity
and anti-symmetry of such orders. In contrast, we focus on verifying proper-
ties relating local changes in balances to changes of the global state (the sum).
Moreover, our encodings enable automated reasoning both in SMT solving and
first-order theorem proving.
Automated Aggregate Reasoning. The theory of first-order logic with aggregate
operators has been thoroughly studied in [15,20]. Though proven to be strictly
more expressive than first-order logic, both in the case of general aggregates
as well as simple counting logics, in this paper we present a practical way to
encode a weakened version of aggregates (specifically sums) in first-order logic.
Our encoding (as in Section 5) works by expressing particular sums of interest,
harnessing domain knowledge to avoid the need of general aggregate operators.
    Previous works [19,5] in the field of higher-order reasoning do not directly
discuss aggregates. The work of [19] extends Presburger arithmetic with Boolean
algebra for finite, unbounded sets of uninterpreted elements. This includes a way
to express the set cardinalities and to compare them against integer variables,
                                            Summing Up Smart Transitions         21

but does not support uninterpreted functions, such as the balance functions we
use throughout our approach.
    The SMT-based framework of [5] takes a different, white-box approach, mod-
ifying the inner workings of SMT solvers to support higher-order logic. We on the
other hand treat theorem provers and SMT solvers as black-boxes, constructing
first-order formulas that are tailored to their capabilities. This allows us to use
any off-the-shelf SMT solver.
    In [8], an SMT module for the theory of FO(Agg) is presented, which can be
used in all DPLL-based SAT, SMT and ASP solvers. However, FO(Agg) only
provides a way to express functions that have sets or similar constructs as inputs,
but not to verify their semantic behavior.


8   Conclusions

We present a methodology for reasoning about unbounded sums in the context
of smart transitions, that is transitions that occur in smart contracts modeling
transactions. Our sum logic SL and its usage of sum constants, instead of fully-
fledged sum operators, turns out to be most appropriate for the setting of smart
contracts. We show that SL has decidable fragments (Section 4.1), as well as
undecidable ones (Section 4.2). Using two phases to first implicitly encode SL in
first-order logic (Section 5.1), and then explicitly encode it (Section 5.3), allows
us to use off-the-shelf automated reasoners in new ways, and automatically verify
the semantic correctness of smart transitions.
    Showing the (un)decidability of the SL fragment with two sets of uninter-
preted functions and sums is an interesting step for further work, as this fragment
supports encoding smart transition systems. Another interesting direction of fu-
ture work is to apply our approach to different aggregates, such as minimum
and maximum and to reason about under which conditions these values stay
above/below certain thresholds. A slightly modified setting of our SL axioms
can already handle min/max aggregates in a basic way, namely by using ≥ and
≤ instead of equality and dropping the injectivity/surjectivity (respectively) ax-
ioms of the counting mechanisms.
    Summing upon multidimensional arrays in various ways is yet another direc-
tion of future research. Our approach supports the summation over all values
in all dimensions by adding the required number of parameters to the predicate
idx and by adapting the axioms accordingly.


Acknowledgements

We thank Petra Hozzová for fruitful discussions on our encodings and Sharon
Shoham-Buchbinder for her insights and contributions to this paper. This work
was partially funded by the ERC CoG ARTIST 101002685, the ERC StG SYM-
CAR 639270, the United States-Israel Binational Science Foundation (BSF)
grant No. 2016260, Grant No. 1810/18 from the Israeli Science Foundation, Len
22     Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

Blavatnik and the Blavatnik Family foundation, the FWF grant LogiCS W1255-
N23, the TU Wien DK SecInt and the Amazon ARA 2020 award FOREST.
                                            Summing Up Smart Transitions         23

References
 1. SMTLIB: Satisfiability Modulo Theories Library.,
    https://smtlib.cs.uiowa.edu/papers/smt-lib-reference-v2.6-r2017-07-18.pdf
 2. Certora Ltd: The Certora Verifier (2020), www.certora.com
 3. Concourse Open Community: DeFi Pulse (2020), https://defipulse.com/
 4. Alt, L.: Solidity’s SMTChecker can Automatically find Real Bugs (2019),
    https://medium.com/@leonardoalt/
    soliditys-smtchecker-can-automatically-find-real-bugs-beb566c24dea
 5. Barbosa, H., Reynolds, A., El Ouraoui, D., Tinelli, C., Barrett, C.: Extending
    SMT Solvers to Higher-Order Logic. In: CADE. pp. 35–54 (2019)
 6. Barrett, C., Conway, C.L., Deters, M., Hadarean, L., Jovanović, D., King, T.,
    Reynolds, A., Tinelli, C.: CVC4. In: CAV. pp. 171–177 (2011)
 7. De Moura, L., Bjørner, N.: Z3: An efficient SMT Solver. In: TACAS. pp. 337–340
    (2008)
 8. Denecker, M., De Cat, B.: DPLL (Agg): An efficient SMT Module for
    Aggregates. In: Logic and Search (2010)
 9. Dutertre, B., De Moura, L.: The Yices SMT Solver. Tool paper at
    http://yices.csl.sri.com/tool-paper.pdf pp. 1–2 (2006)
10. Emerson, A.: Modal and Temporal Logics. In: Handbook of Theoretical
    Computer Science, Volume B, pp. 995–1072 (1990)
11. Etessami, K.: Counting Quantifiers, Successor Relations, and Logarithmic Space.
    In: JCSS. pp. 400–411 (1997)
12. Gleiss, B., Suda, M.: Layered Clause Selection for Saturation-Based Theorem
    Proving. In: IJCAR. pp. 34–52 (2020)
13. Hajdu, Á., Jovanovic, D.: solc-verify: A Modular Verifier for Solidity Smart
    Contracts. In: VSTTE. pp. 161–179 (2019)
14. Hajdú, M., Hozzová, P., Kovács, L., Schoisswohl, J., Voronkov, A.: Induction
    with Generalization in Superposition Reasoning. In: CICM. pp. 123–137 (2020)
15. Hella, L., Libkin, L., Nurmonen, J., Wong, L.: Logics with Aggregate Operators.
    In: J. ACM. pp. 880–907 (2001)
16. Hirai, Y.: Defining the Ethereum Virtual Machine for Interactive Theorem
    Provers. In: FC. pp. 520–535 (2017)
17. Kalra, S., Goel, S., Dhawan, M., Sharma, S.: ZEUS: Analyzing Safety of Smart
    Contracts. In: NDSS (2018)
18. Kovács, L., Voronkov, A.: First-Order Theorem Proving and Vampire. In: CAV.
    pp. 1–35 (2013)
19. Kuncak, V., Nguyen, H.H., Rinard, M.: An Algorithm for Deciding BAPA:
    Boolean Algebra with Presburger Arithmetic. In: CADE. pp. 260–277 (2005)
20. Libkin, L.: Logics with Counting, Auxiliary Relations, and Lower Bounds for
    Invariant Queries. In: LICS. pp. 316–325 (1999)
21. Nipkow, T.: Interactive Proof: Introduction to Isabelle/HOL. In: Software Safety
    and Security, pp. 254–285 (2012)
22. Park, D., Zhang, Y., Rosu, G.: End-to-End Formal Verification of Ethereum 2.0
    Deposit Smart Contract. In: CAV. pp. 151–164 (2020)
23. Passmore, G.O., Cruanes, S., Ignatovich, D., Aitken, D., Bray, M., Kagan, E.,
    Kanishev, K., Maclean, E., Mometto, N.: The Imandra Automated Reasoning
    System (System Description). In: IJCAR. pp. 464–471 (2020)
24. Passmore, G.O.: Formal Verification of Financial Algorithms with Imandra. In:
    FMCAD. pp. i–i (2018)
24      Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

25. Passmore, G.O., Ignatovich, D.: Formal Verification of Financial Algorithms. In:
    CADE. pp. 26–41 (2017)
26. Presburger, M.: Über die Vollständigkeit eines gewissen Systems der Arithmetik
    ganzer Zahlen, in welchem die Addition als einzige Operation hervortritt. In:
    Comptes Rendus du I congres de Mathématiciens des Pays Slaves. pp. 92–101
    (1929)
27. Sadiku, M., Eze, K., Musa, S.: Smart Contracts: A Primer (2018)
28. Schneidewind, C., Grishchenko, I., Scherer, M., Maffei, M.: eThor: Practical and
    Provably Sound Static Analysis of Ethereum Smart Contracts. In: CCS. pp.
    621–640 (2020)
29. Stephens, J., Ferles, K., Mariano, B., Lahiri, S., Dillig, I.: SmartPulse: Automated
    Checking of Temporal Properties in Smart Contracts. In: IEEE S&P (2021)
30. Väänänen, J.A.: Generalized Quantifiers. In: Bull. EATCS (1997)
31. Vogelsteller, F., Buterin, V.: EIP-20: ERC-20 Token Standard. In: EIP no.20
    (2015)
32. Wang, Y., Lahiri, S.K., Chen, S., Pan, R., Dillig, I., Born, C., Naseer, I., Ferles,
    K.: Formal Verification of Workflow Policies for Smart Contracts in Azure
    Blockchain. In: VSTTE. pp. 87–106 (2019)
33. Weidenbach, C., Dimova, D., Fietzke, A., Kumar, R., Suda, M., Wischnewski, P.:
    SPASS Version 3.5. In: CADE. pp. 140–145 (2009)
34. Zhong, J.E., Cheang, K., Qadeer, S., Grieskamp, W., Blackshear, S., Park, J.,
    Zohar, Y., Barrett, C., Dill, D.L.: The Move Prover. In: CAV. pp. 137–150 (2020)
                                                     Summing Up Smart Transitions                25

A      Proofs for Sum Logic
Definition 5 (SL Structure).
   Let Σ be an SL vocabulary. We write a structure A = (D, I) ∈ STRUCT [Σ]
as a tuple
      A = A, N, aA            A A               A A               A A               A
                                                                                                   
                 1 , . . . , al , b1 , . . . , bm , c1 , . . . , cd , s1 , . . . , sm , 0, 1, +, ≤

where A = D(Address) is some finite 8 , possibly empty set. We have aA  i =
I(ai ) ∈ A; bA       1     A       A            A
             j = I(bj ) ∈ N ; and ck = I(ck ), sj = I(sj ) ∈ N.
   We always assume that D(Nat) = N, and that 0, 1, +2 and ≤2 are interpreted
naturally. For brevity, we omit them when describing SL structures.

Distinct Models Proof
Observation 1. For any set X and any partition P thereof, it holds that |P | ≤
|X|.
Definition 6 (Partition-Induced Function).
    Let P be a partition of a finite set X of size l. P = {A1 , . . . , Al0 } where l0 ≤ l.
    We define the partition-induced function fP (x) (for any x ∈ X) as the index
i such that Ai ∈ P and x ∈ Ai .
    For brevity, we denote fP (x) as P (x).
Definition 7 (Function-Induced Equivalence Class).
   Let f be some function over some set X. We define the function-induced
equivalence class for each x ∈ X as
                              [x]f , {x0 ∈ X | f (x0 ) = f (x)} .
Definition 8 (Function-Induced Partition).
   Let f be some function defined over some set X. We define the function-
induced partition Pf as
                           Pf , {[x]f | x ∈ X} .
Definition 9 (Partitioning Sum Terms by P ).
    Let t be some term over an SL vocabulary Σ = Σ l,m,d (with l Address
constants) and let P be some partition of {a1 , . . . , al }.
    We define a transformation TP (t) inductively as a term over an SL vocabu-
              0
lary ΣP = Σ l ,m,d with l0 = |P | ≤ l Address constants:
                
                
                 aP (ai )            if t = ai
                 xi                  if t = xi of sort Address
                
                
       TP (t) , sj                    if t = sj
                 bj (TP (t1 ))       if t = bj (t1 ) where t1 is some ai or xi
                
                
                
                  TP (t1 ) + TP (t2 ) if t = t1 + t2
                
8
    In
     fact, we need only to  require that the set of addresses with non-zero balances
     α ∈ D(Address) | ∀j.bA
                          j (α) > 0   be finite. Except for addresses that are referred
    by an Address constant, we can always discard all zero-balance addresses from a
    model. Thus, we might as well limit ourselves to finite sets of addresses.
26       Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

Definition 10 (Partitioning an SL Formula by P ). We naturally extend
the terms transformation TP to formulas.
Observation 2. For any SL vocabulary Σ, ΣP ⊆ Σ, since l0 ≤ l. Therefore, for
any formula ϕ in some fragment FRAG of SL, TP (ϕ) ∈ FRAG as well.
Definition 11 (Distinct Structures).
    An SL structure A is considered distinct when aA                A
                                                     
                                                       1 , . . . , al = l. I.e. the
l Address constants represent l distinct elements in D(Address).
Theorem 1 (Distinct Models). Let ϕ be an SL formula over Σ, then ϕ
has a model iff there exists a partition P of {a1 , . . . , al } such that TP (ϕ) has a
distinct model.                                                                       t
                                                                                      u
Proof of Theorem 1

Part 1: If ϕ has an SL model, then there exists some partition P such
that TP (ϕ) has a distinct SL model (⇒)
Let A be some SL model of ϕ and let f be the mapping from {a1 , . . . , al } to A,
i.e
                               f (ai ) , aA
                                          i
   Let P be the partition (of size l0 ) induced by f and we construct a distinct
SL model
           A0 = A, a01 , . . . , a0l0 , bA            A A               A A               A
                                                                                            
                                         1 , . . . , bm , c1 , . . . , cn , s1 , . . . , sm

for TP (ϕ), where A, bA              A    A            A         A           A
                        1 , . . . , bm , c1 , . . . , cn , and s1 , . . . , sm are taken from A.
    For every i0 ∈ [1, l0 ], a0i0 is defined as a0i0 = aA      i   for   some   i ∈ [1, l] such that
P (ai ) = i0 .
Remark 3. The choice of i is unimportant, since for any two indices i1 , i2 , if
P (ai1 ) = i0 = P (ai2 ) then by definition of P , aA     A
                                                    i1 = ai2 .
Observation 3. A0 is distinct and holds the sum property.
Claim 1. For any closed term t over Σ, I(t) = I 0 (TP (t)) (i.e. the interpretation
of t in A equals to the interpretation of TP (t) in A0 ).
Proof. Since TP (t) = t for all terms except terms containing ai , and since A0 is
identical to A except for Address constants, we only need to consider this kind
of terms.
    Moreover, since TP is defined inductively, it suffices to prove the claim for
the basis terms ai .
    Let t = ai for some i ∈ [1, l], and let i0 = P (ai ):

                                  I 0 (TP (t)) = I 0 (TP (ai ))
                                              = I 0 (ai0 )
                                              = a0i0
                                              = aA
                                                 i
                                              = I(ai ) = I(t)
                                                   Summing Up Smart Transitions         27

Claim 2. For any term t with free variables x1 , . . . , xr (of sort Address), for
all α1 , . . . , αr ∈ A, for any assignment ∆, let ∆0 = ∆ [α1 /x1 , . . . , αr /xr ], and
                         0
therefore I∆0 (t) = I∆     0 (TP (t)).


Proof. Identical to the proof of Claim 1.

Claim 3. Let ξ be a sub-formula of ϕ, therefore:

 1. If ξ is a closed formula then A  ξ ⇐⇒ A0  TP (ξ)
 2. If ξ is a formula with free variables x1 , . . . , xr then for any α1 , . . . , αr ∈ A,
    A  ξ [α1 /x1 , . . . , αr /xr ] ⇐⇒ A0  TP (ξ) [α1 /x1 , . . . , αr /xr ]

Since ϕ is a closed formula, and since A  ϕ, it holds that A0  TP (ϕ) and
therefore A0 is a distinct SL model for TP (ϕ).

Proof (Claim 3). Let us consider the following cases:
Case 1.1 : ξ = t1 ≈ t2 without free variables
   Follows from Claim 1.
Case 1.2 : ξ = t1 ≈ t2 with free variables x1 , . . . , xr
   Follows from Claim 2.
Case 1.3 : ξ = ¬ζ without free variables
   ζ is also a closed sub-formula of ϕ and from the induction hypothesis:


                                 A  ξ ⇐⇒ A 2 ζ
                                          ⇐⇒ A0 2 TP (ζ)
                                          ⇐⇒ A0  TP (ξ)

Case 1.4 : ξ = ¬ζ with free variables x1 , . . . , xr
   ζ is also a sub-formula of ϕ with free variables x1 , . . . , xr and from the in-
duction hypothesis, for any α1 , . . . , αr ∈ A:


                      A ξ [α1 /x1 , . . . , αr /xr ]
                            ⇐⇒ A 2 ζ [α1 /x1 , . . . , αr /xr ]
                            ⇐⇒ A0 2 TP (ζ) [α1 /x1 , . . . , αr /xr ]
                            ⇐⇒ A0  TP (ξ) [α1 /x1 , . . . , αr /xr ]

Case 1.5 : ξ = ζ1 ∨ ζ2 without free variables
   ζ1 , ζ2 are also closed sub-formulas of ϕ, and from the induction hypothesis:


                      A  ξ ⇐⇒ A  ζ1 or A  ζ2
                               ⇐⇒ A0  TP (ζ1 ) or A0  TP (ζ2 )
                               ⇐⇒ A0  TP (ξ)
28        Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

Case 1.6 : ξ = ζ1 ∨ ζ2 with free variables x1 , . . . , xr
   ζ1 , ζ2 are also sub-formulas of ϕ with (at most) free variables x1 , . . . , xr , and
from the induction hypothesis, for any α1 , . . . , αr :


                         A  ξ [α1 /x1 , . . . , αr /xr ]
                              ⇐⇒ A  ζ1 [α1 /x1 , . . . , αr /xr ]
                                   or A  ζ2 [α1 /x1 , . . . , αr /xr ]
                              ⇐⇒ A0  TP (ζ1 ) [α1 /x1 , . . . , αr /xr ]
                                   or A0  TP (ζ2 ) [α1 /x1 , . . . , αr /xr ]
                              ⇐⇒ A0  TP (ξ) [α1 /x1 , . . . , αr /xr ]

Case 1.7 : ξ = ∀x.ζ without free variables
   ζ is a sub-formula of ϕ with (at most) one free variable x. From the induction
hypothesis:


                       A  ξ ⇐⇒ For any α ∈ A.A  ζ [α/x]
                                ⇐⇒ For any α ∈ A.A0  TP (ζ) [α/x]
                                ⇐⇒ A  TP (ξ)

Case 1.8 : ξ = ∀x.ζ with free variables x1 , . . . , xr
   ζ is a sub-formula of ϕ with (at most) m + 1 free variables x, x1 , . . . , xr . From
the induction hypothesis, for any α1 , . . . , αr ∈ A:


              A  ξ [α1 /x1 , . . . , αr /xr ]
                  ⇐⇒ For any α ∈ A.A  ζ [α/x, α1 /x1 , . . . , αr /xr ]
                  ⇐⇒ For any α ∈ A.A0  TP (ζ) [α/x, α1 /x1 , . . . , αr /xr ]
                  ⇐⇒ A0  TP (ξ) [α1 /x1 , . . . , αr /xr ]

Part 2: If there exists some partition P such that TP (ϕ) has a distinct
SL model, then ϕ has an SL model (⇐)
Let A0 be some SL model for TP (ϕ) and we construct an SL model

            A = A, aA            A A               A A               A A               A
                                                                                         
                    1 , . . . , al , bm , . . . , bm , cn , . . . , cn , sm , . . . , sm

for ϕ, where A, bA             A    A            A        A            A                 0
                  m , . . . , bm , cn , . . . , cn , and sm , . . . , sm are taken from A .
                              A                       A     0
    For every i ∈ [1, l], ai is defined as: ai = aP (ai ) .

Observation 4. A is a Sum structure, and holds the sum property.

Claim 4. For any closed term t, I(t) = I 0 (TP (t))
                                                      Summing Up Smart Transitions            29

Proof. Similarly to Claim 1, we only need to consider t = ai , and we get:


                               I(t) = I(ai )
                                      = aA
                                         i
                                      = a0P (ai )
                                      = I 0 (aP (ai ) ) = I 0 (TP (t))

Claim 5. For any term t with free variables x1 , . . . , xr , for any assignment ∆,
and for any α1 , . . . , αr ∈ A, we define ∆0 = ∆ [α1 /x1 , . . . , αr /xr ], and
                                                  0
            I∆0 (t [α1 /x1 , . . . , αr /xr ]) = I∆ 0 (TP (t) [α1 /x1 , . . . , αr /xr ]) .



Proof. Identical to the proof of Claim 4.
Claim 6. Let ξ be a sub-formula of ϕ, therefore:

 1. If ξ is a closed formula, then A0  TP (ξ) ⇐⇒ A  ξ.
 2. If ξ is a formula with free variables x1 , . . . , xr then for every α1 , . . . , αr ∈ A,
    A0  TP (ξ) [α1 /x1 , . . . , αr /xr ] ⇐⇒ A  ξ [α1 /x1 , . . . , αr /xr ]

Since ϕ is a closed formula, and since A  TP (ϕ) we get that A0  ϕ.
Proof (Claim 6). In the same vain of Claim 3, this follows from Claims 4 and 5.

                                      Q.E.D. Theorem 1.

Small Address Space Proof
Definition 2 (Small Address Space). Let FRAG be some fragment of SL
                       l,m,d
over vocabulary Σ = Σ+,≤     . FRAG is said to have small Address space if there
exists a computable function κΣ (.), such that for any SL formula ϕ ∈ FRAG,
ϕ has a distinct model iff ϕ has a distinct model A = (D, I) with small Address
space, where |D(Address)| ≤ κΣ (|ϕ|).
    We call κΣ (.) the bound function of FRAG; when the vocabulary is clear
from context we simply write κ(.).
Theorem 2 (Small Address Space of (l, 1, d)-FRAG).
   For any l, d, it holds (l, 1, d)-FRAG, the fragment of SL formulas over the
SL vocabulary
                     l,1,d
                           = a1 , . . . , al , b1 , c1 , . . . , cd , s, 0, 1 ,
                                                                             
                    Σ+, ≤
                     
has small Address space with bound function κ(x) = l + x + 1.                   t
                                                                                u
Proof of Theorem 2
                                                        l,1,d
Let there be some universal, closed formula ϕ over Σ = Σ+, ≤
                                                              and let there be
                                                        
some minimal structure A ∈ STRUCT [Σ] such that A SL ϕ (i.e. A is an SL
model for ϕ).
30      Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

    We denote the (finite) size of A as z , |A|, and we assume towards contra-
diction that z ≥ l + |ϕ| + 1 (as our bound function is κ(x) = l + x + 1). We
construct a smaller model A0 for ϕ. Thus contradicting the minimality of A, and
proving our desired claim.
    We write out the given model A = A, aA                   A A A                 A A
                                                                                         
                                                1 , . . . , al , b , c1 , . . . , cn , s
    We know that |A| = z > l, and therefore the set

                              S , A \ aA              A
                                      
                                         1 , . . . , al

is not empty. Let us define

                                     α∗ , arg min bA (α)
                                                 
                                                      α∈S


and b∗      ,           bA (α∗ ). We construct           the smaller          SL   structure
             0
                           A0 A0 A0                A0 A0
A0 = A0 , aA
           1   , . . . , a l , b  , c1 , . . . , c n , s  , where

                                  A0 , A \ {α∗ }                                           (4)
                                      0
                                 aA    A
                                  i , ai                                                   (5)
                                     A0           A                    0
                                 b        ,b          projected on A                       (6)
                                     A0           A         ∗
                                 s        ,s −b                                            (7)
                                          0
     and we postpone defining cA
                               k for now. We observe that:

Observation 5. If A is a distinct SL model, then so is A0 .


Firstly, we prove the following claim:

Claim 7. A0 holds the sum property.

Proof. Since A holds the sum property for sA :
                         0
                       sA = sA − b∗
                            X
                          =     bA (α) − b∗
                                 α∈A
                                                               
                                          X
                             =                        bA (α) + bA (α∗ ) −b∗
                                                                 | {z }
                                     α∈A\{α∗ }
                                                                    =b∗
                                 X            0
                             =            bA (α)
                                 α∈A0

                             0                                                  0
   The definition for cA              ∗      ∗                 A    A
                        k depends on b . If b = 0 then simply ck = ck . In this
case, we prove the following:
                                                   Summing Up Smart Transitions         31

Lemma 1. For any term t, assignment ∆,
                                                 0
                                       I∆ (t) = I∆ (t)
                                           0
Proof. Since b∗ = 0, we get that sA = sA and therefore the interpretations of
A and A0 are identical — I = I 0 .

Corollary 2. Since the domain of A0 is a strict subset of the domain of A, for
any formula ξ, A  ξ ⇒ A0  ξ, and in particular A0 is also an SL model for ϕ.

In the case that b∗ > 0, we define
                         A
                    0
                         s − b∗ if cA k =s
                                            A

                 cA
                  k   ,   cA
                             + 1  if c A
                                         ≥ sA
                                              − b∗ and cA
                                                        k 6= s
                                                              A
                         kA           k
                          ck      otherwise

and the proof is more involved. We firstly make the following observations:

Observation 6. For any k ∈ [1, d],
                                                       0       0
                                cA
                                 k =s
                                     A
                                       ⇐⇒ cA
                                           k =s
                                               A


Observation 7. For any k1 , k2 ∈ [1, d],
                                                       0       0
                                cA     A      A     A
                                 k1 = ck2 ⇐⇒ ck1 = ck2

The central claim we need to prove is:
Claim 8. Let ξ be a sub-formula of ϕ,
 1. If ξ is a closed, quantifier-free formula then

                                       A  ξ ⇐⇒ A0  ξ

 2. If ξ is a quantifier-free formula with free variables x1 , . . . , xr , then for every
    α 1 , . . . , α r ∈ A0 ,

               A  ξ [α1 /x1 , . . . , αr /xr ] ⇐⇒ A0  ξ [α1 /x1 , . . . , αr /xr ]

 3. If ξ is a closed, universally quantified formula then

                                         A  ξ ⇒ A0  ξ

 4. If ξ is a universally quantified formula with free variables x1 , . . . , xr , then
    for every α1 , . . . , αr ∈ A0 ,

                 A  ξ [α1 /x1 , . . . , αr /xr ] ⇒ A0  ξ [α1 /x1 , . . . , αr /xr ]

Corollary 3. A0  ϕ.

Proof. Since ϕ is a closed, universally quantified sub-formula of itself, ] and since
it is given that A  ϕ, we get from Claim 8 that A0  ϕ.
32       Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

     In order to prove Claim 8 we firstly need to prove the following two lemmas:

Lemma 2. For any α ∈ A0 ,
                                                0             0
                             bA (α) = bA (α) < sA < sA
                       0
Proof. First, since bA is defined to be a projection of bA on a subset of its
                                            0
domain A0 ⊆ A it is obvious that bA (α) = bA (α) for any α ∈ A0 .
                  0                                                      0
   Also, since sA = sA − b∗ and we know that b∗ > 0, it is clear that sA < sA .
                                                     0         0
                                               0   A
   What remains to prove is that for anyn α∈A,b o      (α) < sA . A0 has at least
                                                          0             0
l + |ϕ| + 1 elements, and therefore A0 \ aA            A
                                          1 , . . . , al                     has at least 2 elements.
Let us denote them: α1 , α2 .
    For both of these elements,
                                     0               0
                                  bA (α1 ), bA (α2 ) > 0

since otherwise they would have been chosen as α∗ — contradicting b∗ ’s mini-
mality.
For any element α, since A0 holds the sum property,
                         0    X      0
                       sA =        bA (α0 )
                                   α0 ∈A0
                                     0                   X          0
                                 = bA (α) +                       bA (α0 )
                                                    α0 ∈A0 \{α}

     We can re-arrange and get that
                             0              0            X          0
                           bA (α) = sA −                          bA (α0 )
                                                    α0 ∈A0 \{α}

and since A0 \ {α} contains either α1 or α2 , it must be that
                                X        0
                                       bA (α0 ) > 0
                                  α0 ∈A0 \{α}

                  0          0
and therefore bA (α) < sA .

Lemma 3.                                             0
                               |ϕ| < sA < sA
                                        n 0                 o
                                                         A0
Proof. Let us examine the set S , A0 \ aA  1 , . . . , a l   . It has at least |ϕ| + 1
elements.
                     0
   For any α ∈ S, bA (α) > 0, otherwise it would have been chosen as α∗ and
we’d have b∗ = 0 — which contradicts b∗ ’s minimality.
   Therefore, on the one hand,
                       X 0
                           bA (α) ≥ |S| ≥ |ϕ| + 1 > |ϕ|
                           α∈S
                                                      Summing Up Smart Transitions          33

       And, on the other hand, since S ⊆ A0 , we know that
                           X 0          X 0              0
                               bA (α) ≤       bA (α) = sA
                               α∈S             α∈A0

                                                                            0
   And combining the two results we get that |ϕ| < sA , and since b∗ > 0,
   0
sA < sA .

Proof (Proof of Claim 8). We prove the claim using structural induction.
Step 1: ξ = t1 ≈ t2 without free variables
   ξ is a closed, quantifier-free formula, so we prove that A  ξ ⇐⇒ A0  ξ.
We consider the following cases:
Case 1.1 : t1 = t2
   Tautology.
Case 1.2 : t1 = s, t2 = numeral
       Since ξ is a sub-formula of ϕ, |ξ| ≤ |ϕ|, and therefore the numeral is less than
|ϕ|.
                         0
   However, sA , sA > |ϕ| from Lemma 3 and therefore A, A0 2 ξ.
Case 1.3 : t1 = s, t2 = ck
                                                                        0       0
   From Observation 6 we know that sA = cA
                                         k ⇐⇒ s
                                               A
                                                 = cA
                                                    k and therefore
               0
A  ξ ⇐⇒ A  ξ.
Case 1.4 : t1 = s, t2 = b(ai )
                                                                   0                    0
   From Lemma 2 we know that for any α ∈ A0 , bA (α) = bA (α) < sA < sA
                                  A0
and in particular for α = aA              0
                             i = ai , A, A 2 ξ.
Case 1.5 : t1 = ck , t2 = numeral
                  0
    If cA     A                            0
        k = ck then trivially A  ξ ⇐⇒ A  ξ.
                  A A0       A0
    Otherwise, ck , ck ≥ s . However, since ξ is a sub-formula of ϕ, the numeral
                          0
is less than |ϕ|, and sA > |ϕ|, from Lemma 3. Therefore, A, A0 2 ξ.
Case 1.6 : t1 = ck1 , t2 = ck2
   Trivial, from Observation 7.
Case 1.7 : t1 = ck , t2 = b(ai )
                  0
   If cA     A
        k = ck then from Lemma 2, A  ξ ⇐⇒ A  ξ.
                                                    0
                        0       0
   Otherwise, cA       A       A
                 k , ck ≥ s . However, from Lemma 2 we know that for any
                                        A0               A0         A0
a ∈ A (and in particular for aA
      0                                         A
                                  j ), b (a) = b (a) < s    ≤ cA
                                                               k , ck . Therefore,
A, A0 2 ξ.
Case 1.8 : t1 = ai1 , t2 = ai2
       Trivial, since the interpretation of the Address constants is identical in A,
A0 .
   Any other case is symmetrical to one of the cases above.
Step 2: ξ = t1 ≈ t2 with free variables x1 , . . . , xr
       ξ is a quantifier-free formula, so we prove that for any α1 , . . . , αr ∈ A0

                A  ξ [α1 /x1 , . . . , αr /xr ] ⇐⇒ A0  ξ [α1 /x1 , . . . , αr /xr ]
34       Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

   We consider the following cases:
Case 2.1 : t1 = t2
   Tautology.
Case 2.2 : t1 = s, t2 = b(x)
                                                         0                   0
   From Lemma 2 we know that for any α ∈ A0 , bA (α) = bA (α) < sA < sA
and in particular A, A0 2 ξ [α/x].
Case 2.3 : t1 = b(x), t2 = numeral
                                                                   0
   Trivial, since from Lemma 2, for every α ∈ A0 , bA (α) = bA (α).
Case 2.4 : t1 = b(x), t2 = ck
     Let there be α ∈ A0 , we separate into the following cases:
                0
 1. If cA    A
        k = ck :
    From Lemma 2 we get

                              A  ξ [α/x] ⇐⇒ A  b(α) ≈ ck
                                          ⇐⇒ bA (α) = cA
                                                       k
                                                 0           0
                                          ⇐⇒ bA (α) = cA
                                                       k
                                          ⇐⇒ A0  b(α) ≈ ck
                                          ⇐⇒ A0  ξ [α/x]
                          0           0   0                            0
 2. Otherwise, cA
                k ≥s
                    A
                      and cA    A                       A       A
                           k ≥ s . From Lemma 2 we get b (a) = b (a) <
     A0   A                              0
    s < s and therefore A 2 ξ [α/x] and A 2 ξ [α/x].

Case 2.5 : t1 = b(x), t2 = b(ai )
   Trivial from Lemma 2.
Case 2.6 : t1 = b(x1 ), t2 = b(x2 )
   Trivial from Lemma 2.
Case 2.7 : t1 = ai , t2 = x
     Trivial, since the interpretation of the address constants is identical in A and
A0 .
Case 2.8 : t1 = x1 , t2 = x2
   Trivially holds for any a ∈ A0 .
   Any other case is symmetrical to one of the cases above.
Step 3: ξ = ¬ζ without free variables
    Since ϕ is a universal formula we can assume it is in prenex form, and there-
fore, ζ is a closed, quantifier-free formula, shorter than ξ and from the induction
hypothesis, A  ζ ⇐⇒ A0  ζ, and therefore

                                    A  ξ ⇐⇒ A 2 ζ
                                          ⇐⇒ A0 2 ζ
                                          ⇐⇒ A0  ξ
                                                   Summing Up Smart Transitions   35

Step 4: ξ = ¬ζ with free variables x1 , . . . , xr
   Similarly to the closed formula case, ζ is a quantifier-free formula with free
variables x1 , . . . , xr and the claim holds from the induction hypothesis.
Step 5: ξ = ζ1 ∨ ζ2 without free variables
   Similarly to the negation formula case, ζ1 , ζ2 are closed, quantifier-free for-
mulas and the claim holds from the induction hypothesis.
Step 6: ξ = ζ1 ∨ ζ2 with free variables x1 , . . . , xr
   Similarly to the closed formula case, and the claim holds from the induction
hypothesis.
Step 7: ξ = ∀v.ζ without free variables
   Since ξ is a universal formula, we need to show that if A  ξ then A0  ξ
(but not vice versa).
   ζ is a universally quantified formula with (at most) one free variable x. If
A  ξ then for every α ∈ A,
                                   A  ζ [α/x]
   and in particular for any α ∈ A0 ( A.
   ζ is shorter than ξ and therefore the induction hypothesis holds:

                                        A0  ζ [α/x]

   for any α ∈ A0 , and therefore A0  ξ.
Step 8: ξ = ∀v.ζ with free variables x1 , . . . , xr
   Let there be α1 , . . . , αr ∈ A0 . If

                                A  ξ [α1 /x1 , . . . , αr /xr ]

   then for every α ∈ A,

                             A  ζ [α/x, α1 /x1 , . . . , αr /xr ]

   and in particular for every α ∈ A0 ( A. From the induction hypothesis for ζ
we get:
                         A0  ζ [α/x, α1 /x1 , . . . , αr /xr ]
   which is true for any a ∈ A0 , and therefore,

                                A0  ξ [α1 /x1 , . . . , αr /xr ]

                                   Q.E.D. Theorem 2.


Presburger Reduction Proof

Defining the Transformations The transformation of formulas from SL to
PA works by explicitly writing out sums as additions and universal quantifiers
as conjunctions. Since we’re dealing with a fragment of SL that has some bound
36        Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

function κ(·), we know that for given formula ϕ, there is a model with at most
κ(|ϕ|) elements of Address sort.
   Moreover, we use κ̃ , max {κ(|ϕ|), l} as the upper bound (where l is the
amount of Address constants). Since we’re looking for distinct models, it is
obvious that we need at least l distinct elements.
   For each balance function b1j we have κ̃ constants b1,j , . . . , bκ̃,j .
   In addition we have κ̃ indicator constants a1 , . . . , aκ̃ , to mark if an Address
element is ”active”. An inactive element has all zero balances, and is skipped
over in universal quantifiers.
   Any Address constant ai or Address variable x is handled in two ways,
depending on the context they appear in:

 – If they are compared, we replace the comparison with > or ⊥; we know
   statically if the comparison holds, since the Address constants are distinct
   and every universal quantifier is written out as a conjunction.
 – Otherwise, they must be used in some balance function b1j , and then they
   are substituted with the corresponding bi,j or bx,j (which will be determined
   once the universal quantifiers are unrolled).

     The integral constants c1 , . . . , cd are simply copied over.
     In summary:

Definition 12 (Corresponding Presburger Vocabulary). Given the SL
vocabulary Σ l,m,d and a bound κ̃ ≥ l, we define the corresponding Presburger
vocabulary as
  l,m,d
          = Pres(Σ l,m,d , κ̃) , a1 , . . . , aκ̃ , b1,1 , . . . , bκ̃,m , c1 , . . . , cd , 0, 1, +2 , ≤2 .
                                                                                                          
ΣPres(κ̃)

     Firstly, we define the simpler auxiliary formula η(ϕ) in three parts:
Definition 13. We require that inactive Address elements have zero balances
—                                                   
                         ^κ̃               ^m
                η1 (ϕ) =     (ai ≈ 0) →     bi,j ≈ 0
                                     i=1                        j=1


Definition 14. And that elements referred by Address constants be active —
                                                      l
                                                      ^
                                           η2 (ϕ) =         ai 6≈ 0
                                                      i=1

Definition 15. Finally, we require that the active elements are a continuous
sequence starting at 1. Or, put differently, once an indicator is zero, all indicators
following it are also zero:
                                κ̃
                                   "              κ̃
                                                            !#
                               ^                 ^
                      η3 (ϕ) =       ai ≈ 0 →        ai0 ≈ 0
                                       i=1                     i0 =i
                                                 Summing Up Smart Transitions   37

The complete auxiliary formula is then η(ϕ) = η1 (ϕ) ∧ η2 (ϕ) ∧ η3 (ϕ).
   In order to define τ (ϕ), we firstly define the transformation for terms, and
then build up the complete transformation, using several substitutions:

Definition 16. We define the terms transformation inductively, and we sub-
stitute balances and Address terms (constants or variables) with placeholders
(marked with *), which are further substituted:
                      ∗
                      ai                      if t = ai
                      x∗
                     
                                               if t = x for some free variable
                     
                     
            τ0 (t) ,   b1,j +   · · · + b κ̃,j if t = sj
                        ∗
                       b  (τ  (t   ))          if t = bj (t1 ) where t1 ∈ {ai , x}
                     
                      j 0 1
                     
                     
                       τ0 (t1 ) + τ0 (t2 ) if t = t1 + t2
                     

Definition 17. Next we define the transformation for formulas, replacing only
variable placeholders:
                      
                      
                       τ0 (t1 ) ≈ τ0 (t2 )                       if ξ = t1 ≈ t2
                       τ0 (t1 ) ≤ τ0 (t2 )                       if ξ = t1 ≤ t2
                      
                      
              τ1 (ξ) , ¬τ1 (ζ)                                    if ξ = ¬ζ
                      
                      
                       τ1 (ζ 1 ) ∧  τ1 (ζ2 )                     if ξ = ζ1 ∧ ζ2
                       Vκ̃
                      
                                                        ∗    ∗
                          i=1   (a i ≈   0 ∨  τ 1 (ζ) [ai /x   ]) if ξ = ∀x.ζ

We can see that for any formula ξ containing arbitrary terms, τ1 (ξ) only has a∗i
and b∗j placeholders (but no x∗ ones).

Definition 18. Now we define a substitution σ1 that removes Address compar-
isons by evaluating them:

                          σ1 , [>/ (a∗i ≈ a∗i )] [⊥/ (a∗i ≈ a∗i0 )]

where i, i0 ∈ [1, κ̃].

Note 1. We first replace comparisons where a∗i ≈ a∗i , which is equivalent to
true (>). Then any remaining comparison must be where i 6= i0 , and therefore
equivalent to false (⊥).

Definition 19. Finally, we’re left with placeholders inside balance functions,
which we substitute by the corresponding balance constant:

                               σ2 , bi,j /b∗j (a∗i )
                                                   

where i ∈ [1, κ̃], j ∈ [1, m].

Definition 20. The complete transformation is then:

                                   τ (ϕ) , τ1 (ϕ)σ1 σ2

Given the above definitions, let us recall the Presburger Reduction Theorem:
38       Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

Theorem 3 (Presburger Reduction). An SL formula ϕ has a distinct,
SL model with small Address space iff τ (ϕ) ∧ η(ϕ) has a Standard Model of
Arithmetic.                                                             t
                                                                        u
Proof of Theorem 3
We first define congruence between SL structures and structures over the corre-
sponding Presburger vocabulary, and we prove a general theorem about them.
We use that congruence theorem to prove that a formula ϕ has a distinct SL
model with small Address space iff ϕ0 has a Standard Model of Arithmetic.

Part 1: Congruence Lemmas
                                               l,m,d
Definition 21. Given an SL vocabulary
                                     l,m,d Σ       , a bound κ̃ ≥ l and a formula ϕ
over Σ l,m,d
             . Then A ∈ STRUCT Σ              and A0 ∈ STRUCT Pres(Σ l,m,d , κ̃)
are said to be congruent if the following conditions hold:
1. A holds the sum property.
2. A0 satisfies η(ϕ).
3. z , |A| ≤ κ̃, and we write out A = {α1 , . . . , αz }.
4. For any i ∈ [1, l], aA
                        i = αi .                 0
5. For any j ∈ [1, m], for any i ∈ [1, z], bA            A
                                              i,j = bj (αi ), and for any i > z,
      0
   bA
    i,j = 0.
                          0
                                                       A0
6. For any i ∈ [1, z], aAi > 0 and for any i > z, ai = 0.
7. A is distinct, and in particular l ≤ z.
Lemma 4. Let A, A0 be two congruent structures for SL vocabulary Σ, bound
κ̃ and formula ϕ. For any ground term t of sort Nat over Σ,
                                     I 0 (τ0 (t)σ2 ) = I(t)
Proof. We prove the lemma using structural induction over all possible ground
terms:
Step 1.1: t = sj for any j ∈ [1, m]
   From Congruence Condition 1 A holds the sum property, and therefore:
                                           X                 z
                                                             X
                        I(sj ) = sA
                                  j =            bA
                                                  j (α) =          bA
                                                                    j (αi )
                                           α∈A               i=1
                                                                      0
From Congruence Condition 5, for any i ∈ [1, z], bA             A
                                                         i,j = bj (αi ), and for any
                    0
i ∈ [z + 1, κ̃], bA
                  i,j = 0, therefore we can write the sum above as

                                                      κ̃
                                                      X        0
                                   I(sj ) = · · · =         bA
                                                             i,j
                                                      i=1

     From the definition of τ0 we get:
                                                                           κ̃
                                                                           X        0
                 I 0 (τ0 (sj )σ2 ) = I 0 ([b1,j + · · · + bκ̃,j ] σ2 ) =         bA
                                                                                  i,j
                                                                           i=1
                                                   Summing Up Smart Transitions   39

Since we have no placeholders, σ2 has no effect, and we get the same expression
as for I(t).
Step 1.2: t = bj (ai ) where i ∈ [1, l], j ∈ [1, m]
   From Congruence Condition 4, aA
                                 i = αi , and we get:

                                      I(t) = bA
                                              j (αi )

   From the definition of τ0 and σ2 we get:

                          τ0 (t)σ2 = b∗j (a∗i ) σ2 = bi,j
                                              

    And therefore, since A is distinct, i ≤ l ≤ z, and from Congruence Condi-
tion 5,                                                  0
                      I 0 (τ0 (t)σ2 ) = I 0 (bi,j ) = bA      A
                                                       i,j = bj (αi )

Step 1.3: t = t1 + t2
   Follows from the induction hypothesis for t1 and t2 (since + is interpreted in
the same way in A and A0 ).
Lemma 5. Let A, A0 be two congruent structures for SL vocabulary Σ, bound
κ̃ and formula ϕ. For any term t with at most r free variables x1 , . . . , xr , for
any indices i1 , . . . , ir ∈ [1, z], for any assignment ∆ we define

                             ∆0 = ∆ [αi1 /x1 , . . . , αir /xr ]

   and the following holds:

                    I∆0 (t) = I 0 τ0 (t) a∗i1 /x∗1 , . . . , a∗ir /x∗r σ2
                                                                      

Proof. We prove the lemma using structural induction over all possible terms
with free variables:
Step 1.4: t = bj (x)
   For any i ∈ [1, z],

                          I∆0 (t) = I(bj ) (∆0 (x)) = bA
                                                       j (αi )

   By definition, τ0 (t) = b∗j (x∗ ), and therefore

                        I 0 (τ0 (t) [a∗i /x∗ ] σ2 ) = I 0 b∗j (a∗i )σ2
                                                                         

                                                  = I 0 (bi,j )
                                                         0
                                                  = bA
                                                     i,j

                                                  = bA
                                                     j (αi )

since i ∈ [1, z].
Step 1.5: t = t1 + t2
    Either t1 or t2 has free variables, and let us assume w.l.o.g. that t1 does.
Therefore, t2 is either a ground term, or also has free variables. If t2 has no free
variables, the substitution of free variables wouldn’t affect it.
40       Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

      In both cases, from the induction hypothesis and from Lemma 4, for any
i1 , . . . , ir ∈ [1, z],

                          I∆0 (tv ) = I 0 (τ0 (tv ) a∗i1 /x∗1 , . . . , a∗ir /x∗r )
                                                                                

where v ∈ {1, 2}, and we get desired equality for t as well.

Lemma 6. Let A, A0 be two congruent structures for SL vocabulary Σ, bound
κ̃ and formula ϕ. Let ξ be a sub-formula of ϕ, therefore:
 1. If ξ is a closed formula, then A0  τ (ξ) ⇐⇒ A  ξ.
 2. If ξ is a formula with free variables x1 , . . . , xr then for any i1 , . . . , ir ∈ [1, z]:

                         A0  τ1 (ξ) a∗i1 /x∗1 , . . . , a∗ir /x∗r σ1 σ2
                                                                 

                                 ⇐⇒ A  ξ [αi1 /x1 , . . . , αir /xr ]

Proof. Let us separate into the following steps:
Step 1.6: ξ = t1 ≈ t2 without free variables, where t1 , t2 are of Address sort
     Since t1 , t2 are Addresses, there are two indices i1 , i2 ∈ [1, l] such that t1 =
ai1 , t2 = ai2 . From Congruence Condition 7, A is distinct and therefore

                                    A  ξ ⇐⇒ i1 = i2 .

     As for τ (ξ),

                              τ (ξ) = (τ0 (t1 ) ≈ τ0 (t2 )) σ1 σ2
                                    = a∗i1 ≈ a∗i2 σ1
                                                  
                                      
                                        > if i1 = i2
                                    =
                                        ⊥ otherwise

   Which means that A0  τ (ξ) ⇐⇒ i1 = i2 ⇐⇒ A  ξ.
Step 1.7: ξ = t1 ≈ t2 without free variables, where t1 , t2 are of sort Nat
   In this case, σ1 would not change the formula and we can apply σ2 to each
term:
                           τ (ξ) = τ0 (t1 )σ2 ≈ τ0 (t2 )σ2
     Since t1 , t2 are of sort Nat, from Lemma 4 we get that

                      A0  τ (ξ) ⇐⇒ I 0 (τ0 (t1 )σ2 ) = I 0 (τ0 (t2 )σ2 )
                                  ⇐⇒ I(t1 ) = I(t2 )                              (Lemma 4)
                                  ⇐⇒ A  t1 ≈ t2 = ξ

Step 1.8: ξ = t1 ≈ t2 with free variables x1 , . . . , xr , where t1 , t2 are of Address
sort
    Let us first define σ = [αi1 /x1 , . . . , αir /xr ], σ 0 = a∗i1 /x∗1 , . . . , a∗ir /x∗r .
                                                                                            

    If t1 , t2 both have free variables then we can write them as t1 = x1 , t2 = x2
and after substituting σ we get that
                                                    Summing Up Smart Transitions            41



                                       ξσ = αi1 ≈ αi2 .
    Therefore, A  ξσ ⇐⇒ i1 = i2 .
    As for A0 , we get
                             τ1 (ξ)σσ1 σ2 = (x∗1 ≈ x∗2 ) σ 0 σ1 σ2
                                          = a∗i1 ≈ a∗i2 σ1 σ2
                                                         

                                          = a∗i1 ≈ a∗i2 σ1
                                                         
                                            
                                              > if i1 = i2
                                          =
                                              ⊥ otherwise
    And we get that A0  τ1 (ξ)σ 0 σ1 σ2 ⇐⇒ i1 = i2 ⇐⇒ A  ξσ.
Step 1.9: ξ = t1 ≈ t2 with free variables x1 , . . . , xr , where t1 , t2 are of sort Nat
    Similarly     to the case       above, we define σ = [αi1 /x1 , . . . , αir /xr ] and also
σ 0 = a∗i1 /x∗1 , . . . , a∗ir /x∗r . For any assignment ∆, we define
      

                                           ∆0 = ∆σ
    Since t1 , t2 are of sort Nat, σ1 has no effect, and from Lemma 5,

                       A0  τ1 (ξ)σ 0 σ1 σ2
                            ⇐⇒ A0  [τ0 (t1 ) ≈ τ0 (t2 )] σ 0 σ2
                            ⇐⇒ I 0 (τ0 (t1 )σ 0 σ2 ) = I 0 (τ0 (t2 )σ 0 σ2 )
                            ⇐⇒ I∆0 (t1 σ) = I∆0 (t2 σ)                             (Lemma 5)
                            ⇐⇒ A  ξσ
Step 1.10: ξ = ¬ζ without free variables
   Follows from the induction hypothesis for ζ:
                               A0  τ (ξ) ⇐⇒ A0  ¬τ (ζ)
                                              ⇐⇒ A0 2 τ (ζ)
                                              ⇐⇒ A 2 ζ
                                              ⇐⇒ A  ¬ζ
                                              ⇐⇒ A  ξ
Step 1.11: ξ = ¬ζ with free variables x1 , . . . , xr
   Follows from the induction hypothesis for ζ, for any i1 , . . . , ir ∈ [1, z]:
           A0  τ1 (¬ζ) a∗i1 /x∗1 , . . . , a∗ir /x∗r σ1 σ2
                                                    

               ⇐⇒ A0  ¬τ1 (ζ) a∗i1 /x∗1 , . . . , a∗ir /x∗r σ1 σ2
                                                             

               ⇐⇒ A0 2 τ1 (ζ) a∗i1 /x∗1 , . . . , a∗ir /x∗r σ1 σ2
                                                           

                 ⇐⇒ A 2 ζ [αi1 /x1 , . . . , αir /xr ]                  (Induction hypothesis)
                 ⇐⇒ A  ¬ζ [αi1 /x1 , . . . , αir /xr ]
                 ⇐⇒ A  ξ [αi1 /x1 , . . . , αir /xr ]
42      Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

Step 1.12: ξ = ζ1 ∨ ζ2 without free variables
   Follows from the induction hypothesis for ζ1 and ζ2 :

                       A0  τ (ξ) ⇐⇒ A0  τ (ζ1 ) ∨ τ (ζ2 )
                                     ⇐⇒ A0  τ (ζ1 ) or A0  τ (ζ2 )
                                     ⇐⇒ A  ζ1 or A  ζ2
                                     ⇐⇒ A  ζ1 ∨ ζ2
                                     ⇐⇒ A  ξ

Step 1.13: ξ = ζ1 ∨ ζ2 with free variables x1 , . . . , xr
   Follows from the induction hypothesis for ζ1 and ζ2 , similar to the no free
variables case above, since τ1 (ζ1 ∨ ζ2 ) = τ1 (ζ1 ) ∨ τ1 (ζ2 ).
Step 1.14: ξ = ∀x.ζ without free variables
             0
     Since aA
            i = 0 ⇐⇒ i > z we get the following:

                             κ̃
                             ^
     A0  τ (ξ) ⇐⇒ A0             (ai ≈ 0 ∨ τ1 (ζ) [a∗i /x∗ ]) σ1 σ2
                             i=1
                             ^z
                 ⇐⇒ A0            τ1 (ζ) [a∗i /x∗ ] σ1 σ2
                             i=1
                 ⇐⇒ A0  τ1 (ζ) [a∗i /x∗ ] σ1 σ2 for all i ∈ [1, z]
                 ⇐⇒ A  ζ [αi /x] for all i ∈ [1, z]            (Induction hypothesis for ζ)
                 ⇐⇒ A  ∀x.ζ = ξ                      (The set A is covered by α1 , . . . , αz )

Step 1.15: ξ = ∀x.ζ with free variables x1 , . . . , xr
   Similar to the case above, using the induction hypothesis for ζ as a formula
with free variables x, x1 , . . . , xr .

Part 2: Proof of Theorem 3 (⇒): If ϕ has a distinct SL model with
small Address space, then ϕ0 has a Standard Model of Arithmetic
Let there be a distinct SL model for ϕ with small Address space:

            A = A, aA              A A               A A               A A               A
                                                                                           
                      1 , . . . , al , b1 , . . . , bm , c1 , . . . , cn , s1 , . . . , sm .

    We can represent its Addresses set as A = {α1 , . . . , αz } where z = |A|, and
for every i ∈ [1, l], aA
                       i = αi since A is distinct. Combined with the fact that A
has small Address space we know that z ≤ κ̃.
    We define A0 , the Standard Model of Arithmetic for ϕ0 , as follows:
                          0                                                            
                                         A0 A0                 A0     A0             A0
                  A0 = aA 1  , . . . , a κ̃ , b1,1 , . . . , b     ,
                                                               κ̃,m 1c   , . . . , c n


where the indicators are                    
                                       0        1 if i ≤ z
                                    aA
                                     i =                    ;
                                                0 otherwise
                                                      Summing Up Smart Transitions   43

the balances are                       A
                                0      bj (αi ) if i ≤ z
                             bA
                              i,j =                       ;
                                       0        otherwise
                                      0
and the natural constants are cA    A
                               k = ck .

Claim. The structure A0 satisfies η(ϕ).

Proof. We show that A0 satisfies η1 (ϕ), η2 (ϕ) and η3 (ϕ):
Step 2.1: A0 satisfies η1 (ϕ)
      We need to show that for each i ∈ [1, κ̃],
                                                       
                                              ^m
                       A0  (ai ≈ 0) →         bi,j ≈ 0 .
                                                      j=1

                                                  0                0
I.e. for each i ∈ [1, κ̃] and j ∈ [1, m], if aA            A
                                              i = 0, then bi,j = 0.
                        0
                                                                          A0
    By definition, aA i = 0 ⇐⇒ i > z, in which case, for any j ∈ [1, m], bi,j = 0,
as required.
Step 2.2: A0 satisfies η2 (ϕ)
      We need to show that for each i ∈ [1, l],

                                          A0  ai 6≈ 0,
         0
i.e. aA
      i 6= 0.
     Since A is a distinct SL model, it has at least l addresses: l ≤ z. By definition,
                       0
for any i ∈ [1, z], aA
                     i = 1 > 0, in particular for any i ∈ [1, l] ⊆ [1, z].
Step 2.3: A0 satisfies η3 (ϕ)
                                                               0
    We need to show that for each i ∈ [1, κ̃], if aAi   = 0, then for any i0 > i,
  0
 A
ai0 = 0.
                                             0
    Let there be some index i such that aA i = 0, therefore, by definition, i > z.
                                                          0
For any i0 > i it also holds that i0 > z and therefore aA
                                                        i0 = 0.

Claim. The structure A0 satisfies τ (ϕ).

Proof. We show that A and A0 are congruent, and since A  ϕ, from Lemma 6,
A0  τ (ϕ):

 1. A is an SL model of ϕ, therefore it holds the sum property.
 2. A0 satisfies η(ϕ) from Appendix A.
 3. z = |A| ≤ κ̃ as explained above.
 4. For any i ∈ [1, l], aA
                         i = αi by definition.
                                                               0
 5. By construction of A0 , for any j ∈ [1, m], i ∈ [1, z], bA      A
                                                             i,j = bj (αi ) and for any
             A0
    i > z, bi,j = 0.
                                                     0
 6. By construction of A0 , for any i ∈ [1, z], aA i   = 1 > 0, and for any i > z,
        0
    aAi   = 0.
44       Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

 7. A is given to be distinct.

Corollary 4. The structure A0 is a Standard Model of Arithmetic for ϕ0 =
τ (ϕ) ∧ η(ϕ).

Part 3: Proof of Theorem 3 (⇐): If ϕ0 has a Standard Model of
Arithmetic, then ϕ has a distinct SL model with small Address space
          0                                                             
                          A0 A0                 A0     A0             A0
Let A0 = aA 1 , . . . , a κ̃ , b1,1 , . . . , b     ,
                                                κ̃,m 1c   , . . . , c n    be a Standard Model of
Arithmetic for ϕ0 . Since A0  η3 (ϕ), we know that there exists some maxi-
                                    0
                                                                           A0
mal index z ≤ κ̃ such that aA    z 6= 0 and for any i > z, ai = 0. Since A  η1 (ϕ)
                                                                                              0

we know that z ≥ l.
   We construct an SL model A for ϕ as follows:

            A = A, aA                 A A             A A               A A               A
                                                                                            
                       1 , . . . , al , b1 , . . . , bm , c1 , . . . , cn , s1 , . . . , sm

where the Addresses set is
                                          A = [1, z];
the Address constants are
                                            aA
                                             i =i

for any i ∈ [1, l]; the balances are
                                                      0
                                         bA        A
                                          j (i) = bi,j

                                                                         0
for any i ∈ A, j ∈ [1, m]; the natural constants are cA    A
                                                      k = ck and the sums are
defined as                             X
                                sAj =     bA
                                           j (α).
                                             α∈A

We show that A, A0 are congruent:
 1. By construction, A holds the sum property.
 2. It is given that A0 satisfies η(ϕ).
 3. We define A to be the set [1, z], and therefore |A| ≤ κ̃.
 4. aA
     i = αi as defined above.
                                                                A0
 5. By construction, for any j ∈ [1.m], i ∈ [1, z], bA
                                                     j (αi ) = bi,j and z was chosen
                                  0
    such that for any i > z, bA i,j = 0.
                                                  0
                                                                             A0
 6. z was chosen such that for any i ∈ [1, z], aA
                                                i > 0 and for any i > z, ai = 0.
 7. A is distinct by construction.

   Given that A0  ϕ0 , we know in particular that A0  τ (ϕ), and from Lemma 6,
A  ϕ as a many-sorted, first-order formula. Since A holds the sum property,
A SL ϕ. In addition, by construction |A| = z ≤ κ̃. Therefore, A is a distinct
SL model for ϕ with small Address space.
                                    Q.E.D. Theorem 3.
                                            Summing Up Smart Transitions        45

B     Proofs for Encodings

B.1    Soundness of mint1

For readability reasons, the theorem is stated again.

Theorem 7 (Soundness of mint1 (a, c)). Let c ∈ Coin, a ∈ Address such
that mint1 (a, c). Consider balance functions old-bal, new-bal : Address → N,
non-negative integer constants old-sum, new-sum, unary predicates old-active,
new-active ⊆ Coin and binary predicates old-has-coin, new-has-coin ⊆
Address × Coin such that

              |old-active| = old-sum , |new-active| = new-sum,

and for every address a0 , we have

             old-bal(a0 ) = |{c0 ∈ Coin | (a0 , c0 ) ∈ old-has-coin}| ,
             new-bal(a0 ) = |{c0 ∈ Coin | (a0 , c0 ) ∈ new-has-coin}| .

    Then, new-sum = old-sum + 1, new-bal(a) = old-bal(a) + 1. Moreover, for
all other addresses a0 6= a, it holds new-bal(a0 ) = old-bal(a0 ).        t
                                                                          u

    Now the proof is as follows.

Proof. To show that new-sum = old-sum + 1, we consider the subformula (M3)
of mint1 (a, c). It follows that old-active\{c} = new-active\{c}. Now using
(M1), we get old-active = old-active\{c} and (new-active\{c}) ∪ {c} =
new-active. Thus, old-active ∪˙            {c} = new-active and hence
|old-active| + 1 = |old-active ∪˙ {c}| = |new-active| which implies
new-sum = old-sum + 1.
    Similar reasoning works to show new-bal(a) = old-bal(a) + 1. From (M4)
it follows

      {d | (a, d) ∈ old-has-coin}\{c} = {d | (a, d) ∈ new-has-coin}\{c} .

Now using (M2) we get

      {d | (a, d) ∈ old-has-coin} = {d | (a, d) ∈ old-has-coin}\{c}       and
      {d | (a, d) ∈ new-has-coin}\{c} ∪ {c} = {d | (a, d) ∈ new-has-coin} .

As before, we have

        {d | (a, d) ∈ old-has-coin} ∪˙ {c} = {d | (a, d) ∈ new-has-coin} ,

which implies new-bal(a) = old-bal(a) + 1.
    Finally, new-bal(b) = old-bal(b) for b 6= a follows from (M4), since it implies
{d | (b, d) ∈ old-has-coin} = {d | (b, d) ∈ new-has-coin}.                       t
                                                                                 u
46      Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

B.2   Soundness of mintn
To define the smart transition mintn we need one pair of predicates for every
time step. Thus we have an additional ”parameter” i, the i-th time step, in
active and has-coin instead of using the prefixes old-- and new--. Other than
that the definition and the soundness result is analog to the setting of mint1 .
Definition 22 (Transition mintn (a)). Let a ∈ Address. Then, the transition
mintn (a) activates n coins and deposits them into address a, one coin c in each
time step.
1. The coin c was inactive before and is active now:
                             ¬active(c, i) ∧ active(c, i + 1) .                (N1)
2. The address a owns the new coin c:
           has-coin(a, c, i + 1) ∧ ∀a0 : Address. ¬has-coin(a0 , c, i) .       (N2)
3. Everything else stays the same:
              ∀c0 : Coin. ∀a0 : Address. (c0 6≈ c ∨ a0 6≈ a) →                 (N3)
                               0                      0
                  (active(c , i + 1) ↔ active(c , i)) ∧
                  (has-coin(a0 , c0 , i + 1) ↔ has-coin(a0 , c0 , i + 1)) .
                                                                         

The transition mintn (a) is defined as ∀i : Nat. ∃c : Coin. (N1) ∧ (N2) ∧ (N3).
The soundness result we get is similar to Theorem 7 but extended by the new
parameter.
Theorem 10 (Soundness of mintn (a)). Let a ∈ Address such that mintn (a).
Consider a balance function bal : Address × N → N, a summation function
sum : N → N+ , a binary predicate active ⊆ Coin × N and a ternary predicate
has-coin ⊆ Address × Coin × N such that for every i ∈ N
                                   |active(., i)| = sum(i)
                         0
and for every address a and i ∈ N, we have
                bal(a0 , i) = |{c0 ∈ Coin | (a0 , c0 , i) ∈ has-coin}| .
   Then for an arbitrary n ∈ Nat, sum(n) = sum(0) + n, bal(a, n) = bal(a, 0) +
n. Moreover, for all other addresses a0 6= a, it holds bal(a0 , n) = bal(a0 , 0).
Proof. We prove Theorem 10 by induction over n ∈ N. The base case n = 0
is trivially satisfied. For the induction step, we get the induction hypothesis
sum(n) = sum(0) + n, bal(a, n) = bal(a, 0) + n, ∀a0 6= a. bal(a0 , n) = bal(a0 , 0).
By defining old-sum , sum(n), new-sum , sum(n + 1) and analogously for
active, bal and has-coin, all the preconditions of Theorem 7 hold. Therefore,
we get sum(n+1) = sum(n)+1, bal(a, n+1) = bal(a, n)+1, ∀a0 6= a. bal(a0 , n+
1) = bal(a, n), by applying Theorem 7. Together with the induction hypothesis
this yields sum(n + 1) = sum(0) + n + 1, bal(a, n + 1) = bal(a, 0) + n + 1,
∀a0 6= a. bal(a0 , n + 1) = bal(a0 , 0) and thus concludes the induction proof. t u
                                            Summing Up Smart Transitions        47

B.3   Soundness and Completeness relative to f

In order to establish a proof of Theorem 8, some formal definitions of the in
the paper informally explained concepts have to be stated first. The exclusion
of certain elements of F is based on an equivalence relation ∼.
    We first formally define ∼:

Definition 23 (Relation ∼ ). Let the pairs p1 = (has-coin 1 , active 1 ) ∈ F
and p2 = (has-coin 2 , active 2 ) ∈ F. Then p1 ∼ p2 iff

1. |active 1 | = |active 2 | ,
2. |{c ∈ Coin | has-coin 1 (a, c)}| = |{c ∈ Coin | has-coin 2 (a, c)}|, for all a ∈
   Address,
3. p1 violates (I2) in V≤ cases and p2 violates (I2) also V≤ times;
4. p1 does not satisfy (I1) and (I3) in all together V≥ cases, which is also the
   number of times p2 violates (I1) and (I3).

   To properly prove that ∼ is an equivalence relation, we have to define V≤
and V≥ first.

Definition 24. Given a pair (active, has-coin) ∈ F. For an address a, we
define Ca , {c ∈ Coin | has-coin(a, c)}. Further, we define three types of error
coins:

1. MInact , {c ∈ Coin | ¬active(c) ∧ ∃a. c ∈ Ca },
2. MLeast , {c ∈ Coin | active(c) ∧ ∀a. c ∈/ Ca } and
3. MMost , {c ∈ Coin | ∃a, b. a 6≈ b ∧ c ∈ Ca ∧ c ∈ Cb }

and one type of error pairs MPairs , {(a, c) | c ∈ Ca ∧ ∃b. a 6≈ b ∧ c ∈ Cb } to
refine the number of mistakes caused by the violation of (I3).
The number of violations of (I2) is now V≤ , |MLeast |. and the number of
violations of (I1) and (I3) is defined as V≥ , |MInact | + |MPairs | − |MMost |.

Lemma 7. The relation ∼ is an equivalence relation on F.

Proof. – Reflexivity of ∼.
   Let (has-coin, active) ∈ F, then clearly |active| = |active|, for all a we
   have |Ca | = |Ca | and also V≤ = V≤ , V≥ = V≥ . Hence (has-coin, active) ∼
   (has-coin, active).
 – Symmetry of ∼.
   Let p1 , p2 ∈ F such that p1 ∼ p2 , then due to symmetry of = also p2 ∼ p1
   holds.
 – Transitivity of ∼.
   Let p1 , p2 , p3 ∈ F, such that p1 ∼ p2 and p2 ∼ p3 then due to the transitivity
   of = also p1 ∼ p3 holds.                                                       t
                                                                                  u

   The translation function f can now be defined as a function that assigns
every pair (bal, sum) a class from F/∼ .
48      Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

Definition 25 (Translation Function f ). The function f : NAddress × N →
F/∼ , (bal, sum) 7→ [(has-coin, active)]∼ , is defined to satisfy the following
conditions for an arbitrary (has-coin, active) ∈ [(has-coin, active)]∼ .
1. sum = |active| .
2. For every a ∈ Address it holds bal(a) = |{c ∈ Coin | has-coin(a, c)}|.
3. At least one of V≤ = 0 and V≥ = 0 holds.

    The function f is well-defined and injective, ensuring soundness and com-
pleteness of our SL encodings relative to f .

Theorem 8 (Relative Completeness of SL Encoding). Let (bal, sum) ∈
NAddress × N and let (has-coin, active) ∈ f (bal, sum) be arbitrary. Then,
                X
        sum =          bal(a)   ⇐⇒     inv (has-coin, active) .        t
                                                                       u
               a∈Address

Proof. The proof is organized in 4 steps. The first step provides a technicality
that is need for the steps 2 and 3 and finally in the last step the claim is proven.
 1. Consider any pair (has-coin, active) ∈ F with V≤ = V≥ = 0. Then, since
    there
    S     are no coins nor addresses violating the invariants here,
                                                                 P we thus have
     Sa∈Address Ca = active  and all the C a are disjoint. Thus,  a∈Address |Ca | =
    | a∈Address Ca | = |active|.
 2. Now we only assume V≥ = 0. Consider

              MLeast = {c ∈ Coin | active(c) ∧ ∀a. c ∈
                                                     / Ca } ⊆ active .

     Then the pair p0 = (has-coin, active\MLeast ) satisfies V≤0 = V≥0 = 0, be-
     cause all the coins were not active originally are active now and we did not
     change the any of the other mistake sets. From the first step we now get
                              X
                                    |Ca0 | = |active\MLeast |
                             a∈Address

     and therefore           X
                                       |Ca | = |active| + V≥ − V≤ .
                           a∈Address

 3. Similarly to the second step we now only assume V≤ = 0. By definition it
    holds that MInact ∩ active = ∅, MPairs ⊆ has-coin and MMost ⊆ active ∪
    MInact . We now consider the pair

                 p00 = (has-coin\MPairs , (active ∪ MInact )\MMost ) .

     Clearly, there is not any coin assigned to two different addresses in p00 . How-
     ever all the coins that were in two different addresses before are now not
     assigned to any address, this is why these coins have to be removed from
     active ∪ MInact . Also there are no coins that are active without belonging
     to any address. Further, all active coins still are assigned to an address as
                                                 Summing Up Smart Transitions   49

    the problematic ones have been removed. Hence, V≤00 = V≥00 = 0. Now, we can
    again apply the result of the first step to get
                X
                      |Ca | − |MPairs | = |active| + |MInact | − |MMost |
               a∈Address

    and thus                 X
                                       |Ca | = |active| + V≥ − V≤ .
                           a∈Address

4. Using the results of the previous two steps we can now prove the theorem. Let
   (bal, sum) ∈ NAddress × N and (has-coin,
                                          P active) ∈ f (bal, sum), then V≤ =
   0 or V≥ = 0. In both cases it follows a∈Address
                                             P        |Ca | = |active| + V≥ − V≤
                 by definition of f it holds a∈Address bal(a) = sum + V≥ − V≤ .
   and therefore P
   Assume now a∈Address bal(a) = sum. It follows V≥ − V≤ = 0 and since we
   know that one of these values has to be zero by definition of f it holds V≤ =
   V≥ = 0. But this statement is equivalent to inv (has-coin, active). For the
   other direction
              P assume inv (has-coin, active), this implies V≤ = V≥ = 0
   and hence a∈Address bal(A) = sum. This conlcudes the proof.
                                                                               t
                                                                               u

    From Theorem 8, also Theorem 6 follows immediately by stating the prop-
erties of the function f .


B.4   Soundness of Explicit SL Encodings

Theorem 9 (Soundness of Explicit SL Encodings). Let there be a pair
(bal, sum) ∈ NAddress × N, a pair (has-coin, active) ∈ F, and functions count :
Coin → N+ and idx : Address × Coin → N+ .
   Given that count is bijective, idx(a, .) : Coin → N+ is bijective for every a ∈
Address, and that (Ax1), (Ax2) and inv (has-coin, active) hold, then, sum =
|active| and bal(a) = |{c ∈ CoinP: has-coin(a, c)}|, for every a ∈ Address.
   In particular, we have sum = a∈Address bal(a).                                t
                                                                                 u

Proof. Consider (bal, sum), (has-coin, active) as in the theorem. Then by
property (Ax1) and the codomain of count we have active = {c ∈ Coin |
count(c) ∈ [1, sum]}. Since count is bijective, it holds

               |active| = |{c ∈ Coin | count(c) ∈ [1, sum]}| = sum .

Similarly, by (Ax2) and the codomain of idx(a, .) we know Ca = {c ∈ Coin |
idx(a, c) ∈ [1, bal(a)]}. As idx(a, .) is bijective as well it follows

               |Ca | = |{c ∈ Coin | idx(a, c) ∈ [1, bal(a)]}| = bal(a) .

Hence
P       (has-coin, active) ∈ f (bal, sum) and by Theorem 8, we get
  a∈Address bal(a) = sum, since inv (has-coin, active).         t
                                                                u
50     Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

B.5   No Loss of Generality: Restricting idx and count
We want to prove that we do not lose any generality when considering mutual
count and idx functions for the old- and the new-world. In order to do so we
need the following preliminary lemmas.
Lemma
P          8. Given two pairs hx , (x-bal, x-sum), hy , (y-bal, y-sum) with
   a∈Address z-bal(A) = z-sum, for z ∈ {old, new} and x-sum ≤ y-sum. Further,
let px = (x-has-coin, x-active) ∈ f (hx ).
Then there exists py = (y-has-coin, y-active) ∈ f (hy ) satisfying the following
properties:
1. x-active ⊆ y-active.
2. x-bal(a) ≤ y-bal(a) ⇒ Cx,a ⊆ Cy,a .
3. y-bal(a) ≤ x-bal(a) ⇒ Cy,a ⊆ Cx,a .
Proof. We proceed by constructing py = (y-has-coin, y-active) ∈ f (hy ) such
that it satisfies properties (1)-(3). To fulfill property (1), let y-active ,
x-active ∪ S, where S ∈ Coin\x-active and |S| = y-sum − x-sum. Then also
|y-active| = y-sum holds. To construct the Cy,a properly, the set y-active has
to be partitioned, since py ∈ f (hy ) and thus inv(y-has-coin, y-active). For
every a with x-bal(a) ≤ y-bal(a) we require Cx,a ⊆ Cy,a . Therefore there are
                            X
                                       x-bal(a) − y-bal(a)
                     a: x-bal(a)>y-bal(a)

additional spare coins. For a with x-bal(a) ≥ y-bal(a) we want Cy,a ⊆ Cx,a ,
which leaves us with
                            X
                                     y-bal(a) − x-bal(a)
                     a: x-bal(a)<y-bal(a)

missing coins. Hence, the difference is
                                            X
           y-sum − x-sum         +                        x-bal(a) − y-bal(a)
                                          a∈Address,
                                      x-bal(a)>y-bal(a)
                                            X
                                 −                        y-bal(a) − x-bal(a) .
                                          a∈Address,
                                      y-bal(a)>x-bal(a)
                           P
By replacing z-sum by         a∈Address z-bal(a) all the summands with either
y-bal(a) > x-bal(a) or x-bal(a) > y-bal(a) disappear and the remaining
value is 0. Therefore, such a partition of y-active exists and thus, there exists
py = (y-active, y-has-coin) ∈ f (hy ) satisfying (1), (2) and (3).             t
                                                                               u
                                            P
Lemma 9. Given two pairs hx , hy with          a∈Address z-bal(a) = z-sum, pz ∈
f (hz ), for z ∈ {x, y} and x-sum ≤ y-sum as in Lemma 8. Then, there exist a
bijective function count : Coin → N+ with count(z-active) = [1, z-sum] and
bijective functions idx(a, .) : Coin → N+ , with idx(Cz,a ) = [1, z-bal(a)], for
z ∈ {x, y}, a ∈ Address.
                                            Summing Up Smart Transitions         51

Proof. At first, we construct count. We know y-active = x-active ∪˙ S, where
|y-active| = y-sum, |x-active| = x-sum and |S| = y-sum − x-sum. Thus, we
can easily find an injective function with count(x-active) = [1, x-sum] and
count(S) = [x-sum + 1, y-sum]. Further, this function can be bijectively ex-
tended onto N+ . Similarly, for the addresses a, we construct idx(a, .) in the
following way. Since we know |Cz,a | = z-bal(a), we can find an injective func-
tion with idx(a, Cx,a ) = [1, x-bal(a)]. For all a, where y-bal(a) ≤ x-bal(a),
we can assume that idx(a, Cy,a ) = [1, y-bal(a)], as Cy,a ⊆ Cx,a . For these
addresses a, idx(a, .) can now also be extended bijectively onto N+ . Finally,
for a with x-bal(a) ≤ y-bal(a) we know Cx,a ⊆ Cy,a and can thus assume
idx(a, Cy,a \Cx,a )                                                          =
[x-bal(a) + 1, y-bal(a)]. Now also these idx(a, .) can be extended bijectively
onto N+ .                                                                    t
                                                                             u

   Having these two lemmas at hand we can now state and prove the following
result.

Theorem 11. Given any two pairsP ho                   ,     (old-bal, old-sum),
hn     ,       (new-bal, new-sum) with       a∈Address z-bal(a)    =     z-sum,
for z ∈ {old, new}. There exist bijective functions count : Coin → N+ and
idx(a, .) : Coin → N+ , for every a ∈ Address such that there are po =
(old-active, old-has-coin) ∈ f (ho ), pn = (new-active, new-has-coin)
∈ f (hn ) with
                                                      
                 ∀c. z-active(c) ↔ count(c) ≤ z-sum and                     (8)
                                                                
                 ∀a, c. z-has-coin(a, c) ↔ idx(a, c) ≤ z-bal(a) .           (9)

Proof. Let hx ∈ {ho , hn } such that x-sum = min {old-sum, new-sum}. The other
pair gets the prefix ’y-’ from now on. Also elements in f (hx ) and f (hy ) will be
named accordingly.
Let (x-active, x-has-coin) ∈ f (hx ) arbitrary, (y-has-coin, y-active) ∈ f (hy )
as in Lemma 8 and count, idx as in Lemma 9.
Then it holds count(z-active) = [1, z-sum]. Thus, ∀c. c ∈ z-active → count(c) ∈
[1, z-sum]. As count is bijective and therefore injective, it follows ∀c. c ∈
                                                                            / z-active →
count(c) ∈/ [1, z-sum]. Together with the fact that the codomain of count is N+
we get Formula 8. The analog argumentation works for Formula 9. We know
idx(a, Cz,a ) = [1, z-bal(a)]. Thus ∀c. c ∈ Cz,a → idx(a, c) ∈ [1, z-bal(a)].
Also idx(a, .) is bijective and therefore injective which implies ∀c. c ∈    / Cz,a →
idx(a, c) ∈/ [1, z-bal(a)]. By definition of Cz,a and the codomain of idx(a, .)
Formula 9 holds. This concludes the proof.                                          t
                                                                                    u


B.6   No Loss of Generality: Ordering of Coins

The property to prove is that whenever a block of coins has the same order in
two of our counting functions and they are not crossing its crucial value (sum,
bal(ai ) ), then we can assume that they are ordered in the same way. In order to
 52       Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

 do so, we have to formalize the notion of the former invariants inv’(idx, count).
 They are the formulas one gets by replacing has-coin and active by count and
 idx according to (Ax1) and (Ax2) in the invariants (I1)-(I3).

 Definition 26. Let count : Coin → N+ and idx : Address × Coin → N+ , then
 with the formulas

              ∀c. (∃a. idx(a, c) ≤ bal(a)) ↔ count(c) ≤ sum ,                              (I1’)
              ∀a, b, c. (idx(a, c) ≤ bal(a) ∧ idx(b, c) ≤ bal(b)) → a ≈ b                  (I2’)

 we define inv’(idx, count) , I1’ ∧ I2’.

 Theorem 12. Let
  (i) (old-bal, old-sum), (new-bal, new-sum) ∈ NAddress × N,
 (ii) count : Coins → N+ bijective,
(iii) idx : Address × Coin → N+ , such that idx(A, .) bijective for every a and
(iv) inv’(idx, count).
 If now
 (v) ∀c : Coin. f0 (c) ∈ [l0 , u0 ] ↔ f1 (c) ∈ [l1 , u1 ], where f0 , f1 ∈ {count} ∪
     {idx(a, .) : a ∈ Address} and
(vi) either ui ≤ xi or xi < li for i ∈ {0, 1}, where
     – xi , bal(ai ), if fi = idx(ai , .), or
     – xi , sum, if fi = count,
 then there exist idx0 , count0 with the properties (i)-(vi) and ∀c : Coin. f00 (c) ∈
 [l0 , u0 ] → f00 (c) + l1 ≈ f10 (c) + l0 .

 Proof. For simplicity assume f0 = idx(a0 , .) and f1 = idx(a1 , .). However, the
 proof works in an analog way for count. We proceed by constructing idx’ and
 count’ and then showing properties (i)-(vi) and ∀c : Coin. f00 (c) ∈ [l0 , u0 ] →
 f00 (c) + l1 = f10 (c) + l0 hold.
 The function count0 , count. We construct idx’ the following way.

                                      / [l1 , u1 ]) let idx0 (a, c) , idx(a, c)
        ∀a, c. (a 6≈ a1 ∨ idx(a1 , c) ∈                                             and
                                                    0
        ∀c. idx(a1 , c) ∈ [l1 , u1 ] we define idx (a1 , c) , idx(a0 , c) − l0 + l1 .

 With these definitions the properties (i), (ii), (vi) and ∀c : Coin. f00 (c) ∈
 [l0 , u0 ] → f00 (c) + l1 = f10 (c) + l0 obviously hold.
       To show property (v) we first fix a coin c and assume idx0 (a0 , c) ∈ [l0 , u0 ].
 By definition of idx’ we know that also idx(a0 , c) ∈ [l0 , u0 ] and then using (v)
 we get idx(a1 , c) ∈ [l1 , u1 ]. Again by definition of idx’, we have idx0 (a1 , c) =
 idx(a0 , c) − l0 + l1 . Since idx(a0 , c) ∈ [l0 , u0 ], it follows idx0 (a1 , c) = idx(a0 , c) −
 l0 +l1 ∈ [l1 , u0 −l0 +l1 ]. From property (v) and the bijectivity of the idx(a, .) func-
 tions, it follows that the intervalls have the same size and thus u0 − l0 = u1 − l1 .
 Therefore we end up having idx0 (a1 , c) ∈ [l1 , u1 ].
                                                    Summing Up Smart Transitions               53

For the other direction of the equivalence, we fix c and assume idx0 (a0 , c) ∈                /
[l0 , u0 ]. Then idx(a0 , c) ∈  / [l0 , u0 ] and using (v) we get idx(a1 , c) ∈/ [l1 , u1 ] and
thus
idx0 (a1 , c) = idx(a1 , c) ∈  / [l1 , u1 ]. This concludes the proof of (v).
Note that (v) implies idx0 (a1 , c) ∈ [l1 , u1 ] if and only if idx(a1 , c) ∈ [l1 , u1 ].
      The proof of property (iii) only requires showing idx0 (a1 , .) is bijective. For
showing injectivity, assume idx0 (a1 , c) = idx0 (a1 , d). where c 6= d. Then clearly
idx(a1 , c) 6= idx(a1 , d). Thus, one of idx(a1 , c), idx(a1 , d) ∈ [l1 , u1 ], since other-
wise idx0 (a1 , c) = idx(a1 , c) and idx0 (a1 , d) = idx(a1 , d). From the implication
of (v), we know that idx0 (a1 , c) = idx0 (a1 , d) ∈ [l1 , u1 ] and thus idx(a1 , c),
idx(a1 , d) ∈ [l1 , u1 ]. Therefore idx(a0 , c) − l0 + l1 = idx0 (a1 , c) = idx0 (a1 , d) =
idx(a0 , d) − l0 + l1 and thus idx(a0 , c) = idx(a0 , d) which is a contradiction to
the bijectivity of idx.
For surjectivity of idx0 (a1 , .) let n ∈ N+ be arbitrary. Assume n ∈         / [l1 , u1 ] first.
Then by surjectivity of idx(a1 , .) it follows that there is a c such that idx(a1 , c) =
n and as n ∈   / [l1 , u1 ], we have idx0 (a1 , c) = n. Assume now n ∈ [l1 , u1 ], then by
surjectivity of idx(a0 , .), there exists c such that idx(a0 , c) = n − l1 + l0 . With
the same reasoning as above it follows n − l1 + l0 ∈ [l0 , u0 ] and therefore we
conclude idx0 (a1 , c) = idx(a0 , c) − l0 + l1 = n. This completes the surjectivity
proof.
      Finally, we have to prove (iv). Once we have shown idx(a, c) ≤ bal(a) iff
idx0 (a, c) ≤ bal(a) for all a and for all c the property follows immediately,
since count0 = count. For all a, c with one of a 6= a1 or idx(a1 , c) ∈               / [l1 , u1 ]
the equivalence follows from the definition of idx0 . Consider now a1 with a c
such that idx(a1 , c) ∈ [l1 , u1 ]. Using the implication of (v), we get idx0 (a1 , c) ∈
[l1 , u1 ]. Now using property (vi), we know that either u1 ≤ bal(a1 ), in which
case idx(a1 , c), idx0 (a1 , c) ≤ bal(a1 ), or bal(a1 ) < l1 which implies idx(a1 , c),
idx0 (a1 , c) > bal(a1 ). This concludes the proof of property (iv) and thus of the
theorem.                                                                                       t
                                                                                               u
54     Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

C     SMTLIB Encodings and Function Calls

In this section the concrete function calls for each table are listed together with
one example encoding.


C.1   Codes for Table 3

The precise function calls used are as follows.

 – For Z3 default:
   z3 -smt2 <file-name>

 – For CVC4 default with full-saturate-quant:
   cvc4 --lang=smtlib2.6 --full-saturate-quant <file-name>

 – For Vampire default:
   vampire -input syntax smtlib2 <file-name>


Encoding of mint1, full surjectivity, with total, int version:
( set - logic UFLIA )
( declare - sort Coin 0 )
( declare - sort Address 0)
( declare - fun old - sum () Int )
( declare - fun new - sum () Int )
( declare - fun old - total () Int )
( declare - fun new - total () Int )
( declare - fun a0 () Address )
( declare - fun old - bal ( Address ) Int )
( declare - fun new - bal ( Address ) Int )
( declare - fun count ( Coin ) Int )
( declare - fun ind ( Coin Address ) Int )

; # ## axioms on sum and count ###
; # sum non - negative
( assert ( <= 0 old - sum ) )
( assert ( <= 0 new - sum ) )
; # count positive
( assert ( forall (( C Coin ) ) ( < 0 ( count C ) ) ) )
; # count injective
( assert ( forall (( C Coin ) ( D Coin ) )
  (= > (= ( count C ) ( count D ) ) (= C D ) ) ) )
; # count surjective
( assert ( forall (( N Int ) )
  (= >
    ( and ( < 0 N ) ( or ( <= N old - sum ) ( <= N new - sum ) ) )
    ( exists (( C Coin ) ) (= ( count C ) N ) ) ) ) )
                                           Summing Up Smart Transitions        55

; # ### axioms on bal and ind ###
; # bal non - negative
( assert ( forall (( A Address ) ) ( <= 0 ( old - bal A ) ) ) )
( assert ( forall (( A Address ) ) ( <= 0 ( new - bal A ) ) ) )
; # ind positive
( assert ( forall (( C Coin ) ( A Address ) ) ( < 0 ( ind C A ) ) ) )
; # ind (A ,.) injective
( assert ( forall (( C Coin ) ( D Coin ) ( A Address ) )
  (= > (= ( ind C A ) ( ind D A ) ) (= C D ) ) ) )
; # ind (A ,.) surjective
( assert ( forall (( N Int ) ( A Address ) )
  (= > ( and ( < 0 N ) ( or ( <= N ( new - bal A ) ) ( <= N ( old - bal A ) ) ) )
      ( exists (( C Coin ) ) (= ( ind C A ) N ) ) ) ) )

; # ## axioms between sum and bal ###
; # ind leq bal iff count leq sum
( assert ( forall (( C Coin ) ) (=
  ( exists (( A Address ) ) ( <= ( ind C A ) ( old - bal A ) ) )
  ( <= ( count C ) old - sum ) ) ) )
( assert ( forall (( C Coin ) ) (=
  ( exists (( A Address ) ) ( <= ( ind C A ) ( new - bal A ) ) )
  ( <= ( count C ) new - sum ) ) ) )
; # only once ind leq bal
( assert ( forall (( A Address ) ( B Address ) ( C Coin ) )
      (= > ( and
             ( <= ( ind C A ) ( old - bal A ) )
             ( <= ( ind C B ) ( old - bal B ) ) )
            (= A B ) ) ) )
( assert ( forall (( A Address ) ( B Address ) ( C Coin ) )
  (= > ( and
         ( <= ( ind C A ) ( new - bal A ) )
         ( <= ( ind C B ) ( new - bal B ) ) )
       (= A B ) ) ) )

; # ## transition and expected impact ###
; # mint1
( assert ( and
     (= ( new - bal a0 ) (+ ( old - bal a0 ) 1) )
     ( forall (( A Address ) )
         (= > ( distinct A a0 ) (= ( old - bal A ) ( new - bal A ) ) ) ) ) )
; # expected Impact
( assert (= (+ old - sum 1) new - sum ) )

; # ## invariants ###
; # pre - invariant
( assert (= old - sum old - total ) )
; # negated post - invariant
( assert ( distinct new - sum new - total ) )

( check - sat )
56      Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv




C.2    Codes for Table 4

The precise function calls used are as follows.

 – For Z3 default:
   z3 -smt2 <file-name>

 – For CVC4 default with full-saturate-quant:
   cvc4 --lang=smtlib2.6 --full-saturate-quant <file-name>

 – For Vampire default:
   vampire -input syntax smtlib2 <file-name> except the cases with su-
   perscripts.
    • Superscript ∗:
       vampire --input syntax smtlib2 <file-name>
       --forced options "aac=none:add=large:afp=40000:afq=
       1.2:amm=off:anc=none: bd=off:fsr=off:gsp=input only
       :inw=on:irw=on:lma=on:nm=64:nwc=1:sos=on:sp=
       occurrence:tha=off: updr=off:awr=5:s=1011:sa
       =discount:ind=math"

      • Superscript †:
        vampire -input syntax smtlib2 -thsq on -thsqd 6
        -thsqc 6 -thsqr 10,1 <file-name> to prove the property and its
        lemmas, if any.

      • Superscript ‡:
        options from ∗ to prove the inductive property in ind property id.smt
        and options from † to prove the actual property and its lemmas, if any.

Encoding of tranferN, uf version:
( set - logic UFLIA )
( declare - sort Coin 0 )
( declare - sort Address 0)
( declare - fun act ( Coin Int ) Bool )
( declare - fun hc ( Address Coin Int ) Bool )
( declare - fun induct ( Int ) Bool )
( declare - const a1 Address )
( declare - const a2 Address )
( declare - const n Int )

; # ## inductive predicate definition ###
( assert ( forall (( I Int ) )
  (= ( induct I )
                                           Summing Up Smart Transitions   57

      ( and ( forall (( C Coin ) )
              (= ( exists (( A Address ) ) ( hc A C I ) ) ( act C I ) ) ) )
            ( forall (( A Address ) ( B Address ) ( C Coin ) )
              (= > ( and ( hc A C I ) ( hc B C I ) ) (= A B ) ) ) ) ) ) )

; # ## pre - invariants ###
; # inactive coins and at least one
( assert ( forall (( C Coin ) )
(= ( exists (( A Address ) ) ( hc A C 0) )
     ( act C 0) ) ) )
; # at most one
( assert ( forall (( A Address ) ( B Address ) ( C Coin ) )
(= > ( and ( hc A C 0) ( hc B C 0) ) (= A B ) ) ) )

; # ## transition ###
( assert ( forall (( I Int ) ) (= >
  ( <= 0 I )
  ( and ( forall (( D Coin ) ) (= ( act D I ) ( act D (+ I 1) ) ) )
        ( exists (( C Coin ) ) ( and
          ( hc a1 C I ) ( not ( hc a2 C I ) )
          ( not ( hc a1 C (+ I 1) ) ) ( hc a2 C (+ I 1) )
          ( forall (( D Coin ) ( A Address ) )
            (= > ( or ( distinct C D )
                      ( and ( distinct A a1 ) ( distinct A a2 ) ) )
                 (= ( hc A D (+ I 1) ) ( hc A D I ) ) ) ) ) ) ) ) ) )

; # ## negated post - invariant ###
( assert ( and ( <= 0 n ) ( not ( induct n ) ) ) )

( check - sat )



C.3    Codes for Table 5
The precise function calls used are as follows.
 – For Z3 default:
   z3 -smt2 <file-name>

 – For CVC4 default with full-saturate-quant:
   cvc4 --lang=smtlib2.6 --full-saturate-quant <file-name>

 – For Vampire default:
   vampire -input syntax smtlib2 <file-name>


Encoding of bal(a0 ) + 5, bal(a1 ) − 3, bal(a2 ) − 1:
( set - logic UFLIA )
( declare - sort Coin 0 )
58     Neta Elad, Sophie Rain, Neil Immerman, Laura Kovács, and Mooly Sagiv

( declare - sort Address 0)
( declare - fun old - sum () Int )
( declare - fun new - sum () Int )
( declare - fun a0 () Address )
( declare - fun a1 () Address )
( declare - fun a2 () Address )
( declare - fun old - bal ( Address ) Int )
( declare - fun new - bal ( Address ) Int )
( declare - fun count ( Coin ) Int )
( declare - fun ind ( Coin Address ) Int )

; # ## axioms on sum and count ###
; # sum non - negative
( assert ( <= 0 old - sum ) )
( assert ( <= 0 new - sum ) )
; # count positive
( assert ( forall (( C Coin ) ) ( < 0 ( count C ) ) ) )
; # count injective
( assert ( forall (( C Coin ) ( D Coin ) )
  (= > (= ( count C ) ( count D ) ) (= C D ) ) ) )
; # count instances of surjectivity
( assert ( exists (( C Coin ) ) (= ( count C ) old - sum ) ) )
( assert ( exists (( C Coin ) ) (= ( count C ) (+ old - sum 1) ) ) )
( assert ( exists (( C Coin ) ) (= ( count C ) new - sum ) ) )

; # ### axioms on bal and ind ###
; # bal non - negative
( assert ( forall (( A Address ) ) ( <= 0 ( old - bal A ) ) ) )
( assert ( forall (( A Address ) ) ( <= 0 ( new - bal A ) ) ) )
; # ind positive
( assert ( forall (( C Coin ) ( A Address ) ) ( < 0 ( ind C A ) ) ) )
; # ind (A ,.) injective
( assert ( forall (( C Coin ) ( D Coin ) ( A Address ) )
  (= > (= ( ind C A ) ( ind D A ) ) (= C D ) ) ) )
; # ind (A ,.) instances of surjectivity
( assert ( exists (( C Coin ) ) (= ( ind C a0 ) ( old - bal a0 ) ) ) )
( assert ( exists (( C Coin ) ) (= ( ind C a0 ) (+( old - bal a0 ) 1) ) ) )
( assert ( exists (( C Coin ) ) (= ( ind C a0 ) (+( old - bal a0 ) 2) ) ) )
( assert ( exists (( C Coin ) ) (= ( ind C a0 ) (+( old - bal a0 ) 3) ) ) )
( assert ( exists (( C Coin ) ) (= ( ind C a0 ) (+( old - bal a0 ) 4) ) ) )
( assert ( exists (( C Coin ) ) (= ( ind C a0 ) (+( old - bal a0 ) 5) ) ) )
( assert ( exists (( C Coin ) ) (= ( ind C a1 ) ( new - bal a1 ) ) ) )
( assert ( exists (( C Coin ) ) (= ( ind C a1 ) (+( new - bal a1 ) 1) ) ) )
( assert ( exists (( C Coin ) ) (= ( ind C a1 ) (+( new - bal a1 ) 2) ) ) )
( assert ( exists (( C Coin ) ) (= ( ind C a1 ) (+( new - bal a1 ) 3) ) ) )
( assert ( exists (( C Coin ) ) (= ( ind C a2 ) ( new - bal a2 ) ) ) )
( assert ( exists (( C Coin ) ) (= ( ind C a2 ) (+( new - bal a2 ) 1) ) ) )

; # ## axioms between sum and bal          ###
; # ind leq bal iff count leq sum
                                        Summing Up Smart Transitions    59

( assert ( forall (( C Coin ) ) (=
  ( exists (( A Address ) ) ( <= ( ind C A ) ( old - bal A ) ) )
  ( <= ( count C ) old - sum ) ) ) )
( assert ( forall (( C Coin ) ) (=
  ( exists (( A Address ) ) ( <= ( ind C A ) ( new - bal A ) ) )
  ( <= ( count C ) new - sum ) ) ) )
; # only once ind leq bal
( assert ( forall (( A Address ) ( B Address ) ( C Coin ) )
  (= > ( and
          ( <= ( ind C A ) ( old - bal A ) )
          ( <= ( ind C B ) ( old - bal B ) ) )
       (= A B ) ) ) )
( assert ( forall (( A Address ) ( B Address ) ( C Coin ) )
  (= > ( and
          ( <= ( ind C A ) ( new - bal A ) )
          ( <= ( ind C B ) ( new - bal B ) ) )
       (= A B ) ) ) )

; # ## transition and negated impact ###
; # plus5 minus3 minus1
( assert ( and
     (= ( new - bal a0 ) (+ ( old - bal a0 ) 5) )
     (= ( old - bal a1 ) (+ ( new - bal a1 ) 3) )
     (= ( old - bal a2 ) (+ ( new - bal a2 ) 1) )
     ( forall (( A Address ) ) (= >
        ( and ( distinct A a0 ) ( distinct A a1 ) ( distinct A a2 ) )
        (= ( old - bal A ) ( new - bal A ) ) ) ) ) )

; # negated Impact
( assert ( distinct (+ old - sum 1) new - sum ) )

( check - sat )
