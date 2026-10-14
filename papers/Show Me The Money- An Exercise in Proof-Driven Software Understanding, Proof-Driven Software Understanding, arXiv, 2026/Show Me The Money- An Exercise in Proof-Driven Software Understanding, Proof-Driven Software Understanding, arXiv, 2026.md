                                                    Show Me The Money: An Exercise in
                                                    Proof-Driven Software Understanding

                                             Joseph Tafese⋆1 , Karthik Nukala2 , Hassen Saïdi3 , Natarajan Shankar2 ,
                                                                Arie Gurfinkel1 , Giuliano Losa4
                                                              1
                                                               University of Waterloo, Waterloo, Canada
                                                                {jetafese, agurfink}@uwaterloo.ca
                                                                2
                                                                  SRI International, Menlo Park, USA
                                                           {karthik.nukala, natarajan.shankar}@sri.com
                                                                              3
                                                                                Entalus
                                                                     hassen.saidi@entalus.com
                                                                  4
                                                                    Stellar Development Foundation
                                                                       giuliano@stellar.org
arXiv:2607.16499v1 [cs.LO] 17 Jul 2026




                                                 Abstract. We present a case study on proof-driven software understand-
                                                 ing of mature, security-critical infrastructure. While formal methods are
                                                 traditionally applied during the design phase, we present our experience
                                                 applying formal reasoning onto a mature industrial C++ codebase. We
                                                 focus on a formal analysis of the core algorithm that implements the
                                                 Stellar blockchain’s SDEX order book. By combining large language mod-
                                                 els (LLMs), Prototype Verification System (PVS), and Seahorn, we are
                                                 able to prove core properties of the production codebase. Our approach
                                                 also identified an inconsistency in documentation related to the reacha-
                                                 bility of an exception location. Most importantly, however, we produce
                                                 artifacts that make it easy for code changes to be checked against estab-
                                                 lished invariants. This work demonstrates how the strategic combination
                                                 of theorem proving and model checking provides a path for delivering
                                                 robust assurance to legacy systems.

                                                 Keywords: autoformalization, theorem proving, model checking, soft-
                                                 ware understanding


                                         1     Introduction

                                         A vast amount of production software delivers safety/value-critical functionality
                                         long after its original developers have moved on. In such systems, correctness
                                         does not rest solely on the absence of known bugs but on the preservation of
                                         subtle design invariants whose rationale may exist only in developer intuition or
                                         informal documentation. As these systems evolve, the loss of this understand-
                                         ing creates a significant risk since even small changes can violate assumptions
                                         that were not explicitly stated, let alone mechanically checked. We encountered
                                         ⋆
                                             Corresponding author.
2      J. Tafese, et al.

precisely this situation in Stellar’s offer exchange subsystem, SDEX5 , that imple-
ments the order book at the heart of the Stellar blockchain. This code has been
deployed and exercised in production for over a decade, is carefully documented,
and is widely believed to be correct. Yet its correctness arguments (e.g., rounding
behavior, order fairness, etc.) are embedded in comments and complex control
flow. As a result, even minor changes are approached with caution, slowing de-
velopment, and increasing the cost of assurance. The challenge is not a lack of
testing or care, but the absence of a representation of the intended semantics of
the system that can be easily inspected, queried, and evolved.
    Formal models are uniquely suited to this role. They provide a precise vo-
cabulary for stating assumptions, enable invariant-based reasoning, and serve
as stable reference points as implementations evolve. In principle, constructing
such a model is the most direct way to recover and preserve the semantic knowl-
edge embedded in mature code. However, in practice, constructing formal models
from existing implementations has been prohibitively difficult. Recent progress
in large language models (LLMs) fundamentally alters this landscape by en-
abling automatic production of candidate abstractions in formal languages. By
subjecting LLM-generated abstractions to typechecking, proof obligations, and
executable analysis, we can validate and refine them into trustworthy models
that support real reasoning about the system.
    To understand a widely used production system, we analyze the SDEX with
an emphasis on exchangeV10, its core algorithm with 1 344 lines of C/C++
code and 758 lines of comments. Using the production codebase, we construct
an LLM-aided PVS [6] abstraction with 260 lines of PVS and 84 lines of com-
ments. With this, we prove 16 lemmas (generated by the LLM) and 22 proof
obligations (generated by the PVS typechecker) to establish key properties of
exchangeV10. We also encounter an unprovable subgoal which we convert into
a unit proof [9] (i.e., a symbolic test case) on the C++ code for Seahorn [3] to
find a concrete counterexample. Our experience shows how formal methods can
be applied retroactively on mature systems to produce machine-checked artifacts
that aid software understanding.
    This paper is supported by a public GitHub repository6 including documen-
tation, C++ code, PVS models and proofs, and Seahorn unit proofs. The
rest of the paper is structured as follows: we present SDEX and the necessary
background in Section 2, the core components of our exercise in Section 3, our
reflections in Section 4 and conclude in Section 5.


2   SDEX: Stellar’s Offer Exchange
The Stellar network is a blockchain platform that, in addition to smart contracts,
supports asset exchange through a built-in central limit order book, commonly
called the Stellar Decentralized EXchange (SDEX). A central limit order book is
5
  https://developers.stellar.org/docs/learn/fundamentals/liquidity-on-
  stellar-sdex-liquidity-pools
6
  https://github.com/jetafese/order-book-core
 Show Me The Money: An Exercise in Proof-Driven Software Understanding              3

                                  at least 1.5 CAD/USD
                           A
                                  acceptable
                                   to both
                                                 B
                     at most 1.66 CAD/USD
                                                            price (CAD/USD)
                            1.5                1.66

Fig. 1: Crossing offers: A accepts prices p ≥ 1.5, B accepts prices p ≤ 1.66; the
shaded intersection is non-empty.



a standard financial mechanism where participants can submit limit orders, also
called offers in our context, to buy/sell assets at some maximum/minimum limit
price, and all offers are submitted to the same central matching system. Along-
side its native currency – the Lumen (XLM) – users may issue custom assets
and trade them via this order book. Users interact with SDEX by submitting
transactions, each containing a list of operations to be executed atomically; po-
tential operations include creating new assets, placing offers to exchange assets,
and so-called path payment operations that allow chaining asset exchanges (e.g.,
CAD→USD→EUR).
     An offer to exchange assets specifies (i) an asset to sell, (ii) an asset to buy,
(iii) a minimum acceptable price, (iv) a maximum quantity to be sold and (v)
an account for sending/receiving assets. Offers persist in the order book until
they are fully executed or canceled. A trade occurs when two offers are matched
and assets are transferred between accounts. Two offers are said to cross if their
price constraints overlap, meaning that there exists at least one exchange rate
acceptable to both parties. When offers cross, SDEX may execute a trade, subject
to constraints and rounding due to the fixed-point representation of quantities.
    We illustrate these concepts with a simple example. Account A places an
offer to sell up to 100 USD at a price of at least 1.5 CAD/USD, i.e., it is willing
to receive no fewer than 1.5 CAD for each USD sold. Account B places an offer
to sell up to 200 CAD at a price of at least 0.6 USD/CAD. Expressed in the
same units, B requires an exchange rate of at most 1/0.6 ≈ 1.66 CAD/USD
and A requires an exchange rate of at least 1.5 CAD/USD. Since the acceptable
price ranges overlap, the two offers cross. We show this visually in Fig. 1.
    When two crossing offers are matched, the SDEX computes an exchange that
satisfies both parties’ price and quantity constraints after fixed-point rounding.
The exchange executes at most the maximum quantity permitted by both offers.
If the exchange is partial, one offer is fully consumed and removed from the order
book, while the other remains with a reduced quantity. In the example above, one
possible execution is to round in B’s favor: A sells 100 USD to B and receives
⌊100/0.6⌋ = 166 CAD, with an effective exchange rate of approximately 1.66
CAD/USD. However, there are other options, e.g., rounding the other way or
picking another valid price. The exact transfer is determined by exchangeV10.
4        J. Tafese, et al.

Algorithm 1 exchangeV10
Require: Price (n, d), bounds (Wsmax , Wrmax , Ssmax , Srmax ), rounding mode round
Ensure: (Wr , Ss , wheatStays)
 1: (Wr , Ss , wheatStays) ← ExchangeCore((n, d), Wsmax , Wrmax , Ssmax , Srmax , round )
 2: (Wr , Ss ) ← ApplyPriceErrorThresholds((n, d), Wr , Ss , wheatStays, round )
 3: return (Wr , Ss , wheatStays)



    The correctness of SDEX is critical to the functioning of the system, as bugs
may crash the whole system or lead to the loss of assets and may be exploited by
attackers. Because the SDEX operates on fixed-point arithmetic, its correctness
depends on subtle interactions between matching, rounding, and fairness guar-
antees. We start with the core algorithm, exchangeV10, since it is one of the
more intricate parts of SDEX. There are four properties (P1— P4) that must
hold at the time of each exchange in order to ensure predictable and economi-
cally sound behavior. P1: When two offers are matched, rounding is performed
in favor of the offer that remains on the order book after the exchange. P2:
For exchanges that match against a single offer, rounding may alter the effective
exchange rate by no more than 1%. P3: When a transaction is a path payment,
rounding errors may exceed 1%; for all other transactions, any exchange that
would violate this bound is rejected. P4: No unexpected exceptions are thrown.
    exchangeV10 is primarily implemented in a single file7 in the stellar-core
repository. The inputs are: a price, a rounding type, and limit amounts for
both sides of a trade, and the output is the amounts exchanged. We summarize
exchangeV10 and (later) its helper functions in Algorithms 1 and 2 respectively.
The function was developed and maintained for 11 years by at least 5 primary
engineers with a nuanced understanding of the functional behavior and corre-
sponding invariants. However, organizational turnover made it hard to maintain
knowledge of this codebase.



3     Proof-Driven Software Understanding

To understand the exchangeV10 implementation and produce a machine check-
able artifact, we aim at: (1) constructing a formal model that captures its core
functionality, (2) proving that properties (P1 – P4) hold of the model and
(3) ensuring they also hold for the actual code. We present a streamlined ap-
proach (Fig. 2) that (1) leverages LLMs to autoformalize the exchangeV10 code
with feedback from the PVS typechecker (Section 3.1), (2) proves properties of
exchangeV10 aided by PVS’s automation (Section 3.2), and (3) verifies that the
model corresponds to the original C++ code using SeaBMC [8], the bounded
model checker of Seahorn (Section 3.3).

7
    See OfferExchange.cpp
    Show Me The Money: An Exercise in Proof-Driven Software Understanding            5




Fig. 2: We present the three stages of our exercise: Formalizing, Proving and
Finding Defects in Industrial C++ Code using LLMs, PVS and SeaHorn.


3.1     LLM Autoformalization (C++ to PVS)

At this stage, our goal was to go from a blank screen to a potentially useful PVS
model that successfully passes the PVS typechecker, a first anchor for under-
standing the codebase. We leveraged the fact that the PVS language is functional
and exchangeV10 is mostly functional, in that it does not maintain state but
can throw exceptions. exchangeV10 contains both code and natural-language
arguments of established properties and invariants, expressed as comments ac-
companying the C++ code. The goal is to produce a formalization in PVS that
is faithful to the code and comments (see Fig. 3).
    We started by copying the full source code of exchangeV10 to ChatGPT 5
Pro, prompting it to generate a PVS model, and validating the model with a
local PVS client. The PVS typechecker had several complaints that we resolved
by copying failure messages to ChatGPT and copying the PVS model it pro-
duces back to our PVS client. We repeated the process with Claude Opus 4,
to similar results. At this stage, we encountered hallucinations such as x DIV y
(where DIV is not a PVS function), and declaration-level syntactic issues like mis-
placed IMPORTING statements and made-up library names. Once we addressed
these typechecking failures8 , we found that there was significant structural cor-
respondence between exchangeV10 and the PVS model. For example, function
boundaries were respected, conditional statements were in direct correspondence
and the generated lemmas aligned with the comments in exchangeV10. On the
other hand, the LLMs wrongly modeled exceptions as unused boolean variables,
which hindered attempts to prove P4. To capture the learning from this exercise,
we developed a prompt (see Section 4) that successfully reduced these pitfalls.

8
    PVS’s full typechecking involves the generation of TCCs, rendering type inhabita-
    tion undecidable in general. We refer, here, to the first phase which involves name
    resolution and sound generation of TCCs.
6       J. Tafese, et al.

                                                                                               
%---------------------------------------------------------------------------
% less than or equal to 1% bound when cFW is False. That is:
% abs((price‘n/price‘d)-(sS/wR))/((price‘n/price‘d)) <= 1/100
%---------------------------------------------------------------------------
one_percent_normal: LEMMA
FORALL (p: Price, wR: posint64, sS: posint64):
  LET price = (p‘n/p‘d), effP = (sS/wR) IN
  checkPriceErrorBound(p, wR, sS, False) IFF abs(price - effP)/(price) <= 1/100
%---------------------------------------------------------------------------
% less than or equal to 1% bound when cFW is True and sheep is favored.
% That is: abs((price‘n/price‘d)-(sS/wR))/((price‘n/price‘d)) <= 1/100
%---------------------------------------------------------------------------
one_percent_path_favor_sheep: LEMMA
FORALL (p: Price, wR: posint64, sS: posint64):
  LET price = (p‘n/p‘d), effP = (sS/wR), rhs = 100 * p‘d * sS, lhs = 100 * p‘n * wR IN
  checkPriceErrorBound(p, wR, sS, True) AND (rhs < lhs) => abs(price - effP)/(price) <= 1/100
                                                                                               

Fig. 3: Autoformalized lemma from the comment: “Check that the relative error
between the price and the effective price does not exceed 1%. If canFavorWheat
== true then this function does an asymmetric check such that error favoring
the seller of wheat can be unbounded, while the relative error between the price
and the effective price does not exceed 1% if it is favoring the seller of sheep.
The functionality of canFavorWheat (cFW) is required for PathPayment.”


    Through interaction with PVS, we manually separated the theories that cor-
respond to distinct functions used by exchangeV10 into 3 separate files (i.e., a file
for exchangeV10, ApplyPriceErrorThresholds and CheckPriceErrorBound).
This allowed us to isolate properties by their relevance to a function and de-
fine preconditions to determine how functions should interface with each other.
The latter capability proved to be quite a powerful way to specify exception-free
paths through a function (i.e., the “happy path”).
    The rapid iteration with the LLM allowed us to understand the software
being formalized without spending significant manual effort. While there are
many opportunities for automating the otherwise manual parts of this stage,
we explicitly choose to leave the human-in-the-loop because our exercise centers
around human software understanding. Moreover, this exercise can serve as a
gentle introduction to software modeling and theorem proving.

3.2    Theorem Proving and Efficient Arguments in PVS
    PVS’s emphasis on the interplay between language and automation facilitates
both the autoformalization effort and the interactive human proof effort. The
PVS language supports a style of formalization that restricts properties to a
minimal scope, ensuring tractability and predictability of the underlying decision
procedures (involved in discharging these conditions) and providing just enough
feedback so the human can understand what might needed for correctness.
    To prove the properties of exchangeV10, we use PVS’s automated internal
procedures (e.g., assert, grind) built on to Shostak’s method [10]. We also dis-
charge queries involving nonlinear arithmetic with the Yices2 SMT solver [1].
    Show Me The Money: An Exercise in Proof-Driven Software Understanding                 7

                                                                                           
one_percent_path_favor_sheep: LEMMA                 % 1) Skolemization, exposing predicates
FORALL (p: Price, wR: posint64, sS: posint64):      (SKEEP :PREDS? T)
LET price = (p‘n/p‘d), effP = (sS/wR),              % 2) Shostak/SMT simplification
     rhs = 100 * p‘d * sS, lhs = 100 * p‘n * wR     (ASSERT) ; Shostak
IN                                                  % 3) BDD simplifier/normalizer
   checkPriceErrorBound(p, wR, sS, True)            (BDDSIMP)
   AND (rhs < lhs)                                  % 4) Super-duper rewrite/expand/SMT/BDD
   IMPLIES abs(price - effP)/(price) <= 1/100       (GRIND :THEORIES ("real_props"))
                                                                                           

Fig. 4: An example PVS proof of an asymmetrical rounding lemma from Fig. 3.


Shostak’s method enables incremental SMT reasoning and proof state simpli-
fication, allowing a user-facing entry point to the internal solver and tractable
readings of its current solution state. Fig. 4 showcases the variety of procedures
used in establishing the asymmetric rounding condition of the exchangeV10. In
addition to this lemma, there were typechecking constraints that needed to be
established to complete the proof. We show examples of these in Fig. 5.
    In this stage, we gained local, property-directed understanding of the pro-
gram by leveraging PVS’s modular language and representations. When com-
bined with transparent automation and specification utilities, program under-
standing became a dialogue with the proof assistant. We proved 37/38 lemmas
and TCCs that were sufficient to prove correctness of exchangeV10 relative to
P1— P3. For example, for P2, we proved that the PVS model adhered strictly
to the 1% bound on rounding for exchanges that match a single offer. On the
38’th TCC, however, we were confronted with a subgoal for P4 that we could
not prove (after numerous attempts and iterations); this prompted us to go back
to the C++ code.


3.3     SeaHorn and Executable Counter Examples

We found it useful to connect our inability to prove P4 in PVS with a counterex-
ample execution of the C++ code. Inspired by the Floyd-Hoare Logic [2, 4], and
much like a unit test, a unit proof consists of a harness that sets up symbolic
variables and preconditions, invokes the system under test (SUT), and asserts
postconditions. We constructed unit proofs by encoding the type constraints
from the PVS formalization as assumptions over C++ variables, and composed
assertions using standard Boolean operators. Seahorn compiles the unit proof
and the SUT to LLVM bitcode, which is then checked by the SeaBMC model-
checker as demonstrated in [11–14]. For example, we used the executable wit-
ness (read off the PVS sequent/unprovable subgoal) to construct the unit proof
in Fig. 6, from which Seahorn generated an executable counterexample (CEX)
that we debugged with lldb (see the trace in Fig. 7). This is how we disproved a
property in the comments about a path-payment exception that is not expected
to be thrown. Concretely, P4 is disproved since an exception is thrown when the
rounding type is a Path Payment Strict Send and the inputs to exchangeV10
are: p = (2, 4), maxWheatSend = 1, maxWheatReceive = 2, maxSheepSend =
8       J. Tafese, et al.


// - -[ OfferExchange . cpp , L164 -166] - -
// These never overflow since price . n and price . d are int32_t
int64_t errN = ( int64_t ) 100 * ( int64_t ) price . n ;
int64_t errD = ( int64_t ) 100 * ( int64_t ) price . d ;
                                             
Price: TYPE = [# n: uint32, d: uint32 #]
checkPriceErrorBound(price: Price...): bool                                                  
= LET errN: posint64 = 100 * price‘n,             % Subtype TCC generated for 100 * price‘n
      errD: posint64 = 100 * price‘d,             % expected type posint64
      ...                                         checkPriceErrorBound_TCC1: OBLIGATION
                                                  FORALL (price: Price, ...):
                                                    100 * price‘n > 0;
----[Prelude integertypes]----
uint32: TYPE = upto(exp2(32) - 1)                 % Subtype TCC generated for 100 * price‘d
uint64: TYPE = upto(exp2(64) - 1)                 % expected type posint64
posint64: TYPE = { u: uint64 | u > 0 }            checkPriceErrorBound_TCC2: OBLIGATION
times_u16_u16: JUDGEMENT                            FORALL (price: Price, ...):
                                                    100 * price‘d > 0;
  *(ux16, uy16) HAS_TYPE uint32
times_u32_u32: JUDGEMENT                                                                     
  *(ux32, uy32) HAS_TYPE uint64
                                             

Fig. 5: We examine an exchangeV10 lemma derived from comments in
OfferExchange.cpp,shown at the top. During autoformalization, these decla-
rations become LET-bindings as shown in the top-left checkPriceErrorBound
PVS declaration. In the bottom-left, we show that leveraging the existing PVS
Prelude theory, the typechecker can automatically establish type constraints
across type families. On the right, we show type-correctness conditions (TCCs)
generated by the typechecker that need to be discharged in the PVS prover.




1, maxSheepReceive = 0. We present a pseudo-code description of the problem-
atic function in Algorithm 2, where the exception condition in question appears
as an assert at line 15. SDEX developers are confident that upstream code pre-
vents this exception from being reached, but proving this claim is out-of-scope
for exchangeV10.


    Integrating Seahorn complements the proof-based methodology in several
ways. First, it acts as a sanity check, ensuring that formally proven invariants
are relevant and observable in the concrete system. Once a lemma was proven
in PVS, we replicated it with a unit proof, over the exchangeV10 implementa-
tion, to be run with Seahorn. Second, it accelerates debugging by producing
concrete inputs that trigger subtle corner cases. Finally, it enables a tightly
coupled iterative loop: PVS abstractions guide the generation of unit proof pre-
conditions, counterexamples inform refinement of the abstraction, and updated
proofs confirm the corrected properties. This provides a pathway for developers
to gain confidence in the correctness of legacy code while still supporting code
evolution.
    Show Me The Money: An Exercise in Proof-Driven Software Understanding                       9

void v e r i f y _ w h e a t S t a y s _ P A T H _ P A Y M E N T _ S T R I C T _ S E N D () {   1
    // setup variables provided by called                                                       2
    int32_t n = sea_nd_i32 () ;                                                                 3
    int32_t d = sea_nd_i32 () ;                                                                 4
    int64_t maxWheatSend = sea_nd_i64 () ;                                                      5
    int64_t ma xSh eepRecei ve = sea_nd_i64 () ;                                                6
    int64_t ma xWh eatRecei ve = sea_nd_i64 () ;                                                7
    int64_t maxSheepSend = sea_nd_i64 () ;                                                      8
    // assume preconditions                                                                     9
    assume ( n > 0 && d > 0) ;                                                                  10
    assume ( maxWheatSend >= 0 && maxSheepSend > 0) ;                                           11
    assume ( m axW hea tRece ive > 0) ;                                                         12
    auto round = RoundingType :: P A T H _ P A Y M E N T _ S T R I C T _ S E N D ;              13
    // Call SUT                                                                                 14
    Price p {n , d };                                                                           15
    auto res = exchangeV10 (p , maxWheatSend , maxWheatReceive , maxSheepSend ,                 16
           maxSheepReceive , round ) ;                                                          17
    // enforce postcond itions                                                                  18
    sassert (! res . wheatStays || ( res . numSheepSend > 0 &&                                  19
           res . nu mWh ea tRe ce iv ed >= 0) ) ;                                               20
}                                                                                               21


Fig. 6: Unit proof for exchangeV10 with Path Payment Strict Send Rounding.


4      Discussion
We have presented our experience formally specifying an industrial C++ code
in PVS where we successfully proved properties P1—P3 and disproved P4.
While these properties were so far only informally documented, we now have a
validated model and proofs about the implementation. In this section we discuss
the broader applicability of the methodology and areas of improvements and
future research.
    Our success in formalizing and validating the model of exchangeV10 is in
part due to the fact that the C++ code involved is well-documented, including
informal explanations of critical invariants and their proofs, mostly functional,
and modular in its structure and presentation. The informal documentation and
invariants helped us and the LLM formalize the properties to prove. Without
this, we would have had to learn a lot more about the subsystem and the context
in which it is used in order to derive the important properties to check. Mod-
ularity of the code allowed us to proceed step by step, without any blow-up in
complexity as we formalized more and more code. By following good engineering
principles, the original authors of this code already did a good part of the work
involved in applying formal methods to gain assurance in software correctness,
and the methodology we present allows harnessing that work.
    We expect that our methodology will apply equally well to other code bases
that follow strong engineering principles and are well-documented and modular,
even if they are larger. The key reason is that the formal artifacts we construct
(e.g., proof-oriented abstractions, invariants, and lemmas) are aligned with the
code structure and subsystem boundaries, inheriting the modularity and sep-
aration of concerns introduced by the engineers who authored the code. One
important aspect that we have not experienced in practice is the adaptation to
an evolving code base (exchangeV10 did not change during our exercise). The
Seahorn unit proofs are likely to be of help in this case because they can iden-
10      J. Tafese, et al.

Algorithm 2 Apply Price Error Thresholds
Require: Price (n, d), amounts (Wr , Ss ), wheatStays, rounding mode
Ensure: Adjusted (Wr , Ss )
 1: function ApplyPriceErrorThresholds((n, d), maxSend , maxReceive)
 2:    if Wr > 0 ∧ Ss > 0 then
 3:        Vr ← W r · n
 4:        Vs ← S s · d
 5:        assert: wheatStays =⇒ Vs ≥ Vr and ¬wheatStays =⇒ Vs ≤ Vr
 6:        if round = NORMAL then
 7:            if ¬ CheckPriceErrorBound((n, d), Wr , Ss , f alse) then
 8:                Wr ← 0; Ss ← 0
 9:            end if
10:        else
11:            assert: CheckPriceErrorBound((n, d), Wr , Ss , true)
12:        end if
13:    else
14:        assert: round = PPS_SEND =⇒ Ss ̸= 0
15:        Wr ← 0; Ss ← 0
16:    end if
17:    return (Wr , Ss )
18: end function
19: function CheckPriceErrorBound((n, d), (Wr , Ss ), canFavourWheat)
20:    K ← 100                                 ▷ Threshold scaling factor for 1% error
21:    L ← K · n · Wr ; R ← K · d · Ss
22:    if canFavorWheat ∧ R > L then
23:        return true
24:    end if
25:    D ← |L − R|                         ▷ Absolute difference between scaled values
26:    C ← n · Wr                                      ▷ Cap based on intended price
27:    return (D ≤ C)
28: end function



tify property violations as long as the interfaces used by the unit proofs do not
change. Otherwise, we have to reapply the autoformalization methodology and
create new unit proof harnesses. Automating the creation of Seahorn harnesses
would help in this process, and this is an area where our work can be improved.
    An important outcome of this work is that it provides a concrete narrative
that formal methods researchers can use when engaging with industry. Rather
than requiring greenfield development or specialized training, we start from ar-
tifacts engineers already produce: production code, comments, informal invari-
ants, and test harnesses. LLM-assisted autoformalization lowers the barrier to
constructing an initial model; PVS provides strong automation and early feed-
back; and Seahorn reconnects formal reasoning to executable behavior. This
combination makes it feasible to integrate formal reasoning into existing work-
flows such as code review, regression testing, and continuous integration. In the
exchangeV10 codebase, engineers have reasoned explicitly about rounding, fair-
ness, bounds, and unreachable states, but these arguments are scattered across
    Show Me The Money: An Exercise in Proof-Driven Software Understanding                 11

                                                                                              
(lldb) target create "./exchange.out"
Current executable set to ’/order-book-core/exchange/exchange.out’ (arm64).
(lldb) b -n __VERIFIER_error
Breakpoint 1: where = exchange.out‘::__VERIFIER_error() + 8 at seahorn.cpp:26:3, ...
(lldb) r
Process 71139 launched: ’/order-book-core/exchange/exchange.out’ (arm64)
Process 71139 stopped
* thread #1, queue = ’com.apple.main-thread’, stop reason = breakpoint 1.1
    frame #0: 0x0000000100012824 exec.out‘::__VERIFIER_error() at seahorn.cpp:26:3 [opt]
   23    }
   24
   25    void __VERIFIER_error() {
-> 26      printf("[sea] __VERIFIER_error was executed\n");
   27      exit(1);
   28    }
   29
Target 0: (exec.out) stopped.
(lldb) bt
* thread #1, queue = ’com.apple.main-thread’, stop reason = breakpoint 1.1
  * frame #0: 0x0000000100012824 exec.out‘::__VERIFIER_error() at seahorn.cpp:26:3 [opt]
    frame #1: 0x0000000100000e50 exec.out‘sassert(cond=false) at vOfferExchange.cpp:13:9
    frame #2: 0x0000000100002694 exec.out‘stellar::applyPriceErrorThresholds(price=(n = 2, d
      = 4), wheatReceive=0, sheepSend=0, wheatStays=false, round=PATH_PAYMENT_STRICT_SEND)
      at vOfferExchange.cpp:790:17
    frame #3: 0x000000010000213c exec.out‘stellar::exchangeV10(price=(n = 2, d = 4),
      maxWheatSend=1, maxWheatReceive=2, maxSheepSend=1, maxSheepReceive=0,
      round=PATH_PAYMENT_STRICT_SEND) at vOfferExchange.cpp:584:12
    frame #4: 0x0000000100000814 exec.out‘verify_wheatStays_PATH_PAYMENT_STRICT_SEND() at
      verify.cpp:54:16
    frame #5: 0x0000000100000738 exec.out‘main at verify.cpp:25:5
    frame #6: 0x000000018746eb98 dyld‘start + 6076
                                                                                              

           Fig. 7: Debugging the Seahorn Generated CEX with lldb.


comments and control flow. Our approach captures this effort in formal, machine-
checked proofs, reducing the risk of knowledge loss and making future changes
less error-prone. In this sense, formal methods act as a force multiplier on exist-
ing diligence rather than a replacement for it.
     From a research perspective, this case study exposes several concrete di-
rections that merit further investigation. First, the translation from deductive
proof artifacts (such as PVS sequents) to model checking harnesses is highly
structured and ripe for automation. Automating this step would strengthen the
connection between abstract proofs and concrete executions, enabling tighter
feedback loops. Second, richer support for model finding and counterexample
generation at the specification level would help identify underspecification ear-
lier, reducing downstream proof effort. This can be achieved by debugging an
ill-specified lemma using PVS’s integrated type-directed random tester [7] and
the PVSio ground evaluation framework [5]. Third, improving the reliability,
validation, and explainability of LLM-assisted formalization remains an open
challenge with clear industrial impact. Finally, given proof artifacts (e.g., PVS
formalizations, Seahorn unit proofs) for a codebase, maintaining them in light
of evolving specifications is highly valuable. For example, progress in generating
and deploying code changes based on updated proof artifacts ensures only proven
contributions make it to production. On the other hand, enabling the automatic
     12     J. Tafese, et al.


 1   < role >
 2   You are an expert in formal methods , program semantics , and the Prototype
 3   Verification System ( PVS ) . Your task is to translate C ++ code into a
 4   proof - oriented PVS specification that captures the intended mathematical
 5   behavior of the algorithm .
 6   </ role >
 7   < instructions >
 8   1. Read the C ++ code carefully to understand the algorithmic intent ,
 9       control flow , and arithmetic structure .
10   2. Ignore C ++ - specific operational details such as memory management ,
11       logging , profiling , and performance optimizations .
12   3. Translate the code into a PVS theory that :
13       ( a ) uses total functions ,
14       ( b ) replaces exceptions and runtime errors with explicit preconditions
15             or predicate subtypes ,
16       ( c ) models arithmetic over mathematical integers with explicit bounds .
17   4. Preserve the functional behavior of the algorithm under its intended
18       assumptions , but do NOT attempt to model full C ++ semantics .
19   5. For each inline comment or " should never happen " assertion in the C ++
20       code , introduce either :
21       ( a ) a named lemma stating the assumed invariant , or
22       ( b ) a strengthened precondition on the corresponding PVS definition .
23   6. Use idiomatic PVS syntax and structure the specification to facilitate
24       automated reasoning .
25   7. Do not attempt to prove any lemmas ; only state them precisely .
26   8. Clearly separate : ( a ) core computational definitions , ( b ) policy
            decisions ( e . g . , rounding modes ) , ( c ) assumed invariants .
27   </ instructions >
28   < example > < inputs > < cpp_code > ... </ cpp_code > </ inputs >
29   < output > < pvs_spec > ... </ pvs_spec > </ output > </ example >
30   Now generate the output for the following input . The output must be a
31   well - formed PVS theory enclosed in < output > </ output > tags .
32   < inputs > < cpp_code > $ { cpp_code } </ cpp_code > </ inputs >


              Fig. 8: LLM Prompt Template for C++ to PVS Abstraction.


     updating of proof artifacts given code changes ensures that understanding is not
     lost as a codebase evolves.
         Taken together, these observations suggest a complementary role for formal
     methods in industrial software development. Rather than insisting on full for-
     malization upfront, our approach supports incremental adoption, retrospective
     analysis, and continuous validation. This aligns naturally with how critical sys-
     tems are actually built and maintained, and it opens the door to new research
     that is directly informed by industrial constraints. We believe this perspective
     is essential for broadening the impact of formal methods and for ensuring their
     relevance to the next generation of critical and long-lived software systems.


     5    Conclusion
     We have demonstrated that PVS-based abstraction engineering and bounded
     model checking with Seahorn can enable safe, iterative evolution of legacy,
     high-value blockchain infrastructure. By combining mechanized proof and sym-
     bolic validation, we converted semi-formal, comment-based reasoning into a ver-
     ifiable and extensible correctness pipeline. Our ongoing efforts will finalize the
     specification and expand property coverage to additional components of SDEX.
    Show Me The Money: An Exercise in Proof-Driven Software Understanding            13

6      Data-Availability Statement
The data supporting the results reported in your paper can be accessed at the
following link: https://doi.org/10.5281/zenodo.20125587. We have included
an artifact in a docker environment that captures the C/C++ code, Seahorn
proofs, PVS proofs and their respective environments.

References
 1. Dutertre, B.: Yices 2.2. In: Biere, A., Bloem, R. (eds.) Computer-Aided Verification
    (CAV’2014). Lecture Notes in Computer Science, vol. 8559, pp. 737–744. Springer
    (July 2014)
 2. Floyd, R.W.: Assigning meanings to programs. In: Program Verification: Funda-
    mental Issues in Computer Science, pp. 65–81. Springer (1993)
 3. Gurfinkel, A., Kahsai, T., Komuravelli, A., Navas, J.A.: The SeaHorn Verification
    Framework. In: Kroening, D., Păsăreanu, C.S. (eds.) Computer Aided Verification.
    pp. 343–361. Springer International Publishing, Cham (2015)
 4. Hoare, C.A.R.: An axiomatic basis for computer programming. Commun. ACM
    12(10), 576–580 (Oct 1969). https://doi.org/10.1145/363235.363259, https://
    doi.org/10.1145/363235.363259
 5. Muñoz, C.: Rapid prototyping in PVS. Contractor Report NASA/CR-2003-212418,
    NASA, Langley Research Center, Hampton VA 23681-2199, USA (May 2003)
 6. Owre, S., Rushby, J.M., , Shankar, N.: PVS: A prototype verification system. In:
    Kapur, D. (ed.) 11th International Conference on Automated Deduction (CADE).
    Lecture Notes in Artificial Intelligence, vol. 607, pp. 748–752. Springer-Verlag,
    Saratoga, NY (jun 1992), http://www.csl.sri.com/papers/cade92-pvs/
 7. Owre, S.: Random testing in PVS. In: Proceedings of the First International Work-
    shop on Automated Formal Methods (AFM 06). Seattle, WA, USA (Aug 2006),
    https://fm.csl.sri.com/AFM06/papers/5-Owre.pdf, held as part of the Federated
    Logic Conference (FLoC 2006)
 8. Priya, S., Su, Y., Bao, Y., Zhou, X., Vizel, Y., Gurfinkel, A.: Bounded model
    checking for LLVM. In: Griggio, A., Rungta, N. (eds.) 22nd Formal Methods in
    Computer-Aided Design, FMCAD 2022, Trento, Italy, October 17-21, 2022. pp.
    214–224. IEEE (2022). https://doi.org/10.34727/2022/isbn.978-3-85448-053-
    22 8, https://doi.org/10.34727/2022/isbn.978-3-85448-053-22 8
 9. Priya, S., Zhou, X., Su, Y., Vizel, Y., Bao, Y., Gurfinkel, A.: Verifying verified
    code. Innov. Syst. Softw. Eng. 18(3), 335–346 (2022). https://doi.org/10.1007/
    s11334-022-00443-9, https://doi.org/10.1007/s11334-022-00443-9
10. Shostak, R.E.: Deciding combinations of theories. Journal of the ACM 31(1), 1–12
    (Jan 1984)
11. Tafese, J.: Verification Up and Down the Stack. Ph.D. thesis, University of Water-
    loo (2026), https://hdl.handle.net/10012/23030
12. Tafese, J., Garcia-Contreras, I., Gurfinkel, A.: Btor2MLIR: A Format and
    Toolchain for Hardware Verification. In: Proceedings of the 23rd Conference on
    Formal Methods in Computer-Aided Design. pp. 55–63 (2023)
13. Tafese, J., Gurfinkel, A.: Efficient Simulation for Hardware Model Checking. In:
    Bjørner, N., Heule, M., Voronkov, A. (eds.) Proceedings of 25th Conference on
    Logic for Programming, Artificial Intelligence and Reasoning. EPiC Series in Com-
    puting, vol. 100, pp. 136–146. EasyChair (2024). https://doi.org/10.29007/rdbb,
    /publications/paper/FDRF
14      J. Tafese, et al.

14. Tafese, J., Priya, S., Losa, G., Gurfinkel, A., Hoare, G.: A Tale of Two Case Stud-
    ies: A Unified Exploration of Rust Verification with SEABMC. In: Conference on
    Formal Methods in Computer-Aided Design–FMCAD 2025. pp. 262–270
