                                         CV-Rules: Serializability Verification of
                                         Concurrency Control Protocols via Explicit
                                         Transaction Ordering
                                         Takashi Hoshino #
                                         Cybozu Labs, Inc., Japan
                                         Shigeo Mitsunari #
                                         Cybozu Labs, Inc., Japan
                                         Takashi Kambayashi #
                                         NAUTILUS Technologies, Inc., Japan
                                         Ryoji Kurosawa #
arXiv:2606.25409v1 [cs.LO] 24 Jun 2026




                                         NAUTILUS Technologies, Inc., Japan
                                         Sho Nakazono #
                                         LY Corporation, Japan

                                               Abstract
                                         We present CV-rules, an alternative characterization of serializability in which a transaction order
                                         constructed by a protocol satisfies two per-read conditions, C-rule (Causality) and V-rule (View
                                         Consistency), that constrain the reads-from relation and competing writers. While classical Multi-
                                         Version Serialization Graph (MVSG) reasoning characterizes serializability via its acyclicity, our
                                         approach requires explicit order construction, enabling direct proofs that build on the protocol’s
                                         own mechanisms. We prove that CV-rules, serializability, and MVSG acyclicity are all equivalent.
                                         Moreover, the C/V separation reveals that serializability is polynomial-time decidable for any fixed
                                         bound on the width of the order forced by C-rule. We verify five protocols: Two-Phase Locking,
                                         Multi-Version Timestamp Ordering, Serial Safety Net (SSN), Aria, and SnapChain. For SSN and
                                         Aria, whose original papers defined only certification conditions, we identify explicit transaction
                                         orders arising from their mechanisms; we also prove that Aria’s unique-write constraint is unnecessary
                                         for serializability. SnapChain, in contrast, is designed directly from CV-rules, enforcing V-rule by
                                         construction. All results except the complexity bounds are mechanized in Lean with no additional
                                         axioms and no admitted goals.

                                         2012 ACM Subject Classification Information systems → Database transaction processing; Theory
                                         of computation → Logic and verification; Software and its engineering → Formal software verification

                                         Keywords and phrases Serializability, Concurrency Control, Transaction Processing, Formal Verific-
                                         ation, Theorem Proving

                                         Supplementary Material Software: https://doi.org/10.5281/zenodo.20755695 [18]


                                          1     Introduction
                                         Serializability, the requirement that a concurrent execution be equivalent to some serial one,
                                         is the canonical correctness condition for transactional concurrency. Originating in database
                                         theory [4, 28], it underlies correctness reasoning across transaction processing, replicated data
                                         stores, and transactional memory. Verifying that concurrency control protocols guarantee
                                         serializability is a fundamental and recurring problem.
                                             The classical approach to serializability verification uses the Multi-Version Serialization
                                         Graph (MVSG) [4]. A history is serializable if and only if some MVSG for it is acyclic.
                                         While theoretically elegant and well suited to protocols that directly construct dependency
                                         graphs, MVSG-based reasoning presents challenges for protocols that establish serializability
2   CV-Rules: Serializability Verification via Explicit Transaction Ordering


    through other mechanisms. The verification target is a global property (acyclicity of the
    entire dependency graph), and the serial order is a byproduct derived via topological sort,
    not an input specified by the protocol. Since order identification is not required, correctness
    proofs can establish acyclicity by contradiction without ever specifying the serial order. For
    protocols based on locks, timestamps, or certification conditions, these features of MVSG-
    based reasoning can obscure how protocol mechanisms actually establish the required ordering.
    This is particularly evident in recent protocols such as SSN [40] and Aria [24], whose original
    correctness proofs establish serializability via graph acyclicity without identifying which
    transaction order the protocol enforces.
        We propose CV-rules, a characterization of serializability that operates on a transaction
    order explicitly constructed by the protocol. Whereas MVSG identifies serializability with a
    global property (graph acyclicity), CV-rules identify it with two local per-read conditions: C-
    rule (Causality) constrains the reads-from relation, and V-rule (View Consistency) constrains
    competing writers of the same data item.
        CV-rules make protocol mechanisms visible. For SSN, we find that the protocol constructs
    a logical timestamp derived from anti-dependency analysis, a construction not explicit in
    the original work. For Aria, we show that the order combines a batch-local identifier with
    dependency-based reordering, and that Aria’s unique-write constraint is unnecessary for
    serializability. The C/V separation further reveals the complexity structure of serializability:
    V-rule’s disjunctive constraints drive its NP-hardness, and for any fixed bound on the width
    of the order forced by C-rule, the problem becomes polynomial-time decidable.
        More broadly, CV-rules continue the declarative line of work on transactional consist-
    ency [7, 12, 43], which characterizes serializability and weaker consistency levels via axioms
    relating visibility, arbitration, or execution-test structures to an ordered history. Our frame-
    work specializes to serializability while allowing partial transaction orders, enabling direct
    application to concrete protocol mechanisms.
       This paper makes the following contributions:

       Theory. We characterize serializability via two local per-read conditions (C-rule and V-
       rule) and prove their equivalence with MVSG acyclicity. We also show that serializability
       is polynomial-time decidable for any fixed bound on the width of the order forced by
       C-rule.

       Protocol verification. We verify five protocols (2PL, MVTO, SSN, Aria, and Snap-
       Chain) by explicitly constructing their transaction orders and proving CV-rules. This
       includes identifying implicit orders in existing protocols and, with SnapChain, using
       CV-rules as a design principle.

       Mechanization. All theorems are mechanically verified in Lean (∼11.2K lines across
       105 modules) with no additional axioms and no admitted goals; only the complexity
       bounds are argued informally.


        The remainder of the paper is organized as follows. Section 2 presents background
    on multi-version histories and MVSG. Section 3 defines CV-rules, proves their equivalence
    to serializability, and establishes bounded-width tractability. Section 4 establishes the
    equivalence between CV-rules and MVSG and contrasts the two approaches. Section 5 applies
    CV-rules to verify protocols. Section 6 discusses the Lean mechanization. Section 7 surveys
    prior work, and Section 8 concludes.
Hoshino et al.                                                                                              3


 2       Background
This section presents the multi-version transaction model, defines serializability via serial
execution, and recalls the classical MVSG characterization.

2.1      Multi-Version Histories
A transaction is a unit of work that reads and writes data items. We denote a read of data
item x by transaction ti as ri (x), and a write as wi (x). Following the two-step model [29],
also adopted by Bernstein et al. [4], each transaction reads and writes each data item at
most once, and we assume transactions do not read from themselves (no self-reads). These
restrictions are standard normal forms in multi-version serializability theory; histories with
repeated accesses or self-reads can be reduced to this form without affecting serializability.
    Formally, a history is defined as follows:

▶ Definition 1 (History). A history h consists of:
  A finite set D of data items.
  A finite set T of transactions.
  For each transaction t ∈ T , a set of operations ops(t) ⊆ {r(x), w(x) | x ∈ D} specifying
  which data items t reads and writes.
  A distinguished initialization transaction t0 ∈  / T with ops(t0 ) = {w(x) | x ∈ D}, i.e., t0
  writes all data items.
  A version function vf that, for each ti ∈ T and each x ∈ D with r(x) ∈ ops(ti ), specifies
  a unique transaction vf (x, ti ) ∈ T ∪ {t0 } from which ti reads x.

     The version function captures the reads-from relation: vf (x, ti ) = tj means transaction ti
reads the version of x written by tj . Note that vf (x, ti ) is only defined when r(x) ∈ ops(ti ),
i.e., when ti actually reads x. We require that the source tj = vf (x, ti ) actually writes x, i.e.,
w(x) ∈ ops(tj ), and that tj ̸= ti .
     We call this a multi-version history following the terminology of Bernstein et al. [4] (see
also [29]), though our definition differs from the classical one. The key observation, also made
by Bernstein et al. in their multi-version serializability theory, is that operation ordering
within or across transactions does not affect serializability; only the version function matters.
Accordingly, our definition omits operation orderings entirely, and the version function
abstracts over both single-version and multi-version storage. This model deliberately abstracts
away abort handling, operation-level scheduling, and real-time ordering: serializability here
is the multi-version notion of Bernstein et al., determined solely by the version function.

▶ Example 2. Consider three transactions and two data items:

     t1 : w1 (x), w1 (y)
     t2 : r2 (x), w2 (y)
     t3 : r3 (x), r3 (y)

A possible version function: vf (x, t2 ) = t1 , vf (x, t3 ) = t1 , vf (y, t3 ) = t2 . This indicates that
both t2 and t3 read x from t1 , while t3 reads y from t2 .

2.2      Serializability via Serial Execution
Serializability requires that a concurrent execution be equivalent to some serial execution.
We define this in terms of the version function.
4   CV-Rules: Serializability Verification via Explicit Transaction Ordering


        Informally, a serial execution runs transactions one at a time in some total order, where
    each transaction reads the most recent version of each data item, that is, the version written by
    the latest preceding writer. Given a total order ≺ on transactions, this naturally determines
    a version function: vf (x, ti ) is the maximum tj ≺ ti such that tj writes x. The following
    definition formalizes this idea.

    ▶ Definition 3 (Serializability). A history h is serializable if there exists a total order ≺ on
    T ∪ {t0 } (with t0 as the minimum) such that for every transaction ti ∈ T and every data
    item x that ti reads:

       vf (x, ti ) = max{tj | tj ≺ ti and w(x) ∈ ops(tj )}
                     ≺

    (The right-hand side is well-defined: t0 writes all data items and precedes every ti under ≺,
    so t0 is always in the candidate set.) In other words, the version function matches what
    would result from executing transactions serially in that order.

    ▶ Example 4. Continuing Example 2, the serial order t0 ≺ t1 ≺ t2 ≺ t3 produces exactly the
    version function given: t2 and t3 both read x from the most recent writer t1 , and t3 reads y
    from t2 (the most recent writer of y before t3 ). Thus this history is serializable.

    2.3    MVSG Characterization
    The Multi-Version Serialization Graph (MVSG) [4] provides a classical characterization of
    serializability. The construction requires a version order ≪, which is a family (≪x )x∈D
    where each ≪x is a total order on the transactions that write x (including t0 ).

    ▶ Definition 5 (MVSG). Given a history h and a version order ≪, the Multi-Version
    Serialization Graph MVSG(h, ≪) is a directed graph where:
       Nodes are transactions in T ∪ {t0 }.
       Edges capture dependencies:
           Initial: t0 → ti for all ti ∈ T .
           Reads-from: tj → ti if vf (x, ti ) = tj for some x ∈ D.
          Version-order: tk → tj if vf (x, ti ) = tj , w(x) ∈ ops(tk ), tk ∈
                                                                           / {ti , tj }, and tk ≪x tj .
           Anti-dependency: ti → tk if vf (x, ti ) = tj , w(x) ∈ ops(tk ), tk ∈         / {ti , tj }, and
           tj ≪x tk .

       Intuitively, version-order edges enforce that older writers precede newer ones, while
    anti-dependency edges ensure that readers precede later writers.
       The fundamental theorem of MVSG states:

    ▶ Theorem 6 (MVSG Theorem [4]). A history is serializable if and only if there exists a
    version order ≪ such that MVSG(h, ≪) is acyclic.

        When the MVSG is acyclic, a topological sort yields a serial order. The MVSG charac-
    terization is protocol-agnostic: it applies regardless of how the protocol operates. However,
    the verification target is a global property (acyclicity of the entire graph), and the serial
    order is derived from this graph rather than given as input. For protocols that construct
    a transaction order through their own mechanisms, MVSG-based reasoning leads to two
    complications:
    Indirect ordering. The serial order is derived from the graph structure via topological sort;
    it does not appear as an explicit input. When a protocol constructs an order directly, the
Hoshino et al.                                                                                               5


                                                                                         ≺
                        tk            tj                        ti            tk

    Figure 1 V-rule illustrated. For a read vf (x, ti ) = tj , every competing writer tk of x must precede
the source tj or follow the reader ti . The shaded zone, including incomparable positions, is forbidden.


correspondence between that order and the topological sort of the MVSG must be established
separately.
Indirect proofs. Since the MVSG framework does not require order identification, correct-
ness proofs can proceed by contradiction (assuming a cycle exists) without ever specifying
the serial order. When the order a protocol enforces is non-obvious, proofs naturally follow
this indirect strategy, establishing correctness without revealing which order the protocol
constructs.


 3      CV-rules
This section introduces CV-rules, our characterization of serializability based on explicit
transaction ordering.

3.1     Definition
3.1.1     Transaction Order
We extend the notion of history with an explicit transaction order:

▶ Definition 7 (Ordered History). An ordered history (h, ≺) consists of a history h and a
strict partial order ≺ (irreflexive and transitive) on the transactions T ∪ {t0 }, where t0 is the
minimum element: t0 ≺ t for all t ∈ T .

   The order ≺ represents the intended serialization order. A key feature is that ≺ need
only be a partial order: we do not require all transactions to be comparable.

3.1.2     C-rule (Causality)
C-rule captures the basic causality constraint: if a transaction reads data from another
transaction, the writer must precede the reader in the serialization order.

▶ Definition 8 (C-rule). An ordered history (h, ≺) satisfies C-rule if for every transaction
ti ∈ T and every data item x that ti reads from tj (i.e., vf (x, ti ) = tj ), we have tj ≺ ti .

   Intuitively, in any serial execution, a transaction can only read data that was written
before it executed. C-rule directly encodes this causal dependency.

3.1.3     V-rule (View Consistency)
C-rule requires the source to precede the reader, but not to be the most recent writer. V-rule
fills this gap by constraining how other writers of the same item are positioned.

▶ Definition 9 (V-rule). An ordered history (h, ≺) satisfies V-rule if for every transaction
ti ∈ T , every data item x that ti reads from tj (i.e., vf (x, ti ) = tj ), and every other transaction
tk ∈
   / {ti , tj } that writes x, we have tk ≺ tj or ti ≺ tk .
6   CV-Rules: Serializability Verification via Explicit Transaction Ordering


         The intuition is that if ti reads x from tj , no other write to x can interpose between tj
    and ti in the serialization order (Figure 1). If tk wrote x and appeared between tj and ti ,
    ti ’s view would break: serial execution would yield tk ’s version, not tj ’s. Note that since ≺
    is a partial order, tk being concurrent with tj or ti (i.e., incomparable) is also prohibited;
    V-rule requires an explicit ordering.

    ▶ Example 10. Consider three transactions:

       t1 : w1 (x)
       t2 : w2 (x)
       t3 : r3 (x) from t1

    V-rule for the read by t3 from t1 , considering the other writer t2 , requires: t2 ≺ t1 or t3 ≺ t2 .
    This ensures t2 ’s write does not appear between t1 and t3 in the serialization order. If t2 ≺ t1 ,
    then t3 correctly reads from t1 (the most recent). If t3 ≺ t2 , then t2 ’s write occurs after t3
    reads, so it does not break t3 ’s view.

    3.1.4     Connection to MVTO
    CV-rules generalize the correctness conditions of the Multi-Version Timestamp Ordering
    (MVTO) protocol [4, 31], in which each transaction receives a timestamp and read/write
    operations must respect the timestamp order. MVTO’s conditions are C-rule, V-rule, and
    totality of the timestamp order. While the conditions themselves reference only local
    comparisons, dropping totality makes sufficiency non-trivial: one must extend the partial
    order to a linear extension and use V-rule’s disjunctive structure to rule out intervening
    writers. Necessity, in contrast, follows directly from any serial order (Theorem 11). CV-rules
    thus characterize serializability and apply to protocols whose mechanisms are substantially
    different from timestamp ordering, as we demonstrate in Section 5.

    3.2     Main Theorem: Characterizing Serializability
    We now state and prove the main theorem: CV-rules characterize serializability.

    ▶ Theorem 11 (CV-rules Equivalence). A history h is serializable if and only if there exists a
    transaction order ≺ such that (h, ≺) satisfies both C-rule and V-rule.

    3.2.1     Proof Sketch
    Sufficiency (CV ⇒ Serializable). Given a partial order satisfying C-rule and V-rule:
    1. Apply Szpilrajn’s extension theorem ( [35]; see also [33, Theorem 10.2]), explicitly via
       topological sorting, to extend the partial order to a total order. Since the extension
       preserves existing order relations, both rules carry over.
    2. C-rule ensures tj ≺ ti , and V-rule then ensures that no other writer tk appears between
       them, so tj is the most recent writer before ti . The version function thus matches serial
       execution.

    Necessity (Serializable ⇒ CV). Given a serializable history with serial order ≺s :
    1. Use ≺s as the serialization order.
    2. C-rule: In serial execution, each read obtains the version from the most recent prior
       writer. Thus the source precedes the reader: C-rule holds.
Hoshino et al.                                                                                     7


3. V-rule: For any read from tj by ti and any other writer tk : if tj ≺ tk ≺ ti , then ti would
   read x from tk , a contradiction. Hence tk ≺ tj or ti ≺ tk : V-rule holds.

▶ Remark 12 (Complexity). Given an order ≺, checking CV-rules runs in O(|T |2 · |D|) time.
Determining whether any satisfying order exists is NP-complete [4, 28], since by Theorem 11
this is equivalent to deciding serializability.

3.3    V-rule Decomposition
V-rule can be decomposed into two independent conditions.

▶ Theorem 13 (V-rule Decomposition). Under C-rule, V-rule is equivalent to the conjunction
of:
1. Endpoint comparability. For every read vf (x, ti ) = tj and every other writer tk of x,
    tk is comparable with both ti and tj under ≺.
2. No interposition. There is no such tk with tj ≺ tk ≺ ti .

Proof sketch. V-rule ⇒ (1) ∧ (2): C-rule gives tj ≺ ti ; combining with V-rule’s disjunction and
transitivity yields comparability. (1) ∧ (2) ⇒ V-rule: if tk is comparable with both endpoints
and does not interpose, case analysis yields tk ≺ tj or ti ≺ tk .                              ◀

    This decomposition clarifies why partial orders suffice for CV-rules. Transactions on
disjoint data items need not be ordered. The decomposition shows that even among writers
of the same data item, not all pairs need be mutually comparable: endpoint comparability
only demands that each competing writer be comparable with the two endpoints of the
reads-from relationship it competes with. In particular, non-visible writes, writes whose
versions are never read [26, 38], need not be ordered among themselves.
    The decomposition also reflects how protocols ensure V-rule in practice. Endpoint
comparability often follows directly from the protocol’s ordering mechanism, while no-
interposition depends on each protocol’s specific design choices: locks, version selection, or
certification (Section 5).

3.4    Bounded-Width Tractability
As noted in Remark 12, determining serializability is NP-complete in general. The C/V
separation pinpoints the source of this hardness: the orderings forced by C-rule are uniquely
determined by the reads-from relation, while V-rule introduces disjunctive constraints: for
each competing writer tk , either tk ≺ tj or ti ≺ tk must hold. This disjunctive structure
drives the NP-hardness.
    When transaction concurrency is bounded by a fixed constant, however, the problem
becomes tractable.

▶ Definition 14 (Width). The width of a history is the maximum size of an antichain (a set
of pairwise incomparable transactions) under the partial order forced by C-rule, that is, the
transitive closure of the reads-from relation {(tj , ti ) | ∃x. vf (x, ti ) = tj }.

▶ Theorem 15 (Bounded-width decidability). For any fixed k, serializability of histories with
width at most k is decidable by a state-space search.

Proof sketch. By Dilworth’s theorem ( [13]; see also [33, Theorem 2.26]), a partial order
of width k can be partitioned into at most k chains. A chain-progress vector records, for
each chain, how far the serialization has progressed along that chain. At each state, the only
8   CV-Rules: Serializability Verification via Explicit Transaction Ordering


    candidates for placement are the at most k next unplaced transactions, one per chain, and a
    candidate is eligible only when all its predecessors in the forced ordering (including those in
    other chains) have been placed. Placing an eligible transaction advances the corresponding
    chain and is accepted only if no V-rule violation is introduced. An exhaustive search from
    the initial vector (all chains at position zero) explores all reachable states; the history
    is serializable if and only if the search reaches the final vector (all transactions placed).
    Soundness follows because every accepted transition preserves V-rule, and completeness
    because the search explores all valid placements.                                            ◀


        The state space contains O(nk ) chain-progress vectors for n transactions, so for fixed k
    the procedure runs in polynomial time. Each transition evaluates at most k candidates
    and checks V-rule in O(n · |D|) time per candidate, yielding O(nk+1 · |D|) total time for
    fixed k. Additional order constraints such as real-time or session order can be added to the
    forced relation before measuring width; for instance, session order bounds the width by the
    number of sessions. Biswas and Enea [6] showed that serializability is decidable in polynomial
    time when the number of sessions is bounded, also with O(nk ) state space. Their result is
    recovered as the special case where session order is included in the forced relation. Using the
    reads-from structure alone yields a complementary parameterization, bounded even when
    session count grows, as long as reads-from chains span sessions. The C/V separation provides
    a structural explanation of why bounded concurrency, under any parameterization, limits
    the disjunctive constraints.


    3.5    Completeness
    The necessity direction of Theorem 11 (Serializable ⇒ CV) is straightforward: the serial
    order serves as the transaction order, and C-rule and V-rule hold because the version function
    matches serial execution. This has an immediate consequence for protocol verification.

    ▶ Proposition 16 (Serial executability implies completeness). In our version-function-only
    model (Section 2.1), if a protocol can execute any sequence of transactions in a given serial
    order, then it is complete: every serializable history can be realized by the protocol.

        Because our model captures only version functions, not operation ordering, completeness
    reduces to serial executability, a condition that most protocols satisfy trivially. This does not
    contradict classical results showing, e.g., that 2PL cannot produce all conflict-serializable
    schedules [42]: those limitations concern operation ordering. Indeed, all five protocols we
    verify (Section 5) satisfy serial executability and are thus complete and equivalent at the
    version-function level: each can realize every serializable history.
        This equivalence does not imply interchangeability in practice, because our model is
    intentionally primitive: it characterizes serializability but does not distinguish protocols
    by performance. In classical theory, a protocol’s scheduling space (or scheduling power [42,
    §4.1]) is the class of serializable histories it can realize at the operation level; our model
    abstracts this axis away. However, performance depends more directly on commit rate, the
    fraction of transactions a protocol commits (rather than aborting and retrying) under a
    given workload, as demonstrated by restart-cost analysis [20], contention modeling [1], and
    workload-dependent evaluations [37, 44]. Predicting commit rate requires modeling event
    arrival and abort strategies rather than operation ordering, an extension we leave to future
    work.
Hoshino et al.                                                                                       9


 4     Equivalence with MVSG
Having established that CV-rules characterize serializability, we now prove that CV-rules are
equivalent to the classical MVSG characterization. This equivalence serves two purposes.
First, it confirms that CV-rules capture the same notion of serializability as the established
theory [4]: CV-rules do not define a new notion of correctness, but give an equivalent
characterization via a different proof methodology. Second, it allows comparing the two
approaches directly, which we do in Section 4.3.

4.1    Equivalence Theorem
▶ Theorem 17 (MVSG Equivalence). A history h satisfies CV-rules (i.e., there exists a
transaction order ≺ such that (h, ≺) satisfies both C-rule and V-rule) if and only if there exists
a version order ≪ such that MVSG(h, ≪) is acyclic.
    Combined with Theorem 11, this yields: CV-rules ⇔ MVSG Acyclicity ⇔ Serializable.
All three characterizations identify the same set of histories. While Theorem 17 could instead
be obtained by composing Theorem 11 with the classical MVSG theorem (Theorem 6),
we prove it directly: the construction exposes the structural duality between the two
characterizations that we discuss in Section 4.3.

4.2    Proof Sketch
Sufficiency (CV-rules ⇒ MVSG Acyclicity). Given a transaction order satisfying CV-rules:
1. Extend the partial order to a total order using Szpilrajn’s theorem [35].
2. Construct a version order ≪ by restricting this total order to writers of each data item.
3. Build the MVSG using this version order.
4. Acyclicity proof : Show that every MVSG edge respects the serial order.
      Initial edges: t0 ≺ ti holds since t0 is the minimum element.
      Reads-from edges: tj ≺ ti holds by C-rule.
      Version-order and anti-dependency edges: By construction, the version order agrees
      with the serial order, so tk ≪x tj implies tk ≺ tj and tj ≪x tk implies tj ≺ tk .
      A version-order edge tk → tj thus respects the serial order directly. For an anti-
      dependency edge ti → tk (which arises when tj ≪x tk , hence tk ̸≺ tj ), V-rule forces
      ti ≺ tk , so this edge respects the serial order as well.
   Since all edges respect the serial order (a total order), the graph is acyclic.

Necessity (MVSG Acyclicity ⇒ CV-rules). Given an acyclic MVSG:
1. Extract a strict partial order from the acyclic graph. Since the graph is acyclic, the edge
   relation (and its transitive closure) forms a strict partial order on transactions.
2. C-rule verification: For each reads-from edge tj → ti , the extracted order satisfies
   tj ≺ ti .
3. V-rule verification: For each read vf (x, ti ) = tj and each other writer tk , the version
   order places tk either before tj (yielding a version-order edge tk → tj , so tk ≺ tj ) or after
   tj (yielding an anti-dependency edge ti → tk , so ti ≺ tk ). Either case satisfies the V-rule
   disjunction.
   The two directions are asymmetric: necessity extracts a partial order directly from the
acyclic graph, while sufficiency must first extend the partial order to a total order. This
extension is needed because MVSG requires the version order for each data item to be total,
whereas CV-rules compare only the endpoints relevant to each read.
10   CV-Rules: Serializability Verification via Explicit Transaction Ordering


           MVSG        Derive ≪            Build MVSG           Verify acyclicity     Derive serial order


          CV-rules      Derive ≺                                                       Verify CV-rules

        Figure 2 Two verification paths for serializability. MVSG constructs a graph and checks a global
     property (acyclicity), deriving the serial order as output. CV-rules verify local per-read conditions
     against an explicitly given transaction order. Both characterize the same set of serializable histories.


     4.3     CV-rules and MVSG Compared
     Given that CV-rules and MVSG characterize the same histories, what advantages does each
     offer? The two approaches are dual in what they take as given and what they verify (Figure 2).
     MVSG builds a graph whose edges encode local relationships (reads-from, version-order,
     and anti-dependency) and verifies a global property: acyclicity of the entire graph. The
     serial order is derived from this graph as a byproduct. CV-rules take the opposite path: the
     transaction order is given as an explicit input, fixing the global structure, and verification
     reduces to checking local per-read conditions (C-rule and V-rule). The indirect ordering and
     indirect proofs noted in Section 2 are both consequences of this structural asymmetry.
         Which approach is more natural depends on how the protocol establishes serializability.
     Graph-based protocols such as IC3 [41], Janus [25], and Oze [27] construct dependency
     graphs and check acyclicity at runtime; for these, MVSG is a natural foundation. However,
     many protocols establish serializability by constructing an order. For some, the order is
     explicit in the protocol mechanism, as with lock conflicts (2PL) or timestamps (MVTO);
     for others, such as SSN and Aria, the order is left implicit, and we recover it from logical
     timestamps and batch identifiers respectively. In either case CV-rules offer a more direct path
     than MVSG: with the order in hand, the proof checks per-read conditions against it.
         Two case studies illustrate this contrast. For MVTO, both the MVSG-based proof [4]
     and our CV-rules proof rely on the same timestamp properties, but differ in how they are
     used: the MVSG proof routes them through version-order edges and graph acyclicity, while
     our CV-rules proof verifies C-rule and V-rule directly against the timestamp order. For SSN,
     the difference is more fundamental. The original proof [40] proceeds by contradiction via an
     MVSG-like dependency graph, without ever constructing a serialization order. Our CV-rules
     proof instead identifies a logical timestamp not explicit in the original work and directly
     verifies both rules (see Section 5.3).


      5      Protocol Verification
     We apply CV-rules to verify abstract models of five concurrency control protocols: Two-Phase
     Locking (2PL) [15], Multi-Version Timestamp Ordering (MVTO) [4, 31], Serial Safety Net
     (SSN) [40], Aria [24], and SnapChain. For each protocol, we establish soundness: every
     execution satisfying the protocol’s constraints is serializable. Each model considers only
     executions where all transactions satisfy the protocol’s constraints; abort handling (e.g.,
     deadlocks in 2PL, certification failures in SSN) is beyond the scope of this paper.
        Soundness proofs follow a common pattern: we build an abstract model capturing the
     protocol’s ordering and visibility constraints, construct a transaction order from the protocol’s
     mechanisms, and verify C-rule and V-rule. Each protocol, detailed below, illustrates a different
     aspect of CV-rules. 2PL derives a partial order from lock conflicts; MVTO uses predetermined
     timestamps as a total order. SSN derives a logical timestamp from dependency bounds, a
     construction not explicit in the original work. Aria combines batch ordering with dependency-
Hoshino et al.                                                                                     11


based reordering within each batch; our proof also reveals that Aria’s unique-write constraint
is unnecessary for serializability. SnapChain reverses the direction, using CV-rules as a design
principle: it enforces V-rule by construction through per-data-item view chains.
    Completeness for all five protocols holds, because they are serial-executable (Propos-
ition 16). The constructions are: 2PL acquires all locks in serial order; MVTO assigns
timestamps according to serial-order position; SSN assigns commit timestamps as serial-order
positions; Aria places each transaction in its own batch; SnapChain builds each data item’s
view chain following the serial order.

5.1     Two-Phase Locking
5.1.1    Protocol Model
A 2PL execution consists of lock and unlock events with an ordering relation. Each transaction
acquires locks before accessing data and releases them afterward. The key constraints are:
   Lock-unlock pairing: Each lock has a matching unlock.
   Two-phase discipline: For each transaction, all locks precede all unlocks.
   Mutual exclusion: Conflicting locks (same data, different transactions, at least one
   write) must be serialized: one transaction must unlock before the other locks.
We omit read/write events and derive the version function directly from the lock conflict
order, selecting the maximal prior writer for each read. This abstraction is justified by the
mutual exclusion invariant: since each read/write occurs between the corresponding lock and
unlock, conflicting accesses to the same data item are serialized by the lock conflict order,
which in turn determines the version function.

5.1.2    Order Construction
Lock conflicts naturally induce a transaction order. We define tj ≺ ti if tj unlocks data item
x before ti locks x, and the locks conflict (at least one is a write lock). The serialization
order is the transitive closure of this relation.

5.1.3    Soundness
▶ Theorem 18 (2PL Soundness). Every 2PL execution is serializable.

   The proof constructs an ordered history from the serialization order and verifies CV-rules:
   C-rule: If ti reads x from tj , then tj held a write lock on x and released it before ti
   acquired its lock. Thus tj ≺ ti .
   V-rule (via Theorem 13): Endpoint comparability: any other writer tk is ordered with
   both tj and ti by lock mutual exclusion. No interposition: tj ≺ tk ≺ ti would contradict
   the maximality of tj as version source.

5.2     Multi-Version Timestamp Ordering
5.2.1    Protocol Model
An MVTO execution maintains multiple versions of each data item and uses timestamps to
determine serialization order [4, 31]. Each transaction t receives a unique timestamp ts(t) at
the start of execution. The key components are:
   Version store: Each data item has multiple versions, each tagged with its writer t’s
   timestamp ts(t) as writeTs.
12   CV-Rules: Serializability Verification via Explicit Transaction Ordering


        Version selection: A read by transaction ti selects the version with the largest writeTs
        less than ts(ti ).
        Timestamp uniqueness: Different transactions have different timestamps; t0 has the
        minimum timestamp ts(t0 ) = 0.
     Unlike 2PL, MVTO requires no locks; concurrency is achieved through multi-versioning.


     5.2.2     Order Construction
     The serialization order is simply the timestamp order: tj ≺ ti iff ts(tj ) < ts(ti ). This is a
     total order determined at transaction start, before any data access occurs.


     5.2.3     Soundness
     ▶ Theorem 19 (MVTO Soundness). Every MVTO execution is serializable.

        The proof constructs an ordered history from the timestamp order and verifies CV-rules:
        C-rule: If ti reads x from tj , then ti selected a version with writeTs = ts(tj ). Version
        selection requires writeTs < ts(ti ), so ts(tj ) < ts(ti ), establishing tj ≺ ti .
        V-rule (via Theorem 13): Endpoint comparability is immediate since timestamps form
        a total order. No interposition: if ts(tj ) < ts(tk ) < ts(ti ), then tk ’s version would have
        been selected instead of tj ’s, a contradiction.


     5.3     Serial Safety Net
     5.3.1     Protocol Model
     SSN [40] is a verification protocol: rather than scheduling operations, it checks whether a
     given execution is serializable. Each transaction receives a unique physical commit timestamp
     ct(t). Since our model considers only committed transactions, ct is simply a given injective
     assignment from transactions to timestamps. The protocol requires that each transaction
     reads only from already-committed transactions, i.e., ct(tj ) < ct(ti ) whenever ti reads from
     tj . SSN verifies serializability by analyzing dependencies.
          An anti-dependency from ti to tj exists when ti reads a data item x and tj later writes a
     newer version of x in commit-timestamp order (i.e., tj overwrites the version ti read). For
     each transaction t, we define two sets that capture the ordering constraints SSN enforces:
        Ttforward (must precede t): (a) transactions that t reads from; (b) transactions whose
        version of some item is overwritten by t; and (c) transactions from which there is a direct
        (single-step) anti-dependency to t and that committed before t.
        Ttbackward (must follow t): transactions reachable from t via anti-dependencies, restricted
        to those that committed before t.
     From these sets, SSN’s certification values are defined as:
        η(t) = max{ct(t′ ) | t′ ∈ Ttforward } (forward constraint).
         π(t) = min({ct(t′ ) | t′ ∈ Ttbackward } ∪ {ct(t)}) (backward constraint).
     An execution is SSN-certified if η(t) < π(t) for all transactions t. Intuitively, η(t) is the latest
     commit timestamp that must precede t and π(t) the earliest that must follow it; certification
     η(t) < π(t) means these two windows are disjoint, so t can be consistently placed between its
     predecessors and successors.
Hoshino et al.                                                                                            13


                   ct

                                                             2
                                                                      t′

                                                                           backward
                                         1                                 anti-dep.
                                u
                                                                      t
                                                             3


                                                                                       π
                                    π1                           π2


                                         serialization order ≺

    Figure 3 Constructing the serialization order from ρ(t) = (π(t), −ct(t)). Transactions are ordered
primarily by π (the backward constraint); the numbered circles give the resulting order ≺. Within
one π value (here t, t′ at π2 ), the tie-break −ct places the larger commit timestamp first. This
realizes a backward anti-dependency t′ → t: t′ read a version that t overwrote, yet ct(t) < ct(t′ ), so
t ∈ Ttbackward
       ′       . The reader t′ must precede the overwriter t, so the transaction that committed later
is serialized earlier.


5.3.2     Order Construction
The original SSN paper proves serializability indirectly, by showing that the certification
condition prevents cycles in a serialization graph, but does not explicitly construct a serializ-
ation order. We show that SSN implicitly defines a logical timestamp ρ(t) that determines
the serialization order.
    We construct the order from π(t) values. However, multiple transactions may share the
same π value, so π alone does not suffice. The key observation for tie-breaking is: when
π(t) = π(t′ ) and ct(t) < ct(t′ ), an anti-dependency t′ → t connects them, requiring t′ (which
committed later but read a version that t overwrote) to precede t in the serialization order.
That is, among transactions with the same π, the physical commit order must be reversed.
    This motivates the definition ρ(t) = (π(t), −ct(t)) with lexicographic order (Figure 3),
and the serialization order is t ≺ t′ iff ρ(t) < ρ(t′ ). We call ρ a “logical timestamp” because
it differs from the physical commit order. The SSN-certified condition η(t) < π(t) ensures
that transactions preceding t (which contribute to η(t)) have ρ values less than ρ(t), since
ρ(t)1 = π(t) > η(t). A topological sort of the MVSG would also yield some linear extension
of the dependency graph, but without explicit correspondence to SSN’s runtime variables.
Instead, ρ yields the order directly from the protocol’s certification values.

5.3.3     Soundness
▶ Theorem 20 (SSN Soundness). Every SSN-certified execution is serializable.

   The proof verifies CV-rules using the logical timestamp order:
   C-rule: If ti reads from tj , then tj ∈ Ttforward
                                                 i
                                                         , so ct(tj ) ≤ η(ti ). Chaining inequalities:
   ρ(tj )1 = π(tj ) ≤ ct(tj ) ≤ η(ti ) < π(ti ) = ρ(ti )1 , hence ρ(tj ) < ρ(ti ).
   V-rule (via Theorem 13): Endpoint comparability holds because the logical timestamp
   order is total. No interposition: suppose for contradiction that tj ≺ tk ≺ ti , i.e.,
   ρ(tj ) < ρ(tk ) < ρ(ti ). First, ct(tj ) < ct(tk ) must hold; otherwise ρ(tk ) < ρ(tj ) by the
   same reasoning as C-rule (since tk ∈ Ttforward
                                               j
                                                     ), contradicting ρ(tj ) < ρ(tk ). Then tk writes
14   CV-Rules: Serializability Verification via Explicit Transaction Ordering


        a newer version of x than tj , creating an anti-dependency from ti to tk . Two cases arise
        (by ct uniqueness):
       1. ct(ti ) < ct(tk ): then ti ∈ Ttforward
                                          k
                                                   , so π(ti ) ≤ ct(ti ) ≤ η(tk ) and hence ρ(ti ) < ρ(tk ), a
           contradiction.
       2. ct(tk ) < ct(ti ): then tk ∈ Ttbackward
                                           i
                                                     . By transitivity of anti-dependencies, Ttbackward
                                                                                                     k
                                                                                                               ∪
           {tk } ⊆ Ttbackward
                      i
                              , so π(ti ) ≤  π(t k ); combined    with   ct(tk ) < ct(ti ), this gives ρ(t i ) <
           ρ(tk ), a contradiction.


     5.4     Aria
     5.4.1     Protocol Model
     Aria [24] is a deterministic concurrency control protocol based on batch execution. Trans-
     actions are organized into an ordered sequence of batches B0 , B1 , . . .. Within each batch,
     transactions receive unique identifiers called Aria-tids, denoted atid(t), and their serialization
     order is determined by dependency analysis.
         For transaction ti in batch Bn , we define the predecessor set Tiprev = {tj ∈ Bn | atid(tj ) <
     atid(ti )}. The key constraints are:
         Batch snapshot: Each batch reads from a snapshot determined by preceding batches.
         Batch B0 reads from t0 ; for n > 0, batch Bn reads from the state produced by all
         committed writes in batches B0 , . . . , Bn−1 , selecting, for each data item, the ≺-maximum
         writer among the preceding batches under the order constructed in Section 5.4.2. (This
         involves only the restriction of ≺ to B0 , . . . , Bn−1 , a total order that does not depend on
         Bn ’s own intra-batch order.)
         Dependency exclusivity: Within each batch, each transaction has at most one type
         of dependency with its predecessors. A transaction ti has a WAR dependency (write-
         after-read) if ti writes a data item that some tj ∈ Tiprev reads, and a RAW dependency
         (read-after-write) if some tj ∈ Tiprev writes a data item that ti reads. Aria requires that
         no transaction has both types simultaneously.
     The batch snapshot property ensures all transactions in a batch see a consistent state, and
     dependency exclusivity enables deterministic reordering within each batch. The original Aria
     protocol also requires unique writes per data item (no WAW dependency), but this constraint
     is unnecessary for serializability: reads are fully determined by the batch snapshot, and the
     intra-batch serialization order is fully determined by dependency exclusivity, regardless of
     write overlaps. Our proof never uses the unique-write assumption. In Aria’s original setting,
     the no-WAW constraint avoids parallel installations to the same record in its runtime-level
     concrete model, a concern outside our version-function-only model.


     5.4.2     Order Construction
     The serialization order combines batch ordering with dependency-based reordering within
     each batch:
        t0 ≺ t for all t ̸= t0 .
        Inter-batch: If ti ∈ Bm and tk ∈ Bn with m < n, then ti ≺ tk .
        Intra-batch: Within each batch, the order depends on dependency type:
           If t has a RAW dependency, then t ≺ t′ for all t′ ∈ Ttprev (reorder t before its
           predecessors).
           If t has no RAW dependency, then t′ ≺ t for all t′ ∈ Ttprev (keep predecessors before t).
Hoshino et al.                                                                                              15


Dependency exclusivity ensures the intra-batch order construction is well-defined. For any
pair (ti , tj ) in the same batch with atid(ti ) < atid(tj ), the ordering depends solely on whether
tj has a RAW dependency: if so, tj ≺ ti ; otherwise, ti ≺ tj . In particular, if ti reads and tk
writes the same data item within a batch, then ti ≺ tk regardless of Aria-tid order.

5.4.3     Soundness
▶ Theorem 21 (Aria Soundness). Every Aria execution is serializable.
   The proof verifies CV-rules using this serialization order:
   C-rule: If ti in batch Bn reads x from tj , then tj is the writer selected by the batch
   snapshot of Bn at x. If tj = t0 , then t0 ≺ ti by the base rule. Otherwise, tj belongs to
   some earlier batch Bm with m < n, so tj ≺ ti by inter-batch ordering.
   V-rule: Consider ti in batch Bn reading x from tj , and another writer tk of x. If tk is
   in a batch before Bn , then tk ≺ tj because the snapshot selects the maximum writer
   and tk ̸= tj . Otherwise tk is in Bn or later, giving ti ≺ tk : by intra-batch ordering
   (dependency exclusivity ensures readers precede writers of the same item) if tk ∈ Bn , or
   by inter-batch ordering if tk is in a later batch.

5.5     SnapChain
5.5.1     Protocol Model
The preceding four protocols were designed independently and verified against CV-rules after
the fact. SnapChain demonstrates the reverse direction: using CV-rules as a starting point
for design. SnapChain uses per-data-item view chains (ordered slots of writers and readers)
to enforce V-rule by construction.
    For each data item x, a view chain is a list of slots [(W0 , R0 , M0 ), (W1 , R1 , M1 ), . . .]. Each
slot corresponds to a version of x: the writers produce the version, the readers consume it,
and a read-modify-write (rmw) transaction both consumes the current version and produces
the next.
    Ws (writers): a non-empty set of transactions that write x at this position.
    Rs (readers): transactions that read x from the writer of this slot without writing x.
    Ms (rmw): a set of at most one transaction that reads from this slot’s writer and writes
    the next version of x.
The initial slot has W0 = {t0 }. If a slot has readers or an rmw (Rs ∪ Ms =     ̸ ∅), then |Ws | = 1:
readers see a unique version. If Ms = {t}, then slot s + 1 exists with Ws+1 = {t}.
    Each transaction t has start and end events with a partial order: end(t0 ) < start(t) for
      ̸ t0 , and start(t) < end(t). A transaction can only observe effects of transactions that
all t =
ended before it started. This determines its snapshot. Each transaction t ̸= t0 that accesses
x is placed in the view chain based on its unique visible slot: the latest slot containing a
member t′ that accesses x and satisfies end(t′ ) < start(t). Read-only transactions join Rs ,
blind writers join Ws+1 , and rmw transactions join both Ms and Ws+1 . The version function
is derived from the chain: if ti ∈ Rs ∪ Ms , it reads from the unique writer in Ws .
    In practice, determining the visible slot requires observing which transactions have
completed before a new transaction starts. Our model takes this information as given.

5.5.2     Order Construction
The serialization order is built from per-data-item constraints. For each data item x, the
per-data order is generated by:
16   CV-Rules: Serializability Verification via Explicit Transaction Ordering


         Intra-slot: Ws ≺ Rs ≺ Ms .
         Cross-slot: When Ms = ∅, Ws ∪ Rs ≺ Ws+1 . When Ms = {t}, t bridges slot s and s + 1
         as it appears in both Ms and Ws+1 .
     The serialization order is the transitive closure of the union of all per-data orders. This
     requires that per-data orders from different data items are mutually consistent; when they
     are not, some transactions must be aborted to restore consistency. The model assumes that
     committed transactions generate a consistent global order; abort strategies are outside the
     scope.

     5.5.3      Soundness
     ▶ Theorem 22 (SnapChain Soundness). Every SnapChain execution is serializable.

          The proof verifies CV-rules using the serialization order:
          C-rule: tj ∈ Ws and ti ∈ Rs ∪ Ms for some slot s; the intra-slot ordering gives tj ≺ ti .
          V-rule: Since |Ws | = 1, tk appears in slot s′ =
                                                         ̸ s. If s′ < s, the slot ordering gives tk ≺ tj ;
          if s < s′ , it gives ti ≺ tk .

      6      Mechanization in Lean
     All theorems in this paper are mechanically verified in Lean (version 4.31.0). The artifact,
     including build instructions and a mapping from paper theorems to Lean definitions, is
     available as supplementary material [18]. The proof development comprises about 11.2K
     lines of code across 105 modules, with zero axioms and zero admitted goals. “Zero axioms”
     means our development adds no axioms beyond those already provided by Lean’s standard
     library; there are no axiom declarations of our own. “Zero admitted goals” means every
     proof obligation is fully discharged; there are no gaps marked with sorry. Together, these
     properties ensure that anyone can independently verify the correctness of our theorems by
     running the Lean type checker.

     6.1     Proof Statistics
     Table 1 summarizes the proof development. The core theory includes CV-rules definitions,
     the characterization theorem, order-theoretic lemmas, and version function correctness. The
     bounded-width component formalizes Dilworth’s theorem and the state-space search decision
     procedure. Protocol implementations vary in complexity: MVTO is the largest because it
     explicitly formalizes version selection from a multi-version store, while Aria is the smallest.

     6.2     Implementation Notes
     A notable implementation detail is representing SSN’s logical timestamps ρ(t) = (π(t), −ct(t))
     as a lexicographic pair of natural numbers with the order on the second component reversed.
     Keeping both components in N avoids non-negativity invariants and lets standard arithmetic
     tactics apply directly, which simplifies the proofs. The injectivity of ρ (needed to ensure the
     serialization order is well-defined) then reduces to the injectivity of commit timestamps.
         We adopted the decomposed V-rule approach (Theorem 13) for 2PL, MVTO, and SSN.
     For Aria, the batch position of the competing writer relative to the reader and the snapshot
     source uniquely determines which disjunct of V-rule holds in each case, making decomposition
     unnecessary. For 2PL and MVTO, the decomposition automatically determines the case
     splits but increases the number of cases compared to a non-decomposed proof; however, the
Hoshino et al.                                                                                     17


     Table 1 Proof development metrics (Defs = definitions, LOC = lines of code)

                Component             Modules    Defs   Lemmas           LOC(%)
                Core Theory               16      49       114       2,145( 19.2)
                MVSG Equivalence            3     18        11         538( 4.8)
                Bounded Width               9     29        69       1,579( 14.2)
                Protocol Common             4       3       15         150( 1.3)
                2PL                       13      25        48       1,220( 10.9)
                MVTO                      22      23        88       2,152( 19.3)
                SSN                       14      24        55       1,120( 10.0)
                Aria                      10      24        48         991( 8.9)
                SnapChain                 14      32        58       1,258( 11.3)
                Total                    105     227       506     11,153(100.0)


additional cases are trivial (five cases for 2PL, four for MVTO, each a few lines), so the
overhead is negligible. For SSN, the decomposition conversely reduces the number of cases
from six to four, because the hypotheses of the no-interposition obligation cover and merge
case distinctions that a non-decomposed proof must handle separately. SnapChain instead
verifies V-rule directly from its view-chain slot structure, without the decomposition.
    The bounded-width tractability result (Section 3.4) required formalizing Dilworth’s
theorem and the entire state-space search pipeline as a verified decision procedure. The
mechanization establishes that reachability in the state space is equivalent to serializability
(soundness and completeness) and that reachability is decidable, with search termination
proved via a monotonically decreasing measure on unplaced transactions. The complexity
claims are informal, since formalizing complexity bounds in Lean remains a significant
undertaking.


 7      Related Work

7.1     Serializability Characterizations
The classical theory of serializability developed from single-version to multi-version settings,
and from conflict-based to view-based definitions. For single-version histories, conflict
serializability, characterized by acyclicity of the serialization graph [15], is decidable in
polynomial time, while view serializability is NP-complete [28]. Bernstein et al. [4,5] extended
these ideas to multi-version histories with the Multi-Version Serialization Graph (MVSG),
where a history is serializable if and only if some version order makes the MVSG acyclic.
These graph-based approaches characterize serializability via acyclicity of a dependency
graph, without requiring a serialization order as input. Biswas and Enea [6] systematically
studied the complexity of checking consistency models including serializability, showing that
it is decidable in polynomial time for any fixed bound on the number of sessions.
     More recent frameworks adopt declarative specifications. Cerone et al. [7] proposed
an axiomatic framework using visibility (VIS) and arbitration (AR) relations, defining a
hierarchy from Read Atomic to Serializability. AR is a total order at all levels; VIS varies by
isolation level, becoming total and equal to AR at serializability. Cerone and Gotsman [8]
extended this to characterize Snapshot Isolation via dependency graphs, with applications to
transaction chopping and robustness [3]. Crooks et al. [12] introduced state-based definitions
where executions form a totally ordered sequence of states. Xiong et al. [43] developed
operational semantics for distributed key-value stores with execution tests, where the derived
transaction order can be partial; however, their model assumes last-write-wins (LWW),
18   CV-Rules: Serializability Verification via Explicit Transaction Ordering


     making it difficult to model protocols like MVTO (timestamp-based version selection) or
     Aria (batch-snapshot-based reading).
         Our CV-rules characterization differs in two key aspects: (1) we work with partial orders
     rather than total orders, unlike Cerone’s framework where AR’s totality anchors the most-
     recent-writer rule of its external-consistency axiom (EXT); V-rule’s disjunctive structure
     instead localizes comparability to each read-from edge, allowing protocols like 2PL to use
     their natural lock conflict order directly; (2) we provide per-read conditions (verifying C-
     rule and V-rule per read-from edge) with an explicit transaction order, rather than graph
     acyclicity conditions [4,8]. Moreover, the C/V separation reveals the computational structure
     of serializability.

     7.2    Protocol Verification
     Concurrency control protocols can be classified by how they construct serialization order:
     lock-based protocols (2PL [15], Silo [39], Orthrus [32], 2PLSF [30]) derive order from lock
     conflicts; timestamp-based protocols (MVTO [31], TicToc [45], Cicada [23]) use timestamps
     directly; graph-based protocols (IC3 [41], Janus [25], Oze [27]) infer order via topological
     sort of acyclic dependency graphs. SSN [40] and Aria [24] are notably different: they
     define conditions for committing transactions without explicit order construction, leaving
     the underlying serialization order implicit. Classical protocols like 2PL and MVTO have
     well-established correctness proofs in textbooks [5, 42].
         To our knowledge, this paper provides the first explicit order constructions for SSN and
     Aria, within a unified framework that also covers 2PL, MVTO, and SnapChain.

     7.3    Formal and Automated Verification
     Mechanized verification of concurrency control varies in what is verified and how serializability
     is established. Implementation verification: vMVCC [10] and DaisyNFS [9] prove that
     concrete implementations correctly realize a transactional specification using Iris/Perennial in
     Coq; these proofs are protocol-specific and tightly coupled to implementation details. Abstract
     protocol models: Chkliaev et al. [11] verified 2PL in PVS via conflict-preserving timestamps;
     Lesani et al. [21] and Doherty et al. [14] verified STM in PVS using I/O automata, requiring
     total order for committed transactions. C4 [22] formulates serializability as linearizability;
     VerIso [16] proves refinement to abstract serial schedules in Isabelle/HOL, discovering a bug
     in TAPIR [46], though it inherits LWW limitations from Xiong et al. [43]. Mathiasen et al. [2]
     specify weak isolation levels for client reasoning rather than characterizing serializability.
     Runtime checking: Cobra [36], Elle [19], and their successors [17, 34] check recorded traces
     post hoc rather than proving correctness for all executions.
         CV-rules directly characterize serializability, as both necessary and sufficient conditions,
     via per-read conditions on explicit partial orders. They differ from the approaches above in
     three respects: they abstract away implementation details (cf. vMVCC, DaisyNFS); they
     prove correctness for all executions rather than verifying individual ones (cf. Cobra, Elle);
     and they require neither total orders [14, 21] nor LWW semantics [43].


      8     Conclusion
     We presented CV-rules, a characterization of serializability via two local per-read conditions
     (C-rule and V-rule) on an explicit transaction order, and proved their equivalence with MVSG
     acyclicity. We also showed that any fixed bound on the width of the order forced by C-rule
Hoshino et al.                                                                                        19


yields polynomial-time decidability. Using this framework, we verified 2PL, MVTO, SSN,
Aria, and SnapChain, identifying explicit order constructions for SSN and Aria whose original
papers provided only certification conditions. Furthermore, we found that Aria’s unique-write
constraint is unnecessary for serializability, and we used CV-rules as a design principle for
SnapChain. All results except the complexity bounds are mechanized in Lean (∼11.2K lines).
    Future work includes applying CV-rules as a design principle to develop protocols with
greater scheduling power and lower overhead. Another direction is bridging the gap between
scheduling power and deployment performance by extending the verification framework to
incorporate abort handling and workload models.


     References
 1   Rakesh Agrawal, Michael J. Carey, and Miron Livny. Concurrency control performance
     modeling: alternatives and implications. ACM Trans. Database Syst., 12(4):609–654, November
     1987. doi:10.1145/32204.32220.
 2   Anders Alnor Mathiasen, Léon Gondelman, Léon Ducruet, Amin Timany, and Lars Birkedal.
     Reasoning about Weak Isolation Levels in Separation Logic. Proc. ACM Program. Lang.,
     9(ICFP), August 2025. doi:10.1145/3747515.
 3   Giovanni Bernardi and Alexey Gotsman. Robustness against Consistency Models with Atomic
     Visibility. In CONCUR, pages 7:1–7:15, 2016. doi:10.4230/LIPIcs.CONCUR.2016.7.
 4   Philip A. Bernstein and Nathan Goodman. Multiversion Concurrency Control—Theory and
     Algorithms. ACM Trans. Database Syst., 8(4):465–483, December 1983. doi:10.1145/319996.
     319998.
 5   Philip A. Bernstein, Vassos Hadzilacos, and Nathan Goodman. Concurrency Control and
     Recovery in Database Systems. Addison-Wesley Longman Publishing Co., Inc., USA, 1987.
 6   Ranadeep Biswas and Constantin Enea. On the Complexity of Checking Transactional
     Consistency. Proc. ACM Program. Lang., 3(OOPSLA), October 2019. doi:10.1145/3360591.
 7   Andrea Cerone, Giovanni Bernardi, and Alexey Gotsman. A Framework for Transactional
     Consistency Models with Atomic Visibility. In 26th International Conference on Concurrency
     Theory, CONCUR 2015, Madrid, Spain, September 1-4, 2015, volume 42 of LIPIcs, pages
     58–71. Schloss Dagstuhl - Leibniz-Zentrum für Informatik, 2015. doi:10.4230/LIPICS.CONCUR.
     2015.58.
 8   Andrea Cerone and Alexey Gotsman. Analysing Snapshot Isolation. In Proceedings of the
     2016 ACM Symposium on Principles of Distributed Computing, PODC ’16, pages 55–64, New
     York, NY, USA, 2016. ACM. doi:10.1145/2933057.2933096.
 9   Tej Chajed, Joseph Tassarotti, Mark Theng, M. Frans Kaashoek, and Nickolai Zeldovich.
     Verifying the DaisyNFS concurrent and crash-safe file system with sequential reasoning. In
     16th USENIX Symposium on Operating Systems Design and Implementation (OSDI 22), pages
     447–463, Carlsbad, CA, July 2022. USENIX Association.
10   Yun-Sheng Chang, Ralf Jung, Upamanyu Sharma, Joseph Tassarotti, M. Frans Kaashoek, and
     Nickolai Zeldovich. Verifying vMVCC, a high-performance transaction library using multi-
     version concurrency control. In 17th USENIX Symposium on Operating Systems Design and
     Implementation, OSDI 2023, Boston, MA, USA, July 10-12, 2023, pages 871–886. USENIX
     Association, 2023.
11   Dmitri Chkliaev, Jozef Hooman, and Peter van der Stok. Serializability Preserving Extensions
     of Concurrency Control Protocols. In Perspectives of System Informatics, Third International
     Andrei Ershov Memorial Conference, PSI’99, Akademgorodok, Novosibirsk, Russia, July 6-9,
     1999, Proceedings, volume 1755 of Lecture Notes in Computer Science, pages 180–193. Springer,
     1999. doi:10.1007/3-540-46562-6\_15.
12   Natacha Crooks, Youer Pu, Lorenzo Alvisi, and Allen Clement. Seeing is believing: A client-
     centric specification of database isolation. In Proceedings of the ACM Symposium on Principles
20   CV-Rules: Serializability Verification via Explicit Transaction Ordering


          of Distributed Computing, PODC ’17, page 73–82, New York, NY, USA, 2017. Association for
          Computing Machinery. doi:10.1145/3087801.3087802.
     13   Robert P. Dilworth. A Decomposition Theorem for Partially Ordered Sets. Annals of
          Mathematics, 51(1):161–166, 1950. doi:10.2307/1969503.
     14   Simon Doherty, Lindsay Groves, Victor Luchangco, and Mark Moir. Towards Formally Spe-
          cifying and Verifying Transactional Memory. Form. Asp. Comput., 25(5):769–799, September
          2013. doi:10.1007/s00165-012-0225-8.
     15   K. P. Eswaran, J. N. Gray, R. A. Lorie, and I. L. Traiger. The Notions of Consistency and
          Predicate Locks in a Database System. Commun. ACM, 19(11):624–633, November 1976.
          doi:10.1145/360363.360369.
     16   Shabnam Ghasemirad, Si Liu, Christoph Sprenger, Luca Multazzu, and David A. Basin.
          VerIso: Verifiable Isolation Guarantees for Database Transactions. Proc. VLDB Endow.,
          18(5):1362–1375, 2025. doi:10.14778/3718057.3718065.
     17   Long Gu, Si Liu, Tiancheng Xing, Hengfeng Wei, Yuxing Chen, and David Basin. IsoVista:
          Black-Box Checking Database Isolation Guarantees. Proceedings of the VLDB Endowment,
          17(12):4325–4328, 2024. doi:10.14778/3685800.3685866.
     18   Takashi Hoshino. Lean 4 Mechanization of CV-Rules. Zenodo, 2026. doi:10.5281/zenodo.
          20755695.
     19   Kyle Kingsbury and Peter Alvaro. Elle: Inferring Isolation Anomalies from Experimental
          Observations. Proceedings of the VLDB Endowment, 14(3):268–280, 2020. doi:10.14778/
          3430915.3430918.
     20   H. T. Kung and John T. Robinson. On Optimistic Methods for Concurrency Control. ACM
          Trans. Database Syst., 6(2):213–226, June 1981. doi:10.1145/319566.319567.
     21   Mohsen Lesani, Victor Luchangco, and Mark Moir. A Framework for Formally Verifying
          Software Transactional Memory Algorithms. In CONCUR 2012 - Concurrency Theory - 23rd
          International Conference, volume 7454 of Lecture Notes in Computer Science, pages 516–530.
          Springer, 2012. doi:10.1007/978-3-642-32940-1\_36.
     22   Mohsen Lesani, Li-yao Xia, Anders Kaseorg, Christian J. Bell, Adam Chlipala, Benjamin C.
          Pierce, and Steve Zdancewic. C4: verified transactional objects. Proc. ACM Program. Lang.,
          6(OOPSLA1):1–31, 2022. doi:10.1145/3527324.
     23   Hyeontaek Lim, Michael Kaminsky, and David G. Andersen. Cicada: Dependably Fast Multi-
          Core In-Memory Transactions. In Proceedings of the 2017 ACM International Conference
          on Management of Data, SIGMOD ’17, pages 21–35, New York, NY, USA, 2017. ACM.
          doi:10.1145/3035918.3064015.
     24   Yi Lu, Xiangyao Yu, Lei Cao, and Samuel Madden. Aria: A Fast and Practical Deterministic
          OLTP Database. Proc. VLDB Endow., 13(12):2047–2060, July 2020. doi:10.14778/3407790.
          3407808.
     25   Shuai Mu, Lamont Nelson, Wyatt Lloyd, and Jinyang Li. Consolidating Concurrency Control
          and Consensus for Commits under Conflicts. In 12th USENIX Symposium on Operating
          Systems Design and Implementation (OSDI 16), pages 517–532, Savannah, GA, November
          2016. USENIX Association.
     26   Sho Nakazono, Hiroyuki Uchiyama, Yasuhiro Fujiwara, Yasuhiro Nakamura, and Hideyuki
          Kawashima. NWR: Rethinking Thomas Write Rule for Omittable Write Operations, 2020.
          arXiv preprint. doi:10.48550/ARXIV.1904.08119.
     27   Jun Nemoto, Takashi Kambayashi, Takashi Hoshino, and Hideyuki Kawashima. Oze: De-
          centralized Graph-Based Concurrency Control for Long-Running Update Transactions. Proc.
          VLDB Endow., 18(8):2321–2333, April 2025. doi:10.14778/3742728.3742730.
     28   Christos H. Papadimitriou. The Serializability of Concurrent Database Updates. J. ACM,
          26(4):631–653, October 1979. doi:10.1145/322154.322158.
     29   Christos H. Papadimitriou and Paris C. Kanellakis. On Concurrency Control by Multiple
          Versions. ACM Trans. Database Syst., 9(1):89–99, March 1984. doi:10.1145/348.318588.
Hoshino et al.                                                                                    21


30   Pedro Ramalhete, Andreia Correia, and Pascal Felber. 2PLSF: Two-Phase Locking with
     Starvation-Freedom. In Proceedings of the 28th ACM SIGPLAN Annual Symposium on
     Principles and Practice of Parallel Programming, PPoPP ’23, pages 39–51, New York, NY,
     USA, 2023. ACM. doi:10.1145/3572848.3577433.
31   D. P. Reed. Naming and Synchronization in a Decentralized Computer System. Technical
     report, Massachusetts Institute of Technology, Cambridge, MA, USA, 1978.
32   Kun Ren, Jose M. Faleiro, and Daniel J. Abadi. Design Principles for Scaling Multi-core
     OLTP Under High Contention. In Proceedings of the 2016 International Conference on
     Management of Data, SIGMOD ’16, pages 1583–1598, New York, NY, USA, 2016. ACM.
     doi:10.1145/2882903.2882958.
33   Bernd Schröder. Ordered Sets.       Birkhäuser Cham, 2 edition, 2016.       doi:10.1007/
     978-3-319-29788-0.
34   Weihua Sun and Zhaonian Zou. Vbox: Efficient Black-Box Serializability Verification, 2025.
     arXiv preprint. doi:10.48550/arXiv.2503.05163.
35   Edward Szpilrajn. Sur l’extension de l’ordre partiel. Fundamenta Mathematicae, 16:386–389,
     1930. doi:10.4064/fm-16-1-386-389.
36   Cheng Tan, Changgeng Zhao, Shuai Mu, and Michael Walfish. Cobra: Making Transactional
     Key-Value Stores Verifiably Serializable. In 14th USENIX Symposium on Operating Systems
     Design and Implementation (OSDI 20), pages 63–80. USENIX Association, November 2020.
37   Takayuki Tanabe, Takashi Hoshino, Hideyuki Kawashima, and Osamu Tatebe. An Analysis of
     Concurrency Control Protocols for In-Memory Database with CCBench. Proc. VLDB Endow.,
     13(13):3531–3544, 2020. doi:10.14778/3424573.3424575.
38   Robert H. Thomas. A Majority Consensus Approach to Concurrency Control for Multiple Copy
     Databases. ACM Trans. Database Syst., 4(2):180–209, 1979. doi:10.1145/320071.320076.
39   Stephen Tu, Wenting Zheng, Eddie Kohler, Barbara Liskov, and Samuel Madden. Speedy
     Transactions in Multicore In-memory Databases. In Proceedings of the Twenty-Fourth ACM
     Symposium on Operating Systems Principles, SOSP ’13, pages 18–32, New York, NY, USA,
     2013. ACM. doi:10.1145/2517349.2522713.
40   Tianzheng Wang, Ryan Johnson, Alan Fekete, and Ippokratis Pandis. Efficiently Making
     (Almost) Any Concurrency Control Mechanism Serializable. The VLDB Journal, 26(4):537–562,
     August 2017. doi:10.1007/s00778-017-0463-8.
41   Zhaoguo Wang, Shuai Mu, Yang Cui, Han Yi, Haibo Chen, and Jinyang Li. Scaling Multicore
     Databases via Constrained Parallel Execution. In Proceedings of the 2016 International
     Conference on Management of Data, SIGMOD ’16, pages 1643–1658, New York, NY, USA,
     2016. ACM. doi:10.1145/2882903.2882934.
42   Gerhard Weikum and Gottfried Vossen. Transactional Information Systems: Theory, Al-
     gorithms, and the Practice of Concurrency Control and Recovery. Morgan Kaufmann Publishers
     Inc., San Francisco, CA, USA, 2002.
43   Shale Xiong, Andrea Cerone, Azalea Raad, and Philippa Gardner. Data Consistency in
     Transactional Storage Systems: A Centralised Semantics. In 34th European Conference
     on Object-Oriented Programming, ECOOP 2020, Berlin, Germany (Virtual Conference),
     November 15-17, 2020, volume 166 of LIPIcs, pages 21:1–21:31. Schloss Dagstuhl - Leibniz-
     Zentrum für Informatik, 2020. doi:10.4230/LIPICS.ECOOP.2020.21.
44   Xiangyao Yu, George Bezerra, Andrew Pavlo, Srinivas Devadas, and Michael Stonebraker.
     Staring into the Abyss: An Evaluation of Concurrency Control with One Thousand Cores.
     Proc. VLDB Endow., 8(3):209–220, November 2014. doi:10.14778/2735508.2735511.
45   Xiangyao Yu, Andrew Pavlo, Daniel Sanchez, and Srinivas Devadas. TicToc: Time Traveling
     Optimistic Concurrency Control. In Proceedings of the 2016 International Conference on
     Management of Data, SIGMOD ’16, pages 1629–1642, New York, NY, USA, 2016. ACM.
     doi:10.1145/2882903.2882935.
22   CV-Rules: Serializability Verification via Explicit Transaction Ordering


     46   Irene Zhang, Naveen Kr. Sharma, Adriana Szekeres, Arvind Krishnamurthy, and Dan R. K.
          Ports. Building Consistent Transactions with Inconsistent Replication. ACM Trans. Comput.
          Syst., 35(4), December 2018. doi:10.1145/3269981.
